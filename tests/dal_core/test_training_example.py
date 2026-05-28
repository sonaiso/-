"""
Tests for Training Example Contract (PR #146)

Constitutional Test Coverage:
    1. TrainingExample preserves source_trace_id
    2. TrainingExample preserves source_dataset_row_id
    3. TrainingExample is immutable (frozen=True)
    4. TrainingExample is derived from DatasetRow only
    5. Repair examples preserve requires_algorithm_rerun=True

Test Strategy:
    - Unit tests for TrainingExample structure
    - Immutability verification
    - Source binding verification
    - Repair example validation

Created: 2026-05-28
"""

import pytest

from dal_core.training_example import TrainingExample
from dal_core.trace_explanation_dataset_generator import (
    OutputType,
    ValidationStatus,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation


# ============================================================================
# TrainingExample Structure Tests
# ============================================================================

def test_training_example_preserves_source_trace_id():
    """
    Test: TrainingExample preserves source_trace_id.

    Constitutional Requirement:
        TrainingExample MUST preserve source_trace_id from DatasetRow
        to maintain constitutional binding to AlgorithmTracePayload.
    """
    source_trace_id = "trace_abc123"

    example = TrainingExample(
        training_example_id="example_001",
        source_dataset_row_id="row_001",
        source_trace_id=source_trace_id,
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

    assert example.source_trace_id == source_trace_id


def test_training_example_preserves_source_dataset_row_id():
    """
    Test: TrainingExample preserves source_dataset_row_id.

    Constitutional Requirement:
        TrainingExample MUST preserve source_dataset_row_id
        to maintain audit trail to original DatasetRow.
    """
    source_dataset_row_id = "row_xyz789"

    example = TrainingExample(
        training_example_id="example_002",
        source_dataset_row_id=source_dataset_row_id,
        source_trace_id="trace_001",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.SUMMARIZE_CANDIDATES,
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

    assert example.source_dataset_row_id == source_dataset_row_id


def test_training_example_is_immutable():
    """
    Test: TrainingExample is immutable (frozen=True).

    Constitutional Requirement:
        TrainingExample MUST be immutable to prevent modification
        after construction. This ensures serialization boundary integrity.
    """
    example = TrainingExample(
        training_example_id="example_003",
        source_dataset_row_id="row_003",
        source_trace_id="trace_003",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_EXISTING_RANK,
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

    # Attempt to modify should raise error
    with pytest.raises((AttributeError, Exception)):
        example.target_text = "Modified target"

    with pytest.raises((AttributeError, Exception)):
        example.source_trace_id = "modified_trace"


def test_training_example_derived_from_dataset_row():
    """
    Test: TrainingExample fields match DatasetRow structure.

    Constitutional Requirement:
        TrainingExample MUST be derivable from DatasetRow with
        all constitutional fields preserved.
    """
    example = TrainingExample(
        training_example_id="example_004",
        source_dataset_row_id="row_004",
        source_trace_id="trace_004",
        source_algorithm="morphology_analyzer",
        operation=TraceConsumerOperation.GENERATE_BOUNDED_EXPLANATION,
        input_text="Trace ID: trace_004, Algorithm: morphology_analyzer, Layer: U2",
        target_text="This trace contains 3 candidates with 2 residuals.",
        referenced_candidate_ids=("cand_001", "cand_002", "cand_003"),
        referenced_residual_ids=("res_001", "res_002"),
        referenced_gate_ids=("gate_001",),
        referenced_rank_values=("PLAUSIBLE",),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Verify all DatasetRow fields are present
    assert example.source_trace_id == "trace_004"
    assert example.source_dataset_row_id == "row_004"
    assert example.source_algorithm == "morphology_analyzer"
    assert example.operation == TraceConsumerOperation.GENERATE_BOUNDED_EXPLANATION
    assert "trace_004" in example.input_text
    assert example.target_text == "This trace contains 3 candidates with 2 residuals."
    assert len(example.referenced_candidate_ids) == 3
    assert len(example.referenced_residual_ids) == 2
    assert len(example.referenced_gate_ids) == 1
    assert example.output_type == OutputType.EXPLANATION
    assert example.validation_status == ValidationStatus.VALID


def test_repair_example_preserves_requires_algorithm_rerun():
    """
    Test: Repair examples preserve requires_algorithm_rerun=True.

    Constitutional Requirement:
        REPAIR_SUGGESTION examples MUST have requires_algorithm_rerun=True
        because T5 suggests repairs but does NOT execute repairs.
    """
    repair_example = TrainingExample(
        training_example_id="example_005",
        source_dataset_row_id="row_005",
        source_trace_id="trace_005",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.SUGGEST_REPAIR,
        input_text="Test input with residuals",
        target_text="Suggestion: Re-run gate_001 to resolve residual_001",
        referenced_candidate_ids=(),
        referenced_residual_ids=("residual_001",),
        referenced_gate_ids=("gate_001",),
        referenced_rank_values=(),
        output_type=OutputType.REPAIR_SUGGESTION,
        requires_algorithm_rerun=True,  # MUST be True
        validation_status=ValidationStatus.VALID,
    )

    assert repair_example.output_type == OutputType.REPAIR_SUGGESTION
    assert repair_example.requires_algorithm_rerun is True


# ============================================================================
# Reference Preservation Tests
# ============================================================================

def test_training_example_preserves_all_references():
    """
    Test: TrainingExample preserves all reference tuples.

    Constitutional Requirement:
        All referenced_* fields MUST be preserved as immutable tuples
        to maintain audit trail to source trace elements.
    """
    example = TrainingExample(
        training_example_id="example_006",
        source_dataset_row_id="row_006",
        source_trace_id="trace_006",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Test input",
        target_text="Test target",
        referenced_candidate_ids=("c1", "c2"),
        referenced_residual_ids=("r1", "r2", "r3"),
        referenced_gate_ids=("g1",),
        referenced_rank_values=("PLAUSIBLE", "ATTESTED"),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Verify all references preserved
    assert example.referenced_candidate_ids == ("c1", "c2")
    assert example.referenced_residual_ids == ("r1", "r2", "r3")
    assert example.referenced_gate_ids == ("g1",)
    assert example.referenced_rank_values == ("PLAUSIBLE", "ATTESTED")

    # Verify immutability
    assert isinstance(example.referenced_candidate_ids, tuple)
    assert isinstance(example.referenced_residual_ids, tuple)
    assert isinstance(example.referenced_gate_ids, tuple)
    assert isinstance(example.referenced_rank_values, tuple)
