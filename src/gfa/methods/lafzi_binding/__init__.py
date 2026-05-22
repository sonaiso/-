"""
Lafzi Binding Module - وحدة الربط اللفظي

Critical Law:
    الربط ليس دلالة كاملة
    Binding is NOT full Dalālah.

This module implements the first governed relation between DālCandidate
and MadlulLafziCandidate, creating DalMadlulBindingCandidate.

Core Components:
    - BindingBasis: Evidence for binding (NOT full Wadh)
    - BindingResidual: Typed residuals for all failures
    - DalMadlulBindingCandidate: Binding relation candidate
    - DalMadlulBindingGate: Validation and execution gate
    - DalMadlulBindingResult: Success/failure result

Critical Laws:
    1. Binding requires DālCandidate
    2. Binding requires MadlulLafziCandidate
    3. Binding requires LafziMadlul registration
    4. Binding requires StyleSpec(LAFZI_DALALI)
    5. Binding requires NeutralBinding
    6. Binding requires PriorInformation
    7. Binding preserves Dāl trace_id
    8. Binding preserves Madlūl trace_id
    9. Binding preserves residuals from both sides
    10. Binding does NOT create external meaning
    11. Binding does NOT create full Dalālah
    12. Binding does NOT implement Wadh
    13. Binding does NOT classify Mutabaqah/Tadammun/Iltizam
    14. Binding does NOT classify Haqiqah/Majaz
    15. Binding does NOT issue HUKM
    16. Binding does NOT raise PredicateRank
    17. Domain mismatch blocks binding
    18. UNKNOWN_BASIS becomes residual
    19. All failures return governed failures, not exceptions

Position in Architecture:
    RationalMethod
    └── NeutralBinding
        └── StyleSpec(LAFZI_DALALI)
            └── LafziMadlul Registration
                └── LafziTrace
                    ├── DālCandidate
                    └── MadlulLafziCandidate
                        └── DalMadlulBindingCandidate ← THIS MODULE
                            └── (Future) Wadh/Usage Gate (PR-L5)
                            └── (Future) Dalālah Type Gate (PR-L6)
                            └── (Future) Haqiqah/Majaz Gate (PR-L7)
"""

# Binding basis
from .binding_basis import BindingBasis

# Residual taxonomy
from .residual_taxonomy import (
    BindingResidualKind,
    BindingResidual,
    make_missing_dal_candidate_residual,
    make_missing_madlul_lafzi_candidate_residual,
    make_missing_lafzi_registration_residual,
    make_missing_lafzi_dalali_style_residual,
    make_missing_neutral_binding_residual,
    make_missing_prior_information_residual,
    make_domain_mismatch_residual,
    make_unknown_binding_basis_residual,
    make_trace_id_mismatch_residual,
    make_invalid_dal_candidate_residual,
    make_invalid_madlul_candidate_residual,
)

# Binding candidate
from .dal_madlul_binding_candidate import (
    DalMadlulBindingCandidate,
    DalMadlulBindingFailure,
    DalMadlulBindingResult,
)

# Binding gate
from .dal_madlul_binding_gate import (
    DalMadlulBindingInput,
    DalMadlulBindingGate,
)

__all__ = [
    # Binding basis
    "BindingBasis",
    # Residual taxonomy
    "BindingResidualKind",
    "BindingResidual",
    "make_missing_dal_candidate_residual",
    "make_missing_madlul_lafzi_candidate_residual",
    "make_missing_lafzi_registration_residual",
    "make_missing_lafzi_dalali_style_residual",
    "make_missing_neutral_binding_residual",
    "make_missing_prior_information_residual",
    "make_domain_mismatch_residual",
    "make_unknown_binding_basis_residual",
    "make_trace_id_mismatch_residual",
    "make_invalid_dal_candidate_residual",
    "make_invalid_madlul_candidate_residual",
    # Binding candidate
    "DalMadlulBindingCandidate",
    "DalMadlulBindingFailure",
    "DalMadlulBindingResult",
    # Binding gate
    "DalMadlulBindingInput",
    "DalMadlulBindingGate",
]
