"""Tests for :class:`ConstitutionalEvaluationGate` (no transformers needed)."""
from __future__ import annotations

import pytest

from dal_core.adapters.t5 import (
    ConstitutionalEvaluationGate,
    EvaluatedModelOutput,
    EvaluationMode,
    T5ConstitutionalViolationError,
)
from dal_core.model_output import ModelOutput

from ._helpers import make_training_example


def _model_output(predicted_text: str, *, training_example_id: str, trace_id: str) -> ModelOutput:
    return ModelOutput(
        model_output_id="model_out_001",
        source_training_example_id=training_example_id,
        source_trace_id=trace_id,
        predicted_text=predicted_text,
        model_name="dummy-model",
        generation_timestamp="2026-05-31T00:00:00Z",
    )


class TestGateValidOutput:
    def test_strict_returns_evaluated_for_clean_output(self):
        ex = make_training_example()
        out = _model_output(
            "Trace step references candidate_a1.",
            training_example_id=ex.training_example_id,
            trace_id=ex.source_trace_id,
        )
        gate = ConstitutionalEvaluationGate(mode=EvaluationMode.STRICT)
        evaluated = gate.evaluate(out, ex)
        assert isinstance(evaluated, EvaluatedModelOutput)
        assert evaluated.report.passed
        assert evaluated.mode is EvaluationMode.STRICT

    def test_observe_returns_evaluated_for_clean_output(self):
        ex = make_training_example()
        out = _model_output(
            "Trace step references candidate_a1.",
            training_example_id=ex.training_example_id,
            trace_id=ex.source_trace_id,
        )
        gate = ConstitutionalEvaluationGate(mode=EvaluationMode.OBSERVE)
        evaluated = gate.evaluate(out, ex)
        assert evaluated.report.passed


class TestGateAuthorityViolation:
    AUTHORITY_TEXT = "The final answer: this is the correct analysis."

    def test_strict_raises_on_critical_violation(self):
        ex = make_training_example()
        out = _model_output(
            self.AUTHORITY_TEXT,
            training_example_id=ex.training_example_id,
            trace_id=ex.source_trace_id,
        )
        gate = ConstitutionalEvaluationGate(mode=EvaluationMode.STRICT)
        with pytest.raises(T5ConstitutionalViolationError) as excinfo:
            gate.evaluate(out, ex)
        # The exception carries the offending output and the full report.
        assert excinfo.value.model_output is out
        assert excinfo.value.report.critical_violations_count > 0
        assert len(excinfo.value.critical_violations) > 0

    def test_observe_returns_report_without_raising(self):
        ex = make_training_example()
        out = _model_output(
            self.AUTHORITY_TEXT,
            training_example_id=ex.training_example_id,
            trace_id=ex.source_trace_id,
        )
        gate = ConstitutionalEvaluationGate(mode=EvaluationMode.OBSERVE)
        evaluated = gate.evaluate(out, ex)
        assert not evaluated.report.passed


class TestGateBindingViolations:
    def test_missing_source_trace_id_is_critical_in_strict(self):
        ex = make_training_example()
        out = _model_output(
            "trace explanation",
            training_example_id=ex.training_example_id,
            trace_id="",  # missing!
        )
        gate = ConstitutionalEvaluationGate(mode=EvaluationMode.STRICT)
        with pytest.raises(T5ConstitutionalViolationError):
            gate.evaluate(out, ex)


class TestGateConstruction:
    def test_default_mode_is_strict(self):
        gate = ConstitutionalEvaluationGate()
        assert gate.mode is EvaluationMode.STRICT

    def test_mode_must_be_enum(self):
        with pytest.raises(ValueError):
            ConstitutionalEvaluationGate(mode="strict")  # type: ignore[arg-type]
