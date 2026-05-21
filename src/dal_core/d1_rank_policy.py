"""D1 Rank Policy (RankPolicy_D1).

Multi-dimensional ranking for syllable candidates.

Replaces simple confidence score with structured rank vector.

RankVector_D1 captures:
- Pattern legality (is pattern legal?)
- Boundary confidence (how confident in boundaries?)
- Trace completeness (is trace complete/reversible?)
- Atom coverage (% of atoms included)
- Ambiguity penalty (penalty for ambiguity)
- Long vowel confidence (confidence in long vowel detection)
- Shadda/sukun handling (quality of special atom handling)
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from dal_core.syllables import SyllableType


@dataclass
class SyllableRankVector:
    """Multi-dimensional rank for syllable candidate.

    Each dimension in [0.0, 1.0].
    Higher values = better quality.
    """
    pattern_legality: float = 1.0           # Is pattern legal? (1.0 = yes, 0.0 = no)
    boundary_confidence: float = 1.0        # Confidence in boundaries
    trace_completeness: float = 1.0         # Is trace complete/reversible?
    atom_coverage: float = 1.0              # % of atoms included
    ambiguity_penalty: float = 0.0          # Penalty for ambiguity (0.0 = no penalty)
    long_vowel_confidence: float = 1.0      # Confidence in long vowel detection
    shadda_sukun_handling: float = 1.0      # Quality of special atom handling

    def __post_init__(self):
        """Validate rank vector."""
        fields = [
            ('pattern_legality', self.pattern_legality),
            ('boundary_confidence', self.boundary_confidence),
            ('trace_completeness', self.trace_completeness),
            ('atom_coverage', self.atom_coverage),
            ('ambiguity_penalty', self.ambiguity_penalty),
            ('long_vowel_confidence', self.long_vowel_confidence),
            ('shadda_sukun_handling', self.shadda_sukun_handling)
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
            weights = DEFAULT_RANK_WEIGHTS

        total = sum(
            getattr(self, k, 0.0) * v
            for k, v in weights.items()
        )

        # Subtract ambiguity penalty (it's negative)
        total -= self.ambiguity_penalty * weights.get('ambiguity_penalty', 0.10)

        # Clamp to [0.0, 1.0]
        return max(0.0, min(1.0, total))

    def as_dict(self) -> Dict[str, float]:
        """Convert to dictionary."""
        return {
            'pattern_legality': self.pattern_legality,
            'boundary_confidence': self.boundary_confidence,
            'trace_completeness': self.trace_completeness,
            'atom_coverage': self.atom_coverage,
            'ambiguity_penalty': self.ambiguity_penalty,
            'long_vowel_confidence': self.long_vowel_confidence,
            'shadda_sukun_handling': self.shadda_sukun_handling,
            'total': self.total_rank()
        }

    def __str__(self) -> str:
        """Human-readable rank vector."""
        return (
            f"Rank(pattern={self.pattern_legality:.2f}, "
            f"boundary={self.boundary_confidence:.2f}, "
            f"trace={self.trace_completeness:.2f}, "
            f"coverage={self.atom_coverage:.2f}, "
            f"total={self.total_rank():.2f})"
        )


# Default weights for rank components
DEFAULT_RANK_WEIGHTS = {
    'pattern_legality': 0.25,      # 25% - Most important
    'boundary_confidence': 0.20,   # 20%
    'trace_completeness': 0.15,    # 15%
    'atom_coverage': 0.15,         # 15%
    'ambiguity_penalty': 0.10,     # 10% (negative)
    'long_vowel_confidence': 0.10, # 10%
    'shadda_sukun_handling': 0.05  # 5%
}


# ============================================================================
# Rank Computation Functions
# ============================================================================


def compute_pattern_legality(syllable) -> float:
    """Compute pattern legality score.

    Args:
        syllable: Syllable object

    Returns:
        1.0 if legal pattern, 0.0 if illegal
    """
    legal_patterns = {
        SyllableType.CV,
        SyllableType.CVC,
        SyllableType.CVV,
        SyllableType.CVVC,
        SyllableType.CVCC
    }

    return 1.0 if syllable.type in legal_patterns else 0.0


def compute_boundary_confidence(
    syllable,
    has_competing_boundaries: bool = False,
    residual_count: int = 0
) -> float:
    """Compute boundary confidence score.

    Args:
        syllable: Syllable object
        has_competing_boundaries: Are there competing boundary interpretations?
        residual_count: Number of residuals related to boundaries

    Returns:
        Confidence [0.0, 1.0]
    """
    confidence = 1.0

    # Reduce if competing boundaries exist
    if has_competing_boundaries:
        confidence -= 0.3

    # Reduce based on residuals
    confidence -= min(0.4, residual_count * 0.1)

    return max(0.0, confidence)


def compute_trace_completeness(
    trace,
    is_reversible_verified: bool = False
) -> float:
    """Compute trace completeness score.

    Args:
        trace: DalTraceRef object
        is_reversible_verified: Has reversibility been verified (not just claimed)?

    Returns:
        Completeness [0.0, 1.0]
    """
    if trace is None:
        return 0.0

    if not trace.reversible:
        return 0.3  # Has trace but not reversible

    if is_reversible_verified:
        return 1.0  # Fully verified
    else:
        return 0.7  # Claimed but not verified


def compute_atom_coverage(
    source_atoms: List,
    span: tuple[int, int],
    syllable
) -> float:
    """Compute atom coverage score.

    Args:
        source_atoms: Source atoms in candidate
        span: Syllable span
        syllable: Syllable structure

    Returns:
        Coverage [0.0, 1.0]
    """
    expected_count = span[1] - span[0]
    if expected_count == 0:
        return 0.0

    # Count atoms in syllable structure
    actual_count = (
        len(syllable.onset) +
        len(syllable.nucleus) +
        len(syllable.coda)
    )

    coverage = actual_count / expected_count
    return min(1.0, coverage)  # Clamp to 1.0


def compute_ambiguity_penalty(
    competing_candidate_count: int = 1
) -> float:
    """Compute ambiguity penalty.

    Higher penalty for more competing candidates.

    Args:
        competing_candidate_count: Number of competing interpretations

    Returns:
        Penalty [0.0, 1.0], 0.0 = no ambiguity
    """
    if competing_candidate_count <= 1:
        return 0.0

    # Logarithmic penalty
    import math
    penalty = min(1.0, math.log(competing_candidate_count) / math.log(10))
    return penalty


def compute_long_vowel_confidence(
    syllable,
    has_long_vowel_uncertainty: bool = False
) -> float:
    """Compute long vowel confidence score.

    Args:
        syllable: Syllable object
        has_long_vowel_uncertainty: Is there uncertainty about long vowel?

    Returns:
        Confidence [0.0, 1.0]
    """
    # Long vowel patterns
    has_long_vowel = syllable.type in {
        SyllableType.CVV,
        SyllableType.CVVC
    }

    if not has_long_vowel:
        return 1.0  # No long vowel, no uncertainty

    if has_long_vowel_uncertainty:
        return 0.5  # Uncertain

    # Check nucleus length
    if len(syllable.nucleus) >= 2:
        return 1.0  # Clear long vowel
    else:
        return 0.6  # Marked as long but nucleus short


def compute_shadda_sukun_handling(
    source_atoms: List,
    residual_count: int = 0
) -> float:
    """Compute shadda/sukun handling quality.

    Args:
        source_atoms: Source atoms
        residual_count: Number of residuals related to shadda/sukun

    Returns:
        Handling quality [0.0, 1.0]
    """
    from dal_core.atoms import AtomKind

    # Count shadda/sukun atoms
    special_count = sum(
        1 for atom in source_atoms
        if atom.kind in {AtomKind.SUKUN, AtomKind.SHADDA}
    )

    if special_count == 0:
        return 1.0  # No special atoms to handle

    # Base quality
    quality = 1.0

    # Reduce based on residuals
    quality -= min(0.6, residual_count * 0.2)

    return max(0.0, quality)


def compute_syllable_rank(
    candidate,
    context: Optional[Dict] = None
) -> SyllableRankVector:
    """Compute full rank vector for syllable candidate.

    Args:
        candidate: SyllableCandidate object
        context: Optional context dict with:
            - has_competing_boundaries: bool
            - competing_candidate_count: int
            - has_long_vowel_uncertainty: bool
            - shadda_sukun_residual_count: int
            - is_reversible_verified: bool

    Returns:
        SyllableRankVector
    """
    if context is None:
        context = {}

    # Count residuals related to boundaries
    boundary_residuals = sum(
        1 for r in candidate.residuals
        if 'boundary' in str(r).lower()
    )

    # Count shadda/sukun residuals
    shadda_sukun_residuals = context.get('shadda_sukun_residual_count', sum(
        1 for r in candidate.residuals
        if any(term in str(r).lower() for term in ['shadda', 'sukun'])
    ))

    return SyllableRankVector(
        pattern_legality=compute_pattern_legality(candidate.syllable),
        boundary_confidence=compute_boundary_confidence(
            candidate.syllable,
            has_competing_boundaries=context.get('has_competing_boundaries', False),
            residual_count=boundary_residuals
        ),
        trace_completeness=compute_trace_completeness(
            candidate.trace,
            is_reversible_verified=context.get('is_reversible_verified', False)
        ),
        atom_coverage=compute_atom_coverage(
            candidate.source_atoms,
            candidate.span,
            candidate.syllable
        ),
        ambiguity_penalty=compute_ambiguity_penalty(
            competing_candidate_count=context.get('competing_candidate_count', 1)
        ),
        long_vowel_confidence=compute_long_vowel_confidence(
            candidate.syllable,
            has_long_vowel_uncertainty=context.get('has_long_vowel_uncertainty', False)
        ),
        shadda_sukun_handling=compute_shadda_sukun_handling(
            candidate.source_atoms,
            residual_count=shadda_sukun_residuals
        )
    )


def rank_candidates(
    candidates: List,
    context: Optional[Dict] = None
) -> List[tuple[any, SyllableRankVector]]:
    """Rank multiple candidates.

    Args:
        candidates: List of SyllableCandidate objects
        context: Optional context for ranking

    Returns:
        List of (candidate, rank_vector) tuples, sorted by total rank (descending)
    """
    if context is None:
        context = {}

    # Add competing candidate count to context
    context['competing_candidate_count'] = len(candidates)

    # Compute rank for each
    ranked = [
        (candidate, compute_syllable_rank(candidate, context))
        for candidate in candidates
    ]

    # Sort by total rank (descending)
    ranked.sort(key=lambda x: x[1].total_rank(), reverse=True)

    return ranked


def best_candidate_by_rank(
    candidates: List,
    context: Optional[Dict] = None
):
    """Select best candidate by rank.

    Args:
        candidates: List of SyllableCandidate objects
        context: Optional context for ranking

    Returns:
        Best candidate (or None if empty list)
    """
    if not candidates:
        return None

    ranked = rank_candidates(candidates, context)
    return ranked[0][0]  # Return candidate from (candidate, rank) tuple


# ============================================================================
# Critical Law Enforcement
# ============================================================================


def rank_is_not_certificate(rank_vector: SyllableRankVector) -> bool:
    """Verify that rank ≠ certificate.

    High rank does NOT mean correct.
    Correctness must be verified separately via Corr_D1.

    Args:
        rank_vector: Rank vector to check

    Returns:
        True (always - this is a law, not a check)
    """
    # This function exists to document the law
    # Rank can be 1.0 but candidate still incorrect
    return True


def confidence_is_not_certificate(confidence: float) -> bool:
    """Verify that confidence ≠ certificate.

    Simple confidence score does NOT mean correct.

    Args:
        confidence: Confidence value

    Returns:
        True (always - this is a law, not a check)
    """
    # This function exists to document the law
    return True
