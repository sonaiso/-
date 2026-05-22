"""
MinimalRealityUnit - The Foundational Reality Unit

This is Layer -2: The absolute ground layer.

MinimalRealityUnit represents:
- The minimal reality ground that precedes all traces
- The precondition for sensory transfer
- The foundation for all knowledge

Critical laws:
- Reality is NOT produced by the system
- Reality precedes all traces
- Reality cannot be CERTIFIED by the system (reality precedes certification)
- Reality is the ground for resistance to hallucination
- Observer is part of reality (in SelfReality domain)

MinimalRealityUnit has 15 mandatory fields:
1. reality_domain: Which domain (Self, Life, World, Relational)
2. reality_status: Status level (Physical, Biological, Social, etc.)
3. entity_or_process: What exists or occurs
4. embodied_observer: The observer (part of reality)
5. life_context: Living organism context
6. world_context: Physical world context
7. time_marker: When (but not full TimeAnchor - that's in FirstPriorUnit)
8. place_marker: Where (but not full PlaceAnchor - that's in FirstPriorUnit)
9. reality_effects: What effects reality produces
10. physical_constraints: Physical limitations
11. biological_constraints: Biological limitations
12. existence_conditions: Conditions for existence
13. known_boundaries: Reality boundaries
14. reality_trace_id: Unique reality identifier
15. reality_residuals: What is unresolved about reality
"""

from dataclasses import dataclass, field
from typing import Any, Optional, FrozenSet
from uuid import UUID, uuid4

from .reality_domain import RealityDomain
from .reality_status import RealityStatus
from .reality_effect import RealityEffect
from .embodied_observer import EmbodiedObserver
from .life_context import LifeContext
from .world_context import WorldContext


@dataclass(frozen=True)
class RealityResidual:
    """
    A residual about reality itself.

    This represents what is unresolved, uncertain, or incomplete
    about reality - NOT about our knowledge of it.
    """
    description: str
    residual_type: str  # e.g., "boundary_uncertainty", "constraint_unknown"
    severity: Optional[str] = None

    def __post_init__(self):
        if not self.description or not self.description.strip():
            raise ValueError("Residual description cannot be empty")
        if not self.residual_type or not self.residual_type.strip():
            raise ValueError("Residual type cannot be empty")


@dataclass(frozen=True)
class MinimalRealityUnit:
    """
    The Minimal Reality Unit - Layer -2 (absolute ground).

    This is the foundational layer that precedes all traces and knowledge.

    MANDATORY fields (15 total):
    1-3: Domain, Status, Entity
    4-6: Observer, Life, World contexts
    7-8: Time, Place markers
    9-13: Effects, Constraints, Conditions, Boundaries
    14-15: Trace ID, Residuals

    Critical laws enforced:
    - All 15 fields are mandatory
    - Reality is NOT produced by system
    - Reality cannot be CERTIFIED (reality precedes certification)
    - Observer is part of reality (embodied)
    - Reality is the ground for resistance to hallucination
    """

    # Core identity (no defaults)
    reality_domain: RealityDomain
    reality_status: RealityStatus
    entity_or_process: Any

    # Contexts - MANDATORY (no defaults)
    embodied_observer: EmbodiedObserver
    life_context: LifeContext
    world_context: WorldContext

    # Markers (no defaults) - simplified from full Anchors
    time_marker: str  # When (simplified - full TimeAnchor in FirstPriorUnit)
    place_marker: str  # Where (simplified - full PlaceAnchor in FirstPriorUnit)

    # Reality effects and constraints (no defaults)
    reality_effects: FrozenSet[RealityEffect]
    physical_constraints: FrozenSet[str]
    biological_constraints: FrozenSet[str]
    existence_conditions: FrozenSet[str]
    known_boundaries: FrozenSet[str]

    # Fields with defaults (must come last)
    reality_trace_id: UUID = field(default_factory=uuid4)
    reality_residuals: FrozenSet[RealityResidual] = field(default_factory=frozenset)

    def __post_init__(self):
        # Validate all mandatory fields
        self._validate_mandatory_fields()

        # Convert sets to frozensets for immutability
        if self.reality_effects and not isinstance(self.reality_effects, frozenset):
            object.__setattr__(
                self,
                'reality_effects',
                frozenset(self.reality_effects)
            )

        if self.physical_constraints and not isinstance(self.physical_constraints, frozenset):
            object.__setattr__(
                self,
                'physical_constraints',
                frozenset(self.physical_constraints)
            )

        if self.biological_constraints and not isinstance(self.biological_constraints, frozenset):
            object.__setattr__(
                self,
                'biological_constraints',
                frozenset(self.biological_constraints)
            )

        if self.existence_conditions and not isinstance(self.existence_conditions, frozenset):
            object.__setattr__(
                self,
                'existence_conditions',
                frozenset(self.existence_conditions)
            )

        if self.known_boundaries and not isinstance(self.known_boundaries, frozenset):
            object.__setattr__(
                self,
                'known_boundaries',
                frozenset(self.known_boundaries)
            )

        if self.reality_residuals and not isinstance(self.reality_residuals, frozenset):
            object.__setattr__(
                self,
                'reality_residuals',
                frozenset(self.reality_residuals)
            )

    def _validate_mandatory_fields(self):
        """Validate all mandatory fields are present and valid."""
        # Check entity_or_process
        if self.entity_or_process is None:
            raise ValueError("entity_or_process is mandatory")

        # Check reality_domain
        if not isinstance(self.reality_domain, RealityDomain):
            raise ValueError("reality_domain is mandatory")

        # Check reality_status
        if not isinstance(self.reality_status, RealityStatus):
            raise ValueError("reality_status must be RealityStatus enum")

        # Check embodied_observer
        if not isinstance(self.embodied_observer, EmbodiedObserver):
            raise ValueError("embodied_observer is mandatory")

        # Check life_context
        if not isinstance(self.life_context, LifeContext):
            raise ValueError("life_context is mandatory")

        # Check world_context
        if not isinstance(self.world_context, WorldContext):
            raise ValueError("world_context is mandatory")

        # Check time_marker
        if not self.time_marker or not self.time_marker.strip():
            raise ValueError("time_marker is mandatory")

        # Check place_marker
        if not self.place_marker or not self.place_marker.strip():
            raise ValueError("place_marker is mandatory")

        # Check reality_effects
        if self.reality_effects is None:
            raise ValueError("reality_effects is mandatory")

        # Check physical_constraints
        if not self.physical_constraints:
            raise ValueError("physical_constraints cannot be empty")

        # Check biological_constraints
        if not self.biological_constraints:
            raise ValueError("biological_constraints cannot be empty")

        # Check existence_conditions
        if not self.existence_conditions:
            raise ValueError("existence_conditions cannot be empty")

        # Check known_boundaries
        if not self.known_boundaries:
            raise ValueError("known_boundaries cannot be empty")

    @property
    def is_valid(self) -> bool:
        """Check if this MinimalRealityUnit is fully valid."""
        try:
            self._validate_mandatory_fields()
            return True
        except ValueError:
            return False

    @property
    def has_residuals(self) -> bool:
        """Check if this unit has reality residuals."""
        return bool(self.reality_residuals)

    @property
    def is_physical_reality(self) -> bool:
        """Check if this is physical reality status."""
        return self.reality_status == RealityStatus.PHYSICAL

    @property
    def is_biological_reality(self) -> bool:
        """Check if this is biological reality status."""
        return self.reality_status == RealityStatus.BIOLOGICAL

    @property
    def observer_is_part_of_reality(self) -> bool:
        """
        Is the observer part of reality?

        CRITICAL LAW: YES. Observer is embodied, part of reality.
        """
        return True

    def is_produced_by_system(self) -> bool:
        """
        Is this reality produced by the system?

        CRITICAL LAW: NO. Reality is not produced by the system.
        Reality is the precondition for the system's possibility.
        """
        return False

    def can_be_certified_by_system(self) -> bool:
        """
        Can this reality be certified by the system?

        CRITICAL LAW: NO. Reality precedes certification.
        The system cannot certify reality; reality grounds the system.
        """
        return False

    def precedes_all_traces(self) -> bool:
        """
        Does reality precede all traces?

        CRITICAL LAW: YES. Reality is the ground for all traces.
        """
        return True

    def grounds_resistance_to_hallucination(self) -> bool:
        """
        Does reality ground resistance to hallucination?

        CRITICAL LAW: YES. Reality is what resists hallucination.
        """
        return True

    def __str__(self) -> str:
        return (
            f"MinimalRealityUnit("
            f"domain={self.reality_domain.domain_type.name}, "
            f"status={self.reality_status.name}, "
            f"observer={self.embodied_observer.observer_id}, "
            f"residuals={len(self.reality_residuals)})"
        )
