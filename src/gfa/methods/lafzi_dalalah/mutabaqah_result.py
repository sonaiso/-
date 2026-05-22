"""
MutabaqahResult - نتيجة المطابقة

Critical Law:
    قبول المطابقة ≠ حكم كامل
    Mutabaqah admission ≠ full judgment.

MutabaqahResult represents the governed result from MutabaqahGate processing.

What MutabaqahResult Does:
    - Returns governed success/failure
    - Preserves MutabaqahCandidate on success
    - Returns MutabaqahFailure on failure
    - Accumulates residuals
    - Preserves WadhClaim trace
    - Preserves binding trace

What MutabaqahResult Does NOT Do:
    - Does NOT create external meaning
    - Does NOT certify truth
    - Does NOT issue HUKM
    - Does NOT create Tadammun
    - Does NOT create Iltizam
    - Does NOT classify Haqiqah/Majaz/Naql
    - Does NOT raise PredicateRank

Position in Architecture:
    WadhGate (PR-L5B)
    └── MutabaqahGate (PR-L6A)
        └── MutabaqahResult ← THIS MODULE
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple
from uuid import uuid4

from .mutabaqah_candidate import MutabaqahCandidate
from .residual_taxonomy import MutabaqahResidual


@dataclass(frozen=True)
class MutabaqahFailure:
    """
    Governed failure from MutabaqahGate processing.

    Never a bare exception.
    Always returns governed object with reason and residuals.

    Critical Properties:
        - reason: Why gate failed
        - missing_requirements: What was missing
        - residuals: All accumulated residuals
        - failure_id: Unique identifier
        - wadh_trace_id: Preserved from input
        - binding_trace_id: Preserved from input

    Critical Laws:
        - No bare exceptions
        - All residuals preserved
        - WadhClaim trace preserved
        - Binding trace preserved
        - Returns governed failure
    """

    reason: str
    missing_requirements: Tuple[str, ...]
    residuals: Tuple[MutabaqahResidual, ...]
    failure_id: str = ""
    wadh_trace_id: str = ""
    binding_trace_id: str = ""

    def __post_init__(self):
        """Initialize failure_id if not provided."""
        if not self.failure_id:
            object.__setattr__(self, "failure_id", uuid4().hex)

    @property
    def has_blockers(self) -> bool:
        """Check if failure has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    @property
    def blocker_count(self) -> int:
        """Count blocking residuals."""
        return sum(1 for r in self.residuals if r.is_blocker)

    @property
    def has_wadh_trace(self) -> bool:
        """Check if WadhClaim trace is preserved."""
        return bool(self.wadh_trace_id)

    @property
    def has_binding_trace(self) -> bool:
        """Check if binding trace is preserved."""
        return bool(self.binding_trace_id)

    def __str__(self) -> str:
        requirements_str = ", ".join(self.missing_requirements)
        return (
            f"MutabaqahFailure: {self.reason} "
            f"(missing: {requirements_str}, residuals={len(self.residuals)})"
        )

    def __repr__(self) -> str:
        return (
            f"MutabaqahFailure(reason='{self.reason}', "
            f"residuals={len(self.residuals)})"
        )


@dataclass(frozen=True)
class MutabaqahResult:
    """
    Result of MutabaqahGate processing.

    Either:
        - admitted=True, candidate=MutabaqahCandidate, failure=None
        - admitted=False, candidate=None, failure=MutabaqahFailure

    Critical Properties:
        - admitted: Whether MutabaqahCandidate was admitted
        - candidate: The admitted MutabaqahCandidate (if admitted)
        - failure: The failure details (if not admitted)

    Critical Laws:
        - Admitted means MutabaqahCandidate admitted, NOT truth certified
        - Admitted does NOT mean full semantic judgment
        - Admitted does NOT mean HUKM issued
        - Admitted does NOT mean Tadammun/Iltizam created
        - Admitted does NOT mean Haqiqah/Majaz classified
        - Failure preserves all residuals
        - WadhClaim trace preserved in both paths
        - Binding trace preserved in both paths
    """

    admitted: bool
    candidate: Optional[MutabaqahCandidate] = None
    failure: Optional[MutabaqahFailure] = None

    def __post_init__(self):
        """Validate result state."""
        if self.admitted and self.candidate is None:
            raise ValueError("Admitted result must have candidate")
        if not self.admitted and self.failure is None:
            raise ValueError("Blocked result must have failure")
        if self.admitted and self.failure is not None:
            raise ValueError("Admitted result cannot have failure")
        if not self.admitted and self.candidate is not None:
            raise ValueError("Blocked result cannot have candidate")

    @property
    def is_admitted(self) -> bool:
        """Check if MutabaqahCandidate was admitted."""
        return self.admitted

    @property
    def is_blocked(self) -> bool:
        """Check if MutabaqahCandidate was blocked."""
        return not self.admitted

    @property
    def has_candidate(self) -> bool:
        """Check if result has candidate."""
        return self.candidate is not None

    @property
    def has_failure(self) -> bool:
        """Check if result has failure."""
        return self.failure is not None

    @property
    def wadh_trace_id(self) -> str:
        """Get preserved WadhClaim trace ID."""
        if self.admitted and self.candidate:
            return self.candidate.wadh_trace_id
        elif self.failure:
            return self.failure.wadh_trace_id
        return ""

    @property
    def binding_trace_id(self) -> str:
        """Get preserved binding trace ID."""
        if self.admitted and self.candidate:
            return self.candidate.binding_trace_id
        elif self.failure:
            return self.failure.binding_trace_id
        return ""

    def __str__(self) -> str:
        if self.admitted:
            return f"MutabaqahResult[ADMITTED]: {self.candidate}"
        else:
            return f"MutabaqahResult[BLOCKED]: {self.failure}"

    def __repr__(self) -> str:
        return f"MutabaqahResult(admitted={self.admitted})"
