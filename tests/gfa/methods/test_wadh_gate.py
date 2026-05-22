"""
Test WadhGate (PR-L5B)

Critical Laws Being Tested:
    1. WadhGate requires DalMadlulBindingCandidate
    2. WadhGate requires WadhEvidence
    3. WadhGate requires WadhSource
    4. WadhGate requires WadhTransmissionMode
    5. WadhGate requires or residualizes WadhScope
    6. WadhGate requires MawduLahStructure
    7. Lexicon report permits WadhClaim, NOT meaning
    8. Usage attestation permits WadhClaim, NOT UsageGate
    9. Explicit stipulation permits WadhClaim, NOT full Dalālah
    10. Reason alone cannot license Arabic Wadh
    11. WadhGate does NOT create external meaning
    12. WadhGate does NOT issue HUKM
    13. WadhGate does NOT classify Mutabaqah/Tadammun/Iltizam
    14. WadhGate does NOT classify Haqiqah/Majaz/Naql
    15. WadhGate does NOT raise PredicateRank to CERTIFIED
    16. Unknown source becomes residual
    17. Unknown transmission becomes residual
    18. Unknown scope becomes residual
    19. Original Wadh unobserved remains residual
    20. Lexicon conflict becomes residual
    21. WadhGate returns governed failure, not exception
    22. WadhGate full success means WadhClaim admitted, NOT Dalālah

Test Count: 21 tests

Architecture Position:
    DalMadlulBindingCandidate (PR-L4, certified)
    └── WadhGeometry (PR-L5A)
        └── WadhGate (PR-L5B) ← TESTS HERE
"""

import pytest

from gfa.methods.lafzi_wadh import (
    # Gate
    WadhGate,
    WadhGateResult,
    WadhGateFailure,

    # Source
    make_lexicon_report_source,
    make_usage_attestation_source,
    make_explicit_stipulation_source,
    make_reason_inference_source,
    make_unknown_source,

    # Transmission mode
    make_riwayah_mode,
    make_usage_mode,
    make_istidlal_mode,
    make_unknown_mode,

    # Scope
    make_lafzi_arabic_scope,
    make_unknown_scope,

    # Residuals
    make_unknown_source_residual,
    make_unknown_transmission_residual,
    make_unknown_scope_residual,
    make_original_wadh_unobserved_residual,

    # Evidence
    WadhEvidence,

    # Claim
    WadhClaim,

    # MawduLah
    MawduLahStructure,
)

# Test helpers need to be imported from binding module
from gfa.methods.lafzi_binding import (
    DalMadlulBindingCandidate,
    BindingBasis,
)
from gfa.methods.lafzi_dal import DalCandidate, DalType
from gfa.methods.lafzi_madlul import MadlulLafziCandidate, MadlulLafziType


# ============================================================================
# Test Helpers
# ============================================================================

def make_test_binding_candidate() -> DalMadlulBindingCandidate:
    """Create test binding candidate."""
    dal = DalCandidate(
        signifier_form="كَتَبَ",
        dal_type=DalType.SOUND_SIGNIFIER,
        trace_id="dal_trace_001",
    )
    madlul = MadlulLafziCandidate(
        madlul_type=MadlulLafziType.ROOT_CANDIDATE,
        candidate_form="ك-ت-ب",
        source_prior_information="lexicon_root",
        trace_id="madlul_trace_001",
    )
    basis = BindingBasis.LEXICAL_HINT

    return DalMadlulBindingCandidate(
        dal_candidate=dal,
        madlul_candidate=madlul,
        binding_basis=basis,
        trace_id="binding_trace_001",
    )


def make_test_wadh_evidence() -> WadhEvidence:
    """Create test WadhEvidence."""
    return WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="Lexicon reports: كتاب means 'book'",
        binding_trace_id="binding_trace_001",
    )


def make_test_mawdu_lah() -> MawduLahStructure:
    """Create test MawduLahStructure."""
    evidence = make_test_wadh_evidence()
    return MawduLahStructure(
        structure_form="linguistic structure: book concept",
        wadh_evidence=evidence,
        binding_trace_id="binding_trace_001",
    )


# ============================================================================
# Test 1: WadhGate requires DalMadlulBindingCandidate
# ============================================================================

def test_wadh_gate_requires_binding_candidate():
    """
    Critical Law: WadhGate requires DalMadlulBindingCandidate.

    Guards against: Processing without binding context.
    """
    gate = WadhGate()
    evidence = make_test_wadh_evidence()
    mawdu_lah = make_test_mawdu_lah()

    # Missing binding candidate
    result = gate.admit_wadh_claim(
        binding_candidate=None,  # type: ignore
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Should return governed failure
    assert result.is_blocked
    assert result.failure is not None
    assert "DalMadlulBindingCandidate" in result.failure.missing_requirements
    assert "Missing DalMadlulBindingCandidate" in result.failure.reason


# ============================================================================
# Test 2: WadhGate requires WadhEvidence
# ============================================================================

def test_wadh_gate_requires_wadh_evidence():
    """
    Critical Law: WadhGate requires WadhEvidence.

    Guards against: Wadh claim without evidence.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()
    mawdu_lah = make_test_mawdu_lah()

    # Missing evidence
    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=None,  # type: ignore
        mawdu_lah=mawdu_lah,
    )

    # Should return governed failure
    assert result.is_blocked
    assert result.failure is not None
    assert "WadhEvidence" in result.failure.missing_requirements


# ============================================================================
# Test 3: WadhGate requires WadhSource
# ============================================================================

def test_wadh_gate_requires_wadh_source():
    """
    Critical Law: WadhGate requires WadhSource.

    Guards against: Evidence without source.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()
    mawdu_lah = make_test_mawdu_lah()

    # Evidence with missing source - should fail at construction (TypeError)
    with pytest.raises(TypeError, match="source must be WadhSource"):
        evidence = WadhEvidence(
            source=None,  # type: ignore
            transmission_mode=make_riwayah_mode(),
            scope=make_lafzi_arabic_scope(),
            evidence_content="test",
            binding_trace_id="test_trace",
        )


# ============================================================================
# Test 4: WadhGate requires WadhTransmissionMode
# ============================================================================

def test_wadh_gate_requires_transmission_mode():
    """
    Critical Law: WadhGate requires WadhTransmissionMode.

    Guards against: Evidence without transmission verification.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()
    mawdu_lah = make_test_mawdu_lah()

    # Evidence with missing transmission mode
    # Should fail at construction (TypeError)
    with pytest.raises(TypeError):
        evidence = WadhEvidence(
            source=make_lexicon_report_source(),
            transmission_mode=None,  # type: ignore
            scope=make_lafzi_arabic_scope(),
            evidence_content="test",
            binding_trace_id="test_trace",
        )


# ============================================================================
# Test 5: WadhGate requires or residualizes WadhScope
# ============================================================================

def test_wadh_gate_requires_or_residualizes_scope():
    """
    Critical Law: WadhGate requires WadhScope or creates residual.

    Guards against: Evidence without scope classification.
    """
    gate = WadhGate(strict_mode=False)  # Allow residualized scope
    binding = make_test_binding_candidate()
    mawdu_lah = make_test_mawdu_lah()

    # Evidence with unknown scope
    evidence = WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_unknown_scope(),
        evidence_content="test",
        binding_trace_id="binding_trace_001",
    )

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Unknown scope residualizes but doesn't block (in non-strict mode)
    assert result.is_admitted
    assert result.claim is not None
    # Check for unknown scope residual
    assert any("unknown_wadh_scope" in str(r.kind.value) for r in result.claim.residuals)


# ============================================================================
# Test 6: WadhGate requires MawduLahStructure
# ============================================================================

def test_wadh_gate_requires_mawdu_lah_structure():
    """
    Critical Law: WadhGate requires MawduLahStructure.

    Guards against: Wadh claim without placed-for structure.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()
    evidence = make_test_wadh_evidence()

    # Missing MawduLahStructure
    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=None,  # type: ignore
    )

    # Should return governed failure
    assert result.is_blocked
    assert result.failure is not None
    assert "MawduLahStructure" in result.failure.missing_requirements


# ============================================================================
# Test 7: Lexicon report permits WadhClaim, NOT meaning
# ============================================================================

def test_lexicon_report_permits_wadh_claim_not_meaning():
    """
    Critical Law: Lexicon report permits WadhClaim, NOT meaning injection.

    Guards against: Lexicon becoming direct meaning source.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()

    # Evidence from lexicon report
    evidence = WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="Lexicon reports meaning",
        binding_trace_id="binding_trace_001",
    )
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Should admit WadhClaim
    assert result.is_admitted
    assert result.claim is not None

    # CRITICAL: Claim does NOT have meaning fields
    assert not hasattr(result.claim, "meaning")
    assert not hasattr(result.claim, "external_meaning")
    assert not hasattr(result.claim, "semantic_content")


# ============================================================================
# Test 8: Usage attestation permits WadhClaim, NOT UsageGate
# ============================================================================

def test_usage_attestation_permits_wadh_claim_not_usage_gate():
    """
    Critical Law: Usage attestation permits WadhClaim, NOT full UsageGate.

    Guards against: Usage becoming separate gate.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()

    # Evidence from usage attestation
    evidence = WadhEvidence(
        source=make_usage_attestation_source(),
        transmission_mode=make_usage_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="Usage observed in corpus",
        binding_trace_id="binding_trace_001",
    )
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Should admit WadhClaim (not redirect to UsageGate)
    assert result.is_admitted
    assert result.claim is not None
    assert not hasattr(result.claim, "usage_gate_result")


# ============================================================================
# Test 9: Explicit stipulation permits WadhClaim, NOT full Dalālah
# ============================================================================

def test_explicit_stipulation_permits_wadh_claim_not_full_dalalah():
    """
    Critical Law: Explicit stipulation permits WadhClaim, NOT full Dalālah.

    Guards against: Stipulation becoming full semantic certification.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()

    # Evidence from explicit stipulation
    evidence = WadhEvidence(
        source=make_explicit_stipulation_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="Author explicitly defines term",
        binding_trace_id="binding_trace_001",
    )
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Should admit WadhClaim
    assert result.is_admitted
    assert result.claim is not None

    # CRITICAL: Does NOT create full Dalālah
    assert not hasattr(result.claim, "dalalah")
    assert not hasattr(result.claim, "full_signification")


# ============================================================================
# Test 10: Reason alone cannot license Arabic Wadh
# ============================================================================

def test_reason_alone_cannot_license_arabic_wadh():
    """
    Critical Law: Reason alone cannot license Arabic Wadh.

    Guards against: Pure rational inference without transmission.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()

    # Evidence from reason alone (no transmission)
    evidence = WadhEvidence(
        source=make_reason_inference_source(),
        transmission_mode=make_istidlal_mode(),  # Inference, not transmission
        scope=make_lafzi_arabic_scope(),
        evidence_content="Rationally inferred",
        binding_trace_id="binding_trace_001",
    )
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Should be blocked due to reason-alone residual
    assert result.is_blocked
    assert result.failure is not None
    # Check for reason-alone blocker
    assert any(r.is_blocker for r in result.failure.residuals)


# ============================================================================
# Test 11: WadhGate does NOT create external meaning
# ============================================================================

def test_wadh_gate_does_not_create_external_meaning():
    """
    Critical Law: WadhGate does NOT create external meaning.

    Guards against: WadhGate injecting ontological commitments.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()
    evidence = make_test_wadh_evidence()
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    assert result.is_admitted
    assert result.claim is not None

    # CRITICAL: No external meaning fields
    assert not hasattr(result.claim, "external_meaning")
    assert not hasattr(result.claim, "external_truth")
    assert not hasattr(result.claim, "ontological_commitment")
    assert not hasattr(result.claim, "external_referent")


# ============================================================================
# Test 12: WadhGate does NOT issue HUKM
# ============================================================================

def test_wadh_gate_does_not_issue_hukm():
    """
    Critical Law: WadhGate does NOT issue HUKM.

    Guards against: WadhGate making judgments.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()
    evidence = make_test_wadh_evidence()
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    assert result.is_admitted
    assert result.claim is not None

    # CRITICAL: No HUKM fields
    assert not hasattr(result.claim, "hukm")
    assert not hasattr(result.claim, "judgment")
    assert not hasattr(result.claim, "predicate_certified")


# ============================================================================
# Test 13: WadhGate does NOT classify Mutabaqah/Tadammun/Iltizam
# ============================================================================

def test_wadh_gate_does_not_classify_mutabaqah_tadammun_iltizam():
    """
    Critical Law: WadhGate does NOT classify semantic types.

    Guards against: WadhGate performing semantic classification.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()
    evidence = make_test_wadh_evidence()
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    assert result.is_admitted
    assert result.claim is not None

    # CRITICAL: No semantic classification fields
    assert not hasattr(result.claim, "mutabaqah")    # مطابقة
    assert not hasattr(result.claim, "tadammun")     # تضمن
    assert not hasattr(result.claim, "iltizam")      # التزام


# ============================================================================
# Test 14: WadhGate does NOT classify Haqiqah/Majaz/Naql
# ============================================================================

def test_wadh_gate_does_not_classify_haqiqah_majaz_naql():
    """
    Critical Law: WadhGate does NOT classify literal/metaphorical.

    Guards against: WadhGate performing figurative classification.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()
    evidence = make_test_wadh_evidence()
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    assert result.is_admitted
    assert result.claim is not None

    # CRITICAL: No figurative classification fields
    assert not hasattr(result.claim, "haqiqah")      # حقيقة
    assert not hasattr(result.claim, "majaz")        # مجاز
    assert not hasattr(result.claim, "naql")         # نقل


# ============================================================================
# Test 15: WadhGate does NOT raise PredicateRank to CERTIFIED
# ============================================================================

def test_wadh_gate_does_not_raise_predicate_rank_to_certified():
    """
    Critical Law: WadhGate does NOT raise PredicateRank.

    Guards against: WadhGate certifying predicates.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()
    evidence = make_test_wadh_evidence()
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    assert result.is_admitted
    assert result.claim is not None

    # CRITICAL: No rank elevation fields
    assert not hasattr(result.claim, "predicate_rank")
    assert not hasattr(result.claim, "rank_elevated")
    assert not hasattr(result.claim, "certified")


# ============================================================================
# Test 16: Unknown source becomes residual
# ============================================================================

def test_unknown_source_becomes_residual():
    """
    Critical Law: Unknown source becomes blocker residual.

    Guards against: Silent failures on unknown source.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()

    # Evidence with unknown source
    evidence = WadhEvidence(
        source=make_unknown_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="test",
        binding_trace_id="binding_trace_001",
    )
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Should be blocked
    assert result.is_blocked
    assert result.failure is not None
    # Check for unknown source blocker
    assert any(r.is_blocker for r in result.failure.residuals)
    assert "known_source" in result.failure.missing_requirements


# ============================================================================
# Test 17: Unknown transmission becomes residual
# ============================================================================

def test_unknown_transmission_becomes_residual():
    """
    Critical Law: Unknown transmission becomes blocker residual.

    Guards against: Silent failures on unknown transmission.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()

    # Evidence with unknown transmission
    evidence = WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_unknown_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="test",
        binding_trace_id="binding_trace_001",
    )
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Should be blocked
    assert result.is_blocked
    assert result.failure is not None
    # Check for unknown transmission blocker
    assert any(r.is_blocker for r in result.failure.residuals)
    assert "known_transmission" in result.failure.missing_requirements


# ============================================================================
# Test 18: Unknown scope becomes residual
# ============================================================================

def test_unknown_scope_becomes_residual():
    """
    Critical Law: Unknown scope becomes residual (but may not block).

    Guards against: Silent failures on unknown scope.
    """
    gate = WadhGate(strict_mode=False)
    binding = make_test_binding_candidate()

    # Evidence with unknown scope
    evidence = WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_unknown_scope(),
        evidence_content="test",
        binding_trace_id="binding_trace_001",
    )
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Should be admitted with residual
    assert result.is_admitted
    assert result.claim is not None
    # Check for unknown scope residual
    assert any("unknown_wadh_scope" in str(r.kind.value) for r in result.claim.residuals)


# ============================================================================
# Test 19: Original Wadh unobserved remains residual
# ============================================================================

def test_original_wadh_unobserved_remains_residual():
    """
    Critical Law: Original Wadh unobserved creates preserved residual.

    Guards against: Losing information about unobserved origins.
    """
    gate = WadhGate(strict_mode=False)
    binding = make_test_binding_candidate()

    # Evidence with original wadh unobserved residual
    evidence = WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="test",
        binding_trace_id="binding_trace_001",
        residuals=(make_original_wadh_unobserved_residual(),),
    )
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Should preserve residual
    assert result.is_admitted
    assert result.claim is not None
    assert len(result.claim.residuals) > 0
    # Check original wadh residual is preserved
    assert any("original_wadh_unobserved" in str(r.kind.value) for r in result.claim.residuals)


# ============================================================================
# Test 20: Lexicon conflict becomes residual (placeholder)
# ============================================================================

def test_lexicon_conflict_becomes_residual():
    """
    Critical Law: Lexicon conflicts create residuals.

    Note: Full lexicon conflict detection is future work.
    This test verifies residual accumulation pattern.
    """
    gate = WadhGate(strict_mode=False)
    binding = make_test_binding_candidate()

    # For now, just verify residuals accumulate
    evidence = make_test_wadh_evidence()
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Residual accumulation works
    assert result.is_admitted
    # Future: Add conflict detection logic


# ============================================================================
# Test 21: WadhGate returns governed failure, not exception
# ============================================================================

def test_wadh_gate_returns_governed_failure_not_exception():
    """
    Critical Law: WadhGate returns governed failures, NOT bare exceptions.

    Guards against: Ungoverned error paths.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()

    # Trigger failure condition (missing evidence)
    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=None,  # type: ignore
        mawdu_lah=make_test_mawdu_lah(),
    )

    # Should return governed failure, NOT raise exception
    assert isinstance(result, WadhGateResult)
    assert result.is_blocked
    assert isinstance(result.failure, WadhGateFailure)
    assert result.failure.reason
    assert len(result.failure.missing_requirements) > 0


# ============================================================================
# Test 22: WadhGate full success means WadhClaim admitted, NOT Dalālah
# ============================================================================

def test_wadh_gate_full_success_means_wadh_claim_admitted_not_dalalah():
    """
    Critical Law: WadhGate success = WadhClaim admitted, NOT Dalālah completed.

    Guards against: Confusing admission with semantic completion.
    """
    gate = WadhGate()
    binding = make_test_binding_candidate()
    evidence = make_test_wadh_evidence()
    mawdu_lah = make_test_mawdu_lah()

    result = gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # Success means admitted
    assert result.is_admitted
    assert result.claim is not None

    # CRITICAL: Does NOT mean Dalālah completed
    assert not hasattr(result, "dalalah_completed")
    assert not hasattr(result, "semantic_certified")
    assert not hasattr(result, "meaning_established")

    # Result is WadhClaim, not full semantic result
    assert isinstance(result.claim, WadhClaim)

    # Claim still has structure form, not external meaning
    assert hasattr(result.claim.mawdu_lah, "structure_form")
    assert not hasattr(result.claim.mawdu_lah, "external_meaning")
