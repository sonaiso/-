"""
Residual Taxonomy - Classification of Ignored Traces

Defines how ignored traces are preserved as residuals.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional
from uuid import UUID


class ResidualType(Enum):
    """Types of attention residuals"""

    IGNORED = auto()  # Completely ignored (not selected)
    PARTIALLY_ATTENDED = auto()  # Partially processed
    BELOW_THRESHOLD = auto()  # Didn't meet selection criteria
    CAPACITY_LIMITED = auto()  # Ignored due to capacity limits
    POLICY_EXCLUDED = auto()  # Excluded by policy
    GATE_BLOCKED = auto()  # Blocked by gate
    DEFERRED = auto()  # Postponed for later
    BACKGROUND = auto()  # Moved to background processing


@dataclass(frozen=True)
class IgnoredTrace:
    """
    Trace that was not selected for attention

    Critical Law: Ignored ≠ Deleted
    - Ignored traces are preserved as residuals
    - Can be recovered in future attention operations
    - Maintain original trace_id
    """

    original_trace_id: UUID
    attention_event_id: UUID
    residual_type: ResidualType
    reason: str = ""  # Why ignored
    original_rank: str = "CANDIDATE"  # Preserved from original
    timestamp: Optional[Any] = None
    can_recover: bool = True  # Can be attended in future

    def is_deleted(self) -> bool:
        """Ignored traces are NOT deleted"""
        return False

    def is_lost(self) -> bool:
        """Ignored traces are NOT lost"""
        return False

    def is_preserved(self) -> bool:
        """Ignored traces ARE preserved"""
        return True

    def can_be_recovered(self) -> bool:
        """Ignored traces CAN be recovered"""
        return self.can_recover


@dataclass(frozen=True)
class PartiallyAttendedTrace:
    """
    Trace that received partial attention

    Some aspects attended, others remain as residuals
    """

    original_trace_id: UUID
    attention_event_id: UUID
    attended_aspects: set[str] = field(default_factory=set)
    ignored_aspects: set[str] = field(default_factory=set)
    reason: str = ""
    original_rank: str = "CANDIDATE"
    timestamp: Optional[Any] = None

    def __post_init__(self):
        """Validate partial attention"""
        if not self.attended_aspects:
            raise ValueError("PartiallyAttendedTrace must have at least one attended aspect")

        if not self.ignored_aspects:
            raise ValueError("PartiallyAttendedTrace must have at least one ignored aspect")

        # No overlap allowed
        overlap = self.attended_aspects & self.ignored_aspects
        if overlap:
            raise ValueError(f"Aspects cannot be both attended and ignored: {overlap}")

    def completeness_ratio(self) -> float:
        """Fraction of trace that was attended"""
        total = len(self.attended_aspects) + len(self.ignored_aspects)
        if total == 0:
            return 0.0
        return len(self.attended_aspects) / total

    def ignored_ratio(self) -> float:
        """Fraction of trace that was ignored"""
        return 1.0 - self.completeness_ratio()


@dataclass
class AttentionResidual:
    """
    Complete residual record from attention operation

    Tracks:
    - What was ignored
    - Why it was ignored
    - How it can be recovered
    """

    event_id: UUID
    ignored_traces: list[IgnoredTrace] = field(default_factory=list)
    partial_traces: list[PartiallyAttendedTrace] = field(default_factory=list)
    capacity_overflow: list[UUID] = field(default_factory=list)  # Traces beyond capacity
    policy_excluded: list[UUID] = field(default_factory=list)  # Excluded by policy
    total_ignored_count: int = 0

    def __post_init__(self):
        """Validate residual"""
        # Count should match
        expected = (
            len(self.ignored_traces)
            + len(self.partial_traces)
            + len(self.capacity_overflow)
            + len(self.policy_excluded)
        )

        if self.total_ignored_count != expected:
            raise ValueError(
                f"Total ignored count ({self.total_ignored_count}) "
                f"does not match sum of categories ({expected})"
            )

    def is_empty(self) -> bool:
        """Check if any residuals exist"""
        return self.total_ignored_count == 0

    def can_recover_all(self) -> bool:
        """Check if all ignored traces can be recovered"""
        return all(trace.can_be_recovered() for trace in self.ignored_traces)

    def get_recoverable_trace_ids(self) -> set[UUID]:
        """Get IDs of all recoverable traces"""
        return {
            trace.original_trace_id for trace in self.ignored_traces if trace.can_be_recovered()
        }

    def get_partial_trace_ids(self) -> set[UUID]:
        """Get IDs of partially attended traces"""
        return {trace.original_trace_id for trace in self.partial_traces}
