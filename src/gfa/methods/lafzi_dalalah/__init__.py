"""
Lafzi Dalalah Module - الدلالة اللفظية

Critical Law:
    الدلالة تبنى على الوضع، لا تساوي الحكم
    Dalalah is built on Wadh, NOT equivalent to judgment.

This module implements Mutabaqah (conformity) processing for PR-L6A.

What PR-L6A Implements:
    - MutabaqahCandidate structure
    - MutabaqahGate (admission/blocking logic)
    - MutabaqahResult (governed results)
    - MutabaqahResidual taxonomy

What PR-L6A Does NOT Implement:
    - Tadammun (→ PR-L6B)
    - Iltizam (→ PR-L6C)
    - Haqiqah/Majaz/Naql classification (→ PR-L7+)
    - HUKM issuance (→ Future)
    - Ifadah (→ Future)
    - Learning (→ Future)
    - Upward transitions (→ Future)
    - Downward decomposition (→ Future)

Critical Laws Enforced:
    1. MutabaqahCandidate requires admitted WadhClaim
    2. MutabaqahCandidate requires MawduLahStructure
    3. MutabaqahCandidate requires MawduLahStructure.whole
    4. MutabaqahCandidate preserves WadhClaim trace
    5. MutabaqahCandidate preserves binding trace
    6. MutabaqahCandidate preserves residuals
    7. MutabaqahCandidate does NOT create external meaning
    8. MutabaqahCandidate does NOT issue HUKM
    9. MutabaqahCandidate does NOT create Tadammun
    10. MutabaqahCandidate does NOT create Iltizam
    11. MutabaqahCandidate does NOT classify Haqiqah/Majaz/Naql
    12. MutabaqahCandidate does NOT create Ifadah
    13. MutabaqahCandidate does NOT raise PredicateRank to CERTIFIED
    14. Unknown whole becomes residual, not exception
    15. Polysemy possible becomes residual
    16. Homonymy possible becomes residual
    17. Partial usage blocks or residualizes
    18. Success means candidate admitted, NOT truth certified

Position in Architecture:
    RationalMethod
    └── NeutralBinding
        └── StyleSpec(LAFZI_DALALI)
            └── LafziMadlul Registration
                └── LafziTrace
                    ├── DālCandidate
                    └── MadlulLafziCandidate
                        └── DalMadlulBindingCandidate (PR-L4)
                            └── WadhGeometry (PR-L5A)
                                └── WadhGate (PR-L5B)
                                    └── MutabaqahGate (PR-L6A) ← THIS MODULE
"""

from __future__ import annotations

# Residual taxonomy
from .residual_taxonomy import (
    MutabaqahResidualKind,
    MutabaqahResidual,
    make_wadh_claim_not_admitted_residual,
    make_mawdu_lah_whole_unavailable_residual,
    make_polysemy_possible_residual,
    make_homonymy_possible_residual,
    make_partial_usage_detected_residual,
    make_external_meaning_injection_residual,
    make_hukm_injection_residual,
    make_tadammun_created_residual,
    make_iltizam_created_residual,
    make_haqiqah_majaz_classified_residual,
    make_wadh_trace_lost_residual,
    make_binding_trace_lost_residual,
)

# Candidate structure
from .mutabaqah_candidate import MutabaqahCandidate

# Result structures
from .mutabaqah_result import (
    MutabaqahResult,
    MutabaqahFailure,
)

# Gate
from .mutabaqah_gate import MutabaqahGate


__all__ = [
    # Residuals
    "MutabaqahResidualKind",
    "MutabaqahResidual",
    "make_wadh_claim_not_admitted_residual",
    "make_mawdu_lah_whole_unavailable_residual",
    "make_polysemy_possible_residual",
    "make_homonymy_possible_residual",
    "make_partial_usage_detected_residual",
    "make_external_meaning_injection_residual",
    "make_hukm_injection_residual",
    "make_tadammun_created_residual",
    "make_iltizam_created_residual",
    "make_haqiqah_majaz_classified_residual",
    "make_wadh_trace_lost_residual",
    "make_binding_trace_lost_residual",

    # Candidate
    "MutabaqahCandidate",

    # Result
    "MutabaqahResult",
    "MutabaqahFailure",

    # Gate
    "MutabaqahGate",
]
