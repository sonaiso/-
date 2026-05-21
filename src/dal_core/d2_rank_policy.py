"""D2 Rank Policy (RankPolicy_D2).

Multi-dimensional ranking for pre-morphological unit candidates.

Replaces simple confidence score with structured rank vector.

RankVector_D2 captures:
- Segmentation simplicity (fewer segments preferred)
- Clitic detection confidence
- Augmentation pattern consistency
- Frozen word attestation quality
- Functional particle attestation quality
- Syllable preservation quality
- Cross-candidate discriminability

Critical: D2 ranking is INDEPENDENT from D1 ranking.
High rank ≠ correctness. Certification comes from ProofObject_D2.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List


@dataclass
class PreMorphRankVector:
    """Multi-dimensional rank for pre-morphological unit candidate.

    Each dimension in [0.0, 1.0].
    Higher values = better quality.

    Independent from D1's SyllableRankVector.
    """
    segmentation_simplicity: float = 1.0        # Fewer segments = simpler (1.0 = simplest)
    clitic_confidence: float = 1.0              # Confidence in clitic detection
    augmentation_consistency: float = 1.0       # Augmentation pattern consistency
    frozen_word_attestation: float = 0.0        # Frozen word lexicon attestation (0.0 = not frozen)
    particle_attestation: float = 0.0           # Particle lexicon attestation (0.0 = not particle)
    syllable_preservation: float = 1.0          # Quality of syllable preservation
    candidate_discriminability: float = 1.0     # How well this candidate discriminates from others

    def __post_init__(self):
        """Validate rank vector."""
        fields = [
            ('segmentation_simplicity', self.segmentation_simplicity),
            ('clitic_confidence', self.clitic_confidence),
            ('augmentation_consistency', self.augmentation_consistency),
            ('frozen_word_attestation', self.frozen_word_attestation),
            ('particle_attestation', self.particle_attestation),
            ('syllable_preservation', self.syllable_preservation),
            ('candidate_discriminability', self.candidate_discriminability)
        ]

        for name, value in fields:
            if not (0.0 <= value <= 1.0):
                raise ValueError(f"{name} must be in [0.0, 1.0], got {value}")

    def total_rank(self, weights: Optional[Dict[str, float]] = None) -> float:
        """Weighted sum of rank components.

        Args:
            weights: Optional custom weights. If None, uses default weights.

        Returns:
            Total rank score [0.0, 1.0]
        """
        if weights is None:
            weights = DEFAULT_D2_RANK_WEIGHTS

        total = sum(
            getattr(self, k, 0.0) * v
            for k, v in weights.items()
        )

        # Clamp to [0.0, 1.0]
        return max(0.0, min(1.0, total))

    def as_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            'segmentation_simplicity': self.segmentation_simplicity,
            'clitic_confidence': self.clitic_confidence,
            'augmentation_consistency': self.augmentation_consistency,
            'frozen_word_attestation': self.frozen_word_attestation,
            'particle_attestation': self.particle_attestation,
            'syllable_preservation': self.syllable_preservation,
            'candidate_discriminability': self.candidate_discriminability,
            'total': self.total_rank()
        }

    def __str__(self) -> str:
        """Human-readable rank vector."""
        return (
            f"Rank(seg={self.segmentation_simplicity:.2f}, "
            f"clitic={self.clitic_confidence:.2f}, "
            f"preservation={self.syllable_preservation:.2f}, "
            f"total={self.total_rank():.2f})"
        )


# Default weights for D2 rank components
DEFAULT_D2_RANK_WEIGHTS = {
    'segmentation_simplicity': 0.20,        # 20% - Prefer simpler segmentations
    'clitic_confidence': 0.20,              # 20% - Clitic detection quality
    'augmentation_consistency': 0.15,       # 15% - Augmentation pattern quality
    'frozen_word_attestation': 0.15,        # 15% - Frozen word lexicon support
    'particle_attestation': 0.10,           # 10% - Particle lexicon support
    'syllable_preservation': 0.15,          # 15% - Syllable conservation quality
    'candidate_discriminability': 0.05      # 5% - Discriminability from competitors
}


# ============================================================================
# Rank Computation Functions
# ============================================================================


def compute_segmentation_simplicity(candidate) -> float:
    """Compute segmentation simplicity score.

    Simpler = fewer segments (prefer minimal segmentation).

    Args:
        candidate: PreMorphUnitCandidate

    Returns:
        Simplicity [0.0, 1.0], higher = simpler
    """
    if not hasattr(candidate, 'segmentation'):
        return 0.5  # Neutral

    seg = candidate.segmentation

    # Count segments
    segment_count = 0
    if hasattr(seg, 'proclitics') and seg.proclitics:
        segment_count += len(seg.proclitics)
    if hasattr(seg, 'core_syllables') and seg.core_syllables:
        segment_count += 1  # Core counts as 1 unit
    if hasattr(seg, 'enclitics') and seg.enclitics:
        segment_count += len(seg.enclitics)

    # Simplicity inversely proportional to segment count
    # 1 segment = 1.0, 2 = 0.8, 3 = 0.6, 4 = 0.4, 5+ = 0.2
    if segment_count == 1:
        return 1.0
    elif segment_count == 2:
        return 0.8
    elif segment_count == 3:
        return 0.6
    elif segment_count == 4:
        return 0.4
    else:
        return 0.2


def compute_clitic_confidence(candidate) -> float:
    """Compute clitic detection confidence.

    Args:
        candidate: PreMorphUnitCandidate

    Returns:
        Confidence [0.0, 1.0]
    """
    if not hasattr(candidate, 'segmentation'):
        return 1.0  # No clitics = no uncertainty

    seg = candidate.segmentation

    has_proclitics = hasattr(seg, 'proclitics') and seg.proclitics
    has_enclitics = hasattr(seg, 'enclitics') and seg.enclitics

    if not (has_proclitics or has_enclitics):
        return 1.0  # No clitics detected = high confidence

    # Check if clitics have attestation markers
    confidence = 1.0

    # Reduce confidence if clitics not attested
    # (In full implementation, would check lexicon)
    if has_proclitics:
        # For now, assume detected proclitics have moderate confidence
        confidence *= 0.8

    if has_enclitics:
        # For now, assume detected enclitics have moderate confidence
        confidence *= 0.8

    return confidence


def compute_augmentation_consistency(candidate) -> float:
    """Compute augmentation pattern consistency.

    Args:
        candidate: PreMorphUnitCandidate

    Returns:
        Consistency [0.0, 1.0]
    """
    if not hasattr(candidate, 'segmentation'):
        return 1.0  # No augmentation = consistent

    seg = candidate.segmentation

    has_augmentation = hasattr(seg, 'augmentation_markers') and seg.augmentation_markers

    if not has_augmentation:
        return 1.0  # No augmentation detected = consistent

    # For now, assume detected augmentation has moderate consistency
    # (Full implementation would validate against augmentation patterns)
    return 0.7


def compute_frozen_word_attestation(candidate) -> float:
    """Compute frozen word attestation score.

    Args:
        candidate: PreMorphUnitCandidate

    Returns:
        Attestation [0.0, 1.0], 0.0 = not frozen word
    """
    if not hasattr(candidate, 'segmentation'):
        return 0.0

    seg = candidate.segmentation

    is_frozen = hasattr(seg, 'is_frozen_word') and seg.is_frozen_word

    if not is_frozen:
        return 0.0

    # Check if attested in lexicon
    # (Full implementation would query frozen word lexicon)
    is_attested = hasattr(seg, 'frozen_word_attested') and seg.frozen_word_attested

    return 1.0 if is_attested else 0.3


def compute_particle_attestation(candidate) -> float:
    """Compute functional particle attestation score.

    Args:
        candidate: PreMorphUnitCandidate

    Returns:
        Attestation [0.0, 1.0], 0.0 = not particle
    """
    if not hasattr(candidate, 'segmentation'):
        return 0.0

    seg = candidate.segmentation

    is_particle = hasattr(seg, 'is_functional_particle') and seg.is_functional_particle

    if not is_particle:
        return 0.0

    # Check if attested in lexicon
    # (Full implementation would query particle lexicon)
    is_attested = hasattr(seg, 'particle_attested') and seg.particle_attested

    return 1.0 if is_attested else 0.3


def compute_syllable_preservation(candidate) -> float:
    """Compute syllable preservation quality.

    All syllables must be preserved with correct order.

    Args:
        candidate: PreMorphUnitCandidate

    Returns:
        Preservation quality [0.0, 1.0]
    """
    if not hasattr(candidate, 'source_syllables'):
        return 0.0

    expected_count = len(candidate.source_syllables)

    if not hasattr(candidate, 'segmentation'):
        return 0.0

    seg = candidate.segmentation

    # Count preserved syllables
    actual_count = 0
    if hasattr(seg, 'proclitics') and seg.proclitics:
        actual_count += len(seg.proclitics)
    if hasattr(seg, 'core_syllables') and seg.core_syllables:
        actual_count += len(seg.core_syllables)
    if hasattr(seg, 'enclitics') and seg.enclitics:
        actual_count += len(seg.enclitics)

    if actual_count == 0:
        return 0.0

    # Perfect preservation = 1.0
    if actual_count == expected_count:
        return 1.0

    # Partial preservation = ratio
    return min(1.0, actual_count / expected_count)


def compute_candidate_discriminability(
    candidate,
    competing_count: int = 1
) -> float:
    """Compute how well this candidate discriminates from competitors.

    Args:
        candidate: PreMorphUnitCandidate
        competing_count: Number of competing candidates

    Returns:
        Discriminability [0.0, 1.0]
    """
    if competing_count <= 1:
        return 1.0  # No competitors = high discriminability

    # More competitors = lower discriminability
    # 2 competitors = 0.8, 3 = 0.6, 4 = 0.4, 5+ = 0.2
    if competing_count == 2:
        return 0.8
    elif competing_count == 3:
        return 0.6
    elif competing_count == 4:
        return 0.4
    else:
        return 0.2


def compute_premorph_rank(
    candidate,
    context: Optional[Dict[str, any]] = None
) -> PreMorphRankVector:
    """Compute full rank vector for pre-morphological candidate.

    Args:
        candidate: PreMorphUnitCandidate
        context: Optional context with additional info:
            - competing_candidate_count: Number of competing candidates
            - is_reversible_verified: Whether reversibility was verified

    Returns:
        PreMorphRankVector with all dimensions computed
    """
    if context is None:
        context = {}

    competing_count = context.get('competing_candidate_count', 1)

    return PreMorphRankVector(
        segmentation_simplicity=compute_segmentation_simplicity(candidate),
        clitic_confidence=compute_clitic_confidence(candidate),
        augmentation_consistency=compute_augmentation_consistency(candidate),
        frozen_word_attestation=compute_frozen_word_attestation(candidate),
        particle_attestation=compute_particle_attestation(candidate),
        syllable_preservation=compute_syllable_preservation(candidate),
        candidate_discriminability=compute_candidate_discriminability(candidate, competing_count)
    )


# ============================================================================
# Rank Comparison Functions
# ============================================================================


def compare_ranks(rank1: PreMorphRankVector, rank2: PreMorphRankVector) -> int:
    """Compare two rank vectors.

    Args:
        rank1: First rank vector
        rank2: Second rank vector

    Returns:
        1 if rank1 > rank2, -1 if rank1 < rank2, 0 if equal
    """
    total1 = rank1.total_rank()
    total2 = rank2.total_rank()

    if total1 > total2:
        return 1
    elif total1 < total2:
        return -1
    else:
        return 0


def select_best_ranked(
    candidates: List,
    weights: Optional[Dict[str, float]] = None
) -> Optional[any]:
    """Select best-ranked candidate from list.

    Args:
        candidates: List of PreMorphUnitCandidate objects
        weights: Optional custom weights

    Returns:
        Best-ranked candidate, or None if list empty
    """
    if not candidates:
        return None

    best = None
    best_rank = -1.0

    for candidate in candidates:
        if hasattr(candidate, 'rank_vector') and candidate.rank_vector is not None:
            rank_total = candidate.rank_vector.total_rank(weights)
            if rank_total > best_rank:
                best_rank = rank_total
                best = candidate

    return best
