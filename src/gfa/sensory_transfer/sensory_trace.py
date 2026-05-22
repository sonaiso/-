"""
Sensory Trace - The preserved record of what was actually received

CRITICAL DISTINCTION:
- SourceEffect: What we claim exists externally
- SensoryTrace: What we actually received and preserved

These are NOT the same. The trace is evidence, not reality itself.
"""

from dataclasses import dataclass
from typing import Any, Optional
from uuid import UUID, uuid4


@dataclass(frozen=True)
class SensoryTrace:
    """
    The preserved record of what was actually received through sensory transfer.

    CRITICAL LAW: SensoryTrace ≠ External Reality
    The trace is evidence pointing to reality, not reality itself.
    """

    # What was actually received/preserved
    received_content: Any

    # Trace identity
    trace_id: UUID = None

    # Trace characteristics
    trace_quality: Optional[str] = None
    trace_completeness: Optional[str] = None  # e.g., "complete", "partial", "fragmentary"

    # Preservation details
    preservation_medium: Optional[str] = None  # e.g., "memory", "recording", "data_file"
    preservation_fidelity: Optional[str] = None

    def __post_init__(self):
        # Generate trace_id if not provided
        if self.trace_id is None:
            object.__setattr__(self, 'trace_id', uuid4())

        if self.received_content is None:
            raise ValueError("SensoryTrace requires received_content")

    @property
    def is_partial(self) -> bool:
        """Check if trace is incomplete."""
        return self.trace_completeness in {"partial", "fragmentary", "incomplete"}

    def __str__(self) -> str:
        return f"SensoryTrace(id={str(self.trace_id)[:8]}..., quality={self.trace_quality})"
