"""
DalMadlulBindingCandidate - مرشح الربط بين الدال والمدلول

Represents a neutral binding relation between signifier and signified.
"""

from dataclasses import dataclass
from typing import Optional, Tuple, Any


@dataclass(frozen=True)
class DalMadlulBindingCandidate:
    """
    Neutral binding candidate between Dāl (signifier) and Madlūl (signified).

    Critical Law:
        This is a NEUTRAL RELATION, not full Dalalah.
        It connects signifier and signified WITHOUT semantic interpretation.

    Attributes:
        trace_id: Unique trace identifier
        binding_type: Type of binding relation
        dal_candidate: The signifier candidate
        madlul_candidate: The signified candidate
        source_prior_information: Prior information from inputs
        residuals: Accumulated residuals from both sides
        binding_confidence: Confidence in binding (0.0-1.0)
        binding_conditions: Optional conditions/constraints
    """

    trace_id: str
    binding_type: Any  # DalMadlulBindingType (avoid circular import)
    dal_candidate: Any  # DalCandidate
    madlul_candidate: Any  # MadlulLafziCandidate
    source_prior_information: str
    residuals: Tuple[Any, ...] = ()  # Tuple of residuals
    binding_confidence: float = 1.0
    binding_conditions: Optional[Tuple[str, ...]] = None

    def __post_init__(self):
        """Validate DalMadlulBindingCandidate attributes."""
        # Validate trace_id
        if not self.trace_id or not isinstance(self.trace_id, str):
            raise ValueError("trace_id must be non-empty string")

        # Validate binding_confidence
        if not (0.0 <= self.binding_confidence <= 1.0):
            raise ValueError("binding_confidence must be in range [0.0, 1.0]")

        # Validate residuals is tuple
        if not isinstance(self.residuals, tuple):
            raise ValueError("residuals must be tuple")

    @property
    def is_valid(self) -> bool:
        """Check if binding candidate is valid."""
        return (
            self.dal_candidate is not None
            and self.madlul_candidate is not None
            and len(self.trace_id) > 0
        )

    @property
    def has_residuals(self) -> bool:
        """Check if binding has residuals."""
        return len(self.residuals) > 0

    @property
    def has_conditions(self) -> bool:
        """Check if binding has conditions."""
        return (
            self.binding_conditions is not None
            and len(self.binding_conditions) > 0
        )

    @property
    def is_simple(self) -> bool:
        """Check if binding is simple one-to-one."""
        return hasattr(self.binding_type, 'is_simple') and self.binding_type.is_simple

    @property
    def is_composite(self) -> bool:
        """Check if binding is composite."""
        return hasattr(self.binding_type, 'is_composite') and self.binding_type.is_composite

    @property
    def requires_resolution(self) -> bool:
        """Check if binding requires further resolution."""
        return (
            hasattr(self.binding_type, 'requires_resolution')
            and self.binding_type.requires_resolution
        )

    def with_additional_residuals(
        self, *new_residuals: Any
    ) -> "DalMadlulBindingCandidate":
        """
        Create new binding candidate with additional residuals.

        Args:
            *new_residuals: New residuals to add

        Returns:
            New DalMadlulBindingCandidate with merged residuals
        """
        merged_residuals = self.residuals + tuple(new_residuals)
        return DalMadlulBindingCandidate(
            trace_id=self.trace_id,
            binding_type=self.binding_type,
            dal_candidate=self.dal_candidate,
            madlul_candidate=self.madlul_candidate,
            source_prior_information=self.source_prior_information,
            residuals=merged_residuals,
            binding_confidence=self.binding_confidence,
            binding_conditions=self.binding_conditions,
        )

    def describe(self) -> str:
        """Return human-readable description of binding."""
        dal_desc = getattr(self.dal_candidate, 'candidate_form', 'unknown_dal')
        madlul_desc = getattr(self.madlul_candidate, 'candidate_form', 'unknown_madlul')
        binding_desc = (
            self.binding_type.describe()
            if hasattr(self.binding_type, 'describe')
            else str(self.binding_type)
        )

        return f"{binding_desc}: {dal_desc} ← {madlul_desc}"


@dataclass(frozen=True)
class DalMadlulBindingResult:
    """
    Result of DalMadlulBinding operation.

    Attributes:
        candidate: Binding candidate if successful
        failure: Failure object if unsuccessful
        residuals: All accumulated residuals
    """

    candidate: Optional[DalMadlulBindingCandidate] = None
    failure: Optional[Any] = None  # DalMadlulBindingFailure
    residuals: Tuple[Any, ...] = ()

    def __post_init__(self):
        """Validate result has either candidate or failure, not both."""
        if self.candidate is not None and self.failure is not None:
            raise ValueError("Result cannot have both candidate and failure")

        if self.candidate is None and self.failure is None:
            raise ValueError("Result must have either candidate or failure")

    @property
    def is_success(self) -> bool:
        """Check if operation succeeded."""
        return self.candidate is not None and self.failure is None

    @property
    def is_failure(self) -> bool:
        """Check if operation failed."""
        return self.failure is not None and self.candidate is None

    @property
    def has_residuals(self) -> bool:
        """Check if result has residuals."""
        return len(self.residuals) > 0

    @classmethod
    def success(
        cls,
        candidate: DalMadlulBindingCandidate,
        residuals: Tuple[Any, ...] = (),
    ) -> "DalMadlulBindingResult":
        """
        Create successful result.

        Args:
            candidate: Binding candidate
            residuals: Optional residuals

        Returns:
            Successful DalMadlulBindingResult
        """
        return cls(candidate=candidate, residuals=residuals)

    @classmethod
    def failure(
        cls, failure: Any, residuals: Tuple[Any, ...] = ()
    ) -> "DalMadlulBindingResult":
        """
        Create failed result.

        Args:
            failure: Failure object
            residuals: Optional residuals

        Returns:
            Failed DalMadlulBindingResult
        """
        return cls(failure=failure, residuals=residuals)
