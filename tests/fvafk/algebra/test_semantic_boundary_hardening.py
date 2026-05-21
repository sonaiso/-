"""
Phase 5.5: Semantic Boundary Hardening Tests

Tests proving that Phase 5 semantic algebra enforces hard boundaries
against premature jumps and incomplete transitions.

These tests are **mutation-resistant**: if a developer removes gates or
relaxes boundaries, these tests must fail.

Test Categories:
    1. Dāl/Madlūl separation (Tests 1-3)
    2. Dalālah gate enforcement (Tests 4-6)
    3. Nisbah insufficiency (Tests 7-10)
    4. Reference completion (Test 11)

Hard Gates Tested (11 total):
    ✓ Dāl alone never becomes meaning
    ✓ Madlūl alone never becomes dalālah
    ✓ Dāl/Madlūl binding required before dalālah
    ✓ Mutābaqah alone does not become ifādah
    ✓ Taḍammun alone does not become ifādah
    ✓ Iltizām without gate is not licensed
    ✓ Majāz without qarīnah is not licensed
    ✓ Idāfah alone does not become ifādah
    ✓ Taqyīd alone does not become ifādah
    ✓ Conditional without jawāb does not become ifādah
    ✓ Pronoun without referent cannot certify ifādah
"""

import pytest
from src.fvafk.algebra.core import Result, Rank, Evidence, Residual, Carrier, Domain
from src.fvafk.algebra.semantics import (
    # Operations
    DalCandidateOperation,
    MadlulCandidateOperation,
    WadhBindingOperation,
    MutabaqahGate,
    TadammunGate,
    IltizamGate,
    NisbahSemanticOperation,
    ReferenceResolutionOperation,
    # Wrappers
    governed_dal_candidate,
    governed_madlul_candidate,
    governed_wadh_binding,
    governed_mutabaqah,
    governed_tadammun,
    governed_iltizam,
    governed_nisbah_semantic,
    governed_reference_resolution,
    # Residuals
    make_polysemy_possible,
    make_dal_binding_absent,
    make_mutabaqah_insufficient,
    make_tadammun_insufficient,
    make_iltizam_gate_missing,
    make_idafah_not_ifadah,
    make_taqyid_incomplete,
    make_conditional_jawab_missing,
    make_pronoun_referent_missing,
)


# =============================================================================
# Test Category 1: Dāl/Madlūl Separation (Tests 1-3)
# =============================================================================

def test_hard_gate_01_dal_alone_never_becomes_meaning():
    """
    Hard Gate 1: الدال وحده ليس معنى

    Dāl alone is NOT meaning. Even with evidence, dāl remains a signifier
    carrying polysemy residuals until bound to madlūl.

    Mutation resistance:
        - If developer removes polysemy residual → test fails
        - If developer promotes dāl to CERTIFIED → test fails
        - If developer skips binding requirement → test fails
    """
    # Test without evidence
    result_no_evidence = governed_dal_candidate("عين")
    assert result_no_evidence.rank != Rank.CERTIFIED, \
        "Dāl alone must never reach CERTIFIED (no meaning assigned)"
    assert any(r.kind == "semantics.polysemy.possible" for r in result_no_evidence.residuals), \
        "Dāl alone must carry polysemy residual"

    # Test with evidence (still not meaning)
    evidence = (Evidence(kind="lexicon.attestation", source="test"),)
    result_with_evidence = governed_dal_candidate("عين", evidence=evidence)
    assert result_with_evidence.rank in (Rank.CANDIDATE, Rank.LICENSED), \
        "Dāl with evidence can be LICENSED but never CERTIFIED without binding"
    assert any(r.kind == "semantics.polysemy.possible" for r in result_with_evidence.residuals), \
        "Dāl with evidence still carries polysemy residual"

    # Verify it never claims to be "meaning"
    assert all("meaning" not in str(e.kind).lower() for e in result_with_evidence.evidence), \
        "Dāl operation must not emit 'meaning' evidence"


def test_hard_gate_02_madlul_alone_never_becomes_dalalah():
    """
    Hard Gate 2: المدلول وحده ليس دلالة

    Madlūl alone is NOT dalālah. A signified candidate without dāl binding
    remains incomplete.

    Mutation resistance:
        - If developer removes dal_binding.absent residual → test fails
        - If developer promotes madlūl to CERTIFIED → test fails
    """
    result = governed_madlul_candidate("eye_meaning")

    assert result.rank != Rank.CERTIFIED, \
        "Madlūl alone must never reach CERTIFIED (no dalālah established)"
    assert any(r.kind == "semantics.dal_binding.absent" for r in result.residuals), \
        "Madlūl alone must carry dal_binding.absent residual"

    # Verify it never claims to be "dalālah"
    assert all("dalalah" not in str(e.kind).lower() for e in result.evidence), \
        "Madlūl operation must not emit 'dalālah' evidence"


def test_hard_gate_03_dal_madlul_binding_required_before_dalalah():
    """
    Hard Gate 3: لا دلالة بلا ربط

    No dalālah without binding. Dāl and madlūl must be explicitly bound
    before dalālah can be claimed.

    Mutation resistance:
        - If developer allows binding without evidence → test fails
        - If developer skips dalalah_gate.required residual → test fails
    """
    # Binding without evidence requires gate
    result_no_evidence = governed_wadh_binding("عين", "eye", evidence=())

    assert result_no_evidence.rank in (Rank.CANDIDATE, Rank.UNRESOLVED), \
        "Binding without evidence cannot be LICENSED or CERTIFIED"
    assert any(r.kind == "semantics.dalalah_gate.required" for r in result_no_evidence.residuals), \
        "Binding without evidence must require dalalah gate"

    # Binding with evidence can promote
    evidence = (Evidence(kind="wadh.conventional", source="test"),)
    result_with_evidence = governed_wadh_binding("عين", "eye", evidence=evidence)

    assert result_with_evidence.rank in (Rank.LICENSED, Rank.CERTIFIED), \
        "Binding with evidence can be LICENSED"

    # But binding alone is not ifādah
    assert all("ifadah" not in str(e.kind).lower() for e in result_with_evidence.evidence), \
        "Binding must not claim ifādah"


# =============================================================================
# Test Category 2: Dalālah Gate Enforcement (Tests 4-6)
# =============================================================================

def test_hard_gate_04_mutabaqah_alone_does_not_become_ifadah():
    """
    Hard Gate 4: المطابقة لا تصبح إفادة وحدها

    Mutābaqah (direct correspondence) is a pre-ifādah condition,
    not ifādah itself.

    Mutation resistance:
        - If developer removes mutabaqah.insufficient residual → test fails
        - If developer promotes mutābaqah to ifādah → test fails
    """
    binding = "رجل→man"

    result = governed_mutabaqah(binding)

    # Mutābaqah creates insufficiency residual
    assert any(r.kind == "semantics.mutabaqah.insufficient" for r in result.residuals), \
        "Mutābaqah must carry insufficiency residual"

    # Mutābaqah never claims ifādah
    assert all("ifadah" not in str(e.kind).lower() for e in result.evidence), \
        "Mutābaqah must not emit ifādah evidence"

    # Mutābaqah cannot reach CERTIFIED alone
    assert result.rank in (Rank.CANDIDATE, Rank.LICENSED), \
        "Mutābaqah with residual cannot be CERTIFIED"


def test_hard_gate_05_tadammun_alone_does_not_become_ifadah():
    """
    Hard Gate 5: التضمن لا يصبح إفادة وحده

    Taḍammun (partial inclusion) is a pre-ifādah condition,
    not ifādah itself.

    Mutation resistance:
        - If developer removes tadammun.insufficient residual → test fails
        - If developer promotes taḍammun to ifādah → test fails
    """
    binding = "يد→hand"
    part = "part_of_body"

    result = governed_tadammun(binding, part)

    # Taḍammun creates insufficiency residual
    assert any(r.kind == "semantics.tadammun.insufficient" for r in result.residuals), \
        "Taḍammun must carry insufficiency residual"

    # Taḍammun never claims ifādah
    assert all("ifadah" not in str(e.kind).lower() for e in result.evidence), \
        "Taḍammun must not emit ifādah evidence"

    # Taḍammun cannot reach CERTIFIED alone
    assert result.rank in (Rank.CANDIDATE, Rank.LICENSED), \
        "Taḍammun with residual cannot be CERTIFIED"


def test_hard_gate_06_iltizam_without_gate_is_not_licensed():
    """
    Hard Gate 6: الالتزام ليس تلقائياً

    Iltizām (entailment) requires explicit gate, not automatic.
    Without gate evidence, iltizām remains a candidate.

    Mutation resistance:
        - If developer removes iltizam.gate_missing residual → test fails
        - If developer auto-licenses iltizām → test fails
    """
    binding = "سقف→ceiling"
    consequence = "ceiling_implies_walls"

    # Iltizām without gate evidence
    result_no_gate = governed_iltizam(binding, consequence, evidence=())

    assert result_no_gate.rank in (Rank.CANDIDATE, Rank.UNRESOLVED), \
        "Iltizām without gate must not be LICENSED"
    assert any(r.kind == "semantics.iltizam.gate_missing" for r in result_no_gate.residuals), \
        "Iltizām without gate must carry gate_missing residual"

    # Iltizām with gate evidence can be licensed
    evidence = (Evidence(kind="iltizam.logical", source="test"),)
    result_with_gate = governed_iltizam(binding, consequence, evidence=evidence)

    assert result_with_gate.rank in (Rank.LICENSED, Rank.CERTIFIED), \
        "Iltizām with gate can be LICENSED"


def test_hard_gate_07_majaz_without_qarinah_is_not_licensed():
    """
    Hard Gate 7: المجاز بلا قرينة ليس مرخصاً

    Majāz (metaphor/figurative) without qarīnah (contextual indicator)
    cannot be licensed. This is modeled as iltizām requiring gate.

    Mutation resistance:
        - If developer auto-promotes majāz → test fails
        - If developer skips qarīnah requirement → test fails
    """
    binding = "أسد→lion"
    majaz_consequence = "brave_man_not_lion"

    # Majāz without qarīnah (no evidence)
    result_no_qarinah = governed_iltizam(binding, majaz_consequence, evidence=())

    assert result_no_qarinah.rank != Rank.LICENSED, \
        "Majāz without qarīnah must not be LICENSED"
    assert any(r.kind == "semantics.iltizam.gate_missing" for r in result_no_qarinah.residuals), \
        "Majāz without qarīnah must require gate"

    # Majāz with qarīnah (contextual evidence)
    evidence = (Evidence(kind="iltizam.contextual", source="qarinah:context_indicates_metaphor"),)
    result_with_qarinah = governed_iltizam(binding, majaz_consequence, evidence=evidence)

    assert result_with_qarinah.rank in (Rank.LICENSED, Rank.CERTIFIED), \
        "Majāz with qarīnah can be LICENSED"


# =============================================================================
# Test Category 3: Nisbah Insufficiency (Tests 8-10)
# =============================================================================

def test_hard_gate_08_idafah_alone_does_not_become_ifadah():
    """
    Hard Gate 8: النسبة الإضافية لا تصبح إفادة

    Iḍāfah (possessive relation) alone does not become ifādah.
    It requires complete predication.

    Mutation resistance:
        - If developer removes idafah.not_ifadah residual → test fails
        - If developer promotes iḍāfah to ifādah → test fails
    """
    nisbah_type = "IDAFA"
    parties = ("كتاب", "زيد")

    result = governed_nisbah_semantic(nisbah_type, parties, evidence=())

    assert any(r.kind == "semantics.idafah.not_ifadah" for r in result.residuals), \
        "Iḍāfah must carry not_ifadah residual"

    # Iḍāfah never claims ifādah
    assert all("ifadah" not in str(e.kind).lower() for e in result.evidence), \
        "Iḍāfah must not emit ifādah evidence"

    assert result.rank != Rank.CERTIFIED, \
        "Iḍāfah with residual cannot be CERTIFIED"


def test_hard_gate_09_taqyid_alone_does_not_become_ifadah():
    """
    Hard Gate 9: التقييد لا يصبح إفادة حتى يكمل الإسناد

    Taqyīd (modification) alone does not become ifādah until
    complete predication.

    Mutation resistance:
        - If developer removes taqyid.incomplete residual → test fails
        - If developer promotes taqyīd to ifādah → test fails
    """
    nisbah_type = "TAQYID"
    parties = ("في البيت", "modifier")

    result = governed_nisbah_semantic(nisbah_type, parties, evidence=())

    assert any(r.kind == "semantics.taqyid.incomplete" for r in result.residuals), \
        "Taqyīd must carry incomplete residual"

    # Taqyīd never claims ifādah alone
    assert all("ifadah" not in str(e.kind).lower() for e in result.evidence), \
        "Taqyīd must not emit ifādah evidence"


def test_hard_gate_10_conditional_without_jawab_does_not_become_ifadah():
    """
    Hard Gate 10: الشرط بلا جواب لا يصبح إفادة

    Conditional (shart) without jawāb (answer clause) does not
    become ifādah.

    Mutation resistance:
        - If developer removes conditional.jawab_missing residual → test fails
        - If developer allows shart alone to be ifādah → test fails
    """
    nisbah_type = "SHART"
    parties = ("إن تدرس", "condition_without_answer")

    result = governed_nisbah_semantic(nisbah_type, parties, evidence=())

    assert any(r.kind == "semantics.conditional.jawab_missing" for r in result.residuals), \
        "Conditional without jawāb must carry jawab_missing residual"

    # Conditional without jawāb never claims ifādah
    assert all("ifadah" not in str(e.kind).lower() for e in result.evidence), \
        "Conditional without jawāb must not emit ifādah evidence"

    assert result.rank != Rank.CERTIFIED, \
        "Conditional without jawāb cannot be CERTIFIED"


# =============================================================================
# Test Category 4: Reference Completion (Test 11)
# =============================================================================

def test_hard_gate_11_pronoun_without_referent_cannot_certify_ifadah():
    """
    Hard Gate 11: الضمير بلا مرجع لا يصبح إفادة معتمدة

    Pronoun without referent cannot produce CERTIFIED ifādah.
    It remains CANDIDATE or LICENSED with residuals.

    Mutation resistance:
        - If developer removes pronoun.referent_missing residual → test fails
        - If developer certifies ifādah with missing referent → test fails
    """
    pronoun = "هو"
    referent = None  # Missing referent

    result = governed_reference_resolution(pronoun, referent, evidence=())

    assert any(r.kind == "semantics.pronoun.referent_missing" for r in result.residuals), \
        "Pronoun without referent must carry referent_missing residual"

    assert result.rank != Rank.CERTIFIED, \
        "Pronoun without referent cannot be CERTIFIED"

    # With referent, can be licensed
    result_with_referent = governed_reference_resolution(pronoun, "زيد", evidence=())
    assert result_with_referent.rank in (Rank.CANDIDATE, Rank.LICENSED), \
        "Pronoun with referent can be CANDIDATE or LICENSED"


# =============================================================================
# Mutation Resistance Tests
# =============================================================================

def test_mutation_resistance_residual_kinds_unchanged():
    """
    Verify that no developer has removed semantic residual kinds.

    This test acts as a canary: if someone removes a residual kind,
    the count changes and this test fails.
    """
    from src.fvafk.algebra.semantics import SEMANTICS_RESIDUAL_KINDS

    assert len(SEMANTICS_RESIDUAL_KINDS) == 13, \
        "SEMANTICS_RESIDUAL_KINDS must contain exactly 13 residuals"

    required_kinds = {
        "semantics.polysemy.possible",
        "semantics.dal_binding.absent",
        "semantics.dalalah_gate.required",
        "semantics.mutabaqah.insufficient",
        "semantics.tadammun.insufficient",
        "semantics.iltizam.gate_missing",
        "semantics.idafah.not_ifadah",
        "semantics.taqyid.incomplete",
        "semantics.conditional.jawab_missing",
        "semantics.pronoun.referent_missing",
        "semantics.speech_force.uncertain",
        "semantics.ifadah.incomplete",
        "semantics.hukm_boundary.violation",
    }

    assert set(SEMANTICS_RESIDUAL_KINDS) == required_kinds, \
        "SEMANTICS_RESIDUAL_KINDS must not be modified"


def test_mutation_resistance_operations_exist():
    """
    Verify that all Phase 5 operations still exist.

    If a developer removes an operation, this test fails.
    """
    from src.fvafk.algebra.semantics import (
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
    )

    operations = [
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
    ]

    assert len(operations) == 11, \
        "Phase 5 must maintain all 11 operations"


# =============================================================================
# Integration Tests
# =============================================================================

def test_integration_full_chain_respects_all_gates():
    """
    Integration test: Full semantic chain respects all hard gates.

    Tests the complete flow: Dāl → Madlūl → Binding → Dalālah → Nisbah

    Verifies that each step:
    - Cannot skip required gates
    - Cannot bypass residuals
    - Cannot jump to ifādah prematurely
    """
    # Step 1: Dāl candidate
    dal_result = governed_dal_candidate("كتب")
    assert dal_result.rank != Rank.CERTIFIED
    assert any(r.kind == "semantics.polysemy.possible" for r in dal_result.residuals)

    # Step 2: Madlūl candidate
    madlul_result = governed_madlul_candidate("write_concept")
    assert madlul_result.rank != Rank.CERTIFIED
    assert any(r.kind == "semantics.dal_binding.absent" for r in madlul_result.residuals)

    # Step 3: Binding without evidence
    binding_no_ev = governed_wadh_binding("كتب", "write", evidence=())
    assert binding_no_ev.rank in (Rank.CANDIDATE, Rank.UNRESOLVED)

    # Step 4: Binding with evidence
    evidence = (Evidence(kind="wadh.conventional", source="lexicon"),)
    binding_with_ev = governed_wadh_binding("كتب", "write", evidence=evidence)
    assert binding_with_ev.rank in (Rank.LICENSED, Rank.CERTIFIED)

    # Step 5: Mutābaqah still not ifādah
    binding = "كتب→write"
    mutabaqah_result = governed_mutabaqah(binding)
    assert any(r.kind == "semantics.mutabaqah.insufficient" for r in mutabaqah_result.residuals)
    assert all("ifadah" not in str(e.kind).lower() for e in mutabaqah_result.evidence)
