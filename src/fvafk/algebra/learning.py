"""Incremental learning loop over :class:`fvafk.algebra.core.Result`.

A minimal in-memory knowledge store that accumulates evidence/residuals
across results. Phase-0 implementation: append-only, deterministic, no
persistence. Heavier learners (statistical, neural) are out of scope
until the algebra has been wired through Phases 1–5.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from .core import Evidence, Result


@dataclass
class KnowledgeStore:
    """Append-only knowledge store keyed by evidence ``kind``.

    The store records, for each evidence kind, every observed
    ``(source, detail, weight)`` triple. It also tracks the total number
    of results ingested. The data is intentionally simple — the point of
    Phase 0 is to *exercise the constitution*, not to ship a learner.
    """

    facts: Dict[str, List[Tuple[str, str, float]]] = field(default_factory=dict)
    residuals_seen: Dict[str, int] = field(default_factory=dict)
    results_ingested: int = 0

    def ingest(self, result: Result) -> None:
        """Record evidence and residual counters from ``result``."""
        self.results_ingested += 1
        for ev in result.evidence:
            self.facts.setdefault(ev.kind, []).append(
                (ev.source, ev.detail, ev.weight)
            )
        for res in result.residuals:
            self.residuals_seen[res.kind] = self.residuals_seen.get(res.kind, 0) + 1

    def kinds(self) -> Tuple[str, ...]:
        """Return the evidence kinds observed so far."""
        return tuple(sorted(self.facts.keys()))

    def evidence_for(self, kind: str) -> Tuple[Evidence, ...]:
        """Return the evidence atoms accumulated for a given kind."""
        return tuple(
            Evidence(kind=kind, source=src, detail=detail, weight=weight)
            for (src, detail, weight) in self.facts.get(kind, ())
        )


__all__ = ["KnowledgeStore"]
