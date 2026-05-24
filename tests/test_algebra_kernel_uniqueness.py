"""
Guard test: enforce that Rank/Result/Evidence/Residual/Failure/Trace
have a single source — fvafk.algebra.

Allowed exceptions: explicit adapter modules listed below.
"""

from __future__ import annotations

import ast
import pathlib


ALLOWED_REDEFINING_PATHS = {
    "dal_core/evidence.py",
    "dal_core/pipeline.py",
    "dal_core/residuals.py",
    "fvafk/c1/trace_v1.py",
    "gfa/proto_prior/first_prior_unit.py",
}

FORBIDDEN_NAMES = {"Rank", "Result", "Evidence", "Residual", "Failure", "Trace"}


def test_no_parallel_kernel_definitions():
    root = pathlib.Path(__file__).resolve().parent.parent / "src"
    offenders = []

    for py in root.rglob("*.py"):
        rel = str(py.relative_to(root))
        if rel.startswith("fvafk/algebra/"):
            continue
        if rel in ALLOWED_REDEFINING_PATHS:
            continue
        if "vendor/" in rel:
            continue
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name in FORBIDDEN_NAMES:
                offenders.append(f"{rel}: redefines {node.name}")

    assert not offenders, "Parallel kernel definitions found:\n" + "\n".join(offenders)
