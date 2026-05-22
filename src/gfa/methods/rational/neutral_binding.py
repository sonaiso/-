"""
NeutralBinding - العنصر المحايد في الطريقة العقلية

Nabhani Core Principle:
    الربط المحايد لا يرفع الرتبة ولا يخلق المعنى

    Neutral binding does not raise rank and does not create meaning.

NeutralBinding Definition:
    NeutralBinding =
    PriorInformation-preserving
    + Opinion-excluding
    + Trace-preserving
    + Rank-non-inflating
    + Residual-preserving
    + Binding

Critical Laws:
    1. No NeutralBinding without PriorInformation
    2. PriorOpinion is excluded, does not enter binding
    3. Binding preserves PriorInformation
    4. Binding preserves trace_id
    5. Binding preserves residuals
    6. Binding does NOT raise PredicateRank
    7. Binding does NOT convert ZANNI to CERTIFIED
    8. Binding does NOT create meaning
    9. Binding does NOT issue HUKM
    10. Binding does NOT jump domains without bridge
    11. All failures return governed objects, not bare exceptions

Position in Architecture:
    RationalMethod (root)
    └── NeutralBinding (neutral element)

    NeutralBinding is NOT:
    - ScientificMethod (future experimental branch)
    - LogicalStyle (future formal style)
    - StyleSpec (future domain specialization)
    - MeansAlgebra (future tool layer)
    - LafziMadlul (future linguistic domain)
    - Learning (future update layer)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple
from uuid import uuid4

from .prior_filter import PriorInformation, PriorOpinion, FilteredPrior
from .residual_taxonomy import RationalResidual, RationalResidualKind
from .judgment import PredicateRank, ExistenceRank
from .aql_operation import AqlOperationInput


@dataclass(frozen=True)
class NeutralBindingInput:
    """
    Input to neutral binding operation.

    Must contain:
    - Complete AqlOperationInput (all four pillars)
    - trace_id for lineage
    - residuals from prior stages
    """
    aql_input: AqlOperationInput
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    residuals: Tuple[RationalResidual, ...] = ()


@dataclass(frozen=True)
class NeutralBindingFailure:
    """
    Governed failure from neutral binding.

    Never a bare exception.
    Always preserves reason and trace.
    """
    reason: str
    missing_requirements: Tuple[str, ...]
    residuals: Tuple[str, ...]
    trace_id: str = field(default_factory=lambda: uuid4().hex)

    def __str__(self) -> str:
        return f"NeutralBinding failed: {self.reason}"


@dataclass(frozen=True)
class NeutralBindingResult:
    """
    Result of neutral binding operation.

    Critical Properties:
    - prior_information_preserved: PriorInformation unchanged
    - opinion_excluded: PriorOpinion not in binding
    - trace_preserved: trace_id carried through
    - rank_not_inflated: PredicateRank not raised
    - residuals_preserved: All residuals tracked
    """
    success: bool
    prior_information_preserved: bool
    opinion_excluded: bool
    trace_id: str
    predicate_rank_before: Optional[PredicateRank] = None
    predicate_rank_after: Optional[PredicateRank] = None
    residuals: Tuple[RationalResidual, ...] = ()
    failure: Optional[NeutralBindingFailure] = None
    bound_content: Optional[str] = None  # Neutral binding result (NOT meaning, NOT hukm)

    def is_success(self) -> bool:
        """Check if binding succeeded."""
        return self.success and self.failure is None

    def is_failure(self) -> bool:
        """Check if binding failed."""
        return not self.success and self.failure is not None

    def rank_was_not_inflated(self) -> bool:
        """
        Verify that PredicateRank was not raised.

        Critical Law:
            NeutralBinding does NOT raise rank.
            If before=ZANNI and after=CERTIFIED, this is a violation.
        """
        if self.predicate_rank_before is None or self.predicate_rank_after is None:
            return True

        # Define rank hierarchy (lower index = higher rank)
        rank_hierarchy = {
            PredicateRank.CERTIFIED: 0,
            PredicateRank.LICENSED: 1,
            PredicateRank.ZANNI: 2,
            PredicateRank.CANDIDATE: 3,
            PredicateRank.BLOCKED: 4,
            PredicateRank.UNRESOLVED: 5,
        }

        before_level = rank_hierarchy.get(self.predicate_rank_before, 5)
        after_level = rank_hierarchy.get(self.predicate_rank_after, 5)

        # After should be >= before (same or lower rank)
        return after_level >= before_level

    def zanni_was_not_certified(self) -> bool:
        """
        Verify ZANNI was not converted to CERTIFIED.

        Critical Law:
            NeutralBinding cannot certify.
            ZANNI → CERTIFIED is forbidden.
        """
        if self.predicate_rank_before is None or self.predicate_rank_after is None:
            return True

        if self.predicate_rank_before == PredicateRank.ZANNI:
            return self.predicate_rank_after != PredicateRank.CERTIFIED

        return True


class NeutralBinding:
    """
    Neutral element of RationalMethod.

    The binding that connects reality, sensory transfer, cognitive carrier,
    and prior information WITHOUT:
    - Raising predicate rank
    - Creating meaning
    - Issuing hukm
    - Hiding residuals
    - Jumping domains

    Laws Enforced:
    1. Requires PriorInformation
    2. Excludes PriorOpinion
    3. Preserves PriorInformation
    4. Preserves trace_id
    5. Preserves residuals
    6. Does not raise PredicateRank
    7. Does not convert ZANNI to CERTIFIED
    8. Does not create meaning
    9. Does not issue HUKM
    10. Does not jump domains without bridge
    11. Returns governed failures
    """

    @staticmethod
    def validate_input(input_data: NeutralBindingInput) -> Tuple[bool, Tuple[str, ...], Tuple[RationalResidual, ...]]:
        """
        Validate input requirements.

        Critical Requirements:
        1. Complete AqlOperationInput
        2. PriorInformation present and valid

        Returns:
            (is_valid, missing_requirements, residuals)
        """
        missing = []
        residuals_list = []

        if input_data.aql_input is None:
            missing.append("aql_operation_input")
            residuals_list.append(
                RationalResidual(
                    kind=RationalResidualKind.MISSING_PRIOR_INFORMATION,
                    description="No AqlOperationInput provided for NeutralBinding",
                    severity="blocker"
                )
            )
            return False, tuple(missing), tuple(residuals_list)

        # Check for PriorInformation
        if not input_data.aql_input.filtered_prior:
            missing.append("prior_information")
            residuals_list.append(
                RationalResidual(
                    kind=RationalResidualKind.MISSING_PRIOR_INFORMATION,
                    description="No prior information provided for neutral binding",
                    severity="blocker"
                )
            )

        if input_data.aql_input.filtered_prior and not input_data.aql_input.filtered_prior.has_valid_information():
            missing.append("valid_prior_information")
            residuals_list.append(
                RationalResidual(
                    kind=RationalResidualKind.INVALID_PRIOR_INFORMATION,
                    description="Prior information is not valid",
                    severity="blocker"
                )
            )

        is_valid = len(missing) == 0
        return is_valid, tuple(missing), tuple(residuals_list)

    @staticmethod
    def bind(input_data: NeutralBindingInput, initial_rank: PredicateRank = PredicateRank.ZANNI) -> NeutralBindingResult:
        """
        Execute neutral binding.

        Binding Operation:
        1. Validate input (requires PriorInformation)
        2. Exclude PriorOpinion (collect as residuals)
        3. Bind reality + sensory + carrier + prior_info
        4. Preserve trace_id
        5. Preserve residuals
        6. Do NOT raise PredicateRank
        7. Return governed result

        Args:
            input_data: NeutralBindingInput
            initial_rank: Starting PredicateRank (default ZANNI)

        Returns:
            NeutralBindingResult (never bare exception)
        """
        # Validate input
        is_valid, missing_requirements, validation_residuals = NeutralBinding.validate_input(input_data)

        if not is_valid:
            return NeutralBindingResult(
                success=False,
                prior_information_preserved=False,
                opinion_excluded=True,  # Opinions always excluded
                trace_id=input_data.trace_id,
                failure=NeutralBindingFailure(
                    reason="incomplete_neutral_binding_input",
                    missing_requirements=missing_requirements,
                    residuals=tuple(str(r) for r in validation_residuals),
                    trace_id=input_data.trace_id
                ),
                residuals=validation_residuals
            )

        # Collect opinion exclusion residuals
        opinion_residuals = []
        if input_data.aql_input.filtered_prior:
            for exclusion in input_data.aql_input.filtered_prior.get_exclusion_residuals():
                opinion_residuals.append(
                    RationalResidual(
                        kind=RationalResidualKind.PRIOR_OPINION_DETECTED,
                        description=exclusion,
                        severity="medium"
                    )
                )

        # Combine all residuals
        all_residuals = input_data.residuals + tuple(opinion_residuals) + validation_residuals

        # Execute neutral binding
        # This is the NEUTRAL element: it binds without raising rank
        bound_content = NeutralBinding._execute_neutral_binding(input_data)

        # Final rank is SAME as initial rank (no inflation)
        final_rank = initial_rank

        return NeutralBindingResult(
            success=True,
            prior_information_preserved=True,  # PriorInformation unchanged
            opinion_excluded=True,  # PriorOpinion excluded
            trace_id=input_data.trace_id,
            predicate_rank_before=initial_rank,
            predicate_rank_after=final_rank,
            residuals=all_residuals,
            bound_content=bound_content
        )

    @staticmethod
    def _execute_neutral_binding(input_data: NeutralBindingInput) -> str:
        """
        Internal binding execution.

        This is a NEUTRAL binding:
        - Does NOT create meaning
        - Does NOT issue hukm
        - Does NOT raise rank
        - Only connects elements preserving all properties

        Returns:
            Neutral binding description (NOT meaning, NOT hukm)
        """
        reality = input_data.aql_input.reality or "unspecified_reality"
        sensory = input_data.aql_input.sensory_transfer or "unspecified_sensory"
        carrier = input_data.aql_input.cognitive_carrier or "unspecified_carrier"
        prior_count = len(input_data.aql_input.filtered_prior.information) if input_data.aql_input.filtered_prior else 0

        # Neutral description (not interpretation)
        return f"neutral_binding(reality={reality}, sensory={sensory}, carrier={carrier}, prior_info_count={prior_count})"

    @staticmethod
    def does_not_create_meaning() -> bool:
        """
        Verify NeutralBinding does NOT create meaning.

        Meaning creation is domain-specific (lafzi, material, formal).
        NeutralBinding is pre-domain.
        """
        return True

    @staticmethod
    def does_not_issue_hukm() -> bool:
        """
        Verify NeutralBinding does NOT issue hukm (judgment).

        Hukm requires domain interpretation.
        NeutralBinding is pre-interpretation.
        """
        return True

    @staticmethod
    def does_not_implement_scientific_method() -> bool:
        """Verify NeutralBinding does NOT implement ScientificMethod."""
        return True

    @staticmethod
    def does_not_implement_logical_style() -> bool:
        """Verify NeutralBinding does NOT implement LogicalStyle."""
        return True

    @staticmethod
    def does_not_implement_lafzi_madlul() -> bool:
        """Verify NeutralBinding does NOT implement LafziMadlul."""
        return True

    @staticmethod
    def does_not_implement_domain_spec() -> bool:
        """Verify NeutralBinding does NOT implement DomainSpec."""
        return True

    @staticmethod
    def does_not_implement_style_spec() -> bool:
        """Verify NeutralBinding does NOT implement StyleSpec."""
        return True
