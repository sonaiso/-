"""
Instrument - Measurement instruments and their calibration state

CRITICAL LAW: Instrument traces REQUIRE calibration state.
No calibration = unknown systematic error = unreliable measurement.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional
from datetime import datetime


class CalibrationStatus(Enum):
    """Calibration status of an instrument."""
    UNCALIBRATED = auto()      # Never calibrated or calibration unknown
    CALIBRATED = auto()         # Recently calibrated
    EXPIRED = auto()            # Calibration expired
    VERIFIED = auto()           # Calibration verified against standard
    QUESTIONABLE = auto()       # Calibration questionable


@dataclass(frozen=True)
class CalibrationState:
    """
    Calibration state of an instrument.

    MANDATORY for instrument traces.
    """

    calibration_status: CalibrationStatus

    # Calibration details (optional)
    calibration_date: Optional[datetime] = None
    calibration_standard: Optional[str] = None
    calibration_uncertainty: Optional[str] = None
    calibration_notes: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.calibration_status, CalibrationStatus):
            raise ValueError("CalibrationState requires valid CalibrationStatus")

    @property
    def is_reliable(self) -> bool:
        """Check if calibration is reliable."""
        return self.calibration_status in {
            CalibrationStatus.CALIBRATED,
            CalibrationStatus.VERIFIED
        }

    @property
    def is_questionable(self) -> bool:
        """Check if calibration is questionable."""
        return self.calibration_status in {
            CalibrationStatus.UNCALIBRATED,
            CalibrationStatus.EXPIRED,
            CalibrationStatus.QUESTIONABLE
        }

    def __str__(self) -> str:
        return f"CalibrationState({self.calibration_status.name})"


@dataclass(frozen=True)
class Instrument:
    """
    A measurement instrument used in sensory transfer.

    CRITICAL LAW: Instruments MUST declare calibration state.
    """

    instrument_id: str
    instrument_type: str  # e.g., "thermometer", "microscope", "spectrometer"

    # MANDATORY for instruments
    calibration_state: CalibrationState

    # Instrument characteristics (optional)
    instrument_description: Optional[str] = None
    accuracy_spec: Optional[str] = None
    precision_spec: Optional[str] = None

    def __post_init__(self):
        if not self.instrument_id or not self.instrument_id.strip():
            raise ValueError("Instrument requires instrument_id")
        if not self.instrument_type or not self.instrument_type.strip():
            raise ValueError("Instrument requires instrument_type")
        if not isinstance(self.calibration_state, CalibrationState):
            raise ValueError("Instrument requires CalibrationState")

    @property
    def has_reliable_calibration(self) -> bool:
        """Check if instrument has reliable calibration."""
        return self.calibration_state.is_reliable

    def __str__(self) -> str:
        return f"Instrument({self.instrument_type}, cal={self.calibration_state.calibration_status.name})"
