"""
Tests for MorphProof Contract (Phase 2.5)

Tests the morphological proof structure required for composition readiness.

CRITICAL TESTS:
1. Composition readiness requires MorphProof
2. MorphProof contains NO semantic fields (Theorem 5 compliance)
3. All features are candidates with evidence/rank/residuals
4. Competing candidates block composition
5. Unresolved mabni/murab blocks composition
"""

import pytest
from dal_core.morph_proof import (
    MorphProof,
    RootCandidate,
    WaznCandidate,
    VerbFeatureProof,
    SurfaceEffect,
    CandidateStatus,
    make_stub_morph_proof
)
from dal_core.d_mufrad import DClosed
from dal_core.d_type import TypedDal, DalType
from dal_core.d_lugha import LughaAttestation
from dal_core.d_form import FormCandidate
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, ResidualType, ResidualSeverity
from dal_core.evidence import Evidence


class TestMorphProofStructure:
    """Test MorphProof data structure"""

    def test_morph_proof_creation(self):
        """MorphProof can be created with all fields"""
        morph_proof = MorphProof(
            root_candidates=(
                RootCandidate(letters=("ك", "ت", "ب"), rank=LughaRank.FORM),
            ),
            wazn_candidates=(
                WaznCandidate(pattern="فَعَلَ", rank=LughaRank.FORM),
            ),
            mabni_murab_status=CandidateStatus.RESOLVED,
            rank=LughaRank.FORM
        )

        assert morph_proof is not None
        assert len(morph_proof.root_candidates) == 1
        assert len(morph_proof.wazn_candidates) == 1

    def test_stub_morph_proof(self):
        """Stub MorphProof indicates incomplete analysis"""
        stub = make_stub_morph_proof()

        assert stub.rank == LughaRank.ZERO
        assert len(stub.all_residuals) > 0
        assert any(r.type == ResidualType.MORPH_ANALYSIS_INCOMPLETE for r in stub.all_residuals)


class TestCompositionReadiness:
    """Test composition readiness logic"""

    def test_morph_proof_not_composition_ready_without_mabni_murab(self):
        """MorphProof not composition-ready if mabni/murab unresolved"""
        morph_proof = MorphProof(
            mabni_murab_status=CandidateStatus.UNRESOLVED,
            rank=LughaRank.FORM
        )

        assert not morph_proof.is_composition_ready()

    def test_morph_proof_not_composition_ready_with_competing_mabni_murab(self):
        """MorphProof not composition-ready if mabni/murab competing"""
        morph_proof = MorphProof(
            mabni_murab_status=CandidateStatus.COMPETING,
            rank=LughaRank.FORM
        )

        assert not morph_proof.is_composition_ready()

    def test_morph_proof_composition_ready_with_resolved_mabni_murab(self):
        """MorphProof composition-ready if mabni/murab resolved"""
        morph_proof = MorphProof(
            mabni_murab_status=CandidateStatus.RESOLVED,
            rank=LughaRank.FORM
        )

        assert morph_proof.is_composition_ready()

    def test_morph_proof_not_ready_with_blocker_residuals(self):
        """MorphProof not composition-ready with blocker residuals"""
        morph_proof = MorphProof(
            mabni_murab_status=CandidateStatus.RESOLVED,
            rank=LughaRank.FORM,
            all_residuals=(
                Residual(
                    type=ResidualType.MORPH_ANALYSIS_INCOMPLETE,
                    severity=ResidualSeverity.BLOCKER,
                    message="Critical morph analysis failure"
                ),
            )
        )

        assert not morph_proof.is_composition_ready()


class TestDClosedCompositionReadiness:
    """Test DClosed composition readiness with MorphProof"""

    def test_dclosed_not_composition_ready_without_morph_proof(self):
        """DClosed not composition-ready without MorphProof"""
        # Create minimal DClosed without morph_proof
        form = FormCandidate(text="كتب", vocalization="كَتَبَ", rank=LughaRank.FORM)
        lugha = LughaAttestation(form=form, rank=LughaRank.TAWATUR, is_arabic=True)
        typed_dal = TypedDal(attestation=lugha, dal_type=DalType.FIIL)

        dclosed = DClosed(
            typed_dal=typed_dal,
            morph_proof=None,  # No morph proof
            final_rank=LughaRank.TAWATUR
        )

        assert dclosed.is_closed()  # Lexically closed
        assert not dclosed.is_composition_ready()  # Not composition-ready

    def test_dclosed_composition_ready_with_morph_proof(self):
        """DClosed composition-ready with valid MorphProof"""
        form = FormCandidate(text="كتب", vocalization="كَتَبَ", rank=LughaRank.FORM)
        lugha = LughaAttestation(form=form, rank=LughaRank.TAWATUR, is_arabic=True)
        typed_dal = TypedDal(attestation=lugha, dal_type=DalType.FIIL)

        morph_proof = MorphProof(
            mabni_murab_status=CandidateStatus.RESOLVED,
            rank=LughaRank.FORM
        )

        dclosed = DClosed(
            typed_dal=typed_dal,
            morph_proof=morph_proof,
            final_rank=LughaRank.TAWATUR
        )

        assert dclosed.is_closed()  # Lexically closed
        assert dclosed.is_composition_ready()  # Composition-ready


class TestSemanticLeakPrevention:
    """Test that MorphProof contains NO semantic fields"""

    def test_morph_proof_no_meaning_field(self):
        """MorphProof does not have 'meaning' field"""
        morph_proof = MorphProof()

        assert not hasattr(morph_proof, 'meaning')
        assert not hasattr(morph_proof, 'murad')
        assert not hasattr(morph_proof, 'semantic')
        assert not hasattr(morph_proof, 'haqiqa')
        assert not hasattr(morph_proof, 'majaz')

    def test_root_candidate_no_semantic_field(self):
        """RootCandidate contains signifier features only"""
        root = RootCandidate(letters=("ك", "ت", "ب"))

        assert not hasattr(root, 'meaning')
        assert not hasattr(root, 'semantic')
        # Has signifier features
        assert hasattr(root, 'letters')
        assert hasattr(root, 'evidence')
        assert hasattr(root, 'rank')

    def test_wazn_candidate_no_semantic_field(self):
        """WaznCandidate contains pattern info only, not meaning"""
        wazn = WaznCandidate(pattern="فَعَلَ")

        assert not hasattr(wazn, 'meaning')
        assert not hasattr(wazn, 'semantic')
        # Has signifier features
        assert hasattr(wazn, 'pattern')
        assert hasattr(wazn, 'evidence')

    def test_verb_features_are_forms_not_meanings(self):
        """Verb features are morphological forms, not semantic time/agency"""
        verb_features = VerbFeatureProof(
            tense_form="ماضٍ",  # Morphological past form
            voice_form="معلوم"  # Morphological active form
        )

        # These are FORM features, not semantic interpretations
        assert verb_features.tense_form == "ماضٍ"  # Form, not "semantic past time"
        assert verb_features.voice_form == "معلوم"  # Form, not "semantic agent present"

        # No semantic fields
        assert not hasattr(verb_features, 'meaning')
        assert not hasattr(verb_features, 'semantic_time')
        assert not hasattr(verb_features, 'agent_present')


class TestRootAndWaznCandidates:
    """Test root and pattern candidates"""

    def test_root_candidate_not_absolute_without_witness(self):
        """Root extraction is candidate, not absolute truth"""
        root = RootCandidate(
            letters=("ك", "ت", "ب"),
            rank=LughaRank.FORM  # Pattern-based is FORM rank
        )

        # Rank is FORM, not TAWATUR/AHAD (no witness)
        assert root.rank == LughaRank.FORM
        assert root.rank < LughaRank.SAMA

    def test_wazn_does_not_prove_lugha(self):
        """Pattern detection does not prove linguistic attestation"""
        wazn = WaznCandidate(
            pattern="فَعَلَ",
            rank=LughaRank.FORM  # Pattern alone is FORM
        )

        # Wazn detection gives FORM rank, not attestation
        assert wazn.rank == LughaRank.FORM
        assert wazn.rank < LughaRank.SAMA  # Not attested
        assert wazn.rank < LughaRank.AHAD
        assert wazn.rank < LughaRank.TAWATUR


class TestMabniMurabCritical:
    """Test mabni/murab (built vs declined) - critical for composition"""

    def test_mabni_murab_unresolved_blocks_composition(self):
        """Unresolved mabni/murab blocks composition certificate"""
        morph_proof = MorphProof(
            mabni_murab_status=CandidateStatus.UNRESOLVED
        )

        assert not morph_proof.is_composition_ready()

    def test_mabni_murab_competing_blocks_composition(self):
        """Competing mabni/murab candidates block composition"""
        morph_proof = MorphProof(
            mabni_murab_status=CandidateStatus.COMPETING
        )

        assert not morph_proof.is_composition_ready()

    def test_mabni_resolved_allows_composition(self):
        """Resolved mabni status allows composition"""
        morph_proof = MorphProof(
            mabni_murab_status=CandidateStatus.RESOLVED,
            mabni_murab_evidence=(
                Evidence(
                    source="Type classification",
                    reason="Particle type → mabni"
                ),
            )
        )

        assert morph_proof.is_composition_ready()


class TestSurfaceEffects:
    """Test surface effect tracking"""

    def test_surface_effect_preserves_final_state(self):
        """Surface effects track final vowel/letter state"""
        effect = SurfaceEffect(
            effect_type="vowel",
            effect_value="ضمة",
            position="final",
            is_original=False  # Added, not original to root
        )

        assert effect.effect_value == "ضمة"
        assert effect.position == "final"
        assert not effect.is_original

    def test_surface_effects_not_interpreted_as_irab(self):
        """Surface effects are signifier states, NOT i'rab interpretations"""
        effect = SurfaceEffect(
            effect_type="vowel",
            effect_value="ضمة",
            position="final",
            is_original=False
        )

        # It's a surface effect, not an i'rab interpretation
        assert not hasattr(effect, 'irab')
        assert not hasattr(effect, 'case')
        assert not hasattr(effect, 'syntactic_role')
        # Just the signifier state
        assert effect.effect_value == "ضمة"


class TestTheoremCompliance:
    """Test compliance with governing theorems"""

    def test_theorem_no_compositional_cert_without_morph_closed(self):
        """Theorem: Cert(D_murakkab) ⟹ MorphClosed(D_mufrad_i)"""
        # If morph_proof is None or not ready, composition not allowed
        form = FormCandidate(text="كتب", vocalization="كَتَبَ", rank=LughaRank.FORM)
        lugha = LughaAttestation(form=form, rank=LughaRank.TAWATUR, is_arabic=True)
        typed_dal = TypedDal(attestation=lugha, dal_type=DalType.FIIL)

        # Without morph_proof
        dclosed = DClosed(typed_dal=typed_dal, morph_proof=None)
        assert not dclosed.is_composition_ready()

        # With incomplete morph_proof
        incomplete_morph = MorphProof(
            mabni_murab_status=CandidateStatus.UNRESOLVED
        )
        dclosed_incomplete = DClosed(typed_dal=typed_dal, morph_proof=incomplete_morph)
        assert not dclosed_incomplete.is_composition_ready()


class TestDistinctionLexicalVsCompositional:
    """Test distinction between lexical closure and compositional readiness"""

    def test_lexical_closed_not_implies_composition_ready(self):
        """Lexical closure does not imply composition readiness"""
        form = FormCandidate(text="كتاب", vocalization="كِتَابٌ", rank=LughaRank.FORM)
        lugha = LughaAttestation(form=form, rank=LughaRank.TAWATUR, is_arabic=True)
        typed_dal = TypedDal(attestation=lugha, dal_type=DalType.ISM)

        # Lexically closed but no morph_proof
        dclosed = DClosed(
            typed_dal=typed_dal,
            morph_proof=None,
            final_rank=LughaRank.TAWATUR
        )

        # Lexically closed
        assert dclosed.is_closed()
        # But NOT composition-ready
        assert not dclosed.is_composition_ready()

    def test_composition_ready_implies_lexical_closed(self):
        """Composition readiness requires lexical closure"""
        form = FormCandidate(text="كتاب", vocalization="كِتَابٌ", rank=LughaRank.FORM)
        lugha = LughaAttestation(form=form, rank=LughaRank.TAWATUR, is_arabic=True)
        typed_dal = TypedDal(attestation=lugha, dal_type=DalType.ISM)

        morph_proof = MorphProof(
            mabni_murab_status=CandidateStatus.RESOLVED
        )

        dclosed = DClosed(
            typed_dal=typed_dal,
            morph_proof=morph_proof,
            final_rank=LughaRank.TAWATUR
        )

        # Composition-ready
        if dclosed.is_composition_ready():
            # Then must be lexically closed
            assert dclosed.is_closed()
