"""
Prior Information Gate - بوابة المعلومات السابقة

Admits or blocks prior information based on evidence, domain, source, and testability.

Critical Laws:
1. Prior information requires domain + source_trace + (evidence OR testability)
2. Prior opinion is blocked from entering as evidence
3. Missing domain/source → rank lowered or blocked
4. Returns governed failures, not exceptions
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Tuple, List, Any

from .prior_information_candidate import PriorInformationCandidate, PriorContentType
from .prior_opinion_candidate import PriorOpinionCandidate, OpinionType
from .residuals import (
    PriorInformationResidual,
    make_prior_missing_domain_residual,
    make_prior_missing_source_residual,
    make_prior_missing_evidence_residual,
    make_prior_opinion_contamination_residual,
)


class PriorInformationFailureKind(Enum):
    """
    Failure kinds for PriorInformationGate.

    MISSING_DOMAIN: Prior information without domain
    MISSING_SOURCE: Prior information without source trace
    MISSING_EVIDENCE: Prior information without evidence or testability
    OPINION_CONTAMINATION: Prior opinion detected
    INVALID_CONTENT_TYPE: Content type is not valid for prior information
    LOW_RANK: Rank insufficient for admission
    """

    MISSING_DOMAIN = auto()
    MISSING_SOURCE = auto()
    MISSING_EVIDENCE = auto()
    OPINION_CONTAMINATION = auto()
    INVALID_CONTENT_TYPE = auto()
    LOW_RANK = auto()


@dataclass(frozen=True)
class PriorInformationGateFailure:
    """
    Governed failure for PriorInformationGate.

    NOT an exception - a typed failure with residuals.
    """

    kind: PriorInformationFailureKind
    message: str
    blocker_residuals: Tuple[PriorInformationResidual, ...]
    evidence_gap: Optional[str] = None

    def __str__(self) -> str:
        return f"PriorInformationGateFailure({self.kind.name}): {self.message}"


@dataclass(frozen=True)
class PriorInformationGateResult:
    """
    Result of PriorInformationGate admission/blocking.

    Properties:
    - status: ADMITTED | BLOCKED
    - candidate: PriorInformationCandidate if admitted
    - rank: PredicateRank (CANDIDATE | LICENSED | CERTIFIED)
    - residuals: Accumulated residuals
    - failure: Failure if blocked
    - trace: Trace ID
    """

    status: str  # ADMITTED | BLOCKED
    candidate: Optional[PriorInformationCandidate] = None
    rank: str = "CANDIDATE"
    residuals: Tuple[PriorInformationResidual, ...] = field(default_factory=tuple)
    failure: Optional[PriorInformationGateFailure] = None
    trace: Optional[str] = None

    def __post_init__(self):
        """Ensure immutability."""
        if isinstance(self.residuals, list):
            object.__setattr__(self, "residuals", tuple(self.residuals))

    def is_admitted(self) -> bool:
        """Check if prior information was admitted."""
        return self.status == "ADMITTED"

    def is_blocked(self) -> bool:
        """Check if prior information was blocked."""
        return self.status == "BLOCKED"

    def has_blocker_residuals(self) -> bool:
        """Check if there are blocker-level residuals."""
        return any(r.is_blocker() for r in self.residuals)


class PriorInformationGate:
    """
    بوابة المعلومات السابقة - Prior Information Gate

    Critical Laws:
    1. Prior information requires domain + source + evidence (or testability)
    2. Prior opinion is blocked
    3. Missing domain → blocker residual
    4. Missing source → blocker residual
    5. Missing evidence AND testability → high residual
    6. Residuals instead of exceptions

    What This Gate Does:
    - Admits or blocks PriorInformationCandidate
    - Validates domain, source, evidence, testability
    - Preserves trace
    - Accumulates residuals
    - Returns governed failures

    What This Gate Does NOT Do:
    - Does NOT create external meaning
    - Does NOT create HUKM
    - Does NOT raise rank prematurely
    - Does NOT skip evidence requirements
    """

    def admit_prior_information(
        self,
        content: Any,
        domain: Optional[str] = None,
        content_type: Optional[PriorContentType] = None,
        source_trace: Optional[str] = None,
        evidence: Optional[str] = None,
        testability: Optional[str] = None,
    ) -> PriorInformationGateResult:
        """
        Admit or block prior information based on requirements.

        Critical Laws:
        - domain required → BLOCKER if missing
        - source_trace required → BLOCKER if missing
        - evidence OR testability required → HIGH residual if both missing

        Returns:
            PriorInformationGateResult with ADMITTED/BLOCKED status
        """
        residuals: List[PriorInformationResidual] = []

        # Check domain
        if not domain:
            residuals.append(make_prior_missing_domain_residual(str(content)))
            return PriorInformationGateResult(
                status="BLOCKED",
                candidate=None,
                rank="BLOCKED",
                residuals=tuple(residuals),
                failure=PriorInformationGateFailure(
                    kind=PriorInformationFailureKind.MISSING_DOMAIN,
                    message=f"Prior information requires domain: {str(content)[:50]}",
                    blocker_residuals=tuple(residuals),
                    evidence_gap="domain",
                ),
            )

        # Check source_trace
        if not source_trace:
            residuals.append(make_prior_missing_source_residual(str(content)))
            return PriorInformationGateResult(
                status="BLOCKED",
                candidate=None,
                rank="BLOCKED",
                residuals=tuple(residuals),
                failure=PriorInformationGateFailure(
                    kind=PriorInformationFailureKind.MISSING_SOURCE,
                    message=f"Prior information requires source trace: {str(content)[:50]}",
                    blocker_residuals=tuple(residuals),
                    evidence_gap="source_trace",
                ),
            )

        # Check evidence OR testability
        if not evidence and not testability:
            residuals.append(make_prior_missing_evidence_residual(str(content)))
            # This lowers rank but doesn't block entirely
            rank = "CANDIDATE"
        else:
            # Has evidence or testability
            if evidence and testability:
                rank = "LICENSED"  # Both present
            else:
                rank = "CANDIDATE"  # One present

        # Create candidate
        candidate = PriorInformationCandidate(
            domain=domain,
            content=content,
            content_type=content_type or PriorContentType.RULE,
            source_trace=source_trace,
            evidence=evidence,
            testability=testability,
            rank=rank,
            residuals=tuple(r.message for r in residuals),
            contamination_risk=0.0,
        )

        return PriorInformationGateResult(
            status="ADMITTED",
            candidate=candidate,
            rank=rank,
            residuals=tuple(residuals),
            failure=None,
            trace=candidate.trace_id,
        )

    def filter_prior_opinion(
        self,
        content: str,
        opinion_type: OpinionType,
    ) -> PriorInformationGateResult:
        """
        Block prior opinion from entering as prior information.

        Critical Law:
            Prior opinion CANNOT become prior information.

        Returns:
            BLOCKED result with opinion contamination residual
        """
        opinion = PriorOpinionCandidate(
            content=content,
            opinion_type=opinion_type,
            contamination_risk=1.0,
        )

        residual = make_prior_opinion_contamination_residual(
            opinion_type=opinion_type.name,
            contamination_risk=1.0,
        )

        return PriorInformationGateResult(
            status="BLOCKED",
            candidate=None,
            rank="BLOCKED",
            residuals=(residual,),
            failure=PriorInformationGateFailure(
                kind=PriorInformationFailureKind.OPINION_CONTAMINATION,
                message=f"Prior opinion blocked: {opinion.why_excluded()}",
                blocker_residuals=(residual,),
                evidence_gap="opinion_instead_of_information",
            ),
        )
