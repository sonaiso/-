"""
Reference Anchoring

MANDATORY component of FirstPriorUnit.

Without reference anchor:
- We don't know what the trace refers to
- No identity tracking
- No comparison basis
- No linking capability

Reference is not optional - it defines WHAT or WHO the trace is about.
"""

from dataclasses import dataclass
from typing import Optional, Any
from uuid import UUID, uuid4


@dataclass(frozen=True)
class ReferenceAnchor:
    """
    Reference anchoring for FirstPriorUnit.

    This can represent:
    - Entity identifier (what this trace is about)
    - Effect identifier (what phenomenon this trace records)
    - Relation identifier (what connection this trace captures)
    - Process identifier (what process this trace tracks)

    Critical law: No FirstPriorUnit without ReferenceAnchor.
    """

    # At least one must be provided
    entity_id: Optional[str] = None
    effect_id: Optional[str] = None
    relation_id: Optional[str] = None
    process_id: Optional[str] = None

    # Optional: additional reference metadata
    reference_label: Optional[str] = None
    reference_type: Optional[str] = None
    reference_description: Optional[str] = None

    # Auto-generated unique reference ID
    unique_ref_id: UUID = None

    def __post_init__(self):
        # Generate unique_ref_id if not provided
        if self.unique_ref_id is None:
            # Use object.__setattr__ for frozen dataclass
            object.__setattr__(self, 'unique_ref_id', uuid4())

        # At least one reference indicator must be present
        if not any([
            self.entity_id,
            self.effect_id,
            self.relation_id,
            self.process_id,
            self.reference_label
        ]):
            raise ValueError(
                "ReferenceAnchor requires at least one reference indicator: "
                "entity_id, effect_id, relation_id, process_id, or reference_label"
            )

    @property
    def is_valid(self) -> bool:
        """Check if this reference anchor is valid."""
        return any([
            self.entity_id,
            self.effect_id,
            self.relation_id,
            self.process_id,
            self.reference_label
        ]) and self.unique_ref_id is not None

    @property
    def primary_reference(self) -> str:
        """Return the primary reference identifier."""
        if self.entity_id:
            return self.entity_id
        elif self.effect_id:
            return self.effect_id
        elif self.relation_id:
            return self.relation_id
        elif self.process_id:
            return self.process_id
        elif self.reference_label:
            return self.reference_label
        else:
            return str(self.unique_ref_id)

    def __str__(self) -> str:
        return f"ReferenceAnchor({self.primary_reference})"
