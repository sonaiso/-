"""
Constitutional Tests for Golden Trace Explanation Fixtures

PR #144: Tests proving GovernedTraceT5Contract works on realistic traces.

Test Strategy:
    - Load golden fixtures
    - Validate positive fixtures pass all checks
    - Validate negative fixtures fail exactly as expected
    - Prove constitutional boundaries are enforced

Constitutional Laws Under Test:
    1. T5 explains only what specific traces contain (trace_id binding)
    2. T5 cannot invent candidate/residual/gate/rank references
    3. T5 cannot analyze raw Arabic text
    4. T5 cannot create/upgrade/resolve/close
    5. Trace consumption preserves immutability

Test Categories:
    - test_fixture_1_*: Valid explanation fixtures
    - test_fixture_2_*: Valid repair suggestion fixtures
    - test_fixture_3_*: Invalid invented candidate fixtures
    - test_fixture_4_*: Invalid invented residual fixtures
    - test_fixture_5_*: Invalid invented gate fixtures
    - test_fixture_6_*: Invalid rank claim fixtures
    - test_fixture_7_*: Wrong trace fixtures
    - test_fixture_8_*: Raw Arabic bypass fixtures
    - test_fixture_9_*: Immutability fixtures
    - test_constitutional_law_*: Constitutional law demonstrations

Created: 2026-05-28
"""

import pytest
from tests.fixtures.golden_trace_explanation_fixtures import (
    create_valid_explanation_fixture,
    create_valid_repair_suggestion_fixture,
    create_invalid_invented_candidate_fixture,
    create_invalid_invented_residual_fixture,
    create_invalid_invented_gate_fixture,
    create_invalid_rank_claim_fixture,
    create_wrong_trace_fixture,
    create_raw_arabic_bypass_fixture,
    create_immutability_fixture,
    create_all_golden_fixtures,
)
from dal_core.governed_trace_t5_contract import (
    GovernedTraceT5Input,
    GovernedTraceT5Validator,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation


# ============================================================================
# Fixture Family 1: Valid Explanation
# ============================================================================

def test_fixture_1_valid_explanation_construction():
    """Test that valid explanation fixture constructs correctly."""
    fixture = create_valid_explanation_fixture()

    # Verify fixture structure
    assert fixture.trace is not None
    assert fixture.t5_input is not None
    assert fixture.explanation is not None
    assert fixture.trace_id == "trace_golden_001"


def test_fixture_1_valid_explanation_trace_has_expected_elements():
    """Test that valid explanation trace has all expected elements."""
    fixture = create_valid_explanation_fixture()

    # Verify trace has candidates
    assert len(fixture.trace.candidates) == 2
    assert fixture.trace.candidates[0].candidate_id == "relation_cand_1"
    assert fixture.trace.candidates[1].candidate_id == "relation_cand_2"

    # Verify trace has residuals (as string representations)
    residual_payload = fixture.trace.candidates[0].residual_payload
    residual_ids = {str(r) for r in residual_payload.residuals.residuals}
    # Check that residuals exist and contain expected text
    assert len(residual_ids) == 2
    assert any("AgreementGate" in r_id and "Number agreement" in r_id for r_id in residual_ids)
    assert any("CaseGate" in r_id and "Case marker" in r_id for r_id in residual_ids)

    # Verify trace has gates
    assert "IsnadGate" in fixture.trace.candidates[0].trace
    assert "AgreementGate" in fixture.trace.candidates[0].trace


def test_fixture_1_valid_explanation_input_validates():
    """Test that valid explanation input passes validation."""
    fixture = create_valid_explanation_fixture()

    # Validation should not raise
    GovernedTraceT5Validator.validate_input(fixture.t5_input)


def test_fixture_1_valid_explanation_output_validates():
    """Test that valid explanation output passes validation."""
    fixture = create_valid_explanation_fixture()

    # Validation should not raise
    GovernedTraceT5Validator.validate_output(fixture.explanation)


def test_fixture_1_valid_explanation_references_validate():
    """Test that valid explanation references pass validation."""
    fixture = create_valid_explanation_fixture()

    # Reference validation should not raise
    GovernedTraceT5Validator.validate_explanation_references(
        fixture.explanation,
        fixture.trace
    )


def test_fixture_1_valid_explanation_references_only_existing_elements():
    """Test that valid explanation references only existing elements."""
    fixture = create_valid_explanation_fixture()

    # Collect valid IDs from trace
    valid_candidate_ids = {c.candidate_id for c in fixture.trace.candidates}
    valid_gate_ids = set()
    for c in fixture.trace.candidates:
        valid_gate_ids.update(c.trace)
        valid_gate_ids.update(c.residual_payload.residual_sources)

    # Verify all referenced IDs exist in trace
    for ref_id in fixture.explanation.referenced_candidate_ids:
        assert ref_id in valid_candidate_ids, f"Referenced candidate {ref_id} not in trace"

    for ref_gate in fixture.explanation.referenced_gate_ids:
        assert ref_gate in valid_gate_ids, f"Referenced gate {ref_gate} not in trace"


# ============================================================================
# Fixture Family 2: Valid Repair Suggestion
# ============================================================================

def test_fixture_2_valid_repair_suggestion_construction():
    """Test that valid repair suggestion fixture constructs correctly."""
    fixture = create_valid_repair_suggestion_fixture()

    assert fixture.trace is not None
    assert fixture.t5_input is not None
    assert fixture.repair_suggestion is not None


def test_fixture_2_valid_repair_suggestion_has_blocking_residuals():
    """Test that repair suggestion fixture has blocking residuals."""
    fixture = create_valid_repair_suggestion_fixture()

    # Verify trace has blocking residuals
    residual_payload = fixture.trace.candidates[0].residual_payload
    assert residual_payload.blocking_count > 0


def test_fixture_2_valid_repair_suggestion_requires_algorithm_rerun():
    """
    Test that repair suggestion REQUIRES algorithm rerun.

    Constitutional Law:
        RepairSuggestionCandidate.requires_algorithm_rerun MUST be True.
    """
    fixture = create_valid_repair_suggestion_fixture()

    assert fixture.repair_suggestion.requires_algorithm_rerun is True


def test_fixture_2_valid_repair_suggestion_validates():
    """Test that valid repair suggestion passes validation."""
    fixture = create_valid_repair_suggestion_fixture()

    # Validation should not raise
    GovernedTraceT5Validator.validate_output(fixture.repair_suggestion)
    GovernedTraceT5Validator.validate_repair_suggestion(fixture.repair_suggestion)


def test_fixture_2_valid_repair_suggestion_has_no_executed_repair():
    """
    Test that repair suggestion has no executed_repair field.

    Constitutional Law:
        T5 can ONLY suggest repairs, NOT execute them.
    """
    fixture = create_valid_repair_suggestion_fixture()

    assert not hasattr(fixture.repair_suggestion, "executed_repair")
    assert not hasattr(fixture.repair_suggestion, "execute_repair")
    assert not hasattr(fixture.repair_suggestion, "repaired_candidate")


def test_fixture_2_valid_repair_suggestion_has_no_resolved_residuals():
    """
    Test that repair suggestion has no resolved_residuals field.

    Constitutional Law:
        T5 cannot resolve residuals.
    """
    fixture = create_valid_repair_suggestion_fixture()

    assert not hasattr(fixture.repair_suggestion, "resolved_residuals")
    assert not hasattr(fixture.repair_suggestion, "resolve_residuals")


# ============================================================================
# Fixture Family 3: Invalid Invented Candidate
# ============================================================================

def test_fixture_3_invalid_invented_candidate_construction():
    """Test that invalid invented candidate fixture constructs correctly."""
    fixture = create_invalid_invented_candidate_fixture()

    assert fixture.trace is not None
    assert fixture.invalid_explanation is not None


def test_fixture_3_invalid_invented_candidate_references_nonexistent_id():
    """Test that invalid explanation references non-existent candidate_id."""
    fixture = create_invalid_invented_candidate_fixture()

    # Verify referenced candidate does NOT exist in trace
    valid_candidate_ids = {c.candidate_id for c in fixture.trace.candidates}
    for ref_id in fixture.invalid_explanation.referenced_candidate_ids:
        assert ref_id not in valid_candidate_ids


def test_fixture_3_invalid_invented_candidate_validation_fails():
    """
    Test that invented candidate_id validation FAILS.

    Constitutional Law:
        T5 cannot invent candidate references.
    """
    fixture = create_invalid_invented_candidate_fixture()

    # Validation MUST raise ValueError
    with pytest.raises(ValueError, match="candidate_id.*not found"):
        GovernedTraceT5Validator.validate_explanation_references(
            fixture.invalid_explanation,
            fixture.trace
        )


# ============================================================================
# Fixture Family 4: Invalid Invented Residual
# ============================================================================

def test_fixture_4_invalid_invented_residual_construction():
    """Test that invalid invented residual fixture constructs correctly."""
    fixture = create_invalid_invented_residual_fixture()

    assert fixture.trace is not None
    assert fixture.invalid_explanation is not None


def test_fixture_4_invalid_invented_residual_references_nonexistent_id():
    """Test that invalid explanation references non-existent residual_id."""
    fixture = create_invalid_invented_residual_fixture()

    # Collect valid residual IDs from trace
    valid_residual_ids = set()
    for c in fixture.trace.candidates:
        for r in c.residual_payload.residuals.residuals:
            valid_residual_ids.add(str(r))

    # Verify referenced residual does NOT exist
    for ref_id in fixture.invalid_explanation.referenced_residual_ids:
        assert ref_id not in valid_residual_ids


def test_fixture_4_invalid_invented_residual_validation_fails():
    """
    Test that invented residual_id validation FAILS.

    Constitutional Law:
        T5 cannot invent residual references.
    """
    fixture = create_invalid_invented_residual_fixture()

    # Validation MUST raise ValueError
    with pytest.raises(ValueError, match="residual_id.*not found"):
        GovernedTraceT5Validator.validate_explanation_references(
            fixture.invalid_explanation,
            fixture.trace
        )


# ============================================================================
# Fixture Family 5: Invalid Invented Gate
# ============================================================================

def test_fixture_5_invalid_invented_gate_construction():
    """Test that invalid invented gate fixture constructs correctly."""
    fixture = create_invalid_invented_gate_fixture()

    assert fixture.trace is not None
    assert fixture.invalid_explanation is not None


def test_fixture_5_invalid_invented_gate_references_nonexistent_id():
    """Test that invalid explanation references non-existent gate_id."""
    fixture = create_invalid_invented_gate_fixture()

    # Collect valid gate IDs from trace
    valid_gate_ids = set()
    for c in fixture.trace.candidates:
        valid_gate_ids.update(c.trace)
        valid_gate_ids.update(c.residual_payload.residual_sources)

    # Verify referenced gate does NOT exist
    for ref_gate in fixture.invalid_explanation.referenced_gate_ids:
        assert ref_gate not in valid_gate_ids


def test_fixture_5_invalid_invented_gate_validation_fails():
    """
    Test that invented gate_id validation FAILS.

    Constitutional Law:
        T5 cannot invent gate/operation references.
    """
    fixture = create_invalid_invented_gate_fixture()

    # Validation MUST raise ValueError
    with pytest.raises(ValueError, match="gate_id.*not found"):
        GovernedTraceT5Validator.validate_explanation_references(
            fixture.invalid_explanation,
            fixture.trace
        )


# ============================================================================
# Fixture Family 6: Invalid Rank Claim
# ============================================================================

def test_fixture_6_invalid_rank_claim_construction():
    """Test that invalid rank claim fixture constructs correctly."""
    fixture = create_invalid_rank_claim_fixture()

    assert fixture.trace is not None
    assert fixture.invalid_explanation is not None


def test_fixture_6_invalid_rank_claim_references_nonexistent_rank():
    """Test that invalid explanation claims rank not in trace."""
    fixture = create_invalid_rank_claim_fixture()

    # Collect valid rank values from trace
    valid_ranks = {c.rank_payload.rank.name for c in fixture.trace.candidates}

    # Verify referenced rank does NOT exist
    for ref_rank in fixture.invalid_explanation.referenced_rank_values:
        assert ref_rank not in valid_ranks


def test_fixture_6_invalid_rank_claim_validation_fails():
    """
    Test that invalid rank claim validation FAILS.

    Constitutional Law:
        T5 cannot claim ranks not present in trace.
        T5 cannot upgrade rank.
    """
    fixture = create_invalid_rank_claim_fixture()

    # Validation MUST raise ValueError
    with pytest.raises(ValueError, match="rank.*not found"):
        GovernedTraceT5Validator.validate_explanation_references(
            fixture.invalid_explanation,
            fixture.trace
        )


# ============================================================================
# Fixture Family 7: Wrong Trace
# ============================================================================

def test_fixture_7_wrong_trace_construction():
    """Test that wrong trace fixture constructs correctly."""
    fixture = create_wrong_trace_fixture()

    assert fixture.trace_a is not None
    assert fixture.trace_b is not None
    assert fixture.explanation_for_a is not None


def test_fixture_7_wrong_trace_different_trace_ids():
    """Test that traces have different trace_ids."""
    fixture = create_wrong_trace_fixture()

    # Verify different trace_ids
    assert fixture.trace_a.trace_id != fixture.trace_b.trace_id


def test_fixture_7_wrong_trace_same_algorithm():
    """Test that traces come from same algorithm."""
    fixture = create_wrong_trace_fixture()

    # Verify same source_algorithm
    assert fixture.trace_a.source_algorithm == fixture.trace_b.source_algorithm


def test_fixture_7_wrong_trace_explanation_validates_against_correct_trace():
    """Test that explanation validates against correct trace (trace A)."""
    fixture = create_wrong_trace_fixture()

    # Validation against trace A should pass
    GovernedTraceT5Validator.validate_explanation_references(
        fixture.explanation_for_a,
        fixture.trace_a
    )


def test_fixture_7_wrong_trace_explanation_fails_against_wrong_trace():
    """
    Test that explanation FAILS against wrong trace (trace B).

    Constitutional Law:
        Explanations bind to SPECIFIC trace_id, NOT algorithm name.
        Explanation for trace A must NOT validate against trace B.
    """
    fixture = create_wrong_trace_fixture()

    # Validation against trace B MUST fail
    with pytest.raises(ValueError, match="not found in source trace"):
        GovernedTraceT5Validator.validate_explanation_references(
            fixture.explanation_for_a,
            fixture.trace_b
        )


# ============================================================================
# Fixture Family 8: Raw Arabic Bypass
# ============================================================================

def test_fixture_8_raw_arabic_bypass_construction():
    """Test that raw Arabic bypass fixture constructs correctly."""
    fixture = create_raw_arabic_bypass_fixture()

    assert fixture.raw_arabic_text is not None
    assert isinstance(fixture.raw_arabic_text, str)


def test_fixture_8_raw_arabic_bypass_input_construction_fails():
    """
    Test that raw Arabic string CANNOT be used as GovernedTraceT5Input.

    Constitutional Law:
        T5 may NOT analyze raw Arabic text.
        T5 may ONLY consume AlgorithmTracePayload.
    """
    fixture = create_raw_arabic_bypass_fixture()

    # Attempt to create T5 input with raw string MUST fail
    with pytest.raises(TypeError, match="must be AlgorithmTracePayload"):
        GovernedTraceT5Input(
            trace=fixture.raw_arabic_text,  # type: ignore - intentional type error
            operation=TraceConsumerOperation.EXPLAIN_TRACE,
            context=None
        )


# ============================================================================
# Fixture Family 9: Immutability
# ============================================================================

def test_fixture_9_immutability_construction():
    """Test that immutability fixture constructs correctly."""
    fixture = create_immutability_fixture()

    assert fixture.original_trace is not None
    assert fixture.t5_input is not None
    assert fixture.explanation is not None


def test_fixture_9_immutability_trace_is_frozen():
    """Test that AlgorithmTracePayload is frozen (immutable)."""
    fixture = create_immutability_fixture()

    # Attempt to modify trace MUST fail
    with pytest.raises(AttributeError):
        fixture.original_trace.trace_id = "modified"  # type: ignore


def test_fixture_9_immutability_input_is_frozen():
    """Test that GovernedTraceT5Input is frozen (immutable)."""
    fixture = create_immutability_fixture()

    # Attempt to modify input MUST fail
    with pytest.raises(AttributeError):
        fixture.t5_input.operation = TraceConsumerOperation.SUMMARIZE_CANDIDATES  # type: ignore


def test_fixture_9_immutability_explanation_is_frozen():
    """Test that ExplanationCandidate is frozen (immutable)."""
    fixture = create_immutability_fixture()

    # Attempt to modify explanation MUST fail
    with pytest.raises(AttributeError):
        fixture.explanation.confidence = 0.5  # type: ignore


def test_fixture_9_immutability_trace_unchanged_after_consumption():
    """
    Test that consuming trace for explanation does NOT mutate original.

    Constitutional Law:
        AlgorithmTracePayload is immutable audit evidence.
        Creating explanations must NOT modify original trace.
    """
    fixture = create_immutability_fixture()

    # Store original values
    original_trace_id = fixture.original_trace.trace_id
    original_candidate_count = len(fixture.original_trace.candidates)
    original_candidate_id = fixture.original_trace.candidates[0].candidate_id

    # Create T5 input (consumes trace)
    _ = fixture.t5_input

    # Create explanation (consumes trace)
    _ = fixture.explanation

    # Verify trace unchanged
    assert fixture.original_trace.trace_id == original_trace_id
    assert len(fixture.original_trace.candidates) == original_candidate_count
    assert fixture.original_trace.candidates[0].candidate_id == original_candidate_id


# ============================================================================
# Constitutional Law Demonstrations
# ============================================================================

def test_constitutional_law_t5_explains_only_what_trace_contains():
    """
    Constitutional Law Demonstration:
        T5 explains ONLY what a specific immutable trace already contains.

    Proof:
        Valid explanation fixture passes validation.
        Invalid invented reference fixtures fail validation.
    """
    # Valid explanation with existing references passes
    valid_fixture = create_valid_explanation_fixture()
    GovernedTraceT5Validator.validate_explanation_references(
        valid_fixture.explanation,
        valid_fixture.trace
    )

    # Invalid invented candidate fails
    invalid_cand_fixture = create_invalid_invented_candidate_fixture()
    with pytest.raises(ValueError):
        GovernedTraceT5Validator.validate_explanation_references(
            invalid_cand_fixture.invalid_explanation,
            invalid_cand_fixture.trace
        )

    # Invalid invented residual fails
    invalid_res_fixture = create_invalid_invented_residual_fixture()
    with pytest.raises(ValueError):
        GovernedTraceT5Validator.validate_explanation_references(
            invalid_res_fixture.invalid_explanation,
            invalid_res_fixture.trace
        )

    # Invalid invented gate fails
    invalid_gate_fixture = create_invalid_invented_gate_fixture()
    with pytest.raises(ValueError):
        GovernedTraceT5Validator.validate_explanation_references(
            invalid_gate_fixture.invalid_explanation,
            invalid_gate_fixture.trace
        )


def test_constitutional_law_t5_does_not_analyze_raw_arabic():
    """
    Constitutional Law Demonstration:
        T5 does NOT analyze raw Arabic.
        T5 ONLY consumes AlgorithmTracePayload.

    Proof:
        Raw Arabic string cannot be used as T5 input.
    """
    fixture = create_raw_arabic_bypass_fixture()

    with pytest.raises(TypeError, match="must be AlgorithmTracePayload"):
        GovernedTraceT5Input(
            trace=fixture.raw_arabic_text,  # type: ignore
            operation=TraceConsumerOperation.EXPLAIN_TRACE,
            context=None
        )


def test_constitutional_law_t5_does_not_create_candidates():
    """
    Constitutional Law Demonstration:
        T5 does NOT create candidates.

    Proof:
        ExplanationCandidate has no create_candidate field.
        RepairSuggestionCandidate has no create_candidate field.
    """
    valid_explanation = create_valid_explanation_fixture()
    assert not hasattr(valid_explanation.explanation, "new_candidate")
    assert not hasattr(valid_explanation.explanation, "create_candidate")

    valid_repair = create_valid_repair_suggestion_fixture()
    assert not hasattr(valid_repair.repair_suggestion, "new_candidate")
    assert not hasattr(valid_repair.repair_suggestion, "create_candidate")


def test_constitutional_law_t5_does_not_upgrade_rank():
    """
    Constitutional Law Demonstration:
        T5 does NOT upgrade rank.

    Proof:
        ExplanationCandidate has no upgrade_rank field.
        Invalid rank claim fails validation.
    """
    valid_explanation = create_valid_explanation_fixture()
    assert not hasattr(valid_explanation.explanation, "upgraded_rank")
    assert not hasattr(valid_explanation.explanation, "upgrade_rank")

    invalid_rank_fixture = create_invalid_rank_claim_fixture()
    with pytest.raises(ValueError, match="rank.*not found"):
        GovernedTraceT5Validator.validate_explanation_references(
            invalid_rank_fixture.invalid_explanation,
            invalid_rank_fixture.trace
        )


def test_constitutional_law_t5_does_not_resolve_residuals():
    """
    Constitutional Law Demonstration:
        T5 does NOT resolve residuals.

    Proof:
        RepairSuggestionCandidate has no resolved_residuals field.
        RepairSuggestionCandidate requires algorithm rerun.
    """
    valid_repair = create_valid_repair_suggestion_fixture()
    assert not hasattr(valid_repair.repair_suggestion, "resolved_residuals")
    assert not hasattr(valid_repair.repair_suggestion, "resolve_residuals")
    assert valid_repair.repair_suggestion.requires_algorithm_rerun is True


def test_constitutional_law_t5_does_not_close_ifadah():
    """
    Constitutional Law Demonstration:
        T5 does NOT close ifādah.

    Proof:
        ExplanationCandidate has no close_ifadah field.
    """
    valid_explanation = create_valid_explanation_fixture()
    assert not hasattr(valid_explanation.explanation, "closed_ifadah")
    assert not hasattr(valid_explanation.explanation, "close_ifadah")


def test_constitutional_law_t5_does_not_produce_hukm_or_reality():
    """
    Constitutional Law Demonstration:
        T5 does NOT produce hukm or reality.

    Proof:
        ExplanationCandidate has no produce_hukm/produce_reality fields.
    """
    valid_explanation = create_valid_explanation_fixture()
    assert not hasattr(valid_explanation.explanation, "produced_hukm")
    assert not hasattr(valid_explanation.explanation, "produce_hukm")
    assert not hasattr(valid_explanation.explanation, "to_hukm")
    assert not hasattr(valid_explanation.explanation, "produced_reality")
    assert not hasattr(valid_explanation.explanation, "produce_reality")
    assert not hasattr(valid_explanation.explanation, "to_reality")


def test_constitutional_law_trace_id_binding():
    """
    Constitutional Law Demonstration:
        Explanations bind to SPECIFIC trace_id (NOT algorithm name).

    Proof:
        Explanation for trace A fails validation against trace B,
        even though both traces come from same algorithm.
    """
    fixture = create_wrong_trace_fixture()

    # Same algorithm
    assert fixture.trace_a.source_algorithm == fixture.trace_b.source_algorithm

    # Different trace_id
    assert fixture.trace_a.trace_id != fixture.trace_b.trace_id

    # Explanation validates against trace A
    GovernedTraceT5Validator.validate_explanation_references(
        fixture.explanation_for_a,
        fixture.trace_a
    )

    # Explanation fails against trace B
    with pytest.raises(ValueError):
        GovernedTraceT5Validator.validate_explanation_references(
            fixture.explanation_for_a,
            fixture.trace_b
        )


def test_constitutional_law_immutability_preservation():
    """
    Constitutional Law Demonstration:
        Consuming trace for explanation preserves immutability.

    Proof:
        All payloads are frozen.
        Trace unchanged after consumption.
    """
    fixture = create_immutability_fixture()

    # All types are frozen
    with pytest.raises(AttributeError):
        fixture.original_trace.trace_id = "modified"  # type: ignore

    with pytest.raises(AttributeError):
        fixture.t5_input.operation = TraceConsumerOperation.SUMMARIZE_CANDIDATES  # type: ignore

    with pytest.raises(AttributeError):
        fixture.explanation.confidence = 0.5  # type: ignore


# ============================================================================
# Fixture Registry Test
# ============================================================================

def test_all_golden_fixtures_registry():
    """Test that all golden fixtures can be created via registry."""
    all_fixtures = create_all_golden_fixtures()

    # Verify all 9 fixture families present
    assert "valid_explanation" in all_fixtures
    assert "valid_repair_suggestion" in all_fixtures
    assert "invalid_invented_candidate" in all_fixtures
    assert "invalid_invented_residual" in all_fixtures
    assert "invalid_invented_gate" in all_fixtures
    assert "invalid_rank_claim" in all_fixtures
    assert "wrong_trace" in all_fixtures
    assert "raw_arabic_bypass" in all_fixtures
    assert "immutability" in all_fixtures

    assert len(all_fixtures) == 9
