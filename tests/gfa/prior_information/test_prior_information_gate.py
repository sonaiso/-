"""
Tests for Prior Information Gate

Critical Laws Tested:
1. Prior information requires domain + source_trace + (evidence OR testability)
2. Prior opinion is blocked
3. Missing domain → BLOCKED
4. Missing source → BLOCKED
5. Missing evidence AND testability → rank lowered
6. Admitted information carries rank + residuals + trace
"""

import pytest
from gfa.prior_information import (
    PriorInformationGate,
    PriorContentType,
    OpinionType,
    make_prior_missing_domain_residual,
    make_prior_missing_source_residual,
    make_prior_opinion_contamination_residual,
)


class TestPriorInformationGateCore:
    """Test core gate functionality."""

    def test_gate_instantiation(self):
        """Gate can be instantiated."""
        gate = PriorInformationGate()
        assert gate is not None

    def test_admit_complete_prior_information(self):
        """Admit prior information with all requirements."""
        gate = PriorInformationGate()

        result = gate.admit_prior_information(
            content="الفاعل مرفوع",
            domain="grammar",
            content_type=PriorContentType.RULE,
            source_trace="arabic_grammar_tradition",
            evidence="grammatical_attestation",
            testability="syntactic_test",
        )

        assert result.is_admitted()
        assert result.candidate is not None
        assert result.candidate.domain == "grammar"
        assert result.candidate.content_type == PriorContentType.RULE
        assert result.rank == "LICENSED"  # Both evidence and testability
        assert result.failure is None

    def test_admit_with_evidence_only(self):
        """Admit with evidence but no testability."""
        gate = PriorInformationGate()

        result = gate.admit_prior_information(
            content="الماء سائل",
            domain="physical",
            content_type=PriorContentType.DEFINITION,
            source_trace="empirical_observation",
            evidence="sensory_evidence",
        )

        assert result.is_admitted()
        assert result.rank == "CANDIDATE"  # Evidence but no testability

    def test_admit_with_testability_only(self):
        """Admit with testability but no evidence."""
        gate = PriorInformationGate()

        result = gate.admit_prior_information(
            content="hypothesis X",
            domain="empirical",
            content_type=PriorContentType.RULE,
            source_trace="scientific_method",
            testability="empirical_test",
        )

        assert result.is_admitted()
        assert result.rank == "CANDIDATE"  # Testability but no evidence


class TestPriorInformationGateBlockers:
    """Test blocker conditions."""

    def test_block_missing_domain(self):
        """Block prior information without domain."""
        gate = PriorInformationGate()

        result = gate.admit_prior_information(
            content="some rule",
            domain=None,  # Missing
            content_type=PriorContentType.RULE,
            source_trace="source",
            evidence="evidence",
        )

        assert result.is_blocked()
        assert result.candidate is None
        assert result.rank == "BLOCKED"
        assert result.failure is not None
        assert "MISSING_DOMAIN" in result.failure.kind.name
        assert len(result.residuals) > 0

    def test_block_missing_source_trace(self):
        """Block prior information without source trace."""
        gate = PriorInformationGate()

        result = gate.admit_prior_information(
            content="some rule",
            domain="domain_x",
            content_type=PriorContentType.RULE,
            source_trace=None,  # Missing
            evidence="evidence",
        )

        assert result.is_blocked()
        assert result.candidate is None
        assert result.rank == "BLOCKED"
        assert result.failure is not None
        assert "MISSING_SOURCE" in result.failure.kind.name

    def test_block_prior_opinion(self):
        """Block prior opinion from entering as information."""
        gate = PriorInformationGate()

        result = gate.filter_prior_opinion(
            content="رأيي أن المجتمع كذا",
            opinion_type=OpinionType.PRIOR_JUDGMENT,
        )

        assert result.is_blocked()
        assert result.candidate is None
        assert result.rank == "BLOCKED"
        assert result.failure is not None
        assert "OPINION_CONTAMINATION" in result.failure.kind.name
        assert len(result.residuals) > 0


class TestPriorInformationGateResiduals:
    """Test residual generation."""

    def test_residuals_for_missing_evidence_and_testability(self):
        """Generate residuals when both evidence and testability missing."""
        gate = PriorInformationGate()

        result = gate.admit_prior_information(
            content="rule without support",
            domain="domain_x",
            content_type=PriorContentType.RULE,
            source_trace="source",
            evidence=None,
            testability=None,
        )

        # Still admitted but with residuals
        assert result.is_admitted()
        assert result.rank == "CANDIDATE"
        assert len(result.residuals) > 0
        # Should have missing evidence residual
        assert any("MISSING_EVIDENCE" in str(r) for r in result.residuals)

    def test_trace_preservation(self):
        """Trace is preserved in admitted candidate."""
        gate = PriorInformationGate()

        result = gate.admit_prior_information(
            content="rule",
            domain="domain",
            source_trace="source",
            evidence="evidence",
        )

        assert result.is_admitted()
        assert result.trace is not None
        assert result.candidate.trace_id is not None


class TestPriorInformationGateNoLeap:
    """Test NoLeap guards - forbidden transitions."""

    def test_noleap_opinion_to_information(self):
        """Prior opinion CANNOT become prior information."""
        gate = PriorInformationGate()

        # Attempt to admit opinion as information
        result = gate.filter_prior_opinion(
            content="my impression is X",
            opinion_type=OpinionType.IMPRESSION,
        )

        assert result.is_blocked()
        assert "OPINION_CONTAMINATION" in result.failure.kind.name

    def test_noleap_unverified_interpretation(self):
        """Unverified interpretation is opinion, not information."""
        gate = PriorInformationGate()

        result = gate.filter_prior_opinion(
            content="I think this means Y",
            opinion_type=OpinionType.UNVERIFIED_INTERPRETATION,
        )

        assert result.is_blocked()

    def test_noleap_bias_as_information(self):
        """Bias cannot enter as prior information."""
        gate = PriorInformationGate()

        result = gate.filter_prior_opinion(
            content="systematic bias X",
            opinion_type=OpinionType.BIAS,
        )

        assert result.is_blocked()

    def test_noleap_taste_as_information(self):
        """Aesthetic taste cannot be prior information."""
        gate = PriorInformationGate()

        result = gate.filter_prior_opinion(
            content="I prefer style X",
            opinion_type=OpinionType.TASTE,
        )

        assert result.is_blocked()


class TestPriorInformationGateGoldenCases:
    """Test against golden dataset cases."""

    def test_golden_grammar_rule(self):
        """Grammar rule from source → ADMITTED."""
        gate = PriorInformationGate()

        result = gate.admit_prior_information(
            content="الفاعل مرفوع",
            domain="grammar",
            content_type=PriorContentType.RULE,
            source_trace="arabic_grammar_tradition",
            evidence="grammatical_attestation",
            testability="syntactic_test",
        )

        assert result.is_admitted()
        assert result.rank in ["LICENSED", "CERTIFIED"]

    def test_golden_personal_interpretation_filtered(self):
        """Personal interpretation → FILTERED (opinion)."""
        gate = PriorInformationGate()

        result = gate.filter_prior_opinion(
            content="personal interpretation",
            opinion_type=OpinionType.UNVERIFIED_INTERPRETATION,
        )

        assert result.is_blocked()

    def test_golden_undocumented_practice_filtered(self):
        """Undocumented practice → FILTERED (habit)."""
        gate = PriorInformationGate()

        result = gate.filter_prior_opinion(
            content="undocumented practice",
            opinion_type=OpinionType.HABIT,
        )

        assert result.is_blocked()

    def test_golden_definition_from_lexicon(self):
        """Definition from lexicon → ADMITTED."""
        gate = PriorInformationGate()

        result = gate.admit_prior_information(
            content="الماء: سائل عديم اللون",
            domain="lexical",
            content_type=PriorContentType.DEFINITION,
            source_trace="arabic_lexicon",
            evidence="lexicon_entry",
        )

        assert result.is_admitted()

    def test_golden_bias_filtered(self):
        """Bias → FILTERED."""
        gate = PriorInformationGate()

        result = gate.filter_prior_opinion(
            content="systematic bias",
            opinion_type=OpinionType.BIAS,
        )

        assert result.is_blocked()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
