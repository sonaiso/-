"""
Lafzi Dalalah Module - بوابة الدلالة اللفظية

Critical Law:
    الربط بين الدال والمدلول ليس دلالة كاملة
    Binding between Dāl and Madlūl is NOT full Dalalah.
    It is a neutral relation candidate, not semantic signification.

PR-L4 Purpose:
    Implement DalMadlulBindingCandidate as neutral relation between
    Dāl (signifier) and Madlūl (signified) within LAFZI_DALALI domain.

What This Module Does:
    - Creates DalMadlulBindingCandidate from Dāl and Madlūl inputs
    - Establishes neutral binding relation
    - Preserves trace_id and residuals from both sides
    - Preserves source prior information
    - Returns governed binding results
    - Maintains residuals for binding failures

What This Module Does NOT Do:
    - Does NOT create full Dalalah (الدلالة الكاملة)
    - Does NOT create Wadh (الوضع)
    - Does NOT implement external meaning
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
    - Does NOT perform semantic interpretation
    - Does NOT implement Mutabaqah/Tadammun/Iltizam
    - Does NOT create conventional placement
    - Does NOT perform learning

Position in Architecture:
    RationalMethod (PR #55)
    └── NeutralBinding (PR #56)
        └── StyleSpec (PR #57)
            └── LafziMadlul Registration (PR #58)
                └── LafziTrace Gate (PR #59)
                    └── Dāl-alone Gate (PR #60)
                        └── Madlūl-lafẓī Gate (PR-L3/PR #61)
                            └── Dāl/Madlūl Binding Gate (PR-L4) ← THIS MODULE
                                └── Full Dālālah (future)

Critical:
    DalMadlulBindingCandidate is a NEUTRAL relation candidate.
    It connects signifier and signified WITHOUT semantic interpretation.
    It is a prerequisite for Dalalah, NOT Dalalah itself.
"""

from .dal_madlul_binding_type import DalMadlulBindingType
from .dal_madlul_binding_candidate import (
    DalMadlulBindingCandidate,
    DalMadlulBindingResult,
)
from .dal_madlul_binding_gate import (
    DalMadlulBindingGate,
    DalMadlulBindingFailure,
)
from .binding_residual_taxonomy import (
    DalMadlulBindingFailureKind,
    DalMadlulBindingResidual,
    make_missing_dal_candidate_residual,
    make_missing_madlul_candidate_residual,
    make_dal_madlul_type_mismatch_residual,
    make_binding_trace_not_preserved_residual,
    make_binding_residuals_not_preserved_residual,
    make_dalalah_creation_attempted_residual,
    make_wadh_attempted_in_binding_residual,
    make_meaning_creation_in_binding_residual,
    make_hukm_issuance_in_binding_residual,
    make_rank_inflation_in_binding_residual,
    make_semantic_interpretation_attempted_residual,
    make_mutabaqah_attempted_too_early_residual,
    make_governed_failure_not_returned_residual,
)

__all__ = [
    # Binding types
    "DalMadlulBindingType",
    # Core candidate
    "DalMadlulBindingCandidate",
    "DalMadlulBindingResult",
    # Gate
    "DalMadlulBindingGate",
    "DalMadlulBindingFailure",
    # Residual taxonomy
    "DalMadlulBindingFailureKind",
    "DalMadlulBindingResidual",
    "make_missing_dal_candidate_residual",
    "make_missing_madlul_candidate_residual",
    "make_dal_madlul_type_mismatch_residual",
    "make_binding_trace_not_preserved_residual",
    "make_binding_residuals_not_preserved_residual",
    "make_dalalah_creation_attempted_residual",
    "make_wadh_attempted_in_binding_residual",
    "make_meaning_creation_in_binding_residual",
    "make_hukm_issuance_in_binding_residual",
    "make_rank_inflation_in_binding_residual",
    "make_semantic_interpretation_attempted_residual",
    "make_mutabaqah_attempted_too_early_residual",
    "make_governed_failure_not_returned_residual",
]
