"""Tests for forbidden semantic jumps (Ifādah boundary enforcement).

These tests verify that the semantic algebra enforces hard boundaries preventing
premature jumps to HUKM (judgment) domain.

Test Categories:
    1. Direct forbidden bridges (SEMANTICS→HUKM)
    2. Indirect attempts via operations
    3. Speech force limitations
    4. Ifādah closure boundaries
"""

from __future__ import annotations

import pytest

from fvafk.algebra import Domain, Rank
from fvafk.algebra.semantics import (
    governed_boundary_guard,
    governed_speech_force,
    governed_ifadah_closure,
)
from fvafk.algebra import Evidence


def _ev(source: str = "test") -> Evidence:
    """Create test evidence."""
    return Evidence(kind="test.evidence", source=source, detail="ok")


# =============================================================================
# Direct Forbidden Bridges
# =============================================================================


def test_semantics_to_hukm_direct_jump_refuted():
    """Direct SEMANTICS→HUKM jump must be REFUTED."""
    result = governed_boundary_guard(Domain.SEMANTICS, Domain.HUKM, "attempt")
    assert result.rank == Rank.REFUTED
    assert len(result.failures) > 0
    assert any(f.fatal for f in result.failures)
    assert any("boundary.violation" in f.kind for f in result.failures)


def test_syntax_to_hukm_would_also_be_invalid():
    """SYNTAX→HUKM jump would also need to go through SEMANTICS."""
    # This test documents that jumping from SYNTAX to HUKM
    # would bypass SEMANTICS layer, which is architecturally wrong
    result = governed_boundary_guard(Domain.SYNTAX, Domain.HUKM, "attempt")
    # BoundaryGuardOperation only checks SEMANTICS→HUKM,
    # so this returns CANDIDATE (not blocked)
    # But the CPB layer would reject SYNTAX→HUKM as unlicensed bridge
    assert result.rank == Rank.CANDIDATE


# =============================================================================
# Speech Force Limitations
# =============================================================================


def test_khabar_speech_force_stays_in_semantics():
    """Khabar (declarative) speech force stays in SEMANTICS domain."""
    result = governed_speech_force("محمد كاتب", force="khabar", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    # Value indicates speech_force, not hukm
    assert "speech_force:khabar" in result.value
    # No failures (not attempting HUKM jump)
    assert len(result.failures) == 0


def test_amr_speech_force_is_not_obligation():
    """Amr (command) speech force is NOT legal obligation."""
    result = governed_speech_force("اكتب", force="amr", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    assert "speech_force:amr" in result.value
    # Amr at Phase 5 is illocutionary force, not deontic modality
    assert len(result.failures) == 0


def test_nahy_speech_force_is_not_prohibition():
    """Nahy (prohibition) speech force is NOT legal prohibition."""
    result = governed_speech_force("لا تكتب", force="nahy", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    assert "speech_force:nahy" in result.value
    # Nahy at Phase 5 is illocutionary force, not deontic modality
    assert len(result.failures) == 0


def test_istifham_speech_force_is_not_interrogative_judgment():
    """Istifhām speech force is NOT interrogative judgment."""
    result = governed_speech_force("هل تكتب", force="istifham", evidence=(_ev(),))
    assert result.rank == Rank.LICENSED
    assert "speech_force:istifham" in result.value
    # Interrogative at Phase 5 is speech act, not judgment
    assert len(result.failures) == 0


# =============================================================================
# Ifādah Closure Boundaries
# =============================================================================


def test_complete_ifadah_stays_in_semantics_domain():
    """Complete ifādah closure stays in SEMANTICS, does not jump to HUKM."""
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
    # Ifādah is semantic completion, not hukm
    assert "ifadah:" in result.value
    # No attempt to jump to HUKM
    assert len(result.failures) == 0


def test_ifadah_with_khabar_force_is_not_hukm():
    """Ifādah with khabar speech force is NOT hukm."""
    # Even a complete ifādah with declarative force doesn't become hukm
    complete_components = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": "ISN",  # Isnadi nisbah
        "structure": True,
        "references": True,
        "speech_force": "khabar",  # Declarative force
    }

    result = governed_ifadah_closure(complete_components, evidence=(_ev(),))
    assert result.rank == Rank.CERTIFIED
    # Still ifādah, not hukm
    assert "ifadah:" in result.value
    assert len(result.failures) == 0


def test_ifadah_with_amr_force_is_not_obligation_hukm():
    """Ifādah with amr speech force is NOT obligation hukm."""
    complete_components = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": "ISN",
        "structure": True,
        "references": True,
        "speech_force": "amr",  # Command force
    }

    result = governed_ifadah_closure(complete_components, evidence=(_ev(),))
    assert result.rank == Rank.CERTIFIED
    # Ifādah with amr force, not obligation hukm
    assert "ifadah:" in result.value
    assert len(result.failures) == 0


# =============================================================================
# Residual Accounting Prevents HUKM Jump
# =============================================================================


def test_ifadah_with_residuals_cannot_reach_hukm():
    """Ifādah with residuals is LICENSED, cannot jump to HUKM."""
    incomplete_components = {
        "parties": True,
        "binding": True,
        "dalalah": False,  # Missing dalālah
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": True,
    }

    result = governed_ifadah_closure(incomplete_components, evidence=(_ev(),))
    assert result.rank == Rank.CANDIDATE
    assert len(result.residuals) > 0
    # Residuals prevent CERTIFIED, therefore prevent HUKM readiness
    assert any("ifadah.incomplete" in r.kind for r in result.residuals)


def test_ifadah_missing_speech_force_cannot_be_certified():
    """Ifādah without speech force cannot be CERTIFIED."""
    components_no_force = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": True,
        "structure": True,
        "references": True,
        "speech_force": False,  # Missing
    }

    result = governed_ifadah_closure(components_no_force, evidence=(_ev(),))
    assert result.rank == Rank.CANDIDATE
    assert len(result.residuals) > 0


def test_ifadah_missing_references_cannot_be_certified():
    """Ifādah with unresolved references cannot be CERTIFIED."""
    components_no_refs = {
        "parties": True,
        "binding": True,
        "dalalah": True,
        "nisbah": True,
        "structure": True,
        "references": False,  # Missing
        "speech_force": True,
    }

    result = governed_ifadah_closure(components_no_refs, evidence=(_ev(),))
    assert result.rank == Rank.CANDIDATE
    assert len(result.residuals) > 0


# =============================================================================
# Boundary Guard Edge Cases
# =============================================================================


def test_boundary_guard_allows_valid_transitions():
    """Boundary guard allows valid transitions (not SEMANTICS→HUKM)."""
    # SYNTAX → SEMANTICS is valid
    result_syn_sem = governed_boundary_guard(Domain.SYNTAX, Domain.SEMANTICS, "ok")
    assert result_syn_sem.rank == Rank.CANDIDATE
    assert len(result_syn_sem.failures) == 0

    # SEMANTICS → SEMANTICS is valid (identity)
    result_sem_sem = governed_boundary_guard(Domain.SEMANTICS, Domain.SEMANTICS, "ok")
    assert result_sem_sem.rank == Rank.CANDIDATE
    assert len(result_sem_sem.failures) == 0


def test_boundary_guard_rejects_only_semantics_to_hukm():
    """Boundary guard specifically rejects SEMANTICS→HUKM."""
    result = governed_boundary_guard(Domain.SEMANTICS, Domain.HUKM, "blocked")
    assert result.rank == Rank.REFUTED
    assert any(f.fatal for f in result.failures)
    assert "SEMANTICS→HUKM" in str(result.failures[0].description)
