"""
Sensory Channels - The pathways through which reality effects are transferred

CRITICAL: The channel defines the limitations, bandwidth, and characteristics
of how reality can be perceived or measured.

Each channel has:
- Specific physical/perceptual basis
- Inherent bandwidth limitations
- Characteristic noise profile
- Detection thresholds
- Saturation limits
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Set, FrozenSet
from decimal import Decimal


class ChannelType(Enum):
    """Types of sensory or instrumental channels."""
    # Biological sensory channels
    VISUAL = auto()           # Light/electromagnetic (visible spectrum)
    AUDITORY = auto()         # Sound/pressure waves
    TACTILE = auto()          # Touch/pressure/texture
    OLFACTORY = auto()        # Smell/chemical detection
    GUSTATORY = auto()        # Taste/chemical detection
    PROPRIOCEPTIVE = auto()   # Body position/movement
    INTEROCEPTIVE = auto()    # Internal body states
    VESTIBULAR = auto()       # Balance/spatial orientation

    # Instrumental/measurement channels
    INSTRUMENTAL_EM = auto()        # Electromagnetic instruments (beyond visible)
    INSTRUMENTAL_ACOUSTIC = auto()  # Acoustic instruments (beyond audible)
    INSTRUMENTAL_THERMAL = auto()   # Temperature measurement
    INSTRUMENTAL_PRESSURE = auto()  # Pressure measurement
    INSTRUMENTAL_CHEMICAL = auto()  # Chemical analysis
    INSTRUMENTAL_MASS = auto()      # Mass/weight measurement
    INSTRUMENTAL_TIME = auto()      # Time measurement
    INSTRUMENTAL_SPATIAL = auto()   # Distance/position measurement

    # Abstract/computational channels
    COMPUTATIONAL = auto()    # Computed from other channels
    DERIVED = auto()          # Derived from combinations


@dataclass(frozen=True)
class SensoryChannel:
    """
    A sensory or instrumental channel through which effects are transferred.

    CRITICAL LAW: Every trace must declare its channel.
    No channel = no way to assess limitations, noise, or validity.
    """

    channel_type: ChannelType

    # Channel characteristics
    bandwidth_description: Optional[str] = None  # e.g., "380-750 nm wavelength"
    threshold_description: Optional[str] = None  # e.g., "minimum detectable intensity"
    saturation_description: Optional[str] = None  # e.g., "maximum before saturation"

    # Channel-specific parameters
    sensitivity: Optional[Decimal] = None
    resolution: Optional[Decimal] = None
    dynamic_range: Optional[Decimal] = None

    # Channel limitations
    known_limitations: Optional[FrozenSet[str]] = None
    known_artifacts: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        # Convert sets to frozensets for immutability
        if self.known_limitations and not isinstance(self.known_limitations, frozenset):
            object.__setattr__(self, 'known_limitations', frozenset(self.known_limitations))
        if self.known_artifacts and not isinstance(self.known_artifacts, frozenset):
            object.__setattr__(self, 'known_artifacts', frozenset(self.known_artifacts))

    @property
    def is_biological(self) -> bool:
        """Check if this is a biological sensory channel."""
        return self.channel_type in {
            ChannelType.VISUAL,
            ChannelType.AUDITORY,
            ChannelType.TACTILE,
            ChannelType.OLFACTORY,
            ChannelType.GUSTATORY,
            ChannelType.PROPRIOCEPTIVE,
            ChannelType.INTEROCEPTIVE,
            ChannelType.VESTIBULAR,
        }

    @property
    def is_instrumental(self) -> bool:
        """Check if this is an instrumental measurement channel."""
        return self.channel_type.name.startswith('INSTRUMENTAL_')

    @property
    def is_derived(self) -> bool:
        """Check if this channel is computed/derived."""
        return self.channel_type in {ChannelType.COMPUTATIONAL, ChannelType.DERIVED}

    def has_limitation(self, limitation: str) -> bool:
        """Check if channel has specific limitation."""
        if not self.known_limitations:
            return False
        return limitation in self.known_limitations

    def has_artifact(self, artifact: str) -> bool:
        """Check if channel produces specific artifact."""
        if not self.known_artifacts:
            return False
        return artifact in self.known_artifacts

    def __str__(self) -> str:
        return f"SensoryChannel({self.channel_type.name})"
