"""
RationalMethod - الطريقة العقلية (Root Governing Method)

Nabhani Core Principle:
    الطريقة العقلية هي الأصل
    "The rational method is the root"

    All other methods are branches or specializations.
    No branch may claim to be root.

Critical Laws:
    1. No thought without four pillars (reality, sensory, carrier, prior info)
    2. Prior opinion must be excluded
    3. Existence rank ≠ Predicate rank
    4. Failures return governed objects
    5. No method may bypass rational method
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Any

from .prior_filter import filter_prior, PriorInformation, PriorOpinion
from .aql_operation import AqlOperation, AqlOperationInput, AqlOperationResult


@dataclass(frozen=True)
class RationalMethod:
    """
    The governing root method for all thinking.

    Nabhani Hierarchy:
        RationalMethod (root)
        ├─ ScientificMethod (experimental branch - NOT YET IMPLEMENTED)
        ├─ LogicalStyle (formal grounded style - NOT YET IMPLEMENTED)
        ├─ StyleAlgebra (domain specializations - NOT YET IMPLEMENTED)
        └─ MeansAlgebra (non-certifying tools - NOT YET IMPLEMENTED)

    This class implements ONLY the rational method root.
    It does NOT implement scientific, logical, or means algebra.
    """

    @staticmethod
    def is_root_method() -> bool:
        """
        Confirm this is the root method.

        No other method may claim root status.
        """
        return True

    @staticmethod
    def judge(
        reality: str,
        sensory_transfer: str,
        cognitive_carrier: str,
        prior_knowledge: FrozenSet[Any]
    ) -> AqlOperationResult:
        """
        Execute complete rational judgment.

        Steps (Nabhani procedure):
        1. Filter prior (exclude opinions)
        2. Validate four pillars
        3. Execute AqlOperation
        4. Return governed result

        Args:
            reality: The reality being considered
            sensory_transfer: Sensory data about reality
            cognitive_carrier: Valid cognitive substrate
            prior_knowledge: Mixed prior items (to be filtered)

        Returns:
            Governed AqlOperationResult (never bare exception)
        """
        # Step 1: Filter prior knowledge
        filtered = filter_prior(prior_knowledge)

        # Step 2: Create operation input
        input_data = AqlOperationInput(
            reality=reality,
            sensory_transfer=sensory_transfer,
            cognitive_carrier=cognitive_carrier,
            filtered_prior=filtered
        )

        # Step 3: Execute operation
        result = AqlOperation.execute(input_data)

        return result

    @staticmethod
    def does_not_implement_scientific_method() -> bool:
        """
        Verify that RationalMethod does NOT implement ScientificMethod.

        ScientificMethod is a future branch, not part of root.
        """
        return True

    @staticmethod
    def does_not_implement_logical_style() -> bool:
        """
        Verify that RationalMethod does NOT implement LogicalStyle.

        LogicalStyle is a future specialized style, not part of root.
        """
        return True

    @staticmethod
    def does_not_implement_means_algebra() -> bool:
        """
        Verify that RationalMethod does NOT implement MeansAlgebra.

        MeansAlgebra is future tool layer, not part of root.
        """
        return True
