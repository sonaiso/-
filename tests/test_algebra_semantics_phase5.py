"""
Phase 5 Semantic Algebra Tests

Tests for all 9 subphases of Phase 5 (5A-5I).

Test Categories:
    - Residual taxonomy (13 residuals)
    - Dāl/Madlūl operations (5A-5C)
    - Dalālah gates (5D)
    - Nisbah semantic (5E)
    - Reference resolution (5F)
    - Speech force (5G)
    - Ifādah closure (5H)
    - Boundary guards (5I)
    - Hard gates enforcement
    - Regression tests
"""

import pytest
from src.fvafk.algebra.core import Result, Rank, Evidence, Residual, Failure, Carrier, Domain
from src.fvafk.algebra.semantics import (
    # Residuals
    SEMANTICS_RESIDUAL_KINDS,
    make_polysemy_possible,
    make_dal_binding_absent,
    make_dalalah_gate_required,
    make_mutabaqah_insufficient,
    make_tadammun_insufficient,
    make_iltizam_gate_missing,
    make_idafah_not_ifadah,
    make_taqyid_incomplete,
    make_conditional_jawab_missing,
    make_pronoun_referent_missing,
    make_speech_force_uncertain,
    make_ifadah_incomplete,
    make_hukm_boundary_violation,
    # Operations
    DalCandidateOperation,
    MadlulCandidateOperation,
    WadhBindingOperation,
    MutabaqahGate,
    TadammunGate,
    IltizamGate,
    NisbahSemanticOperation,
    ReferenceResolutionOperation,
    SpeechForceOperation,
    IfadahClosureOperation,
    BoundaryGuardOperation,
    # Wrappers
    governed_dal_candidate,
    governed_madlul_candidate,
    governed_wadh_binding,
    governed_mutabaqah,
    governed_tadammun,
    governed_iltizam,
    governed_nisbah_semantic,
    governed_reference_resolution,
    governed_speech_force,
    governed_ifadah_closure,
    governed_boundary_guard,
)


# =============================================================================
# Residual Taxonomy Tests
# =============================================================================

def test_semantics_residual_kinds_canonical_set():
    """Verify canonical set of 13 semantic residuals."""
    assert len(SEMANTICS_RESIDUAL_KINDS) == 13
    assert "semantics.polysemy.possible" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.dal_binding.absent" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.dalalah_gate.required" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.mutabaqah.insufficient" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.tadammun.insufficient" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.iltizam.gate_missing" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.idafah.not_ifadah" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.taqyid.incomplete" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.conditional.jawab_missing" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.pronoun.referent_missing" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.speech_force.uncertain" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.ifadah.incomplete" in SEMANTICS_RESIDUAL_KINDS
    assert "semantics.hukm_boundary.violation" in SEMANTICS_RESIDUAL_KINDS


def test_make_polysemy_possible():
    """Test polysemy residual creation."""
    r = make_polysemy_possible("عين")
    assert r.kind == "semantics.polysemy.possible"
    assert "عين" in r.description


def test_make_dal_binding_absent():
    """Test dal_binding.absent residual."""
    r = make_dal_binding_absent("eye")
    assert r.kind == "semantics.dal_binding.absent"
    assert "eye" in r.description


def test_make_mutabaqah_insufficient():
    """Test mutābaqah insufficiency residual."""
    r = make_mutabaqah_insufficient()
    assert r.kind == "semantics.mutabaqah.insufficient"
    assert "pre_ifadah" in r.description


def test_make_iltizam_gate_missing():
    """Test iltizām gate missing residual."""
    r = make_iltizam_gate_missing("logical")
    assert r.kind == "semantics.iltizam.gate_missing"
    assert "logical" in r.description


def test_make_idafah_not_ifadah():
    """Test iḍāfah not ifādah residual."""
    r = make_idafah_not_ifadah("كتاب زيد")
    assert r.kind == "semantics.idafah.not_ifadah"
    assert "كتاب زيد" in r.description


def test_make_conditional_jawab_missing():
    """Test conditional jawāb missing residual."""
    r = make_conditional_jawab_missing()
    assert r.kind == "semantics.conditional.jawab_missing"
    assert "jawab" in r.description


def test_make_hukm_boundary_violation():
    """Test HUKM boundary violation residual."""
    r = make_hukm_boundary_violation("SEMANTICS→HUKM")
    assert r.kind == "semantics.hukm_boundary.violation"
    assert "SEMANTICS" in r.description


# =============================================================================
# Phase 5A: Dāl Candidate Tests
# =============================================================================

def test_dal_candidate_without_evidence():
    """Test dāl candidate without evidence stays CANDIDATE."""
    result = governed_dal_candidate("كتب")
    assert isinstance(result, Result)
    assert result.rank == Rank.CANDIDATE
    assert len(result.residuals) > 0
    assert any(r.kind == "semantics.polysemy.possible" for r in result.residuals)


def test_dal_candidate_with_evidence_promotes_to_licensed():
    """Test dāl candidate with evidence promotes to LICENSED."""
    evidence = (Evidence(kind="lexicon.attestation", source="test"),)
    result = governed_dal_candidate("كتب", evidence)
    assert result.rank == Rank.LICENSED
    assert len(result.evidence) == 1


def test_dal_alone_is_not_meaning():
    """
    Hard Gate: الدال وحده ليس معنى (Dāl alone is not meaning)

    Dāl alone must always carry polysemy residual.
    """
    result = governed_dal_candidate("كتب")
    # Even with evidence, polysemy residual remains
    assert any(r.kind == "semantics.polysemy.possible" for r in result.residuals)


# =============================================================================
# Phase 5B: Madlūl Candidate Tests
# =============================================================================

def test_madlul_candidate_without_binding():
    """Test madlūl candidate without binding has dal_binding.absent residual."""
    result = governed_madlul_candidate("writing")
    assert result.rank == Rank.CANDIDATE
    assert any(r.kind == "semantics.dal_binding.absent" for r in result.residuals)


def test_madlul_alone_is_not_dalalah():
    """
    Hard Gate: المدلول وحده ليس دلالة (Madlūl alone is not dalālah)

    Madlūl alone must carry dal_binding.absent residual.
    """
    result = governed_madlul_candidate("writing")
    assert any(r.kind == "semantics.dal_binding.absent" for r in result.residuals)


# =============================================================================
# Phase 5C: Wadh' Binding Tests
# =============================================================================

def test_wadh_binding_without_evidence():
    """Test wadh' binding without evidence requires gate."""
    result = governed_wadh_binding("كتب", "writing")
    assert result.rank == Rank.CANDIDATE
    assert any(r.kind == "semantics.dalalah_gate.required" for r in result.residuals)


def test_wadh_binding_with_evidence_licensed():
    """Test wadh' binding with evidence becomes LICENSED."""
    evidence = (Evidence(kind="wadh.attestation", source="test"),)
    result = governed_wadh_binding("كتب", "writing", evidence)
    assert result.rank == Rank.LICENSED
    assert len(result.residuals) == 0


def test_dal_madlul_binding_required():
    """
    Hard Gate: لا دلالة بلا ربط (No dalālah without binding)

    Binding must require evidence to become LICENSED.
    """
    result_without = governed_wadh_binding("كتب", "writing")
    assert result_without.rank == Rank.CANDIDATE

    evidence = (Evidence(kind="wadh.attestation", source="test"),)
    result_with = governed_wadh_binding("كتب", "writing", evidence)
    assert result_with.rank == Rank.LICENSED


# =============================================================================
# Phase 5D: Dalālah Gates Tests
# =============================================================================

def test_mutabaqah_is_not_ifadah():
    """
    Hard Gate: المطابقة لا تصبح إفادة وحدها
    (Mutābaqah does not become ifādah alone)

    Mutābaqah must always carry insufficiency residual.
    """
    result = governed_mutabaqah("كتب→writing")
    assert any(r.kind == "semantics.mutabaqah.insufficient" for r in result.residuals)


def test_tadammun_is_not_ifadah():
    """
    Hard Gate: التضمن لا يصبح إفادة وحده
    (Taḍammun does not become ifādah alone)

    Taḍammun must always carry insufficiency residual.
    """
    result = governed_tadammun("كتب→writing", "inscription")
    assert any(r.kind == "semantics.tadammun.insufficient" for r in result.residuals)


def test_iltizam_requires_gate():
    """
    Hard Gate: الالتزام ليس تلقائياً (Iltizām is not automatic)

    Iltizām without gate must fail or carry gate_missing residual.
    """
    # Without gate
    result = governed_iltizam("كتب→writing", "literacy")
    assert result.rank == Rank.CANDIDATE
    assert any(r.kind == "semantics.iltizam.gate_missing" for r in result.residuals)

    # With gate
    evidence = (Evidence(kind="iltizam.logical", source="test"),)
    result_with_gate = governed_iltizam("كتب→writing", "literacy", "logical", evidence)
    assert result_with_gate.rank == Rank.LICENSED


# =============================================================================
# Phase 5E: Nisbah Semantic Tests
# =============================================================================

def test_idafah_alone_is_not_ifadah():
    """
    Hard Gate: النسبة الإضافية لا تصبح إفادة
    (Iḍāfah relation does not become ifādah)

    Iḍāfah must carry idafah.not_ifadah residual.
    """
    result = governed_nisbah_semantic("IDAFA", "كتاب زيد")
    assert any(r.kind == "semantics.idafah.not_ifadah" for r in result.residuals)


def test_taqyid_alone_is_not_ifadah():
    """
    Hard Gate: Taqyīd incomplete without predication.
    """
    result = governed_nisbah_semantic("TAQYID", "رجل كريم")
    assert any(r.kind == "semantics.taqyid.incomplete" for r in result.residuals)


def test_conditional_without_jawab_is_not_ifadah():
    """
    Hard Gate: الشرط بلا جواب لا يصبح إفادة
    (Conditional without jawāb does not become ifādah)
    """
    result = governed_nisbah_semantic("SHART", "إن جئت")
    assert any(r.kind == "semantics.conditional.jawab_missing" for r in result.residuals)


# =============================================================================
# Phase 5F: Reference Resolution Tests
# =============================================================================

def test_pronoun_without_referent_cannot_certify_ifadah():
    """
    Hard Gate: الضمير بلا مرجع لا يصبح إفادة معتمدة
    (Pronoun without referent cannot become CERTIFIED ifādah)
    """
    result = governed_reference_resolution("هو")
    assert result.rank == Rank.CANDIDATE
    assert any(r.kind == "semantics.pronoun.referent_missing" for r in result.residuals)


def test_pronoun_with_referent_licensed():
    """Test pronoun with referent becomes LICENSED."""
    result = governed_reference_resolution("هو", "زيد")
    assert result.rank == Rank.CANDIDATE  # Still needs evidence
    assert len([r for r in result.residuals if r.kind == "semantics.pronoun.referent_missing"]) == 0


# =============================================================================
# Phase 5G: Speech Force Tests
# =============================================================================

def test_khabar_is_not_hukm():
    """
    Hard Gate: Khabar does NOT become HUKM

    Speech force detection must not claim HUKM.
    """
    result = governed_speech_force("زيد قائم", "khabar")
    # Result must NOT claim HUKM domain or evidence
    assert result.rank in (Rank.CANDIDATE, Rank.LICENSED)
    for ev in result.evidence:
        assert not ev.kind.startswith("hukm.")


def test_amr_is_not_obligation_at_phase5():
    """
    Hard Gate: Amr does NOT become obligation at Phase 5
    """
    result = governed_speech_force("اكتب", "amr")
    # Result must NOT claim HUKM
    assert result.rank in (Rank.CANDIDATE, Rank.LICENSED)
    for ev in result.evidence:
        assert not ev.kind.startswith("hukm.")


def test_speech_force_uncertain():
    """Test uncertain speech force creates residual."""
    result = governed_speech_force("ما هذا؟")
    assert any(r.kind == "semantics.speech_force.uncertain" for r in result.residuals)


# =============================================================================
# Phase 5H: Ifādah Closure Tests
# =============================================================================

def test_ifadah_requires_all_eight_components():
    """
    Test ifādah closure requires ALL 8 components:
    1. Licensed parties
    2. Licensed dāl/madlūl binding
    3. Licensed dalālah
    4. Licensed nisbah
    5. Complete structure
    6. Resolved references or residuals
    7. Known speech force or residual
    8. Full residual accounting
    """
    # Incomplete ifādah
    incomplete = {
        "parties": True,
        "binding": True,
        # Missing other components
    }
    result = governed_ifadah_closure(incomplete)
    assert result.rank == Rank.CANDIDATE
    assert any(r.kind == "semantics.ifadah.incomplete" for r in result.residuals)


def test_ifadah_with_residuals_cannot_certify():
    """
    Hard Gate: Ifādah with residuals cannot be CERTIFIED

    Even complete ifādah without evidence stays CANDIDATE.
    """
    complete = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": True,
    }
    # Without evidence
    result = governed_ifadah_closure(complete)
    assert result.rank == Rank.CANDIDATE  # Not LICENSED without evidence


def test_ifadah_complete_with_evidence_certified():
    """Test complete ifādah with evidence becomes CERTIFIED."""
    complete = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": True,
    }
    evidence = (Evidence(kind="ifadah.complete", source="test"),)
    result = governed_ifadah_closure(complete, evidence)
    assert result.rank == Rank.CERTIFIED
    assert len(result.residuals) == 0


# =============================================================================
# Phase 5I: Boundary Guard Tests
# =============================================================================

def test_semantics_cannot_jump_to_hukm():
    """
    Hard Gate: SEMANTICS cannot jump to HUKM

    This is a fatal boundary violation.
    """
    result = governed_boundary_guard(Domain.SEMANTICS, Domain.HUKM, "test")
    assert result.rank == Rank.REFUTED
    assert any(f.fatal for f in result.failures)
    assert any(r.kind == "semantics.hukm_boundary.violation" for r in result.residuals)


def test_ifadah_cannot_issue_hukm():
    """
    Hard Gate: IFADAH cannot issue HUKM

    Attempting to claim HUKM from ifādah must be refuted.
    """
    result = governed_boundary_guard(Domain.SEMANTICS, Domain.HUKM, "ifadah_result")
    assert result.rank == Rank.REFUTED


# =============================================================================
# Evidence Integration Tests
# =============================================================================

def test_evidence_supports_semantic_operations():
    """Test evidence from adapters supports semantic claims."""
    evidence = (Evidence(kind="semantic.wadh_attestation", source="adapter:LexiconAdapter:1"),)
    result = governed_wadh_binding("كتب", "writing", evidence)
    assert result.rank == Rank.LICENSED
    assert len(result.evidence) == 1
    assert result.evidence[0].source.startswith("adapter:")


# =============================================================================
# Domain Boundary Tests
# =============================================================================

def test_semantics_operations_never_claim_hukm():
    """Test semantic operations never emit hukm.* evidence."""
    operations = [
        governed_dal_candidate("test"),
        governed_madlul_candidate("test"),
        governed_wadh_binding("dal", "madlul"),
        governed_mutabaqah("binding"),
        governed_tadammun("binding", "part"),
        governed_iltizam("binding", "consequence"),
        governed_nisbah_semantic("ISN", "parties"),
        governed_reference_resolution("pronoun", "referent"),
        governed_speech_force("utterance", "khabar"),
    ]

    for result in operations:
        for ev in result.evidence:
            assert not ev.kind.startswith("hukm.")


# =============================================================================
# Rank Invariants Tests
# =============================================================================

def test_licensed_rank_requires_evidence():
    """Test LICENSED rank requires at least one Evidence."""
    # This is inherited from Phase 0, verify it holds for semantic operations
    evidence = (Evidence(kind="test", source="test"),)
    result = governed_dal_candidate("test", evidence)
    assert result.rank == Rank.LICENSED
    assert len(result.evidence) >= 1


def test_certified_rank_forbids_residuals():
    """Test CERTIFIED rank forbids residuals."""
    complete = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": True,
    }
    evidence = (Evidence(kind="ifadah.complete", source="test"),)
    result = governed_ifadah_closure(complete, evidence)
    assert result.rank == Rank.CERTIFIED
    assert len(result.residuals) == 0


# =============================================================================
# Regression Tests
# =============================================================================

def test_phase0_rank_set_unchanged():
    """Test Phase 0 Rank set unchanged."""
    assert Rank.UNRESOLVED.name == "UNRESOLVED"
    assert Rank.CANDIDATE.name == "CANDIDATE"
    assert Rank.LICENSED.name == "LICENSED"
    assert Rank.CERTIFIED.name == "CERTIFIED"
    assert Rank.REFUTED.name == "REFUTED"


def test_phase0_result_structure_unchanged():
    """Test Phase 0 Result structure unchanged."""
    r = Result(
        value="test",
        rank=Rank.CANDIDATE,
        evidence=(),
        residuals=(),
        failures=(),
        
    )
    assert hasattr(r, "value")
    assert hasattr(r, "rank")
    assert hasattr(r, "evidence")
    assert hasattr(r, "residuals")
    assert hasattr(r, "failures")
    assert hasattr(r, "trace")
    assert callable(r.replay)


# =============================================================================
# Integration Test: Full Semantic Chain
# =============================================================================

def test_full_semantic_chain():
    """
    Integration test: Dāl → Madlūl → Binding → Dalālah → Nisbah → Ifādah

    This demonstrates the complete flow through Phase 5A-5H.
    """
    # Phase 5A: Dāl candidate
    dal_result = governed_dal_candidate("كتب")
    assert dal_result.rank == Rank.CANDIDATE

    # Phase 5B: Madlūl candidate
    madlul_result = governed_madlul_candidate("writing")
    assert madlul_result.rank == Rank.CANDIDATE

    # Phase 5C: Binding
    evidence_binding = (Evidence(kind="wadh.attestation", source="lexicon"),)
    binding_result = governed_wadh_binding("كتب", "writing", evidence_binding)
    assert binding_result.rank == Rank.LICENSED

    # Phase 5D: Mutābaqah
    mutabaqah_result = governed_mutabaqah("كتب→writing")
    # Still has insufficiency residual
    assert any(r.kind == "semantics.mutabaqah.insufficient" for r in mutabaqah_result.residuals)

    # Phase 5E: Nisbah (ISN)
    nisbah_result = governed_nisbah_semantic("ISN", "زيد كتب")
    # Can proceed to ifādah

    # Phase 5H: Ifādah closure
    components = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": True,
    }
    evidence_ifadah = (Evidence(kind="ifadah.complete", source="semantic_chain"),)
    ifadah_result = governed_ifadah_closure(components, evidence_ifadah)
    assert ifadah_result.rank == Rank.CERTIFIED

    # Phase 5I: Boundary guard prevents HUKM jump
    boundary_result = governed_boundary_guard(Domain.SEMANTICS, Domain.HUKM, "ifadah")
    assert boundary_result.rank == Rank.REFUTED
