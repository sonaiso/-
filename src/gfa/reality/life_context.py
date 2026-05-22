"""
LifeContext - Living Processes and Organism Context

Context for living organisms and life processes.

Critical laws:
- Life is biological reality
- Life requires physical substrate
- Life has phases (birth, growth, maturity, decline, death)
- Life has needs and constraints
- Life context is part of LifeReality domain
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, FrozenSet
from uuid import UUID, uuid4


class LifePhase(Enum):
    """Phases of life process."""
    GENESIS = auto()         # Origin/birth
    GROWTH = auto()          # Growth phase
    MATURITY = auto()        # Mature phase
    REPRODUCTION = auto()    # Reproductive phase
    DECLINE = auto()         # Decline phase
    TERMINATION = auto()     # Death/termination


@dataclass(frozen=True)
class LifeContext:
    """
    Context for living organisms and life processes.

    This represents the biological context in which an embodied observer exists.

    CRITICAL: LifeContext is in LifeReality domain.
    """

    # Life phase
    life_phase: LifePhase

    # Organism type (species, category)
    organism_type: str

    # Biological requirements
    biological_requirements: FrozenSet[str]

    # Life constraints
    life_constraints: FrozenSet[str]

    # Fields with defaults (must come last)
    context_id: UUID = field(default_factory=uuid4)
    context_description: Optional[str] = None
    environmental_dependencies: Optional[FrozenSet[str]] = None
    reproductive_capability: bool = False

    def __post_init__(self):
        # Validate organism_type
        if not self.organism_type or not self.organism_type.strip():
            raise ValueError("organism_type cannot be empty")

        # Validate biological requirements
        if not self.biological_requirements:
            raise ValueError("biological_requirements cannot be empty")

        # Validate life constraints
        if not self.life_constraints:
            raise ValueError("life_constraints cannot be empty")

        # Convert sets to frozensets for immutability
        if not isinstance(self.biological_requirements, frozenset):
            object.__setattr__(
                self,
                'biological_requirements',
                frozenset(self.biological_requirements)
            )

        if not isinstance(self.life_constraints, frozenset):
            object.__setattr__(
                self,
                'life_constraints',
                frozenset(self.life_constraints)
            )

        if self.environmental_dependencies and not isinstance(self.environmental_dependencies, frozenset):
            object.__setattr__(
                self,
                'environmental_dependencies',
                frozenset(self.environmental_dependencies)
            )

    @property
    def is_alive(self) -> bool:
        """Check if this life context represents living organism."""
        return self.life_phase != LifePhase.TERMINATION

    @property
    def is_growing(self) -> bool:
        """Check if in growth phase."""
        return self.life_phase == LifePhase.GROWTH

    @property
    def is_mature(self) -> bool:
        """Check if in mature phase."""
        return self.life_phase == LifePhase.MATURITY

    @property
    def can_reproduce(self) -> bool:
        """Check if reproduction is possible."""
        return (
            self.reproductive_capability and
            self.life_phase in {LifePhase.MATURITY, LifePhase.REPRODUCTION}
        )

    @property
    def is_declining(self) -> bool:
        """Check if in decline phase."""
        return self.life_phase == LifePhase.DECLINE

    @property
    def is_terminated(self) -> bool:
        """Check if life is terminated."""
        return self.life_phase == LifePhase.TERMINATION

    def __str__(self) -> str:
        return (
            f"LifeContext("
            f"phase={self.life_phase.name}, "
            f"organism={self.organism_type})"
        )
