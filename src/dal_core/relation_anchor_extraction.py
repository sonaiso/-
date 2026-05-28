"""
Relation Anchor Extraction (استخراج مرساة النسبة)

Constitutional Bridge Layer: PreSyntaxMufradVector → AnchoredInput → RelationOperation

CRITICAL PRINCIPLE:
    This module bridges the gap between PreSyntaxMufradVector and RelationAlgebraCore
    by preserving INSTANCE identity, not just TYPE identity.

Purpose:
    Convert RelationSlotVector → Tuple[AnchoredMufradInput, ...]
    Preserve instance-level traceability for downward audit.

Constitutional Laws:
    1. لا تعديل مباشر على Anchor classes
       No direct modification to existing Anchor classes

    2. لا execution داخل RelationSlotVector
       No execution logic inside RelationSlotVector

    3. حفظ هوية النسخة لا النوع فقط
       Preserve instance identity not just type identity

    4. كل AnchoredInput يجب أن يحفظ source_vector_id
       Every AnchoredInput must preserve source_vector_id

    5. لا meaning/ifadah/hukm
       No meaning/ifadah/hukm production

Forbidden Outputs:
    ❌ meaning, semantic, madlul, murad
    ❌ ifadah, pragmatic_completion
    ❌ hukm, judgment
    ❌ final_relation (only relation_operation_proof)

Architecture Position:
    PreSyntaxMufradVector^k
        → RelationSlotVector
            → extract_anchored_inputs (THIS MODULE)
                → Tuple[AnchoredMufradInput, ...]
                    → RelationOperation.apply()
                        → RelationResultWithInstanceTrace
                            → downward_audit()

Reference:
    docs/RELATION_ANCHOR_EXTRACTION_CONSTITUTION.md (to be created)

Created: 2026-05-28
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional, Dict, Any, FrozenSet
from types import MappingProxyType

from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.relation_slot_readiness import RelationSlotVector
from dal_core.relation_algebra_core import (
    Anchor,
    EntityAnchor,
    TransformationAnchor,
    FunctionAnchor,
    RelationType,
    RelationResult,
    IdentityType,
)
from dal_core.mufrad_axes import IshtiqaqJudgment, BinaaJudgment
from dal_core.type_ids import NounTypeID, VerbTypeID, ParticleTypeID
from dal_core.foundation import Rank, ResidualSet


# ============================================================================
# Relation Side Classification
# ============================================================================

class RelationSide(Enum):
    """
    جانب النسبة (Which side of the relation?)

    For bidirectional relation tracking.
    """
    LEFT = "left"
    """Left side of relation (typically subject/entity)"""

    RIGHT = "right"
    """Right side of relation (typically predicate/attribute)"""

    CONTAINER = "container"
    """Container in TADMIN relation"""

    CONTAINED = "contained"
    """Contained in TADMIN relation"""

    BASE = "base"
    """Base in TAQYID relation"""

    RESTRICTOR = "restrictor"
    """Restrictor in TAQYID relation"""

    UNKNOWN = "unknown"
    """Unknown/unresolved side"""


# ============================================================================
# Anchored Mufrad Input (WRAPPER - not modification)
# ============================================================================

@dataclass(frozen=True)
class AnchoredMufradInput:
    """
    مدخل مفرد مُرسى (Anchored Mufrad Input)

    WRAPPER preserving instance-level identity for relational operations.

    Constitutional Law:
        This is a WRAPPER around Anchor, NOT a replacement.
        Preserves bidirectional traceability:
        - Upward: from mufrad to anchor to relation
        - Downward: from relation to anchor to mufrad

    This structure addresses the gap:
        RelationResult.preserved_identities: FrozenSet[IdentityType]  ❌ TYPE-LEVEL
        vs
        AnchoredMufradInput: instance-level ✅ with source_vector_id

    Example Problem (without this):
        زيد قائم
        - Entity: زيد (FORM_IDENTITY)
        - Transformation: قائم (FORM_IDENTITY)

        RelationResult = {FORM_IDENTITY}  ❌ Cannot distinguish which is which

    Example Solution (with this):
        AnchoredMufradInput[0]:
            anchor_instance_id = "rel_slot_123_anchor_0"
            source_vector_id = "mufrad_زيد_456"
            anchor = EntityAnchor(FORM_IDENTITY, ...)
            relation_side = LEFT

        AnchoredMufradInput[1]:
            anchor_instance_id = "rel_slot_123_anchor_1"
            source_vector_id = "mufrad_قائم_789"
            anchor = TransformationAnchor(FORM_IDENTITY, ...)
            relation_side = RIGHT

        ✅ Now we can audit: which طرف was entity, which was transformation
    """

    # Instance-level identities
    anchor_instance_id: str
    """Unique ID for this specific anchor instance (not type)"""

    source_vector_id: str
    """From PreSyntaxMufradVector.mufrad_id - which mufrad produced this anchor?"""

    source_trace_id: str
    """From PreSyntaxMufradVector.trace_id - full pipeline trace"""

    # The actual typed anchor (PRESERVED - not modified)
    anchor: EntityAnchor | TransformationAnchor | FunctionAnchor
    """The typed anchor from RelationAlgebraCore (unchanged)"""

    # Relation context
    relation_side: RelationSide
    """Which side of the relation is this anchor?"""

    # Reserved for future implementation
    reference_links: Tuple[str, ...] = ()
    """
    Reserved for ReferenceLink IDs.

    NOT IMPLEMENTED YET.

    Future: Will track pronoun references, demonstratives, relatives, etc.
    For now: empty tuple placeholder.
    """

    def __post_init__(self):
        """Validate constitutional requirements."""
        if not self.anchor_instance_id:
            raise ValueError("AnchoredMufradInput.anchor_instance_id is required")

        if not self.source_vector_id:
            raise ValueError("AnchoredMufradInput.source_vector_id is required")

        if not self.source_trace_id:
            raise ValueError("AnchoredMufradInput.source_trace_id is required")

        if self.anchor is None:
            raise ValueError("AnchoredMufradInput.anchor is required")

        # Forbidden fields check
        forbidden_fields = ['meaning', 'ifadah', 'hukm', 'murad', 'semantic']
        for field in forbidden_fields:
            if hasattr(self, field):
                raise ValueError(
                    f"AnchoredMufradInput MUST NOT contain field '{field}'"
                )


# ============================================================================
# Extended Relation Result (WRAPPER - not modification)
# ============================================================================

@dataclass(frozen=True)
class RelationResultWithInstanceTrace:
    """
    نتيجة علاقة مع أثر النسخة (Relation Result with Instance Trace)

    WRAPPER around RelationResult preserving instance-level audit trail.

    Constitutional Law:
        Preserves both:
        1. Original RelationResult (type-level identities)
        2. Instance-level audit trail (which specific anchors/vectors)

    Enables downward audit:
        RelationResultWithInstanceTrace
            → input_anchor_instance_ids
            → input_source_vector_ids
            → PreSyntaxMufradVector sources

    Does NOT produce:
        ❌ meaning
        ❌ ifadah
        ❌ hukm
    """

    # Original result (PRESERVED - not modified)
    base_result: RelationResult
    """Original RelationResult from RelationOperation.apply()"""

    # Instance-level preservation
    input_anchor_instance_ids: Tuple[str, ...]
    """Which anchor instances were inputs? (downward audit support)"""

    input_source_vector_ids: Tuple[str, ...]
    """Which PreSyntaxMufradVector sources? (downward audit support)"""

    input_source_trace_ids: Tuple[str, ...]
    """Full trace IDs from sources (downward audit support)"""

    operation_trace_id: str
    """Unique ID for this specific operation application"""

    relation_type: RelationType
    """Which relation operation was applied"""

    def __post_init__(self):
        """Validate constitutional requirements."""
        if not self.input_anchor_instance_ids:
            raise ValueError(
                "RelationResultWithInstanceTrace.input_anchor_instance_ids required"
            )

        if not self.input_source_vector_ids:
            raise ValueError(
                "RelationResultWithInstanceTrace.input_source_vector_ids required"
            )

        if len(self.input_anchor_instance_ids) != len(self.input_source_vector_ids):
            raise ValueError(
                "input_anchor_instance_ids and input_source_vector_ids must match"
            )

        if not self.operation_trace_id:
            raise ValueError(
                "RelationResultWithInstanceTrace.operation_trace_id required"
            )

        # Forbidden fields check
        forbidden_fields = ['meaning', 'ifadah', 'hukm', 'murad', 'semantic']
        for field in forbidden_fields:
            if hasattr(self, field):
                raise ValueError(
                    f"RelationResultWithInstanceTrace MUST NOT contain '{field}'"
                )

    def downward_audit(self) -> Dict[str, Any]:
        """
        تدقيق رجوعي (Downward Audit)

        Trace from relation result back to original sources.

        Returns:
            Audit trail mapping:
            {
                'anchor_instances': [list of anchor instance IDs],
                'source_vectors': [list of source vector IDs],
                'source_traces': [list of full trace IDs],
                'operation_id': operation trace ID,
                'relation_type': relation type name,
                'preserved_types': [list of preserved identity types],
                'added_loads': [list of added loads],
                'rank': rank name,
            }

        Constitutional Law:
            This audit MUST enable complete reconstruction of:
            - Which مفردات entered the relation
            - Which anchors were created
            - Which operation was applied
            - What was preserved/added
        """
        return MappingProxyType({
            'anchor_instances': list(self.input_anchor_instance_ids),
            'source_vectors': list(self.input_source_vector_ids),
            'source_traces': list(self.input_source_trace_ids),
            'operation_id': self.operation_trace_id,
            'relation_type': self.relation_type.value if hasattr(self.relation_type, 'value') else str(self.relation_type),
            'preserved_types': [str(t) for t in self.base_result.preserved_identities],
            'added_loads': list(self.base_result.added_loads),
            'rank': str(self.base_result.rank),
            'residuals_count': len(self.base_result.residuals) if hasattr(self.base_result.residuals, '__len__') else 0,
        })

    def get_preserved_type_identities(self) -> FrozenSet[IdentityType]:
        """Get type-level preserved identities from base result."""
        return self.base_result.preserved_identities

    def get_instance_count(self) -> int:
        """Get number of input instances."""
        return len(self.input_anchor_instance_ids)


# ============================================================================
# Anchor Extraction Logic (HELPER FUNCTIONS)
# ============================================================================

def _extract_anchor_from_presyntax(vec: PreSyntaxMufradVector) -> Anchor:
    """
    استخراج مرساة من شعاع المفرد

    Extract typed Anchor from PreSyntaxMufradVector.

    Decision tree:
        if ISM + jamid → EntityAnchor
        if ISM/FIIL + mushtaq → TransformationAnchor
        if HARF + mabni → FunctionAnchor

    Args:
        vec: PreSyntaxMufradVector to convert

    Returns:
        Typed Anchor (Entity/Transformation/Function)

    Raises:
        ValueError: If vector cannot be converted to anchor

    Constitutional Law:
        This extraction MUST preserve identity trace from vec.
        It does NOT add meaning/ifadah/hukm.
    """
    # TODO: Implement full extraction logic
    # For now: stub that raises NotImplementedError
    # Full implementation requires:
    # 1. Check ishtiqaq_judgment (if available)
    # 2. Check binaa_judgment (if available)
    # 3. Check type_id
    # 4. Build appropriate anchor type

    raise NotImplementedError(
        "_extract_anchor_from_presyntax not yet implemented. "
        "Requires full mapping from PreSyntaxMufradVector features to Anchor types."
    )


def _determine_relation_side(
    index: int,
    slot_vector: RelationSlotVector
) -> RelationSide:
    """
    تحديد جانب النسبة

    Determine which side of relation this input occupies.

    Args:
        index: Position in input_vectors
        slot_vector: The RelationSlotVector context

    Returns:
        RelationSide classification

    Logic:
        Based on relation_slot_type and position:
        - ISNAD: index 0 → LEFT (entity), index 1 → RIGHT (predicate)
        - TADMIN: index 0 → CONTAINER, index 1 → CONTAINED
        - TAQYID: index 0 → BASE, index 1 → RESTRICTOR
        - WASF: index 0 → BASE, index 1 → ATTRIBUTE
        - IDAFAH: index 0 → POSSESSED, index 1 → POSSESSOR
    """
    relation_type = slot_vector.relation_slot_type

    if relation_type == RelationType.ISNAD:
        return RelationSide.LEFT if index == 0 else RelationSide.RIGHT
    elif relation_type == RelationType.TADMIN:
        return RelationSide.CONTAINER if index == 0 else RelationSide.CONTAINED
    elif relation_type == RelationType.TAQYID:
        return RelationSide.BASE if index == 0 else RelationSide.RESTRICTOR
    elif relation_type in (RelationType.WASF, RelationType.IDAFAH):
        return RelationSide.BASE if index == 0 else RelationSide.RESTRICTOR
    else:
        return RelationSide.UNKNOWN


# ============================================================================
# Main Bridge Function
# ============================================================================

def extract_anchored_inputs_from_slot_vector(
    slot_vector: RelationSlotVector
) -> Tuple[AnchoredMufradInput, ...]:
    """
    استخراج مدخلات مُرساة من شعاع الخانات

    Convert RelationSlotVector → Tuple[AnchoredMufradInput, ...]

    This is the MAIN BRIDGE function between:
        RelationSlotReadiness → RelationAlgebraCore

    Args:
        slot_vector: Prepared relation slot vector

    Returns:
        Tuple of AnchoredMufradInput preserving instance identities

    Raises:
        ValueError: If slot_vector invalid or conversion fails
        NotImplementedError: If _extract_anchor_from_presyntax not ready

    Constitutional Law:
        This function MUST:
        1. Preserve every PreSyntaxMufradVector identity
        2. Generate unique anchor_instance_id for each
        3. Track source_vector_id and source_trace_id
        4. NOT produce meaning/ifadah/hukm

    Usage:
        slot_vector = RelationSlotVector(...)
        anchored_inputs = extract_anchored_inputs_from_slot_vector(slot_vector)

        # Now can pass to RelationOperation:
        # operation = IsnadOperation()
        # anchors = tuple(ai.anchor for ai in anchored_inputs)
        # base_result = operation.apply(anchors)

        # Wrap with instance trace:
        # result = RelationResultWithInstanceTrace(
        #     base_result=base_result,
        #     input_anchor_instance_ids=tuple(ai.anchor_instance_id for ai in anchored_inputs),
        #     ...
        # )
    """
    if not slot_vector.input_vectors:
        raise ValueError("RelationSlotVector.input_vectors cannot be empty")

    anchored_inputs = []

    # Generate base ID for this slot vector's anchors
    # Use vector_id if available, otherwise generate from preserved_trace_ids
    if hasattr(slot_vector, 'vector_id') and slot_vector.vector_id:
        base_id = slot_vector.vector_id
    else:
        # Fallback: use first trace_id as base
        base_id = slot_vector.preserved_trace_ids[0] if slot_vector.preserved_trace_ids else "unknown"

    for i, vec in enumerate(slot_vector.input_vectors):
        # Generate unique instance ID
        anchor_instance_id = f"{base_id}_anchor_{i}"

        # Extract typed anchor (STUB - will raise NotImplementedError)
        try:
            anchor = _extract_anchor_from_presyntax(vec)
        except NotImplementedError:
            # For now, we document the gap but allow construction
            # In production, this should fail
            anchor = None  # Will be caught by AnchoredMufradInput validation

        # Determine relation side
        relation_side = _determine_relation_side(i, slot_vector)

        # Get source identities from vec
        source_vector_id = vec.mufrad_id
        source_trace_id = getattr(vec, 'trace_id', f"trace_{vec.mufrad_id}")

        # Create anchored input
        anchored_input = AnchoredMufradInput(
            anchor_instance_id=anchor_instance_id,
            source_vector_id=source_vector_id,
            source_trace_id=source_trace_id,
            anchor=anchor,
            relation_side=relation_side,
            reference_links=()  # Empty for now - reserved for future
        )

        anchored_inputs.append(anchored_input)

    return tuple(anchored_inputs)
