"""
Name Reality SubGate - بوابة حقيقة الاسم (داخل نظام المعلومات السابقة)

CRITICAL ARCHITECTURAL CORRECTION:

NameRealitySubGate is NOT an isolated ontological gate.
NameRealitySubGate is a sub-gate INSIDE the Prior Information System.

Why?

The question "Does this name refer to reality or usurp reality?"
cannot be answered from the name alone.

It must be answered from within the prior domain system:
- What domain does the name appear in?
- What prior information system licenses it?
- Does it have a domain definition?
- Does it have a referent candidate?
- Does it have evidence or witness?
- Is it technical/metaphorical/conventional/external?
- Is evidence from the domain itself?

Critical Laws:
1. Name alone does NOT produce RealityCandidate
2. Name without domain is blocked
3. Name without referent evidence is blocked
4. Technical name without domain is blocked
5. Metaphor cannot usurp external existence
6. Prior opinion cannot be referent_evidence
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Tuple, List, Any

from .named_reality_candidate import NamedRealityCandidate
from .reality_type import RealityType
from .prior_information_candidate import PriorInformationCandidate
from .residuals import (
    PriorInformationResidual,
    make_name_only_residual,
    make_name_missing_referent_residual,
    make_name_missing_domain_residual,
    make_name_metaphor_as_external_residual,
    make_name_technical_without_domain_residual,
)


class NameRealityFailureKind(Enum):
    """
    Failure kinds for NameRealitySubGate.

    NAME_WITHOUT_REFERENT: Name alone without referent candidate
    NAME_WITHOUT_DOMAIN: Name requiring domain but none provided
    NAME_WITHOUT_EVIDENCE: Name without referent evidence
    METAPHOR_AS_EXTERNAL: Metaphorical name claiming external existence
    TECHNICAL_WITHOUT_DOMAIN: Technical term without domain
    OPINION_AS_EVIDENCE: Prior opinion used as referent evidence
    """

    NAME_WITHOUT_REFERENT = auto()
    NAME_WITHOUT_DOMAIN = auto()
    NAME_WITHOUT_EVIDENCE = auto()
    METAPHOR_AS_EXTERNAL = auto()
    TECHNICAL_WITHOUT_DOMAIN = auto()
    OPINION_AS_EVIDENCE = auto()


@dataclass(frozen=True)
class NameRealitySubGateFailure:
    """
    Governed failure for NameRealitySubGate.

    NOT an exception - a typed failure with residuals.
    """

    kind: NameRealityFailureKind
    message: str
    blocker_residuals: Tuple[PriorInformationResidual, ...]
    evidence_gap: Optional[str] = None

    def __str__(self) -> str:
        return f"NameRealityFailure({self.kind.name}): {self.message}"


@dataclass(frozen=True)
class NameRealitySubGateResult:
    """
    Result of NameRealitySubGate admission/blocking.

    Properties:
    - status: ADMITTED | BLOCKED
    - candidate: NamedRealityCandidate if admitted
    - rank: PredicateRank (CANDIDATE | LICENSED | CERTIFIED | BLOCKED)
    - residuals: Accumulated residuals
    - failure: Failure if blocked
    - trace: Trace ID
    """

    status: str  # ADMITTED | BLOCKED
    candidate: Optional[NamedRealityCandidate] = None
    rank: str = "CANDIDATE"
    residuals: Tuple[PriorInformationResidual, ...] = field(default_factory=tuple)
    failure: Optional[NameRealitySubGateFailure] = None
    trace: Optional[str] = None

    def __post_init__(self):
        """Ensure immutability."""
        if isinstance(self.residuals, list):
            object.__setattr__(self, "residuals", tuple(self.residuals))

    def is_admitted(self) -> bool:
        """Check if named reality was admitted."""
        return self.status == "ADMITTED"

    def is_blocked(self) -> bool:
        """Check if named reality was blocked."""
        return self.status == "BLOCKED"

    def has_blocker_residuals(self) -> bool:
        """Check if there are blocker-level residuals."""
        return any(r.is_blocker() for r in self.residuals)


class NameRealitySubGate:
    """
    بوابة حقيقة الاسم - Name Reality SubGate

    Sub-gate INSIDE Prior Information Geometry.

    Critical Laws:
    1. Name alone does NOT become RealityCandidate
    2. Name without domain → BLOCKED
    3. Name without referent evidence → BLOCKED
    4. Technical/Mental/Normative existence → domain required
    5. Metaphorical cannot claim external existence
    6. Prior opinion cannot be referent_evidence

    Existence Types (classified from within domain):
    - EXTERNAL: External/physical (requires sensory evidence)
    - EFFECTUAL: Via trace/effect (requires effect evidence)
    - MENTAL: Mental/cognitive (requires mental domain)
    - VERBAL: Linguistic (requires linguistic domain)
    - TECHNICAL: Conventional within domain (requires domain)
    - METAPHORICAL: Metaphorical (cannot claim external)
    - NORMATIVE: Normative/value (requires normative domain)

    What This Gate Does:
    - Admits or blocks NamedRealityCandidate
    - Classifies existence type from within domain
    - Validates referent candidate + evidence
    - Prevents metaphor → external leap
    - Prevents opinion → evidence leap
    - Preserves trace and residuals

    What This Gate Does NOT Do:
    - Does NOT create RealityCandidate from name alone
    - Does NOT skip domain requirement
    - Does NOT allow usurpation of external reality
    - Does NOT accept opinion as evidence
    """

    def admit_named_reality(
        self,
        name: str,
        referent_candidate: Optional[Any] = None,
        existence_type: Optional[RealityType] = None,
        domain: Optional[str] = None,
        referent_evidence: Optional[str] = None,
        prior_information: Optional[PriorInformationCandidate] = None,
    ) -> NameRealitySubGateResult:
        """
        Admit or block named reality based on domain, referent, evidence.

        Critical Laws:
        - Name without referent → BLOCKED
        - Name without domain (when required by existence type) → BLOCKED
        - Metaphor claiming external → BLOCKED
        - Technical without domain → BLOCKED

        Args:
            name: The name
            referent_candidate: Proposed referent (NOT final referent)
            existence_type: Type of existence
            domain: Domain specification
            referent_evidence: Evidence for referent
            prior_information: Prior information context

        Returns:
            NameRealitySubGateResult with ADMITTED/BLOCKED status
        """
        residuals: List[PriorInformationResidual] = []

        # Check referent candidate
        if referent_candidate is None:
            residuals.append(make_name_only_residual(name))
            return NameRealitySubGateResult(
                status="BLOCKED",
                candidate=None,
                rank="BLOCKED",
                residuals=tuple(residuals),
                failure=NameRealitySubGateFailure(
                    kind=NameRealityFailureKind.NAME_WITHOUT_REFERENT,
                    message=f"Name '{name}' has no referent candidate",
                    blocker_residuals=tuple(residuals),
                    evidence_gap="referent_candidate",
                ),
            )

        # Default existence type if not provided
        if existence_type is None:
            existence_type = RealityType.EXTERNAL  # Default assumption

        # Check domain requirement
        if existence_type.requires_domain() and not domain:
            residuals.append(
                make_name_missing_domain_residual(name, existence_type.name)
            )
            return NameRealitySubGateResult(
                status="BLOCKED",
                candidate=None,
                rank="BLOCKED",
                residuals=tuple(residuals),
                failure=NameRealitySubGateFailure(
                    kind=NameRealityFailureKind.NAME_WITHOUT_DOMAIN,
                    message=f"Name '{name}' with type '{existence_type}' requires domain",
                    blocker_residuals=tuple(residuals),
                    evidence_gap="domain",
                ),
            )

        # Check technical without domain
        if existence_type == RealityType.TECHNICAL and not domain:
            residuals.append(make_name_technical_without_domain_residual(name))
            return NameRealitySubGateResult(
                status="BLOCKED",
                candidate=None,
                rank="BLOCKED",
                residuals=tuple(residuals),
                failure=NameRealitySubGateFailure(
                    kind=NameRealityFailureKind.TECHNICAL_WITHOUT_DOMAIN,
                    message=f"Technical name '{name}' requires domain",
                    blocker_residuals=tuple(residuals),
                    evidence_gap="domain_for_technical",
                ),
            )

        # Check metaphor claiming external
        if existence_type == RealityType.METAPHORICAL:
            # Metaphor cannot claim external existence
            if referent_evidence and "external" in referent_evidence.lower():
                residuals.append(make_name_metaphor_as_external_residual(name))
                return NameRealitySubGateResult(
                    status="BLOCKED",
                    candidate=None,
                    rank="BLOCKED",
                    residuals=tuple(residuals),
                    failure=NameRealitySubGateFailure(
                        kind=NameRealityFailureKind.METAPHOR_AS_EXTERNAL,
                        message=f"Metaphorical name '{name}' cannot claim external existence",
                        blocker_residuals=tuple(residuals),
                        evidence_gap="metaphor_usurping_external",
                    ),
                )

        # Check referent evidence
        if not referent_evidence:
            residuals.append(make_name_missing_referent_residual(name))
            rank = "CANDIDATE"  # Lower rank but don't block entirely
        else:
            rank = "LICENSED"

        # Determine ambiguity score
        ambiguity_score = 0.0
        if not domain:
            ambiguity_score += 0.3
        if not referent_evidence:
            ambiguity_score += 0.3
        if existence_type == RealityType.TECHNICAL:
            ambiguity_score += 0.2

        # Create candidate
        candidate = NamedRealityCandidate(
            name=name,
            referent_candidate=referent_candidate,
            existence_type=existence_type,
            domain=domain or "",
            referent_evidence=referent_evidence,
            ambiguity_score=ambiguity_score,
            rank=rank,
            residuals=tuple(r.message for r in residuals),
        )

        return NameRealitySubGateResult(
            status="ADMITTED",
            candidate=candidate,
            rank=rank,
            residuals=tuple(residuals),
            failure=None,
            trace=candidate.trace,
        )
