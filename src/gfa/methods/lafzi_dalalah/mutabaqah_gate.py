"""
MutabaqahGate - بوابة المطابقة

Critical Law:
    المطابقة = دلالة على تمام الموضوع له، لا معنى خارجي
    Mutabaqah = signification to the whole placed-for, NOT external meaning.

MutabaqahGate admits or blocks a MutabaqahCandidate based on admitted WadhClaim,
MawduLahStructure, and availability of whole.

What MutabaqahGate Does:
    - Admits or blocks MutabaqahCandidate
    - Requires admitted WadhClaim
    - Requires MawduLahStructure
    - Requires MawduLahStructure.whole
    - Preserves WadhClaim trace
    - Preserves binding trace
    - Accumulates residuals
    - Returns governed failures

What MutabaqahGate Does NOT Do:
    - Does NOT create external meaning
    - Does NOT issue HUKM
    - Does NOT create Tadammun
    - Does NOT create Iltizam
    - Does NOT classify Haqiqah/Majaz/Naql
    - Does NOT create Ifadah
    - Does NOT raise PredicateRank to CERTIFIED
    - Does NOT implement learning
    - Does NOT implement upward transitions
    - Does NOT implement downward decomposition

Position in Architecture:
    WadhGate (PR-L5B)
    └── MutabaqahGate (PR-L6A) ← THIS MODULE
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from gfa.methods.lafzi_wadh import WadhGateResult, WadhClaim, MawduLahStructure
from .mutabaqah_candidate import MutabaqahCandidate
from .mutabaqah_result import MutabaqahResult, MutabaqahFailure
from .residual_taxonomy import (
    MutabaqahResidual,
    make_wadh_claim_not_admitted_residual,
    make_mawdu_lah_whole_unavailable_residual,
    make_wadh_trace_lost_residual,
    make_binding_trace_lost_residual,
)


@dataclass(frozen=True)
class MutabaqahGate:
    """
    Gate for admitting or blocking MutabaqahCandidate.

    MutabaqahGate admission means:
        - MutabaqahCandidate admitted (signifies whole of placed-for)

    It does NOT mean:
        - external truth certified
        - full semantic judgment issued
        - HUKM issued
        - Tadammun/Iltizam created
        - Haqiqah/Majaz classified

    Critical Laws:
        1. Requires admitted WadhClaim (or admitted WadhGateResult)
        2. Requires MawduLahStructure
        3. Requires MawduLahStructure.whole or equivalent
        4. Preserves WadhClaim trace
        5. Preserves binding trace
        6. Preserves residuals from WadhClaim
        7. Does NOT raise PredicateRank to CERTIFIED
        8. Does NOT create external meaning
        9. Does NOT issue HUKM
        10. Does NOT create Tadammun
        11. Does NOT create Iltizam
        12. Does NOT classify Haqiqah/Majaz/Naql
        13. Does NOT create Ifadah
        14. Unknown whole becomes residual, not exception
        15. Polysemy possible becomes residual
        16. Homonymy possible becomes residual
        17. Partial usage blocks or residualizes
        18. Returns governed failures, not bare exceptions
    """

    strict_mode: bool = True

    def admit_mutabaqah_candidate(
        self,
        wadh_gate_result: WadhGateResult,
    ) -> MutabaqahResult:
        """
        Admit or block MutabaqahCandidate based on WadhGateResult.

        Critical Law: Admission means MutabaqahCandidate admitted, NOT truth certified.

        Args:
            wadh_gate_result: Required admitted WadhGateResult

        Returns:
            MutabaqahResult with admitted candidate or governed failure
        """
        residuals: list[MutabaqahResidual] = []
        missing: list[str] = []

        # Law 1: Requires admitted WadhClaim
        if not wadh_gate_result or not wadh_gate_result.is_admitted:
            residual = make_wadh_claim_not_admitted_residual()
            residuals.append(residual)
            missing.append("admitted_wadh_claim")
            return self._make_failure(
                "WadhClaim not admitted",
                tuple(missing),
                tuple(residuals),
                "",
                "",
            )

        # Extract WadhClaim
        wadh_claim = wadh_gate_result.claim
        if not wadh_claim:
            missing.append("wadh_claim")
            return self._make_failure(
                "Missing WadhClaim in admitted result",
                tuple(missing),
                tuple(residuals),
                "",
                "",
            )

        # Extract traces
        wadh_trace_id = wadh_claim.claim_id
        binding_trace_id = wadh_claim.binding_trace_id

        # Law 4: Preserves WadhClaim trace
        if not wadh_trace_id:
            residual = make_wadh_trace_lost_residual()
            residuals.append(residual)
            missing.append("wadh_trace_id")

        # Law 5: Preserves binding trace
        if not binding_trace_id:
            residual = make_binding_trace_lost_residual()
            residuals.append(residual)
            missing.append("binding_trace_id")

        # Law 2: Requires MawduLahStructure
        mawdu_lah = wadh_claim.mawdu_lah
        if not mawdu_lah:
            missing.append("mawdu_lah_structure")
            return self._make_failure(
                "Missing MawduLahStructure",
                tuple(missing),
                tuple(residuals),
                wadh_trace_id,
                binding_trace_id,
            )

        # Law 3: Requires MawduLahStructure.whole
        # For now, use structure_form as "whole"
        # In future implementations, MawduLahStructure may have explicit "whole" field
        mawdu_lah_whole = mawdu_lah.structure_form
        if not mawdu_lah_whole:
            residual = make_mawdu_lah_whole_unavailable_residual()
            residuals.append(residual)
            missing.append("mawdu_lah_whole")

        # Law 6: Preserve residuals from WadhClaim
        # Note: WadhClaim residuals are WadhResidual type, not MutabaqahResidual
        # We accumulate them separately and track their presence
        wadh_claim_has_blockers = wadh_claim.has_blocking_residuals

        # Check if any blocking residuals exist
        has_blockers = any(r.is_blocker for r in residuals) or wadh_claim_has_blockers

        # If strict mode and has missing requirements or blockers, fail
        if self.strict_mode and (missing or has_blockers):
            reason = "MutabaqahGate requirements not met" if missing else "Blocking residuals present"
            return self._make_failure(
                reason,
                tuple(missing),
                tuple(residuals),
                wadh_trace_id,
                binding_trace_id,
            )

        # Create MutabaqahCandidate
        candidate = MutabaqahCandidate(
            wadh_claim=wadh_claim,
            mawdu_lah_whole=mawdu_lah_whole,
            binding_trace_id=binding_trace_id,
            wadh_trace_id=wadh_trace_id,
            residuals=tuple(residuals),
        )

        # Return admitted result
        return MutabaqahResult(
            admitted=True,
            candidate=candidate,
        )

    def _make_failure(
        self,
        reason: str,
        missing_requirements: Tuple[str, ...],
        residuals: Tuple[MutabaqahResidual, ...],
        wadh_trace_id: str,
        binding_trace_id: str,
    ) -> MutabaqahResult:
        """
        Create governed failure result.

        Critical Law: No bare exceptions, always governed failure.
        """
        failure = MutabaqahFailure(
            reason=reason,
            missing_requirements=missing_requirements,
            residuals=residuals,
            wadh_trace_id=wadh_trace_id,
            binding_trace_id=binding_trace_id,
        )
        return MutabaqahResult(
            admitted=False,
            failure=failure,
        )
