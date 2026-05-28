"""
Constitutional Tests for Trace Explanation Dataset Generator

PR #145: Tests proving dataset generation respects constitutional boundaries.

Test Strategy:
    - Load golden fixtures
    - Generate dataset rows from valid fixtures
    - Reject invalid inputs
    - Prove constitutional boundaries are enforced

Constitutional Laws Under Test:
    1. Dataset rows derived ONLY from validated traces
    2. Dataset rows preserve source_trace_id binding
    3. Dataset generation rejects raw Arabic
    4. Dataset generation rejects invented references
    5. Dataset generation does NOT upgrade rank
    6. Dataset generation does NOT resolve residuals
    7. Dataset generation does NOT close ifādah/hukm/reality
    8. All generated rows pass GovernedTraceT5Contract validation

Test Categories:
    - test_generate_from_valid_explanation_*: Generate from valid explanation fixtures
    - test_generate_from_valid_repair_*: Generate from valid repair suggestion fixtures
    - test_reject_invalid_*: Reject invalid inputs
    - test_reject_raw_arabic_*: Reject raw Arabic text
    - test_constitutional_*: Constitutional boundary enforcement

Created: 2026-05-28
"""

import pytest
from tests.fixtures.golden_trace_explanation_fixtures import (
    create_valid_explanation_fixture,
    create_valid_repair_suggestion_fixture,
    create_invalid_invented_candidate_fixture,
    create_invalid_invented_residual_fixture,
    create_invalid_invented_gate_fixture,
)
from dal_core.trace_explanation_dataset_generator import (
    TraceExplanationDatasetGenerator,
    DatasetRow,
    OutputType,
    ValidationStatus,
)
from dal_core.governed_trace_t5_contract import (
    GovernedTraceT5Validator,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation


# ============================================================================
# Test 1: Valid Explanation Fixture → Dataset Row
# ============================================================================

def test_generate_from_valid_explanation_fixture():
    """
    Test 1: Valid explanation fixture becomes dataset row.

    Constitutional Requirement:
        Validated ExplanationCandidate + AlgorithmTracePayload → DatasetRow
    """
    fixture = create_valid_explanation_fixture()

    # Generate dataset row
    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.explanation,
    )

    # Verify dataset row structure
    assert isinstance(row, DatasetRow)
    assert row.dataset_row_id.startswith("dataset_row_")
    assert row.source_trace_id == fixture.trace.trace_id
    assert row.source_algorithm == fixture.trace.source_algorithm
    assert row.operation == TraceConsumerOperation.EXPLAIN_TRACE
    assert row.output_type == OutputType.EXPLANATION
    assert row.validation_status == ValidationStatus.VALID
    assert not row.requires_algorithm_rerun  # Explanation, not repair


def test_generate_from_valid_explanation_preserves_trace_id():
    """
    Test 10: Dataset row preserves source_trace_id.

    Constitutional Requirement:
        Dataset rows MUST preserve trace_id from source trace.
    """
    fixture = create_valid_explanation_fixture()

    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.explanation,
    )

    # Verify trace_id preservation
    assert row.source_trace_id == fixture.trace.trace_id
    assert row.source_trace_id == "trace_golden_001"


def test_generate_from_valid_explanation_includes_references():
    """
    Test that valid explanation dataset row includes all references.

    Constitutional Requirement:
        All references MUST come from source trace.
    """
    fixture = create_valid_explanation_fixture()

    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.explanation,
    )

    # Verify references are preserved
    assert len(row.referenced_candidate_ids) == 2
    assert "relation_cand_1" in row.referenced_candidate_ids
    assert "relation_cand_2" in row.referenced_candidate_ids

    # Verify residual references
    assert len(row.referenced_residual_ids) >= 1

    # Verify gate references
    assert len(row.referenced_gate_ids) >= 1


# ============================================================================
# Test 2: Valid Repair Suggestion Fixture → Dataset Row
# ============================================================================

def test_generate_from_valid_repair_suggestion_fixture():
    """
    Test 2: Valid repair suggestion fixture becomes dataset row.

    Constitutional Requirement:
        Validated RepairSuggestionCandidate + AlgorithmTracePayload → DatasetRow
    """
    fixture = create_valid_repair_suggestion_fixture()

    # Generate dataset row
    row = TraceExplanationDatasetGenerator.generate_from_repair_suggestion_candidate(
        trace=fixture.trace,
        repair=fixture.repair_suggestion,
    )

    # Verify dataset row structure
    assert isinstance(row, DatasetRow)
    assert row.dataset_row_id.startswith("dataset_row_")
    assert row.source_trace_id == fixture.trace.trace_id
    assert row.source_algorithm == fixture.trace.source_algorithm
    assert row.operation == TraceConsumerOperation.SUGGEST_REPAIR
    assert row.output_type == OutputType.REPAIR_SUGGESTION
    assert row.validation_status == ValidationStatus.VALID
    assert row.requires_algorithm_rerun  # MUST be True for repair suggestions


def test_generate_from_valid_repair_requires_algorithm_rerun():
    """
    Test 12: Repair suggestion dataset row requires_algorithm_rerun is True.

    Constitutional Requirement:
        Repair suggestion rows MUST require algorithm rerun.
        T5 suggests repairs; T5 does NOT execute repairs.
    """
    fixture = create_valid_repair_suggestion_fixture()

    row = TraceExplanationDatasetGenerator.generate_from_repair_suggestion_candidate(
        trace=fixture.trace,
        repair=fixture.repair_suggestion,
    )

    # Verify requires_algorithm_rerun is True
    assert row.requires_algorithm_rerun is True
    assert row.output_type == OutputType.REPAIR_SUGGESTION


# ============================================================================
# Test 3: Invalid Explanation Fixture is Rejected
# ============================================================================

def test_reject_invalid_explanation_with_invented_candidate():
    """
    Test 3 + 5: Invalid explanation fixture is rejected.

    Constitutional Requirement:
        Explanations with invented candidate IDs MUST be rejected.
    """
    fixture = create_invalid_invented_candidate_fixture()

    # Generate dataset row (should mark as REJECTED)
    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.invalid_explanation,
    )

    # Verify rejection
    assert row.validation_status == ValidationStatus.REJECTED_VALIDATION_FAILURE
    assert len(row.residuals_about_dataset_generation) > 0
    assert row.residuals_about_dataset_generation[0].issue_type == "validation_failure"


def test_reject_invalid_explanation_with_invented_residual():
    """
    Test 6: Invented residual references cannot become valid dataset row.

    Constitutional Requirement:
        Explanations with invented residual IDs MUST be rejected.
    """
    fixture = create_invalid_invented_residual_fixture()

    # Generate dataset row (should mark as REJECTED)
    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.invalid_explanation,
    )

    # Verify rejection
    assert row.validation_status == ValidationStatus.REJECTED_VALIDATION_FAILURE
    assert len(row.residuals_about_dataset_generation) > 0


def test_reject_invalid_explanation_with_invented_gate():
    """
    Test 7: Invented gate references cannot become valid dataset row.

    Constitutional Requirement:
        Explanations with invented gate IDs MUST be rejected.
    """
    fixture = create_invalid_invented_gate_fixture()

    # Generate dataset row (should mark as REJECTED)
    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.invalid_explanation,
    )

    # Verify rejection
    assert row.validation_status == ValidationStatus.REJECTED_VALIDATION_FAILURE
    assert len(row.residuals_about_dataset_generation) > 0


# ============================================================================
# Test 4: Raw Arabic Cannot Become Dataset Row
# ============================================================================

def test_reject_raw_arabic_input():
    """
    Test 4: Raw Arabic cannot become dataset row.

    Constitutional Requirement:
        Dataset rows MUST be derived from AlgorithmTracePayload only.
        Raw Arabic text is NOT a valid dataset input.
    """
    raw_arabic = "زَيْدٌ قَائِمٌ"

    # Attempt to generate from raw Arabic
    row = TraceExplanationDatasetGenerator.reject_raw_arabic(raw_arabic)

    # Verify rejection
    assert row.validation_status == ValidationStatus.REJECTED_RAW_ARABIC
    assert row.source_trace_id == "<no_trace>"
    assert row.source_algorithm == "<no_algorithm>"
    assert len(row.residuals_about_dataset_generation) == 1
    assert row.residuals_about_dataset_generation[0].issue_type == "raw_arabic_input"
    assert raw_arabic in row.residuals_about_dataset_generation[0].message


def test_raw_arabic_cannot_bypass_trace_requirement():
    """
    Test that there is no method to generate dataset row from raw Arabic.

    Constitutional Requirement:
        TraceExplanationDatasetGenerator MUST NOT have a method that accepts raw Arabic.
    """
    # Verify no such method exists
    generator = TraceExplanationDatasetGenerator()

    assert not hasattr(generator, "generate_from_raw_arabic")
    assert not hasattr(generator, "analyze_raw_arabic")
    assert not hasattr(generator, "create_from_text")


# ============================================================================
# Test 11: Dataset Row Has No Dangerous Authority Fields
# ============================================================================

def test_dataset_row_has_no_dangerous_fields():
    """
    Test 11: Dataset row does not contain constitutional authority fields.

    Constitutional Requirement:
        Dataset rows are teaching artifacts; they do NOT create constitutional facts.
    """
    fixture = create_valid_explanation_fixture()

    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.explanation,
    )

    # Verify no dangerous fields exist
    assert not hasattr(row, "new_candidate")
    assert not hasattr(row, "upgraded_rank")
    assert not hasattr(row, "resolved_residuals")
    assert not hasattr(row, "closed_ifadah")
    assert not hasattr(row, "hukm")
    assert not hasattr(row, "reality")
    assert not hasattr(row, "semantic_certainty")
    assert not hasattr(row, "final_answer")
    assert not hasattr(row, "correct_analysis")
    assert not hasattr(row, "gold_label_hukm")
    assert not hasattr(row, "resolved_output")


# ============================================================================
# Test 13: Repair Row Does Not Resolve Residuals
# ============================================================================

def test_repair_row_does_not_resolve_residuals():
    """
    Test 13: Repair row does not resolve residuals.

    Constitutional Requirement:
        Dataset rows reference residuals; they do NOT resolve residuals.
    """
    fixture = create_valid_repair_suggestion_fixture()

    row = TraceExplanationDatasetGenerator.generate_from_repair_suggestion_candidate(
        trace=fixture.trace,
        repair=fixture.repair_suggestion,
    )

    # Verify no residual resolution fields exist
    assert not hasattr(row, "resolved_residuals")
    assert not hasattr(row, "residual_discharge")
    assert not hasattr(row, "residual_resolution")

    # Verify requires_algorithm_rerun is True (repair not executed)
    assert row.requires_algorithm_rerun is True


# ============================================================================
# Test 14: Row Generation Validates Through GovernedTraceT5Contract
# ============================================================================

def test_generated_valid_explanation_row_passes_contract_validation():
    """
    Test 14: Generated rows pass GovernedTraceT5Contract validation before serialization.

    Constitutional Requirement:
        All valid dataset rows MUST pass GovernedTraceT5Contract validation.
    """
    fixture = create_valid_explanation_fixture()

    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.explanation,
    )

    # Verify validation status
    assert row.validation_status == ValidationStatus.VALID

    # Verify no generation residuals
    assert len(row.residuals_about_dataset_generation) == 0

    # Verify explanation candidate passes validation
    GovernedTraceT5Validator.validate_explanation(fixture.explanation)
    GovernedTraceT5Validator.validate_explanation_references(
        fixture.explanation, fixture.trace
    )


def test_generated_valid_repair_row_passes_contract_validation():
    """
    Test that valid repair suggestion dataset row passes contract validation.

    Constitutional Requirement:
        All valid repair suggestion rows MUST pass GovernedTraceT5Contract validation.
    """
    fixture = create_valid_repair_suggestion_fixture()

    row = TraceExplanationDatasetGenerator.generate_from_repair_suggestion_candidate(
        trace=fixture.trace,
        repair=fixture.repair_suggestion,
    )

    # Verify validation status
    assert row.validation_status == ValidationStatus.VALID

    # Verify no generation residuals
    assert len(row.residuals_about_dataset_generation) == 0

    # Verify repair suggestion candidate passes validation
    GovernedTraceT5Validator.validate_repair_suggestion(
        fixture.repair_suggestion
    )


# ============================================================================
# Test 15: Generated Rows Do Not Close Ifādah/Hukm/Reality
# ============================================================================

def test_dataset_row_does_not_close_ifadah_hukm_reality():
    """
    Test 15: Dataset row does not close ifādah/hukm/reality.

    Constitutional Requirement:
        Dataset rows are teaching artifacts; they do NOT close ifādah,
        produce hukm, or establish reality.
    """
    fixture = create_valid_explanation_fixture()

    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.explanation,
    )

    # Verify no ifādah/hukm/reality fields exist
    assert not hasattr(row, "close_ifadah")
    assert not hasattr(row, "closed_ifadah")
    assert not hasattr(row, "produce_hukm")
    assert not hasattr(row, "produced_hukm")
    assert not hasattr(row, "produce_reality")
    assert not hasattr(row, "produced_reality")
    assert not hasattr(row, "establish_reality")


# ============================================================================
# Test 16: All Dataclasses Are Frozen/Immutable
# ============================================================================

def test_constitutional_immutability():
    """
    Test 16: DatasetRow is immutable (frozen dataclass).

    Constitutional Requirement:
        Dataset rows are immutable teaching artifacts.
    """
    fixture = create_valid_explanation_fixture()

    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.explanation,
    )

    # Verify frozen (immutable)
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        row.source_trace_id = "modified"

    with pytest.raises(Exception):
        row.target_output_text = "modified"


def test_constitutional_trace_id_binding():
    """
    Test 9: Dataset rows bind to specific trace_id, not algorithm name.

    Constitutional Requirement:
        trace_id identifies execution instance.
        Dataset rows MUST bind to execution instances, NOT algorithm classes.
    """
    fixture = create_valid_explanation_fixture()

    row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=fixture.trace,
        explanation=fixture.explanation,
    )

    # Verify trace_id is specific instance ID, not algorithm name
    assert row.source_trace_id == fixture.trace.trace_id
    assert row.source_trace_id != row.source_algorithm
    assert row.source_trace_id.startswith("trace_")


def test_constitutional_output_type_classification():
    """
    Test that output_type correctly classifies explanation vs repair.

    Constitutional Requirement:
        OutputType distinguishes explanation (teaching) from repair suggestion (rerun required).
    """
    explanation_fixture = create_valid_explanation_fixture()
    repair_fixture = create_valid_repair_suggestion_fixture()

    explanation_row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
        trace=explanation_fixture.trace,
        explanation=explanation_fixture.explanation,
    )

    repair_row = TraceExplanationDatasetGenerator.generate_from_repair_suggestion_candidate(
        trace=repair_fixture.trace,
        repair=repair_fixture.repair_suggestion,
    )

    # Verify output types
    assert explanation_row.output_type == OutputType.EXPLANATION
    assert repair_row.output_type == OutputType.REPAIR_SUGGESTION

    # Verify requires_algorithm_rerun distinction
    assert not explanation_row.requires_algorithm_rerun
    assert repair_row.requires_algorithm_rerun
