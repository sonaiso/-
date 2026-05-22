"""
Residual Taxonomy for MadlulLafziGate - تصنيف البقايا

Defines residuals (failures) that can occur during MadlulLafzi processing.

Critical Law:
    كل فشل محكوم، لا exception خام
    All failures are governed, not bare exceptions.

Failure Kinds:
    1. MISSING_LAFZI_REGISTRATION: No LafziMadlul registration
    2. WRONG_DOMAIN: Domain is not LAFZI_DALALI
    3. MISSING_NEUTRAL_BINDING: NeutralBinding not available
    4. MISSING_PRIOR_INFORMATION: PriorInformation not available
    5. TRACE_NOT_PRESERVED: trace_id not preserved
    6. RESIDUALS_NOT_PRESERVED: residuals not preserved
    7. UNKNOWN_MADLUL_TYPE: Madlul type is UNKNOWN (becomes residual)
    8. EXTERNAL_MEANING_ATTEMPTED: Attempted external meaning creation
    9. DALALAH_CREATION_ATTEMPTED: Attempted Dalalah creation
    10. WADH_IMPLEMENTATION_ATTEMPTED: Attempted Wadh implementation
    11. HUKM_ISSUANCE_ATTEMPTED: Attempted HUKM issuance
    12. RANK_INFLATION_ATTEMPTED: Attempted PredicateRank inflation
    13. DAL_CANDIDATE_REQUIRED_TOO_EARLY: DalCandidate required prematurely

Critical:
    All residuals are dataclasses, NOT exceptions.
    All residuals preserve trace_id.
    All residuals include violated_law.
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class MadlulLafziFailureKind(Enum):
    """
    Kinds of failures that can occur in MadlulLafzi processing.

    Each failure kind maps to a specific violated governance law.
    """

    MISSING_LAFZI_REGISTRATION = "missing_lafzi_registration"
    WRONG_DOMAIN = "wrong_domain"
    MISSING_NEUTRAL_BINDING = "missing_neutral_binding"
    MISSING_PRIOR_INFORMATION = "missing_prior_information"
    TRACE_NOT_PRESERVED = "trace_not_preserved"
    RESIDUALS_NOT_PRESERVED = "residuals_not_preserved"
    UNKNOWN_MADLUL_TYPE = "unknown_madlul_type"
    EXTERNAL_MEANING_ATTEMPTED = "external_meaning_attempted"
    DALALAH_CREATION_ATTEMPTED = "dalalah_creation_attempted"
    WADH_IMPLEMENTATION_ATTEMPTED = "wadh_implementation_attempted"
    HUKM_ISSUANCE_ATTEMPTED = "hukm_issuance_attempted"
    RANK_INFLATION_ATTEMPTED = "rank_inflation_attempted"
    DAL_CANDIDATE_REQUIRED_TOO_EARLY = "dal_candidate_required_too_early"


@dataclass(frozen=True)
class MadlulLafziResidual:
    """
    Residual from MadlulLafzi processing failure.

    Properties:
        kind: Type of failure
        reason: Human-readable explanation
        violated_law: Which governance law was violated
        trace_id: Preserved trace identifier
    """

    kind: MadlulLafziFailureKind
    reason: str
    violated_law: str
    trace_id: str = ""

    def __str__(self) -> str:
        return (
            f"MadlulLafziResidual[{self.kind.name}]: {self.reason} "
            f"(violated: {self.violated_law}, trace={self.trace_id})"
        )

    def __repr__(self) -> str:
        return f"MadlulLafziResidual(kind={self.kind.name}, trace_id='{self.trace_id}')"


# Factory functions for creating residuals


def make_missing_lafzi_registration_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for missing LafziMadlul registration."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.MISSING_LAFZI_REGISTRATION,
        reason="LafziMadlul registration not successful",
        violated_law="Law 1: No MadlulLafziCandidate without LafziMadlul registration",
        trace_id=trace_id,
    )


def make_wrong_domain_residual(actual_domain: str, trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for wrong domain."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.WRONG_DOMAIN,
        reason=f"Domain must be LAFZI_DALALI, got {actual_domain}",
        violated_law="Law 2: No MadlulLafziCandidate without StyleSpec(LAFZI_DALALI)",
        trace_id=trace_id,
    )


def make_missing_neutral_binding_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for missing NeutralBinding."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.MISSING_NEUTRAL_BINDING,
        reason="NeutralBinding not available",
        violated_law="Law 3: No MadlulLafziCandidate without NeutralBinding",
        trace_id=trace_id,
    )


def make_missing_prior_information_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for missing PriorInformation."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.MISSING_PRIOR_INFORMATION,
        reason="PriorInformation not available",
        violated_law="Law 4: No MadlulLafziCandidate without PriorInformation",
        trace_id=trace_id,
    )


def make_trace_not_preserved_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for trace not preserved."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.TRACE_NOT_PRESERVED,
        reason="trace_id not preserved",
        violated_law="Law 5: MadlulLafziCandidate preserves trace_id",
        trace_id=trace_id,
    )


def make_residuals_not_preserved_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for residuals not preserved."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.RESIDUALS_NOT_PRESERVED,
        reason="residuals not preserved",
        violated_law="Law 6: MadlulLafziCandidate preserves residuals",
        trace_id=trace_id,
    )


def make_unknown_madlul_type_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for UNKNOWN madlul type."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.UNKNOWN_MADLUL_TYPE,
        reason="UNKNOWN MadlulLafziType mapped to residual",
        violated_law="Law 13: UNKNOWN_MADLUL becomes residual",
        trace_id=trace_id,
    )


def make_external_meaning_attempted_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for attempted external meaning creation."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.EXTERNAL_MEANING_ATTEMPTED,
        reason="Attempted to create external meaning",
        violated_law="Law 7: MadlulLafziCandidate does not create external meaning",
        trace_id=trace_id,
    )


def make_dalalah_creation_attempted_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for attempted Dalalah creation."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.DALALAH_CREATION_ATTEMPTED,
        reason="Attempted to create Dalalah",
        violated_law="Law 8: MadlulLafziCandidate does not create Dalalah",
        trace_id=trace_id,
    )


def make_wadh_implementation_attempted_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for attempted Wadh implementation."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.WADH_IMPLEMENTATION_ATTEMPTED,
        reason="Attempted to implement Wadh",
        violated_law="Law 9: MadlulLafziCandidate does not implement Wadh",
        trace_id=trace_id,
    )


def make_hukm_issuance_attempted_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for attempted HUKM issuance."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.HUKM_ISSUANCE_ATTEMPTED,
        reason="Attempted to issue HUKM",
        violated_law="Law 10: MadlulLafziCandidate does not issue HUKM",
        trace_id=trace_id,
    )


def make_rank_inflation_attempted_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for attempted rank inflation."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.RANK_INFLATION_ATTEMPTED,
        reason="Attempted to raise PredicateRank",
        violated_law="Law 11: MadlulLafziCandidate does not raise PredicateRank",
        trace_id=trace_id,
    )


def make_dal_candidate_required_too_early_residual(trace_id: str = "") -> MadlulLafziResidual:
    """Create residual for premature DalCandidate requirement."""
    return MadlulLafziResidual(
        kind=MadlulLafziFailureKind.DAL_CANDIDATE_REQUIRED_TOO_EARLY,
        reason="DalCandidate required before MadlulLafziCandidate built",
        violated_law="Law 12: MadlulLafziCandidate does not require DalCandidate yet",
        trace_id=trace_id,
    )
