"""
Configuration objects for the real T5 adapter.

All values are frozen and validated at construction. Nothing in this
module imports ``transformers`` or ``torch``.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Tuple


class EvaluationMode(Enum):
    """How ``ConstitutionalEvaluationGate`` should react to violations.

    Members:
        STRICT: Any CRITICAL violation raises
            ``T5ConstitutionalViolationError`` and the output is
            **not** returned to the caller. Non-critical violations are
            attached to the returned report.
        OBSERVE: All violations (critical or not) are reported but the
            output is still returned. Intended for development and for
            offline auditing.
    """

    STRICT = auto()
    OBSERVE = auto()


# Default device names recognised by ``T5ModelLoader``. We deliberately
# keep this short; CUDA / MPS support arrives in later carve-outs.
_ALLOWED_DEVICES = frozenset({"cpu", "cuda", "mps"})

# Default conservative generation kwargs. They are stored as a tuple of
# string pairs so ``T5AdapterConfig`` stays hashable / frozen.
_DEFAULT_GENERATION_KWARGS: Tuple[Tuple[str, str], ...] = (
    ("do_sample", "false"),
    ("num_beams", "1"),
    ("early_stopping", "true"),
)


@dataclass(frozen=True)
class T5AdapterConfig:
    """Immutable configuration for ``T5AdapterRunner``.

    The configuration deliberately stores only **strings, ints, enums and
    tuples**. It never stores tokenizer instances, model instances or
    torch tensors — those are constructed locally inside ``runner.py``.

    Fields:
        model_name: Hugging Face model identifier or local path.
        tokenizer_name: Optional tokenizer identifier (defaults to
            ``model_name``).
        max_input_tokens: Truncation length applied at tokenization
            time (local-only).
        max_output_tokens: ``max_new_tokens`` passed to ``.generate()``.
        device: ``"cpu"`` (default), ``"cuda"`` or ``"mps"``.
        evaluation_mode: ``STRICT`` or ``OBSERVE``.
        prompt_prefix: Optional prompt template prefix prepended to
            ``TrainingExample.input_text`` by ``T5InputAdapter``.
        generation_kwargs: Extra kwargs forwarded to ``.generate()``,
            stored as ``((key, str_value), ...)``.
    """

    model_name: str = "google/flan-t5-small"
    tokenizer_name: str = ""
    max_input_tokens: int = 512
    max_output_tokens: int = 128
    device: str = "cpu"
    evaluation_mode: EvaluationMode = EvaluationMode.STRICT
    prompt_prefix: str = ""
    generation_kwargs: Tuple[Tuple[str, str], ...] = field(
        default_factory=lambda: _DEFAULT_GENERATION_KWARGS
    )

    def __post_init__(self) -> None:
        if not isinstance(self.model_name, str) or not self.model_name:
            raise ValueError("T5AdapterConfig.model_name must be a non-empty string")
        if not isinstance(self.tokenizer_name, str):
            raise ValueError("T5AdapterConfig.tokenizer_name must be a string")
        if self.max_input_tokens <= 0:
            raise ValueError("T5AdapterConfig.max_input_tokens must be > 0")
        if self.max_output_tokens <= 0:
            raise ValueError("T5AdapterConfig.max_output_tokens must be > 0")
        if self.device not in _ALLOWED_DEVICES:
            raise ValueError(
                f"T5AdapterConfig.device must be one of {sorted(_ALLOWED_DEVICES)}, "
                f"got {self.device!r}"
            )
        if not isinstance(self.evaluation_mode, EvaluationMode):
            raise ValueError(
                "T5AdapterConfig.evaluation_mode must be an EvaluationMode member"
            )
        if not isinstance(self.generation_kwargs, tuple):
            raise ValueError(
                "T5AdapterConfig.generation_kwargs must be a tuple of (key, value) pairs"
            )
        for pair in self.generation_kwargs:
            if (
                not isinstance(pair, tuple)
                or len(pair) != 2
                or not isinstance(pair[0], str)
                or not isinstance(pair[1], str)
            ):
                raise ValueError(
                    "T5AdapterConfig.generation_kwargs entries must be (str, str) pairs"
                )

        # NOTE: ``FORBIDDEN_ADAPTER_FIELDS`` (PR #152) applies to data
        # structures that cross the *adapter boundary* (``AdapterInput`` /
        # ``AdapterRawOutput`` / ``ModelOutput``). It does not apply to
        # internal configuration objects like this one. The fields here
        # are plain strings/ints/enums; no tensor or model handle ever
        # lives on the config.

    def effective_tokenizer_name(self) -> str:
        """Return the tokenizer identifier, defaulting to ``model_name``."""
        return self.tokenizer_name or self.model_name

    def generation_kwargs_dict(self) -> dict:
        """Decode ``generation_kwargs`` into a plain dict for ``.generate()``.

        Values are interpreted with a small heuristic:
            * ``"true"`` / ``"false"`` → ``bool``
            * integer-looking strings → ``int``
            * float-looking strings → ``float``
            * everything else → ``str`` (passed through unchanged)
        """
        decoded: dict = {}
        for key, value in self.generation_kwargs:
            decoded[key] = _decode_generation_value(value)
        return decoded


def _decode_generation_value(value: str):
    lowered = value.strip().lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value
