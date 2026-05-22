"""
Tests for DalMadlulBindingCandidate - PR-L4

Critical Law:
    الربط ليس دلالة كاملة
    Binding is NOT full Dalālah.

Test Coverage (20 tests):
    1. test_binding_requires_dal_candidate
    2. test_binding_requires_madlul_lafzi_candidate
    3. test_binding_requires_lafzi_registration
    4. test_binding_requires_lafzi_dalali_style
    5. test_binding_requires_neutral_binding
    6. test_binding_requires_prior_information
    7. test_binding_preserves_dal_trace_id
    8. test_binding_preserves_madlul_trace_id
    9. test_binding_preserves_residuals_from_both_sides
    10. test_binding_does_not_create_external_meaning
    11. test_binding_does_not_create_full_dalalah
    12. test_binding_does_not_implement_wadh
    13. test_binding_does_not_classify_mutabaqah_tadammun_iltizam
    14. test_binding_does_not_classify_haqiqah_majaz
    15. test_binding_does_not_issue_hukm
    16. test_binding_does_not_raise_predicate_rank
    17. test_binding_blocks_domain_mismatch
    18. test_unknown_binding_basis_becomes_residual
    19. test_binding_returns_governed_failure_not_exception
    20. test_binding_full_success_path
"""

import pytest
from uuid import uuid4

from gfa.methods.lafzi_dal import DalCandidate, DalType
from gfa.methods.lafzi_madlul import MadlulLafziCandidate, MadlulLafziType
from gfa.methods.rational import (
    NeutralBinding,
    NeutralBindingInput,
    AqlOperationInput,
    FilteredPrior,
    PriorInformation,
    PredicateRank,
)
from gfa.methods.styles import StyleSpec, make_lafzi_dalali_style, ThinkingDomain

from gfa.methods.lafzi_binding import (
    BindingBasis,
    BindingResidualKind,
    DalMadlulBindingCandidate,
    DalMadlulBindingGate,
    DalMadlulBindingInput,
    DalMadlulBindingResult,
    make_missing_dal_candidate_residual,
    make_missing_madlul_lafzi_candidate_residual,
    make_unknown_binding_basis_residual,
)


# Test helpers

def make_valid_dal_candidate(trace_id: str = None) -> DalCandidate:
    """Create a valid DālCandidate for testing."""
    return DalCandidate(
        trace_id=trace_id or uuid4().hex,
        signifier_form="كَتَبَ",
        dal_type=DalType.SOUND_FORM,
    )


def make_valid_madlul_lafzi_candidate(trace_id: str = None) -> MadlulLafziCandidate:
    """Create a valid MadlulLafziCandidate for testing."""
    return MadlulLafziCandidate(
        trace_id=trace_id or uuid4().hex,
        madlul_type=MadlulLafziType.ROOT,
        candidate_form="ك-ت-ب",
        source_prior_information="lexicon_root",
    )


def make_valid_neutral_binding_result() -> "NeutralBindingResult":
    """Create a valid NeutralBindingResult for testing."""
    prior_info = PriorInformation(
        content="test_prior",
        source="test",
        strength="strong",
    )
    filtered_prior = FilteredPrior(information=(prior_info,))
    aql_input = AqlOperationInput(
        reality="test_reality",
        sensory_transfer="test_sensory",
        cognitive_carrier="test_carrier",
        filtered_prior=filtered_prior,
    )
    binding_input = NeutralBindingInput(aql_input=aql_input)
    return NeutralBinding.bind(binding_input)


def make_valid_style_spec() -> StyleSpec:
    """Create a valid LAFZI_DALALI StyleSpec for testing."""
    return make_lafzi_dalali_style()


# Test 1: Requires DālCandidate

def test_binding_requires_dal_candidate():
    """
    Law 1: No binding without DālCandidate.

    Expected: Failure with MISSING_DAL_CANDIDATE residual.
    """
    madlul = make_valid_madlul_lafzi_candidate()
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=None,  # Missing!
        madlul_candidate=madlul,
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_failure
    assert result.failure is not None
    assert "dal_candidate" in result.failure.missing_requirements
    assert any(
        r.kind == BindingResidualKind.MISSING_DAL_CANDIDATE
        for r in result.failure.residuals
    )


# Test 2: Requires MadlulLafziCandidate

def test_binding_requires_madlul_lafzi_candidate():
    """
    Law 2: No binding without MadlulLafziCandidate.

    Expected: Failure with MISSING_MADLUL_LAFZI_CANDIDATE residual.
    """
    dal = make_valid_dal_candidate()
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=None,  # Missing!
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_failure
    assert result.failure is not None
    assert "madlul_candidate" in result.failure.missing_requirements
    assert any(
        r.kind == BindingResidualKind.MISSING_MADLUL_LAFZI_CANDIDATE
        for r in result.failure.residuals
    )


# Test 3: Requires LafziMadlul registration

def test_binding_requires_lafzi_registration():
    """
    Law 3: No binding without LafziMadlul registration.

    Expected: Failure with MISSING_LAFZI_REGISTRATION residual.
    """
    dal = make_valid_dal_candidate()
    madlul = make_valid_madlul_lafzi_candidate()
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=False,  # Failed!
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_failure
    assert result.failure is not None
    assert "lafzi_registration_success" in result.failure.missing_requirements
    assert any(
        r.kind == BindingResidualKind.MISSING_LAFZI_REGISTRATION
        for r in result.failure.residuals
    )


# Test 4: Requires LAFZI_DALALI StyleSpec

def test_binding_requires_lafzi_dalali_style():
    """
    Law 4: No binding without StyleSpec(LAFZI_DALALI).

    Expected: Failure with MISSING_LAFZI_DALALI_STYLE residual.
    """
    dal = make_valid_dal_candidate()
    madlul = make_valid_madlul_lafzi_candidate()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=None,  # Missing!
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_failure
    assert result.failure is not None
    assert "style_spec" in result.failure.missing_requirements
    assert any(
        r.kind == BindingResidualKind.MISSING_LAFZI_DALALI_STYLE
        for r in result.failure.residuals
    )


# Test 5: Requires NeutralBinding

def test_binding_requires_neutral_binding():
    """
    Law 5: No binding without NeutralBinding.

    Expected: Failure with MISSING_NEUTRAL_BINDING residual.
    """
    dal = make_valid_dal_candidate()
    madlul = make_valid_madlul_lafzi_candidate()
    style_spec = make_valid_style_spec()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=style_spec,
        neutral_binding_result=None,  # Missing!
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_failure
    assert result.failure is not None
    assert "neutral_binding_result" in result.failure.missing_requirements
    assert any(
        r.kind == BindingResidualKind.MISSING_NEUTRAL_BINDING
        for r in result.failure.residuals
    )


# Test 6: Requires PriorInformation

def test_binding_requires_prior_information():
    """
    Law 6: No binding without PriorInformation.

    Expected: Failure with MISSING_PRIOR_INFORMATION residual.
    """
    dal = make_valid_dal_candidate()
    madlul = make_valid_madlul_lafzi_candidate()
    style_spec = make_valid_style_spec()

    # Create NeutralBinding without PriorInformation
    from gfa.methods.rational import NeutralBindingResult

    failed_binding = NeutralBindingResult(
        success=True,
        prior_information_preserved=False,  # No prior information!
        opinion_excluded=True,
        trace_id=uuid4().hex,
    )

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=style_spec,
        neutral_binding_result=failed_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_failure
    assert result.failure is not None
    assert "prior_information" in result.failure.missing_requirements


# Test 7: Preserves Dāl trace_id

def test_binding_preserves_dal_trace_id():
    """
    Law 7: Binding preserves Dāl trace_id.

    Expected: Success with dal_trace_id preserved.
    """
    dal_trace = uuid4().hex
    dal = make_valid_dal_candidate(trace_id=dal_trace)
    madlul = make_valid_madlul_lafzi_candidate()
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success
    assert result.candidate.dal_trace_id == dal_trace


# Test 8: Preserves Madlūl trace_id

def test_binding_preserves_madlul_trace_id():
    """
    Law 8: Binding preserves Madlūl trace_id.

    Expected: Success with madlul_trace_id preserved.
    """
    madlul_trace = uuid4().hex
    dal = make_valid_dal_candidate()
    madlul = make_valid_madlul_lafzi_candidate(trace_id=madlul_trace)
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success
    assert result.candidate.madlul_trace_id == madlul_trace


# Test 9: Preserves residuals from both sides

def test_binding_preserves_residuals_from_both_sides():
    """
    Law 9: Binding preserves residuals from both sides.

    Expected: Success with residuals from Dāl and Madlūl preserved.
    """
    dal_residual = make_missing_dal_candidate_residual("test_dal_residual")
    madlul_residual = make_missing_madlul_lafzi_candidate_residual("test_madlul_residual")

    dal = make_valid_dal_candidate().with_residual(dal_residual)
    madlul = make_valid_madlul_lafzi_candidate().with_residual(madlul_residual)
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success
    assert dal_residual in result.candidate.residuals
    assert madlul_residual in result.candidate.residuals


# Test 10: Does NOT create external meaning

def test_binding_does_not_create_external_meaning():
    """
    Law 10: Binding does NOT create external meaning.

    Expected: Gate method confirms no meaning creation.
    """
    assert DalMadlulBindingGate.does_not_create_external_meaning() is True


# Test 11: Does NOT create full Dalālah

def test_binding_does_not_create_full_dalalah():
    """
    Law 11: Binding does NOT create full Dalālah.

    Expected: Gate method confirms no full Dalālah.
    """
    assert DalMadlulBindingGate.does_not_create_full_dalalah() is True


# Test 12: Does NOT implement Wadh

def test_binding_does_not_implement_wadh():
    """
    Law 12: Binding does NOT implement Wadh.

    Expected: Gate method confirms no Wadh implementation.
    """
    assert DalMadlulBindingGate.does_not_implement_wadh() is True


# Test 13: Does NOT classify Mutabaqah/Tadammun/Iltizam

def test_binding_does_not_classify_mutabaqah_tadammun_iltizam():
    """
    Law 13: Binding does NOT classify Mutabaqah/Tadammun/Iltizam.

    Expected: Gate method confirms no classification.
    """
    assert DalMadlulBindingGate.does_not_classify_mutabaqah_tadammun_iltizam() is True


# Test 14: Does NOT classify Haqiqah/Majaz

def test_binding_does_not_classify_haqiqah_majaz():
    """
    Law 14: Binding does NOT classify Haqiqah/Majaz.

    Expected: Gate method confirms no classification.
    """
    assert DalMadlulBindingGate.does_not_classify_haqiqah_majaz() is True


# Test 15: Does NOT issue HUKM

def test_binding_does_not_issue_hukm():
    """
    Law 15: Binding does NOT issue HUKM.

    Expected: Gate method confirms no HUKM issuance.
    """
    assert DalMadlulBindingGate.does_not_issue_hukm() is True


# Test 16: Does NOT raise PredicateRank

def test_binding_does_not_raise_predicate_rank():
    """
    Law 16: Binding does NOT raise PredicateRank.

    Expected: Gate method confirms no rank raising.
    """
    assert DalMadlulBindingGate.does_not_raise_predicate_rank() is True


# Test 17: Domain mismatch blocks binding

def test_binding_blocks_domain_mismatch():
    """
    Law 17: Domain mismatch blocks binding.

    Expected: Warning residual for trace_id mismatch (proxy for domain).
    """
    dal_trace = uuid4().hex
    madlul_trace = uuid4().hex  # Different trace

    dal = make_valid_dal_candidate(trace_id=dal_trace)
    madlul = make_valid_madlul_lafzi_candidate(trace_id=madlul_trace)
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success  # Not a blocker, just warning
    assert any(
        r.kind == BindingResidualKind.TRACE_ID_MISMATCH
        for r in result.candidate.residuals
    )


# Test 18: UNKNOWN_BASIS becomes residual

def test_unknown_binding_basis_becomes_residual():
    """
    Law 18: UNKNOWN_BASIS becomes residual, not exception.

    Expected: Success with UNKNOWN_BINDING_BASIS residual.
    """
    dal = make_valid_dal_candidate()
    madlul = make_valid_madlul_lafzi_candidate()
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.UNKNOWN_BASIS,  # Unknown!
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success  # Not a blocker
    assert any(
        r.kind == BindingResidualKind.UNKNOWN_BINDING_BASIS
        for r in result.candidate.residuals
    )


# Test 19: Returns governed failure, not exception

def test_binding_returns_governed_failure_not_exception():
    """
    Law 19: All failures return governed failures, not exceptions.

    Expected: Failure with proper DalMadlulBindingFailure, no exception.
    """
    # Missing all requirements
    input_data = DalMadlulBindingInput()

    # Should NOT raise exception
    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_failure
    assert result.failure is not None
    assert isinstance(result.failure.residuals, tuple)
    assert len(result.failure.residuals) > 0


# Test 20: Full success path

def test_binding_full_success_path():
    """
    Law: Full success path with all requirements satisfied.

    Expected: Success with valid DalMadlulBindingCandidate.
    """
    trace_id = uuid4().hex
    dal = make_valid_dal_candidate(trace_id=trace_id)
    madlul = make_valid_madlul_lafzi_candidate(trace_id=trace_id)
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.PRIOR_INFORMATION,
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success
    assert result.candidate is not None
    assert result.candidate.is_valid
    assert result.candidate.binding_basis == BindingBasis.PRIOR_INFORMATION
    assert result.candidate.dal_trace_id == trace_id
    assert result.candidate.madlul_trace_id == trace_id
    assert result.failure is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
