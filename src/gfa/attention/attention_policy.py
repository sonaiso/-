"""
Attention Policy - Selection Strategy

An AttentionPolicy defines how traces are selected for attention.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional, Set
from uuid import UUID


class PolicyType(Enum):
    """Types of attention policies"""

    SALIENCE_BASED = auto()  # Select most salient
    GOAL_DIRECTED = auto()  # Select relevant to goal
    NOVELTY_BASED = auto()  # Select novel/unexpected
    THREAT_BASED = auto()  # Select potential threats
    CURIOSITY_BASED = auto()  # Select interesting/uncertain
    RESOURCE_LIMITED = auto()  # Select within capacity limits
    MIXED = auto()  # Combination of strategies


@dataclass(frozen=True)
class SelectionCriterion:
    """
    Single selection criterion

    Defines one aspect to consider when selecting traces
    """

    criterion_id: str
    feature_name: str  # What feature to evaluate
    threshold: Optional[float] = None  # Minimum/maximum value
    weight: float = 1.0  # Importance [0, 1]
    description: str = ""

    def __post_init__(self):
        """Validate criterion"""
        if not (0.0 <= self.weight <= 1.0):
            raise ValueError(f"Weight must be in [0, 1], got {self.weight}")

        if self.threshold is not None and not (0.0 <= self.threshold <= 1.0):
            raise ValueError(f"Threshold must be in [0, 1], got {self.threshold}")


@dataclass
class AttentionPolicy:
    """
    Strategy for selecting traces

    An AttentionPolicy:
    - Defines selection criteria
    - Does NOT certify selected traces
    - Does NOT raise rank
    - Operates within capacity constraints
    """

    policy_id: str
    policy_type: PolicyType
    criteria: list[SelectionCriterion] = field(default_factory=list)
    max_selection_ratio: float = 1.0  # Maximum fraction to select [0, 1]
    min_selection_count: int = 0  # Minimum number to select
    max_selection_count: Optional[int] = None  # Maximum number to select
    capacity_budget: float = 1.0  # Available capacity [0, 1]
    description: str = ""

    def __post_init__(self):
        """Validate policy"""
        if not (0.0 <= self.max_selection_ratio <= 1.0):
            raise ValueError(f"Selection ratio must be in [0, 1], got {self.max_selection_ratio}")

        if self.min_selection_count < 0:
            raise ValueError(f"Min selection count must be >= 0, got {self.min_selection_count}")

        if self.max_selection_count is not None and self.max_selection_count < self.min_selection_count:
            raise ValueError(
                f"Max selection count ({self.max_selection_count}) must be >= "
                f"min selection count ({self.min_selection_count})"
            )

        if not (0.0 <= self.capacity_budget <= 1.0):
            raise ValueError(f"Capacity budget must be in [0, 1], got {self.capacity_budget}")

    def can_select_all(self, trace_count: int) -> bool:
        """Check if policy allows selecting all traces"""
        if self.max_selection_ratio < 1.0:
            return False

        if self.max_selection_count is not None and self.max_selection_count < trace_count:
            return False

        return True

    def max_allowed_selection(self, trace_count: int) -> int:
        """Calculate maximum number of traces that can be selected"""
        max_by_ratio = int(trace_count * self.max_selection_ratio)

        if self.max_selection_count is None:
            return max_by_ratio

        return min(max_by_ratio, self.max_selection_count)

    def min_required_selection(self) -> int:
        """Minimum number of traces that must be selected"""
        return self.min_selection_count

    def can_certify(self) -> bool:
        """Policy CANNOT certify"""
        return False

    def can_raise_rank(self) -> bool:
        """Policy CANNOT raise rank"""
        return False

    def can_create_memory(self) -> bool:
        """Policy does NOT create memory"""
        return False
