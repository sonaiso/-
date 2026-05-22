"""
Sensory Transfer Event - The complete record of reality-to-trace transfer

This is the CORE object establishing that reality enters the algebra
only through channel-bound, time/place/reference anchored, noisy transfer.

CRITICAL LAWS:
1. No sensory transfer without channel
2. No sensory transfer without time/place/reference
3. No sensory transfer without retained trace
4. No sensory transfer without noise profile
5. Sensory trace ≠ external reality
6. SensoryTransfer → FirstPriorUnit(rank ≤ CANDIDATE)
"""

from dataclasses import dataclass, field
from typing import Optional, Union, FrozenSet
from uuid import UUID, uuid4

from gfa.proto_prior.time_anchor import TimeAnchor
from gfa.proto_prior.place_anchor import PlaceAnchor
from gfa.proto_prior.reference_anchor import ReferenceAnchor
from gfa.proto_prior.first_prior_unit import Rank, Residual

from .sensory_channel import SensoryChannel
from .source_effect import SourceEffect
from .medium import Medium
from .transduction import TransductionProcess
from .observer import Observer
from .instrument import Instrument
from .signal import Signal
from .noise import NoiseProfile
from .sensory_trace import SensoryTrace


@dataclass(frozen=True)
class SensoryTransferEvent:
    """
    Complete record of a sensory transfer from claimed reality to preserved trace.

    This establishes the bridge: Reality → Channel → Trace → FirstPriorUnit

    MANDATORY fields (12):
    1. source_effect: Claimed external reality
    2. channel: How the effect was transferred
    3. time_anchor: When transfer occurred
    4. place_anchor: Where transfer occurred
    5. reference_anchor: What/who it refers to
    6. signal: What was actually received
    7. noise_profile: Noise/error characteristics
    8. retained_trace: What was preserved
    9. medium: Propagation medium
    10. transduction: Conversion process
    11. observer_or_instrument: Who/what received it
    12. residuals: Unresolved aspects

    Plus: rank (CANNOT exceed CANDIDATE from sensory transfer alone)
    """

    # Source (CLAIMED, not proven)
    source_effect: SourceEffect

    # Channel (MANDATORY - defines how transfer occurred)
    channel: SensoryChannel

    # Anchoring (MANDATORY - no transfer without time/place/reference)
    time_anchor: TimeAnchor
    place_anchor: PlaceAnchor
    reference_anchor: ReferenceAnchor

    # What was actually received (MANDATORY)
    signal: Signal
    noise_profile: NoiseProfile
    retained_trace: SensoryTrace

    # Transfer pathway
    medium: Medium
    transduction: TransductionProcess

    # Observer/instrument (MANDATORY - who/what received it)
    observer_or_instrument: Union[Observer, Instrument]

    # Threshold (optional - detection/measurement threshold)
    threshold: Optional[str] = None

    # Fields with defaults (must come last)
    transfer_id: UUID = field(default_factory=uuid4)
    residuals: FrozenSet[Residual] = field(default_factory=frozenset)
    rank: Rank = Rank.CANDIDATE  # CANNOT exceed CANDIDATE from sensory alone

    def __post_init__(self):
        # Validate all mandatory fields
        self._validate_mandatory_fields()

        # Enforce rank ceiling
        self._validate_rank_constraints()

        # Convert residuals to frozenset
        if self.residuals and not isinstance(self.residuals, frozenset):
            object.__setattr__(self, 'residuals', frozenset(self.residuals))

    def _validate_mandatory_fields(self):
        """Validate all mandatory fields are present and valid."""
        # Check source_effect
        if not isinstance(self.source_effect, SourceEffect):
            raise ValueError("source_effect is mandatory")

        # Check channel
        if not isinstance(self.channel, SensoryChannel):
            raise ValueError("channel is mandatory - no sensory transfer without channel")

        # Check time_anchor
        if not isinstance(self.time_anchor, TimeAnchor):
            raise ValueError("time_anchor is mandatory")
        if not self.time_anchor.is_valid:
            raise ValueError("time_anchor must be valid")

        # Check place_anchor
        if not isinstance(self.place_anchor, PlaceAnchor):
            raise ValueError("place_anchor is mandatory")
        if not self.place_anchor.is_valid:
            raise ValueError("place_anchor must be valid")

        # Check reference_anchor
        if not isinstance(self.reference_anchor, ReferenceAnchor):
            raise ValueError("reference_anchor is mandatory")
        if not self.reference_anchor.is_valid:
            raise ValueError("reference_anchor must be valid")

        # Check signal
        if not isinstance(self.signal, Signal):
            raise ValueError("signal is mandatory - must record what was actually received")

        # Check noise_profile
        if not isinstance(self.noise_profile, NoiseProfile):
            raise ValueError("noise_profile is mandatory - no transfer without noise accounting")

        # Check retained_trace
        if not isinstance(self.retained_trace, SensoryTrace):
            raise ValueError("retained_trace is mandatory - no transfer without preserved trace")

        # Check medium
        if not isinstance(self.medium, Medium):
            raise ValueError("medium is mandatory")

        # Check transduction
        if not isinstance(self.transduction, TransductionProcess):
            raise ValueError("transduction is mandatory")

        # Check observer_or_instrument
        if not isinstance(self.observer_or_instrument, (Observer, Instrument)):
            raise ValueError("observer_or_instrument is mandatory")

    def _validate_rank_constraints(self):
        """Validate rank constraints."""
        # CRITICAL LAW: Sensory transfer alone cannot produce CERTIFIED rank
        if self.rank == Rank.CERTIFIED:
            raise ValueError(
                "Sensory transfer alone cannot produce CERTIFIED rank. "
                "CERTIFIED requires independent verification beyond sensory transfer."
            )

        # Sensory transfer typically limited to CANDIDATE or OBSERVED
        if self.rank not in {Rank.CANDIDATE, Rank.OBSERVED}:
            raise ValueError(
                f"Sensory transfer should produce CANDIDATE or OBSERVED rank, not {self.rank.name}. "
                "Higher ranks require additional evidence/corroboration."
            )

    @property
    def is_instrumental(self) -> bool:
        """Check if this is an instrumental measurement."""
        return isinstance(self.observer_or_instrument, Instrument)

    @property
    def is_biological(self) -> bool:
        """Check if this is biological perception."""
        return isinstance(self.observer_or_instrument, Observer)

    @property
    def has_reliable_calibration(self) -> bool:
        """Check if instrument has reliable calibration (only for instrumental)."""
        if not self.is_instrumental:
            return False
        return self.observer_or_instrument.has_reliable_calibration

    @property
    def has_significant_noise(self) -> bool:
        """Check if transfer has significant noise."""
        return self.noise_profile.has_significant_noise

    @property
    def has_residuals(self) -> bool:
        """Check if transfer has unresolved residuals."""
        return bool(self.residuals)

    def can_certify_source(self) -> bool:
        """
        Can this sensory transfer certify its source?

        CRITICAL LAW: NO. Sensory transfer cannot certify source.
        Signal indicates something, but doesn't prove what the source is.
        """
        return False

    def can_certify_causality(self) -> bool:
        """
        Can this sensory transfer certify causality?

        CRITICAL LAW: NO. Even repeated transfer doesn't prove causality.
        Correlation ≠ causation.
        """
        return False

    def can_certify_reality(self) -> bool:
        """
        Can this sensory transfer certify external reality?

        CRITICAL LAW: NO. Trace is evidence of reality, not reality itself.
        """
        return False

    def equals_external_reality(self) -> bool:
        """
        Does this sensory trace equal external reality?

        CRITICAL LAW: NO. Sensory trace ≠ external reality.
        The trace is a limited, noisy representation.
        """
        return False

    def __str__(self) -> str:
        return (
            f"SensoryTransferEvent("
            f"channel={self.channel.channel_type.name}, "
            f"signal_quality={self.signal.signal_quality}, "
            f"rank={self.rank.name})"
        )
