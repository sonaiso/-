"""
CognitiveCarrier - The Cognitive Processing Substrate

This is the core object representing the cognitive carrier that can process traces.

Critical laws:
- No cognitive processing without CognitiveCarrier
- Carrier must declare all required capacities
- Missing capacity becomes residual or failure
- Carrier does NOT create meaning
- Carrier does NOT issue judgment
- Carrier does NOT certify
- Carrier does NOT raise rank
"""

from dataclasses import dataclass, field
from typing import Optional, FrozenSet
from uuid import UUID, uuid4

from .embodied_state import EmbodiedState
from .carrier_capacity import (
    SensoryCapacity,
    AttentionCapacity,
    MemoryCapacity,
    ComparisonCapacity,
    BindingCapacity,
    InterpretationCapacity,
    FeedbackCapacity,
    OutputCapacity,
)


@dataclass(frozen=True)
class CarrierResidual:
    """
    A residual about the cognitive carrier itself.

    This represents what is unresolved, uncertain, or incomplete
    about the carrier's capacities or state.
    """

    description: str
    residual_type: str  # e.g., "capacity_limitation", "degraded_function"
    severity: Optional[str] = None

    def __post_init__(self):
        if not self.description or not self.description.strip():
            raise ValueError("Residual description cannot be empty")
        if not self.residual_type or not self.residual_type.strip():
            raise ValueError("Residual type cannot be empty")


@dataclass(frozen=True)
class CognitiveCarrier:
    """
    The Cognitive Carrier - the substrate for cognitive processing.

    This represents the cognitive system that can process FirstPriorUnits.

    MANDATORY fields:
    1. carrier_id
    2. embodied_state
    3. sensory_capacity
    4. attention_capacity
    5. memory_capacity
    6. comparison_capacity
    7. binding_capacity
    8. interpretation_capacity
    9. feedback_capacity
    10. output_capacity

    Critical laws enforced:
    - All 10 fields are mandatory
    - Carrier does NOT create meaning
    - Carrier does NOT issue judgment
    - Carrier does NOT certify
    - Carrier does NOT raise rank
    - Missing capacity becomes residual
    """

    # Mandatory fields (no defaults)
    carrier_id: str
    embodied_state: EmbodiedState
    sensory_capacity: SensoryCapacity
    attention_capacity: AttentionCapacity
    memory_capacity: MemoryCapacity
    comparison_capacity: ComparisonCapacity
    binding_capacity: BindingCapacity
    interpretation_capacity: InterpretationCapacity
    feedback_capacity: FeedbackCapacity
    output_capacity: OutputCapacity

    # Fields with defaults (must come last)
    carrier_trace_id: UUID = field(default_factory=uuid4)
    carrier_residuals: FrozenSet[CarrierResidual] = field(default_factory=frozenset)
    carrier_rank: str = "SUBSTRATE"  # Not epistemic rank - just carrier classification

    def __post_init__(self):
        # Validate all mandatory fields
        self._validate_mandatory_fields()

        # Convert sets to frozensets
        if self.carrier_residuals and not isinstance(self.carrier_residuals, frozenset):
            object.__setattr__(
                self,
                'carrier_residuals',
                frozenset(self.carrier_residuals)
            )

    def _validate_mandatory_fields(self):
        """Validate all mandatory fields are present and valid."""
        # Check carrier_id
        if not self.carrier_id or not self.carrier_id.strip():
            raise ValueError("carrier_id cannot be empty")

        # Check embodied_state
        if not isinstance(self.embodied_state, EmbodiedState):
            raise ValueError("embodied_state is mandatory")

        # Check all capacities
        if not isinstance(self.sensory_capacity, SensoryCapacity):
            raise ValueError("sensory_capacity is mandatory")

        if not isinstance(self.attention_capacity, AttentionCapacity):
            raise ValueError("attention_capacity is mandatory")

        if not isinstance(self.memory_capacity, MemoryCapacity):
            raise ValueError("memory_capacity is mandatory")

        if not isinstance(self.comparison_capacity, ComparisonCapacity):
            raise ValueError("comparison_capacity is mandatory")

        if not isinstance(self.binding_capacity, BindingCapacity):
            raise ValueError("binding_capacity is mandatory")

        if not isinstance(self.interpretation_capacity, InterpretationCapacity):
            raise ValueError("interpretation_capacity is mandatory")

        if not isinstance(self.feedback_capacity, FeedbackCapacity):
            raise ValueError("feedback_capacity is mandatory")

        if not isinstance(self.output_capacity, OutputCapacity):
            raise ValueError("output_capacity is mandatory")

    @property
    def is_valid(self) -> bool:
        """Check if this CognitiveCarrier is fully valid."""
        try:
            self._validate_mandatory_fields()
            return True
        except ValueError:
            return False

    @property
    def has_residuals(self) -> bool:
        """Check if this carrier has residuals."""
        return bool(self.carrier_residuals)

    @property
    def can_process_traces(self) -> bool:
        """
        Can this carrier process traces?

        Requires: functional embodiment and available capacities.
        """
        return (
            self.embodied_state.is_functional and
            self.attention_capacity.is_available and
            self.memory_capacity.is_available and
            self.comparison_capacity.is_available
        )

    @property
    def can_create_bindings(self) -> bool:
        """
        Can this carrier create bindings?

        Requires: processing capability and binding capacity.
        """
        return (
            self.can_process_traces and
            self.binding_capacity.is_available
        )

    def creates_meaning(self) -> bool:
        """
        Does this carrier create meaning?

        CRITICAL LAW: NO. Carrier provides substrate for processing.
        Meaning emerges from binding history and learning.
        """
        return False

    def issues_judgment(self) -> bool:
        """
        Does this carrier issue judgment?

        CRITICAL LAW: NO. Carrier provides processing capacity only.
        Judgment requires full epistemic evaluation.
        """
        return False

    def certifies_claims(self) -> bool:
        """
        Does this carrier certify claims?

        CRITICAL LAW: NO. Carrier processes traces.
        Certification requires evidence and validation.
        """
        return False

    def raises_rank(self) -> bool:
        """
        Does carrier processing raise epistemic rank?

        CRITICAL LAW: NO. Processing does not imply correctness.
        Rank promotion requires evidence and testing.
        """
        return False

    def capacity_proves_correctness(self) -> bool:
        """
        Does having capacity prove output correctness?

        CRITICAL LAW: NO. Capacity is declaration, not proof.
        """
        return False

    def __str__(self) -> str:
        return (
            f"CognitiveCarrier("
            f"id={self.carrier_id}, "
            f"embodiment={self.embodied_state.embodiment_type.name}, "
            f"residuals={len(self.carrier_residuals)})"
        )
