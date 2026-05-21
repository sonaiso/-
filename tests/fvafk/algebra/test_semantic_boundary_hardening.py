"""
Phase 5.5: Semantic Boundary Hardening with 28 Mutation-Resistant Tests

Comprehensive mutation-resistant test suite for all 9 semantic operations across
Phase 5A-5I.

Test Strategy:
    Each operation tested with:
        1. Hard gate: what MUST fail (REFUTED or CANDIDATE)
        2. Soft gate: what MAY succeed (LICENSED)
        3. Certificate path: what CAN reach CERTIFIED (if applicable)

Coverage:
    - Phase 5A: DalCandidateOperation (3 tests)
    - Phase 5B: MadlulCandidateOperation (3 tests)
    - Phase 5C: WadhBindingOperation (3 tests)
    - Phase 5D: MutabaqahGate (2 tests)
    - Phase 5D: TadammunGate (2 tests)
    - Phase 5D: IltizamGate (3 tests)
    - Phase 5E: NisbahSemanticOperation (4 tests)
    - Phase 5F: ReferenceResolutionOperation (2 tests)
    - Phase 5G: SpeechForceOperation (2 tests)
    - Phase 5H: IfadahClosureOperation (2 tests)
    - Phase 5I: BoundaryGuardOperation (2 tests)

Total: 28 tests
"""

from __future__ import annotations

import pytest

from fvafk.algebra import (
    Carrier,
    Domain,
    Evidence,
    Rank,
    Result,
)
from fvafk.algebra.semantics import (
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


# =============================================================================
# Phase 5A: Dāl Candidate Operation (3 tests)
# =============================================================================

def test_hard_gate_01_dal_without_evidence_is_candidate():
    """Dāl alone without evidence must be CANDIDATE."""
    op = DalCandidateOperation()
    carrier = Carrier(domain=Domain.SEMANTICS, value="كتاب")
    result = op.run(carrier, evidence=())

    # Hard gate: no evidence → CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.polysemy.possible" for r in result.residuals)


def test_soft_gate_01_dal_with_evidence_is_licensed():
    """Dāl with evidence can be LICENSED."""
    op = DalCandidateOperation()
    carrier = Carrier(domain=Domain.SEMANTICS, value="كتاب")
    ev = (Evidence(kind="test.dal", source="lexicon", detail="attested"),)
    result = op.run(carrier, evidence=ev)

    # Soft gate: evidence → LICENSED
    assert result.rank is Rank.LICENSED
    # But still has polysemy residual (cannot be CERTIFIED)
    assert result.residuals
    assert any(r.kind == "semantics.polysemy.possible" for r in result.residuals)


def test_hard_gate_02_dal_from_wrong_domain_is_refuted():
    """Dāl from wrong domain must be REFUTED."""
    op = DalCandidateOperation()
    carrier = Carrier(domain=Domain.GRAPHEME, value="كتاب")
    result = op.run(carrier, evidence=())

    # Hard gate: domain mismatch → REFUTED
    assert result.rank is Rank.REFUTED
    assert result.failures
    assert any(f.fatal for f in result.failures)


# =============================================================================
# Phase 5B: Madlūl Candidate Operation (3 tests)
# =============================================================================

def test_hard_gate_03_madlul_without_evidence_is_candidate():
    """Madlūl alone without evidence must be CANDIDATE."""
    op = MadlulCandidateOperation()
    carrier = Carrier(domain=Domain.SEMANTICS, value="written_object")
    result = op.run(carrier, evidence=())

    # Hard gate: no evidence → CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.dal_binding.absent" for r in result.residuals)


def test_soft_gate_02_madlul_with_evidence_is_licensed():
    """Madlūl with evidence can be LICENSED."""
    op = MadlulCandidateOperation()
    carrier = Carrier(domain=Domain.SEMANTICS, value="written_object")
    ev = (Evidence(kind="test.madlul", source="semantic_category", detail="concrete"),)
    result = op.run(carrier, evidence=ev)

    # Soft gate: evidence → LICENSED
    assert result.rank is Rank.LICENSED
    # But still has binding residual (cannot be CERTIFIED)
    assert result.residuals
    assert any(r.kind == "semantics.dal_binding.absent" for r in result.residuals)


def test_hard_gate_04_madlul_from_wrong_domain_is_refuted():
    """Madlūl from non-SEMANTICS domain must be REFUTED."""
    op = MadlulCandidateOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value="written_object")
    result = op.run(carrier, evidence=())

    # Hard gate: domain mismatch → REFUTED
    assert result.rank is Rank.REFUTED
    assert result.failures
    assert any(f.fatal for f in result.failures)


# =============================================================================
# Phase 5C: Wadh' Binding Operation (3 tests)
# =============================================================================

def test_hard_gate_05_wadh_without_evidence_is_candidate():
    """Wadh' binding without evidence must be CANDIDATE."""
    op = WadhBindingOperation()
    result = op.run(dal="كتاب", madlul="written_object", evidence=())

    # Hard gate: no evidence → CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.dalalah_gate.required" for r in result.residuals)


def test_soft_gate_03_wadh_with_evidence_is_licensed():
    """Wadh' binding with evidence can be LICENSED."""
    op = WadhBindingOperation()
    ev = (Evidence(kind="test.wadh", source="convention", detail="established"),)
    result = op.run(dal="كتاب", madlul="written_object", evidence=ev)

    # Soft gate: evidence → LICENSED
    assert result.rank is Rank.LICENSED
    assert not result.residuals


def test_certificate_01_wadh_with_full_evidence_is_licensed_not_certified():
    """Wadh' binding reaches LICENSED but not CERTIFIED (binding is pre-ifādah)."""
    op = WadhBindingOperation()
    ev = (Evidence(kind="test.wadh", source="convention", detail="established"),)
    result = op.run(dal="كتاب", madlul="written_object", evidence=ev)

    # Certificate check: binding is LICENSED, not CERTIFIED
    assert result.rank is Rank.LICENSED
    # Binding alone doesn't reach CERTIFIED (requires full ifādah)
    assert result.rank is not Rank.CERTIFIED


# =============================================================================
# Phase 5D: Mutābaqah Gate (2 tests)
# =============================================================================

def test_soft_gate_04_mutabaqah_with_evidence_is_licensed():
    """Mutābaqah with evidence can be LICENSED."""
    gate = MutabaqahGate()
    ev = (Evidence(kind="test.mutabaqah", source="direct_correspondence", detail="verified"),)
    result = gate.run(binding="دار→بيت", evidence=ev)

    # Soft gate: evidence → LICENSED
    assert result.rank is Rank.LICENSED
    # But still insufficient for ifādah
    assert result.residuals
    assert any(r.kind == "semantics.mutabaqah.insufficient" for r in result.residuals)


def test_certificate_02_mutabaqah_never_reaches_certified():
    """Mutābaqah alone never reaches CERTIFIED (pre-ifādah condition)."""
    gate = MutabaqahGate()
    ev = (Evidence(kind="test.mutabaqah", source="direct_correspondence", detail="verified"),)
    result = gate.run(binding="دار→بيت", evidence=ev)

    # Certificate check: always has residual
    assert result.rank is not Rank.CERTIFIED
    assert result.residuals


# =============================================================================
# Phase 5D: Taḍammun Gate (2 tests)
# =============================================================================

def test_soft_gate_05_tadammun_with_evidence_is_licensed():
    """Taḍammun with evidence can be LICENSED."""
    gate = TadammunGate()
    ev = (Evidence(kind="test.tadammun", source="partial_inclusion", detail="verified"),)
    result = gate.run(binding="سقف→بيت", part="جزء", evidence=ev)

    # Soft gate: evidence → LICENSED
    assert result.rank is Rank.LICENSED
    # But still insufficient for ifādah
    assert result.residuals
    assert any(r.kind == "semantics.tadammun.insufficient" for r in result.residuals)


def test_certificate_03_tadammun_never_reaches_certified():
    """Taḍammun alone never reaches CERTIFIED (pre-ifādah condition)."""
    gate = TadammunGate()
    ev = (Evidence(kind="test.tadammun", source="partial_inclusion", detail="verified"),)
    result = gate.run(binding="سقف→بيت", part="جزء", evidence=ev)

    # Certificate check: always has residual
    assert result.rank is not Rank.CERTIFIED
    assert result.residuals


# =============================================================================
# Phase 5D: Iltizām Gate (3 tests)
# =============================================================================

def test_hard_gate_06_iltizam_without_gate_is_not_licensed():
    """Iltizām without gate is not licensed; with gate can be LICENSED."""
    gate = IltizamGate()

    # Part 1: Without gate → NOT LICENSED (CANDIDATE)
    result_without_gate = gate.run(
        binding="طلوع:الشمس",
        consequence="نهار",
        gate_type="",
        evidence=()
    )

    # Hard gate: no gate_type → CANDIDATE (not licensed)
    assert result_without_gate.rank is Rank.CANDIDATE
    assert result_without_gate.residuals
    assert any(r.kind == "semantics.iltizam.gate_missing" for r in result_without_gate.residuals)

    # Part 2: With gate → CAN be LICENSED
    ev = (Evidence(kind="test.iltizam", source="logical_entailment", detail="causality"),)
    result_with_gate = gate.run(
        binding="طلوع:الشمس",
        consequence="نهار",
        gate_type="logical",
        evidence=ev
    )

    # Soft gate: gate_type + evidence → LICENSED
    assert result_with_gate.rank in (Rank.LICENSED, Rank.CERTIFIED), \
        "Iltizām with gate can be LICENSED"
    assert not result_with_gate.residuals


def test_certificate_04_iltizam_with_gate_is_licensed_not_certified():
    """Iltizām with gate reaches LICENSED but not CERTIFIED (pre-ifādah)."""
    gate = IltizamGate()
    ev = (Evidence(kind="test.iltizam", source="logical_entailment", detail="causality"),)
    result = gate.run(
        binding="طلوع:الشمس",
        consequence="نهار",
        gate_type="logical",
        evidence=ev
    )

    # Certificate check: LICENSED, not CERTIFIED
    assert result.rank is Rank.LICENSED
    assert result.rank is not Rank.CERTIFIED


# =============================================================================
# Phase 5E: Nisbah Semantic Operation (4 tests)
# =============================================================================

def test_hard_gate_07_idafah_always_has_residual():
    """Iḍāfah nisbah always has residual (never becomes ifādah)."""
    op = NisbahSemanticOperation()
    ev = (Evidence(kind="test.nisbah", source="idafa_structure", detail="detected"),)
    result = op.run(nisbah_type="IDAFA", parties="كتاب:الطالب", evidence=ev)

    # Hard gate: IDAFA always has residual
    assert result.residuals
    assert any(r.kind == "semantics.idafah.not_ifadah" for r in result.residuals)
    # Can be LICENSED but not CERTIFIED
    assert result.rank is not Rank.CERTIFIED


def test_hard_gate_08_conditional_always_has_jawab_residual():
    """Conditional nisbah always has jawāb residual."""
    op = NisbahSemanticOperation()
    result = op.run(nisbah_type="SHART", parties="إن:تدرس", evidence=())

    # Hard gate: SHART always has jawab residual
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.conditional.jawab_missing" for r in result.residuals)


def test_soft_gate_07_taqyid_with_evidence_is_licensed():
    """Taqyīd with evidence can be LICENSED."""
    op = NisbahSemanticOperation()
    ev = (Evidence(kind="test.nisbah", source="taqyid_modifier", detail="detected"),)
    result = op.run(nisbah_type="TAQYID", parties="في:البيت", evidence=ev)

    # Soft gate: evidence → LICENSED
    assert result.rank is Rank.LICENSED
    # But still incomplete
    assert result.residuals
    assert any(r.kind == "semantics.taqyid.incomplete" for r in result.residuals)


def test_soft_gate_08_isnadi_with_evidence_is_licensed():
    """Isnadi nisbah with evidence can be LICENSED."""
    op = NisbahSemanticOperation()
    ev = (Evidence(kind="test.nisbah", source="isn_structure", detail="predication"),)
    result = op.run(nisbah_type="ISN", parties="الطالب:مجتهد", evidence=ev)

    # Soft gate: ISN + evidence → LICENSED
    assert result.rank is Rank.LICENSED
    # ISN has no inherent residual (may lead to ifādah)
    assert not result.residuals


# =============================================================================
# Phase 5F: Reference Resolution Operation (2 tests)
# =============================================================================

def test_hard_gate_09_reference_without_referent_is_candidate():
    """Reference without referent must be CANDIDATE."""
    op = ReferenceResolutionOperation()
    result = op.run(reference="هو", referent="", evidence=())

    # Hard gate: no referent → CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.pronoun.referent_missing" for r in result.residuals)


def test_soft_gate_09_reference_with_referent_is_licensed():
    """Reference with referent and evidence can be LICENSED."""
    op = ReferenceResolutionOperation()
    ev = (Evidence(kind="test.reference", source="antecedent", detail="الطالب"),)
    result = op.run(reference="هو", referent="الطالب", evidence=ev)

    # Soft gate: referent + evidence → LICENSED
    assert result.rank is Rank.LICENSED
    assert not result.residuals


# =============================================================================
# Phase 5G: Speech Force Operation (2 tests)
# =============================================================================

def test_hard_gate_10_speech_force_uncertain_is_candidate():
    """Speech force uncertain or invalid must be CANDIDATE."""
    op = SpeechForceOperation()
    result = op.run(utterance="...", force="", evidence=())

    # Hard gate: no force → CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.speech_force.uncertain" for r in result.residuals)


def test_soft_gate_10_speech_force_determined_is_licensed():
    """Speech force determined with evidence can be LICENSED."""
    op = SpeechForceOperation()
    ev = (Evidence(kind="test.speech", source="khabar_markers", detail="detected"),)
    result = op.run(utterance="الطالب مجتهد", force="khabar", evidence=ev)

    # Soft gate: force + evidence → LICENSED
    assert result.rank is Rank.LICENSED
    assert not result.residuals


# =============================================================================
# Phase 5H: Ifādah Closure Operation (2 tests)
# =============================================================================

def test_hard_gate_11_ifadah_incomplete_is_candidate():
    """Ifādah with missing components must be CANDIDATE."""
    op = IfadahClosureOperation()
    components = {
        "parties": True,
        "binding": True,
        "dalalah": False,  # Missing
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": True,
    }
    result = op.run(components=components, evidence=())

    # Hard gate: incomplete → CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.ifadah.incomplete" for r in result.residuals)


def test_certificate_05_ifadah_complete_with_evidence_is_certified():
    """Ifādah with all components and evidence can be CERTIFIED."""
    op = IfadahClosureOperation()
    components = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": True,
    }
    ev = (Evidence(kind="test.ifadah", source="complete_closure", detail="verified"),)
    result = op.run(components=components, evidence=ev)

    # Certificate: complete + evidence → CERTIFIED
    assert result.rank is Rank.CERTIFIED
    assert not result.residuals


# =============================================================================
# Phase 5I: Boundary Guard Operation (2 tests)
# =============================================================================

def test_hard_gate_12_semantics_to_hukm_is_refuted():
    """SEMANTICS → HUKM jump must be REFUTED."""
    op = BoundaryGuardOperation()
    result = op.run(source=Domain.SEMANTICS, target=Domain.HUKM, value="حكم:تحريم")

    # Hard gate: boundary violation → REFUTED
    assert result.rank is Rank.REFUTED
    assert result.failures
    assert any(f.fatal for f in result.failures)
    assert any(f.kind == "boundary.violation" for f in result.failures)


def test_soft_gate_11_semantics_identity_passes():
    """SEMANTICS → SEMANTICS identity transition passes guard."""
    op = BoundaryGuardOperation()
    result = op.run(source=Domain.SEMANTICS, target=Domain.SEMANTICS, value="معنى")

    # Soft gate: identity → CANDIDATE (passes)
    assert result.rank is Rank.CANDIDATE
    assert not result.failures


# =============================================================================
# Mutation Resistance: Rank Ordering Invariants (2 tests)
# =============================================================================

def test_mutation_01_candidate_below_licensed():
    """CANDIDATE < LICENSED ordering must hold."""
    assert Rank.CANDIDATE < Rank.LICENSED


def test_mutation_02_licensed_below_certified():
    """LICENSED < CERTIFIED ordering must hold."""
    assert Rank.LICENSED < Rank.CERTIFIED
