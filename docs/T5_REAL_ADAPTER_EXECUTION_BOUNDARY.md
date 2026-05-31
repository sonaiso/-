# T5 Real Adapter Execution Boundary (الاستثناء الدستوري لتنفيذ T5)

**Status:** Constitutional carve-out, ratified alongside PR #152 / #153 / #155.
**Scope:** This document defines the **only** location in `src/` where actual
loading of `transformers` / `torch` and execution of T5 inference is permitted.
**Audience:** Anyone modifying `dal_core/**` or adding ML execution code.

---

## 1. Why this carve-out is required

Up to (and including) the No-Op Adapter Fixtures (PR #153) and the Golden
No-Op Adapter Chain Fixtures (PR #155), the constitution states:

> Adapter contracts declare transformation boundaries.
> Adapter contracts do **NOT** execute transformations.

That law was enforced by `GovernedT5IntegrationSkeleton` via
`FORBIDDEN_EXECUTION_MARKERS` (`src/dal_core/governed_t5_integration_skeleton.py`),
which forbids `import transformers`, `import torch`, `.from_pretrained(`,
`.generate(`, `Trainer(`, etc., **throughout `dal_core`**.

To actually call T5 we need an explicit, narrowly scoped relaxation. This
document records that relaxation as a constitutional act, so reviewers can
verify exactly:

1. **Where** execution is allowed.
2. **What** kind of execution is allowed.
3. **What** remains forbidden, *even inside the carve-out*.
4. **How** the carve-out is mechanically enforced so it cannot leak.

---

## 2. The carve-out (normative)

### 2.1 The one allowed path

Execution of T5 (real `transformers` / `torch` calls) is permitted **only**
inside files matching:

```
src/dal_core/adapters/t5/**
```

Every other path under `src/dal_core/**` remains under the original
`FORBIDDEN_EXECUTION_MARKERS` regime defined in
`governed_t5_integration_skeleton.py`.

### 2.2 What the carve-out permits (inside `adapters/t5/` only)

| Permitted | Notes |
|-----------|-------|
| `import transformers` | Lazy, isolated in `_dependencies.py` |
| `import torch` | Lazy, isolated in `_dependencies.py` |
| `AutoTokenizer.from_pretrained(...)` | Inside `model_loader.py` only |
| `T5ForConditionalGeneration.from_pretrained(...)` | Inside `model_loader.py` only |
| `model.eval()` + `torch.inference_mode()` + `model.generate(...)` | Inside `runner.py` only |
| Tokenizing / decoding as **local variables** | Tokens MUST NOT be persisted into any dataclass that crosses the adapter boundary |

### 2.3 What the carve-out does **NOT** permit (still forbidden, even here)

These remain absolute prohibitions for the entire repository, including
inside the carve-out:

| Forbidden | Constitutional reason |
|-----------|-----------------------|
| Fine-tuning, gradient updates (`loss.backward`, `optimizer.step`, `Trainer(`, `model.train(`) | This carve-out covers **inference only**; training has its own (yet-to-be-ratified) carve-out |
| Storing `tokenizer`, `input_ids`, `attention_mask`, `tensor`, `logits`, etc. as fields of any `@dataclass` that crosses the adapter boundary | `FORBIDDEN_ADAPTER_FIELDS` (see `src/dal_core/t5_adapter_interface_contracts.py`) — `AdapterInput` / `AdapterRawOutput` / `ModelOutput` remain *abstract text only* |
| Rank upgrade, residual resolution, ifādah closure, hukm/reality production, authority claims emitted from model output | `T5OutputAdapter` never produces `Candidate`/`Rank`/`Ifadah`/`Hukm`/`Reality` |
| Returning any `ModelOutput` without passing through `ConstitutionalEvaluationGate` | `T5AdapterRunner.run()` has no code path that bypasses the gate |
| Calling `transformers` / `torch` from any file outside `src/dal_core/adapters/t5/**` | Enforced by `scan_path_for_execution_markers()` and `test_t5_real_adapter_carveout.py` |

### 2.4 Constitutional formula (unchanged from PR #152)

```
TrainingExample
    → T5InputAdapter.prepare_input → AdapterInput        (abstract text)
    → T5AdapterRunner (tokenize → model.generate → decode, all LOCAL)
    → AdapterRawOutput                                   (abstract text)
    → T5OutputAdapter.parse_output → ModelOutput
    → ConstitutionalEvaluationGate.evaluate              (MANDATORY)
    → EvaluatedModelOutput
```

The shape of `AdapterInput` / `AdapterRawOutput` / `ModelOutput` defined by
PR #152 is **unchanged**. Tokens and tensors live only as local variables
inside `runner.py`; they never enter the dataclasses.

---

## 3. Mechanical enforcement

The carve-out is enforced by three independent mechanisms:

### 3.1 Path-aware scanner (`scan_path_for_execution_markers`)

`src/dal_core/governed_t5_integration_skeleton.py` exposes a *new*
function `scan_path_for_execution_markers(path, text)`:

* If `path` is inside `src/dal_core/adapters/t5/`, the scanner returns an
  empty tuple (carve-out applies).
* Otherwise it delegates to the existing
  `scan_for_execution_markers(text)` (the original strict behaviour from
  PR #150 is preserved bit-for-bit).

The original `scan_for_execution_markers(text)` is untouched. No existing
test or caller changes behaviour.

### 3.2 Repository-wide scope test

`tests/dal_core/test_t5_real_adapter_carveout.py` walks the source tree and
asserts:

1. No file under `src/dal_core/` *outside* `adapters/t5/` contains a
   `FORBIDDEN_EXECUTION_MARKERS` substring (in code).
2. The carve-out function is a *path* filter only — text outside the
   allowed path is still scanned strictly.

If anyone adds `import transformers` to (say) `case_signs.py`, this test
fails CI immediately.

### 3.3 Optional dependency

`transformers` / `torch` are declared as an **optional** dependency in
`pyproject.toml` under `[project.optional-dependencies] t5 = [...]`.
Users of `bayan-fvafk` who do not install `.[t5]` cannot accidentally
execute the adapter; `_dependencies._require_t5_runtime()` raises a
clear `T5RuntimeUnavailableError`.

---

## 4. Relationship to prior constitutional documents

| Document | Status after this carve-out |
|----------|------------------------------|
| `GOVERNED_T5_INTEGRATION_SKELETON.md` (PR #150) | Unchanged. Still defines the strict default. The carve-out is the **only** documented exception. |
| `T5_ADAPTER_INTERFACE_CONTRACTS.md` (PR #152) | Unchanged. `T5InputAdapter` / `T5OutputAdapter` must satisfy these contracts. |
| `NOOP_ADAPTER_FIXTURES.md` (PR #153) | Unchanged. No-op fixtures remain the contract conformance witness without `transformers`. |
| `GOLDEN_NOOP_ADAPTER_CHAINS.md` (PR #155) | Unchanged. Golden chains keep proving deterministic binding preservation. |
| `CONSTITUTIONAL_EVALUATION_HARNESS.md` (PR #147) | Now invoked as a **mandatory** post-step on every real T5 output via `ConstitutionalEvaluationGate`. |

---

## 5. Supreme law

> **Execution of T5 is permitted only inside `src/dal_core/adapters/t5/`,
> only for inference, only with abstract-text dataclasses crossing the
> boundary, and only when every output is gated through
> `ConstitutionalEvaluator`. Any other use is a constitutional violation.**

Reference:
* User requirement (2026-05-31): "بناء أول T5 Input/Output Adapter حقيقي
  يستوفي عقود PR #152 ويستدعي transformers فعلاً — يبقى داخل
  `dal_core/adapters/t5/` مع تشغيل `ConstitutionalEvaluator` على كل خرج."
* Builds on PR #147, PR #150, PR #152, PR #153, PR #155.
