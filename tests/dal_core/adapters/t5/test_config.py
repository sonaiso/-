"""Tests for :class:`T5AdapterConfig` (no transformers required)."""
from __future__ import annotations

import dataclasses

import pytest

from dal_core.adapters.t5 import EvaluationMode, T5AdapterConfig


class TestT5AdapterConfigDefaults:
    def test_defaults_are_sensible(self):
        cfg = T5AdapterConfig()
        assert cfg.model_name == "google/flan-t5-small"
        assert cfg.max_input_tokens > 0
        assert cfg.max_output_tokens > 0
        assert cfg.device == "cpu"
        assert cfg.evaluation_mode is EvaluationMode.STRICT
        assert cfg.tokenizer_name == ""
        assert cfg.effective_tokenizer_name() == cfg.model_name

    def test_config_is_frozen(self):
        cfg = T5AdapterConfig()
        with pytest.raises(dataclasses.FrozenInstanceError):
            cfg.model_name = "other"  # type: ignore[misc]

    def test_explicit_tokenizer_overrides_default(self):
        cfg = T5AdapterConfig(model_name="t5-base", tokenizer_name="t5-small")
        assert cfg.effective_tokenizer_name() == "t5-small"


class TestT5AdapterConfigValidation:
    def test_empty_model_name_rejected(self):
        with pytest.raises(ValueError):
            T5AdapterConfig(model_name="")

    def test_zero_max_input_tokens_rejected(self):
        with pytest.raises(ValueError):
            T5AdapterConfig(max_input_tokens=0)

    def test_negative_max_output_tokens_rejected(self):
        with pytest.raises(ValueError):
            T5AdapterConfig(max_output_tokens=-1)

    def test_unknown_device_rejected(self):
        with pytest.raises(ValueError):
            T5AdapterConfig(device="tpu")

    def test_evaluation_mode_must_be_enum(self):
        with pytest.raises(ValueError):
            T5AdapterConfig(evaluation_mode="strict")  # type: ignore[arg-type]

    def test_generation_kwargs_must_be_tuple_of_pairs(self):
        with pytest.raises(ValueError):
            T5AdapterConfig(generation_kwargs=[("a", "b")])  # type: ignore[arg-type]
        with pytest.raises(ValueError):
            T5AdapterConfig(generation_kwargs=(("a", 1),))  # type: ignore[arg-type]


class TestGenerationKwargsDecoding:
    def test_decodes_booleans(self):
        cfg = T5AdapterConfig(generation_kwargs=(("do_sample", "true"),))
        assert cfg.generation_kwargs_dict() == {"do_sample": True}

    def test_decodes_integers(self):
        cfg = T5AdapterConfig(generation_kwargs=(("num_beams", "4"),))
        assert cfg.generation_kwargs_dict() == {"num_beams": 4}

    def test_decodes_floats(self):
        cfg = T5AdapterConfig(generation_kwargs=(("temperature", "0.7"),))
        assert cfg.generation_kwargs_dict() == {"temperature": 0.7}

    def test_passes_through_strings(self):
        cfg = T5AdapterConfig(generation_kwargs=(("eos_token", "<eos>"),))
        assert cfg.generation_kwargs_dict() == {"eos_token": "<eos>"}
