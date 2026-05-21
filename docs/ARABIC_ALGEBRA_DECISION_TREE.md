# Decision Tree — Worked Example for `كاتب`

This is the canonical Phase-0 walkthrough. It shows exactly which
nodes [`ArabicAlgebraDecisionTree`](../src/fvafk/algebra/decision_tree.py)
visits, which `Evidence` and `Residual` atoms each node emits, and why
the final rank settles at `LICENSED` (not `CERTIFIED`).

---

## 1. Code

```python
from fvafk.algebra import ArabicAlgebraDecisionTree

result = ArabicAlgebraDecisionTree().analyze("كاتب")

print(result.value.surface)            # 'كاتب'
print(result.value.pattern)            # 'فاعل'
print(result.value.root)               # ('ك', 'ت', 'ب')
print(result.rank.name)                # 'LICENSED'
print(result.certificate_allowed)      # False
print([r.kind for r in result.residuals])
# ['context.absent', 'lexical.ambiguity']
```

## 2. Trace

```
كاتب
 │
 ├── node 1: input → token
 │     domain: GRAPHEME → MORPH_SURFACE
 │     carrier: Carrier(domain=MORPH_SURFACE, value='كاتب', label='كاتب')
 │
 ├── node 2: token → wazn (CPB token→wazn, MORPH_SURFACE → MORPH_SURFACE)
 │     evidence:
 │       • kind=pattern.surface_match  source='كاتب'
 │         detail="surface 'كاتب' matches wazn 'فاعل'"
 │         weight=0.7
 │
 ├── node 3: wazn → root  (CPB wazn→root, MORPH_SURFACE → ROOT)
 │     evidence:
 │       • kind=root.candidate         source='كاتب'
 │         detail="candidate root letters ('ك','ت','ب')"
 │         weight=0.7
 │     residuals:
 │       • kind=context.absent
 │         description="no syntactic context supplied — operator scope,
 │                      idafa, and definiteness are unknown."
 │       • kind=lexical.ambiguity
 │         description="wazn 'فاعل' candidate may be a proper noun, a
 │                      nickname, or a borrowed/transferred form."
 │
 └── node 4: rank  (apply default_policy)
       inputs: 2 evidence atoms, 2 residuals, 0 failures
       verdict: LICENSED   (because evidence ≥ 1 ∧ residuals > 0)
       certificate_allowed = False
```

## 3. Why not `CERTIFIED`?

Two residuals block certification:

- **`context.absent`** — `كاتب` was analyzed in isolation. Without a
  surrounding sentence the operator scope (`إنّ`, `كان`, `لا`...), the
  definiteness, and the إعراب are all unknown. Any of these can flip
  the morphological reading.
- **`lexical.ambiguity`** — `فاعل` is a wazn *candidate*, not a final
  judgement. The same surface may be a proper noun (علم), a nickname
  (لقب), or a transferred/borrowed form (منقول). Phase-2 evidence from
  `c2b.RootExtractor` plus a syntactic context could resolve this, but
  in Phase 0 it remains explicitly unresolved.

This is the constitution in action: **the wazn never steals the rank
of the judgement**. The algebra forces the caller to acknowledge what
was *not* resolved.

## 4. What would flip the rank to `CERTIFIED`?

Removing both residuals — typically by supplying:

1. a sentence-level context that fixes the syntactic role (resolves
   `context.absent`), **and**
2. a higher-confidence root attestation (e.g. agreement with a known
   lexicon entry under `c2b/root_resolver/`) that rules out the
   proper-noun / nickname interpretations (resolves
   `lexical.ambiguity`).

Both are Phase 2 / Phase 4 work. See
[`ARABIC_ALGEBRA_ROADMAP.md`](ARABIC_ALGEBRA_ROADMAP.md).

## 5. Replay

The full result is JSON-serialisable via `result.replay()`:

```json
{
  "value": { "surface": "كاتب", "pattern": "فاعل", "root": ["ك","ت","ب"], ... },
  "rank": "LICENSED",
  "evidence":  [ { "kind": "pattern.surface_match", "source": "كاتب", ... },
                 { "kind": "root.candidate",        "source": "كاتب", ... } ],
  "residuals": [ { "kind": "context.absent",    "description": "..." },
                 { "kind": "lexical.ambiguity", "description": "..." } ],
  "failures":  [],
  "trace":     { "operation": "ArabicAlgebraDecisionTree.analyze", ... }
}
```

This record is the contract: anyone replaying it can reconstruct
*every* claim, *every* support, and *every* gap of the analysis.

---

## 6. Phase 1 — Surface coverage

Phase 1 extends the Phase-0 illustrative table from three exemplars to
**nine wazn families** worth of hand-built fixtures. The catalog lives
in [`tests/fixtures/algebra/wazn_surface_cases.json`](../tests/fixtures/algebra/wazn_surface_cases.json)
and is exercised by
[`tests/test_algebra_decision_tree_phase1.py`](../tests/test_algebra_decision_tree_phase1.py).

### Covered families

| Family   | Default extra residual | Sample exemplars                    |
|----------|------------------------|-------------------------------------|
| `فاعل`   | (per-token)            | كاتب، قارئ، ناصر, حامد              |
| `مفعول` | (per-token)             | مكتوب، مقروء، محمود                  |
| `فعّال` | `transfer.possible`     | كذّاب، نجّار، خبّاز                |
| `مفعال` | (none)                  | مفتاح، مكثار، مهذار                  |
| `مِفعل` | (per-token)             | مِبرد، مِنشار، مِقص                |
| `مَفعل` | `pattern.collision`     | مَكتب، مَلعب، مَجلس                |
| `فعلة`   | (none)                  | غرفة، شجرة، نخلة                    |
| `فعول`   | `transfer.possible`     | صبور، شكور، غفور                    |
| `فعيل`   | (per-token)             | كريم، عظيم، حكيم                    |

Tokens that surface-coincide with a frequent proper-noun reading
(`ناصر`, `حامد`, `محمود`, `كريم`, `حكيم`) carry an additional
per-token `proper_name.possible` residual. Per the Phase-1 plan
(option (a)), the surface match is **not refused** when a proper-noun
reading is plausible — the algebra honestly records the surface match
*and* the unresolved alternative reading via the residual.

### Worked example — `مكتوب → مفعول`

```
مكتوب
 │
 ├── node 1: input → token
 │     domain: GRAPHEME → MORPH_SURFACE
 │     carrier: Carrier(domain=MORPH_SURFACE, value='مكتوب', label='مكتوب')
 │
 ├── node 2: token → wazn (CPB token→wazn, MORPH_SURFACE → MORPH_SURFACE)
 │     evidence:
 │       • kind=pattern.surface_match  source='مكتوب'
 │         detail="surface 'مكتوب' matches wazn 'مفعول'"
 │
 ├── node 3: wazn → root  (CPB wazn→root, MORPH_SURFACE → ROOT)
 │     evidence:
 │       • kind=root.candidate         source='مكتوب'
 │         detail="candidate root letters ('ك','ت','ب')"
 │     residuals:
 │       • kind=context.absent
 │       • kind=lexical.ambiguity
 │
 └── node 4: rank  (apply default_policy)
       inputs: 2 evidence atoms, 2 residuals, 0 failures
       verdict: LICENSED   (residuals > 0 ⇒ no certification)
       certificate_allowed = False
```

### The Phase-1 invariant

Every covered family proves the same rule:

> الوزن السطحي يرخّص احتمالاً صرفياً،
> ولا يمنح دلالة نهائية،
> ولا يرفع النتيجة إلى CERTIFIED،
> ولا يقفز إلى SEMANTICS أو HUKM.

Concretely, Phase 1 pins three runtime guards in
[`decision_tree.py`](../src/fvafk/algebra/decision_tree.py):

1. **Surface cap.** A surface result that somehow reaches
   `Rank.CERTIFIED` raises an `AssertionError`. The `default_policy`
   already prevents this because every match emits at least
   `context.absent` + `lexical.ambiguity`; the assertion is a
   defensive contract against future patches.
2. **No semantic / hukm evidence.** The surface tree may only emit
   evidence kinds in `{pattern.surface_match, root.candidate}`. Any
   `semantic.*` or `hukm.*` kind triggers an `AssertionError` —
   `MORPH_SURFACE` must never jump to `SEMANTICS` or `HUKM`.
3. **Whitelisted residuals.** Residual kinds are restricted to
   `{context.absent, lexical.ambiguity, proper_name.possible,`
   `transfer.possible, pattern.collision, pattern.no_match}`.

The forbidden bridges `MORPH_SURFACE → MORPH_DEEP`,
`MORPH_SURFACE → SEMANTICS`, and `MORPH_DEEP → HUKM` continue to be
rejected at `CPB` construction time by Phase 0 / 0.5 governance, and
Phase 1 adds explicit regression tests pinning that behaviour.

Phase 2 will replace the hand-built catalog with adapters over
`c2b.RootExtractor`; Phase 1 deliberately keeps the catalog
self-contained so the algebra can be audited without pulling the rest
of the FVAFK pipeline in.

---

## 7. Phase 2 — FVAFK Evidence adapters

Phase 2 introduces `src/fvafk/algebra/adapters/` to wire real FVAFK
pipeline outputs (C1, C2a, C2b, syntax) as Evidence sources for the
algebra layer. **No FVAFK pipeline code is modified**; adapters are
pure read-only translators.

### Adapter architecture

All adapters inherit from `BaseAdapter` which enforces:

1. **Immutability** — adapters are stateless transformers; no state
   mutation after initialization
2. **Evidence-only output** — adapters return `Tuple[Evidence, ...]`,
   never bare values
3. **Source citation** — every Evidence cites upstream object via
   `source` field (format: `"<module>:<type>:<id>"`)
4. **Domain boundaries** — adapters respect forbidden bridges (no
   `MORPH_SURFACE → SEMANTICS` jump)

### C2bAdapter — RootExtractor → Evidence (primary use case)

The primary Phase-2 use case is `C2bAdapter`, which translates
`RootExtractionResult` from `fvafk.c2b.RootExtractor` into ROOT domain
Evidence:

```python
from fvafk.c2b import RootExtractor
from fvafk.algebra.adapters import C2bAdapter

extractor = RootExtractor()
result = extractor.extract_with_affixes("كاتب")

adapter = C2bAdapter()
evidence_tuple = adapter.adapt(result)

for ev in evidence_tuple:
    print(ev.kind, ev.source, ev.detail)
# Output:
# root.candidate c2b:RootExtractionResult:كاتب root=('ك', 'ت', 'ب') from 'كاتب'
```

Key contracts:

- **Root evidence** — when `result.root` is not `None`, adapter emits
  Evidence with kind `"root.candidate"`
- **Weight by confidence** — roots with weak letters (و/ي/ا) receive
  lower weight (more ambiguous)
- **Affix evidence** — prefix/suffix information translated to
  `"affix.detected"` Evidence
- **Residuals for gaps** — `adapt_with_residuals()` method emits
  residuals for aggressive stripping or multiple weak letters
- **No semantic/hukm jump** — C2bAdapter never emits `semantic.*` or
  `hukm.*` Evidence kinds

### Other adapters

- **C1Adapter** — encoding/normalization → GRAPHEME/PHONEME Evidence
  - Emits `"encoding.validated"` and `"encoding.normalized"` kinds
  - Operates on plain strings or dict-like objects

- **C2aAdapter** — phonological gates → PHONEME/SYLLABLE Evidence
  - Emits `"phonology.gate_fired"` and
    `"syllable.structure_detected"` kinds
  - Adapts gate traces and syllable structures

- **SyntaxAdapter** — syntactic links → SYNTAX Evidence
  - Emits `"syntax.relation_candidate"` kind
  - Assigns weight by link type (ISNADI > TADMINI > TAQYIDI)
  - Never emits SEMANTICS or HUKM evidence kinds

### CPB validation

All adapter Evidence must pass CPB validation. Example:

```python
from fvafk.algebra import CPB, Domain, Carrier, validate_cpb

# C2bAdapter Evidence validates for MORPH_SURFACE → ROOT bridge
cpb = CPB(name="c2b_bridge", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
carrier = Carrier(domain=Domain.MORPH_SURFACE, value="كاتب", label="كاتب")

result_with_evidence = Result(
    value="كاتب",
    rank=Rank.LICENSED,
    evidence=evidence_tuple,  # from adapter
    trace=Trace(operation="test"),
)

validated = validate_cpb(cpb, carrier, result_with_evidence)
# Passes without fatal failures
```

### Integration with ArabicAlgebraDecisionTree

In Phase 2, the decision tree does **not** consume adapter Evidence
directly (it still uses hand-built fixtures from Phase 1). The adapter
suite provides the **infrastructure** for Phase 3+ to wire real FVAFK
outputs into algebraic operations.

Tests verify that adapter Evidence is **compatible** with the tree's
Result structure:

```python
from fvafk.c2b import RootExtractor
from fvafk.algebra import ArabicAlgebraDecisionTree
from fvafk.algebra.adapters import C2bAdapter

# Extract root using real RootExtractor
extractor = RootExtractor()
extraction_result = extractor.extract_with_affixes("كاتب")

# Adapt to Evidence
adapter = C2bAdapter()
evidence_tuple = adapter.adapt(extraction_result)

# Verify compatibility with decision tree Result
tree = ArabicAlgebraDecisionTree()
tree_result = tree.analyze("كاتب")

# Tree result surface matches extraction
assert tree_result.value.surface == extraction_result.normalized_word

# Adapter evidence cites same root
assert str(extraction_result.root.letters) in evidence_tuple[0].detail
```

### Phase 2 acceptance criteria

✅ All criteria met:

1. Adapters are **read-only** (tests verify no upstream mutation)
2. Adapters emit **Evidence only** (no bare values)
3. All Evidence **cites source** (format: `"c2b:RootExtractionResult:كاتب"`)
4. No **semantic/hukm jump** (forbidden evidence kinds rejected)
5. Evidence **passes CPB validation** (bridge matrix enforced)
6. All **Phase 0, 0.5, 1 tests remain green** (227 tests pass)
7. **30 new Phase 2 tests** cover adapter contracts

---
