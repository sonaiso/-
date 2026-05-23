"""GFA Foundations - Core geometric kernels for General Algebra.

Foundation kernels implement the basic geometric structures
required for General Algebra.

Layers:
    - Memory Geometry (PR-G1)
    - Comparison Geometry (PR-G2)
    - Identity Geometry (PR-G3)
    - Binding Core (PR-G4)
"""

from .memory import (
    # Memory Trace
    MemoryTrace,
    MemoryTraceKind,
    TemporalPosition,
    make_memory_trace,

    # Storage
    MemoryStorage,
    StorageCapacity,
    StorageGeometry,
    SENSORY_STORAGE,
    SHORT_TERM_STORAGE,
    WORKING_STORAGE,
    LONG_TERM_STORAGE,

    # Recall
    RecallProcess,
    RecallResult,
    RecallResidual,

    # Residuals
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

    # Gate
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
