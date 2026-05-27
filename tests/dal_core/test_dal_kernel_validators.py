"""
Tests for Dal Kernel Mapping Validators (PR-122)

Tests that dal_* fields are validated for consistency with ExecutionLayer and DomainType.

Critical Tests:
1. Valid mappings pass
2. Invalid dal_domain ↔ ExecutionLayer blocked
3. Invalid dal_domain ↔ DomainType blocked
4. Invalid dal_claim_scope ↔ dal_domain blocked
5. Invalid dal_contract consistency blocked
6. ApprovedTransitionContext creation blocked with invalid dal_*
"""

import pytest
from dataclasses import replace

from dal_core.dal_kernel_validators import (
    validate_dal_kernel_mapping,
    is_dal_kernel_mapping_valid,
    DAL_DOMAIN_TO_EXECUTION_LAYER_MAP,
    DAL_DOMAIN_TO_DOMAIN_TYPE_MAP,
    DAL_DOMAIN_TO_CLAIM_SCOPE_MAP,
)
from dal_core.dal_algebra import (
    DalTransitionDomain,
    DalClaimScope,
    DalTransitionContract,
)
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.domain_registry import DomainType
from dal_core.algebraic_decision_core import (
    AlgebraicDecisionCore,
    CPBStatus,
)
from dal_core.approved_transition_context import create_approved_context
from dal_core.identity_registry import IdentityType
from dal_core.foundation import Rank, ResidualSet


# ============================================================================
# Test Mapping Tables
# ============================================================================

def test_dal_domain_to_execution_layer_map_exists():
    """Test that DalTransitionDomain → ExecutionLayer mapping exists."""
    assert DAL_DOMAIN_TO_EXECUTION_LAYER_MAP is not None
    assert len(DAL_DOMAIN_TO_EXECUTION_LAYER_MAP) > 0


def test_dal_domain_to_domain_type_map_exists():
    """Test that DalTransitionDomain → DomainType mapping exists."""
    assert DAL_DOMAIN_TO_DOMAIN_TYPE_MAP is not None
    assert len(DAL_DOMAIN_TO_DOMAIN_TYPE_MAP) > 0


def test_dal_domain_to_claim_scope_map_exists():
    """Test that DalTransitionDomain → DalClaimScope mapping exists."""
    assert DAL_DOMAIN_TO_CLAIM_SCOPE_MAP is not None
    assert len(DAL_DOMAIN_TO_CLAIM_SCOPE_MAP) > 0


# ============================================================================
# Test Valid Mappings
# ============================================================================

def test_valid_template_domain_for_u8_to_u9_passes():
    """Test that TEMPLATE domain with U₈→U₉ transition passes validation."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.TEMPLATE,
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        dal_contract=None,
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.WEIGHT_DOMAIN
    )
    assert len(violations) == 0, f"Expected no violations, got: {violations}"


def test_valid_syllabic_domain_passes():
    """Test that SYLLABIC domain with U₂s passes validation."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.SYLLABIC,
        dal_claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,
        dal_contract=None,
        from_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
        to_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
        domain=DomainType.SYLLABLE_DOMAIN
    )
    assert len(violations) == 0, f"Expected no violations, got: {violations}"


def test_valid_origin_domain_for_u8_passes():
    """Test that ORIGIN domain with U₈ passes validation."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.ORIGIN,
        dal_claim_scope=DalClaimScope.ORIGIN_CLASSIFIED,
        dal_contract=None,
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U8_ROOT_STEM,
        domain=DomainType.ROOT_STEM_DOMAIN
    )
    assert len(violations) == 0, f"Expected no violations, got: {violations}"


def test_valid_graphophonemic_domain_passes():
    """Test that GRAPHOPHONEMIC domain with U₀→U₁ passes validation."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        dal_claim_scope=DalClaimScope.ATOM_SEQUENCE_VALID,
        dal_contract=None,
        from_layer=ExecutionLayer.U0_UNICODE,
        to_layer=ExecutionLayer.U1_GRAPHEME,
        domain=DomainType.SOUND_DOMAIN
    )
    assert len(violations) == 0, f"Expected no violations, got: {violations}"


def test_none_dal_domain_allows_legacy_mode():
    """Test that None dal_domain allows legacy mode (no validation)."""
    violations = validate_dal_kernel_mapping(
        dal_domain=None,
        dal_claim_scope=None,
        dal_contract=None,
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.WEIGHT_DOMAIN
    )
    assert len(violations) == 0, "Legacy mode should allow any transition"


# ============================================================================
# Test Invalid dal_domain ↔ ExecutionLayer Mapping
# ============================================================================

def test_syllabic_domain_cannot_be_used_for_u8_to_u9():
    """Test that SYLLABIC domain is invalid for U₈→U₉ transition."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.SYLLABIC,  # Wrong domain
        dal_claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,
        dal_contract=None,
        from_layer=ExecutionLayer.U8_ROOT_STEM,  # U₈
        to_layer=ExecutionLayer.U9_WEIGHT,  # U₉
        domain=DomainType.WEIGHT_DOMAIN
    )
    assert len(violations) > 0, "Should have violations for wrong dal_domain"
    assert any("expects layers" in v for v in violations), \
        "Should mention expected layers in violation"


def test_template_domain_cannot_be_used_for_u2s():
    """Test that TEMPLATE domain is invalid for U₂s (syllable) layer."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.TEMPLATE,  # Wrong domain
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        dal_contract=None,
        from_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
        to_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
        domain=DomainType.SYLLABLE_DOMAIN
    )
    assert len(violations) > 0, "Should have violations for wrong dal_domain"


# ============================================================================
# Test Invalid dal_domain ↔ DomainType Mapping
# ============================================================================

def test_template_domain_with_syllable_domaintype_fails():
    """Test that TEMPLATE dal_domain with SYLLABLE_DOMAIN fails."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.TEMPLATE,
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        dal_contract=None,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.SYLLABLE_DOMAIN  # Wrong DomainType
    )
    assert len(violations) > 0, "Should have violations for wrong DomainType"
    assert any("expects domains" in v for v in violations), \
        "Should mention expected domains in violation"


def test_syllabic_domain_with_weight_domaintype_fails():
    """Test that SYLLABIC dal_domain with WEIGHT_DOMAIN fails."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.SYLLABIC,
        dal_claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,
        dal_contract=None,
        from_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
        to_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
        domain=DomainType.WEIGHT_DOMAIN  # Wrong DomainType
    )
    assert len(violations) > 0, "Should have violations for wrong DomainType"


# ============================================================================
# Test Invalid dal_claim_scope ↔ dal_domain Mapping
# ============================================================================

def test_claim_scope_must_match_dal_domain():
    """Test that dal_claim_scope must match dal_domain."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.TEMPLATE,
        dal_claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,  # Wrong scope
        dal_contract=None,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.WEIGHT_DOMAIN
    )
    assert len(violations) > 0, "Should have violations for wrong claim_scope"
    assert any("not allowed for" in v for v in violations), \
        "Should mention claim_scope not allowed"


def test_syllabic_claim_scope_with_template_domain_fails():
    """Test that SYLLABLE_STRUCTURE_VALID with TEMPLATE domain fails."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.SYLLABIC,
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED,  # Wrong scope
        dal_contract=None,
        from_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
        to_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
        domain=DomainType.SYLLABLE_DOMAIN
    )
    assert len(violations) > 0, "Should have violations for wrong claim_scope"


# ============================================================================
# Test Invalid dal_contract Consistency
# ============================================================================

def test_dal_contract_claim_scope_mismatch_blocks_context():
    """Test that dal_contract claim_scope must match dal_claim_scope."""
    contract = DalTransitionContract(
        contract_id="test-contract",
        source_domain=DalTransitionDomain.TEMPLATE,
        target_domain=DalTransitionDomain.JUDGMENT,
        input_type=dict,
        output_type=dict,
        claim_scope=DalClaimScope.ORIGIN_CLASSIFIED  # Wrong scope
    )

    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.TEMPLATE,
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        dal_contract=contract,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.WEIGHT_DOMAIN
    )
    assert len(violations) > 0, "Should have violations for contract mismatch"
    assert any("dal_contract.claim_scope" in v for v in violations), \
        "Should mention contract claim_scope mismatch"


def test_dal_contract_source_domain_mismatch_fails():
    """Test that dal_contract.source_domain must match dal_domain."""
    contract = DalTransitionContract(
        contract_id="test-contract",
        source_domain=DalTransitionDomain.SYLLABIC,  # Wrong source
        target_domain=DalTransitionDomain.TEMPLATE,
        input_type=dict,
        output_type=dict,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED
    )

    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.TEMPLATE,
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        dal_contract=contract,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.WEIGHT_DOMAIN
    )
    assert len(violations) > 0, "Should have violations for source_domain mismatch"
    assert any("dal_contract.source_domain" in v for v in violations), \
        "Should mention contract source_domain mismatch"


# ============================================================================
# Test AlgebraicDecisionCore Integration
# ============================================================================

def test_algebraic_decision_core_rejects_invalid_dal_domain():
    """Test that AlgebraicDecisionCore rejects invalid dal_domain."""
    core = AlgebraicDecisionCore()

    audit = core.decide_transition(
        transition_id="test_u8_to_u9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        existing_identities=frozenset({
            IdentityType.ROOT_MATERIAL_IDENTITY,
            IdentityType.STEM_IDENTITY,  # Required for U8→U9
        }),
        domain=DomainType.WEIGHT_DOMAIN,
        attempted_determination="weight_pattern",  # Valid competency
        gate_name="weight_gate",
        gate_passed=True,
        evidence=("test_evidence",),
        required_evidence=frozenset(),
        input_rank=Rank.CANDIDATE,
        output_rank=Rank.CANDIDATE,
        residual_set=ResidualSet(frozenset()),
        trace=("test_trace",),
        # Invalid dal_domain for this transition
        dal_domain=DalTransitionDomain.SYLLABIC,
        dal_claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID
    )

    assert not audit.allowed, "Audit should not be allowed with invalid dal_domain"
    # Dal kernel violations should be present
    assert any("Dal Kernel" in v for v in audit.violations), \
        "Should have kernel validation violation"


def test_algebraic_decision_core_approves_valid_dal_domain():
    """Test that AlgebraicDecisionCore approves valid dal_domain."""
    core = AlgebraicDecisionCore()

    audit = core.decide_transition(
        transition_id="test_u8_to_u9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        existing_identities=frozenset({
            IdentityType.ROOT_MATERIAL_IDENTITY,
            IdentityType.STEM_IDENTITY,  # Required for U8→U9
        }),
        domain=DomainType.WEIGHT_DOMAIN,
        attempted_determination="weight_pattern",
        gate_name="weight_gate",
        gate_passed=True,
        evidence=("test_evidence",),
        required_evidence=frozenset(),
        input_rank=Rank.CANDIDATE,
        output_rank=Rank.CANDIDATE,
        residual_set=ResidualSet(frozenset()),
        trace=("test_trace",),
        # Valid dal_domain for this transition
        dal_domain=DalTransitionDomain.TEMPLATE,
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED
    )

    assert audit.allowed, f"Audit should be allowed with valid dal_domain. Violations: {audit.violations}"
    assert audit.cpb_status == CPBStatus.APPROVED, \
        f"Expected APPROVED, got {audit.cpb_status}"


# ============================================================================
# Test ApprovedTransitionContext Enforcement
# ============================================================================

def test_approved_context_preserves_valid_dal_fields():
    """Test that ApprovedTransitionContext preserves valid dal_* fields."""
    core = AlgebraicDecisionCore()

    audit = core.decide_transition(
        transition_id="test_u8_to_u9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        existing_identities=frozenset({
            IdentityType.ROOT_MATERIAL_IDENTITY,
            IdentityType.STEM_IDENTITY,  # Required for U8→U9
        }),
        domain=DomainType.WEIGHT_DOMAIN,
        attempted_determination="weight_pattern",
        gate_name="weight_gate",
        gate_passed=True,
        evidence=("test_evidence",),
        required_evidence=frozenset(),
        input_rank=Rank.CANDIDATE,
        output_rank=Rank.CANDIDATE,
        residual_set=ResidualSet(frozenset()),
        trace=("test_trace",),
        dal_domain=DalTransitionDomain.TEMPLATE,
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED
    )

    context = create_approved_context(
        audit,
        frozenset({
            IdentityType.ROOT_MATERIAL_IDENTITY,
            IdentityType.STEM_IDENTITY,
        })
    )

    assert context.dal_domain == DalTransitionDomain.TEMPLATE
    assert context.dal_claim_scope == DalClaimScope.TEMPLATE_MATCHED


def test_missing_dal_fields_allowed_only_as_legacy_metadata():
    """Test that missing dal_* fields are allowed (legacy mode)."""
    core = AlgebraicDecisionCore()

    audit = core.decide_transition(
        transition_id="test_u8_to_u9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        existing_identities=frozenset({
            IdentityType.ROOT_MATERIAL_IDENTITY,
            IdentityType.STEM_IDENTITY,  # Required for U8→U9
        }),
        domain=DomainType.WEIGHT_DOMAIN,
        attempted_determination="weight_pattern",
        gate_name="weight_gate",
        gate_passed=True,
        evidence=("test_evidence",),
        required_evidence=frozenset(),
        input_rank=Rank.CANDIDATE,
        output_rank=Rank.CANDIDATE,
        residual_set=ResidualSet(frozenset()),
        trace=("test_trace",),
        # No dal_* fields (legacy mode)
    )

    assert audit.allowed, "Legacy mode should be allowed"
    assert audit.cpb_status == CPBStatus.APPROVED

    context = create_approved_context(
        audit,
        frozenset({
            IdentityType.ROOT_MATERIAL_IDENTITY,
            IdentityType.STEM_IDENTITY,
        })
    )
    assert context.dal_domain is None
    assert context.dal_claim_scope is None


def test_approved_context_blocks_invalid_dal_kernel():
    """Test that ApprovedTransitionContext cannot be created with invalid dal_kernel."""
    core = AlgebraicDecisionCore()

    # Create audit with invalid dal_domain (will be rejected)
    audit = core.decide_transition(
        transition_id="test_invalid",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        existing_identities=frozenset({
            IdentityType.ROOT_MATERIAL_IDENTITY,
            IdentityType.STEM_IDENTITY,  # Required for U8→U9
        }),
        domain=DomainType.WEIGHT_DOMAIN,
        attempted_determination="weight_pattern",
        gate_name="weight_gate",
        gate_passed=True,
        evidence=("test_evidence",),
        required_evidence=frozenset(),
        input_rank=Rank.CANDIDATE,
        output_rank=Rank.CANDIDATE,
        residual_set=ResidualSet(frozenset()),
        trace=("test_trace",),
        dal_domain=DalTransitionDomain.SYLLABIC,  # Invalid
        dal_claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID
    )

    # Audit should not be approved due to dal_kernel violations
    assert not audit.allowed
    # Check that dal_kernel violations are present
    assert any("Dal Kernel" in v for v in audit.violations), \
        f"Expected dal_kernel violations in: {audit.violations}"

    # Trying to create context should raise ValueError
    with pytest.raises(ValueError, match="unapproved audit"):
        create_approved_context(
            audit,
            frozenset({
                IdentityType.ROOT_MATERIAL_IDENTITY,
                IdentityType.STEM_IDENTITY,
            })
        )


# ============================================================================
# Test Convenience Function
# ============================================================================

def test_is_dal_kernel_mapping_valid_returns_bool():
    """Test that is_dal_kernel_mapping_valid() returns boolean."""
    # Valid mapping
    assert is_dal_kernel_mapping_valid(
        dal_domain=DalTransitionDomain.TEMPLATE,
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        dal_contract=None,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.WEIGHT_DOMAIN
    ) is True

    # Invalid mapping
    assert is_dal_kernel_mapping_valid(
        dal_domain=DalTransitionDomain.SYLLABIC,  # Wrong
        dal_claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,
        dal_contract=None,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.WEIGHT_DOMAIN
    ) is False


# ============================================================================
# Test PR-124: dal_contract without dal_domain / dal_claim_scope Validation
# ============================================================================

def test_dal_contract_without_dal_domain_is_violation():
    """Test that dal_contract without dal_domain is a violation (PR-124)."""
    contract = DalTransitionContract(
        contract_id="test-contract",
        source_domain=DalTransitionDomain.TEMPLATE,
        target_domain=DalTransitionDomain.JUDGMENT,
        input_type=dict,
        output_type=dict,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED
    )

    violations = validate_dal_kernel_mapping(
        dal_domain=None,  # Missing domain
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        dal_contract=contract,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.WEIGHT_DOMAIN
    )

    assert len(violations) > 0, "Should have violation for dal_contract without dal_domain"
    assert any("dal_contract present but dal_domain is None" in v for v in violations), \
        f"Should mention dal_contract without dal_domain. Got: {violations}"
    assert any("No contract without domain" in v for v in violations), \
        "Should mention constitutional law"


def test_dal_contract_without_dal_claim_scope_is_violation():
    """Test that dal_contract without dal_claim_scope is a violation (PR-124)."""
    contract = DalTransitionContract(
        contract_id="test-contract",
        source_domain=DalTransitionDomain.TEMPLATE,
        target_domain=DalTransitionDomain.JUDGMENT,
        input_type=dict,
        output_type=dict,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED
    )

    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.TEMPLATE,
        dal_claim_scope=None,  # Missing claim scope
        dal_contract=contract,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.WEIGHT_DOMAIN
    )

    assert len(violations) > 0, "Should have violation for dal_contract without dal_claim_scope"
    assert any("dal_contract present but dal_claim_scope is None" in v for v in violations), \
        f"Should mention dal_contract without dal_claim_scope. Got: {violations}"
    assert any("No contract without claim scope" in v for v in violations), \
        "Should mention constitutional law"


def test_dal_contract_without_both_domain_and_scope_has_two_violations():
    """Test that dal_contract without both dal_domain and dal_claim_scope has two violations (PR-124)."""
    contract = DalTransitionContract(
        contract_id="test-contract",
        source_domain=DalTransitionDomain.TEMPLATE,
        target_domain=DalTransitionDomain.JUDGMENT,
        input_type=dict,
        output_type=dict,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED
    )

    violations = validate_dal_kernel_mapping(
        dal_domain=None,  # Missing domain
        dal_claim_scope=None,  # Missing claim scope
        dal_contract=contract,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        domain=DomainType.WEIGHT_DOMAIN
    )

    assert len(violations) == 2, f"Should have 2 violations. Got {len(violations)}: {violations}"
    assert any("dal_domain is None" in v for v in violations), \
        "Should have violation for missing dal_domain"
    assert any("dal_claim_scope is None" in v for v in violations), \
        "Should have violation for missing dal_claim_scope"


def test_approved_context_rejects_dal_contract_without_domain():
    """Test that ApprovedTransitionContext rejects audit with dal_contract but no dal_domain (PR-124)."""
    core = AlgebraicDecisionCore()

    contract = DalTransitionContract(
        contract_id="test-contract",
        source_domain=DalTransitionDomain.TEMPLATE,
        target_domain=DalTransitionDomain.JUDGMENT,
        input_type=dict,
        output_type=dict,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED
    )

    # Create audit with dal_contract but no dal_domain
    audit = core.decide_transition(
        transition_id="test_contract_without_domain",
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.WEIGHT_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        existing_identities=frozenset({
            IdentityType.WEIGHT_IDENTITY,
        }),
        domain=DomainType.WEIGHT_DOMAIN,
        attempted_determination="test",
        gate_name="test_gate",
        gate_passed=True,
        evidence=("test_evidence",),
        required_evidence=frozenset(),
        input_rank=Rank.CANDIDATE,
        output_rank=Rank.CANDIDATE,
        residual_set=ResidualSet(frozenset()),
        trace=("test_trace",),
        dal_contract=contract,
        dal_domain=None,  # Missing
        dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED
    )

    # Audit should not be approved
    assert not audit.allowed, "Audit should not be allowed with dal_contract without dal_domain"
    assert any("Dal Kernel" in v for v in audit.violations), \
        f"Should have Dal Kernel violation. Got: {audit.violations}"

    # Trying to create context should raise ValueError
    with pytest.raises(ValueError, match="unapproved audit"):
        create_approved_context(
            audit,
            frozenset({IdentityType.WEIGHT_IDENTITY})
        )


def test_approved_context_rejects_dal_contract_without_claim_scope():
    """Test that ApprovedTransitionContext rejects audit with dal_contract but no dal_claim_scope (PR-124)."""
    core = AlgebraicDecisionCore()

    contract = DalTransitionContract(
        contract_id="test-contract",
        source_domain=DalTransitionDomain.TEMPLATE,
        target_domain=DalTransitionDomain.JUDGMENT,
        input_type=dict,
        output_type=dict,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED
    )

    # Create audit with dal_contract but no dal_claim_scope
    audit = core.decide_transition(
        transition_id="test_contract_without_claim_scope",
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.WEIGHT_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        existing_identities=frozenset({
            IdentityType.WEIGHT_IDENTITY,
        }),
        domain=DomainType.WEIGHT_DOMAIN,
        attempted_determination="test",
        gate_name="test_gate",
        gate_passed=True,
        evidence=("test_evidence",),
        required_evidence=frozenset(),
        input_rank=Rank.CANDIDATE,
        output_rank=Rank.CANDIDATE,
        residual_set=ResidualSet(frozenset()),
        trace=("test_trace",),
        dal_contract=contract,
        dal_domain=DalTransitionDomain.TEMPLATE,
        dal_claim_scope=None  # Missing
    )

    # Audit should not be approved
    assert not audit.allowed, "Audit should not be allowed with dal_contract without dal_claim_scope"
    assert any("Dal Kernel" in v for v in audit.violations), \
        f"Should have Dal Kernel violation. Got: {audit.violations}"

    # Trying to create context should raise ValueError
    with pytest.raises(ValueError, match="unapproved audit"):
        create_approved_context(
            audit,
            frozenset({IdentityType.WEIGHT_IDENTITY})
        )



# ============================================================================
# Test PR-125: IDENTITY_DOMAIN and WORDFORM_DOMAIN
# ============================================================================

def test_identity_axis_with_identity_domain_passes():
    """Test that IDENTITY_AXIS with IDENTITY_DOMAIN passes validation."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.IDENTITY_AXIS,
        dal_claim_scope=DalClaimScope.IDENTITY_DETERMINED,
        dal_contract=None,
        from_layer=ExecutionLayer.U5_FUNCTIONAL_ROLE,
        to_layer=ExecutionLayer.U6_MABNI_CLOSED_CLASS,
        domain=DomainType.IDENTITY_DOMAIN
    )
    assert len(violations) == 0, f"Expected no violations, got: {violations}"


def test_identity_axis_with_wrong_domain_fails():
    """Test that IDENTITY_AXIS with wrong domain fails validation."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.IDENTITY_AXIS,
        dal_claim_scope=DalClaimScope.IDENTITY_DETERMINED,
        dal_contract=None,
        from_layer=ExecutionLayer.U5_FUNCTIONAL_ROLE,
        to_layer=ExecutionLayer.U6_MABNI_CLOSED_CLASS,
        domain=DomainType.WEIGHT_DOMAIN  # Wrong domain
    )
    assert len(violations) > 0
    assert any("IDENTITY_AXIS" in v and "WEIGHT_DOMAIN" in v for v in violations)


def test_identity_domain_exists_in_mapping():
    """Test that IDENTITY_DOMAIN is registered in DAL_DOMAIN_TO_DOMAIN_TYPE_MAP."""
    identity_domains = DAL_DOMAIN_TO_DOMAIN_TYPE_MAP.get(DalTransitionDomain.IDENTITY_AXIS)
    assert identity_domains is not None, "IDENTITY_AXIS should have DomainType mapping"
    assert DomainType.IDENTITY_DOMAIN in identity_domains


def test_wordform_domain_exists_in_domain_registry():
    """Test that WORDFORM_DOMAIN exists in DomainType enum."""
    # Simply accessing it should not raise AttributeError
    assert hasattr(DomainType, 'WORDFORM_DOMAIN')
    wordform_domain = DomainType.WORDFORM_DOMAIN
    assert wordform_domain is not None


def test_identity_domain_exists_in_domain_registry():
    """Test that IDENTITY_DOMAIN exists in DomainType enum."""
    # Simply accessing it should not raise AttributeError
    assert hasattr(DomainType, 'IDENTITY_DOMAIN')
    identity_domain = DomainType.IDENTITY_DOMAIN
    assert identity_domain is not None


# ============================================================================
# Test PR-126: WORDFORM Domain Mapping (U₁₀)
# ============================================================================

def test_wordform_domain_with_u10_passes():
    """Test that WORDFORM domain with U₁₀ layer passes validation."""
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.WORDFORM,
        dal_claim_scope=DalClaimScope.WORDFORM_DETERMINED,
        dal_contract=None,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U10_WORD_FORM,
        domain=DomainType.WORDFORM_DOMAIN
    )
    assert len(violations) == 0, f"Expected no violations, got: {violations}"


def test_u10_with_judgment_domain_fails():
    """Test that U₁₀ with JUDGMENT_DOMAIN fails validation.

    Constitutional law: WordForm is not Judgment.
    U₁₀ must use WORDFORM_DOMAIN, not JUDGMENT_DOMAIN.
    """
    violations = validate_dal_kernel_mapping(
        dal_domain=DalTransitionDomain.JUDGMENT,
        dal_claim_scope=DalClaimScope.JUDGMENT_ISSUED,
        dal_contract=None,
        from_layer=ExecutionLayer.U9_WEIGHT,
        to_layer=ExecutionLayer.U10_WORD_FORM,
        domain=DomainType.JUDGMENT_DOMAIN
    )
    # Should fail because JUDGMENT does not map to U10_WORD_FORM
    assert len(violations) > 0
    assert any("JUDGMENT" in v and "U10_WORD_FORM" in v for v in violations)


def test_judgment_domain_does_not_include_u10():
    """Test that JUDGMENT domain mapping does NOT include U10_WORD_FORM."""
    judgment_layers = DAL_DOMAIN_TO_EXECUTION_LAYER_MAP.get(DalTransitionDomain.JUDGMENT)
    assert judgment_layers is not None
    assert ExecutionLayer.U10_WORD_FORM not in judgment_layers
    # JUDGMENT should only map to U7C
    assert ExecutionLayer.U7C_CLAUSE_SURFACE_AGREEMENT in judgment_layers


def test_wordform_domain_maps_to_u10():
    """Test that WORDFORM domain maps to U10_WORD_FORM execution layer."""
    wordform_layers = DAL_DOMAIN_TO_EXECUTION_LAYER_MAP.get(DalTransitionDomain.WORDFORM)
    assert wordform_layers is not None
    assert ExecutionLayer.U10_WORD_FORM in wordform_layers


def test_wordform_domain_maps_to_wordform_domain_type():
    """Test that WORDFORM maps to WORDFORM_DOMAIN type."""
    wordform_domains = DAL_DOMAIN_TO_DOMAIN_TYPE_MAP.get(DalTransitionDomain.WORDFORM)
    assert wordform_domains is not None
    assert DomainType.WORDFORM_DOMAIN in wordform_domains


def test_wordform_claim_scope_exists():
    """Test that WORDFORM_DETERMINED claim scope exists and maps correctly."""
    wordform_scopes = DAL_DOMAIN_TO_CLAIM_SCOPE_MAP.get(DalTransitionDomain.WORDFORM)
    assert wordform_scopes is not None
    assert DalClaimScope.WORDFORM_DETERMINED in wordform_scopes
