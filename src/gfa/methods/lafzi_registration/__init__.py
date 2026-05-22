"""
LafziMadlul Registration Module - تسجيل المدلول اللفظي

Critical Law:
    لا مدلول لفظي بلا حوكمة
    No LafziMadlul without governance.

PR-L0 Purpose:
    Register LafziMadlul as governed LAFZI_DALALI style ONLY.

What This Module Does:
    - Verifies governance requirements
    - Creates governance contract
    - Returns governed registration results

What This Module Does NOT Do:
    - Does NOT implement Dal (الدال)
    - Does NOT implement Madlul (المدلول)
    - Does NOT implement Dalalah (الدلالة)
    - Does NOT implement Wadh (الوضع)
    - Does NOT create meaning
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
    - Does NOT implement learning
    - Does NOT implement upward transitions
    - Does NOT implement downward decomposition
    - Does NOT implement ScientificMethod
    - Does NOT implement LogicalStyle
    - Does NOT implement MeansAlgebra
    - Does NOT implement UniversalRules

Position in Architecture:
    RationalMethod (PR #55)
    └── NeutralBinding (PR #56)
        └── StyleSpec (PR #57)
            └── LafziMadlul Registration (PR-L0) ← THIS MODULE
                └── LafziMadlul Execution (future)

Critical:
    Registration is NOT execution.
    Registration is a governance gate.
"""

from .lafzi_governance_contract import LafziGovernanceContract

from .residual_taxonomy import (
    LafziRegistrationFailureKind,
    LafziRegistrationResidual,
    make_missing_style_spec_residual,
    make_wrong_domain_residual,
    make_material_domain_rejected_residual,
    make_formal_domain_rejected_residual,
    make_missing_neutral_binding_residual,
    make_missing_prior_information_residual,
    make_prior_opinion_present_residual,
    make_trace_not_preserved_residual,
    make_residuals_not_preserved_residual,
    make_rank_inflated_residual,
    make_governance_violation_residual,
)

from .lafzi_style_registration import (
    LafziStyleRegistration,
    LafziRegistrationResult,
    LafziRegistrationFailure,
)

__all__ = [
    # Governance contract
    "LafziGovernanceContract",
    # Residual taxonomy
    "LafziRegistrationFailureKind",
    "LafziRegistrationResidual",
    "make_missing_style_spec_residual",
    "make_wrong_domain_residual",
    "make_material_domain_rejected_residual",
    "make_formal_domain_rejected_residual",
    "make_missing_neutral_binding_residual",
    "make_missing_prior_information_residual",
    "make_prior_opinion_present_residual",
    "make_trace_not_preserved_residual",
    "make_residuals_not_preserved_residual",
    "make_rank_inflated_residual",
    "make_governance_violation_residual",
    # Registration
    "LafziStyleRegistration",
    "LafziRegistrationResult",
    "LafziRegistrationFailure",
]
