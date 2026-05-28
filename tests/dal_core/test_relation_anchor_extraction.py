"""
Tests for Relation Anchor Extraction (Instance Identity Bridge)

Constitutional Tests:
    These tests verify that the bridge layer preserves instance-level identity
    and enables downward audit from relation results to source mufrad vectors.

Critical Requirements:
    1. AnchoredMufradInput preserves source_vector_id
    2. RelationResultWithInstanceTrace enables downward_audit
    3. No meaning/ifadah/hukm production
    4. Wrapper pattern (no modification to existing Anchors)
"""

import pytest
from dataclasses import FrozenInstanceError

from dal_core.relation_anchor_extraction import (
    AnchoredMufradInput,
    RelationResultWithInstanceTrace,
    RelationSide,
    extract_anchored_inputs_from_slot_vector,
    _determine_relation_side,
)
from dal_core.relation_algebra_core import (
    EntityAnchor,
    TransformationAnchor,
    RelationType,
    RelationResult,
    IdentityType,
)
from dal_core.ranks import Rank
from dal_core.residuals import ResidualSet


# ============================================================================
# Test AnchoredMufradInput
# ============================================================================

def test_anchored_mufrad_input_preserves_source_identity():
    """
    Constitutional Test: AnchoredMufradInput MUST preserve source_vector_id

    Law:
        Every anchored input must track which PreSyntaxMufradVector it came from.
    """
    # Create mock anchor
    mock_anchor = EntityAnchor(
        identity=IdentityType.FORM_IDENTITY,
        ontic_type="substance",
        genus_or_individual="individual",
        reference_status="definite",
        preserved_invariant="entity_stability",
        stability="stable",
        verified_bearability=True,
        trace=("U8", "U9", "U10")
    )

    # Create anchored input
    anchored = AnchoredMufradInput(
        anchor_instance_id="test_anchor_001",
        source_vector_id="mufrad_زيد_123",
        source_trace_id="trace_mufrad_زيد_123",
        anchor=mock_anchor,
        relation_side=RelationSide.LEFT,
        reference_links=()
    )

    # Verify preservation
    assert anchored.anchor_instance_id == "test_anchor_001"
    assert anchored.source_vector_id == "mufrad_زيد_123"
    assert anchored.source_trace_id == "trace_mufrad_زيد_123"
    assert anchored.anchor == mock_anchor
    assert anchored.relation_side == RelationSide.LEFT


def test_anchored_mufrad_input_requires_instance_id():
    """
    Constitutional Test: AnchoredMufradInput requires anchor_instance_id

    Law:
        No anchor without unique instance identifier.
    """
    mock_anchor = EntityAnchor(
        identity=IdentityType.FORM_IDENTITY,
        ontic_type="substance",
        genus_or_individual="individual",
        reference_status="definite",
        preserved_invariant="entity_stability",
        stability="stable",
        verified_bearability=True,
        trace=("U8", "U9", "U10")
    )

    with pytest.raises(ValueError, match="anchor_instance_id is required"):
        AnchoredMufradInput(
            anchor_instance_id="",  # Empty - should fail
            source_vector_id="mufrad_123",
            source_trace_id="trace_123",
            anchor=mock_anchor,
            relation_side=RelationSide.LEFT,
        )


def test_anchored_mufrad_input_requires_source_vector_id():
    """
    Constitutional Test: AnchoredMufradInput requires source_vector_id

    Law:
        No anchor without source mufrad identifier.
    """
    mock_anchor = EntityAnchor(
        identity=IdentityType.FORM_IDENTITY,
        ontic_type="substance",
        genus_or_individual="individual",
        reference_status="definite",
        preserved_invariant="entity_stability",
        stability="stable",
        verified_bearability=True,
        trace=("U8", "U9", "U10")
    )

    with pytest.raises(ValueError, match="source_vector_id is required"):
        AnchoredMufradInput(
            anchor_instance_id="anchor_001",
            source_vector_id="",  # Empty - should fail
            source_trace_id="trace_123",
            anchor=mock_anchor,
            relation_side=RelationSide.LEFT,
        )


def test_anchored_mufrad_input_is_frozen():
    """
    Constitutional Test: AnchoredMufradInput must be immutable

    Law:
        All algebra structures must be frozen after construction.
    """
    mock_anchor = EntityAnchor(
        identity=IdentityType.FORM_IDENTITY,
        ontic_type="substance",
        genus_or_individual="individual",
        reference_status="definite",
        preserved_invariant="entity_stability",
        stability="stable",
        verified_bearability=True,
        trace=("U8", "U9", "U10")
    )

    anchored = AnchoredMufradInput(
        anchor_instance_id="test_anchor_001",
        source_vector_id="mufrad_زيد_123",
        source_trace_id="trace_123",
        anchor=mock_anchor,
        relation_side=RelationSide.LEFT,
    )

    # Attempt mutation should fail
    with pytest.raises(FrozenInstanceError):
        anchored.source_vector_id = "different_id"


# ============================================================================
# Test RelationResultWithInstanceTrace
# ============================================================================

def test_relation_result_with_instance_trace_preserves_base_result():
    """
    Constitutional Test: Wrapper must preserve original RelationResult

    Law:
        RelationResultWithInstanceTrace is WRAPPER not replacement.
    """
    # Create base result
    base_result = RelationResult(
        preserved_identities=frozenset({IdentityType.FORM_IDENTITY}),
        added_loads=frozenset({"predication_load"}),
        residuals=ResidualSet(),
        rank=Rank.CANDIDATE,
        evidence=("operation_trace",)
    )

    # Wrap with instance trace
    result_with_trace = RelationResultWithInstanceTrace(
        base_result=base_result,
        input_anchor_instance_ids=("anchor_001", "anchor_002"),
        input_source_vector_ids=("mufrad_زيد_123", "mufrad_قائم_456"),
        input_source_trace_ids=("trace_123", "trace_456"),
        operation_trace_id="operation_789",
        relation_type=RelationType.ISNAD,
    )

    # Verify base result preserved
    assert result_with_trace.base_result == base_result
    assert result_with_trace.base_result.preserved_identities == frozenset({IdentityType.FORM_IDENTITY})
    assert result_with_trace.base_result.rank == Rank.CANDIDATE


def test_relation_result_downward_audit():
    """
    Constitutional Test: downward_audit must trace to original sources

    Law:
        Every relation result must enable reconstruction of:
        - Which مفردات entered
        - Which anchors were created
        - Which operation was applied

    This is the CRITICAL test proving instance-level preservation.
    """
    base_result = RelationResult(
        preserved_identities=frozenset({IdentityType.FORM_IDENTITY}),
        added_loads=frozenset({"predication_load"}),
        residuals=ResidualSet(),
        rank=Rank.CANDIDATE,
        evidence=("operation_evidence",)
    )

    result_with_trace = RelationResultWithInstanceTrace(
        base_result=base_result,
        input_anchor_instance_ids=("anchor_زيد_001", "anchor_قائم_002"),
        input_source_vector_ids=("mufrad_زيد_123", "mufrad_قائم_456"),
        input_source_trace_ids=("trace_زيد_123", "trace_قائم_456"),
        operation_trace_id="isnad_operation_789",
        relation_type=RelationType.ISNAD,
    )

    # Perform downward audit
    audit = result_with_trace.downward_audit()

    # Verify complete traceability
    assert audit['anchor_instances'] == ["anchor_زيد_001", "anchor_قائم_002"]
    assert audit['source_vectors'] == ["mufrad_زيد_123", "mufrad_قائم_456"]
    assert audit['source_traces'] == ["trace_زيد_123", "trace_قائم_456"]
    assert audit['operation_id'] == "isnad_operation_789"
    assert audit['relation_type'] == "ISNAD"
    assert IdentityType.FORM_IDENTITY.name in audit['preserved_types'] or 'FORM_IDENTITY' in str(audit['preserved_types'])

    # CRITICAL: Can distinguish which input was which
    # This solves the problem: "زيد قائم both FORM_IDENTITY → cannot distinguish"
    assert len(audit['anchor_instances']) == 2
    assert audit['anchor_instances'][0] != audit['anchor_instances'][1]
    assert audit['source_vectors'][0] != audit['source_vectors'][1]


def test_relation_result_prevents_instance_loss():
    """
    Constitutional Test: Instance identities must not be lost

    Law:
        Even if both inputs have same TYPE identity (FORM_IDENTITY),
        INSTANCE identities must remain distinct.

    This test proves the gap is closed:
        Before: {FORM_IDENTITY} → cannot distinguish زيد from قائم
        After: anchor_instances + source_vectors → full distinction
    """
    base_result = RelationResult(
        preserved_identities=frozenset({IdentityType.FORM_IDENTITY}),  # Same type!
        added_loads=frozenset({"predication_load"}),
        residuals=ResidualSet(),
        rank=Rank.CANDIDATE,
        evidence=("operation_evidence",)
    )

    result_with_trace = RelationResultWithInstanceTrace(
        base_result=base_result,
        input_anchor_instance_ids=("anchor_entity_001", "anchor_transformation_002"),
        input_source_vector_ids=("mufrad_entity_123", "mufrad_transformation_456"),
        input_source_trace_ids=("trace_entity", "trace_transformation"),
        operation_trace_id="operation_789",
        relation_type=RelationType.ISNAD,
    )

    # Both have FORM_IDENTITY type
    assert IdentityType.FORM_IDENTITY in result_with_trace.base_result.preserved_identities

    # But instance-level distinction preserved
    audit = result_with_trace.downward_audit()
    assert len(set(audit['anchor_instances'])) == 2  # Distinct instances
    assert len(set(audit['source_vectors'])) == 2  # Distinct sources

    # Can identify: which was entity, which was transformation
    assert "entity" in audit['anchor_instances'][0]
    assert "transformation" in audit['anchor_instances'][1]


def test_relation_result_forbids_meaning():
    """
    Constitutional Test: RelationResultWithInstanceTrace MUST NOT contain meaning

    Law:
        No meaning/ifadah/hukm fields allowed.
    """
    base_result = RelationResult(
        preserved_identities=frozenset({IdentityType.FORM_IDENTITY}),
        added_loads=frozenset(),
        residuals=ResidualSet(),
        rank=Rank.CANDIDATE,
        evidence=()
    )

    # This should succeed (no forbidden fields)
    result = RelationResultWithInstanceTrace(
        base_result=base_result,
        input_anchor_instance_ids=("a1",),
        input_source_vector_ids=("v1",),
        input_source_trace_ids=("t1",),
        operation_trace_id="op1",
        relation_type=RelationType.ISNAD,
    )

    # Verify no forbidden fields exist
    assert not hasattr(result, 'meaning')
    assert not hasattr(result, 'ifadah')
    assert not hasattr(result, 'hukm')
    assert not hasattr(result, 'murad')


# ============================================================================
# Test Relation Side Determination
# ============================================================================

def test_determine_relation_side_isnad():
    """
    Test: ISNAD relation side classification

    ISNAD: index 0 → LEFT (entity), index 1 → RIGHT (predicate)
    """
    from dal_core.relation_slot_readiness import RelationSlotVector, CompositionFrameType
    from unittest.mock import Mock

    # Mock RelationSlotVector
    slot_vector = Mock(spec=RelationSlotVector)
    slot_vector.relation_slot_type = RelationType.ISNAD

    assert _determine_relation_side(0, slot_vector) == RelationSide.LEFT
    assert _determine_relation_side(1, slot_vector) == RelationSide.RIGHT


def test_determine_relation_side_tadmin():
    """
    Test: TADMIN relation side classification

    TADMIN: index 0 → CONTAINER, index 1 → CONTAINED
    """
    from unittest.mock import Mock

    slot_vector = Mock()
    slot_vector.relation_slot_type = RelationType.TADMIN

    assert _determine_relation_side(0, slot_vector) == RelationSide.CONTAINER
    assert _determine_relation_side(1, slot_vector) == RelationSide.CONTAINED


def test_determine_relation_side_taqyid():
    """
    Test: TAQYID relation side classification

    TAQYID: index 0 → BASE, index 1 → RESTRICTOR
    """
    from unittest.mock import Mock

    slot_vector = Mock()
    slot_vector.relation_slot_type = RelationType.TAQYID

    assert _determine_relation_side(0, slot_vector) == RelationSide.BASE
    assert _determine_relation_side(1, slot_vector) == RelationSide.RESTRICTOR


# ============================================================================
# Integration Test (stub - will fail until _extract_anchor implemented)
# ============================================================================

def test_extract_anchored_inputs_requires_implementation():
    """
    Integration Test: extract_anchored_inputs requires full implementation

    This test documents the current gap:
        _extract_anchor_from_presyntax is NOT IMPLEMENTED YET

    When implemented, this test should be updated to verify full flow:
        RelationSlotVector → Tuple[AnchoredMufradInput, ...]
    """
    from unittest.mock import Mock

    # Mock RelationSlotVector
    slot_vector = Mock()
    slot_vector.input_vectors = []  # Empty will raise ValueError

    # Should fail due to empty input_vectors
    with pytest.raises(ValueError, match="cannot be empty"):
        extract_anchored_inputs_from_slot_vector(slot_vector)

    # When input_vectors non-empty, will fail due to NotImplementedError in _extract_anchor
    # This is EXPECTED and DOCUMENTED behavior until full implementation


# ============================================================================
# Constitutional Completeness Tests
# ============================================================================

def test_no_direct_anchor_modification():
    """
    Constitutional Test: Verify Anchors not modified

    Law:
        AnchoredMufradInput is WRAPPER, not modification of Anchor classes.

    This test verifies the safe design decision:
        - No fields added to EntityAnchor/TransformationAnchor/FunctionAnchor
        - Wrapper pattern used instead
    """
    # Original anchor structure
    original_anchor = EntityAnchor(
        identity=IdentityType.FORM_IDENTITY,
        ontic_type="substance",
        genus_or_individual="individual",
        reference_status="definite",
        preserved_invariant="stability",
        stability="stable",
        verified_bearability=True,
        trace=("U8", "U9", "U10")
    )

    # Wrap without modifying
    wrapped = AnchoredMufradInput(
        anchor_instance_id="instance_001",
        source_vector_id="vector_123",
        source_trace_id="trace_123",
        anchor=original_anchor,
        relation_side=RelationSide.LEFT,
    )

    # Original anchor unchanged
    assert wrapped.anchor == original_anchor
    assert wrapped.anchor.identity == IdentityType.FORM_IDENTITY

    # Instance fields stored in wrapper, not anchor
    assert hasattr(wrapped, 'anchor_instance_id')
    assert hasattr(wrapped, 'source_vector_id')
    assert not hasattr(original_anchor, 'anchor_instance_id')
    assert not hasattr(original_anchor, 'source_vector_id')


def test_wrapper_count_matches_input_count():
    """
    Constitutional Test: Instance count integrity

    Law:
        Number of AnchoredMufradInput instances must equal
        number of input PreSyntaxMufradVector instances.

    No instance loss, no instance duplication.
    """
    base_result = RelationResult(
        preserved_identities=frozenset({IdentityType.FORM_IDENTITY}),
        added_loads=frozenset(),
        residuals=ResidualSet(),
        rank=Rank.CANDIDATE,
        evidence=()
    )

    # 3 input instances
    result = RelationResultWithInstanceTrace(
        base_result=base_result,
        input_anchor_instance_ids=("a1", "a2", "a3"),
        input_source_vector_ids=("v1", "v2", "v3"),
        input_source_trace_ids=("t1", "t2", "t3"),
        operation_trace_id="op1",
        relation_type=RelationType.ISNAD,
    )

    # Verify count preservation
    assert result.get_instance_count() == 3
    assert len(result.input_anchor_instance_ids) == 3
    assert len(result.input_source_vector_ids) == 3
    assert len(result.input_source_trace_ids) == 3


def test_mismatched_counts_rejected():
    """
    Constitutional Test: Reject mismatched instance counts

    Law:
        input_anchor_instance_ids and input_source_vector_ids must match.
    """
    base_result = RelationResult(
        preserved_identities=frozenset({IdentityType.FORM_IDENTITY}),
        added_loads=frozenset(),
        residuals=ResidualSet(),
        rank=Rank.CANDIDATE,
        evidence=()
    )

    # Mismatched counts should fail
    with pytest.raises(ValueError, match="must match"):
        RelationResultWithInstanceTrace(
            base_result=base_result,
            input_anchor_instance_ids=("a1", "a2"),  # 2 items
            input_source_vector_ids=("v1",),  # 1 item - MISMATCH
            input_source_trace_ids=("t1",),
            operation_trace_id="op1",
            relation_type=RelationType.ISNAD,
        )
