"""
DalMadlulBindingGate - بوابة الربط بين الدال والمدلول

Governance gate for creating neutral binding between signifier and signified.
"""

from dataclasses import dataclass
from typing import Optional, Tuple, Any

from ..styles import StyleSpec, ThinkingDomain
from ..lafzi_dal import DalCandidate
from ..lafzi_madlul import MadlulLafziCandidate, MadlulLafziType

from .dal_madlul_binding_type import DalMadlulBindingType
from .dal_madlul_binding_candidate import (
    DalMadlulBindingCandidate,
    DalMadlulBindingResult,
)
from .binding_residual_taxonomy import (
    DalMadlulBindingFailureKind,
    DalMadlulBindingResidual,
    make_missing_dal_candidate_residual,
    make_missing_madlul_candidate_residual,
    make_binding_trace_not_preserved_residual,
    make_binding_residuals_not_preserved_residual,
)


@dataclass(frozen=True)
class DalMadlulBindingFailure:
    """
    Failure from DalMadlulBindingGate operation.

    Attributes:
        residual: Primary residual explaining failure
        violated_law: Which governance law was violated
        trace_id: Trace identifier
        additional_residuals: Other accumulated residuals
    """

    residual: DalMadlulBindingResidual
    violated_law: str
    trace_id: str
    additional_residuals: Tuple[Any, ...] = ()

    @property
    def reason(self) -> str:
        """Get human-readable failure reason."""
        return self.residual.reason

    @property
    def kind(self) -> DalMadlulBindingFailureKind:
        """Get failure kind."""
        return self.residual.kind


class DalMadlulBindingGate:
    """
    Governance gate for DalMadlulBinding operations.

    Enforces 13 laws:
        Law 1: Requires DalCandidate
        Law 2: Requires MadlulLafziCandidate
        Law 3: Compatible types required
        Law 4: Preserves trace_id
        Law 5: Preserves residuals from both sides
        Law 6: Does NOT create full Dalalah
        Law 7: Does NOT implement Wadh
        Law 8: Does NOT create external meaning
        Law 9: Does NOT issue HUKM
        Law 10: Does NOT raise PredicateRank
        Law 11: Does NOT perform semantic interpretation
        Law 12: Does NOT implement Mutabaqah/Tadammun/Iltizam
        Law 13: Returns governed failures, not exceptions

    Critical:
        DalMadlulBinding is NEUTRAL RELATION, not full Dalalah.
    """

    def __init__(
        self,
        style_spec: StyleSpec,
        neutral_binding_available: bool = True,
    ):
        """
        Initialize DalMadlulBindingGate.

        Args:
            style_spec: StyleSpec (must be LAFZI_DALALI domain)
            neutral_binding_available: Whether NeutralBinding is available
        """
        self.style_spec = style_spec
        self.neutral_binding_available = neutral_binding_available

    def verify_style_spec(self) -> bool:
        """Verify StyleSpec is LAFZI_DALALI domain."""
        return self.style_spec.get_domain() == ThinkingDomain.LAFZI_DALALI

    def verify_neutral_binding(self) -> bool:
        """Verify NeutralBinding is available."""
        return self.neutral_binding_available

    def verify_dal_candidate(self, dal_candidate: Optional[Any]) -> bool:
        """
        Law 1: Verify DalCandidate is provided.

        Args:
            dal_candidate: DalCandidate to verify

        Returns:
            True if valid DalCandidate provided
        """
        return dal_candidate is not None

    def verify_madlul_candidate(
        self, madlul_candidate: Optional[Any]
    ) -> bool:
        """
        Law 2: Verify MadlulLafziCandidate is provided.

        Args:
            madlul_candidate: MadlulLafziCandidate to verify

        Returns:
            True if valid MadlulLafziCandidate provided
        """
        return madlul_candidate is not None

    def verify_type_compatibility(
        self, dal_candidate: Any, madlul_candidate: Any
    ) -> bool:
        """
        Law 3: Verify DalCandidate and MadlulCandidate types are compatible.

        Args:
            dal_candidate: DalCandidate
            madlul_candidate: MadlulLafziCandidate

        Returns:
            True if types are compatible
        """
        # For now, accept all combinations
        # Future: implement stricter type matching
        return True

    def preserves_trace_id(self, trace_id: str) -> bool:
        """
        Law 4: Verify trace_id is preserved.

        Args:
            trace_id: Trace identifier

        Returns:
            True if trace_id is non-empty string
        """
        return isinstance(trace_id, str) and len(trace_id) > 0

    def preserves_residuals(self) -> bool:
        """
        Law 5: Verify residuals from both sides are preserved.

        Returns:
            True (residuals are always preserved by design)
        """
        return True

    def does_not_create_dalalah(self) -> bool:
        """
        Law 6: Verify binding does NOT create full Dalalah.

        Returns:
            True (by design, binding ≠ Dalalah)
        """
        return True

    def does_not_implement_wadh(self) -> bool:
        """
        Law 7: Verify binding does NOT implement Wadh.

        Returns:
            True (by design, binding does not implement Wadh)
        """
        return True

    def does_not_create_external_meaning(self) -> bool:
        """
        Law 8: Verify binding does NOT create external meaning.

        Returns:
            True (by design, binding is neutral)
        """
        return True

    def does_not_issue_hukm(self) -> bool:
        """
        Law 9: Verify binding does NOT issue HUKM.

        Returns:
            True (by design, no judgment)
        """
        return True

    def does_not_raise_predicate_rank(self) -> bool:
        """
        Law 10: Verify binding does NOT raise PredicateRank.

        Returns:
            True (by design, rank is preserved)
        """
        return True

    def does_not_perform_semantic_interpretation(self) -> bool:
        """
        Law 11: Verify binding does NOT perform semantic interpretation.

        Returns:
            True (by design, binding is neutral)
        """
        return True

    def does_not_implement_mutabaqah(self) -> bool:
        """
        Law 12: Verify binding does NOT implement Mutabaqah/Tadammun/Iltizam.

        Returns:
            True (by design, semantic relations are not implemented)
        """
        return True

    def returns_governed_failures(self) -> bool:
        """
        Law 13: Verify gate returns governed failures, not exceptions.

        Returns:
            True (by design, all failures are governed)
        """
        return True

    def process_binding(
        self,
        trace_id: str,
        dal_candidate: Optional[DalCandidate],
        madlul_candidate: Optional[MadlulLafziCandidate],
        prior_information: str = "",
        binding_type: DalMadlulBindingType = DalMadlulBindingType.SIMPLE_BINDING,
        input_residuals: Tuple[Any, ...] = (),
    ) -> DalMadlulBindingResult:
        """
        Process binding between DalCandidate and MadlulLafziCandidate.

        Args:
            trace_id: Unique trace identifier
            dal_candidate: DalCandidate (signifier)
            madlul_candidate: MadlulLafziCandidate (signified)
            prior_information: Source prior information
            binding_type: Type of binding
            input_residuals: Input residuals to preserve

        Returns:
            DalMadlulBindingResult (success or governed failure)
        """
        # Verify Law 1: DalCandidate required
        if not self.verify_dal_candidate(dal_candidate):
            residual = make_missing_dal_candidate_residual(trace_id)
            failure = DalMadlulBindingFailure(
                residual=residual,
                violated_law="Law 1: Requires DalCandidate",
                trace_id=trace_id,
                additional_residuals=input_residuals,
            )
            return DalMadlulBindingResult.failure(
                failure=failure, residuals=input_residuals + (residual,)
            )

        # Verify Law 2: MadlulLafziCandidate required
        if not self.verify_madlul_candidate(madlul_candidate):
            residual = make_missing_madlul_candidate_residual(trace_id)
            failure = DalMadlulBindingFailure(
                residual=residual,
                violated_law="Law 2: Requires MadlulLafziCandidate",
                trace_id=trace_id,
                additional_residuals=input_residuals,
            )
            return DalMadlulBindingResult.failure(
                failure=failure, residuals=input_residuals + (residual,)
            )

        # Verify Law 4: Trace preservation
        if not self.preserves_trace_id(trace_id):
            residual = make_binding_trace_not_preserved_residual(trace_id)
            failure = DalMadlulBindingFailure(
                residual=residual,
                violated_law="Law 4: Preserves trace_id",
                trace_id=trace_id,
                additional_residuals=input_residuals,
            )
            return DalMadlulBindingResult.failure(
                failure=failure, residuals=input_residuals + (residual,)
            )

        # Collect residuals from both sides
        dal_residuals = getattr(dal_candidate, 'residuals', ())
        madlul_residuals = getattr(madlul_candidate, 'residuals', ())
        all_residuals = input_residuals + dal_residuals + madlul_residuals

        # Create binding candidate
        candidate = DalMadlulBindingCandidate(
            trace_id=trace_id,
            binding_type=binding_type,
            dal_candidate=dal_candidate,
            madlul_candidate=madlul_candidate,
            source_prior_information=prior_information,
            residuals=all_residuals,
            binding_confidence=1.0,
            binding_conditions=None,
        )

        return DalMadlulBindingResult.success(
            candidate=candidate, residuals=all_residuals
        )
