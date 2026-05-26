"""
Tests for ApprovedTransitionContext Security and Forgery Prevention

Constitutional Principle:
    ApprovedTransitionContext is transition-specific evidence,
    NOT a universal permission token.

Security Requirements:
    1. Cannot create context from unapproved audit
    2. Cannot use context for wrong from_layer
    3. Cannot use context for wrong to_layer
    4. Cannot use context for wrong input_identity
    5. Cannot use context for wrong output_identity
    6. Cannot use context for wrong domain
    7. Cannot create context without trace
    8. Cannot create context with blocking residuals
    9. Cannot create context with rank elevation without evidence
    10. U₉ must reject execution without ApprovedTransitionContext
    11. No layer should instantiate AlgebraicDecisionCore internally

PR: ALGEBRAIC-DECISION-CORE
Created: 2026-05-26
"""

import pytest
from unittest.mock import Mock

from dal_core.approved_transition_context import (
    ApprovedTransitionContext,
    create_approved_context,
)
from dal_core.algebraic_decision_core import (
    AlgebraicDecisionCore,
    CPBStatus,
    DecisionAudit,
)
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.identity_registry import IdentityType
from dal_core.domain_registry import DomainType
from dal_core.foundation import Rank
from dal_core.residuals import Residual, ResidualType, ResidualSeverity


class TestApprovedTransitionContextSecurity:
    """
    Test suite for ApprovedTransitionContext security.

    Ensures that ApprovedTransitionContext cannot be forged or misused
    as a universal bypass mechanism.
    """

    def create_mock_approved_audit(
        self,
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        domain=DomainType.WEIGHT_DOMAIN,
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=tuple(),
        trace=("u0_id", "u1_id", "u8_id"),
        residuals=tuple(),
        evidence=("root_candidate",),
        rank=Rank.CANDIDATE,
        input_rank=Rank.CANDIDATE,
    ):
        """Create mock approved DecisionAudit for testing."""
        audit = Mock(spec=DecisionAudit)
        audit.decision_id = "test_decision_123"
        audit.transition_id = "U8_to_U9"
        audit.from_layer = from_layer
        audit.to_layer = to_layer
        audit.input_identity = input_identity
        audit.output_identity = output_identity
        audit.domain = domain
        audit.function = "weight_pattern"
        audit.cpb_status = cpb_status
        audit.allowed = allowed
        audit.violations = violations
        audit.trace = trace
        audit.residuals = residuals
        audit.evidence = evidence
        audit.rank = rank
        audit.input_rank = input_rank

        # Mock methods
        audit.is_approved = Mock(return_value=(
            cpb_status == CPBStatus.APPROVED
            and allowed
            and len(violations) == 0
        ))
        audit.get_blocking_residuals = Mock(return_value=tuple([
            r for r in residuals
            if r.severity == ResidualSeverity.BLOCKING
        ]))

        return audit

    def test_approved_context_rejects_unapproved_audit(self):
        """
        Test 1: Cannot create ApprovedTransitionContext from unapproved audit.

        Security: Prevents forgery by requiring actual approval.
        """
        # Create unapproved audit
        unapproved_audit = self.create_mock_approved_audit(
            cpb_status=CPBStatus.IDENTITY_VIOLATION,
            allowed=False,
            violations=("Identity violation",)
        )

        # Attempt to create context should fail
        with pytest.raises(ValueError, match="unapproved audit"):
            create_approved_context(
                unapproved_audit,
                frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
            )

    def test_approved_context_rejects_wrong_from_layer(self):
        """
        Test 2: Cannot use context for wrong from_layer.

        Security: Prevents using U7→U8 approval for U8→U9 transition.
        """
        # Create approved audit for U8→U9
        audit = self.create_mock_approved_audit(
            from_layer=ExecutionLayer.U8_ROOT_STEM,
            to_layer=ExecutionLayer.U9_WEIGHT
        )

        # Attempt to create context with wrong from_layer
        with pytest.raises(ValueError, match="from_layer"):
            ApprovedTransitionContext(
                audit=audit,
                from_layer=ExecutionLayer.U7_PRE_WEIGHT,  # WRONG
                to_layer=ExecutionLayer.U9_WEIGHT,
                input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
                output_identity=IdentityType.WEIGHT_IDENTITY,
                domain=DomainType.WEIGHT_DOMAIN,
                allowed_determination="weight_pattern",
                trace=("u0", "u1", "u8"),
                existing_identities=frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
            )

    def test_approved_context_rejects_wrong_to_layer(self):
        """
        Test 3: Cannot use context for wrong to_layer.

        Security: Prevents using U8→U9 approval for U8→U10 transition.
        """
        audit = self.create_mock_approved_audit(
            from_layer=ExecutionLayer.U8_ROOT_STEM,
            to_layer=ExecutionLayer.U9_WEIGHT
        )

        with pytest.raises(ValueError, match="to_layer"):
            ApprovedTransitionContext(
                audit=audit,
                from_layer=ExecutionLayer.U8_ROOT_STEM,
                to_layer=ExecutionLayer.U10_SEMANTIC,  # WRONG
                input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
                output_identity=IdentityType.WEIGHT_IDENTITY,
                domain=DomainType.WEIGHT_DOMAIN,
                allowed_determination="weight_pattern",
                trace=("u0", "u1", "u8"),
                existing_identities=frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
            )

    def test_approved_context_rejects_wrong_output_identity(self):
        """
        Test 4: Cannot use context for wrong output_identity.

        Security: Prevents using WEIGHT_IDENTITY approval for SEMANTIC_IDENTITY.
        """
        audit = self.create_mock_approved_audit(
            output_identity=IdentityType.WEIGHT_IDENTITY
        )

        with pytest.raises(ValueError, match="output_identity"):
            ApprovedTransitionContext(
                audit=audit,
                from_layer=ExecutionLayer.U8_ROOT_STEM,
                to_layer=ExecutionLayer.U9_WEIGHT,
                input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
                output_identity=IdentityType.SEMANTIC_IDENTITY,  # WRONG
                domain=DomainType.WEIGHT_DOMAIN,
                allowed_determination="weight_pattern",
                trace=("u0", "u1", "u8"),
                existing_identities=frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
            )

    def test_approved_context_rejects_wrong_domain(self):
        """
        Test 5: Cannot use context for wrong domain.

        Security: Prevents using WEIGHT_DOMAIN approval for SEMANTIC_DOMAIN.
        Critical: صيغة فاعل ≠ معنى الفاعلية
        """
        audit = self.create_mock_approved_audit(
            domain=DomainType.WEIGHT_DOMAIN
        )

        with pytest.raises(ValueError, match="domain"):
            ApprovedTransitionContext(
                audit=audit,
                from_layer=ExecutionLayer.U8_ROOT_STEM,
                to_layer=ExecutionLayer.U9_WEIGHT,
                input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
                output_identity=IdentityType.WEIGHT_IDENTITY,
                domain=DomainType.SEMANTIC_DOMAIN,  # WRONG - violates domain boundary
                allowed_determination="meaning",
                trace=("u0", "u1", "u8"),
                existing_identities=frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
            )

    def test_approved_context_rejects_missing_trace(self):
        """
        Test 6: Cannot create context without execution trace.

        Security: Trace is required for constitutional governance.
        """
        audit = self.create_mock_approved_audit(
            trace=tuple()  # Empty trace
        )

        with pytest.raises(ValueError, match="trace"):
            ApprovedTransitionContext(
                audit=audit,
                from_layer=ExecutionLayer.U8_ROOT_STEM,
                to_layer=ExecutionLayer.U9_WEIGHT,
                input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
                output_identity=IdentityType.WEIGHT_IDENTITY,
                domain=DomainType.WEIGHT_DOMAIN,
                allowed_determination="weight_pattern",
                trace=tuple(),  # WRONG - no trace
                existing_identities=frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
            )

    def test_approved_context_rejects_blocking_residuals(self):
        """
        Test 7: Cannot create context with blocking residuals.

        Security: Blocked transitions cannot be approved.
        """
        blocking_residual = Residual(
            residual_id="blocking_1",
            residual_type=ResidualType.UNRESOLVED_AMBIGUITY,
            severity=ResidualSeverity.BLOCKING,
            description="Blocking ambiguity"
        )

        audit = self.create_mock_approved_audit(
            residuals=(blocking_residual,)
        )

        with pytest.raises(ValueError, match="blocking residuals"):
            ApprovedTransitionContext(
                audit=audit,
                from_layer=ExecutionLayer.U8_ROOT_STEM,
                to_layer=ExecutionLayer.U9_WEIGHT,
                input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
                output_identity=IdentityType.WEIGHT_IDENTITY,
                domain=DomainType.WEIGHT_DOMAIN,
                allowed_determination="weight_pattern",
                trace=("u0", "u1", "u8"),
                existing_identities=frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
            )

    def test_approved_context_accepts_valid_approval(self):
        """
        Test 8: GOLDEN PATH - Valid approved audit creates context successfully.

        Security: Proves that legitimate approvals work correctly.
        """
        audit = self.create_mock_approved_audit()

        # Should succeed
        context = create_approved_context(
            audit,
            frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
        )

        assert context.is_approved()
        assert context.from_layer == ExecutionLayer.U8_ROOT_STEM
        assert context.to_layer == ExecutionLayer.U9_WEIGHT
        assert context.input_identity == IdentityType.ROOT_MATERIAL_IDENTITY
        assert context.output_identity == IdentityType.WEIGHT_IDENTITY
        assert context.domain == DomainType.WEIGHT_DOMAIN
        assert len(context.trace) > 0
        assert not context.has_blocking_residuals()

    def test_approved_context_is_transition_specific(self):
        """
        Test 9: Context is transition-specific, not universal permission.

        Security: Each context is valid only for its specific transition.
        """
        # Create context for U8→U9
        audit_u8_u9 = self.create_mock_approved_audit(
            from_layer=ExecutionLayer.U8_ROOT_STEM,
            to_layer=ExecutionLayer.U9_WEIGHT
        )

        context = create_approved_context(
            audit_u8_u9,
            frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
        )

        # Verify context is specific to U8→U9
        assert context.from_layer == ExecutionLayer.U8_ROOT_STEM
        assert context.to_layer == ExecutionLayer.U9_WEIGHT
        assert context.get_transition_id() == "U8_to_U9"

        # This context CANNOT be used for U7→U8 or U9→U10
        # (enforced by layer checks in __post_init__)

    def test_factory_function_is_only_way_to_create_context(self):
        """
        Test 10: create_approved_context is the canonical way to create context.

        Security: Factory function enforces all validations.
        """
        audit = self.create_mock_approved_audit()

        # Factory function should work
        context = create_approved_context(
            audit,
            frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
        )

        assert context.is_approved()

        # Direct constructor also works but has same validations
        # (dataclass cannot be made truly private in Python)
        context2 = ApprovedTransitionContext(
            audit=audit,
            from_layer=audit.from_layer,
            to_layer=audit.to_layer,
            input_identity=audit.input_identity,
            output_identity=audit.output_identity,
            domain=audit.domain,
            allowed_determination=audit.function,
            trace=audit.trace,
            existing_identities=frozenset({IdentityType.ROOT_MATERIAL_IDENTITY})
        )

        assert context2.is_approved()


class TestU9ConstitutionalRequirements:
    """
    Tests proving U₉ follows constitutional governance pattern.

    These are integration-level tests that will require U₉ implementation.
    For now, they document the required behavior.
    """

    @pytest.mark.skip(reason="Requires U₉ implementation")
    def test_u9_rejects_execution_without_approved_context(self):
        """
        U₉ MUST reject execution without ApprovedTransitionContext.

        Constitutional Law:
            No U₉ execution without ApprovedTransitionContext.
        """
        # This test will be implemented when U₉ transition function exists
        pass

    @pytest.mark.skip(reason="Requires U₉ implementation")
    def test_u9_verifies_context_before_execution(self):
        """
        U₉ MUST verify context is approved before executing.

        Constitutional Law:
            Layer must verify context.is_approved() before proceeding.
        """
        pass

    @pytest.mark.skip(reason="Requires codebase scan")
    def test_no_layer_instantiates_algebraic_decision_core(self):
        """
        NO execution layer should instantiate AlgebraicDecisionCore internally.

        Constitutional Law:
            Layer does not own Governor.
            Only Pipeline/Orchestrator owns AlgebraicDecisionCore.

        Implementation:
            Scan all layer files (u0-u9) for AlgebraicDecisionCore()
            Should only appear in pipeline/orchestrator and tests.
        """
        pass

    @pytest.mark.skip(reason="Requires pipeline implementation")
    def test_pipeline_owns_governor_and_passes_context(self):
        """
        Pipeline/Orchestrator should own AlgebraicDecisionCore.

        Correct Pattern:
            pipeline.governor = AlgebraicDecisionCore()
            audit = pipeline.governor.decide_transition(...)
            context = create_approved_context(audit, ...)
            u9_output = transition_to_weight(u8_output, context)
        """
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
