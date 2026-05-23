"""
General Foundational Algebra (GFA)

This package implements the foundational components required for General Algebra,
starting from the minimal sufficient unit (FirstPriorUnit) that serves as the
foundation for all knowledge systems.

Key Principles:
- No CPB as axiom (CPB is a learned theorem: μΦ)
- Every prior must trace to ExistentialTrace
- No rule without binding history
- No rank promotion without audit
- **Honest status declaration** (governance module)

Architecture:
- governance: Status gate and false claim prevention ← **NEW**
- proto_prior: Minimal sufficient unit for first prior geometry
- methods: Specialized GFA methods (PROVISIONAL_SPECIALIZED status)
- (future) primitive_binding: Experimental binding that may fail
- (future) prior_geometry: Stabilized trace memory
- (future) learning: Binding condition extraction (Φ function)
- (future) cpb: Stable binding policy extraction (μΦ)
- (future) algebra: Layer algebra generation

Current Status:
    GFA Methods: PROVISIONAL_SPECIALIZED
    General Algebra Runtime: ~2% (specification only)
    CPB Extraction: Not implemented
    See docs/GENERAL_ALGEBRA_STATUS.md for details
"""

__version__ = "0.1.0"

# Expose governance for status checking
from .governance import (
    AlgebraStatus,
    ComponentStatus,
    get_project_status,
    validate_project_status,
)

__all__ = [
    "AlgebraStatus",
    "ComponentStatus",
    "get_project_status",
    "validate_project_status",
]
