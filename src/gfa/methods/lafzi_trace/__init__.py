"""
LafziTrace Module - بوابة الأثر اللفظي

Critical Law:
    لا مدلول لفظي بلا أثر لفظي
    No LafziMadlul execution without LafziTrace.

PR-L1 Purpose:
    Implement LafziTrace gate as first governed Lafzi execution step.

What This Module Does:
    - Verifies linguistic trace exists
    - Preserves trace_id and trace_type
    - Returns governed trace results
    - Maintains residuals for unknown traces

What This Module Does NOT Do:
    - Does NOT implement Dal (الدال)
    - Does NOT implement Madlul (المدلول)
    - Does NOT implement Dalalah (الدلالة)
    - Does NOT implement Wadh (الوضع)
    - Does NOT create meaning
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
            └── LafziMadlul Registration (PR-L0)
                └── LafziTrace Gate (PR-L1) ← THIS MODULE
                    └── Dāl (future)
                    └── Madlūl (future)
                    └── Dālālah (future)

Critical:
    LafziTrace is a condition for linguistic processing.
    LafziTrace is NOT semantic execution.
    LafziTrace is NOT meaning.
"""

from .lafzi_trace_type import LafziTraceType
from .lafzi_trace import LafziTrace, LafziTraceResult
from .lafzi_trace_gate import LafziTraceGate, LafziTraceFailure
from .residual_taxonomy import (
    LafziTraceFailureKind,
    LafziTraceResidual,
    make_missing_registration_residual,
    make_missing_style_spec_residual,
    make_wrong_domain_residual,
    make_missing_neutral_binding_residual,
    make_missing_prior_information_residual,
    make_trace_not_preserved_residual,
    make_unknown_trace_type_residual,
    make_meaning_creation_attempted_residual,
    make_hukm_issuance_attempted_residual,
    make_dal_implementation_attempted_residual,
    make_madlul_implementation_attempted_residual,
    make_dalalah_implementation_attempted_residual,
    make_rank_inflation_attempted_residual,
)

__all__ = [
    # Trace types
    "LafziTraceType",
    # Core trace
    "LafziTrace",
    "LafziTraceResult",
    # Gate
    "LafziTraceGate",
    "LafziTraceFailure",
    # Residual taxonomy
    "LafziTraceFailureKind",
    "LafziTraceResidual",
    "make_missing_registration_residual",
    "make_missing_style_spec_residual",
    "make_wrong_domain_residual",
    "make_missing_neutral_binding_residual",
    "make_missing_prior_information_residual",
    "make_trace_not_preserved_residual",
    "make_unknown_trace_type_residual",
    "make_meaning_creation_attempted_residual",
    "make_hukm_issuance_attempted_residual",
    "make_dal_implementation_attempted_residual",
    "make_madlul_implementation_attempted_residual",
    "make_dalalah_implementation_attempted_residual",
    "make_rank_inflation_attempted_residual",
]
