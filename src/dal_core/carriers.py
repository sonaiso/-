"""
Unicode Carrier Contract (عقد الحامل)

Contract 1: Unicode → Carrier
Unicode is not a letter; it's a carrier that must pass through contracts.
"""

from dataclasses import dataclass
from typing import Optional
import unicodedata

from dal_core.residuals import Residual, make_blocker, ResidualType


@dataclass
class Carrier:
    """
    حامل (Carrier)

    A Unicode codepoint is NOT an Arabic letter.
    It's a neutral carrier that must be classified through contracts.

    This enforces Theorem 1: لا Unicode بلا عقد
    """
    char: str                    # Character as displayed
    codepoint: int              # U+XXXX numeric value
    index: int                  # Position in input stream
    unicode_name: str           # Official Unicode name

    def __post_init__(self):
        """Validate that this is truly a carrier, not a letter"""
        if len(self.char) != 1:
            raise ValueError(f"Carrier must be single character, got: {self.char!r}")

    def is_arabic_block(self) -> bool:
        """Check if in Arabic Unicode block"""
        return 0x0600 <= self.codepoint <= 0x06FF or \
               0x0750 <= self.codepoint <= 0x077F or \
               0x08A0 <= self.codepoint <= 0x08FF or \
               0xFB50 <= self.codepoint <= 0xFDFF or \
               0xFE70 <= self.codepoint <= 0xFEFF

    def __str__(self) -> str:
        return f"Carrier({self.char!r} U+{self.codepoint:04X} @{self.index})"

    def __repr__(self) -> str:
        return self.__str__()


def make_carrier(char: str, index: int) -> tuple[Optional[Carrier], list[Residual]]:
    """
    Create a carrier from a character.

    Returns (carrier, residuals) tuple.
    Non-Arabic characters produce blocker residuals.
    """
    residuals = []

    if len(char) != 1:
        residuals.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            f"Expected single character, got {len(char)} characters",
            location=f"index {index}"
        ))
        return None, residuals

    codepoint = ord(char)
    try:
        unicode_name = unicodedata.name(char, f"U+{codepoint:04X}")
    except ValueError:
        unicode_name = f"UNKNOWN-{codepoint:04X}"

    carrier = Carrier(
        char=char,
        codepoint=codepoint,
        index=index,
        unicode_name=unicode_name
    )

    # Check if in Arabic block
    if not carrier.is_arabic_block():
        # Check if it's whitespace or punctuation (allowed but marked)
        category = unicodedata.category(char)
        if category.startswith('Z'):  # Whitespace
            # Allow whitespace with info residual
            pass
        elif category.startswith('P'):  # Punctuation
            # Allow punctuation with info residual
            pass
        else:
            residuals.append(make_blocker(
                ResidualType.NON_ARABIC_SYMBOL,
                f"Character {char!r} not in Arabic Unicode block",
                location=f"index {index}",
                codepoint=codepoint,
                category=category
            ))

    return carrier, residuals


def text_to_carriers(text: str) -> tuple[list[Carrier], list[Residual]]:
    """
    Convert text to sequence of carriers.

    Returns (carriers, all_residuals) tuple.
    Skips characters that produce blocking residuals.
    """
    carriers = []
    all_residuals = []

    for i, char in enumerate(text):
        carrier, residuals = make_carrier(char, i)
        all_residuals.extend(residuals)

        if carrier is not None and not any(r.is_blocker() for r in residuals):
            carriers.append(carrier)

    return carriers, all_residuals
