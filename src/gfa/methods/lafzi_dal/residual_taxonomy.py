"""
Residual Taxonomy for DalGate

Residuals represent failures in the DalGate process.
These are governed failures, not bare exceptions.

Critical Law:
    كل فشل محكوم، لا استثناء عاري
    Every failure is governed, not a bare exception.

Dal Failure Kinds:
    - MISSING_LAFZI_TRACE: LafziTrace not provided
    - MISSING_REGISTRATION: LafziMadlul registration not found
    - MISSING_STYLE_SPEC: StyleSpec not provided
    - WRONG_DOMAIN: Domain is not LAFZI_DALALI
    - MISSING_NEUTRAL_BINDING: NeutralBinding not provided
    - TRACE_NOT_PRESERVED: trace_id missing
    - RESIDUALS_NOT_PRESERVED: Residuals not maintained
    - UNKNOWN_DAL_TYPE: Signifier type is UNKNOWN (becomes residual)
    - MEANING_CREATION_ATTEMPTED: DalCandidate tried to create meaning (forbidden)
    - MADLUL_CREATION_ATTEMPTED: DalCandidate tried to create Madlul (forbidden)
    - DALALAH_CREATION_ATTEMPTED: DalCandidate tried to create Dalalah (forbidden)
    - WADH_IMPLEMENTATION_ATTEMPTED: DalCandidate tried to implement Wadh (forbidden)
    - HUKM_ISSUANCE_ATTEMPTED: DalCandidate tried to issue HUKM (forbidden)
    - RANK_INFLATION_ATTEMPTED: DalCandidate tried to raise PredicateRank (forbidden)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DalFailureKind(Enum):
    """
    Types of failures in DalGate.

    Each failure kind represents a specific governance law violation.
    """

    # Dependency violations
    MISSING_LAFZI_TRACE = "missing_lafzi_trace"
    MISSING_REGISTRATION = "missing_registration"

    # StyleSpec violations
    MISSING_STYLE_SPEC = "missing_style_spec"
    WRONG_DOMAIN = "wrong_domain"

    # NeutralBinding violations
    MISSING_NEUTRAL_BINDING = "missing_neutral_binding"

    # Preservation violations
    TRACE_NOT_PRESERVED = "trace_not_preserved"
    RESIDUALS_NOT_PRESERVED = "residuals_not_preserved"

    # Type violations
    UNKNOWN_DAL_TYPE = "unknown_dal_type"

    # Forbidden operations (must NOT happen)
    MEANING_CREATION_ATTEMPTED = "meaning_creation_attempted"
    MADLUL_CREATION_ATTEMPTED = "madlul_creation_attempted"
    DALALAH_CREATION_ATTEMPTED = "dalalah_creation_attempted"
    WADH_IMPLEMENTATION_ATTEMPTED = "wadh_implementation_attempted"
    HUKM_ISSUANCE_ATTEMPTED = "hukm_issuance_attempted"
    RANK_INFLATION_ATTEMPTED = "rank_inflation_attempted"


@dataclass(frozen=True)
class DalResidual:
    """
    Residual from DalGate failure.

    A residual is a governed failure object.
    It preserves:
        - failure kind
        - reason (explanation)
        - trace_id (lineage)
        - violated_law (which governance law was broken)

    Never a bare exception.
    """

    kind: DalFailureKind
    reason: str
    violated_law: str
    trace_id: Optional[str] = None

    def __str__(self) -> str:
        return (
            f"DalResidual[{self.kind.value}]: {self.reason} "
            f"(violated: {self.violated_law})"
        )

    def __repr__(self) -> str:
        return (
            f"DalResidual("
            f"kind={self.kind.value}, "
            f"violated_law='{self.violated_law}')"
        )


# Factory functions for creating specific residuals

def make_missing_lafzi_trace_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for missing LafziTrace."""
    return DalResidual(
        kind=DalFailureKind.MISSING_LAFZI_TRACE,
        reason="LafziTrace is required before DalCandidate",
        violated_law="Law 1: No DalCandidate without LafziTrace",
        trace_id=trace_id,
    )


def make_missing_registration_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for missing LafziMadlul registration."""
    return DalResidual(
        kind=DalFailureKind.MISSING_REGISTRATION,
        reason="LafziMadlul registration is required before DalCandidate",
        violated_law="Law 2: No DalCandidate without LafziMadlul registration",
        trace_id=trace_id,
    )


def make_missing_style_spec_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for missing StyleSpec."""
    return DalResidual(
        kind=DalFailureKind.MISSING_STYLE_SPEC,
        reason="StyleSpec is required for DalCandidate",
        violated_law="Law 3: No DalCandidate without StyleSpec(LAFZI_DALALI)",
        trace_id=trace_id,
    )


def make_wrong_domain_residual(
    actual_domain: str,
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for wrong domain."""
    return DalResidual(
        kind=DalFailureKind.WRONG_DOMAIN,
        reason=f"Domain must be LAFZI_DALALI, got {actual_domain}",
        violated_law="Law 3: No DalCandidate without StyleSpec(LAFZI_DALALI)",
        trace_id=trace_id,
    )


def make_missing_neutral_binding_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for missing NeutralBinding."""
    return DalResidual(
        kind=DalFailureKind.MISSING_NEUTRAL_BINDING,
        reason="NeutralBinding is required for DalCandidate",
        violated_law="Law 4: No DalCandidate without NeutralBinding",
        trace_id=trace_id,
    )


def make_trace_not_preserved_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for missing trace_id."""
    return DalResidual(
        kind=DalFailureKind.TRACE_NOT_PRESERVED,
        reason="trace_id must be preserved in DalCandidate",
        violated_law="Law 5: DalCandidate preserves trace_id",
        trace_id=trace_id,
    )


def make_residuals_not_preserved_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for lost residuals."""
    return DalResidual(
        kind=DalFailureKind.RESIDUALS_NOT_PRESERVED,
        reason="Residuals must be preserved in DalCandidate",
        violated_law="Law 6: DalCandidate preserves residuals",
        trace_id=trace_id,
    )


def make_unknown_dal_type_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for UNKNOWN signifier type."""
    return DalResidual(
        kind=DalFailureKind.UNKNOWN_DAL_TYPE,
        reason="Signifier type is UNKNOWN (becomes residual for future resolution)",
        violated_law="Law 13: UNKNOWN signifier type becomes residual, not exception",
        trace_id=trace_id,
    )


def make_meaning_creation_attempted_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for forbidden meaning creation."""
    return DalResidual(
        kind=DalFailureKind.MEANING_CREATION_ATTEMPTED,
        reason="DalCandidate must not create meaning",
        violated_law="Law 7: DalCandidate does not create meaning",
        trace_id=trace_id,
    )


def make_madlul_creation_attempted_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for forbidden Madlul creation."""
    return DalResidual(
        kind=DalFailureKind.MADLUL_CREATION_ATTEMPTED,
        reason="DalCandidate must not create Madlul",
        violated_law="Law 8: DalCandidate does not create Madlul",
        trace_id=trace_id,
    )


def make_dalalah_creation_attempted_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for forbidden Dalalah creation."""
    return DalResidual(
        kind=DalFailureKind.DALALAH_CREATION_ATTEMPTED,
        reason="DalCandidate must not create Dalalah",
        violated_law="Law 9: DalCandidate does not create Dalalah",
        trace_id=trace_id,
    )


def make_wadh_implementation_attempted_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for forbidden Wadh implementation."""
    return DalResidual(
        kind=DalFailureKind.WADH_IMPLEMENTATION_ATTEMPTED,
        reason="DalCandidate must not implement Wadh",
        violated_law="Law 10: DalCandidate does not implement Wadh",
        trace_id=trace_id,
    )


def make_hukm_issuance_attempted_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for forbidden HUKM issuance."""
    return DalResidual(
        kind=DalFailureKind.HUKM_ISSUANCE_ATTEMPTED,
        reason="DalCandidate must not issue HUKM",
        violated_law="Law 11: DalCandidate does not issue HUKM",
        trace_id=trace_id,
    )


def make_rank_inflation_attempted_residual(
    trace_id: Optional[str] = None
) -> DalResidual:
    """Create residual for forbidden rank inflation."""
    return DalResidual(
        kind=DalFailureKind.RANK_INFLATION_ATTEMPTED,
        reason="DalCandidate must not raise PredicateRank",
        violated_law="Law 12: DalCandidate does not raise PredicateRank",
        trace_id=trace_id,
    )
