"""
Tests for No-Op Adapter Contract Fixtures (PR #153)

Constitutional Test Coverage:
    1. NoOpInputAdapter implements InputAdapterContract Protocol
    2. NoOpOutputAdapter implements OutputAdapterContract Protocol
    3. NoOpValidationAdapter implements ValidationAdapterContract ABC
    4. No-op adapters preserve source bindings
    5. No-op adapters do NOT tokenize
    6. No-op adapters do NOT create tensors
    7. No-op adapters do NOT load models
    8. No-op adapters do NOT execute inference
    9. No-op adapters are identity-like transformations
    10. Full chain works: TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput
    11. No forbidden imports in fixture module
    12. No execution markers in fixture module

Test Strategy:
    - Unit tests for each no-op adapter
    - Protocol/ABC compliance verification
    - Source binding preservation tests
    - Full chain integration tests
    - Negative tests (no execution, no forbidden operations)
    - Module import safety tests

Created: 2026-05-29
"""

import pytest
from typing import get_type_hints
import inspect

from tests.fixtures.dal_core.noop_adapter_fixtures import (
    # No-op adapters
    NoOpInputAdapter,
    NoOpOutputAdapter,
    NoOpValidationAdapter,

    # Factory functions
    create_noop_input_adapter,
    create_noop_output_adapter,
    create_noop_validation_adapter,
    create_sample_adapter_raw_output,

    # Adapter chain registry
    AdapterChainLink,
    AdapterChainRegistry,
    create_adapter_chain_registry,
    create_chain_link_from_training_example,
    add_adapter_input_to_chain,
    add_adapter_output_to_chain,
    add_model_output_to_chain,
)

from dal_core.t5_adapter_interface_contracts import (
    # Protocols/ABCs
    InputAdapterContract,
    OutputAdapterContract,
    ValidationAdapterContract,

    # Data structures
    AdapterInput,
    AdapterRawOutput,
    AdapterValidationResult,
    AdapterStatus,
    AdapterViolationType,
)

from dal_core.training_example import TrainingExample
from dal_core.model_output import ModelOutput
from dal_core.governed_t5_integration_skeleton import (
    GovernedT5IntegrationConfig,
    ModelDependencyDeclaration,
    ModelFamily,
    AdapterBoundaryPlan,
    AdapterBoundaryType,
)
from dal_core.trace_explanation_dataset_generator import (
    OutputType,
    ValidationStatus,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation


# ============================================================================
# NoOpInputAdapter Tests
# ============================================================================

def test_noop_input_adapter_implements_input_adapter_contract():
    """
    Test: NoOpInputAdapter implements InputAdapterContract Protocol.

    Constitutional Requirement:
        NoOpInputAdapter MUST implement prepare_input and validate_input methods.
    """
    adapter = NoOpInputAdapter()

    # Check methods exist
    assert hasattr(adapter, 'prepare_input')
    assert hasattr(adapter, 'validate_input')
    assert callable(adapter.prepare_input)
    assert callable(adapter.validate_input)

    # Check method signatures match Protocol
    prepare_hints = get_type_hints(adapter.prepare_input)
    assert 'training_example' in prepare_hints
    assert 'return' in prepare_hints

    validate_hints = get_type_hints(adapter.validate_input)
    assert 'adapter_input' in validate_hints
    assert 'return' in validate_hints


def test_noop_input_adapter_preserves_source_bindings():
    """
    Test: NoOpInputAdapter preserves source bindings.

    Constitutional Requirement:
        NoOpInputAdapter MUST preserve source_trace_id and source_training_example_id.
    """
    adapter = NoOpInputAdapter()

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

    # Prepare input
    adapter_input = adapter.prepare_input(training_example)

    # Verify bindings preserved
    assert adapter_input.source_trace_id == training_example.source_trace_id
    assert adapter_input.source_training_example_id == training_example.training_example_id


def test_noop_input_adapter_does_not_tokenize():
    """
    Test: NoOpInputAdapter does NOT tokenize (only formats text).

    Constitutional Requirement:
        NoOpInputAdapter MUST NOT tokenize, only format abstract text.
    """
    adapter = NoOpInputAdapter()

    # Create TrainingExample
    training_example = TrainingExample(
        training_example_id="example_002",
        source_dataset_row_id="row_002",
        source_trace_id="trace_xyz789",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Test input text",
        target_text="Test target",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Prepare input
    adapter_input = adapter.prepare_input(training_example)

    # Verify output is still text (not tokens)
    assert isinstance(adapter_input.input_text, str)
    assert len(adapter_input.input_text) > 0

    # Verify no tokenization occurred (text is formatted, not tokenized)
    assert "[INPUT]" in adapter_input.input_text  # Formatting marker
    assert "Test input text" in adapter_input.input_text  # Original text preserved


def test_noop_input_adapter_is_immutable():
    """
    Test: NoOpInputAdapter is immutable (frozen dataclass).

    Constitutional Requirement:
        NoOpInputAdapter MUST be immutable to prevent state mutations.
    """
    adapter = NoOpInputAdapter()

    # Verify it's a frozen dataclass
    assert hasattr(adapter, '__dataclass_fields__')

    # Verify cannot modify attributes
    with pytest.raises(AttributeError):
        adapter.adapter_name = "ModifiedName"  # type: ignore

    with pytest.raises(AttributeError):
        adapter.version = "modified_version"  # type: ignore


def test_noop_input_adapter_factory():
    """
    Test: create_noop_input_adapter factory works correctly.

    Constitutional Requirement:
        Factory MUST create valid NoOpInputAdapter instance.
    """
    adapter = create_noop_input_adapter()

    assert isinstance(adapter, NoOpInputAdapter)
    assert adapter.adapter_name == "NoOpInputAdapter"
    assert hasattr(adapter, 'prepare_input')
    assert hasattr(adapter, 'validate_input')


# ============================================================================
# NoOpOutputAdapter Tests
# ============================================================================

def test_noop_output_adapter_implements_output_adapter_contract():
    """
    Test: NoOpOutputAdapter implements OutputAdapterContract Protocol.

    Constitutional Requirement:
        NoOpOutputAdapter MUST implement parse_output and validate_output methods.
    """
    adapter = NoOpOutputAdapter()

    # Check methods exist
    assert hasattr(adapter, 'parse_output')
    assert hasattr(adapter, 'validate_output')
    assert callable(adapter.parse_output)
    assert callable(adapter.validate_output)

    # Check method signatures match Protocol
    parse_hints = get_type_hints(adapter.parse_output)
    assert 'adapter_raw_output' in parse_hints
    assert 'source_training_example_id' in parse_hints
    assert 'source_trace_id' in parse_hints
    assert 'return' in parse_hints

    validate_hints = get_type_hints(adapter.validate_output)
    assert 'model_output' in validate_hints
    assert 'return' in validate_hints


def test_noop_output_adapter_preserves_source_bindings():
    """
    Test: NoOpOutputAdapter preserves source bindings.

    Constitutional Requirement:
        NoOpOutputAdapter MUST preserve source_trace_id and source_training_example_id.
    """
    adapter = NoOpOutputAdapter()

    # Create AdapterRawOutput
    adapter_raw_output = create_sample_adapter_raw_output(
        adapter_output_id="output_001",
        source_adapter_input_id="input_001",
        raw_text="Test output",
    )

    source_trace_id = "trace_abc123"
    source_training_example_id = "example_001"

    # Parse output
    model_output = adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=source_training_example_id,
        source_trace_id=source_trace_id,
    )

    # Verify bindings preserved
    assert model_output.source_trace_id == source_trace_id
    assert model_output.source_training_example_id == source_training_example_id


def test_noop_output_adapter_does_not_generate():
    """
    Test: NoOpOutputAdapter does NOT generate text (receives abstract text).

    Constitutional Requirement:
        NoOpOutputAdapter MUST NOT generate, only parse abstract text.
    """
    adapter = NoOpOutputAdapter()

    # Create AdapterRawOutput with pre-existing text
    adapter_raw_output = create_sample_adapter_raw_output(
        raw_text="Pre-existing output text",
    )

    # Parse output
    model_output = adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id="example_001",
        source_trace_id="trace_001",
    )

    # Verify text is parsed (not generated)
    assert isinstance(model_output.predicted_text, str)
    assert "Pre-existing output text" in model_output.predicted_text


def test_noop_output_adapter_is_immutable():
    """
    Test: NoOpOutputAdapter is immutable (frozen dataclass).

    Constitutional Requirement:
        NoOpOutputAdapter MUST be immutable to prevent state mutations.
    """
    adapter = NoOpOutputAdapter()

    # Verify it's a frozen dataclass
    assert hasattr(adapter, '__dataclass_fields__')

    # Verify cannot modify attributes
    with pytest.raises(AttributeError):
        adapter.adapter_name = "ModifiedName"  # type: ignore

    with pytest.raises(AttributeError):
        adapter.version = "modified_version"  # type: ignore


def test_noop_output_adapter_validate_output_detects_missing_bindings():
    """
    Test: NoOpOutputAdapter.validate_output detects missing source bindings.

    Constitutional Requirement:
        validate_output MUST detect missing source_trace_id and source_training_example_id.
    """
    adapter = NoOpOutputAdapter()

    # Create ModelOutput with empty source_trace_id (if allowed by ModelOutput)
    # Note: ModelOutput may enforce bindings at construction
    model_output = ModelOutput.create_from_prediction(
        source_training_example_id="example_001",
        source_trace_id="",  # Empty
        predicted_text="Test output",
        model_name="test_model",
    )

    # Validate output
    validation_result = adapter.validate_output(model_output)

    # Verify validation detects missing binding
    if not model_output.source_trace_id:
        assert not validation_result.is_valid
        assert AdapterViolationType.MISSING_SOURCE_TRACE_ID in validation_result.violations


def test_noop_output_adapter_factory():
    """
    Test: create_noop_output_adapter factory works correctly.

    Constitutional Requirement:
        Factory MUST create valid NoOpOutputAdapter instance.
    """
    adapter = create_noop_output_adapter()

    assert isinstance(adapter, NoOpOutputAdapter)
    assert adapter.adapter_name == "NoOpOutputAdapter"
    assert hasattr(adapter, 'parse_output')
    assert hasattr(adapter, 'validate_output')


# ============================================================================
# NoOpValidationAdapter Tests
# ============================================================================

def test_noop_validation_adapter_implements_validation_adapter_contract():
    """
    Test: NoOpValidationAdapter implements ValidationAdapterContract ABC.

    Constitutional Requirement:
        NoOpValidationAdapter MUST implement abstract methods from ABC.
    """
    adapter = NoOpValidationAdapter()

    # Check methods exist
    assert hasattr(adapter, 'validate_adapter_boundaries')
    assert hasattr(adapter, 'check_constitutional_compliance')
    assert callable(adapter.validate_adapter_boundaries)
    assert callable(adapter.check_constitutional_compliance)

    # Verify it's a subclass of ABC
    assert isinstance(adapter, ValidationAdapterContract)


def test_noop_validation_adapter_is_immutable():
    """
    Test: NoOpValidationAdapter is immutable (frozen dataclass).

    Constitutional Requirement:
        NoOpValidationAdapter MUST be immutable to prevent state mutations.
    """
    adapter = NoOpValidationAdapter()

    # Verify it's a frozen dataclass
    assert hasattr(adapter, '__dataclass_fields__')

    # Verify cannot modify attributes
    with pytest.raises(AttributeError):
        adapter.adapter_name = "ModifiedName"  # type: ignore

    with pytest.raises(AttributeError):
        adapter.version = "modified_version"  # type: ignore


def test_noop_validation_adapter_validate_boundaries():
    """
    Test: NoOpValidationAdapter.validate_adapter_boundaries works.

    Constitutional Requirement:
        validate_adapter_boundaries MUST check config structure.
    """
    adapter = NoOpValidationAdapter()

    # Create GovernedT5IntegrationConfig
    config = GovernedT5IntegrationConfig(
        integration_id="test_integration_001",
        training_run_plan_id="plan_001",
        dependency_declaration=ModelDependencyDeclaration(
            dependency_id="test_dependency_001",
            model_family=ModelFamily.T5_SMALL,
            required_transformers_version="4.30.0",
            required_torch_version=None,
            checkpoint_path=None,
            additional_requirements=(),
        ),
        input_adapter_boundary=AdapterBoundaryPlan(
            boundary_id="test_input_boundary_001",
            boundary_type=AdapterBoundaryType.INPUT_ADAPTER,
            input_contract_description="Test input contract",
            output_contract_description="Test output contract",
            constitutional_constraints=("preserve_source_bindings",),
            preserves_source_bindings=True,
            prevents_authority_claims=True,
            prevents_rank_upgrade=True,
        ),
        output_adapter_boundary=AdapterBoundaryPlan(
            boundary_id="test_output_boundary_001",
            boundary_type=AdapterBoundaryType.OUTPUT_ADAPTER,
            input_contract_description="Test output input contract",
            output_contract_description="Test output contract",
            constitutional_constraints=("preserve_source_bindings",),
            preserves_source_bindings=True,
            prevents_authority_claims=True,
            prevents_rank_upgrade=True,
        ),
        validation_adapter_boundary=AdapterBoundaryPlan(
            boundary_id="test_validation_boundary_001",
            boundary_type=AdapterBoundaryType.VALIDATION_ADAPTER,
            input_contract_description="Test validation contract",
            output_contract_description="Test validation output",
            constitutional_constraints=("prevent_authority_claims",),
            preserves_source_bindings=True,
            prevents_authority_claims=True,
            prevents_rank_upgrade=True,
        ),
        constitutional_constraints=("no_execution", "no_authority_claims"),
    )

    # Validate boundaries
    validation_result = adapter.validate_adapter_boundaries(config)

    # Verify validation executes without error
    assert isinstance(validation_result, AdapterValidationResult)
    assert validation_result.validation_id is not None
    assert len(validation_result.checked_constraints) > 0


def test_noop_validation_adapter_check_constitutional_compliance():
    """
    Test: NoOpValidationAdapter.check_constitutional_compliance works.

    Constitutional Requirement:
        check_constitutional_compliance MUST check AdapterInput structure.
    """
    adapter = NoOpValidationAdapter()

    # Create valid AdapterInput
    adapter_input = AdapterInput(
        adapter_input_id="input_001",
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        input_text="Test input",
        metadata=(),
    )

    # Check compliance
    validation_result = adapter.check_constitutional_compliance(adapter_input)

    # Verify validation executes and passes
    assert isinstance(validation_result, AdapterValidationResult)
    assert validation_result.is_valid
    assert len(validation_result.checked_constraints) > 0


def test_noop_validation_adapter_detects_authority_claims():
    """
    Test: NoOpValidationAdapter detects authority claims in input text.

    Constitutional Requirement:
        check_constitutional_compliance MUST detect authority claims.
    """
    adapter = NoOpValidationAdapter()

    # Create AdapterInput with authority claim
    adapter_input = AdapterInput(
        adapter_input_id="input_002",
        source_training_example_id="example_002",
        source_trace_id="trace_002",
        input_text="This is the final_answer to the question",
        metadata=(),
    )

    # Check compliance
    validation_result = adapter.check_constitutional_compliance(adapter_input)

    # Verify authority claim detected
    assert not validation_result.is_valid
    assert AdapterViolationType.AUTHORITY_CLAIM_ATTEMPTED in validation_result.violations


def test_noop_validation_adapter_factory():
    """
    Test: create_noop_validation_adapter factory works correctly.

    Constitutional Requirement:
        Factory MUST create valid NoOpValidationAdapter instance.
    """
    adapter = create_noop_validation_adapter()

    assert isinstance(adapter, NoOpValidationAdapter)
    assert adapter.adapter_name == "NoOpValidationAdapter"
    assert hasattr(adapter, 'validate_adapter_boundaries')
    assert hasattr(adapter, 'check_constitutional_compliance')


# ============================================================================
# Full Chain Integration Tests
# ============================================================================

def test_full_noop_chain_training_example_to_model_output():
    """
    Test: Full no-op chain works: TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput.

    Constitutional Formula:
        TrainingExample → (NoOpInputAdapter) → AdapterInput
                       → (simulated execution) → AdapterRawOutput
                       → (NoOpOutputAdapter) → ModelOutput

    This test proves contracts are fully implementable without T5.
    """
    # 1. Create TrainingExample
    training_example = TrainingExample(
        training_example_id="example_chain_001",
        source_dataset_row_id="row_chain_001",
        source_trace_id="trace_chain_abc123",
        source_algorithm="noop_test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Test chain input",
        target_text="Test chain target",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # 2. NoOpInputAdapter: TrainingExample → AdapterInput
    input_adapter = create_noop_input_adapter()
    adapter_input = input_adapter.prepare_input(training_example)

    # Verify AdapterInput created
    assert adapter_input.source_trace_id == training_example.source_trace_id
    assert adapter_input.source_training_example_id == training_example.training_example_id

    # 3. Simulate execution: AdapterInput → AdapterRawOutput
    # (In real T5, this would be model inference; here it's identity-like)
    adapter_raw_output = create_sample_adapter_raw_output(
        adapter_output_id=f"output_{adapter_input.adapter_input_id}",
        source_adapter_input_id=adapter_input.adapter_input_id,
        raw_text=adapter_input.input_text,  # Identity-like: input → output
    )

    # 4. NoOpOutputAdapter: AdapterRawOutput → ModelOutput
    output_adapter = create_noop_output_adapter()
    model_output = output_adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=adapter_input.source_training_example_id,
        source_trace_id=adapter_input.source_trace_id,
    )

    # 5. Verify full chain integrity
    assert model_output.source_trace_id == training_example.source_trace_id
    assert model_output.source_training_example_id == training_example.training_example_id
    assert isinstance(model_output.predicted_text, str)
    assert len(model_output.predicted_text) > 0


def test_full_noop_chain_with_validation():
    """
    Test: Full no-op chain with validation at each step.

    Constitutional Requirement:
        Each transformation MUST preserve source bindings and pass validation.
    """
    # Create adapters
    input_adapter = create_noop_input_adapter()
    output_adapter = create_noop_output_adapter()
    validation_adapter = create_noop_validation_adapter()

    # 1. TrainingExample
    training_example = TrainingExample(
        training_example_id="example_val_001",
        source_dataset_row_id="row_val_001",
        source_trace_id="trace_val_abc123",
        source_algorithm="validation_test",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Validation test input",
        target_text="Validation test target",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # 2. Prepare input
    adapter_input = input_adapter.prepare_input(training_example)

    # 3. Validate input
    input_validation = input_adapter.validate_input(adapter_input)
    assert input_validation.is_valid

    # 4. Check constitutional compliance
    compliance_validation = validation_adapter.check_constitutional_compliance(adapter_input)
    assert compliance_validation.is_valid

    # 5. Simulate execution
    adapter_raw_output = create_sample_adapter_raw_output(
        adapter_output_id=f"output_{adapter_input.adapter_input_id}",
        source_adapter_input_id=adapter_input.adapter_input_id,
        raw_text="Validation test output",
    )

    # 6. Parse output
    model_output = output_adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=adapter_input.source_training_example_id,
        source_trace_id=adapter_input.source_trace_id,
    )

    # 7. Validate output
    output_validation = output_adapter.validate_output(model_output)
    assert output_validation.is_valid

    # 8. Verify chain integrity
    assert model_output.source_trace_id == training_example.source_trace_id
    assert model_output.source_training_example_id == training_example.training_example_id


# ============================================================================
# Module Safety Tests
# ============================================================================

def test_no_forbidden_imports_in_noop_fixtures_module():
    """
    Test: No-op fixtures module contains no forbidden imports.

    Constitutional Requirement:
        Module MUST NOT import transformers or torch.
    """
    import tests.fixtures.dal_core.noop_adapter_fixtures as fixtures_module

    # Get module source
    source = inspect.getsource(fixtures_module)

    # Extract only import lines
    import_lines = [
        line.strip()
        for line in source.split('\n')
        if line.strip().startswith('import ') or line.strip().startswith('from ')
    ]

    # Verify no forbidden imports
    for import_line in import_lines:
        assert "transformers" not in import_line, f"Forbidden import found: {import_line}"
        assert "torch" not in import_line, f"Forbidden import found: {import_line}"


def test_no_execution_markers_in_noop_fixtures_module():
    """
    Test: No-op fixtures module contains no execution markers.

    Constitutional Requirement:
        Module MUST NOT contain tokenization, tensor conversion, model loading, etc.
    """
    import tests.fixtures.dal_core.noop_adapter_fixtures as fixtures_module

    # Get module source
    source = inspect.getsource(fixtures_module)

    # Check code lines only (not comments or docstrings)
    code_lines = [
        line.strip()
        for line in source.split('\n')
        if line.strip()
        and not line.strip().startswith('#')
        and not line.strip().startswith('"""')
        and not line.strip().startswith("'''")
        and '"""' not in line
        and "❌" not in line  # Skip forbidden operations lists
    ]

    code_text = ' '.join(code_lines)

    # Verify no execution markers
    assert ".encode(" not in code_text
    assert ".tokenize(" not in code_text
    assert "AutoTokenizer" not in code_text
    assert "T5ForConditionalGeneration" not in code_text
    assert "from_pretrained(" not in code_text
    assert "model.generate(" not in code_text
    assert "Trainer(" not in code_text
    assert "to_tensor(" not in code_text


def test_noop_fixtures_not_exported_from_src_dal_core():
    """
    Test: No-op fixtures are NOT exported from src/dal_core.

    Constitutional Requirement:
        No-op adapters MUST remain test fixtures only.
        They MUST NOT appear in src/dal_core/__init__.py or any production module.
    """
    # Check src/dal_core/__init__.py does NOT export no-op adapters
    import dal_core

    dal_core_exports = dir(dal_core)

    # Verify no-op adapters NOT in dal_core exports
    assert "NoOpInputAdapter" not in dal_core_exports
    assert "NoOpOutputAdapter" not in dal_core_exports
    assert "NoOpValidationAdapter" not in dal_core_exports
    assert "create_noop_input_adapter" not in dal_core_exports
    assert "create_noop_output_adapter" not in dal_core_exports
    assert "create_noop_validation_adapter" not in dal_core_exports


def test_noop_fixtures_only_in_tests_directory():
    """
    Test: No-op fixtures only exist in tests/ directory.

    Constitutional Requirement:
        No-op adapter implementations MUST only exist in tests/fixtures/.
        They MUST NOT exist anywhere in src/dal_core/.
    """
    import os
    import glob

    # Get repository root
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    src_dal_core_path = os.path.join(repo_root, 'src/dal_core')

    # Search for NoOp* classes in src/dal_core
    search_patterns = [
        'NoOpInputAdapter',
        'NoOpOutputAdapter',
        'NoOpValidationAdapter',
    ]

    for root, dirs, files in os.walk(src_dal_core_path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Check for class definitions (not just imports)
                    for pattern in search_patterns:
                        # Look for "class NoOp*" definitions
                        class_def = f"class {pattern}"
                        assert class_def not in content, (
                            f"Found {pattern} class definition in production code: {filepath}"
                        )


def test_noop_adapters_have_no_forbidden_methods():
    """
    Test: No-op adapter classes have no forbidden methods.

    Constitutional Requirement:
        No-op adapters MUST NOT implement tokenize, load_model, generate, etc.
    """
    input_adapter = NoOpInputAdapter()
    output_adapter = NoOpOutputAdapter()
    validation_adapter = NoOpValidationAdapter()

    # Forbidden methods
    forbidden_methods = [
        'tokenize', 'encode', 'decode', 'to_tensor', 'from_tensor',
        'load_model', 'from_pretrained', 'generate', 'forward',
        'train', 'train_step', 'upgrade_rank', 'resolve_residuals',
        'close_ifadah', 'produce_hukm', 'produce_reality',
    ]

    # Check NoOpInputAdapter
    for method in forbidden_methods:
        assert not hasattr(input_adapter, method), f"Forbidden method {method} found in NoOpInputAdapter"

    # Check NoOpOutputAdapter
    for method in forbidden_methods:
        assert not hasattr(output_adapter, method), f"Forbidden method {method} found in NoOpOutputAdapter"

    # Check NoOpValidationAdapter
    for method in forbidden_methods:
        assert not hasattr(validation_adapter, method), f"Forbidden method {method} found in NoOpValidationAdapter"


# ============================================================================
# Contract Implementability Proof Tests
# ============================================================================

def test_contract_implementability_proof():
    """
    Test: Prove that T5 Adapter Interface Contracts are fully implementable.

    Constitutional Proof:
        If NoOpAdapters can implement all contract methods without T5,
        then contracts are implementable (not tied to specific implementation).

    This test is the central proof of PR #153.
    """
    # 1. Create all no-op adapters
    input_adapter = create_noop_input_adapter()
    output_adapter = create_noop_output_adapter()
    validation_adapter = create_noop_validation_adapter()

    # 2. Verify all contract methods implemented
    # InputAdapterContract
    assert hasattr(input_adapter, 'prepare_input')
    assert hasattr(input_adapter, 'validate_input')

    # OutputAdapterContract
    assert hasattr(output_adapter, 'parse_output')
    assert hasattr(output_adapter, 'validate_output')

    # ValidationAdapterContract
    assert hasattr(validation_adapter, 'validate_adapter_boundaries')
    assert hasattr(validation_adapter, 'check_constitutional_compliance')

    # 3. Verify no T5 dependencies
    # (already tested in module safety tests)

    # 4. Verify full chain works
    training_example = TrainingExample(
        training_example_id="proof_001",
        source_dataset_row_id="proof_row_001",
        source_trace_id="proof_trace_001",
        source_algorithm="proof_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Proof input",
        target_text="Proof target",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    adapter_input = input_adapter.prepare_input(training_example)
    adapter_raw_output = create_sample_adapter_raw_output(
        source_adapter_input_id=adapter_input.adapter_input_id,
        raw_text="Proof output",
    )
    model_output = output_adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=adapter_input.source_training_example_id,
        source_trace_id=adapter_input.source_trace_id,
    )

    # 5. Verify integrity
    assert model_output.source_trace_id == training_example.source_trace_id
    assert model_output.source_training_example_id == training_example.training_example_id

    # QED: Contracts are implementable without T5


# ============================================================================
# Adapter Chain Registry Tests
# ============================================================================

def test_adapter_chain_link_creation():
    """
    Test: AdapterChainLink can be created from TrainingExample.

    Constitutional Requirement:
        Chain link MUST preserve source bindings.
    """
    # Create TrainingExample
    training_example = TrainingExample(
        training_example_id="chain_example_001",
        source_dataset_row_id="chain_row_001",
        source_trace_id="chain_trace_001",
        source_algorithm="chain_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Chain test input",
        target_text="Chain test target",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Create chain link
    chain = create_chain_link_from_training_example(
        training_example=training_example,
        link_id="link_001",
    )

    # Verify bindings preserved
    assert chain.source_training_example_id == training_example.training_example_id
    assert chain.source_trace_id == training_example.source_trace_id
    assert chain.link_id == "link_001"
    assert "training_example_created" in chain.transformation_steps


def test_adapter_chain_registry_creation():
    """
    Test: AdapterChainRegistry can be created and is immutable.

    Constitutional Requirement:
        Registry MUST be immutable (frozen dataclass).
    """
    registry = create_adapter_chain_registry("test_registry")

    # Verify immutability
    assert hasattr(registry, '__dataclass_fields__')

    with pytest.raises(AttributeError):
        registry.registry_id = "modified"  # type: ignore

    # Verify initial state
    assert registry.registry_id == "test_registry"
    assert len(registry.chains) == 0


def test_adapter_chain_preserves_bindings_through_full_chain():
    """
    Test: Adapter chain preserves bindings through full transformation.

    Constitutional Requirement:
        Source bindings MUST be preserved through entire chain:
        TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput
    """
    # 1. Create TrainingExample
    training_example = TrainingExample(
        training_example_id="full_chain_001",
        source_dataset_row_id="full_chain_row_001",
        source_trace_id="full_chain_trace_001",
        source_algorithm="full_chain_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Full chain input",
        target_text="Full chain target",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # 2. Create initial chain link
    chain = create_chain_link_from_training_example(
        training_example=training_example,
        link_id="full_chain_link_001",
    )

    # 3. Add AdapterInput
    input_adapter = create_noop_input_adapter()
    adapter_input = input_adapter.prepare_input(training_example)
    chain = add_adapter_input_to_chain(chain, adapter_input)

    # Verify bindings preserved
    assert chain.adapter_input_id == adapter_input.adapter_input_id
    assert "adapter_input_prepared" in chain.transformation_steps

    # 4. Add AdapterRawOutput
    adapter_raw_output = create_sample_adapter_raw_output(
        adapter_output_id="full_chain_output_001",
        source_adapter_input_id=adapter_input.adapter_input_id,
        raw_text="Full chain output",
    )
    chain = add_adapter_output_to_chain(chain, adapter_raw_output)

    # Verify bindings preserved
    assert chain.adapter_output_id == adapter_raw_output.adapter_output_id
    assert "adapter_raw_output_generated" in chain.transformation_steps

    # 5. Add ModelOutput
    output_adapter = create_noop_output_adapter()
    model_output = output_adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=training_example.training_example_id,
        source_trace_id=training_example.source_trace_id,
    )
    chain = add_model_output_to_chain(chain, model_output)

    # Verify bindings preserved through entire chain
    assert chain.model_output_id == model_output.model_output_id
    assert chain.source_training_example_id == training_example.training_example_id
    assert chain.source_trace_id == training_example.source_trace_id
    assert "model_output_parsed" in chain.transformation_steps

    # Verify all transformation steps recorded
    assert len(chain.transformation_steps) == 4
    assert chain.transformation_steps == (
        "training_example_created",
        "adapter_input_prepared",
        "adapter_raw_output_generated",
        "model_output_parsed",
    )


def test_adapter_chain_registry_find_operations():
    """
    Test: AdapterChainRegistry can find chains by trace_id and training_example_id.

    Constitutional Requirement:
        Registry MUST enable verification of binding preservation.
    """
    # Create registry
    registry = create_adapter_chain_registry("find_test_registry")

    # Create TrainingExample
    training_example = TrainingExample(
        training_example_id="find_example_001",
        source_dataset_row_id="find_row_001",
        source_trace_id="find_trace_001",
        source_algorithm="find_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Find test input",
        target_text="Find test target",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Create chain link
    chain = create_chain_link_from_training_example(
        training_example=training_example,
        link_id="find_link_001",
    )

    # Add to registry
    registry = registry.with_chain(chain)

    # Find by trace_id
    found_by_trace = registry.find_by_trace_id("find_trace_001")
    assert len(found_by_trace) == 1
    assert found_by_trace[0].link_id == "find_link_001"

    # Find by training_example_id
    found_by_example = registry.find_by_training_example_id("find_example_001")
    assert len(found_by_example) == 1
    assert found_by_example[0].link_id == "find_link_001"

    # Verify not found for non-existent IDs
    not_found = registry.find_by_trace_id("nonexistent_trace")
    assert len(not_found) == 0


def test_adapter_chain_detects_binding_loss():
    """
    Test: Adapter chain detects when source bindings are lost.

    Constitutional Requirement:
        Chain MUST reject transformations that lose source bindings.
    """
    # Create TrainingExample
    training_example = TrainingExample(
        training_example_id="binding_loss_001",
        source_dataset_row_id="binding_loss_row_001",
        source_trace_id="binding_loss_trace_001",
        source_algorithm="binding_loss_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Binding loss test",
        target_text="Binding loss target",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Create chain link
    chain = create_chain_link_from_training_example(
        training_example=training_example,
        link_id="binding_loss_link_001",
    )

    # Create AdapterInput with WRONG bindings
    adapter_input_wrong_bindings = AdapterInput(
        adapter_input_id="wrong_input_001",
        source_training_example_id="WRONG_EXAMPLE_ID",  # Wrong!
        source_trace_id=training_example.source_trace_id,
        input_text="Test input",
        metadata=(),
    )

    # Verify chain rejects AdapterInput with wrong bindings
    with pytest.raises(ValueError, match="lost source_training_example_id binding"):
        add_adapter_input_to_chain(chain, adapter_input_wrong_bindings)

