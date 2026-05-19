"""
Context Contract (عقد السياق)

Contract 4: Context enrichment for operative units
Tracks position, gates (entry/judgment), and wasl/waqf context.
"""

from dataclasses import dataclass
from typing import Optional

from dal_core.units import OperativeUnit


@dataclass
class UnitContext:
    """
    سياق الوحدة (Unit Context)

    Enriches operative units with positional and contextual information.
    """
    unit: OperativeUnit
    prev_unit: Optional[OperativeUnit] = None
    next_unit: Optional[OperativeUnit] = None
    is_entry_gate: bool = False     # First in sequence
    is_judgment_gate: bool = False  # Last in sequence
    is_wasl: bool = False           # وصل context
    is_waqf: bool = False           # وقف context

    def __str__(self) -> str:
        gates = []
        if self.is_entry_gate:
            gates.append("entry")
        if self.is_judgment_gate:
            gates.append("judgment")
        gate_str = f" [{','.join(gates)}]" if gates else ""
        return f"Context({self.unit}{gate_str})"
