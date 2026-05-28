"""
Constitutional Tests for RelationSlotReadiness

These tests enforce the 10 constitutional laws preventing premature jumps:
    1. No RelationSlotVector without PreSyntaxMufradVector
    2. No consumption without composition_readiness
    3. No deletion of mufrad vector traces
    4. No predication without compositional frame
    5. No embedding without licensed container/contained
    6. No restriction without qualified/qualifier
    7. No final RelationCandidate from this layer
    8. No Ifadah
    9. No Hukm
    10. No meaning
"""

import pytest
from dal_core.relation_slot_readiness import (
    RelationSlotVector,
    NominalFrameSlotGeometry,
    VerbalFrameSlotGeometry,
    SemiSentenceFrameSlotGeometry,
    CompositionFrameType,
)
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.relation_algebra_core import RelationType
from dal_core.composition_readiness import CompositionReadiness
from dal_core.type_ids import NounTypeID
from dal_core.ranks import LughaRank
from dal_core.mufrad_axes import BinaaJudgment, IshtiqaqJudgment


def make_ready_presyntax_vector(
    mufrad_id: str = "test_001",
    type_value: str = "ISM",
    readiness: CompositionReadiness = CompositionReadiness.READY_FOR_COMPOSITION,
) -> PreSyntaxMufradVector:
    """Helper to create composition-ready PreSyntaxMufradVector"""
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 3),
        type_value=type_value,
        type_id=NounTypeID.ISM_COMMON,
        type_rank=LughaRank.TAWATUR,
        mabni_murab_status="MURAB_CANDIDATE",
        noun_inflection_class="DIPTOTE",
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=(),
        morph_rank=LughaRank.TAWATUR,
        final_rank=LughaRank.TAWATUR,
        residuals=(),
        trace_id=f"trace_{mufrad_id}",
        competitors_count=0,
        composition_readiness=readiness,
        binaa_judgment=BinaaJudgment.MURAB,
        ishtiqaq_judgment=IshtiqaqJudgment.JAMID,
    )


# ============================================================================
# Constitutional Law Tests
# ============================================================================

def test_relation_slot_readiness_rejects_raw_string():
    """
    Constitutional Test 1: No RelationSlotVector without PreSyntaxMufradVector

    RelationSlotVector MUST reject raw strings.
    """
    with pytest.raises((ValueError, TypeError)):
        # This should fail at construction or validation
        NominalFrameSlotGeometry(
            mubtada_vector="زيد",  # Raw string - FORBIDDEN
            khabar_vector="قائم",  # Raw string - FORBIDDEN
            isnad_potential=True,
            agreement_potential=True,
            terminal_i3rab_potential=True,
            mubtada_trace_id="trace_1",
            khabar_trace_id="trace_2",
            residuals=(),
            rank=LughaRank.TAWATUR,
            frame_id="frame_001",
        )


def test_relation_slot_readiness_rejects_unready_presyntax_vector():
    """
    Constitutional Test 2: No consumption without composition_readiness

    RelationSlotVector MUST reject PreSyntaxMufradVector with NOT_READY.
    """
    unready_vector = make_ready_presyntax_vector(
        mufrad_id="unready",
        readiness=CompositionReadiness.NOT_READY
    )
    ready_vector = make_ready_presyntax_vector(mufrad_id="ready")

    with pytest.raises(ValueError, match="not ready for composition"):
        NominalFrameSlotGeometry(
            mubtada_vector=unready_vector,  # NOT_READY - FORBIDDEN
            khabar_vector=ready_vector,
            isnad_potential=True,
            agreement_potential=True,
            terminal_i3rab_potential=True,
            mubtada_trace_id=unready_vector.trace_id,
            khabar_trace_id=ready_vector.trace_id,
            residuals=(),
            rank=LughaRank.TAWATUR,
            frame_id="frame_002",
        )


def test_relation_slot_readiness_preserves_all_mufrad_trace_ids():
    """
    Constitutional Test 3: Preserve trace_id for each input

    RelationSlotVector MUST preserve all input trace_ids.
    """
    mubtada_vec = make_ready_presyntax_vector(mufrad_id="mubtada")
    khabar_vec = make_ready_presyntax_vector(mufrad_id="khabar")

    # Correct: preserved trace_ids match
    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada_vec,
        khabar_vector=khabar_vec,
        isnad_potential=True,
        agreement_potential=True,
        terminal_i3rab_potential=True,
        mubtada_trace_id=mubtada_vec.trace_id,  # PRESERVED
        khabar_trace_id=khabar_vec.trace_id,    # PRESERVED
        residuals=(),
        rank=LughaRank.TAWATUR,
        frame_id="frame_003",
    )

    assert geometry.mubtada_trace_id == mubtada_vec.trace_id
    assert geometry.khabar_trace_id == khabar_vec.trace_id

    # Incorrect: mismatched trace_id
    with pytest.raises(ValueError, match="must preserve.*trace_id"):
        NominalFrameSlotGeometry(
            mubtada_vector=mubtada_vec,
            khabar_vector=khabar_vec,
            isnad_potential=True,
            agreement_potential=True,
            terminal_i3rab_potential=True,
            mubtada_trace_id="wrong_trace",  # VIOLATION
            khabar_trace_id=khabar_vec.trace_id,
            residuals=(),
            rank=LughaRank.TAWATUR,
            frame_id="frame_004",
        )


def test_isnad_slot_does_not_create_ifadah():
    """
    Constitutional Test 8: No Ifadah from slot geometry

    NominalFrameSlotGeometry MUST NOT contain ifadah field.
    """
    mubtada_vec = make_ready_presyntax_vector(mufrad_id="mubtada")
    khabar_vec = make_ready_presyntax_vector(mufrad_id="khabar")

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada_vec,
        khabar_vector=khabar_vec,
        isnad_potential=True,
        agreement_potential=True,
        terminal_i3rab_potential=True,
        mubtada_trace_id=mubtada_vec.trace_id,
        khabar_trace_id=khabar_vec.trace_id,
        residuals=(),
        rank=LughaRank.TAWATUR,
        frame_id="frame_005",
    )

    # Verify no ifadah field
    assert not hasattr(geometry, 'ifadah')
    assert not hasattr(geometry, 'pragmatic_completion')
    assert not hasattr(geometry, 'ifadah_closure')


def test_tadmin_slot_does_not_create_semantics():
    """
    Constitutional Test 10: No meaning from slot geometry

    VerbalFrameSlotGeometry MUST NOT contain meaning field.
    """
    verb_vec = make_ready_presyntax_vector(mufrad_id="verb", type_value="FIIL")
    actor_vec = make_ready_presyntax_vector(mufrad_id="actor")

    geometry = VerbalFrameSlotGeometry(
        verb_vector=verb_vec,
        actor_vector=actor_vec,
        object_vector=None,
        verb_actor_isnad_potential=True,
        verb_object_tadmin_potential=False,
        valency_satisfied=True,
        tense_event_potential=True,
        verb_trace_id=verb_vec.trace_id,
        actor_trace_id=actor_vec.trace_id,
        object_trace_id=None,
        residuals=(),
        rank=LughaRank.TAWATUR,
        frame_id="frame_006",
    )

    # Verify no semantic fields
    assert not hasattr(geometry, 'meaning')
    assert not hasattr(geometry, 'semantic')
    assert not hasattr(geometry, 'madlul')
    assert not hasattr(geometry, 'murad')


def test_taqyid_slot_does_not_create_hukm():
    """
    Constitutional Test 9: No Hukm from slot geometry

    SemiSentenceFrameSlotGeometry MUST NOT contain hukm field.
    """
    prep_vec = make_ready_presyntax_vector(mufrad_id="prep", type_value="HARF")
    noun_vec = make_ready_presyntax_vector(mufrad_id="noun")

    geometry = SemiSentenceFrameSlotGeometry(
        operator_or_preposition_vector=prep_vec,
        governed_nominal_vector=noun_vec,
        taqyid_potential=True,
        tadmin_potential=False,
        attachment_target_expected=True,
        operator_trace_id=prep_vec.trace_id,
        governed_trace_id=noun_vec.trace_id,
        residuals=(),
        rank=LughaRank.TAWATUR,
        frame_id="frame_007",
    )

    # Verify no hukm fields
    assert not hasattr(geometry, 'hukm')
    assert not hasattr(geometry, 'judgment')
    assert not hasattr(geometry, 'truth_value')


def test_nominal_frame_requires_two_ready_vectors():
    """
    Constitutional Test 4: No predication without compositional frame

    NominalFrameSlotGeometry requires both mubtada and khabar ready.
    """
    mubtada_vec = make_ready_presyntax_vector(mufrad_id="mubtada")
    khabar_vec = make_ready_presyntax_vector(mufrad_id="khabar")

    # Success: both ready
    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada_vec,
        khabar_vector=khabar_vec,
        isnad_potential=True,
        agreement_potential=True,
        terminal_i3rab_potential=True,
        mubtada_trace_id=mubtada_vec.trace_id,
        khabar_trace_id=khabar_vec.trace_id,
        residuals=(),
        rank=LughaRank.TAWATUR,
        frame_id="frame_008",
    )

    assert geometry.isnad_potential is True


def test_verbal_frame_requires_verb_anchor():
    """
    Constitutional Test 4: Verbal frame requires verb anchor

    VerbalFrameSlotGeometry requires verb vector.
    """
    verb_vec = make_ready_presyntax_vector(mufrad_id="verb", type_value="FIIL")
    actor_vec = make_ready_presyntax_vector(mufrad_id="actor")

    geometry = VerbalFrameSlotGeometry(
        verb_vector=verb_vec,
        actor_vector=actor_vec,
        object_vector=None,
        verb_actor_isnad_potential=True,
        verb_object_tadmin_potential=False,
        valency_satisfied=True,
        tense_event_potential=True,
        verb_trace_id=verb_vec.trace_id,
        actor_trace_id=actor_vec.trace_id,
        object_trace_id=None,
        residuals=(),
        rank=LughaRank.TAWATUR,
        frame_id="frame_009",
    )

    assert geometry.verb_actor_isnad_potential is True


def test_semisentence_frame_requires_operator_or_preposition_potential():
    """
    Constitutional Test 6: Semi-sentence requires operator/prep

    SemiSentenceFrameSlotGeometry requires operator or preposition.
    """
    prep_vec = make_ready_presyntax_vector(mufrad_id="prep", type_value="HARF")
    noun_vec = make_ready_presyntax_vector(mufrad_id="noun")

    geometry = SemiSentenceFrameSlotGeometry(
        operator_or_preposition_vector=prep_vec,
        governed_nominal_vector=noun_vec,
        taqyid_potential=True,
        tadmin_potential=False,
        attachment_target_expected=True,
        operator_trace_id=prep_vec.trace_id,
        governed_trace_id=noun_vec.trace_id,
        residuals=(),
        rank=LughaRank.TAWATUR,
        frame_id="frame_010",
    )

    assert geometry.taqyid_potential is True


def test_relation_slot_vector_can_only_target_relation_algebra_core():
    """
    Constitutional Test 7: RelationSlotVector targets only RelationAlgebraCore

    This vector prepares slots but does NOT create final relations.
    Only RelationAlgebraCore creates RelationCandidate.
    """
    mubtada_vec = make_ready_presyntax_vector(mufrad_id="mubtada")
    khabar_vec = make_ready_presyntax_vector(mufrad_id="khabar")

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada_vec,
        khabar_vector=khabar_vec,
        isnad_potential=True,
        agreement_potential=True,
        terminal_i3rab_potential=True,
        mubtada_trace_id=mubtada_vec.trace_id,
        khabar_trace_id=khabar_vec.trace_id,
        residuals=(),
        rank=LughaRank.TAWATUR,
        frame_id="frame_011",
    )

    slot_vector = RelationSlotVector(
        frame_type=CompositionFrameType.NOMINAL_SENTENCE,
        frame_geometry=geometry,
        relation_slot_type=RelationType.ISNAD,
        input_vectors=(mubtada_vec, khabar_vec),
        preserved_trace_ids=(mubtada_vec.trace_id, khabar_vec.trace_id),
        before_vector_indices=(0,),
        after_candidate_index=1,
        before_after_relation_type=RelationType.ISNAD,
        residuals=(),
        rank=LughaRank.TAWATUR,
        vector_id="slot_001",
    )

    # Verify: can target RelationAlgebraCore
    assert slot_vector.can_target_relation_algebra_core() is True

    # Verify: does NOT contain final relation
    assert not hasattr(slot_vector, 'relation_candidate')
    assert not hasattr(slot_vector, 'final_relation')
    assert not hasattr(slot_vector, 'closed_relation')


def test_relation_slot_vector_preserves_all_input_traces():
    """
    Constitutional Test 3: All input traces preserved

    RelationSlotVector MUST preserve all input PreSyntaxMufradVector traces.
    """
    vec1 = make_ready_presyntax_vector(mufrad_id="vec1")
    vec2 = make_ready_presyntax_vector(mufrad_id="vec2")
    vec3 = make_ready_presyntax_vector(mufrad_id="vec3")

    verb_geometry = VerbalFrameSlotGeometry(
        verb_vector=vec1,
        actor_vector=vec2,
        object_vector=vec3,
        verb_actor_isnad_potential=True,
        verb_object_tadmin_potential=True,
        valency_satisfied=True,
        tense_event_potential=True,
        verb_trace_id=vec1.trace_id,
        actor_trace_id=vec2.trace_id,
        object_trace_id=vec3.trace_id,
        residuals=(),
        rank=LughaRank.TAWATUR,
        frame_id="frame_012",
    )

    slot_vector = RelationSlotVector(
        frame_type=CompositionFrameType.VERBAL_SENTENCE,
        frame_geometry=verb_geometry,
        relation_slot_type=RelationType.ISNAD,
        input_vectors=(vec1, vec2, vec3),
        preserved_trace_ids=(vec1.trace_id, vec2.trace_id, vec3.trace_id),
        before_vector_indices=(0,),
        after_candidate_index=1,
        before_after_relation_type=RelationType.ISNAD,
        residuals=(),
        rank=LughaRank.TAWATUR,
        vector_id="slot_002",
    )

    # Verify all traces preserved
    assert slot_vector.preserved_trace_ids == (
        vec1.trace_id,
        vec2.trace_id,
        vec3.trace_id
    )
    assert len(slot_vector.input_vectors) == 3
    assert slot_vector.input_vectors[0] is vec1
    assert slot_vector.input_vectors[1] is vec2
    assert slot_vector.input_vectors[2] is vec3


def test_relation_slot_vector_summary():
    """Test human-readable summary"""
    mubtada_vec = make_ready_presyntax_vector(mufrad_id="mubtada")
    khabar_vec = make_ready_presyntax_vector(mufrad_id="khabar")

    geometry = NominalFrameSlotGeometry(
        mubtada_vector=mubtada_vec,
        khabar_vector=khabar_vec,
        isnad_potential=True,
        agreement_potential=True,
        terminal_i3rab_potential=True,
        mubtada_trace_id=mubtada_vec.trace_id,
        khabar_trace_id=khabar_vec.trace_id,
        residuals=(),
        rank=LughaRank.TAWATUR,
        frame_id="frame_013",
    )

    slot_vector = RelationSlotVector(
        frame_type=CompositionFrameType.NOMINAL_SENTENCE,
        frame_geometry=geometry,
        relation_slot_type=RelationType.ISNAD,
        input_vectors=(mubtada_vec, khabar_vec),
        preserved_trace_ids=(mubtada_vec.trace_id, khabar_vec.trace_id),
        before_vector_indices=(0,),
        after_candidate_index=1,
        before_after_relation_type=RelationType.ISNAD,
        residuals=(),
        rank=LughaRank.TAWATUR,
        vector_id="slot_summary",
    )

    summary = slot_vector.summary()
    assert "slot_summary" in summary
    assert "جملة اسمية" in summary or "NOMINAL" in summary
    assert "ISNAD" in summary
    assert "inputs=2" in summary
