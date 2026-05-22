"""
Tests for LafziTrace Gate - بوابة الأثر اللفظي

Critical Law:
    لا مدلول لفظي بلا أثر لفظي
    No LafziMadlul execution without LafziTrace.

Test Coverage (14 Required Tests):
    1. test_lafzi_trace_requires_lafzi_registration
    2. test_lafzi_trace_requires_lafzi_dalali_style
    3. test_lafzi_trace_requires_neutral_binding
    4. test_lafzi_trace_requires_prior_information
    5. test_lafzi_trace_preserves_trace_id
    6. test_lafzi_trace_preserves_residuals
    7. test_lafzi_trace_does_not_create_meaning
    8. test_lafzi_trace_does_not_issue_hukm
    9. test_lafzi_trace_does_not_create_dal
    10. test_lafzi_trace_does_not_create_madlul
    11. test_lafzi_trace_does_not_create_dalalah
    12. test_lafzi_trace_does_not_raise_predicate_rank
    13. test_unknown_lafzi_trace_type_becomes_residual
    14. test_lafzi_trace_returns_governed_failure_not_exception

Critical:
    Registration is NOT execution.
    LafziTrace is NOT meaning.
    LafziTrace is a condition for linguistic processing.
"""

import pytest
from uuid import uuid4

from gfa.methods.rational import (
    NeutralBindingInput,
    AqlOperationInput,
    FilteredPrior,
    PriorInformation,
)
from gfa.methods.styles import (
    StyleSpec,
    ThinkingDomain,
    make_lafzi_dalali_style,
)
from gfa.methods.lafzi_registration import (
    LafziGovernanceContract,
    LafziStyleRegistration,
)
from gfa.methods.lafzi_trace import (
    LafziTraceType,
    LafziTrace,
    LafziTraceGate,
    LafziTraceResult,
    LafziTraceFailureKind,
)


# Test fixtures

def make_test_prior_information() -> PriorInformation:
    """Create test prior information."""
    return PriorInformation(
        content="كَتَبَ - test linguistic trace",
        domain="lafzi_dalali",
        rank="LICENSED",
        evidence_trace="lexicon_source",
        trace_id=uuid4().hex,
    )


def make_test_filtered_prior() -> FilteredPrior:
    """Create test filtered prior with information."""
    info = make_test_prior_information()
    return FilteredPrior(
        information=frozenset([info]),
        excluded_opinions=frozenset(),
    )


def make_test_aql_input() -> AqlOperationInput:
    """Create test AqlOperationInput."""
    filtered_prior = make_test_filtered_prior()
    return AqlOperationInput(
        reality="test_reality",
        sensory_transfer="test_sensory",
        cognitive_carrier="test_carrier",
        filtered_prior=filtered_prior,
    )


def make_test_neutral_binding_input() -> NeutralBindingInput:
    """Create test NeutralBindingInput."""
    aql_input = make_test_aql_input()
    return NeutralBindingInput(
        aql_input=aql_input,
        trace_id="test_trace_001",
        residuals=(),
    )


def make_test_lafzi_registration():
    """Create successful LafziMadlul registration."""
    # Create StyleSpec for LAFZI_DALALI using factory function
    style_spec = make_lafzi_dalali_style()

    # Create NeutralBindingInput
    binding_input = make_test_neutral_binding_input()

    # Register using class method
    result = LafziStyleRegistration.register(
        style_spec=style_spec,
        neutral_binding_input=binding_input,
    )

    assert result.success, "Registration must succeed for tests"
    return result


# Test 1: Requires LafziMadlul registration

def test_lafzi_trace_requires_lafzi_registration():
    """
    Law 1: No LafziTrace without LafziMadlul registration.

    Test that LafziTraceGate requires successful registration.
    """
    # Get successful registration
    registration_result = make_test_lafzi_registration()

    # Create gate (should succeed)
    gate = LafziTraceGate(registration_result)

    # Verify registration requirement
    assert gate.verify_registration()

    # Process trace should succeed
    result = gate.process_trace(
        trace_id="test_trace_002",
        trace_type=LafziTraceType.UNICODE,
        trace_content="كَتَبَ",
    )

    assert result.is_success


# Test 2: Requires StyleSpec(LAFZI_DALALI)

def test_lafzi_trace_requires_lafzi_dalali_style():
    """
    Law 2: No LafziTrace without StyleSpec(LAFZI_DALALI).

    Test that LafziTraceGate requires correct StyleSpec domain.
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Verify StyleSpec requirement
    assert gate.verify_style_spec()
    assert gate.style_spec.get_domain() == ThinkingDomain.LAFZI_DALALI


# Test 3: Requires NeutralBinding

def test_lafzi_trace_requires_neutral_binding():
    """
    Law 3: No LafziTrace without NeutralBinding.

    Test that LafziTraceGate requires NeutralBinding.
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Verify NeutralBinding requirement
    assert gate.verify_neutral_binding()
    assert gate.neutral_binding_input is not None


# Test 4: Requires PriorInformation

def test_lafzi_trace_requires_prior_information():
    """
    Law 4: No LafziTrace without PriorInformation.

    Test that LafziTraceGate requires PriorInformation.
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Verify PriorInformation requirement
    assert gate.verify_prior_information()


# Test 5: Preserves trace_id

def test_lafzi_trace_preserves_trace_id():
    """
    Law 5: LafziTrace preserves trace_id.

    Test that trace_id is preserved through processing.
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    trace_id = "test_trace_preserve_001"
    result = gate.process_trace(
        trace_id=trace_id,
        trace_type=LafziTraceType.WRITTEN,
        trace_content="الكتاب",
    )

    assert result.is_success
    assert result.trace.trace_id == trace_id


# Test 6: Preserves residuals

def test_lafzi_trace_preserves_residuals():
    """
    Law 6: LafziTrace preserves residuals.

    Test that residuals are preserved.
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Verify residuals preservation
    assert gate.preserves_residuals()

    # Process successful trace (no residuals initially)
    result = gate.process_trace(
        trace_id="test_trace_003",
        trace_type=LafziTraceType.PHONOLOGICAL,
        trace_content="/kataba/",
    )

    assert result.is_success
    assert isinstance(result.trace.residuals, tuple)


# Test 7: Does not create meaning

def test_lafzi_trace_does_not_create_meaning():
    """
    Law 7: LafziTrace does not create meaning.

    Test that LafziTrace does NOT create semantic meaning.
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Verify no meaning creation
    assert gate.does_not_create_meaning()

    # Process trace
    result = gate.process_trace(
        trace_id="test_trace_004",
        trace_type=LafziTraceType.UNICODE,
        trace_content="قَرَأَ",
    )

    assert result.is_success

    # Trace object has no 'meaning' attribute
    assert not hasattr(result.trace, "meaning")
    assert not hasattr(result.trace, "murad")
    assert not hasattr(result.trace, "haqiqa_majaz")


# Test 8: Does not issue HUKM

def test_lafzi_trace_does_not_issue_hukm():
    """
    Law 8: LafziTrace does not issue HUKM.

    Test that LafziTrace does NOT issue judgment.
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Verify no HUKM issuance
    assert gate.does_not_issue_hukm()

    result = gate.process_trace(
        trace_id="test_trace_005",
        trace_type=LafziTraceType.ORTHOGRAPHIC,
        trace_content="كتب",
    )

    assert result.is_success

    # Trace has no HUKM attribute
    assert not hasattr(result.trace, "hukm")
    assert not hasattr(result.trace, "judgment")
    assert not hasattr(result.trace, "certification")


# Test 9: Does not create Dal

def test_lafzi_trace_does_not_create_dal():
    """
    Law 9: LafziTrace does not create Dal.

    Test that LafziTrace does NOT implement Dal (الدال).
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Verify no Dal creation
    assert gate.does_not_create_dal()

    result = gate.process_trace(
        trace_id="test_trace_006",
        trace_type=LafziTraceType.ACOUSTIC,
        trace_content="[kataba_audio]",
    )

    assert result.is_success

    # Trace has no Dal attribute
    assert not hasattr(result.trace, "dal")
    assert not hasattr(result.trace, "signifier")


# Test 10: Does not create Madlul

def test_lafzi_trace_does_not_create_madlul():
    """
    Law 10: LafziTrace does not create Madlul.

    Test that LafziTrace does NOT implement Madlul (المدلول).
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Verify no Madlul creation
    assert gate.does_not_create_madlul()

    result = gate.process_trace(
        trace_id="test_trace_007",
        trace_type=LafziTraceType.SYMBOLIC,
        trace_content="KTB",
    )

    assert result.is_success

    # Trace has no Madlul attribute
    assert not hasattr(result.trace, "madlul")
    assert not hasattr(result.trace, "signified")


# Test 11: Does not create Dalalah

def test_lafzi_trace_does_not_create_dalalah():
    """
    Law 11: LafziTrace does not create Dalalah.

    Test that LafziTrace does NOT implement Dalalah (الدلالة).
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Verify no Dalalah creation
    assert gate.does_not_create_dalalah()

    result = gate.process_trace(
        trace_id="test_trace_008",
        trace_type=LafziTraceType.UNICODE,
        trace_content="دَرَسَ",
    )

    assert result.is_success

    # Trace has no Dalalah attribute
    assert not hasattr(result.trace, "dalalah")
    assert not hasattr(result.trace, "signification")
    assert not hasattr(result.trace, "wadh")


# Test 12: Does not raise PredicateRank

def test_lafzi_trace_does_not_raise_predicate_rank():
    """
    Law 12: LafziTrace does not raise PredicateRank.

    Test that LafziTrace does NOT inflate predicate rank.
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Verify no rank inflation
    assert gate.does_not_raise_predicate_rank()

    result = gate.process_trace(
        trace_id="test_trace_009",
        trace_type=LafziTraceType.WRITTEN,
        trace_content="الكِتَابُ",
    )

    assert result.is_success

    # Trace has no rank attribute
    assert not hasattr(result.trace, "predicate_rank")
    assert not hasattr(result.trace, "certification_level")


# Test 13: UNKNOWN trace type becomes residual

def test_unknown_lafzi_trace_type_becomes_residual():
    """
    Law 13: UNKNOWN trace type becomes residual, not exception.

    Test that UNKNOWN trace type is handled gracefully as residual.
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Process UNKNOWN trace type
    result = gate.process_trace(
        trace_id="test_trace_unknown_001",
        trace_type=LafziTraceType.UNKNOWN,
        trace_content="[unknown_format]",
    )

    # Should still succeed (not raise exception)
    assert result.is_success

    # But should have residual
    assert result.trace.has_residuals
    assert len(result.trace.residuals) == 1

    # Residual should be UNKNOWN_TRACE_TYPE
    residual = result.trace.residuals[0]
    assert residual.kind == LafziTraceFailureKind.UNKNOWN_TRACE_TYPE
    assert "UNKNOWN" in residual.reason


# Test 14: Returns governed failure, not exception

def test_lafzi_trace_returns_governed_failure_not_exception():
    """
    Test that LafziTrace returns governed failures, not bare exceptions.

    When requirements not met, should return LafziTraceFailure,
    not raise Python exception.
    """
    registration_result = make_test_lafzi_registration()
    gate = LafziTraceGate(registration_result)

    # Process with missing trace_id (should fail gracefully)
    result = gate.process_trace(
        trace_id=None,  # Missing trace_id
        trace_type=LafziTraceType.UNICODE,
        trace_content="test",
    )

    # Should return failure, not raise exception
    assert result.is_failure
    assert result.failure is not None
    assert result.failure.residual.kind == LafziTraceFailureKind.TRACE_NOT_PRESERVED


# Integration test: Full success path

def test_lafzi_trace_full_success_path():
    """
    Integration test: Full successful LafziTrace processing.

    Tests complete flow:
        1. LafziMadlul registration
        2. LafziTraceGate creation
        3. Trace processing
        4. Result validation
    """
    # Step 1: Register LafziMadlul
    registration_result = make_test_lafzi_registration()
    assert registration_result.success

    # Step 2: Create trace gate
    gate = LafziTraceGate(registration_result)

    # Step 3: Process trace
    result = gate.process_trace(
        trace_id="integration_test_001",
        trace_type=LafziTraceType.UNICODE,
        trace_content="الْحَمْدُ لِلَّهِ",
    )

    # Step 4: Validate result
    assert result.is_success
    assert result.trace is not None
    assert result.trace.trace_id == "integration_test_001"
    assert result.trace.trace_type == LafziTraceType.UNICODE
    assert result.trace.trace_content == "الْحَمْدُ لِلَّهِ"
    assert result.trace.is_valid

    # Verify all laws satisfied
    assert gate.verify_registration()
    assert gate.verify_style_spec()
    assert gate.verify_neutral_binding()
    assert gate.verify_prior_information()
    assert gate.preserves_trace_id(result.trace.trace_id)
    assert gate.preserves_residuals()
    assert gate.does_not_create_meaning()
    assert gate.does_not_issue_hukm()
    assert gate.does_not_create_dal()
    assert gate.does_not_create_madlul()
    assert gate.does_not_create_dalalah()
    assert gate.does_not_raise_predicate_rank()
