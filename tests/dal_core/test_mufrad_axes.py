"""Tests for ``dal_core.mufrad_axes`` (PR-A).

These are intentionally minimal: PR-A introduces enums only. The tests
verify that the enums import, expose the required members, and have
human-readable Arabic values. Behavioral coverage lives in PR-C/D/E/G.
"""

import pytest

from dal_core.mufrad_axes import (
    BinaaJudgment,
    BinaaSubtype,
    IshtiqaqJudgment,
    JamidSubtype,
    MushtaqSubtype,
    SarfFlexibility,
)


class TestBinaaJudgment:
    def test_required_members(self):
        names = {m.name for m in BinaaJudgment}
        assert names == {"MABNI", "MUERAB", "UNRESOLVED", "NOT_APPLICABLE"}

    def test_values_are_arabic(self):
        assert BinaaJudgment.MABNI.value == "مبني"
        assert BinaaJudgment.MUERAB.value == "معرب"


class TestBinaaSubtype:
    def test_required_members(self):
        names = {m.name for m in BinaaSubtype}
        assert names == {
            "BINAA_SUKUN",
            "BINAA_FATH",
            "BINAA_DAMM",
            "BINAA_KASR",
            "INVARIANT_PROPER",
        }


class TestIshtiqaqJudgment:
    def test_required_members(self):
        names = {m.name for m in IshtiqaqJudgment}
        assert names == {"JAMID", "MUSHTAQ", "UNRESOLVED", "NOT_APPLICABLE"}


class TestMushtaqSubtype:
    def test_required_members(self):
        # Closed set of classical mushtaq patterns
        names = {m.name for m in MushtaqSubtype}
        assert names == {
            "ISM_FAIL",
            "ISM_MAFUL",
            "SIFA_MUSHABBAHA",
            "ISM_TAFDIL",
            "ISM_ZAMAN",
            "ISM_MAKAN",
            "ISM_ALA",
            "MASDAR_MIMI",
            "MASDAR_SINAII",
        }


class TestJamidSubtype:
    def test_required_members(self):
        names = {m.name for m in JamidSubtype}
        assert names == {
            "JAMID_DHAT",
            "JAMID_MASDAR_ASLI",
            "JAMID_PROPER_NAME",
            "JAMID_FUNCTIONAL",
        }


class TestSarfFlexibility:
    def test_required_members(self):
        names = {m.name for m in SarfFlexibility}
        assert names == {"MUNSARIF", "MAMNU_MIN_SARF", "NOT_APPLICABLE"}

    def test_no_mabni_value(self):
        """``mabni`` is on the binaa axis, NOT the sarf-flexibility axis."""
        names = {m.name.lower() for m in SarfFlexibility}
        assert "mabni" not in names


class TestAxisOrthogonality:
    """Types alone cannot prove orthogonality; we assert that no axis
    re-uses another axis's value names so accidental coupling is harder."""

    def test_binaa_and_ishtiqaq_disjoint(self):
        binaa = {m.name for m in BinaaJudgment}
        ishtiqaq = {m.name for m in IshtiqaqJudgment}
        # UNRESOLVED / NOT_APPLICABLE intentionally appear on both — but
        # they are distinct enum members; equality across enums is False.
        assert BinaaJudgment.UNRESOLVED is not IshtiqaqJudgment.UNRESOLVED
        # And the value-only intersection is exactly the shared sentinels.
        shared = binaa & ishtiqaq
        assert shared == {"UNRESOLVED", "NOT_APPLICABLE"}
