"""
DalMadlulBindingCandidate - مرشح الربط بين الدال والمدلول

Critical Law:
    الربط ليس دلالة كاملة
    Binding is NOT full Dalālah.

DalMadlulBindingCandidate represents the first governed relation candidate
between DālCandidate and MadlulLafziCandidate.

What DalMadlulBindingCandidate Does:
    - Creates governed relation between Dāl and Madlūl-lafẓī
    - Preserves trace_id from both sides
    - Preserves residuals from both sides
    - Records binding_basis (evidence for binding)
    - Operates inside LAFZI_DALALI domain
    - Requires NeutralBinding
    - Requires PriorInformation

What DalMadlulBindingCandidate Does NOT Do:
    - Does NOT create full Dalālah
    - Does NOT implement Wadh
    - Does NOT classify Mutabaqah/Tadammun/Iltizam
    - Does NOT classify Haqiqah/Majaz
    - Does NOT create external meaning
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
    - Does NOT perform learning
    - Does NOT implement upward transitions
    - Does NOT implement downward decomposition

Position in Architecture:
    RationalMethod
    └── NeutralBinding
        └── StyleSpec(LAFZI_DALALI)
            └── LafziMadlul Registration
                └── LafziTrace
                    ├── DālCandidate
                    └── MadlulLafziCandidate
                        └── DalMadlulBindingCandidate ← THIS MODULE
                            └── (Future) Full Dalālah
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple
from uuid import uuid4

from gfa.methods.lafzi_dal import DalCandidate
from gfa.methods.lafzi_madlul import MadlulLafziCandidate
from .binding_basis import BindingBasis
from .residual_taxonomy import BindingResidual


@dataclass(frozen=True)
class DalMadlulBindingCandidate:
    """
    Governed binding candidate between Dāl and Madlūl-lafẓī.

    This is the first relation between signifier and signified,
    but it is NOT full Dalālah (signification).

    Critical Properties:
        - dal_candidate: The signifier candidate
        - madlul_candidate: The signified candidate
        - binding_basis: Evidence for binding
        - trace_id: Preserved lineage
        - dal_trace_id: Preserved from DālCandidate
        - madlul_trace_id: Preserved from MadlulLafziCandidate
        - residuals: All residuals from both sides
        - is_valid: Whether binding satisfies all requirements

    Critical Laws:
        - Binding is NOT full Dalālah
        - Binding does NOT create meaning
        - Binding does NOT issue HUKM
        - Binding does NOT raise PredicateRank
    """

    dal_candidate: DalCandidate
    madlul_candidate: MadlulLafziCandidate
    binding_basis: BindingBasis
    trace_id: str = ""
    dal_trace_id: str = ""
    madlul_trace_id: str = ""
    residuals: Tuple[BindingResidual, ...] = ()

    def __post_init__(self):
        """Validate binding candidate construction."""
        if not self.dal_candidate:
            raise ValueError("dal_candidate is required for DalMadlulBindingCandidate")
        if not self.madlul_candidate:
            raise ValueError("madlul_candidate is required for DalMadlulBindingCandidate")
        if not isinstance(self.binding_basis, BindingBasis):
            raise TypeError("binding_basis must be BindingBasis")

        # Preserve trace_ids if not provided
        if not self.trace_id:
            object.__setattr__(self, "trace_id", uuid4().hex)
        if not self.dal_trace_id:
            object.__setattr__(self, "dal_trace_id", self.dal_candidate.trace_id)
        if not self.madlul_trace_id:
            object.__setattr__(self, "madlul_trace_id", self.madlul_candidate.trace_id)

    @property
    def is_known_basis(self) -> bool:
        """Check if binding basis is known (not UNKNOWN_BASIS)."""
        return self.binding_basis.is_known

    @property
    def has_residuals(self) -> bool:
        """Check if binding has residuals."""
        return len(self.residuals) > 0

    @property
    def has_blocking_residuals(self) -> bool:
        """Check if binding has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    @property
    def is_valid(self) -> bool:
        """
        Check if binding candidate is valid.

        Valid means:
            - dal_candidate is valid
            - madlul_candidate is valid
            - binding_basis is known
            - no blocking residuals
            - trace_ids preserved
        """
        return (
            self.dal_candidate.is_valid
            and self.madlul_candidate.is_valid
            and self.binding_basis.is_known
            and not self.has_blocking_residuals
            and bool(self.trace_id)
            and bool(self.dal_trace_id)
            and bool(self.madlul_trace_id)
        )

    def with_residual(self, residual: BindingResidual) -> DalMadlulBindingCandidate:
        """Return new binding candidate with additional residual."""
        return DalMadlulBindingCandidate(
            dal_candidate=self.dal_candidate,
            madlul_candidate=self.madlul_candidate,
            binding_basis=self.binding_basis,
            trace_id=self.trace_id,
            dal_trace_id=self.dal_trace_id,
            madlul_trace_id=self.madlul_trace_id,
            residuals=self.residuals + (residual,),
        )

    def __str__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        residual_count = len(self.residuals)
        return (
            f"DalMadlulBindingCandidate[{status}]: "
            f"{self.dal_candidate.signifier_form} → {self.madlul_candidate.candidate_form} "
            f"(basis={self.binding_basis.name}, residuals={residual_count})"
        )

    def __repr__(self) -> str:
        return (
            f"DalMadlulBindingCandidate(trace_id='{self.trace_id}', "
            f"basis={self.binding_basis.name}, "
            f"residuals={len(self.residuals)})"
        )


@dataclass(frozen=True)
class DalMadlulBindingFailure:
    """
    Governed failure from Dāl/Madlūl binding.

    Never a bare exception.
    Always returns governed object with:
        - reason: Failure reason
        - missing_requirements: List of missing requirements
        - residuals: Typed residual objects
        - trace_id: Lineage preservation
    """

    reason: str
    missing_requirements: Tuple[str, ...]
    residuals: Tuple[BindingResidual, ...]
    trace_id: str = ""

    def __post_init__(self):
        """Initialize trace_id if not provided."""
        if not self.trace_id:
            object.__setattr__(self, "trace_id", uuid4().hex)

    @property
    def has_blockers(self) -> bool:
        """Check if failure has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    def __str__(self) -> str:
        requirements_str = ", ".join(self.missing_requirements)
        return f"DalMadlulBindingFailure: {self.reason} (missing: {requirements_str})"

    def __repr__(self) -> str:
        return f"DalMadlulBindingFailure(reason='{self.reason}', residuals={len(self.residuals)})"


@dataclass(frozen=True)
class DalMadlulBindingResult:
    """
    Result of Dāl/Madlūl binding operation.

    Either:
        - success=True, candidate=DalMadlulBindingCandidate, failure=None
        - success=False, candidate=None, failure=DalMadlulBindingFailure
    """

    success: bool
    candidate: Optional[DalMadlulBindingCandidate] = None
    failure: Optional[DalMadlulBindingFailure] = None

    def __post_init__(self):
        """Validate result state."""
        if self.success and self.candidate is None:
            raise ValueError("Success result must have candidate")
        if not self.success and self.failure is None:
            raise ValueError("Failure result must have failure")
        if self.success and self.failure is not None:
            raise ValueError("Success result cannot have failure")
        if not self.success and self.candidate is not None:
            raise ValueError("Failure result cannot have candidate")

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
            return f"DalMadlulBindingResult[SUCCESS]: {self.candidate}"
        else:
            return f"DalMadlulBindingResult[FAILURE]: {self.failure}"

    def __repr__(self) -> str:
        return f"DalMadlulBindingResult(success={self.success})"
