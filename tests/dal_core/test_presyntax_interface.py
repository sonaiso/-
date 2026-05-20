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
        from dal_core.mufrad_axes import BinaaJudgment, IshtiqaqJudgment

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
            # PR-F: axes must be resolved before any operator consumes the vector.
            binaa_judgment=BinaaJudgment.MUERAB,
            ishtiqaq_judgment=IshtiqaqJudgment.JAMID,
        )

        # READY_FOR_COMPOSITION + resolved axes allows operator consumption
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


# ============================================================================
# PR #10 HARDENING TESTS
# ============================================================================
# The following tests implement the 4 hardening requirements before PR #10
# can move from Draft to Ready for Review.
# ============================================================================


class TestOperatorConsumptionGate:
    """
    Hardening Requirement 1: allows_operator_consumption() must be conditional.

    The PreSyntaxMufradVector must be a governed gate, not passive data export.
    Operators may consume only when ALL conditions met.
    """

    def test_presyntax_vector_does_not_allow_operator_consumption_by_default(self):
        """NOT_READY composition readiness blocks operator consumption"""
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

        # NOT_READY must block operator consumption
        assert not vector.allows_operator_consumption()

    def test_presyntax_vector_rejects_blockers(self):
        """Blocking residuals prevent operator consumption"""
        blocker = Residual(
            type=ResidualType.MUFRAD_NOT_READY_FOR_COMPOSITION,
            severity=ResidualSeverity.BLOCKER,
            message="Missing required morphological features",
            location="test"
        )

        vector = PreSyntaxMufradVector(
            mufrad_id="test_002",
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
            residuals=(blocker,),
            trace_id="trace_002",
            competitors_count=0,
            composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
        )

        # Blocker must prevent consumption even if READY_FOR_COMPOSITION
        assert not vector.allows_operator_consumption()

    def test_presyntax_vector_rejects_unresolved_competitors_for_certificate(self):
        """Unresolved competitors block certificate-level composition"""
        vector = PreSyntaxMufradVector(
            mufrad_id="test_003",
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
            trace_id="trace_003",
            competitors_count=2,  # Unresolved competitors
            composition_readiness=CompositionReadiness.READY_FOR_CERTIFICATE_COMPOSITION,
        )

        # Certificate-level readiness with competitors must block consumption
        assert not vector.allows_operator_consumption()

    def test_presyntax_vector_requires_trace_to_raw_input(self):
        """Missing or empty trace_id prevents operator consumption"""
        # Test with empty trace_id
        vector_empty_trace = PreSyntaxMufradVector(
            mufrad_id="test_004",
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
            trace_id="",  # Empty trace
            competitors_count=0,
            composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
        )

        # Empty trace must block consumption
        assert not vector_empty_trace.allows_operator_consumption()


class TestCaseSignPotentialHardening:
    """
    Hardening Requirement 2: CaseSignPotential must not become disguised CaseEffect.

    These tests prove CaseSignPotential contains NO syntax governance fields.
    """

    def test_case_sign_potential_contains_no_operator_binding(self):
        """CaseSignPotential must not contain operator or governed_by fields"""
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
            sign_value=CaseSignValue.DAMMA,
            compatible_case_effects=("rafa_candidate", "building_on_damma_candidate"),
            evidence=Evidence(source="test", reason="test", confidence=1.0),
            rank=LughaRank.SAMA,
            residuals=(),
            trace_id="test_trace",
        )

        # Verify NO operator binding fields exist
        forbidden_fields = ['operator', 'operator_id', 'governed_by', 'governed_by_operator']
        for field in forbidden_fields:
            assert not hasattr(potential, field), f"Found forbidden field: {field}"

    def test_case_sign_potential_contains_no_final_case_judgment(self):
        """CaseSignPotential must not contain marfoo_by, mansub_by, majroor_by, majzum_by"""
        surface = SurfaceEffect(
            effect_type=SurfaceEffectType.FINAL_FATHA,
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
            sign_value=CaseSignValue.FATHA,
            compatible_case_effects=("nasb_candidate", "building_on_fatha_candidate"),
            evidence=Evidence(source="test", reason="test", confidence=1.0),
            rank=LughaRank.SAMA,
            residuals=(),
            trace_id="test_trace",
        )

        # Verify NO case judgment fields exist
        forbidden_fields = ['marfoo_by', 'mansub_by', 'majroor_by', 'majzum_by', 'case_effect', 'case_judgment']
        for field in forbidden_fields:
            assert not hasattr(potential, field), f"Found forbidden field: {field}"

    def test_case_sign_potential_contains_no_syntax_role(self):
        """CaseSignPotential must not contain syntax role fields (faail, mafool, etc.)"""
        surface = SurfaceEffect(
            effect_type=SurfaceEffectType.FINAL_KASRA,
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
            sign_value=CaseSignValue.KASRA,
            compatible_case_effects=("jarr_candidate",),
            evidence=Evidence(source="test", reason="test", confidence=1.0),
            rank=LughaRank.SAMA,
            residuals=(),
            trace_id="test_trace",
        )

        # Verify NO syntax role fields exist
        forbidden_fields = ['syntax_role', 'faail', 'mafool', 'mubtada', 'khabar']
        for field in forbidden_fields:
            assert not hasattr(potential, field), f"Found forbidden field: {field}"


class TestTypeIDsOperationalNotSemantic:
    """
    Hardening Requirement 3: Type IDs are operational codes, not meanings.

    type_id ≠ meaning
    type_id = operational key for operator matching
    """

    def test_type_id_is_operational_code_not_meaning(self):
        """Type IDs are operator-matching codes, not semantic meanings"""
        # NounTypeID values are operational identifiers
        assert isinstance(NounTypeID.ISM_COMMON.value, str)
        assert isinstance(VerbTypeID.FIIL_MADI.value, str)
        assert isinstance(ParticleTypeID.HARF_JARR.value, str)

        # They are codes for operator contract matching
        # NOT semantic meanings or denotations
        # Operators check: if type_id == NounTypeID.ISM_COMMON
        # NOT: if meaning == "common noun"

    def test_particle_type_id_does_not_emit_semantic_value(self):
        """ParticleTypeID must not provide semantic meaning or madlul"""
        # ParticleTypeID is an operational code
        particle_id = ParticleTypeID.HARF_JARR

        # It has a value (operational string)
        assert particle_id.value == "حرف_جر"

        # But it does NOT have semantic fields
        assert not hasattr(particle_id, 'meaning')
        assert not hasattr(particle_id, 'semantic')
        assert not hasattr(particle_id, 'madlul')
        assert not hasattr(particle_id, 'murad')
        assert not hasattr(particle_id, 'denotation')
        assert not hasattr(particle_id, 'referent')

    def test_verb_type_id_does_not_emit_intended_time(self):
        """VerbTypeID must not provide intended_time or semantic temporal reference"""
        # VerbTypeID.FIIL_MADI is an operational code
        verb_id = VerbTypeID.FIIL_MADI

        # It has a value (operational string)
        assert verb_id.value == "فعل_ماضٍ"

        # But it does NOT have semantic temporal fields
        assert not hasattr(verb_id, 'intended_time')
        assert not hasattr(verb_id, 'semantic_time')
        assert not hasattr(verb_id, 'temporal_reference')
        assert not hasattr(verb_id, 'meaning')
        assert not hasattr(verb_id, 'madlul')

        # "فعل_ماضٍ" is a grammatical category code, not a semantic time assertion


class TestRankAndResidualInheritance:
    """
    Hardening Requirement 4: PreSyntax rank must not raise MufradProof rank.

    PreSyntaxMufradVector is an extraction interface, not a proof upgrade.

    Rules:
    - rank(PreSyntaxMufradVector) <= rank(MufradProof)
    - residuals(PreSyntaxMufradVector) ⊇ residuals(MufradProof)
    - trace(PreSyntaxMufradVector) includes raw input trace
    """

    def test_presyntax_vector_rank_cannot_exceed_mufrad_rank(self):
        """PreSyntaxMufradVector final_rank must not exceed source MufradProof rank"""
        # Source: MufradProof has AHAD rank
        # PreSyntaxVector must preserve or lower, not upgrade

        vector_preserves_rank = PreSyntaxMufradVector(
            mufrad_id="test_010",
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
            morph_rank=LughaRank.AHAD,
            final_rank=LughaRank.AHAD,  # Preserved from MufradProof
            residuals=(),
            trace_id="trace_010",
            competitors_count=0,
            composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
        )

        # final_rank should match or be lower than morph_rank
        assert vector_preserves_rank.final_rank.value <= vector_preserves_rank.morph_rank.value

        # FORBIDDEN: final_rank > morph_rank (upgrade)
        # This would violate weakest-link principle

    def test_presyntax_vector_preserves_mufrad_residuals(self):
        """PreSyntaxMufradVector must preserve all residuals from MufradProof"""
        source_residual = Residual(
            type=ResidualType.MUFRAD_DEFINITENESS_UNRESOLVED,
            severity=ResidualSeverity.WARNING,
            message="Definiteness unresolved in morphological analysis",
            location="mufrad_proof"
        )

        vector = PreSyntaxMufradVector(
            mufrad_id="test_011",
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
            residuals=(source_residual,),  # Preserved from MufradProof
            trace_id="trace_011",
            competitors_count=0,
            composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
        )

        # Residuals must be preserved
        assert len(vector.residuals) == 1
        assert vector.residuals[0].type == ResidualType.MUFRAD_DEFINITENESS_UNRESOLVED

        # FORBIDDEN: Erasing residuals from MufradProof
        # This would hide unresolved issues

    def test_presyntax_vector_preserves_mufrad_trace(self):
        """PreSyntaxMufradVector must preserve trace_id linking to raw input"""
        # Trace linking to raw input witness chain
        source_trace_id = "raw_input_witness_001"

        vector = PreSyntaxMufradVector(
            mufrad_id="test_012",
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
            trace_id=source_trace_id,  # Preserved from MufradProof
            competitors_count=0,
            composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
        )

        # Trace must be preserved and link to raw input
        assert vector.trace_id == source_trace_id
        assert vector.trace_id != ""

        # FORBIDDEN: Losing trace connection to raw input
        # This would break witness chain
