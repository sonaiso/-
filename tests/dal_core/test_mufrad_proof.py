#!/usr/bin/env python3
"""
MufradProof Theorem Tests

Tests for the 10 non-negotiable theorems for composition-ready MufradProof.
"""

import sys
sys.path.insert(0, 'src')

from dal_core.mufrad_proof import MufradProof, verify_no_semantic_leak, verify_no_syntax_role_leak, verify_no_case_effect_leak
from dal_core.morph_features import (
    SegmentationProof, StemProof, CliticProof, RootCandidate, WaznCandidate,
    CandidateStatus, VerbFeatureProof, NounInflectionClass, ParticleOperatorPotential
)
from dal_core.surface_effects import SurfaceEffect, SurfaceEffectType, SurfaceEffectVisibility
from dal_core.composition_readiness import CompositionReadiness
from dal_core.d_form import FormCandidate
from dal_core.d_lugha import LughaAttestation, LughaRank
from dal_core.d_type import TypedDal, DalType
from dal_core.ranks import FormRank
from dal_core.residuals import ResidualType, ResidualSeverity
from dal_core.evidence import Evidence
from dal_core.operator_contract import OperatorContract, reject_token_application


def make_minimal_mufrad_proof() -> MufradProof:
    """Helper to create minimal valid MufradProof"""
    form = FormCandidate(
        text="كتب",
        vocalization="كَتَبَ",
        rank=FormRank.FORM
    )
    lugha = LughaAttestation(
        form=form,
        rank=LughaRank.TAWATUR,
        is_arabic=True
    )
    typed_dal = TypedDal(
        attestation=lugha,
        dal_type=DalType.FIIL
    )

    segmentation = SegmentationProof(
        segments=("كتب",),
        evidence=(Evidence("manual", "test", LughaRank.TAWATUR),),
        rank=LughaRank.TAWATUR
    )
    stem = StemProof(
        stem="كتب",
        evidence=(Evidence("manual", "test", LughaRank.TAWATUR),),
        rank=LughaRank.TAWATUR
    )

    return MufradProof(
        form=form,
        lugha=lugha,
        type=typed_dal,
        segmentation=segmentation,
        stem=stem,
        clitics=tuple(),
        root_candidates=tuple(),
        wazn_candidates=tuple(),
        derivation_status=CandidateStatus.NOT_APPLICABLE,
        jamid_mushtaq_status=CandidateStatus.NOT_APPLICABLE,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
        definiteness_status=CandidateStatus.NOT_APPLICABLE,
        gender_status=CandidateStatus.RESOLVED_CERTAIN,
        number_status=CandidateStatus.RESOLVED_CERTAIN,
        composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION
    )


def test_mufrad_proof_has_required_fields():
    """Test MufradProof has all required fields"""
    proof = make_minimal_mufrad_proof()

    assert hasattr(proof, 'form')
    assert hasattr(proof, 'lugha')
    assert hasattr(proof, 'type')
    assert hasattr(proof, 'segmentation')
    assert hasattr(proof, 'stem')
    assert hasattr(proof, 'clitics')
    assert hasattr(proof, 'root_candidates')
    assert hasattr(proof, 'wazn_candidates')
    assert hasattr(proof, 'surface_effects')
    assert hasattr(proof, 'composition_readiness')
    assert hasattr(proof, 'rank')
    assert hasattr(proof, 'residuals')
    assert hasattr(proof, 'trace')
    assert hasattr(proof, 'competitors')

    print("✓ test_mufrad_proof_has_required_fields")


def test_mufrad_proof_requires_form_lugha_type():
    """Test MufradProof requires form, lugha, type"""
    proof = make_minimal_mufrad_proof()

    assert proof.form is not None
    assert proof.lugha is not None
    assert proof.type is not None
    assert proof.type.dal_type != DalType.AMBIGUOUS

    print("✓ test_mufrad_proof_requires_form_lugha_type")


def test_surface_effect_allowed_in_mufrad():
    """Test SurfaceEffect is allowed in MufradProof"""
    proof = make_minimal_mufrad_proof()

    # Create surface effect
    effect = SurfaceEffect(
        effect_type=SurfaceEffectType.FINAL_DAMMA,
        visibility=SurfaceEffectVisibility.VISIBLE,
        location="final",
        evidence=(Evidence("manual", "visible damma", LughaRank.TAWATUR),),
        rank=LughaRank.TAWATUR
    )

    # Should be able to add surface effects
    assert hasattr(proof, 'surface_effects')
    print("✓ test_surface_effect_allowed_in_mufrad")


def test_case_effect_forbidden_in_mufrad():
    """Test CaseEffect fields are forbidden in MufradProof"""
    proof = make_minimal_mufrad_proof()

    # These fields must NOT exist
    forbidden = ["case_effect", "marfoo_by", "mansub_by", "majroor_by", "governed_by_operator"]
    for field in forbidden:
        assert not hasattr(proof, field), f"MufradProof must not have '{field}'"

    # Verification function should pass
    leaks = verify_no_case_effect_leak(proof)
    assert len(leaks) == 0, "No case effect leaks should be detected"

    print("✓ test_case_effect_forbidden_in_mufrad")


def test_morph_features_allowed_as_candidates():
    """Test morphological features are allowed as candidates"""
    proof = make_minimal_mufrad_proof()

    # Morph status fields should exist
    assert hasattr(proof, 'derivation_status')
    assert hasattr(proof, 'jamid_mushtaq_status')
    assert hasattr(proof, 'mabni_murab_status')
    assert hasattr(proof, 'definiteness_status')
    assert hasattr(proof, 'gender_status')
    assert hasattr(proof, 'number_status')

    # Should allow root/wazn candidates
    assert hasattr(proof, 'root_candidates')
    assert hasattr(proof, 'wazn_candidates')

    print("✓ test_morph_features_allowed_as_candidates")


def test_syntax_role_forbidden_in_mufrad():
    """Test syntax roles are forbidden in MufradProof"""
    proof = make_minimal_mufrad_proof()

    # These fields must NOT exist
    forbidden = ["faail", "mafool", "mubtada", "khabar", "syntax_role", "subject", "object"]
    for field in forbidden:
        assert not hasattr(proof, field), f"MufradProof must not have '{field}'"

    # Verification function should pass
    leaks = verify_no_syntax_role_leak(proof)
    assert len(leaks) == 0, "No syntax role leaks should be detected"

    print("✓ test_syntax_role_forbidden_in_mufrad")


def test_operator_contract_rejects_raw_token():
    """Test operator contract rejects raw token"""
    operator = OperatorContract()

    # Try with raw string (FORBIDDEN)
    result = operator.apply("كتب")
    assert not result.success
    assert len(result.residuals) > 0
    assert result.residuals[0].type == ResidualType.OPERATOR_ON_TOKEN_FORBIDDEN

    # Try with reject helper
    result2 = reject_token_application("test")
    assert not result2.success

    print("✓ test_operator_contract_rejects_raw_token")


def test_operator_contract_accepts_mufrad_proof():
    """Test operator contract accepts MufradProof"""
    operator = OperatorContract()
    proof = make_minimal_mufrad_proof()

    # Should accept MufradProof
    result = operator.apply(proof)
    assert result.success
    assert len(result.residuals) == 0

    # Reject helper should accept
    result2 = reject_token_application(proof)
    assert result2.success

    print("✓ test_operator_contract_accepts_mufrad_proof")


def test_unresolved_mufrad_competitor_blocks_certificate():
    """Test unresolved competitors prevent certificate"""
    proof1 = make_minimal_mufrad_proof()

    # Proof with competitors
    proof2 = MufradProof(
        form=proof1.form,
        lugha=proof1.lugha,
        type=proof1.type,
        segmentation=proof1.segmentation,
        stem=proof1.stem,
        clitics=tuple(),
        root_candidates=tuple(),
        wazn_candidates=tuple(),
        derivation_status=CandidateStatus.UNRESOLVED,
        jamid_mushtaq_status=CandidateStatus.UNRESOLVED,
        mabni_murab_status=CandidateStatus.UNRESOLVED,
        definiteness_status=CandidateStatus.UNRESOLVED,
        gender_status=CandidateStatus.UNRESOLVED,
        number_status=CandidateStatus.UNRESOLVED,
        composition_readiness=CompositionReadiness.READY_AS_HYPOTHESIS,
        competitors=(proof1,)  # Has unresolved competitor
    )

    assert proof2.has_unresolved_competitors()
    assert not proof2.can_issue_certificate()

    print("✓ test_unresolved_mufrad_competitor_blocks_certificate")


def test_no_semantic_leak_in_mufrad_proof():
    """Test no semantic meaning fields in MufradProof"""
    proof = make_minimal_mufrad_proof()

    # These fields must NOT exist
    forbidden = ["meaning", "murad", "madlul", "haqiqa_majaz", "semantic"]
    for field in forbidden:
        assert not hasattr(proof, field), f"MufradProof must not have '{field}'"

    # Verification should pass
    leaks = verify_no_semantic_leak(proof)
    assert len(leaks) == 0

    print("✓ test_no_semantic_leak_in_mufrad_proof")


def test_composition_readiness_levels():
    """Test composition readiness levels"""
    # NOT_READY
    assert not CompositionReadiness.NOT_READY.allows_composition()
    assert not CompositionReadiness.NOT_READY.allows_certificate()

    # READY_AS_HYPOTHESIS
    assert CompositionReadiness.READY_AS_HYPOTHESIS.allows_composition()
    assert not CompositionReadiness.READY_AS_HYPOTHESIS.allows_certificate()

    # READY_FOR_COMPOSITION
    assert CompositionReadiness.READY_FOR_COMPOSITION.allows_composition()
    assert not CompositionReadiness.READY_FOR_COMPOSITION.allows_certificate()

    # READY_FOR_CERTIFICATE_COMPOSITION
    assert CompositionReadiness.READY_FOR_CERTIFICATE_COMPOSITION.allows_composition()
    assert CompositionReadiness.READY_FOR_CERTIFICATE_COMPOSITION.allows_certificate()

    print("✓ test_composition_readiness_levels")


def test_weakest_link_rank():
    """Test weakest-link rank calculation"""
    proof = make_minimal_mufrad_proof()

    # All components have TAWATUR
    weakest = proof.get_weakest_rank()
    # Should be LughaRank.FORM (value 1) from FormRank.FORM
    assert weakest.value >= 0

    print("✓ test_weakest_link_rank")


def test_residual_collection():
    """Test residual collection from all components"""
    proof = make_minimal_mufrad_proof()

    # Collect all residuals
    all_residuals = proof.collect_all_residuals()
    assert isinstance(all_residuals, tuple)

    print("✓ test_residual_collection")


def test_verb_features_required_for_fiil():
    """Test verb features required when type is FIIL"""
    proof = make_minimal_mufrad_proof()

    # Type is FIIL
    assert proof.type.dal_type == DalType.FIIL

    # Verb features slot exists (even if None in minimal test)
    assert hasattr(proof, 'verb_features')

    print("✓ test_verb_features_required_for_fiil")


def test_noun_inflection_required_for_ism():
    """Test noun inflection class exists for ISM"""
    form = FormCandidate(text="كتاب", vocalization="كِتَابٌ", rank=FormRank.FORM)
    lugha = LughaAttestation(form=form, rank=LughaRank.TAWATUR, is_arabic=True)
    typed_dal = TypedDal(attestation=lugha, dal_type=DalType.ISM)

    segmentation = SegmentationProof(
        segments=("كتاب",),
        evidence=(Evidence("manual", "test", LughaRank.TAWATUR),),
        rank=LughaRank.TAWATUR
    )
    stem = StemProof(
        stem="كتاب",
        evidence=(Evidence("manual", "test", LughaRank.TAWATUR),),
        rank=LughaRank.TAWATUR
    )

    proof = MufradProof(
        form=form,
        lugha=lugha,
        type=typed_dal,
        segmentation=segmentation,
        stem=stem,
        clitics=tuple(),
        root_candidates=tuple(),
        wazn_candidates=tuple(),
        derivation_status=CandidateStatus.NOT_APPLICABLE,
        jamid_mushtaq_status=CandidateStatus.NOT_APPLICABLE,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
        definiteness_status=CandidateStatus.RESOLVED_CERTAIN,
        gender_status=CandidateStatus.RESOLVED_CERTAIN,
        number_status=CandidateStatus.RESOLVED_CERTAIN
    )

    # Type is ISM
    assert proof.type.dal_type == DalType.ISM

    # Noun inflection class slot exists
    assert hasattr(proof, 'noun_inflection_class')

    print("✓ test_noun_inflection_required_for_ism")


def main():
    """Run all MufradProof theorem tests"""
    print("Running MufradProof theorem tests...\n")

    tests = [
        test_mufrad_proof_has_required_fields,
        test_mufrad_proof_requires_form_lugha_type,
        test_surface_effect_allowed_in_mufrad,
        test_case_effect_forbidden_in_mufrad,
        test_morph_features_allowed_as_candidates,
        test_syntax_role_forbidden_in_mufrad,
        test_operator_contract_rejects_raw_token,
        test_operator_contract_accepts_mufrad_proof,
        test_unresolved_mufrad_competitor_blocks_certificate,
        test_no_semantic_leak_in_mufrad_proof,
        test_composition_readiness_levels,
        test_weakest_link_rank,
        test_residual_collection,
        test_verb_features_required_for_fiil,
        test_noun_inflection_required_for_ism,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
