"""
Residual Taxonomy for Rational Method

Residuals that may occur in rational operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RationalResidualKind(Enum):
    """Categories of residuals in rational operations."""

    # Missing pillars
    MISSING_REALITY = "missing_reality"
    MISSING_SENSORY_TRANSFER = "missing_sensory_transfer"
    MISSING_COGNITIVE_CARRIER = "missing_cognitive_carrier"
    MISSING_PRIOR_INFORMATION = "missing_prior_information"

    # Prior contamination
    PRIOR_OPINION_DETECTED = "prior_opinion_detected"
    PRIOR_OPINION_CONTAMINATION_RISK = "prior_opinion_contamination_risk"
    INVALID_PRIOR_INFORMATION = "invalid_prior_information"

    # Judgment issues
    PREDICATE_RANK_UNCERTAIN = "predicate_rank_uncertain"
    EXISTENCE_PREDICATE_CONFUSION = "existence_predicate_confusion"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"

    # Trace issues
    TRACE_INCOMPLETE = "trace_incomplete"
    TRACE_BROKEN = "trace_broken"


@dataclass(frozen=True)
class RationalResidual:
    """
    A residual from rational method operation.

    Residuals represent unresolved aspects, uncertainties, or
    constraints that must be preserved and tracked.
    """
    kind: RationalResidualKind
    description: str
    severity: str = "medium"  # "low", "medium", "high", "blocker"

    def is_blocker(self) -> bool:
        """Check if this residual blocks rational operation."""
        return self.severity == "blocker"

    def __str__(self) -> str:
        return f"[{self.kind.value}] {self.description}"
