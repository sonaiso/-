"""
CognitiveCarrierGeometry Kernel - The Cognitive Processing Substrate

This module implements the cognitive carrier that serves as the substrate for all
cognitive processing operations.

Key Principle:
- No cognitive processing without an admissible CognitiveCarrier
- FirstPriorUnit cannot be processed, compared, remembered, interpreted, or bound
  unless there exists a CognitiveCarrier with declared minimal capacities

Critical Laws:
- Carrier must declare attention capacity
- Carrier must declare memory capacity
- Carrier must declare comparison capacity
- Carrier must declare binding capacity
- Carrier does NOT create meaning
- Carrier does NOT issue judgment
- Carrier does NOT certify claims
- Carrier does NOT raise epistemic rank
- Carrier capacity is NOT proof of correctness
- Missing capacity must become residual or failure

This is Layer 0.5 - the bridge between traces and cognitive operations.
"""

from .embodied_state import EmbodiedState, EmbodimentType
from .carrier_capacity import (
    CarrierCapacity,
    CapacityLevel,
    SensoryCapacity,
    AttentionCapacity,
    MemoryCapacity,
    ComparisonCapacity,
    BindingCapacity,
    InterpretationCapacity,
    FeedbackCapacity,
    OutputCapacity,
)
from .cognitive_carrier import CognitiveCarrier, CarrierResidual
from .carrier_validator import CarrierValidator

__all__ = [
    "EmbodiedState",
    "EmbodimentType",
    "CarrierCapacity",
    "CapacityLevel",
    "SensoryCapacity",
    "AttentionCapacity",
    "MemoryCapacity",
    "ComparisonCapacity",
    "BindingCapacity",
    "InterpretationCapacity",
    "FeedbackCapacity",
    "OutputCapacity",
    "CognitiveCarrier",
    "CarrierResidual",
    "CarrierValidator",
]
