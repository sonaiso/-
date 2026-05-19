"""
Syllable Contract (عقد المقطع)

Contract 5: OperativeUnits → Syllables
Folds units into prosodic syllables (CV, CVC, CVV, CVVC).
"""

from dataclasses import dataclass, field
from enum import Enum

from dal_core.atoms import ArabicAtom
from dal_core.units import OperativeUnit
from dal_core.residuals import Residual


class SyllableType(Enum):
    """أنواع المقاطع (Syllable Types)"""
    CV = "قصير مفتوح"      # Short open
    CVC = "قصير مغلق"      # Short closed
    CVV = "طويل مفتوح"     # Long open
    CVVC = "طويل مغلق"     # Long closed


@dataclass
class Syllable:
    """
    مقطع (Syllable)

    Prosodic syllable unit.
    """
    type: SyllableType
    onset: list[ArabicAtom] = field(default_factory=list)
    nucleus: list[ArabicAtom] = field(default_factory=list)
    coda: list[ArabicAtom] = field(default_factory=list)
    units: list[OperativeUnit] = field(default_factory=list)
    residuals: list[Residual] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Syllable({self.type.value})"
