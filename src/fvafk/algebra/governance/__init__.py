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

G6 Compliance:

    InspectionReport is a domain value.
    Result[InspectionReport] is the constitutional judgment container.
    No parallel InspectionResult class is allowed.

Public Surface
--------------

Core types:

- :class:`InspectionArtifact` — what is being inspected
- :class:`InspectionFinding` — claim + evidence + counter_evidence
- :class:`InspectionResidual` — what was not resolved
- :class:`InspectionReport` — status + findings + replay (domain report)

Lifting functions:

- :func:`make_inspection_result` — wrap InspectionReport in Result[...]
- :func:`inspection_result_to_legacy_dict` — convert to legacy format

NO bare boolean.
NO parallel InspectionResult.
"""

from __future__ import annotations

from .inspection import (
    InspectionArtifact,
    InspectionFinding,
    InspectionResidual,
    InspectionReport,
    InspectionResidualKind,
    make_inspection_result,
    inspection_result_to_legacy_dict,
)

__all__ = [
    "InspectionArtifact",
    "InspectionFinding",
    "InspectionResidual",
    "InspectionReport",
    "InspectionResidualKind",
    "make_inspection_result",
    "inspection_result_to_legacy_dict",
]
