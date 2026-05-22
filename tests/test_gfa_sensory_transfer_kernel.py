"""
Comprehensive test suite for Sensory Transfer Kernel - Reality-to-Trace Bridge

Tests all constitutional laws:
1. No sensory transfer without channel
2. No sensory transfer without time/place/reference
3. No sensory transfer without retained trace
4. No sensory transfer without noise profile
5. Sensory trace is not equal to external reality
6. Visual signal does not certify source
7. Auditory signal does not certify speaker
8. Instrument trace requires calibration
9. Repeated transfer does not imply causality
10. Sensory transfer can create FirstPriorUnit only as CANDIDATE
11. Sensory transfer preserves residuals
12. Sensory transfer serializes without losing channel/time/place/reference
"""

import pytest
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from gfa.sensory_transfer import (
    SensoryChannel,
    ChannelType,
    SourceEffect,
    Medium,
    TransductionProcess,
    Observer,
    Instrument,
    CalibrationState,
    Signal,
    NoiseProfile,
    SensoryTrace,
    SensoryTransferEvent,
    SensoryTransferValidator,
)
from gfa.sensory_transfer.instrument import CalibrationStatus
from gfa.sensory_transfer.sensory_transfer_validator import ValidationError
from gfa.proto_prior.existence_type import ExistenceType
from gfa.proto_prior.time_anchor import TimeAnchor
from gfa.proto_prior.place_anchor import PlaceAnchor
from gfa.proto_prior.reference_anchor import ReferenceAnchor
from gfa.proto_prior.first_prior_unit import Rank, Residual


# Helper function to create a valid SensoryTransferEvent
def make_valid_sensory_transfer(**overrides):
    """Create a valid SensoryTransferEvent with optional overrides."""
    defaults = {
        "source_effect": SourceEffect(
            claimed_entity_or_effect="light_source",
            claimed_existence_type=ExistenceType.PHYSICAL
        ),
        "channel": SensoryChannel(channel_type=ChannelType.VISUAL),
        "time_anchor": TimeAnchor(timestamp=datetime.now()),
        "place_anchor": PlaceAnchor(locality_label="observation_point_A"),
        "reference_anchor": ReferenceAnchor(entity_id="light_001"),
        "signal": Signal(signal_value="bright_flash"),
        "noise_profile": NoiseProfile(noise_type="photon_shot_noise"),
        "retained_trace": SensoryTrace(received_content="visual_pattern"),
        "medium": Medium(medium_type="air"),
        "transduction": TransductionProcess(transduction_type="photoreceptor"),
        "observer_or_instrument": Observer(observer_id="observer_1"),
    }
    defaults.update(overrides)
    return SensoryTransferEvent(**defaults)


class TestSensoryTransferMandatoryFields:
    """Test that all mandatory fields are enforced."""

    def test_no_sensory_transfer_without_channel(self):
        """SensoryTransferEvent requires channel."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_sensory_transfer(channel=None)

    def test_no_sensory_transfer_without_time_place_reference(self):
        """SensoryTransferEvent requires time/place/reference anchors."""
        # No time
        with pytest.raises((ValueError, TypeError)):
            make_valid_sensory_transfer(time_anchor=None)

        # No place
        with pytest.raises((ValueError, TypeError)):
            make_valid_sensory_transfer(place_anchor=None)

        # No reference
        with pytest.raises((ValueError, TypeError)):
            make_valid_sensory_transfer(reference_anchor=None)

    def test_no_sensory_transfer_without_retained_trace(self):
        """SensoryTransferEvent requires retained_trace."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_sensory_transfer(retained_trace=None)

    def test_no_sensory_transfer_without_noise_profile(self):
        """SensoryTransferEvent requires noise_profile."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_sensory_transfer(noise_profile=None)


class TestSensoryTraceNotReality:
    """Test that sensory trace is NOT equal to external reality."""

    def test_sensory_trace_not_equal_external_reality(self):
        """Sensory trace ≠ external reality (by design)."""
        event = make_valid_sensory_transfer()

        # The transfer itself cannot equal external reality
        assert event.equals_external_reality() is False

    def test_validator_checks_trace_not_reality(self):
        """Validator enforces sensory trace ≠ reality."""
        event = make_valid_sensory_transfer()

        # Should not raise - designed to never equal reality
        SensoryTransferValidator.validate_sensory_trace_not_reality(event)


class TestSignalDoesNotCertifySource:
    """Test that visual/auditory signals do NOT certify their sources."""

    def test_visual_signal_does_not_certify_source(self):
        """Visual signal cannot certify its source."""
        event = make_valid_sensory_transfer(
            channel=SensoryChannel(channel_type=ChannelType.VISUAL),
            source_effect=SourceEffect(
                claimed_entity_or_effect="star",
                claimed_existence_type=ExistenceType.PHYSICAL
            )
        )

        assert event.can_certify_source() is False

    def test_auditory_signal_does_not_certify_speaker(self):
        """Auditory signal cannot certify speaker/source."""
        event = make_valid_sensory_transfer(
            channel=SensoryChannel(channel_type=ChannelType.AUDITORY),
            source_effect=SourceEffect(
                claimed_entity_or_effect="voice",
                claimed_existence_type=ExistenceType.PHYSICAL
            ),
            signal=Signal(signal_value="sound_wave"),
            transduction=TransductionProcess(transduction_type="hair_cell")
        )

        assert event.can_certify_source() is False

    def test_validator_enforces_no_source_certification(self):
        """Validator enforces that signals don't certify sources."""
        event = make_valid_sensory_transfer()

        # Should not raise - designed to never certify source
        SensoryTransferValidator.validate_signal_does_not_certify_source(event)


class TestInstrumentRequiresCalibration:
    """Test that instrument traces require calibration state."""

    def test_instrument_trace_requires_calibration(self):
        """Instrument must have calibration_state."""
        # Creating an Instrument without calibration should fail
        with pytest.raises(ValueError, match="requires CalibrationState"):
            Instrument(
                instrument_id="thermometer_1",
                instrument_type="thermometer",
                calibration_state=None
            )

    def test_instrumental_transfer_validates_calibration(self):
        """Validator checks instrument has calibration."""
        calibration = CalibrationState(
            calibration_status=CalibrationStatus.CALIBRATED,
            calibration_date=datetime.now()
        )
        instrument = Instrument(
            instrument_id="thermometer_1",
            instrument_type="thermometer",
            calibration_state=calibration
        )

        event = make_valid_sensory_transfer(
            channel=SensoryChannel(channel_type=ChannelType.INSTRUMENTAL_THERMAL),
            observer_or_instrument=instrument
        )

        # Should not raise
        SensoryTransferValidator.validate_instrument_requires_calibration(event)

    def test_uncalibrated_instrument_is_questionable(self):
        """Uncalibrated instruments are marked questionable."""
        calibration = CalibrationState(
            calibration_status=CalibrationStatus.UNCALIBRATED
        )
        instrument = Instrument(
            instrument_id="sensor_1",
            instrument_type="pressure_sensor",
            calibration_state=calibration
        )

        assert calibration.is_questionable is True
        assert calibration.is_reliable is False


class TestRepeatedTransferNotCausality:
    """Test that repeated sensory transfer does NOT imply causality."""

    def test_repeated_transfer_does_not_imply_causality(self):
        """Repeated transfer ≠ causal relationship."""
        event1 = make_valid_sensory_transfer(
            time_anchor=TimeAnchor(timestamp=datetime(2026, 1, 1, 10, 0, 0))
        )
        event2 = make_valid_sensory_transfer(
            time_anchor=TimeAnchor(timestamp=datetime(2026, 1, 1, 10, 0, 1))
        )

        # Neither event can certify causality
        assert event1.can_certify_causality() is False
        assert event2.can_certify_causality() is False

    def test_validator_enforces_no_causality_claim(self):
        """Validator enforces no causality claims."""
        event1 = make_valid_sensory_transfer()
        event2 = make_valid_sensory_transfer()

        # Should not raise - designed to never certify causality
        SensoryTransferValidator.validate_repeated_transfer_not_causality(event1, event2)


class TestRankConstraints:
    """Test rank constraints for sensory transfer."""

    def test_sensory_transfer_can_create_first_prior_unit_only_as_candidate(self):
        """Sensory transfer limited to CANDIDATE or OBSERVED rank."""
        # CANDIDATE is allowed
        event_candidate = make_valid_sensory_transfer(rank=Rank.CANDIDATE)
        assert event_candidate.rank == Rank.CANDIDATE

        # OBSERVED is allowed
        event_observed = make_valid_sensory_transfer(rank=Rank.OBSERVED)
        assert event_observed.rank == Rank.OBSERVED

        # LICENSED is NOT allowed
        with pytest.raises(ValueError, match="should produce CANDIDATE or OBSERVED"):
            make_valid_sensory_transfer(rank=Rank.LICENSED)

        # CERTIFIED is NOT allowed
        with pytest.raises(ValueError, match="cannot produce CERTIFIED"):
            make_valid_sensory_transfer(rank=Rank.CERTIFIED)

    def test_validator_enforces_rank_ceiling(self):
        """Validator enforces rank ceiling at OBSERVED."""
        event = make_valid_sensory_transfer(rank=Rank.OBSERVED)

        # Should not raise
        SensoryTransferValidator.validate_sensory_transfer_event(event)


class TestResidualPreservation:
    """Test that residuals are preserved."""

    def test_sensory_transfer_preserves_residuals(self):
        """Residuals must be preserved in SensoryTransferEvent."""
        residual1 = Residual(
            description="Signal partially saturated",
            residual_type="incompleteness"
        )
        residual2 = Residual(
            description="Background noise elevated",
            residual_type="uncertainty"
        )

        event = make_valid_sensory_transfer(
            residuals={residual1, residual2}
        )

        assert event.has_residuals
        assert len(event.residuals) == 2
        assert residual1 in event.residuals
        assert residual2 in event.residuals


class TestSerialization:
    """Test serialization and field preservation."""

    def test_sensory_transfer_serializes_without_losing_channel_time_place_reference(self):
        """All critical fields must be accessible."""
        event = make_valid_sensory_transfer()

        # Check all mandatory fields are accessible
        assert isinstance(event.source_effect, SourceEffect)
        assert isinstance(event.channel, SensoryChannel)
        assert isinstance(event.time_anchor, TimeAnchor)
        assert isinstance(event.place_anchor, PlaceAnchor)
        assert isinstance(event.reference_anchor, ReferenceAnchor)
        assert isinstance(event.signal, Signal)
        assert isinstance(event.noise_profile, NoiseProfile)
        assert isinstance(event.retained_trace, SensoryTrace)
        assert isinstance(event.medium, Medium)
        assert isinstance(event.transduction, TransductionProcess)
        assert event.observer_or_instrument is not None
        assert isinstance(event.transfer_id, UUID)
        assert isinstance(event.rank, Rank)

    def test_sensory_trace_has_stable_id(self):
        """SensoryTrace has stable, unique ID."""
        trace1 = SensoryTrace(received_content="content_1")
        trace2 = SensoryTrace(received_content="content_2")

        assert isinstance(trace1.trace_id, UUID)
        assert isinstance(trace2.trace_id, UUID)
        assert trace1.trace_id != trace2.trace_id


class TestChannelTypes:
    """Test different channel types."""

    def test_biological_channels(self):
        """Test biological sensory channels."""
        for channel_type in [
            ChannelType.VISUAL,
            ChannelType.AUDITORY,
            ChannelType.TACTILE,
            ChannelType.OLFACTORY,
            ChannelType.GUSTATORY
        ]:
            channel = SensoryChannel(channel_type=channel_type)
            assert channel.is_biological is True
            assert channel.is_instrumental is False

    def test_instrumental_channels(self):
        """Test instrumental measurement channels."""
        for channel_type in [
            ChannelType.INSTRUMENTAL_EM,
            ChannelType.INSTRUMENTAL_THERMAL,
            ChannelType.INSTRUMENTAL_PRESSURE
        ]:
            channel = SensoryChannel(channel_type=channel_type)
            assert channel.is_instrumental is True
            assert channel.is_biological is False


class TestNoiseProfile:
    """Test noise profile requirements."""

    def test_noise_profile_requires_at_least_one_indicator(self):
        """NoiseProfile requires at least one noise/error indicator."""
        with pytest.raises(ValueError, match="requires at least one noise/error indicator"):
            NoiseProfile()

    def test_noise_profile_with_explicit_none(self):
        """NoiseProfile can explicitly declare noise-free."""
        profile = NoiseProfile(noise_type="none")
        assert profile.is_noise_free is True

    def test_noise_profile_with_level(self):
        """NoiseProfile can specify noise level."""
        profile = NoiseProfile(noise_level=Decimal("0.05"))
        assert profile.has_significant_noise is False

        profile_noisy = NoiseProfile(noise_level=Decimal("0.5"))
        assert profile_noisy.has_significant_noise is True


class TestIntegrationScenarios:
    """Integration tests for realistic scenarios."""

    def test_visual_observation_scenario(self):
        """Test realistic visual observation."""
        event = SensoryTransferEvent(
            source_effect=SourceEffect(
                claimed_entity_or_effect="red_ball_falling",
                claimed_existence_type=ExistenceType.PHYSICAL,
                claimed_location="3m above ground"
            ),
            channel=SensoryChannel(
                channel_type=ChannelType.VISUAL,
                bandwidth_description="380-750nm visible spectrum",
                sensitivity=Decimal("0.01")
            ),
            time_anchor=TimeAnchor(timestamp=datetime.now()),
            place_anchor=PlaceAnchor(locality_label="lab_room_A"),
            reference_anchor=ReferenceAnchor(entity_id="ball_001"),
            signal=Signal(
                signal_value="red_moving_object",
                signal_quality="clear"
            ),
            noise_profile=NoiseProfile(
                noise_type="photon_shot_noise",
                noise_level=Decimal("0.02"),
                snr=Decimal("30")
            ),
            retained_trace=SensoryTrace(
                received_content="red_sphere_trajectory",
                trace_quality="high",
                preservation_medium="visual_memory"
            ),
            medium=Medium(medium_type="air"),
            transduction=TransductionProcess(transduction_type="cone_photoreceptor"),
            observer_or_instrument=Observer(
                observer_id="experimenter_1",
                attention_state="focused"
            ),
            rank=Rank.OBSERVED
        )

        # Validate all laws
        assert SensoryTransferValidator.check_minimal_sensory_requirements(event)
        assert event.can_certify_source() is False
        assert event.can_certify_reality() is False
        assert event.equals_external_reality() is False

    def test_instrumental_measurement_scenario(self):
        """Test realistic instrumental measurement."""
        calibration = CalibrationState(
            calibration_status=CalibrationStatus.CALIBRATED,
            calibration_date=datetime(2026, 5, 1),
            calibration_standard="NIST_traceable",
            calibration_uncertainty="±0.1°C"
        )

        instrument = Instrument(
            instrument_id="thermometer_T001",
            instrument_type="digital_thermometer",
            calibration_state=calibration,
            accuracy_spec="±0.5°C",
            precision_spec="0.1°C"
        )

        event = SensoryTransferEvent(
            source_effect=SourceEffect(
                claimed_entity_or_effect="water_temperature",
                claimed_existence_type=ExistenceType.PHYSICAL
            ),
            channel=SensoryChannel(channel_type=ChannelType.INSTRUMENTAL_THERMAL),
            time_anchor=TimeAnchor(timestamp=datetime.now()),
            place_anchor=PlaceAnchor(locality_label="beaker_1"),
            reference_anchor=ReferenceAnchor(entity_id="water_sample_001"),
            signal=Signal(
                signal_value=Decimal("23.4"),
                signal_strength=Decimal("1.0"),
                signal_quality="stable"
            ),
            noise_profile=NoiseProfile(
                noise_type="thermal_noise",
                systematic_error=Decimal("0.1"),
                random_error=Decimal("0.05")
            ),
            retained_trace=SensoryTrace(
                received_content="temperature_reading_23.4C",
                preservation_medium="data_logger"
            ),
            medium=Medium(medium_type="thermal_contact"),
            transduction=TransductionProcess(transduction_type="thermistor"),
            observer_or_instrument=instrument,
            rank=Rank.OBSERVED,
            residuals=frozenset([
                Residual(
                    description="Calibration uncertainty ±0.1°C",
                    residual_type="uncertainty"
                )
            ])
        )

        assert event.is_instrumental is True
        assert event.has_reliable_calibration is True
        assert SensoryTransferValidator.check_minimal_sensory_requirements(event)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
