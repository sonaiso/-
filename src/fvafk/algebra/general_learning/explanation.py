"""Explanation: Explain why rules were modified, promoted, or demoted.

Core Principle:
    كل تغيير في القاعدة يجب أن يُفسَّر.
    "Every change in a rule must be explained."

Central Law:
    لا ترقية ولا تخفيض بلا تفسير.
    "No promotion and no demotion without explanation."

Architecture:
    An **Explanation** is a structured justification that:
    1. Describes WHAT changed (modification, rank change, status change)
    2. Explains WHY it changed (trigger, evidence, counterexamples)
    3. Shows WHAT was learned (new constraints, scope refinements)
    4. Tracks WHO made the change (human, learner, verifier)
    5. Preserves provenance (trace, timestamp)

    Explanation Types:
    - **Rank Promotion**: Why rank increased
    - **Rank Demotion**: Why rank decreased
    - **Scope Refinement**: Why scope narrowed or broadened
    - **Manaat Change**: Why determining factor changed
    - **Exception Added**: Why exception was noted
    - **Rule Deprecated**: Why rule was replaced

Example (فاعل Pattern):
    Modification:
        Before: "All فاعل → agentive"
        After: "فاعل → agentive OR qualitative (based on root semantics)"

    Explanation:
        Type: SCOPE_REFINEMENT
        Trigger: "3 counterexamples found (طاهر، حامض، بارد)"
        Reasoning: "Original rule over-generalized; pattern licenses
                    both agentive AND qualitative interpretations"
        Evidence: "طاهر from state root → qualitative, not agentive"
        Learned: "Root semantics (event vs. state) determines interpretation"
        Confidence: 0.85
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Tuple, Mapping, Any
from datetime import datetime, timezone

from fvafk.algebra import Evidence, Residual, Rank, Trace


# ===========================================================================
# Explanation Kinds
# ===========================================================================


class ExplanationKind(Enum):
    """Types of explanations for rule changes.

    Each kind represents a different type of change that requires explanation.
    """

    RANK_PROMOTION = auto()         # ترقية الرتبة
    RANK_DEMOTION = auto()          # تخفيض الرتبة
    SCOPE_REFINEMENT = auto()       # تحسين النطاق
    SCOPE_NARROWING = auto()        # تضييق النطاق
    SCOPE_BROADENING = auto()       # توسيع النطاق
    MANAAT_CHANGE = auto()          # تغيير المناط
    EXCEPTION_ADDED = auto()        # إضافة استثناء
    RULE_DEPRECATED = auto()        # إهمال القاعدة
    RULE_REPLACED = auto()          # استبدال القاعدة
    CONFIDENCE_INCREASED = auto()   # زيادة الثقة
    CONFIDENCE_DECREASED = auto()   # نقص الثقة


# ===========================================================================
# Explanation
# ===========================================================================


@dataclass(frozen=True)
class Explanation:
    """A structured justification for a rule change.

    Attributes:
        kind: Type of explanation.
        what_changed: Description of what changed.
        why_changed: Explanation of why it changed.
        trigger: What triggered the change (counterexample, new evidence, etc.).
        evidence: Evidence supporting the change.
        residuals: Residuals introduced by the change.
        learned: What was learned from this change.
        confidence: Confidence in this explanation [0.0, 1.0].
        actor: Who/what made the change (human, learner, verifier).
        trace: Provenance trace.
        timestamp: When the change was made.
        metadata: Additional information.

    Example:
        >>> explanation = Explanation(
        ...     kind=ExplanationKind.SCOPE_REFINEMENT,
        ...     what_changed="Rule scope narrowed from 'all فاعل' to 'event-root فاعل'",
        ...     why_changed="Original rule over-generalized to qualitative interpretations",
        ...     trigger="3 counterexamples: طاهر، حامض، بارد",
        ...     learned="Root semantics (event vs. state) determines interpretation",
        ...     confidence=0.85,
        ...     actor="general_learner",
        ... )
        >>> explanation.kind
        <ExplanationKind.SCOPE_REFINEMENT: 3>
    """

    kind: ExplanationKind
    what_changed: str
    why_changed: str
    trigger: str = ""
    evidence: Tuple[Evidence, ...] = ()
    residuals: Tuple[Residual, ...] = ()
    learned: str = ""
    confidence: float = 0.7
    actor: str = "general_learner"
    trace: Trace = field(default_factory=lambda: Trace(operation="explanation"))
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.what_changed:
            raise ValueError("Explanation.what_changed must be non-empty")
        if not self.why_changed:
            raise ValueError("Explanation.why_changed must be non-empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Explanation.confidence must be in [0.0, 1.0]")

    @property
    def is_confident(self) -> bool:
        """Check if explanation has high confidence (≥ 0.7)."""
        return self.confidence >= 0.7

    @property
    def is_promotion(self) -> bool:
        """Check if this explains a rank promotion."""
        return self.kind in {
            ExplanationKind.RANK_PROMOTION,
            ExplanationKind.CONFIDENCE_INCREASED,
        }

    @property
    def is_demotion(self) -> bool:
        """Check if this explains a rank demotion."""
        return self.kind in {
            ExplanationKind.RANK_DEMOTION,
            ExplanationKind.CONFIDENCE_DECREASED,
        }

    @property
    def is_refinement(self) -> bool:
        """Check if this explains a refinement."""
        return self.kind in {
            ExplanationKind.SCOPE_REFINEMENT,
            ExplanationKind.SCOPE_NARROWING,
            ExplanationKind.SCOPE_BROADENING,
            ExplanationKind.MANAAT_CHANGE,
        }

    def to_readable(self) -> str:
        """Convert to human-readable explanation text.

        Returns:
            Multi-line formatted explanation.
        """
        lines = [
            f"### Explanation: {self.kind.name}",
            f"",
            f"**What changed:** {self.what_changed}",
            f"**Why changed:** {self.why_changed}",
        ]

        if self.trigger:
            lines.append(f"**Trigger:** {self.trigger}")

        if self.learned:
            lines.append(f"**Learned:** {self.learned}")

        lines.append(f"**Confidence:** {self.confidence:.2f}")
        lines.append(f"**Actor:** {self.actor}")
        lines.append(f"**Timestamp:** {self.timestamp}")

        if self.evidence:
            lines.append(f"**Evidence:** {len(self.evidence)} item(s)")

        if self.residuals:
            lines.append(f"**Residuals:** {len(self.residuals)} item(s)")

        return "\n".join(lines)


# ===========================================================================
# Explanation Construction
# ===========================================================================


def explain_modification(
    modification: Any,  # Should be RuleModification but avoiding circular import
    kind: ExplanationKind | None = None,
    learned: str = "",
    confidence: float = 0.7,
) -> Explanation:
    """Create an explanation from a rule modification.

    Args:
        modification: The RuleModification to explain.
        kind: Explanation kind (auto-detected if None).
        learned: What was learned (optional).
        confidence: Confidence in explanation.

    Returns:
        Explanation instance.

    Example:
        >>> from fvafk.algebra.general_learning import RuleModification
        >>> mod = RuleModification(
        ...     modification_type="scope_refinement",
        ...     before_description="All فاعل → agentive",
        ...     after_description="فاعل from event roots → agentive",
        ...     trigger="Counterexample: طاهر",
        ... )
        >>> explanation = explain_modification(mod, learned="Root semantics matter")
        >>> explanation.kind
        <ExplanationKind.SCOPE_REFINEMENT: 3>
    """
    # Auto-detect kind from modification type
    if kind is None:
        mod_type_raw = getattr(modification, "modification_type", "")

        # Handle RefinementPolicy enum
        if hasattr(mod_type_raw, "name"):  # It's an enum
            mod_type_name = mod_type_raw.name.lower()
            if "scope_narrowing" in mod_type_name:
                kind = ExplanationKind.SCOPE_NARROWING
            elif "scope_broadening" in mod_type_name:
                kind = ExplanationKind.SCOPE_BROADENING
            elif "manaat" in mod_type_name:
                kind = ExplanationKind.MANAAT_CHANGE
            elif "exception" in mod_type_name:
                kind = ExplanationKind.EXCEPTION_ADDED
            elif "rank_demotion" in mod_type_name:
                kind = ExplanationKind.RANK_DEMOTION
            elif "rule_rejection" in mod_type_name:
                kind = ExplanationKind.RULE_DEPRECATED
            else:
                kind = ExplanationKind.SCOPE_REFINEMENT  # Default
        else:
            # Handle string (legacy)
            mod_type = mod_type_raw.lower() if isinstance(mod_type_raw, str) else ""
            if "scope" in mod_type and "narrow" in mod_type:
                kind = ExplanationKind.SCOPE_NARROWING
            elif "scope" in mod_type and "broad" in mod_type:
                kind = ExplanationKind.SCOPE_BROADENING
            elif "scope" in mod_type or "refine" in mod_type:
                kind = ExplanationKind.SCOPE_REFINEMENT
            elif "manaat" in mod_type:
                kind = ExplanationKind.MANAAT_CHANGE
            else:
                kind = ExplanationKind.SCOPE_REFINEMENT  # Default

    what_changed = f"{getattr(modification, 'before_description', '')} → {getattr(modification, 'after_description', '')}"
    why_changed = f"Modification type: {getattr(modification, 'modification_type', 'unknown')}"
    trigger = getattr(modification, "trigger", "")

    return Explanation(
        kind=kind,
        what_changed=what_changed,
        why_changed=why_changed,
        trigger=trigger,
        evidence=getattr(modification, "evidence", ()),
        residuals=getattr(modification, "residuals", ()),
        learned=learned,
        confidence=confidence,
        trace=getattr(modification, "trace", Trace(operation="explanation")),
    )


def explain_rank_change(
    before_rank: Rank,
    after_rank: Rank,
    trigger: str = "",
    evidence: Tuple[Evidence, ...] = (),
    learned: str = "",
) -> Explanation:
    """Create an explanation for a rank change.

    Args:
        before_rank: Rank before change.
        after_rank: Rank after change.
        trigger: What triggered the change.
        evidence: Supporting evidence.
        learned: What was learned.

    Returns:
        Explanation instance.

    Example:
        >>> explanation = explain_rank_change(
        ...     before_rank=Rank.CANDIDATE,
        ...     after_rank=Rank.LICENSED,
        ...     trigger="3 confirming examples found",
        ...     learned="Pattern is stable across examples",
        ... )
        >>> explanation.kind
        <ExplanationKind.RANK_PROMOTION: 1>
    """
    if after_rank > before_rank:
        kind = ExplanationKind.RANK_PROMOTION
        why = "Rank promoted due to additional evidence and verification"
    elif after_rank < before_rank:
        kind = ExplanationKind.RANK_DEMOTION
        why = "Rank demoted due to counterexamples or insufficient evidence"
    else:
        kind = ExplanationKind.CONFIDENCE_INCREASED
        why = "Rank unchanged but confidence increased"

    what = f"Rank changed: {before_rank.name} → {after_rank.name}"

    return Explanation(
        kind=kind,
        what_changed=what,
        why_changed=why,
        trigger=trigger,
        evidence=evidence,
        learned=learned,
        confidence=0.8 if after_rank > before_rank else 0.6,
    )


def explain_counterexample_handling(
    counterexample: Any,  # Should be Counterexample but avoiding circular import
    action_taken: str,
    learned: str = "",
) -> Explanation:
    """Create an explanation for how a counterexample was handled.

    Args:
        counterexample: The counterexample.
        action_taken: What action was taken (refinement, exception, etc.).
        learned: What was learned.

    Returns:
        Explanation instance.

    Example:
        >>> from fvafk.algebra.general_learning import Counterexample, CounterexampleKind
        >>> ce = Counterexample(
        ...     surface="طاهر",
        ...     pattern="فاعل",
        ...     expected="agentive",
        ...     actual="qualitative",
        ...     kind=CounterexampleKind.FALSE_POSITIVE,
        ... )
        >>> explanation = explain_counterexample_handling(
        ...     ce,
        ...     action_taken="Scope narrowed to event roots",
        ...     learned="Root semantics determine interpretation",
        ... )
        >>> explanation.kind
        <ExplanationKind.SCOPE_NARROWING: 4>
    """
    surface = getattr(counterexample, "surface", "")
    expected = getattr(counterexample, "expected", "")
    actual = getattr(counterexample, "actual", "")

    what = f"Counterexample handled: {surface} (expected {expected}, got {actual})"
    why = f"Action taken: {action_taken}"
    trigger = f"Counterexample: {surface}"

    # Determine kind from action
    if "narrow" in action_taken.lower():
        kind = ExplanationKind.SCOPE_NARROWING
    elif "broad" in action_taken.lower():
        kind = ExplanationKind.SCOPE_BROADENING
    elif "exception" in action_taken.lower():
        kind = ExplanationKind.EXCEPTION_ADDED
    else:
        kind = ExplanationKind.SCOPE_REFINEMENT

    return Explanation(
        kind=kind,
        what_changed=what,
        why_changed=why,
        trigger=trigger,
        evidence=getattr(counterexample, "evidence", ()),
        learned=learned,
        confidence=0.75,
    )


__all__ = [
    "ExplanationKind",
    "Explanation",
    "explain_modification",
    "explain_rank_change",
    "explain_counterexample_handling",
]
