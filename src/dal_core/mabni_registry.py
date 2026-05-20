"""
Mabni Registry (سجلّ الأسماء المبنية المغلق)

A closed, immutable registry of nouns that are MABNI by lexical identity:
pronouns, demonstratives, relative nouns, interrogatives, conditionals,
indeclinable adverbs, names-of-verb, and compound numbers (11..19).

This registry is the SOLE source of truth consulted by ``binaa_judge`` for
the "is this noun built?" question. It is:

* Closed — no runtime additions. New entries require a code change + tests.
* Immutable — backed by ``MappingProxyType`` and frozen dataclasses, with
  ``__setattr__`` / ``__delattr__`` guards on the registry container.
* Span-free — entries describe the *type* of word; positional evidence is
  attached at judge time, not here.

Mirrors the immutability pattern of ``NahwOperatorRegistry`` (PR #16).

Architectural note: this registry is consulted by both the BINAA judge
(to license MABNI on the binaa axis) and by the ISHTIQAQ judge (to license
``JamidSubtype.JAMID_FUNCTIONAL`` on the ishtiqaq axis). The two axes
remain logically independent — the registry merely supplies one of many
inputs each judge needs.
"""

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Mapping

from dal_core.mufrad_axes import BinaaSubtype


# =============================================================================
# Categories
# =============================================================================


class MabniCategory(Enum):
    """The lexical category that licenses MABNI."""

    PRONOUN_DETACHED = "ضمير منفصل"
    PRONOUN_ATTACHED = "ضمير متصل"
    DEMONSTRATIVE = "اسم إشارة"
    RELATIVE = "اسم موصول"
    INTERROGATIVE = "اسم استفهام"
    CONDITIONAL = "اسم شرط"
    ADVERB_MABNI = "ظرف مبني"
    NAME_OF_VERB = "اسم فعل"
    COMPOUND_NUMBER = "عدد مركّب"


# =============================================================================
# Entry
# =============================================================================


@dataclass(frozen=True)
class MabniEntry:
    """One row in the closed registry.

    ``forms`` is a tuple of surface variants that all map to the same
    lexical entry (e.g. هذا/ذا/هذه — same demonstrative family with
    different gender/number, kept as separate entries to preserve the
    distinction).
    """

    canonical_form: str
    """Canonical surface form, e.g. "هذا"."""

    forms: tuple[str, ...]
    """All accepted surface variants (must be non-empty, ``canonical_form``
    must appear in it)."""

    category: MabniCategory

    binaa_subtype: BinaaSubtype
    """The classical building shape (sukun / fath / damm / kasr / invariant)."""

    citation: str
    """A short linguistic-tradition witness for this MABNI classification
    (e.g. "الكافية في النحو"). Required for evidence chaining."""

    note: str = ""
    """Optional remark (e.g. dual exception)."""

    def __post_init__(self) -> None:
        if not self.canonical_form:
            raise ValueError("canonical_form must not be empty")
        if not self.forms:
            raise ValueError("forms must contain at least one surface variant")
        if self.canonical_form not in self.forms:
            raise ValueError(
                f"canonical_form {self.canonical_form!r} must appear in forms {self.forms!r}"
            )
        if not self.citation:
            raise ValueError("citation must not be empty")


# =============================================================================
# Seed data
# =============================================================================


def _seed_entries() -> tuple[MabniEntry, ...]:
    """Build the closed seed list.

    Coverage targets the productive closed-class items. Exhaustive coverage
    is not required for correctness; what IS required is that:

    * every classical sub-category is represented by at least one entry, so
      consumers can rely on category presence;
    * any entry for a dual demonstrative or dual relative (which are MUERAB)
      is intentionally absent.
    """
    cite = "النحو العربي — قاعدة مغلقة كلاسيكية"

    entries: list[MabniEntry] = []

    # Detached personal pronouns (ضمائر منفصلة) — invariant proper.
    for form in (
        "أَنَا",
        "نَحْنُ",
        "أَنْتَ",
        "أَنْتِ",
        "أَنْتُمَا",
        "أَنْتُمْ",
        "أَنْتُنَّ",
        "هُوَ",
        "هِيَ",
        "هُمَا",
        "هُمْ",
        "هُنَّ",
    ):
        entries.append(
            MabniEntry(
                canonical_form=form,
                forms=(form,),
                category=MabniCategory.PRONOUN_DETACHED,
                binaa_subtype=BinaaSubtype.INVARIANT_PROPER,
                citation=cite,
            )
        )

    # Attached pronouns (ضمائر متصلة).
    for form, subtype in (
        ("ـِي", BinaaSubtype.BINAA_KASR),
        ("ـنَا", BinaaSubtype.BINAA_FATH),
        ("ـكَ", BinaaSubtype.BINAA_FATH),
        ("ـكِ", BinaaSubtype.BINAA_KASR),
        ("ـكُمَا", BinaaSubtype.BINAA_FATH),
        ("ـكُمْ", BinaaSubtype.BINAA_SUKUN),
        ("ـكُنَّ", BinaaSubtype.BINAA_FATH),
        ("ـهُ", BinaaSubtype.BINAA_DAMM),
        ("ـهَا", BinaaSubtype.BINAA_FATH),
        ("ـهُمَا", BinaaSubtype.BINAA_FATH),
        ("ـهُمْ", BinaaSubtype.BINAA_SUKUN),
        ("ـهُنَّ", BinaaSubtype.BINAA_FATH),
    ):
        entries.append(
            MabniEntry(
                canonical_form=form,
                forms=(form,),
                category=MabniCategory.PRONOUN_ATTACHED,
                binaa_subtype=subtype,
                citation=cite,
            )
        )

    # Demonstratives (أسماء الإشارة) — singular and plural ONLY.
    # NOTE: dual demonstratives (هذان، هاتان) are MUERAB and intentionally
    # excluded from this registry.
    for form, subtype in (
        ("هَذَا", BinaaSubtype.INVARIANT_PROPER),
        ("هَذِهِ", BinaaSubtype.INVARIANT_PROPER),
        ("ذَلِكَ", BinaaSubtype.INVARIANT_PROPER),
        ("تِلْكَ", BinaaSubtype.INVARIANT_PROPER),
        ("هَؤُلَاءِ", BinaaSubtype.BINAA_KASR),
        ("أُولَئِكَ", BinaaSubtype.BINAA_FATH),
        ("هُنَا", BinaaSubtype.BINAA_FATH),
        ("هُنَاكَ", BinaaSubtype.BINAA_FATH),
        ("ثَمَّ", BinaaSubtype.BINAA_FATH),
    ):
        entries.append(
            MabniEntry(
                canonical_form=form,
                forms=(form,),
                category=MabniCategory.DEMONSTRATIVE,
                binaa_subtype=subtype,
                citation=cite,
                note="Dual demonstratives excluded — they are MUERAB.",
            )
        )

    # Relative nouns (الأسماء الموصولة) — singular/plural; dual excluded.
    for form, subtype in (
        ("الَّذِي", BinaaSubtype.BINAA_SUKUN),
        ("الَّتِي", BinaaSubtype.BINAA_SUKUN),
        ("الَّذِينَ", BinaaSubtype.BINAA_FATH),
        ("اللَّاتِي", BinaaSubtype.BINAA_KASR),
        ("اللَّوَاتِي", BinaaSubtype.BINAA_KASR),
        ("مَنْ", BinaaSubtype.BINAA_SUKUN),
        ("مَا", BinaaSubtype.BINAA_SUKUN),
    ):
        entries.append(
            MabniEntry(
                canonical_form=form,
                forms=(form,),
                category=MabniCategory.RELATIVE,
                binaa_subtype=subtype,
                citation=cite,
                note="Dual relatives (اللذان/اللتان) excluded — MUERAB.",
            )
        )

    # Interrogatives (أسماء الاستفهام).
    for form, subtype in (
        ("مَنْ", BinaaSubtype.BINAA_SUKUN),
        ("مَا", BinaaSubtype.BINAA_SUKUN),
        ("مَاذَا", BinaaSubtype.BINAA_SUKUN),
        ("مَتَى", BinaaSubtype.BINAA_SUKUN),
        ("أَيْنَ", BinaaSubtype.BINAA_FATH),
        ("كَيْفَ", BinaaSubtype.BINAA_FATH),
        ("كَمْ", BinaaSubtype.BINAA_SUKUN),
        ("أَنَّى", BinaaSubtype.BINAA_SUKUN),
    ):
        entries.append(
            MabniEntry(
                canonical_form=form,
                forms=(form,),
                category=MabniCategory.INTERROGATIVE,
                binaa_subtype=subtype,
                citation=cite,
            )
        )

    # Conditionals (أسماء الشرط).
    for form, subtype in (
        ("مَنْ", BinaaSubtype.BINAA_SUKUN),
        ("مَا", BinaaSubtype.BINAA_SUKUN),
        ("مَهْمَا", BinaaSubtype.BINAA_SUKUN),
        ("مَتَى", BinaaSubtype.BINAA_SUKUN),
        ("أَيْنَمَا", BinaaSubtype.BINAA_FATH),
        ("حَيْثُمَا", BinaaSubtype.BINAA_FATH),
        ("كَيْفَمَا", BinaaSubtype.BINAA_FATH),
    ):
        entries.append(
            MabniEntry(
                canonical_form=form,
                forms=(form,),
                category=MabniCategory.CONDITIONAL,
                binaa_subtype=subtype,
                citation=cite,
            )
        )

    # Indeclinable adverbs (الظروف المبنية).
    for form, subtype in (
        ("حَيْثُ", BinaaSubtype.BINAA_DAMM),
        ("إِذْ", BinaaSubtype.BINAA_SUKUN),
        ("إِذَا", BinaaSubtype.BINAA_SUKUN),
        ("أَمْسِ", BinaaSubtype.BINAA_KASR),
        ("الْآنَ", BinaaSubtype.BINAA_FATH),
        ("قَطُّ", BinaaSubtype.BINAA_DAMM),
        ("لَدُنْ", BinaaSubtype.BINAA_SUKUN),
    ):
        entries.append(
            MabniEntry(
                canonical_form=form,
                forms=(form,),
                category=MabniCategory.ADVERB_MABNI,
                binaa_subtype=subtype,
                citation=cite,
            )
        )

    # Names of verb (أسماء الأفعال).
    for form, subtype in (
        ("هَيْهَاتَ", BinaaSubtype.BINAA_FATH),
        ("صَهْ", BinaaSubtype.BINAA_SUKUN),
        ("مَهْ", BinaaSubtype.BINAA_SUKUN),
        ("شَتَّانَ", BinaaSubtype.BINAA_FATH),
        ("آمِينَ", BinaaSubtype.BINAA_FATH),
    ):
        entries.append(
            MabniEntry(
                canonical_form=form,
                forms=(form,),
                category=MabniCategory.NAME_OF_VERB,
                binaa_subtype=subtype,
                citation=cite,
            )
        )

    # Compound numbers 11..19 (الأعداد المركّبة) — both parts built on fath.
    for form in (
        "أَحَدَ عَشَرَ",
        "اثْنَا عَشَرَ",
        "ثَلَاثَةَ عَشَرَ",
        "أَرْبَعَةَ عَشَرَ",
        "خَمْسَةَ عَشَرَ",
        "سِتَّةَ عَشَرَ",
        "سَبْعَةَ عَشَرَ",
        "ثَمَانِيَةَ عَشَرَ",
        "تِسْعَةَ عَشَرَ",
    ):
        entries.append(
            MabniEntry(
                canonical_form=form,
                forms=(form,),
                category=MabniCategory.COMPOUND_NUMBER,
                binaa_subtype=BinaaSubtype.BINAA_FATH,
                citation=cite,
                note="اثنا عشر: only the second word is MABNI in some accounts.",
            )
        )

    return tuple(entries)


# =============================================================================
# Registry container
# =============================================================================


class MabniRegistry:
    """Immutable registry. After construction:

    * ``_entries``, ``_by_form``, ``_by_category`` are wrapped in
      ``MappingProxyType``/frozen sequences.
    * ``__setattr__`` and ``__delattr__`` raise ``AttributeError`` for any
      post-init mutation attempt.

    Public lookups are O(1) average via the form index.
    """

    __slots__ = ("_entries", "_by_form", "_by_category", "_frozen")

    def __init__(self, entries: tuple[MabniEntry, ...]) -> None:
        # During init, bypass the freeze guard via object.__setattr__.
        object.__setattr__(self, "_frozen", False)

        # Index by every surface form (a single entry can have multiple
        # forms; multiple entries can share a surface form, e.g. مَنْ as
        # both interrogative and relative).
        by_form: dict[str, tuple[MabniEntry, ...]] = {}
        by_category: dict[MabniCategory, list[MabniEntry]] = {}
        for entry in entries:
            for form in entry.forms:
                by_form[form] = by_form.get(form, ()) + (entry,)
            by_category.setdefault(entry.category, []).append(entry)

        object.__setattr__(self, "_entries", entries)
        object.__setattr__(self, "_by_form", MappingProxyType(by_form))
        object.__setattr__(
            self,
            "_by_category",
            MappingProxyType({cat: tuple(items) for cat, items in by_category.items()}),
        )
        object.__setattr__(self, "_frozen", True)

    # --- mutation guards --------------------------------------------------

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_frozen", False):
            raise AttributeError(
                f"MabniRegistry is immutable; cannot set {name!r}"
            )
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        if getattr(self, "_frozen", False):
            raise AttributeError(
                f"MabniRegistry is immutable; cannot delete {name!r}"
            )
        object.__delattr__(self, name)

    # --- public API -------------------------------------------------------

    @property
    def entries(self) -> tuple[MabniEntry, ...]:
        return self._entries

    @property
    def by_form(self) -> Mapping[str, tuple[MabniEntry, ...]]:
        return self._by_form

    @property
    def by_category(self) -> Mapping[MabniCategory, tuple[MabniEntry, ...]]:
        return self._by_category

    def lookup(self, form: str) -> tuple[MabniEntry, ...]:
        """Return all entries matching the given surface form.

        Multiple entries may match (e.g. مَنْ ≡ interrogative + relative +
        conditional). Caller decides how to handle competition.

        Returns an empty tuple if no entry matches — the form is not in the
        closed mabni set, which licenses MUERAB by default for a noun.
        """
        if not form:
            return ()
        return self._by_form.get(form, ())

    def is_mabni_noun(self, form: str) -> bool:
        """Convenience predicate. True iff ``form`` is in the registry."""
        return bool(self.lookup(form))


# =============================================================================
# Module-level default registry
# =============================================================================


_DEFAULT_REGISTRY: MabniRegistry | None = None


def get_default_mabni_registry() -> MabniRegistry:
    """Lazy singleton accessor. Always returns the same immutable registry."""
    global _DEFAULT_REGISTRY
    if _DEFAULT_REGISTRY is None:
        _DEFAULT_REGISTRY = MabniRegistry(_seed_entries())
    return _DEFAULT_REGISTRY


__all__ = [
    "MabniCategory",
    "MabniEntry",
    "MabniRegistry",
    "get_default_mabni_registry",
]
