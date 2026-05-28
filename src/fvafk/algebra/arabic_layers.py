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

PATH-AWARE BRIDGES (not globally allowed, not globally forbidden):

- ``LAFZ`` → ``IDENTITY``: Path-aware, requires validation

  Two valid paths to IDENTITY exist:

  1. Mushtaq (derived) path:
     LAFZ → MARKER_PROTECTION/CLAUSE_AGREEMENT → ROOT_STEM → WEIGHT → IDENTITY

  2. Non-weight path (for mabni, particles, pronouns, jāmid, proper names, loans):
     LAFZ → PathAwareIdentityValidator → IDENTITY

  This bridge is delegated to PathAwareIdentityValidator, not declared
  globally allowed or forbidden.
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

    LEGACY DOMAINS (original FVAFK pipeline):
        GRAPHEME, PHONEME, SYLLABLE, MORPH_SURFACE, ROOT, MORPH_DEEP,
        SYNTAX, SEMANTICS, HUKM

    CANONICAL GARA DOMAINS (aligned with dal_core DomainType):
        SCRIPT, SOUND, SYLLABLE_CANONICAL, BOUNDARY, LAFZ,
        MARKER_PROTECTION, CLAUSE_AGREEMENT, ROOT_STEM, WEIGHT,
        IDENTITY, SOURCE_FORM, ATTRIBUTE_FORM, FUNCTIONAL_FORM, WORDFORM,
        I3RAB_SURFACE, AMIL_RELATION, SYNTAX_CANONICAL,
        SEMANTICS_CANONICAL, PRAGMATICS, EVIDENCE, JUDGMENT
    """

    # ========================================================================
    # LEGACY DOMAINS (original FVAFK pipeline)
    # ========================================================================
    GRAPHEME = "grapheme"        # رسم
    PHONEME = "phoneme"          # صوت
    SYLLABLE = "syllable"        # مقطع
    MORPH_SURFACE = "morph_surface"  # وزن ظاهر
    ROOT = "root"                # جذر
    MORPH_DEEP = "morph_deep"    # وزن عميق
    SYNTAX = "syntax"            # نحو
    SEMANTICS = "semantics"      # دلالة
    HUKM = "hukm"                # حكم

    # ========================================================================
    # CANONICAL GARA DOMAINS (aligned with dal_core)
    # ========================================================================
    # Surface and Script Domains (U₀-U₁)
    SCRIPT = "script"                          # مجال الخط
    SOUND = "sound"                            # مجال الصوت

    # Phonological Domains (U₂-U₃)
    SYLLABLE_CANONICAL = "syllable_canonical"  # مجال المقطع
    BOUNDARY = "boundary"                      # مجال الحد

    # Lexical Unit Domain (U₄)
    LAFZ = "lafz"                              # مجال اللفظ

    # Surface Protection Domains (U₇)
    MARKER_PROTECTION = "marker_protection"    # مجال حماية العلامات
    CLAUSE_AGREEMENT = "clause_agreement"      # مجال الاتفاق الجملي

    # Morphological Domains (U₈-U₉)
    ROOT_STEM = "root_stem"                    # مجال الجذر والجذع
    WEIGHT = "weight"                          # مجال الوزن

    # Identity Domain (U₅-U₆)
    IDENTITY = "identity"                      # مجال محور الهوية (Ism/Fi'l/Harf)

    # Derivational Domains (U₁₀+)
    SOURCE_FORM = "source_form"                # مجال صيغة المصدر
    ATTRIBUTE_FORM = "attribute_form"          # مجال صيغة الصفة
    FUNCTIONAL_FORM = "functional_form"        # مجال الصيغة الوظيفية
    WORDFORM = "wordform"                      # مجال صورة الكلمة المرشحة

    # Syntactic Domains (U₁₃+)
    I3RAB_SURFACE = "i3rab_surface"            # مجال سطح الإعراب
    AMIL_RELATION = "amil_relation"            # مجال علاقة العامل
    SYNTAX_CANONICAL = "syntax_canonical"      # مجال النحو

    # Semantic Domains (U₁₄-U₁₅)
    SEMANTICS_CANONICAL = "semantics_canonical"  # مجال الدلالة
    PRAGMATICS = "pragmatics"                  # مجال التداول

    # Meta-Domains
    EVIDENCE = "evidence"                      # مجال الدليل
    JUDGMENT = "judgment"                      # مجال الحكم


# ============================================================================
# LEGACY BRIDGE TOPOLOGY (original FVAFK pipeline)
# ============================================================================

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
        # The following two are *transitively* implied by the bridges
        # above (no GRAPHEME/PHONEME → SEMANTICS path exists through
        # ALLOWED_BRIDGES). They are listed explicitly so a caller who
        # only consults FORBIDDEN_BRIDGES still gets the right answer
        # without having to recompute reachability.
        (Domain.GRAPHEME, Domain.SEMANTICS),
        (Domain.PHONEME, Domain.SEMANTICS),
    }
)


# ============================================================================
# CANONICAL GARA BRIDGE TOPOLOGY (constitutional domain architecture)
# ============================================================================

CANONICAL_ALLOWED_BRIDGES: FrozenSet[Tuple[Domain, Domain]] = frozenset(
    {
        # Surface → Phonological chain
        (Domain.SCRIPT, Domain.SOUND),
        (Domain.SOUND, Domain.SYLLABLE_CANONICAL),
        (Domain.SYLLABLE_CANONICAL, Domain.BOUNDARY),

        # Boundary → Lafz
        (Domain.BOUNDARY, Domain.LAFZ),

        # Lafz → Protection domains (parallel paths)
        (Domain.LAFZ, Domain.MARKER_PROTECTION),
        (Domain.LAFZ, Domain.CLAUSE_AGREEMENT),

        # Protection → Morphological analysis
        (Domain.MARKER_PROTECTION, Domain.ROOT_STEM),
        (Domain.CLAUSE_AGREEMENT, Domain.ROOT_STEM),

        # Morphological chain
        (Domain.ROOT_STEM, Domain.WEIGHT),
        (Domain.WEIGHT, Domain.IDENTITY),

        # Identity → Derivational forms (parallel paths)
        (Domain.IDENTITY, Domain.SOURCE_FORM),
        (Domain.IDENTITY, Domain.ATTRIBUTE_FORM),
        (Domain.IDENTITY, Domain.FUNCTIONAL_FORM),

        # Derivational → WordForm convergence
        (Domain.SOURCE_FORM, Domain.WORDFORM),
        (Domain.ATTRIBUTE_FORM, Domain.WORDFORM),
        (Domain.FUNCTIONAL_FORM, Domain.WORDFORM),

        # WordForm → Syntactic domains
        (Domain.WORDFORM, Domain.I3RAB_SURFACE),
        (Domain.WORDFORM, Domain.AMIL_RELATION),

        # Syntactic → Syntax convergence
        (Domain.I3RAB_SURFACE, Domain.SYNTAX_CANONICAL),
        (Domain.AMIL_RELATION, Domain.SYNTAX_CANONICAL),

        # Syntax → Semantics chain
        (Domain.SYNTAX_CANONICAL, Domain.SEMANTICS_CANONICAL),
        (Domain.SEMANTICS_CANONICAL, Domain.PRAGMATICS),

        # Pragmatics → Judgment path
        (Domain.PRAGMATICS, Domain.EVIDENCE),
        (Domain.EVIDENCE, Domain.JUDGMENT),
    }
)


CANONICAL_FORBIDDEN_BRIDGES: FrozenSet[Tuple[Domain, Domain]] = frozenset(
    {
        # Surface layers → Deep layers (forbidden jumps)
        (Domain.SCRIPT, Domain.ROOT_STEM),
        (Domain.SCRIPT, Domain.WEIGHT),
        (Domain.SCRIPT, Domain.IDENTITY),
        (Domain.SCRIPT, Domain.SEMANTICS_CANONICAL),
        (Domain.SCRIPT, Domain.JUDGMENT),

        (Domain.SOUND, Domain.ROOT_STEM),
        (Domain.SOUND, Domain.WEIGHT),
        (Domain.SOUND, Domain.IDENTITY),
        (Domain.SOUND, Domain.SEMANTICS_CANONICAL),
        (Domain.SOUND, Domain.JUDGMENT),

        (Domain.SYLLABLE_CANONICAL, Domain.ROOT_STEM),
        (Domain.SYLLABLE_CANONICAL, Domain.WEIGHT),
        (Domain.SYLLABLE_CANONICAL, Domain.IDENTITY),
        (Domain.SYLLABLE_CANONICAL, Domain.SEMANTICS_CANONICAL),

        (Domain.BOUNDARY, Domain.ROOT_STEM),
        (Domain.BOUNDARY, Domain.WEIGHT),
        (Domain.BOUNDARY, Domain.IDENTITY),

        # Lafz → Weight jumps (must go through protection)
        (Domain.LAFZ, Domain.ROOT_STEM),
        (Domain.LAFZ, Domain.WEIGHT),
        # Note: LAFZ → IDENTITY is path-aware, not forbidden categorically
        # (allows mabni, particles, pronouns, jāmid, proper names, loans)
        (Domain.LAFZ, Domain.SYNTAX_CANONICAL),
        (Domain.LAFZ, Domain.SEMANTICS_CANONICAL),

        # Morphology → Semantics/Judgment jumps
        (Domain.ROOT_STEM, Domain.SEMANTICS_CANONICAL),
        (Domain.ROOT_STEM, Domain.JUDGMENT),
        (Domain.WEIGHT, Domain.SEMANTICS_CANONICAL),
        (Domain.WEIGHT, Domain.JUDGMENT),
        (Domain.IDENTITY, Domain.SEMANTICS_CANONICAL),
        (Domain.IDENTITY, Domain.JUDGMENT),

        # Derivational → Semantics/Judgment jumps
        (Domain.SOURCE_FORM, Domain.SEMANTICS_CANONICAL),
        (Domain.SOURCE_FORM, Domain.JUDGMENT),
        (Domain.ATTRIBUTE_FORM, Domain.SEMANTICS_CANONICAL),
        (Domain.ATTRIBUTE_FORM, Domain.JUDGMENT),
        (Domain.FUNCTIONAL_FORM, Domain.SEMANTICS_CANONICAL),
        (Domain.FUNCTIONAL_FORM, Domain.JUDGMENT),

        # WordForm → Semantics/Judgment jumps (must go through syntax)
        (Domain.WORDFORM, Domain.SEMANTICS_CANONICAL),
        (Domain.WORDFORM, Domain.PRAGMATICS),
        (Domain.WORDFORM, Domain.EVIDENCE),
        (Domain.WORDFORM, Domain.JUDGMENT),

        # Syntax → Judgment jump (must go through semantics → pragmatics → evidence)
        (Domain.I3RAB_SURFACE, Domain.JUDGMENT),
        (Domain.AMIL_RELATION, Domain.JUDGMENT),
        (Domain.SYNTAX_CANONICAL, Domain.JUDGMENT),
        (Domain.SYNTAX_CANONICAL, Domain.EVIDENCE),

        # Semantics → Judgment jump (must go through pragmatics → evidence)
        (Domain.SEMANTICS_CANONICAL, Domain.JUDGMENT),
        (Domain.SEMANTICS_CANONICAL, Domain.EVIDENCE),

        # Pragmatics → Judgment jump (must go through evidence)
        (Domain.PRAGMATICS, Domain.JUDGMENT),

        # Constitutional prohibition: لا حكم بلا دليل (no judgment without evidence)
        # This is enforced by requiring Evidence before Judgment
    }
)


def is_legacy_bridge_allowed(source: Domain, target: Domain) -> bool:
    """Return ``True`` iff a direct bridge ``source → target`` is legal in LEGACY topology.

    A bridge is legal when it is explicitly listed in
    :data:`ALLOWED_BRIDGES` and is not in :data:`FORBIDDEN_BRIDGES`.
    Identity bridges (``source == target``) are always legal.

    This function maintains backward compatibility with the original FVAFK pipeline.
    """
    if source == target:
        return True
    if (source, target) in FORBIDDEN_BRIDGES:
        return False
    return (source, target) in ALLOWED_BRIDGES


def is_canonical_bridge_allowed(source: Domain, target: Domain) -> bool:
    """Return ``True`` iff a direct bridge ``source → target`` is legal in CANONICAL topology.

    A bridge is legal when it is explicitly listed in
    :data:`CANONICAL_ALLOWED_BRIDGES` and is not in :data:`CANONICAL_FORBIDDEN_BRIDGES`.
    Identity bridges (``source == target``) are always legal.

    Default policy: Unknown bridges are FORBIDDEN (fail-safe).

    This function enforces the canonical GARA domain architecture aligned with dal_core.

    Constitutional Laws Enforced:
        - لا وزن قبل جذر (no weight before root)
        - لا معنى قبل نحو (no meaning before syntax)
        - لا حكم قبل دليل (no judgment before evidence)
        - لا انتقال من اللفظ المفرد إلى المعنى (no isolated-word → meaning jump)
    """
    if source == target:
        return True
    if (source, target) in CANONICAL_FORBIDDEN_BRIDGES:
        return False
    return (source, target) in CANONICAL_ALLOWED_BRIDGES


def is_bridge_allowed(source: Domain, target: Domain) -> bool:
    """Return ``True`` iff a direct bridge ``source → target`` is legal.

    A bridge is legal when it is explicitly listed in
    :data:`ALLOWED_BRIDGES` and is not in :data:`FORBIDDEN_BRIDGES`.
    Identity bridges (``source == target``) are always legal.

    LEGACY FUNCTION: Delegates to is_legacy_bridge_allowed() for backward compatibility.
    New code should use is_canonical_bridge_allowed() or is_legacy_bridge_allowed() explicitly.
    """
    return is_legacy_bridge_allowed(source, target)


__all__ = [
    "Domain",
    # Legacy topology
    "ALLOWED_BRIDGES",
    "FORBIDDEN_BRIDGES",
    "is_bridge_allowed",
    "is_legacy_bridge_allowed",
    # Canonical GARA topology
    "CANONICAL_ALLOWED_BRIDGES",
    "CANONICAL_FORBIDDEN_BRIDGES",
    "is_canonical_bridge_allowed",
]
