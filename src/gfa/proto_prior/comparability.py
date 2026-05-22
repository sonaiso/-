"""
Comparability

MANDATORY component of FirstPriorUnit.

Without comparability:
- No pattern detection
- No similarity/difference observation
- No classification
- No learning from repetition or contrast

Comparability defines WHETHER and HOW this unit can be compared to others.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Set


class ComparabilityType(Enum):
    """Type of comparison possible."""
    IDENTICAL = auto()          # Can test for identity
    SIMILAR = auto()            # Can measure similarity
    ORDERED = auto()            # Can establish ordering
    CATEGORICAL = auto()        # Can categorize
    METRIC = auto()             # Can measure distance
    RELATIONAL = auto()         # Can compare relations


@dataclass(frozen=True)
class ComparabilityState:
    """
    Comparability state for FirstPriorUnit.

    This defines what types of comparison are possible with this unit.

    Critical law: No FirstPriorUnit without comparability.
    Without comparability, no learning is possible.
    """

    # At least one comparison type must be supported
    supported_comparisons: Set[ComparabilityType]

    # Optional: comparison metadata
    comparison_precision: Optional[str] = None
    comparison_dimensions: Optional[Set[str]] = None

    def __post_init__(self):
        if not self.supported_comparisons:
            raise ValueError(
                "ComparabilityState requires at least one supported comparison type. "
                "Without comparability, no learning is possible."
            )

        # Convert to frozenset for immutability
        if not isinstance(self.supported_comparisons, frozenset):
            object.__setattr__(
                self,
                'supported_comparisons',
                frozenset(self.supported_comparisons)
            )

        # Convert comparison_dimensions to frozenset if provided
        if self.comparison_dimensions and not isinstance(self.comparison_dimensions, frozenset):
            object.__setattr__(
                self,
                'comparison_dimensions',
                frozenset(self.comparison_dimensions)
            )

    @property
    def is_comparable(self) -> bool:
        """Check if this unit is comparable."""
        return bool(self.supported_comparisons)

    @property
    def supports_metric_comparison(self) -> bool:
        """Check if metric (distance-based) comparison is supported."""
        return ComparabilityType.METRIC in self.supported_comparisons

    @property
    def supports_ordering(self) -> bool:
        """Check if ordering comparison is supported."""
        return ComparabilityType.ORDERED in self.supported_comparisons

    def can_compare_with(self, comparison_type: ComparabilityType) -> bool:
        """Check if specific comparison type is supported."""
        return comparison_type in self.supported_comparisons

    def __str__(self) -> str:
        types = ", ".join(t.name for t in sorted(self.supported_comparisons, key=lambda x: x.name)[:3])
        if len(self.supported_comparisons) > 3:
            types += f", ... (+{len(self.supported_comparisons) - 3} more)"
        return f"ComparabilityState[{types}]"
