"""
Domain Candidate - مرشح المجال

A domain defines the primitives, rules, and boundaries for reality admissions.

Critical Laws:
1. No reality admission without domain specification
2. Domain transfers require explicit license
3. Forbidden transfers are blocked (not residualized)
"""

from dataclasses import dataclass, field
from typing import FrozenSet, Optional, List, Tuple
from uuid import uuid4


@dataclass(frozen=True)
class DomainCandidate:
    """
    Domain Candidate - مرشح المجال

    Defines the scope within which prior information, reality types,
    and names operate.

    Critical Properties:
    - domain: Domain identifier (linguistic/empirical/mental/social/legal...)
    - primitives: Foundational elements of this domain
    - rules: Domain-specific inference rules
    - allowed_transfers: Domains to which transfer is licensed
    - forbidden_transfers: Domains to which transfer is explicitly blocked
    - rank: PredicateRank indicating confidence in domain boundaries
    - residuals: Uncertainties about domain specification
    - trace: Source of domain definition
    """

    domain: str
    primitives: FrozenSet[str] = field(default_factory=frozenset)
    rules: FrozenSet[str] = field(default_factory=frozenset)
    allowed_transfers: FrozenSet[str] = field(default_factory=frozenset)
    forbidden_transfers: FrozenSet[str] = field(default_factory=frozenset)
    rank: str = "CANDIDATE"  # CANDIDATE | LICENSED | CERTIFIED
    residuals: Tuple[str, ...] = field(default_factory=tuple)
    trace: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        """Ensure immutability by converting mutable collections."""
        # Convert sets to frozensets
        if not isinstance(self.primitives, frozenset):
            object.__setattr__(self, "primitives", frozenset(self.primitives))
        if not isinstance(self.rules, frozenset):
            object.__setattr__(self, "rules", frozenset(self.rules))
        if not isinstance(self.allowed_transfers, frozenset):
            object.__setattr__(self, "allowed_transfers", frozenset(self.allowed_transfers))
        if not isinstance(self.forbidden_transfers, frozenset):
            object.__setattr__(self, "forbidden_transfers", frozenset(self.forbidden_transfers))

        # Convert lists to tuples
        if isinstance(self.residuals, list):
            object.__setattr__(self, "residuals", tuple(self.residuals))

    def can_transfer_to(self, target_domain: str) -> bool:
        """Check if transfer to target domain is allowed."""
        if target_domain in self.forbidden_transfers:
            return False
        if self.allowed_transfers and target_domain not in self.allowed_transfers:
            return False
        return True

    def is_well_defined(self) -> bool:
        """Check if domain is sufficiently defined."""
        return bool(self.domain) and (bool(self.primitives) or bool(self.rules))

    def __str__(self) -> str:
        return f"DomainCandidate(domain={self.domain}, rank={self.rank})"


def make_linguistic_domain() -> DomainCandidate:
    """Create a linguistic domain candidate."""
    return DomainCandidate(
        domain="linguistic",
        primitives=frozenset(["phoneme", "morpheme", "word", "sentence"]),
        rules=frozenset(["grammar", "syntax", "morphology"]),
        allowed_transfers=frozenset(["semantic", "pragmatic"]),
        forbidden_transfers=frozenset(["empirical", "ontological"]),
        rank="CERTIFIED",
        residuals=(),
        trace="linguistic_domain_specification",
    )


def make_empirical_domain() -> DomainCandidate:
    """Create an empirical domain candidate."""
    return DomainCandidate(
        domain="empirical",
        primitives=frozenset(["observation", "measurement", "experiment"]),
        rules=frozenset(["causation", "correlation", "falsifiability"]),
        allowed_transfers=frozenset(["physical", "biological"]),
        forbidden_transfers=frozenset(["linguistic", "grammatical"]),
        rank="CERTIFIED",
        residuals=(),
        trace="empirical_domain_specification",
    )


def make_mental_domain() -> DomainCandidate:
    """Create a mental/cognitive domain candidate."""
    return DomainCandidate(
        domain="mental",
        primitives=frozenset(["concept", "thought", "intention", "belief"]),
        rules=frozenset(["inference", "association", "reasoning"]),
        allowed_transfers=frozenset(["linguistic", "social"]),
        forbidden_transfers=frozenset(["external", "physical"]),
        rank="LICENSED",
        residuals=("mental_domain_boundaries_debated",),
        trace="mental_domain_specification",
    )
