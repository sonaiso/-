"""
WadhTransmissionMode - نمط نقل الوضع

Critical Law:
    النقل شرط للوضع العربي، لا العقل وحده
    Transmission is condition for Arabic Wadh, not reason alone.

WadhTransmissionMode represents how Wadh evidence was transmitted.

What WadhTransmissionMode Does:
    - Classifies transmission pathway
    - Guards against reason-alone certification
    - Distinguishes direct transmission from inference
    - Creates residuals for unknown modes

What WadhTransmissionMode Does NOT Do:
    - Does NOT certify Wadh
    - Does NOT create meaning
    - Does NOT bypass transmission requirement
    - Does NOT implement full Dalālah

Position in Architecture:
    WadhGeometry (PR-L5A)
    ├── WadhSource
    ├── WadhTransmissionMode ← THIS MODULE
    ├── WadhScope
    └── ...
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass


class WadhTransmissionKind(Enum):
    """
    Categories of Wadh transmission modes.

    Critical Law: Arabic Wadh requires transmission (رواية/نقل/استعمال),
    not reason alone.
    """

    # Direct transmission modes
    RIWAYAH = "riwayah"                    # رواية (narration)
    NAQL = "naql"                          # نقل (transmission)
    USAGE = "usage"                        # استعمال (usage)
    EXPLICIT_TEXT = "explicit_text"        # نص صريح

    # Indirect/inferred modes
    QIYAS = "qiyas"                        # قياس (analogy)
    ISTIDLAL = "istidlal"                  # استدلال (inference)

    # Unknown/residual
    UNKNOWN_MODE = "unknown_mode"          # مجهول النمط

    @property
    def is_direct(self) -> bool:
        """Check if transmission is direct (not inferred)."""
        return self in {
            WadhTransmissionKind.RIWAYAH,
            WadhTransmissionKind.NAQL,
            WadhTransmissionKind.USAGE,
            WadhTransmissionKind.EXPLICIT_TEXT,
        }

    @property
    def is_indirect(self) -> bool:
        """Check if transmission is indirect (inferred)."""
        return self in {
            WadhTransmissionKind.QIYAS,
            WadhTransmissionKind.ISTIDLAL,
        }

    @property
    def is_known(self) -> bool:
        """Check if mode is known (not UNKNOWN_MODE)."""
        return self != WadhTransmissionKind.UNKNOWN_MODE

    @property
    def sufficient_for_arabic_wadh(self) -> bool:
        """
        Check if mode is sufficient for Arabic Wadh.

        Critical Law: Arabic Wadh requires direct transmission,
        not pure reason alone.
        """
        return self.is_direct


@dataclass(frozen=True)
class WadhTransmissionMode:
    """
    Wadh transmission mode classification.

    Represents HOW Wadh evidence was transmitted, not the Wadh itself.

    Critical Properties:
        - kind: Transmission category
        - description: Mode details
        - is_direct: Whether transmission is direct
        - sufficient_for_arabic_wadh: Whether sufficient for Arabic

    Critical Laws:
        - Transmission mode is condition, NOT certification
        - Direct transmission required for Arabic Wadh
        - Reason/inference alone insufficient
        - Unknown mode becomes residual
    """

    kind: WadhTransmissionKind
    description: str = ""

    @property
    def is_direct(self) -> bool:
        """Check if transmission is direct."""
        return self.kind.is_direct

    @property
    def is_indirect(self) -> bool:
        """Check if transmission is indirect (inferred)."""
        return self.kind.is_indirect

    @property
    def is_known(self) -> bool:
        """Check if mode is known."""
        return self.kind.is_known

    @property
    def sufficient_for_arabic_wadh(self) -> bool:
        """
        Check if mode is sufficient for Arabic Wadh.

        Critical Law: Arabic Wadh requires direct transmission.
        """
        return self.kind.sufficient_for_arabic_wadh

    @property
    def requires_verification(self) -> bool:
        """Check if mode requires transmission verification."""
        return not self.is_direct

    def __str__(self) -> str:
        mode_type = "DIRECT" if self.is_direct else "INDIRECT" if self.is_indirect else "UNKNOWN"
        return f"WadhTransmissionMode[{mode_type}]: {self.kind.value}"

    def __repr__(self) -> str:
        return f"WadhTransmissionMode(kind={self.kind.value})"


# Factory functions for common modes

def make_riwayah_mode(description: str = "") -> WadhTransmissionMode:
    """Create WadhTransmissionMode from riwayah (narration)."""
    return WadhTransmissionMode(
        kind=WadhTransmissionKind.RIWAYAH,
        description=description or "Transmitted via riwayah (narration)",
    )


def make_naql_mode(description: str = "") -> WadhTransmissionMode:
    """Create WadhTransmissionMode from naql (transmission)."""
    return WadhTransmissionMode(
        kind=WadhTransmissionKind.NAQL,
        description=description or "Transmitted via naql (transmission)",
    )


def make_usage_mode(description: str = "") -> WadhTransmissionMode:
    """Create WadhTransmissionMode from usage."""
    return WadhTransmissionMode(
        kind=WadhTransmissionKind.USAGE,
        description=description or "Transmitted via usage (استعمال)",
    )


def make_istidlal_mode(description: str = "") -> WadhTransmissionMode:
    """
    Create WadhTransmissionMode from istidlal (inference).

    Critical Law: Inference alone insufficient for Arabic Wadh.
    """
    return WadhTransmissionMode(
        kind=WadhTransmissionKind.ISTIDLAL,
        description=description or "Inferred via istidlal (insufficient for Arabic Wadh alone)",
    )


def make_unknown_mode() -> WadhTransmissionMode:
    """
    Create unknown WadhTransmissionMode (becomes residual).

    Critical Law: Unknown mode becomes residual.
    """
    return WadhTransmissionMode(
        kind=WadhTransmissionKind.UNKNOWN_MODE,
        description="Unknown transmission mode (residual)",
    )
