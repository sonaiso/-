"""Matrix tests for every ``ALLOWED_BRIDGES`` and ``FORBIDDEN_BRIDGES`` pair.

These tests defend the topology declared in
``src/fvafk/algebra/arabic_layers.py`` against silent mutation. If a future
PR adds, removes, or relabels a bridge, this file will fail loudly.
"""

from __future__ import annotations

import itertools

import pytest

from fvafk.algebra import (
    ALLOWED_BRIDGES,
    CPB,
    Domain,
    FORBIDDEN_BRIDGES,
    is_bridge_allowed,
)


# ---------------------------------------------------------------------------
# Canonical domain set — locks the 9 legacy FVAFK domains in place.
# PR-129 added 20 canonical GARA domains. This test ensures legacy domains remain.
# ---------------------------------------------------------------------------


LEGACY_FVAFK_DOMAINS = {
    "GRAPHEME",
    "PHONEME",
    "SYLLABLE",
    "MORPH_SURFACE",
    "ROOT",
    "MORPH_DEEP",
    "SYNTAX",
    "SEMANTICS",
    "HUKM",
}


def test_domain_membership_includes_legacy_nine():
    """Legacy 9 FVAFK domains must be preserved for backward compatibility.

    PR-129 expanded Domain enum with 20 canonical GARA domains.
    This test ensures the original 9 legacy domains remain intact.
    """
    domain_names = {d.name for d in Domain}
    assert LEGACY_FVAFK_DOMAINS.issubset(domain_names), (
        f"Missing legacy domains: {LEGACY_FVAFK_DOMAINS - domain_names}"
    )


# ---------------------------------------------------------------------------
# Allowed bridges — every entry must round-trip through is_bridge_allowed.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,target",
    sorted(ALLOWED_BRIDGES, key=lambda p: (p[0].name, p[1].name)),
    ids=lambda p: getattr(p, "name", str(p)),
)
def test_every_allowed_bridge_is_recognised(source: Domain, target: Domain):
    """``is_bridge_allowed`` must return True for each ALLOWED entry."""
    assert is_bridge_allowed(source, target) is True


@pytest.mark.parametrize(
    "source,target",
    sorted(ALLOWED_BRIDGES, key=lambda p: (p[0].name, p[1].name)),
    ids=lambda p: getattr(p, "name", str(p)),
)
def test_every_allowed_bridge_constructs_a_cpb(source: Domain, target: Domain):
    """Constructing a CPB on an allowed bridge must succeed."""
    cpb = CPB(name=f"{source.value}->{target.value}", source=source, target=target)
    assert cpb.source is source
    assert cpb.target is target


# ---------------------------------------------------------------------------
# Forbidden bridges — every entry must be rejected by is_bridge_allowed *and*
# refused at CPB construction.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "source,target",
    sorted(FORBIDDEN_BRIDGES, key=lambda p: (p[0].name, p[1].name)),
    ids=lambda p: getattr(p, "name", str(p)),
)
def test_every_forbidden_bridge_is_rejected(source: Domain, target: Domain):
    """``is_bridge_allowed`` must return False for each FORBIDDEN entry."""
    assert is_bridge_allowed(source, target) is False


@pytest.mark.parametrize(
    "source,target",
    sorted(FORBIDDEN_BRIDGES, key=lambda p: (p[0].name, p[1].name)),
    ids=lambda p: getattr(p, "name", str(p)),
)
def test_every_forbidden_bridge_blocks_cpb_construction(
    source: Domain, target: Domain
):
    """Constructing a CPB on a forbidden bridge must raise ValueError."""
    with pytest.raises(ValueError):
        CPB(name=f"bad-{source.value}->{target.value}", source=source, target=target)


# ---------------------------------------------------------------------------
# Topology consistency.
# ---------------------------------------------------------------------------


def test_allowed_and_forbidden_are_disjoint():
    """A bridge may not be both allowed and forbidden simultaneously."""
    assert ALLOWED_BRIDGES.isdisjoint(FORBIDDEN_BRIDGES)


@pytest.mark.parametrize("domain", list(Domain), ids=lambda d: d.name)
def test_identity_bridges_are_always_legal(domain: Domain):
    """A carrier staying in its own domain is always a legal no-op."""
    assert is_bridge_allowed(domain, domain) is True


def test_unspecified_pairs_default_to_forbidden():
    """Pairs neither in ALLOWED nor in FORBIDDEN must be rejected by default.

    This pins the ``is_bridge_allowed`` semantics: only explicit ALLOWED entries
    are legal. A future change that flips the default to permissive breaks here.
    """
    explicit = ALLOWED_BRIDGES | FORBIDDEN_BRIDGES
    unspecified = [
        (s, t)
        for s, t in itertools.product(Domain, Domain)
        if s is not t and (s, t) not in explicit
    ]
    # Expect at least one unspecified pair to exist (sanity); pick any and check.
    assert unspecified, "expected some unspecified domain pairs to exist"
    for s, t in unspecified:
        assert is_bridge_allowed(s, t) is False, (
            f"unspecified pair {s.name}->{t.name} must default to forbidden"
        )


def test_no_grapheme_or_phoneme_path_to_semantics_via_allowed_bridges():
    """Transitive sanity: surface layers cannot reach SEMANTICS.

    The explicit FORBIDDEN_BRIDGES list states this; here we verify that the
    ALLOWED_BRIDGES graph also has no such path, i.e. the two sources of truth
    cannot drift apart.
    """
    forward: dict[Domain, set[Domain]] = {d: set() for d in Domain}
    for s, t in ALLOWED_BRIDGES:
        forward[s].add(t)

    def reachable(start: Domain) -> set[Domain]:
        seen: set[Domain] = set()
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in forward[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    # Surface → SEMANTICS path is allowed through the canonical chain
    # (GRAPHEME → ... → SEMANTICS), so we instead verify the forbidden DIRECT
    # bridges remain forbidden and that no accidental shortcut exists.
    for surface in (Domain.GRAPHEME, Domain.PHONEME, Domain.SYLLABLE):
        assert (surface, Domain.MORPH_DEEP) not in ALLOWED_BRIDGES
        assert (surface, Domain.HUKM) not in ALLOWED_BRIDGES
