"""
Dal Kernel Mapping Validators (PR-122)

Validates consistency between dal_algebra types and AlgebraicDecisionCore types:
- DalTransitionDomain ↔ ExecutionLayer
- DalTransitionDomain ↔ DomainType
- DalClaimScope ↔ DalTransitionDomain
- DalTransitionContract ↔ dal_domain/dal_claim_scope

Constitutional Law:
    لا metadata غير محكومة.
    No ungoverned metadata.

PR-122 Goal:
    Transform dal_* fields from transitional metadata into validated governance metadata.

Created: 2026-05-27
"""

from typing import Tuple, FrozenSet, Dict, Set
from types import MappingProxyType

from dal_core.dal_algebra import (
    DalTransitionDomain,
    DalClaimScope,
    DalTransitionContract,
)
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.domain_registry import DomainType


# ============================================================================
# Canonical Mapping Tables (Immutable)
# ============================================================================

# Map 1: DalTransitionDomain → ExecutionLayer(s)
# Based on DAL_KERNEL_MAPPING.md canonical mapping
_DAL_DOMAIN_TO_EXECUTION_LAYER: Dict[DalTransitionDomain, FrozenSet[ExecutionLayer]] = {
    DalTransitionDomain.GRAPHOPHONEMIC: frozenset({
        ExecutionLayer.U0_UNICODE,
        ExecutionLayer.U1_GRAPHEME,
    }),
    DalTransitionDomain.SYLLABIC: frozenset({
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
    }),
    DalTransitionDomain.PRE_MORPH: frozenset({
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        ExecutionLayer.U4_TRUE_SINGULAR_LAFZ,
    }),
    DalTransitionDomain.ORIGIN: frozenset({
        ExecutionLayer.U8_ROOT_STEM,
    }),
    DalTransitionDomain.TEMPLATE: frozenset({
        ExecutionLayer.U9_WEIGHT,
    }),
    DalTransitionDomain.IDENTITY_AXIS: frozenset({
        ExecutionLayer.U5_FUNCTIONAL_ROLE,
        ExecutionLayer.U6_MABNI_CLOSED_CLASS,
    }),
    DalTransitionDomain.DIRECTIONAL_ANALYSIS: frozenset({
        ExecutionLayer.U7A_PRE_WEIGHT_CONTRACT,
        ExecutionLayer.U7B_INFLECTIONAL_SURFACE_CONTRACT,
        ExecutionLayer.U7C_CLAUSE_SURFACE_AGREEMENT,
    }),
    DalTransitionDomain.WORDFORM: frozenset({
        ExecutionLayer.U10_WORD_FORM,
    }),
    DalTransitionDomain.JUDGMENT: frozenset({
        ExecutionLayer.U7C_CLAUSE_SURFACE_AGREEMENT,
    }),
}

DAL_DOMAIN_TO_EXECUTION_LAYER_MAP = MappingProxyType(_DAL_DOMAIN_TO_EXECUTION_LAYER)


# Map 2: DalTransitionDomain → DomainType(s)
# Based on DAL_KERNEL_MAPPING.md with documented gaps
_DAL_DOMAIN_TO_DOMAIN_TYPE: Dict[DalTransitionDomain, FrozenSet[DomainType]] = {
    DalTransitionDomain.GRAPHOPHONEMIC: frozenset({
        DomainType.SCRIPT_DOMAIN,
        DomainType.SOUND_DOMAIN,
    }),
    DalTransitionDomain.SYLLABIC: frozenset({
        DomainType.SYLLABLE_DOMAIN,
    }),
    DalTransitionDomain.PRE_MORPH: frozenset({
        DomainType.BOUNDARY_DOMAIN,
        DomainType.LAFZ_DOMAIN,
    }),
    DalTransitionDomain.ORIGIN: frozenset({
        DomainType.ROOT_STEM_DOMAIN,
    }),
    DalTransitionDomain.TEMPLATE: frozenset({
        DomainType.WEIGHT_DOMAIN,
    }),
    # IDENTITY_AXIS maps to IDENTITY_DOMAIN
    DalTransitionDomain.IDENTITY_AXIS: frozenset({
        DomainType.IDENTITY_DOMAIN,
    }),
    DalTransitionDomain.DIRECTIONAL_ANALYSIS: frozenset({
        DomainType.MARKER_PROTECTION_DOMAIN,
        DomainType.CLAUSE_AGREEMENT_DOMAIN,
    }),
    # WORDFORM maps to WORDFORM_DOMAIN (U₁₀)
    DalTransitionDomain.WORDFORM: frozenset({
        DomainType.WORDFORM_DOMAIN,
    }),
    # JUDGMENT maps to JUDGMENT_DOMAIN (U₇-C), NOT U₁₀ WordForm
    DalTransitionDomain.JUDGMENT: frozenset({
        DomainType.JUDGMENT_DOMAIN,
    }),
}

DAL_DOMAIN_TO_DOMAIN_TYPE_MAP = MappingProxyType(_DAL_DOMAIN_TO_DOMAIN_TYPE)


# Map 3: DalTransitionDomain → DalClaimScope(s)
# Based on dal_algebra.py DalClaimScope definitions
_DAL_DOMAIN_TO_CLAIM_SCOPE: Dict[DalTransitionDomain, FrozenSet[DalClaimScope]] = {
    DalTransitionDomain.GRAPHOPHONEMIC: frozenset({
        DalClaimScope.CARRIER_VALID,
        DalClaimScope.ATOM_SEQUENCE_VALID,
    }),
    DalTransitionDomain.SYLLABIC: frozenset({
        DalClaimScope.SYLLABLE_STRUCTURE_VALID,
    }),
    DalTransitionDomain.PRE_MORPH: frozenset({
        # Pre-morphological classification doesn't have explicit claim scope yet
        # Could use ATOM_SEQUENCE_VALID or define new scope
        DalClaimScope.ATOM_SEQUENCE_VALID,
    }),
    DalTransitionDomain.ORIGIN: frozenset({
        DalClaimScope.ORIGIN_CLASSIFIED,
    }),
    DalTransitionDomain.TEMPLATE: frozenset({
        DalClaimScope.TEMPLATE_MATCHED,
    }),
    DalTransitionDomain.IDENTITY_AXIS: frozenset({
        DalClaimScope.IDENTITY_DETERMINED,
    }),
    DalTransitionDomain.DIRECTIONAL_ANALYSIS: frozenset({
        DalClaimScope.FORM_ANALYZED,
    }),
    DalTransitionDomain.WORDFORM: frozenset({
        DalClaimScope.WORDFORM_DETERMINED,
    }),
    DalTransitionDomain.JUDGMENT: frozenset({
        DalClaimScope.JUDGMENT_ISSUED,
    }),
}

DAL_DOMAIN_TO_CLAIM_SCOPE_MAP = MappingProxyType(_DAL_DOMAIN_TO_CLAIM_SCOPE)


# ============================================================================
# Validation Functions
# ============================================================================

def validate_dal_kernel_mapping(
    dal_domain: DalTransitionDomain | None,
    dal_claim_scope: DalClaimScope | None,
    dal_contract: DalTransitionContract | None,
    from_layer: ExecutionLayer,
    to_layer: ExecutionLayer,
    domain: DomainType
) -> Tuple[str, ...]:
    """
    Validate consistency between dal_* fields and ExecutionLayer/DomainType.

    This is the MAIN VALIDATOR enforcing kernel mapping governance.

    Args:
        dal_domain: Optional DalTransitionDomain from audit
        dal_claim_scope: Optional DalClaimScope from audit
        dal_contract: Optional DalTransitionContract from audit
        from_layer: Source ExecutionLayer
        to_layer: Target ExecutionLayer
        domain: DomainType of operation

    Returns:
        Tuple of validation error messages (empty if valid)

    Validation Rules:
        0. If dal_contract present: dal_domain and dal_claim_scope are REQUIRED
        1. If dal_domain is None: allow legacy mode (no validation)
        2. If dal_domain present: must match from_layer/to_layer
        3. If dal_claim_scope present: must be allowed for dal_domain
        4. If dal_contract present: must match dal_domain/dal_claim_scope
        5. Domain mapping must be consistent (or documented GAP)

    Constitutional Law:
        Dal_* inconsistency in approved audit = violation, not warning.
    """
    violations: list[str] = []

    # Rule 0: If dal_contract present, dal_domain and dal_claim_scope are REQUIRED
    # Constitutional Law: No contract without domain. No contract without claim scope.
    if dal_contract is not None:
        if dal_domain is None:
            violations.append(
                "dal_contract present but dal_domain is None. "
                "Constitutional law: No contract without domain."
            )
        if dal_claim_scope is None:
            violations.append(
                "dal_contract present but dal_claim_scope is None. "
                "Constitutional law: No contract without claim scope."
            )

    # Rule 1: If dal_domain absent, allow legacy mode
    if dal_domain is None:
        return tuple(violations)  # No dal_domain = no validation (unless dal_contract present)

    # Rule 2: Validate dal_domain ↔ ExecutionLayer mapping
    expected_layers = DAL_DOMAIN_TO_EXECUTION_LAYER_MAP.get(dal_domain, frozenset())
    if not expected_layers:
        violations.append(
            f"dal_domain {dal_domain.name} has no ExecutionLayer mapping defined"
        )
    else:
        # Check if either from_layer or to_layer is in expected range
        if from_layer not in expected_layers and to_layer not in expected_layers:
            violations.append(
                f"dal_domain {dal_domain.name} expects layers {_format_layers(expected_layers)}, "
                f"but got {from_layer.name}→{to_layer.name}"
            )

    # Rule 3: Validate dal_domain ↔ DomainType mapping
    expected_domains = DAL_DOMAIN_TO_DOMAIN_TYPE_MAP.get(dal_domain, frozenset())
    if not expected_domains:
        violations.append(
            f"dal_domain {dal_domain.name} has no DomainType mapping defined"
        )
    else:
        if domain not in expected_domains:
            violations.append(
                f"dal_domain {dal_domain.name} expects domains {_format_domains(expected_domains)}, "
                f"but got {domain.name}"
            )

    # Rule 4: Validate dal_claim_scope ↔ dal_domain consistency
    if dal_claim_scope is not None:
        expected_scopes = DAL_DOMAIN_TO_CLAIM_SCOPE_MAP.get(dal_domain, frozenset())
        if not expected_scopes:
            violations.append(
                f"dal_domain {dal_domain.name} has no DalClaimScope mapping defined"
            )
        elif dal_claim_scope not in expected_scopes:
            violations.append(
                f"dal_claim_scope {dal_claim_scope.name} not allowed for "
                f"dal_domain {dal_domain.name} "
                f"(expected: {_format_scopes(expected_scopes)})"
            )

    # Rule 5: Validate dal_contract consistency
    if dal_contract is not None:
        # Check source_domain matches dal_domain
        if dal_contract.source_domain != dal_domain:
            violations.append(
                f"dal_contract.source_domain {dal_contract.source_domain.name} "
                f"!= dal_domain {dal_domain.name}"
            )

        # Check target_domain is valid (must be in mapping)
        target_expected_layers = DAL_DOMAIN_TO_EXECUTION_LAYER_MAP.get(
            dal_contract.target_domain, frozenset()
        )
        if not target_expected_layers:
            violations.append(
                f"dal_contract.target_domain {dal_contract.target_domain.name} "
                f"has no ExecutionLayer mapping"
            )

        # Check claim_scope matches dal_claim_scope
        if dal_claim_scope is not None and dal_contract.claim_scope != dal_claim_scope:
            violations.append(
                f"dal_contract.claim_scope {dal_contract.claim_scope.name} "
                f"!= dal_claim_scope {dal_claim_scope.name}"
            )

    return tuple(violations)


def _format_layers(layers: FrozenSet[ExecutionLayer]) -> str:
    """Format ExecutionLayer set for error message."""
    return "{" + ", ".join(layer.name for layer in sorted(layers, key=lambda x: x.value)) + "}"


def _format_domains(domains: FrozenSet[DomainType]) -> str:
    """Format DomainType set for error message."""
    return "{" + ", ".join(domain.name for domain in sorted(domains, key=lambda x: x.value)) + "}"


def _format_scopes(scopes: FrozenSet[DalClaimScope]) -> str:
    """Format DalClaimScope set for error message."""
    return "{" + ", ".join(scope.name for scope in sorted(scopes, key=lambda x: x.value)) + "}"


def is_dal_kernel_mapping_valid(
    dal_domain: DalTransitionDomain | None,
    dal_claim_scope: DalClaimScope | None,
    dal_contract: DalTransitionContract | None,
    from_layer: ExecutionLayer,
    to_layer: ExecutionLayer,
    domain: DomainType
) -> bool:
    """
    Check if dal_kernel mapping is valid (convenience function).

    Returns:
        True if valid (no violations), False otherwise
    """
    violations = validate_dal_kernel_mapping(
        dal_domain, dal_claim_scope, dal_contract,
        from_layer, to_layer, domain
    )
    return len(violations) == 0


__all__ = [
    "DAL_DOMAIN_TO_EXECUTION_LAYER_MAP",
    "DAL_DOMAIN_TO_DOMAIN_TYPE_MAP",
    "DAL_DOMAIN_TO_CLAIM_SCOPE_MAP",
    "validate_dal_kernel_mapping",
    "is_dal_kernel_mapping_valid",
]
