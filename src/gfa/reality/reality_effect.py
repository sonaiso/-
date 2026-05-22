"""
RealityEffect - What Reality Produces

RealityEffect is DISTINCT from reality itself.
- Reality produces effects
- Effects can be detected, measured, observed
- Effects are evidence of reality, not reality itself

Critical laws:
- RealityEffect ≠ Reality
- Effects can be sensory, causal, relational, structural
- Effects have source (what produced them)
- Effects have manifestation (how they appear)
- Effects can propagate through domains
- Hypothetical effects require validation
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional, FrozenSet
from uuid import UUID, uuid4

from .reality_status import RealityStatus


class EffectType(Enum):
    """Types of reality effects."""
    SENSORY = auto()        # Detectable by senses
    CAUSAL = auto()         # Causal influence
    RELATIONAL = auto()     # Relational change
    STRUCTURAL = auto()     # Structural modification
    EMERGENT = auto()       # Emergent property
    CONSTRAINT = auto()     # Constraint/limitation


@dataclass(frozen=True)
class RealityEffect:
    """
    An effect produced by reality.

    CRITICAL: RealityEffect ≠ Reality itself.
    Effects are evidence, manifestations, consequences - not the reality that produces them.

    This is the bridge between reality and sensory transfer:
    Reality → RealityEffect → SensoryTransfer → FirstPriorUnit
    """

    # What kind of effect
    effect_type: EffectType

    # What produced this effect (description, not the reality itself)
    source_description: str

    # How this effect manifests
    manifestation: Any

    # Reality status of the source
    source_status: RealityStatus

    # Fields with defaults (must come last)
    effect_id: UUID = field(default_factory=uuid4)
    effect_description: Optional[str] = None
    propagation_conditions: Optional[FrozenSet[str]] = None
    known_limitations: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        # Validate source_description
        if not self.source_description or not self.source_description.strip():
            raise ValueError("source_description cannot be empty")

        # Validate manifestation
        if self.manifestation is None:
            raise ValueError("manifestation is mandatory")

        # Convert sets to frozensets for immutability
        if self.propagation_conditions and not isinstance(self.propagation_conditions, frozenset):
            object.__setattr__(
                self,
                'propagation_conditions',
                frozenset(self.propagation_conditions)
            )

        if self.known_limitations and not isinstance(self.known_limitations, frozenset):
            object.__setattr__(
                self,
                'known_limitations',
                frozenset(self.known_limitations)
            )

    @property
    def is_sensory_effect(self) -> bool:
        """Check if this effect is detectable by senses."""
        return self.effect_type == EffectType.SENSORY

    @property
    def is_causal_effect(self) -> bool:
        """Check if this effect represents causal influence."""
        return self.effect_type == EffectType.CAUSAL

    @property
    def is_physical_source(self) -> bool:
        """Check if source has physical reality status."""
        return self.source_status == RealityStatus.PHYSICAL

    @property
    def is_hypothetical_source(self) -> bool:
        """Check if source has hypothetical reality status."""
        return self.source_status == RealityStatus.HYPOTHETICAL

    @property
    def requires_validation(self) -> bool:
        """
        Check if this effect requires validation.

        CRITICAL LAW: Hypothetical sources always require validation.
        """
        return self.is_hypothetical_source

    def equals_reality(self) -> bool:
        """
        Does this effect equal the reality that produced it?

        CRITICAL LAW: NO. RealityEffect ≠ Reality.
        Effects are manifestations, not the underlying reality.
        """
        return False

    def can_certify_source(self) -> bool:
        """
        Can this effect certify its source?

        CRITICAL LAW: NO. Effects are evidence, not certification.
        """
        return False

    def __str__(self) -> str:
        return (
            f"RealityEffect("
            f"type={self.effect_type.name}, "
            f"source={self.source_description[:30]}..., "
            f"status={self.source_status.name})"
        )
