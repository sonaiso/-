"""Recall Process - Recall ≠ Original.

Memory recall always produces a trace with residuals, never the original.

Critical Law:
    الاستدعاء ليس الأصل.
    "Recall is not the original."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime
from uuid import UUID

from .memory_trace import MemoryTrace, make_memory_trace, MemoryTraceKind


class RecallResidual(Enum):
    """Residual from recall process.

    Attributes:
        TEMPORAL_DECAY: Time-based decay
        INTERFERENCE: Interference from other memories
        RECONSTRUCTION: Reconstructive recall (not verbatim)
        CONTEXT_DEPENDENT: Context-dependent retrieval
        PARTIAL: Partial recall only
        DISTORTED: Distortion during recall
    """

    TEMPORAL_DECAY = "temporal_decay"
    INTERFERENCE = "interference"
    RECONSTRUCTION = "reconstruction"
    CONTEXT_DEPENDENT = "context_dependent"
    PARTIAL = "partial_recall"
    DISTORTED = "distorted"


@dataclass(frozen=True)
class RecallResult:
    """Result of memory recall.

    Critical Laws:
        1. Recall ≠ Original (always has residual)
        2. Recall does NOT certify original
        3. Recall does NOT raise rank
        4. Source trace must be preserved
        5. Recall creates NEW trace, not original

    Attributes:
        success: Whether recall succeeded
        original_trace_id: ID of original trace
        recalled_trace: NEW trace from recall (if success)
        residuals: Residuals from recall process
        recall_timestamp: When recall occurred
        confidence: Confidence in recall (0.0-1.0)
        metadata: Additional metadata
    """

    success: bool
    original_trace_id: UUID
    recalled_trace: Optional[MemoryTrace]
    residuals: tuple[RecallResidual, ...]
    recall_timestamp: datetime
    confidence: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be in [0.0, 1.0]")

        if self.success and self.recalled_trace is None:
            raise ValueError("success=True requires recalled_trace")

        if not self.success and self.recalled_trace is not None:
            raise ValueError("success=False cannot have recalled_trace")

        # Recall MUST have residuals (recall ≠ original)
        if self.success and not self.residuals:
            raise ValueError("Successful recall must have residuals (recall ≠ original)")

    def is_original(self) -> bool:
        """Check if recall is original.

        Always returns False - recall is NEVER original.
        """
        return False

    def get_residual_count(self) -> int:
        """Get count of residuals."""
        return len(self.residuals)


@dataclass
class RecallProcess:
    """Memory recall process.

    Implements recall with mandatory residuals.

    Critical Laws:
        1. Recall creates NEW trace, not original
        2. Recall always has residuals
        3. Recall does NOT certify
        4. Recall does NOT raise rank
        5. Temporal decay affects confidence
        6. Context affects retrieval

    Attributes:
        base_decay_rate: Base decay rate (0.0-1.0)
        interference_factor: Interference factor (0.0-1.0)
        min_confidence: Minimum confidence for success (0.0-1.0)
    """

    base_decay_rate: float = 0.05
    interference_factor: float = 0.1
    min_confidence: float = 0.3

    def __post_init__(self):
        if not 0.0 <= self.base_decay_rate <= 1.0:
            raise ValueError("base_decay_rate must be in [0.0, 1.0]")
        if not 0.0 <= self.interference_factor <= 1.0:
            raise ValueError("interference_factor must be in [0.0, 1.0]")
        if not 0.0 <= self.min_confidence <= 1.0:
            raise ValueError("min_confidence must be in [0.0, 1.0]")

    def _compute_decay(
        self,
        original_trace: MemoryTrace,
        recall_time: datetime,
    ) -> float:
        """Compute temporal decay factor.

        Args:
            original_trace: Original memory trace
            recall_time: When recall occurs

        Returns:
            Decay factor (0.0-1.0)
        """
        time_diff = (recall_time - original_trace.temporal.timestamp).total_seconds()

        # Exponential decay
        decay_factor = max(0.0, 1.0 - (self.base_decay_rate * (time_diff / 3600.0)))

        return decay_factor

    def _determine_residuals(
        self,
        original_trace: MemoryTrace,
        decay_factor: float,
        interference_count: int,
    ) -> tuple[RecallResidual, ...]:
        """Determine residuals from recall.

        Args:
            original_trace: Original trace
            decay_factor: Temporal decay factor
            interference_count: Number of interfering traces

        Returns:
            Tuple of residuals
        """
        residuals = []

        # Temporal decay always present
        if decay_factor < 1.0:
            residuals.append(RecallResidual.TEMPORAL_DECAY)

        # Interference if other traces present
        if interference_count > 0:
            residuals.append(RecallResidual.INTERFERENCE)

        # Reconstruction always occurs (not verbatim)
        residuals.append(RecallResidual.RECONSTRUCTION)

        # Context-dependent retrieval
        residuals.append(RecallResidual.CONTEXT_DEPENDENT)

        # Partial if low confidence
        if decay_factor < 0.7:
            residuals.append(RecallResidual.PARTIAL)

        # Distorted if very low confidence
        if decay_factor < 0.5:
            residuals.append(RecallResidual.DISTORTED)

        return tuple(residuals)

    def recall(
        self,
        original_trace: MemoryTrace,
        interference_count: int = 0,
        recall_time: Optional[datetime] = None,
    ) -> RecallResult:
        """Recall a memory trace.

        Args:
            original_trace: Original memory trace
            interference_count: Number of interfering traces
            recall_time: When recall occurs (default: now)

        Returns:
            RecallResult with NEW trace (not original)

        Critical:
            - Recall creates NEW trace
            - Recall ≠ Original (always has residuals)
            - Confidence affected by decay and interference
        """
        if recall_time is None:
            recall_time = datetime.now()

        # Compute decay
        decay_factor = self._compute_decay(original_trace, recall_time)

        # Compute interference penalty
        interference_penalty = self.interference_factor * min(interference_count / 10.0, 1.0)

        # Compute confidence
        confidence = max(0.0, decay_factor - interference_penalty)

        # Determine residuals
        residuals = self._determine_residuals(
            original_trace, decay_factor, interference_count
        )

        # Check if recall succeeds
        success = confidence >= self.min_confidence

        # Create recalled trace (NEW trace, not original)
        recalled_trace = None
        if success:
            recalled_trace = make_memory_trace(
                kind=original_trace.kind,
                source_operation=f"recall_of_{original_trace.source_operation}",
                content=original_trace.content,  # Content recalled
                timestamp=recall_time,
                metadata={
                    "original_trace_id": str(original_trace.trace_id),
                    "recall_confidence": confidence,
                    "decay_factor": decay_factor,
                    "interference_count": interference_count,
                    "residuals": [r.value for r in residuals],
                },
            )

        return RecallResult(
            success=success,
            original_trace_id=original_trace.trace_id,
            recalled_trace=recalled_trace,
            residuals=residuals,
            recall_timestamp=recall_time,
            confidence=confidence,
            metadata={
                "decay_factor": decay_factor,
                "interference_count": interference_count,
            },
        )
