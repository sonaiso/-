"""
MadlulLafziCandidate - المدلول اللفظي المرشح

Core dataclass representing a linguistic signified candidate.

Critical Law:
    المدلول اللفظي ليس معنى خارجياً بالضرورة
    Madlūl-lafẓī is NOT necessarily external meaning.
    Madlūl-lafẓī is a governed candidate for what may be signified
    inside the linguistic domain.

MadlulLafziCandidate Properties:
    - trace_id: Preserved from upstream processing
    - madlul_type: Type of linguistic signified
    - candidate_form: The linguistic form serving as signified
    - source_prior_information: Evidence from PriorInformation
    - residuals: Tuple of residuals from processing
    - is_valid: Whether candidate satisfies all requirements

What MadlulLafziCandidate Does:
    - Preserves trace_id
    - Records linguistic signified candidate
    - Classifies madlul type
    - Preserves source prior information
    - Preserves residuals
    - Serves as candidate for future Dalalah binding

What MadlulLafziCandidate Does NOT Do:
    - Does NOT create external meaning
    - Does NOT create Dalalah
    - Does NOT implement Wadh
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
    - Does NOT require DalCandidate yet
    - Does NOT perform learning
    - Does NOT create semantic content
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Any
from .madlul_lafzi_type import MadlulLafziType


@dataclass(frozen=True)
class MadlulLafziCandidate:
    """
    Linguistic signified candidate - المدلول اللفظي المرشح

    A signified candidate represents a linguistic entity that could
    participate in signification within the linguistic domain.

    It is a candidate inside the linguistic domain, not external meaning.
    It is a candidate for binding, not bound signified.

    Critical Properties:
        - Preserves trace_id (lineage from upstream)
        - Records candidate_form (the linguistic entity)
        - Classifies madlul_type (entity type)
        - Preserves source_prior_information (evidence)
        - Preserves residuals (failures)
        - Does NOT create external meaning
        - Does NOT create Dalalah
        - Does NOT raise PredicateRank
        - Does NOT require DalCandidate yet
    """

    trace_id: str
    madlul_type: MadlulLafziType
    candidate_form: str
    source_prior_information: str = ""
    residuals: tuple = ()

    def __post_init__(self):
        """Validate MadlulLafziCandidate construction."""
        if not self.trace_id:
            raise ValueError("trace_id is required for MadlulLafziCandidate")
        if not isinstance(self.madlul_type, MadlulLafziType):
            raise TypeError("madlul_type must be MadlulLafziType")
        if self.candidate_form is None:
            raise ValueError("candidate_form is required for MadlulLafziCandidate")

    @property
    def is_known_type(self) -> bool:
        """Check if madlul type is known (not UNKNOWN)."""
        return self.madlul_type.is_known

    @property
    def has_residuals(self) -> bool:
        """Check if candidate has residuals."""
        return len(self.residuals) > 0

    @property
    def has_prior_information(self) -> bool:
        """Check if candidate has source prior information."""
        return bool(self.source_prior_information)

    @property
    def is_valid(self) -> bool:
        """
        Check if candidate is valid for processing.

        Valid means:
        - trace_id exists
        - madlul_type is known
        - candidate_form exists
        - has prior information
        """
        return (
            bool(self.trace_id)
            and self.madlul_type.is_known
            and bool(self.candidate_form)
            and self.has_prior_information
        )

    def with_residual(self, residual) -> MadlulLafziCandidate:
        """Return new MadlulLafziCandidate with additional residual."""
        return MadlulLafziCandidate(
            trace_id=self.trace_id,
            madlul_type=self.madlul_type,
            candidate_form=self.candidate_form,
            source_prior_information=self.source_prior_information,
            residuals=self.residuals + (residual,),
        )

    def __str__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        residual_count = len(self.residuals)
        return (
            f"MadlulLafziCandidate[{status}]: {self.madlul_type.name} "
            f"(id={self.trace_id}, form='{self.candidate_form}', residuals={residual_count})"
        )

    def __repr__(self) -> str:
        return (
            f"MadlulLafziCandidate(trace_id='{self.trace_id}', "
            f"madlul_type={self.madlul_type.name}, "
            f"residuals={len(self.residuals)})"
        )


@dataclass(frozen=True)
class MadlulLafziResult:
    """
    Result of MadlulLafziGate processing.

    Either:
        - success=True, candidate=MadlulLafziCandidate, failure=None
        - success=False, candidate=None, failure=MadlulLafziFailure
    """

    success: bool
    candidate: Optional[MadlulLafziCandidate] = None
    failure: Optional[MadlulLafziFailure] = None

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
            return f"MadlulLafziResult[SUCCESS]: {self.candidate}"
        else:
            return f"MadlulLafziResult[FAILURE]: {self.failure}"

    def __repr__(self) -> str:
        return f"MadlulLafziResult(success={self.success})"


# Forward reference for type checking
class MadlulLafziFailure:
    """Forward declaration for MadlulLafziFailure (defined in madlul_lafzi_gate.py)."""
    pass
