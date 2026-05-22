"""
Retention

MANDATORY component of FirstPriorUnit.

Without retention:
- No memory
- No prior formation
- No learning
- No comparison over time

Retention defines WHETHER and HOW this trace can be preserved for future reference.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class RetentionLevel(Enum):
    """Level of retention capability."""
    NONE = auto()           # Cannot be retained
    TRANSIENT = auto()      # Short-term only
    STABLE = auto()         # Medium-term retention
    PERSISTENT = auto()     # Long-term retention
    PERMANENT = auto()      # Permanent retention


@dataclass(frozen=True)
class RetentionState:
    """
    Retention state for FirstPriorUnit.

    This defines whether and how the trace can be preserved.

    Critical law: No FirstPriorUnit without retention capability.
    Without retention, there can be no prior, no memory, no learning.
    """

    retention_level: RetentionLevel

    # Optional: retention metadata
    retention_duration: Optional[str] = None
    retention_medium: Optional[str] = None  # e.g., "memory", "record", "physical trace"
    retention_quality: Optional[str] = None  # e.g., "high fidelity", "lossy", "compressed"

    def __post_init__(self):
        if self.retention_level == RetentionLevel.NONE:
            raise ValueError(
                "FirstPriorUnit requires retention capability. "
                "RetentionLevel.NONE is not allowed for prior formation."
            )

    @property
    def is_retainable(self) -> bool:
        """Check if this unit can be retained."""
        return self.retention_level != RetentionLevel.NONE

    @property
    def is_stable_or_better(self) -> bool:
        """Check if retention is stable or better."""
        return self.retention_level in {
            RetentionLevel.STABLE,
            RetentionLevel.PERSISTENT,
            RetentionLevel.PERMANENT
        }

    def __str__(self) -> str:
        return f"RetentionState({self.retention_level.name})"
