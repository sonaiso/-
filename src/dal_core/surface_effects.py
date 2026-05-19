"""
Surface Effects for MufradProof (الآثار السطحية لبرهان المفرد)

Surface phonological/orthographic effects visible on word form.
These belong to MufradProof, NOT to syntax composition.

CRITICAL DISTINCTION:
- SurfaceEffect: visible form on the word (ALLOWED in MufradProof)
- CaseEffect: syntactic case assignment (FORBIDDEN in MufradProof)
"""

from dataclasses import dataclass, field
from enum import Enum

from dal_core.ranks import LughaRank
from dal_core.residuals import Residual
from dal_core.evidence import Evidence


class SurfaceEffectType(Enum):
    """Types of surface effects"""
    # Final vowel/diacritic
    FINAL_DAMMA = "ضمة نهائية"
    FINAL_FATHA = "فتحة نهائية"
    FINAL_KASRA = "كسرة نهائية"
    FINAL_SUKUN = "سكون نهائي"

    # Tanwin
    TANWIN_DAMM = "تنوين ضم"
    TANWIN_FATH = "تنوين فتح"
    TANWIN_KASR = "تنوين كسر"

    # Long vowels (final position)
    FINAL_ALIF = "ألف نهائي"
    FINAL_WAW = "واو نهائي"
    FINAL_YA = "ياء نهائي"

    # Nun handling (dual/plural)
    NUN_RETAINED = "نون محفوظ"
    NUN_DELETED = "نون محذوف"

    # Weak letter effects
    WEAK_LETTER_DELETED = "حرف علة محذوف"
    WEAK_LETTER_REPLACED = "حرف علة مبدل"

    # Visible vs hidden marking
    VISIBLE_FINAL_MARK = "علامة نهائية ظاهرة"
    HIDDEN_FINAL_MARK = "علامة نهائية مقدرة"
    ESTIMATED_EFFECT_CANDIDATE = "أثر مقدر مرشح"


class SurfaceEffectVisibility(Enum):
    """Whether effect is visible in written/vocalized form"""
    VISIBLE = "ظاهر"           # Explicitly marked
    HIDDEN = "مقدر"            # Estimated/implied
    OMITTED = "محذوف"          # Deleted for phonological reasons


@dataclass(frozen=True)
class SurfaceEffect:
    """
    أثر سطحي (Surface Effect)

    A phonological/orthographic effect visible on word surface.

    ALLOWED in MufradProof:
    - Final diacritics (visible or estimated)
    - Tanwin
    - Nun retention/deletion
    - Weak letter modifications
    - Long vowel appearances

    FORBIDDEN in MufradProof:
    - Syntax role (فاعل، مفعول، etc)
    - Operator governance (مرفوع بـ، منصوب بـ)
    - Case assignment reason
    """
    effect_type: SurfaceEffectType
    visibility: SurfaceEffectVisibility
    location: str  # "final" | "penultimate" | "position_N"

    # Proof data
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)

    # Alternative candidates (if effect is ambiguous)
    alternatives: tuple["SurfaceEffect", ...] = field(default_factory=tuple)

    def is_visible(self) -> bool:
        """Check if effect is visible in vocalized text"""
        return self.visibility == SurfaceEffectVisibility.VISIBLE

    def is_final(self) -> bool:
        """Check if effect is in final position"""
        return self.location == "final"

    def __str__(self) -> str:
        return f"SurfaceEffect({self.effect_type.value}, {self.visibility.value})"


def has_forbidden_case_effect_fields(effect: dict) -> bool:
    """
    Detect forbidden CaseEffect fields in SurfaceEffect.

    Returns True if any forbidden field is present.
    """
    forbidden_fields = {
        "case_effect",
        "syntax_role",
        "faail",
        "mafool",
        "mubtada",
        "khabar",
        "majroor_by",
        "mansub_by",
        "marfoo_by",
        "governed_by_operator",
        "governed_by",
        "operator",
    }

    if isinstance(effect, dict):
        return bool(forbidden_fields & set(effect.keys()))
    elif hasattr(effect, "__dict__"):
        return bool(forbidden_fields & set(effect.__dict__.keys()))
    return False
