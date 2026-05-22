"""
Sensory Transfer Kernel - Reality-to-Trace Bridge

This module implements the foundational layer proving that:
- Reality does NOT enter the algebra directly
- All traces come through channel-bound sensory or instrumental transfer
- Every transfer has inherent limitations, noise, and residuals
- Sensory trace ≠ External reality

Key Laws:
- No sensory transfer without channel
- No sensory transfer without time/place/reference
- No sensory transfer without retained trace
- No sensory transfer without noise/residual accounting
- Sensory trace is not external reality
- Visual/auditory signals do not certify sources
- Instrument traces require calibration
- Repeated transfer does not imply causality
- SensoryTransfer may produce FirstPriorUnit only as CANDIDATE or lower
- No CERTIFIED rank from sensory transfer alone

This is the bridge from physics/perception to knowledge.
"""

from .sensory_channel import SensoryChannel, ChannelType
from .source_effect import SourceEffect
from .medium import Medium
from .transduction import TransductionProcess
from .observer import Observer
from .instrument import Instrument, CalibrationState
from .signal import Signal
from .noise import NoiseProfile
from .sensory_trace import SensoryTrace
from .sensory_transfer import SensoryTransferEvent
from .sensory_transfer_validator import SensoryTransferValidator

__all__ = [
    "SensoryChannel",
    "ChannelType",
    "SourceEffect",
    "Medium",
    "TransductionProcess",
    "Observer",
    "Instrument",
    "CalibrationState",
    "Signal",
    "NoiseProfile",
    "SensoryTrace",
    "SensoryTransferEvent",
    "SensoryTransferValidator",
]
