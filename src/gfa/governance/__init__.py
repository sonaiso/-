"""GFA Governance: Status Gate and False Claim Prevention.

This module implements constitutional safeguards to prevent false completion claims
and ensure honest status declaration across the project.

Core Principle:
    لا ادعاء بالإنجاز بلا برهان تنفيذي.
    "No completion claim without executable proof."

Architecture:
    - AlgebraStatus: Classification of algebra implementation status
    - ComponentStatus: Tracking of specific component implementation
    - StatusValidator: Runtime validation against false claims
    - Residual taxonomy for provisional components

Critical Law:
    Every specialized algebra component must declare:
    1. AlgebraStatus = PROVISIONAL_SPECIALIZED (if not general)
    2. Residual: "depends on CPB extraction"
    3. No claim of generality
    4. No Hukm issuance
    5. Trace preserved

Example:
    >>> from gfa.governance import AlgebraStatus, validate_project_status
    >>> status = validate_project_status()
    >>> status.gfa_status
    <AlgebraStatus.PROVISIONAL_SPECIALIZED>
    >>> status.cpb_proven
    False
"""

from .algebra_status import (
    AlgebraStatus,
    ComponentStatus,
    ProjectStatus,
    get_project_status,
)

from .status_validator import (
    StatusValidator,
    validate_project_status,
    validate_no_false_claims,
    GovernanceViolation,
)

from .residual_taxonomy import (
    StatusResidual,
    make_provisional_residual,
    make_cpb_dependency_residual,
    make_generality_unproven_residual,
)

__all__ = [
    # Status classification
    "AlgebraStatus",
    "ComponentStatus",
    "ProjectStatus",
    "get_project_status",

    # Validation
    "StatusValidator",
    "validate_project_status",
    "validate_no_false_claims",
    "GovernanceViolation",

    # Residuals
    "StatusResidual",
    "make_provisional_residual",
    "make_cpb_dependency_residual",
    "make_generality_unproven_residual",
]
