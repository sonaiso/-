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
in :data:`ALLOWED_REDEFINING_PATHS`. Every entry in that whitelist is
additionally required to declare itself as an adapter and to reference
``docs/KERNEL_MIGRATION_GAPS.md`` — see
``test_allowed_redefining_paths_are_documented_adapters``.

This module enforces **PR-ARCH0: Architecture Unification and Kernel
Authority Map** (see ``docs/ARCHITECTURE_AUTHORITY_MAP.md``).
"""

from __future__ import annotations

import ast
import pathlib


ALLOWED_REDEFINING_PATHS = {
    # dal_core domain structures with documented adapter notes.
    "dal_core/evidence.py",
    "dal_core/pipeline.py",
    "dal_core/residuals.py",
    # gfa domain backwards-compatibility surface.
    "gfa/proto_prior/first_prior_unit.py",
    # gfa.governance.rank: explicit migration-gap adapter (G1 in
    # docs/KERNEL_MIGRATION_GAPS.md). Re-exports a parallel ``Rank`` enum
    # pending migration to fvafk.algebra.Rank.
    "gfa/governance/rank.py",
}

# Adapter marker tokens. Any file in ALLOWED_REDEFINING_PATHS must contain
# both an explicit "adapter"/"migration" marker AND a reference to the
# kernel migration gaps document, otherwise the whitelist would be a
# silent parallel kernel.
_ADAPTER_TOKENS = ("adapter", "migration-gap", "migration gap")
_MIGRATION_DOC_TOKENS = (
    "KERNEL_MIGRATION_GAPS",
    "ARCHITECTURE_AUTHORITY_MAP",
    "ALGEBRA_KERNEL_CONSTITUTION",
)

FORBIDDEN_NAMES = {"Rank", "Result", "Evidence", "Residual", "Failure", "Trace"}


def _src_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent.parent / "src"


def test_no_parallel_kernel_definitions():
    root = _src_root()
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


def test_allowed_redefining_paths_are_documented_adapters():
    """Every whitelisted path must explicitly declare itself an adapter.

    Enforces PR-ARCH0: the ``ALLOWED_REDEFINING_PATHS`` whitelist is not a
    parallel kernel. Each listed file must contain an adapter/migration
    marker AND a reference to the migration-gaps / authority-map / kernel
    constitution document, so that any future reader can see *why* the file
    is allowed to use a kernel name.
    """
    root = _src_root()
    offenders: list[str] = []

    for rel in sorted(ALLOWED_REDEFINING_PATHS):
        path = root / rel
        if not path.exists():
            offenders.append(f"{rel}: listed in ALLOWED_REDEFINING_PATHS but file is missing")
            continue
        source = path.read_text(encoding="utf-8")
        lowered = source.lower()
        has_adapter = any(token in lowered for token in _ADAPTER_TOKENS)
        has_doc_ref = any(token in source for token in _MIGRATION_DOC_TOKENS)
        if not has_adapter:
            offenders.append(
                f"{rel}: missing adapter/migration marker "
                f"(expected one of {_ADAPTER_TOKENS!r})"
            )
        if not has_doc_ref:
            offenders.append(
                f"{rel}: missing reference to a kernel authority doc "
                f"(expected one of {_MIGRATION_DOC_TOKENS!r})"
            )

    assert not offenders, (
        "Whitelisted parallel-kernel paths must be documented as adapters:\n"
        + "\n".join(offenders)
    )


def test_architecture_authority_map_exists():
    """PR-ARCH0 authority map must be present alongside the test."""
    docs = _src_root().parent / "docs"
    authority_map = docs / "ARCHITECTURE_AUTHORITY_MAP.md"
    migration_gaps = docs / "KERNEL_MIGRATION_GAPS.md"

    assert authority_map.exists(), (
        "docs/ARCHITECTURE_AUTHORITY_MAP.md is missing — PR-ARCH0 declares it "
        "as the constitutional authority map for the repository."
    )
    assert migration_gaps.exists(), (
        "docs/KERNEL_MIGRATION_GAPS.md is missing — PR-ARCH0 requires it as "
        "the working list of legacy/adapter surfaces."
    )

    authority_text = authority_map.read_text(encoding="utf-8")
    assert "constitutional kernel" in authority_text.lower(), (
        "ARCHITECTURE_AUTHORITY_MAP.md must declare fvafk.algebra as the "
        "constitutional kernel."
    )
    assert "fvafk.algebra" in authority_text, (
        "ARCHITECTURE_AUTHORITY_MAP.md must name fvafk.algebra explicitly."
    )


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
