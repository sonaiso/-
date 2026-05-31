"""
First real T5 Input/Output Adapter (executes under constitutional carve-out).

This is the **only** location in ``src/dal_core/`` where ``transformers``
and ``torch`` may be imported and where real T5 inference may run. See
``docs/T5_REAL_ADAPTER_EXECUTION_BOUNDARY.md`` for the constitutional
basis and ``docs/T5_REAL_ADAPTER.md`` for the operational contract.

Public surface (everything else is internal):

    Config & dependencies
        - ``T5AdapterConfig``: frozen integration configuration
        - ``EvaluationMode``: ``STRICT`` / ``OBSERVE``
        - ``T5RuntimeUnavailableError``: raised when ``[t5]`` extra not installed

    Adapters (satisfy PR #152 contracts)
        - ``T5InputAdapter``: ``InputAdapterContract`` implementation
        - ``T5OutputAdapter``: ``OutputAdapterContract`` implementation

    Evaluation
        - ``ConstitutionalEvaluationGate``
        - ``EvaluatedModelOutput``
        - ``T5ConstitutionalViolationError``

    Runner
        - ``T5AdapterRunner``: TrainingExample → EvaluatedModelOutput
        - ``T5AdapterError``: structural runner errors

Constitutional law (recap):
    * AdapterInput / AdapterRawOutput / ModelOutput stay abstract text only;
      tokenization happens as a local variable inside ``runner.py``.
    * Every ModelOutput produced by ``T5AdapterRunner.run`` is gated through
      ``ConstitutionalEvaluator`` before being returned.
    * No rank upgrade, no residual resolution, no ifādah/hukm/reality.
    * No training, no fine-tuning, no gradients.
"""

from .config import T5AdapterConfig, EvaluationMode
from ._dependencies import T5RuntimeUnavailableError, is_t5_runtime_available
from .input_adapter import T5InputAdapter
from .output_adapter import T5OutputAdapter
from .evaluation_gate import (
    ConstitutionalEvaluationGate,
    EvaluatedModelOutput,
    T5ConstitutionalViolationError,
)
from .runner import T5AdapterRunner, T5AdapterError

__all__ = [
    "T5AdapterConfig",
    "EvaluationMode",
    "T5RuntimeUnavailableError",
    "is_t5_runtime_available",
    "T5InputAdapter",
    "T5OutputAdapter",
    "ConstitutionalEvaluationGate",
    "EvaluatedModelOutput",
    "T5ConstitutionalViolationError",
    "T5AdapterRunner",
    "T5AdapterError",
]
