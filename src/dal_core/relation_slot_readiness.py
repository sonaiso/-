"""
Relation Slot Readiness (جاهزية خانات النسبة)

Constitutional Bridge Layer between PreSyntaxMufradVector and RelationAlgebraCore.

CRITICAL PRINCIPLE:
    This layer PRESERVES PreSyntaxMufradVector identity.
    It prepares relation slots but does NOT create final relations.
    It does NOT produce meaning, ifadah, or hukm.

Purpose:
    Bridge PreSyntaxMufradVector → RelationAlgebraCore

    Prepares composition slot geometry for:
    - Nominal sentences (الجملة الاسمية)
    - Verbal sentences (الجملة الفعلية)
    - Semi-sentences (شبه الجملة)

Constitutional Laws:
    1. لا RelationSlotVector بلا PreSyntaxMufradVector
       No RelationSlotVector without PreSyntaxMufradVector

    2. لا استهلاك لمن لا يسمح composition_readiness باستهلاكه
       No consumption without composition_readiness permission

    3. لا حذف لشعاع المفرد؛ يجب حفظ trace_id لكل مدخل
       No deletion of mufrad vector; must preserve trace_id for each input

    4. لا نسبة إسنادية بلا إطار تركيبي
       No predication without compositional frame

    5. لا نسبة تضمينية بلا حاوية/محمول مرخص
       No embedding without licensed container/contained

    6. لا نسبة تقييدية بلا مقيد ومقيد به مرشحين
       No restriction without qualified/qualifier candidates

    7. لا RelationCandidate نهائي من هذه الطبقة
       No final RelationCandidate from this layer
       (Only RelationAlgebraCore produces RelationCandidate)

    8. لا Ifadah - No ifadah
    9. لا Hukm - No hukm
    10. لا meaning - No meaning

Forbidden Outputs:
    ❌ meaning, semantic, madlul, murad
    ❌ ifadah, pragmatic_completion
    ❌ hukm, judgment
    ❌ final_relation (only relation_slot_readiness)
    ❌ case_effect (only case_sign_potential allowed)

Architecture Position:
    PreSyntaxMufradVector
        → RelationSlotReadiness (this module)
            → RelationAlgebraCore
                → RelationCandidate
                    → Ifadah (U₁₃+)
                        → Hukm (U₁₄+)

Reference:
    docs/RELATION_SLOT_READINESS_CONSTITUTION.md

PR: RELATION-SLOT-READINESS
Created: 2026-05-28
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional, FrozenSet

from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.relation_algebra_core import RelationType
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual


# ============================================================================
# Frame Type Classification
# ============================================================================

class CompositionFrameType(Enum):
    """
    إطار التركيب (Composition Frame Type)

    Three fundamental Arabic sentence frame types.
    """
    NOMINAL_SENTENCE = "جملة اسمية"
    """Nominal sentence (مبتدأ + خبر)"""

    VERBAL_SENTENCE = "جملة فعلية"
    """Verbal sentence (فعل + فاعل + ...)"""

    SEMI_SENTENCE = "شبه جملة"
    """Semi-sentence (prepositional/adverbial phrase)"""


# ============================================================================
# Slot Geometries for Each Frame Type
# ============================================================================

@dataclass(frozen=True)
class NominalFrameSlotGeometry:
    """
    هندسة خانات الجملة الاسمية

    Slot geometry for nominal sentence composition.

    This prepares ISNAD readiness between mubtada and khabar,
    but does NOT produce final relation.

    Example: زيدٌ قائمٌ
        - mubtada_vector: PreSyntaxMufradVector for "زيد"
        - khabar_vector: PreSyntaxMufradVector for "قائم"
        - isnad_potential: True (both ready)
        - But NOT yet ISNAD relation (awaits RelationAlgebraCore)

    Forbidden:
        ❌ mubtada_final (only mubtada_candidate_slot)
        ❌ khabar_final (only khabar_candidate_slot)
        ❌ meaning
        ❌ ifadah
    """

    # Preserved input vectors
    mubtada_vector: PreSyntaxMufradVector
    """Preserved PreSyntaxMufradVector for topic candidate"""

    khabar_vector: PreSyntaxMufradVector
    """Preserved PreSyntaxMufradVector for predicate candidate"""

    # Slot readiness
    isnad_potential: bool
    """Whether ISNAD relation is potentially applicable"""

    agreement_potential: bool
    """Whether agreement conditions are potentially satisfiable"""

    terminal_i3rab_potential: bool
    """Whether terminal i'rab is potentially applicable"""

    # Preserved traces
    mubtada_trace_id: str
    """Preserved trace_id from mubtada_vector"""

    khabar_trace_id: str
    """Preserved trace_id from khabar_vector"""

    # Governance
    residuals: Tuple[Residual, ...]
    """Unresolved residuals from slot preparation"""

    rank: LughaRank
    """Weakest rank between inputs"""

    frame_id: str
    """Unique identifier for this frame geometry"""

    def __post_init__(self):
        """Validate constitutional laws"""
        # Law 1: Require PreSyntaxMufradVector
        if not isinstance(self.mubtada_vector, PreSyntaxMufradVector):
            raise ValueError("mubtada_vector must be PreSyntaxMufradVector")
        if not isinstance(self.khabar_vector, PreSyntaxMufradVector):
            raise ValueError("khabar_vector must be PreSyntaxMufradVector")

        # Law 2: Require composition readiness
        if not self.mubtada_vector.allows_operator_consumption():
            raise ValueError(
                f"mubtada_vector not ready for composition: "
                f"readiness={self.mubtada_vector.composition_readiness}"
            )
        if not self.khabar_vector.allows_operator_consumption():
            raise ValueError(
                f"khabar_vector not ready for composition: "
                f"readiness={self.khabar_vector.composition_readiness}"
            )

        # Law 3: Require preserved trace_ids
        if self.mubtada_trace_id != self.mubtada_vector.trace_id:
            raise ValueError("mubtada_trace_id must preserve mubtada_vector.trace_id")
        if self.khabar_trace_id != self.khabar_vector.trace_id:
            raise ValueError("khabar_trace_id must preserve khabar_vector.trace_id")

        # Check for forbidden fields
        forbidden_fields = [
            'mubtada_final', 'khabar_final',
            'meaning', 'semantic', 'madlul', 'murad',
            'ifadah', 'hukm', 'judgment',
            'relation_candidate', 'final_relation'
        ]
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        violations = field_names.intersection(forbidden_fields)
        if violations:
            raise ValueError(
                f"NominalFrameSlotGeometry contains forbidden fields: {violations}"
            )


@dataclass(frozen=True)
class VerbalFrameSlotGeometry:
    """
    هندسة خانات الجملة الفعلية

    Slot geometry for verbal sentence composition.

    This prepares ISNAD readiness between verb and actor,
    and optional TADMIN/TAQYID for object/complements.

    Example: كَتَبَ زيدٌ رسالةً
        - verb_vector: PreSyntaxMufradVector for "كتب"
        - actor_vector: PreSyntaxMufradVector for "زيد"
        - object_vector: PreSyntaxMufradVector for "رسالة"
        - But NOT yet final faail/mafool roles

    Forbidden:
        ❌ faail_final (only actor_candidate_slot)
        ❌ mafool_final (only object_candidate_slot)
        ❌ meaning
        ❌ ifadah
    """

    # Preserved input vectors
    verb_vector: PreSyntaxMufradVector
    """Preserved PreSyntaxMufradVector for verb"""

    actor_vector: PreSyntaxMufradVector
    """Preserved PreSyntaxMufradVector for actor candidate"""

    object_vector: Optional[PreSyntaxMufradVector]
    """Optional PreSyntaxMufradVector for object candidate"""

    # Slot readiness
    verb_actor_isnad_potential: bool
    """Whether verb-actor ISNAD is potentially applicable"""

    verb_object_tadmin_potential: bool
    """Whether verb-object TADMIN is potentially applicable"""

    valency_satisfied: bool
    """Whether verb valency requirements are satisfied"""

    tense_event_potential: bool
    """Whether tense/event structure is potentially complete"""

    # Preserved traces
    verb_trace_id: str
    actor_trace_id: str
    object_trace_id: Optional[str]

    # Governance
    residuals: Tuple[Residual, ...]
    rank: LughaRank
    frame_id: str

    def __post_init__(self):
        """Validate constitutional laws"""
        # Law 1: Require PreSyntaxMufradVector
        if not isinstance(self.verb_vector, PreSyntaxMufradVector):
            raise ValueError("verb_vector must be PreSyntaxMufradVector")
        if not isinstance(self.actor_vector, PreSyntaxMufradVector):
            raise ValueError("actor_vector must be PreSyntaxMufradVector")
        if self.object_vector is not None:
            if not isinstance(self.object_vector, PreSyntaxMufradVector):
                raise ValueError("object_vector must be PreSyntaxMufradVector or None")

        # Law 2: Require composition readiness
        if not self.verb_vector.allows_operator_consumption():
            raise ValueError("verb_vector not ready for composition")
        if not self.actor_vector.allows_operator_consumption():
            raise ValueError("actor_vector not ready for composition")
        if self.object_vector is not None:
            if not self.object_vector.allows_operator_consumption():
                raise ValueError("object_vector not ready for composition")

        # Law 3: Require preserved trace_ids
        if self.verb_trace_id != self.verb_vector.trace_id:
            raise ValueError("verb_trace_id must preserve verb_vector.trace_id")
        if self.actor_trace_id != self.actor_vector.trace_id:
            raise ValueError("actor_trace_id must preserve actor_vector.trace_id")
        if self.object_vector is not None:
            if self.object_trace_id != self.object_vector.trace_id:
                raise ValueError("object_trace_id must preserve object_vector.trace_id")

        # Check for forbidden fields
        forbidden_fields = [
            'faail_final', 'mafool_final',
            'meaning', 'semantic', 'madlul', 'murad',
            'ifadah', 'hukm', 'judgment'
        ]
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        violations = field_names.intersection(forbidden_fields)
        if violations:
            raise ValueError(
                f"VerbalFrameSlotGeometry contains forbidden fields: {violations}"
            )


@dataclass(frozen=True)
class SemiSentenceFrameSlotGeometry:
    """
    هندسة خانات شبه الجملة

    Slot geometry for semi-sentence (prepositional/adverbial phrase).

    This prepares TAQYID or TADMIN readiness,
    but does NOT produce final attachment.

    Example: في البيتِ
        - operator_vector: PreSyntaxMufradVector for "في"
        - governed_vector: PreSyntaxMufradVector for "البيت"
        - But NOT yet final متعلق role

    Forbidden:
        ❌ mutaalliq_final (only attachment_candidate)
        ❌ khabar_final
        ❌ haal_final
        ❌ meaning
        ❌ ifadah
    """

    # Preserved input vectors
    operator_or_preposition_vector: PreSyntaxMufradVector
    """Preserved PreSyntaxMufradVector for operator/preposition"""

    governed_nominal_vector: PreSyntaxMufradVector
    """Preserved PreSyntaxMufradVector for governed nominal"""

    # Slot readiness
    taqyid_potential: bool
    """Whether TAQYID (restriction) is potentially applicable"""

    tadmin_potential: bool
    """Whether TADMIN (embedding) is potentially applicable"""

    attachment_target_expected: bool
    """Whether attachment target is expected (not yet identified)"""

    # Preserved traces
    operator_trace_id: str
    governed_trace_id: str

    # Governance
    residuals: Tuple[Residual, ...]
    rank: LughaRank
    frame_id: str

    def __post_init__(self):
        """Validate constitutional laws"""
        # Law 1: Require PreSyntaxMufradVector
        if not isinstance(self.operator_or_preposition_vector, PreSyntaxMufradVector):
            raise ValueError("operator_or_preposition_vector must be PreSyntaxMufradVector")
        if not isinstance(self.governed_nominal_vector, PreSyntaxMufradVector):
            raise ValueError("governed_nominal_vector must be PreSyntaxMufradVector")

        # Law 2: Require composition readiness
        if not self.operator_or_preposition_vector.allows_operator_consumption():
            raise ValueError("operator_or_preposition_vector not ready")
        if not self.governed_nominal_vector.allows_operator_consumption():
            raise ValueError("governed_nominal_vector not ready")

        # Law 3: Require preserved trace_ids
        if self.operator_trace_id != self.operator_or_preposition_vector.trace_id:
            raise ValueError("operator_trace_id must preserve vector trace_id")
        if self.governed_trace_id != self.governed_nominal_vector.trace_id:
            raise ValueError("governed_trace_id must preserve vector trace_id")

        # Check for forbidden fields
        forbidden_fields = [
            'mutaalliq_final', 'khabar_final', 'haal_final',
            'meaning', 'semantic', 'madlul', 'murad',
            'ifadah', 'hukm', 'judgment'
        ]
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        violations = field_names.intersection(forbidden_fields)
        if violations:
            raise ValueError(
                f"SemiSentenceFrameSlotGeometry contains forbidden fields: {violations}"
            )


# ============================================================================
# Unified Relation Slot Vector
# ============================================================================

@dataclass(frozen=True)
class RelationSlotVector:
    """
    شعاع خانات النسبة (Relation Slot Vector)

    Unified container for relation slot readiness.

    This vector:
    - PRESERVES all PreSyntaxMufradVector traces
    - PREPARES relation slots for RelationAlgebraCore
    - Does NOT create final relations
    - Does NOT produce meaning/ifadah/hukm

    Constitutional Law:
        This is the ONLY permitted input to RelationAlgebraCore.
        RelationAlgebraCore MUST NOT accept raw PreSyntaxMufradVector.

    Architecture:
        PreSyntaxMufradVector^k
            → RelationSlotVector (this structure)
                → RelationAlgebraCore.apply()
                    → RelationCandidate
    """

    # Frame identification
    frame_type: CompositionFrameType
    """Type of composition frame"""

    frame_geometry: NominalFrameSlotGeometry | VerbalFrameSlotGeometry | SemiSentenceFrameSlotGeometry
    """Typed slot geometry for this frame"""

    # Relation type readiness
    relation_slot_type: RelationType
    """Relation type this slot prepares for (ISNAD/TADMIN/TAQYID/WASF/IDAFAH)"""

    # Preserved input vectors (flattened for access)
    input_vectors: Tuple[PreSyntaxMufradVector, ...]
    """All input PreSyntaxMufradVector instances (preserved)"""

    preserved_trace_ids: Tuple[str, ...]
    """All preserved trace_ids from inputs"""

    # Before-after relation tracking
    before_vector_indices: Tuple[int, ...]
    """Indices of input_vectors representing 'before' state"""

    after_candidate_index: Optional[int]
    """Index of input_vector representing 'after' state (if applicable)"""

    before_after_relation_type: Optional[RelationType]
    """Relation type between before and after (if applicable)"""

    # Governance
    residuals: Tuple[Residual, ...]
    rank: LughaRank
    vector_id: str

    def __post_init__(self):
        """Validate constitutional laws"""
        # Law 1: Require at least one PreSyntaxMufradVector
        if len(self.input_vectors) == 0:
            raise ValueError("RelationSlotVector requires at least one PreSyntaxMufradVector")

        # Verify all inputs are PreSyntaxMufradVector
        for i, vec in enumerate(self.input_vectors):
            if not isinstance(vec, PreSyntaxMufradVector):
                raise ValueError(f"input_vectors[{i}] must be PreSyntaxMufradVector")

        # Law 2: All inputs must allow composition
        for i, vec in enumerate(self.input_vectors):
            if not vec.allows_operator_consumption():
                raise ValueError(
                    f"input_vectors[{i}] not ready: "
                    f"readiness={vec.composition_readiness}"
                )

        # Law 3: Preserved trace_ids must match
        actual_traces = tuple(vec.trace_id for vec in self.input_vectors)
        if self.preserved_trace_ids != actual_traces:
            raise ValueError(
                f"preserved_trace_ids {self.preserved_trace_ids} "
                f"must match input trace_ids {actual_traces}"
            )

        # Check for forbidden fields
        forbidden_fields = [
            'meaning', 'semantic', 'madlul', 'murad',
            'ifadah', 'hukm', 'judgment',
            'final_relation', 'relation_candidate'
        ]
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        violations = field_names.intersection(forbidden_fields)
        if violations:
            raise ValueError(
                f"RelationSlotVector contains forbidden fields: {violations}"
            )

    def can_target_relation_algebra_core(self) -> bool:
        """
        Check if this vector is ready to target RelationAlgebraCore.

        Returns:
            True if all constitutional gates pass
        """
        # Gate 1: All input vectors must be ready
        if not all(vec.allows_operator_consumption() for vec in self.input_vectors):
            return False

        # Gate 2: Frame geometry must match frame type
        if self.frame_type == CompositionFrameType.NOMINAL_SENTENCE:
            if not isinstance(self.frame_geometry, NominalFrameSlotGeometry):
                return False
        elif self.frame_type == CompositionFrameType.VERBAL_SENTENCE:
            if not isinstance(self.frame_geometry, VerbalFrameSlotGeometry):
                return False
        elif self.frame_type == CompositionFrameType.SEMI_SENTENCE:
            if not isinstance(self.frame_geometry, SemiSentenceFrameSlotGeometry):
                return False

        # Gate 3: Relation type must be one of the five core types
        if self.relation_slot_type not in RelationType:
            return False

        # Gate 4: No blocking residuals
        from dal_core.residuals import has_blocking_residuals
        if has_blocking_residuals(self.residuals):
            return False

        return True

    def summary(self) -> str:
        """Human-readable summary"""
        num_inputs = len(self.input_vectors)
        return (
            f"RelationSlotVector[{self.vector_id}]: "
            f"frame={self.frame_type.value}, "
            f"relation={self.relation_slot_type.name}, "
            f"inputs={num_inputs}, "
            f"rank={self.rank.name if hasattr(self.rank, 'name') else self.rank}"
        )
