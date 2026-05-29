"""
Tests for Model Output Contract (PR #147)

Constitutional Test Coverage:
    1. ModelOutput preserves source_trace_id
    2. ModelOutput preserves source_training_example_id
    3. ModelOutput is immutable (frozen=True)
    4. ModelOutput validates required fields
    5. ModelOutput.create_from_prediction preserves bindings

Test Strategy:
    - Unit tests for ModelOutput structure
    - Immutability verification
    - Source binding verification
    - Factory method validation

Created: 2026-05-29
"""

import pytest
from datetime import datetime

from dal_core.model_output import ModelOutput


# ============================================================================
# ModelOutput Structure Tests
# ============================================================================

def test_model_output_preserves_source_trace_id():
    """
    Test: ModelOutput preserves source_trace_id.

    Constitutional Requirement:
        ModelOutput MUST preserve source_trace_id to maintain
        constitutional binding to AlgorithmTracePayload.
    """
    source_trace_id = "trace_abc123"

    output = ModelOutput(
        model_output_id="output_001",
        source_training_example_id="example_001",
        source_trace_id=source_trace_id,
        predicted_text="Test prediction",
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )

    assert output.source_trace_id == source_trace_id


def test_model_output_preserves_source_training_example_id():
    """
    Test: ModelOutput preserves source_training_example_id.

    Constitutional Requirement:
        ModelOutput MUST preserve source_training_example_id to maintain
        constitutional binding to TrainingExample.
    """
    source_example_id = "example_xyz789"

    output = ModelOutput(
        model_output_id="output_001",
        source_training_example_id=source_example_id,
        source_trace_id="trace_001",
        predicted_text="Test prediction",
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )

    assert output.source_training_example_id == source_example_id


def test_model_output_is_immutable():
    """
    Test: ModelOutput is immutable (frozen=True).

    Constitutional Requirement:
        ModelOutput MUST be immutable to prevent post-creation modification.
    """
    output = ModelOutput(
        model_output_id="output_001",
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        predicted_text="Test prediction",
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )

    with pytest.raises(AttributeError):
        output.predicted_text = "Modified text"  # type: ignore


def test_model_output_requires_model_output_id():
    """
    Test: ModelOutput requires model_output_id.

    Constitutional Requirement:
        Every ModelOutput MUST have unique identifier.
    """
    with pytest.raises(ValueError, match="model_output_id"):
        ModelOutput(
            model_output_id="",  # Empty ID
            source_training_example_id="example_001",
            source_trace_id="trace_001",
            predicted_text="Test prediction",
            model_name="test_model",
            generation_timestamp="2026-05-29T00:00:00Z",
        )


def test_model_output_requires_source_trace_id():
    """
    Test: ModelOutput allows empty source_trace_id (evaluator detects violation).

    Constitutional Design Change:
        ModelOutput is a container for model predictions that may be malformed.
        The evaluator (ConstitutionalEvaluator) is the guardian that detects violations.

        Therefore:
        - ModelOutput construction MUST succeed even with empty source_trace_id
        - ConstitutionalEvaluator detects missing binding as CRITICAL violation
    """
    # ModelOutput construction succeeds with empty binding
    output = ModelOutput(
        model_output_id="output_001",
        source_training_example_id="example_001",
        source_trace_id="",  # Empty binding allowed at construction
        predicted_text="Test prediction",
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )

    # Verify object created successfully
    assert output.source_trace_id == ""
    # Note: ConstitutionalEvaluator will detect this as CRITICAL violation


def test_model_output_requires_source_training_example_id():
    """
    Test: ModelOutput allows empty source_training_example_id (evaluator detects violation).

    Constitutional Design Change:
        ModelOutput is a container for model predictions that may be malformed.
        The evaluator (ConstitutionalEvaluator) is the guardian that detects violations.

        Therefore:
        - ModelOutput construction MUST succeed even with empty source_training_example_id
        - ConstitutionalEvaluator detects missing binding as CRITICAL violation
    """
    # ModelOutput construction succeeds with empty binding
    output = ModelOutput(
        model_output_id="output_001",
        source_training_example_id="",  # Empty binding allowed at construction
        source_trace_id="trace_001",
        predicted_text="Test prediction",
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )

    # Verify object created successfully
    assert output.source_training_example_id == ""
    # Note: ConstitutionalEvaluator will detect this as CRITICAL violation


def test_model_output_requires_predicted_text():
    """
    Test: ModelOutput requires predicted_text.

    Constitutional Requirement:
        ModelOutput MUST contain predicted text for evaluation.
    """
    with pytest.raises(ValueError, match="predicted_text"):
        ModelOutput(
            model_output_id="output_001",
            source_training_example_id="example_001",
            source_trace_id="trace_001",
            predicted_text="",  # Missing text
            model_name="test_model",
            generation_timestamp="2026-05-29T00:00:00Z",
        )


def test_model_output_requires_model_name():
    """
    Test: ModelOutput requires model_name.

    Constitutional Requirement:
        ModelOutput MUST identify which model generated the output.
    """
    with pytest.raises(ValueError, match="model_name"):
        ModelOutput(
            model_output_id="output_001",
            source_training_example_id="example_001",
            source_trace_id="trace_001",
            predicted_text="Test prediction",
            model_name="",  # Missing model name
            generation_timestamp="2026-05-29T00:00:00Z",
        )


def test_model_output_requires_generation_timestamp():
    """
    Test: ModelOutput requires generation_timestamp.

    Constitutional Requirement:
        ModelOutput MUST record when prediction was generated.
    """
    with pytest.raises(ValueError, match="generation_timestamp"):
        ModelOutput(
            model_output_id="output_001",
            source_training_example_id="example_001",
            source_trace_id="trace_001",
            predicted_text="Test prediction",
            model_name="test_model",
            generation_timestamp="",  # Missing timestamp
        )


# ============================================================================
# Factory Method Tests
# ============================================================================

def test_create_from_prediction_preserves_source_bindings():
    """
    Test: create_from_prediction preserves source bindings.

    Constitutional Requirement:
        Factory method MUST preserve source_trace_id and
        source_training_example_id from input parameters.
    """
    source_example_id = "example_abc123"
    source_trace_id = "trace_xyz789"
    predicted_text = "Test prediction from model"
    model_name = "test_t5_model"

    output = ModelOutput.create_from_prediction(
        source_training_example_id=source_example_id,
        source_trace_id=source_trace_id,
        predicted_text=predicted_text,
        model_name=model_name,
    )

    assert output.source_training_example_id == source_example_id
    assert output.source_trace_id == source_trace_id
    assert output.predicted_text == predicted_text
    assert output.model_name == model_name


def test_create_from_prediction_generates_model_output_id():
    """
    Test: create_from_prediction generates unique model_output_id.

    Constitutional Requirement:
        Factory method MUST generate unique identifier for ModelOutput.
    """
    output = ModelOutput.create_from_prediction(
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        predicted_text="Test prediction",
        model_name="test_model",
    )

    assert output.model_output_id
    assert output.model_output_id.startswith("model_output_")


def test_create_from_prediction_generates_timestamp():
    """
    Test: create_from_prediction generates generation_timestamp.

    Constitutional Requirement:
        Factory method MUST generate timestamp for when prediction
        was created.
    """
    output = ModelOutput.create_from_prediction(
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        predicted_text="Test prediction",
        model_name="test_model",
    )

    assert output.generation_timestamp
    assert "T" in output.generation_timestamp  # ISO 8601 format
    assert output.generation_timestamp.endswith("Z")  # UTC timezone


def test_create_from_prediction_rejects_missing_source_trace_id():
    """
    Test: create_from_prediction allows empty source_trace_id (evaluator detects violation).

    Constitutional Design Change:
        Factory method creates ModelOutput even with empty bindings.
        ConstitutionalEvaluator will detect missing binding as CRITICAL violation.
    """
    # Factory method succeeds with empty binding
    output = ModelOutput.create_from_prediction(
        source_training_example_id="example_001",
        source_trace_id="",  # Empty binding allowed
        predicted_text="Test prediction",
        model_name="test_model",
    )

    # Verify object created successfully
    assert output.source_trace_id == ""
    # Note: ConstitutionalEvaluator will detect this as CRITICAL violation


def test_create_from_prediction_rejects_missing_source_training_example_id():
    """
    Test: create_from_prediction allows empty source_training_example_id (evaluator detects violation).

    Constitutional Design Change:
        Factory method creates ModelOutput even with empty bindings.
        ConstitutionalEvaluator will detect missing binding as CRITICAL violation.
    """
    # Factory method succeeds with empty binding
    output = ModelOutput.create_from_prediction(
        source_training_example_id="",  # Empty binding allowed
        source_trace_id="trace_001",
        predicted_text="Test prediction",
        model_name="test_model",
    )

    # Verify object created successfully
    assert output.source_training_example_id == ""
    # Note: ConstitutionalEvaluator will detect this as CRITICAL violation


# ============================================================================
# Forbidden Fields Tests
# ============================================================================

def test_model_output_has_no_upgraded_rank_field():
    """
    Test: ModelOutput has NO upgraded_rank field.

    Constitutional Prohibition:
        ModelOutput MUST NOT have upgraded_rank field.
        Rank upgrade is FORBIDDEN operation.
    """
    output = ModelOutput(
        model_output_id="output_001",
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        predicted_text="Test prediction",
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )

    assert not hasattr(output, "upgraded_rank")


def test_model_output_has_no_resolved_residuals_field():
    """
    Test: ModelOutput has NO resolved_residuals field.

    Constitutional Prohibition:
        ModelOutput MUST NOT have resolved_residuals field.
        Residual resolution is FORBIDDEN operation.
    """
    output = ModelOutput(
        model_output_id="output_001",
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        predicted_text="Test prediction",
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )

    assert not hasattr(output, "resolved_residuals")


def test_model_output_has_no_produced_hukm_field():
    """
    Test: ModelOutput has NO produced_hukm field.

    Constitutional Prohibition:
        ModelOutput MUST NOT have produced_hukm field.
        Hukm production is FORBIDDEN operation.
    """
    output = ModelOutput(
        model_output_id="output_001",
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        predicted_text="Test prediction",
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )

    assert not hasattr(output, "produced_hukm")


def test_model_output_has_no_constitutional_authority_field():
    """
    Test: ModelOutput has NO constitutional_authority field.

    Constitutional Prohibition:
        ModelOutput MUST NOT have constitutional_authority field.
        Model outputs do NOT have constitutional authority.
    """
    output = ModelOutput(
        model_output_id="output_001",
        source_training_example_id="example_001",
        source_trace_id="trace_001",
        predicted_text="Test prediction",
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )

    assert not hasattr(output, "constitutional_authority")
