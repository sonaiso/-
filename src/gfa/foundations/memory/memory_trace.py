"""Memory Trace - NOT a string, but a structured trace.

Memory stores traces of cognitive events, not raw content.

Critical Law:
    الذاكرة تسجل أثر الحدث لا الحدث نفسه.
    "Memory records trace of event, not the event itself."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, FrozenSet, Optional
from datetime import datetime
from uuid import UUID, uuid4


class MemoryTraceKind(Enum):
    """Kind of memory trace.

    Attributes:
        SENSORY: Trace from sensory input
        ATTENTION: Trace from attention focus
        COMPARISON: Trace from comparison operation
        BINDING: Trace from binding operation
        INTERPRETATION: Trace from interpretation
        FEEDBACK: Trace from feedback loop
        COMPOSITE: Composite of multiple traces
    """

    SENSORY = "sensory_trace"
    ATTENTION = "attention_trace"
    COMPARISON = "comparison_trace"
    BINDING = "binding_trace"
    INTERPRETATION = "interpretation_trace"
    FEEDBACK = "feedback_trace"
    COMPOSITE = "composite_trace"


@dataclass(frozen=True)
class TemporalPosition:
    """Temporal position in memory.

    Attributes:
        timestamp: When trace was created
        sequence_id: Sequence number for ordering
        duration_ms: Duration of traced event (if applicable)
    """

    timestamp: datetime
    sequence_id: int
    duration_ms: Optional[float] = None

    def __post_init__(self):
        if self.sequence_id < 0:
            raise ValueError("sequence_id must be non-negative")
        if self.duration_ms is not None and self.duration_ms < 0:
            raise ValueError("duration_ms must be non-negative")


@dataclass(frozen=True)
class MemoryTrace:
    """Memory trace structure.

    NOT a string - a structured trace with:
    - Unique ID
    - Kind of cognitive event
    - Temporal position
    - Source information
    - Content (as abstract data, not string)

    Critical Laws:
        1. Memory stores trace, not raw content
        2. Source must be preserved
        3. Temporal ordering must be preserved
        4. Trace is immutable once created

    Attributes:
        trace_id: Unique identifier
        kind: Kind of memory trace
        temporal: Temporal position
        source_operation: Which cognitive operation created this
        content: Abstract content (NOT raw string)
        metadata: Additional metadata
        parent_traces: Parent traces if composite
    """

    trace_id: UUID
    kind: MemoryTraceKind
    temporal: TemporalPosition
    source_operation: str
    content: Any  # Abstract content, not string
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent_traces: FrozenSet[UUID] = field(default_factory=frozenset)

    def __post_init__(self):
        # Validate source_operation is not empty
        if not self.source_operation or not self.source_operation.strip():
            raise ValueError("source_operation cannot be empty")

        # Validate composite traces have parents
        if self.kind == MemoryTraceKind.COMPOSITE and not self.parent_traces:
            raise ValueError("COMPOSITE trace must have parent_traces")

        # Non-composite traces should not have parents
        if self.kind != MemoryTraceKind.COMPOSITE and self.parent_traces:
            raise ValueError(f"{self.kind.value} trace cannot have parent_traces")

    def is_composite(self) -> bool:
        """Check if trace is composite."""
        return self.kind == MemoryTraceKind.COMPOSITE

    def get_lineage(self) -> FrozenSet[UUID]:
        """Get full lineage including self and parents."""
        return frozenset({self.trace_id}) | self.parent_traces


def make_memory_trace(
    kind: MemoryTraceKind,
    source_operation: str,
    content: Any,
    timestamp: Optional[datetime] = None,
    sequence_id: Optional[int] = None,
    duration_ms: Optional[float] = None,
    metadata: Optional[Dict[str, Any]] = None,
    parent_traces: Optional[FrozenSet[UUID]] = None,
) -> MemoryTrace:
    """Create a memory trace.

    Args:
        kind: Kind of memory trace
        source_operation: Source cognitive operation
        content: Abstract content
        timestamp: When created (default: now)
        sequence_id: Sequence number (default: 0)
        duration_ms: Duration of event
        metadata: Additional metadata
        parent_traces: Parent traces for composite

    Returns:
        MemoryTrace instance

    Raises:
        ValueError: If validation fails
    """
    if timestamp is None:
        timestamp = datetime.now()

    if sequence_id is None:
        sequence_id = 0

    temporal = TemporalPosition(
        timestamp=timestamp,
        sequence_id=sequence_id,
        duration_ms=duration_ms,
    )

    return MemoryTrace(
        trace_id=uuid4(),
        kind=kind,
        temporal=temporal,
        source_operation=source_operation,
        content=content,
        metadata=metadata or {},
        parent_traces=parent_traces or frozenset(),
    )
