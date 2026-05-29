"""Test FactorMarkEquation.

Tests verify factor/mark candidate equations WITHOUT case_effect production.
"""

import pytest
from unittest.mock import Mock

from dal_core.factor_mark_equation import (
    FactorMarkEquationType,
    FactorMarkEquation,
    build_factor_mark_equation,
)
from dal_core.case_signs import CaseSignPotential, CaseSignFamily, CaseSignValue
from dal_core.transition_proof_kernel import TransitionDecision


# ============================================================================
# Helper: Build Mock PreSyntaxMufradVector
# ============================================================================

def build_mock_presyntax_vector(
    *,
    trace_id: str = "trace:test",
    allows_consumption: bool = True,
    final_rank: str = "CANDIDATE",
    residuals: tuple = (),
) -> Mock:
    """Build mock PreSyntaxMufradVector for testing."""
    vector = Mock()
    vector.trace_id = trace_id
    vector.allows_operator_consumption = Mock(return_value=allows_consumption)
    vector.residuals = residuals

    # Final rank
    rank = Mock()
    rank.name = final_rank
    vector.final_rank = rank

    return vector


# ============================================================================
# Helper: Build Mock CaseSignPotential
# ============================================================================

def build_mock_case_sign_potential(
    *,
    family: CaseSignFamily = CaseSignFamily.ORIGINAL,
    value: CaseSignValue = CaseSignValue.DAMMA,
) -> CaseSignPotential:
    """Build mock CaseSignPotential."""
    return CaseSignPotential(
        family=family,
        value=value,
        confidence=0.9,
        source="test",
        observation_id="obs:test",
    )


# ============================================================================
# FactorMarkEquationType Tests
# ============================================================================

def test_factor_mark_equation_type_values():
    """Test all equation type enum values exist."""
    assert FactorMarkEquationType.RAFʿ_CANDIDATE.value == "raf_candidate"
    assert FactorMarkEquationType.NASB_CANDIDATE.value == "nasb_candidate"
    assert FactorMarkEquationType.JARR_CANDIDATE.value == "jarr_candidate"
    assert FactorMarkEquationType.JAZM_CANDIDATE.value == "jazm_candidate"
    assert FactorMarkEquationType.DEFERRED.value == "deferred"


# ============================================================================
# FactorMarkEquation Structure Tests
# ============================================================================

def test_factor_mark_equation_structure():
    """Test basic FactorMarkEquation structure."""
    vector = build_mock_presyntax_vector()
    mark = build_mock_case_sign_potential()

    equation = FactorMarkEquation(
        equation_id="factor_mark:test_001",
        factor_trace_id="trace:factor",
        affected_trace_id="trace:affected",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
        transition_proof=Mock(),
    )

    assert equation.equation_id == "factor_mark:test_001"
    assert equation.factor_trace_id == "trace:factor"
    assert equation.equation_type == FactorMarkEquationType.RAFʿ_CANDIDATE


def test_factor_mark_equation_constitutional_prohibitions():
    """Test that FactorMarkEquation enforces constitutional prohibitions."""
    vector = build_mock_presyntax_vector()

    equation = FactorMarkEquation(
        equation_id="factor_mark:test",
        factor_trace_id="trace:factor",
        affected_trace_id="trace:affected",
        affected_vector=vector,
        mark_potential=None,
        equation_type=FactorMarkEquationType.DEFERRED,
        transition_proof=Mock(),
    )

    # Default values enforce prohibitions
    assert not equation.produces_case_effect
    assert not equation.produces_meaning
    assert not equation.produces_ifadah
    assert not equation.produces_hukm


# ============================================================================
# build_factor_mark_equation Tests
# ============================================================================

def test_build_factor_mark_equation_basic():
    """Test basic factor-mark equation building."""
    vector = build_mock_presyntax_vector(trace_id="trace:affected_123")
    mark = build_mock_case_sign_potential(family=CaseSignFamily.ORIGINAL)

    equation = build_factor_mark_equation(
        factor_trace_id="trace:operator_456",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    assert equation.equation_id == "factor_mark:trace:operator_456:trace:affected_123"
    assert equation.factor_trace_id == "trace:operator_456"
    assert equation.affected_trace_id == "trace:affected_123"
    assert equation.equation_type == FactorMarkEquationType.RAFʿ_CANDIDATE
    assert equation.mark_potential == mark


def test_build_factor_mark_equation_deferred_when_mark_missing():
    """Test that equation is DEFERRED when mark_potential is None."""
    vector = build_mock_presyntax_vector()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=None,  # Missing mark
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    # Should override to DEFERRED
    assert equation.equation_type == FactorMarkEquationType.DEFERRED


def test_build_factor_mark_equation_verifies_readiness():
    """Test that equation building verifies vector readiness."""
    vector = build_mock_presyntax_vector(allows_consumption=False)
    mark = build_mock_case_sign_potential()

    # Should raise error if vector not ready
    with pytest.raises(ValueError, match="not ready"):
        build_factor_mark_equation(
            factor_trace_id="trace:factor",
            affected_vector=vector,
            mark_potential=mark,
            equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
        )


def test_build_factor_mark_equation_preserves_traces():
    """Test that factor and affected traces are preserved."""
    vector = build_mock_presyntax_vector(trace_id="trace:affected")
    mark = build_mock_case_sign_potential()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.NASB_CANDIDATE,
    )

    # Verify traces preserved in transition proof
    assert "trace:factor" in equation.transition_proof.preserved_trace_ids
    assert "trace:affected" in equation.transition_proof.preserved_trace_ids


def test_build_factor_mark_equation_constitutional_prohibitions():
    """Test that no forbidden outputs are produced."""
    vector = build_mock_presyntax_vector()
    mark = build_mock_case_sign_potential()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    # Verify constitutional prohibitions
    assert not equation.produces_case_effect
    assert not equation.produces_meaning
    assert not equation.produces_ifadah
    assert not equation.produces_hukm


# ============================================================================
# TransitionProof Tests
# ============================================================================

def test_build_factor_mark_equation_transition_proof_complete():
    """Test that complete transition proof is built."""
    vector = build_mock_presyntax_vector()
    mark = build_mock_case_sign_potential()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    # Verify all transition proof components
    proof = equation.transition_proof
    assert proof.qiyas is not None
    assert proof.identity_neutral is not None
    assert proof.minimal_completeness is not None

    # Verify layers
    assert proof.source_layer == "PRESYNTAX_MUFRAD_VECTOR"
    assert proof.target_layer == "FACTOR_MARK_EQUATION"


def test_build_factor_mark_equation_accepted_when_mark_present():
    """Test that equation is ACCEPTED when all conditions met."""
    vector = build_mock_presyntax_vector()
    mark = build_mock_case_sign_potential()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    # Should be accepted (all conditions satisfied)
    assert equation.transition_proof.decision == TransitionDecision.ACCEPTED


def test_build_factor_mark_equation_deferred_when_mark_missing_in_transition():
    """Test that transition is DEFERRED when mark missing."""
    vector = build_mock_presyntax_vector()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=None,  # Missing
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    # Should be deferred (missing condition)
    assert equation.transition_proof.decision == TransitionDecision.DEFERRED


# ============================================================================
# QiyasProof Tests
# ============================================================================

def test_build_factor_mark_equation_qiyas_components():
    """Test that qiyas proof has all required components."""
    vector = build_mock_presyntax_vector(trace_id="trace:affected")
    mark = build_mock_case_sign_potential()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    qiyas = equation.transition_proof.qiyas

    # Verify qiyas structure
    assert qiyas.origin_id.startswith("origin:")
    assert qiyas.branch_id == "trace:affected"
    assert qiyas.effective_description is not None
    assert qiyas.shared_cause


def test_build_factor_mark_equation_qiyas_accepted():
    """Test that qiyas is accepted when no blocking differences."""
    vector = build_mock_presyntax_vector()
    mark = build_mock_case_sign_potential()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    # Qiyas should be accepted
    assert equation.transition_proof.qiyas.accepted
    assert not equation.transition_proof.qiyas.has_blocking_difference


# ============================================================================
# Identity Preservation Tests
# ============================================================================

def test_build_factor_mark_equation_preserves_identities():
    """Test that identities are preserved in transition."""
    vector = build_mock_presyntax_vector(trace_id="trace:affected")
    mark = build_mock_case_sign_potential()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    neutral = equation.transition_proof.identity_neutral

    # Input and output identities should match (preserved)
    assert neutral.preserved
    assert "trace:factor" in neutral.input_identity_ids
    assert "trace:affected" in neutral.input_identity_ids
    assert "trace:factor" in neutral.output_identity_ids
    assert "trace:affected" in neutral.output_identity_ids


# ============================================================================
# Minimal Completeness Tests
# ============================================================================

def test_build_factor_mark_equation_minimal_completeness_satisfied():
    """Test minimal completeness when all conditions satisfied."""
    vector = build_mock_presyntax_vector()
    mark = build_mock_case_sign_potential()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    minimum = equation.transition_proof.minimal_completeness

    # All required conditions should be satisfied
    assert minimum.passed
    assert len(minimum.missing_conditions) == 0
    assert "no_case_effect" in minimum.satisfied_conditions
    assert "no_meaning" in minimum.satisfied_conditions
    assert "no_ifadah" in minimum.satisfied_conditions
    assert "no_hukm" in minimum.satisfied_conditions


def test_build_factor_mark_equation_minimal_completeness_missing_mark():
    """Test minimal completeness when mark_potential missing."""
    vector = build_mock_presyntax_vector()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=None,  # Missing
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    minimum = equation.transition_proof.minimal_completeness

    # Should not pass (missing mark_potential)
    assert not minimum.passed
    assert "mark_potential_missing" in minimum.missing_conditions


# ============================================================================
# Residual Handling Tests
# ============================================================================

def test_build_factor_mark_equation_includes_residuals():
    """Test that residuals are included in transition proof."""
    residual1 = Mock()
    residual1.__str__ = Mock(return_value="residual:1")
    residual2 = Mock()
    residual2.__str__ = Mock(return_value="residual:2")

    vector = build_mock_presyntax_vector(residuals=(residual1, residual2))
    mark = build_mock_case_sign_potential()

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    # Should include residuals in transition proof
    assert "residual:1" in equation.transition_proof.residual_ids
    assert "residual:2" in equation.transition_proof.residual_ids


# ============================================================================
# Equation Type Tests
# ============================================================================

def test_build_factor_mark_equation_raf_candidate():
    """Test building RAF' candidate equation."""
    vector = build_mock_presyntax_vector()
    mark = build_mock_case_sign_potential(family=CaseSignFamily.RAF)

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )

    assert equation.equation_type == FactorMarkEquationType.RAFʿ_CANDIDATE


def test_build_factor_mark_equation_nasb_candidate():
    """Test building NASB candidate equation."""
    vector = build_mock_presyntax_vector()
    mark = build_mock_case_sign_potential(family=CaseSignFamily.ORIGINAL)

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.NASB_CANDIDATE,
    )

    assert equation.equation_type == FactorMarkEquationType.NASB_CANDIDATE


def test_build_factor_mark_equation_jarr_candidate():
    """Test building JARR candidate equation."""
    vector = build_mock_presyntax_vector()
    mark = build_mock_case_sign_potential(family=CaseSignFamily.ORIGINAL)

    equation = build_factor_mark_equation(
        factor_trace_id="trace:factor",
        affected_vector=vector,
        mark_potential=mark,
        equation_type=FactorMarkEquationType.JARR_CANDIDATE,
    )

    assert equation.equation_type == FactorMarkEquationType.JARR_CANDIDATE
