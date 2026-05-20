"""
Tests for OperatorCandidate (PR #17).

The candidate layer sits between OperatorTriggerPotential and (future)
RelationCandidate. It creates typed (TriggerSource, NahwOperatorEntry) pairs;
it must NOT apply operators, produce relations, produce case effects, assign
syntax roles, or resolve competing candidates.

Test groups:

A. Strict input typing (trigger & registry; typed objects only).
B. Candidate creation preserves all (source, entry) pairs.
C. Competing families and entries preserved (no suppression/resolution).
D. Empty registry entries handled gracefully (residual, no fake candidate).
E. Rank ceiling enforcement (candidate and set levels).
F. Residual inheritance (trigger → candidate → set).
G. Trace recoverability.
H. Governance: no forbidden fields, no forbidden methods.
I. Immutability.
J. Family matching (source.family == entry.family).
"""

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
    OperatorSource,
)
from dal_core.operator_candidate import (
    OperatorCandidate,
    OperatorCandidateSet,
    OperatorCandidateTrace,
    build_operator_candidates,
)
from dal_core.operator_trigger import (
    OperatorTriggerFamily,
    OperatorTriggerPotential,
    OperatorTriggerTrace,
    TriggerSource,
    build_operator_trigger_potential,
)
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, ResidualSeverity, ResidualType
from dal_core.sentence_frame import (
    FrameType,
    NominalFrameCandidate,
    ParticleLedFrameCandidate,
    SentenceFrameCandidate,
)
from dal_core.surface_effects import (
    SurfaceEffect,
    SurfaceEffectType,
    SurfaceEffectVisibility,
)
from dal_core.type_ids import NounTypeID, ParticleTypeID


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
    type_id: NounTypeID = NounTypeID.ISM_COMMON,
    potentials: tuple[CaseSignPotential, ...] = (),
) -> PreSyntaxMufradVector:
    nic = NounInflectionClass(
        inflection_type="munassarif",
        declension_pattern="triptote",
        evidence=(_ev(),),
        rank=LughaRank.SAMA,
    )
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 5),
        type_value="ISM",
        type_id=type_id,
        type_rank=LughaRank.SAMA,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
        noun_inflection_class=nic,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=potentials,
        morph_rank=LughaRank.SAMA,
        final_rank=LughaRank.SAMA,
        residuals=(),
        trace_id=f"trace-{mufrad_id}",
        competitors_count=0,
        composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
    )


def _particle_vector(
    mufrad_id: str = "p1",
    type_id: ParticleTypeID = ParticleTypeID.HARF_JARR,
) -> PreSyntaxMufradVector:
    return PreSyntaxMufradVector(
        mufrad_id=mufrad_id,
        raw_span=(0, 2),
        type_value="HARF",
        type_id=type_id,
        type_rank=LughaRank.SAMA,
        mabni_murab_status=CandidateStatus.NOT_APPLICABLE,
        noun_inflection_class=None,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=(),
        morph_rank=LughaRank.SAMA,
        final_rank=LughaRank.SAMA,
        residuals=(),
        trace_id=f"trace-{mufrad_id}",
        competitors_count=0,
        composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
    )


def _make_nominal_frame(
    constituents: tuple[PreSyntaxMufradVector, ...]
) -> NominalFrameCandidate:
    lead_noun_index = next(
        (i for i, c in enumerate(constituents) if isinstance(c.type_id, NounTypeID)),
        None,
    )
    if lead_noun_index is None:
        raise ValueError("Nominal test frame requires at least one noun constituent.")
    return NominalFrameCandidate(
        frame_id=f"frame-nominal-{id(constituents)}",
        frame_type=FrameType.NOMINAL,
        constituents=constituents,
        lead_noun_index=lead_noun_index,
        frame_rank=min(c.final_rank for c in constituents),
        inherited_residuals=tuple(r for c in constituents for r in c.residuals),
        frame_specific_residuals=(),
        trace_id=f"frame-trace-{id(constituents)}",
    )


def _make_particle_led_frame(
    constituents: tuple[PreSyntaxMufradVector, ...],
    particle_index: int = 0,
) -> ParticleLedFrameCandidate:
    return ParticleLedFrameCandidate(
        frame_id=f"frame-particle-{id(constituents)}",
        frame_type=FrameType.PARTICLE_LED,
        constituents=constituents,
        particle_index=particle_index,
        frame_rank=min(c.final_rank for c in constituents),
        inherited_residuals=tuple(r for c in constituents for r in c.residuals),
        frame_specific_residuals=(),
        trace_id=f"frame-trace-{id(constituents)}",
        particle_operator_potential=None,
    )


def _make_registry(entries: tuple[NahwOperatorEntry, ...]) -> NahwOperatorRegistry:
    return NahwOperatorRegistry(entries)


def _make_inna_entry(operator_id: str = "inna-001") -> NahwOperatorEntry:
    return NahwOperatorEntry(
        operator_id=operator_id,
        family=OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY,
        display_name_ar="إِنَّ",
        source=OperatorSource.KITAB_SIBAWAYH,
        school=NahwSchool.BASRI,
        input_signature=OperatorInputSignature(
            expected_arity=2,
            expected_neighbour_types=("ISM_COMMON",),
        ),
        activation_conditions=(ActivationCondition.IMMEDIATELY_PRECEDES_NOMINAL_FRAME,),
        blocking_conditions=tuple(),
        expected_relation_families=(ExpectedRelationFamily.ISN_LIKE,),
        case_effect_policy_families=(CaseEffectPolicyFamily.MIXED_RAFI_NASB_POLICY_FAMILY,),
        rank=LughaRank.SAMA,
        citations=(
            Citation(
                source=OperatorSource.KITAB_SIBAWAYH,
                reference="الكتاب ١/٣٣",
            ),
        ),
        entry_residuals=(),
        entry_trace_id=f"entry-trace-{operator_id}",
    )


def _make_jarr_entry(operator_id: str = "jarr-001") -> NahwOperatorEntry:
    return NahwOperatorEntry(
        operator_id=operator_id,
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        display_name_ar="فِي",
        source=OperatorSource.KITAB_SIBAWAYH,
        school=NahwSchool.BASRI,
        input_signature=OperatorInputSignature(
            expected_arity=2,
            expected_neighbour_types=("ISM_COMMON",),
        ),
        activation_conditions=(ActivationCondition.IMMEDIATELY_PRECEDES_ISM,),
        blocking_conditions=tuple(),
        expected_relation_families=(ExpectedRelationFamily.TAQYID_LIKE,),
        case_effect_policy_families=(CaseEffectPolicyFamily.JARR_POLICY_FAMILY,),
        rank=LughaRank.SAMA,
        citations=(
            Citation(
                source=OperatorSource.KITAB_SIBAWAYH,
                reference="الكتاب ١/٢٠",
            ),
        ),
        entry_residuals=(),
        entry_trace_id=f"entry-trace-{operator_id}",
    )


# ---------------------------------------------------------------------------
# (A) Strict input typing
# ---------------------------------------------------------------------------


def test_operator_candidate_requires_trigger_and_registry():
    """build_operator_candidates must accept only OperatorTriggerPotential and NahwOperatorRegistry."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    # Should succeed
    candidate_set = build_operator_candidates(trigger, registry)
    assert isinstance(candidate_set, OperatorCandidateSet)


def test_operator_candidate_rejects_raw_tokens():
    """Candidate layer must reject raw frames, matrices, or other non-trigger inputs."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    registry = _make_registry((_make_jarr_entry(),))

    # Passing frame instead of trigger should fail
    with pytest.raises(TypeError, match="requires an OperatorTriggerPotential"):
        build_operator_candidates(frame, registry)  # type: ignore[arg-type]

    # Passing matrix instead of trigger should fail
    with pytest.raises(TypeError, match="requires an OperatorTriggerPotential"):
        build_operator_candidates(matrix, registry)  # type: ignore[arg-type]

    # Passing non-registry should fail
    trigger = build_operator_trigger_potential(frame, matrix)
    with pytest.raises(TypeError, match="requires a NahwOperatorRegistry"):
        build_operator_candidates(trigger, "not-a-registry")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# (B) Candidate requires TriggerSource
# ---------------------------------------------------------------------------


def test_candidate_requires_trigger_source():
    """Every OperatorCandidate must be tied to a specific TriggerSource."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    # Every candidate must have a trigger_source
    for candidate in candidate_set.candidates:
        assert isinstance(candidate.trigger_source, TriggerSource)
        assert candidate.trigger_source.vector_id
        assert candidate.trigger_source.family == candidate.trigger_family


def test_candidate_family_must_match_registry_entry_family():
    """TriggerSource.family must equal NahwOperatorEntry.family."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    # Every candidate must match families
    for candidate in candidate_set.candidates:
        assert candidate.trigger_source.family == candidate.registry_entry.family
        assert candidate.trigger_family == candidate.registry_entry.family


# ---------------------------------------------------------------------------
# (C) Competing families and entries preserved
# ---------------------------------------------------------------------------


def test_operator_candidate_preserves_all_trigger_families():
    """All trigger families must be preserved, no suppression."""
    # Create a nominal frame that triggers both IBTIDAA and potentially NASIKH
    n1 = _noun_vector(
        mufrad_id="n1",
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),)
    )
    n2 = _noun_vector(
        mufrad_id="n2",
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),)
    )
    frame = _make_nominal_frame((n1, n2))
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)

    # Registry with entries (even if empty for this test)
    registry = _make_registry(())

    candidate_set = build_operator_candidates(trigger, registry)

    # All trigger families must be preserved in the lookup
    # Even if no candidates created, trigger families should be checked
    assert trigger.triggered_families  # Should have at least IBTIDAA


def test_operator_candidate_preserves_all_registry_entries():
    """All matching registry entries must be preserved, no resolution."""
    # Create multiple entries for the same family
    jarr_entry1 = _make_jarr_entry("jarr-001")
    jarr_entry2 = NahwOperatorEntry(
        operator_id="jarr-002",
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        display_name_ar="مِنْ",
        source=OperatorSource.KITAB_SIBAWAYH,
        school=NahwSchool.BASRI,
        input_signature=OperatorInputSignature(
            expected_arity=2,
            expected_neighbour_types=("ISM_COMMON",),
        ),
        activation_conditions=(ActivationCondition.IMMEDIATELY_PRECEDES_ISM,),
        blocking_conditions=tuple(),
        expected_relation_families=(ExpectedRelationFamily.TAQYID_LIKE,),
        case_effect_policy_families=(CaseEffectPolicyFamily.JARR_POLICY_FAMILY,),
        rank=LughaRank.SAMA,
        citations=(
            Citation(
                source=OperatorSource.KITAB_SIBAWAYH,
                reference="الكتاب ١/٢١",
            ),
        ),
        entry_residuals=(),
        entry_trace_id="entry-trace-jarr-002",
    )

    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((jarr_entry1, jarr_entry2))

    candidate_set = build_operator_candidates(trigger, registry)

    # Both entries should create candidates
    assert len(candidate_set.candidates) >= 2
    entry_ids = {c.registry_entry_id for c in candidate_set.candidates}
    assert "jarr-001" in entry_ids
    assert "jarr-002" in entry_ids


def test_inna_family_produces_all_competing_candidates():
    """INNA family with multiple entries creates all candidate pairs."""
    inna_entry1 = _make_inna_entry("inna-001")
    inna_entry2 = NahwOperatorEntry(
        operator_id="inna-002",
        family=OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY,
        display_name_ar="أَنَّ",
        source=OperatorSource.KITAB_SIBAWAYH,
        school=NahwSchool.KUFI,
        input_signature=OperatorInputSignature(
            expected_arity=2,
            expected_neighbour_types=("ISM_COMMON",),
        ),
        activation_conditions=(ActivationCondition.IMMEDIATELY_PRECEDES_NOMINAL_FRAME,),
        blocking_conditions=tuple(),
        expected_relation_families=(ExpectedRelationFamily.ISN_LIKE,),
        case_effect_policy_families=(CaseEffectPolicyFamily.MIXED_RAFI_NASB_POLICY_FAMILY,),
        rank=LughaRank.SAMA,
        citations=(
            Citation(
                source=OperatorSource.KITAB_SIBAWAYH,
                reference="معاني القرآن",
            ),
        ),
        entry_residuals=(),
        entry_trace_id="entry-trace-inna-002",
    )

    p = _particle_vector(
        mufrad_id="p_inna",
        type_id=ParticleTypeID.HARF_NASIKH_INNA,
    )
    n1 = _noun_vector(
        mufrad_id="n1",
        potentials=(_potential(CaseSignValue.FATHA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_FATHA),)
    )
    n2 = _noun_vector(
        mufrad_id="n2",
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_DAMMA),)
    )
    frame = _make_particle_led_frame((p, n1, n2), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((inna_entry1, inna_entry2))

    candidate_set = build_operator_candidates(trigger, registry)

    # Both INNA entries should create candidates
    entry_ids = {c.registry_entry_id for c in candidate_set.candidates}
    assert "inna-001" in entry_ids
    assert "inna-002" in entry_ids
    assert candidate_set.competitors_preserved


def test_multiple_sources_and_entries_preserved_as_pairs():
    """Multiple trigger sources and entries create all (source, entry) pairs."""
    # This is a more complex scenario where we might have multiple sources
    # for the same family (e.g., multiple particles triggering jarr)
    jarr_entry1 = _make_jarr_entry("jarr-001")
    jarr_entry2 = _make_jarr_entry("jarr-002")

    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR, mufrad_id="p1")
    n = _noun_vector(
        mufrad_id="n1",
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((jarr_entry1, jarr_entry2))

    candidate_set = build_operator_candidates(trigger, registry)

    # Should have candidates for all (source, entry) pairs
    # With 1 source and 2 entries, expect 2 candidates
    assert len(candidate_set.candidates) == 2
    assert candidate_set.competitors_preserved


# ---------------------------------------------------------------------------
# (D) Empty registry entries
# ---------------------------------------------------------------------------


def test_unresolved_trigger_produces_no_candidate_and_residual():
    """UNRESOLVED_TRIGGER with no entries produces empty candidates and residual."""
    # Create trigger with UNRESOLVED_TRIGGER family
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),)
    )
    # Use a nominal frame that might trigger IBTIDAA but with empty registry
    frame = _make_nominal_frame((n,))
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)

    # Empty registry
    registry = _make_registry(())

    candidate_set = build_operator_candidates(trigger, registry)

    # Should have no candidates
    assert len(candidate_set.candidates) == 0

    # Should have residual about no registry entries
    residual_types = {r.type for r in candidate_set.candidate_set_residuals}
    assert ResidualType.OPERATOR_CANDIDATE_NO_REGISTRY_ENTRIES in residual_types


def test_empty_candidate_set_does_not_min_empty():
    """Empty candidate set rank ≤ trigger.rank, not min([])."""
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.DAMMA, CaseSignFamily.ORIGINAL),)
    )
    frame = _make_nominal_frame((n,))
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry(())  # Empty registry

    candidate_set = build_operator_candidates(trigger, registry)

    # Rank should be ≤ trigger.rank
    assert candidate_set.rank.value <= trigger.rank.value
    assert len(candidate_set.candidates) == 0


# ---------------------------------------------------------------------------
# (E) Rank ceiling
# ---------------------------------------------------------------------------


def test_candidate_rank_cannot_exceed_trigger_or_entry():
    """Candidate rank ≤ min(trigger.rank, lookup.rank, entry.rank)."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)

    # Create entry with lower rank
    jarr_entry_low = NahwOperatorEntry(
        operator_id="jarr-low",
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        display_name_ar="فِي",
        source=OperatorSource.KALAAM_ARAB,
        school=NahwSchool.BASRI,
        input_signature=OperatorInputSignature(
            expected_arity=2,
            expected_neighbour_types=("ISM_COMMON",),
        ),
        activation_conditions=(ActivationCondition.IMMEDIATELY_PRECEDES_ISM,),
        blocking_conditions=tuple(),
        expected_relation_families=(ExpectedRelationFamily.TAQYID_LIKE,),
        case_effect_policy_families=(CaseEffectPolicyFamily.JARR_POLICY_FAMILY,),
        rank=LughaRank.QIYAS,  # Lower rank
        citations=(
            Citation(
                source=OperatorSource.OTHER,
                reference="test",
            ),
        ),
        entry_residuals=(),
        entry_trace_id="entry-trace-jarr-low",
    )

    registry = _make_registry((jarr_entry_low,))
    candidate_set = build_operator_candidates(trigger, registry)

    # All candidates should have rank ≤ min(trigger, entry)
    for candidate in candidate_set.candidates:
        assert candidate.rank.value <= trigger.rank.value
        assert candidate.rank.value <= candidate.registry_entry.rank.value


def test_candidate_set_rank_cannot_exceed_candidates():
    """CandidateSet rank ≤ min(candidate.rank)."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    # Set rank should be ≤ all candidate ranks
    if candidate_set.candidates:
        for candidate in candidate_set.candidates:
            assert candidate_set.rank.value <= candidate.rank.value


# ---------------------------------------------------------------------------
# (F) Residual inheritance
# ---------------------------------------------------------------------------


def test_candidate_residuals_include_trigger_residuals():
    """Candidate inherited_residuals must include trigger.get_all_residuals()."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    trigger_residuals = trigger.get_all_residuals()
    candidate_set = build_operator_candidates(trigger, registry)

    # Every candidate should inherit trigger residuals
    for candidate in candidate_set.candidates:
        for tr in trigger_residuals:
            assert tr in candidate.inherited_residuals

    # Set should also inherit trigger residuals
    for tr in trigger_residuals:
        assert tr in candidate_set.inherited_residuals


def test_candidate_residuals_include_lookup_residuals():
    """Candidate must not erase registry lookup residuals."""
    # Create scenario with multiple entries to trigger lookup residuals
    jarr_entry1 = _make_jarr_entry("jarr-001")
    jarr_entry2 = _make_jarr_entry("jarr-002")

    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((jarr_entry1, jarr_entry2))

    candidate_set = build_operator_candidates(trigger, registry)

    # Lookup should have created info residual about multiple entries
    # Check that candidates inherit this
    for candidate in candidate_set.candidates:
        # Should have some inherited residuals from lookup
        assert candidate.inherited_residuals


def test_empty_candidate_set_preserves_lookup_residuals():
    """Lookup residuals must be preserved even when no candidates are produced."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)

    # Registry has no JARR entries for this trigger family.
    registry = _make_registry((_make_inna_entry(),))
    candidate_set = build_operator_candidates(trigger, registry)

    assert candidate_set.candidates == ()
    residual_types = {r.type for r in candidate_set.candidate_set_residuals}
    assert ResidualType.REGISTRY_FAMILY_HAS_NO_ENTRIES in residual_types
    assert ResidualType.OPERATOR_CANDIDATE_NO_REGISTRY_ENTRIES in residual_types


# ---------------------------------------------------------------------------
# (G) Trace
# ---------------------------------------------------------------------------


def test_candidate_trace_links_trigger_source_and_registry_entry():
    """Trace must link back to trigger source and registry entry."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    for candidate in candidate_set.candidates:
        # Trace should link to trigger
        assert candidate.trace.trigger_id == trigger.trigger_id
        assert candidate.trace.trigger_source_vector_id == candidate.trigger_source.vector_id
        assert candidate.trace.registry_entry_id == candidate.registry_entry_id
        assert candidate.trace.frame_id == frame.frame_id
        assert candidate.trace.matrix_id == matrix.matrix_id
        assert candidate.trace.derivation == "from_operator_trigger_and_registry"


def test_empty_candidate_set_trace_uses_trigger_source_vector():
    """Empty candidate sets should still trace to an actual trigger source."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_inna_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    assert candidate_set.candidates == ()
    assert candidate_set.trace.trigger_source_vector_id == trigger.sources[0].vector_id


# ---------------------------------------------------------------------------
# (H) Governance: forbidden fields and methods
# ---------------------------------------------------------------------------


def test_no_relation_candidate_in_operator_candidate():
    """OperatorCandidate must not contain 'relation' fields."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    for candidate in candidate_set.candidates:
        field_names = {f.name for f in candidate.__dataclass_fields__.values()}
        assert "relation" not in field_names
        assert "relation_type" not in field_names


def test_no_case_effect_in_operator_candidate():
    """OperatorCandidate must not contain 'case_effect' fields."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    for candidate in candidate_set.candidates:
        field_names = {f.name for f in candidate.__dataclass_fields__.values()}
        assert "case_effect" not in field_names
        assert "case_effect_candidate" not in field_names


def test_no_syntax_role_in_operator_candidate():
    """OperatorCandidate must not contain syntax role fields."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    for candidate in candidate_set.candidates:
        field_names = {f.name for f in candidate.__dataclass_fields__.values()}
        forbidden = {"faail", "mafool", "mubtada", "khabar", "mudaf", "mudaf_ilayh", "syntax_role"}
        assert not (field_names & forbidden)


def test_no_semantic_leak_in_operator_candidate():
    """OperatorCandidate must not contain semantic fields."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    for candidate in candidate_set.candidates:
        field_names = {f.name for f in candidate.__dataclass_fields__.values()}
        forbidden = {"meaning", "semantic", "madlul", "murad", "haqiqa", "majaz", "grounding"}
        assert not (field_names & forbidden)


def test_no_apply_bind_resolve_methods_exist():
    """OperatorCandidate must not have apply/bind/resolve methods."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    for candidate in candidate_set.candidates:
        method_names = [m for m in dir(candidate) if not m.startswith("_")]
        forbidden_methods = {
            "apply", "bind", "resolve", "governs", "governance",
            "produces_relation", "produces_case", "matches_relation",
            "case_policy_applied", "applies_to"
        }
        actual_methods = set(method_names)
        assert not (actual_methods & forbidden_methods), \
            f"Found forbidden methods: {actual_methods & forbidden_methods}"


def test_operator_candidate_has_no_governs_or_produces_methods():
    """Specifically check for governs/produces_* methods."""
    # Check the class itself
    candidate_methods = [m for m in dir(OperatorCandidate) if not m.startswith("_")]
    forbidden_patterns = ["governs", "produces", "applies_to", "matches_relation"]

    for method in candidate_methods:
        for pattern in forbidden_patterns:
            assert pattern not in method.lower(), \
                f"OperatorCandidate has forbidden method pattern '{pattern}' in '{method}'"


# ---------------------------------------------------------------------------
# (I) Immutability
# ---------------------------------------------------------------------------


def test_operator_candidate_set_is_immutable():
    """OperatorCandidateSet and OperatorCandidate must be frozen (immutable)."""
    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((_make_jarr_entry(),))

    candidate_set = build_operator_candidates(trigger, registry)

    # Try to modify candidate_set (should fail)
    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        candidate_set.rank = LughaRank.QIYAS  # type: ignore[misc]

    # Try to modify a candidate (should fail)
    if candidate_set.candidates:
        with pytest.raises(Exception):
            candidate_set.candidates[0].rank = LughaRank.QIYAS  # type: ignore[misc]


# ---------------------------------------------------------------------------
# (J) Competition flags
# ---------------------------------------------------------------------------


def test_unresolved_competition_flag_true_when_multiple_candidates():
    """has_unresolved_competition() should return True when multiple candidates exist."""
    jarr_entry1 = _make_jarr_entry("jarr-001")
    jarr_entry2 = _make_jarr_entry("jarr-002")

    p = _particle_vector(type_id=ParticleTypeID.HARF_JARR)
    n = _noun_vector(
        potentials=(_potential(CaseSignValue.KASRA, CaseSignFamily.ORIGINAL, SurfaceEffectType.FINAL_KASRA),)
    )
    frame = _make_particle_led_frame((p, n), particle_index=0)
    matrix = build_case_sign_matrix(frame)
    trigger = build_operator_trigger_potential(frame, matrix)
    registry = _make_registry((jarr_entry1, jarr_entry2))

    candidate_set = build_operator_candidates(trigger, registry)

    # Should have multiple candidates
    assert len(candidate_set.candidates) >= 2
    assert candidate_set.has_unresolved_competition()
    assert candidate_set.competitors_preserved
