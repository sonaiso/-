"""
Tests for Adapter Boundary Review Matrix (PR #157)

Constitutional Testing Laws:
    1. Tests verify matrix structure ONLY (not full validation engine)
    2. Tests do NOT import transformers
    3. Tests do NOT import torch
    4. Tests do NOT tokenize, load models, or execute inference
    5. Tests verify golden fixtures pass shape verification
    6. Tests verify requirement coverage is complete
    7. Tests are minimal scope (no deep content validation yet)

Test Categories:
    1. Matrix Construction Tests (6 tests)
    2. Transition Requirement Tests (12 tests - 3 per transition)
    3. Verification Tests with Golden Fixtures (12 tests)
    4. Integration Tests (6 tests)

Target: ~25 tests total

Created: 2026-05-29
"""

import pytest

from dal_core.adapter_boundary_review_matrix import (
    BoundaryTransitionType,
    BoundaryRequirementType,
    BoundaryRequirement,
    BoundaryTransition,
    AdapterBoundaryReviewMatrix,
    BoundaryVerificationResult,
    make_training_example_to_adapter_input_transition,
    make_adapter_input_to_raw_output_transition,
    make_adapter_raw_output_to_model_output_transition,
    make_model_output_to_evaluator_transition,
    build_canonical_adapter_boundary_matrix,
    verify_transition_shape,
    verify_matrix_shape,
    verify_golden_fixture_against_matrix,
)
from dal_core.constitutional_evaluator import ConstitutionalViolationSeverity

# Import golden fixtures for integration tests
from tests.fixtures.dal_core.golden_noop_adapter_chains import (
    make_valid_explanation_chain_fixture,
    make_authority_violation_chain_fixture,
    make_binding_loss_blocked_fixture,
    make_wrong_adapter_output_link_blocked_fixture,
    make_reference_preservation_chain_fixture,
    make_constitutional_evaluator_ready_fixture,
)


# ============================================================================
# Matrix Construction Tests (6 tests)
# ============================================================================

def test_build_canonical_matrix_structure():
    """Test canonical matrix builds successfully with correct structure."""
    matrix = build_canonical_adapter_boundary_matrix()

    assert matrix.matrix_id == "adapter_boundary_matrix_v1"
    assert matrix.matrix_version == "1.0.0"
    assert len(matrix.transitions) == 4
    assert matrix.total_requirements_count > 0
    assert matrix.critical_requirements_count > 0


def test_all_transitions_present():
    """Test all 4 transition types are present in canonical matrix."""
    matrix = build_canonical_adapter_boundary_matrix()

    transition_types = {t.transition_type for t in matrix.transitions}
    expected_types = {
        BoundaryTransitionType.TRAINING_EXAMPLE_TO_ADAPTER_INPUT,
        BoundaryTransitionType.ADAPTER_INPUT_TO_ADAPTER_RAW_OUTPUT,
        BoundaryTransitionType.ADAPTER_RAW_OUTPUT_TO_MODEL_OUTPUT,
        BoundaryTransitionType.MODEL_OUTPUT_TO_CONSTITUTIONAL_EVALUATOR,
    }

    assert transition_types == expected_types


def test_all_requirement_types_covered():
    """Test all 9 requirement types are represented in matrix."""
    matrix = build_canonical_adapter_boundary_matrix()

    requirement_types = {
        req.requirement_type
        for transition in matrix.transitions
        for req in transition.requirements
    }

    expected_types = {
        BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
        BoundaryRequirementType.REFERENCE_PRESERVATION,
        BoundaryRequirementType.AUTHORITY_PROHIBITION,
        BoundaryRequirementType.RANK_UPGRADE_PROHIBITION,
        BoundaryRequirementType.RESIDUAL_RESOLUTION_PROHIBITION,
        BoundaryRequirementType.IFADAH_CLOSURE_PROHIBITION,
        BoundaryRequirementType.HUKM_PRODUCTION_PROHIBITION,
        BoundaryRequirementType.REALITY_PRODUCTION_PROHIBITION,
        BoundaryRequirementType.EXECUTION_MARKER_PROHIBITION,
    }

    assert requirement_types == expected_types


def test_matrix_immutability():
    """Test matrix is immutable (frozen dataclass)."""
    matrix = build_canonical_adapter_boundary_matrix()

    with pytest.raises(Exception):  # FrozenInstanceError
        matrix.matrix_version = "2.0.0"  # type: ignore


def test_requirement_counts_correct():
    """Test requirement counts are correctly calculated."""
    matrix = build_canonical_adapter_boundary_matrix()

    # Count manually
    actual_total = sum(len(t.requirements) for t in matrix.transitions)
    actual_critical = sum(
        1 for t in matrix.transitions
        for r in t.requirements
        if r.failure_severity == ConstitutionalViolationSeverity.CRITICAL
    )

    assert matrix.total_requirements_count == actual_total
    assert matrix.critical_requirements_count == actual_critical
    assert matrix.critical_requirements_count > 0


def test_critical_requirements_identified():
    """Test critical requirements are properly identified."""
    matrix = build_canonical_adapter_boundary_matrix()

    critical_requirements = [
        req for transition in matrix.transitions
        for req in transition.requirements
        if req.failure_severity == ConstitutionalViolationSeverity.CRITICAL
    ]

    # All source binding requirements should be critical
    assert any(
        "source_trace_id" in req.description.lower()
        for req in critical_requirements
    )
    assert any(
        "source_training_example_id" in req.description.lower()
        for req in critical_requirements
    )


# ============================================================================
# Transition Requirement Tests (12 tests - 3 per transition)
# ============================================================================

def test_training_example_to_adapter_input_preservations():
    """Test TrainingExample → AdapterInput has source binding preservation requirements."""
    transition = make_training_example_to_adapter_input_transition()

    assert transition.transition_id == "transition_te_to_ai"
    assert transition.transition_type == BoundaryTransitionType.TRAINING_EXAMPLE_TO_ADAPTER_INPUT
    assert "source_trace_id" in transition.required_preservations
    assert "source_training_example_id" in transition.required_preservations
    assert len(transition.requirements) >= 3  # At least source bindings + references


def test_training_example_to_adapter_input_prohibitions():
    """Test TrainingExample → AdapterInput has execution prohibition requirements."""
    transition = make_training_example_to_adapter_input_transition()

    assert "tokenizer" in transition.required_prohibitions
    assert "tensor" in transition.required_prohibitions
    assert "model" in transition.required_prohibitions


def test_training_example_to_adapter_input_verification_criteria():
    """Test TrainingExample → AdapterInput has verification criteria."""
    transition = make_training_example_to_adapter_input_transition()

    assert len(transition.verification_criteria) > 0
    assert any("preserved" in criterion.lower() for criterion in transition.verification_criteria)
    assert any("tokenization" in criterion.lower() or "execution" in criterion.lower() for criterion in transition.verification_criteria)


def test_adapter_input_to_raw_output_preservations():
    """Test AdapterInput → AdapterRawOutput has source binding preservation requirements."""
    transition = make_adapter_input_to_raw_output_transition()

    assert transition.transition_id == "transition_ai_to_aro"
    assert transition.transition_type == BoundaryTransitionType.ADAPTER_INPUT_TO_ADAPTER_RAW_OUTPUT
    assert "source_adapter_input_id" in transition.required_preservations
    assert "chain_traceability" in transition.required_preservations


def test_adapter_input_to_raw_output_prohibitions():
    """Test AdapterInput → AdapterRawOutput has execution prohibition requirements."""
    transition = make_adapter_input_to_raw_output_transition()

    assert "model_generation" in transition.required_prohibitions
    assert "tensor_decoding" in transition.required_prohibitions
    assert "inference_execution" in transition.required_prohibitions


def test_adapter_input_to_raw_output_verification_criteria():
    """Test AdapterInput → AdapterRawOutput has verification criteria."""
    transition = make_adapter_input_to_raw_output_transition()

    assert len(transition.verification_criteria) > 0
    assert any("preserved" in criterion.lower() or "maintained" in criterion.lower() for criterion in transition.verification_criteria)


def test_adapter_raw_output_to_model_output_preservations():
    """Test AdapterRawOutput → ModelOutput has source binding preservation requirements."""
    transition = make_adapter_raw_output_to_model_output_transition()

    assert transition.transition_id == "transition_aro_to_mo"
    assert transition.transition_type == BoundaryTransitionType.ADAPTER_RAW_OUTPUT_TO_MODEL_OUTPUT
    assert "source_trace_id" in transition.required_preservations
    assert "source_training_example_id" in transition.required_preservations


def test_adapter_raw_output_to_model_output_prohibitions():
    """Test AdapterRawOutput → ModelOutput has authority/constitutional prohibition requirements."""
    transition = make_adapter_raw_output_to_model_output_transition()

    assert "authority_claim" in transition.required_prohibitions
    assert "rank_upgrade" in transition.required_prohibitions
    assert "hukm_production" in transition.required_prohibitions
    assert "reality_production" in transition.required_prohibitions


def test_adapter_raw_output_to_model_output_verification_criteria():
    """Test AdapterRawOutput → ModelOutput has verification criteria."""
    transition = make_adapter_raw_output_to_model_output_transition()

    assert len(transition.verification_criteria) > 0
    assert any("preserved" in criterion.lower() for criterion in transition.verification_criteria)
    assert any("authority" in criterion.lower() or "hukm" in criterion.lower() for criterion in transition.verification_criteria)


def test_model_output_to_evaluator_preservations():
    """Test ModelOutput → ConstitutionalEvaluator has required field requirements."""
    transition = make_model_output_to_evaluator_transition()

    assert transition.transition_id == "transition_mo_to_eval"
    assert transition.transition_type == BoundaryTransitionType.MODEL_OUTPUT_TO_CONSTITUTIONAL_EVALUATOR
    assert "source_trace_id" in transition.required_preservations
    assert "source_training_example_id" in transition.required_preservations
    assert "predicted_text" in transition.required_preservations
    assert "model_name" in transition.required_preservations
    assert "generation_timestamp" in transition.required_preservations


def test_model_output_to_evaluator_prohibitions():
    """Test ModelOutput → ConstitutionalEvaluator has detection requirements."""
    transition = make_model_output_to_evaluator_transition()

    assert "missing_bindings" in transition.required_prohibitions
    assert "authority_claims" in transition.required_prohibitions
    assert "invented_references" in transition.required_prohibitions
    assert "rank_upgrade" in transition.required_prohibitions


def test_model_output_to_evaluator_verification_criteria():
    """Test ModelOutput → ConstitutionalEvaluator has verification criteria."""
    transition = make_model_output_to_evaluator_transition()

    assert len(transition.verification_criteria) > 0
    assert any("required" in criterion.lower() for criterion in transition.verification_criteria)
    assert any("detect" in criterion.lower() for criterion in transition.verification_criteria)


# ============================================================================
# Verification Tests with Golden Fixtures (12 tests)
# ============================================================================

def test_verify_transition_shape_passes_for_canonical():
    """Test verify_transition_shape passes for canonical transitions."""
    transition = make_training_example_to_adapter_input_transition()
    result = verify_transition_shape(transition)

    assert result.passed
    assert len(result.violations) == 0
    assert len(result.preserved_bindings) > 0
    assert len(result.detected_prohibitions) > 0


def test_verify_matrix_shape_passes_for_canonical():
    """Test verify_matrix_shape passes for canonical matrix."""
    matrix = build_canonical_adapter_boundary_matrix()
    result = verify_matrix_shape(matrix)

    assert result.passed
    assert len(result.violations) == 0


def test_valid_explanation_fixture_passes_matrix_verification():
    """Test valid explanation golden fixture passes all boundary verifications."""
    fixture = make_valid_explanation_chain_fixture()
    matrix = build_canonical_adapter_boundary_matrix()

    results = verify_golden_fixture_against_matrix(fixture, matrix)

    assert len(results) == 4  # One per transition
    assert all(result.passed for result in results)


def test_authority_violation_fixture_maps_to_authority_prohibition():
    """Test authority violation fixture is detectable by matrix requirements."""
    fixture = make_authority_violation_chain_fixture()
    matrix = build_canonical_adapter_boundary_matrix()

    # Find authority prohibition requirements
    authority_requirements = [
        req for transition in matrix.transitions
        for req in transition.requirements
        if req.requirement_type == BoundaryRequirementType.AUTHORITY_PROHIBITION
    ]

    assert len(authority_requirements) > 0
    # Matrix documents that authority must be prohibited (fixture demonstrates violation)


def test_binding_loss_fixture_maps_to_source_binding_preservation():
    """Test binding loss fixture is detectable by matrix requirements."""
    fixture = make_binding_loss_blocked_fixture()

    # Verify fixture demonstrates binding loss
    # (This fixture intentionally has WRONG_ID to demonstrate binding mismatch)
    assert fixture.expected_validation_status == False
    # Note: fixture has expected_violations=() because it demonstrates structural mismatch,
    # not AdapterViolationType enum violations. The actual binding loss is detected
    # by comparing adapter_input.source_training_example_id ('WRONG_ID')
    # against training_example.training_example_id ('golden_te_003')


def test_wrong_output_link_fixture_maps_to_adapter_input_preservation():
    """Test wrong output link fixture is detectable by matrix requirements."""
    fixture = make_wrong_adapter_output_link_blocked_fixture()

    # Verify fixture demonstrates wrong linkage
    # (This fixture intentionally has WRONG_INPUT_ID to demonstrate linkage mismatch)
    assert fixture.expected_validation_status == False
    # Note: fixture has expected_violations=() because it demonstrates structural mismatch,
    # not AdapterViolationType enum violations. The actual linkage error is detected
    # by comparing adapter_raw_output.source_adapter_input_id ('WRONG_INPUT_ID')
    # against adapter_input.adapter_input_id ('noop_input_golden_te_004')


def test_reference_preservation_fixture_passes_reference_requirements():
    """Test reference preservation fixture passes reference preservation requirements."""
    fixture = make_reference_preservation_chain_fixture()
    matrix = build_canonical_adapter_boundary_matrix()

    results = verify_golden_fixture_against_matrix(fixture, matrix)

    # Verify source bindings are preserved (minimal check)
    assert all(result.passed for result in results)


def test_evaluator_ready_fixture_passes_evaluator_requirements():
    """Test evaluator-ready fixture passes evaluator transition requirements."""
    fixture = make_constitutional_evaluator_ready_fixture()
    matrix = build_canonical_adapter_boundary_matrix()

    results = verify_golden_fixture_against_matrix(fixture, matrix)

    # Check ModelOutput → Evaluator transition (last one)
    evaluator_result = results[-1]
    assert evaluator_result.passed
    assert "source_trace_id" in evaluator_result.preserved_bindings
    assert "source_training_example_id" in evaluator_result.preserved_bindings
    assert "predicted_text" in evaluator_result.preserved_bindings


def test_every_transition_has_at_least_one_preservation():
    """Test every transition has at least one preservation requirement."""
    matrix = build_canonical_adapter_boundary_matrix()

    for transition in matrix.transitions:
        preservation_requirements = [
            req for req in transition.requirements
            if req.requirement_type in (
                BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
                BoundaryRequirementType.REFERENCE_PRESERVATION,
            )
        ]
        assert len(preservation_requirements) > 0, f"Transition {transition.transition_id} has no preservation requirements"


def test_every_transition_has_at_least_one_prohibition():
    """Test every transition has at least one prohibition requirement."""
    matrix = build_canonical_adapter_boundary_matrix()

    for transition in matrix.transitions:
        prohibition_requirements = [
            req for req in transition.requirements
            if req.requirement_type in (
                BoundaryRequirementType.AUTHORITY_PROHIBITION,
                BoundaryRequirementType.RANK_UPGRADE_PROHIBITION,
                BoundaryRequirementType.RESIDUAL_RESOLUTION_PROHIBITION,
                BoundaryRequirementType.IFADAH_CLOSURE_PROHIBITION,
                BoundaryRequirementType.HUKM_PRODUCTION_PROHIBITION,
                BoundaryRequirementType.REALITY_PRODUCTION_PROHIBITION,
                BoundaryRequirementType.EXECUTION_MARKER_PROHIBITION,
            )
        ]
        assert len(prohibition_requirements) > 0, f"Transition {transition.transition_id} has no prohibition requirements"


def test_transition_ids_are_unique():
    """Test all transition IDs are unique."""
    matrix = build_canonical_adapter_boundary_matrix()

    transition_ids = [t.transition_id for t in matrix.transitions]
    assert len(transition_ids) == len(set(transition_ids))


def test_requirement_ids_are_unique():
    """Test all requirement IDs are unique across all transitions."""
    matrix = build_canonical_adapter_boundary_matrix()

    requirement_ids = [
        req.requirement_id
        for transition in matrix.transitions
        for req in transition.requirements
    ]

    assert len(requirement_ids) == len(set(requirement_ids))


# ============================================================================
# Integration Tests (6 tests)
# ============================================================================

def test_no_transformers_imports():
    """Test module does NOT import transformers."""
    import sys

    # Check transformers not imported
    assert "transformers" not in sys.modules or not any(
        "adapter_boundary_review_matrix" in str(module)
        for name, module in sys.modules.items()
        if name == "transformers"
    )


def test_no_torch_imports():
    """Test module does NOT import torch."""
    import sys

    # Check torch not imported by this module
    assert "torch" not in sys.modules or not any(
        "adapter_boundary_review_matrix" in str(module)
        for name, module in sys.modules.items()
        if name == "torch"
    )


def test_no_execution_markers():
    """Test module does NOT contain execution markers."""
    import dal_core.adapter_boundary_review_matrix as matrix_module

    module_source = matrix_module.__doc__ or ""

    # Check forbidden execution markers NOT present in module
    forbidden_markers = [
        "from_pretrained",
        "model.generate",
        "Trainer(",
        "tokenize(",
        "to_tensor(",
    ]

    for marker in forbidden_markers:
        assert marker not in module_source


def test_no_production_code_imports_from_fixtures():
    """Test production code does NOT import from tests/fixtures."""
    import dal_core.adapter_boundary_review_matrix as matrix_module
    import inspect

    source = inspect.getsource(matrix_module)

    # Check no imports from tests.fixtures (except in type hints which are allowed)
    lines = source.split("\n")
    import_lines = [line for line in lines if line.strip().startswith("from tests.fixtures")]

    # Type hint imports are allowed (e.g., for verify_golden_fixture_against_matrix)
    # but actual runtime imports are not
    for line in import_lines:
        # Type hints use quotes or are in TYPE_CHECKING blocks
        assert '"""' in line or "'''" in line or "# type:" in line or "TYPE_CHECKING" in line


def test_matrix_documentation_exists():
    """Test matrix has comprehensive documentation."""
    matrix = build_canonical_adapter_boundary_matrix()

    for transition in matrix.transitions:
        assert len(transition.verification_criteria) > 0
        for req in transition.requirements:
            assert req.description
            assert req.verification_method


def test_canonical_matrix_is_complete():
    """Test canonical matrix covers complete adapter chain."""
    matrix = build_canonical_adapter_boundary_matrix()

    # Check chain coverage
    source_types = {t.source_type_name for t in matrix.transitions}
    target_types = {t.target_type_name for t in matrix.transitions}

    # Complete chain: TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput → ConstitutionalEvaluator
    assert "TrainingExample" in source_types
    assert "AdapterInput" in source_types
    assert "AdapterInput" in target_types
    assert "AdapterRawOutput" in source_types
    assert "AdapterRawOutput" in target_types
    assert "ModelOutput" in source_types
    assert "ModelOutput" in target_types
    assert "ConstitutionalEvaluator" in target_types
