"""
Real-inference tests for :class:`T5AdapterRunner`.

These tests load a small Hugging Face checkpoint and run actual T5
inference. They are gated behind ``@pytest.mark.t5`` so the default CI
job (``pytest -m "not t5"``) does not require ``transformers`` / ``torch``.

Run them locally with::

    pip install -e .[t5]
    pytest -m t5
"""
from __future__ import annotations

import os

import pytest

from dal_core.adapters.t5 import (
    ConstitutionalEvaluationGate,
    EvaluatedModelOutput,
    EvaluationMode,
    T5AdapterConfig,
    T5AdapterRunner,
    T5ConstitutionalViolationError,
    is_t5_runtime_available,
)
from dal_core.adapters.t5.model_loader import T5ModelLoader

from ._helpers import make_training_example


pytestmark = pytest.mark.t5

if not is_t5_runtime_available():
    pytest.skip(
        "Optional [t5] extra not installed; skipping real T5 inference tests.",
        allow_module_level=True,
    )


# The smallest T5 we can realistically run on CPU.
_DEFAULT_TEST_MODEL = os.environ.get("T5_TEST_MODEL", "google/flan-t5-small")


@pytest.fixture(scope="module")
def runner_strict() -> T5AdapterRunner:
    cfg = T5AdapterConfig(
        model_name=_DEFAULT_TEST_MODEL,
        max_input_tokens=64,
        max_output_tokens=16,
        device="cpu",
        evaluation_mode=EvaluationMode.STRICT,
        prompt_prefix="translate English to German: ",
    )
    runner = T5AdapterRunner(config=cfg)
    yield runner
    T5ModelLoader.clear()


def test_runs_real_inference_and_passes_gate(runner_strict: T5AdapterRunner):
    example = make_training_example(
        training_example_id="ex_real_001",
        source_trace_id="trace_real_001",
        input_text="Hello, world.",
    )
    evaluated = runner_strict.run(example)
    assert isinstance(evaluated, EvaluatedModelOutput)
    # Bindings preserved end-to-end
    assert evaluated.model_output.source_training_example_id == example.training_example_id
    assert evaluated.model_output.source_trace_id == example.source_trace_id
    # Model produced *some* text
    assert evaluated.model_output.predicted_text.strip() != ""
    # Report attached and passed (no authority violation expected for a translation)
    assert evaluated.report.model_output_id == evaluated.model_output.model_output_id
    assert evaluated.report.passed


def test_strict_gate_blocks_authority_via_observe_then_strict():
    """We cannot reliably force T5 to say a forbidden phrase; instead we
    replay the same flow through an OBSERVE gate followed by an explicit
    STRICT evaluation on a doctored output to assert the gate's
    contractual behaviour with real-runner-shaped data."""

    cfg = T5AdapterConfig(
        model_name=_DEFAULT_TEST_MODEL,
        max_input_tokens=32,
        max_output_tokens=8,
        device="cpu",
        evaluation_mode=EvaluationMode.OBSERVE,
        prompt_prefix="translate English to German: ",
    )
    runner = T5AdapterRunner(config=cfg)

    example = make_training_example(input_text="cat")
    evaluated = runner.run(example)
    assert evaluated.report is not None  # OBSERVE returned even if not passed

    # Now reuse the gate with STRICT semantics on a deliberately doctored
    # ModelOutput carrying an authority claim to prove STRICT raises.
    from dal_core.model_output import ModelOutput
    doctored = ModelOutput(
        model_output_id="doctored_001",
        source_training_example_id=example.training_example_id,
        source_trace_id=example.source_trace_id,
        predicted_text="The final answer: cat → Katze. Correct analysis.",
        model_name="t5-doctored",
        generation_timestamp="2026-05-31T00:00:00Z",
    )
    strict_gate = ConstitutionalEvaluationGate(mode=EvaluationMode.STRICT)
    with pytest.raises(T5ConstitutionalViolationError):
        strict_gate.evaluate(doctored, example)


def test_run_batch_preserves_bindings(runner_strict: T5AdapterRunner):
    examples = tuple(
        make_training_example(
            training_example_id=f"ex_batch_{i}",
            source_trace_id=f"trace_batch_{i}",
            input_text=f"Sentence number {i}.",
        )
        for i in range(2)
    )
    results = runner_strict.run_batch(examples)
    assert len(results) == 2
    for example, evaluated in zip(examples, results):
        assert (
            evaluated.model_output.source_training_example_id
            == example.training_example_id
        )
        assert evaluated.model_output.source_trace_id == example.source_trace_id


def test_no_forbidden_fields_leak_into_model_output(runner_strict: T5AdapterRunner):
    """The dataclasses crossing the boundary stay tensor-free."""
    import dataclasses as _dc
    from dal_core.t5_adapter_interface_contracts import FORBIDDEN_ADAPTER_FIELDS

    example = make_training_example(input_text="Hello")
    evaluated = runner_strict.run(example)

    model_output_fields = {f.name for f in _dc.fields(evaluated.model_output)}
    assert model_output_fields.isdisjoint(set(FORBIDDEN_ADAPTER_FIELDS))
