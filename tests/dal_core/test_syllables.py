"""
Tests for Syllable Contract expansion

Covers CV/CVC/CVV/CVVC/CVCC patterns and special handling
for shadda, tanwin, madd, and sukun.
"""

import pytest
from dal_core.syllables import (
    Syllable,
    SyllableType,
    handle_shadda,
    handle_tanwin,
    handle_sukun,
    handle_madd,
    is_long_vowel_sequence,
    parse_syllables,
    validate_syllable_pattern
)
from dal_core.atoms import ArabicAtom, AtomKind, classify_carrier
from dal_core.carriers import Carrier, make_carrier


class TestSyllableTypes:
    """Test syllable type enumeration"""

    def test_syllable_types_exist(self):
        """All required syllable types are defined"""
        assert SyllableType.CV
        assert SyllableType.CVC
        assert SyllableType.CVV
        assert SyllableType.CVVC
        assert SyllableType.CVCC


class TestShaddaHandling:
    """Test shadda (gemination) handling"""

    def test_shadda_trace(self):
        """Shadda produces trace with gemination info"""
        # Create shadda atom
        carrier_shadda, _ = make_carrier('\u0651', 0)  # shadda
        atom_shadda, _ = classify_carrier(carrier_shadda)

        # Create base letter
        carrier_base, _ = make_carrier('ر', 0)
        atom_base, _ = classify_carrier(carrier_base)

        # Handle shadda
        result, trace = handle_shadda(atom_shadda, atom_base)

        # Verify trace
        assert trace['effect'] == 'gemination'
        assert trace['base_letter'] == 'ر'
        assert 'shadda_position' in trace

    def test_non_shadda_returns_empty_trace(self):
        """Non-shadda atoms return empty trace"""
        carrier, _ = make_carrier('ك', 0)
        atom, _ = classify_carrier(carrier)

        carrier_base, _ = make_carrier('ت', 0)
        atom_base, _ = classify_carrier(carrier_base)

        result, trace = handle_shadda(atom, atom_base)

        assert trace == {}


class TestTanwinHandling:
    """Test tanwin (nunation) handling"""

    def test_tanwin_operational_trace(self):
        """Tanwin produces operational trace (not semantic)"""
        # Create tanwin atom
        carrier, _ = make_carrier('\u064B', 0)  # fathatan
        atom, _ = classify_carrier(carrier)

        # Handle tanwin
        result, trace = handle_tanwin(atom)

        # Verify trace shows operational nature
        assert trace['effect'] == 'nunation marker'
        assert trace['operational'] is True
        assert 'tanwin_type' in trace

    def test_non_tanwin_returns_empty_trace(self):
        """Non-tanwin atoms return empty trace"""
        carrier, _ = make_carrier('ب', 0)
        atom, _ = classify_carrier(carrier)

        result, trace = handle_tanwin(atom)

        assert trace == {}


class TestSukunHandling:
    """Test sukun handling"""

    def test_sukun_closes_syllable(self):
        """Sukun in coda position is valid (closes syllable)"""
        carrier, _ = make_carrier('\u0652', 0)  # sukun
        atom, _ = classify_carrier(carrier)

        # Sukun in coda position (valid)
        residuals = handle_sukun(atom, 'coda')

        # No residuals (valid position)
        assert len(residuals) == 0

    def test_sukun_onset_invalid(self):
        """Sukun in onset position produces blocker"""
        carrier, _ = make_carrier('\u0652', 0)  # sukun
        atom, _ = classify_carrier(carrier)

        # Sukun in onset position (invalid)
        residuals = handle_sukun(atom, 'onset')

        # Should have blocker residual
        assert len(residuals) > 0
        assert any(r.is_blocker() for r in residuals)

    def test_non_sukun_returns_empty(self):
        """Non-sukun atoms return no residuals"""
        carrier, _ = make_carrier('م', 0)
        atom, _ = classify_carrier(carrier)

        residuals = handle_sukun(atom, 'onset')

        assert len(residuals) == 0


class TestMaddHandling:
    """Test madd (long vowel) handling"""

    def test_madd_lengthens_syllable(self):
        """Madd produces lengthened nucleus trace"""
        # Create fatha + alif sequence (madd)
        carrier_fatha, _ = make_carrier('\u064E', 0)  # fatha
        atom_fatha, _ = classify_carrier(carrier_fatha)

        carrier_alif, _ = make_carrier('ا', 1)  # alif
        atom_alif, _ = classify_carrier(carrier_alif)

        atoms = [atom_fatha, atom_alif]

        # Handle madd
        nucleus_atoms, trace = handle_madd(atoms, 0)

        # Verify lengthening
        assert len(nucleus_atoms) == 2
        assert trace['effect'] == 'syllable lengthening'
        assert 'madd_type' in trace

    def test_is_long_vowel_sequence_fatha_alif(self):
        """Fatha + alif is recognized as long vowel"""
        carrier_fatha, _ = make_carrier('\u064E', 0)
        atom_fatha, _ = classify_carrier(carrier_fatha)

        carrier_alif, _ = make_carrier('ا', 1)
        atom_alif, _ = classify_carrier(carrier_alif)

        atoms = [atom_fatha, atom_alif]

        assert is_long_vowel_sequence(atoms, 0) is True

    def test_is_long_vowel_sequence_damma_waw(self):
        """Damma + waw is recognized as long vowel"""
        carrier_damma, _ = make_carrier('\u064F', 0)
        atom_damma, _ = classify_carrier(carrier_damma)

        carrier_waw, _ = make_carrier('و', 1)
        atom_waw, _ = classify_carrier(carrier_waw)

        atoms = [atom_damma, atom_waw]

        assert is_long_vowel_sequence(atoms, 0) is True

    def test_is_long_vowel_sequence_kasra_ya(self):
        """Kasra + ya is recognized as long vowel"""
        carrier_kasra, _ = make_carrier('\u0650', 0)
        atom_kasra, _ = classify_carrier(carrier_kasra)

        carrier_ya, _ = make_carrier('ي', 1)
        atom_ya, _ = classify_carrier(carrier_ya)

        atoms = [atom_kasra, atom_ya]

        assert is_long_vowel_sequence(atoms, 0) is True

    def test_non_madd_sequence_returns_single_atom(self):
        """Non-madd sequence returns single atom"""
        carrier, _ = make_carrier('\u064E', 0)  # fatha alone
        atom, _ = classify_carrier(carrier)

        atoms = [atom]

        nucleus_atoms, trace = handle_madd(atoms, 0)

        assert len(nucleus_atoms) == 1
        assert trace == {}


class TestSyllableValidation:
    """Test syllable pattern validation"""

    def test_invalid_syllable_pattern_blocks_certificate(self):
        """Invalid syllable produces blocker residual"""
        # Empty syllable (invalid)
        syllable = Syllable(
            type=SyllableType.CV,
            onset=[],
            nucleus=[],
            coda=[]
        )

        residuals = validate_syllable_pattern(syllable)

        # Should have blocker
        assert len(residuals) > 0
        assert any(r.is_blocker() for r in residuals)

    def test_valid_syllable_no_blocker(self):
        """Valid syllable produces no blocker"""
        # Create valid CV syllable
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        syllable = Syllable(
            type=SyllableType.CV,
            onset=[atom_k],
            nucleus=[atom_a],
            coda=[]
        )

        residuals = validate_syllable_pattern(syllable)

        # No blockers for valid structure
        blockers = [r for r in residuals if r.is_blocker()]
        assert len(blockers) == 0


class TestSyllableReconstruction:
    """Test syllable text reconstruction"""

    def test_to_text_reconstructs_syllable(self):
        """Syllable.to_text() reconstructs original text"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        syllable = Syllable(
            type=SyllableType.CV,
            onset=[atom_k],
            nucleus=[atom_a]
        )

        text = syllable.to_text()

        assert 'ك' in text
        assert '\u064E' in text
