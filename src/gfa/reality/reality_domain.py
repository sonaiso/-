"""
Reality Domain - Four Primary Domains of Reality

The four fundamental domains where reality manifests:
1. SelfReality: The embodied self (body, sensation, pain, need, action)
2. LifeReality: Living processes, growth, death, reproduction
3. WorldReality: Physical/material world, space, objects, forces
4. RelationalReality: Relations between entities, social structures, interactions

Critical laws:
- Observer is part of SelfReality, not external
- SelfReality is primary - it is the precondition for accessing other domains
- Domains are not isolated - they interconnect
- Domain transitions require validation
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, FrozenSet


class DomainType(Enum):
    """Four primary reality domains."""
    SELF = auto()          # Embodied self (body, sensation, need)
    LIFE = auto()          # Living processes and organisms
    WORLD = auto()          # Physical/material world
    RELATIONAL = auto()    # Relations and interactions


@dataclass(frozen=True)
class RealityDomain:
    """
    A reality domain with boundaries and access conditions.

    Critical laws:
    - SelfReality is primary (precondition for accessing others)
    - Domain transitions must be validated
    - Domains can interconnect but remain distinct
    """

    domain_type: DomainType
    domain_description: Optional[str] = None
    access_conditions: Optional[FrozenSet[str]] = None
    known_boundaries: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        # Convert sets to frozensets for immutability
        if self.access_conditions and not isinstance(self.access_conditions, frozenset):
            object.__setattr__(
                self,
                'access_conditions',
                frozenset(self.access_conditions)
            )

        if self.known_boundaries and not isinstance(self.known_boundaries, frozenset):
            object.__setattr__(
                self,
                'known_boundaries',
                frozenset(self.known_boundaries)
            )

    @property
    def is_self_reality(self) -> bool:
        """Check if this is SelfReality domain."""
        return self.domain_type == DomainType.SELF

    @property
    def is_primary_domain(self) -> bool:
        """Check if this is a primary domain (SelfReality)."""
        return self.is_self_reality

    @property
    def requires_embodiment(self) -> bool:
        """Check if this domain requires embodied access."""
        # SelfReality IS embodiment
        # LifeReality requires embodied organism
        # WorldReality can be accessed through embodiment
        # RelationalReality requires embodied participants
        return self.domain_type in {DomainType.SELF, DomainType.LIFE}

    def can_transition_to(self, target: "RealityDomain") -> bool:
        """
        Check if transition to target domain is possible.

        Critical law: All domains accessible from SelfReality.
        """
        if self.domain_type == DomainType.SELF:
            return True  # SelfReality can access all domains

        if target.domain_type == DomainType.SELF:
            return True  # All domains connect back to SelfReality

        # Other transitions require validation
        return True  # Permissive by default, but validation required

    def __str__(self) -> str:
        return f"RealityDomain({self.domain_type.name})"
