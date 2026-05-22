"""
WadhResidual - بقايا الوضع

Critical Law:
    البقايا تحفظ، لا تُهمل
    Residuals are preserved, NOT ignored.

WadhResidual represents unresolved aspects in Wadh processing.

What WadhResidual Does:
    - Classifies residual types
    - Preserves unresolved issues
    - Guards against silent failures
    - Blocks when necessary

What WadhResidual Does NOT Do:
    - Does NOT create meaning
    - Does NOT bypass governance
    - Does NOT suppress errors
    - Does NOT implement recovery

Position in Architecture:
    WadhGeometry (PR-L5A)
    └── WadhResidual ← THIS MODULE
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class WadhResidualKind(Enum):
    """
    Categories of residuals in Wadh processing.

    Critical Law: All residuals must be preserved and tracked.
    """

    # Source residuals
    UNKNOWN_WADH_SOURCE = "unknown_wadh_source"
    INSUFFICIENT_SOURCE_EVIDENCE = "insufficient_source_evidence"
    REASON_ALONE_INSUFFICIENT = "reason_alone_insufficient"

    # Transmission residuals
    UNKNOWN_TRANSMISSION_MODE = "unknown_transmission_mode"
    UNVERIFIED_TRANSMISSION = "unverified_transmission"
    INDIRECT_TRANSMISSION_ONLY = "indirect_transmission_only"

    # Scope residuals
    UNKNOWN_WADH_SCOPE = "unknown_wadh_scope"
    SCOPE_BOUNDARY_VIOLATION = "scope_boundary_violation"

    # Original Wadh residuals
    ORIGINAL_WADH_UNOBSERVED = "original_wadh_unobserved"
    WADH_RECONSTRUCTION_UNCERTAIN = "wadh_reconstruction_uncertain"

    # Binding preservation residuals
    BINDING_TRACE_LOST = "binding_trace_lost"
    BINDING_EVIDENCE_INCOMPLETE = "binding_evidence_incomplete"

    # Semantic drift residuals
    PREMATURE_SEMANTIC_CLAIM = "premature_semantic_claim"
    EXTERNAL_MEANING_INJECTION = "external_meaning_injection"


@dataclass(frozen=True)
class WadhResidual:
    """
    A residual from Wadh processing.

    Residuals represent unresolved aspects, uncertainties, or
    constraints that must be preserved and tracked.

    Critical Properties:
        - kind: Residual category
        - description: Residual details
        - severity: Impact level
        - is_blocker: Whether residual blocks processing

    Critical Laws:
        - All residuals preserved (not discarded)
        - Blockers prevent downstream processing
        - Residuals accumulate through pipeline
        - No silent failures
    """

    kind: WadhResidualKind
    description: str
    severity: str = "medium"  # "low", "medium", "high", "blocker"

    @property
    def is_blocker(self) -> bool:
        """Check if this residual blocks Wadh processing."""
        return self.severity == "blocker"

    @property
    def is_warning(self) -> bool:
        """Check if this residual is warning-level."""
        return self.severity in {"low", "medium"}

    @property
    def is_critical(self) -> bool:
        """Check if this residual is critical."""
        return self.severity in {"high", "blocker"}

    def __str__(self) -> str:
        return f"[{self.kind.value}] {self.description} (severity={self.severity})"

    def __repr__(self) -> str:
        return f"WadhResidual(kind={self.kind.value}, severity={self.severity})"


# Factory functions for common residuals

def make_unknown_source_residual(description: str = "") -> WadhResidual:
    """
    Create residual for unknown Wadh source.

    Critical Law: Unknown source becomes blocker residual.
    """
    return WadhResidual(
        kind=WadhResidualKind.UNKNOWN_WADH_SOURCE,
        description=description or "Unknown Wadh source (blocker)",
        severity="blocker",
    )


def make_unknown_transmission_residual(description: str = "") -> WadhResidual:
    """
    Create residual for unknown transmission mode.

    Critical Law: Unknown transmission mode becomes blocker residual.
    """
    return WadhResidual(
        kind=WadhResidualKind.UNKNOWN_TRANSMISSION_MODE,
        description=description or "Unknown transmission mode (blocker)",
        severity="blocker",
    )


def make_unknown_scope_residual(description: str = "") -> WadhResidual:
    """
    Create residual for unknown Wadh scope.

    Critical Law: Unknown scope becomes blocker residual.
    """
    return WadhResidual(
        kind=WadhResidualKind.UNKNOWN_WADH_SCOPE,
        description=description or "Unknown Wadh scope (blocker)",
        severity="blocker",
    )


def make_reason_alone_residual(description: str = "") -> WadhResidual:
    """
    Create residual for reason-alone insufficiency.

    Critical Law: Reason alone cannot certify Arabic Wadh.
    """
    return WadhResidual(
        kind=WadhResidualKind.REASON_ALONE_INSUFFICIENT,
        description=description or "Reason alone insufficient for Arabic Wadh (requires transmission)",
        severity="blocker",
    )


def make_original_wadh_unobserved_residual(description: str = "") -> WadhResidual:
    """
    Create residual for unobserved original Wadh.

    Critical Law: Original Wadh unobserved becomes residual unless directly attested.
    """
    return WadhResidual(
        kind=WadhResidualKind.ORIGINAL_WADH_UNOBSERVED,
        description=description or "Original Wadh unobserved (reconstruction uncertain)",
        severity="high",
    )


def make_binding_trace_lost_residual(description: str = "") -> WadhResidual:
    """Create residual for lost binding trace."""
    return WadhResidual(
        kind=WadhResidualKind.BINDING_TRACE_LOST,
        description=description or "Binding trace lost (lineage broken)",
        severity="blocker",
    )


def make_external_meaning_injection_residual(description: str = "") -> WadhResidual:
    """
    Create residual for external meaning injection attempt.

    Critical Law: WadhClaim does NOT create external meaning.
    """
    return WadhResidual(
        kind=WadhResidualKind.EXTERNAL_MEANING_INJECTION,
        description=description or "External meaning injection attempt (blocker)",
        severity="blocker",
    )
