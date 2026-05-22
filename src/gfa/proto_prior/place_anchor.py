"""
Place/Domain Anchoring

MANDATORY component of FirstPriorUnit.

Without place/domain anchor:
- No spatial boundary
- No origin identification
- No direction observation
- No locality principle
- No practical distinction

Place (or domain/field) is not optional - it defines WHERE the trace exists.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
from decimal import Decimal


@dataclass(frozen=True)
class PlaceAnchor:
    """
    Place or domain anchoring for FirstPriorUnit.

    This can represent:
    - Physical spatial coordinates (x, y, z)
    - Abstract domain position
    - Field/space identifier
    - Locality label

    Critical law: No FirstPriorUnit without PlaceAnchor.
    """

    # At least one must be provided
    spatial_coordinates: Optional[Tuple[Decimal, ...]] = None
    domain_position: Optional[str] = None
    field_identifier: Optional[str] = None
    locality_label: Optional[str] = None

    # Optional: spatial extent
    spatial_extent: Optional[Decimal] = None
    position_precision: Optional[str] = None

    def __post_init__(self):
        # At least one spatial/domain indicator must be present
        if not any([
            self.spatial_coordinates,
            self.domain_position,
            self.field_identifier,
            self.locality_label
        ]):
            raise ValueError(
                "PlaceAnchor requires at least one spatial/domain indicator: "
                "spatial_coordinates, domain_position, field_identifier, or locality_label"
            )

        # Validate spatial_coordinates if provided
        if self.spatial_coordinates:
            if not self.spatial_coordinates:
                raise ValueError("spatial_coordinates cannot be empty tuple")

    @property
    def is_valid(self) -> bool:
        """Check if this place anchor is valid."""
        return any([
            self.spatial_coordinates,
            self.domain_position,
            self.field_identifier,
            self.locality_label
        ])

    @property
    def dimensionality(self) -> Optional[int]:
        """Return dimensionality of spatial coordinates if available."""
        if self.spatial_coordinates:
            return len(self.spatial_coordinates)
        return None

    def __str__(self) -> str:
        if self.spatial_coordinates:
            coords = ", ".join(str(c) for c in self.spatial_coordinates)
            return f"PlaceAnchor(coords=[{coords}])"
        elif self.domain_position:
            return f"PlaceAnchor(domain={self.domain_position})"
        elif self.field_identifier:
            return f"PlaceAnchor(field={self.field_identifier})"
        else:
            return f"PlaceAnchor(locality={self.locality_label})"
