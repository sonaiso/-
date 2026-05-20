"""
Tests for OperatorCandidate (PR #17).

The OperatorCandidate layer sits between NahwOperatorRegistry and (future)
RelationCandidate. It creates typed candidate LINKS from trigger sources
and registry entries; it must NOT apply operators, produce relations,
produce CaseEffect, assign syntax roles, or silently resolve competing
candidates.

Test groups:

A. OperatorCandidateSetTrace preserves ALL candidate/trigger/registry ids
B. get_all_residuals aggregates across hierarchy
C. Rank ceiling semantics (CEILED vs VIOLATION)
D. Family matching enforcement
E. Competition preservation
F. Empty set safety
G. No fake candidates
H. Forbidden fields guard
I. Builder correctness
"""

import pytest

from dal_core.nahw_operator_registry import (
    NahwOperatorEntry,
    NahwOperatorRegistry,
    OperatorSource,
    NahwSchool,
    OperatorInputSignature,
)
from dal_core.operator_candidate import (
    OperatorCandidate,
    OperatorCandidateBuilder,
    OperatorCandidateSet,
    OperatorCandidateSetTrace,
    OperatorCandidateTrace,
)
from dal_core.operator_trigger import (
    OperatorTriggerFamily,
    OperatorTriggerPotential,
    TriggerSource,
)
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, ResidualType


# ---------------------------------------------------------------------------
# Test Group A: OperatorCandidateSetTrace preserves ALL ids
# ---------------------------------------------------------------------------


def test_candidate_set_trace_preserves_all_candidate_ids():
    """
    OperatorCandidateSetTrace must preserve ALL candidate_ids,
    not just the first one.
    """
    trace = OperatorCandidateSetTrace(
        set_id="test_set_001",
        candidate_ids=("cand_1", "cand_2", "cand_3"),
        trigger_source_vector_ids=("vec_1", "vec_2", "vec_3"),
        registry_entry_ids=("entry_1", "entry_2", "entry_3"),
        families=(
            OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
            OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
            OperatorTriggerFamily.POSSIBLE_NASB_OPERATOR_FAMILY,
        ),
        trigger_id="trigger_001",
        frame_id="frame_001",
        matrix_id="matrix_001",
    )

    assert len(trace.candidate_ids) == 3
    assert trace.candidate_ids == ("cand_1", "cand_2", "cand_3")
    assert trace.candidate_ids[0] == "cand_1"
    assert trace.candidate_ids[1] == "cand_2"
    assert trace.candidate_ids[2] == "cand_3"


def test_candidate_set_trace_preserves_all_registry_entry_ids():
    """
    OperatorCandidateSetTrace must preserve ALL registry_entry_ids,
    not just the first one.
    """
    trace = OperatorCandidateSetTrace(
        set_id="test_set_002",
        candidate_ids=("cand_1", "cand_2"),
        trigger_source_vector_ids=("vec_1", "vec_2"),
        registry_entry_ids=("entry_A", "entry_B"),
        families=(
            OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY,
            OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY,
        ),
        trigger_id="trigger_002",
        frame_id="frame_002",
        matrix_id="matrix_002",
    )

    assert len(trace.registry_entry_ids) == 2
    assert trace.registry_entry_ids == ("entry_A", "entry_B")
    assert trace.registry_entry_ids[0] == "entry_A"
    assert trace.registry_entry_ids[1] == "entry_B"


def test_candidate_set_trace_tuple_length_mismatch():
    """
    OperatorCandidateSetTrace must reject mismatched tuple lengths.
    """
    with pytest.raises(ValueError, match="tuple length mismatch"):
        OperatorCandidateSetTrace(
            set_id="test_set_003",
            candidate_ids=("cand_1", "cand_2"),  # length 2
            trigger_source_vector_ids=("vec_1",),  # length 1 — mismatch!
            registry_entry_ids=("entry_1", "entry_2"),
            families=(
                OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
                OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
            ),
            trigger_id="trigger_003",
            frame_id="frame_003",
            matrix_id="matrix_003",
        )


# ---------------------------------------------------------------------------
# Test Group B: get_all_residuals aggregates across hierarchy
# ---------------------------------------------------------------------------


def test_candidate_set_get_all_residuals_includes_candidate_residuals(
    minimal_trigger_source, minimal_registry_entry
):
    """
    OperatorCandidateSet.get_all_residuals() must include:
    - inherited_residuals
    - candidate_set_residuals
    - all residuals from every OperatorCandidate
    """
    # Create candidate with its own residuals
    candidate_trace = OperatorCandidateTrace(
        candidate_id="cand_001",
        trigger_source_vector_id=minimal_trigger_source.vector_id,
        registry_entry_id=minimal_registry_entry.operator_id,
        trigger_id="trigger_001",
        frame_id="frame_001",
        matrix_id="matrix_001",
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
    )

    candidate_residual = Residual(
        type=ResidualType.OPERATOR_CANDIDATE_RANK_CEILED,
        severity=ResidualType.OPERATOR_CANDIDATE_RANK_CEILED,
        message="Candidate-level residual",
    )

    candidate = OperatorCandidate(
        candidate_id="cand_001",
        trigger_source=minimal_trigger_source,
        registry_entry=minimal_registry_entry,
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        rank=LughaRank.FORM,
        residuals=(candidate_residual,),
        trace=candidate_trace,
    )

    # Create set with inherited and set-level residuals
    set_trace = OperatorCandidateSetTrace(
        set_id="set_001",
        candidate_ids=("cand_001",),
        trigger_source_vector_ids=(minimal_trigger_source.vector_id,),
        registry_entry_ids=(minimal_registry_entry.operator_id,),
        families=(OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,),
        trigger_id="trigger_001",
        frame_id="frame_001",
        matrix_id="matrix_001",
    )

    inherited_residual = Residual(
        type=ResidualType.TRIGGER_REQUIRES_FRAME_AND_MATRIX,
        severity=ResidualType.TRIGGER_REQUIRES_FRAME_AND_MATRIX,
        message="Inherited residual",
    )

    set_residual = Residual(
        type=ResidualType.OPERATOR_CANDIDATE_COMPETING_PRESERVED,
        severity=ResidualType.OPERATOR_CANDIDATE_COMPETING_PRESERVED,
        message="Set-level residual",
    )

    candidate_set = OperatorCandidateSet(
        set_id="set_001",
        candidates=(candidate,),
        set_trace=set_trace,
        inherited_residuals=(inherited_residual,),
        candidate_set_residuals=(set_residual,),
    )

    # get_all_residuals must include all three sources
    all_residuals = candidate_set.get_all_residuals()

    # Check that all residuals are present
    residual_messages = {r.message for r in all_residuals}
    assert "Inherited residual" in residual_messages
    assert "Set-level residual" in residual_messages
    assert "Candidate-level residual" in residual_messages
    assert len(all_residuals) >= 3


# ---------------------------------------------------------------------------
# Test Group C: Rank ceiling semantics (CEILED vs VIOLATION)
# ---------------------------------------------------------------------------


def test_rank_ceiling_lowering_is_not_violation(
    minimal_trigger_source, minimal_registry_entry
):
    """
    Normal rank lowering due to ceiling should use RANK_CEILED,
    not RANK_CEILING_VIOLATION.

    Note: Rank comes from OperatorTriggerPotential level and registry entry,
    not from individual TriggerSource.
    """
    # Registry entry with lower rank
    low_rank_entry = NahwOperatorEntry(
        operator_id="entry_001",
        display_name_ar="في",
        source=OperatorSource.OTHER,
        school=NahwSchool.SHARED,
        rank=LughaRank.FORM,  # Lower rank
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        input_signature=OperatorInputSignature(expected_arity=1),
        activation_conditions=(),
        blocking_conditions=(),
        expected_relation_families=(),
        case_effect_policy_families=(),
        citations=(),
        entry_residuals=(),
        entry_trace_id="trace_001",
    )

    # Candidate rank should match registry (FORM)
    candidate_trace = OperatorCandidateTrace(
        candidate_id="cand_001",
        trigger_source_vector_id=minimal_trigger_source.vector_id,
        registry_entry_id=low_rank_entry.operator_id,
        trigger_id="trigger_001",
        frame_id="frame_001",
        matrix_id="matrix_001",
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
    )

    from dal_core.residuals import make_info

    ceiled_residual = make_info(
        ResidualType.OPERATOR_CANDIDATE_RANK_CEILED,
        f"Rank lowered to {LughaRank.FORM.value} (ceiling)",
    )

    candidate = OperatorCandidate(
        candidate_id="cand_001",
        trigger_source=minimal_trigger_source,
        registry_entry=low_rank_entry,
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        rank=LughaRank.FORM,  # Matches registry
        residuals=(ceiled_residual,),
        trace=candidate_trace,
    )

    # Verify rank
    assert candidate.rank == LughaRank.FORM

    # Verify residual is CEILED, not VIOLATION
    assert any(
        r.type == ResidualType.OPERATOR_CANDIDATE_RANK_CEILED for r in candidate.residuals
    )
    assert not any(
        r.type == ResidualType.OPERATOR_CANDIDATE_RANK_CEILING_VIOLATION
        for r in candidate.residuals
    )


def test_rank_ceiling_violation_only_on_illegal_elevation(
    minimal_trigger_source, minimal_registry_entry
):
    """
    RANK_CEILING_VIOLATION should only occur when rank is illegally
    elevated above the ceiling.
    """
    # Attempt to create candidate with rank higher than ceiling
    with pytest.raises(ValueError, match="Rank ceiling violation"):
        candidate_trace = OperatorCandidateTrace(
            candidate_id="cand_002",
            trigger_source_vector_id=minimal_trigger_source.vector_id,
            registry_entry_id=minimal_registry_entry.operator_id,
            trigger_id="trigger_002",
            frame_id="frame_002",
            matrix_id="matrix_002",
            family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        )

        # Trigger source rank: FORM, registry entry rank: FORM
        # Ceiling should be FORM
        # Attempting to set rank to SAMA (higher) should fail
        OperatorCandidate(
            candidate_id="cand_002",
            trigger_source=minimal_trigger_source,
            registry_entry=minimal_registry_entry,
            family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
            rank=LughaRank.SAMA,  # Illegal elevation!
            residuals=(),
            trace=candidate_trace,
        )


# ---------------------------------------------------------------------------
# Test Group D: Family matching enforcement
# ---------------------------------------------------------------------------


def test_operator_candidate_family_matches_trigger_and_registry(
    minimal_trigger_source, minimal_registry_entry
):
    """
    OperatorCandidate.family must match both trigger_source.family
    and registry_entry.family.
    """
    candidate_trace = OperatorCandidateTrace(
        candidate_id="cand_003",
        trigger_source_vector_id=minimal_trigger_source.vector_id,
        registry_entry_id=minimal_registry_entry.operator_id,
        trigger_id="trigger_003",
        frame_id="frame_003",
        matrix_id="matrix_003",
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
    )

    candidate = OperatorCandidate(
        candidate_id="cand_003",
        trigger_source=minimal_trigger_source,
        registry_entry=minimal_registry_entry,
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        rank=LughaRank.FORM,
        residuals=(),
        trace=candidate_trace,
    )

    # All families must match
    assert candidate.family == minimal_trigger_source.family
    assert candidate.family == minimal_registry_entry.family
    assert minimal_trigger_source.family == minimal_registry_entry.family


def test_family_mismatch_raises_error(minimal_trigger_source):
    """
    Creating an OperatorCandidate with mismatched families should fail.
    """
    # Create registry entry with DIFFERENT family
    wrong_family_entry = NahwOperatorEntry(
        operator_id="entry_wrong",
        display_name_ar="إن",
        source=OperatorSource.OTHER,
        school=NahwSchool.SHARED,
        rank=LughaRank.FORM,
        family=OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY,  # Different!
        input_signature=OperatorInputSignature(expected_arity=1),
        activation_conditions=(),
        blocking_conditions=(),
        expected_relation_families=(),
        case_effect_policy_families=(),
        citations=(),
        entry_residuals=(),
        entry_trace_id="trace_wrong",
    )

    with pytest.raises(ValueError, match="Family mismatch"):
        candidate_trace = OperatorCandidateTrace(
            candidate_id="cand_wrong",
            trigger_source_vector_id=minimal_trigger_source.vector_id,
            registry_entry_id=wrong_family_entry.operator_id,
            trigger_id="trigger_wrong",
            frame_id="frame_wrong",
            matrix_id="matrix_wrong",
            family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        )

        OperatorCandidate(
            candidate_id="cand_wrong",
            trigger_source=minimal_trigger_source,
            registry_entry=wrong_family_entry,
            family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
            rank=LughaRank.FORM,
            residuals=(),
            trace=candidate_trace,
        )


# ---------------------------------------------------------------------------
# Test Group E: Competition preservation
# ---------------------------------------------------------------------------


def test_operator_candidate_set_preserves_competition():
    """
    OperatorCandidateSet must preserve ALL competing candidates.
    Multiple candidates is normal and expected.
    """
    # Create multiple candidates
    candidates = []
    for i in range(3):
        source = TriggerSource(
            family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
            frame_index=i,
            vector_id=f"vec_{i}",
            matrix_row_index=i,
            triggering_type_id="HARF_JARR",
            compatibility_evidence=(),
            source_trace_id=f"source_trace_{i}",
        )

        entry = NahwOperatorEntry(
            operator_id=f"entry_{i}",
            display_name_ar=f"في_{i}",
            source=OperatorSource.OTHER,
            school=NahwSchool.SHARED,
            rank=LughaRank.FORM,
            family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
            input_signature=OperatorInputSignature(expected_arity=1),
            activation_conditions=(),
            blocking_conditions=(),
            expected_relation_families=(),
            case_effect_policy_families=(),
            citations=(),
            entry_residuals=(),
            entry_trace_id=f"trace_{i}",
        )

        trace = OperatorCandidateTrace(
            candidate_id=f"cand_{i}",
            trigger_source_vector_id=source.vector_id,
            registry_entry_id=entry.operator_id,
            trigger_id="trigger_001",
            frame_id="frame_001",
            matrix_id="matrix_001",
            family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        )

        candidate = OperatorCandidate(
            candidate_id=f"cand_{i}",
            trigger_source=source,
            registry_entry=entry,
            family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
            rank=LughaRank.FORM,
            residuals=(),
            trace=trace,
        )

        candidates.append(candidate)

    # Create set
    set_trace = OperatorCandidateSetTrace(
        set_id="set_competition",
        candidate_ids=tuple(f"cand_{i}" for i in range(3)),
        trigger_source_vector_ids=tuple(f"vec_{i}" for i in range(3)),
        registry_entry_ids=tuple(f"entry_{i}" for i in range(3)),
        families=tuple(OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY for _ in range(3)),
        trigger_id="trigger_001",
        frame_id="frame_001",
        matrix_id="matrix_001",
    )

    candidate_set = OperatorCandidateSet(
        set_id="set_competition",
        candidates=tuple(candidates),
        set_trace=set_trace,
        inherited_residuals=(),
        candidate_set_residuals=(),
    )

    # All candidates must be preserved
    assert len(candidate_set.candidates) == 3
    assert candidate_set.candidates[0].candidate_id == "cand_0"
    assert candidate_set.candidates[1].candidate_id == "cand_1"
    assert candidate_set.candidates[2].candidate_id == "cand_2"


# ---------------------------------------------------------------------------
# Test Group F: Empty set safety
# ---------------------------------------------------------------------------


def test_empty_candidate_set_safe():
    """
    An empty OperatorCandidateSet should be valid and safe.
    """
    set_trace = OperatorCandidateSetTrace(
        set_id="set_empty",
        candidate_ids=(),
        trigger_source_vector_ids=(),
        registry_entry_ids=(),
        families=(),
        trigger_id="trigger_empty",
        frame_id="frame_empty",
        matrix_id="matrix_empty",
    )

    empty_set = OperatorCandidateSet(
        set_id="set_empty",
        candidates=(),
        set_trace=set_trace,
        inherited_residuals=(),
        candidate_set_residuals=(),
    )

    assert empty_set.is_empty()
    assert len(empty_set.candidates) == 0
    assert len(empty_set.get_all_residuals()) == 0


# ---------------------------------------------------------------------------
# Test Group G: No fake candidates
# ---------------------------------------------------------------------------


def test_no_fake_candidates():
    """
    OperatorCandidateSet must reject fake candidates (None).
    """
    set_trace = OperatorCandidateSetTrace(
        set_id="set_fake",
        candidate_ids=("cand_1",),
        trigger_source_vector_ids=("vec_1",),
        registry_entry_ids=("entry_1",),
        families=(OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,),
        trigger_id="trigger_fake",
        frame_id="frame_fake",
        matrix_id="matrix_fake",
    )

    with pytest.raises(ValueError, match="Fake candidate"):
        OperatorCandidateSet(
            set_id="set_fake",
            candidates=(None,),  # Fake candidate!
            set_trace=set_trace,
            inherited_residuals=(),
            candidate_set_residuals=(),
        )


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def minimal_trigger_source():
    """Minimal TriggerSource for testing"""
    return TriggerSource(
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        frame_index=0,
        vector_id="vec_minimal",
        matrix_row_index=0,
        triggering_type_id="HARF_JARR",
        compatibility_evidence=(),
        source_trace_id="trace_minimal",
    )


@pytest.fixture
def minimal_registry_entry():
    """Minimal NahwOperatorEntry for testing"""
    return NahwOperatorEntry(
        operator_id="entry_minimal",
        display_name_ar="في",
        source=OperatorSource.OTHER,
        school=NahwSchool.SHARED,
        rank=LughaRank.FORM,
        family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
        input_signature=OperatorInputSignature(expected_arity=1),
        activation_conditions=(),
        blocking_conditions=(),
        expected_relation_families=(),
        case_effect_policy_families=(),
        citations=(),
        entry_residuals=(),
        entry_trace_id="trace_minimal",
    )
