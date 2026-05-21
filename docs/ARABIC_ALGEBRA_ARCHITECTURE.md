# Arabic Correspondence-Preserving Algebra — Architecture

> **Constitution:** *لا مخرج عارٍ.*
> Every result = `value + rank + evidence + residuals + failures + replay`.

This document specifies the algebraic layer added under
[`src/fvafk/algebra/`](../src/fvafk/algebra). It sits **on top of**
the FVAFK pipeline (`c1` → `c2a` → `c2b` → `syntax`) without modifying
any of those layers. Phase 0 ships the constitution and the typed
primitives; Phases 1–7 (see [`ARABIC_ALGEBRA_ROADMAP.md`](ARABIC_ALGEBRA_ROADMAP.md))
progressively wire the existing FVAFK results in as `Evidence`.

---

## 1. Why an algebra?

Most NLP pipelines emit *bare values* — `pattern="فاعل"`, `root=("ك","ت","ب")`,
etc. — with no first-class record of *what supported the claim*, *what
remained unexplained*, or *what may refute it*. This makes downstream
reasoning brittle: a downstream consumer has no principled way to tell
a certified fact from a guess.

The Arabic algebra fixes this at the type level: **the only type any
operation may return is** [`Result`](../src/fvafk/algebra/core.py),
which is a tuple of `(value, rank, evidence, residuals, failures, trace)`
whose invariants are checked at construction.

## 2. Constitution (one paragraph)

> No operation may emit a `value` alone. Every result must carry the
> **rank** of its claim, the **evidence** that supports it, the
> **residuals** that block it from being certified, the **failures**
> that actively contradict it, and a **trace** that makes the operation
> replay-able. A `Rank.CERTIFIED` result is forbidden while residuals
> remain. A fatal `Failure` forces `Rank.REFUTED`.

The full grammar (with mnemonic Arabic glosses):

```
Trace      ← أثر       — provenance DAG
Domain     ← مجال      — layer over which a carrier lives
Carrier    ← حامل      — typed substrate (value + domain)
CPB        ← ربط مطابق — Correspondence-Preserving Bridge
Operation  ← عملية     — Carrier → Result
Evidence   ← دليل      — scoped supporting observation
Rank       ← رتبة      — UNRESOLVED < CANDIDATE < LICENSED < CERTIFIED
Residual   ← بقية      — explicit unresolved item, blocks certification
Failure    ← فشل       — typed contradiction; fatal → REFUTED
Result     ← نتيجة     — the only output type
```

## 3. Domains and forbidden bridges

[`arabic_layers.py`](../src/fvafk/algebra/arabic_layers.py) declares the
nine domains (grapheme → hukm) and the allowed-bridge matrix. Direct
cross-layer promotions are **rejected at CPB construction**:

| Source | Forbidden target | Reason |
|---|---|---|
| `GRAPHEME` | `MORPH_DEEP` | رسم → وزن عميق |
| `PHONEME` | `MORPH_DEEP` | صوت → وزن عميق |
| `SYLLABLE` | `ROOT` | مقطع → جذر |
| `MORPH_SURFACE` | `MORPH_DEEP` | وزن ظاهر → وزن عميق |
| `MORPH_SURFACE` | `SEMANTICS` | وزن → دلالة |
| `MORPH_DEEP` | `HUKM` | وزن عميق → حكم |

These restate, for the FVAFK pipeline, the prohibitions documented in
[`docs/DAL_ALGEBRA_SIGNATURE.md`](DAL_ALGEBRA_SIGNATURE.md). The two
algebras stay independent (see §6).

## 4. The `Result` invariant

Implemented in [`core.py`](../src/fvafk/algebra/core.py):

1. A rank ≥ `LICENSED` requires at least one `Evidence`.
2. `CERTIFIED` forbids non-empty `residuals`.
3. Any fatal `Failure` forces `REFUTED` (enforced via `with_failure`).

These three rules are sufficient to make *every* output auditable.

## 5. Decision tree (Phase 0 demonstrator)

[`decision_tree.py`](../src/fvafk/algebra/decision_tree.py) ships a
deterministic illustrator that walks four nodes for a single surface
form (e.g. `كاتب`):

```
كاتب
 → كلمة
 → وزن فاعل (مرشح)
 → جذر محتمل: ك ت ب
 → rank = LICENSED
 → residuals = السياق غائب، احتمال العلمية/النقل/اللقب
 → certificate_allowed = False
```

The output is **licensed, not certified**, because the absence of
syntactic context and the proper-noun ambiguity are both unresolved
`Residual`s. The wazn never "steals" the judgement rank.

## 6. Boundary vs. `dal_core`

The repository also hosts [`src/dal_core/`](../src/dal_core), which
implements its own *lexical-sign* algebra ending at `D_mufrad`
(see [`SPEC_DAL_CORE.md`](SPEC_DAL_CORE.md) and
[`DAL_ALGEBRA_SIGNATURE.md`](DAL_ALGEBRA_SIGNATURE.md)). The two
algebras share the *constitution* (no bare output, no direct cross-layer
promotion) but operate at different scopes and **do not import each
other** in Phase 0:

| Layer | Module | Scope |
|---|---|---|
| Lexical-sign (D0–D7) | `dal_core` | Up to pre-syntax / lexical closure |
| FVAFK pipeline (G→H) | `fvafk.algebra` | Phon/morph/syntax artefacts produced by `c1`–`syntax` |

A future PR may unify the two under a common `Result` envelope; until
then they evolve in parallel.

## 7. Public surface

```python
from fvafk.algebra import (
    # core
    Trace, Domain, Carrier, Evidence, Residual, Failure, Rank, Result,
    Operation, empty_result,
    # bridges & policy
    CPB, validate_cpb, Policy, default_policy, apply_policy,
    # layers
    ALLOWED_BRIDGES, FORBIDDEN_BRIDGES, is_bridge_allowed,
    # analyzers
    ArabicAlgebraDecisionTree, AnalysisReport,
    # code learning
    CodeChange, CodeLearningTrace, KnowledgeStore,
)
```

See [`ARABIC_ALGEBRA_ROADMAP.md`](ARABIC_ALGEBRA_ROADMAP.md) for the
phase plan and [`ARABIC_ALGEBRA_DECISION_TREE.md`](ARABIC_ALGEBRA_DECISION_TREE.md)
for a worked example.
