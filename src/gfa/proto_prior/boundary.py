"""
Boundary

MANDATORY component of FirstPriorUnit.

Without boundary:
- No clear extent
- No finitude
- No well-defined unit
- No composition possible

Boundary defines WHERE the unit begins and ends (spatially, temporally, or conceptually).
"""

from dataclasses import dataclass
from typing import Optional, Any, Dict


@dataclass(frozen=True)
class Boundary:
    """
    Boundary of the FirstPriorUnit.

    This defines the extent/limits of the entity/effect.

    Types of boundaries:
    - Spatial: where it ends in space
    - Temporal: when it begins/ends in time
    - Conceptual: what is included/excluded
    - Relational: what connections define its edge
    """

    # At least one boundary type must be specified
    spatial_boundary: Optional[str] = None
    temporal_boundary: Optional[str] = None
    conceptual_boundary: Optional[str] = None
    relational_boundary: Optional[str] = None

    # Optional: boundary properties
    boundary_type: Optional[str] = None  # e.g., "sharp", "fuzzy", "permeable"
    boundary_metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not any([
            self.spatial_boundary,
            self.temporal_boundary,
            self.conceptual_boundary,
            self.relational_boundary
        ]):
            raise ValueError(
                "Boundary requires at least one boundary specification. "
                "Without boundary, the unit has no defined extent."
            )

    @property
    def is_valid(self) -> bool:
        """Check if this boundary is valid."""
        return any([
            self.spatial_boundary,
            self.temporal_boundary,
            self.conceptual_boundary,
            self.relational_boundary
        ])

    @property
    def boundary_dimensions(self) -> int:
        """Count how many boundary dimensions are specified."""
        return sum([
            bool(self.spatial_boundary),
            bool(self.temporal_boundary),
            bool(self.conceptual_boundary),
            bool(self.relational_boundary)
        ])

    def __str__(self) -> str:
        bounds = []
        if self.spatial_boundary:
            bounds.append(f"spatial:{self.spatial_boundary[:20]}")
        if self.temporal_boundary:
            bounds.append(f"temporal:{self.temporal_boundary[:20]}")
        if self.conceptual_boundary:
            bounds.append(f"conceptual:{self.conceptual_boundary[:20]}")
        if self.relational_boundary:
            bounds.append(f"relational:{self.relational_boundary[:20]}")
        return f"Boundary({', '.join(bounds)})"
