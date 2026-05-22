"""
WorldContext - Physical/Material World Context

Context for the physical/material world in which organisms exist.

Critical laws:
- World is physical reality
- World has structure (space, objects, forces)
- World has laws (physical laws, constraints)
- World context is part of WorldReality domain
- World is independent of observer (exists regardless)
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, FrozenSet
from uuid import UUID, uuid4


class WorldType(Enum):
    """Types of world contexts."""
    NATURAL = auto()         # Natural environment
    BUILT = auto()           # Built/constructed environment
    LABORATORY = auto()      # Controlled laboratory
    VIRTUAL = auto()         # Virtual/simulated world
    HYBRID = auto()          # Hybrid (natural + built)


@dataclass(frozen=True)
class WorldContext:
    """
    Context for the physical/material world.

    This represents the physical world in which observations occur.

    CRITICAL: WorldContext is in WorldReality domain.
    """

    # World type
    world_type: WorldType

    # Spatial structure
    spatial_structure: str  # Description of space/location

    # Physical constraints
    physical_constraints: FrozenSet[str]

    # Physical laws/regularities
    physical_laws: FrozenSet[str]

    # Fields with defaults (must come last)
    context_id: UUID = field(default_factory=uuid4)
    context_description: Optional[str] = None
    accessible_regions: Optional[FrozenSet[str]] = None
    known_hazards: Optional[FrozenSet[str]] = None
    temperature_range: Optional[str] = None
    pressure_range: Optional[str] = None

    def __post_init__(self):
        # Validate spatial_structure
        if not self.spatial_structure or not self.spatial_structure.strip():
            raise ValueError("spatial_structure cannot be empty")

        # Validate physical constraints
        if not self.physical_constraints:
            raise ValueError("physical_constraints cannot be empty")

        # Validate physical laws
        if not self.physical_laws:
            raise ValueError("physical_laws cannot be empty")

        # Convert sets to frozensets for immutability
        if not isinstance(self.physical_constraints, frozenset):
            object.__setattr__(
                self,
                'physical_constraints',
                frozenset(self.physical_constraints)
            )

        if not isinstance(self.physical_laws, frozenset):
            object.__setattr__(
                self,
                'physical_laws',
                frozenset(self.physical_laws)
            )

        if self.accessible_regions and not isinstance(self.accessible_regions, frozenset):
            object.__setattr__(
                self,
                'accessible_regions',
                frozenset(self.accessible_regions)
            )

        if self.known_hazards and not isinstance(self.known_hazards, frozenset):
            object.__setattr__(
                self,
                'known_hazards',
                frozenset(self.known_hazards)
            )

    @property
    def is_natural_world(self) -> bool:
        """Check if this is a natural world context."""
        return self.world_type == WorldType.NATURAL

    @property
    def is_built_world(self) -> bool:
        """Check if this is a built/constructed world."""
        return self.world_type == WorldType.BUILT

    @property
    def is_controlled_environment(self) -> bool:
        """Check if this is a controlled environment (laboratory)."""
        return self.world_type == WorldType.LABORATORY

    @property
    def is_virtual_world(self) -> bool:
        """Check if this is a virtual/simulated world."""
        return self.world_type == WorldType.VIRTUAL

    @property
    def has_hazards(self) -> bool:
        """Check if this world context has known hazards."""
        return bool(self.known_hazards)

    @property
    def is_observer_independent(self) -> bool:
        """
        Does this world exist independently of observer?

        CRITICAL LAW: Physical world is observer-independent.
        Virtual world may depend on implementation.
        """
        return self.world_type != WorldType.VIRTUAL

    def __str__(self) -> str:
        return (
            f"WorldContext("
            f"type={self.world_type.name}, "
            f"structure={self.spatial_structure[:30]}...)"
        )
