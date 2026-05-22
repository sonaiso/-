"""
Residual Taxonomy for LafziMadlul Registration

Residuals represent failures in the governance registration process.
These are governed failures, not bare exceptions.

Critical Law:
    كل فشل محكوم، لا استثناء عاري
    Every failure is governed, not a bare exception.

Registration Failure Kinds:
    - MISSING_STYLE_SPEC: StyleSpec not provided
    - WRONG_DOMAIN: Domain is not LAFZI_DALALI
    - MATERIAL_DOMAIN_REJECTED: MATERIAL_EXPERIMENTAL not allowed
    - FORMAL_DOMAIN_REJECTED: FORMAL_LOGICAL not allowed
    - MISSING_NEUTRAL_BINDING: NeutralBinding not provided
    - MISSING_PRIOR_INFORMATION: PriorInformation not provided
    - PRIOR_OPINION_PRESENT: PriorOpinion found (excluded)
    - TRACE_NOT_PRESERVED: trace_id missing
    - RESIDUALS_NOT_PRESERVED: residuals not maintained
    - RANK_INFLATED: PredicateRank incorrectly raised
    - GOVERNANCE_VIOLATION: General governance rule violated
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class LafziRegistrationFailureKind(Enum):
    """
    Types of failures in LafziMadlul registration.

    Each failure kind represents a specific governance law violation.
    """

    # StyleSpec violations
    MISSING_STYLE_SPEC = "missing_style_spec"
    WRONG_DOMAIN = "wrong_domain"
    MATERIAL_DOMAIN_REJECTED = "material_domain_rejected"
    FORMAL_DOMAIN_REJECTED = "formal_domain_rejected"

    # NeutralBinding violations
    MISSING_NEUTRAL_BINDING = "missing_neutral_binding"

    # Prior violations
    MISSING_PRIOR_INFORMATION = "missing_prior_information"
    PRIOR_OPINION_PRESENT = "prior_opinion_present"

    # Trace/Residual violations
    TRACE_NOT_PRESERVED = "trace_not_preserved"
    RESIDUALS_NOT_PRESERVED = "residuals_not_preserved"

    # Rank violations
    RANK_INFLATED = "rank_inflated"

    # General governance
    GOVERNANCE_VIOLATION = "governance_violation"


@dataclass(frozen=True)
class LafziRegistrationResidual:
    """
    Residual from LafziMadlul registration failure.

    A residual is a governed failure object.
    It preserves:
        - failure kind
        - reason (explanation)
        - trace_id (lineage)
        - violated_law (which governance law was broken)

    Never a bare exception.
    """

    kind: LafziRegistrationFailureKind
    reason: str
    violated_law: str
    trace_id: Optional[str] = None
    domain_attempted: Optional[str] = None

    def __str__(self) -> str:
        return (
            f"LafziRegistrationResidual[{self.kind.value}]: {self.reason} "
            f"(violated: {self.violated_law})"
        )

    def __repr__(self) -> str:
        return (
            f"LafziRegistrationResidual("
            f"kind={self.kind.value}, "
            f"violated_law='{self.violated_law}')"
        )


# Factory functions for creating specific residuals

def make_missing_style_spec_residual(trace_id: Optional[str] = None) -> LafziRegistrationResidual:
    """Create residual for missing StyleSpec."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.MISSING_STYLE_SPEC,
        reason="StyleSpec is required for LafziMadlul registration",
        violated_law="Law 1: No LafziMadlul without StyleSpec",
        trace_id=trace_id,
    )


def make_wrong_domain_residual(
    actual_domain: str,
    trace_id: Optional[str] = None
) -> LafziRegistrationResidual:
    """Create residual for wrong domain."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.WRONG_DOMAIN,
        reason=f"Domain must be LAFZI_DALALI, got {actual_domain}",
        violated_law="Law 2: No LafziMadlul unless domain = LAFZI_DALALI",
        trace_id=trace_id,
        domain_attempted=actual_domain,
    )


def make_material_domain_rejected_residual(
    trace_id: Optional[str] = None
) -> LafziRegistrationResidual:
    """Create residual for MATERIAL_EXPERIMENTAL domain rejection."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.MATERIAL_DOMAIN_REJECTED,
        reason="MATERIAL_EXPERIMENTAL domain not allowed for LafziMadlul",
        violated_law="Law 3: No LafziMadlul with MATERIAL_EXPERIMENTAL domain",
        trace_id=trace_id,
        domain_attempted="MATERIAL_EXPERIMENTAL",
    )


def make_formal_domain_rejected_residual(
    trace_id: Optional[str] = None
) -> LafziRegistrationResidual:
    """Create residual for FORMAL_LOGICAL domain rejection."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.FORMAL_DOMAIN_REJECTED,
        reason="FORMAL_LOGICAL domain not allowed for LafziMadlul",
        violated_law="Law 4: No LafziMadlul with FORMAL_LOGICAL domain",
        trace_id=trace_id,
        domain_attempted="FORMAL_LOGICAL",
    )


def make_missing_neutral_binding_residual(
    trace_id: Optional[str] = None
) -> LafziRegistrationResidual:
    """Create residual for missing NeutralBinding."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.MISSING_NEUTRAL_BINDING,
        reason="NeutralBinding is required for LafziMadlul registration",
        violated_law="Law 5: No LafziMadlul without NeutralBinding",
        trace_id=trace_id,
    )


def make_missing_prior_information_residual(
    trace_id: Optional[str] = None
) -> LafziRegistrationResidual:
    """Create residual for missing PriorInformation."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.MISSING_PRIOR_INFORMATION,
        reason="PriorInformation is required for LafziMadlul registration",
        violated_law="Law 6: No LafziMadlul without PriorInformation",
        trace_id=trace_id,
    )


def make_prior_opinion_present_residual(
    trace_id: Optional[str] = None
) -> LafziRegistrationResidual:
    """Create residual for PriorOpinion presence."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.PRIOR_OPINION_PRESENT,
        reason="PriorOpinion is excluded from LafziMadlul registration",
        violated_law="Law 7: No LafziMadlul with PriorOpinion",
        trace_id=trace_id,
    )


def make_trace_not_preserved_residual(
    trace_id: Optional[str] = None
) -> LafziRegistrationResidual:
    """Create residual for missing trace."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.TRACE_NOT_PRESERVED,
        reason="trace_id must be preserved in LafziMadlul registration",
        violated_law="Law 8: LafziMadlul registration preserves trace",
        trace_id=trace_id,
    )


def make_residuals_not_preserved_residual(
    trace_id: Optional[str] = None
) -> LafziRegistrationResidual:
    """Create residual for missing residuals."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.RESIDUALS_NOT_PRESERVED,
        reason="Residuals must be preserved in LafziMadlul registration",
        violated_law="Law 9: LafziMadlul registration preserves residuals",
        trace_id=trace_id,
    )


def make_rank_inflated_residual(
    trace_id: Optional[str] = None
) -> LafziRegistrationResidual:
    """Create residual for rank inflation."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.RANK_INFLATED,
        reason="LafziMadlul registration must not raise PredicateRank",
        violated_law="Law 10: LafziMadlul registration preserves rank",
        trace_id=trace_id,
    )


def make_governance_violation_residual(
    reason: str,
    violated_law: str,
    trace_id: Optional[str] = None
) -> LafziRegistrationResidual:
    """Create general governance violation residual."""
    return LafziRegistrationResidual(
        kind=LafziRegistrationFailureKind.GOVERNANCE_VIOLATION,
        reason=reason,
        violated_law=violated_law,
        trace_id=trace_id,
    )
