"""Manaat: Determine scope and basis of rule application.

Core Principle:
    المناط هو ما تدور معه الحكم وجوداً وعدماً.
    "The manaat (basis) is what determines the rule's presence or absence."

Central Law:
    لا قاعدة بلا مناط.
    "No rule without manaat (scope/basis)."

Architecture:
    The **Manaat** (المناط) is the determining factor that:
    1. Specifies the **scope** of rule application
    2. Distinguishes **when** the rule applies vs. when it doesn't
    3. May be morphological, semantic, contextual, or lexical
    4. Can be refined when counterexamples are found

    Manaat determines:
    - **Positive scope**: What the rule DOES cover
    - **Negative scope**: What the rule does NOT cover
    - **Boundary conditions**: Edge cases, exceptions
    - **Constraints**: Additional requirements for application

Example (فاعل Pattern):
    Initial manaat (too broad):
        "All فاعل patterns → agentive"

    Constraining examples found:
        طاهر (pure), حامض (sour), بارد (cold) → qualitative, not agentive

    Refined manaat:
        "فاعل patterns from event-denoting roots → agentive potential
         فاعل patterns from state-denoting roots → qualitative potential"

    Further refinement:
        "فاعل agentive/qualitative distinction depends on:
         1. Source root semantics (event vs. state)
         2. Lexicalization (frozen vs. productive)
         3. Context (syntactic position, modifiers)"
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Tuple, Mapping, Any, FrozenSet

from fvafk.algebra import Evidence, Residual, Rank


# ===========================================================================
# Manaat Scope
# ===========================================================================


class ManaatScope(Enum):
    """Scope types for rule application basis.

    The scope determines what aspect of the input determines rule application.
    """

    # Morphological scope
    PATTERN_ONLY = auto()               # وزن فقط (pattern alone)
    PATTERN_WITH_ROOT = auto()          # وزن + جذر (pattern + root type)
    PATTERN_WITH_AFFIXES = auto()       # وزن + زيادات (pattern + affixes)

    # Semantic scope
    ROOT_SEMANTICS = auto()             # دلالة الجذر (root meaning)
    DERIVATION_SEMANTICS = auto()       # دلالة الاشتقاق (derived meaning)
    LEXICAL_SEMANTICS = auto()          # دلالة معجمية (lexicon entry)

    # Contextual scope
    SYNTACTIC_CONTEXT = auto()          # سياق نحوي (syntactic position)
    SEMANTIC_CONTEXT = auto()           # سياق دلالي (semantic role)
    PRAGMATIC_CONTEXT = auto()          # سياق تداولي (discourse context)

    # Mixed scope
    MORPHOSEMANTICS = auto()            # صرف + دلالة
    MORPHOSYNTAX = auto()               # صرف + نحو
    FULL_CONTEXT = auto()               # سياق كامل


# ===========================================================================
# Manaat
# ===========================================================================


@dataclass(frozen=True)
class Manaat:
    """The determining factor (basis/scope) of a rule.

    A Manaat specifies WHEN a rule applies and WHEN it doesn't.

    Attributes:
        scope: The type of scope (PATTERN_ONLY, ROOT_SEMANTICS, etc.).
        positive_conditions: Conditions that MUST be met for rule to apply.
        negative_conditions: Conditions that PREVENT rule from applying.
        description: Human-readable description of the manaat.
        evidence: Supporting evidence for this manaat.
        residuals: Unresolved aspects (ambiguity, exceptions).
        confidence: Confidence in this manaat [0.0, 1.0].
        metadata: Additional information.

    Example:
        >>> manaat = Manaat(
        ...     scope=ManaatScope.PATTERN_WITH_ROOT,
        ...     positive_conditions=("pattern=فاعل", "root_type=event"),
        ...     negative_conditions=("root_type=state",),
        ...     description="فاعل from event roots → agentive",
        ...     confidence=0.85,
        ... )
        >>> manaat.scope
        <ManaatScope.PATTERN_WITH_ROOT: 2>
    """

    scope: ManaatScope
    positive_conditions: Tuple[str, ...] = ()
    negative_conditions: Tuple[str, ...] = ()
    description: str = ""
    evidence: Tuple[Evidence, ...] = ()
    residuals: Tuple[Residual, ...] = ()
    confidence: float = 0.7
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Manaat.confidence must be in [0.0, 1.0]")

    @property
    def is_clear(self) -> bool:
        """Check if manaat is clear (has conditions and confidence ≥ 0.7)."""
        has_conditions = bool(self.positive_conditions or self.negative_conditions)
        return has_conditions and self.confidence >= 0.7

    @property
    def is_ambiguous(self) -> bool:
        """Check if manaat is ambiguous (no clear conditions or low confidence)."""
        return not self.is_clear

    @property
    def is_too_broad(self) -> bool:
        """Check if manaat may be too broad (few/no negative conditions)."""
        return len(self.negative_conditions) == 0 and len(self.positive_conditions) < 2

    @property
    def is_too_narrow(self) -> bool:
        """Check if manaat may be too narrow (many constraints)."""
        total_conditions = len(self.positive_conditions) + len(self.negative_conditions)
        return total_conditions > 5

    def applies_to(self, conditions: FrozenSet[str]) -> bool:
        """Check if this manaat applies given a set of conditions.

        Args:
            conditions: Set of condition strings to check.

        Returns:
            True if all positive conditions are met and no negative conditions are met.

        Example:
            >>> manaat = Manaat(
            ...     scope=ManaatScope.PATTERN_WITH_ROOT,
            ...     positive_conditions=("pattern=فاعل", "root_type=event"),
            ...     negative_conditions=("root_type=state",),
            ... )
            >>> manaat.applies_to(frozenset({"pattern=فاعل", "root_type=event"}))
            True
            >>> manaat.applies_to(frozenset({"pattern=فاعل", "root_type=state"}))
            False
        """
        # Check all positive conditions are met
        for pos_cond in self.positive_conditions:
            if pos_cond not in conditions:
                return False

        # Check no negative conditions are met
        for neg_cond in self.negative_conditions:
            if neg_cond in conditions:
                return False

        return True


# ===========================================================================
# Manaat Determination
# ===========================================================================


def determine_manaat(
    invariants: Tuple[Any, ...],  # Should be Tuple[Invariant, ...] but avoiding circular import
    positive_examples: Tuple[Any, ...],  # Origin examples
    negative_examples: Tuple[Any, ...] = (),  # Counterexamples
) -> Manaat:
    """Determine the manaat (scope/basis) from invariants and examples.

    This function:
    1. Analyzes invariants to identify the primary determining factor
    2. Extracts positive conditions from positive examples
    3. Extracts negative conditions from negative examples
    4. Determines the scope type
    5. Computes confidence based on consistency

    Args:
        invariants: Detected invariant features.
        positive_examples: Examples where rule applies.
        negative_examples: Examples where rule does NOT apply.

    Returns:
        Manaat specifying when the rule applies.

    Example:
        >>> from fvafk.algebra.general_learning import Invariant, InvariantKind, Origin, Rank
        >>> inv = Invariant(kind=InvariantKind.PATTERN, value="فاعل", coverage=1.0, confidence=0.9)
        >>> pos1 = Origin(surface="كاتب", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> pos2 = Origin(surface="زارع", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> manaat = determine_manaat(invariants=(inv,), positive_examples=(pos1, pos2))
        >>> manaat.scope
        <ManaatScope.PATTERN_ONLY: 1>
    """
    if not invariants:
        raise ValueError("invariants must be non-empty")

    # Extract primary invariant (should be the strongest one)
    primary_inv = invariants[0]  # Assume first is primary/strongest

    # Determine scope based on invariant kind
    scope = _infer_scope_from_invariants(invariants)

    # Extract positive conditions
    positive_conditions = _extract_positive_conditions(invariants, positive_examples)

    # Extract negative conditions (from counterexamples)
    negative_conditions = _extract_negative_conditions(negative_examples)

    # Compute confidence based on consistency
    confidence = _compute_manaat_confidence(
        invariants, positive_examples, negative_examples
    )

    # Build description
    description = _build_manaat_description(
        primary_inv, positive_conditions, negative_conditions
    )

    # Collect evidence
    evidence_list = [
        Evidence(
            kind="manaat.determination",
            source="invariant_analysis",
            detail=f"Manaat determined from {len(invariants)} invariant(s)",
            weight=confidence,
        )
    ]

    # Identify residuals
    residuals_list = _identify_manaat_residuals(
        positive_conditions, negative_conditions, confidence
    )

    return Manaat(
        scope=scope,
        positive_conditions=positive_conditions,
        negative_conditions=negative_conditions,
        description=description,
        evidence=tuple(evidence_list),
        residuals=tuple(residuals_list),
        confidence=confidence,
    )


# ===========================================================================
# Helpers
# ===========================================================================


def _infer_scope_from_invariants(invariants: Tuple[Any, ...]) -> ManaatScope:
    """Infer manaat scope from invariant types."""
    # Count invariant kinds
    from .invariant import InvariantKind

    kinds = set()
    for inv in invariants:
        if hasattr(inv, "kind"):
            kinds.add(inv.kind)

    # Determine scope based on invariant kinds
    has_morphological = any(
        k
        in {
            InvariantKind.PATTERN,
            InvariantKind.ROOT_STRUCTURE,
            InvariantKind.AFFIX_SET,
        }
        for k in kinds
    )
    has_semantic = any(
        k
        in {
            InvariantKind.INTERPRETATION_TYPE,
            InvariantKind.SEMANTIC_ROLE,
            InvariantKind.AKTIONSART,
        }
        for k in kinds
    )
    has_syntactic = any(
        k
        in {
            InvariantKind.SYNTACTIC_CATEGORY,
            InvariantKind.ARGUMENT_STRUCTURE,
        }
        for k in kinds
    )

    if has_morphological and has_semantic:
        return ManaatScope.MORPHOSEMANTICS
    elif has_morphological and has_syntactic:
        return ManaatScope.MORPHOSYNTAX
    elif has_morphological:
        return ManaatScope.PATTERN_ONLY
    elif has_semantic:
        return ManaatScope.ROOT_SEMANTICS
    else:
        return ManaatScope.FULL_CONTEXT


def _extract_positive_conditions(
    invariants: Tuple[Any, ...], examples: Tuple[Any, ...]
) -> Tuple[str, ...]:
    """Extract positive conditions from invariants and examples."""
    conditions = []

    # Add invariant-based conditions
    for inv in invariants:
        if hasattr(inv, "kind") and hasattr(inv, "value"):
            kind_name = inv.kind.name.lower() if hasattr(inv.kind, "name") else "feature"
            conditions.append(f"{kind_name}={inv.value}")

    return tuple(conditions)


def _extract_negative_conditions(examples: Tuple[Any, ...]) -> Tuple[str, ...]:
    """Extract negative conditions from counterexamples."""
    if not examples:
        return ()

    conditions = []

    # Extract patterns/interpretations that should be excluded
    for ex in examples:
        if hasattr(ex, "interpretation") and ex.interpretation:
            # If counterexample has different interpretation, add negative condition
            conditions.append(f"not_interpretation={ex.interpretation}")

    return tuple(conditions)


def _compute_manaat_confidence(
    invariants: Tuple[Any, ...],
    positive_examples: Tuple[Any, ...],
    negative_examples: Tuple[Any, ...],
) -> float:
    """Compute confidence in manaat based on consistency."""
    # Start with average invariant confidence
    if invariants:
        inv_confidences = [
            getattr(inv, "confidence", 0.7) for inv in invariants if hasattr(inv, "confidence")
        ]
        base_confidence = sum(inv_confidences) / len(inv_confidences) if inv_confidences else 0.7
    else:
        base_confidence = 0.5

    # Boost if we have negative examples (helps define boundaries)
    if negative_examples:
        base_confidence = min(base_confidence * 1.1, 1.0)

    # Reduce if few positive examples
    if len(positive_examples) < 3:
        base_confidence *= 0.9

    return min(base_confidence, 1.0)


def _build_manaat_description(
    primary_inv: Any, positive_conds: Tuple[str, ...], negative_conds: Tuple[str, ...]
) -> str:
    """Build human-readable manaat description."""
    parts = []

    # Add primary invariant
    if hasattr(primary_inv, "value"):
        parts.append(f"Rule applies when: {primary_inv.value}")

    # Add positive conditions
    if positive_conds:
        parts.append(f"Requires: {', '.join(positive_conds)}")

    # Add negative conditions
    if negative_conds:
        parts.append(f"Excludes: {', '.join(negative_conds)}")

    return " | ".join(parts) if parts else "Manaat unclear"


def _identify_manaat_residuals(
    positive_conds: Tuple[str, ...], negative_conds: Tuple[str, ...], confidence: float
) -> list[Residual]:
    """Identify residuals in manaat determination."""
    residuals = []

    # Check if manaat is ambiguous
    if not positive_conds and not negative_conds:
        residuals.append(
            Residual(
                kind="manaat.ambiguous",
                description="No clear conditions identified for rule application",
            )
        )

    # Check if manaat is too broad
    if positive_conds and not negative_conds:
        residuals.append(
            Residual(
                kind="manaat.too_broad",
                description="No negative conditions; rule may over-generalize",
            )
        )

    # Check if confidence is low
    if confidence < 0.7:
        residuals.append(
            Residual(
                kind="manaat.ambiguous",
                description=f"Low confidence ({confidence:.2f}); manaat may be unclear",
            )
        )

    return residuals


__all__ = [
    "ManaatScope",
    "Manaat",
    "determine_manaat",
]
