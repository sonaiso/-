"""
Tests for CaseSignMatrix (PR #13).

These tests prove the seven required properties from correction 6 plus
the two confirmations from the final review:

A. ALIF (substitute) does NOT imply rafa/nasb without morph-class evidence.
B. NUN_DELETED (substitute) does NOT imply jazm/nasb without an operator.
C. compatibility_families are enum members, not strings.
D. No row contains operator binding, relation, syntax role, or CaseEffect.
E. All matrix residuals are in the central ResidualType taxonomy.
F. Matrix rank never exceeds frame rank.
G. Matrix residuals preserve all frame residuals.

Plus:
H. A visible original sign on a proven `mabni` word yields BUILDING_COMPATIBLE
   only (never mixed with case families).
I. mabni/murab unresolved → UNRESOLVED + residual; not a case judgment.
J. Build entrypoint accepts only SentenceFrameCandidate.
K. Trace ↔ rows alignment is enforced.
L. Forbidden judgment tokens cannot be smuggled into any row string field.
M. Building / case-family mutual exclusion is enforced at construction.
"""

import pytest

from dal_core.case_signs import (
    CaseSignFamily,
    CaseSignPotential,
    CaseSignValue,
)
from dal_core.case_sign_matrix import (
    CaseCompatibilityFamily,
    CaseSignMatrix,
    CaseSignMatrixBuilder,
    CaseSignMatrixRow,
    CaseSignMatrixTrace,
    SurfaceSignObservation,
    build_case_sign_matrix,
)
from dal_core.composition_readiness import CompositionReadiness
from dal_core.evidence import Evidence
from dal_core.morph_features import CandidateStatus, NounInflectionClass
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, ResidualSeverity, ResidualType
from dal_core.sentence_frame import (
    FragmentFrameCandidate,
    FrameType,
    NominalFrameCandidate,
    SentenceFrameCandidate,
    VerbalFrameCandidate,
)
from dal_core.surface_effects import (
    SurfaceEffect,
    SurfaceEffectType,
    SurfaceEffectVisibility,
)
from dal_core.type_ids import NounTypeID, VerbTypeID


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _ev(reason: str = "test") -> Evidence:
    return Evidence(source="test", reason=reason)


def _surface(kind: SurfaceEffectType) -> SurfaceEffect:
    return SurfaceEffect(
        effect_type=kind,
        visibility=SurfaceEffectVisibility.VISIBLE,
        location="final",
        evidence=(_ev(),),
        rank=LughaRank.SAMA,
    )


def _potential(
    sign: CaseSignValue,
    family: CaseSignFamily,
    compatible: tuple[str, ...] = ("rafa_candidate",),
    surface_kind: SurfaceEffectType = SurfaceEffectType.FINAL_DAMMA,
    trace_id: str = "trace-pot",
) -> CaseSignPotential:
    return CaseSignPotential(
        observed_surface=_surface(surface_kind),
        sign_family=family,
        sign_value=sign,
        compatible_case_effects=compatible,
        evidence=_ev(),
        rank=LughaRank.SAMA,
        residuals=(),
        trace_id=trace_id,
    )


def _noun_vector(
    mufrad_id: str = "n1",
    inflection_type: str | None = "munassarif",
    declension_pattern: str = "triptote",
    potentials: tuple[CaseSignPotential, ...] = (),
    residuals: tuple[Residual, ...] = (),
    mabni_status: CandidateStatus = CandidateStatus.RESOLVED_CERTAIN,
    rank: LughaRank = LughaRank.SAMA,
) -> PreSyntaxMufradVector:
    nic = None
    if inflection_type is not None:
        nic = NounInflectionClass(
            inflection_type=inflection_type,
            declension_pattern=declension_pattern,
            evidence=(_ev(),),
            rank=rank,
        )
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 5),
        type_value="ISM",
        type_id=NounTypeID.ISM_COMMON,
        type_rank=rank,
        mabni_murab_status=mabni_status,
        noun_inflection_class=nic,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=potentials,
        morph_rank=rank,
        final_rank=rank,
        residuals=residuals,
        trace_id=f"trace-{mufrad_id}",
        competitors_count=0,
        composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
    )


def _verb_vector(
    mufrad_id: str = "v1",
    potentials: tuple[CaseSignPotential, ...] = (),
    rank: LughaRank = LughaRank.SAMA,
) -> PreSyntaxMufradVector:
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 5),
        type_value="FIIL",
        type_id=VerbTypeID.FIIL_MUDARI,
        type_rank=rank,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
        noun_inflection_class=None,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=potentials,
        morph_rank=rank,
        final_rank=rank,
        residuals=(),
        trace_id=f"trace-{mufrad_id}",
        competitors_count=0,
        composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
    )


def _make_nominal_frame(
    constituents: tuple[PreSyntaxMufradVector, ...],
    frame_residuals: tuple[Residual, ...] = (),
) -> NominalFrameCandidate:
    return NominalFrameCandidate(
        frame_id="frame-1",
        frame_type=FrameType.NOMINAL,
        constituents=constituents,
        frame_rank=min(c.final_rank for c in constituents),
        inherited_residuals=tuple(r for c in constituents for r in c.residuals),
        frame_specific_residuals=frame_residuals,
        trace_id="frame-trace-1",
        lead_noun_index=0,
    )


def _make_fragment_frame(
    constituents: tuple[PreSyntaxMufradVector, ...],
    frame_residuals: tuple[Residual, ...] = (),
) -> FragmentFrameCandidate:
    return FragmentFrameCandidate(
        frame_id="frame-frag",
        frame_type=FrameType.FRAGMENT,
        constituents=constituents,
        frame_rank=min(c.final_rank for c in constituents),
        inherited_residuals=tuple(r for c in constituents for r in c.residuals),
        frame_specific_residuals=frame_residuals,
        trace_id="frame-trace-frag",
        fragment_reason="test",
    )


# ---------------------------------------------------------------------------
# (J) Input validation
# ---------------------------------------------------------------------------


def test_build_rejects_non_frame_input():
    with pytest.raises(TypeError):
        build_case_sign_matrix("not a frame")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        build_case_sign_matrix([_noun_vector()])  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# (C) Compatibility families are enum, never strings
# ---------------------------------------------------------------------------


def test_compatibility_families_are_enum_not_strings():
    pot = _potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL)
    n = _noun_vector(potentials=(pot,))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    row = matrix.rows[0]
    assert all(
        isinstance(f, CaseCompatibilityFamily) for f in row.compatibility_families
    )
    # And the row refuses to be constructed with a string family.
    with pytest.raises(TypeError):
        CaseSignMatrixRow(
            vector_id="x",
            word_index=0,
            raw_span=(0, 1),
            type_id="ISM_COMMON",
            surface_observations=(),
            compatibility_families=("RAFA_COMPATIBLE",),  # type: ignore[arg-type]
            rank=LughaRank.SAMA,
            residuals=(),
            row_trace_id="t",
        )


def test_serialization_uses_strings_only_in_explanation_output():
    pot = _potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL)
    n = _noun_vector(potentials=(pot,))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    expl = matrix.to_explanation()
    assert isinstance(expl, list)
    assert expl[0]["compatibility_families"] == ["rafa_compatible"]


# ---------------------------------------------------------------------------
# (A) ALIF does NOT imply rafa/nasb without morph-class evidence
# ---------------------------------------------------------------------------


def test_alif_without_morph_class_does_not_imply_rafa_or_nasb():
    pot = _potential(
        CaseSignValue.ALIF,
        CaseSignFamily.SUBSTITUTE,
        compatible=("dual_rafa_candidate", "five_nouns_nasb_candidate"),
        surface_kind=SurfaceEffectType.FINAL_ALIF,
    )
    # Even with inflection_type=munassarif (triptote), the current model
    # has NO valued evidence of dual/sound-masc-plural/five-nouns.
    n = _noun_vector(potentials=(pot,))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    row = matrix.rows[0]
    assert row.compatibility_families == (CaseCompatibilityFamily.UNRESOLVED,)
    assert CaseCompatibilityFamily.RAFA_COMPATIBLE not in row.compatibility_families
    assert CaseCompatibilityFamily.NASB_COMPATIBLE not in row.compatibility_families
    residual_types = {r.type for r in row.residuals}
    assert ResidualType.SUBSTITUTE_SIGN_REQUIRES_INFLECTION_CLASS in residual_types
    assert ResidualType.CASE_SIGN_COMPATIBILITY_UNRESOLVED in residual_types


def test_alif_observation_marks_requires_inflection_class():
    pot = _potential(
        CaseSignValue.ALIF,
        CaseSignFamily.SUBSTITUTE,
        surface_kind=SurfaceEffectType.FINAL_ALIF,
    )
    n = _noun_vector(potentials=(pot,))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    obs = matrix.rows[0].surface_observations[0]
    assert obs.observed_sign == CaseSignValue.ALIF
    assert obs.sign_family == CaseSignFamily.SUBSTITUTE
    assert obs.requires_inflection_class is True
    assert obs.requires_operator is True


# ---------------------------------------------------------------------------
# (B) NUN_DELETED does NOT imply jazm/nasb without operator
# ---------------------------------------------------------------------------


def test_nun_deletion_without_operator_does_not_imply_jazm_or_nasb():
    pot = _potential(
        CaseSignValue.NUN_DELETED,
        CaseSignFamily.SUBSTITUTE,
        compatible=("five_verbs_jazm_candidate", "five_verbs_nasb_candidate"),
        surface_kind=SurfaceEffectType.NUN_DELETED,
    )
    v = _verb_vector(potentials=(pot,))
    frame = _make_fragment_frame((v,))
    matrix = build_case_sign_matrix(frame)
    row = matrix.rows[0]
    assert row.compatibility_families == (CaseCompatibilityFamily.UNRESOLVED,)
    assert CaseCompatibilityFamily.JAZM_COMPATIBLE not in row.compatibility_families
    assert CaseCompatibilityFamily.NASB_COMPATIBLE not in row.compatibility_families
    residual_types = {r.type for r in row.residuals}
    assert ResidualType.CASE_SIGN_COMPATIBILITY_UNRESOLVED in residual_types
    assert ResidualType.SUBSTITUTE_SIGN_REQUIRES_INFLECTION_CLASS in residual_types


# ---------------------------------------------------------------------------
# (H, I) Building rule
# ---------------------------------------------------------------------------


def test_mabni_word_with_visible_fatha_yields_building_only():
    pot = _potential(
        CaseSignValue.FATHA,
        CaseSignFamily.ORIGINAL,
        compatible=("building_on_fatha_candidate",),
        surface_kind=SurfaceEffectType.FINAL_FATHA,
    )
    n = _noun_vector(
        inflection_type="mabni",
        declension_pattern="indeclinable",
        potentials=(pot,),
    )
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    row = matrix.rows[0]
    assert row.compatibility_families == (CaseCompatibilityFamily.BUILDING_COMPATIBLE,)
    for forbidden in (
        CaseCompatibilityFamily.RAFA_COMPATIBLE,
        CaseCompatibilityFamily.NASB_COMPATIBLE,
        CaseCompatibilityFamily.JARR_COMPATIBLE,
        CaseCompatibilityFamily.JAZM_COMPATIBLE,
    ):
        assert forbidden not in row.compatibility_families


def test_explicit_building_sign_family_yields_building_only():
    pot = _potential(
        CaseSignValue.DAMMA,
        CaseSignFamily.BUILDING,
        compatible=("building_on_damma_candidate",),
        surface_kind=SurfaceEffectType.FINAL_DAMMA,
    )
    # inflection_type is munassarif but the sign family itself is BUILDING.
    n = _noun_vector(potentials=(pot,))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    assert matrix.rows[0].compatibility_families == (
        CaseCompatibilityFamily.BUILDING_COMPATIBLE,
    )


def test_unresolved_mabni_status_emits_unresolved_and_residuals():
    pot = _potential(
        CaseSignValue.DAMMA,
        CaseSignFamily.ORIGINAL,
        surface_kind=SurfaceEffectType.FINAL_DAMMA,
    )
    n = _noun_vector(
        inflection_type=None,  # no NIC at all
        potentials=(pot,),
        mabni_status=CandidateStatus.UNRESOLVED,  # unresolved status
    )
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    row = matrix.rows[0]
    assert row.compatibility_families == (CaseCompatibilityFamily.UNRESOLVED,)
    residual_types = {r.type for r in row.residuals}
    assert ResidualType.MATRIX_BUILDING_STATUS_UNRESOLVED in residual_types
    assert ResidualType.CASE_SIGN_COMPATIBILITY_UNRESOLVED in residual_types


def test_mabni_status_alone_is_not_proof_of_being_mabni():
    """RESOLVED_CERTAIN on mabni_murab_status without a 'mabni' VALUE in
    noun_inflection_class must NOT trigger BUILDING_COMPATIBLE."""
    pot = _potential(
        CaseSignValue.DAMMA,
        CaseSignFamily.ORIGINAL,
        surface_kind=SurfaceEffectType.FINAL_DAMMA,
    )
    n = _noun_vector(
        inflection_type="munassarif",  # explicitly NOT "mabni"
        potentials=(pot,),
        mabni_status=CandidateStatus.RESOLVED_CERTAIN,
    )
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    row = matrix.rows[0]
    assert (
        CaseCompatibilityFamily.BUILDING_COMPATIBLE
        not in row.compatibility_families
    )
    assert row.compatibility_families == (CaseCompatibilityFamily.RAFA_COMPATIBLE,)


def test_row_rejects_building_mixed_with_case_family():
    with pytest.raises(ValueError):
        CaseSignMatrixRow(
            vector_id="x",
            word_index=0,
            raw_span=(0, 1),
            type_id="ISM_COMMON",
            surface_observations=(),
            compatibility_families=(
                CaseCompatibilityFamily.BUILDING_COMPATIBLE,
                CaseCompatibilityFamily.NASB_COMPATIBLE,
            ),
            rank=LughaRank.SAMA,
            residuals=(),
            row_trace_id="t",
        )


# ---------------------------------------------------------------------------
# Original signs map to canonical families when not mabni
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "sign, expected",
    [
        (CaseSignValue.DAMMA, CaseCompatibilityFamily.RAFA_COMPATIBLE),
        (CaseSignValue.FATHA, CaseCompatibilityFamily.NASB_COMPATIBLE),
        (CaseSignValue.KASRA, CaseCompatibilityFamily.JARR_COMPATIBLE),
        (CaseSignValue.SUKUN, CaseCompatibilityFamily.JAZM_COMPATIBLE),
    ],
)
def test_original_sign_canonical_mapping_on_murab_word(sign, expected):
    pot = _potential(sign, CaseSignFamily.ORIGINAL)
    n = _noun_vector(potentials=(pot,))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    assert matrix.rows[0].compatibility_families == (expected,)


# ---------------------------------------------------------------------------
# (D) No row contains operator binding, relation, syntax role, CaseEffect
# ---------------------------------------------------------------------------


def test_no_row_contains_operator_relation_or_case_effect():
    pot = _potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL)
    n = _noun_vector(potentials=(pot,))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    row = matrix.rows[0]
    row_field_names = {f.name for f in row.__dataclass_fields__.values()}
    forbidden = {
        "case_effect",
        "operator",
        "operator_id",
        "relation",
        "relation_type",
        "syntax_role",
        "faail",
        "mafool",
        "mubtada",
        "khabar",
        "marfoo_by",
        "mansub_by",
        "majroor_by",
        "majzum_by",
        "governed_by",
        "governed_by_operator",
        "meaning",
        "semantic",
        "madlul",
        "murad",
    }
    assert row_field_names.isdisjoint(forbidden)
    matrix_field_names = {f.name for f in matrix.__dataclass_fields__.values()}
    assert matrix_field_names.isdisjoint(forbidden)


def test_row_string_fields_reject_forbidden_judgment_tokens():
    with pytest.raises(ValueError):
        CaseSignMatrixRow(
            vector_id="marfoo_by_faail",  # banned token
            word_index=0,
            raw_span=(0, 1),
            type_id="ISM_COMMON",
            surface_observations=(),
            compatibility_families=(CaseCompatibilityFamily.UNRESOLVED,),
            rank=LughaRank.SAMA,
            residuals=(),
            row_trace_id="t",
        )


def test_observation_requires_operator_must_be_true():
    with pytest.raises(ValueError):
        SurfaceSignObservation(
            observed_sign=CaseSignValue.DAMMA,
            sign_family=CaseSignFamily.ORIGINAL,
            requires_operator=False,
        )


# ---------------------------------------------------------------------------
# (E) All matrix residuals are in central ResidualType taxonomy
# ---------------------------------------------------------------------------


def test_all_matrix_residuals_are_in_central_taxonomy():
    pot_alif = _potential(
        CaseSignValue.ALIF,
        CaseSignFamily.SUBSTITUTE,
        surface_kind=SurfaceEffectType.FINAL_ALIF,
    )
    n = _noun_vector(potentials=(pot_alif,))
    frame_residual = Residual(
        type=ResidualType.LOW_CONFIDENCE,
        severity=ResidualSeverity.WARNING,
        message="frame-level warning",
    )
    frame = _make_fragment_frame((n,), frame_residuals=(frame_residual,))
    matrix = build_case_sign_matrix(frame)
    all_residuals = matrix.get_all_residuals()
    assert all_residuals  # produced some
    for r in all_residuals:
        assert isinstance(r.type, ResidualType)


# ---------------------------------------------------------------------------
# (F) Matrix rank never exceeds frame rank
# ---------------------------------------------------------------------------


def test_matrix_rank_never_exceeds_frame_rank():
    pot = _potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL)
    n_hi = _noun_vector(mufrad_id="hi", potentials=(pot,), rank=LughaRank.SAMA)
    pot2 = _potential(CaseSignValue.FATHA, CaseSignFamily.ORIGINAL)
    n_lo = _noun_vector(mufrad_id="lo", potentials=(pot2,), rank=LughaRank.QIYAS)
    frame = _make_fragment_frame((n_hi, n_lo))
    matrix = build_case_sign_matrix(frame)
    assert matrix.rank.value <= frame.frame_rank.value


# ---------------------------------------------------------------------------
# (G) Matrix residuals preserve frame residuals
# ---------------------------------------------------------------------------


def test_matrix_residuals_preserve_frame_residuals():
    pot = _potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL)
    n_residual = Residual(
        type=ResidualType.MISSING_VOCALIZATION,
        severity=ResidualSeverity.WARNING,
        message="vector-level",
    )
    n = _noun_vector(potentials=(pot,), residuals=(n_residual,))
    f_residual = Residual(
        type=ResidualType.LOW_CONFIDENCE,
        severity=ResidualSeverity.INFO,
        message="frame-level",
    )
    frame = _make_fragment_frame((n,), frame_residuals=(f_residual,))
    matrix = build_case_sign_matrix(frame)
    for r in frame.get_all_residuals():
        assert r in matrix.inherited_residuals


# ---------------------------------------------------------------------------
# (K) Trace alignment
# ---------------------------------------------------------------------------


def test_trace_row_vector_ids_align_with_rows():
    pots = (_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),)
    a = _noun_vector(mufrad_id="a", potentials=pots)
    b = _noun_vector(mufrad_id="b", potentials=pots)
    frame = _make_fragment_frame((a, b))
    matrix = build_case_sign_matrix(frame)
    assert matrix.trace.row_vector_ids == ("a", "b")
    assert matrix.trace.frame_trace_id == frame.trace_id
    assert matrix.trace.frame_id == frame.frame_id


def test_matrix_rejects_misaligned_trace():
    rows = (
        CaseSignMatrixRow(
            vector_id="a",
            word_index=0,
            raw_span=(0, 1),
            type_id="ISM_COMMON",
            surface_observations=(),
            compatibility_families=(CaseCompatibilityFamily.UNRESOLVED,),
            rank=LughaRank.SAMA,
            residuals=(),
            row_trace_id="t",
        ),
    )
    bad_trace = CaseSignMatrixTrace(
        frame_id="f",
        frame_trace_id="ft",
        row_vector_ids=("DIFFERENT",),
    )
    with pytest.raises(ValueError):
        CaseSignMatrix(
            matrix_id="m",
            frame_id="f",
            rows=rows,
            rank=LughaRank.SAMA,
            inherited_residuals=(),
            matrix_residuals=(),
            trace=bad_trace,
        )


def test_matrix_rejects_mismatched_frame_id():
    rows = (
        CaseSignMatrixRow(
            vector_id="a",
            word_index=0,
            raw_span=(0, 1),
            type_id="ISM_COMMON",
            surface_observations=(),
            compatibility_families=(CaseCompatibilityFamily.UNRESOLVED,),
            rank=LughaRank.SAMA,
            residuals=(),
            row_trace_id="t",
        ),
    )
    trace = CaseSignMatrixTrace(
        frame_id="OTHER", frame_trace_id="ft", row_vector_ids=("a",)
    )
    with pytest.raises(ValueError):
        CaseSignMatrix(
            matrix_id="m",
            frame_id="f",  # mismatch
            rows=rows,
            rank=LughaRank.SAMA,
            inherited_residuals=(),
            matrix_residuals=(),
            trace=trace,
        )


# ---------------------------------------------------------------------------
# Row identity must be preserved (each row has vector_id, raw_span, trace)
# ---------------------------------------------------------------------------


def test_row_preserves_vector_identity_fields():
    pot = _potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL)
    n = _noun_vector(potentials=(pot,))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    row = matrix.rows[0]
    assert row.vector_id == n.mufrad_id
    assert row.raw_span == n.raw_span
    assert row.row_trace_id  # non-empty


# ---------------------------------------------------------------------------
# Empty / missing surface sign → UNRESOLVED + residual
# ---------------------------------------------------------------------------


def test_missing_case_sign_potential_yields_unresolved_and_residual():
    n = _noun_vector(potentials=())  # no potentials at all
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    row = matrix.rows[0]
    assert row.compatibility_families == (CaseCompatibilityFamily.UNRESOLVED,)
    residual_types = {r.type for r in row.residuals}
    assert ResidualType.MATRIX_UNRESOLVED_REQUIRED_SIGN in residual_types


# ---------------------------------------------------------------------------
# Estimated sign requires trace
# ---------------------------------------------------------------------------


def test_estimated_sign_without_trace_emits_residual_and_unresolved():
    # CaseSignPotential allows empty trace_id; construct directly to test
    # the matrix's own ESTIMATED_SIGN_REQUIRES_TRACE_IN_MATRIX gate.
    pot = CaseSignPotential(
        observed_surface=_surface(SurfaceEffectType.HIDDEN_FINAL_MARK),
        sign_family=CaseSignFamily.ESTIMATED,
        sign_value=CaseSignValue.ESTIMATED_DAMMA,
        compatible_case_effects=("rafa_candidate",),
        evidence=_ev(),
        rank=LughaRank.SAMA,
        residuals=(),
        trace_id="",
    )
    n = _noun_vector(potentials=(pot,))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    row = matrix.rows[0]
    residual_types = {r.type for r in row.residuals}
    assert ResidualType.ESTIMATED_SIGN_REQUIRES_TRACE_IN_MATRIX in residual_types
    assert CaseCompatibilityFamily.UNRESOLVED in row.compatibility_families


# ---------------------------------------------------------------------------
# Builder class wrapper
# ---------------------------------------------------------------------------


def test_builder_class_produces_same_matrix_shape():
    pot = _potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL)
    n = _noun_vector(potentials=(pot,))
    frame = _make_fragment_frame((n,))
    m1 = build_case_sign_matrix(frame)
    m2 = CaseSignMatrixBuilder().build(frame)
    assert len(m1.rows) == len(m2.rows) == 1
    assert m1.rows[0].compatibility_families == m2.rows[0].compatibility_families


# ---------------------------------------------------------------------------
# Multi-constituent nominal frame end-to-end
# ---------------------------------------------------------------------------


def test_nominal_frame_two_constituents_end_to_end():
    pot_a = _potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL)
    pot_b = _potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL)
    a = _noun_vector(mufrad_id="a", potentials=(pot_a,))
    b = _noun_vector(mufrad_id="b", potentials=(pot_b,))
    frame = _make_nominal_frame((a, b))
    matrix = build_case_sign_matrix(frame)
    assert len(matrix.rows) == 2
    assert all(
        r.compatibility_families == (CaseCompatibilityFamily.RAFA_COMPATIBLE,)
        for r in matrix.rows
    )
    assert matrix.trace.row_vector_ids == ("a", "b")
