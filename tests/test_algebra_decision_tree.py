"""Tests for :class:`fvafk.algebra.ArabicAlgebraDecisionTree`."""

from __future__ import annotations

from fvafk.algebra import ArabicAlgebraDecisionTree, Rank


def test_analyze_kateb_is_licensed_not_certified():
    """كاتب → wazn فاعل candidate is LICENSED but not CERTIFIED."""
    result = ArabicAlgebraDecisionTree().analyze("كاتب")
    assert result.rank is Rank.LICENSED
    assert result.certificate_allowed is False
    assert result.value.pattern == "فاعل"
    assert result.value.root == ("ك", "ت", "ب")


def test_analyze_kateb_records_context_and_lexical_residuals():
    """Residuals must explain *why* certification is blocked."""
    result = ArabicAlgebraDecisionTree().analyze("كاتب")
    kinds = {r.kind for r in result.residuals}
    assert "context.absent" in kinds
    assert "lexical.ambiguity" in kinds


def test_analyze_cites_input_in_every_evidence():
    """CPB correspondence: every evidence atom cites the surface form."""
    result = ArabicAlgebraDecisionTree().analyze("كاتب")
    assert result.evidence  # not empty
    for ev in result.evidence:
        assert "كاتب" in ev.source or "كاتب" in ev.detail


def test_analyze_unknown_token_is_unresolved():
    """Tokens outside the Phase-0 table cannot be ranked above UNRESOLVED."""
    result = ArabicAlgebraDecisionTree().analyze("xyz_not_arabic")
    assert result.rank is Rank.UNRESOLVED
    assert result.evidence == ()
    assert any(r.kind == "pattern.no_match" for r in result.residuals)


def test_analyze_empty_input_is_unresolved_not_refuted():
    """Empty input is unresolved (no claim), not refuted."""
    result = ArabicAlgebraDecisionTree().analyze("   ")
    assert result.rank is Rank.UNRESOLVED
    assert result.value.pattern is None


def test_analyze_replay_is_serializable():
    """The replay record of a real analysis is a plain dict."""
    result = ArabicAlgebraDecisionTree().analyze("كاتب")
    replay = result.replay()
    assert replay["rank"] == "LICENSED"
    assert len(replay["evidence"]) >= 1
    assert len(replay["residuals"]) >= 2
