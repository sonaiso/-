"""
RankPolicy - سياسة الرتبة

Defines how ranks (existence and predicate) are managed in each domain.

Nabhani Core Principle:
    الوجود لا يثبت الحكم
    Existence does not prove predicate.

Critical Laws:
    1. Existence rank ≠ Predicate rank
    2. No rank inflation without proper evidence
    3. Domain determines valid rank transitions
    4. ZANNI → CERTIFIED requires specific evidence
    5. Rank policy does NOT issue judgment
    6. Rank policy only declares rules

Position:
    RankPolicy is declaration layer, not execution layer.
    RankPolicy does NOT certify claims.
    RankPolicy does NOT raise ranks.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .domain_spec import ThinkingDomain
from ..rational import PredicateRank, ExistenceRank


class RankTransition(Enum):
    """
    Allowed transitions between ranks.
    """

    # Existence rank transitions
    EXISTENCE_NONE_TO_POSSIBLE = "existence_none_to_possible"
    EXISTENCE_POSSIBLE_TO_CONFIRMED = "existence_possible_to_confirmed"

    # Predicate rank transitions
    PREDICATE_NONE_TO_ZANNI = "predicate_none_to_zanni"
    PREDICATE_ZANNI_TO_CERTIFIED = "predicate_zanni_to_certified"
    PREDICATE_CERTIFIED_TO_DECISIVE = "predicate_certified_to_decisive"

    # Forbidden transitions (for documentation)
    FORBIDDEN_EXISTENCE_TO_PREDICATE = "forbidden_existence_to_predicate"
    FORBIDDEN_SKIP_ZANNI = "forbidden_skip_zanni"


@dataclass(frozen=True)
class RankConstraint:
    """
    Constraint on rank transition.
    """
    from_rank: str  # Source rank
    to_rank: str  # Target rank
    allowed: bool  # Whether transition is allowed
    requires_evidence: bool  # Whether evidence is required
    reason: str  # Explanation


@dataclass(frozen=True)
class RankPolicy:
    """
    Policy governing rank assignments and transitions in a domain.

    RankPolicy declares what rank transitions are valid.
    It does NOT perform rank assignments.
    It does NOT certify claims.

    Critical Laws:
        - RankPolicy is domain-bound
        - RankPolicy does NOT raise ranks
        - RankPolicy does NOT convert ZANNI to CERTIFIED
        - RankPolicy only declares valid transitions
        - Actual rank assignment happens in judgment layer
    """
    domain: ThinkingDomain

    # Can this domain certify claims at all?
    allows_certification: bool

    # Can this domain reach decisive rank?
    allows_decisive: bool

    # Forbidden rank inflations
    forbids_existence_to_predicate: bool = True
    forbids_skip_zanni: bool = True

    def does_not_inflate(self, before: PredicateRank, after: PredicateRank) -> bool:
        """
        Check if rank transition is non-inflating.

        This is the key check for NeutralBinding compatibility.
        """
        rank_order = [
            PredicateRank.BLOCKED,
            PredicateRank.UNRESOLVED,
            PredicateRank.CANDIDATE,
            PredicateRank.ZANNI,
            PredicateRank.LICENSED,
            PredicateRank.CERTIFIED,
        ]

        try:
            before_idx = rank_order.index(before)
            after_idx = rank_order.index(after)
            return after_idx <= before_idx
        except ValueError:
            return False

    def allows_transition(
        self,
        from_rank: PredicateRank,
        to_rank: PredicateRank
    ) -> bool:
        """
        Check if transition from one rank to another is allowed.

        This is declaration only - does not perform transition.
        """
        # Cannot go backwards (demotion)
        if self.does_not_inflate(to_rank, from_rank):
            return False

        # CANDIDATE → ZANNI always allowed (initial claim)
        if from_rank == PredicateRank.CANDIDATE and to_rank == PredicateRank.ZANNI:
            return True

        # ZANNI → LICENSED/CERTIFIED requires certification capability
        if from_rank == PredicateRank.ZANNI and to_rank in (PredicateRank.LICENSED, PredicateRank.CERTIFIED):
            return self.allows_certification

        # LICENSED → CERTIFIED allowed if certification enabled
        if from_rank == PredicateRank.LICENSED and to_rank == PredicateRank.CERTIFIED:
            return self.allows_certification

        # CANDIDATE → CERTIFIED (skipping ZANNI)
        if from_rank == PredicateRank.CANDIDATE and to_rank == PredicateRank.CERTIFIED:
            return not self.forbids_skip_zanni and self.allows_certification

        # Unknown transition
        return False

    def blocks_existence_to_predicate_confusion(self) -> bool:
        """
        Check if policy blocks existence→predicate confusion.

        Critical for Nabhani principle: existence ≠ predicate.
        """
        return self.forbids_existence_to_predicate

    def get_max_rank(self) -> PredicateRank:
        """Get maximum rank achievable in this domain."""
        if self.allows_certification:
            return PredicateRank.CERTIFIED
        else:
            return PredicateRank.LICENSED


# Factory functions for domain-specific policies

def make_material_rank_policy() -> RankPolicy:
    """
    Create rank policy for material/experimental domain.

    Material domain can certify through repeated observation,
    but rarely reaches decisive (always subject to falsification).
    """
    return RankPolicy(
        domain=ThinkingDomain.MATERIAL_EXPERIMENTAL,
        allows_certification=True,
        allows_decisive=False,  # Scientific claims rarely decisive
        forbids_existence_to_predicate=True,
        forbids_skip_zanni=True,
    )


def make_formal_rank_policy() -> RankPolicy:
    """
    Create rank policy for formal/logical domain.

    Formal domain can reach decisive through proof.
    """
    return RankPolicy(
        domain=ThinkingDomain.FORMAL_LOGICAL,
        allows_certification=True,
        allows_decisive=True,  # Proofs can be decisive
        forbids_existence_to_predicate=True,
        forbids_skip_zanni=False,  # Can jump to decisive with proof
    )


def make_lafzi_rank_policy() -> RankPolicy:
    """
    Create rank policy for lafzi/dalali domain.

    This is DECLARATION ONLY.
    Actual LafziMadlul implementation is NOT part of this PR.

    Linguistic claims can be certified through وضع + استعمال.
    """
    return RankPolicy(
        domain=ThinkingDomain.LAFZI_DALALI,
        allows_certification=True,
        allows_decisive=False,  # Meaning rarely decisive
        forbids_existence_to_predicate=True,
        forbids_skip_zanni=True,
    )


def make_textual_rank_policy() -> RankPolicy:
    """
    Create rank policy for textual/normative domain.

    Textual claims can reach decisive with explicit نص.
    """
    return RankPolicy(
        domain=ThinkingDomain.TEXTUAL_NORMATIVE,
        allows_certification=True,
        allows_decisive=True,  # Explicit text can be decisive
        forbids_existence_to_predicate=True,
        forbids_skip_zanni=False,  # Can jump with explicit text
    )


def make_programming_rank_policy() -> RankPolicy:
    """
    Create rank policy for programming/execution domain.

    Execution can certify through type checking and successful runs.
    """
    return RankPolicy(
        domain=ThinkingDomain.PROGRAMMING_EXECUTION,
        allows_certification=True,
        allows_decisive=False,  # Execution rarely decisive (bugs possible)
        forbids_existence_to_predicate=True,
        forbids_skip_zanni=True,
    )
