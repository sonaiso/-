"""
RealityBridge - Mode Transfer Validation

RealityBridge validates transitions between reality domains and status levels.

Critical laws:
- Physical → Biological requires living substrate
- Biological → Social requires multiple organisms
- Social → Conceptual requires symbolic capacity
- Conceptual → Symbolic requires representation system
- Symbolic → Hypothetical requires theoretical framework
- Hypothetical → Physical requires experimental validation (bridge)

Bridge types:
- EMBODIMENT: Physical ↔ Biological (through body)
- SOCIAL_FORMATION: Biological ↔ Social (through interaction)
- ABSTRACTION: Social/Biological ↔ Conceptual (through categorization)
- SYMBOLIZATION: Conceptual ↔ Symbolic (through representation)
- THEORIZATION: Symbolic ↔ Hypothetical (through theory)
- EXPERIMENTAL: Hypothetical ↔ Physical (through experiment)
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, FrozenSet

from .reality_status import RealityStatus
from .reality_domain import RealityDomain


class BridgeType(Enum):
    """Types of reality bridges."""
    EMBODIMENT = auto()         # Physical ↔ Biological
    SOCIAL_FORMATION = auto()   # Biological ↔ Social
    ABSTRACTION = auto()        # Physical/Social ↔ Conceptual
    SYMBOLIZATION = auto()      # Conceptual ↔ Symbolic
    THEORIZATION = auto()       # Symbolic ↔ Hypothetical
    EXPERIMENTAL = auto()       # Hypothetical ↔ Physical


class BridgeValidation(Enum):
    """Validation status for bridge crossing."""
    VALID = auto()              # Bridge crossing is valid
    INVALID = auto()            # Bridge crossing is invalid
    REQUIRES_CONDITIONS = auto() # Bridge crossing requires additional conditions
    FORBIDDEN = auto()          # Bridge crossing is forbidden


@dataclass(frozen=True)
class RealityBridge:
    """
    Validator for reality status and domain transitions.

    This ensures that transitions between reality levels are valid
    and enforces bridge requirements.

    CRITICAL: No hypothetical → physical without experimental validation.
    """

    source_status: RealityStatus
    target_status: RealityStatus
    bridge_type: BridgeType
    required_conditions: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        # Convert sets to frozensets for immutability
        if self.required_conditions and not isinstance(self.required_conditions, frozenset):
            object.__setattr__(
                self,
                'required_conditions',
                frozenset(self.required_conditions)
            )

        # Validate bridge type matches status transition
        self._validate_bridge_type()

    def _validate_bridge_type(self):
        """Validate that bridge type is appropriate for status transition."""
        # EMBODIMENT: Physical ↔ Biological
        if self.bridge_type == BridgeType.EMBODIMENT:
            if not (
                (self.source_status == RealityStatus.PHYSICAL and
                 self.target_status == RealityStatus.BIOLOGICAL) or
                (self.source_status == RealityStatus.BIOLOGICAL and
                 self.target_status == RealityStatus.PHYSICAL)
            ):
                raise ValueError(
                    f"EMBODIMENT bridge requires Physical ↔ Biological transition, "
                    f"got {self.source_status.name} → {self.target_status.name}"
                )

        # SOCIAL_FORMATION: Biological ↔ Social
        elif self.bridge_type == BridgeType.SOCIAL_FORMATION:
            if not (
                (self.source_status == RealityStatus.BIOLOGICAL and
                 self.target_status == RealityStatus.SOCIAL) or
                (self.source_status == RealityStatus.SOCIAL and
                 self.target_status == RealityStatus.BIOLOGICAL)
            ):
                raise ValueError(
                    f"SOCIAL_FORMATION bridge requires Biological ↔ Social transition, "
                    f"got {self.source_status.name} → {self.target_status.name}"
                )

        # EXPERIMENTAL: Hypothetical ↔ Physical
        elif self.bridge_type == BridgeType.EXPERIMENTAL:
            if not (
                (self.source_status == RealityStatus.HYPOTHETICAL and
                 self.target_status == RealityStatus.PHYSICAL) or
                (self.source_status == RealityStatus.PHYSICAL and
                 self.target_status == RealityStatus.HYPOTHETICAL)
            ):
                raise ValueError(
                    f"EXPERIMENTAL bridge requires Hypothetical ↔ Physical transition, "
                    f"got {self.source_status.name} → {self.target_status.name}"
                )

    def validate_crossing(self) -> BridgeValidation:
        """
        Validate whether this bridge crossing is valid.

        Returns BridgeValidation status.
        """
        # Hypothetical → Physical REQUIRES experimental bridge
        if (self.source_status == RealityStatus.HYPOTHETICAL and
            self.target_status == RealityStatus.PHYSICAL):
            if self.bridge_type != BridgeType.EXPERIMENTAL:
                return BridgeValidation.FORBIDDEN
            return BridgeValidation.REQUIRES_CONDITIONS

        # Physical → Hypothetical is always valid (theorization)
        if (self.source_status == RealityStatus.PHYSICAL and
            self.target_status == RealityStatus.HYPOTHETICAL):
            return BridgeValidation.VALID

        # Same status → no bridge needed
        if self.source_status == self.target_status:
            return BridgeValidation.VALID

        # Foundational → Emergent requires conditions
        if (self.source_status.is_foundational() and
            self.target_status.is_emergent()):
            return BridgeValidation.REQUIRES_CONDITIONS

        # Emergent → Foundational requires grounding
        if (self.source_status.is_emergent() and
            self.target_status.is_foundational()):
            return BridgeValidation.REQUIRES_CONDITIONS

        # Adjacent levels are generally valid
        if self.source_status.can_promote_to(self.target_status):
            return BridgeValidation.VALID

        # Default: requires conditions
        return BridgeValidation.REQUIRES_CONDITIONS

    @property
    def is_experimental_bridge(self) -> bool:
        """Check if this is an experimental bridge (hypothetical → physical)."""
        return self.bridge_type == BridgeType.EXPERIMENTAL

    @property
    def requires_validation(self) -> bool:
        """Check if this bridge crossing requires validation."""
        return self.validate_crossing() in {
            BridgeValidation.REQUIRES_CONDITIONS,
            BridgeValidation.FORBIDDEN
        }

    @property
    def is_forbidden(self) -> bool:
        """Check if this bridge crossing is forbidden."""
        return self.validate_crossing() == BridgeValidation.FORBIDDEN

    def __str__(self) -> str:
        return (
            f"RealityBridge("
            f"{self.source_status.name} → {self.target_status.name}, "
            f"type={self.bridge_type.name})"
        )
