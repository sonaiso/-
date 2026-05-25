"""
U₅ Stem/Root Carrier (طبقة الجذر والجذع)

Domain: U₅ = StemRootCarrier
Transition: Morpheme (U₄) → Root/Stem Classification (U₅)
Purpose: Distinguish between root (جذر) and stem (جذع) without pattern commitment

Key Principle:
    Root ≠ Stem ≠ Pattern ≠ Word
    Frozen (جامد) ≠ Derived (مشتق)

Critical Laws:
    1. Root extraction requires radical identification from U₄
    2. Weak/Hamzated/Doubled classification at root level
    3. Primitive stem vs Derived stem distinction
    4. Frozen (جامد) items have no derivational history
    5. No pattern (وزن) commitment until U₆
    6. No word-level syntax at U₅

Architecture:
    U₄ (Morpheme) → U₅ (StemRoot) → U₆ (PatternWeight)

PR: U5-LAYER
Created: 2026-05-25
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Set, FrozenSet, Dict, Any, Tuple
from uuid import uuid4

from dal_core.u4_morpheme_carrier import MorphemeSpan
from dal_core.residuals import Residual


# ============================================================================
# Root Type Taxonomy
# ============================================================================

class RootType(Enum):
    """
    Root type classification.
    """
    TRILATERAL = "ثلاثي"               # Three radicals (ك ت ب)
    QUADRILATERAL = "رباعي"            # Four radicals (ز ل ز ل)
    QUINQUELITERAL = "خماسي"           # Five radicals (rare)
    WEAK = "معتل"                      # Contains weak letter (و، ي، ا)
    HAMZATED = "مهموز"                 # Contains hamza
    DOUBLED = "مضعف"                   # Contains doubled radical (shadda)
    DEFECTIVE_ASSIMILATED = "مثال"     # First radical is weak
    DEFECTIVE_HOLLOW = "أجوف"          # Middle radical is weak
    DEFECTIVE_DEFECTIVE = "ناقص"       # Last radical is weak
    DOUBLY_WEAK = "لفيف"               # Multiple weak radicals
    FROZEN = "جامد"                    # No derivational structure
    UNKNOWN = "غير محدد"               # Not yet determined


class RootStatus(Enum):
    """
    Root extraction status.
    """
    CANDIDATE = "مرشح"                 # Candidate root
    HYPOTHESIS = "فرضية"               # Hypothetical root with evidence
    CONFIRMED = "مؤكد"                 # Confirmed by pattern
    ATTESTED = "مشهود"                 # Attested in lexicon
    FROZEN = "جامد"                    # Frozen form (no root)
    UNKNOWN = "غير معروف"              # Unknown


# ============================================================================
# Stem Type Taxonomy
# ============================================================================

class StemType(Enum):
    """
    Stem classification.
    """
    PRIMITIVE = "جذع بدائي"            # Primitive stem (minimal)
    DERIVED = "جذع مشتق"               # Derived stem (with augments)
    FROZEN = "جامد"                    # Frozen (no derivation)
    COMPOUND = "مركب"                  # Compound stem
    BORROWED = "دخيل"                  # Borrowed/foreign
    PROPER_NAME = "علم"                # Proper name
    UNKNOWN = "غير محدد"


class StemStatus(Enum):
    """
    Stem analysis status.
    """
    CANDIDATE = "مرشح"
    HYPOTHESIS = "فرضية"
    CONFIRMED = "مؤكد"
    FROZEN = "جامد"


# ============================================================================
# Radical Position
# ============================================================================

class RadicalPosition(Enum):
    """Position of radical in root."""
    FA = "فاء"          # First
    AYN = "عين"         # Second
    LAM = "لام"         # Third
    FOURTH = "رابع"     # Fourth (quadrilateral)
    FIFTH = "خامس"      # Fifth (quinqueliteral)


@dataclass(frozen=True)
class Radical:
    """
    Single radical of a root.

    Attributes:
        letter: The radical letter
        position: Position in root
        is_weak: Is weak letter (و، ي، ا)
        is_hamzated: Contains hamza
        is_doubled: Is doubled (shadda)
        morpheme_id: Trace to U₄ morpheme
    """
    letter: str
    position: RadicalPosition
    is_weak: bool = False
    is_hamzated: bool = False
    is_doubled: bool = False
    morpheme_id: Optional[str] = None


# ============================================================================
# Root Rank System
# ============================================================================

class RootRank(Enum):
    """
    Epistemic rank for root classification.
    """
    ZERO = 0                    # No root identified
    CANDIDATE = 1               # Possible root
    HYPOTHESIS = 2              # Supported by evidence
    STRONG_HYPOTHESIS = 3       # Pattern-supported
    CERTIFICATE = 4             # Lexicon-attested


# ============================================================================
# Root Residual Codes
# ============================================================================

class RootResidualCode(Enum):
    """Residual codes for root/stem layer."""
    # Warnings
    WEAK_ROOT_AMBIGUITY = "weak_root_ambiguity"
    HAMZA_POSITION_UNCERTAIN = "hamza_position_uncertain"
    MISSING_RADICAL = "missing_radical"
    EXTRA_LETTERS = "extra_letters"
    FROZEN_UNCERTAIN = "frozen_uncertain"

    # Blockers
    INVALID_RADICAL_SEQUENCE = "invalid_radical_sequence"
    NO_ROOT_FOUND = "no_root_found"
    CONFLICTING_PATTERNS = "conflicting_patterns"
    BLOCKED_BY_U4 = "blocked_by_u4"


# ============================================================================
# Core Root Structures
# ============================================================================

@dataclass(frozen=True)
class RootIdentity:
    """
    Identity of a root.

    Attributes:
        root_id: Unique identifier
        radicals: Tuple of radicals
        root_type: Type of root
        surface_form: Surface representation
        trace_to_u4: Trace to U₄ morpheme spans
    """
    root_id: str
    radicals: Tuple[Radical, ...]
    root_type: RootType
    surface_form: str
    trace_to_u4: Tuple[str, ...]  # morpheme_span_ids

    def __post_init__(self):
        # Validate radical count matches type
        count = len(self.radicals)
        if self.root_type == RootType.TRILATERAL and count != 3:
            raise ValueError(f"Trilateral root must have 3 radicals, got {count}")
        elif self.root_type == RootType.QUADRILATERAL and count != 4:
            raise ValueError(f"Quadrilateral root must have 4 radicals, got {count}")

    def get_radical_string(self) -> str:
        """Get root as string (e.g., 'ك ت ب')."""
        return ' '.join(r.letter for r in self.radicals)


@dataclass
class RootCandidate:
    """
    Single root candidate.

    Attributes:
        identity: Root identity
        status: Root status
        rank: Epistemic rank
        evidence: Supporting evidence
        competitors: Other root interpretations
        residuals: Warnings/blockers
    """
    identity: RootIdentity
    status: RootStatus
    rank: RootRank
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    competitors: FrozenSet[str] = field(default_factory=frozenset)  # root_ids
    residuals: List[Residual] = field(default_factory=list)

    def has_blocker(self) -> bool:
        """Check if root has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    def is_confirmed(self) -> bool:
        """Check if root is confirmed."""
        return self.status in {RootStatus.CONFIRMED, RootStatus.ATTESTED} and \
               not self.has_blocker()


# ============================================================================
# Stem Structures
# ============================================================================

@dataclass(frozen=True)
class StemIdentity:
    """
    Identity of a stem.

    Attributes:
        stem_id: Unique identifier
        stem_type: Type of stem
        surface_form: Surface representation
        root_id: Associated root (if derived)
        original_letters: Original letters
        extra_letters: Extra letters (augments)
        trace_to_u4: Trace to U₄
    """
    stem_id: str
    stem_type: StemType
    surface_form: str
    root_id: Optional[str] = None
    original_letters: Tuple[str, ...] = field(default_factory=tuple)
    extra_letters: Tuple[str, ...] = field(default_factory=tuple)
    trace_to_u4: Tuple[str, ...] = field(default_factory=tuple)


@dataclass
class StemCandidate:
    """
    Single stem candidate.

    Attributes:
        identity: Stem identity
        status: Stem status
        rank: Epistemic rank
        is_frozen: Is frozen (جامد) form
        is_derived: Is derived (مشتق) form
        evidence: Supporting evidence
        residuals: Warnings/blockers
    """
    identity: StemIdentity
    status: StemStatus
    rank: RootRank  # Reuse RootRank
    is_frozen: bool = False
    is_derived: bool = False
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    residuals: List[Residual] = field(default_factory=list)

    def __post_init__(self):
        # Enforce law: frozen ≠ derived
        if self.is_frozen and self.is_derived:
            raise ValueError("Stem cannot be both frozen and derived")


# ============================================================================
# Root/Stem Span
# ============================================================================

@dataclass
class RootStemSpan:
    """
    Root/Stem span over morphemes.

    This is the U₅ carrier element.

    Attributes:
        span_id: Unique identifier
        morpheme_span_ids: Source U₄ morpheme spans
        root_candidates: Competing root candidates
        stem_candidates: Competing stem candidates
        frozen_hypothesis: Is this a frozen form?
        pattern_hints: Hints for U₆ pattern matching
        trace_to_u4: Preserved trace
        residuals: Span-level residuals
        rank: Overall span rank
    """
    span_id: str
    morpheme_span_ids: List[str]
    root_candidates: List[RootCandidate]
    stem_candidates: List[StemCandidate]
    frozen_hypothesis: bool
    pattern_hints: List[str]  # Hints for U₆ (e.g., "فعل", "فاعل")
    trace_to_u4: List[str]
    residuals: List[Residual]
    rank: int

    def __post_init__(self):
        if not self.span_id:
            object.__setattr__(self, 'span_id', f"rootstem_{uuid4().hex[:8]}")
        if not self.trace_to_u4:
            object.__setattr__(self, 'trace_to_u4', self.morpheme_span_ids.copy())

    def has_blocker(self) -> bool:
        """Check if span has blocking residuals."""
        return any(r.is_blocker for r in self.residuals) or \
               any(c.has_blocker() for c in self.root_candidates)

    def primary_root(self) -> Optional[RootCandidate]:
        """Get highest-ranked root candidate."""
        if not self.root_candidates:
            return None
        return max(self.root_candidates, key=lambda c: c.rank.value)

    def primary_stem(self) -> Optional[StemCandidate]:
        """Get highest-ranked stem candidate."""
        if not self.stem_candidates:
            return None
        return max(self.stem_candidates, key=lambda c: c.rank.value)


# ============================================================================
# U₅ Completeness Predicate
# ============================================================================

def CompleteOne₅(rootstem_span: RootStemSpan) -> bool:
    """
    Minimal completeness for U₅ root/stem span.

    A root/stem span is minimally complete if:
    1. Has at least one root OR stem candidate
    2. If frozen, has stem candidate (no root)
    3. If derived, has root candidate
    4. No blocking residuals
    5. Trace to U₄ preserved

    Args:
        rootstem_span: Root/stem span to check

    Returns:
        True if minimally complete
    """
    # Check basic structure
    has_root = len(rootstem_span.root_candidates) > 0
    has_stem = len(rootstem_span.stem_candidates) > 0

    if not has_root and not has_stem:
        return False

    # Check frozen constraint
    if rootstem_span.frozen_hypothesis:
        if not has_stem:
            return False
        # Frozen items should not have root
        if has_root:
            return False

    # Check for blockers
    if rootstem_span.has_blocker():
        return False

    # Check trace preservation
    if not rootstem_span.trace_to_u4:
        return False

    return True


# ============================================================================
# Critical Laws (Enforcement Functions)
# ============================================================================

def enforce_root_neq_stem(root: RootCandidate, stem: StemCandidate) -> bool:
    """
    Law: Root ≠ Stem

    Root is abstract radical sequence.
    Stem is surface realization (may include augments).
    """
    return root.identity.root_id != stem.identity.stem_id


def enforce_frozen_no_root(stem: StemCandidate) -> bool:
    """
    Law: Frozen items have no root

    If stem is frozen (جامد), it has no derivational root.
    """
    if stem.is_frozen:
        return stem.identity.root_id is None
    return True


def enforce_derived_has_root(stem: StemCandidate) -> bool:
    """
    Law: Derived stems have roots

    If stem is derived (مشتق), it must reference a root.
    """
    if stem.is_derived:
        return stem.identity.root_id is not None
    return True


def enforce_root_neq_pattern(root: RootCandidate) -> bool:
    """
    Law: Root ≠ Pattern

    Root extraction does not commit to pattern (وزن).
    Pattern matching is at U₆.
    """
    # Verify no 'pattern' or 'wazn' field in evidence
    for ev in root.evidence:
        if 'pattern' in ev or 'wazn' in ev or 'وزن' in ev:
            return False
    return True


def enforce_no_word_level(root: RootCandidate, stem: StemCandidate) -> bool:
    """
    Law: No word-level syntax at U₅

    Root/stem analysis does not involve POS, case, or syntax.
    """
    # Check root
    for ev in root.evidence:
        if 'pos' in ev or 'case' in ev or 'syntax' in ev:
            return False

    # Check stem
    for ev in stem.evidence:
        if 'pos' in ev or 'case' in ev or 'syntax' in ev:
            return False

    return True


# ============================================================================
# Helper Functions
# ============================================================================

def identify_weak_root(radicals: Tuple[Radical, ...]) -> bool:
    """Check if root is weak (contains و، ي، ا)."""
    return any(r.is_weak for r in radicals)


def identify_hamzated_root(radicals: Tuple[Radical, ...]) -> bool:
    """Check if root is hamzated."""
    return any(r.is_hamzated for r in radicals)


def classify_weak_type(radicals: Tuple[Radical, ...]) -> RootType:
    """
    Classify specific weak root type.

    - DEFECTIVE_ASSIMILATED (مثال): First radical weak
    - DEFECTIVE_HOLLOW (أجوف): Middle radical weak
    - DEFECTIVE_DEFECTIVE (ناقص): Last radical weak
    - DOUBLY_WEAK (لفيف): Multiple weak radicals
    """
    weak_positions = [i for i, r in enumerate(radicals) if r.is_weak]

    if len(weak_positions) == 0:
        return RootType.TRILATERAL

    if len(weak_positions) > 1:
        return RootType.DOUBLY_WEAK

    pos = weak_positions[0]
    if pos == 0:
        return RootType.DEFECTIVE_ASSIMILATED
    elif pos == 1 and len(radicals) == 3:
        return RootType.DEFECTIVE_HOLLOW
    elif pos == len(radicals) - 1:
        return RootType.DEFECTIVE_DEFECTIVE

    return RootType.WEAK


def extract_root_from_morphemes(morpheme_spans: List[MorphemeSpan]) -> Tuple[Radical, ...]:
    """
    Extract root radicals from morpheme spans.

    This is a placeholder - actual implementation requires
    pattern matching from U₆.
    """
    # Placeholder: will be implemented with proper pattern matching
    return tuple()
