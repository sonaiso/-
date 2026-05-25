"""
U₆ Pattern Operations (عمليات الوزن)

Implements Ω₆ = Pattern operation algebra

Operations:
    - match_pattern: RootStem → PatternCandidate
    - identify_augments: Pattern → Original + Extra
    - map_vowels: Pattern → VowelTemplate
    - promote_pattern: candidate → hypothesis → certificate
    - add_form_hint: Pattern → FormHint (for U₇)

PR: U6-LAYER
Created: 2026-05-25
"""

from dataclasses import dataclass, replace
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum
from uuid import uuid4

from dal_core.u6_pattern_carrier import (
    PatternSpan,
    PatternCandidate,
    PatternIdentity,
    VowelTemplate,
    LetterMapping,
    PatternSort,
    PatternRank,
    VerbPattern,
    NounPattern,
    extract_vowel_template,
    map_root_to_pattern,
    identify_extra_letters,
)
from dal_core.u5_stemroot_carrier import RootStemSpan
from dal_core.residuals import Residual, make_warning, make_blocker, ResidualType


# ============================================================================
# Operation Result Types
# ============================================================================

class PatternOperationStatus(Enum):
    """Status of a pattern operation."""
    SUCCESS = "success"
    BLOCKED = "blocked"
    WARNING = "warning"
    FAILED = "failed"


@dataclass
class PatternOperationResult:
    """
    Result of a pattern operation.

    Attributes:
        status: Operation status
        output: Resulting pattern span
        residuals: New residuals
        evidence: Supporting evidence
        message: Human-readable message
    """
    status: PatternOperationStatus
    output: Optional[PatternSpan] = None
    residuals: List[Residual] = None
    evidence: Dict[str, Any] = None
    message: str = ""

    def __post_init__(self):
        if self.residuals is None:
            self.residuals = []
        if self.evidence is None:
            self.evidence = {}

    def is_success(self) -> bool:
        return self.status == PatternOperationStatus.SUCCESS


# ============================================================================
# Operation 1: match_pattern
# ============================================================================

def match_pattern(
    rootstem_span: RootStemSpan,
    pattern_type: Any,  # VerbPattern or NounPattern
    pattern_sort: PatternSort,
    evidence: Optional[Dict[str, Any]] = None
) -> PatternOperationResult:
    """
    Match a pattern to root/stem.

    This is the basic U₅ → U₆ transition.

    Args:
        rootstem_span: Source U₅ root/stem span
        pattern_type: Pattern type to match
        pattern_sort: Pattern sort
        evidence: Matching evidence

    Returns:
        PatternOperationResult with pattern span
    """
    if evidence is None:
        evidence = {}

    # Get primary root
    primary_root = rootstem_span.primary_root()
    if not primary_root and not rootstem_span.frozen_hypothesis:
        return PatternOperationResult(
            status=PatternOperationStatus.FAILED,
            residuals=[make_blocker(
                ResidualType.INVALID_SYLLABLE,
                "No root found for pattern matching",
                location="match_pattern"
            )],
            message="No root available"
        )

    # Extract pattern string
    pattern_str = pattern_type.value

    # Create vowel template
    vowel_template = extract_vowel_template(pattern_str)

    # Map root to pattern (if not frozen)
    root_mapping = tuple()
    original_letters = tuple()

    if primary_root:
        root_mapping = map_root_to_pattern(primary_root, pattern_str)
        original_letters = tuple(r.letter for r in primary_root.identity.radicals)

    # Identify extra letters
    surface_form = rootstem_span.primary_stem().identity.surface_form if rootstem_span.primary_stem() else ""
    extra_letters = identify_extra_letters(surface_form, original_letters) if surface_form else tuple()

    # Create pattern identity
    identity = PatternIdentity(
        pattern_id=f"pattern_{uuid4().hex[:8]}",
        sort=pattern_sort,
        pattern_type=pattern_type,
        abstract_pattern=pattern_str,
        vowel_template=vowel_template,
        root_mapping=root_mapping,
        trace_to_u5=rootstem_span.span_id
    )

    # Create pattern candidate
    candidate = PatternCandidate(
        identity=identity,
        rank=PatternRank.CANDIDATE,
        original_letters=original_letters,
        extra_letters=extra_letters,
        derivational_gate=None,
        evidence=[evidence],
        residuals=[]
    )

    # Create pattern span
    span = PatternSpan(
        span_id=f"pattern_{uuid4().hex[:8]}",
        rootstem_span_id=rootstem_span.span_id,
        pattern_candidates=[candidate],
        transformation_type=None,
        form_hints=[],
        trace_to_u5=rootstem_span.span_id,
        residuals=[],
        rank=PatternRank.CANDIDATE.value
    )

    return PatternOperationResult(
        status=PatternOperationStatus.SUCCESS,
        output=span,
        evidence=evidence,
        message=f"Matched pattern {pattern_str}"
    )


# ============================================================================
# Operation 2: identify_transformation
# ============================================================================

def identify_transformation(
    pattern_span: PatternSpan,
    transformation_type: str,  # "derivation" | "inflection" | "frozen"
    evidence: Dict[str, Any]
) -> PatternOperationResult:
    """
    Identify transformation type for pattern.

    Args:
        pattern_span: Target pattern span
        transformation_type: Type of transformation
        evidence: Evidence for transformation

    Returns:
        PatternOperationResult with transformation marked
    """
    valid_types = {"derivation", "inflection", "frozen"}
    if transformation_type not in valid_types:
        return PatternOperationResult(
            status=PatternOperationStatus.FAILED,
            message=f"Invalid transformation type: {transformation_type}"
        )

    updated_span = replace(
        pattern_span,
        transformation_type=transformation_type
    )

    return PatternOperationResult(
        status=PatternOperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message=f"Identified as {transformation_type}"
    )


# ============================================================================
# Operation 3: promote_pattern
# ============================================================================

def promote_pattern(
    pattern_span: PatternSpan,
    candidate_index: int,
    new_evidence: Dict[str, Any]
) -> PatternOperationResult:
    """
    Promote a pattern candidate's rank.

    Args:
        pattern_span: Target pattern span
        candidate_index: Index of candidate to promote
        new_evidence: Evidence supporting promotion

    Returns:
        PatternOperationResult with promoted pattern
    """
    if candidate_index >= len(pattern_span.pattern_candidates):
        return PatternOperationResult(
            status=PatternOperationStatus.FAILED,
            message="Invalid candidate index"
        )

    candidate = pattern_span.pattern_candidates[candidate_index]

    # Determine new rank
    rank_progression = {
        PatternRank.ZERO: PatternRank.CANDIDATE,
        PatternRank.CANDIDATE: PatternRank.HYPOTHESIS,
        PatternRank.HYPOTHESIS: PatternRank.STRONG_HYPOTHESIS,
        PatternRank.STRONG_HYPOTHESIS: PatternRank.CERTIFICATE,
    }

    new_rank = rank_progression.get(candidate.rank, candidate.rank)

    # Create promoted candidate
    promoted = replace(
        candidate,
        rank=new_rank,
        evidence=candidate.evidence + [new_evidence]
    )

    # Update span
    updated_candidates = pattern_span.pattern_candidates.copy()
    updated_candidates[candidate_index] = promoted

    updated_span = replace(
        pattern_span,
        pattern_candidates=updated_candidates,
        rank=min(c.rank.value for c in updated_candidates)
    )

    return PatternOperationResult(
        status=PatternOperationStatus.SUCCESS,
        output=updated_span,
        evidence=new_evidence,
        message=f"Promoted to {new_rank.name}"
    )


# ============================================================================
# Operation 4: add_form_hint
# ============================================================================

def add_form_hint(
    pattern_span: PatternSpan,
    hint: str,
    evidence: Dict[str, Any]
) -> PatternOperationResult:
    """
    Add form hint for U₇ transition.

    Hints guide word form construction without committing.

    Args:
        pattern_span: Target pattern span
        hint: Form hint (e.g., "verb_past", "noun_active_participle")
        evidence: Evidence for hint

    Returns:
        PatternOperationResult with hint added
    """
    updated_hints = pattern_span.form_hints + [hint]

    updated_span = replace(
        pattern_span,
        form_hints=updated_hints
    )

    return PatternOperationResult(
        status=PatternOperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message=f"Added form hint: {hint}"
    )


# ============================================================================
# Operation 5: mark_derivational_gate
# ============================================================================

def mark_derivational_gate(
    pattern_span: PatternSpan,
    candidate_index: int,
    gate: str,
    evidence: Dict[str, Any]
) -> PatternOperationResult:
    """
    Mark derivational gate for pattern.

    Gates: causative, reflexive, reciprocal, intensive, etc.

    Args:
        pattern_span: Target pattern span
        candidate_index: Index of candidate
        gate: Derivational gate
        evidence: Evidence for gate

    Returns:
        PatternOperationResult with gate marked
    """
    if candidate_index >= len(pattern_span.pattern_candidates):
        return PatternOperationResult(
            status=PatternOperationStatus.FAILED,
            message="Invalid candidate index"
        )

    candidate = pattern_span.pattern_candidates[candidate_index]

    updated_candidate = replace(
        candidate,
        derivational_gate=gate,
        evidence=candidate.evidence + [evidence]
    )

    updated_candidates = pattern_span.pattern_candidates.copy()
    updated_candidates[candidate_index] = updated_candidate

    updated_span = replace(
        pattern_span,
        pattern_candidates=updated_candidates
    )

    return PatternOperationResult(
        status=PatternOperationStatus.SUCCESS,
        output=updated_span,
        evidence=evidence,
        message=f"Marked derivational gate: {gate}"
    )
