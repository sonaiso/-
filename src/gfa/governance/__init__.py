"""GFA Governance: Status Gate and False Claim Prevention.

This module implements constitutional safeguards to prevent false completion claims
and ensure honest status declaration across the project.

Core Principle:
    لا ادعاء بالإنجاز بلا برهان تنفيذي.
    "No completion claim without executable proof."

Architecture:
    - Rank: Unified epistemic rank enum (ZERO, BLOCKED, CANDIDATE, ZANNI, LICENSED, CERTIFIED)
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

    >>> from gfa.governance import Rank
    >>> result.rank = Rank.CANDIDATE  # ✅ Correct
    >>> result.rank = "CANDIDATE"     # ❌ FORBIDDEN
"""

from .rank import Rank, rank_from_string, rank_to_string

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
    # Rank system
    "Rank",
    "rank_from_string",
    "rank_to_string",

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
