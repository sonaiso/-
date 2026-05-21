# Arabic Algebra — Roadmap

The algebra lands in eight phases. Phase 0 is implemented in this PR;
later phases are scoped here so contributors can pick them up as
follow-up PRs without scope drift.

The cardinal rule across all phases:

> **No algebra may claim outputs of a later phase.**
> Each phase only consumes what previous phases certify, and only emits
> what its own contracts allow.

---

## Phase 0 — CPB, ranks, and residuals ✅ (merged via PR #35)

**Goal.** Land the constitution and the typed primitives without
touching the existing FVAFK pipeline.

**Deliverables.**
- `src/fvafk/algebra/{core,cpb,policies,arabic_layers}.py`
- `src/fvafk/algebra/{decision_tree,code_learning,learning}.py`
- `tests/test_algebra_{cpb,decision_tree,code_learning}.py`
- `docs/ARABIC_ALGEBRA_{ARCHITECTURE,ROADMAP,DECISION_TREE}.md`

**Status.** **Merged into `main` via PR #35.** Phase 0 is no longer a
proposal; the constitution **لا مخرج عارٍ** (every Result =
`value + rank + evidence + residuals + failures + replay`) is now a
runtime contract enforced by `core.Result`, `cpb.validate_cpb`, and the
typed `ALLOWED_BRIDGES` / `FORBIDDEN_BRIDGES` matrix.

The canonical `Rank` set is exactly:

> `UNRESOLVED`, `CANDIDATE`, `LICENSED`, `CERTIFIED`, `REFUTED`.

Legacy names (e.g. `CERTIFICATE`, `BLOCKED`) are forbidden and pinned
out by `tests/fvafk/algebra/test_result_invariants.py`.

**Exit criterion.** ✅ All algebra tests pass; no existing test changes.

---

## Phase 0.5 — Governance hardening (this PR)

**Goal.** Lock the merged constitution so future PRs cannot silently
violate it. No production code changes; only tests + CI + docs.

**Deliverables.**
- `tests/fvafk/algebra/test_bridge_matrix.py` — parametrised tests over
  every entry of `ALLOWED_BRIDGES` and `FORBIDDEN_BRIDGES`, plus a
  topology consistency check (the two sets are disjoint; identity
  bridges are always legal; unspecified pairs default to forbidden).
- `tests/fvafk/algebra/test_result_invariants.py` — pins the canonical
  `Rank` names, the four `Result` invariants (`LICENSED`/`CERTIFIED`
  require evidence; `CERTIFIED` forbids residuals; fatal `Failure`
  forces `REFUTED`), and the `default_policy` truth table.
- `tests/fvafk/algebra/test_cpb_contract.py` — full coverage of
  `validate_cpb`: domain mismatch, uncited output (LICENSED and
  CERTIFIED), `UNRESOLVED` exemption, label/domain citation fallback.
- `.github/workflows/ci.yml` — new blocking `algebra-governance` job
  on Python 3.11 / 3.12 that runs the algebra tests on every push and
  pull request to `main` / `develop`.

**Exit criterion.** All algebra tests green in CI; the canonical Rank
set and bridge matrix are pinned by tests; legacy `tests/test_algebra_*`
files continue to pass unmodified. **Phase 0 is merged; the next
substantive milestone is Phase 1 surface coverage.**

---

## Phase 1 — Decision-tree surface coverage

Extend `ArabicAlgebraDecisionTree` from the Phase-0 illustrative table
to cover the wazn families already documented under `awzan-claude-atwah.csv`
and `src/fvafk/c2b/pattern_catalog.py`. Still no coupling to
`RootExtractor`: the goal is to verify the algebra holds at scale on
hand-built fixtures.

**Touches.** `decision_tree.py`; new fixtures under
`tests/fixtures/algebra/`.

---

## Phase 2 — Wire `c1` / `c2a` / `c2b` / `syntax` as `Evidence` sources

Introduce `src/fvafk/algebra/adapters/` with thin wrappers that take the
existing dataclasses (`MorphologicalAnalysis`, `WordForm`,
`RootExtractionResult`, syntax links) and emit `Evidence` whose
`source` cites the original analysis. **No FVAFK code is modified**;
the adapters are pure read-only translators.

**Exit criterion.** `ArabicAlgebraDecisionTree.analyze("كاتب")` returns
evidence whose `source` is a real `RootExtractionResult` id, not a
hand-coded table.

---

## Phase 3 — Algebraic morphology

Promote morphology operations (pattern matching, root extraction,
broken-plural derivation, augmentation operators) from "functions that
return values" to first-class `Operation` instances. Each is gated by
a CPB declaring `MORPH_SURFACE → ROOT` or `ROOT → MORPH_DEEP`.

**Touches.** New `algebra/morphology.py`; no edits to `c2b/`.

---

## Phase 4 — Algebraic syntax

Same shape as Phase 3 but for the syntax layer: `ROOT → SYNTAX` and
`MORPH_DEEP → SYNTAX` bridges, with `Failure`s reflecting
case/agreement violations.

---

## Phase 5 — Semantics, إفادة, and حكم

Add the final three domains: `SYNTAX → SEMANTICS → HUKM`. Residuals at
this layer capture the gap between *form* and *intended meaning*; only
explicit evidence (rhetoric markers, scope operators, lexicon entries
with `haqiqa_majaz` annotation) may upgrade rank to `CERTIFIED`.

> **Note.** This phase must respect the
> [`dal_core` meaning-field prohibition](SPEC_DAL_CORE.md): no leakage
> of `meaning` / `murad` / `haqiqa_majaz` fields into the `MORPH_*` or
> `SYNTAX` domains.

---

## Phase 6 — Code-learning algebra

Promote `CodeLearningTrace` (Phase 0 seed) into a CI-integrated learner:
each PR generates a trace whose `Evidence` is the test/CI signal and
whose `Residuals` are uncovered branches. `parallel_validation` output
becomes a typed `Evidence` stream.

**Touches.** New `algebra/ci_adapters.py`; CI workflow under
`.github/workflows/`.

---

## Phase 7 — CI governance

Encode the constitution as a CI gate: any module that returns a
non-`Result` from a public API fails `parallel_validation`. The gate
runs against `src/fvafk/algebra/` first, then expands progressively to
the rest of the repository.

---

## Out-of-scope (for now)

- Refactoring existing `fvafk.c1`–`c2b` modules to return `Result`.
  This is a Phase 8+ migration and requires its own RFC.
- Statistical/neural learners on top of `KnowledgeStore`. The store is
  deliberately append-only and deterministic in Phase 0.
- Cross-importing `dal_core` types. See
  [`ARABIC_ALGEBRA_ARCHITECTURE.md`](ARABIC_ALGEBRA_ARCHITECTURE.md) §6.
