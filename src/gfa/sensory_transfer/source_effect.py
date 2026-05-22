"""
Source Effect - What exists/happens in reality that produces a sensory transfer

CRITICAL: SourceEffect represents the claimed external reality,
NOT the sensory trace itself.

The distinction is essential:
- SourceEffect: What we claim exists externally
- SensoryTrace: What we actually received through the channel

These are NOT the same. The channel introduces limitations, noise, and transformation.
"""

from dataclasses import dataclass
from typing import Any, Optional
from gfa.proto_prior.existence_type import ExistenceType


@dataclass(frozen=True)
class SourceEffect:
    """
    A claimed source effect in reality that produces sensory transfer.

    CRITICAL LAW: SourceEffect represents a CLAIM, not certainty.
    The sensory transfer does not prove the source exists as claimed.
    """

    # What we claim exists/happens
    claimed_entity_or_effect: Any
    claimed_existence_type: ExistenceType

    # Source characteristics (if known/claimed)
    claimed_location: Optional[str] = None
    claimed_time: Optional[str] = None
    claimed_properties: Optional[str] = None

    # Confidence in source claim (CANNOT be CERTIFIED from sensory alone)
    source_confidence: Optional[str] = None  # e.g., "hypothetical", "inferred", "unknown"

    def __post_init__(self):
        if self.claimed_entity_or_effect is None:
            raise ValueError("SourceEffect requires claimed_entity_or_effect")
        if not isinstance(self.claimed_existence_type, ExistenceType):
            raise ValueError("SourceEffect requires valid ExistenceType")

    @property
    def is_hypothetical_source(self) -> bool:
        """Check if source is hypothetical/inferred rather than directly observed."""
        return self.source_confidence in {"hypothetical", "inferred", "unknown", None}

    def __str__(self) -> str:
        return f"SourceEffect(claimed={self.claimed_entity_or_effect}, type={self.claimed_existence_type.name})"
