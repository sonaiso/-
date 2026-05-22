"""
Styles Module - أساليب التفكير

Domain-specific specializations of RationalMethod.

This module provides the StyleSpec framework for declaring
domain constraints and policies. It does NOT implement:
    - ScientificMethod
    - LogicalStyle
    - MeansAlgebra
    - UniversalRules
    - LafziMadlul
    - Learning
    - Domain Registry

StyleSpec is a declaration and validation layer only.

Critical Laws:
    1. Every thinking style is a domain-specific specialization
    2. StyleSpec requires DomainSpec
    3. StyleSpec requires EvidencePolicy
    4. StyleSpec requires RankPolicy
    5. StyleSpec requires ResidualPolicy
    6. StyleSpec requires OperationPolicy
    7. StyleSpec does NOT implement reasoning
    8. StyleSpec does NOT issue judgment
    9. StyleSpec does NOT certify claims

Architecture:
    RationalMethod (root)
    └── NeutralBinding (neutral element)
        └── StyleSpec (domain specialization)
            ├── Material/Experimental (declared)
            ├── Formal/Logical (declared)
            ├── Lafzi/Dalali (declared)
            ├── Textual/Normative (declared)
            └── Programming/Execution (declared)
"""

# Domain specifications
from .domain_spec import (
    ThinkingDomain,
    EvidenceKind,
    DomainBoundary,
    DomainSpec,
    make_material_experimental_domain,
    make_formal_logical_domain,
    make_lafzi_dalali_domain,
    make_textual_normative_domain,
    make_programming_execution_domain,
)

# Evidence policy
from .evidence_policy import (
    EvidenceStrength,
    EvidenceRequirement,
    EvidenceConstraint,
    EvidencePolicy,
    make_material_evidence_policy,
    make_formal_evidence_policy,
    make_lafzi_evidence_policy,
    make_textual_evidence_policy,
    make_programming_evidence_policy,
)

# Rank policy
from .rank_policy import (
    RankTransition,
    RankConstraint,
    RankPolicy,
    make_material_rank_policy,
    make_formal_rank_policy,
    make_lafzi_rank_policy,
    make_textual_rank_policy,
    make_programming_rank_policy,
)

# Residual policy
from .residual_policy import (
    ResidualSeverity,
    ResidualHandling,
    ResidualRule,
    ResidualPolicy,
    make_material_residual_policy,
    make_formal_residual_policy,
    make_lafzi_residual_policy,
    make_textual_residual_policy,
    make_programming_residual_policy,
)

# Operation policy
from .operation_policy import (
    OperationKind,
    AllowedOperation,
    ForbiddenOperation,
    OperationPolicy,
    UNIVERSAL_FORBIDDEN_OPERATIONS,
    UNIVERSAL_ALLOWED_OPERATIONS,
    make_material_operation_policy,
    make_formal_operation_policy,
    make_lafzi_operation_policy,
    make_textual_operation_policy,
    make_programming_operation_policy,
)

# Residual taxonomy
from .residual_taxonomy import (
    StyleResidualKind,
    StyleResidual,
    make_domain_mismatch_residual,
    make_forbidden_domain_jump_residual,
    make_forbidden_evidence_residual,
    make_missing_required_evidence_residual,
    make_rank_inflation_residual,
    make_forbidden_operation_residual,
    make_style_spec_missing_residual,
    make_meta_violation_residual,
)

# Style spec
from .style_spec import (
    StyleSpec,
    make_material_experimental_style,
    make_formal_logical_style,
    make_lafzi_dalali_style,
    make_textual_normative_style,
    make_programming_execution_style,
)

# Style validator
from .style_validator import (
    StyleValidationResult,
    StyleValidator,
)

__all__ = [
    # Domain
    "ThinkingDomain",
    "EvidenceKind",
    "DomainBoundary",
    "DomainSpec",
    "make_material_experimental_domain",
    "make_formal_logical_domain",
    "make_lafzi_dalali_domain",
    "make_textual_normative_domain",
    "make_programming_execution_domain",
    # Evidence
    "EvidenceStrength",
    "EvidenceRequirement",
    "EvidenceConstraint",
    "EvidencePolicy",
    "make_material_evidence_policy",
    "make_formal_evidence_policy",
    "make_lafzi_evidence_policy",
    "make_textual_evidence_policy",
    "make_programming_evidence_policy",
    # Rank
    "RankTransition",
    "RankConstraint",
    "RankPolicy",
    "make_material_rank_policy",
    "make_formal_rank_policy",
    "make_lafzi_rank_policy",
    "make_textual_rank_policy",
    "make_programming_rank_policy",
    # Residual
    "ResidualSeverity",
    "ResidualHandling",
    "ResidualRule",
    "ResidualPolicy",
    "make_material_residual_policy",
    "make_formal_residual_policy",
    "make_lafzi_residual_policy",
    "make_textual_residual_policy",
    "make_programming_residual_policy",
    # Operation
    "OperationKind",
    "AllowedOperation",
    "ForbiddenOperation",
    "OperationPolicy",
    "UNIVERSAL_FORBIDDEN_OPERATIONS",
    "UNIVERSAL_ALLOWED_OPERATIONS",
    "make_material_operation_policy",
    "make_formal_operation_policy",
    "make_lafzi_operation_policy",
    "make_textual_operation_policy",
    "make_programming_operation_policy",
    # Style residual
    "StyleResidualKind",
    "StyleResidual",
    "make_domain_mismatch_residual",
    "make_forbidden_domain_jump_residual",
    "make_forbidden_evidence_residual",
    "make_missing_required_evidence_residual",
    "make_rank_inflation_residual",
    "make_forbidden_operation_residual",
    "make_style_spec_missing_residual",
    "make_meta_violation_residual",
    # Style spec
    "StyleSpec",
    "make_material_experimental_style",
    "make_formal_logical_style",
    "make_lafzi_dalali_style",
    "make_textual_normative_style",
    "make_programming_execution_style",
    # Validator
    "StyleValidationResult",
    "StyleValidator",
]
