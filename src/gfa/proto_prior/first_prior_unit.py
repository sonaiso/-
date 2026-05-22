"""
FirstPriorUnit - The Minimal Sufficient Unit for All Prior Geometry

This is the foundational unit from which all knowledge systems emerge:
- Physics
- Mathematics
- Logic
- Language

FirstPriorUnit is NOT:
- A rule
- A concept/meaning
- A word
- A law
- A judgment

FirstPriorUnit IS:
- A distinguished existential trace
- Anchored in time, place, and reference
- Bounded and retainable
- Comparable and primitively bindable
- Carrying residuals and rank
- Sufficient for entering PriorGeometry
- Insufficient for producing rules/meanings/judgments

This is the minimal sufficient unit - nothing less will work,
nothing more is needed at this foundational level.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional, Set, FrozenSet
from uuid import UUID, uuid4

from .existence_type import ExistenceType, Domain, Channel
from .time_anchor import TimeAnchor
from .place_anchor import PlaceAnchor
from .reference_anchor import ReferenceAnchor
from .distinction import Distinction
from .boundary import Boundary
from .retention import RetentionState
from .comparability import ComparabilityState
from .primitive_bindability import PrimitiveBindability


class Rank(Enum):
    """
    Epistemic rank of a unit or result.

    Critical law: FirstPriorUnit typically starts at CANDIDATE or OBSERVED.
    It CANNOT be CERTIFIED based on hypothetical/textual existence alone.
    """
    CANDIDATE = auto()      # Candidate/proposed
    OBSERVED = auto()       # Directly observed
    CORROBORATED = auto()   # Corroborated by multiple observations
    LICENSED = auto()       # Licensed by binding conditions
    CERTIFIED = auto()      # Fully certified with audit

    def can_promote_to(self, target: "Rank") -> bool:
        """Check if promotion to target rank is valid."""
        rank_order = {
            Rank.CANDIDATE: 0,
            Rank.OBSERVED: 1,
            Rank.CORROBORATED: 2,
            Rank.LICENSED: 3,
            Rank.CERTIFIED: 4
        }
        return rank_order.get(self, 0) < rank_order.get(target, 0)


@dataclass(frozen=True)
class Residual:
    """
    A residual - something unresolved, incomplete, or uncertain.

    Residuals are MANDATORY to preserve - they prevent hallucination.
    """
    description: str
    residual_type: str  # e.g., "uncertainty", "incompleteness", "ambiguity"
    severity: Optional[str] = None  # e.g., "minor", "major", "critical"

    def __post_init__(self):
        if not self.description or not self.description.strip():
            raise ValueError("Residual description cannot be empty")
        if not self.residual_type or not self.residual_type.strip():
            raise ValueError("Residual type cannot be empty")


@dataclass(frozen=True)
class FirstPriorUnit:
    """
    The Minimal Sufficient Unit for First Prior Geometry.

    This is the foundation from which all future knowledge emerges.

    MANDATORY fields (14 total):
    1. entity_or_effect: What exists
    2. existence_type: Mode of existence
    3. domain: Realm/field
    4. distinction: How it's distinguished from background
    5. boundary: Extent/limits
    6. time_anchor: Temporal anchoring
    7. place_anchor: Spatial/domain anchoring
    8. reference_anchor: What/who it refers to
    9. channel: Access pathway
    10. trace_id: Unique trace identifier
    11. retention_state: Retention capability
    12. comparability_state: Comparison capability
    13. primitive_bindability: Binding capability
    14. residuals: Unresolved aspects

    Plus: rank (epistemic status)

    Critical laws enforced:
    - All 14 fields are mandatory
    - Hypothetical existence cannot be CERTIFIED
    - Textual/symbolic/acoustic existence cannot imply physical without bridge
    - FirstPriorUnit CANNOT produce rules/meanings/judgments/certificates
    """

    # Core identity
    entity_or_effect: Any
    existence_type: ExistenceType
    domain: Domain

    # Fundamental properties
    distinction: Distinction
    boundary: Boundary

    # Anchoring (MANDATORY)
    time_anchor: TimeAnchor
    place_anchor: PlaceAnchor
    reference_anchor: ReferenceAnchor

    # Access
    channel: Channel

    # Trace identity
    trace_id: UUID = field(default_factory=uuid4)

    # Capabilities (MANDATORY)
    retention_state: RetentionState
    comparability_state: ComparabilityState
    primitive_bindability: PrimitiveBindability

    # Epistemic status
    residuals: FrozenSet[Residual] = field(default_factory=frozenset)
    rank: Rank = Rank.CANDIDATE

    def __post_init__(self):
        # Validate all mandatory fields are present and valid
        self._validate_mandatory_fields()

        # Enforce rank constraints based on existence type
        self._validate_rank_constraints()

        # Convert residuals to frozenset if needed
        if self.residuals and not isinstance(self.residuals, frozenset):
            object.__setattr__(self, 'residuals', frozenset(self.residuals))

    def _validate_mandatory_fields(self):
        """Validate all mandatory fields are present."""
        # Check entity_or_effect
        if self.entity_or_effect is None:
            raise ValueError("entity_or_effect is mandatory")

        # Check existence_type
        if not isinstance(self.existence_type, ExistenceType):
            raise ValueError("existence_type must be ExistenceType enum")

        # Check domain
        if not isinstance(self.domain, Domain):
            raise ValueError("domain is mandatory")

        # Check distinction
        if not isinstance(self.distinction, Distinction):
            raise ValueError("distinction is mandatory")
        if not self.distinction.is_valid:
            raise ValueError("distinction must be valid")

        # Check boundary
        if not isinstance(self.boundary, Boundary):
            raise ValueError("boundary is mandatory")
        if not self.boundary.is_valid:
            raise ValueError("boundary must be valid")

        # Check time_anchor
        if not isinstance(self.time_anchor, TimeAnchor):
            raise ValueError("time_anchor is mandatory")
        if not self.time_anchor.is_valid:
            raise ValueError("time_anchor must be valid")

        # Check place_anchor
        if not isinstance(self.place_anchor, PlaceAnchor):
            raise ValueError("place_anchor is mandatory")
        if not self.place_anchor.is_valid:
            raise ValueError("place_anchor must be valid")

        # Check reference_anchor
        if not isinstance(self.reference_anchor, ReferenceAnchor):
            raise ValueError("reference_anchor is mandatory")
        if not self.reference_anchor.is_valid:
            raise ValueError("reference_anchor must be valid")

        # Check channel
        if not isinstance(self.channel, Channel):
            raise ValueError("channel is mandatory")

        # Check retention_state
        if not isinstance(self.retention_state, RetentionState):
            raise ValueError("retention_state is mandatory")
        if not self.retention_state.is_retainable:
            raise ValueError("retention_state must allow retention")

        # Check comparability_state
        if not isinstance(self.comparability_state, ComparabilityState):
            raise ValueError("comparability_state is mandatory")
        if not self.comparability_state.is_comparable:
            raise ValueError("comparability_state must allow comparison")

        # Check primitive_bindability
        if not isinstance(self.primitive_bindability, PrimitiveBindability):
            raise ValueError("primitive_bindability is mandatory")
        if not self.primitive_bindability.is_bindable:
            raise ValueError("primitive_bindability must allow binding")

    def _validate_rank_constraints(self):
        """Validate rank constraints based on existence type."""
        # Hypothetical existence cannot be CERTIFIED
        if self.existence_type == ExistenceType.HYPOTHETICAL:
            if self.rank == Rank.CERTIFIED:
                raise ValueError(
                    "Hypothetical existence cannot have CERTIFIED rank. "
                    "Hypothetical units can be CANDIDATE or OBSERVED at most."
                )

        # Linguistic/textual existence alone cannot be CERTIFIED for physical claims
        if self.existence_type == ExistenceType.LINGUISTIC:
            if self.rank == Rank.CERTIFIED and "physical" in str(self.entity_or_effect).lower():
                raise ValueError(
                    "Linguistic/textual existence cannot certify physical existence without bridge."
                )

    @property
    def is_valid(self) -> bool:
        """Check if this FirstPriorUnit is fully valid."""
        try:
            self._validate_mandatory_fields()
            self._validate_rank_constraints()
            return True
        except ValueError:
            return False

    @property
    def has_residuals(self) -> bool:
        """Check if this unit has unresolved residuals."""
        return bool(self.residuals)

    @property
    def residual_count(self) -> int:
        """Return number of residuals."""
        return len(self.residuals)

    def can_produce_rule(self) -> bool:
        """
        Can this FirstPriorUnit produce a rule?

        CRITICAL LAW: NO. FirstPriorUnit cannot produce rules.
        Rules emerge later from PriorGeometry and learning.
        """
        return False

    def can_produce_meaning(self) -> bool:
        """
        Can this FirstPriorUnit produce meaning?

        CRITICAL LAW: NO. FirstPriorUnit cannot produce meaning.
        Meaning emerges later from binding and learning.
        """
        return False

    def can_issue_judgment(self) -> bool:
        """
        Can this FirstPriorUnit issue judgment?

        CRITICAL LAW: NO. FirstPriorUnit cannot issue judgment.
        Judgment requires learned binding conditions and CPB.
        """
        return False

    def can_certify(self) -> bool:
        """
        Can this FirstPriorUnit certify results?

        CRITICAL LAW: NO. FirstPriorUnit cannot certify.
        Certification requires full audit and evidence.
        """
        return False

    def __str__(self) -> str:
        return (
            f"FirstPriorUnit("
            f"type={self.existence_type.name}, "
            f"ref={self.reference_anchor.primary_reference}, "
            f"rank={self.rank.name}, "
            f"residuals={self.residual_count})"
        )
