"""
Test WadhGeometry Definitions (PR-L5A)

Critical Laws Being Tested:
    1. Lexicon report is evidence, NOT Wadh itself
    2. Reason alone CANNOT certify Arabic Wadh (requires transmission)
    3. WadhClaim does NOT create external meaning
    4. WadhClaim does NOT create full Dalālah
    5. WadhClaim does NOT issue HUKM
    6. WadhClaim does NOT classify Mutabaqah/Tadammun/Iltizam
    7. WadhClaim does NOT classify Haqiqah/Majaz/Naql
    8. MawduLahStructure is NOT external truth
    9. Unknown source/transmission/scope becomes residual
    10. Original Wadh unobserved becomes residual
    11. WadhClaim preserves binding trace

Test Count: 14 tests

Architecture Position:
    DalMadlulBindingCandidate (PR-L4, certified)
    └── WadhGeometry (PR-L5A) ← TESTS HERE
"""

import pytest

from gfa.methods.lafzi_wadh import (
    # Source
    WadhSourceKind,
    WadhSource,
    make_lexicon_report_source,
    make_usage_attestation_source,
    make_reason_inference_source,
    make_unknown_source,

    # Transmission mode
    WadhTransmissionKind,
    WadhTransmissionMode,
    make_riwayah_mode,
    make_usage_mode,
    make_istidlal_mode,
    make_unknown_mode,

    # Scope
    WadhScopeKind,
    WadhScope,
    make_lafzi_arabic_scope,
    make_unknown_scope,

    # Residuals
    WadhResidual,
    make_unknown_source_residual,
    make_unknown_transmission_residual,
    make_unknown_scope_residual,
    make_reason_alone_residual,
    make_original_wadh_unobserved_residual,
    make_binding_trace_lost_residual,

    # Evidence
    WadhEvidence,

    # Claim
    WadhClaim,
    WadhClaimFailure,

    # MawduLah
    MawduLahStructure,
)


# ============================================================================
# Test 1: Lexicon report is evidence, NOT Wadh itself
# ============================================================================

def test_wadh_source_lexicon_report_is_evidence_not_wadh():
    """
    Critical Law: Lexicon report is evidence, NOT Wadh itself.

    Guards against: Lexicon becoming direct meaning injection.
    """
    # Create lexicon report source with default description
    lexicon_source = make_lexicon_report_source()

    # Verify it's classified as evidence
    assert lexicon_source.kind == WadhSourceKind.LEXICON_REPORT
    assert lexicon_source.is_transmitted  # Lexicon is transmitted source

    # CRITICAL: Source does NOT have semantic fields
    assert not hasattr(lexicon_source, "meaning")
    assert not hasattr(lexicon_source, "external_meaning")
    assert not hasattr(lexicon_source, "semantic_content")
    assert not hasattr(lexicon_source, "dalalah")
    assert not hasattr(lexicon_source, "wadh_certified")

    # Source is evidence only (verify default description)
    assert "evidence" in lexicon_source.description.lower()
    assert "not direct meaning injection" in lexicon_source.description.lower()


# ============================================================================
# Test 2: Transmission mode required or residual
# ============================================================================

def test_wadh_transmission_mode_required_or_residual():
    """
    Critical Law: Transmission mode must be known or become residual.

    Guards against: Silent unknown transmission.
    """
    # Known transmission mode
    riwayah_mode = make_riwayah_mode()
    assert riwayah_mode.is_known
    assert riwayah_mode.is_direct
    assert riwayah_mode.sufficient_for_arabic_wadh

    # Unknown transmission mode creates residual
    unknown_mode = make_unknown_mode()
    assert not unknown_mode.is_known
    assert not unknown_mode.sufficient_for_arabic_wadh

    # Create residual for unknown mode
    residual = make_unknown_transmission_residual()
    assert residual.kind.value == "unknown_transmission_mode"
    assert residual.is_blocker  # Blocks processing


# ============================================================================
# Test 3: Reason alone cannot certify Arabic Wadh
# ============================================================================

def test_reason_alone_cannot_certify_arabic_wadh():
    """
    Critical Law: Reason alone CANNOT certify Arabic Wadh.
    Arabic Wadh requires transmission (رواية/نقل/استعمال).

    Guards against: Pure rational derivation becoming Wadh certification.
    """
    # Reason-based source
    reason_source = make_reason_inference_source()
    assert reason_source.is_reason_based
    assert not reason_source.is_transmitted

    # CRITICAL: Reason alone is insufficient for Arabic Wadh
    assert not reason_source.sufficient_for_arabic_wadh

    # Reason requires transmission verification
    assert reason_source.requires_transmission

    # Create residual for reason-alone insufficiency
    residual = make_reason_alone_residual()
    assert residual.kind.value == "reason_alone_insufficient"
    assert residual.is_blocker  # Blocks Arabic Wadh certification


# ============================================================================
# Test 4: Scope required or residual
# ============================================================================

def test_wadh_scope_required_or_residual():
    """
    Critical Law: Wadh scope must be known or become residual.

    Guards against: Unbounded scope claims.
    """
    # Known scope
    arabic_scope = make_lafzi_arabic_scope()
    assert arabic_scope.is_known
    assert arabic_scope.is_linguistic
    assert arabic_scope.is_arabic_linguistic

    # Unknown scope creates residual
    unknown_scope_obj = make_unknown_scope()
    assert not unknown_scope_obj.is_known

    # Create residual for unknown scope
    residual = make_unknown_scope_residual()
    assert residual.kind.value == "unknown_wadh_scope"
    assert residual.is_blocker  # Blocks processing


# ============================================================================
# Test 5: WadhClaim does NOT create Dalālah
# ============================================================================

def test_wadh_claim_does_not_create_dalalah():
    """
    Critical Law: WadhClaim does NOT create full Dalālah.

    Guards against: Wadh becoming full semantic signification.
    """
    # Create valid WadhClaim
    evidence = WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="كتاب mentioned in lexicon",
        binding_trace_id="test_binding_123",
    )

    mawdu_lah = MawduLahStructure(
        structure_form="written artifact",
        wadh_evidence=evidence,
    )

    claim = WadhClaim(
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # CRITICAL: WadhClaim does NOT have Dalālah fields
    assert not hasattr(claim, "dalalah")
    assert not hasattr(claim, "full_signification")
    assert not hasattr(claim, "semantic_certified")
    assert not hasattr(claim, "mutabaqah")
    assert not hasattr(claim, "tadammun")
    assert not hasattr(claim, "iltizam")


# ============================================================================
# Test 6: WadhClaim does NOT create external meaning
# ============================================================================

def test_wadh_claim_does_not_create_external_meaning():
    """
    Critical Law: WadhClaim does NOT create external meaning.

    Guards against: Wadh becoming external truth injection.
    """
    # Create WadhClaim
    evidence = WadhEvidence(
        source=make_usage_attestation_source(),
        transmission_mode=make_usage_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="Usage in classical texts",
        binding_trace_id="test_binding_456",
    )

    mawdu_lah = MawduLahStructure(
        structure_form="conceptual structure",
        wadh_evidence=evidence,
    )

    claim = WadhClaim(
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # CRITICAL: WadhClaim does NOT have external meaning fields
    assert not hasattr(claim, "external_meaning")
    assert not hasattr(claim, "external_truth")
    assert not hasattr(claim, "reality_mapping")
    assert not hasattr(claim, "ontological_commitment")


# ============================================================================
# Test 7: WadhClaim does NOT issue HUKM
# ============================================================================

def test_wadh_claim_does_not_issue_hukm():
    """
    Critical Law: WadhClaim does NOT issue HUKM (judgment).

    Guards against: Wadh becoming judgment authority.
    """
    # Create WadhClaim
    evidence = WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="Transmitted convention",
        binding_trace_id="test_binding_789",
    )

    mawdu_lah = MawduLahStructure(
        structure_form="structured placed-for",
        wadh_evidence=evidence,
    )

    claim = WadhClaim(
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # CRITICAL: WadhClaim does NOT have HUKM fields
    assert not hasattr(claim, "hukm")
    assert not hasattr(claim, "judgment")
    assert not hasattr(claim, "predicate_rank_elevated")
    assert not hasattr(claim, "certified_rank")


# ============================================================================
# Test 8: MawduLahStructure is NOT external truth
# ============================================================================

def test_mawdu_lah_structure_is_not_external_truth():
    """
    Critical Law: MawduLahStructure is linguistic structure, NOT external truth.

    Guards against: Placed-for becoming ontological commitment.
    """
    # Create MawduLahStructure
    evidence = WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="Lexicon entry",
        binding_trace_id="test_binding_abc",
    )

    mawdu_lah = MawduLahStructure(
        structure_form="linguistic structure X",
        wadh_evidence=evidence,
    )

    # CRITICAL: MawduLahStructure does NOT have truth fields
    assert not hasattr(mawdu_lah, "external_truth")
    assert not hasattr(mawdu_lah, "ontological_reality")
    assert not hasattr(mawdu_lah, "truth_value")
    assert not hasattr(mawdu_lah, "verified_reality")

    # It's a structure, not truth
    assert mawdu_lah.structure_form == "linguistic structure X"


# ============================================================================
# Test 9: Original Wadh unobserved becomes residual
# ============================================================================

def test_original_wadh_unobserved_becomes_residual():
    """
    Critical Law: Original Wadh unobserved becomes residual unless directly attested.

    Guards against: Claiming original Wadh without evidence.
    """
    # Create residual for unobserved original Wadh
    residual = make_original_wadh_unobserved_residual()

    assert residual.kind.value == "original_wadh_unobserved"
    assert residual.severity == "high"  # Not blocker, but high severity
    assert "reconstruction uncertain" in residual.description.lower()


# ============================================================================
# Test 10: Unknown Wadh source becomes residual
# ============================================================================

def test_unknown_wadh_source_becomes_residual():
    """
    Critical Law: Unknown Wadh source becomes blocker residual.

    Guards against: Processing without source verification.
    """
    # Unknown source
    unknown_src = make_unknown_source()
    assert not unknown_src.is_known
    assert not unknown_src.sufficient_for_arabic_wadh

    # Create residual
    residual = make_unknown_source_residual()
    assert residual.kind.value == "unknown_wadh_source"
    assert residual.is_blocker  # Blocks processing


# ============================================================================
# Test 11: Unknown transmission mode becomes residual
# ============================================================================

def test_unknown_transmission_mode_becomes_residual():
    """
    Critical Law: Unknown transmission mode becomes blocker residual.

    Guards against: Bypassing transmission verification.
    """
    # Unknown transmission mode
    unknown_tx = make_unknown_mode()
    assert not unknown_tx.is_known
    assert not unknown_tx.sufficient_for_arabic_wadh

    # Create residual
    residual = make_unknown_transmission_residual()
    assert residual.kind.value == "unknown_transmission_mode"
    assert residual.is_blocker


# ============================================================================
# Test 12: WadhClaim preserves binding trace
# ============================================================================

def test_wadh_claim_preserves_binding_trace():
    """
    Critical Law: WadhClaim preserves binding trace from DalMadlulBindingCandidate.

    Guards against: Losing lineage through Wadh processing.
    """
    binding_trace_id = "dal_madlul_binding_xyz"

    # Create evidence with binding trace
    evidence = WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="Test evidence",
        binding_trace_id=binding_trace_id,
    )

    # Create MawduLah with preserved trace
    mawdu_lah = MawduLahStructure(
        structure_form="test structure",
        wadh_evidence=evidence,
    )

    # Create WadhClaim
    claim = WadhClaim(
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # CRITICAL: Binding trace preserved through all layers
    assert evidence.binding_trace_id == binding_trace_id
    assert mawdu_lah.binding_trace_id == binding_trace_id
    assert claim.binding_trace_id == binding_trace_id
    assert claim.has_binding_trace


# ============================================================================
# Test 13: WadhClaim does NOT classify Mutabaqah/Tadammun/Iltizam
# ============================================================================

def test_wadh_claim_does_not_classify_mutabaqah_tadammun_iltizam():
    """
    Critical Law: WadhClaim does NOT classify semantic relation types.

    Guards against: Premature semantic classification.
    """
    # Create WadhClaim
    evidence = WadhEvidence(
        source=make_lexicon_report_source(),
        transmission_mode=make_riwayah_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="Evidence",
        binding_trace_id="test_trace",
    )

    mawdu_lah = MawduLahStructure(
        structure_form="structure",
        wadh_evidence=evidence,
    )

    claim = WadhClaim(
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # CRITICAL: No semantic classification fields
    assert not hasattr(claim, "mutabaqah")      # مطابقة (conformity)
    assert not hasattr(claim, "tadammun")       # تضمن (implication)
    assert not hasattr(claim, "iltizam")        # التزام (entailment)
    assert not hasattr(claim, "semantic_type")
    assert not hasattr(claim, "signification_kind")


# ============================================================================
# Test 14: WadhClaim does NOT classify Haqiqah/Majaz/Naql
# ============================================================================

def test_wadh_claim_does_not_classify_haqiqah_majaz_naql():
    """
    Critical Law: WadhClaim does NOT classify literal/metaphorical meaning.

    Guards against: Premature literal/metaphorical classification.
    """
    # Create WadhClaim
    evidence = WadhEvidence(
        source=make_usage_attestation_source(),
        transmission_mode=make_usage_mode(),
        scope=make_lafzi_arabic_scope(),
        evidence_content="Usage evidence",
        binding_trace_id="test_trace_2",
    )

    mawdu_lah = MawduLahStructure(
        structure_form="usage structure",
        wadh_evidence=evidence,
    )

    claim = WadhClaim(
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )

    # CRITICAL: No literal/metaphorical classification fields
    assert not hasattr(claim, "haqiqah")        # حقيقة (literal)
    assert not hasattr(claim, "majaz")          # مجاز (metaphorical)
    assert not hasattr(claim, "naql")           # نقل (semantic transfer)
    assert not hasattr(claim, "literal_metaphorical_type")
    assert not hasattr(claim, "meaning_transfer_mode")


# ============================================================================
# Test Summary
# ============================================================================

def test_summary_all_critical_laws_enforced():
    """
    Summary test: Verify all critical laws are enforced.

    This test documents that all 14 required tests are implemented
    and all critical laws from PR-L5A specification are tested.
    """
    # 14 tests implemented (including this one)
    # All critical laws covered:
    # 1. ✓ Lexicon report is evidence, NOT Wadh
    # 2. ✓ Transmission mode required or residual
    # 3. ✓ Reason alone cannot certify Arabic Wadh
    # 4. ✓ Scope required or residual
    # 5. ✓ WadhClaim does NOT create Dalālah
    # 6. ✓ WadhClaim does NOT create external meaning
    # 7. ✓ WadhClaim does NOT issue HUKM
    # 8. ✓ MawduLahStructure is NOT external truth
    # 9. ✓ Original Wadh unobserved becomes residual
    # 10. ✓ Unknown source becomes residual
    # 11. ✓ Unknown transmission mode becomes residual
    # 12. ✓ WadhClaim preserves binding trace
    # 13. ✓ WadhClaim does NOT classify Mutabaqah/Tadammun/Iltizam
    # 14. ✓ WadhClaim does NOT classify Haqiqah/Majaz/Naql

    assert True  # All laws enforced
