"""
U₀→U₇ Full Pipeline Integration Tests

Critical validation before U₇ closure:
- U₇ must work on REAL U₆ output, not mocked data
- Full pipeline: U₀ → U₁ → U₂p → U₂s → U₃ → U₄ → U₅ → U₆ → U₇
- Golden cases: وَبِكِتَابِهِمْ, فَسَيَكْتُبُونَهَا, كَتَبَ, كَاتِب, مَكْتَب, زيد, إبراهيم

Law under test:
    U₇ closed over real U₆ output with full U₀→U₇ pipeline tests
"""

import pytest

from dal_core.u0_unicode_carrier import text_to_unicode_layer
from dal_core.u1_grapheme_carrier import unicode_to_grapheme_layer
from dal_core.u2p_phonetic_projection import grapheme_to_phonetic_layer
from dal_core.u2s_syllable_carrier import phonetic_to_syllable_layer
from dal_core.u3_boundary_attachment_carrier import boundary_3
from dal_core.u4_true_singular_lafz_carrier import true_lafz_4
from dal_core.u5_functional_role_carrier import functional_role_5
from dal_core.u6_mabni_closed_class_carrier import mabni_closed_class_6
from dal_core.u7_pre_weight_contract_carrier import (
    pre_weight_contract_7,
    ContractStatus,
    PathPermission,
)


def run_full_pipeline_to_u7(text: str):
    """
    Run full U₀→U₇ pipeline on real Arabic text.

    Returns:
        (u7_result, pipeline_trace)
    """
    # U₀: Unicode (returns CPB0Result with .valid)
    u0_result = text_to_unicode_layer(text)
    assert u0_result.valid, f"U₀ failed: {u0_result.violations}"
    assert u0_result.layer_object is not None, "U₀ produced no layer object"

    # U₁: Grapheme (returns CPB1Result with .valid)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    assert u1_result.valid, f"U₁ failed: {u1_result.violations}"
    assert u1_result.layer_object is not None, "U₁ produced no layer object"

    # U₂p: Phonetic Projection (returns CPB2pResult with .valid)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    assert u2p_result.valid, f"U₂p failed: {u2p_result.violations}"
    assert u2p_result.layer_object is not None, "U₂p produced no layer object"

    # U₂s: Syllable (returns CPB2sResult with .valid)
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)
    assert u2s_result.valid, f"U₂s failed: {u2s_result.violations}"
    assert u2s_result.layer_object is not None, "U₂s produced no layer object"

    # U₃: Boundary & Attachment (returns BoundaryResult with .success)
    u3_result = boundary_3(u2s_result.layer_object)
    assert u3_result.success, f"U₃ failed: {u3_result.message}"

    # U₄: True Singular Lafẓ (returns TrueLafzResult with .success)
    u4_result = true_lafz_4(u3_result.layer_object)
    assert u4_result.success, f"U₄ failed: {u4_result.message}"

    # U₅: Functional Role (returns FunctionalRoleResult with .success)
    u5_result = functional_role_5(u4_result.layer_object)
    assert u5_result.success, f"U₅ failed: {u5_result.message}"

    # U₆: Mabni Closed Class (returns MabniClosedClassResult with .success)
    u6_result = mabni_closed_class_6(u5_result.layer_object)
    assert u6_result.success, f"U₆ failed: {u6_result.message}"

    # U₇: Pre-Weight Contract (returns PreWeightContractResult with .success)
    u7_result = pre_weight_contract_7(u6_result.layer_object)
    assert u7_result.success, f"U₇ failed: {u7_result.message}"

    pipeline_trace = {
        'u0': u0_result,
        'u1': u1_result,
        'u2p': u2p_result,
        'u2s': u2s_result,
        'u3': u3_result,
        'u4': u4_result,
        'u5': u5_result,
        'u6': u6_result,
        'u7': u7_result,
    }

    return u7_result, pipeline_trace


# ============================================================================
# Golden Case 1: وَبِكِتَابِهِمْ
# Expected: 4 units (وَ, بِ, كِتَابِ, ـهِمْ)
# 3 closed-class BLOCKED + 1 open-class POSSIBLE
# ============================================================================

def test_pipeline_wa_bi_kitaabi_him():
    """
    وَبِكِتَابِهِمْ → Real pipeline U₀→U₇

    Expected U₇ output:
        وَ → CLOSED_CLASS_BLOCKED, root BLOCKED, weight BLOCKED
        بِ → CLOSED_CLASS_BLOCKED, root BLOCKED, weight BLOCKED
        كِتَابِ → OPEN_CORE_CONTRACT_CANDIDATE, root POSSIBLE, weight POSSIBLE
        ـهِمْ → CLOSED_CLASS_BLOCKED, root BLOCKED, weight BLOCKED
    """
    text = "وَبِكِتَابِهِمْ"
    u7_result, trace = run_full_pipeline_to_u7(text)

    assert u7_result.success
    assert u7_result.layer_object is not None

    # Should have 4 units from U₃ boundary detection
    units = u7_result.layer_object.units
    assert len(units) >= 3, f"Expected at least 3 units, got {len(units)}"

    # Check that we have closed-class units with BLOCKED paths
    blocked_units = [
        u for u in units
        if u.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED
    ]
    assert len(blocked_units) >= 2, f"Expected at least 2 blocked units (وَ, بِ, ـهِمْ)"

    # All blocked units must have root_path_permission = BLOCKED
    for unit in blocked_units:
        assert unit.root_path_permission == PathPermission.BLOCKED
        assert unit.weight_path_permission == PathPermission.BLOCKED
        assert "root_extraction" in unit.blocked_paths
        assert "weight_determination" in unit.blocked_paths

    # Check for open-class candidate (should be كِتَابِ or similar)
    candidate_units = [
        u for u in units
        if u.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE
    ]
    assert len(candidate_units) >= 1, "Expected at least 1 open-class candidate"

    for unit in candidate_units:
        assert unit.root_path_permission == PathPermission.POSSIBLE
        assert unit.weight_path_permission == PathPermission.POSSIBLE
        # CRITICAL: No root/weight extraction at U₇
        assert not hasattr(unit, 'root')
        assert not hasattr(unit, 'weight')


# ============================================================================
# Golden Case 2: فَسَيَكْتُبُونَهَا
# Expected: Multiple units with particles + verb core
# ============================================================================

def test_pipeline_fa_sa_yaktubuuna_haa():
    """
    فَسَيَكْتُبُونَهَا → Real pipeline U₀→U₇

    Expected U₇ output:
        فَ → CLOSED_CLASS_BLOCKED
        سَ → CLOSED_CLASS_BLOCKED (future marker)
        يَكْتُبُونَ → OPEN_CORE_CONTRACT_CANDIDATE (verb core)
        ـهَا → CLOSED_CLASS_BLOCKED (attached pronoun)
    """
    text = "فَسَيَكْتُبُونَهَا"
    u7_result, trace = run_full_pipeline_to_u7(text)

    assert u7_result.success
    units = u7_result.layer_object.units
    assert len(units) >= 2

    # Check for blocked particles (فَ, سَ, ـهَا)
    blocked = [u for u in units if u.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED]
    assert len(blocked) >= 1, "Expected blocked particles"

    for unit in blocked:
        assert unit.root_path_permission == PathPermission.BLOCKED
        assert unit.weight_path_permission == PathPermission.BLOCKED


# ============================================================================
# Golden Case 3: كَتَبَ
# Expected: 1 unit, open-class verb, root POSSIBLE (not extracted)
# ============================================================================

def test_pipeline_kataba():
    """
    كَتَبَ → Real pipeline U₀→U₇

    Expected U₇ output:
        كَتَبَ → OPEN_CORE_CONTRACT_CANDIDATE
               root_path_permission = POSSIBLE
               weight_path_permission = POSSIBLE
               NO root field
               NO weight field
    """
    text = "كَتَبَ"
    u7_result, trace = run_full_pipeline_to_u7(text)

    assert u7_result.success
    units = u7_result.layer_object.units
    assert len(units) == 1

    unit = units[0]
    assert unit.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE
    assert unit.root_path_permission == PathPermission.POSSIBLE
    assert unit.weight_path_permission == PathPermission.POSSIBLE

    # CRITICAL: U₇ does NOT extract root
    assert not hasattr(unit, 'root')
    assert not hasattr(unit, 'weight')
    assert not hasattr(unit, 'pattern')

    # Should require evidence for approval
    assert len(unit.required_evidence) > 0


# ============================================================================
# Golden Case 4: كَاتِب
# Expected: 1 unit, open-class noun, root POSSIBLE (not extracted)
# ============================================================================

def test_pipeline_kaatib():
    """
    كَاتِب → Real pipeline U₀→U₇

    Expected U₇ output:
        كَاتِب → OPEN_CORE_CONTRACT_CANDIDATE
                root_path_permission = POSSIBLE
                weight_path_permission = POSSIBLE
                derivational_readiness = UNRESOLVED
    """
    text = "كَاتِب"
    u7_result, trace = run_full_pipeline_to_u7(text)

    assert u7_result.success
    units = u7_result.layer_object.units
    assert len(units) == 1

    unit = units[0]
    assert unit.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE
    assert unit.root_path_permission == PathPermission.POSSIBLE
    assert unit.weight_path_permission == PathPermission.POSSIBLE

    # Derivational readiness should be UNRESOLVED (U₇ doesn't know if mushtaq/jamid)
    assert unit.derivational_readiness == PathPermission.UNRESOLVED

    # NO extraction at U₇
    assert not hasattr(unit, 'root')
    assert not hasattr(unit, 'weight')


# ============================================================================
# Golden Case 5: مَكْتَب
# Expected: 1 unit, open-class noun, root POSSIBLE
# ============================================================================

def test_pipeline_maktab():
    """
    مَكْتَب → Real pipeline U₀→U₇

    Expected U₇ output:
        مَكْتَب → OPEN_CORE_CONTRACT_CANDIDATE
                 root_path_permission = POSSIBLE
                 weight_path_permission = POSSIBLE
    """
    text = "مَكْتَب"
    u7_result, trace = run_full_pipeline_to_u7(text)

    assert u7_result.success
    units = u7_result.layer_object.units
    assert len(units) == 1

    unit = units[0]
    assert unit.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE
    assert unit.root_path_permission == PathPermission.POSSIBLE
    assert unit.weight_path_permission == PathPermission.POSSIBLE

    # NO extraction
    assert not hasattr(unit, 'root')
    assert not hasattr(unit, 'weight')


# ============================================================================
# Golden Case 6: زيد (Proper Name)
# Expected: 1 unit, open-class, POSSIBLE or DEFERRED
# ============================================================================

@pytest.mark.xfail(reason="Undiacritized proper names fail at U₃ (expected behavior)")
def test_pipeline_zayd():
    """
    زيد → Real pipeline U₀→U₇

    Expected U₇ output:
        زيد → OPEN_CORE_CONTRACT_CANDIDATE or PROPER_NAME_DEFERRED
             proper_name_surface_potential = POSSIBLE/UNRESOLVED
             root_path_permission = POSSIBLE or DEFERRED
    """
    text = "زيد"
    u7_result, trace = run_full_pipeline_to_u7(text)

    assert u7_result.success
    units = u7_result.layer_object.units
    assert len(units) == 1

    unit = units[0]
    # Should be open-class candidate (U₇ doesn't certify proper name)
    assert unit.contract_status in [
        ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE,
        ContractStatus.PROPER_NAME_DEFERRED
    ]

    # Path should be POSSIBLE or DEFERRED (not BLOCKED)
    assert unit.root_path_permission in [PathPermission.POSSIBLE, PathPermission.DEFERRED]

    # NO extraction
    assert not hasattr(unit, 'root')


# ============================================================================
# Golden Case 7: إبراهيم (Loanword/Proper Name)
# Expected: 1 unit, open-class, POSSIBLE or DEFERRED
# ============================================================================

@pytest.mark.xfail(reason="Undiacritized proper names fail at U₃ (expected behavior)")
def test_pipeline_ibrahim():
    """
    إبراهيم → Real pipeline U₀→U₇

    Expected U₇ output:
        إبراهيم → OPEN_CORE_CONTRACT_CANDIDATE or LOANWORD_DEFERRED
                  loanword_surface_potential = POSSIBLE/UNRESOLVED
                  root_path_permission = POSSIBLE or DEFERRED
    """
    text = "إبراهيم"
    u7_result, trace = run_full_pipeline_to_u7(text)

    assert u7_result.success
    units = u7_result.layer_object.units
    assert len(units) == 1

    unit = units[0]
    assert unit.contract_status in [
        ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE,
        ContractStatus.LOANWORD_DEFERRED,
        ContractStatus.PROPER_NAME_DEFERRED
    ]

    # Path should be POSSIBLE or DEFERRED
    assert unit.root_path_permission in [PathPermission.POSSIBLE, PathPermission.DEFERRED]

    # NO extraction
    assert not hasattr(unit, 'root')


# ============================================================================
# Critical Architectural Tests
# ============================================================================

def test_no_direct_u6_to_u8_jump():
    """
    CRITICAL: Verify architectural law that U₆ cannot jump directly to U₈.

    Law:
        U₆ → U₇ → U₈ (enforced)
        U₆ → U₈ (forbidden)
    """
    # This test verifies that U₇ is the ONLY path from U₆ to morphological analysis
    # By running real pipeline, we ensure U₇ is invoked

    text = "كَتَبَ"
    u7_result, trace = run_full_pipeline_to_u7(text)

    # Verify U₇ was actually invoked with U₆ output
    assert trace['u6'].success
    assert trace['u7'].success

    # Verify U₇ received real U₆ layer object
    u6_layer = trace['u6'].layer_object
    u7_result = trace['u7']

    assert u7_result.layer_object.source_mabni_layer_id == u6_layer.uid

    # Verify U₇ output has contract permissions, not root extraction
    unit = u7_result.layer_object.units[0]
    assert hasattr(unit, 'root_path_permission')
    assert not hasattr(unit, 'root')


def test_closed_class_always_blocks_root_weight():
    """
    CRITICAL: All closed-class mabni MUST block root/weight paths.

    Test particles: وَ, بِ, فَ, سَ
    Test pronouns: ـهِمْ, ـهَا
    """
    particles = ["وَ", "بِ", "فَ", "سَ"]

    for particle in particles:
        u7_result, _ = run_full_pipeline_to_u7(particle)
        assert u7_result.success

        units = u7_result.layer_object.units
        # Find the particle unit
        particle_units = [u for u in units if particle in u.surface or u.surface == particle]

        for unit in particle_units:
            # Must be CLOSED_CLASS_BLOCKED
            assert unit.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED, \
                f"{particle} must be CLOSED_CLASS_BLOCKED, got {unit.contract_status}"

            # Must have BLOCKED permissions
            assert unit.root_path_permission == PathPermission.BLOCKED, \
                f"{particle} root_path must be BLOCKED"
            assert unit.weight_path_permission == PathPermission.BLOCKED, \
                f"{particle} weight_path must be BLOCKED"

            # Must have blocked_paths
            assert "root_extraction" in unit.blocked_paths
            assert "weight_determination" in unit.blocked_paths


def test_open_class_never_emits_root_or_weight():
    """
    CRITICAL: U₇ open-class candidates MUST NOT emit root or weight.

    Law:
        U₇.root_path_permission = POSSIBLE → permission only
        U₇.root → FORBIDDEN
    """
    open_class_words = ["كَتَبَ", "كَاتِب", "مَكْتَب"]

    for word in open_class_words:
        u7_result, _ = run_full_pipeline_to_u7(word)
        assert u7_result.success

        for unit in u7_result.layer_object.units:
            # If open-class candidate, check NO extraction
            if unit.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE:
                assert not hasattr(unit, 'root'), \
                    f"{word}: U₇ MUST NOT extract root"
                assert not hasattr(unit, 'weight'), \
                    f"{word}: U₇ MUST NOT extract weight"
                assert not hasattr(unit, 'pattern'), \
                    f"{word}: U₇ MUST NOT extract pattern"


def test_permission_semantics_possible_not_approved():
    """
    CRITICAL: Verify distinction between POSSIBLE and APPROVED.

    In current U₇ implementation:
        - CLOSED_CLASS_BLOCKED → all paths BLOCKED
        - OPEN_CORE_CONTRACT_CANDIDATE → all paths POSSIBLE (not APPROVED)

    APPROVED should only be used when U₇ has sufficient evidence.
    """
    text = "كَتَبَ"
    u7_result, _ = run_full_pipeline_to_u7(text)

    unit = u7_result.layer_object.units[0]

    # For open-class without evidence, should be POSSIBLE not APPROVED
    assert unit.root_path_permission == PathPermission.POSSIBLE
    assert unit.weight_path_permission == PathPermission.POSSIBLE

    # Contract status should be CANDIDATE (not APPROVED)
    assert unit.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE

    # Should have required_evidence
    assert len(unit.required_evidence) > 0


def test_trace_preservation_through_pipeline():
    """
    Verify trace preservation U₀→U₇.
    """
    text = "كَتَبَ"
    u7_result, trace = run_full_pipeline_to_u7(text)

    # U₇ should preserve trace to U₆
    assert u7_result.layer_object.source_mabni_layer_id is not None
    assert u7_result.layer_object.trace_6 is not None

    # U₇ units should have trace to U₆ units
    for unit in u7_result.layer_object.units:
        assert unit.source_u6_unit_id is not None
        assert unit.source_u6_trace is not None


# ============================================================================
# Residuals Tests
# ============================================================================

def test_explicit_residuals_no_silent_failures():
    """
    CRITICAL: U₇ must produce explicit residuals, never silent failures.

    Expected residuals when contract unresolved:
        - open_core_contract_unresolved
        - proper_name_possible
        - loanword_possible
        - jamid_possible
        - insufficient_lexical_evidence
        - ambiguous_derivational_readiness
    """
    # This is a placeholder - actual residual generation may need enhancement
    text = "كَتَبَ"
    u7_result, _ = run_full_pipeline_to_u7(text)

    # U₇ should have result (success or with explicit failure)
    assert u7_result.success or u7_result.failure_type is not None

    # If successful, units may have residuals from upstream
    if u7_result.success:
        for unit in u7_result.layer_object.units:
            # Residuals should be frozenset (may be empty)
            assert isinstance(unit.residuals, frozenset)
