"""Test MufradAcceptanceEquation.

Tests verify LHS ≡ RHS equation proof for MufradProof acceptance.
"""

import pytest
from unittest.mock import Mock

from dal_core.mufrad_acceptance_equation import (
    MufradAcceptanceEquation,
    prove_mufrad_acceptance,
)
from dal_core.transition_proof_kernel import TransitionDecision
from dal_core.foundation import Rank


# ============================================================================
# Helper: Build Mock MufradProof
# ============================================================================

def build_mock_mufrad_proof(
    *,
    vocalization: str = "كِتَابٌ",
    composition_ready: bool = True,
    has_competitors: bool = False,
    residuals: tuple = (),
) -> Mock:
    """Build mock MufradProof for testing."""
    proof = Mock()

    # Form
    proof.form = Mock()
    proof.form.vocalization = vocalization
    proof.form.text = vocalization

    # Type
    proof.type = Mock()
    proof.type.dal_type = "noun"

    # Root candidates
    root = Mock()
    root.root = "كتب"
    proof.root_candidates = [root]

    # Wazn candidates
    wazn = Mock()
    wazn.pattern = "فِعَال"
    proof.wazn_candidates = [wazn]

    # Clitics
    proof.clitics = []

    # Readiness and competitors
    proof.is_composition_ready = Mock(return_value=composition_ready)
    proof.has_unresolved_competitors = Mock(return_value=has_competitors)
    proof.collect_all_residuals = Mock(return_value=list(residuals))

    # Rank and trace
    proof.rank = Rank.CANDIDATE
    proof.trace = {"id": "trace:test_123"}

    return proof


# ============================================================================
# MufradAcceptanceEquation Tests
# ============================================================================

def test_mufrad_acceptance_equation_structure():
    """Test basic acceptance equation structure."""
    equation = MufradAcceptanceEquation(
        equation_id="equation:test_001",
        mufrad_id="mufrad:test_001",
        lhs_carrier_ids=("carrier:0:ك", "carrier:1:ِ", "carrier:2:ت"),
        lhs_identity_ids=("form:كتاب", "type:noun"),
        lhs_effective_description_ids=("effective:test",),
        lhs_qiyas_proof_ids=("qiyas:test",),
        rhs_word_surface="كِتَابٌ",
        rhs_preserved_carrier_ids=("carrier:0:ك", "carrier:1:ِ", "carrier:2:ت"),
        rhs_preserved_identity_ids=("form:كتاب", "type:noun", "root:كتب"),
        rhs_trace_id="trace:test_001",
        transition_proof=Mock(decision=Mock(value="accepted")),
    )

    assert equation.equation_id == "equation:test_001"
    assert equation.rhs_word_surface == "كِتَابٌ"


def test_carriers_balanced_when_preserved():
    """Test carriers_balanced property when LHS ⊆ RHS."""
    equation = MufradAcceptanceEquation(
        equation_id="eq:test",
        mufrad_id="mufrad:test",
        lhs_carrier_ids=("carrier:0", "carrier:1"),
        lhs_identity_ids=(),
        lhs_effective_description_ids=(),
        lhs_qiyas_proof_ids=(),
        rhs_word_surface="test",
        rhs_preserved_carrier_ids=("carrier:0", "carrier:1", "carrier:2"),
        rhs_preserved_identity_ids=(),
        rhs_trace_id="trace:test",
        transition_proof=Mock(),
    )

    assert equation.carriers_balanced


def test_carriers_not_balanced_when_lost():
    """Test carriers_balanced property when carriers lost."""
    equation = MufradAcceptanceEquation(
        equation_id="eq:test",
        mufrad_id="mufrad:test",
        lhs_carrier_ids=("carrier:0", "carrier:1", "carrier:2"),
        lhs_identity_ids=(),
        lhs_effective_description_ids=(),
        lhs_qiyas_proof_ids=(),
        rhs_word_surface="test",
        rhs_preserved_carrier_ids=("carrier:0", "carrier:1"),  # Lost carrier:2
        rhs_preserved_identity_ids=(),
        rhs_trace_id="trace:test",
        transition_proof=Mock(),
    )

    assert not equation.carriers_balanced


def test_identities_balanced_when_preserved():
    """Test identities_balanced property when LHS ⊆ RHS."""
    equation = MufradAcceptanceEquation(
        equation_id="eq:test",
        mufrad_id="mufrad:test",
        lhs_carrier_ids=(),
        lhs_identity_ids=("form:test", "type:noun"),
        lhs_effective_description_ids=(),
        lhs_qiyas_proof_ids=(),
        rhs_word_surface="test",
        rhs_preserved_carrier_ids=(),
        rhs_preserved_identity_ids=("form:test", "type:noun", "root:tst"),
        rhs_trace_id="trace:test",
        transition_proof=Mock(),
    )

    assert equation.identities_balanced


def test_identities_not_balanced_when_lost():
    """Test identities_balanced property when identities lost."""
    equation = MufradAcceptanceEquation(
        equation_id="eq:test",
        mufrad_id="mufrad:test",
        lhs_carrier_ids=(),
        lhs_identity_ids=("form:test", "type:noun", "root:xyz"),
        lhs_effective_description_ids=(),
        lhs_qiyas_proof_ids=(),
        rhs_word_surface="test",
        rhs_preserved_carrier_ids=(),
        rhs_preserved_identity_ids=("form:test", "type:noun"),  # Lost root
        rhs_trace_id="trace:test",
        transition_proof=Mock(),
    )

    assert not equation.identities_balanced


def test_accepted_when_all_conditions_met():
    """Test accepted property when all conditions satisfied."""
    transition = Mock()
    transition.decision = Mock(value="accepted")

    equation = MufradAcceptanceEquation(
        equation_id="eq:test",
        mufrad_id="mufrad:test",
        lhs_carrier_ids=("c:0",),
        lhs_identity_ids=("id:a",),
        lhs_effective_description_ids=(),
        lhs_qiyas_proof_ids=(),
        rhs_word_surface="test",
        rhs_preserved_carrier_ids=("c:0",),
        rhs_preserved_identity_ids=("id:a",),
        rhs_trace_id="trace:test",
        transition_proof=transition,
    )

    assert equation.accepted


def test_not_accepted_when_transition_rejected():
    """Test not accepted when transition proof rejected."""
    transition = Mock()
    transition.decision = Mock(value="rejected")

    equation = MufradAcceptanceEquation(
        equation_id="eq:test",
        mufrad_id="mufrad:test",
        lhs_carrier_ids=("c:0",),
        lhs_identity_ids=("id:a",),
        lhs_effective_description_ids=(),
        lhs_qiyas_proof_ids=(),
        rhs_word_surface="test",
        rhs_preserved_carrier_ids=("c:0",),
        rhs_preserved_identity_ids=("id:a",),
        rhs_trace_id="trace:test",
        transition_proof=transition,
    )

    assert not equation.accepted


# ============================================================================
# prove_mufrad_acceptance Tests
# ============================================================================

def test_prove_mufrad_acceptance_basic():
    """Test basic prove_mufrad_acceptance with composition-ready proof."""
    proof = build_mock_mufrad_proof(
        vocalization="كِتَابٌ",
        composition_ready=True,
        has_competitors=False,
    )

    equation = prove_mufrad_acceptance(proof)

    assert equation.mufrad_id.startswith("mufrad:")
    assert equation.rhs_word_surface == "كِتَابٌ"
    assert equation.carriers_balanced
    assert equation.identities_balanced
    assert equation.transition_proof.decision == TransitionDecision.ACCEPTED


def test_prove_mufrad_acceptance_not_composition_ready():
    """Test prove_mufrad_acceptance with non-composition-ready proof."""
    proof = build_mock_mufrad_proof(
        composition_ready=False,
        has_competitors=False,
    )

    equation = prove_mufrad_acceptance(proof)

    # Should have blocking difference
    assert len(equation.transition_proof.qiyas.invalidating_differences) > 0
    blocking = equation.transition_proof.qiyas.invalidating_differences[0]
    assert blocking.blocks_transition
    assert "composition_ready" in blocking.difference_id

    # Should be rejected
    assert equation.transition_proof.decision == TransitionDecision.REJECTED


def test_prove_mufrad_acceptance_with_unresolved_competitors():
    """Test prove_mufrad_acceptance with unresolved competitors."""
    proof = build_mock_mufrad_proof(
        composition_ready=True,
        has_competitors=True,
    )

    equation = prove_mufrad_acceptance(proof)

    # Should have blocking difference for competitors
    differences = equation.transition_proof.qiyas.invalidating_differences
    assert any("competitors" in d.difference_id for d in differences)

    # Should be rejected
    assert equation.transition_proof.decision == TransitionDecision.REJECTED


def test_prove_mufrad_acceptance_extracts_carrier_ids():
    """Test that carrier IDs are extracted from form."""
    proof = build_mock_mufrad_proof(vocalization="كتب")

    equation = prove_mufrad_acceptance(proof)

    # Should have carrier for each character
    assert len(equation.lhs_carrier_ids) == len("كتب")
    assert all(cid.startswith("carrier:") for cid in equation.lhs_carrier_ids)


def test_prove_mufrad_acceptance_extracts_identity_ids():
    """Test that identity IDs are extracted from proof components."""
    proof = build_mock_mufrad_proof(vocalization="كتاب")

    equation = prove_mufrad_acceptance(proof)

    # Should have form identity
    assert any("form:" in iid for iid in equation.lhs_identity_ids)

    # Should have type identity
    assert any("type:" in iid for iid in equation.lhs_identity_ids)

    # Should have root identity
    assert any("root:" in iid for iid in equation.lhs_identity_ids)

    # Should have wazn identity
    assert any("wazn:" in iid for iid in equation.lhs_identity_ids)


def test_prove_mufrad_acceptance_preserves_trace():
    """Test that trace ID is preserved in equation."""
    proof = build_mock_mufrad_proof()
    proof.trace = {"id": "trace:specific_123"}

    equation = prove_mufrad_acceptance(proof)

    assert equation.rhs_trace_id == "trace:specific_123"
    assert "trace:specific_123" in equation.transition_proof.preserved_trace_ids


def test_prove_mufrad_acceptance_includes_residuals():
    """Test that residuals are included in transition proof."""
    residual1 = Mock()
    residual1.__str__ = Mock(return_value="residual:1")
    residual2 = Mock()
    residual2.__str__ = Mock(return_value="residual:2")

    proof = build_mock_mufrad_proof(residuals=(residual1, residual2))

    equation = prove_mufrad_acceptance(proof)

    # Should include residuals in transition proof
    assert "residual:1" in equation.transition_proof.residual_ids
    assert "residual:2" in equation.transition_proof.residual_ids


def test_prove_mufrad_acceptance_constitutional_prohibitions():
    """Test that no forbidden outputs are produced."""
    proof = build_mock_mufrad_proof()

    equation = prove_mufrad_acceptance(proof)

    # Verify constitutional prohibitions
    assert not equation.transition_proof.produces_meaning
    assert not equation.transition_proof.produces_ifadah
    assert not equation.transition_proof.produces_hukm


def test_prove_mufrad_acceptance_transition_proof_complete():
    """Test that complete transition proof is built."""
    proof = build_mock_mufrad_proof()

    equation = prove_mufrad_acceptance(proof)

    # Verify all transition proof components
    assert equation.transition_proof.qiyas is not None
    assert equation.transition_proof.identity_neutral is not None
    assert equation.transition_proof.minimal_completeness is not None

    # Verify layers
    assert equation.transition_proof.source_layer == "MUFRAD_PROOF"
    assert equation.transition_proof.target_layer == "PRESYNTAX_MUFRAD_VECTOR"

    # Verify rank preserved
    assert equation.transition_proof.rank_name == "CANDIDATE"
