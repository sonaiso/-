"""
MutabaqahResidual - بقايا المطابقة

Critical Law:
    البقايا تحفظ، لا تُهمل
    Residuals are preserved, NOT ignored.

MutabaqahResidual represents unresolved aspects in Mutabaqah processing.

What MutabaqahResidual Does:
    - Classifies residual types
    - Preserves unresolved issues
    - Guards against silent failures
    - Blocks when necessary

What MutabaqahResidual Does NOT Do:
    - Does NOT create meaning
    - Does NOT bypass governance
    - Does NOT suppress errors
    - Does NOT implement recovery

Position in Architecture:
    WadhGate (PR-L5B)
    └── MutabaqahGate (PR-L6A)
        └── MutabaqahResidual ← THIS MODULE
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MutabaqahResidualKind(Enum):
    """
    Categories of residuals in Mutabaqah processing.

    Critical Law: All residuals must be preserved and tracked.
    """

    # WadhClaim residuals
    WADH_CLAIM_NOT_ADMITTED = "wadh_claim_not_admitted"
    WADH_CLAIM_MISSING = "wadh_claim_missing"
    WADH_EVIDENCE_INSUFFICIENT = "wadh_evidence_insufficient"

    # MawduLah structure residuals
    MAWDU_LAH_STRUCTURE_MISSING = "mawdu_lah_structure_missing"
    MAWDU_LAH_WHOLE_UNAVAILABLE = "mawdu_lah_whole_unavailable"
    MAWDU_LAH_WHOLE_AMBIGUOUS = "mawdu_lah_whole_ambiguous"
    MAWDU_LAH_STRUCTURE_INVALID = "mawdu_lah_structure_invalid"

    # Semantic ambiguity residuals
    POLYSEMY_POSSIBLE = "polysemy_possible"
    HOMONYMY_POSSIBLE = "homonymy_possible"
    MULTIPLE_WADH_CONVENTIONS = "multiple_wadh_conventions"

    # Partial usage residuals
    PARTIAL_USAGE_DETECTED = "partial_usage_detected"
    TADAMMUN_POSSIBLE = "tadammun_possible"
    ILTIZAM_POSSIBLE = "iltizam_possible"

    # Scope residuals
    SCOPE_UNDETERMINED = "scope_undetermined"
    SCOPE_BOUNDARY_UNCLEAR = "scope_boundary_unclear"

    # Trace preservation residuals
    WADH_TRACE_LOST = "wadh_trace_lost"
    BINDING_TRACE_LOST = "binding_trace_lost"

    # Semantic inflation residuals (blockers)
    EXTERNAL_MEANING_INJECTION_ATTEMPT = "external_meaning_injection_attempt"
    HUKM_INJECTION_ATTEMPT = "hukm_injection_attempt"
    PREDICATE_RANK_INFLATION_ATTEMPT = "predicate_rank_inflation_attempt"
    TADAMMUN_CREATED = "tadammun_created"
    ILTIZAM_CREATED = "iltizam_created"
    HAQIQAH_MAJAZ_CLASSIFIED = "haqiqah_majaz_classified"
    NAQL_CLASSIFIED = "naql_classified"
    IFADAH_CREATED = "ifadah_created"


@dataclass(frozen=True)
class MutabaqahResidual:
    """
    A residual from Mutabaqah processing.

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

    kind: MutabaqahResidualKind
    description: str
    severity: str = "medium"  # "low", "medium", "high", "blocker"

    @property
    def is_blocker(self) -> bool:
        """Check if this residual blocks Mutabaqah processing."""
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
        return f"MutabaqahResidual(kind={self.kind.value}, severity={self.severity})"


# Factory functions for common residuals

def make_wadh_claim_not_admitted_residual(description: str = "") -> MutabaqahResidual:
    """
    Create residual for non-admitted WadhClaim.

    Critical Law: WadhClaim must be admitted before Mutabaqah.
    """
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.WADH_CLAIM_NOT_ADMITTED,
        description=description or "WadhClaim not admitted (blocker)",
        severity="blocker",
    )


def make_mawdu_lah_whole_unavailable_residual(description: str = "") -> MutabaqahResidual:
    """
    Create residual for unavailable MawduLah whole.

    Critical Law: Mutabaqah requires whole of MawduLah.
    """
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.MAWDU_LAH_WHOLE_UNAVAILABLE,
        description=description or "MawduLah whole unavailable (blocker)",
        severity="blocker",
    )


def make_polysemy_possible_residual(description: str = "") -> MutabaqahResidual:
    """
    Create residual for possible polysemy.

    Critical Law: Polysemy possibility becomes residual, not exception.
    """
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.POLYSEMY_POSSIBLE,
        description=description or "Polysemy possible (multiple related meanings)",
        severity="high",
    )


def make_homonymy_possible_residual(description: str = "") -> MutabaqahResidual:
    """
    Create residual for possible homonymy.

    Critical Law: Homonymy possibility becomes residual, not exception.
    """
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.HOMONYMY_POSSIBLE,
        description=description or "Homonymy possible (multiple unrelated meanings)",
        severity="high",
    )


def make_partial_usage_detected_residual(description: str = "") -> MutabaqahResidual:
    """
    Create residual for partial usage detection.

    Critical Law: Partial usage blocks or residualizes Mutabaqah.
    """
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.PARTIAL_USAGE_DETECTED,
        description=description or "Partial usage detected (may indicate Tadammun)",
        severity="blocker",
    )


def make_external_meaning_injection_residual(description: str = "") -> MutabaqahResidual:
    """
    Create residual for external meaning injection attempt.

    Critical Law: Mutabaqah does NOT create external meaning.
    """
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.EXTERNAL_MEANING_INJECTION_ATTEMPT,
        description=description or "External meaning injection attempt (blocker)",
        severity="blocker",
    )


def make_hukm_injection_residual(description: str = "") -> MutabaqahResidual:
    """
    Create residual for HUKM injection attempt.

    Critical Law: Mutabaqah does NOT issue HUKM.
    """
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.HUKM_INJECTION_ATTEMPT,
        description=description or "HUKM injection attempt (blocker)",
        severity="blocker",
    )


def make_tadammun_created_residual(description: str = "") -> MutabaqahResidual:
    """
    Create residual for Tadammun creation attempt.

    Critical Law: Mutabaqah does NOT create Tadammun.
    """
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.TADAMMUN_CREATED,
        description=description or "Tadammun created (blocker)",
        severity="blocker",
    )


def make_iltizam_created_residual(description: str = "") -> MutabaqahResidual:
    """
    Create residual for Iltizam creation attempt.

    Critical Law: Mutabaqah does NOT create Iltizam.
    """
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.ILTIZAM_CREATED,
        description=description or "Iltizam created (blocker)",
        severity="blocker",
    )


def make_haqiqah_majaz_classified_residual(description: str = "") -> MutabaqahResidual:
    """
    Create residual for Haqiqah/Majaz classification attempt.

    Critical Law: Mutabaqah does NOT classify Haqiqah/Majaz/Naql.
    """
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.HAQIQAH_MAJAZ_CLASSIFIED,
        description=description or "Haqiqah/Majaz classification attempt (blocker)",
        severity="blocker",
    )


def make_wadh_trace_lost_residual(description: str = "") -> MutabaqahResidual:
    """Create residual for lost Wadh trace."""
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.WADH_TRACE_LOST,
        description=description or "Wadh trace lost (lineage broken)",
        severity="blocker",
    )


def make_binding_trace_lost_residual(description: str = "") -> MutabaqahResidual:
    """Create residual for lost binding trace."""
    return MutabaqahResidual(
        kind=MutabaqahResidualKind.BINDING_TRACE_LOST,
        description=description or "Binding trace lost (lineage broken)",
        severity="blocker",
    )
