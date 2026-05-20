"""Tests for ``dal_core.mabni_registry`` (PR-B)."""

import pytest

from dal_core.mabni_registry import (
    MabniCategory,
    MabniEntry,
    MabniRegistry,
    get_default_mabni_registry,
)
from dal_core.mufrad_axes import BinaaSubtype


@pytest.fixture(scope="module")
def registry() -> MabniRegistry:
    return get_default_mabni_registry()


class TestEntryValidation:
    def test_empty_canonical_rejected(self):
        with pytest.raises(ValueError):
            MabniEntry(
                canonical_form="",
                forms=("x",),
                category=MabniCategory.PRONOUN_DETACHED,
                binaa_subtype=BinaaSubtype.INVARIANT_PROPER,
                citation="c",
            )

    def test_empty_forms_rejected(self):
        with pytest.raises(ValueError):
            MabniEntry(
                canonical_form="x",
                forms=(),
                category=MabniCategory.PRONOUN_DETACHED,
                binaa_subtype=BinaaSubtype.INVARIANT_PROPER,
                citation="c",
            )

    def test_canonical_must_be_in_forms(self):
        with pytest.raises(ValueError):
            MabniEntry(
                canonical_form="x",
                forms=("y",),
                category=MabniCategory.PRONOUN_DETACHED,
                binaa_subtype=BinaaSubtype.INVARIANT_PROPER,
                citation="c",
            )

    def test_empty_citation_rejected(self):
        with pytest.raises(ValueError):
            MabniEntry(
                canonical_form="x",
                forms=("x",),
                category=MabniCategory.PRONOUN_DETACHED,
                binaa_subtype=BinaaSubtype.INVARIANT_PROPER,
                citation="",
            )


class TestRegistryCategories:
    """At least one entry per classical category must exist."""

    def test_all_categories_present(self, registry):
        for cat in MabniCategory:
            entries = registry.by_category.get(cat, ())
            assert entries, f"Category {cat} has no entries"

    def test_dual_demonstratives_excluded(self, registry):
        # هذان / هاتان are MUERAB and must NOT be in registry.
        assert not registry.is_mabni_noun("هَذَانِ")
        assert not registry.is_mabni_noun("هَاتَانِ")

    def test_dual_relatives_excluded(self, registry):
        assert not registry.is_mabni_noun("اللَّذَانِ")
        assert not registry.is_mabni_noun("اللَّتَانِ")


class TestLookup:
    def test_pronoun_present(self, registry):
        assert registry.is_mabni_noun("نَحْنُ")
        results = registry.lookup("نَحْنُ")
        assert len(results) == 1
        assert results[0].category == MabniCategory.PRONOUN_DETACHED

    def test_demonstrative_present(self, registry):
        assert registry.is_mabni_noun("هَذَا")

    def test_relative_present(self, registry):
        assert registry.is_mabni_noun("الَّذِينَ")

    def test_interrogative_present(self, registry):
        assert registry.is_mabni_noun("كَيْفَ")

    def test_compound_number_present(self, registry):
        assert registry.is_mabni_noun("خَمْسَةَ عَشَرَ")

    def test_name_of_verb_present(self, registry):
        assert registry.is_mabni_noun("هَيْهَاتَ")

    def test_shared_form_multiple_categories(self, registry):
        # مَنْ may be interrogative AND relative AND conditional.
        results = registry.lookup("مَنْ")
        categories = {e.category for e in results}
        assert MabniCategory.INTERROGATIVE in categories
        assert MabniCategory.RELATIVE in categories
        assert MabniCategory.CONDITIONAL in categories

    def test_unknown_form_returns_empty(self, registry):
        assert registry.lookup("رَجُلٌ") == ()
        assert registry.lookup("كَاتِبٌ") == ()
        assert not registry.is_mabni_noun("رَجُلٌ")

    def test_empty_form_safe(self, registry):
        assert registry.lookup("") == ()


class TestImmutability:
    """Mirrors the NahwOperatorRegistry immutability test pattern (PR #16)."""

    def test_setattr_rejected(self, registry):
        with pytest.raises(AttributeError):
            registry.entries = ()  # type: ignore[misc]

    def test_delattr_rejected(self, registry):
        with pytest.raises(AttributeError):
            del registry.entries  # type: ignore[misc]

    def test_by_form_is_mapping_proxy(self, registry):
        from types import MappingProxyType

        assert isinstance(registry.by_form, MappingProxyType)
        with pytest.raises(TypeError):
            registry.by_form["x"] = ()  # type: ignore[index]

    def test_by_category_is_mapping_proxy(self, registry):
        from types import MappingProxyType

        assert isinstance(registry.by_category, MappingProxyType)


class TestSingleton:
    def test_lazy_singleton_identity(self):
        a = get_default_mabni_registry()
        b = get_default_mabni_registry()
        assert a is b
