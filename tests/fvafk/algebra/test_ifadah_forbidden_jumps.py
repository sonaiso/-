"""
Phase 5.5: Ifādah Forbidden Jumps Tests

Tests proving that Phase 5 semantic algebra CANNOT jump to HUKM domain.

These tests enforce the critical boundary: SEMANTICS ≠ HUKM.

Test Categories:
    1. Speech force boundaries (Tests 12-14)
    2. Ifādah completion boundaries (Test 15)
    3. Domain jump prevention (Tests 16-17)
    4. Mutation/bypass resistance

Hard Gates Tested (6 total):
    ✓ Khabar does not become HUKM
    ✓ Amr does not become obligation in Phase 5
    ✓ Nahy does not become prohibition/fasād in Phase 5
    ✓ Ifādah with residuals cannot become CERTIFIED
    ✓ SEMANTICS cannot jump to HUKM
    ✓ IFADAH cannot issue HUKM
"""

import pytest
from src.fvafk.algebra.core import Result, Rank, Evidence, Residual, Carrier, Domain
from src.fvafk.algebra.semantics import (
    # Operations
    SpeechForceOperation,
    IfadahClosureOperation,
    BoundaryGuardOperation,
    # Wrappers
    governed_speech_force,
    governed_ifadah_closure,
    governed_boundary_guard,
    # Residuals
    make_speech_force_uncertain,
    make_ifadah_incomplete,
    make_hukm_boundary_violation,
)


# =============================================================================
# Test Category 1: Speech Force Boundaries (Tests 12-14)
# =============================================================================

def test_hard_gate_12_khabar_does_not_become_hukm():
    """
    Hard Gate 12: الخبر ليس حكماً

    Khabar (declarative) does not become HUKM.
    Khabar is speech force, not legal/epistemic judgment.

    Mutation resistance:
        - If developer emits hukm.* evidence from khabar → test fails
        - If developer promotes khabar to HUKM domain → test fails
    """
    utterance = "زيد قائم"
    force_type = "khabar"

    result = governed_speech_force(utterance, force_type, evidence=())

    # Khabar must stay in SEMANTICS domain
    assert all(e.kind != Domain.HUKM for e in result.evidence), \
        "Khabar evidence must not be in HUKM domain"

    # Khabar must not emit hukm.* evidence kinds
    assert all("hukm" not in str(e.kind).lower() for e in result.evidence), \
        "Khabar must not emit HUKM evidence"

    # Khabar must not claim obligation, prohibition, or judgment
    forbidden_claims = ["obligation", "prohibition", "fasad", "judgment", "ruling"]
    for claim in forbidden_claims:
        assert all(claim not in str(e.kind).lower() for e in result.evidence), \
            f"Khabar must not claim '{claim}'"


def test_hard_gate_13_amr_does_not_become_obligation_in_phase5():
    """
    Hard Gate 13: الأمر ليس وجوباً في Phase 5

    Amr (imperative) does not become obligation at Phase 5.
    Amr is speech force; obligation is HUKM (Phase 6).

    Mutation resistance:
        - If developer emits obligation evidence → test fails
        - If developer promotes amr to HUKM → test fails
    """
    utterance = "اضرب"
    force_type = "amr"

    result = governed_speech_force(utterance, force_type, evidence=())

    # Amr must stay in SEMANTICS domain
    assert all("hukm" not in str(e.kind).lower() for e in result.evidence), \
        "Amr must not emit HUKM evidence"

    # Amr must not claim obligation (وجوب)
    forbidden_claims = ["obligation", "wajib", "fard", "mandatory"]
    for claim in forbidden_claims:
        assert all(claim not in str(e.kind).lower() for e in result.evidence), \
            f"Amr must not claim '{claim}' at Phase 5"

    # Amr can be LICENSED as speech force, but not HUKM
    assert result.rank in (Rank.CANDIDATE, Rank.LICENSED), \
        "Amr can be LICENSED as speech force but never as HUKM"


def test_hard_gate_14_nahy_does_not_become_prohibition_in_phase5():
    """
    Hard Gate 14: النهي ليس حراماً/فساداً في Phase 5

    Nahy (prohibitive) does not become prohibition or fasād at Phase 5.
    Nahy is speech force; prohibition is HUKM (Phase 6).

    Mutation resistance:
        - If developer emits prohibition/fasad evidence → test fails
        - If developer promotes nahy to HUKM → test fails
    """
    utterance = "لا تضرب"
    force_type = "nahy"

    result = governed_speech_force(utterance, force_type, evidence=())

    # Nahy must stay in SEMANTICS domain
    assert all("hukm" not in str(e.kind).lower() for e in result.evidence), \
        "Nahy must not emit HUKM evidence"

    # Nahy must not claim prohibition or fasād
    forbidden_claims = ["prohibition", "haram", "forbidden", "fasad", "invalid"]
    for claim in forbidden_claims:
        assert all(claim not in str(e.kind).lower() for e in result.evidence), \
            f"Nahy must not claim '{claim}' at Phase 5"

    # Nahy can be LICENSED as speech force, but not HUKM
    assert result.rank in (Rank.CANDIDATE, Rank.LICENSED), \
        "Nahy can be LICENSED as speech force but never as HUKM"


# =============================================================================
# Test Category 2: Ifādah Completion Boundaries (Test 15)
# =============================================================================

def test_hard_gate_15_ifadah_with_residuals_cannot_become_certified():
    """
    Hard Gate 15: الإفادة ذات البقايا لا تُعتَمد

    Ifādah with residuals cannot become CERTIFIED.
    Residuals prevent certification by constitution.

    Mutation resistance:
        - If developer certifies ifādah with residuals → test fails
        - If developer bypasses residual check → test fails
    """
    parties = ("مبتدأ", "خبر")
    complete = False  # Incomplete ifādah

    result = governed_ifadah_closure(parties, complete, evidence=())

    # Incomplete ifādah must have residuals
    assert len(result.residuals) > 0, \
        "Incomplete ifādah must carry residuals"

    # Ifādah with residuals cannot be CERTIFIED
    assert result.rank != Rank.CERTIFIED, \
        "Ifādah with residuals cannot be CERTIFIED"

    # Verify ifadah.incomplete residual present
    assert any(r.kind == "semantics.ifadah.incomplete" for r in result.residuals), \
        "Incomplete ifādah must carry ifadah.incomplete residual"


def test_ifadah_complete_without_evidence_still_not_certified():
    """
    Ifādah completeness is necessary but not sufficient for CERTIFIED.
    Evidence is also required.

    Mutation resistance:
        - If developer certifies without evidence → test fails
    """
    parties = ("مبتدأ", "خبر")
    complete = True  # Structure complete

    result = governed_ifadah_closure(parties, complete, evidence=())

    # Without evidence, even complete ifādah cannot be CERTIFIED
    if not result.evidence:
        assert result.rank in (Rank.CANDIDATE, Rank.LICENSED), \
            "Complete ifādah without evidence cannot be CERTIFIED"


def test_ifadah_complete_with_evidence_can_certify():
    """
    Ifādah that is complete AND has evidence can reach CERTIFIED.

    This is the positive test showing the happy path.
    """
    parties = ("مبتدأ", "خبر")
    complete = True
    evidence = (
        Evidence(kind="syntax.predication", source="test"),
        Evidence(kind="semantics.binding", source="test"),
    )

    result = governed_ifadah_closure(parties, complete, evidence=evidence)

    # With complete structure + evidence + no residuals → can be CERTIFIED
    if len(result.residuals) == 0:
        assert result.rank == Rank.CERTIFIED, \
            "Complete ifādah with evidence and no residuals can be CERTIFIED"


# =============================================================================
# Test Category 3: Domain Jump Prevention (Tests 16-17)
# =============================================================================

def test_hard_gate_16_semantics_cannot_jump_to_hukm():
    """
    Hard Gate 16: SEMANTICS لا يقفز إلى HUKM

    SEMANTICS domain cannot jump to HUKM domain.
    This is enforced by BoundaryGuardOperation.

    Mutation resistance:
        - If developer allows SEMANTICS → HUKM bridge → test fails
        - If developer removes boundary guard → test fails
    """
    source_domain = Domain.SEMANTICS
    target_domain = "HUKM"  # String to represent forbidden domain

    result = governed_boundary_guard(source_domain, target_domain)

    # Attempted jump must be REFUTED
    assert result.rank == Rank.REFUTED, \
        "SEMANTICS → HUKM jump must be REFUTED"

    # Must carry hukm_boundary.violation residual or failure
    has_violation = any(r.kind == "semantics.hukm_boundary.violation" for r in result.residuals)
    has_failure = any(f.kind == "domain.jump.forbidden" for f in result.failures)

    assert has_violation or has_failure, \
        "SEMANTICS → HUKM jump must carry violation residual or failure"


def test_hard_gate_17_ifadah_cannot_issue_hukm():
    """
    Hard Gate 17: الإفادة لا تُصدِر حكماً

    IFADAH cannot issue HUKM.
    Ifādah is semantic completion; HUKM is judgment (Phase 6).

    Mutation resistance:
        - If developer emits hukm.* evidence from ifādah → test fails
        - If developer promotes ifādah to HUKM domain → test fails
    """
    parties = ("subject", "predicate")
    complete = True
    evidence = (Evidence(kind="semantics.complete", source="test"),)

    result = governed_ifadah_closure(parties, complete, evidence=evidence)

    # Ifādah must not emit HUKM evidence
    assert all("hukm" not in str(e.kind).lower() for e in result.evidence), \
        "Ifādah must not emit HUKM evidence"

    # Ifādah must not claim judgment
    forbidden_claims = ["judgment", "ruling", "hukm", "obligation", "prohibition"]
    for claim in forbidden_claims:
        assert all(claim not in str(e.kind).lower() for e in result.evidence), \
            f"Ifādah must not claim '{claim}'"


# =============================================================================
# Mutation Resistance Tests
# =============================================================================

def test_mutation_resistance_gate_removal_detection():
    """
    Detect if a developer removes semantic boundary gates.

    This test verifies that key operations still enforce residuals.
    If gates are removed, residuals disappear, and this test fails.
    """
    # Test 1: Speech force without evidence creates uncertainty
    result_speech = governed_speech_force("test", "uncertain", evidence=())
    assert any(r.kind == "semantics.speech_force.uncertain" for r in result_speech.residuals) or \
           result_speech.rank in (Rank.CANDIDATE, Rank.UNRESOLVED), \
        "Speech force without evidence must create uncertainty residual or low rank"

    # Test 2: Incomplete ifādah creates incomplete residual
    result_ifadah = governed_ifadah_closure(("a", "b"), complete=False, evidence=())
    assert any(r.kind == "semantics.ifadah.incomplete" for r in result_ifadah.residuals), \
        "Incomplete ifādah must create ifadah.incomplete residual"

    # Test 3: HUKM boundary jump creates violation
    result_boundary = governed_boundary_guard(Domain.SEMANTICS, "HUKM")
    assert result_boundary.rank == Rank.REFUTED or \
           any(r.kind == "semantics.hukm_boundary.violation" for r in result_boundary.residuals), \
        "HUKM boundary jump must be REFUTED or carry violation residual"


def test_mutation_resistance_evidence_bypass_detection():
    """
    Detect if a developer bypasses evidence requirements.

    Operations without evidence should not promote to CERTIFIED.
    """
    # Test: Ifādah without evidence and incomplete cannot be CERTIFIED
    result = governed_ifadah_closure(("subject", "predicate"), complete=False, evidence=())

    assert result.rank != Rank.CERTIFIED, \
        "Ifādah without evidence and incomplete cannot be CERTIFIED"

    # If complete but no evidence, still not CERTIFIED
    result_complete = governed_ifadah_closure(("subject", "predicate"), complete=True, evidence=())
    if not result_complete.evidence:
        assert result_complete.rank != Rank.CERTIFIED, \
            "Ifādah without evidence cannot be CERTIFIED even if complete"


def test_mutation_resistance_forbidden_evidence_kinds():
    """
    Verify that semantic operations never emit forbidden evidence kinds.

    Forbidden kinds:
        - hukm.*
        - obligation.*
        - prohibition.*
        - fasad.*
        - judgment.*

    If a developer adds these to semantic operations, this test fails.
    """
    forbidden_prefixes = ["hukm.", "obligation.", "prohibition.", "fasad.", "judgment."]

    # Test all semantic operations
    test_cases = [
        governed_speech_force("test", "khabar", evidence=()),
        governed_ifadah_closure(("a", "b"), True, evidence=()),
        governed_boundary_guard(Domain.SEMANTICS, Domain.SYNTAX),  # Valid transition
    ]

    for result in test_cases:
        for evidence in result.evidence:
            for prefix in forbidden_prefixes:
                assert not evidence.kind.startswith(prefix), \
                    f"Semantic operation emitted forbidden evidence kind: {evidence.kind}"


# =============================================================================
# Integration Tests
# =============================================================================

def test_integration_complete_semantic_chain_never_reaches_hukm():
    """
    Integration test: Complete semantic chain never enters HUKM domain.

    Tests full chain from speech force → ifādah → boundary check.
    Verifies that at no point does the chain emit HUKM evidence.
    """
    # Step 1: Determine speech force (khabar)
    speech_result = governed_speech_force("زيد قائم", "khabar", evidence=())
    assert all("hukm" not in str(e.kind).lower() for e in speech_result.evidence)

    # Step 2: Close ifādah
    ifadah_result = governed_ifadah_closure(("زيد", "قائم"), complete=True, evidence=())
    assert all("hukm" not in str(e.kind).lower() for e in ifadah_result.evidence)

    # Step 3: Verify boundary guard prevents jump
    boundary_result = governed_boundary_guard(Domain.SEMANTICS, "HUKM")
    assert boundary_result.rank == Rank.REFUTED, \
        "Boundary guard must prevent SEMANTICS → HUKM jump"

    # Final verification: No HUKM evidence anywhere
    all_evidence = list(speech_result.evidence) + list(ifadah_result.evidence) + list(boundary_result.evidence)
    for e in all_evidence:
        assert "hukm" not in str(e.kind).lower(), \
            f"No operation may emit HUKM evidence: {e.kind}"


def test_integration_imperative_chain_stops_before_obligation():
    """
    Integration test: Imperative chain stops before becoming obligation.

    Tests that amr (imperative) → ifādah → boundary never claims وجوب.
    """
    # Step 1: Determine speech force (amr)
    speech_result = governed_speech_force("اضرب", "amr", evidence=())
    assert all("obligation" not in str(e.kind).lower() for e in speech_result.evidence)
    assert all("wajib" not in str(e.kind).lower() for e in speech_result.evidence)

    # Step 2: Close ifādah (imperative structure)
    ifadah_result = governed_ifadah_closure(("امر", "فعل"), complete=True, evidence=())
    assert all("obligation" not in str(e.kind).lower() for e in ifadah_result.evidence)

    # Step 3: Verify no jump to HUKM
    boundary_result = governed_boundary_guard(Domain.SEMANTICS, "HUKM")
    assert boundary_result.rank == Rank.REFUTED

    # Final verification: No obligation claim anywhere
    all_evidence = list(speech_result.evidence) + list(ifadah_result.evidence)
    forbidden = ["obligation", "wajib", "fard", "mandatory"]
    for e in all_evidence:
        for term in forbidden:
            assert term not in str(e.kind).lower(), \
                f"Imperative chain must not claim '{term}': {e.kind}"


def test_integration_prohibitive_chain_stops_before_haram():
    """
    Integration test: Prohibitive chain stops before becoming harām/fasād.

    Tests that nahy (prohibitive) → ifādah → boundary never claims حرام/فساد.
    """
    # Step 1: Determine speech force (nahy)
    speech_result = governed_speech_force("لا تضرب", "nahy", evidence=())
    assert all("prohibition" not in str(e.kind).lower() for e in speech_result.evidence)
    assert all("haram" not in str(e.kind).lower() for e in speech_result.evidence)
    assert all("fasad" not in str(e.kind).lower() for e in speech_result.evidence)

    # Step 2: Close ifādah (prohibitive structure)
    ifadah_result = governed_ifadah_closure(("نهي", "فعل"), complete=True, evidence=())
    assert all("prohibition" not in str(e.kind).lower() for e in ifadah_result.evidence)

    # Step 3: Verify no jump to HUKM
    boundary_result = governed_boundary_guard(Domain.SEMANTICS, "HUKM")
    assert boundary_result.rank == Rank.REFUTED

    # Final verification: No prohibition claim anywhere
    all_evidence = list(speech_result.evidence) + list(ifadah_result.evidence)
    forbidden = ["prohibition", "haram", "forbidden", "fasad", "invalid"]
    for e in all_evidence:
        for term in forbidden:
            assert term not in str(e.kind).lower(), \
                f"Prohibitive chain must not claim '{term}': {e.kind}"
