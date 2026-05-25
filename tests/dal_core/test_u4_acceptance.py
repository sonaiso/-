"""
U₄ True Singular Lafẓ Acceptance Tests - Comprehensive

Tests the acceptance criteria specified for U₄ implementation.

All tests MUST pass for U₄ to be considered closed.

Critical test cases:
1. كَتَبَ → 1 TRUE_SINGULAR_CORE_CANDIDATE
2. كَاتِب → 1 TRUE_SINGULAR_CORE_CANDIDATE (no false split)
3. مَكْتَب → 1 TRUE_SINGULAR_CORE_CANDIDATE (no false prefix)
4. بِكِتَابٍ → بِـ (BOUND_PROCLITIC) + كِتَابٍ (TRUE_SINGULAR_CORE_CANDIDATE)
5. وَبِكِتَابِهِمْ → وَ + بِـ (BOUND_PROCLITIC) + كِتَابِ (TRUE_SINGULAR_CORE_CANDIDATE) + ـهِمْ (ATTACHED_PRONOUN_CANDIDATE)
6. فَسَيَكْتُبُونَهَا → فـ + سـ (BOUND_PROCLITIC) + يَكْتُبُونَ (TRUE_SINGULAR_CORE_CANDIDATE) + ـهَا (ATTACHED_PRONOUN_CANDIDATE)

Architectural law tested:
    U₃ BoundaryAndAttachment → U₄ TrueSingularLafẓ
    U₄ MUST NOT produce: root, weight, meaning, hukm, functional_role, iʿrab
"""

from dal_core.u0_unicode_carrier import text_to_unicode_layer
from dal_core.u1_grapheme_carrier import unicode_to_grapheme_layer
from dal_core.u2p_phonetic_projection import grapheme_to_phonetic_layer
from dal_core.u2s_syllable_carrier import phonetic_to_syllable_layer
from dal_core.u3_boundary_attachment_carrier import boundary_3
from dal_core.u4_true_singular_lafz_carrier import (
    true_lafz_4,
    TrueLafzUnitType
)


def full_u0_to_u4_pipeline(text: str):
    """Run full U₀→U₁→U₂p→U₂s→U₃→U₄ pipeline."""
    u0 = text_to_unicode_layer(text)
    u1 = unicode_to_grapheme_layer(u0.layer_object)
    u2p = grapheme_to_phonetic_layer(u1.layer_object)
    u2s = phonetic_to_syllable_layer(u2p.layer_object)
    u3 = boundary_3(u2s.layer_object)
    u4 = true_lafz_4(u3.layer_object)
    return u0, u1, u2p, u2s, u3, u4


# ============================================================================
# Test 1: كَتَبَ (simple verb - standalone core)
# ============================================================================

def test_kataba_single_core_candidate():
    """
    Test: كَتَبَ (he wrote)
    Expected: 1 unit → TRUE_SINGULAR_CORE_CANDIDATE
    Reason: Simple trilateral verb, no proclitics/enclitics
    """
    text = "كَتَبَ"
    _, _, _, _, u3_result, u4_result = full_u0_to_u4_pipeline(text)

    # Verify U₃ passed
    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None
    assert len(u3_result.layer_object.units) == 1

    # Verify U₄ passed
    assert u4_result.success, f"U₄ failed for {text}"
    assert u4_result.layer_object is not None

    units = u4_result.layer_object.units
    assert len(units) == 1, f"Expected 1 unit, got {len(units)}"

    unit = units[0]
    assert unit.surface == "كَتَبَ", f"Expected 'كَتَبَ', got '{unit.surface}'"
    assert unit.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE

    # Verify no forbidden fields
    assert not hasattr(unit, 'root'), "U₄ unit MUST NOT have 'root' field"
    assert not hasattr(unit, 'weight'), "U₄ unit MUST NOT have 'weight' field"
    assert not hasattr(unit, 'meaning'), "U₄ unit MUST NOT have 'meaning' field"
    assert not hasattr(unit, 'functional_role'), "U₄ unit MUST NOT have 'functional_role' field"
    assert not hasattr(unit, 'hukm'), "U₄ unit MUST NOT have 'hukm' field"

    print(f"✓ Test passed: {text} → 1 TRUE_SINGULAR_CORE_CANDIDATE")


# ============================================================================
# Test 2: كَاتِب (active participle - no false split)
# ============================================================================

def test_kaatib_no_false_split():
    """
    Test: كَاتِب (writer/scribe)
    Expected: 1 unit → TRUE_SINGULAR_CORE_CANDIDATE
    Reason: Active participle, كَ is NOT a proclitic here
    """
    text = "كَاتِب"
    _, _, _, _, u3_result, u4_result = full_u0_to_u4_pipeline(text)

    # Verify U₃ passed
    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None
    assert len(u3_result.layer_object.units) == 1, "كَاتِب should NOT be split"

    # Verify U₄ passed
    assert u4_result.success, f"U₄ failed for {text}"
    assert u4_result.layer_object is not None

    units = u4_result.layer_object.units
    assert len(units) == 1, f"Expected 1 unit, got {len(units)}"

    unit = units[0]
    assert unit.surface == "كَاتِب", f"Expected 'كَاتِب', got '{unit.surface}'"
    assert unit.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE

    print(f"✓ Test passed: {text} → 1 TRUE_SINGULAR_CORE_CANDIDATE (no false split)")


# ============================================================================
# Test 3: مَكْتَب (noun of place - no false prefix)
# ============================================================================

def test_maktab_no_false_prefix():
    """
    Test: مَكْتَب (office/desk)
    Expected: 1 unit → TRUE_SINGULAR_CORE_CANDIDATE
    Reason: Noun of place, مَ is NOT a separate proclitic
    """
    text = "مَكْتَب"
    _, _, _, _, u3_result, u4_result = full_u0_to_u4_pipeline(text)

    # Verify U₃ passed
    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None
    assert len(u3_result.layer_object.units) == 1, "مَكْتَب should NOT be split"

    # Verify U₄ passed
    assert u4_result.success, f"U₄ failed for {text}"
    assert u4_result.layer_object is not None

    units = u4_result.layer_object.units
    assert len(units) == 1, f"Expected 1 unit, got {len(units)}"

    unit = units[0]
    assert unit.surface == "مَكْتَب", f"Expected 'مَكْتَب', got '{unit.surface}'"
    assert unit.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE

    print(f"✓ Test passed: {text} → 1 TRUE_SINGULAR_CORE_CANDIDATE (no false prefix)")


# ============================================================================
# Test 4: بِكِتَابٍ (preposition + noun)
# ============================================================================

def test_bikitabin_proclitic_plus_core():
    """
    Test: بِكِتَابٍ (in a book)
    Expected: 2 units → بِـ (BOUND_PROCLITIC) + كِتَابٍ (TRUE_SINGULAR_CORE_CANDIDATE)
    Reason: بِ is preposition (bound proclitic), كِتَابٍ is core
    """
    text = "بِكِتَابٍ"
    _, _, _, _, u3_result, u4_result = full_u0_to_u4_pipeline(text)

    # Verify U₃ passed
    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None
    assert len(u3_result.layer_object.units) == 2

    # Verify U₄ passed
    assert u4_result.success, f"U₄ failed for {text}"
    assert u4_result.layer_object is not None

    units = u4_result.layer_object.units
    assert len(units) == 2, f"Expected 2 units, got {len(units)}"

    # First unit: بِ (BOUND_PROCLITIC)
    assert units[0].surface == "بِ", f"Expected 'بِ', got '{units[0].surface}'"
    assert units[0].unit_type == TrueLafzUnitType.BOUND_PROCLITIC

    # Second unit: كِتَابٍ (TRUE_SINGULAR_CORE_CANDIDATE)
    assert units[1].surface == "كِتَابٍ", f"Expected 'كِتَابٍ', got '{units[1].surface}'"
    assert units[1].unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE

    print(f"✓ Test passed: {text} → بِـ (BOUND_PROCLITIC) + كِتَابٍ (TRUE_SINGULAR_CORE_CANDIDATE)")


# ============================================================================
# Test 5: وَبِكِتَابِهِمْ (conjunction + preposition + noun + pronoun)
# ============================================================================

def test_wabikitabihim_full_composite():
    """
    Test: وَبِكِتَابِهِمْ (and with their book)
    Expected: 4 units
        - وَ → BOUND_PROCLITIC
        - بِـ → BOUND_PROCLITIC
        - كِتَابِ → TRUE_SINGULAR_CORE_CANDIDATE
        - ـهِمْ → ATTACHED_PRONOUN_CANDIDATE
    Reason: Multiple attachments around core
    """
    text = "وَبِكِتَابِهِمْ"
    _, _, _, _, u3_result, u4_result = full_u0_to_u4_pipeline(text)

    # Verify U₃ passed
    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None
    assert len(u3_result.layer_object.units) == 4

    # Verify U₄ passed
    assert u4_result.success, f"U₄ failed for {text}"
    assert u4_result.layer_object is not None

    units = u4_result.layer_object.units
    assert len(units) == 4, f"Expected 4 units, got {len(units)}"

    # Unit 1: وَ (BOUND_PROCLITIC)
    assert units[0].surface == "وَ", f"Expected 'وَ', got '{units[0].surface}'"
    assert units[0].unit_type == TrueLafzUnitType.BOUND_PROCLITIC

    # Unit 2: بِـ (BOUND_PROCLITIC)
    # Note: Could be بِ or بِـ depending on U₃ output
    assert units[1].surface in ["بِ", "بِـ"], f"Expected 'بِ' or 'بِـ', got '{units[1].surface}'"
    assert units[1].unit_type == TrueLafzUnitType.BOUND_PROCLITIC

    # Unit 3: كِتَابِ (TRUE_SINGULAR_CORE_CANDIDATE)
    assert units[2].surface == "كِتَابِ", f"Expected 'كِتَابِ', got '{units[2].surface}'"
    assert units[2].unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE

    # Unit 4: ـهِمْ (ATTACHED_PRONOUN_CANDIDATE)
    # Note: Could be ـهِمْ or هِمْ depending on U₃ output
    assert units[3].surface in ["ـهِمْ", "هِمْ"], f"Expected 'ـهِمْ' or 'هِمْ', got '{units[3].surface}'"
    assert units[3].unit_type == TrueLafzUnitType.ATTACHED_PRONOUN_CANDIDATE

    print(f"✓ Test passed: {text} → وَ + بِـ (BOUND_PROCLITIC) + كِتَابِ (CORE) + ـهِمْ (PRONOUN)")


# ============================================================================
# Test 6: فَسَيَكْتُبُونَهَا (conjunction + future + verb + pronoun)
# ============================================================================

def test_fasayaktubunaha_future_verb_composite():
    """
    Test: فَسَيَكْتُبُونَهَا (and they will write it)
    Expected: 4 units
        - فَ → BOUND_PROCLITIC
        - سَـ → BOUND_PROCLITIC
        - يَكْتُبُونَ → TRUE_SINGULAR_CORE_CANDIDATE
        - ـهَا → ATTACHED_PRONOUN_CANDIDATE
    Reason: Future verb with multiple proclitics and enclitic pronoun
    """
    text = "فَسَيَكْتُبُونَهَا"
    _, _, _, _, u3_result, u4_result = full_u0_to_u4_pipeline(text)

    # Verify U₃ passed
    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None
    assert len(u3_result.layer_object.units) == 4

    # Verify U₄ passed
    assert u4_result.success, f"U₄ failed for {text}"
    assert u4_result.layer_object is not None

    units = u4_result.layer_object.units
    assert len(units) == 4, f"Expected 4 units, got {len(units)}"

    # Unit 1: فَ (BOUND_PROCLITIC)
    assert units[0].surface == "فَ", f"Expected 'فَ', got '{units[0].surface}'"
    assert units[0].unit_type == TrueLafzUnitType.BOUND_PROCLITIC

    # Unit 2: سَـ (BOUND_PROCLITIC)
    # Note: Could be سَ or سَـ depending on U₃ output
    assert units[1].surface in ["سَ", "سَـ"], f"Expected 'سَ' or 'سَـ', got '{units[1].surface}'"
    assert units[1].unit_type == TrueLafzUnitType.BOUND_PROCLITIC

    # Unit 3: يَكْتُبُونَ (TRUE_SINGULAR_CORE_CANDIDATE)
    assert units[2].surface == "يَكْتُبُونَ", f"Expected 'يَكْتُبُونَ', got '{units[2].surface}'"
    assert units[2].unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE

    # Unit 4: ـهَا (ATTACHED_PRONOUN_CANDIDATE)
    # Note: Could be ـهَا or هَا depending on U₃ output
    assert units[3].surface in ["ـهَا", "هَا"], f"Expected 'ـهَا' or 'هَا', got '{units[3].surface}'"
    assert units[3].unit_type == TrueLafzUnitType.ATTACHED_PRONOUN_CANDIDATE

    print(f"✓ Test passed: {text} → فَ + سَـ (BOUND_PROCLITIC) + يَكْتُبُونَ (CORE) + ـهَا (PRONOUN)")


# ============================================================================
# Negative Test: Verify no forbidden fields in layer object
# ============================================================================

def test_u4_layer_no_forbidden_fields():
    """
    Test: U₄ layer object MUST NOT contain forbidden fields
    Forbidden: root, weight, meaning, hukm, functional_role, iʿrab
    """
    text = "كَتَبَ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    layer_obj = u4_result.layer_object
    assert layer_obj is not None

    # Check layer object has no forbidden fields
    assert not hasattr(layer_obj, 'root'), "U₄ layer MUST NOT have 'root' field"
    assert not hasattr(layer_obj, 'weight'), "U₄ layer MUST NOT have 'weight' field"
    assert not hasattr(layer_obj, 'meaning'), "U₄ layer MUST NOT have 'meaning' field"
    assert not hasattr(layer_obj, 'hukm'), "U₄ layer MUST NOT have 'hukm' field"
    assert not hasattr(layer_obj, 'functional_role'), "U₄ layer MUST NOT have 'functional_role' field"
    assert not hasattr(layer_obj, 'iʿrab'), "U₄ layer MUST NOT have 'iʿrab' field"
    assert not hasattr(layer_obj, 'i3rab'), "U₄ layer MUST NOT have 'i3rab' field"

    # Check all units have no forbidden fields
    for unit in layer_obj.units:
        assert not hasattr(unit, 'root'), f"Unit '{unit.surface}' MUST NOT have 'root' field"
        assert not hasattr(unit, 'weight'), f"Unit '{unit.surface}' MUST NOT have 'weight' field"
        assert not hasattr(unit, 'meaning'), f"Unit '{unit.surface}' MUST NOT have 'meaning' field"
        assert not hasattr(unit, 'hukm'), f"Unit '{unit.surface}' MUST NOT have 'hukm' field"
        assert not hasattr(unit, 'functional_role'), f"Unit '{unit.surface}' MUST NOT have 'functional_role' field"

    print("✓ Test passed: U₄ has no forbidden fields (root, weight, meaning, hukm, functional_role, iʿrab)")


# ============================================================================
# Proof Test: Verify ProofObject forbidden gates
# ============================================================================

def test_u4_proof_forbidden_gates():
    """
    Test: U₄ ProofObject MUST forbid direct jumps to U₅+
    Forbidden gates: root_certificate, weight_certificate, meaning_certificate, hukm_certificate, i3rab_certificate
    Allowed gate: functional_role_gate (U₅)
    """
    text = "كَتَبَ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    layer_obj = u4_result.layer_object
    assert layer_obj is not None
    assert layer_obj.proof is not None

    proof = layer_obj.proof

    # Verify allowed next gate
    assert "functional_role_gate" in proof.allowed_next_gates, \
        "U₄ MUST allow transition to U₅ FunctionalRole"

    # Verify forbidden gates
    forbidden = proof.forbidden_next_gates
    assert "root_certificate" in forbidden, "U₄ MUST forbid direct jump to root"
    assert "weight_certificate" in forbidden, "U₄ MUST forbid direct jump to weight"
    assert "meaning_certificate" in forbidden, "U₄ MUST forbid direct jump to meaning"
    assert "hukm_certificate" in forbidden, "U₄ MUST forbid direct jump to hukm"
    assert "i3rab_certificate" in forbidden, "U₄ MUST forbid direct jump to i3rab"

    print("✓ Test passed: U₄ ProofObject correctly forbids direct jumps to U₈/U₉/U₁₅")


# ============================================================================
# Run all tests
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("U₄ True Singular Lafẓ - Acceptance Tests")
    print("=" * 70)
    print()

    test_kataba_single_core_candidate()
    test_kaatib_no_false_split()
    test_maktab_no_false_prefix()
    test_bikitabin_proclitic_plus_core()
    test_wabikitabihim_full_composite()
    test_fasayaktubunaha_future_verb_composite()
    test_u4_layer_no_forbidden_fields()
    test_u4_proof_forbidden_gates()

    print()
    print("=" * 70)
    print("ALL U₄ ACCEPTANCE TESTS PASSED ✓")
    print("=" * 70)
