"""
Test suite for RealityGeometry Kernel - Layer -2 (Absolute Ground)

This test suite validates all critical laws for the RealityGeometry Kernel:
- Reality is NOT produced by system
- Reality cannot be CERTIFIED by system
- Reality precedes all traces
- Observer is part of reality (embodied)
- Hypothetical → Physical requires experimental bridge
- Reality grounds resistance to hallucination
- All mandatory fields enforced
- RealityEffect ≠ Reality

Test coverage:
1. MinimalRealityUnit creation and validation
2. Reality domains (Self, Life, World, Relational)
3. Reality status (Physical, Biological, Social, etc.)
4. RealityEffect and prohibition laws
5. EmbodiedObserver requirements
6. LifeContext and WorldContext
7. RealityBridge validation
8. Constitutional law enforcement
9. Integration scenarios
10. Residual preservation
"""

import pytest
from uuid import UUID

from gfa.reality import (
    MinimalRealityUnit,
    RealityDomain,
    DomainType,
    RealityStatus,
    RealityEffect,
    EffectType,
    EmbodiedObserver,
    BodyState,
    NeedState,
    LifeContext,
    LifePhase,
    WorldContext,
    WorldType,
    RealityBridge,
    BridgeType,
    BridgeValidation,
    RealityValidator,
)
from gfa.reality.minimal_reality_unit import RealityResidual


# ============================================================================
# Test 1: MinimalRealityUnit - Mandatory Fields
# ============================================================================

def test_minimal_reality_unit_mandatory_fields():
    """Test that all 15 mandatory fields are enforced."""
    # Create valid MinimalRealityUnit
    domain = RealityDomain(domain_type=DomainType.SELF)

    observer = EmbodiedObserver(
        observer_id="observer_1",
        body_state=BodyState.FUNCTIONAL,
        need_state=NeedState.SATISFIED,
        available_sensory_channels=frozenset({"visual", "auditory", "tactile"}),
        available_actions=frozenset({"move", "grasp", "speak"}),
        biological_needs=frozenset({"oxygen", "water", "food", "warmth"}),
    )

    life_ctx = LifeContext(
        life_phase=LifePhase.MATURITY,
        organism_type="homo_sapiens",
        biological_requirements=frozenset({"oxygen", "water", "nutrients"}),
        life_constraints=frozenset({"temperature_range", "pressure_range"}),
    )

    world_ctx = WorldContext(
        world_type=WorldType.NATURAL,
        spatial_structure="Earth surface, urban environment",
        physical_constraints=frozenset({"gravity", "atmosphere"}),
        physical_laws=frozenset({"conservation_of_energy", "thermodynamics"}),
    )

    effect = RealityEffect(
        effect_type=EffectType.SENSORY,
        source_description="Light reflection from surface",
        manifestation="Visual pattern",
        source_status=RealityStatus.PHYSICAL,
    )

    unit = MinimalRealityUnit(
        reality_domain=domain,
        reality_status=RealityStatus.PHYSICAL,
        entity_or_process="Physical object in environment",
        embodied_observer=observer,
        life_context=life_ctx,
        world_context=world_ctx,
        time_marker="2024-01-15T10:30:00Z",
        place_marker="Lab room, coordinates (x, y, z)",
        reality_effects=frozenset({effect}),
        physical_constraints=frozenset({"mass", "volume", "temperature"}),
        biological_constraints=frozenset({"non_toxic", "safe_temperature"}),
        existence_conditions=frozenset({"stable_substrate", "ambient_conditions"}),
        known_boundaries=frozenset({"spatial_extent", "temporal_duration"}),
    )

    assert unit.is_valid
    assert isinstance(unit.reality_trace_id, UUID)
    assert unit.reality_domain.domain_type == DomainType.SELF
    assert unit.reality_status == RealityStatus.PHYSICAL


def test_minimal_reality_unit_missing_fields():
    """Test that missing mandatory fields raise errors."""
    # Missing entity_or_process
    with pytest.raises(TypeError):
        MinimalRealityUnit()

    # Missing reality_domain
    with pytest.raises(TypeError):
        MinimalRealityUnit(
            entity_or_process="test",
        )


# ============================================================================
# Test 2: Reality Prohibition Laws
# ============================================================================

def test_reality_cannot_be_produced_by_system():
    """Test that reality is NOT produced by system."""
    domain = RealityDomain(domain_type=DomainType.WORLD)
    observer = EmbodiedObserver(
        observer_id="obs_1",
        body_state=BodyState.FUNCTIONAL,
        need_state=NeedState.SATISFIED,
        available_sensory_channels=frozenset({"visual"}),
        available_actions=frozenset({"observe"}),
        biological_needs=frozenset({"oxygen"}),
    )
    life_ctx = LifeContext(
        life_phase=LifePhase.MATURITY,
        organism_type="human",
        biological_requirements=frozenset({"oxygen"}),
        life_constraints=frozenset({"temperature"}),
    )
    world_ctx = WorldContext(
        world_type=WorldType.NATURAL,
        spatial_structure="outdoor",
        physical_constraints=frozenset({"gravity"}),
        physical_laws=frozenset({"physics"}),
    )
    effect = RealityEffect(
        effect_type=EffectType.SENSORY,
        source_description="tree",
        manifestation="green",
        source_status=RealityStatus.PHYSICAL,
    )

    unit = MinimalRealityUnit(
        reality_domain=domain,
        reality_status=RealityStatus.PHYSICAL,
        entity_or_process="tree",
        embodied_observer=observer,
        life_context=life_ctx,
        world_context=world_ctx,
        time_marker="2024-01-15",
        place_marker="forest",
        reality_effects=frozenset({effect}),
        physical_constraints=frozenset({"mass"}),
        biological_constraints=frozenset({"living"}),
        existence_conditions=frozenset({"soil"}),
        known_boundaries=frozenset({"height"}),
    )

    # CRITICAL LAW: Reality is NOT produced by system
    assert not unit.is_produced_by_system()


def test_reality_cannot_be_certified_by_system():
    """Test that reality cannot be CERTIFIED by system."""
    domain = RealityDomain(domain_type=DomainType.SELF)
    observer = EmbodiedObserver(
        observer_id="obs_1",
        body_state=BodyState.FUNCTIONAL,
        need_state=NeedState.SATISFIED,
        available_sensory_channels=frozenset({"proprioceptive"}),
        available_actions=frozenset({"move"}),
        biological_needs=frozenset({"oxygen"}),
    )
    life_ctx = LifeContext(
        life_phase=LifePhase.MATURITY,
        organism_type="human",
        biological_requirements=frozenset({"oxygen"}),
        life_constraints=frozenset({"temperature"}),
    )
    world_ctx = WorldContext(
        world_type=WorldType.NATURAL,
        spatial_structure="body",
        physical_constraints=frozenset({"gravity"}),
        physical_laws=frozenset({"physics"}),
    )
    effect = RealityEffect(
        effect_type=EffectType.SENSORY,
        source_description="body sensation",
        manifestation="pain",
        source_status=RealityStatus.BIOLOGICAL,
    )

    unit = MinimalRealityUnit(
        reality_domain=domain,
        reality_status=RealityStatus.BIOLOGICAL,
        entity_or_process="my body",
        embodied_observer=observer,
        life_context=life_ctx,
        world_context=world_ctx,
        time_marker="now",
        place_marker="here",
        reality_effects=frozenset({effect}),
        physical_constraints=frozenset({"mass"}),
        biological_constraints=frozenset({"alive"}),
        existence_conditions=frozenset({"metabolic_activity"}),
        known_boundaries=frozenset({"skin"}),
    )

    # CRITICAL LAW: Reality cannot be certified by system
    assert not unit.can_be_certified_by_system()


def test_reality_precedes_all_traces():
    """Test that reality precedes all traces."""
    domain = RealityDomain(domain_type=DomainType.WORLD)
    observer = EmbodiedObserver(
        observer_id="obs_1",
        body_state=BodyState.FUNCTIONAL,
        need_state=NeedState.SATISFIED,
        available_sensory_channels=frozenset({"visual"}),
        available_actions=frozenset({"observe"}),
        biological_needs=frozenset({"oxygen"}),
    )
    life_ctx = LifeContext(
        life_phase=LifePhase.MATURITY,
        organism_type="human",
        biological_requirements=frozenset({"oxygen"}),
        life_constraints=frozenset({"temperature"}),
    )
    world_ctx = WorldContext(
        world_type=WorldType.NATURAL,
        spatial_structure="outdoor",
        physical_constraints=frozenset({"gravity"}),
        physical_laws=frozenset({"physics"}),
    )
    effect = RealityEffect(
        effect_type=EffectType.SENSORY,
        source_description="rock",
        manifestation="solid",
        source_status=RealityStatus.PHYSICAL,
    )

    unit = MinimalRealityUnit(
        reality_domain=domain,
        reality_status=RealityStatus.PHYSICAL,
        entity_or_process="rock",
        embodied_observer=observer,
        life_context=life_ctx,
        world_context=world_ctx,
        time_marker="2024-01-15",
        place_marker="ground",
        reality_effects=frozenset({effect}),
        physical_constraints=frozenset({"mass"}),
        biological_constraints=frozenset({"inert"}),
        existence_conditions=frozenset({"stable"}),
        known_boundaries=frozenset({"surface"}),
    )

    # CRITICAL LAW: Reality precedes all traces
    assert unit.precedes_all_traces()


def test_reality_grounds_resistance_to_hallucination():
    """Test that reality grounds resistance to hallucination."""
    domain = RealityDomain(domain_type=DomainType.SELF)
    observer = EmbodiedObserver(
        observer_id="obs_1",
        body_state=BodyState.FUNCTIONAL,
        need_state=NeedState.URGENT,
        available_sensory_channels=frozenset({"interoceptive"}),
        available_actions=frozenset({"seek_food"}),
        biological_needs=frozenset({"food", "water"}),
    )
    life_ctx = LifeContext(
        life_phase=LifePhase.MATURITY,
        organism_type="human",
        biological_requirements=frozenset({"food", "water"}),
        life_constraints=frozenset({"metabolic_rate"}),
    )
    world_ctx = WorldContext(
        world_type=WorldType.NATURAL,
        spatial_structure="environment",
        physical_constraints=frozenset({"resources"}),
        physical_laws=frozenset({"thermodynamics"}),
    )
    effect = RealityEffect(
        effect_type=EffectType.SENSORY,
        source_description="hunger signal",
        manifestation="discomfort",
        source_status=RealityStatus.BIOLOGICAL,
    )

    unit = MinimalRealityUnit(
        reality_domain=domain,
        reality_status=RealityStatus.BIOLOGICAL,
        entity_or_process="hunger",
        embodied_observer=observer,
        life_context=life_ctx,
        world_context=world_ctx,
        time_marker="now",
        place_marker="body",
        reality_effects=frozenset({effect}),
        physical_constraints=frozenset({"energy_depletion"}),
        biological_constraints=frozenset({"metabolic_need"}),
        existence_conditions=frozenset({"living_organism"}),
        known_boundaries=frozenset({"tolerance_limit"}),
    )

    # CRITICAL LAW: Reality grounds resistance to hallucination
    assert unit.grounds_resistance_to_hallucination()


# ============================================================================
# Test 3: Observer Embodiment
# ============================================================================

def test_observer_is_part_of_reality():
    """Test that observer is part of reality, not external."""
    observer = EmbodiedObserver(
        observer_id="human_observer",
        body_state=BodyState.FUNCTIONAL,
        need_state=NeedState.SATISFIED,
        available_sensory_channels=frozenset({"visual", "auditory", "tactile"}),
        available_actions=frozenset({"move", "manipulate"}),
        biological_needs=frozenset({"oxygen", "water", "food"}),
    )

    # CRITICAL LAW: Observer is NOT external to reality
    assert not observer.is_external_to_reality()

    # CRITICAL LAW: Observer cannot escape embodiment
    assert not observer.can_escape_embodiment()


def test_observer_requirements():
    """Test that observer has mandatory requirements."""
    # Observer must have sensory channels
    with pytest.raises(ValueError, match="available_sensory_channels cannot be empty"):
        EmbodiedObserver(
            observer_id="obs_1",
            body_state=BodyState.FUNCTIONAL,
            need_state=NeedState.SATISFIED,
            available_sensory_channels=frozenset(),  # Empty!
            available_actions=frozenset({"move"}),
            biological_needs=frozenset({"oxygen"}),
        )

    # Observer must have actions
    with pytest.raises(ValueError, match="available_actions cannot be empty"):
        EmbodiedObserver(
            observer_id="obs_1",
            body_state=BodyState.FUNCTIONAL,
            need_state=NeedState.SATISFIED,
            available_sensory_channels=frozenset({"visual"}),
            available_actions=frozenset(),  # Empty!
            biological_needs=frozenset({"oxygen"}),
        )

    # Observer must have biological needs
    with pytest.raises(ValueError, match="biological_needs cannot be empty"):
        EmbodiedObserver(
            observer_id="obs_1",
            body_state=BodyState.FUNCTIONAL,
            need_state=NeedState.SATISFIED,
            available_sensory_channels=frozenset({"visual"}),
            available_actions=frozenset({"move"}),
            biological_needs=frozenset(),  # Empty!
        )


# ============================================================================
# Test 4: RealityEffect Prohibition Laws
# ============================================================================

def test_reality_effect_not_equal_reality():
    """Test that RealityEffect ≠ Reality."""
    effect = RealityEffect(
        effect_type=EffectType.SENSORY,
        source_description="Physical object",
        manifestation="Visual appearance",
        source_status=RealityStatus.PHYSICAL,
    )

    # CRITICAL LAW: RealityEffect ≠ Reality
    assert not effect.equals_reality()


def test_reality_effect_cannot_certify_source():
    """Test that RealityEffect cannot certify its source."""
    effect = RealityEffect(
        effect_type=EffectType.CAUSAL,
        source_description="Impact force",
        manifestation="Deformation",
        source_status=RealityStatus.PHYSICAL,
    )

    # CRITICAL LAW: Effects cannot certify sources
    assert not effect.can_certify_source()


def test_hypothetical_effect_requires_validation():
    """Test that hypothetical sources require validation."""
    effect = RealityEffect(
        effect_type=EffectType.EMERGENT,
        source_description="Theoretical entity",
        manifestation="Predicted pattern",
        source_status=RealityStatus.HYPOTHETICAL,
    )

    # CRITICAL LAW: Hypothetical sources require validation
    assert effect.requires_validation


# ============================================================================
# Test 5: Reality Bridge Validation
# ============================================================================

def test_hypothetical_to_physical_requires_experimental_bridge():
    """Test that hypothetical → physical requires EXPERIMENTAL bridge."""
    # Valid experimental bridge
    bridge = RealityBridge(
        source_status=RealityStatus.HYPOTHETICAL,
        target_status=RealityStatus.PHYSICAL,
        bridge_type=BridgeType.EXPERIMENTAL,
        required_conditions=frozenset({"controlled_experiment", "measurement"}),
    )

    assert bridge.is_experimental_bridge
    assert bridge.validate_crossing() == BridgeValidation.REQUIRES_CONDITIONS

    # Invalid bridge types should be detected by validator
    # (Note: RealityBridge doesn't enforce all combinations in __init__,
    # validation is done via validate_crossing)
    invalid_bridge = RealityBridge(
        source_status=RealityStatus.HYPOTHETICAL,
        target_status=RealityStatus.PHYSICAL,
        bridge_type=BridgeType.ABSTRACTION,  # Wrong bridge type
    )
    # Validator should detect this as requiring experimental bridge
    violations = RealityValidator.validate_reality_bridge(invalid_bridge)
    assert len(violations) > 0


def test_physical_to_biological_requires_embodiment_bridge():
    """Test that physical → biological requires EMBODIMENT bridge."""
    # Valid EMBODIMENT bridge
    bridge = RealityBridge(
        source_status=RealityStatus.PHYSICAL,
        target_status=RealityStatus.BIOLOGICAL,
        bridge_type=BridgeType.EMBODIMENT,
        required_conditions=frozenset({"living_substrate", "metabolic_activity"}),
    )

    assert bridge.validate_crossing() in {
        BridgeValidation.VALID,
        BridgeValidation.REQUIRES_CONDITIONS
    }

    # Test that wrong transitions for EMBODIMENT are detected
    # EMBODIMENT only allows Physical ↔ Biological
    with pytest.raises(ValueError, match="EMBODIMENT bridge requires"):
        RealityBridge(
            source_status=RealityStatus.SOCIAL,  # Not physical or biological
            target_status=RealityStatus.CONCEPTUAL,
            bridge_type=BridgeType.EMBODIMENT,  # Wrong transition for EMBODIMENT
        )


# ============================================================================
# Test 6: Reality Domains
# ============================================================================

def test_self_reality_is_primary():
    """Test that SelfReality is the primary domain."""
    self_domain = RealityDomain(domain_type=DomainType.SELF)

    assert self_domain.is_self_reality
    assert self_domain.is_primary_domain
    assert self_domain.requires_embodiment


def test_domain_transitions():
    """Test domain transition validation."""
    self_domain = RealityDomain(domain_type=DomainType.SELF)
    world_domain = RealityDomain(domain_type=DomainType.WORLD)

    # SelfReality can transition to any domain
    assert self_domain.can_transition_to(world_domain)

    # Any domain can transition back to SelfReality
    assert world_domain.can_transition_to(self_domain)


# ============================================================================
# Test 7: Reality Status
# ============================================================================

def test_physical_reality_is_foundational():
    """Test that physical reality is foundational."""
    assert RealityStatus.PHYSICAL.is_foundational()
    assert RealityStatus.BIOLOGICAL.is_foundational()
    assert not RealityStatus.SOCIAL.is_foundational()
    assert not RealityStatus.HYPOTHETICAL.is_foundational()


def test_hypothetical_cannot_produce_physical_effect():
    """Test that hypothetical cannot directly produce physical effects."""
    # Hypothetical requires bridge
    assert RealityStatus.HYPOTHETICAL.requires_bridge_for_physical()
    assert not RealityStatus.HYPOTHETICAL.can_produce_physical_effect()

    # Physical can produce physical effects
    assert RealityStatus.PHYSICAL.can_produce_physical_effect()


# ============================================================================
# Test 8: Constitutional Validator
# ============================================================================

def test_validator_enforces_all_laws():
    """Test that RealityValidator enforces all constitutional laws."""
    domain = RealityDomain(domain_type=DomainType.WORLD)
    observer = EmbodiedObserver(
        observer_id="obs_1",
        body_state=BodyState.FUNCTIONAL,
        need_state=NeedState.SATISFIED,
        available_sensory_channels=frozenset({"visual"}),
        available_actions=frozenset({"observe"}),
        biological_needs=frozenset({"oxygen"}),
    )
    life_ctx = LifeContext(
        life_phase=LifePhase.MATURITY,
        organism_type="human",
        biological_requirements=frozenset({"oxygen"}),
        life_constraints=frozenset({"temperature"}),
    )
    world_ctx = WorldContext(
        world_type=WorldType.NATURAL,
        spatial_structure="outdoor",
        physical_constraints=frozenset({"gravity"}),
        physical_laws=frozenset({"physics"}),
    )
    effect = RealityEffect(
        effect_type=EffectType.SENSORY,
        source_description="stone",
        manifestation="solid",
        source_status=RealityStatus.PHYSICAL,
    )

    unit = MinimalRealityUnit(
        reality_domain=domain,
        reality_status=RealityStatus.PHYSICAL,
        entity_or_process="stone",
        embodied_observer=observer,
        life_context=life_ctx,
        world_context=world_ctx,
        time_marker="2024-01-15",
        place_marker="ground",
        reality_effects=frozenset({effect}),
        physical_constraints=frozenset({"mass"}),
        biological_constraints=frozenset({"inert"}),
        existence_conditions=frozenset({"stable"}),
        known_boundaries=frozenset({"surface"}),
    )

    # Valid unit should have no violations
    violations = RealityValidator.validate_minimal_reality_unit(unit)
    assert len(violations) == 0
    assert RealityValidator.is_valid_minimal_reality_unit(unit)


# ============================================================================
# Test 9: Integration Scenario - Physical Observation
# ============================================================================

def test_integration_physical_observation():
    """Integration test: Physical observation by embodied observer."""
    # Observer in SelfReality
    observer = EmbodiedObserver(
        observer_id="scientist_1",
        body_state=BodyState.FUNCTIONAL,
        need_state=NeedState.SATISFIED,
        available_sensory_channels=frozenset({"visual", "tactile"}),
        available_actions=frozenset({"observe", "measure", "record"}),
        biological_needs=frozenset({"oxygen", "water", "food"}),
    )

    # Life context
    life_ctx = LifeContext(
        life_phase=LifePhase.MATURITY,
        organism_type="homo_sapiens",
        biological_requirements=frozenset({"oxygen", "nutrients", "water"}),
        life_constraints=frozenset({"temperature_range", "pressure_range"}),
        reproductive_capability=True,
    )

    # World context (laboratory)
    world_ctx = WorldContext(
        world_type=WorldType.LABORATORY,
        spatial_structure="Controlled lab environment",
        physical_constraints=frozenset({"controlled_temperature", "controlled_pressure"}),
        physical_laws=frozenset({"thermodynamics", "mechanics"}),
        accessible_regions=frozenset({"lab_bench", "measurement_area"}),
    )

    # Reality effect (visual observation)
    visual_effect = RealityEffect(
        effect_type=EffectType.SENSORY,
        source_description="Specimen under microscope",
        manifestation="Cellular structure visible",
        source_status=RealityStatus.BIOLOGICAL,
    )

    # MinimalRealityUnit
    reality_unit = MinimalRealityUnit(
        reality_domain=RealityDomain(domain_type=DomainType.LIFE),
        reality_status=RealityStatus.BIOLOGICAL,
        entity_or_process="Biological specimen (cell culture)",
        embodied_observer=observer,
        life_context=life_ctx,
        world_context=world_ctx,
        time_marker="2024-01-15T14:30:00Z",
        place_marker="Lab bench position (2, 3), microscope stage",
        reality_effects=frozenset({visual_effect}),
        physical_constraints=frozenset({"size_limit", "temperature_sensitivity"}),
        biological_constraints=frozenset({"viable_environment", "nutrient_availability"}),
        existence_conditions=frozenset({"culture_medium", "controlled_environment"}),
        known_boundaries=frozenset({"petri_dish_boundary", "observation_window"}),
        reality_residuals=frozenset({
            RealityResidual(
                description="Exact cell count uncertain due to overlapping cells",
                residual_type="measurement_uncertainty",
                severity="minor"
            )
        })
    )

    # Validate
    assert reality_unit.is_valid
    assert reality_unit.has_residuals
    assert reality_unit.observer_is_part_of_reality  # Property, not method
    assert not reality_unit.is_produced_by_system()
    assert not reality_unit.can_be_certified_by_system()
    assert reality_unit.precedes_all_traces()
    assert reality_unit.grounds_resistance_to_hallucination()

    # Validator check
    violations = RealityValidator.validate_minimal_reality_unit(reality_unit)
    assert len(violations) == 0


# ============================================================================
# Test 10: Residual Preservation
# ============================================================================

def test_reality_residuals_preserved():
    """Test that reality residuals are preserved."""
    residual1 = RealityResidual(
        description="Boundary uncertainty at microscopic scale",
        residual_type="boundary_uncertainty",
        severity="minor"
    )

    residual2 = RealityResidual(
        description="Unknown interaction effects with environment",
        residual_type="constraint_unknown",
        severity="moderate"
    )

    domain = RealityDomain(domain_type=DomainType.WORLD)
    observer = EmbodiedObserver(
        observer_id="obs_1",
        body_state=BodyState.FUNCTIONAL,
        need_state=NeedState.SATISFIED,
        available_sensory_channels=frozenset({"visual"}),
        available_actions=frozenset({"observe"}),
        biological_needs=frozenset({"oxygen"}),
    )
    life_ctx = LifeContext(
        life_phase=LifePhase.MATURITY,
        organism_type="human",
        biological_requirements=frozenset({"oxygen"}),
        life_constraints=frozenset({"temperature"}),
    )
    world_ctx = WorldContext(
        world_type=WorldType.NATURAL,
        spatial_structure="outdoor",
        physical_constraints=frozenset({"gravity"}),
        physical_laws=frozenset({"physics"}),
    )
    effect = RealityEffect(
        effect_type=EffectType.SENSORY,
        source_description="particle",
        manifestation="visible",
        source_status=RealityStatus.PHYSICAL,
    )

    unit = MinimalRealityUnit(
        reality_domain=domain,
        reality_status=RealityStatus.PHYSICAL,
        entity_or_process="quantum_particle",
        embodied_observer=observer,
        life_context=life_ctx,
        world_context=world_ctx,
        time_marker="2024-01-15",
        place_marker="chamber",
        reality_effects=frozenset({effect}),
        physical_constraints=frozenset({"uncertainty"}),
        biological_constraints=frozenset({"non_biological"}),
        existence_conditions=frozenset({"vacuum"}),
        known_boundaries=frozenset({"probabilistic"}),
        reality_residuals=frozenset({residual1, residual2}),
    )

    assert unit.has_residuals
    assert len(unit.reality_residuals) == 2
    assert residual1 in unit.reality_residuals
    assert residual2 in unit.reality_residuals


# ============================================================================
# Run all tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
