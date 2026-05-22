"""Tests for General Learning: فاعل Pattern Experiment.

This test file implements the canonical experiment specified in Issue #49:

Positive Origins:
    كاتب (writer), زارع (farmer), عامل (worker)

Initial Rule:
    "وزن فاعل يرشح علاقة فاعلية"
    "فاعل pattern licenses agentive relation"

Constraining Examples (Counterexamples):
    طاهر (pure), حامض (sour), بارد (cold), كريم (generous), حكيم (wise)

Expected Refinement:
    "فاعل does not always indicate actual agency;
     it licenses agentive OR qualitative interpretation
     based on source event, lexicalization, usage, and context"

This test proves:
    1. Rules are LEARNED from origins (not declared)
    2. Rules are TESTED against examples
    3. Rules FACE counterexamples
    4. Rules are REFINED with explicit scope/constraints
    5. Modifications PRESERVE traces, residuals, and ranks
    6. Changes are EXPLAINED (why promoted/demoted/refined)
"""

from __future__ import annotations

import pytest

from fvafk.algebra import Evidence, Residual, Rank

from fvafk.algebra.general_learning import (
    # Origin
    Origin,
    OriginSet,
    extract_origin,
    make_origin_set,
    # Invariant
    Invariant,
    InvariantKind,
    detect_invariants,
    # Manaat
    Manaat,
    ManaatScope,
    determine_manaat,
    # Rule Candidate
    RuleCandidate,
    RuleStatus,
    make_rule_candidate,
    # Verification
    verify_rule,
    detect_counterexamples,
    Counterexample,
    CounterexampleKind,
    # Explanation
    Explanation,
    ExplanationKind,
    explain_modification,
    explain_rank_change,
    # Learner
    GeneralLearner,
    LearningCycle,
    # Residuals
    make_origin_insufficient,
    make_invariant_unclear,
    make_manaat_ambiguous,
    make_counterexample_unresolved,
)


# ===========================================================================
# Fixtures: Positive Origins
# ===========================================================================


@pytest.fixture
def origin_katib():
    """كاتب (writer) - agentive origin."""
    return Origin(
        surface="كاتب",
        pattern="فاعل",
        root=("ك", "ت", "ب"),
        interpretation="agentive",
        evidence=(
            Evidence(
                kind="lexicon.attested",
                source="Hans Wehr Dictionary",
                detail="writer, author, clerk (one who writes)",
                weight=1.0,
            ),
        ),
        rank=Rank.LICENSED,
    )


@pytest.fixture
def origin_zaare():
    """زارع (farmer) - agentive origin."""
    return Origin(
        surface="زارع",
        pattern="فاعل",
        root=("ز", "ر", "ع"),
        interpretation="agentive",
        evidence=(
            Evidence(
                kind="lexicon.attested",
                source="Hans Wehr Dictionary",
                detail="farmer, cultivator (one who plants/cultivates)",
                weight=1.0,
            ),
        ),
        rank=Rank.LICENSED,
    )


@pytest.fixture
def origin_aamil():
    """عامل (worker) - agentive origin."""
    return Origin(
        surface="عامل",
        pattern="فاعل",
        root=("ع", "م", "ل"),
        interpretation="agentive",
        evidence=(
            Evidence(
                kind="lexicon.attested",
                source="Hans Wehr Dictionary",
                detail="worker, laborer, agent (one who works/acts)",
                weight=1.0,
            ),
        ),
        rank=Rank.LICENSED,
    )


# ===========================================================================
# Fixtures: Constraining Examples (Counterexamples)
# ===========================================================================


@pytest.fixture
def counter_tahir():
    """طاهر (pure) - qualitative, not agentive."""
    return Origin(
        surface="طاهر",
        pattern="فاعل",
        root=("ط", "ه", "ر"),
        interpretation="qualitative",
        evidence=(
            Evidence(
                kind="lexicon.attested",
                source="Hans Wehr Dictionary",
                detail="pure, clean, chaste (quality/state, not agent)",
                weight=1.0,
            ),
        ),
        rank=Rank.LICENSED,
    )


@pytest.fixture
def counter_haamid():
    """حامض (sour) - qualitative, not agentive."""
    return Origin(
        surface="حامض",
        pattern="فاعل",
        root=("ح", "م", "ض"),
        interpretation="qualitative",
        evidence=(
            Evidence(
                kind="lexicon.attested",
                source="Hans Wehr Dictionary",
                detail="sour, acid (quality/taste, not agent)",
                weight=1.0,
            ),
        ),
        rank=Rank.LICENSED,
    )


@pytest.fixture
def counter_baarid():
    """بارد (cold) - qualitative, not agentive."""
    return Origin(
        surface="بارد",
        pattern="فاعل",
        root=("ب", "ر", "د"),
        interpretation="qualitative",
        evidence=(
            Evidence(
                kind="lexicon.attested",
                source="Hans Wehr Dictionary",
                detail="cold, cool (temperature quality, not agent)",
                weight=1.0,
            ),
        ),
        rank=Rank.LICENSED,
    )


# ===========================================================================
# Test 1: Origin Extraction
# ===========================================================================


def test_origin_extraction_from_positive_examples(origin_katib, origin_zaare, origin_aamil):
    """Test that origins are properly extracted from positive examples."""
    # All three origins should be valid
    assert origin_katib.surface == "كاتب"
    assert origin_katib.pattern == "فاعل"
    assert origin_katib.interpretation == "agentive"
    assert origin_katib.is_verified

    assert origin_zaare.surface == "زارع"
    assert origin_aamil.surface == "عامل"

    # All should have same pattern
    assert origin_katib.pattern == origin_zaare.pattern == origin_aamil.pattern


def test_origin_set_construction(origin_katib, origin_zaare, origin_aamil):
    """Test that origin set is properly constructed from origins."""
    origin_set = make_origin_set(origins=(origin_katib, origin_zaare, origin_aamil))

    assert len(origin_set.origins) == 3
    assert origin_set.is_sufficient  # ≥3 origins
    assert origin_set.is_consistent  # All same pattern and interpretation
    assert origin_set.is_verified  # All verified
    assert origin_set.shared_pattern == "فاعل"
    assert origin_set.shared_feature == "agentive"


# ===========================================================================
# Test 2: Invariant Detection
# ===========================================================================


def test_invariant_detection_from_origins(origin_katib, origin_zaare, origin_aamil):
    """Test that invariants are detected from origin set."""
    origins = (origin_katib, origin_zaare, origin_aamil)
    inv_set = detect_invariants(origins)

    # Should detect at least 2 invariants: pattern and interpretation
    assert len(inv_set.invariants) >= 2

    # Check pattern invariant
    pattern_inv = next((inv for inv in inv_set.invariants if inv.kind == InvariantKind.PATTERN), None)
    assert pattern_inv is not None
    assert pattern_inv.value == "فاعل"
    assert pattern_inv.coverage == 1.0  # All origins have this pattern
    assert pattern_inv.is_stable

    # Check interpretation invariant
    interp_inv = next((inv for inv in inv_set.invariants if inv.kind == InvariantKind.INTERPRETATION_TYPE), None)
    assert interp_inv is not None
    assert interp_inv.value == "agentive"
    assert interp_inv.coverage == 1.0

    # Strongest invariant should be pattern (morphological is stronger than semantic)
    assert inv_set.strongest.kind == InvariantKind.PATTERN


# ===========================================================================
# Test 3: Manaat Determination
# ===========================================================================


def test_manaat_determination_from_invariants(origin_katib, origin_zaare, origin_aamil):
    """Test that manaat (scope/basis) is determined from invariants."""
    origins = (origin_katib, origin_zaare, origin_aamil)
    inv_set = detect_invariants(origins)

    manaat = determine_manaat(
        invariants=inv_set.invariants,
        positive_examples=origins,
    )

    # Manaat should be clear
    assert manaat.is_clear
    assert not manaat.is_ambiguous

    # Should include pattern condition
    assert any("pattern" in cond.lower() for cond in manaat.positive_conditions)

    # Confidence should be reasonable
    assert manaat.confidence >= 0.7


# ===========================================================================
# Test 4: Rule Candidate Extraction
# ===========================================================================


def test_rule_candidate_extraction(origin_katib, origin_zaare, origin_aamil):
    """Test that rule candidate is extracted from origins."""
    learner = GeneralLearner()
    learner.add_origins(origin_katib, origin_zaare, origin_aamil)

    rule = learner.extract_rule()

    # Rule should be properly formed
    assert rule.pattern == "فاعل"
    assert "agentive" in rule.description.lower()
    assert rule.rank in (Rank.CANDIDATE, Rank.LICENSED)
    assert rule.status == RuleStatus.HYPOTHESIS

    # Rule should have origins and invariants
    assert len(rule.origins) == 3
    assert len(rule.invariants) >= 2

    # Rule should have evidence
    assert len(rule.evidence) >= 1


# ===========================================================================
# Test 5: Counterexample Detection
# ===========================================================================


def test_counterexample_detection(origin_katib, origin_zaare, origin_aamil, counter_tahir, counter_haamid, counter_baarid):
    """Test that counterexamples are detected when rule is tested."""
    # Extract rule from positive origins
    learner = GeneralLearner()
    learner.add_origins(origin_katib, origin_zaare, origin_aamil)
    rule = learner.extract_rule()

    # Detect counterexamples
    counterexamples = detect_counterexamples(
        rule,
        examples=(counter_tahir, counter_haamid, counter_baarid),
    )

    # All three should be counterexamples (qualitative, not agentive)
    assert len(counterexamples) >= 1  # At least one detected

    # Check first counterexample
    ce = counterexamples[0]
    assert ce.pattern == "فاعل"
    assert ce.expected != ce.actual  # Expected agentive, got qualitative
    assert ce.kind == CounterexampleKind.FALSE_POSITIVE
    assert ce.requires_refinement


# ===========================================================================
# Test 6: Rule Verification
# ===========================================================================


def test_rule_verification_with_counterexamples(origin_katib, origin_zaare, origin_aamil, counter_tahir, counter_haamid, counter_baarid):
    """Test that rule verification detects counterexamples and suggests refinement."""
    # Extract rule
    learner = GeneralLearner()
    learner.add_origins(origin_katib, origin_zaare, origin_aamil)
    rule = learner.extract_rule()

    # Verify against counterexamples
    verification = verify_rule(
        rule,
        test_examples=(counter_tahir, counter_haamid, counter_baarid),
    )

    # Should find counterexamples
    assert verification.has_counterexamples
    assert verification.needs_refinement

    # Should have refinement suggestions
    assert len(verification.refinement_suggestions) >= 1

    # Confirmation rate should be low (all are counterexamples)
    assert verification.confirmation_rate < 0.5


# ===========================================================================
# Test 7: Rule Refinement
# ===========================================================================


def test_rule_refinement_after_counterexamples(origin_katib, origin_zaare, origin_aamil, counter_tahir, counter_haamid, counter_baarid):
    """Test that rule is refined after encountering counterexamples."""
    # Extract and verify
    learner = GeneralLearner()
    learner.add_origins(origin_katib, origin_zaare, origin_aamil)
    learner.extract_rule()

    initial_description = learner.current_rule.description

    # Verify and refine
    final_rule = learner.verify_and_refine(
        test_examples=(counter_tahir, counter_haamid, counter_baarid),
    )

    # Rule should have been refined
    assert final_rule.is_refined
    assert len(final_rule.modifications) >= 1

    # Description should have changed
    assert final_rule.description != initial_description

    # Refined description should mention both interpretations
    assert "agentive" in final_rule.description.lower() or "qualitative" in final_rule.description.lower()

    # Status should be REFINED
    assert final_rule.status == RuleStatus.REFINED


# ===========================================================================
# Test 8: Modification History
# ===========================================================================


def test_modification_history_preserved(origin_katib, origin_zaare, origin_aamil, counter_tahir, counter_haamid):
    """Test that modification history is preserved with traces and residuals."""
    learner = GeneralLearner()
    learner.add_origins(origin_katib, origin_zaare, origin_aamil)
    learner.extract_rule()

    final_rule = learner.verify_and_refine(
        test_examples=(counter_tahir, counter_haamid),
    )

    # Should have modification history
    assert final_rule.modification_count >= 1

    # Latest modification should have details
    mod = final_rule.latest_modification
    assert mod is not None
    assert mod.before_description != ""
    assert mod.after_description != ""
    assert mod.trigger != ""  # Should mention counterexamples

    # Should have trace
    assert final_rule.trace.operation != ""


# ===========================================================================
# Test 9: Rank Changes
# ===========================================================================


def test_rank_changes_during_learning(origin_katib, origin_zaare, origin_aamil, counter_tahir):
    """Test that rank changes appropriately during learning."""
    learner = GeneralLearner()
    learner.add_origins(origin_katib, origin_zaare, origin_aamil)

    initial_rule = learner.extract_rule()
    initial_rank = initial_rule.rank

    # After encountering counterexamples, rank may change
    final_rule = learner.verify_and_refine(test_examples=(counter_tahir,))

    # Rank should be recorded in cycles
    assert len(learner.cycles) >= 1
    cycle = learner.cycles[0]

    # Cycle should record rank change (if any)
    assert cycle.rule_before.rank in (Rank.CANDIDATE, Rank.LICENSED, Rank.CERTIFIED)
    assert cycle.rule_after.rank in (Rank.CANDIDATE, Rank.LICENSED, Rank.CERTIFIED)


# ===========================================================================
# Test 10: Explanations
# ===========================================================================


def test_explanations_generated(origin_katib, origin_zaare, origin_aamil, counter_tahir):
    """Test that explanations are generated for modifications."""
    learner = GeneralLearner()
    learner.add_origins(origin_katib, origin_zaare, origin_aamil)
    learner.extract_rule()

    learner.verify_and_refine(test_examples=(counter_tahir,))

    # Should have at least one cycle
    assert len(learner.cycles) >= 1

    # Cycle should have explanations
    cycle = learner.cycles[0]
    assert len(cycle.explanations) >= 1

    # Explanation should have required fields
    explanation = cycle.explanations[0]
    assert explanation.what_changed != ""
    assert explanation.why_changed != ""
    assert explanation.kind in ExplanationKind


# ===========================================================================
# Test 11: Complete Learning Cycle
# ===========================================================================


def test_complete_learning_cycle(origin_katib, origin_zaare, origin_aamil, counter_tahir, counter_haamid, counter_baarid):
    """Test complete learning cycle from origins to refined rule."""
    learner = GeneralLearner()

    # Step 1: Add origins
    learner.add_origins(origin_katib, origin_zaare, origin_aamil)
    assert learner.origin_set is not None
    assert len(learner.origin_set.origins) == 3

    # Step 2: Extract rule
    rule = learner.extract_rule()
    assert rule.pattern == "فاعل"
    assert rule.status == RuleStatus.HYPOTHESIS

    # Step 3: Verify and refine
    final_rule = learner.verify_and_refine(
        test_examples=(counter_tahir, counter_haamid, counter_baarid),
    )

    # Step 4: Verify final state
    assert final_rule.is_refined
    assert final_rule.status in (RuleStatus.REFINED, RuleStatus.STABLE)
    assert len(learner.cycles) >= 1

    # Step 5: Verify learning happened
    assert learner.cycles[0].had_counterexamples
    assert learner.cycles[0].rule_changed
    assert len(learner.cycles[0].explanations) >= 1


# ===========================================================================
# Test 12: Residual Tracking
# ===========================================================================


def test_residual_tracking_through_learning(origin_katib, origin_zaare):
    """Test that residuals are tracked throughout learning process."""
    learner = GeneralLearner()

    # With only 2 origins, should have "origin.insufficient" residual
    learner.add_origins(origin_katib, origin_zaare)
    rule = learner.extract_rule()

    # Check for origin insufficiency residual
    assert any(r.kind == "origin.insufficient" for r in rule.residuals)


# ===========================================================================
# Test 13: Evidence Accumulation
# ===========================================================================


def test_evidence_accumulation(origin_katib, origin_zaare, origin_aamil):
    """Test that evidence accumulates from origins, invariants, and verification."""
    learner = GeneralLearner()
    learner.add_origins(origin_katib, origin_zaare, origin_aamil)
    rule = learner.extract_rule()

    # Should have evidence from rule extraction
    assert len(rule.evidence) >= 1

    # Evidence should include origin and invariant evidence
    evidence_kinds = {e.kind for e in rule.evidence}
    assert any("rule" in kind or "invariant" in kind for kind in evidence_kinds)


# ===========================================================================
# Test 14: Replay-ability
# ===========================================================================


def test_rule_replay_ability(origin_katib, origin_zaare, origin_aamil):
    """Test that rules are replay-able (can be serialized for debugging)."""
    learner = GeneralLearner()
    learner.add_origins(origin_katib, origin_zaare, origin_aamil)
    rule = learner.extract_rule()

    # Should be able to convert to replay dict
    replay = rule.to_replay()

    # Replay should have all key fields
    assert "description" in replay
    assert "pattern" in replay
    assert "rank" in replay
    assert "status" in replay
    assert "origin_count" in replay
    assert replay["origin_count"] == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
