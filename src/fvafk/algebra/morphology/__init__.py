"""Algebraic morphology operations (Phase 3).

الصرف الجبري لا يحكم بالمعنى، بل يرخص بنية صرفية محفوظة الأثر والرتبة والبقايا.

Morphology operations transition from plain functions to governed
algebraic operations that produce Result objects with:

- **value**: The morphological structure (root, pattern, affix set)
- **rank**: Epistemic status (UNRESOLVED → CANDIDATE → LICENSED → CERTIFIED)
- **evidence**: Supporting observations from adapters
- **residuals**: Explicit gaps (ambiguity, weak letters, context absence)
- **failures**: Active contradictions
- **trace**: Replayable provenance

Core principles:

1. **الجذر ليس معنى** (ROOT is not meaning): Root extraction supports
   ROOT domain claims only, never SEMANTICS or HUKM.
2. **الوزن ليس حكماً** (Pattern is not judgment): Pattern matching
   licenses MORPH_SURFACE claims, not semantic conclusions.
3. **الاشتقاق ليس دلالة نهائية** (Derivation is not final semantics):
   Augmentation operators emit MORPH_DEEP evidence without claiming
   meaning.
4. **الصرف يرخص بنية** (Morphology licenses structure): All operations
   stay LICENSED when residuals remain; CERTIFIED requires full
   resolution.

Operations:

- :class:`PatternMatchOperation` — MORPH_SURFACE candidate + Evidence → Result
- :class:`RootExtractionOperation` — ROOT evidence → Result
- :class:`AffixDetectionOperation` — Affix stripping with residuals
- :func:`governed_pattern_match` — Convenience wrapper
- :func:`governed_root_extract` — Convenience wrapper
- :func:`governed_affix_detect` — Convenience wrapper

Residual taxonomy:

- ``context.absent`` — Missing surrounding tokens
- ``lexical.ambiguity`` — Multiple valid interpretations
- ``proper_name.possible`` — Could be proper noun
- ``transfer.possible`` — Could be loanword/transliteration
- ``weak_letter.present`` — Weak radicals (و، ي، alif)
- ``affix.aggressive_strip`` — Over-zealous prefix/suffix removal
- ``root.ambiguous`` — Multiple root candidates
- ``pattern.collision`` — Multiple patterns match
- ``broken_plural.possible`` — Could be broken plural form
"""

from __future__ import annotations

from .residual_taxonomy import (
    MORPHOLOGY_RESIDUAL_KINDS,
    make_context_absent,
    make_lexical_ambiguity,
    make_proper_name_possible,
    make_transfer_possible,
    make_weak_letter_present,
    make_affix_aggressive_strip,
    make_root_ambiguous,
    make_pattern_collision,
    make_broken_plural_possible,
)

from .operations import (
    PatternMatchOperation,
    RootExtractionOperation,
    AffixDetectionOperation,
    governed_pattern_match,
    governed_root_extract,
    governed_affix_detect,
)

__all__ = [
    # Residual taxonomy
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
    # Operations
    "PatternMatchOperation",
    "RootExtractionOperation",
    "AffixDetectionOperation",
    "governed_pattern_match",
    "governed_root_extract",
    "governed_affix_detect",
]
