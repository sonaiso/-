"""
Tests for StyleSpec - مواصفة الأسلوب

Critical Laws Being Tested:
1. StyleSpec requires DomainSpec
2. StyleSpec requires EvidencePolicy
3. StyleSpec requires RankPolicy
4. StyleSpec requires ResidualPolicy
5. StyleSpec requires OperationPolicy
6. StyleSpec blocks forbidden operations
7. StyleSpec preserves domain boundaries
8. StyleSpec does NOT claim to be RationalMethod
9. StyleSpec does NOT implement ScientificMethod
10. StyleSpec does NOT implement LogicalStyle
11. StyleSpec does NOT implement LafziMadlul
12. Lafzi/Dalali domain can be declared but not executed
13. Material/Experimental domain can be declared but not executed
14. Programming/Execution domain can be declared but not executed
"""

import pytest

from gfa.methods.styles import (
    # Domain
    ThinkingDomain,
    DomainSpec,
    make_material_experimental_domain,
    make_formal_logical_domain,
    make_lafzi_dalali_domain,
    make_textual_normative_domain,
    make_programming_execution_domain,
    # Evidence
    EvidenceKind,
    EvidencePolicy,
    make_material_evidence_policy,
    make_lafzi_evidence_policy,
    # Rank
    RankPolicy,
    make_material_rank_policy,
    make_lafzi_rank_policy,
    # Residual
    ResidualPolicy,
    make_material_residual_policy,
    make_lafzi_residual_policy,
    # Operation
    OperationKind,
    OperationPolicy,
    make_material_operation_policy,
    make_lafzi_operation_policy,
    # Style
    StyleSpec,
    make_material_experimental_style,
    make_formal_logical_style,
    make_lafzi_dalali_style,
    make_textual_normative_style,
    make_programming_execution_style,
    # Validator
    StyleValidator,
    StyleValidationResult,
)

from gfa.methods.rational import PredicateRank


class TestStyleSpecRequirements:
    """Test core requirements for StyleSpec."""

    def test_style_spec_requires_domain_spec(self):
        """
        Law 1: No StyleSpec without DomainSpec.

        Attempting to create StyleSpec without DomainSpec should fail.
        """
        # This is enforced at construction time by dataclass __post_init__
        with pytest.raises(ValueError, match="DomainSpec is required"):
            StyleSpec(
                domain_spec=None,  # Missing!
                evidence_policy=make_material_evidence_policy(),
                rank_policy=make_material_rank_policy(),
                residual_policy=make_material_residual_policy(),
                operation_policy=make_material_operation_policy(),
                name_ar="test",
                name_en="test",
                description="test"
            )

    def test_style_spec_requires_evidence_policy(self):
        """Law 2: No StyleSpec without EvidencePolicy."""
        with pytest.raises(ValueError, match="EvidencePolicy is required"):
            StyleSpec(
                domain_spec=make_material_experimental_domain(),
                evidence_policy=None,  # Missing!
                rank_policy=make_material_rank_policy(),
                residual_policy=make_material_residual_policy(),
                operation_policy=make_material_operation_policy(),
                name_ar="test",
                name_en="test",
                description="test"
            )

    def test_style_spec_requires_rank_policy(self):
        """Law 3: No StyleSpec without RankPolicy."""
        with pytest.raises(ValueError, match="RankPolicy is required"):
            StyleSpec(
                domain_spec=make_material_experimental_domain(),
                evidence_policy=make_material_evidence_policy(),
                rank_policy=None,  # Missing!
                residual_policy=make_material_residual_policy(),
                operation_policy=make_material_operation_policy(),
                name_ar="test",
                name_en="test",
                description="test"
            )

    def test_style_spec_requires_residual_policy(self):
        """Law 4: No StyleSpec without ResidualPolicy."""
        with pytest.raises(ValueError, match="ResidualPolicy is required"):
            StyleSpec(
                domain_spec=make_material_experimental_domain(),
                evidence_policy=make_material_evidence_policy(),
                rank_policy=make_material_rank_policy(),
                residual_policy=None,  # Missing!
                operation_policy=make_material_operation_policy(),
                name_ar="test",
                name_en="test",
                description="test"
            )

    def test_style_spec_requires_operation_policy(self):
        """Law 5: No StyleSpec without OperationPolicy (allowed + forbidden)."""
        with pytest.raises(ValueError, match="OperationPolicy is required"):
            StyleSpec(
                domain_spec=make_material_experimental_domain(),
                evidence_policy=make_material_evidence_policy(),
                rank_policy=make_material_rank_policy(),
                residual_policy=make_material_residual_policy(),
                operation_policy=None,  # Missing!
                name_ar="test",
                name_en="test",
                description="test"
            )

    def test_style_spec_all_components_present(self):
        """Verify complete StyleSpec can be created."""
        style = make_material_experimental_style()

        assert style.domain_spec is not None
        assert style.evidence_policy is not None
        assert style.rank_policy is not None
        assert style.residual_policy is not None
        assert style.operation_policy is not None
        assert style.get_domain() == ThinkingDomain.MATERIAL_EXPERIMENTAL


class TestStyleSpecOperationBlocking:
    """Test operation blocking behavior."""

    def test_style_blocks_forbidden_operation(self):
        """
        Law 6: StyleSpec blocks forbidden operations.

        Forbidden operations are blocked with governed failure.
        """
        style = make_material_experimental_style()

        # Material domain forbids CREATE_MEANING
        assert style.blocks_forbidden_operation(OperationKind.CREATE_MEANING)

        # Validate explicitly
        result = StyleValidator.validate_operation_allowed(
            style,
            OperationKind.CREATE_MEANING
        )

        assert result.is_failure()
        assert len(result.policy_violations) > 0

    def test_style_allows_valid_operation(self):
        """StyleSpec allows valid operations."""
        style = make_material_experimental_style()

        # Material domain allows MEASURE
        assert style.allows_operation(OperationKind.MEASURE)

        # Validate explicitly
        result = StyleValidator.validate_operation_allowed(
            style,
            OperationKind.MEASURE
        )

        assert result.success


class TestStyleSpecDomainBoundary:
    """Test domain boundary preservation."""

    def test_style_preserves_domain_boundary(self):
        """
        Law 7: StyleSpec preserves domain boundaries.

        Domain jumps without bridge are blocked.
        """
        material_style = make_material_experimental_style()
        logical_style = make_formal_logical_style()

        # Same domain OK
        result = StyleValidator.validate_domain_boundary(
            material_style,
            ThinkingDomain.MATERIAL_EXPERIMENTAL
        )
        assert result.success

        # Different domain blocked
        result = StyleValidator.validate_domain_boundary(
            material_style,
            ThinkingDomain.FORMAL_LOGICAL
        )
        assert result.is_failure()
        assert len(result.domain_violations) > 0


class TestStyleSpecArchitecturalLaws:
    """Test architectural meta-laws."""

    def test_style_does_not_claim_to_be_rational_method(self):
        """
        Law 8: StyleSpec does NOT claim to be RationalMethod.

        RationalMethod is root, StyleSpec is specialization.
        """
        style = make_material_experimental_style()
        assert style.does_not_claim_to_be_rational_method()

    def test_style_does_not_implement_scientific_method(self):
        """
        Law 9: StyleSpec does NOT implement ScientificMethod.

        This PR only declares, does not implement.
        """
        style = make_material_experimental_style()
        assert style.does_not_implement_scientific_method()

    def test_style_does_not_implement_logical_style(self):
        """
        Law 10: StyleSpec does NOT implement LogicalStyle.

        This PR only declares, does not implement.
        """
        style = make_formal_logical_style()
        assert style.does_not_implement_logical_style()

    def test_style_does_not_implement_lafzi_madlul(self):
        """
        Law 11: StyleSpec does NOT implement LafziMadlul.

        This PR only declares, does not implement.
        Declaration ≠ Implementation.
        """
        style = make_lafzi_dalali_style()
        assert style.does_not_implement_lafzi_madlul()


class TestDomainDeclarations:
    """Test that domains can be declared but not executed."""

    def test_lafzi_dalali_domain_can_be_declared_but_not_executed(self):
        """
        Law 12: Lafzi/Dalali domain can be declared.

        Declaration exists, implementation does NOT.
        """
        # Can create domain spec
        domain = make_lafzi_dalali_domain()
        assert domain.domain == ThinkingDomain.LAFZI_DALALI

        # Can create style spec
        style = make_lafzi_dalali_style()
        assert style.get_domain() == ThinkingDomain.LAFZI_DALALI

        # Evidence policy exists
        assert style.evidence_policy.requires_evidence_kind(EvidenceKind.WADH)
        assert style.evidence_policy.requires_evidence_kind(EvidenceKind.ISTIMAL)

        # Operation policy declares operations
        assert style.allows_operation(OperationKind.EXTRACT_DAL)
        assert style.allows_operation(OperationKind.INFER_MADLUL)

        # But implementation does NOT exist
        # (This is verified by construction - no execute method)
        assert style.does_not_implement_lafzi_madlul()

    def test_material_experimental_domain_can_be_declared_but_not_executed(self):
        """
        Law 13: Material/Experimental domain can be declared.

        Declaration exists, ScientificMethod implementation does NOT.
        """
        # Can create domain spec
        domain = make_material_experimental_domain()
        assert domain.domain == ThinkingDomain.MATERIAL_EXPERIMENTAL

        # Can create style spec
        style = make_material_experimental_style()
        assert style.get_domain() == ThinkingDomain.MATERIAL_EXPERIMENTAL

        # Evidence policy exists
        assert style.evidence_policy.requires_evidence_kind(EvidenceKind.MEASUREMENT)
        assert style.evidence_policy.requires_evidence_kind(EvidenceKind.OBSERVATION)

        # Operation policy declares operations
        assert style.allows_operation(OperationKind.MEASURE)
        assert style.allows_operation(OperationKind.EXPERIMENT)

        # But ScientificMethod implementation does NOT exist
        assert style.does_not_implement_scientific_method()

    def test_programming_execution_domain_can_be_declared_but_not_executed(self):
        """
        Law 14: Programming/Execution domain can be declared.

        Declaration exists, execution implementation does NOT.
        """
        # Can create domain spec
        domain = make_programming_execution_domain()
        assert domain.domain == ThinkingDomain.PROGRAMMING_EXECUTION

        # Can create style spec
        style = make_programming_execution_style()
        assert style.get_domain() == ThinkingDomain.PROGRAMMING_EXECUTION

        # Evidence policy exists
        assert style.evidence_policy.requires_evidence_kind(EvidenceKind.EXECUTION)
        assert style.evidence_policy.requires_evidence_kind(EvidenceKind.TYPE_CHECK)

        # Operation policy declares operations
        assert style.allows_operation(OperationKind.EXECUTE)
        assert style.allows_operation(OperationKind.COMPILE)

        # But execution implementation is declaration only


class TestEvidencePolicy:
    """Test evidence policy constraints."""

    def test_evidence_policy_forbids_wrong_evidence(self):
        """Evidence from wrong domain is forbidden."""
        material_policy = make_material_evidence_policy()

        # Material domain forbids formal proof
        assert material_policy.forbids_evidence_kind(EvidenceKind.PROOF)
        assert material_policy.forbids_evidence_kind(EvidenceKind.AXIOM)

    def test_evidence_policy_requires_domain_evidence(self):
        """Evidence policy requires domain-specific evidence."""
        lafzi_policy = make_lafzi_evidence_policy()

        # Lafzi domain requires وضع and استعمال
        assert lafzi_policy.requires_evidence_kind(EvidenceKind.WADH)
        assert lafzi_policy.requires_evidence_kind(EvidenceKind.ISTIMAL)


class TestRankPolicy:
    """Test rank policy constraints."""

    def test_rank_policy_does_not_inflate(self):
        """Rank policy checks for non-inflation."""
        material_policy = make_material_rank_policy()

        # ZANNI → ZANNI is non-inflating
        assert material_policy.does_not_inflate(
            PredicateRank.ZANNI,
            PredicateRank.ZANNI
        )

        # CERTIFIED → ZANNI is non-inflating (demotion)
        assert material_policy.does_not_inflate(
            PredicateRank.CERTIFIED,
            PredicateRank.ZANNI
        )

        # ZANNI → CERTIFIED is inflating
        assert not material_policy.does_not_inflate(
            PredicateRank.ZANNI,
            PredicateRank.CERTIFIED
        )

    def test_rank_policy_blocks_existence_predicate_confusion(self):
        """Rank policy enforces existence ≠ predicate."""
        material_policy = make_material_rank_policy()

        assert material_policy.blocks_existence_to_predicate_confusion()


class TestStyleValidator:
    """Test style validator functionality."""

    def test_validator_accepts_complete_style_spec(self):
        """Validator accepts properly constructed StyleSpec."""
        style = make_lafzi_dalali_style()

        result = StyleValidator.validate_style_spec(style)

        assert result.success
        assert not result.has_blockers()
        assert not result.has_meta_violations()

    def test_validator_rejects_none_style_spec(self):
        """Validator rejects None StyleSpec."""
        result = StyleValidator.validate_style_spec(None)

        assert result.is_failure()
        assert result.has_blockers()
        assert "style_spec" in result.missing_components

    def test_validator_detects_domain_mismatch(self):
        """Validator detects domain mismatches."""
        material_style = make_material_experimental_style()

        result = StyleValidator.validate_domain_match(
            material_style,
            ThinkingDomain.LAFZI_DALALI  # Wrong domain!
        )

        assert result.is_failure()
        assert result.has_domain_violations()

    def test_validator_detects_forbidden_operation(self):
        """Validator detects forbidden operations."""
        style = make_material_experimental_style()

        # CREATE_MEANING is universally forbidden
        result = StyleValidator.validate_operation_allowed(
            style,
            OperationKind.CREATE_MEANING
        )

        assert result.is_failure()
        assert len(result.policy_violations) > 0


class TestAllFiveDomains:
    """Test all five declared domains."""

    def test_all_five_domains_can_be_created(self):
        """All five domains can be created."""
        domains = [
            make_material_experimental_style(),
            make_formal_logical_style(),
            make_lafzi_dalali_style(),
            make_textual_normative_style(),
            make_programming_execution_style(),
        ]

        assert len(domains) == 5

        # Each has unique domain
        domain_values = {s.get_domain() for s in domains}
        assert len(domain_values) == 5

        # All pass validation
        for style in domains:
            result = StyleValidator.validate_style_spec(style)
            assert result.success, f"{style.name_en} validation failed"
