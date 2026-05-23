"""Memory Geometry - Foundation Kernel for General Algebra.

Memory Geometry defines how traces are stored, recalled, and decay over time.

Core Principle:
    الذاكرة تحفظ الأثر لا المحتوى الخام.
    "Memory preserves trace, not raw content."

Critical Laws:
    1. Memory stores trace, not raw content
    2. Recall ≠ Original (always carries residual)
    3. Memory does NOT certify
    4. Memory does NOT raise rank
    5. Decay is mandatory residual
    6. Source trace preserved
    7. Temporal ordering preserved
    8. Memory gate blocks non-traceable
"""

from .memory_trace import (
    MemoryTrace,
    MemoryTraceKind,
    TemporalPosition,
    make_memory_trace,
)

from .memory_storage import (
    MemoryStorage,
    StorageCapacity,
    StorageGeometry,
    SENSORY_STORAGE,
    SHORT_TERM_STORAGE,
    WORKING_STORAGE,
    LONG_TERM_STORAGE,
)

from .recall_process import (
    RecallProcess,
    RecallResult,
    RecallResidual,
)

from .memory_residual import (
    MemoryResidualKind,
    MemoryResidual,
    DecayFunction,
    exponential_decay,
    power_law_decay,
    linear_decay,
    make_decay_residual,
    make_distortion_residual,
    make_interference_residual,
    make_capacity_overflow_residual,
)

from .memory_gate import (
    MemoryGate,
    MemoryAdmissionResult,
    AdmissionViolation,
    validate_memory_trace,
)

__all__ = [
    # Memory Trace
    "MemoryTrace",
    "MemoryTraceKind",
    "TemporalPosition",
    "make_memory_trace",

    # Storage
    "MemoryStorage",
    "StorageCapacity",
    "StorageGeometry",
    "SENSORY_STORAGE",
    "SHORT_TERM_STORAGE",
    "WORKING_STORAGE",
    "LONG_TERM_STORAGE",

    # Recall
    "RecallProcess",
    "RecallResult",
    "RecallResidual",

    # Residuals
    "MemoryResidualKind",
    "MemoryResidual",
    "DecayFunction",
    "exponential_decay",
    "power_law_decay",
    "linear_decay",
    "make_decay_residual",
    "make_distortion_residual",
    "make_interference_residual",
    "make_capacity_overflow_residual",

    # Gate
    "MemoryGate",
    "MemoryAdmissionResult",
    "AdmissionViolation",
    "validate_memory_trace",
]
