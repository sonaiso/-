"""
Residuals System (البقايا)

Residuals track issues, warnings, and blockers throughout the pipeline.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Any


class ResidualSeverity(Enum):
    """Severity levels for residuals"""
    INFO = 0      # معلومة - Informational only
    WARNING = 1   # تحذير - Non-blocking warning
    BLOCKER = 2   # مانع - Prevents closure


class ResidualType(Enum):
    """Types of residuals at different pipeline stages"""

    # Carrier level (Unicode → Carrier)
    NON_ARABIC_SYMBOL = "رمز غير عربي"
    AMBIGUOUS_SYMBOL = "رمز ملتبس"
    ORNAMENTAL_SYMBOL = "رمز زخرفي"
    NON_NORMALIZABLE = "غير قابل للتطبيع"

    # Atom level (Carrier → ArabicAtom)
    UNKNOWN_ATOM = "ذرة مجهولة"
    MALFORMED_ATOM = "ذرة مشوهة"

    # Unit level (Atoms → OperativeUnit)
    ORPHAN_MARK = "علامة يتيمة"
    MISSING_VOCALIZATION = "تشكيل ناقص"
    DOUBLE_VOCALIZATION = "تشكيل مزدوج"

    # Syllable level (Units → Syllables)
    INVALID_SYLLABLE = "مقطع غير صحيح"
    SYLLABLE_VIOLATION = "خرق قاعدة مقطعية"

    # Form level (Syllables → FormCandidate)
    MALFORMED_STRUCTURE = "بنية مشوهة"
    UNRECOGNIZED_PATTERN = "وزن غير معروف"

    # Lugha level (Form → LughaAttestation)
    NOT_ATTESTED = "غير مثبت لغويًا"
    LOW_CONFIDENCE = "ثقة منخفضة"
    FOREIGN_WORD = "لفظ دخيل"

    # Type level (Attestation → TypedDal)
    AMBIGUOUS_TYPE = "نوع ملتبس"
    CONFLICTING_TYPE = "نوع متضارب"

    # Mufrad level (TypedDal → DClosed)
    NOT_MUFRAD = "ليس مفردًا"
    NOT_PLACEABLE = "غير صالح للوضع"
    COMPOSITIONAL = "تركيبي"


@dataclass
class Residual:
    """
    بقية (Residual)

    Represents an issue, warning, or blocker in processing.
    """
    type: ResidualType
    severity: ResidualSeverity
    message: str
    location: Optional[str] = None
    metadata: Optional[dict] = None

    def is_blocker(self) -> bool:
        """Check if this residual prevents closure"""
        return self.severity == ResidualSeverity.BLOCKER

    def is_warning(self) -> bool:
        """Check if this is a warning"""
        return self.severity == ResidualSeverity.WARNING

    def __str__(self) -> str:
        loc = f" at {self.location}" if self.location else ""
        return f"[{self.severity.name}] {self.type.value}{loc}: {self.message}"


def has_blocking_residuals(residuals: list[Residual]) -> bool:
    """Check if any residual is a blocker"""
    return any(r.is_blocker() for r in residuals)


def make_blocker(
    residual_type: ResidualType,
    message: str,
    location: Optional[str] = None,
    **metadata: Any
) -> Residual:
    """Helper to create a blocking residual"""
    return Residual(
        type=residual_type,
        severity=ResidualSeverity.BLOCKER,
        message=message,
        location=location,
        metadata=metadata or None
    )


def make_warning(
    residual_type: ResidualType,
    message: str,
    location: Optional[str] = None,
    **metadata: Any
) -> Residual:
    """Helper to create a warning residual"""
    return Residual(
        type=residual_type,
        severity=ResidualSeverity.WARNING,
        message=message,
        location=location,
        metadata=metadata or None
    )


def make_info(
    residual_type: ResidualType,
    message: str,
    location: Optional[str] = None,
    **metadata: Any
) -> Residual:
    """Helper to create an info residual"""
    return Residual(
        type=residual_type,
        severity=ResidualSeverity.INFO,
        message=message,
        location=location,
        metadata=metadata or None
    )
