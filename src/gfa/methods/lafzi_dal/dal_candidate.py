"""
DalCandidate - الدال المرشح

Core dataclass representing a linguistic signifier candidate.

Critical Law:
    الدال وحده حامل لفظي مرشح، لا معنى
    Dāl-alone is a signifier candidate, not meaning, not Madlul, not Dalalah.

DalCandidate Properties:
    - trace_id: Preserved from LafziTrace
    - signifier_form: The linguistic form serving as signifier
    - dal_type: Type of signifier (sound, written, etc.)
    - residuals: Tuple of residuals from processing
    - is_valid: Whether candidate satisfies all requirements

What DalCandidate Does:
    - Preserves trace_id from LafziTrace
    - Records signifier form
    - Classifies signifier modality
    - Preserves residuals
    - Serves as candidate for future Dalalah binding

What DalCandidate Does NOT Do:
    - Does NOT create meaning
    - Does NOT create Madlul
    - Does NOT create Dalalah
    - Does NOT implement Wadh
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
    - Does NOT perform learning
    - Does NOT create semantic content
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from .dal_type import DalType


@dataclass(frozen=True)
class DalCandidate:
    """
    Linguistic signifier candidate - الدال المرشح

    A signifier candidate is derived from LafziTrace and represents
    a linguistic form that could participate in signification.

    It is a carrier, not a meaning.
    It is a candidate for binding, not a bound signifier.

    Critical Properties:
        - Preserves trace_id (lineage from LafziTrace)
        - Records signifier_form (the linguistic carrier)
        - Classifies dal_type (modality)
        - Preserves residuals (failures)
        - Does NOT create meaning
        - Does NOT create Madlul
        - Does NOT create Dalalah
        - Does NOT raise PredicateRank
    """

    trace_id: str
    signifier_form: str
    dal_type: DalType
    residuals: tuple = ()

    def __post_init__(self):
        """Validate DalCandidate construction."""
        if not self.trace_id:
            raise ValueError("trace_id is required for DalCandidate")
        if not isinstance(self.dal_type, DalType):
            raise TypeError("dal_type must be DalType")
        if self.signifier_form is None:
            raise ValueError("signifier_form is required for DalCandidate")

    @property
    def is_known_type(self) -> bool:
        """Check if signifier type is known (not UNKNOWN)."""
        return self.dal_type.is_known

    @property
    def has_residuals(self) -> bool:
        """Check if candidate has residuals."""
        return len(self.residuals) > 0

    @property
    def is_valid(self) -> bool:
        """
        Check if candidate is valid for processing.

        Valid means:
        - trace_id exists
        - dal_type is known
        - signifier_form exists
        - no blocking residuals
        """
        return (
            bool(self.trace_id)
            and self.dal_type.is_known
            and bool(self.signifier_form)
        )

    def with_residual(self, residual) -> DalCandidate:
        """Return new DalCandidate with additional residual."""
        return DalCandidate(
            trace_id=self.trace_id,
            signifier_form=self.signifier_form,
            dal_type=self.dal_type,
            residuals=self.residuals + (residual,),
        )

    def __str__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        residual_count = len(self.residuals)
        return (
            f"DalCandidate[{status}]: {self.dal_type.name} "
            f"(id={self.trace_id}, form='{self.signifier_form}', residuals={residual_count})"
        )

    def __repr__(self) -> str:
        return (
            f"DalCandidate(trace_id='{self.trace_id}', "
            f"dal_type={self.dal_type.name}, "
            f"residuals={len(self.residuals)})"
        )


@dataclass(frozen=True)
class DalResult:
    """
    Result of DalGate processing.

    Either:
        - success=True, candidate=DalCandidate, failure=None
        - success=False, candidate=None, failure=DalFailure
    """

    success: bool
    candidate: Optional[DalCandidate] = None
    failure: Optional[DalFailure] = None

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
            return f"DalResult[SUCCESS]: {self.candidate}"
        else:
            return f"DalResult[FAILURE]: {self.failure}"

    def __repr__(self) -> str:
        return f"DalResult(success={self.success})"


# Forward reference for type checking
class DalFailure:
    """Forward declaration for DalFailure (defined in dal_gate.py)."""
    pass
