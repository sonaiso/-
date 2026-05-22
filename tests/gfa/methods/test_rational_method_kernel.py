"""
Tests for Nabhani RationalMethod Kernel

Critical Laws Being Tested:
1. No rational operation without reality
2. No rational operation without sensory transfer
3. No rational operation without cognitive carrier
4. No rational operation without prior information
5. Prior opinion is excluded
6. Prior opinion cannot be used as information
7. Rational method returns governed results (not exceptions)
8. Existence rank does not promote predicate rank
9. RationalMethod does NOT implement ScientificMethod
10. RationalMethod does NOT implement LogicalStyle
11. RationalMethod does NOT implement MeansAlgebra
"""

import pytest

from gfa.methods.rational import (
    RationalMethod,
    PriorInformation,
    PriorOpinion,
    FilteredPrior,
    filter_prior,
    AqlOperation,
    AqlOperationInput,
    ExistenceRank,
    PredicateRank,
    RationalResidual,
    RationalResidualKind,
)


class TestPriorFilter:
    """Test prior information vs opinion filtering."""

    def test_prior_opinion_is_excluded(self):
        """Prior opinion must be excluded from rational operation."""
        opinion = PriorOpinion(
            content="predetermined conclusion",
            opinion_type="bias",
            contamination_risk="imposes_result"
        )

        filtered = filter_prior(frozenset([opinion]))

        assert filtered.count_excluded() == 1
        assert len(filtered.information) == 0
        assert opinion in filtered.excluded_opinions

    def test_prior_opinion_cannot_be_used_as_information(self):
        """Prior opinion must not enter as information."""
        opinion = PriorOpinion(
            content="biased assumption",
            opinion_type="assumption",
            contamination_risk="high"
        )

        filtered = filter_prior(frozenset([opinion]))

        # Opinion is excluded, not converted to information
        assert not filtered.has_valid_information()
        assert filtered.count_excluded() == 1

    def test_valid_prior_information_passes_filter(self):
        """Valid prior information passes through filter."""
        info = PriorInformation(
            content="validated fact",
            domain="test_domain",
            rank="LICENSED",
            evidence_trace="test_evidence"
        )

        filtered = filter_prior(frozenset([info]))

        assert filtered.has_valid_information()
        assert len(filtered.information) == 1
        assert info in filtered.information
        assert filtered.count_excluded() == 0

    def test_invalid_prior_information_becomes_opinion(self):
        """Invalid prior information (insufficient rank) is excluded."""
        invalid_info = PriorInformation(
            content="unvalidated claim",
            domain="test",
            rank="UNRESOLVED",  # Not LICENSED or CERTIFIED
            evidence_trace="none"
        )

        filtered = filter_prior(frozenset([invalid_info]))

        # Invalid information excluded like opinion
        assert not filtered.has_valid_information()
        assert filtered.count_excluded() == 1


class TestAqlOperationPillars:
    """Test four-pillar requirement for rational operations."""

    def test_no_aql_operation_without_reality(self):
        """Rational operation fails without reality."""
        input_data = AqlOperationInput(
            reality=None,  # Missing!
            sensory_transfer="test_sensory",
            cognitive_carrier="test_carrier",
            filtered_prior=FilteredPrior(
                information=frozenset([
                    PriorInformation("test", "domain", "LICENSED", "evidence")
                ]),
                excluded_opinions=frozenset()
            )
        )

        result = AqlOperation.execute(input_data)

        assert result.is_failure()
        assert "reality" in result.failure.missing_pillars
        assert any(r.kind == RationalResidualKind.MISSING_REALITY for r in result.residuals)

    def test_no_aql_operation_without_sensory_transfer(self):
        """Rational operation fails without sensory transfer."""
        input_data = AqlOperationInput(
            reality="test_reality",
            sensory_transfer=None,  # Missing!
            cognitive_carrier="test_carrier",
            filtered_prior=FilteredPrior(
                information=frozenset([
                    PriorInformation("test", "domain", "LICENSED", "evidence")
                ]),
                excluded_opinions=frozenset()
            )
        )

        result = AqlOperation.execute(input_data)

        assert result.is_failure()
        assert "sensory_transfer" in result.failure.missing_pillars

    def test_no_aql_operation_without_cognitive_carrier(self):
        """Rational operation fails without cognitive carrier."""
        input_data = AqlOperationInput(
            reality="test_reality",
            sensory_transfer="test_sensory",
            cognitive_carrier=None,  # Missing!
            filtered_prior=FilteredPrior(
                information=frozenset([
                    PriorInformation("test", "domain", "LICENSED", "evidence")
                ]),
                excluded_opinions=frozenset()
            )
        )

        result = AqlOperation.execute(input_data)

        assert result.is_failure()
        assert "cognitive_carrier" in result.failure.missing_pillars

    def test_no_aql_operation_without_prior_information(self):
        """Rational operation fails without prior information."""
        input_data = AqlOperationInput(
            reality="test_reality",
            sensory_transfer="test_sensory",
            cognitive_carrier="test_carrier",
            filtered_prior=None  # Missing!
        )

        result = AqlOperation.execute(input_data)

        assert result.is_failure()
        assert "prior_information" in result.failure.missing_pillars

    def test_aql_operation_succeeds_with_all_pillars(self):
        """Rational operation succeeds when all four pillars present."""
        input_data = AqlOperationInput(
            reality="test_reality",
            sensory_transfer="test_sensory",
            cognitive_carrier="test_carrier",
            filtered_prior=FilteredPrior(
                information=frozenset([
                    PriorInformation("valid info", "domain", "LICENSED", "evidence")
                ]),
                excluded_opinions=frozenset()
            )
        )

        result = AqlOperation.execute(input_data)

        assert result.is_success()
        assert result.judgment is not None
        assert result.failure is None


class TestGovernedResults:
    """Test that failures return governed objects, not bare exceptions."""

    def test_rational_method_returns_governed_result_not_exception(self):
        """Failures return AqlOperationResult, never bare exception."""
        # Missing all pillars - should return governed failure
        result = RationalMethod.judge(
            reality="",  # Empty/invalid
            sensory_transfer="",
            cognitive_carrier="",
            prior_knowledge=frozenset()
        )

        # Should be AqlOperationResult, not exception
        assert result is not None
        assert hasattr(result, 'success')
        assert hasattr(result, 'failure')
        assert result.is_failure()

    def test_aql_judgment_preserves_trace(self):
        """Judgments preserve trace_id."""
        input_data = AqlOperationInput(
            reality="test",
            sensory_transfer="test",
            cognitive_carrier="test",
            filtered_prior=FilteredPrior(
                information=frozenset([
                    PriorInformation("info", "domain", "LICENSED", "evidence")
                ]),
                excluded_opinions=frozenset()
            )
        )

        result = AqlOperation.execute(input_data)

        assert result.judgment.trace_id is not None
        assert len(result.judgment.trace_id) > 0

    def test_aql_judgment_preserves_residuals(self):
        """Judgments preserve residuals from excluded opinions."""
        opinion = PriorOpinion("bias", "assumption", "high_risk")
        info = PriorInformation("valid", "domain", "LICENSED", "evidence")

        result = RationalMethod.judge(
            reality="test",
            sensory_transfer="test",
            cognitive_carrier="test",
            prior_knowledge=frozenset([info, opinion])
        )

        assert result.is_success()
        # Should have residuals from excluded opinion
        assert len(result.judgment.residuals) > 0


class TestExistencePredicateRanks:
    """Test dual rank system (existence vs predicate)."""

    def test_existence_rank_does_not_promote_predicate_rank(self):
        """
        Nabhani Law: رأيت شيئاً ≠ عرفت حقيقته
        Seeing a thing ≠ Knowing its reality

        Existence may be QATI, but predicate remains ZANNI.
        """
        input_data = AqlOperationInput(
            reality="observed_thing",
            sensory_transfer="direct_observation",  # Should give QATI existence
            cognitive_carrier="test",
            filtered_prior=FilteredPrior(
                information=frozenset([
                    PriorInformation("some info", "domain", "LICENSED", "evidence")
                ]),
                excluded_opinions=frozenset()
            )
        )

        result = AqlOperation.execute(input_data)

        assert result.is_success()
        # Existence can be QATI
        assert result.judgment.existence_rank == ExistenceRank.QATI_EXISTENCE
        # But predicate should not auto-certify
        assert result.judgment.predicate_rank != PredicateRank.CERTIFIED
        # Should be ZANNI or CANDIDATE
        assert result.judgment.predicate_rank in (PredicateRank.ZANNI, PredicateRank.CANDIDATE)


class TestRationalMethodBoundaries:
    """Test that RationalMethod does NOT implement future branches."""

    def test_rational_method_does_not_implement_scientific_method(self):
        """RationalMethod does NOT implement ScientificMethod."""
        assert RationalMethod.does_not_implement_scientific_method()

    def test_rational_method_does_not_implement_logical_style(self):
        """RationalMethod does NOT implement LogicalStyle."""
        assert RationalMethod.does_not_implement_logical_style()

    def test_rational_method_does_not_implement_means_algebra(self):
        """RationalMethod does NOT implement MeansAlgebra."""
        assert RationalMethod.does_not_implement_means_algebra()

    def test_rational_method_is_root(self):
        """RationalMethod is the root method."""
        assert RationalMethod.is_root_method()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
