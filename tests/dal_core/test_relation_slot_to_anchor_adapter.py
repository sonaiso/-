"""Test RelationSlotToAnchorAdapter.

Tests verify critical bridge from RelationSlotVector to Anchors.
"""

import pytest
from unittest.mock import Mock

from dal_core.relation_slot_to_anchor_adapter import (
    RelationSlotAnchorBundle,
    adapt_slot_to_anchors,
)
from dal_core.relation_slot_readiness import (
    CompositionFrameType,
    NominalFrameSlotGeometry,
    VerbalFrameSlotGeometry,
    SemiSentenceFrameSlotGeometry,
    RelationSlotVector,
)
from dal_core.relation_algebra_core import ReferenceStatus, StabilityType
from dal_core.transition_proof_kernel import TransitionDecision


# ============================================================================
# Helper: Build Mock PreSyntaxMufradVector
# ============================================================================

def build_mock_presyntax_vector(
    *,
    surface: str = "كتاب",
    trace_id: str = "trace:test_001",
    root_id: str = "root:كتب",
    pattern_id: str = "pattern:فعال",
) -> Mock:
    """Build mock PreSyntaxMufradVector for testing."""
    vector = Mock()
    vector.final_surface = surface
    vector.trace_id = trace_id

    # Root candidates
    root = Mock()
    root.root = root_id
    vector.root_candidates = [root] if root_id != "UNRESOLVED" else []

    # Wazn candidates
    wazn = Mock()
    wazn.pattern = pattern_id
    vector.wazn_candidates = [wazn] if pattern_id != "UNRESOLVED" else []

    return vector


# ============================================================================
# adapt_slot_to_anchors - Nominal Frame Tests
# ============================================================================

def test_adapt_nominal_frame_basic():
    """Test adapting nominal frame to anchors."""
    mubtada = build_mock_presyntax_vector(
        surface="الكتابُ", trace_id="trace:mubtada"
    )
    khabar = build_mock_presyntax_vector(
        surface="جديدٌ", trace_id="trace:khabar"
    )

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada,
        khabar_vector=khabar,
    )

    slot = RelationSlotVector(
        slot_id="slot:nominal_001",
        relation_slot_type=CompositionFrameType.NOMINAL,
        slot_geometry=geometry,
        source_trace_ids=("trace:mubtada", "trace:khabar"),
    )

    bundle = adapt_slot_to_anchors(slot)

    # Verify bundle structure
    assert bundle.slot_id == "slot:nominal_001"
    assert len(bundle.anchors) == 2

    # Verify Entity anchor (mubtada)
    entity_anchor = bundle.anchors[0]
    assert entity_anchor.anchor_type.value == "entity"
    assert entity_anchor.surface == "الكتابُ"

    # Verify Transformation anchor (khabar)
    transformation_anchor = bundle.anchors[1]
    assert transformation_anchor.anchor_type.value == "transformation"
    assert transformation_anchor.surface == "جديدٌ"

    # Verify transition proof
    assert bundle.transition_proof.decision == TransitionDecision.ACCEPTED


def test_adapt_nominal_frame_with_missing_root():
    """Test nominal frame adaptation when root ID unavailable."""
    mubtada = build_mock_presyntax_vector(
        surface="هذا",
        root_id="UNRESOLVED",  # No root candidates
    )
    khabar = build_mock_presyntax_vector(surface="جميل")

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada,
        khabar_vector=khabar,
    )

    slot = RelationSlotVector(
        slot_id="slot:nominal_002",
        relation_slot_type=CompositionFrameType.NOMINAL,
        slot_geometry=geometry,
        source_trace_ids=("trace:mubtada", "trace:khabar"),
    )

    bundle = adapt_slot_to_anchors(slot)

    # Should use UNRESOLVED for reference and stability
    entity_anchor = bundle.anchors[0]
    assert entity_anchor.reference_status == ReferenceStatus.UNRESOLVED


# ============================================================================
# adapt_slot_to_anchors - Verbal Frame Tests
# ============================================================================

def test_adapt_verbal_frame_intransitive():
    """Test adapting intransitive verbal frame."""
    verb = build_mock_presyntax_vector(
        surface="ذهبَ", trace_id="trace:verb"
    )
    actor = build_mock_presyntax_vector(
        surface="الطالبُ", trace_id="trace:actor"
    )

    geometry = VerbalFrameSlotGeometry(
        verb_vector=verb,
        actor_vector=actor,
        object_vector=None,  # Intransitive
    )

    slot = RelationSlotVector(
        slot_id="slot:verbal_001",
        relation_slot_type=CompositionFrameType.VERBAL,
        slot_geometry=geometry,
        source_trace_ids=("trace:verb", "trace:actor"),
    )

    bundle = adapt_slot_to_anchors(slot)

    # Should have 2 anchors (verb + actor)
    assert len(bundle.anchors) == 2

    # Transformation (verb)
    transformation_anchor = bundle.anchors[0]
    assert transformation_anchor.anchor_type.value == "transformation"
    assert transformation_anchor.surface == "ذهبَ"

    # Entity (actor)
    entity_anchor = bundle.anchors[1]
    assert entity_anchor.anchor_type.value == "entity"
    assert entity_anchor.surface == "الطالبُ"


def test_adapt_verbal_frame_transitive():
    """Test adapting transitive verbal frame."""
    verb = build_mock_presyntax_vector(
        surface="كتبَ", trace_id="trace:verb"
    )
    actor = build_mock_presyntax_vector(
        surface="الطالبُ", trace_id="trace:actor"
    )
    obj = build_mock_presyntax_vector(
        surface="الدرسَ", trace_id="trace:object"
    )

    geometry = VerbalFrameSlotGeometry(
        verb_vector=verb,
        actor_vector=actor,
        object_vector=obj,  # Transitive
    )

    slot = RelationSlotVector(
        slot_id="slot:verbal_002",
        relation_slot_type=CompositionFrameType.VERBAL,
        slot_geometry=geometry,
        source_trace_ids=("trace:verb", "trace:actor", "trace:object"),
    )

    bundle = adapt_slot_to_anchors(slot)

    # Should have 3 anchors (verb + actor + object)
    assert len(bundle.anchors) == 3

    # Transformation (verb)
    assert bundle.anchors[0].anchor_type.value == "transformation"

    # Entity (actor)
    assert bundle.anchors[1].anchor_type.value == "entity"
    assert bundle.anchors[1].surface == "الطالبُ"

    # Entity (object)
    assert bundle.anchors[2].anchor_type.value == "entity"
    assert bundle.anchors[2].surface == "الدرسَ"


# ============================================================================
# adapt_slot_to_anchors - Semi-Sentence Frame Tests
# ============================================================================

def test_adapt_semi_sentence_frame():
    """Test adapting semi-sentence (prepositional) frame."""
    operator = build_mock_presyntax_vector(
        surface="في", trace_id="trace:operator"
    )
    governed = build_mock_presyntax_vector(
        surface="البيتِ", trace_id="trace:governed"
    )

    geometry = SemiSentenceFrameSlotGeometry(
        operator_vector=operator,
        governed_vector=governed,
    )

    slot = RelationSlotVector(
        slot_id="slot:semi_001",
        relation_slot_type=CompositionFrameType.SEMI_SENTENCE,
        slot_geometry=geometry,
        source_trace_ids=("trace:operator", "trace:governed"),
    )

    bundle = adapt_slot_to_anchors(slot)

    # Should have 2 anchors
    assert len(bundle.anchors) == 2

    # Function anchor (operator)
    function_anchor = bundle.anchors[0]
    assert function_anchor.anchor_type.value == "function"
    assert function_anchor.surface == "في"

    # Entity anchor (governed)
    entity_anchor = bundle.anchors[1]
    assert entity_anchor.anchor_type.value == "entity"
    assert entity_anchor.surface == "البيتِ"


# ============================================================================
# Transition Proof Tests
# ============================================================================

def test_adapt_transition_proof_components():
    """Test that transition proof has all required components."""
    mubtada = build_mock_presyntax_vector()
    khabar = build_mock_presyntax_vector()

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada,
        khabar_vector=khabar,
    )

    slot = RelationSlotVector(
        slot_id="slot:test",
        relation_slot_type=CompositionFrameType.NOMINAL,
        slot_geometry=geometry,
        source_trace_ids=("trace:a", "trace:b"),
    )

    bundle = adapt_slot_to_anchors(slot)

    # Verify transition proof structure
    proof = bundle.transition_proof
    assert proof.source_layer == "RELATION_SLOT_VECTOR"
    assert proof.target_layer == "RELATION_ALGEBRA_ANCHORS"

    # Verify qiyas
    assert proof.qiyas is not None
    assert proof.qiyas.accepted

    # Verify identity preservation
    assert proof.identity_neutral is not None
    assert proof.identity_neutral.preserved

    # Verify minimal completeness
    assert proof.minimal_completeness is not None
    assert proof.minimal_completeness.passed


def test_adapt_preserves_trace_ids():
    """Test that source trace IDs are preserved in transition."""
    mubtada = build_mock_presyntax_vector(trace_id="trace:mubtada_123")
    khabar = build_mock_presyntax_vector(trace_id="trace:khabar_456")

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada,
        khabar_vector=khabar,
    )

    slot = RelationSlotVector(
        slot_id="slot:test",
        relation_slot_type=CompositionFrameType.NOMINAL,
        slot_geometry=geometry,
        source_trace_ids=("trace:mubtada_123", "trace:khabar_456"),
    )

    bundle = adapt_slot_to_anchors(slot)

    # Verify traces preserved
    assert "trace:mubtada_123" in bundle.transition_proof.preserved_trace_ids
    assert "trace:khabar_456" in bundle.transition_proof.preserved_trace_ids


def test_adapt_constitutional_prohibitions():
    """Test that no forbidden outputs are produced."""
    mubtada = build_mock_presyntax_vector()
    khabar = build_mock_presyntax_vector()

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada,
        khabar_vector=khabar,
    )

    slot = RelationSlotVector(
        slot_id="slot:test",
        relation_slot_type=CompositionFrameType.NOMINAL,
        slot_geometry=geometry,
        source_trace_ids=("trace:a", "trace:b"),
    )

    bundle = adapt_slot_to_anchors(slot)

    # Verify constitutional prohibitions
    assert not bundle.transition_proof.produces_meaning
    assert not bundle.transition_proof.produces_ifadah
    assert not bundle.transition_proof.produces_hukm


# ============================================================================
# Error Cases
# ============================================================================

def test_adapt_unsupported_frame_type():
    """Test error when unsupported frame type provided."""
    slot = RelationSlotVector(
        slot_id="slot:invalid",
        relation_slot_type=Mock(value="UNSUPPORTED"),  # Invalid type
        slot_geometry=Mock(),
        source_trace_ids=(),
    )

    with pytest.raises(ValueError, match="Unsupported"):
        adapt_slot_to_anchors(slot)


def test_adapt_nominal_with_wrong_geometry():
    """Test error when geometry doesn't match frame type."""
    # Verbal geometry with NOMINAL type
    verb = build_mock_presyntax_vector()
    actor = build_mock_presyntax_vector()

    geometry = VerbalFrameSlotGeometry(
        verb_vector=verb,
        actor_vector=actor,
        object_vector=None,
    )

    slot = RelationSlotVector(
        slot_id="slot:mismatch",
        relation_slot_type=CompositionFrameType.NOMINAL,  # Wrong type
        slot_geometry=geometry,
        source_trace_ids=("trace:a", "trace:b"),
    )

    with pytest.raises(ValueError, match="Expected.*NominalFrameSlotGeometry"):
        adapt_slot_to_anchors(slot)


# ============================================================================
# Conservative Anchor Building Tests
# ============================================================================

def test_conservative_anchor_uses_unresolved_for_missing_data():
    """Test that UNRESOLVED is used when data unavailable."""
    mubtada = build_mock_presyntax_vector(
        root_id="UNRESOLVED",
        pattern_id="UNRESOLVED",
    )
    khabar = build_mock_presyntax_vector()

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada,
        khabar_vector=khabar,
    )

    slot = RelationSlotVector(
        slot_id="slot:test",
        relation_slot_type=CompositionFrameType.NOMINAL,
        slot_geometry=geometry,
        source_trace_ids=("trace:a", "trace:b"),
    )

    bundle = adapt_slot_to_anchors(slot)

    # Entity anchor should have UNRESOLVED for missing data
    entity_anchor = bundle.anchors[0]
    assert entity_anchor.reference_status == ReferenceStatus.UNRESOLVED
    assert entity_anchor.stability == StabilityType.UNRESOLVED
