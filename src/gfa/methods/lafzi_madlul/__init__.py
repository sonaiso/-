"""
Lafzi Madlul Module - بوابة المدلول اللفظي

Critical Law:
    المدلول اللفظي ليس معنى خارجياً بالضرورة
    Madlūl-lafẓī is NOT necessarily external meaning.
    Madlūl-lafẓī is a governed candidate for what may be signified
    inside the linguistic domain.

PR-L3 Purpose:
    Implement MadlulLafziCandidate as governed linguistic signified candidate
    within LAFZI_DALALI domain.

What This Module Does:
    - Creates MadlulLafziCandidate from input
    - Classifies madlul type (letter, harakah, pattern, etc.)
    - Preserves trace_id and residuals
    - Preserves source prior information
    - Returns governed candidate results
    - Maintains residuals for unknown madlul types

What This Module Does NOT Do:
    - Does NOT create external meaning
    - Does NOT create Dalalah (الدلالة)
    - Does NOT implement Wadh (الوضع)
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
    - Does NOT require DalCandidate yet
    - Does NOT create semantic content
    - Does NOT perform learning
    - Does NOT implement upward transitions
    - Does NOT implement downward decomposition

Position in Architecture:
    RationalMethod (PR #55)
    └── NeutralBinding (PR #56)
        └── StyleSpec (PR #57)
            └── LafziMadlul Registration (PR #58)
                └── LafziTrace Gate (PR #59)
                    └── Dāl-alone Gate (PR #60)
                        └── Madlūl-lafẓī Gate (PR-L3) ← THIS MODULE
                            └── Dālālah Binding (future)

Critical:
    MadlulLafziCandidate is a linguistic signified candidate, not external meaning.
    MadlulLafziCandidate is a candidate for future binding, not bound signified.
"""

from .madlul_lafzi_type import MadlulLafziType
from .madlul_lafzi_candidate import MadlulLafziCandidate, MadlulLafziResult
from .madlul_lafzi_gate import MadlulLafziGate, MadlulLafziFailure
from .residual_taxonomy import (
    MadlulLafziFailureKind,
    MadlulLafziResidual,
    make_missing_lafzi_registration_residual,
    make_wrong_domain_residual,
    make_missing_neutral_binding_residual,
    make_missing_prior_information_residual,
    make_trace_not_preserved_residual,
    make_residuals_not_preserved_residual,
    make_unknown_madlul_type_residual,
    make_external_meaning_attempted_residual,
    make_dalalah_creation_attempted_residual,
    make_wadh_implementation_attempted_residual,
    make_hukm_issuance_attempted_residual,
    make_rank_inflation_attempted_residual,
    make_dal_candidate_required_too_early_residual,
)

__all__ = [
    # Madlul types
    "MadlulLafziType",
    # Core candidate
    "MadlulLafziCandidate",
    "MadlulLafziResult",
    # Gate
    "MadlulLafziGate",
    "MadlulLafziFailure",
    # Residual taxonomy
    "MadlulLafziFailureKind",
    "MadlulLafziResidual",
    "make_missing_lafzi_registration_residual",
    "make_wrong_domain_residual",
    "make_missing_neutral_binding_residual",
    "make_missing_prior_information_residual",
    "make_trace_not_preserved_residual",
    "make_residuals_not_preserved_residual",
    "make_unknown_madlul_type_residual",
    "make_external_meaning_attempted_residual",
    "make_dalalah_creation_attempted_residual",
    "make_wadh_implementation_attempted_residual",
    "make_hukm_issuance_attempted_residual",
    "make_rank_inflation_attempted_residual",
    "make_dal_candidate_required_too_early_residual",
]
