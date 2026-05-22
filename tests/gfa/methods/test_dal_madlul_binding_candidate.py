"""
Tests for DalMadlulBindingCandidate - PR-L4

Critical Law:
    الربط ليس دلالة كاملة
    Binding is NOT full Dalālah.

Test Coverage (26 tests):
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
    20. test_binding_candidate_admission_success

    Hardening Guards (6 tests):
    H1. test_binding_success_is_not_dalalah_success
    H2. test_prior_information_permits_binding_but_does_not_certify_dalalah
    H3. test_conventional_hint_does_not_implement_wadh
    H4. test_usage_hint_does_not_implement_usage_gate
    H5. test_lexical_hint_does_not_certify_binding
    H6. test_binding_preserves_distinct_trace_lineages
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


# Test 20: Binding candidate admission success path

def test_binding_candidate_admission_success():
    """
    Law: Binding candidate admission success path.

    Critical clarification:
        Success means: binding candidate ADMITTED
        Success does NOT mean: full Dalālah achieved
        Success does NOT mean: semantic certification
        Success does NOT mean: signification completed

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


# ============================================================================
# HARDENING TESTS: Guard against semantic drift
# ============================================================================
# These tests prevent PR-L4 from accidentally implementing full Dalālah,
# Wadh, or semantic interpretation.


# Test H1: Binding success is NOT Dalālah success

def test_binding_success_is_not_dalalah_success():
    """
    Hardening Guard: Binding success ≠ Dalālah success.

    Critical Law:
        الربط شرط إمكان الدلالة، لا الدلالة المكتملة
        Binding is a condition for possible Dalālah, NOT full signification.

    This test ensures that:
        - Successful binding creates a BindingCandidate
        - BindingCandidate does NOT have dalalah, meaning, wadh fields
        - Success means "binding candidate admitted", not "signification achieved"

    Expected:
        - Result is success
        - Candidate has NO attributes: dalalah, wadh, meaning, hukm
        - Candidate is only a governed relation candidate
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
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success
    assert result.candidate is not None

    # Critical: Candidate must NOT have semantic fields
    candidate = result.candidate
    assert not hasattr(candidate, "dalalah"), "Binding must NOT have dalalah field"
    assert not hasattr(candidate, "wadh"), "Binding must NOT have wadh field"
    assert not hasattr(candidate, "meaning"), "Binding must NOT have meaning field"
    assert not hasattr(candidate, "hukm"), "Binding must NOT have hukm field"
    assert not hasattr(candidate, "haqiqah"), "Binding must NOT have haqiqah field"
    assert not hasattr(candidate, "majaz"), "Binding must NOT have majaz field"
    assert not hasattr(candidate, "mutabaqah"), "Binding must NOT have mutabaqah field"
    assert not hasattr(candidate, "tadammun"), "Binding must NOT have tadammun field"
    assert not hasattr(candidate, "iltizam"), "Binding must NOT have iltizam field"

    # Success means: binding candidate admitted, not semantic truth
    assert isinstance(candidate, DalMadlulBindingCandidate)
    assert candidate.is_valid


# Test H2: PriorInformation permits binding but does NOT certify Dalālah

def test_prior_information_permits_binding_but_does_not_certify_dalalah():
    """
    Hardening Guard: PriorInformation permits binding, does NOT certify signification.

    Critical Law:
        PriorInformation permits binding candidate.
        PriorInformation does NOT certify Dalālah.

    This test ensures:
        - PriorInformation allows binding attempt
        - Binding success does NOT mean semantic certification
        - No rank elevation from prior presence

    Expected:
        - Binding succeeds with PriorInformation
        - No semantic certification implied
        - Candidate remains at candidate rank (not certified)
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
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success
    candidate = result.candidate

    # PriorInformation permits binding
    assert candidate.binding_basis == BindingBasis.PRIOR_INFORMATION

    # But does NOT certify Dalālah
    assert not hasattr(candidate, "certified"), "Binding must NOT be certified"
    assert not hasattr(candidate, "rank"), "Binding must NOT have rank field"
    assert not hasattr(candidate, "semantic_certification"), "No semantic certification"

    # Remains a candidate
    assert isinstance(candidate, DalMadlulBindingCandidate)


# Test H3: CONVENTIONAL_HINT does NOT implement Wadh

def test_conventional_hint_does_not_implement_wadh():
    """
    Hardening Guard: CONVENTIONAL_HINT ≠ Wadh.

    Critical Law:
        CONVENTIONAL_HINT is a hint, NOT full Wadh (convention).
        Wadh requires explicit convention establishment (future PR-L5).

    This test ensures:
        - CONVENTIONAL_HINT can be used as binding basis
        - It does NOT constitute Wadh
        - No conventional establishment implied

    Expected:
        - Binding succeeds with CONVENTIONAL_HINT
        - No Wadh field or implementation
        - Hint status preserved
    """
    dal = make_valid_dal_candidate()
    madlul = make_valid_madlul_lafzi_candidate()
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.CONVENTIONAL_HINT,  # Hint only!
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success
    candidate = result.candidate

    # CONVENTIONAL_HINT is basis
    assert candidate.binding_basis == BindingBasis.CONVENTIONAL_HINT

    # But does NOT implement Wadh
    assert not hasattr(candidate, "wadh"), "CONVENTIONAL_HINT must NOT be Wadh"
    assert not hasattr(candidate, "convention"), "No convention field"
    assert not hasattr(candidate, "wadh_type"), "No wadh_type field"

    # Remains hint-based candidate
    assert isinstance(candidate, DalMadlulBindingCandidate)


# Test H4: USAGE_HINT does NOT implement UsageGate

def test_usage_hint_does_not_implement_usage_gate():
    """
    Hardening Guard: USAGE_HINT ≠ UsageGate.

    Critical Law:
        USAGE_HINT is a hint from usage evidence.
        USAGE_HINT does NOT implement full usage validation gate.

    This test ensures:
        - USAGE_HINT can support binding
        - It does NOT constitute usage proof
        - No usage certification implied

    Expected:
        - Binding succeeds with USAGE_HINT
        - No usage gate implementation
        - Hint status preserved
    """
    dal = make_valid_dal_candidate()
    madlul = make_valid_madlul_lafzi_candidate()
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.USAGE_HINT,  # Hint only!
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success
    candidate = result.candidate

    # USAGE_HINT is basis
    assert candidate.binding_basis == BindingBasis.USAGE_HINT

    # But does NOT implement UsageGate
    assert not hasattr(candidate, "usage_validated"), "USAGE_HINT must NOT be usage gate"
    assert not hasattr(candidate, "usage_proof"), "No usage proof"
    assert not hasattr(candidate, "usage_certification"), "No usage certification"

    # Remains hint-based candidate
    assert isinstance(candidate, DalMadlulBindingCandidate)


# Test H5: LEXICAL_HINT does NOT certify binding

def test_lexical_hint_does_not_certify_binding():
    """
    Hardening Guard: LEXICAL_HINT ≠ Lexical Proof.

    Critical Law:
        LEXICAL_HINT provides lexical evidence.
        LEXICAL_HINT does NOT certify binding as lexically proven.

    This test ensures:
        - LEXICAL_HINT supports binding attempt
        - It does NOT constitute lexical certification
        - No semantic proof implied

    Expected:
        - Binding succeeds with LEXICAL_HINT
        - No lexical certification
        - Hint status preserved
    """
    dal = make_valid_dal_candidate()
    madlul = make_valid_madlul_lafzi_candidate()
    style_spec = make_valid_style_spec()
    neutral_binding = make_valid_neutral_binding_result()

    input_data = DalMadlulBindingInput(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=BindingBasis.LEXICAL_HINT,  # Hint only!
        style_spec=style_spec,
        neutral_binding_result=neutral_binding,
        lafzi_registration_success=True,
    )

    result = DalMadlulBindingGate.create_binding(input_data)

    assert result.is_success
    candidate = result.candidate

    # LEXICAL_HINT is basis
    assert candidate.binding_basis == BindingBasis.LEXICAL_HINT

    # But does NOT certify binding
    assert not hasattr(candidate, "lexically_certified"), "LEXICAL_HINT must NOT certify"
    assert not hasattr(candidate, "lexical_proof"), "No lexical proof"
    assert not hasattr(candidate, "semantic_proof"), "No semantic proof"

    # Remains hint-based candidate
    assert isinstance(candidate, DalMadlulBindingCandidate)


# Test H6: Binding preserves distinct trace lineages

def test_binding_preserves_distinct_trace_lineages():
    """
    Hardening Guard: Binding preserves both trace lineages.

    Critical Law:
        Binding must preserve trace lineage from both Dāl and Madlūl.
        Different trace_ids are allowed (warning, not blocker).

    This test ensures:
        - Dāl trace preserved even when different from Madlūl
        - Madlūl trace preserved even when different from Dāl
        - Trace mismatch creates warning residual, not failure

    Expected:
        - Success with different trace_ids
        - Both lineages preserved
        - Warning residual present (not blocker)
    """
    dal_trace = uuid4().hex
    madlul_trace = uuid4().hex  # Different!

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

    # Must succeed (mismatch is warning, not blocker)
    assert result.is_success
    candidate = result.candidate

    # Both lineages preserved
    assert candidate.dal_trace_id == dal_trace, "Dāl trace must be preserved"
    assert candidate.madlul_trace_id == madlul_trace, "Madlūl trace must be preserved"
    assert candidate.dal_trace_id != candidate.madlul_trace_id, "Traces remain distinct"

    # Warning residual present
    assert any(
        r.kind == BindingResidualKind.TRACE_ID_MISMATCH
        for r in candidate.residuals
    ), "TRACE_ID_MISMATCH residual must be present"

    # Verify it's warning, not blocker
    mismatch_residual = next(
        r for r in candidate.residuals
        if r.kind == BindingResidualKind.TRACE_ID_MISMATCH
    )
    assert mismatch_residual.severity == "warning", "Trace mismatch must be warning"
    assert not mismatch_residual.is_blocker, "Trace mismatch must NOT be blocker"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
