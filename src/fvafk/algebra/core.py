"""Core algebraic primitives for ``fvafk.algebra``.

Implements the constitution **"لا مخرج عارٍ"** (no bare output):

    Every Result = value + rank + evidence + residuals + failures + replay.

The flow encoded here is::

    Trace → Domain → Carrier → CPB → Operation → Evidence → Rank
                                                  ↓
                                              Residuals
                                                  ↓
                                              Learning

This module is intentionally dependency-light (stdlib only) so it can be
adopted across the FVAFK pipeline without widening the install graph.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, Generic, Mapping, Protocol, Sequence, Tuple, TypeVar
from uuid import uuid4

from .arabic_layers import Domain

T = TypeVar("T")


# ---------------------------------------------------------------------------
# Rank
# ---------------------------------------------------------------------------


class Rank(Enum):
    """Ordered epistemic rank of a :class:`Result`.

    The ranks form a strict total order. Higher rank claims demand
    proportionally stronger evidence and an empty residual set; see
    :func:`fvafk.algebra.policies.default_policy` for the canonical
    promotion rules.
    """

    UNRESOLVED = 0   # no claim
    CANDIDATE = 1    # claim exists but is unsupported
    LICENSED = 2     # supported by evidence, but residuals remain
    CERTIFIED = 3    # supported and residual-free
    REFUTED = -1     # actively contradicted by failures

    def __lt__(self, other: "Rank") -> bool:  # pragma: no cover - trivial
        if not isinstance(other, Rank):
            return NotImplemented
        return self.value < other.value


# ---------------------------------------------------------------------------
# Trace
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Trace:
    """Immutable provenance record.

    A trace records *which operation* produced a result, *over which
    input span*, and *from which parent traces*. Traces form a DAG that
    must be replayable.
    """

    operation: str
    source_span: Tuple[int, int] = (0, 0)
    parents: Tuple[str, ...] = ()
    trace_id: str = field(default_factory=lambda: uuid4().hex)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def child(self, operation: str, source_span: Tuple[int, int] | None = None) -> "Trace":
        """Build a child trace whose only parent is ``self``."""
        return Trace(
            operation=operation,
            source_span=source_span if source_span is not None else self.source_span,
            parents=(self.trace_id,),
        )


# ---------------------------------------------------------------------------
# Carrier
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Carrier(Generic[T]):
    """Typed substrate that an :class:`Operation` consumes or produces.

    A carrier binds a value to its :class:`Domain` so that bridges
    between domains can be type-checked by the CPB layer.
    """

    domain: Domain
    value: T
    label: str = ""


# ---------------------------------------------------------------------------
# Evidence / Residual / Failure
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Evidence:
    """Atomic supporting observation behind a claim.

    Evidence must be *scoped* (it cites a span, a rule, or a lower-layer
    result). Bare assertions without a source are not admissible.
    """

    kind: str
    source: str
    detail: str = ""
    weight: float = 1.0

    def __post_init__(self) -> None:
        if not self.kind:
            raise ValueError("Evidence.kind must be non-empty")
        if not self.source:
            raise ValueError("Evidence.source must be non-empty")
        if self.weight <= 0.0:
            raise ValueError("Evidence.weight must be strictly positive")


@dataclass(frozen=True)
class Residual:
    """Something the operation *did not* resolve.

    Residuals are the explicit reason a result is not promoted to
    :attr:`Rank.CERTIFIED`. Examples: missing context, lexical
    ambiguity, untested branch.
    """

    kind: str
    description: str

    def __post_init__(self) -> None:
        if not self.kind:
            raise ValueError("Residual.kind must be non-empty")


@dataclass(frozen=True)
class Failure:
    """Typed failure record.

    Distinct from :class:`Residual`: a failure is an *active*
    contradiction (a rule fired and rejected the carrier), whereas a
    residual is merely *unresolved*.
    """

    kind: str
    description: str
    fatal: bool = False


# ---------------------------------------------------------------------------
# Result
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Result(Generic[T]):
    """The single, governed output type of every algebraic operation.

    Embodies the constitution: ``value + rank + evidence + residuals +
    failures + replay``. Construction enforces the invariants. Use
    :meth:`with_rank` / :meth:`with_residual` / :meth:`with_failure` to
    derive new results immutably.
    """

    value: T
    rank: Rank
    evidence: Tuple[Evidence, ...] = ()
    residuals: Tuple[Residual, ...] = ()
    failures: Tuple[Failure, ...] = ()
    trace: Trace = field(default_factory=lambda: Trace(operation="root"))

    def __post_init__(self) -> None:
        # "No bare output": any rank at or above LICENSED demands evidence.
        # CANDIDATE permits an unsupported claim; REFUTED only carries
        # failures; UNRESOLVED carries nothing.
        if self.rank in (Rank.LICENSED, Rank.CERTIFIED) and not self.evidence:
            raise ValueError(
                "Result with rank >= LICENSED requires at least one Evidence "
                "(la-mukhraj-arin invariant)."
            )
        # Certification requires an empty residual set.
        if self.rank is Rank.CERTIFIED and self.residuals:
            raise ValueError(
                "Result cannot be CERTIFIED while residuals remain; "
                "demote to LICENSED or resolve the residuals first."
            )
        # A fatal failure forces REFUTED.
        if any(f.fatal for f in self.failures) and self.rank is not Rank.REFUTED:
            raise ValueError(
                "Result carries a fatal Failure but rank is not REFUTED."
            )

    # -- derivation helpers -------------------------------------------------

    def with_evidence(self, *items: Evidence) -> "Result[T]":
        """Return a copy with additional evidence appended."""
        if not items:
            return self
        return replace(self, evidence=self.evidence + tuple(items))

    def with_residual(self, *items: Residual) -> "Result[T]":
        """Return a copy with additional residuals appended."""
        if not items:
            return self
        return replace(self, residuals=self.residuals + tuple(items))

    def with_failure(self, *items: Failure) -> "Result[T]":
        """Return a copy with additional failures appended.

        If any added failure is fatal, the rank is set to
        :attr:`Rank.REFUTED` in the same transition so that the
        no-bare-output invariants remain consistent.
        """
        if not items:
            return self
        new_failures = self.failures + tuple(items)
        new_rank = (
            Rank.REFUTED if any(f.fatal for f in new_failures) else self.rank
        )
        return replace(self, failures=new_failures, rank=new_rank)

    def with_rank(self, rank: Rank) -> "Result[T]":
        """Return a copy with a new rank (re-validating the invariants)."""
        return replace(self, rank=rank)

    @property
    def certificate_allowed(self) -> bool:
        """``True`` iff this result *could* be promoted to ``CERTIFIED``.

        Requires evidence, no residuals, and no failures.
        """
        return bool(self.evidence) and not self.residuals and not self.failures

    def replay(self) -> Mapping[str, Any]:
        """Return a plain-dict replay record of this result.

        The replay is intentionally simple (JSON-friendly) so it can be
        persisted, diffed, or shipped to another process.
        """
        return {
            "value": self.value,
            "rank": self.rank.name,
            "evidence": [e.__dict__ for e in self.evidence],
            "residuals": [r.__dict__ for r in self.residuals],
            "failures": [f.__dict__ for f in self.failures],
            "trace": {
                "operation": self.trace.operation,
                "trace_id": self.trace.trace_id,
                "parents": list(self.trace.parents),
                "source_span": list(self.trace.source_span),
            },
        }


# ---------------------------------------------------------------------------
# Operation protocol
# ---------------------------------------------------------------------------


class Operation(Protocol[T]):
    """Protocol every algebraic operation must satisfy.

    Implementations are responsible for declaring the domains they
    bridge so the CPB layer can validate them statically.
    """

    source_domain: Domain
    target_domain: Domain
    name: str

    def run(self, carrier: Carrier[Any]) -> Result[T]:  # pragma: no cover
        ...


def empty_result(value: T, *, operation: str = "noop") -> Result[T]:
    """Return an ``UNRESOLVED`` result; a convenience constructor."""
    return Result(value=value, rank=Rank.UNRESOLVED, trace=Trace(operation=operation))


__all__ = [
    "Carrier",
    "Domain",
    "Evidence",
    "Failure",
    "Operation",
    "Rank",
    "Residual",
    "Result",
    "Trace",
    "empty_result",
]


# Re-export Domain (and a Sequence alias) for convenience.
_ = Sequence
