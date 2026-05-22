"""
StyleValidator - مدقق الأسلوب

Validates style spec compliance and constraints.

Nabhani Core Principle:
    التدقيق يكشف المخالفات ولا يصلحها
    Validation reveals violations, does not fix them.

Critical Laws:
    1. Validator does NOT modify
    2. Validator does NOT execute
    3. Validator does NOT issue judgment
    4. Validator only checks and reports
    5. All violations preserved as residuals

Position:
    StyleValidator is checking layer, not execution layer.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .style_spec import StyleSpec
from .domain_spec import ThinkingDomain
from .operation_policy import OperationKind
from .residual_taxonomy import (
    StyleResidual,
    StyleResidualKind,
    make_domain_mismatch_residual,
    make_forbidden_domain_jump_residual,
    make_forbidden_operation_residual,
    make_style_spec_missing_residual,
    make_meta_violation_residual,
)


@dataclass(frozen=True)
class StyleValidationResult:
    """
    Result of style spec validation.

    Contains validation status and all residuals found.
    """

    # Is validation successful?
    success: bool

    # Style spec being validated (if present)
    style_spec: Optional[StyleSpec]

    # All residuals found during validation
    residuals: frozenset[StyleResidual] = field(default_factory=frozenset)

    # Specific violation categories (for quick checking)
    missing_components: frozenset[str] = field(default_factory=frozenset)
    meta_violations: frozenset[StyleResidual] = field(default_factory=frozenset)
    domain_violations: frozenset[StyleResidual] = field(default_factory=frozenset)
    policy_violations: frozenset[StyleResidual] = field(default_factory=frozenset)

    def is_failure(self) -> bool:
        """Check if validation failed."""
        return not self.success

    def has_blockers(self) -> bool:
        """Check if any residual is a blocker."""
        return any(r.is_blocker() for r in self.residuals)

    def has_meta_violations(self) -> bool:
        """Check if any meta-level violations exist."""
        return len(self.meta_violations) > 0

    def has_domain_violations(self) -> bool:
        """Check if any domain violations exist."""
        return len(self.domain_violations) > 0

    def get_blocker_residuals(self) -> frozenset[StyleResidual]:
        """Get all blocker residuals."""
        return frozenset(r for r in self.residuals if r.is_blocker())

    def __str__(self) -> str:
        if self.success:
            return "StyleValidation: SUCCESS"
        else:
            blockers = len(self.get_blocker_residuals())
            return f"StyleValidation: FAILURE ({blockers} blockers, {len(self.residuals)} total residuals)"


class StyleValidator:
    """
    Validator for style specifications.

    Checks StyleSpec compliance with critical laws.
    Does NOT modify or execute.
    Only validates and reports.
    """

    @staticmethod
    def validate_style_spec(style_spec: Optional[StyleSpec]) -> StyleValidationResult:
        """
        Validate a style spec.

        Checks:
        1. StyleSpec exists
        2. All required components present
        3. No meta violations
        4. Domain consistency
        """
        residuals: set[StyleResidual] = set()
        missing_components: set[str] = set()
        meta_violations: set[StyleResidual] = set()
        domain_violations: set[StyleResidual] = set()
        policy_violations: set[StyleResidual] = set()

        # Check 1: StyleSpec must exist
        if style_spec is None:
            residual = make_style_spec_missing_residual("entire_style_spec")
            residuals.add(residual)
            missing_components.add("style_spec")

            return StyleValidationResult(
                success=False,
                style_spec=None,
                residuals=frozenset(residuals),
                missing_components=frozenset(missing_components),
                meta_violations=frozenset(meta_violations),
                domain_violations=frozenset(domain_violations),
                policy_violations=frozenset(policy_violations),
            )

        # Check 2: All components must be present
        if style_spec.domain_spec is None:
            residual = make_style_spec_missing_residual("domain_spec")
            residuals.add(residual)
            missing_components.add("domain_spec")

        if style_spec.evidence_policy is None:
            residual = make_style_spec_missing_residual("evidence_policy")
            residuals.add(residual)
            missing_components.add("evidence_policy")

        if style_spec.rank_policy is None:
            residual = make_style_spec_missing_residual("rank_policy")
            residuals.add(residual)
            missing_components.add("rank_policy")

        if style_spec.residual_policy is None:
            residual = make_style_spec_missing_residual("residual_policy")
            residuals.add(residual)
            missing_components.add("residual_policy")

        if style_spec.operation_policy is None:
            residual = make_style_spec_missing_residual("operation_policy")
            residuals.add(residual)
            missing_components.add("operation_policy")

        # Check 3: Meta violations (architectural)
        # These are checked by construction in StyleSpec
        # But we document them here for completeness

        # StyleSpec is NOT RationalMethod (always true)
        if not style_spec.does_not_claim_to_be_rational_method():
            residual = make_meta_violation_residual(
                StyleResidualKind.STYLE_CLAIMS_TO_BE_RATIONAL_METHOD
            )
            residuals.add(residual)
            meta_violations.add(residual)

        # StyleSpec does NOT implement ScientificMethod (always true)
        if not style_spec.does_not_implement_scientific_method():
            residual = make_meta_violation_residual(
                StyleResidualKind.STYLE_IMPLEMENTS_SCIENTIFIC_METHOD
            )
            residuals.add(residual)
            meta_violations.add(residual)

        # StyleSpec does NOT implement LogicalStyle (always true)
        if not style_spec.does_not_implement_logical_style():
            residual = make_meta_violation_residual(
                StyleResidualKind.STYLE_IMPLEMENTS_LOGICAL_STYLE
            )
            residuals.add(residual)
            meta_violations.add(residual)

        # StyleSpec does NOT implement LafziMadlul (always true)
        if not style_spec.does_not_implement_lafzi_madlul():
            residual = make_meta_violation_residual(
                StyleResidualKind.STYLE_IMPLEMENTS_LAFZI_MADLUL
            )
            residuals.add(residual)
            meta_violations.add(residual)

        # Success if no residuals or only non-blocker residuals
        has_blockers = any(r.is_blocker() for r in residuals)
        success = not has_blockers and len(missing_components) == 0

        return StyleValidationResult(
            success=success,
            style_spec=style_spec,
            residuals=frozenset(residuals),
            missing_components=frozenset(missing_components),
            meta_violations=frozenset(meta_violations),
            domain_violations=frozenset(domain_violations),
            policy_violations=frozenset(policy_violations),
        )

    @staticmethod
    def validate_domain_match(
        style_spec: StyleSpec,
        expected_domain: ThinkingDomain
    ) -> StyleValidationResult:
        """
        Validate that style spec matches expected domain.

        Used when checking if style is appropriate for operation.
        """
        residuals: set[StyleResidual] = set()
        domain_violations: set[StyleResidual] = set()

        actual_domain = style_spec.get_domain()

        if actual_domain != expected_domain:
            residual = make_domain_mismatch_residual(
                expected_domain=expected_domain.value,
                actual_domain=actual_domain.value
            )
            residuals.add(residual)
            domain_violations.add(residual)

        success = len(residuals) == 0

        return StyleValidationResult(
            success=success,
            style_spec=style_spec,
            residuals=frozenset(residuals),
            domain_violations=frozenset(domain_violations),
        )

    @staticmethod
    def validate_operation_allowed(
        style_spec: StyleSpec,
        operation: OperationKind
    ) -> StyleValidationResult:
        """
        Validate that operation is allowed in style.

        Returns failure if operation is forbidden.
        """
        residuals: set[StyleResidual] = set()
        policy_violations: set[StyleResidual] = set()

        if style_spec.blocks_forbidden_operation(operation):
            forbidden_op = style_spec.operation_policy.get_forbidden_operation(operation)
            if forbidden_op:
                residual = make_forbidden_operation_residual(
                    operation=operation.value,
                    domain=style_spec.get_domain().value,
                    reason=forbidden_op.reason
                )
                residuals.add(residual)
                policy_violations.add(residual)

        success = len(residuals) == 0

        return StyleValidationResult(
            success=success,
            style_spec=style_spec,
            residuals=frozenset(residuals),
            policy_violations=frozenset(policy_violations),
        )

    @staticmethod
    def validate_domain_boundary(
        style_spec: StyleSpec,
        target_domain: ThinkingDomain
    ) -> StyleValidationResult:
        """
        Validate that domain boundary is preserved.

        Returns failure if attempting forbidden domain jump.
        """
        residuals: set[StyleResidual] = set()
        domain_violations: set[StyleResidual] = set()

        source_domain = style_spec.get_domain()

        # Same domain always OK
        if source_domain == target_domain:
            return StyleValidationResult(
                success=True,
                style_spec=style_spec,
            )

        # Different domain requires bridge (not implemented)
        if style_spec.preserves_domain_boundary(target_domain):
            residual = make_forbidden_domain_jump_residual(
                from_domain=source_domain.value,
                to_domain=target_domain.value
            )
            residuals.add(residual)
            domain_violations.add(residual)

        success = len(residuals) == 0

        return StyleValidationResult(
            success=success,
            style_spec=style_spec,
            residuals=frozenset(residuals),
            domain_violations=frozenset(domain_violations),
        )
