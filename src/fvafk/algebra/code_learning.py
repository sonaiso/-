"""Algebraic trace for learning from code edits.

Treats a code edit as an operation in the algebra: each change yields a
:class:`Result` whose evidence is the set of *passing* facts (tests,
type-checks, proofs) and whose residuals are the *missing* facts
(untested branches, missing docs, missing proofs).

The same constitution applies:

- a refactor cannot be promoted to :attr:`Rank.CERTIFIED` while any
  residual (e.g. an untested branch) remains;
- a regression manifests as a fatal :class:`Failure`, which forces
  :attr:`Rank.REFUTED`;
- every :class:`CodeLearningTrace` is replay-able as a plain dict.

This module is the Phase-6 seed (*"تعلم الكود جبرياً"*); it deliberately
stays small and dependency-free.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

from .core import Evidence, Failure, Rank, Residual, Result, Trace
from .policies import apply_policy, default_policy


@dataclass(frozen=True)
class CodeChange:
    """A single before/after pair for a unit of code."""

    path: str
    before: str
    after: str

    def __post_init__(self) -> None:
        if not self.path:
            raise ValueError("CodeChange.path must be non-empty")


@dataclass(frozen=True)
class CodeLearningTrace:
    """Algebraic record of a code-edit operation.

    Attributes:
        change: The before/after code pair.
        evidence: Passing facts (tests, type-checks, proofs) that
            *support* the change.
        residuals: Missing facts that *block* certification.
        failures: Actively failing facts (regressions, broken proofs).
    """

    change: CodeChange
    evidence: Sequence[Evidence] = field(default_factory=tuple)
    residuals: Sequence[Residual] = field(default_factory=tuple)
    failures: Sequence[Failure] = field(default_factory=tuple)

    def to_result(self) -> Result["CodeLearningTrace"]:
        """Project this trace into the standard :class:`Result` envelope.

        The rank is computed by :func:`fvafk.algebra.policies.default_policy`.
        """
        ev = tuple(self.evidence)
        res = tuple(self.residuals)
        fl = tuple(self.failures)

        if ev:
            base_rank = Rank.LICENSED
        elif fl:
            base_rank = Rank.REFUTED
        else:
            base_rank = Rank.UNRESOLVED

        raw = Result(
            value=self,
            rank=base_rank,
            evidence=ev,
            residuals=res,
            failures=fl,
            trace=Trace(operation=f"code_learning:{self.change.path}"),
        )
        return apply_policy(raw, default_policy)

    def replay(self) -> Mapping[str, object]:
        """Return a JSON-friendly replay record of this trace."""
        return {
            "change": {
                "path": self.change.path,
                "before": self.change.before,
                "after": self.change.after,
            },
            "evidence": [e.__dict__ for e in self.evidence],
            "residuals": [r.__dict__ for r in self.residuals],
            "failures": [f.__dict__ for f in self.failures],
        }


__all__ = ["CodeChange", "CodeLearningTrace"]
