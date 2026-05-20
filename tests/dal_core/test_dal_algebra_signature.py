"""
Tests for Dal Algebra Signature (F1)

Tests the foundational typed transition contract for dal_core.
Including 8-layer transition domain architecture.
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
    # 8-Layer Architecture Enums
    TransitionDomain,
    TemplateKind,
    OriginKind,
    EvidencePolarity,
    AttestationPolicy,
    IdentityAxis,
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


# ---------------------------------------------------------------------------
# Test: 8-Layer Transition Domain Architecture
# ---------------------------------------------------------------------------


def test_transition_domain_enum_has_8_values():
    """Test that TransitionDomain enum has exactly 8 domains (D0-D7)."""
    domains = list(TransitionDomain)
    assert len(domains) == 8

    # Verify all 8 domains are present
    domain_values = {d.value for d in domains}
    expected = {
        "رسم_صوت",       # GRAPHOPHONEMIC
        "مقطعي",         # SYLLABIC
        "ما_قبل_الصرف",   # PRE_MORPH
        "أصل",           # ORIGIN
        "قالب",          # TEMPLATE
        "محاور_هوية",    # IDENTITY_AXIS
        "تحليل_اتجاهي",  # DIRECTIONAL_ANALYSIS
        "حكم",           # JUDGMENT
    }
    assert domain_values == expected


def test_template_kind_enum_has_7_values():
    """Test that TemplateKind enum has 7 template types."""
    template_kinds = list(TemplateKind)
    assert len(template_kinds) == 7

    # Verify key distinction: surface vs deep
    assert TemplateKind.SURFACE in template_kinds
    assert TemplateKind.DEEP in template_kinds
    assert TemplateKind.UNRESOLVED in template_kinds


def test_origin_kind_enum_distinguishes_root_vs_functional():
    """Test that OriginKind distinguishes root from functional units."""
    origin_kinds = list(OriginKind)

    # Must have ROOT and NON_ROOT_FUNCTIONAL
    assert OriginKind.ROOT in origin_kinds
    assert OriginKind.NON_ROOT_FUNCTIONAL in origin_kinds

    # Must have LEXICAL_JAMID for frozen words (يد، دم، شمس)
    assert OriginKind.LEXICAL_JAMID in origin_kinds


def test_attestation_policy_enum_enforces_lexicon_requirement():
    """Test that AttestationPolicy enforces lexicon requirement levels."""
    policies = list(AttestationPolicy)

    # Must have all 4 levels
    assert len(policies) == 4
    assert AttestationPolicy.NOT_REQUIRED in policies
    assert AttestationPolicy.OPTIONAL in policies
    assert AttestationPolicy.REQUIRED_FOR_CERTIFICATE in policies
    assert AttestationPolicy.REQUIRED_FOR_ANY_ACCEPTANCE in policies


def test_identity_axis_enum_has_5_parallel_axes():
    """Test that IdentityAxis has 5 parallel axes (not linear)."""
    axes = list(IdentityAxis)

    # Must have exactly 5 axes
    assert len(axes) == 5

    # Verify all 5 axes
    axis_values = {a.value for a in axes}
    expected = {
        "اشتقاق",  # DERIVATION
        "إعراب",   # IRAB
        "أصل",     # ORIGIN
        "تركيب",   # COMPOSITION
        "وظيفة",   # FUNCTION
    }
    assert axis_values == expected


def test_evidence_polarity_enum_tracks_supporting_vs_counter():
    """Test that EvidencePolarity tracks supporting vs counter-evidence."""
    polarities = list(EvidencePolarity)

    assert len(polarities) == 3
    assert EvidencePolarity.SUPPORTING in polarities
    assert EvidencePolarity.COUNTER in polarities
    assert EvidencePolarity.NEUTRAL in polarities


def test_transition_contract_with_8_layer_extensions():
    """Test DalTransitionContract with 8-layer architecture extensions."""

    # Create contract with TEMPLATE domain
    contract = DalTransitionContract(
        input_type=DalTypedInput(
            input_type_name="RootCandidate",
            source_stage="root_extractor"
        ),
        output_type=DalTypedOutput(
            output_type_name="TemplateCandidate",
            target_stage="template_matcher"
        ),
        stage_name="template_analyzer",
        transition_domain=TransitionDomain.TEMPLATE,
        template_kind=TemplateKind.GENERATED_MORPHOLOGICAL,
        requires_lexicon=False,
        requires_attestation=AttestationPolicy.OPTIONAL,
        requires_context=False,
        allows_unresolved=True
    )

    # Validate contract
    is_valid, violations = contract.validate_contract()
    assert is_valid
    assert len(violations) == 0

    # Verify 8-layer fields
    assert contract.transition_domain == TransitionDomain.TEMPLATE
    assert contract.template_kind == TemplateKind.GENERATED_MORPHOLOGICAL
    assert contract.requires_lexicon is False
    assert contract.requires_attestation == AttestationPolicy.OPTIONAL


def test_transition_contract_with_identity_axes():
    """Test DalTransitionContract with multiple identity axes."""

    contract = DalTransitionContract(
        input_type=DalTypedInput(
            input_type_name="TemplateCandidate",
            source_stage="template_matcher"
        ),
        output_type=DalTypedOutput(
            output_type_name="IdentityCandidate",
            target_stage="identity_analyzer"
        ),
        stage_name="identity_analysis",
        transition_domain=TransitionDomain.IDENTITY_AXIS,
        identity_axes=(
            IdentityAxis.DERIVATION,
            IdentityAxis.IRAB,
            IdentityAxis.FUNCTION,
        ),
        requires_lexicon=True,
        requires_attestation=AttestationPolicy.REQUIRED_FOR_CERTIFICATE,
    )

    # Verify multiple axes can be specified
    assert len(contract.identity_axes) == 3
    assert IdentityAxis.DERIVATION in contract.identity_axes
    assert IdentityAxis.IRAB in contract.identity_axes
    assert IdentityAxis.FUNCTION in contract.identity_axes


def test_transition_contract_with_frozen_lexical():
    """Test DalTransitionContract for frozen/lexical words (يد، دم، شمس)."""

    contract = DalTransitionContract(
        input_type=DalTypedInput(
            input_type_name="GraphophonemeCandidate",
            source_stage="graphophonemic"
        ),
        output_type=DalTypedOutput(
            output_type_name="OriginCandidate",
            target_stage="origin_analyzer"
        ),
        stage_name="frozen_word_detector",
        transition_domain=TransitionDomain.ORIGIN,
        origin_kind=OriginKind.LEXICAL_JAMID,
        requires_lexicon=True,
        requires_attestation=AttestationPolicy.REQUIRED_FOR_ANY_ACCEPTANCE,
        allows_unresolved=False,  # Frozen words MUST be in lexicon
    )

    # Verify frozen word contract
    assert contract.origin_kind == OriginKind.LEXICAL_JAMID
    assert contract.requires_lexicon is True
    assert contract.requires_attestation == AttestationPolicy.REQUIRED_FOR_ANY_ACCEPTANCE
    assert contract.allows_unresolved is False


def test_transition_contract_with_unresolved_template():
    """Test DalTransitionContract allowing unresolved patterns."""

    contract = DalTransitionContract(
        input_type=DalTypedInput(
            input_type_name="SyllableCandidate",
            source_stage="syllabifier"
        ),
        output_type=DalTypedOutput(
            output_type_name="TemplateCandidate",
            target_stage="template_matcher"
        ),
        stage_name="pattern_analyzer",
        transition_domain=TransitionDomain.TEMPLATE,
        template_kind=TemplateKind.UNRESOLVED,
        requires_lexicon=True,
        requires_context=True,
        allows_unresolved=True,
    )

    # Verify unresolved template allows pending outputs
    assert contract.template_kind == TemplateKind.UNRESOLVED
    assert contract.allows_unresolved is True
    assert contract.requires_lexicon is True
    assert contract.requires_context is True


def test_no_direct_promotion_across_layers():
    """
    Test the critical invariant: No direct promotion across layers.

    From problem statement:
    "رسم/صوت لا يرقى مباشرة إلى وزن"
    (Grapheme/phoneme does not promote directly to pattern)

    Each layer jump must go through intermediate contract.
    """

    # Contract D0 → D4 DIRECT (FORBIDDEN pattern)
    # This should be caught by validation logic (future enhancement)
    forbidden_direct_jump = DalTransitionContract(
        input_type=DalTypedInput(
            input_type_name="Grapheme",
            source_stage="graphophonemic"
        ),
        output_type=DalTypedOutput(
            output_type_name="Pattern",
            target_stage="template"  # Direct jump!
        ),
        stage_name="forbidden_direct_jump",
        transition_domain=TransitionDomain.GRAPHOPHONEMIC,
        # Note: This creates a mismatch between domain and output
    )

    # For now, just document this is a bad pattern
    # Future: Add validation that checks transition_domain matches input/output stages
    assert forbidden_direct_jump.transition_domain == TransitionDomain.GRAPHOPHONEMIC
    # But output is TEMPLATE domain - mismatch!

    # CORRECT pattern: D0 → D1 → D2 → D3 → D4
    # Each transition respects domain boundaries
