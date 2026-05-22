"""
StyleSpec - مواصفة الأسلوب

Every thinking style is a domain-specific specialization of RationalMethod.

Nabhani Core Principle:
    الأسلوب تخصيص للطريقة بحسب المجال
    Style is specialization of method by domain.

Critical Laws:
    1. No StyleSpec without DomainSpec
    2. No StyleSpec without EvidencePolicy
    3. No StyleSpec without RankPolicy
    4. No StyleSpec without ResidualPolicy
    5. No StyleSpec without allowed_operations
    6. No StyleSpec without forbidden_operations
    7. StyleSpec does NOT implement reasoning
    8. StyleSpec does NOT issue judgment
    9. StyleSpec does NOT certify claims
    10. StyleSpec is declaration and validation layer ONLY

Position in Architecture:
    RationalMethod (root)
    └── NeutralBinding (neutral element)
        └── StyleSpec (domain specialization)
            ├── ScientificMethod (future)
            ├── LogicalStyle (future)
            ├── LafziMadlul (future)
            └── ...

    StyleSpec is NOT:
    - RationalMethod (root)
    - ScientificMethod (experimental branch)
    - LogicalStyle (formal branch)
    - LafziMadlul (linguistic branch)
    - MeansAlgebra (tool layer)
    - Learning (update layer)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .domain_spec import DomainSpec, ThinkingDomain
from .evidence_policy import EvidencePolicy
from .rank_policy import RankPolicy
from .residual_policy import ResidualPolicy
from .operation_policy import OperationPolicy, OperationKind
from .residual_taxonomy import (
    StyleResidual,
    StyleResidualKind,
    make_style_spec_missing_residual,
    make_meta_violation_residual,
)


@dataclass(frozen=True)
class StyleSpec:
    """
    Complete specification of a thinking style.

    StyleSpec declares domain constraints and policies.
    StyleSpec does NOT execute reasoning.
    StyleSpec does NOT implement methods.

    Critical Laws:
        - StyleSpec requires all 5 components
        - StyleSpec is declaration only, not execution
        - StyleSpec does NOT issue judgment
        - StyleSpec does NOT certify claims
        - StyleSpec does NOT implement ScientificMethod
        - StyleSpec does NOT implement LogicalStyle
        - StyleSpec does NOT implement LafziMadlul
        - StyleSpec only declares and validates
    """

    # Required components
    domain_spec: DomainSpec
    evidence_policy: EvidencePolicy
    rank_policy: RankPolicy
    residual_policy: ResidualPolicy
    operation_policy: OperationPolicy

    # Metadata
    name_ar: str
    name_en: str
    description: str

    def __post_init__(self):
        """
        Validate StyleSpec construction.

        All 5 policies must match the same domain.
        """
        # Check required components are not None
        if self.domain_spec is None:
            raise ValueError("DomainSpec is required")

        if self.evidence_policy is None:
            raise ValueError("EvidencePolicy is required")

        if self.rank_policy is None:
            raise ValueError("RankPolicy is required")

        if self.residual_policy is None:
            raise ValueError("ResidualPolicy is required")

        if self.operation_policy is None:
            raise ValueError("OperationPolicy is required")

        domain = self.domain_spec.domain

        # Check all policies match domain
        if self.evidence_policy.domain != domain:
            raise ValueError(
                f"EvidencePolicy domain {self.evidence_policy.domain} "
                f"does not match DomainSpec {domain}"
            )

        if self.rank_policy.domain != domain:
            raise ValueError(
                f"RankPolicy domain {self.rank_policy.domain} "
                f"does not match DomainSpec {domain}"
            )

        if self.residual_policy.domain != domain:
            raise ValueError(
                f"ResidualPolicy domain {self.residual_policy.domain} "
                f"does not match DomainSpec {domain}"
            )

        if self.operation_policy.domain != domain:
            raise ValueError(
                f"OperationPolicy domain {self.operation_policy.domain} "
                f"does not match DomainSpec {domain}"
            )

    def get_domain(self) -> ThinkingDomain:
        """Get the domain of this style."""
        return self.domain_spec.domain

    def blocks_forbidden_operation(self, operation: OperationKind) -> bool:
        """
        Check if operation is forbidden and blocked.

        Returns True if operation should be blocked.
        """
        return self.operation_policy.forbids_operation(operation)

    def allows_operation(self, operation: OperationKind) -> bool:
        """Check if operation is allowed in this style."""
        return self.operation_policy.allows_operation(operation)

    def preserves_domain_boundary(self, target_domain: ThinkingDomain) -> bool:
        """
        Check if target domain respects boundary.

        Returns True if domain jump is blocked.
        """
        return self.domain_spec.blocks_domain_jump_to(target_domain)

    def does_not_claim_to_be_rational_method(self) -> bool:
        """
        StyleSpec is NOT RationalMethod.

        RationalMethod is the root.
        StyleSpec is domain specialization.
        """
        # This is always True by construction
        # StyleSpec ≠ RationalMethod
        return True

    def does_not_implement_scientific_method(self) -> bool:
        """
        StyleSpec does NOT implement ScientificMethod.

        ScientificMethod is a future specialized branch.
        This PR only declares domain/style framework.
        """
        # This is always True by construction
        # We are NOT implementing ScientificMethod in this PR
        return True

    def does_not_implement_logical_style(self) -> bool:
        """
        StyleSpec does NOT implement LogicalStyle.

        LogicalStyle is a future specialized branch.
        This PR only declares domain/style framework.
        """
        # This is always True by construction
        # We are NOT implementing LogicalStyle in this PR
        return True

    def does_not_implement_lafzi_madlul(self) -> bool:
        """
        StyleSpec does NOT implement LafziMadlul.

        LafziMadlul is a future specialized branch.
        This PR only declares domain/style framework.
        Declaration ≠ Implementation.
        """
        # This is always True by construction
        # We are NOT implementing LafziMadlul in this PR
        # We only declare LAFZI_DALALI domain
        return True

    def __str__(self) -> str:
        return f"StyleSpec[{self.get_domain().value}]: {self.name_en}"

    def __repr__(self) -> str:
        return (
            f"StyleSpec(domain={self.get_domain().value}, "
            f"name_en='{self.name_en}', "
            f"name_ar='{self.name_ar}')"
        )


# Factory functions for creating style specs

def make_material_experimental_style() -> StyleSpec:
    """
    Create MaterialExperimental style specification.

    This is DECLARATION ONLY.
    ScientificMethod implementation is NOT part of this PR.
    """
    from .domain_spec import make_material_experimental_domain
    from .evidence_policy import make_material_evidence_policy
    from .rank_policy import make_material_rank_policy
    from .residual_policy import make_material_residual_policy
    from .operation_policy import make_material_operation_policy

    return StyleSpec(
        domain_spec=make_material_experimental_domain(),
        evidence_policy=make_material_evidence_policy(),
        rank_policy=make_material_rank_policy(),
        residual_policy=make_material_residual_policy(),
        operation_policy=make_material_operation_policy(),
        name_ar="الأسلوب المادي التجريبي",
        name_en="Material Experimental Style",
        description=(
            "Style for material/experimental domain. "
            "Declaration only - ScientificMethod NOT implemented."
        ),
    )


def make_formal_logical_style() -> StyleSpec:
    """
    Create FormalLogical style specification.

    This is DECLARATION ONLY.
    LogicalStyle implementation is NOT part of this PR.
    """
    from .domain_spec import make_formal_logical_domain
    from .evidence_policy import make_formal_evidence_policy
    from .rank_policy import make_formal_rank_policy
    from .residual_policy import make_formal_residual_policy
    from .operation_policy import make_formal_operation_policy

    return StyleSpec(
        domain_spec=make_formal_logical_domain(),
        evidence_policy=make_formal_evidence_policy(),
        rank_policy=make_formal_rank_policy(),
        residual_policy=make_formal_residual_policy(),
        operation_policy=make_formal_operation_policy(),
        name_ar="الأسلوب الصوري المنطقي",
        name_en="Formal Logical Style",
        description=(
            "Style for formal/logical domain. "
            "Declaration only - LogicalStyle NOT implemented."
        ),
    )


def make_lafzi_dalali_style() -> StyleSpec:
    """
    Create LafziDalali style specification.

    This is DECLARATION ONLY.
    LafziMadlul implementation is NOT part of this PR.

    Critical:
    - This declares the domain and constraints
    - This does NOT implement linguistic analysis
    - LafziMadlul will be implemented in future PR-L0
    """
    from .domain_spec import make_lafzi_dalali_domain
    from .evidence_policy import make_lafzi_evidence_policy
    from .rank_policy import make_lafzi_rank_policy
    from .residual_policy import make_lafzi_residual_policy
    from .operation_policy import make_lafzi_operation_policy

    return StyleSpec(
        domain_spec=make_lafzi_dalali_domain(),
        evidence_policy=make_lafzi_evidence_policy(),
        rank_policy=make_lafzi_rank_policy(),
        residual_policy=make_lafzi_residual_policy(),
        operation_policy=make_lafzi_operation_policy(),
        name_ar="الأسلوب اللفظي الدلالي",
        name_en="Lafzi Dalali Style",
        description=(
            "Style for lafzi/dalali domain (وضع/استعمال). "
            "Declaration only - LafziMadlul NOT implemented. "
            "Implementation will be in future PR-L0."
        ),
    )


def make_textual_normative_style() -> StyleSpec:
    """
    Create TextualNormative style specification.

    This is DECLARATION ONLY.
    Textual interpretation implementation is NOT part of this PR.
    """
    from .domain_spec import make_textual_normative_domain
    from .evidence_policy import make_textual_evidence_policy
    from .rank_policy import make_textual_rank_policy
    from .residual_policy import make_textual_residual_policy
    from .operation_policy import make_textual_operation_policy

    return StyleSpec(
        domain_spec=make_textual_normative_domain(),
        evidence_policy=make_textual_evidence_policy(),
        rank_policy=make_textual_rank_policy(),
        residual_policy=make_textual_residual_policy(),
        operation_policy=make_textual_operation_policy(),
        name_ar="الأسلوب النصي الشرعي",
        name_en="Textual Normative Style",
        description=(
            "Style for textual/normative domain (نصوص/أحكام). "
            "Declaration only - interpretation NOT implemented."
        ),
    )


def make_programming_execution_style() -> StyleSpec:
    """
    Create ProgrammingExecution style specification.

    This is DECLARATION ONLY.
    Code execution implementation is NOT part of this PR.
    """
    from .domain_spec import make_programming_execution_domain
    from .evidence_policy import make_programming_evidence_policy
    from .rank_policy import make_programming_rank_policy
    from .residual_policy import make_programming_residual_policy
    from .operation_policy import make_programming_operation_policy

    return StyleSpec(
        domain_spec=make_programming_execution_domain(),
        evidence_policy=make_programming_evidence_policy(),
        rank_policy=make_programming_rank_policy(),
        residual_policy=make_programming_residual_policy(),
        operation_policy=make_programming_operation_policy(),
        name_ar="الأسلوب البرمجي التنفيذي",
        name_en="Programming Execution Style",
        description=(
            "Style for programming/execution domain. "
            "Declaration only - execution NOT implemented."
        ),
    )
