"""
Constitutional Tests for PreSyntaxReadinessResult (GARA-FT-1 Boundary)

Tests enforce the 7 constitutional laws from PR #132:
1. No semantic leak (meaning/murad/madlul/ifadah/hukm)
2. No syntax roles (faail/mafool/mubtada/khabar)
3. No case effects - only CaseSignPotential (observation, not judgment)
4. No applied operators (governed_by/governs) - only OperatorTriggerPotential
5. No relations (ISN/TADMIN/TAQYID)
6. No RelationCandidate or OperatorCandidate before RelationAlgebraCore
7. SignifierTokenResult remains boundary-only (not modified)

Additional architectural laws:
8. PreSyntaxReadinessResult is separate object from SignifierTokenResult
9. Rejects failed SignifierTokenResult inputs
10. Preserves underlying MufradProof identity and trace

See: docs/GARA_FT_0_BOUNDARY_SPEC.md (extended for GARA-FT-1)
"""

import pytest
from dataclasses import FrozenInstanceError

from dal_core.presyntax_readiness_result import (
    PreSyntaxReadinessResult,
    create_presyntax_readiness_result,
)
from dal_core.signifier_token_result import (
    SignifierToken,
    SignifierTokenResult,
    create_signifier_token_result,
)
from dal_core.dal_algebra import AlgebraicFailure
from dal_core.mufrad_proof import MufradProof
from dal_core.d_form import FormCandidate
from dal_core.d_lugha import LughaAttestation
from dal_core.d_type import TypedDal, DalType
from dal_core.morph_features import (
    SegmentationProof,
    StemProof,
    CandidateStatus,
)
from dal_core.composition_readiness import CompositionReadiness


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def minimal_mufrad_proof():
    """Minimal valid MufradProof for testing."""
    from dal_core.ranks import FormRank, LughaRank
    from dal_core.evidence import Evidence

    form = FormCandidate(
        text="كتاب",
        vocalization="كِتَابٌ",
        rank=FormRank.FORM
    )
    lugha = LughaAttestation(
        form=form,
        rank=LughaRank.TAWATUR,
        is_arabic=True
    )
    typed_dal = TypedDal(
        attestation=lugha,
        dal_type=DalType.ISM
    )

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

    return MufradProof(
        form=form,
        lugha=lugha,
        type=typed_dal,
        segmentation=segmentation,
        stem=stem,
        clitics=(),
        root_candidates=(),
        wazn_candidates=(),
        derivation_status=CandidateStatus.NOT_APPLICABLE,
        jamid_mushtaq_status=CandidateStatus.NOT_APPLICABLE,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
        definiteness_status=CandidateStatus.NOT_APPLICABLE,
        gender_status=CandidateStatus.RESOLVED_CERTAIN,
        number_status=CandidateStatus.RESOLVED_CERTAIN,
        composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION
    )


@pytest.fixture
def success_signifier_token_result(minimal_mufrad_proof):
    """SignifierTokenResult in success state."""
    return create_signifier_token_result(minimal_mufrad_proof)


@pytest.fixture
def failure_signifier_token_result():
    """SignifierTokenResult in failure state."""
    return SignifierTokenResult(
        signifier_token=None,
        failure=AlgebraicFailure(reason="Test failure")
    )


# ============================================================================
# Constitutional Prohibition Tests (7 Laws)
# ============================================================================


class TestConstitutionalProhibitions:
    """
    دستور المنع - Constitutional prohibition tests

    Each test enforces one constitutional law by attempting to violate it
    and verifying the violation is prevented.
    """

    def test_law_1_readiness_result_forbids_meaning(self, success_signifier_token_result):
        """
        Constitutional Law #1: No Semantic Leak

        PreSyntaxReadinessResult MUST NOT contain semantic fields:
        - meaning, murad, madlul, semantic
        - haqiqa, majaz, ifadah, hukm

        Violation: Attempting to add 'meaning' field to PreSyntaxReadinessResult

        Expected: AttributeError or FrozenInstanceError (frozen dataclass)
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        # Frozen dataclass prevents field addition
        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.meaning = "book"

    def test_law_1_readiness_result_forbids_ifadah(self, success_signifier_token_result):
        """
        Constitutional Law #1: No Semantic Leak (ifadah variant)

        PreSyntaxReadinessResult MUST NOT contain 'ifadah' (pragmatic closure).
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.ifadah = "statement"

    def test_law_1_readiness_result_forbids_hukm(self, success_signifier_token_result):
        """
        Constitutional Law #1: No Semantic Leak (hukm variant)

        PreSyntaxReadinessResult MUST NOT contain 'hukm' (epistemic judgment).
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.hukm = "truth_value"

    def test_law_2_readiness_result_forbids_syntax_role(self, success_signifier_token_result):
        """
        Constitutional Law #2: No Syntax Roles Before Governance

        PreSyntaxReadinessResult MUST NOT contain syntax roles:
        - faail, mafool, mubtada, khabar
        - syntax_role, governed_by, governs
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.syntax_role = "faail"

    def test_law_2_readiness_result_forbids_faail(self, success_signifier_token_result):
        """
        Constitutional Law #2: No Syntax Roles (faail variant)

        PreSyntaxReadinessResult MUST NOT contain 'faail' (subject role).
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.faail = True

    def test_law_3_readiness_result_forbids_case_effect(self, success_signifier_token_result):
        """
        Constitutional Law #3: No Case Effects - Only CaseSignPotential

        PreSyntaxReadinessResult MUST NOT contain case effects:
        - case_effect, raf, nasb, jarr (as grammatical judgments)

        CaseSignPotential (observation) is allowed in the readiness_vector.
        CaseEffect (judgment) is forbidden in the result wrapper.
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.case_effect = "raf"

    def test_law_3_readiness_result_forbids_marfoo_by(self, success_signifier_token_result):
        """
        Constitutional Law #3: No Case Effects (governance variant)

        PreSyntaxReadinessResult MUST NOT contain 'marfoo_by' (governed in raf' case).
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.marfoo_by = "verb"

    def test_law_4_readiness_result_forbids_applied_operator(self, success_signifier_token_result):
        """
        Constitutional Law #4: No Applied Operators - Only OperatorTriggerPotential

        PreSyntaxReadinessResult MUST NOT contain applied operators:
        - applied_operator, operator_binding
        - governs, governed_nodes

        OperatorTriggerPotential (potential) is allowed in the readiness_vector.
        AppliedOperator (governance) is forbidden in the result wrapper.
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.applied_operator = "inna"

    def test_law_4_readiness_result_forbids_governs(self, success_signifier_token_result):
        """
        Constitutional Law #4: No Applied Operators (governance variant)

        PreSyntaxReadinessResult MUST NOT contain 'governs' (governance relation).
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.governs = []

    def test_law_5_readiness_result_forbids_relation(self, success_signifier_token_result):
        """
        Constitutional Law #5: No Relations Before Algebra

        PreSyntaxReadinessResult MUST NOT contain relations:
        - relation, relation_type, relation_binding
        - isn_subject, isn_predicate
        - tadmin_incorporated, taqyid_restricted
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.relation = "ISN"

    def test_law_5_readiness_result_forbids_isn_subject(self, success_signifier_token_result):
        """
        Constitutional Law #5: No Relations (ISN variant)

        PreSyntaxReadinessResult MUST NOT contain 'isn_subject' (ISNAD relation marker).
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.isn_subject = True

    def test_law_6_result_forbids_relation_candidate_import(self):
        """
        Constitutional Law #6: No RelationCandidate Before RelationAlgebraCore

        PreSyntaxReadinessResult MUST NOT produce or reference RelationCandidate.

        Violation: Attempting to import RelationCandidate from this module

        Expected: ImportError or AttributeError
        """
        with pytest.raises((ImportError, AttributeError)):
            from dal_core.presyntax_readiness_result import RelationCandidate

    def test_law_6_result_forbids_operator_candidate_import(self):
        """
        Constitutional Law #6: No OperatorCandidate Before Boundary

        PreSyntaxReadinessResult MUST NOT produce or reference OperatorCandidate.

        OperatorCandidate requires further processing beyond readiness.
        """
        with pytest.raises((ImportError, AttributeError)):
            from dal_core.presyntax_readiness_result import OperatorCandidate

    def test_law_6_result_has_no_relation_candidate_field(self, success_signifier_token_result):
        """
        Constitutional Law #6: No RelationCandidate (field absence)

        PreSyntaxReadinessResult MUST NOT have relation_candidate field.
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        assert not hasattr(result, 'relation_candidate')
        assert not hasattr(result, 'operator_candidate')

    def test_law_7_signifier_token_result_unchanged(self, success_signifier_token_result):
        """
        Constitutional Law #7: SignifierTokenResult Remains Boundary-Only

        PreSyntaxReadinessResult MUST NOT modify SignifierTokenResult.

        Critical distinction:
        - SignifierTokenResult is input boundary (preserved)
        - PreSyntaxReadinessResult is separate output boundary
        - No mutation, only consumption
        """
        original_token = success_signifier_token_result.signifier_token
        original_proof = original_token.proof if original_token else None

        result = create_presyntax_readiness_result(success_signifier_token_result)

        # SignifierTokenResult unchanged
        assert result.source_token_result is success_signifier_token_result
        assert result.source_token_result.signifier_token is original_token

        # Underlying proof unchanged
        if original_token:
            assert result.source_token_result.signifier_token.proof is original_proof


# ============================================================================
# Result Semantics Tests
# ============================================================================


class TestResultSemantics:
    """
    دلالات النتيجة - Result semantics tests

    Verifies that PreSyntaxReadinessResult is separate from SignifierTokenResult.
    """

    def test_result_is_separate_from_signifier_token_result(self, success_signifier_token_result):
        """
        Result Semantics: PreSyntaxReadinessResult ≠ SignifierTokenResult

        Critical Distinction:
        - SignifierTokenResult: MufradProof → SignifierToken wrapper
        - PreSyntaxReadinessResult: SignifierTokenResult → PreSyntaxMufradVector

        These are SEPARATE boundary layers, not enrichments.
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        # Different types
        assert not isinstance(result, SignifierTokenResult)
        assert isinstance(result, PreSyntaxReadinessResult)

        # Contains SignifierTokenResult as input
        assert isinstance(result.source_token_result, SignifierTokenResult)

    def test_result_success_case(self, success_signifier_token_result):
        """
        Result Semantics: Success case structure

        Success result contains:
        - source_token_result: SignifierTokenResult (input)
        - readiness_vector: PreSyntaxMufradVector (output)
        - failure: None
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        assert result.is_success
        assert not result.is_failure
        assert result.source_token_result is success_signifier_token_result
        assert result.readiness_vector is not None
        assert result.failure is None

    def test_result_failure_case_from_failed_input(self, failure_signifier_token_result):
        """
        Result Semantics: Failure case from failed input

        Failed SignifierTokenResult → Failed PreSyntaxReadinessResult

        Failure result contains:
        - source_token_result: SignifierTokenResult (failed input)
        - readiness_vector: None
        - failure: AlgebraicFailure (propagated)
        """
        result = create_presyntax_readiness_result(failure_signifier_token_result)

        assert result.is_failure
        assert not result.is_success
        assert result.source_token_result is failure_signifier_token_result
        assert result.readiness_vector is None
        assert result.failure is not None
        assert "Input SignifierTokenResult failed" in result.failure.reason

    def test_result_mutual_exclusion_both_present(self, success_signifier_token_result):
        """
        Result Invariant: Cannot have both success AND failure

        Violation: Both readiness_vector and failure present

        Expected: ValueError on construction
        """
        from dal_core.presyntax_vector import PreSyntaxMufradVector

        # Create mock readiness_vector (minimal)
        mock_vector = success_signifier_token_result.signifier_token.proof.to_presyntax_vector()

        with pytest.raises(ValueError, match="exactly one"):
            PreSyntaxReadinessResult(
                source_token_result=success_signifier_token_result,
                readiness_vector=mock_vector,
                failure=AlgebraicFailure(reason="Test"),
            )

    def test_result_mutual_exclusion_both_absent(self, success_signifier_token_result):
        """
        Result Invariant: Cannot have neither success NOR failure

        Violation: Both readiness_vector and failure are None

        Expected: ValueError on construction
        """
        with pytest.raises(ValueError, match="exactly one"):
            PreSyntaxReadinessResult(
                source_token_result=success_signifier_token_result,
                readiness_vector=None,
                failure=None,
            )


# ============================================================================
# Boundary Validation Tests
# ============================================================================


class TestBoundaryValidation:
    """
    اختبارات الحدود - Boundary validation tests

    Verifies GARA-FT-1 boundary constraints.
    """

    def test_readiness_result_requires_signifier_token_result(self):
        """
        Boundary: PreSyntaxReadinessResult requires SignifierTokenResult input

        Violation: Passing non-SignifierTokenResult

        Expected: TypeError
        """
        with pytest.raises(TypeError, match="requires SignifierTokenResult"):
            PreSyntaxReadinessResult(
                source_token_result="not a result",
                readiness_vector=None,
                failure=AlgebraicFailure(reason="Test")
            )

    def test_readiness_result_preserves_immutability(self, success_signifier_token_result):
        """
        Boundary: PreSyntaxReadinessResult is frozen (immutable)

        Cannot modify result fields after construction.
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        # Cannot reassign fields
        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.readiness_vector = None

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.failure = AlgebraicFailure(reason="Test")

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.source_token_result = None

    def test_create_function_success_path(self, success_signifier_token_result):
        """
        Factory Function: create_presyntax_readiness_result success path

        Valid SignifierTokenResult → Success result with PreSyntaxMufradVector
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        assert result.is_success
        assert result.readiness_vector is not None
        assert result.failure is None

    def test_create_function_rejects_failed_input(self, failure_signifier_token_result):
        """
        Factory Function: create_presyntax_readiness_result rejects failed input

        Failed SignifierTokenResult → Failure result
        """
        result = create_presyntax_readiness_result(failure_signifier_token_result)

        assert result.is_failure
        assert result.readiness_vector is None
        assert result.failure is not None

    def test_create_function_invalid_input_type(self):
        """
        Factory Function: create_presyntax_readiness_result invalid input type

        Non-SignifierTokenResult → Failure result
        """
        result = create_presyntax_readiness_result("not a result")

        assert result.is_failure
        assert result.readiness_vector is None
        assert result.failure is not None
        assert "Expected SignifierTokenResult" in result.failure.reason


# ============================================================================
# Layer Separation Tests
# ============================================================================


class TestLayerSeparation:
    """
    اختبارات فصل الطبقات - Layer separation tests

    Verifies architectural separation between boundary layers.
    """

    def test_layer_separation_signifier_token_result_unchanged(
        self, success_signifier_token_result
    ):
        """
        Layer Separation: SignifierTokenResult NOT modified by readiness extraction

        Critical architectural law:
        - PreSyntaxReadinessResult consumes SignifierTokenResult
        - Does NOT mutate or enrich it
        - Separate object, separate boundary
        """
        # Capture original state
        original_id = id(success_signifier_token_result)
        original_token = success_signifier_token_result.signifier_token
        original_failure = success_signifier_token_result.failure

        # Extract readiness
        result = create_presyntax_readiness_result(success_signifier_token_result)

        # SignifierTokenResult identity preserved
        assert id(success_signifier_token_result) == original_id
        assert success_signifier_token_result.signifier_token is original_token
        assert success_signifier_token_result.failure is original_failure

        # No new fields added to SignifierTokenResult
        assert not hasattr(success_signifier_token_result, 'readiness_vector')
        assert not hasattr(success_signifier_token_result, 'presyntax_vector')

    def test_layer_separation_mufrad_proof_identity_preserved(
        self, minimal_mufrad_proof
    ):
        """
        Layer Separation: MufradProof identity preserved through both boundaries

        Pipeline:
        MufradProof → SignifierTokenResult → PreSyntaxReadinessResult

        MufradProof identity must be preserved (not copied, not mutated).
        """
        # Create SignifierTokenResult
        token_result = create_signifier_token_result(minimal_mufrad_proof)

        # Create PreSyntaxReadinessResult
        readiness_result = create_presyntax_readiness_result(token_result)

        # MufradProof identity preserved
        assert token_result.signifier_token.proof is minimal_mufrad_proof
        assert readiness_result.source_token_result.signifier_token.proof is minimal_mufrad_proof

    def test_layer_separation_no_cross_boundary_fields(
        self, success_signifier_token_result
    ):
        """
        Layer Separation: No cross-boundary field contamination

        SignifierTokenResult fields:
        - signifier_token
        - failure

        PreSyntaxReadinessResult fields:
        - source_token_result
        - readiness_vector
        - failure

        No overlap, no contamination.
        """
        result = create_presyntax_readiness_result(success_signifier_token_result)

        # SignifierTokenResult does NOT have readiness fields
        assert not hasattr(success_signifier_token_result, 'readiness_vector')
        assert not hasattr(success_signifier_token_result, 'source_token_result')

        # PreSyntaxReadinessResult does NOT have token fields
        assert not hasattr(result, 'signifier_token')

        # Each has its own failure field (separate boundaries)
        assert hasattr(success_signifier_token_result, 'failure')
        assert hasattr(result, 'failure')
