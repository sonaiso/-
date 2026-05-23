"""
DalMadlulBindingType - أنواع الربط بين الدال والمدلول

Defines types of neutral binding relations between signifier and signified.
"""

from enum import Enum, auto
from typing import Optional


class DalMadlulBindingType(Enum):
    """
    Types of neutral binding between Dāl (signifier) and Madlūl (signified).

    Critical Law:
        These are NEUTRAL relation types, not semantic interpretation types.
        Binding type ≠ Dalalah type.

    Types:
        SIMPLE_BINDING: Direct one-to-one binding (دال واحد ← مدلول واحد)
        COMPOSITE_BINDING: Composite binding (دال مركب ← مدلول مركب)
        PARTIAL_BINDING: Partial binding with residuals
        CONDITIONAL_BINDING: Binding with conditions/constraints
        UNKNOWN_BINDING: Unknown binding type (becomes residual)
    """

    SIMPLE_BINDING = auto()           # دال واحد ← مدلول واحد
    COMPOSITE_BINDING = auto()        # دال مركب ← مدلول مركب
    PARTIAL_BINDING = auto()          # ربط جزئي
    CONDITIONAL_BINDING = auto()      # ربط مشروط
    UNKNOWN_BINDING = auto()          # ربط غير معروف

    @property
    def is_simple(self) -> bool:
        """Check if binding is simple one-to-one."""
        return self == DalMadlulBindingType.SIMPLE_BINDING

    @property
    def is_composite(self) -> bool:
        """Check if binding is composite."""
        return self == DalMadlulBindingType.COMPOSITE_BINDING

    @property
    def is_partial(self) -> bool:
        """Check if binding is partial."""
        return self == DalMadlulBindingType.PARTIAL_BINDING

    @property
    def is_conditional(self) -> bool:
        """Check if binding has conditions."""
        return self == DalMadlulBindingType.CONDITIONAL_BINDING

    @property
    def is_unknown(self) -> bool:
        """Check if binding type is unknown."""
        return self == DalMadlulBindingType.UNKNOWN_BINDING

    @property
    def requires_resolution(self) -> bool:
        """Check if binding requires further resolution."""
        return self in {
            DalMadlulBindingType.PARTIAL_BINDING,
            DalMadlulBindingType.CONDITIONAL_BINDING,
            DalMadlulBindingType.UNKNOWN_BINDING,
        }

    def describe(self) -> str:
        """Return Arabic description of binding type."""
        descriptions = {
            DalMadlulBindingType.SIMPLE_BINDING: "ربط بسيط (دال ← مدلول)",
            DalMadlulBindingType.COMPOSITE_BINDING: "ربط مركب",
            DalMadlulBindingType.PARTIAL_BINDING: "ربط جزئي",
            DalMadlulBindingType.CONDITIONAL_BINDING: "ربط مشروط",
            DalMadlulBindingType.UNKNOWN_BINDING: "ربط غير معروف",
        }
        return descriptions.get(self, "نوع ربط غير محدد")
