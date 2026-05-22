"""
DalType - أنواع الدال

Defines the types of linguistic signifiers (Dāl) that can serve
as carriers for potential signification.

Critical Law:
    الدال وحده حامل لفظي مرشح، لا معنى
    Dāl-alone is a signifier candidate, not meaning.

Signifier Types:
    - SOUND_SIGNIFIER: Acoustic/sound signifier (دال صوتي)
    - WRITTEN_SIGNIFIER: Written/manuscript signifier (دال كتابي)
    - SYMBOLIC_SIGNIFIER: Symbolic/formal signifier (دال رمزي)
    - ORTHOGRAPHIC_SIGNIFIER: Orthographic signifier (دال إملائي)
    - UNKNOWN_SIGNIFIER: Unknown signifier type (becomes residual, not error)

Critical:
    UNKNOWN signifier type does NOT raise exception.
    UNKNOWN becomes governed residual for future resolution.

What DalType Is:
    - Modality classifier for signifiers
    - Derived from LafziTraceType
    - Does NOT determine meaning
    - Does NOT create Madlul
    - Does NOT establish Dalalah

What DalType Is NOT:
    - NOT a semantic category
    - NOT a meaning type
    - NOT a Madlul classifier
    - NOT a Dalalah relation
"""

from __future__ import annotations
from enum import Enum


class DalType(Enum):
    """
    Types of linguistic signifiers (الدال).

    Each type represents a different modality of signifier
    derived from LafziTrace.

    UNKNOWN is a residual state, not an error state.
    """

    SOUND_SIGNIFIER = "sound_signifier"           # دال صوتي - Acoustic signifier
    WRITTEN_SIGNIFIER = "written_signifier"       # دال كتابي - Written signifier
    SYMBOLIC_SIGNIFIER = "symbolic_signifier"     # دال رمزي - Symbolic signifier
    ORTHOGRAPHIC_SIGNIFIER = "orthographic_signifier"  # دال إملائي - Orthographic
    UNKNOWN_SIGNIFIER = "unknown_signifier"       # دال مجهول - Unknown/unclassified

    @property
    def is_known(self) -> bool:
        """Check if signifier type is known (not UNKNOWN)."""
        return self != DalType.UNKNOWN_SIGNIFIER

    @property
    def is_sound(self) -> bool:
        """Check if signifier is sound-based."""
        return self == DalType.SOUND_SIGNIFIER

    @property
    def is_written(self) -> bool:
        """Check if signifier is written."""
        return self == DalType.WRITTEN_SIGNIFIER

    @property
    def is_symbolic(self) -> bool:
        """Check if signifier is symbolic."""
        return self == DalType.SYMBOLIC_SIGNIFIER

    @property
    def is_orthographic(self) -> bool:
        """Check if signifier is orthographic."""
        return self == DalType.ORTHOGRAPHIC_SIGNIFIER

    def __str__(self) -> str:
        return f"DalType.{self.name}"

    def __repr__(self) -> str:
        return f"DalType.{self.name}"
