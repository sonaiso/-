"""
MadlulLafziType - أنواع المدلول اللفظي

Defines the types of linguistic signifieds (Madlūl-lafẓī) that can serve
as second term in signification relation within the linguistic domain.

Critical Law:
    المدلول اللفظي ليس معنى خارجياً بالضرورة
    Madlūl-lafẓī is NOT necessarily external meaning.
    Madlūl-lafẓī is a governed candidate for what may be signified
    inside the linguistic domain.

Madlul-Lafzi Types:
    - LETTER_ENTITY: Letter as linguistic entity (حرف ككيان لفظي)
    - HARAKAH_ENTITY: Diacritic as linguistic entity (حركة ككيان لفظي)
    - SYLLABLE_ENTITY: Syllable as linguistic entity (مقطع ككيان لفظي)
    - ROOT_CANDIDATE: Root candidate (جذر مرشح)
    - PATTERN_ENTITY: Pattern/weight as linguistic entity (وزن ككيان لفظي)
    - FORM_ENTITY: Form as linguistic entity (صيغة ككيان لفظي)
    - WORD_ENTITY: Word as linguistic entity (لفظ ككيان لفظي)
    - COMPOSITE_LAFZI_ENTITY: Composite linguistic entity (تركيب لفظي)
    - CONCEPTUAL_LAFZI_ENTITY: Conceptual linguistic entity (مفهوم لفظي)
    - UNKNOWN_MADLUL: Unknown madlul type (becomes residual, not error)

Critical:
    UNKNOWN madlul type does NOT raise exception.
    UNKNOWN becomes governed residual for future resolution.

What MadlulLafziType Is:
    - Type classifier for linguistic signifieds
    - Domain-internal classification
    - Does NOT determine external meaning
    - Does NOT create Dalalah
    - Does NOT establish Wadh

What MadlulLafziType Is NOT:
    - NOT a semantic category
    - NOT an external meaning type
    - NOT a truth value
    - NOT a Dalalah relation
"""

from __future__ import annotations
from enum import Enum


class MadlulLafziType(Enum):
    """
    Types of linguistic signifieds (المدلول اللفظي).

    Each type represents a different kind of linguistic entity
    that can serve as signified within the linguistic domain.

    UNKNOWN is a residual state, not an error state.
    """

    LETTER_ENTITY = "letter_entity"                       # حرف ككيان
    HARAKAH_ENTITY = "harakah_entity"                     # حركة ككيان
    SYLLABLE_ENTITY = "syllable_entity"                   # مقطع ككيان
    ROOT_CANDIDATE = "root_candidate"                     # جذر مرشح
    PATTERN_ENTITY = "pattern_entity"                     # وزن ككيان
    FORM_ENTITY = "form_entity"                           # صيغة ككيان
    WORD_ENTITY = "word_entity"                           # لفظ ككيان
    COMPOSITE_LAFZI_ENTITY = "composite_lafzi_entity"     # تركيب لفظي
    CONCEPTUAL_LAFZI_ENTITY = "conceptual_lafzi_entity"   # مفهوم لفظي
    UNKNOWN_MADLUL = "unknown_madlul"                     # مدلول مجهول

    @property
    def is_known(self) -> bool:
        """Check if madlul type is known (not UNKNOWN)."""
        return self != MadlulLafziType.UNKNOWN_MADLUL

    @property
    def is_letter(self) -> bool:
        """Check if madlul is letter entity."""
        return self == MadlulLafziType.LETTER_ENTITY

    @property
    def is_harakah(self) -> bool:
        """Check if madlul is harakah entity."""
        return self == MadlulLafziType.HARAKAH_ENTITY

    @property
    def is_pattern(self) -> bool:
        """Check if madlul is pattern entity."""
        return self == MadlulLafziType.PATTERN_ENTITY

    @property
    def is_root_candidate(self) -> bool:
        """Check if madlul is root candidate."""
        return self == MadlulLafziType.ROOT_CANDIDATE

    def __str__(self) -> str:
        return f"MadlulLafziType.{self.name}"

    def __repr__(self) -> str:
        return f"MadlulLafziType.{self.name}"
