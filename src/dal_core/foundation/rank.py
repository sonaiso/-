"""
Rank Lattice - Shared epistemic rank system across all carrier layers.

Rank represents the epistemic status of linguistic claims across all layers.
It is NOT layer-specific - the same rank values apply to Unicode, Grapheme,
Syllable, Morpheme, and all higher layers.

Architecture:
    Rank lattice is general above layers, not Unicode-specific.
    Each layer can have its own rank, but uses the same Rank enum.

Progression:
    ZERO → CANDIDATE → HYPOTHESIS → STRONG_HYPOTHESIS → CERTIFICATE

    BLOCKED is a terminal failure state, not a higher rank.

Laws:
    - Rank can only increase with evidence
    - Rank cannot skip levels without intermediate evidence
    - BLOCKED terminates progression
    - Each layer maintains independent rank (tracked in RankVector)

PR: U0-STRICT-TYPE-SYSTEM (Foundation extraction)
Created: 2026-05-25
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict


class Rank(Enum):
    """
    Epistemic rank for linguistic claims across all carrier layers.

    Shared across:
        - U₀ (Unicode)
        - U₁ (Grapheme)
        - U₂p (Phonetic Projection)
        - U₂s (Syllable)
        - U₃ (Functional Roles)
        - U₄+ (Morpheme and higher)

    Progression:
        ZERO: No claim/classification
        CANDIDATE: Potential classification, minimal evidence
        HYPOTHESIS: Weak evidence supporting claim
        STRONG_HYPOTHESIS: Strong evidence, competing alternatives exist
        CERTIFICATE: Certified by policy/evidence, blockers resolved
        BLOCKED: Terminal failure, cannot progress

    Laws:
        - Rank monotonically increases with evidence (never decreases)
        - BLOCKED terminates progression
        - CERTIFICATE requires all competing alternatives blocked or resolved
    """
    ZERO = auto()                # No classification
    CANDIDATE = auto()           # Potential classification
    HYPOTHESIS = auto()          # Weak evidence
    STRONG_HYPOTHESIS = auto()   # Strong evidence
    CERTIFICATE = auto()         # Certified by policy
    BLOCKED = auto()             # Terminal failure

    def can_progress_to(self, target: 'Rank') -> bool:
        """
        Check if progression to target rank is permitted.

        Rules:
            - Cannot progress from BLOCKED
            - Cannot progress to ZERO (regression)
            - Cannot skip levels (must go through intermediate ranks)

        Constitutional Law:
            لا قفز رتبي - No rank skipping
            ZERO → CANDIDATE → HYPOTHESIS → STRONG_HYPOTHESIS → CERTIFICATE
            Each step requires evidence; no direct ZERO → CERTIFICATE
        """
        if self == Rank.BLOCKED:
            return False
        if target == Rank.ZERO:
            return False

        # Define progression order (excluding BLOCKED)
        order = [Rank.ZERO, Rank.CANDIDATE, Rank.HYPOTHESIS,
                 Rank.STRONG_HYPOTHESIS, Rank.CERTIFICATE]

        if target == Rank.BLOCKED:
            return True  # Can always fail

        try:
            current_idx = order.index(self)
            target_idx = order.index(target)

            # Can only progress forward, but no skipping
            # Must be same rank (allowed) or next rank only (progression by one step)
            if target_idx < current_idx:
                return False  # Cannot regress

            # Allow staying at same rank
            if target_idx == current_idx:
                return True

            # Allow progression to next rank only (no skipping)
            if target_idx == current_idx + 1:
                return True

            # Skipping ranks is forbidden
            return False
        except ValueError:
            return False

    def is_certified(self) -> bool:
        """Check if rank is CERTIFICATE."""
        return self == Rank.CERTIFICATE

    def is_blocked(self) -> bool:
        """Check if rank is BLOCKED."""
        return self == Rank.BLOCKED

    def is_at_least(self, minimum: 'Rank') -> bool:
        """Check if rank is at least the minimum level."""
        order = [Rank.ZERO, Rank.CANDIDATE, Rank.HYPOTHESIS,
                 Rank.STRONG_HYPOTHESIS, Rank.CERTIFICATE]
        try:
            return order.index(self) >= order.index(minimum)
        except ValueError:
            return False


@dataclass(frozen=True)
class RankVector:
    """
    Multi-layer rank tracking.

    Each layer maintains independent rank. A structure can have:
        - unicode_rank = CERTIFICATE
        - grapheme_rank = CERTIFICATE
        - syllable_rank = ZERO (not yet syllabified)
        - weight_rank = ZERO (no morphological analysis)
        - semantic_rank = ZERO (no semantic interpretation)

    Law:
        Higher layer rank cannot exceed lower layer rank.
        E.g., if unicode_rank = HYPOTHESIS, then grapheme_rank ≤ HYPOTHESIS

    This prevents:
        - Syllable certificate without Unicode/Grapheme certificate
        - Meaning certificate without Form certificate
        - Judgment without preceding evidence
    """
    unicode_rank: Rank = Rank.ZERO
    grapheme_rank: Rank = Rank.ZERO
    phonetic_rank: Rank = Rank.ZERO
    syllable_rank: Rank = Rank.ZERO
    functional_role_rank: Rank = Rank.ZERO
    morpheme_rank: Rank = Rank.ZERO
    stem_root_rank: Rank = Rank.ZERO
    pattern_weight_rank: Rank = Rank.ZERO
    semantic_rank: Rank = Rank.ZERO
    hukm_rank: Rank = Rank.ZERO

    def validate_consistency(self) -> bool:
        """
        Validate that rank vector is consistent.

        Higher layers cannot have higher rank than lower layers.
        """
        # Define layer ordering (lower → higher)
        layers = [
            self.unicode_rank,
            self.grapheme_rank,
            self.phonetic_rank,
            self.syllable_rank,
            self.functional_role_rank,
            self.morpheme_rank,
            self.stem_root_rank,
            self.pattern_weight_rank,
            self.semantic_rank,
            self.hukm_rank
        ]

        # Check that no higher layer exceeds lower layer
        order = [Rank.ZERO, Rank.CANDIDATE, Rank.HYPOTHESIS,
                 Rank.STRONG_HYPOTHESIS, Rank.CERTIFICATE]

        max_rank_so_far = Rank.ZERO
        for layer_rank in layers:
            if layer_rank == Rank.BLOCKED:
                continue  # BLOCKED doesn't participate in ordering

            if layer_rank in order:
                layer_idx = order.index(layer_rank)
                max_idx = order.index(max_rank_so_far)

                if layer_idx > max_idx:
                    # Higher layer has higher rank than previous layers
                    # This is invalid
                    return False

                # Update max
                if layer_idx >= max_idx:
                    max_rank_so_far = layer_rank

        return True

    def as_dict(self) -> Dict[str, Rank]:
        """Convert to dictionary for serialization."""
        return {
            "unicode_rank": self.unicode_rank,
            "grapheme_rank": self.grapheme_rank,
            "phonetic_rank": self.phonetic_rank,
            "syllable_rank": self.syllable_rank,
            "functional_role_rank": self.functional_role_rank,
            "morpheme_rank": self.morpheme_rank,
            "stem_root_rank": self.stem_root_rank,
            "pattern_weight_rank": self.pattern_weight_rank,
            "semantic_rank": self.semantic_rank,
            "hukm_rank": self.hukm_rank
        }
