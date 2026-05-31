"""
Lazy access to the optional ``[t5]`` runtime (transformers + torch).

This file is the **only** module in the entire repository that may
``import transformers`` or ``import torch``. It does so lazily so that
the rest of ``dal_core`` keeps importing cleanly when the optional
``[t5]`` extra is not installed.

See ``docs/T5_REAL_ADAPTER_EXECUTION_BOUNDARY.md`` for the constitutional
basis. The path-aware scanner
``GovernedT5IntegrationSkeleton.scan_path_for_execution_markers`` exempts
this directory from the strict marker check.
"""
from __future__ import annotations

from types import ModuleType
from typing import Tuple


class T5RuntimeUnavailableError(RuntimeError):
    """Raised when ``transformers`` / ``torch`` are not importable.

    Installing the optional extra resolves it::

        pip install -e .[t5]
    """


def is_t5_runtime_available() -> bool:
    """Cheap, side-effect free probe.

    Returns ``True`` iff both ``transformers`` and ``torch`` can be
    imported. Does not initialise CUDA, does not load any model.
    """
    try:
        import importlib

        importlib.import_module("transformers")
        importlib.import_module("torch")
    except Exception:
        return False
    return True


def require_t5_runtime() -> Tuple[ModuleType, ModuleType]:
    """Return ``(transformers, torch)`` or raise ``T5RuntimeUnavailableError``.

    Constitutional notes:
        * This is the single legal site of ``import transformers`` and
          ``import torch`` inside ``src/``.
        * No CUDA context is initialised here; the caller chooses the
          device (see ``T5AdapterConfig.device``).
    """
    try:
        import transformers  # type: ignore  # noqa: WPS433  (carve-out)
        import torch  # type: ignore  # noqa: WPS433  (carve-out)
    except ImportError as exc:  # pragma: no cover - exercised via tests with monkeypatch
        raise T5RuntimeUnavailableError(
            "The T5 real adapter requires the optional [t5] extra. "
            "Install it with:  pip install -e .[t5]  "
            f"(underlying error: {exc!s})"
        ) from exc
    return transformers, torch
