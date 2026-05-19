"""
Trace System (نظام الأثر)

Tracks decision graph for explainability.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class TraceNodeType(Enum):
    """Types of trace nodes"""
    CARRIER = "carrier"
    ATOM = "atom"
    UNIT = "unit"
    CONTEXT = "context"
    SYLLABLE = "syllable"
    FORM = "form"
    LUGHA = "lugha"
    TYPE = "type"
    MUFRAD = "mufrad"
    RESIDUAL = "residual"
    EVIDENCE = "evidence"


@dataclass
class TraceNode:
    """
    عقدة أثر (Trace Node)

    Records a decision point in the pipeline.
    """
    node_type: TraceNodeType
    data: dict = field(default_factory=dict)
    parent: Optional['TraceNode'] = None
    children: list['TraceNode'] = field(default_factory=list)

    def add_child(self, child: 'TraceNode') -> 'TraceNode':
        """Add a child node"""
        child.parent = self
        self.children.append(child)
        return child
