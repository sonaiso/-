"""Memory Storage - Geometry of memory storage.

Defines storage capacity, organization, and retrieval geometry.

Critical Law:
    السعة محدودة والتنظيم هندسي.
    "Capacity is limited and organization is geometric."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, FrozenSet, List, Optional
from uuid import UUID

from .memory_trace import MemoryTrace, MemoryTraceKind


class StorageCapacity(Enum):
    """Storage capacity limits.

    Attributes:
        SENSORY_BUFFER: Very limited, ~500ms
        SHORT_TERM: Limited, ~7±2 items
        WORKING: Limited, ~4 items active
        LONG_TERM: Effectively unlimited but with decay
    """

    SENSORY_BUFFER = "sensory_buffer"
    SHORT_TERM = "short_term"
    WORKING = "working"
    LONG_TERM = "long_term"


@dataclass(frozen=True)
class StorageGeometry:
    """Geometry of memory storage organization.

    Defines how traces are organized in memory space.

    Attributes:
        capacity_type: Type of storage capacity
        max_items: Maximum number of items (None = unlimited)
        temporal_ordering: Whether items preserve temporal order
        associative_links: Whether items can be associatively linked
        decay_enabled: Whether decay occurs over time
    """

    capacity_type: StorageCapacity
    max_items: Optional[int]
    temporal_ordering: bool
    associative_links: bool
    decay_enabled: bool

    def __post_init__(self):
        if self.max_items is not None and self.max_items < 0:
            raise ValueError("max_items must be non-negative")


# Standard storage geometries
SENSORY_STORAGE = StorageGeometry(
    capacity_type=StorageCapacity.SENSORY_BUFFER,
    max_items=10,
    temporal_ordering=True,
    associative_links=False,
    decay_enabled=True,
)

SHORT_TERM_STORAGE = StorageGeometry(
    capacity_type=StorageCapacity.SHORT_TERM,
    max_items=7,
    temporal_ordering=True,
    associative_links=True,
    decay_enabled=True,
)

WORKING_STORAGE = StorageGeometry(
    capacity_type=StorageCapacity.WORKING,
    max_items=4,
    temporal_ordering=False,
    associative_links=True,
    decay_enabled=False,
)

LONG_TERM_STORAGE = StorageGeometry(
    capacity_type=StorageCapacity.LONG_TERM,
    max_items=None,  # Unlimited
    temporal_ordering=True,
    associative_links=True,
    decay_enabled=True,
)


@dataclass
class MemoryStorage:
    """Memory storage container.

    Stores traces according to storage geometry.

    Critical Laws:
        1. Capacity limits enforced
        2. Temporal ordering preserved (if required)
        3. No raw content storage (only traces)
        4. Source preserved
        5. Decay occurs over time

    Attributes:
        geometry: Storage geometry
        traces: Stored memory traces
        associations: Associative links between traces
        next_sequence_id: Next sequence ID for temporal ordering
    """

    geometry: StorageGeometry
    traces: Dict[UUID, MemoryTrace] = field(default_factory=dict)
    associations: Dict[UUID, FrozenSet[UUID]] = field(default_factory=dict)
    next_sequence_id: int = 0

    def __post_init__(self):
        """Initialize storage."""
        # Validate capacity on initialization
        if self.geometry.max_items is not None:
            if len(self.traces) > self.geometry.max_items:
                raise ValueError(
                    f"Initial traces ({len(self.traces)}) exceeds "
                    f"capacity ({self.geometry.max_items})"
                )

    def is_full(self) -> bool:
        """Check if storage is at capacity."""
        if self.geometry.max_items is None:
            return False
        return len(self.traces) >= self.geometry.max_items

    def can_store(self, trace: MemoryTrace) -> bool:
        """Check if trace can be stored.

        Args:
            trace: Memory trace to check

        Returns:
            True if can be stored
        """
        # Check capacity
        if self.is_full() and trace.trace_id not in self.traces:
            return False

        # Check trace validity
        if not isinstance(trace, MemoryTrace):
            return False

        return True

    def store(self, trace: MemoryTrace) -> bool:
        """Store a memory trace.

        Args:
            trace: Memory trace to store

        Returns:
            True if stored successfully

        Raises:
            ValueError: If storage is full or trace invalid
        """
        if not self.can_store(trace):
            raise ValueError("Cannot store trace: capacity exceeded or invalid trace")

        self.traces[trace.trace_id] = trace
        self.next_sequence_id = max(self.next_sequence_id, trace.temporal.sequence_id + 1)

        return True

    def retrieve(self, trace_id: UUID) -> Optional[MemoryTrace]:
        """Retrieve trace by ID.

        Args:
            trace_id: Trace identifier

        Returns:
            MemoryTrace if found, None otherwise
        """
        return self.traces.get(trace_id)

    def retrieve_by_kind(self, kind: MemoryTraceKind) -> List[MemoryTrace]:
        """Retrieve all traces of given kind.

        Args:
            kind: Memory trace kind

        Returns:
            List of matching traces
        """
        return [trace for trace in self.traces.values() if trace.kind == kind]

    def retrieve_temporal_range(
        self, start_seq: int, end_seq: int
    ) -> List[MemoryTrace]:
        """Retrieve traces in temporal range.

        Args:
            start_seq: Start sequence ID (inclusive)
            end_seq: End sequence ID (inclusive)

        Returns:
            List of traces in range, ordered by sequence
        """
        if not self.geometry.temporal_ordering:
            raise ValueError("Storage does not preserve temporal ordering")

        traces = [
            trace
            for trace in self.traces.values()
            if start_seq <= trace.temporal.sequence_id <= end_seq
        ]

        return sorted(traces, key=lambda t: t.temporal.sequence_id)

    def add_association(self, trace_id: UUID, associated_id: UUID) -> bool:
        """Add associative link between traces.

        Args:
            trace_id: Source trace ID
            associated_id: Associated trace ID

        Returns:
            True if association added

        Raises:
            ValueError: If storage doesn't support associations
        """
        if not self.geometry.associative_links:
            raise ValueError("Storage does not support associative links")

        if trace_id not in self.traces or associated_id not in self.traces:
            raise ValueError("Both traces must exist in storage")

        current = self.associations.get(trace_id, frozenset())
        self.associations[trace_id] = current | {associated_id}

        return True

    def get_associations(self, trace_id: UUID) -> FrozenSet[UUID]:
        """Get associated traces.

        Args:
            trace_id: Trace ID

        Returns:
            Set of associated trace IDs
        """
        return self.associations.get(trace_id, frozenset())

    def count(self) -> int:
        """Count stored traces."""
        return len(self.traces)
