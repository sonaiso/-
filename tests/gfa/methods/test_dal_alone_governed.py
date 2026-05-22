"""
Tests for DalGate - بوابة الدال

Critical Law:
    الدال وحده حامل لفظي مرشح، لا معنى
    Dāl-alone is a signifier candidate, not meaning, not Madlul, not Dalalah.

Test Coverage (15 Required Tests):
    1. test_dal_requires_lafzi_trace
    2. test_dal_requires_lafzi_registration
    3. test_dal_requires_lafzi_dalali_style
    4. test_dal_requires_neutral_binding
    5. test_dal_preserves_trace_id
    6. test_dal_preserves_residuals
    7. test_dal_does_not_create_meaning
    8. test_dal_does_not_create_madlul
    9. test_dal_does_not_create_dalalah
    10. test_dal_does_not_implement_wadh
    11. test_dal_does_not_issue_hukm
    12. test_dal_does_not_raise_predicate_rank
    13. test_unknown_dal_type_becomes_residual
    14. test_dal_returns_governed_failure_not_exception
    15. test_dal_full_success_path

Critical:
    DalCandidate is NOT meaning.
    DalCandidate is NOT Madlul.
    DalCandidate is NOT Dalalah.
    DalCandidate is a signifier carrier candidate.
"""

import pytest
from uuid import uuid4

from gfa.methods.lafzi_trace import (
    LafziTrace,
    LafziTraceType,
)
from gfa.methods.styles import (
    StyleSpec,
    ThinkingDomain,
    make_lafzi_dalali_style,
)
from gfa.methods.lafzi_dal import (
    DalType,
    DalCandidate,
    DalGate,
    DalResult,
    DalFailureKind,
)


# Test fixtures

def make_test_lafzi_trace(
    trace_id: str = None,
    trace_type: LafziTraceType = LafziTraceType.UNICODE,
    trace_content: str = "كَتَبَ"
) -> LafziTrace:
    """Create test LafziTrace."""
    if trace_id is None:
        trace_id = f"test_trace_{uuid4().hex[:8]}"

    return LafziTrace(
        trace_id=trace_id,
        trace_type=trace_type,
        trace_content=trace_content,
        residuals=(),
    )


def make_test_dal_gate(
    registration_successful: bool = True,
    neutral_binding_available: bool = True,
    use_lafzi_dalali_style: bool = True
) -> DalGate:
    """Create test DalGate with specified configuration."""
    if use_lafzi_dalali_style:
        style_spec = make_lafzi_dalali_style()
    else:
        # For negative test, use a different domain style
        from gfa.methods.styles import make_formal_logical_style
        style_spec = make_formal_logical_style()

    return DalGate(
        style_spec=style_spec,
        neutral_binding_available=neutral_binding_available,
        registration_successful=registration_successful,
    )


# Test 1: Requires LafziTrace

def test_dal_requires_lafzi_trace():
    """
    Law 1: No DalCandidate without LafziTrace.

    Test that DalGate requires LafziTrace input.
    """
    gate = make_test_dal_gate()

    # Process with None trace (should fail gracefully)
    result = gate.process_trace(None)

    assert result.is_failure
    assert result.failure is not None
    assert result.failure.residual.kind == DalFailureKind.MISSING_LAFZI_TRACE


# Test 2: Requires LafziMadlul registration

def test_dal_requires_lafzi_registration():
    """
    Law 2: No DalCandidate without LafziMadlul registration.

    Test that DalGate requires successful registration.
    """
    # Create gate without registration
    gate = make_test_dal_gate(registration_successful=False)

    assert not gate.verify_registration()

    # Process trace should fail
    trace = make_test_lafzi_trace()
    result = gate.process_trace(trace)

    assert result.is_failure
    assert result.failure.residual.kind == DalFailureKind.MISSING_REGISTRATION


# Test 3: Requires StyleSpec(LAFZI_DALALI)

def test_dal_requires_lafzi_dalali_style():
    """
    Law 3: No DalCandidate without StyleSpec(LAFZI_DALALI).

    Test that DalGate requires correct StyleSpec domain.
    """
    # Create gate with correct style
    gate = make_test_dal_gate(use_lafzi_dalali_style=True)
    assert gate.verify_style_spec()
    assert gate.style_spec.get_domain() == ThinkingDomain.LAFZI_DALALI

    # Create gate with wrong domain
    gate_wrong = make_test_dal_gate(use_lafzi_dalali_style=False)
    assert not gate_wrong.verify_style_spec()

    # Process should fail with wrong domain
    trace = make_test_lafzi_trace()
    result = gate_wrong.process_trace(trace)

    assert result.is_failure
    assert result.failure.residual.kind == DalFailureKind.WRONG_DOMAIN


# Test 4: Requires NeutralBinding

def test_dal_requires_neutral_binding():
    """
    Law 4: No DalCandidate without NeutralBinding.

    Test that DalGate requires NeutralBinding.
    """
    # Create gate without NeutralBinding
    gate = make_test_dal_gate(neutral_binding_available=False)

    assert not gate.verify_neutral_binding()

    # Process trace should fail
    trace = make_test_lafzi_trace()
    result = gate.process_trace(trace)

    assert result.is_failure
    assert result.failure.residual.kind == DalFailureKind.MISSING_NEUTRAL_BINDING


# Test 5: Preserves trace_id

def test_dal_preserves_trace_id():
    """
    Law 5: DalCandidate preserves trace_id.

    Test that trace_id is preserved through processing.
    """
    gate = make_test_dal_gate()

    trace_id = "test_dal_preserve_001"
    trace = make_test_lafzi_trace(trace_id=trace_id)
    result = gate.process_trace(trace)

    assert result.is_success
    assert result.candidate.trace_id == trace_id


# Test 6: Preserves residuals

def test_dal_preserves_residuals():
    """
    Law 6: DalCandidate preserves residuals.

    Test that residuals are preserved from LafziTrace.
    """
    gate = make_test_dal_gate()

    # Create trace with residual
    from gfa.methods.lafzi_trace import make_unknown_trace_type_residual
    trace = make_test_lafzi_trace()
    residual = make_unknown_trace_type_residual(trace.trace_id)
    trace_with_residual = trace.with_residual(residual)

    # Process
    result = gate.process_trace(trace_with_residual)

    assert result.is_success
    assert isinstance(result.candidate.residuals, tuple)
    assert len(result.candidate.residuals) >= 1
    assert gate.preserves_residuals()


# Test 7: Does not create meaning

def test_dal_does_not_create_meaning():
    """
    Law 7: DalCandidate does not create meaning.

    Test that DalCandidate does NOT create semantic meaning.
    """
    gate = make_test_dal_gate()

    # Verify no meaning creation
    assert gate.does_not_create_meaning()

    # Process trace
    trace = make_test_lafzi_trace(trace_content="قَرَأَ")
    result = gate.process_trace(trace)

    assert result.is_success

    # Candidate object has no 'meaning' attribute
    assert not hasattr(result.candidate, "meaning")
    assert not hasattr(result.candidate, "murad")
    assert not hasattr(result.candidate, "haqiqa_majaz")


# Test 8: Does not create Madlul

def test_dal_does_not_create_madlul():
    """
    Law 8: DalCandidate does not create Madlul.

    Test that DalCandidate does NOT implement Madlul (المدلول).
    """
    gate = make_test_dal_gate()

    # Verify no Madlul creation
    assert gate.does_not_create_madlul()

    # Process trace
    trace = make_test_lafzi_trace(trace_content="دَرَسَ")
    result = gate.process_trace(trace)

    assert result.is_success

    # Candidate has no Madlul attribute
    assert not hasattr(result.candidate, "madlul")
    assert not hasattr(result.candidate, "signified")
    assert not hasattr(result.candidate, "madlul_lafzi")


# Test 9: Does not create Dalalah

def test_dal_does_not_create_dalalah():
    """
    Law 9: DalCandidate does not create Dalalah.

    Test that DalCandidate does NOT implement Dalalah (الدلالة).
    """
    gate = make_test_dal_gate()

    # Verify no Dalalah creation
    assert gate.does_not_create_dalalah()

    # Process trace
    trace = make_test_lafzi_trace(trace_content="عَلِمَ")
    result = gate.process_trace(trace)

    assert result.is_success

    # Candidate has no Dalalah attribute
    assert not hasattr(result.candidate, "dalalah")
    assert not hasattr(result.candidate, "signification")
    assert not hasattr(result.candidate, "dalalah_wadia")


# Test 10: Does not implement Wadh

def test_dal_does_not_implement_wadh():
    """
    Law 10: DalCandidate does not implement Wadh.

    Test that DalCandidate does NOT implement Wadh (الوضع).
    """
    gate = make_test_dal_gate()

    # Verify no Wadh implementation
    assert gate.does_not_implement_wadh()

    # Process trace
    trace = make_test_lafzi_trace(trace_content="فَهِمَ")
    result = gate.process_trace(trace)

    assert result.is_success

    # Candidate has no Wadh attribute
    assert not hasattr(result.candidate, "wadh")
    assert not hasattr(result.candidate, "conventional_placement")
    assert not hasattr(result.candidate, "arbitrary_assignment")


# Test 11: Does not issue HUKM

def test_dal_does_not_issue_hukm():
    """
    Law 11: DalCandidate does not issue HUKM.

    Test that DalCandidate does NOT issue judgment.
    """
    gate = make_test_dal_gate()

    # Verify no HUKM issuance
    assert gate.does_not_issue_hukm()

    # Process trace
    trace = make_test_lafzi_trace(trace_content="حَكَمَ")
    result = gate.process_trace(trace)

    assert result.is_success

    # Candidate has no HUKM attribute
    assert not hasattr(result.candidate, "hukm")
    assert not hasattr(result.candidate, "judgment")
    assert not hasattr(result.candidate, "certification")


# Test 12: Does not raise PredicateRank

def test_dal_does_not_raise_predicate_rank():
    """
    Law 12: DalCandidate does not raise PredicateRank.

    Test that DalCandidate does NOT inflate predicate rank.
    """
    gate = make_test_dal_gate()

    # Verify no rank inflation
    assert gate.does_not_raise_predicate_rank()

    # Process trace
    trace = make_test_lafzi_trace(trace_content="رَتَبَ")
    result = gate.process_trace(trace)

    assert result.is_success

    # Candidate has no rank attribute
    assert not hasattr(result.candidate, "predicate_rank")
    assert not hasattr(result.candidate, "certification_level")
    assert not hasattr(result.candidate, "rank_elevation")


# Test 13: UNKNOWN signifier type becomes residual

def test_unknown_dal_type_becomes_residual():
    """
    Law 13: UNKNOWN signifier type becomes residual, not exception.

    Test that UNKNOWN signifier type is handled gracefully as residual.
    """
    gate = make_test_dal_gate()

    # Process UNKNOWN trace type
    trace = make_test_lafzi_trace(
        trace_id="test_unknown_dal_001",
        trace_type=LafziTraceType.UNKNOWN,
        trace_content="[unknown_format]",
    )

    result = gate.process_trace(trace)

    # Should still succeed (not raise exception)
    assert result.is_success

    # But should have residual
    assert result.candidate.has_residuals
    assert len(result.candidate.residuals) >= 1

    # Should map to UNKNOWN_SIGNIFIER
    assert result.candidate.dal_type == DalType.UNKNOWN_SIGNIFIER

    # Should have UNKNOWN_DAL_TYPE residual
    dal_residuals = [r for r in result.candidate.residuals
                     if hasattr(r, 'kind') and r.kind == DalFailureKind.UNKNOWN_DAL_TYPE]
    assert len(dal_residuals) == 1
    assert "UNKNOWN" in dal_residuals[0].reason


# Test 14: Returns governed failure, not exception

def test_dal_returns_governed_failure_not_exception():
    """
    Law 14: DalGate returns governed failure, not exception.

    When requirements not met, should return DalFailure,
    not raise Python exception.
    """
    # Test with missing registration
    gate = make_test_dal_gate(registration_successful=False)
    trace = make_test_lafzi_trace()
    result = gate.process_trace(trace)

    # Should return failure, not raise exception
    assert result.is_failure
    assert result.failure is not None
    assert result.failure.residual.kind == DalFailureKind.MISSING_REGISTRATION

    # Test with missing NeutralBinding
    gate2 = make_test_dal_gate(neutral_binding_available=False)
    result2 = gate2.process_trace(trace)

    assert result2.is_failure
    assert result2.failure.residual.kind == DalFailureKind.MISSING_NEUTRAL_BINDING


# Test 15: Full success path

def test_dal_full_success_path():
    """
    Integration test: Full successful DalCandidate processing.

    Tests complete flow:
        1. LafziTrace input
        2. DalGate verification
        3. DalCandidate creation
        4. Result validation
    """
    # Step 1: Create LafziTrace
    trace = make_test_lafzi_trace(
        trace_id="integration_dal_001",
        trace_type=LafziTraceType.UNICODE,
        trace_content="الْحَمْدُ لِلَّهِ",
    )

    # Step 2: Create gate with all requirements
    gate = make_test_dal_gate()

    # Step 3: Process trace
    result = gate.process_trace(trace)

    # Step 4: Validate result
    assert result.is_success
    assert result.candidate is not None
    assert result.candidate.trace_id == "integration_dal_001"
    assert result.candidate.signifier_form == "الْحَمْدُ لِلَّهِ"
    assert result.candidate.dal_type == DalType.WRITTEN_SIGNIFIER
    assert result.candidate.is_valid

    # Verify all laws satisfied
    assert gate.verify_registration()
    assert gate.verify_style_spec()
    assert gate.verify_neutral_binding()
    assert gate.preserves_trace_id(result.candidate.trace_id)
    assert gate.preserves_residuals()
    assert gate.does_not_create_meaning()
    assert gate.does_not_create_madlul()
    assert gate.does_not_create_dalalah()
    assert gate.does_not_implement_wadh()
    assert gate.does_not_issue_hukm()
    assert gate.does_not_raise_predicate_rank()


# Additional integration tests

def test_dal_type_mapping_from_trace_types():
    """
    Test that all LafziTraceType values map correctly to DalType.

    Verifies the trace type → signifier type mapping is complete.
    """
    gate = make_test_dal_gate()

    mappings = [
        (LafziTraceType.ACOUSTIC, DalType.SOUND_SIGNIFIER),
        (LafziTraceType.WRITTEN, DalType.WRITTEN_SIGNIFIER),
        (LafziTraceType.UNICODE, DalType.WRITTEN_SIGNIFIER),
        (LafziTraceType.ORTHOGRAPHIC, DalType.ORTHOGRAPHIC_SIGNIFIER),
        (LafziTraceType.PHONOLOGICAL, DalType.SOUND_SIGNIFIER),
        (LafziTraceType.SYMBOLIC, DalType.SYMBOLIC_SIGNIFIER),
        (LafziTraceType.UNKNOWN, DalType.UNKNOWN_SIGNIFIER),
    ]

    for trace_type, expected_dal_type in mappings:
        trace = make_test_lafzi_trace(trace_type=trace_type)
        result = gate.process_trace(trace)

        assert result.is_success
        assert result.candidate.dal_type == expected_dal_type


def test_dal_candidate_immutability():
    """
    Test that DalCandidate is immutable (frozen dataclass).

    This ensures lineage integrity and trace preservation.
    """
    trace = make_test_lafzi_trace()
    gate = make_test_dal_gate()
    result = gate.process_trace(trace)

    assert result.is_success
    candidate = result.candidate

    # Attempt to modify should raise error
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        candidate.trace_id = "modified"

    with pytest.raises(Exception):
        candidate.signifier_form = "modified"

    with pytest.raises(Exception):
        candidate.dal_type = DalType.SOUND_SIGNIFIER


def test_dal_residual_preservation_chain():
    """
    Test that residuals are preserved through the chain:
    LafziTrace → DalCandidate

    This ensures no information loss in the processing pipeline.
    """
    from gfa.methods.lafzi_trace import LafziTraceResidual, LafziTraceFailureKind

    gate = make_test_dal_gate()

    # Create trace with multiple residuals
    trace = make_test_lafzi_trace()

    residual1 = LafziTraceResidual(
        kind=LafziTraceFailureKind.UNKNOWN_TRACE_TYPE,
        reason="Test residual 1",
        violated_law="Test law 1",
        trace_id=trace.trace_id,
    )

    trace = trace.with_residual(residual1)

    # Process through DalGate
    result = gate.process_trace(trace)

    assert result.is_success
    assert len(result.candidate.residuals) >= 1

    # Original residual should be preserved
    assert residual1 in result.candidate.residuals
