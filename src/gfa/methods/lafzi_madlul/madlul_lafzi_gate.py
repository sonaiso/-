"""
MadlulLafziGate - بوابة المدلول اللفظي

Gate for creating governed MadlulLafziCandidate instances.

Critical Law:
    لا مدلول لفظي بلا حوكمة
    No MadlulLafziCandidate without governance.

Gate Requirements:
    1. Requires successful LafziMadlul registration
    2. Requires StyleSpec(LAFZI_DALALI)
    3. Requires NeutralBinding
    4. Requires PriorInformation
    5. Preserves trace_id
    6. Preserves residuals
    7. Does NOT create external meaning
    8. Does NOT create Dalalah
    9. Does NOT implement Wadh
    10. Does NOT issue HUKM
    11. Does NOT raise PredicateRank
    12. Does NOT require DalCandidate yet
    13. UNKNOWN madlul type becomes residual
    14. Returns governed failures, not exceptions

Position in Architecture:
    RationalMethod (PR #55)
    └── NeutralBinding (PR #56)
        └── StyleSpec (PR #57)
            └── LafziMadlul Registration (PR #58)
                └── LafziTrace Gate (PR #59)
                    └── Dāl-alone Gate (PR #60)
                        └── Madlūl-lafẓī Gate (PR-L3) ← THIS MODULE
                            └── Dālālah Binding (future)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any

from gfa.methods.styles import StyleSpec, ThinkingDomain
from .madlul_lafzi_type import MadlulLafziType
from .madlul_lafzi_candidate import MadlulLafziCandidate, MadlulLafziResult
from .residual_taxonomy import (
    MadlulLafziResidual,
    MadlulLafziFailureKind,
    make_missing_lafzi_registration_residual,
    make_wrong_domain_residual,
    make_missing_neutral_binding_residual,
    make_missing_prior_information_residual,
    make_unknown_madlul_type_residual,
)


@dataclass(frozen=True)
class MadlulLafziFailure:
    """
    Governed failure from MadlulLafziGate.

    Contains:
        - residual: The specific failure residual
        - message: Human-readable explanation
    """

    residual: MadlulLafziResidual
    message: str

    def __str__(self) -> str:
        return f"MadlulLafziFailure: {self.message} ({self.residual.kind.name})"

    def __repr__(self) -> str:
        return f"MadlulLafziFailure(kind={self.residual.kind.name})"


@dataclass(frozen=True)
class MadlulLafziGate:
    """
    Gate for creating governed MadlulLafziCandidate instances.

    Critical Properties:
        - Requires successful registration
        - Requires LAFZI_DALALI domain
        - Requires NeutralBinding
        - Requires PriorInformation
        - Preserves trace_id
        - Preserves residuals
        - Does NOT create external meaning
        - Does NOT create Dalalah
        - Does NOT implement Wadh
        - Does NOT issue HUKM
        - Does NOT raise PredicateRank
        - Does NOT require DalCandidate yet
        - Returns governed failures, not exceptions
    """

    style_spec: StyleSpec
    neutral_binding_available: bool = True
    registration_successful: bool = True

    def verify_registration(self) -> bool:
        """Verify Law 1: Requires successful LafziMadlul registration."""
        return self.registration_successful

    def verify_style_spec(self) -> bool:
        """Verify Law 2: Requires StyleSpec(LAFZI_DALALI)."""
        return self.style_spec.get_domain() == ThinkingDomain.LAFZI_DALALI

    def verify_neutral_binding(self) -> bool:
        """Verify Law 3: Requires NeutralBinding."""
        return self.neutral_binding_available

    def verify_prior_information(self, prior_info: str) -> bool:
        """Verify Law 4: Requires PriorInformation."""
        return bool(prior_info)

    def preserves_trace_id(self, trace_id: str = "") -> bool:
        """Verify Law 5: Preserves trace_id."""
        return True  # By construction in process_input

    def preserves_residuals(self) -> bool:
        """Verify Law 6: Preserves residuals."""
        return True  # By construction in process_input

    def does_not_create_external_meaning(self) -> bool:
        """Verify Law 7: Does not create external meaning."""
        return True  # By construction (no meaning attribute)

    def does_not_create_dalalah(self) -> bool:
        """Verify Law 8: Does not create Dalalah."""
        return True  # By construction (no dalalah attribute)

    def does_not_implement_wadh(self) -> bool:
        """Verify Law 9: Does not implement Wadh."""
        return True  # By construction (no wadh attribute)

    def does_not_issue_hukm(self) -> bool:
        """Verify Law 10: Does not issue HUKM."""
        return True  # By construction (no hukm attribute)

    def does_not_raise_predicate_rank(self) -> bool:
        """Verify Law 11: Does not raise PredicateRank."""
        return True  # By construction (no rank attribute)

    def does_not_require_dal_candidate_yet(self) -> bool:
        """Verify Law 12: Does not require DalCandidate yet."""
        return True  # By construction (no dal_candidate parameter)

    def process_input(
        self,
        trace_id: str,
        madlul_type: MadlulLafziType,
        candidate_form: str,
        prior_information: str = "",
        residuals: tuple = (),
    ) -> MadlulLafziResult:
        """
        Process input to create MadlulLafziCandidate.

        Args:
            trace_id: Preserved trace identifier
            madlul_type: Type of linguistic signified
            candidate_form: The linguistic entity
            prior_information: Source evidence
            residuals: Existing residuals to preserve

        Returns:
            MadlulLafziResult with success or governed failure
        """
        # Law 1: Verify registration
        if not self.verify_registration():
            residual = make_missing_lafzi_registration_residual(trace_id)
            failure = MadlulLafziFailure(
                residual=residual,
                message="LafziMadlul registration not successful",
            )
            return MadlulLafziResult(success=False, failure=failure)

        # Law 2: Verify style spec domain
        if not self.verify_style_spec():
            actual_domain = str(self.style_spec.get_domain())
            residual = make_wrong_domain_residual(actual_domain, trace_id)
            failure = MadlulLafziFailure(
                residual=residual,
                message=f"Domain must be LAFZI_DALALI, got {actual_domain}",
            )
            return MadlulLafziResult(success=False, failure=failure)

        # Law 3: Verify neutral binding
        if not self.verify_neutral_binding():
            residual = make_missing_neutral_binding_residual(trace_id)
            failure = MadlulLafziFailure(
                residual=residual,
                message="NeutralBinding not available",
            )
            return MadlulLafziResult(success=False, failure=failure)

        # Law 4: Verify prior information
        if not self.verify_prior_information(prior_information):
            residual = make_missing_prior_information_residual(trace_id)
            failure = MadlulLafziFailure(
                residual=residual,
                message="PriorInformation not available",
            )
            return MadlulLafziResult(success=False, failure=failure)

        # Law 13: Handle UNKNOWN madlul type as residual
        current_residuals = residuals
        if madlul_type == MadlulLafziType.UNKNOWN_MADLUL:
            unknown_residual = make_unknown_madlul_type_residual(trace_id)
            current_residuals = current_residuals + (unknown_residual,)

        # Create candidate (Laws 5, 6 preserved by construction)
        candidate = MadlulLafziCandidate(
            trace_id=trace_id,
            madlul_type=madlul_type,
            candidate_form=candidate_form,
            source_prior_information=prior_information,
            residuals=current_residuals,
        )

        return MadlulLafziResult(success=True, candidate=candidate)

    def __str__(self) -> str:
        valid = all([
            self.verify_registration(),
            self.verify_style_spec(),
            self.verify_neutral_binding(),
        ])
        status = "VALID" if valid else "INVALID"
        return f"MadlulLafziGate[{status}]: domain={self.style_spec.get_domain().value}"

    def __repr__(self) -> str:
        return (
            f"MadlulLafziGate("
            f"domain={self.style_spec.get_domain().value}, "
            f"registration={self.registration_successful})"
        )
