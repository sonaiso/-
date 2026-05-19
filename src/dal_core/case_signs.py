"""
Case Sign Modeling (نمذجة علامات الإعراب)

Models original and substitute case signs as surface observations,
NOT as grammatical case effects.

CRITICAL DISTINCTION:
- CaseSignPotential: surface observation + compatible interpretations (ALLOWED in MufradProof)
- CaseEffect: grammatical judgment by operator (FORBIDDEN in MufradProof)

The hundred nahw operators will work on CaseSignPotential to produce CaseEffectCandidate.
"""

from dataclasses import dataclass
from enum import Enum

from dal_core.ranks import LughaRank
from dal_core.residuals import Residual
from dal_core.evidence import Evidence
from dal_core.surface_effects import SurfaceEffect


class CaseSignFamily(Enum):
    """
    عائلة العلامة الإعرابية

    Classification of case sign types.
    """
    ORIGINAL = "أصلية"
    """Original case marks: damma, fatha, kasra, sukun"""

    SUBSTITUTE = "فرعية"
    """Substitute marks: alif, waw, ya, nun retention/deletion, weak letter modifications"""

    BUILDING = "بناء"
    """Building on diacritics (invariant marking)"""

    ESTIMATED = "مقدرة"
    """Estimated/hidden marks"""

    UNRESOLVED = "غير محسومة"
    """Competing or unresolved sign interpretations"""


class CaseSignValue(Enum):
    """
    قيمة العلامة الإعرابية

    Enumeration of all case sign values (original + substitute).

    These are SURFACE OBSERVATIONS, not grammatical judgments.
    """
    # Original signs (علامات أصلية)
    DAMMA = "ضمة"
    FATHA = "فتحة"
    KASRA = "كسرة"
    SUKUN = "سكون"

    # Substitute signs for nouns (علامات فرعية للأسماء)
    ALIF = "ألف"              # dual rafa, five nouns nasb
    WAW = "واو"               # sound masc plural rafa, five nouns rafa
    YA = "ياء"                # dual nasb/jarr, sound masc plural nasb/jarr, five nouns jarr

    # Nun handling (حذف النون وثبوتها)
    NUN_RETAINED = "ثبوت النون"
    NUN_DELETED = "حذف النون"

    # Weak letter effects (حروف العلة)
    WEAK_LETTER_DELETED = "حذف حرف العلة"
    WEAK_LETTER_REPLACED = "تبديل حرف العلة"

    # Tanwin (treated as potential marker)
    TANWIN_DAMM = "تنوين ضم"
    TANWIN_FATH = "تنوين فتح"
    TANWIN_KASR = "تنوين كسر"

    # Estimated signs
    ESTIMATED_DAMMA = "ضمة مقدرة"
    ESTIMATED_FATHA = "فتحة مقدرة"
    ESTIMATED_KASRA = "كسرة مقدرة"

    # Unresolved
    UNRESOLVED_SIGN = "علامة غير محسومة"


@dataclass(frozen=True)
class CaseSignPotential:
    """
    احتمال العلامة الإعرابية

    A surface case sign observation that MAY support one or more case effects
    when combined with operator and relation contracts.

    ALLOWED in MufradProof.

    This is NOT a case effect judgment. It only says:
    "This surface sign was observed, and it is compatible with these potential
    case interpretations, but no operator has applied yet."

    Example:
        observed_surface: FINAL_DAMMA
        sign_family: ORIGINAL
        sign_value: DAMMA
        compatible_case_effects: ("rafa_candidate", "building_on_damma_candidate")

    The actual case effect (marfu' vs mabni) can only be determined by
    OperatorCandidate + RelationCandidate in composition layer.
    """

    observed_surface: SurfaceEffect
    """The actual surface effect observed on the word"""

    sign_family: CaseSignFamily
    """Classification: original, substitute, building, estimated, unresolved"""

    sign_value: CaseSignValue
    """The specific sign value"""

    compatible_case_effects: tuple[str, ...]
    """
    Names of compatible case effects (NOT applied case effects).

    Examples:
    - DAMMA → ("rafa_candidate", "building_on_damma_candidate")
    - FATHA → ("nasb_candidate", "building_on_fatha_candidate", "substitute_for_kasra_candidate")
    - ALIF → ("dual_rafa_candidate", "five_nouns_nasb_candidate")
    - NUN_DELETED → ("five_verbs_jazm_candidate", "five_verbs_nasb_candidate")

    These are string identifiers only. The actual CaseEffectCandidate
    will be created by NahwOperatorRegistry in composition layer.
    """

    evidence: Evidence
    """Evidence for this sign observation"""

    rank: LughaRank
    """Rank of the sign observation (inherited from surface analysis)"""

    residuals: tuple[Residual, ...]
    """Residuals from sign analysis"""

    trace_id: str
    """Trace linking to witness/evidence chain"""

    def __post_init__(self):
        """Validate that this is a potential, not an effect"""
        # Forbidden field names (these belong to CaseEffect, not CaseSignPotential)
        forbidden_terms = [
            'marfoo', 'mansub', 'majrur', 'majzum',  # Case judgments
            'governed_by', 'operator', 'relation',     # Syntax governance
            'faail', 'mafool', 'mubtada', 'khabar',   # Syntax roles
        ]

        # Check compatible_case_effects are names only (candidates)
        for effect_name in self.compatible_case_effects:
            if not effect_name.endswith('_candidate'):
                # Verify it's a descriptive name, not a judgment
                for term in forbidden_terms:
                    if term in effect_name.lower():
                        raise ValueError(
                            f"CaseSignPotential cannot contain case judgment: {effect_name}. "
                            f"Use '*_candidate' naming for compatibility list."
                        )


# Residual types for case sign analysis
class CaseSignResidualType:
    """Residual types specific to case sign analysis"""

    MUFRAD_CASE_SIGN_UNRESOLVED = "MUFRAD_CASE_SIGN_UNRESOLVED"
    """Multiple competing case sign interpretations"""

    MUFRAD_ORIGINAL_SIGN_UNRESOLVED = "MUFRAD_ORIGINAL_SIGN_UNRESOLVED"
    """Ambiguity in original sign interpretation"""

    MUFRAD_SUBSTITUTE_SIGN_UNRESOLVED = "MUFRAD_SUBSTITUTE_SIGN_UNRESOLVED"
    """Ambiguity in substitute sign interpretation"""

    MUFRAD_ESTIMATED_SIGN_REQUIRES_TRACE = "MUFRAD_ESTIMATED_SIGN_REQUIRES_TRACE"
    """Estimated sign needs stronger evidence/trace"""

    MUFRAD_TANWIN_DEFINITENESS_CONFLICT = "MUFRAD_TANWIN_DEFINITENESS_CONFLICT"
    """Tanwin appears on definite noun (impossible)"""

    MUFRAD_SIGN_INFLECTION_CLASS_MISMATCH = "MUFRAD_SIGN_INFLECTION_CLASS_MISMATCH"
    """Case sign doesn't match noun inflection class"""
