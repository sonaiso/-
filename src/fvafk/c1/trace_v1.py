"""
C1 Pre-Kernel Trace Surface (Plan-aligned, lightweight).

This module provides an **operational** trace surface used by C1 gates and
``FormStream`` replay. It is intentionally separate from — and subordinate to —
the constitutional algebra kernel defined in :mod:`fvafk.algebra`.

Two kinds of trace exist in the project, and they MUST NOT be conflated:

* **Operational C1 trace** (this module — :class:`C1Trace`):
  records gate-by-gate transformations over a :class:`FormStream`, with
  before/after hashes for deterministic replay at the C1 boundary.

* **Constitutional algebra trace** (:class:`fvafk.algebra.Trace`):
  immutable provenance record attached to :class:`Result` /
  :class:`Evidence` in the general algebra. It is the *only* trace that
  carries constitutional weight (rank, evidence, residuals, replay).

Design rules (see ``docs/ALGEBRA_KERNEL_CONSTITUTION.md``):

1. :class:`C1Trace` is NOT a constitutional trace; it is a pre-kernel
   operational surface kept for C1 compatibility.
2. The name :data:`Trace` is exposed here only as a **backward-compatible
   alias** for :class:`C1Trace`. New code should prefer :class:`C1Trace`.
3. Crossing into the algebra kernel happens through the explicit
   :func:`to_algebra_trace` adapter; this module never re-imports
   ``fvafk.algebra`` at module scope, so C1 remains usable standalone.
4. No ``Rank``, ``Result``, ``Evidence``, ``Residual`` or ``Failure``
   types may be (re-)defined in this file — those live in
   :mod:`fvafk.algebra` only.

Pre-kernel adapter status: this module is a documented adapter surface.
It MUST NOT grow into a parallel kernel. See
``tests/test_algebra_kernel_uniqueness.py`` for the enforced guards.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Dict, Iterable, List, Optional, Protocol, Sequence, Tuple

from .form_codec_v2 import FormCodecV2, FormStream, GraphemeToken, stable_hash

if TYPE_CHECKING:  # pragma: no cover - typing only, keeps C1 standalone at runtime
    from fvafk.algebra import Trace as AlgebraTrace


class GateFn(Protocol):
    def __call__(self, stream: FormStream, *, rule_id: Optional[str] = None) -> FormStream: ...


@dataclass(frozen=True)
class TokenDiff:
    """
    A stable-ish token diff for trace/debugging.

    We describe changes at the *token text* level. This is intentionally simple:
    later versions can add minimal edit paths or richer diffs.
    """

    op: str  # "equal" | "replace" | "insert" | "delete"
    a_range: Tuple[int, int]
    b_range: Tuple[int, int]
    a_text: Tuple[str, ...]
    b_text: Tuple[str, ...]


def _token_texts(tokens: Sequence[GraphemeToken]) -> List[str]:
    return [t.to_text() for t in tokens]


def diff_tokens(a: FormStream, b: FormStream) -> List[TokenDiff]:
    """
    Token-level diff using SequenceMatcher over token texts.
    """
    from difflib import SequenceMatcher

    a_txt = _token_texts(a.tokens)
    b_txt = _token_texts(b.tokens)
    sm = SequenceMatcher(a=a_txt, b=b_txt)
    out: List[TokenDiff] = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        out.append(
            TokenDiff(
                op=tag,
                a_range=(i1, i2),
                b_range=(j1, j2),
                a_text=tuple(a_txt[i1:i2]),
                b_text=tuple(b_txt[j1:j2]),
            )
        )
    return out


@dataclass(frozen=True)
class C1TraceStep:
    """Operational record of a single gate application within C1.

    This is **not** a constitutional algebra step; it carries no rank or
    evidence. It is consumed only by :func:`replay` to reproduce a
    :class:`FormStream` transformation deterministically.
    """

    gate_id: str
    rule_id: Optional[str]
    before_hash: str
    after_hash: str
    diff: Tuple[TokenDiff, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class C1Trace:
    """A lightweight operational trace over C1 ``FormStream`` gates.

    Important: a :class:`C1Trace` does not by itself reproduce the final
    form — replay requires the same deterministic gates (provided via a
    registry). To lift a :class:`C1Trace` into the constitutional kernel
    use :func:`to_algebra_trace`.

    This class is intentionally separate from :class:`fvafk.algebra.Trace`:
    the algebra trace is the only constitutional provenance record.
    """

    inventory_id: str
    original_hash: str
    steps: Tuple[C1TraceStep, ...] = field(default_factory=tuple)

    def append(self, step: C1TraceStep) -> "C1Trace":
        return C1Trace(self.inventory_id, self.original_hash, self.steps + (step,))


# Backward-compatible aliases. New code should use C1Trace / C1TraceStep.
# These aliases exist ONLY for legacy C1 callers and MUST NOT be treated as
# constitutional. See docs/ALGEBRA_KERNEL_CONSTITUTION.md and
# tests/test_algebra_kernel_uniqueness.py.
TraceStep = C1TraceStep
Trace = C1Trace


def hash_stream(stream: FormStream) -> str:
    """
    Hash identity for a FormStream based on exact decoded text (NFC).
    """
    return stable_hash(stream.decode())


def apply_gate_with_trace(
    stream: FormStream,
    trace: C1Trace,
    *,
    gate_id: str,
    gate: GateFn,
    rule_id: Optional[str] = None,
) -> Tuple[FormStream, C1Trace]:
    before_hash = hash_stream(stream)
    out = gate(stream, rule_id=rule_id)
    after_hash = hash_stream(out)
    step = C1TraceStep(
        gate_id=gate_id,
        rule_id=rule_id,
        before_hash=before_hash,
        after_hash=after_hash,
        diff=tuple(diff_tokens(stream, out)),
    )
    return out, trace.append(step)


def replay(
    original: FormStream,
    trace: C1Trace,
    *,
    registry: Dict[str, GateFn],
) -> FormStream:
    """
    Replay a trace from an original `FormStream` given a registry of deterministic gates.

    This verifies hash chaining and re-applies gates in order.
    """
    if trace.original_hash != hash_stream(original):
        raise ValueError("Trace replay error: original_hash does not match provided stream.")

    current = original
    for step in trace.steps:
        if step.gate_id not in registry:
            raise KeyError(f"Missing gate in registry: {step.gate_id}")
        if hash_stream(current) != step.before_hash:
            raise ValueError(f"Trace replay error: before_hash mismatch at gate {step.gate_id}")
        current = registry[step.gate_id](current, rule_id=step.rule_id)
        if hash_stream(current) != step.after_hash:
            raise ValueError(f"Trace replay error: after_hash mismatch at gate {step.gate_id}")
    return current


def new_trace(stream: FormStream) -> C1Trace:
    return C1Trace(inventory_id=stream.inventory_id, original_hash=hash_stream(stream))


def encode_with_trace(codec: FormCodecV2, text: str) -> Tuple[FormStream, C1Trace]:
    fs = codec.encode(text)
    return fs, new_trace(fs)


# ---------------------------------------------------------------------------
# Adapter to the constitutional algebra kernel
# ---------------------------------------------------------------------------


def to_algebra_trace(trace: C1Trace) -> "AlgebraTrace":
    """Adapt a pre-kernel :class:`C1Trace` into a constitutional
    :class:`fvafk.algebra.Trace`.

    This is the **only** sanctioned crossing from the C1 operational trace
    surface into the algebra kernel. The adapter:

    * preserves ``inventory_id`` and ``original_hash`` in the algebra
      trace's metadata,
    * records gate ids and step before/after hashes in metadata so the
      C1 chain remains auditable from inside the kernel,
    * does NOT promote rank, evidence, or residuals — those must be
      attached separately via the algebra :class:`Result` API.

    The import is performed lazily so this module stays usable without
    pulling in ``fvafk.algebra`` (Phase-0 standalone constraint).
    """
    # Lazy import: keeps C1 standalone at module load time.
    from fvafk.algebra import Trace as AlgebraTrace

    metadata = {
        "source": "fvafk.c1.trace_v1",
        "inventory_id": trace.inventory_id,
        "original_hash": trace.original_hash,
        "gate_ids": tuple(step.gate_id for step in trace.steps),
        "step_hashes": tuple(
            (step.before_hash, step.after_hash) for step in trace.steps
        ),
    }
    return AlgebraTrace(
        operation="c1.trace_v1.replay",
        source_span=(0, 0),
        parents=(),
        metadata=metadata,
    )
