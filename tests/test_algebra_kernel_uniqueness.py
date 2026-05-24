"""
Guard tests: enforce that Rank/Result/Evidence/Residual/Failure/Trace
have a single source — fvafk.algebra.

Additional guards for the C1 pre-kernel trace surface (``fvafk.c1.trace_v1``):
that module is permitted to expose a *backward-compatible alias* called
``Trace`` (pointing at :class:`C1Trace`), but it MUST NOT:

1. Redefine ``Trace`` as a new class.
2. Be re-exported from :mod:`fvafk.algebra`.
3. Lose its pre-kernel adapter documentation.
4. Lose its documented adapter path (:func:`to_algebra_trace`).

Allowed exceptions for the AST-level "no parallel kernel" check are listed
in :data:`ALLOWED_REDEFINING_PATHS`.
"""

from __future__ import annotations

import ast
import pathlib


ALLOWED_REDEFINING_PATHS = {
    "dal_core/evidence.py",
    "dal_core/pipeline.py",
    "dal_core/residuals.py",
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


# ---------------------------------------------------------------------------
# C1 pre-kernel trace surface guards
# ---------------------------------------------------------------------------


def _trace_v1_path() -> pathlib.Path:
    return (
        pathlib.Path(__file__).resolve().parent.parent
        / "src"
        / "fvafk"
        / "c1"
        / "trace_v1.py"
    )


def test_algebra_trace_is_the_constitutional_kernel():
    """fvafk.algebra.Trace is the constitutional Trace.

    It must be a real class defined inside fvafk.algebra.core, not an
    alias to anything in fvafk.c1.
    """
    from fvafk.algebra import Trace as AlgebraTrace
    from fvafk.algebra.core import Trace as AlgebraTraceCore

    assert AlgebraTrace is AlgebraTraceCore
    assert AlgebraTrace.__module__ == "fvafk.algebra.core"


def test_trace_v1_trace_is_alias_not_constitutional_origin():
    """trace_v1.Trace is an alias to C1Trace, not a parallel kernel class.

    The pre-kernel surface may keep the public name ``Trace`` only as a
    backward-compatible alias of :class:`C1Trace`. It MUST NOT be the
    same object as :class:`fvafk.algebra.Trace`.
    """
    from fvafk.algebra import Trace as AlgebraTrace
    from fvafk.c1.trace_v1 import C1Trace, Trace as C1TraceAlias

    # Alias points at C1Trace, the operational pre-kernel class.
    assert C1TraceAlias is C1Trace
    # And is distinct from the constitutional algebra Trace.
    assert C1TraceAlias is not AlgebraTrace
    assert C1Trace.__module__ == "fvafk.c1.trace_v1"


def test_trace_v1_is_not_exported_from_fvafk_algebra():
    """fvafk.algebra must not re-export the C1 trace as the kernel Trace."""
    import fvafk.algebra as algebra
    from fvafk.c1.trace_v1 import C1Trace

    # No attribute on the algebra package should be the C1 trace class.
    assert getattr(algebra, "Trace") is not C1Trace
    for name in getattr(algebra, "__all__", []):
        assert getattr(algebra, name, None) is not C1Trace, (
            f"fvafk.algebra re-exports C1Trace via '{name}'"
        )


def test_trace_v1_documents_pre_kernel_adapter_status():
    """trace_v1.py must explicitly document its pre-kernel/adapter status."""
    source = _trace_v1_path().read_text(encoding="utf-8")
    lowered = source.lower()
    assert "pre-kernel" in lowered, "trace_v1.py missing 'pre-kernel' marker"
    assert "adapter" in lowered, "trace_v1.py missing 'adapter' documentation"
    assert "algebra_kernel_constitution" in lowered, (
        "trace_v1.py must reference docs/ALGEBRA_KERNEL_CONSTITUTION.md"
    )


def test_trace_v1_provides_adapter_to_algebra_trace():
    """A documented adapter path from C1Trace to fvafk.algebra.Trace exists."""
    from fvafk.algebra import Trace as AlgebraTrace
    from fvafk.c1.trace_v1 import C1Trace, to_algebra_trace

    sample = C1Trace(inventory_id="inv-test", original_hash="hash-test")
    adapted = to_algebra_trace(sample)

    assert isinstance(adapted, AlgebraTrace)
    # Adapter preserves C1 provenance so the chain remains auditable.
    assert adapted.metadata["inventory_id"] == "inv-test"
    assert adapted.metadata["original_hash"] == "hash-test"
    assert adapted.metadata["source"] == "fvafk.c1.trace_v1"
