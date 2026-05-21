"""
Ifādah Forbidden Jumps Tests

Tests for semantic layer constraints preventing premature meaning completion.

These tests verify hard laws about what does NOT become ifādah:
    1. Iḍāfah alone ≠ ifādah
    2. Conditional without jawāb ≠ ifādah
    3. Pronoun without referent ≠ CERTIFIED ifādah
    4. Mutābaqah alone ≠ ifādah
    5. Taḍammun alone ≠ ifādah
    6. Iltizām without gate ≠ ifādah
    7. Taqyīd alone ≠ ifādah
    8. Speech force alone ≠ HUKM
    9. SEMANTICS ≠ HUKM (boundary violation)
"""

from __future__ import annotations

from fvafk.algebra import (
    Domain,
    Evidence,
    Rank,
)
from fvafk.algebra.semantics import (
    governed_nisbah_semantic,
    governed_reference_resolution,
    governed_mutabaqah,
    governed_tadammun,
    governed_iltizam,
    governed_speech_force,
    governed_boundary_guard,
)


# =============================================================================
# Test 1: Iḍāfah alone ≠ ifādah
# =============================================================================

def test_idafah_cannot_become_ifadah():
    """Iḍāfah relation alone does not produce ifādah."""
    result = governed_nisbah_semantic("IDAFA", "كتاب:الطالب", evidence=())

    # Without evidence → CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.idafah.not_ifadah" for r in result.residuals)


def test_idafah_with_evidence_still_has_residual():
    """Even with evidence, iḍāfah alone carries residual (not complete ifādah)."""
    ev = (Evidence(kind="test", source="idafa_attestation", detail="attested"),)
    result = governed_nisbah_semantic("IDAFA", "كتاب:الطالب", evidence=ev)

    # With evidence → LICENSED but still has residual
    assert result.rank is Rank.LICENSED
    assert result.residuals
    assert any(r.kind == "semantics.idafah.not_ifadah" for r in result.residuals)


# =============================================================================
# Test 2: Conditional without jawāb ≠ ifādah
# =============================================================================

def test_conditional_without_jawab_is_candidate():
    """Conditional without jawāb does not become ifādah."""
    result = governed_nisbah_semantic("SHART", "إن:تدرس", evidence=())

    # Always CANDIDATE without jawāb
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.conditional.jawab_missing" for r in result.residuals)


def test_conditional_with_evidence_but_no_jawab_still_candidate():
    """Even with evidence, conditional without jawāb remains CANDIDATE."""
    ev = (Evidence(kind="test", source="shart_particle", detail="detected"),)
    result = governed_nisbah_semantic("SHART", "إن:تدرس", evidence=ev)

    # Evidence cannot overcome missing jawāb
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.conditional.jawab_missing" for r in result.residuals)


# =============================================================================
# Test 3: Pronoun without referent ≠ CERTIFIED ifādah
# =============================================================================

def test_pronoun_without_referent_is_candidate():
    """Pronoun without referent cannot become LICENSED."""
    result = governed_reference_resolution("هو", referent="", evidence=())

    # Without referent → CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.pronoun.referent_missing" for r in result.residuals)


def test_pronoun_with_referent_can_be_licensed():
    """Pronoun with referent and evidence can reach LICENSED."""
    ev = (Evidence(kind="test", source="reference_resolved", detail="الطالب"),)
    result = governed_reference_resolution("هو", referent="الطالب", evidence=ev)

    # With referent + evidence → LICENSED
    assert result.rank is Rank.LICENSED
    assert not result.residuals


# =============================================================================
# Test 4: Mutābaqah alone ≠ ifādah
# =============================================================================

def test_mutabaqah_alone_has_residual():
    """Mutābaqah (direct correspondence) alone does not produce ifādah."""
    result = governed_mutabaqah("دار→بيت", evidence=())

    # Always has mutabaqah.insufficient residual
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.mutabaqah.insufficient" for r in result.residuals)


def test_mutabaqah_with_evidence_still_insufficient():
    """Even with evidence, mutābaqah alone is insufficient for ifādah."""
    ev = (Evidence(kind="test", source="mutabaqah_direct", detail="verified"),)
    result = governed_mutabaqah("دار→بيت", evidence=ev)

    # With evidence → LICENSED but still has residual (pre-ifādah)
    assert result.rank is Rank.LICENSED
    assert result.residuals
    assert any(r.kind == "semantics.mutabaqah.insufficient" for r in result.residuals)


# =============================================================================
# Test 5: Taḍammun alone ≠ ifādah
# =============================================================================

def test_tadammun_alone_has_residual():
    """Taḍammun (partial inclusion) alone does not produce ifādah."""
    result = governed_tadammun("سقف→بيت", "جزء", evidence=())

    # Always has tadammun.insufficient residual
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.tadammun.insufficient" for r in result.residuals)


def test_tadammun_with_evidence_still_insufficient():
    """Even with evidence, taḍammun alone is insufficient for ifādah."""
    ev = (Evidence(kind="test", source="tadammun_partial", detail="verified"),)
    result = governed_tadammun("سقف→بيت", "جزء", evidence=ev)

    # With evidence → LICENSED but still has residual (pre-ifādah)
    assert result.rank is Rank.LICENSED
    assert result.residuals
    assert any(r.kind == "semantics.tadammun.insufficient" for r in result.residuals)


# =============================================================================
# Test 6: Iltizām without gate ≠ licensed
# =============================================================================

def test_iltizam_without_gate_is_candidate():
    """Iltizām without explicit gate is CANDIDATE."""
    result = governed_iltizam("طلوع:الشمس", "نهار", gate_type="", evidence=())

    # Without gate → CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.iltizam.gate_missing" for r in result.residuals)


def test_iltizam_with_evidence_but_no_gate_still_candidate():
    """Even with evidence, iltizām without gate_type is CANDIDATE."""
    ev = (Evidence(kind="test", source="iltizam_attempted", detail="observed"),)
    result = governed_iltizam("طلوع:الشمس", "نهار", gate_type="", evidence=ev)

    # Evidence without gate_type → still CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.iltizam.gate_missing" for r in result.residuals)


def test_iltizam_with_gate_can_be_licensed():
    """Iltizām with explicit gate and evidence can reach LICENSED."""
    ev = (Evidence(kind="test", source="iltizam_logical", detail="causality"),)
    result = governed_iltizam("طلوع:الشمس", "نهار", gate_type="logical", evidence=ev)

    # With gate + evidence → LICENSED
    assert result.rank is Rank.LICENSED
    assert not result.residuals


# =============================================================================
# Test 7: Taqyīd alone ≠ ifādah
# =============================================================================

def test_taqyid_without_predication_has_residual():
    """Taqyīd alone without predication does not become ifādah."""
    result = governed_nisbah_semantic("TAQYID", "في:البيت", evidence=())

    # Without evidence → CANDIDATE
    assert result.rank is Rank.CANDIDATE
    assert result.residuals
    assert any(r.kind == "semantics.taqyid.incomplete" for r in result.residuals)


def test_taqyid_with_evidence_still_incomplete():
    """Even with evidence, taqyīd alone is incomplete without predication."""
    ev = (Evidence(kind="test", source="taqyid_modifier", detail="detected"),)
    result = governed_nisbah_semantic("TAQYID", "في:البيت", evidence=ev)

    # With evidence → LICENSED but still incomplete
    assert result.rank is Rank.LICENSED
    assert result.residuals
    assert any(r.kind == "semantics.taqyid.incomplete" for r in result.residuals)


# =============================================================================
# Test 8: Speech force alone ≠ HUKM
# =============================================================================

def test_speech_force_khabar_is_not_hukm():
    """Khabar (declarative) does NOT become HUKM at Phase 5."""
    ev = (Evidence(kind="test", source="khabar_markers", detail="detected"),)
    result = governed_speech_force("الطالب مجتهد", force="khabar", evidence=ev)

    # Speech force determined → LICENSED but NOT HUKM
    assert result.rank is Rank.LICENSED
    assert not result.residuals
    # Value does not contain "hukm"
    assert "hukm" not in result.value.lower()
    assert "speech_force:khabar" in result.value


def test_speech_force_amr_is_not_hukm():
    """Amr (imperative) does NOT become HUKM at Phase 5."""
    ev = (Evidence(kind="test", source="amr_markers", detail="detected"),)
    result = governed_speech_force("ادرس", force="amr", evidence=ev)

    # Speech force determined → LICENSED but NOT HUKM
    assert result.rank is Rank.LICENSED
    assert not result.residuals
    # Value does not contain "hukm"
    assert "hukm" not in result.value.lower()
    assert "speech_force:amr" in result.value


# =============================================================================
# Test 9: SEMANTICS → HUKM boundary violation
# =============================================================================

def test_semantics_to_hukm_jump_is_refuted():
    """Attempted SEMANTICS → HUKM jump is REFUTED with fatal failure."""
    result = governed_boundary_guard(Domain.SEMANTICS, Domain.HUKM, "حكم:تحريم")

    # Boundary violation → REFUTED
    assert result.rank is Rank.REFUTED
    assert result.failures
    assert any(f.fatal for f in result.failures)
    assert any(f.kind == "boundary.violation" for f in result.failures)


def test_semantics_identity_is_candidate():
    """SEMANTICS → SEMANTICS identity transition is allowed (CANDIDATE)."""
    result = governed_boundary_guard(Domain.SEMANTICS, Domain.SEMANTICS, "معنى")

    # Identity transition → CANDIDATE (passes guard)
    assert result.rank is Rank.CANDIDATE
    assert not result.failures
