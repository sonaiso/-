"""
Attention Gate - Selection Filter

An AttentionGate applies selection criteria to traces.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Optional, Set
from uuid import UUID


class GateStatus(Enum):
    """Status of gate application"""

    PASS = auto()  # Trace passes through
    BLOCK = auto()  # Trace is ignored
    PARTIAL = auto()  # Trace partially attended


@dataclass(frozen=True)
class AttentionGate:
    """
    Selection gate for attention

    An AttentionGate:
    - Filters traces based on criteria
    - Does NOT certify passing traces
    - Does NOT raise rank
    - Preserves original trace properties
    """

    gate_id: str
    criterion: Callable[[Any], bool]  # Selection function
    priority_weight: float = 1.0  # Relative importance [0, 1]
    description: str = ""

    def __post_init__(self):
        """Validate gate"""
        if not (0.0 <= self.priority_weight <= 1.0):
            raise ValueError(f"Priority weight must be in [0, 1], got {self.priority_weight}")

        if not callable(self.criterion):
            raise ValueError("Criterion must be callable")

    def apply(self, trace: Any) -> GateStatus:
        """
        Apply gate to trace

        Returns:
            GateStatus.PASS if trace passes
            GateStatus.BLOCK if trace is blocked
        """
        try:
            if self.criterion(trace):
                return GateStatus.PASS
            else:
                return GateStatus.BLOCK
        except Exception:
            # If criterion fails, block by default (fail-safe)
            return GateStatus.BLOCK

    def can_certify(self) -> bool:
        """Gate CANNOT certify traces"""
        return False

    def can_raise_rank(self) -> bool:
        """Gate CANNOT raise epistemic rank"""
        return False


@dataclass
class CompositeGate:
    """
    Combination of multiple gates

    Can combine gates with AND/OR logic
    """

    gates: list[AttentionGate] = field(default_factory=list)
    combination_mode: str = "AND"  # "AND" or "OR"

    def __post_init__(self):
        """Validate composite gate"""
        if self.combination_mode not in ("AND", "OR"):
            raise ValueError(f"Combination mode must be 'AND' or 'OR', got {self.combination_mode}")

        if not self.gates:
            raise ValueError("CompositeGate requires at least one gate")

    def apply(self, trace: Any) -> GateStatus:
        """Apply all gates"""
        results = [gate.apply(trace) for gate in self.gates]

        if self.combination_mode == "AND":
            # All gates must pass
            if all(status == GateStatus.PASS for status in results):
                return GateStatus.PASS
            elif all(status == GateStatus.BLOCK for status in results):
                return GateStatus.BLOCK
            else:
                return GateStatus.PARTIAL
        else:  # OR
            # At least one gate must pass
            if any(status == GateStatus.PASS for status in results):
                return GateStatus.PASS
            else:
                return GateStatus.BLOCK

    def can_certify(self) -> bool:
        """Composite gate CANNOT certify"""
        return False

    def can_raise_rank(self) -> bool:
        """Composite gate CANNOT raise rank"""
        return False
