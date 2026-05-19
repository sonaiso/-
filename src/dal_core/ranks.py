"""
Rank System (نظام الرتب)

Tracks levels of linguistic attestation following Nabahani methodology.
"""

from enum import Enum


class LughaRank(Enum):
    """
    رتبة الثبوت اللغوي

    Linguistic attestation ranks from lowest to highest.
    Based on طريق معرفة العربية (ways of knowing Arabic).
    """

    ZERO = 0      # غير ثابت - Not attested at all
    FORM = 1      # صورة فقط - Valid form/pattern only
    QIYAS = 2     # قياس مرخص - Permitted by analogy
    SAMA = 3      # سماع خاص - Specific hearing/citation
    AHAD = 4      # آحاد لغوي - Singular linguistic transmission
    TAWATUR = 5   # تواتر - Mass transmission

    def __lt__(self, other):
        if not isinstance(other, LughaRank):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other):
        if not isinstance(other, LughaRank):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other):
        if not isinstance(other, LughaRank):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other):
        if not isinstance(other, LughaRank):
            return NotImplemented
        return self.value >= other.value


class FormRank(Enum):
    """
    رتبة الصورة

    Ranks for form-level confidence (D_form stage).
    """

    MALFORMED = 0  # مشوهة - Invalid structure
    TENTATIVE = 1  # محتملة - Possible but uncertain
    FORM = 2       # صورة - Valid form
    CONFIDENT = 3  # واثقة - High confidence


def rank_to_arabic(rank: LughaRank) -> str:
    """Convert rank to Arabic description"""
    mapping = {
        LughaRank.ZERO: "غير ثابت",
        LughaRank.FORM: "صورة فقط",
        LughaRank.QIYAS: "قياس مرخص",
        LughaRank.SAMA: "سماع خاص",
        LughaRank.AHAD: "آحاد لغوي",
        LughaRank.TAWATUR: "تواتر",
    }
    return mapping.get(rank, "مجهول")
