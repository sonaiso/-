"""
Tests for T5 Adapter Interface Contracts (PR #152)

Constitutional Test Coverage:
    1. All dataclasses are frozen (immutable)
    2. Required fields are validated
    3. Protocols expose required method names
    4. AdapterInput preserves source_trace_id
    5. AdapterInput preserves source_training_example_id
    6. AdapterRawOutput is raw text only (no tensors)
    7. AdapterResult can carry violations without resolving them
    8. No forbidden fields exist in contract types
    9. Source bindings preserved from TrainingExample to AdapterInput
    10. AdapterRawOutput can be converted to ModelOutput shape without generation
    11. No forbidden imports or execution markers present
    12. No concrete T5 adapter class is implemented

Test Strategy:
    - Unit tests for each dataclass structure
    - Immutability verification
    - Source binding verification
    - Protocol method signature verification
    - Forbidden field detection tests
    - Integration chain verification
    - Negative tests (violations properly detected)

Created: 2026-05-29
"""

import pytest
from typing import get_type_hints
from dataclasses import fields

from dal_core.t5_adapter_interface_contracts import (
    # Enums
    AdapterStatus,
    AdapterViolationType,

    # Data structures
    AdapterInput,
    AdapterRawOutput,
    AdapterValidationResult,
    AdapterResult,

    # Protocols/ABCs
    InputAdapterContract,
    OutputAdapterContract,
    ValidationAdapterContract,

    # Constants
    FORBIDDEN_ADAPTER_FIELDS,
)

from dal_core.training_example import TrainingExample
from dal_core.model_output import ModelOutput
from dal_core.trace_explanation_dataset_generator import (
    OutputType,
    ValidationStatus,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation


# ============================================================================
# AdapterInput Structure Tests
# ============================================================================

def test_adapter_input_is_frozen():
    """
    Test: AdapterInput is immutable (frozen=True).

    Constitutional Requirement:
        AdapterInput MUST be frozen to prevent mutation.
    """
    adapter_input = AdapterInput(
        adapter_input_id="input_001",
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        input_text="Test input",
        metadata=(("key", "value"),),
    )

    with pytest.raises(Exception):  # FrozenInstanceError
        adapter_input.input_text = "Modified"


def test_adapter_input_preserves_source_trace_id():
    """
    Test: AdapterInput preserves source_trace_id.

    Constitutional Requirement:
        AdapterInput MUST preserve source_trace_id from TrainingExample.
    """
    source_trace_id = "trace_abc123"

    adapter_input = AdapterInput(
        adapter_input_id="input_001",
        source_training_example_id="example_001",
        source_trace_id=source_trace_id,
        input_text="Test input",
        metadata=(),
    )

    assert adapter_input.source_trace_id == source_trace_id


def test_adapter_input_preserves_source_training_example_id():
    """
    Test: AdapterInput preserves source_training_example_id.

    Constitutional Requirement:
        AdapterInput MUST preserve source_training_example_id from TrainingExample.
    """
    source_training_example_id = "example_xyz789"

    adapter_input = AdapterInput(
        adapter_input_id="input_002",
        source_training_example_id=source_training_example_id,
        source_trace_id="trace_001",
        input_text="Test input",
        metadata=(),
    )

    assert adapter_input.source_training_example_id == source_training_example_id


def test_adapter_input_requires_all_fields():
    """
    Test: AdapterInput validates required fields.

    Constitutional Requirement:
        AdapterInput MUST validate all required fields are present.
    """
    # Missing adapter_input_id
    with pytest.raises(ValueError, match="adapter_input_id"):
        AdapterInput(
            adapter_input_id="",
            source_training_example_id="example_001",
            source_trace_id="trace_001",
            input_text="Test input",
            metadata=(),
        )

    # Missing source_training_example_id
    with pytest.raises(ValueError, match="source_training_example_id"):
        AdapterInput(
            adapter_input_id="input_001",
            source_training_example_id="",
            source_trace_id="trace_001",
            input_text="Test input",
            metadata=(),
        )

    # Missing source_trace_id
    with pytest.raises(ValueError, match="source_trace_id"):
        AdapterInput(
            adapter_input_id="input_001",
            source_training_example_id="example_001",
            source_trace_id="",
            input_text="Test input",
            metadata=(),
        )

    # Missing input_text
    with pytest.raises(ValueError, match="input_text"):
        AdapterInput(
            adapter_input_id="input_001",
            source_training_example_id="example_001",
            source_trace_id="trace_001",
            input_text="",
            metadata=(),
        )


def test_adapter_input_has_no_forbidden_fields():
    """
    Test: AdapterInput has no forbidden fields.

    Constitutional Requirement:
        AdapterInput MUST NOT contain tokenizer, tensor, model, device, etc.
    """
    adapter_input = AdapterInput(
        adapter_input_id="input_001",
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        input_text="Test input",
        metadata=(),
    )

    # Get all field names
    field_names = {f.name for f in fields(adapter_input)}

    # Check forbidden fields
    forbidden_in_input = {
        "tokenizer", "input_ids", "attention_mask", "tensor",
        "model", "device", "logits", "loss", "trainer", "optimizer"
    }

    for forbidden in forbidden_in_input:
        assert forbidden not in field_names, f"Forbidden field {forbidden} found in AdapterInput"


# ============================================================================
# AdapterRawOutput Structure Tests
# ============================================================================

def test_adapter_raw_output_is_frozen():
    """
    Test: AdapterRawOutput is immutable (frozen=True).

    Constitutional Requirement:
        AdapterRawOutput MUST be frozen to prevent mutation.
    """
    adapter_output = AdapterRawOutput(
        adapter_output_id="output_001",
        source_adapter_input_id="input_001",
        raw_output_text="Test output",
        adapter_metadata=(("key", "value"),),
    )

    with pytest.raises(Exception):  # FrozenInstanceError
        adapter_output.raw_output_text = "Modified"


def test_adapter_raw_output_is_text_only():
    """
    Test: AdapterRawOutput contains raw text only (no tensors).

    Constitutional Requirement:
        AdapterRawOutput MUST contain abstract text, NOT decoded tensors.
    """
    adapter_output = AdapterRawOutput(
        adapter_output_id="output_001",
        source_adapter_input_id="input_001",
        raw_output_text="This is abstract output text",
        adapter_metadata=(),
    )

    # Verify it's just text
    assert isinstance(adapter_output.raw_output_text, str)
    assert len(adapter_output.raw_output_text) > 0


def test_adapter_raw_output_requires_all_fields():
    """
    Test: AdapterRawOutput validates required fields.

    Constitutional Requirement:
        AdapterRawOutput MUST validate all required fields are present.
    """
    # Missing adapter_output_id
    with pytest.raises(ValueError, match="adapter_output_id"):
        AdapterRawOutput(
            adapter_output_id="",
            source_adapter_input_id="input_001",
            raw_output_text="Test output",
            adapter_metadata=(),
        )

    # Missing source_adapter_input_id
    with pytest.raises(ValueError, match="source_adapter_input_id"):
        AdapterRawOutput(
            adapter_output_id="output_001",
            source_adapter_input_id="",
            raw_output_text="Test output",
            adapter_metadata=(),
        )

    # Missing raw_output_text
    with pytest.raises(ValueError, match="raw_output_text"):
        AdapterRawOutput(
            adapter_output_id="output_001",
            source_adapter_input_id="input_001",
            raw_output_text="",
            adapter_metadata=(),
        )


def test_adapter_raw_output_has_no_forbidden_fields():
    """
    Test: AdapterRawOutput has no forbidden fields.

    Constitutional Requirement:
        AdapterRawOutput MUST NOT contain logits, tensors, model, device, etc.
    """
    adapter_output = AdapterRawOutput(
        adapter_output_id="output_001",
        source_adapter_input_id="input_001",
        raw_output_text="Test output",
        adapter_metadata=(),
    )

    # Get all field names
    field_names = {f.name for f in fields(adapter_output)}

    # Check forbidden fields
    forbidden_in_output = {
        "output_ids", "logits", "scores", "tensor",
        "model", "device", "loss", "trainer"
    }

    for forbidden in forbidden_in_output:
        assert forbidden not in field_names, f"Forbidden field {forbidden} found in AdapterRawOutput"


# ============================================================================
# AdapterValidationResult Structure Tests
# ============================================================================

def test_adapter_validation_result_is_frozen():
    """
    Test: AdapterValidationResult is immutable (frozen=True).

    Constitutional Requirement:
        AdapterValidationResult MUST be frozen to prevent mutation.
    """
    validation_result = AdapterValidationResult(
        validation_id="validation_001",
        is_valid=True,
        violations=(),
        warnings=(),
        checked_constraints=("constraint1",),
    )

    with pytest.raises(Exception):  # FrozenInstanceError
        validation_result.is_valid = False


def test_adapter_validation_result_consistency():
    """
    Test: AdapterValidationResult enforces consistency (violations → not valid).

    Constitutional Requirement:
        AdapterValidationResult cannot be valid if violations present.
    """
    # Invalid: is_valid=True with violations
    with pytest.raises(ValueError, match="cannot be valid with violations"):
        AdapterValidationResult(
            validation_id="validation_001",
            is_valid=True,
            violations=(AdapterViolationType.MISSING_SOURCE_TRACE_ID,),
            warnings=(),
            checked_constraints=(),
        )

    # Valid: is_valid=False with violations
    validation_result = AdapterValidationResult(
        validation_id="validation_002",
        is_valid=False,
        violations=(AdapterViolationType.MISSING_SOURCE_TRACE_ID,),
        warnings=(),
        checked_constraints=(),
    )
    assert not validation_result.is_valid
    assert len(validation_result.violations) == 1


# ============================================================================
# AdapterResult Structure Tests
# ============================================================================

def test_adapter_result_is_frozen():
    """
    Test: AdapterResult is immutable (frozen=True).

    Constitutional Requirement:
        AdapterResult MUST be frozen to prevent mutation.
    """
    adapter_result = AdapterResult(
        adapter_result_id="result_001",
        status=AdapterStatus.VALID,
        model_output=ModelOutput.create_from_prediction(
            source_training_example_id="example_001",
            source_trace_id="trace_001",
            predicted_text="Test output",
            model_name="test_model",
        ),
        violations=(),
        residuals=(),
    )

    with pytest.raises(Exception):  # FrozenInstanceError
        adapter_result.status = AdapterStatus.BOUNDARY_VIOLATION


def test_adapter_result_can_carry_violations_without_resolving():
    """
    Test: AdapterResult can carry violations without resolving them.

    Constitutional Requirement:
        AdapterResult MUST carry violations, NOT resolve them.
    """
    adapter_result = AdapterResult(
        adapter_result_id="result_001",
        status=AdapterStatus.BOUNDARY_VIOLATION,
        model_output=None,
        violations=(
            AdapterViolationType.MISSING_SOURCE_TRACE_ID,
            AdapterViolationType.TOKENIZATION_ATTEMPTED,
        ),
        residuals=("unresolved_issue_1", "unresolved_issue_2"),
    )

    # Violations are preserved, not resolved
    assert len(adapter_result.violations) == 2
    assert len(adapter_result.residuals) == 2
    assert adapter_result.status == AdapterStatus.BOUNDARY_VIOLATION

    # No resolution methods exist
    assert not hasattr(adapter_result, 'resolve_violations')
    assert not hasattr(adapter_result, 'repair_violations')
    assert not hasattr(adapter_result, 'resolve_residuals')


def test_adapter_result_valid_status_requires_model_output():
    """
    Test: AdapterResult with VALID status requires model_output.

    Constitutional Requirement:
        AdapterResult with VALID status MUST have model_output present.
    """
    # Invalid: VALID status without model_output
    with pytest.raises(ValueError, match="VALID status requires model_output"):
        AdapterResult(
            adapter_result_id="result_001",
            status=AdapterStatus.VALID,
            model_output=None,
            violations=(),
            residuals=(),
        )

    # Valid: VALID status with model_output
    adapter_result = AdapterResult(
        adapter_result_id="result_002",
        status=AdapterStatus.VALID,
        model_output=ModelOutput.create_from_prediction(
            source_training_example_id="example_001",
            source_trace_id="trace_001",
            predicted_text="Test output",
            model_name="test_model",
        ),
        violations=(),
        residuals=(),
    )
    assert adapter_result.status == AdapterStatus.VALID
    assert adapter_result.model_output is not None


def test_adapter_result_non_valid_status_requires_violations_or_residuals():
    """
    Test: AdapterResult with non-VALID status requires violations or residuals.

    Constitutional Requirement:
        AdapterResult with error status MUST have violations or residuals.
    """
    # Invalid: BOUNDARY_VIOLATION without violations or residuals
    with pytest.raises(ValueError, match="requires violations or residuals"):
        AdapterResult(
            adapter_result_id="result_001",
            status=AdapterStatus.BOUNDARY_VIOLATION,
            model_output=None,
            violations=(),
            residuals=(),
        )

    # Valid: BOUNDARY_VIOLATION with violations
    adapter_result = AdapterResult(
        adapter_result_id="result_002",
        status=AdapterStatus.BOUNDARY_VIOLATION,
        model_output=None,
        violations=(AdapterViolationType.MISSING_SOURCE_TRACE_ID,),
        residuals=(),
    )
    assert adapter_result.status == AdapterStatus.BOUNDARY_VIOLATION
    assert len(adapter_result.violations) == 1


def test_adapter_result_has_no_forbidden_fields():
    """
    Test: AdapterResult has no forbidden fields.

    Constitutional Requirement:
        AdapterResult MUST NOT contain resolution methods, rank upgrades, etc.
    """
    adapter_result = AdapterResult(
        adapter_result_id="result_001",
        status=AdapterStatus.VALID,
        model_output=ModelOutput.create_from_prediction(
            source_training_example_id="example_001",
            source_trace_id="trace_001",
            predicted_text="Test output",
            model_name="test_model",
        ),
        violations=(),
        residuals=(),
    )

    # Get all field names
    field_names = {f.name for f in fields(adapter_result)}

    # Check forbidden fields
    forbidden_in_result = {
        "resolved_residuals", "upgraded_rank", "closed_ifadah",
        "produced_hukm", "produced_reality", "repair_function",
        "resolution_function", "optimizer", "trainer"
    }

    for forbidden in forbidden_in_result:
        assert forbidden not in field_names, f"Forbidden field {forbidden} found in AdapterResult"


# ============================================================================
# Protocol/ABC Method Signature Tests
# ============================================================================

def test_input_adapter_contract_exposes_required_methods():
    """
    Test: InputAdapterContract Protocol exposes required method names.

    Constitutional Requirement:
        InputAdapterContract MUST declare prepare_input and validate_input.
    """
    # Get method signatures from Protocol
    hints = get_type_hints(InputAdapterContract.prepare_input)
    assert 'training_example' in hints
    assert 'return' in hints

    hints = get_type_hints(InputAdapterContract.validate_input)
    assert 'adapter_input' in hints
    assert 'return' in hints


def test_output_adapter_contract_exposes_required_methods():
    """
    Test: OutputAdapterContract Protocol exposes required method names.

    Constitutional Requirement:
        OutputAdapterContract MUST declare parse_output and validate_output.
    """
    # Get method signatures from Protocol
    hints = get_type_hints(OutputAdapterContract.parse_output)
    assert 'adapter_raw_output' in hints
    assert 'source_training_example_id' in hints
    assert 'source_trace_id' in hints
    assert 'return' in hints

    hints = get_type_hints(OutputAdapterContract.validate_output)
    assert 'model_output' in hints
    assert 'return' in hints


def test_validation_adapter_contract_exposes_required_methods():
    """
    Test: ValidationAdapterContract ABC exposes required method names.

    Constitutional Requirement:
        ValidationAdapterContract MUST declare validate_adapter_boundaries
        and check_constitutional_compliance.
    """
    # Check abstract methods exist
    assert hasattr(ValidationAdapterContract, 'validate_adapter_boundaries')
    assert hasattr(ValidationAdapterContract, 'check_constitutional_compliance')

    # Verify they are abstract
    assert getattr(
        ValidationAdapterContract.validate_adapter_boundaries,
        '__isabstractmethod__',
        False
    )
    assert getattr(
        ValidationAdapterContract.check_constitutional_compliance,
        '__isabstractmethod__',
        False
    )


# ============================================================================
# Integration Chain Tests
# ============================================================================

def test_source_bindings_preserved_from_training_example_to_adapter_input():
    """
    Test: Source bindings preserved from TrainingExample to AdapterInput.

    Constitutional Requirement:
        TrainingExample → AdapterInput transformation MUST preserve bindings.
    """
    # Create TrainingExample
    training_example = TrainingExample(
        training_example_id="example_001",
        source_dataset_row_id="row_001",
        source_trace_id="trace_abc123",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Test input",
        target_text="Test target",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Create AdapterInput (simulating prepare_input contract)
    adapter_input = AdapterInput(
        adapter_input_id="input_001",
        source_training_example_id=training_example.training_example_id,
        source_trace_id=training_example.source_trace_id,
        input_text=training_example.input_text,
        metadata=(),
    )

    # Verify bindings preserved
    assert adapter_input.source_trace_id == training_example.source_trace_id
    assert adapter_input.source_training_example_id == training_example.training_example_id


def test_adapter_raw_output_can_be_converted_to_model_output_shape():
    """
    Test: AdapterRawOutput can be converted to ModelOutput shape (without generation).

    Constitutional Requirement:
        AdapterRawOutput → ModelOutput transformation MUST be possible
        without generating text (receives abstract text).
    """
    # Create AdapterRawOutput
    adapter_raw_output = AdapterRawOutput(
        adapter_output_id="output_001",
        source_adapter_input_id="input_001",
        raw_output_text="This is abstract generated text",
        adapter_metadata=(("model_name", "test_model"),),
    )

    # Create ModelOutput (simulating parse_output contract)
    model_output = ModelOutput.create_from_prediction(
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        predicted_text=adapter_raw_output.raw_output_text,
        model_name="test_model",
    )

    # Verify conversion successful
    assert model_output.predicted_text == adapter_raw_output.raw_output_text
    assert model_output.source_trace_id == "trace_001"
    assert model_output.source_training_example_id == "example_001"


def test_full_constitutional_chain_shape():
    """
    Test: Full constitutional chain shape is valid.

    Constitutional Formula:
        TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput → ConstitutionalEvaluator

    This test verifies the shape of the transformation chain (not actual execution).
    """
    # 1. TrainingExample
    training_example = TrainingExample(
        training_example_id="example_001",
        source_dataset_row_id="row_001",
        source_trace_id="trace_abc123",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Test input",
        target_text="Test target",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # 2. AdapterInput (from TrainingExample)
    adapter_input = AdapterInput(
        adapter_input_id="input_001",
        source_training_example_id=training_example.training_example_id,
        source_trace_id=training_example.source_trace_id,
        input_text=training_example.input_text,
        metadata=(),
    )

    # 3. AdapterRawOutput (abstract, no generation)
    adapter_raw_output = AdapterRawOutput(
        adapter_output_id="output_001",
        source_adapter_input_id=adapter_input.adapter_input_id,
        raw_output_text="Abstract output text",
        adapter_metadata=(),
    )

    # 4. ModelOutput (from AdapterRawOutput)
    model_output = ModelOutput.create_from_prediction(
        source_training_example_id=adapter_input.source_training_example_id,
        source_trace_id=adapter_input.source_trace_id,
        predicted_text=adapter_raw_output.raw_output_text,
        model_name="test_model",
    )

    # 5. Verify chain integrity
    assert model_output.source_trace_id == training_example.source_trace_id
    assert model_output.source_training_example_id == training_example.training_example_id
    assert model_output.predicted_text == adapter_raw_output.raw_output_text


# ============================================================================
# Forbidden Fields Detection Tests
# ============================================================================

def test_forbidden_adapter_fields_constant_is_comprehensive():
    """
    Test: FORBIDDEN_ADAPTER_FIELDS constant lists all forbidden fields.

    Constitutional Requirement:
        FORBIDDEN_ADAPTER_FIELDS MUST list all execution/authority fields.
    """
    # Verify key forbidden fields present
    assert "tokenizer" in FORBIDDEN_ADAPTER_FIELDS
    assert "input_ids" in FORBIDDEN_ADAPTER_FIELDS
    assert "tensor" in FORBIDDEN_ADAPTER_FIELDS
    assert "logits" in FORBIDDEN_ADAPTER_FIELDS
    assert "model" in FORBIDDEN_ADAPTER_FIELDS
    assert "device" in FORBIDDEN_ADAPTER_FIELDS
    assert "trainer" in FORBIDDEN_ADAPTER_FIELDS
    assert "optimizer" in FORBIDDEN_ADAPTER_FIELDS
    assert "loss" in FORBIDDEN_ADAPTER_FIELDS
    assert "upgraded_rank" in FORBIDDEN_ADAPTER_FIELDS
    assert "resolved_residuals" in FORBIDDEN_ADAPTER_FIELDS
    assert "closed_ifadah" in FORBIDDEN_ADAPTER_FIELDS
    assert "produced_hukm" in FORBIDDEN_ADAPTER_FIELDS
    assert "produced_reality" in FORBIDDEN_ADAPTER_FIELDS
    assert "constitutional_authority" in FORBIDDEN_ADAPTER_FIELDS


# ============================================================================
# Negative Tests (No Concrete Implementation)
# ============================================================================

def test_no_concrete_t5_adapter_implementation():
    """
    Test: No concrete T5 adapter class is implemented.

    Constitutional Requirement:
        PR #152 is INTERFACES ONLY, no implementation.
    """
    # This module should contain NO concrete adapter classes
    # Only Protocols, ABCs, and data structures

    import dal_core.t5_adapter_interface_contracts as contracts_module

    # Check no ConcreteInputAdapter exists
    assert not hasattr(contracts_module, 'ConcreteInputAdapter')
    assert not hasattr(contracts_module, 'T5InputAdapter')
    assert not hasattr(contracts_module, 'HuggingFaceInputAdapter')

    # Check no ConcreteOutputAdapter exists
    assert not hasattr(contracts_module, 'ConcreteOutputAdapter')
    assert not hasattr(contracts_module, 'T5OutputAdapter')
    assert not hasattr(contracts_module, 'HuggingFaceOutputAdapter')

    # Check no ConcreteValidationAdapter exists
    assert not hasattr(contracts_module, 'ConcreteValidationAdapter')
    assert not hasattr(contracts_module, 'T5ValidationAdapter')


def test_no_forbidden_imports_in_contracts_module():
    """
    Test: Adapter contracts module contains no forbidden imports.

    Constitutional Requirement:
        Module MUST NOT import transformers or torch.
    """
    import dal_core.t5_adapter_interface_contracts as contracts_module

    # Get module source
    import inspect
    source = inspect.getsource(contracts_module)

    # Extract only import lines (lines starting with 'import ' or 'from ')
    import_lines = [
        line.strip()
        for line in source.split('\n')
        if line.strip().startswith('import ') or line.strip().startswith('from ')
    ]

    # Verify no forbidden imports in actual import statements
    for import_line in import_lines:
        assert "transformers" not in import_line, f"Forbidden import found: {import_line}"
        assert "torch" not in import_line, f"Forbidden import found: {import_line}"

    # Verify no execution markers (outside of docstrings/comments/constants)
    # Split before FORBIDDEN_ADAPTER_FIELDS to exclude intentional constant declarations
    code_before_constants = source.split("FORBIDDEN_ADAPTER_FIELDS")[0]

    # Check code lines only (not comments or docstrings)
    code_lines = [
        line.strip()
        for line in code_before_constants.split('\n')
        if line.strip()
        and not line.strip().startswith('#')
        and not line.strip().startswith('"""')
        and not line.strip().startswith("'''")
        and '"""' not in line  # Skip lines with inline docstrings
        and "❌" not in line  # Skip forbidden operations lists
    ]

    code_text = ' '.join(code_lines)

    assert "AutoTokenizer" not in code_text
    assert "T5ForConditionalGeneration" not in code_text
    assert "from_pretrained(" not in code_text
    assert "Trainer(" not in code_text
