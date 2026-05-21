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
from typing import FrozenSet, List, Mapping, Sequence, Tuple

from .arabic_layers import Domain
from .core import Carrier, Evidence, Rank, Residual, Result, Trace
from .cpb import CPB, validate_cpb
from .policies import default_policy, apply_policy


@dataclass(frozen=True)
class _PatternHit:
    """A wazn-candidate match against a surface form.

    Phase-1 extension: ``extra_residual_kinds`` carries token-level
    residual hints (e.g. a token whose surface coincides with a known
    proper-noun pattern adds ``proper_name.possible``). Family-level
    hints come from :data:`_FAMILY_RESIDUALS` and are merged in by
    :meth:`ArabicAlgebraDecisionTree._collect`.
    """

    pattern: str
    root_letters: Tuple[str, ...]
    confidence: float
    extra_residual_kinds: Tuple[str, ...] = ()


# Phase-1 surface catalog. Covers the nine wazn families documented in
# ``docs/ARABIC_ALGEBRA_DECISION_TREE.md``. Hand-built fixtures only;
# real evidence will come from ``c2b.RootExtractor`` in Phase 2.
#
# Confidence stays at 0.7 across the board: in isolation (no syntactic
# context, no lexicon lookup), every match carries the *same* level of
# residual ambiguity vs. the proper-noun / transferred-usage readings.
_SURFACE_CATALOG: Mapping[str, _PatternHit] = {
    # فاعل — active-participle-shape
    "كاتب": _PatternHit("فاعل", ("ك", "ت", "ب"), 0.7),
    "قارئ": _PatternHit("فاعل", ("ق", "ر", "أ"), 0.7),
    "ناصر": _PatternHit("فاعل", ("ن", "ص", "ر"), 0.7, ("proper_name.possible",)),
    "حامد": _PatternHit("فاعل", ("ح", "م", "د"), 0.7, ("proper_name.possible",)),
    # مفعول — passive-participle-shape
    "مكتوب": _PatternHit("مفعول", ("ك", "ت", "ب"), 0.7),
    "مقروء": _PatternHit("مفعول", ("ق", "ر", "أ"), 0.7),
    "محمود": _PatternHit("مفعول", ("ح", "م", "د"), 0.7, ("proper_name.possible",)),
    # فعّال — intensive / professional shape
    "كذّاب": _PatternHit("فعّال", ("ك", "ذ", "ب"), 0.7),
    "نجّار": _PatternHit("فعّال", ("ن", "ج", "ر"), 0.7),
    "خبّاز": _PatternHit("فعّال", ("خ", "ب", "ز"), 0.7),
    # مفعال — tool / intensive shape
    "مفتاح": _PatternHit("مفعال", ("ف", "ت", "ح"), 0.7),
    "مكثار": _PatternHit("مفعال", ("ك", "ث", "ر"), 0.7),
    "مهذار": _PatternHit("مفعال", ("ه", "ذ", "ر"), 0.7),
    # مِفعل — tool shape (kasra)
    "مِبرد": _PatternHit("مِفعل", ("ب", "ر", "د"), 0.7),
    "مِنشار": _PatternHit("مِفعل", ("ن", "ش", "ر"), 0.7, ("pattern.collision",)),
    "مِقص": _PatternHit("مِفعل", ("ق", "ص", "ص"), 0.7),
    # مَفعل — place / time shape (fatha)
    "مَكتب": _PatternHit("مَفعل", ("ك", "ت", "ب"), 0.7),
    "مَلعب": _PatternHit("مَفعل", ("ل", "ع", "ب"), 0.7),
    "مَجلس": _PatternHit("مَفعل", ("ج", "ل", "س"), 0.7),
    # فعلة — small-noun shape
    "غرفة": _PatternHit("فعلة", ("غ", "ر", "ف"), 0.7),
    "شجرة": _PatternHit("فعلة", ("ش", "ج", "ر"), 0.7),
    "نخلة": _PatternHit("فعلة", ("ن", "خ", "ل"), 0.7),
    # فعول — intensive / quality shape
    "صبور": _PatternHit("فعول", ("ص", "ب", "ر"), 0.7),
    "شكور": _PatternHit("فعول", ("ش", "ك", "ر"), 0.7),
    "غفور": _PatternHit("فعول", ("غ", "ف", "ر"), 0.7),
    # فعيل — quality / participle shape
    "كريم": _PatternHit("فعيل", ("ك", "ر", "م"), 0.7, ("proper_name.possible",)),
    "عظيم": _PatternHit("فعيل", ("ع", "ظ", "م"), 0.7),
    "حكيم": _PatternHit("فعيل", ("ح", "ك", "م"), 0.7, ("proper_name.possible",)),
}

# Backward-compatibility alias for any external code that imported the
# Phase-0 table name. New code should use ``_SURFACE_CATALOG``.
_WAZN_FAEL_TABLE: Mapping[str, _PatternHit] = {
    k: v for k, v in _SURFACE_CATALOG.items() if v.pattern == "فاعل"
}


# Family-level residuals. These are the residuals that apply to *every*
# token in a wazn family, regardless of which specific exemplar was hit.
# Per-token residuals (``_PatternHit.extra_residual_kinds``) are merged
# on top.
_FAMILY_RESIDUALS: Mapping[str, Tuple[str, ...]] = {
    # فعّال is overwhelmingly read as a profession/intensive noun even
    # without context, so the transferred-usage reading is the default
    # alternative the surface analyzer must keep alive.
    "فعّال": ("transfer.possible",),
    # مَفعل surfaces are a chronic place/time/verb-noun collision point
    # (مَفعِل vs مَفعَل vs مَفْعَل) — flag it at the family level.
    "مَفعل": ("pattern.collision",),
    # فعول shape readily transfers between intensive (صبور) and
    # quality / divine-name readings (غفور) without a lexicon lookup.
    "فعول": ("transfer.possible",),
}


# Residual kinds the surface analyzer is allowed to emit. Anything else
# would be a Phase-1 contract violation (e.g., a future contributor
# wiring a ``semantic.*`` or ``hukm.*`` residual into the surface tree).
_ALLOWED_RESIDUAL_KINDS: FrozenSet[str] = frozenset(
    {
        "context.absent",
        "lexical.ambiguity",
        "proper_name.possible",
        "transfer.possible",
        "pattern.collision",
        "pattern.no_match",
    }
)


# Evidence-kind prefixes the surface analyzer must never emit. The
# surface tree only deals in pattern matching and candidate-root
# extraction; semantic interpretation and judgement live in later
# phases (Phase 5+). The :class:`ArabicAlgebraDecisionTree` runtime
# guard re-checks this set in case a future patch wires in a
# higher-layer evidence kind by accident.
_FORBIDDEN_EVIDENCE_PREFIXES: Tuple[str, ...] = ("semantic.", "hukm.")


# Human-readable descriptions for every allowed residual kind.
# Centralised so the surface tree emits consistent prose regardless of
# which family contributed the kind.
_RESIDUAL_DESCRIPTIONS: Mapping[str, str] = {
    "context.absent": (
        "no syntactic context supplied — operator scope, idafa, and "
        "definiteness are unknown."
    ),
    "lexical.ambiguity": (
        "surface candidate may be a proper noun, a nickname, or a "
        "borrowed/transferred form (علمية/نقل/لقب)."
    ),
    "proper_name.possible": (
        "surface coincides with a frequent proper-noun reading; "
        "lexical confirmation is required before any rank promotion."
    ),
    "transfer.possible": (
        "surface admits a transferred-usage (نقل) reading: "
        "intensive/professional/quality alternatives compete with the "
        "literal pattern reading."
    ),
    "pattern.collision": (
        "surface admits two or more wazn parses (e.g. مَفعِل vs مَفعَل, "
        "place vs time vs verb-noun); disambiguation requires context."
    ),
    "pattern.no_match": (
        "no wazn candidate available for this surface in the Phase-1 "
        "catalog; later phases will route this through c2b.RootExtractor."
    ),
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

        hit = _SURFACE_CATALOG.get(token)
        if hit is None:
            return self._no_pattern_match(token)

        evidence, residuals = self._collect(token, hit)
        trace = Trace(operation="ArabicAlgebraDecisionTree.analyze")

        # Phase-1 surface guard: the surface tree must never emit a
        # ``semantic.*`` or ``hukm.*`` evidence kind. This is enforced
        # by construction (we only emit ``pattern.surface_match`` and
        # ``root.candidate``); the runtime check defends against future
        # patches that might wire a higher-layer evidence kind into the
        # surface analyzer by accident.
        for ev in evidence:
            if ev.kind.startswith(_FORBIDDEN_EVIDENCE_PREFIXES):
                raise AssertionError(
                    f"surface analyzer emitted forbidden evidence kind "
                    f"'{ev.kind}'; MORPH_SURFACE must not jump to "
                    f"SEMANTICS or HUKM."
                )

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

        # Phase-1 surface cap: a context-free surface result must never
        # be promoted to ``CERTIFIED``. ``default_policy`` already
        # respects this because we always emit at least the
        # ``context.absent`` and ``lexical.ambiguity`` residuals, but
        # the assertion is a defensive contract: if a future change
        # ever drops both residuals, the failure should be loud, not
        # silent rank theft.
        if final_rank is Rank.CERTIFIED:
            raise AssertionError(
                "surface analyzer reached CERTIFIED without context; "
                "MORPH_SURFACE must remain capped at LICENSED."
            )

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
        residuals = self._build_residuals(hit)
        return tuple(evidence), residuals

    def _build_residuals(self, hit: _PatternHit) -> Tuple[Residual, ...]:
        """Merge universal, family-level, and per-token residuals.

        - **Universal**: every surface match emits ``context.absent``
          and ``lexical.ambiguity`` because in isolation no syntactic
          context is available and the proper-noun / transferred reading
          can never be ruled out.
        - **Family-level**: pulled from :data:`_FAMILY_RESIDUALS` (e.g.
          فعّال always carries ``transfer.possible``).
        - **Per-token**: pulled from ``hit.extra_residual_kinds`` (e.g.
          ``ناصر`` carries ``proper_name.possible``).

        Residuals are deduplicated by ``kind`` while preserving order.
        """
        ordered_kinds: List[str] = []
        for kind in (
            "context.absent",
            "lexical.ambiguity",
            *_FAMILY_RESIDUALS.get(hit.pattern, ()),
            *hit.extra_residual_kinds,
        ):
            if kind not in ordered_kinds:
                ordered_kinds.append(kind)

        residuals = tuple(
            Residual(kind=kind, description=_RESIDUAL_DESCRIPTIONS[kind])
            for kind in ordered_kinds
        )

        # Phase-1 invariant: the surface analyzer is only allowed to
        # emit residual kinds in the whitelisted set. A typo or future
        # patch that introduces an unrecognised kind should fail loudly.
        for r in residuals:
            if r.kind not in _ALLOWED_RESIDUAL_KINDS:
                raise AssertionError(
                    f"surface analyzer produced disallowed residual kind "
                    f"'{r.kind}'; allowed: {sorted(_ALLOWED_RESIDUAL_KINDS)}."
                )
        return residuals

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
            description=_RESIDUAL_DESCRIPTIONS["pattern.no_match"],
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
