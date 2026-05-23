"""
Reality Type - نوع الوجود

Existence types within domains - not bare ontological categories.

Critical Laws:
1. Reality type must be determined within a domain
2. No automatic assignment from name alone
3. Technical/conventional existence requires domain
4. Metaphorical cannot usurp external
"""

from enum import Enum, auto


class RealityType(Enum):
    """
    نوع الوجود - Existence Type

    Seven types of existence, determined within domains:

    EXTERNAL: External/physical existence (الوجود الخارجي)
        Example: الماء (water), النار (fire) - if sensory evidence exists

    EFFECTUAL: Effectual existence via trace (الوجود الأثري)
        Example: أثر قدم (footprint), smoke → fire inference

    MENTAL: Mental/cognitive existence (الوجود الذهني)
        Example: العقل (mind/intellect) - requires mental domain

    VERBAL: Verbal/linguistic existence (الوجود اللفظي)
        Example: اللغة (language) as linguistic system

    TECHNICAL: Technical/conventional existence within domain (الوجود الاصطلاحي)
        Example: العامل (operator) in grammar domain
                 المجتمع (society) in social domain

    METAPHORICAL: Metaphorical existence (الوجود المجازي)
        Example: نار الحرب (fire of war) - metaphor, not external

    NORMATIVE: Normative/value existence (الوجود المعياري)
        Example: العدالة (justice), الحرية (freedom)
    """

    EXTERNAL = auto()       # الوجود الخارجي
    EFFECTUAL = auto()      # الوجود الأثري
    MENTAL = auto()         # الوجود الذهني
    VERBAL = auto()         # الوجود اللفظي
    TECHNICAL = auto()      # الوجود الاصطلاحي
    METAPHORICAL = auto()   # الوجود المجازي
    NORMATIVE = auto()      # الوجود المعياري

    def requires_domain(self) -> bool:
        """Check if this reality type requires domain specification."""
        return self in {
            RealityType.MENTAL,
            RealityType.TECHNICAL,
            RealityType.NORMATIVE,
        }

    def allows_external_leap(self) -> bool:
        """Check if this type can legitimately claim external existence."""
        return self in {RealityType.EXTERNAL, RealityType.EFFECTUAL}

    def is_domain_relative(self) -> bool:
        """Check if this type is relative to domain specification."""
        return self in {
            RealityType.TECHNICAL,
            RealityType.VERBAL,
            RealityType.MENTAL,
        }

    def __str__(self) -> str:
        names_ar = {
            RealityType.EXTERNAL: "خارجي",
            RealityType.EFFECTUAL: "أثري",
            RealityType.MENTAL: "ذهني",
            RealityType.VERBAL: "لفظي",
            RealityType.TECHNICAL: "اصطلاحي",
            RealityType.METAPHORICAL: "مجازي",
            RealityType.NORMATIVE: "معياري",
        }
        return names_ar.get(self, self.name)
