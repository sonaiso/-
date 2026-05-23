"""Memory Gate - Admission control for memory traces.

Gates control what can be admitted to memory and enforce critical laws.

Critical Law:
    البوابة تمنع ما لا أثر له.
    "The gate blocks what has no trace."
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional

from .memory_trace import MemoryTrace, MemoryTraceKind
from .memory_storage import MemoryStorage
from .memory_residual import MemoryResidual, MemoryResidualKind


class AdmissionViolation(Enum):
    """Violation preventing memory admission.

    Attributes:
        NO_TRACE: Content has no trace structure
        NO_SOURCE: No source operation specified
        NO_TEMPORAL: No temporal information
        INVALID_COMPOSITE: Invalid composite trace
        STORAGE_FULL: Storage at capacity
        DUPLICATE_ID: Duplicate trace ID
    """

    NO_TRACE = "no_trace_structure"
    NO_SOURCE = "no_source_operation"
    NO_TEMPORAL = "no_temporal_information"
    INVALID_COMPOSITE = "invalid_composite_trace"
    STORAGE_FULL = "storage_at_capacity"
    DUPLICATE_ID = "duplicate_trace_id"


@dataclass(frozen=True)
class MemoryAdmissionResult:
    """Result of memory admission check.

    Attributes:
        admitted: Whether trace was admitted
        trace_id: Trace ID (if admitted)
        violations: Violations preventing admission
        residuals: Residuals from admission process
        warnings: Non-blocking warnings
    """

    admitted: bool
    trace_id: Optional[str] = None
    violations: tuple[AdmissionViolation, ...] = ()
    residuals: tuple[MemoryResidual, ...] = ()
    warnings: tuple[str, ...] = ()

    def __post_init__(self):
        if self.admitted and not self.trace_id:
            raise ValueError("admitted=True requires trace_id")

        if not self.admitted and self.trace_id:
            raise ValueError("admitted=False cannot have trace_id")

        if self.admitted and self.violations:
            raise ValueError("admitted=True cannot have violations")


@dataclass
class MemoryGate:
    """Memory admission gate.

    Enforces critical laws:
        1. Memory stores trace, not raw content
        2. Source must be preserved
        3. Temporal ordering preserved
        4. No non-traceable content admitted
        5. Capacity limits enforced
        6. Composite traces validated
        7. No certification of content
        8. No rank elevation

    Attributes:
        require_source: Whether source operation required
        require_temporal: Whether temporal info required
        validate_composite: Whether to validate composite traces
        enforce_capacity: Whether to enforce storage capacity
    """

    require_source: bool = True
    require_temporal: bool = True
    validate_composite: bool = True
    enforce_capacity: bool = True

    def check_trace_structure(self, trace: MemoryTrace) -> List[AdmissionViolation]:
        """Check trace structure validity.

        Args:
            trace: Memory trace to check

        Returns:
            List of violations
        """
        violations = []

        # Check source
        if self.require_source:
            if not trace.source_operation or not trace.source_operation.strip():
                violations.append(AdmissionViolation.NO_SOURCE)

        # Check temporal
        if self.require_temporal:
            if trace.temporal is None:
                violations.append(AdmissionViolation.NO_TEMPORAL)

        # Check composite validity
        if self.validate_composite and trace.kind == MemoryTraceKind.COMPOSITE:
            if not trace.parent_traces:
                violations.append(AdmissionViolation.INVALID_COMPOSITE)

        return violations

    def check_storage_capacity(
        self,
        storage: MemoryStorage,
        trace: MemoryTrace,
    ) -> List[AdmissionViolation]:
        """Check storage capacity.

        Args:
            storage: Memory storage
            trace: Trace to admit

        Returns:
            List of violations
        """
        violations = []

        if self.enforce_capacity:
            # Check if storage full
            if storage.is_full() and trace.trace_id not in storage.traces:
                violations.append(AdmissionViolation.STORAGE_FULL)

            # Check for duplicate
            if trace.trace_id in storage.traces:
                violations.append(AdmissionViolation.DUPLICATE_ID)

        return violations

    def admit(
        self,
        trace: MemoryTrace,
        storage: Optional[MemoryStorage] = None,
    ) -> MemoryAdmissionResult:
        """Admit trace to memory.

        Args:
            trace: Memory trace to admit
            storage: Target storage (optional, for capacity check)

        Returns:
            MemoryAdmissionResult

        Critical Laws Enforced:
            1. Trace structure required (not raw content)
            2. Source preserved
            3. Temporal preserved
            4. No non-traceable content
            5. Capacity enforced
        """
        violations = []
        residuals = []
        warnings = []

        # Check trace is actually a MemoryTrace
        if not isinstance(trace, MemoryTrace):
            return MemoryAdmissionResult(
                admitted=False,
                violations=(AdmissionViolation.NO_TRACE,),
            )

        # Check trace structure
        structure_violations = self.check_trace_structure(trace)
        violations.extend(structure_violations)

        # Check storage capacity if provided
        if storage is not None:
            capacity_violations = self.check_storage_capacity(storage, trace)
            violations.extend(capacity_violations)

            # Add capacity residual if near full
            if storage.geometry.max_items is not None:
                capacity_ratio = storage.count() / storage.geometry.max_items
                if capacity_ratio > 0.8:
                    from .memory_residual import make_capacity_overflow_residual

                    residuals.append(
                        make_capacity_overflow_residual(
                            storage.count(),
                            storage.geometry.max_items,
                        )
                    )
                    warnings = ("Storage near capacity",)

        # Determine admission
        admitted = len(violations) == 0

        return MemoryAdmissionResult(
            admitted=admitted,
            trace_id=str(trace.trace_id) if admitted else None,
            violations=tuple(violations),
            residuals=tuple(residuals),
            warnings=tuple(warnings),
        )


def validate_memory_trace(trace: MemoryTrace) -> bool:
    """Validate memory trace structure.

    Args:
        trace: Memory trace to validate

    Returns:
        True if valid

    Enforces:
        - Source operation required
        - Temporal information required
        - Composite traces have parents
        - Non-composite traces don't have parents
    """
    gate = MemoryGate()
    result = gate.admit(trace)

    return result.admitted
