"""
Algebraic Decision Core (النواة الجبرية للقرار)

Governance layer above ALL execution layers (U₀-Uₙ).

Purpose:
    Audit and control EVERY transition in the Arabic linguistic pipeline.
    Not a replacement for layers - a guardian ABOVE them.

Architecture Position:
    AlgebraicDecisionCore (this module)
        ├── IdentityRegistry
        ├── DomainRegistry
        ├── TransitionRegistry (to be implemented)
        ├── GateRegistry (to be implemented)
        ├── EvidenceRegistry (to be implemented)
        ├── RankPolicy (extends existing Rank)
        ├── ResidualGeometry (extends existing ResidualSet)
        ├── CPBIdentityGuardian (unified CPB)
        └── AppendixSystem (extensibility)

        ↓ (governs)

    U₀ → U₁ → U₂p → U₂s → U₃ → U₄ → U₅ → U₆ → U₇(A/B/C) → U₈ → U₉ → U₁₀+

Central Law (القانون المركزي):
    كل انتقال قرار.
    كل قرار له هوية.
    كل هوية لها مجال.
    كل مجال له دالة.
    كل دالة لها بوابة.
    كل بوابة لها دليل.
    كل دليل له رتبة.
    كل رتبة لها بقايا.
    والـ CPB يحرس ذلك كله.

    Every transition is a decision.
    Every decision has an identity.
    Every identity has a domain.
    Every domain has a function.
    Every function has a gate.
    Every gate has evidence.
    Every evidence has rank.
    Every rank has residuals.
    And CPB guards all of this.

Contract (العقد التنفيذي):
    Decision = {
        transition_id: str
        from_layer: ExecutionLayer
        to_layer: ExecutionLayer
        input_identity: IdentityType
        output_identity: IdentityType
        domain: DomainType
        function: str
        gate: str
        evidence: Tuple[Evidence, ...]
        rank: Rank
        residuals: Tuple[Residual, ...]
        trace: Tuple[str, ...]
        cpb_status: CPBStatus
    }

No output without Decision.
No Decision without CPB approval.

PR: ALGEBRAIC-DECISION-CORE
Created: 2026-05-26
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional, FrozenSet, Any, Dict
from uuid import uuid4

from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.identity_registry import (
    IdentityRegistry,
    IdentityType,
    verify_identity_preserved
)
from dal_core.domain_registry import (
    DomainRegistry,
    DomainType,
    verify_domain_boundary
)
from dal_core.foundation import Rank, ResidualSet
from dal_core.residuals import Residual


# ============================================================================
# CPB Status
# ============================================================================

class CPBStatus(Enum):
    """
    CPB (Completeness Predicate and Proof Builder) validation status.

    The unified guardian checks multiple dimensions before allowing transition.
    """
    APPROVED = "approved"                      # موافق - All checks passed
    IDENTITY_VIOLATION = "identity_violation"  # هوية منتهكة
    DOMAIN_VIOLATION = "domain_violation"      # مجال منتهك
    GATE_VIOLATION = "gate_violation"          # بوابة منتهكة
    EVIDENCE_INSUFFICIENT = "evidence_insufficient"  # دليل غير كافٍ
    RANK_VIOLATION = "rank_violation"          # رتبة منتهكة
    RESIDUAL_BLOCKING = "residual_blocking"    # بقايا معطلة
    TRACE_LOSS = "trace_loss"                  # أثر مفقود
    FORBIDDEN_LEAP = "forbidden_leap"          # قفزة ممنوعة


# ============================================================================
# Decision Audit Structure
# ============================================================================

@dataclass(frozen=True)
class DecisionAudit:
    """
    Complete audit record for one transition decision.

    This is the EVIDENCE that a transition was permitted (or blocked).

    Attributes:
        decision_id: Unique identifier for this decision
        transition_id: Identifier for the transition type
        from_layer: Source execution layer
        to_layer: Target execution layer
        input_identity: Identity before transition
        output_identity: Identity after transition
        domain: Domain where decision occurs
        function: Function being performed
        gate: Gate being passed through
        evidence: Evidence supporting decision
        rank: Rank assigned to output
        residuals: Residuals from decision
        trace: Execution trace
        cpb_status: CPB validation status
        allowed: Whether transition is allowed
        violations: List of violations (empty if allowed)
        timestamp: When decision was made
    """
    decision_id: str
    transition_id: str
    from_layer: ExecutionLayer
    to_layer: ExecutionLayer
    input_identity: IdentityType
    output_identity: IdentityType
    domain: DomainType
    function: str
    gate: str
    evidence: Tuple[str, ...]  # Evidence identifiers
    rank: Rank
    residuals: Tuple[Residual, ...]
    trace: Tuple[str, ...]
    cpb_status: CPBStatus
    allowed: bool
    violations: Tuple[str, ...] = tuple()
    timestamp: Optional[str] = None

    def is_approved(self) -> bool:
        """Check if decision was approved."""
        return self.allowed and self.cpb_status == CPBStatus.APPROVED

    def has_violations(self) -> bool:
        """Check if decision has violations."""
        return len(self.violations) > 0

    def get_blocking_residuals(self) -> Tuple[Residual, ...]:
        """Get residuals that block progression."""
        return tuple(r for r in self.residuals if r.is_blocker())


# ============================================================================
# CPB Identity Guardian - Unified Guardian Across All Layers
# ============================================================================

class CPBIdentityGuardian:
    """
    Unified CPB (Completeness Predicate and Proof Builder) guardian.

    Integrates individual layer CPBs (CPB₀, CPB₁, CPB₂s, ..., CPB₈, CPB₉)
    into a single governance system.

    Responsibilities:
        1. Identity preservation: Input identity → Output identity valid?
        2. Domain boundary: Operation within domain competency?
        3. Gate enforcement: Required gates passed?
        4. Evidence validation: Sufficient evidence provided?
        5. Rank consistency: Rank progression valid?
        6. Residual audit: Residuals tracked and blocking checked?
        7. Trace preservation: Execution trace maintained?
        8. Forbidden leap prevention: No layer skipping?

    The guardian does NOT replace layer-specific CPB implementations.
    It provides ADDITIONAL governance and coordination.
    """

    def __init__(
        self,
        identity_registry: IdentityRegistry,
        domain_registry: DomainRegistry
    ):
        """
        Initialize CPB Identity Guardian.

        Args:
            identity_registry: Identity classification system
            domain_registry: Domain boundary system
        """
        self.identity_registry = identity_registry
        self.domain_registry = domain_registry

    def verify_identity(
        self,
        input_identity: IdentityType,
        output_identity: IdentityType,
        existing_identities: FrozenSet[IdentityType]
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify identity preservation or valid transition.

        Law: Output identity must be same as input OR valid transition target.

        Args:
            input_identity: Identity before transition
            output_identity: Identity after transition
            existing_identities: Set of already-established identities

        Returns:
            (is_valid, reason) tuple
        """
        # First check basic preservation
        is_preserved, reason = verify_identity_preserved(
            input_identity,
            output_identity,
            self.identity_registry
        )

        if not is_preserved:
            return False, reason

        # Check transition validity with context
        can_transition, reason = self.identity_registry.can_transition(
            input_identity,
            output_identity,
            existing_identities
        )

        return can_transition, reason

    def verify_domain(
        self,
        domain: DomainType,
        attempted_determination: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify that determination respects domain boundaries.

        Law: No determination outside domain competency.

        Args:
            domain: Domain where determination is attempted
            attempted_determination: What is being determined

        Returns:
            (is_valid, reason) tuple
        """
        return verify_domain_boundary(
            domain,
            attempted_determination,
            self.domain_registry
        )

    def verify_gate(
        self,
        layer: ExecutionLayer,
        gate_name: str,
        gate_passed: bool
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify that required gate was passed.

        Law: No transition without gate passage.

        Args:
            layer: Execution layer
            gate_name: Name of gate
            gate_passed: Whether gate was passed

        Returns:
            (is_valid, reason) tuple
        """
        if not gate_passed:
            return False, f"Gate {gate_name} not passed at layer {layer.value}"

        return True, None

    def verify_evidence(
        self,
        evidence: Tuple[str, ...],
        required_evidence_types: FrozenSet[str]
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify that sufficient evidence is provided.

        Law: No rank elevation without evidence.

        Args:
            evidence: Evidence identifiers provided
            required_evidence_types: Evidence types required

        Returns:
            (is_valid, reason) tuple
        """
        provided_types = frozenset(evidence)

        if not required_evidence_types.issubset(provided_types):
            missing = required_evidence_types - provided_types
            return False, f"Missing required evidence: {', '.join(missing)}"

        return True, None

    def verify_rank(
        self,
        input_rank: Rank,
        output_rank: Rank
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify rank progression is valid.

        Law: Rank can only increase with evidence, cannot skip levels.

        Args:
            input_rank: Rank before transition
            output_rank: Rank after transition

        Returns:
            (is_valid, reason) tuple
        """
        if not input_rank.can_progress_to(output_rank):
            return False, f"Invalid rank progression: {input_rank} → {output_rank}"

        return True, None

    def verify_residuals(
        self,
        residual_set: ResidualSet
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify residuals are properly tracked and check for blockers.

        Law: Residuals must be tracked, blockers prevent progression.

        Args:
            residual_set: Set of residuals

        Returns:
            (is_valid, reason) tuple - False if blocking residuals exist
        """
        if residual_set.has_blocking():
            blocking_count = residual_set.count_blocking()
            return False, f"{blocking_count} blocking residual(s) present"

        return True, None

    def verify_no_forbidden_leap(
        self,
        from_layer: ExecutionLayer,
        to_layer: ExecutionLayer
    ) -> Tuple[bool, Optional[str]]:
        """
        Verify no forbidden layer jump.

        Law: Cannot skip required intermediate layers.

        Args:
            from_layer: Source layer
            to_layer: Target layer

        Returns:
            (is_valid, reason) tuple
        """
        # Import here to avoid circular dependency
        from dal_core.execution_layer_registry import (
            is_transition_allowed,
            get_forbidden_jump_reason
        )

        if not is_transition_allowed(from_layer, to_layer):
            reason = get_forbidden_jump_reason(from_layer, to_layer)
            if reason:
                return False, f"Forbidden leap: {reason}"
            return False, f"Invalid transition: {from_layer.value} → {to_layer.value}"

        return True, None

    def audit_decision(
        self,
        transition_id: str,
        from_layer: ExecutionLayer,
        to_layer: ExecutionLayer,
        input_identity: IdentityType,
        output_identity: IdentityType,
        existing_identities: FrozenSet[IdentityType],
        domain: DomainType,
        attempted_determination: str,
        gate_name: str,
        gate_passed: bool,
        evidence: Tuple[str, ...],
        required_evidence: FrozenSet[str],
        input_rank: Rank,
        output_rank: Rank,
        residual_set: ResidualSet,
        trace: Tuple[str, ...]
    ) -> DecisionAudit:
        """
        Perform complete audit of a transition decision.

        This is the MAIN ENTRY POINT for decision governance.

        Args:
            transition_id: Identifier for transition type
            from_layer: Source layer
            to_layer: Target layer
            input_identity: Identity before transition
            output_identity: Identity after transition
            existing_identities: Set of established identities
            domain: Domain of operation
            attempted_determination: What is being determined
            gate_name: Gate being passed
            gate_passed: Whether gate was passed
            evidence: Evidence provided
            required_evidence: Evidence required
            input_rank: Rank before transition
            output_rank: Rank after transition
            residual_set: Residuals from operation
            trace: Execution trace

        Returns:
            DecisionAudit with complete audit record
        """
        violations = []
        cpb_status = CPBStatus.APPROVED

        # 1. Verify identity
        identity_ok, identity_reason = self.verify_identity(
            input_identity, output_identity, existing_identities
        )
        if not identity_ok:
            violations.append(f"Identity: {identity_reason}")
            cpb_status = CPBStatus.IDENTITY_VIOLATION

        # 2. Verify domain
        domain_ok, domain_reason = self.verify_domain(
            domain, attempted_determination
        )
        if not domain_ok:
            violations.append(f"Domain: {domain_reason}")
            if cpb_status == CPBStatus.APPROVED:
                cpb_status = CPBStatus.DOMAIN_VIOLATION

        # 3. Verify gate
        gate_ok, gate_reason = self.verify_gate(
            to_layer, gate_name, gate_passed
        )
        if not gate_ok:
            violations.append(f"Gate: {gate_reason}")
            if cpb_status == CPBStatus.APPROVED:
                cpb_status = CPBStatus.GATE_VIOLATION

        # 4. Verify evidence
        evidence_ok, evidence_reason = self.verify_evidence(
            evidence, required_evidence
        )
        if not evidence_ok:
            violations.append(f"Evidence: {evidence_reason}")
            if cpb_status == CPBStatus.APPROVED:
                cpb_status = CPBStatus.EVIDENCE_INSUFFICIENT

        # 5. Verify rank
        rank_ok, rank_reason = self.verify_rank(input_rank, output_rank)
        if not rank_ok:
            violations.append(f"Rank: {rank_reason}")
            if cpb_status == CPBStatus.APPROVED:
                cpb_status = CPBStatus.RANK_VIOLATION

        # 6. Verify residuals
        residuals_ok, residuals_reason = self.verify_residuals(residual_set)
        if not residuals_ok:
            violations.append(f"Residuals: {residuals_reason}")
            if cpb_status == CPBStatus.APPROVED:
                cpb_status = CPBStatus.RESIDUAL_BLOCKING

        # 7. Verify trace (basic check - trace should not be empty)
        if not trace:
            violations.append("Trace: Empty trace not allowed")
            if cpb_status == CPBStatus.APPROVED:
                cpb_status = CPBStatus.TRACE_LOSS

        # 8. Verify no forbidden leap
        leap_ok, leap_reason = self.verify_no_forbidden_leap(
            from_layer, to_layer
        )
        if not leap_ok:
            violations.append(f"Forbidden leap: {leap_reason}")
            if cpb_status == CPBStatus.APPROVED:
                cpb_status = CPBStatus.FORBIDDEN_LEAP

        # Decision is allowed only if ALL checks pass
        allowed = len(violations) == 0

        return DecisionAudit(
            decision_id=str(uuid4()),
            transition_id=transition_id,
            from_layer=from_layer,
            to_layer=to_layer,
            input_identity=input_identity,
            output_identity=output_identity,
            domain=domain,
            function=attempted_determination,
            gate=gate_name,
            evidence=evidence,
            rank=output_rank,
            residuals=tuple(residual_set.active_residuals()),
            trace=trace,
            cpb_status=cpb_status,
            allowed=allowed,
            violations=tuple(violations)
        )


# ============================================================================
# Algebraic Decision Core - Main Governance System
# ============================================================================

class AlgebraicDecisionCore:
    """
    Governance layer above all execution layers (U₀-Uₙ).

    Responsibilities:
        - Audit every transition as a decision
        - Enforce identity preservation
        - Enforce domain boundaries
        - Coordinate gate enforcement
        - Validate evidence sufficiency
        - Track rank progression
        - Manage residual algebra
        - Prevent forbidden leaps

    This is NOT a replacement for execution layers.
    This is a GUARDIAN that ensures layers operate correctly.

    Usage:
        core = AlgebraicDecisionCore()
        audit = core.decide_transition(
            layer_id="U7C_to_U8",
            input_obj=u7c_output,
            proposed_output=u8_candidate
        )
        if audit.is_approved():
            # Proceed with transition
            pass
        else:
            # Handle violations
            for violation in audit.violations:
                handle_violation(violation)
    """

    def __init__(self):
        """Initialize Algebraic Decision Core with all registries."""
        self.identity_registry = IdentityRegistry()
        self.domain_registry = DomainRegistry()
        self.cpb = CPBIdentityGuardian(
            self.identity_registry,
            self.domain_registry
        )

    def decide_transition(
        self,
        transition_id: str,
        from_layer: ExecutionLayer,
        to_layer: ExecutionLayer,
        input_identity: IdentityType,
        output_identity: IdentityType,
        existing_identities: FrozenSet[IdentityType],
        domain: DomainType,
        attempted_determination: str,
        gate_name: str,
        gate_passed: bool,
        evidence: Tuple[str, ...],
        required_evidence: FrozenSet[str],
        input_rank: Rank,
        output_rank: Rank,
        residual_set: ResidualSet,
        trace: Tuple[str, ...]
    ) -> DecisionAudit:
        """
        Make a decision about whether a transition is allowed.

        This is the MAIN ENTRY POINT for the governance system.

        Every layer transition must call this function and respect its decision.

        Args:
            transition_id: Identifier for transition type
            from_layer: Source execution layer
            to_layer: Target execution layer
            input_identity: Identity before transition
            output_identity: Identity after transition
            existing_identities: Set of established identities
            domain: Domain of operation
            attempted_determination: What is being determined
            gate_name: Gate being passed
            gate_passed: Whether gate was passed
            evidence: Evidence provided
            required_evidence: Evidence required
            input_rank: Rank before
            output_rank: Rank after
            residual_set: Residuals
            trace: Execution trace

        Returns:
            DecisionAudit with complete audit and approval/rejection
        """
        return self.cpb.audit_decision(
            transition_id=transition_id,
            from_layer=from_layer,
            to_layer=to_layer,
            input_identity=input_identity,
            output_identity=output_identity,
            existing_identities=existing_identities,
            domain=domain,
            attempted_determination=attempted_determination,
            gate_name=gate_name,
            gate_passed=gate_passed,
            evidence=evidence,
            required_evidence=required_evidence,
            input_rank=input_rank,
            output_rank=output_rank,
            residual_set=residual_set,
            trace=trace
        )


__all__ = [
    "CPBStatus",
    "DecisionAudit",
    "CPBIdentityGuardian",
    "AlgebraicDecisionCore",
]
