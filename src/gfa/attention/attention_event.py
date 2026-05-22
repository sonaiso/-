"""
Attention Event - Single Attention Operation

An AttentionEvent represents one attention operation over traces.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional, Set
from uuid import UUID, uuid4
from datetime import datetime


class AttentionType(Enum):
    """Types of attention operations"""

    VOLUNTARY = auto()  # Deliberate, goal-directed
    INVOLUNTARY = auto()  # Stimulus-driven, automatic
    SUSTAINED = auto()  # Prolonged focus
    SELECTIVE = auto()  # Filter specific features
    DIVIDED = auto()  # Multiple traces simultaneously
    ALTERNATING = auto()  # Sequential switching


@dataclass(frozen=True)
class AttentionEvent:
    """
    Single attention operation

    An AttentionEvent:
    - Operates on traces from CognitiveCarrier
    - Selects subset for processing
    - Does NOT certify selected traces
    - Does NOT raise epistemic rank
    - Preserves original trace_ids
    - Records ignored traces as residuals
    """

    event_id: UUID = field(default_factory=uuid4)
    attention_type: AttentionType = field(default=AttentionType.SELECTIVE)
    carrier_id: Optional[UUID] = None  # Which carrier enabled this attention
    input_trace_ids: Set[UUID] = field(default_factory=set)
    selected_trace_ids: Set[UUID] = field(default_factory=set)
    ignored_trace_ids: Set[UUID] = field(default_factory=set)
    timestamp: datetime = field(default_factory=datetime.now)
    attention_capacity_used: float = 0.0  # [0, 1] fraction of capacity
    policy_applied: Optional[str] = None  # Which policy was used
    residuals: dict = field(default_factory=dict)  # Unresolved aspects

    def __post_init__(self):
        """Validate attention event"""
        # Carrier is mandatory
        if self.carrier_id is None:
            raise ValueError("AttentionEvent requires carrier_id (no attention without carrier)")

        # Capacity must be in valid range
        if not (0.0 <= self.attention_capacity_used <= 1.0):
            raise ValueError(f"Attention capacity must be in [0, 1], got {self.attention_capacity_used}")

        # Selected + ignored must equal input
        expected = self.input_trace_ids
        actual = self.selected_trace_ids | self.ignored_trace_ids

        if expected != actual:
            missing = expected - actual
            extra = actual - expected
            raise ValueError(
                f"Selected + ignored must equal input traces. "
                f"Missing: {missing}, Extra: {extra}"
            )

    def can_certify(self) -> bool:
        """Attention CANNOT certify"""
        return False

    def can_raise_rank(self) -> bool:
        """Attention CANNOT raise epistemic rank"""
        return False

    def can_create_memory(self) -> bool:
        """Attention does NOT create memory"""
        return False

    def can_compare_traces(self) -> bool:
        """Attention does NOT compare traces"""
        return False

    def can_bind(self) -> bool:
        """Attention does NOT bind traces"""
        return False

    def can_learn(self) -> bool:
        """Attention does NOT learn"""
        return False

    def selection_ratio(self) -> float:
        """Fraction of traces selected"""
        if not self.input_trace_ids:
            return 0.0
        return len(self.selected_trace_ids) / len(self.input_trace_ids)

    def ignored_ratio(self) -> float:
        """Fraction of traces ignored"""
        if not self.input_trace_ids:
            return 0.0
        return len(self.ignored_trace_ids) / len(self.input_trace_ids)
