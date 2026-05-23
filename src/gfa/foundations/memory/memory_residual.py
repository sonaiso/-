"""Memory Residuals - Decay and distortion over time.

Defines residual types and decay functions for memory.

Critical Law:
    الاضمحلال إلزامي.
    "Decay is mandatory."
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional
import math


class MemoryResidualKind(Enum):
    """Kind of memory residual.

    Attributes:
        TEMPORAL_DECAY: Time-based decay
        CAPACITY_OVERFLOW: Storage capacity exceeded
        INTERFERENCE: Interference from competing memories
        RECONSTRUCTION_ARTIFACT: Artifact from reconstruction
        CONTEXT_LOSS: Loss of original context
        PARTIAL_RETRIEVAL: Only partial information retrieved
        DISTORTION: Content distortion
        SOURCE_UNCERTAINTY: Uncertainty about source
    """

    TEMPORAL_DECAY = "temporal_decay"
    CAPACITY_OVERFLOW = "capacity_overflow"
    INTERFERENCE = "interference"
    RECONSTRUCTION_ARTIFACT = "reconstruction_artifact"
    CONTEXT_LOSS = "context_loss"
    PARTIAL_RETRIEVAL = "partial_retrieval"
    DISTORTION = "distortion"
    SOURCE_UNCERTAINTY = "source_uncertainty"


@dataclass(frozen=True)
class MemoryResidual:
    """Memory residual descriptor.

    Attributes:
        kind: Kind of residual
        description: Human-readable description
        severity: Severity (0.0-1.0, where 1.0 is complete loss)
        blocker: Whether this residual blocks usage
        affected_properties: Which properties are affected
    """

    kind: MemoryResidualKind
    description: str
    severity: float
    blocker: bool = False
    affected_properties: tuple[str, ...] = ()

    def __post_init__(self):
        if not 0.0 <= self.severity <= 1.0:
            raise ValueError("severity must be in [0.0, 1.0]")


# Decay function type
DecayFunction = Callable[[float], float]


def exponential_decay(half_life: float = 3600.0) -> DecayFunction:
    """Create exponential decay function.

    Args:
        half_life: Half-life in seconds

    Returns:
        Decay function: time_elapsed -> retention_factor
    """

    def decay(time_elapsed: float) -> float:
        """Compute retention factor.

        Args:
            time_elapsed: Time elapsed in seconds

        Returns:
            Retention factor (0.0-1.0)
        """
        if time_elapsed < 0:
            raise ValueError("time_elapsed must be non-negative")

        return math.exp(-math.log(2) * time_elapsed / half_life)

    return decay


def power_law_decay(exponent: float = 0.5) -> DecayFunction:
    """Create power-law decay function.

    Args:
        exponent: Decay exponent

    Returns:
        Decay function: time_elapsed -> retention_factor
    """

    def decay(time_elapsed: float) -> float:
        """Compute retention factor.

        Args:
            time_elapsed: Time elapsed in seconds

        Returns:
            Retention factor (0.0-1.0)
        """
        if time_elapsed < 0:
            raise ValueError("time_elapsed must be non-negative")

        # Power law: retention = 1 / (1 + time)^exponent
        return 1.0 / ((1.0 + time_elapsed / 3600.0) ** exponent)

    return decay


def linear_decay(rate: float = 0.01) -> DecayFunction:
    """Create linear decay function.

    Args:
        rate: Decay rate per hour

    Returns:
        Decay function: time_elapsed -> retention_factor
    """

    def decay(time_elapsed: float) -> float:
        """Compute retention factor.

        Args:
            time_elapsed: Time elapsed in seconds

        Returns:
            Retention factor (0.0-1.0)
        """
        if time_elapsed < 0:
            raise ValueError("time_elapsed must be non-negative")

        return max(0.0, 1.0 - rate * (time_elapsed / 3600.0))

    return decay


def make_decay_residual(
    time_elapsed: float,
    decay_fn: Optional[DecayFunction] = None,
) -> MemoryResidual:
    """Create temporal decay residual.

    Args:
        time_elapsed: Time elapsed in seconds
        decay_fn: Decay function (default: exponential)

    Returns:
        MemoryResidual for temporal decay
    """
    if decay_fn is None:
        decay_fn = exponential_decay()

    retention = decay_fn(time_elapsed)
    severity = 1.0 - retention

    return MemoryResidual(
        kind=MemoryResidualKind.TEMPORAL_DECAY,
        description=(
            f"Temporal decay: {time_elapsed:.1f}s elapsed, "
            f"retention {retention:.2%}, severity {severity:.2%}"
        ),
        severity=severity,
        blocker=(severity > 0.9),  # Block if >90% decay
        affected_properties=("content", "confidence"),
    )


def make_distortion_residual(
    distortion_level: float,
    source: str = "unknown",
) -> MemoryResidual:
    """Create distortion residual.

    Args:
        distortion_level: Distortion level (0.0-1.0)
        source: Source of distortion

    Returns:
        MemoryResidual for distortion
    """
    if not 0.0 <= distortion_level <= 1.0:
        raise ValueError("distortion_level must be in [0.0, 1.0]")

    return MemoryResidual(
        kind=MemoryResidualKind.DISTORTION,
        description=(
            f"Distortion from {source}: level {distortion_level:.2%}"
        ),
        severity=distortion_level,
        blocker=(distortion_level > 0.8),  # Block if >80% distorted
        affected_properties=("content", "accuracy"),
    )


def make_interference_residual(
    interference_count: int,
    interference_factor: float = 0.1,
) -> MemoryResidual:
    """Create interference residual.

    Args:
        interference_count: Number of interfering traces
        interference_factor: Interference factor per trace

    Returns:
        MemoryResidual for interference
    """
    severity = min(1.0, interference_count * interference_factor)

    return MemoryResidual(
        kind=MemoryResidualKind.INTERFERENCE,
        description=(
            f"Interference from {interference_count} traces, "
            f"severity {severity:.2%}"
        ),
        severity=severity,
        blocker=False,
        affected_properties=("retrieval", "confidence"),
    )


def make_capacity_overflow_residual(
    current_count: int,
    max_capacity: int,
) -> MemoryResidual:
    """Create capacity overflow residual.

    Args:
        current_count: Current item count
        max_capacity: Maximum capacity

    Returns:
        MemoryResidual for capacity overflow
    """
    overflow = max(0, current_count - max_capacity)
    severity = min(1.0, overflow / max_capacity)

    return MemoryResidual(
        kind=MemoryResidualKind.CAPACITY_OVERFLOW,
        description=(
            f"Capacity overflow: {current_count}/{max_capacity} items, "
            f"overflow {overflow}"
        ),
        severity=severity,
        blocker=(overflow > 0),  # Block if capacity exceeded
        affected_properties=("storage", "admission"),
    )
