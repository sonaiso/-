"""
Primitive Bindability

MANDATORY component of FirstPriorUnit.

Without primitive bindability:
- No connections can be attempted
- No relations can be explored
- No binding history can form
- No CPB can eventually be learned

Primitive bindability defines WHETHER this unit can participate in binding attempts.

CRITICAL: Primitive bindability does NOT produce meaning or judgment.
It only enables experimental binding that may succeed or fail.
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Set


class BindabilityLevel(Enum):
    """Level of primitive bindability."""
    NONE = auto()               # Cannot participate in binding
    RESTRICTED = auto()         # Can bind only under strict conditions
    CONDITIONAL = auto()        # Can bind with conditions
    GENERAL = auto()            # Can generally participate in binding


class BindingConstraint(Enum):
    """Types of binding constraints."""
    TEMPORAL_PROXIMITY = auto()     # Must be close in time
    SPATIAL_PROXIMITY = auto()      # Must be close in space
    SAME_DOMAIN = auto()            # Must be in same domain
    SAME_EXISTENCE_TYPE = auto()    # Must have same existence type
    EXPLICIT_PERMISSION = auto()    # Requires explicit permission
    REFERENCE_COMPATIBILITY = auto() # References must be compatible


@dataclass(frozen=True)
class PrimitiveBindability:
    """
    Primitive bindability for FirstPriorUnit.

    This defines whether and under what constraints this unit can participate
    in primitive binding attempts.

    Critical laws:
    - Primitive binding does NOT produce meaning
    - Primitive binding does NOT issue judgment
    - Primitive binding may fail
    - Primitive binding preserves failure history
    """

    bindability_level: BindabilityLevel

    # Optional: binding constraints
    required_constraints: Optional[Set[BindingConstraint]] = None
    forbidden_bindings: Optional[Set[str]] = None

    # Optional: bindability metadata
    bindability_description: Optional[str] = None

    def __post_init__(self):
        if self.bindability_level == BindabilityLevel.NONE:
            raise ValueError(
                "FirstPriorUnit requires primitive bindability. "
                "BindabilityLevel.NONE is not allowed for prior formation."
            )

        # Convert sets to frozensets for immutability
        if self.required_constraints and not isinstance(self.required_constraints, frozenset):
            object.__setattr__(
                self,
                'required_constraints',
                frozenset(self.required_constraints)
            )

        if self.forbidden_bindings and not isinstance(self.forbidden_bindings, frozenset):
            object.__setattr__(
                self,
                'forbidden_bindings',
                frozenset(self.forbidden_bindings)
            )

    @property
    def is_bindable(self) -> bool:
        """Check if this unit can participate in primitive binding."""
        return self.bindability_level != BindabilityLevel.NONE

    @property
    def is_unrestricted(self) -> bool:
        """Check if binding is unrestricted (no required constraints)."""
        return (
            self.bindability_level == BindabilityLevel.GENERAL and
            not self.required_constraints
        )

    def requires_constraint(self, constraint: BindingConstraint) -> bool:
        """Check if specific constraint is required."""
        if not self.required_constraints:
            return False
        return constraint in self.required_constraints

    def is_binding_forbidden(self, binding_type: str) -> bool:
        """Check if specific binding type is forbidden."""
        if not self.forbidden_bindings:
            return False
        return binding_type in self.forbidden_bindings

    def __str__(self) -> str:
        if self.required_constraints:
            constraints = ", ".join(c.name for c in sorted(self.required_constraints, key=lambda x: x.name)[:2])
            return f"PrimitiveBindability({self.bindability_level.name}, constraints={constraints}...)"
        return f"PrimitiveBindability({self.bindability_level.name})"
