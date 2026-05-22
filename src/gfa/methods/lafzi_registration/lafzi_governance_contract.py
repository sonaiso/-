"""
LafziGovernanceContract - عقد الحوكمة للمدلول اللفظي

Critical Law:
    لا مدلول لفظي بلا حوكمة
    No LafziMadlul without governance.

Governance Contract Definition:
    LafziMadlul allowed ⇔
    RationalMethod exists
    ∧ NeutralBinding exists
    ∧ StyleSpec.domain = LAFZI_DALALI
    ∧ PriorInformation exists
    ∧ PriorOpinion excluded

Critical Laws (10 Governance Rules):
    1. No LafziMadlul without StyleSpec
    2. No LafziMadlul unless domain = LAFZI_DALALI
    3. No LafziMadlul with MATERIAL_EXPERIMENTAL domain
    4. No LafziMadlul with FORMAL_LOGICAL domain
    5. No LafziMadlul without NeutralBinding
    6. No LafziMadlul without PriorInformation
    7. No LafziMadlul with PriorOpinion
    8. LafziMadlul registration preserves trace
    9. LafziMadlul registration preserves residuals
    10. LafziMadlul registration preserves rank

Position in Architecture:
    RationalMethod (root)
    └── NeutralBinding (neutral element)
        └── StyleSpec(LAFZI_DALALI) (domain specialization)
            └── LafziMadlul Registration (governance gate)
                └── LafziMadlul Execution (future, NOT in this PR)

This PR (PR-L0):
    - Registration as governance gate ONLY
    - Does NOT implement Dal
    - Does NOT implement Madlul
    - Does NOT implement Dalalah
    - Does NOT implement Wadh
    - Does NOT implement learning
    - Does NOT implement upward transitions
    - Does NOT implement downward decomposition

Registration is NOT execution.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from gfa.methods.rational import (
    NeutralBinding,
    NeutralBindingInput,
    PriorInformation,
    PriorOpinion,
)
from gfa.methods.styles import (
    StyleSpec,
    ThinkingDomain,
)


@dataclass(frozen=True)
class LafziGovernanceContract:
    """
    Governance contract for LafziMadlul domain.

    This contract verifies that all governance requirements are met
    BEFORE any linguistic operation can proceed.

    Critical Properties:
        - Requires StyleSpec
        - Requires LAFZI_DALALI domain
        - Rejects MATERIAL_EXPERIMENTAL domain
        - Rejects FORMAL_LOGICAL domain
        - Requires NeutralBinding
        - Requires PriorInformation
        - Excludes PriorOpinion
        - Preserves trace
        - Preserves residuals
        - Preserves rank

    What this contract does NOT do:
        - Does NOT implement Dal
        - Does NOT implement Madlul
        - Does NOT implement Dalalah
        - Does NOT create meaning
        - Does NOT issue HUKM
        - Does NOT raise PredicateRank
    """

    # Required components
    style_spec: StyleSpec
    neutral_binding_input: NeutralBindingInput

    def __post_init__(self):
        """Validate governance contract construction."""
        # Verify StyleSpec exists
        if self.style_spec is None:
            raise ValueError("StyleSpec is required for LafziMadlul governance")

        # Verify NeutralBindingInput exists
        if self.neutral_binding_input is None:
            raise ValueError("NeutralBindingInput is required for LafziMadlul governance")

    def get_domain(self) -> ThinkingDomain:
        """Get the domain of this governance contract."""
        return self.style_spec.get_domain()

    def requires_style_spec(self) -> bool:
        """
        Law 1: No LafziMadlul without StyleSpec.

        Returns True if StyleSpec exists.
        """
        return self.style_spec is not None

    def requires_lafzi_dalali_domain(self) -> bool:
        """
        Law 2: No LafziMadlul unless domain = LAFZI_DALALI.

        Returns True if domain is LAFZI_DALALI.
        """
        return self.style_spec.get_domain() == ThinkingDomain.LAFZI_DALALI

    def rejects_material_experimental_domain(self) -> bool:
        """
        Law 3: No LafziMadlul with MATERIAL_EXPERIMENTAL domain.

        Returns True if domain is NOT MATERIAL_EXPERIMENTAL.
        """
        return self.style_spec.get_domain() != ThinkingDomain.MATERIAL_EXPERIMENTAL

    def rejects_formal_logical_domain(self) -> bool:
        """
        Law 4: No LafziMadlul with FORMAL_LOGICAL domain.

        Returns True if domain is NOT FORMAL_LOGICAL.
        """
        return self.style_spec.get_domain() != ThinkingDomain.FORMAL_LOGICAL

    def requires_neutral_binding(self) -> bool:
        """
        Law 5: No LafziMadlul without NeutralBinding.

        Returns True if NeutralBindingInput exists.
        """
        return self.neutral_binding_input is not None

    def requires_prior_information(self) -> bool:
        """
        Law 6: No LafziMadlul without PriorInformation.

        Returns True if PriorInformation exists in aql_input.filtered_prior.
        """
        aql_input = self.neutral_binding_input.aql_input
        filtered_prior = aql_input.filtered_prior

        if filtered_prior is None:
            return False

        # Check that filtered_prior has valid information
        return filtered_prior.has_valid_information()

    def excludes_prior_opinion(self) -> bool:
        """
        Law 7: No LafziMadlul with PriorOpinion.

        Returns True if no opinions in filtered_prior.
        """
        aql_input = self.neutral_binding_input.aql_input
        filtered_prior = aql_input.filtered_prior

        if filtered_prior is None:
            return True  # No prior at all means no opinion

        # Prior must NOT have excluded opinions
        return filtered_prior.count_excluded() == 0

    def preserves_trace(self) -> bool:
        """
        Law 8: LafziMadlul registration preserves trace.

        Returns True if trace_id exists.
        """
        return self.neutral_binding_input.trace_id is not None

    def preserves_residuals(self) -> bool:
        """
        Law 9: LafziMadlul registration preserves residuals.

        Returns True (residuals always preserved, even if empty tuple).
        """
        # Residuals exist as tuple (may be empty)
        return isinstance(self.neutral_binding_input.residuals, tuple)

    def preserves_rank(self) -> bool:
        """
        Law 10: LafziMadlul registration preserves rank.

        Registration does NOT raise PredicateRank.
        Returns True (rank never inflated by registration).
        """
        # Registration itself does not modify rank
        # This is a declaration that rank is preserved
        return True

    def is_valid(self) -> bool:
        """
        Check if all governance requirements are satisfied.

        Returns True if all 10 laws are satisfied.
        """
        return (
            self.requires_style_spec()
            and self.requires_lafzi_dalali_domain()
            and self.rejects_material_experimental_domain()
            and self.rejects_formal_logical_domain()
            and self.requires_neutral_binding()
            and self.requires_prior_information()
            and self.excludes_prior_opinion()
            and self.preserves_trace()
            and self.preserves_residuals()
            and self.preserves_rank()
        )

    def get_violations(self) -> list[str]:
        """
        Get list of violated governance laws.

        Returns empty list if all laws satisfied.
        """
        violations = []

        if not self.requires_style_spec():
            violations.append("Missing StyleSpec")

        if not self.requires_lafzi_dalali_domain():
            violations.append(
                f"Domain must be LAFZI_DALALI, got {self.style_spec.get_domain()}"
            )

        if not self.rejects_material_experimental_domain():
            violations.append("MATERIAL_EXPERIMENTAL domain not allowed")

        if not self.rejects_formal_logical_domain():
            violations.append("FORMAL_LOGICAL domain not allowed")

        if not self.requires_neutral_binding():
            violations.append("Missing NeutralBindingInput")

        if not self.requires_prior_information():
            violations.append("Missing PriorInformation")

        if not self.excludes_prior_opinion():
            violations.append("PriorOpinion not allowed")

        if not self.preserves_trace():
            violations.append("Missing trace_id")

        if not self.preserves_residuals():
            violations.append("Residuals not preserved")

        if not self.preserves_rank():
            violations.append("Rank not preserved")

        return violations

    def does_not_create_meaning(self) -> bool:
        """
        Registration does NOT create meaning.

        This is a governance gate, not semantic execution.
        Returns True always (by construction).
        """
        return True

    def does_not_issue_hukm(self) -> bool:
        """
        Registration does NOT issue HUKM.

        This is a governance gate, not judgment.
        Returns True always (by construction).
        """
        return True

    def does_not_raise_predicate_rank(self) -> bool:
        """
        Registration does NOT raise PredicateRank.

        Registration verifies governance, does not certify claims.
        Returns True always (by construction).
        """
        return True

    def does_not_implement_dal(self) -> bool:
        """
        Registration does NOT implement Dal (الدال).

        Dal implementation is future work, not in PR-L0.
        Returns True always (by construction).
        """
        return True

    def does_not_implement_madlul(self) -> bool:
        """
        Registration does NOT implement Madlul (المدلول).

        Madlul implementation is future work, not in PR-L0.
        Returns True always (by construction).
        """
        return True

    def does_not_implement_dalalah(self) -> bool:
        """
        Registration does NOT implement Dalalah (الدلالة).

        Dalalah implementation is future work, not in PR-L0.
        Returns True always (by construction).
        """
        return True

    def __str__(self) -> str:
        if self.is_valid():
            return f"LafziGovernanceContract[VALID]: {self.style_spec.name_en}"
        else:
            violations = ", ".join(self.get_violations())
            return f"LafziGovernanceContract[INVALID]: {violations}"

    def __repr__(self) -> str:
        return (
            f"LafziGovernanceContract("
            f"domain={self.style_spec.get_domain().value}, "
            f"valid={self.is_valid()})"
        )
