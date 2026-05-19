"""
Tests for OperatorTriggerPotential (PR #14).

The trigger layer sits between CaseSignMatrix and the (future)
NahwOperatorRegistry. It emits typed candidate operator FAMILIES; it
must NOT apply operators, produce CaseEffect, assign syntax roles, or
silently resolve competing families.

Test groups (mirror PR #13's test_case_sign_matrix.py style):

A. Strict input typing (frame & matrix; matching frame_id; non-empty).
B. Particle / verbal / nominal / idafa triggers fire correctly.
C. **Competing families are PRESERVED** (no suppression rule, PR #14
   clarification #2 + new invariant #5).
D. Idafa is a construction trigger only — no mudaf / mudaf_ilayh /
   idafa-relation / jarr-judgment.
E. Unresolved / fragment fallbacks.
F. Governance: no forbidden fields, no forbidden tokens, families are
   typed enum, never strings.
G. Residual inheritance: trigger.inherited ⊇ matrix.all ⊇ frame.all.
H. Rank ceiling chain: trigger.rank ≤ matrix.rank ≤ frame.frame_rank.
I. Trace recoverability.
J. Determinism.
K. Matrix-blocker propagation.
L. Helpers (families_for_row, sources_by_family, to_explanation).
"""

import dataclasses

import pytest

from dal_core.case_sign_matrix import (
    CaseCompatibilityFamily,
    CaseSignMatrix,
    build_case_sign_matrix,
)
from dal_core.case_signs import (
    CaseSignFamily,
    CaseSignPotential,
    CaseSignValue,
)
from dal_core.composition_readiness import CompositionReadiness
from dal_core.evidence import Evidence
from dal_core.morph_features import CandidateStatus, NounInflectionClass
from dal_core.operator_trigger import (
    OperatorTriggerFamily,
    OperatorTriggerPotential,
    OperatorTriggerPotentialBuilder,
    OperatorTriggerTrace,
    TriggerSource,
    build_operator_trigger_potential,
)
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, ResidualSeverity, ResidualType
from dal_core.sentence_frame import (
    FragmentFrameCandidate,
    FrameType,
    NominalFrameCandidate,
    ParticleLedFrameCandidate,
    SentenceFrameCandidate,
    UnresolvedFrameCandidate,
    VerbalFrameCandidate,
)
from dal_core.surface_effects import (
    SurfaceEffect,
    SurfaceEffectType,
    SurfaceEffectVisibility,
)
from dal_core.type_ids import NounTypeID, ParticleTypeID, VerbTypeID


# ---------------------------------------------------------------------------
# Fixtures (mirror tests/dal_core/test_case_sign_matrix.py)
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
    surface_kind: SurfaceEffectType = SurfaceEffectType.FINAL_DAMMA,
    trace_id: str = "trace-pot",
) -> CaseSignPotential:
    return CaseSignPotential(
        observed_surface=_surface(surface_kind),
        sign_family=family,
        sign_value=sign,
        compatible_case_effects=("rafa_candidate",),
        evidence=_ev(),
        rank=LughaRank.SAMA,
        residuals=(),
        trace_id=trace_id,
    )


def _noun_vector(
    mufrad_id: str = "n1",
    potentials: tuple[CaseSignPotential, ...] = (),
    rank: LughaRank = LughaRank.SAMA,
    type_id: NounTypeID = NounTypeID.ISM_COMMON,
    residuals: tuple[Residual, ...] = (),
) -> PreSyntaxMufradVector:
    nic = NounInflectionClass(
        inflection_type="munassarif",
        declension_pattern="triptote",
        evidence=(_ev(),),
        rank=rank,
    )
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 5),
        type_value="ISM",
        type_id=type_id,
        type_rank=rank,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
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
    type_id: VerbTypeID = VerbTypeID.FIIL_MUDARI,
    rank: LughaRank = LughaRank.SAMA,
) -> PreSyntaxMufradVector:
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 5),
        type_value="FIIL",
        type_id=type_id,
        type_rank=rank,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
        noun_inflection_class=None,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=(),
        morph_rank=rank,
        final_rank=rank,
        residuals=(),
        trace_id=f"trace-{mufrad_id}",
        competitors_count=0,
        composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
    )


def _particle_vector(
    mufrad_id: str = "p1",
    type_id: ParticleTypeID = ParticleTypeID.HARF_JARR,
    rank: LughaRank = LughaRank.SAMA,
) -> PreSyntaxMufradVector:
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 2),
        type_value="HARF",
        type_id=type_id,
        type_rank=rank,
        mabni_murab_status=CandidateStatus.NOT_APPLICABLE,
        noun_inflection_class=None,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=(),
        morph_rank=rank,
        final_rank=rank,
        residuals=(),
        trace_id=f"trace-{mufrad_id}",
        competitors_count=0,
        composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
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


def _make_nominal_frame(
    constituents: tuple[PreSyntaxMufradVector, ...],
    lead_index: int = 0,
    frame_residuals: tuple[Residual, ...] = (),
) -> NominalFrameCandidate:
    return NominalFrameCandidate(
        frame_id="frame-nom",
        frame_type=FrameType.NOMINAL,
        constituents=constituents,
        frame_rank=min(c.final_rank for c in constituents),
        inherited_residuals=tuple(r for c in constituents for r in c.residuals),
        frame_specific_residuals=frame_residuals,
        trace_id="frame-trace-nom",
        lead_noun_index=lead_index,
    )


def _make_verbal_frame(
    constituents: tuple[PreSyntaxMufradVector, ...],
    verb_index: int = 0,
) -> VerbalFrameCandidate:
    return VerbalFrameCandidate(
        frame_id="frame-vrb",
        frame_type=FrameType.VERBAL,
        constituents=constituents,
        frame_rank=min(c.final_rank for c in constituents),
        inherited_residuals=tuple(r for c in constituents for r in c.residuals),
        frame_specific_residuals=(),
        trace_id="frame-trace-vrb",
        verb_index=verb_index,
    )


def _make_particle_led_frame(
    constituents: tuple[PreSyntaxMufradVector, ...],
    particle_index: int = 0,
) -> ParticleLedFrameCandidate:
    return ParticleLedFrameCandidate(
        frame_id="frame-par",
        frame_type=FrameType.PARTICLE_LED,
        constituents=constituents,
        frame_rank=min(c.final_rank for c in constituents),
        inherited_residuals=tuple(r for c in constituents for r in c.residuals),
        frame_specific_residuals=(),
        trace_id="frame-trace-par",
        particle_index=particle_index,
        particle_operator_potential=None,
    )


def _make_unresolved_frame(
    constituents: tuple[PreSyntaxMufradVector, ...],
) -> UnresolvedFrameCandidate:
    return UnresolvedFrameCandidate(
        frame_id="frame-unr",
        frame_type=FrameType.UNRESOLVED,
        constituents=constituents,
        frame_rank=min(c.final_rank for c in constituents),
        inherited_residuals=tuple(r for c in constituents for r in c.residuals),
        frame_specific_residuals=(),
        trace_id="frame-trace-unr",
        competing_frame_types=(FrameType.NOMINAL, FrameType.VERBAL),
        unresolved_reason="test",
    )


# ---------------------------------------------------------------------------
# (A) Strict input typing
# ---------------------------------------------------------------------------


def test_build_rejects_non_frame_first_argument():
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    with pytest.raises(TypeError):
        build_operator_trigger_potential("not a frame", matrix)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        build_operator_trigger_potential([frame], matrix)  # type: ignore[arg-type]


def test_build_rejects_non_matrix_second_argument():
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_fragment_frame((n,))
    with pytest.raises(TypeError):
        build_operator_trigger_potential(frame, "not a matrix")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        build_operator_trigger_potential(frame, None)  # type: ignore[arg-type]


def test_build_rejects_mismatched_frame_id():
    n1 = _noun_vector(mufrad_id="n1", potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    n2 = _noun_vector(mufrad_id="n2", potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame_a = _make_fragment_frame((n1,))
    frame_b = _make_fragment_frame((n2,))
    # Both fragment frames share the same default frame_id; alter one to differ.
    matrix_a = build_case_sign_matrix(frame_a)
    # Replace frame_b.frame_id to force mismatch with matrix_a.frame_id.
    object.__setattr__(frame_b, "frame_id", "frame-different")
    with pytest.raises(ValueError):
        build_operator_trigger_potential(frame_b, matrix_a)


def test_builder_class_delegates():
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    obj = OperatorTriggerPotentialBuilder().build(frame, matrix)
    assert isinstance(obj, OperatorTriggerPotential)


# ---------------------------------------------------------------------------
# (B) Particle / verbal / nominal / idafa triggers
# ---------------------------------------------------------------------------


def test_harf_jarr_fires_jarr_family():
    p = _particle_vector(mufrad_id="p_jarr", type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        mufrad_id="n_after",
        potentials=(
            _potential(
                CaseSignValue.KASRA,
                CaseSignFamily.ORIGINAL,
                surface_kind=SurfaceEffectType.FINAL_KASRA,
            ),
        ),
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY in trig.triggered_families
    jarr_sources = [
        s for s in trig.sources
        if s.family == OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY
    ]
    assert len(jarr_sources) == 1
    assert jarr_sources[0].frame_index == 0
    assert jarr_sources[0].vector_id == "p_jarr"
    assert jarr_sources[0].matrix_row_index == 0
    assert jarr_sources[0].triggering_type_id == "HARF_JARR"


@pytest.mark.parametrize(
    "particle_type, expected_family",
    [
        (ParticleTypeID.HARF_NASB, OperatorTriggerFamily.POSSIBLE_NASB_OPERATOR_FAMILY),
        (ParticleTypeID.HARF_JAZM, OperatorTriggerFamily.POSSIBLE_JAZM_OPERATOR_FAMILY),
        (ParticleTypeID.HARF_NIDA, OperatorTriggerFamily.POSSIBLE_NIDA_FAMILY),
        (ParticleTypeID.HARF_ATF, OperatorTriggerFamily.POSSIBLE_ATF_FAMILY),
        (ParticleTypeID.HARF_NAFI, OperatorTriggerFamily.POSSIBLE_NAFI_FAMILY),
        (ParticleTypeID.HARF_ISTIFHAM, OperatorTriggerFamily.POSSIBLE_ISTIFHAM_FAMILY),
        (ParticleTypeID.HARF_NASIKH_LA_NAFI_LILJINS, OperatorTriggerFamily.POSSIBLE_NASIKH_LA_LILJINS_FAMILY),
    ],
)
def test_particle_family_mapping(particle_type, expected_family):
    p = _particle_vector(mufrad_id="p", type_id=particle_type)
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert expected_family in trig.triggered_families


def test_unresolved_particle_emits_residual_no_family():
    p = _particle_vector(mufrad_id="p_unr", type_id=ParticleTypeID.HARF_UNRESOLVED)
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY not in trig.triggered_families
    types = {r.type for r in trig.get_all_residuals()}
    assert ResidualType.TRIGGER_PARTICLE_TYPE_UNRESOLVED in types


def test_verbal_frame_fires_verbal_governance_once():
    v = _verb_vector(mufrad_id="v_mudari")
    n1 = _noun_vector(mufrad_id="n_subj", potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    n2 = _noun_vector(mufrad_id="n_obj", potentials=(_potential(CaseSignValue.FATHA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_FATHA),))
    frame = _make_verbal_frame((v, n1, n2), verb_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    verbal_sources = [
        s for s in trig.sources
        if s.family == OperatorTriggerFamily.POSSIBLE_VERBAL_GOVERNANCE_FAMILY
    ]
    assert len(verbal_sources) == 1
    assert verbal_sources[0].frame_index == 0
    assert verbal_sources[0].triggering_type_id == "FIIL_MUDARI"


def test_nominal_frame_fires_ibtidaa_once():
    n1 = _noun_vector(mufrad_id="n_lead", potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    n2 = _noun_vector(mufrad_id="n_pred", potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_nominal_frame((n1, n2), lead_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    ibtidaa = [
        s for s in trig.sources
        if s.family == OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY
    ]
    assert len(ibtidaa) == 1
    assert ibtidaa[0].frame_index == 0
    assert ibtidaa[0].vector_id == "n_lead"


def test_idafa_fires_on_adjacent_ism_ism_with_jarr_compat():
    n_first = _noun_vector(
        mufrad_id="n_first",
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),),
    )
    n_second = _noun_vector(
        mufrad_id="n_second",
        potentials=(
            _potential(
                CaseSignValue.KASRA,
                CaseSignFamily.ORIGINAL,
                surface_kind=SurfaceEffectType.FINAL_KASRA,
            ),
        ),
    )
    frame = _make_fragment_frame((n_first, n_second))
    matrix = build_case_sign_matrix(frame)
    # Sanity: row 1 has JARR_COMPATIBLE.
    assert CaseCompatibilityFamily.JARR_COMPATIBLE in matrix.rows[1].compatibility_families
    trig = build_operator_trigger_potential(frame, matrix)
    idafa = [s for s in trig.sources if s.family == OperatorTriggerFamily.POSSIBLE_IDAFA_FAMILY]
    assert len(idafa) == 1
    assert idafa[0].frame_index == 1
    assert idafa[0].vector_id == "n_second"


def test_idafa_does_not_fire_when_second_is_not_jarr_compatible():
    n_first = _noun_vector(
        mufrad_id="n_first",
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),),
    )
    n_second = _noun_vector(
        mufrad_id="n_second",
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),),
    )
    frame = _make_fragment_frame((n_first, n_second))
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert OperatorTriggerFamily.POSSIBLE_IDAFA_FAMILY not in trig.triggered_families


# ---------------------------------------------------------------------------
# (C) **Competing families are preserved** (PR #14 clarification #2 + invariant)
# ---------------------------------------------------------------------------


def test_nasikh_inna_and_ibtidaa_both_preserved():
    """
    إنَّ الكتابَ ... — both POSSIBLE_NASIKH_INNA_FAMILY and
    POSSIBLE_IBTIDAA_FAMILY are emitted. The trigger layer does NOT
    suppress one in favor of the other; resolution belongs to a later
    ParseCompetition / OperatorCandidate stage.

    Constructing a real NominalFrameCandidate validates that the lead is
    an ISM. To create the test scenario we use a fragment frame containing
    [HARF_NASIKH_INNA, ISM] AND additionally invoke the nominal frame
    fixture to ensure the symmetric path is also tested.
    """
    p_inna = _particle_vector(mufrad_id="p_inna", type_id=ParticleTypeID.HARF_NASIKH_INNA)
    n_lead = _noun_vector(
        mufrad_id="n_lead",
        potentials=(
            _potential(
                CaseSignValue.FATHA,
                CaseSignFamily.ORIGINAL,
                surface_kind=SurfaceEffectType.FINAL_FATHA,
            ),
        ),
    )
    # Nominal frame: lead noun at index 1. Particle precedes.
    frame = _make_nominal_frame((p_inna, n_lead), lead_index=1)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)

    # BOTH families must be present.
    assert OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY in trig.triggered_families
    assert OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY in trig.triggered_families

    # An info residual must announce that competition was preserved.
    info_types = {r.type for r in trig.trigger_residuals if r.severity == ResidualSeverity.INFO}
    assert ResidualType.TRIGGER_COMPETING_FAMILIES_PRESERVED in info_types


def test_competition_residual_lists_competing_family_names():
    p_inna = _particle_vector(mufrad_id="p_inna", type_id=ParticleTypeID.HARF_NASIKH_INNA)
    n_lead = _noun_vector(
        mufrad_id="n_lead",
        potentials=(
            _potential(
                CaseSignValue.FATHA,
                CaseSignFamily.ORIGINAL,
                surface_kind=SurfaceEffectType.FINAL_FATHA,
            ),
        ),
    )
    frame = _make_nominal_frame((p_inna, n_lead), lead_index=1)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    comp_res = [
        r for r in trig.trigger_residuals
        if r.type == ResidualType.TRIGGER_COMPETING_FAMILIES_PRESERVED
    ]
    assert len(comp_res) == 1
    assert "possible_nasikh_inna_family" in comp_res[0].message
    assert "possible_ibtidaa_family" in comp_res[0].message


def test_no_competition_residual_when_only_one_family():
    # Pure fragment with one noun — only UNRESOLVED_TRIGGER (or one non-
    # unresolved family) — must NOT emit the competition info residual.
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    types = {r.type for r in trig.trigger_residuals}
    assert ResidualType.TRIGGER_COMPETING_FAMILIES_PRESERVED not in types


def test_no_silent_suppression_invariant_at_construction():
    """
    Direct construction of an OperatorTriggerPotential that drops a
    family attested by a source must raise — enforcing the no-suppression
    invariant structurally.
    """
    src = TriggerSource(
        family=OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY,
        frame_index=0,
        vector_id="v",
        matrix_row_index=0,
        triggering_type_id="ISM_COMMON",
        compatibility_evidence=(),
        source_trace_id="t",
    )
    trace = OperatorTriggerTrace(
        frame_id="f",
        frame_trace_id="ft",
        matrix_id="m",
        matrix_trace_id="mt",
    )
    with pytest.raises(ValueError):
        OperatorTriggerPotential(
            trigger_id="tr",
            frame_id="f",
            matrix_id="m",
            # Source attests IBTIDAA but families list omits it → must fail.
            triggered_families=(OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,),
            sources=(src,),
            rank=LughaRank.SAMA,
            inherited_residuals=(),
            trigger_residuals=(),
            trace=trace,
        )


def test_orphan_family_without_source_rejected():
    trace = OperatorTriggerTrace(
        frame_id="f",
        frame_trace_id="ft",
        matrix_id="m",
        matrix_trace_id="mt",
    )
    with pytest.raises(ValueError):
        OperatorTriggerPotential(
            trigger_id="tr",
            frame_id="f",
            matrix_id="m",
            triggered_families=(OperatorTriggerFamily.POSSIBLE_NIDA_FAMILY,),
            sources=(),  # no source supports the family
            rank=LughaRank.SAMA,
            inherited_residuals=(),
            trigger_residuals=(),
            trace=trace,
        )


# ---------------------------------------------------------------------------
# (D) Idafa is construction-trigger only
# ---------------------------------------------------------------------------


def test_idafa_trigger_does_not_assert_mudaf_or_relation():
    n_first = _noun_vector(
        mufrad_id="n_first",
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),),
    )
    n_second = _noun_vector(
        mufrad_id="n_second",
        potentials=(
            _potential(
                CaseSignValue.KASRA,
                CaseSignFamily.ORIGINAL,
                surface_kind=SurfaceEffectType.FINAL_KASRA,
            ),
        ),
    )
    frame = _make_fragment_frame((n_first, n_second))
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    expl = trig.to_explanation()
    # No mudaf / mudaf_ilayh / relation / case effect keys or values.
    forbidden = ("mudaf", "mudaf_ilayh", "relation", "case_effect", "marfoo", "mansub", "majroor")
    blob = repr(expl).lower()
    for tok in forbidden:
        assert tok not in blob, f"Forbidden token {tok!r} in explanation output"


# ---------------------------------------------------------------------------
# (E) Unresolved / fragment fallbacks
# ---------------------------------------------------------------------------


def test_unresolved_frame_emits_unresolved_trigger_and_blocker():
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_unresolved_frame((n,))
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert OperatorTriggerFamily.UNRESOLVED_TRIGGER in trig.triggered_families
    types = {r.type for r in trig.trigger_residuals}
    assert ResidualType.TRIGGER_UNRESOLVED_FRAME in types
    assert any(r.is_blocker() for r in trig.trigger_residuals)


def test_fragment_with_no_rule_firing_emits_unresolved_warning():
    # Single particle with type_id that does not map to a trigger family.
    p = _particle_vector(mufrad_id="p", type_id=ParticleTypeID.HARF_IBTIDA)
    frame = _make_fragment_frame((p,))
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert OperatorTriggerFamily.UNRESOLVED_TRIGGER in trig.triggered_families
    types = {r.type for r in trig.trigger_residuals}
    assert ResidualType.TRIGGER_FRAGMENT_NO_FAMILY in types
    # Warning, not blocker, per the design.
    assert not any(
        r.type == ResidualType.TRIGGER_FRAGMENT_NO_FAMILY and r.is_blocker()
        for r in trig.trigger_residuals
    )


# ---------------------------------------------------------------------------
# (F) Governance: typed families, no forbidden tokens, no forbidden fields
# ---------------------------------------------------------------------------


def test_triggered_families_are_enum_not_strings():
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),))
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert all(isinstance(f, OperatorTriggerFamily) for f in trig.triggered_families)


def test_construction_rejects_string_family_in_triggered_families():
    src = TriggerSource(
        family=OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY,
        frame_index=0,
        vector_id="v",
        matrix_row_index=0,
        triggering_type_id="ISM_COMMON",
        compatibility_evidence=(),
        source_trace_id="t",
    )
    trace = OperatorTriggerTrace(
        frame_id="f", frame_trace_id="ft", matrix_id="m", matrix_trace_id="mt"
    )
    with pytest.raises(TypeError):
        OperatorTriggerPotential(
            trigger_id="tr",
            frame_id="f",
            matrix_id="m",
            triggered_families=("possible_ibtidaa_family",),  # type: ignore[arg-type]
            sources=(src,),
            rank=LughaRank.SAMA,
            inherited_residuals=(),
            trigger_residuals=(),
            trace=trace,
        )


def test_construction_rejects_string_family_in_source():
    with pytest.raises(TypeError):
        TriggerSource(
            family="possible_ibtidaa_family",  # type: ignore[arg-type]
            frame_index=0,
            vector_id="v",
            matrix_row_index=0,
            triggering_type_id="ISM_COMMON",
            compatibility_evidence=(),
            source_trace_id="t",
        )


@pytest.mark.parametrize(
    "tok",
    [
        "marfoo", "mansub", "majroor", "majzum",
        "governed_by", "operator_id", "operator_binding",
        "relation_type", "faail", "mafool", "mubtada",
        "khabar", "mudaf", "mudaf_ilayh",
        "case_effect", "syntax_role",
        "marfoo_by", "mansub_by", "majroor_by", "majzum_by",
        "meaning", "madlul", "murad", "haqiqa", "majaz",
    ],
)
def test_forbidden_tokens_cannot_be_smuggled_into_trigger_id(tok):
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    # Construct a valid trigger then try to mutate trigger_id with a
    # forbidden token via re-construction.
    base = build_operator_trigger_potential(frame, matrix)
    with pytest.raises(ValueError):
        OperatorTriggerPotential(
            trigger_id=f"tr-{tok}-leak",
            frame_id=base.frame_id,
            matrix_id=base.matrix_id,
            triggered_families=base.triggered_families,
            sources=base.sources,
            rank=base.rank,
            inherited_residuals=base.inherited_residuals,
            trigger_residuals=base.trigger_residuals,
            trace=base.trace,
        )


def test_no_forbidden_field_names_in_dataclasses():
    forbidden = {
        "operator", "operator_id", "operator_binding",
        "relation", "relation_type", "case_effect", "syntax_role",
        "faail", "mafool", "mubtada", "khabar", "mudaf", "mudaf_ilayh",
        "marfoo_by", "mansub_by", "majroor_by", "majzum_by",
        "governed_by", "governed_by_operator",
        "meaning", "semantic", "madlul", "murad", "haqiqa", "majaz",
    }
    for cls in (OperatorTriggerPotential, TriggerSource, OperatorTriggerTrace):
        names = {f.name for f in dataclasses.fields(cls)}
        assert not (names & forbidden), f"{cls.__name__} has forbidden fields: {names & forbidden}"


def test_to_explanation_strings_appear_only_here():
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),))
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    expl = trig.to_explanation()
    assert isinstance(expl, list)
    assert expl[0]["family"] == "possible_jarr_operator_family"
    # No grammatical role keys.
    for entry in expl:
        for forbidden_key in (
            "operator", "operator_id", "relation", "case_effect",
            "syntax_role", "faail", "mafool", "mubtada", "khabar",
        ):
            assert forbidden_key not in entry


# ---------------------------------------------------------------------------
# (G) Residual inheritance
# ---------------------------------------------------------------------------


def test_inherited_residuals_superset_of_matrix_residuals():
    # Frame with a frame-specific residual; matrix inherits it; trigger
    # must inherit it as well.
    frame_resid = Residual(
        type=ResidualType.COMPOSITION_BLOCKER,
        severity=ResidualSeverity.WARNING,
        message="test-frame-resid",
    )
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_fragment_frame((n,), frame_residuals=(frame_resid,))
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    matrix_all = matrix.get_all_residuals()
    # Set inclusion on tuple membership (identity of type/severity/message).
    for r in matrix_all:
        assert r in trig.inherited_residuals
    assert frame_resid in trig.inherited_residuals


# ---------------------------------------------------------------------------
# (H) Rank ceiling chain
# ---------------------------------------------------------------------------


def test_rank_ceiling_chain():
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),),
        rank=LughaRank.SAMA,
    )
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert trig.rank.value <= matrix.rank.value <= frame.frame_rank.value


# ---------------------------------------------------------------------------
# (I) Trace recoverability
# ---------------------------------------------------------------------------


def test_trace_links_frame_and_matrix():
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert trig.trace.frame_id == frame.frame_id
    assert trig.trace.frame_trace_id == frame.trace_id
    assert trig.trace.matrix_id == matrix.matrix_id
    assert trig.trace.matrix_trace_id == matrix.trace.frame_trace_id


def test_each_source_matrix_row_index_matches_vector_id():
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR, mufrad_id="p_jarr")
    n = _noun_vector(
        mufrad_id="n_after",
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),),
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    for src in trig.sources:
        if src.matrix_row_index is not None:
            assert matrix.rows[src.matrix_row_index].vector_id == src.vector_id


# ---------------------------------------------------------------------------
# (J) Determinism
# ---------------------------------------------------------------------------


def test_two_builds_produce_equal_families_and_sources():
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR, mufrad_id="p")
    n = _noun_vector(potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),))
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    a = build_operator_trigger_potential(frame, matrix)
    b = build_operator_trigger_potential(frame, matrix)
    # trigger_id may differ (uuid) but structural content must match.
    assert a.triggered_families == b.triggered_families
    assert tuple(
        (s.family, s.frame_index, s.vector_id, s.matrix_row_index, s.triggering_type_id)
        for s in a.sources
    ) == tuple(
        (s.family, s.frame_index, s.vector_id, s.matrix_row_index, s.triggering_type_id)
        for s in b.sources
    )


# ---------------------------------------------------------------------------
# (K) Matrix-blocker propagation
# ---------------------------------------------------------------------------


def test_matrix_blocker_propagates_as_trigger_warning_per_family():
    # An ALIF substitute sign with no morph evidence forces matrix blockers.
    n = _noun_vector(
        potentials=(
            _potential(
                CaseSignValue.ALIF,
                CaseSignFamily.SUBSTITUTE,
                surface_kind=SurfaceEffectType.FINAL_ALIF,
            ),
        ),
    )
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    assert matrix.has_blocking_residuals()
    trig = build_operator_trigger_potential(frame, matrix)
    # Trigger still emitted (even if only UNRESOLVED_TRIGGER), but a
    # TRIGGER_BLOCKED_BY_MATRIX_RESIDUAL warning is recorded per family.
    types = {r.type for r in trig.trigger_residuals}
    assert ResidualType.TRIGGER_BLOCKED_BY_MATRIX_RESIDUAL in types
    # Matrix's original blocker is preserved in inherited_residuals.
    inherited_types = {r.type for r in trig.inherited_residuals}
    assert ResidualType.SUBSTITUTE_SIGN_REQUIRES_INFLECTION_CLASS in inherited_types


# ---------------------------------------------------------------------------
# (L) Helpers
# ---------------------------------------------------------------------------


def test_families_for_row_returns_per_row_families():
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR, mufrad_id="p")
    n = _noun_vector(potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),))
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY in trig.families_for_row(0)


def test_sources_by_family_groups_all_sources():
    p_inna = _particle_vector(mufrad_id="p_inna", type_id=ParticleTypeID.HARF_NASIKH_INNA)
    n_lead = _noun_vector(
        mufrad_id="n_lead",
        potentials=(_potential(CaseSignValue.FATHA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_FATHA),),
    )
    frame = _make_nominal_frame((p_inna, n_lead), lead_index=1)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    grouped = trig.sources_by_family()
    assert OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY in grouped
    assert OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY in grouped
    # Each grouped value is a tuple
    for fam, srcs in grouped.items():
        assert isinstance(srcs, tuple)
        assert all(s.family == fam for s in srcs)


def test_get_all_residuals_merges_inherited_and_trigger():
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_fragment_frame((n,))
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert trig.get_all_residuals() == trig.inherited_residuals + trig.trigger_residuals


def test_has_blocking_residuals_true_on_unresolved_frame():
    n = _noun_vector(potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),))
    frame = _make_unresolved_frame((n,))
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    assert trig.has_blocking_residuals() is True
