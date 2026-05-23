"""Residual Taxonomy for Status and Provisional Components.

Defines residuals for components that operate on provisional foundations.

Core Law:
    كل مؤقت يجب أن يعلن حالته.
    "Every provisional must declare its status."
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from fvafk.algebra.core import Residual


class StatusResidualKind(Enum):
    """Kinds of status-related residuals.

    Attributes:
        PROVISIONAL_FOUNDATION: Component built on provisional foundation
        CPB_DEPENDENCY: Depends on CPB extraction (not yet done)
        GENERALITY_UNPROVEN: Generality not computationally proven
        SPECIALIZED_ONLY: Works only in specialized domain
        PATTERN_SPECIFIC: Works only on specific patterns
        INCOMPLETE_ARCHITECTURE: Architecture not complete
    """

    PROVISIONAL_FOUNDATION = "provisional_foundation"
    CPB_DEPENDENCY = "cpb_dependency"
    GENERALITY_UNPROVEN = "generality_unproven"
    SPECIALIZED_ONLY = "specialized_only"
    PATTERN_SPECIFIC = "pattern_specific"
    INCOMPLETE_ARCHITECTURE = "incomplete_architecture"


@dataclass(frozen=True)
class StatusResidual:
    """Status residual for provisional components.

    Attributes:
        kind: Kind of status residual
        description: Human-readable description
        blocker: Whether this blocks higher-level operations
        affected_claims: Claims that cannot be made due to this residual
    """

    kind: StatusResidualKind
    description: str
    blocker: bool = False
    affected_claims: tuple[str, ...] = ()

    def to_residual(self) -> Residual:
        """Convert to standard Residual.

        Returns:
            Residual instance
        """
        return Residual(
            kind=f"status.{self.kind.value}",
            description=self.description,
        )


def make_provisional_residual(component_name: str) -> StatusResidual:
    """Create residual for provisional specialized algebra.

    Args:
        component_name: Name of the component

    Returns:
        StatusResidual declaring provisional status
    """
    return StatusResidual(
        kind=StatusResidualKind.PROVISIONAL_FOUNDATION,
        description=(
            f"{component_name} operates on provisional NeutralBinding; "
            "not generated from General Algebra; "
            "status: PROVISIONAL_SPECIALIZED_ALGEBRA"
        ),
        blocker=False,
        affected_claims=(
            "general algebra completion",
            "cross-domain generality",
            "hukm issuance",
        ),
    )


def make_cpb_dependency_residual(component_name: str) -> StatusResidual:
    """Create residual for CPB dependency.

    Args:
        component_name: Name of the component

    Returns:
        StatusResidual declaring CPB dependency
    """
    return StatusResidual(
        kind=StatusResidualKind.CPB_DEPENDENCY,
        description=(
            f"{component_name} depends on CPB extraction; "
            "CPB not extracted yet; "
            "binding policy not proven minimal/stable/safe"
        ),
        blocker=False,
        affected_claims=(
            "general binding proven",
            "cpb extraction complete",
            "binding optimality",
        ),
    )


def make_generality_unproven_residual(component_name: str) -> StatusResidual:
    """Create residual for unproven generality.

    Args:
        component_name: Name of the component

    Returns:
        StatusResidual declaring unproven generality
    """
    return StatusResidual(
        kind=StatusResidualKind.GENERALITY_UNPROVEN,
        description=(
            f"{component_name} generality not proven; "
            "no 3-domain proof; "
            "may not work outside tested domain"
        ),
        blocker=False,
        affected_claims=(
            "general algebra proven",
            "works across all domains",
            "domain-independent",
        ),
    )


def make_specialized_only_residual(
    component_name: str, domain: str
) -> StatusResidual:
    """Create residual for specialized-only component.

    Args:
        component_name: Name of the component
        domain: Domain it works in

    Returns:
        StatusResidual declaring specialization
    """
    return StatusResidual(
        kind=StatusResidualKind.SPECIALIZED_ONLY,
        description=(
            f"{component_name} works only in {domain} domain; "
            "not proven for other domains; "
            "domain-specific implementation"
        ),
        blocker=False,
        affected_claims=(
            "general purpose",
            "domain independent",
            "universal applicability",
        ),
    )


def make_pattern_specific_residual(
    component_name: str, pattern: str
) -> StatusResidual:
    """Create residual for pattern-specific component.

    Args:
        component_name: Name of the component
        pattern: Pattern it works on

    Returns:
        StatusResidual declaring pattern specificity
    """
    return StatusResidual(
        kind=StatusResidualKind.PATTERN_SPECIFIC,
        description=(
            f"{component_name} tested only on {pattern} pattern; "
            "not verified for general patterns; "
            "prototype implementation"
        ),
        blocker=False,
        affected_claims=(
            "general learning",
            "pattern independent",
            "universal pattern handling",
        ),
    )


__all__ = [
    "StatusResidualKind",
    "StatusResidual",
    "make_provisional_residual",
    "make_cpb_dependency_residual",
    "make_generality_unproven_residual",
    "make_specialized_only_residual",
    "make_pattern_specific_residual",
]
