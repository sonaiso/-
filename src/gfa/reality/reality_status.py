"""
Reality Status - Levels of Reality

The progression from physical to hypothetical:
1. PHYSICAL: Matter, energy, forces (fundamental)
2. BIOLOGICAL: Living organisms, life processes
3. SOCIAL: Social structures, institutions, collective patterns
4. CONCEPTUAL: Concepts, categories, abstractions
5. SYMBOLIC: Symbols, signs, representations
6. HYPOTHETICAL: Hypothesized entities, theoretical constructs

Critical laws:
- Physical reality is foundational
- Higher levels emerge from lower levels
- Hypothetical cannot produce physical effects without bridge
- Status transitions require validation
- Observer embodiment is BIOLOGICAL (at minimum)
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, FrozenSet


class RealityStatus(Enum):
    """
    Levels of reality from physical to hypothetical.

    CRITICAL: This is an ontological hierarchy, not epistemic.
    Physical reality is foundational; hypothetical is derived.
    """
    PHYSICAL = auto()       # Matter, energy, forces
    BIOLOGICAL = auto()     # Living organisms
    SOCIAL = auto()         # Social structures, institutions
    CONCEPTUAL = auto()     # Concepts, categories
    SYMBOLIC = auto()       # Symbols, signs, representations
    HYPOTHETICAL = auto()   # Hypothesized entities

    def is_foundational(self) -> bool:
        """Check if this status is foundational (physical or biological)."""
        return self in {RealityStatus.PHYSICAL, RealityStatus.BIOLOGICAL}

    def is_emergent(self) -> bool:
        """Check if this status is emergent (social, conceptual, symbolic)."""
        return self in {RealityStatus.SOCIAL, RealityStatus.CONCEPTUAL, RealityStatus.SYMBOLIC}

    def is_hypothetical(self) -> bool:
        """Check if this is hypothetical status."""
        return self == RealityStatus.HYPOTHETICAL

    def can_produce_physical_effect(self) -> bool:
        """
        Can this reality status produce physical effects?

        CRITICAL LAW: Only physical and biological can directly produce physical effects.
        Social/conceptual/symbolic require embodied mediation.
        Hypothetical cannot produce physical effects without bridge.
        """
        return self in {RealityStatus.PHYSICAL, RealityStatus.BIOLOGICAL}

    def requires_bridge_for_physical(self) -> bool:
        """
        Does this status require a bridge to produce physical effects?

        CRITICAL LAW: Hypothetical always requires bridge.
        Social/conceptual/symbolic require embodied mediation.
        """
        return self in {
            RealityStatus.SOCIAL,
            RealityStatus.CONCEPTUAL,
            RealityStatus.SYMBOLIC,
            RealityStatus.HYPOTHETICAL
        }

    def can_promote_to(self, target: "RealityStatus") -> bool:
        """
        Check if promotion to target status is valid.

        Status hierarchy:
        PHYSICAL (0) → BIOLOGICAL (1) → SOCIAL (2) → CONCEPTUAL (3) → SYMBOLIC (4) → HYPOTHETICAL (5)
        """
        status_order = {
            RealityStatus.PHYSICAL: 0,
            RealityStatus.BIOLOGICAL: 1,
            RealityStatus.SOCIAL: 2,
            RealityStatus.CONCEPTUAL: 3,
            RealityStatus.SYMBOLIC: 4,
            RealityStatus.HYPOTHETICAL: 5
        }
        return status_order.get(self, 0) < status_order.get(target, 0)


@dataclass(frozen=True)
class RealityStatusDescriptor:
    """
    Descriptor for reality status with constraints.

    This describes the reality status of an entity with its constraints
    and requirements for status transitions.
    """

    status: RealityStatus
    status_description: Optional[str] = None
    emergence_conditions: Optional[FrozenSet[str]] = None
    required_substrate: Optional[RealityStatus] = None

    def __post_init__(self):
        # Convert sets to frozensets for immutability
        if self.emergence_conditions and not isinstance(self.emergence_conditions, frozenset):
            object.__setattr__(
                self,
                'emergence_conditions',
                frozenset(self.emergence_conditions)
            )

        # Validate substrate requirements
        if self.required_substrate:
            if not isinstance(self.required_substrate, RealityStatus):
                raise ValueError("required_substrate must be RealityStatus enum")

            # Check substrate is lower in hierarchy
            if not self.required_substrate.can_promote_to(self.status):
                raise ValueError(
                    f"Invalid substrate: {self.required_substrate.name} "
                    f"cannot support {self.status.name}"
                )

    @property
    def is_foundational(self) -> bool:
        """Check if this is foundational status."""
        return self.status.is_foundational()

    @property
    def requires_physical_substrate(self) -> bool:
        """Check if this status requires physical substrate."""
        return self.status != RealityStatus.PHYSICAL

    def __str__(self) -> str:
        if self.required_substrate:
            return f"RealityStatus({self.status.name}, substrate={self.required_substrate.name})"
        return f"RealityStatus({self.status.name})"
