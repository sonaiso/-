"""
Grapheme Phonetic Projection (U₁ Layer)

This module implements initial phonetic classification for grapheme clusters
WITHOUT producing phonological certificates or syllable structures.

Key Principle: U₁ produces phonetic CANDIDATES (hypotheses), not CERTIFICATES (proven structures).

Theorem: Grapheme Phonetic Projection Theorem
For every licensed grapheme G ∈ U₁, the system produces one or more initial
phonetic projections or classified residuals, without claiming syllable/root/pattern/meaning.

Mathematical formulation:
∀G ∈ U₁, phon_project₁(G) ∈ PhoneticCandidate₁⁺ ∪ Residual₁ ∪ Fail₁

Critical Laws:
1. NO syllable formation (belongs in U₂)
2. NO root extraction (belongs in morphology)
3. NO pattern matching (belongs in morphology)
4. Trace preservation mandatory
5. Residuals accumulate, never erased
6. Maximum rank: grapheme_phonetic_hypothesis
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Tuple, Set

from dal_core.atoms import ArabicAtom, AtomKind
from dal_core.carriers import Carrier
from dal_core.residuals import Residual, make_blocker, make_warning, ResidualType
from dal_core.evidence import Evidence, make_evidence


# ============================================================================
# Phonetic Classification Categories (10 types)
# ============================================================================

class PhoneticClass₁(Enum):
    """
    التصنيف الصوتي الأولي (Initial Phonetic Classification)

    These are CANDIDATES, not final phonological categories.
    """
    CLEAR_CONSONANT_C = "صامت_واضح"           # Clear consonant (ب، ت، ج...)
    CLEAR_SHORT_VOWEL_V = "صائت_قصير_واضح"   # Clear short vowel (َ ُ ِ)
    CLEAR_LONG_VOWEL_VV = "صائت_طويل_واضح"   # Long vowel candidate (ا، و، ي after compatible vowel)
    SUKUN_OR_CLOSURE = "سكون_أو_إغلاق"        # Sukun mark (potential coda)
    SHADDA_POLICY = "سياسة_شدة"               # Shadda with gemination policy
    TANWEEN_POLICY = "سياسة_تنوين"            # Tanween with waqf/wasl policy
    MADD_POLICY = "سياسة_مد"                  # Madd with expansion policy
    WAQF_WASL_POLICY = "سياسة_وقف_وصل"       # Boundary policy
    DEFERRED = "مؤجل"                         # Ambiguous, needs context
    RESIDUAL = "بقايا"                        # Unclassifiable


# ============================================================================
# Policy Types
# ============================================================================

class ShaddahPolicy(Enum):
    """سياسة الشدة (Shadda Policy)"""
    PRESERVE_AS_MARK = "حفظ_كعلامة"                    # Keep as written mark
    EXPAND_TO_GEMINATE_CANDIDATE = "توسيع_لمرشح_تضعيف" # Expand to geminate candidate
    EXPAND_ONLY_IN_PHONOLOGY = "توسيع_في_الصوتيات"     # Defer to U₂
    RESIDUALIZE_IF_AMBIGUOUS = "بقايا_إن_ملتبس"        # Mark as residual


class TanweenPolicy(Enum):
    """سياسة التنوين (Tanween Policy)"""
    PRESERVE_AS_MARK = "حفظ_كعلامة"                    # Keep as written mark
    PROJECT_AS_VOWEL_PLUS_N = "إسقاط_كحركة_ونون"      # Project as vowel+n candidate
    DEFER_TO_MORPH_SYNTAX = "تأجيل_للصرف_النحو"       # Needs morphosyntax
    WAQF_SENSITIVE = "حساس_للوقف"                     # Waqf changes realization


class MaddPolicy(Enum):
    """سياسة المد (Madd Policy)"""
    PRESERVE_WRITTEN_MADD = "حفظ_المد_المكتوب"        # Keep written madd
    SPLIT_HAMZA_ALIF_CANDIDATE = "فصل_همزة_ألف"       # Split آ candidate
    PROJECT_LONG_VOWEL_CANDIDATE = "إسقاط_مد_طويل"    # Long vowel candidate
    QURANIC_MADD_DEFERRED = "مد_قرآني_مؤجل"           # Tajweed madd deferred
    RESIDUALIZE_AMBIGUOUS_MADD = "بقايا_مد_ملتبس"     # Ambiguous madd


class BoundaryPolicy(Enum):
    """سياسة الوقف والوصل (Boundary Policy)"""
    WASL_MODE = "وصل"                                  # Connected speech
    WAQF_MODE = "وقف"                                  # Pausal form
    UNKNOWN_BOUNDARY = "حد_مجهول"                      # Unknown boundary
    PRESERVE_BOTH_CANDIDATES = "حفظ_المرشحين"         # Keep both options


# ============================================================================
# Phonetic Candidates
# ============================================================================

@dataclass
class MakhrajCandidate:
    """مرشح مخرج (Articulation Point Candidate)"""
    region: str = ""           # منطقة: throat, tongue, lips...
    subregion: str = ""        # منطقة فرعية: specific point
    confidence: float = 0.0    # NOT a certificate, just confidence
    evidence: List[Evidence] = field(default_factory=list)


@dataclass
class VowelCandidate:
    """مرشح حركة (Vowel Candidate)"""
    quality: str = ""          # a, u, i (or Arabic names)
    length: str = ""           # short, long
    confidence: float = 0.0
    evidence: List[Evidence] = field(default_factory=list)


@dataclass
class ClosureCandidate:
    """مرشح إغلاق (Closure Candidate)"""
    is_coda: bool = False      # Potential syllable coda
    is_sukun: bool = False     # Written sukun
    is_assimilated: bool = False  # May undergo assimilation
    confidence: float = 0.0
    evidence: List[Evidence] = field(default_factory=list)


@dataclass
class PhoneticCandidate:
    """
    مرشح صوتي (Phonetic Candidate)

    NOT a phonological certificate, just an initial hypothesis.
    """
    makhraj_candidate: Optional[MakhrajCandidate] = None
    vowel_candidate: Optional[VowelCandidate] = None
    closure_candidate: Optional[ClosureCandidate] = None
    length_candidate: str = ""  # short, long, unknown
    alternative_candidates: List[PhoneticCandidate] = field(default_factory=list)
    confidence: float = 0.0
    rank: float = 0.0  # Maximum: grapheme_phonetic_hypothesis


# ============================================================================
# Policy Declarations
# ============================================================================

@dataclass
class PolicyDeclaration:
    """
    إعلان سياسة (Policy Declaration)

    Declares how ambiguous graphemes should be handled.
    Does NOT resolve them at this layer.
    """
    policy_type: str           # shadda, tanween, madd, boundary
    policy_choice: Enum        # Specific policy enum value
    candidates: List[PhoneticCandidate] = field(default_factory=list)
    constraints: Dict[str, any] = field(default_factory=dict)
    residuals: List[Residual] = field(default_factory=list)


# ============================================================================
# Grapheme Carrier U₁ (Enhanced Structure)
# ============================================================================

@dataclass
class GraphemeCarrierU1:
    """
    حامل العنقود الكتابي U₁ (Grapheme Carrier U₁)

    Enhanced grapheme cluster with initial phonetic projection.

    Structure:
    G = (base, marks, position, trace₀, grapheme_class,
         phonetic_projection₁, policies, residuals)
    """
    # Core grapheme data
    base: str                              # Base character
    marks: List[str] = field(default_factory=list)  # Diacritics
    position: int = 0                      # Position in sequence

    # Trace from lower layer
    trace₀: Optional[Carrier] = None       # Trace to U₀ Carrier
    source_atom: Optional[ArabicAtom] = None  # Source atom if available

    # Classification
    grapheme_class: str = ""               # Graphemic classification

    # NEW: Phonetic projection
    phonetic_class: Optional[PhoneticClass₁] = None
    phonetic_projection₁: Optional[PhoneticCandidate] = None

    # NEW: Policy declarations
    policies: List[PolicyDeclaration] = field(default_factory=list)

    # Trace and residuals
    trace₁: Optional[GraphemeCarrierU1] = None  # Self-reference for expanded forms
    residuals: List[Residual] = field(default_factory=list)

    # Rank (maximum: grapheme_phonetic_hypothesis)
    rank: float = 0.0

    def get_full_grapheme(self) -> str:
        """Reconstruct full grapheme"""
        return self.base + "".join(self.marks)

    def has_policy(self, policy_type: str) -> bool:
        """Check if grapheme has specific policy"""
        return any(p.policy_type == policy_type for p in self.policies)


# ============================================================================
# Phonetic Projection Result
# ============================================================================

@dataclass
class PhoneticProjectionResult:
    """
    نتيجة الإسقاط الصوتي (Phonetic Projection Result)

    Result of phonetic projection for a grapheme.
    """
    grapheme: GraphemeCarrierU1
    success: bool = False
    phonetic_class: Optional[PhoneticClass₁] = None
    candidates: List[PhoneticCandidate] = field(default_factory=list)
    policies: List[PolicyDeclaration] = field(default_factory=list)
    residuals: List[Residual] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)
    rank: float = 0.0  # ≤ grapheme_phonetic_hypothesis


# ============================================================================
# Classification Constants
# ============================================================================

# Clear Arabic consonants (unambiguous)
CLEAR_CONSONANTS = {
    'ب', 'ت', 'ث', 'ج', 'ح', 'خ', 'د', 'ذ', 'ر', 'ز',
    'س', 'ش', 'ص', 'ض', 'ط', 'ظ', 'ع', 'غ', 'ف', 'ق',
    'ك', 'ل', 'م', 'ن', 'ه'
}

# Ambiguous letters (can be consonant OR long vowel)
AMBIGUOUS_LETTERS = {'ا', 'و', 'ي', 'ى'}

# Hamza variations (complex behavior)
HAMZA_CARRIERS = {'ء', 'أ', 'إ', 'ؤ', 'ئ', 'آ'}

# Short vowel marks
SHORT_VOWEL_MARKS = {
    '\u064E': 'fatha',   # َ
    '\u064F': 'damma',   # ُ
    '\u0650': 'kasra',   # ِ
}

# Long vowel compatibility
LONG_VOWEL_COMPAT = {
    'fatha': 'ا',  # َ + ا
    'damma': 'و',  # ُ + و
    'kasra': 'ي',  # ِ + ي
}

# Tanween marks
TANWEEN_MARKS = {
    '\u064B': ('fathatan', 'fatha', 'n'),  # ً
    '\u064C': ('dammatan', 'damma', 'n'),  # ٌ
    '\u064D': ('kasratan', 'kasra', 'n'),  # ٍ
}

# Special marks
SUKUN_MARK = '\u0652'  # ْ
SHADDA_MARK = '\u0651'  # ّ


# ============================================================================
# Rank Constants
# ============================================================================

# Maximum rank for this layer
GRAPHEME_PHONETIC_HYPOTHESIS_RANK = 0.5  # Not a certificate, just hypothesis

# Rank values
RANK_CLEAR_CLASSIFICATION = 0.45
RANK_POLICY_DEPENDENT = 0.35
RANK_AMBIGUOUS_CANDIDATE = 0.25
RANK_DEFERRED = 0.15
RANK_RESIDUAL = 0.0


# ============================================================================
# Helper Functions
# ============================================================================

def extract_marks_from_grapheme(grapheme: str) -> Tuple[str, List[str]]:
    """
    Extract base character and marks from a grapheme string.

    Returns: (base, marks_list)
    """
    if not grapheme:
        return "", []

    base = grapheme[0]
    marks = list(grapheme[1:]) if len(grapheme) > 1 else []
    return base, marks


def has_mark(marks: List[str], target_mark: str) -> bool:
    """Check if marks list contains a specific mark"""
    return target_mark in marks


def get_short_vowel(marks: List[str]) -> Optional[str]:
    """Extract short vowel from marks (fatha, damma, kasra)"""
    for mark in marks:
        if mark in SHORT_VOWEL_MARKS:
            return SHORT_VOWEL_MARKS[mark]
    return None


def has_shadda(marks: List[str]) -> bool:
    """Check if marks contain shadda"""
    return SHADDA_MARK in marks


def has_sukun(marks: List[str]) -> bool:
    """Check if marks contain sukun"""
    return SUKUN_MARK in marks


def get_tanween(marks: List[str]) -> Optional[Tuple[str, str, str]]:
    """Extract tanween info if present"""
    for mark in marks:
        if mark in TANWEEN_MARKS:
            return TANWEEN_MARKS[mark]
    return None
