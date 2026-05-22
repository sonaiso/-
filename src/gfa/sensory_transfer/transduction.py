"""
Transduction - The process of converting physical effect to neural/digital signal

For biological sensors: photoreceptors, hair cells, mechanoreceptors, etc.
For instruments: photodiodes, microphones, thermocouples, etc.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class TransductionProcess:
    """
    The process that converts the physical effect into a perceivable/measurable signal.

    CRITICAL: Transduction introduces limitations and transformations.
    What comes out is NOT identical to what went in.
    """

    transduction_type: str  # e.g., "photoreceptor", "microphone", "thermistor"

    # Transduction characteristics
    transduction_description: Optional[str] = None
    linearity_description: Optional[str] = None  # Is it linear? Non-linear?
    response_time_description: Optional[str] = None

    # Transduction limitations
    saturation_behavior: Optional[str] = None
    adaptation_behavior: Optional[str] = None

    def __post_init__(self):
        if not self.transduction_type or not self.transduction_type.strip():
            raise ValueError("TransductionProcess requires transduction_type")

    def __str__(self) -> str:
        return f"TransductionProcess({self.transduction_type})"
