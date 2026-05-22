"""
DalGate - بوابة الدال

Gate for verifying DalCandidate conditions before Lafzi signification.

Critical Law:
    الدال وحده حامل لفظي مرشح، لا معنى
    Dāl-alone is a signifier candidate, not meaning, not Madlul, not Dalalah.

14 Governance Laws:
    1. No DalCandidate without LafziTrace
    2. No DalCandidate without LafziMadlul registration
    3. No DalCandidate without StyleSpec(LAFZI_DALALI)
    4. No DalCandidate without NeutralBinding
    5. DalCandidate preserves trace_id
    6. DalCandidate preserves residuals
    7. DalCandidate does not create meaning
    8. DalCandidate does not create Madlul
    9. DalCandidate does not create Dalalah
    10. DalCandidate does not implement Wadh
    11. DalCandidate does not issue HUKM
    12. DalCandidate does not raise PredicateRank
    13. UNKNOWN signifier type becomes residual, not exception
    14. DalGate returns governed failure, not exception

What DalGate Does:
    - Verifies LafziTrace exists
    - Verifies LafziMadlul registration exists
    - Verifies StyleSpec(LAFZI_DALALI) exists
    - Verifies NeutralBinding exists
    - Maps LafziTraceType to DalType
    - Preserves trace_id
    - Preserves residuals
    - Returns governed failures (not exceptions)

What DalGate Does NOT Do:
    - Does NOT create meaning
    - Does NOT create Madlul
    - Does NOT create Dalalah
    - Does NOT implement Wadh
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from gfa.methods.lafzi_trace import LafziTrace, LafziTraceType
from gfa.methods.styles import StyleSpec, ThinkingDomain

from .dal_candidate import DalCandidate, DalResult
from .dal_type import DalType
from .residual_taxonomy import (
    DalResidual,
    make_missing_lafzi_trace_residual,
    make_missing_registration_residual,
    make_missing_style_spec_residual,
    make_wrong_domain_residual,
    make_missing_neutral_binding_residual,
    make_trace_not_preserved_residual,
    make_residuals_not_preserved_residual,
    make_unknown_dal_type_residual,
)


@dataclass(frozen=True)
class DalFailure:
    """
    Failure from DalGate.

    Contains:
        - residual: The specific failure residual
        - trace_id: Preserved trace identifier
    """

    residual: DalResidual
    trace_id: Optional[str] = None

    def __str__(self) -> str:
        return f"DalFailure: {self.residual}"

    def __repr__(self) -> str:
        return f"DalFailure(kind={self.residual.kind.value})"


class DalGate:
    """
    Gate for verifying DalCandidate conditions.

    This gate enforces 14 governance laws before allowing
    signifier candidate creation.

    Critical Properties:
        - Requires LafziTrace
        - Requires LafziMadlul registration
        - Requires StyleSpec(LAFZI_DALALI)
        - Requires NeutralBinding
        - Preserves trace_id
        - Preserves residuals
        - Does NOT create meaning
        - Does NOT create Madlul
        - Does NOT create Dalalah
        - Does NOT implement Wadh
        - Does NOT issue HUKM
        - Does NOT raise PredicateRank
        - UNKNOWN signifier type becomes residual
    """

    def __init__(
        self,
        style_spec: StyleSpec,
        neutral_binding_available: bool,
        registration_successful: bool
    ):
        """
        Initialize DalGate with governance context.

        Args:
            style_spec: StyleSpec for domain verification
            neutral_binding_available: Whether NeutralBinding exists
            registration_successful: Whether LafziMadlul registration succeeded

        Critical:
            All three dependencies must be satisfied.
        """
        self.style_spec = style_spec
        self.neutral_binding_available = neutral_binding_available
        self.registration_successful = registration_successful

    def verify_registration(self) -> bool:
        """
        Law 2: No DalCandidate without LafziMadlul registration.

        Returns True if registration successful.
        """
        return self.registration_successful

    def verify_style_spec(self) -> bool:
        """
        Law 3: No DalCandidate without StyleSpec(LAFZI_DALALI).

        Returns True if StyleSpec exists and domain is LAFZI_DALALI.
        """
        return (
            self.style_spec is not None
            and self.style_spec.get_domain() == ThinkingDomain.LAFZI_DALALI
        )

    def verify_neutral_binding(self) -> bool:
        """
        Law 4: No DalCandidate without NeutralBinding.

        Returns True if NeutralBinding exists.
        """
        return self.neutral_binding_available

    def preserves_trace_id(self, trace_id: Optional[str]) -> bool:
        """
        Law 5: DalCandidate preserves trace_id.

        Returns True if trace_id exists.
        """
        return trace_id is not None

    def preserves_residuals(self) -> bool:
        """
        Law 6: DalCandidate preserves residuals.

        Returns True always (residuals always preserved).
        """
        return True

    def does_not_create_meaning(self) -> bool:
        """
        Law 7: DalCandidate does not create meaning.

        Returns True always (by construction).
        """
        return True

    def does_not_create_madlul(self) -> bool:
        """
        Law 8: DalCandidate does not create Madlul.

        Returns True always (by construction).
        """
        return True

    def does_not_create_dalalah(self) -> bool:
        """
        Law 9: DalCandidate does not create Dalalah.

        Returns True always (by construction).
        """
        return True

    def does_not_implement_wadh(self) -> bool:
        """
        Law 10: DalCandidate does not implement Wadh.

        Returns True always (by construction).
        """
        return True

    def does_not_issue_hukm(self) -> bool:
        """
        Law 11: DalCandidate does not issue HUKM.

        Returns True always (by construction).
        """
        return True

    def does_not_raise_predicate_rank(self) -> bool:
        """
        Law 12: DalCandidate does not raise PredicateRank.

        Returns True always (by construction).
        """
        return True

    def map_trace_type_to_dal_type(self, trace_type: LafziTraceType) -> DalType:
        """
        Map LafziTraceType to DalType.

        This mapping preserves modality across trace → signifier.

        Mapping:
            ACOUSTIC → SOUND_SIGNIFIER
            WRITTEN → WRITTEN_SIGNIFIER
            UNICODE → WRITTEN_SIGNIFIER
            ORTHOGRAPHIC → ORTHOGRAPHIC_SIGNIFIER
            PHONOLOGICAL → SOUND_SIGNIFIER
            SYMBOLIC → SYMBOLIC_SIGNIFIER
            UNKNOWN → UNKNOWN_SIGNIFIER
        """
        mapping = {
            LafziTraceType.ACOUSTIC: DalType.SOUND_SIGNIFIER,
            LafziTraceType.WRITTEN: DalType.WRITTEN_SIGNIFIER,
            LafziTraceType.UNICODE: DalType.WRITTEN_SIGNIFIER,
            LafziTraceType.ORTHOGRAPHIC: DalType.ORTHOGRAPHIC_SIGNIFIER,
            LafziTraceType.PHONOLOGICAL: DalType.SOUND_SIGNIFIER,
            LafziTraceType.SYMBOLIC: DalType.SYMBOLIC_SIGNIFIER,
            LafziTraceType.UNKNOWN: DalType.UNKNOWN_SIGNIFIER,
        }
        return mapping.get(trace_type, DalType.UNKNOWN_SIGNIFIER)

    def process_trace(self, lafzi_trace: LafziTrace) -> DalResult:
        """
        Process a LafziTrace to create DalCandidate.

        Args:
            lafzi_trace: The linguistic trace to process

        Returns:
            DalResult with either success or governed failure

        Critical:
            - UNKNOWN signifier type becomes residual, not exception
            - All failures are governed (no bare exceptions)
        """
        # Law 1: Verify LafziTrace exists
        if lafzi_trace is None:
            residual = make_missing_lafzi_trace_residual()
            failure = DalFailure(residual=residual)
            return DalResult(success=False, failure=failure)

        trace_id = lafzi_trace.trace_id

        # Law 2: Verify registration
        if not self.verify_registration():
            residual = make_missing_registration_residual(trace_id)
            failure = DalFailure(residual=residual, trace_id=trace_id)
            return DalResult(success=False, failure=failure)

        # Law 3: Verify StyleSpec
        if not self.verify_style_spec():
            if self.style_spec is None:
                residual = make_missing_style_spec_residual(trace_id)
            else:
                residual = make_wrong_domain_residual(
                    actual_domain=self.style_spec.get_domain().value,
                    trace_id=trace_id,
                )
            failure = DalFailure(residual=residual, trace_id=trace_id)
            return DalResult(success=False, failure=failure)

        # Law 4: Verify NeutralBinding
        if not self.verify_neutral_binding():
            residual = make_missing_neutral_binding_residual(trace_id)
            failure = DalFailure(residual=residual, trace_id=trace_id)
            return DalResult(success=False, failure=failure)

        # Law 5: Verify trace_id preservation
        if not self.preserves_trace_id(trace_id):
            residual = make_trace_not_preserved_residual(trace_id)
            failure = DalFailure(residual=residual, trace_id=trace_id)
            return DalResult(success=False, failure=failure)

        # Map trace type to dal type
        dal_type = self.map_trace_type_to_dal_type(lafzi_trace.trace_type)

        # Create base candidate
        candidate = DalCandidate(
            trace_id=trace_id,
            signifier_form=lafzi_trace.trace_content,
            dal_type=dal_type,
            residuals=lafzi_trace.residuals,  # Law 6: Preserve residuals
        )

        # Law 13: UNKNOWN signifier type becomes residual
        if dal_type == DalType.UNKNOWN_SIGNIFIER:
            residual = make_unknown_dal_type_residual(trace_id)
            candidate = candidate.with_residual(residual)

        # Success
        return DalResult(success=True, candidate=candidate)

    def __str__(self) -> str:
        domain = self.style_spec.get_domain().value if self.style_spec else "None"
        return f"DalGate[domain={domain}, registered={self.registration_successful}]"

    def __repr__(self) -> str:
        return (
            f"DalGate(registered={self.registration_successful}, "
            f"neutral_binding={self.neutral_binding_available})"
        )
