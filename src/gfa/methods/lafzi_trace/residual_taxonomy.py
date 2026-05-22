"""
Residual Taxonomy for LafziTrace Gate

Residuals represent failures in the LafziTrace gate process.
These are governed failures, not bare exceptions.

Critical Law:
    كل فشل محكوم، لا استثناء عاري
    Every failure is governed, not a bare exception.

Trace Failure Kinds:
    - MISSING_REGISTRATION: LafziMadlul registration not found
    - MISSING_STYLE_SPEC: StyleSpec not provided
    - WRONG_DOMAIN: Domain is not LAFZI_DALALI
    - MISSING_NEUTRAL_BINDING: NeutralBinding not provided
    - MISSING_PRIOR_INFORMATION: PriorInformation not provided
    - TRACE_NOT_PRESERVED: trace_id missing
    - UNKNOWN_TRACE_TYPE: Trace type is UNKNOWN (becomes residual)
    - MEANING_CREATION_ATTEMPTED: LafziTrace tried to create meaning (forbidden)
    - HUKM_ISSUANCE_ATTEMPTED: LafziTrace tried to issue HUKM (forbidden)
    - DAL_IMPLEMENTATION_ATTEMPTED: LafziTrace tried to implement Dal (forbidden)
    - MADLUL_IMPLEMENTATION_ATTEMPTED: LafziTrace tried to implement Madlul (forbidden)
    - DALALAH_IMPLEMENTATION_ATTEMPTED: LafziTrace tried to implement Dalalah (forbidden)
    - RANK_INFLATION_ATTEMPTED: LafziTrace tried to raise PredicateRank (forbidden)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LafziTraceFailureKind(Enum):
    """
    Types of failures in LafziTrace gate.

    Each failure kind represents a specific governance law violation.
    """

    # Registration violations
    MISSING_REGISTRATION = "missing_registration"

    # StyleSpec violations
    MISSING_STYLE_SPEC = "missing_style_spec"
    WRONG_DOMAIN = "wrong_domain"

    # NeutralBinding violations
    MISSING_NEUTRAL_BINDING = "missing_neutral_binding"

    # Prior violations
    MISSING_PRIOR_INFORMATION = "missing_prior_information"

    # Trace violations
    TRACE_NOT_PRESERVED = "trace_not_preserved"
    UNKNOWN_TRACE_TYPE = "unknown_trace_type"

    # Forbidden operations (must NOT happen)
    MEANING_CREATION_ATTEMPTED = "meaning_creation_attempted"
    HUKM_ISSUANCE_ATTEMPTED = "hukm_issuance_attempted"
    DAL_IMPLEMENTATION_ATTEMPTED = "dal_implementation_attempted"
    MADLUL_IMPLEMENTATION_ATTEMPTED = "madlul_implementation_attempted"
    DALALAH_IMPLEMENTATION_ATTEMPTED = "dalalah_implementation_attempted"
    RANK_INFLATION_ATTEMPTED = "rank_inflation_attempted"


@dataclass(frozen=True)
class LafziTraceResidual:
    """
    Residual from LafziTrace gate failure.

    A residual is a governed failure object.
    It preserves:
        - failure kind
        - reason (explanation)
        - trace_id (lineage)
        - violated_law (which governance law was broken)

    Never a bare exception.
    """

    kind: LafziTraceFailureKind
    reason: str
    violated_law: str
    trace_id: Optional[str] = None

    def __str__(self) -> str:
        return (
            f"LafziTraceResidual[{self.kind.value}]: {self.reason} "
            f"(violated: {self.violated_law})"
        )

    def __repr__(self) -> str:
        return (
            f"LafziTraceResidual("
            f"kind={self.kind.value}, "
            f"violated_law='{self.violated_law}')"
        )


# Factory functions for creating specific residuals

def make_missing_registration_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for missing LafziMadlul registration."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.MISSING_REGISTRATION,
        reason="LafziMadlul registration is required before LafziTrace",
        violated_law="Law 1: No LafziTrace without LafziMadlul registration",
        trace_id=trace_id,
    )


def make_missing_style_spec_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for missing StyleSpec."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.MISSING_STYLE_SPEC,
        reason="StyleSpec is required for LafziTrace",
        violated_law="Law 2: No LafziTrace without StyleSpec(LAFZI_DALALI)",
        trace_id=trace_id,
    )


def make_wrong_domain_residual(
    actual_domain: str,
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for wrong domain."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.WRONG_DOMAIN,
        reason=f"Domain must be LAFZI_DALALI, got {actual_domain}",
        violated_law="Law 2: No LafziTrace without StyleSpec(LAFZI_DALALI)",
        trace_id=trace_id,
    )


def make_missing_neutral_binding_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for missing NeutralBinding."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.MISSING_NEUTRAL_BINDING,
        reason="NeutralBinding is required for LafziTrace",
        violated_law="Law 3: No LafziTrace without NeutralBinding",
        trace_id=trace_id,
    )


def make_missing_prior_information_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for missing PriorInformation."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.MISSING_PRIOR_INFORMATION,
        reason="PriorInformation is required for LafziTrace",
        violated_law="Law 4: No LafziTrace without PriorInformation",
        trace_id=trace_id,
    )


def make_trace_not_preserved_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for missing trace_id."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.TRACE_NOT_PRESERVED,
        reason="trace_id must be preserved in LafziTrace",
        violated_law="Law 5: LafziTrace preserves trace_id",
        trace_id=trace_id,
    )


def make_unknown_trace_type_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for UNKNOWN trace type."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.UNKNOWN_TRACE_TYPE,
        reason="Trace type is UNKNOWN (becomes residual for future resolution)",
        violated_law="Law 6: UNKNOWN trace type becomes residual, not exception",
        trace_id=trace_id,
    )


def make_meaning_creation_attempted_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for forbidden meaning creation."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.MEANING_CREATION_ATTEMPTED,
        reason="LafziTrace must not create meaning",
        violated_law="Law 7: LafziTrace does not create meaning",
        trace_id=trace_id,
    )


def make_hukm_issuance_attempted_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for forbidden HUKM issuance."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.HUKM_ISSUANCE_ATTEMPTED,
        reason="LafziTrace must not issue HUKM",
        violated_law="Law 8: LafziTrace does not issue HUKM",
        trace_id=trace_id,
    )


def make_dal_implementation_attempted_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for forbidden Dal implementation."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.DAL_IMPLEMENTATION_ATTEMPTED,
        reason="LafziTrace must not implement Dal",
        violated_law="Law 9: LafziTrace does not create Dal",
        trace_id=trace_id,
    )


def make_madlul_implementation_attempted_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for forbidden Madlul implementation."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.MADLUL_IMPLEMENTATION_ATTEMPTED,
        reason="LafziTrace must not implement Madlul",
        violated_law="Law 10: LafziTrace does not create Madlul",
        trace_id=trace_id,
    )


def make_dalalah_implementation_attempted_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for forbidden Dalalah implementation."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.DALALAH_IMPLEMENTATION_ATTEMPTED,
        reason="LafziTrace must not implement Dalalah",
        violated_law="Law 11: LafziTrace does not create Dalalah",
        trace_id=trace_id,
    )


def make_rank_inflation_attempted_residual(
    trace_id: Optional[str] = None
) -> LafziTraceResidual:
    """Create residual for forbidden rank inflation."""
    return LafziTraceResidual(
        kind=LafziTraceFailureKind.RANK_INFLATION_ATTEMPTED,
        reason="LafziTrace must not raise PredicateRank",
        violated_law="Law 12: LafziTrace does not raise PredicateRank",
        trace_id=trace_id,
    )
