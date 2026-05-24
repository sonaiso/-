"""
Prior Information Candidate - مرشح المعلومة السابقة

Valid prior information that can guide interpretation.

Critical Laws:
1. Prior information requires domain + source + evidence (or testability)
2. Prior opinion is excluded
3. Missing domain/source → rank lowered or blocked
4. Returns residuals instead of exceptions
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Tuple, Any
from uuid import uuid4


class PriorContentType(Enum):
    """
    Type of prior information content.

    RULE: Grammatical, logical, or domain-specific rule
    DEFINITION: Lexical or technical definition
    WITNESS: Textual or empirical witness
    REGISTRY_ENTRY: Entry from authoritative registry
    CLASSIFICATION: Taxonomic or categorical classification
    EXCEPTION: Documented exception to general rule
    SOURCE: Source attribution or citation
    """

    RULE = auto()
    DEFINITION = auto()
    WITNESS = auto()
    REGISTRY_ENTRY = auto()
    CLASSIFICATION = auto()
    EXCEPTION = auto()
    SOURCE = auto()


@dataclass(frozen=True)
class PriorInformationCandidate:
    """
    مرشح المعلومة السابقة - Prior Information Candidate

    Valid prior information that can be used for interpretation.

    Critical Properties:
    - domain: Domain in which this information applies
    - content: The actual information content
    - content_type: Type of content (RULE/DEFINITION/WITNESS/...)
    - source_trace: Where this information comes from
    - evidence: Supporting evidence (optional but affects rank)
    - testability: Whether this information is testable
    - rank: PredicateRank (CANDIDATE/LICENSED/CERTIFIED)
    - residuals: Uncertainties about this information
    - contamination_risk: Risk of opinion contamination

    Critical Laws:
    - Requires domain
    - Requires source_trace
    - Requires evidence OR testability
    - No opinion content allowed
    """

    domain: str
    content: Any
    content_type: PriorContentType
    source_trace: str
    evidence: Optional[str] = None
    testability: Optional[str] = None
    rank: str = "CANDIDATE"  # CANDIDATE | LICENSED | CERTIFIED
    residuals: Tuple[str, ...] = field(default_factory=tuple)
    contamination_risk: float = 0.0
    trace_id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        """Ensure immutability."""
        if isinstance(self.residuals, list):
            object.__setattr__(self, "residuals", tuple(self.residuals))

    def is_valid(self) -> bool:
        """Check if this prior information is valid."""
        has_domain = bool(self.domain)
        has_source = bool(self.source_trace)
        has_support = bool(self.evidence) or bool(self.testability)
        return has_domain and has_source and has_support

    def is_admissible(self) -> bool:
        """Check if this information can be admitted."""
        return self.is_valid() and self.contamination_risk < 0.5

    def get_admission_residuals(self) -> Tuple[str, ...]:
        """Get residuals that would prevent full admission."""
        res = list(self.residuals)

        if not self.domain:
            res.append("R-PRIOR-MISSING-DOMAIN")
        if not self.source_trace:
            res.append("R-PRIOR-MISSING-SOURCE")
        if not self.evidence and not self.testability:
            res.append("R-PRIOR-MISSING-EVIDENCE")
        if self.contamination_risk > 0.0:
            res.append(f"R-PRIOR-OPINION-CONTAMINATION:{self.contamination_risk:.2f}")

        return tuple(res)

    def __str__(self) -> str:
        return f"PriorInformation(domain={self.domain}, type={self.content_type.name}, rank={self.rank})"
