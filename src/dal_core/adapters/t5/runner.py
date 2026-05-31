"""
T5 adapter runner — the only place where T5 inference actually runs.

This module is the single executable site of the carve-out:

    TrainingExample
        → T5InputAdapter.prepare_input      (abstract text)
        → tokenizer(...)                    (local variable)
        → model.generate(...)               (local variable, inference_mode)
        → tokenizer.decode(...)             (local variable)
        → AdapterRawOutput                  (abstract text)
        → T5OutputAdapter.parse_output      → ModelOutput
        → ConstitutionalEvaluationGate      → EvaluatedModelOutput

The runner has no code path that emits a :class:`ModelOutput` (or
:class:`EvaluatedModelOutput`) without first passing it through the
gate. The gate is mandatory.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Tuple
from uuid import uuid4

from dal_core.t5_adapter_interface_contracts import (
    AdapterRawOutput,
    AdapterStatus,
    AdapterValidationResult,
)
from dal_core.training_example import TrainingExample

from ._dependencies import require_t5_runtime
from .config import EvaluationMode, T5AdapterConfig
from .evaluation_gate import (
    ConstitutionalEvaluationGate,
    EvaluatedModelOutput,
)
from .input_adapter import T5InputAdapter
from .model_loader import T5ModelLoader
from .output_adapter import T5OutputAdapter


class T5AdapterError(RuntimeError):
    """Raised for structural / boundary failures in :class:`T5AdapterRunner`.

    Constitutional violations from the evaluator surface as
    :class:`T5ConstitutionalViolationError` (different class), so callers
    can distinguish "the runner is broken" from "the model output broke
    the constitution".
    """

    def __init__(self, message: str, validation: AdapterValidationResult | None = None):
        super().__init__(message)
        self.validation = validation


@dataclass
class T5AdapterRunner:
    """Top-level real T5 runner.

    The runner is intentionally **not** ``frozen``: it owns no mutable
    state of its own, but Python dataclasses cannot use ``frozen=True``
    here because the runner constructs adapters lazily in
    :meth:`__post_init__`.

    Fields:
        config: ``T5AdapterConfig``.
        input_adapter: Defaults to ``T5InputAdapter(config)``.
        output_adapter: Defaults to ``T5OutputAdapter(config)``.
        gate: Defaults to ``ConstitutionalEvaluationGate(config.evaluation_mode)``.
    """

    config: T5AdapterConfig
    input_adapter: T5InputAdapter = field(default=None)  # type: ignore[assignment]
    output_adapter: T5OutputAdapter = field(default=None)  # type: ignore[assignment]
    gate: ConstitutionalEvaluationGate = field(default=None)  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if not isinstance(self.config, T5AdapterConfig):
            raise ValueError("T5AdapterRunner.config must be a T5AdapterConfig")
        if self.input_adapter is None:
            self.input_adapter = T5InputAdapter(config=self.config)
        if self.output_adapter is None:
            self.output_adapter = T5OutputAdapter(config=self.config)
        if self.gate is None:
            self.gate = ConstitutionalEvaluationGate(mode=self.config.evaluation_mode)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self, training_example: TrainingExample) -> EvaluatedModelOutput:
        """Full pipeline for a single :class:`TrainingExample`.

        Raises:
            T5AdapterError: structural / boundary failure (e.g. validation
                of the prepared :class:`AdapterInput` failed).
            T5ConstitutionalViolationError: gate raised in STRICT mode.
            T5RuntimeUnavailableError: ``[t5]`` extra not installed.
        """
        adapter_input = self.input_adapter.prepare_input(training_example)

        input_validation = self.input_adapter.validate_input(adapter_input)
        if not input_validation.is_valid:
            raise T5AdapterError(
                f"T5InputAdapter rejected prepared input: "
                f"violations={[v.name for v in input_validation.violations]}",
                validation=input_validation,
            )

        raw_output = self._infer(adapter_input.input_text, adapter_input)

        model_output = self.output_adapter.parse_output(
            adapter_raw_output=raw_output,
            source_training_example_id=adapter_input.source_training_example_id,
            source_trace_id=adapter_input.source_trace_id,
        )

        output_validation = self.output_adapter.validate_output(model_output)
        if not output_validation.is_valid:
            raise T5AdapterError(
                f"T5OutputAdapter rejected ModelOutput: "
                f"violations={[v.name for v in output_validation.violations]}",
                validation=output_validation,
            )

        # MANDATORY: every ModelOutput passes through the gate.
        return self.gate.evaluate(model_output, training_example)

    def run_batch(
        self,
        training_examples: Tuple[TrainingExample, ...],
    ) -> Tuple[EvaluatedModelOutput, ...]:
        """Sequentially run :meth:`run` for each example.

        Real batching across the GPU is deferred to a later carve-out.
        Sequential execution keeps the constitutional contract simple:
        one input ↔ one gate evaluation.
        """
        return tuple(self.run(example) for example in training_examples)

    # ------------------------------------------------------------------
    # Internal — the only place tokenization & generation occur
    # ------------------------------------------------------------------

    def _infer(self, input_text: str, adapter_input) -> AdapterRawOutput:
        """Tokenize, generate, decode. Tokens stay local to this method."""
        _transformers, torch = require_t5_runtime()

        tokenizer, model = T5ModelLoader.load(self.config)

        encoded = tokenizer(
            input_text,
            return_tensors="pt",
            truncation=True,
            max_length=self.config.max_input_tokens,
        )

        # Move tensors to the model's device.
        encoded = {k: v.to(self.config.device) for k, v in encoded.items()}

        start = time.perf_counter()
        with torch.inference_mode():
            output_ids = model.generate(
                **encoded,
                max_new_tokens=self.config.max_output_tokens,
                **self.config.generation_kwargs_dict(),
            )
        elapsed = time.perf_counter() - start

        decoded_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        if not decoded_text:
            raise T5AdapterError(
                "T5 model produced empty decoded output; cannot build AdapterRawOutput"
            )

        metadata: Tuple[Tuple[str, str], ...] = (
            ("model_name", self.config.model_name),
            ("device", self.config.device),
            ("inference_seconds", f"{elapsed:.6f}"),
            ("max_new_tokens", str(self.config.max_output_tokens)),
            ("evaluation_mode", self.config.evaluation_mode.name),
            ("source_adapter_input_id", adapter_input.adapter_input_id),
        )

        return AdapterRawOutput(
            adapter_output_id=f"t5_raw_output_{uuid4().hex[:16]}",
            source_adapter_input_id=adapter_input.adapter_input_id,
            raw_output_text=decoded_text,
            adapter_metadata=metadata,
        )


# Re-export AdapterStatus / EvaluationMode for ergonomic imports.
__all__ = [
    "T5AdapterRunner",
    "T5AdapterError",
    "AdapterStatus",
    "EvaluationMode",
]
