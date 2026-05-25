"""
Shared algebraic foundations for carrier layers.

This module contains the fundamental algebraic structures used across
all carrier layers (U₀, U₁, U₂, ...).

Exports:
    - Rank: Epistemic rank lattice (shared across all layers)
    - ProofObject: Layer-agnostic proof structure
    - ResidualSet: Residual algebra with merge/discharge operations
    - CPBContract: Identity guardian contract interface
    - LayerObject: Base protocol for layer outputs
"""

from dal_core.foundation.rank import Rank, RankVector
from dal_core.foundation.proof_object import ProofObject, make_proof_object
from dal_core.foundation.residual_set import (
    ResidualSet,
    merge_residuals,
    discharge_residual,
    has_blocking_residuals
)

__all__ = [
    "Rank",
    "RankVector",
    "ProofObject",
    "make_proof_object",
    "ResidualSet",
    "merge_residuals",
    "discharge_residual",
    "has_blocking_residuals"
]
