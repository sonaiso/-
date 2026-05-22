"""
LafziTrace - الأثر اللفظي

Core dataclass representing a linguistic trace.

Critical Law:
    لا مدلول لفظي بلا أثر لفظي
    No LafziMadlul without LafziTrace.

LafziTrace Properties:
    - trace_id: Unique identifier for the trace
    - trace_type: Type of linguistic trace (acoustic, written, etc.)
    - trace_content: The actual trace data (string representation)
    - residuals: Tuple of residuals from processing
    - is_valid: Whether trace satisfies all requirements

What LafziTrace Does:
    - Preserves trace_id
    - Preserves trace_type
    - Preserves residuals
    - Validates trace existence

What LafziTrace Does NOT Do:
    - Does NOT create meaning
    - Does NOT create Dal
    - Does NOT create Madlul
    - Does NOT create Dalalah
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union
from .lafzi_trace_type import LafziTraceType


@dataclass(frozen=True)
class LafziTrace:
    """
    Linguistic trace - الأثر اللفظي

    A trace is the preserved input to Lafzi processing.
    It is a condition for possibility, not a semantic object.

    Critical Properties:
        - Preserves trace_id (lineage)
        - Preserves trace_type (modality)
        - Preserves residuals (failures)
        - Does NOT create meaning
        - Does NOT create Dal/Madlul/Dalalah
        - Does NOT raise PredicateRank
    """

    trace_id: str
    trace_type: LafziTraceType
    trace_content: str
    residuals: tuple = ()

    def __post_init__(self):
        """Validate LafziTrace construction."""
        if not self.trace_id:
            raise ValueError("trace_id is required for LafziTrace")
        if not isinstance(self.trace_type, LafziTraceType):
            raise TypeError("trace_type must be LafziTraceType")
        if self.trace_content is None:
            raise ValueError("trace_content is required for LafziTrace")

    @property
    def is_known_type(self) -> bool:
        """Check if trace type is known (not UNKNOWN)."""
        return self.trace_type.is_known

    @property
    def has_residuals(self) -> bool:
        """Check if trace has residuals."""
        return len(self.residuals) > 0

    @property
    def is_valid(self) -> bool:
        """
        Check if trace is valid for processing.

        Valid means:
        - trace_id exists
        - trace_type is known
        - trace_content exists
        - no blocking residuals
        """
        return (
            bool(self.trace_id)
            and self.trace_type.is_known
            and bool(self.trace_content)
        )

    def with_residual(self, residual) -> LafziTrace:
        """Return new LafziTrace with additional residual."""
        return LafziTrace(
            trace_id=self.trace_id,
            trace_type=self.trace_type,
            trace_content=self.trace_content,
            residuals=self.residuals + (residual,),
        )

    def __str__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        residual_count = len(self.residuals)
        return (
            f"LafziTrace[{status}]: {self.trace_type.name} "
            f"(id={self.trace_id}, residuals={residual_count})"
        )

    def __repr__(self) -> str:
        return (
            f"LafziTrace(trace_id='{self.trace_id}', "
            f"trace_type={self.trace_type.name}, "
            f"residuals={len(self.residuals)})"
        )


@dataclass(frozen=True)
class LafziTraceResult:
    """
    Result of LafziTrace gate processing.

    Either:
        - success=True, trace=LafziTrace, failure=None
        - success=False, trace=None, failure=LafziTraceFailure
    """

    success: bool
    trace: Optional[LafziTrace] = None
    failure: Optional[LafziTraceFailure] = None

    def __post_init__(self):
        """Validate result state."""
        if self.success and self.trace is None:
            raise ValueError("Success result must have trace")
        if not self.success and self.failure is None:
            raise ValueError("Failure result must have failure")
        if self.success and self.failure is not None:
            raise ValueError("Success result cannot have failure")
        if not self.success and self.trace is not None:
            raise ValueError("Failure result cannot have trace")

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
            return f"LafziTraceResult[SUCCESS]: {self.trace}"
        else:
            return f"LafziTraceResult[FAILURE]: {self.failure}"

    def __repr__(self) -> str:
        return f"LafziTraceResult(success={self.success})"


# Forward reference for type checking
class LafziTraceFailure:
    """Forward declaration for LafziTraceFailure (defined in lafzi_trace_gate.py)."""
    pass
