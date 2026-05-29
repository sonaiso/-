"""
Test Golden No-Op Adapter Chain Fixtures (PR #155)

Constitutional Purpose:
    Verify that golden adapter chain fixtures demonstrate deterministic
    chain behavior with preserved bindings BEFORE any real model integration.

Test Coverage:
    1. All golden fixtures are immutable
    2. Valid chain preserves source_trace_id
    3. Valid chain preserves source_training_example_id
    4. Valid chain preserves adapter input/output/model output IDs in registry
    5. Authority marker chain is detected as violation
    6. Binding loss attempt raises ValueError
    7. Wrong adapter output link raises ValueError
    8. Referenced candidate/residual/gate/rank IDs are preserved
    9. Model output from valid chain passes shape requirements for ConstitutionalEvaluator
    10. No fixture imports transformers/torch
    11. No fixture contains execution markers
    12. Fixtures remain under tests/fixtures, not src/dal_core
    13. No production export from dal_core

Constitutional Laws:
    1. Golden fixtures are TEST DATA ONLY
    2. Golden fixtures do NOT execute T5
    3. Golden fixtures do NOT tokenize
    4. Golden fixtures do NOT train
    5. Golden fixtures preserve bindings deterministically

Created: 2026-05-29
"""

import pytest
from dataclasses import fields, FrozenInstanceError

# Import golden fixtures
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../fixtures/dal_core'))

from golden_noop_adapter_chains import (
    GoldenNoOpChainFixture,
    make_valid_explanation_chain_fixture,
    make_authority_violation_chain_fixture,
    make_binding_loss_blocked_fixture,
    make_wrong_adapter_output_link_blocked_fixture,
    make_reference_preservation_chain_fixture,
    make_constitutional_evaluator_ready_fixture,
    all_golden_noop_chain_fixtures,
)

from noop_adapter_fixtures import (
    NoOpInputAdapter,
    NoOpOutputAdapter,
    NoOpValidationAdapter,
    add_adapter_input_to_chain,
    add_adapter_output_to_chain,
    create_chain_link_from_training_example,
)

from dal_core.t5_adapter_interface_contracts import AdapterViolationType


# ============================================================================
# Test: All Golden Fixtures Are Immutable
# ============================================================================

def test_all_golden_fixtures_are_immutable():
    """
    Verify all golden fixtures are frozen dataclasses (immutable).

    Constitutional Requirement:
        Golden fixtures MUST be immutable to ensure reproducibility.
    """
    all_fixtures = all_golden_noop_chain_fixtures()

    for fixture in all_fixtures:
        # Verify fixture is frozen
        assert fixture.__dataclass_fields__  # Is a dataclass

        # Attempt to modify should raise FrozenInstanceError
        with pytest.raises(FrozenInstanceError):
            fixture.fixture_id = "modified"  # type: ignore


def test_golden_fixture_has_immutable_components():
    """
    Verify golden fixture components are also immutable.

    Constitutional Requirement:
        All components (TrainingExample, AdapterInput, etc.) MUST be immutable.
    """
    fixture = make_valid_explanation_chain_fixture()

    # Verify TrainingExample is frozen
    with pytest.raises(FrozenInstanceError):
        fixture.source_training_example.training_example_id = "modified"  # type: ignore

    # Verify AdapterInput is frozen
    with pytest.raises(FrozenInstanceError):
        fixture.adapter_input.adapter_input_id = "modified"  # type: ignore

    # Verify AdapterRawOutput is frozen
    with pytest.raises(FrozenInstanceError):
        fixture.adapter_raw_output.adapter_output_id = "modified"  # type: ignore

    # Verify ModelOutput is frozen
    with pytest.raises(FrozenInstanceError):
        fixture.model_output.model_output_id = "modified"  # type: ignore

    # Verify AdapterChainRegistry is frozen
    with pytest.raises(FrozenInstanceError):
        fixture.adapter_chain_registry.registry_id = "modified"  # type: ignore


# ============================================================================
# Test: Valid Chain Preserves source_trace_id
# ============================================================================

def test_valid_chain_preserves_source_trace_id():
    """
    Verify valid explanation chain preserves source_trace_id through transformation.

    Chain: TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput

    Constitutional Requirement:
        source_trace_id MUST be preserved from TrainingExample to ModelOutput.
    """
    fixture = make_valid_explanation_chain_fixture()

    # Get source trace ID
    source_trace_id = fixture.source_training_example.source_trace_id

    # Verify preserved in AdapterInput
    assert fixture.adapter_input.source_trace_id == source_trace_id

    # Verify preserved in ModelOutput
    assert fixture.model_output.source_trace_id == source_trace_id

    # Verify preserved in chain registry
    chain_link = fixture.adapter_chain_registry.chains[0]
    assert chain_link.source_trace_id == source_trace_id


# ============================================================================
# Test: Valid Chain Preserves source_training_example_id
# ============================================================================

def test_valid_chain_preserves_source_training_example_id():
    """
    Verify valid explanation chain preserves source_training_example_id.

    Chain: TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput

    Constitutional Requirement:
        source_training_example_id MUST be preserved from TrainingExample to ModelOutput.
    """
    fixture = make_valid_explanation_chain_fixture()

    # Get source training example ID
    source_training_example_id = fixture.source_training_example.training_example_id

    # Verify preserved in AdapterInput
    assert fixture.adapter_input.source_training_example_id == source_training_example_id

    # Verify preserved in ModelOutput
    assert fixture.model_output.source_training_example_id == source_training_example_id

    # Verify preserved in chain registry
    chain_link = fixture.adapter_chain_registry.chains[0]
    assert chain_link.source_training_example_id == source_training_example_id


# ============================================================================
# Test: Valid Chain Preserves Adapter IDs in Registry
# ============================================================================

def test_valid_chain_preserves_adapter_ids_in_registry():
    """
    Verify adapter input/output/model output IDs are preserved in chain registry.

    Constitutional Requirement:
        Chain registry MUST track all transformation IDs for audit trail.
    """
    fixture = make_valid_explanation_chain_fixture()

    chain_link = fixture.adapter_chain_registry.chains[0]

    # Verify adapter_input_id preserved
    assert chain_link.adapter_input_id == fixture.adapter_input.adapter_input_id

    # Verify adapter_output_id preserved
    assert chain_link.adapter_output_id == fixture.adapter_raw_output.adapter_output_id

    # Verify model_output_id preserved
    assert chain_link.model_output_id == fixture.model_output.model_output_id

    # Verify transformation steps recorded
    assert "training_example_created" in chain_link.transformation_steps
    assert "adapter_input_prepared" in chain_link.transformation_steps
    assert "adapter_raw_output_generated" in chain_link.transformation_steps
    assert "model_output_parsed" in chain_link.transformation_steps


# ============================================================================
# Test: Authority Marker Chain Detected as Violation
# ============================================================================

def test_authority_marker_chain_detected_as_violation():
    """
    Verify authority marker in input is detected by validation adapter.

    Constitutional Requirement:
        Authority markers (final_answer, etc.) MUST be detected as violations.
    """
    fixture = make_authority_violation_chain_fixture()

    # Verify input contains authority marker
    assert "final_answer" in fixture.adapter_input.input_text.lower()

    # Validate with NoOpValidationAdapter
    validation_adapter = NoOpValidationAdapter()
    result = validation_adapter.check_constitutional_compliance(fixture.adapter_input)

    # Verify violation detected
    assert not result.is_valid
    assert AdapterViolationType.AUTHORITY_CLAIM_ATTEMPTED in result.violations

    # Verify expected violation matches fixture
    assert AdapterViolationType.AUTHORITY_CLAIM_ATTEMPTED in fixture.expected_violations


# ============================================================================
# Test: Binding Loss Attempt Raises ValueError
# ============================================================================

def test_binding_loss_attempt_raises_valueerror():
    """
    Verify binding loss is blocked by chain functions.

    Constitutional Requirement:
        Chain functions MUST detect binding loss and raise ValueError.
    """
    fixture = make_binding_loss_blocked_fixture()

    # Attempt to add adapter input with wrong binding to chain
    chain_link = create_chain_link_from_training_example(
        training_example=fixture.source_training_example,
        link_id="test_chain",
    )

    # Should raise ValueError because adapter_input has wrong source_training_example_id
    with pytest.raises(ValueError) as exc_info:
        add_adapter_input_to_chain(chain_link, fixture.adapter_input)

    assert "source_training_example_id" in str(exc_info.value)


# ============================================================================
# Test: Wrong Adapter Output Link Raises ValueError
# ============================================================================

def test_wrong_adapter_output_link_raises_valueerror():
    """
    Verify wrong adapter output link is blocked by chain functions.

    Constitutional Requirement:
        Chain functions MUST detect wrong adapter output link and raise ValueError.
    """
    fixture = make_wrong_adapter_output_link_blocked_fixture()

    # Create valid chain with adapter input
    chain_link = create_chain_link_from_training_example(
        training_example=fixture.source_training_example,
        link_id="test_chain",
    )
    chain_link = add_adapter_input_to_chain(chain_link, fixture.adapter_input)

    # Should raise ValueError because adapter_raw_output has wrong source_adapter_input_id
    with pytest.raises(ValueError) as exc_info:
        add_adapter_output_to_chain(chain_link, fixture.adapter_raw_output)

    assert "AdapterInput" in str(exc_info.value)


# ============================================================================
# Test: Referenced IDs Are Preserved
# ============================================================================

def test_referenced_candidate_ids_are_preserved():
    """
    Verify referenced candidate IDs are preserved in fixture.

    Constitutional Requirement:
        Referenced candidate IDs MUST be traceable through chain.
    """
    fixture = make_reference_preservation_chain_fixture()

    # Verify candidate IDs in TrainingExample
    assert len(fixture.source_training_example.referenced_candidate_ids) == 3
    assert "candidate_c10" in fixture.source_training_example.referenced_candidate_ids
    assert "candidate_c11" in fixture.source_training_example.referenced_candidate_ids
    assert "candidate_c12" in fixture.source_training_example.referenced_candidate_ids

    # Verify preserved in output text
    assert "candidate_c10" in fixture.model_output.predicted_text
    assert "candidate_c11" in fixture.model_output.predicted_text
    assert "candidate_c12" in fixture.model_output.predicted_text


def test_referenced_residual_ids_are_preserved():
    """
    Verify referenced residual IDs are preserved in fixture.

    Constitutional Requirement:
        Referenced residual IDs MUST be traceable through chain.
    """
    fixture = make_reference_preservation_chain_fixture()

    # Verify residual IDs in TrainingExample
    assert len(fixture.source_training_example.referenced_residual_ids) == 2
    assert "residual_r5" in fixture.source_training_example.referenced_residual_ids
    assert "residual_r6" in fixture.source_training_example.referenced_residual_ids

    # Verify preserved in output text
    assert "residual_r5" in fixture.model_output.predicted_text
    assert "residual_r6" in fixture.model_output.predicted_text


def test_referenced_gate_ids_are_preserved():
    """
    Verify referenced gate IDs are preserved in fixture.

    Constitutional Requirement:
        Referenced gate IDs MUST be traceable through chain.
    """
    fixture = make_reference_preservation_chain_fixture()

    # Verify gate IDs in TrainingExample
    assert len(fixture.source_training_example.referenced_gate_ids) == 2
    assert "gate_sukun_repair" in fixture.source_training_example.referenced_gate_ids
    assert "gate_shadda_enforcement" in fixture.source_training_example.referenced_gate_ids

    # Verify preserved in output text
    assert "gate_sukun_repair" in fixture.model_output.predicted_text
    assert "gate_shadda_enforcement" in fixture.model_output.predicted_text


def test_referenced_rank_values_are_preserved():
    """
    Verify referenced rank values are preserved in fixture.

    Constitutional Requirement:
        Referenced rank values MUST be traceable through chain.
    """
    fixture = make_reference_preservation_chain_fixture()

    # Verify rank values in TrainingExample
    assert len(fixture.source_training_example.referenced_rank_values) == 2
    assert "PLAUSIBLE" in fixture.source_training_example.referenced_rank_values
    assert "DEFENSIBLE" in fixture.source_training_example.referenced_rank_values

    # Verify preserved in output text
    assert "PLAUSIBLE" in fixture.model_output.predicted_text
    assert "DEFENSIBLE" in fixture.model_output.predicted_text


def test_referenced_ids_preserved_in_metadata():
    """
    Verify referenced IDs are preserved in adapter_raw_output metadata.

    Constitutional Requirement:
        Metadata SHOULD preserve references for audit trail.
    """
    fixture = make_reference_preservation_chain_fixture()

    # Get metadata from adapter_raw_output
    metadata_dict = dict(fixture.adapter_raw_output.adapter_metadata)

    # Verify referenced IDs in metadata
    assert "referenced_candidates" in metadata_dict
    assert "candidate_c10" in metadata_dict["referenced_candidates"]
    assert "candidate_c11" in metadata_dict["referenced_candidates"]
    assert "candidate_c12" in metadata_dict["referenced_candidates"]

    assert "referenced_residuals" in metadata_dict
    assert "residual_r5" in metadata_dict["referenced_residuals"]
    assert "residual_r6" in metadata_dict["referenced_residuals"]

    assert "referenced_gates" in metadata_dict
    assert "gate_sukun_repair" in metadata_dict["referenced_gates"]
    assert "gate_shadda_enforcement" in metadata_dict["referenced_gates"]

    assert "referenced_ranks" in metadata_dict
    assert "PLAUSIBLE" in metadata_dict["referenced_ranks"]
    assert "DEFENSIBLE" in metadata_dict["referenced_ranks"]


# ============================================================================
# Test: Model Output Passes ConstitutionalEvaluator Shape Requirements
# ============================================================================

def test_model_output_has_required_fields_for_evaluator():
    """
    Verify ModelOutput has all required fields for ConstitutionalEvaluator.

    Constitutional Requirement:
        ModelOutput MUST have:
        - model_output_id
        - source_training_example_id
        - source_trace_id
        - predicted_text
        - model_name
        - generation_timestamp
    """
    fixture = make_constitutional_evaluator_ready_fixture()

    model_output = fixture.model_output

    # Verify all required fields present
    assert model_output.model_output_id
    assert model_output.source_training_example_id
    assert model_output.source_trace_id
    assert model_output.predicted_text
    assert model_output.model_name
    assert model_output.generation_timestamp

    # Verify field types
    assert isinstance(model_output.model_output_id, str)
    assert isinstance(model_output.source_training_example_id, str)
    assert isinstance(model_output.source_trace_id, str)
    assert isinstance(model_output.predicted_text, str)
    assert isinstance(model_output.model_name, str)
    assert isinstance(model_output.generation_timestamp, str)


def test_model_output_bindings_match_training_example():
    """
    Verify ModelOutput bindings match source TrainingExample.

    Constitutional Requirement:
        ModelOutput bindings MUST match TrainingExample for evaluator to link them.
    """
    fixture = make_constitutional_evaluator_ready_fixture()

    # Verify bindings match
    assert (
        fixture.model_output.source_training_example_id ==
        fixture.source_training_example.training_example_id
    )
    assert (
        fixture.model_output.source_trace_id ==
        fixture.source_training_example.source_trace_id
    )


# ============================================================================
# Test: No Forbidden Imports
# ============================================================================

def test_no_transformers_import_in_golden_fixtures():
    """
    Verify golden fixtures do NOT import transformers.

    Constitutional Requirement:
        Golden fixtures MUST NOT import transformers (forbidden).
    """
    import golden_noop_adapter_chains

    # Read source file
    import inspect
    source = inspect.getsource(golden_noop_adapter_chains)

    # Check actual import statements (not in docstrings/comments)
    lines = source.split('\n')
    in_docstring = False
    for line in lines:
        # Track docstring state
        if '"""' in line:
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue

        # Skip comment lines
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        # Skip lines that are documenting what's forbidden (with ❌ or numbered lists)
        if '❌' in line or 'Forbidden' in line or line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
            continue

        # Check for actual imports
        if 'import transformers' in line:
            pytest.fail(f"Found 'import transformers' in executable code: {line}")
        if 'from transformers' in line:
            pytest.fail(f"Found 'from transformers' in executable code: {line}")


def test_no_torch_import_in_golden_fixtures():
    """
    Verify golden fixtures do NOT import torch.

    Constitutional Requirement:
        Golden fixtures MUST NOT import torch (forbidden).
    """
    import golden_noop_adapter_chains

    # Read source file
    import inspect
    source = inspect.getsource(golden_noop_adapter_chains)

    # Check actual import statements (not in docstrings/comments)
    lines = source.split('\n')
    in_docstring = False
    for line in lines:
        # Track docstring state
        if '"""' in line:
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue

        # Skip comment lines
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        # Skip lines that are documenting what's forbidden (with ❌ or numbered lists)
        if '❌' in line or 'Forbidden' in line or line.strip().startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
            continue

        # Check for actual imports
        if 'import torch' in line:
            pytest.fail(f"Found 'import torch' in executable code: {line}")
        if 'from torch' in line:
            pytest.fail(f"Found 'from torch' in executable code: {line}")


# ============================================================================
# Test: No Execution Markers
# ============================================================================

def test_no_tokenization_markers_in_golden_fixtures():
    """
    Verify golden fixtures do NOT contain tokenization execution markers.

    Constitutional Requirement:
        Golden fixtures MUST NOT tokenize (forbidden).
    """
    import golden_noop_adapter_chains

    # Read source file
    import inspect
    source = inspect.getsource(golden_noop_adapter_chains)

    # Verify no tokenization markers (except in comments/forbidden lists)
    # Note: .encode( and .tokenize( are forbidden execution markers
    lines = source.split('\n')
    in_docstring = False
    for line in lines:
        # Track docstring state
        if '"""' in line:
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue

        # Skip comment lines
        if line.strip().startswith('#'):
            continue
        # Skip forbidden marker lists (intentionally documenting what's forbidden)
        if '❌' in line or 'Forbidden' in line or 'forbidden' in line:
            continue

        # Check for execution markers
        if '.encode(' in line:
            pytest.fail(f"Found .encode( in executable code: {line}")
        if '.tokenize(' in line:
            pytest.fail(f"Found .tokenize( in executable code: {line}")


def test_no_model_loading_markers_in_golden_fixtures():
    """
    Verify golden fixtures do NOT contain model loading execution markers.

    Constitutional Requirement:
        Golden fixtures MUST NOT load models (forbidden).
    """
    import golden_noop_adapter_chains

    # Read source file
    import inspect
    source = inspect.getsource(golden_noop_adapter_chains)

    # Verify no model loading markers (except in comments/forbidden lists)
    lines = source.split('\n')
    in_docstring = False
    for line in lines:
        # Track docstring state
        if '"""' in line:
            in_docstring = not in_docstring
            continue
        if in_docstring:
            continue

        # Skip comment lines
        if line.strip().startswith('#'):
            continue
        # Skip forbidden marker lists
        if '❌' in line or 'Forbidden' in line or 'forbidden' in line:
            continue

        # Check for execution markers
        if '.from_pretrained(' in line:
            pytest.fail(f"Found .from_pretrained( in executable code: {line}")
        if 'model.generate(' in line:
            pytest.fail(f"Found model.generate( in executable code: {line}")
        if 'Trainer(' in line:
            pytest.fail(f"Found Trainer( in executable code: {line}")


# ============================================================================
# Test: Fixtures Under tests/fixtures, Not src/dal_core
# ============================================================================

def test_golden_fixtures_location_under_tests_fixtures():
    """
    Verify golden fixtures are in tests/fixtures/dal_core, not src/dal_core.

    Constitutional Requirement:
        Golden fixtures MUST remain in tests/fixtures (not production).
    """
    import golden_noop_adapter_chains
    import os

    # Get file path
    file_path = golden_noop_adapter_chains.__file__
    # Normalize path
    normalized = os.path.normpath(file_path)

    # Verify in tests/fixtures/dal_core
    assert 'tests' in normalized.split(os.sep)
    assert 'fixtures' in normalized.split(os.sep)
    assert 'dal_core' in normalized.split(os.sep)
    assert 'src' not in normalized.split(os.sep)


# ============================================================================
# Test: No Production Export from dal_core
# ============================================================================

def test_no_golden_fixtures_exported_from_dal_core():
    """
    Verify golden fixtures are NOT exported from src/dal_core.

    Constitutional Requirement:
        dal_core MUST NOT export test fixtures.
    """
    import dal_core

    # Verify golden fixture types NOT in dal_core
    assert not hasattr(dal_core, 'GoldenNoOpChainFixture')
    assert not hasattr(dal_core, 'make_valid_explanation_chain_fixture')
    assert not hasattr(dal_core, 'make_authority_violation_chain_fixture')
    assert not hasattr(dal_core, 'make_binding_loss_blocked_fixture')
    assert not hasattr(dal_core, 'make_wrong_adapter_output_link_blocked_fixture')
    assert not hasattr(dal_core, 'make_reference_preservation_chain_fixture')
    assert not hasattr(dal_core, 'make_constitutional_evaluator_ready_fixture')
    assert not hasattr(dal_core, 'all_golden_noop_chain_fixtures')


# ============================================================================
# Test: All 6 Golden Fixtures Exist
# ============================================================================

def test_all_six_golden_fixtures_exist():
    """
    Verify all 6 golden fixtures are created and accessible.

    Constitutional Requirement:
        All 6 required golden cases MUST be implemented.
    """
    all_fixtures = all_golden_noop_chain_fixtures()

    # Verify count
    assert len(all_fixtures) == 6

    # Verify fixture IDs
    fixture_ids = {f.fixture_id for f in all_fixtures}
    assert "golden_fixture_001_valid_explanation" in fixture_ids
    assert "golden_fixture_002_authority_violation" in fixture_ids
    assert "golden_fixture_003_binding_loss_blocked" in fixture_ids
    assert "golden_fixture_004_wrong_output_link_blocked" in fixture_ids
    assert "golden_fixture_005_reference_preservation" in fixture_ids
    assert "golden_fixture_006_evaluator_ready" in fixture_ids


def test_all_fixtures_have_unique_ids():
    """
    Verify all golden fixtures have unique fixture_ids.

    Constitutional Requirement:
        Fixture IDs MUST be unique for identification.
    """
    all_fixtures = all_golden_noop_chain_fixtures()

    fixture_ids = [f.fixture_id for f in all_fixtures]

    # Verify uniqueness
    assert len(fixture_ids) == len(set(fixture_ids))


# ============================================================================
# Test: Valid Fixtures Are Marked Valid
# ============================================================================

def test_valid_fixtures_marked_with_expected_status():
    """
    Verify valid fixtures are correctly marked as valid.

    Constitutional Requirement:
        expected_validation_status MUST be True for valid chains.
    """
    valid_fixtures = [
        make_valid_explanation_chain_fixture(),
        make_reference_preservation_chain_fixture(),
        make_constitutional_evaluator_ready_fixture(),
    ]

    for fixture in valid_fixtures:
        assert fixture.expected_validation_status is True
        assert len(fixture.expected_violations) == 0


def test_invalid_fixtures_marked_with_expected_status():
    """
    Verify invalid fixtures are correctly marked as invalid.

    Constitutional Requirement:
        expected_validation_status MUST be False for invalid chains.
    """
    # Authority violation fixture is invalid
    fixture = make_authority_violation_chain_fixture()
    assert fixture.expected_validation_status is False
    assert len(fixture.expected_violations) > 0

    # Error case fixtures (binding loss, wrong link) are invalid
    binding_loss_fixture = make_binding_loss_blocked_fixture()
    assert binding_loss_fixture.expected_validation_status is False

    wrong_link_fixture = make_wrong_adapter_output_link_blocked_fixture()
    assert wrong_link_fixture.expected_validation_status is False
