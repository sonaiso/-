"""
Lazy, cached loader for the T5 tokenizer and model.

This module touches ``transformers`` and ``torch`` only through
``_dependencies.require_t5_runtime``. Nothing here is imported at
package load time unless the caller actually needs to load a model.
"""
from __future__ import annotations

from threading import Lock
from typing import Any, Dict, Tuple

from ._dependencies import require_t5_runtime
from .config import T5AdapterConfig


class T5ModelLoader:
    """Process-wide cache of ``(tokenizer, model)`` pairs.

    The cache is keyed by ``(model_name, tokenizer_name, device)`` so two
    runners sharing a config never re-download or re-instantiate the
    weights. Models are placed on the configured device and switched to
    ``eval()`` mode immediately; gradient computation stays disabled
    through ``torch.inference_mode()`` at call sites in ``runner.py``.
    """

    _cache: Dict[Tuple[str, str, str], Tuple[Any, Any]] = {}
    _lock: Lock = Lock()

    @classmethod
    def load(cls, config: T5AdapterConfig) -> Tuple[Any, Any]:
        """Return ``(tokenizer, model)`` for ``config``, loading on miss."""
        key = (config.model_name, config.effective_tokenizer_name(), config.device)
        cached = cls._cache.get(key)
        if cached is not None:
            return cached

        with cls._lock:
            cached = cls._cache.get(key)
            if cached is not None:
                return cached

            transformers, torch = require_t5_runtime()

            tokenizer = transformers.AutoTokenizer.from_pretrained(
                config.effective_tokenizer_name()
            )
            model = transformers.AutoModelForSeq2SeqLM.from_pretrained(
                config.model_name
            )

            # Move to the requested device, switch to eval mode.
            try:
                model = model.to(config.device)
            except Exception as exc:  # pragma: no cover - device errors are env-specific
                raise RuntimeError(
                    f"Failed to move T5 model to device {config.device!r}: {exc!s}"
                ) from exc
            model.eval()

            cls._cache[key] = (tokenizer, model)
            return tokenizer, model

    @classmethod
    def clear(cls) -> None:
        """Drop all cached models. Primarily useful in tests."""
        with cls._lock:
            cls._cache.clear()
