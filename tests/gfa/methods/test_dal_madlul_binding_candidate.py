"""
Tests for DalMadlulBindingGate - بوابة الربط بين الدال والمدلول

Critical Law:
    الربط بين الدال والمدلول ليس دلالة كاملة
    Binding between Dāl and Madlūl is NOT full Dalalah.
    It is a neutral relation candidate.

Test Coverage (18 Required Tests):
    1. test_dal_madlul_binding_requires_dal_candidate
    2. test_dal_madlul_binding_requires_madlul_candidate
    3. test_dal_madlul_binding_requires_lafzi_dalali_style
    4. test_dal_madlul_binding_requires_neutral_binding
    5. test_dal_madlul_binding_preserves_trace_id
    6. test_dal_madlul_binding_preserves_residuals_from_both_sides
    7. test_dal_madlul_binding_does_not_create_dalalah
    8. test_dal_madlul_binding_does_not_implement_wadh
    9. test_dal_madlul_binding_does_not_create_external_meaning
    10. test_dal_madlul_binding_does_not_issue_hukm
    11. test_dal_madlul_binding_does_not_raise_predicate_rank
    12. test_dal_madlul_binding_does_not_perform_semantic_interpretation
    13. test_dal_madlul_binding_does_not_implement_mutabaqah
    14. test_dal_madlul_binding_returns_governed_failure_not_exception
    15. test_dal_madlul_binding_simple_binding_success
    16. test_dal_madlul_binding_composite_binding_success
    17. test_dal_madlul_binding_candidate_immutability
    18. test_dal_madlul_binding_full_success_path

Critical:
    DalMadlulBindingCandidate is a NEUTRAL RELATION, not full Dalalah.
    It connects signifier and signified WITHOUT semantic interpretation.
"""

import pytest
from uuid import uuid4

from gfa.methods.styles import (
    StyleSpec,
    ThinkingDomain,
    make_lafzi_dalali_style,
)
from gfa.methods.lafzi_dal import DalCandidate, DalType
from gfa.methods.lafzi_madlul import (
    MadlulLafziCandidate,
    MadlulLafziType,
)
from gfa.methods.lafzi_dalalah import (
    DalMadlulBindingType,
    DalMadlulBindingCandidate,
    DalMadlulBindingResult,
    DalMadlulBindingGate,
    DalMadlulBindingFailure,
    DalMadlulBindingFailureKind,
)


# Test fixtures


def make_test_dal_candidate(
    candidate_form: str = "ك", trace_id: str = "dal_001"
) -> DalCandidate:
    """Create test DalCandidate."""
    return DalCandidate(
        trace_id=trace_id,
        dal_type=DalType.LETTER_DAL,
        candidate_form=candidate_form,
        source_prior_information=f"letter {candidate_form}",
        residuals=(),
    )


def make_test_madlul_candidate(
    candidate_form: str = "ك", trace_id: str = "madlul_001"
) -> MadlulLafziCandidate:
    """Create test MadlulLafziCandidate."""
    return MadlulLafziCandidate(
        trace_id=trace_id,
        madlul_type=MadlulLafziType.LETTER_ENTITY,
        candidate_form=candidate_form,
        source_prior_information=f"letter entity {candidate_form}",
        residuals=(),
    )


def make_test_binding_gate(
    neutral_binding_available: bool = True,
    use_lafzi_dalali_style: bool = True,
) -> DalMadlulBindingGate:
    """Create test DalMadlulBindingGate with specified configuration."""
    if use_lafzi_dalali_style:
        style_spec = make_lafzi_dalali_style()
    else:
        from gfa.methods.styles import make_formal_logical_style

        style_spec = make_formal_logical_style()

    return DalMadlulBindingGate(
        style_spec=style_spec,
        neutral_binding_available=neutral_binding_available,
    )


# Test 1: Requires DalCandidate


def test_dal_madlul_binding_requires_dal_candidate():
    """
    Law 1: No DalMadlulBinding without DalCandidate.

    Test that DalMadlulBindingGate requires DalCandidate.
    """
    gate = make_test_binding_gate()
    madlul = make_test_madlul_candidate()

    # Process without DalCandidate should fail
    result = gate.process_binding(
        trace_id="test_binding_001",
        dal_candidate=None,  # Missing DalCandidate
        madlul_candidate=madlul,
        prior_information="test binding",
    )

    assert result.is_failure
    assert result.failure.residual.kind == DalMadlulBindingFailureKind.MISSING_DAL_CANDIDATE


# Test 2: Requires MadlulLafziCandidate


def test_dal_madlul_binding_requires_madlul_candidate():
    """
    Law 2: No DalMadlulBinding without MadlulLafziCandidate.

    Test that DalMadlulBindingGate requires MadlulLafziCandidate.
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate()

    # Process without MadlulLafziCandidate should fail
    result = gate.process_binding(
        trace_id="test_binding_002",
        dal_candidate=dal,
        madlul_candidate=None,  # Missing MadlulLafziCandidate
        prior_information="test binding",
    )

    assert result.is_failure
    assert result.failure.residual.kind == DalMadlulBindingFailureKind.MISSING_MADLUL_CANDIDATE


# Test 3: Requires StyleSpec(LAFZI_DALALI)


def test_dal_madlul_binding_requires_lafzi_dalali_style():
    """
    Law 3: No DalMadlulBinding without StyleSpec(LAFZI_DALALI).

    Test that DalMadlulBindingGate requires correct StyleSpec domain.
    """
    # Create gate with correct style
    gate = make_test_binding_gate(use_lafzi_dalali_style=True)
    assert gate.verify_style_spec()
    assert gate.style_spec.get_domain() == ThinkingDomain.LAFZI_DALALI

    # Create gate with wrong domain
    gate_wrong = make_test_binding_gate(use_lafzi_dalali_style=False)
    assert not gate_wrong.verify_style_spec()


# Test 4: Requires NeutralBinding


def test_dal_madlul_binding_requires_neutral_binding():
    """
    Law 4: No DalMadlulBinding without NeutralBinding.

    Test that DalMadlulBindingGate requires NeutralBinding.
    """
    # Create gate without NeutralBinding
    gate = make_test_binding_gate(neutral_binding_available=False)

    assert not gate.verify_neutral_binding()


# Test 5: Preserves trace_id


def test_dal_madlul_binding_preserves_trace_id():
    """
    Law 5: DalMadlulBinding preserves trace_id.

    Test that trace_id is preserved through binding.
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate()
    madlul = make_test_madlul_candidate()

    trace_id = "test_binding_preserve_001"
    result = gate.process_binding(
        trace_id=trace_id,
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="binding with trace",
    )

    assert result.is_success
    assert result.candidate.trace_id == trace_id
    assert gate.preserves_trace_id(trace_id)


# Test 6: Preserves residuals from both sides


def test_dal_madlul_binding_preserves_residuals_from_both_sides():
    """
    Law 6: DalMadlulBinding preserves residuals from both sides.

    Test that residuals from Dal and Madlul are preserved.
    """
    gate = make_test_binding_gate()

    # Create Dal and Madlul with residuals
    from gfa.methods.lafzi_dal import make_unknown_dal_type_residual
    from gfa.methods.lafzi_madlul import make_unknown_madlul_type_residual

    dal_residual = make_unknown_dal_type_residual("dal_trace_001")
    madlul_residual = make_unknown_madlul_type_residual("madlul_trace_001")

    dal = DalCandidate(
        trace_id="dal_trace_001",
        dal_type=DalType.LETTER_DAL,
        candidate_form="ب",
        source_prior_information="letter ba",
        residuals=(dal_residual,),
    )

    madlul = MadlulLafziCandidate(
        trace_id="madlul_trace_001",
        madlul_type=MadlulLafziType.LETTER_ENTITY,
        candidate_form="ب",
        source_prior_information="letter entity ba",
        residuals=(madlul_residual,),
    )

    # Process binding
    result = gate.process_binding(
        trace_id="test_binding_preserve_002",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="binding with residuals",
    )

    assert result.is_success
    assert isinstance(result.candidate.residuals, tuple)
    assert len(result.candidate.residuals) >= 2
    assert dal_residual in result.candidate.residuals
    assert madlul_residual in result.candidate.residuals
    assert gate.preserves_residuals()


# Test 7: Does not create Dalalah


def test_dal_madlul_binding_does_not_create_dalalah():
    """
    Law 7: DalMadlulBinding does NOT create full Dalalah.

    Test that binding does NOT create Dalalah (الدلالة).
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate()
    madlul = make_test_madlul_candidate()

    # Verify no Dalalah creation
    assert gate.does_not_create_dalalah()

    # Process binding
    result = gate.process_binding(
        trace_id="test_binding_dalalah_001",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="neutral binding",
    )

    assert result.is_success

    # Candidate has no Dalalah attribute
    assert not hasattr(result.candidate, "dalalah")
    assert not hasattr(result.candidate, "signification")
    assert not hasattr(result.candidate, "full_dalalah")


# Test 8: Does not implement Wadh


def test_dal_madlul_binding_does_not_implement_wadh():
    """
    Law 8: DalMadlulBinding does NOT implement Wadh.

    Test that binding does NOT implement Wadh (الوضع).
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate()
    madlul = make_test_madlul_candidate()

    # Verify no Wadh implementation
    assert gate.does_not_implement_wadh()

    # Process binding
    result = gate.process_binding(
        trace_id="test_binding_wadh_001",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="neutral binding",
    )

    assert result.is_success

    # Candidate has no Wadh attribute
    assert not hasattr(result.candidate, "wadh")
    assert not hasattr(result.candidate, "conventional_placement")
    assert not hasattr(result.candidate, "arbitrary_assignment")


# Test 9: Does not create external meaning


def test_dal_madlul_binding_does_not_create_external_meaning():
    """
    Law 9: DalMadlulBinding does NOT create external meaning.

    Test that binding does NOT create semantic external meaning.
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate()
    madlul = make_test_madlul_candidate()

    # Verify no external meaning creation
    assert gate.does_not_create_external_meaning()

    # Process binding
    result = gate.process_binding(
        trace_id="test_binding_meaning_001",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="neutral binding",
    )

    assert result.is_success

    # Candidate has no external meaning attribute
    assert not hasattr(result.candidate, "meaning")
    assert not hasattr(result.candidate, "external_meaning")
    assert not hasattr(result.candidate, "semantic_meaning")


# Test 10: Does not issue HUKM


def test_dal_madlul_binding_does_not_issue_hukm():
    """
    Law 10: DalMadlulBinding does NOT issue HUKM.

    Test that binding does NOT issue judgment.
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate()
    madlul = make_test_madlul_candidate()

    # Verify no HUKM issuance
    assert gate.does_not_issue_hukm()

    # Process binding
    result = gate.process_binding(
        trace_id="test_binding_hukm_001",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="neutral binding",
    )

    assert result.is_success

    # Candidate has no HUKM attribute
    assert not hasattr(result.candidate, "hukm")
    assert not hasattr(result.candidate, "judgment")
    assert not hasattr(result.candidate, "certification")


# Test 11: Does not raise PredicateRank


def test_dal_madlul_binding_does_not_raise_predicate_rank():
    """
    Law 11: DalMadlulBinding does NOT raise PredicateRank.

    Test that binding does NOT inflate predicate rank.
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate()
    madlul = make_test_madlul_candidate()

    # Verify no rank inflation
    assert gate.does_not_raise_predicate_rank()

    # Process binding
    result = gate.process_binding(
        trace_id="test_binding_rank_001",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="neutral binding",
    )

    assert result.is_success

    # Candidate has no rank attribute
    assert not hasattr(result.candidate, "predicate_rank")
    assert not hasattr(result.candidate, "certification_level")
    assert not hasattr(result.candidate, "rank_elevation")


# Test 12: Does not perform semantic interpretation


def test_dal_madlul_binding_does_not_perform_semantic_interpretation():
    """
    Law 12: DalMadlulBinding does NOT perform semantic interpretation.

    Test that binding is neutral, not interpretive.
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate()
    madlul = make_test_madlul_candidate()

    # Verify no semantic interpretation
    assert gate.does_not_perform_semantic_interpretation()

    # Process binding
    result = gate.process_binding(
        trace_id="test_binding_semantic_001",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="neutral binding",
    )

    assert result.is_success

    # Candidate has no semantic interpretation attributes
    assert not hasattr(result.candidate, "semantic_interpretation")
    assert not hasattr(result.candidate, "meaning_analysis")
    assert not hasattr(result.candidate, "interpretation")


# Test 13: Does not implement Mutabaqah


def test_dal_madlul_binding_does_not_implement_mutabaqah():
    """
    Law 13: DalMadlulBinding does NOT implement Mutabaqah/Tadammun/Iltizam.

    Test that binding does NOT implement semantic relations.
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate()
    madlul = make_test_madlul_candidate()

    # Verify no Mutabaqah implementation
    assert gate.does_not_implement_mutabaqah()

    # Process binding
    result = gate.process_binding(
        trace_id="test_binding_mutabaqah_001",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="neutral binding",
    )

    assert result.is_success

    # Candidate has no semantic relation attributes
    assert not hasattr(result.candidate, "mutabaqah")
    assert not hasattr(result.candidate, "tadammun")
    assert not hasattr(result.candidate, "iltizam")


# Test 14: Returns governed failure, not exception


def test_dal_madlul_binding_returns_governed_failure_not_exception():
    """
    Law 14: DalMadlulBindingGate returns governed failure, not exception.

    When requirements not met, should return DalMadlulBindingFailure,
    not raise Python exception.
    """
    gate = make_test_binding_gate()

    # Test with missing DalCandidate
    result = gate.process_binding(
        trace_id="test_binding_governed_001",
        dal_candidate=None,
        madlul_candidate=make_test_madlul_candidate(),
        prior_information="test binding",
    )

    # Should return failure, not raise exception
    assert result.is_failure
    assert result.failure is not None
    assert result.failure.residual.kind == DalMadlulBindingFailureKind.MISSING_DAL_CANDIDATE

    # Test with missing MadlulCandidate
    result2 = gate.process_binding(
        trace_id="test_binding_governed_002",
        dal_candidate=make_test_dal_candidate(),
        madlul_candidate=None,
        prior_information="test binding",
    )

    assert result2.is_failure
    assert result2.failure.residual.kind == DalMadlulBindingFailureKind.MISSING_MADLUL_CANDIDATE


# Test 15: Simple binding success


def test_dal_madlul_binding_simple_binding_success():
    """
    Test simple one-to-one binding success path.

    Simple binding: دال واحد ← مدلول واحد
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate(candidate_form="ت")
    madlul = make_test_madlul_candidate(candidate_form="ت")

    result = gate.process_binding(
        trace_id="test_simple_binding_001",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="simple letter binding",
        binding_type=DalMadlulBindingType.SIMPLE_BINDING,
    )

    assert result.is_success
    assert result.candidate.binding_type == DalMadlulBindingType.SIMPLE_BINDING
    assert result.candidate.is_simple
    assert result.candidate.dal_candidate == dal
    assert result.candidate.madlul_candidate == madlul


# Test 16: Composite binding success


def test_dal_madlul_binding_composite_binding_success():
    """
    Test composite binding success path.

    Composite binding: دال مركب ← مدلول مركب
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate(candidate_form="كتاب")
    madlul = make_test_madlul_candidate(candidate_form="كتاب")

    result = gate.process_binding(
        trace_id="test_composite_binding_001",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="composite word binding",
        binding_type=DalMadlulBindingType.COMPOSITE_BINDING,
    )

    assert result.is_success
    assert result.candidate.binding_type == DalMadlulBindingType.COMPOSITE_BINDING
    assert result.candidate.is_composite
    assert result.candidate.dal_candidate == dal
    assert result.candidate.madlul_candidate == madlul


# Test 17: Candidate immutability


def test_dal_madlul_binding_candidate_immutability():
    """
    Test that DalMadlulBindingCandidate is immutable (frozen dataclass).

    This ensures binding integrity and trace preservation.
    """
    gate = make_test_binding_gate()
    dal = make_test_dal_candidate()
    madlul = make_test_madlul_candidate()

    result = gate.process_binding(
        trace_id="test_immutable_001",
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information="immutable binding",
    )

    assert result.is_success
    candidate = result.candidate

    # Attempt to modify should raise error
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        candidate.trace_id = "modified"

    with pytest.raises(Exception):
        candidate.binding_type = DalMadlulBindingType.COMPOSITE_BINDING

    with pytest.raises(Exception):
        candidate.dal_candidate = None


# Test 18: Full success path


def test_dal_madlul_binding_full_success_path():
    """
    Integration test: Full successful DalMadlulBinding processing.

    Tests complete flow:
        1. Input preparation (Dal + Madlul)
        2. DalMadlulBindingGate verification
        3. DalMadlulBindingCandidate creation
        4. Result validation
    """
    # Step 1: Prepare inputs
    trace_id = "integration_binding_001"
    dal = make_test_dal_candidate(candidate_form="ج", trace_id="dal_int_001")
    madlul = make_test_madlul_candidate(
        candidate_form="ج", trace_id="madlul_int_001"
    )
    prior_information = "letter jeem binding as neutral relation"

    # Step 2: Create gate with all requirements
    gate = make_test_binding_gate()

    # Step 3: Process binding
    result = gate.process_binding(
        trace_id=trace_id,
        dal_candidate=dal,
        madlul_candidate=madlul,
        prior_information=prior_information,
        binding_type=DalMadlulBindingType.SIMPLE_BINDING,
    )

    # Step 4: Validate result
    assert result.is_success
    assert result.candidate is not None
    assert result.candidate.trace_id == trace_id
    assert result.candidate.binding_type == DalMadlulBindingType.SIMPLE_BINDING
    assert result.candidate.dal_candidate == dal
    assert result.candidate.madlul_candidate == madlul
    assert result.candidate.source_prior_information == prior_information
    assert result.candidate.is_valid
    assert result.candidate.is_simple

    # Verify all laws satisfied
    assert gate.verify_style_spec()
    assert gate.verify_neutral_binding()
    assert gate.verify_dal_candidate(dal)
    assert gate.verify_madlul_candidate(madlul)
    assert gate.preserves_trace_id(trace_id)
    assert gate.preserves_residuals()
    assert gate.does_not_create_dalalah()
    assert gate.does_not_implement_wadh()
    assert gate.does_not_create_external_meaning()
    assert gate.does_not_issue_hukm()
    assert gate.does_not_raise_predicate_rank()
    assert gate.does_not_perform_semantic_interpretation()
    assert gate.does_not_implement_mutabaqah()
    assert gate.returns_governed_failures()
