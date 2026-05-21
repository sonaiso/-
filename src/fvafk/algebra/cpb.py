"""Correspondence-Preserving Bridge (CPB).

A CPB is the morphism contract that an :class:`Operation` must satisfy
when moving a :class:`Carrier` across :class:`Domain`s.

Two invariants are enforced:

1. **Topological legality** — the source/target pair must be allowed by
   :func:`fvafk.algebra.arabic_layers.is_bridge_allowed`. Direct cross-layer
   promotions (e.g. ``GRAPHEME → MORPH_DEEP``) are rejected.
2. **Correspondence** — the output result must carry evidence that
   *cites* the input carrier (no claim may appear out of thin air).

The module exposes the :class:`CPB` dataclass and :func:`validate_cpb`,
which is the single entry point used by higher-level operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .arabic_layers import Domain, is_bridge_allowed
from .core import Carrier, Evidence, Failure, Rank, Result


@dataclass(frozen=True)
class CPB:
    """A typed, immutable bridge between two domains.

    Attributes:
        name: Human-readable identifier of the bridge.
        source: Domain of the input carrier.
        target: Domain of the output carrier.
    """

    name: str
    source: Domain
    target: Domain

    def __post_init__(self) -> None:
        if not self.name:
            raise ValueError("CPB.name must be non-empty")
        if not is_bridge_allowed(self.source, self.target):
            raise ValueError(
                f"CPB '{self.name}' declares a forbidden bridge "
                f"{self.source.value} → {self.target.value}; "
                "direct cross-layer promotion is not allowed."
            )


def validate_cpb(
    cpb: CPB,
    carrier: Carrier[Any],
    result: Result[Any],
) -> Result[Any]:
    """Validate that ``result`` is a legal output of ``cpb`` applied to ``carrier``.

    The result is annotated with a typed :class:`Failure` (and demoted to
    :attr:`Rank.REFUTED`) when any invariant is violated. When all
    invariants hold the input result is returned unchanged.

    Invariants checked:

    1. The carrier's domain matches ``cpb.source``.
    2. The bridge ``cpb.source → cpb.target`` is allowed.
    3. The result carries at least one :class:`Evidence` whose
       ``source`` references the carrier (label or domain).
    """
    # 1. carrier domain matches bridge source.
    if carrier.domain is not cpb.source:
        failure = Failure(
            kind="cpb.domain_mismatch",
            description=(
                f"CPB '{cpb.name}' expects source {cpb.source.value} "
                f"but received carrier in {carrier.domain.value}."
            ),
            fatal=True,
        )
        return result.with_failure(failure)

    # 2. bridge legality.
    if not is_bridge_allowed(cpb.source, cpb.target):
        failure = Failure(
            kind="cpb.forbidden_bridge",
            description=(
                f"CPB '{cpb.name}' uses a forbidden bridge "
                f"{cpb.source.value} → {cpb.target.value}."
            ),
            fatal=True,
        )
        return result.with_failure(failure)

    # 3. correspondence: result must cite the input.
    citation_key = carrier.label or carrier.domain.value
    if result.rank is not Rank.UNRESOLVED and not _has_citation(result, citation_key):
        failure = Failure(
            kind="cpb.uncited_output",
            description=(
                f"CPB '{cpb.name}' produced a ranked result with no "
                f"evidence citing the input carrier '{citation_key}'."
            ),
            fatal=True,
        )
        return result.with_failure(failure)

    return result


def _has_citation(result: Result[Any], key: str) -> bool:
    """Return ``True`` iff any evidence in ``result`` cites ``key``."""
    needle = key.lower()
    for ev in result.evidence:
        if needle and (needle in ev.source.lower() or needle in ev.detail.lower()):
            return True
    return False


__all__ = ["CPB", "validate_cpb"]
