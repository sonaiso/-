"""
Tests for NeutralBinding - العنصر المحايد في الطريقة العقلية

Critical Laws Being Tested:
1. No NeutralBinding without PriorInformation
2. PriorOpinion is excluded from binding
3. NeutralBinding preserves PriorInformation
4. NeutralBinding preserves trace_id
5. NeutralBinding preserves residuals
6. NeutralBinding does NOT raise PredicateRank
7. NeutralBinding does NOT convert ZANNI to CERTIFIED
8. NeutralBinding does NOT create meaning
9. NeutralBinding does NOT issue HUKM
10. NeutralBinding blocks domain jump without bridge
11. NeutralBinding returns governed failure, not bare exception
12. NeutralBinding does NOT implement ScientificMethod
13. NeutralBinding does NOT implement LogicalStyle
14. NeutralBinding does NOT implement LafziMadlul
"""

import pytest

from gfa.methods.rational import (
    NeutralBinding,
    NeutralBindingInput,
    NeutralBindingResult,
    NeutralBindingFailure,
    AqlOperationInput,
    PriorInformation,
    PriorOpinion,
    FilteredPrior,
    filter_prior,
    PredicateRank,
    RationalResidual,
    RationalResidualKind,
)


class TestNeutralBindingRequirements:
    """Test core requirements for NeutralBinding."""

    def test_neutral_binding_requires_prior_information(self):
        """
        Law 1: No NeutralBinding without PriorInformation.

        Without prior information, binding must fail with governed result.
        """
        # Create input without valid prior information
        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="test_reality",
                sensory_transfer="test_sensory",
                cognitive_carrier="test_carrier",
                filtered_prior=None  # Missing!
            )
        )

        result = NeutralBinding.bind(input_data)

        # Should fail
        assert result.is_failure()
        assert not result.is_success()
        assert result.failure is not None
        assert "prior_information" in result.failure.missing_requirements
        assert any(r.kind == RationalResidualKind.MISSING_PRIOR_INFORMATION for r in result.residuals)

    def test_neutral_binding_excludes_prior_opinion(self):
        """
        Law 2: PriorOpinion is excluded from binding.

        Opinions generate residuals but do not enter binding.
        """
        opinion = PriorOpinion("biased view", "bias", "high")
        info = PriorInformation("valid info", "domain", "LICENSED", "evidence")

        filtered = filter_prior(frozenset([info, opinion]))

        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="test",
                sensory_transfer="test",
                cognitive_carrier="test",
                filtered_prior=filtered
            )
        )

        result = NeutralBinding.bind(input_data)

        # Should succeed
        assert result.is_success()
        # Opinion excluded
        assert result.opinion_excluded
        # Should have residual from excluded opinion
        assert len(result.residuals) > 0
        assert any(r.kind == RationalResidualKind.PRIOR_OPINION_DETECTED for r in result.residuals)

    def test_neutral_binding_preserves_prior_information(self):
        """
        Law 3: NeutralBinding preserves PriorInformation.

        Prior information enters binding unchanged.
        """
        info1 = PriorInformation("fact1", "domain", "LICENSED", "evidence1")
        info2 = PriorInformation("fact2", "domain", "CERTIFIED", "evidence2")

        filtered = filter_prior(frozenset([info1, info2]))

        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="test",
                sensory_transfer="test",
                cognitive_carrier="test",
                filtered_prior=filtered
            )
        )

        result = NeutralBinding.bind(input_data)

        assert result.is_success()
        assert result.prior_information_preserved
        # Prior information count should be reflected in bound content
        assert "prior_info_count=2" in result.bound_content

    def test_neutral_binding_preserves_trace_id(self):
        """
        Law 4: NeutralBinding preserves trace_id.

        Trace lineage must be maintained through binding.
        """
        info = PriorInformation("test", "domain", "LICENSED", "evidence")
        filtered = filter_prior(frozenset([info]))

        custom_trace = "custom_trace_12345"
        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="test",
                sensory_transfer="test",
                cognitive_carrier="test",
                filtered_prior=filtered
            ),
            trace_id=custom_trace
        )

        result = NeutralBinding.bind(input_data)

        assert result.is_success()
        assert result.trace_id == custom_trace

    def test_neutral_binding_preserves_residuals(self):
        """
        Law 5: NeutralBinding preserves residuals.

        Input residuals must be carried through to output.
        """
        info = PriorInformation("test", "domain", "LICENSED", "evidence")
        filtered = filter_prior(frozenset([info]))

        input_residual = RationalResidual(
            kind=RationalResidualKind.TRACE_INCOMPLETE,
            description="Test residual",
            severity="low"
        )

        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="test",
                sensory_transfer="test",
                cognitive_carrier="test",
                filtered_prior=filtered
            ),
            residuals=(input_residual,)
        )

        result = NeutralBinding.bind(input_data)

        assert result.is_success()
        # Input residual should be preserved
        assert input_residual in result.residuals


class TestNeutralBindingRankPreservation:
    """Test that NeutralBinding does NOT raise PredicateRank."""

    def test_neutral_binding_does_not_raise_predicate_rank(self):
        """
        Law 6: NeutralBinding does NOT raise PredicateRank.

        Rank after binding must be <= rank before binding.
        """
        info = PriorInformation("test", "domain", "LICENSED", "evidence")
        filtered = filter_prior(frozenset([info]))

        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="test",
                sensory_transfer="test",
                cognitive_carrier="test",
                filtered_prior=filtered
            )
        )

        # Start with ZANNI rank
        result = NeutralBinding.bind(input_data, initial_rank=PredicateRank.ZANNI)

        assert result.is_success()
        assert result.predicate_rank_before == PredicateRank.ZANNI
        assert result.predicate_rank_after == PredicateRank.ZANNI
        assert result.rank_was_not_inflated()

    def test_neutral_binding_does_not_convert_zanni_to_certified(self):
        """
        Law 7: NeutralBinding does NOT convert ZANNI to CERTIFIED.

        This is the most critical rank preservation test.
        ZANNI → CERTIFIED promotion is forbidden.
        """
        info = PriorInformation("test", "domain", "LICENSED", "evidence")
        filtered = filter_prior(frozenset([info]))

        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="test",
                sensory_transfer="test",
                cognitive_carrier="test",
                filtered_prior=filtered
            )
        )

        result = NeutralBinding.bind(input_data, initial_rank=PredicateRank.ZANNI)

        assert result.is_success()
        # ZANNI must NOT become CERTIFIED
        assert result.predicate_rank_after != PredicateRank.CERTIFIED
        assert result.zanni_was_not_certified()

    def test_neutral_binding_preserves_candidate_rank(self):
        """NeutralBinding preserves CANDIDATE rank."""
        info = PriorInformation("test", "domain", "LICENSED", "evidence")
        filtered = filter_prior(frozenset([info]))

        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="test",
                sensory_transfer="test",
                cognitive_carrier="test",
                filtered_prior=filtered
            )
        )

        result = NeutralBinding.bind(input_data, initial_rank=PredicateRank.CANDIDATE)

        assert result.is_success()
        assert result.predicate_rank_after == PredicateRank.CANDIDATE
        assert result.rank_was_not_inflated()


class TestNeutralBindingBoundaries:
    """Test what NeutralBinding does NOT do."""

    def test_neutral_binding_does_not_create_meaning(self):
        """
        Law 8: NeutralBinding does NOT create meaning.

        Meaning is domain-specific.
        NeutralBinding is pre-domain.
        """
        assert NeutralBinding.does_not_create_meaning()

        # Verify bound_content is neutral description, not meaning
        info = PriorInformation("test", "domain", "LICENSED", "evidence")
        filtered = filter_prior(frozenset([info]))

        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="observed_thing",
                sensory_transfer="visual",
                cognitive_carrier="test",
                filtered_prior=filtered
            )
        )

        result = NeutralBinding.bind(input_data)

        assert result.is_success()
        # bound_content should be neutral description
        assert "neutral_binding" in result.bound_content
        # Should NOT contain meaning claims
        assert "meaning=" not in result.bound_content
        assert "interpretation=" not in result.bound_content

    def test_neutral_binding_does_not_issue_hukm(self):
        """
        Law 9: NeutralBinding does NOT issue HUKM.

        Hukm (judgment) requires domain interpretation.
        NeutralBinding is pre-interpretation.
        """
        assert NeutralBinding.does_not_issue_hukm()

    def test_neutral_binding_blocks_domain_jump_without_bridge(self):
        """
        Law 10: NeutralBinding blocks domain jump without bridge.

        Cannot jump from pre-domain to domain-specific without StyleSpec.
        This is tested by verifying NeutralBinding does not implement domains.
        """
        # NeutralBinding cannot implement domain-specific methods
        assert NeutralBinding.does_not_implement_lafzi_madlul()
        assert NeutralBinding.does_not_implement_domain_spec()
        assert NeutralBinding.does_not_implement_style_spec()

    def test_neutral_binding_returns_governed_failure_not_exception(self):
        """
        Law 11: NeutralBinding returns governed failure, not bare exception.

        Even complete failure returns NeutralBindingResult with failure info.
        """
        # Missing AqlOperationInput entirely
        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality=None,
                sensory_transfer=None,
                cognitive_carrier=None,
                filtered_prior=None
            )
        )

        # Should NOT raise exception
        result = NeutralBinding.bind(input_data)

        # Should return governed result
        assert isinstance(result, NeutralBindingResult)
        assert result.is_failure()
        assert isinstance(result.failure, NeutralBindingFailure)
        assert result.failure.reason is not None


class TestNeutralBindingArchitectureBoundaries:
    """Test that NeutralBinding does NOT implement future components."""

    def test_neutral_binding_does_not_implement_scientific_method(self):
        """
        Law 12: NeutralBinding does NOT implement ScientificMethod.

        ScientificMethod is future experimental branch.
        """
        assert NeutralBinding.does_not_implement_scientific_method()

    def test_neutral_binding_does_not_implement_logical_style(self):
        """
        Law 13: NeutralBinding does NOT implement LogicalStyle.

        LogicalStyle is future formal style.
        """
        assert NeutralBinding.does_not_implement_logical_style()

    def test_neutral_binding_does_not_implement_lafzi_madlul(self):
        """
        Law 14: NeutralBinding does NOT implement LafziMadlul.

        LafziMadlul is future linguistic domain.
        It must be built on top of NeutralBinding, not inside it.
        """
        assert NeutralBinding.does_not_implement_lafzi_madlul()

    def test_neutral_binding_does_not_implement_domain_spec(self):
        """NeutralBinding does NOT implement DomainSpec."""
        assert NeutralBinding.does_not_implement_domain_spec()

    def test_neutral_binding_does_not_implement_style_spec(self):
        """NeutralBinding does NOT implement StyleSpec."""
        assert NeutralBinding.does_not_implement_style_spec()


class TestNeutralBindingIntegration:
    """Integration tests for NeutralBinding."""

    def test_neutral_binding_full_success_path(self):
        """Test complete successful binding with all components."""
        info1 = PriorInformation("fact1", "domain", "LICENSED", "evidence1")
        info2 = PriorInformation("fact2", "domain", "CERTIFIED", "evidence2")
        opinion = PriorOpinion("bias", "assumption", "medium")

        filtered = filter_prior(frozenset([info1, info2, opinion]))

        custom_residual = RationalResidual(
            kind=RationalResidualKind.TRACE_INCOMPLETE,
            description="Custom residual",
            severity="low"
        )

        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="observed_reality",
                sensory_transfer="visual_audio",
                cognitive_carrier="active_carrier",
                filtered_prior=filtered
            ),
            trace_id="integration_test_trace",
            residuals=(custom_residual,)
        )

        result = NeutralBinding.bind(input_data, initial_rank=PredicateRank.ZANNI)

        # Verify all success conditions
        assert result.is_success()
        assert result.prior_information_preserved
        assert result.opinion_excluded
        assert result.trace_id == "integration_test_trace"
        assert result.predicate_rank_before == PredicateRank.ZANNI
        assert result.predicate_rank_after == PredicateRank.ZANNI
        assert result.rank_was_not_inflated()
        assert result.zanni_was_not_certified()
        assert custom_residual in result.residuals
        assert any(r.kind == RationalResidualKind.PRIOR_OPINION_DETECTED for r in result.residuals)
        assert result.bound_content is not None
        assert "neutral_binding" in result.bound_content

    def test_neutral_binding_failure_path_preserves_trace(self):
        """Test that even failures preserve trace and residuals."""
        input_data = NeutralBindingInput(
            aql_input=AqlOperationInput(
                reality="test",
                sensory_transfer="test",
                cognitive_carrier="test",
                filtered_prior=None  # Will fail
            ),
            trace_id="failure_test_trace"
        )

        result = NeutralBinding.bind(input_data)

        # Verify failure is governed
        assert result.is_failure()
        assert result.failure is not None
        # Trace preserved even in failure
        assert result.trace_id == "failure_test_trace"
        assert result.failure.trace_id == "failure_test_trace"
        # Residuals present
        assert len(result.residuals) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
