"""
CarrierCapacity - Declared Cognitive Capacities

Capacities are DECLARATIONS, not implementations.
A carrier declares what it can do, but declaration ≠ correctness.

Critical laws:
- Capacity declaration is not proof of correctness
- Missing capacity must become residual or failure
- Capacity does not raise epistemic rank
- Capacity availability depends on embodiment state
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, FrozenSet


class CapacityLevel(Enum):
    """Level of capacity availability."""
    FULL = auto()           # Full capacity available
    PARTIAL = auto()        # Partial capacity available
    DEGRADED = auto()       # Degraded capacity
    ABSENT = auto()         # Capacity absent


@dataclass(frozen=True)
class CarrierCapacity:
    """
    Base class for carrier capacity declarations.

    CRITICAL: Capacity is a DECLARATION, not a proof.
    Having capacity does not mean outputs are correct.
    """

    capacity_level: CapacityLevel
    capacity_description: Optional[str] = None
    known_limitations: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        # Convert sets to frozensets
        if self.known_limitations and not isinstance(self.known_limitations, frozenset):
            object.__setattr__(
                self,
                'known_limitations',
                frozenset(self.known_limitations)
            )

    @property
    def is_available(self) -> bool:
        """Check if capacity is available (full or partial)."""
        return self.capacity_level in {CapacityLevel.FULL, CapacityLevel.PARTIAL}

    @property
    def is_absent(self) -> bool:
        """Check if capacity is absent."""
        return self.capacity_level == CapacityLevel.ABSENT

    @property
    def is_degraded(self) -> bool:
        """Check if capacity is degraded."""
        return self.capacity_level == CapacityLevel.DEGRADED


@dataclass(frozen=True)
class SensoryCapacity(CarrierCapacity):
    """
    Capacity to receive sensory input.

    CRITICAL: Having sensory capacity does not mean sensory trace is correct.
    """

    available_channels: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        super().__post_init__()
        if self.available_channels and not isinstance(self.available_channels, frozenset):
            object.__setattr__(
                self,
                'available_channels',
                frozenset(self.available_channels)
            )


@dataclass(frozen=True)
class AttentionCapacity(CarrierCapacity):
    """
    Capacity to selectively focus on traces.

    CRITICAL: Attention selects; it does NOT certify.
    Attention does NOT raise epistemic rank.
    """

    selection_policy: Optional[str] = None

    def can_raise_rank(self) -> bool:
        """
        Can attention raise epistemic rank?

        CRITICAL LAW: NO. Attention affects processing priority, not epistemic rank.
        """
        return False


@dataclass(frozen=True)
class MemoryCapacity(CarrierCapacity):
    """
    Capacity to store and recall traces.

    CRITICAL: Recalled trace ≠ original trace.
    Memory recall creates a new trace about previous trace.
    Memory does NOT certify original claim.
    """

    storage_type: Optional[str] = None
    distortion_risk: Optional[str] = None

    def recall_equals_original(self) -> bool:
        """
        Does recalled trace equal original trace?

        CRITICAL LAW: NO. Recall(trace) = memory_trace_about_original_trace.
        """
        return False


@dataclass(frozen=True)
class ComparisonCapacity(CarrierCapacity):
    """
    Capacity to compare traces.

    CRITICAL: Comparison is the foundation of all binding.
    No binding without comparison.
    """

    comparison_fields: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        super().__post_init__()
        if self.comparison_fields and not isinstance(self.comparison_fields, frozenset):
            object.__setattr__(
                self,
                'comparison_fields',
                frozenset(self.comparison_fields)
            )


@dataclass(frozen=True)
class BindingCapacity(CarrierCapacity):
    """
    Capacity to create bindings between traces.

    CRITICAL: Binding capacity does not mean binding is correct.
    Primitive binding does NOT raise rank.
    """

    binding_types: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        super().__post_init__()
        if self.binding_types and not isinstance(self.binding_types, frozenset):
            object.__setattr__(
                self,
                'binding_types',
                frozenset(self.binding_types)
            )

    def primitive_binding_raises_rank(self) -> bool:
        """
        Does primitive binding raise epistemic rank?

        CRITICAL LAW: NO. Primitive binding produces CANDIDATE relations only.
        """
        return False


@dataclass(frozen=True)
class InterpretationCapacity(CarrierCapacity):
    """
    Capacity to interpret traces.

    CRITICAL: Interpretation capacity does not create meaning.
    Interpretation does not certify.
    """

    interpretation_types: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        super().__post_init__()
        if self.interpretation_types and not isinstance(self.interpretation_types, frozenset):
            object.__setattr__(
                self,
                'interpretation_types',
                frozenset(self.interpretation_types)
            )

    def creates_meaning(self) -> bool:
        """
        Does interpretation create meaning?

        CRITICAL LAW: NO. Interpretation operates on existing traces.
        """
        return False


@dataclass(frozen=True)
class FeedbackCapacity(CarrierCapacity):
    """
    Capacity to receive feedback about processing results.

    Feedback enables learning from success/failure.
    """

    feedback_channels: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        super().__post_init__()
        if self.feedback_channels and not isinstance(self.feedback_channels, frozenset):
            object.__setattr__(
                self,
                'feedback_channels',
                frozenset(self.feedback_channels)
            )


@dataclass(frozen=True)
class OutputCapacity(CarrierCapacity):
    """
    Capacity to produce outputs.

    Output capacity does not certify output correctness.
    """

    output_types: Optional[FrozenSet[str]] = None

    def __post_init__(self):
        super().__post_init__()
        if self.output_types and not isinstance(self.output_types, frozenset):
            object.__setattr__(
                self,
                'output_types',
                frozenset(self.output_types)
            )
