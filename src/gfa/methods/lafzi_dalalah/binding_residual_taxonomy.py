"""
Binding Residual Taxonomy - تصنيف بقايا فشل الربط

Defines 13 failure kinds for DalMadlulBinding operations with factory functions.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class DalMadlulBindingFailureKind(Enum):
    """
    Taxonomy of binding failure kinds.

    13 failure categories:
        1. MISSING_DAL_CANDIDATE
        2. MISSING_MADLUL_CANDIDATE
        3. DAL_MADLUL_TYPE_MISMATCH
        4. BINDING_TRACE_NOT_PRESERVED
        5. BINDING_RESIDUALS_NOT_PRESERVED
        6. DALALAH_CREATION_ATTEMPTED
        7. WADH_ATTEMPTED_IN_BINDING
        8. MEANING_CREATION_IN_BINDING
        9. HUKM_ISSUANCE_IN_BINDING
        10. RANK_INFLATION_IN_BINDING
        11. SEMANTIC_INTERPRETATION_ATTEMPTED
        12. MUTABAQAH_ATTEMPTED_TOO_EARLY
        13. GOVERNED_FAILURE_NOT_RETURNED
    """

    MISSING_DAL_CANDIDATE = auto()
    MISSING_MADLUL_CANDIDATE = auto()
    DAL_MADLUL_TYPE_MISMATCH = auto()
    BINDING_TRACE_NOT_PRESERVED = auto()
    BINDING_RESIDUALS_NOT_PRESERVED = auto()
    DALALAH_CREATION_ATTEMPTED = auto()
    WADH_ATTEMPTED_IN_BINDING = auto()
    MEANING_CREATION_IN_BINDING = auto()
    HUKM_ISSUANCE_IN_BINDING = auto()
    RANK_INFLATION_IN_BINDING = auto()
    SEMANTIC_INTERPRETATION_ATTEMPTED = auto()
    MUTABAQAH_ATTEMPTED_TOO_EARLY = auto()
    GOVERNED_FAILURE_NOT_RETURNED = auto()


@dataclass(frozen=True)
class DalMadlulBindingResidual:
    """
    Residual from failed DalMadlulBinding operation.

    Attributes:
        kind: Type of failure
        reason: Human-readable explanation
        violated_law: Which governance law was violated
        trace_id: Trace ID from original operation
    """

    kind: DalMadlulBindingFailureKind
    reason: str
    violated_law: str
    trace_id: str


# Factory functions for each failure kind


def make_missing_dal_candidate_residual(trace_id: str) -> DalMadlulBindingResidual:
    """
    Law 1: No DalMadlulBinding without DalCandidate.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating missing DalCandidate
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.MISSING_DAL_CANDIDATE,
        reason="DalMadlulBinding requires DalCandidate (الدال)",
        violated_law="Law 1: No binding without DalCandidate",
        trace_id=trace_id,
    )


def make_missing_madlul_candidate_residual(trace_id: str) -> DalMadlulBindingResidual:
    """
    Law 2: No DalMadlulBinding without MadlulLafziCandidate.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating missing MadlulLafziCandidate
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.MISSING_MADLUL_CANDIDATE,
        reason="DalMadlulBinding requires MadlulLafziCandidate (المدلول اللفظي)",
        violated_law="Law 2: No binding without MadlulLafziCandidate",
        trace_id=trace_id,
    )


def make_dal_madlul_type_mismatch_residual(
    trace_id: str, dal_type: str, madlul_type: str
) -> DalMadlulBindingResidual:
    """
    Law 3: DalCandidate and MadlulCandidate types must be compatible.

    Args:
        trace_id: Trace identifier
        dal_type: Type of DalCandidate
        madlul_type: Type of MadlulCandidate

    Returns:
        Residual indicating type mismatch
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.DAL_MADLUL_TYPE_MISMATCH,
        reason=f"Type mismatch: Dal={dal_type}, Madlul={madlul_type}",
        violated_law="Law 3: Compatible types required for binding",
        trace_id=trace_id,
    )


def make_binding_trace_not_preserved_residual(
    trace_id: str,
) -> DalMadlulBindingResidual:
    """
    Law 4: DalMadlulBinding must preserve trace_id.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating trace not preserved
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.BINDING_TRACE_NOT_PRESERVED,
        reason="Binding trace_id not preserved",
        violated_law="Law 4: Binding preserves trace_id",
        trace_id=trace_id,
    )


def make_binding_residuals_not_preserved_residual(
    trace_id: str,
) -> DalMadlulBindingResidual:
    """
    Law 5: DalMadlulBinding must preserve residuals from both sides.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating residuals not preserved
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.BINDING_RESIDUALS_NOT_PRESERVED,
        reason="Residuals from Dal or Madlul not preserved",
        violated_law="Law 5: Binding preserves all residuals",
        trace_id=trace_id,
    )


def make_dalalah_creation_attempted_residual(
    trace_id: str,
) -> DalMadlulBindingResidual:
    """
    Law 6: DalMadlulBinding does NOT create full Dalalah.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating Dalalah creation attempt
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.DALALAH_CREATION_ATTEMPTED,
        reason="DalMadlulBinding does NOT create Dalalah (الدلالة)",
        violated_law="Law 6: Binding ≠ Dalalah",
        trace_id=trace_id,
    )


def make_wadh_attempted_in_binding_residual(
    trace_id: str,
) -> DalMadlulBindingResidual:
    """
    Law 7: DalMadlulBinding does NOT implement Wadh.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating Wadh attempt
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.WADH_ATTEMPTED_IN_BINDING,
        reason="DalMadlulBinding does NOT implement Wadh (الوضع)",
        violated_law="Law 7: Binding does not implement Wadh",
        trace_id=trace_id,
    )


def make_meaning_creation_in_binding_residual(
    trace_id: str,
) -> DalMadlulBindingResidual:
    """
    Law 8: DalMadlulBinding does NOT create external meaning.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating meaning creation attempt
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.MEANING_CREATION_IN_BINDING,
        reason="DalMadlulBinding does NOT create external meaning",
        violated_law="Law 8: Binding does not create meaning",
        trace_id=trace_id,
    )


def make_hukm_issuance_in_binding_residual(
    trace_id: str,
) -> DalMadlulBindingResidual:
    """
    Law 9: DalMadlulBinding does NOT issue HUKM.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating HUKM issuance attempt
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.HUKM_ISSUANCE_IN_BINDING,
        reason="DalMadlulBinding does NOT issue HUKM",
        violated_law="Law 9: Binding does not issue judgment",
        trace_id=trace_id,
    )


def make_rank_inflation_in_binding_residual(
    trace_id: str,
) -> DalMadlulBindingResidual:
    """
    Law 10: DalMadlulBinding does NOT raise PredicateRank.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating rank inflation attempt
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.RANK_INFLATION_IN_BINDING,
        reason="DalMadlulBinding does NOT raise PredicateRank",
        violated_law="Law 10: Binding preserves rank",
        trace_id=trace_id,
    )


def make_semantic_interpretation_attempted_residual(
    trace_id: str,
) -> DalMadlulBindingResidual:
    """
    Law 11: DalMadlulBinding does NOT perform semantic interpretation.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating semantic interpretation attempt
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.SEMANTIC_INTERPRETATION_ATTEMPTED,
        reason="DalMadlulBinding does NOT interpret semantics",
        violated_law="Law 11: Binding is neutral, not interpretive",
        trace_id=trace_id,
    )


def make_mutabaqah_attempted_too_early_residual(
    trace_id: str,
) -> DalMadlulBindingResidual:
    """
    Law 12: DalMadlulBinding does NOT implement Mutabaqah/Tadammun/Iltizam.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating Mutabaqah attempt
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.MUTABAQAH_ATTEMPTED_TOO_EARLY,
        reason="DalMadlulBinding does NOT implement Mutabaqah/Tadammun/Iltizam",
        violated_law="Law 12: Binding does not implement semantic relations",
        trace_id=trace_id,
    )


def make_governed_failure_not_returned_residual(
    trace_id: str,
) -> DalMadlulBindingResidual:
    """
    Law 13: DalMadlulBinding returns governed failures, not exceptions.

    Args:
        trace_id: Trace identifier

    Returns:
        Residual indicating bare exception was raised
    """
    return DalMadlulBindingResidual(
        kind=DalMadlulBindingFailureKind.GOVERNED_FAILURE_NOT_RETURNED,
        reason="Bare exception raised instead of governed failure",
        violated_law="Law 13: Return governed failures, not exceptions",
        trace_id=trace_id,
    )
