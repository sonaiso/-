"""
Named Reality Candidate - مرشح الواقع المسمى

A name bound to a referent candidate with existence type and domain.

Critical Laws:
1. Name alone does not produce reality
2. Referent candidate required
3. Domain required for technical/mental/normative existence
4. Evidence required for admission
5. Ambiguity tracked via residuals
"""

from dataclasses import dataclass, field
from typing import Optional, Any, Tuple
from uuid import uuid4

from .reality_type import RealityType


@dataclass(frozen=True)
class NamedRealityCandidate:
    """
    مرشح الواقع المسمى - Named Reality Candidate

    A name associated with a referent candidate, existence type, and domain.

    Critical Properties:
    - name: The linguistic name
    - referent_candidate: Proposed referent (NOT final referent)
    - existence_type: Type of existence (EXTERNAL/MENTAL/TECHNICAL/...)
    - domain: Domain in which this referent exists
    - referent_evidence: Evidence for referent
    - ambiguity_score: Ambiguity measure [0.0, 1.0]
    - rank: PredicateRank
    - residuals: Uncertainties and gaps
    - trace: Source trace

    Critical Laws:
    - Name without referent → BLOCKED
    - Technical/Mental/Normative without domain → BLOCKED
    - Metaphorical claiming EXTERNAL → BLOCKED
    - Prior opinion as evidence → BLOCKED
    """

    name: str
    referent_candidate: Any
    existence_type: RealityType
    domain: str
    referent_evidence: Optional[str] = None
    ambiguity_score: float = 0.0
    rank: str = "CANDIDATE"  # CANDIDATE | LICENSED | CERTIFIED | BLOCKED
    residuals: Tuple[str, ...] = field(default_factory=tuple)
    trace: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        """Ensure immutability."""
        if isinstance(self.residuals, list):
            object.__setattr__(self, "residuals", tuple(self.residuals))

    def is_admissible(self) -> bool:
        """Check if this named reality can be admitted."""
        has_name = bool(self.name)
        has_referent = self.referent_candidate is not None
        has_domain = bool(self.domain)

        # Technical/Mental/Normative require domain
        if self.existence_type.requires_domain() and not has_domain:
            return False

        # Name + referent required
        if not has_name or not has_referent:
            return False

        # Metaphorical cannot claim external
        if (self.existence_type == RealityType.METAPHORICAL and
            self.existence_type.allows_external_leap()):
            return False

        return True

    def get_blocking_residuals(self) -> Tuple[str, ...]:
        """Get residuals that would block admission."""
        res = []

        if not self.name:
            res.append("R-NAME-MISSING")

        if self.referent_candidate is None:
            res.append("R-NAME-MISSING-REFERENT")

        if self.existence_type.requires_domain() and not self.domain:
            res.append("R-NAME-MISSING-DOMAIN")

        if self.existence_type == RealityType.TECHNICAL and not self.domain:
            res.append("R-NAME-TECHNICAL-WITHOUT-DOMAIN")

        if self.existence_type == RealityType.METAPHORICAL:
            # Check if trying to claim external existence
            if "external" in str(self.referent_evidence).lower():
                res.append("R-NAME-METAPHOR-AS-EXTERNAL")

        if self.ambiguity_score > 0.5:
            res.append(f"R-NAME-HIGH-AMBIGUITY:{self.ambiguity_score:.2f}")

        return tuple(res)

    def has_blocking_residuals(self) -> bool:
        """Check if there are any blocking residuals."""
        return len(self.get_blocking_residuals()) > 0

    def __str__(self) -> str:
        return f"NamedReality(name={self.name}, type={self.existence_type}, domain={self.domain}, rank={self.rank})"
