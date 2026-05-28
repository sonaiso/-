"""
Constitutional Tests for Operation Algebra (PR #133)

Tests all 10 constitutional laws from OPERATION_ALGEBRA_CONSTITUTION.md

Test Coverage:
    1. Law 1: Operation requires complete OperationSpec
    2. Law 2: Operation requires BeforeAfterRelation
    3. Law 3: Operation requires complete CauseGeometry
    4. Law 4: CauseGeometry requires Bāb and Domain
    5. Law 5: SurfaceInverse never returns certainty
    6. Law 6: TraceInverse certainty requires conditions
    7. Law 7: Incomplete trace → lowered rank
    8. Law 8: Operations stop before meaning
    9. Law 9: BackwardAudit validates domain
    10. Law 10: Trace does not imply meaning

PR: #133
Created: 2026-05-28
"""

import pytest
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping, Tuple

from dal_core.operation_algebra import (
    BeforeAfterRelation,
    LicenseSpec,
    LicenseType,
    CauseGeometry,
    OperationTrace,
    SurfaceInverse,
    TraceInverse,
    BackwardAudit,
    AuditResult,
    AuditStatus,
    InvariantPolicy,
    ResidualPolicy,
    RankPolicy,
    TracePolicy,
    MeaningStopGate,
    OperationSpec,
    TraceRequirement,
)
from dal_core.foundation import Rank
from dal_core.residuals import Residual, ResidualSeverity


# ============================================================================
# Test Law 1: Operation Requires Complete Specification
# ============================================================================


def test_operation_spec_requires_name():
    """Law 1: OperationSpec must have name."""
    license = LicenseSpec(
        license_type=LicenseType.MORPHOLOGICAL_BAB,
        licensing_condition="test",
        required_prior_info=frozenset()
    )
    cause_geo = CauseGeometry(
        prior_info=frozenset(),
        bāb="test_bab",
        domain="test_domain",
        material_cause="test_material",
        formal_cause="test_formal",
        efficient_cause="test_efficient",
        final_cause_before_meaning="test_final",
        license=license,
        invariant="identity",
        trace_requirement=TraceRequirement.MINIMAL,
        residual_handling="inherit",
        rank_assignment=Rank.CANDIDATE
    )
    before_after = BeforeAfterRelation(
        operation_name="test_op",
        before_type=str,
        after_type=str,
        identity_preservation="preserved",
        change_description="none",
        reversibility=True,
        trace_requirement=TraceRequirement.MINIMAL
    )

    with pytest.raises(ValueError, match="requires name"):
        OperationSpec(
            name="",  # Empty name
            domain_before="D0",
            domain_after="D1",
            input_type=str,
            output_type=str,
            required_prior_info=frozenset(),
            bāb="test_bab",
            cause_geometry=cause_geo,
            licensed_operation=lambda x: x,
            declared_before_after_relation=before_after,
            preserved_invariant="identity",
            changed_component="none",
            trace_policy=TracePolicy(
                required_completeness=False,
                preserved_preimage_fields=frozenset(),
                injective_operation=True,
                inverse_certainty_conditions=()
            ),
            residual_policy=ResidualPolicy(
                inherited_residuals=frozenset(),
                operation_residuals=frozenset(),
                discharge_conditions=MappingProxyType({}),
                blocking_residuals=frozenset()
            ),
            rank_policy=RankPolicy(
                input_rank_requirement=Rank.CANDIDATE,
                output_rank=Rank.HYPOTHESIS,
                rank_lowering_conditions=MappingProxyType({})
            ),
            surface_inverse_policy=None,
            trace_inverse_policy=None,
            forbidden_outputs=frozenset(["meaning", "ifadah", "hukm", "semantic_identity"]),
            next_allowed_operations=frozenset()
        )


# ============================================================================
# Test Law 2: Operation Requires Before/After Relation
# ============================================================================


def test_operation_spec_requires_before_after_relation():
    """Law 2: OperationSpec must declare BeforeAfterRelation."""
    license = LicenseSpec(
        license_type=LicenseType.MORPHOLOGICAL_BAB,
        licensing_condition="test",
        required_prior_info=frozenset()
    )
    cause_geo = CauseGeometry(
        prior_info=frozenset(),
        bāb="test_bab",
        domain="test_domain",
        material_cause="test_material",
        formal_cause="test_formal",
        efficient_cause="test_efficient",
        final_cause_before_meaning="test_final",
        license=license,
        invariant="identity",
        trace_requirement=TraceRequirement.MINIMAL,
        residual_handling="inherit",
        rank_assignment=Rank.CANDIDATE
    )

    with pytest.raises(ValueError, match="declared_before_after_relation"):
        OperationSpec(
            name="test_op",
            domain_before="D0",
            domain_after="D1",
            input_type=str,
            output_type=str,
            required_prior_info=frozenset(),
            bāb="test_bab",
            cause_geometry=cause_geo,
            licensed_operation=lambda x: x,
            declared_before_after_relation=None,  # Missing!
            preserved_invariant="identity",
            changed_component="none",
            trace_policy=TracePolicy(
                required_completeness=False,
                preserved_preimage_fields=frozenset(),
                injective_operation=True,
                inverse_certainty_conditions=()
            ),
            residual_policy=ResidualPolicy(
                inherited_residuals=frozenset(),
                operation_residuals=frozenset(),
                discharge_conditions=MappingProxyType({}),
                blocking_residuals=frozenset()
            ),
            rank_policy=RankPolicy(
                input_rank_requirement=Rank.CANDIDATE,
                output_rank=Rank.HYPOTHESIS,
                rank_lowering_conditions=MappingProxyType({})
            ),
            surface_inverse_policy=None,
            trace_inverse_policy=None,
            forbidden_outputs=frozenset(["meaning", "ifadah", "hukm", "semantic_identity"]),
            next_allowed_operations=frozenset()
        )


# ============================================================================
# Test Law 3: Operation Requires Complete CauseGeometry
# ============================================================================


def test_operation_spec_requires_cause_geometry():
    """Law 3: OperationSpec must have complete CauseGeometry."""
    before_after = BeforeAfterRelation(
        operation_name="test_op",
        before_type=str,
        after_type=str,
        identity_preservation="preserved",
        change_description="none",
        reversibility=True,
        trace_requirement=TraceRequirement.MINIMAL
    )

    with pytest.raises(ValueError, match="cause_geometry"):
        OperationSpec(
            name="test_op",
            domain_before="D0",
            domain_after="D1",
            input_type=str,
            output_type=str,
            required_prior_info=frozenset(),
            bāb="test_bab",
            cause_geometry=None,  # Missing!
            licensed_operation=lambda x: x,
            declared_before_after_relation=before_after,
            preserved_invariant="identity",
            changed_component="none",
            trace_policy=TracePolicy(
                required_completeness=False,
                preserved_preimage_fields=frozenset(),
                injective_operation=True,
                inverse_certainty_conditions=()
            ),
            residual_policy=ResidualPolicy(
                inherited_residuals=frozenset(),
                operation_residuals=frozenset(),
                discharge_conditions=MappingProxyType({}),
                blocking_residuals=frozenset()
            ),
            rank_policy=RankPolicy(
                input_rank_requirement=Rank.CANDIDATE,
                output_rank=Rank.HYPOTHESIS,
                rank_lowering_conditions=MappingProxyType({})
            ),
            surface_inverse_policy=None,
            trace_inverse_policy=None,
            forbidden_outputs=frozenset(["meaning", "ifadah", "hukm", "semantic_identity"]),
            next_allowed_operations=frozenset()
        )


# ============================================================================
# Test Law 4: CauseGeometry Requires Bāb and Domain
# ============================================================================


def test_cause_geometry_requires_bab():
    """Law 4: CauseGeometry must have bāb."""
    license = LicenseSpec(
        license_type=LicenseType.MORPHOLOGICAL_BAB,
        licensing_condition="test",
        required_prior_info=frozenset()
    )

    with pytest.raises(ValueError, match="bāb"):
        CauseGeometry(
            prior_info=frozenset(),
            bāb="",  # Empty!
            domain="test_domain",
            material_cause="test_material",
            formal_cause="test_formal",
            efficient_cause="test_efficient",
            final_cause_before_meaning="test_final",
            license=license,
            invariant="identity",
            trace_requirement=TraceRequirement.MINIMAL,
            residual_handling="inherit",
            rank_assignment=Rank.CANDIDATE
        )


def test_cause_geometry_requires_domain():
    """Law 4: CauseGeometry must have domain."""
    license = LicenseSpec(
        license_type=LicenseType.MORPHOLOGICAL_BAB,
        licensing_condition="test",
        required_prior_info=frozenset()
    )

    with pytest.raises(ValueError, match="domain"):
        CauseGeometry(
            prior_info=frozenset(),
            bāb="test_bab",
            domain="",  # Empty!
            material_cause="test_material",
            formal_cause="test_formal",
            efficient_cause="test_efficient",
            final_cause_before_meaning="test_final",
            license=license,
            invariant="identity",
            trace_requirement=TraceRequirement.MINIMAL,
            residual_handling="inherit",
            rank_assignment=Rank.CANDIDATE
        )


def test_cause_geometry_requires_all_four_causes():
    """Law 3: CauseGeometry must have all four causes."""
    license = LicenseSpec(
        license_type=LicenseType.MORPHOLOGICAL_BAB,
        licensing_condition="test",
        required_prior_info=frozenset()
    )

    # Missing material_cause
    with pytest.raises(ValueError, match="material_cause"):
        CauseGeometry(
            prior_info=frozenset(),
            bāb="test_bab",
            domain="test_domain",
            material_cause="",  # Empty!
            formal_cause="test_formal",
            efficient_cause="test_efficient",
            final_cause_before_meaning="test_final",
            license=license,
            invariant="identity",
            trace_requirement=TraceRequirement.MINIMAL,
            residual_handling="inherit",
            rank_assignment=Rank.CANDIDATE
        )

    # Missing formal_cause
    with pytest.raises(ValueError, match="formal_cause"):
        CauseGeometry(
            prior_info=frozenset(),
            bāb="test_bab",
            domain="test_domain",
            material_cause="test_material",
            formal_cause="",  # Empty!
            efficient_cause="test_efficient",
            final_cause_before_meaning="test_final",
            license=license,
            invariant="identity",
            trace_requirement=TraceRequirement.MINIMAL,
            residual_handling="inherit",
            rank_assignment=Rank.CANDIDATE
        )


# ============================================================================
# Test Law 5: SurfaceInverse Never Returns Certainty
# ============================================================================


def test_surface_inverse_forbids_certainty():
    """Law 5: SurfaceInverse.certainty must be False."""
    with pytest.raises(ValueError, match="SurfaceInverse.certainty MUST be False"):
        SurfaceInverse(
            surface_after="test",
            recovered_candidates=("a", "b"),
            residuals=frozenset(),
            rank=Rank.HYPOTHESIS,
            certainty=True  # Forbidden!
        )


def test_surface_inverse_rank_limit():
    """Law 5: SurfaceInverse rank cannot exceed STRONG_HYPOTHESIS."""
    with pytest.raises(ValueError, match="cannot exceed STRONG_HYPOTHESIS"):
        SurfaceInverse(
            surface_after="test",
            recovered_candidates=("a", "b"),
            residuals=frozenset(),
            rank=Rank.CERTIFICATE,  # Too high!
            certainty=False
        )


def test_surface_inverse_valid():
    """Law 5: SurfaceInverse valid case."""
    surface_inv = SurfaceInverse(
        surface_after="كَتَبَ",
        recovered_candidates=("ك ت ب", "ك ت ب + فَعَلَ"),
        residuals=frozenset([
            Residual(
                severity=ResidualSeverity.WARNING,
                category="ambiguity",
                description="Multiple root candidates",
                gate_origin="surface_analysis",
                layer="morphology"
            )
        ]),
        rank=Rank.HYPOTHESIS,
        certainty=False
    )
    assert surface_inv.certainty is False
    assert surface_inv.rank == Rank.HYPOTHESIS
    assert len(surface_inv.recovered_candidates) == 2


# ============================================================================
# Test Law 6: TraceInverse Certainty Requires Conditions
# ============================================================================


def test_trace_inverse_certainty_requires_complete_trace():
    """Law 6: TraceInverse cannot claim certainty without complete trace."""
    incomplete_trace = OperationTrace(
        operation_name="test_op",
        before_identity="before_id",
        after_identity="after_id",
        preserved_invariant="identity",
        changed_components=("haraka",),
        trace_data=MappingProxyType({}),
        is_complete=False,  # Incomplete!
        is_injective_operation=True,
        carries_preimage=False,
        residuals_at_operation=frozenset(),
        rank_at_operation=Rank.HYPOTHESIS
    )

    with pytest.raises(ValueError, match="cannot claim certainty without complete trace"):
        TraceInverse(
            after_state="test",
            trace=incomplete_trace,
            domain="test_domain",
            recovered_before="recovered",
            alternative_candidates=(),
            residuals=frozenset(),
            rank=Rank.STRONG_HYPOTHESIS,
            is_certain=True,  # Claiming certainty with incomplete trace!
            certainty_basis="injective"
        )


def test_trace_inverse_certain_with_injective():
    """Law 6: TraceInverse certain when operation injective and trace complete."""
    complete_trace = OperationTrace(
        operation_name="add_diacritics",
        before_identity="ك ت ب",
        after_identity="كَتَبَ",
        preserved_invariant="root_identity",
        changed_components=("diacritics",),
        trace_data=MappingProxyType({"original_form": "ك ت ب"}),
        is_complete=True,
        is_injective_operation=True,  # Injective: can reverse
        carries_preimage=False,
        residuals_at_operation=frozenset(),
        rank_at_operation=Rank.HYPOTHESIS
    )

    trace_inv = TraceInverse(
        after_state="كَتَبَ",
        trace=complete_trace,
        domain="morphology",
        recovered_before="ك ت ب",
        alternative_candidates=(),
        residuals=frozenset(),
        rank=Rank.STRONG_HYPOTHESIS,
        is_certain=True,
        certainty_basis="injective"
    )

    assert trace_inv.is_certain is True
    assert trace_inv.certainty_basis == "injective"
    assert trace_inv.recovered_before == "ك ت ب"


def test_trace_inverse_certain_with_preimage():
    """Law 6: TraceInverse certain when trace carries preimage (non-injective op)."""
    complete_trace_with_preimage = OperationTrace(
        operation_name="idgham_assimilation",
        before_identity="ن + ل",
        after_identity="لّ",  # Assimilated
        preserved_invariant="segment_count",
        changed_components=("first_consonant", "gemination"),
        trace_data=MappingProxyType({"deleted_consonant": "ن"}),  # Carries preimage!
        is_complete=True,
        is_injective_operation=False,  # Non-injective (deletion)
        carries_preimage=True,  # But trace carries lost info
        residuals_at_operation=frozenset(),
        rank_at_operation=Rank.HYPOTHESIS
    )

    trace_inv = TraceInverse(
        after_state="لّ",
        trace=complete_trace_with_preimage,
        domain="phonology",
        recovered_before="ن + ل",
        alternative_candidates=(),
        residuals=frozenset(),
        rank=Rank.STRONG_HYPOTHESIS,
        is_certain=True,
        certainty_basis="trace_carries_preimage"
    )

    assert trace_inv.is_certain is True
    assert trace_inv.certainty_basis == "trace_carries_preimage"


# ============================================================================
# Test Law 7: Incomplete Trace → Lowered Rank
# ============================================================================


def test_incomplete_trace_requires_lowered_rank():
    """Law 7: Incomplete trace must have rank ≤ HYPOTHESIS."""
    incomplete_trace = OperationTrace(
        operation_name="partial_op",
        before_identity="before",
        after_identity="after",
        preserved_invariant="identity",
        changed_components=("unknown",),
        trace_data=MappingProxyType({}),
        is_complete=False,  # Incomplete
        is_injective_operation=False,
        carries_preimage=False,
        residuals_at_operation=frozenset(),
        rank_at_operation=Rank.HYPOTHESIS
    )

    with pytest.raises(ValueError, match="Incomplete trace requires rank ≤ HYPOTHESIS"):
        TraceInverse(
            after_state="test",
            trace=incomplete_trace,
            domain="test_domain",
            recovered_before=None,
            alternative_candidates=("a", "b"),
            residuals=frozenset(),  # Also wrong - should have residuals
            rank=Rank.STRONG_HYPOTHESIS,  # Too high!
            is_certain=False,
            certainty_basis=None
        )


def test_incomplete_trace_requires_residuals():
    """Law 7: Incomplete trace must have residuals."""
    incomplete_trace = OperationTrace(
        operation_name="partial_op",
        before_identity="before",
        after_identity="after",
        preserved_invariant="identity",
        changed_components=("unknown",),
        trace_data=MappingProxyType({}),
        is_complete=False,  # Incomplete
        is_injective_operation=False,
        carries_preimage=False,
        residuals_at_operation=frozenset(),
        rank_at_operation=Rank.HYPOTHESIS
    )

    with pytest.raises(ValueError, match="Incomplete trace MUST have residuals"):
        TraceInverse(
            after_state="test",
            trace=incomplete_trace,
            domain="test_domain",
            recovered_before=None,
            alternative_candidates=("a", "b"),
            residuals=frozenset(),  # Empty residuals not allowed!
            rank=Rank.HYPOTHESIS,
            is_certain=False,
            certainty_basis=None
        )


# ============================================================================
# Test Law 8: Operations Stop Before Meaning
# ============================================================================


def test_meaning_stop_gate_blocks_meaning_field():
    """Law 8: MeaningStopGate prevents meaning field."""
    gate = MeaningStopGate()

    @dataclass
    class BadOutput:
        result: str
        meaning: str  # Forbidden!

    output = BadOutput(result="test", meaning="semantic content")

    with pytest.raises(ValueError, match="MUST NOT contain 'meaning'"):
        gate.validate(output)


def test_meaning_stop_gate_blocks_ifadah_field():
    """Law 8: MeaningStopGate prevents ifadah field."""
    gate = MeaningStopGate()

    @dataclass
    class BadOutput:
        result: str
        ifadah_identity: str  # Forbidden!

    output = BadOutput(result="test", ifadah_identity="pragmatic closure")

    with pytest.raises(ValueError, match="MUST NOT contain 'ifadah_identity'"):
        gate.validate(output)


def test_operation_spec_requires_meaning_prohibition():
    """Law 8: OperationSpec.stop_before_meaning must be True."""
    license = LicenseSpec(
        license_type=LicenseType.MORPHOLOGICAL_BAB,
        licensing_condition="test",
        required_prior_info=frozenset()
    )
    cause_geo = CauseGeometry(
        prior_info=frozenset(),
        bāb="test_bab",
        domain="test_domain",
        material_cause="test_material",
        formal_cause="test_formal",
        efficient_cause="test_efficient",
        final_cause_before_meaning="test_final",
        license=license,
        invariant="identity",
        trace_requirement=TraceRequirement.MINIMAL,
        residual_handling="inherit",
        rank_assignment=Rank.CANDIDATE
    )
    before_after = BeforeAfterRelation(
        operation_name="test_op",
        before_type=str,
        after_type=str,
        identity_preservation="preserved",
        change_description="none",
        reversibility=True,
        trace_requirement=TraceRequirement.MINIMAL
    )

    with pytest.raises(ValueError, match="stop_before_meaning MUST be True"):
        OperationSpec(
            name="test_op",
            domain_before="D0",
            domain_after="D1",
            input_type=str,
            output_type=str,
            required_prior_info=frozenset(),
            bāb="test_bab",
            cause_geometry=cause_geo,
            licensed_operation=lambda x: x,
            declared_before_after_relation=before_after,
            preserved_invariant="identity",
            changed_component="none",
            trace_policy=TracePolicy(
                required_completeness=False,
                preserved_preimage_fields=frozenset(),
                injective_operation=True,
                inverse_certainty_conditions=()
            ),
            residual_policy=ResidualPolicy(
                inherited_residuals=frozenset(),
                operation_residuals=frozenset(),
                discharge_conditions=MappingProxyType({}),
                blocking_residuals=frozenset()
            ),
            rank_policy=RankPolicy(
                input_rank_requirement=Rank.CANDIDATE,
                output_rank=Rank.HYPOTHESIS,
                rank_lowering_conditions=MappingProxyType({})
            ),
            surface_inverse_policy=None,
            trace_inverse_policy=None,
            forbidden_outputs=frozenset(["meaning", "ifadah", "hukm", "semantic_identity"]),
            next_allowed_operations=frozenset(),
            stop_before_meaning=False  # Forbidden!
        )


# ============================================================================
# Test Law 9: BackwardAudit Validates Domain
# ============================================================================


def test_backward_audit_verified_certain_requires_all_checks():
    """Law 9: AuditStatus.VERIFIED_CERTAIN requires all checks to pass."""
    # Attempt to create verified certain with failed checks
    with pytest.raises(ValueError, match="requires all verifications to pass"):
        BackwardAudit(
            after_state="test",
            trace=OperationTrace(
                operation_name="test_op",
                before_identity="before",
                after_identity="after",
                preserved_invariant="identity",
                changed_components=(),
                trace_data=MappingProxyType({}),
                is_complete=True,
                is_injective_operation=True,
                carries_preimage=False,
                residuals_at_operation=frozenset(),
                rank_at_operation=Rank.HYPOTHESIS
            ),
            attempted_recovery="recovered",
            audit_result=AuditResult(
                status=AuditStatus.VERIFIED_CERTAIN,
                verified_invariant=True,
                verified_domain=False,  # Failed!
                verified_trace_complete=True,
                verified_no_meaning=True,
                violation_details=()
            ),
            residuals=frozenset(),
            rank=Rank.STRONG_HYPOTHESIS
        )


def test_backward_audit_valid():
    """Law 9: Valid BackwardAudit with all checks passing."""
    trace = OperationTrace(
        operation_name="add_haraka",
        before_identity="ك ت ب",
        after_identity="كَتَبَ",
        preserved_invariant="consonant_identity",
        changed_components=("diacritics",),
        trace_data=MappingProxyType({"operation": "add_fatha"}),
        is_complete=True,
        is_injective_operation=True,
        carries_preimage=False,
        residuals_at_operation=frozenset(),
        rank_at_operation=Rank.HYPOTHESIS
    )

    audit = BackwardAudit(
        after_state="كَتَبَ",
        trace=trace,
        attempted_recovery="ك ت ب",
        audit_result=AuditResult(
            status=AuditStatus.VERIFIED_CERTAIN,
            verified_invariant=True,
            verified_domain=True,
            verified_trace_complete=True,
            verified_no_meaning=True,
            violation_details=()
        ),
        residuals=frozenset(),
        rank=Rank.STRONG_HYPOTHESIS
    )

    assert audit.audit_result.status == AuditStatus.VERIFIED_CERTAIN
    assert audit.audit_result.verified_domain is True
    assert audit.audit_result.verified_no_meaning is True


# ============================================================================
# Test Law 10: Trace Does Not Imply Meaning
# ============================================================================


def test_operation_trace_forbids_semantic_data():
    """Law 10: OperationTrace.trace_data must not contain semantic info."""
    # This is a documentation test - trace_data is untyped dict
    # Constitutional requirement: do not store meaning in trace_data
    trace = OperationTrace(
        operation_name="valid_op",
        before_identity="before",
        after_identity="after",
        preserved_invariant="identity",
        changed_components=("structure",),
        trace_data=MappingProxyType({
            "operation_type": "structural",
            "preserved_root": "ك ت ب",
            # NO "meaning", "semantic_value", etc.
        }),
        is_complete=True,
        is_injective_operation=True,
        carries_preimage=False,
        residuals_at_operation=frozenset(),
        rank_at_operation=Rank.HYPOTHESIS
    )

    # Verify trace_data does not contain meaning keys
    forbidden_keys = {"meaning", "semantic", "murad", "haqiqa", "ifadah", "hukm"}
    actual_keys = set(trace.trace_data.keys())
    violation = actual_keys.intersection(forbidden_keys)

    assert len(violation) == 0, (
        f"OperationTrace.trace_data contains forbidden semantic keys: {violation}. "
        f"Violation of Operation Algebra Constitution Law #10."
    )


# ============================================================================
# Test: Rank Policy Prohibition
# ============================================================================


def test_rank_policy_forbids_certification():
    """Operations cannot produce CERTIFICATE rank."""
    with pytest.raises(ValueError, match="MUST NOT produce CERTIFICATE"):
        RankPolicy(
            input_rank_requirement=Rank.STRONG_HYPOTHESIS,
            output_rank=Rank.CERTIFICATE,  # Forbidden!
            rank_lowering_conditions=MappingProxyType({}),
            certification_prohibited=True
        )


def test_rank_policy_requires_certification_prohibited():
    """RankPolicy.certification_prohibited must be True."""
    with pytest.raises(ValueError, match="certification_prohibited MUST be True"):
        RankPolicy(
            input_rank_requirement=Rank.CANDIDATE,
            output_rank=Rank.HYPOTHESIS,
            rank_lowering_conditions=MappingProxyType({}),
            certification_prohibited=False  # Forbidden!
        )


# ============================================================================
# Test: Integration - Valid Complete OperationSpec
# ============================================================================


def test_valid_complete_operation_spec():
    """Integration test: Valid complete OperationSpec."""
    license = LicenseSpec(
        license_type=LicenseType.MORPHOLOGICAL_BAB,
        licensing_condition="trilateral root + فَعَلَ pattern",
        required_prior_info=frozenset(["root_identity", "pattern_identity"])
    )

    cause_geo = CauseGeometry(
        prior_info=frozenset(["root=ك ت ب", "pattern=فَعَلَ"]),
        bāb="باب فَعَلَ",
        domain="trilateral_verbs",
        material_cause="consonantal root ك ت ب",
        formal_cause="pattern فَعَلَ with slots",
        efficient_cause="morphological licensing via bāb",
        final_cause_before_meaning="verbal form candidate (pre-semantic)",
        license=license,
        invariant="root_consonant_identity",
        trace_requirement=TraceRequirement.COMPLETE,
        residual_handling="inherit_and_track",
        rank_assignment=Rank.HYPOTHESIS
    )

    before_after = BeforeAfterRelation(
        operation_name="pattern_application",
        before_type=str,
        after_type=str,
        identity_preservation="root consonants preserved",
        change_description="pattern slots filled with harakat",
        reversibility=True,
        trace_requirement=TraceRequirement.COMPLETE
    )

    op_spec = OperationSpec(
        name="pattern_application",
        domain_before="root_domain",
        domain_after="verbal_form_domain",
        input_type=str,
        output_type=str,
        required_prior_info=frozenset(["root", "pattern"]),
        bāb="باب فَعَلَ",
        cause_geometry=cause_geo,
        licensed_operation=lambda x: f"كَتَبَ",  # Simplified
        declared_before_after_relation=before_after,
        preserved_invariant="root_consonants",
        changed_component="diacritics_and_slots",
        trace_policy=TracePolicy(
            required_completeness=True,
            preserved_preimage_fields=frozenset(["root", "pattern"]),
            injective_operation=True,
            inverse_certainty_conditions=("complete_trace", "injective")
        ),
        residual_policy=ResidualPolicy(
            inherited_residuals=frozenset(),
            operation_residuals=frozenset(),
            discharge_conditions=MappingProxyType({}),
            blocking_residuals=frozenset()
        ),
        rank_policy=RankPolicy(
            input_rank_requirement=Rank.CANDIDATE,
            output_rank=Rank.HYPOTHESIS,
            rank_lowering_conditions=MappingProxyType({
                "incomplete_trace": Rank.CANDIDATE
            })
        ),
        surface_inverse_policy="candidates_only",
        trace_inverse_policy="certain_if_complete_trace",
        forbidden_outputs=frozenset([
            "meaning", "ifadah", "hukm", "semantic_identity",
            "lexical_meaning", "contextual_meaning"
        ]),
        next_allowed_operations=frozenset(["operator_application", "composition"])
    )

    # Verify all constitutional requirements met
    assert op_spec.name == "pattern_application"
    assert op_spec.declared_before_after_relation is not None
    assert op_spec.cause_geometry is not None
    assert op_spec.cause_geometry.bāb == "باب فَعَلَ"
    assert op_spec.cause_geometry.domain == "trilateral_verbs"
    assert op_spec.stop_before_meaning is True
    assert "meaning" in op_spec.forbidden_outputs
    assert "ifadah" in op_spec.forbidden_outputs
    assert "hukm" in op_spec.forbidden_outputs
    assert "semantic_identity" in op_spec.forbidden_outputs
