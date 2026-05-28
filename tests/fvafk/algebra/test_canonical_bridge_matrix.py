"""Comprehensive tests for canonical GARA domain matrix topology.

This test suite validates PR-129: Canonical GARA Domain Matrix topology.

Purpose:
    - Verify CANONICAL_ALLOWED_BRIDGES and CANONICAL_FORBIDDEN_BRIDGES topology
    - Ensure is_canonical_bridge_allowed() enforces constitutional laws
    - Prove unknown bridges default to FORBIDDEN (fail-safe)
    - Validate separation between legacy and canonical topologies
    - Ensure no execution logic, meaning, ifadah, or hukm introduced

Constitutional Laws Tested:
    - لا وزن قبل جذر (no weight before root)
    - لا معنى قبل نحو (no meaning before syntax)
    - لا حكم قبل دليل (no judgment before evidence)
    - لا انتقال من اللفظ المفرد إلى المعنى (no isolated-word → meaning jump)
"""

from __future__ import annotations

import itertools

import pytest

from fvafk.algebra import Domain
from fvafk.algebra.arabic_layers import (
    CANONICAL_ALLOWED_BRIDGES,
    CANONICAL_FORBIDDEN_BRIDGES,
    is_canonical_bridge_allowed,
    is_legacy_bridge_allowed,
    is_bridge_allowed,
)


# =============================================================================
# Test Set 1: Canonical Domain Membership
# =============================================================================


CANONICAL_GARA_DOMAINS = {
    # Surface and Script Domains (U₀-U₁)
    "SCRIPT",
    "SOUND",
    # Phonological Domains (U₂-U₃)
    "SYLLABLE_CANONICAL",
    "BOUNDARY",
    # Lexical Unit Domain (U₄)
    "LAFZ",
    # Surface Protection Domains (U₇)
    "MARKER_PROTECTION",
    "CLAUSE_AGREEMENT",
    # Morphological Domains (U₈-U₉)
    "ROOT_STEM",
    "WEIGHT",
    # Identity Domain (U₅-U₆)
    "IDENTITY",
    # Derivational Domains (U₁₀+)
    "SOURCE_FORM",
    "ATTRIBUTE_FORM",
    "FUNCTIONAL_FORM",
    "WORDFORM",
    # Syntactic Domains (U₁₃+)
    "I3RAB_SURFACE",
    "AMIL_RELATION",
    "SYNTAX_CANONICAL",
    # Semantic Domains (U₁₄-U₁₅)
    "SEMANTICS_CANONICAL",
    "PRAGMATICS",
    # Meta-Domains
    "EVIDENCE",
    "JUDGMENT",
}


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


def test_domain_enum_contains_all_canonical_domains():
    """Domain enum must contain exactly all 20 canonical GARA domains."""
    domain_names = {d.name for d in Domain}
    assert domain_names >= CANONICAL_GARA_DOMAINS, (
        f"Missing canonical domains: {CANONICAL_GARA_DOMAINS - domain_names}"
    )
    # Exact match: domain_names should contain canonical + legacy (29 total)
    expected_total = CANONICAL_GARA_DOMAINS | LEGACY_FVAFK_DOMAINS
    assert domain_names == expected_total, (
        f"Domain enum should contain exactly canonical + legacy domains. "
        f"Extra: {domain_names - expected_total}, Missing: {expected_total - domain_names}"
    )


def test_domain_enum_preserves_legacy_domains():
    """Domain enum must preserve all 9 legacy FVAFK domains for compatibility."""
    domain_names = {d.name for d in Domain}
    assert LEGACY_FVAFK_DOMAINS.issubset(domain_names), (
        f"Missing legacy domains: {LEGACY_FVAFK_DOMAINS - domain_names}"
    )


def test_canonical_and_legacy_domains_are_disjoint():
    """Canonical and legacy domain sets must be completely separate."""
    assert CANONICAL_GARA_DOMAINS.isdisjoint(LEGACY_FVAFK_DOMAINS), (
        "Canonical and legacy domains must not overlap"
    )


# =============================================================================
# Test Set 2: CANONICAL_ALLOWED_BRIDGES Validation
# =============================================================================


@pytest.mark.parametrize(
    "source,target",
    sorted(CANONICAL_ALLOWED_BRIDGES, key=lambda p: (p[0].name, p[1].name)),
    ids=lambda p: getattr(p, "name", str(p)),
)
def test_every_canonical_allowed_bridge_is_recognized(
    source: Domain, target: Domain
):
    """is_canonical_bridge_allowed() must return True for each CANONICAL_ALLOWED entry."""
    assert is_canonical_bridge_allowed(source, target) is True, (
        f"Canonical allowed bridge {source.name} → {target.name} not recognized"
    )


def test_canonical_allowed_bridges_count():
    """CANONICAL_ALLOWED_BRIDGES must contain exactly 24 bridges."""
    assert len(CANONICAL_ALLOWED_BRIDGES) == 24, (
        f"Expected 24 canonical allowed bridges, got {len(CANONICAL_ALLOWED_BRIDGES)}"
    )


def test_canonical_allowed_bridges_only_use_canonical_domains():
    """All bridges in CANONICAL_ALLOWED_BRIDGES must use only canonical domains."""
    for source, target in CANONICAL_ALLOWED_BRIDGES:
        assert source.name in CANONICAL_GARA_DOMAINS, (
            f"Bridge {source.name} → {target.name} uses non-canonical source"
        )
        assert target.name in CANONICAL_GARA_DOMAINS, (
            f"Bridge {source.name} → {target.name} uses non-canonical target"
        )


# =============================================================================
# Test Set 3: CANONICAL_FORBIDDEN_BRIDGES Validation
# =============================================================================


@pytest.mark.parametrize(
    "source,target",
    sorted(CANONICAL_FORBIDDEN_BRIDGES, key=lambda p: (p[0].name, p[1].name)),
    ids=lambda p: getattr(p, "name", str(p)),
)
def test_every_canonical_forbidden_bridge_is_rejected(
    source: Domain, target: Domain
):
    """is_canonical_bridge_allowed() must return False for each CANONICAL_FORBIDDEN entry."""
    assert is_canonical_bridge_allowed(source, target) is False, (
        f"Canonical forbidden bridge {source.name} → {target.name} not rejected"
    )


def test_canonical_forbidden_bridges_count():
    """CANONICAL_FORBIDDEN_BRIDGES must contain exactly 44 forbidden jumps."""
    assert len(CANONICAL_FORBIDDEN_BRIDGES) == 44, (
        f"Expected 44 canonical forbidden bridges, got {len(CANONICAL_FORBIDDEN_BRIDGES)}"
    )


def test_canonical_allowed_and_forbidden_are_disjoint():
    """A bridge may not be both allowed and forbidden simultaneously."""
    assert CANONICAL_ALLOWED_BRIDGES.isdisjoint(CANONICAL_FORBIDDEN_BRIDGES), (
        "Canonical allowed and forbidden bridges must be disjoint"
    )


# =============================================================================
# Test Set 4: Constitutional Law Enforcement
# =============================================================================


def test_no_weight_before_root_stem():
    """Constitutional law: لا وزن قبل جذر (no weight before root)."""
    # All surface/phonological layers → WEIGHT must be forbidden
    for source_name in ["SCRIPT", "SOUND", "SYLLABLE_CANONICAL", "BOUNDARY", "LAFZ"]:
        source = Domain[source_name]
        assert is_canonical_bridge_allowed(source, Domain.WEIGHT) is False, (
            f"{source_name} → WEIGHT must be forbidden (no weight before root)"
        )


def test_no_meaning_before_syntax():
    """Constitutional law: لا معنى قبل نحو (no meaning before syntax)."""
    # All non-syntax layers → SEMANTICS_CANONICAL must be forbidden
    forbidden_sources = [
        "SCRIPT", "SOUND", "SYLLABLE_CANONICAL", "BOUNDARY", "LAFZ",
        "ROOT_STEM", "WEIGHT", "IDENTITY",
        "SOURCE_FORM", "ATTRIBUTE_FORM", "FUNCTIONAL_FORM", "WORDFORM",
    ]
    for source_name in forbidden_sources:
        source = Domain[source_name]
        assert is_canonical_bridge_allowed(source, Domain.SEMANTICS_CANONICAL) is False, (
            f"{source_name} → SEMANTICS_CANONICAL must be forbidden (no meaning before syntax)"
        )


def test_no_judgment_before_evidence():
    """Constitutional law: لا حكم قبل دليل (no judgment without evidence)."""
    # All layers except EVIDENCE → JUDGMENT must be forbidden
    all_domains = {d for d in Domain if d.name in CANONICAL_GARA_DOMAINS}
    for source in all_domains:
        if source == Domain.EVIDENCE:
            # Only EVIDENCE → JUDGMENT is allowed
            assert is_canonical_bridge_allowed(source, Domain.JUDGMENT) is True, (
                "EVIDENCE → JUDGMENT must be allowed"
            )
        elif source == Domain.JUDGMENT:
            # JUDGMENT → JUDGMENT is identity bridge (always allowed), skip
            continue
        else:
            # All other domains → JUDGMENT must be forbidden
            assert is_canonical_bridge_allowed(source, Domain.JUDGMENT) is False, (
                f"{source.name} → JUDGMENT must be forbidden (no judgment without evidence)"
            )


def test_no_isolated_word_to_meaning_jump():
    """Constitutional law: لا انتقال من اللفظ المفرد إلى المعنى (no isolated-word → meaning)."""
    # LAFZ and WORDFORM → SEMANTICS_CANONICAL must be forbidden
    assert is_canonical_bridge_allowed(Domain.LAFZ, Domain.SEMANTICS_CANONICAL) is False
    assert is_canonical_bridge_allowed(Domain.WORDFORM, Domain.SEMANTICS_CANONICAL) is False


# =============================================================================
# Test Set 5: Topology Consistency
# =============================================================================


@pytest.mark.parametrize("domain", [d for d in Domain if d.name in CANONICAL_GARA_DOMAINS])
def test_canonical_identity_bridges_are_always_legal(domain: Domain):
    """A carrier staying in its own domain is always a legal no-op."""
    assert is_canonical_bridge_allowed(domain, domain) is True, (
        f"Identity bridge {domain.name} → {domain.name} must be allowed"
    )


def test_canonical_unknown_pairs_default_to_forbidden():
    """Pairs neither in CANONICAL_ALLOWED nor CANONICAL_FORBIDDEN must be rejected.

    This enforces fail-safe semantics: only explicit CANONICAL_ALLOWED entries are legal.
    """
    canonical_domains = [d for d in Domain if d.name in CANONICAL_GARA_DOMAINS]
    explicit = CANONICAL_ALLOWED_BRIDGES | CANONICAL_FORBIDDEN_BRIDGES

    unspecified = [
        (s, t)
        for s, t in itertools.product(canonical_domains, canonical_domains)
        if s is not t and (s, t) not in explicit
    ]

    # Verify at least some unspecified pairs exist (sanity check)
    assert unspecified, "Expected some unspecified canonical domain pairs to exist"

    # All unspecified pairs must be rejected
    for s, t in unspecified:
        assert is_canonical_bridge_allowed(s, t) is False, (
            f"Unspecified canonical pair {s.name} → {t.name} must default to forbidden"
        )


# =============================================================================
# Test Set 6: Legacy vs Canonical Separation
# =============================================================================


def test_is_legacy_bridge_allowed_unchanged():
    """is_legacy_bridge_allowed() must preserve original FVAFK behavior."""
    # Test a few known legacy bridges
    assert is_legacy_bridge_allowed(Domain.GRAPHEME, Domain.PHONEME) is True
    assert is_legacy_bridge_allowed(Domain.SYLLABLE, Domain.ROOT) is False
    assert is_legacy_bridge_allowed(Domain.MORPH_SURFACE, Domain.MORPH_SURFACE) is True


def test_is_bridge_allowed_delegates_to_legacy():
    """is_bridge_allowed() must delegate to is_legacy_bridge_allowed() for compatibility."""
    # Test that both functions return the same result for legacy domains
    legacy_test_pairs = [
        (Domain.GRAPHEME, Domain.PHONEME),
        (Domain.SYLLABLE, Domain.ROOT),
        (Domain.MORPH_DEEP, Domain.SYNTAX),
    ]

    for source, target in legacy_test_pairs:
        assert is_bridge_allowed(source, target) == is_legacy_bridge_allowed(source, target), (
            f"is_bridge_allowed must delegate to is_legacy_bridge_allowed for {source.name} → {target.name}"
        )


def test_canonical_and_legacy_functions_are_independent():
    """Canonical and legacy bridge functions must operate on separate topologies."""
    # SCRIPT → SOUND is canonical allowed, but should not affect legacy
    assert is_canonical_bridge_allowed(Domain.SCRIPT, Domain.SOUND) is True
    assert is_legacy_bridge_allowed(Domain.SCRIPT, Domain.SOUND) is False  # Not in legacy bridges


# =============================================================================
# Test Set 7: Architectural Path Validation
# =============================================================================


def test_surface_to_judgment_requires_full_path():
    """Surface domains → JUDGMENT requires the full canonical path."""
    # SCRIPT → ... → JUDGMENT: must go through all intermediate layers
    # Direct jumps from SCRIPT to JUDGMENT must be forbidden
    assert is_canonical_bridge_allowed(Domain.SCRIPT, Domain.JUDGMENT) is False

    # Verify the full path exists (not testing reachability, just direct bridges)
    assert is_canonical_bridge_allowed(Domain.SCRIPT, Domain.SOUND) is True
    assert is_canonical_bridge_allowed(Domain.EVIDENCE, Domain.JUDGMENT) is True


def test_derivational_forms_converge_to_wordform():
    """All derivational forms (SOURCE, ATTRIBUTE, FUNCTIONAL) must converge to WORDFORM."""
    assert is_canonical_bridge_allowed(Domain.SOURCE_FORM, Domain.WORDFORM) is True
    assert is_canonical_bridge_allowed(Domain.ATTRIBUTE_FORM, Domain.WORDFORM) is True
    assert is_canonical_bridge_allowed(Domain.FUNCTIONAL_FORM, Domain.WORDFORM) is True


def test_syntactic_domains_converge_to_syntax_canonical():
    """Syntactic domains (I3RAB_SURFACE, AMIL_RELATION) must converge to SYNTAX_CANONICAL."""
    assert is_canonical_bridge_allowed(Domain.I3RAB_SURFACE, Domain.SYNTAX_CANONICAL) is True
    assert is_canonical_bridge_allowed(Domain.AMIL_RELATION, Domain.SYNTAX_CANONICAL) is True


def test_protection_domains_both_lead_to_root_stem():
    """Both protection domains must lead to ROOT_STEM (parallel paths)."""
    assert is_canonical_bridge_allowed(Domain.MARKER_PROTECTION, Domain.ROOT_STEM) is True
    assert is_canonical_bridge_allowed(Domain.CLAUSE_AGREEMENT, Domain.ROOT_STEM) is True


# =============================================================================
# Test Set 8: PR-129 Scope Compliance
# =============================================================================


def test_no_execution_logic_in_module():
    """arabic_layers.py must contain ONLY topology declarations, no execution logic.

    This test verifies that the module does not import or define:
    - Operation classes
    - Gate classes
    - Carrier transformation logic
    - Meaning/Ifadah/Hukm semantics
    """
    import fvafk.algebra.arabic_layers as module

    # Check that only expected symbols are exported
    forbidden_symbols = [
        "Operation", "Gate", "Carrier", "Transform", "Transition",
        "Meaning", "Ifadah", "Hukm", "Murad", "HaqiqaMajaz",
        "apply", "execute", "compute", "infer", "decide",
    ]

    module_attrs = dir(module)
    for symbol in forbidden_symbols:
        assert symbol not in module_attrs, (
            f"Forbidden symbol '{symbol}' found in arabic_layers.py - "
            "module must contain only topology declarations"
        )


def test_module_only_exports_topology():
    """__all__ must export only Domain enum and bridge topology."""
    from fvafk.algebra.arabic_layers import __all__

    expected_exports = {
        "Domain",
        "ALLOWED_BRIDGES",
        "FORBIDDEN_BRIDGES",
        "is_bridge_allowed",
        "is_legacy_bridge_allowed",
        "CANONICAL_ALLOWED_BRIDGES",
        "CANONICAL_FORBIDDEN_BRIDGES",
        "is_canonical_bridge_allowed",
    }

    assert set(__all__) == expected_exports, (
        f"__all__ exports unexpected symbols. Expected: {expected_exports}, Got: {set(__all__)}"
    )


# =============================================================================
# Test Set 9: Edge Cases and Boundary Conditions
# =============================================================================


def test_no_self_loops_in_allowed_bridges():
    """CANONICAL_ALLOWED_BRIDGES should not contain identity bridges (handled separately)."""
    for source, target in CANONICAL_ALLOWED_BRIDGES:
        assert source != target, (
            f"Identity bridge {source.name} → {target.name} should not be in CANONICAL_ALLOWED_BRIDGES"
        )


def test_no_backward_bridges_in_allowed():
    """Canonical allowed bridges should generally flow forward in layer hierarchy.

    This is a soft constraint - we check that most bridges move "forward" in the
    typical U₀ → U₁₅ progression.
    """
    # Define rough layer ordering (U₀ → U₁₅)
    layer_order = {
        "SCRIPT": 0,
        "SOUND": 1,
        "SYLLABLE_CANONICAL": 2,
        "BOUNDARY": 3,
        "LAFZ": 4,
        "MARKER_PROTECTION": 7,
        "CLAUSE_AGREEMENT": 7,
        "ROOT_STEM": 8,
        "WEIGHT": 9,
        "IDENTITY": 6,  # Special: can come after Weight or before
        "SOURCE_FORM": 10,
        "ATTRIBUTE_FORM": 10,
        "FUNCTIONAL_FORM": 10,
        "WORDFORM": 10,
        "I3RAB_SURFACE": 13,
        "AMIL_RELATION": 13,
        "SYNTAX_CANONICAL": 13,
        "SEMANTICS_CANONICAL": 14,
        "PRAGMATICS": 14,
        "EVIDENCE": 15,
        "JUDGMENT": 15,
    }

    backward_bridges = []
    for source, target in CANONICAL_ALLOWED_BRIDGES:
        if source.name in layer_order and target.name in layer_order:
            if layer_order[source.name] > layer_order[target.name]:
                backward_bridges.append((source.name, target.name))

    # Allow some backward/parallel bridges (e.g., convergence patterns)
    # but verify the list is small
    assert len(backward_bridges) <= 2, (
        f"Too many backward bridges detected: {backward_bridges}"
    )


# =============================================================================
# Test Set 10: Path-Aware Bridges (LAFZ → IDENTITY)
# =============================================================================


def test_lafz_to_identity_not_forbidden_categorically():
    """LAFZ → IDENTITY must NOT be in CANONICAL_FORBIDDEN_BRIDGES.

    Constitutional requirement: LAFZ → IDENTITY is path-aware, not categorically forbidden.

    Two valid paths exist:
    1. Mushtaq (derived) path: LAFZ → ROOT_STEM → WEIGHT → IDENTITY
    2. Non-weight path: LAFZ → IDENTITY (for mabni, particles, pronouns, jāmid, etc.)

    Forbidding this bridge categorically violates: لا هوية من الوزن وحده
    (No Identity from weight alone)
    """
    assert (Domain.LAFZ, Domain.IDENTITY) not in CANONICAL_FORBIDDEN_BRIDGES, (
        "LAFZ → IDENTITY must not be forbidden categorically; "
        "it is path-aware (allows mabni, particles, pronouns, jāmid, proper names, loans)"
    )


def test_lafz_to_identity_not_globally_allowed():
    """LAFZ → IDENTITY must NOT be in CANONICAL_ALLOWED_BRIDGES.

    Constitutional requirement: LAFZ → IDENTITY requires path-aware validation.

    This bridge is not a universal allowed bridge. It requires:
    - PathAwareIdentityValidator to determine which path applies
    - Either: mushtaq path through ROOT_STEM → WEIGHT
    - Or: non-weight path for closed-class items

    Making this globally allowed would bypass path validation.
    """
    assert (Domain.LAFZ, Domain.IDENTITY) not in CANONICAL_ALLOWED_BRIDGES, (
        "LAFZ → IDENTITY must not be globally allowed; "
        "it requires path-aware validation (PathAwareIdentityValidator)"
    )


def test_lafz_to_identity_path_awareness():
    """LAFZ → IDENTITY must be neither allowed nor forbidden by default checks.

    This proves the bridge is truly path-aware (delegated to validators).

    - is_canonical_bridge_allowed(LAFZ, IDENTITY) returns False (not in allowed set)
    - (LAFZ, IDENTITY) not in CANONICAL_FORBIDDEN_BRIDGES (not categorically forbidden)

    Result: The bridge requires explicit path-aware validation at runtime.
    """
    # Not globally allowed
    assert is_canonical_bridge_allowed(Domain.LAFZ, Domain.IDENTITY) is False, (
        "LAFZ → IDENTITY should not be globally allowed"
    )

    # Not categorically forbidden
    assert (Domain.LAFZ, Domain.IDENTITY) not in CANONICAL_FORBIDDEN_BRIDGES, (
        "LAFZ → IDENTITY should not be categorically forbidden"
    )

    # This combination means: path-aware validation required

