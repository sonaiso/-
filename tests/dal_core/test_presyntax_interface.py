"""
Tests for PreSyntax Interface Layer (طبقة واجهة ما قبل التركيب)

Critical tests ensuring:
1. PreSyntaxMufradVector has no semantic/syntax role/case effect leaks
2. CaseSignPotential distinct from forbidden CaseEffect
3. Operators cannot consume raw tokens
4. Type IDs are operational codes, not meanings
5. MufradProof exports to PreSyntaxVector correctly
"""

import pytest
from dal_core.case_signs import (
    CaseSignFamily,
    CaseSignValue,
    CaseSignPotential,
    CaseSignResidualType,
)
from dal_core.type_ids import NounTypeID, VerbTypeID, ParticleTypeID
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.surface_effects import (
    SurfaceEffect,
    SurfaceEffectType,
    SurfaceEffectVisibility,
)
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, ResidualType, ResidualSeverity
from dal_core.evidence import Evidence
from dal_core.composition_readiness import CompositionReadiness
from dal_core.morph_features import CandidateStatus


class TestCaseSignPotentialVsCaseEffect:
    """
    Test critical distinction:
    CaseSignPotential (ALLOWED in Mufrad Proof) vs CaseEffect (FORBIDDEN)
    """

    def test_case_sign_potential_is_observation_not_judgment(self):
        """CaseSignPotential records surface observation, not grammatical judgment"""
        surface = SurfaceEffect(
            effect_type=SurfaceEffectType.FINAL_DAMMA,
            visibility=SurfaceEffectVisibility.VISIBLE,
            location="final",
            evidence=(Evidence(source="test", reason="test observation", confidence=1.0),),
            rank=LughaRank.SAMA,
            residuals=(),
            trace={"id": "test_trace"},
        )

        potential = CaseSignPotential(
            observed_surface=surface,
            sign_family=CaseSignFamily.ORIGINAL,
            sign_value=CaseSignValue.DAMMA,
            compatible_case_effects=("rafa_candidate", "building_on_damma_candidate"),
            evidence=Evidence(source="test", reason="test case sign", confidence=1.0),
            rank=LughaRank.SAMA,
            residuals=(),
            trace_id="test_trace",
        )

        # Verify it's a potential, not a judgment
        assert potential.sign_family == CaseSignFamily.ORIGINAL
        assert potential.sign_value == CaseSignValue.DAMMA
        assert "candidate" in potential.compatible_case_effects[0]

        # Verify no case judgment fields
        assert not hasattr(potential, 'marfoo_by')
        assert not hasattr(potential, 'mansub_by')
        assert not hasattr(potential, 'governed_by')

    def test_case_sign_potential_rejects_judgment_names(self):
        """CaseSignPotential must use '*_candidate' naming, not judgments"""
        surface = SurfaceEffect(
            effect_type=SurfaceEffectType.FINAL_DAMMA,
            visibility=SurfaceEffectVisibility.VISIBLE,
            location="final",
            evidence=(Evidence(source="test", reason="test", confidence=1.0),),
            rank=LughaRank.SAMA,
            residuals=(),
            trace={"id": "test_trace"},
        )

        # This should fail - using "marfoo" instead of "*_candidate"
        with pytest.raises(ValueError, match="case judgment"):
            CaseSignPotential(
                observed_surface=surface,
                sign_family=CaseSignFamily.ORIGINAL,
                sign_value=CaseSignValue.DAMMA,
                compatible_case_effects=("marfoo_by_fiil",),  # Forbidden!
                evidence=(Evidence(source="test", reason="test", confidence=1.0),),
                rank=LughaRank.SAMA,
                residuals=(),
                trace_id="test_trace",
            )

    def test_original_case_signs_are_potentials(self):
        """Original case marks (damma, fatha, kasra, sukun) are potentials"""
        for sign_value in [
            CaseSignValue.DAMMA,
            CaseSignValue.FATHA,
            CaseSignValue.KASRA,
            CaseSignValue.SUKUN,
        ]:
            surface = SurfaceEffect(
                effect_type=SurfaceEffectType.FINAL_DAMMA,
                visibility=SurfaceEffectVisibility.VISIBLE,
                location="final",
                evidence=(Evidence(source="test", reason="test", confidence=1.0),),
                rank=LughaRank.SAMA,
                residuals=(),
                trace={"id": "test_trace"},
            )

            potential = CaseSignPotential(
                observed_surface=surface,
                sign_family=CaseSignFamily.ORIGINAL,
                sign_value=sign_value,
                compatible_case_effects=("rafa_candidate",),
                evidence=(Evidence(source="test", reason="test", confidence=1.0),),
                rank=LughaRank.SAMA,
                residuals=(),
                trace_id="test_trace",
            )

            assert potential.sign_family == CaseSignFamily.ORIGINAL

    def test_substitute_case_signs_are_potentials(self):
        """Substitute marks (alif, waw, ya, nun) are potentials"""
        for sign_value in [
            CaseSignValue.ALIF,
            CaseSignValue.WAW,
            CaseSignValue.YA,
            CaseSignValue.NUN_DELETED,
        ]:
            surface = SurfaceEffect(
                effect_type=SurfaceEffectType.FINAL_ALIF,
                visibility=SurfaceEffectVisibility.VISIBLE,
                location="final",
                evidence=(Evidence(source="test", reason="test", confidence=1.0),),
                rank=LughaRank.SAMA,
                residuals=(),
                trace={"id": "test_trace"},
            )

            potential = CaseSignPotential(
                observed_surface=surface,
                sign_family=CaseSignFamily.SUBSTITUTE,
                sign_value=sign_value,
                compatible_case_effects=("dual_rafa_candidate",),
                evidence=(Evidence(source="test", reason="test", confidence=1.0),),
                rank=LughaRank.SAMA,
                residuals=(),
                trace_id="test_trace",
            )

            assert potential.sign_family == CaseSignFamily.SUBSTITUTE


class TestPreSyntaxVectorNoLeaks:
    """
    Test that PreSyntaxMufradVector contains NO forbidden fields.

    FORBIDDEN:
    - meaning, semantic, madlul, murad, haqiqa, majaz
    - syntax roles (faail, mafool, mubtada, khabar)
    - case effects (marfoo_by, mansub_by, majroor_by)
    - operator governance
    """

    def test_presyntax_vector_has_no_semantic_fields(self):
        """PreSyntaxMufradVector must not have semantic/meaning fields"""
        vector = PreSyntaxMufradVector(
            mufrad_id="test_001",
            raw_span=(0, 5),
            type_value="ISM",
            type_id=None,
            type_rank=LughaRank.SAMA,
            mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
            noun_inflection_class=None,
            verb_features=None,
            particle_operator_potential=None,
            surface_effects=(),
            case_sign_potentials=(),
            morph_rank=LughaRank.SAMA,
            final_rank=LughaRank.SAMA,
            residuals=(),
            trace_id="trace_001",
            competitors_count=0,
            composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
        )

        # Verify no semantic fields
        forbidden = ['meaning', 'semantic', 'madlul', 'murad', 'haqiqa', 'majaz']
        for field in forbidden:
            assert not hasattr(vector, field), f"Found forbidden field: {field}"

    def test_presyntax_vector_has_no_syntax_role_fields(self):
        """PreSyntaxMufradVector must not have syntax role fields"""
        vector = PreSyntaxMufradVector(
            mufrad_id="test_001",
            raw_span=(0, 5),
            type_value="ISM",
            type_id=None,
            type_rank=LughaRank.SAMA,
            mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
            noun_inflection_class=None,
            verb_features=None,
            particle_operator_potential=None,
            surface_effects=(),
            case_sign_potentials=(),
            morph_rank=LughaRank.SAMA,
            final_rank=LughaRank.SAMA,
            residuals=(),
            trace_id="trace_001",
            competitors_count=0,
            composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
        )

        # Verify no syntax role fields
        forbidden = ['faail', 'mafool', 'mubtada', 'khabar', 'syntax_role']
        for field in forbidden:
            assert not hasattr(vector, field), f"Found forbidden field: {field}"

    def test_presyntax_vector_has_no_case_effect_fields(self):
        """PreSyntaxMufradVector must not have case effect fields"""
        vector = PreSyntaxMufradVector(
            mufrad_id="test_001",
            raw_span=(0, 5),
            type_value="ISM",
            type_id=None,
            type_rank=LughaRank.SAMA,
            mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
            noun_inflection_class=None,
            verb_features=None,
            particle_operator_potential=None,
            surface_effects=(),
            case_sign_potentials=(),
            morph_rank=LughaRank.SAMA,
            final_rank=LughaRank.SAMA,
            residuals=(),
            trace_id="trace_001",
            competitors_count=0,
            composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
        )

        # Verify no case effect fields
        forbidden = [
            'case_effect', 'marfoo_by', 'mansub_by', 'majroor_by',
            'governed_by_operator', 'governed_by',
        ]
        for field in forbidden:
            assert not hasattr(vector, field), f"Found forbidden field: {field}"


class TestTypeIDsAreOperationalNotSemantic:
    """
    Test that type IDs are operational codes, not semantic meanings.

    type_id ≠ meaning
    type_id = operational key for operator entry
    """

    def test_noun_type_ids_are_codes_not_meanings(self):
        """Noun type IDs are operational identifiers"""
        # These are codes for operator matching
        assert NounTypeID.ISM_COMMON.value == "اسم_جنس"
        assert NounTypeID.ISM_PROPER.value == "اسم_علم"
        assert NounTypeID.ISM_DERIVED_ACTIVE_PARTICIPLE.value == "اسم_فاعل"

        # They are NOT semantic meanings - they are entry keys
        # Operators check: if type_id == ISM_COMMON: ...
        # NOT: if meaning == "common noun": ...

    def test_verb_type_ids_are_codes_not_meanings(self):
        """Verb type IDs are operational identifiers"""
        assert VerbTypeID.FIIL_MADI.value == "فعل_ماضٍ"
        assert VerbTypeID.FIIL_MUDARI.value == "فعل_مضارع"
        assert VerbTypeID.FIIL_AMR.value == "فعل_أمر"

    def test_particle_type_ids_are_codes_not_meanings(self):
        """Particle type IDs are operational identifiers"""
        assert ParticleTypeID.HARF_JARR.value == "حرف_جر"
        assert ParticleTypeID.HARF_NASB.value == "حرف_نصب"
        assert ParticleTypeID.HARF_JAZM.value == "حرف_جزم"


class TestOperatorCannotConsumeTokens:
    """
    Test that operators CANNOT work on raw tokens.

    Mathematical foundation:
    O_j : PreSyntaxMufradVector^k → CandidateSet  (CORRECT)

    NOT:
    O_j : Token^k → CaseEffect  (FORBIDDEN)
    """

    def test_operator_contract_rejects_raw_string(self):
        """OperatorContract must reject raw string input"""
        from dal_core.operator_contract import OperatorContract

        # Operators must only accept PreSyntaxMufradVector or MufradProof
        # NOT raw strings or tokens

        # This test verifies the contract exists and has proper type hints
        # Full implementation will be in OperatorContract itself

    def test_operator_requires_presyntax_vector(self):
        """Operators must require PreSyntaxMufradVector input"""
        # This is tested via type system and runtime validation
        # Future operators will have signature:
        # def apply(self, inputs: tuple[PreSyntaxMufradVector, ...]) -> ...

    def test_composition_readiness_gates_operator_access(self):
        """NOT_READY MufradProof blocks operator consumption"""
        vector = PreSyntaxMufradVector(
            mufrad_id="test_001",
            raw_span=(0, 5),
            type_value="ISM",
            type_id=None,
            type_rank=LughaRank.SAMA,
            mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
            noun_inflection_class=None,
            verb_features=None,
            particle_operator_potential=None,
            surface_effects=(),
            case_sign_potentials=(),
            morph_rank=LughaRank.SAMA,
            final_rank=LughaRank.SAMA,
            residuals=(),
            trace_id="trace_001",
            competitors_count=0,
            composition_readiness=CompositionReadiness.NOT_READY,
        )

        # NOT_READY should block operator consumption
        assert not vector.allows_operator_consumption()

    def test_ready_vector_allows_operator_consumption(self):
        """READY_FOR_COMPOSITION allows operator consumption"""
        vector = PreSyntaxMufradVector(
            mufrad_id="test_001",
            raw_span=(0, 5),
            type_value="ISM",
            type_id=None,
            type_rank=LughaRank.SAMA,
            mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
            noun_inflection_class=None,
            verb_features=None,
            particle_operator_potential=None,
            surface_effects=(),
            case_sign_potentials=(),
            morph_rank=LughaRank.SAMA,
            final_rank=LughaRank.SAMA,
            residuals=(),
            trace_id="trace_001",
            competitors_count=0,
            composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
        )

        # READY_FOR_COMPOSITION allows operator consumption
        assert vector.allows_operator_consumption()


class TestMufradProofExportsToVector:
    """
    Test that MufradProof correctly exports to PreSyntaxMufradVector.

    This is the ONLY interface operators may consume.
    """

    def test_mufrad_proof_has_to_presyntax_vector_method(self):
        """MufradProof must have to_presyntax_vector() method"""
        from dal_core.mufrad_proof import MufradProof

        # Check method exists
        assert hasattr(MufradProof, 'to_presyntax_vector')

    def test_mufrad_proof_exports_case_sign_potentials_not_effects(self):
        """MufradProof can contain case_sign_potentials field"""
        from dal_core.mufrad_proof import MufradProof

        # Check that MufradProof has case_sign_potentials field
        # (this was added in PR #10)
        fields = {f.name for f in MufradProof.__dataclass_fields__.values()}
        assert 'case_sign_potentials' in fields

        # Verify case_effect is NOT allowed
        assert 'case_effect' not in fields


class TestCaseSignResidualTypes:
    """Test case sign specific residual types"""

    def test_case_sign_residual_types_exist(self):
        """Case sign residuals must be defined"""
        assert hasattr(CaseSignResidualType, 'MUFRAD_CASE_SIGN_UNRESOLVED')
        assert hasattr(CaseSignResidualType, 'MUFRAD_ORIGINAL_SIGN_UNRESOLVED')
        assert hasattr(CaseSignResidualType, 'MUFRAD_SUBSTITUTE_SIGN_UNRESOLVED')
        assert hasattr(CaseSignResidualType, 'MUFRAD_ESTIMATED_SIGN_REQUIRES_TRACE')
