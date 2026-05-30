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

# CRITICAL FIX (PR #163): Import Rank from fvafk.algebra
from fvafk.algebra.core import Rank, Result, Evidence, Residual, Failure


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
        has_missing_identity=False,
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
        has_missing_identity=False,
    )

    assert not check.preserved


def test_identity_neutral_missing_identity_empty_input():
    """
    Test missing identity detection with empty input (PR #166).

    Constitutional Law: Empty identity_ids linguistically means "missing identity".
    Mathematically preserved (∅ ⊆ ∅), but flagged for linguistic resolution.
    """
    check = IdentityNeutralCheck(
        check_id="id_neutral:missing_001",
        input_identity_ids=(),
        output_identity_ids=(),
        preserved=True,  # ∅ ⊆ ∅ = true (mathematically)
        has_missing_identity=True,  # Linguistically missing
    )

    assert check.preserved  # Trivially preserved
    assert check.has_missing_identity  # But flagged as missing


def test_identity_neutral_missing_identity_validation_failure():
    """
    Test that empty identity_ids requires has_missing_identity=True (PR #166).

    Constitutional Violation: Cannot have empty identity_ids with
    has_missing_identity=False.
    """
    with pytest.raises(ValueError, match="empty identity_ids"):
        IdentityNeutralCheck(
            check_id="id_neutral:invalid_missing",
            input_identity_ids=(),
            output_identity_ids=(),
            preserved=True,  # Can be True (∅ ⊆ ∅)
            has_missing_identity=False,  # Violation: empty but claims not missing
        )


def test_identity_neutral_non_empty_with_missing_flag():
    """
    Test that non-empty identity_ids cannot have has_missing_identity=True (PR #166).

    Constitutional Violation: Cannot claim missing identity when IDs present.
    """
    with pytest.raises(ValueError, match="claims missing identity but has non-empty"):
        IdentityNeutralCheck(
            check_id="id_neutral:invalid_flag",
            input_identity_ids=("form:كتاب",),
            output_identity_ids=("form:كتاب",),
            preserved=True,
            has_missing_identity=True,  # Violation: has IDs but claims missing
        )


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
        has_missing_identity=False,
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
        rank=Rank.CANDIDATE,  # CRITICAL FIX (PR #163): Use typed Rank
    )

    assert transition.decision == TransitionDecision.ACCEPTED


def test_transition_proof_rejected_by_forbidden_output():
    """Test transition rejected by constitutional prohibition."""
    effective = EffectiveDescription("eff", "test", ("test",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
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
        rank=Rank.CANDIDATE,  # CRITICAL FIX (PR #163): Use typed Rank
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
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
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
        rank=Rank.CANDIDATE,  # CRITICAL FIX (PR #163): Use typed Rank
    )

    assert transition.decision == TransitionDecision.REJECTED


def test_transition_proof_deferred_by_missing_conditions():
    """Test transition deferred when minimal completeness not satisfied."""
    effective = EffectiveDescription("eff", "test", ("test",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)

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
        rank=Rank.CANDIDATE,  # CRITICAL FIX (PR #163): Use typed Rank
    )

    assert transition.decision == TransitionDecision.DEFERRED


def test_transition_proof_rejected_by_identity_loss():
    """Test transition rejected when identity not preserved."""
    effective = EffectiveDescription("eff", "test", ("test",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())

    neutral = IdentityNeutralCheck(
        "neutral", ("a", "b"), ("a",), preserved=False, has_missing_identity=False
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
        rank=Rank.CANDIDATE,  # CRITICAL FIX (PR #163): Use typed Rank
    )

    assert transition.decision == TransitionDecision.REJECTED


def test_transition_proof_deferred_by_missing_identity():
    """
    Test transition deferred when identity_ids are empty (PR #166).

    Constitutional Law: Empty identity_ids requires residual and DEFERRED decision.

    Semantic Note: Empty → empty IS preserved (trivially: ∅ ⊆ ∅),
    but has_missing_identity=True flags it for deferral.
    """
    effective = EffectiveDescription("eff", "test", ("test",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())

    # Empty identity_ids → has_missing_identity=True, but preserved=True (∅ ⊆ ∅)
    neutral = IdentityNeutralCheck(
        "neutral", (), (), preserved=True, has_missing_identity=True
    )

    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        proof_id="transition:missing_identity",
        source_layer="SOURCE",
        target_layer="TARGET",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=(),
        residual_ids=("residual:missing_identity:test",),  # Residual added
        rank=Rank.CANDIDATE,
    )

    # Decision should be DEFERRED (not REJECTED) because missing identity is recoverable
    assert transition.decision == TransitionDecision.DEFERRED


def test_transition_proof_missing_identity_requires_residual():
    """
    Test that has_missing_identity=True requires residual:missing_identity.

    Constitutional Law (PR #167 completion):
        If identity_neutral.has_missing_identity is True,
        residual_ids MUST contain at least one residual starting
        with "residual:missing_identity".

    This test ensures the gap identified in the PR #167 review is closed.
    """
    effective = EffectiveDescription("eff", "test", ("test",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())

    # Empty identity_ids → has_missing_identity=True
    neutral = IdentityNeutralCheck(
        "neutral", (), (), preserved=True, has_missing_identity=True
    )

    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    # Attempt to create TransitionProof WITHOUT missing_identity residual
    with pytest.raises(ValueError, match="residual:missing_identity"):
        TransitionProof(
            proof_id="transition:invalid_missing",
            source_layer="SOURCE",
            target_layer="TARGET",
            qiyas=qiyas,
            identity_neutral=neutral,
            minimal_completeness=minimum,
            preserved_trace_ids=(),
            residual_ids=(),  # NO residual:missing_identity (violation!)
            rank=Rank.CANDIDATE,
        )


def test_transition_proof_missing_identity_with_residual_is_deferred():
    """
    Test that missing identity WITH proper residual results in DEFERRED.

    Constitutional Law:
        has_missing_identity=True + residual:missing_identity → DEFERRED
        (not REJECTED, because it's recoverable)

    This confirms the intended behavior after closing the PR #167 gap.
    """
    effective = EffectiveDescription("eff", "test", ("test",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())

    # Empty identity_ids with proper flag
    neutral = IdentityNeutralCheck(
        "neutral", (), (), preserved=True, has_missing_identity=True
    )

    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    # Create with proper residual
    transition = TransitionProof(
        proof_id="transition:missing_with_residual",
        source_layer="SOURCE",
        target_layer="TARGET",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=(),
        residual_ids=("residual:missing_identity:source:test",),  # Proper residual
        rank=Rank.CANDIDATE,
    )

    # Should be DEFERRED (recoverable), not REJECTED
    assert transition.decision == TransitionDecision.DEFERRED
    assert transition.identity_neutral.preserved  # Trivially preserved (∅ ⊆ ∅)
    assert transition.identity_neutral.has_missing_identity  # But flagged as missing
    assert any("residual:missing_identity" in str(r) for r in transition.residual_ids)


# ============================================================================
# TransitionDecision Enum Tests
# ============================================================================

def test_transition_decision_values():
    """Test all transition decision enum values exist."""
    assert TransitionDecision.ACCEPTED.value == "accepted"
    assert TransitionDecision.REJECTED.value == "rejected"
    assert TransitionDecision.DEFERRED.value == "deferred"


# ============================================================================
# TransitionProof.to_result() Tests (PR #163)
# ============================================================================


def test_to_result_accepted_with_licensed_rank():
    """Test to_result() with ACCEPTED decision and LICENSED rank."""
    effective = EffectiveDescription(
        "eff", "morphological", ("evidence:form", "evidence:surface")
    )
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("id:a",), ("id:a",), True, False)
    minimum = MinimalCompletenessCheck("min", "TARGET", ("a",), ("a",), (), True)

    transition = TransitionProof(
        proof_id="proof:test",
        source_layer="SOURCE",
        target_layer="TARGET",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=("trace:001",),
        residual_ids=(),
        rank=Rank.LICENSED,
    )

    result = transition.to_result("test_value", operation="test_transition")

    assert result.value == "test_value"
    assert result.rank == Rank.LICENSED
    assert len(result.evidence) == 2  # From effective description evidence
    assert len(result.residuals) == 0  # No residuals
    assert len(result.failures) == 0  # No failures
    assert result.trace.operation == "test_transition"
    assert "trace:001" in result.trace.parents


def test_to_result_rejected_with_blocking_difference():
    """Test to_result() with REJECTED decision due to blocking difference."""
    effective = EffectiveDescription("eff", "test", ("ev",))
    blocking = InvalidatingDifference(
        "diff", "Composition not ready", blocks_transition=True, evidence=("test",)
    )
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", (blocking,))
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        "proof", "SOURCE", "TARGET", qiyas, neutral, minimum, (), (), Rank.CANDIDATE
    )

    result = transition.to_result(42)

    assert result.value == 42
    assert result.rank == Rank.REFUTED  # REJECTED → REFUTED
    assert len(result.failures) == 1
    assert result.failures[0].kind == "blocking_difference"
    assert result.failures[0].fatal is True


def test_to_result_rejected_with_constitutional_prohibition():
    """Test to_result() with REJECTED due to forbidden output."""
    effective = EffectiveDescription("eff", "test", ("ev",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        "proof",
        "SOURCE",
        "TARGET",
        qiyas,
        neutral,
        minimum,
        (),
        (),
        Rank.CANDIDATE,
        produces_meaning=True,  # FORBIDDEN
    )

    result = transition.to_result("value")

    assert result.rank == Rank.REFUTED
    assert len(result.failures) == 1
    assert result.failures[0].kind == "constitutional_prohibition"
    assert "forbidden meaning" in result.failures[0].description
    assert result.failures[0].fatal is True


def test_to_result_deferred_with_missing_conditions():
    """Test to_result() with DEFERRED decision due to missing conditions."""
    effective = EffectiveDescription("eff", "test", ("ev",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
    minimum = MinimalCompletenessCheck(
        "min", "TEST", ("a", "b"), ("a",), ("b",), passed=False
    )

    transition = TransitionProof(
        "proof", "SOURCE", "TARGET", qiyas, neutral, minimum, (), (), Rank.CANDIDATE
    )

    result = transition.to_result("deferred_value")

    assert result.value == "deferred_value"
    assert result.rank == Rank.CANDIDATE  # DEFERRED with evidence → CANDIDATE
    assert len(result.residuals) == 1  # Missing condition "b"
    assert result.residuals[0].kind == "missing_condition"
    assert "b" in result.residuals[0].description


def test_to_result_with_non_blocking_differences_as_residuals():
    """Test that non-blocking differences become residuals."""
    effective = EffectiveDescription("eff", "test", ("ev",))
    warning = InvalidatingDifference(
        "diff", "Low confidence", blocks_transition=False, evidence=("conf",)
    )
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", (warning,))
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        "proof", "SOURCE", "TARGET", qiyas, neutral, minimum, (), (), Rank.CANDIDATE
    )

    result = transition.to_result("value")

    assert result.rank == Rank.CANDIDATE
    assert len(result.residuals) == 1
    assert result.residuals[0].kind == "non_blocking_difference"
    assert "Low confidence" in result.residuals[0].description


def test_to_result_with_residual_ids():
    """Test that residual_ids are converted to Residual objects."""
    effective = EffectiveDescription("eff", "test", ("ev",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        "proof",
        "SOURCE",
        "TARGET",
        qiyas,
        neutral,
        minimum,
        (),
        ("residual:001", "residual:002"),  # residual_ids
        Rank.CANDIDATE,
    )

    result = transition.to_result("value")

    assert len(result.residuals) == 2
    assert result.residuals[0].kind == "residual_id"
    assert "residual:001" in result.residuals[0].description


def test_to_result_raises_for_licensed_without_evidence():
    """Test that LICENSED rank without evidence raises ValueError."""
    # Create TransitionProof with LICENSED rank but no evidence
    effective = EffectiveDescription("eff", "test", ())  # NO evidence
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        "proof",
        "SOURCE",
        "TARGET",
        qiyas,
        neutral,
        minimum,
        (),
        (),
        Rank.LICENSED,  # LICENSED but no evidence
    )

    with pytest.raises(ValueError, match="rank LICENSED but no evidence"):
        transition.to_result("value")


def test_to_result_trace_metadata():
    """Test that trace metadata includes proof details."""
    effective = EffectiveDescription("eff", "test", ("ev",))
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        "proof:metadata_test",
        "LAYER_A",
        "LAYER_B",
        qiyas,
        neutral,
        minimum,
        ("parent:001", "parent:002"),
        (),
        Rank.CANDIDATE,
    )

    result = transition.to_result("value", operation="custom_op")

    assert result.trace.operation == "custom_op"
    assert result.trace.metadata["proof_id"] == "proof:metadata_test"
    assert result.trace.metadata["source_layer"] == "LAYER_A"
    assert result.trace.metadata["target_layer"] == "LAYER_B"
    assert result.trace.metadata["decision"] == "accepted"
    assert "parent:001" in result.trace.parents
    assert "parent:002" in result.trace.parents


# ============================================================================
# Rank Ceiling Tests (PR #163 improvements)
# ============================================================================


def test_to_result_rank_ceiling_prevents_inflation():
    """Test that rank ceiling prevents inflation from weak evidence."""
    # Create proof with LICENSED rank but only string evidence (weak)
    effective = EffectiveDescription(
        "eff", "test", ("evidence:weak1", "evidence:weak2")
    )
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        "proof",
        "SOURCE",
        "TARGET",
        qiyas,
        neutral,
        minimum,
        (),
        (),
        Rank.LICENSED,  # Proof claims LICENSED
    )

    result = transition.to_result("value")

    # CRITICAL: Rank ceiling should cap at CANDIDATE
    # because evidence is just strings, not validated traces
    assert result.rank == Rank.CANDIDATE  # NOT LICENSED!
    assert len(result.evidence) == 2  # Evidence is present
    # But rank is capped by ceiling


def test_to_result_weak_evidence_creates_residual():
    """Test that weak/unvalidated evidence sources create residuals."""
    # Create proof with evidence that lacks proper namespace
    effective = EffectiveDescription(
        "eff", "test", ("some random string", "evidence:valid_one")
    )
    qiyas = QiyasProof("qiyas", "orig", "branch", effective, "cause", ())
    neutral = IdentityNeutralCheck("neutral", ("a",), ("a",), True, False)
    minimum = MinimalCompletenessCheck("min", "TEST", ("a",), ("a",), (), True)

    transition = TransitionProof(
        "proof", "SOURCE", "TARGET", qiyas, neutral, minimum, (), (), Rank.CANDIDATE
    )

    result = transition.to_result("value")

    # Should have only 1 Evidence (the valid one)
    assert len(result.evidence) == 1
    assert result.evidence[0].source == "evidence:valid_one"

    # Should have 1 residual for weak evidence
    weak_residuals = [r for r in result.residuals if r.kind == "weak_evidence_source"]
    assert len(weak_residuals) == 1
    assert "some random string" in weak_residuals[0].description


def test_validate_evidence_source_accepts_proper_namespaces():
    """Test that evidence validation accepts proper namespaces."""
    # Valid namespaces
    assert TransitionProof._validate_evidence_source("trace:abc123")
    assert TransitionProof._validate_evidence_source("candidate:def456")
    assert TransitionProof._validate_evidence_source("evidence:form_match")
    assert TransitionProof._validate_evidence_source("test:unit_001")
    assert TransitionProof._validate_evidence_source("proof:qiyas_123")
    assert TransitionProof._validate_evidence_source("source:span_10_20")

    # Invalid/weak sources
    assert not TransitionProof._validate_evidence_source("random string")
    assert not TransitionProof._validate_evidence_source("no_namespace_here")
    assert not TransitionProof._validate_evidence_source("")
    assert not TransitionProof._validate_evidence_source(None)
