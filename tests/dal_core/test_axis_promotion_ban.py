"""Tests for the SYLLABIC → BINAA_JUDGMENT promotion ban (plan §5.1).

These tests exist as a permanent canary. If a future engineer
"normalizes" the FORBIDDEN_AXIS_PROMOTIONS set or removes the
``assert_axis_promotion_allowed`` callsite, this file will fail loudly.
"""

import pytest

from dal_core.dal_algebra import (
    DalTransitionDomain,
    FORBIDDEN_AXIS_PROMOTIONS,
    assert_axis_promotion_allowed,
)


class TestForbiddenAxisPromotions:
    def test_set_includes_syllabic_to_binaa(self):
        assert ("SYLLABIC", "BINAA_JUDGMENT") in FORBIDDEN_AXIS_PROMOTIONS

    def test_set_includes_syllabic_to_ishtiqaq(self):
        assert ("SYLLABIC", "ISHTIQAQ_JUDGMENT") in FORBIDDEN_AXIS_PROMOTIONS

    def test_set_is_immutable(self):
        # frozenset has no mutating methods. Confirm the type.
        assert isinstance(FORBIDDEN_AXIS_PROMOTIONS, frozenset)


class TestAssertAxisPromotionAllowed:
    def test_raises_on_syllabic_to_binaa(self):
        with pytest.raises(ValueError, match="SYLLABIC.*BINAA_JUDGMENT"):
            assert_axis_promotion_allowed(
                DalTransitionDomain.SYLLABIC, "BINAA_JUDGMENT"
            )

    def test_raises_on_syllabic_to_ishtiqaq(self):
        with pytest.raises(ValueError, match="SYLLABIC.*ISHTIQAQ_JUDGMENT"):
            assert_axis_promotion_allowed(
                DalTransitionDomain.SYLLABIC, "ISHTIQAQ_JUDGMENT"
            )

    def test_allowed_promotion_does_not_raise(self):
        # IDENTITY_AXIS → BINAA_JUDGMENT is the LEGITIMATE pathway.
        # It must not raise.
        assert_axis_promotion_allowed(
            DalTransitionDomain.IDENTITY_AXIS, "BINAA_JUDGMENT"
        )

    def test_other_combinations_do_not_raise(self):
        # PRE_MORPH → BINAA_JUDGMENT is not in the explicit ban list.
        # That doesn't mean it's a good idea, but the ban is targeted
        # specifically at SYLLABIC because that is the historical
        # hallucination vector.
        assert_axis_promotion_allowed(
            DalTransitionDomain.PRE_MORPH, "BINAA_JUDGMENT"
        )


class TestPublicAPI:
    def test_exports_present(self):
        import dal_core

        assert hasattr(dal_core, "FORBIDDEN_AXIS_PROMOTIONS")
        assert hasattr(dal_core, "assert_axis_promotion_allowed")
