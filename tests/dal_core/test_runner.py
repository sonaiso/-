#!/usr/bin/env python3
"""
Simple test runner for dal_core without pytest dependency
"""

import sys
sys.path.insert(0, 'src')

from dal_core.carriers import make_carrier, text_to_carriers
from dal_core.atoms import classify_carrier, AtomKind
from dal_core.residuals import ResidualType

def test_unicode_not_letter():
    """Test that Unicode ≠ Letter"""
    char = 'ك'
    carrier, _ = make_carrier(char, 0)
    assert carrier.char == 'ك'
    assert carrier.codepoint == 0x0643
    print("✓ test_unicode_not_letter passed")

def test_vowel_classification():
    """Test that vowel ≠ letter"""
    carrier, _ = make_carrier('\u064E', 0)  # fatha
    atom, _ = classify_carrier(carrier)
    assert atom.kind == AtomKind.VOWEL
    assert atom.kind != AtomKind.LETTER
    print("✓ test_vowel_classification passed")

def test_letter_classification():
    """Test letter classification"""
    carrier, _ = make_carrier('ب', 0)
    atom, _ = classify_carrier(carrier)
    assert atom.kind == AtomKind.LETTER
    assert atom.is_letter()
    assert not atom.is_vowel()
    print("✓ test_letter_classification passed")

def test_vocalized_word():
    """Test vocalized word parsing"""
    carriers, _ = text_to_carriers("كَتَبَ")
    assert len(carriers) == 6  # 3 letters + 3 vowels
    print("✓ test_vocalized_word passed")

def test_non_arabic_blocker():
    """Test non-Arabic produces blocker"""
    carrier, residuals = make_carrier('A', 0)
    blockers = [r for r in residuals if r.is_blocker()]
    assert len(blockers) > 0
    assert blockers[0].type == ResidualType.NON_ARABIC_SYMBOL
    print("✓ test_non_arabic_blocker passed")

def test_dclosed_enforces_no_meaning():
    """
    Test DClosed enforces meaning=None via field absence.

    Theorem 5: لا معنى داخل الدال
    DClosed must NOT contain fields: meaning, murad, haqiqa_majaz
    """
    from dal_core.d_mufrad import DClosed
    from dal_core.d_type import TypedDal, DalType
    from dal_core.d_lugha import LughaAttestation, LughaRank
    from dal_core.d_form import FormCandidate
    from dal_core.ranks import FormRank

    form = FormCandidate(text="test", vocalization="test", rank=FormRank.FORM)
    attestation = LughaAttestation(form=form, rank=LughaRank.TAWATUR, is_arabic=True)
    typed_dal = TypedDal(attestation=attestation, dal_type=DalType.ISM)

    d = DClosed(typed_dal=typed_dal)

    # Fields must be absent (not just None)
    assert not hasattr(d, "meaning"), "DClosed must not have 'meaning' field"
    assert not hasattr(d, "murad"), "DClosed must not have 'murad' field"
    assert not hasattr(d, "haqiqa_majaz"), "DClosed must not have 'haqiqa_majaz' field"

    print("✓ test_dclosed_enforces_no_meaning passed")

def main():
    """Run all tests"""
    print("Running dal_core tests...\n")

    tests = [
        test_unicode_not_letter,
        test_vowel_classification,
        test_letter_classification,
        test_vocalized_word,
        test_non_arabic_blocker,
        test_dclosed_enforces_no_meaning,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
