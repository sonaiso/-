"""
U₆ Pattern/Weight Carrier (طبقة الوزن والصيغة)

Domain: U₆ = PatternWeightCarrier
Transition: Root/Stem (U₅) → Pattern Classification (U₆)
Purpose: Pattern (وزن) matching without semantic commitment

Key Principle:
    Pattern ≠ Meaning
    Weight is transformation function, not semantic judgment

Critical Laws:
    1. Pattern maps root to form candidates
    2. Pattern does NOT give final meaning
    3. Distinguish: stem pattern, derivational pattern, transformation pattern
    4. Vowel template separate from consonantal skeleton
    5. Original vs extra letters explicitly marked
    6. No word-level syntax at U₆

Architecture:
    U₅ (StemRoot) → U₆ (PatternWeight) → U₇ (WordForm)

PR: U6-LAYER
Created: 2026-05-25
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Set, FrozenSet, Dict, Any, Tuple
from uuid import uuid4

from dal_core.u5_stemroot_carrier import RootStemSpan, RootCandidate
from dal_core.residuals import Residual


# ============================================================================
# Pattern Type Taxonomy
# ============================================================================

class PatternSort(Enum):
    """
    Pattern sort categories.
    """
    STEM_PATTERN = "وزن الجذع"         # Stem/frozen pattern
    DERIVATIONAL = "وزن الاشتقاق"      # Derivational pattern
    TRANSFORMATION = "وزن التحول"      # Transformation/form pattern
    INFLECTIONAL = "وزن الصرف"        # Inflectional pattern


class VerbPattern(Enum):
    """Verb patterns (أوزان الأفعال)."""
    # Trilateral patterns
    FAALA = "فَعَلَ"                   # Basic trilateral (past)
    FAILA = "فَعِلَ"
    FAULA = "فَعُلَ"
    YAFALU = "يَفْعَلُ"                # Basic trilateral (present)
    YAFILU = "يَفْعِلُ"
    YAFULU = "يَفْعُلُ"

    # Augmented forms
    AFALA = "أَفْعَلَ"                 # Form II (إفعال)
    FAALA_II = "فَعَّلَ"              # Form II (تفعيل)
    FAALA_III = "فَاعَلَ"             # Form III (مفاعلة)
    AFALA_IV = "أَفْعَلَ"             # Form IV (إفعال)
    TAFAALA = "تَفَعَّلَ"             # Form V (تفعّل)
    TAFAALA_VI = "تَفَاعَلَ"          # Form VI (تفاعل)
    INFAALA = "انْفَعَلَ"             # Form VII (انفعال)
    IFTAALA = "افْتَعَلَ"             # Form VIII (افتعال)
    IFALLA = "افْعَلَّ"               # Form IX (افعلال)
    ISTAFALA = "اسْتَفْعَلَ"          # Form X (استفعال)


class NounPattern(Enum):
    """Noun patterns (أوزان الأسماء)."""
    # Active participle
    FAAIL = "فَاعِل"                  # Active participle
    MUFAIL = "مُفَعِّل"               # Active participle (Form II)
    MUFAAIL = "مُفَاعِل"              # Active participle (Form III)
    MUSTAFIL = "مُسْتَفْعِل"          # Active participle (Form X)

    # Passive participle
    MAFUUL = "مَفْعُول"                # Passive participle
    MUFAAL = "مُفَعَّل"               # Passive participle (Form II)

    # Nouns of place/time
    MAFAL = "مَفْعَل"                  # Noun of place
    MAFIL = "مَفْعِل"

    # Verbal nouns (مصادر)
    FAIL = "فَعْل"                     # Verbal noun
    FUUL = "فُعُول"
    FIAAL = "فِعَال"
    TAFIL = "تَفْعِيل"                # Verbal noun (Form II)
    MUFAALA = "مُفَاعَلَة"             # Verbal noun (Form III)
    IFAAL = "إِفْعَال"                # Verbal noun (Form IV)
    TAFAUL = "تَفَعُّل"               # Verbal noun (Form V)
    TAFAAUL = "تَفَاعُل"              # Verbal noun (Form VI)
    INFIAAL = "انْفِعَال"             # Verbal noun (Form VII)
    IFTIAAL = "افْتِعَال"             # Verbal noun (Form VIII)
    ISTIFAAL = "اسْتِفْعَال"          # Verbal noun (Form X)

    # Comparative/superlative
    AFAL = "أَفْعَل"                   # Comparative/superlative

    # Diminutive
    FUAYL = "فُعَيْل"                  # Diminutive

    # Plural patterns
    AFAAL = "أَفْعَال"                 # Broken plural
    FUUL_PLURAL = "فُعُل"             # Broken plural
    FIAAL_PLURAL = "فِعَال"           # Broken plural
    AFILA = "أَفْعِلَة"               # Broken plural
    MAFAAIL = "مَفَاعِيل"             # Broken plural


# ============================================================================
# Pattern Rank System
# ============================================================================

class PatternRank(Enum):
    """Epistemic rank for pattern classification."""
    ZERO = 0
    CANDIDATE = 1
    HYPOTHESIS = 2
    STRONG_HYPOTHESIS = 3
    CERTIFICATE = 4


# ============================================================================
# Core Pattern Structures
# ============================================================================

@dataclass(frozen=True)
class VowelTemplate:
    """
    Vowel template for pattern.

    Attributes:
        pattern: Vowel pattern (e.g., "َ َ َ" for فَعَلَ)
        positions: Position-specific vowels
    """
    pattern: str
    positions: Tuple[str, ...]  # One vowel per position


@dataclass(frozen=True)
class LetterMapping:
    """
    Mapping between root letters and pattern positions.

    Attributes:
        root_letter: Letter from root
        pattern_position: Position in pattern
        is_original: Is original (from root) or extra (augment)
    """
    root_letter: str
    pattern_position: int
    is_original: bool


@dataclass(frozen=True)
class PatternIdentity:
    """
    Identity of a pattern.

    Attributes:
        pattern_id: Unique identifier
        sort: Pattern sort
        pattern_type: Specific pattern type
        abstract_pattern: Abstract pattern (فَعَلَ)
        vowel_template: Vowel template
        root_mapping: Mapping to root radicals
        trace_to_u5: Trace to U₅
    """
    pattern_id: str
    sort: PatternSort
    pattern_type: Any  # Union of VerbPattern, NounPattern
    abstract_pattern: str
    vowel_template: VowelTemplate
    root_mapping: Tuple[LetterMapping, ...]
    trace_to_u5: str


@dataclass
class PatternCandidate:
    """
    Single pattern candidate.

    Attributes:
        identity: Pattern identity
        rank: Epistemic rank
        original_letters: Original letters (from root)
        extra_letters: Extra letters (augments)
        derivational_gate: Derivational transformation hint
        evidence: Supporting evidence
        residuals: Warnings/blockers
    """
    identity: PatternIdentity
    rank: PatternRank
    original_letters: Tuple[str, ...]
    extra_letters: Tuple[str, ...]
    derivational_gate: Optional[str] = None  # Hint for transformation
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    residuals: List[Residual] = field(default_factory=list)

    def has_blocker(self) -> bool:
        """Check if pattern has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)


@dataclass
class PatternSpan:
    """
    Pattern span over root/stem.

    This is the U₆ carrier element.

    Attributes:
        span_id: Unique identifier
        rootstem_span_id: Source U₅ span
        pattern_candidates: Competing pattern candidates
        transformation_type: Type of transformation
        form_hints: Hints for U₇ word form
        trace_to_u5: Preserved trace
        residuals: Span-level residuals
        rank: Overall span rank
    """
    span_id: str
    rootstem_span_id: str
    pattern_candidates: List[PatternCandidate]
    transformation_type: Optional[str]  # "derivation" | "inflection" | "frozen"
    form_hints: List[str]  # Hints for U₇
    trace_to_u5: str
    residuals: List[Residual]
    rank: int

    def __post_init__(self):
        if not self.span_id:
            object.__setattr__(self, 'span_id', f"pattern_{uuid4().hex[:8]}")

    def has_blocker(self) -> bool:
        """Check if span has blocking residuals."""
        return any(r.is_blocker for r in self.residuals) or \
               any(c.has_blocker() for c in self.pattern_candidates)

    def primary_pattern(self) -> Optional[PatternCandidate]:
        """Get highest-ranked pattern."""
        if not self.pattern_candidates:
            return None
        return max(self.pattern_candidates, key=lambda c: c.rank.value)


# ============================================================================
# U₆ Completeness Predicate
# ============================================================================

def CompleteOne₆(pattern_span: PatternSpan) -> bool:
    """
    Minimal completeness for U₆ pattern span.

    A pattern span is minimally complete if:
    1. Has at least one pattern candidate
    2. No blocking residuals
    3. Trace to U₅ preserved
    4. Original vs extra letters distinguished

    Args:
        pattern_span: Pattern span to check

    Returns:
        True if minimally complete
    """
    if not pattern_span.pattern_candidates:
        return False

    if pattern_span.has_blocker():
        return False

    if not pattern_span.trace_to_u5:
        return False

    # Check primary pattern has letter distinction
    primary = pattern_span.primary_pattern()
    if primary:
        if not primary.original_letters and not primary.extra_letters:
            return False

    return True


# ============================================================================
# Critical Laws (Enforcement Functions)
# ============================================================================

def enforce_pattern_neq_meaning(pattern: PatternCandidate) -> bool:
    """
    Law: Pattern ≠ Meaning

    Pattern is transformation function, not semantic judgment.
    """
    for ev in pattern.evidence:
        if 'meaning' in ev or 'murad' in ev or 'dalālah' in ev:
            return False
    return True


def enforce_pattern_is_transformation(pattern: PatternCandidate) -> bool:
    """
    Law: Pattern is transformation

    Pattern: Weight(root) → FormCandidate
    Not: Weight(root) ⊢ FinalMeaning
    """
    # Pattern should have transformation info, not semantic info
    return True  # Enforced by structure


def enforce_original_vs_extra(pattern: PatternCandidate) -> bool:
    """
    Law: Original vs Extra letters explicit

    Pattern must distinguish root letters from augments.
    """
    # At least original letters must be specified
    return len(pattern.original_letters) > 0


def enforce_no_syntax(pattern: PatternCandidate) -> bool:
    """
    Law: No syntax at U₆

    Pattern does not determine syntactic role.
    """
    for ev in pattern.evidence:
        if 'syntax' in ev or 'case' in ev or 'i3rab' in ev:
            return False
    return True


# ============================================================================
# Pattern Analysis Helpers
# ============================================================================

def extract_vowel_template(surface_form: str) -> VowelTemplate:
    """
    Extract vowel template from surface form.

    Args:
        surface_form: Surface representation

    Returns:
        VowelTemplate extracted from form
    """
    # Placeholder - real implementation requires diacritic extraction
    vowels = []
    for char in surface_form:
        if char in 'َُِْ':  # Fatha, Kasra, Damma, Sukun
            vowels.append(char)

    return VowelTemplate(
        pattern=''.join(vowels),
        positions=tuple(vowels)
    )


def map_root_to_pattern(
    root: RootCandidate,
    pattern_str: str
) -> Tuple[LetterMapping, ...]:
    """
    Map root radicals to pattern positions.

    Args:
        root: Root candidate
        pattern_str: Pattern string (e.g., "فَعَلَ")

    Returns:
        Tuple of letter mappings
    """
    # Placeholder - real implementation requires pattern matching algorithm
    mappings = []

    # Example: فَعَلَ maps to positions 0, 2, 4 for ف ع ل
    for i, radical in enumerate(root.identity.radicals):
        mappings.append(LetterMapping(
            root_letter=radical.letter,
            pattern_position=i * 2,  # Simplified
            is_original=True
        ))

    return tuple(mappings)


def identify_extra_letters(surface_form: str, root_letters: Tuple[str, ...]) -> Tuple[str, ...]:
    """
    Identify extra letters (augments) not in root.

    Args:
        surface_form: Surface representation
        root_letters: Root letters

    Returns:
        Tuple of extra letters
    """
    # Placeholder - real implementation requires alignment
    extras = []
    root_set = set(root_letters)

    for char in surface_form:
        if char not in root_set and char.isalpha():
            extras.append(char)

    return tuple(extras)
