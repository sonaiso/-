"""``fvafk.algebra.governance`` — Governed Inspection Algebra.

Constitutional Law:

    لا فحص بلا أثر.
    لا أثر بلا معيار.
    لا معيار بلا ربط.
    لا ربط بلا نتيجة مرشحة.
    لا نتيجة بلا رتبة.
    لا رتبة بلا بقايا.
    لا حكم فحص بلا replay.

Critical Principle:

    Verification is itself a cognitive operation.

    Just as linguistic processing follows the rational method:
        artifact → prior → binding → conception → judgment

    So must code inspection follow the same method:
        artifact → evidence → finding → rank → residuals → trace

This prevents the project from being hypocritical — enforcing constitutional
laws it does not follow.

Public Surface
--------------

Core types:

- :class:`InspectionArtifact` — what is being inspected
- :class:`InspectionFinding` — claim + evidence + counter_evidence
- :class:`InspectionResidual` — what was not resolved
- :class:`InspectionResult` — status + findings + rank + residuals + replay

NO bare boolean.
"""

from __future__ import annotations

from .inspection import (
    InspectionArtifact,
    InspectionFinding,
    InspectionResidual,
    InspectionResult,
    InspectionResidualKind,
)

__all__ = [
    "InspectionArtifact",
    "InspectionFinding",
    "InspectionResidual",
    "InspectionResult",
    "InspectionResidualKind",
]
