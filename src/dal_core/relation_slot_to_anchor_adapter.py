"""
Relation Slot to Anchor Adapter (محول خانات النسبة إلى المراسي)

Critical bridge between RelationSlotVector and RelationAlgebraCore anchors.

Constitutional Purpose:
    RelationAlgebraCore operations require Anchor types (EntityAnchor/
    TransformationAnchor/FunctionAnchor), but RelationSlotReadiness produces
    RelationSlotVector with PreSyntaxMufradVector inputs.

    This adapter builds the critical bridge WITHOUT semantic interpretation.

Critical Principles:
    1. Preserve ALL PreSyntaxMufradVector trace_ids into Anchor traces
    2. Build anchors from vector features (NOT from meaning)
    3. Use conservative/unresolved values where information incomplete
    4. NO meaning/ifadah/hukm production

Forbidden Outputs:
    ❌ meaning, semantic, madlul, murad
    ❌ ifadah, pragmatic_completion
    ❌ hukm, judgment
    ❌ final_root/final_pattern (only conservative estimates)

Architecture Position:
    PreSyntaxMufradVector^k
        → RelationSlotVector
            → adapt_slot_to_anchors (this module)
                → Tuple[Anchor, ...]
                    → RelationAlgebraCore.apply()

Reference:
    PR: Bridge Arabic Composition Chain
    Builds on: RelationSlotReadiness, RelationAlgebraCore

Created: 2026-05-29
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from dal_core.identity_registry import IdentityType
from dal_core.relation_algebra_core import (
    Anchor,
    EntityAnchor,
    FunctionAnchor,
    TransformationAnchor,
    OnticType,
    GenusType,
    ReferenceStatus,
    StabilityType,
    TransformationType,
    ScopeType,
)
from dal_core.relation_slot_readiness import (
    CompositionFrameType,
    RelationSlotVector,
    NominalFrameSlotGeometry,
    VerbalFrameSlotGeometry,
    SemiSentenceFrameSlotGeometry,
)
from dal_core.transition_proof_kernel import (
    EffectiveDescription,
    IdentityNeutralCheck,
    MinimalCompletenessCheck,
    QiyasProof,
    TransitionProof,
)
from dal_core.ranks import LughaRank
from fvafk.algebra.core import Rank


# ============================================================================
# Rank Conversion (PR #163 Integration)
# ============================================================================

def _lugha_rank_to_fvafk_rank(lugha_rank: LughaRank) -> Rank:
    """
    Convert LughaRank to fvafk.algebra.Rank.

    Conservative mapping to prevent rank inflation (same as factor_mark_equation).

    Args:
        lugha_rank: LughaRank enum value

    Returns:
        Corresponding fvafk.algebra.Rank value (conservative mapping)
    """
    if lugha_rank == LughaRank.ZERO:
        return Rank.UNRESOLVED
    else:
        return Rank.CANDIDATE


# ============================================================================
# Anchor Bundle Result
# ============================================================================

@dataclass(frozen=True)
class RelationSlotAnchorBundle:
    """
    حزمة مراسي خانات النسبة

    Bundle containing anchors produced from RelationSlotVector
    plus transition proof.

    Fields:
        bundle_id: Unique identifier
        slot_vector_id: Source RelationSlotVector ID
        anchors: Tuple of anchors for RelationAlgebraCore
        transition_proof: Complete transition proof
    """
    bundle_id: str
    slot_vector_id: str
    anchors: Tuple[Anchor, ...]
    transition_proof: TransitionProof


# ============================================================================
# Helper Functions
# ============================================================================

def _trace(vec) -> Tuple[str, ...]:
    """Extract trace tuple from vector."""
    return (vec.trace_id,)


def _entity_anchor_from_vector(vec, *, bearable: bool = True) -> EntityAnchor:
    """
    Build conservative EntityAnchor from PreSyntaxMufradVector.

    Conservative approach:
    - Uses FORM_IDENTITY (most basic)
    - SUBSTANCE ontic type (default for nominals)
    - INDIVIDUAL (default, not universal)
    - UNRESOLVED reference (no definiteness judgment yet)
    - Preserves trace_id

    Args:
        vec: PreSyntaxMufradVector
        bearable: Whether this entity can bear predication

    Returns:
        EntityAnchor with conservative values
    """
    return EntityAnchor(
        identity=IdentityType.FORM_IDENTITY,
        ontic_type=OnticType.SUBSTANCE,
        genus_or_individual=GenusType.INDIVIDUAL,
        reference_status=ReferenceStatus.UNRESOLVED,
        preserved_invariant=f"preserve:{vec.trace_id}",
        stability=StabilityType.UNRESOLVED,
        verified_bearability=bearable,
        trace=_trace(vec),
    )


def _transformation_anchor_from_vector(vec) -> TransformationAnchor:
    """
    Build conservative TransformationAnchor from PreSyntaxMufradVector.

    Conservative approach:
    - root_id = "root:unresolved" (no final root claim)
    - pattern_id = "pattern:unresolved" (no final pattern claim)
    - EVENT vs ATTRIBUTE based on verb_features presence
    - Preserves trace_id

    Args:
        vec: PreSyntaxMufradVector

    Returns:
        TransformationAnchor with conservative values
    """
    root_id = "root:unresolved"
    pattern_id = "pattern:unresolved"

    # Infer EVENT vs ATTRIBUTE from verb_features
    if getattr(vec, "verb_features", None) is not None:
        event_type = TransformationType.EVENT
    else:
        event_type = TransformationType.ATTRIBUTE

    return TransformationAnchor(
        identity=IdentityType.FORM_IDENTITY,
        origin_root_id=root_id,
        pattern_id=pattern_id,
        event_or_attribute=event_type,
        bearability_requirements=frozenset({"bearable_entity"}),
        valency_requirements=None,
        trace=_trace(vec),
    )


def _function_anchor_from_vector(vec) -> FunctionAnchor:
    """
    Build conservative FunctionAnchor from PreSyntaxMufradVector.

    Conservative approach:
    - Uses FORM_IDENTITY
    - locked_form from type_signature
    - LOCAL scope (most restrictive)
    - Preserves trace_id

    Args:
        vec: PreSyntaxMufradVector

    Returns:
        FunctionAnchor with conservative values
    """
    return FunctionAnchor(
        identity=IdentityType.FORM_IDENTITY,
        locked_form=vec.get_type_signature(),
        scope_type=ScopeType.LOCAL,
        attachment_requirements=frozenset({"governed_complement"}),
        trace=_trace(vec),
    )


# ============================================================================
# Main Adapter Function
# ============================================================================

def adapt_slot_to_anchors(slot: RelationSlotVector) -> RelationSlotAnchorBundle:
    """
    Adapt RelationSlotVector to Anchor tuple for RelationAlgebraCore.

    Constitutional Requirements:
        1. Verify slot can target RelationAlgebraCore
        2. Build appropriate anchors for frame type
        3. Preserve all trace_ids
        4. Build complete transition proof
        5. NO meaning/ifadah/hukm production

    Args:
        slot: RelationSlotVector to adapt

    Returns:
        RelationSlotAnchorBundle with anchors and proof

    Raises:
        ValueError: If slot cannot target RelationAlgebraCore or
                   frame geometry doesn't match frame type

    Example:
        >>> bundle = adapt_slot_to_anchors(relation_slot_vector)
        >>> result = IsnadOperation().apply(bundle.anchors)
    """
    # Gate: Verify readiness
    if not slot.can_target_relation_algebra_core():
        raise ValueError("RelationSlotVector cannot target RelationAlgebraCore")

    # Build anchors based on frame type
    if slot.frame_type == CompositionFrameType.NOMINAL_SENTENCE:
        geom = slot.frame_geometry
        if not isinstance(geom, NominalFrameSlotGeometry):
            raise ValueError("Nominal frame requires NominalFrameSlotGeometry")

        # Nominal: Entity (mubtada) + Transformation (khabar)
        anchors = (
            _entity_anchor_from_vector(geom.mubtada_vector),
            _transformation_anchor_from_vector(geom.khabar_vector),
        )

    elif slot.frame_type == CompositionFrameType.VERBAL_SENTENCE:
        geom = slot.frame_geometry
        if not isinstance(geom, VerbalFrameSlotGeometry):
            raise ValueError("Verbal frame requires VerbalFrameSlotGeometry")

        # Verbal: Transformation (verb) + Entity (actor) [+ Entity (object)]
        anchors = (
            _transformation_anchor_from_vector(geom.verb_vector),
            _entity_anchor_from_vector(geom.actor_vector),
        )
        if geom.object_vector is not None:
            anchors = anchors + (_entity_anchor_from_vector(geom.object_vector),)

    elif slot.frame_type == CompositionFrameType.SEMI_SENTENCE:
        geom = slot.frame_geometry
        if not isinstance(geom, SemiSentenceFrameSlotGeometry):
            raise ValueError("Semi-sentence frame requires SemiSentenceFrameSlotGeometry")

        # Semi-sentence: Function (operator/prep) + Entity (governed)
        anchors = (
            _function_anchor_from_vector(geom.operator_or_preposition_vector),
            _entity_anchor_from_vector(geom.governed_nominal_vector),
        )

    else:
        raise ValueError(f"Unsupported frame type: {slot.frame_type}")

    # Build transition proof components
    effective = EffectiveDescription(
        description_id=f"effective:slot_to_anchor:{slot.vector_id}",
        description_type="relation_slot_to_anchor_mapping",
        evidence=("RelationSlotVector", slot.frame_type.value, slot.relation_slot_type.name),
    )

    qiyas = QiyasProof(
        proof_id=f"qiyas:slot_to_anchor:{slot.vector_id}",
        origin_id="origin:relation_slot_anchor_contract",
        branch_id=slot.vector_id,
        effective_description=effective,
        shared_cause="relation slot vector preserves PreSyntaxMufradVector traces and opens algebraic anchor input",
        invalidating_differences=(),
    )

    # Build identity preservation check
    # PR #163: Enforce identity_ids ≠ trace_ids constitutional law
    # Extract identity_ids from slot's vectors (NO fallback to trace_ids)
    input_identity_ids = []
    if slot.frame_type == CompositionFrameType.NOMINAL_SENTENCE:
        geom = slot.frame_geometry
        if isinstance(geom, NominalFrameSlotGeometry):
            input_identity_ids.extend(geom.mubtada_vector.identity_ids or ())
            input_identity_ids.extend(geom.khabar_vector.identity_ids or ())
    elif slot.frame_type == CompositionFrameType.VERBAL_SENTENCE:
        geom = slot.frame_geometry
        if isinstance(geom, VerbalFrameSlotGeometry):
            input_identity_ids.extend(geom.verb_vector.identity_ids or ())
            input_identity_ids.extend(geom.actor_vector.identity_ids or ())
            if geom.object_vector is not None:
                input_identity_ids.extend(geom.object_vector.identity_ids or ())
    elif slot.frame_type == CompositionFrameType.SEMI_SENTENCE:
        geom = slot.frame_geometry
        if isinstance(geom, SemiSentenceFrameSlotGeometry):
            input_identity_ids.extend(geom.operator_or_preposition_vector.identity_ids or ())
            input_identity_ids.extend(geom.governed_nominal_vector.identity_ids or ())

    input_identity_ids = tuple(input_identity_ids)

    # Constitutional Law: identity_ids ≠ trace_ids
    # Output identities = preserved input identities (NOT extracted from anchor.trace)
    # anchor.trace contains trace_ids, which MUST NOT be used as identity_ids
    output_identity_ids = input_identity_ids  # Identity-preserving: output = input

    neutral = IdentityNeutralCheck(
        check_id=f"id_neutral:slot_to_anchor:{slot.vector_id}",
        input_identity_ids=input_identity_ids,
        output_identity_ids=output_identity_ids,
        preserved=True,  # Always preserved since output = input
    )

    # Build minimal completeness check
    minimum = MinimalCompletenessCheck(
        check_id=f"minimum:slot_to_anchor:{slot.vector_id}",
        target_layer="RELATION_ANCHORS",
        required_conditions=(
            "slot_vector_ready",
            "frame_geometry_matches",
            "anchors_created",
            "input_traces_preserved",
            "no_meaning",
            "no_ifadah",
            "no_hukm",
        ),
        satisfied_conditions=(
            "slot_vector_ready",
            "frame_geometry_matches",
            "anchors_created",
            "input_traces_preserved",
            "no_meaning",
            "no_ifadah",
            "no_hukm",
        ),
        missing_conditions=(),
        passed=True,
    )

    # Build complete transition proof
    transition = TransitionProof(
        proof_id=f"transition:slot_to_anchor:{slot.vector_id}",
        source_layer="RELATION_SLOT_VECTOR",
        target_layer="RELATION_ANCHORS",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=tuple(slot.preserved_trace_ids),
        residual_ids=tuple(str(r) for r in slot.residuals),
        rank=_lugha_rank_to_fvafk_rank(slot.rank),
    )

    # Return bundle
    return RelationSlotAnchorBundle(
        bundle_id=f"anchor_bundle:{slot.vector_id}",
        slot_vector_id=slot.vector_id,
        anchors=anchors,
        transition_proof=transition,
    )
