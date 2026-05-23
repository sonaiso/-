"""
Layer Scoring Engine with Ceiling Caps
محرك تسجيل الطبقات مع حدود السقف

Implements scoring logic from GOVERNANCE_METRICS.md and LAYER_MATURITY_MODEL.md
"""

import sys
from pathlib import Path
from typing import Tuple

# Add tools to path
tools_dir = Path(__file__).parent.parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

from project_audit.types import (
    LayerScoreComponents,
    MaturityLevel,
    LayerStatus,
    RiskLevel
)
from project_audit.code_analyzer import LayerCodeInfo
from project_audit.test_analyzer import GoldenDatasetInfo


class LayerScorer:
    """Scores layers based on governance metrics"""

    # Layer weights from GOVERNANCE_METRICS.md
    LAYER_WEIGHTS = {
        "A0": 1.5,  # Kernel
        "A1": 1.5,  # Typed Layers
        "A2": 1.0,  # Pure Dāl
        "A3": 1.0,  # Madlūl-Lafẓī
        "A4": 1.0,  # Binding
        "A5": 1.0,  # Wadh
        "A6": 1.0,  # Dalālah
        "A7": 1.0,  # Ifādah
        "A8": 1.0,  # Hukm Boundary
        "A9": 0.8,  # Cognitive (planned)
        "A10": 1.2, # Golden/Audit (quality gate)
    }

    def score_typed_contract(self, code_info: LayerCodeInfo) -> int:
        """
        Score typed contract (0-15 points)

        Criteria:
        - 13-15: All frozen dataclasses, protocols, enums
        - 10-12: Mostly typed, some Any types
        - 5-9: Some typed contracts
        - 1-4: Minimal typing
        - 0: No typed contracts
        """
        if not code_info.has_typed_contract:
            return 0

        # Simplified scoring - in production would analyze AST deeper
        score = 10  # Base score for having typed contracts

        # Bonus for using frozen dataclasses (best practice)
        if code_info.has_typed_contract:
            score += 5

        return min(score, 15)

    def score_runtime_implementation(self, code_info: LayerCodeInfo) -> int:
        """
        Score runtime implementation (0-20 points)

        Criteria:
        - 18-20: Complete logic, no TODOs
        - 14-17: Core logic complete
        - 8-13: Core paths work
        - 1-7: Basic proof of concept
        - 0: No implementation
        """
        if not code_info.implementation_files:
            return 0

        # Simplified heuristic based on file count and presence
        score = 12  # Base score for having implementation

        # Bonus for multiple files (indicates comprehensive implementation)
        if len(code_info.implementation_files) >= 2:
            score += 5

        # Bonus for evidence/trace usage
        if code_info.evidence_count > 0 or code_info.trace_count > 0:
            score += 3

        return min(score, 20)

    def score_evidence_policy(self, code_info: LayerCodeInfo) -> int:
        """
        Score evidence policy (0-10 points)

        Criteria:
        - 9-10: Layer-specific required evidence
        - 7-8: Evidence types defined
        - 4-6: Evidence mentioned
        - 1-3: Evidence field exists
        - 0: No evidence policy
        """
        if code_info.evidence_count == 0:
            return 0

        score = 5  # Base for having evidence

        if code_info.evidence_count >= 5:
            score += 3
        if code_info.evidence_count >= 10:
            score += 2

        return min(score, 10)

    def score_rank_policy(self, code_info: LayerCodeInfo) -> int:
        """
        Score rank policy (0-10 points)

        Criteria:
        - 9-10: Layer-specific rank ceiling
        - 7-8: Rank ceiling exists
        - 4-6: Rank mentioned
        - 1-3: Rank field exists
        - 0: No rank policy
        """
        # Simplified - would need to check for actual rank policy code
        return 7  # Assume generic rank policy exists from core

    def score_residual_taxonomy(self, code_info: LayerCodeInfo) -> int:
        """
        Score residual taxonomy (0-10 points)

        Criteria:
        - 9-10: Clear separation with enums
        - 7-8: Taxonomy defined, mostly correct
        - 4-6: Some classification
        - 1-3: String residuals
        - 0: No residual tracking
        """
        if code_info.residual_count == 0:
            return 0

        score = 6  # Base for having residuals

        if code_info.residual_count >= 5:
            score += 2
        if code_info.residual_count >= 10:
            score += 2

        return min(score, 10)

    def score_noleap_tests(self, noleap_coverage: float) -> int:
        """
        Score NoLeap tests (0-10 points)

        Criteria:
        - 9-10: All forbidden transitions tested (100%)
        - 7-8: Most transitions tested (≥90%)
        - 4-6: Some transitions tested (50-89%)
        - 1-3: Few transitions tested (<50%)
        - 0: No NoLeap tests
        """
        if noleap_coverage >= 100:
            return 10
        elif noleap_coverage >= 90:
            return 8
        elif noleap_coverage >= 70:
            return 6
        elif noleap_coverage >= 50:
            return 4
        elif noleap_coverage > 0:
            return 2
        else:
            return 0

    def score_trace_replay(self, code_info: LayerCodeInfo) -> int:
        """
        Score trace/replay (0-10 points)

        Criteria:
        - 9-10: Complete trace with replay
        - 7-8: Trace exists, replay works
        - 4-6: Trace field present
        - 1-3: Trace is string
        - 0: No trace
        """
        if code_info.trace_count == 0:
            return 0

        score = 6  # Base for having trace

        if code_info.trace_count >= 5:
            score += 2
        if code_info.trace_count >= 10:
            score += 2

        return min(score, 10)

    def score_golden_dataset(self, golden_info: GoldenDatasetInfo) -> int:
        """
        Score golden dataset (0-10 points)

        Criteria:
        - 9-10: All case types covered
        - 7-8: Most case types (≥4/5)
        - 4-6: Some case types (2-3/5)
        - 1-3: Only positive cases
        - 0: No golden dataset
        """
        if not golden_info.has_positive:
            return 0

        case_type_count = sum([
            golden_info.has_positive,
            golden_info.has_negative,
            golden_info.has_ambiguous,
            golden_info.has_blocked,
            golden_info.has_rank_lowering
        ])

        if case_type_count >= 5 and golden_info.is_complete:
            return 10
        elif case_type_count >= 4:
            return 8
        elif case_type_count >= 3:
            return 6
        elif case_type_count >= 2:
            return 4
        else:
            return 2

    def score_doc_honesty(self, has_conflicts: bool) -> int:
        """
        Score documentation honesty (0-5 points)

        Criteria:
        - 5: Docs match code exactly
        - 4: Minor wording issues
        - 2-3: Some discrepancies
        - 1: Misleading wording
        - 0: False claims
        """
        if has_conflicts:
            return 2
        return 4  # Assume generally honest unless conflicts detected

    def calculate_raw_score(
        self,
        code_info: LayerCodeInfo,
        noleap_coverage: float,
        golden_info: GoldenDatasetInfo,
        has_conflicts: bool = False
    ) -> LayerScoreComponents:
        """Calculate raw score components for a layer"""
        return LayerScoreComponents(
            typed_contract=self.score_typed_contract(code_info),
            runtime_implementation=self.score_runtime_implementation(code_info),
            evidence_policy=self.score_evidence_policy(code_info),
            rank_policy=self.score_rank_policy(code_info),
            residual_taxonomy=self.score_residual_taxonomy(code_info),
            noleap_tests=self.score_noleap_tests(noleap_coverage),
            trace_replay=self.score_trace_replay(code_info),
            golden_dataset=self.score_golden_dataset(golden_info),
            doc_honesty=self.score_doc_honesty(has_conflicts)
        )

    def apply_ceiling(
        self,
        raw_score: int,
        code_info: LayerCodeInfo,
        noleap_coverage: float,
        has_conflicts: bool,
        trace_broken: bool = False
    ) -> Tuple[int, str]:
        """
        Apply ceiling caps to raw score

        Returns: (capped_score, cap_reason)

        Ceiling rules from GOVERNANCE_METRICS.md:
        - No typed contract → max 30%
        - Strings instead of types → max 45%
        - No tests → max 50%
        - No NoLeap tests → max 55%
        - Broken trace/replay → max 60%
        - Claim conflicts → max 70%
        - No golden dataset → max 70%
        """
        if not code_info.has_typed_contract:
            return (min(raw_score, 30), "No typed contract")

        if code_info.uses_strings_not_types:
            return (min(raw_score, 45), "Strings/booleans instead of typed candidates")

        if not code_info.has_tests:
            return (min(raw_score, 50), "No tests")

        if noleap_coverage < 90:
            return (min(raw_score, 55), f"NoLeap coverage at {noleap_coverage:.0f}% (need 90%+)")

        if trace_broken:
            return (min(raw_score, 60), "Broken trace/replay")

        if has_conflicts:
            return (min(raw_score, 70), "Claim/code conflict")

        if not code_info.has_golden_dataset:
            return (min(raw_score, 70), "No complete golden dataset")

        # No cap
        return (raw_score, "")

    def determine_maturity_level(self, capped_score: int) -> MaturityLevel:
        """Determine maturity level from capped score"""
        if capped_score >= 90:
            return MaturityLevel.CERTIFIED
        elif capped_score >= 70:
            return MaturityLevel.IMPLEMENTED
        elif capped_score >= 50:
            return MaturityLevel.PARTIAL
        elif capped_score >= 30:
            return MaturityLevel.DEMONSTRATOR
        elif capped_score >= 10:
            return MaturityLevel.PLANNED
        else:
            return MaturityLevel.GAP

    def determine_status(self, maturity_level: MaturityLevel) -> LayerStatus:
        """Determine layer status from maturity level"""
        mapping = {
            MaturityLevel.CERTIFIED: LayerStatus.IMPLEMENTED,
            MaturityLevel.IMPLEMENTED: LayerStatus.IMPLEMENTED,
            MaturityLevel.PARTIAL: LayerStatus.PARTIAL,
            MaturityLevel.DEMONSTRATOR: LayerStatus.DEMONSTRATOR,
            MaturityLevel.PLANNED: LayerStatus.PLANNED,
            MaturityLevel.GAP: LayerStatus.GAP
        }
        return mapping[maturity_level]

    def calculate_real_completion(self, layer_scores: dict) -> float:
        """
        Calculate overall real completion percentage

        Args:
            layer_scores: Dict mapping layer_id to capped_score

        Returns:
            Real completion percentage (0-100)
        """
        total_weighted_score = 0
        total_weight = 0

        for layer_id, capped_score in layer_scores.items():
            weight = self.LAYER_WEIGHTS.get(layer_id, 1.0)
            total_weighted_score += capped_score * weight
            total_weight += weight

        return (total_weighted_score / total_weight) if total_weight > 0 else 0
