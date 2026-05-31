"""
Tests for ``T5InputAdapter`` and ``T5OutputAdapter`` (no transformers needed).

These adapters do all their work on abstract strings; they never touch
``transformers`` or ``torch``. The tests below therefore run on the
plain CI matrix.
"""
from __future__ import annotations

import dataclasses

import pytest

from dal_core.adapters.t5 import T5AdapterConfig, T5InputAdapter, T5OutputAdapter
from dal_core.model_output import ModelOutput
from dal_core.t5_adapter_interface_contracts import (
    AdapterInput,
    AdapterRawOutput,
    AdapterValidationResult,
    AdapterViolationType,
    FORBIDDEN_ADAPTER_FIELDS,
)

from ._helpers import make_training_example


# ---------------------------------------------------------------------------
# T5InputAdapter
# ---------------------------------------------------------------------------

class TestT5InputAdapterPrepareInput:
    def test_preserves_source_bindings(self):
        cfg = T5AdapterConfig()
        adapter = T5InputAdapter(config=cfg)
        example = make_training_example(
            training_example_id="ex_42",
            source_trace_id="trace_42",
            input_text="What is the trace?",
        )

        result = adapter.prepare_input(example)

        assert isinstance(result, AdapterInput)
        assert result.source_training_example_id == "ex_42"
        assert result.source_trace_id == "trace_42"
        assert "What is the trace?" in result.input_text

    def test_prompt_prefix_is_applied(self):
        cfg = T5AdapterConfig(prompt_prefix="explain trace: ")
        adapter = T5InputAdapter(config=cfg)
        example = make_training_example(input_text="step T1.")

        result = adapter.prepare_input(example)

        assert result.input_text.startswith("explain trace: ")
        assert "step T1." in result.input_text

    def test_metadata_contains_model_name(self):
        cfg = T5AdapterConfig(model_name="my/local-t5")
        adapter = T5InputAdapter(config=cfg)
        example = make_training_example()
        result = adapter.prepare_input(example)
        meta = dict(result.metadata)
        assert meta["model_name"] == "my/local-t5"
        assert meta["adapter_name"] == "T5InputAdapter"

    def test_rejects_example_without_trace_id(self):
        # TrainingExample itself does not validate empty fields, so we
        # simulate by zeroing the source_trace_id afterwards via
        # ``dataclasses.replace`` on a built example.
        cfg = T5AdapterConfig()
        adapter = T5InputAdapter(config=cfg)
        example = make_training_example()
        bad = dataclasses.replace(example, source_trace_id="")
        with pytest.raises(ValueError):
            adapter.prepare_input(bad)

    def test_rejects_example_without_input_text(self):
        cfg = T5AdapterConfig()
        adapter = T5InputAdapter(config=cfg)
        example = make_training_example()
        bad = dataclasses.replace(example, input_text="")
        with pytest.raises(ValueError):
            adapter.prepare_input(bad)


class TestT5InputAdapterValidateInput:
    def test_valid_input_passes(self):
        cfg = T5AdapterConfig()
        adapter = T5InputAdapter(config=cfg)
        example = make_training_example()
        result = adapter.validate_input(adapter.prepare_input(example))
        assert isinstance(result, AdapterValidationResult)
        assert result.is_valid
        assert result.violations == ()

    def test_oversize_input_warns(self):
        cfg = T5AdapterConfig(max_input_tokens=8)
        adapter = T5InputAdapter(config=cfg)
        example = make_training_example(input_text="x" * 5_000)
        result = adapter.validate_input(adapter.prepare_input(example))
        # Still valid (warning only), but warnings must mention the budget.
        assert result.is_valid
        assert any("budget" in w for w in result.warnings)

    def test_adapter_input_has_no_forbidden_fields(self):
        """Static guarantee: ``AdapterInput`` declares no forbidden field."""
        names = {f.name for f in dataclasses.fields(AdapterInput)}
        assert names.isdisjoint(set(FORBIDDEN_ADAPTER_FIELDS))


# ---------------------------------------------------------------------------
# T5OutputAdapter
# ---------------------------------------------------------------------------

class TestT5OutputAdapterParseOutput:
    def _raw(self, text: str = "T1 produced CandidateA.") -> AdapterRawOutput:
        return AdapterRawOutput(
            adapter_output_id="raw_001",
            source_adapter_input_id="input_001",
            raw_output_text=text,
            adapter_metadata=(),
        )

    def test_preserves_bindings(self):
        cfg = T5AdapterConfig()
        adapter = T5OutputAdapter(config=cfg)
        raw = self._raw()
        out = adapter.parse_output(raw, "ex_42", "trace_42")
        assert isinstance(out, ModelOutput)
        assert out.source_training_example_id == "ex_42"
        assert out.source_trace_id == "trace_42"
        assert out.predicted_text == raw.raw_output_text
        assert cfg.model_name in out.model_name
        assert "T5OutputAdapter" in out.model_name

    def test_requires_source_ids(self):
        cfg = T5AdapterConfig()
        adapter = T5OutputAdapter(config=cfg)
        raw = self._raw()
        with pytest.raises(ValueError):
            adapter.parse_output(raw, "", "trace_42")
        with pytest.raises(ValueError):
            adapter.parse_output(raw, "ex_42", "")

    def test_requires_non_empty_raw_text(self):
        cfg = T5AdapterConfig()
        adapter = T5OutputAdapter(config=cfg)
        # AdapterRawOutput's own __post_init__ already blocks empty text,
        # but ``parse_output`` is defensive in case a future subclass
        # bypasses construction. Verify both paths.
        with pytest.raises(ValueError):
            AdapterRawOutput(
                adapter_output_id="raw_001",
                source_adapter_input_id="input_001",
                raw_output_text="",
                adapter_metadata=(),
            )

    def test_validate_output_detects_forbidden_fields_static(self):
        """``ModelOutput`` itself must not declare any forbidden field."""
        names = {f.name for f in dataclasses.fields(ModelOutput)}
        assert names.isdisjoint(set(FORBIDDEN_ADAPTER_FIELDS))

    def test_validate_output_valid_when_complete(self):
        cfg = T5AdapterConfig()
        adapter = T5OutputAdapter(config=cfg)
        out = adapter.parse_output(self._raw(), "ex_42", "trace_42")
        result = adapter.validate_output(out)
        assert result.is_valid
        assert result.violations == ()

    def test_validate_output_detects_missing_bindings(self):
        cfg = T5AdapterConfig()
        adapter = T5OutputAdapter(config=cfg)
        # Build a ModelOutput with empty bindings — allowed by
        # ModelOutput.__post_init__ (PR #147 hotfix), surfaced as
        # violations by the adapter / evaluator.
        bad = ModelOutput(
            model_output_id="m_001",
            source_training_example_id="",
            source_trace_id="",
            predicted_text="hi",
            model_name="t5",
            generation_timestamp="2026-05-31T00:00:00Z",
        )
        result = adapter.validate_output(bad)
        assert not result.is_valid
        assert AdapterViolationType.MISSING_SOURCE_TRACE_ID in result.violations
        assert (
            AdapterViolationType.MISSING_SOURCE_TRAINING_EXAMPLE_ID
            in result.violations
        )


# ---------------------------------------------------------------------------
# Contract conformance (structural, not runtime_checkable)
# ---------------------------------------------------------------------------

class TestContractConformance:
    def test_input_adapter_has_protocol_methods(self):
        adapter = T5InputAdapter(config=T5AdapterConfig())
        assert callable(getattr(adapter, "prepare_input", None))
        assert callable(getattr(adapter, "validate_input", None))

    def test_output_adapter_has_protocol_methods(self):
        adapter = T5OutputAdapter(config=T5AdapterConfig())
        assert callable(getattr(adapter, "parse_output", None))
        assert callable(getattr(adapter, "validate_output", None))

    def test_adapters_are_frozen(self):
        adapter_in = T5InputAdapter(config=T5AdapterConfig())
        adapter_out = T5OutputAdapter(config=T5AdapterConfig())
        with pytest.raises(dataclasses.FrozenInstanceError):
            adapter_in.adapter_name = "x"  # type: ignore[misc]
        with pytest.raises(dataclasses.FrozenInstanceError):
            adapter_out.adapter_name = "x"  # type: ignore[misc]
