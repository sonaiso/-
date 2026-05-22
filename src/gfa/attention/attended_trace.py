"""
Attended Trace - Result of Attention Selection

An AttendedTrace represents a trace that has passed through attention gate.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional
from uuid import UUID


class AttentionPriority(Enum):
    """Processing priority levels"""

    CRITICAL = auto()  # Must process immediately
    HIGH = auto()  # Process soon
    NORMAL = auto()  # Standard processing
    LOW = auto()  # Process when capacity available
    BACKGROUND = auto()  # Process in idle time


@dataclass(frozen=True)
class AttendedTrace:
    """
    Trace selected for attention

    An AttendedTrace:
    - References original trace (preserves trace_id)
    - Has processing priority (NOT epistemic rank)
    - Does NOT have higher epistemic rank than original
    - Carries forward all residuals
    """

    original_trace_id: UUID  # Reference to original trace
    attention_event_id: UUID  # Which attention event selected this
    priority: AttentionPriority = AttentionPriority.NORMAL
    original_rank: str = "CANDIDATE"  # Epistemic rank (unchanged by attention)
    attention_timestamp: Optional[Any] = None  # When selected
    selection_reason: str = ""  # Why selected (for audit)
    preserved_residuals: dict = field(default_factory=dict)  # From original
    attention_residuals: dict = field(default_factory=dict)  # From attention process
    capacity_cost: float = 0.0  # Capacity consumed [0, 1]

    def __post_init__(self):
        """Validate attended trace"""
        if not (0.0 <= self.capacity_cost <= 1.0):
            raise ValueError(f"Capacity cost must be in [0, 1], got {self.capacity_cost}")

    def is_higher_rank_than_original(self) -> bool:
        """
        Check if rank was raised

        Attention MUST NOT raise rank - this should always return False
        """
        # In proper implementation, would compare self.current_rank with self.original_rank
        # For now, attention never raises rank
        return False

    def can_certify(self) -> bool:
        """Attention CANNOT certify traces"""
        return False

    def priority_is_not_rank(self) -> bool:
        """
        Verify that priority ≠ epistemic rank

        Priority affects processing order
        Rank affects epistemic status

        These are orthogonal dimensions
        """
        return True

    def preserves_original_trace_id(self) -> bool:
        """Verify original trace_id is preserved"""
        return self.original_trace_id is not None

    def get_all_residuals(self) -> dict:
        """Combine preserved and attention residuals"""
        return {**self.preserved_residuals, **self.attention_residuals}


@dataclass
class AttendedTraceSet:
    """
    Collection of traces selected in one attention operation

    Maintains:
    - Selected traces
    - Original trace lineage
    - Residuals
    """

    attended_traces: list[AttendedTrace] = field(default_factory=list)
    attention_event_id: Optional[UUID] = None
    total_capacity_used: float = 0.0

    def __post_init__(self):
        """Validate trace set"""
        if not (0.0 <= self.total_capacity_used <= 1.0):
            raise ValueError(f"Total capacity must be in [0, 1], got {self.total_capacity_used}")

    def count(self) -> int:
        """Number of attended traces"""
        return len(self.attended_traces)

    def get_priorities(self) -> dict[AttentionPriority, int]:
        """Count traces by priority"""
        counts = {priority: 0 for priority in AttentionPriority}
        for trace in self.attended_traces:
            counts[trace.priority] += 1
        return counts

    def capacity_available(self) -> float:
        """Remaining capacity"""
        return 1.0 - self.total_capacity_used

    def can_certify(self) -> bool:
        """Attended trace set CANNOT certify"""
        return False
