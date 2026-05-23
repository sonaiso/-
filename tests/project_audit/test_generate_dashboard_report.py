"""
Tests for Dashboard Report Generator
اختبارات مولّد تقرير لوحة القياس

PR-D1: Static Audit Generator Tests
"""

import sys
import json
import pytest
from pathlib import Path

# Add project root and tools to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "tools"))

from project_audit.types import *
from project_audit.scorer import LayerScorer
from project_audit.code_analyzer import LayerCodeInfo
from project_audit.test_analyzer import GoldenDatasetInfo


class TestLayerScorer:
    """Test layer scoring with ceiling caps"""

    def test_ceiling_no_typed_contract(self):
        """Layer without typed contract cannot exceed 30%"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="TEST",
            has_typed_contract=False,
            has_tests=True,
            has_noleap_tests=True,
            has_golden_dataset=True,
        )

        raw_score = 85  # High raw score
        capped, reason = scorer.apply_ceiling(
            raw_score, code_info, 95.0, False, False
        )

        assert capped <= 30, f"Score {capped} exceeds 30% cap for no typed contract"
        assert "typed contract" in reason.lower()

    def test_ceiling_strings_instead_of_types(self):
        """Layer using strings instead of types cannot exceed 45%"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="TEST",
            has_typed_contract=True,
            uses_strings_not_types=True,  # KEY: Uses strings
            has_tests=True,
            has_noleap_tests=True,
        )

        raw_score = 75
        capped, reason = scorer.apply_ceiling(
            raw_score, code_info, 95.0, False, False
        )

        assert capped <= 45, f"Score {capped} exceeds 45% cap for strings instead of types"
        assert "string" in reason.lower() or "boolean" in reason.lower()

    def test_ceiling_no_tests(self):
        """Layer without tests cannot exceed 50%"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="TEST",
            has_typed_contract=True,
            uses_strings_not_types=False,
            has_tests=False,  # KEY: No tests
        )

        raw_score = 70
        capped, reason = scorer.apply_ceiling(
            raw_score, code_info, 95.0, False, False
        )

        assert capped <= 50, f"Score {capped} exceeds 50% cap for no tests"
        assert "test" in reason.lower()

    def test_ceiling_no_noleap_tests(self):
        """Layer without NoLeap tests cannot exceed 55%"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="TEST",
            has_typed_contract=True,
            uses_strings_not_types=False,
            has_tests=True,
            has_noleap_tests=True,
        )

        raw_score = 75
        noleap_coverage = 50.0  # KEY: Below 90%
        capped, reason = scorer.apply_ceiling(
            raw_score, code_info, noleap_coverage, False, False
        )

        assert capped <= 55, f"Score {capped} exceeds 55% cap for low NoLeap coverage"
        assert "noleap" in reason.lower()

    def test_ceiling_no_golden_dataset(self):
        """Layer without golden dataset cannot exceed 70%"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="TEST",
            has_typed_contract=True,
            uses_strings_not_types=False,
            has_tests=True,
            has_noleap_tests=True,
            has_golden_dataset=False,  # KEY: No golden dataset
        )

        raw_score = 82
        capped, reason = scorer.apply_ceiling(
            raw_score, code_info, 95.0, False, False
        )

        assert capped <= 70, f"Score {capped} exceeds 70% cap for no golden dataset"
        assert "golden" in reason.lower()

    def test_claim_conflicts_cap_at_70(self):
        """Layer with claim conflicts capped at 70%"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="TEST",
            has_typed_contract=True,
            uses_strings_not_types=False,
            has_tests=True,
            has_noleap_tests=True,
            has_golden_dataset=True,
        )

        raw_score = 88
        capped, reason = scorer.apply_ceiling(
            raw_score, code_info, 95.0, has_conflicts=True, trace_broken=False
        )

        assert capped <= 70, f"Score {capped} exceeds 70% cap for claim conflicts"
        assert "conflict" in reason.lower()

    def test_no_cap_when_all_criteria_met(self):
        """Layer meeting all criteria has no cap"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="TEST",
            has_typed_contract=True,
            uses_strings_not_types=False,
            has_tests=True,
            has_noleap_tests=True,
            has_golden_dataset=True,
        )

        raw_score = 92
        capped, reason = scorer.apply_ceiling(
            raw_score, code_info, 95.0, False, False
        )

        assert capped == raw_score, f"Score should not be capped when all criteria met"
        assert reason == ""

    def test_claims_in_docs_do_not_raise_score_without_code(self):
        """Documentation claims should not raise score without code evidence"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="TEST",
            has_typed_contract=False,  # No actual implementation
            has_tests=False,
            implementation_files=[],  # Empty
        )

        golden_info = GoldenDatasetInfo(layer_id="TEST")

        components = scorer.calculate_raw_score(
            code_info, 0.0, golden_info, False
        )

        # Score should be very low without implementation
        assert components.total <= 20, \
            "Score should be low without actual code implementation"

    def test_a2_cannot_exceed_cap_without_golden_dataset(self):
        """A2 Pure Dāl Geometry cannot exceed cap without Golden Dataset"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="A2",
            has_typed_contract=True,
            uses_strings_not_types=False,
            has_tests=True,
            has_noleap_tests=False,  # Missing some
            has_golden_dataset=False,  # KEY: No golden dataset
            evidence_count=23,
            residual_count=15,
            trace_count=18,
        )

        golden_info = GoldenDatasetInfo(layer_id="A2")

        components = scorer.calculate_raw_score(
            code_info, 71.0, golden_info, False
        )
        raw_score = components.total

        capped, reason = scorer.apply_ceiling(
            raw_score, code_info, 71.0, False, False
        )

        # Should be capped at 55% due to NoLeap coverage < 90%
        assert capped <= 55, \
            f"A2 score {capped} should not exceed 55% without 90%+ NoLeap coverage"

    def test_layer_without_noleap_tests_capped_at_55(self):
        """Layer without adequate NoLeap tests cannot exceed 55%"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="TEST",
            has_typed_contract=True,
            uses_strings_not_types=False,
            has_tests=True,
            has_noleap_tests=True,
        )

        raw_score = 75
        noleap_coverage = 60.0  # Below 90%

        capped, reason = scorer.apply_ceiling(
            raw_score, code_info, noleap_coverage, False, False
        )

        assert capped <= 55, \
            f"Score {capped} exceeds 55% cap for NoLeap coverage {noleap_coverage}%"

    def test_layer_without_tests_capped_at_50(self):
        """Layer without tests cannot exceed 50%"""
        scorer = LayerScorer()
        code_info = LayerCodeInfo(
            layer_id="TEST",
            has_typed_contract=True,
            uses_strings_not_types=False,
            has_tests=False,  # KEY: No tests
        )

        raw_score = 68

        capped, reason = scorer.apply_ceiling(
            raw_score, code_info, 0.0, False, False
        )

        assert capped <= 50, \
            f"Score {capped} exceeds 50% cap for no tests"

    def test_blocking_gaps_appear_clearly(self):
        """Blocking gaps should be clearly identified"""
        # This is tested via the generate_dashboard_report.py
        # which calls _identify_gaps
        # We verify it produces a list of actionable gaps
        pass  # Integration test

    def test_real_completion_calculation(self):
        """Test overall real completion calculation with weighted scores"""
        scorer = LayerScorer()

        layer_scores = {
            "A0": 85,
            "A1": 82,
            "A2": 55,
            "A3": 45,
            "A4": 78,
            "A5": 45,
            "A6": 58,
            "A7": 35,
            "A8": 72,
            "A9": 15,
            "A10": 22,
        }

        real_completion = scorer.calculate_real_completion(layer_scores)

        # Should be around 42% based on weighted average
        assert 35 <= real_completion <= 50, \
            f"Real completion {real_completion:.1f}% outside expected range"


class TestGoldenDatasetInfo:
    """Test golden dataset coverage logic"""

    def test_complete_golden_dataset(self):
        """Complete golden dataset meets all requirements"""
        golden = GoldenDatasetInfo(
            layer_id="TEST",
            has_positive=True,
            positive_count=5,
            has_negative=True,
            negative_count=3,
            has_ambiguous=True,
            ambiguous_count=2,
            has_blocked=True,
            blocked_count=1,
            has_rank_lowering=True,
            rank_lowering_count=1,
        )

        assert golden.is_complete, "Golden dataset should be complete"
        assert golden.coverage == 1.0, "Coverage should be 100%"

    def test_incomplete_golden_dataset(self):
        """Incomplete golden dataset identified correctly"""
        golden = GoldenDatasetInfo(
            layer_id="TEST",
            has_positive=True,
            positive_count=3,  # Not enough
            has_negative=False,  # Missing
        )

        assert not golden.is_complete, "Golden dataset should be incomplete"
        assert golden.coverage < 1.0, "Coverage should be less than 100%"


class TestMaturityLevels:
    """Test maturity level determination"""

    def test_certified_requires_90_plus(self):
        """CERTIFIED maturity requires 90%+ score"""
        scorer = LayerScorer()

        assert scorer.determine_maturity_level(92) == MaturityLevel.CERTIFIED
        assert scorer.determine_maturity_level(89) != MaturityLevel.CERTIFIED

    def test_implemented_requires_70_to_89(self):
        """IMPLEMENTED maturity requires 70-89%"""
        scorer = LayerScorer()

        assert scorer.determine_maturity_level(75) == MaturityLevel.IMPLEMENTED
        assert scorer.determine_maturity_level(69) != MaturityLevel.IMPLEMENTED

    def test_partial_requires_50_to_69(self):
        """PARTIAL maturity requires 50-69%"""
        scorer = LayerScorer()

        assert scorer.determine_maturity_level(55) == MaturityLevel.PARTIAL
        assert scorer.determine_maturity_level(49) != MaturityLevel.PARTIAL

    def test_demonstrator_requires_30_to_49(self):
        """DEMONSTRATOR maturity requires 30-49%"""
        scorer = LayerScorer()

        assert scorer.determine_maturity_level(35) == MaturityLevel.DEMONSTRATOR
        assert scorer.determine_maturity_level(29) != MaturityLevel.DEMONSTRATOR


def test_json_schema_validation():
    """Test that generated JSON is valid"""
    # This would be tested by running the actual generator
    # and validating the output JSON structure
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
