"""
Constitutional Tests for Governed Trace T5 Contract

PR #142: Tests enforcing constitutional laws for T5 trace consumption.

Constitutional Laws Under Test:
    1. T5 may only consume AlgorithmTracePayload (not raw Arabic)
    2. T5 may only perform permitted operations
    3. ExplanationCandidate cannot create candidates
    4. ExplanationCandidate cannot modify rank
    5. ExplanationCandidate cannot close ifadah
    6. ExplanationCandidate cannot produce hukm/reality
    7. RepairSuggestionCandidate cannot execute repairs
    8. RepairSuggestionCandidate cannot resolve residuals
    9. RepairSuggestionCandidate must require algorithm rerun
    10. Explanation references must belong to source trace
    11. All contract dataclasses are frozen/immutable

Test Categories:
    - test_input_*: Input validation tests
    - test_explanation_*: ExplanationCandidate tests
    - test_repair_*: RepairSuggestionCandidate tests
    - test_validator_*: Validator enforcement tests
    - test_forbidden_*: Forbidden operation tests
    - test_immutability_*: Immutability tests

Created: 2026-05-28
"""

import pytest
from dal_core.governed_trace_t5_contract import (
    GovernedTraceT5Input,
    ExplanationCandidate,
    RepairSuggestionCandidate,
    TraceConsumerContext,
    ForbiddenT5Operation,
    GovernedTraceT5Validator,
)
from dal_core.algorithm_trace_payload import (
    AlgorithmTracePayload,
    CandidateTracePayload,
    RankTracePayload,
    ResidualTracePayload,
    TraceConsumerOperation,
)
from dal_core.foundation import Rank, create_residual_set


# ============================================================================
# Test Helpers
# ============================================================================

def create_test_trace_payload() -> AlgorithmTracePayload:
    """Create a test AlgorithmTracePayload for testing."""
    rank_payload = RankTracePayload(
        rank=Rank.HYPOTHESIS,
        rank_evidence=("evidence1",),
        rank_trace=("trace1",)
    )
    residual_payload = ResidualTracePayload(
        residuals=create_residual_set(frozenset()),
        residual_sources=(),
        blocking_count=0
    )
    candidate_payload = CandidateTracePayload(
        candidate_id="test_cand_1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )
    return AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="TestAlgorithm",
        source_layer="test_layer",
        input_surface="test input",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )


# ============================================================================
# Test Input Validation
# ============================================================================

def test_input_requires_algorithm_trace_payload():
    """Test that GovernedTraceT5Input requires AlgorithmTracePayload."""
    trace = create_test_trace_payload()
    operation = TraceConsumerOperation.EXPLAIN_TRACE

    # Valid input with AlgorithmTracePayload
    valid_input = GovernedTraceT5Input(
        trace=trace,
        operation=operation,
        context=None
    )
    assert valid_input.trace == trace


def test_input_rejects_raw_arabic_string():
    """
    Test that GovernedTraceT5Input rejects raw Arabic string.

    Constitutional Law:
        T5 may NOT analyze raw Arabic text.
        T5 may ONLY consume AlgorithmTracePayload.
    """
    operation = TraceConsumerOperation.EXPLAIN_TRACE

    # Attempt to create input with raw string (should fail)
    with pytest.raises(TypeError, match="must be AlgorithmTracePayload"):
        GovernedTraceT5Input(
            trace="زيد قائم",  # type: ignore - intentional type error
            operation=operation,
            context=None
        )


def test_input_requires_permitted_operation():
    """Test that GovernedTraceT5Input requires permitted operation."""
    trace = create_test_trace_payload()

    # Valid permitted operation
    valid_input = GovernedTraceT5Input(
        trace=trace,
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        context=None
    )
    assert valid_input.operation.is_permitted()


def test_input_rejects_forbidden_operation():
    """Test that GovernedTraceT5Input rejects forbidden operations."""
    trace = create_test_trace_payload()

    # Forbidden operation: PRODUCE_HUKM
    with pytest.raises(ValueError, match="must be permitted"):
        GovernedTraceT5Input(
            trace=trace,
            operation=TraceConsumerOperation.PRODUCE_HUKM,
            context=None
        )


def test_input_context_rejects_forbidden_instructions():
    """Test that TraceConsumerContext rejects forbidden instructions."""
    # Attempt to create context with forbidden instruction
    with pytest.raises(ValueError, match="contains forbidden instruction"):
        TraceConsumerContext(
            user_query="Please create a new candidate for this word",
            explanation_scope=None,
            max_referenced_elements=None
        )


def test_input_context_allows_valid_queries():
    """Test that TraceConsumerContext allows valid user queries."""
    # Valid context with permitted query
    context = TraceConsumerContext(
        user_query="Explain why this relation was constructed",
        explanation_scope="relations only",
        max_referenced_elements=10
    )
    assert context.user_query == "Explain why this relation was constructed"


# ============================================================================
# Test ExplanationCandidate
# ============================================================================

def test_explanation_candidate_basic_construction():
    """Test basic construction of ExplanationCandidate."""
    explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="This relation connects زيد and قائم",
        referenced_candidate_ids=("test_cand_1",),
        referenced_rank_values=("HYPOTHESIS",),
        referenced_residual_ids=(),
        referenced_gate_ids=("PredicationGate",),
        confidence=0.85
    )
    assert explanation.source_trace_id == "test_trace_1"
    assert explanation.confidence == 0.85


def test_explanation_candidate_requires_source_trace_id():
    """Test that ExplanationCandidate requires source_trace_id."""
    with pytest.raises(ValueError, match="requires non-empty source_trace_id"):
        ExplanationCandidate(
            source_trace_id="",  # Empty - should fail
            operation=TraceConsumerOperation.EXPLAIN_TRACE,
            explanation_text="Some explanation",
            referenced_candidate_ids=(),
            referenced_rank_values=(),
            referenced_residual_ids=(),
            referenced_gate_ids=(),
            confidence=0.5
        )


def test_explanation_candidate_requires_permitted_operation():
    """Test that ExplanationCandidate requires permitted operation."""
    with pytest.raises(ValueError, match="must be permitted"):
        ExplanationCandidate(
            source_trace_id="test_trace_1",
            operation=TraceConsumerOperation.PRODUCE_HUKM,  # Forbidden
            explanation_text="Some explanation",
            referenced_candidate_ids=(),
            referenced_rank_values=(),
            referenced_residual_ids=(),
            referenced_gate_ids=(),
            confidence=0.5
        )


def test_explanation_candidate_validates_confidence_bounds():
    """Test that ExplanationCandidate validates confidence in [0.0, 1.0]."""
    # Confidence too high
    with pytest.raises(ValueError, match="confidence must be in"):
        ExplanationCandidate(
            source_trace_id="test_trace_1",
            operation=TraceConsumerOperation.EXPLAIN_TRACE,
            explanation_text="Some explanation",
            referenced_candidate_ids=(),
            referenced_rank_values=(),
            referenced_residual_ids=(),
            referenced_gate_ids=(),
            confidence=1.5  # > 1.0 - should fail
        )

    # Confidence too low
    with pytest.raises(ValueError, match="confidence must be in"):
        ExplanationCandidate(
            source_trace_id="test_trace_1",
            operation=TraceConsumerOperation.EXPLAIN_TRACE,
            explanation_text="Some explanation",
            referenced_candidate_ids=(),
            referenced_rank_values=(),
            referenced_residual_ids=(),
            referenced_gate_ids=(),
            confidence=-0.1  # < 0.0 - should fail
        )


def test_explanation_candidate_has_no_create_candidate_field():
    """
    Test that ExplanationCandidate has no create_candidate field.

    Constitutional Law:
        ExplanationCandidate MUST NOT have fields for creating candidates.
    """
    explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Some explanation",
        referenced_candidate_ids=(),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.5
    )

    assert not hasattr(explanation, "new_candidate")
    assert not hasattr(explanation, "create_candidate")
    assert not hasattr(explanation, "created_candidate")


def test_explanation_candidate_has_no_upgrade_rank_field():
    """
    Test that ExplanationCandidate has no upgrade_rank field.

    Constitutional Law:
        ExplanationCandidate MUST NOT have fields for upgrading rank.
    """
    explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Some explanation",
        referenced_candidate_ids=(),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.5
    )

    assert not hasattr(explanation, "upgraded_rank")
    assert not hasattr(explanation, "upgrade_rank")
    assert not hasattr(explanation, "new_rank")


def test_explanation_candidate_has_no_close_ifadah_field():
    """
    Test that ExplanationCandidate has no close_ifadah field.

    Constitutional Law:
        ExplanationCandidate MUST NOT have fields for closing ifadah.
    """
    explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Some explanation",
        referenced_candidate_ids=(),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.5
    )

    assert not hasattr(explanation, "closed_ifadah")
    assert not hasattr(explanation, "close_ifadah")
    assert not hasattr(explanation, "to_ifadah")


def test_explanation_candidate_has_no_produce_hukm_field():
    """
    Test that ExplanationCandidate has no produce_hukm field.

    Constitutional Law:
        ExplanationCandidate MUST NOT have fields for producing hukm.
    """
    explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Some explanation",
        referenced_candidate_ids=(),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.5
    )

    assert not hasattr(explanation, "produced_hukm")
    assert not hasattr(explanation, "produce_hukm")
    assert not hasattr(explanation, "to_hukm")


def test_explanation_candidate_has_no_produce_reality_field():
    """
    Test that ExplanationCandidate has no produce_reality field.

    Constitutional Law:
        ExplanationCandidate MUST NOT have fields for producing reality.
    """
    explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Some explanation",
        referenced_candidate_ids=(),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.5
    )

    assert not hasattr(explanation, "produced_reality")
    assert not hasattr(explanation, "produce_reality")
    assert not hasattr(explanation, "to_reality")


# ============================================================================
# Test RepairSuggestionCandidate
# ============================================================================

def test_repair_suggestion_basic_construction():
    """Test basic construction of RepairSuggestionCandidate."""
    suggestion = RepairSuggestionCandidate(
        source_trace_id="test_trace_1",
        blocked_by_residual_ids=("residual_1",),
        suggested_gate="AgreementGate",
        suggested_rerun=True,
        explanation="Rerun AgreementGate to resolve agreement residual",
        requires_algorithm_rerun=True
    )
    assert suggestion.source_trace_id == "test_trace_1"
    assert suggestion.requires_algorithm_rerun is True


def test_repair_suggestion_requires_algorithm_rerun():
    """
    Test that RepairSuggestionCandidate MUST require algorithm rerun.

    Constitutional Law:
        T5 cannot execute repairs.
        T5 can only suggest repairs that require algorithm rerun.
    """
    with pytest.raises(ValueError, match="MUST be True"):
        RepairSuggestionCandidate(
            source_trace_id="test_trace_1",
            blocked_by_residual_ids=("residual_1",),
            suggested_gate="SomeGate",
            suggested_rerun=True,
            explanation="Some explanation",
            requires_algorithm_rerun=False  # False - FORBIDDEN
        )


def test_repair_suggestion_has_no_executed_repair_field():
    """
    Test that RepairSuggestionCandidate has no executed_repair field.

    Constitutional Law:
        RepairSuggestionCandidate MUST NOT have fields for executed repairs.
    """
    suggestion = RepairSuggestionCandidate(
        source_trace_id="test_trace_1",
        blocked_by_residual_ids=("residual_1",),
        suggested_gate="SomeGate",
        suggested_rerun=True,
        explanation="Some explanation",
        requires_algorithm_rerun=True
    )

    assert not hasattr(suggestion, "executed_repair")
    assert not hasattr(suggestion, "execute_repair")


def test_repair_suggestion_has_no_resolved_residuals_field():
    """
    Test that RepairSuggestionCandidate has no resolved_residuals field.

    Constitutional Law:
        RepairSuggestionCandidate MUST NOT have fields for resolved residuals.
    """
    suggestion = RepairSuggestionCandidate(
        source_trace_id="test_trace_1",
        blocked_by_residual_ids=("residual_1",),
        suggested_gate="SomeGate",
        suggested_rerun=True,
        explanation="Some explanation",
        requires_algorithm_rerun=True
    )

    assert not hasattr(suggestion, "resolved_residuals")
    assert not hasattr(suggestion, "resolve_residuals")
    assert not hasattr(suggestion, "delete_residuals")


def test_repair_suggestion_has_no_new_candidate_field():
    """
    Test that RepairSuggestionCandidate has no new_candidate field.

    Constitutional Law:
        RepairSuggestionCandidate MUST NOT have fields for creating candidates.
    """
    suggestion = RepairSuggestionCandidate(
        source_trace_id="test_trace_1",
        blocked_by_residual_ids=("residual_1",),
        suggested_gate="SomeGate",
        suggested_rerun=True,
        explanation="Some explanation",
        requires_algorithm_rerun=True
    )

    assert not hasattr(suggestion, "new_candidate")
    assert not hasattr(suggestion, "create_candidate")


# ============================================================================
# Test Validator Enforcement
# ============================================================================

def test_validator_validates_input():
    """Test that validator validates GovernedTraceT5Input."""
    trace = create_test_trace_payload()
    valid_input = GovernedTraceT5Input(
        trace=trace,
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        context=None
    )

    # Should not raise
    GovernedTraceT5Validator.validate_input(valid_input)


def test_validator_rejects_raw_arabic_input():
    """Test that validator rejects raw Arabic input."""
    # Validator should reject non-AlgorithmTracePayload
    # (This is already enforced by __post_init__, but validator adds extra layer)
    trace = create_test_trace_payload()
    valid_input = GovernedTraceT5Input(
        trace=trace,
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        context=None
    )

    # Replace trace with string (violates type contract)
    # We can't actually do this with frozen dataclass, so we test via constructor
    with pytest.raises(TypeError):
        GovernedTraceT5Input(
            trace="raw arabic",  # type: ignore
            operation=TraceConsumerOperation.EXPLAIN_TRACE,
            context=None
        )


def test_validator_validates_explanation():
    """Test that validator validates ExplanationCandidate."""
    explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Some explanation",
        referenced_candidate_ids=(),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.5
    )

    # Should not raise
    GovernedTraceT5Validator.validate_explanation(explanation)


def test_validator_validates_repair_suggestion():
    """Test that validator validates RepairSuggestionCandidate."""
    suggestion = RepairSuggestionCandidate(
        source_trace_id="test_trace_1",
        blocked_by_residual_ids=("residual_1",),
        suggested_gate="SomeGate",
        suggested_rerun=True,
        explanation="Some explanation",
        requires_algorithm_rerun=True
    )

    # Should not raise
    GovernedTraceT5Validator.validate_repair_suggestion(suggestion)


def test_validator_validates_output_union():
    """Test that validator validates GovernedTraceT5Output union."""
    explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Some explanation",
        referenced_candidate_ids=(),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.5
    )

    # Should not raise
    GovernedTraceT5Validator.validate_output(explanation)


def test_validator_validates_explanation_references():
    """Test that validator validates explanation references belong to trace."""
    trace = create_test_trace_payload()

    # Valid explanation referencing existing candidate
    valid_explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Some explanation",
        referenced_candidate_ids=("test_cand_1",),  # Exists in trace
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.5
    )

    # Should not raise
    GovernedTraceT5Validator.validate_explanation_references(
        valid_explanation, trace
    )


def test_validator_rejects_invalid_explanation_references():
    """Test that validator rejects explanation references not in trace."""
    trace = create_test_trace_payload()

    # Invalid explanation referencing non-existent candidate
    invalid_explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Some explanation",
        referenced_candidate_ids=("nonexistent_cand",),  # Does not exist
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.5
    )

    with pytest.raises(ValueError, match="not found in source trace"):
        GovernedTraceT5Validator.validate_explanation_references(
            invalid_explanation, trace
        )


# ============================================================================
# Test Forbidden Operations Enum
# ============================================================================

def test_forbidden_operations_declared():
    """Test that all forbidden operations are declared."""
    forbidden_ops = [
        ForbiddenT5Operation.CREATE_CANDIDATE,
        ForbiddenT5Operation.UPGRADE_RANK,
        ForbiddenT5Operation.DELETE_RESIDUALS,
        ForbiddenT5Operation.CLOSE_IFADAH,
        ForbiddenT5Operation.PRODUCE_HUKM,
        ForbiddenT5Operation.PRODUCE_REALITY,
        ForbiddenT5Operation.ANALYZE_RAW_ARABIC,
        ForbiddenT5Operation.MODIFY_TRACE,
        ForbiddenT5Operation.EXECUTE_REPAIR,
        ForbiddenT5Operation.RESOLVE_RESIDUALS,
        ForbiddenT5Operation.PRODUCE_SEMANTIC_CERTAINTY,
    ]

    assert len(forbidden_ops) == 11


# ============================================================================
# Test Immutability (Frozen Dataclasses)
# ============================================================================

def test_governed_trace_t5_input_is_immutable():
    """Test that GovernedTraceT5Input is immutable (frozen=True)."""
    trace = create_test_trace_payload()
    input_obj = GovernedTraceT5Input(
        trace=trace,
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        context=None
    )

    with pytest.raises(AttributeError):
        input_obj.operation = TraceConsumerOperation.SUMMARIZE_CANDIDATES  # type: ignore


def test_explanation_candidate_is_immutable():
    """Test that ExplanationCandidate is immutable (frozen=True)."""
    explanation = ExplanationCandidate(
        source_trace_id="test_trace_1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        explanation_text="Some explanation",
        referenced_candidate_ids=(),
        referenced_rank_values=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.5
    )

    with pytest.raises(AttributeError):
        explanation.confidence = 0.9  # type: ignore


def test_repair_suggestion_candidate_is_immutable():
    """Test that RepairSuggestionCandidate is immutable (frozen=True)."""
    suggestion = RepairSuggestionCandidate(
        source_trace_id="test_trace_1",
        blocked_by_residual_ids=("residual_1",),
        suggested_gate="SomeGate",
        suggested_rerun=True,
        explanation="Some explanation",
        requires_algorithm_rerun=True
    )

    with pytest.raises(AttributeError):
        suggestion.suggested_gate = "DifferentGate"  # type: ignore


def test_trace_consumer_context_is_immutable():
    """Test that TraceConsumerContext is immutable (frozen=True)."""
    context = TraceConsumerContext(
        user_query="Some query",
        explanation_scope="relations",
        max_referenced_elements=10
    )

    with pytest.raises(AttributeError):
        context.max_referenced_elements = 20  # type: ignore


# ============================================================================
# Test Complete T5 Contract Flow
# ============================================================================

def test_complete_t5_contract_flow_explanation():
    """
    Test complete T5 contract flow: Input → Explanation.

    This test validates the full contract flow:
        AlgorithmTracePayload
        → GovernedTraceT5Input
        → ExplanationCandidate
    """
    # Step 1: Create algorithm trace
    trace = create_test_trace_payload()

    # Step 2: Create T5 input
    t5_input = GovernedTraceT5Input(
        trace=trace,
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        context=TraceConsumerContext(
            user_query="Explain this relation",
            explanation_scope=None,
            max_referenced_elements=None
        )
    )

    # Step 3: Validate input
    GovernedTraceT5Validator.validate_input(t5_input)

    # Step 4: Create explanation output
    explanation = ExplanationCandidate(
        source_trace_id=trace.source_algorithm,
        operation=t5_input.operation,
        explanation_text="This trace shows a predicative relation",
        referenced_candidate_ids=("test_cand_1",),
        referenced_rank_values=("HYPOTHESIS",),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        confidence=0.8
    )

    # Step 5: Validate output
    GovernedTraceT5Validator.validate_output(explanation)
    GovernedTraceT5Validator.validate_explanation_references(explanation, trace)

    # Verify constitutional boundaries
    assert not hasattr(explanation, "new_candidate")
    assert not hasattr(explanation, "upgraded_rank")
    assert not hasattr(explanation, "closed_ifadah")


def test_complete_t5_contract_flow_repair_suggestion():
    """
    Test complete T5 contract flow: Input → Repair Suggestion.

    This test validates the full contract flow:
        AlgorithmTracePayload
        → GovernedTraceT5Input
        → RepairSuggestionCandidate
    """
    # Step 1: Create algorithm trace
    trace = create_test_trace_payload()

    # Step 2: Create T5 input
    t5_input = GovernedTraceT5Input(
        trace=trace,
        operation=TraceConsumerOperation.SUGGEST_REPAIR,
        context=None
    )

    # Step 3: Validate input
    GovernedTraceT5Validator.validate_input(t5_input)

    # Step 4: Create repair suggestion output
    suggestion = RepairSuggestionCandidate(
        source_trace_id=trace.source_algorithm,
        blocked_by_residual_ids=("residual_agreement",),
        suggested_gate="AgreementGate",
        suggested_rerun=True,
        explanation="Rerun AgreementGate with additional evidence",
        requires_algorithm_rerun=True
    )

    # Step 5: Validate output
    GovernedTraceT5Validator.validate_output(suggestion)

    # Verify constitutional boundaries
    assert suggestion.requires_algorithm_rerun is True
    assert not hasattr(suggestion, "executed_repair")
    assert not hasattr(suggestion, "resolved_residuals")
