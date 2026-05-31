# T5 Real Adapter — `dal_core.adapters.t5`

**Status:** First real T5 Input/Output adapter (inference only).
**Carve-out:** See [`T5_REAL_ADAPTER_EXECUTION_BOUNDARY.md`](./T5_REAL_ADAPTER_EXECUTION_BOUNDARY.md)
for the constitutional basis. This is the **only** location in `src/dal_core/`
where `transformers` and `torch` may be imported and where real T5 inference
may execute.

---

## 1. What this adapter is

`dal_core.adapters.t5` is a thin, governed wrapper around Hugging Face's
`AutoModelForSeq2SeqLM` (T5 / Flan-T5 / mT5 family) that satisfies the
PR #152 adapter interface contracts and routes **every** model output
through `ConstitutionalEvaluator` (PR #147) before returning it.

It does:

* `prepare_input(TrainingExample) → AdapterInput` (abstract text only)
* tokenize → `model.generate()` → decode, **all as local variables** inside
  `runner.py`
* `parse_output(AdapterRawOutput) → ModelOutput`
* `ConstitutionalEvaluationGate.evaluate(ModelOutput, TrainingExample) → EvaluatedModelOutput`

It deliberately does **not**:

* fine-tune, train, or backpropagate anything
* compute metrics or quality scores
* upgrade rank / resolve residuals / close ifādah / produce hukm / reality
* expose tokens, tensors, logits or any other ML internals on the
  dataclasses that cross the adapter boundary
* call `transformers` / `torch` from any file outside
  `src/dal_core/adapters/t5/**`

---

## 2. Public surface

```python
from dal_core.adapters.t5 import (
    T5AdapterConfig,
    EvaluationMode,
    T5InputAdapter,
    T5OutputAdapter,
    ConstitutionalEvaluationGate,
    EvaluatedModelOutput,
    T5ConstitutionalViolationError,
    T5AdapterRunner,
    T5AdapterError,
    T5RuntimeUnavailableError,
    is_t5_runtime_available,
)
```

| Symbol | Purpose |
|--------|---------|
| `T5AdapterConfig` | Frozen integration config (model name, device, prompt prefix, generation kwargs, evaluation mode). |
| `EvaluationMode` | `STRICT` (raise on CRITICAL violations) / `OBSERVE` (return report). |
| `T5InputAdapter` | `InputAdapterContract` implementation. |
| `T5OutputAdapter` | `OutputAdapterContract` implementation. |
| `ConstitutionalEvaluationGate` | Mandatory post-step; delegates to `ConstitutionalEvaluator`. |
| `EvaluatedModelOutput` | Frozen bundle of `ModelOutput + ConstitutionalViolationReport + mode`. |
| `T5ConstitutionalViolationError` | Raised by the gate in `STRICT` mode. Carries the report and the offending output. |
| `T5AdapterRunner` | End-to-end orchestrator. The only path that can produce a `ModelOutput`. |
| `T5AdapterError` | Structural/boundary error (e.g. `validate_input` failed). |
| `T5RuntimeUnavailableError` | Raised when the optional `[t5]` extra is not installed. |
| `is_t5_runtime_available()` | Cheap, side-effect free probe. |

---

## 3. Installation

The adapter ships as an **optional extra**. The rest of `bayan-fvafk`
keeps working without it.

```bash
pip install -e .[t5]
```

That installs `transformers`, `torch`, and `sentencepiece`. If the extra
is missing, *importing* the adapter package is fine, but calling
`T5AdapterRunner.run(...)` raises `T5RuntimeUnavailableError` with a
hint to install the extra.

---

## 4. Minimal usage example

```python
from dal_core.adapters.t5 import (
    EvaluationMode,
    T5AdapterConfig,
    T5AdapterRunner,
)
from dal_core.training_example import TrainingExample
from dal_core.trace_explanation_dataset_generator import (
    OutputType, ValidationStatus,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation

cfg = T5AdapterConfig(
    model_name="google/flan-t5-small",
    device="cpu",
    max_input_tokens=256,
    max_output_tokens=64,
    prompt_prefix="explain trace step: ",
    evaluation_mode=EvaluationMode.STRICT,
)
runner = T5AdapterRunner(config=cfg)

example = TrainingExample(
    training_example_id="ex_001",
    source_dataset_row_id="row_001",
    source_trace_id="trace_001",
    source_algorithm="MufradAcceptanceEquation",
    operation=TraceConsumerOperation.EXPLAIN_TRACE,
    input_text="T1 produces candidate_a1.",
    target_text="T1 emitted candidate_a1.",
    referenced_candidate_ids=("candidate_a1",),
    referenced_residual_ids=(),
    referenced_gate_ids=(),
    referenced_rank_values=(),
    output_type=OutputType.EXPLANATION,
    requires_algorithm_rerun=False,
    validation_status=ValidationStatus.VALID,
)

evaluated = runner.run(example)

print(evaluated.model_output.predicted_text)
print("passed:", evaluated.report.passed)
print("critical:", evaluated.report.critical_violations_count)
```

### What happens if the model output is forbidden?

In `STRICT` mode (default), a model output containing forbidden phrases
like *"final answer"*, *"correct analysis"*, *"gold_label_hukm"*, etc.,
or that drops a `source_trace_id` binding, causes
`T5ConstitutionalViolationError` to be raised. The exception carries
both the full `ConstitutionalViolationReport` and the offending
`ModelOutput` for forensic inspection:

```python
try:
    evaluated = runner.run(example)
except T5ConstitutionalViolationError as err:
    print("Rejected:", err)
    for v in err.critical_violations:
        print("  -", v.violation_type.name, v.detected_phrase)
```

In `OBSERVE` mode the same case returns an `EvaluatedModelOutput` with
`report.passed == False` and the violations attached.

---

## 5. End-to-end data flow

```
TrainingExample (PR #146)
  │
  ▼
T5InputAdapter.prepare_input        ──→  AdapterInput   (PR #152: abstract text)
  │                                       │
  │                                       ▼
  │                              T5InputAdapter.validate_input
  │                                       │  is_valid? → else T5AdapterError
  ▼
runner._infer  (LOCAL: tokenizer + model.generate + decode, torch.inference_mode)
  │
  ▼
AdapterRawOutput   (PR #152: abstract text)
  │
  ▼
T5OutputAdapter.parse_output        ──→  ModelOutput    (PR #147)
  │                                       │
  │                                       ▼
  │                              T5OutputAdapter.validate_output
  │                                       │  is_valid? → else T5AdapterError
  ▼
ConstitutionalEvaluationGate.evaluate     (PR #147 ConstitutionalEvaluator)
  │
  │  STRICT and critical_violations_count > 0  ──→ raise T5ConstitutionalViolationError
  │  otherwise
  ▼
EvaluatedModelOutput   (ModelOutput + ConstitutionalViolationReport + mode)
```

The runner has **no** code path that emits an `EvaluatedModelOutput` (or
a `ModelOutput`) without passing through `ConstitutionalEvaluationGate`.

---

## 6. Behavioral boundaries (what stays forbidden, even here)

| Forbidden | Why it stays forbidden |
|-----------|------------------------|
| Fine-tuning / `Trainer(` / `loss.backward()` / `optimizer.step()` | Carve-out covers inference only. Training carve-out is a future, separately ratified document. |
| Storing tokenizer / tensors / logits as fields of `AdapterInput`, `AdapterRawOutput`, `ModelOutput` | These dataclasses remain *abstract text only*; tokens live as local variables inside `runner.py`. Enforced by `FORBIDDEN_ADAPTER_FIELDS` checks. |
| Emitting `Candidate`, `Rank`, `Ifādah`, `Hukm`, `Reality` from model output | `T5OutputAdapter` never produces those; `ConstitutionalEvaluator` detects authority claims and the gate raises. |
| Bypassing the gate | The runner's `run()` and `run_batch()` are the only public entry points and both terminate at the gate. |
| Importing `transformers` / `torch` outside `src/dal_core/adapters/t5/` | Enforced by `test_t5_real_adapter_carveout.py` (CI fails otherwise). |
| Authority phrases in `predicted_text` while in `STRICT` mode | Raised as `T5ConstitutionalViolationError`; output is not surfaced through `run()`. |

---

## 7. Testing

| Test file | Requires `[t5]`? | Purpose |
|-----------|------------------|---------|
| `tests/dal_core/test_t5_real_adapter_carveout.py` | No | Audits the source tree and the path-aware scanner. |
| `tests/dal_core/adapters/t5/test_config.py` | No | `T5AdapterConfig` validation and decoding. |
| `tests/dal_core/adapters/t5/test_dependencies.py` | No | `T5RuntimeUnavailableError` + lazy import contract. |
| `tests/dal_core/adapters/t5/test_adapters.py` | No | `T5InputAdapter` / `T5OutputAdapter` behaviour on plain strings. |
| `tests/dal_core/adapters/t5/test_evaluation_gate.py` | No | `STRICT` / `OBSERVE` enforcement against forged `ModelOutput`s. |
| `tests/dal_core/adapters/t5/test_runner_t5.py` | **Yes** (`pytest -m t5`) | Real inference end-to-end; binding preservation; no tensor leak. |

Run the no-t5 layer:

```bash
pytest -m "not t5" tests/dal_core/adapters tests/dal_core/test_t5_real_adapter_carveout.py
```

Run the real-inference layer (requires `[t5]`):

```bash
pip install -e .[t5]
pytest -m t5
```

---

## 8. Supreme law (recap)

> Execution of T5 is permitted only inside `src/dal_core/adapters/t5/`,
> only for inference, only with abstract-text dataclasses crossing the
> boundary, and only when every output is gated through
> `ConstitutionalEvaluator`. Any other use is a constitutional
> violation.

See [`T5_REAL_ADAPTER_EXECUTION_BOUNDARY.md`](./T5_REAL_ADAPTER_EXECUTION_BOUNDARY.md)
for the carve-out, [`T5_ADAPTER_INTERFACE_CONTRACTS.md`](./T5_ADAPTER_INTERFACE_CONTRACTS.md)
for the contracts this adapter implements, and
[`CONSTITUTIONAL_EVALUATION_HARNESS.md`](./CONSTITUTIONAL_EVALUATION_HARNESS.md)
for the evaluator the gate invokes.
