"""
U₄ Morpheme Operations (عمليات الوحدات الصرفية)

Implements Ω₄ = Morpheme operation algebra

Operations:
    - classify_morpheme: RoleSpan → MorphemeCandidate
    - merge_morphemes: M₁ + M₂ → MCompound
    - attach_affix: Affix + Host → AttachedMorpheme
    - promote_morpheme: candidate → hypothesis → certificate
    - demote_morpheme: certificate → hypothesis → candidate
    - block_morpheme: Morpheme → blocked
    - discharge_residual: Remove resolved residual
    - preserve_competitors: Maintain competing morpheme interpretations

PR: U4-LAYER
Created: 2026-05-25
"""

from dataclasses import dataclass, replace
from typing import List, Optional, Dict, Any
from enum import Enum
from uuid import uuid4

from dal_core.u4_morpheme_carrier import (
    MorphemeSpan,
    MorphemeCandidate,
    MorphemeIdentity,
    MorphemeSet,
    MorphemeSort,
    MorphemeRank,
    MorphemeResidualCode,
    ClosedClassType,
    AffixType,
    RootCandidateType,
    AttachmentMode,
    FeaturePotential,
)
from dal_core.u3_functional_roles import RoleSpan
from dal_core.residuals import Residual, make_warning, make_blocker, ResidualType


# ============================================================================
# Operation Result Types
# ============================================================================

class MorphemeOperationStatus(Enum):
    """Status of a morpheme operation."""
    SUCCESS = "success"
    BLOCKED = "blocked"
    WARNING = "warning"
    FAILED = "failed"


@dataclass
class MorphemeOperationResult:
    """
    Result of a morpheme operation.

    Attributes:
        status: Operation status
        output: Resulting morpheme span
        outputs: Multiple output spans (for split operations)
        residuals: New residuals from operation
        evidence: Evidence supporting operation
        message: Human-readable message
    """
    status: MorphemeOperationStatus
    output: Optional[MorphemeSpan] = None
    outputs: List[MorphemeSpan] = None
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
        return self.status == MorphemeOperationStatus.SUCCESS

    def is_blocked(self) -> bool:
        return self.status == MorphemeOperationStatus.BLOCKED


# ============================================================================
# Operation 1: classify_morpheme
# ============================================================================

def classify_morpheme(
    role_span: RoleSpan,
    morpheme_sort: MorphemeSort,
    morpheme_type: Any,
    evidence: Optional[Dict[str, Any]] = None
) -> MorphemeOperationResult:
    """
    Classify a role span as a morpheme candidate.

    This is the basic U₃ → U₄ transition.

    Args:
        role_span: Source U₃ role span
        morpheme_sort: Morpheme sort category
        morpheme_type: Specific morpheme type
        evidence: Classification evidence

    Returns:
        MorphemeOperationResult with new morpheme span
    """
    if evidence is None:
        evidence = {}

    # Create morpheme identity
    identity = MorphemeIdentity(
        morpheme_id=f"morph_{uuid4().hex[:8]}",
        sort=morpheme_sort,
        morpheme_type=morpheme_type,
        surface_form=role_span.surface,
        trace_to_u3=role_span.span_id
    )

    # Create morpheme candidate
    candidate = MorphemeCandidate(
        identity=identity,
        rank=MorphemeRank.CANDIDATE,
        evidence=[evidence],
        competitors=frozenset(),
        residuals=[]
    )

    # Determine attachment mode
    attachment = AttachmentMode()
    if morpheme_sort == MorphemeSort.AFFIX:
        attachment = AttachmentMode(
            requires_host=True,
            host_position="prefix" if "PREFIX" in morpheme_type.name else "suffix",
            host_category=None  # Will be determined by context
        )

    # Create morpheme span
    morpheme_span = MorphemeSpan(
        span_id=f"mspan_{uuid4().hex[:8]}",
        role_span_ids=[role_span.span_id],
        candidates=[candidate],
        attachment=attachment,
        features=FeaturePotential(),
        trace_to_u3=[role_span.span_id],
        residuals=[],
        rank=MorphemeRank.CANDIDATE.value
    )

    return MorphemeOperationResult(
        status=MorphemeOperationStatus.SUCCESS,
        output=morpheme_span,
        evidence=evidence,
        message=f"Classified {role_span.surface} as {morpheme_sort.value}"
    )


# ============================================================================
# Operation 2: merge_morphemes
# ============================================================================

def merge_morphemes(
    span1: MorphemeSpan,
    span2: MorphemeSpan,
    evidence: Optional[Dict[str, Any]] = None
) -> MorphemeOperationResult:
    """
    Merge two adjacent morpheme spans.

    Used for compound morphemes (e.g., إِنَّ = إِ + نَّ).

    Args:
        span1: First morpheme span
        span2: Second morpheme span
        evidence: Merge evidence

    Returns:
        MorphemeOperationResult with merged span
    """
    if evidence is None:
        evidence = {}

    # Check for blockers
    if span1.has_blocker() or span2.has_blocker():
        return MorphemeOperationResult(
            status=MorphemeOperationStatus.BLOCKED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                "Cannot merge spans with blockers",
                location="merge_morphemes"
            )],
            message="One or both spans have blocking residuals"
        )

    # Merge candidates
    merged_candidates = span1.candidates + span2.candidates

    # Merge traces
    merged_traces = span1.trace_to_u3 + span2.trace_to_u3

    # Merge role span IDs
    merged_role_ids = span1.role_span_ids + span2.role_span_ids

    # Create merged span
    merged_span = MorphemeSpan(
        span_id=f"mspan_merged_{uuid4().hex[:8]}",
        role_span_ids=merged_role_ids,
        candidates=merged_candidates,
        attachment=span1.attachment,  # Inherit from first
        features=FeaturePotential(),
        trace_to_u3=merged_traces,
        residuals=[],
        rank=min(span1.rank, span2.rank)
    )

    # Add ambiguity warning if multiple candidates
    residuals = []
    if len(merged_candidates) > 1:
        residuals.append(make_warning(
            ResidualType.AMBIGUOUS_PATTERN,
            f"Merged span has {len(merged_candidates)} competing candidates",
            location=merged_span.span_id
        ))

    return MorphemeOperationResult(
        status=MorphemeOperationStatus.SUCCESS,
        output=merged_span,
        residuals=residuals,
        evidence=evidence,
        message=f"Merged {len(merged_candidates)} morpheme candidates"
    )


# ============================================================================
# Operation 3: attach_affix
# ============================================================================

def attach_affix(
    affix_span: MorphemeSpan,
    host_span: MorphemeSpan,
    position: str,  # "prefix" | "suffix" | "infix"
    evidence: Optional[Dict[str, Any]] = None
) -> MorphemeOperationResult:
    """
    Attach an affix to a host morpheme.

    Args:
        affix_span: Affix morpheme span
        host_span: Host morpheme span
        position: Attachment position
        evidence: Attachment evidence

    Returns:
        MorphemeOperationResult with attached structure
    """
    if evidence is None:
        evidence = {}

    # Verify affix requires attachment
    if not affix_span.attachment.requires_host:
        return MorphemeOperationResult(
            status=MorphemeOperationStatus.FAILED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                "Morpheme does not require host attachment",
                location="attach_affix"
            )],
            message="Not an affix morpheme"
        )

    # Verify position matches
    if affix_span.attachment.host_position and \
       affix_span.attachment.host_position != position:
        return MorphemeOperationResult(
            status=MorphemeOperationStatus.FAILED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                f"Position mismatch: expected {affix_span.attachment.host_position}, got {position}",
                location="attach_affix"
            )],
            message="Position mismatch"
        )

    # Create attached structure (preserve both spans with attachment relation)
    # The actual combination happens at U₇ (WordForm)
    # Here we just record the attachment

    updated_affix = replace(
        affix_span,
        attachment=replace(
            affix_span.attachment,
            host_position=position
        )
    )

    evidence_with_attachment = {
        **evidence,
        'attached_to': host_span.span_id,
        'position': position
    }

    return MorphemeOperationResult(
        status=MorphemeOperationStatus.SUCCESS,
        output=updated_affix,
        evidence=evidence_with_attachment,
        message=f"Attached {position} to host {host_span.span_id}"
    )


# ============================================================================
# Operation 4: promote_morpheme
# ============================================================================

def promote_morpheme(
    morpheme_span: MorphemeSpan,
    candidate_index: int,
    new_evidence: Dict[str, Any]
) -> MorphemeOperationResult:
    """
    Promote a morpheme candidate's rank.

    Progression: CANDIDATE → HYPOTHESIS → STRONG_HYPOTHESIS → CERTIFICATE

    Args:
        morpheme_span: Target morpheme span
        candidate_index: Index of candidate to promote
        new_evidence: Evidence supporting promotion

    Returns:
        MorphemeOperationResult with promoted candidate
    """
    if candidate_index >= len(morpheme_span.candidates):
        return MorphemeOperationResult(
            status=MorphemeOperationStatus.FAILED,
            message="Invalid candidate index"
        )

    candidate = morpheme_span.candidates[candidate_index]

    # Check if already at max rank
    if candidate.rank == MorphemeRank.CERTIFICATE:
        return MorphemeOperationResult(
            status=MorphemeOperationStatus.SUCCESS,
            output=morpheme_span,
            message="Already at certificate rank"
        )

    # Determine new rank
    rank_progression = {
        MorphemeRank.ZERO: MorphemeRank.CANDIDATE,
        MorphemeRank.CANDIDATE: MorphemeRank.HYPOTHESIS,
        MorphemeRank.HYPOTHESIS: MorphemeRank.STRONG_HYPOTHESIS,
        MorphemeRank.STRONG_HYPOTHESIS: MorphemeRank.CERTIFICATE,
    }

    new_rank = rank_progression.get(candidate.rank, candidate.rank)

    # Create promoted candidate
    promoted_candidate = replace(
        candidate,
        rank=new_rank,
        evidence=candidate.evidence + [new_evidence]
    )

    # Update span
    updated_candidates = morpheme_span.candidates.copy()
    updated_candidates[candidate_index] = promoted_candidate

    updated_span = replace(
        morpheme_span,
        candidates=updated_candidates,
        rank=min(c.rank.value for c in updated_candidates)
    )

    return MorphemeOperationResult(
        status=MorphemeOperationStatus.SUCCESS,
        output=updated_span,
        evidence=new_evidence,
        message=f"Promoted to {new_rank.name}"
    )


# ============================================================================
# Operation 5: block_morpheme
# ============================================================================

def block_morpheme(
    morpheme_span: MorphemeSpan,
    candidate_index: int,
    blocker: Residual
) -> MorphemeOperationResult:
    """
    Block a morpheme candidate with evidence.

    Args:
        morpheme_span: Target morpheme span
        candidate_index: Index of candidate to block
        blocker: Blocking residual

    Returns:
        MorphemeOperationResult with blocked candidate
    """
    if candidate_index >= len(morpheme_span.candidates):
        return MorphemeOperationResult(
            status=MorphemeOperationStatus.FAILED,
            message="Invalid candidate index"
        )

    candidate = morpheme_span.candidates[candidate_index]

    # Add blocker to candidate
    blocked_candidate = replace(
        candidate,
        residuals=candidate.residuals + [blocker],
        rank=MorphemeRank.ZERO  # Reset to zero when blocked
    )

    # Update span
    updated_candidates = morpheme_span.candidates.copy()
    updated_candidates[candidate_index] = blocked_candidate

    updated_span = replace(
        morpheme_span,
        candidates=updated_candidates
    )

    return MorphemeOperationResult(
        status=MorphemeOperationStatus.SUCCESS,
        output=updated_span,
        residuals=[blocker],
        message=f"Blocked candidate {candidate_index}"
    )


# ============================================================================
# Operation 6: preserve_competitors
# ============================================================================

def preserve_competitors(
    morpheme_span: MorphemeSpan,
    evidence: Optional[Dict[str, Any]] = None
) -> MorphemeOperationResult:
    """
    Explicitly preserve competing morpheme interpretations.

    This operation marks that competition is intentional and should not
    be resolved yet.

    Args:
        morpheme_span: Target morpheme span
        evidence: Evidence for preserving competition

    Returns:
        MorphemeOperationResult with preserved competitors
    """
    if evidence is None:
        evidence = {'preserve_competitors': True}

    # Get all non-blocked candidates
    active_candidates = [
        c for c in morpheme_span.candidates
        if not c.has_blocker()
    ]

    if len(active_candidates) <= 1:
        return MorphemeOperationResult(
            status=MorphemeOperationStatus.SUCCESS,
            output=morpheme_span,
            message="No competitors to preserve"
        )

    # Mark all candidates as competitors of each other
    competitor_ids = frozenset(c.identity.morpheme_id for c in active_candidates)

    updated_candidates = []
    for candidate in morpheme_span.candidates:
        if not candidate.has_blocker():
            updated = replace(
                candidate,
                competitors=competitor_ids
            )
            updated_candidates.append(updated)
        else:
            updated_candidates.append(candidate)

    updated_span = replace(
        morpheme_span,
        candidates=updated_candidates
    )

    return MorphemeOperationResult(
        status=MorphemeOperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message=f"Preserved {len(active_candidates)} competing interpretations"
    )
