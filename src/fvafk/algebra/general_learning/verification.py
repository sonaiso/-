"""Verification: Counterexample detection and rule refinement.

Core Principle:
    المثال المضاد ليس فشلاً؛ بل هو فرصة لتحسين القاعدة.
    "A counterexample is not a failure; it is an opportunity to refine the rule."

Central Law:
    كل قاعدة يجب أن تُختبر على أمثلة مضادة.
    "Every rule must be tested against counterexamples."

Architecture:
    **Verification** is the process that:
    1. Tests a rule against new examples
    2. Detects counterexamples (violations)
    3. Classifies counterexample types
    4. Suggests refinements
    5. Tracks verification history

    Counterexample Types:
    - **False Positive**: Rule applies but shouldn't
    - **False Negative**: Rule doesn't apply but should
    - **Scope Error**: Rule scope is wrong
    - **Manaat Error**: Determining factor is wrong

Example (فاعل Pattern):
    Rule: "All فاعل → agentive"

    Counterexamples found:
        طاهر (pure) → qualitative, not agentive  [FALSE POSITIVE]
        حامض (sour) → qualitative, not agentive  [FALSE POSITIVE]
        بارد (cold) → qualitative, not agentive  [FALSE POSITIVE]

    Refinement suggested:
        Scope narrowing: "فاعل from event roots → agentive"
        OR
        Scope broadening: "فاعل → agentive OR qualitative"
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Tuple, Mapping, Any

from fvafk.algebra import Evidence, Residual, Rank, Trace


# ===========================================================================
# Counterexample Types
# ===========================================================================


class CounterexampleKind(Enum):
    """Types of counterexamples that can be detected.

    Each kind indicates a different type of rule violation.
    """

    FALSE_POSITIVE = auto()     # Rule applies but shouldn't
    FALSE_NEGATIVE = auto()     # Rule doesn't apply but should
    SCOPE_TOO_BROAD = auto()    # Rule over-generalizes
    SCOPE_TOO_NARROW = auto()   # Rule under-generalizes
    MANAAT_ERROR = auto()       # Wrong determining factor
    EXCEPTION = auto()          # Legitimate exception (not error)


# ===========================================================================
# Counterexample
# ===========================================================================


@dataclass(frozen=True)
class Counterexample:
    """An example that violates the current rule.

    Attributes:
        surface: Surface form (e.g., "طاهر").
        pattern: Pattern (e.g., "فاعل").
        expected: What the rule predicts.
        actual: What is actually observed.
        kind: Type of counterexample.
        evidence: Evidence that this is indeed a counterexample.
        description: Human-readable description.
        metadata: Additional information.

    Example:
        >>> ce = Counterexample(
        ...     surface="طاهر",
        ...     pattern="فاعل",
        ...     expected="agentive",
        ...     actual="qualitative",
        ...     kind=CounterexampleKind.FALSE_POSITIVE,
        ...     description="Rule predicts agentive but actual is qualitative",
        ... )
        >>> ce.kind
        <CounterexampleKind.FALSE_POSITIVE: 1>
    """

    surface: str
    pattern: str
    expected: str
    actual: str
    kind: CounterexampleKind
    evidence: Tuple[Evidence, ...] = ()
    description: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.surface:
            raise ValueError("Counterexample.surface must be non-empty")
        if not self.pattern:
            raise ValueError("Counterexample.pattern must be non-empty")

    @property
    def requires_refinement(self) -> bool:
        """Check if this counterexample requires rule refinement."""
        # Exceptions can be noted but don't require refinement
        return self.kind is not CounterexampleKind.EXCEPTION

    @property
    def suggests_scope_narrowing(self) -> bool:
        """Check if this counterexample suggests narrowing rule scope."""
        return self.kind in {
            CounterexampleKind.FALSE_POSITIVE,
            CounterexampleKind.SCOPE_TOO_BROAD,
        }

    @property
    def suggests_scope_broadening(self) -> bool:
        """Check if this counterexample suggests broadening rule scope."""
        return self.kind in {
            CounterexampleKind.FALSE_NEGATIVE,
            CounterexampleKind.SCOPE_TOO_NARROW,
        }


# ===========================================================================
# Verification Result
# ===========================================================================


@dataclass(frozen=True)
class VerificationResult:
    """Result of verifying a rule against examples.

    Attributes:
        rule: The rule being verified.
        counterexamples: Counterexamples detected.
        confirmed_examples: Examples that confirmed the rule.
        refinement_suggestions: Suggested refinements.
        evidence: Evidence from verification.
        residuals: Residuals from verification.
        rank: Resulting rank after verification.
        trace: Provenance trace.

    Example:
        >>> result = VerificationResult(
        ...     rule=some_rule,
        ...     counterexamples=(ce1, ce2),
        ...     confirmed_examples=(ex1, ex2, ex3),
        ...     refinement_suggestions=("Narrow scope to event roots",),
        ...     rank=Rank.CANDIDATE,
        ... )
        >>> result.has_counterexamples
        True
        >>> result.needs_refinement
        True
    """

    rule: Any  # Should be RuleCandidate but avoiding circular import
    counterexamples: Tuple[Counterexample, ...] = ()
    confirmed_examples: Tuple[Any, ...] = ()
    refinement_suggestions: Tuple[str, ...] = ()
    evidence: Tuple[Evidence, ...] = ()
    residuals: Tuple[Residual, ...] = ()
    rank: Rank = Rank.CANDIDATE
    trace: Trace = field(default_factory=lambda: Trace(operation="rule_verification"))

    @property
    def has_counterexamples(self) -> bool:
        """Check if counterexamples were found."""
        return bool(self.counterexamples)

    @property
    def needs_refinement(self) -> bool:
        """Check if rule needs refinement."""
        return any(ce.requires_refinement for ce in self.counterexamples)

    @property
    def is_confirmed(self) -> bool:
        """Check if rule is confirmed (no counterexamples)."""
        return not self.has_counterexamples and bool(self.confirmed_examples)

    @property
    def confirmation_rate(self) -> float:
        """Get fraction of examples that confirmed the rule."""
        total = len(self.confirmed_examples) + len(self.counterexamples)
        if total == 0:
            return 0.0
        return len(self.confirmed_examples) / total


# ===========================================================================
# Verification Functions
# ===========================================================================


def verify_rule(
    rule: Any,  # Should be RuleCandidate
    test_examples: Tuple[Any, ...],  # Should be Tuple[Origin, ...]
) -> VerificationResult:
    """Verify a rule against test examples.

    This function:
    1. Tests each example against the rule
    2. Detects counterexamples
    3. Classifies counterexample types
    4. Suggests refinements
    5. Computes new rank

    Args:
        rule: The rule to verify.
        test_examples: Examples to test against.

    Returns:
        VerificationResult with counterexamples and suggestions.

    Example:
        >>> from fvafk.algebra.general_learning import RuleCandidate, Origin, Manaat, ManaatScope
        >>> rule = RuleCandidate(
        ...     description="All فاعل → agentive",
        ...     pattern="فاعل",
        ...     manaat=Manaat(scope=ManaatScope.PATTERN_ONLY, positive_conditions=("pattern=فاعل",)),
        ...     rank=Rank.CANDIDATE,
        ... )
        >>> ex1 = Origin(surface="طاهر", pattern="فاعل", interpretation="qualitative", rank=Rank.LICENSED)
        >>> result = verify_rule(rule, test_examples=(ex1,))
        >>> result.has_counterexamples
        True
    """
    if not test_examples:
        return VerificationResult(
            rule=rule,
            rank=Rank.UNRESOLVED,
            residuals=(Residual(kind="verification.no_examples", description="No test examples provided"),),
        )

    counterexamples = []
    confirmed = []

    # Test each example
    for example in test_examples:
        ce = _check_example_against_rule(rule, example)
        if ce is not None:
            counterexamples.append(ce)
        else:
            confirmed.append(example)

    # Generate refinement suggestions
    suggestions = _generate_refinement_suggestions(counterexamples)

    # Compute new rank
    new_rank = _compute_verification_rank(rule, counterexamples, confirmed)

    # Generate evidence
    # Weight must be strictly positive; use confirmation rate or minimum 0.01
    confirmation_rate = len(confirmed) / len(test_examples) if test_examples else 0.0
    evidence_weight = max(0.01, confirmation_rate)  # Ensure strictly positive

    evidence_list = [
        Evidence(
            kind="rule.verification",
            source="verification_test",
            detail=f"Tested {len(test_examples)} examples: {len(confirmed)} confirmed, {len(counterexamples)} counterexamples",
            weight=evidence_weight,
        )
    ]

    # Generate residuals
    residuals_list = _generate_verification_residuals(counterexamples)

    return VerificationResult(
        rule=rule,
        counterexamples=tuple(counterexamples),
        confirmed_examples=tuple(confirmed),
        refinement_suggestions=tuple(suggestions),
        evidence=tuple(evidence_list),
        residuals=tuple(residuals_list),
        rank=new_rank,
    )


def detect_counterexamples(
    rule: Any,  # Should be RuleCandidate
    examples: Tuple[Any, ...],  # Should be Tuple[Origin, ...]
) -> Tuple[Counterexample, ...]:
    """Detect counterexamples in a set of examples.

    Args:
        rule: The rule to test against.
        examples: Examples to check.

    Returns:
        Tuple of counterexamples found.

    Example:
        >>> counterexamples = detect_counterexamples(rule, examples=(ex1, ex2, ex3))
        >>> len(counterexamples)
        2
    """
    counterexamples = []
    for example in examples:
        ce = _check_example_against_rule(rule, example)
        if ce is not None:
            counterexamples.append(ce)
    return tuple(counterexamples)


# ===========================================================================
# Helpers
# ===========================================================================


def _check_example_against_rule(rule: Any, example: Any) -> Counterexample | None:
    """Check if an example violates the rule.

    Returns None if example confirms rule, Counterexample if it violates.
    """
    # Extract rule pattern
    rule_pattern = getattr(rule, "pattern", "")

    # Extract example actuals
    example_pattern = getattr(example, "pattern", "")
    actual_interpretation = getattr(example, "interpretation", "")

    # Check if patterns match
    if not example_pattern or example_pattern != rule_pattern:
        # Pattern doesn't match; not a counterexample to this rule
        return None

    # Check if interpretation available
    if not actual_interpretation:
        # No interpretation available; can't verify
        return None

    # Use InterpretationClaim if available, otherwise fall back to description parsing
    interpretation_claim = getattr(rule, "interpretation_claim", None)

    if interpretation_claim is not None:
        # Use structured claim
        if not interpretation_claim.matches(actual_interpretation):
            # This is a counterexample: interpretation not in expected set
            primary = interpretation_claim.primary_interpretation or next(iter(interpretation_claim.expected_interpretations))
            return Counterexample(
                surface=getattr(example, "surface", ""),
                pattern=example_pattern,
                expected=primary,
                actual=actual_interpretation,
                kind=CounterexampleKind.FALSE_POSITIVE,
                description=f"Rule expects one of {set(interpretation_claim.expected_interpretations)}, but got '{actual_interpretation}'",
                evidence=(
                    Evidence(
                        kind="counterexample.detection",
                        source=getattr(example, "surface", ""),
                        detail=f"Pattern {example_pattern} with interpretation {actual_interpretation}",
                        weight=1.0,
                    ),
                ),
            )
    else:
        # Fall back to legacy description parsing
        expected_interpretation = _extract_expected_interpretation(rule)

        if actual_interpretation != expected_interpretation:
            # This is a counterexample: pattern matches but interpretation doesn't
            return Counterexample(
                surface=getattr(example, "surface", ""),
                pattern=example_pattern,
                expected=expected_interpretation,
                actual=actual_interpretation,
                kind=CounterexampleKind.FALSE_POSITIVE,
                description=f"Rule predicts '{expected_interpretation}' but actual is '{actual_interpretation}'",
                evidence=(
                    Evidence(
                        kind="counterexample.detection",
                        source=getattr(example, "surface", ""),
                        detail=f"Pattern {example_pattern} with interpretation {actual_interpretation}",
                        weight=1.0,
                    ),
                ),
            )

    # Example confirms the rule
    return None


def _extract_expected_interpretation(rule: Any) -> str:
    """Extract expected interpretation from rule description.

    DEPRECATED: This function parses description strings which is fragile.
    Use rule.interpretation_claim (InterpretationClaim) instead.

    This function is kept for backward compatibility with rules that don't
    have interpretation_claim set.
    """
    # Simplified: look for keywords in description
    description = getattr(rule, "description", "").lower()

    if "agentive" in description or "فاعلية" in description:
        return "agentive"
    elif "qualitative" in description or "وصفية" in description:
        return "qualitative"
    elif "patient" in description or "مفعولية" in description:
        return "patient"
    else:
        # Extract from manaat or invariants if possible
        return "unknown"


def _generate_refinement_suggestions(counterexamples: list[Counterexample]) -> list[str]:
    """Generate refinement suggestions based on counterexamples."""
    if not counterexamples:
        return []

    suggestions = []

    # Count counterexample types
    false_positives = sum(1 for ce in counterexamples if ce.kind is CounterexampleKind.FALSE_POSITIVE)
    false_negatives = sum(1 for ce in counterexamples if ce.kind is CounterexampleKind.FALSE_NEGATIVE)

    if false_positives > 0:
        suggestions.append(
            f"Narrow scope: {false_positives} false positive(s) suggest rule over-generalizes"
        )
        suggestions.append(
            "Consider adding constraints based on root semantics or lexicalization"
        )

    if false_negatives > 0:
        suggestions.append(
            f"Broaden scope: {false_negatives} false negative(s) suggest rule under-generalizes"
        )

    # Suggest alternatives based on actual interpretations
    actual_interps = {ce.actual for ce in counterexamples}
    if len(actual_interps) == 1:
        alt_interp = next(iter(actual_interps))
        suggestions.append(
            f"Consider alternative interpretation: pattern may license '{alt_interp}' in some contexts"
        )

    return suggestions


def _compute_verification_rank(
    rule: Any, counterexamples: list[Counterexample], confirmed: list[Any]
) -> Rank:
    """Compute new rank based on verification results."""
    if not confirmed and not counterexamples:
        return Rank.UNRESOLVED

    if counterexamples:
        # Has counterexamples; demote
        return Rank.CANDIDATE

    # No counterexamples; confirm
    if len(confirmed) >= 3:
        return Rank.LICENSED
    else:
        return Rank.CANDIDATE


def _generate_verification_residuals(counterexamples: list[Counterexample]) -> list[Residual]:
    """Generate residuals from verification."""
    residuals = []

    if counterexamples:
        for ce in counterexamples:
            residuals.append(
                Residual(
                    kind="counterexample.unresolved",
                    description=f"Counterexample '{ce.surface}': {ce.description}",
                )
            )

    return residuals


__all__ = [
    "CounterexampleKind",
    "Counterexample",
    "VerificationResult",
    "verify_rule",
    "detect_counterexamples",
]
