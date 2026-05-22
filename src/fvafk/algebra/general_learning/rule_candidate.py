"""Rule Candidate: Learned rules with evidence, rank, and residuals.

Core Principle:
    القاعدة المتعلمة ليست مجرد نص؛ بل هي نتيجة محكومة.
    "A learned rule is not mere text; it is a governed result."

Central Law:
    كل قاعدة متعلمة يجب أن تحمل:
    - الأصول (origins)
    - الثوابت (invariants)
    - المناط (manaat/scope)
    - الأدلة (evidence)
    - البقايا (residuals)
    - الرتبة (rank)
    - الأثر (trace)

    "Every learned rule must carry:
    origins, invariants, manaat, evidence, residuals, rank, trace."

Architecture:
    A **RuleCandidate** is a hypothesis about a linguistic pattern that:
    1. Was learned from origin examples
    2. Has identified invariants
    3. Has a determined manaat (scope)
    4. Carries evidence and residuals
    5. Has an epistemic rank
    6. Can be refined/modified when counterexamples appear
    7. Preserves modification history

    Rules progress through statuses:
    - HYPOTHESIS → Initial extraction from origins
    - TESTED → Tested against examples
    - REFINED → Modified after counterexamples
    - STABLE → No recent modifications
    - DEPRECATED → Replaced by better rule
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum, auto
from typing import Tuple, Mapping, Any

from fvafk.algebra import Evidence, Residual, Rank, Trace


# ===========================================================================
# Rule Status
# ===========================================================================


class RuleStatus(Enum):
    """Status of a learned rule in its lifecycle.

    Rules evolve through these statuses as they are tested and refined.
    """

    HYPOTHESIS = auto()     # فرضية (initial extraction from origins)
    TESTED = auto()         # مختبرة (tested against examples)
    REFINED = auto()        # مُحسّنة (modified after counterexamples)
    STABLE = auto()         # مستقرة (no recent modifications)
    DEPRECATED = auto()     # مُهملة (replaced by better rule)


# ===========================================================================
# Rule Modification
# ===========================================================================


@dataclass(frozen=True)
class RuleModification:
    """A record of a single modification to a rule.

    Tracks what changed, why, and the evidence for the change.

    Attributes:
        modification_type: Type of modification (refinement, generalization, etc.).
        before_description: Rule description before modification.
        after_description: Rule description after modification.
        trigger: What triggered this modification (counterexample, new evidence, etc.).
        evidence: Evidence supporting this modification.
        residuals: New residuals introduced by this modification.
        trace: Provenance trace.

    Example:
        >>> mod = RuleModification(
        ...     modification_type="scope_refinement",
        ...     before_description="All فاعل → agentive",
        ...     after_description="فاعل from event roots → agentive potential",
        ...     trigger="Counterexample: طاهر (qualitative, not agentive)",
        ... )
        >>> mod.modification_type
        'scope_refinement'
    """

    modification_type: str
    before_description: str
    after_description: str
    trigger: str = ""
    evidence: Tuple[Evidence, ...] = ()
    residuals: Tuple[Residual, ...] = ()
    trace: Trace = field(default_factory=lambda: Trace(operation="rule_modification"))

    def __post_init__(self) -> None:
        if not self.modification_type:
            raise ValueError("RuleModification.modification_type must be non-empty")
        if not self.before_description:
            raise ValueError("RuleModification.before_description must be non-empty")
        if not self.after_description:
            raise ValueError("RuleModification.after_description must be non-empty")


# ===========================================================================
# Rule Candidate
# ===========================================================================


@dataclass(frozen=True)
class RuleCandidate:
    """A learned rule with full governance (evidence, rank, residuals, trace).

    A RuleCandidate embodies the constitution: every rule is a Result.

    Attributes:
        description: Human-readable rule description.
        pattern: The pattern this rule applies to (e.g., "فاعل").
        manaat: The scope/basis determining when rule applies.
        origins: The positive examples from which rule was extracted.
        invariants: The stable features detected.
        evidence: Supporting evidence for this rule.
        residuals: Unresolved aspects (ambiguity, exceptions).
        rank: Epistemic rank (CANDIDATE, LICENSED, CERTIFIED).
        status: Rule lifecycle status (HYPOTHESIS, TESTED, etc.).
        modifications: History of modifications to this rule.
        trace: Provenance trace.
        metadata: Additional information.

    Example:
        >>> from fvafk.algebra.general_learning import Origin, Manaat, ManaatScope
        >>> origin = Origin(surface="كاتب", pattern="فاعل", interpretation="agentive", rank=Rank.LICENSED)
        >>> manaat = Manaat(scope=ManaatScope.PATTERN_ONLY, positive_conditions=("pattern=فاعل",))
        >>> rule = RuleCandidate(
        ...     description="فاعل pattern licenses agentive interpretation",
        ...     pattern="فاعل",
        ...     manaat=manaat,
        ...     origins=(origin,),
        ...     rank=Rank.CANDIDATE,
        ...     status=RuleStatus.HYPOTHESIS,
        ... )
        >>> rule.pattern
        'فاعل'
        >>> rule.status
        <RuleStatus.HYPOTHESIS: 1>
    """

    description: str
    pattern: str
    manaat: Any  # Should be Manaat but avoiding circular import
    origins: Tuple[Any, ...] = ()  # Should be Tuple[Origin, ...] but avoiding circular import
    invariants: Tuple[Any, ...] = ()  # Should be Tuple[Invariant, ...] but avoiding circular import
    evidence: Tuple[Evidence, ...] = ()
    residuals: Tuple[Residual, ...] = ()
    rank: Rank = Rank.CANDIDATE
    status: RuleStatus = RuleStatus.HYPOTHESIS
    modifications: Tuple[RuleModification, ...] = ()
    trace: Trace = field(default_factory=lambda: Trace(operation="rule_extraction"))
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.description:
            raise ValueError("RuleCandidate.description must be non-empty")
        if not self.pattern:
            raise ValueError("RuleCandidate.pattern must be non-empty")

    @property
    def is_stable(self) -> bool:
        """Check if rule is stable (status is STABLE)."""
        return self.status is RuleStatus.STABLE

    @property
    def is_refined(self) -> bool:
        """Check if rule has been refined (has modifications)."""
        return bool(self.modifications)

    @property
    def is_certified(self) -> bool:
        """Check if rule has reached CERTIFIED rank."""
        return self.rank is Rank.CERTIFIED

    @property
    def modification_count(self) -> int:
        """Get number of modifications applied to this rule."""
        return len(self.modifications)

    @property
    def latest_modification(self) -> RuleModification | None:
        """Get the most recent modification (if any)."""
        return self.modifications[-1] if self.modifications else None

    def with_refinement(
        self,
        new_description: str,
        new_manaat: Any,  # Should be Manaat
        trigger: str = "",
        evidence: Tuple[Evidence, ...] = (),
        residuals: Tuple[Residual, ...] = (),
    ) -> "RuleCandidate":
        """Create a refined version of this rule.

        Args:
            new_description: Updated rule description.
            new_manaat: Updated manaat (scope/basis).
            trigger: What triggered this refinement.
            evidence: Evidence for the refinement.
            residuals: New residuals introduced.

        Returns:
            New RuleCandidate with refinement applied.

        Example:
            >>> rule = RuleCandidate(
            ...     description="All فاعل → agentive",
            ...     pattern="فاعل",
            ...     manaat=Manaat(scope=ManaatScope.PATTERN_ONLY),
            ...     rank=Rank.CANDIDATE,
            ...     status=RuleStatus.HYPOTHESIS,
            ... )
            >>> refined = rule.with_refinement(
            ...     new_description="فاعل from event roots → agentive potential",
            ...     new_manaat=Manaat(scope=ManaatScope.PATTERN_WITH_ROOT),
            ...     trigger="Counterexample: طاهر",
            ... )
            >>> refined.status
            <RuleStatus.REFINED: 3>
        """
        modification = RuleModification(
            modification_type="scope_refinement",
            before_description=self.description,
            after_description=new_description,
            trigger=trigger,
            evidence=evidence,
            residuals=residuals,
            trace=self.trace.child("rule_refinement"),
        )

        return replace(
            self,
            description=new_description,
            manaat=new_manaat,
            evidence=self.evidence + evidence,
            residuals=self.residuals + residuals,
            status=RuleStatus.REFINED,
            modifications=self.modifications + (modification,),
            trace=self.trace.child("rule_refinement"),
        )

    def with_status(self, status: RuleStatus) -> "RuleCandidate":
        """Create a copy with updated status.

        Args:
            status: New rule status.

        Returns:
            New RuleCandidate with updated status.
        """
        return replace(self, status=status)

    def with_rank(self, rank: Rank) -> "RuleCandidate":
        """Create a copy with updated rank.

        Args:
            rank: New epistemic rank.

        Returns:
            New RuleCandidate with updated rank.
        """
        return replace(self, rank=rank)

    def with_evidence(self, *items: Evidence) -> "RuleCandidate":
        """Create a copy with additional evidence.

        Args:
            items: Evidence items to add.

        Returns:
            New RuleCandidate with additional evidence.
        """
        if not items:
            return self
        return replace(self, evidence=self.evidence + tuple(items))

    def with_residual(self, *items: Residual) -> "RuleCandidate":
        """Create a copy with additional residuals.

        Args:
            items: Residual items to add.

        Returns:
            New RuleCandidate with additional residuals.
        """
        if not items:
            return self
        return replace(self, residuals=self.residuals + tuple(items))

    def to_replay(self) -> Mapping[str, Any]:
        """Convert to replay-able dict for persistence/debugging.

        Returns:
            JSON-friendly dict representation.
        """
        return {
            "description": self.description,
            "pattern": self.pattern,
            "manaat": str(self.manaat),  # Simplified for replay
            "rank": self.rank.name,
            "status": self.status.name,
            "origin_count": len(self.origins),
            "invariant_count": len(self.invariants),
            "evidence_count": len(self.evidence),
            "residual_count": len(self.residuals),
            "modification_count": self.modification_count,
            "trace_id": self.trace.trace_id,
        }


# ===========================================================================
# Rule Candidate Construction
# ===========================================================================


def make_rule_candidate(
    description: str,
    pattern: str,
    manaat: Any,  # Should be Manaat
    origins: Tuple[Any, ...] = (),  # Should be Tuple[Origin, ...]
    invariants: Tuple[Any, ...] = (),  # Should be Tuple[Invariant, ...]
    evidence: Tuple[Evidence, ...] = (),
    residuals: Tuple[Residual, ...] = (),
    rank: Rank | None = None,
) -> RuleCandidate:
    """Construct a RuleCandidate with automatic rank determination.

    Args:
        description: Human-readable rule description.
        pattern: The pattern this rule applies to.
        manaat: The scope/basis for rule application.
        origins: Positive examples.
        invariants: Detected invariants.
        evidence: Supporting evidence.
        residuals: Unresolved aspects.
        rank: Epistemic rank (auto-determined if None).

    Returns:
        RuleCandidate instance.

    Example:
        >>> rule = make_rule_candidate(
        ...     description="فاعل pattern licenses agentive interpretation",
        ...     pattern="فاعل",
        ...     manaat=Manaat(scope=ManaatScope.PATTERN_ONLY),
        ... )
        >>> rule.rank
        <Rank.CANDIDATE: 1>
    """
    # Auto-determine rank if not provided
    if rank is None:
        if evidence and not residuals:
            rank = Rank.CERTIFIED
        elif evidence:
            rank = Rank.LICENSED
        else:
            rank = Rank.CANDIDATE

    return RuleCandidate(
        description=description,
        pattern=pattern,
        manaat=manaat,
        origins=origins,
        invariants=invariants,
        evidence=evidence,
        residuals=residuals,
        rank=rank,
        status=RuleStatus.HYPOTHESIS,
    )


__all__ = [
    "RuleStatus",
    "RuleModification",
    "RuleCandidate",
    "make_rule_candidate",
]
