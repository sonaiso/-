"""
CarrierValidator - Constitutional Law Enforcer for CognitiveCarrier

This validator enforces all critical laws for the CognitiveCarrierGeometry Kernel.

Critical laws enforced:
1. No cognitive processing without CognitiveCarrier
2. Carrier must declare attention capacity
3. Carrier must declare memory capacity
4. Carrier must declare comparison capacity
5. Carrier must declare binding capacity
6. Carrier does NOT create meaning
7. Carrier does NOT issue judgment
8. Carrier does NOT certify
9. Carrier does NOT raise rank
10. Carrier capacity is NOT proof of correctness
11. Missing capacity must become residual or failure

This is the constitutional enforcer for Layer 0.5.
"""

from typing import List

from .cognitive_carrier import CognitiveCarrier
from .carrier_capacity import CapacityLevel


class CarrierValidator:
    """
    Constitutional law enforcer for CognitiveCarrierGeometry Kernel.

    This validator ensures all critical laws are followed.
    """

    @staticmethod
    def validate_cognitive_carrier(carrier: CognitiveCarrier) -> List[str]:
        """
        Validate CognitiveCarrier against all critical laws.

        Returns list of violations (empty if valid).
        """
        violations = []

        # Law 1: Check all mandatory fields present
        if not carrier.is_valid:
            violations.append("CognitiveCarrier has invalid or missing mandatory fields")

        # Law 2: Attention capacity required
        if not carrier.attention_capacity:
            violations.append("Carrier must declare attention_capacity")
        elif carrier.attention_capacity.is_absent:
            violations.append("Attention capacity cannot be ABSENT")

        # Law 3: Memory capacity required
        if not carrier.memory_capacity:
            violations.append("Carrier must declare memory_capacity")
        elif carrier.memory_capacity.is_absent:
            violations.append("Memory capacity cannot be ABSENT")

        # Law 4: Comparison capacity required
        if not carrier.comparison_capacity:
            violations.append("Carrier must declare comparison_capacity")
        elif carrier.comparison_capacity.is_absent:
            violations.append("Comparison capacity cannot be ABSENT")

        # Law 5: Binding capacity required
        if not carrier.binding_capacity:
            violations.append("Carrier must declare binding_capacity")
        elif carrier.binding_capacity.is_absent:
            violations.append("Binding capacity cannot be ABSENT")

        # Law 6: Carrier does NOT create meaning
        if carrier.creates_meaning():
            violations.append("CRITICAL: Carrier cannot create meaning")

        # Law 7: Carrier does NOT issue judgment
        if carrier.issues_judgment():
            violations.append("CRITICAL: Carrier cannot issue judgment")

        # Law 8: Carrier does NOT certify
        if carrier.certifies_claims():
            violations.append("CRITICAL: Carrier cannot certify claims")

        # Law 9: Carrier does NOT raise rank
        if carrier.raises_rank():
            violations.append("CRITICAL: Carrier cannot raise epistemic rank")

        # Law 10: Capacity is NOT proof of correctness
        if carrier.capacity_proves_correctness():
            violations.append("CRITICAL: Capacity does not prove correctness")

        # Law 11: Embodiment state required
        if not carrier.embodied_state:
            violations.append("Carrier must have embodied_state")

        # Law 12: Functional capacities needed for processing
        if carrier.can_process_traces:
            if not carrier.embodied_state.is_functional:
                violations.append("Processing requires functional embodiment")

        # Law 13: Attention does not raise rank
        if hasattr(carrier.attention_capacity, 'can_raise_rank'):
            if carrier.attention_capacity.can_raise_rank():
                violations.append("CRITICAL: Attention cannot raise rank")

        # Law 14: Memory recall ≠ original
        if hasattr(carrier.memory_capacity, 'recall_equals_original'):
            if carrier.memory_capacity.recall_equals_original():
                violations.append("CRITICAL: Recalled trace cannot equal original trace")

        # Law 15: Primitive binding does not raise rank
        if hasattr(carrier.binding_capacity, 'primitive_binding_raises_rank'):
            if carrier.binding_capacity.primitive_binding_raises_rank():
                violations.append("CRITICAL: Primitive binding cannot raise rank")

        # Law 16: Interpretation does not create meaning
        if hasattr(carrier.interpretation_capacity, 'creates_meaning'):
            if carrier.interpretation_capacity.creates_meaning():
                violations.append("CRITICAL: Interpretation cannot create meaning")

        return violations

    @staticmethod
    def is_valid_cognitive_carrier(carrier: CognitiveCarrier) -> bool:
        """Check if CognitiveCarrier is fully valid (no violations)."""
        return len(CarrierValidator.validate_cognitive_carrier(carrier)) == 0

    @staticmethod
    def validate_processing_readiness(carrier: CognitiveCarrier) -> List[str]:
        """
        Validate that carrier is ready for cognitive processing.

        Returns list of violations (empty if ready).
        """
        violations = []

        # Check basic validity first
        basic_violations = CarrierValidator.validate_cognitive_carrier(carrier)
        if basic_violations:
            violations.extend(basic_violations)
            return violations

        # Check processing readiness
        if not carrier.can_process_traces:
            violations.append("Carrier not ready for trace processing")

            # Identify specific issues
            if not carrier.embodied_state.is_functional:
                violations.append("Embodiment not functional")

            if not carrier.attention_capacity.is_available:
                violations.append("Attention capacity not available")

            if not carrier.memory_capacity.is_available:
                violations.append("Memory capacity not available")

            if not carrier.comparison_capacity.is_available:
                violations.append("Comparison capacity not available")

        return violations

    @staticmethod
    def validate_binding_readiness(carrier: CognitiveCarrier) -> List[str]:
        """
        Validate that carrier is ready for binding operations.

        Returns list of violations (empty if ready).
        """
        violations = []

        # Check processing readiness first
        processing_violations = CarrierValidator.validate_processing_readiness(carrier)
        if processing_violations:
            violations.extend(processing_violations)
            return violations

        # Check binding readiness
        if not carrier.can_create_bindings:
            violations.append("Carrier not ready for binding operations")

            if not carrier.binding_capacity.is_available:
                violations.append("Binding capacity not available")

        return violations
