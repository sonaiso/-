"""
Signal - The actual signal received through the channel

The signal is what we ACTUALLY receive, not what we claim exists externally.
"""

from dataclasses import dataclass
from typing import Any, Optional
from decimal import Decimal


@dataclass(frozen=True)
class Signal:
    """
    The actual signal received through the sensory channel.

    This is what was DETECTED, not what exists externally.
    """

    signal_value: Any  # The measured/perceived value

    # Signal characteristics
    signal_strength: Optional[Decimal] = None
    signal_quality: Optional[str] = None  # e.g., "clear", "noisy", "distorted"

    # Signal metadata
    signal_description: Optional[str] = None

    def __post_init__(self):
        if self.signal_value is None:
            raise ValueError("Signal requires signal_value")

    def __str__(self) -> str:
        return f"Signal(value={self.signal_value}, quality={self.signal_quality})"
