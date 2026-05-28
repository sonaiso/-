"""
Golden Trace Explanation Fixtures (تثبيتات شرح الأثر الذهبية)

PR #144: Constitutional fixtures proving GovernedTraceT5Contract works on realistic traces.

Purpose:
    Demonstrate that GovernedTraceT5Contract enforces constitutional boundaries:
        1. T5 explains only what traces contain
        2. T5 cannot invent references
        3. T5 cannot analyze raw Arabic
        4. T5 cannot create/upgrade/resolve/close

Fixture Families:
    1. Valid explanation (references existing elements)
    2. Valid repair suggestion (requires rerun)
    3. Invalid invented candidate
    4. Invalid invented residual
    5. Invalid invented gate/operation
    6. Invalid rank claim
    7. Wrong trace (different trace_id)
    8. Raw Arabic bypass attempt
    9. Immutability preservation

Constitutional Law:
    T5 يستهلك الأثر المحدد، ولا ينشئ حقائق دستورية
    (T5 consumes specific traces; T5 does not create constitutional facts)

Created: 2026-05-28
"""

from dataclasses import dataclass
from typing import Tuple

from dal_core.algorithm_trace_payload import (
    AlgorithmTracePayload,
    CandidateTracePayload,
    RankTracePayload,
    ResidualTracePayload,
    TraceConsumerOperation,
)
from dal_core.governed_trace_t5_contract import (
    GovernedTraceT5Input,
    ExplanationCandidate,
    RepairSuggestionCandidate,
    TraceConsumerContext,
)
from dal_core.foundation import Rank, create_residual_set
from dal_core.residuals import Residual, ResidualSeverity, ResidualType


# ============================================================================
# Fixture Family 1: Valid Explanation (Golden Path)
# ============================================================================

@dataclass(frozen=True)
class ValidExplanationFixture:
    """
    Golden fixture: Valid explanation referencing only existing trace elements.

    Constitutional guarantee:
        All referenced IDs (candidates, residuals, gates, ranks) exist in trace.
    """
    trace: AlgorithmTracePayload
    t5_input: GovernedTraceT5Input
    explanation: ExplanationCandidate

    @property
    def trace_id(self) -> str:
        return self.trace.trace_id


def create_valid_explanation_fixture() -> ValidExplanationFixture:
    """
    Create golden fixture with valid explanation.

    Scenario:
        Algorithm produces trace with:
        - 2 candidates (relation_cand_1, relation_cand_2)
        - HYPOTHESIS rank
        - 2 residuals (agreement_residual, case_residual)
        - 3 gates (IsnadGate, AgreementGate, CaseGate)

        T5 explains trace referencing only existing elements.

    Returns:
        ValidExplanationFixture with all valid references
    """
    # Create residuals (str(residual) will be used as ID)
    residual_1 = Residual(
        type=ResidualType.MORPH_ANALYSIS_INCOMPLETE,
        severity=ResidualSeverity.WARNING,
        message="Number agreement required",
        location="AgreementGate"
    )
    residual_2 = Residual(
        type=ResidualType.SURFACE_EFFECT_UNRESOLVED,
        severity=ResidualSeverity.WARNING,
        message="Case marker ambiguous",
        location="CaseGate"
    )

    # Create rank payload
    rank_payload = RankTracePayload(
        rank=Rank.HYPOTHESIS,
        rank_evidence=("morphological_pattern", "syntactic_structure"),
        rank_trace=("IsnadGate", "AgreementGate", "CaseGate")
    )

    # Create residual payloads
    residual_payload_1 = ResidualTracePayload(
        residuals=create_residual_set(frozenset([residual_1, residual_2])),
        residual_sources=("AgreementGate", "CaseGate"),
        blocking_count=0
    )

    residual_payload_2 = ResidualTracePayload(
        residuals=create_residual_set(frozenset([residual_2])),
        residual_sources=("CaseGate",),
        blocking_count=0
    )

    # Create candidate payloads
    candidate_1 = CandidateTracePayload(
        candidate_id="relation_cand_1",
        candidate_type="PredicativeRelationCandidate",
        layer="relation_network",
        trace=("IsnadGate", "AgreementGate", "CaseGate"),
        rank_payload=rank_payload,
        residual_payload=residual_payload_1,
        forbidden_outputs=("to_hukm", "to_reality", "close_ifadah")
    )

    candidate_2 = CandidateTracePayload(
        candidate_id="relation_cand_2",
        candidate_type="InclusionRelationCandidate",
        layer="relation_network",
        trace=("IsnadGate", "CaseGate"),
        rank_payload=rank_payload,
        residual_payload=residual_payload_2,
        forbidden_outputs=("to_hukm", "to_reality", "close_ifadah")
    )

    # Create algorithm trace payload
    trace = AlgorithmTracePayload(
        trace_id="trace_golden_001",
        schema_version="algorithm-trace-v1",
        source_algorithm="IsnadRelationAlgorithm",
        source_layer="relation_network",
        input_surface="زَيْدٌ قَائِمٌ",
        candidates=(candidate_1, candidate_2),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    # Create T5 input
    t5_input = GovernedTraceT5Input(
        trace=trace,
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        context=TraceConsumerContext(
            user_query="Explain how this predicative relation was constructed",
            explanation_scope="relations and residuals",
            max_referenced_elements=10
        )
    )

    # Create valid explanation (references only existing elements)
    # Note: referenced_residual_ids must match str(residual) from trace
    explanation = ExplanationCandidate(
        source_trace_id="trace_golden_001",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text=(
            "تم بناء علاقة إسنادية بين المبتدأ والخبر. "
            "المرشح الأول relation_cand_1 يمثل العلاقة الرئيسية "
            "مع بقايا تتعلق بالموافقة العددية والإعراب. "
            "الرتبة الحالية هي HYPOTHESIS نظرًا للبقايا المتبقية."
        ),
        referenced_candidate_ids=("relation_cand_1", "relation_cand_2"),
        referenced_rank_values=("HYPOTHESIS",),
        referenced_residual_ids=(
            "[WARNING] تحليل صرفي غير مكتمل at AgreementGate: Number agreement required",
            "[WARNING] أثر سطحي غير محسوم at CaseGate: Case marker ambiguous"
        ),
        referenced_gate_ids=("IsnadGate", "AgreementGate", "CaseGate"),
        confidence=0.85
    )

    return ValidExplanationFixture(
        trace=trace,
        t5_input=t5_input,
        explanation=explanation
    )


# ============================================================================
# Fixture Family 2: Valid Repair Suggestion
# ============================================================================

@dataclass(frozen=True)
class ValidRepairSuggestionFixture:
    """
    Golden fixture: Valid repair suggestion requiring algorithm rerun.

    Constitutional guarantee:
        - Binds to trace.trace_id
        - References existing blocking residuals
        - Requires algorithm rerun
        - Does NOT resolve residuals
        - Does NOT create repaired candidate
    """
    trace: AlgorithmTracePayload
    t5_input: GovernedTraceT5Input
    repair_suggestion: RepairSuggestionCandidate


def create_valid_repair_suggestion_fixture() -> ValidRepairSuggestionFixture:
    """
    Create golden fixture with valid repair suggestion.

    Scenario:
        Algorithm produces trace with blocking residuals.
        T5 suggests repair requiring algorithm rerun.
        T5 does NOT execute repair.
        T5 does NOT resolve residuals.

    Returns:
        ValidRepairSuggestionFixture
    """
    # Create blocking residual
    blocking_residual = Residual(
        type=ResidualType.MORPH_ANALYSIS_INCOMPLETE,
        severity=ResidualSeverity.BLOCKER,
        message="Subject-predicate agreement required for certification",
        location="AgreementGate"
    )

    # Create rank payload (cannot exceed HYPOTHESIS with blocker)
    rank_payload = RankTracePayload(
        rank=Rank.HYPOTHESIS,
        rank_evidence=("partial_structure",),
        rank_trace=("IsnadGate",)
    )

    # Create residual payload with blocker
    residual_payload = ResidualTracePayload(
        residuals=create_residual_set(frozenset([blocking_residual])),
        residual_sources=("AgreementGate",),
        blocking_count=1
    )

    # Create candidate payload
    candidate = CandidateTracePayload(
        candidate_id="blocked_candidate_1",
        candidate_type="PredicativeRelationCandidate",
        layer="relation_network",
        trace=("IsnadGate",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("to_hukm", "to_reality", "close_ifadah")
    )

    # Create algorithm trace payload
    trace = AlgorithmTracePayload(
        trace_id="trace_golden_002",
        schema_version="algorithm-trace-v1",
        source_algorithm="IsnadRelationAlgorithm",
        source_layer="relation_network",
        input_surface="الطلاب قائم",  # Intentional agreement error
        candidates=(candidate,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    # Create T5 input
    t5_input = GovernedTraceT5Input(
        trace=trace,
        operation=TraceConsumerOperation.SUGGEST_REPAIR,
        context=None
    )

    # Create repair suggestion (MUST require algorithm rerun)
    # Note: blocked_by_residual_ids must match str(blocking_residual)
    repair_suggestion = RepairSuggestionCandidate(
        source_trace_id="trace_golden_002",
        blocked_by_residual_ids=(
            "[BLOCKER] تحليل صرفي غير مكتمل at AgreementGate: Subject-predicate agreement required for certification",
        ),
        suggested_gate="AgreementGate",
        suggested_rerun=True,
        explanation=(
            "هناك عدم توافق في العدد بين المبتدأ والخبر. "
            "يُقترح إعادة تشغيل AgreementGate مع التحقق من العدد. "
            "هذا الإصلاح يتطلب إعادة تشغيل الخوارزمية بالكامل."
        ),
        requires_algorithm_rerun=True  # CONSTITUTIONAL REQUIREMENT
    )

    return ValidRepairSuggestionFixture(
        trace=trace,
        t5_input=t5_input,
        repair_suggestion=repair_suggestion
    )


# ============================================================================
# Fixture Family 3: Invalid Invented Candidate
# ============================================================================

@dataclass(frozen=True)
class InvalidInventedCandidateFixture:
    """
    Negative fixture: Explanation inventing candidate_id not in trace.

    Constitutional violation:
        ExplanationCandidate references candidate_id that does NOT exist in trace.

    Expected behavior:
        GovernedTraceT5Validator.validate_explanation_references() MUST reject.
    """
    trace: AlgorithmTracePayload
    invalid_explanation: ExplanationCandidate


def create_invalid_invented_candidate_fixture() -> InvalidInventedCandidateFixture:
    """
    Create negative fixture with invented candidate_id.

    Scenario:
        Trace contains candidate_id="real_cand_1".
        T5 explanation references candidate_id="invented_cand_999" (NOT in trace).
        Validation must reject.

    Returns:
        InvalidInventedCandidateFixture
    """
    # Create minimal trace
    rank_payload = RankTracePayload(
        rank=Rank.HYPOTHESIS,
        rank_evidence=("evidence",),
        rank_trace=("gate",)
    )
    residual_payload = ResidualTracePayload(
        residuals=create_residual_set(frozenset()),
        residual_sources=(),
        blocking_count=0
    )
    candidate = CandidateTracePayload(
        candidate_id="real_cand_1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("IsnadGate",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=()
    )
    trace = AlgorithmTracePayload(
        trace_id="trace_golden_003",
        schema_version="algorithm-trace-v1",
        source_algorithm="TestAlgorithm",
        source_layer="test_layer",
        input_surface="test",
        candidates=(candidate,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    # Create explanation with INVENTED candidate_id
    invalid_explanation = ExplanationCandidate(
        source_trace_id="trace_golden_003",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="T5 invented a candidate",
        referenced_candidate_ids=("invented_cand_999",),  # NOT IN TRACE
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.9
    )

    return InvalidInventedCandidateFixture(
        trace=trace,
        invalid_explanation=invalid_explanation
    )


# ============================================================================
# Fixture Family 4: Invalid Invented Residual
# ============================================================================

@dataclass(frozen=True)
class InvalidInventedResidualFixture:
    """
    Negative fixture: Explanation inventing residual_id not in trace.

    Constitutional violation:
        ExplanationCandidate references residual_id that does NOT exist in trace.
    """
    trace: AlgorithmTracePayload
    invalid_explanation: ExplanationCandidate


def create_invalid_invented_residual_fixture() -> InvalidInventedResidualFixture:
    """
    Create negative fixture with invented residual_id.

    Returns:
        InvalidInventedResidualFixture
    """
    # Create trace with specific residual
    real_residual = Residual(
        type=ResidualType.TYPE_UNRESOLVED,
        severity=ResidualSeverity.WARNING,
        message="Real residual message",
        location="RealGate"
    )
    rank_payload = RankTracePayload(
        rank=Rank.HYPOTHESIS,
        rank_evidence=("evidence",),
        rank_trace=("gate",)
    )
    residual_payload = ResidualTracePayload(
        residuals=create_residual_set(frozenset([real_residual])),
        residual_sources=("RealGate",),
        blocking_count=0
    )
    candidate = CandidateTracePayload(
        candidate_id="cand_1",
        candidate_type="RelationCandidate",
        layer="test_layer",
        trace=("RealGate",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=()
    )
    trace = AlgorithmTracePayload(
        trace_id="trace_golden_004",
        schema_version="algorithm-trace-v1",
        source_algorithm="TestAlgorithm",
        source_layer="test_layer",
        input_surface="test",
        candidates=(candidate,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    # Create explanation with INVENTED residual_id (does not match str(any residual))
    invalid_explanation = ExplanationCandidate(
        source_trace_id="trace_golden_004",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="T5 invented a residual",
        referenced_candidate_ids=(),
        referenced_rank_values=(),
        referenced_residual_ids=("[FAKE] Invented residual ID",),  # NOT IN TRACE
        referenced_gate_ids=(),
        confidence=0.9
    )

    return InvalidInventedResidualFixture(
        trace=trace,
        invalid_explanation=invalid_explanation
    )


# ============================================================================
# Fixture Family 5: Invalid Invented Gate/Operation
# ============================================================================

@dataclass(frozen=True)
class InvalidInventedGateFixture:
    """
    Negative fixture: Explanation inventing gate_id not in trace.

    Constitutional violation:
        ExplanationCandidate references gate_id that does NOT exist in trace.
    """
    trace: AlgorithmTracePayload
    invalid_explanation: ExplanationCandidate


def create_invalid_invented_gate_fixture() -> InvalidInventedGateFixture:
    """
    Create negative fixture with invented gate_id.

    Returns:
        InvalidInventedGateFixture
    """
    # Create trace with specific gates
    rank_payload = RankTracePayload(
        rank=Rank.HYPOTHESIS,
        rank_evidence=("evidence",),
        rank_trace=("RealGate1", "RealGate2")
    )
    residual_payload = ResidualTracePayload(
        residuals=create_residual_set(frozenset()),
        residual_sources=("RealGate1",),
        blocking_count=0
    )
    candidate = CandidateTracePayload(
        candidate_id="cand_1",
        candidate_type="RelationCandidate",
        layer="test_layer",
        trace=("RealGate1", "RealGate2"),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=()
    )
    trace = AlgorithmTracePayload(
        trace_id="trace_golden_005",
        schema_version="algorithm-trace-v1",
        source_algorithm="TestAlgorithm",
        source_layer="test_layer",
        input_surface="test",
        candidates=(candidate,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    # Create explanation with INVENTED gate_id
    invalid_explanation = ExplanationCandidate(
        source_trace_id="trace_golden_005",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="T5 invented a gate",
        referenced_candidate_ids=(),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=("InventedGate999",),  # NOT IN TRACE
        confidence=0.9
    )

    return InvalidInventedGateFixture(
        trace=trace,
        invalid_explanation=invalid_explanation
    )


# ============================================================================
# Fixture Family 6: Invalid Rank Claim
# ============================================================================

@dataclass(frozen=True)
class InvalidRankClaimFixture:
    """
    Negative fixture: Explanation claiming rank not in trace.

    Constitutional violation:
        ExplanationCandidate references rank value NOT present in trace.
    """
    trace: AlgorithmTracePayload
    invalid_explanation: ExplanationCandidate


def create_invalid_rank_claim_fixture() -> InvalidRankClaimFixture:
    """
    Create negative fixture with invalid rank claim.

    Scenario:
        Trace has HYPOTHESIS rank.
        T5 claims CERTIFICATE rank (NOT in trace).
        Validation must reject.

    Returns:
        InvalidRankClaimFixture
    """
    # Create trace with HYPOTHESIS rank
    rank_payload = RankTracePayload(
        rank=Rank.HYPOTHESIS,  # ONLY THIS RANK IN TRACE
        rank_evidence=("evidence",),
        rank_trace=("gate",)
    )
    residual_payload = ResidualTracePayload(
        residuals=create_residual_set(frozenset()),
        residual_sources=(),
        blocking_count=0
    )
    candidate = CandidateTracePayload(
        candidate_id="cand_1",
        candidate_type="RelationCandidate",
        layer="test_layer",
        trace=("gate",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=()
    )
    trace = AlgorithmTracePayload(
        trace_id="trace_golden_006",
        schema_version="algorithm-trace-v1",
        source_algorithm="TestAlgorithm",
        source_layer="test_layer",
        input_surface="test",
        candidates=(candidate,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    # Create explanation claiming CERTIFICATE rank (NOT in trace)
    invalid_explanation = ExplanationCandidate(
        source_trace_id="trace_golden_006",
        operation=TraceConsumerOperation.EXPLAIN_EXISTING_RANK,
        explanation_text="T5 claimed higher rank",
        referenced_candidate_ids=(),
        referenced_rank_values=("CERTIFICATE",),  # NOT IN TRACE
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.9
    )

    return InvalidRankClaimFixture(
        trace=trace,
        invalid_explanation=invalid_explanation
    )


# ============================================================================
# Fixture Family 7: Wrong Trace (Different trace_id)
# ============================================================================

@dataclass(frozen=True)
class WrongTraceFixture:
    """
    Negative fixture: Explanation bound to wrong trace_id.

    Constitutional principle:
        Explanations bind to SPECIFIC trace execution (trace_id),
        NOT to algorithm name (source_algorithm).

    Scenario:
        Two traces from SAME algorithm but DIFFERENT trace_id.
        Explanation for trace A must NOT validate against trace B.
    """
    trace_a: AlgorithmTracePayload
    trace_b: AlgorithmTracePayload
    explanation_for_a: ExplanationCandidate


def create_wrong_trace_fixture() -> WrongTraceFixture:
    """
    Create negative fixture with wrong trace_id binding.

    Returns:
        WrongTraceFixture
    """
    # Create trace A
    rank_payload_a = RankTracePayload(
        rank=Rank.HYPOTHESIS,
        rank_evidence=("evidence_a",),
        rank_trace=("gate_a",)
    )
    residual_payload_a = ResidualTracePayload(
        residuals=create_residual_set(frozenset()),
        residual_sources=(),
        blocking_count=0
    )
    candidate_a = CandidateTracePayload(
        candidate_id="cand_from_trace_a",
        candidate_type="RelationCandidate",
        layer="test_layer",
        trace=("gate_a",),
        rank_payload=rank_payload_a,
        residual_payload=residual_payload_a,
        forbidden_outputs=()
    )
    trace_a = AlgorithmTracePayload(
        trace_id="trace_golden_007a",  # TRACE A
        schema_version="algorithm-trace-v1",
        source_algorithm="SameAlgorithm",  # SAME ALGORITHM
        source_layer="test_layer",
        input_surface="input A",
        candidates=(candidate_a,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    # Create trace B (DIFFERENT trace_id, SAME algorithm)
    rank_payload_b = RankTracePayload(
        rank=Rank.HYPOTHESIS,
        rank_evidence=("evidence_b",),
        rank_trace=("gate_b",)
    )
    residual_payload_b = ResidualTracePayload(
        residuals=create_residual_set(frozenset()),
        residual_sources=(),
        blocking_count=0
    )
    candidate_b = CandidateTracePayload(
        candidate_id="cand_from_trace_b",
        candidate_type="RelationCandidate",
        layer="test_layer",
        trace=("gate_b",),
        rank_payload=rank_payload_b,
        residual_payload=residual_payload_b,
        forbidden_outputs=()
    )
    trace_b = AlgorithmTracePayload(
        trace_id="trace_golden_007b",  # TRACE B (DIFFERENT)
        schema_version="algorithm-trace-v1",
        source_algorithm="SameAlgorithm",  # SAME ALGORITHM
        source_layer="test_layer",
        input_surface="input B",
        candidates=(candidate_b,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    # Create explanation bound to trace A
    explanation_for_a = ExplanationCandidate(
        source_trace_id="trace_golden_007a",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Explanation for trace A",
        referenced_candidate_ids=("cand_from_trace_a",),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.9
    )

    return WrongTraceFixture(
        trace_a=trace_a,
        trace_b=trace_b,
        explanation_for_a=explanation_for_a
    )


# ============================================================================
# Fixture Family 8: Raw Arabic Bypass Attempt
# ============================================================================

@dataclass(frozen=True)
class RawArabicBypassFixture:
    """
    Negative fixture: Attempt to bypass with raw Arabic text.

    Constitutional violation:
        T5 may NOT analyze raw Arabic text.
        T5 may ONLY consume AlgorithmTracePayload.

    Expected behavior:
        GovernedTraceT5Input constructor MUST reject raw string.
    """
    raw_arabic_text: str


def create_raw_arabic_bypass_fixture() -> RawArabicBypassFixture:
    """
    Create negative fixture attempting raw Arabic bypass.

    Returns:
        RawArabicBypassFixture
    """
    return RawArabicBypassFixture(
        raw_arabic_text="زَيْدٌ قَائِمٌ وَعَمْرٌو قَاعِدٌ"
    )


# ============================================================================
# Fixture Family 9: Immutability Preservation
# ============================================================================

@dataclass(frozen=True)
class ImmutabilityFixture:
    """
    Positive fixture: Trace consumption preserves immutability.

    Constitutional guarantee:
        Consuming AlgorithmTracePayload for explanation MUST NOT mutate original.

    Test:
        Create trace → Create input → Create explanation → Verify trace unchanged.
    """
    original_trace: AlgorithmTracePayload
    t5_input: GovernedTraceT5Input
    explanation: ExplanationCandidate


def create_immutability_fixture() -> ImmutabilityFixture:
    """
    Create fixture demonstrating immutability preservation.

    Returns:
        ImmutabilityFixture
    """
    # Create trace
    rank_payload = RankTracePayload(
        rank=Rank.HYPOTHESIS,
        rank_evidence=("evidence",),
        rank_trace=("gate",)
    )
    residual_payload = ResidualTracePayload(
        residuals=create_residual_set(frozenset()),
        residual_sources=(),
        blocking_count=0
    )
    candidate = CandidateTracePayload(
        candidate_id="immutable_cand_1",
        candidate_type="RelationCandidate",
        layer="test_layer",
        trace=("gate",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=()
    )
    original_trace = AlgorithmTracePayload(
        trace_id="trace_golden_009",
        schema_version="algorithm-trace-v1",
        source_algorithm="TestAlgorithm",
        source_layer="test_layer",
        input_surface="immutable test",
        candidates=(candidate,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    # Create T5 input
    t5_input = GovernedTraceT5Input(
        trace=original_trace,
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        context=None
    )

    # Create explanation
    explanation = ExplanationCandidate(
        source_trace_id="trace_golden_009",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Immutability test",
        referenced_candidate_ids=("immutable_cand_1",),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.9
    )

    return ImmutabilityFixture(
        original_trace=original_trace,
        t5_input=t5_input,
        explanation=explanation
    )


# ============================================================================
# Fixture Registry
# ============================================================================

def create_all_golden_fixtures() -> dict:
    """
    Create all golden trace explanation fixtures.

    Returns:
        Dictionary mapping fixture names to fixture objects
    """
    return {
        "valid_explanation": create_valid_explanation_fixture(),
        "valid_repair_suggestion": create_valid_repair_suggestion_fixture(),
        "invalid_invented_candidate": create_invalid_invented_candidate_fixture(),
        "invalid_invented_residual": create_invalid_invented_residual_fixture(),
        "invalid_invented_gate": create_invalid_invented_gate_fixture(),
        "invalid_rank_claim": create_invalid_rank_claim_fixture(),
        "wrong_trace": create_wrong_trace_fixture(),
        "raw_arabic_bypass": create_raw_arabic_bypass_fixture(),
        "immutability": create_immutability_fixture(),
    }
