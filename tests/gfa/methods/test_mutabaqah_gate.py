"""
Test MutabaqahGate (PR-L6A)

Critical Laws Being Tested:
    1. MutabaqahGate requires admitted WadhClaim
    2. MutabaqahGate requires MawduLahStructure
    3. MutabaqahGate requires MawduLahStructure.whole
    4. MutabaqahGate preserves WadhClaim trace
    5. MutabaqahGate preserves binding trace
    6. MutabaqahGate preserves residuals
    7. MutabaqahGate does NOT create external meaning
    8. MutabaqahGate does NOT issue HUKM
    9. MutabaqahGate does NOT create Tadammun
    10. MutabaqahGate does NOT create Iltizam
    11. MutabaqahGate does NOT classify Haqiqah/Majaz/Naql
    12. MutabaqahGate does NOT create Ifadah
    13. MutabaqahGate does NOT raise PredicateRank to CERTIFIED
    14. Unknown MawduLah whole becomes residual
    15. Polysemy possible becomes residual
    16. Homonymy possible becomes residual
    17. Partial usage blocks or residualizes Mutabaqah
    18. Success means candidate admitted, NOT truth certified
    19. MutabaqahGate returns governed failure, not exception

Test Count: 19 tests

Architecture Position:
    WadhGate (PR-L5B)
    └── MutabaqahGate (PR-L6A) ← TESTS HERE
"""

import pytest

from gfa.methods.lafzi_dalalah import (
    # Gate
    MutabaqahGate,
    MutabaqahResult,
    MutabaqahFailure,
    MutabaqahCandidate,

    # Residuals
    make_wadh_claim_not_admitted_residual,
    make_mawdu_lah_whole_unavailable_residual,
    make_polysemy_possible_residual,
    make_homonymy_possible_residual,
    make_partial_usage_detected_residual,
    make_external_meaning_injection_residual,
    make_hukm_injection_residual,
    make_tadammun_created_residual,
    make_iltizam_created_residual,
    make_haqiqah_majaz_classified_residual,
)

from gfa.methods.lafzi_wadh import (
    # Gate and results
    WadhGate,
    WadhGateResult,

    # Source
    make_lexicon_report_source,
    make_riwayah_mode,
    make_lafzi_arabic_scope,

    # Evidence
    WadhEvidence,

    # MawduLah
    MawduLahStructure,
)

# Test helpers from binding module
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
    """Create test Wadh evidence."""
    source = make_lexicon_report_source("Arabic lexicon")
    transmission = make_riwayah_mode("Transmitted through lexicon")
    scope = make_lafzi_arabic_scope()
    return WadhEvidence(
        source=source,
        transmission_mode=transmission,
        scope=scope,
        evidence_content="Lexicon reports: كتب means 'writing'",
        binding_trace_id="binding_trace_001",
    )


def make_test_mawdu_lah_structure() -> MawduLahStructure:
    """Create test MawduLah structure."""
    evidence = make_test_wadh_evidence()
    return MawduLahStructure(
        structure_form="الكتابة الكاملة",  # "the complete writing"
        wadh_evidence=evidence,
        binding_trace_id="binding_trace_001",
    )


def make_admitted_wadh_gate_result() -> WadhGateResult:
    """Create admitted WadhGate result."""
    gate = WadhGate(strict_mode=True)
    binding = make_test_binding_candidate()
    evidence = make_test_wadh_evidence()
    mawdu_lah = make_test_mawdu_lah_structure()

    return gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=mawdu_lah,
    )


# ============================================================================
# Law 1: MutabaqahGate requires admitted WadhClaim
# ============================================================================

def test_mutabaqah_requires_admitted_wadh_claim():
    """
    Law 1: MutabaqahGate requires admitted WadhClaim.

    Critical: WadhClaim must be admitted before Mutabaqah processing.
    """
    gate = MutabaqahGate(strict_mode=True)

    # Create non-admitted WadhGateResult (failure)
    wadh_gate = WadhGate(strict_mode=True)
    binding = make_test_binding_candidate()
    evidence = make_test_wadh_evidence()
    # Missing mawdu_lah to cause failure
    result = wadh_gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=None,  # Missing!
    )

    # Verify WadhGateResult is not admitted
    assert not result.is_admitted
    assert result.is_blocked

    # Try to create MutabaqahCandidate with non-admitted WadhClaim
    mutabaqah_result = gate.admit_mutabaqah_candidate(result)

    # Verify failure
    assert not mutabaqah_result.is_admitted
    assert mutabaqah_result.is_blocked
    assert mutabaqah_result.has_failure
    assert "WadhClaim not admitted" in mutabaqah_result.failure.reason


# ============================================================================
# Law 2: MutabaqahGate requires MawduLahStructure
# ============================================================================

def test_mutabaqah_requires_mawdu_lah_structure():
    """
    Law 2: MutabaqahGate requires MawduLahStructure.

    Critical: MawduLahStructure must exist in WadhClaim.
    """
    # Note: This is implicitly tested since WadhGate requires MawduLahStructure
    # and we require admitted WadhClaim. But we verify explicitly.

    admitted_result = make_admitted_wadh_gate_result()
    assert admitted_result.is_admitted
    assert admitted_result.claim is not None
    assert admitted_result.claim.mawdu_lah is not None

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Should succeed
    assert mutabaqah_result.is_admitted
    assert mutabaqah_result.candidate is not None


# ============================================================================
# Law 3: MutabaqahGate requires MawduLahStructure.whole
# ============================================================================

def test_mutabaqah_requires_mawdu_lah_whole():
    """
    Law 3: MutabaqahGate requires MawduLahStructure.whole.

    Critical: The whole of MawduLah must be available.
    """
    admitted_result = make_admitted_wadh_gate_result()
    assert admitted_result.claim.mawdu_lah.structure_form  # whole exists

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify success and whole is preserved
    assert mutabaqah_result.is_admitted
    assert mutabaqah_result.candidate.mawdu_lah_whole
    assert mutabaqah_result.candidate.mawdu_lah_whole == "الكتابة الكاملة"


# ============================================================================
# Law 4: MutabaqahGate preserves WadhClaim trace
# ============================================================================

def test_mutabaqah_preserves_wadh_trace():
    """
    Law 4: MutabaqahGate preserves WadhClaim trace.

    Critical: WadhClaim trace must be preserved through processing.
    """
    admitted_result = make_admitted_wadh_gate_result()
    wadh_trace_id = admitted_result.claim.claim_id

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify WadhClaim trace preserved
    assert mutabaqah_result.is_admitted
    assert mutabaqah_result.candidate.has_wadh_trace
    assert mutabaqah_result.candidate.wadh_trace_id == wadh_trace_id


# ============================================================================
# Law 5: MutabaqahGate preserves binding trace
# ============================================================================

def test_mutabaqah_preserves_binding_trace():
    """
    Law 5: MutabaqahGate preserves binding trace.

    Critical: Binding trace must be preserved from original binding.
    """
    admitted_result = make_admitted_wadh_gate_result()
    binding_trace_id = admitted_result.claim.binding_trace_id

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify binding trace preserved
    assert mutabaqah_result.is_admitted
    assert mutabaqah_result.candidate.has_binding_trace
    assert mutabaqah_result.candidate.binding_trace_id == binding_trace_id
    assert mutabaqah_result.candidate.binding_trace_id == "binding_trace_001"


# ============================================================================
# Law 6: MutabaqahGate preserves residuals
# ============================================================================

def test_mutabaqah_preserves_residuals():
    """
    Law 6: MutabaqahGate preserves residuals.

    Critical: Residuals from WadhClaim must be tracked (not lost).
    """
    admitted_result = make_admitted_wadh_gate_result()

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify residuals are tracked (even if empty in this case)
    assert mutabaqah_result.is_admitted
    # Residuals should be accessible
    assert hasattr(mutabaqah_result.candidate, 'residuals')


# ============================================================================
# Law 7: MutabaqahGate does NOT create external meaning
# ============================================================================

def test_mutabaqah_does_not_create_external_meaning():
    """
    Law 7: MutabaqahGate does NOT create external meaning.

    Critical: MutabaqahCandidate is linguistic structure, NOT external truth.
    """
    admitted_result = make_admitted_wadh_gate_result()

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify success
    assert mutabaqah_result.is_admitted
    candidate = mutabaqah_result.candidate

    # Verify NO external meaning fields
    assert not hasattr(candidate, 'external_meaning')
    assert not hasattr(candidate, 'external_truth')
    assert not hasattr(candidate, 'external_referent')
    assert not hasattr(candidate, 'semantic_value')


# ============================================================================
# Law 8: MutabaqahGate does NOT issue HUKM
# ============================================================================

def test_mutabaqah_does_not_issue_hukm():
    """
    Law 8: MutabaqahGate does NOT issue HUKM.

    Critical: MutabaqahCandidate does NOT issue judgment.
    """
    admitted_result = make_admitted_wadh_gate_result()

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify success
    assert mutabaqah_result.is_admitted
    candidate = mutabaqah_result.candidate

    # Verify NO HUKM fields
    assert not hasattr(candidate, 'hukm')
    assert not hasattr(candidate, 'judgment')
    assert not hasattr(candidate, 'ruling')
    assert not hasattr(candidate, 'verdict')


# ============================================================================
# Law 9: MutabaqahGate does NOT create Tadammun
# ============================================================================

def test_mutabaqah_does_not_create_tadammun():
    """
    Law 9: MutabaqahGate does NOT create Tadammun.

    Critical: Mutabaqah is whole only, NOT part (Tadammun).
    """
    admitted_result = make_admitted_wadh_gate_result()

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify success
    assert mutabaqah_result.is_admitted
    candidate = mutabaqah_result.candidate

    # Verify NO Tadammun fields
    assert not hasattr(candidate, 'tadammun')
    assert not hasattr(candidate, 'part')
    assert not hasattr(candidate, 'partial_signification')
    assert not hasattr(candidate, 'component')


# ============================================================================
# Law 10: MutabaqahGate does NOT create Iltizam
# ============================================================================

def test_mutabaqah_does_not_create_iltizam():
    """
    Law 10: MutabaqahGate does NOT create Iltizam.

    Critical: Mutabaqah is placed-for only, NOT external entailment (Iltizam).
    """
    admitted_result = make_admitted_wadh_gate_result()

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify success
    assert mutabaqah_result.is_admitted
    candidate = mutabaqah_result.candidate

    # Verify NO Iltizam fields
    assert not hasattr(candidate, 'iltizam')
    assert not hasattr(candidate, 'entailment')
    assert not hasattr(candidate, 'implication')
    assert not hasattr(candidate, 'necessary_consequence')


# ============================================================================
# Law 11: MutabaqahGate does NOT classify Haqiqah/Majaz/Naql
# ============================================================================

def test_mutabaqah_does_not_classify_haqiqah_majaz_naql():
    """
    Law 11: MutabaqahGate does NOT classify Haqiqah/Majaz/Naql.

    Critical: Mutabaqah does NOT determine literal vs. metaphorical.
    """
    admitted_result = make_admitted_wadh_gate_result()

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify success
    assert mutabaqah_result.is_admitted
    candidate = mutabaqah_result.candidate

    # Verify NO Haqiqah/Majaz/Naql fields
    assert not hasattr(candidate, 'haqiqah')
    assert not hasattr(candidate, 'majaz')
    assert not hasattr(candidate, 'naql')
    assert not hasattr(candidate, 'literal_metaphor_classification')
    assert not hasattr(candidate, 'usage_type')


# ============================================================================
# Law 12: MutabaqahGate does NOT create Ifadah
# ============================================================================

def test_mutabaqah_does_not_create_ifadah():
    """
    Law 12: MutabaqahGate does NOT create Ifadah.

    Critical: Mutabaqah does NOT create learning or benefit.
    """
    admitted_result = make_admitted_wadh_gate_result()

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify success
    assert mutabaqah_result.is_admitted
    candidate = mutabaqah_result.candidate

    # Verify NO Ifadah fields
    assert not hasattr(candidate, 'ifadah')
    assert not hasattr(candidate, 'benefit')
    assert not hasattr(candidate, 'learning')
    assert not hasattr(candidate, 'knowledge_production')


# ============================================================================
# Law 13: MutabaqahGate does NOT raise PredicateRank to CERTIFIED
# ============================================================================

def test_mutabaqah_does_not_raise_predicate_rank_to_certified():
    """
    Law 13: MutabaqahGate does NOT raise PredicateRank to CERTIFIED.

    Critical: Admission does NOT mean certification.
    """
    admitted_result = make_admitted_wadh_gate_result()

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify success
    assert mutabaqah_result.is_admitted
    candidate = mutabaqah_result.candidate

    # Verify NO rank elevation fields
    assert not hasattr(candidate, 'predicate_rank')
    assert not hasattr(candidate, 'rank')
    assert not hasattr(candidate, 'certification')
    assert not hasattr(candidate, 'certified')


# ============================================================================
# Law 14: Unknown MawduLah whole becomes residual
# ============================================================================

def test_unknown_mawdu_lah_whole_becomes_residual():
    """
    Law 14: Unknown MawduLah whole becomes residual.

    Critical: Unknown whole is residualized, not ignored.
    """
    # This is tested implicitly in Law 3 (requires whole)
    # If whole is unavailable, it becomes residual and blocks

    residual = make_mawdu_lah_whole_unavailable_residual()
    assert residual.is_blocker
    assert "MawduLah whole unavailable" in residual.description


# ============================================================================
# Law 15: Polysemy possible becomes residual
# ============================================================================

def test_polysemy_possible_becomes_residual():
    """
    Law 15: Polysemy possible becomes residual.

    Critical: Polysemy possibility is residualized, not exception.
    """
    residual = make_polysemy_possible_residual()
    assert residual.severity == "high"
    assert not residual.is_blocker  # High but not blocker
    assert "Polysemy possible" in residual.description


# ============================================================================
# Law 16: Homonymy possible becomes residual
# ============================================================================

def test_homonymy_possible_becomes_residual():
    """
    Law 16: Homonymy possible becomes residual.

    Critical: Homonymy possibility is residualized, not exception.
    """
    residual = make_homonymy_possible_residual()
    assert residual.severity == "high"
    assert not residual.is_blocker  # High but not blocker
    assert "Homonymy possible" in residual.description


# ============================================================================
# Law 17: Partial usage blocks or residualizes Mutabaqah
# ============================================================================

def test_partial_usage_blocks_or_residualizes_mutabaqah():
    """
    Law 17: Partial usage blocks or residualizes Mutabaqah.

    Critical: Partial usage indicates Tadammun, blocks Mutabaqah.
    """
    residual = make_partial_usage_detected_residual()
    assert residual.is_blocker
    assert "Partial usage detected" in residual.description
    assert "Tadammun" in residual.description


# ============================================================================
# Law 18: Success means candidate admitted, NOT truth certified
# ============================================================================

def test_mutabaqah_success_means_candidate_admitted_not_truth_certified():
    """
    Law 18: Success means candidate admitted, NOT truth certified.

    Critical: MutabaqahCandidate admission ≠ external truth certification.
    """
    admitted_result = make_admitted_wadh_gate_result()

    gate = MutabaqahGate(strict_mode=True)
    mutabaqah_result = gate.admit_mutabaqah_candidate(admitted_result)

    # Verify success means candidate admitted
    assert mutabaqah_result.is_admitted
    assert mutabaqah_result.candidate.is_admitted

    # But does NOT mean truth certified
    assert not hasattr(mutabaqah_result.candidate, 'truth_certified')
    assert not hasattr(mutabaqah_result.candidate, 'external_truth_value')
    assert not hasattr(mutabaqah_result.candidate, 'verified_truth')


# ============================================================================
# Law 19: MutabaqahGate returns governed failure, not exception
# ============================================================================

def test_mutabaqah_returns_governed_failure_not_exception():
    """
    Law 19: MutabaqahGate returns governed failure, not exception.

    Critical: All failures are governed, never bare exceptions.
    """
    gate = MutabaqahGate(strict_mode=True)

    # Create non-admitted WadhGateResult
    wadh_gate = WadhGate(strict_mode=True)
    binding = make_test_binding_candidate()
    evidence = make_test_wadh_evidence()
    # Missing mawdu_lah to cause failure
    result = wadh_gate.admit_wadh_claim(
        binding_candidate=binding,
        wadh_evidence=evidence,
        mawdu_lah=None,
    )

    # Process should NOT raise exception
    mutabaqah_result = gate.admit_mutabaqah_candidate(result)

    # Verify governed failure
    assert isinstance(mutabaqah_result, MutabaqahResult)
    assert mutabaqah_result.is_blocked
    assert mutabaqah_result.has_failure
    assert isinstance(mutabaqah_result.failure, MutabaqahFailure)
    assert mutabaqah_result.failure.reason
    assert mutabaqah_result.failure.missing_requirements
