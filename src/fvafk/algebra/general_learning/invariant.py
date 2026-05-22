"""Invariant: Detect stable patterns across origin examples.

Core Principle:
    الثابت هو ما يتكرر في جميع الأصول.
    "The invariant is what repeats across all origins."

Central Law:
    لا قاعدة بلا ثابت.
    "No rule without invariant."

Architecture:
    An **Invariant** is a stable feature that:
    1. Appears in all (or most) origin examples
    2. Distinguishes the pattern from other patterns
    3. Can be morphological, phonological, or semantic
    4. Forms the basis for rule formulation

    Invariants can be:
    - **Morphological**: Pattern (وزن), affixes, root structure
    - **Phonological**: Vowel melody, consonant structure
    - **Semantic**: Interpretation type (agentive, qualitative, etc.)
    - **Distributional**: Syntactic behavior, usage patterns

Example (فاعل Pattern):
    Origins: كاتب، زارع، عامل

    Invariants detected:
    1. Morphological: فاعل pattern (ف-ا-ع-ِ-ل)
    2. Semantic: Agentive interpretation (doer of action)
    3. Derivational: Derived from triliteral roots
    4. Syntactic: Can function as noun or adjective

    Strongest invariant:
        فاعل pattern → agentive potential
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Tuple, Any, Mapping, FrozenSet

from fvafk.algebra import Evidence, Residual, Rank


# ===========================================================================
# Invariant Kinds
# ===========================================================================


class InvariantKind(Enum):
    """Types of invariant features that can be detected.

    Each kind represents a different level or aspect of the pattern.
    """

    # Morphological invariants
    PATTERN = auto()                # وزن (morphological template)
    ROOT_STRUCTURE = auto()         # بنية الجذر (root composition)
    AFFIX_SET = auto()              # مجموعة الزيادات (affix inventory)

    # Phonological invariants
    VOWEL_MELODY = auto()           # لحن الصوائت (vowel pattern)
    CONSONANT_FRAME = auto()        # إطار الصوامت (consonant skeleton)
    SYLLABLE_PATTERN = auto()       # نمط المقاطع (syllable structure)

    # Semantic invariants
    INTERPRETATION_TYPE = auto()    # نوع التفسير (agentive, qualitative, etc.)
    SEMANTIC_ROLE = auto()          # الدور الدلالي (agent, patient, etc.)
    AKTIONSART = auto()             # النوع الحدثي (state, process, etc.)

    # Distributional invariants
    SYNTACTIC_CATEGORY = auto()     # الصنف النحوي (noun, adjective, etc.)
    ARGUMENT_STRUCTURE = auto()     # البنية الحجاجية (valency, case pattern)
    USAGE_CONTEXT = auto()          # سياق الاستعمال (typical contexts)

    # Derivational invariants
    SOURCE_CATEGORY = auto()        # الصنف المصدري (from verb, noun, etc.)
    DERIVATION_LEVEL = auto()       # مستوى الاشتقاق (primary, secondary)
    PRODUCTIVITY = auto()           # الإنتاجية (productive vs. frozen)


# ===========================================================================
# Invariant
# ===========================================================================


@dataclass(frozen=True)
class Invariant:
    """A stable feature detected across origin examples.

    An invariant is NOT a simple string or value; it is a **governed feature**
    with evidence, confidence, and stability metrics.

    Attributes:
        kind: The type of invariant (PATTERN, INTERPRETATION_TYPE, etc.).
        value: The invariant value (e.g., "فاعل", "agentive").
        description: Human-readable description.
        coverage: Fraction of origins that exhibit this invariant [0.0, 1.0].
        confidence: Confidence in this invariant [0.0, 1.0].
        evidence: Supporting evidence for this invariant.
        residuals: Unresolved aspects (e.g., exceptions, ambiguity).
        metadata: Additional information.

    Example:
        >>> inv = Invariant(
        ...     kind=InvariantKind.PATTERN,
        ...     value="فاعل",
        ...     description="Morphological pattern فاعل (fa'il)",
        ...     coverage=1.0,
        ...     confidence=0.9,
        ...     evidence=(Evidence(kind="pattern.match", source="all_origins", detail="100% coverage"),),
        ... )
        >>> inv.kind
        <InvariantKind.PATTERN: 1>
        >>> inv.value
        'فاعل'
        >>> inv.is_stable
        True
    """

    kind: InvariantKind
    value: str
    description: str = ""
    coverage: float = 1.0   # Fraction of origins with this feature [0.0, 1.0]
    confidence: float = 0.7  # Confidence in this invariant [0.0, 1.0]
    evidence: Tuple[Evidence, ...] = ()
    residuals: Tuple[Residual, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.value:
            raise ValueError("Invariant.value must be non-empty")
        if not 0.0 <= self.coverage <= 1.0:
            raise ValueError("Invariant.coverage must be in [0.0, 1.0]")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Invariant.confidence must be in [0.0, 1.0]")

    @property
    def is_stable(self) -> bool:
        """Check if invariant is stable (coverage ≥ 0.8 and confidence ≥ 0.7)."""
        return self.coverage >= 0.8 and self.confidence >= 0.7

    @property
    def is_universal(self) -> bool:
        """Check if invariant is universal (coverage = 1.0)."""
        return self.coverage == 1.0

    @property
    def has_exceptions(self) -> bool:
        """Check if invariant has exceptions (coverage < 1.0)."""
        return self.coverage < 1.0

    @property
    def strength(self) -> float:
        """Get invariant strength (coverage × confidence)."""
        return self.coverage * self.confidence


# ===========================================================================
# Invariant Set
# ===========================================================================


@dataclass(frozen=True)
class InvariantSet:
    """A collection of invariants detected from an origin set.

    Attributes:
        invariants: The detected invariants.
        primary: The strongest/most reliable invariant.
        rank: Epistemic rank of the invariant set.

    Example:
        >>> inv1 = Invariant(kind=InvariantKind.PATTERN, value="فاعل", coverage=1.0, confidence=0.9)
        >>> inv2 = Invariant(kind=InvariantKind.INTERPRETATION_TYPE, value="agentive", coverage=1.0, confidence=0.8)
        >>> inv_set = InvariantSet(invariants=(inv1, inv2), primary=inv1)
        >>> inv_set.primary.value
        'فاعل'
        >>> inv_set.strongest.value
        'فاعل'
    """

    invariants: Tuple[Invariant, ...]
    primary: Invariant | None = None
    rank: Rank = Rank.CANDIDATE

    def __post_init__(self) -> None:
        if not self.invariants:
            raise ValueError("InvariantSet.invariants must be non-empty")

    @property
    def strongest(self) -> Invariant:
        """Get the strongest invariant (highest strength)."""
        return max(self.invariants, key=lambda inv: inv.strength)

    @property
    def all_stable(self) -> bool:
        """Check if all invariants are stable."""
        return all(inv.is_stable for inv in self.invariants)

    @property
    def has_conflicts(self) -> bool:
        """Check if there are multiple strong invariants."""
        strong = [inv for inv in self.invariants if inv.strength >= 0.7]
        return len(strong) > 1


# ===========================================================================
# Invariant Detection
# ===========================================================================


def detect_invariants(
    origins: Tuple[Any, ...],  # Should be Tuple[Origin, ...] but avoiding circular import
    kinds: FrozenSet[InvariantKind] | None = None,
) -> InvariantSet:
    """Detect invariant features across a set of origins.

    This function:
    1. Analyzes all origins for common features
    2. Extracts invariants of specified kinds
    3. Computes coverage and confidence for each
    4. Ranks invariants by strength
    5. Returns an InvariantSet

    Args:
        origins: Collection of Origin instances.
        kinds: Set of invariant kinds to detect (default: all kinds).

    Returns:
        InvariantSet with detected invariants.

    Raises:
        ValueError: If origins is empty.

    Example:
        >>> from fvafk.algebra.general_learning import Origin, Rank, Evidence
        >>> origin1 = Origin(surface="كاتب", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> origin2 = Origin(surface="زارع", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> origin3 = Origin(surface="عامل", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> inv_set = detect_invariants(origins=(origin1, origin2, origin3))
        >>> len(inv_set.invariants)
        2
        >>> inv_set.strongest.kind
        <InvariantKind.PATTERN: 1>
    """
    if not origins:
        raise ValueError("origins must be non-empty")

    # Default: detect all kinds
    if kinds is None:
        kinds = frozenset(InvariantKind)

    invariants: list[Invariant] = []

    # Detect pattern invariant
    if InvariantKind.PATTERN in kinds:
        pattern_inv = _detect_pattern_invariant(origins)
        if pattern_inv:
            invariants.append(pattern_inv)

    # Detect interpretation type invariant
    if InvariantKind.INTERPRETATION_TYPE in kinds:
        interp_inv = _detect_interpretation_invariant(origins)
        if interp_inv:
            invariants.append(interp_inv)

    # Detect root structure invariant
    if InvariantKind.ROOT_STRUCTURE in kinds:
        root_inv = _detect_root_structure_invariant(origins)
        if root_inv:
            invariants.append(root_inv)

    if not invariants:
        # No invariants detected; create a fallback
        invariants.append(
            Invariant(
                kind=InvariantKind.PATTERN,
                value="unknown",
                description="No clear invariant pattern detected",
                coverage=0.0,
                confidence=0.0,
                residuals=(Residual(kind="invariant.unclear", description="Pattern unclear"),),
            )
        )

    # Determine primary invariant (strongest one)
    primary = max(invariants, key=lambda inv: inv.strength)

    # Determine rank based on stability
    if all(inv.is_stable for inv in invariants):
        rank = Rank.LICENSED
    elif any(inv.is_stable for inv in invariants):
        rank = Rank.CANDIDATE
    else:
        rank = Rank.UNRESOLVED

    return InvariantSet(
        invariants=tuple(invariants),
        primary=primary,
        rank=rank,
    )


# ===========================================================================
# Invariant Detection Helpers
# ===========================================================================


def _detect_pattern_invariant(origins: Tuple[Any, ...]) -> Invariant | None:
    """Detect morphological pattern invariant."""
    patterns = [o.pattern for o in origins if hasattr(o, "pattern") and o.pattern]
    if not patterns:
        return None

    # Count pattern frequencies
    pattern_counts: dict[str, int] = {}
    for p in patterns:
        pattern_counts[p] = pattern_counts.get(p, 0) + 1

    # Find most common pattern
    most_common = max(pattern_counts.items(), key=lambda x: x[1])
    pattern_value, count = most_common

    coverage = count / len(origins)
    confidence = min(coverage * 1.1, 1.0)  # Slight boost if coverage is high

    evidence_list = [
        Evidence(
            kind="pattern.match",
            source=f"{count}/{len(origins)}_origins",
            detail=f"Pattern '{pattern_value}' found in {count} of {len(origins)} origins",
            weight=coverage,
        )
    ]

    return Invariant(
        kind=InvariantKind.PATTERN,
        value=pattern_value,
        description=f"Morphological pattern {pattern_value}",
        coverage=coverage,
        confidence=confidence,
        evidence=tuple(evidence_list),
    )


def _detect_interpretation_invariant(origins: Tuple[Any, ...]) -> Invariant | None:
    """Detect semantic interpretation invariant."""
    interpretations = [
        o.interpretation
        for o in origins
        if hasattr(o, "interpretation") and o.interpretation
    ]
    if not interpretations:
        return None

    # Count interpretation frequencies
    interp_counts: dict[str, int] = {}
    for i in interpretations:
        interp_counts[i] = interp_counts.get(i, 0) + 1

    # Find most common interpretation
    most_common = max(interp_counts.items(), key=lambda x: x[1])
    interp_value, count = most_common

    coverage = count / len(origins)
    confidence = coverage * 0.9  # Semantic features are less certain than morphological

    evidence_list = [
        Evidence(
            kind="interpretation.match",
            source=f"{count}/{len(origins)}_origins",
            detail=f"Interpretation '{interp_value}' found in {count} of {len(origins)} origins",
            weight=coverage,
        )
    ]

    return Invariant(
        kind=InvariantKind.INTERPRETATION_TYPE,
        value=interp_value,
        description=f"Semantic interpretation: {interp_value}",
        coverage=coverage,
        confidence=confidence,
        evidence=tuple(evidence_list),
    )


def _detect_root_structure_invariant(origins: Tuple[Any, ...]) -> Invariant | None:
    """Detect root structure invariant (e.g., trilateral, quadrilateral)."""
    root_lengths = []
    for o in origins:
        if hasattr(o, "root") and o.root:
            root_lengths.append(len(o.root))

    if not root_lengths:
        return None

    # Find most common root length
    length_counts: dict[int, int] = {}
    for length in root_lengths:
        length_counts[length] = length_counts.get(length, 0) + 1

    most_common_length, count = max(length_counts.items(), key=lambda x: x[1])

    coverage = count / len(origins)
    confidence = min(coverage * 1.05, 1.0)

    # Map length to description
    length_names = {
        2: "bilateral",
        3: "trilateral",
        4: "quadrilateral",
        5: "quinqueliteral",
    }
    length_name = length_names.get(most_common_length, f"{most_common_length}-radical")

    evidence_list = [
        Evidence(
            kind="root_structure.match",
            source=f"{count}/{len(origins)}_origins",
            detail=f"Root length {most_common_length} found in {count} of {len(origins)} origins",
            weight=coverage,
        )
    ]

    return Invariant(
        kind=InvariantKind.ROOT_STRUCTURE,
        value=length_name,
        description=f"Root structure: {length_name}",
        coverage=coverage,
        confidence=confidence,
        evidence=tuple(evidence_list),
    )


__all__ = [
    "InvariantKind",
    "Invariant",
    "InvariantSet",
    "detect_invariants",
]
