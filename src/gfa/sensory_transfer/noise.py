"""
Noise Profile - The noise/error characteristics of the transfer

CRITICAL: Every sensory transfer has noise.
No noise accounting = hallucination risk.
"""

from dataclasses import dataclass
from typing import Optional, FrozenSet
from decimal import Decimal


@dataclass(frozen=True)
class NoiseProfile:
    """
    Noise and error characteristics of the sensory transfer.

    MANDATORY: Must be preserved to prevent treating noisy signal as perfect reality.
    """

    # Noise characteristics
    noise_level: Optional[Decimal] = None
    noise_type: Optional[str] = None  # e.g., "thermal", "shot", "quantization", "perceptual"

    # Error characteristics
    systematic_error: Optional[Decimal] = None
    random_error: Optional[Decimal] = None
    error_description: Optional[str] = None

    # Known noise sources
    noise_sources: Optional[FrozenSet[str]] = None

    # Signal-to-noise ratio (if applicable)
    snr: Optional[Decimal] = None

    def __post_init__(self):
        # At least one noise/error indicator should be present
        if not any([
            self.noise_level,
            self.noise_type,
            self.systematic_error,
            self.random_error,
            self.noise_sources,
            self.error_description
        ]):
            raise ValueError(
                "NoiseProfile requires at least one noise/error indicator. "
                "If truly noise-free, explicitly state noise_type='none' or noise_level=0"
            )

        # Convert to frozenset for immutability
        if self.noise_sources and not isinstance(self.noise_sources, frozenset):
            object.__setattr__(self, 'noise_sources', frozenset(self.noise_sources))

    @property
    def has_significant_noise(self) -> bool:
        """Check if noise is significant."""
        if self.noise_level and self.noise_level > Decimal("0.1"):
            return True
        if self.snr and self.snr < Decimal("10"):  # SNR < 10 dB is noisy
            return True
        return False

    @property
    def is_noise_free(self) -> bool:
        """Check if explicitly declared noise-free."""
        return (
            self.noise_type == "none" or
            (self.noise_level is not None and self.noise_level == Decimal("0"))
        )

    def __str__(self) -> str:
        if self.snr:
            return f"NoiseProfile(SNR={self.snr}dB)"
        elif self.noise_level:
            return f"NoiseProfile(level={self.noise_level})"
        else:
            return f"NoiseProfile(type={self.noise_type})"
