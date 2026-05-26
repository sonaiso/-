"""
Tests for U₇-B Inflectional Surface Contract Carrier

Tests verify:
1. Surface marker protection (الـ, تنوين, ان/ين/ون/ات, ة, etc.)
2. Architectural separation: surface ≠ protected_core ≠ root_input
3. No marker deletion (only protection + classification + residuals)
4. Golden cases from problem statement
5. Constitutional prohibitions (no root, weight, hukm, i3rab_final, etc.)
"""

import pytest
from uuid import uuid4

from dal_core.foundation import Rank
from dal_core.residuals import Residual
from dal_core.u7_pre_weight_contract_carrier import (
    PreWeightContractLayerObject,
    PreWeightContractUnit,
    ContractStatus,
    PathPermission,
)
from dal_core.u7b_inflectional_surface_contract_carrier import (
    inflectional_surface_contract_7b,
    InflectionalSurfaceContractLayerObject,
    InflectionalSurfaceContractUnit,
    MarkerHint,
    CPB7B,
)


def make_test_u7_unit(
    surface: str,
    contract_status: ContractStatus = ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE,
    root_path_permission: PathPermission = PathPermission.POSSIBLE
) -> PreWeightContractUnit:
    """Helper to create test U₇-A pre-weight contract unit."""
    return PreWeightContractUnit(
        uid=str(uuid4()),
        surface=surface,
        source_u6_unit_id=str(uuid4()),
        source_u6_trace=(str(uuid4()),),
        open_closed_status="open_class",
        contract_status=contract_status,
        lexical_path_potential=root_path_permission,
        root_path_permission=root_path_permission,
        stem_path_permission=root_path_permission,
        weight_path_permission=root_path_permission,
        jamid_surface_potential=PathPermission.UNRESOLVED,
        proper_name_surface_potential=PathPermission.UNRESOLVED,
        loanword_surface_potential=PathPermission.UNRESOLVED,
        frozen_primitive_potential=PathPermission.UNRESOLVED,
        derivational_readiness=PathPermission.UNRESOLVED,
        required_evidence=(),
        blocked_paths=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=(str(uuid4()),)
    )


def make_test_u7_layer(units: list[PreWeightContractUnit]) -> PreWeightContractLayerObject:
    """Helper to create test U₇-A layer."""
    return PreWeightContractLayerObject(
        uid=str(uuid4()),
        units=tuple(units),
        source_mabni_layer_id=str(uuid4()),
        trace_6=(str(uuid4()),),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )


# ============================================================================
# Golden Cases Tests (From Problem Statement)
# ============================================================================

class TestGoldenCases:
    """Test golden cases specified in problem statement."""

    def test_al_kitaab_definiteness_marker(self):
        """
        Test: الكتاب
        Expected:
            - protected_prefixes = ("الـ",)
            - protected_core = "كتاب"
            - root_input = "كتاب"
            - definiteness_marker_hint = POSSIBLE
        """
        # Create U₇-A unit
        u7_unit = make_test_u7_unit("الكتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        # Apply U₇-B
        result = inflectional_surface_contract_7b(u7_layer)

        # Verify success
        assert result.success
        assert result.layer_object is not None
        assert len(result.layer_object.units) == 1

        # Verify unit
        unit = result.layer_object.units[0]
        assert unit.surface == "الكتاب"
        assert "الـ" in unit.protected_prefixes
        assert unit.protected_core == "كتاب"
        assert unit.root_input == "كتاب"
        assert unit.definiteness_marker_hint == MarkerHint.POSSIBLE

    def test_kitaabun_tanwin_marker(self):
        """
        Test: كتابٌ
        Expected:
            - protected_core = "كتاب"
            - root_input = "كتاب"
            - tanwin_marker_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("كتابٌ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.surface == "كتابٌ"
        assert unit.protected_core == "كتاب"
        assert unit.root_input == "كتاب"
        assert unit.tanwin_marker_hint == MarkerHint.POSSIBLE

    def test_muslimaani_dual_marker(self):
        """
        Test: مسلمان
        Expected:
            - protected_suffixes = ("ان",)
            - protected_core = "مسلم"
            - root_input = "مسلم"
            - number_marker_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("مسلمان")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.surface == "مسلمان"
        assert "ان" in unit.protected_suffixes
        assert unit.protected_core == "مسلم"
        assert unit.root_input == "مسلم"
        assert unit.number_marker_hint == MarkerHint.POSSIBLE

    def test_muslimiina_ambiguous_marker(self):
        """
        Test: مسلمين
        Expected:
            - protected_suffixes = ("ين",)
            - protected_core = "مسلم"
            - root_input = "مسلم"
            - residuals += ("ambiguous_dual_or_sound_masculine_plural_or_case_marker",)
        """
        u7_unit = make_test_u7_unit("مسلمين")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.surface == "مسلمين"
        assert "ين" in unit.protected_suffixes
        assert unit.protected_core == "مسلم"
        assert unit.root_input == "مسلم"
        assert unit.number_marker_hint == MarkerHint.AMBIGUOUS
        # Check residual warning exists
        residual_ids = {r.id for r in unit.residuals}
        assert any("ambiguous" in rid for rid in residual_ids)

    def test_muslimuuna_sound_masculine_plural(self):
        """
        Test: مسلمون
        Expected:
            - protected_suffixes = ("ون",)
            - protected_core = "مسلم"
            - root_input = "مسلم"
            - number_marker_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("مسلمون")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.surface == "مسلمون"
        assert "ون" in unit.protected_suffixes
        assert unit.protected_core == "مسلم"
        assert unit.root_input == "مسلم"
        assert unit.number_marker_hint == MarkerHint.POSSIBLE

    def test_muslimaatun_sound_feminine_plural(self):
        """
        Test: مسلمات
        Expected:
            - protected_suffixes = ("ات",)
            - protected_core = "مسلم"
            - root_input = "مسلم"
            - number_marker_hint = POSSIBLE
            - gender_marker_hint = POSSIBLE (implicitly from ات)
        """
        u7_unit = make_test_u7_unit("مسلمات")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.surface == "مسلمات"
        assert "ات" in unit.protected_suffixes
        assert unit.protected_core == "مسلم"
        assert unit.root_input == "مسلم"
        assert unit.number_marker_hint == MarkerHint.POSSIBLE

    def test_madrasatun_feminine_marker(self):
        """
        Test: مدرسة
        Expected:
            - protected_suffixes = ("ة",)
            - protected_core = "مدرس"
            - root_input = "مدرس"
            - gender_marker_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("مدرسة")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.surface == "مدرسة"
        assert "ة" in unit.protected_suffixes
        assert unit.protected_core == "مدرس"
        assert unit.root_input == "مدرس"
        assert unit.gender_marker_hint == MarkerHint.POSSIBLE

    def test_yaktubuuna_verb_with_prefixes_suffixes(self):
        """
        Test: يكتبون
        Expected:
            - protected_prefixes = ("ي",)
            - protected_suffixes = ("ون",)
            - protected_core = "كتب"
            - root_input = "كتب"
            - verb_prefix_hint = POSSIBLE
            - number_marker_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("يكتبون")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.surface == "يكتبون"
        assert "ي" in unit.protected_prefixes
        assert "ون" in unit.protected_suffixes
        assert unit.protected_core == "كتب"
        assert unit.root_input == "كتب"
        assert unit.verb_prefix_hint == MarkerHint.POSSIBLE
        assert unit.number_marker_hint == MarkerHint.POSSIBLE

    def test_istakhraja_mazid_prefix(self):
        """
        Test: استخرج
        Expected:
            - protected_prefixes = ("است",)
            - protected_core = "خرج"
            - root_input = "خرج"
            - mazid_extra_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("استخرج")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.surface == "استخرج"
        assert "است" in unit.protected_prefixes
        assert unit.protected_core == "خرج"
        assert unit.root_input == "خرج"
        assert unit.mazid_extra_hint == MarkerHint.POSSIBLE


# ============================================================================
# Architectural Separation Tests
# ============================================================================

class TestArchitecturalSeparation:
    """Test surface ≠ protected_core ≠ root_input separation."""

    def test_surface_not_equal_protected_core(self):
        """Verify surface ≠ protected_core when markers present."""
        u7_unit = make_test_u7_unit("الكتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        # Surface has الـ, protected_core doesn't
        assert unit.surface == "الكتاب"
        assert unit.protected_core == "كتاب"
        assert unit.surface != unit.protected_core

    def test_protected_core_equals_root_input_simple_case(self):
        """Verify protected_core == root_input in simple cases."""
        u7_unit = make_test_u7_unit("كتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        # No markers - all three should be same
        assert unit.protected_core == unit.root_input

    def test_all_three_fields_present(self):
        """Verify all three fields always present."""
        u7_unit = make_test_u7_unit("الكتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        # All three required fields must be present
        assert hasattr(unit, 'surface')
        assert hasattr(unit, 'protected_core')
        assert hasattr(unit, 'root_input')
        assert unit.surface
        assert unit.protected_core
        assert unit.root_input


# ============================================================================
# Constitutional Prohibition Tests
# ============================================================================

class TestConstitutionalProhibitions:
    """Test that forbidden fields do NOT exist in U₇-B."""

    def test_no_root_field(self):
        """Verify 'root' field does NOT exist."""
        u7_unit = make_test_u7_unit("كتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        assert not hasattr(unit, 'root')

    def test_no_weight_field(self):
        """Verify 'weight' field does NOT exist."""
        u7_unit = make_test_u7_unit("كتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        assert not hasattr(unit, 'weight')

    def test_no_hukm_field(self):
        """Verify 'hukm' field does NOT exist."""
        u7_unit = make_test_u7_unit("كتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        assert not hasattr(unit, 'hukm')

    def test_no_irab_final_field(self):
        """Verify 'i3rab_final' field does NOT exist."""
        u7_unit = make_test_u7_unit("كتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        assert not hasattr(unit, 'i3rab_final')
        assert not hasattr(unit, 'final_irab')

    def test_no_meaning_field(self):
        """Verify 'meaning' field does NOT exist."""
        u7_unit = make_test_u7_unit("كتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        assert not hasattr(unit, 'meaning')
        assert not hasattr(unit, 'dalalah')


# ============================================================================
# CPB₇B Tests
# ============================================================================

class TestCPB7B:
    """Test CPB₇B completeness predicate and proof builder."""

    def test_is_complete_valid_layer(self):
        """Test CPB7B.is_complete returns True for valid layer."""
        u7_unit = make_test_u7_unit("كتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        layer_obj = result.layer_object

        assert CPB7B.is_complete(layer_obj)

    def test_build_proof_includes_marker_counts(self):
        """Test CPB7B.build_proof includes marker statistics."""
        u7_units = [
            make_test_u7_unit("الكتاب"),  # definiteness
            make_test_u7_unit("كتابٌ"),    # tanwin
            make_test_u7_unit("مسلمان"),   # number
        ]
        u7_layer = make_test_u7_layer(u7_units)

        result = inflectional_surface_contract_7b(u7_layer)
        layer_obj = result.layer_object

        proof = CPB7B.build_proof(layer_obj)

        # Verify proof contains evidence about marker counts
        evidence_strings = [str(e) for e in proof.evidence]
        assert any("units_with_definiteness_hint" in e for e in evidence_strings)
        assert any("units_with_tanwin_hint" in e for e in evidence_strings)
        assert any("units_with_number_markers_hint" in e for e in evidence_strings)

    def test_proof_forbidden_gates_include_root_weight(self):
        """Test proof explicitly forbids root/weight certificates."""
        u7_unit = make_test_u7_unit("كتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        proof = result.layer_object.proof

        # Verify forbidden gates
        assert "root_certificate" in proof.forbidden_next_gates
        assert "weight_certificate" in proof.forbidden_next_gates
        assert "hukm_certificate" in proof.forbidden_next_gates

    def test_proof_allows_root_stem_candidate_gate(self):
        """Test proof allows U₈ RootStemCandidate as next gate."""
        u7_unit = make_test_u7_unit("كتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        proof = result.layer_object.proof

        # Verify allowed next gate
        assert "root_stem_candidate_gate" in proof.allowed_next_gates


# ============================================================================
# Marker Hint Tests
# ============================================================================

class TestMarkerHints:
    """Test that all marker hints are hints, NOT judgments."""

    def test_hints_are_marker_hint_enum(self):
        """Verify all hint fields use MarkerHint enum."""
        u7_unit = make_test_u7_unit("الكتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        # All hint fields should be MarkerHint enum values
        assert isinstance(unit.definiteness_marker_hint, MarkerHint)
        assert isinstance(unit.tanwin_marker_hint, MarkerHint)
        assert isinstance(unit.number_marker_hint, MarkerHint)
        assert isinstance(unit.gender_marker_hint, MarkerHint)
        assert isinstance(unit.verb_prefix_hint, MarkerHint)

    def test_unresolved_when_no_marker_detected(self):
        """Test hints are UNRESOLVED when no marker detected."""
        u7_unit = make_test_u7_unit("كتاب")  # No markers
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        # No definiteness marker → UNRESOLVED
        assert unit.definiteness_marker_hint == MarkerHint.UNRESOLVED
        # No tanwin → UNRESOLVED
        assert unit.tanwin_marker_hint == MarkerHint.UNRESOLVED


# ============================================================================
# Blocked Segments Tests
# ============================================================================

class TestBlockedSegments:
    """Test blocked_root_segments and blocked_weight_segments."""

    def test_blocked_segments_populated(self):
        """Test blocked segments contain protected markers."""
        u7_unit = make_test_u7_unit("الكتاب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        # الـ should be in blocked segments
        assert "الـ" in unit.blocked_root_segments
        assert "الـ" in unit.blocked_weight_segments

    def test_blocked_segments_prevent_marker_consumption(self):
        """Test blocked segments document what U₈/U₉ must NOT consume."""
        u7_unit = make_test_u7_unit("يكتبون")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)
        unit = result.layer_object.units[0]

        # Both prefix and suffix should be blocked
        assert "ي" in unit.blocked_root_segments
        assert "ون" in unit.blocked_root_segments
