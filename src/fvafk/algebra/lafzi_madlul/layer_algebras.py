"""Concrete Layer Algebras: 11 Lafẓī Madlūl Layers.

Each layer is a complete algebra implementing the fractal pattern::

    A_L = (U_L, T_L, B_L, I_L, O_L, G_L, CPB_L, ρ_L, R_L, F_L)

This module implements all 11 layers from Trace to WordCandidate.

## Design Principle

Every layer is **self-contained**. No layer generates semantic meaning.
Transitions between layers preserve trace, rank, and residuals.

"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple

from ..core import Rank, Trace
from .fractal_algebra import LayerType, validate_no_meaning_field


# ===========================================================================
# Type Systems for Each Layer
# ===========================================================================


class LetterType(Enum):
    """Types of letters (الحرف)."""
    CONSONANT = auto()      # صامت
    VOWEL = auto()          # علة
    HAMZA = auto()          # همزة
    UNRESOLVED = auto()


class LetterRole(Enum):
    """Roles of letters in morphology."""
    ROOT_CANDIDATE = auto()      # محتمل جذري
    AFFIX_CANDIDATE = auto()     # محتمل زيادة
    FUNCTIONAL = auto()          # حرف معنى
    UNRESOLVED = auto()


class HarakahType(Enum):
    """Types of diacritics (الحركة)."""
    FATHA = auto()          # َ
    DAMMA = auto()          # ُ
    KASRA = auto()          # ِ
    SUKUN = auto()          # ْ
    TANWIN_FATH = auto()    # ً
    TANWIN_DAMM = auto()    # ٌ
    TANWIN_KASR = auto()    # ٍ
    SHADDA = auto()         # ّ


class HarakahRole(Enum):
    """Roles of diacritics (not intrinsic, context-dependent)."""
    PHONETIC = auto()       # صوتي
    PATTERN = auto()        # وزني
    BINAA = auto()          # بناء
    IRAB = auto()           # إعراب
    WASL = auto()           # وصل
    WAQF = auto()           # وقف
    UNRESOLVED = auto()


class SyllableType(Enum):
    """Syllable structures (أنواع المقاطع)."""
    CV = auto()
    CVC = auto()
    CVV = auto()
    CVVC = auto()
    CVCC = auto()


class RootType(Enum):
    """Root types (أنواع الجذور)."""
    TRILATERAL = auto()         # ثلاثي
    QUADRILATERAL = auto()      # رباعي
    WEAK = auto()               # معتل
    HOLLOW = auto()             # أجوف
    DEFECTIVE = auto()          # ناقص


# ===========================================================================
# Layer 0: Trace Algebra (جبر الأثر)
# ===========================================================================


@dataclass(frozen=True)
class TraceAlgebra:
    """L0: Trace Algebra - raw phonetic/graphic trace.

    الأثر هو أول ظهور قبل التصنيف.

    This is the entry point: raw observations before any classification.
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.TRACE, init=False)
    unit_value: str = ""

    # T: النوع
    trace_type: str = "unknown"  # صوت / رسم / رمز

    # B: الحدود
    is_readable: bool = False
    is_disambiguated: bool = False

    # I: الربط الداخلي
    script_context: Optional[str] = None

    # ρ: الرتبة
    rank: Rank = Rank.UNRESOLVED
    evidence: List[str] = field(default_factory=list)

    # R: البقايا
    residuals: List[str] = field(default_factory=list)
    # trace.unclear, script.ambiguous, sound_or_script_unresolved

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("trace_init"))

    # CPB metadata
    boundaries: Dict[str, bool] = field(default_factory=dict, init=False)
    internal_bindings: Dict[str, str] = field(default_factory=dict, init=False)
    allowed_operations: List[str] = field(default_factory=lambda: ["classify"], init=False)
    licensing_status: str = field(default="candidate", init=False)
    cpb_metadata: Dict[str, str] = field(default_factory=dict, init=False)
    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)


# ===========================================================================
# Layer 1: Letter Algebra (جبر الحرف)
# ===========================================================================


@dataclass(frozen=True)
class LetterAlgebra:
    """L1: Letter Algebra - grapheme/phoneme unit.

    الحرف ليس معنى، لكنه حامل بناء.

    A letter is not meaning, but a structural carrier.
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.LETTER, init=False)
    unit_value: str = ""

    # T: النوع
    letter_type: LetterType = LetterType.UNRESOLVED
    role: LetterRole = LetterRole.UNRESOLVED

    # B: الحدود
    boundaries: Dict[str, bool] = field(default_factory=dict)
    # is_root_eligible, is_affix_eligible, is_functional

    # I: الربط الداخلي
    internal_bindings: Dict[str, str] = field(default_factory=dict)
    # graph, phoneme, makhraj, sifat

    # O: العمليات
    allowed_operations: List[str] = field(
        default_factory=lambda: ["classify", "test_root", "test_affix"]
    )

    # G: البوابات
    licensing_status: str = "candidate"

    # CPB
    cpb_metadata: Dict[str, str] = field(default_factory=dict)

    # ρ: الرتبة
    rank: Rank = Rank.CANDIDATE
    evidence: List[str] = field(default_factory=list)

    # R: البقايا
    residuals: List[str] = field(default_factory=list)
    # letter.role_unresolved, root_or_affix_ambiguous, weak_letter.possible

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("letter_init"))

    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)

    @classmethod
    def from_form(cls, letter_form: str) -> LetterAlgebra:
        """Construct LetterAlgebra from a letter form."""
        return cls(
            unit_value=letter_form,
            trace=Trace("letter_from_form", source_span=(0, len(letter_form))),
        )


# ===========================================================================
# Layer 2: Harakah Algebra (جبر الحركة)
# ===========================================================================


@dataclass(frozen=True)
class HarakahAlgebra:
    """L2: Harakah Algebra - diacritic constraint.

    الحركة ليست معنى، لكنها قيد تشغيل.

    A harakah is not meaning, but an operational constraint.
    **Critical**: HarakahForm ≠ HarakahRole (role is context-dependent).
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.HARAKAH, init=False)
    unit_value: str = ""

    # T: النوع
    harakah_type: HarakahType = HarakahType.FATHA
    role: HarakahRole = HarakahRole.UNRESOLVED  # context-dependent!

    # B: الحدود
    position: int = -1
    position_type: str = "unknown"  # بداية / وسط / نهاية

    # I: الربط الداخلي
    attached_to_letter: Optional[str] = None
    internal_bindings: Dict[str, str] = field(default_factory=dict)

    # O: العمليات
    allowed_operations: List[str] = field(
        default_factory=lambda: ["infer_role_from_context"]
    )

    # B & G: الحدود والبوابات
    boundaries: Dict[str, bool] = field(default_factory=dict)
    licensing_status: str = "candidate"

    # CPB
    cpb_metadata: Dict[str, str] = field(default_factory=dict)

    # ρ: الرتبة
    rank: Rank = Rank.CANDIDATE
    evidence: List[str] = field(default_factory=list)

    # R: البقايا
    residuals: List[str] = field(default_factory=list)
    # harakah.role_unresolved, irab_or_bina_ambiguous, weight_or_case_ambiguous

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("harakah_init"))

    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)

    @classmethod
    def from_form(cls, harakah_form: str) -> HarakahAlgebra:
        """Construct HarakahAlgebra from a diacritic form."""
        return cls(
            unit_value=harakah_form,
            trace=Trace("harakah_from_form"),
        )


# ===========================================================================
# Layer 3: Atom Algebra (جبر الذرة)
# ===========================================================================


@dataclass(frozen=True)
class AtomAlgebra:
    """L3: Atom Algebra - letter + harakah binding.

    الذرة = حرف + حركة (أول وحدة تشغيلية).

    First operational unit: CPB(letter, harakah) → Atom.
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.ATOM, init=False)
    letter: LetterAlgebra
    harakah: HarakahAlgebra

    # B: الحدود
    position: int = -1

    # I: الربط الداخلي
    internal_bindings: Dict[str, str] = field(default_factory=dict)

    # O: العمليات
    allowed_operations: List[str] = field(
        default_factory=lambda: ["is_syllable_start", "is_syllable_nucleus"]
    )

    # G & B
    boundaries: Dict[str, bool] = field(default_factory=dict)
    licensing_status: str = "licensed"  # atoms are generally auto-licensed

    # CPB
    cpb_metadata: Dict[str, str] = field(default_factory=dict)

    # ρ: الرتبة (capped by min of letter/harakah)
    rank: Rank = Rank.LICENSED
    evidence: List[str] = field(default_factory=list)

    # R: البقايا (accumulated from letter + harakah)
    residuals: List[str] = field(default_factory=list)

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("atom_init"))

    @property
    def unit_value(self) -> str:
        """Return the surface form of the atom."""
        return f"{self.letter.unit_value}{self.harakah.unit_value}"

    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)


# ===========================================================================
# Layer 4: Syllable Algebra (جبر المقطع)
# ===========================================================================


@dataclass(frozen=True)
class SyllableAlgebra:
    """L4: Syllable Algebra - phonotactic unit.

    المقطع ليس معنى، لكنه حد صوتي كافٍ.

    A syllable is not meaning, but a phonotactically valid unit.
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.SYLLABLE, init=False)
    atoms: Tuple[AtomAlgebra, ...] = ()

    # T: النوع
    syllable_type: SyllableType = SyllableType.CV

    # B: الحدود
    is_heavy: bool = False

    # I: الربط الداخلي
    internal_bindings: Dict[str, str] = field(default_factory=dict)

    # O: العمليات
    allowed_operations: List[str] = field(
        default_factory=lambda: ["test_phonotactic_validity"]
    )

    # G & B
    boundaries: Dict[str, bool] = field(default_factory=dict)
    licensing_status: str = "candidate"

    # CPB
    cpb_metadata: Dict[str, str] = field(default_factory=dict)

    # ρ: الرتبة
    rank: Rank = Rank.CANDIDATE
    evidence: List[str] = field(default_factory=list)

    # R: البقايا
    residuals: List[str] = field(default_factory=list)
    # syllable.invalid, phonotactic.heavy, weak_letter_effect

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("syllable_init"))

    @property
    def unit_value(self) -> str:
        """Return the surface form of the syllable."""
        return "".join(atom.unit_value for atom in self.atoms)

    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)


# ===========================================================================
# Layer 5: Sequence Algebra (جبر التتابع)
# ===========================================================================


@dataclass(frozen=True)
class SequenceAlgebra:
    """L5: Sequence Algebra - syllable chain + phonetic economy.

    التتابع المقطعي + الاقتصاد الصوتي.

    Phonetic economy constraints (idghām, i'lāl, ḥadhf) apply here.
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.SEQUENCE, init=False)
    syllables: Tuple[SyllableAlgebra, ...] = ()

    # T: النوع
    is_phonotactically_valid: bool = False

    # I: الربط الداخلي
    phonotactic_effects: List[str] = field(default_factory=list)
    # idgham, i'lal, hazf, qalb, iltiqaa_saakinayn
    internal_bindings: Dict[str, str] = field(default_factory=dict)

    # O: العمليات
    allowed_operations: List[str] = field(
        default_factory=lambda: ["apply_phonetic_economy"]
    )

    # G & B
    boundaries: Dict[str, bool] = field(default_factory=dict)
    licensing_status: str = "candidate"

    # CPB
    cpb_metadata: Dict[str, str] = field(default_factory=dict)

    # ρ: الرتبة
    rank: Rank = Rank.CANDIDATE
    evidence: List[str] = field(default_factory=list)

    # R: البقايا
    residuals: List[str] = field(default_factory=list)

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("sequence_init"))

    @property
    def unit_value(self) -> str:
        """Return the surface form of the sequence."""
        return "".join(syl.unit_value for syl in self.syllables)

    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)


# ===========================================================================
# Layer 6: Root Candidate Algebra (جبر الجذر المرشح)
# ===========================================================================


@dataclass(frozen=True)
class RootCandidateAlgebra:
    """L6: Root Candidate Algebra - consonantal skeleton.

    الجذر ليس معنى كاملاً، بل مادة لفظية مرشحة.

    **Critical**: Root is NOT meaning. Root is lexical material.
    No maṣdar, no fi'l, no meaning from root alone.
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.ROOT_CANDIDATE, init=False)
    consonants: Tuple[str, ...] = ()

    # T: النوع
    root_type: RootType = RootType.TRILATERAL

    # B: الحدود
    extracted_from: str = ""

    # I: الربط الداخلي
    internal_bindings: Dict[str, str] = field(default_factory=dict)

    # O: العمليات
    allowed_operations: List[str] = field(
        default_factory=lambda: ["test_lexicon_attestation"]
    )

    # G & B
    boundaries: Dict[str, bool] = field(default_factory=dict)
    licensing_status: str = "candidate"

    # CPB
    cpb_metadata: Dict[str, str] = field(default_factory=dict)

    # ρ: الرتبة
    rank: Rank = Rank.CANDIDATE
    evidence: List[str] = field(default_factory=list)

    # R: البقايا
    residuals: List[str] = field(default_factory=list)
    # root.unconfirmed, lexical_confirmation_missing, borrowed_word_possible

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("root_init"))

    @property
    def unit_value(self) -> str:
        """Return the root consonants."""
        return " ".join(self.consonants)

    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)


# ===========================================================================
# Layer 7: Affix Operator Algebra (جبر الزيادة)
# ===========================================================================


@dataclass(frozen=True)
class AffixOperatorAlgebra:
    """L7: Affix Operator Algebra - augmentation as operator.

    الزيادة ليست حرفاً عادياً، بل operator تحويل.

    Affixes are operators, not ordinary letters.
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.AFFIX_OPERATOR, init=False)
    affix_letter: str = ""

    # T: النوع
    affix_position: str = "unknown"  # prefix / infix / suffix

    # I: الربط الداخلي
    operation_type: str = "unknown"  # causative, reflexive, etc.
    internal_bindings: Dict[str, str] = field(default_factory=dict)

    # O: العمليات
    allowed_operations: List[str] = field(
        default_factory=lambda: ["apply_to_root"]
    )

    # G & B
    boundaries: Dict[str, bool] = field(default_factory=dict)
    licensing_status: str = "candidate"

    # CPB
    cpb_metadata: Dict[str, str] = field(default_factory=dict)

    # ρ: الرتبة
    rank: Rank = Rank.CANDIDATE
    evidence: List[str] = field(default_factory=list)

    # R: البقايا
    residuals: List[str] = field(default_factory=list)

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("affix_init"))

    @property
    def unit_value(self) -> str:
        """Return the affix letter."""
        return self.affix_letter

    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)


# ===========================================================================
# Layer 8: Pattern Template Algebra (جبر الوزن)
# ===========================================================================


@dataclass(frozen=True)
class PatternTemplateAlgebra:
    """L8: Pattern Template Algebra - morphological template.

    الوزن ليس معنى، بل هيئة لفظية.

    **Critical**: Pattern is NOT meaning. Pattern is formal template.
    فاعل does NOT mean "agent" directly; it's a template that opens
    semantic *potential*, not semantic *certainty*.
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.PATTERN_TEMPLATE, init=False)
    template: str = ""  # فَعَلَ, فَاعِل, مَفْعُول, etc.

    # T: النوع
    pattern_status: str = "unknown"  # qiyasi / samai

    # B: الحدود
    root_positions: Tuple[int, ...] = ()  # where root consonants go
    affix_positions: Tuple[int, ...] = ()  # where affixes go

    # I: الربط الداخلي
    harakah_pattern: str = ""
    internal_bindings: Dict[str, str] = field(default_factory=dict)

    # O: العمليات
    allowed_operations: List[str] = field(
        default_factory=lambda: ["apply_to_root"]
    )

    # G & B
    boundaries: Dict[str, bool] = field(default_factory=dict)
    licensing_status: str = "candidate"

    # CPB
    cpb_metadata: Dict[str, str] = field(default_factory=dict)

    # ρ: الرتبة
    rank: Rank = Rank.CANDIDATE
    evidence: List[str] = field(default_factory=list)

    # R: البقايا
    residuals: List[str] = field(default_factory=list)
    # pattern.collision, pattern.unlicensed, samai_required

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("pattern_init"))

    @property
    def unit_value(self) -> str:
        """Return the template."""
        return self.template

    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)


# ===========================================================================
# Layer 9: Built Form Algebra (جبر الصيغة)
# ===========================================================================


@dataclass(frozen=True)
class BuiltFormAlgebra:
    """L9: Built Form Algebra - root ⊗ pattern.

    الصيغة = جذر ⊗ وزن (لكن ليست معنى نهائي).

    **Critical**: Built form is NOT final meaning.
    Requires wadh'/usage evidence before meaning.
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.BUILT_FORM, init=False)
    root: RootCandidateAlgebra
    pattern: PatternTemplateAlgebra

    # T: النوع
    surface_form: str = ""

    # I: الربط الداخلي
    affixes: Tuple[AffixOperatorAlgebra, ...] = ()
    phonotactic_adjustments: List[str] = field(default_factory=list)
    internal_bindings: Dict[str, str] = field(default_factory=dict)

    # O: العمليات
    allowed_operations: List[str] = field(
        default_factory=lambda: ["check_lexicon"]
    )

    # G & B
    boundaries: Dict[str, bool] = field(default_factory=dict)
    licensing_status: str = "candidate"

    # CPB
    cpb_metadata: Dict[str, str] = field(default_factory=dict)

    # ρ: الرتبة
    rank: Rank = Rank.CANDIDATE
    evidence: List[str] = field(default_factory=list)

    # R: البقايا
    residuals: List[str] = field(default_factory=list)
    # form.lexical_attestation_missing, form.meaning_unlicensed

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("built_form_init"))

    @property
    def unit_value(self) -> str:
        """Return the surface form."""
        return self.surface_form

    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)


# ===========================================================================
# Layer 10: Word Candidate Algebra (جبر الكلمة المرشحة)
# ===========================================================================


@dataclass(frozen=True)
class WordCandidateAlgebra:
    """L10: Word Candidate Algebra - lexical candidate.

    الكلمة المرشحة (تصنف قبل معناها).

    **Critical**: Unknown words are NOT rejected directly.
    They are classified into possibility matrix:
    - attested / unused / borrowed / coined / transferred / etc.
    """

    # U: الوحدة
    unit_type: LayerType = field(default=LayerType.WORD_CANDIDATE, init=False)
    built_form: BuiltFormAlgebra

    # T: النوع
    word_status: str = "unknown"  # attested / unused / borrowed / etc.

    # I: الربط الداخلي
    usage_context: Optional[str] = None
    attestation_evidence: List[str] = field(default_factory=list)
    internal_bindings: Dict[str, str] = field(default_factory=dict)

    # O: العمليات
    allowed_operations: List[str] = field(
        default_factory=lambda: ["classify_usage"]
    )

    # G & B
    boundaries: Dict[str, bool] = field(default_factory=dict)
    licensing_status: str = "candidate"

    # CPB
    cpb_metadata: Dict[str, str] = field(default_factory=dict)

    # ρ: الرتبة
    rank: Rank = Rank.CANDIDATE
    evidence: List[str] = field(default_factory=list)

    # R: البقايا
    residuals: List[str] = field(default_factory=list)
    # usage.unattested, placement.absent, foreign_origin_possible

    # Trace
    trace: Trace = field(default_factory=lambda: Trace("word_init"))

    @property
    def unit_value(self) -> str:
        """Return the word form."""
        return self.built_form.surface_form

    failure_type: Optional[str] = None

    def __post_init__(self):
        validate_no_meaning_field(self)
