"""
Golden No-Op Adapter Chain Fixtures (PR #155)

Constitutional Purpose:
    Prove that adapter chains can be reproduced deterministically
    with preserved bindings and traceable transformations BEFORE
    any real model integration (T5, Hugging Face, tokenizers).

Constitutional Laws:
    1. Golden fixtures are TEST DATA ONLY (not production implementation)
    2. Golden fixtures do NOT import transformers
    3. Golden fixtures do NOT import torch
    4. Golden fixtures do NOT tokenize
    5. Golden fixtures do NOT create tensors
    6. Golden fixtures do NOT load models
    7. Golden fixtures do NOT execute inference
    8. Golden fixtures do NOT train models
    9. Golden fixtures preserve source bindings deterministically
    10. Golden fixtures demonstrate chain integrity preservation

Forbidden Operations:
    ❌ import transformers: Golden fixtures do NOT import transformers
    ❌ import torch: Golden fixtures do NOT import torch
    ❌ .encode(): Golden fixtures do NOT tokenize
    ❌ .to_tensor(): Golden fixtures do NOT create tensors
    ❌ .from_pretrained(): Golden fixtures do NOT load models
    ❌ model.generate(): Golden fixtures do NOT generate
    ❌ Trainer(): Golden fixtures do NOT train

Permitted Operations:
    ✅ Immutable fixture data structures
    ✅ Source binding preservation examples
    ✅ Chain integrity demonstration
    ✅ Validation status examples
    ✅ Reference preservation examples (candidate/residual/gate/rank IDs)

Supreme Law:
    Golden fixtures prove deterministic chain behavior.
    Golden fixtures do NOT implement T5.

Reference:
    Builds on: PR #154 (No-Op Adapter Fixtures with Chain Registry)
    Purpose: Prove chain reproducibility before T5 implementation
    Next step: NOT T5 implementation (boundary review or controlled preflight)

Created: 2026-05-29
"""

from dataclasses import dataclass
from typing import Tuple

from dal_core.training_example import TrainingExample
from dal_core.t5_adapter_interface_contracts import (
    AdapterInput,
    AdapterRawOutput,
    AdapterValidationResult,
    AdapterStatus,
    AdapterViolationType,
)
from dal_core.model_output import ModelOutput
from dal_core.algorithm_trace_payload import TraceConsumerOperation
from dal_core.trace_explanation_dataset_generator import OutputType, ValidationStatus

# Import chain registry types from noop adapter fixtures
from tests.fixtures.dal_core.noop_adapter_fixtures import (
    AdapterChainLink,
    AdapterChainRegistry,
    NoOpInputAdapter,
    NoOpOutputAdapter,
    NoOpValidationAdapter,
    create_chain_link_from_training_example,
    add_adapter_input_to_chain,
    add_adapter_output_to_chain,
    add_model_output_to_chain,
)


# ============================================================================
# Golden No-Op Chain Fixture
# ============================================================================

@dataclass(frozen=True)
class GoldenNoOpChainFixture:
    """
    Immutable golden chain fixture for testing adapter chains.

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - fixture_id is unique identifier
        - source_training_example is the starting point
        - adapter_input is prepared input (no tokenization)
        - adapter_raw_output is abstract output (no tensor decoding)
        - model_output is final output for ConstitutionalEvaluator
        - adapter_chain_registry tracks transformation chain
        - expected_validation_status indicates expected validation result
        - expected_violations lists expected boundary violations
        - expected_preserved_bindings confirms binding preservation
        - description explains the fixture's purpose

    Fields:
        fixture_id: Unique identifier for this golden fixture
        description: Human-readable description of fixture purpose
        source_training_example: TrainingExample (chain start)
        adapter_input: AdapterInput (after prepare_input)
        adapter_raw_output: AdapterRawOutput (abstract output)
        model_output: ModelOutput (final output for evaluation)
        adapter_chain_registry: Registry tracking chain transformations
        expected_validation_status: Expected validation result
        expected_violations: Expected adapter boundary violations
        expected_preserved_bindings: Bindings that should be preserved
    """
    fixture_id: str
    description: str
    source_training_example: TrainingExample
    adapter_input: AdapterInput
    adapter_raw_output: AdapterRawOutput
    model_output: ModelOutput
    adapter_chain_registry: AdapterChainRegistry
    expected_validation_status: bool  # True = valid, False = invalid
    expected_violations: Tuple[AdapterViolationType, ...]
    expected_preserved_bindings: Tuple[str, ...]  # List of binding field names


# ============================================================================
# Golden Fixture Factories
# ============================================================================

def make_valid_explanation_chain_fixture() -> GoldenNoOpChainFixture:
    """
    Create golden fixture for valid explanation chain.

    Chain: TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput

    Constitutional Requirements:
        - All source bindings preserved through chain
        - No authority markers present
        - No violations detected
        - Suitable for ConstitutionalEvaluator input

    Returns:
        GoldenNoOpChainFixture with valid chain
    """
    # Create training example with rich trace references
    training_example = TrainingExample(
        training_example_id="golden_te_001",
        source_dataset_row_id="golden_row_001",
        source_trace_id="golden_trace_001",
        source_algorithm="mufrad_analyzer_v1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Explain candidates: candidate_c1, candidate_c2 with residual_r1",
        target_text="The algorithm identified two candidates (candidate_c1, candidate_c2) "
                    "during morphological analysis. Residual residual_r1 indicates unresolved "
                    "ambiguity between the candidates. Both candidates hold PLAUSIBLE rank.",
        referenced_candidate_ids=("candidate_c1", "candidate_c2"),
        referenced_residual_ids=("residual_r1",),
        referenced_gate_ids=("gate_morphology_pattern_match",),
        referenced_rank_values=("PLAUSIBLE",),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Prepare adapter input
    input_adapter = NoOpInputAdapter()
    adapter_input = input_adapter.prepare_input(training_example)

    # Create adapter raw output
    adapter_raw_output = AdapterRawOutput(
        adapter_output_id="golden_output_001",
        source_adapter_input_id=adapter_input.adapter_input_id,
        raw_output_text="[OUTPUT] The algorithm identified two candidates (candidate_c1, candidate_c2) "
                       "during morphological analysis. Residual residual_r1 indicates unresolved "
                       "ambiguity between the candidates. Both candidates hold PLAUSIBLE rank.",
        adapter_metadata=(
            ("adapter_type", "noop"),
            ("version", "fixture_1.0"),
        ),
    )

    # Parse to model output
    output_adapter = NoOpOutputAdapter()
    model_output = output_adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=training_example.training_example_id,
        source_trace_id=training_example.source_trace_id,
    )

    # Build chain registry
    chain_link = create_chain_link_from_training_example(
        training_example=training_example,
        link_id="golden_chain_001",
    )
    chain_link = add_adapter_input_to_chain(chain_link, adapter_input)
    chain_link = add_adapter_output_to_chain(chain_link, adapter_raw_output)
    chain_link = add_model_output_to_chain(chain_link, model_output)

    registry = AdapterChainRegistry(
        registry_id="golden_registry_001",
        chains=(chain_link,),
    )

    return GoldenNoOpChainFixture(
        fixture_id="golden_fixture_001_valid_explanation",
        description="Valid explanation chain with preserved bindings and referenced IDs",
        source_training_example=training_example,
        adapter_input=adapter_input,
        adapter_raw_output=adapter_raw_output,
        model_output=model_output,
        adapter_chain_registry=registry,
        expected_validation_status=True,
        expected_violations=(),
        expected_preserved_bindings=(
            "source_trace_id",
            "source_training_example_id",
        ),
    )


def make_authority_violation_chain_fixture() -> GoldenNoOpChainFixture:
    """
    Create golden fixture for chain with authority marker in input.

    Chain: TrainingExample → AdapterInput (with authority marker) → ...

    Constitutional Requirements:
        - Authority marker detected by validation adapter
        - AUTHORITY_CLAIM_ATTEMPTED violation expected
        - Chain demonstrates validation detection capability

    Returns:
        GoldenNoOpChainFixture with authority violation
    """
    # Create training example with authority marker
    training_example = TrainingExample(
        training_example_id="golden_te_002",
        source_dataset_row_id="golden_row_002",
        source_trace_id="golden_trace_002",
        source_algorithm="invalid_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="This is the final_answer for the analysis",  # Authority marker
        target_text="Invalid output with authority claim",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Prepare adapter input (contains authority marker)
    input_adapter = NoOpInputAdapter()
    adapter_input = input_adapter.prepare_input(training_example)

    # Create adapter raw output
    adapter_raw_output = AdapterRawOutput(
        adapter_output_id="golden_output_002",
        source_adapter_input_id=adapter_input.adapter_input_id,
        raw_output_text="[OUTPUT] Invalid output",
        adapter_metadata=(
            ("adapter_type", "noop"),
            ("version", "fixture_1.0"),
        ),
    )

    # Parse to model output
    output_adapter = NoOpOutputAdapter()
    model_output = output_adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=training_example.training_example_id,
        source_trace_id=training_example.source_trace_id,
    )

    # Build chain registry
    chain_link = create_chain_link_from_training_example(
        training_example=training_example,
        link_id="golden_chain_002",
    )
    chain_link = add_adapter_input_to_chain(chain_link, adapter_input)
    chain_link = add_adapter_output_to_chain(chain_link, adapter_raw_output)
    chain_link = add_model_output_to_chain(chain_link, model_output)

    registry = AdapterChainRegistry(
        registry_id="golden_registry_002",
        chains=(chain_link,),
    )

    return GoldenNoOpChainFixture(
        fixture_id="golden_fixture_002_authority_violation",
        description="Chain with authority marker detected by validation adapter",
        source_training_example=training_example,
        adapter_input=adapter_input,
        adapter_raw_output=adapter_raw_output,
        model_output=model_output,
        adapter_chain_registry=registry,
        expected_validation_status=False,
        expected_violations=(AdapterViolationType.AUTHORITY_CLAIM_ATTEMPTED,),
        expected_preserved_bindings=(
            "source_trace_id",
            "source_training_example_id",
        ),
    )


def make_binding_loss_blocked_fixture() -> GoldenNoOpChainFixture:
    """
    Create golden fixture demonstrating binding loss prevention.

    Demonstrates: ValueError raised when adapter loses source bindings

    Constitutional Requirements:
        - Adapter chain functions detect binding loss
        - ValueError raised immediately
        - Chain integrity preserved

    Returns:
        GoldenNoOpChainFixture showing expected ValueError scenario
    """
    # Create valid training example
    training_example = TrainingExample(
        training_example_id="golden_te_003",
        source_dataset_row_id="golden_row_003",
        source_trace_id="golden_trace_003",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Valid input text",
        target_text="Valid target text",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Create adapter input (this will be used to demonstrate the error case)
    adapter_input = AdapterInput(
        adapter_input_id="golden_input_003",
        source_training_example_id="WRONG_ID",  # Mismatched binding
        source_trace_id=training_example.source_trace_id,
        input_text="[INPUT] Valid input text",
        metadata=(("adapter_name", "NoOpInputAdapter"),),
    )

    # For demonstration, create valid outputs (won't be reached in error test)
    adapter_raw_output = AdapterRawOutput(
        adapter_output_id="golden_output_003",
        source_adapter_input_id=adapter_input.adapter_input_id,
        raw_output_text="[OUTPUT] Valid output",
        adapter_metadata=(
            ("adapter_type", "noop"),
            ("version", "fixture_1.0"),
        ),
    )

    output_adapter = NoOpOutputAdapter()
    model_output = output_adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=training_example.training_example_id,
        source_trace_id=training_example.source_trace_id,
    )

    # Create minimal chain (will fail at add_adapter_input_to_chain)
    chain_link = create_chain_link_from_training_example(
        training_example=training_example,
        link_id="golden_chain_003",
    )

    registry = AdapterChainRegistry(
        registry_id="golden_registry_003",
        chains=(chain_link,),
    )

    return GoldenNoOpChainFixture(
        fixture_id="golden_fixture_003_binding_loss_blocked",
        description="Demonstrates ValueError when adapter loses source_training_example_id",
        source_training_example=training_example,
        adapter_input=adapter_input,  # Has wrong binding
        adapter_raw_output=adapter_raw_output,
        model_output=model_output,
        adapter_chain_registry=registry,
        expected_validation_status=False,
        expected_violations=(),  # ValueError, not violation
        expected_preserved_bindings=(),  # No bindings preserved (error case)
    )


def make_wrong_adapter_output_link_blocked_fixture() -> GoldenNoOpChainFixture:
    """
    Create golden fixture demonstrating wrong adapter output link detection.

    Demonstrates: ValueError raised when adapter output references wrong input

    Constitutional Requirements:
        - Chain functions verify adapter output links to correct input
        - ValueError raised immediately
        - Chain integrity preserved

    Returns:
        GoldenNoOpChainFixture showing expected ValueError scenario
    """
    # Create valid training example
    training_example = TrainingExample(
        training_example_id="golden_te_004",
        source_dataset_row_id="golden_row_004",
        source_trace_id="golden_trace_004",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Valid input text",
        target_text="Valid target text",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Create valid adapter input
    input_adapter = NoOpInputAdapter()
    adapter_input = input_adapter.prepare_input(training_example)

    # Create adapter raw output with WRONG source_adapter_input_id
    adapter_raw_output = AdapterRawOutput(
        adapter_output_id="golden_output_004",
        source_adapter_input_id="WRONG_INPUT_ID",  # Wrong reference
        raw_output_text="[OUTPUT] Valid output",
        adapter_metadata=(
            ("adapter_type", "noop"),
            ("version", "fixture_1.0"),
        ),
    )

    output_adapter = NoOpOutputAdapter()
    model_output = output_adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=training_example.training_example_id,
        source_trace_id=training_example.source_trace_id,
    )

    # Create chain (will fail at add_adapter_output_to_chain)
    chain_link = create_chain_link_from_training_example(
        training_example=training_example,
        link_id="golden_chain_004",
    )
    chain_link = add_adapter_input_to_chain(chain_link, adapter_input)

    registry = AdapterChainRegistry(
        registry_id="golden_registry_004",
        chains=(chain_link,),
    )

    return GoldenNoOpChainFixture(
        fixture_id="golden_fixture_004_wrong_output_link_blocked",
        description="Demonstrates ValueError when adapter output references wrong input",
        source_training_example=training_example,
        adapter_input=adapter_input,
        adapter_raw_output=adapter_raw_output,  # Has wrong link
        model_output=model_output,
        adapter_chain_registry=registry,
        expected_validation_status=False,
        expected_violations=(),  # ValueError, not violation
        expected_preserved_bindings=(),  # Error case
    )


def make_reference_preservation_chain_fixture() -> GoldenNoOpChainFixture:
    """
    Create golden fixture demonstrating reference preservation.

    Chain: TrainingExample (with rich references) → ... → ModelOutput

    Constitutional Requirements:
        - Referenced candidate IDs preserved
        - Referenced residual IDs preserved
        - Referenced gate IDs preserved
        - Referenced rank values preserved
        - All references traceable through metadata

    Returns:
        GoldenNoOpChainFixture with reference preservation
    """
    # Create training example with comprehensive references
    training_example = TrainingExample(
        training_example_id="golden_te_005",
        source_dataset_row_id="golden_row_005",
        source_trace_id="golden_trace_005",
        source_algorithm="comprehensive_analyzer_v2",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Analyze candidates: candidate_c10, candidate_c11, candidate_c12 "
                   "with residuals: residual_r5, residual_r6 "
                   "using gates: gate_sukun_repair, gate_shadda_enforcement "
                   "at ranks: PLAUSIBLE, DEFENSIBLE",
        target_text="Analysis shows three candidates (candidate_c10, candidate_c11, candidate_c12) "
                   "with two residuals (residual_r5, residual_r6). Gates gate_sukun_repair and "
                   "gate_shadda_enforcement were applied. Ranks: PLAUSIBLE for candidate_c10, "
                   "DEFENSIBLE for candidate_c11 and candidate_c12.",
        referenced_candidate_ids=("candidate_c10", "candidate_c11", "candidate_c12"),
        referenced_residual_ids=("residual_r5", "residual_r6"),
        referenced_gate_ids=("gate_sukun_repair", "gate_shadda_enforcement"),
        referenced_rank_values=("PLAUSIBLE", "DEFENSIBLE"),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Prepare adapter input
    input_adapter = NoOpInputAdapter()
    adapter_input = input_adapter.prepare_input(training_example)

    # Create adapter raw output preserving references
    adapter_raw_output = AdapterRawOutput(
        adapter_output_id="golden_output_005",
        source_adapter_input_id=adapter_input.adapter_input_id,
        raw_output_text="[OUTPUT] Analysis shows three candidates (candidate_c10, candidate_c11, candidate_c12) "
                       "with two residuals (residual_r5, residual_r6). Gates gate_sukun_repair and "
                       "gate_shadda_enforcement were applied. Ranks: PLAUSIBLE for candidate_c10, "
                       "DEFENSIBLE for candidate_c11 and candidate_c12.",
        adapter_metadata=(
            ("adapter_type", "noop"),
            ("version", "fixture_1.0"),
            ("referenced_candidates", "candidate_c10,candidate_c11,candidate_c12"),
            ("referenced_residuals", "residual_r5,residual_r6"),
            ("referenced_gates", "gate_sukun_repair,gate_shadda_enforcement"),
            ("referenced_ranks", "PLAUSIBLE,DEFENSIBLE"),
        ),
    )

    # Parse to model output
    output_adapter = NoOpOutputAdapter()
    model_output = output_adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=training_example.training_example_id,
        source_trace_id=training_example.source_trace_id,
    )

    # Build chain registry
    chain_link = create_chain_link_from_training_example(
        training_example=training_example,
        link_id="golden_chain_005",
    )
    chain_link = add_adapter_input_to_chain(chain_link, adapter_input)
    chain_link = add_adapter_output_to_chain(chain_link, adapter_raw_output)
    chain_link = add_model_output_to_chain(chain_link, model_output)

    registry = AdapterChainRegistry(
        registry_id="golden_registry_005",
        chains=(chain_link,),
    )

    return GoldenNoOpChainFixture(
        fixture_id="golden_fixture_005_reference_preservation",
        description="Chain preserving referenced candidate/residual/gate/rank IDs through metadata",
        source_training_example=training_example,
        adapter_input=adapter_input,
        adapter_raw_output=adapter_raw_output,
        model_output=model_output,
        adapter_chain_registry=registry,
        expected_validation_status=True,
        expected_violations=(),
        expected_preserved_bindings=(
            "source_trace_id",
            "source_training_example_id",
            "referenced_candidate_ids",
            "referenced_residual_ids",
            "referenced_gate_ids",
            "referenced_rank_values",
        ),
    )


def make_constitutional_evaluator_ready_fixture() -> GoldenNoOpChainFixture:
    """
    Create golden fixture for ModelOutput suitable for ConstitutionalEvaluator.

    Chain: TrainingExample → ... → ModelOutput (ready for evaluation)

    Constitutional Requirements:
        - ModelOutput has all required bindings
        - ModelOutput has predicted_text
        - ModelOutput has model_name
        - ModelOutput has generation_timestamp
        - ModelOutput ready for ConstitutionalEvaluator.evaluate()

    Returns:
        GoldenNoOpChainFixture with ConstitutionalEvaluator-ready output
    """
    # Create training example
    training_example = TrainingExample(
        training_example_id="golden_te_006",
        source_dataset_row_id="golden_row_006",
        source_trace_id="golden_trace_006",
        source_algorithm="evaluator_test_v1",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Explain candidate_eval_1 with residual_eval_1",
        target_text="The candidate candidate_eval_1 was identified. Residual residual_eval_1 remains.",
        referenced_candidate_ids=("candidate_eval_1",),
        referenced_residual_ids=("residual_eval_1",),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Prepare adapter input
    input_adapter = NoOpInputAdapter()
    adapter_input = input_adapter.prepare_input(training_example)

    # Create adapter raw output
    adapter_raw_output = AdapterRawOutput(
        adapter_output_id="golden_output_006",
        source_adapter_input_id=adapter_input.adapter_input_id,
        raw_output_text="[OUTPUT] The candidate candidate_eval_1 was identified. "
                       "Residual residual_eval_1 remains.",
        adapter_metadata=(
            ("adapter_type", "noop"),
            ("version", "fixture_1.0"),
        ),
    )

    # Parse to model output (ConstitutionalEvaluator-ready)
    output_adapter = NoOpOutputAdapter()
    model_output = output_adapter.parse_output(
        adapter_raw_output=adapter_raw_output,
        source_training_example_id=training_example.training_example_id,
        source_trace_id=training_example.source_trace_id,
    )

    # Build chain registry
    chain_link = create_chain_link_from_training_example(
        training_example=training_example,
        link_id="golden_chain_006",
    )
    chain_link = add_adapter_input_to_chain(chain_link, adapter_input)
    chain_link = add_adapter_output_to_chain(chain_link, adapter_raw_output)
    chain_link = add_model_output_to_chain(chain_link, model_output)

    registry = AdapterChainRegistry(
        registry_id="golden_registry_006",
        chains=(chain_link,),
    )

    return GoldenNoOpChainFixture(
        fixture_id="golden_fixture_006_evaluator_ready",
        description="ModelOutput ready for ConstitutionalEvaluator with all required fields",
        source_training_example=training_example,
        adapter_input=adapter_input,
        adapter_raw_output=adapter_raw_output,
        model_output=model_output,
        adapter_chain_registry=registry,
        expected_validation_status=True,
        expected_violations=(),
        expected_preserved_bindings=(
            "source_trace_id",
            "source_training_example_id",
            "model_output_id",
            "predicted_text",
            "model_name",
            "generation_timestamp",
        ),
    )


def all_golden_noop_chain_fixtures() -> Tuple[GoldenNoOpChainFixture, ...]:
    """
    Get all golden no-op adapter chain fixtures.

    Returns:
        Tuple of all 6 golden fixtures
    """
    return (
        make_valid_explanation_chain_fixture(),
        make_authority_violation_chain_fixture(),
        make_binding_loss_blocked_fixture(),
        make_wrong_adapter_output_link_blocked_fixture(),
        make_reference_preservation_chain_fixture(),
        make_constitutional_evaluator_ready_fixture(),
    )
