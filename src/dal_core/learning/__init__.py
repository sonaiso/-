"""
Learning Module (التعلم المقيد)

Constrained learning that ranks but doesn't create.

Theorem 6: التعلم لا يرفع الرتبة
ML ranks candidates but cannot create atoms, sama', tawatur, or wad'.
"""

from typing import List, Tuple
from dal_core.d_form import FormCandidate


def rank_vocalization_candidates(
    unvocalized: str,
    candidates: List[FormCandidate]
) -> List[Tuple[FormCandidate, float]]:
    """
    Rank vocalization candidates.

    PERMITTED: Ordering existing candidates by likelihood.
    FORBIDDEN: Creating new atoms or raising attestation rank.

    Returns list of (candidate, score) tuples sorted by score.
    """
    # Stub implementation
    return [(c, 1.0) for c in candidates]
