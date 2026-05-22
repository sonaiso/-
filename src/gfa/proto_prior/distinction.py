"""
Distinction

MANDATORY component of FirstPriorUnit.

Without distinction:
- No unit exists (indistinguishable from background)
- No identity
- No comparison possible
- No learning possible

Distinction is the most fundamental requirement - it defines THAT something exists.
"""

from dataclasses import dataclass
from typing import Optional, Any, Set


@dataclass(frozen=True)
class Distinction:
    """
    Distinction from background.

    This records HOW an entity/effect is distinguished from its background/context.

    Without distinction, there is no "unit" to record as FirstPriorUnit.
    """

    # What distinguishes this from background
    distinguishing_features: Set[str]

    # Optional: what is the background/context
    background_context: Optional[str] = None

    # Optional: how strong is the distinction
    distinction_strength: Optional[str] = None  # e.g., "sharp", "gradual", "threshold"

    def __post_init__(self):
        if not self.distinguishing_features:
            raise ValueError(
                "Distinction requires at least one distinguishing feature. "
                "Without distinction, there is no unit."
            )

        # Convert to frozenset for immutability
        if not isinstance(self.distinguishing_features, frozenset):
            object.__setattr__(
                self,
                'distinguishing_features',
                frozenset(self.distinguishing_features)
            )

    @property
    def is_valid(self) -> bool:
        """Check if this distinction is valid."""
        return bool(self.distinguishing_features)

    @property
    def feature_count(self) -> int:
        """Return number of distinguishing features."""
        return len(self.distinguishing_features)

    def __str__(self) -> str:
        features = ", ".join(sorted(self.distinguishing_features)[:3])
        if len(self.distinguishing_features) > 3:
            features += f", ... (+{len(self.distinguishing_features) - 3} more)"
        return f"Distinction[{features}]"
