"""CPB contract tests: domain match, allowed bridge, cited output.

Covers ``validate_cpb`` exhaustively:

- Carrier domain must match CPB.source → otherwise ``cpb.domain_mismatch``.
- Bridge must be allowed (forbidden bridges already blocked at construction).
- Ranked results (>= LICENSED) must cite the input carrier in evidence —
  otherwise ``cpb.uncited_output``. Unranked results are exempt.
"""

from __future__ import annotations

import pytest

from fvafk.algebra import (
    CPB,
    Carrier,
    Domain,
    Evidence,
    Failure,
    Rank,
    Result,
    Trace,
    validate_cpb,
)


def _trace() -> Trace:
    return Trace(operation="t")


# ---------------------------------------------------------------------------
# Domain mismatch.
# ---------------------------------------------------------------------------


def test_validate_cpb_flags_domain_mismatch_as_fatal_refuted():
    cpb = CPB(name="b", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
    carrier = Carrier(domain=Domain.PHONEME, value="X", label="x")
    result = Result(
        value="r",
        rank=Rank.LICENSED,
        evidence=(Evidence(kind="k", source="x"),),
        trace=_trace(),
    )
    validated = validate_cpb(cpb, carrier, result)
    assert validated.rank is Rank.REFUTED
    assert any(f.kind == "cpb.domain_mismatch" and f.fatal for f in validated.failures)


def test_validate_cpb_passes_when_domain_matches_and_evidence_cites_carrier():
    cpb = CPB(name="b", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="كاتب", label="كاتب")
    result = Result(
        value=("ك", "ت", "ب"),
        rank=Rank.LICENSED,
        evidence=(Evidence(kind="root.extract", source="كاتب"),),
        residuals=(),
        trace=_trace(),
    )
    validated = validate_cpb(cpb, carrier, result)
    assert validated.rank is Rank.LICENSED
    assert validated.failures == ()


# ---------------------------------------------------------------------------
# Uncited output.
# ---------------------------------------------------------------------------


def test_validate_cpb_rejects_uncited_licensed_output():
    cpb = CPB(name="b", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="كاتب", label="كاتب")
    bogus = Result(
        value="root",
        rank=Rank.LICENSED,
        evidence=(Evidence(kind="x", source="unrelated", detail="no link"),),
        trace=_trace(),
    )
    validated = validate_cpb(cpb, carrier, bogus)
    assert validated.rank is Rank.REFUTED
    assert any(f.kind == "cpb.uncited_output" and f.fatal for f in validated.failures)


def test_validate_cpb_rejects_uncited_certified_output():
    cpb = CPB(name="b", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="كاتب", label="كاتب")
    bogus = Result(
        value="root",
        rank=Rank.CERTIFIED,
        evidence=(Evidence(kind="x", source="unrelated"),),
        trace=_trace(),
    )
    validated = validate_cpb(cpb, carrier, bogus)
    assert validated.rank is Rank.REFUTED
    assert any(f.kind == "cpb.uncited_output" for f in validated.failures)


def test_validate_cpb_does_not_check_citation_for_unresolved_results():
    """UNRESOLVED carries no claim and is exempt from the citation check."""
    cpb = CPB(name="b", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="كاتب", label="كاتب")
    raw = Result(
        value=None,
        rank=Rank.UNRESOLVED,
        trace=_trace(),
    )
    validated = validate_cpb(cpb, carrier, raw)
    assert validated.rank is Rank.UNRESOLVED
    assert validated.failures == ()


def test_validate_cpb_accepts_citation_in_evidence_detail():
    """Citation may appear in either ``source`` or ``detail`` of an Evidence."""
    cpb = CPB(name="b", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="كاتب", label="كاتب")
    result = Result(
        value=("ك", "ت", "ب"),
        rank=Rank.LICENSED,
        evidence=(Evidence(kind="root.extract", source="rule:42", detail="from كاتب"),),
        trace=_trace(),
    )
    validated = validate_cpb(cpb, carrier, result)
    assert validated.failures == ()


def test_validate_cpb_falls_back_to_domain_when_label_is_empty():
    """If carrier has no label, the domain name is used as the citation key."""
    cpb = CPB(name="b", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="x", label="")
    result = Result(
        value="r",
        rank=Rank.LICENSED,
        evidence=(Evidence(kind="k", source="from morph_surface input"),),
        trace=_trace(),
    )
    validated = validate_cpb(cpb, carrier, result)
    assert validated.failures == ()


# ---------------------------------------------------------------------------
# CPB construction-time guards.
# ---------------------------------------------------------------------------


def test_cpb_requires_non_empty_name():
    with pytest.raises(ValueError):
        CPB(name="", source=Domain.GRAPHEME, target=Domain.PHONEME)


def test_cpb_construction_rejects_self_unrelated_pair():
    """Unspecified pairs (neither in ALLOWED nor FORBIDDEN) must fail at construction."""
    # GRAPHEME -> SYLLABLE is neither explicitly allowed nor explicitly forbidden;
    # since is_bridge_allowed defaults to False, CPB construction must refuse it.
    with pytest.raises(ValueError):
        CPB(name="skip-phoneme", source=Domain.GRAPHEME, target=Domain.SYLLABLE)


# ---------------------------------------------------------------------------
# Failure cumulation: an already-failed result keeps its prior failures.
# ---------------------------------------------------------------------------


def test_validate_cpb_preserves_existing_failures():
    cpb = CPB(name="b", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
    carrier = Carrier(domain=Domain.PHONEME, value="x", label="x")
    prior = Result(
        value="r",
        rank=Rank.REFUTED,
        failures=(Failure(kind="prior", description="x", fatal=True),),
        trace=_trace(),
    )
    validated = validate_cpb(cpb, carrier, prior)
    kinds = {f.kind for f in validated.failures}
    assert "prior" in kinds
    assert "cpb.domain_mismatch" in kinds
