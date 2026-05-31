"""
Real T5 output adapter (AdapterRawOutput → ModelOutput).

Satisfies :class:`dal_core.t5_adapter_interface_contracts.OutputAdapterContract`.

Constitutional reminder:
    * The incoming :class:`AdapterRawOutput` already contains decoded
      *abstract text*: the runner decoded the model's output ids using
      the tokenizer as a local variable. No tensor crosses this
      boundary.
    * :class:`ModelOutput` is built via
      :meth:`ModelOutput.create_from_prediction`, which guarantees the
      source bindings are preserved.
    * Validation never modifies the output; violations are surfaced for
      the gate / ``ConstitutionalEvaluator`` to act on.
"""
from __future__ import annotations

from dataclasses import dataclass, fields

from dal_core.model_output import ModelOutput
from dal_core.t5_adapter_interface_contracts import (
    AdapterRawOutput,
    AdapterValidationResult,
    AdapterViolationType,
    FORBIDDEN_ADAPTER_FIELDS,
    OutputAdapterContract,
)

from .config import T5AdapterConfig


@dataclass(frozen=True)
class T5OutputAdapter(OutputAdapterContract):
    """Concrete ``OutputAdapterContract`` implementation for T5 inference."""

    config: T5AdapterConfig
    adapter_name: str = "T5OutputAdapter"
    version: str = "real_1.0"

    def __post_init__(self) -> None:
        if not isinstance(self.config, T5AdapterConfig):
            raise ValueError("T5OutputAdapter.config must be a T5AdapterConfig")

    # ------------------------------------------------------------------
    # OutputAdapterContract
    # ------------------------------------------------------------------

    def parse_output(
        self,
        adapter_raw_output: AdapterRawOutput,
        source_training_example_id: str,
        source_trace_id: str,
    ) -> ModelOutput:
        if not source_training_example_id:
            raise ValueError("parse_output requires source_training_example_id")
        if not source_trace_id:
            raise ValueError("parse_output requires source_trace_id")
        if not adapter_raw_output.raw_output_text:
            raise ValueError("AdapterRawOutput has empty raw_output_text")

        predicted_text = adapter_raw_output.raw_output_text

        # The adapter never strips authority claims. The downstream
        # ConstitutionalEvaluator is the sole authority on what is
        # acceptable; the gate raises in STRICT mode.
        return ModelOutput.create_from_prediction(
            source_training_example_id=source_training_example_id,
            source_trace_id=source_trace_id,
            predicted_text=predicted_text,
            model_name=f"{self.config.model_name}@{self.adapter_name}/{self.version}",
        )

    def validate_output(self, model_output: ModelOutput) -> AdapterValidationResult:
        violations = []
        warnings = []
        checked = []

        checked.append("source_trace_id_present")
        if not model_output.source_trace_id:
            violations.append(AdapterViolationType.MISSING_SOURCE_TRACE_ID)

        checked.append("source_training_example_id_present")
        if not model_output.source_training_example_id:
            violations.append(AdapterViolationType.MISSING_SOURCE_TRAINING_EXAMPLE_ID)

        checked.append("predicted_text_present")
        if not model_output.predicted_text:
            warnings.append("ModelOutput has empty predicted_text")

        checked.append("no_forbidden_fields")
        field_names = {f.name for f in fields(model_output)}
        leaked = field_names & set(FORBIDDEN_ADAPTER_FIELDS)
        if leaked:
            violations.append(AdapterViolationType.FORBIDDEN_FIELD_PRESENT)
            warnings.append(f"Forbidden fields detected: {sorted(leaked)}")

        return AdapterValidationResult(
            validation_id=f"t5_validation_output_{model_output.model_output_id}",
            is_valid=len(violations) == 0,
            violations=tuple(violations),
            warnings=tuple(warnings),
            checked_constraints=tuple(checked),
        )
