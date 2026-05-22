"""
LafziTraceGate - بوابة الأثر اللفظي

Gate for verifying LafziTrace conditions before Lafzi processing.

Critical Law:
    لا مدلول لفظي بلا أثر لفظي
    No LafziMadlul execution without LafziTrace.

12 Governance Laws:
    1. No LafziTrace without LafziMadlul registration
    2. No LafziTrace without StyleSpec(LAFZI_DALALI)
    3. No LafziTrace without NeutralBinding
    4. No LafziTrace without PriorInformation
    5. LafziTrace preserves trace_id
    6. LafziTrace preserves residuals
    7. LafziTrace does not create meaning
    8. LafziTrace does not issue HUKM
    9. LafziTrace does not create Dal
    10. LafziTrace does not create Madlul
    11. LafziTrace does not create Dalalah
    12. LafziTrace does not raise PredicateRank
    13. UNKNOWN trace type becomes residual, not exception

What LafziTraceGate Does:
    - Verifies LafziMadlul registration exists
    - Verifies StyleSpec(LAFZI_DALALI) exists
    - Verifies NeutralBinding exists
    - Verifies PriorInformation exists
    - Preserves trace_id
    - Preserves residuals
    - Returns governed failures (not exceptions)

What LafziTraceGate Does NOT Do:
    - Does NOT create meaning
    - Does NOT create Dal
    - Does NOT create Madlul
    - Does NOT create Dalalah
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from gfa.methods.lafzi_registration import (
    LafziStyleRegistration,
    LafziRegistrationResult,
)
from gfa.methods.styles import StyleSpec, ThinkingDomain

from .lafzi_trace import LafziTrace, LafziTraceResult
from .lafzi_trace_type import LafziTraceType
from .residual_taxonomy import (
    LafziTraceResidual,
    make_missing_registration_residual,
    make_missing_style_spec_residual,
    make_wrong_domain_residual,
    make_missing_neutral_binding_residual,
    make_missing_prior_information_residual,
    make_trace_not_preserved_residual,
    make_unknown_trace_type_residual,
)


@dataclass(frozen=True)
class LafziTraceFailure:
    """
    Failure from LafziTrace gate.

    Contains:
        - residual: The specific failure residual
        - trace_id: Preserved trace identifier
    """

    residual: LafziTraceResidual
    trace_id: Optional[str] = None

    def __str__(self) -> str:
        return f"LafziTraceFailure: {self.residual}"

    def __repr__(self) -> str:
        return f"LafziTraceFailure(kind={self.residual.kind.value})"


class LafziTraceGate:
    """
    Gate for verifying LafziTrace conditions.

    This gate enforces 12 governance laws before allowing
    Lafzi processing to proceed.

    Critical Properties:
        - Requires LafziMadlul registration
        - Requires StyleSpec(LAFZI_DALALI)
        - Requires NeutralBinding
        - Requires PriorInformation
        - Preserves trace_id
        - Preserves residuals
        - Does NOT create meaning
        - Does NOT create Dal/Madlul/Dalalah
        - Does NOT issue HUKM
        - Does NOT raise PredicateRank
        - UNKNOWN trace type becomes residual
    """

    def __init__(self, registration_result: LafziRegistrationResult):
        """
        Initialize LafziTraceGate with registration result.

        Args:
            registration_result: Result from LafziStyleRegistration

        Critical:
            Registration must be successful before trace gate can operate.
        """
        if not registration_result.success:
            raise ValueError(
                "LafziTraceGate requires successful LafziMadlul registration"
            )

        self.registration_result = registration_result
        self.style_spec = registration_result.governance_contract.style_spec
        self.neutral_binding_input = registration_result.governance_contract.neutral_binding_input

    def verify_registration(self) -> bool:
        """
        Law 1: No LafziTrace without LafziMadlul registration.

        Returns True if registration successful.
        """
        return self.registration_result.success

    def verify_style_spec(self) -> bool:
        """
        Law 2: No LafziTrace without StyleSpec(LAFZI_DALALI).

        Returns True if StyleSpec exists and domain is LAFZI_DALALI.
        """
        return (
            self.style_spec is not None
            and self.style_spec.get_domain() == ThinkingDomain.LAFZI_DALALI
        )

    def verify_neutral_binding(self) -> bool:
        """
        Law 3: No LafziTrace without NeutralBinding.

        Returns True if NeutralBindingInput exists.
        """
        return self.neutral_binding_input is not None

    def verify_prior_information(self) -> bool:
        """
        Law 4: No LafziTrace without PriorInformation.

        Returns True if PriorInformation exists.
        """
        aql_input = self.neutral_binding_input.aql_input
        filtered_prior = aql_input.filtered_prior
        return (
            filtered_prior is not None
            and filtered_prior.has_valid_information()
        )

    def preserves_trace_id(self, trace_id: Optional[str]) -> bool:
        """
        Law 5: LafziTrace preserves trace_id.

        Returns True if trace_id exists.
        """
        return trace_id is not None

    def preserves_residuals(self) -> bool:
        """
        Law 6: LafziTrace preserves residuals.

        Returns True (residuals always preserved).
        """
        return isinstance(self.neutral_binding_input.residuals, tuple)

    def does_not_create_meaning(self) -> bool:
        """
        Law 7: LafziTrace does not create meaning.

        Returns True always (by construction).
        """
        return True

    def does_not_issue_hukm(self) -> bool:
        """
        Law 8: LafziTrace does not issue HUKM.

        Returns True always (by construction).
        """
        return True

    def does_not_create_dal(self) -> bool:
        """
        Law 9: LafziTrace does not create Dal.

        Returns True always (by construction).
        """
        return True

    def does_not_create_madlul(self) -> bool:
        """
        Law 10: LafziTrace does not create Madlul.

        Returns True always (by construction).
        """
        return True

    def does_not_create_dalalah(self) -> bool:
        """
        Law 11: LafziTrace does not create Dalalah.

        Returns True always (by construction).
        """
        return True

    def does_not_raise_predicate_rank(self) -> bool:
        """
        Law 12: LafziTrace does not raise PredicateRank.

        Returns True always (by construction).
        """
        return True

    def process_trace(
        self,
        trace_id: str,
        trace_type: LafziTraceType,
        trace_content: str,
    ) -> LafziTraceResult:
        """
        Process a linguistic trace through the gate.

        Args:
            trace_id: Unique trace identifier
            trace_type: Type of trace (acoustic, written, etc.)
            trace_content: The actual trace data

        Returns:
            LafziTraceResult with either success or governed failure

        Critical:
            - UNKNOWN trace type becomes residual, not exception
            - All failures are governed (no bare exceptions)
        """
        # Law 1: Verify registration
        if not self.verify_registration():
            residual = make_missing_registration_residual(trace_id)
            failure = LafziTraceFailure(residual=residual, trace_id=trace_id)
            return LafziTraceResult(success=False, failure=failure)

        # Law 2: Verify StyleSpec
        if not self.verify_style_spec():
            if self.style_spec is None:
                residual = make_missing_style_spec_residual(trace_id)
            else:
                residual = make_wrong_domain_residual(
                    actual_domain=self.style_spec.get_domain().value,
                    trace_id=trace_id,
                )
            failure = LafziTraceFailure(residual=residual, trace_id=trace_id)
            return LafziTraceResult(success=False, failure=failure)

        # Law 3: Verify NeutralBinding
        if not self.verify_neutral_binding():
            residual = make_missing_neutral_binding_residual(trace_id)
            failure = LafziTraceFailure(residual=residual, trace_id=trace_id)
            return LafziTraceResult(success=False, failure=failure)

        # Law 4: Verify PriorInformation
        if not self.verify_prior_information():
            residual = make_missing_prior_information_residual(trace_id)
            failure = LafziTraceFailure(residual=residual, trace_id=trace_id)
            return LafziTraceResult(success=False, failure=failure)

        # Law 5: Verify trace_id preservation
        if not self.preserves_trace_id(trace_id):
            residual = make_trace_not_preserved_residual(trace_id)
            failure = LafziTraceFailure(residual=residual, trace_id=trace_id)
            return LafziTraceResult(success=False, failure=failure)

        # Create base trace
        trace = LafziTrace(
            trace_id=trace_id,
            trace_type=trace_type,
            trace_content=trace_content,
            residuals=(),
        )

        # Law 13: UNKNOWN trace type becomes residual
        if trace_type == LafziTraceType.UNKNOWN:
            residual = make_unknown_trace_type_residual(trace_id)
            trace = trace.with_residual(residual)

        # Success
        return LafziTraceResult(success=True, trace=trace)

    def __str__(self) -> str:
        domain = self.style_spec.get_domain().value if self.style_spec else "None"
        return f"LafziTraceGate[domain={domain}]"

    def __repr__(self) -> str:
        return f"LafziTraceGate(registered={self.verify_registration()})"
