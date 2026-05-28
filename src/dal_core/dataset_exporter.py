"""
Dataset Exporter Contract (عقد مصدّر مجموعة البيانات)

PR #146: Export validated dataset rows to training format.

Constitutional Laws:
    1. Export ONLY DatasetRow with validation_status == VALID
    2. Export MUST preserve source_trace_id
    3. Export MUST preserve source_dataset_row_id
    4. Export MUST reject forbidden authority fields/phrases
    5. Export MUST NOT create candidates
    6. Export MUST NOT upgrade rank
    7. Export MUST NOT delete residuals
    8. Export MUST NOT close ifādah
    9. Export MUST NOT produce hukm
    10. Export MUST NOT produce reality
    11. Export MUST NOT include raw Arabic as authority
    12. Repair examples MUST preserve requires_algorithm_rerun=True

Forbidden Content Detection:
    ❌ "final_answer"
    ❌ "correct_analysis"
    ❌ "gold_label_hukm"
    ❌ "resolved_residuals"
    ❌ "upgraded_rank"
    ❌ "closed_ifadah"
    ❌ "produced_hukm"
    ❌ "produced_reality"
    ❌ "new_candidate"
    ❌ "semantic_certainty"
    ❌ "resolved_output"

Constitutional Formula:
    DatasetRow → TrainingExample → JSONL Export
    (Protected serialization boundary, NOT authority)

Supreme Law:
    Dataset export is serialization, NOT evaluation.
    Dataset export is serialization, NOT training.
    Dataset export is serialization, NOT analysis.

Reference:
    User requirement: PR #146 specification (2026-05-28)
    Builds on: PR #141, PR #142, PR #145

Created: 2026-05-28
"""

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Tuple
from uuid import uuid4

from dal_core.trace_explanation_dataset_generator import (
    DatasetRow,
    ValidationStatus,
    OutputType,
)
from dal_core.training_example import TrainingExample


# ============================================================================
# Dataset Export Residual
# ============================================================================

@dataclass(frozen=True)
class DatasetExportResidual:
    """
    Residual about dataset export process (NOT about Arabic analysis).

    Constitutional Law:
        These residuals record issues with export validation itself,
        NOT issues with Arabic linguistic analysis.

    Fields:
        issue_type: Type of export issue
        message: Description of the issue
        rejected_content: Content that failed validation (if applicable)
    """
    issue_type: str
    message: str
    rejected_content: str = ""


# ============================================================================
# Dataset Export Result
# ============================================================================

@dataclass(frozen=True)
class DatasetExportResult:
    """
    Result of dataset export operation.

    Constitutional Law:
        Export result is success/failure indicator for serialization,
        NOT a judgment about Arabic analysis quality.

    Fields:
        success: Whether export succeeded
        exported_count: Number of examples successfully exported
        rejected_count: Number of examples rejected
        residuals: Issues encountered during export (if any)
        output_path: Path to exported JSONL file (if success)
    """
    success: bool
    exported_count: int
    rejected_count: int
    residuals: Tuple[DatasetExportResidual, ...]
    output_path: str = ""


# ============================================================================
# Forbidden Authority Phrases
# ============================================================================

FORBIDDEN_AUTHORITY_PHRASES = frozenset([
    "final_answer",
    "correct_analysis",
    "gold_label_hukm",
    "resolved_residuals",
    "upgraded_rank",
    "closed_ifadah",
    "produced_hukm",
    "produced_reality",
    "new_candidate",
    "semantic_certainty",
    "resolved_output",
    "final analysis",
    "correct answer",
    "true meaning",
    "definitive interpretation",
    "resolved",
    "upgraded to",
    "closed ifadah",
    "produces hukm",
    "establishes reality",
    "creates candidate",
])


# ============================================================================
# Dataset Exporter
# ============================================================================

class DatasetExporter:
    """
    Export validated dataset rows to training format with constitutional safeguards.

    Constitutional Laws:
        1. Only DatasetRow → TrainingExample conversion allowed
        2. All conversions preserve source_trace_id and source_dataset_row_id
        3. Only VALID validation_status rows are exported
        4. Forbidden authority phrases are detected and rejected
        5. Repair examples must preserve requires_algorithm_rerun=True

    Forbidden Operations:
        ❌ export_from_raw_arabic(): Raw Arabic is NOT export input
        ❌ upgrade_rank(): Export does NOT upgrade rank
        ❌ resolve_residuals(): Export does NOT resolve residuals
        ❌ close_ifadah(): Export does NOT close ifādah
        ❌ produce_hukm(): Export does NOT produce hukm
        ❌ produce_reality(): Export does NOT produce reality
        ❌ create_candidate(): Export does NOT create candidates

    Permitted Operations:
        ✅ dataset_row_to_training_example(): Convert validated DatasetRow
        ✅ validate_training_example(): Validate constitutional compliance
        ✅ export_to_jsonl(): Serialize to JSONL format
    """

    @staticmethod
    def dataset_row_to_training_example(row: DatasetRow) -> TrainingExample:
        """
        Convert DatasetRow to TrainingExample.

        Constitutional Requirements:
            1. row.validation_status MUST be VALID
            2. Preserves source_trace_id
            3. Preserves source_dataset_row_id
            4. Preserves all trace bindings
            5. Repair examples preserve requires_algorithm_rerun=True

        Args:
            row: Source DatasetRow (immutable)

        Returns:
            TrainingExample with all source bindings preserved

        Raises:
            ValueError: If row.validation_status is not VALID
        """
        # Validate that row is VALID (constitutional requirement)
        if row.validation_status != ValidationStatus.VALID:
            raise ValueError(
                f"Constitutional violation: Cannot export DatasetRow with "
                f"validation_status {row.validation_status}. "
                f"Only VALID rows may be exported to training format."
            )

        # Validate repair examples preserve requires_algorithm_rerun
        if row.output_type == OutputType.REPAIR_SUGGESTION:
            if not row.requires_algorithm_rerun:
                raise ValueError(
                    "Constitutional violation: REPAIR_SUGGESTION rows MUST have "
                    "requires_algorithm_rerun=True. T5 suggests repairs; T5 does NOT execute repairs."
                )

        # Generate training example ID
        training_example_id = f"training_example_{uuid4().hex[:16]}"

        # Create immutable TrainingExample
        return TrainingExample(
            training_example_id=training_example_id,
            source_dataset_row_id=row.dataset_row_id,
            source_trace_id=row.source_trace_id,
            source_algorithm=row.source_algorithm,
            operation=row.operation,
            input_text=row.input_trace_summary,
            target_text=row.target_output_text,
            referenced_candidate_ids=row.referenced_candidate_ids,
            referenced_residual_ids=row.referenced_residual_ids,
            referenced_gate_ids=row.referenced_gate_ids,
            referenced_rank_values=row.referenced_rank_values,
            output_type=row.output_type,
            requires_algorithm_rerun=row.requires_algorithm_rerun,
            validation_status=row.validation_status,
        )

    @staticmethod
    def validate_training_example(example: TrainingExample) -> DatasetExportResult:
        """
        Validate TrainingExample for constitutional compliance.

        Constitutional Validation:
            1. validation_status MUST be VALID
            2. Forbidden authority phrases MUST NOT appear in input_text or target_text
            3. Repair examples MUST have requires_algorithm_rerun=True
            4. All source bindings MUST be preserved

        Args:
            example: TrainingExample to validate

        Returns:
            DatasetExportResult indicating success or rejection with residuals
        """
        residuals = []

        # Check validation_status
        if example.validation_status != ValidationStatus.VALID:
            residuals.append(
                DatasetExportResidual(
                    issue_type="invalid_validation_status",
                    message=f"TrainingExample has validation_status {example.validation_status}, expected VALID",
                )
            )

        # Check for forbidden authority phrases in input_text
        input_lower = example.input_text.lower()
        for phrase in FORBIDDEN_AUTHORITY_PHRASES:
            if phrase in input_lower:
                residuals.append(
                    DatasetExportResidual(
                        issue_type="forbidden_authority_phrase_in_input",
                        message=f"Forbidden phrase '{phrase}' found in input_text",
                        rejected_content=phrase,
                    )
                )

        # Check for forbidden authority phrases in target_text
        target_lower = example.target_text.lower()
        for phrase in FORBIDDEN_AUTHORITY_PHRASES:
            if phrase in target_lower:
                residuals.append(
                    DatasetExportResidual(
                        issue_type="forbidden_authority_phrase_in_target",
                        message=f"Forbidden phrase '{phrase}' found in target_text",
                        rejected_content=phrase,
                    )
                )

        # Validate repair examples
        if example.output_type == OutputType.REPAIR_SUGGESTION:
            if not example.requires_algorithm_rerun:
                residuals.append(
                    DatasetExportResidual(
                        issue_type="repair_without_algorithm_rerun",
                        message="REPAIR_SUGGESTION example must have requires_algorithm_rerun=True",
                    )
                )

        # Check source bindings
        if not example.source_trace_id:
            residuals.append(
                DatasetExportResidual(
                    issue_type="missing_source_trace_id",
                    message="TrainingExample must preserve source_trace_id",
                )
            )

        if not example.source_dataset_row_id:
            residuals.append(
                DatasetExportResidual(
                    issue_type="missing_source_dataset_row_id",
                    message="TrainingExample must preserve source_dataset_row_id",
                )
            )

        # Return result
        if residuals:
            return DatasetExportResult(
                success=False,
                exported_count=0,
                rejected_count=1,
                residuals=tuple(residuals),
            )
        else:
            return DatasetExportResult(
                success=True,
                exported_count=1,
                rejected_count=0,
                residuals=(),
            )

    @staticmethod
    def export_to_jsonl(
        examples: Tuple[TrainingExample, ...],
        output_path: Path,
    ) -> DatasetExportResult:
        """
        Export validated TrainingExamples to JSONL format.

        Constitutional Requirements:
            1. All examples MUST pass validation
            2. All examples MUST have validation_status == VALID
            3. All examples MUST preserve source bindings
            4. JSONL output MUST be UTF-8 encoded
            5. Each line is valid JSON object

        JSONL Format:
            Each line contains a JSON object with fields:
                - training_example_id
                - source_dataset_row_id
                - source_trace_id
                - source_algorithm
                - operation
                - input_text
                - target_text
                - referenced_candidate_ids
                - referenced_residual_ids
                - referenced_gate_ids
                - referenced_rank_values
                - output_type
                - requires_algorithm_rerun
                - validation_status

        Args:
            examples: Tuple of TrainingExample instances to export
            output_path: Path where JSONL file will be written

        Returns:
            DatasetExportResult with success/failure and counts
        """
        residuals = []
        exported_count = 0
        rejected_count = 0

        # Validate all examples before export
        validated_examples = []
        for example in examples:
            validation_result = DatasetExporter.validate_training_example(example)
            if validation_result.success:
                validated_examples.append(example)
                exported_count += 1
            else:
                rejected_count += 1
                residuals.extend(validation_result.residuals)

        # Export validated examples to JSONL
        if validated_examples:
            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    for example in validated_examples:
                        # Convert TrainingExample to dict
                        example_dict = {
                            'training_example_id': example.training_example_id,
                            'source_dataset_row_id': example.source_dataset_row_id,
                            'source_trace_id': example.source_trace_id,
                            'source_algorithm': example.source_algorithm,
                            'operation': example.operation.name,
                            'input_text': example.input_text,
                            'target_text': example.target_text,
                            'referenced_candidate_ids': list(example.referenced_candidate_ids),
                            'referenced_residual_ids': list(example.referenced_residual_ids),
                            'referenced_gate_ids': list(example.referenced_gate_ids),
                            'referenced_rank_values': list(example.referenced_rank_values),
                            'output_type': example.output_type.name,
                            'requires_algorithm_rerun': example.requires_algorithm_rerun,
                            'validation_status': example.validation_status.name,
                        }
                        # Write as single-line JSON
                        f.write(json.dumps(example_dict, ensure_ascii=False) + '\n')

                return DatasetExportResult(
                    success=True,
                    exported_count=exported_count,
                    rejected_count=rejected_count,
                    residuals=tuple(residuals),
                    output_path=str(output_path),
                )
            except (IOError, OSError) as e:
                residuals.append(
                    DatasetExportResidual(
                        issue_type="file_write_error",
                        message=f"Failed to write JSONL file: {str(e)}",
                    )
                )
                return DatasetExportResult(
                    success=False,
                    exported_count=0,
                    rejected_count=len(examples),
                    residuals=tuple(residuals),
                )
        else:
            # No valid examples to export
            return DatasetExportResult(
                success=False,
                exported_count=0,
                rejected_count=rejected_count,
                residuals=tuple(residuals),
            )
