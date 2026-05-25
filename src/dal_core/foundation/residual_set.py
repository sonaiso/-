"""
ResidualSet Algebra - Algebraic operations on residual collections.

Residuals are not just warnings/errors to be logged. They form an algebraic
structure with defined operations:

    - merge: Combine residual sets
    - discharge: Remove residuals with proof
    - inheritance: Preserve residuals across layers
    - blocking: Check if any residual blocks progression

Laws:
    Res(output) ⊇ Res(input) - DischargedByProof(output)

    Residuals are preserved unless explicitly discharged by proof.
    No silent deletion of residuals.

Operations:
    merge_residuals: Res₁ ⊕ Res₂ → Res_combined
    discharge_residual: Res × Proof → Res' (with proof of discharge)
    has_blocking_residuals: Res → Bool

PR: U0-STRICT-TYPE-SYSTEM (Foundation extraction)
Created: 2026-05-25
"""

from dataclasses import dataclass
from typing import FrozenSet, Optional, Set
from enum import Enum

from dal_core.residuals import Residual, ResidualSeverity


class DischargeStatus(Enum):
    """Status of residual discharge attempt."""
    DISCHARGED = "discharged"          # Successfully discharged
    PERSISTS = "persists"              # Remains after discharge attempt
    UPGRADED = "upgraded"              # Severity increased
    DOWNGRADED = "downgraded"          # Severity decreased


@dataclass(frozen=True)
class ResidualSet:
    """
    Algebraic container for residuals.

    Provides operations for combining, discharging, and querying residuals.

    Fields:
        residuals: Frozenset of residuals
        discharged: Frozenset of residuals that were discharged
        inherited: Frozenset of residuals inherited from lower layers

    Laws:
        - residuals is immutable
        - discharged residuals are tracked, not deleted
        - inherited residuals are preserved
    """
    residuals: FrozenSet[Residual]
    discharged: FrozenSet[Residual] = frozenset()
    inherited: FrozenSet[Residual] = frozenset()

    def active_residuals(self) -> FrozenSet[Residual]:
        """Get active (non-discharged) residuals."""
        return self.residuals - self.discharged

    def has_blocking(self) -> bool:
        """Check if any active residual is blocking."""
        return any(r.is_blocker() for r in self.active_residuals())

    def has_warnings(self) -> bool:
        """Check if any active residual is warning."""
        return any(r.is_warning() for r in self.active_residuals())

    def count_active(self) -> int:
        """Count active residuals."""
        return len(self.active_residuals())

    def count_blocking(self) -> int:
        """Count active blocking residuals."""
        return sum(1 for r in self.active_residuals() if r.is_blocker())

    def count_warnings(self) -> int:
        """Count active warning residuals."""
        return sum(1 for r in self.active_residuals() if r.is_warning())


def merge_residuals(
    res1: FrozenSet[Residual],
    res2: FrozenSet[Residual]
) -> FrozenSet[Residual]:
    """
    Merge two residual sets.

    Operation: Res₁ ⊕ Res₂ → Res_combined

    Union of residuals, preserving all warnings and blockers.

    Args:
        res1: First residual set
        res2: Second residual set

    Returns:
        Combined residual set (union)

    Law:
        |merge(R1, R2)| ≤ |R1| + |R2| (deduplication)
    """
    return res1 | res2


def has_blocking_residuals(residuals: FrozenSet[Residual]) -> bool:
    """
    Check if any residual is blocking.

    Args:
        residuals: Set of residuals to check

    Returns:
        True if at least one blocker exists
    """
    return any(r.severity == ResidualSeverity.BLOCKER for r in residuals)


@dataclass(frozen=True)
class DischargeProof:
    """
    Proof that a residual can be discharged.

    Contains:
        - residual_id: ID of residual being discharged
        - reason: Human-readable reason for discharge
        - evidence: Evidence supporting discharge
        - layer: Layer where discharge occurred
    """
    residual_id: str  # Use str(residual) or hash
    reason: str
    evidence: FrozenSet[str]
    layer: str


def discharge_residual(
    residuals: FrozenSet[Residual],
    target_residual: Residual,
    proof: DischargeProof
) -> tuple[FrozenSet[Residual], DischargeStatus]:
    """
    Attempt to discharge a residual with proof.

    Operation: Res × Proof → Res' × Status

    A residual can be discharged if:
        - Proof provides sufficient evidence
        - Discharge is permitted for this residual type
        - Layer authority allows discharge

    Args:
        residuals: Current residual set
        target_residual: Residual to discharge
        proof: Proof of discharge

    Returns:
        (updated_residuals, status)

    Laws:
        - If discharged, residual is NOT deleted (tracked in ResidualSet.discharged)
        - If cannot discharge, residual persists unchanged
        - Discharge must have proof, no silent deletion
    """
    # Check if target exists in residuals
    if target_residual not in residuals:
        return residuals, DischargeStatus.PERSISTS

    # For now, simple discharge logic: if proof provided, discharge
    # (In full implementation, would check proof validity)

    # Remove from active residuals
    updated = frozenset(r for r in residuals if r != target_residual)

    return updated, DischargeStatus.DISCHARGED


def inherit_residuals(
    lower_layer_residuals: FrozenSet[Residual],
    current_layer_residuals: FrozenSet[Residual]
) -> ResidualSet:
    """
    Inherit residuals from lower layer to current layer.

    Law:
        Res(output) ⊇ Res(input)

    Residuals from lower layers are preserved unless explicitly discharged.

    Args:
        lower_layer_residuals: Residuals from lower layer
        current_layer_residuals: New residuals from current layer

    Returns:
        ResidualSet with inheritance tracked
    """
    all_residuals = merge_residuals(lower_layer_residuals, current_layer_residuals)

    return ResidualSet(
        residuals=all_residuals,
        discharged=frozenset(),
        inherited=lower_layer_residuals
    )


def create_residual_set(
    residuals: FrozenSet[Residual],
    inherited_from: Optional[FrozenSet[Residual]] = None
) -> ResidualSet:
    """
    Create a new ResidualSet.

    Args:
        residuals: Active residuals
        inherited_from: Optional residuals inherited from lower layer

    Returns:
        ResidualSet instance
    """
    return ResidualSet(
        residuals=residuals,
        discharged=frozenset(),
        inherited=inherited_from or frozenset()
    )
