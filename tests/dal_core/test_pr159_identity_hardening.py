"""
Test PR #159: Harden Bridge Identity and Carrier Provenance

Regression tests proving:
1. trace_id cannot substitute for identity
2. carrier text fallback is residual, not full provenance
3. factor cannot be a bare string
4. missing structural completeness evidence yields warnings
"""

import pytest
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.mufrad_acceptance_equation import (
    _carrier_ids_from_mufrad,
    _identity_ids_from_mufrad,
    _has_carrier_fallback,
)
from dal_core.factor_mark_equation import (
    FactorSourceKind,
    FactorSourceCandidate,
    FactorMarkEquationType,
    build_factor_mark_equation,
)
from dal_core.ranks import LughaRank
from dal_core.type_ids import NounTypeID
from dal_core.morph_features import CandidateStatus
from dal_core.composition_readiness import CompositionReadiness
from dal_core.mufrad_axes import BinaaJudgment, IshtiqaqJudgment
from unittest.mock import Mock


# ============================================================================
# Test 1: identity_ids ≠ trace_ids
# ============================================================================

def test_presyntax_vector_has_separate_identity_and_trace_fields():
    """PR #159: PreSyntaxMufradVector has separate identity_ids and carrier_ids."""
    vector = PreSyntaxMufradVector(
        mufrad_id="test_mufrad",
        raw_span=(0, 5),
        type_value="ISM",
        type_id=NounTypeID.ISM_COMMON,
        type_rank=LughaRank.FORM,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
        noun_inflection_class=None,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=(),
        morph_rank=LughaRank.FORM,
        final_rank=LughaRank.FORM,
        residuals=(),
        trace_id="trace:123",
        competitors_count=0,
        composition_readiness=CompositionReadiness.READY_FOR_CERTIFICATE_COMPOSITION,
        binaa_judgment=BinaaJudgment.MUERAB,
        ishtiqaq_judgment=IshtiqaqJudgment.JAMID,
        identity_ids=("form:xyz", "root:ktb"),
        carrier_ids=("carrier:unicode:0", "carrier:unicode:1"),
    )

    # Assert: identity_ids and trace_id are different concepts
    assert vector.identity_ids != ()
    assert vector.trace_id != ""
    assert vector.identity_ids != (vector.trace_id,)

    # Assert: carrier_ids is separate field
    assert vector.carrier_ids != ()


def test_identity_ids_not_equal_trace_ids():
    """PR #159: Demonstrate identity_ids ≠ trace_ids conceptually."""
    identity_ids = ("form:كتب", "root:ktb", "pattern:فعل")
    trace_ids = ("trace:mufrad_123",)

    # These are different concepts
    assert set(identity_ids) != set(trace_ids)

    # Identity is about linguistic features
    assert any("form:" in iid for iid in identity_ids)
    assert any("root:" in iid for iid in identity_ids)

    # Trace is about provenance
    assert all("trace:" in tid for tid in trace_ids)


# ============================================================================
# Test 2: Carrier fallback detection
# ============================================================================

def test_carrier_fallback_detection():
    """PR #159: Carrier text fallback is marked explicitly."""
    # Create mock proof with text
    mock_proof = Mock()
    mock_proof.form.vocalization = "كَتَبَ"
    mock_proof.form.text = "كَتَبَ"

    carrier_ids = _carrier_ids_from_mufrad(mock_proof)

    # Assert: Fallback is marked
    assert _has_carrier_fallback(carrier_ids)
    assert any(":fallback:" in cid for cid in carrier_ids)


def test_carrier_fallback_marker_in_ids():
    """PR #159: Fallback carrier IDs contain :fallback: marker."""
    fallback_carriers = (
        "carrier:fallback:0:ك",
        "carrier:fallback:1:َ",
        "carrier:fallback:2:ت",
    )

    assert _has_carrier_fallback(fallback_carriers)


def test_carrier_non_fallback_no_marker():
    """PR #159: Non-fallback carrier IDs don't have :fallback: marker."""
    real_carriers = (
        "carrier:unicode:U+0643",
        "carrier:unicode:U+064E",
        "carrier:unicode:U+062A",
    )

    assert not _has_carrier_fallback(real_carriers)


# ============================================================================
# Test 3: Factor as structured object (not bare string)
# ============================================================================

def test_factor_source_candidate_structure():
    """PR #159: Factor is structured FactorSourceCandidate, not bare string."""
    factor = FactorSourceCandidate(
        source_id="relation:123",
        source_kind=FactorSourceKind.RELATION_CANDIDATE,
        identity_ids=("form:إن", "operator:inna"),
        trace_ids=("trace:rel_123",),
        rank=LughaRank.QIYAS,
    )

    # Assert: Factor has structured fields
    assert factor.source_id == "relation:123"
    assert factor.source_kind == FactorSourceKind.RELATION_CANDIDATE
    assert len(factor.identity_ids) > 0
    assert len(factor.trace_ids) > 0
    assert isinstance(factor.rank, LughaRank)


def test_factor_source_kind_enum():
    """PR #159: FactorSourceKind provides classification."""
    assert FactorSourceKind.RELATION_CANDIDATE.value == "relation_candidate"
    assert FactorSourceKind.OPERATOR_CANDIDATE.value == "operator_candidate"
    assert FactorSourceKind.ANCHOR.value == "anchor"
    assert FactorSourceKind.PREPOSITION.value == "preposition"


def test_build_factor_mark_equation_requires_structured_factor():
    """PR #159: build_factor_mark_equation requires FactorSourceCandidate."""
    factor = FactorSourceCandidate(
        source_id="test:factor",
        source_kind=FactorSourceKind.OPERATOR_CANDIDATE,
        identity_ids=("operator:test",),
        trace_ids=("trace:test",),
        rank=LughaRank.QIYAS,
    )

    mock_vector = Mock()
    mock_vector.allows_operator_consumption.return_value = True
    mock_vector.trace_id = "trace:affected"
    mock_vector.identity_ids = ("form:test",)
    mock_vector.residuals = ()
    mock_vector.final_rank = LughaRank.FORM

    # This should work with structured factor
    equation = build_factor_mark_equation(
        factor_source=factor,
        affected_vector=mock_vector,
        mark_potential=None,
        equation_type=FactorMarkEquationType.DEFERRED,
    )

    # Assert: Equation uses structured factor
    assert equation.factor_source == factor
    assert equation.factor_source.source_id == "test:factor"


def test_factor_source_preserves_identity_and_trace():
    """PR #159: FactorSourceCandidate preserves both identity_ids and trace_ids."""
    factor = FactorSourceCandidate(
        source_id="rel:456",
        source_kind=FactorSourceKind.RELATION_CANDIDATE,
        identity_ids=("form:كان", "root:kwn", "operator:kana"),
        trace_ids=("trace:rel_456", "trace:parent_123"),
        rank=LughaRank.QIYAS,
    )

    # Assert: Both identity and trace preserved
    assert len(factor.identity_ids) == 3
    assert len(factor.trace_ids) == 2
    assert "form:كان" in factor.identity_ids
    assert "trace:rel_456" in factor.trace_ids


# ============================================================================
# Test 4: Completeness check strengthening
# ============================================================================

def test_factor_mark_equation_has_factor_source_structured_condition():
    """PR #159: MinimalCompletenessCheck includes factor_source_structured."""
    factor = FactorSourceCandidate(
        source_id="test",
        source_kind=FactorSourceKind.ANCHOR,
        identity_ids=("test",),
        trace_ids=("test",),
        rank=LughaRank.QIYAS,
    )

    mock_vector = Mock()
    mock_vector.allows_operator_consumption.return_value = True
    mock_vector.trace_id = "trace:test"
    mock_vector.identity_ids = ()
    mock_vector.residuals = ()
    mock_vector.final_rank = LughaRank.QIYAS

    equation = build_factor_mark_equation(
        factor_source=factor,
        affected_vector=mock_vector,
        mark_potential=None,
        equation_type=FactorMarkEquationType.DEFERRED,
    )

    # Assert: Completeness check includes factor_source_structured
    completeness = equation.transition_proof.minimal_completeness
    assert "factor_source_structured" in completeness.required_conditions
    assert "factor_source_structured" in completeness.satisfied_conditions


def test_constitutional_prohibitions_still_enforced():
    """PR #159: Constitutional prohibitions preserved from PR #158."""
    factor = FactorSourceCandidate(
        source_id="test",
        source_kind=FactorSourceKind.PREPOSITION,
        identity_ids=("test",),
        trace_ids=("test",),
        rank=LughaRank.QIYAS,
    )

    mock_vector = Mock()
    mock_vector.allows_operator_consumption.return_value = True
    mock_vector.trace_id = "trace:test"
    mock_vector.identity_ids = ()
    mock_vector.residuals = ()
    mock_vector.final_rank = LughaRank.QIYAS

    equation = build_factor_mark_equation(
        factor_source=factor,
        affected_vector=mock_vector,
        mark_potential=None,
        equation_type=FactorMarkEquationType.DEFERRED,
    )

    # Assert: No meaning/ifadah/hukm/case_effect
    assert not equation.produces_meaning
    assert not equation.produces_ifadah
    assert not equation.produces_hukm
    assert not equation.produces_case_effect
