"""Test RelationCandidateBuilder.

Tests verify complete composition chain: slot → anchors → operation → candidate.
"""

import pytest
from unittest.mock import Mock, patch

from dal_core.relation_candidate_builder import (
    RelationCandidate,
    build_relation_candidate,
)
from dal_core.relation_slot_readiness import (
    CompositionFrameType,
    NominalFrameSlotGeometry,
    RelationSlotVector,
)
from dal_core.relation_algebra_core import RelationType
from dal_core.foundation import Rank


# ============================================================================
# Helper: Build Mock PreSyntaxMufradVector
# ============================================================================

def build_mock_presyntax_vector(
    *,
    surface: str = "test",
    trace_id: str = "trace:test",
) -> Mock:
    """Build mock PreSyntaxMufradVector."""
    vector = Mock()
    vector.final_surface = surface
    vector.trace_id = trace_id
    vector.root_candidates = [Mock(root="root:test")]
    vector.wazn_candidates = [Mock(pattern="pattern:test")]
    return vector


# ============================================================================
# Helper: Build Mock RelationSlotVector
# ============================================================================

def build_mock_nominal_slot(
    *,
    slot_id: str = "slot:test",
    mubtada_surface: str = "الكتابُ",
    khabar_surface: str = "جديدٌ",
) -> RelationSlotVector:
    """Build mock nominal RelationSlotVector."""
    mubtada = build_mock_presyntax_vector(
        surface=mubtada_surface, trace_id="trace:mubtada"
    )
    khabar = build_mock_presyntax_vector(
        surface=khabar_surface, trace_id="trace:khabar"
    )

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada,
        khabar_vector=khabar,
    )

    return RelationSlotVector(
        slot_id=slot_id,
        relation_slot_type=CompositionFrameType.NOMINAL,
        slot_geometry=geometry,
        source_trace_ids=("trace:mubtada", "trace:khabar"),
    )


# ============================================================================
# RelationCandidate Structure Tests
# ============================================================================

def test_relation_candidate_structure():
    """Test basic RelationCandidate structure."""
    candidate = RelationCandidate(
        candidate_id="candidate:test_001",
        slot_id="slot:test_001",
        relation_type=RelationType.ISNAD,
        anchor_trace_ids=("trace:a", "trace:b"),
        preserved_slot_trace_ids=("trace:slot",),
        rank=Rank.CANDIDATE,
        produces_meaning=False,
        produces_ifadah=False,
        produces_hukm=False,
    )

    assert candidate.candidate_id == "candidate:test_001"
    assert candidate.relation_type == RelationType.ISNAD
    assert candidate.rank == Rank.CANDIDATE


def test_relation_candidate_constitutional_prohibitions():
    """Test that RelationCandidate enforces constitutional prohibitions."""
    candidate = RelationCandidate(
        candidate_id="candidate:test",
        slot_id="slot:test",
        relation_type=RelationType.ISNAD,
        anchor_trace_ids=(),
        preserved_slot_trace_ids=(),
        rank=Rank.CANDIDATE,
    )

    # Default values enforce prohibitions
    assert not candidate.produces_meaning
    assert not candidate.produces_ifadah
    assert not candidate.produces_hukm


# ============================================================================
# build_relation_candidate Tests
# ============================================================================

@patch('dal_core.relation_candidate_builder.get_relation_operation')
def test_build_relation_candidate_nominal_basic(mock_get_operation):
    """Test building relation candidate from nominal slot."""
    # Setup mock operation
    mock_result = Mock()
    mock_result.relation_type = RelationType.ISNAD
    mock_result.anchor_ids = ("anchor:0", "anchor:1")

    mock_operation = Mock()
    mock_operation.apply = Mock(return_value=mock_result)
    mock_get_operation.return_value = mock_operation

    # Build slot
    slot = build_mock_nominal_slot()

    # Build candidate
    candidate = build_relation_candidate(slot)

    # Verify candidate structure
    assert candidate.slot_id == slot.slot_id
    assert candidate.relation_type == RelationType.ISNAD
    assert candidate.rank == Rank.CANDIDATE

    # Verify operation was called
    mock_get_operation.assert_called_once()
    mock_operation.apply.assert_called_once()


@patch('dal_core.relation_candidate_builder.get_relation_operation')
def test_build_relation_candidate_preserves_traces(mock_get_operation):
    """Test that build_relation_candidate preserves all trace IDs."""
    # Setup mock
    mock_result = Mock()
    mock_result.relation_type = RelationType.ISNAD
    mock_result.anchor_ids = ("anchor:0", "anchor:1")

    mock_operation = Mock()
    mock_operation.apply = Mock(return_value=mock_result)
    mock_get_operation.return_value = mock_operation

    # Build slot
    slot = build_mock_nominal_slot(slot_id="slot:specific_123")

    # Build candidate
    candidate = build_relation_candidate(slot)

    # Verify slot trace preserved
    assert "slot:specific_123" in candidate.preserved_slot_trace_ids

    # Verify anchor traces preserved
    assert "trace:mubtada" in candidate.anchor_trace_ids
    assert "trace:khabar" in candidate.anchor_trace_ids


@patch('dal_core.relation_candidate_builder.get_relation_operation')
def test_build_relation_candidate_constitutional_prohibitions(mock_get_operation):
    """Test that no forbidden outputs are produced."""
    # Setup mock
    mock_result = Mock()
    mock_result.relation_type = RelationType.ISNAD
    mock_result.anchor_ids = ()

    mock_operation = Mock()
    mock_operation.apply = Mock(return_value=mock_result)
    mock_get_operation.return_value = mock_operation

    # Build slot
    slot = build_mock_nominal_slot()

    # Build candidate
    candidate = build_relation_candidate(slot)

    # Verify constitutional prohibitions
    assert not candidate.produces_meaning
    assert not candidate.produces_ifadah
    assert not candidate.produces_hukm


@patch('dal_core.relation_candidate_builder.get_relation_operation')
def test_build_relation_candidate_rank_always_candidate(mock_get_operation):
    """Test that rank is always CANDIDATE (never upgraded)."""
    # Setup mock
    mock_result = Mock()
    mock_result.relation_type = RelationType.ISNAD
    mock_result.anchor_ids = ()

    mock_operation = Mock()
    mock_operation.apply = Mock(return_value=mock_result)
    mock_get_operation.return_value = mock_operation

    # Build slot
    slot = build_mock_nominal_slot()

    # Build candidate
    candidate = build_relation_candidate(slot)

    # Verify rank never upgraded
    assert candidate.rank == Rank.CANDIDATE


# ============================================================================
# Integration Tests (end-to-end chain)
# ============================================================================

@patch('dal_core.relation_candidate_builder.get_relation_operation')
def test_build_relation_candidate_complete_chain(mock_get_operation):
    """Test complete chain: slot → adapt → anchors → operation → candidate."""
    # Setup mock operation for ISNAD
    mock_result = Mock()
    mock_result.relation_type = RelationType.ISNAD
    mock_result.anchor_ids = ("anchor:entity", "anchor:transformation")

    mock_operation = Mock()
    mock_operation.apply = Mock(return_value=mock_result)
    mock_get_operation.return_value = mock_operation

    # Build nominal slot
    slot = build_mock_nominal_slot(
        slot_id="slot:nominal_complete",
        mubtada_surface="الطالبُ",
        khabar_surface="مجتهدٌ",
    )

    # Build candidate (triggers full chain)
    candidate = build_relation_candidate(slot)

    # Verify complete chain executed
    assert candidate.candidate_id.startswith("candidate:")
    assert candidate.slot_id == "slot:nominal_complete"
    assert candidate.relation_type == RelationType.ISNAD

    # Verify adapter was invoked (anchors created)
    call_args = mock_operation.apply.call_args
    anchors = call_args[0][0]  # First positional arg
    assert len(anchors) == 2  # Entity + Transformation for nominal

    # Verify traces preserved through entire chain
    assert "trace:mubtada" in candidate.anchor_trace_ids
    assert "trace:khabar" in candidate.anchor_trace_ids


# ============================================================================
# get_relation_operation Tests
# ============================================================================

def test_get_relation_operation_nominal():
    """Test that NOMINAL frame maps to ISNAD operation."""
    from dal_core.relation_candidate_builder import get_relation_operation

    operation = get_relation_operation(CompositionFrameType.NOMINAL)

    # Should return ISNAD operation
    assert hasattr(operation, 'apply')
    assert operation.relation_type == RelationType.ISNAD


def test_get_relation_operation_verbal():
    """Test that VERBAL frame maps to ISNAD operation."""
    from dal_core.relation_candidate_builder import get_relation_operation

    operation = get_relation_operation(CompositionFrameType.VERBAL)

    # Should return ISNAD operation
    assert hasattr(operation, 'apply')
    assert operation.relation_type == RelationType.ISNAD


def test_get_relation_operation_semi_sentence():
    """Test that SEMI_SENTENCE frame maps to TADMIN/TAQYID operation."""
    from dal_core.relation_candidate_builder import get_relation_operation

    operation = get_relation_operation(CompositionFrameType.SEMI_SENTENCE)

    # Should return TADMIN or TAQYID operation
    assert hasattr(operation, 'apply')
    assert operation.relation_type in (RelationType.TADMIN, RelationType.TAQYID)


def test_get_relation_operation_unsupported():
    """Test error for unsupported frame type."""
    from dal_core.relation_candidate_builder import get_relation_operation

    with pytest.raises(ValueError, match="Unsupported"):
        get_relation_operation(Mock(value="UNSUPPORTED_TYPE"))


# ============================================================================
# Error Handling Tests
# ============================================================================

@patch('dal_core.relation_candidate_builder.get_relation_operation')
def test_build_relation_candidate_operation_failure(mock_get_operation):
    """Test handling of operation failure."""
    # Setup mock to raise error
    mock_operation = Mock()
    mock_operation.apply = Mock(side_effect=RuntimeError("Operation failed"))
    mock_get_operation.return_value = mock_operation

    # Build slot
    slot = build_mock_nominal_slot()

    # Should propagate error
    with pytest.raises(RuntimeError, match="Operation failed"):
        build_relation_candidate(slot)


@patch('dal_core.relation_candidate_builder.adapt_slot_to_anchors')
def test_build_relation_candidate_adapter_failure(mock_adapt):
    """Test handling of adapter failure."""
    # Setup mock to raise error
    mock_adapt.side_effect = ValueError("Adapter failed")

    # Build slot
    slot = build_mock_nominal_slot()

    # Should propagate error
    with pytest.raises(ValueError, match="Adapter failed"):
        build_relation_candidate(slot)


# ============================================================================
# Trace Preservation Tests
# ============================================================================

@patch('dal_core.relation_candidate_builder.get_relation_operation')
def test_build_relation_candidate_preserves_all_source_traces(mock_get_operation):
    """Test that all source traces from slot are preserved."""
    # Setup mock
    mock_result = Mock()
    mock_result.relation_type = RelationType.ISNAD
    mock_result.anchor_ids = ()

    mock_operation = Mock()
    mock_operation.apply = Mock(return_value=mock_result)
    mock_get_operation.return_value = mock_operation

    # Build slot with specific trace IDs
    mubtada = build_mock_presyntax_vector(trace_id="trace:mubtada_specific")
    khabar = build_mock_presyntax_vector(trace_id="trace:khabar_specific")

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada,
        khabar_vector=khabar,
    )

    slot = RelationSlotVector(
        slot_id="slot:test",
        relation_slot_type=CompositionFrameType.NOMINAL,
        slot_geometry=geometry,
        source_trace_ids=(
            "trace:mubtada_specific",
            "trace:khabar_specific",
            "trace:frame_specific",
        ),
    )

    # Build candidate
    candidate = build_relation_candidate(slot)

    # All source traces must be in anchor_trace_ids
    assert "trace:mubtada_specific" in candidate.anchor_trace_ids
    assert "trace:khabar_specific" in candidate.anchor_trace_ids
    assert "trace:frame_specific" in candidate.anchor_trace_ids
