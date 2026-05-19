"""
Tests for Carrier Contract (عقد الحامل)

Theorem 1: لا Unicode بلا عقد
Unicode is not a letter; it must pass through Carrier contract.
"""

import pytest
from dal_core.carriers import Carrier, make_carrier, text_to_carriers
from dal_core.residuals import ResidualSeverity, ResidualType


class TestCarrierContract:
    """Test Contract 1: Unicode → Carrier"""

    def test_unicode_is_not_letter(self):
        """
        المبرهنة 1: Unicode ≠ حرف
        A Unicode character is NOT a letter until classified
        """
        # Raw string 'ك' is NOT an ArabicAtom
        char = 'ك'
        assert not isinstance(char, object)  # It's just a string

        # It becomes a Carrier through the contract
        carrier, residuals = make_carrier(char, 0)
        assert isinstance(carrier, Carrier)
        assert carrier.char == 'ك'
        assert carrier.codepoint == 0x0643

    def test_carrier_properties(self):
        """Test carrier has all required properties"""
        carrier, _ = make_carrier('ب', 5)
        assert carrier.char == 'ب'
        assert carrier.codepoint == 0x0628
        assert carrier.index == 5
        assert carrier.unicode_name is not None

    def test_arabic_block_detection(self):
        """Test detection of Arabic Unicode blocks"""
        carrier_arabic, _ = make_carrier('م', 0)
        assert carrier_arabic.is_arabic_block()

        carrier_latin, _ = make_carrier('A', 0)
        assert not carrier_latin.is_arabic_block()

    def test_non_arabic_symbol_residual(self):
        """Non-Arabic symbols produce BLOCKER residuals"""
        carrier, residuals = make_carrier('A', 0)
        assert len(residuals) > 0
        blocker = [r for r in residuals if r.is_blocker()]
        assert len(blocker) > 0
        assert blocker[0].type == ResidualType.NON_ARABIC_SYMBOL

    def test_text_to_carriers(self):
        """Convert text to carrier sequence"""
        carriers, residuals = text_to_carriers("كتب")
        assert len(carriers) == 3
        assert carriers[0].char == 'ك'
        assert carriers[1].char == 'ت'
        assert carriers[2].char == 'ب'

    def test_mixed_text_filters_non_arabic(self):
        """Mixed text filters out non-Arabic characters"""
        carriers, residuals = text_to_carriers("كتابX")
        # Should have 4 carriers (كتاب) and skip X
        assert len(carriers) == 4
        # Should have blocker residual for 'X'
        blockers = [r for r in residuals if r.is_blocker()]
        assert len(blockers) >= 1

    def test_carrier_index_tracking(self):
        """Carriers track their position in input"""
        carriers, _ = text_to_carriers("مكتبة")
        assert carriers[0].index == 0
        assert carriers[1].index == 1
        assert carriers[2].index == 2
        assert carriers[3].index == 3
        assert carriers[4].index == 4

    def test_whitespace_allowed(self):
        """Whitespace is allowed (not blocked)"""
        carrier, residuals = make_carrier(' ', 0)
        assert carrier is not None
        blockers = [r for r in residuals if r.is_blocker()]
        assert len(blockers) == 0
