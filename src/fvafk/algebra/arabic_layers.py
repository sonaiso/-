"""Typed algebraic layers (Domains) and the allowed-bridge matrix.

This module defines *only* the topology of the algebra; it contains no
linguistic logic. Linguistic rules live in higher modules
(``cpb.py``, ``decision_tree.py``).

The forbidden transitions mirror the prohibitions documented in
``docs/DAL_ALGEBRA_SIGNATURE.md`` for ``dal_core`` and are restated here
for the FVAFK pipeline:

- ``GRAPHEME`` ↛ ``MORPH_DEEP``     (رسم → وزن عميق)
- ``PHONEME``  ↛ ``MORPH_DEEP``     (صوت → وزن عميق)
- ``SYLLABLE`` ↛ ``ROOT``           (مقطع → جذر)
- ``MORPH_SURFACE`` ↛ ``MORPH_DEEP``(وزن ظاهر → وزن عميق)
- ``MORPH_SURFACE`` ↛ ``SEMANTICS`` (وزن → دلالة)
- ``MORPH_DEEP``    ↛ ``HUKM``      (وزن عميق → حكم)

Each forbidden jump must be mediated by an intermediate carrier.
"""

from __future__ import annotations

from enum import Enum
from typing import FrozenSet, Tuple


class Domain(str, Enum):
    """Algebraic domain (layer) over which a carrier lives.

    Domains are ordered from surface (raw text) toward judgement (hukm).
    The numeric ordering is **not** a guarantee of legal promotion; the
    allowed transitions are defined explicitly in
    :data:`ALLOWED_BRIDGES` and the prohibited transitions in
    :data:`FORBIDDEN_BRIDGES`.
    """

    GRAPHEME = "grapheme"        # رسم
    PHONEME = "phoneme"          # صوت
    SYLLABLE = "syllable"        # مقطع
    MORPH_SURFACE = "morph_surface"  # وزن ظاهر
    ROOT = "root"                # جذر
    MORPH_DEEP = "morph_deep"    # وزن عميق
    SYNTAX = "syntax"            # نحو
    SEMANTICS = "semantics"      # دلالة
    HUKM = "hukm"                # حكم


# Pair (source, target). A bridge is *legal* iff (source, target) is in
# ALLOWED_BRIDGES and not in FORBIDDEN_BRIDGES.
ALLOWED_BRIDGES: FrozenSet[Tuple[Domain, Domain]] = frozenset(
    {
        (Domain.GRAPHEME, Domain.PHONEME),
        (Domain.PHONEME, Domain.SYLLABLE),
        (Domain.SYLLABLE, Domain.MORPH_SURFACE),
        (Domain.MORPH_SURFACE, Domain.ROOT),
        (Domain.ROOT, Domain.MORPH_DEEP),
        (Domain.MORPH_DEEP, Domain.SYNTAX),
        (Domain.SYNTAX, Domain.SEMANTICS),
        (Domain.SEMANTICS, Domain.HUKM),
    }
)


FORBIDDEN_BRIDGES: FrozenSet[Tuple[Domain, Domain]] = frozenset(
    {
        (Domain.GRAPHEME, Domain.MORPH_DEEP),
        (Domain.PHONEME, Domain.MORPH_DEEP),
        (Domain.SYLLABLE, Domain.ROOT),
        (Domain.MORPH_SURFACE, Domain.MORPH_DEEP),
        (Domain.MORPH_SURFACE, Domain.SEMANTICS),
        (Domain.MORPH_DEEP, Domain.HUKM),
        (Domain.GRAPHEME, Domain.SEMANTICS),
        (Domain.PHONEME, Domain.SEMANTICS),
    }
)


def is_bridge_allowed(source: Domain, target: Domain) -> bool:
    """Return ``True`` iff a direct bridge ``source → target`` is legal.

    A bridge is legal when it is explicitly listed in
    :data:`ALLOWED_BRIDGES` and is not in :data:`FORBIDDEN_BRIDGES`.
    Identity bridges (``source == target``) are always legal.
    """
    if source == target:
        return True
    if (source, target) in FORBIDDEN_BRIDGES:
        return False
    return (source, target) in ALLOWED_BRIDGES


__all__ = [
    "Domain",
    "ALLOWED_BRIDGES",
    "FORBIDDEN_BRIDGES",
    "is_bridge_allowed",
]
