"""
WadhGateResult - نتيجة بوابة الوضع

Critical Law:
    قبول الوضع ≠ دلالة كاملة
    Wadh admission ≠ full Dalālah.

WadhGateResult represents the governed result from WadhGate processing.

What WadhGateResult Does:
    - Returns governed success/failure
    - Preserves WadhClaim on success
    - Returns WadhGateFailure on failure
    - Accumulates residuals
    - Preserves binding trace

What WadhGateResult Does NOT Do:
    - Does NOT create full Dalālah
    - Does NOT create external meaning
    - Does NOT classify Mutabaqah/Tadammun/Iltizam
    - Does NOT classify Haqiqah/Majaz/Naql
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank

Position in Architecture:
    DalMadlulBindingCandidate (PR-L4, certified)
    └── WadhGeometry (PR-L5A)
        ├── WadhEvidence
        ├── WadhClaim
        └── WadhGate (PR-L5B) ← THIS MODULE
            └── WadhGateResult
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple
from uuid import uuid4

from .wadh_claim import WadhClaim
from .residual_taxonomy import WadhResidual


@dataclass(frozen=True)
class WadhGateFailure:
    """
    Governed failure from WadhGate processing.

    Never a bare exception.
    Always returns governed object with reason and residuals.

    Critical Properties:
        - reason: Why gate failed
        - missing_requirements: What was missing
        - residuals: All accumulated residuals
        - failure_id: Unique identifier
        - binding_trace_id: Preserved from input

    Critical Laws:
        - No bare exceptions
        - All residuals preserved
        - Binding trace preserved
        - Returns governed failure
    """

    reason: str
    missing_requirements: Tuple[str, ...]
    residuals: Tuple[WadhResidual, ...]
    failure_id: str = ""
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
    def has_binding_trace(self) -> bool:
        """Check if binding trace is preserved."""
        return bool(self.binding_trace_id)

    def __str__(self) -> str:
        requirements_str = ", ".join(self.missing_requirements)
        return (
            f"WadhGateFailure: {self.reason} "
            f"(missing: {requirements_str}, residuals={len(self.residuals)})"
        )

    def __repr__(self) -> str:
        return (
            f"WadhGateFailure(reason='{self.reason}', "
            f"residuals={len(self.residuals)})"
        )


@dataclass(frozen=True)
class WadhGateResult:
    """
    Result of WadhGate processing.

    Either:
        - admitted=True, claim=WadhClaim, failure=None
        - admitted=False, claim=None, failure=WadhGateFailure

    Critical Properties:
        - admitted: Whether WadhClaim was admitted
        - claim: The admitted WadhClaim (if admitted)
        - failure: The failure details (if not admitted)

    Critical Laws:
        - Admitted means WadhClaim admitted, NOT meaning certified
        - Admitted does NOT mean full Dalālah completed
        - Admitted does NOT mean HUKM issued
        - Admitted does NOT mean semantic classification done
        - Failure preserves all residuals
        - Binding trace preserved in both paths
    """

    admitted: bool
    claim: Optional[WadhClaim] = None
    failure: Optional[WadhGateFailure] = None

    def __post_init__(self):
        """Validate result state."""
        if self.admitted and self.claim is None:
            raise ValueError("Admitted result must have claim")
        if not self.admitted and self.failure is None:
            raise ValueError("Blocked result must have failure")
        if self.admitted and self.failure is not None:
            raise ValueError("Admitted result cannot have failure")
        if not self.admitted and self.claim is not None:
            raise ValueError("Blocked result cannot have claim")

    @property
    def is_admitted(self) -> bool:
        """Check if WadhClaim was admitted."""
        return self.admitted

    @property
    def is_blocked(self) -> bool:
        """Check if WadhClaim was blocked."""
        return not self.admitted

    @property
    def has_claim(self) -> bool:
        """Check if result has claim."""
        return self.claim is not None

    @property
    def has_failure(self) -> bool:
        """Check if result has failure."""
        return self.failure is not None

    @property
    def binding_trace_id(self) -> str:
        """Get preserved binding trace ID."""
        if self.admitted and self.claim:
            return self.claim.binding_trace_id
        elif self.failure:
            return self.failure.binding_trace_id
        return ""

    def __str__(self) -> str:
        if self.admitted:
            return f"WadhGateResult[ADMITTED]: {self.claim}"
        else:
            return f"WadhGateResult[BLOCKED]: {self.failure}"

    def __repr__(self) -> str:
        return f"WadhGateResult(admitted={self.admitted})"
