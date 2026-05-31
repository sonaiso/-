"""
Helpers shared by the T5 adapter test suite (no-transformers and t5 alike).
"""
from __future__ import annotations

from dal_core.algorithm_trace_payload import TraceConsumerOperation
from dal_core.trace_explanation_dataset_generator import (
    OutputType,
    ValidationStatus,
)
from dal_core.training_example import TrainingExample


def make_training_example(
    *,
    training_example_id: str = "training_example_t5_001",
    source_trace_id: str = "trace_t5_001",
    source_dataset_row_id: str = "dataset_row_t5_001",
    input_text: str = "Explain trace step: T1 emits CandidateA.",
    target_text: str = "Explanation: T1 produced CandidateA.",
    output_type: OutputType = OutputType.EXPLANATION,
    operation: TraceConsumerOperation = TraceConsumerOperation.EXPLAIN_TRACE,
    referenced_candidate_ids=("candidate_a1",),
    referenced_residual_ids=(),
    referenced_gate_ids=(),
    referenced_rank_values=(),
    requires_algorithm_rerun: bool = False,
    validation_status: ValidationStatus = ValidationStatus.VALID,
    source_algorithm: str = "MufradAcceptanceEquation",
) -> TrainingExample:
    """Build a minimal valid :class:`TrainingExample` for adapter tests."""
    return TrainingExample(
        training_example_id=training_example_id,
        source_dataset_row_id=source_dataset_row_id,
        source_trace_id=source_trace_id,
        source_algorithm=source_algorithm,
        operation=operation,
        input_text=input_text,
        target_text=target_text,
        referenced_candidate_ids=tuple(referenced_candidate_ids),
        referenced_residual_ids=tuple(referenced_residual_ids),
        referenced_gate_ids=tuple(referenced_gate_ids),
        referenced_rank_values=tuple(referenced_rank_values),
        output_type=output_type,
        requires_algorithm_rerun=requires_algorithm_rerun,
        validation_status=validation_status,
    )
