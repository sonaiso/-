"""Test TransitionProofKernel components.

Tests verify unified transition proof patterns across all layers.
"""

import pytest

from dal_core.transition_proof_kernel import (
    TransitionDecision,
    EffectiveDescription,
    InvalidatingDifference,
    QiyasProof,
    IdentityNeutralCheck,
    MinimalCompletenessCheck,
    TransitionProof,
)


# ============================================================================
# EffectiveDescription Tests
# ============================================================================

def test_effective_description_creation():
    """Test basic effective description creation."""
    effective = EffectiveDescription(
        description_id="effective:test_001",
        description_type="morphological_carrier",
        evidence=("MufradProof", "surface_effects"),
    )

    assert effective.description_id == "effective:test_001"
    assert effective.description_type == "morphological_carrier"
    assert len(effective.evidence) == 2
    assert "MufradProof" in effective.evidence


def test_effective_description_frozen():
    """Test that effective description is immutable."""
    effective = EffectiveDescription(
        description_id="effective:test_002",
        description_type="test",
        evidence=("test_evidence",),
    )

    with pytest.raises(Exception):  # FrozenInstanceError
        effective.description_id = "modified"


# ============================================================================
# InvalidatingDifference Tests
# ============================================================================

def test_invalidating_difference_blocking():
    """Test blocking invalidating difference."""
    difference = InvalidatingDifference(
        difference_id="diff:blocking_001",
        message="Missing required field",
        blocks_transition=True,
        evidence=("composition_readiness",),
    )

    assert difference.blocks_transition
    assert "Missing" in difference.message


def test_invalidating_difference_warning():
    """Test non-blocking invalidating difference (warning)."""
    difference = InvalidatingDifference(
        difference_id="diff:warning_001",
        message="Low confidence in root extraction",
        blocks_transition=False,
        evidence=("root_candidates",),
    )

    assert not difference.blocks_transition


# ============================================================================
# QiyasProof Tests
# ============================================================================

def test_qiyas_proof_accepted():
    """Test qiyas proof with no blocking differences."""
    effective = EffectiveDescription(
        description_id="effective:qiyas_001",
        description_type="carrier",
        evidence=("test",),
    )

    qiyas = QiyasProof(
        proof_id="qiyas:test_001",
        origin_id="origin:mufrad_contract",
        branch_id="branch:test_word",
        effective_description=effective,
        shared_cause="preserves form without meaning",
        invalidating_differences=(),
    )

    assert qiyas.accepted
    assert not qiyas.has_blocking_difference


def test_qiyas_proof_with_blocking_difference():
    """Test qiyas proof rejected by blocking difference."""
    effective = EffectiveDescription(
        description_id="effective:qiyas_002",
        description_type="carrier",
        evidence=("test",),
    )

    blocking = InvalidatingDifference(
        difference_id="diff:block",
        message="Composition not ready",
        blocks_transition=True,
        evidence=("readiness",),
    )

    qiyas = QiyasProof(
        proof_id="qiyas:test_002",
        origin_id="origin:test",
        branch_id="branch:test",
        effective_description=effective,
        shared_cause="test",
        invalidating_differences=(blocking,),
    )

    assert not qiyas.accepted
    assert qiyas.has_blocking_difference


def test_qiyas_proof_with_warning_only():
    """Test qiyas proof accepted with non-blocking warnings."""
    effective = EffectiveDescription(
        description_id="effective:qiyas_003",
        description_type="carrier",
        evidence=("test",),
    )

    warning = InvalidatingDifference(
        difference_id="diff:warn",
        message="Low confidence warning",
        blocks_transition=False,
        evidence=("confidence",),
    )

    qiyas = QiyasProof(
        proof_id="qiyas:test_003",
        origin_id="origin:test",
        branch_id="branch:test",
        effective_description=effective,
        shared_cause="test",
        invalidating_differences=(warning,),
    )

    assert qiyas.accepted
    assert not qiyas.has_blocking_difference


# ============================================================================
# IdentityNeutralCheck Tests
# ============================================================================

def test_identity_neutral_preserved():
    """Test identity preservation check passes."""
    check = IdentityNeutralCheck(
        check_id="id_neutral:test_001",
        input_identity_ids=("form:كتاب", "type:noun"),
        output_identity_ids=("form:كتاب", "type:noun", "root:كتب"),
        preserved=True,
    )

    assert check.preserved
    assert len(check.input_identity_ids) == 2
    assert len(check.output_identity_ids) == 3


def test_identity_neutral_validation_failure():
    """Test that identity neutral check validates preservation claim."""
    with pytest.raises(ValueError, match="lost"):
        IdentityNeutralCheck(
            check_id="id_neutral:invalid",
            input_identity_ids=("form:كتاب", "type:noun"),
            output_identity_ids=("form:كتاب",),  # Lost "type:noun"
            preserved=True,  # Claims preservation but actually lost identity
        )


def test_identity_neutral_honest_non_preservation():
    """Test identity neutral check with honest non-preservation."""
    check = IdentityNeutralCheck(
        check_id="id_neutral:test_002",
        input_identity_ids=("form:كتاب", "type:noun"),
        output_identity_ids=("form:كتاب",),
        preserved=False,  # Honestly states non-preservation
    )

    assert not check.preserved


# ============================================================================
# MinimalCompletenessCheck Tests
# ============================================================================

def test_minimal_completeness_passed():
    """Test minimal completeness when all conditions satisfied."""
    check = MinimalCompletenessCheck(
        check_id="minimum:test_001",
        target_layer="PRESYNTAX_MUFRAD_VECTOR",
        required_conditions=(
            "carriers_present",
            "identities_preserved",
            "no_meaning",
        ),
        satisfied_conditions=(
            "carriers_present",
            "identities_preserved",
            "no_meaning",
        ),
        missing_conditions=(),
        passed=True,
    )

    assert check.passed
    assert len(check.missing_conditions) == 0


def test_minimal_completeness_failed():
    """Test minimal completeness when conditions missing."""
    check = MinimalCompletenessCheck(
        check_id="minimum:test_002",
        target_layer="PRESYNTAX_MUFRAD_VECTOR",
        required_conditions=(
            "carriers_present",
            "identities_preserved",
            "composition_ready",
        ),
        satisfied_conditions=(
            "carriers_present",
            "identities_preserved",
        ),
        missing_conditions=("composition_ready",),
        passed=False,
    )

    assert not check.passed
    assert "composition_ready" in check.missing_conditions


def test_minimal_completeness_validation_failure():
    """Test that minimal completeness validates passed flag."""
    with pytest.raises(ValueError, match="missing conditions"):
        MinimalCompletenessCheck(
            check_id="minimum:invalid",
            target_layer="TEST",
            required_conditions=("a", "b", "c"),
            satisfied_conditions=("a", "b"),
            missing_conditions=("c",),
            passed=True,  # Claims pass but has missing conditions
        )


# ============================================================================
# TransitionProof Tests
# ============================================================================

def test_transition_proof_accepted():
    """Test complete transition proof that is accepted."""
    effective = EffectiveDescription(
        description_id="effective:transition_001",
        description_type="carrier",
        evidence=("test",),
    )

    qiyas = QiyasProof(
        proof_id="qiyas:transition_001",
        origin_id="origin:test",
        branch_id="branch:test",
        effective_description=effective,
        shared_cause="test",
        invalidating_differences=(),
    )

    neutral = IdentityNeutralCheck(
        check_id="id_neutral:transition_001",
        input_identity_ids=("id:a",),
        output_identity_ids=("id:a",),
        preserved=True,
    )

    minimum = MinimalCompletenessCheck(
        check_id="minimum:transition_001",
        target_layer="TEST",
        required_conditions=("a",),
        satisfied_conditions=("a",),
        missing_conditions=(),
        passed=True,
    )

    transition = TransitionProof(
        proof_id="transition:test_001",
        source_layer="SOURCE",
        target_layer="TARGET",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=("trace:001",),
        residual_ids=(),
        rank_name="CANDIDATE",
    )

    assert transition.decision == TransitionDecision.ACCEPTED


def test_transition_proof_rejected_by_forbidden_output():
    """Test transition rejected by constitutional prohibition."""
    effective = EffectiveDescription("eff", "test", ("test",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True)
    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        proof_id="transition:forbidden",
        source_layer="SOURCE",
        target_layer="TARGET",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=(),
        residual_ids=(),
        rank_name="CANDIDATE",
        produces_meaning=True,  # FORBIDDEN
    )

    assert transition.decision == TransitionDecision.REJECTED


def test_transition_proof_rejected_by_blocking_difference():
    """Test transition rejected by qiyas blocking difference."""
    effective = EffectiveDescription("eff", "test", ("test",))

    blocking = InvalidatingDifference(
        "diff", "Blocked", blocks_transition=True, evidence=("test",)
    )

    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", (blocking,))
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True)
    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        proof_id="transition:blocked",
        source_layer="SOURCE",
        target_layer="TARGET",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=(),
        residual_ids=(),
        rank_name="CANDIDATE",
    )

    assert transition.decision == TransitionDecision.REJECTED


def test_transition_proof_deferred_by_missing_conditions():
    """Test transition deferred when minimal completeness not satisfied."""
    effective = EffectiveDescription("eff", "test", ("test",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True)

    minimum = MinimalCompletenessCheck(
        "min", "TEST", ("a", "b"), ("a",), ("b",), passed=False
    )

    transition = TransitionProof(
        proof_id="transition:deferred",
        source_layer="SOURCE",
        target_layer="TARGET",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=(),
        residual_ids=(),
        rank_name="CANDIDATE",
    )

    assert transition.decision == TransitionDecision.DEFERRED


def test_transition_proof_rejected_by_identity_loss():
    """Test transition rejected when identity not preserved."""
    effective = EffectiveDescription("eff", "test", ("test",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())

    neutral = IdentityNeutralCheck(
        "neutral", ("a", "b"), ("a",), preserved=False
    )

    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        proof_id="transition:identity_loss",
        source_layer="SOURCE",
        target_layer="TARGET",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=(),
        residual_ids=(),
        rank_name="CANDIDATE",
    )

    assert transition.decision == TransitionDecision.REJECTED


# ============================================================================
# TransitionDecision Enum Tests
# ============================================================================

def test_transition_decision_values():
    """Test all transition decision enum values exist."""
    assert TransitionDecision.ACCEPTED.value == "accepted"
    assert TransitionDecision.REJECTED.value == "rejected"
    assert TransitionDecision.DEFERRED.value == "deferred"
