"""
Time Anchoring

MANDATORY component of FirstPriorUnit.

Without time anchor:
- No repetition detection
- No temporal ordering
- No change observation
- No causal learning
- No sequential memory

Time is not optional - it is the foundation of learning and prior formation.
"""

from dataclasses import dataclass
from typing import Optional, Union
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class TimeAnchor:
    """
    Time anchoring for FirstPriorUnit.

    This can represent:
    - Absolute timestamp (physical time)
    - Relative time point (sequence order)
    - Time interval/span
    - Abstract temporal position

    Critical law: No FirstPriorUnit without TimeAnchor.
    """

    # At least one must be provided
    timestamp: Optional[datetime] = None
    sequence_order: Optional[int] = None
    relative_time: Optional[Decimal] = None
    temporal_label: Optional[str] = None

    # Optional: time span/interval
    duration: Optional[Decimal] = None
    time_precision: Optional[str] = None

    def __post_init__(self):
        # At least one temporal indicator must be present
        if not any([
            self.timestamp,
            self.sequence_order is not None,
            self.relative_time is not None,
            self.temporal_label
        ]):
            raise ValueError(
                "TimeAnchor requires at least one temporal indicator: "
                "timestamp, sequence_order, relative_time, or temporal_label"
            )

    @property
    def is_valid(self) -> bool:
        """Check if this time anchor is valid."""
        return any([
            self.timestamp,
            self.sequence_order is not None,
            self.relative_time is not None,
            self.temporal_label
        ])

    def __str__(self) -> str:
        if self.timestamp:
            return f"TimeAnchor(timestamp={self.timestamp.isoformat()})"
        elif self.sequence_order is not None:
            return f"TimeAnchor(sequence={self.sequence_order})"
        elif self.relative_time is not None:
            return f"TimeAnchor(relative={self.relative_time})"
        else:
            return f"TimeAnchor(label={self.temporal_label})"
