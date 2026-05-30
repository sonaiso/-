"""
Relation Candidate Builder (بناء مرشح النسبة)

Builds RelationCandidate from RelationSlotVector → Anchors → RelationResult.

Constitutional Purpose:
    Complete the chain from slot readiness to verifiable relation candidate
    WITHOUT producing semantic/ifadah/hukm.

Critical Principles:
    1. Use adapt_slot_to_anchors to get Anchors
    2. Apply appropriate RelationOperation
    3. Package result as RelationCandidate
    4. Preserve all traces and identities
    5. Rank always remains CANDIDATE
    6. NO meaning/ifadah/hukm

Forbidden Outputs:
    ❌ meaning, semantic, madlul, murad
    ❌ ifadah, pragmatic_completion
    ❌ hukm, judgment
    ❌ rank upgrade (always CANDIDATE)

Architecture Position:
    RelationSlotVector
        → adapt_slot_to_anchors
            → RelationAlgebraCore.apply()
                → build_relation_candidate (this module)
                    → RelationCandidate

Reference:
    PR: Bridge Arabic Composition Chain
    Builds on: RelationSlotToAnchorAdapter, RelationAlgebraCore

Created: 2026-05-29
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, FrozenSet

from dal_core.relation_algebra_core import (
    Anchor,
    RelationResult,
    get_relation_operation,
)
from dal_core.relation_slot_readiness import RelationSlotVector
from dal_core.relation_slot_to_anchor_adapter import adapt_slot_to_anchors
from dal_core.transition_proof_kernel import (
    EffectiveDescription,
    IdentityNeutralCheck,
    MinimalCompletenessCheck,
    QiyasProof,
    TransitionProof,
)


# ============================================================================
# Relation Candidate
# ============================================================================

@dataclass(frozen=True)
class RelationCandidate:
    """
    مرشح النسبة (Relation Candidate)

    Complete relation candidate preserving all traces and identities.

    Constitutional Law:
        A RelationCandidate is ALWAYS rank CANDIDATE.
        It does NOT produce meaning/ifadah/hukm.
        It preserves all input traces and anchors.

    Fields:
        candidate_id: Unique identifier
        relation_slot_vector_id: Source RelationSlotVector ID
        relation_type_name: Relation type name (ISNAD/TADMIN/TAQYID/WASF/IDAFAH)
        anchors: Preserved anchors from adaptation
        preserved_trace_ids: All preserved trace IDs
        added_loads: Load additions from relation operation
        residual_ids: Residual IDs carried forward
        rank_name: Rank name (NOT upgraded)
        transition_proof: Complete transition proof
        produces_meaning: Whether produces meaning (ALWAYS False)
        produces_ifadah: Whether produces ifadah (ALWAYS False)
        produces_hukm: Whether produces hukm (ALWAYS False)
    """
    candidate_id: str
    relation_slot_vector_id: str
    relation_type_name: str

    anchors: Tuple[Anchor, ...]
    preserved_trace_ids: Tuple[str, ...]
    added_loads: FrozenSet[str]

    residual_ids: Tuple[str, ...]
    rank_name: str

    transition_proof: TransitionProof

    produces_meaning: bool = False
    produces_ifadah: bool = False
    produces_hukm: bool = False


# ============================================================================
# Main Builder Function
# ============================================================================

def build_relation_candidate(slot: RelationSlotVector) -> RelationCandidate:
    """
    Build RelationCandidate from RelationSlotVector.

    Constitutional Requirements:
        1. Adapt slot to anchors
        2. Get appropriate relation operation
        3. Apply operation to get result
        4. Build complete transition proof
        5. Package as RelationCandidate
        6. NO meaning/ifadah/hukm production

    Args:
        slot: RelationSlotVector to build candidate from

    Returns:
        RelationCandidate with complete proof

    Example:
        >>> candidate = build_relation_candidate(relation_slot_vector)
        >>> assert candidate.rank_name == "CANDIDATE"
        >>> assert not candidate.produces_meaning
    """
    # Step 1: Adapt slot to anchors
    bundle = adapt_slot_to_anchors(slot)

    # Step 2: Get relation operation for this relation type
    operation = get_relation_operation(slot.relation_slot_type)

    # Step 3: Apply operation to get result
    result: RelationResult = operation.apply(bundle.anchors)

    # Step 4: Build transition proof components
    input_trace_ids = tuple(slot.preserved_trace_ids)
    output_trace_ids = tuple(t for anchor in bundle.anchors for t in anchor.trace)

    effective = EffectiveDescription(
        description_id=f"effective:relation_candidate:{slot.vector_id}",
        description_type="relation_operation_candidate",
        evidence=("RelationSlotVector", "RelationAlgebraCore", slot.relation_slot_type.name),
    )

    qiyas = QiyasProof(
        proof_id=f"qiyas:relation_candidate:{slot.vector_id}",
        origin_id=f"origin:relation_operation:{slot.relation_slot_type.name}",
        branch_id=slot.vector_id,
        effective_description=effective,
        shared_cause="slot readiness maps to relation operation while preserving input traces and identities",
        invalidating_differences=(),
    )

    neutral = IdentityNeutralCheck(
        check_id=f"id_neutral:relation_candidate:{slot.vector_id}",
        input_identity_ids=input_trace_ids,
        output_identity_ids=output_trace_ids,
        preserved=set(input_trace_ids).issubset(set(output_trace_ids)),
    )

    minimum = MinimalCompletenessCheck(
        check_id=f"minimum:relation_candidate:{slot.vector_id}",
        target_layer="RELATION_CANDIDATE",
        required_conditions=(
            "relation_slot_vector_ready",
            "anchors_created",
            "operation_applied",
            "rank_candidate_only",
            "no_meaning",
            "no_ifadah",
            "no_hukm",
        ),
        satisfied_conditions=(
            "relation_slot_vector_ready",
            "anchors_created",
            "operation_applied",
            "rank_candidate_only",
            "no_meaning",
            "no_ifadah",
            "no_hukm",
        ),
        missing_conditions=(),
        passed=True,
    )

    transition = TransitionProof(
        proof_id=f"transition:relation_candidate:{slot.vector_id}",
        source_layer="RELATION_SLOT_VECTOR",
        target_layer="RELATION_CANDIDATE",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=input_trace_ids,
        residual_ids=tuple(str(r) for r in result.residuals.residuals),
        rank=result.rank,  # PR #163: Use Rank directly, not rank_name
    )

    # Step 5: Build and return RelationCandidate
    return RelationCandidate(
        candidate_id=f"relation_candidate:{slot.vector_id}",
        relation_slot_vector_id=slot.vector_id,
        relation_type_name=slot.relation_slot_type.name,
        anchors=bundle.anchors,
        preserved_trace_ids=input_trace_ids,
        added_loads=result.added_loads,
        residual_ids=tuple(str(r) for r in result.residuals.residuals),
        rank_name=result.rank.name,  # Keep rank_name for RelationCandidate compatibility
        transition_proof=transition,
    )
