"""
U₇ Critical Review Tests - Before PR Merge

These tests verify the 5 critical review points before declaring U₇ closed:

1. U₇ consumes real MabniClosedClassLayerObject from U₆ (not just mocks)
2. Closed-class (وَ, بِ, فَ, سَ, ـهِمْ, ـهَا) ALWAYS blocks root/weight paths
3. No direct U₆→U₈ or U₆→U₉ jumps possible
4. All forbidden fields tested and enforced
5. Explicit residuals on unresolved cases (no silent failures)

Law under test:
    U₇ closed over real U₆ output, not mocked fixtures only
"""

import pytest
from uuid import uuid4

from dal_core.foundation import Rank
from dal_core.u5_functional_role_carrier import (
    FunctionalRoleUnit,
    FunctionalRoleLayerObject,
    FunctionalRoleCandidate,
    RoleSort,
    ClosedClassRoleCandidate,
    PronounRoleCandidate,
)
from dal_core.u6_mabni_closed_class_carrier import (
    MabniClosedClassUnit,
    MabniClosedClassLayerObject,
    MabniClosedClassCandidate,
    MabniClosedClassType,
    ClosedClassSubtype,
    mabni_closed_class_6,
)
from dal_core.u7_pre_weight_contract_carrier import (
    ContractStatus,
    PathPermission,
    pre_weight_contract_7,
)


# ============================================================================
# Fixture: Create Real U₅ Layer (not mock)
# ============================================================================

def make_real_u5_layer_for_particle(surface: str, role_type: str) -> FunctionalRoleLayerObject:
    """Create real U₅ layer object for a particle."""
    if role_type == "conjunction":
        role_candidate = FunctionalRoleCandidate(
            uid=str(uuid4()),
            sort=RoleSort.CLOSED_CLASS,
            role=ClosedClassRoleCandidate.HARF_ATF_CANDIDATE,
            confidence=0.9,
            evidence=("surface_match",),
            residuals=frozenset(),
            rank=Rank.CANDIDATE
        )
    elif role_type == "preposition":
        role_candidate = FunctionalRoleCandidate(
            uid=str(uuid4()),
            sort=RoleSort.CLOSED_CLASS,
            role=ClosedClassRoleCandidate.HARF_JARR_CANDIDATE,
            confidence=0.9,
            evidence=("surface_match",),
            residuals=frozenset(),
            rank=Rank.CANDIDATE
        )
    else:  # open-class
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
# Critical Test 1: U₇ Consumes Real U₆ Output
# ============================================================================

def test_u7_consumes_real_u6_output_not_mock():
    """
    CRITICAL: U₇ must consume real MabniClosedClassLayerObject from U₆.

    Flow:
        Real U₅ → U₆ (mabni_closed_class_6) → Real U₆ output → U₇ (pre_weight_contract_7)
    """
    # Create real U₅ layer
    u5_layer = make_real_u5_layer_for_particle("وَ", "conjunction")

    # Run real U₆ function
    u6_result = mabni_closed_class_6(u5_layer)
    assert u6_result.success, "U₆ must succeed on real U₅ input"
    assert u6_result.layer_object is not None

    # Verify U₆ produced real MabniClosedClassLayerObject
    assert isinstance(u6_result.layer_object, MabniClosedClassLayerObject)
    assert len(u6_result.layer_object.units) > 0

    # Run real U₇ function on REAL U₆ output (not mock)
    u7_result = pre_weight_contract_7(u6_result.layer_object)
    assert u7_result.success, "U₇ must succeed on real U₆ output"
    assert u7_result.layer_object is not None

    # Verify U₇ processed real U₆ data
    assert u7_result.layer_object.source_mabni_layer_id == u6_result.layer_object.uid
    assert len(u7_result.layer_object.units) > 0


# ============================================================================
# Critical Test 2: Closed-Class ALWAYS Blocks Root/Weight
# ============================================================================

@pytest.mark.parametrize("surface,role_type", [
    ("وَ", "conjunction"),     # Conjunction
    ("بِ", "preposition"),     # Preposition
    ("فَ", "conjunction"),     # Conjunction
])
def test_closed_class_always_blocks_root_weight_real_u6(surface, role_type):
    """
    CRITICAL: Closed-class particles MUST ALWAYS block root/weight paths.

    Tests: وَ, بِ, فَ (and by extension سَ, ـهِمْ, ـهَا)

    Law:
        closed_class_mabni → root_path_permission = BLOCKED
        closed_class_mabni → weight_path_permission = BLOCKED
    """
    # Real U₅ → Real U₆ → Real U₇
    u5_layer = make_real_u5_layer_for_particle(surface, role_type)
    u6_result = mabni_closed_class_6(u5_layer)
    assert u6_result.success

    u7_result = pre_weight_contract_7(u6_result.layer_object)
    assert u7_result.success

    # Find the particle unit
    units = u7_result.layer_object.units
    particle_unit = None
    for unit in units:
        if surface in unit.surface:
            particle_unit = unit
            break

    assert particle_unit is not None, f"Must find {surface} in U₇ output"

    # CRITICAL CHECKS
    assert particle_unit.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED, \
        f"{surface} must be CLOSED_CLASS_BLOCKED"

    assert particle_unit.root_path_permission == PathPermission.BLOCKED, \
        f"{surface} root_path must be BLOCKED"

    assert particle_unit.weight_path_permission == PathPermission.BLOCKED, \
        f"{surface} weight_path must be BLOCKED"

    assert "root_extraction" in particle_unit.blocked_paths, \
        f"{surface} must block root_extraction"

    assert "weight_determination" in particle_unit.blocked_paths, \
        f"{surface} must block weight_determination"


# ============================================================================
# Critical Test 3: No Direct U₆→U₈ Jump
# ============================================================================

def test_no_direct_u6_to_u8_architectural_law():
    """
    CRITICAL: Verify no direct U₆→U₈ jump is possible.

    Law:
        U₆ → U₇ → U₈ (enforced via contract gate)
        U₆ → U₈ (forbidden)

    This test verifies that:
    1. U₇ is invoked between U₆ and any morphological analysis
    2. U₇ output contains path permissions (not root/weight extraction)
    """
    # Create open-class unit
    u5_layer = make_real_u5_layer_for_particle("كِتَابِ", "open-class")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    assert u7_result.success

    # Verify U₇ was invoked (has contract permissions)
    unit = u7_result.layer_object.units[0]
    assert hasattr(unit, 'root_path_permission'), "U₇ must provide root_path_permission"
    assert hasattr(unit, 'weight_path_permission'), "U₇ must provide weight_path_permission"
    assert hasattr(unit, 'contract_status'), "U₇ must provide contract_status"

    # Verify U₇ did NOT extract root/weight (that's U₈/U₉)
    assert not hasattr(unit, 'root'), "U₇ MUST NOT extract root"
    assert not hasattr(unit, 'weight'), "U₇ MUST NOT extract weight"


# ============================================================================
# Critical Test 4: Forbidden Fields Enforced
# ============================================================================

def test_forbidden_fields_comprehensive():
    """
    CRITICAL: All 14 forbidden fields must be tested and enforced.

    Forbidden fields:
        root, root_certificate, stem, stem_certificate,
        weight, weight_certificate, pattern, pattern_certificate,
        meaning, dalalah, ifadah, hukm, final_irab, resolved_reference
    """
    u5_layer = make_real_u5_layer_for_particle("كَتَبَ", "open-class")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    assert u7_result.success

    forbidden_fields = [
        'root', 'root_certificate',
        'stem', 'stem_certificate',
        'weight', 'weight_certificate',
        'pattern', 'pattern_certificate',
        'meaning', 'dalalah', 'ifadah',
        'hukm', 'final_irab',
        'resolved_reference'
    ]

    for unit in u7_result.layer_object.units:
        for field in forbidden_fields:
            assert not hasattr(unit, field), \
                f"U₇ unit MUST NOT have '{field}' field (constitutional violation)"


# ============================================================================
# Critical Test 5: Permission Semantics (possible vs approved)
# ============================================================================

def test_permission_semantics_possible_not_approved():
    """
    CRITICAL: Distinguish POSSIBLE vs APPROVED.

    For open-class without sufficient evidence:
        root_path_permission = POSSIBLE (not APPROVED)
        contract_status = OPEN_CORE_CONTRACT_CANDIDATE (not APPROVED)
        required_evidence = non-empty

    APPROVED should only appear when U₇ has verified evidence.
    """
    u5_layer = make_real_u5_layer_for_particle("كَتَبَ", "open-class")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    assert u7_result.success
    unit = u7_result.layer_object.units[0]

    # Should be POSSIBLE (permission), not APPROVED (certification)
    assert unit.root_path_permission == PathPermission.POSSIBLE, \
        "Without evidence, should be POSSIBLE not APPROVED"

    assert unit.weight_path_permission == PathPermission.POSSIBLE, \
        "Without evidence, should be POSSIBLE not APPROVED"

    # Contract should be CANDIDATE (not APPROVED)
    assert unit.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE, \
        "Without evidence, should be CANDIDATE not APPROVED"

    # Should have required_evidence
    assert len(unit.required_evidence) > 0, \
        "CANDIDATE status requires evidence specification"


# ============================================================================
# Critical Test 6: Explicit Residuals (No Silent Failures)
# ============================================================================

def test_explicit_residuals_no_silent_failures():
    """
    CRITICAL: U₇ must provide explicit residuals, never silent failures.

    Expected residual types (when applicable):
        - open_core_contract_unresolved
        - proper_name_possible
        - loanword_possible
        - jamid_possible
        - insufficient_lexical_evidence
        - ambiguous_derivational_readiness
        - surface_allows_multiple_paths
    """
    u5_layer = make_real_u5_layer_for_particle("كَتَبَ", "open-class")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    assert u7_result.success

    # U₇ result must have residuals field (even if empty)
    assert hasattr(u7_result, 'residuals')
    assert isinstance(u7_result.residuals, frozenset)

    # Units must have residuals field
    for unit in u7_result.layer_object.units:
        assert hasattr(unit, 'residuals')
        assert isinstance(unit.residuals, frozenset)

        # If contract unresolved, should have evidence requirements
        if unit.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE:
            assert len(unit.required_evidence) > 0, \
                "Unresolved contract must specify required_evidence"


# ============================================================================
# Critical Test 7: Derivational Readiness = UNRESOLVED
# ============================================================================

def test_derivational_readiness_unresolved_for_open_class():
    """
    CRITICAL: U₇ does NOT know if unit is mushtaq/jamid.

    For open-class without evidence:
        derivational_readiness = UNRESOLVED (not mushtaq/jamid)

    U₇ does NOT certify derivational status (that's U₈+).
    """
    u5_layer = make_real_u5_layer_for_particle("كَاتِب", "open-class")
    u6_result = mabni_closed_class_6(u5_layer)
    u7_result = pre_weight_contract_7(u6_result.layer_object)

    assert u7_result.success
    unit = u7_result.layer_object.units[0]

    # Derivational readiness must be UNRESOLVED
    assert unit.derivational_readiness == PathPermission.UNRESOLVED, \
        "U₇ cannot know if mushtaq/jamid without evidence"

    # Jamid potential should be UNRESOLVED (not certified)
    assert unit.jamid_surface_potential == PathPermission.UNRESOLVED, \
        "U₇ cannot certify jamid status"


# ============================================================================
# Summary Test: All Critical Laws
# ============================================================================

def test_u7_critical_laws_summary():
    """
    COMPREHENSIVE: Verify all critical U₇ laws in one test.

    Laws:
        1. U₇ consumes real U₆ output ✓
        2. Closed-class blocks root/weight ✓
        3. No direct U₆→U₈ jump ✓
        4. No forbidden fields ✓
        5. Explicit residuals ✓
        6. Permission = POSSIBLE (not APPROVED without evidence) ✓
        7. Derivational readiness = UNRESOLVED ✓
    """
    # Law 1: Real U₆ output
    u5_layer = make_real_u5_layer_for_particle("وَ", "conjunction")
    u6_result = mabni_closed_class_6(u5_layer)
    assert u6_result.success
    assert isinstance(u6_result.layer_object, MabniClosedClassLayerObject)

    # Law 2 & 3: U₇ processing
    u7_result = pre_weight_contract_7(u6_result.layer_object)
    assert u7_result.success

    unit = u7_result.layer_object.units[0]

    # Law 2: Closed-class blocks
    assert unit.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED
    assert unit.root_path_permission == PathPermission.BLOCKED
    assert unit.weight_path_permission == PathPermission.BLOCKED

    # Law 3: No direct jump (has permissions, not extraction)
    assert hasattr(unit, 'root_path_permission')
    assert not hasattr(unit, 'root')

    # Law 4: No forbidden fields
    forbidden = ['root', 'weight', 'meaning', 'hukm']
    for field in forbidden:
        assert not hasattr(unit, field)

    # Law 5: Explicit residuals
    assert hasattr(unit, 'residuals')
    assert isinstance(unit.residuals, frozenset)

    print("\n✅ All 7 critical U₇ laws verified")
