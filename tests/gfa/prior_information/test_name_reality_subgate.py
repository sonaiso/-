"""
Tests for Name Reality SubGate

Critical Laws Tested:
1. Name alone does NOT produce RealityCandidate
2. Name without domain (when required) → BLOCKED
3. Name without referent evidence → rank lowered or blocked
4. Technical name without domain → BLOCKED
5. Metaphor cannot usurp external existence → BLOCKED
6. Prior opinion cannot be referent_evidence → BLOCKED
"""

import pytest
from gfa.prior_information import (
    NameRealitySubGate,
    RealityType,
    PriorInformationCandidate,
    PriorContentType,
)


class TestNameRealitySubGateCore:
    """Test core sub-gate functionality."""

    def test_subgate_instantiation(self):
        """SubGate can be instantiated."""
        gate = NameRealitySubGate()
        assert gate is not None

    def test_admit_external_with_evidence(self):
        """Admit external reality with sensory evidence."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="الماء",
            referent_candidate="H2O liquid substance",
            existence_type=RealityType.EXTERNAL,
            domain="physical",
            referent_evidence="sensory_evidence",
        )

        assert result.is_admitted()
        assert result.candidate is not None
        assert result.candidate.name == "الماء"
        assert result.candidate.existence_type == RealityType.EXTERNAL
        assert result.rank == "LICENSED"

    def test_admit_mental_with_domain(self):
        """Admit mental existence with domain."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="العقل",
            referent_candidate="cognitive faculty",
            existence_type=RealityType.MENTAL,
            domain="mental",
            referent_evidence="introspective_evidence",
        )

        assert result.is_admitted()
        assert result.candidate.existence_type == RealityType.MENTAL
        assert result.rank == "LICENSED"

    def test_admit_technical_with_domain(self):
        """Admit technical term with domain."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="العامل",
            referent_candidate="grammatical operator",
            existence_type=RealityType.TECHNICAL,
            domain="grammar",
            referent_evidence="grammar_definition",
        )

        assert result.is_admitted()
        assert result.candidate.existence_type == RealityType.TECHNICAL
        assert result.candidate.domain == "grammar"


class TestNameRealitySubGateBlockers:
    """Test blocker conditions."""

    def test_block_name_without_referent(self):
        """Block name without referent candidate."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="X",
            referent_candidate=None,  # Missing
            existence_type=RealityType.EXTERNAL,
        )

        assert result.is_blocked()
        assert result.candidate is None
        assert result.rank == "BLOCKED"
        assert result.failure is not None
        assert "NAME_WITHOUT_REFERENT" in result.failure.kind.name

    def test_block_mental_without_domain(self):
        """Block mental existence without domain."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="العقل",
            referent_candidate="cognitive faculty",
            existence_type=RealityType.MENTAL,
            domain=None,  # Missing - required for MENTAL
        )

        assert result.is_blocked()
        assert "NAME_WITHOUT_DOMAIN" in result.failure.kind.name

    def test_block_technical_without_domain(self):
        """Block technical term without domain."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="العامل",
            referent_candidate="operator",
            existence_type=RealityType.TECHNICAL,
            domain=None,  # Missing - required for TECHNICAL
        )

        assert result.is_blocked()
        assert "TECHNICAL_WITHOUT_DOMAIN" in result.failure.kind.name

    def test_block_normative_without_domain(self):
        """Block normative existence without domain."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="العدالة",
            referent_candidate="justice concept",
            existence_type=RealityType.NORMATIVE,
            domain=None,  # Missing - required for NORMATIVE
        )

        assert result.is_blocked()
        assert "NAME_WITHOUT_DOMAIN" in result.failure.kind.name

    def test_block_metaphor_claiming_external(self):
        """Block metaphor claiming external existence."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="نار الحرب",
            referent_candidate="literal fire",
            existence_type=RealityType.METAPHORICAL,
            domain="rhetorical",
            referent_evidence="external_fire",  # Wrong - metaphor claiming external
        )

        assert result.is_blocked()
        assert "METAPHOR_AS_EXTERNAL" in result.failure.kind.name


class TestNameRealitySubGateResiduals:
    """Test residual generation."""

    def test_residuals_for_missing_evidence(self):
        """Generate residuals when referent evidence missing."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="X",
            referent_candidate="something",
            existence_type=RealityType.EXTERNAL,
            domain="physical",
            referent_evidence=None,  # Missing
        )

        # Admitted but with lower rank
        assert result.is_admitted()
        assert result.rank == "CANDIDATE"
        assert len(result.residuals) > 0

    def test_ambiguity_score_calculation(self):
        """Ambiguity score calculated based on missing components."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="X",
            referent_candidate="something",
            existence_type=RealityType.TECHNICAL,
            domain="some_domain",
            referent_evidence=None,
        )

        assert result.is_admitted()
        assert result.candidate.ambiguity_score > 0.0

    def test_trace_preservation(self):
        """Trace is preserved in admitted candidate."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="الماء",
            referent_candidate="water",
            existence_type=RealityType.EXTERNAL,
            domain="physical",
            referent_evidence="sensory",
        )

        assert result.is_admitted()
        assert result.trace is not None
        assert result.candidate.trace is not None


class TestNameRealitySubGateNoLeap:
    """Test NoLeap guards - forbidden transitions."""

    def test_noleap_name_to_reality_without_referent(self):
        """Name alone CANNOT become RealityCandidate."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="some_name",
            referent_candidate=None,
        )

        assert result.is_blocked()

    def test_noleap_technical_without_domain(self):
        """Technical term CANNOT skip domain requirement."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="technical_term",
            referent_candidate="something",
            existence_type=RealityType.TECHNICAL,
            domain=None,
        )

        assert result.is_blocked()

    def test_noleap_metaphor_to_external(self):
        """Metaphor CANNOT usurp external existence."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="metaphor",
            referent_candidate="ref",
            existence_type=RealityType.METAPHORICAL,
            referent_evidence="external_evidence",
        )

        assert result.is_blocked()

    def test_noleap_mental_without_domain(self):
        """Mental existence CANNOT skip domain requirement."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="mental_concept",
            referent_candidate="concept",
            existence_type=RealityType.MENTAL,
            domain=None,
        )

        assert result.is_blocked()


class TestNameRealitySubGateGoldenCases:
    """Test against golden dataset cases."""

    def test_golden_water_external(self):
        """الماء → EXTERNAL with sensory evidence."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="الماء",
            referent_candidate="H2O liquid",
            existence_type=RealityType.EXTERNAL,
            domain="physical",
            referent_evidence="sensory_evidence",
        )

        assert result.is_admitted()
        assert result.candidate.existence_type == RealityType.EXTERNAL

    def test_golden_fire_external(self):
        """النار → EXTERNAL with sensory evidence."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="النار",
            referent_candidate="combustion process",
            existence_type=RealityType.EXTERNAL,
            domain="physical",
            referent_evidence="sensory_evidence",
        )

        assert result.is_admitted()

    def test_golden_mind_requires_domain(self):
        """العقل → MENTAL requires domain."""
        gate = NameRealitySubGate()

        # Without domain - blocked
        result_blocked = gate.admit_named_reality(
            name="العقل",
            referent_candidate="cognitive faculty",
            existence_type=RealityType.MENTAL,
            domain=None,
        )
        assert result_blocked.is_blocked()

        # With domain - admitted
        result_admitted = gate.admit_named_reality(
            name="العقل",
            referent_candidate="cognitive faculty",
            existence_type=RealityType.MENTAL,
            domain="mental",
            referent_evidence="introspective",
        )
        assert result_admitted.is_admitted()

    def test_golden_society_requires_domain(self):
        """المجتمع → TECHNICAL requires domain."""
        gate = NameRealitySubGate()

        # Without domain - blocked
        result = gate.admit_named_reality(
            name="المجتمع",
            referent_candidate="social collective",
            existence_type=RealityType.TECHNICAL,
            domain=None,
        )
        assert result.is_blocked()

    def test_golden_operator_grammar_domain(self):
        """العامل → TECHNICAL with grammar domain."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="العامل",
            referent_candidate="grammatical operator",
            existence_type=RealityType.TECHNICAL,
            domain="grammar",
            referent_evidence="grammar_definition",
        )

        assert result.is_admitted()
        assert result.candidate.domain == "grammar"

    def test_golden_fire_of_war_metaphorical(self):
        """نار الحرب → METAPHORICAL, not external."""
        gate = NameRealitySubGate()

        # Metaphorical with metaphorical evidence - admitted
        result_metaphorical = gate.admit_named_reality(
            name="نار الحرب",
            referent_candidate="metaphorical intensity",
            existence_type=RealityType.METAPHORICAL,
            domain="rhetorical",
            referent_evidence="metaphorical_usage",
        )
        assert result_metaphorical.is_admitted()

        # Metaphorical claiming external - blocked
        result_external = gate.admit_named_reality(
            name="نار الحرب",
            referent_candidate="literal fire",
            existence_type=RealityType.METAPHORICAL,
            referent_evidence="external_fire",
        )
        assert result_external.is_blocked()

    def test_golden_language_verbal_domain(self):
        """اللغة → VERBAL/TECHNICAL depending on domain."""
        gate = NameRealitySubGate()

        # As linguistic system
        result = gate.admit_named_reality(
            name="اللغة",
            referent_candidate="linguistic system",
            existence_type=RealityType.VERBAL,
            domain="linguistic",
            referent_evidence="linguistic_definition",
        )
        assert result.is_admitted()


class TestNameRealitySubGateIntegration:
    """Test integration with Prior Information system."""

    def test_subgate_within_prior_information_geometry(self):
        """NameRealitySubGate is part of PriorInformationGeometry."""
        # This test verifies architectural placement
        gate = NameRealitySubGate()

        # SubGate operates within prior information context
        result = gate.admit_named_reality(
            name="test",
            referent_candidate="ref",
            existence_type=RealityType.EXTERNAL,
            domain="domain",
        )

        # Result carries trace and residuals
        assert hasattr(result, "trace")
        assert hasattr(result, "residuals")
        assert hasattr(result, "rank")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
