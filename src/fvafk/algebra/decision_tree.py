"""The Arabic-algebra decision tree.

A *Phase 0* illustrative analyzer that demonstrates the constitution
end-to-end on a single example::

    >>> from fvafk.algebra import ArabicAlgebraDecisionTree
    >>> r = ArabicAlgebraDecisionTree().analyze("كاتب")
    >>> r.rank.name
    'LICENSED'
    >>> r.certificate_allowed
    False

The tree intentionally does **not** import the heavyweight ``c1`` /
``c2a`` / ``c2b`` / ``syntax`` packages. Coupling those layers as
``Evidence`` sources is Phase 2 of the roadmap; until then the tree
relies on a small hand-written rule table so the algebraic layer is
independently testable.

The output is *licensed, not certified*: the وزن "فاعل" is a candidate,
but the proper-noun / nickname interpretation is an unresolved
:class:`Residual`, which the policy uses to cap the rank at
:attr:`Rank.LICENSED`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence, Tuple

from .arabic_layers import Domain
from .core import Carrier, Evidence, Rank, Residual, Result, Trace
from .cpb import CPB, validate_cpb
from .policies import default_policy, apply_policy


@dataclass(frozen=True)
class _PatternHit:
    """A wazn-candidate match against a surface form."""

    pattern: str
    root_letters: Tuple[str, ...]
    confidence: float


# Minimal Phase-0 illustrative table — three wazn-فاعل exemplars used
# only to drive the worked example in
# ``docs/ARABIC_ALGEBRA_DECISION_TREE.md``. The shared 0.7 confidence
# reflects the fact that, in isolation (no syntactic context, no
# lexicon lookup), all three carry the *same* level of ambiguity vs.
# the proper-noun / nickname reading. Extending this table is a Phase 2
# concern; the real evidence will come from ``c2b.RootExtractor``.
_WAZN_FAEL_TABLE: Mapping[str, _PatternHit] = {
    "كاتب": _PatternHit(pattern="فاعل", root_letters=("ك", "ت", "ب"), confidence=0.7),
    "قارئ": _PatternHit(pattern="فاعل", root_letters=("ق", "ر", "أ"), confidence=0.7),
    "ناصر": _PatternHit(pattern="فاعل", root_letters=("ن", "ص", "ر"), confidence=0.7),
}


@dataclass(frozen=True)
class AnalysisReport:
    """A structured view over a decision-tree :class:`Result`.

    Convenience accessor returned by :meth:`ArabicAlgebraDecisionTree.analyze`
    alongside the raw :class:`Result`. The :class:`Result` remains the
    canonical artefact; this report is a flat read-only view.
    """

    surface: str
    pattern: str | None
    root: Tuple[str, ...] | None
    rank: Rank
    residuals: Tuple[Residual, ...]
    evidence: Tuple[Evidence, ...]

    @property
    def certificate_allowed(self) -> bool:
        return self.rank is Rank.CERTIFIED


class ArabicAlgebraDecisionTree:
    """A small, deterministic, *licensed-only* Arabic analyzer.

    The tree walks four nodes:

    1. **input → token**: classify the surface as a single Arabic word.
    2. **token → surface wazn**: match against the wazn-فاعل table.
    3. **wazn → candidate root**: read root letters from the pattern hit.
    4. **rank**: collect residuals (proper-noun ambiguity, no syntactic
       context) and ask the policy for a verdict.

    Every transition that crosses :class:`Domain` boundaries is
    validated by :func:`fvafk.algebra.cpb.validate_cpb`.
    """

    def __init__(self) -> None:
        self._bridge_token_to_wazn = CPB(
            name="token→wazn",
            source=Domain.MORPH_SURFACE,
            target=Domain.MORPH_SURFACE,
        )
        self._bridge_wazn_to_root = CPB(
            name="wazn→root",
            source=Domain.MORPH_SURFACE,
            target=Domain.ROOT,
        )

    # -- public API ---------------------------------------------------------

    def analyze(self, surface: str) -> Result[AnalysisReport]:
        """Analyze a single Arabic surface form.

        Returns a :class:`Result` whose ``value`` is an
        :class:`AnalysisReport`. The result is guaranteed to satisfy the
        no-bare-output invariant.
        """
        if not isinstance(surface, str) or not surface.strip():
            return self._refuse_empty_input(surface)

        token = surface.strip()
        carrier = Carrier(
            domain=Domain.MORPH_SURFACE,
            value=token,
            label=token,
        )

        hit = _WAZN_FAEL_TABLE.get(token)
        if hit is None:
            return self._no_pattern_match(token)

        evidence, residuals = self._collect(token, hit)
        trace = Trace(operation="ArabicAlgebraDecisionTree.analyze")

        # Validate the wazn→root bridge against an empty placeholder
        # result; the CPB layer only needs to inspect the evidence/citation
        # state, so we can run validation before deciding the final rank.
        probe = Result(
            value=token,
            rank=Rank.LICENSED,
            evidence=evidence,
            residuals=residuals,
            trace=trace,
        )
        validated = validate_cpb(self._bridge_wazn_to_root, carrier, probe)
        final_rank = apply_policy(validated, default_policy).rank

        report = AnalysisReport(
            surface=token,
            pattern=hit.pattern,
            root=hit.root_letters,
            rank=final_rank,
            residuals=residuals,
            evidence=evidence,
        )
        return Result(
            value=report,
            rank=final_rank,
            evidence=evidence,
            residuals=residuals,
            failures=validated.failures,
            trace=trace,
        )

    # -- helpers ------------------------------------------------------------

    def _collect(
        self,
        token: str,
        hit: _PatternHit,
    ) -> Tuple[Tuple[Evidence, ...], Tuple[Residual, ...]]:
        evidence: Sequence[Evidence] = (
            Evidence(
                kind="pattern.surface_match",
                source=token,
                detail=f"surface '{token}' matches wazn '{hit.pattern}'",
                weight=hit.confidence,
            ),
            Evidence(
                kind="root.candidate",
                source=token,
                detail=f"candidate root letters {hit.root_letters}",
                weight=hit.confidence,
            ),
        )
        residuals: Sequence[Residual] = (
            Residual(
                kind="context.absent",
                description=(
                    "no syntactic context supplied — operator scope, idafa, "
                    "and definiteness are unknown."
                ),
            ),
            Residual(
                kind="lexical.ambiguity",
                description=(
                    "wazn 'فاعل' candidate may be a proper noun, a nickname, "
                    "or a borrowed/transferred form (علمية/نقل/لقب)."
                ),
            ),
        )
        return tuple(evidence), tuple(residuals)

    def _refuse_empty_input(self, surface: object) -> Result[AnalysisReport]:
        report = AnalysisReport(
            surface=str(surface),
            pattern=None,
            root=None,
            rank=Rank.UNRESOLVED,
            residuals=(),
            evidence=(),
        )
        return Result(
            value=report,
            rank=Rank.UNRESOLVED,
            trace=Trace(operation="ArabicAlgebraDecisionTree.analyze.empty"),
        )

    def _no_pattern_match(self, token: str) -> Result[AnalysisReport]:
        residual = Residual(
            kind="pattern.no_match",
            description=(
                f"no wazn candidate available for '{token}' in the Phase-0 "
                "table; later phases will route this through c2b.RootExtractor."
            ),
        )
        report = AnalysisReport(
            surface=token,
            pattern=None,
            root=None,
            rank=Rank.UNRESOLVED,
            residuals=(residual,),
            evidence=(),
        )
        return Result(
            value=report,
            rank=Rank.UNRESOLVED,
            residuals=(residual,),
            trace=Trace(operation="ArabicAlgebraDecisionTree.analyze.no_match"),
        )


__all__ = ["AnalysisReport", "ArabicAlgebraDecisionTree"]
