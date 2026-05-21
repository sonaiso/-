"""Morphology-specific residual taxonomy.

Defines the canonical set of residuals for morphological operations.
Each residual kind has a constructor function that ensures consistent
description formatting.

The nine morphology residual kinds:

1. **context.absent** — Surrounding tokens needed for disambiguation
2. **lexical.ambiguity** — Multiple valid lexical interpretations
3. **proper_name.possible** — Could be proper noun (علم)
4. **transfer.possible** — Could be loanword/transliteration (دخيل/معرب)
5. **weak_letter.present** — Weak radicals (حروف علة: و، ي، alif)
6. **affix.aggressive_strip** — Over-zealous prefix/suffix removal
7. **root.ambiguous** — Multiple root candidates
8. **pattern.collision** — Multiple patterns match surface
9. **broken_plural.possible** — Could be broken plural form (جمع تكسير)

All residual constructors return :class:`fvafk.algebra.Residual` instances.
"""

from __future__ import annotations

from typing import FrozenSet

from fvafk.algebra import Residual


# Canonical set of morphology residual kinds
MORPHOLOGY_RESIDUAL_KINDS: FrozenSet[str] = frozenset({
    "context.absent",
    "lexical.ambiguity",
    "proper_name.possible",
    "transfer.possible",
    "weak_letter.present",
    "affix.aggressive_strip",
    "root.ambiguous",
    "pattern.collision",
    "broken_plural.possible",
})


def make_context_absent(description: str = "") -> Residual:
    """Create residual for missing surrounding tokens.

    Args:
        description: Custom description (optional). If empty, uses default.

    Returns:
        Residual with kind ``context.absent``.

    Example:
        >>> r = make_context_absent("Verb tense ambiguous without subject")
        >>> r.kind
        'context.absent'
    """
    if not description:
        description = "Surrounding tokens needed for disambiguation"
    return Residual(kind="context.absent", description=description)


def make_lexical_ambiguity(description: str = "") -> Residual:
    """Create residual for multiple valid interpretations.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``lexical.ambiguity``.
    """
    if not description:
        description = "Multiple valid lexical interpretations possible"
    return Residual(kind="lexical.ambiguity", description=description)


def make_proper_name_possible(description: str = "") -> Residual:
    """Create residual for possible proper noun.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``proper_name.possible``.
    """
    if not description:
        description = "Could be proper noun (علم) requiring capitalization check"
    return Residual(kind="proper_name.possible", description=description)


def make_transfer_possible(description: str = "") -> Residual:
    """Create residual for possible loanword/transliteration.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``transfer.possible``.
    """
    if not description:
        description = "Could be loanword/transliteration (دخيل/معرب)"
    return Residual(kind="transfer.possible", description=description)


def make_weak_letter_present(weak_letters: str = "", description: str = "") -> Residual:
    """Create residual for weak radicals.

    Args:
        weak_letters: Weak letters detected (e.g. "و", "ي", "alif").
        description: Custom description (optional).

    Returns:
        Residual with kind ``weak_letter.present``.
    """
    if not description:
        if weak_letters:
            description = f"Weak radicals detected: {weak_letters} (حروف علة)"
        else:
            description = "Weak radicals present (حروف علة: و، ي، alif)"
    return Residual(kind="weak_letter.present", description=description)


def make_affix_aggressive_strip(
    affix: str = "", position: str = "", description: str = ""
) -> Residual:
    """Create residual for aggressive affix stripping.

    Args:
        affix: Stripped affix string (e.g. "ال", "ت").
        position: Affix position ("prefix" or "suffix").
        description: Custom description (optional).

    Returns:
        Residual with kind ``affix.aggressive_strip``.
    """
    if not description:
        if affix and position:
            description = f"Aggressive {position} stripping: '{affix}' may belong to stem"
        else:
            description = "Over-zealous prefix/suffix removal; may have stripped stem"
    return Residual(kind="affix.aggressive_strip", description=description)


def make_root_ambiguous(candidates: str = "", description: str = "") -> Residual:
    """Create residual for multiple root candidates.

    Args:
        candidates: Root candidates (e.g. "ك-ت-ب, ك-ت-ب-ة").
        description: Custom description (optional).

    Returns:
        Residual with kind ``root.ambiguous``.
    """
    if not description:
        if candidates:
            description = f"Multiple root candidates: {candidates}"
        else:
            description = "Root extraction ambiguous; multiple candidates"
    return Residual(kind="root.ambiguous", description=description)


def make_pattern_collision(patterns: str = "", description: str = "") -> Residual:
    """Create residual for multiple pattern matches.

    Args:
        patterns: Colliding patterns (e.g. "فاعل, مفعول").
        description: Custom description (optional).

    Returns:
        Residual with kind ``pattern.collision``.
    """
    if not description:
        if patterns:
            description = f"Multiple patterns match: {patterns}"
        else:
            description = "Pattern collision; multiple awzan match surface"
    return Residual(kind="pattern.collision", description=description)


def make_broken_plural_possible(description: str = "") -> Residual:
    """Create residual for possible broken plural.

    Args:
        description: Custom description (optional).

    Returns:
        Residual with kind ``broken_plural.possible``.
    """
    if not description:
        description = "Could be broken plural form (جمع تكسير)"
    return Residual(kind="broken_plural.possible", description=description)


__all__ = [
    "MORPHOLOGY_RESIDUAL_KINDS",
    "make_context_absent",
    "make_lexical_ambiguity",
    "make_proper_name_possible",
    "make_transfer_possible",
    "make_weak_letter_present",
    "make_affix_aggressive_strip",
    "make_root_ambiguous",
    "make_pattern_collision",
    "make_broken_plural_possible",
]
