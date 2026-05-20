"""
Tests for Sentence Frame Proof (برهان إطار الجملة)

Critical tests ensuring:
1. Frame candidates built only from PreSyntaxMufradVector (not tokens)
2. No semantic/meaning/murad fields in any frame type
3. No final syntax roles (faail, mafool, mubtada, khabar)
4. No case effects (marfoo_by, mansub_by...)
5. Rank ceiling theorem enforced (frame_rank ≤ min(constituent_ranks))
6. Residual inheritance enforced (all constituent residuals inherited)
7. Frame types correctly identified
8. Operators not applied (frames prepare for operators, don't apply them)
"""

import pytest
from dal_core.sentence_frame import (
    SentenceFrameCandidate,
    NominalFrameCandidate,
    VerbalFrameCandidate,
    ParticleLedFrameCandidate,
    FragmentFrameCandidate,
    UnresolvedFrameCandidate,
    FrameType,
    calculate_frame_rank,
    collect_inherited_residuals,
)
from dal_core.frame_builder import FrameBuilder, build_sentence_frames
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.type_ids import NounTypeID, VerbTypeID, ParticleTypeID
from dal_core.ranks import LughaRank
from dal_core.mufrad_axes import BinaaJudgment, IshtiqaqJudgment
from dal_core.residuals import Residual, ResidualType, ResidualSeverity
from dal_core.evidence import Evidence
from dal_core.composition_readiness import CompositionReadiness
from dal_core.morph_features import CandidateStatus


# Test fixtures
def make_test_noun_vector(
    mufrad_id: str = "noun1",
    readiness: CompositionReadiness = CompositionReadiness.READY_FOR_COMPOSITION,
    rank: LughaRank = LughaRank.SAMA,
    residuals: tuple = (),
) -> PreSyntaxMufradVector:
    """Create test noun vector"""
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 10),
        type_value="ISM",
        type_id=NounTypeID.ISM_COMMON,
        type_rank=rank,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,  # Using actual enum value
        noun_inflection_class=None,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=(),
        morph_rank=rank,
        final_rank=rank,
        residuals=residuals,
        trace_id="test_trace",
        competitors_count=0,
        composition_readiness=readiness,
        # PR-F: ready vectors used in frame-builder tests must have
        # resolved mufrad axes; otherwise the 5th gate (correctly) blocks
        # operator consumption and the frame builder rejects the frame.
        binaa_judgment=BinaaJudgment.MUERAB,
        ishtiqaq_judgment=IshtiqaqJudgment.JAMID,
    )


def make_test_verb_vector(
    mufrad_id: str = "verb1",
    readiness: CompositionReadiness = CompositionReadiness.READY_FOR_COMPOSITION,
    rank: LughaRank = LughaRank.SAMA,
) -> PreSyntaxMufradVector:
    """Create test verb vector"""
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 10),
        type_value="FIIL",
        type_id=VerbTypeID.FIIL_MADI,
        type_rank=rank,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,  # Using actual enum value
        noun_inflection_class=None,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=(),
        morph_rank=rank,
        final_rank=rank,
        residuals=(),
        trace_id="test_trace",
        competitors_count=0,
        composition_readiness=readiness,
        binaa_judgment=BinaaJudgment.MABNI,
        ishtiqaq_judgment=IshtiqaqJudgment.NOT_APPLICABLE,
    )


def make_test_particle_vector(
    mufrad_id: str = "particle1",
    particle_type: ParticleTypeID = ParticleTypeID.HARF_NASIKH_INNA,
    readiness: CompositionReadiness = CompositionReadiness.READY_FOR_COMPOSITION,
    rank: LughaRank = LughaRank.SAMA,
) -> PreSyntaxMufradVector:
    """Create test particle vector"""
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 10),
        type_value="HARF",
        type_id=particle_type,
        type_rank=rank,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,  # Using actual enum value
        noun_inflection_class=None,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=(),
        morph_rank=rank,
        final_rank=rank,
        residuals=(),
        trace_id="test_trace",
        competitors_count=0,
        composition_readiness=readiness,
        binaa_judgment=BinaaJudgment.MABNI,
        ishtiqaq_judgment=IshtiqaqJudgment.NOT_APPLICABLE,
    )


class TestFrameForbiddenFields:
    """Test that frames have NO forbidden fields"""

    def test_sentence_frame_has_no_meaning_fields(self):
        """SentenceFrameCandidate must NOT have semantic fields"""
        noun1 = make_test_noun_vector("noun1")
        noun2 = make_test_noun_vector("noun2")

        frame = NominalFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.NOMINAL,
            constituents=(noun1, noun2),
            frame_rank=LughaRank.SAMA,
            inherited_residuals=(),
            frame_specific_residuals=(),
            trace_id="test_trace",
            lead_noun_index=0,
        )

        # Verify no semantic fields
        assert not hasattr(frame, 'meaning')
        assert not hasattr(frame, 'semantic')
        assert not hasattr(frame, 'murad')
        assert not hasattr(frame, 'madlul')
        assert not hasattr(frame, 'haqiqa')
        assert not hasattr(frame, 'majaz')

    def test_sentence_frame_has_no_syntax_role_fields(self):
        """SentenceFrameCandidate must NOT have syntax role fields"""
        noun1 = make_test_noun_vector("noun1")
        noun2 = make_test_noun_vector("noun2")

        frame = NominalFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.NOMINAL,
            constituents=(noun1, noun2),
            frame_rank=LughaRank.SAMA,
            inherited_residuals=(),
            frame_specific_residuals=(),
            trace_id="test_trace",
            lead_noun_index=0,
        )

        # Verify no syntax role fields
        assert not hasattr(frame, 'faail')
        assert not hasattr(frame, 'mafool')
        assert not hasattr(frame, 'mubtada')
        assert not hasattr(frame, 'khabar')

    def test_sentence_frame_has_no_case_effect_fields(self):
        """SentenceFrameCandidate must NOT have case effect fields"""
        verb = make_test_verb_vector("verb1")
        noun = make_test_noun_vector("noun1")

        frame = VerbalFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.VERBAL,
            constituents=(verb, noun),
            frame_rank=LughaRank.SAMA,
            inherited_residuals=(),
            frame_specific_residuals=(),
            trace_id="test_trace",
            verb_index=0,
        )

        # Verify no case effect fields
        assert not hasattr(frame, 'case_effect')
        assert not hasattr(frame, 'marfoo_by')
        assert not hasattr(frame, 'mansub_by')
        assert not hasattr(frame, 'majroor_by')
        assert not hasattr(frame, 'majzum_by')

    def test_sentence_frame_has_no_operator_governance_fields(self):
        """SentenceFrameCandidate must NOT have operator governance fields"""
        particle = make_test_particle_vector("particle1")
        noun = make_test_noun_vector("noun1")

        frame = ParticleLedFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.PARTICLE_LED,
            constituents=(particle, noun),
            frame_rank=LughaRank.SAMA,
            inherited_residuals=(),
            frame_specific_residuals=(),
            trace_id="test_trace",
            particle_index=0,
            particle_operator_potential=None,
        )

        # Verify no operator governance fields
        assert not hasattr(frame, 'governed_by_operator')
        assert not hasattr(frame, 'operator_id')
        assert not hasattr(frame, 'relation_type')


class TestRankCeilingTheorem:
    """Test Theorem 5: Rank ceiling - frame rank cannot exceed min constituent rank"""

    def test_frame_rank_equals_min_constituent_rank(self):
        """Frame rank must equal minimum of constituent ranks"""
        noun1 = make_test_noun_vector("noun1", rank=LughaRank.SAMA)
        noun2 = make_test_noun_vector("noun2", rank=LughaRank.QIYAS)  # Lower rank

        frame = NominalFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.NOMINAL,
            constituents=(noun1, noun2),
            frame_rank=LughaRank.QIYAS,  # Should be min
            inherited_residuals=(),
            frame_specific_residuals=(),
            trace_id="test_trace",
            lead_noun_index=0,
        )

        assert frame.frame_rank == LughaRank.QIYAS

    def test_frame_rank_violation_raises_error(self):
        """Frame rank higher than min constituent rank should raise error"""
        noun1 = make_test_noun_vector("noun1", rank=LughaRank.QIYAS)  # Lower rank
        noun2 = make_test_noun_vector("noun2", rank=LughaRank.FORM)   # Even lower

        with pytest.raises(ValueError, match="Rank ceiling violated"):
            NominalFrameCandidate(
                frame_id="test_frame",
                frame_type=FrameType.NOMINAL,
                constituents=(noun1, noun2),
                frame_rank=LughaRank.SAMA,  # Higher than min (FORM)
                inherited_residuals=(),
                frame_specific_residuals=(),
                trace_id="test_trace",
                lead_noun_index=0,
            )

    def test_calculate_frame_rank_returns_minimum(self):
        """calculate_frame_rank should return minimum constituent rank"""
        noun1 = make_test_noun_vector("noun1", rank=LughaRank.SAMA)      # 3
        noun2 = make_test_noun_vector("noun2", rank=LughaRank.QIYAS)     # 2
        noun3 = make_test_noun_vector("noun3", rank=LughaRank.FORM)      # 1

        rank = calculate_frame_rank((noun1, noun2, noun3))
        assert rank == LughaRank.FORM  # Lowest


class TestResidualInheritance:
    """Test Theorem 6: Residual inheritance - all constituent residuals inherited"""

    def test_frame_inherits_all_constituent_residuals(self):
        """Frame must inherit ALL residuals from constituents"""
        residual1 = Residual(
            type=ResidualType.ROOT_UNRESOLVED,  # Using actual field name
            severity=ResidualSeverity.WARNING,
            message="Test residual 1",  # Using actual field name
        )
        residual2 = Residual(
            type=ResidualType.NOT_ATTESTED,
            severity=ResidualSeverity.WARNING,
            message="Test residual 2",
        )

        noun1 = make_test_noun_vector("noun1", residuals=(residual1,))
        noun2 = make_test_noun_vector("noun2", residuals=(residual2,))

        inherited = collect_inherited_residuals((noun1, noun2))
        assert len(inherited) == 2
        assert residual1 in inherited
        assert residual2 in inherited

    def test_frame_preserves_inherited_residuals(self):
        """Frame constructed with inherited residuals preserves them"""
        residual1 = Residual(
            type=ResidualType.ROOT_UNRESOLVED,  # Using actual field name
            severity=ResidualSeverity.WARNING,
            message="Test residual",  # Using actual field name
        )

        noun1 = make_test_noun_vector("noun1", residuals=(residual1,))
        noun2 = make_test_noun_vector("noun2")

        frame = NominalFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.NOMINAL,
            constituents=(noun1, noun2),
            frame_rank=LughaRank.SAMA,
            inherited_residuals=(residual1,),
            frame_specific_residuals=(),
            trace_id="test_trace",
            lead_noun_index=0,
        )

        all_residuals = frame.get_all_residuals()
        assert residual1 in all_residuals


class TestNominalFrameCandidate:
    """Test nominal frame candidate identification"""

    def test_nominal_frame_requires_ism_lead(self):
        """Nominal frame must have ISM as lead constituent"""
        noun1 = make_test_noun_vector("noun1")
        noun2 = make_test_noun_vector("noun2")

        frame = NominalFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.NOMINAL,
            constituents=(noun1, noun2),
            frame_rank=LughaRank.SAMA,
            inherited_residuals=(),
            frame_specific_residuals=(),
            trace_id="test_trace",
            lead_noun_index=0,
        )

        assert frame.frame_type == FrameType.NOMINAL
        assert frame.lead_noun_index == 0
        assert isinstance(frame.constituents[0].type_id, NounTypeID)

    def test_nominal_frame_rejects_non_ism_lead(self):
        """Nominal frame should reject non-ISM lead"""
        verb = make_test_verb_vector("verb1")
        noun = make_test_noun_vector("noun1")

        with pytest.raises(ValueError, match="must be ISM"):
            NominalFrameCandidate(
                frame_id="test_frame",
                frame_type=FrameType.NOMINAL,
                constituents=(verb, noun),
                frame_rank=LughaRank.SAMA,
                inherited_residuals=(),
                frame_specific_residuals=(),
                trace_id="test_trace",
                lead_noun_index=0,
            )


class TestVerbalFrameCandidate:
    """Test verbal frame candidate identification"""

    def test_verbal_frame_requires_fiil(self):
        """Verbal frame must have FIIL constituent"""
        verb = make_test_verb_vector("verb1")
        noun = make_test_noun_vector("noun1")

        frame = VerbalFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.VERBAL,
            constituents=(verb, noun),
            frame_rank=LughaRank.SAMA,
            inherited_residuals=(),
            frame_specific_residuals=(),
            trace_id="test_trace",
            verb_index=0,
        )

        assert frame.frame_type == FrameType.VERBAL
        assert frame.verb_index == 0
        assert isinstance(frame.constituents[0].type_id, VerbTypeID)

    def test_verbal_frame_rejects_non_fiil_verb(self):
        """Verbal frame should reject non-FIIL at verb_index"""
        noun1 = make_test_noun_vector("noun1")
        noun2 = make_test_noun_vector("noun2")

        with pytest.raises(ValueError, match="must be FIIL"):
            VerbalFrameCandidate(
                frame_id="test_frame",
                frame_type=FrameType.VERBAL,
                constituents=(noun1, noun2),
                frame_rank=LughaRank.SAMA,
                inherited_residuals=(),
                frame_specific_residuals=(),
                trace_id="test_trace",
                verb_index=0,
            )


class TestParticleLedFrameCandidate:
    """Test particle-led frame candidate identification"""

    def test_particle_led_frame_requires_harf(self):
        """Particle-led frame must have HARF constituent"""
        particle = make_test_particle_vector("particle1")
        noun = make_test_noun_vector("noun1")

        frame = ParticleLedFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.PARTICLE_LED,
            constituents=(particle, noun),
            frame_rank=LughaRank.SAMA,
            inherited_residuals=(),
            frame_specific_residuals=(),
            trace_id="test_trace",
            particle_index=0,
            particle_operator_potential=None,
        )

        assert frame.frame_type == FrameType.PARTICLE_LED
        assert frame.particle_index == 0
        assert isinstance(frame.constituents[0].type_id, ParticleTypeID)

    def test_particle_led_frame_rejects_non_harf_particle(self):
        """Particle-led frame should reject non-HARF at particle_index"""
        noun1 = make_test_noun_vector("noun1")
        noun2 = make_test_noun_vector("noun2")

        with pytest.raises(ValueError, match="must be HARF"):
            ParticleLedFrameCandidate(
                frame_id="test_frame",
                frame_type=FrameType.PARTICLE_LED,
                constituents=(noun1, noun2),
                frame_rank=LughaRank.SAMA,
                inherited_residuals=(),
                frame_specific_residuals=(),
                trace_id="test_trace",
                particle_index=0,
                particle_operator_potential=None,
            )


class TestFragmentFrameCandidate:
    """Test fragment frame candidate identification"""

    def test_fragment_frame_single_constituent(self):
        """Single constituent creates fragment"""
        noun = make_test_noun_vector("noun1")

        frame = FragmentFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.FRAGMENT,
            constituents=(noun,),
            frame_rank=LughaRank.SAMA,
            inherited_residuals=(),
            frame_specific_residuals=(),
            trace_id="test_trace",
            fragment_reason="single_ISM",
        )

        assert frame.frame_type == FrameType.FRAGMENT
        assert frame.fragment_reason == "single_ISM"


class TestUnresolvedFrameCandidate:
    """Test unresolved frame candidate"""

    def test_unresolved_frame_has_competing_types(self):
        """Unresolved frame must have competing frame types"""
        noun = make_test_noun_vector("noun1")

        frame = UnresolvedFrameCandidate(
            frame_id="test_frame",
            frame_type=FrameType.UNRESOLVED,
            constituents=(noun,),
            frame_rank=LughaRank.SAMA,
            inherited_residuals=(),
            frame_specific_residuals=(),
            trace_id="test_trace",
            competing_frame_types=(FrameType.NOMINAL, FrameType.FRAGMENT),
            unresolved_reason="ambiguous",
        )

        assert frame.frame_type == FrameType.UNRESOLVED
        assert len(frame.competing_frame_types) == 2
        assert FrameType.NOMINAL in frame.competing_frame_types

    def test_unresolved_frame_requires_competing_types(self):
        """Unresolved frame must have at least one competing type"""
        noun = make_test_noun_vector("noun1")

        with pytest.raises(ValueError, match="at least one competing"):
            UnresolvedFrameCandidate(
                frame_id="test_frame",
                frame_type=FrameType.UNRESOLVED,
                constituents=(noun,),
                frame_rank=LughaRank.SAMA,
                inherited_residuals=(),
                frame_specific_residuals=(),
                trace_id="test_trace",
                competing_frame_types=(),  # Empty!
                unresolved_reason="ambiguous",
            )


class TestFrameBuilder:
    """Test frame builder functionality"""

    def test_frame_builder_identifies_verbal_frame(self):
        """Frame builder identifies verbal frame from FIIL + ISM"""
        verb = make_test_verb_vector("verb1")
        noun = make_test_noun_vector("noun1")

        builder = FrameBuilder()
        frames = builder.build_frames((verb, noun))

        assert len(frames) > 0
        # Should have verbal frame
        verbal_frames = [f for f in frames if f.frame_type == FrameType.VERBAL]
        assert len(verbal_frames) == 1
        assert verbal_frames[0].verb_index == 0

    def test_frame_builder_identifies_nominal_frame(self):
        """Frame builder identifies nominal frame from ISM + ISM"""
        noun1 = make_test_noun_vector("noun1")
        noun2 = make_test_noun_vector("noun2")

        builder = FrameBuilder()
        frames = builder.build_frames((noun1, noun2))

        assert len(frames) > 0
        # Should have nominal frame
        nominal_frames = [f for f in frames if f.frame_type == FrameType.NOMINAL]
        assert len(nominal_frames) == 1
        assert nominal_frames[0].lead_noun_index == 0

    def test_frame_builder_identifies_particle_led_frame(self):
        """Frame builder identifies particle-led frame from HARF + ISM"""
        particle = make_test_particle_vector("particle1")
        noun = make_test_noun_vector("noun1")

        builder = FrameBuilder()
        frames = builder.build_frames((particle, noun))

        assert len(frames) > 0
        # Should have particle-led frame
        particle_frames = [f for f in frames if f.frame_type == FrameType.PARTICLE_LED]
        assert len(particle_frames) == 1
        assert particle_frames[0].particle_index == 0

    def test_frame_builder_identifies_fragment(self):
        """Frame builder identifies fragment from single constituent"""
        noun = make_test_noun_vector("noun1")

        builder = FrameBuilder()
        frames = builder.build_frames((noun,))

        assert len(frames) > 0
        # Should have fragment
        fragment_frames = [f for f in frames if f.frame_type == FrameType.FRAGMENT]
        assert len(fragment_frames) == 1

    def test_frame_builder_blocks_on_not_ready_constituents(self):
        """Frame builder creates unresolved frame when constituents not ready"""
        noun = make_test_noun_vector(
            "noun1",
            readiness=CompositionReadiness.NOT_READY
        )

        builder = FrameBuilder()
        frames = builder.build_frames((noun,))

        assert len(frames) == 1
        assert frames[0].frame_type == FrameType.UNRESOLVED
        assert frames[0].unresolved_reason == "constituents_blocked"

    def test_build_sentence_frames_convenience_function(self):
        """Test convenience function build_sentence_frames"""
        verb = make_test_verb_vector("verb1")
        noun = make_test_noun_vector("noun1")

        frames = build_sentence_frames((verb, noun))

        assert len(frames) > 0
        verbal_frames = [f for f in frames if f.frame_type == FrameType.VERBAL]
        assert len(verbal_frames) == 1
