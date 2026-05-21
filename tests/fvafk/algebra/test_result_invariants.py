"""Invariant tests pinning the ``Result`` constitution: لا مخرج عارٍ.

Every Result = value + rank + evidence + residuals + failures + replay.

These tests defend the four core invariants encoded in
``src/fvafk/algebra/core.py`` :

1. Ranks ``LICENSED`` and ``CERTIFIED`` require at least one Evidence.
2. ``CERTIFIED`` forbids residuals.
3. A fatal Failure forces rank ``REFUTED``.
4. The canonical Rank set is exactly
   ``{UNRESOLVED, CANDIDATE, LICENSED, CERTIFIED, REFUTED}`` —
   legacy names like ``CERTIFICATE`` or ``BLOCKED`` are forbidden.
"""

from __future__ import annotations

import json

import pytest

from fvafk.algebra import (
    Evidence,
    Failure,
    Rank,
    Residual,
    Result,
    Trace,
    apply_policy,
    default_policy,
)


def _ev(source: str = "كاتب") -> Evidence:
    return Evidence(kind="test.evidence", source=source, detail="ok")


# ---------------------------------------------------------------------------
# Canonical Rank surface — locks names + numeric values.
# ---------------------------------------------------------------------------


CANONICAL_RANK_NAMES = {
    "UNRESOLVED",
    "CANDIDATE",
    "LICENSED",
    "CERTIFIED",
    "REFUTED",
}


def test_rank_names_are_exactly_the_canonical_five():
    """Legacy names (CERTIFICATE, BLOCKED, ...) must not creep back in."""
    assert {r.name for r in Rank} == CANONICAL_RANK_NAMES


def test_rank_numeric_values_are_pinned():
    """Re-ordering ranks would silently break promotion logic; pin them."""
    assert Rank.UNRESOLVED.value == 0
    assert Rank.CANDIDATE.value == 1
    assert Rank.LICENSED.value == 2
    assert Rank.CERTIFIED.value == 3
    assert Rank.REFUTED.value == -1


def test_rank_ordering_certified_above_licensed_above_candidate():
    assert Rank.UNRESOLVED < Rank.CANDIDATE
    assert Rank.CANDIDATE < Rank.LICENSED
    assert Rank.LICENSED < Rank.CERTIFIED
    # REFUTED is below UNRESOLVED (negative value).
    assert Rank.REFUTED < Rank.UNRESOLVED


# ---------------------------------------------------------------------------
# Invariant 1: LICENSED / CERTIFIED require evidence.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("rank", [Rank.LICENSED, Rank.CERTIFIED])
def test_ranked_claim_without_evidence_is_rejected(rank: Rank):
    """la-mukhraj-arin: cannot claim LICENSED/CERTIFIED with no evidence."""
    with pytest.raises(ValueError):
        Result(value="x", rank=rank)


@pytest.mark.parametrize("rank", [Rank.UNRESOLVED, Rank.CANDIDATE])
def test_unranked_claim_without_evidence_is_allowed(rank: Rank):
    """UNRESOLVED and CANDIDATE permit empty evidence."""
    r = Result(value="x", rank=rank)
    assert r.rank is rank
    assert r.evidence == ()


# ---------------------------------------------------------------------------
# Invariant 2: CERTIFIED forbids residuals.
# ---------------------------------------------------------------------------


def test_certified_with_residuals_is_rejected():
    with pytest.raises(ValueError):
        Result(
            value="x",
            rank=Rank.CERTIFIED,
            evidence=(_ev(),),
            residuals=(Residual(kind="ctx", description="missing"),),
        )


def test_certified_clean_state_is_accepted():
    r = Result(value="x", rank=Rank.CERTIFIED, evidence=(_ev(),))
    assert r.rank is Rank.CERTIFIED
    assert r.residuals == ()
    assert r.certificate_allowed is True


def test_licensed_with_residuals_is_accepted():
    r = Result(
        value="x",
        rank=Rank.LICENSED,
        evidence=(_ev(),),
        residuals=(Residual(kind="ctx", description="missing"),),
    )
    assert r.rank is Rank.LICENSED
    assert r.certificate_allowed is False


# ---------------------------------------------------------------------------
# Invariant 3: fatal Failure forces REFUTED.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "rank",
    [Rank.UNRESOLVED, Rank.CANDIDATE, Rank.LICENSED, Rank.CERTIFIED],
)
def test_fatal_failure_paired_with_non_refuted_rank_is_rejected(rank: Rank):
    """A fatal Failure must coincide with rank=REFUTED."""
    kwargs: dict = {"value": "x", "rank": rank}
    if rank in (Rank.LICENSED, Rank.CERTIFIED):
        kwargs["evidence"] = (_ev(),)
    kwargs["failures"] = (Failure(kind="x", description="bad", fatal=True),)
    with pytest.raises(ValueError):
        Result(**kwargs)


def test_fatal_failure_with_refuted_is_accepted():
    r = Result(
        value="x",
        rank=Rank.REFUTED,
        failures=(Failure(kind="x", description="bad", fatal=True),),
    )
    assert r.rank is Rank.REFUTED
    assert any(f.fatal for f in r.failures)


def test_with_failure_auto_demotes_to_refuted_on_fatal():
    """``Result.with_failure`` re-establishes the invariant when adding fatals."""
    r = Result(value="x", rank=Rank.LICENSED, evidence=(_ev(),))
    refuted = r.with_failure(Failure(kind="x", description="bad", fatal=True))
    assert refuted.rank is Rank.REFUTED
    assert any(f.fatal for f in refuted.failures)


def test_with_failure_keeps_rank_when_failure_is_non_fatal():
    r = Result(value="x", rank=Rank.LICENSED, evidence=(_ev(),))
    same = r.with_failure(Failure(kind="x", description="warn", fatal=False))
    assert same.rank is Rank.LICENSED
    assert same.failures and not same.failures[0].fatal


# ---------------------------------------------------------------------------
# Replay record is JSON-serialisable (forms part of "no bare output").
# ---------------------------------------------------------------------------


def test_replay_record_is_json_serialisable():
    r = Result(
        value="kateb",
        rank=Rank.LICENSED,
        evidence=(_ev(),),
        residuals=(Residual(kind="ctx", description="missing"),),
        trace=Trace(operation="t"),
    )
    payload = json.dumps(r.replay())  # must not raise
    assert "LICENSED" in payload
    assert "test.evidence" in payload


# ---------------------------------------------------------------------------
# Default policy: full truth table over (evidence, residuals, fatal failure).
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "evidence,residuals,fatal,expected",
    [
        # No evidence, nothing else → UNRESOLVED.
        ((), (), False, Rank.UNRESOLVED),
        # No evidence, but residual exists → CANDIDATE (claim made, unsupported).
        ((), (Residual(kind="ctx", description="m"),), False, Rank.CANDIDATE),
        # Evidence + no residual → CERTIFIED.
        ((Evidence(kind="k", source="s"),), (), False, Rank.CERTIFIED),
        # Evidence + residual → LICENSED.
        (
            (Evidence(kind="k", source="s"),),
            (Residual(kind="ctx", description="m"),),
            False,
            Rank.LICENSED,
        ),
        # Fatal failure trumps everything → REFUTED.
        ((Evidence(kind="k", source="s"),), (), True, Rank.REFUTED),
        ((), (), True, Rank.REFUTED),
    ],
)
def test_default_policy_truth_table(evidence, residuals, fatal, expected):
    failures = (
        (Failure(kind="x", description="bad", fatal=True),) if fatal else ()
    )
    assert default_policy(evidence, residuals, failures) is expected


def test_apply_policy_is_idempotent():
    r = Result(
        value="x",
        rank=Rank.LICENSED,
        evidence=(_ev(),),
        residuals=(Residual(kind="ctx", description="m"),),
    )
    once = apply_policy(r, default_policy)
    twice = apply_policy(once, default_policy)
    assert once.rank is twice.rank is Rank.LICENSED


# ---------------------------------------------------------------------------
# Evidence / Residual constructor invariants (small helpers tied to "no bare output").
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "kind,source,weight",
    [
        ("", "src", 1.0),    # empty kind
        ("k", "", 1.0),      # empty source
        ("k", "src", 0.0),   # non-positive weight
        ("k", "src", -1.0),
    ],
)
def test_evidence_constructor_rejects_invalid_atoms(kind, source, weight):
    with pytest.raises(ValueError):
        Evidence(kind=kind, source=source, weight=weight)


def test_residual_constructor_rejects_empty_kind():
    with pytest.raises(ValueError):
        Residual(kind="", description="x")
