"""Phase-1 surface-coverage tests for :class:`ArabicAlgebraDecisionTree`.

These tests are driven by ``tests/fixtures/algebra/wazn_surface_cases.json``.
They prove the central Phase-1 rule:

    الوزن السطحي يرخّص احتمالاً صرفياً،
    ولا يمنح دلالة نهائية،
    ولا يرفع النتيجة إلى CERTIFIED،
    ولا يقفز إلى SEMANTICS أو HUKM.

The Phase-0 file ``tests/test_algebra_decision_tree.py`` is left
untouched and continues to exercise the original ``كاتب`` walkthrough.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

from fvafk.algebra import (
    ArabicAlgebraDecisionTree,
    CPB,
    Domain,
    Rank,
)


_FIXTURE_PATH = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "algebra"
    / "wazn_surface_cases.json"
)


def _load_cases() -> List[Dict[str, Any]]:
    with _FIXTURE_PATH.open(encoding="utf-8") as f:
        return json.load(f)


_CASES = _load_cases()


def _case_id(case: Dict[str, Any]) -> str:
    return f"{case['expected_pattern']}::{case['input']}"


# ---------------------------------------------------------------------------
# Sanity checks on the fixture itself
# ---------------------------------------------------------------------------


def test_fixture_loads_and_is_non_empty():
    assert len(_CASES) >= 25, (
        f"fixture should cover ≥25 surface cases, found {len(_CASES)}"
    )


def test_fixture_covers_all_nine_families():
    """All nine wazn families from the Phase-1 plan must be present."""
    expected_families = {
        "فاعل", "مفعول", "فعّال", "مفعال", "مِفعل",
        "مَفعل", "فعلة", "فعول", "فعيل",
    }
    actual_families = {c["expected_pattern"] for c in _CASES}
    assert actual_families == expected_families, (
        f"family mismatch — missing: {expected_families - actual_families}, "
        f"unexpected: {actual_families - expected_families}"
    )


def test_fixture_never_expects_certified():
    """No fixture case may expect CERTIFIED — that's the whole point."""
    for case in _CASES:
        assert case["expected_rank"] != "CERTIFIED", (
            f"case {_case_id(case)} illegally expects CERTIFIED"
        )
        assert "CERTIFIED" in case["forbidden_ranks"], (
            f"case {_case_id(case)} must list CERTIFIED in forbidden_ranks"
        )


# ---------------------------------------------------------------------------
# Per-case parametrised behaviour
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("case", _CASES, ids=[_case_id(c) for c in _CASES])
def test_fixture_cases_are_licensed_not_certified(case):
    """Every surface match returns LICENSED with certificate_allowed=False."""
    result = ArabicAlgebraDecisionTree().analyze(case["input"])
    assert result.rank.name == case["expected_rank"], (
        f"{case['input']}: expected rank {case['expected_rank']}, "
        f"got {result.rank.name}"
    )
    assert result.rank is Rank.LICENSED
    assert result.certificate_allowed is False
    for forbidden in case["forbidden_ranks"]:
        assert result.rank.name != forbidden


@pytest.mark.parametrize("case", _CASES, ids=[_case_id(c) for c in _CASES])
def test_fixture_pattern_and_root_match(case):
    """Pattern and root letters must match exactly the fixture spec."""
    result = ArabicAlgebraDecisionTree().analyze(case["input"])
    assert result.value.pattern == case["expected_pattern"]
    assert result.value.root == tuple(case["expected_root_letters"])


@pytest.mark.parametrize("case", _CASES, ids=[_case_id(c) for c in _CASES])
def test_fixture_required_residuals_present(case):
    """Every required_residual kind must appear in the result."""
    result = ArabicAlgebraDecisionTree().analyze(case["input"])
    actual = {r.kind for r in result.residuals}
    for required in case["required_residuals"]:
        assert required in actual, (
            f"{case['input']}: missing required residual '{required}', "
            f"got {sorted(actual)}"
        )


@pytest.mark.parametrize("case", _CASES, ids=[_case_id(c) for c in _CASES])
def test_evidence_cites_input(case):
    """Every emitted evidence must cite the input surface (CPB invariant)."""
    result = ArabicAlgebraDecisionTree().analyze(case["input"])
    assert result.evidence, f"{case['input']} produced no evidence"
    for ev in result.evidence:
        assert (
            case["input"] in ev.source or case["input"] in ev.detail
        ), (
            f"{case['input']}: evidence kind '{ev.kind}' does not cite "
            f"the surface form"
        )


# ---------------------------------------------------------------------------
# No-jump invariants — the heart of Phase 1
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("case", _CASES, ids=[_case_id(c) for c in _CASES])
def test_no_morph_surface_to_semantics_evidence(case):
    """Surface analyzer must never emit semantic.* or hukm.* evidence."""
    result = ArabicAlgebraDecisionTree().analyze(case["input"])
    for ev in result.evidence:
        assert not ev.kind.startswith("semantic."), (
            f"{case['input']}: forbidden evidence kind '{ev.kind}' — "
            f"MORPH_SURFACE must not jump to SEMANTICS"
        )
        assert not ev.kind.startswith("hukm."), (
            f"{case['input']}: forbidden evidence kind '{ev.kind}' — "
            f"MORPH_SURFACE must not jump to HUKM"
        )


@pytest.mark.parametrize("case", _CASES, ids=[_case_id(c) for c in _CASES])
def test_no_morph_surface_to_semantics_residual(case):
    """Surface residuals must never claim a semantic / hukm jurisdiction."""
    result = ArabicAlgebraDecisionTree().analyze(case["input"])
    for r in result.residuals:
        assert not r.kind.startswith("semantic.")
        assert not r.kind.startswith("hukm.")


def test_morph_surface_to_morph_deep_bridge_is_forbidden():
    """Phase-0 regression: MORPH_SURFACE → MORPH_DEEP must stay illegal.

    Restated here so a Phase-1 contributor cannot quietly relax the
    bridge matrix in ``arabic_layers.py`` without this test catching it.
    """
    with pytest.raises(ValueError, match="forbidden bridge"):
        CPB(
            name="phase1.surface→deep",
            source=Domain.MORPH_SURFACE,
            target=Domain.MORPH_DEEP,
        )


def test_morph_surface_to_semantics_bridge_is_forbidden():
    """Phase-0 regression: MORPH_SURFACE → SEMANTICS must stay illegal."""
    with pytest.raises(ValueError, match="forbidden bridge"):
        CPB(
            name="phase1.surface→semantics",
            source=Domain.MORPH_SURFACE,
            target=Domain.SEMANTICS,
        )


def test_morph_deep_to_hukm_bridge_is_forbidden():
    """Phase-0 regression: MORPH_DEEP → HUKM must stay illegal."""
    with pytest.raises(ValueError, match="forbidden bridge"):
        CPB(
            name="phase1.deep→hukm",
            source=Domain.MORPH_DEEP,
            target=Domain.HUKM,
        )


# ---------------------------------------------------------------------------
# Negative / proper-name cases (option (a) from the plan)
# ---------------------------------------------------------------------------


def test_proper_name_token_still_licensed_not_refused():
    """Per plan choice (a): a proper-noun-leaning surface still matches.

    The surface match is *not* refused; instead the result stays
    LICENSED and carries an explicit ``proper_name.possible`` residual
    that prevents promotion.
    """
    result = ArabicAlgebraDecisionTree().analyze("ناصر")
    assert result.rank is Rank.LICENSED
    assert result.value.pattern == "فاعل"
    kinds = {r.kind for r in result.residuals}
    assert "proper_name.possible" in kinds


def test_proper_name_token_never_certified():
    """A proper-noun-leaning surface must never reach CERTIFIED."""
    for token in ("ناصر", "حامد", "محمود", "كريم", "حكيم"):
        result = ArabicAlgebraDecisionTree().analyze(token)
        assert result.rank is not Rank.CERTIFIED, (
            f"{token}: proper-noun-leaning surface illegally promoted"
        )
        assert result.certificate_allowed is False


def test_transfer_possible_residual_for_intensive_shapes():
    """فعّال / فعول families must always carry transfer.possible."""
    for token in ("كذّاب", "نجّار", "خبّاز", "صبور", "شكور", "غفور"):
        result = ArabicAlgebraDecisionTree().analyze(token)
        kinds = {r.kind for r in result.residuals}
        assert "transfer.possible" in kinds, (
            f"{token}: missing transfer.possible residual"
        )


def test_pattern_collision_residual_for_mafal_family():
    """مَفعل family must always carry pattern.collision."""
    for token in ("مَكتب", "مَلعب", "مَجلس"):
        result = ArabicAlgebraDecisionTree().analyze(token)
        kinds = {r.kind for r in result.residuals}
        assert "pattern.collision" in kinds, (
            f"{token}: missing pattern.collision residual"
        )


# ---------------------------------------------------------------------------
# Phase-0 regressions — the original walkthrough must still hold
# ---------------------------------------------------------------------------


def test_phase0_kateb_invariant_unchanged():
    """The Phase-0 ``كاتب`` walkthrough must produce identical output."""
    result = ArabicAlgebraDecisionTree().analyze("كاتب")
    assert result.rank is Rank.LICENSED
    assert result.certificate_allowed is False
    assert result.value.pattern == "فاعل"
    assert result.value.root == ("ك", "ت", "ب")
    kinds = {r.kind for r in result.residuals}
    assert "context.absent" in kinds
    assert "lexical.ambiguity" in kinds


def test_unknown_token_still_unresolved():
    """Tokens outside the Phase-1 catalog stay UNRESOLVED (Phase-0 contract)."""
    result = ArabicAlgebraDecisionTree().analyze("xyz_not_arabic")
    assert result.rank is Rank.UNRESOLVED
    assert result.evidence == ()
    assert any(r.kind == "pattern.no_match" for r in result.residuals)


def test_empty_input_is_unresolved_not_refuted():
    result = ArabicAlgebraDecisionTree().analyze("   ")
    assert result.rank is Rank.UNRESOLVED
    assert result.value.pattern is None


# ---------------------------------------------------------------------------
# Replay must remain serialisable for every covered case
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("case", _CASES, ids=[_case_id(c) for c in _CASES])
def test_replay_is_well_formed(case):
    """Phase-0 replay contract holds for every Phase-1 case."""
    result = ArabicAlgebraDecisionTree().analyze(case["input"])
    replay = result.replay()
    assert replay["rank"] == "LICENSED"
    assert len(replay["evidence"]) >= 1
    assert len(replay["residuals"]) >= 2
    # Trace metadata must point at the surface analyzer.
    assert "ArabicAlgebraDecisionTree" in replay["trace"]["operation"]
