"""
Training Example Contract (عقد مثال التدريب)

PR #146: Dataset export contract for T5 training/evaluation.

Constitutional Laws:
    1. TrainingExample is derived ONLY from DatasetRow
    2. TrainingExample MUST preserve source_trace_id
    3. TrainingExample MUST preserve source_dataset_row_id
    4. TrainingExample is immutable serialization boundary
    5. TrainingExample does NOT create candidates
    6. TrainingExample does NOT upgrade rank
    7. TrainingExample does NOT delete residuals
    8. TrainingExample does NOT close ifādah
    9. TrainingExample does NOT produce hukm
    10. TrainingExample does NOT produce reality

Forbidden Pipeline:
    ❌ Raw Arabic → TrainingExample
    ❌ TrainingExample → Candidate
    ❌ TrainingExample → Rank Upgrade
    ❌ TrainingExample → Residual Resolution
    ❌ TrainingExample → Ifādah Closure
    ❌ TrainingExample → Hukm
    ❌ TrainingExample → Reality

Permitted Pipeline:
    ✅ DatasetRow → TrainingExample → JSONL Export
    ✅ AlgorithmTracePayload → DatasetRow → TrainingExample

Constitutional Formula:
    الجبر = الدستور (Algebra = Constitution)
    الخوارزمية = تنفيذ الدستور (Algorithm = Constitutional Execution)
    AlgorithmTracePayload = أثر التنفيذ (Trace = Execution Evidence)
    DatasetRow = صف البيانات (Dataset Row)
    TrainingExample = مثال التدريب المحمي (Protected Training Example)

Supreme Law:
    Training examples are protected serialization artifacts.
    Training examples do NOT create constitutional facts.

Reference:
    User requirement: PR #146 specification (2026-05-28)
    Builds on: PR #141, PR #142, PR #145

Created: 2026-05-28
"""

from dataclasses import dataclass
from typing import Tuple

from dal_core.trace_explanation_dataset_generator import (
    OutputType,
    ValidationStatus,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation


# ============================================================================
# Training Example
# ============================================================================

@dataclass(frozen=True)
class TrainingExample:
    """
    Single immutable training/evaluation example derived from DatasetRow.

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - training_example_id is unique identifier
        - source_dataset_row_id MUST reference valid DatasetRow
        - source_trace_id MUST reference valid AlgorithmTracePayload
        - source_algorithm preserves algorithm attribution
        - operation preserves consumer operation type
        - input_text derived from DatasetRow.input_trace_summary
        - target_text derived from DatasetRow.target_output_text
        - All referenced_* fields preserve trace bindings
        - output_type preserves EXPLANATION or REPAIR_SUGGESTION classification
        - requires_algorithm_rerun preserves repair requirement
        - validation_status preserves constitutional validation result

    Forbidden Fields:
        ❌ upgraded_rank: TrainingExample does NOT upgrade rank
        ❌ resolved_residuals: TrainingExample does NOT resolve residuals
        ❌ closed_ifadah: TrainingExample does NOT close ifādah
        ❌ produced_hukm: TrainingExample does NOT produce hukm
        ❌ produced_reality: TrainingExample does NOT produce reality
        ❌ raw_arabic_source: TrainingExample does NOT analyze raw Arabic
        ❌ new_candidate: TrainingExample does NOT create candidates
        ❌ semantic_certainty: TrainingExample does NOT produce semantic certainty
        ❌ final_answer: TrainingExample does NOT assert final answers
        ❌ correct_analysis: TrainingExample does NOT assert correct analysis
        ❌ gold_label_hukm: TrainingExample does NOT assert gold label hukm
        ❌ resolved_output: TrainingExample does NOT assert resolved outputs

    Fields:
        training_example_id: Unique identifier for this training example
        source_dataset_row_id: dataset_row_id from DatasetRow (CONSTITUTIONAL BINDING)
        source_trace_id: trace_id from AlgorithmTracePayload (CONSTITUTIONAL BINDING)
        source_algorithm: Algorithm that produced the trace
        operation: TraceConsumerOperation performed
        input_text: Input text for training (from DatasetRow.input_trace_summary)
        target_text: Target output text for training (from DatasetRow.target_output_text)
        referenced_candidate_ids: Candidate IDs referenced in output
        referenced_residual_ids: Residual IDs referenced in output
        referenced_gate_ids: Gate/operation IDs referenced in output
        referenced_rank_values: Rank values referenced in output
        output_type: EXPLANATION or REPAIR_SUGGESTION
        requires_algorithm_rerun: True for repair suggestions
        validation_status: Result of constitutional validation
    """
    training_example_id: str
    source_dataset_row_id: str
    source_trace_id: str
    source_algorithm: str
    operation: TraceConsumerOperation
    input_text: str
    target_text: str
    referenced_candidate_ids: Tuple[str, ...]
    referenced_residual_ids: Tuple[str, ...]
    referenced_gate_ids: Tuple[str, ...]
    referenced_rank_values: Tuple[str, ...]
    output_type: OutputType
    requires_algorithm_rerun: bool
    validation_status: ValidationStatus
