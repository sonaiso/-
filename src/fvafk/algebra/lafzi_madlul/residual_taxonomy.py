"""Residual Taxonomy for Lafẓī Madlūl Layers.

Residuals are **unresolved aspects** that prevent a layer from reaching
CERTIFIED rank. They accumulate through transitions and must be explicit.

## Core Principle

    البقايا ليست فشلاً، بل هي ما لم يُحل بعد.
    كل بقية يجب أن تُسمى وتُوصف صراحة.

    "Residuals are not failures; they are what remains unresolved.
    Every residual must be explicitly named and described."

## Residual vs Failure

- **Residual**: Unresolved aspect (missing context, ambiguity, untested branch)
  - Does NOT reject the result
  - Prevents promotion to CERTIFIED
  - Can be resolved by additional evidence/context

- **Failure**: Active contradiction (rule violation, constraint broken)
  - DOES reject the result (or part of it)
  - Forces rank to REFUTED if fatal
  - Cannot be resolved without changing the structure

## Taxonomy Structure

Each layer has specific residual types:

- **LetterResidual**: Is this letter from root or affix?
- **HarakahResidual**: Is this harakah binā' or i'rāb?
- **SyllableResidual**: Where does syllable boundary fall?
- **RootResidual**: Is root verified in lexicon?
- **PatternResidual**: Is pattern productive or frozen?
- **FormResidual**: Does form carry fā'iliyyah or maf'ūliyyah potential?
"""

from __future__ import annotations

from enum import Enum, auto


# ===========================================================================
# Base Residual Taxonomy
# ===========================================================================


class LafziResidual(Enum):
    """Base residual types across all lafẓī layers.

    These are the **general categories** of what can remain unresolved.
    """

    # Boundary residuals
    BOUNDARY_UNCLEAR = auto()           # حد غير واضح
    SPAN_AMBIGUOUS = auto()             # نطاق ملتبس

    # Binding residuals
    BINDING_INCOMPLETE = auto()         # ربط ناقص
    DEPENDENCY_UNRESOLVED = auto()      # تبعية غير محسومة

    # Type residuals
    TYPE_UNCERTAIN = auto()             # نوع غير مؤكد
    CLASSIFICATION_PENDING = auto()     # تصنيف معلق

    # Context residuals
    CONTEXT_MISSING = auto()            # سياق مفقود
    ENVIRONMENT_INCOMPLETE = auto()     # بيئة ناقصة

    # Verification residuals
    LEXICON_UNVERIFIED = auto()         # معجم غير محقق
    CORPUS_UNATTESTED = auto()          # مدونة غير مشهودة


# ===========================================================================
# Layer-Specific Residuals
# ===========================================================================


class LetterResidual(Enum):
    """Residuals specific to Letter layer (L1).

    الحرف: ما لم يُحل في طبقة الحرف
    """

    # Boundary questions
    IS_FROM_ROOT = auto()               # هل من الجذر؟
    IS_FROM_AFFIX = auto()              # هل من الزيادة؟
    IS_SEMANTIC_PARTICLE = auto()       # هل حرف معنى؟

    # Type questions
    HAMZA_TYPE_UNCLEAR = auto()         # نوع الهمزة غير واضح
    YAA_TYPE_UNCLEAR = auto()           # نوع الياء غير واضح (أصلية/منقلبة/زائدة)
    WAAW_TYPE_UNCLEAR = auto()          # نوع الواو غير واضح
    ALIF_TYPE_UNCLEAR = auto()          # نوع الألف غير واضح

    # Position questions
    POSITION_IN_ROOT = auto()           # موضع في الجذر (فاء/عين/لام)
    DELETION_SUSPECTED = auto()         # حذف مشتبه
    EPENTHESIS_SUSPECTED = auto()       # إدراج مشتبه


class HarakahResidual(Enum):
    """Residuals specific to Harakah layer (L2).

    الحركة: ما لم يُحل في طبقة الحركة
    """

    # Role questions (CRITICAL: harakah form ≠ harakah role)
    IS_BINAA = auto()                   # هل بناء؟
    IS_IRAAB = auto()                   # هل إعراب؟
    IS_PATTERN_VOWEL = auto()           # هل حركة وزن؟
    IS_EPENTHETIC = auto()              # هل إدراج صوتي؟

    # Context dependency
    ROLE_CONTEXT_DEPENDENT = auto()     # الدور يعتمد على السياق
    CASE_UNRESOLVED = auto()            # الحالة الإعرابية غير محسومة

    # Phonological questions
    DELETION_EXPECTED = auto()          # حذف متوقع (وقف)
    ASSIMILATION_EXPECTED = auto()      # إدغام متوقع


class SyllableResidual(Enum):
    """Residuals specific to Syllable layer (L4).

    المقطع: ما لم يُحل في طبقة المقطع
    """

    # Boundary questions
    BOUNDARY_LEFT_UNCLEAR = auto()      # حد أيسر غير واضح
    BOUNDARY_RIGHT_UNCLEAR = auto()     # حد أيمن غير واضح
    RESYLLABIFICATION = auto()          # إعادة مقطعة محتملة

    # Type questions
    SYLLABLE_TYPE_AMBIGUOUS = auto()    # نوع المقطع ملتبس (CV/CVC/CVV...)
    WEIGHT_UNCLEAR = auto()             # وزن المقطع غير واضح

    # Phonotactic questions
    CLUSTER_RESOLUTION = auto()         # حل تجمع صوامت
    HIATUS_RESOLUTION = auto()          # حل تجاور صوائت


class RootResidual(Enum):
    """Residuals specific to Root layer (L6).

    الجذر: ما لم يُحل في طبقة الجذر
    """

    # Verification questions
    LEXICON_UNVERIFIED = auto()         # لم يُحقق في المعجم
    ATTESTED_BUT_RARE = auto()          # مشهود لكنه نادر
    NEOLOGISM_SUSPECTED = auto()        # مستحدث مشتبه

    # Structure questions
    ROOT_TYPE_UNCERTAIN = auto()        # نوع الجذر غير مؤكد (ثلاثي/رباعي...)
    ORIGINAL_LETTERS = auto()           # الأحرف الأصلية غير محسومة
    RADICAL_ORDER = auto()              # ترتيب الأصول غير مؤكد

    # Defectiveness questions
    WEAK_RADICAL_POSITION = auto()      # موضع الحرف المعتل
    ASSIMILATED_RADICAL = auto()        # أصل مدغم
    DELETED_RADICAL = auto()            # أصل محذوف


class PatternResidual(Enum):
    """Residuals specific to Pattern layer (L8).

    الوزن: ما لم يُحل في طبقة الوزن
    """

    # Pattern identification
    PATTERN_FORM_UNCERTAIN = auto()     # صيغة الوزن غير مؤكدة
    AUGMENTATION_COUNT = auto()         # عدد الزيادات غير محسوم

    # Semantic potential (NOT meaning!)
    POTENTIAL_UNRESOLVED = auto()       # الإمكان غير محسوم
    DIRECTION_AMBIGUOUS = auto()        # الاتجاه ملتبس (فاعلية/مفعولية)

    # Productivity questions
    PRODUCTIVE_STATUS = auto()          # حالة الإنتاجية (منتج/جامد)
    ANALOGICAL_EXTENSION = auto()       # امتداد قياسي محتمل

    # Slot alignment
    SLOT_MISMATCH = auto()              # عدم توافق مواضع
    VOWEL_MELODY_UNCLEAR = auto()       # لحن الصوائت غير واضح


class FormResidual(Enum):
    """Residuals specific to BuiltForm layer (L9).

    الصيغة: ما لم يُحل في طبقة الصيغة
    """

    # Root-pattern binding
    ROOT_PATTERN_MISMATCH = auto()      # عدم توافق جذر-وزن
    AFFIX_INTEGRATION = auto()          # دمج الزيادات غير كامل

    # Phonological adjustments
    ASSIMILATION_PENDING = auto()       # إدغام معلق
    DELETION_PENDING = auto()           # حذف معلق
    EPENTHESIS_PENDING = auto()         # إدراج معلق

    # Morphophonemic
    VOWEL_HARMONY_INCOMPLETE = auto()   # توافق الصوائت ناقص
    STRESS_PATTERN_UNCLEAR = auto()     # نمط النبر غير واضح

    # Lexical status
    FORM_LEXICALIZED = auto()           # الصيغة متعجمة (frozen)
    FORM_COMPOSITIONAL = auto()         # الصيغة تركيبية (productive)

    # Semantic potential (NOT direct meaning!)
    FAALIYYAH_POTENTIAL = auto()        # إمكان الفاعلية
    MAFUULIYYAH_POTENTIAL = auto()      # إمكان المفعولية
    SIFAH_POTENTIAL = auto()            # إمكان الوصفية
    MASDAR_POTENTIAL = auto()           # إمكان المصدرية


# ===========================================================================
# Residual Promotion Helpers
# ===========================================================================


def is_resolvable_with_context(residual: LafziResidual | LetterResidual | HarakahResidual | SyllableResidual | RootResidual | PatternResidual | FormResidual) -> bool:
    """Check if residual can be resolved with additional context.

    Some residuals are **intrinsically unresolvable** at their layer
    (require semantic judgment). Others can be resolved with more evidence.

    Args:
        residual: Residual to check

    Returns:
        True if resolvable with more context/evidence

    Example::

        if is_resolvable_with_context(LetterResidual.IS_FROM_ROOT):
            # Can be resolved by checking root candidates
            pass

        if not is_resolvable_with_context(FormResidual.FAALIYYAH_POTENTIAL):
            # Requires semantic judgment (external to lafẓī)
            pass
    """
    # Context-dependent residuals (resolvable)
    RESOLVABLE = {
        # Letter
        LetterResidual.IS_FROM_ROOT,
        LetterResidual.IS_FROM_AFFIX,
        LetterResidual.POSITION_IN_ROOT,

        # Harakah
        HarakahResidual.IS_BINAA,
        HarakahResidual.IS_IRAAB,
        HarakahResidual.IS_PATTERN_VOWEL,

        # Syllable
        SyllableResidual.BOUNDARY_LEFT_UNCLEAR,
        SyllableResidual.BOUNDARY_RIGHT_UNCLEAR,

        # Root
        RootResidual.LEXICON_UNVERIFIED,
        RootResidual.ROOT_TYPE_UNCERTAIN,

        # Pattern
        PatternResidual.PATTERN_FORM_UNCERTAIN,
        PatternResidual.PRODUCTIVE_STATUS,
    }

    # Semantic-dependent residuals (NOT resolvable at lafẓī level)
    UNRESOLVABLE_LEXICAL = {
        FormResidual.FAALIYYAH_POTENTIAL,
        FormResidual.MAFUULIYYAH_POTENTIAL,
        FormResidual.SIFAH_POTENTIAL,
        FormResidual.MASDAR_POTENTIAL,
    }

    if residual in UNRESOLVABLE_LEXICAL:
        return False

    if residual in RESOLVABLE:
        return True

    # Default: assume resolvable with more evidence
    return True


def residual_to_description(residual: LafziResidual | LetterResidual | HarakahResidual | SyllableResidual | RootResidual | PatternResidual | FormResidual) -> str:
    """Convert residual enum to human-readable Arabic description.

    Args:
        residual: Residual to describe

    Returns:
        Arabic description string

    Example::

        desc = residual_to_description(LetterResidual.IS_FROM_ROOT)
        # Returns: "هل هذا الحرف من الجذر؟"
    """
    DESCRIPTIONS = {
        # Letter
        LetterResidual.IS_FROM_ROOT: "هل هذا الحرف من الجذر؟",
        LetterResidual.IS_FROM_AFFIX: "هل هذا الحرف من الزيادة؟",
        LetterResidual.IS_SEMANTIC_PARTICLE: "هل هذا حرف معنى؟",

        # Harakah
        HarakahResidual.IS_BINAA: "هل هذه الحركة بنائية؟",
        HarakahResidual.IS_IRAAB: "هل هذه الحركة إعرابية؟",
        HarakahResidual.IS_PATTERN_VOWEL: "هل هذه حركة وزن؟",
        HarakahResidual.ROLE_CONTEXT_DEPENDENT: "دور الحركة يعتمد على السياق",

        # Syllable
        SyllableResidual.BOUNDARY_LEFT_UNCLEAR: "حد المقطع الأيسر غير واضح",
        SyllableResidual.BOUNDARY_RIGHT_UNCLEAR: "حد المقطع الأيمن غير واضح",

        # Root
        RootResidual.LEXICON_UNVERIFIED: "الجذر لم يُحقق في المعجم",
        RootResidual.NEOLOGISM_SUSPECTED: "الجذر قد يكون مستحدثاً",

        # Pattern
        PatternResidual.PATTERN_FORM_UNCERTAIN: "صيغة الوزن غير مؤكدة",
        PatternResidual.PRODUCTIVE_STATUS: "حالة إنتاجية الوزن غير محسومة",
        PatternResidual.POTENTIAL_UNRESOLVED: "الإمكان الصرفي غير محسوم",

        # Form
        FormResidual.FAALIYYAH_POTENTIAL: "إمكان الفاعلية (يحتاج حكماً دلالياً)",
        FormResidual.MAFUULIYYAH_POTENTIAL: "إمكان المفعولية (يحتاج حكماً دلالياً)",
        FormResidual.FORM_LEXICALIZED: "الصيغة متعجمة (جامدة)",
        FormResidual.FORM_COMPOSITIONAL: "الصيغة تركيبية (منتجة)",
    }

    return DESCRIPTIONS.get(residual, residual.name)


__all__ = [
    "LafziResidual",
    "LetterResidual",
    "HarakahResidual",
    "SyllableResidual",
    "RootResidual",
    "PatternResidual",
    "FormResidual",
    "is_resolvable_with_context",
    "residual_to_description",
]
