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
