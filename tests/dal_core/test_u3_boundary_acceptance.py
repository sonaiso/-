"""
U₃ Boundary Detection Acceptance Tests - Comprehensive

Tests the acceptance criteria specified for U₃ closure after PR #98.

All tests MUST pass for U₃ to be considered closed.

Critical test cases:
1. كَتَبَ → 1 unit (standalone_core)
2. بِكِتَابٍ → بِـ + كِتَابٍ (2 units)
3. وَبِكِتَابِهِمْ → وَ + بِـ + كِتَابِ + ـهِمْ (4 units)
4. فَسَيَكْتُبُونَهَا → فـ + سـ + يَكْتُبُونَ + ـهَا (4 units)
5. كَاتِب → 1 unit (no false split on كَ)
6. مَكْتَب → 1 unit (no false prefix on مَ)

Architectural law tested:
    Phonetic surface ≠ Orthographic boundary surface
"""

from dal_core.u0_unicode_carrier import text_to_unicode_layer
from dal_core.u1_grapheme_carrier import unicode_to_grapheme_layer
from dal_core.u2p_phonetic_projection import grapheme_to_phonetic_layer
from dal_core.u2s_syllable_carrier import phonetic_to_syllable_layer
from dal_core.u3_boundary_attachment_carrier import (
    boundary_3,
    BoundaryUnitType,
    AttachmentType
)


def full_u0_to_u3_pipeline(text: str):
    """Run full U₀→U₁→U₂p→U₂s→U₃ pipeline."""
    u0 = text_to_unicode_layer(text)
    u1 = unicode_to_grapheme_layer(u0.layer_object)
    u2p = grapheme_to_phonetic_layer(u1.layer_object)
    u2s = phonetic_to_syllable_layer(u2p.layer_object)
    u3 = boundary_3(u2s.layer_object)
    return u0, u1, u2p, u2s, u3


# ============================================================================
# Test 1: كَتَبَ (simple verb - standalone core)
# ============================================================================

def test_kataba_standalone_core():
    """
    Test: كَتَبَ (he wrote)
    Expected: 1 unit (standalone_core)
    Reason: Simple trilateral verb, no proclitics/enclitics
    """
    text = "كَتَبَ"
    _, _, _, _, u3_result = full_u0_to_u3_pipeline(text)

    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None

    units = u3_result.layer_object.units
    assert len(units) == 1, f"Expected 1 unit, got {len(units)}"

    unit = units[0]
    assert unit.surface == "كَتَبَ", f"Expected 'كَتَبَ', got '{unit.surface}'"
    assert unit.unit_type == BoundaryUnitType.STANDALONE_CORE
    assert unit.attachment_type == AttachmentType.NO_ATTACHMENT

    print(f"✓ Test passed: {text} → 1 standalone_core")


# ============================================================================
# Test 2: بِكِتَابٍ (preposition + noun)
# ============================================================================

def test_bikitabin_proclitic_plus_core():
    """
    Test: بِكِتَابٍ (in a book)
    Expected: 2 units (بِـ + كِتَابٍ)
    Reason: بِ is attached proclitic (preposition), كِتَابٍ is core
    """
    text = "بِكِتَابٍ"
    _, _, _, _, u3_result = full_u0_to_u3_pipeline(text)

    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None

    units = u3_result.layer_object.units
    assert len(units) == 2, f"Expected 2 units, got {len(units)}"

    # First unit: بِ (attached proclitic)
    assert units[0].surface == "بِ", f"Expected 'بِ', got '{units[0].surface}'"
    assert units[0].unit_type == BoundaryUnitType.ATTACHED_PROCLITIC
    assert units[0].attachment_type == AttachmentType.PROCLITIC_TO_HOST

    # Second unit: كِتَابٍ (core)
    assert units[1].surface == "كِتَابٍ", f"Expected 'كِتَابٍ', got '{units[1].surface}'"
    assert units[1].unit_type == BoundaryUnitType.CORE_CANDIDATE
    assert units[1].attachment_type == AttachmentType.PROCLITIC_TO_HOST

    print(f"✓ Test passed: {text} → بِـ + كِتَابٍ")


# ============================================================================
# Test 3: وَبِكِتَابِهِمْ (conjunction + preposition + noun + pronoun) - CRITICAL
# ============================================================================

def test_wabikitabihim_full_segmentation():
    """
    Test: وَبِكِتَابِهِمْ (and in their book) - CRITICAL TEST CASE
    Expected: 4 units (وَ + بِـ + كِتَابِ + ـهِمْ)
    Reason:
        - وَ: standalone proclitic (conjunction)
        - بِـ: attached proclitic (preposition)
        - كِتَابِ: core (noun)
        - ـهِمْ: attached enclitic (pronoun 3mp genitive)

    This is the CRITICAL test case that was failing before orthographic reconstruction.
    """
    text = "وَبِكِتَابِهِمْ"
    _, _, _, _, u3_result = full_u0_to_u3_pipeline(text)

    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None

    units = u3_result.layer_object.units
    assert len(units) == 4, f"Expected 4 units, got {len(units)} - CRITICAL FAILURE"

    # First unit: وَ (standalone proclitic - conjunction)
    assert units[0].surface == "وَ", f"Expected 'وَ', got '{units[0].surface}'"
    assert units[0].unit_type == BoundaryUnitType.STANDALONE_PROCLITIC
    assert units[0].attachment_type == AttachmentType.NO_ATTACHMENT

    # Second unit: بِ (attached proclitic - preposition)
    assert units[1].surface == "بِ", f"Expected 'بِ', got '{units[1].surface}'"
    assert units[1].unit_type == BoundaryUnitType.ATTACHED_PROCLITIC
    assert units[1].attachment_type == AttachmentType.PROCLITIC_TO_HOST

    # Third unit: كِتَابِ (core - noun)
    assert units[2].surface == "كِتَابِ", f"Expected 'كِتَابِ', got '{units[2].surface}'"
    assert units[2].unit_type == BoundaryUnitType.CORE_CANDIDATE
    assert units[2].attachment_type == AttachmentType.BOTH_SIDES

    # Fourth unit: هِمْ (attached enclitic - pronoun)
    assert units[3].surface == "هِمْ", f"Expected 'هِمْ', got '{units[3].surface}'"
    assert units[3].unit_type == BoundaryUnitType.ATTACHED_ENCLITIC
    assert units[3].attachment_type == AttachmentType.ENCLITIC_TO_HOST

    print(f"✓ Test passed: {text} → وَ + بِـ + كِتَابِ + ـهِمْ (CRITICAL)")


# ============================================================================
# Test 4: فَسَيَكْتُبُونَهَا (future verb with proclitics and enclitic)
# ============================================================================

def test_fasayaktubunaha_complex_segmentation():
    """
    Test: فَسَيَكْتُبُونَهَا (and they will write it)
    Expected: 4 units (فـ + سـ + يَكْتُبُونَ + ـهَا)
    Reason:
        - فَ: standalone proclitic (conjunction)
        - سَـ: attached proclitic (future marker)
        - يَكْتُبُونَ: core (verb)
        - ـهَا: attached enclitic (pronoun 3fs)
    """
    text = "فَسَيَكْتُبُونَهَا"
    _, _, _, _, u3_result = full_u0_to_u3_pipeline(text)

    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None

    units = u3_result.layer_object.units
    assert len(units) == 4, f"Expected 4 units, got {len(units)}"

    # First unit: فَ (standalone proclitic - conjunction)
    assert units[0].surface == "فَ", f"Expected 'فَ', got '{units[0].surface}'"
    assert units[0].unit_type == BoundaryUnitType.STANDALONE_PROCLITIC

    # Second unit: سَ (attached proclitic - future marker)
    assert units[1].surface == "سَ", f"Expected 'سَ', got '{units[1].surface}'"
    assert units[1].unit_type == BoundaryUnitType.ATTACHED_PROCLITIC

    # Third unit: يَكْتُبُونَ (core - verb)
    assert units[2].surface == "يَكْتُبُونَ", f"Expected 'يَكْتُبُونَ', got '{units[2].surface}'"
    assert units[2].unit_type == BoundaryUnitType.CORE_CANDIDATE

    # Fourth unit: هَا (attached enclitic - pronoun)
    assert units[3].surface == "هَا", f"Expected 'هَا', got '{units[3].surface}'"
    assert units[3].unit_type == BoundaryUnitType.ATTACHED_ENCLITIC

    print(f"✓ Test passed: {text} → فـ + سـ + يَكْتُبُونَ + ـهَا")


# ============================================================================
# Test 5: كَاتِب (active participle - no false split)
# ============================================================================

def test_kaatib_no_false_split():
    """
    Test: كَاتِب (writer/author)
    Expected: 1 unit (standalone_core)
    Reason: كَ is NOT a proclitic here, it's part of the pattern فَاعِل

    This tests that U₃ does NOT falsely detect كَ as a proclitic.
    """
    text = "كَاتِب"
    _, _, _, _, u3_result = full_u0_to_u3_pipeline(text)

    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None

    units = u3_result.layer_object.units
    assert len(units) == 1, f"Expected 1 unit (no false split), got {len(units)}"

    unit = units[0]
    assert unit.surface == "كَاتِب", f"Expected 'كَاتِب', got '{unit.surface}'"
    assert unit.unit_type == BoundaryUnitType.STANDALONE_CORE

    print(f"✓ Test passed: {text} → 1 core (no false split on كَ)")


# ============================================================================
# Test 6: مَكْتَب (noun - no false prefix)
# ============================================================================

def test_maktab_no_false_prefix():
    """
    Test: مَكْتَب (office/desk)
    Expected: 1 unit (standalone_core)
    Reason: مَ is NOT a proclitic, it's part of the pattern مَفْعَل

    This tests that U₃ does NOT falsely detect مَ as a prefix.
    """
    text = "مَكْتَب"
    _, _, _, _, u3_result = full_u0_to_u3_pipeline(text)

    assert u3_result.success, f"U₃ failed for {text}"
    assert u3_result.layer_object is not None

    units = u3_result.layer_object.units
    assert len(units) == 1, f"Expected 1 unit (no false prefix), got {len(units)}"

    unit = units[0]
    assert unit.surface == "مَكْتَب", f"Expected 'مَكْتَب', got '{unit.surface}'"
    assert unit.unit_type == BoundaryUnitType.STANDALONE_CORE

    print(f"✓ Test passed: {text} → 1 core (no false prefix on مَ)")


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("U₃ Boundary Detection Acceptance Tests")
    print("Orthographic Surface Reconstruction - Post PR #98")
    print("=" * 70)
    print()

    tests = [
        ("كَتَبَ (standalone verb)", test_kataba_standalone_core),
        ("بِكِتَابٍ (proclitic + noun)", test_bikitabin_proclitic_plus_core),
        ("وَبِكِتَابِهِمْ (CRITICAL)", test_wabikitabihim_full_segmentation),
        ("فَسَيَكْتُبُونَهَا (complex)", test_fasayaktubunaha_complex_segmentation),
        ("كَاتِب (no false split)", test_kaatib_no_false_split),
        ("مَكْتَب (no false prefix)", test_maktab_no_false_prefix),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test FAILED: {name}")
            print(f"  Error: {str(e)}")
            failed += 1
        except Exception as e:
            print(f"✗ Test ERROR: {name}")
            print(f"  Exception: {str(e)}")
            failed += 1

    print()
    print("=" * 70)
    print(f"Acceptance Tests: {passed} passed, {failed} failed")
    print("=" * 70)

    if failed == 0:
        print()
        print("✅ U₃ CLOSURE STATUS: ALL ACCEPTANCE CRITERIA MET")
        print("   U₃ is now CLOSED over real U₂s output.")
        print("   Ready to proceed to U₄ TrueSingularLafẓ.")
    else:
        print()
        print("❌ U₃ CLOSURE STATUS: BLOCKED")
        print(f"   {failed} acceptance test(s) failed.")
        print("   U₃ NOT closed - fix failing tests before proceeding to U₄.")
