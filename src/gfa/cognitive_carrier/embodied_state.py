"""
EmbodiedState - The Physical/Biological State of the Carrier

The cognitive carrier is not disembodied. It exists in a physical/biological state
that constrains and enables its cognitive capacities.

Critical laws:
- Carrier is embodied (not abstract)
- Embodiment state affects capacity availability
- Degraded embodiment may reduce capacities
- Embodiment state is not epistemic rank
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, FrozenSet


class EmbodimentType(Enum):
    """Type of embodiment for the cognitive carrier."""
    BIOLOGICAL = auto()      # Living organism
    ARTIFICIAL = auto()      # Artificial system
    HYBRID = auto()          # Hybrid biological-artificial
    SIMULATED = auto()       # Simulated cognitive system


@dataclass(frozen=True)
class EmbodiedState:
    """
    The embodiment state of a cognitive carrier.

    This represents the physical/biological substrate that enables
    cognitive processing.

    CRITICAL: Embodiment state affects capacity availability but
    does NOT determine epistemic rank.
    """

    embodiment_type: EmbodimentType
    functional_status: str  # e.g., "fully_functional", "degraded", "impaired"
    known_limitations: FrozenSet[str]
    embodiment_description: Optional[str] = None

    def __post_init__(self):
        # Validate functional_status
        if not self.functional_status or not self.functional_status.strip():
            raise ValueError("functional_status cannot be empty")

        # Validate known_limitations
        if not isinstance(self.known_limitations, frozenset):
            object.__setattr__(
                self,
                'known_limitations',
                frozenset(self.known_limitations) if self.known_limitations else frozenset()
            )

    @property
    def is_biological(self) -> bool:
        """Check if this is biological embodiment."""
        return self.embodiment_type == EmbodimentType.BIOLOGICAL

    @property
    def is_artificial(self) -> bool:
        """Check if this is artificial embodiment."""
        return self.embodiment_type == EmbodimentType.ARTIFICIAL

    @property
    def is_functional(self) -> bool:
        """Check if embodiment is fully functional."""
        return "functional" in self.functional_status.lower()

    @property
    def is_degraded(self) -> bool:
        """Check if embodiment is degraded."""
        return "degraded" in self.functional_status.lower()

    @property
    def has_limitations(self) -> bool:
        """Check if there are known limitations."""
        return bool(self.known_limitations)

    def __str__(self) -> str:
        return (
            f"EmbodiedState("
            f"type={self.embodiment_type.name}, "
            f"status={self.functional_status})"
        )
