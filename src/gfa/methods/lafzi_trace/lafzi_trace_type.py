"""
LafziTraceType - أنواع الأثر اللفظي

Defines the types of linguistic traces that can serve as input
to LafziMadlul processing.

Critical Law:
    الأثر اللفظي شرط إمكان، لا معنى
    LafziTrace is a condition for possibility, not meaning.

Trace Types:
    - ACOUSTIC: Sound/audio trace (صوتي)
    - WRITTEN: Written/manuscript trace (كتابي)
    - UNICODE: Unicode character trace (يونيكود)
    - ORTHOGRAPHIC: Orthographic/spelling trace (إملائي)
    - PHONOLOGICAL: Phonological representation (صوتيات)
    - SYMBOLIC: Symbolic/formal notation (رمزي)
    - UNKNOWN: Unknown trace type (becomes residual, not error)

Critical:
    UNKNOWN trace type does NOT raise exception.
    UNKNOWN becomes governed residual for future resolution.
"""

from __future__ import annotations
from enum import Enum


class LafziTraceType(Enum):
    """
    Types of linguistic traces.

    Each type represents a different modality of linguistic input.
    All types are equally valid as entry points for Lafzi processing.

    UNKNOWN is a residual state, not an error state.
    """

    ACOUSTIC = "acoustic"           # صوتي - Sound/audio recording
    WRITTEN = "written"             # كتابي - Written/manuscript text
    UNICODE = "unicode"             # يونيكود - Unicode character sequence
    ORTHOGRAPHIC = "orthographic"   # إملائي - Orthographic representation
    PHONOLOGICAL = "phonological"   # صوتيات - Phonological transcription
    SYMBOLIC = "symbolic"           # رمزي - Symbolic/formal notation
    UNKNOWN = "unknown"             # مجهول - Unknown/unclassified trace

    @property
    def is_known(self) -> bool:
        """Check if trace type is known (not UNKNOWN)."""
        return self != LafziTraceType.UNKNOWN

    @property
    def is_acoustic(self) -> bool:
        """Check if trace is acoustic."""
        return self == LafziTraceType.ACOUSTIC

    @property
    def is_written(self) -> bool:
        """Check if trace is written."""
        return self == LafziTraceType.WRITTEN

    @property
    def is_unicode(self) -> bool:
        """Check if trace is unicode."""
        return self == LafziTraceType.UNICODE

    @property
    def is_orthographic(self) -> bool:
        """Check if trace is orthographic."""
        return self == LafziTraceType.ORTHOGRAPHIC

    @property
    def is_phonological(self) -> bool:
        """Check if trace is phonological."""
        return self == LafziTraceType.PHONOLOGICAL

    @property
    def is_symbolic(self) -> bool:
        """Check if trace is symbolic."""
        return self == LafziTraceType.SYMBOLIC

    def __str__(self) -> str:
        return f"LafziTraceType.{self.name}"

    def __repr__(self) -> str:
        return f"LafziTraceType.{self.name}"
