"""
Sensory Transfer Validator - Enforces all constitutional laws

This validator ensures:
1. No sensory transfer without channel
2. No sensory transfer without time/place/reference
3. No sensory transfer without retained trace
4. No sensory transfer without noise profile
5. Sensory trace ≠ external reality
6. Visual/auditory signals do not certify sources
7. Instrument traces require calibration
8. Repeated transfer does not imply causality
9. Sensory transfer produces only CANDIDATE/OBSERVED rank
10. No CERTIFIED rank from sensory transfer alone
"""

from typing import Optional

from .sensory_transfer import SensoryTransferEvent
from .sensory_channel import ChannelType
from .instrument import Instrument, CalibrationStatus
from gfa.proto_prior.first_prior_unit import Rank


class ValidationError(Exception):
    """Validation error in sensory transfer."""
    pass


class SensoryTransferValidator:
    """
    Validator enforcing all sensory transfer constitutional laws.
    """

    @staticmethod
    def validate_sensory_transfer_event(event: SensoryTransferEvent) -> None:
        """
        Validate a sensory transfer event against all laws.

        Raises ValidationError if any law is violated.
        """
        # Law 1: No sensory transfer without channel
        if not event.channel:
            raise ValidationError("No sensory transfer without channel")

        # Law 2: No sensory transfer without time/place/reference
        if not event.time_anchor or not event.time_anchor.is_valid:
            raise ValidationError("No sensory transfer without valid time anchor")
        if not event.place_anchor or not event.place_anchor.is_valid:
            raise ValidationError("No sensory transfer without valid place anchor")
        if not event.reference_anchor or not event.reference_anchor.is_valid:
            raise ValidationError("No sensory transfer without valid reference anchor")

        # Law 3: No sensory transfer without retained trace
        if not event.retained_trace:
            raise ValidationError("No sensory transfer without retained trace")

        # Law 4: No sensory transfer without noise profile
        if not event.noise_profile:
            raise ValidationError("No sensory transfer without noise/residual accounting")

        # Law 9: Rank ceiling at OBSERVED
        if event.rank not in {Rank.CANDIDATE, Rank.OBSERVED}:
            raise ValidationError(
                f"Sensory transfer cannot produce {event.rank.name} rank. "
                "Limited to CANDIDATE or OBSERVED."
            )

        # Law 10: No CERTIFIED from sensory transfer alone
        if event.rank == Rank.CERTIFIED:
            raise ValidationError(
                "No CERTIFIED rank from sensory transfer alone. "
                "Requires independent verification."
            )

    @staticmethod
    def validate_instrument_requires_calibration(event: SensoryTransferEvent) -> None:
        """
        Validate that instrument traces have calibration state.

        Law 7: Instrument trace requires calibration.
        """
        if event.is_instrumental:
            instrument = event.observer_or_instrument
            if not isinstance(instrument, Instrument):
                raise ValidationError("Instrumental transfer must use Instrument")

            if not instrument.calibration_state:
                raise ValidationError("Instrument trace requires calibration state")

            # Warn if calibration is questionable
            if instrument.calibration_state.is_questionable:
                # This is a warning, not an error, but should be noted in residuals
                pass

    @staticmethod
    def validate_sensory_trace_not_reality(event: SensoryTransferEvent) -> None:
        """
        Validate that sensory trace is not treated as external reality.

        Law 5: Sensory trace ≠ external reality.
        """
        # This is enforced by design (no method claims equality)
        # But we check the semantic distinction is preserved
        if event.equals_external_reality():
            raise ValidationError(
                "Sensory trace cannot equal external reality. "
                "Trace is evidence, not reality itself."
            )

    @staticmethod
    def validate_signal_does_not_certify_source(event: SensoryTransferEvent) -> None:
        """
        Validate that visual/auditory signals do not certify their sources.

        Law 6: Visual/auditory signals do not certify source.
        """
        if event.can_certify_source():
            raise ValidationError(
                f"{event.channel.channel_type.name} signal cannot certify source. "
                "Signal indicates something, but doesn't prove what the source is."
            )

    @staticmethod
    def validate_repeated_transfer_not_causality(
        event1: SensoryTransferEvent,
        event2: SensoryTransferEvent
    ) -> None:
        """
        Validate that repeated sensory transfer does not imply causality.

        Law 8: Repeated transfer ≠ causality.
        """
        # Even if two events are temporally ordered, this doesn't prove causation
        # This is a conceptual law enforced by API design (no causality claims)
        # If either event claimed to certify causality, it would be an error
        if event1.can_certify_causality() or event2.can_certify_causality():
            raise ValidationError(
                "Sensory transfer cannot certify causality. "
                "Temporal sequence ≠ causal relationship."
            )

    @staticmethod
    def check_minimal_sensory_requirements(event: SensoryTransferEvent) -> bool:
        """
        Check if event meets minimal requirements for sensory transfer.

        Returns True if all minimal requirements are met.
        """
        try:
            SensoryTransferValidator.validate_sensory_transfer_event(event)
            SensoryTransferValidator.validate_instrument_requires_calibration(event)
            SensoryTransferValidator.validate_sensory_trace_not_reality(event)
            SensoryTransferValidator.validate_signal_does_not_certify_source(event)
            return True
        except ValidationError:
            return False
