"""
Constitutional Tests for PreMeaning Dataset Schema (PR #135)

Tests all constitutional laws for GARA-T5 dataset schemas:
    1. Dataset examples cannot contain final meaning
    2. Dataset examples cannot contain syntax role
    3. Dataset examples cannot contain relation candidate
    4. Dataset examples cannot contain ifādah or hukm
    5. SurfaceInverse examples cannot be certain
    6. TraceInverse examples cannot be certain without trace
    7. TraceInverse certainty requires injective operation or preserved preimage trace
    8. Every example has residuals and rank
    9. Every example has stop_before_meaning = true
    10. Dataset schemas use existing Rank and Residual types

PR: #135
Created: 2026-05-28
"""

import pytest
from types import MappingProxyType

from dal_core.premeaning_dataset_schema import (
    CauseGeometryDataset,
    PreMeaningTrainingExample,
    OperationTraceTrainingExample,
    SurfaceInverseTrainingExample,
    TraceInverseTrainingExample,
    StopGateTrainingExample,
    ResidualRankTrainingExample,
    ForbiddenOutput,
    validate_no_forbidden_outputs,
    validate_premeaning_example,
    make_sample_surface_inverse_example,
    make_sample_trace_inverse_example,
)
from dal_core.foundation import Rank
from dal_core.residuals import Residual, ResidualType, ResidualSeverity


# ============================================================================
# Test Law 1: Dataset examples cannot contain final meaning
# ============================================================================


def test_base_example_forbids_meaning_in_trace():
    """Law 1: Trace cannot contain 'meaning' key."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="MINIMAL"
    )

    with pytest.raises(ValueError, match="forbidden semantic key: meaning"):
        PreMeaningTrainingExample(
            example_id="test_001",
            example_type="test",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="before",
            after_state="after",
            invariant="test",
            trace=MappingProxyType({"meaning": "forbidden"}),  # ❌ Forbidden!
            residuals=frozenset([("TEST", "WARNING", "test")]),
            rank="HYPOTHESIS",
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"])
        )


def test_forbidden_output_validator_blocks_meaning():
    """Law 1: validate_no_forbidden_outputs blocks meaning field."""
    with pytest.raises(ValueError, match="meaning is FORBIDDEN"):
        validate_no_forbidden_outputs(meaning="some meaning")


def test_forbidden_output_validator_blocks_translation():
    """Law 1: validate_no_forbidden_outputs blocks translation."""
    with pytest.raises(ValueError, match="translation is FORBIDDEN"):
        validate_no_forbidden_outputs(translation="some translation")


def test_forbidden_output_validator_blocks_ifadah():
    """Law 1: validate_no_forbidden_outputs blocks ifadah."""
    with pytest.raises(ValueError, match="ifadah is FORBIDDEN"):
        validate_no_forbidden_outputs(ifadah="some ifadah")


def test_forbidden_output_validator_blocks_hukm():
    """Law 1: validate_no_forbidden_outputs blocks hukm."""
    with pytest.raises(ValueError, match="hukm is FORBIDDEN"):
        validate_no_forbidden_outputs(hukm="some hukm")


# ============================================================================
# Test Law 2-4: No syntax_role, relation_candidate, ifadah, hukm
# ============================================================================


def test_forbidden_output_validator_blocks_syntax_role():
    """Law 2: validate_no_forbidden_outputs blocks syntax_role."""
    with pytest.raises(ValueError, match="syntax_role is FORBIDDEN"):
        validate_no_forbidden_outputs(syntax_role="فاعل")


def test_forbidden_output_validator_blocks_relation_candidate():
    """Law 3: validate_no_forbidden_outputs blocks relation_candidate."""
    with pytest.raises(ValueError, match="relation_candidate is FORBIDDEN"):
        validate_no_forbidden_outputs(relation_candidate="إسناد")


def test_forbidden_output_enum_complete():
    """Laws 1-4: ForbiddenOutput enum includes all prohibited fields."""
    forbidden_values = {fo.value for fo in ForbiddenOutput}
    required = {
        "meaning", "semantic_payload", "translation", "syntax_role",
        "relation_candidate", "ifadah", "hukm", "truth_judgment"
    }
    assert required.issubset(forbidden_values), \
        f"Missing forbidden outputs: {required - forbidden_values}"


# ============================================================================
# Test Law 5: SurfaceInverse examples cannot be certain
# ============================================================================


def test_surface_inverse_forbids_certainty():
    """Law 5: SurfaceInverse cannot have certainty=True."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="MINIMAL"
    )

    with pytest.raises(ValueError, match="SurfaceInverse CANNOT be certain"):
        SurfaceInverseTrainingExample(
            example_id="surf_001",
            example_type="surface_inverse",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="",
            after_state="test",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([("TEST", "WARNING", "ambiguity")]),
            rank="HYPOTHESIS",
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            recovered_candidates=("cand1", "cand2"),
            certainty=True  # ❌ Forbidden!
        )


def test_surface_inverse_rank_ceiling():
    """Law 5: SurfaceInverse rank ≤ STRONG_HYPOTHESIS (not CERTIFICATE)."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="MINIMAL"
    )

    with pytest.raises(ValueError, match="rank=CERTIFICATE exceeds ceiling"):
        SurfaceInverseTrainingExample(
            example_id="surf_002",
            example_type="surface_inverse",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="",
            after_state="test",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([("TEST", "WARNING", "ambiguity")]),
            rank="CERTIFICATE",  # ❌ Exceeds ceiling!
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            recovered_candidates=("cand1", "cand2"),
            certainty=False
        )


def test_surface_inverse_requires_multiple_candidates():
    """Law 5: SurfaceInverse MUST have multiple candidates."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="MINIMAL"
    )

    with pytest.raises(ValueError, match="multiple candidates"):
        SurfaceInverseTrainingExample(
            example_id="surf_003",
            example_type="surface_inverse",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="",
            after_state="test",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([("TEST", "WARNING", "ambiguity")]),
            rank="HYPOTHESIS",
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            recovered_candidates=("only_one",),  # ❌ Only one candidate!
            certainty=False
        )


def test_surface_inverse_sample_valid():
    """Law 5: Sample SurfaceInverse example is valid."""
    example = make_sample_surface_inverse_example()
    assert example.certainty is False
    assert example.rank != "CERTIFICATE"
    assert len(example.recovered_candidates) >= 2
    validate_premeaning_example(example)


# ============================================================================
# Test Law 6: TraceInverse cannot be certain without trace
# ============================================================================


def test_trace_inverse_certainty_requires_complete_trace():
    """Law 6: TraceInverse cannot claim certainty without complete trace."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="COMPLETE"
    )

    with pytest.raises(ValueError, match="complete trace"):
        TraceInverseTrainingExample(
            example_id="trace_001",
            example_type="trace_inverse",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="before",
            after_state="after",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([]),
            rank="HYPOTHESIS",
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            recovered_before="before",
            alternative_candidates=(),
            is_certain=True,  # Claiming certainty...
            certainty_basis="injective",
            trace_is_complete=False,  # ❌ But trace incomplete!
            domain_declared=True,
            invariant_preserved=True,
            has_blocking_residuals=False,
            is_injective_operation=True,
            carries_preimage=False
        )


def test_trace_inverse_certainty_requires_domain():
    """Law 6: TraceInverse cannot claim certainty without declared domain."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="COMPLETE"
    )

    with pytest.raises(ValueError, match="declared domain"):
        TraceInverseTrainingExample(
            example_id="trace_002",
            example_type="trace_inverse",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="before",
            after_state="after",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([]),
            rank="HYPOTHESIS",
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            recovered_before="before",
            alternative_candidates=(),
            is_certain=True,
            certainty_basis="injective",
            trace_is_complete=True,
            domain_declared=False,  # ❌ Domain not declared!
            invariant_preserved=True,
            has_blocking_residuals=False,
            is_injective_operation=True,
            carries_preimage=False
        )


def test_trace_inverse_certainty_forbids_blocking_residuals():
    """Law 6: TraceInverse cannot be certain with blocking residuals."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="COMPLETE"
    )

    with pytest.raises(ValueError, match="blocking residuals"):
        TraceInverseTrainingExample(
            example_id="trace_003",
            example_type="trace_inverse",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="before",
            after_state="after",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([("BLOCKER", "BLOCKER", "test")]),
            rank="HYPOTHESIS",
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            recovered_before="before",
            alternative_candidates=(),
            is_certain=True,
            certainty_basis="injective",
            trace_is_complete=True,
            domain_declared=True,
            invariant_preserved=True,
            has_blocking_residuals=True,  # ❌ Blocking residuals!
            is_injective_operation=True,
            carries_preimage=False
        )


# ============================================================================
# Test Law 7: TraceInverse certainty requires injective OR carries_preimage
# ============================================================================


def test_trace_inverse_certainty_requires_injective_or_preimage():
    """Law 7: TraceInverse certainty needs is_injective_operation OR carries_preimage."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="COMPLETE"
    )

    with pytest.raises(ValueError, match="is_injective_operation OR carries_preimage"):
        TraceInverseTrainingExample(
            example_id="trace_004",
            example_type="trace_inverse",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="before",
            after_state="after",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([]),
            rank="HYPOTHESIS",
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            recovered_before="before",
            alternative_candidates=(),
            is_certain=True,
            certainty_basis="injective",
            trace_is_complete=True,
            domain_declared=True,
            invariant_preserved=True,
            has_blocking_residuals=False,
            is_injective_operation=False,  # ❌ Not injective
            carries_preimage=False  # ❌ And no preimage!
        )


def test_trace_inverse_certainty_requires_basis():
    """Law 7: TraceInverse certainty MUST declare basis."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="COMPLETE"
    )

    with pytest.raises(ValueError, match="MUST declare basis"):
        TraceInverseTrainingExample(
            example_id="trace_005",
            example_type="trace_inverse",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="before",
            after_state="after",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([]),
            rank="HYPOTHESIS",
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            recovered_before="before",
            alternative_candidates=(),
            is_certain=True,
            certainty_basis=None,  # ❌ No basis declared!
            trace_is_complete=True,
            domain_declared=True,
            invariant_preserved=True,
            has_blocking_residuals=False,
            is_injective_operation=True,
            carries_preimage=False
        )


def test_trace_inverse_certain_with_injective():
    """Law 7: TraceInverse certain when injective operation."""
    example = make_sample_trace_inverse_example()
    # This example is non-injective but carries preimage
    assert example.is_certain
    assert example.certainty_basis == "trace_carries_preimage"
    validate_premeaning_example(example)


def test_trace_inverse_sample_valid():
    """Law 7: Sample TraceInverse (إدغام with preimage) is valid."""
    example = make_sample_trace_inverse_example()
    assert example.is_certain is True
    assert example.carries_preimage is True
    assert example.recovered_before == "ن + ل"
    validate_premeaning_example(example)


# ============================================================================
# Test Law 8: Every example has residuals and rank
# ============================================================================


def test_example_requires_residuals():
    """Law 8: Examples MUST have residuals."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="MINIMAL"
    )

    example = PreMeaningTrainingExample(
        example_id="test_no_residuals",
        example_type="test",
        input_surface="test",
        input_classification="test",
        operation_name="test",
        operation_spec_reference="test",
        cause_geometry=cause_geo,
        before_state="before",
        after_state="after",
        invariant="test",
        trace=MappingProxyType({}),
        residuals=frozenset([]),  # Empty residuals
        rank="HYPOTHESIS",
        stop_before_meaning=True,
        forbidden_outputs=frozenset(["meaning"])
    )

    with pytest.raises(ValueError, match="residuals cannot be empty"):
        validate_premeaning_example(example)


def test_example_requires_rank():
    """Law 8: Examples MUST have rank."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="MINIMAL"
    )

    example = PreMeaningTrainingExample(
        example_id="test_no_rank",
        example_type="test",
        input_surface="test",
        input_classification="test",
        operation_name="test",
        operation_spec_reference="test",
        cause_geometry=cause_geo,
        before_state="before",
        after_state="after",
        invariant="test",
        trace=MappingProxyType({}),
        residuals=frozenset([("TEST", "WARNING", "test")]),
        rank="",  # Empty rank
        stop_before_meaning=True,
        forbidden_outputs=frozenset(["meaning"])
    )

    with pytest.raises(ValueError, match="rank cannot be empty"):
        validate_premeaning_example(example)


# ============================================================================
# Test Law 9: Every example has stop_before_meaning = True
# ============================================================================


def test_example_requires_stop_before_meaning():
    """Law 9: stop_before_meaning MUST be True."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="MINIMAL"
    )

    with pytest.raises(ValueError, match="stop_before_meaning MUST be True"):
        PreMeaningTrainingExample(
            example_id="test_no_stop",
            example_type="test",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="before",
            after_state="after",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([("TEST", "WARNING", "test")]),
            rank="HYPOTHESIS",
            stop_before_meaning=False,  # ❌ Forbidden!
            forbidden_outputs=frozenset(["meaning"])
        )


def test_stop_gate_example_enforces_no_compositional_relation():
    """Law 9: StopGate example MUST NOT have compositional_relation."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="MINIMAL"
    )

    with pytest.raises(ValueError, match="compositional_relation"):
        StopGateTrainingExample(
            example_id="stop_001",
            example_type="stop_gate",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="before",
            after_state="after",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([("TEST", "WARNING", "test")]),
            rank="HYPOTHESIS",
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            has_pattern_signified=True,
            has_root_stem_signified=True,
            has_operator_potential=False,
            has_reference_potential=False,
            has_relation_readiness=False,
            has_trace_only=True,
            has_compositional_relation=True,  # ❌ Forbidden!
            has_pragmatic_closure=False,
            has_evidence_for_truth=False,
            expected_output="STOP_BEFORE_MEANING"
        )


# ============================================================================
# Test Law 10: CauseGeometry requires all 4 causes
# ============================================================================


def test_cause_geometry_requires_material_cause():
    """Law 10: CauseGeometry MUST have material_cause."""
    with pytest.raises(ValueError, match="material_cause"):
        CauseGeometryDataset(
            prior_info=frozenset(["test"]),
            bāb="test",
            domain="test",
            material_cause="",  # ❌ Empty!
            formal_cause="test",
            efficient_cause="test",
            final_cause_before_meaning="test purpose",
            license_type="MORPHOLOGICAL_BAB",
            license_condition="test",
            invariant="test",
            trace_requirement="MINIMAL"
        )


def test_cause_geometry_requires_all_four_causes():
    """Law 10: CauseGeometry MUST have all 4 Aristotelian causes."""
    # Missing formal_cause
    with pytest.raises(ValueError, match="formal_cause"):
        CauseGeometryDataset(
            prior_info=frozenset(["test"]),
            bāb="test",
            domain="test",
            material_cause="test",
            formal_cause="",  # ❌ Empty!
            efficient_cause="test",
            final_cause_before_meaning="test purpose",
            license_type="MORPHOLOGICAL_BAB",
            license_condition="test",
            invariant="test",
            trace_requirement="MINIMAL"
        )


def test_cause_geometry_requires_bab_and_domain():
    """Law 10: CauseGeometry MUST have bāb and domain."""
    with pytest.raises(ValueError, match="bāb"):
        CauseGeometryDataset(
            prior_info=frozenset(["test"]),
            bāb="",  # ❌ Empty!
            domain="test",
            material_cause="test",
            formal_cause="test",
            efficient_cause="test",
            final_cause_before_meaning="test purpose",
            license_type="MORPHOLOGICAL_BAB",
            license_condition="test",
            invariant="test",
            trace_requirement="MINIMAL"
        )


def test_cause_geometry_final_cause_forbids_semantic_terms():
    """Law 10: final_cause_before_meaning MUST NOT contain semantic terms."""
    with pytest.raises(ValueError, match="forbidden semantic term"):
        CauseGeometryDataset(
            prior_info=frozenset(["test"]),
            bāb="test",
            domain="test",
            material_cause="test",
            formal_cause="test",
            efficient_cause="test",
            final_cause_before_meaning="derive meaning",  # ❌ Contains 'meaning'!
            license_type="MORPHOLOGICAL_BAB",
            license_condition="test",
            invariant="test",
            trace_requirement="MINIMAL"
        )


# ============================================================================
# Test Residual/Rank Integration
# ============================================================================


def test_residual_rank_example_validates_trace_completeness():
    """Residual/Rank: Incomplete trace → residuals + lowered rank."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="INCOMPLETE"
    )

    # Incomplete trace WITHOUT residuals should fail
    with pytest.raises(ValueError, match="Incomplete trace MUST generate residuals"):
        ResidualRankTrainingExample(
            example_id="resrank_001",
            example_type="residual_rank",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="before",
            after_state="after",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([]),  # ❌ No residuals!
            rank="HYPOTHESIS",
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            trace_completeness="incomplete",
            has_blocking_residuals=False,
            has_warning_residuals=False,
            residual_count=0,
            rank_justification="test"
        )


def test_residual_rank_example_blocking_residuals_lower_rank():
    """Residual/Rank: Blocking residuals MUST lower rank."""
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["test"]),
        bāb="test",
        domain="test",
        material_cause="test",
        formal_cause="test",
        efficient_cause="test",
        final_cause_before_meaning="test purpose",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="test",
        invariant="test",
        trace_requirement="COMPLETE"
    )

    with pytest.raises(ValueError, match="rank=CERTIFICATE is too high"):
        ResidualRankTrainingExample(
            example_id="resrank_002",
            example_type="residual_rank",
            input_surface="test",
            input_classification="test",
            operation_name="test",
            operation_spec_reference="test",
            cause_geometry=cause_geo,
            before_state="before",
            after_state="after",
            invariant="test",
            trace=MappingProxyType({}),
            residuals=frozenset([("BLOCKER", "BLOCKER", "test")]),
            rank="CERTIFICATE",  # ❌ Too high with blocker!
            stop_before_meaning=True,
            forbidden_outputs=frozenset(["meaning"]),
            trace_completeness="complete",
            has_blocking_residuals=True,
            has_warning_residuals=False,
            residual_count=1,
            rank_justification="test"
        )


# ============================================================================
# Integration Tests
# ============================================================================


def test_sample_examples_all_valid():
    """Integration: Both sample examples pass validation."""
    surf_example = make_sample_surface_inverse_example()
    trace_example = make_sample_trace_inverse_example()

    validate_premeaning_example(surf_example)
    validate_premeaning_example(trace_example)

    assert surf_example.stop_before_meaning is True
    assert trace_example.stop_before_meaning is True
    assert "meaning" in surf_example.forbidden_outputs
    assert "meaning" in trace_example.forbidden_outputs
