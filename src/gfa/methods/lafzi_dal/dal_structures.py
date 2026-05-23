"""
Pure Dāl Geometry Structures - هندسة الدال وحده

Core data structures for PR-L3 implementation.

Critical Law:
    الدال المرخّص له هندسة كاملة قبل السؤال عن معناه
    A licensed signifier has complete geometry before asking about meaning.

What This Module Provides:
    - PhonicCarrier: Sound/grapheme carriers from C1
    - HarakaOperation: Haraka transformations from C2a gates
    - SyllableLicense: CV/CVC/CVV patterns
    - WordBoundaryInfo: Word boundary detection
    - CliticAnalysis: Clitic separation
    - FormulaCandidate: Pattern candidates (فَعَل, فاعِل...)
    - PathType: Morphological path classification
    - PatternStatus: Pattern recognition status
    - TerminalState: I'rab/Bina status
    - SyntacticReadiness: Ready for syntax
    - SentenceShape: Sentence type classification
    - RoleProjection: Syntactic role candidates

What This Module Does NOT Provide:
    - NO meaning fields
    - NO dalalah fields
    - NO wadh fields
    - NO hukm fields
    - NO mutabaqah fields
    - NO tadammun fields
    - NO iltizam fields
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Optional, FrozenSet


# ============================================================================
# Phase 1: Phonic Carriers (C1)
# ============================================================================

@dataclass(frozen=True)
class PhonicCarrier:
    """
    حامل صوتي - Phonic Carrier

    Represents a sound or grapheme unit from C1 encoding.
    """

    form: str  # The surface form (grapheme)
    phoneme: Optional[str]  # Phonemic representation
    position: int  # Position in sequence
    features: FrozenSet[str]  # Phonetic features

    def __post_init__(self):
        if not self.form:
            raise ValueError("PhonicCarrier form cannot be empty")
        if self.position < 0:
            raise ValueError("PhonicCarrier position must be >= 0")


# ============================================================================
# Phase 2: Haraka Operations (C2a)
# ============================================================================

class HarakaOperationType(Enum):
    """Types of haraka operations from C2a gates."""
    SUKUN = "sukun"
    SHADDA = "shadda"
    TANWIN = "tanwin"
    HAMZA = "hamza"
    WAQF = "waqf"
    IDGHAM = "idgham"
    MADD = "madd"
    DELETION = "deletion"
    EPENTHESIS = "epenthesis"
    ASSIMILATION = "assimilation"


@dataclass(frozen=True)
class HarakaOperation:
    """
    عملية حركة - Haraka Operation

    Records a transformation applied by C2a phonology gates.
    """

    operation_type: HarakaOperationType
    position: int  # Where in sequence
    input_form: str  # Before transformation
    output_form: str  # After transformation
    gate_name: str  # Which gate applied it

    def __post_init__(self):
        if self.position < 0:
            raise ValueError("HarakaOperation position must be >= 0")
        if not self.gate_name:
            raise ValueError("HarakaOperation must specify gate_name")


# ============================================================================
# Phase 3: Syllable Licenses (C2a)
# ============================================================================

class SyllableType(Enum):
    """Syllable structure types."""
    CV = "CV"      # Open light
    CVV = "CVV"    # Open heavy
    CVC = "CVC"    # Closed
    CVVC = "CVVC"  # Super-heavy
    CVCC = "CVCC"  # Super-heavy closed


@dataclass(frozen=True)
class SyllableLicense:
    """
    ترخيص مقطعي - Syllable License

    Proof that a syllable structure is valid.
    """

    syllable_type: SyllableType
    onset: str  # Consonant(s) at start
    nucleus: str  # Vowel core
    coda: Optional[str]  # Consonant(s) at end
    position: int  # Syllable position in word
    is_valid: bool  # Whether licensed

    def __post_init__(self):
        if not self.nucleus:
            raise ValueError("SyllableLicense must have nucleus")
        if self.position < 0:
            raise ValueError("SyllableLicense position must be >= 0")


# ============================================================================
# Phase 4: Word Boundaries (C2b)
# ============================================================================

@dataclass(frozen=True)
class WordBoundaryInfo:
    """
    معلومات حدود الكلمة - Word Boundary Information

    Detection of word start and end.
    """

    start_position: int
    end_position: int
    boundary_markers: FrozenSet[str]  # Signals used (space, hamza, etc.)
    confidence: float  # [0, 1] confidence in boundary

    def __post_init__(self):
        if self.start_position < 0:
            raise ValueError("start_position must be >= 0")
        if self.end_position < self.start_position:
            raise ValueError("end_position must be >= start_position")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be in [0, 1]")

    @property
    def length(self) -> int:
        """Word length in positions."""
        return self.end_position - self.start_position


# ============================================================================
# Phase 5: Clitic Analysis (C2b)
# ============================================================================

@dataclass(frozen=True)
class Clitic:
    """
    لاصقة - Clitic

    A prefix or suffix attached to the stem.
    """

    form: str
    position: int
    is_prefix: bool  # True=prefix, False=suffix
    clitic_type: str  # "article", "conjunction", "pronoun", etc.


@dataclass(frozen=True)
class CliticAnalysis:
    """
    تحليل اللواصق - Clitic Analysis

    Separation of prefixes and suffixes from stem.
    """

    stem: str
    prefixes: Tuple[Clitic, ...]
    suffixes: Tuple[Clitic, ...]
    has_clitics: bool

    def __post_init__(self):
        if not self.stem:
            raise ValueError("CliticAnalysis must have stem")

    @property
    def total_clitics(self) -> int:
        """Total number of clitics."""
        return len(self.prefixes) + len(self.suffixes)


# ============================================================================
# Phase 6: Formula Candidates (C2b)
# ============================================================================

class FormulaClass(Enum):
    """Classes of morphological patterns."""
    VERB_PAST = "verb_past"
    VERB_PRESENT = "verb_present"
    VERB_COMMAND = "verb_command"
    ACTIVE_PARTICIPLE = "active_participle"
    PASSIVE_PARTICIPLE = "passive_participle"
    NOUN_INSTRUMENT = "noun_instrument"
    NOUN_PLACE = "noun_place"
    NOUN_TIME = "noun_time"
    MASDAR = "masdar"
    MUBALLAGHA = "muballagha"
    ADJECTIVE = "adjective"
    BROKEN_PLURAL = "broken_plural"
    DIMINUTIVE = "diminutive"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class FormulaCandidate:
    """
    مرشح صيغة - Formula Candidate

    A potential morphological pattern match.
    """

    pattern: str  # e.g., "فَعَلَ", "فاعِل"
    root: Optional[str]  # Trilateral/quadrilateral root
    formula_class: FormulaClass
    confidence: float  # [0, 1]
    residuals: FrozenSet[str]  # Issues with match

    def __post_init__(self):
        if not self.pattern:
            raise ValueError("FormulaCandidate must have pattern")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be in [0, 1]")


# ============================================================================
# Phase 7: Path Type (C2b)
# ============================================================================

class PathType(Enum):
    """
    نوع المسار - Path Type

    Morphological path classification.
    """
    JAMID = "jamid"  # جامد - Frozen noun
    MUSHTAQQ = "mushtaqq"  # مشتق - Derived
    KHAS = "khas"  # خاص - Proper noun
    VERB = "verb"  # فعل
    PARTICLE = "particle"  # حرف
    UNKNOWN = "unknown"

    @property
    def is_known(self) -> bool:
        """Check if path type is known."""
        return self != PathType.UNKNOWN


# ============================================================================
# Phase 8: Pattern Status (C2b)
# ============================================================================

class PatternStatus(Enum):
    """
    حالة الوزن - Pattern Status

    Pattern recognition status.
    """
    KNOWN = "known"  # معروف - Well-known pattern
    CANDIDATE = "candidate"  # مرشح - Possible pattern
    UNKNOWN = "unknown"  # مجهول - Unrecognized
    MULTIPLE = "multiple"  # متعدد - Multiple candidates

    @property
    def is_known(self) -> bool:
        """Check if pattern is definitively known."""
        return self == PatternStatus.KNOWN


# ============================================================================
# Phase 9: Terminal State (C2b)
# ============================================================================

class TerminalState(Enum):
    """
    الحالة النهائية - Terminal State

    I'rab or Bina status.
    """
    MURAB = "murab"  # معرب - Declinable
    MABNI = "mabni"  # مبني - Indeclinable
    MAMNU_MIN_SARF = "mamnu_min_sarf"  # ممنوع من الصرف - Diptote
    UNKNOWN = "unknown"

    @property
    def is_declinable(self) -> bool:
        """Check if word is declinable."""
        return self == TerminalState.MURAB


# ============================================================================
# Phase 10: Syntactic Readiness (C2b)
# ============================================================================

class SyntacticReadiness(Enum):
    """
    الجاهزية النحوية - Syntactic Readiness

    Ready to enter syntactic structures.
    """
    READY = "ready"  # مؤهل
    NEEDS_CONTEXT = "needs_context"  # يحتاج سياق
    BLOCKED = "blocked"  # محجوب
    UNKNOWN = "unknown"

    @property
    def is_ready(self) -> bool:
        """Check if ready for syntax."""
        return self == SyntacticReadiness.READY


# ============================================================================
# Phase 11: Sentence Shape (C2b)
# ============================================================================

class SentenceShape(Enum):
    """
    شكل الجملة - Sentence Shape

    Sentence type classification.
    """
    NOMINAL = "nominal"  # اسمية - Nominal sentence
    VERBAL = "verbal"  # فعلية - Verbal sentence
    SHIBH_JUMLAH = "shibh_jumlah"  # شبه الجملة - Quasi-sentence
    FRAGMENT = "fragment"  # جزء
    UNKNOWN = "unknown"

    @property
    def is_complete(self) -> bool:
        """Check if complete sentence."""
        return self in (SentenceShape.NOMINAL, SentenceShape.VERBAL)


# ============================================================================
# Phase 12: Role Projection (C2b)
# ============================================================================

class RoleType(Enum):
    """Syntactic role types."""
    FAIL = "fail"  # فاعل
    MAFOOL = "mafool"  # مفعول
    MUBTADA = "mubtada"  # مبتدأ
    KHABAR = "khabar"  # خبر
    MUDAF = "mudaf"  # مضاف
    MUDAF_ILAYH = "mudaf_ilayh"  # مضاف إليه
    NAIB_FAIL = "naib_fail"  # نائب فاعل
    TAMYIZ = "tamyiz"  # تمييز
    HAL = "hal"  # حال
    SIFAH = "sifah"  # صفة
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class RoleProjection:
    """
    إسقاط الدور - Role Projection

    Potential syntactic role.
    """

    role_type: RoleType
    confidence: float  # [0, 1]
    requirements: FrozenSet[str]  # What's needed for this role

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("confidence must be in [0, 1]")


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Phonic
    "PhonicCarrier",
    # Haraka
    "HarakaOperationType",
    "HarakaOperation",
    # Syllable
    "SyllableType",
    "SyllableLicense",
    # Boundaries
    "WordBoundaryInfo",
    # Clitics
    "Clitic",
    "CliticAnalysis",
    # Formulas
    "FormulaClass",
    "FormulaCandidate",
    # Classification
    "PathType",
    "PatternStatus",
    "TerminalState",
    "SyntacticReadiness",
    "SentenceShape",
    # Roles
    "RoleType",
    "RoleProjection",
]
