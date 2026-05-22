"""
Prior Filter - عزل الرأي السابق عن المعلومة السابقة

Nabhani Core Principle:
    المعلومات السابقة ≠ الآراء السابقة

    Prior information interprets reality.
    Prior opinion imposes predetermined conclusions.

Critical Law:
    Prior opinion must be excluded from rational operations.
    Prior opinion cannot be used as prior information.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet, Any, Tuple
from uuid import uuid4


@dataclass(frozen=True)
class PriorInformation:
    """
    معلومة سابقة - Prior Information

    Valid prior information that can be used in rational operations.

    Characteristics:
    - Linked to reality or evidence
    - Has been validated (at least LICENSED rank)
    - Not a mere opinion or bias
    - Can interpret new sensory data
    """
    content: str
    domain: str
    rank: str  # "LICENSED", "CERTIFIED", etc.
    evidence_trace: str
    trace_id: str = field(default_factory=lambda: uuid4().hex)

    def is_valid_for_rational_operation(self) -> bool:
        """Check if this information is valid for use."""
        return self.rank in ("LICENSED", "CERTIFIED") and bool(self.content)


@dataclass(frozen=True)
class PriorOpinion:
    """
    رأي سابق - Prior Opinion

    Opinion, bias, or predetermined conclusion that must be excluded.

    Characteristics:
    - May impose conclusion rather than interpret
    - May contaminate rational operation
    - Must be excluded from AqlOperation
    - Becomes residual when detected
    """
    content: str
    opinion_type: str  # "bias", "assumption", "prejudgment", etc.
    contamination_risk: str
    trace_id: str = field(default_factory=lambda: uuid4().hex)

    def why_excluded(self) -> str:
        """Explain why this opinion is excluded."""
        return f"Prior opinion excluded: {self.opinion_type} - {self.contamination_risk}"


@dataclass(frozen=True)
class FilteredPrior:
    """
    Result of filtering prior knowledge.

    Separates valid prior information from opinions that must be excluded.
    """
    information: FrozenSet[PriorInformation]
    excluded_opinions: FrozenSet[PriorOpinion]
    filter_trace: str = field(default_factory=lambda: uuid4().hex)

    def has_valid_information(self) -> bool:
        """Check if there is any valid prior information."""
        return len(self.information) > 0

    def count_excluded(self) -> int:
        """Count how many opinions were excluded."""
        return len(self.excluded_opinions)

    def get_exclusion_residuals(self) -> Tuple[str, ...]:
        """Get residuals from excluded opinions."""
        return tuple(op.why_excluded() for op in self.excluded_opinions)


def filter_prior(
    prior_items: FrozenSet[Any],
) -> FilteredPrior:
    """
    Filter prior knowledge into information and opinions.

    Nabhani Law:
        Prior opinion must be excluded.
        Only prior information may enter rational operation.

    Args:
        prior_items: Mixed set of prior knowledge items

    Returns:
        FilteredPrior with separated information and excluded opinions
    """
    information_set = set()
    opinion_set = set()

    for item in prior_items:
        if isinstance(item, PriorInformation):
            if item.is_valid_for_rational_operation():
                information_set.add(item)
            else:
                # Invalid information becomes opinion-like exclusion
                opinion_set.add(
                    PriorOpinion(
                        content=item.content,
                        opinion_type="invalid_information",
                        contamination_risk="insufficient_rank_or_evidence"
                    )
                )
        elif isinstance(item, PriorOpinion):
            opinion_set.add(item)
        else:
            # Unknown items treated as opinions (safer)
            opinion_set.add(
                PriorOpinion(
                    content=str(item),
                    opinion_type="untyped_prior",
                    contamination_risk="unvalidated_assumption"
                )
            )

    return FilteredPrior(
        information=frozenset(information_set),
        excluded_opinions=frozenset(opinion_set)
    )
