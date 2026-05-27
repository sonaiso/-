"""
Constitutional Tests for SignifierTokenResult (GARA-FT-0 Boundary)

Tests enforce the 6 constitutional laws from PR #130:
1. No semantic leak (meaning/murad/madlul/ifadah/hukm)
2. No syntax roles (faail/mafool/mubtada/khabar)
3. No case effects (raf/nasb/jarr as judgments)
4. No applied operators (governed_by/governs)
5. No relations (ISN/TADMIN/TAQYID)
6. No RelationCandidate before RelationAlgebraCore

See: docs/GARA_FT_0_BOUNDARY_SPEC.md
"""

import pytest
from dataclasses import FrozenInstanceError

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
from dal_core.mufrad_axes import BinaaJudgment, IshtiqaqJudgment


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


# ============================================================================
# Constitutional Prohibition Tests (6 Laws)
# ============================================================================


class TestConstitutionalProhibitions:
    """
    دستور المنع - Constitutional prohibition tests

    Each test enforces one constitutional law by attempting to violate it
    and verifying the violation is prevented.
    """

    def test_law_1_signifier_token_forbids_meaning(self, minimal_mufrad_proof):
        """
        Constitutional Law #1: No Semantic Leak

        SignifierToken MUST NOT contain semantic fields:
        - meaning, murad, madlul, semantic
        - haqiqa, majaz, ifadah, hukm

        Violation: Attempting to add 'meaning' field to SignifierToken

        Expected: AttributeError or FrozenInstanceError (frozen dataclass)

        Rationale: SignifierToken represents الدال (signifier) only,
                   not المدلول (signified). Meaning assignment requires
                   DalMadlulContract which doesn't exist yet.
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        # Frozen dataclass prevents field addition
        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.meaning = "book"

    def test_law_1_signifier_token_forbids_murad(self, minimal_mufrad_proof):
        """
        Constitutional Law #1: No Semantic Leak (murad variant)

        SignifierToken MUST NOT contain 'murad' (intended meaning).
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.murad = "intended"

    def test_law_1_signifier_token_forbids_ifadah(self, minimal_mufrad_proof):
        """
        Constitutional Law #1: No Semantic Leak (ifadah variant)

        SignifierToken MUST NOT contain 'ifadah' (pragmatic closure).
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.ifadah = "statement"

    def test_law_2_signifier_token_forbids_syntax_role(self, minimal_mufrad_proof):
        """
        Constitutional Law #2: No Syntax Roles Before Governance

        SignifierToken MUST NOT contain syntax roles:
        - faail, mafool, mubtada, khabar
        - syntax_role, governed_by, governs

        Violation: Attempting to add 'syntax_role' field

        Expected: AttributeError or FrozenInstanceError

        Rationale: Syntax roles require operator governance,
                   which happens in composition layer (U₁₁+).
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.syntax_role = "faail"

    def test_law_2_signifier_token_forbids_faail(self, minimal_mufrad_proof):
        """
        Constitutional Law #2: No Syntax Roles (faail variant)

        SignifierToken MUST NOT contain 'faail' (subject role).
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.faail = True

    def test_law_3_signifier_token_forbids_case_effect(self, minimal_mufrad_proof):
        """
        Constitutional Law #3: No Case Effects Before Operators

        SignifierToken MUST NOT contain case effects:
        - case_effect, raf, nasb, jarr
        - marfoo_by, mansub_by, majroor_by

        Violation: Attempting to add 'case_effect' field

        Expected: AttributeError or FrozenInstanceError

        Rationale: Case effects are grammatical judgments produced by
                   operator governance, not surface observations.
                   CaseSignPotential (allowed) ≠ CaseEffect (forbidden).
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.case_effect = "raf"

    def test_law_3_signifier_token_forbids_marfoo_by(self, minimal_mufrad_proof):
        """
        Constitutional Law #3: No Case Effects (governance variant)

        SignifierToken MUST NOT contain 'marfoo_by' (governed in raf' case).
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.marfoo_by = "verb"

    def test_law_4_signifier_token_forbids_applied_operator(self, minimal_mufrad_proof):
        """
        Constitutional Law #4: No Applied Operators Before Selection

        SignifierToken MUST NOT contain applied operators:
        - applied_operator, operator_binding
        - governs, governed_nodes

        Violation: Attempting to add 'applied_operator' field

        Expected: AttributeError or FrozenInstanceError

        Rationale: Applied operators are governance results,
                   not pre-syntactic potentials.
                   OperatorTriggerPotential (allowed) ≠ AppliedOperator (forbidden).
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.applied_operator = "inna"

    def test_law_4_signifier_token_forbids_governs(self, minimal_mufrad_proof):
        """
        Constitutional Law #4: No Applied Operators (governance variant)

        SignifierToken MUST NOT contain 'governs' (governance relation).
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.governs = []

    def test_law_5_signifier_token_forbids_relation(self, minimal_mufrad_proof):
        """
        Constitutional Law #5: No Relations Before Algebra

        SignifierToken MUST NOT contain relations:
        - relation, relation_type, relation_binding
        - isn_subject, isn_predicate
        - tadmin_incorporated, taqyid_restricted

        Violation: Attempting to add 'relation' field

        Expected: AttributeError or FrozenInstanceError

        Rationale: Relations (ISN/TADMIN/TAQYID/WASF/IDAFAH) require
                   RelationAlgebraCore, which is a preventing boundary.
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.relation = "ISN"

    def test_law_5_signifier_token_forbids_isn_subject(self, minimal_mufrad_proof):
        """
        Constitutional Law #5: No Relations (ISN variant)

        SignifierToken MUST NOT contain 'isn_subject' (ISNAD relation marker).
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.isn_subject = True

    def test_law_6_result_forbids_relation_candidate_import(self):
        """
        Constitutional Law #6: No RelationCandidate Before RelationAlgebraCore

        SignifierTokenResult MUST NOT produce or reference RelationCandidate.

        Violation: Attempting to import RelationCandidate from this module

        Expected: ImportError or AttributeError

        Rationale: RelationCandidate production requires RelationAlgebraCore
                   activation. GARA-FT-0 is pre-algebra boundary.
        """
        with pytest.raises((ImportError, AttributeError)):
            from dal_core.signifier_token_result import RelationCandidate

    def test_law_6_result_has_no_relation_candidate_field(self, minimal_mufrad_proof):
        """
        Constitutional Law #6: No RelationCandidate (field absence)

        SignifierTokenResult MUST NOT have relation_candidate field.
        """
        result = SignifierTokenResult(
            signifier_token=SignifierToken(proof=minimal_mufrad_proof),
            failure=None
        )

        # Should not have relation_candidate field
        assert not hasattr(result, 'relation_candidate')


# ============================================================================
# Result Semantics Tests
# ============================================================================


class TestResultSemantics:
    """
    دلالات النتيجة - Result semantics tests

    Verifies that Result is wrapper, not payload.
    """

    def test_result_is_wrapper_not_token(self, minimal_mufrad_proof):
        """
        Result Semantics: Result ≠ Token

        SignifierTokenResult wraps SignifierToken, is not token itself.

        Critical Distinction:
        - Result = wrapper with success/failure discriminator
        - Token = payload (operational unit)

        This prevents conceptual confusion between wrapper and content.
        """
        result = SignifierTokenResult(
            signifier_token=SignifierToken(proof=minimal_mufrad_proof),
            failure=None
        )

        # Result has wrapper fields
        assert hasattr(result, 'signifier_token')
        assert hasattr(result, 'failure')

        # Result is NOT a token
        assert not isinstance(result, SignifierToken)

        # But result CONTAINS a token
        assert isinstance(result.signifier_token, SignifierToken)

    def test_result_success_case(self, minimal_mufrad_proof):
        """
        Result Semantics: Success case structure

        Success result contains:
        - signifier_token: SignifierToken
        - failure: None
        """
        token = SignifierToken(proof=minimal_mufrad_proof)
        result = SignifierTokenResult(
            signifier_token=token,
            failure=None
        )

        assert result.is_success
        assert not result.is_failure
        assert result.signifier_token is token
        assert result.failure is None

    def test_result_failure_case(self):
        """
        Result Semantics: Failure case structure

        Failure result contains:
        - signifier_token: None
        - failure: AlgebraicFailure
        """
        failure = AlgebraicFailure(reason="Test failure")
        result = SignifierTokenResult(
            signifier_token=None,
            failure=failure
        )

        assert result.is_failure
        assert not result.is_success
        assert result.signifier_token is None
        assert result.failure is failure

    def test_result_mutual_exclusion_both_present(self, minimal_mufrad_proof):
        """
        Result Invariant: Cannot have both success AND failure

        Violation: Both signifier_token and failure present

        Expected: ValueError on construction
        """
        with pytest.raises(ValueError, match="exactly one"):
            SignifierTokenResult(
                signifier_token=SignifierToken(proof=minimal_mufrad_proof),
                failure=AlgebraicFailure(reason="Test"),
            )

    def test_result_mutual_exclusion_both_absent(self):
        """
        Result Invariant: Cannot have neither success NOR failure

        Violation: Both signifier_token and failure are None

        Expected: ValueError on construction
        """
        with pytest.raises(ValueError, match="exactly one"):
            SignifierTokenResult(
                signifier_token=None,
                failure=None,
            )


# ============================================================================
# Boundary Validation Tests
# ============================================================================


class TestBoundaryValidation:
    """
    اختبارات الحدود - Boundary validation tests

    Verifies GARA-FT-0 boundary constraints.
    """

    def test_signifier_token_requires_mufrad_proof(self):
        """
        Boundary: SignifierToken requires MufradProof input

        Violation: Passing non-MufradProof to SignifierToken

        Expected: TypeError
        """
        with pytest.raises(TypeError, match="requires MufradProof"):
            SignifierToken(proof="not a proof")

    def test_signifier_token_preserves_proof_immutability(self, minimal_mufrad_proof):
        """
        Boundary: SignifierToken is frozen (immutable)

        SignifierToken inherits immutability from frozen dataclass.
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        # Cannot reassign proof
        with pytest.raises((AttributeError, FrozenInstanceError)):
            token.proof = minimal_mufrad_proof  # Try to reassign

    def test_create_function_success_path(self, minimal_mufrad_proof):
        """
        Factory Function: create_signifier_token_result success path

        Valid MufradProof → Success result with SignifierToken
        """
        result = create_signifier_token_result(minimal_mufrad_proof)

        assert result.is_success
        assert result.signifier_token is not None
        assert result.signifier_token.proof == minimal_mufrad_proof
        assert result.failure is None

    def test_create_function_invalid_proof_type(self):
        """
        Factory Function: create_signifier_token_result failure path

        Invalid input → Failure result with AlgebraicFailure
        """
        result = create_signifier_token_result("not a proof")

        assert result.is_failure
        assert result.signifier_token is None
        assert result.failure is not None
        assert "Expected MufradProof" in result.failure.reason

    def test_result_frozen_immutability(self, minimal_mufrad_proof):
        """
        Boundary: SignifierTokenResult is frozen (immutable)

        Cannot modify result fields after construction.
        """
        result = SignifierTokenResult(
            signifier_token=SignifierToken(proof=minimal_mufrad_proof),
            failure=None
        )

        # Cannot reassign fields
        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.signifier_token = None

        with pytest.raises((AttributeError, FrozenInstanceError)):
            result.failure = AlgebraicFailure(reason="Test")


# ============================================================================
# Anti-Axiom Tests (Future Neural/Syntax Prevention)
# ============================================================================


class TestAntiAxiomPreventions:
    """
    منع البديهيات - Anti-axiom tests

    Prevents architectural violations and jumps.
    """

    def test_mufrad_proof_not_neural_token(self, minimal_mufrad_proof):
        """
        Anti-Axiom: MufradProof does NOT become Neural token directly

        MufradProof → SignifierToken (algebraic wrapper)
        NOT:
        MufradProof → NeuralToken (requires GARA-T5, deferred)

        This prevents the jump: MufradProof → GARA-T5
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        # Should not have neural encoding fields
        assert not hasattr(token, 'neural_embedding')
        assert not hasattr(token, 'encoder_hidden_state')
        assert not hasattr(token, 'transformer_output')

    def test_signifier_token_not_syntax_node(self, minimal_mufrad_proof):
        """
        Anti-Axiom: SignifierToken is NOT a syntax graph node

        SignifierToken is operational unit, not graph vertex.

        This prevents the jump: SignifierToken → SyntaxNode
        """
        token = SignifierToken(proof=minimal_mufrad_proof)

        # Should not have graph node fields
        assert not hasattr(token, 'edges')
        assert not hasattr(token, 'incoming_edges')
        assert not hasattr(token, 'outgoing_edges')
        assert not hasattr(token, 'graph_position')

    def test_result_does_not_contain_presyntax_vector(self, minimal_mufrad_proof):
        """
        Boundary: SignifierTokenResult does NOT contain PreSyntaxMufradVector

        GARA-FT-0 boundary spec (section 6.2) shows PreSyntaxMufradVector
        as PLACEHOLDER in the spec, but it already exists independently
        in presyntax_vector.py.

        SignifierTokenResult is minimal: token + failure only.
        PreSyntaxMufradVector is extracted separately from MufradProof.

        This verifies the boundary: Result is just wrapper, not full interface.
        """
        result = create_signifier_token_result(minimal_mufrad_proof)

        # Result contains only token and failure
        assert hasattr(result, 'signifier_token')
        assert hasattr(result, 'failure')

        # Result does NOT contain presyntax_readiness
        # (that was in the spec as future possibility, but we're minimal)
        assert not hasattr(result, 'presyntax_readiness')
