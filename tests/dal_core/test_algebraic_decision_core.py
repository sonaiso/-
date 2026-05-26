"""
Tests for Algebraic Decision Core

Tests the governance layer that audits all transitions in the Arabic linguistic pipeline.
"""

import pytest

from dal_core.algebraic_decision_core import (
    AlgebraicDecisionCore,
    CPBStatus,
    DecisionAudit,
    CPBIdentityGuardian,
)
from dal_core.identity_registry import IdentityType, IdentityRegistry
from dal_core.domain_registry import DomainType, DomainRegistry
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.foundation import Rank, ResidualSet, create_residual_set
from dal_core.residuals import make_info, make_blocker


# ============================================================================
# IdentityRegistry Tests
# ============================================================================

class TestIdentityRegistry:
    """Test identity classification and transition validation."""

    def test_registry_initialization(self):
        """Test that registry initializes with all identity types."""
        registry = IdentityRegistry()

        # Should have specs for all identity types
        spec = registry.get_spec(IdentityType.RAW_SURFACE_IDENTITY)
        assert spec.arabic_name == "سطح خام"

        spec = registry.get_spec(IdentityType.ROOT_MATERIAL_IDENTITY)
        assert spec.arabic_name == "مادة جذرية (مرشح)"
        assert spec.is_certificate is False  # Root in U₈ is candidate only

    def test_valid_identity_transition(self):
        """Test that valid identity transitions are allowed."""
        registry = IdentityRegistry()

        # RAW_SURFACE → ORTHOGRAPHIC is valid
        can_transition, reason = registry.can_transition(
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ORTHOGRAPHIC_IDENTITY,
            existing_identities=frozenset({IdentityType.RAW_SURFACE_IDENTITY})
        )

        assert can_transition is True
        assert reason is None

    def test_invalid_identity_transition(self):
        """Test that invalid identity transitions are blocked."""
        registry = IdentityRegistry()

        # RAW_SURFACE → ROOT_MATERIAL is invalid (skips many layers)
        can_transition, reason = registry.can_transition(
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,
            existing_identities=frozenset({IdentityType.RAW_SURFACE_IDENTITY})
        )

        assert can_transition is False
        assert reason is not None

    def test_forbidden_leap_root_before_license(self):
        """
        Test that root material identity cannot exist before licensed root input.

        Constitutional Law:
            لا RootMaterialIdentity قبل LicensedRootInputIdentity
        """
        registry = IdentityRegistry()

        # Attempt to go directly to ROOT_MATERIAL without LICENSED_ROOT_INPUT
        can_transition, reason = registry.can_transition(
            IdentityType.PROTECTED_CORE_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,
            existing_identities=frozenset({
                IdentityType.RAW_SURFACE_IDENTITY,
                IdentityType.PROTECTED_CORE_IDENTITY
                # Missing LICENSED_ROOT_INPUT_IDENTITY
            })
        )

        assert can_transition is False
        assert "Missing required identities" in reason

    def test_identity_sequence_validation(self):
        """Test validation of complete identity sequences."""
        registry = IdentityRegistry()

        # Valid sequence: RAW → ORTHOGRAPHIC → PHONETIC
        valid_sequence = (
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ORTHOGRAPHIC_IDENTITY,
            IdentityType.PHONETIC_IDENTITY,
        )

        is_valid, error = registry.validate_identity_sequence(valid_sequence)
        assert is_valid is True
        assert error is None

        # Invalid sequence: RAW → ROOT (skips intermediate)
        invalid_sequence = (
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,  # Skips many layers
        )

        is_valid, error = registry.validate_identity_sequence(invalid_sequence)
        assert is_valid is False
        assert error is not None


# ============================================================================
# DomainRegistry Tests
# ============================================================================

class TestDomainRegistry:
    """Test domain boundary enforcement."""

    def test_registry_initialization(self):
        """Test that registry initializes with all domains."""
        registry = DomainRegistry()

        spec = registry.get_spec(DomainType.WEIGHT_DOMAIN)
        assert spec.arabic_name == "مجال الوزن"

        spec = registry.get_spec(DomainType.SYNTAX_DOMAIN)
        assert spec.arabic_name == "مجال النحو"

    def test_domain_competency_checking(self):
        """Test that domain competencies are enforced."""
        registry = DomainRegistry()

        # WEIGHT_DOMAIN can determine weight_pattern
        can_determine, reason = registry.can_determine_in_domain(
            DomainType.WEIGHT_DOMAIN,
            "weight_pattern"
        )
        assert can_determine is True

        # WEIGHT_DOMAIN CANNOT determine meaning
        can_determine, reason = registry.can_determine_in_domain(
            DomainType.WEIGHT_DOMAIN,
            "meaning"
        )
        assert can_determine is False
        assert "prohibited" in reason

    def test_critical_domain_separation_faail(self):
        """
        Test critical separation: فاعل weight ≠ فاعل syntax ≠ فاعل meaning

        Constitutional Law:
            صيغة فاعل (WeightDomain) ≠ الفاعل النحوي (SyntaxDomain) ≠ معنى الفاعلية (SemanticsDomain)
        """
        registry = DomainRegistry()

        # Weight domain can determine morphological pattern "فاعل"
        weight_spec = registry.get_spec(DomainType.WEIGHT_DOMAIN)
        assert weight_spec.can_determine("morphological_template")

        # But CANNOT determine syntactic role
        assert weight_spec.is_prohibited("syntactic_role")

        # Syntax domain can determine syntactic "فاعل"
        syntax_spec = registry.get_spec(DomainType.SYNTAX_DOMAIN)
        assert syntax_spec.can_determine("faa_il_maf_ool")

        # But CANNOT determine meaning
        assert syntax_spec.is_prohibited("meaning")

    def test_domain_prohibitions(self):
        """Test that domain prohibitions are enforced."""
        registry = DomainRegistry()

        # ROOT_STEM_DOMAIN prohibits syntactic_role
        prohibitions = registry.get_prohibitions(DomainType.ROOT_STEM_DOMAIN)
        assert "syntactic_role" in prohibitions
        assert "meaning" in prohibitions
        assert "i3rab" in prohibitions

    def test_domain_transition_validation(self):
        """Test domain transition validation."""
        registry = DomainRegistry()

        # WEIGHT_DOMAIN → SYNTAX_DOMAIN is valid (through FUNCTIONAL_FORM)
        # But direct transition requires going through intermediate domains
        is_valid, reason = registry.validate_domain_transition(
            DomainType.WEIGHT_DOMAIN,
            DomainType.FUNCTIONAL_FORM_DOMAIN
        )
        assert is_valid is True


# ============================================================================
# CPBIdentityGuardian Tests
# ============================================================================

class TestCPBIdentityGuardian:
    """Test unified CPB guardian."""

    def test_guardian_initialization(self):
        """Test guardian initializes with registries."""
        identity_reg = IdentityRegistry()
        domain_reg = DomainRegistry()
        guardian = CPBIdentityGuardian(identity_reg, domain_reg)

        assert guardian.identity_registry is identity_reg
        assert guardian.domain_registry is domain_reg

    def test_identity_verification(self):
        """Test identity preservation verification."""
        identity_reg = IdentityRegistry()
        domain_reg = DomainRegistry()
        guardian = CPBIdentityGuardian(identity_reg, domain_reg)

        # Valid transition
        is_valid, reason = guardian.verify_identity(
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ORTHOGRAPHIC_IDENTITY,
            existing_identities=frozenset({IdentityType.RAW_SURFACE_IDENTITY})
        )
        assert is_valid is True

    def test_domain_verification(self):
        """Test domain boundary verification."""
        identity_reg = IdentityRegistry()
        domain_reg = DomainRegistry()
        guardian = CPBIdentityGuardian(identity_reg, domain_reg)

        # Valid determination in domain
        is_valid, reason = guardian.verify_domain(
            DomainType.WEIGHT_DOMAIN,
            "weight_pattern"
        )
        assert is_valid is True

        # Invalid determination (meaning in weight domain)
        is_valid, reason = guardian.verify_domain(
            DomainType.WEIGHT_DOMAIN,
            "meaning"
        )
        assert is_valid is False

    def test_rank_verification(self):
        """Test rank progression verification."""
        identity_reg = IdentityRegistry()
        domain_reg = DomainRegistry()
        guardian = CPBIdentityGuardian(identity_reg, domain_reg)

        # Valid progression: ZERO → CANDIDATE
        is_valid, reason = guardian.verify_rank(
            Rank.ZERO,
            Rank.CANDIDATE
        )
        assert is_valid is True

        # Invalid progression: ZERO → CERTIFICATE (skips levels)
        is_valid, reason = guardian.verify_rank(
            Rank.ZERO,
            Rank.CERTIFICATE
        )
        assert is_valid is False

    def test_residuals_verification(self):
        """Test residual blocking verification."""
        identity_reg = IdentityRegistry()
        domain_reg = DomainRegistry()
        guardian = CPBIdentityGuardian(identity_reg, domain_reg)

        # No blocking residuals - should pass
        info_residual = make_info("test", "Test info")
        residual_set = create_residual_set(frozenset({info_residual}))

        is_valid, reason = guardian.verify_residuals(residual_set)
        assert is_valid is True

        # Blocking residual - should fail
        blocker = make_blocker("test_blocker", "Test blocker")
        residual_set_blocking = create_residual_set(frozenset({blocker}))

        is_valid, reason = guardian.verify_residuals(residual_set_blocking)
        assert is_valid is False
        assert "blocking" in reason

    def test_forbidden_leap_verification(self):
        """Test forbidden layer leap detection."""
        identity_reg = IdentityRegistry()
        domain_reg = DomainRegistry()
        guardian = CPBIdentityGuardian(identity_reg, domain_reg)

        # Valid transition: U₂s → U₃
        is_valid, reason = guardian.verify_no_forbidden_leap(
            ExecutionLayer.U2S_ARABIC_SYLLABLE,
            ExecutionLayer.U3_BOUNDARY_ATTACHMENT
        )
        assert is_valid is True

        # Forbidden leap: U₂s → U₅ (skips U₃, U₄)
        is_valid, reason = guardian.verify_no_forbidden_leap(
            ExecutionLayer.U2S_ARABIC_SYLLABLE,
            ExecutionLayer.U5_FUNCTIONAL_ROLE
        )
        assert is_valid is False


# ============================================================================
# AlgebraicDecisionCore Tests
# ============================================================================

class TestAlgebraicDecisionCore:
    """Test complete governance system."""

    def test_core_initialization(self):
        """Test core initializes with all components."""
        core = AlgebraicDecisionCore()

        assert core.identity_registry is not None
        assert core.domain_registry is not None
        assert core.cpb is not None

    def test_approved_decision(self):
        """Test decision that passes all checks."""
        core = AlgebraicDecisionCore()

        # Create valid decision parameters
        audit = core.decide_transition(
            transition_id="U0_to_U1",
            from_layer=ExecutionLayer.U0_UNICODE,
            to_layer=ExecutionLayer.U1_GRAPHEME,
            input_identity=IdentityType.RAW_SURFACE_IDENTITY,
            output_identity=IdentityType.ORTHOGRAPHIC_IDENTITY,
            existing_identities=frozenset({IdentityType.RAW_SURFACE_IDENTITY}),
            domain=DomainType.SCRIPT_DOMAIN,
            attempted_determination="character_classification",
            gate_name="GraphemeGate",
            gate_passed=True,
            evidence=("unicode_validation",),
            required_evidence=frozenset({"unicode_validation"}),
            input_rank=Rank.ZERO,
            output_rank=Rank.CANDIDATE,
            residual_set=create_residual_set(frozenset()),
            trace=("U0_processing", "grapheme_detection")
        )

        assert audit.is_approved() is True
        assert audit.cpb_status == CPBStatus.APPROVED
        assert len(audit.violations) == 0

    def test_rejected_decision_identity_violation(self):
        """Test decision rejected due to identity violation."""
        core = AlgebraicDecisionCore()

        # Attempt forbidden identity leap: RAW → ROOT
        audit = core.decide_transition(
            transition_id="INVALID_U0_to_U8",
            from_layer=ExecutionLayer.U0_UNICODE,
            to_layer=ExecutionLayer.U8_ROOT_STEM,
            input_identity=IdentityType.RAW_SURFACE_IDENTITY,
            output_identity=IdentityType.ROOT_MATERIAL_IDENTITY,  # Invalid leap
            existing_identities=frozenset({IdentityType.RAW_SURFACE_IDENTITY}),
            domain=DomainType.ROOT_STEM_DOMAIN,
            attempted_determination="root_candidate_extraction",
            gate_name="RootGate",
            gate_passed=True,
            evidence=("surface_analysis",),
            required_evidence=frozenset({"surface_analysis"}),
            input_rank=Rank.ZERO,
            output_rank=Rank.CANDIDATE,
            residual_set=create_residual_set(frozenset()),
            trace=("invalid_processing",)
        )

        assert audit.is_approved() is False
        assert audit.cpb_status == CPBStatus.IDENTITY_VIOLATION
        assert len(audit.violations) > 0

    def test_rejected_decision_domain_violation(self):
        """Test decision rejected due to domain violation."""
        core = AlgebraicDecisionCore()

        # Attempt to determine meaning in weight domain (forbidden)
        audit = core.decide_transition(
            transition_id="U8_to_U9",
            from_layer=ExecutionLayer.U8_ROOT_STEM,
            to_layer=ExecutionLayer.U9_WEIGHT,
            input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
            output_identity=IdentityType.WEIGHT_IDENTITY,
            existing_identities=frozenset({
                IdentityType.RAW_SURFACE_IDENTITY,
                IdentityType.ORTHOGRAPHIC_IDENTITY,
                IdentityType.ROOT_MATERIAL_IDENTITY
            }),
            domain=DomainType.WEIGHT_DOMAIN,
            attempted_determination="meaning",  # Forbidden in weight domain
            gate_name="WeightGate",
            gate_passed=True,
            evidence=("weight_pattern",),
            required_evidence=frozenset({"weight_pattern"}),
            input_rank=Rank.CANDIDATE,
            output_rank=Rank.HYPOTHESIS,
            residual_set=create_residual_set(frozenset()),
            trace=("weight_processing",)
        )

        assert audit.is_approved() is False
        assert audit.cpb_status == CPBStatus.DOMAIN_VIOLATION
        assert any("meaning" in v for v in audit.violations)

    def test_rejected_decision_blocking_residual(self):
        """Test decision rejected due to blocking residual."""
        core = AlgebraicDecisionCore()

        # Create blocking residual
        blocker = make_blocker("root_extraction_blocked", "Proper name requires lexical attestation")

        audit = core.decide_transition(
            transition_id="U7C_to_U8",
            from_layer=ExecutionLayer.U7C_CLAUSE_SURFACE_AGREEMENT,
            to_layer=ExecutionLayer.U8_ROOT_STEM,
            input_identity=IdentityType.LICENSED_ROOT_INPUT_IDENTITY,
            output_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
            existing_identities=frozenset({
                IdentityType.RAW_SURFACE_IDENTITY,
                IdentityType.LICENSED_ROOT_INPUT_IDENTITY
            }),
            domain=DomainType.ROOT_STEM_DOMAIN,
            attempted_determination="root_candidate_extraction",
            gate_name="RootInputGate",
            gate_passed=True,
            evidence=("license_permission",),
            required_evidence=frozenset({"license_permission"}),
            input_rank=Rank.CANDIDATE,
            output_rank=Rank.CANDIDATE,
            residual_set=create_residual_set(frozenset({blocker})),
            trace=("U7C_agreement", "U8_root_attempt")
        )

        assert audit.is_approved() is False
        assert audit.cpb_status == CPBStatus.RESIDUAL_BLOCKING
        assert len(audit.get_blocking_residuals()) == 1

    def test_rejected_decision_forbidden_leap(self):
        """Test decision rejected due to forbidden layer leap."""
        core = AlgebraicDecisionCore()

        # Attempt forbidden leap: U₂s → U₈ (skips U₃, U₄, U₅, U₆, U₇)
        audit = core.decide_transition(
            transition_id="FORBIDDEN_U2S_to_U8",
            from_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
            to_layer=ExecutionLayer.U8_ROOT_STEM,
            input_identity=IdentityType.SYLLABIC_IDENTITY,
            output_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
            existing_identities=frozenset({IdentityType.SYLLABIC_IDENTITY}),
            domain=DomainType.ROOT_STEM_DOMAIN,
            attempted_determination="root_candidate_extraction",
            gate_name="RootGate",
            gate_passed=True,
            evidence=("syllable_analysis",),
            required_evidence=frozenset({"syllable_analysis"}),
            input_rank=Rank.CANDIDATE,
            output_rank=Rank.CANDIDATE,
            residual_set=create_residual_set(frozenset()),
            trace=("syllable_processing",)
        )

        assert audit.is_approved() is False
        assert audit.cpb_status == CPBStatus.FORBIDDEN_LEAP
        assert any("Forbidden leap" in v for v in audit.violations)


# ============================================================================
# Integration Tests
# ============================================================================

class TestAlgebraicDecisionCoreIntegration:
    """Integration tests for complete decision auditing."""

    def test_complete_valid_pipeline_u0_to_u3(self):
        """Test complete valid decision pipeline U₀ → U₁ → U₂p → U₂s → U₃."""
        core = AlgebraicDecisionCore()

        existing = frozenset({IdentityType.RAW_SURFACE_IDENTITY})

        # U₀ → U₁
        audit1 = core.decide_transition(
            transition_id="U0_to_U1",
            from_layer=ExecutionLayer.U0_UNICODE,
            to_layer=ExecutionLayer.U1_GRAPHEME,
            input_identity=IdentityType.RAW_SURFACE_IDENTITY,
            output_identity=IdentityType.ORTHOGRAPHIC_IDENTITY,
            existing_identities=existing,
            domain=DomainType.SCRIPT_DOMAIN,
            attempted_determination="character_classification",
            gate_name="GraphemeGate",
            gate_passed=True,
            evidence=("unicode_validation",),
            required_evidence=frozenset({"unicode_validation"}),
            input_rank=Rank.ZERO,
            output_rank=Rank.CANDIDATE,
            residual_set=create_residual_set(frozenset()),
            trace=("U0",)
        )

        assert audit1.is_approved()
        existing = existing | {IdentityType.ORTHOGRAPHIC_IDENTITY}

        # U₁ → U₂p
        audit2 = core.decide_transition(
            transition_id="U1_to_U2p",
            from_layer=ExecutionLayer.U1_GRAPHEME,
            to_layer=ExecutionLayer.U2P_PHONETIC_PROJECTION,
            input_identity=IdentityType.ORTHOGRAPHIC_IDENTITY,
            output_identity=IdentityType.PHONETIC_IDENTITY,
            existing_identities=existing,
            domain=DomainType.SOUND_DOMAIN,
            attempted_determination="phoneme_classification",
            gate_name="PhoneticGate",
            gate_passed=True,
            evidence=("grapheme_analysis",),
            required_evidence=frozenset({"grapheme_analysis"}),
            input_rank=Rank.CANDIDATE,
            output_rank=Rank.CANDIDATE,
            residual_set=create_residual_set(frozenset()),
            trace=("U0", "U1")
        )

        assert audit2.is_approved()
        existing = existing | {IdentityType.PHONETIC_IDENTITY}

        # U₂p → U₂s
        audit3 = core.decide_transition(
            transition_id="U2p_to_U2s",
            from_layer=ExecutionLayer.U2P_PHONETIC_PROJECTION,
            to_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
            input_identity=IdentityType.PHONETIC_IDENTITY,
            output_identity=IdentityType.SYLLABIC_IDENTITY,
            existing_identities=existing,
            domain=DomainType.SYLLABLE_DOMAIN,
            attempted_determination="syllable_structure",
            gate_name="SyllableGate",
            gate_passed=True,
            evidence=("phonetic_sequence",),
            required_evidence=frozenset({"phonetic_sequence"}),
            input_rank=Rank.CANDIDATE,
            output_rank=Rank.CANDIDATE,
            residual_set=create_residual_set(frozenset()),
            trace=("U0", "U1", "U2p")
        )

        assert audit3.is_approved()
        existing = existing | {IdentityType.SYLLABIC_IDENTITY}

        # U₂s → U₃
        audit4 = core.decide_transition(
            transition_id="U2s_to_U3",
            from_layer=ExecutionLayer.U2S_ARABIC_SYLLABLE,
            to_layer=ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
            input_identity=IdentityType.SYLLABIC_IDENTITY,
            output_identity=IdentityType.BOUNDARY_IDENTITY,
            existing_identities=existing,
            domain=DomainType.BOUNDARY_DOMAIN,
            attempted_determination="word_boundary_detection",
            gate_name="BoundaryGate",
            gate_passed=True,
            evidence=("syllable_pattern",),
            required_evidence=frozenset({"syllable_pattern"}),
            input_rank=Rank.CANDIDATE,
            output_rank=Rank.CANDIDATE,
            residual_set=create_residual_set(frozenset()),
            trace=("U0", "U1", "U2p", "U2s")
        )

        assert audit4.is_approved()
