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
    - PotentialPath: Foundational potentiality-certification separation
    - PotentialPathStatus: Status enum for potential paths
    - NeutralPotential: Redefined neutral element as preserved potential without certification
"""

from dal_core.foundation.rank import Rank, RankVector
from dal_core.foundation.proof_object import ProofObject, make_proof_object
from dal_core.foundation.residual_set import (
    ResidualSet,
    merge_residuals,
    discharge_residual,
    has_blocking_residuals
)
from dal_core.foundation.potential_path import (
    PotentialPath,
    PotentialPathStatus,
    certify_path,
    validate_no_direct_certificate,
    DirectCertificationError,
    make_potential_path,
    certify_potential_path,
    block_potential_path,
)
from dal_core.foundation.neutral_potential import (
    NeutralPotential,
    NeutralSyllablePotential,
    NeutralWeightPotential,
    NeutralBoundaryPotential,
    NeutralPotentialViolation,
    validate_neutral_potential,
    validate_cpb_zero_preserves_neutral,
    make_neutral_syllable_potential,
    make_neutral_weight_potential,
    make_neutral_boundary_potential,
)

__all__ = [
    "Rank",
    "RankVector",
    "ProofObject",
    "make_proof_object",
    "ResidualSet",
    "merge_residuals",
    "discharge_residual",
    "has_blocking_residuals",
    "PotentialPath",
    "PotentialPathStatus",
    "certify_path",
    "validate_no_direct_certificate",
    "DirectCertificationError",
    "make_potential_path",
    "certify_potential_path",
    "block_potential_path",
    "NeutralPotential",
    "NeutralSyllablePotential",
    "NeutralWeightPotential",
    "NeutralBoundaryPotential",
    "NeutralPotentialViolation",
    "validate_neutral_potential",
    "validate_cpb_zero_preserves_neutral",
    "make_neutral_syllable_potential",
    "make_neutral_weight_potential",
    "make_neutral_boundary_potential",
]
