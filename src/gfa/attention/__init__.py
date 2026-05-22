"""
AttentionGeometry Kernel - The First Processing Gate

This module implements attention as the first cognitive processing gate after
CognitiveCarrierGeometry.

Core Principle:
- Attention selects traces for processing
- Attention does NOT certify
- Attention does NOT raise epistemic rank
- Ignored traces become residuals, not deletion

Key Laws:
- No attention without CognitiveCarrier
- Attention requires attention_capacity
- Attention selects, but does NOT certify
- Attention changes processing priority, NOT epistemic rank
- Attention preserves original trace_id
- Ignored trace becomes residual
- Attention does NOT store memory
- Attention does NOT compare
- Attention does NOT bind
- Attention does NOT learn
- Attention does NOT create CPB

This is Layer 1 - the selection gate for cognitive processing.
"""

from .attention_event import AttentionEvent, AttentionType
from .attention_gate import AttentionGate, GateStatus
from .attention_policy import AttentionPolicy, PolicyType, SelectionCriterion
from .attended_trace import AttendedTrace, AttentionPriority
from .residual_taxonomy import (
    AttentionResidual,
    ResidualType,
    IgnoredTrace,
    PartiallyAttendedTrace,
)

__all__ = [
    "AttentionEvent",
    "AttentionType",
    "AttentionGate",
    "GateStatus",
    "AttentionPolicy",
    "PolicyType",
    "SelectionCriterion",
    "AttendedTrace",
    "AttentionPriority",
    "AttentionResidual",
    "ResidualType",
    "IgnoredTrace",
    "PartiallyAttendedTrace",
]
