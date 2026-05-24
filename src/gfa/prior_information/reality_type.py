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

    Eight types of existence, determined within domains:

    UNSPECIFIED: Unspecified/unknown existence type (default safety state)
        Must be determined before admission - prevents dangerous defaults

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

    Critical Safety Law:
        Default to UNSPECIFIED (not EXTERNAL) to prevent accidental ontological claims
    """

    UNSPECIFIED = auto()    # غير محدد - Safety default
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
            RealityType.UNSPECIFIED,  # UNSPECIFIED also requires domain
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

    def is_specified(self) -> bool:
        """Check if existence type has been specified."""
        return self != RealityType.UNSPECIFIED

    def __str__(self) -> str:
        names_ar = {
            RealityType.UNSPECIFIED: "غير محدد",
            RealityType.EXTERNAL: "خارجي",
            RealityType.EFFECTUAL: "أثري",
            RealityType.MENTAL: "ذهني",
            RealityType.VERBAL: "لفظي",
            RealityType.TECHNICAL: "اصطلاحي",
            RealityType.METAPHORICAL: "مجازي",
            RealityType.NORMATIVE: "معياري",
        }
        return names_ar.get(self, self.name)
