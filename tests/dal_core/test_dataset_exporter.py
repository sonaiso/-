"""
Tests for Dataset Exporter Contract (PR #146)

Constitutional Test Coverage:
    1. Export rejects invalid DatasetRow (validation_status != VALID)
    2. Export rejects forbidden authority phrases
    3. Export to JSONL preserves source bindings
    4. Export to JSONL contains no forbidden fields
    5. Export does not create candidate/rank/ifadah/hukm/reality

Test Strategy:
    - Unit tests for dataset_row_to_training_example
    - Validation tests for forbidden content
    - JSONL export format verification
    - Constitutional boundary enforcement

Created: 2026-05-28
"""

import json
import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from dal_core.dataset_exporter import (
    DatasetExporter,
    DatasetExportResult,
    DatasetExportResidual,
    FORBIDDEN_AUTHORITY_PHRASES,
)
from dal_core.training_example import TrainingExample
from dal_core.trace_explanation_dataset_generator import (
    DatasetRow,
    DatasetGenerationResidual,
    OutputType,
    ValidationStatus,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation


# ============================================================================
# Dataset Row to Training Example Tests
# ============================================================================

def test_export_rejects_invalid_dataset_row():
    """
    Test: Export rejects DatasetRow with validation_status != VALID.

    Constitutional Requirement:
        Only VALID DatasetRows may be exported to training format.
        Invalid rows MUST be rejected.
    """
    invalid_row = DatasetRow(
        dataset_row_id="row_001",
        source_trace_id="trace_001",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_trace_summary="Test summary",
        target_output_text="Test output",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.REJECTED_VALIDATION_FAILURE,  # INVALID
        residuals_about_dataset_generation=(),
    )

    # Attempt to convert should raise ValueError
    with pytest.raises(ValueError) as exc_info:
        DatasetExporter.dataset_row_to_training_example(invalid_row)

    assert "Constitutional violation" in str(exc_info.value)
    assert "VALID" in str(exc_info.value)


def test_export_rejects_forbidden_authority_phrases():
    """
    Test: Export validation rejects forbidden authority phrases.

    Constitutional Requirement:
        Training examples containing forbidden authority phrases
        (e.g., "final_answer", "correct_analysis") MUST be rejected.
    """
    # Create example with forbidden phrase in target_text
    example = TrainingExample(
        training_example_id="example_001",
        source_dataset_row_id="row_001",
        source_trace_id="trace_001",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Test input",
        target_text="This is the final_answer to the analysis.",  # FORBIDDEN
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    result = DatasetExporter.validate_training_example(example)

    assert result.success is False
    assert result.rejected_count == 1
    assert len(result.residuals) > 0
    assert any("forbidden" in r.issue_type.lower() for r in result.residuals)
    assert any("final_answer" in r.message.lower() for r in result.residuals)


def test_export_to_jsonl_preserves_source_bindings():
    """
    Test: JSONL export preserves source_trace_id and source_dataset_row_id.

    Constitutional Requirement:
        All exported training examples MUST preserve constitutional bindings
        to source trace and source dataset row.
    """
    # Create valid training example
    example = TrainingExample(
        training_example_id="example_002",
        source_dataset_row_id="row_002",
        source_trace_id="trace_002",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.SUMMARIZE_CANDIDATES,
        input_text="Test input summary",
        target_text="Test target output",
        referenced_candidate_ids=("cand_001",),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    # Export to temporary JSONL file
    with TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_export.jsonl"
        result = DatasetExporter.export_to_jsonl((example,), output_path)

        assert result.success is True
        assert result.exported_count == 1
        assert result.rejected_count == 0
        assert output_path.exists()

        # Read JSONL and verify source bindings
        with open(output_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            data = json.loads(line)

            assert data['source_trace_id'] == "trace_002"
            assert data['source_dataset_row_id'] == "row_002"
            assert data['training_example_id'] == "example_002"


def test_export_to_jsonl_contains_no_forbidden_fields():
    """
    Test: JSONL export does not contain forbidden authority fields.

    Constitutional Requirement:
        Exported JSONL MUST NOT contain fields like:
        - upgraded_rank
        - resolved_residuals
        - closed_ifadah
        - produced_hukm
        - produced_reality
        - new_candidate
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

    with TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_export.jsonl"
        result = DatasetExporter.export_to_jsonl((example,), output_path)

        assert result.success is True

        # Read JSONL and verify no forbidden fields
        with open(output_path, 'r', encoding='utf-8') as f:
            line = f.readline()
            data = json.loads(line)

            # Forbidden fields MUST NOT exist
            assert 'upgraded_rank' not in data
            assert 'resolved_residuals' not in data
            assert 'closed_ifadah' not in data
            assert 'produced_hukm' not in data
            assert 'produced_reality' not in data
            assert 'new_candidate' not in data
            assert 'semantic_certainty' not in data
            assert 'final_answer' not in data
            assert 'correct_analysis' not in data
            assert 'gold_label_hukm' not in data


def test_export_does_not_create_candidate_rank_ifadah_hukm_or_reality():
    """
    Test: Export process does NOT create candidates, rank, ifādah, hukm, or reality.

    Constitutional Requirement:
        Dataset export is serialization boundary only.
        Export MUST NOT create any constitutional facts:
        - No candidate creation
        - No rank upgrade
        - No ifādah closure
        - No hukm production
        - No reality establishment
    """
    # Create valid DatasetRow
    valid_row = DatasetRow(
        dataset_row_id="row_004",
        source_trace_id="trace_004",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_trace_summary="Trace summary",
        target_output_text="Explanation text",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
        residuals_about_dataset_generation=(),
    )

    # Convert to TrainingExample
    example = DatasetExporter.dataset_row_to_training_example(valid_row)

    # Verify NO constitutional facts created
    # TrainingExample is pure serialization artifact
    assert isinstance(example, TrainingExample)
    assert example.source_trace_id == valid_row.source_trace_id
    assert example.source_dataset_row_id == valid_row.dataset_row_id

    # Export to JSONL
    with TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_export.jsonl"
        result = DatasetExporter.export_to_jsonl((example,), output_path)

        assert result.success is True

        # Verify export is pure serialization
        with open(output_path, 'r', encoding='utf-8') as f:
            data = json.loads(f.readline())

            # No authority fields present
            assert 'upgraded_rank' not in data
            assert 'new_candidate' not in data
            assert 'closed_ifadah' not in data
            assert 'produced_hukm' not in data
            assert 'produced_reality' not in data


# ============================================================================
# Repair Example Validation Tests
# ============================================================================

def test_repair_example_requires_algorithm_rerun():
    """
    Test: Repair examples MUST have requires_algorithm_rerun=True.

    Constitutional Requirement:
        REPAIR_SUGGESTION examples MUST preserve requires_algorithm_rerun=True
        because T5 suggests repairs but does NOT execute repairs.
    """
    # Create REPAIR_SUGGESTION row with requires_algorithm_rerun=False (invalid)
    invalid_repair_row = DatasetRow(
        dataset_row_id="row_005",
        source_trace_id="trace_005",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.SUGGEST_REPAIR,
        input_trace_summary="Test summary with residuals",
        target_output_text="Suggestion: Re-run gate",
        referenced_candidate_ids=(),
        referenced_residual_ids=("res_001",),
        referenced_gate_ids=("gate_001",),
        referenced_rank_values=(),
        output_type=OutputType.REPAIR_SUGGESTION,
        requires_algorithm_rerun=False,  # INVALID for repair
        validation_status=ValidationStatus.VALID,
        residuals_about_dataset_generation=(),
    )

    # Attempt to convert should raise ValueError
    with pytest.raises(ValueError) as exc_info:
        DatasetExporter.dataset_row_to_training_example(invalid_repair_row)

    assert "Constitutional violation" in str(exc_info.value)
    assert "requires_algorithm_rerun" in str(exc_info.value)


def test_valid_dataset_row_to_training_example():
    """
    Test: Valid DatasetRow converts to TrainingExample successfully.

    Constitutional Requirement:
        VALID DatasetRows with proper source bindings MUST convert
        to TrainingExample without errors.
    """
    valid_row = DatasetRow(
        dataset_row_id="row_006",
        source_trace_id="trace_006",
        source_algorithm="morphology_analyzer",
        operation=TraceConsumerOperation.GENERATE_BOUNDED_EXPLANATION,
        input_trace_summary="Trace ID: trace_006, Algorithm: morphology_analyzer",
        target_output_text="This trace contains 2 candidates.",
        referenced_candidate_ids=("cand_001", "cand_002"),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=("PLAUSIBLE",),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
        residuals_about_dataset_generation=(),
    )

    # Convert should succeed
    example = DatasetExporter.dataset_row_to_training_example(valid_row)

    assert isinstance(example, TrainingExample)
    assert example.source_trace_id == "trace_006"
    assert example.source_dataset_row_id == "row_006"
    assert example.source_algorithm == "morphology_analyzer"
    assert example.validation_status == ValidationStatus.VALID
    assert len(example.referenced_candidate_ids) == 2


# ============================================================================
# Multiple Example Export Tests
# ============================================================================

def test_export_multiple_examples_with_mixed_validity():
    """
    Test: Export correctly handles multiple examples with mixed validity.

    Constitutional Requirement:
        Export MUST accept valid examples and reject invalid ones,
        providing accurate counts in result.
    """
    valid_example = TrainingExample(
        training_example_id="example_007",
        source_dataset_row_id="row_007",
        source_trace_id="trace_007",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Valid input",
        target_text="Valid explanation",
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    invalid_example = TrainingExample(
        training_example_id="example_008",
        source_dataset_row_id="row_008",
        source_trace_id="trace_008",
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Invalid input",
        target_text="This is the correct_analysis.",  # FORBIDDEN
        referenced_candidate_ids=(),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )

    with TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_export.jsonl"
        result = DatasetExporter.export_to_jsonl(
            (valid_example, invalid_example),
            output_path
        )

        # Only valid example should be exported
        assert result.exported_count == 1
        assert result.rejected_count == 1
        assert len(result.residuals) > 0

        # Verify JSONL contains only valid example
        if output_path.exists():
            with open(output_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                assert len(lines) == 1
                data = json.loads(lines[0])
                assert data['training_example_id'] == "example_007"
