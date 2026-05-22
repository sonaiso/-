"""
WadhScope - نطاق الوضع

Critical Law:
    النطاق يحدد مجال الموضوع له، لا المعنى الخارجي
    Scope defines domain of placed-for, NOT external meaning.

WadhScope represents the domain/context where Wadh applies.

What WadhScope Does:
    - Classifies domain of Wadh claim
    - Distinguishes linguistic/logical/conventional scopes
    - Guards against scope expansion
    - Creates residuals for unknown scopes

What WadhScope Does NOT Do:
    - Does NOT create meaning
    - Does NOT certify semantic content
    - Does NOT implement full Dalālah
    - Does NOT bypass scope boundaries

Position in Architecture:
    WadhGeometry (PR-L5A)
    ├── WadhSource
    ├── WadhTransmissionMode
    ├── WadhScope ← THIS MODULE
    └── ...
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass


class WadhScopeKind(Enum):
    """
    Categories of Wadh scope.

    Critical Law: Scope limits domain, does not create meaning.
    """

    # Linguistic scopes
    LAFZI = "lafzi"                                    # لفظي (linguistic)
    LAFZI_LUGHA_ARABI = "lafzi_lugha_arabi"           # لفظي (لغة عربية)
    LAFZI_DOMAIN_SPECIFIC = "lafzi_domain_specific"    # لفظي (مجال خاص)

    # Logical scopes
    AQLIY_MANTIQIY = "aqliy_mantiqiy"                 # عقلي منطقي (logical)

    # Conventional scopes
    ISTILAHY = "istilahy"                             # اصطلاحي (conventional/technical)
    URFI = "urfi"                                      # عرفي (customary)

    # Unknown/residual
    UNKNOWN_SCOPE = "unknown_scope"                    # مجهول النطاق

    @property
    def is_linguistic(self) -> bool:
        """Check if scope is linguistic (lafzi)."""
        return self in {
            WadhScopeKind.LAFZI,
            WadhScopeKind.LAFZI_LUGHA_ARABI,
            WadhScopeKind.LAFZI_DOMAIN_SPECIFIC,
        }

    @property
    def is_logical(self) -> bool:
        """Check if scope is logical."""
        return self == WadhScopeKind.AQLIY_MANTIQIY

    @property
    def is_conventional(self) -> bool:
        """Check if scope is conventional."""
        return self in {
            WadhScopeKind.ISTILAHY,
            WadhScopeKind.URFI,
        }

    @property
    def is_known(self) -> bool:
        """Check if scope is known (not UNKNOWN_SCOPE)."""
        return self != WadhScopeKind.UNKNOWN_SCOPE


@dataclass(frozen=True)
class WadhScope:
    """
    Wadh scope classification.

    Represents the domain where Wadh claim applies.

    Critical Properties:
        - kind: Scope category
        - description: Scope details
        - is_linguistic: Whether scope is linguistic
        - is_logical: Whether scope is logical
        - is_conventional: Whether scope is conventional

    Critical Laws:
        - Scope defines domain, NOT meaning
        - Scope limits applicability, does NOT certify content
        - Unknown scope becomes residual
        - Scope boundary violations create residuals
    """

    kind: WadhScopeKind
    description: str = ""

    @property
    def is_linguistic(self) -> bool:
        """Check if scope is linguistic."""
        return self.kind.is_linguistic

    @property
    def is_logical(self) -> bool:
        """Check if scope is logical."""
        return self.kind.is_logical

    @property
    def is_conventional(self) -> bool:
        """Check if scope is conventional."""
        return self.kind.is_conventional

    @property
    def is_known(self) -> bool:
        """Check if scope is known."""
        return self.kind.is_known

    @property
    def is_arabic_linguistic(self) -> bool:
        """Check if scope is specifically Arabic linguistic."""
        return self.kind == WadhScopeKind.LAFZI_LUGHA_ARABI

    def __str__(self) -> str:
        scope_type = (
            "LINGUISTIC" if self.is_linguistic
            else "LOGICAL" if self.is_logical
            else "CONVENTIONAL" if self.is_conventional
            else "UNKNOWN"
        )
        return f"WadhScope[{scope_type}]: {self.kind.value}"

    def __repr__(self) -> str:
        return f"WadhScope(kind={self.kind.value})"


# Factory functions for common scopes

def make_lafzi_arabic_scope(description: str = "") -> WadhScope:
    """Create WadhScope for Arabic linguistic domain."""
    return WadhScope(
        kind=WadhScopeKind.LAFZI_LUGHA_ARABI,
        description=description or "Arabic linguistic scope (لفظي - لغة عربية)",
    )


def make_lafzi_scope(description: str = "") -> WadhScope:
    """Create general WadhScope for linguistic domain."""
    return WadhScope(
        kind=WadhScopeKind.LAFZI,
        description=description or "Linguistic scope (لفظي)",
    )


def make_istilahy_scope(description: str = "") -> WadhScope:
    """Create WadhScope for technical/conventional domain."""
    return WadhScope(
        kind=WadhScopeKind.ISTILAHY,
        description=description or "Technical/conventional scope (اصطلاحي)",
    )


def make_urfi_scope(description: str = "") -> WadhScope:
    """Create WadhScope for customary domain."""
    return WadhScope(
        kind=WadhScopeKind.URFI,
        description=description or "Customary scope (عرفي)",
    )


def make_unknown_scope() -> WadhScope:
    """
    Create unknown WadhScope (becomes residual).

    Critical Law: Unknown scope becomes residual.
    """
    return WadhScope(
        kind=WadhScopeKind.UNKNOWN_SCOPE,
        description="Unknown Wadh scope (residual)",
    )
