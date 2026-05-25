"""
U₅ Root/Stem Operations (عمليات الجذر والجذع)

Implements Ω₅ = Root/Stem operation algebra

Operations:
    - extract_root: MorphemeSpan → RootCandidate
    - build_stem: MorphemeSpan → StemCandidate
    - classify_weak_root: Root → WeakType
    - mark_frozen: Stem → Frozen
    - mark_derived: Stem + Root → Derived
    - promote_root: candidate → hypothesis → confirmed
    - preserve_competitors: Maintain competing root/stem interpretations

PR: U5-LAYER
Created: 2026-05-25
"""

from dataclasses import dataclass, replace
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum
from uuid import uuid4

from dal_core.u5_stemroot_carrier import (
    RootStemSpan,
    RootCandidate,
    StemCandidate,
    RootIdentity,
    StemIdentity,
    Radical,
    RadicalPosition,
    RootType,
    RootStatus,
    StemType,
    StemStatus,
    RootRank,
    RootResidualCode,
    classify_weak_type,
    identify_weak_root,
    identify_hamzated_root,
)
from dal_core.u4_morpheme_carrier import MorphemeSpan, MorphemeSort, RootCandidateType
from dal_core.residuals import Residual, make_warning, make_blocker, ResidualType


# ============================================================================
# Operation Result Types
# ============================================================================

class RootStemOperationStatus(Enum):
    """Status of a root/stem operation."""
    SUCCESS = "success"
    BLOCKED = "blocked"
    WARNING = "warning"
    FAILED = "failed"


@dataclass
class RootStemOperationResult:
    """
    Result of a root/stem operation.

    Attributes:
        status: Operation status
        output: Resulting root/stem span
        residuals: New residuals
        evidence: Supporting evidence
        message: Human-readable message
    """
    status: RootStemOperationStatus
    output: Optional[RootStemSpan] = None
    residuals: List[Residual] = None
    evidence: Dict[str, Any] = None
    message: str = ""

    def __post_init__(self):
        if self.residuals is None:
            self.residuals = []
        if self.evidence is None:
            self.evidence = {}

    def is_success(self) -> bool:
        return self.status == RootStemOperationStatus.SUCCESS


# ============================================================================
# Operation 1: extract_root
# ============================================================================

def extract_root(
    morpheme_spans: List[MorphemeSpan],
    radicals: Tuple[Radical, ...],
    evidence: Optional[Dict[str, Any]] = None
) -> RootStemOperationResult:
    """
    Extract root from morpheme spans.

    This operation creates a root candidate from identified radicals.

    Args:
        morpheme_spans: Source U₄ morpheme spans
        radicals: Identified radicals
        evidence: Extraction evidence

    Returns:
        RootStemOperationResult with root candidate
    """
    if evidence is None:
        evidence = {}

    if not radicals:
        return RootStemOperationResult(
            status=RootStemOperationStatus.FAILED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                "No radicals provided for root extraction",
                location="extract_root"
            )],
            message="No radicals"
        )

    # Determine root type
    num_radicals = len(radicals)
    if num_radicals == 3:
        base_type = RootType.TRILATERAL
    elif num_radicals == 4:
        base_type = RootType.QUADRILATERAL
    elif num_radicals == 5:
        base_type = RootType.QUINQUELITERAL
    else:
        return RootStemOperationResult(
            status=RootStemOperationStatus.FAILED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                f"Invalid radical count: {num_radicals}",
                location="extract_root"
            )],
            message="Invalid radical count"
        )

    # Check for weak/hamzated/doubled
    is_weak = identify_weak_root(radicals)
    is_hamzated = identify_hamzated_root(radicals)
    is_doubled = any(r.is_doubled for r in radicals)

    # Classify specific type
    if is_weak:
        root_type = classify_weak_type(radicals)
    elif is_hamzated:
        root_type = RootType.HAMZATED
    elif is_doubled:
        root_type = RootType.DOUBLED
    else:
        root_type = base_type

    # Create root identity
    surface_form = ''.join(r.letter for r in radicals)
    trace_ids = tuple(ms.span_id for ms in morpheme_spans)

    identity = RootIdentity(
        root_id=f"root_{uuid4().hex[:8]}",
        radicals=radicals,
        root_type=root_type,
        surface_form=surface_form,
        trace_to_u4=trace_ids
    )

    # Create root candidate
    root_candidate = RootCandidate(
        identity=identity,
        status=RootStatus.CANDIDATE,
        rank=RootRank.CANDIDATE,
        evidence=[evidence],
        competitors=frozenset(),
        residuals=[]
    )

    # Create root/stem span
    span = RootStemSpan(
        span_id=f"rootstem_{uuid4().hex[:8]}",
        morpheme_span_ids=[ms.span_id for ms in morpheme_spans],
        root_candidates=[root_candidate],
        stem_candidates=[],
        frozen_hypothesis=False,
        pattern_hints=[],
        trace_to_u4=list(trace_ids),
        residuals=[],
        rank=RootRank.CANDIDATE.value
    )

    return RootStemOperationResult(
        status=RootStemOperationStatus.SUCCESS,
        output=span,
        evidence=evidence,
        message=f"Extracted {root_type.value} root: {identity.get_radical_string()}"
    )


# ============================================================================
# Operation 2: build_stem
# ============================================================================

def build_stem(
    morpheme_spans: List[MorphemeSpan],
    stem_type: StemType,
    is_frozen: bool = False,
    root_id: Optional[str] = None,
    evidence: Optional[Dict[str, Any]] = None
) -> RootStemOperationResult:
    """
    Build stem from morpheme spans.

    Args:
        morpheme_spans: Source U₄ morpheme spans
        stem_type: Type of stem
        is_frozen: Is frozen (جامد) form
        root_id: Associated root (if derived)
        evidence: Building evidence

    Returns:
        RootStemOperationResult with stem candidate
    """
    if evidence is None:
        evidence = {}

    # Enforce law: frozen stems have no root
    if is_frozen and root_id is not None:
        return RootStemOperationResult(
            status=RootStemOperationStatus.FAILED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                "Frozen stem cannot have root reference",
                location="build_stem"
            )],
            message="Frozen stem with root"
        )

    # Extract surface form
    surface_form = ''.join(ms.primary_candidate().identity.surface_form
                          for ms in morpheme_spans
                          if ms.primary_candidate())

    # Create stem identity
    trace_ids = tuple(ms.span_id for ms in morpheme_spans)

    identity = StemIdentity(
        stem_id=f"stem_{uuid4().hex[:8]}",
        stem_type=stem_type,
        surface_form=surface_form,
        root_id=root_id,
        original_letters=tuple(),  # Will be filled by pattern analysis
        extra_letters=tuple(),
        trace_to_u4=trace_ids
    )

    # Create stem candidate
    stem_candidate = StemCandidate(
        identity=identity,
        status=StemStatus.CANDIDATE,
        rank=RootRank.CANDIDATE,
        is_frozen=is_frozen,
        is_derived=root_id is not None,
        evidence=[evidence],
        residuals=[]
    )

    # Create root/stem span
    span = RootStemSpan(
        span_id=f"rootstem_{uuid4().hex[:8]}",
        morpheme_span_ids=[ms.span_id for ms in morpheme_spans],
        root_candidates=[],
        stem_candidates=[stem_candidate],
        frozen_hypothesis=is_frozen,
        pattern_hints=[],
        trace_to_u4=list(trace_ids),
        residuals=[],
        rank=RootRank.CANDIDATE.value
    )

    return RootStemOperationResult(
        status=RootStemOperationStatus.SUCCESS,
        output=span,
        evidence=evidence,
        message=f"Built {stem_type.value} stem: {surface_form}"
    )


# ============================================================================
# Operation 3: mark_frozen
# ============================================================================

def mark_frozen(
    rootstem_span: RootStemSpan,
    evidence: Dict[str, Any]
) -> RootStemOperationResult:
    """
    Mark a root/stem span as frozen (جامد).

    Frozen items have no derivational structure.

    Args:
        rootstem_span: Target span
        evidence: Evidence for frozen status

    Returns:
        RootStemOperationResult with frozen marking
    """
    # Frozen items should not have root candidates
    if rootstem_span.root_candidates:
        return RootStemOperationResult(
            status=RootStemOperationStatus.WARNING,
            residuals=[make_warning(
                ResidualType.AMBIGUOUS_PATTERN,
                "Frozen marking conflicts with root candidates",
                location=rootstem_span.span_id
            )],
            message="Conflict: has root candidates"
        )

    # Mark all stem candidates as frozen
    updated_stems = []
    for stem in rootstem_span.stem_candidates:
        updated_stem = replace(
            stem,
            is_frozen=True,
            is_derived=False,  # Frozen ≠ Derived
            evidence=stem.evidence + [evidence]
        )
        updated_stems.append(updated_stem)

    updated_span = replace(
        rootstem_span,
        stem_candidates=updated_stems,
        frozen_hypothesis=True,
        root_candidates=[]  # Clear root candidates
    )

    return RootStemOperationResult(
        status=RootStemOperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message="Marked as frozen (جامد)"
    )


# ============================================================================
# Operation 4: mark_derived
# ============================================================================

def mark_derived(
    rootstem_span: RootStemSpan,
    stem_index: int,
    root_index: int,
    evidence: Dict[str, Any]
) -> RootStemOperationResult:
    """
    Mark a stem as derived from a root.

    Args:
        rootstem_span: Target span
        stem_index: Index of stem to mark
        root_index: Index of associated root
        evidence: Evidence for derivation

    Returns:
        RootStemOperationResult with derived marking
    """
    if stem_index >= len(rootstem_span.stem_candidates):
        return RootStemOperationResult(
            status=RootStemOperationStatus.FAILED,
            message="Invalid stem index"
        )

    if root_index >= len(rootstem_span.root_candidates):
        return RootStemOperationResult(
            status=RootStemOperationStatus.FAILED,
            message="Invalid root index"
        )

    stem = rootstem_span.stem_candidates[stem_index]
    root = rootstem_span.root_candidates[root_index]

    # Create updated stem with root reference
    updated_stem = replace(
        stem,
        identity=replace(
            stem.identity,
            root_id=root.identity.root_id
        ),
        is_derived=True,
        is_frozen=False,  # Derived ≠ Frozen
        evidence=stem.evidence + [evidence]
    )

    # Update span
    updated_stems = rootstem_span.stem_candidates.copy()
    updated_stems[stem_index] = updated_stem

    updated_span = replace(
        rootstem_span,
        stem_candidates=updated_stems,
        frozen_hypothesis=False
    )

    return RootStemOperationResult(
        status=RootStemOperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message=f"Marked stem as derived from root {root.identity.get_radical_string()}"
    )


# ============================================================================
# Operation 5: promote_root
# ============================================================================

def promote_root(
    rootstem_span: RootStemSpan,
    root_index: int,
    new_evidence: Dict[str, Any]
) -> RootStemOperationResult:
    """
    Promote a root candidate's rank.

    Progression: CANDIDATE → HYPOTHESIS → STRONG_HYPOTHESIS → CERTIFICATE

    Args:
        rootstem_span: Target span
        root_index: Index of root to promote
        new_evidence: Evidence supporting promotion

    Returns:
        RootStemOperationResult with promoted root
    """
    if root_index >= len(rootstem_span.root_candidates):
        return RootStemOperationResult(
            status=RootStemOperationStatus.FAILED,
            message="Invalid root index"
        )

    root = rootstem_span.root_candidates[root_index]

    # Determine new rank
    rank_progression = {
        RootRank.ZERO: RootRank.CANDIDATE,
        RootRank.CANDIDATE: RootRank.HYPOTHESIS,
        RootRank.HYPOTHESIS: RootRank.STRONG_HYPOTHESIS,
        RootRank.STRONG_HYPOTHESIS: RootRank.CERTIFICATE,
    }

    new_rank = rank_progression.get(root.rank, root.rank)

    # Determine new status based on rank
    if new_rank == RootRank.CERTIFICATE:
        new_status = RootStatus.ATTESTED
    elif new_rank == RootRank.STRONG_HYPOTHESIS:
        new_status = RootStatus.CONFIRMED
    elif new_rank == RootRank.HYPOTHESIS:
        new_status = RootStatus.HYPOTHESIS
    else:
        new_status = root.status

    # Create promoted root
    promoted_root = replace(
        root,
        rank=new_rank,
        status=new_status,
        evidence=root.evidence + [new_evidence]
    )

    # Update span
    updated_roots = rootstem_span.root_candidates.copy()
    updated_roots[root_index] = promoted_root

    updated_span = replace(
        rootstem_span,
        root_candidates=updated_roots,
        rank=min(r.rank.value for r in updated_roots)
    )

    return RootStemOperationResult(
        status=RootStemOperationStatus.SUCCESS,
        output=updated_span,
        evidence=new_evidence,
        message=f"Promoted to {new_rank.name} / {new_status.value}"
    )


# ============================================================================
# Operation 6: add_pattern_hint
# ============================================================================

def add_pattern_hint(
    rootstem_span: RootStemSpan,
    pattern: str,
    evidence: Dict[str, Any]
) -> RootStemOperationResult:
    """
    Add pattern hint for U₆ transition.

    This does NOT commit to pattern, just provides hint.

    Args:
        rootstem_span: Target span
        pattern: Pattern hint (e.g., "فعل", "فاعل")
        evidence: Evidence for hint

    Returns:
        RootStemOperationResult with pattern hint
    """
    updated_hints = rootstem_span.pattern_hints + [pattern]

    updated_span = replace(
        rootstem_span,
        pattern_hints=updated_hints
    )

    return RootStemOperationResult(
        status=RootStemOperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message=f"Added pattern hint: {pattern}"
    )
