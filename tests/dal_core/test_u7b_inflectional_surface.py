"""
U₇-B Inflectional Surface Contract Tests

Tests for inflectional surface marker detection before root/weight extraction.

Critical Law under test:
    علامات الإعراب والعدد والجنس والتعريف ليست جذورًا
    Iʿrāb, number, gender, and definiteness markers are NOT root letters.

Test Coverage:
    1. Dual surface markers (ان/ين) → stripped_core extraction
    2. Sound masculine plural (ون/ين) → stripped_core extraction
    3. Sound feminine plural (ات) → stripped_core extraction
    4. Al-definiteness (ال) → stripped_core extraction
    5. Tanwīn detection (ٌ/ٍ/ً)
    6. Iʿrāb surface hints (nominative/accusative/genitive/jussive)
    7. Gender surface hints (masculine/feminine/literal/semantic)
    8. Blocked root segments preservation
    9. Closed-class units skip inflectional analysis (already blocked)
"""

import pytest
from uuid import uuid4

from dal_core.foundation import Rank
from dal_core.u5_functional_role_carrier import (
    FunctionalRoleUnit,
    FunctionalRoleLayerObject,
    FunctionalRoleCandidate,
    RoleSort,
)
from dal_core.u6_mabni_closed_class_carrier import (
    mabni_closed_class_6,
)
from dal_core.u7_pre_weight_contract_carrier import (
    PathPermission,
    pre_weight_contract_7,
)


# ============================================================================
# Fixture: Create U₅ Layer
# ============================================================================

def make_u5_layer(surface: str) -> FunctionalRoleLayerObject:
    """Create U₅ layer for testing."""
    role_candidate = FunctionalRoleCandidate(
        uid=str(uuid4()),
        sort=RoleSort.ROOT,
        role=None,
        confidence=0.5,
        evidence=("default_open",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    unit = FunctionalRoleUnit(
        uid=str(uuid4()),
        surface=surface,
        source_lafz_unit_id="lafz_id",
        trace_4=("lafz_layer",),
        role_candidates=(role_candidate,),
        primary_role=role_candidate,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    return FunctionalRoleLayerObject(
        uid=str(uuid4()),
        units=(unit,),
        source_lafz_layer_id="lafz_layer",
        trace_4=("lafz_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )


# ============================================================================
# Test 1: Dual Surface Markers (كتابان → كتاب)
# ============================================================================

def test_dual_surface_marker_kitaabaan():
    """
    Critical Test: كتابان → dual_surface_hint=possible, stripped_core=كتاب

    Law:
        ان suffix is dual marker, NOT root letter.
        stripped_core_candidate must be كتاب.
        blocked_root_segments must include ان.
    """
    # U₅ → U₆ → U₇
    u5_layer = make_u5_layer("كتابان")
    u6_result = mabni_closed_class_6(u5_layer)
    assert u6_result.success

    u7_result = pre_weight_contract_7(u6_result.layer_object)
    assert u7_result.success
    assert u7_result.layer_object is not None

    # Get unit
    unit = u7_result.layer_object.units[0]
    profile = unit.inflectional_surface_profile
    assert profile is not None, "Open-class must have inflectional_surface_profile"

    # CRITICAL CHECKS
    assert profile.dual_surface_hint == PathPermission.POSSIBLE, \
        "كتابان must detect dual suffix"

    assert profile.stripped_core_candidate == "كتاب", \
        "stripped_core must be كتاب (not كتابان)"

    assert "ان" in profile.preserved_suffixes, \
        "ان must be preserved as suffix"

    assert "ان" in profile.blocked_root_segments, \
        "ان must be blocked from root analysis"

    # Sound plural should be unresolved (not dual)
    assert profile.sound_masculine_plural_surface_hint == PathPermission.UNRESOLVED
    assert profile.sound_feminine_plural_surface_hint == PathPermission.UNRESOLVED


def test_dual_surface_marker_kitaabayn():
    """
    Critical Test: كتابين → dual_surface_hint=possible, stripped_core=كتاب
    """
    u5_layer = make_u5_layer("كتابين")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    unit = u7_result.layer_object.units[0]
    profile = unit.inflectional_surface_profile

    assert profile.dual_surface_hint == PathPermission.POSSIBLE
    assert profile.stripped_core_candidate == "كتاب"
    assert "ين" in profile.preserved_suffixes
    assert "ين" in profile.blocked_root_segments


# ============================================================================
# Test 2: Sound Masculine Plural (مسلمون → مسلم)
# ============================================================================

def test_sound_masculine_plural_muslimuun():
    """
    Critical Test: مسلمون → sound_masc_plural=possible, stripped_core=مسلم

    Law:
        ون suffix is sound masculine plural marker, NOT root letter.
        stripped_core_candidate must be مسلم.
        blocked_root_segments must include ون.
    """
    u5_layer = make_u5_layer("مسلمون")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    unit = u7_result.layer_object.units[0]
    profile = unit.inflectional_surface_profile

    assert profile.sound_masculine_plural_surface_hint == PathPermission.POSSIBLE
    assert profile.stripped_core_candidate == "مسلم"
    assert "ون" in profile.preserved_suffixes
    assert "ون" in profile.blocked_root_segments

    # Dual should be unresolved
    assert profile.dual_surface_hint == PathPermission.UNRESOLVED


# ============================================================================
# Test 3: Sound Feminine Plural (مسلمات → مسلم)
# ============================================================================

def test_sound_feminine_plural_muslimaat():
    """
    Critical Test: مسلمات → sound_fem_plural=possible, stripped_core=مسلم

    Law:
        ات suffix is sound feminine plural marker, NOT root letter.
        stripped_core_candidate must be مسلم.
        blocked_root_segments must include ات.
    """
    u5_layer = make_u5_layer("مسلمات")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    unit = u7_result.layer_object.units[0]
    profile = unit.inflectional_surface_profile

    assert profile.sound_feminine_plural_surface_hint == PathPermission.POSSIBLE
    assert profile.stripped_core_candidate == "مسلم"
    assert "ات" in profile.preserved_suffixes
    assert "ات" in profile.blocked_root_segments

    # Also detects feminine
    assert profile.feminine_surface_hint == PathPermission.POSSIBLE
    assert profile.literal_feminine_hint == PathPermission.POSSIBLE


# ============================================================================
# Test 4: Al-Definiteness (الكتاب → كتاب)
# ============================================================================

def test_al_definiteness_alkitaab():
    """
    Critical Test: الكتاب → al_definiteness=possible, stripped_core=كتاب

    Law:
        ال prefix is definiteness marker, NOT root letter.
        stripped_core_candidate must be كتاب.
    """
    u5_layer = make_u5_layer("الكتاب")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    unit = u7_result.layer_object.units[0]
    profile = unit.inflectional_surface_profile

    assert profile.al_definiteness_surface_hint == PathPermission.POSSIBLE
    assert profile.stripped_core_candidate == "كتاب", \
        "ال must be stripped, core is كتاب"

    # Tanwīn should be unresolved (mutually exclusive with ال)
    assert profile.tanwin_surface_hint == PathPermission.UNRESOLVED


# ============================================================================
# Test 5: Tanwīn Detection (كتابٌ)
# ============================================================================

@pytest.mark.parametrize("surface,expected_hint", [
    ("كتابٌ", PathPermission.POSSIBLE),   # Nominative tanwīn
    ("كتابٍ", PathPermission.POSSIBLE),   # Genitive tanwīn
    ("كتابًا", PathPermission.POSSIBLE),  # Accusative tanwīn
    ("كتاب", PathPermission.UNRESOLVED),  # No tanwīn
])
def test_tanwin_detection(surface, expected_hint):
    """
    Critical Test: Tanwīn surface hint detection.
    """
    u5_layer = make_u5_layer(surface)
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    unit = u7_result.layer_object.units[0]
    profile = unit.inflectional_surface_profile

    assert profile.tanwin_surface_hint == expected_hint


# ============================================================================
# Test 6: Iʿrāb Surface Hints
# ============================================================================

def test_irab_nominative_hint():
    """Test nominative iʿrāb surface hint (ٌ or ُ)."""
    u5_layer = make_u5_layer("كتابٌ")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    profile = u7_result.layer_object.units[0].inflectional_surface_profile
    assert profile.nominative_surface_hint == PathPermission.POSSIBLE


def test_irab_genitive_hint():
    """Test genitive iʿrāb surface hint (ٍ or ِ)."""
    u5_layer = make_u5_layer("كتابٍ")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    profile = u7_result.layer_object.units[0].inflectional_surface_profile
    assert profile.genitive_surface_hint == PathPermission.POSSIBLE


def test_irab_accusative_hint():
    """Test accusative iʿrāb surface hint (ً or َ)."""
    u5_layer = make_u5_layer("كتابًا")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    profile = u7_result.layer_object.units[0].inflectional_surface_profile
    assert profile.accusative_surface_hint == PathPermission.POSSIBLE


# ============================================================================
# Test 7: Gender Surface Hints
# ============================================================================

def test_feminine_literal_hint_taa_marbutah():
    """Test literal feminine hint with tāʾ marbūṭa (ة)."""
    u5_layer = make_u5_layer("كاتبة")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    profile = u7_result.layer_object.units[0].inflectional_surface_profile
    assert profile.feminine_surface_hint == PathPermission.POSSIBLE
    assert profile.literal_feminine_hint == PathPermission.POSSIBLE


def test_masculine_hint_no_feminine_marker():
    """Test masculine hint when no feminine marker present."""
    u5_layer = make_u5_layer("كاتب")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    profile = u7_result.layer_object.units[0].inflectional_surface_profile
    assert profile.masculine_surface_hint == PathPermission.POSSIBLE
    assert profile.semantic_feminine_hint == PathPermission.POSSIBLE  # Could be semantic feminine


# ============================================================================
# Test 8: Blocked Root Segments
# ============================================================================

def test_blocked_root_segments_comprehensive():
    """
    Critical Test: All inflectional markers must be blocked from root analysis.

    Examples:
        كتابان → blocked: ان
        مسلمون → blocked: ون
        مسلمات → blocked: ات
    """
    test_cases = [
        ("كتابان", "ان"),
        ("مسلمون", "ون"),
        ("مسلمات", "ات"),
        ("كتابين", "ين"),
    ]

    for surface, expected_blocked in test_cases:
        u5_layer = make_u5_layer(surface)
        u6_result = mabni_closed_class_6(u5_layer)
        u7_result = pre_weight_contract_7(u6_result.layer_object)

        profile = u7_result.layer_object.units[0].inflectional_surface_profile
        assert expected_blocked in profile.blocked_root_segments, \
            f"{surface}: {expected_blocked} must be blocked from root"


# ============================================================================
# Test 9: Closed-Class Units (No Inflectional Analysis)
# ============================================================================

def test_closed_class_no_inflectional_analysis():
    """
    Critical Test: Closed-class units must NOT have inflectional analysis.

    Law:
        Closed-class (وَ, بِ, فَ) already blocked at U₇-A.
        U₇-B inflectional analysis only applies to open-class units.
    """
    # Create closed-class unit via U₅
    from dal_core.u5_functional_role_carrier import ClosedClassRoleCandidate

    role_candidate = FunctionalRoleCandidate(
        uid=str(uuid4()),
        sort=RoleSort.CLOSED_CLASS,
        role=ClosedClassRoleCandidate.HARF_ATF_CANDIDATE,
        confidence=0.9,
        evidence=("surface_match",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    unit = FunctionalRoleUnit(
        uid=str(uuid4()),
        surface="وَ",
        source_lafz_unit_id="lafz_id",
        trace_4=("lafz_layer",),
        role_candidates=(role_candidate,),
        primary_role=role_candidate,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    u5_layer = FunctionalRoleLayerObject(
        uid=str(uuid4()),
        units=(unit,),
        source_lafz_layer_id="lafz_layer",
        trace_4=("lafz_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    unit = u7_result.layer_object.units[0]

    # CRITICAL: Closed-class should have None for inflectional_surface_profile
    assert unit.inflectional_surface_profile is None, \
        "Closed-class units must NOT have inflectional analysis"


# ============================================================================
# Test 10: Forbidden Fields
# ============================================================================

def test_inflectional_profile_no_forbidden_fields():
    """
    Critical Test: InflectionalSurfaceProfile must NOT contain forbidden fields.

    Forbidden fields:
        - i3rab_certificate
        - number_certificate
        - gender_certificate
        - definiteness_certificate
        - root
        - weight
    """
    u5_layer = make_u5_layer("كتابان")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    profile = u7_result.layer_object.units[0].inflectional_surface_profile

    forbidden_fields = [
        'i3rab_certificate', 'case_marking',
        'number_certificate', 'quantity',
        'gender_certificate', 'gender',
        'definiteness_certificate', 'is_definite',
        'root', 'root_certificate',
        'weight', 'weight_certificate',
        'pattern', 'meaning', 'hukm'
    ]

    for field in forbidden_fields:
        assert not hasattr(profile, field), \
            f"InflectionalSurfaceProfile MUST NOT have '{field}' field"


# ============================================================================
# Summary Test: Complete U₇-B Pipeline
# ============================================================================

def test_u7b_complete_pipeline():
    """
    COMPREHENSIVE: U₇-B complete pipeline test.

    Tests: كتابان through full U₅→U₆→U₇ pipeline

    Verifies:
        1. U₇-B inflectional analysis executed
        2. Dual surface marker detected
        3. Stripped core extracted correctly
        4. Blocked root segments preserved
        5. All hints are hints (not certificates)
    """
    u5_layer = make_u5_layer("كتابان")
    u6_result = mabni_closed_class_6(u5_layer)
    assert u6_result.success

    u7_result = pre_weight_contract_7(u6_result.layer_object)
    assert u7_result.success

    unit = u7_result.layer_object.units[0]
    profile = unit.inflectional_surface_profile

    # Verify U₇-B executed
    assert profile is not None

    # Verify dual detection
    assert profile.dual_surface_hint == PathPermission.POSSIBLE

    # Verify core extraction
    assert profile.stripped_core_candidate == "كتاب"
    assert "ان" in profile.preserved_suffixes
    assert "ان" in profile.blocked_root_segments

    # Verify hints (not certificates)
    assert profile.nominative_surface_hint in [PathPermission.POSSIBLE, PathPermission.UNRESOLVED]
    assert isinstance(profile.dual_surface_hint, PathPermission)

    # Verify trace preservation
    assert profile.trace_source == "كتابان"

    print("\n✅ U₇-B Complete Pipeline Test PASSED")
    print(f"   Original surface: {profile.trace_source}")
    print(f"   Stripped core: {profile.stripped_core_candidate}")
    print(f"   Preserved suffixes: {profile.preserved_suffixes}")
    print(f"   Blocked root segments: {profile.blocked_root_segments}")
    print(f"   Dual hint: {profile.dual_surface_hint.value}")
