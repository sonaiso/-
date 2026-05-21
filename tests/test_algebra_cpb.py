"""Tests for ``fvafk.algebra`` CPB primitives and the Result invariants."""

from __future__ import annotations

import pytest

from fvafk.algebra import (
    CPB,
    Carrier,
    Domain,
    Evidence,
    Failure,
    Rank,
    Residual,
    Result,
    Trace,
    apply_policy,
    default_policy,
    is_bridge_allowed,
    validate_cpb,
)


def _ev(source: str = "كاتب") -> Evidence:
    return Evidence(kind="test.evidence", source=source, detail="ok")


def test_result_rejects_ranked_claim_without_evidence():
    """la-mukhraj-arin: ranks above UNRESOLVED require evidence."""
    with pytest.raises(ValueError):
        Result(value="x", rank=Rank.LICENSED)


def test_certified_result_forbids_residuals():
    """CERTIFIED requires an empty residual set."""
    with pytest.raises(ValueError):
        Result(
            value="x",
            rank=Rank.CERTIFIED,
            evidence=(_ev(),),
            residuals=(Residual(kind="ctx", description="missing context"),),
        )


def test_fatal_failure_forces_refuted():
    """A fatal Failure must be paired with REFUTED rank."""
    with pytest.raises(ValueError):
        Result(
            value="x",
            rank=Rank.LICENSED,
            evidence=(_ev(),),
            failures=(Failure(kind="x", description="bad", fatal=True),),
        )


def test_certificate_allowed_requires_clean_state():
    licensed = Result(
        value="x",
        rank=Rank.LICENSED,
        evidence=(_ev(),),
        residuals=(Residual(kind="ctx", description="missing"),),
    )
    assert licensed.certificate_allowed is False

    clean = Result(value="x", rank=Rank.CERTIFIED, evidence=(_ev(),))
    assert clean.certificate_allowed is True


def test_cpb_rejects_forbidden_bridge_at_construction():
    """CPB construction must reject prohibited cross-layer promotions."""
    with pytest.raises(ValueError):
        CPB(name="bad", source=Domain.GRAPHEME, target=Domain.MORPH_DEEP)


def test_is_bridge_allowed_topology():
    assert is_bridge_allowed(Domain.GRAPHEME, Domain.PHONEME) is True
    assert is_bridge_allowed(Domain.SYLLABLE, Domain.ROOT) is False
    assert is_bridge_allowed(Domain.MORPH_SURFACE, Domain.MORPH_SURFACE) is True


def test_validate_cpb_detects_uncited_output():
    """A CPB result with no evidence citing the carrier is REFUTED."""
    cpb = CPB(
        name="wazn→root",
        source=Domain.MORPH_SURFACE,
        target=Domain.ROOT,
    )
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="كاتب", label="كاتب")
    bogus = Result(
        value="root",
        rank=Rank.LICENSED,
        evidence=(Evidence(kind="x", source="unrelated", detail="no link"),),
        trace=Trace(operation="t"),
    )

    validated = validate_cpb(cpb, carrier, bogus)
    assert validated.rank is Rank.REFUTED
    assert any(f.kind == "cpb.uncited_output" for f in validated.failures)


def test_validate_cpb_detects_domain_mismatch():
    cpb = CPB(name="b", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
    carrier = Carrier(domain=Domain.PHONEME, value="X", label="x")
    raw = Result(
        value="r",
        rank=Rank.LICENSED,
        evidence=(_ev("x"),),
        trace=Trace(operation="t"),
    )
    validated = validate_cpb(cpb, carrier, raw)
    assert validated.rank is Rank.REFUTED
    assert any(f.kind == "cpb.domain_mismatch" for f in validated.failures)


def test_default_policy_promotes_when_clean():
    rank = default_policy(
        evidence=(_ev(),),
        residuals=(),
        failures=(),
    )
    assert rank is Rank.CERTIFIED


def test_default_policy_caps_at_licensed_with_residuals():
    rank = default_policy(
        evidence=(_ev(),),
        residuals=(Residual(kind="ctx", description="missing"),),
        failures=(),
    )
    assert rank is Rank.LICENSED


def test_apply_policy_demotes_then_repromotes():
    """apply_policy should be idempotent on a stable state."""
    r = Result(
        value="x",
        rank=Rank.LICENSED,
        evidence=(_ev(),),
        residuals=(Residual(kind="ctx", description="missing"),),
    )
    first = apply_policy(r, default_policy)
    second = apply_policy(first, default_policy)
    assert first.rank is Rank.LICENSED
    assert second.rank is Rank.LICENSED


def test_result_replay_is_json_friendly():
    r = Result(
        value="kateb",
        rank=Rank.LICENSED,
        evidence=(_ev(),),
        residuals=(Residual(kind="ctx", description="missing"),),
    )
    replay = r.replay()
    assert replay["rank"] == "LICENSED"
    assert replay["evidence"][0]["kind"] == "test.evidence"
    assert replay["residuals"][0]["kind"] == "ctx"
    assert "trace" in replay and "operation" in replay["trace"]
