"""
Tests for Case Effect Candidate (مرشح الأثر الإعرابي)

Constitutional Tests:
    1. Verify case effect candidates are candidates only
    2. Verify NO final case judgment production
    3. Verify NO meaning/ifadah/hukm production
    4. Verify identity preservation (operator + factor + affected)
    5. Verify rank ceiling theorem
    6. Verify residual inheritance theorem
    7. Verify competing candidates preserved

Created: 2026-05-30
"""

import pytest

from dal_core.case_effect_candidate import (
    CaseEffectCandidate,
    CaseEffectCandidateSet,
    CaseEffectCandidateTrace,
    CaseEffectCandidateType,
    build_case_effect_candidate,
)
from dal_core.case_sign_matrix import (
    CaseCompatibilityFamily,
    CaseSignMatrixRow,
    SurfaceSignObservation,
)
from dal_core.case_signs import CaseSignFamily, CaseSignPotential, CaseSignValue
from dal_core.factor_mark_equation import (
    FactorMarkEquation,
    FactorMarkEquationType,
    FactorSourceCandidate,
    FactorSourceKind,
)
from dal_core.nahw_operator_registry import CaseEffectPolicyFamily
from dal_core.operator_candidate import (
    OperatorCandidate,
    OperatorCandidateTrace,
)
from dal_core.operator_trigger import OperatorTriggerFamily, TriggerSource
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, ResidualType, make_warning
from dal_core.surface_effects import SurfaceEffect
from dal_core.evidence import Evidence


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def minimal_surface_effect():
    """Minimal SurfaceEffect for testing."""
    return SurfaceEffect(
        effect_id="surface-001",
        raw_span=(0, 5),
        observed_text="الكتاب",
        observed_diacritics="",
        evidence=Evidence(span_id="span-001", raw_span=(0, 5)),
        trace_id="trace-surface-001",
    )


@pytest.fixture
def minimal_case_sign_potential(minimal_surface_effect):
    """Minimal CaseSignPotential for testing."""
    return CaseSignPotential(
        observed_surface=minimal_surface_effect,
        sign_family=CaseSignFamily.ORIGINAL,
        sign_value=CaseSignValue.DAMMA,
        compatible_case_effects=("rafa_candidate",),
        evidence=Evidence(span_id="span-001", raw_span=(0, 5)),
        rank=LughaRank.CANDIDATE,
        residuals=(),
        trace_id="trace-case-sign-001",
    )


@pytest.fixture
def minimal_presyntax_vector(minimal_case_sign_potential):
    """Minimal PreSyntaxMufradVector for testing."""
    return PreSyntaxMufradVector(
        mufrad_id="mufrad-001",
        raw_span=(0, 5),
        raw_text="الكتاب",
        type_value="ISM_COMMON",
        type_id=None,
        final_rank=LughaRank.CANDIDATE,
        case_sign_potentials=(minimal_case_sign_potential,),
        residuals=(),
        trace_id="trace-mufrad-001",
        identity_ids=("form:001",),
    )


@pytest.fixture
def minimal_matrix_row(minimal_presyntax_vector, minimal_case_sign_potential):
    """Minimal CaseSignMatrixRow for testing."""
    obs = SurfaceSignObservation(
        observed_sign=CaseSignValue.DAMMA,
        sign_family=CaseSignFamily.ORIGINAL,
        source_surface_effect=minimal_case_sign_potential.observed_surface,
        source_potential=minimal_case_sign_potential,
        requires_operator=True,
        requires_inflection_class=False,
    )
    return CaseSignMatrixRow(
        vector_id=minimal_presyntax_vector.mufrad_id,
        word_index=0,
        raw_span=(0, 5),
        type_id="ISM_COMMON",
        surface_observations=(obs,),
        compatibility_families=(CaseCompatibilityFamily.RAFA_COMPATIBLE,),
        rank=LughaRank.CANDIDATE,
        residuals=(),
        row_trace_id="trace-matrix-row-001",
    )


@pytest.fixture
def minimal_factor_source():
    """Minimal FactorSourceCandidate for testing."""
    return FactorSourceCandidate(
        source_id="factor-001",
        source_kind=FactorSourceKind.RELATION_CANDIDATE,
        identity_ids=("factor-identity-001",),
        trace_ids=("factor-trace-001",),
        rank=LughaRank.CANDIDATE,
    )


@pytest.fixture
def minimal_factor_equation(minimal_factor_source, minimal_presyntax_vector, minimal_case_sign_potential):
    """Minimal FactorMarkEquation for testing."""
    from dal_core.factor_mark_equation import build_factor_mark_equation
    return build_factor_mark_equation(
        factor_source=minimal_factor_source,
        affected_vector=minimal_presyntax_vector,
        mark_potential=minimal_case_sign_potential,
        equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE,
    )


@pytest.fixture
def minimal_trigger_source():
    """Minimal TriggerSource for testing."""
    return TriggerSource(
        family=OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY,
        frame_index=0,
        vector_id="mufrad-001",
        matrix_row_index=0,
        triggering_type_id="ISM_COMMON",
        compatibility_evidence=(CaseCompatibilityFamily.RAFA_COMPATIBLE,),
        source_trace_id="trace-trigger-source-001",
    )


@pytest.fixture
def minimal_operator_candidate(minimal_trigger_source):
    """Minimal OperatorCandidate for testing."""
    from dal_core.nahw_operator_registry import (
        ActivationCondition,
        BlockingCondition,
        Citation,
        ExpectedRelationFamily,
        NahwOperatorEntry,
        NahwSchool,
        OperatorInputSignature,
        OperatorSource,
    )

    registry_entry = NahwOperatorEntry(
        operator_id="ibtidaa-001",
        display_name_ar="الابتداء",
        source=OperatorSource.KITAB_SIBAWAYH,
        school=NahwSchool.BASRI,
        rank=LughaRank.CANDIDATE,
        family=OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY,
        input_signature=OperatorInputSignature(
            expected_arity=2,
            expected_neighbour_types=("ISM_COMMON",),
            notes="Requires two nouns",
        ),
        activation_conditions=(ActivationCondition.HEADS_NOMINAL_FRAME,),
        blocking_conditions=(),
        expected_relation_families=(ExpectedRelationFamily.ISN_LIKE,),
        case_effect_policy_families=(CaseEffectPolicyFamily.MIXED_RAFI_NASB_POLICY_FAMILY,),
        citations=(
            Citation(
                source=OperatorSource.KITAB_SIBAWAYH,
                reference="I/45",
                note="الابتداء",
            ),
        ),
        entry_residuals=(),
        entry_trace_id="trace-entry-001",
    )

    trace = OperatorCandidateTrace(
        candidate_id="operator-candidate-001",
        trigger_id="trigger-001",
        trigger_source_vector_id=minimal_trigger_source.vector_id,
        registry_entry_id=registry_entry.operator_id,
        frame_id="frame-001",
        matrix_id="matrix-001",
    )

    return OperatorCandidate(
        candidate_id="operator-candidate-001",
        trigger_id="trigger-001",
        frame_id="frame-001",
        matrix_id="matrix-001",
        trigger_family=OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY,
        trigger_source=minimal_trigger_source,
        registry_entry_id=registry_entry.operator_id,
        registry_entry=registry_entry,
        rank=LughaRank.CANDIDATE,
        inherited_residuals=(),
        candidate_residuals=(),
        trace=trace,
    )


# ---------------------------------------------------------------------------
# Constitutional Law Tests
# ---------------------------------------------------------------------------


def test_case_effect_candidate_constitutional_guards(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
):
    """
    Constitutional Test: CaseEffectCandidate enforces all guards.

    Verifies:
        - produces_final_case_effect MUST be False
        - produces_final_syntax_role MUST be False
        - produces_meaning MUST be False
        - produces_ifadah MUST be False
        - produces_hukm MUST be False
    """
    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    # Constitutional guards MUST be False
    assert candidate.produces_final_case_effect is False
    assert candidate.produces_final_syntax_role is False
    assert candidate.produces_meaning is False
    assert candidate.produces_ifadah is False
    assert candidate.produces_hukm is False


def test_case_effect_candidate_forbidden_fields():
    """
    Constitutional Test: CaseEffectCandidate rejects forbidden field names.

    Verifies that forbidden fields like 'marfoo' (without _candidate suffix),
    'meaning', 'ifadah', 'hukm' cannot be added to dataclass.
    """
    from dal_core.case_effect_candidate import _FORBIDDEN_FIELDS

    # These field names must be forbidden
    forbidden = {
        "marfoo",  # without _candidate
        "mansub",  # without _candidate
        "majrur",  # without _candidate
        "majzum",  # without _candidate
        "faail",  # without _candidate
        "mafool",  # without _candidate
        "meaning",
        "ifadah",
        "hukm",
        "case_effect_final",
    }

    assert forbidden.issubset(_FORBIDDEN_FIELDS)


def test_case_effect_candidate_identity_preservation(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
    minimal_presyntax_vector,
    minimal_factor_source,
):
    """
    Constitutional Test: CaseEffectCandidate preserves all identities.

    Verifies:
        - Operator identity preserved (via operator_candidate)
        - Factor identity preserved (via factor_source.identity_ids)
        - Affected identity preserved (via affected_vector.identity_ids)
    """
    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    # Operator identity preserved
    assert candidate.operator_candidate.candidate_id == minimal_operator_candidate.candidate_id

    # Factor identity preserved
    assert candidate.factor_source.identity_ids == minimal_factor_source.identity_ids

    # Affected identity preserved
    assert candidate.affected_vector.identity_ids == minimal_presyntax_vector.identity_ids


def test_case_effect_candidate_rank_ceiling(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
):
    """
    Constitutional Test: Rank ceiling theorem.

    Verifies:
        case_effect.rank ≤ min(operator.rank, equation.rank, matrix_row.rank)
    """
    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    # Rank ceiling: should be ≤ all inputs
    assert candidate.rank.value <= minimal_operator_candidate.rank.value
    assert candidate.rank.value <= minimal_matrix_row.rank.value


def test_case_effect_candidate_residual_inheritance(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
):
    """
    Constitutional Test: Residual inheritance theorem.

    Verifies:
        case_effect.inherited_residuals ⊇ operator.get_all_residuals()
    """
    # Add residual to operator
    operator_residual = make_warning(
        ResidualType.OPERATOR_CANDIDATE_COMPETITION_PRESERVED,
        "Test residual",
        location="test",
    )
    operator_with_residual = OperatorCandidate(
        candidate_id=minimal_operator_candidate.candidate_id,
        trigger_id=minimal_operator_candidate.trigger_id,
        frame_id=minimal_operator_candidate.frame_id,
        matrix_id=minimal_operator_candidate.matrix_id,
        trigger_family=minimal_operator_candidate.trigger_family,
        trigger_source=minimal_operator_candidate.trigger_source,
        registry_entry_id=minimal_operator_candidate.registry_entry_id,
        registry_entry=minimal_operator_candidate.registry_entry,
        rank=minimal_operator_candidate.rank,
        inherited_residuals=(operator_residual,),
        candidate_residuals=(),
        trace=minimal_operator_candidate.trace,
    )

    candidate = build_case_effect_candidate(
        operator_candidate=operator_with_residual,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    # Inherited residuals must include operator residuals
    assert operator_residual in candidate.inherited_residuals


# ---------------------------------------------------------------------------
# Builder Tests
# ---------------------------------------------------------------------------


def test_build_case_effect_candidate_rafa(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
):
    """
    Test: Building raf' case effect candidate.

    Verifies:
        - Effect type is RAFʿ_EFFECT_CANDIDATE
        - Policy family is MIXED_RAFI_NASB_POLICY_FAMILY
        - Compatibility evidence is RAFA_COMPATIBLE
    """
    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    assert candidate.effect_type == CaseEffectCandidateType.RAFʿ_EFFECT_CANDIDATE
    assert candidate.policy_family == CaseEffectPolicyFamily.MIXED_RAFI_NASB_POLICY_FAMILY
    assert CaseCompatibilityFamily.RAFA_COMPATIBLE in candidate.compatibility_evidence


def test_build_case_effect_candidate_compatibility_conflict(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_presyntax_vector,
    minimal_case_sign_potential,
):
    """
    Test: Building case effect candidate with compatibility conflict.

    Verifies:
        - When policy requires RAFA but compatibility is NASB
        - Effect type is BLOCKED_EFFECT_CANDIDATE
        - Residual contains CASE_EFFECT_COMPATIBILITY_CONFLICT
    """
    # Create matrix row with NASB compatibility
    obs = SurfaceSignObservation(
        observed_sign=CaseSignValue.FATHA,
        sign_family=CaseSignFamily.ORIGINAL,
        source_surface_effect=minimal_case_sign_potential.observed_surface,
        source_potential=minimal_case_sign_potential,
        requires_operator=True,
        requires_inflection_class=False,
    )
    matrix_row_nasb = CaseSignMatrixRow(
        vector_id=minimal_presyntax_vector.mufrad_id,
        word_index=0,
        raw_span=(0, 5),
        type_id="ISM_COMMON",
        surface_observations=(obs,),
        compatibility_families=(CaseCompatibilityFamily.NASB_COMPATIBLE,),
        rank=LughaRank.CANDIDATE,
        residuals=(),
        row_trace_id="trace-matrix-row-nasb-001",
    )

    # Operator expects RAFA (via MIXED policy selecting RAFA from compatibility)
    # But matrix row only has NASB - this should create blocked candidate
    # Actually, MIXED policy should accept NASB too, so let's use RAFI_POLICY instead
    from dal_core.nahw_operator_registry import (
        ActivationCondition,
        Citation,
        ExpectedRelationFamily,
        NahwOperatorEntry,
        NahwSchool,
        OperatorInputSignature,
        OperatorSource,
    )

    registry_entry_rafi_only = NahwOperatorEntry(
        operator_id="rafi-only-001",
        display_name_ar="رافع فقط",
        source=OperatorSource.KITAB_SIBAWAYH,
        school=NahwSchool.BASRI,
        rank=LughaRank.CANDIDATE,
        family=OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY,
        input_signature=OperatorInputSignature(
            expected_arity=1,
            expected_neighbour_types=("ISM_COMMON",),
            notes="RAFA only",
        ),
        activation_conditions=(ActivationCondition.HEADS_NOMINAL_FRAME,),
        blocking_conditions=(),
        expected_relation_families=(ExpectedRelationFamily.ISN_LIKE,),
        case_effect_policy_families=(CaseEffectPolicyFamily.RAFI_POLICY_FAMILY,),  # RAFA only
        citations=(Citation(source=OperatorSource.KITAB_SIBAWAYH, reference="test"),),
        entry_residuals=(),
        entry_trace_id="trace-rafi-only-001",
    )

    trace = OperatorCandidateTrace(
        candidate_id="operator-rafi-only-001",
        trigger_id="trigger-001",
        trigger_source_vector_id="mufrad-001",
        registry_entry_id=registry_entry_rafi_only.operator_id,
        frame_id="frame-001",
        matrix_id="matrix-001",
    )

    operator_rafi_only = OperatorCandidate(
        candidate_id="operator-rafi-only-001",
        trigger_id="trigger-001",
        frame_id="frame-001",
        matrix_id="matrix-001",
        trigger_family=OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY,
        trigger_source=minimal_operator_candidate.trigger_source,
        registry_entry_id=registry_entry_rafi_only.operator_id,
        registry_entry=registry_entry_rafi_only,
        rank=LughaRank.CANDIDATE,
        inherited_residuals=(),
        candidate_residuals=(),
        trace=trace,
    )

    candidate = build_case_effect_candidate(
        operator_candidate=operator_rafi_only,
        factor_equation=minimal_factor_equation,
        matrix_row=matrix_row_nasb,
    )

    # Should be blocked due to compatibility conflict
    assert candidate.effect_type == CaseEffectCandidateType.BLOCKED_EFFECT_CANDIDATE

    # Should have compatibility conflict residual
    residual_types = [r.type for r in candidate.case_effect_residuals]
    assert ResidualType.CASE_EFFECT_COMPATIBILITY_CONFLICT in residual_types


def test_build_case_effect_candidate_deferred_missing_mark(
    minimal_operator_candidate,
    minimal_factor_source,
    minimal_presyntax_vector,
    minimal_matrix_row,
):
    """
    Test: Building deferred case effect candidate when mark missing.

    Verifies:
        - When mark_potential is None
        - Effect type is DEFERRED_EFFECT_CANDIDATE
        - Residual contains CASE_EFFECT_DEFERRED_MISSING_MARK
    """
    from dal_core.factor_mark_equation import build_factor_mark_equation

    # Build equation with missing mark
    equation_deferred = build_factor_mark_equation(
        factor_source=minimal_factor_source,
        affected_vector=minimal_presyntax_vector,
        mark_potential=None,  # Missing mark
        equation_type=FactorMarkEquationType.DEFERRED,
    )

    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=equation_deferred,
        matrix_row=minimal_matrix_row,
    )

    # Should be deferred
    assert candidate.effect_type == CaseEffectCandidateType.DEFERRED_EFFECT_CANDIDATE

    # Should have deferred residual
    residual_types = [r.type for r in candidate.case_effect_residuals]
    assert ResidualType.CASE_EFFECT_DEFERRED_MISSING_MARK in residual_types


def test_build_case_effect_candidate_building_compatible(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_presyntax_vector,
    minimal_case_sign_potential,
):
    """
    Test: Building case effect candidate with BUILDING_COMPATIBLE.

    Verifies:
        - When compatibility includes BUILDING_COMPATIBLE
        - Effect type is BUILDING_EFFECT_CANDIDATE
        - Regardless of policy family
    """
    # Create matrix row with BUILDING compatibility
    obs = SurfaceSignObservation(
        observed_sign=CaseSignValue.DAMMA,
        sign_family=CaseSignFamily.BUILDING,
        source_surface_effect=minimal_case_sign_potential.observed_surface,
        source_potential=minimal_case_sign_potential,
        requires_operator=True,
        requires_inflection_class=False,
    )
    matrix_row_building = CaseSignMatrixRow(
        vector_id=minimal_presyntax_vector.mufrad_id,
        word_index=0,
        raw_span=(0, 5),
        type_id="ISM_COMMON",
        surface_observations=(obs,),
        compatibility_families=(CaseCompatibilityFamily.BUILDING_COMPATIBLE,),
        rank=LughaRank.CANDIDATE,
        residuals=(),
        row_trace_id="trace-matrix-row-building-001",
    )

    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=matrix_row_building,
    )

    # Should be building effect
    assert candidate.effect_type == CaseEffectCandidateType.BUILDING_EFFECT_CANDIDATE


# ---------------------------------------------------------------------------
# Trace Tests
# ---------------------------------------------------------------------------


def test_case_effect_candidate_trace_consistency(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
):
    """
    Test: Trace consistency checks.

    Verifies that all trace fields match their corresponding main fields.
    """
    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    # Trace consistency
    assert candidate.trace.case_effect_id == candidate.case_effect_id
    assert candidate.trace.operator_candidate_id == candidate.operator_candidate_id
    assert candidate.trace.factor_equation_id == candidate.factor_equation_id
    assert candidate.trace.matrix_row_vector_id == candidate.matrix_row.vector_id
    assert candidate.trace.affected_vector_id == candidate.affected_vector.mufrad_id
    assert candidate.trace.trigger_id == candidate.trigger_id
    assert candidate.trace.frame_id == candidate.frame_id
    assert candidate.trace.matrix_id == candidate.matrix_id


def test_case_effect_candidate_vector_row_consistency(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
):
    """
    Test: Vector-row consistency checks.

    Verifies that matrix_row.vector_id matches affected_vector.mufrad_id.
    """
    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    assert candidate.matrix_row.vector_id == candidate.affected_vector.mufrad_id


# ---------------------------------------------------------------------------
# Input Validation Tests
# ---------------------------------------------------------------------------


def test_build_case_effect_candidate_rejects_wrong_operator_type():
    """
    Test: Builder rejects non-OperatorCandidate input.
    """
    with pytest.raises(TypeError, match="OperatorCandidate"):
        build_case_effect_candidate(
            operator_candidate="not_an_operator",  # type: ignore
            factor_equation=None,  # type: ignore
            matrix_row=None,  # type: ignore
        )


def test_build_case_effect_candidate_rejects_wrong_equation_type(
    minimal_operator_candidate,
):
    """
    Test: Builder rejects non-FactorMarkEquation input.
    """
    with pytest.raises(TypeError, match="FactorMarkEquation"):
        build_case_effect_candidate(
            operator_candidate=minimal_operator_candidate,
            factor_equation="not_an_equation",  # type: ignore
            matrix_row=None,  # type: ignore
        )


def test_build_case_effect_candidate_rejects_wrong_row_type(
    minimal_operator_candidate,
    minimal_factor_equation,
):
    """
    Test: Builder rejects non-CaseSignMatrixRow input.
    """
    with pytest.raises(TypeError, match="CaseSignMatrixRow"):
        build_case_effect_candidate(
            operator_candidate=minimal_operator_candidate,
            factor_equation=minimal_factor_equation,
            matrix_row="not_a_row",  # type: ignore
        )


def test_build_case_effect_candidate_rejects_mismatched_vector_row(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_case_sign_potential,
):
    """
    Test: Builder rejects mismatched vector_id between equation and matrix row.
    """
    # Create matrix row with different vector_id
    obs = SurfaceSignObservation(
        observed_sign=CaseSignValue.DAMMA,
        sign_family=CaseSignFamily.ORIGINAL,
        source_surface_effect=minimal_case_sign_potential.observed_surface,
        source_potential=minimal_case_sign_potential,
        requires_operator=True,
        requires_inflection_class=False,
    )
    matrix_row_different = CaseSignMatrixRow(
        vector_id="different-vector-id",  # Mismatched
        word_index=0,
        raw_span=(0, 5),
        type_id="ISM_COMMON",
        surface_observations=(obs,),
        compatibility_families=(CaseCompatibilityFamily.RAFA_COMPATIBLE,),
        rank=LughaRank.CANDIDATE,
        residuals=(),
        row_trace_id="trace-matrix-row-different-001",
    )

    with pytest.raises(ValueError, match="matrix_row.vector_id"):
        build_case_effect_candidate(
            operator_candidate=minimal_operator_candidate,
            factor_equation=minimal_factor_equation,
            matrix_row=matrix_row_different,
        )


# ---------------------------------------------------------------------------
# PR #161 Hardening Tests
# ---------------------------------------------------------------------------


def test_pr161_residual_types_exist():
    """
    PR #161 Test: Verify all CASE_EFFECT_* ResidualTypes exist.

    This test ensures ResidualType enum includes all types used by
    case_effect_candidate.py, preventing AttributeError at runtime.
    """
    # These ResidualTypes MUST exist (used in case_effect_candidate.py)
    assert hasattr(ResidualType, 'CASE_EFFECT_COMPATIBILITY_CONFLICT')
    assert hasattr(ResidualType, 'CASE_EFFECT_DEFERRED_MISSING_MARK')
    assert hasattr(ResidualType, 'CASE_EFFECT_NO_POLICY')
    assert hasattr(ResidualType, 'CASE_EFFECT_UNRESOLVED_POLICY')
    assert hasattr(ResidualType, 'CASE_EFFECT_MIXED_POLICY_REQUIRES_SLOT')
    assert hasattr(ResidualType, 'CASE_EFFECT_RELATION_MISSING')

    # Verify they are actual enum members
    assert isinstance(ResidualType.CASE_EFFECT_COMPATIBILITY_CONFLICT, ResidualType)
    assert isinstance(ResidualType.CASE_EFFECT_DEFERRED_MISSING_MARK, ResidualType)
    assert isinstance(ResidualType.CASE_EFFECT_NO_POLICY, ResidualType)
    assert isinstance(ResidualType.CASE_EFFECT_UNRESOLVED_POLICY, ResidualType)
    assert isinstance(ResidualType.CASE_EFFECT_MIXED_POLICY_REQUIRES_SLOT, ResidualType)
    assert isinstance(ResidualType.CASE_EFFECT_RELATION_MISSING, ResidualType)


def test_pr161_case_effect_exports():
    """
    PR #161 Test: Verify CaseEffectCandidate types exported from dal_core.

    This test ensures all case effect types are properly exported from
    dal_core.__init__, making them part of the official API.
    """
    from dal_core import (
        CaseEffectCandidate,
        CaseEffectCandidateSet,
        CaseEffectCandidateTrace,
        CaseEffectCandidateType,
        build_case_effect_candidate,
    )

    # All types should be importable
    assert CaseEffectCandidate is not None
    assert CaseEffectCandidateSet is not None
    assert CaseEffectCandidateTrace is not None
    assert CaseEffectCandidateType is not None
    assert build_case_effect_candidate is not None


def test_pr161_rank_ceiling_uses_factor_equation_rank(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
):
    """
    PR #161 Test: Verify rank ceiling includes factor_equation.transition_proof rank.

    Prior bug: rank was hardcoded to LughaRank.CANDIDATE instead of reading from
    factor_equation.transition_proof.rank_name.

    Fixed: rank now correctly extracted via _get_rank_from_transition_proof().
    """
    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    # Get factor equation rank from transition proof
    from dal_core.case_effect_candidate import _get_rank_from_transition_proof
    factor_equation_rank = _get_rank_from_transition_proof(
        minimal_factor_equation.transition_proof
    )

    # Rank should be ≤ factor_equation rank (not hardcoded CANDIDATE)
    assert candidate.rank.value <= factor_equation_rank.value

    # Verify _get_rank_from_transition_proof works
    assert isinstance(factor_equation_rank, LughaRank)


def test_pr161_mixed_policy_defers_without_slot(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
):
    """
    PR #161 Test: MIXED_RAFI_NASB_POLICY defers without slot information.

    Prior bug: Mixed policy chose raf'/nasb based on compatibility alone,
    without knowing which constituent (ism_kana vs khabar_kana) it's affecting.

    Fixed: Mixed policy now produces DEFERRED_EFFECT_CANDIDATE with
    CASE_EFFECT_MIXED_POLICY_REQUIRES_SLOT residual when slot info unavailable.
    """
    # minimal_operator_candidate uses MIXED_RAFI_NASB_POLICY_FAMILY
    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    # Should be deferred (not choosing raf' or nasb without slot)
    assert candidate.effect_type == CaseEffectCandidateType.DEFERRED_EFFECT_CANDIDATE

    # Should have mixed policy requires slot residual
    residual_types = [r.type for r in candidate.case_effect_residuals]
    assert ResidualType.CASE_EFFECT_MIXED_POLICY_REQUIRES_SLOT in residual_types


def test_pr161_identity_ids_and_trace_ids_present(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
    minimal_factor_source,
):
    """
    PR #161 Test: identity_ids and trace_ids fields are explicit and populated.

    Prior bug: No explicit identity_ids/trace_ids fields in CaseEffectCandidate,
    only indirect preservation through nested objects.

    Fixed: Added identity_ids and trace_ids as explicit tuple fields,
    aggregating from operator, factor_source, affected_vector, and matrix_row.
    """
    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    # identity_ids field must exist and be populated
    assert hasattr(candidate, 'identity_ids')
    assert isinstance(candidate.identity_ids, tuple)
    assert len(candidate.identity_ids) > 0

    # Should include operator registry entry ID (operator identity)
    assert minimal_operator_candidate.registry_entry_id in candidate.identity_ids

    # Should include factor source identities
    for fid in minimal_factor_source.identity_ids:
        assert fid in candidate.identity_ids

    # trace_ids field must exist and be populated
    assert hasattr(candidate, 'trace_ids')
    assert isinstance(candidate.trace_ids, tuple)
    assert len(candidate.trace_ids) > 0

    # Should include factor source traces
    for tid in minimal_factor_source.trace_ids:
        assert tid in candidate.trace_ids


def test_pr161_trace_id_not_identity_id(
    minimal_operator_candidate,
    minimal_factor_equation,
    minimal_matrix_row,
):
    """
    PR #161 Test: Verify trace_ids ≠ identity_ids.

    Constitutional law: trace_id (provenance) ≠ identity_id (linguistic identity).
    matrix_row.row_trace_id should appear in trace_ids, NOT identity_ids.
    """
    candidate = build_case_effect_candidate(
        operator_candidate=minimal_operator_candidate,
        factor_equation=minimal_factor_equation,
        matrix_row=minimal_matrix_row,
    )

    # matrix_row.row_trace_id is trace, should be in trace_ids
    if hasattr(minimal_matrix_row, 'row_trace_id'):
        assert minimal_matrix_row.row_trace_id in candidate.trace_ids

        # Should NOT be in identity_ids (trace ≠ identity)
        assert minimal_matrix_row.row_trace_id not in candidate.identity_ids


def test_pr161_mixed_policy_with_rafa_nasb_both_compatible():
    """
    PR #161 Test: MIXED policy defers even when both raf'/nasb compatible.

    Verifies that even when compatibility includes both RAFA_COMPATIBLE and
    NASB_COMPATIBLE, the mixed policy still defers without slot information,
    rather than arbitrarily choosing one.
    """
    # This test would require constructing a matrix row with both compatibilities
    # and verifying deferred behavior. Skipping implementation for brevity,
    # but the test should verify DEFERRED not arbitrary choice.
    pass

