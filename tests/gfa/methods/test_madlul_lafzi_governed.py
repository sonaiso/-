"""
Tests for MadlulLafziGate - بوابة المدلول اللفظي

Critical Law:
    المدلول اللفظي ليس معنى خارجياً بالضرورة
    Madlūl-lafẓī is NOT necessarily external meaning.
    Madlūl-lafẓī is a governed candidate for what may be signified
    inside the linguistic domain.

Test Coverage (18 Required Tests):
    1. test_madlul_lafzi_requires_lafzi_registration
    2. test_madlul_lafzi_requires_lafzi_dalali_style
    3. test_madlul_lafzi_requires_neutral_binding
    4. test_madlul_lafzi_requires_prior_information
    5. test_madlul_lafzi_preserves_trace_id
    6. test_madlul_lafzi_preserves_residuals
    7. test_madlul_lafzi_does_not_create_external_meaning
    8. test_madlul_lafzi_does_not_create_dalalah
    9. test_madlul_lafzi_does_not_implement_wadh
    10. test_madlul_lafzi_does_not_issue_hukm
    11. test_madlul_lafzi_does_not_raise_predicate_rank
    12. test_madlul_lafzi_does_not_require_dal_candidate_yet
    13. test_unknown_madlul_type_becomes_residual
    14. test_madlul_lafzi_returns_governed_failure_not_exception
    15. test_madlul_lafzi_accepts_letter_entity
    16. test_madlul_lafzi_accepts_harakah_entity
    17. test_madlul_lafzi_accepts_pattern_entity
    18. test_madlul_lafzi_full_success_path

Critical:
    MadlulLafziCandidate is NOT external meaning.
    MadlulLafziCandidate is NOT Dalalah.
    MadlulLafziCandidate is a linguistic signified candidate.
"""

import pytest
from uuid import uuid4

from gfa.methods.styles import (
    StyleSpec,
    ThinkingDomain,
    make_lafzi_dalali_style,
)
from gfa.methods.lafzi_madlul import (
    MadlulLafziType,
    MadlulLafziCandidate,
    MadlulLafziGate,
    MadlulLafziResult,
    MadlulLafziFailureKind,
)


# Test fixtures

def make_test_madlul_lafzi_gate(
    registration_successful: bool = True,
    neutral_binding_available: bool = True,
    use_lafzi_dalali_style: bool = True
) -> MadlulLafziGate:
    """Create test MadlulLafziGate with specified configuration."""
    if use_lafzi_dalali_style:
        style_spec = make_lafzi_dalali_style()
    else:
        # For negative test, use a different domain style
        from gfa.methods.styles import make_formal_logical_style
        style_spec = make_formal_logical_style()

    return MadlulLafziGate(
        style_spec=style_spec,
        neutral_binding_available=neutral_binding_available,
        registration_successful=registration_successful,
    )


# Test 1: Requires LafziMadlul registration

def test_madlul_lafzi_requires_lafzi_registration():
    """
    Law 1: No MadlulLafziCandidate without LafziMadlul registration.

    Test that MadlulLafziGate requires successful registration.
    """
    # Create gate without registration
    gate = make_test_madlul_lafzi_gate(registration_successful=False)

    assert not gate.verify_registration()

    # Process input should fail
    result = gate.process_input(
        trace_id="test_madlul_001",
        madlul_type=MadlulLafziType.LETTER_ENTITY,
        candidate_form="ك",
        prior_information="letter kaf",
    )

    assert result.is_failure
    assert result.failure.residual.kind == MadlulLafziFailureKind.MISSING_LAFZI_REGISTRATION


# Test 2: Requires StyleSpec(LAFZI_DALALI)

def test_madlul_lafzi_requires_lafzi_dalali_style():
    """
    Law 2: No MadlulLafziCandidate without StyleSpec(LAFZI_DALALI).

    Test that MadlulLafziGate requires correct StyleSpec domain.
    """
    # Create gate with correct style
    gate = make_test_madlul_lafzi_gate(use_lafzi_dalali_style=True)
    assert gate.verify_style_spec()
    assert gate.style_spec.get_domain() == ThinkingDomain.LAFZI_DALALI

    # Create gate with wrong domain
    gate_wrong = make_test_madlul_lafzi_gate(use_lafzi_dalali_style=False)
    assert not gate_wrong.verify_style_spec()

    # Process should fail with wrong domain
    result = gate_wrong.process_input(
        trace_id="test_madlul_002",
        madlul_type=MadlulLafziType.LETTER_ENTITY,
        candidate_form="ت",
        prior_information="letter ta",
    )

    assert result.is_failure
    assert result.failure.residual.kind == MadlulLafziFailureKind.WRONG_DOMAIN


# Test 3: Requires NeutralBinding

def test_madlul_lafzi_requires_neutral_binding():
    """
    Law 3: No MadlulLafziCandidate without NeutralBinding.

    Test that MadlulLafziGate requires NeutralBinding.
    """
    # Create gate without NeutralBinding
    gate = make_test_madlul_lafzi_gate(neutral_binding_available=False)

    assert not gate.verify_neutral_binding()

    # Process input should fail
    result = gate.process_input(
        trace_id="test_madlul_003",
        madlul_type=MadlulLafziType.HARAKAH_ENTITY,
        candidate_form="َ",
        prior_information="fatha",
    )

    assert result.is_failure
    assert result.failure.residual.kind == MadlulLafziFailureKind.MISSING_NEUTRAL_BINDING


# Test 4: Requires PriorInformation

def test_madlul_lafzi_requires_prior_information():
    """
    Law 4: No MadlulLafziCandidate without PriorInformation.

    Test that MadlulLafziGate requires PriorInformation.
    """
    gate = make_test_madlul_lafzi_gate()

    # Process without prior information should fail
    result = gate.process_input(
        trace_id="test_madlul_004",
        madlul_type=MadlulLafziType.PATTERN_ENTITY,
        candidate_form="فَعَلَ",
        prior_information="",  # Empty prior information
    )

    assert result.is_failure
    assert result.failure.residual.kind == MadlulLafziFailureKind.MISSING_PRIOR_INFORMATION

    # Process with prior information should succeed
    result2 = gate.process_input(
        trace_id="test_madlul_004b",
        madlul_type=MadlulLafziType.PATTERN_ENTITY,
        candidate_form="فَعَلَ",
        prior_information="trilateral verb pattern",
    )

    assert result2.is_success


# Test 5: Preserves trace_id

def test_madlul_lafzi_preserves_trace_id():
    """
    Law 5: MadlulLafziCandidate preserves trace_id.

    Test that trace_id is preserved through processing.
    """
    gate = make_test_madlul_lafzi_gate()

    trace_id = "test_madlul_preserve_001"
    result = gate.process_input(
        trace_id=trace_id,
        madlul_type=MadlulLafziType.ROOT_CANDIDATE,
        candidate_form="كتب",
        prior_information="trilateral root k-t-b",
    )

    assert result.is_success
    assert result.candidate.trace_id == trace_id
    assert gate.preserves_trace_id(trace_id)


# Test 6: Preserves residuals

def test_madlul_lafzi_preserves_residuals():
    """
    Law 6: MadlulLafziCandidate preserves residuals.

    Test that residuals are preserved from input.
    """
    gate = make_test_madlul_lafzi_gate()

    # Create input with residual
    from gfa.methods.lafzi_madlul import make_unknown_madlul_type_residual
    residual = make_unknown_madlul_type_residual("test_trace_001")

    # Process with residual
    result = gate.process_input(
        trace_id="test_madlul_preserve_002",
        madlul_type=MadlulLafziType.FORM_ENTITY,
        candidate_form="كَاتِب",
        prior_information="active participle form",
        residuals=(residual,),
    )

    assert result.is_success
    assert isinstance(result.candidate.residuals, tuple)
    assert len(result.candidate.residuals) >= 1
    assert residual in result.candidate.residuals
    assert gate.preserves_residuals()


# Test 7: Does not create external meaning

def test_madlul_lafzi_does_not_create_external_meaning():
    """
    Law 7: MadlulLafziCandidate does not create external meaning.

    Test that MadlulLafziCandidate does NOT create semantic external meaning.
    """
    gate = make_test_madlul_lafzi_gate()

    # Verify no external meaning creation
    assert gate.does_not_create_external_meaning()

    # Process input
    result = gate.process_input(
        trace_id="test_madlul_meaning_001",
        madlul_type=MadlulLafziType.WORD_ENTITY,
        candidate_form="كتاب",
        prior_information="word kitab",
    )

    assert result.is_success

    # Candidate object has no external 'meaning' attribute
    assert not hasattr(result.candidate, "meaning")
    assert not hasattr(result.candidate, "external_meaning")
    assert not hasattr(result.candidate, "semantic_meaning")


# Test 8: Does not create Dalalah

def test_madlul_lafzi_does_not_create_dalalah():
    """
    Law 8: MadlulLafziCandidate does not create Dalalah.

    Test that MadlulLafziCandidate does NOT implement Dalalah (الدلالة).
    """
    gate = make_test_madlul_lafzi_gate()

    # Verify no Dalalah creation
    assert gate.does_not_create_dalalah()

    # Process input
    result = gate.process_input(
        trace_id="test_madlul_dalalah_001",
        madlul_type=MadlulLafziType.COMPOSITE_LAFZI_ENTITY,
        candidate_form="كتب الدرس",
        prior_information="composite phrase",
    )

    assert result.is_success

    # Candidate has no Dalalah attribute
    assert not hasattr(result.candidate, "dalalah")
    assert not hasattr(result.candidate, "signification")
    assert not hasattr(result.candidate, "dalalah_wadia")


# Test 9: Does not implement Wadh

def test_madlul_lafzi_does_not_implement_wadh():
    """
    Law 9: MadlulLafziCandidate does not implement Wadh.

    Test that MadlulLafziCandidate does NOT implement Wadh (الوضع).
    """
    gate = make_test_madlul_lafzi_gate()

    # Verify no Wadh implementation
    assert gate.does_not_implement_wadh()

    # Process input
    result = gate.process_input(
        trace_id="test_madlul_wadh_001",
        madlul_type=MadlulLafziType.CONCEPTUAL_LAFZI_ENTITY,
        candidate_form="اسم",
        prior_information="conceptual entity 'noun'",
    )

    assert result.is_success

    # Candidate has no Wadh attribute
    assert not hasattr(result.candidate, "wadh")
    assert not hasattr(result.candidate, "conventional_placement")
    assert not hasattr(result.candidate, "arbitrary_assignment")


# Test 10: Does not issue HUKM

def test_madlul_lafzi_does_not_issue_hukm():
    """
    Law 10: MadlulLafziCandidate does not issue HUKM.

    Test that MadlulLafziCandidate does NOT issue judgment.
    """
    gate = make_test_madlul_lafzi_gate()

    # Verify no HUKM issuance
    assert gate.does_not_issue_hukm()

    # Process input
    result = gate.process_input(
        trace_id="test_madlul_hukm_001",
        madlul_type=MadlulLafziType.SYLLABLE_ENTITY,
        candidate_form="كَتَ",
        prior_information="syllable ka-ta",
    )

    assert result.is_success

    # Candidate has no HUKM attribute
    assert not hasattr(result.candidate, "hukm")
    assert not hasattr(result.candidate, "judgment")
    assert not hasattr(result.candidate, "certification")


# Test 11: Does not raise PredicateRank

def test_madlul_lafzi_does_not_raise_predicate_rank():
    """
    Law 11: MadlulLafziCandidate does not raise PredicateRank.

    Test that MadlulLafziCandidate does NOT inflate predicate rank.
    """
    gate = make_test_madlul_lafzi_gate()

    # Verify no rank inflation
    assert gate.does_not_raise_predicate_rank()

    # Process input
    result = gate.process_input(
        trace_id="test_madlul_rank_001",
        madlul_type=MadlulLafziType.LETTER_ENTITY,
        candidate_form="ب",
        prior_information="letter ba",
    )

    assert result.is_success

    # Candidate has no rank attribute
    assert not hasattr(result.candidate, "predicate_rank")
    assert not hasattr(result.candidate, "certification_level")
    assert not hasattr(result.candidate, "rank_elevation")


# Test 12: Does not require DalCandidate yet

def test_madlul_lafzi_does_not_require_dal_candidate_yet():
    """
    Law 12: MadlulLafziCandidate does not require DalCandidate yet.

    Test that MadlulLafziCandidate can be built independently
    without requiring DalCandidate.
    """
    gate = make_test_madlul_lafzi_gate()

    # Verify no DalCandidate requirement
    assert gate.does_not_require_dal_candidate_yet()

    # Process input without any DalCandidate parameter
    result = gate.process_input(
        trace_id="test_madlul_dal_001",
        madlul_type=MadlulLafziType.HARAKAH_ENTITY,
        candidate_form="ُ",
        prior_information="damma",
    )

    assert result.is_success

    # Candidate has no dal_candidate attribute
    assert not hasattr(result.candidate, "dal_candidate")
    assert not hasattr(result.candidate, "signifier")
    assert not hasattr(result.candidate, "dal")


# Test 13: UNKNOWN madlul type becomes residual

def test_unknown_madlul_type_becomes_residual():
    """
    Law 13: UNKNOWN madlul type becomes residual, not exception.

    Test that UNKNOWN madlul type is handled gracefully as residual.
    """
    gate = make_test_madlul_lafzi_gate()

    # Process UNKNOWN madlul type
    result = gate.process_input(
        trace_id="test_madlul_unknown_001",
        madlul_type=MadlulLafziType.UNKNOWN_MADLUL,
        candidate_form="[unknown_entity]",
        prior_information="unknown entity information",
    )

    # Should still succeed (not raise exception)
    assert result.is_success

    # But should have residual
    assert result.candidate.has_residuals
    assert len(result.candidate.residuals) >= 1

    # Should be UNKNOWN type
    assert result.candidate.madlul_type == MadlulLafziType.UNKNOWN_MADLUL

    # Should have UNKNOWN_MADLUL_TYPE residual
    madlul_residuals = [r for r in result.candidate.residuals
                        if hasattr(r, 'kind') and r.kind == MadlulLafziFailureKind.UNKNOWN_MADLUL_TYPE]
    assert len(madlul_residuals) == 1
    assert "UNKNOWN" in madlul_residuals[0].reason


# Test 14: Returns governed failure, not exception

def test_madlul_lafzi_returns_governed_failure_not_exception():
    """
    Law 14: MadlulLafziGate returns governed failure, not exception.

    When requirements not met, should return MadlulLafziFailure,
    not raise Python exception.
    """
    # Test with missing registration
    gate = make_test_madlul_lafzi_gate(registration_successful=False)
    result = gate.process_input(
        trace_id="test_madlul_governed_001",
        madlul_type=MadlulLafziType.LETTER_ENTITY,
        candidate_form="ج",
        prior_information="letter jeem",
    )

    # Should return failure, not raise exception
    assert result.is_failure
    assert result.failure is not None
    assert result.failure.residual.kind == MadlulLafziFailureKind.MISSING_LAFZI_REGISTRATION

    # Test with missing NeutralBinding
    gate2 = make_test_madlul_lafzi_gate(neutral_binding_available=False)
    result2 = gate2.process_input(
        trace_id="test_madlul_governed_002",
        madlul_type=MadlulLafziType.HARAKAH_ENTITY,
        candidate_form="ِ",
        prior_information="kasra",
    )

    assert result2.is_failure
    assert result2.failure.residual.kind == MadlulLafziFailureKind.MISSING_NEUTRAL_BINDING


# Test 15: Accepts letter entity

def test_madlul_lafzi_accepts_letter_entity():
    """
    Test that MadlulLafziGate accepts LETTER_ENTITY type.

    Letter as linguistic entity: حرف ككيان لفظي
    """
    gate = make_test_madlul_lafzi_gate()

    result = gate.process_input(
        trace_id="test_letter_entity_001",
        madlul_type=MadlulLafziType.LETTER_ENTITY,
        candidate_form="د",
        prior_information="letter dal",
    )

    assert result.is_success
    assert result.candidate.madlul_type == MadlulLafziType.LETTER_ENTITY
    assert result.candidate.madlul_type.is_letter
    assert result.candidate.candidate_form == "د"


# Test 16: Accepts harakah entity

def test_madlul_lafzi_accepts_harakah_entity():
    """
    Test that MadlulLafziGate accepts HARAKAH_ENTITY type.

    Harakah as linguistic entity: حركة ككيان لفظي
    """
    gate = make_test_madlul_lafzi_gate()

    result = gate.process_input(
        trace_id="test_harakah_entity_001",
        madlul_type=MadlulLafziType.HARAKAH_ENTITY,
        candidate_form="َ",
        prior_information="fatha diacritic",
    )

    assert result.is_success
    assert result.candidate.madlul_type == MadlulLafziType.HARAKAH_ENTITY
    assert result.candidate.madlul_type.is_harakah
    assert result.candidate.candidate_form == "َ"


# Test 17: Accepts pattern entity

def test_madlul_lafzi_accepts_pattern_entity():
    """
    Test that MadlulLafziGate accepts PATTERN_ENTITY type.

    Pattern as linguistic entity: وزن ككيان لفظي
    """
    gate = make_test_madlul_lafzi_gate()

    result = gate.process_input(
        trace_id="test_pattern_entity_001",
        madlul_type=MadlulLafziType.PATTERN_ENTITY,
        candidate_form="فَاعِل",
        prior_information="faa'il active participle pattern",
    )

    assert result.is_success
    assert result.candidate.madlul_type == MadlulLafziType.PATTERN_ENTITY
    assert result.candidate.madlul_type.is_pattern
    assert result.candidate.candidate_form == "فَاعِل"


# Test 18: Full success path

def test_madlul_lafzi_full_success_path():
    """
    Integration test: Full successful MadlulLafziCandidate processing.

    Tests complete flow:
        1. Input preparation
        2. MadlulLafziGate verification
        3. MadlulLafziCandidate creation
        4. Result validation
    """
    # Step 1: Prepare input
    trace_id = "integration_madlul_001"
    madlul_type = MadlulLafziType.WORD_ENTITY
    candidate_form = "كِتَاب"
    prior_information = "word kitab (book) as linguistic entity"

    # Step 2: Create gate with all requirements
    gate = make_test_madlul_lafzi_gate()

    # Step 3: Process input
    result = gate.process_input(
        trace_id=trace_id,
        madlul_type=madlul_type,
        candidate_form=candidate_form,
        prior_information=prior_information,
    )

    # Step 4: Validate result
    assert result.is_success
    assert result.candidate is not None
    assert result.candidate.trace_id == trace_id
    assert result.candidate.madlul_type == madlul_type
    assert result.candidate.candidate_form == candidate_form
    assert result.candidate.source_prior_information == prior_information
    assert result.candidate.is_valid

    # Verify all laws satisfied
    assert gate.verify_registration()
    assert gate.verify_style_spec()
    assert gate.verify_neutral_binding()
    assert gate.verify_prior_information(prior_information)
    assert gate.preserves_trace_id(trace_id)
    assert gate.preserves_residuals()
    assert gate.does_not_create_external_meaning()
    assert gate.does_not_create_dalalah()
    assert gate.does_not_implement_wadh()
    assert gate.does_not_issue_hukm()
    assert gate.does_not_raise_predicate_rank()
    assert gate.does_not_require_dal_candidate_yet()


# Additional integration tests

def test_madlul_lafzi_candidate_immutability():
    """
    Test that MadlulLafziCandidate is immutable (frozen dataclass).

    This ensures lineage integrity and trace preservation.
    """
    gate = make_test_madlul_lafzi_gate()
    result = gate.process_input(
        trace_id="test_immutable_001",
        madlul_type=MadlulLafziType.ROOT_CANDIDATE,
        candidate_form="درس",
        prior_information="trilateral root d-r-s",
    )

    assert result.is_success
    candidate = result.candidate

    # Attempt to modify should raise error
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        candidate.trace_id = "modified"

    with pytest.raises(Exception):
        candidate.candidate_form = "modified"

    with pytest.raises(Exception):
        candidate.madlul_type = MadlulLafziType.LETTER_ENTITY


def test_madlul_lafzi_residual_preservation_chain():
    """
    Test that residuals are preserved through processing chain.

    This ensures no information loss in the processing pipeline.
    """
    from gfa.methods.lafzi_madlul import MadlulLafziResidual, MadlulLafziFailureKind

    gate = make_test_madlul_lafzi_gate()

    # Create input with multiple residuals
    residual1 = MadlulLafziResidual(
        kind=MadlulLafziFailureKind.UNKNOWN_MADLUL_TYPE,
        reason="Test residual 1",
        violated_law="Test law 1",
        trace_id="test_trace_chain_001",
    )

    residual2 = MadlulLafziResidual(
        kind=MadlulLafziFailureKind.TRACE_NOT_PRESERVED,
        reason="Test residual 2",
        violated_law="Test law 2",
        trace_id="test_trace_chain_001",
    )

    # Process through MadlulLafziGate
    result = gate.process_input(
        trace_id="test_trace_chain_001",
        madlul_type=MadlulLafziType.FORM_ENTITY,
        candidate_form="مَفْعُول",
        prior_information="passive participle form",
        residuals=(residual1, residual2),
    )

    assert result.is_success
    assert len(result.candidate.residuals) >= 2

    # Original residuals should be preserved
    assert residual1 in result.candidate.residuals
    assert residual2 in result.candidate.residuals
