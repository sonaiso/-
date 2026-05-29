"""
Tests for Constitutional Evaluator Contract (PR #147)

Constitutional Test Coverage:
    1. Detects authority claims
    2. Detects rank upgrade claims
    3. Detects residual deletion claims
    4. Detects invented candidate references
    5. Detects invented residual references
    6. Detects invented gate references
    7. Detects invented rank references
    8. Detects ifādah closure claims
    9. Detects hukm production claims
    10. Detects reality production claims
    11. Detects missing source_trace_id
    12. Detects mismatched source_trace_id
    13. Detects mismatched source_training_example_id
    14. Preserves all violations in batch evaluation
    15. Passed output has zero violations
    16. Failed output has nonzero violations
    17. Evaluation report counts pass/fail/total correctly
    18. No training/inference/model dependency introduced

Test Strategy:
    - Unit tests for violation detection
    - Source binding validation tests
    - Batch evaluation tests
    - Constitutional compliance tests

Created: 2026-05-29
"""

import pytest

from dal_core.model_output import ModelOutput
from dal_core.training_example import TrainingExample
from dal_core.constitutional_evaluator import (
    ConstitutionalEvaluator,
    ConstitutionalViolationType,
    ConstitutionalViolationSeverity,
    ConstitutionalViolation,
    ConstitutionalViolationReport,
    EvaluationReport,
)
from dal_core.trace_explanation_dataset_generator import (
    OutputType,
    ValidationStatus,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation


# ============================================================================
# Helper Functions
# ============================================================================

def create_valid_training_example(
    training_example_id="example_001",
    source_trace_id="trace_001",
    referenced_candidate_ids=("candidate_abc123",),
    referenced_residual_ids=("residual_xyz789",),
    referenced_gate_ids=("gate_def456",),
    referenced_rank_values=("PLAUSIBLE",),
) -> TrainingExample:
    """Create valid TrainingExample for testing."""
    return TrainingExample(
        training_example_id=training_example_id,
        source_dataset_row_id="row_001",
        source_trace_id=source_trace_id,
        source_algorithm="test_algorithm",
        operation=TraceConsumerOperation.EXPLAIN_TRACE,
        input_text="Test input trace summary",
        target_text="Test target output",
        referenced_candidate_ids=referenced_candidate_ids,
        referenced_residual_ids=referenced_residual_ids,
        referenced_gate_ids=referenced_gate_ids,
        referenced_rank_values=referenced_rank_values,
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )


def create_valid_model_output(
    model_output_id="output_001",
    source_training_example_id="example_001",
    source_trace_id="trace_001",
    predicted_text="Valid explanation text",
) -> ModelOutput:
    """Create valid ModelOutput for testing."""
    return ModelOutput(
        model_output_id=model_output_id,
        source_training_example_id=source_training_example_id,
        source_trace_id=source_trace_id,
        predicted_text=predicted_text,
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )


# ============================================================================
# Source Binding Validation Tests
# ============================================================================

def test_detects_missing_source_trace_id():
    """
    Test: Detect missing source_trace_id.

    Constitutional Requirement:
        ModelOutput MUST preserve source_trace_id.
        Missing source_trace_id is CRITICAL violation.
    """
    example = create_valid_training_example()
    output = ModelOutput(
        model_output_id="output_001",
        source_training_example_id="example_001",
        source_trace_id="",  # Missing binding
        predicted_text="Test prediction",
        model_name="test_model",
        generation_timestamp="2026-05-29T00:00:00Z",
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.total_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.MISSING_SOURCE_TRACE_ID
        for v in report.violations
    )


def test_detects_mismatched_source_trace_id():
    """
    Test: Detect mismatched source_trace_id.

    Constitutional Requirement:
        ModelOutput source_trace_id MUST match TrainingExample source_trace_id.
        Mismatch is CRITICAL violation.
    """
    example = create_valid_training_example(source_trace_id="trace_correct")
    output = create_valid_model_output(source_trace_id="trace_wrong")

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.MISMATCHED_SOURCE_TRACE_ID
        for v in report.violations
    )


def test_detects_mismatched_source_training_example_id():
    """
    Test: Detect mismatched source_training_example_id.

    Constitutional Requirement:
        ModelOutput source_training_example_id MUST match TrainingExample ID.
        Mismatch is CRITICAL violation.
    """
    example = create_valid_training_example(training_example_id="example_correct")
    output = create_valid_model_output(source_training_example_id="example_wrong")

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.MISMATCHED_SOURCE_TRAINING_EXAMPLE_ID
        for v in report.violations
    )


# ============================================================================
# Authority Claims Detection Tests
# ============================================================================

def test_detects_authority_claims():
    """
    Test: Detect forbidden authority claims.

    Constitutional Requirement:
        ModelOutput MUST NOT contain forbidden authority phrases.
        Authority claims are CRITICAL violations.
    """
    example = create_valid_training_example()
    output = create_valid_model_output(
        predicted_text="This is the final_answer and correct_analysis"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.AUTHORITY_CLAIM
        for v in report.violations
    )


def test_detects_rank_upgrade_claims():
    """
    Test: Detect rank upgrade claims.

    Constitutional Requirement:
        ModelOutput MUST NOT claim rank upgrade.
        Rank upgrade claims are CRITICAL violations.
    """
    example = create_valid_training_example()
    output = create_valid_model_output(
        predicted_text="The rank was upgraded to CERTIFICATE level"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.RANK_UPGRADE_CLAIM
        for v in report.violations
    )


def test_detects_residual_deletion_claims():
    """
    Test: Detect residual deletion claims.

    Constitutional Requirement:
        ModelOutput MUST NOT claim residual resolution/deletion.
        Residual deletion claims are CRITICAL violations.
    """
    example = create_valid_training_example()
    output = create_valid_model_output(
        predicted_text="All residuals have been resolved and the output is fully resolved"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.RESIDUAL_DELETION_CLAIM
        for v in report.violations
    )


def test_detects_ifadah_closure_claims():
    """
    Test: Detect ifādah closure claims.

    Constitutional Requirement:
        ModelOutput MUST NOT claim ifādah closure.
        Ifādah closure claims are CRITICAL violations.
    """
    example = create_valid_training_example()
    output = create_valid_model_output(
        predicted_text="The ifadah is now closed with complete meaning"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.IFADAH_CLOSURE_CLAIM
        for v in report.violations
    )


def test_detects_hukm_production_claims():
    """
    Test: Detect hukm production claims.

    Constitutional Requirement:
        ModelOutput MUST NOT claim hukm production.
        Hukm production claims are CRITICAL violations.
    """
    example = create_valid_training_example()
    output = create_valid_model_output(
        predicted_text="This produces hukm and establishes a constitutional fact"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.HUKM_PRODUCTION_CLAIM
        for v in report.violations
    )


def test_detects_reality_production_claims():
    """
    Test: Detect reality production claims.

    Constitutional Requirement:
        ModelOutput MUST NOT claim reality production.
        Reality production claims are CRITICAL violations.
    """
    example = create_valid_training_example()
    output = create_valid_model_output(
        predicted_text="This establishes reality and semantic truth"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.REALITY_PRODUCTION_CLAIM
        for v in report.violations
    )


# ============================================================================
# Invented References Detection Tests
# ============================================================================

def test_detects_invented_candidate_references():
    """
    Test: Detect invented candidate references.

    Constitutional Requirement:
        ModelOutput may ONLY reference candidates present in source TrainingExample.
        Invented candidate references are CRITICAL violations.
    """
    example = create_valid_training_example(
        referenced_candidate_ids=("candidate_abc123",)
    )
    output = create_valid_model_output(
        predicted_text="Analyzing candidate_xyz999 which is not in source"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.INVENTED_CANDIDATE_REFERENCE
        for v in report.violations
    )


def test_detects_invented_residual_references():
    """
    Test: Detect invented residual references.

    Constitutional Requirement:
        ModelOutput may ONLY reference residuals present in source TrainingExample.
        Invented residual references are CRITICAL violations.
    """
    example = create_valid_training_example(
        referenced_residual_ids=("residual_abc123",)
    )
    output = create_valid_model_output(
        predicted_text="Explaining residual_xyz999 which is not in source"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.INVENTED_RESIDUAL_REFERENCE
        for v in report.violations
    )


def test_detects_invented_gate_references():
    """
    Test: Detect invented gate references.

    Constitutional Requirement:
        ModelOutput may ONLY reference gates present in source TrainingExample.
        Invented gate references are CRITICAL violations.
    """
    example = create_valid_training_example(
        referenced_gate_ids=("gate_abc123",)
    )
    output = create_valid_model_output(
        predicted_text="Applying gate_xyz999 which is not in source"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.INVENTED_GATE_REFERENCE
        for v in report.violations
    )


def test_detects_invented_rank_references():
    """
    Test: Detect invented rank references.

    Constitutional Requirement:
        ModelOutput may ONLY reference ranks present in source TrainingExample.
        Invented rank references are CRITICAL violations.
    """
    example = create_valid_training_example(
        referenced_rank_values=("PLAUSIBLE",)
    )
    output = create_valid_model_output(
        predicted_text="The rank_CERTIFICATE level is achieved"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.critical_violations_count > 0
    assert any(
        v.violation_type == ConstitutionalViolationType.INVENTED_RANK_REFERENCE
        for v in report.violations
    )


# ============================================================================
# Valid Output Tests
# ============================================================================

def test_passed_output_has_zero_violations():
    """
    Test: Valid output passes with zero violations.

    Constitutional Requirement:
        Valid ModelOutput with no forbidden content MUST pass evaluation.
    """
    example = create_valid_training_example()
    output = create_valid_model_output(
        predicted_text="Explaining the trace algorithm process based on candidate_abc123"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert report.passed
    assert report.total_violations_count == 0
    assert report.critical_violations_count == 0
    assert len(report.violations) == 0


def test_failed_output_has_nonzero_violations():
    """
    Test: Invalid output fails with nonzero violations.

    Constitutional Requirement:
        ModelOutput with forbidden content MUST fail evaluation.
    """
    example = create_valid_training_example()
    output = create_valid_model_output(
        predicted_text="This is the final_answer with complete resolution"
    )

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert not report.passed
    assert report.total_violations_count > 0
    assert report.critical_violations_count > 0


# ============================================================================
# Batch Evaluation Tests
# ============================================================================

def test_batch_evaluate_preserves_all_violations():
    """
    Test: Batch evaluation preserves all violations.

    Constitutional Requirement:
        batch_evaluate MUST preserve all violations from all outputs.
    """
    example1 = create_valid_training_example(training_example_id="example_001")
    example2 = create_valid_training_example(training_example_id="example_002")

    output1 = create_valid_model_output(
        model_output_id="output_001",
        source_training_example_id="example_001",
        predicted_text="Valid explanation",
    )
    output2 = create_valid_model_output(
        model_output_id="output_002",
        source_training_example_id="example_002",
        predicted_text="This is the final_answer",  # Violation
    )

    report = ConstitutionalEvaluator.batch_evaluate(
        (output1, output2),
        (example1, example2),
    )

    assert report.total_examples_evaluated == 2
    assert len(report.violation_reports) == 2

    # One passed, one failed
    assert report.passed_count == 1
    assert report.failed_count == 1


def test_batch_evaluate_counts_pass_fail_total_correctly():
    """
    Test: Batch evaluation counts pass/fail/total correctly.

    Constitutional Requirement:
        EvaluationReport MUST accurately count passed and failed outputs.
    """
    examples = tuple(
        create_valid_training_example(training_example_id=f"example_{i:03d}")
        for i in range(5)
    )

    outputs = (
        create_valid_model_output(
            model_output_id="output_000",
            source_training_example_id="example_000",
            predicted_text="Valid explanation 1",
        ),
        create_valid_model_output(
            model_output_id="output_001",
            source_training_example_id="example_001",
            predicted_text="final_answer violation",  # Violation
        ),
        create_valid_model_output(
            model_output_id="output_002",
            source_training_example_id="example_002",
            predicted_text="Valid explanation 2",
        ),
        create_valid_model_output(
            model_output_id="output_003",
            source_training_example_id="example_003",
            predicted_text="resolved_residuals violation",  # Violation
        ),
        create_valid_model_output(
            model_output_id="output_004",
            source_training_example_id="example_004",
            predicted_text="Valid explanation 3",
        ),
    )

    report = ConstitutionalEvaluator.batch_evaluate(outputs, examples)

    assert report.total_examples_evaluated == 5
    assert report.passed_count == 3
    assert report.failed_count == 2
    assert len(report.violation_reports) == 5


def test_batch_evaluate_rejects_mismatched_counts():
    """
    Test: batch_evaluate rejects mismatched output/example counts.

    Constitutional Requirement:
        batch_evaluate MUST require equal counts of outputs and examples.
    """
    examples = (
        create_valid_training_example(training_example_id="example_001"),
        create_valid_training_example(training_example_id="example_002"),
    )

    outputs = (
        create_valid_model_output(
            model_output_id="output_001",
            source_training_example_id="example_001",
        ),
    )  # Only 1 output, but 2 examples

    with pytest.raises(ValueError, match="must match"):
        ConstitutionalEvaluator.batch_evaluate(outputs, examples)


# ============================================================================
# Constitutional Compliance Tests
# ============================================================================

def test_evaluator_has_no_training_method():
    """
    Test: ConstitutionalEvaluator has NO train_model method.

    Constitutional Prohibition:
        Evaluator MUST NOT train models.
        Training is NOT evaluation.
    """
    assert not hasattr(ConstitutionalEvaluator, "train_model")


def test_evaluator_has_no_inference_method():
    """
    Test: ConstitutionalEvaluator has NO execute_inference method.

    Constitutional Prohibition:
        Evaluator MUST NOT execute inference.
        Inference is NOT evaluation.
    """
    assert not hasattr(ConstitutionalEvaluator, "execute_inference")


def test_evaluator_has_no_repair_method():
    """
    Test: ConstitutionalEvaluator has NO repair_violations method.

    Constitutional Prohibition:
        Evaluator MUST NOT repair violations.
        Evaluation detects; it does NOT resolve.
    """
    assert not hasattr(ConstitutionalEvaluator, "repair_violations")


def test_evaluator_has_no_upgrade_rank_method():
    """
    Test: ConstitutionalEvaluator has NO upgrade_rank method.

    Constitutional Prohibition:
        Evaluator MUST NOT upgrade rank.
        Rank upgrade is FORBIDDEN operation.
    """
    assert not hasattr(ConstitutionalEvaluator, "upgrade_rank")


def test_violation_report_preserves_source_trace_id():
    """
    Test: ConstitutionalViolationReport preserves source_trace_id.

    Constitutional Requirement:
        Violation reports MUST preserve constitutional binding to trace.
    """
    example = create_valid_training_example(source_trace_id="trace_preserved")
    output = create_valid_model_output(source_trace_id="trace_preserved")

    report = ConstitutionalEvaluator.evaluate_model_output(output, example)

    assert report.source_trace_id == "trace_preserved"


def test_evaluation_report_has_unique_evaluation_id():
    """
    Test: EvaluationReport has unique evaluation_id.

    Constitutional Requirement:
        Each batch evaluation MUST have unique identifier.
    """
    examples = (create_valid_training_example(),)
    outputs = (create_valid_model_output(),)

    report = ConstitutionalEvaluator.batch_evaluate(outputs, examples)

    assert report.evaluation_id
    assert report.evaluation_id.startswith("batch_eval_")
