"""
Operative Unit Contract (عقد الوحدة التشغيلية)

Contract 3: ArabicAtoms → OperativeUnit
Combines letter + marks into operational units.
"""

from dataclasses import dataclass, field
from typing import Optional

from dal_core.atoms import ArabicAtom, AtomKind
from dal_core.residuals import Residual, make_blocker, ResidualType


@dataclass
class OperativeUnit:
    """
    وحدة تشغيلية (Operative Unit)

    Smallest operational unit: حرف + حركة
    Combines a base letter with its diacritic marks.

    Enforces Theorem 2: حرف مفرد لا يغلق دالًا
    """
    base_letter: ArabicAtom
    mark_bundle: list[ArabicAtom] = field(default_factory=list)
    position: int = 0
    residuals: list[Residual] = field(default_factory=list)

    def __post_init__(self):
        """Validate operative unit"""
        if not self.base_letter.is_letter():
            self.residuals.append(make_blocker(
                ResidualType.ORPHAN_MARK,
                f"Base must be letter, got {self.base_letter.kind.value}",
                location=f"position {self.position}"
            ))

    def has_vowel(self) -> bool:
        """Check if unit has a vowel"""
        return any(m.kind == AtomKind.VOWEL for m in self.mark_bundle)

    def has_sukun(self) -> bool:
        """Check if unit has sukun"""
        return any(m.kind == AtomKind.SUKUN for m in self.mark_bundle)

    def has_shadda(self) -> bool:
        """Check if unit has shadda"""
        return any(m.kind == AtomKind.SHADDA for m in self.mark_bundle)

    def __str__(self) -> str:
        marks = ''.join(m.carrier.char for m in self.mark_bundle)
        return f"Unit({self.base_letter.carrier.char}{marks})"


def make_unit(
    base_letter: ArabicAtom,
    marks: list[ArabicAtom],
    position: int = 0
) -> OperativeUnit:
    """Create an operative unit"""
    return OperativeUnit(
        base_letter=base_letter,
        mark_bundle=marks,
        position=position
    )
