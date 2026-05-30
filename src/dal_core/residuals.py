"""
Residuals System (البقايا)

Residuals track issues, warnings, and blockers throughout the pipeline.

PR-ARCH0 adapter note
---------------------
This module is a documented adapter surface (migration-gap G3). Per
``docs/ARCHITECTURE_AUTHORITY_MAP.md`` and ``docs/KERNEL_MIGRATION_GAPS.md``
the constitutional ``Residual`` lives in :mod:`fvafk.algebra`; the
``Residual`` defined here is a dal_core domain structure pending a lift
adapter into the kernel and MUST NOT be treated as a parallel kernel
source of truth.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any


class ResidualSeverity(Enum):
    """Severity levels for residuals"""
    INFO = 0      # معلومة - Informational only
    WARNING = 1   # تحذير - Non-blocking warning
    BLOCKER = 2   # مانع - Prevents closure


class ResidualType(Enum):
    """Types of residuals at different pipeline stages"""

    # Carrier level (Unicode → Carrier)
    NON_ARABIC_SYMBOL = "رمز غير عربي"
    AMBIGUOUS_SYMBOL = "رمز ملتبس"
    ORNAMENTAL_SYMBOL = "رمز زخرفي"
    NON_NORMALIZABLE = "غير قابل للتطبيع"

    # Atom level (Carrier → ArabicAtom)
    UNKNOWN_ATOM = "ذرة مجهولة"
    MALFORMED_ATOM = "ذرة مشوهة"

    # Unit level (Atoms → OperativeUnit)
    ORPHAN_MARK = "علامة يتيمة"
    MISSING_VOCALIZATION = "تشكيل ناقص"
    DOUBLE_VOCALIZATION = "تشكيل مزدوج"

    # Syllable level (Units → Syllables)
    INVALID_SYLLABLE = "مقطع غير صحيح"
    SYLLABLE_VIOLATION = "خرق قاعدة مقطعية"

    # Form level (Syllables → FormCandidate)
    MALFORMED_STRUCTURE = "بنية مشوهة"
    UNRECOGNIZED_PATTERN = "وزن غير معروف"

    # Lugha level (Form → LughaAttestation)
    NOT_ATTESTED = "غير مثبت لغويًا"
    LOW_CONFIDENCE = "ثقة منخفضة"
    FOREIGN_WORD = "لفظ دخيل"

    # Type level (Attestation → TypedDal)
    AMBIGUOUS_TYPE = "نوع ملتبس"
    CONFLICTING_TYPE = "نوع متضارب"

    # Mufrad level (TypedDal → DClosed)
    NOT_MUFRAD = "ليس مفردًا"
    NOT_PLACEABLE = "غير صالح للوضع"
    COMPOSITIONAL = "تركيبي"

    # Morphological proof level (NEW: Phase 2.5)
    MORPH_ANALYSIS_INCOMPLETE = "تحليل صرفي غير مكتمل"
    ROOT_UNRESOLVED = "جذر غير محسوم"
    WAZN_UNRESOLVED = "وزن غير محسوم"
    MABNI_MURAB_COMPETING = "تنافس مبني/معرب"
    MABNI_MURAB_UNRESOLVED = "مبني/معرب غير محسوم"
    JAMID_MUSHTAQ_COMPETING = "تنافس جامد/مشتق"
    DEFINITENESS_UNRESOLVED = "تعريف غير محسوم"
    GENDER_UNRESOLVED = "جنس غير محسوم"
    NUMBER_UNRESOLVED = "عدد غير محسوم"
    VERB_FEATURES_INCOMPLETE = "خصائص فعلية ناقصة"
    SURFACE_EFFECT_UNRESOLVED = "أثر سطحي غير محسوم"
    NOT_COMPOSITION_READY = "غير جاهز للتركيب"

    # Additional required residuals for compliance
    MISSING_VISIBLE_HARAKA = "حركات مفقودة"
    INVALID_SYLLABLE_PATTERN = "نمط مقطعي غير صحيح"
    FORM_ONLY_NOT_LUGHA = "صورة فقط لا لغة"
    WEIGHT_NOT_ATTESTATION = "الوزن لا يثبت العربية"
    LUGHA_WITNESS_MISSING = "شاهد لغوي مفقود"
    TYPE_UNRESOLVED = "نوع غير محسوم"
    TYPE_REQUIRES_LUGHA = "النوع يتطلب ثبوتًا لغويًا"
    MUFRAD_REQUIRES_FORM = "المفرد يتطلب صورة"
    MUFRAD_REQUIRES_LUGHA = "المفرد يتطلب ثبوتًا لغويًا"
    MUFRAD_REQUIRES_TYPE = "المفرد يتطلب نوعًا"

    # Contract violation detection
    DAL_SEMANTIC_LEAK = "تسرب دلالي في الدال"
    DAL_GROUNDING_LEAK = "تسرب إحالي في الدال"
    DAL_MURAD_LEAK = "تسرب مرادي في الدال"
    DAL_CONTRACT_SILENT_LEVEL_SKIP = "تخطي مستوى صامت"
    REVERSE_TRACE_MISSING_RAW_INPUT = "أثر عكسي يفتقد المدخل الخام"
    FOLD_TRACE_MISSING_SOURCE_UNITS = "أثر طي يفتقد الوحدات المصدر"
    RANK_WEAKEST_LINK_VIOLATION = "خرق سقف أضعف حلقة"
    RESIDUAL_ERASURE = "محو البقايا"

    # MufradProof residuals
    MUFRAD_MORPH_PROOF_MISSING = "برهان صرفي مفقود للمفرد"
    MUFRAD_SURFACE_PROOF_MISSING = "برهان سطحي مفقود للمفرد"
    MUFRAD_SEGMENTATION_UNRESOLVED = "تقطيع غير محسوم للمفرد"
    MUFRAD_STEM_UNRESOLVED = "جذع غير محسوم للمفرد"
    MUFRAD_CLITICS_UNRESOLVED = "ملحقات غير محسومة للمفرد"
    MUFRAD_ROOT_COMPETITION_UNRESOLVED = "تنافس جذور غير محسوم"
    MUFRAD_WAZN_COMPETITION_UNRESOLVED = "تنافس أوزان غير محسوم"
    MUFRAD_DERIVATION_UNRESOLVED = "اشتقاق غير محسوم"
    MUFRAD_JAMID_MUSHTAQ_UNRESOLVED = "جامد/مشتق غير محسوم"
    MUFRAD_MABNI_MURAB_UNRESOLVED = "مبني/معرب غير محسوم"
    MUFRAD_DEFINITENESS_UNRESOLVED = "تعريف/تنكير غير محسوم"
    MUFRAD_GENDER_UNRESOLVED = "جنس غير محسوم"
    MUFRAD_NUMBER_UNRESOLVED = "عدد غير محسوم"
    MUFRAD_VERB_FEATURES_REQUIRED = "خصائص فعلية مطلوبة"
    MUFRAD_NOUN_INFLECTION_REQUIRED = "تصريف اسمي مطلوب"
    MUFRAD_PARTICLE_OPERATOR_POTENTIAL_REQUIRED = "احتمال عملية حرفية مطلوب"
    MUFRAD_COMPETITORS_UNRESOLVED = "منافسون غير محسومين للمفرد"
    MUFRAD_NOT_READY_FOR_COMPOSITION = "المفرد غير جاهز للتركيب"
    CASE_EFFECT_LEAK_IN_MUFRAD = "تسرب أثر إعرابي في المفرد"
    SYNTAX_ROLE_LEAK_IN_MUFRAD = "تسرب دور نحوي في المفرد"
    OPERATOR_ON_TOKEN_FORBIDDEN = "منع العامل على الرمز المباشر"
    COMPOSITION_RANK_OVER_MUFRAD = "رتبة تركيبية تفوق المفرد"
    COMPOSITION_ERASED_MUFRAD_RESIDUAL = "محو بقية مفردية في التركيب"
    COMPOSITION_BLOCKER = "مانع تركيبي"  # Frame composition blocker

    # CaseSignMatrix governance residuals (PR #13)
    # Matrix is post-frame, pre-operator: compatibilities only, never judgments.
    MATRIX_REQUIRES_SENTENCE_FRAME = "المصفوفة تتطلب إطار جملة"
    MATRIX_RANK_CEILING_VIOLATION = "خرق سقف الرتبة في المصفوفة"
    MATRIX_RESIDUAL_INHERITANCE_VIOLATION = "محو بقايا الإطار في المصفوفة"
    MATRIX_UNRESOLVED_REQUIRED_SIGN = "علامة لازمة غير محسومة في المصفوفة"
    MATRIX_ROW_TRACE_MISSING_VECTOR = "صف المصفوفة يفتقد شعاع المفرد"
    SUBSTITUTE_SIGN_REQUIRES_INFLECTION_CLASS = "علامة فرعية تتطلب فئة صرفية"
    CASE_SIGN_COMPATIBILITY_UNRESOLVED = "توافق العلامة الإعرابية غير محسوم"
    ESTIMATED_SIGN_REQUIRES_TRACE_IN_MATRIX = "علامة مقدرة في المصفوفة تتطلب أثرًا"
    MATRIX_BUILDING_STATUS_UNRESOLVED = "حال البناء غير محسوم في المصفوفة"

    # OperatorTriggerPotential governance residuals (PR #14)
    # Trigger layer is post-matrix, pre-operator: candidate operator FAMILIES
    # only, never operators, never relations, never case effects. Competing
    # trigger families are PRESERVED, never silently resolved.
    TRIGGER_REQUIRES_FRAME_AND_MATRIX = "محفز العامل يتطلب إطارًا ومصفوفة"
    TRIGGER_FRAME_MATRIX_ID_MISMATCH = "عدم تطابق معرّف الإطار بين الإطار والمصفوفة"
    TRIGGER_RANK_CEILING_VIOLATION = "خرق سقف الرتبة في محفزات العوامل"
    TRIGGER_RESIDUAL_INHERITANCE_VIOLATION = "محو بقايا المصفوفة في محفزات العوامل"
    TRIGGER_UNRESOLVED_FRAME = "إطار غير محسوم: لا محفز عامل ممكن"
    TRIGGER_FRAGMENT_NO_FAMILY = "إطار شبه جملة لم يستدعِ أيّ عائلة عامل"
    TRIGGER_BLOCKED_BY_MATRIX_RESIDUAL = "محفز عامل مع بقايا مانعة في المصفوفة"
    TRIGGER_PARTICLE_TYPE_UNRESOLVED = "نوع الحرف غير محسوم: لا محفز محدد"
    TRIGGER_COMPETING_FAMILIES_PRESERVED = "محفزات عوامل متنافسة محفوظة دون حسم"

    # NahwOperatorRegistry governance residuals (PR #15)
    # Registry is post-trigger, pre-operator: typed operator ENTRIES lookup
    # only. Never applies an operator, never resolves competing entries,
    # never produces a relation or a case effect.
    REGISTRY_FAMILY_HAS_NO_ENTRIES = "عائلة المحفز لا تحوي مدخلات في السجل"
    REGISTRY_FAMILY_HAS_MULTIPLE_ENTRIES_PRESERVED = "عدة مدخلات في عائلة واحدة محفوظة دون حسم"
    REGISTRY_ENTRY_HAS_SCHOOL_DISAGREEMENT = "خلاف مدارس في مدخل عامل"
    REGISTRY_LOOKUP_RANK_CEILED = "تعليق رتبة في استعلام السجل"

    # OperatorCandidate governance residuals (PR #17)
    # Candidate layer is post-registry: typed (TriggerSource, RegistryEntry)
    # pairs only. Never applies operators, never produces relations/case effects.
    # Preserves ALL competing sources and entries without resolution.
    OPERATOR_CANDIDATE_REQUIRES_TRIGGER_AND_REGISTRY = "المرشح العاملي يتطلب محفزًا وسجلًا"
    OPERATOR_CANDIDATE_RANK_CEILING_VIOLATION = "خرق سقف الرتبة في المرشح العاملي"
    OPERATOR_CANDIDATE_RESIDUAL_INHERITANCE_VIOLATION = "محو بقايا في المرشح العاملي"
    OPERATOR_CANDIDATE_NO_REGISTRY_ENTRIES = "لا مدخلات سجلية للمرشح العاملي"
    OPERATOR_CANDIDATE_COMPETITION_PRESERVED = "منافسة مرشحين عامليين محفوظة دون حسم"
    OPERATOR_CANDIDATE_TRACE_MISSING = "أثر المرشح العاملي مفقود"

    # CaseEffectCandidate governance residuals (PR #160/#161)
    # Case effect layer is post-operator-candidate: typed case effect candidates
    # only. Never produces final case judgments, never produces syntax roles,
    # never produces meaning/ifadah/hukm. Preserves ALL competing case effects.
    CASE_EFFECT_COMPATIBILITY_CONFLICT = "تعارض توافق الأثر الإعرابي"
    CASE_EFFECT_DEFERRED_MISSING_MARK = "تأجيل الأثر الإعرابي لغياب العلامة"
    CASE_EFFECT_NO_POLICY = "لا سياسة أثر إعرابي للعامل"
    CASE_EFFECT_UNRESOLVED_POLICY = "سياسة الأثر الإعرابي غير محسومة"
    CASE_EFFECT_MIXED_POLICY_REQUIRES_SLOT = "سياسة مختلطة رفع/نصب تتطلب موقع معمول"
    CASE_EFFECT_RELATION_MISSING = "علاقة مفقودة في مرشح الأثر الإعرابي"


# TEMPORARY ADAPTER NOTE:
# This DAL residual model remains for compatibility only. The constitutional
# kernel is documented in docs/ALGEBRA_KERNEL_CONSTITUTION.md and this surface
# should migrate to fvafk.algebra.Residual via a documented adapter plan.
@dataclass(frozen=True)
class Residual:
    """
    بقية (Residual)

    Represents an issue, warning, or blocker in processing.
    Frozen for immutability and hashability.
    """
    type: ResidualType
    severity: ResidualSeverity
    message: str
    location: Optional[str] = None
    metadata: Optional[tuple] = None  # Changed to tuple for hashability

    def is_blocker(self) -> bool:
        """Check if this residual prevents closure"""
        return self.severity == ResidualSeverity.BLOCKER

    def is_warning(self) -> bool:
        """Check if this is a warning"""
        return self.severity == ResidualSeverity.WARNING

    def __str__(self) -> str:
        loc = f" at {self.location}" if self.location else ""
        return f"[{self.severity.name}] {self.type.value}{loc}: {self.message}"


def has_blocking_residuals(residuals: list[Residual]) -> bool:
    """Check if any residual is a blocker"""
    return any(r.is_blocker() for r in residuals)


def make_blocker(
    residual_type: ResidualType,
    message: str,
    location: Optional[str] = None,
    **metadata: Any
) -> Residual:
    """Helper to create a blocking residual"""
    # Convert metadata dict to tuple of items for hashability
    meta_tuple = tuple(sorted(metadata.items())) if metadata else None
    return Residual(
        type=residual_type,
        severity=ResidualSeverity.BLOCKER,
        message=message,
        location=location,
        metadata=meta_tuple
    )


def make_warning(
    residual_type: ResidualType,
    message: str,
    location: Optional[str] = None,
    **metadata: Any
) -> Residual:
    """Helper to create a warning residual"""
    # Convert metadata dict to tuple of items for hashability
    meta_tuple = tuple(sorted(metadata.items())) if metadata else None
    return Residual(
        type=residual_type,
        severity=ResidualSeverity.WARNING,
        message=message,
        location=location,
        metadata=meta_tuple
    )


def make_info(
    residual_type: ResidualType,
    message: str,
    location: Optional[str] = None,
    **metadata: Any
) -> Residual:
    """Helper to create an info residual"""
    # Convert metadata dict to tuple of items for hashability
    meta_tuple = tuple(sorted(metadata.items())) if metadata else None
    return Residual(
        type=residual_type,
        severity=ResidualSeverity.INFO,
        message=message,
        location=location,
        metadata=meta_tuple
    )
