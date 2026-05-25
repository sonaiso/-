"""
U₃ Role Operations (عمليات الأدوار الوظيفية)

Implements Ω₃ = Role operation algebra

Operations:
    - assign_candidate_role: S → RoleCandidate
    - merge_span: Sᵢ + Sᵢ₊₁ → RoleSpan
    - split_span: RoleSpan → RoleSpan₁ + RoleSpan₂
    - attach_to_host: RoleSpan + Host → AttachedRole
    - promote_role: candidate → hypothesis → certificate
    - demote_role: certificate → hypothesis → candidate
    - block_role: Role → blocked
    - discharge_residual: Remove resolved residual
    - preserve_competitors: Maintain competing role candidates

PR: U3-LAYER
Created: 2026-05-25
"""

from dataclasses import dataclass, replace
from typing import List, Optional, Dict, Any
from enum import Enum

from dal_core.u3_functional_roles import (
    RoleSpan,
    RoleSet,
    FunctionalRole,
    RoleSort,
    RoleRank,
    RoleResidualCode,
    ClosedClassRole,
    PronounRole,
    RootRole,
    DerivationalRole,
)
from dal_core.syllables import Syllable
from dal_core.residuals import Residual, make_warning, make_blocker, ResidualType


# ============================================================================
# Operation Result Types
# ============================================================================

class OperationStatus(Enum):
    """Status of a role operation."""
    SUCCESS = "success"
    BLOCKED = "blocked"
    WARNING = "warning"
    FAILED = "failed"


@dataclass
class OperationResult:
    """
    Result of a role operation.

    Attributes:
        status: Operation status
        output: Resulting role span(s)
        residuals: New residuals from operation
        evidence: Evidence supporting operation
        message: Human-readable message
    """
    status: OperationStatus
    output: Optional[RoleSpan] = None
    outputs: List[RoleSpan] = None  # For operations producing multiple spans
    residuals: List[Residual] = None
    evidence: Dict[str, Any] = None
    message: str = ""

    def __post_init__(self):
        if self.residuals is None:
            self.residuals = []
        if self.evidence is None:
            self.evidence = {}
        if self.outputs is None:
            self.outputs = []

    def is_success(self) -> bool:
        return self.status == OperationStatus.SUCCESS

    def is_blocked(self) -> bool:
        return self.status == OperationStatus.BLOCKED


# ============================================================================
# Operation 1: assign_candidate_role
# ============================================================================

def assign_candidate_role(
    role_span: RoleSpan,
    role: FunctionalRole,
    evidence: Optional[Dict[str, Any]] = None
) -> OperationResult:
    """
    Assign a candidate role to a role span.

    This is the most basic operation: adding a role hypothesis to the candidate set.

    Args:
        role_span: Target role span
        role: Role to assign
        evidence: Evidence supporting assignment

    Returns:
        OperationResult with updated role span
    """
    if evidence is None:
        evidence = {}

    # Check if span is blocked
    if role_span.has_blocker():
        return OperationResult(
            status=OperationStatus.BLOCKED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                f"Cannot assign role to blocked span {role_span.span_id}",
                location="assign_candidate_role"
            )],
            message="Span has blocking residuals"
        )

    # Create updated role span with new role
    updated_roles = RoleSet(roles=role_span.candidate_roles.roles.copy())
    updated_roles.add_role(role)

    updated_span = replace(
        role_span,
        candidate_roles=updated_roles,
        evidence=role_span.evidence + [evidence],
        rank=RoleRank.ROLE_CANDIDATE.value
    )

    # Add residual if this creates ambiguity
    residuals = []
    if len(updated_roles) > 1:
        residuals.append(make_warning(
            ResidualType.AMBIGUOUS_PATTERN,
            f"Role ambiguity: {len(updated_roles)} competing roles",
            location=f"span {role_span.span_id}"
        ))

    return OperationResult(
        status=OperationStatus.SUCCESS,
        output=updated_span,
        residuals=residuals,
        evidence=evidence,
        message=f"Assigned role {role.role} to span"
    )


# ============================================================================
# Operation 2: merge_span
# ============================================================================

def merge_span(
    span1: RoleSpan,
    span2: RoleSpan,
    merged_role: Optional[FunctionalRole] = None,
    evidence: Optional[Dict[str, Any]] = None
) -> OperationResult:
    """
    Merge two adjacent role spans into a single span.

    Use case: Multi-syllable roles like إنّ، استفعل prefixes

    Args:
        span1: First span
        span2: Second span (must be adjacent)
        merged_role: Optional role for merged span
        evidence: Evidence supporting merge

    Returns:
        OperationResult with merged span
    """
    if evidence is None:
        evidence = {}

    # Check adjacency
    if span1.syllable_indices and span2.syllable_indices:
        if span1.syllable_indices[-1] + 1 != span2.syllable_indices[0]:
            return OperationResult(
                status=OperationStatus.FAILED,
                residuals=[make_blocker(
                    ResidualType.INVALID_SYLLABLE,
                    "Spans are not adjacent",
                    location="merge_span"
                )],
                message="Cannot merge non-adjacent spans"
            )

    # Check for blockers
    if span1.has_blocker() or span2.has_blocker():
        return OperationResult(
            status=OperationStatus.BLOCKED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                "Cannot merge spans with blockers",
                location="merge_span"
            )],
            message="One or both spans have blocking residuals"
        )

    # Merge syllables and indices
    merged_syllables = span1.syllables + span2.syllables
    merged_indices = tuple(list(span1.syllable_indices) + list(span2.syllable_indices))

    # Combine roles
    merged_role_set = RoleSet(
        roles=span1.candidate_roles.roles + span2.candidate_roles.roles
    )
    if merged_role:
        merged_role_set.add_role(merged_role)

    # Create merged span
    from dal_core.u3_functional_roles import create_role_span
    merged = create_role_span(
        syllables=merged_syllables,
        indices=merged_indices,
        position=span1.position  # Inherit position from first span
    )
    merged = replace(
        merged,
        candidate_roles=merged_role_set,
        evidence=span1.evidence + span2.evidence + [evidence],
        trace_u2=span1.trace_u2 + span2.trace_u2,
        residuals=span1.residuals + span2.residuals,
        rank=RoleRank.ROLE_CANDIDATE.value
    )

    return OperationResult(
        status=OperationStatus.SUCCESS,
        output=merged,
        evidence=evidence,
        message=f"Merged spans into {merged.span_id}"
    )


# ============================================================================
# Operation 3: split_span
# ============================================================================

def split_span(
    span: RoleSpan,
    split_index: int,
    evidence: Optional[Dict[str, Any]] = None
) -> OperationResult:
    """
    Split a role span into two spans at the given syllable index.

    Args:
        span: Span to split
        split_index: Index to split at (relative to span syllables)
        evidence: Evidence supporting split

    Returns:
        OperationResult with two output spans
    """
    if evidence is None:
        evidence = {}

    # Validate split index
    if not (0 < split_index < len(span.syllables)):
        return OperationResult(
            status=OperationStatus.FAILED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                f"Invalid split index {split_index}",
                location="split_span"
            )],
            message="Split index out of bounds"
        )

    # Check for blockers
    if span.has_blocker():
        return OperationResult(
            status=OperationStatus.BLOCKED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                "Cannot split span with blockers",
                location="split_span"
            )],
            message="Span has blocking residuals"
        )

    # Split syllables
    syllables1 = span.syllables[:split_index]
    syllables2 = span.syllables[split_index:]

    # Split indices
    indices1 = span.syllable_indices[:split_index]
    indices2 = span.syllable_indices[split_index:]

    # Create two new spans
    from dal_core.u3_functional_roles import create_role_span
    span1 = create_role_span(syllables=syllables1, indices=indices1, position="initial")
    span2 = create_role_span(syllables=syllables2, indices=indices2, position="final")

    # Inherit roles to both (they remain competitors)
    span1 = replace(span1, candidate_roles=span.candidate_roles)
    span2 = replace(span2, candidate_roles=span.candidate_roles)

    return OperationResult(
        status=OperationStatus.SUCCESS,
        outputs=[span1, span2],
        evidence=evidence,
        message=f"Split span at index {split_index}"
    )


# ============================================================================
# Operation 4: attach_to_host
# ============================================================================

def attach_to_host(
    role_span: RoleSpan,
    host_info: Dict[str, Any],
    evidence: Optional[Dict[str, Any]] = None
) -> OperationResult:
    """
    Attach role span to a host element (word, particle, etc.)

    Use case: Attached pronouns, affixes, particles

    Args:
        role_span: Span to attach
        host_info: Information about host element
        evidence: Evidence supporting attachment

    Returns:
        OperationResult with updated span
    """
    if evidence is None:
        evidence = {}

    # Check for blockers
    if role_span.has_blocker():
        return OperationResult(
            status=OperationStatus.BLOCKED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                "Cannot attach span with blockers",
                location="attach_to_host"
            )],
            message="Span has blocking residuals"
        )

    # Update host relation
    updated_span = replace(
        role_span,
        host_relation=host_info,
        evidence=role_span.evidence + [evidence]
    )

    return OperationResult(
        status=OperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message="Attached span to host"
    )


# ============================================================================
# Operation 5: promote_role
# ============================================================================

def promote_role(
    role_span: RoleSpan,
    target_role: FunctionalRole,
    evidence: Dict[str, Any]
) -> OperationResult:
    """
    Promote a specific role in the candidate set.

    Progression: candidate → hypothesis → strong_hypothesis → certificate

    Requires evidence to justify promotion.

    Args:
        role_span: Span containing role
        target_role: Role to promote
        evidence: Evidence justifying promotion

    Returns:
        OperationResult with promoted role
    """
    # Check if target role exists in candidate set
    if target_role not in role_span.candidate_roles.roles:
        return OperationResult(
            status=OperationStatus.FAILED,
            message=f"Role {target_role.role} not in candidate set"
        )

    # Check current rank
    current_rank = RoleRank(role_span.rank)

    # Determine new rank
    rank_progression = {
        RoleRank.ROLE_ZERO: RoleRank.ROLE_CANDIDATE,
        RoleRank.ROLE_CANDIDATE: RoleRank.ROLE_HYPOTHESIS,
        RoleRank.ROLE_HYPOTHESIS: RoleRank.ROLE_STRONG_HYPOTHESIS,
        RoleRank.ROLE_STRONG_HYPOTHESIS: RoleRank.ROLE_CERTIFICATE,
    }

    if current_rank == RoleRank.ROLE_CERTIFICATE:
        return OperationResult(
            status=OperationStatus.SUCCESS,
            output=role_span,
            message="Already at certificate rank"
        )

    new_rank = rank_progression.get(current_rank, RoleRank.ROLE_CANDIDATE)

    # Update span
    updated_span = replace(
        role_span,
        rank=new_rank.value,
        evidence=role_span.evidence + [evidence]
    )

    return OperationResult(
        status=OperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message=f"Promoted role to {new_rank.value}"
    )


# ============================================================================
# Operation 6: demote_role
# ============================================================================

def demote_role(
    role_span: RoleSpan,
    reason: str,
    evidence: Optional[Dict[str, Any]] = None
) -> OperationResult:
    """
    Demote a role due to conflicting evidence.

    Demotion: certificate → strong_hypothesis → hypothesis → candidate → blocked

    Args:
        role_span: Span to demote
        reason: Reason for demotion
        evidence: Evidence supporting demotion

    Returns:
        OperationResult with demoted role
    """
    if evidence is None:
        evidence = {"reason": reason}

    current_rank = RoleRank(role_span.rank)

    # Rank demotion
    rank_demotion = {
        RoleRank.ROLE_CERTIFICATE: RoleRank.ROLE_STRONG_HYPOTHESIS,
        RoleRank.ROLE_STRONG_HYPOTHESIS: RoleRank.ROLE_HYPOTHESIS,
        RoleRank.ROLE_HYPOTHESIS: RoleRank.ROLE_CANDIDATE,
        RoleRank.ROLE_CANDIDATE: RoleRank.ROLE_BLOCKED,
    }

    new_rank = rank_demotion.get(current_rank, RoleRank.ROLE_BLOCKED)

    # Add residual explaining demotion
    residual = make_warning(
        ResidualType.AMBIGUOUS_PATTERN,
        f"Role demoted: {reason}",
        location=f"span {role_span.span_id}"
    )

    updated_span = replace(
        role_span,
        rank=new_rank.value,
        residuals=role_span.residuals + [residual],
        evidence=role_span.evidence + [evidence]
    )

    return OperationResult(
        status=OperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message=f"Demoted role to {new_rank.value}: {reason}"
    )


# ============================================================================
# Operation 7: block_role
# ============================================================================

def block_role(
    role_span: RoleSpan,
    role_to_block: FunctionalRole,
    reason: str,
    evidence: Dict[str, Any]
) -> OperationResult:
    """
    Block a specific role from the candidate set.

    This removes the role as a viable candidate.

    Args:
        role_span: Span containing role
        role_to_block: Role to block
        reason: Reason for blocking
        evidence: Evidence supporting block

    Returns:
        OperationResult with role blocked
    """
    # Remove role from candidate set
    updated_roles = RoleSet(
        roles=[r for r in role_span.candidate_roles.roles if r != role_to_block]
    )

    # Add residual documenting the block
    residual = make_warning(
        ResidualType.AMBIGUOUS_PATTERN,
        f"Blocked role {role_to_block.role}: {reason}",
        location=f"span {role_span.span_id}"
    )

    updated_span = replace(
        role_span,
        candidate_roles=updated_roles,
        residuals=role_span.residuals + [residual],
        evidence=role_span.evidence + [evidence]
    )

    return OperationResult(
        status=OperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message=f"Blocked role {role_to_block.role}"
    )


# ============================================================================
# Operation 8: discharge_residual
# ============================================================================

def discharge_residual(
    role_span: RoleSpan,
    residual_to_discharge: Residual,
    evidence: Dict[str, Any]
) -> OperationResult:
    """
    Discharge (remove) a resolved residual.

    Only non-blocker residuals can be discharged.
    Blockers require evidence proving they're resolved.

    Args:
        role_span: Span with residual
        residual_to_discharge: Residual to remove
        evidence: Evidence proving resolution

    Returns:
        OperationResult with residual removed
    """
    if residual_to_discharge.is_blocker() and not evidence.get("blocker_resolved", False):
        return OperationResult(
            status=OperationStatus.BLOCKED,
            message="Cannot discharge blocker without explicit resolution evidence"
        )

    # Remove residual
    updated_residuals = [r for r in role_span.residuals if r != residual_to_discharge]

    updated_span = replace(
        role_span,
        residuals=updated_residuals,
        evidence=role_span.evidence + [evidence]
    )

    return OperationResult(
        status=OperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message="Discharged residual"
    )


# ============================================================================
# Operation 9: preserve_competitors
# ============================================================================

def preserve_competitors(
    role_span: RoleSpan,
    evidence: Dict[str, Any]
) -> OperationResult:
    """
    Explicitly preserve all competing roles.

    This operation marks that competitor preservation is intentional,
    not an oversight.

    Args:
        role_span: Span with competitors
        evidence: Evidence supporting preservation

    Returns:
        OperationResult confirming preservation
    """
    updated_span = replace(
        role_span,
        evidence=role_span.evidence + [{
            "operation": "preserve_competitors",
            "competitor_count": len(role_span.candidate_roles),
            **evidence
        }]
    )

    return OperationResult(
        status=OperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message=f"Preserved {len(role_span.candidate_roles)} competing roles"
    )
