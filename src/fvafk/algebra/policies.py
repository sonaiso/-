"""Rank-promotion policies.

A :class:`Policy` maps the *state* of a :class:`fvafk.algebra.core.Result`
(its evidence, residuals, and failures) to a :class:`fvafk.algebra.core.Rank`.

The canonical policy is :func:`default_policy`, which encodes the
constitution:

- any fatal failure forces :attr:`Rank.REFUTED`;
- empty evidence caps the rank at :attr:`Rank.CANDIDATE`;
- non-empty residuals cap the rank at :attr:`Rank.LICENSED`;
- otherwise the result may be :attr:`Rank.CERTIFIED`.

Alternative policies can be plugged in by implementing the
:class:`Policy` protocol.
"""

from __future__ import annotations

from typing import Protocol, Sequence

from .core import Evidence, Failure, Rank, Residual, Result


class Policy(Protocol):
    """Maps ``(evidence, residuals, failures)`` to a :class:`Rank`."""

    def __call__(
        self,
        evidence: Sequence[Evidence],
        residuals: Sequence[Residual],
        failures: Sequence[Failure],
    ) -> Rank:  # pragma: no cover - protocol
        ...


def default_policy(
    evidence: Sequence[Evidence],
    residuals: Sequence[Residual],
    failures: Sequence[Failure],
) -> Rank:
    """The canonical promotion policy.

    See module docstring for the rules.
    """
    if any(f.fatal for f in failures):
        return Rank.REFUTED
    if not evidence:
        return Rank.CANDIDATE if (residuals or failures) else Rank.UNRESOLVED
    if residuals:
        return Rank.LICENSED
    return Rank.CERTIFIED


def apply_policy(result: Result, policy: Policy = default_policy) -> Result:
    """Return a new :class:`Result` whose rank is the policy verdict."""
    new_rank = policy(result.evidence, result.residuals, result.failures)
    if new_rank is result.rank:
        return result
    return result.with_rank(new_rank)


__all__ = ["Policy", "apply_policy", "default_policy"]
