"""
Constitutional Tests for Algorithm Trace Payload

PR #141: Tests enforcing constitutional laws for algorithm trace serialization.

Constitutional Laws Under Test:
    1. Payload is non-authoritative (audit evidence, not proof)
    2. Payload cannot create candidates
    3. Payload cannot upgrade rank
    4. Payload cannot delete residuals
    5. Payload cannot close ifadah
    6. Payload cannot produce hukm
    7. Payload cannot produce reality
    8. Required fields must be present and non-empty
    9. Forbidden operations must not exist as methods
    10. Consumer operations must be classified (permitted vs forbidden)

Test Categories:
    - test_required_fields_*: Validate required field presence
    - test_forbidden_methods_*: Verify forbidden methods don't exist
    - test_rank_preservation_*: Ensure rank cannot be upgraded
    - test_residual_preservation_*: Ensure residuals cannot be deleted
    - test_consumer_operation_*: Validate consumer operation classification
    - test_constitutional_invariants_*: Test constitutional guarantees

Created: 2026-05-28
"""

import pytest
from dal_core.algorithm_trace_payload import (
    AlgorithmTracePayload,
    CandidateTracePayload,
    RelationTracePayload,
    NetworkTracePayload,
    RankTracePayload,
    ResidualTracePayload,
    ForbiddenJumpPayload,
    AllowedNextLayerPayload,
    TraceConsumerOperation,
)
from dal_core.foundation import Rank, ResidualSet, create_residual_set
from dal_core.residuals import Residual, ResidualSeverity


# ============================================================================
# Test Required Fields
# ============================================================================

def test_algorithm_trace_payload_requires_schema_version():
    """Test that AlgorithmTracePayload requires schema_version."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )

    with pytest.raises(ValueError, match="requires non-empty schema_version"):
        AlgorithmTracePayload(
            schema_version="",  # Empty - should fail
            source_algorithm="RelationAlgebra",
            source_layer="relation_network",
            input_surface="زيد قائم",
            candidates=(candidate_payload,),
            network=None,
            allowed_next_layers=(),
            forbidden_jumps=()
        )


def test_algorithm_trace_payload_requires_source_algorithm():
    """Test that AlgorithmTracePayload requires source_algorithm."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )

    with pytest.raises(ValueError, match="requires non-empty source_algorithm"):
        AlgorithmTracePayload(
            schema_version="algorithm-trace-v1",
            source_algorithm="",  # Empty - should fail
            source_layer="relation_network",
            input_surface="زيد قائم",
            candidates=(candidate_payload,),
            network=None,
            allowed_next_layers=(),
            forbidden_jumps=()
        )


def test_algorithm_trace_payload_requires_candidates():
    """Test that AlgorithmTracePayload requires non-empty candidates."""
    with pytest.raises(ValueError, match="requires non-empty candidates"):
        AlgorithmTracePayload(
            schema_version="algorithm-trace-v1",
            source_algorithm="RelationAlgebra",
            source_layer="relation_network",
            input_surface="زيد قائم",
            candidates=(),  # Empty - should fail
            network=None,
            allowed_next_layers=(),
            forbidden_jumps=()
        )


def test_candidate_trace_payload_requires_candidate_id():
    """Test that CandidateTracePayload requires candidate_id."""
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

    with pytest.raises(ValueError, match="requires non-empty candidate_id"):
        CandidateTracePayload(
            candidate_id="",  # Empty - should fail
            candidate_type="RelationCandidate",
            layer="relation_network",
            trace=("step1",),
            rank_payload=rank_payload,
            residual_payload=residual_payload,
            forbidden_outputs=("hukm",)
        )


def test_candidate_trace_payload_requires_trace():
    """Test that CandidateTracePayload requires non-empty trace."""
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

    with pytest.raises(ValueError, match="requires non-empty trace"):
        CandidateTracePayload(
            candidate_id="cand1",
            candidate_type="RelationCandidate",
            layer="relation_network",
            trace=(),  # Empty - should fail
            rank_payload=rank_payload,
            residual_payload=residual_payload,
            forbidden_outputs=("hukm",)
        )


def test_relation_trace_payload_requires_anchor_id():
    """Test that RelationTracePayload requires anchor_id."""
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

    with pytest.raises(ValueError, match="requires non-empty anchor_id"):
        RelationTracePayload(
            relation_id="rel1",
            relation_type="predicative",
            anchor_id="",  # Empty - should fail
            related_id="قائم",
            trace=("step1",),
            rank_payload=rank_payload,
            residual_payload=residual_payload
        )


# ============================================================================
# Test Forbidden Methods Do Not Exist
# ============================================================================

def test_algorithm_trace_payload_has_no_to_hukm_method():
    """Test that AlgorithmTracePayload does not have to_hukm() method."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )
    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    assert not hasattr(payload, "to_hukm"), \
        "AlgorithmTracePayload MUST NOT have to_hukm() method"


def test_algorithm_trace_payload_has_no_to_reality_method():
    """Test that AlgorithmTracePayload does not have to_reality() method."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )
    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    assert not hasattr(payload, "to_reality"), \
        "AlgorithmTracePayload MUST NOT have to_reality() method"


def test_algorithm_trace_payload_has_no_close_ifadah_method():
    """Test that AlgorithmTracePayload does not have close_ifadah() method."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )
    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    assert not hasattr(payload, "close_ifadah"), \
        "AlgorithmTracePayload MUST NOT have close_ifadah() method"
    assert not hasattr(payload, "to_ifadah"), \
        "AlgorithmTracePayload MUST NOT have to_ifadah() method"


def test_algorithm_trace_payload_has_no_create_candidate_method():
    """Test that AlgorithmTracePayload does not have create_candidate() method."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )
    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    assert not hasattr(payload, "create_candidate"), \
        "AlgorithmTracePayload MUST NOT have create_candidate() method"


def test_algorithm_trace_payload_has_no_upgrade_rank_method():
    """Test that AlgorithmTracePayload does not have upgrade_rank() method."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )
    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    assert not hasattr(payload, "upgrade_rank"), \
        "AlgorithmTracePayload MUST NOT have upgrade_rank() method"


def test_algorithm_trace_payload_has_no_delete_residuals_method():
    """Test that AlgorithmTracePayload does not have delete_residuals() method."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )
    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    assert not hasattr(payload, "delete_residuals"), \
        "AlgorithmTracePayload MUST NOT have delete_residuals() method"


# ============================================================================
# Test Rank Preservation
# ============================================================================

def test_rank_trace_payload_preserves_rank_exactly():
    """Test that RankTracePayload preserves rank without modification."""
    original_rank = Rank.HYPOTHESIS
    rank_payload = RankTracePayload(
        rank=original_rank,
        rank_evidence=("evidence1", "evidence2"),
        rank_trace=("trace1", "trace2")
    )

    # Rank must be preserved exactly
    assert rank_payload.rank == original_rank
    assert rank_payload.rank is original_rank  # Same object


def test_rank_trace_payload_is_immutable():
    """Test that RankTracePayload is immutable (frozen dataclass)."""
    rank_payload = RankTracePayload(
        rank=Rank.HYPOTHESIS,
        rank_evidence=("evidence1",),
        rank_trace=("trace1",)
    )

    # Attempting to modify should fail (frozen=True)
    with pytest.raises(AttributeError):
        rank_payload.rank = Rank.CERTIFICATE  # type: ignore


# ============================================================================
# Test Residual Preservation
# ============================================================================

def test_residual_trace_payload_preserves_residuals_exactly():
    """Test that ResidualTracePayload preserves residuals without deletion."""
    from dal_core.residuals import ResidualType

    residual1 = Residual(
        type=ResidualType.MORPH_ANALYSIS_INCOMPLETE,
        severity=ResidualSeverity.WARNING,
        message="Unresolved agreement"
    )
    residual2 = Residual(
        type=ResidualType.MISSING_VISIBLE_HARAKA,
        severity=ResidualSeverity.BLOCKER,
        message="Missing evidence"
    )
    original_residuals = create_residual_set(frozenset([residual1, residual2]))

    residual_payload = ResidualTracePayload(
        residuals=original_residuals,
        residual_sources=("gate1", "gate2"),
        blocking_count=1
    )

    # Residuals must be preserved exactly
    assert residual_payload.residuals == original_residuals
    assert residual_payload.residuals is original_residuals  # Same object
    assert len(residual_payload.residuals.residuals) == 2


def test_residual_trace_payload_counts_blocking_correctly():
    """Test that ResidualTracePayload counts blocking residuals correctly."""
    from dal_core.residuals import ResidualType

    residual_blocker = Residual(
        type=ResidualType.COMPOSITION_BLOCKER,
        severity=ResidualSeverity.BLOCKER,
        message="Critical failure"
    )
    residual_warning = Residual(
        type=ResidualType.LOW_CONFIDENCE,
        severity=ResidualSeverity.WARNING,
        message="Minor issue"
    )
    residuals = create_residual_set(frozenset([residual_blocker, residual_warning]))

    residual_payload = ResidualTracePayload(
        residuals=residuals,
        residual_sources=("gate1",),
        blocking_count=1
    )

    assert residual_payload.blocking_count == 1


# ============================================================================
# Test Consumer Operation Classification
# ============================================================================

def test_consumer_operation_explain_trace_is_permitted():
    """Test that EXPLAIN_TRACE is a permitted operation."""
    op = TraceConsumerOperation.EXPLAIN_TRACE
    assert op.is_permitted()
    assert not op.is_forbidden()


def test_consumer_operation_summarize_candidates_is_permitted():
    """Test that SUMMARIZE_CANDIDATES is a permitted operation."""
    op = TraceConsumerOperation.SUMMARIZE_CANDIDATES
    assert op.is_permitted()
    assert not op.is_forbidden()


def test_consumer_operation_explain_existing_rank_is_permitted():
    """Test that EXPLAIN_EXISTING_RANK is permitted (not assign rank)."""
    op = TraceConsumerOperation.EXPLAIN_EXISTING_RANK
    assert op.is_permitted()
    assert not op.is_forbidden()


def test_consumer_operation_suggest_repair_is_permitted():
    """Test that SUGGEST_REPAIR is permitted (not execute repair)."""
    op = TraceConsumerOperation.SUGGEST_REPAIR
    assert op.is_permitted()
    assert not op.is_forbidden()


def test_consumer_operation_generate_bounded_explanation_is_permitted():
    """Test that GENERATE_BOUNDED_EXPLANATION is permitted."""
    op = TraceConsumerOperation.GENERATE_BOUNDED_EXPLANATION
    assert op.is_permitted()
    assert not op.is_forbidden()


def test_consumer_operation_produce_hukm_is_forbidden():
    """Test that PRODUCE_HUKM is forbidden."""
    op = TraceConsumerOperation.PRODUCE_HUKM
    assert op.is_forbidden()
    assert not op.is_permitted()


def test_consumer_operation_close_ifadah_is_forbidden():
    """Test that CLOSE_IFADAH is forbidden."""
    op = TraceConsumerOperation.CLOSE_IFADAH
    assert op.is_forbidden()
    assert not op.is_permitted()


def test_consumer_operation_create_reality_is_forbidden():
    """Test that CREATE_REALITY is forbidden."""
    op = TraceConsumerOperation.CREATE_REALITY
    assert op.is_forbidden()
    assert not op.is_permitted()


def test_consumer_operation_upgrade_rank_is_forbidden():
    """Test that UPGRADE_RANK is forbidden."""
    op = TraceConsumerOperation.UPGRADE_RANK
    assert op.is_forbidden()
    assert not op.is_permitted()


def test_consumer_operation_delete_residuals_is_forbidden():
    """Test that DELETE_RESIDUALS is forbidden."""
    op = TraceConsumerOperation.DELETE_RESIDUALS
    assert op.is_forbidden()
    assert not op.is_permitted()


def test_consumer_operation_create_candidate_is_forbidden():
    """Test that CREATE_CANDIDATE is forbidden."""
    op = TraceConsumerOperation.CREATE_CANDIDATE
    assert op.is_forbidden()
    assert not op.is_permitted()


# ============================================================================
# Test Constitutional Invariants
# ============================================================================

def test_algorithm_trace_payload_is_non_authoritative():
    """
    Test that AlgorithmTracePayload declares itself as non-authoritative.

    Constitutional Law:
        Payload is audit evidence, NOT proof authority.
    """
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )
    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    assert payload.is_non_authoritative is True


def test_algorithm_trace_payload_declares_forbidden_operations():
    """Test that AlgorithmTracePayload explicitly declares forbidden operations."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )
    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    forbidden_ops = payload.forbidden_operations
    assert "to_hukm" in forbidden_ops
    assert "to_reality" in forbidden_ops
    assert "close_ifadah" in forbidden_ops
    assert "create_candidate" in forbidden_ops
    assert "upgrade_rank" in forbidden_ops
    assert "delete_residuals" in forbidden_ops


def test_forbidden_jumps_are_preserved():
    """Test that forbidden jumps are preserved in payload."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )

    forbidden_jump1 = ForbiddenJumpPayload(
        from_layer="RelationCandidate",
        to_layer="Hukm",
        reason="Relations cannot produce hukm directly"
    )
    forbidden_jump2 = ForbiddenJumpPayload(
        from_layer="RelationCandidate",
        to_layer="Reality",
        reason="Relations cannot claim reality"
    )

    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=(forbidden_jump1, forbidden_jump2)
    )

    assert len(payload.forbidden_jumps) == 2
    assert forbidden_jump1 in payload.forbidden_jumps
    assert forbidden_jump2 in payload.forbidden_jumps


def test_allowed_next_layers_are_preserved():
    """Test that allowed next layers are preserved in payload."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality")
    )

    allowed_layer = AllowedNextLayerPayload(
        current_layer="RelationNetworkCandidate",
        next_layer="RelationClosureGate",
        conditions=("no_blocking_residuals", "sufficient_rank")
    )

    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(allowed_layer,),
        forbidden_jumps=()
    )

    assert len(payload.allowed_next_layers) == 1
    assert allowed_layer in payload.allowed_next_layers


# ============================================================================
# Test Complete Payload Construction
# ============================================================================

def test_complete_algorithm_trace_payload_construction():
    """
    Test complete construction of AlgorithmTracePayload with all components.

    This test validates the full payload structure that would be consumed
    by GovernedTraceT5 (future PR #142).
    """
    # Build rank payload
    rank_payload = RankTracePayload(
        rank=Rank.STRONG_HYPOTHESIS,
        rank_evidence=("wordform_evidence", "agreement_evidence"),
        rank_trace=("wordform_analysis", "relation_construction")
    )

    # Build residual payload (with no blocking residuals)
    residual_payload = ResidualTracePayload(
        residuals=create_residual_set(frozenset()),
        residual_sources=(),
        blocking_count=0
    )

    # Build relation trace
    relation_trace = RelationTracePayload(
        relation_id="rel_zayd_qaim",
        relation_type="predicative",
        anchor_id="زيد",
        related_id="قائم",
        trace=("wordform:زيد", "wordform:قائم", "edge:predication"),
        rank_payload=rank_payload,
        residual_payload=residual_payload
    )

    # Build network trace
    network_trace = NetworkTracePayload(
        network_id="network_zayd_qaim",
        relations=(relation_trace,),
        network_status="closable_candidate",
        closure_eligible=True,
        closure_residuals=residual_payload
    )

    # Build candidate trace
    candidate_trace = CandidateTracePayload(
        candidate_id="cand_predicative_zayd_qaim",
        candidate_type="PredicativeRelationCandidate",
        layer="relation_network",
        trace=("wordform_pair", "predication_analysis"),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm", "reality", "final_meaning")
    )

    # Build forbidden jumps
    forbidden_jump = ForbiddenJumpPayload(
        from_layer="RelationCandidate",
        to_layer="Hukm",
        reason="Relations are dal structures, not reality claims"
    )

    # Build allowed next layer
    allowed_next = AllowedNextLayerPayload(
        current_layer="RelationNetworkCandidate",
        next_layer="IfadahDalClosureGate",
        conditions=("closure_eligible", "no_blocking_residuals")
    )

    # Build complete payload
    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebraCore",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_trace,),
        network=network_trace,
        allowed_next_layers=(allowed_next,),
        forbidden_jumps=(forbidden_jump,)
    )

    # Validate payload structure
    assert payload.schema_version == "algorithm-trace-v1"
    assert payload.source_algorithm == "RelationAlgebraCore"
    assert payload.source_layer == "relation_network"
    assert payload.input_surface == "زيد قائم"
    assert len(payload.candidates) == 1
    assert payload.network is not None
    assert len(payload.allowed_next_layers) == 1
    assert len(payload.forbidden_jumps) == 1
    assert payload.is_non_authoritative is True


def test_algorithm_trace_payload_is_immutable():
    """Test that AlgorithmTracePayload is immutable (frozen dataclass)."""
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
        candidate_id="cand1",
        candidate_type="RelationCandidate",
        layer="relation_network",
        trace=("step1",),
        rank_payload=rank_payload,
        residual_payload=residual_payload,
        forbidden_outputs=("hukm",)
    )
    payload = AlgorithmTracePayload(
        schema_version="algorithm-trace-v1",
        source_algorithm="RelationAlgebra",
        source_layer="relation_network",
        input_surface="زيد قائم",
        candidates=(candidate_payload,),
        network=None,
        allowed_next_layers=(),
        forbidden_jumps=()
    )

    # Attempting to modify should fail (frozen=True)
    with pytest.raises(AttributeError):
        payload.schema_version = "v2"  # type: ignore
