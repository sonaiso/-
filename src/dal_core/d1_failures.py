"""D1 Typed Failure Algebra.

Replaces generic residuals with structured, typed failures.

Each failure type encodes:
- What went wrong
- Where it happened
- Why it matters
- How to recover (if possible)
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Any


class D1FailureType(Enum):
    """Typed failure categories for D1 (SYLLABIC domain)."""

    # Atom sequence failures
    INVALID_ATOM_SEQUENCE = auto()      # Atoms don't form valid syllable
    EMPTY_SEQUENCE = auto()             # No atoms provided
    ATOM_KIND_MISMATCH = auto()         # Wrong atom kinds for syllable

    # Structure failures
    MISSING_NUCLEUS = auto()            # No vowel found
    MISSING_ONSET = auto()              # No initial consonant
    ILLEGAL_SYLLABLE_PATTERN = auto()   # Pattern not in {CV, CVC, CVV, CVVC, CVCC}
    INVALID_CODA = auto()               # Coda structure invalid

    # Boundary failures
    BOUNDARY_AMBIGUITY = auto()         # Multiple valid boundary interpretations
    SPAN_MISMATCH = auto()              # Span doesn't match atom count
    OVERLAP_DETECTED = auto()           # Syllables overlap

    # Long vowel failures
    LONG_VOWEL_AMBIGUITY = auto()       # Unclear if sequence is long vowel
    INCOMPLETE_LONG_VOWEL = auto()      # Long vowel pattern incomplete

    # Special atom failures
    SHADDA_EXPANSION_FAILURE = auto()   # Can't expand shadda properly
    SUKUN_CONFLICT = auto()             # Sukun in invalid position
    TANWIN_PLACEMENT_ERROR = auto()     # Tanwin incorrectly placed
    HAMZA_HANDLING_ERROR = auto()       # Hamza not handled correctly

    # Trace failures
    TRACE_LOSS = auto()                 # Cannot trace back to atoms
    NON_REVERSIBLE_TRACE = auto()       # Trace claims reversible but isn't

    # Resource failures
    CANDIDATE_OVERFLOW = auto()         # Too many candidates generated

    # Conservation failures
    ATOM_LOSS = auto()                  # Atoms lost during syllabification
    ATOM_ORDER_VIOLATION = auto()       # Atom order not preserved
    SPAN_CORRUPTION = auto()            # Span boundaries corrupted


@dataclass
class D1Failure:
    """Structured failure object for D1 domain.

    Replaces generic Residual with typed, actionable failure.
    """
    failure_type: D1FailureType
    span: tuple[int, int]               # Where failure occurred
    message: str                        # Human-readable description
    severity: float = 1.0               # Severity [0.0, 1.0], 1.0 = critical
    recovery_hint: str = ""             # How to fix/handle
    context: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate failure invariants."""
        if not (0.0 <= self.severity <= 1.0):
            raise ValueError(f"Severity must be in [0.0, 1.0], got {self.severity}")
        if self.span[0] > self.span[1]:
            raise ValueError(f"Invalid span: start > end ({self.span})")
        if self.span[0] < 0:
            raise ValueError(f"Invalid span: negative start ({self.span})")

    def is_critical(self) -> bool:
        """Check if this is a critical (blocking) failure."""
        return self.severity >= 0.8

    def is_warning(self) -> bool:
        """Check if this is a warning (non-blocking)."""
        return self.severity < 0.5

    def __str__(self) -> str:
        """Human-readable failure representation."""
        severity_mark = "🔴" if self.is_critical() else ("⚠️" if self.severity >= 0.5 else "ℹ️")
        return f"{severity_mark} {self.failure_type.name} at {self.span}: {self.message}"


@dataclass
class D1FailureSet:
    """Collection of failures for a syllabification attempt."""
    failures: List[D1Failure] = field(default_factory=list)
    global_context: dict[str, Any] = field(default_factory=dict)

    def add(self, failure: D1Failure):
        """Add a failure to the set."""
        self.failures.append(failure)

    def has_critical_failure(self) -> bool:
        """Check if any critical failure exists."""
        return any(f.is_critical() for f in self.failures)

    def critical_failures(self) -> List[D1Failure]:
        """Get all critical failures."""
        return [f for f in self.failures if f.is_critical()]

    def warnings(self) -> List[D1Failure]:
        """Get all warnings."""
        return [f for f in self.failures if f.is_warning()]

    def by_type(self, failure_type: D1FailureType) -> List[D1Failure]:
        """Get failures of specific type."""
        return [f for f in self.failures if f.failure_type == failure_type]

    def summary(self) -> str:
        """Summary of all failures."""
        critical = len(self.critical_failures())
        warnings = len(self.warnings())
        total = len(self.failures)
        return f"{total} failures ({critical} critical, {warnings} warnings)"


# ============================================================================
# Failure Constructors (Factory Functions)
# ============================================================================


def make_empty_sequence_failure(span: tuple[int, int] = (0, 0)) -> D1Failure:
    """Create failure for empty atom sequence."""
    return D1Failure(
        failure_type=D1FailureType.EMPTY_SEQUENCE,
        span=span,
        message="Empty atom sequence provided",
        severity=1.0,
        recovery_hint="Provide at least one atom for syllabification"
    )


def make_missing_nucleus_failure(
    span: tuple[int, int],
    onset_count: int = 0
) -> D1Failure:
    """Create failure for missing nucleus (vowel)."""
    return D1Failure(
        failure_type=D1FailureType.MISSING_NUCLEUS,
        span=span,
        message=f"No nucleus (vowel) found after {onset_count} onset consonant(s)",
        severity=1.0,
        recovery_hint="Arabic syllables require a vowel nucleus",
        context={'onset_count': onset_count}
    )


def make_missing_onset_failure(span: tuple[int, int]) -> D1Failure:
    """Create failure for missing onset (initial consonant)."""
    return D1Failure(
        failure_type=D1FailureType.MISSING_ONSET,
        span=span,
        message="Syllable must start with consonant onset",
        severity=0.9,
        recovery_hint="Arabic syllables typically require onset consonant"
    )


def make_illegal_pattern_failure(
    span: tuple[int, int],
    attempted_pattern: str
) -> D1Failure:
    """Create failure for illegal syllable pattern."""
    return D1Failure(
        failure_type=D1FailureType.ILLEGAL_SYLLABLE_PATTERN,
        span=span,
        message=f"Illegal syllable pattern: {attempted_pattern}",
        severity=1.0,
        recovery_hint="Legal patterns: CV, CVC, CVV, CVVC, CVCC",
        context={'attempted_pattern': attempted_pattern}
    )


def make_boundary_ambiguity_failure(
    span: tuple[int, int],
    candidate_count: int,
    ambiguity_type: str = "general"
) -> D1Failure:
    """Create failure for boundary ambiguity."""
    return D1Failure(
        failure_type=D1FailureType.BOUNDARY_AMBIGUITY,
        span=span,
        message=f"Boundary ambiguity: {candidate_count} possible interpretations",
        severity=0.6,
        recovery_hint="Consider context or preserve all candidates",
        context={
            'candidate_count': candidate_count,
            'ambiguity_type': ambiguity_type
        }
    )


def make_long_vowel_ambiguity_failure(
    span: tuple[int, int],
    sequence: str
) -> D1Failure:
    """Create failure for long vowel ambiguity."""
    return D1Failure(
        failure_type=D1FailureType.LONG_VOWEL_AMBIGUITY,
        span=span,
        message=f"Ambiguous long vowel sequence: {sequence}",
        severity=0.5,
        recovery_hint="Check for fatha+alif, damma+waw, kasra+ya patterns",
        context={'sequence': sequence}
    )


def make_shadda_expansion_failure(
    span: tuple[int, int],
    consonant: str
) -> D1Failure:
    """Create failure for shadda expansion."""
    return D1Failure(
        failure_type=D1FailureType.SHADDA_EXPANSION_FAILURE,
        span=span,
        message=f"Cannot expand shadda on '{consonant}'",
        severity=0.7,
        recovery_hint="Shadda requires consonant gemination",
        context={'consonant': consonant}
    )


def make_sukun_conflict_failure(
    span: tuple[int, int],
    position: str
) -> D1Failure:
    """Create failure for sukun conflict."""
    return D1Failure(
        failure_type=D1FailureType.SUKUN_CONFLICT,
        span=span,
        message=f"Sukun in invalid position: {position}",
        severity=0.8,
        recovery_hint="Sukun typically appears word-finally or in coda",
        context={'position': position}
    )


def make_trace_loss_failure(span: tuple[int, int]) -> D1Failure:
    """Create failure for trace loss."""
    return D1Failure(
        failure_type=D1FailureType.TRACE_LOSS,
        span=span,
        message="Cannot trace syllable back to source atoms",
        severity=1.0,
        recovery_hint="Trace must be reversible in dal_algebra"
    )


def make_atom_loss_failure(
    span: tuple[int, int],
    expected_count: int,
    actual_count: int
) -> D1Failure:
    """Create failure for atom loss."""
    return D1Failure(
        failure_type=D1FailureType.ATOM_LOSS,
        span=span,
        message=f"Atoms lost: expected {expected_count}, got {actual_count}",
        severity=1.0,
        recovery_hint="All atoms must be preserved in syllable structure",
        context={
            'expected_count': expected_count,
            'actual_count': actual_count,
            'lost_count': expected_count - actual_count
        }
    )


def make_atom_order_violation_failure(
    span: tuple[int, int],
    position: int
) -> D1Failure:
    """Create failure for atom order violation."""
    return D1Failure(
        failure_type=D1FailureType.ATOM_ORDER_VIOLATION,
        span=span,
        message=f"Atom order violated at position {position}",
        severity=1.0,
        recovery_hint="Atom sequence order must be preserved",
        context={'violation_position': position}
    )


def make_span_mismatch_failure(
    span: tuple[int, int],
    expected_length: int,
    actual_length: int
) -> D1Failure:
    """Create failure for span mismatch."""
    return D1Failure(
        failure_type=D1FailureType.SPAN_MISMATCH,
        span=span,
        message=f"Span mismatch: expected length {expected_length}, got {actual_length}",
        severity=0.9,
        recovery_hint="Verify span boundaries match atom count",
        context={
            'expected_length': expected_length,
            'actual_length': actual_length
        }
    )


def make_non_reversible_trace_failure(span: tuple[int, int]) -> D1Failure:
    """Create failure for non-reversible trace."""
    return D1Failure(
        failure_type=D1FailureType.NON_REVERSIBLE_TRACE,
        span=span,
        message="Trace claims reversible but reverse operation failed",
        severity=1.0,
        recovery_hint="Trace must support actual reverse operation, not just flag"
    )


def make_candidate_overflow_failure(
    span: tuple[int, int],
    candidate_count: int,
    limit: int
) -> D1Failure:
    """Create failure for too many candidates."""
    return D1Failure(
        failure_type=D1FailureType.CANDIDATE_OVERFLOW,
        span=span,
        message=f"Too many candidates: {candidate_count} exceeds limit {limit}",
        severity=0.7,
        recovery_hint="Use stricter boundary rules or increase limit",
        context={
            'candidate_count': candidate_count,
            'limit': limit
        }
    )


# ============================================================================
# Failure Recovery Strategies
# ============================================================================


def suggest_recovery(failure: D1Failure) -> List[str]:
    """Suggest recovery strategies for a failure.

    Args:
        failure: The failure to recover from

    Returns:
        List of recovery strategy suggestions
    """
    strategies = []

    if failure.failure_type == D1FailureType.MISSING_NUCLEUS:
        strategies.append("Insert default vowel (fatha)")
        strategies.append("Check for hidden vowel markers")
        strategies.append("Treat as exceptional frozen form")

    elif failure.failure_type == D1FailureType.BOUNDARY_AMBIGUITY:
        strategies.append("Preserve all candidate interpretations")
        strategies.append("Use context from adjacent syllables")
        strategies.append("Apply statistical likelihood ranking")

    elif failure.failure_type == D1FailureType.LONG_VOWEL_AMBIGUITY:
        strategies.append("Check for madd letters (alif, waw, ya)")
        strategies.append("Examine vowel before madd letter")
        strategies.append("Consider word etymology")

    elif failure.failure_type == D1FailureType.SHADDA_EXPANSION_FAILURE:
        strategies.append("Duplicate consonant (CVC → CVCC)")
        strategies.append("Check if consonant gemination allowed")
        strategies.append("Verify shadda position (not word-initial)")

    elif failure.failure_type == D1FailureType.ATOM_LOSS:
        strategies.append("Verify syllable structure includes all atoms")
        strategies.append("Check for filtering of non-structural atoms")
        strategies.append("Reconstruct from trace")

    # Add general hint from failure if available
    if failure.recovery_hint:
        strategies.insert(0, failure.recovery_hint)

    return strategies


def is_recoverable(failure: D1Failure) -> bool:
    """Check if a failure is potentially recoverable.

    Args:
        failure: The failure to check

    Returns:
        True if recovery strategies exist
    """
    recoverable_types = {
        D1FailureType.BOUNDARY_AMBIGUITY,
        D1FailureType.LONG_VOWEL_AMBIGUITY,
        D1FailureType.SUKUN_CONFLICT,
        D1FailureType.CANDIDATE_OVERFLOW
    }

    return failure.failure_type in recoverable_types
