"""
RealityValidator - Constitutional Law Enforcer for Reality Layer

This validator enforces all critical laws for the RealityGeometry Kernel.

Critical laws enforced:
1. Reality is NOT produced by the system
2. Reality cannot be CERTIFIED by the system
3. Reality precedes all traces
4. Observer is part of reality (embodied)
5. Hypothetical → Physical requires experimental bridge
6. Physical reality is foundational
7. Reality grounds resistance to hallucination
8. All 15 mandatory fields present in MinimalRealityUnit
9. Observer has body state and biological needs
10. Life context and world context are mandatory
11. Reality effects ≠ Reality itself
12. Time and place markers are mandatory

This is the constitutional enforcer for Layer -2.
"""

from typing import List, Optional

from .minimal_reality_unit import MinimalRealityUnit
from .reality_status import RealityStatus
from .reality_bridge import RealityBridge, BridgeType, BridgeValidation
from .reality_effect import RealityEffect
from .embodied_observer import EmbodiedObserver


class RealityValidator:
    """
    Constitutional law enforcer for RealityGeometry Kernel.

    This validator ensures all critical laws are followed.
    """

    @staticmethod
    def validate_minimal_reality_unit(unit: MinimalRealityUnit) -> List[str]:
        """
        Validate MinimalRealityUnit against all critical laws.

        Returns list of violations (empty if valid).
        """
        violations = []

        # Law 1: Check all mandatory fields present
        if not unit.is_valid:
            violations.append("MinimalRealityUnit has invalid or missing mandatory fields")

        # Law 2: Reality is NOT produced by system
        if unit.is_produced_by_system():
            violations.append("CRITICAL: Reality cannot be produced by system")

        # Law 3: Reality cannot be CERTIFIED by system
        if unit.can_be_certified_by_system():
            violations.append("CRITICAL: Reality cannot be certified by system")

        # Law 4: Reality precedes all traces
        if not unit.precedes_all_traces():
            violations.append("CRITICAL: Reality must precede all traces")

        # Law 5: Reality grounds resistance to hallucination
        if not unit.grounds_resistance_to_hallucination():
            violations.append("CRITICAL: Reality must ground resistance to hallucination")

        # Law 6: Observer is part of reality
        if not unit.observer_is_part_of_reality:  # Property, not method
            violations.append("CRITICAL: Observer must be part of reality (embodied)")

        # Law 7: Observer has valid embodiment
        if not isinstance(unit.embodied_observer, EmbodiedObserver):
            violations.append("Observer must be EmbodiedObserver instance")

        # Law 8: Observer can observe or act
        if not (unit.embodied_observer.can_observe or unit.embodied_observer.can_act):
            violations.append("Observer must be able to observe or act")

        # Law 9: Physical/biological constraints present
        if not unit.physical_constraints:
            violations.append("Physical constraints cannot be empty")

        if not unit.biological_constraints:
            violations.append("Biological constraints cannot be empty")

        # Law 10: Existence conditions present
        if not unit.existence_conditions:
            violations.append("Existence conditions cannot be empty")

        # Law 11: Reality effects ≠ Reality
        for effect in unit.reality_effects:
            if not isinstance(effect, RealityEffect):
                violations.append("All reality_effects must be RealityEffect instances")
            if effect.equals_reality():
                violations.append("CRITICAL: RealityEffect cannot equal Reality")

        # Law 12: Time and place markers mandatory
        if not unit.time_marker or not unit.time_marker.strip():
            violations.append("time_marker cannot be empty")

        if not unit.place_marker or not unit.place_marker.strip():
            violations.append("place_marker cannot be empty")

        return violations

    @staticmethod
    def validate_reality_bridge(bridge: RealityBridge) -> List[str]:
        """
        Validate reality bridge against critical laws.

        Returns list of violations (empty if valid).
        """
        violations = []

        # Law 1: Hypothetical → Physical requires experimental bridge
        if (bridge.source_status == RealityStatus.HYPOTHETICAL and
            bridge.target_status == RealityStatus.PHYSICAL):
            if bridge.bridge_type != BridgeType.EXPERIMENTAL:
                violations.append(
                    "CRITICAL: Hypothetical → Physical requires EXPERIMENTAL bridge"
                )

        # Law 2: Forbidden crossings must be rejected
        if bridge.is_forbidden:
            violations.append(
                f"CRITICAL: Bridge crossing {bridge.source_status.name} → "
                f"{bridge.target_status.name} is FORBIDDEN"
            )

        # Law 3: Bridge type must match transition
        validation = bridge.validate_crossing()
        if validation == BridgeValidation.INVALID:
            violations.append(
                f"Invalid bridge: {bridge.source_status.name} → "
                f"{bridge.target_status.name} via {bridge.bridge_type.name}"
            )

        return violations

    @staticmethod
    def validate_observer_embodiment(observer: EmbodiedObserver) -> List[str]:
        """
        Validate embodied observer against critical laws.

        Returns list of violations (empty if valid).
        """
        violations = []

        # Law 1: Observer is NOT external to reality
        if observer.is_external_to_reality():
            violations.append("CRITICAL: Observer cannot be external to reality")

        # Law 2: Observer cannot escape embodiment
        if observer.can_escape_embodiment():
            violations.append("CRITICAL: Observer cannot escape embodiment")

        # Law 3: Observer must have sensory channels
        if not observer.available_sensory_channels:
            violations.append("Observer must have available sensory channels")

        # Law 4: Observer must have action capabilities
        if not observer.available_actions:
            violations.append("Observer must have available action capabilities")

        # Law 5: Observer must have biological needs
        if not observer.biological_needs:
            violations.append("Observer must have biological needs")

        # Law 6: Observer must be able to function
        if not (observer.can_observe or observer.can_act):
            violations.append("Observer must be able to observe or act")

        return violations

    @staticmethod
    def validate_reality_effect(effect: RealityEffect) -> List[str]:
        """
        Validate reality effect against critical laws.

        Returns list of violations (empty if valid).
        """
        violations = []

        # Law 1: RealityEffect ≠ Reality
        if effect.equals_reality():
            violations.append("CRITICAL: RealityEffect cannot equal Reality")

        # Law 2: Effect cannot certify source
        if effect.can_certify_source():
            violations.append("CRITICAL: RealityEffect cannot certify its source")

        # Law 3: Hypothetical sources require validation
        if effect.is_hypothetical_source and not effect.requires_validation:
            violations.append("Hypothetical source must require validation")

        # Law 4: Source description mandatory
        if not effect.source_description or not effect.source_description.strip():
            violations.append("source_description cannot be empty")

        # Law 5: Manifestation mandatory
        if effect.manifestation is None:
            violations.append("manifestation is mandatory")

        return violations

    @staticmethod
    def is_valid_minimal_reality_unit(unit: MinimalRealityUnit) -> bool:
        """Check if MinimalRealityUnit is fully valid (no violations)."""
        return len(RealityValidator.validate_minimal_reality_unit(unit)) == 0

    @staticmethod
    def is_valid_reality_bridge(bridge: RealityBridge) -> bool:
        """Check if RealityBridge is fully valid (no violations)."""
        return len(RealityValidator.validate_reality_bridge(bridge)) == 0

    @staticmethod
    def is_valid_observer(observer: EmbodiedObserver) -> bool:
        """Check if EmbodiedObserver is fully valid (no violations)."""
        return len(RealityValidator.validate_observer_embodiment(observer)) == 0

    @staticmethod
    def is_valid_reality_effect(effect: RealityEffect) -> bool:
        """Check if RealityEffect is fully valid (no violations)."""
        return len(RealityValidator.validate_reality_effect(effect)) == 0
