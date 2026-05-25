"""
U₄ Morpheme/Affix/ClosedClass Carrier (طبقة الوحدات الصرفية)

Domain: U₄ = MorphemeCarrier
Transition: Functional Role (U₃) → Morpheme Classification (U₄)
Purpose: Classify functional roles into morpheme types without premature word commitment

Key Principle:
    Morpheme ≠ Word
    Morpheme ≠ Root
    Morpheme ≠ Final Meaning

Critical Laws:
    1. Closed-class items require lexicon attestation
    2. Affixes require host attachment evidence
    3. Root candidates require pattern confirmation (→ U₅)
    4. No word-level syntax or semantics at U₄
    5. Preserve competing morpheme interpretations

Architecture:
    U₃ (FunctionalRole) → U₄ (Morpheme) → U₅ (StemRoot)

PR: U4-LAYER
Created: 2026-05-25
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Set, FrozenSet, Dict, Any
from uuid import uuid4

from dal_core.u3_functional_roles import RoleSpan
from dal_core.residuals import Residual


# ============================================================================
# Morpheme Type Taxonomy
# ============================================================================

class MorphemeSort(Enum):
    """
    Morpheme sort categories for multi-sorted algebra.

    Each morpheme belongs to exactly one sort.
    """
    CLOSED_CLASS = "closed_class"      # Particles, pronouns (مِنْ، إِنَّ، هُوَ)
    AFFIX = "affix"                    # Prefixes, infixes, suffixes
    ROOT_CANDIDATE = "root_candidate"  # Potential root material
    STEM = "stem"                      # Stem structure (→ U₅ for full analysis)
    INFLECTIONAL = "inflectional"      # Gender, number, case markers
    DERIVATIONAL = "derivational"      # Pattern augments
    RESIDUAL = "residual"              # Unresolved morphemes


class ClosedClassType(Enum):
    """
    Closed-class morpheme types (وحدات مغلقة).

    Requires lexicon match for certification.
    """
    HARF_JARR = "حرف جر"               # بِ، لِ، مِنْ، إِلَى، عَنْ
    HARF_ATF = "حرف عطف"               # وَ، فَ، ثُمَّ، أَوْ
    HARF_NASB = "حرف نصب"              # إِنَّ، أَنَّ، لَكِنَّ، لَيْتَ
    HARF_JAZM = "حرف جزم"              # لَمْ، لَمَّا، لِـ (أمر)
    HARF_NAFY = "حرف نفي"              # لَا، مَا، لَمْ، لَنْ
    HARF_ISTIFHAM = "حرف استفهام"     # هَلْ، أَ، الهمزة
    HARF_SHART = "حرف شرط"             # إِنْ، لَوْ، لَوْلَا
    HARF_TAWKID = "حرف توكيد"          # قَدْ، لَقَدْ، نُونُ التوكيد
    HARF_NIDA = "حرف نداء"             # يَا، أَيَا، هَيَا
    HARF_TASHBIH = "حرف تشبيه"         # كَ، كَأَنَّ
    HARF_TANBIH = "حرف تنبيه"          # أَلَا، أَمَا
    PRONOUN = "ضمير"                   # هُوَ، هِيَ، ـهُ، ـكَ
    DEMONSTRATIVE = "اسم إشارة"        # هَذَا، هَذِهِ، ذَلِكَ
    RELATIVE = "اسم موصول"             # الَّذِي، الَّتِي، مَنْ، مَا
    INTERROGATIVE = "اسم استفهام"      # مَنْ، مَا، أَيْنَ، كَيْفَ، مَتَى


class AffixType(Enum):
    """
    Affix morpheme types (سوابق ولواحق وزوائد).

    Requires host attachment evidence.
    """
    # Prefixes (سوابق)
    DEFINITE_ARTICLE = "ال التعريف"    # الـ
    FUTURE_PREFIX = "سين المستقبل"     # سَـ، سَوْفَ
    QUESTION_PREFIX = "همزة الاستفهام" # أَـ
    CONJUNCTION_PREFIX = "واو/فاء العطف" # وَ، فَ
    PREPOSITION_PREFIX = "حرف جر سابق" # بِـ، لِـ، كَـ

    # Suffixes (لواحق)
    TA_MARBUTA = "تاء مربوطة"          # ـة
    TANWIN = "تنوين"                   # ـٌ، ـً، ـٍ
    CASE_ENDING = "علامة إعراب"        # ـُ، ـَ، ـِ، ـْ
    PRONOUN_SUFFIX = "ضمير متصل لاحق"  # ـهُ، ـكَ، ـنَا
    DUAL_SUFFIX = "علامة تثنية"        # ـانِ، ـيْنِ
    PLURAL_SUFFIX = "علامة جمع"        # ـونَ، ـينَ، ـاتٌ
    NISBAH_SUFFIX = "ياء النسبة"       # ـِيّ

    # Infixes (وسائط)
    ALIF_MUFAALA = "ألف المفاعلة"      # فَاعَلَ
    DOUBLING_SHADDA = "تضعيف"          # فَعَّلَ

    # Derivational augments (زوائد اشتقاقية)
    HAMZA_IFAL = "همزة الإفعال"        # أَفْعَلَ
    SIN_TA_ISTIFAL = "سين وتاء الاستفعال" # اسْتَفْعَلَ
    TA_TAFAUL = "تاء التفاعل"          # تَفَاعَلَ
    MIM_MASDAR = "ميم المصدر/الاسم"    # مَفْعُول، مُفَاعِل


class RootCandidateType(Enum):
    """
    Root candidate types (مرشحات الجذر).

    Not certified as root until U₅ pattern matching.
    """
    FA_CANDIDATE = "مرشح فاء"
    AYN_CANDIDATE = "مرشح عين"
    LAM_CANDIDATE = "مرشح لام"
    FOURTH_CANDIDATE = "مرشح رابع"
    WEAK_LETTER = "حرف علة محتمل"
    HAMZATED = "مهموز محتمل"
    DOUBLED = "مضعف محتمل"
    UNKNOWN_POSITION = "موضع غير محدد"


# ============================================================================
# Morpheme Rank System
# ============================================================================

class MorphemeRank(Enum):
    """
    Epistemic rank for morpheme classification.

    Progression: ZERO → CANDIDATE → HYPOTHESIS → STRONG_HYPOTHESIS → CERTIFICATE
    """
    ZERO = 0                    # No morpheme classification
    CANDIDATE = 1               # Possible morpheme (from U₃ role)
    HYPOTHESIS = 2              # Supported by evidence
    STRONG_HYPOTHESIS = 3       # Multiple evidence sources
    CERTIFICATE = 4             # Lexicon-attested or pattern-confirmed


# ============================================================================
# Morpheme Residual Codes
# ============================================================================

class MorphemeResidualCode(Enum):
    """Residual codes for morpheme layer."""
    # Warnings
    AMBIGUOUS_MORPHEME = "ambiguous_morpheme"
    MISSING_HOST = "missing_host"
    WEAK_EVIDENCE = "weak_evidence"
    COMPETING_INTERPRETATIONS = "competing_interpretations"

    # Blockers
    NO_LEXICON_MATCH = "no_lexicon_match"
    INVALID_AFFIX_POSITION = "invalid_affix_position"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    BLOCKED_BY_U3 = "blocked_by_u3"


# ============================================================================
# Core Morpheme Structures
# ============================================================================

@dataclass(frozen=True)
class MorphemeIdentity:
    """
    Identity of a morpheme.

    Attributes:
        morpheme_id: Unique identifier
        sort: Morpheme sort category
        morpheme_type: Specific type within sort
        surface_form: Surface representation
        trace_to_u3: Trace to U₃ role span
    """
    morpheme_id: str
    sort: MorphemeSort
    morpheme_type: Any  # Union of ClosedClassType, AffixType, RootCandidateType
    surface_form: str
    trace_to_u3: str  # RoleSpan.span_id

    def __post_init__(self):
        # Validate type matches sort
        type_map = {
            MorphemeSort.CLOSED_CLASS: ClosedClassType,
            MorphemeSort.AFFIX: AffixType,
            MorphemeSort.ROOT_CANDIDATE: RootCandidateType,
        }
        if self.sort in type_map:
            expected_enum = type_map[self.sort]
            if not isinstance(self.morpheme_type, expected_enum):
                raise ValueError(
                    f"Morpheme type {self.morpheme_type} does not match sort {self.sort}"
                )


@dataclass
class MorphemeCandidate:
    """
    Single morpheme candidate.

    Attributes:
        identity: Morpheme identity
        rank: Epistemic rank
        evidence: Supporting evidence
        competitors: Other interpretations
        residuals: Warnings/blockers
    """
    identity: MorphemeIdentity
    rank: MorphemeRank
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    competitors: FrozenSet[str] = field(default_factory=frozenset)  # morpheme_ids
    residuals: List[Residual] = field(default_factory=list)

    def has_blocker(self) -> bool:
        """Check if morpheme has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    def is_certified(self) -> bool:
        """Check if morpheme is certified."""
        return self.rank == MorphemeRank.CERTIFICATE and not self.has_blocker()


@dataclass
class AttachmentMode:
    """
    Attachment mode for affixes.

    Attributes:
        requires_host: Must attach to host
        host_position: Required position (prefix/suffix/infix)
        host_category: Required host category (verb/noun/particle)
    """
    requires_host: bool = False
    host_position: Optional[str] = None  # "prefix" | "suffix" | "infix"
    host_category: Optional[str] = None  # "verb" | "noun" | "particle"


@dataclass
class FeaturePotential:
    """
    Feature potential for morpheme.

    What features this morpheme might contribute (→ U₉).
    """
    gender: Optional[str] = None        # "masculine" | "feminine"
    number: Optional[str] = None        # "singular" | "dual" | "plural"
    definiteness: Optional[str] = None  # "definite" | "indefinite"
    case_marker: Optional[str] = None   # "nominative" | "accusative" | "genitive"
    person: Optional[str] = None        # "first" | "second" | "third"


@dataclass
class MorphemeSpan:
    """
    Morpheme span over functional roles.

    This is the U₄ carrier element.

    Attributes:
        span_id: Unique identifier
        role_span_ids: Source U₃ role spans
        candidates: Competing morpheme candidates
        attachment: Attachment requirements
        features: Feature potential
        trace_to_u3: Preserved trace
        residuals: Span-level residuals
        rank: Overall span rank
    """
    span_id: str
    role_span_ids: List[str]
    candidates: List[MorphemeCandidate]
    attachment: AttachmentMode
    features: FeaturePotential
    trace_to_u3: List[str]  # Preserved traces
    residuals: List[Residual]
    rank: int  # Minimum of candidate ranks

    def __post_init__(self):
        if not self.span_id:
            object.__setattr__(self, 'span_id', f"morpheme_{uuid4().hex[:8]}")
        if not self.trace_to_u3:
            object.__setattr__(self, 'trace_to_u3', self.role_span_ids.copy())

    def has_blocker(self) -> bool:
        """Check if span has blocking residuals."""
        return any(r.is_blocker for r in self.residuals) or \
               any(c.has_blocker() for c in self.candidates)

    def primary_candidate(self) -> Optional[MorphemeCandidate]:
        """Get highest-ranked candidate."""
        if not self.candidates:
            return None
        return max(self.candidates, key=lambda c: c.rank.value)


# ============================================================================
# Morpheme Set (Competing Interpretations)
# ============================================================================

@dataclass
class MorphemeSet:
    """
    Set of competing morpheme candidates.

    Attributes:
        morphemes: Set of morpheme candidates
        evidence: Shared evidence
    """
    morphemes: List[MorphemeCandidate] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)

    def __len__(self) -> int:
        return len(self.morphemes)

    def add_morpheme(self, morpheme: MorphemeCandidate):
        """Add morpheme to set."""
        self.morphemes.append(morpheme)

    def filter_by_sort(self, sort: MorphemeSort) -> List[MorphemeCandidate]:
        """Filter morphemes by sort."""
        return [m for m in self.morphemes if m.identity.sort == sort]

    def highest_ranked(self) -> Optional[MorphemeCandidate]:
        """Get highest-ranked morpheme."""
        if not self.morphemes:
            return None
        return max(self.morphemes, key=lambda m: m.rank.value)


# ============================================================================
# U₄ Completeness Predicate
# ============================================================================

def CompleteOne₄(morpheme_span: MorphemeSpan) -> bool:
    """
    Minimal completeness for U₄ morpheme span.

    A morpheme span is minimally complete if:
    1. Has at least one candidate
    2. No blocking residuals
    3. Trace to U₃ preserved
    4. If affix, has attachment mode

    Args:
        morpheme_span: Morpheme span to check

    Returns:
        True if minimally complete
    """
    # Check basic structure
    if not morpheme_span.candidates:
        return False

    # Check for blockers
    if morpheme_span.has_blocker():
        return False

    # Check trace preservation
    if not morpheme_span.trace_to_u3:
        return False

    # Check affix attachment mode
    primary = morpheme_span.primary_candidate()
    if primary and primary.identity.sort == MorphemeSort.AFFIX:
        if not morpheme_span.attachment.requires_host:
            return False

    return True


# ============================================================================
# Transition Gate U₃ → U₄
# ============================================================================

@dataclass
class U3_U4_TransitionEvidence:
    """
    Evidence for U₃ → U₄ transition.

    Attributes:
        role_span: Source U₃ role span
        lexicon_match: Closed-class lexicon match
        pattern_hint: Pattern-based hint
        context: Contextual evidence
    """
    role_span: RoleSpan
    lexicon_match: Optional[Dict[str, Any]] = None
    pattern_hint: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Critical Laws (Enforcement Functions)
# ============================================================================

def enforce_morpheme_neq_word(morpheme: MorphemeCandidate) -> bool:
    """
    Law: Morpheme ≠ Word

    Morphemes are subword units. No POS or syntactic role at U₄.
    """
    # Check that morpheme does not claim to be a complete word
    # This will be enforced in operations
    return True


def enforce_morpheme_neq_root(morpheme: MorphemeCandidate) -> bool:
    """
    Law: Morpheme ≠ Root

    Root candidates are not certified until U₅ pattern matching.
    """
    if morpheme.identity.sort == MorphemeSort.ROOT_CANDIDATE:
        return morpheme.rank != MorphemeRank.CERTIFICATE
    return True


def enforce_no_semantics(morpheme: MorphemeCandidate) -> bool:
    """
    Law: No semantics at U₄

    Morphemes do not carry final meaning. Meaning is at U₁₂ (Dalālah).
    """
    # Verify no 'meaning' field exists in evidence
    for ev in morpheme.evidence:
        if 'meaning' in ev or 'murad' in ev or 'dalālah' in ev:
            return False
    return True
