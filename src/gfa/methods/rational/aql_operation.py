"""
AqlOperation - العملية العقلية

Nabhani Core Definition:
    العقل = نقل الحس بالواقع إلى الدماغ + معلومات سابقة

Four Pillars (الأركان الأربعة):
    1. Reality (الواقع)
    2. Sensory Transfer (نقل الحس)
    3. Cognitive Carrier (الدماغ الصالح)
    4. Prior Information (المعلومات السابقة)

Critical Laws:
    - All four pillars must be present
    - Absence of one pillar prevents thought
    - Prior opinion must be excluded
    - Result is governed (not bare exception)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple
from uuid import uuid4

from .prior_filter import FilteredPrior
from .residual_taxonomy import RationalResidual, RationalResidualKind
from .judgment import AqlJudgment, AqlJudgmentFailure, ExistenceRank, PredicateRank


@dataclass(frozen=True)
class AqlOperationInput:
    """
    Input to rational operation.

    Placeholder types - will integrate with actual GFA types.
    """
    reality: Optional[str]  # Placeholder for Reality
    sensory_transfer: Optional[str]  # Placeholder for SensoryTransfer
    cognitive_carrier: Optional[str]  # Placeholder for CognitiveCarrier
    filtered_prior: Optional[FilteredPrior]


@dataclass(frozen=True)
class AqlOperationResult:
    """
    Result of rational operation.

    Either success (judgment) or governed failure.
    Never a bare exception.
    """
    success: bool
    judgment: Optional[AqlJudgment] = None
    failure: Optional[AqlJudgmentFailure] = None
    residuals: Tuple[RationalResidual, ...] = ()
    trace_id: str = field(default_factory=lambda: uuid4().hex)

    def is_success(self) -> bool:
        """Check if operation succeeded."""
        return self.success and self.judgment is not None

    def is_failure(self) -> bool:
        """Check if operation failed."""
        return not self.success and self.failure is not None


class AqlOperation:
    """
    Rational operation implementing Nabhani four-pillar requirement.

    Laws enforced:
    - No operation without reality
    - No operation without sensory transfer
    - No operation without cognitive carrier
    - No operation without prior information
    - Prior opinion excluded
    - Failures return governed objects
    """

    @staticmethod
    def validate_pillars(input_data: AqlOperationInput) -> Tuple[bool, Tuple[str, ...], Tuple[RationalResidual, ...]]:
        """
        Validate that all four pillars are present.

        Returns:
            (is_valid, missing_pillars, residuals)
        """
        missing = []
        residuals_list = []

        if not input_data.reality:
            missing.append("reality")
            residuals_list.append(
                RationalResidual(
                    kind=RationalResidualKind.MISSING_REALITY,
                    description="No reality provided for rational operation",
                    severity="blocker"
                )
            )

        if not input_data.sensory_transfer:
            missing.append("sensory_transfer")
            residuals_list.append(
                RationalResidual(
                    kind=RationalResidualKind.MISSING_SENSORY_TRANSFER,
                    description="No sensory transfer provided",
                    severity="blocker"
                )
            )

        if not input_data.cognitive_carrier:
            missing.append("cognitive_carrier")
            residuals_list.append(
                RationalResidual(
                    kind=RationalResidualKind.MISSING_COGNITIVE_CARRIER,
                    description="No cognitive carrier provided",
                    severity="blocker"
                )
            )

        if not input_data.filtered_prior or not input_data.filtered_prior.has_valid_information():
            missing.append("prior_information")
            residuals_list.append(
                RationalResidual(
                    kind=RationalResidualKind.MISSING_PRIOR_INFORMATION,
                    description="No valid prior information provided",
                    severity="blocker"
                )
            )

        is_valid = len(missing) == 0
        return is_valid, tuple(missing), tuple(residuals_list)

    @staticmethod
    def execute(input_data: AqlOperationInput) -> AqlOperationResult:
        """
        Execute rational operation.

        Nabhani Law:
            نقص واحد من الأركان الأربعة يمنع حصول الفكر
            "Absence of one pillar prevents thought"

        Returns:
            Governed result (never bare exception)
        """
        # Validate pillars
        is_valid, missing_pillars, pillar_residuals = AqlOperation.validate_pillars(input_data)

        if not is_valid:
            # Return governed failure
            return AqlOperationResult(
                success=False,
                failure=AqlJudgmentFailure(
                    reason="incomplete_aql_operation",
                    missing_pillars=missing_pillars,
                    residuals=tuple(str(r) for r in pillar_residuals)
                ),
                residuals=pillar_residuals
            )

        # Collect residuals from excluded opinions
        opinion_residuals = []
        if input_data.filtered_prior:
            for exclusion in input_data.filtered_prior.get_exclusion_residuals():
                opinion_residuals.append(
                    RationalResidual(
                        kind=RationalResidualKind.PRIOR_OPINION_DETECTED,
                        description=exclusion,
                        severity="medium"
                    )
                )

        # Execute rational binding
        # For now, simplified judgment
        # Real implementation would use NeutralBinding
        judgment = AqlJudgment(
            claim=f"Rational judgment from {input_data.reality}",
            existence_rank=ExistenceRank.QATI_EXISTENCE if input_data.sensory_transfer else ExistenceRank.ZANNI_EXISTENCE,
            predicate_rank=PredicateRank.ZANNI,  # Always start as ZANNI
            evidence=(
                f"sensory: {input_data.sensory_transfer}",
                f"prior_info_count: {len(input_data.filtered_prior.information)}"
            ),
            residuals=tuple(str(r) for r in opinion_residuals),
            trace_lineage=()
        )

        return AqlOperationResult(
            success=True,
            judgment=judgment,
            residuals=tuple(opinion_residuals)
        )
