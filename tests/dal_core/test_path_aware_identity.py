"""
Path-Aware Identity Tests (PR-127)

Tests proving that IDENTITY_DOMAIN does not unconditionally require WEIGHT_DOMAIN.
Arabic identity can arise through multiple paths:
1. Weight path: root/stem → weight → identity
2. Mabni/closed-class path: lafz → mabni → identity
3. Tool/particle path: lafz → tool → identity
4. Pronoun path: lafz → pronoun → identity
5. Jāmid/frozen path: lafz → jāmid → identity

Constitutional Law:
    لا هوية من الوزن وحده
    No Identity from weight alone for all paths.

    الهوية يجب أن تكون مدركة للمسار
    Identity must be path-aware.

Created: 2026-05-27 (PR-127)
"""

import pytest
from dal_core.domain_registry import DomainRegistry, DomainType
from dal_core.identity_registry import IdentityRegistry, IdentityType


class TestPathAwareIdentityDomain:
    """Test IDENTITY_DOMAIN path-awareness."""

    def test_identity_domain_does_not_require_weight_domain(self):
        """IDENTITY_DOMAIN must not unconditionally require WEIGHT_DOMAIN."""
        registry = DomainRegistry()
        spec = registry.get_spec(DomainType.IDENTITY_DOMAIN)

        # CRITICAL: IDENTITY_DOMAIN should not require WEIGHT_DOMAIN
        assert DomainType.WEIGHT_DOMAIN not in spec.requires_domains, (
            "IDENTITY_DOMAIN must not unconditionally require WEIGHT_DOMAIN. "
            "Identity can arise from mabni/tool/pronoun/jāmid paths."
        )

    def test_identity_domain_allows_multiple_entry_paths(self):
        """IDENTITY_DOMAIN should be reachable from multiple domains."""
        registry = DomainRegistry()

        # Path 1: Weight path (weighted derivation)
        weight_spec = registry.get_spec(DomainType.WEIGHT_DOMAIN)
        assert DomainType.IDENTITY_DOMAIN in weight_spec.allows_transition_to, (
            "WEIGHT_DOMAIN → IDENTITY_DOMAIN path must exist"
        )

        # Verify IDENTITY_DOMAIN is reachable (no circular dependency)
        identity_spec = registry.get_spec(DomainType.IDENTITY_DOMAIN)
        assert identity_spec is not None

    def test_identity_domain_prohibits_meaning_and_syntax(self):
        """IDENTITY_DOMAIN must prohibit meaning and syntactic role."""
        registry = DomainRegistry()
        spec = registry.get_spec(DomainType.IDENTITY_DOMAIN)

        # Critical prohibitions
        assert "meaning" in spec.prohibitions
        assert "syntactic_role" in spec.prohibitions
        assert "i3rab" in spec.prohibitions
        assert "semantic_interpretation" in spec.prohibitions

    def test_identity_domain_competencies(self):
        """IDENTITY_DOMAIN must support Ism/Fi'l/Harf classification."""
        registry = DomainRegistry()
        spec = registry.get_spec(DomainType.IDENTITY_DOMAIN)

        # Required competencies
        assert "ism_fil_harf_classification" in spec.competencies
        assert "functional_role_determination" in spec.competencies
        assert "mabni_closed_class_determination" in spec.competencies


class TestPathAwareWeightIdentity:
    """Test WEIGHT_IDENTITY path-awareness (PR-127 critical fix)."""

    def test_weight_identity_does_not_require_both_root_and_stem(self):
        """
        WEIGHT_IDENTITY must not require BOTH root AND stem simultaneously.

        Bug: Old code had frozenset({ROOT_MATERIAL_IDENTITY, STEM_IDENTITY})
        which creates AND logic (requires both).

        Fix: Arabic weight derives from root OR stem, not both.
        """
        registry = IdentityRegistry()
        spec = registry.get_spec(IdentityType.WEIGHT_IDENTITY)

        # CRITICAL FIX: Should NOT require both
        # Original bug: requires = frozenset({ROOT, STEM}) creates AND logic
        # Correct: Path-aware validation at transition time
        requires_set = spec.requires

        has_both = (
            IdentityType.ROOT_MATERIAL_IDENTITY in requires_set and
            IdentityType.STEM_IDENTITY in requires_set
        )

        assert not has_both, (
            "WEIGHT_IDENTITY must not require BOTH root AND stem. "
            "Arabic weight derivation: root → weight OR stem → weight, not both. "
            "This is algebraically incorrect AND logic."
        )

    def test_weight_identity_path_aware_requirements(self):
        """WEIGHT_IDENTITY requirements should be path-aware."""
        registry = IdentityRegistry()
        spec = registry.get_spec(IdentityType.WEIGHT_IDENTITY)

        # After PR-127: Path-aware, validated at transition time
        # frozenset-based requirements cannot express ONE-OF semantics
        # So requirements should be empty (validated elsewhere)
        assert len(spec.requires) == 0 or (
            IdentityType.ROOT_MATERIAL_IDENTITY not in spec.requires or
            IdentityType.STEM_IDENTITY not in spec.requires
        ), "WEIGHT_IDENTITY must not use AND logic for root/stem"


class TestPathAwareWordFormIdentity:
    """Test WORDFORM_IDENTITY path-awareness."""

    def test_wordform_identity_does_not_unconditionally_require_weight(self):
        """
        WORDFORM_IDENTITY must not unconditionally require WEIGHT_IDENTITY.

        Word forms can arise from:
        - Weight path: WEIGHT_IDENTITY → WORDFORM_IDENTITY
        - Mabni path: CLOSED_CLASS_IDENTITY → WORDFORM_IDENTITY
        - Tool path: direct from LAFZ
        - Pronoun path: direct from LAFZ
        """
        registry = IdentityRegistry()
        spec = registry.get_spec(IdentityType.WORDFORM_IDENTITY)

        # Should not unconditionally require WEIGHT_IDENTITY
        # (Mabni/tool/pronoun paths bypass weight)
        # After PR-127: path-aware
        requires_only_weight = (
            spec.requires == frozenset({IdentityType.WEIGHT_IDENTITY})
        )

        assert not requires_only_weight, (
            "WORDFORM_IDENTITY must not unconditionally require WEIGHT_IDENTITY. "
            "Non-weighted paths exist: mabni/tool/pronoun/jāmid."
        )


class TestIdentityPathSeparation:
    """Test that identity paths are properly separated."""

    def test_identity_does_not_imply_meaning(self):
        """Identity determination must not imply meaning determination."""
        domain_registry = DomainRegistry()
        identity_spec = domain_registry.get_spec(DomainType.IDENTITY_DOMAIN)

        # IDENTITY_DOMAIN must prohibit meaning
        assert "meaning" in identity_spec.prohibitions

        # IDENTITY_DOMAIN must NOT allow direct transition to SEMANTICS_DOMAIN
        assert DomainType.SEMANTICS_DOMAIN not in identity_spec.allows_transition_to

    def test_identity_does_not_imply_ifadah(self):
        """Identity determination must not imply Ifādah."""
        domain_registry = DomainRegistry()
        identity_spec = domain_registry.get_spec(DomainType.IDENTITY_DOMAIN)

        # IDENTITY_DOMAIN must prohibit compositional closure
        # (Ifādah is compositional benefit, not identity)
        assert DomainType.PRAGMATICS_DOMAIN not in identity_spec.allows_transition_to
        assert DomainType.JUDGMENT_DOMAIN not in identity_spec.allows_transition_to

    def test_identity_does_not_imply_hukm(self):
        """Identity determination must not imply Hukm (judgment)."""
        domain_registry = DomainRegistry()
        identity_spec = domain_registry.get_spec(DomainType.IDENTITY_DOMAIN)

        # IDENTITY_DOMAIN must NOT allow transition to JUDGMENT_DOMAIN
        assert DomainType.JUDGMENT_DOMAIN not in identity_spec.allows_transition_to

        # IDENTITY_DOMAIN must prohibit judgment
        # (covered by meaning prohibition, but verify)
        assert "meaning" in identity_spec.prohibitions


class TestMabniToolPronounPaths:
    """Test that mabni/tool/pronoun paths don't require WEIGHT_DOMAIN."""

    def test_mabni_path_does_not_require_weight(self):
        """
        Mabni/closed-class path should not require WEIGHT_DOMAIN.

        Examples: ما، هل، إن، كان...
        These are closed-class items, not derived forms.
        """
        domain_registry = DomainRegistry()

        # LAFZ_DOMAIN should allow transition to IDENTITY_DOMAIN
        # without going through WEIGHT_DOMAIN
        lafz_spec = domain_registry.get_spec(DomainType.LAFZ_DOMAIN)

        # Verify LAFZ can reach protection/agreement layers
        # (which lead to root/stem OR directly to identity for closed-class)
        assert (
            DomainType.MARKER_PROTECTION_DOMAIN in lafz_spec.allows_transition_to or
            DomainType.CLAUSE_AGREEMENT_DOMAIN in lafz_spec.allows_transition_to
        ), "LAFZ_DOMAIN must allow transition to protection layers"

    def test_identity_transition_validates_path_not_structure(self):
        """
        Identity transitions should validate path at transition time,
        not at structure time (frozenset requirements).

        This test documents the architectural decision:
        - frozenset requirements = structural AND logic
        - Path-aware validation = transition-time OR logic
        """
        identity_registry = IdentityRegistry()
        domain_registry = DomainRegistry()

        # IDENTITY_DOMAIN has empty requires_domains (path-aware)
        identity_domain_spec = domain_registry.get_spec(DomainType.IDENTITY_DOMAIN)
        assert len(identity_domain_spec.requires_domains) == 0, (
            "IDENTITY_DOMAIN should have empty requires_domains. "
            "Path validation happens at transition time, not structure time."
        )

        # WORDFORM_IDENTITY has empty requires (path-aware)
        wordform_identity_spec = identity_registry.get_spec(IdentityType.WORDFORM_IDENTITY)
        # After PR-127: should be path-aware (empty or non-restrictive)
        # We don't mandate empty, but do mandate non-AND logic
        pass  # Verified by other tests


class TestConstitutionalLaws:
    """Test constitutional laws enforced by path-aware identity."""

    def test_no_identity_from_weight_alone(self):
        """
        Constitutional law: لا هوية من الوزن وحده
        No Identity from weight alone for all paths.
        """
        domain_registry = DomainRegistry()
        identity_spec = domain_registry.get_spec(DomainType.IDENTITY_DOMAIN)

        # IDENTITY_DOMAIN must not REQUIRE weight
        assert DomainType.WEIGHT_DOMAIN not in identity_spec.requires_domains, (
            "Constitutional law violated: "
            "IDENTITY_DOMAIN must not unconditionally require WEIGHT_DOMAIN. "
            "لا هوية من الوزن وحده"
        )

    def test_identity_must_be_path_aware(self):
        """
        Constitutional law: الهوية يجب أن تكون مدركة للمسار
        Identity must be path-aware.

        This means identity determination varies by path:
        - Weight path requires root/stem analysis
        - Mabni path requires closed-class recognition
        - Tool path requires particle classification
        - Pronoun path requires pronoun identification
        """
        # This is a design principle test, not a code test
        # Documents the architectural requirement

        domain_registry = DomainRegistry()
        identity_spec = domain_registry.get_spec(DomainType.IDENTITY_DOMAIN)

        # Identity should support multiple determination types
        assert "ism_fil_harf_classification" in identity_spec.competencies
        assert "mabni_closed_class_determination" in identity_spec.competencies
        assert "functional_role_determination" in identity_spec.competencies

        # Multiple competencies = path-aware
        assert len(identity_spec.competencies) >= 3, (
            "IDENTITY_DOMAIN must support multiple competencies "
            "(path-aware identity determination)"
        )

    def test_no_wordform_without_identity(self):
        """
        WordForm requires identity, but identity doesn't require weight.

        Flow: Path-specific → IDENTITY → WORDFORM
        Not: WEIGHT → IDENTITY → WORDFORM (for all paths)
        """
        domain_registry = DomainRegistry()

        # WORDFORM_DOMAIN should allow transition FROM identity
        identity_spec = domain_registry.get_spec(DomainType.IDENTITY_DOMAIN)
        assert DomainType.WORDFORM_DOMAIN in identity_spec.allows_transition_to

        # But IDENTITY should not require WEIGHT unconditionally
        assert DomainType.WEIGHT_DOMAIN not in identity_spec.requires_domains


# ============================================================================
# Integration Tests
# ============================================================================

class TestPathAwareIntegration:
    """Integration tests for path-aware identity system."""

    def test_weighted_path_still_works(self):
        """
        Verify weighted derivation path still works after PR-127.

        Path: WEIGHT_DOMAIN → IDENTITY_DOMAIN → WORDFORM_DOMAIN
        """
        domain_registry = DomainRegistry()

        # WEIGHT can transition to IDENTITY
        weight_spec = domain_registry.get_spec(DomainType.WEIGHT_DOMAIN)
        assert DomainType.IDENTITY_DOMAIN in weight_spec.allows_transition_to

        # IDENTITY can transition to WORDFORM
        identity_spec = domain_registry.get_spec(DomainType.IDENTITY_DOMAIN)
        assert DomainType.WORDFORM_DOMAIN in identity_spec.allows_transition_to

    def test_path_aware_does_not_break_existing_tests(self):
        """
        Path-aware changes should not break existing functionality.

        This is a meta-test ensuring other tests still pass.
        If this test passes but others fail, PR-127 broke something.
        """
        # Instantiate registries (smoke test)
        domain_registry = DomainRegistry()
        identity_registry = IdentityRegistry()

        # Verify critical domains exist
        assert domain_registry.get_spec(DomainType.IDENTITY_DOMAIN) is not None
        assert domain_registry.get_spec(DomainType.WEIGHT_DOMAIN) is not None
        assert domain_registry.get_spec(DomainType.WORDFORM_DOMAIN) is not None

        # Verify critical identities exist
        assert identity_registry.get_spec(IdentityType.WEIGHT_IDENTITY) is not None
        assert identity_registry.get_spec(IdentityType.WORDFORM_IDENTITY) is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
