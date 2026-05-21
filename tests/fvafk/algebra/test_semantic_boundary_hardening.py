"""Semantic boundary hardening tests with 28 mutation-resistant tests.

These tests defend the hard boundaries declared in Phase 5 (Semantic Algebra)
against silent mutation. They test:

1. Hard Gate Enforcement (12 tests)
   - Dāl alone is NOT meaning
   - Madlūl alone is NOT dalālah
   - Wadh' binding requires evidence
   - Mutābaqah alone is NOT ifādah
   - Taḍammun alone is NOT ifādah
   - Iltizām requires explicit gate
   - Iḍāfah alone is NOT ifādah
   - Taqyīd alone is incomplete
   - Conditional without jawāb is incomplete
   - Pronoun without referent cannot be CERTIFIED
   - Speech force determines illocution, NOT hukm
   - Ifādah with residuals cannot be CERTIFIED

2. Forbidden Jumps (8 tests)
   - SEMANTICS cannot jump to HUKM
   - IFADAH cannot issue HUKM
   - Khabar is NOT hukm
   - Amr is NOT obligation (at Phase 5)
   - Nahy is NOT prohibition (at Phase 5)
   - Istifhām is NOT interrogation-hukm
   - Shart is NOT conditional-hukm
   - Tamanni is NOT wish-hukm

3. Rank Discipline (8 tests)
   - LICENSED requires evidence
   - CERTIFIED requires evidence + no residuals
   - CANDIDATE without evidence is acceptable
   - REFUTED on boundary violation
   - REFUTED on fatal failure
   - Rank downgrade on residual addition
   - Rank preservation on non-fatal failure
   - CERTIFIED cannot have residuals
"""

from __future__ import annotations

import pytest

from fvafk.algebra import Rank, Evidence, Residual, Failure, Carrier, Domain
from fvafk.algebra.semantics import (
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


def _ev(source: str = "test") -> Evidence:
    """Create test evidence."""
    return Evidence(kind="test.evidence", source=source, detail="ok")


# =============================================================================
# Hard Gate Enforcement Tests (12 tests)
# =============================================================================


def test_hard_gate_01_dal_alone_is_not_meaning():
    """Dāl alone must have polysemy residual, never CERTIFIED."""
    result_without_evidence = governed_dal_candidate("كتاب")
    assert result_without_evidence.rank == Rank.CANDIDATE
    assert len(result_without_evidence.residuals) > 0
    assert any("polysemy" in r.kind for r in result_without_evidence.residuals)

    result_with_evidence = governed_dal_candidate("كتاب", evidence=(_ev(),))
    assert result_with_evidence.rank == Rank.LICENSED
    # Still has polysemy residual even with evidence
    assert len(result_with_evidence.residuals) > 0
    assert any("polysemy" in r.kind for r in result_with_evidence.residuals)


def test_hard_gate_02_madlul_alone_is_not_dalalah():
    """Madlūl alone must have dal_binding residual."""
    result_without_evidence = governed_madlul_candidate("book")
    assert result_without_evidence.rank == Rank.CANDIDATE
    assert len(result_without_evidence.residuals) > 0
    assert any("dal_binding" in r.kind for r in result_without_evidence.residuals)

    result_with_evidence = governed_madlul_candidate("book", evidence=(_ev(),))
    assert result_with_evidence.rank == Rank.LICENSED
    # Still has dal_binding residual
    assert len(result_with_evidence.residuals) > 0


def test_hard_gate_03_wadh_binding_requires_evidence():
    """Wadh' binding without evidence is CANDIDATE with residual."""
    result_without_evidence = governed_wadh_binding("كتاب", "book")
    assert result_without_evidence.rank == Rank.CANDIDATE
    assert len(result_without_evidence.residuals) > 0
    assert any("dalalah_gate" in r.kind for r in result_without_evidence.residuals)

    result_with_evidence = governed_wadh_binding("كتاب", "book", evidence=(_ev(),))
    assert result_with_evidence.rank == Rank.LICENSED
    assert len(result_with_evidence.residuals) == 0


def test_hard_gate_04_mutabaqah_alone_is_not_ifadah():
    """Mutābaqah alone is insufficient for ifādah."""
    result_without_evidence = governed_mutabaqah("كتاب→book")
    assert result_without_evidence.rank == Rank.CANDIDATE
    assert len(result_without_evidence.residuals) > 0
    assert any("mutabaqah.insufficient" in r.kind for r in result_without_evidence.residuals)

    result_with_evidence = governed_mutabaqah("كتاب→book", evidence=(_ev(),))
    assert result_with_evidence.rank == Rank.LICENSED
    # Still has mutabaqah.insufficient residual
    assert len(result_with_evidence.residuals) > 0


def test_hard_gate_05_tadammun_alone_is_not_ifadah():
    """Taḍammun alone is insufficient for ifādah."""
    result_without_evidence = governed_tadammun("كتاب→book", "paper")
    assert result_without_evidence.rank == Rank.CANDIDATE
    assert len(result_without_evidence.residuals) > 0
    assert any("tadammun.insufficient" in r.kind for r in result_without_evidence.residuals)

    result_with_evidence = governed_tadammun("كتاب→book", "paper", evidence=(_ev(),))
    assert result_with_evidence.rank == Rank.LICENSED
    # Still has tadammun.insufficient residual
    assert len(result_with_evidence.residuals) > 0


def test_hard_gate_06_iltizam_without_gate_is_not_licensed():
    """Iltizām requires explicit gate to be LICENSED."""
    # Without gate type or evidence
    result_without_gate = governed_iltizam("كتاب→book", "writing")
    assert result_without_gate.rank == Rank.CANDIDATE
    assert len(result_without_gate.residuals) > 0
    assert any("iltizam.gate_missing" in r.kind for r in result_without_gate.residuals), \
        "Iltizām without gate must have iltizam.gate_missing residual"

    # With gate type and evidence
    result_with_gate = governed_iltizam(
        "كتاب→book", "writing",
        gate_type="logical",
        evidence=(_ev("logical_gate"),)
    )
    assert result_with_gate.rank in (Rank.LICENSED, Rank.CERTIFIED), \
        "Iltizām with gate can be LICENSED"
    # Check that residuals are empty when gate is provided
    assert len(result_with_gate.residuals) == 0, \
        "Iltizām with gate should have no residuals"


def test_hard_gate_07_idafah_alone_is_not_ifadah():
    """Iḍāfah alone does not become ifādah."""
    result_without_evidence = governed_nisbah_semantic("IDAFA", "كتاب+محمد")
    assert result_without_evidence.rank == Rank.CANDIDATE
    assert len(result_without_evidence.residuals) > 0
    assert any("idafah.not_ifadah" in r.kind for r in result_without_evidence.residuals)

    result_with_evidence = governed_nisbah_semantic("IDAFA", "كتاب+محمد", evidence=(_ev(),))
    assert result_with_evidence.rank == Rank.LICENSED
    # Still has idafah.not_ifadah residual
    assert len(result_with_evidence.residuals) > 0


def test_hard_gate_08_taqyid_alone_is_incomplete():
    """Taqyīd alone is incomplete without predication."""
    result_without_evidence = governed_nisbah_semantic("TAQYID", "في البيت")
    assert result_without_evidence.rank == Rank.CANDIDATE
    assert len(result_without_evidence.residuals) > 0
    assert any("taqyid.incomplete" in r.kind for r in result_without_evidence.residuals)

    result_with_evidence = governed_nisbah_semantic("TAQYID", "في البيت", evidence=(_ev(),))
    assert result_with_evidence.rank == Rank.LICENSED
    # Still has taqyid.incomplete residual
    assert len(result_with_evidence.residuals) > 0


def test_hard_gate_09_conditional_without_jawab_is_incomplete():
    """Conditional (shart) without jawāb is incomplete."""
    result = governed_nisbah_semantic("SHART", "إن تدرس")
    assert result.rank == Rank.CANDIDATE
    assert len(result.residuals) > 0
    assert any("conditional.jawab_missing" in r.kind for r in result.residuals)


def test_hard_gate_10_pronoun_without_referent_cannot_be_certified():
    """Pronoun without referent cannot be CERTIFIED."""
    result_without_referent = governed_reference_resolution("هو")
    assert result_without_referent.rank == Rank.CANDIDATE
    assert len(result_without_referent.residuals) > 0
    assert any("pronoun.referent_missing" in r.kind for r in result_without_referent.residuals)

    result_with_referent = governed_reference_resolution("هو", referent="محمد", evidence=(_ev(),))
    assert result_with_referent.rank == Rank.LICENSED
    assert len(result_with_referent.residuals) == 0


def test_hard_gate_11_speech_force_not_hukm():
    """Speech force (khabar, inshā, etc.) is NOT hukm."""
    result_uncertain = governed_speech_force("محمد كاتب")
    assert result_uncertain.rank == Rank.CANDIDATE
    assert len(result_uncertain.residuals) > 0
    assert any("speech_force.uncertain" in r.kind for r in result_uncertain.residuals)

    result_khabar = governed_speech_force("محمد كاتب", force="khabar", evidence=(_ev(),))
    assert result_khabar.rank == Rank.LICENSED
    # Khabar is not hukm, just speech force
    assert len(result_khabar.residuals) == 0


def test_hard_gate_12_ifadah_with_residuals_cannot_be_certified():
    """Ifādah with residuals cannot be CERTIFIED."""
    # Complete components
    complete_components = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": True,
    }

    result_complete = governed_ifadah_closure(complete_components, evidence=(_ev(),))
    assert result_complete.rank == Rank.CERTIFIED
    assert len(result_complete.residuals) == 0

    # Incomplete components
    incomplete_components = {
        "parties": True,
        "binding": True,
        "dalalah": False,  # Missing
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": True,
    }

    result_incomplete = governed_ifadah_closure(incomplete_components, evidence=(_ev(),))
    assert result_incomplete.rank == Rank.CANDIDATE
    assert len(result_incomplete.residuals) > 0
    assert any("ifadah.incomplete" in r.kind for r in result_incomplete.residuals)


# =============================================================================
# Forbidden Jumps Tests (8 tests)
# =============================================================================


def test_forbidden_jump_01_semantics_cannot_jump_to_hukm():
    """SEMANTICS→HUKM jump must be REFUTED."""
    result = governed_boundary_guard(Domain.SEMANTICS, Domain.HUKM, "test")
    assert result.rank == Rank.REFUTED
    assert any(f.fatal for f in result.failures)
    assert any("boundary.violation" in f.kind for f in result.failures)


def test_forbidden_jump_02_ifadah_cannot_issue_hukm():
    """IFADAH cannot issue HUKM (tested via boundary guard)."""
    result = governed_boundary_guard(Domain.SEMANTICS, Domain.HUKM, "ifadah")
    assert result.rank == Rank.REFUTED
    assert len(result.failures) > 0
    assert any(f.fatal for f in result.failures)


def test_forbidden_jump_03_khabar_is_not_hukm():
    """Khabar (declarative) is NOT hukm at Phase 5."""
    result = governed_speech_force("محمد كاتب", force="khabar", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    # Khabar does not jump to HUKM
    assert result.value.startswith("speech_force:khabar")


def test_forbidden_jump_04_amr_is_not_obligation():
    """Amr (command) is NOT obligation at Phase 5."""
    result = governed_speech_force("اكتب", force="amr", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    # Amr is speech force, not HUKM obligation
    assert result.value.startswith("speech_force:amr")


def test_forbidden_jump_05_nahy_is_not_prohibition():
    """Nahy (prohibition) is NOT legal prohibition at Phase 5."""
    result = governed_speech_force("لا تكتب", force="nahy", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    # Nahy is speech force, not HUKM prohibition
    assert result.value.startswith("speech_force:nahy")


def test_forbidden_jump_06_istifham_is_not_interrogation_hukm():
    """Istifhām is NOT interrogation-hukm at Phase 5."""
    result = governed_speech_force("هل كتبت", force="istifham", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    # Istifhām is speech force, not HUKM
    assert result.value.startswith("speech_force:istifham")


def test_forbidden_jump_07_shart_is_not_conditional_hukm():
    """Shart (conditional) is NOT conditional-hukm at Phase 5."""
    result = governed_speech_force("إن تدرس تنجح", force="shart", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    # Shart is speech force, not HUKM
    assert result.value.startswith("speech_force:shart")


def test_forbidden_jump_08_tamanni_is_not_wish_hukm():
    """Tamanni (wish) is NOT wish-hukm at Phase 5."""
    result = governed_speech_force("ليتني كنت معهم", force="tamanni", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    # Tamanni is speech force, not HUKM
    assert result.value.startswith("speech_force:tamanni")


# =============================================================================
# Rank Discipline Tests (8 tests)
# =============================================================================


def test_rank_discipline_01_licensed_requires_evidence():
    """LICENSED rank requires at least one Evidence."""
    # WadhBindingOperation with evidence → LICENSED
    result = governed_wadh_binding("كتاب", "book", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    assert len(result.evidence) > 0


def test_rank_discipline_02_certified_requires_evidence_and_no_residuals():
    """CERTIFIED requires evidence + no residuals."""
    complete_components = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": True,
    }

    result = governed_ifadah_closure(complete_components, evidence=(_ev(),))
    assert result.rank == Rank.CERTIFIED
    assert len(result.evidence) > 0
    assert len(result.residuals) == 0


def test_rank_discipline_03_candidate_without_evidence_acceptable():
    """CANDIDATE without evidence is acceptable."""
    result = governed_dal_candidate("كتاب")
    assert result.rank == Rank.CANDIDATE
    assert len(result.evidence) == 0


def test_rank_discipline_04_refuted_on_boundary_violation():
    """REFUTED on boundary violation."""
    result = governed_boundary_guard(Domain.SEMANTICS, Domain.HUKM, "test")
    assert result.rank == Rank.REFUTED
    assert any(f.fatal for f in result.failures)


def test_rank_discipline_05_refuted_on_fatal_failure():
    """REFUTED when fatal failure is added."""
    from fvafk.algebra import Result

    result = Result(
        value="test",
        rank=Rank.LICENSED,
        evidence=(_ev(),)
    )

    # Add fatal failure
    refuted = result.with_failure(Failure(kind="test", description="fatal", fatal=True))
    assert refuted.rank == Rank.REFUTED


def test_rank_discipline_06_rank_preserved_on_non_fatal_failure():
    """Rank preserved when non-fatal failure is added."""
    from fvafk.algebra import Result

    result = Result(
        value="test",
        rank=Rank.LICENSED,
        evidence=(_ev(),)
    )

    # Add non-fatal failure
    same = result.with_failure(Failure(kind="test", description="warning", fatal=False))
    assert same.rank == Rank.LICENSED


def test_rank_discipline_07_certified_cannot_have_residuals():
    """CERTIFIED cannot have residuals (constructor enforces this)."""
    from fvafk.algebra import Result

    with pytest.raises(ValueError, match="CERTIFIED.*residuals"):
        Result(
            value="test",
            rank=Rank.CERTIFIED,
            evidence=(_ev(),),
            residuals=(Residual(kind="test", description="leftover"),)
        )


def test_rank_discipline_08_licensed_or_certified_requires_evidence():
    """LICENSED/CERTIFIED without evidence is rejected."""
    from fvafk.algebra import Result

    with pytest.raises(ValueError, match="LICENSED.*Evidence"):
        Result(value="test", rank=Rank.LICENSED)

    with pytest.raises(ValueError, match="LICENSED.*Evidence"):
        Result(value="test", rank=Rank.CERTIFIED)
