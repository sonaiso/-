"""
Approved Transition Context (سياق الانتقال المُجاز)

Constitutional Contract:
    Layer does not own Governor.
    Governor owns Transition Permission.

This module provides the evidence structure that proves a transition
has been approved by AlgebraicDecisionCore.

Key Principle:
    U₉ (or any layer) should NEVER instantiate AlgebraicDecisionCore internally.

    Instead:
    - Pipeline/Orchestrator owns AlgebraicDecisionCore
    - Pipeline asks AlgebraicDecisionCore to approve transition
    - Layer receives ApprovedTransitionContext as proof
    - Layer MUST refuse execution without ApprovedTransitionContext

Architecture Pattern:
    Pipeline/Orchestrator
      → owns AlgebraicDecisionCore
      → asks: approve U₈→U₉ transition?
      → receives DecisionAudit
      → if approved: creates ApprovedTransitionContext
      → passes context to U₉
      → U₉ verifies context and executes

    NOT:
    U₉
      → creates AlgebraicDecisionCore()
      → approves itself
      → executes

    (This would make the guard inside the guarded - breaks constitutional meaning)

PR: ALGEBRAIC-DECISION-CORE
Created: 2026-05-26
"""

from dataclasses import dataclass
from typing import Tuple, FrozenSet

from dal_core.algebraic_decision_core import DecisionAudit, CPBStatus
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.identity_registry import IdentityType
from dal_core.domain_registry import DomainType
from dal_core.foundation import Rank
from dal_core.residuals import Residual


@dataclass(frozen=True)
class ApprovedTransitionContext:
    """
    سياق الانتقال المُجاز (Approved Transition Context)

    Evidence that AlgebraicDecisionCore approved a specific transition.

    Constitutional Law:
        No layer execution without ApprovedTransitionContext.
        No ApprovedTransitionContext without AlgebraicDecisionCore approval.
        No approval without 8-dimensional validation.

    The 8 Dimensions:
        1. Identity: Input → Output identity valid?
        2. Domain: Operation within competency?
        3. Gate: Required gates passed?
        4. Evidence: Sufficient evidence?
        5. Rank: Rank progression valid?
        6. Residuals: No blocking residuals?
        7. Trace: Execution trace preserved?
        8. No Leap: Sequential progression?

    Attributes:
        audit: Complete DecisionAudit from AlgebraicDecisionCore
        from_layer: Source layer (verified)
        to_layer: Target layer (verified)
        input_identity: Identity before transition (verified)
        output_identity: Identity after transition (verified)
        domain: Domain of operation (verified)
        allowed_determination: What the layer may determine
        trace: Execution trace (verified)
        existing_identities: All established identities up to this point
    """
    audit: DecisionAudit
    from_layer: ExecutionLayer
    to_layer: ExecutionLayer
    input_identity: IdentityType
    output_identity: IdentityType
    domain: DomainType
    allowed_determination: str
    trace: Tuple[str, ...]
    existing_identities: FrozenSet[IdentityType]

    def __post_init__(self):
        """Verify that this context is truly approved."""
        if not self.is_approved():
            raise ValueError(
                f"Cannot create ApprovedTransitionContext with unapproved audit. "
                f"CPB Status: {self.audit.cpb_status}, "
                f"Violations: {self.audit.violations}"
            )

        # Verify layer consistency
        if self.audit.from_layer != self.from_layer:
            raise ValueError(
                f"Audit from_layer {self.audit.from_layer} != context from_layer {self.from_layer}"
            )
        if self.audit.to_layer != self.to_layer:
            raise ValueError(
                f"Audit to_layer {self.audit.to_layer} != context to_layer {self.to_layer}"
            )

        # Verify identity consistency
        if self.audit.input_identity != self.input_identity:
            raise ValueError(
                f"Audit input_identity {self.audit.input_identity} != context input_identity {self.input_identity}"
            )
        if self.audit.output_identity != self.output_identity:
            raise ValueError(
                f"Audit output_identity {self.audit.output_identity} != context output_identity {self.output_identity}"
            )

    def is_approved(self) -> bool:
        """
        Check if audit is truly approved.

        Returns:
            True only if CPB status is APPROVED and no violations
        """
        return (
            self.audit.cpb_status == CPBStatus.APPROVED
            and self.audit.allowed
            and len(self.audit.violations) == 0
        )

    def get_decision_id(self) -> str:
        """Get the unique decision ID."""
        return self.audit.decision_id

    def get_transition_id(self) -> str:
        """Get the transition type ID."""
        return self.audit.transition_id

    def get_rank(self) -> Rank:
        """Get the approved rank for this transition."""
        return self.audit.rank

    def get_residuals(self) -> Tuple[Residual, ...]:
        """Get residuals from the transition."""
        return self.audit.residuals

    def get_evidence(self) -> Tuple[str, ...]:
        """Get evidence that supported this approval."""
        return self.audit.evidence

    def has_blocking_residuals(self) -> bool:
        """
        Check if there are blocking residuals.

        Note: Should always be False for approved context,
        but provided for completeness.
        """
        return len(self.audit.get_blocking_residuals()) > 0

    def __str__(self) -> str:
        return (
            f"ApprovedTransition({self.from_layer.value}→{self.to_layer.value}, "
            f"{self.input_identity.value}→{self.output_identity.value}, "
            f"domain={self.domain.value}, "
            f"decision_id={self.audit.decision_id[:8]}...)"
        )

    def __repr__(self) -> str:
        return self.__str__()


def create_approved_context(
    audit: DecisionAudit,
    existing_identities: FrozenSet[IdentityType]
) -> ApprovedTransitionContext:
    """
    Create ApprovedTransitionContext from DecisionAudit.

    This is the ONLY way to create ApprovedTransitionContext.

    Args:
        audit: DecisionAudit from AlgebraicDecisionCore.decide_transition()
        existing_identities: Set of all established identities

    Returns:
        ApprovedTransitionContext if audit is approved

    Raises:
        ValueError: If audit is not approved

    Usage:
        core = AlgebraicDecisionCore()
        audit = core.decide_transition(...)

        if audit.is_approved():
            context = create_approved_context(audit, existing_identities)
            u9_output = transition_to_u9(u8_input, context)
        else:
            handle_violations(audit.violations)
    """
    if not audit.is_approved():
        raise ValueError(
            f"Cannot create ApprovedTransitionContext from unapproved audit. "
            f"CPB Status: {audit.cpb_status}, "
            f"Violations: {audit.violations}"
        )

    return ApprovedTransitionContext(
        audit=audit,
        from_layer=audit.from_layer,
        to_layer=audit.to_layer,
        input_identity=audit.input_identity,
        output_identity=audit.output_identity,
        domain=audit.domain,
        allowed_determination=audit.function,
        trace=audit.trace,
        existing_identities=existing_identities
    )


__all__ = [
    "ApprovedTransitionContext",
    "create_approved_context",
]
