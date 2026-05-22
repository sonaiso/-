"""
ProtoPrior Kernel - First Prior Minimal Sufficiency

This module implements the minimal sufficient unit for entering Prior Geometry.

FirstPriorUnit is NOT:
- A rule
- A concept
- A word/meaning
- A law

FirstPriorUnit IS:
- A distinguished existential trace
- Anchored in time, place, and reference
- Preserved and retainable
- Comparable to other units
- Primitively bindable (without producing meaning)
- Carrying residuals and rank
- Bounded by clear boundaries

Key Laws:
- No FirstPriorUnit without existence
- No FirstPriorUnit without distinction
- No FirstPriorUnit without boundary
- No FirstPriorUnit without time/place/reference anchors
- No FirstPriorUnit without retention capability
- No FirstPriorUnit without comparability
- No FirstPriorUnit without primitive bindability
- FirstPriorUnit CANNOT produce rules/meanings/judgments/certificates

This is the foundation from which physics, mathematics, logic, and language emerge.
"""

from .existence_type import ExistenceType, Domain, Channel
from .time_anchor import TimeAnchor
from .place_anchor import PlaceAnchor
from .reference_anchor import ReferenceAnchor
from .distinction import Distinction
from .boundary import Boundary
from .retention import RetentionState
from .comparability import ComparabilityState
from .primitive_bindability import PrimitiveBindability
from .first_prior_unit import FirstPriorUnit, Residual, Rank
from .proto_prior_validator import ProtoPriorValidator

__all__ = [
    "ExistenceType",
    "Domain",
    "Channel",
    "TimeAnchor",
    "PlaceAnchor",
    "ReferenceAnchor",
    "Distinction",
    "Boundary",
    "RetentionState",
    "ComparabilityState",
    "PrimitiveBindability",
    "FirstPriorUnit",
    "Residual",
    "Rank",
    "ProtoPriorValidator",
]
