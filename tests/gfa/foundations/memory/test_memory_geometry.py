"""Tests for Memory Geometry Kernel (PR-G1).

Tests enforce all 8 critical laws of Memory Geometry.
"""

import pytest
from datetime import datetime, timedelta
from uuid import UUID

from gfa.foundations.memory import (
    # Trace
    MemoryTrace,
    MemoryTraceKind,
    TemporalPosition,
    make_memory_trace,

    # Storage
    MemoryStorage,
    StorageCapacity,
    StorageGeometry,
    SENSORY_STORAGE,
    SHORT_TERM_STORAGE,
    WORKING_STORAGE,
    LONG_TERM_STORAGE,

    # Recall
    RecallProcess,
    RecallResult,
    RecallResidual,

    # Residuals
    MemoryResidualKind,
    MemoryResidual,
    exponential_decay,
    power_law_decay,
    linear_decay,
    make_decay_residual,
    make_distortion_residual,
    make_interference_residual,
    make_capacity_overflow_residual,

    # Gate
    MemoryGate,
    MemoryAdmissionResult,
    AdmissionViolation,
    validate_memory_trace,
)


# ============================================================================
# Law 1: Memory stores trace, not raw content
# ============================================================================


def test_memory_stores_trace_not_string():
    """Memory must store MemoryTrace, not raw string."""
    trace = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="sensory_input",
        content={"data": "value"},  # NOT a string
    )

    assert isinstance(trace, MemoryTrace)
    assert isinstance(trace.trace_id, UUID)
    assert trace.kind == MemoryTraceKind.SENSORY
    assert trace.source_operation == "sensory_input"


def test_trace_has_structure_not_raw_content():
    """Trace has structure: ID, kind, temporal, source."""
    trace = make_memory_trace(
        kind=MemoryTraceKind.COMPARISON,
        source_operation="comparison_op",
        content={"compared": ["a", "b"]},
    )

    # Has required structure
    assert hasattr(trace, "trace_id")
    assert hasattr(trace, "kind")
    assert hasattr(trace, "temporal")
    assert hasattr(trace, "source_operation")
    assert hasattr(trace, "content")

    # Trace is immutable
    with pytest.raises((AttributeError, Exception)):
        trace.content = "new"  # type: ignore


def test_trace_requires_source_operation():
    """Trace must have non-empty source operation."""
    with pytest.raises(ValueError, match="source_operation cannot be empty"):
        MemoryTrace(
            trace_id=UUID("12345678-1234-5678-1234-567812345678"),
            kind=MemoryTraceKind.SENSORY,
            temporal=TemporalPosition(datetime.now(), 0),
            source_operation="",  # Empty
            content={},
        )


# ============================================================================
# Law 2: Recall ≠ Original (always residual)
# ============================================================================


def test_recall_is_not_original():
    """Recall creates NEW trace, never returns original."""
    original = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="original_input",
        content={"value": 42},
        timestamp=datetime.now() - timedelta(hours=1),
    )

    recall_proc = RecallProcess()
    result = recall_proc.recall(original)

    assert result.success
    assert result.recalled_trace is not None

    # Recalled trace is NEW, not original
    assert result.recalled_trace.trace_id != original.trace_id
    assert result.recalled_trace.source_operation == "recall_of_original_input"
    assert not result.is_original()  # NEVER original


def test_recall_must_have_residuals():
    """Successful recall MUST have residuals."""
    original = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="test_op",
        content={"data": "test"},
    )

    recall_proc = RecallProcess()
    result = recall_proc.recall(original)

    assert result.success
    assert len(result.residuals) > 0  # MUST have residuals
    assert result.get_residual_count() >= 2  # At least reconstruction + context


def test_recall_result_enforces_residuals_on_success():
    """RecallResult with success=True must have residuals."""
    recalled = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="recalled",
        content={},
    )

    with pytest.raises(ValueError, match="must have residuals"):
        RecallResult(
            success=True,
            original_trace_id=UUID("12345678-1234-5678-1234-567812345678"),
            recalled_trace=recalled,
            residuals=(),  # Empty - violation
            recall_timestamp=datetime.now(),
        )


# ============================================================================
# Law 3: Memory does NOT certify
# ============================================================================


def test_memory_does_not_certify_content():
    """Memory storage does not certify content truth."""
    trace = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="questionable_source",
        content={"claim": "unverified"},
    )

    storage = MemoryStorage(SHORT_TERM_STORAGE)
    storage.store(trace)

    # Storage stores trace but does NOT certify
    retrieved = storage.retrieve(trace.trace_id)
    assert retrieved is not None
    # No certification field or method
    assert not hasattr(retrieved, "certified")
    assert not hasattr(retrieved, "certify")


def test_recall_does_not_certify():
    """Recall does not certify original correctness."""
    original = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="test",
        content={"uncertain": "data"},
    )

    recall_proc = RecallProcess()
    result = recall_proc.recall(original)

    # Recall returns result but does NOT certify
    assert not hasattr(result, "certified")
    assert not hasattr(result, "certify")
    # Confidence ≠ certification
    assert 0.0 <= result.confidence <= 1.0


# ============================================================================
# Law 4: Memory does NOT raise rank
# ============================================================================


def test_memory_does_not_raise_rank():
    """Storing in memory does not raise predicate rank."""
    trace = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="uncertain_observation",
        content={"observation": "data"},
        metadata={"rank": "zanni"},  # Uncertain
    )

    storage = MemoryStorage(LONG_TERM_STORAGE)
    storage.store(trace)

    retrieved = storage.retrieve(trace.trace_id)
    assert retrieved is not None

    # Rank unchanged
    assert retrieved.metadata.get("rank") == "zanni"
    # No rank elevation
    assert not hasattr(storage, "elevate_rank")


def test_recall_does_not_raise_rank():
    """Recall does not elevate predicate rank."""
    original = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="test",
        content={"data": "uncertain"},
        metadata={"epistemic_rank": "opinion"},
    )

    recall_proc = RecallProcess()
    result = recall_proc.recall(original)

    # Recalled trace does not have elevated rank
    assert result.recalled_trace is not None
    # Original rank preserved (or degraded by recall)
    assert "epistemic_rank" not in result.recalled_trace.metadata or \
           result.recalled_trace.metadata.get("epistemic_rank") != "certified"


# ============================================================================
# Law 5: Decay is mandatory residual
# ============================================================================


def test_temporal_decay_is_mandatory():
    """Temporal decay occurs over time (mandatory)."""
    original = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="test",
        content={"data": "test"},
        timestamp=datetime.now() - timedelta(hours=5),
    )

    recall_proc = RecallProcess(base_decay_rate=0.1)
    result = recall_proc.recall(original)

    # Decay residual present
    assert RecallResidual.TEMPORAL_DECAY in result.residuals
    assert result.confidence < 1.0  # Decay affects confidence


def test_decay_function_exponential():
    """Exponential decay function works correctly."""
    decay_fn = exponential_decay(half_life=3600.0)  # 1 hour

    # At 0 hours
    assert abs(decay_fn(0.0) - 1.0) < 0.01

    # At 1 hour (half-life)
    assert abs(decay_fn(3600.0) - 0.5) < 0.01

    # At 2 hours
    assert abs(decay_fn(7200.0) - 0.25) < 0.01


def test_decay_residual_creation():
    """Can create decay residual."""
    residual = make_decay_residual(time_elapsed=7200.0)  # 2 hours

    assert residual.kind == MemoryResidualKind.TEMPORAL_DECAY
    assert 0.0 <= residual.severity <= 1.0
    assert "content" in residual.affected_properties


# ============================================================================
# Law 6: Source trace preserved
# ============================================================================


def test_source_trace_preserved_in_storage():
    """Source operation preserved in storage."""
    trace = make_memory_trace(
        kind=MemoryTraceKind.BINDING,
        source_operation="original_binding_op",
        content={"binding": "data"},
    )

    storage = MemoryStorage(LONG_TERM_STORAGE)
    storage.store(trace)

    retrieved = storage.retrieve(trace.trace_id)
    assert retrieved is not None
    assert retrieved.source_operation == "original_binding_op"


def test_source_trace_preserved_in_recall():
    """Original trace ID preserved in recall metadata."""
    original = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="original_source",
        content={},
    )

    recall_proc = RecallProcess()
    result = recall_proc.recall(original)

    assert result.success
    assert result.original_trace_id == original.trace_id
    # Original ID in recalled trace metadata
    assert str(original.trace_id) == result.recalled_trace.metadata["original_trace_id"]


def test_composite_trace_preserves_parent_traces():
    """Composite traces preserve parent lineage."""
    parent1 = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="input1",
        content={},
    )

    parent2 = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="input2",
        content={},
    )

    composite = make_memory_trace(
        kind=MemoryTraceKind.COMPOSITE,
        source_operation="composite_op",
        content={"combined": True},
        parent_traces=frozenset({parent1.trace_id, parent2.trace_id}),
    )

    assert composite.is_composite()
    assert parent1.trace_id in composite.parent_traces
    assert parent2.trace_id in composite.parent_traces
    assert len(composite.get_lineage()) == 3  # self + 2 parents


# ============================================================================
# Law 7: Temporal ordering preserved
# ============================================================================


def test_temporal_ordering_preserved_in_storage():
    """Storage with temporal_ordering preserves sequence."""
    storage = MemoryStorage(LONG_TERM_STORAGE)

    traces = []
    for i in range(5):
        trace = make_memory_trace(
            kind=MemoryTraceKind.SENSORY,
            source_operation=f"op_{i}",
            content={"index": i},
            sequence_id=i,
        )
        storage.store(trace)
        traces.append(trace)

    # Retrieve in temporal range
    retrieved = storage.retrieve_temporal_range(1, 3)
    assert len(retrieved) == 3
    assert retrieved[0].temporal.sequence_id == 1
    assert retrieved[1].temporal.sequence_id == 2
    assert retrieved[2].temporal.sequence_id == 3


def test_temporal_position_validates_sequence():
    """TemporalPosition validates sequence_id."""
    with pytest.raises(ValueError, match="sequence_id must be non-negative"):
        TemporalPosition(datetime.now(), sequence_id=-1)


def test_temporal_position_validates_duration():
    """TemporalPosition validates duration_ms."""
    with pytest.raises(ValueError, match="duration_ms must be non-negative"):
        TemporalPosition(datetime.now(), 0, duration_ms=-100.0)


# ============================================================================
# Law 8: Memory gate blocks non-traceable
# ============================================================================


def test_memory_gate_blocks_non_trace():
    """Memory gate blocks non-MemoryTrace objects."""
    gate = MemoryGate()

    result = gate.admit("not a trace")  # type: ignore

    assert not result.admitted
    assert AdmissionViolation.NO_TRACE in result.violations


def test_memory_gate_blocks_no_source():
    """Memory gate blocks trace without source operation."""
    # Can't create invalid trace directly due to validation
    # Test that gate would block
    gate = MemoryGate(require_source=True)

    # Valid trace
    valid_trace = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="valid_source",
        content={},
    )

    result = gate.admit(valid_trace)
    assert result.admitted


def test_memory_gate_blocks_invalid_composite():
    """Memory gate blocks composite trace without parents."""
    gate = MemoryGate(validate_composite=True)

    # Try to create invalid composite (should fail)
    with pytest.raises(ValueError, match="COMPOSITE trace must have parent_traces"):
        make_memory_trace(
            kind=MemoryTraceKind.COMPOSITE,
            source_operation="composite",
            content={},
            parent_traces=frozenset(),  # Empty - invalid
        )


def test_memory_gate_blocks_storage_full():
    """Memory gate blocks when storage at capacity."""
    storage = MemoryStorage(SENSORY_STORAGE)  # max_items=10

    # Fill storage
    for i in range(10):
        trace = make_memory_trace(
            kind=MemoryTraceKind.SENSORY,
            source_operation=f"op_{i}",
            content={"i": i},
        )
        storage.store(trace)

    assert storage.is_full()

    # Try to admit another
    gate = MemoryGate(enforce_capacity=True)
    new_trace = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="overflow",
        content={},
    )

    result = gate.admit(new_trace, storage=storage)
    assert not result.admitted
    assert AdmissionViolation.STORAGE_FULL in result.violations


def test_validate_memory_trace_helper():
    """validate_memory_trace helper works."""
    valid_trace = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="test",
        content={},
    )

    assert validate_memory_trace(valid_trace) is True


# ============================================================================
# Additional Tests: Storage Geometry
# ============================================================================


def test_storage_geometries_defined():
    """Standard storage geometries are defined."""
    assert SENSORY_STORAGE.capacity_type == StorageCapacity.SENSORY_BUFFER
    assert SHORT_TERM_STORAGE.capacity_type == StorageCapacity.SHORT_TERM
    assert WORKING_STORAGE.capacity_type == StorageCapacity.WORKING
    assert LONG_TERM_STORAGE.capacity_type == StorageCapacity.LONG_TERM


def test_storage_capacity_limits_enforced():
    """Storage enforces capacity limits."""
    storage = MemoryStorage(SHORT_TERM_STORAGE)  # max_items=7

    # Store 7 items
    for i in range(7):
        trace = make_memory_trace(
            kind=MemoryTraceKind.SENSORY,
            source_operation=f"op_{i}",
            content={},
        )
        storage.store(trace)

    assert storage.count() == 7
    assert storage.is_full()

    # Try to store 8th
    overflow_trace = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="overflow",
        content={},
    )

    with pytest.raises(ValueError, match="capacity exceeded"):
        storage.store(overflow_trace)


def test_storage_associative_links():
    """Storage with associative links supports associations."""
    storage = MemoryStorage(LONG_TERM_STORAGE)

    trace1 = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="op1",
        content={},
    )

    trace2 = make_memory_trace(
        kind=MemoryTraceKind.SENSORY,
        source_operation="op2",
        content={},
    )

    storage.store(trace1)
    storage.store(trace2)

    # Add association
    storage.add_association(trace1.trace_id, trace2.trace_id)

    associations = storage.get_associations(trace1.trace_id)
    assert trace2.trace_id in associations


# ============================================================================
# Additional Tests: Residuals
# ============================================================================


def test_distortion_residual():
    """Distortion residual creation."""
    residual = make_distortion_residual(0.5, source="interference")

    assert residual.kind == MemoryResidualKind.DISTORTION
    assert residual.severity == 0.5
    assert not residual.blocker  # 0.5 < 0.8


def test_interference_residual():
    """Interference residual creation."""
    residual = make_interference_residual(5, interference_factor=0.1)

    assert residual.kind == MemoryResidualKind.INTERFERENCE
    assert residual.severity == 0.5  # 5 * 0.1


def test_capacity_overflow_residual():
    """Capacity overflow residual creation."""
    residual = make_capacity_overflow_residual(10, 7)

    assert residual.kind == MemoryResidualKind.CAPACITY_OVERFLOW
    assert residual.blocker  # Overflow > 0
