"""
WadhClaim - مطالبة الوضع

Critical Law:
    المطالبة بالوضع ليست دلالة كاملة
    Wadh claim is NOT full Dalālah.

WadhClaim represents a governed claim that a Wadh convention exists,
NOT full semantic signification.

What WadhClaim Does:
    - Creates governed Wadh claim
    - Preserves binding trace
    - Records Wadh evidence
    - Creates MawduLahStructure candidate
    - Guards against premature semantics

What WadhClaim Does NOT Do:
    - Does NOT create full Dalālah
    - Does NOT create external meaning
    - Does NOT classify Mutabaqah/Tadammun/Iltizam
    - Does NOT classify Haqiqah/Majaz/Naql
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
    - Does NOT bypass transmission requirements

Position in Architecture:
    DalMadlulBindingCandidate (PR-L4, certified)
    └── WadhGeometry (PR-L5A)
        ├── WadhEvidence
        ├── WadhClaim ← THIS MODULE
        └── MawduLahStructure
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple
from uuid import uuid4

from .wadh_evidence import WadhEvidence
from .mawdu_lah_structure import MawduLahStructure
from .residual_taxonomy import WadhResidual


@dataclass(frozen=True)
class WadhClaim:
    """
    Governed Wadh claim - مطالبة الوضع

    This represents a claim that a Wadh (convention) exists,
    based on evidence, NOT full semantic signification.

    Critical Properties:
        - wadh_evidence: Evidence supporting claim
        - mawdu_lah: The placed-for structure
        - binding_trace_id: Preserved from binding candidate
        - claim_id: Unique identifier
        - residuals: Unresolved issues

    Critical Laws:
        - WadhClaim is NOT full Dalālah
        - WadhClaim does NOT create external meaning
        - WadhClaim does NOT issue HUKM
        - WadhClaim does NOT classify Mutabaqah/Tadammun/Iltizam
        - WadhClaim does NOT classify Haqiqah/Majaz/Naql
        - WadhClaim preserves binding trace
        - WadhClaim does NOT raise PredicateRank
    """

    wadh_evidence: WadhEvidence
    mawdu_lah: MawduLahStructure
    binding_trace_id: str = ""
    claim_id: str = ""
    residuals: Tuple[WadhResidual, ...] = ()

    def __post_init__(self):
        """Validate WadhClaim construction."""
        if not isinstance(self.wadh_evidence, WadhEvidence):
            raise TypeError("wadh_evidence must be WadhEvidence")
        if not isinstance(self.mawdu_lah, MawduLahStructure):
            raise TypeError("mawdu_lah must be MawduLahStructure")

        # Generate claim_id if not provided
        if not self.claim_id:
            object.__setattr__(self, "claim_id", uuid4().hex)

        # Preserve binding_trace_id from evidence if not provided
        if not self.binding_trace_id and self.wadh_evidence.binding_trace_id:
            object.__setattr__(self, "binding_trace_id", self.wadh_evidence.binding_trace_id)

    @property
    def has_binding_trace(self) -> bool:
        """Check if binding trace is preserved."""
        return bool(self.binding_trace_id)

    @property
    def has_valid_evidence(self) -> bool:
        """Check if Wadh evidence is valid."""
        return self.wadh_evidence.is_valid

    @property
    def has_valid_structure(self) -> bool:
        """Check if MawduLah structure is valid."""
        return self.mawdu_lah.is_valid

    @property
    def has_residuals(self) -> bool:
        """Check if claim has residuals."""
        return len(self.residuals) > 0

    @property
    def has_blocking_residuals(self) -> bool:
        """Check if claim has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    @property
    def is_transmitted(self) -> bool:
        """
        Check if claim is based on transmitted evidence.

        Critical Law: Arabic Wadh requires transmission.
        """
        return self.wadh_evidence.is_transmitted

    @property
    def sufficient_for_arabic_wadh(self) -> bool:
        """
        Check if claim is sufficient for Arabic Wadh.

        Critical Law: Requires transmitted evidence + valid structure.
        """
        return (
            self.wadh_evidence.sufficient_for_arabic_wadh
            and self.mawdu_lah.is_valid
            and not self.has_blocking_residuals
        )

    @property
    def is_valid(self) -> bool:
        """
        Check if claim is valid.

        Valid means:
            - wadh_evidence is valid
            - mawdu_lah structure is valid
            - binding trace preserved
            - no blocking residuals
        """
        return (
            self.has_valid_evidence
            and self.has_valid_structure
            and self.has_binding_trace
            and not self.has_blocking_residuals
        )

    def with_residual(self, residual: WadhResidual) -> WadhClaim:
        """Return new WadhClaim with additional residual."""
        return WadhClaim(
            wadh_evidence=self.wadh_evidence,
            mawdu_lah=self.mawdu_lah,
            binding_trace_id=self.binding_trace_id,
            claim_id=self.claim_id,
            residuals=self.residuals + (residual,),
        )

    def __str__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        transmitted = "TRANSMITTED" if self.is_transmitted else "NOT_TRANSMITTED"
        return (
            f"WadhClaim[{status}, {transmitted}]: "
            f"{self.mawdu_lah.structure_form} "
            f"(evidence={self.wadh_evidence.source.kind.value}, "
            f"residuals={len(self.residuals)})"
        )

    def __repr__(self) -> str:
        return (
            f"WadhClaim(claim_id='{self.claim_id}', "
            f"structure='{self.mawdu_lah.structure_form}', "
            f"residuals={len(self.residuals)})"
        )


@dataclass(frozen=True)
class WadhClaimFailure:
    """
    Governed failure from Wadh claim processing.

    Never a bare exception.
    Always returns governed object with reason and residuals.
    """

    reason: str
    missing_requirements: Tuple[str, ...]
    residuals: Tuple[WadhResidual, ...]
    failure_id: str = ""

    def __post_init__(self):
        """Initialize failure_id if not provided."""
        if not self.failure_id:
            object.__setattr__(self, "failure_id", uuid4().hex)

    @property
    def has_blockers(self) -> bool:
        """Check if failure has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    def __str__(self) -> str:
        requirements_str = ", ".join(self.missing_requirements)
        return f"WadhClaimFailure: {self.reason} (missing: {requirements_str})"

    def __repr__(self) -> str:
        return f"WadhClaimFailure(reason='{self.reason}', residuals={len(self.residuals)})"


@dataclass(frozen=True)
class WadhClaimResult:
    """
    Result of Wadh claim processing.

    Either:
        - success=True, claim=WadhClaim, failure=None
        - success=False, claim=None, failure=WadhClaimFailure
    """

    success: bool
    claim: Optional[WadhClaim] = None
    failure: Optional[WadhClaimFailure] = None

    def __post_init__(self):
        """Validate result state."""
        if self.success and self.claim is None:
            raise ValueError("Success result must have claim")
        if not self.success and self.failure is None:
            raise ValueError("Failure result must have failure")
        if self.success and self.failure is not None:
            raise ValueError("Success result cannot have failure")
        if not self.success and self.claim is not None:
            raise ValueError("Failure result cannot have claim")

    @property
    def is_success(self) -> bool:
        """Check if result is success."""
        return self.success

    @property
    def is_failure(self) -> bool:
        """Check if result is failure."""
        return not self.success

    def __str__(self) -> str:
        if self.success:
            return f"WadhClaimResult[SUCCESS]: {self.claim}"
        else:
            return f"WadhClaimResult[FAILURE]: {self.failure}"

    def __repr__(self) -> str:
        return f"WadhClaimResult(success={self.success})"
