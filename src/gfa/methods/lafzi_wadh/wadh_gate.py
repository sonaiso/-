"""
WadhGate - بوابة الوضع

Critical Law:
    الوضع يُرخِّص دعوى، لا يُدخِل معنى
    Wadh licenses a claim, does NOT inject meaning.

WadhGate admits or blocks a WadhClaim based on evidence, transmission,
source, scope, MawduLahStructure, rank, and residuals.

What WadhGate Does:
    - Admits or blocks WadhClaim
    - Validates WadhEvidence
    - Validates transmission requirements
    - Validates source sufficiency
    - Validates or residualizes scope
    - Validates MawduLahStructure
    - Preserves binding trace
    - Accumulates residuals
    - Returns governed failures

What WadhGate Does NOT Do:
    - Does NOT create full Dalālah
    - Does NOT create external meaning
    - Does NOT classify Mutabaqah/Tadammun/Iltizam
    - Does NOT classify Haqiqah/Majaz/Naql
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank to CERTIFIED
    - Does NOT implement learning
    - Does NOT implement upward transitions
    - Does NOT implement downward decomposition

Position in Architecture:
    DalMadlulBindingCandidate (PR-L4, certified)
    └── WadhGeometry (PR-L5A)
        ├── WadhEvidence
        ├── WadhClaim
        └── WadhGate (PR-L5B) ← THIS MODULE
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from gfa.methods.lafzi_binding import DalMadlulBindingCandidate
from .wadh_evidence import WadhEvidence
from .wadh_source import WadhSource, WadhSourceKind
from .wadh_transmission_mode import WadhTransmissionMode, WadhTransmissionKind
from .wadh_scope import WadhScope, WadhScopeKind
from .mawdu_lah_structure import MawduLahStructure
from .wadh_claim import WadhClaim
from .residual_taxonomy import (
    WadhResidual,
    make_unknown_source_residual,
    make_unknown_transmission_residual,
    make_unknown_scope_residual,
    make_reason_alone_residual,
    make_binding_trace_lost_residual,
)
from .wadh_gate_result import WadhGateResult, WadhGateFailure


@dataclass(frozen=True)
class WadhGate:
    """
    Gate for admitting or blocking WadhClaim.

    WadhGate admission means:
        - WadhClaim admitted

    It does NOT mean:
        - meaning certified
        - full Dalālah completed
        - Mutabaqah/Tadammun/Iltizam classified
        - Haqiqah/Majaz/Naql classified
        - HUKM issued

    Critical Laws:
        1. Requires DalMadlulBindingCandidate
        2. Requires WadhEvidence
        3. Requires WadhSource
        4. Requires WadhTransmissionMode
        5. Requires or residualizes WadhScope
        6. Requires MawduLahStructure
        7. Unknown source becomes residual
        8. Unknown transmission becomes residual
        9. Unknown scope becomes residual
        10. Lexicon report permits WadhClaim, not meaning
        11. Usage attestation permits WadhClaim, not UsageGate
        12. Explicit stipulation permits WadhClaim, not full Dalālah
        13. Reason alone cannot license Arabic Wadh
        14. Preserves binding trace
        15. Preserves residuals
        16. Does not raise PredicateRank to CERTIFIED
        17. Does not create external meaning
        18. Does not issue HUKM
        19. Does not classify Mutabaqah/Tadammun/Iltizam
        20. Does not classify Haqiqah/Majaz/Naql
        21. Returns governed failures, not bare exceptions
    """

    strict_mode: bool = True

    def admit_wadh_claim(
        self,
        binding_candidate: DalMadlulBindingCandidate,
        wadh_evidence: WadhEvidence,
        mawdu_lah: MawduLahStructure,
    ) -> WadhGateResult:
        """
        Admit or block WadhClaim based on evidence and requirements.

        Critical Law: Admission means WadhClaim admitted, NOT meaning certified.

        Args:
            binding_candidate: Required DalMadlulBindingCandidate
            wadh_evidence: Required WadhEvidence
            mawdu_lah: Required MawduLahStructure

        Returns:
            WadhGateResult with admitted claim or governed failure
        """
        residuals: list[WadhResidual] = []
        missing: list[str] = []

        # Law 1: Requires DalMadlulBindingCandidate
        if not binding_candidate:
            missing.append("DalMadlulBindingCandidate")
            return self._make_failure(
                "Missing DalMadlulBindingCandidate",
                tuple(missing),
                tuple(residuals),
                "",
            )

        # Extract binding_trace_id
        binding_trace_id = binding_candidate.trace_id

        # Law 14: Preserves binding trace
        if not binding_trace_id:
            residual = make_binding_trace_lost_residual()
            residuals.append(residual)
            missing.append("binding_trace_id")

        # Law 2: Requires WadhEvidence
        if not wadh_evidence:
            missing.append("WadhEvidence")
            return self._make_failure(
                "Missing WadhEvidence",
                tuple(missing),
                tuple(residuals),
                binding_trace_id,
            )

        # Law 3: Requires WadhSource
        if not wadh_evidence.source:
            missing.append("WadhSource")
            return self._make_failure(
                "Missing WadhSource",
                tuple(missing),
                tuple(residuals),
                binding_trace_id,
            )

        # Law 7: Unknown source becomes residual
        if not wadh_evidence.source.is_known:
            residual = make_unknown_source_residual(
                f"Source kind: {wadh_evidence.source.kind.value}"
            )
            residuals.append(residual)
            missing.append("known_source")

        # Law 4: Requires WadhTransmissionMode
        if not wadh_evidence.transmission_mode:
            missing.append("WadhTransmissionMode")
            return self._make_failure(
                "Missing WadhTransmissionMode",
                tuple(missing),
                tuple(residuals),
                binding_trace_id,
            )

        # Law 8: Unknown transmission becomes residual
        if not wadh_evidence.transmission_mode.is_known:
            residual = make_unknown_transmission_residual(
                f"Transmission kind: {wadh_evidence.transmission_mode.kind.value}"
            )
            residuals.append(residual)
            missing.append("known_transmission")

        # Law 13: Reason alone cannot license Arabic Wadh
        if wadh_evidence.source.kind == WadhSourceKind.REASON_INFERENCE:
            if not wadh_evidence.is_transmitted:
                residual = make_reason_alone_residual(
                    "Reason alone insufficient for Arabic Wadh (requires transmission)"
                )
                residuals.append(residual)
                missing.append("transmitted_evidence")

        # Law 5: Requires or residualizes WadhScope
        if not wadh_evidence.scope:
            missing.append("WadhScope")
            return self._make_failure(
                "Missing WadhScope",
                tuple(missing),
                tuple(residuals),
                binding_trace_id,
            )

        # Law 9: Unknown scope becomes residual (but doesn't block)
        if not wadh_evidence.scope.is_known:
            residual = make_unknown_scope_residual(
                f"Scope kind: {wadh_evidence.scope.kind.value}"
            )
            residuals.append(residual)
            # Note: Unknown scope residualizes but doesn't add to missing

        # Law 6: Requires MawduLahStructure
        if not mawdu_lah:
            missing.append("MawduLahStructure")
            return self._make_failure(
                "Missing MawduLahStructure",
                tuple(missing),
                tuple(residuals),
                binding_trace_id,
            )

        # Accumulate residuals from evidence
        residuals.extend(wadh_evidence.residuals)

        # Check if any blocking residuals exist
        has_blockers = any(r.is_blocker for r in residuals)

        # If strict mode and has missing requirements or blockers, fail
        if self.strict_mode and (missing or has_blockers):
            reason = "WadhGate requirements not met" if missing else "Blocking residuals present"
            return self._make_failure(
                reason,
                tuple(missing),
                tuple(residuals),
                binding_trace_id,
            )

        # Create WadhClaim
        claim = WadhClaim(
            wadh_evidence=wadh_evidence,
            mawdu_lah=mawdu_lah,
            binding_trace_id=binding_trace_id,
            residuals=tuple(residuals),
        )

        # Return admitted result
        return WadhGateResult(
            admitted=True,
            claim=claim,
        )

    def _make_failure(
        self,
        reason: str,
        missing_requirements: Tuple[str, ...],
        residuals: Tuple[WadhResidual, ...],
        binding_trace_id: str,
    ) -> WadhGateResult:
        """
        Create governed failure result.

        Critical Law: No bare exceptions, always governed failure.
        """
        failure = WadhGateFailure(
            reason=reason,
            missing_requirements=missing_requirements,
            residuals=residuals,
            binding_trace_id=binding_trace_id,
        )
        return WadhGateResult(
            admitted=False,
            failure=failure,
        )
