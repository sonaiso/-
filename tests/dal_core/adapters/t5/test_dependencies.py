"""
Tests for ``_dependencies`` and ``T5RuntimeUnavailableError``.

These tests must keep working even when ``transformers`` and ``torch``
are not installed.
"""
from __future__ import annotations

import builtins
import importlib
import sys

import pytest

from dal_core.adapters.t5 import (
    T5RuntimeUnavailableError,
    is_t5_runtime_available,
)
from dal_core.adapters.t5 import _dependencies as deps


def test_is_t5_runtime_available_returns_bool():
    value = is_t5_runtime_available()
    assert isinstance(value, bool)


def test_require_t5_runtime_raises_clearly_when_missing(monkeypatch):
    """Force ``import transformers`` to fail and verify the error message."""

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "transformers" or name.startswith("transformers."):
            raise ImportError("simulated absence of transformers")
        if name == "torch" or name.startswith("torch."):
            raise ImportError("simulated absence of torch")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    # Drop any cached modules so the fake import is triggered.
    for mod_name in list(sys.modules):
        if mod_name == "transformers" or mod_name.startswith("transformers."):
            sys.modules.pop(mod_name)
        if mod_name == "torch" or mod_name.startswith("torch."):
            sys.modules.pop(mod_name)

    with pytest.raises(T5RuntimeUnavailableError) as excinfo:
        deps.require_t5_runtime()

    msg = str(excinfo.value)
    assert "pip install" in msg
    assert "[t5]" in msg


def test_dependencies_module_does_not_import_transformers_eagerly():
    """Importing ``_dependencies`` must not pull in transformers/torch."""
    # Drop transformers/torch from sys.modules, then reload the module
    # and check nothing reappears as a side effect of the import.
    for mod_name in list(sys.modules):
        if mod_name == "transformers" or mod_name.startswith("transformers."):
            sys.modules.pop(mod_name)
        if mod_name == "torch" or mod_name.startswith("torch."):
            sys.modules.pop(mod_name)

    importlib.reload(deps)

    assert "transformers" not in sys.modules
    assert "torch" not in sys.modules
