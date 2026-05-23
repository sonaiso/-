"""
WadhSource - مصدر الوضع

Critical Law:
    مصدر الوضع شاهد فقط، لا وضع بحد ذاته
    Wadh source is evidence witness, NOT Wadh itself.

WadhSource represents the origin of Wadh evidence, not the Wadh convention itself.

What WadhSource Does:
    - Classifies source of Wadh evidence
    - Distinguishes transmission modes (riwayah/naql vs. reason alone)
    - Guards against reason-alone certification for Arabic
    - Creates residuals for unknown sources

What WadhSource Does NOT Do:
    - Does NOT certify Wadh
    - Does NOT create meaning
    - Does NOT implement full Dalālah
    - Does NOT bypass transmission requirements
    - Does NOT issue HUKM

Position in Architecture:
    DalMadlulBindingCandidate (PR-L4, certified)
    └── WadhGeometry (PR-L5A) ← THIS MODULE
        ├── WadhSource
        ├── WadhTransmissionMode
        ├── WadhScope
        ├── WadhEvidence
        ├── WadhClaim
        ├── MawduLahStructure
        └── WadhResidual
"""

from __future__ import annotations

from enum import Enum
from dataclasses import dataclass


class WadhSourceKind(Enum):
    """
    Categories of Wadh evidence sources.

    Critical Law: Source classification ≠ Wadh certification
    """

    # Transmitted sources (acceptable for Arabic Wadh)
    LEXICON_REPORT = "lexicon_report"              # معجم (تقرير فقط)
    USAGE_ATTESTATION = "usage_attestation"        # استعمال (شهادة)
    EXPLICIT_STIPULATION = "explicit_stipulation"  # نص صريح
    TRANSMISSION_CHAIN = "transmission_chain"      # رواية/نقل

    # Non-transmitted sources (evidence only, insufficient for Arabic Wadh alone)
    REASON_INFERENCE = "reason_inference"          # استدلال عقلي
    ANALOGY_QIYAS = "analogy_qiyas"                # قياس

    # Unknown/residual
    UNKNOWN_SOURCE = "unknown_source"              # مجهول المصدر

    @property
    def is_transmitted(self) -> bool:
        """Check if source is transmitted (رواية/نقل)."""
        return self in {
            WadhSourceKind.LEXICON_REPORT,
            WadhSourceKind.USAGE_ATTESTATION,
            WadhSourceKind.EXPLICIT_STIPULATION,
            WadhSourceKind.TRANSMISSION_CHAIN,
        }

    @property
    def is_reason_based(self) -> bool:
        """Check if source is reason-based only."""
        return self in {
            WadhSourceKind.REASON_INFERENCE,
            WadhSourceKind.ANALOGY_QIYAS,
        }

    @property
    def is_known(self) -> bool:
        """Check if source is known (not UNKNOWN_SOURCE)."""
        return self != WadhSourceKind.UNKNOWN_SOURCE

    @property
    def sufficient_for_arabic_wadh(self) -> bool:
        """
        Check if source is sufficient for Arabic Wadh certification.

        Critical Law: Reason alone cannot certify Arabic Wadh.
        Arabic Wadh requires transmission (رواية/نقل/استعمال).
        """
        return self.is_transmitted


@dataclass(frozen=True)
class WadhSource:
    """
    Wadh evidence source classification.

    This represents the source of Wadh evidence, NOT the Wadh itself.

    Critical Properties:
        - kind: Source category
        - description: Source details
        - is_transmitted: Whether source is transmitted
        - sufficient_for_arabic_wadh: Whether sufficient for Arabic

    Critical Laws:
        - WadhSource is evidence, NOT Wadh
        - Lexicon report is evidence, NOT meaning injection
        - Reason alone CANNOT certify Arabic Wadh
        - Unknown source becomes residual
    """

    kind: WadhSourceKind
    description: str = ""

    @property
    def is_transmitted(self) -> bool:
        """Check if source is transmitted."""
        return self.kind.is_transmitted

    @property
    def is_reason_based(self) -> bool:
        """Check if source is reason-based only."""
        return self.kind.is_reason_based

    @property
    def is_known(self) -> bool:
        """Check if source is known."""
        return self.kind.is_known

    @property
    def sufficient_for_arabic_wadh(self) -> bool:
        """
        Check if source is sufficient for Arabic Wadh.

        Critical Law: Reason alone cannot certify Arabic Wadh.
        """
        return self.kind.sufficient_for_arabic_wadh

    @property
    def requires_transmission(self) -> bool:
        """Check if source requires transmission verification."""
        return not self.is_transmitted

    def __str__(self) -> str:
        transmitted = "TRANSMITTED" if self.is_transmitted else "NON-TRANSMITTED"
        return f"WadhSource[{transmitted}]: {self.kind.value}"

    def __repr__(self) -> str:
        return f"WadhSource(kind={self.kind.value})"


# Factory functions for common sources

def make_lexicon_report_source(description: str = "") -> WadhSource:
    """
    Create WadhSource from lexicon report.

    Critical Law: Lexicon report is evidence, NOT Wadh itself.
    """
    return WadhSource(
        kind=WadhSourceKind.LEXICON_REPORT,
        description=description or "Lexicon report (evidence only, not direct meaning injection)",
    )


def make_usage_attestation_source(description: str = "") -> WadhSource:
    """
    Create WadhSource from usage attestation.

    Critical Law: Usage attestation is evidence, NOT UsageGate itself.
    """
    return WadhSource(
        kind=WadhSourceKind.USAGE_ATTESTATION,
        description=description or "Usage attestation (evidence only)",
    )


def make_explicit_stipulation_source(description: str = "") -> WadhSource:
    """Create WadhSource from explicit stipulation."""
    return WadhSource(
        kind=WadhSourceKind.EXPLICIT_STIPULATION,
        description=description or "Explicit stipulation",
    )


def make_reason_inference_source(description: str = "") -> WadhSource:
    """
    Create WadhSource from reason inference.

    Critical Law: Reason alone CANNOT certify Arabic Wadh.
    Requires transmission verification.
    """
    return WadhSource(
        kind=WadhSourceKind.REASON_INFERENCE,
        description=description or "Reason inference (insufficient for Arabic Wadh alone)",
    )


def make_unknown_source() -> WadhSource:
    """
    Create unknown WadhSource (becomes residual).

    Critical Law: Unknown source becomes residual.
    """
    return WadhSource(
        kind=WadhSourceKind.UNKNOWN_SOURCE,
        description="Unknown Wadh source (residual)",
    )
