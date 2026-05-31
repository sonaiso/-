"""
Real T5 input adapter (TrainingExample → AdapterInput).

Satisfies :class:`dal_core.t5_adapter_interface_contracts.InputAdapterContract`.

Constitutional reminder:
    * The returned :class:`AdapterInput` is *abstract text only*. Any
      tokenization happens later, as a local variable inside
      :mod:`dal_core.adapters.t5.runner`. Tokens never become fields of
      the dataclass.
    * Source bindings (``source_trace_id`` and
      ``source_training_example_id``) are copied verbatim from the
      :class:`TrainingExample`.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Tuple

from dal_core.t5_adapter_interface_contracts import (
    AdapterInput,
    AdapterValidationResult,
    AdapterViolationType,
    FORBIDDEN_ADAPTER_FIELDS,
    InputAdapterContract,
)
from dal_core.training_example import TrainingExample

from .config import T5AdapterConfig


@dataclass(frozen=True)
class T5InputAdapter(InputAdapterContract):
    """Concrete ``InputAdapterContract`` implementation for T5 inference.

    Fields:
        config: Frozen ``T5AdapterConfig`` (provides prompt prefix).
        adapter_name: Stable identifier used in metadata / model_name.
        version: Adapter version string (stored in metadata).
    """

    config: T5AdapterConfig
    adapter_name: str = "T5InputAdapter"
    version: str = "real_1.0"

    def __post_init__(self) -> None:
        if not isinstance(self.config, T5AdapterConfig):
            raise ValueError("T5InputAdapter.config must be a T5AdapterConfig")

    # ------------------------------------------------------------------
    # InputAdapterContract
    # ------------------------------------------------------------------

    def prepare_input(self, training_example: TrainingExample) -> AdapterInput:
        if not training_example.training_example_id:
            raise ValueError("TrainingExample missing training_example_id")
        if not training_example.source_trace_id:
            raise ValueError("TrainingExample missing source_trace_id")
        if not training_example.input_text:
            raise ValueError("TrainingExample missing input_text")

        if self.config.prompt_prefix:
            input_text = f"{self.config.prompt_prefix}{training_example.input_text}"
        else:
            input_text = training_example.input_text

        metadata: Tuple[Tuple[str, str], ...] = (
            ("adapter_name", self.adapter_name),
            ("adapter_version", self.version),
            ("source_algorithm", training_example.source_algorithm),
            ("model_name", self.config.model_name),
            ("max_input_tokens", str(self.config.max_input_tokens)),
        )

        return AdapterInput(
            adapter_input_id=f"t5_input_{training_example.training_example_id}",
            source_training_example_id=training_example.training_example_id,
            source_trace_id=training_example.source_trace_id,
            input_text=input_text,
            metadata=metadata,
        )

    def validate_input(self, adapter_input: AdapterInput) -> AdapterValidationResult:
        violations = []
        warnings = []
        checked = []

        checked.append("source_trace_id_present")
        if not adapter_input.source_trace_id:
            violations.append(AdapterViolationType.MISSING_SOURCE_TRACE_ID)

        checked.append("source_training_example_id_present")
        if not adapter_input.source_training_example_id:
            violations.append(AdapterViolationType.MISSING_SOURCE_TRAINING_EXAMPLE_ID)

        checked.append("input_text_present")
        if not adapter_input.input_text:
            warnings.append("AdapterInput has empty input_text")

        checked.append("no_forbidden_fields")
        field_names = {f.name for f in fields(adapter_input)}
        leaked = field_names & set(FORBIDDEN_ADAPTER_FIELDS)
        if leaked:
            violations.append(AdapterViolationType.FORBIDDEN_FIELD_PRESENT)
            warnings.append(f"Forbidden fields detected: {sorted(leaked)}")

        # Pre-tokenisation heuristic: bail out early on absurd lengths so
        # the (expensive) tokenizer is not invoked needlessly. We compare
        # against a character budget proportional to ``max_input_tokens``.
        checked.append("input_text_length_within_budget")
        char_budget = self.config.max_input_tokens * 8
        if len(adapter_input.input_text) > char_budget:
            warnings.append(
                f"AdapterInput.input_text length {len(adapter_input.input_text)} "
                f"exceeds soft character budget {char_budget}; will be truncated"
            )

        return AdapterValidationResult(
            validation_id=f"t5_validation_input_{adapter_input.adapter_input_id}",
            is_valid=len(violations) == 0,
            violations=tuple(violations),
            warnings=tuple(warnings),
            checked_constraints=tuple(checked),
        )
