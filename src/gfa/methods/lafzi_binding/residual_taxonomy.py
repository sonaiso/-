"""
BindingResidual Taxonomy - تصنيف بقايا الربط

All failures in Dāl/Madlūl binding become typed residuals.

Critical Law:
    كل فشل يرجع بقايا محكومة، لا استثناءات عارية
    All failures return governed residuals, not bare exceptions.

BindingResidualKind Types:
    - MISSING_DAL_CANDIDATE: No DālCandidate provided
    - MISSING_MADLUL_LAFZI_CANDIDATE: No MadlulLafziCandidate provided
    - MISSING_LAFZI_REGISTRATION: LafziMadlul registration failed
    - MISSING_LAFZI_DALALI_STYLE: StyleSpec is not LAFZI_DALALI
    - MISSING_NEUTRAL_BINDING: NeutralBinding not provided
    - MISSING_PRIOR_INFORMATION: PriorInformation not provided
    - DOMAIN_MISMATCH: Dāl and Madlūl from different domains
    - UNKNOWN_BINDING_BASIS: BindingBasis is UNKNOWN_BASIS
    - TRACE_ID_MISMATCH: trace_id mismatch between Dāl and Madlūl
    - INVALID_DAL_CANDIDATE: DālCandidate is invalid
    - INVALID_MADLUL_CANDIDATE: MadlulLafziCandidate is invalid
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class BindingResidualKind(Enum):
    """Types of binding residuals."""

    MISSING_DAL_CANDIDATE = auto()
    MISSING_MADLUL_LAFZI_CANDIDATE = auto()
    MISSING_LAFZI_REGISTRATION = auto()
    MISSING_LAFZI_DALALI_STYLE = auto()
    MISSING_NEUTRAL_BINDING = auto()
    MISSING_PRIOR_INFORMATION = auto()
    DOMAIN_MISMATCH = auto()
    UNKNOWN_BINDING_BASIS = auto()
    TRACE_ID_MISMATCH = auto()
    INVALID_DAL_CANDIDATE = auto()
    INVALID_MADLUL_CANDIDATE = auto()

    def __str__(self) -> str:
        return self.name


@dataclass(frozen=True)
class BindingResidual:
    """
    Typed residual from Dāl/Madlūl binding.

    All failures become residuals, not exceptions.

    Properties:
        kind: Type of residual
        description: Human-readable description
        severity: "blocker", "warning", or "info"
        source: Optional source identifier
    """

    kind: BindingResidualKind
    description: str
    severity: str = "blocker"
    source: Optional[str] = None

    def __post_init__(self):
        """Validate residual."""
        if self.severity not in ("blocker", "warning", "info"):
            raise ValueError(f"Invalid severity: {self.severity}")

    @property
    def is_blocker(self) -> bool:
        """Check if residual is a blocker."""
        return self.severity == "blocker"

    def __str__(self) -> str:
        source_str = f" [{self.source}]" if self.source else ""
        return f"{self.kind.name} ({self.severity}): {self.description}{source_str}"


# Factory functions for common residuals

def make_missing_dal_candidate_residual(description: str = "") -> BindingResidual:
    """Create residual for missing DālCandidate."""
    desc = description or "DālCandidate is required for binding"
    return BindingResidual(
        kind=BindingResidualKind.MISSING_DAL_CANDIDATE,
        description=desc,
        severity="blocker",
    )


def make_missing_madlul_lafzi_candidate_residual(description: str = "") -> BindingResidual:
    """Create residual for missing MadlulLafziCandidate."""
    desc = description or "MadlulLafziCandidate is required for binding"
    return BindingResidual(
        kind=BindingResidualKind.MISSING_MADLUL_LAFZI_CANDIDATE,
        description=desc,
        severity="blocker",
    )


def make_missing_lafzi_registration_residual(description: str = "") -> BindingResidual:
    """Create residual for missing LafziMadlul registration."""
    desc = description or "Successful LafziMadlul registration is required for binding"
    return BindingResidual(
        kind=BindingResidualKind.MISSING_LAFZI_REGISTRATION,
        description=desc,
        severity="blocker",
    )


def make_missing_lafzi_dalali_style_residual(description: str = "") -> BindingResidual:
    """Create residual for missing LAFZI_DALALI StyleSpec."""
    desc = description or "StyleSpec(LAFZI_DALALI) is required for binding"
    return BindingResidual(
        kind=BindingResidualKind.MISSING_LAFZI_DALALI_STYLE,
        description=desc,
        severity="blocker",
    )


def make_missing_neutral_binding_residual(description: str = "") -> BindingResidual:
    """Create residual for missing NeutralBinding."""
    desc = description or "NeutralBinding is required for binding"
    return BindingResidual(
        kind=BindingResidualKind.MISSING_NEUTRAL_BINDING,
        description=desc,
        severity="blocker",
    )


def make_missing_prior_information_residual(description: str = "") -> BindingResidual:
    """Create residual for missing PriorInformation."""
    desc = description or "PriorInformation is required for binding"
    return BindingResidual(
        kind=BindingResidualKind.MISSING_PRIOR_INFORMATION,
        description=desc,
        severity="blocker",
    )


def make_domain_mismatch_residual(dal_domain: str, madlul_domain: str) -> BindingResidual:
    """Create residual for domain mismatch."""
    return BindingResidual(
        kind=BindingResidualKind.DOMAIN_MISMATCH,
        description=f"Dāl domain ({dal_domain}) does not match Madlūl domain ({madlul_domain})",
        severity="blocker",
    )


def make_unknown_binding_basis_residual(description: str = "") -> BindingResidual:
    """Create residual for unknown binding basis."""
    desc = description or "BindingBasis is UNKNOWN_BASIS"
    return BindingResidual(
        kind=BindingResidualKind.UNKNOWN_BINDING_BASIS,
        description=desc,
        severity="warning",  # Unknown basis is warning, not blocker
    )


def make_trace_id_mismatch_residual(dal_trace: str, madlul_trace: str) -> BindingResidual:
    """Create residual for trace_id mismatch."""
    return BindingResidual(
        kind=BindingResidualKind.TRACE_ID_MISMATCH,
        description=f"Dāl trace_id ({dal_trace}) does not match Madlūl trace_id ({madlul_trace})",
        severity="warning",  # Mismatch is warning, not blocker
    )


def make_invalid_dal_candidate_residual(reason: str) -> BindingResidual:
    """Create residual for invalid DālCandidate."""
    return BindingResidual(
        kind=BindingResidualKind.INVALID_DAL_CANDIDATE,
        description=f"DālCandidate is invalid: {reason}",
        severity="blocker",
    )


def make_invalid_madlul_candidate_residual(reason: str) -> BindingResidual:
    """Create residual for invalid MadlulLafziCandidate."""
    return BindingResidual(
        kind=BindingResidualKind.INVALID_MADLUL_CANDIDATE,
        description=f"MadlulLafziCandidate is invalid: {reason}",
        severity="blocker",
    )
