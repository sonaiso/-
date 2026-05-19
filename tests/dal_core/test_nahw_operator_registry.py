"""
Tests for NahwOperatorRegistry (PR #15 + PR #16a).

The registry is post-trigger, pre-operator: it returns typed
`NahwOperatorEntry` candidates for each `OperatorTriggerFamily` in an
`OperatorTriggerPotential`. It NEVER applies an operator, resolves
competing entries, produces a relation, or produces a case effect.

Test groups (mirror PR #14 style):

A. Read-only API surface (no apply/bind/resolve/choose).
B. Typed-only fields (Enums everywhere; strings forbidden).
C. Forbidden field-name / token guards.
D. Seed coverage (every non-UNRESOLVED family has ≥ 1 entry).
E. IDAFA is construction-trigger only — NO case-effect policy.
F. UNRESOLVED_TRIGGER returns empty tuple + warning residual.
G. Competing entries preserved (≥ 2 entries → INFO residual).
H. Competing families preserved across trigger lookup (NASIKH_INNA +
   IBTIDAA both yield results, no suppression).
I. Residual inheritance: lookup.inherited ⊇ trigger.get_all_residuals().
J. Rank ceiling: every lookup.rank ≤ trigger.rank.
K. frame_id / matrix_id / trigger_id propagation.
L. Cross-layer non-regression — uses real frame/matrix/trigger pipeline.
M. Immutability hardening (PR #16a) — internal indexes are MappingProxyType,
   reassignment/deletion prevented, mutation attempts fail cleanly.
"""

from __future__ import annotations

from types import MappingProxyType

import pytest

from dal_core.case_sign_matrix import build_case_sign_matrix
from dal_core.case_signs import (
    CaseSignFamily,
    CaseSignPotential,
    CaseSignValue,
)
from dal_core.composition_readiness import CompositionReadiness
from dal_core.evidence import Evidence
from dal_core.morph_features import CandidateStatus, NounInflectionClass
from dal_core.nahw_operator_registry import (
    ActivationCondition,
    BlockingCondition,
    CaseEffectPolicyFamily,
    Citation,
    ExpectedRelationFamily,
    NahwOperatorEntry,
    NahwOperatorRegistry,
    NahwSchool,
    OperatorInputSignature,
    OperatorRegistryLookupResult,
    OperatorSource,
    build_default_nahw_operator_registry,
)
from dal_core.nahw_operator_registry_seed import build_seed_entries
from dal_core.operator_trigger import (
    OperatorTriggerFamily,
    build_operator_trigger_potential,
)
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, ResidualSeverity, ResidualType
from dal_core.sentence_frame import (
    FrameType,
    NominalFrameCandidate,
    ParticleLedFrameCandidate,
)
from dal_core.surface_effects import (
    SurfaceEffect,
    SurfaceEffectType,
    SurfaceEffectVisibility,
)
from dal_core.type_ids import NounTypeID, ParticleTypeID


# ---------------------------------------------------------------------------
# Fixtures (mirror tests/dal_core/test_operator_trigger.py shape)
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


def _make_nominal_frame(
    constituents: tuple[PreSyntaxMufradVector, ...],
    lead_index: int = 0,
) -> NominalFrameCandidate:
    return NominalFrameCandidate(
        frame_id="frame-nom",
        frame_type=FrameType.NOMINAL,
        constituents=constituents,
        frame_rank=min(c.final_rank for c in constituents),
        inherited_residuals=tuple(r for c in constituents for r in c.residuals),
        frame_specific_residuals=(),
        trace_id="frame-trace-nom",
        lead_noun_index=lead_index,
    )


def _make_inna_plus_nominal_frame() -> NominalFrameCandidate:
    """إنّ الكتابَ — preserves competing NASIKH_INNA + IBTIDAA families."""
    p = _particle_vector(mufrad_id="p_inna", type_id=ParticleTypeID.HARF_NASIKH_INNA)
    n = _noun_vector(
        mufrad_id="n_kitab",
        potentials=(
            _potential(
                CaseSignValue.FATHA,
                CaseSignFamily.ORIGINAL,
                surface_kind=SurfaceEffectType.FINAL_FATHA,
            ),
        ),
    )
    return NominalFrameCandidate(
        frame_id="frame-inna",
        frame_type=FrameType.NOMINAL,
        constituents=(p, n),
        frame_rank=min(c.final_rank for c in (p, n)),
        inherited_residuals=(),
        frame_specific_residuals=(),
        trace_id="frame-trace-inna",
        lead_noun_index=1,
    )


# ===========================================================================
# (A) Read-only API surface
# ===========================================================================


def test_registry_has_no_apply_or_bind_or_resolve_methods():
    reg = build_default_nahw_operator_registry()
    forbidden = {"apply", "bind", "resolve", "choose", "rank_entries", "select"}
    public = {n for n in dir(reg) if not n.startswith("_")}
    assert public.isdisjoint(forbidden), (
        f"Registry must be read-only; found forbidden methods: "
        f"{public & forbidden}"
    )


def test_entry_has_no_apply_or_bind_methods():
    reg = build_default_nahw_operator_registry()
    entry = reg.entry_by_id("INNA")
    assert entry is not None
    forbidden = {"apply", "bind", "resolve", "execute"}
    public = {n for n in dir(entry) if not n.startswith("_")}
    assert public.isdisjoint(forbidden)


def test_registry_constructor_rejects_non_tuple():
    with pytest.raises(TypeError):
        NahwOperatorRegistry([])  # type: ignore[arg-type]


def test_registry_constructor_rejects_non_entry():
    with pytest.raises(TypeError):
        NahwOperatorRegistry(("not an entry",))  # type: ignore[arg-type]


def test_registry_constructor_rejects_duplicate_operator_id():
    seed = build_seed_entries()
    with pytest.raises(ValueError):
        NahwOperatorRegistry(seed + (seed[0],))


def test_entries_for_family_requires_enum():
    reg = build_default_nahw_operator_registry()
    with pytest.raises(TypeError):
        reg.entries_for_family("possible_jarr_operator_family")  # type: ignore[arg-type]


def test_entries_for_trigger_requires_trigger_potential():
    reg = build_default_nahw_operator_registry()
    with pytest.raises(TypeError):
        reg.entries_for_trigger("not a trigger")  # type: ignore[arg-type]


# ===========================================================================
# (B) Typed-only fields
# ===========================================================================


def _base_entry_kwargs() -> dict:
    return dict(
        operator_id="X",
        display_name_ar="عامل",
        source=OperatorSource.KALAAM_ARAB,
        school=NahwSchool.SHARED,
        rank=LughaRank.TAWATUR,
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        input_signature=OperatorInputSignature(expected_arity=1),
        activation_conditions=(),
        blocking_conditions=(),
        expected_relation_families=(ExpectedRelationFamily.TAQYID_LIKE,),
        case_effect_policy_families=(CaseEffectPolicyFamily.JARR_POLICY_FAMILY,),
        citations=(Citation(source=OperatorSource.KALAAM_ARAB, reference="ref"),),
        entry_residuals=(),
        entry_trace_id="trace-x",
    )


def test_entry_rejects_string_in_expected_relation_families():
    kwargs = _base_entry_kwargs()
    kwargs["expected_relation_families"] = ("isn_like",)  # type: ignore[assignment]
    with pytest.raises(TypeError):
        NahwOperatorEntry(**kwargs)


def test_entry_rejects_string_in_case_effect_policy_families():
    kwargs = _base_entry_kwargs()
    kwargs["case_effect_policy_families"] = ("jarr_policy_family",)  # type: ignore[assignment]
    with pytest.raises(TypeError):
        NahwOperatorEntry(**kwargs)


def test_entry_rejects_string_family():
    kwargs = _base_entry_kwargs()
    kwargs["family"] = "possible_jarr_operator_family"  # type: ignore[assignment]
    with pytest.raises(TypeError):
        NahwOperatorEntry(**kwargs)


def test_entry_rejects_non_enum_activation_condition():
    kwargs = _base_entry_kwargs()
    kwargs["activation_conditions"] = ("immediately_precedes_ism",)  # type: ignore[assignment]
    with pytest.raises(TypeError):
        NahwOperatorEntry(**kwargs)


def test_entry_rejects_non_enum_blocking_condition():
    kwargs = _base_entry_kwargs()
    kwargs["blocking_conditions"] = ("blocked_if_follows_verb",)  # type: ignore[assignment]
    with pytest.raises(TypeError):
        NahwOperatorEntry(**kwargs)


def test_entry_rejects_non_citation():
    kwargs = _base_entry_kwargs()
    kwargs["citations"] = ("Q 2:1",)  # type: ignore[assignment]
    with pytest.raises(TypeError):
        NahwOperatorEntry(**kwargs)


def test_entry_rejects_missing_operator_id():
    kwargs = _base_entry_kwargs()
    kwargs["operator_id"] = ""
    with pytest.raises(ValueError):
        NahwOperatorEntry(**kwargs)


def test_input_signature_rejects_negative_arity():
    with pytest.raises(ValueError):
        OperatorInputSignature(expected_arity=-1)


def test_citation_requires_typed_source():
    with pytest.raises(TypeError):
        Citation(source="quran", reference="Q 2:1")  # type: ignore[arg-type]


# ===========================================================================
# (C) Forbidden field-name / token guards
# ===========================================================================


def test_entry_field_names_contain_no_forbidden_tokens():
    field_names = {
        f.name for f in NahwOperatorEntry.__dataclass_fields__.values()
    }
    forbidden = {
        "meaning",
        "murad",
        "madlul",
        "haqiqa",
        "majaz",
        "relation_type",
        "operator_id_resolved",
        "case_effect",
        "syntax_role",
        "faail",
        "mafool",
        "mubtada",
        "khabar",
        "mudaf",
        "mudaf_ilayh",
        "marfoo_by",
        "mansub_by",
        "majroor_by",
        "majzum_by",
        "governed_by",
        "operator_binding",
    }
    assert field_names.isdisjoint(forbidden), (
        f"Forbidden fields present on NahwOperatorEntry: "
        f"{field_names & forbidden}"
    )


def test_lookup_result_field_names_contain_no_forbidden_tokens():
    field_names = {
        f.name for f in OperatorRegistryLookupResult.__dataclass_fields__.values()
    }
    forbidden = {
        "meaning",
        "case_effect",
        "syntax_role",
        "relation_type",
        "faail",
        "mafool",
        "mubtada",
        "khabar",
    }
    assert field_names.isdisjoint(forbidden)


# ===========================================================================
# (D) Seed coverage
# ===========================================================================


def test_seed_covers_every_non_unresolved_family():
    reg = build_default_nahw_operator_registry()
    families_seen = reg.all_families()
    required = {
        f for f in OperatorTriggerFamily
        if f is not OperatorTriggerFamily.UNRESOLVED_TRIGGER
    }
    missing = required - families_seen
    assert not missing, f"Seed is missing entries for families: {missing}"


def test_seed_has_no_entry_for_unresolved_trigger():
    reg = build_default_nahw_operator_registry()
    assert reg.entries_for_family(OperatorTriggerFamily.UNRESOLVED_TRIGGER) == ()


def test_seed_inna_family_has_six_competing_entries():
    reg = build_default_nahw_operator_registry()
    es = reg.entries_for_family(OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY)
    op_ids = {e.operator_id for e in es}
    assert {"INNA", "ANNA", "KAANNA", "LAKINNA", "LAYTA", "LAALLA"} <= op_ids


def test_seed_entries_all_typed():
    for e in build_seed_entries():
        assert isinstance(e.family, OperatorTriggerFamily)
        assert isinstance(e.source, OperatorSource)
        assert isinstance(e.school, NahwSchool)
        assert isinstance(e.rank, LughaRank)
        for rel in e.expected_relation_families:
            assert isinstance(rel, ExpectedRelationFamily)
        for pol in e.case_effect_policy_families:
            assert isinstance(pol, CaseEffectPolicyFamily)
        for act in e.activation_conditions:
            assert isinstance(act, ActivationCondition)
        for blk in e.blocking_conditions:
            assert isinstance(blk, BlockingCondition)


# ===========================================================================
# (E) IDAFA is construction-trigger only
# ===========================================================================


def test_idafa_entry_has_no_case_effect_policy():
    """
    IDAFA must NOT carry a jarr-policy (or any policy other than
    NO_CASE_EFFECT_POLICY_FAMILY). Case-effect of mudaf-ilayh belongs
    to a later layer.
    """
    reg = build_default_nahw_operator_registry()
    es = reg.entries_for_family(OperatorTriggerFamily.POSSIBLE_IDAFA_FAMILY)
    assert len(es) >= 1
    for e in es:
        assert e.case_effect_policy_families == (
            CaseEffectPolicyFamily.NO_CASE_EFFECT_POLICY_FAMILY,
        ), (
            f"IDAFA entry {e.operator_id} must carry only "
            f"NO_CASE_EFFECT_POLICY_FAMILY; got {e.case_effect_policy_families}"
        )
        assert ExpectedRelationFamily.IDAFA_LIKE in e.expected_relation_families


# ===========================================================================
# (F) UNRESOLVED_TRIGGER lookup returns empty + warning
# ===========================================================================


def test_entries_for_family_unresolved_is_empty_tuple():
    reg = build_default_nahw_operator_registry()
    assert reg.entries_for_family(OperatorTriggerFamily.UNRESOLVED_TRIGGER) == ()


def test_unresolved_trigger_lookup_emits_warning_residual():
    """When a trigger emits UNRESOLVED_TRIGGER, the registry lookup must
    emit REGISTRY_FAMILY_HAS_NO_ENTRIES as a warning (not a blocker)."""
    reg = build_default_nahw_operator_registry()
    # Use a nominal frame with a single noun — the trigger layer falls
    # back to UNRESOLVED_TRIGGER in that path? Actually NominalFrame fires
    # IBTIDAA, so use FragmentFrame instead via direct trigger fabrication.
    # Simpler: directly build a trigger whose families include
    # UNRESOLVED_TRIGGER by going through the public pipeline.
    # We use a particle-led frame with HARF_UNRESOLVED to get an
    # UNRESOLVED_TRIGGER fallback.
    p = _particle_vector(mufrad_id="p_unr", type_id=ParticleTypeID.HARF_UNRESOLVED)
    n = _noun_vector(
        mufrad_id="n",
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),),
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    # Trigger should have at least one UNRESOLVED_TRIGGER family (it has no
    # particle mapping and no other trigger fires).
    assert OperatorTriggerFamily.UNRESOLVED_TRIGGER in trig.triggered_families

    results = reg.entries_for_trigger(trig)
    unresolved_result = next(
        r for r in results
        if r.family is OperatorTriggerFamily.UNRESOLVED_TRIGGER
    )
    assert unresolved_result.matched_entries == ()
    has_warning = any(
        r.type is ResidualType.REGISTRY_FAMILY_HAS_NO_ENTRIES
        and r.severity is ResidualSeverity.WARNING
        for r in unresolved_result.lookup_residuals
    )
    assert has_warning
    # And NOT a blocker.
    assert not any(r.is_blocker() for r in unresolved_result.lookup_residuals)


# ===========================================================================
# (G) Competing entries inside one family are preserved
# ===========================================================================


def test_competing_entries_in_inna_family_preserved_with_info_residual():
    reg = build_default_nahw_operator_registry()
    p = _particle_vector(mufrad_id="p_inna", type_id=ParticleTypeID.HARF_NASIKH_INNA)
    n = _noun_vector(
        mufrad_id="n_kitab",
        potentials=(
            _potential(
                CaseSignValue.FATHA,
                CaseSignFamily.ORIGINAL,
                surface_kind=SurfaceEffectType.FINAL_FATHA,
            ),
        ),
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    results = reg.entries_for_trigger(trig)
    inna_result = next(
        r for r in results
        if r.family is OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY
    )
    assert len(inna_result.matched_entries) >= 2
    has_info = any(
        r.type is ResidualType.REGISTRY_FAMILY_HAS_MULTIPLE_ENTRIES_PRESERVED
        and r.severity is ResidualSeverity.INFO
        for r in inna_result.lookup_residuals
    )
    assert has_info
    # And NOT a blocker.
    assert not any(r.is_blocker() for r in inna_result.lookup_residuals)


# ===========================================================================
# (H) Competing FAMILIES preserved across lookup
# ===========================================================================


def test_inna_plus_ibtidaa_both_yield_lookup_results():
    """
    The PR #14 invariant says NASIKH_INNA and IBTIDAA both fire from
    `إنّ الكتابَ`. The registry MUST emit one lookup result per family,
    with neither suppressed. This is the cross-layer invariant of the
    plan.
    """
    reg = build_default_nahw_operator_registry()
    frame = _make_inna_plus_nominal_frame()
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)

    # Sanity check: the trigger preserves both families.
    families = set(trig.triggered_families)
    assert OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY in families
    assert OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY in families

    results = reg.entries_for_trigger(trig)
    result_families = {r.family for r in results}
    # Both families are looked up; neither is dropped.
    assert OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY in result_families
    assert OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY in result_families
    # The number of results equals the number of triggered families
    # (registry preserves order and count).
    assert len(results) == len(trig.triggered_families)

    # No blocker residuals at the registry level.
    for r in results:
        assert not any(res.is_blocker() for res in r.lookup_residuals)


# ===========================================================================
# (I) Residual inheritance
# ===========================================================================


def test_lookup_inherits_all_trigger_residuals():
    reg = build_default_nahw_operator_registry()
    frame = _make_inna_plus_nominal_frame()
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    trigger_residuals = trig.get_all_residuals()

    results = reg.entries_for_trigger(trig)
    for r in results:
        # Identity-based superset check (Residual is not hashable).
        ids = {id(x) for x in r.inherited_residuals}
        for tr in trigger_residuals:
            assert id(tr) in ids, (
                "lookup.inherited_residuals must be a superset of "
                "trigger.get_all_residuals()"
            )


# ===========================================================================
# (J) Rank ceiling
# ===========================================================================


def test_lookup_rank_never_exceeds_trigger_rank():
    reg = build_default_nahw_operator_registry()
    frame = _make_inna_plus_nominal_frame()
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    for r in reg.entries_for_trigger(trig):
        assert r.rank <= trig.rank, (
            f"lookup.rank={r.rank} exceeds trigger.rank={trig.rank} for "
            f"family {r.family.value}"
        )


# ===========================================================================
# (K) ID propagation
# ===========================================================================


def test_lookup_propagates_ids_from_trigger():
    reg = build_default_nahw_operator_registry()
    frame = _make_inna_plus_nominal_frame()
    matrix = build_case_sign_matrix(frame)
    trig = build_operator_trigger_potential(frame, matrix)
    for r in reg.entries_for_trigger(trig):
        assert r.trigger_id == trig.trigger_id
        assert r.frame_id == trig.frame_id
        assert r.matrix_id == trig.matrix_id


# ===========================================================================
# (L) Cross-layer non-regression — single-particle JARR sanity
# ===========================================================================


def test_jarr_particle_yields_jarr_entries_lookup():
    reg = build_default_nahw_operator_registry()
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
    results = reg.entries_for_trigger(trig)
    jarr_result = next(
        r for r in results
        if r.family is OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY
    )
    op_ids = {e.operator_id for e in jarr_result.matched_entries}
    assert {"HARF_JARR_MIN", "HARF_JARR_FI", "HARF_JARR_BA"} <= op_ids
    # Every entry must belong to the jarr family.
    for e in jarr_result.matched_entries:
        assert e.family is OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY
        assert (
            CaseEffectPolicyFamily.JARR_POLICY_FAMILY
            in e.case_effect_policy_families
        )


def test_lookup_result_rejects_entry_from_wrong_family():
    """Direct construction guard: a lookup result may not contain an
    entry from a different family."""
    reg = build_default_nahw_operator_registry()
    inna_entry = reg.entry_by_id("INNA")
    assert inna_entry is not None
    with pytest.raises(ValueError):
        OperatorRegistryLookupResult(
            trigger_id="t",
            frame_id="f",
            matrix_id="m",
            family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
            matched_entries=(inna_entry,),
            rank=LughaRank.SAMA,
            inherited_residuals=(),
            lookup_residuals=(),
        )


def test_registry_is_immutable():
    """Adding entries after construction must not be possible via the
    public API; mutations to internal dicts must not break later
    queries."""
    reg = build_default_nahw_operator_registry()
    snapshot = reg.entries_for_family(
        OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY
    )
    assert isinstance(snapshot, tuple)
    # No public setter exists.
    public = {n for n in dir(reg) if not n.startswith("_")}
    setters = {n for n in public if n.startswith("add_") or n.startswith("set_") or n == "register"}
    assert setters == set()


# ===========================================================================
# (M) Immutability hardening (PR #16a)
# ===========================================================================


def test_registry_internal_indexes_are_mapping_proxy():
    """Internal _by_id and _by_family dictionaries must be
    MappingProxyType to prevent mutation."""
    reg = build_default_nahw_operator_registry()
    assert isinstance(reg._by_id, MappingProxyType)
    assert isinstance(reg._by_family, MappingProxyType)


def test_registry_by_id_cannot_be_mutated():
    """Attempting to mutate _by_id must raise TypeError."""
    reg = build_default_nahw_operator_registry()
    with pytest.raises(TypeError):
        reg._by_id["FAKE"] = next(iter(reg.all_entries()))


def test_registry_by_family_cannot_be_mutated():
    """Attempting to mutate _by_family must raise TypeError."""
    reg = build_default_nahw_operator_registry()
    fam = next(iter(reg.all_families()))
    with pytest.raises(TypeError):
        reg._by_family[fam] = ()


def test_registry_internal_slots_cannot_be_reassigned():
    """Attempting to reassign internal storage slots must raise
    AttributeError."""
    reg = build_default_nahw_operator_registry()
    with pytest.raises(AttributeError):
        reg._by_id = {}


def test_registry_internal_slots_cannot_be_deleted():
    """Attempting to delete internal storage slots must raise
    AttributeError."""
    reg = build_default_nahw_operator_registry()
    with pytest.raises(AttributeError):
        del reg._by_id


def test_registry_mutation_attempts_do_not_affect_lookup_results():
    """Even after attempting mutation (which fails), lookup results
    remain unchanged."""
    reg = build_default_nahw_operator_registry()
    # Snapshot original lookup result.
    original_jarr = reg.entries_for_family(
        OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY
    )
    original_jarr_ids = {e.operator_id for e in original_jarr}

    # Attempt mutation (will fail).
    with pytest.raises(TypeError):
        reg._by_family[OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY] = ()

    # Verify lookup still returns original data.
    after_attempt = reg.entries_for_family(
        OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY
    )
    after_attempt_ids = {e.operator_id for e in after_attempt}
    assert after_attempt_ids == original_jarr_ids
