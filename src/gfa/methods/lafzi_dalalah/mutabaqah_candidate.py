"""
MutabaqahCandidate - مرشح المطابقة

Critical Law:
    المطابقة = دلالة الدال على تمام ما وضع له
    Mutabaqah = signification to the whole of what is placed-for.

MutabaqahCandidate represents a governed candidate for Mutabaqah signification,
NOT certified external truth or full semantic judgment.

What MutabaqahCandidate Does:
    - Creates governed Mutabaqah candidate
    - Preserves WadhClaim trace
    - Preserves binding trace
    - Reads whole of MawduLahStructure
    - Guards against semantic inflation

What MutabaqahCandidate Does NOT Do:
    - Does NOT create external meaning
    - Does NOT certify truth
    - Does NOT issue HUKM
    - Does NOT create Tadammun
    - Does NOT create Iltizam
    - Does NOT classify Haqiqah/Majaz/Naql
    - Does NOT create Ifadah
    - Does NOT raise PredicateRank to CERTIFIED

Position in Architecture:
    WadhGate (PR-L5B)
    └── MutabaqahGate (PR-L6A)
        └── MutabaqahCandidate ← THIS MODULE
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
from uuid import uuid4

from gfa.methods.lafzi_wadh import WadhClaim, MawduLahStructure
from .residual_taxonomy import MutabaqahResidual


@dataclass(frozen=True)
class MutabaqahCandidate:
    """
    Governed candidate for Mutabaqah signification - مرشح المطابقة

    This represents a candidate for signifying the whole of what is placed-for,
    based on an admitted WadhClaim, NOT external truth or full semantic judgment.

    Critical Properties:
        - wadh_claim: Admitted WadhClaim (required)
        - mawdu_lah_whole: The whole of MawduLahStructure
        - binding_trace_id: Preserved from WadhClaim
        - wadh_trace_id: Preserved from WadhClaim
        - candidate_id: Unique identifier
        - residuals: Unresolved issues

    Critical Laws:
        1. Requires admitted WadhClaim
        2. Requires MawduLahStructure
        3. Requires MawduLahStructure.whole
        4. Preserves WadhClaim trace
        5. Preserves binding trace
        6. Does NOT create external meaning
        7. Does NOT issue HUKM
        8. Does NOT create Tadammun
        9. Does NOT create Iltizam
        10. Does NOT classify Haqiqah/Majaz/Naql
        11. Does NOT create Ifadah
        12. Does NOT raise PredicateRank to CERTIFIED
        13. Unknown whole becomes residual
        14. Polysemy possible becomes residual
        15. Homonymy possible becomes residual
        16. Partial usage blocks or residualizes
    """

    wadh_claim: WadhClaim
    mawdu_lah_whole: str
    binding_trace_id: str = ""
    wadh_trace_id: str = ""
    candidate_id: str = ""
    residuals: Tuple[MutabaqahResidual, ...] = ()

    def __post_init__(self):
        """Validate MutabaqahCandidate construction."""
        if not isinstance(self.wadh_claim, WadhClaim):
            raise TypeError("wadh_claim must be WadhClaim")
        if not self.mawdu_lah_whole:
            raise ValueError("mawdu_lah_whole is required")

        # Generate candidate_id if not provided
        if not self.candidate_id:
            object.__setattr__(self, "candidate_id", uuid4().hex)

        # Preserve wadh_trace_id from claim if not provided
        if not self.wadh_trace_id and self.wadh_claim.claim_id:
            object.__setattr__(self, "wadh_trace_id", self.wadh_claim.claim_id)

        # Preserve binding_trace_id from claim if not provided
        if not self.binding_trace_id and self.wadh_claim.binding_trace_id:
            object.__setattr__(self, "binding_trace_id", self.wadh_claim.binding_trace_id)

    @property
    def has_wadh_trace(self) -> bool:
        """Check if WadhClaim trace is preserved."""
        return bool(self.wadh_trace_id)

    @property
    def has_binding_trace(self) -> bool:
        """Check if binding trace is preserved."""
        return bool(self.binding_trace_id)

    @property
    def has_valid_claim(self) -> bool:
        """Check if underlying WadhClaim is valid."""
        return self.wadh_claim.is_valid

    @property
    def has_residuals(self) -> bool:
        """Check if candidate has residuals."""
        return len(self.residuals) > 0

    @property
    def has_blocking_residuals(self) -> bool:
        """Check if candidate has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    @property
    def is_valid(self) -> bool:
        """
        Check if candidate is valid.

        Valid means:
            - wadh_claim is valid
            - mawdu_lah_whole exists
            - wadh trace preserved
            - binding trace preserved
            - no blocking residuals
        """
        return (
            self.has_valid_claim
            and bool(self.mawdu_lah_whole)
            and self.has_wadh_trace
            and self.has_binding_trace
            and not self.has_blocking_residuals
        )

    @property
    def is_admitted(self) -> bool:
        """
        Check if candidate is admitted.

        Critical Law: Admission means candidate admitted, NOT truth certified.
        """
        return self.is_valid

    def with_residual(self, residual: MutabaqahResidual) -> MutabaqahCandidate:
        """Return new MutabaqahCandidate with additional residual."""
        return MutabaqahCandidate(
            wadh_claim=self.wadh_claim,
            mawdu_lah_whole=self.mawdu_lah_whole,
            binding_trace_id=self.binding_trace_id,
            wadh_trace_id=self.wadh_trace_id,
            candidate_id=self.candidate_id,
            residuals=self.residuals + (residual,),
        )

    def __str__(self) -> str:
        status = "ADMITTED" if self.is_admitted else "BLOCKED"
        return (
            f"MutabaqahCandidate[{status}]: whole='{self.mawdu_lah_whole}' "
            f"(wadh_trace={self.wadh_trace_id[:8]}..., "
            f"residuals={len(self.residuals)})"
        )

    def __repr__(self) -> str:
        return (
            f"MutabaqahCandidate(candidate_id='{self.candidate_id}', "
            f"whole='{self.mawdu_lah_whole}', "
            f"residuals={len(self.residuals)})"
        )
