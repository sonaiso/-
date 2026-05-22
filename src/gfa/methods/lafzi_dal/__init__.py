"""
Lafzi Dal Module - بوابة الدال

Critical Law:
    الدال وحده حامل لفظي مرشح، لا معنى
    Dāl-alone is a signifier candidate, not meaning, not Madlul, not Dalalah.

PR-L2 Purpose:
    Implement DalCandidate as governed linguistic signifier candidate
    derived from LafziTrace.

What This Module Does:
    - Creates DalCandidate from LafziTrace
    - Classifies signifier modality (DalType)
    - Preserves trace_id and residuals
    - Returns governed candidate results
    - Maintains residuals for unknown signifier types

What This Module Does NOT Do:
    - Does NOT create meaning
    - Does NOT create Madlul (المدلول)
    - Does NOT create Dalalah (الدلالة)
    - Does NOT implement Wadh (الوضع)
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
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
                    └── Dāl-alone Gate (PR-L2) ← THIS MODULE
                        └── Madlūl-lafẓī (future)
                        └── Dālālah (future)

Critical:
    DalCandidate is a signifier carrier, not semantic execution.
    DalCandidate is a candidate for future binding, not bound meaning.
"""

from .dal_type import DalType
from .dal_candidate import DalCandidate, DalResult
from .dal_gate import DalGate, DalFailure
from .residual_taxonomy import (
    DalFailureKind,
    DalResidual,
    make_missing_lafzi_trace_residual,
    make_missing_registration_residual,
    make_missing_style_spec_residual,
    make_wrong_domain_residual,
    make_missing_neutral_binding_residual,
    make_trace_not_preserved_residual,
    make_residuals_not_preserved_residual,
    make_unknown_dal_type_residual,
    make_meaning_creation_attempted_residual,
    make_madlul_creation_attempted_residual,
    make_dalalah_creation_attempted_residual,
    make_wadh_implementation_attempted_residual,
    make_hukm_issuance_attempted_residual,
    make_rank_inflation_attempted_residual,
)

__all__ = [
    # Signifier types
    "DalType",
    # Core candidate
    "DalCandidate",
    "DalResult",
    # Gate
    "DalGate",
    "DalFailure",
    # Residual taxonomy
    "DalFailureKind",
    "DalResidual",
    "make_missing_lafzi_trace_residual",
    "make_missing_registration_residual",
    "make_missing_style_spec_residual",
    "make_wrong_domain_residual",
    "make_missing_neutral_binding_residual",
    "make_trace_not_preserved_residual",
    "make_residuals_not_preserved_residual",
    "make_unknown_dal_type_residual",
    "make_meaning_creation_attempted_residual",
    "make_madlul_creation_attempted_residual",
    "make_dalalah_creation_attempted_residual",
    "make_wadh_implementation_attempted_residual",
    "make_hukm_issuance_attempted_residual",
    "make_rank_inflation_attempted_residual",
]
