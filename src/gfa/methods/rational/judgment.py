"""
AqlJudgment - Governed Judgment Result

Nabhani Principle:
    وجود الشيء المحسوس قطعي
    حقيقة الشيء أو صفته ظنية

    Existence of sensed thing is certain (قطعي)
    Reality/attribute of thing is probable (ظني)

Critical Law:
    Existence rank does not certify predicate rank.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple, FrozenSet
from uuid import uuid4


class ExistenceRank(Enum):
    """
    Rank of existence claim.

    QATI: Certain existence (محسوس قطعي)
    ZANNI: Probable existence (ظني)
    """
    QATI_EXISTENCE = "qati_existence"
    ZANNI_EXISTENCE = "zanni_existence"
    UNRESOLVED = "unresolved"


class PredicateRank(Enum):
    """
    Rank of predicate/attribute claim.

    Even if existence is certain, predicate remains probable
    until fully proven with residuals resolved.
    """
    CERTIFIED = "certified"  # Full proof, no residuals
    LICENSED = "licensed"    # Supported but with residuals
    ZANNI = "zanni"          # Probable
    CANDIDATE = "candidate"  # Proposed
    BLOCKED = "blocked"      # Contradicted
    UNRESOLVED = "unresolved"


@dataclass(frozen=True)
class AqlJudgment:
    """
    Governed judgment result from rational operation.

    Never a bare exception.
    Always preserves trace and residuals.

    Nabhani Law:
        Existence rank ≠ Predicate rank
        Seeing a thing ≠ Knowing its reality
    """
    claim: str
    existence_rank: ExistenceRank
    predicate_rank: PredicateRank
    evidence: Tuple[str, ...]
    residuals: Tuple[str, ...]
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    trace_lineage: Tuple[str, ...] = ()

    def is_valid(self) -> bool:
        """Check if judgment is valid (not blocked or unresolved)."""
        return self.predicate_rank not in (
            PredicateRank.BLOCKED,
            PredicateRank.UNRESOLVED
        )

    def has_residuals(self) -> bool:
        """Check if judgment has unresolved residuals."""
        return len(self.residuals) > 0

    def can_be_certified(self) -> bool:
        """
        Check if predicate can be certified.

        Requires:
        - Valid judgment
        - No residuals
        - At least LICENSED rank
        """
        return (
            self.is_valid() and
            not self.has_residuals() and
            self.predicate_rank in (PredicateRank.LICENSED, PredicateRank.CERTIFIED)
        )

    def existence_does_not_certify_predicate(self) -> bool:
        """
        Nabhani Law verification:
            رأيت شيئاً ≠ عرفت حقيقته

        Even if existence is QATI, predicate may be ZANNI.
        """
        if self.existence_rank == ExistenceRank.QATI_EXISTENCE:
            # Predicate should not auto-certify
            return self.predicate_rank != PredicateRank.CERTIFIED or not self.has_residuals()
        return True


@dataclass(frozen=True)
class AqlJudgmentFailure:
    """
    Governed failure (not bare exception).

    Represents failed rational operation with preserved trace.
    """
    reason: str
    missing_pillars: Tuple[str, ...]
    residuals: Tuple[str, ...]
    trace_id: str = field(default_factory=lambda: uuid4().hex)

    def __str__(self) -> str:
        return f"AqlJudgment failed: {self.reason} (missing: {', '.join(self.missing_pillars)})"
