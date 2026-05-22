"""
Comprehensive test suite for ProtoPrior Kernel - FirstPriorUnit

Tests all constitutional laws:
1. No FirstPriorUnit without existence
2. No FirstPriorUnit without distinction
3. No FirstPriorUnit without boundary
4. No FirstPriorUnit without time anchor
5. No FirstPriorUnit without place anchor
6. No FirstPriorUnit without reference anchor
7. No FirstPriorUnit without retention
8. No FirstPriorUnit without comparability
9. No FirstPriorUnit without primitive bindability
10. FirstPriorUnit cannot produce rule
11. FirstPriorUnit cannot produce meaning
12. FirstPriorUnit cannot issue judgment
13. FirstPriorUnit cannot certify
14. Hypothetical existence cannot be CERTIFIED
15. Textual/symbolic/acoustic do not imply physical existence
16. FirstPriorUnit serializes without losing fields
17. FirstPriorUnit preserves residuals
18. FirstPriorUnit has stable trace_id
"""

import pytest
from datetime import datetime
from decimal import Decimal
from uuid import UUID

from gfa.proto_prior import (
    ExistenceType,
    Domain,
    Channel,
    TimeAnchor,
    PlaceAnchor,
    ReferenceAnchor,
    Distinction,
    Boundary,
    RetentionState,
    ComparabilityState,
    PrimitiveBindability,
    FirstPriorUnit,
    Residual,
    Rank,
    ProtoPriorValidator,
)
from gfa.proto_prior.retention import RetentionLevel
from gfa.proto_prior.comparability import ComparabilityType
from gfa.proto_prior.primitive_bindability import BindabilityLevel
from gfa.proto_prior.proto_prior_validator import ValidationError


# Helper function to create a valid FirstPriorUnit
def make_valid_first_prior_unit(**overrides):
    """Create a valid FirstPriorUnit with optional overrides."""
    defaults = {
        "entity_or_effect": "test_entity",
        "existence_type": ExistenceType.PHYSICAL,
        "domain": Domain(name="test_domain"),
        "distinction": Distinction(
            distinguishing_features={"feature1", "feature2"}
        ),
        "boundary": Boundary(spatial_boundary="bounded region"),
        "time_anchor": TimeAnchor(timestamp=datetime.now()),
        "place_anchor": PlaceAnchor(locality_label="test_location"),
        "reference_anchor": ReferenceAnchor(entity_id="entity_123"),
        "channel": Channel(name="test_channel"),
        "retention_state": RetentionState(retention_level=RetentionLevel.STABLE),
        "comparability_state": ComparabilityState(
            supported_comparisons={ComparabilityType.SIMILAR}
        ),
        "primitive_bindability": PrimitiveBindability(
            bindability_level=BindabilityLevel.GENERAL
        ),
    }
    defaults.update(overrides)
    return FirstPriorUnit(**defaults)


class TestFirstPriorUnitMandatoryFields:
    """Test that all mandatory fields are enforced."""

    def test_no_first_prior_without_existence(self):
        """FirstPriorUnit requires entity_or_effect."""
        with pytest.raises(ValueError, match="entity_or_effect is mandatory"):
            make_valid_first_prior_unit(entity_or_effect=None)

    def test_no_first_prior_without_distinction(self):
        """FirstPriorUnit requires distinction."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_first_prior_unit(distinction=None)

    def test_no_first_prior_without_boundary(self):
        """FirstPriorUnit requires boundary."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_first_prior_unit(boundary=None)

    def test_no_first_prior_without_time_anchor(self):
        """FirstPriorUnit requires time_anchor."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_first_prior_unit(time_anchor=None)

    def test_no_first_prior_without_place_anchor(self):
        """FirstPriorUnit requires place_anchor."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_first_prior_unit(place_anchor=None)

    def test_no_first_prior_without_reference_anchor(self):
        """FirstPriorUnit requires reference_anchor."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_first_prior_unit(reference_anchor=None)

    def test_no_first_prior_without_retention(self):
        """FirstPriorUnit requires retention_state."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_first_prior_unit(retention_state=None)

    def test_no_first_prior_without_comparability(self):
        """FirstPriorUnit requires comparability_state."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_first_prior_unit(comparability_state=None)

    def test_no_first_prior_without_primitive_bindability(self):
        """FirstPriorUnit requires primitive_bindability."""
        with pytest.raises((ValueError, TypeError)):
            make_valid_first_prior_unit(primitive_bindability=None)


class TestFirstPriorUnitProhibitions:
    """Test that FirstPriorUnit CANNOT produce rules/meanings/judgments/certificates."""

    def test_first_prior_unit_cannot_produce_rule(self):
        """FirstPriorUnit.can_produce_rule() must return False."""
        unit = make_valid_first_prior_unit()
        assert unit.can_produce_rule() is False

    def test_first_prior_unit_cannot_produce_meaning(self):
        """FirstPriorUnit.can_produce_meaning() must return False."""
        unit = make_valid_first_prior_unit()
        assert unit.can_produce_meaning() is False

    def test_first_prior_unit_cannot_issue_judgment(self):
        """FirstPriorUnit.can_issue_judgment() must return False."""
        unit = make_valid_first_prior_unit()
        assert unit.can_issue_judgment() is False

    def test_first_prior_unit_cannot_certify(self):
        """FirstPriorUnit.can_certify() must return False."""
        unit = make_valid_first_prior_unit()
        assert unit.can_certify() is False


class TestExistenceTypeConstraints:
    """Test existence type constraints."""

    def test_hypothetical_existence_cannot_be_certified(self):
        """Hypothetical existence cannot have CERTIFIED rank."""
        with pytest.raises(ValueError, match="Hypothetical existence cannot have CERTIFIED rank"):
            make_valid_first_prior_unit(
                existence_type=ExistenceType.HYPOTHETICAL,
                rank=Rank.CERTIFIED
            )

    def test_hypothetical_existence_can_be_candidate(self):
        """Hypothetical existence can have CANDIDATE rank."""
        unit = make_valid_first_prior_unit(
            existence_type=ExistenceType.HYPOTHETICAL,
            rank=Rank.CANDIDATE
        )
        assert unit.rank == Rank.CANDIDATE

    def test_hypothetical_existence_can_be_observed(self):
        """Hypothetical existence can have OBSERVED rank."""
        unit = make_valid_first_prior_unit(
            existence_type=ExistenceType.HYPOTHETICAL,
            rank=Rank.OBSERVED
        )
        assert unit.rank == Rank.OBSERVED

    def test_textual_symbolic_acoustic_do_not_imply_physical_existence(self):
        """Linguistic existence claiming physical content cannot be CERTIFIED."""
        with pytest.raises(ValueError, match="cannot certify physical existence"):
            make_valid_first_prior_unit(
                entity_or_effect="exists physically in space",
                existence_type=ExistenceType.LINGUISTIC,
                rank=Rank.CERTIFIED
            )

    def test_linguistic_existence_can_be_certified_for_linguistic_content(self):
        """Linguistic existence can be CERTIFIED for linguistic claims."""
        unit = make_valid_first_prior_unit(
            entity_or_effect="word 'tree' in Arabic",
            existence_type=ExistenceType.LINGUISTIC,
            rank=Rank.CERTIFIED
        )
        assert unit.rank == Rank.CERTIFIED


class TestResidualPreservation:
    """Test that residuals are preserved."""

    def test_first_prior_unit_preserves_residuals(self):
        """Residuals must be preserved in FirstPriorUnit."""
        residual1 = Residual(
            description="Uncertain temporal precision",
            residual_type="uncertainty"
        )
        residual2 = Residual(
            description="Incomplete spatial data",
            residual_type="incompleteness"
        )

        unit = make_valid_first_prior_unit(
            residuals={residual1, residual2}
        )

        assert unit.has_residuals
        assert unit.residual_count == 2
        assert residual1 in unit.residuals
        assert residual2 in unit.residuals

    def test_first_prior_unit_without_residuals(self):
        """FirstPriorUnit can have empty residuals set."""
        unit = make_valid_first_prior_unit(residuals=frozenset())
        assert not unit.has_residuals
        assert unit.residual_count == 0


class TestTraceIdentity:
    """Test trace identity and serialization."""

    def test_first_prior_unit_has_stable_trace_id(self):
        """Each FirstPriorUnit has a unique, stable trace_id."""
        unit1 = make_valid_first_prior_unit()
        unit2 = make_valid_first_prior_unit()

        # Each unit has a trace_id
        assert isinstance(unit1.trace_id, UUID)
        assert isinstance(unit2.trace_id, UUID)

        # Different units have different trace_ids
        assert unit1.trace_id != unit2.trace_id

    def test_first_prior_unit_serializes_without_losing_minimal_sufficient_fields(self):
        """All 14 mandatory fields are present and accessible."""
        unit = make_valid_first_prior_unit()

        # Check all 14 mandatory fields are accessible
        assert unit.entity_or_effect is not None
        assert isinstance(unit.existence_type, ExistenceType)
        assert isinstance(unit.domain, Domain)
        assert isinstance(unit.distinction, Distinction)
        assert isinstance(unit.boundary, Boundary)
        assert isinstance(unit.time_anchor, TimeAnchor)
        assert isinstance(unit.place_anchor, PlaceAnchor)
        assert isinstance(unit.reference_anchor, ReferenceAnchor)
        assert isinstance(unit.channel, Channel)
        assert isinstance(unit.trace_id, UUID)
        assert isinstance(unit.retention_state, RetentionState)
        assert isinstance(unit.comparability_state, ComparabilityState)
        assert isinstance(unit.primitive_bindability, PrimitiveBindability)
        assert isinstance(unit.residuals, frozenset)
        assert isinstance(unit.rank, Rank)


class TestProtoPriorValidator:
    """Test ProtoPriorValidator enforcement."""

    def test_validator_accepts_valid_unit(self):
        """Validator accepts valid FirstPriorUnit."""
        unit = make_valid_first_prior_unit()
        # Should not raise
        ProtoPriorValidator.validate_first_prior_unit(unit)

    def test_validator_rejects_hypothetical_certified(self):
        """Validator rejects hypothetical existence with CERTIFIED rank."""
        with pytest.raises(ValueError, match="Hypothetical existence cannot have CERTIFIED rank"):
            unit = make_valid_first_prior_unit(
                existence_type=ExistenceType.HYPOTHETICAL,
                rank=Rank.CERTIFIED
            )

    def test_validator_checks_minimal_sufficiency(self):
        """Validator can check minimal sufficiency criteria."""
        unit = make_valid_first_prior_unit()
        assert ProtoPriorValidator.check_minimal_sufficiency(unit) is True

    def test_existence_type_promotion_without_bridge(self):
        """Validator enforces existence type promotion rules."""
        # Physical can imply relational
        ProtoPriorValidator.validate_existence_type_promotion(
            ExistenceType.PHYSICAL,
            ExistenceType.RELATIONAL,
            has_bridge=False
        )

        # Linguistic cannot imply physical without bridge
        with pytest.raises(ValidationError, match="cannot imply.*without explicit ExistenceBridge"):
            ProtoPriorValidator.validate_existence_type_promotion(
                ExistenceType.LINGUISTIC,
                ExistenceType.PHYSICAL,
                has_bridge=False
            )

    def test_existence_type_promotion_with_bridge(self):
        """Existence type promotion allowed with explicit bridge."""
        # With bridge, any promotion is allowed
        ProtoPriorValidator.validate_existence_type_promotion(
            ExistenceType.LINGUISTIC,
            ExistenceType.PHYSICAL,
            has_bridge=True
        )

    def test_rank_promotion_requires_evidence(self):
        """Rank promotion to LICENSED/CERTIFIED requires evidence."""
        with pytest.raises(ValidationError, match="requires positive evidence"):
            ProtoPriorValidator.validate_rank_promotion(
                Rank.CANDIDATE,
                Rank.LICENSED,
                has_evidence=False
            )

    def test_rank_promotion_to_certified_requires_audit(self):
        """Rank promotion to CERTIFIED requires audit."""
        with pytest.raises(ValidationError, match="requires full audit"):
            ProtoPriorValidator.validate_rank_promotion(
                Rank.LICENSED,
                Rank.CERTIFIED,
                has_evidence=True,
                has_audit=False
            )

    def test_rank_promotion_with_evidence_and_audit(self):
        """Rank promotion allowed with evidence and audit."""
        ProtoPriorValidator.validate_rank_promotion(
            Rank.LICENSED,
            Rank.CERTIFIED,
            has_evidence=True,
            has_audit=True
        )


class TestComponentTypes:
    """Test individual component types."""

    def test_time_anchor_requires_at_least_one_indicator(self):
        """TimeAnchor requires at least one temporal indicator."""
        with pytest.raises(ValueError, match="requires at least one temporal indicator"):
            TimeAnchor()

    def test_time_anchor_with_timestamp(self):
        """TimeAnchor can be created with timestamp."""
        anchor = TimeAnchor(timestamp=datetime.now())
        assert anchor.is_valid

    def test_time_anchor_with_sequence_order(self):
        """TimeAnchor can be created with sequence order."""
        anchor = TimeAnchor(sequence_order=42)
        assert anchor.is_valid

    def test_place_anchor_requires_at_least_one_indicator(self):
        """PlaceAnchor requires at least one spatial/domain indicator."""
        with pytest.raises(ValueError, match="requires at least one spatial/domain indicator"):
            PlaceAnchor()

    def test_place_anchor_with_coordinates(self):
        """PlaceAnchor can be created with spatial coordinates."""
        anchor = PlaceAnchor(spatial_coordinates=(Decimal("1.0"), Decimal("2.0"), Decimal("3.0")))
        assert anchor.is_valid
        assert anchor.dimensionality == 3

    def test_reference_anchor_requires_at_least_one_indicator(self):
        """ReferenceAnchor requires at least one reference indicator."""
        with pytest.raises(ValueError, match="requires at least one reference indicator"):
            ReferenceAnchor()

    def test_reference_anchor_with_entity_id(self):
        """ReferenceAnchor can be created with entity_id."""
        anchor = ReferenceAnchor(entity_id="entity_123")
        assert anchor.is_valid
        assert anchor.primary_reference == "entity_123"

    def test_distinction_requires_features(self):
        """Distinction requires at least one distinguishing feature."""
        with pytest.raises(ValueError, match="requires at least one distinguishing feature"):
            Distinction(distinguishing_features=set())

    def test_boundary_requires_at_least_one_type(self):
        """Boundary requires at least one boundary specification."""
        with pytest.raises(ValueError, match="requires at least one boundary specification"):
            Boundary()

    def test_retention_state_forbids_none_level(self):
        """RetentionState forbids NONE level for FirstPriorUnit."""
        with pytest.raises(ValueError, match="requires retention capability"):
            RetentionState(retention_level=RetentionLevel.NONE)

    def test_comparability_state_requires_at_least_one_type(self):
        """ComparabilityState requires at least one comparison type."""
        with pytest.raises(ValueError, match="requires at least one supported comparison type"):
            ComparabilityState(supported_comparisons=set())

    def test_primitive_bindability_forbids_none_level(self):
        """PrimitiveBindability forbids NONE level for FirstPriorUnit."""
        with pytest.raises(ValueError, match="requires primitive bindability"):
            PrimitiveBindability(bindability_level=BindabilityLevel.NONE)


class TestIntegrationScenarios:
    """Integration tests for realistic scenarios."""

    def test_physical_observation_scenario(self):
        """Test realistic physical observation scenario."""
        unit = FirstPriorUnit(
            entity_or_effect="ball falling",
            existence_type=ExistenceType.PHYSICAL,
            domain=Domain(name="3D space"),
            distinction=Distinction(
                distinguishing_features={"red color", "spherical shape", "motion"},
                background_context="static environment"
            ),
            boundary=Boundary(
                spatial_boundary="0.1m radius sphere",
                temporal_boundary="t0 to t0+2s"
            ),
            time_anchor=TimeAnchor(
                timestamp=datetime.now(),
                duration=Decimal("2.0")
            ),
            place_anchor=PlaceAnchor(
                spatial_coordinates=(Decimal("0"), Decimal("0"), Decimal("10"))
            ),
            reference_anchor=ReferenceAnchor(
                entity_id="ball_001",
                reference_type="physical_object"
            ),
            channel=Channel(name="visual_observation"),
            retention_state=RetentionState(
                retention_level=RetentionLevel.PERSISTENT,
                retention_medium="video_recording"
            ),
            comparability_state=ComparabilityState(
                supported_comparisons={
                    ComparabilityType.METRIC,
                    ComparabilityType.ORDERED,
                    ComparabilityType.SIMILAR
                }
            ),
            primitive_bindability=PrimitiveBindability(
                bindability_level=BindabilityLevel.GENERAL
            ),
            rank=Rank.OBSERVED
        )

        assert unit.is_valid
        assert ProtoPriorValidator.check_minimal_sufficiency(unit)

    def test_linguistic_trace_scenario(self):
        """Test realistic linguistic trace scenario."""
        unit = FirstPriorUnit(
            entity_or_effect="word 'كتاب' (book)",
            existence_type=ExistenceType.LINGUISTIC,
            domain=Domain(name="Arabic lexicon"),
            distinction=Distinction(
                distinguishing_features={"consonants ك-ت-ب", "vocalization pattern"}
            ),
            boundary=Boundary(
                conceptual_boundary="single lexical item",
                temporal_boundary="observed in text at timestamp t0"
            ),
            time_anchor=TimeAnchor(
                timestamp=datetime.now(),
                temporal_label="first_attestation"
            ),
            place_anchor=PlaceAnchor(
                domain_position="Classical Arabic lexicon",
                field_identifier="morphology_layer"
            ),
            reference_anchor=ReferenceAnchor(
                entity_id="كتاب",
                reference_type="lexical_form"
            ),
            channel=Channel(name="textual_observation"),
            retention_state=RetentionState(
                retention_level=RetentionLevel.PERMANENT,
                retention_medium="written_record"
            ),
            comparability_state=ComparabilityState(
                supported_comparisons={
                    ComparabilityType.IDENTICAL,
                    ComparabilityType.CATEGORICAL
                }
            ),
            primitive_bindability=PrimitiveBindability(
                bindability_level=BindabilityLevel.CONDITIONAL
            ),
            residuals=frozenset([
                Residual(
                    description="Semantic content not yet bound",
                    residual_type="incompleteness"
                )
            ]),
            rank=Rank.OBSERVED
        )

        assert unit.is_valid
        assert unit.has_residuals
        assert ProtoPriorValidator.check_minimal_sufficiency(unit)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
