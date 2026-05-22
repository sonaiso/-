"""
AttentionGeometry Kernel Tests

Comprehensive test suite enforcing all AttentionGeometry laws.
"""

import pytest
from uuid import uuid4
from datetime import datetime

from gfa.attention import (
    AttentionEvent,
    AttentionType,
    AttentionGate,
    GateStatus,
    AttentionPolicy,
    PolicyType,
    SelectionCriterion,
    AttendedTrace,
    AttentionPriority,
    AttentionResidual,
    ResidualType,
    IgnoredTrace,
    PartiallyAttendedTrace,
)


# ============================================================================
# Test 1: No attention without CognitiveCarrier
# ============================================================================


def test_attention_requires_cognitive_carrier():
    """Attention requires carrier_id (no attention without carrier)"""
    trace_ids = {uuid4(), uuid4(), uuid4()}

    # Should raise error without carrier_id
    with pytest.raises(ValueError, match="requires carrier_id"):
        AttentionEvent(
            carrier_id=None,  # Missing carrier
            input_trace_ids=trace_ids,
            selected_trace_ids=trace_ids,
            ignored_trace_ids=set(),
        )


# ============================================================================
# Test 2: Attention requires attention_capacity
# ============================================================================


def test_attention_requires_attention_capacity():
    """Attention capacity must be in valid range [0, 1]"""
    carrier_id = uuid4()
    trace_ids = {uuid4()}

    # Invalid capacity values
    with pytest.raises(ValueError, match="capacity must be in"):
        AttentionEvent(
            carrier_id=carrier_id,
            input_trace_ids=trace_ids,
            selected_trace_ids=trace_ids,
            ignored_trace_ids=set(),
            attention_capacity_used=-0.1,  # Invalid
        )

    with pytest.raises(ValueError, match="capacity must be in"):
        AttentionEvent(
            carrier_id=carrier_id,
            input_trace_ids=trace_ids,
            selected_trace_ids=trace_ids,
            ignored_trace_ids=set(),
            attention_capacity_used=1.5,  # Invalid
        )

    # Valid capacity
    event = AttentionEvent(
        carrier_id=carrier_id,
        input_trace_ids=trace_ids,
        selected_trace_ids=trace_ids,
        ignored_trace_ids=set(),
        attention_capacity_used=0.5,  # Valid
    )
    assert event.attention_capacity_used == 0.5


# ============================================================================
# Test 3: Attention selects trace without raising rank
# ============================================================================


def test_attention_selects_trace_without_raising_rank():
    """Attention changes selection, not epistemic rank"""
    original_trace_id = uuid4()
    event_id = uuid4()

    attended = AttendedTrace(
        original_trace_id=original_trace_id,
        attention_event_id=event_id,
        priority=AttentionPriority.HIGH,
        original_rank="CANDIDATE",
    )

    # Verify rank not raised
    assert not attended.is_higher_rank_than_original()
    assert attended.original_rank == "CANDIDATE"


# ============================================================================
# Test 4: Attention does not certify trace
# ============================================================================


def test_attention_does_not_certify_trace():
    """Attention CANNOT certify traces"""
    carrier_id = uuid4()
    trace_ids = {uuid4()}

    event = AttentionEvent(
        carrier_id=carrier_id,
        input_trace_ids=trace_ids,
        selected_trace_ids=trace_ids,
        ignored_trace_ids=set(),
    )

    assert not event.can_certify()

    # AttendedTrace also cannot certify
    attended = AttendedTrace(
        original_trace_id=list(trace_ids)[0],
        attention_event_id=event.event_id,
    )
    assert not attended.can_certify()

    # Gate cannot certify
    gate = AttentionGate(gate_id="test_gate", criterion=lambda x: True)
    assert not gate.can_certify()


# ============================================================================
# Test 5: Attention priority is not epistemic rank
# ============================================================================


def test_attention_priority_is_not_epistemic_rank():
    """Processing priority ≠ epistemic rank"""
    trace_id = uuid4()
    event_id = uuid4()

    # High priority trace
    high_priority = AttendedTrace(
        original_trace_id=trace_id,
        attention_event_id=event_id,
        priority=AttentionPriority.CRITICAL,
        original_rank="CANDIDATE",
    )

    # Low priority trace
    low_priority = AttendedTrace(
        original_trace_id=uuid4(),
        attention_event_id=event_id,
        priority=AttentionPriority.BACKGROUND,
        original_rank="CANDIDATE",
    )

    # Both have same rank despite different priorities
    assert high_priority.original_rank == low_priority.original_rank
    assert high_priority.priority != low_priority.priority

    # Priority is orthogonal to rank
    assert high_priority.priority_is_not_rank()
    assert low_priority.priority_is_not_rank()


# ============================================================================
# Test 6: Ignored trace becomes residual
# ============================================================================


def test_ignored_trace_becomes_residual():
    """Ignored traces are preserved as residuals, not deleted"""
    trace_id = uuid4()
    event_id = uuid4()

    ignored = IgnoredTrace(
        original_trace_id=trace_id,
        attention_event_id=event_id,
        residual_type=ResidualType.BELOW_THRESHOLD,
        reason="Did not meet salience threshold",
    )

    # Verify preservation laws
    assert ignored.is_preserved()
    assert not ignored.is_deleted()
    assert not ignored.is_lost()
    assert ignored.can_be_recovered()


# ============================================================================
# Test 7: Attention preserves original trace ID
# ============================================================================


def test_attention_preserves_original_trace_id():
    """Attention maintains trace lineage"""
    original_id = uuid4()
    event_id = uuid4()

    attended = AttendedTrace(
        original_trace_id=original_id,
        attention_event_id=event_id,
    )

    assert attended.preserves_original_trace_id()
    assert attended.original_trace_id == original_id


# ============================================================================
# Test 8: Attention does not store memory
# ============================================================================


def test_attention_does_not_store_memory():
    """Attention does NOT create memory storage"""
    carrier_id = uuid4()
    trace_ids = {uuid4()}

    event = AttentionEvent(
        carrier_id=carrier_id,
        input_trace_ids=trace_ids,
        selected_trace_ids=trace_ids,
        ignored_trace_ids=set(),
    )

    assert not event.can_create_memory()


# ============================================================================
# Test 9: Attention does not recall memory
# ============================================================================


def test_attention_does_not_recall_memory():
    """Attention is not memory retrieval"""
    # AttentionEvent has no memory recall methods
    carrier_id = uuid4()
    trace_ids = {uuid4()}

    event = AttentionEvent(
        carrier_id=carrier_id,
        input_trace_ids=trace_ids,
        selected_trace_ids=trace_ids,
        ignored_trace_ids=set(),
    )

    # Verify no memory operations
    assert not hasattr(event, "recall_memory")
    assert not hasattr(event, "retrieve_from_memory")
    assert not hasattr(event, "access_memory_store")


# ============================================================================
# Test 10: Attention does not compare traces
# ============================================================================


def test_attention_does_not_compare_traces():
    """Attention does NOT perform trace comparison"""
    carrier_id = uuid4()
    trace_ids = {uuid4(), uuid4()}

    event = AttentionEvent(
        carrier_id=carrier_id,
        input_trace_ids=trace_ids,
        selected_trace_ids=trace_ids,
        ignored_trace_ids=set(),
    )

    assert not event.can_compare_traces()


# ============================================================================
# Test 11: Attention does not bind
# ============================================================================


def test_attention_does_not_bind():
    """Attention does NOT bind traces"""
    carrier_id = uuid4()
    trace_ids = {uuid4(), uuid4()}

    event = AttentionEvent(
        carrier_id=carrier_id,
        input_trace_ids=trace_ids,
        selected_trace_ids=trace_ids,
        ignored_trace_ids=set(),
    )

    assert not event.can_bind()


# ============================================================================
# Test 12: Attention does not learn
# ============================================================================


def test_attention_does_not_learn():
    """Attention does NOT learn patterns"""
    carrier_id = uuid4()
    trace_ids = {uuid4()}

    event = AttentionEvent(
        carrier_id=carrier_id,
        input_trace_ids=trace_ids,
        selected_trace_ids=trace_ids,
        ignored_trace_ids=set(),
    )

    assert not event.can_learn()


# ============================================================================
# Test 13: Attention does not create CPB
# ============================================================================


def test_attention_does_not_create_cpb():
    """Attention does NOT create compositional binding policies"""
    # AttentionEvent has no CPB generation methods
    carrier_id = uuid4()
    trace_ids = {uuid4()}

    event = AttentionEvent(
        carrier_id=carrier_id,
        input_trace_ids=trace_ids,
        selected_trace_ids=trace_ids,
        ignored_trace_ids=set(),
    )

    # Verify no CPB operations
    assert not hasattr(event, "create_cpb")
    assert not hasattr(event, "extract_binding_policy")
    assert not hasattr(event, "generate_compositional_policy")


# ============================================================================
# Test 14: Attention event serializes without losing trace lineage
# ============================================================================


def test_attention_serializes_without_losing_trace_lineage():
    """Attention event preserves all trace IDs"""
    carrier_id = uuid4()
    input_ids = {uuid4(), uuid4(), uuid4()}
    selected_ids = {list(input_ids)[0], list(input_ids)[1]}
    ignored_ids = {list(input_ids)[2]}

    event = AttentionEvent(
        carrier_id=carrier_id,
        input_trace_ids=input_ids,
        selected_trace_ids=selected_ids,
        ignored_trace_ids=ignored_ids,
    )

    # Verify all IDs preserved
    assert event.carrier_id == carrier_id
    assert event.input_trace_ids == input_ids
    assert event.selected_trace_ids == selected_ids
    assert event.ignored_trace_ids == ignored_ids

    # Verify lineage
    assert event.selected_trace_ids | event.ignored_trace_ids == event.input_trace_ids


# ============================================================================
# Integration Tests
# ============================================================================


def test_attention_gate_applies_criterion():
    """Attention gate filters based on criterion"""

    def salience_criterion(trace):
        return trace.get("salience", 0.0) > 0.5

    gate = AttentionGate(
        gate_id="salience_gate", criterion=salience_criterion, priority_weight=0.8
    )

    # High salience trace
    high_trace = {"salience": 0.7, "id": "trace1"}
    assert gate.apply(high_trace) == GateStatus.PASS

    # Low salience trace
    low_trace = {"salience": 0.3, "id": "trace2"}
    assert gate.apply(low_trace) == GateStatus.BLOCK


def test_attention_policy_enforces_capacity_limits():
    """Attention policy respects capacity constraints"""
    policy = AttentionPolicy(
        policy_id="limited_policy",
        policy_type=PolicyType.RESOURCE_LIMITED,
        max_selection_ratio=0.5,  # Max 50% selection
        capacity_budget=0.6,
    )

    trace_count = 10

    # Should allow max 5 traces (50% of 10)
    assert policy.max_allowed_selection(trace_count) == 5

    # Cannot select all if ratio < 1.0
    assert not policy.can_select_all(trace_count)


def test_partial_attention_tracks_residuals():
    """Partially attended traces preserve ignored aspects"""
    trace_id = uuid4()
    event_id = uuid4()

    partial = PartiallyAttendedTrace(
        original_trace_id=trace_id,
        attention_event_id=event_id,
        attended_aspects={"color", "shape"},
        ignored_aspects={"texture", "weight"},
        reason="Limited capacity",
    )

    # Verify completeness
    assert partial.completeness_ratio() == 0.5  # 2 attended / 4 total
    assert partial.ignored_ratio() == 0.5


def test_attention_residual_preserves_all_ignored():
    """Attention residual tracks all ignored traces"""
    event_id = uuid4()

    ignored1 = IgnoredTrace(
        original_trace_id=uuid4(),
        attention_event_id=event_id,
        residual_type=ResidualType.CAPACITY_LIMITED,
    )

    ignored2 = IgnoredTrace(
        original_trace_id=uuid4(),
        attention_event_id=event_id,
        residual_type=ResidualType.BELOW_THRESHOLD,
    )

    residual = AttentionResidual(
        event_id=event_id, ignored_traces=[ignored1, ignored2], total_ignored_count=2
    )

    assert not residual.is_empty()
    assert residual.can_recover_all()
    assert len(residual.get_recoverable_trace_ids()) == 2


def test_selected_and_ignored_must_equal_input():
    """Attention event enforces accounting: selected + ignored = input"""
    carrier_id = uuid4()
    input_ids = {uuid4(), uuid4(), uuid4()}
    selected_ids = {list(input_ids)[0]}
    ignored_ids = {list(input_ids)[1]}  # Missing one trace!

    with pytest.raises(ValueError, match="Selected \\+ ignored must equal input"):
        AttentionEvent(
            carrier_id=carrier_id,
            input_trace_ids=input_ids,
            selected_trace_ids=selected_ids,
            ignored_trace_ids=ignored_ids,  # Incomplete accounting
        )
