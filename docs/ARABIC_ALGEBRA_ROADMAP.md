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

## Phase 1 — Decision-tree surface coverage ✅ (PR #37)

Extend `ArabicAlgebraDecisionTree` from the Phase-0 illustrative table
to cover the wazn families already documented under `awzan-claude-atwah.csv`
and `src/fvafk/c2b/pattern_catalog.py`. Still no coupling to
`RootExtractor`: the goal is to verify the algebra holds at scale on
hand-built fixtures.

**Status.** Implemented via PR #37. The Phase-1 catalog covers nine
wazn families — `فاعل`, `مفعول`, `فعّال`, `مفعال`, `مِفعل`, `مَفعل`,
`فعلة`, `فعول`, `فعيل` — with hand-built fixtures under
`tests/fixtures/algebra/wazn_surface_cases.json`. Every covered
surface returns `Rank.LICENSED` with explicit residuals
(`context.absent`, `lexical.ambiguity`, plus per-family/per-token
hints such as `transfer.possible`, `proper_name.possible`,
`pattern.collision`); none ever reaches `CERTIFIED` and none emits a
`semantic.*` or `hukm.*` evidence kind. The neighbouring families
`فِعال` and `فُعَل` are deliberately out of scope and reserved for
Phase 1.5.

**Touches.** `decision_tree.py`; new fixtures under
`tests/fixtures/algebra/`.

---

## Phase 2 — Wire `c1` / `c2a` / `c2b` / `syntax` as `Evidence` sources ✅ (this PR)

Introduce `src/fvafk/algebra/adapters/` with thin wrappers that take the
existing dataclasses (`MorphologicalAnalysis`, `WordForm`,
`RootExtractionResult`, syntax links) and emit `Evidence` whose
`source` cites the original analysis. **No FVAFK code is modified**;
the adapters are pure read-only translators.

**Status.** Implemented via this PR. The Phase-2 adapter suite provides:

- `BaseAdapter` — immutable base class enforcing read-only contract
- `C1Adapter` — encoding/normalization → GRAPHEME/PHONEME Evidence
- `C2aAdapter` — phonological gates → PHONEME/SYLLABLE Evidence
- `C2bAdapter` — RootExtractor → ROOT Evidence (primary use case)
- `SyntaxAdapter` — syntactic links → SYNTAX Evidence

All adapters:
- Are **read-only**: never mutate upstream objects
- Emit **Evidence only**: no bare values, no direct Rank promotions
- Cite **sources**: every Evidence references upstream object via
  `source` field (format: `"<module>:<type>:<id>"`)
- Respect **domain boundaries**: no `MORPH_SURFACE → SEMANTICS` or
  `MORPH_DEEP → HUKM` jumps
- Pass **CPB validation**: all Evidence validates against bridge matrix

**Deliverables.**
- `src/fvafk/algebra/adapters/{__init__,common,c1_adapter,c2a_adapter,c2b_adapter,syntax_adapter}.py`
- `tests/test_algebra_adapters_phase2.py` — 30 tests covering adapter
  contracts, immutability, CPB compliance, and domain boundary
  enforcement
- `docs/ARABIC_ALGEBRA_ROADMAP.md` and
  `docs/ARABIC_ALGEBRA_DECISION_TREE.md` updated

**Exit criterion.** ✅ `ArabicAlgebraDecisionTree.analyze("كاتب")` can
optionally consume adapter Evidence (tests verify Evidence is
compatible with tree's Result structure); RootExtractor evidence cites
real `RootExtractionResult` id; all Phase 0, 0.5, 1 tests remain green;
no direct `MORPH_SURFACE → SEMANTICS` / `HUKM` jump; CPB validation
passes.

**Touches.** New `src/fvafk/algebra/adapters/` module; new tests;
documentation updates. **No changes to c1, c2a, c2b, syntax, dal_core,
core.py, cpb.py, policies.py, or arabic_layers.py.**

---

## Phase 3 — Algebraic morphology ✅ (this PR)

Promote morphology operations (pattern matching, root extraction,
broken-plural derivation, augmentation operators) from "functions that
return values" to first-class `Operation` instances. Each is gated by
a CPB declaring `MORPH_SURFACE → ROOT` or `ROOT → MORPH_DEEP`.

**Goal.** Transform morphology from plain functions into governed
algebraic operations that produce Result objects with full provenance:
`value + rank + evidence + residuals + failures + replay`.

**Status.** Implemented via this PR. Phase 3 morphology suite provides:

- `MORPHOLOGY_RESIDUAL_KINDS` — 9 morphology-specific residual kinds
  (context.absent, lexical.ambiguity, proper_name.possible,
  transfer.possible, weak_letter.present, affix.aggressive_strip,
  root.ambiguous, pattern.collision, broken_plural.possible)
- `PatternMatchOperation` — MORPH_SURFACE → MORPH_SURFACE Result
- `RootExtractionOperation` — MORPH_SURFACE → ROOT Result
- `AffixDetectionOperation` — MORPH_SURFACE → MORPH_SURFACE Result
  with affix residuals
- Convenience wrappers: `governed_pattern_match()`,
  `governed_root_extract()`, `governed_affix_detect()`

All operations:
- **License structure, not meaning** (الصرف يرخص بنية، ولا يصدر حكماً)
- **Root is not meaning** (الجذر ليس معنى): ROOT evidence never
  claims SEMANTICS or HUKM
- **Pattern is not judgment** (الوزن ليس حكماً): Pattern matching
  stays LICENSED when residuals remain
- **Never promote to CERTIFIED with residuals**: All morphology
  operations emit residuals for context absence, ambiguity, weak
  letters, aggressive affix stripping
- **Full provenance**: Every Result includes trace, evidence, residuals

**Deliverables.**
- `src/fvafk/algebra/morphology/{__init__,residual_taxonomy,operations}.py`
- `tests/test_algebra_morphology_phase3.py` — 33 tests covering
  residual taxonomy, governed operations, evidence integration, domain
  boundary enforcement, rank invariants, and regression tests
- `docs/ARABIC_ALGEBRA_ROADMAP.md` updated

**Exit criterion.** ✅ All 33 Phase 3 tests pass; root extraction with
Evidence promotes to LICENSED (never CERTIFIED with residuals); weak
letters create `weak_letter.present` residual; aggressive affix
stripping creates `affix.aggressive_strip` residual; fatal
contradiction forces REFUTED; all Phase 0, 0.5, 1, 2 tests remain green
(63 total passing); no MORPH_SURFACE → SEMANTICS or MORPH_DEEP → HUKM
jump; morphology operations never emit `semantic.*` or `hukm.*`
evidence kinds.

**Touches.** New `src/fvafk/algebra/morphology/` module; new tests;
documentation updates. **No changes to c1, c2a, c2b, syntax, dal_core,
core.py, cpb.py, policies.py, or arabic_layers.py.**

---

## Phase 4 — Algebraic syntax ✅ (this PR)

**Goal.** Transform syntax operations from plain analysis into governed
algebraic operations that produce `Result` with full provenance.

**Deliverables.**
- `src/fvafk/algebra/syntax/{__init__,residual_taxonomy,operations}.py`
- `tests/test_algebra_syntax_phase4.py`
- `docs/PHASE4_ALGEBRAIC_SYNTAX_SUMMARY.md`

**Status.** Implemented via this PR. Phase 4 syntax suite provides:

1. **Five governed syntax operations** that return `Result`:
   - `MabniClosedOperatorOperation` (مبني: لم، إن، من...)
   - `MurabOpenCarrierOperation` (معرب: open relational carriers)
   - `AmilFunctionOperation` (عامل: governor functions)
   - `IrabRelationEffectOperation` (إعراب: case as relational effect)
   - `NisbahBindingOperation` (نسبة: ISN/TADMN/TAQYID bindings)

2. **Ten syntax residual kinds** covering:
   - `syntax.context_absent` — Surrounding tokens needed
   - `syntax.operator_scope_unresolved` — Operator scope undetermined
   - `syntax.case_missing` / `case_estimated` / `case_ambiguous` — Case marks
   - `syntax.governor_ambiguous` — Multiple عامل candidates
   - `syntax.ellipsis_possible` — Possible حذف
   - `syntax.attachment_ambiguous` — Unclear attachment
   - `syntax.relation_candidate` — Relation type not finalized
   - `syntax.word_order_ambiguous` — Multiple interpretations

3. **Domain boundaries enforced**:
   - No `SYNTAX → HUKM` jump
   - No `SYNTAX → SEMANTICS` certification with residuals
   - Syntax operations never emit `semantic.*` or `hukm.*` evidence

4. **Core principle**: النحو الجبري يرخص علاقة تركيبية، لا يحكم بالمعنى النهائي
   (Syntax licenses relational structure, does not judge final meaning)

**Exit criterion.** ✅ All 43 Phase 4 tests pass; syntax operations stay
LICENSED when residuals remain; no SYNTAX → HUKM jump; all Phase 0-3
tests remain green.

---

## Phase 5 — Dāl/Madlūl/Dalālah/Ifādah Algebra (Semantic Layers) ✅ (merged via PR #41)

**Critical Insight**: Semantics is not a single layer. Before ifādah (semantic
completion) can be achieved, we must establish:

1. **Dāl algebra** (signifier alone - linguistic carrier)
2. **Madlūl algebra** (signified alone - possible meanings)
3. **Wadh' contract** (signifier-signified binding)
4. **Dalālah gates** (semantic relations: mutābaqah, taḍammun, iltizām)
5. **Nisbah algebra** (compositional semantics)
6. **Ifādah closure** (complete statement)
7. **Judgment boundary** (prevent premature HUKM)

> **Core Principle**: الإفادة لا تبدأ من النحو مباشرة ولا من المعجم مباشرة
>
> (Ifādah does not begin directly from syntax or directly from lexicon.
> It requires intermediate layers of dāl, madlūl, binding, and dalālah.)

### Phase 5A — Dāl Algebra (Signifier Candidates)

**Goal**: Represent signifier alone as governed candidate (not meaning).

**Deliverables**:
- `src/fvafk/algebra/semantics/dal_candidates.py`
- Dāl candidate structure with residuals (polysemy.possible, context.absent)
- No semantic interpretation at this layer

**Key Law**: الدال وحده ليس معنى (Dāl alone is not meaning)

---

### Phase 5B — Madlūl Algebra (Signified Candidates)

**Goal**: Represent possible signifieds as candidates (not dalālah).

**Deliverables**:
- `src/fvafk/algebra/semantics/madlul_candidates.py`
- Multiple madlūl candidates per dāl
- Residuals: dal_binding.absent

**Key Law**: المدلول وحده ليس دلالة (Madlūl alone is not dalālah)

---

### Phase 5C — Dāl/Madlūl Binding (Wadh' Contract)

**Goal**: License transition from signifier to signified through wadh'/usage.

**Deliverables**:
- `src/fvafk/algebra/semantics/wadh_binding.py`
- Binding operation: Dāl + Madlūl + Evidence → Licensed binding
- Evidence types: lexical attestation, conventional usage, context

**Key Law**: لا دلالة بلا ربط (No dalālah without binding)

**Maps to**: A5 in PROJECT_ALGEBRA_ARCHITECTURE_MAP.md

---

### Phase 5D — Individual Dalālah Gates

**Goal**: Implement three classical semantic relations as **pre-ifādah conditions**.

**Deliverables**:
- `src/fvafk/algebra/semantics/dalalah_gates.py`
- `MutabaqahGate` — Direct correspondence (word → total meaning)
- `TadammunGate` — Partial inclusion (word → part of meaning)
- `IltizamGate` — Entailment (word → necessary consequence)

**Critical Rules**:
- Mutābaqah alone does NOT produce ifādah
- Taḍammun alone does NOT produce ifādah
- Iltizām requires explicit gate (not automatic)
- All three are **شروط غير موجبة** (necessary but not sufficient conditions)

**Key Law**: المطابقة والتضمن والالتزام قبل الإفادة (Mutābaqah, taḍammun,
iltizām are before ifādah, not ifādah itself)

**Maps to**: A7 in PROJECT_ALGEBRA_ARCHITECTURE_MAP.md

---

### Phase 5E — Nisbah Algebra (Compositional Semantics)

**Goal**: Distinguish relations that can produce ifādah from those that cannot.

**Deliverables**:
- `src/fvafk/algebra/semantics/nisbah_semantic.py`
- Semantic composition from Phase 4 syntactic nisbah
- Isnadi relation → ifādah candidate
- Iḍāfah relation alone → NOT ifādah
- Taqyīd relation alone → NOT ifādah (until complete predication)

**Key Laws**:
- النسبة الإضافية لا تصبح إفادة (Iḍāfah relation alone does not become ifādah)
- الشرط بلا جواب لا يصبح إفادة (Conditional without jawāb does not become ifādah)

---

### Phase 5F — Reference and Completion

**Goal**: Resolve anaphora, ellipsis, and incomplete structures.

**Deliverables**:
- `src/fvafk/algebra/semantics/reference_resolution.py`
- Pronoun resolution (requires referent)
- Demonstrative resolution
- Relative clause resolution
- Ellipsis handling
- Conditional jawāb requirement

**Key Law**: الضمير بلا مرجع لا يصبح إفادة معتمدة
(Pronoun without referent cannot produce CERTIFIED ifādah)

---

### Phase 5G — Speech Force (Illocutionary Force)

**Goal**: Detect speech act type without issuing HUKM.

**Deliverables**:
- `src/fvafk/algebra/semantics/speech_force.py`
- Speech force types: khabar, inshā, amr, nahy, istifhām, shart, nidā,
  tamannī, tarjjī, taʿajjub
- Force detection from markers and structure

**Critical Rules**:
- Khabar does NOT become final HUKM
- Inshā does NOT become legal judgment
- Istifhām does NOT become denial without qarīnah
- Amr does NOT become obligation at this layer
- Nahy does NOT become prohibition at this layer

**Maps to**: Partial A8 in PROJECT_ALGEBRA_ARCHITECTURE_MAP.md

---

### Phase 5H — Ifādah Closure

**Goal**: Close semantic completion with full residual accounting.

**Deliverables**:
- `src/fvafk/algebra/semantics/ifadah_closure.py`
- Ifādah requires ALL of:
  1. Licensed parties
  2. Licensed dāl/madlūl binding
  3. Licensed dalālah (mutābaqah/taḍammun/iltizām)
  4. Licensed nisbah
  5. Complete structure
  6. Resolved references or residuals
  7. Known speech force or residual
  8. Full residual accounting

**Rank Rules**:
- Ifādah with residuals → LICENSED only
- Ifādah without residuals + full evidence → CERTIFIED
- Incomplete ifādah → CANDIDATE

**Maps to**: Partial A9 in PROJECT_ALGEBRA_ARCHITECTURE_MAP.md

---

### Phase 5I — Judgment Boundary Guard

**Goal**: Prevent any SEMANTICS → HUKM or IFADAH → HUKM jump.

**Deliverables**:
- `src/fvafk/algebra/semantics/boundary_guards.py`
- Hard gates preventing:
  - Direct SEMANTICS → HUKM certification
  - Direct IFADAH → HUKM inference
  - Bypassing murad layer (A9)

**Test Requirements**:
- Every forbidden jump must fail
- Every incomplete structure must remain residual-bearing
- HUKM is Phase 6 (future, separate algebra)

**Maps to**: A9/A10 boundary in PROJECT_ALGEBRA_ARCHITECTURE_MAP.md

---

### Phase 5 Hard Gates (All Subphases)

These gates must be enforced across all Phase 5 subphases:

```python
# Dāl/Madlūl separation
assert dāl_alone_is_not_meaning()
assert madlūl_alone_is_not_dalālah()
assert dāl_madlūl_binding_required()

# Dalālah gates
assert mutābaqah_is_not_ifādah()
assert taḍammun_is_not_ifādah()
assert iltizām_requires_gate()  # Not automatic

# Nisbah gates
assert iḍāfah_alone_is_not_ifādah()
assert taqyīd_alone_is_not_ifādah()
assert conditional_without_jawāb_is_not_ifādah()

# Reference gates
assert pronoun_without_referent_cannot_certify_ifādah()

# Speech force gates
assert khabar_is_not_hukm()
assert amr_is_not_obligation_at_phase5()
assert nahy_is_not_prohibition_at_phase5()

# Boundary gates
assert ifādah_with_residuals_cannot_certify()
assert semantics_cannot_jump_to_hukm()
assert ifādah_cannot_issue_hukm()
```

---

> **Note.** This phase must respect the
> [`dal_core` meaning-field prohibition](SPEC_DAL_CORE.md): no leakage
> of `meaning` / `murad` / `haqiqa_majaz` fields into the `MORPH_*` or
> `SYNTAX` domains.
>
> **Architecture Mapping**: Phase 5A-5I implements layers A5-A9 from
> `PROJECT_ALGEBRA_ARCHITECTURE_MAP.md`. See that document for the
> complete 11-layer architecture (A0-A10).

---

## Phase 5.5 — Semantic Boundary Hardening (this PR)

**Goal.** Lock the merged Phase 5 semantic algebra so future PRs cannot silently
violate the boundaries between dāl, madlūl, dalālah, ifādah, and HUKM.
No production code changes; only tests + docs.

**Deliverables.**
- `tests/fvafk/algebra/test_semantic_boundary_hardening.py` — 14 tests covering
  gates 1-11 (dāl/madlūl separation, dalālah enforcement, nisbah insufficiency,
  reference completion)
- `tests/fvafk/algebra/test_ifadah_forbidden_jumps.py` — 14 tests covering
  gates 12-17 (speech force boundaries, domain jump prevention)
- `docs/PHASE5_5_SEMANTIC_BOUNDARY_HARDENING.md` — Complete hardening
  documentation with rationale, threat model, 17 hard gates, mutation testing
  strategy, and CI integration guide
- `docs/ARABIC_ALGEBRA_ROADMAP.md` — Updated to mark Phase 5.5

**17 Hard Gates Enforced:**
1. Dāl alone never becomes meaning (الدال وحده ليس معنى)
2. Madlūl alone never becomes dalālah (المدلول وحده ليس دلالة)
3. Dāl/Madlūl binding required before dalālah (لا دلالة بلا ربط)
4. Mutābaqah alone does not become ifādah (المطابقة لا تصبح إفادة وحدها)
5. Taḍammun alone does not become ifādah (التضمن لا يصبح إفادة وحده)
6. Iltizām without gate is not licensed (الالتزام ليس تلقائياً)
7. Majāz without qarīnah is not licensed (المجاز بلا قرينة ليس مرخصاً)
8. Idāfah alone does not become ifādah (النسبة الإضافية لا تصبح إفادة)
9. Taqyīd alone does not become ifādah (التقييد لا يصبح إفادة حتى يكمل الإسناد)
10. Conditional without jawāb does not become ifādah (الشرط بلا جواب لا يصبح إفادة)
11. Pronoun without referent cannot certify ifādah (الضمير بلا مرجع لا يصبح إفادة معتمدة)
12. Khabar does not become HUKM (الخبر ليس حكماً)
13. Amr does not become obligation in Phase 5 (الأمر ليس وجوباً في Phase 5)
14. Nahy does not become prohibition in Phase 5 (النهي ليس حراماً/فساداً في Phase 5)
15. Ifādah with residuals cannot become CERTIFIED (الإفادة ذات البقايا لا تُعتَمد)
16. SEMANTICS cannot jump to HUKM (SEMANTICS لا يقفز إلى HUKM)
17. IFADAH cannot issue HUKM (الإفادة لا تُصدِر حكماً)

**Mutation Resistance:**
- Tests fail if developer removes residual kinds
- Tests fail if developer bypasses evidence requirements
- Tests fail if developer emits `hukm.*` evidence from semantic operations
- Tests fail if developer allows SEMANTICS → HUKM bridge
- Tests fail if developer certifies ifādah with residuals

**Exit criterion.** All 28 Phase 5.5 tests pass; all Phase 0-5 tests remain
green; no production code changes; the 17 hard gates are pinned by tests.
**Phase 5 is merged and hardened; the next substantive milestone is Phase 6 HUKM.**

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
