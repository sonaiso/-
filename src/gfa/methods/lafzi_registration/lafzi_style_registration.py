"""
LafziStyleRegistration - تسجيل الأسلوب اللفظي الدلالي

Critical Law:
    التسجيل ليس التنفيذ
    Registration is NOT execution.

Registration Purpose:
    Prove that LafziMadlul cannot operate as independent island.
    LafziMadlul must be governed by:
        RationalMethod + NeutralBinding + StyleSpec(LAFZI_DALALI)

Registration Process:
    1. Verify StyleSpec exists
    2. Verify domain = LAFZI_DALALI
    3. Reject MATERIAL_EXPERIMENTAL domain
    4. Reject FORMAL_LOGICAL domain
    5. Verify NeutralBinding exists
    6. Verify PriorInformation exists
    7. Verify PriorOpinion excluded
    8. Preserve trace
    9. Preserve residuals
    10. Preserve rank

What Registration Does NOT Do:
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
    RationalMethod (root)
    └── NeutralBinding (neutral element)
        └── StyleSpec(LAFZI_DALALI) (domain specialization)
            └── LafziMadlul Registration (governance gate) ← THIS PR
                └── LafziMadlul Execution (future, NOT this PR)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple
from uuid import uuid4

from gfa.methods.rational import (
    NeutralBinding,
    NeutralBindingInput,
    NeutralBindingResult,
    PriorInformation,
)
from gfa.methods.styles import (
    StyleSpec,
    ThinkingDomain,
    make_lafzi_dalali_style,
)

from .lafzi_governance_contract import LafziGovernanceContract
from .residual_taxonomy import (
    LafziRegistrationResidual,
    LafziRegistrationFailureKind,
    make_missing_style_spec_residual,
    make_wrong_domain_residual,
    make_material_domain_rejected_residual,
    make_formal_domain_rejected_residual,
    make_missing_neutral_binding_residual,
    make_missing_prior_information_residual,
    make_prior_opinion_present_residual,
)


@dataclass(frozen=True)
class LafziRegistrationFailure:
    """
    Governed failure from LafziMadlul registration.

    Never a bare exception.
    Always returns governed object with:
        - residuals (typed failure objects)
        - trace_id (lineage)
        - violations (law descriptions)
    """

    residuals: Tuple[LafziRegistrationResidual, ...]
    violations: Tuple[str, ...]
    trace_id: str

    def __str__(self) -> str:
        violations_str = ", ".join(self.violations)
        return f"LafziRegistrationFailure: {violations_str}"

    def __repr__(self) -> str:
        return (
            f"LafziRegistrationFailure("
            f"residuals={len(self.residuals)}, "
            f"violations={len(self.violations)})"
        )


@dataclass(frozen=True)
class LafziRegistrationResult:
    """
    Result of LafziMadlul registration attempt.

    Success means:
        - All governance requirements satisfied
        - LafziMadlul is now allowed to operate (in future PRs)
        - Trace preserved
        - Residuals preserved
        - Rank preserved

    Success does NOT mean:
        - Dal implemented
        - Madlul implemented
        - Dalalah implemented
        - Meaning created
        - HUKM issued
        - Rank raised

    Critical:
        Registration is a governance gate, not semantic execution.
    """

    success: bool
    governance_contract: Optional[LafziGovernanceContract]
    failure: Optional[LafziRegistrationFailure]
    trace_id: str

    def __post_init__(self):
        """Validate registration result."""
        if self.success and self.governance_contract is None:
            raise ValueError("Success requires valid governance_contract")

        if not self.success and self.failure is None:
            raise ValueError("Failure requires failure object")

        if self.success and self.failure is not None:
            raise ValueError("Success and failure are mutually exclusive")

        if not self.success and self.governance_contract is not None:
            # Governance contract can exist even on failure (for analysis)
            pass

    def is_success(self) -> bool:
        """Check if registration succeeded."""
        return self.success

    def is_failure(self) -> bool:
        """Check if registration failed."""
        return not self.success

    def get_violations(self) -> list[str]:
        """Get list of violated laws."""
        if self.success:
            return []

        if self.failure:
            return list(self.failure.violations)

        return []

    def does_not_create_meaning(self) -> bool:
        """
        Registration does NOT create meaning.

        Returns True always (by construction).
        """
        return True

    def does_not_issue_hukm(self) -> bool:
        """
        Registration does NOT issue HUKM.

        Returns True always (by construction).
        """
        return True

    def does_not_raise_predicate_rank(self) -> bool:
        """
        Registration does NOT raise PredicateRank.

        Returns True always (by construction).
        """
        return True

    def does_not_implement_dal(self) -> bool:
        """
        Registration does NOT implement Dal.

        Returns True always (by construction).
        """
        return True

    def does_not_implement_madlul(self) -> bool:
        """
        Registration does NOT implement Madlul.

        Returns True always (by construction).
        """
        return True

    def does_not_implement_dalalah(self) -> bool:
        """
        Registration does NOT implement Dalalah.

        Returns True always (by construction).
        """
        return True

    def __str__(self) -> str:
        if self.success:
            return f"LafziRegistrationResult[SUCCESS]: Governance satisfied"
        else:
            return f"LafziRegistrationResult[FAILURE]: {self.failure}"

    def __repr__(self) -> str:
        return f"LafziRegistrationResult(success={self.success})"


class LafziStyleRegistration:
    """
    Registration system for LafziMadlul governance.

    This class verifies that LafziMadlul operates under proper governance:
        RationalMethod + NeutralBinding + StyleSpec(LAFZI_DALALI)

    Critical Laws:
        1. Registration is governance verification, not execution
        2. Registration requires all governance components
        3. Registration rejects wrong domains
        4. Registration preserves trace/residuals/rank
        5. Registration returns governed failures, not exceptions

    What this class does NOT do:
        - Does NOT implement Dal/Madlul/Dalalah
        - Does NOT create meaning
        - Does NOT issue HUKM
        - Does NOT raise PredicateRank
        - Does NOT implement learning
        - Does NOT implement transitions
    """

    @staticmethod
    def register(
        style_spec: Optional[StyleSpec],
        neutral_binding_input: Optional[NeutralBindingInput],
        trace_id: Optional[str] = None,
    ) -> LafziRegistrationResult:
        """
        Attempt to register LafziMadlul under governance.

        This verifies all governance requirements.
        This does NOT execute linguistic operations.

        Args:
            style_spec: StyleSpec (must be LAFZI_DALALI domain)
            neutral_binding_input: NeutralBindingInput with all requirements
            trace_id: Optional trace for lineage

        Returns:
            LafziRegistrationResult (success or governed failure)

        Critical:
            This is governance gate, not semantic execution.
            Registration ≠ Implementation.
        """
        trace_id = trace_id or uuid4().hex
        residuals: list[LafziRegistrationResidual] = []
        violations: list[str] = []

        # Law 1: Requires StyleSpec
        if style_spec is None:
            residuals.append(make_missing_style_spec_residual(trace_id))
            violations.append("Missing StyleSpec")
            return LafziRegistrationResult(
                success=False,
                governance_contract=None,
                failure=LafziRegistrationFailure(
                    residuals=tuple(residuals),
                    violations=tuple(violations),
                    trace_id=trace_id,
                ),
                trace_id=trace_id,
            )

        # Law 2: Requires LAFZI_DALALI domain
        domain = style_spec.get_domain()
        if domain != ThinkingDomain.LAFZI_DALALI:
            residuals.append(make_wrong_domain_residual(domain.value, trace_id))
            violations.append(f"Domain must be LAFZI_DALALI, got {domain.value}")

        # Law 3: Rejects MATERIAL_EXPERIMENTAL
        if domain == ThinkingDomain.MATERIAL_EXPERIMENTAL:
            residuals.append(make_material_domain_rejected_residual(trace_id))
            violations.append("MATERIAL_EXPERIMENTAL domain not allowed")

        # Law 4: Rejects FORMAL_LOGICAL
        if domain == ThinkingDomain.FORMAL_LOGICAL:
            residuals.append(make_formal_domain_rejected_residual(trace_id))
            violations.append("FORMAL_LOGICAL domain not allowed")

        # Law 5: Requires NeutralBinding
        if neutral_binding_input is None:
            residuals.append(make_missing_neutral_binding_residual(trace_id))
            violations.append("Missing NeutralBindingInput")
            return LafziRegistrationResult(
                success=False,
                governance_contract=None,
                failure=LafziRegistrationFailure(
                    residuals=tuple(residuals),
                    violations=tuple(violations),
                    trace_id=trace_id,
                ),
                trace_id=trace_id,
            )

        # Law 6: Requires PriorInformation
        aql_input = neutral_binding_input.aql_input
        prior = aql_input.prior_information
        if not isinstance(prior, PriorInformation):
            residuals.append(make_missing_prior_information_residual(trace_id))
            violations.append("Missing PriorInformation")

        # Law 7: Excludes PriorOpinion
        from gfa.methods.rational import PriorOpinion
        if isinstance(prior, PriorOpinion):
            residuals.append(make_prior_opinion_present_residual(trace_id))
            violations.append("PriorOpinion not allowed")

        # Check if any violations occurred
        if residuals or violations:
            return LafziRegistrationResult(
                success=False,
                governance_contract=None,
                failure=LafziRegistrationFailure(
                    residuals=tuple(residuals),
                    violations=tuple(violations),
                    trace_id=trace_id,
                ),
                trace_id=trace_id,
            )

        # All laws satisfied - create governance contract
        governance_contract = LafziGovernanceContract(
            style_spec=style_spec,
            neutral_binding_input=neutral_binding_input,
        )

        # Verify contract is valid
        if not governance_contract.is_valid():
            contract_violations = governance_contract.get_violations()
            return LafziRegistrationResult(
                success=False,
                governance_contract=governance_contract,
                failure=LafziRegistrationFailure(
                    residuals=tuple(residuals),
                    violations=tuple(contract_violations),
                    trace_id=trace_id,
                ),
                trace_id=trace_id,
            )

        # Success - governance satisfied
        return LafziRegistrationResult(
            success=True,
            governance_contract=governance_contract,
            failure=None,
            trace_id=trace_id,
        )

    @staticmethod
    def does_not_implement_dal() -> bool:
        """
        This class does NOT implement Dal.

        Dal implementation is future work (PR-L2).
        Returns True always.
        """
        return True

    @staticmethod
    def does_not_implement_madlul() -> bool:
        """
        This class does NOT implement Madlul.

        Madlul implementation is future work (PR-L3).
        Returns True always.
        """
        return True

    @staticmethod
    def does_not_implement_dalalah() -> bool:
        """
        This class does NOT implement Dalalah.

        Dalalah implementation is future work (PR-L4).
        Returns True always.
        """
        return True
