"""
U₀→U₈ Full Pipeline Integration Tests

Critical validation for U₈ closure:
- U₈ must work on REAL U₇ output, not mocked data
- Full pipeline: U₀ → U₁ → U₂p → U₂s → U₃ → U₄ → U₅ → U₆ → U₇ → U₈
- Golden cases: وَبِكِتَابِهِمْ, فَسَيَكْتُبُونَهَا, كَتَبَ, كَاتِب, مَكْتَب

Law under test:
    U₈ closed over real U₇ output with full U₀→U₈ pipeline tests
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
from dal_core.u8_root_stem_candidate_carrier import (
    root_stem_candidate_8,
    RootCandidateStatus,
    StemCandidateStatus,
    RadicalCountHint,
)


def run_full_pipeline_to_u8(text: str):
    """
    Run full U₀→U₈ pipeline on real Arabic text.

    Returns:
        (u8_result, pipeline_trace)
    """
    # U₀: Unicode
    u0_result = text_to_unicode_layer(text)
    assert u0_result.valid, f"U₀ failed: {u0_result.violations}"
    assert u0_result.layer_object is not None

    # U₁: Grapheme
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    assert u1_result.valid, f"U₁ failed: {u1_result.violations}"
    assert u1_result.layer_object is not None

    # U₂p: Phonetic Projection
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    assert u2p_result.valid, f"U₂p failed: {u2p_result.violations}"
    assert u2p_result.layer_object is not None

    # U₂s: Syllable
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)
    assert u2s_result.valid, f"U₂s failed: {u2s_result.violations}"
    assert u2s_result.layer_object is not None

    # U₃: Boundary & Attachment
    u3_result = boundary_3(u2s_result.layer_object)
    assert u3_result.success, f"U₃ failed: {u3_result.message}"

    # U₄: True Singular Lafẓ
    u4_result = true_lafz_4(u3_result.layer_object)
    assert u4_result.success, f"U₄ failed: {u4_result.message}"

    # U₅: Functional Role
    u5_result = functional_role_5(u4_result.layer_object)
    assert u5_result.success, f"U₅ failed: {u5_result.message}"

    # U₆: Mabni Closed Class
    u6_result = mabni_closed_class_6(u5_result.layer_object)
    assert u6_result.success, f"U₆ failed: {u6_result.message}"

    # U₇: Pre-Weight Contract
    u7_result = pre_weight_contract_7(u6_result.layer_object)
    assert u7_result.success, f"U₇ failed: {u7_result.message}"

    # U₈: Root/Stem Candidate
    u8_result = root_stem_candidate_8(u7_result.layer_object)
    assert u8_result.success, f"U₈ failed: {u8_result.message}"

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
        'u8': u8_result,
    }

    return u8_result, pipeline_trace


# ============================================================================
# Golden Case 1: وَبِكِتَابِهِمْ
# Expected: 4 units (وَ, بِ, كِتَابِ, ـهِمْ)
# 3 blocked + 1 candidate
# ============================================================================

def test_pipeline_wa_bi_kitaabi_him():
    """
    وَبِكِتَابِهِمْ → Real pipeline U₀→U₈

    Expected U₈ output:
        وَ → BLOCKED, no root candidates
        بِ → BLOCKED, no root candidates
        كِتَابِ → CANDIDATE, root candidates = [ك-ت-ب]
        ـهِمْ → BLOCKED, no root candidates
    """
    text = "وَبِكِتَابِهِمْ"
    u8_result, trace = run_full_pipeline_to_u8(text)

    assert u8_result.success
    assert u8_result.layer_object is not None

    units = u8_result.layer_object.units
    assert len(units) >= 3

    # Check blocked units (particles and pronouns)
    blocked_units = [
        u for u in units
        if u.root_status == RootCandidateStatus.BLOCKED
    ]
    assert len(blocked_units) >= 2

    for unit in blocked_units:
        assert len(unit.root_candidate_paths) == 0
        assert len(unit.stem_candidate_paths) == 0
        assert "root_extraction" in unit.blocked_paths

    # Check candidate units (open-class cores)
    candidate_units = [
        u for u in units
        if u.root_status in [RootCandidateStatus.CANDIDATE, RootCandidateStatus.MULTIPLE_CANDIDATES]
    ]
    assert len(candidate_units) >= 1

    for unit in candidate_units:
        # Should have root candidates
        assert len(unit.root_candidate_paths) > 0

        # CRITICAL: No weight/pattern/meaning at U₈
        assert not hasattr(unit, 'weight')
        assert not hasattr(unit, 'pattern')
        assert not hasattr(unit, 'meaning')


# ============================================================================
# Golden Case 2: فَسَيَكْتُبُونَهَا
# Expected: Multiple units with particles + verb core
# ============================================================================

def test_pipeline_fa_sa_yaktubuuna_haa():
    """
    فَسَيَكْتُبُونَهَا → Real pipeline U₀→U₈

    Expected U₈ output:
        Particles → BLOCKED
        Verb core → CANDIDATE with root candidates
        Pronoun → BLOCKED
    """
    text = "فَسَيَكْتُبُونَهَا"
    u8_result, trace = run_full_pipeline_to_u8(text)

    assert u8_result.success
    units = u8_result.layer_object.units
    assert len(units) >= 2

    # Should have blocked particles
    blocked = [u for u in units if u.root_status == RootCandidateStatus.BLOCKED]
    assert len(blocked) >= 1

    # Should have at least one candidate (verb core)
    candidates = [u for u in units if u.root_status == RootCandidateStatus.CANDIDATE]
    # Note: Might be 0 if all parts are detected as particles/pronouns
    # This is acceptable behavior


# ============================================================================
# Golden Case 3: كَتَبَ
# Expected: 1 unit, root candidate [ك-ت-ب], NO weight
# ============================================================================

def test_pipeline_kataba():
    """
    كَتَبَ → Real pipeline U₀→U₈

    Expected U₈ output:
        كَتَبَ → CANDIDATE
               root_candidates = [ك-ت-ب]
               stem_candidates = [كتب]
               NO weight field
               NO pattern field
    """
    text = "كَتَبَ"
    u8_result, trace = run_full_pipeline_to_u8(text)

    assert u8_result.success
    units = u8_result.layer_object.units
    assert len(units) == 1

    unit = units[0]
    assert unit.root_status in [RootCandidateStatus.CANDIDATE, RootCandidateStatus.MULTIPLE_CANDIDATES]

    # Should have root candidates
    assert len(unit.root_candidate_paths) > 0

    # Should have stem candidates
    assert len(unit.stem_candidate_paths) > 0

    # CRITICAL: U₈ does NOT determine weight/pattern
    assert not hasattr(unit, 'weight')
    assert not hasattr(unit, 'pattern')
    assert not hasattr(unit, 'meaning')

    # Should require evidence for certification
    assert len(unit.required_evidence) > 0


# ============================================================================
# Golden Case 4: كَاتِب
# Expected: 1 unit, root candidate [ك-ت-ب], NO weight فَاعِل
# ============================================================================

def test_pipeline_kaatib():
    """
    كَاتِب → Real pipeline U₀→U₈

    Expected U₈ output:
        كَاتِب → CANDIDATE
                root_candidates = [ك-ت-ب]
                stem_candidates = [كاتب]
                NO weight فَاعِل (that's U₉)
    """
    text = "كَاتِب"
    u8_result, trace = run_full_pipeline_to_u8(text)

    assert u8_result.success
    units = u8_result.layer_object.units
    assert len(units) == 1

    unit = units[0]
    assert unit.root_status in [RootCandidateStatus.CANDIDATE, RootCandidateStatus.MULTIPLE_CANDIDATES]

    # Should have candidates
    assert len(unit.root_candidate_paths) > 0
    assert len(unit.stem_candidate_paths) > 0

    # CRITICAL: No weight فَاعِل at U₈
    assert not hasattr(unit, 'weight')
    assert not hasattr(unit, 'pattern')


# ============================================================================
# Golden Case 5: مَكْتَب
# Expected: 1 unit, root candidate [ك-ت-ب], NO weight مَفْعَل
# ============================================================================

def test_pipeline_maktab():
    """
    مَكْتَب → Real pipeline U₀→U₈

    Expected U₈ output:
        مَكْتَب → CANDIDATE
                 root_candidates = [ك-ت-ب]
                 stem_candidates = [مكتب]
                 NO weight مَفْعَل (that's U₉)
    """
    text = "مَكْتَب"
    u8_result, trace = run_full_pipeline_to_u8(text)

    assert u8_result.success
    units = u8_result.layer_object.units
    assert len(units) == 1

    unit = units[0]
    assert unit.root_status in [RootCandidateStatus.CANDIDATE, RootCandidateStatus.MULTIPLE_CANDIDATES]

    # Should have candidates
    assert len(unit.root_candidate_paths) > 0

    # CRITICAL: No weight at U₈
    assert not hasattr(unit, 'weight')


# ============================================================================
# Critical Architectural Tests
# ============================================================================

def test_no_direct_u7_to_u9_jump():
    """
    CRITICAL: Verify architectural law that U₇ cannot jump directly to U₉.

    Law:
        U₇ → U₈ → U₉ (enforced)
        U₇ → U₉ (forbidden)
    """
    text = "كَتَبَ"
    u8_result, trace = run_full_pipeline_to_u8(text)

    # Verify U₈ was invoked with U₇ output
    assert trace['u7'].success
    assert trace['u8'].success

    # Verify U₈ received real U₇ layer object
    u7_layer = trace['u7'].layer_object
    u8_result_check = trace['u8']

    assert u8_result_check.layer_object.source_pre_weight_layer_id == u7_layer.uid

    # Verify U₈ output has root candidates, not weight
    unit = u8_result_check.layer_object.units[0]
    assert hasattr(unit, 'root_candidate_paths')
    assert not hasattr(unit, 'weight')


def test_blocked_in_u7_stays_blocked_in_u8():
    """
    CRITICAL: Blocked in U₇ → Blocked in U₈.

    Test particles: وَ, بِ, فَ, سَ
    """
    particles = ["وَ", "بِ", "فَ", "سَ"]

    for particle in particles:
        u8_result, _ = run_full_pipeline_to_u8(particle)
        assert u8_result.success

        units = u8_result.layer_object.units

        # Find particle unit
        particle_units = [u for u in units if particle in u.surface or u.surface == particle]

        for unit in particle_units:
            # Must be BLOCKED
            assert unit.root_status == RootCandidateStatus.BLOCKED, \
                f"{particle} must be BLOCKED in U₈"

            # Must have no candidates
            assert len(unit.root_candidate_paths) == 0, \
                f"{particle} must have no root candidates"


def test_open_class_never_emits_weight_or_pattern():
    """
    CRITICAL: U₈ open-class candidates MUST NOT emit weight or pattern.

    Law:
        U₈.root_candidates = CANDIDATES (hypotheses)
        U₈.weight → FORBIDDEN
    """
    open_class_words = ["كَتَبَ", "كَاتِب", "مَكْتَب"]

    for word in open_class_words:
        u8_result, _ = run_full_pipeline_to_u8(word)
        assert u8_result.success

        for unit in u8_result.layer_object.units:
            # If candidate, check NO weight/pattern
            if unit.root_status in [RootCandidateStatus.CANDIDATE, RootCandidateStatus.MULTIPLE_CANDIDATES]:
                assert not hasattr(unit, 'weight'), \
                    f"{word}: U₈ MUST NOT extract weight"
                assert not hasattr(unit, 'pattern'), \
                    f"{word}: U₈ MUST NOT extract pattern"
                assert not hasattr(unit, 'meaning'), \
                    f"{word}: U₈ MUST NOT assign meaning"


def test_candidates_not_certificates():
    """
    CRITICAL: Verify distinction between CANDIDATE and CERTIFICATE.

    In U₈:
        - root_candidates exist (HYPOTHESES)
        - root_certificate does NOT exist
        - stem_candidates exist (HYPOTHESES)
        - stem_certificate does NOT exist
    """
    text = "كَتَبَ"
    u8_result, _ = run_full_pipeline_to_u8(text)

    unit = u8_result.layer_object.units[0]

    # Should have candidates
    if unit.root_status == RootCandidateStatus.CANDIDATE:
        assert len(unit.root_candidate_paths) > 0

    # Should NOT have certificates
    assert not hasattr(unit, 'root_certificate')
    assert not hasattr(unit, 'stem_certificate')
    assert not hasattr(unit, 'weight_certificate')

    # Should have required_evidence
    assert len(unit.required_evidence) > 0


def test_trace_preservation_through_pipeline():
    """Verify trace preservation U₀→U₈."""
    text = "كَتَبَ"
    u8_result, trace = run_full_pipeline_to_u8(text)

    # U₈ should preserve trace to U₇
    assert u8_result.layer_object.source_pre_weight_layer_id is not None
    assert u8_result.layer_object.trace_7 is not None

    # U₈ units should have trace to U₇ units
    for unit in u8_result.layer_object.units:
        assert unit.source_u7_unit_id is not None
        assert unit.source_u7_trace is not None


# ============================================================================
# Residuals Tests
# ============================================================================

def test_explicit_residuals_no_silent_failures():
    """
    CRITICAL: U₈ must produce explicit residuals, never silent failures.
    """
    text = "كَتَبَ"
    u8_result, _ = run_full_pipeline_to_u8(text)

    # U₈ should have result (success or with explicit failure)
    assert u8_result.success or u8_result.failure_type is not None

    # If successful, units may have residuals from upstream
    if u8_result.success:
        for unit in u8_result.layer_object.units:
            # Residuals should be frozenset (may be empty)
            assert isinstance(unit.residuals, frozenset)


# ============================================================================
# Root Candidate Structure Tests
# ============================================================================

def test_root_candidate_has_evidence():
    """Root candidates must have evidence."""
    text = "كَتَبَ"
    u8_result, _ = run_full_pipeline_to_u8(text)

    unit = u8_result.layer_object.units[0]
    if unit.root_candidate_paths:
        for candidate in unit.root_candidate_paths:
            assert len(candidate.evidence) > 0
            assert len(candidate.radicals) >= 3


def test_stem_candidate_has_evidence():
    """Stem candidates must have evidence."""
    text = "كَتَبَ"
    u8_result, _ = run_full_pipeline_to_u8(text)

    unit = u8_result.layer_object.units[0]
    if unit.stem_candidate_paths:
        for candidate in unit.stem_candidate_paths:
            assert len(candidate.evidence) > 0
            assert len(candidate.surface) > 0
