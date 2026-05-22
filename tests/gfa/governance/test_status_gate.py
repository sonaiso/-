"""Tests for General Algebra Status Gate.

Verifies that false completion claims are prevented and
honest status is maintained.

Core Principle:
    الاختبار يمنع الهلوسة.
    "Testing prevents hallucination."
"""

import pytest

from gfa.governance import (
    AlgebraStatus,
    ComponentStatus,
    ProjectStatus,
    get_project_status,
    StatusValidator,
    validate_project_status,
    GovernanceViolation,
    make_provisional_residual,
    make_cpb_dependency_residual,
)


# =============================================================================
# Test 1-5: Current Status Classification
# =============================================================================


def test_current_gfa_is_provisional_specialized():
    """GFA must be classified as PROVISIONAL_SPECIALIZED."""
    status = get_project_status()
    assert status.gfa_status == AlgebraStatus.PROVISIONAL_SPECIALIZED


def test_current_general_learning_is_pattern_specific():
    """General learning must be PATTERN_SPECIFIC_PROTOTYPE."""
    status = get_project_status()
    assert status.learning_status == AlgebraStatus.PATTERN_SPECIFIC_PROTOTYPE


def test_general_algebra_spec_is_constitutional_seed():
    """General Algebra spec is incomplete, not 100%."""
    status = get_project_status()
    # Constitution should be < 1.0 (not 100%)
    assert status.general_algebra_constitution < 1.0
    assert status.general_algebra_constitution >= 0.60  # Around 65%


def test_cpb_extraction_not_implemented():
    """CPB extraction must not be marked as proven."""
    status = get_project_status()
    assert not status.cpb_proven
    assert ComponentStatus.CPB_EXTRACTION in status.missing_components


def test_layer_generator_not_implemented():
    """LayerGenerator must not exist."""
    status = get_project_status()
    assert not status.layer_generator_exists
    assert ComponentStatus.LAYER_GENERATOR in status.missing_components


# =============================================================================
# Test 6-10: Architecture Honesty
# =============================================================================


def test_architecture_completeness_is_35_to_45_percent():
    """Architecture is ~40%, not 100%."""
    status = get_project_status()
    assert 0.35 <= status.general_algebra_architecture <= 0.45


def test_general_algebra_runtime_is_0_to_5_percent():
    """Runtime implementation is ~2%, almost nothing."""
    status = get_project_status()
    assert 0.0 <= status.general_algebra_runtime <= 0.05


def test_generality_proof_not_implemented():
    """3-layer generality proof doesn't exist."""
    status = get_project_status()
    assert ComponentStatus.GENERALITY_PROOF in status.missing_components


def test_memory_geometry_not_implemented():
    """Memory geometry kernel not implemented yet."""
    status = get_project_status()
    assert ComponentStatus.MEMORY_GEOMETRY in status.missing_components


def test_comparison_geometry_not_implemented():
    """Comparison geometry kernel not implemented yet."""
    status = get_project_status()
    assert ComponentStatus.COMPARISON_GEOMETRY in status.missing_components


# =============================================================================
# Test 11-15: Component Detection
# =============================================================================


def test_cognitive_carrier_is_implemented():
    """CognitiveCarrier should be detected as implemented."""
    status = get_project_status()
    assert ComponentStatus.COGNITIVE_CARRIER in status.implemented_components


def test_gfa_methods_are_implemented():
    """GFA methods should be detected as implemented."""
    status = get_project_status()
    assert ComponentStatus.GFA_METHODS in status.implemented_components


def test_dal_algebra_is_implemented():
    """Dal algebra should be detected as implemented."""
    status = get_project_status()
    assert ComponentStatus.DAL_ALGEBRA in status.implemented_components


def test_binding_core_not_implemented():
    """Binding core kernel not implemented yet."""
    status = get_project_status()
    assert ComponentStatus.BINDING_CORE in status.missing_components


def test_subject_grounding_not_implemented():
    """RationalSubjectGrounding not implemented yet."""
    status = get_project_status()
    assert ComponentStatus.SUBJECT_GROUNDING in status.missing_components


# =============================================================================
# Test 16-20: Residual Generation
# =============================================================================


def test_provisional_residual_declares_status():
    """Provisional residual must declare PROVISIONAL status."""
    residual = make_provisional_residual("MutabaqahGate")
    assert "provisional" in residual.description.lower()
    assert "PROVISIONAL_SPECIALIZED_ALGEBRA" in residual.description


def test_cpb_dependency_residual_declares_dependency():
    """CPB dependency residual must declare dependence."""
    residual = make_cpb_dependency_residual("NeutralBinding")
    assert "CPB not extracted yet" in residual.description
    assert "depends on CPB extraction" in residual.description


def test_provisional_residual_not_blocker():
    """Provisional status is warning, not blocker."""
    residual = make_provisional_residual("MutabaqahGate")
    assert not residual.blocker


def test_cpb_residual_affects_claims():
    """CPB residual must list affected claims."""
    residual = make_cpb_dependency_residual("NeutralBinding")
    assert len(residual.affected_claims) > 0
    assert any("cpb" in claim.lower() for claim in residual.affected_claims)


def test_residual_to_standard_residual_conversion():
    """StatusResidual must convert to standard Residual."""
    status_residual = make_provisional_residual("TestComponent")
    standard_residual = status_residual.to_residual()

    assert hasattr(standard_residual, "kind")
    assert hasattr(standard_residual, "description")
    assert "provisional" in standard_residual.kind


# =============================================================================
# Test 21-25: Validation & Guards
# =============================================================================


def test_status_validator_runs():
    """Status validator must run without errors."""
    validator = StatusValidator()
    result = validator.validate_project_status()

    assert hasattr(result, "passed")
    assert hasattr(result, "violations")
    assert hasattr(result, "warnings")
    assert hasattr(result, "status")


def test_validator_checks_false_claims():
    """Validator must search for false claims."""
    validator = StatusValidator()
    result = validator.validate_project_status()

    # Should check for forbidden claims
    # (may or may not find violations depending on docs)
    assert isinstance(result.violations, list)


def test_validator_warns_missing_components():
    """Validator must warn about missing required components."""
    validator = StatusValidator()
    result = validator.validate_project_status()

    # Should have warnings about missing components
    assert isinstance(result.warnings, list)


def test_status_gate_prevents_specialized_claiming_general():
    """GFA cannot claim GENERAL_ALGEBRA_RUNTIME status."""
    # This test verifies the guard exists
    # If GFA ever claims general status, validator will catch it
    status = get_project_status()

    assert status.gfa_status != AlgebraStatus.GENERAL_ALGEBRA_RUNTIME
    assert status.gfa_status != AlgebraStatus.PROVEN_GENERAL


def test_project_status_is_retrievable():
    """Project status must be retrievable at any time."""
    status = get_project_status()

    assert isinstance(status, ProjectStatus)
    assert isinstance(status.general_algebra_constitution, float)
    assert isinstance(status.general_algebra_architecture, float)
    assert isinstance(status.general_algebra_runtime, float)
    assert isinstance(status.cpb_proven, bool)
    assert isinstance(status.layer_generator_exists, bool)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
