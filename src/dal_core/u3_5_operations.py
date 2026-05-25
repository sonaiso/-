"""
U₃.₅ Boundary and Attachment Operations

Operations for segmenting WrittenCompositeToken into TrueSingularLafẓ units.

All operations:
    1. Preserve trace from U₃
    2. Propagate residuals
    3. Return OperationResult (no exceptions)
    4. Document evidence

PR: U3.5-BOUNDARY-LAYER
Created: 2026-05-25
"""

from dataclasses import dataclass, field, replace
from enum import Enum, auto
from typing import List, Optional, Set, FrozenSet, Dict, Any, Tuple
from uuid import uuid4

from dal_core.u3_5_boundary_attachment import (
    WrittenCompositeToken,
    TrueSingularLafz,
    BoundarySegmentation,
    BoundaryCandidate,
    AttachmentType,
    BoundarySegmentationType,
    TrueSingularLafzType,
    BoundaryRank,
    BoundaryResidual,
    CompleteOne_3_5,
)
from dal_core.u3_functional_roles import RoleSpan
from dal_core.residuals import Residual


# ============================================================================
# Operation Result
# ============================================================================

class OperationStatus(Enum):
    """Status of operation execution."""
    SUCCESS = auto()       # Operation succeeded
    BLOCKED = auto()       # Operation blocked by residuals/evidence
    WARNING = auto()       # Operation succeeded with warnings
    FAILED = auto()        # Operation failed


@dataclass
class OperationResult:
    """
    Result of boundary operation.

    Structured result type - NO exceptions.

    Fields:
        status: Operation status
        output: Resulting candidate (if successful)
        residuals: New/propagated residuals
        evidence: Evidence for this operation
        message: Human-readable message
    """
    status: OperationStatus
    output: Optional[BoundaryCandidate] = None
    residuals: List[BoundaryResidual] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    message: str = ""

    def is_success(self) -> bool:
        """Check if operation succeeded."""
        return self.status in {OperationStatus.SUCCESS, OperationStatus.WARNING}

    def is_blocked(self) -> bool:
        """Check if operation was blocked."""
        return self.status == OperationStatus.BLOCKED

    def __str__(self) -> str:
        if self.output:
            return f"{self.status.name}: {self.output}"
        return f"{self.status.name}: {self.message}"


# ============================================================================
# Operation 1: Segment Written Token
# ============================================================================

def segment_written_token(
    written_token: WrittenCompositeToken,
    lexicon_proclitics: Optional[Set[str]] = None,
    lexicon_enclitics: Optional[Set[str]] = None,
    policy: Optional[Dict[str, Any]] = None
) -> OperationResult:
    """
    Segment written composite token into true singular lafẓ units.

    Strategy:
        1. Check for known proclitics (و، ف، ب، ل، ك، etc.)
        2. Check for known enclitics (pronouns: ـه، ـك، ـها، etc.)
        3. Identify core stem/verbal unit
        4. Build segmentation with proper attachment types
        5. Preserve trace from U₃
        6. Add residuals for ambiguities

    Args:
        written_token: Written composite token to segment
        lexicon_proclitics: Set of attested proclitic forms
        lexicon_enclitics: Set of attested enclitic forms
        policy: Segmentation policy (exhaustive, etc.)

    Returns:
        OperationResult with BoundaryCandidate

    Examples:
        وَبِكِتَابِهِمْ → [وَ, بِ, كِتَاب, ـهِمْ]
        كِتَابٌ → [كِتَابٌ]
        فَسَيَكْتُبُونَهَا → [فَ, سَ, يَكْتُبُونَ, ـها]
    """
    surface = written_token.surface
    residuals: List[BoundaryResidual] = []
    evidence: Dict[str, Any] = {
        'surface': surface,
        'operation': 'segment_written_token'
    }

    # Default lexicons
    if lexicon_proclitics is None:
        lexicon_proclitics = {'و', 'وَ', 'ف', 'فَ', 'ب', 'بِ', 'ل', 'لِ', 'ك', 'كَ'}
    if lexicon_enclitics is None:
        lexicon_enclitics = {'ه', 'ـه', 'ـهُ', 'ك', 'ـك', 'ـكَ', 'ها', 'ـها', 'هم', 'ـهم', 'ـهُمْ'}

    # Policy defaults
    policy = policy or {}
    max_proclitics = policy.get('max_proclitics', 3)
    max_enclitics = policy.get('max_enclitics', 2)

    # Try to segment
    units: List[TrueSingularLafz] = []
    remaining = surface
    position = 0

    # Extract proclitics (greedy left-to-right)
    proclitics_found = []
    while remaining and len(proclitics_found) < max_proclitics:
        matched = False
        for proclitic in sorted(lexicon_proclitics, key=len, reverse=True):
            if remaining.startswith(proclitic):
                proclitics_found.append(proclitic)
                remaining = remaining[len(proclitic):]
                matched = True
                break
        if not matched:
            break

    # Extract enclitics (greedy right-to-left)
    enclitics_found = []
    while remaining and len(enclitics_found) < max_enclitics:
        matched = False
        for enclitic in sorted(lexicon_enclitics, key=len, reverse=True):
            if remaining.endswith(enclitic):
                enclitics_found.insert(0, enclitic)  # Insert at beginning to preserve order
                remaining = remaining[:-len(enclitic)]
                matched = True
                break
        if not matched:
            break

    # Remaining is the core
    core_surface = remaining

    # Build units
    # 1. Proclitics
    for proclitic in proclitics_found:
        unit = TrueSingularLafz(
            surface=proclitic,
            lafz_type=TrueSingularLafzType.CLOSED_CLASS,
            attachment_type=AttachmentType.PROCLITIC,
            role_spans=written_token.role_spans,  # Simplified - should split properly
            weight_access=False,
            detachable=True
        )
        units.append(unit)

    # 2. Core (if exists)
    if core_surface:
        # Determine core type (heuristic - should use U₃ evidence)
        core_type = AttachmentType.STEM_CORE  # Default to stem
        lafz_type = TrueSingularLafzType.OPEN_LEXICAL_CORE

        # Simple heuristic: if starts with verb prefix, might be verbal
        verb_prefixes = {'ي', 'يَ', 'ت', 'تَ', 'ن', 'نَ', 'أ', 'أَ'}
        if any(core_surface.startswith(p) for p in verb_prefixes):
            # Could be verbal, but don't commit yet
            residuals.append(BoundaryResidual.PREFIX_VS_PATTERN_AUGMENT_AMBIGUITY)

        core_unit = TrueSingularLafz(
            surface=core_surface,
            lafz_type=lafz_type,
            attachment_type=core_type,
            role_spans=written_token.role_spans,
            weight_access=True,  # Core enters weight analysis
            detachable=False
        )
        units.append(core_unit)
    else:
        # No core found - problematic
        residuals.append(BoundaryResidual.UNDER_SEGMENTATION_RISK)
        return OperationResult(
            status=OperationStatus.BLOCKED,
            residuals=residuals,
            evidence=evidence,
            message=f"No core found in segmentation of {surface}"
        )

    # 3. Enclitics
    for enclitic in enclitics_found:
        unit = TrueSingularLafz(
            surface=enclitic,
            lafz_type=TrueSingularLafzType.PRONOUN,
            attachment_type=AttachmentType.ENCLITIC,
            role_spans=written_token.role_spans,
            weight_access=False,
            detachable=True
        )
        units.append(unit)

    # Determine segmentation type
    if len(units) == 1:
        seg_type = BoundarySegmentationType.CORE_ONLY
    elif proclitics_found and enclitics_found:
        seg_type = BoundarySegmentationType.PROCLITIC_CORE_ENCLITIC
    elif len(proclitics_found) > 1:
        seg_type = BoundarySegmentationType.MULTIPLE_PROCLITICS
    elif len(enclitics_found) > 1:
        seg_type = BoundarySegmentationType.MULTIPLE_ENCLITICS
    else:
        seg_type = BoundarySegmentationType.COMPLEX_SEGMENTATION

    # Add residuals for ambiguities
    if proclitics_found:
        # Could the first proclitic be part of stem?
        residuals.append(BoundaryResidual.PROCLITIC_VS_STEM_AMBIGUITY)
    if enclitics_found:
        residuals.append(BoundaryResidual.ENCLITIC_VS_STEM_AMBIGUITY)

    # Build segmentation
    segmentation = BoundarySegmentation(
        written_token=written_token,
        units=tuple(units),
        segmentation_type=seg_type,
        trace=written_token.role_spans,
        residuals=frozenset(residuals),
        rank=BoundaryRank.BOUNDARY_HYPOTHESIS if proclitics_found or enclitics_found
             else BoundaryRank.BOUNDARY_CANDIDATE,
        evidence=evidence
    )

    # Build candidate
    candidate = BoundaryCandidate(
        segmentation=segmentation,
        rank=segmentation.rank,
        residuals=segmentation.residuals,
        trace=written_token.role_spans,
        evidence=evidence
    )

    status = OperationStatus.WARNING if residuals else OperationStatus.SUCCESS
    return OperationResult(
        status=status,
        output=candidate,
        residuals=residuals,
        evidence=evidence,
        message=f"Segmented {surface} into {len(units)} units"
    )


# ============================================================================
# Operation 2: Classify Unit
# ============================================================================

def classify_unit(
    unit: TrueSingularLafz,
    lexicon_particles: Optional[Set[str]] = None,
    lexicon_pronouns: Optional[Set[str]] = None
) -> OperationResult:
    """
    Classify or reclassify a true singular lafẓ unit.

    Determines the proper lafz_type based on evidence.

    Args:
        unit: Unit to classify
        lexicon_particles: Set of attested particles
        lexicon_pronouns: Set of attested pronouns

    Returns:
        OperationResult with updated BoundaryCandidate
    """
    surface = unit.surface
    residuals: List[BoundaryResidual] = []
    evidence: Dict[str, Any] = {
        'surface': surface,
        'operation': 'classify_unit'
    }

    # Default lexicons
    if lexicon_particles is None:
        lexicon_particles = {'و', 'ف', 'ب', 'ل', 'ك', 'في', 'من', 'إلى', 'عن'}
    if lexicon_pronouns is None:
        lexicon_pronouns = {'ه', 'ـه', 'ك', 'ـك', 'ها', 'ـها', 'هم', 'ـهم', 'هو', 'هي'}

    # Classify
    new_type = unit.lafz_type
    new_rank = BoundaryRank.BOUNDARY_CANDIDATE

    # Remove diacritics for matching
    surface_bare = surface.replace('َ', '').replace('ُ', '').replace('ِ', '').replace('ْ', '').replace('ّ', '')

    if surface_bare in lexicon_particles:
        new_type = TrueSingularLafzType.CLOSED_CLASS
        new_rank = BoundaryRank.BOUNDARY_CERTIFICATE
        evidence['lexicon_match'] = 'particle'
    elif surface_bare in lexicon_pronouns:
        new_type = TrueSingularLafzType.PRONOUN
        new_rank = BoundaryRank.BOUNDARY_CERTIFICATE
        evidence['lexicon_match'] = 'pronoun'
    else:
        # Heuristics
        if len(surface_bare) <= 2:
            new_type = TrueSingularLafzType.CLOSED_CLASS
            residuals.append(BoundaryResidual.INSUFFICIENT_EVIDENCE)
        else:
            new_type = TrueSingularLafzType.OPEN_LEXICAL_CORE
            new_rank = BoundaryRank.BOUNDARY_HYPOTHESIS

    # Build updated unit (frozen, so create new)
    updated_unit = TrueSingularLafz(
        surface=unit.surface,
        lafz_type=new_type,
        attachment_type=unit.attachment_type,
        role_spans=unit.role_spans,
        weight_access=unit.weight_access,
        detachable=unit.detachable,
        id=unit.id
    )

    # Create minimal candidate for return
    # (In real usage, this would update a full BoundaryCandidate)
    seg = BoundarySegmentation(
        written_token=WrittenCompositeToken(surface=surface, role_spans=unit.role_spans),
        units=(updated_unit,),
        segmentation_type=BoundarySegmentationType.CORE_ONLY,
        trace=unit.role_spans,
        residuals=frozenset(residuals),
        rank=new_rank,
        evidence=evidence
    )

    candidate = BoundaryCandidate(
        segmentation=seg,
        rank=new_rank,
        residuals=frozenset(residuals),
        trace=unit.role_spans,
        evidence=evidence
    )

    status = OperationStatus.WARNING if residuals else OperationStatus.SUCCESS
    return OperationResult(
        status=status,
        output=candidate,
        residuals=residuals,
        evidence=evidence,
        message=f"Classified {surface} as {new_type.value}"
    )


# ============================================================================
# Operation 3: Promote Boundary Candidate
# ============================================================================

def promote_boundary(
    candidate: BoundaryCandidate,
    evidence_type: str,
    evidence_data: Dict[str, Any]
) -> OperationResult:
    """
    Promote boundary candidate rank based on evidence.

    Rank progression: ZERO → CANDIDATE → HYPOTHESIS → STRONG_HYPOTHESIS → CERTIFICATE

    Args:
        candidate: Candidate to promote
        evidence_type: Type of evidence (lexicon, pattern, context)
        evidence_data: Evidence data

    Returns:
        OperationResult with promoted candidate
    """
    current_rank = candidate.rank
    residuals: List[BoundaryResidual] = []
    evidence: Dict[str, Any] = {
        'evidence_type': evidence_type,
        'evidence_data': evidence_data,
        'operation': 'promote_boundary'
    }

    # Determine new rank
    if evidence_type == 'lexicon_certificate':
        new_rank = BoundaryRank.BOUNDARY_CERTIFICATE
    elif evidence_type == 'strong_evidence':
        new_rank = BoundaryRank.BOUNDARY_STRONG_HYPOTHESIS
    elif evidence_type == 'hypothesis':
        new_rank = BoundaryRank.BOUNDARY_HYPOTHESIS
    else:
        # Insufficient evidence
        residuals.append(BoundaryResidual.INSUFFICIENT_EVIDENCE)
        new_rank = current_rank

    # Can't demote via promotion
    if new_rank.value < current_rank.value:
        new_rank = current_rank

    # Update candidate
    updated_candidate = BoundaryCandidate(
        segmentation=candidate.segmentation,
        rank=new_rank,
        residuals=candidate.residuals | frozenset(residuals),
        trace=candidate.trace,
        competitors=candidate.competitors,
        evidence={**candidate.evidence, **evidence},
        id=candidate.id
    )

    status = OperationStatus.WARNING if residuals else OperationStatus.SUCCESS
    return OperationResult(
        status=status,
        output=updated_candidate,
        residuals=residuals,
        evidence=evidence,
        message=f"Promoted from {current_rank.name} to {new_rank.name}"
    )


# ============================================================================
# Operation 4: Block Segmentation
# ============================================================================

def block_segmentation(
    candidate: BoundaryCandidate,
    reason: BoundaryResidual,
    blocking_evidence: Dict[str, Any]
) -> OperationResult:
    """
    Block a boundary segmentation candidate.

    Used when evidence shows segmentation is incorrect.

    Args:
        candidate: Candidate to block
        reason: Blocking residual
        blocking_evidence: Evidence for blocking

    Returns:
        OperationResult with blocked candidate
    """
    residuals = [reason]
    evidence: Dict[str, Any] = {
        'blocking_reason': reason.value,
        'blocking_evidence': blocking_evidence,
        'operation': 'block_segmentation'
    }

    # Create blocked candidate
    blocked_candidate = BoundaryCandidate(
        segmentation=candidate.segmentation,
        rank=BoundaryRank.BOUNDARY_BLOCKED,
        residuals=candidate.residuals | frozenset(residuals),
        trace=candidate.trace,
        competitors=candidate.competitors,
        evidence={**candidate.evidence, **evidence},
        id=candidate.id
    )

    return OperationResult(
        status=OperationStatus.BLOCKED,
        output=blocked_candidate,
        residuals=residuals,
        evidence=evidence,
        message=f"Blocked segmentation: {reason.value}"
    )


# ============================================================================
# Operation 5: Preserve Competitors
# ============================================================================

def preserve_competitors(
    candidate: BoundaryCandidate,
    competitors: List[BoundaryCandidate]
) -> OperationResult:
    """
    Preserve competing segmentation hypotheses.

    Multiple segmentations may be valid until evidence resolves.

    Args:
        candidate: Primary candidate
        competitors: Competing candidates

    Returns:
        OperationResult with updated candidate
    """
    evidence: Dict[str, Any] = {
        'competitor_count': len(competitors),
        'operation': 'preserve_competitors'
    }

    # Update candidate with competitors
    updated_candidate = BoundaryCandidate(
        segmentation=candidate.segmentation,
        rank=candidate.rank,
        residuals=candidate.residuals,
        trace=candidate.trace,
        competitors=frozenset(competitors),
        evidence={**candidate.evidence, **evidence},
        id=candidate.id
    )

    return OperationResult(
        status=OperationStatus.SUCCESS,
        output=updated_candidate,
        evidence=evidence,
        message=f"Preserved {len(competitors)} competing segmentations"
    )


# ============================================================================
# Operation 6: Detach Clitic
# ============================================================================

def detach_clitic(
    unit: TrueSingularLafz,
    host_unit: TrueSingularLafz
) -> OperationResult:
    """
    Detach a clitic from its host.

    Reverse operation of attachment.

    Args:
        unit: Clitic unit to detach
        host_unit: Host unit

    Returns:
        OperationResult with segmentation
    """
    residuals: List[BoundaryResidual] = []
    evidence: Dict[str, Any] = {
        'clitic': unit.surface,
        'host': host_unit.surface,
        'operation': 'detach_clitic'
    }

    # Check if unit is detachable
    if not unit.detachable:
        residuals.append(BoundaryResidual.CLITIC_MISIDENTIFIED_AS_PATTERN)
        return OperationResult(
            status=OperationStatus.BLOCKED,
            residuals=residuals,
            evidence=evidence,
            message=f"Unit {unit.surface} is not detachable"
        )

    # Build segmentation with separated units
    units = [unit, host_unit]
    seg_type = BoundarySegmentationType.PROCLITIC_CORE_ENCLITIC if \
                unit.attachment_type == AttachmentType.PROCLITIC else \
                BoundarySegmentationType.COMPLEX_SEGMENTATION

    # Combine surfaces
    combined_surface = unit.surface + host_unit.surface if \
                       unit.attachment_type == AttachmentType.PROCLITIC else \
                       host_unit.surface + unit.surface

    written_token = WrittenCompositeToken(
        surface=combined_surface,
        role_spans=unit.role_spans
    )

    segmentation = BoundarySegmentation(
        written_token=written_token,
        units=tuple(units),
        segmentation_type=seg_type,
        trace=unit.role_spans,
        residuals=frozenset(residuals),
        rank=BoundaryRank.BOUNDARY_HYPOTHESIS,
        evidence=evidence
    )

    candidate = BoundaryCandidate(
        segmentation=segmentation,
        rank=BoundaryRank.BOUNDARY_HYPOTHESIS,
        residuals=frozenset(residuals),
        trace=unit.role_spans,
        evidence=evidence
    )

    return OperationResult(
        status=OperationStatus.SUCCESS,
        output=candidate,
        residuals=residuals,
        evidence=evidence,
        message=f"Detached {unit.surface} from {host_unit.surface}"
    )
