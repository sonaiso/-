"""
Central Rank Enum - Unified Epistemic Ranking System

This module provides the canonical Rank enum used throughout the GFA project.

Critical Laws:
1. Rank must be typed enum, NOT string
2. Rank progression: ZERO < CANDIDATE < ZANNI < LICENSED < CERTIFIED
3. BLOCKED is a special state (not in progression)
4. Promotion requires evidence/trace preservation
5. Demotion preserves residuals

Usage:
    from gfa.governance.rank import Rank

    result.rank = Rank.CANDIDATE  # ✅ Correct
    result.rank = "CANDIDATE"     # ❌ FORBIDDEN - string not allowed
"""

from enum import Enum, auto


class Rank(Enum):
    """
    Epistemic rank of a unit, candidate, or result.

    Rank Progression (ascending):
    - ZERO: Null/empty state (non-admitted)
    - CANDIDATE: Proposed/candidate status (admitted but low confidence)
    - ZANNI: Probabilistic/conjectural (ظني)
    - LICENSED: Licensed by binding conditions (admitted with conditions)
    - CERTIFIED: Fully certified with audit trail

    Special States:
    - BLOCKED: Rejected/blocked (not in progression)

    Critical Law: Rank promotion requires:
    - Evidence preservation
    - Trace continuity
    - Residual tracking
    - No forbidden leaps (CANDIDATE → CERTIFIED requires intermediate steps)
    """

    ZERO = auto()           # Null state / non-admitted
    BLOCKED = auto()        # Rejected / blocked (special state)
    CANDIDATE = auto()      # Candidate / proposed
    ZANNI = auto()          # Conjectural / probabilistic (ظني)
    LICENSED = auto()       # Licensed by conditions
    CERTIFIED = auto()      # Fully certified with audit

    def can_promote_to(self, target: "Rank") -> bool:
        """
        Check if promotion to target rank is valid.

        Rules:
        1. Cannot promote from BLOCKED
        2. Cannot promote to ZERO (demotion only)
        3. Must follow progression order (no skipping)
        4. Can only promote upward
        """
        if self == Rank.BLOCKED:
            return False  # Cannot promote from blocked

        if target == Rank.ZERO:
            return False  # Cannot promote to ZERO

        if target == Rank.BLOCKED:
            return False  # Cannot promote to BLOCKED (blocking is separate action)

        rank_order = {
            Rank.ZERO: 0,
            Rank.CANDIDATE: 1,
            Rank.ZANNI: 2,
            Rank.LICENSED: 3,
            Rank.CERTIFIED: 4,
        }

        return rank_order.get(self, 0) < rank_order.get(target, 0)

    def can_demote_to(self, target: "Rank") -> bool:
        """
        Check if demotion to target rank is valid.

        Rules:
        1. Cannot demote to BLOCKED (blocking is separate action)
        2. Can demote to ZERO (removal)
        3. Must preserve residuals during demotion
        """
        if target == Rank.BLOCKED:
            return False  # Blocking is not demotion

        rank_order = {
            Rank.ZERO: 0,
            Rank.CANDIDATE: 1,
            Rank.ZANNI: 2,
            Rank.LICENSED: 3,
            Rank.CERTIFIED: 4,
        }

        return rank_order.get(self, 0) > rank_order.get(target, 0)

    @property
    def is_admitted(self) -> bool:
        """Check if rank represents admitted status."""
        return self in {Rank.CANDIDATE, Rank.ZANNI, Rank.LICENSED, Rank.CERTIFIED}

    @property
    def is_blocked(self) -> bool:
        """Check if rank is blocked."""
        return self == Rank.BLOCKED

    @property
    def is_certified(self) -> bool:
        """Check if rank is fully certified."""
        return self == Rank.CERTIFIED


# Backward compatibility - map strings to Rank enum
def rank_from_string(rank_str: str) -> Rank:
    """
    Convert string rank to Rank enum (for backward compatibility).

    WARNING: This function exists only for migration purposes.
    New code MUST use Rank enum directly.
    """
    mapping = {
        "ZERO": Rank.ZERO,
        "BLOCKED": Rank.BLOCKED,
        "CANDIDATE": Rank.CANDIDATE,
        "ZANNI": Rank.ZANNI,
        "LICENSED": Rank.LICENSED,
        "CERTIFIED": Rank.CERTIFIED,
    }

    rank_upper = rank_str.upper()
    if rank_upper not in mapping:
        raise ValueError(
            f"Unknown rank string: {rank_str}. "
            f"Valid values: {list(mapping.keys())}"
        )

    return mapping[rank_upper]


def rank_to_string(rank: Rank) -> str:
    """
    Convert Rank enum to string (for serialization/display).

    Use this ONLY for output/serialization, never for internal logic.
    """
    return rank.name


__all__ = [
    "Rank",
    "rank_from_string",
    "rank_to_string",
]
