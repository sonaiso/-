"""
U₁₁ RelationCompositionCandidateCarrier Constitutional Tests

Domain: U₁₁ = RelationCompositionCandidateCarrier
Transition: U₁₀ (WordFormCandidate) → U₁₁ (RelationCompositionCandidate)
Purpose: Licensed binding between word form candidates (NOT meaning assignment)

Constitutional Principle:
    التركيب ليس جمع ألفاظ. التركيب ربط مرخّص بين مرشحات لفظية محفوظة
    Composition ≠ WordList, Composition = GovernedBinding(WordFormCandidates)

Key Laws from Composition Constitution:
    1. لا تركيب بلا مفردات مرخصة (No composition without licensed word candidates)
    2. لا ربط بلا نوع (No binding without relation type)
    3. لا علاقة بلا محفوظات (No relation without preserved identities)
    4. Jāmid/Mushtaq/Mabni distinction enforced
    5. Three-axis temporal system (RelationTime, OccurrenceState, ContinuationState)
    6. Operator taxonomy enforced (not semantic determination)
    7. No IFADAH_IDENTITY output (ifadah is U₁₂)
    8. No HUKM_IDENTITY output (hukm is U₁₃)
    9. No SEMANTIC_IDENTITY output (meaning is preserved trace, not output)

Created: 2026-05-26
"""

import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from dal_core.u11_relation_composition_candidate_carrier import (
    RelationCompositionCandidateUnit,
    RelationCompositionCandidateResult,
    relation_composition_candidate_carrier_11,
    validate_approved_context_for_u11,
    RelationType,
    RelationTime,
    OccurrenceState,
    ContinuationState,
    BindingEdge,
    BearabilityCheck,
    AnchorType,
    OperatorClass,
    CompositionType,
)
from dal_core.approved_transition_context import ApprovedTransitionContext
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.identity_registry import IdentityType
from dal_core.domain_registry import DomainType
from dal_core.foundation.rank import Rank


# ============================================================================
# Test Helpers
# ============================================================================

def make_valid_approved_context_u10_to_u11():
    """Create valid ApprovedTransitionContext for U₁₀→U₁₁."""
    # NOTE: This is a mock. Real implementation requires DecisionAudit.
    context = MagicMock(spec=ApprovedTransitionContext)
    context.from_layer = ExecutionLayer.U10_WORD_FORM
    context.to_layer = ExecutionLayer.U11_RELATION_COMPOSITION
    context.input_identity = IdentityType.WORDFORM_IDENTITY
    context.output_identity = IdentityType.RELATION_COMPOSITION_IDENTITY
    context.domain = DomainType.WEIGHT_DOMAIN  # Placeholder (should be COMPOSITION_DOMAIN when added)
    return context


# ============================================================================
# Test 1: Constitutional Law - No U₁₁ without ApprovedTransitionContext
# ============================================================================

def test_u11_requires_approved_context():
    """
    Law: لا U₁₁ بلا ApprovedTransitionContext

    U₁₁ cannot execute without approved transition context from governor.
    """
    u10_input = {
        "word_candidates": [],
    }

    with pytest.raises(ValueError, match="U₁₁.*requires ApprovedTransitionContext"):
        relation_composition_candidate_carrier_11(
            u10_input=u10_input,
            approved_context=None  # ❌ Missing context
        )


# ============================================================================
# Test 2: Constitutional Law - Wrong transition context
# ============================================================================

def test_u11_rejects_wrong_transition():
    """
    Law: Context must be for U₁₀→U₁₁ transition specifically
    """
    u10_input = {"word_candidates": []}

    # Wrong FROM layer (using MagicMock)
    wrong_context = MagicMock(spec=ApprovedTransitionContext)
    wrong_context.from_layer = ExecutionLayer.U9_WEIGHT  # ❌ Should be U10_WORD_FORM
    wrong_context.to_layer = ExecutionLayer.U11_RELATION_COMPOSITION
    wrong_context.input_identity = IdentityType.WORDFORM_IDENTITY
    wrong_context.output_identity = IdentityType.RELATION_COMPOSITION_IDENTITY
    wrong_context.domain = DomainType.WEIGHT_DOMAIN

    with pytest.raises(ValueError, match="FROM U10_WORD_FORM"):
        validate_approved_context_for_u11(wrong_context, u10_input)


# ============================================================================
# Test 3: Constitutional Law - No composition without word candidates
# ============================================================================

def test_u11_requires_word_candidates():
    """
    Law: لا تركيب بلا مفردات مرخصة

    Composition requires at least one licensed word form candidate.
    """
    approved_context = make_valid_approved_context_u10_to_u11()

    u10_input = {
        "word_candidates": []  # ❌ Empty
    }

    with pytest.raises(ValueError, match="word_candidates.*U₁₀"):
        relation_composition_candidate_carrier_11(
            u10_input=u10_input,
            approved_context=approved_context
        )


# ============================================================================
# Test 4: Constitutional Law - Forbidden outputs
# ============================================================================

def test_u11_forbids_semantic_output():
    """
    Law: U₁₁ cannot output SEMANTIC_IDENTITY

    Composition binds word forms, does not determine meaning.
    """
    forbidden_context = MagicMock(spec=ApprovedTransitionContext)
    forbidden_context.from_layer = ExecutionLayer.U10_WORD_FORM
    forbidden_context.to_layer = ExecutionLayer.U11_RELATION_COMPOSITION
    forbidden_context.input_identity = IdentityType.WORDFORM_IDENTITY
    forbidden_context.output_identity = IdentityType.SEMANTIC_IDENTITY  # ❌ Forbidden
    forbidden_context.domain = DomainType.SEMANTICS_DOMAIN  # ❌ Wrong domain

    u10_input = {"word_candidates": [{"unit_id": "w1"}]}

    with pytest.raises(ValueError, match="cannot output.*SEMANTIC_IDENTITY"):
        validate_approved_context_for_u11(forbidden_context, u10_input)


def test_u11_forbids_hukm_output():
    """
    Law: U₁₁ cannot output HUKM_IDENTITY

    Hukm is U₁₃, not U₁₁.
    """
    forbidden_context = MagicMock(spec=ApprovedTransitionContext)
    forbidden_context.from_layer = ExecutionLayer.U10_WORD_FORM
    forbidden_context.to_layer = ExecutionLayer.U11_RELATION_COMPOSITION
    forbidden_context.input_identity = IdentityType.WORDFORM_IDENTITY
    forbidden_context.output_identity = IdentityType.HUKM_IDENTITY  # ❌ Forbidden
    forbidden_context.domain = DomainType.JUDGMENT_DOMAIN  # ❌ Wrong domain

    u10_input = {"word_candidates": [{"unit_id": "w1"}]}

    with pytest.raises(ValueError, match="cannot output.*HUKM_IDENTITY"):
        validate_approved_context_for_u11(forbidden_context, u10_input)


def test_u11_forbids_ifadah_output():
    """
    Law: U₁₁ cannot output IFADAH_IDENTITY

    Ifadah is U₁₂, not U₁₁.
    """
    forbidden_context = MagicMock(spec=ApprovedTransitionContext)
    forbidden_context.from_layer = ExecutionLayer.U10_WORD_FORM
    forbidden_context.to_layer = ExecutionLayer.U11_RELATION_COMPOSITION
    forbidden_context.input_identity = IdentityType.WORDFORM_IDENTITY
    forbidden_context.output_identity = IdentityType.IFADAH_IDENTITY  # ❌ Forbidden
    forbidden_context.domain = DomainType.WEIGHT_DOMAIN

    u10_input = {"word_candidates": [{"unit_id": "w1"}]}

    with pytest.raises(ValueError, match="cannot output.*IFADAH_IDENTITY"):
        validate_approved_context_for_u11(forbidden_context, u10_input)


# ============================================================================
# Test 5: Binding Edge Structure
# ============================================================================

def test_binding_edge_requires_type():
    """
    Law: لا ربط بلا نوع

    Every binding edge must have explicit relation type.
    """
    edge = BindingEdge(
        edge_id=str(uuid4()),
        governor_id="w1",
        governed_id="w2",
        relation_type=RelationType.ISNAD,  # ✓ Explicit
        rank=Rank.CANDIDATE
    )

    assert edge.relation_type == RelationType.ISNAD


def test_binding_edge_preserves_trace():
    """
    Law: لا علاقة بلا محفوظات

    Binding edge preserves governor/governed identities.
    """
    edge = BindingEdge(
        edge_id=str(uuid4()),
        governor_id="w1",
        governed_id="w2",
        relation_type=RelationType.WASF,
        rank=Rank.CANDIDATE
    )

    assert edge.governor_id == "w1"
    assert edge.governed_id == "w2"


# ============================================================================
# Test 6: Three Pillars - Jāmid/Mushtaq/Mabni Anchors
# ============================================================================

def test_jamid_anchor_entity():
    """
    Pillar 1: الجامد (Jāmid) - Entity Anchor

    Jāmid forms can anchor entities and bear predication.
    """
    check = BearabilityCheck(
        check_id=str(uuid4()),
        word_id="w1",
        anchor_type=AnchorType.ENTITY,  # Jāmid
        can_bear_predication=True,
        transformational_source=False,
        rank=Rank.CANDIDATE
    )

    assert check.anchor_type == AnchorType.ENTITY
    assert check.can_bear_predication is True
    assert check.transformational_source is False


def test_mushtaq_anchor_transformation():
    """
    Pillar 2: المشتق (Mushtaq) - Transformation Anchor

    Mushtaq forms require transformation source and can predicate.
    """
    check = BearabilityCheck(
        check_id=str(uuid4()),
        word_id="w2",
        anchor_type=AnchorType.TRANSFORMATION,  # Mushtaq
        can_bear_predication=True,
        transformational_source=True,
        requires_origin=True,
        rank=Rank.CANDIDATE
    )

    assert check.anchor_type == AnchorType.TRANSFORMATION
    assert check.transformational_source is True
    assert check.requires_origin is True


def test_mabni_anchor_function():
    """
    Pillar 3: المبني (Mabni) - Function Anchor

    Mabni forms anchor functions, cannot bear predication.
    """
    check = BearabilityCheck(
        check_id=str(uuid4()),
        word_id="w3",
        anchor_type=AnchorType.FUNCTION,  # Mabni
        can_bear_predication=False,  # ✓ Functions don't bear predication
        transformational_source=False,
        rank=Rank.CANDIDATE
    )

    assert check.anchor_type == AnchorType.FUNCTION
    assert check.can_bear_predication is False


# ============================================================================
# Test 7: Three-Axis Temporal System
# ============================================================================

def test_temporal_three_axes_independent():
    """
    Law: Temporal state has 3 independent axes

    Not 5 names (ماض/مضارع/أمر/كان/كاد), but:
        - RelationTime (PAST/PRESENT/FUTURE)
        - OccurrenceState (OCCURRED/OCCURRING/NEAR/...)
        - ContinuationState (ENDED/CONTINUING/...)
    """
    unit = RelationCompositionCandidateUnit(
        unit_id=str(uuid4()),
        composition_id=str(uuid4()),
        word_candidate_ids=("w1", "w2"),
        binding_edges=(
            BindingEdge(
                edge_id=str(uuid4()),
                governor_id="w1",
                governed_id="w2",
                relation_type=RelationType.ISNAD,
                rank=Rank.CANDIDATE
            ),
        ),
        relation_time=RelationTime.PAST,
        occurrence_state=OccurrenceState.OCCURRED,
        continuation_state=ContinuationState.ENDED,
        rank=Rank.CANDIDATE
    )

    # Three independent axes
    assert unit.relation_time == RelationTime.PAST
    assert unit.occurrence_state == OccurrenceState.OCCURRED
    assert unit.continuation_state == ContinuationState.ENDED


def test_occurrence_state_near_not_closure():
    """
    Law: كاد = NEAR, not definitive NOT_OCCURRED

    كاد يفعل = near occurrence + residual about actual occurrence
    """
    unit = RelationCompositionCandidateUnit(
        unit_id=str(uuid4()),
        composition_id=str(uuid4()),
        word_candidate_ids=("w1", "w2"),
        binding_edges=(),
        occurrence_state=OccurrenceState.NEAR,  # ✓ كاد
        rank=Rank.CANDIDATE
    )

    assert unit.occurrence_state == OccurrenceState.NEAR
    # Actual occurrence requires evidence, left as residual


# ============================================================================
# Test 8: Operator Class Taxonomy (Not Over-generalization)
# ============================================================================

def test_operator_class_temporal_transfer():
    """
    Operator Class: TEMPORAL_TRANSFER (كان وأخواتها)

    كان ≠ صار ≠ ليس
    Each has distinct time_transfer and negation properties.
    """
    assert OperatorClass.TEMPORAL_TRANSFER.value == "TEMPORAL_TRANSFER"


def test_operator_class_state_transition():
    """
    Operator Class: STATE_TRANSITION (صار، أصبح، ...)

    Marks state change, distinct from temporal transfer.
    """
    assert OperatorClass.STATE_TRANSITION.value == "STATE_TRANSITION"


def test_operator_class_negated_predication():
    """
    Operator Class: NEGATED_PREDICATION (ليس، ما، لا)

    Negates relation, distinct from temporal transfer.
    """
    assert OperatorClass.NEGATED_PREDICATION.value == "NEGATED_PREDICATION"


def test_operator_class_continuation():
    """
    Operator Class: CONTINUATION (ما زال، ما انفك، ...)

    Marks continuation, distinct from state transition.
    """
    assert OperatorClass.CONTINUATION.value == "CONTINUATION"


def test_operator_class_epistemic():
    """
    Operator Class: EPISTEMIC (ظن، علم، حسب، ...)

    Epistemic operators preserved for future U₁₃ (hukm layer).
    At U₁₁, they establish binding but NOT epistemic rank.
    """
    assert OperatorClass.EPISTEMIC.value == "EPISTEMIC"


# ============================================================================
# Test 9: Composition Type Routing (Beyond Predicative)
# ============================================================================

def test_composition_type_predicative():
    """
    Composition Type: PREDICATIVE (جملة خبرية)
    """
    unit = RelationCompositionCandidateUnit(
        unit_id=str(uuid4()),
        composition_id=str(uuid4()),
        word_candidate_ids=("w1", "w2"),
        binding_edges=(),
        composition_type=CompositionType.PREDICATIVE,
        rank=Rank.CANDIDATE
    )

    assert unit.composition_type == CompositionType.PREDICATIVE


def test_composition_type_interrogative():
    """
    Composition Type: INTERROGATIVE (جملة استفهامية)

    هل، من، ما، ... establish interrogative composition.
    """
    unit = RelationCompositionCandidateUnit(
        unit_id=str(uuid4()),
        composition_id=str(uuid4()),
        word_candidate_ids=("w1", "w2"),
        binding_edges=(),
        composition_type=CompositionType.INTERROGATIVE,
        rank=Rank.CANDIDATE
    )

    assert unit.composition_type == CompositionType.INTERROGATIVE


def test_composition_type_imperative():
    """
    Composition Type: IMPERATIVE (جملة أمرية)
    """
    unit = RelationCompositionCandidateUnit(
        unit_id=str(uuid4()),
        composition_id=str(uuid4()),
        word_candidate_ids=("w1",),
        binding_edges=(),
        composition_type=CompositionType.IMPERATIVE,
        rank=Rank.CANDIDATE
    )

    assert unit.composition_type == CompositionType.IMPERATIVE


def test_composition_type_vocative():
    """
    Composition Type: VOCATIVE (جملة ندائية)

    يا، أيها، ... establish vocative composition.
    """
    unit = RelationCompositionCandidateUnit(
        unit_id=str(uuid4()),
        composition_id=str(uuid4()),
        word_candidate_ids=("w1", "w2"),
        binding_edges=(),
        composition_type=CompositionType.VOCATIVE,
        rank=Rank.CANDIDATE
    )

    assert unit.composition_type == CompositionType.VOCATIVE


# ============================================================================
# Test 10: Relation Type Preservation
# ============================================================================

def test_relation_type_isnad():
    """
    Relation Type: ISNAD (الإسناد)

    Core predication relation (مبتدأ-خبر، فعل-فاعل).
    """
    edge = BindingEdge(
        edge_id=str(uuid4()),
        governor_id="w1",
        governed_id="w2",
        relation_type=RelationType.ISNAD,
        rank=Rank.CANDIDATE
    )

    assert edge.relation_type == RelationType.ISNAD


def test_relation_type_wasf():
    """
    Relation Type: WASF (الوصف)

    Adjectival/participial description.
    """
    edge = BindingEdge(
        edge_id=str(uuid4()),
        governor_id="w1",
        governed_id="w2",
        relation_type=RelationType.WASF,
        rank=Rank.CANDIDATE
    )

    assert edge.relation_type == RelationType.WASF


def test_relation_type_idafah():
    """
    Relation Type: IDAFAH (الإضافة)

    Possessive/annexation relation.
    """
    edge = BindingEdge(
        edge_id=str(uuid4()),
        governor_id="w1",
        governed_id="w2",
        relation_type=RelationType.IDAFAH,
        rank=Rank.CANDIDATE
    )

    assert edge.relation_type == RelationType.IDAFAH


# ============================================================================
# Test 11: Golden Path Execution
# ============================================================================

def test_u11_golden_path_simple_isnad():
    """
    Golden Path: الرجلُ كاتبٌ (The man is a writer)

    Jāmid (entity) + Mushtaq (transformation) → ISNAD relation
    """
    approved_context = make_valid_approved_context_u10_to_u11()

    u10_input = {
        "word_candidates": [
            {
                "unit_id": "w1",
                "surface_form": "الرجلُ",
                "anchor_type": "ENTITY",  # Jāmid
                "can_bear_predication": True,
                "transformational_source": False,  # ✓ Jāmid has no transformation
            },
            {
                "unit_id": "w2",
                "surface_form": "كاتبٌ",
                "anchor_type": "TRANSFORMATION",  # Mushtaq
                "can_bear_predication": True,
                "transformational_source": True,  # ✓ Mushtaq requires transformation
                "requires_origin": True,
            }
        ]
    }

    result = relation_composition_candidate_carrier_11(
        u10_input=u10_input,
        approved_context=approved_context
    )

    # Verify result structure
    assert result.source_layer == ExecutionLayer.U10_WORD_FORM
    assert result.target_layer == ExecutionLayer.U11_RELATION_COMPOSITION
    assert len(result.candidates) > 0

    # Verify first candidate
    candidate = result.candidates[0]
    assert len(candidate.word_candidate_ids) == 2
    assert len(candidate.binding_edges) > 0

    # Verify binding edge
    edge = candidate.binding_edges[0]
    assert edge.relation_type == RelationType.ISNAD
    assert edge.rank == Rank.CANDIDATE
