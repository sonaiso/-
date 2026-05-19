"""
Tests for ArabicAtom Contract (عقد الذرة العربية)

Theorem 1 & 2: Letters and vowels must be classified through contracts
"""

import pytest
from dal_core.carriers import make_carrier
from dal_core.atoms import (
    ArabicAtom, AtomKind, classify_carrier,
    carriers_to_atoms, ARABIC_LETTERS, ARABIC_MARKS
)
from dal_core.residuals import ResidualType


class TestArabicAtomContract:
    """Test Contract 2: Carrier → ArabicAtom"""

    def test_letter_classification(self):
        """Letters are classified as AtomKind.LETTER"""
        carrier, _ = make_carrier('ك', 0)
        atom, residuals = classify_carrier(carrier)

        assert atom.kind == AtomKind.LETTER
        assert atom.carrier.char == 'ك'
        assert 'name' in atom.features
        assert atom.rank == 1.0
        assert not any(r.is_blocker() for r in residuals)

    def test_vowel_classification(self):
        """
        المبرهنة: الحركة ليست حرفًا
        Vowels are NOT letters
        """
        carrier, _ = make_carrier('\u064E', 0)  # fatha
        atom, _ = classify_carrier(carrier)

        assert atom.kind == AtomKind.VOWEL
        assert atom.kind != AtomKind.LETTER
        assert atom.is_vowel()
        assert not atom.is_letter()

    def test_sukun_classification(self):
        """Sukun is classified separately"""
        carrier, _ = make_carrier('\u0652', 0)  # sukun
        atom, _ = classify_carrier(carrier)

        assert atom.kind == AtomKind.SUKUN
        assert atom.kind != AtomKind.LETTER
        assert atom.kind != AtomKind.VOWEL

    def test_shadda_classification(self):
        """Shadda is classified separately"""
        carrier, _ = make_carrier('\u0651', 0)  # shadda
        atom, _ = classify_carrier(carrier)

        assert atom.kind == AtomKind.SHADDA
        assert atom.kind != AtomKind.LETTER

    def test_tanwin_classification(self):
        """Tanwin is classified as TANWIN kind"""
        carrier, _ = make_carrier('\u064B', 0)  # fathatan
        atom, _ = classify_carrier(carrier)

        assert atom.kind == AtomKind.TANWIN
        assert atom.is_mark()

    def test_all_letters_classified(self):
        """All 28+ Arabic letters are classified"""
        for char in ARABIC_LETTERS:
            carrier, _ = make_carrier(char, 0)
            atom, residuals = classify_carrier(carrier)

            assert atom.kind == AtomKind.LETTER
            assert not any(r.is_blocker() for r in residuals)

    def test_all_marks_classified(self):
        """All diacritics are classified"""
        for char in ARABIC_MARKS:
            carrier, _ = make_carrier(char, 0)
            atom, residuals = classify_carrier(carrier)

            assert atom.kind in {AtomKind.VOWEL, AtomKind.SUKUN,
                                 AtomKind.SHADDA, AtomKind.TANWIN,
                                 AtomKind.MARK}
            assert not any(r.is_blocker() for r in residuals)

    def test_unknown_atom_blocker(self):
        """Unknown characters produce BLOCKER residuals"""
        carrier, _ = make_carrier('🔥', 0)
        atom, residuals = classify_carrier(carrier)

        assert atom.kind == AtomKind.UNKNOWN
        assert atom.rank == 0.0
        blockers = [r for r in residuals if r.is_blocker()]
        assert len(blockers) > 0
        assert blockers[0].type == ResidualType.UNKNOWN_ATOM

    def test_atom_has_evidence(self):
        """Every atom has evidence for its classification"""
        carrier, _ = make_carrier('ت', 0)
        atom, _ = classify_carrier(carrier)

        assert len(atom.evidence) > 0
        assert atom.evidence[0].source is not None
        assert atom.evidence[0].reason is not None

    def test_atom_not_number(self):
        """
        ك ≠ "number 22"
        ك = Atom with recoverable features
        """
        carrier, _ = make_carrier('ك', 0)
        atom, _ = classify_carrier(carrier)

        # It's not just a number
        assert isinstance(atom, ArabicAtom)
        assert atom.features is not None
        assert atom.evidence is not None
        # Features are recoverable
        assert 'name' in atom.features
        assert len(atom.evidence) > 0

    def test_vocalized_word_to_atoms(self):
        """Convert vocalized word to atom sequence"""
        from dal_core.carriers import text_to_carriers

        carriers, _ = text_to_carriers("كَتَبَ")
        atoms, residuals = carriers_to_atoms(carriers)

        # Should have 6 atoms: ك َ ت َ ب َ
        assert len(atoms) == 6
        assert atoms[0].kind == AtomKind.LETTER  # ك
        assert atoms[1].kind == AtomKind.VOWEL   # َ
        assert atoms[2].kind == AtomKind.LETTER  # ت
        assert atoms[3].kind == AtomKind.VOWEL   # َ
        assert atoms[4].kind == AtomKind.LETTER  # ب
        assert atoms[5].kind == AtomKind.VOWEL   # َ

    def test_atom_is_mark_predicate(self):
        """Test is_mark() predicate"""
        carrier_vowel, _ = make_carrier('\u064E', 0)
        atom_vowel, _ = classify_carrier(carrier_vowel)
        assert atom_vowel.is_mark()

        carrier_letter, _ = make_carrier('ب', 0)
        atom_letter, _ = classify_carrier(carrier_letter)
        assert not atom_letter.is_mark()
