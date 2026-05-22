"""
Medium - The physical medium through which the effect propagates

Examples:
- Air (for sound)
- Vacuum/space (for light)
- Solid material (for touch/vibration)
- Chemical solution (for taste/smell)
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Medium:
    """
    The medium through which the source effect propagates to the channel.

    The medium affects:
    - Propagation speed
    - Attenuation
    - Distortion
    - Noise introduction
    """

    medium_type: str  # e.g., "air", "vacuum", "water", "solid", "electromagnetic"

    # Medium properties (optional)
    medium_description: Optional[str] = None
    attenuation_description: Optional[str] = None
    dispersion_description: Optional[str] = None

    def __post_init__(self):
        if not self.medium_type or not self.medium_type.strip():
            raise ValueError("Medium requires medium_type")

    def __str__(self) -> str:
        return f"Medium({self.medium_type})"
