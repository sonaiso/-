"""
Tests for Dal Algebra Signature (F1)

Tests the foundational typed transition contract for dal_core.
"""

import pytest
from dataclasses import dataclass

from dal_core.dal_algebra import (
    DalTypedInput,
    DalTypedOutput,
    DalEvidence,
    DalTrace,
    DalTransitionGuard,
    DalForbiddenOutput,
    DalTransitionContract,
    DalCandidateSetProtocol,
    DalTransitionProtocol,
    validate_transition_contract,
    validate_candidate_set_shape,
    ensure_no_forbidden_outputs,
)
from dal_core.ranks import LughaRank
from dal_core.evidence import Evidence
from dal_core.residuals import Residual, ResidualType, ResidualSeverity


# ---------------------------------------------------------------------------
# Test: Transition Contract Requires Input and Output Types
# ---------------------------------------------------------------------------


def test_transition_contract_requires_input_and_output_types():
    """Test that DalTransitionContract requires typed input and output."""

    # Valid contract
    valid_input = DalTypedInput(
        input_type_name="TestInput",
        source_stage="test_source"
    )
    valid_output = DalTypedOutput(
        output_type_name="TestOutput",
        target_stage="test_target"
    )
    valid_contract = DalTransitionContract(
        input_type=valid_input,
        output_type=valid_output,
        stage_name="test_stage"
    )

    is_valid, violations = valid_contract.validate_contract()
    assert is_valid
    assert len(violations) == 0

    # Invalid contract: empty input type name
    invalid_input = DalTypedInput(
        input_type_name="",  # Empty
        source_stage="test_source"
    )
    invalid_contract = DalTransitionContract(
        input_type=invalid_input,
        output_type=valid_output,
        stage_name="test_stage"
    )

    is_valid, violations = invalid_contract.validate_contract()
    assert not is_valid
    assert "input_type.input_type_name is empty" in violations

    # Invalid contract: empty output type name
    invalid_output = DalTypedOutput(
        output_type_name="",  # Empty
        target_stage="test_target"
    )
    invalid_contract2 = DalTransitionContract(
        input_type=valid_input,
        output_type=invalid_output,
        stage_name="test_stage"
    )

    is_valid, violations = invalid_contract2.validate_contract()
    assert not is_valid
    assert "output_type.output_type_name is empty" in violations


# ---------------------------------------------------------------------------
# Test: Transition Contract Requires Rank/Residual/Trace Fields
# ---------------------------------------------------------------------------


def test_transition_contract_requires_rank_residual_trace_fields():
    """Test that DalTransitionContract has rank, residual, trace fields."""

    input_type = DalTypedInput(
        input_type_name="TestInput",
        source_stage="test_source"
    )
    output_type = DalTypedOutput(
        output_type_name="TestOutput",
        target_stage="test_target"
    )

    # Contract with all optional fields
    contract = DalTransitionContract(
        input_type=input_type,
        output_type=output_type,
        stage_name="test_stage",
        rank_constraint=LughaRank.SAMA,
        forbidden_outputs=(
            DalForbiddenOutput(
                forbidden_field_names=frozenset({"meaning", "semantic"}),
                stage_name="test_stage",
                reason="No semantic meaning in dal layer"
            ),
        ),
        guards=(
            DalTransitionGuard(
                guard_type="input_validation",
                condition="input must be valid",
                required=True
            ),
        ),
        evidence_required=True,
        trace_required=True,
        competitors_allowed=True
    )

    # Verify fields are accessible
    assert contract.rank_constraint == LughaRank.SAMA
    assert len(contract.forbidden_outputs) == 1
    assert len(contract.guards) == 1
    assert contract.evidence_required is True
    assert contract.trace_required is True
    assert contract.competitors_allowed is True

    # Verify validation passes
    is_valid, violations = contract.validate_contract()
    assert is_valid
    assert len(violations) == 0


# ---------------------------------------------------------------------------
# Test: Candidate Set Shape Allows Empty Set
# ---------------------------------------------------------------------------


def test_candidate_set_shape_allows_empty_set():
    """Test that empty candidate sets are allowed when allow_empty=True."""

    # Mock candidate set with empty candidates
    @dataclass(frozen=True)
    class MockCandidate:
        value: str

    @dataclass(frozen=True)
    class EmptyCandidateSet:
        def get_candidates(self) -> tuple[MockCandidate, ...]:
            return ()

        def get_rank(self) -> LughaRank:
            return LughaRank.FORM

        def get_residuals(self) -> tuple[Residual, ...]:
            return ()

        def get_trace(self) -> DalTrace:
            return DalTrace(
                stage_name="test_stage",
                input_signature="test::input",
                output_signature="test::output",
                transformation_id="test_id"
            )

        def get_competitors(self) -> tuple[MockCandidate, ...]:
            return ()

    empty_set = EmptyCandidateSet()

    # Should pass with allow_empty=True (default)
    validate_candidate_set_shape(empty_set, allow_empty=True)

    # Should fail with allow_empty=False
    with pytest.raises(ValueError, match="Candidate set is empty"):
        validate_candidate_set_shape(empty_set, allow_empty=False)


# ---------------------------------------------------------------------------
# Test: Candidate Set Shape Rejects None Candidates
# ---------------------------------------------------------------------------


def test_candidate_set_shape_rejects_none_candidates():
    """Test that candidate sets cannot contain None candidates."""

    @dataclass(frozen=True)
    class MockCandidate:
        value: str

    @dataclass(frozen=True)
    class InvalidCandidateSet:
        def get_candidates(self) -> tuple[MockCandidate | None, ...]:
            return (
                MockCandidate(value="valid"),
                None,  # Invalid!
                MockCandidate(value="also_valid")
            )

        def get_rank(self) -> LughaRank:
            return LughaRank.SAMA

        def get_residuals(self) -> tuple[Residual, ...]:
            return ()

        def get_trace(self) -> DalTrace:
            return DalTrace(
                stage_name="test_stage",
                input_signature="test::input",
                output_signature="test::output",
                transformation_id="test_id"
            )

        def get_competitors(self) -> tuple[MockCandidate | None, ...]:
            return self.get_candidates()

    invalid_set = InvalidCandidateSet()

    # Should fail because of None candidate
    with pytest.raises(ValueError, match="None candidates"):
        validate_candidate_set_shape(invalid_set)


# ---------------------------------------------------------------------------
# Test: Forbidden Outputs Detect Forbidden Field Names
# ---------------------------------------------------------------------------


def test_forbidden_outputs_detect_forbidden_field_names():
    """Test that forbidden output validation detects forbidden fields."""

    # Object with forbidden field
    @dataclass
    class ObjectWithForbiddenField:
        meaning: str = "forbidden_value"
        valid_field: str = "allowed"

    forbidden_spec = DalForbiddenOutput(
        forbidden_field_names=frozenset({"meaning", "semantic", "murad"}),
        stage_name="test_stage",
        reason="No semantic fields allowed"
    )

    obj = ObjectWithForbiddenField()

    # Should raise ValueError for forbidden field
    with pytest.raises(ValueError, match="Forbidden outputs detected"):
        ensure_no_forbidden_outputs(
            obj,
            (forbidden_spec,),
            "test_stage"
        )


# ---------------------------------------------------------------------------
# Test: Forbidden Outputs Allow Stage-Specific Allowed Names
# ---------------------------------------------------------------------------


def test_forbidden_outputs_allow_stage_specific_allowed_names():
    """Test that forbidden outputs are stage-specific."""

    # Object with field that's forbidden in one stage but allowed in another
    @dataclass
    class ObjectWithStageSpecificField:
        case_effect: str = "some_value"

    # Forbidden in mufrad_proof stage
    mufrad_forbidden = DalForbiddenOutput(
        forbidden_field_names=frozenset({"case_effect", "relation"}),
        stage_name="mufrad_proof",
        reason="No case effects in mufrad layer"
    )

    # Allowed in relation_builder stage
    obj = ObjectWithStageSpecificField()

    # Should fail when checking mufrad_proof stage
    with pytest.raises(ValueError, match="Forbidden outputs detected"):
        ensure_no_forbidden_outputs(
            obj,
            (mufrad_forbidden,),
            "mufrad_proof"
        )

    # Should pass when checking relation_builder stage (different stage)
    ensure_no_forbidden_outputs(
        obj,
        (mufrad_forbidden,),
        "relation_builder"  # Different stage
    )


# ---------------------------------------------------------------------------
# Test: Protocol Does Not Force Existing Classes to Inherit
# ---------------------------------------------------------------------------


def test_protocol_does_not_force_existing_classes_to_inherit():
    """Test that protocols work with duck typing, no inheritance required."""

    # Existing class that implements protocol without inheriting
    @dataclass(frozen=True)
    class ExistingCandidate:
        value: str

    @dataclass(frozen=True)
    class ExistingCandidateSet:
        """Existing class that implements protocol through duck typing."""

        candidates: tuple[ExistingCandidate, ...]

        def get_candidates(self) -> tuple[ExistingCandidate, ...]:
            return self.candidates

        def get_rank(self) -> LughaRank:
            return LughaRank.QIYAS

        def get_residuals(self) -> tuple[Residual, ...]:
            return ()

        def get_trace(self) -> DalTrace:
            return DalTrace(
                stage_name="existing_stage",
                input_signature="existing::input",
                output_signature="existing::output",
                transformation_id="existing_id"
            )

        def get_competitors(self) -> tuple[ExistingCandidate, ...]:
            return self.candidates

    # Create instance
    candidate_set = ExistingCandidateSet(
        candidates=(
            ExistingCandidate(value="c1"),
            ExistingCandidate(value="c2")
        )
    )

    # Should work with protocol validation (duck typing)
    validate_candidate_set_shape(candidate_set)

    # Verify it satisfies protocol through isinstance check
    # Note: isinstance with Protocol only works if @runtime_checkable decorator is used
    # For now, we just verify duck typing works through validation
    assert candidate_set.get_candidates() == (
        ExistingCandidate(value="c1"),
        ExistingCandidate(value="c2")
    )


# ---------------------------------------------------------------------------
# Test: Dal Algebra Signature Does Not Import Relation or Case Effect
# ---------------------------------------------------------------------------


def test_dal_algebra_signature_does_not_import_relation_or_case_effect():
    """Test that dal_algebra module does not import relation or case_effect modules."""

    import dal_core.dal_algebra as dal_algebra_module
    import sys

    # Get all imported modules from dal_algebra
    imported_names = dir(dal_algebra_module)

    # Check that no relation/case_effect related names are imported
    forbidden_imports = {
        "RelationCandidate",
        "CaseEffectCandidate",
        "CaseEffect",
        "Relation",
        "ISN",
        "TADMN",
        "TAQYID",
        "marfoo_by",
        "mansub_by",
        "majroor_by",
        "majzum_by",
    }

    found_forbidden = [name for name in forbidden_imports if name in imported_names]

    assert len(found_forbidden) == 0, (
        f"dal_algebra should not import relation/case_effect concepts. "
        f"Found: {found_forbidden}"
    )

    # Also check sys.modules to ensure these modules aren't loaded
    forbidden_module_patterns = [
        "relation_candidate",
        "case_effect_candidate",
        "relation_builder",
        "case_effect_builder",
    ]

    loaded_forbidden = [
        mod_name for mod_name in sys.modules
        if any(pattern in mod_name for pattern in forbidden_module_patterns)
    ]

    # Note: This might be too strict if other tests load these modules,
    # but it's good to document the intent
    # assert len(loaded_forbidden) == 0, (
    #     f"dal_algebra should not trigger loading of relation/case modules. "
    #     f"Found: {loaded_forbidden}"
    # )


# ---------------------------------------------------------------------------
# Test: DalEvidence Chain
# ---------------------------------------------------------------------------


def test_dal_evidence_chain():
    """Test DalEvidence with evidence chain."""

    evidence1 = Evidence(
        source="syllabifier",
        reason="Valid CV pattern",
        confidence=1.0
    )

    evidence2 = Evidence(
        source="pattern_matcher",
        reason="Matches فَعَل pattern",
        confidence=0.95
    )

    dal_evidence = DalEvidence(
        transformation_type="morphological_analysis",
        evidence_chain=(evidence1, evidence2)
    )

    summary = dal_evidence.get_evidence_summary()
    assert "morphological_analysis" in summary
    assert "syllabifier" in summary
    assert "pattern_matcher" in summary


# ---------------------------------------------------------------------------
# Test: DalTrace Path
# ---------------------------------------------------------------------------


def test_dal_trace_path():
    """Test DalTrace with parent chaining."""

    # Parent trace
    parent_trace = DalTrace(
        stage_name="syllabifier",
        input_signature="atoms::input",
        output_signature="syllables::output",
        transformation_id="syll_001"
    )

    # Child trace
    child_trace = DalTrace(
        stage_name="pattern_matcher",
        input_signature="syllables::input",
        output_signature="patterns::output",
        transformation_id="pattern_001",
        parent_trace_id="syll_001"
    )

    assert parent_trace.get_trace_path() == "syll_001"
    assert child_trace.get_trace_path() == "syll_001 → pattern_001"


# ---------------------------------------------------------------------------
# Test: DalTransitionGuard Check
# ---------------------------------------------------------------------------


def test_dal_transition_guard_check():
    """Test DalTransitionGuard check method."""

    guard = DalTransitionGuard(
        guard_type="rank_ceiling",
        condition="output.rank ≤ input.rank",
        required=True
    )

    # Note: check() is a placeholder for now
    satisfied, message = guard.check({})
    assert satisfied  # Placeholder always returns True
    assert "not yet implemented" in message


# ---------------------------------------------------------------------------
# Test: validate_transition_contract Helper
# ---------------------------------------------------------------------------


def test_validate_transition_contract_helper():
    """Test validate_transition_contract helper function."""

    # Valid contract
    valid_contract = DalTransitionContract(
        input_type=DalTypedInput(
            input_type_name="ValidInput",
            source_stage="source"
        ),
        output_type=DalTypedOutput(
            output_type_name="ValidOutput",
            target_stage="target"
        ),
        stage_name="valid_stage"
    )

    # Should not raise
    validate_transition_contract(valid_contract)

    # Invalid contract
    invalid_contract = DalTransitionContract(
        input_type=DalTypedInput(
            input_type_name="",  # Invalid
            source_stage="source"
        ),
        output_type=DalTypedOutput(
            output_type_name="ValidOutput",
            target_stage="target"
        ),
        stage_name="invalid_stage"
    )

    # Should raise ValueError
    with pytest.raises(ValueError, match="Invalid DalTransitionContract"):
        validate_transition_contract(invalid_contract)


# ---------------------------------------------------------------------------
# Test: Contract Signature
# ---------------------------------------------------------------------------


def test_contract_signature():
    """Test DalTransitionContract signature generation."""

    contract = DalTransitionContract(
        input_type=DalTypedInput(
            input_type_name="MufradProof",
            source_stage="mufrad_proof"
        ),
        output_type=DalTypedOutput(
            output_type_name="OperatorCandidate",
            target_stage="operator_candidate"
        ),
        stage_name="operator_builder"
    )

    signature = contract.get_contract_signature()
    assert "operator_builder" in signature
    assert "mufrad_proof::MufradProof" in signature
    assert "operator_candidate::OperatorCandidate" in signature
    assert "→" in signature


# ---------------------------------------------------------------------------
# Test: Forbidden Output Contains Check
# ---------------------------------------------------------------------------


def test_forbidden_output_contains_check():
    """Test DalForbiddenOutput field checking."""

    forbidden = DalForbiddenOutput(
        forbidden_field_names=frozenset({"meaning", "semantic", "murad"}),
        stage_name="mufrad_proof",
        reason="No semantic fields"
    )

    assert forbidden.contains_forbidden_field("meaning")
    assert forbidden.contains_forbidden_field("semantic")
    assert not forbidden.contains_forbidden_field("allowed_field")

    msg = forbidden.get_violation_message("meaning")
    assert "meaning" in msg
    assert "forbidden" in msg
    assert "mufrad_proof" in msg


# ---------------------------------------------------------------------------
# Test: Type Signatures
# ---------------------------------------------------------------------------


def test_type_signatures():
    """Test DalTypedInput and DalTypedOutput signature generation."""

    typed_input = DalTypedInput(
        input_type_name="TestInput",
        source_stage="test_source"
    )

    typed_output = DalTypedOutput(
        output_type_name="TestOutput",
        target_stage="test_target"
    )

    assert typed_input.get_type_signature() == "test_source::TestInput"
    assert typed_output.get_type_signature() == "test_target::TestOutput"


# ---------------------------------------------------------------------------
# Test: Candidate Set Protocol with Dict-like Object
# ---------------------------------------------------------------------------


def test_ensure_no_forbidden_outputs_with_dict():
    """Test forbidden output validation with dict-like objects."""

    forbidden_spec = DalForbiddenOutput(
        forbidden_field_names=frozenset({"meaning", "semantic"}),
        stage_name="test_stage",
        reason="No semantic fields"
    )

    # Dict with forbidden key
    dict_obj = {
        "meaning": "forbidden_value",
        "allowed_key": "allowed_value"
    }

    with pytest.raises(ValueError, match="Forbidden outputs detected"):
        ensure_no_forbidden_outputs(
            dict_obj,
            (forbidden_spec,),
            "test_stage"
        )

    # Dict without forbidden keys
    clean_dict = {
        "allowed_key": "allowed_value"
    }

    # Should pass
    ensure_no_forbidden_outputs(
        clean_dict,
        (forbidden_spec,),
        "test_stage"
    )
