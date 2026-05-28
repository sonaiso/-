"""
Trace Explanation Dataset Generator (مولّد مجموعة بيانات شرح الأثر)

PR #145: Generate supervised training/evaluation datasets from governed traces only.

Constitutional Laws:
    1. Dataset rows are derived ONLY from AlgorithmTracePayload
    2. Dataset rows MUST preserve source_trace_id
    3. Dataset generation MUST NOT analyze raw Arabic text
    4. Dataset generation MUST NOT invent candidate/residual/gate/rank references
    5. Dataset generation MUST NOT upgrade rank
    6. Dataset generation MUST NOT resolve residuals
    7. Dataset generation MUST NOT close ifādah
    8. Dataset generation MUST NOT produce hukm or reality
    9. All dataset rows MUST pass GovernedTraceT5Contract validation

Forbidden Pipeline:
    ❌ Raw Arabic → Dataset Row
    ❌ Unvalidated Explanation → Dataset Row
    ❌ Invented References → Dataset Row

Permitted Pipeline:
    ✅ AlgorithmTracePayload + ExplanationCandidate → DatasetRow
    ✅ AlgorithmTracePayload + RepairSuggestionCandidate → DatasetRow
    ✅ Golden Fixtures → DatasetRow

Constitutional Formula:
    الجبر = الدستور (Algebra = Constitution)
    الخوارزمية = تنفيذ الدستور (Algorithm = Constitutional Execution)
    AlgorithmTracePayload = أثر التنفيذ (Trace = Execution Evidence)
    DatasetRow = تدريس من الأثر (Dataset = Teaching from Trace)

Supreme Law:
    Dataset is replay/teaching artifact derived from traces.
    Dataset is NOT an authority that creates analysis, rank, residual resolution,
    ifādah, hukm, or reality.

Reference:
    User requirement: Trace-based dataset generator specification (2026-05-28)
    Builds on: PR #141, PR #142, PR #144

Created: 2026-05-28
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple
from uuid import uuid4

from dal_core.algorithm_trace_payload import (
    AlgorithmTracePayload,
    TraceConsumerOperation,
)
from dal_core.governed_trace_t5_contract import (
    ExplanationCandidate,
    RepairSuggestionCandidate,
    GovernedTraceT5Validator,
)
from dal_core.foundation import Rank


# ============================================================================
# Dataset Row Output Type
# ============================================================================

class OutputType(Enum):
    """
    Type of output for dataset row.

    Constitutional Classification:
        EXPLANATION: Explains existing trace without creating new facts
        REPAIR_SUGGESTION: Suggests repair requiring algorithm rerun (NOT execution)
    """
    EXPLANATION = auto()
    REPAIR_SUGGESTION = auto()


# ============================================================================
# Dataset Row Validation Status
# ============================================================================

class ValidationStatus(Enum):
    """
    Validation status of dataset row.

    Constitutional Classification:
        VALID: All references exist in source trace, passes all validation
        REJECTED_INVENTED_REFERENCES: Contains references not in source trace
        REJECTED_RAW_ARABIC: Attempt to generate from raw Arabic
        REJECTED_VALIDATION_FAILURE: Failed GovernedTraceT5Contract validation
        REJECTED_FORBIDDEN_OPERATION: Contains forbidden operation claims
    """
    VALID = auto()
    REJECTED_INVENTED_REFERENCES = auto()
    REJECTED_RAW_ARABIC = auto()
    REJECTED_VALIDATION_FAILURE = auto()
    REJECTED_FORBIDDEN_OPERATION = auto()


# ============================================================================
# Dataset Generation Residual
# ============================================================================

@dataclass(frozen=True)
class DatasetGenerationResidual:
    """
    Residual about dataset generation process (NOT about Arabic analysis).

    Constitutional Law:
        These residuals record issues with dataset generation itself,
        NOT issues with Arabic linguistic analysis.

    Fields:
        issue_type: Type of generation issue
        message: Description of the issue
        rejected_references: References that failed validation (if applicable)
    """
    issue_type: str
    message: str
    rejected_references: Tuple[str, ...] = ()


# ============================================================================
# Dataset Row
# ============================================================================

@dataclass(frozen=True)
class DatasetRow:
    """
    Single row in trace explanation dataset.

    Constitutional Requirements:
        - All fields are immutable (frozen dataclass)
        - source_trace_id MUST match AlgorithmTracePayload.trace_id
        - All referenced_* fields MUST reference elements that exist in source trace
        - output_type determines interpretation of target_output_text
        - requires_algorithm_rerun MUST be True for REPAIR_SUGGESTION rows
        - validation_status records constitutional validation result

    Forbidden Fields:
        ❌ upgraded_rank: Dataset does NOT upgrade rank
        ❌ resolved_residuals: Dataset does NOT resolve residuals
        ❌ closed_ifadah: Dataset does NOT close ifādah
        ❌ produced_hukm: Dataset does NOT produce hukm
        ❌ produced_reality: Dataset does NOT produce reality
        ❌ raw_arabic_source: Dataset does NOT analyze raw Arabic
        ❌ new_candidate: Dataset does NOT create candidates
        ❌ semantic_certainty: Dataset does NOT produce semantic certainty
        ❌ final_answer: Dataset does NOT assert final answers
        ❌ correct_analysis: Dataset does NOT assert correct analysis
        ❌ gold_label_hukm: Dataset does NOT assert gold label hukm
        ❌ resolved_output: Dataset does NOT assert resolved outputs

    Fields:
        dataset_row_id: Unique identifier for this dataset row
        source_trace_id: trace_id from AlgorithmTracePayload (CONSTITUTIONAL BINDING)
        source_algorithm: Algorithm that produced the trace
        operation: TraceConsumerOperation performed
        input_trace_summary: Summary of input trace for context
        target_output_text: Natural language explanation or repair suggestion
        referenced_candidate_ids: Candidate IDs referenced in output (MUST exist in trace)
        referenced_residual_ids: Residual IDs referenced in output (MUST exist in trace)
        referenced_gate_ids: Gate/operation IDs referenced in output (MUST exist in trace)
        referenced_rank_values: Rank values referenced in output (MUST exist in trace)
        output_type: EXPLANATION or REPAIR_SUGGESTION
        requires_algorithm_rerun: True for repair suggestions (constitutional requirement)
        validation_status: Result of constitutional validation
        residuals_about_dataset_generation: Issues with dataset generation (if any)
    """
    dataset_row_id: str
    source_trace_id: str
    source_algorithm: str
    operation: TraceConsumerOperation
    input_trace_summary: str
    target_output_text: str
    referenced_candidate_ids: Tuple[str, ...]
    referenced_residual_ids: Tuple[str, ...]
    referenced_gate_ids: Tuple[str, ...]
    referenced_rank_values: Tuple[str, ...]
    output_type: OutputType
    requires_algorithm_rerun: bool
    validation_status: ValidationStatus
    residuals_about_dataset_generation: Tuple[DatasetGenerationResidual, ...]


# ============================================================================
# Dataset Generator
# ============================================================================

class TraceExplanationDatasetGenerator:
    """
    Generate supervised training/evaluation datasets from governed traces.

    Constitutional Laws:
        1. Generator consumes ONLY AlgorithmTracePayload (NO raw Arabic)
        2. Generator produces ONLY DatasetRow (NO candidates, rank, ifādah, hukm, reality)
        3. All references MUST exist in source trace
        4. All dataset rows MUST pass GovernedTraceT5Contract validation

    Forbidden Operations:
        ❌ generate_from_raw_arabic(): Raw Arabic is NOT dataset input
        ❌ upgrade_rank(): Dataset does NOT upgrade rank
        ❌ resolve_residuals(): Dataset does NOT resolve residuals
        ❌ close_ifadah(): Dataset does NOT close ifādah
        ❌ produce_hukm(): Dataset does NOT produce hukm
        ❌ produce_reality(): Dataset does NOT produce reality
        ❌ invent_references(): All references MUST exist in trace

    Permitted Operations:
        ✅ generate_from_explanation_candidate(): Generate from validated explanation
        ✅ generate_from_repair_suggestion_candidate(): Generate from validated repair suggestion
        ✅ validate_references(): Ensure all references exist in trace
    """

    @staticmethod
    def generate_from_explanation_candidate(
        trace: AlgorithmTracePayload,
        explanation: ExplanationCandidate,
    ) -> DatasetRow:
        """
        Generate dataset row from validated ExplanationCandidate.

        Constitutional Requirements:
            1. explanation.source_trace_id MUST match trace.trace_id
            2. All references in explanation MUST exist in trace
            3. explanation MUST pass GovernedTraceT5Contract validation
            4. Generated row preserves all trace bindings

        Args:
            trace: Source algorithm trace (immutable)
            explanation: Validated explanation candidate (immutable)

        Returns:
            DatasetRow with validation_status indicating success/rejection

        Raises:
            ValueError: If trace_id mismatch (constitutional violation)
        """
        # Validate trace_id binding (CONSTITUTIONAL REQUIREMENT)
        if explanation.source_trace_id != trace.trace_id:
            raise ValueError(
                f"Constitutional violation: explanation.source_trace_id "
                f"'{explanation.source_trace_id}' does not match "
                f"trace.trace_id '{trace.trace_id}'. "
                f"Explanations MUST bind to specific trace instances."
            )

        # Validate explanation against contract
        residuals = []
        validation_status = ValidationStatus.VALID

        try:
            GovernedTraceT5Validator.validate_explanation(explanation)
            GovernedTraceT5Validator.validate_explanation_references(
                explanation, trace
            )
        except (ValueError, TypeError) as e:
            validation_status = ValidationStatus.REJECTED_VALIDATION_FAILURE
            residuals.append(
                DatasetGenerationResidual(
                    issue_type="validation_failure",
                    message=str(e),
                )
            )

        # Extract references from explanation
        referenced_candidate_ids = explanation.referenced_candidate_ids
        referenced_residual_ids = explanation.referenced_residual_ids
        referenced_gate_ids = explanation.referenced_gate_ids
        referenced_rank_values = tuple(explanation.referenced_rank_values)

        # Create input trace summary (NO raw surface - trace metadata only)
        input_trace_summary = (
            f"Trace ID: {trace.trace_id}, "
            f"Algorithm: {trace.source_algorithm}, "
            f"Layer: {trace.source_layer}, "
            f"Candidates: {len(trace.candidates)}, "
            f"Residuals: {sum(len(c.residual_payload.residuals.residuals) for c in trace.candidates)}"
        )

        # Generate dataset row
        return DatasetRow(
            dataset_row_id=f"dataset_row_{uuid4().hex[:16]}",
            source_trace_id=trace.trace_id,
            source_algorithm=trace.source_algorithm,
            operation=explanation.operation,
            input_trace_summary=input_trace_summary,
            target_output_text=explanation.explanation_text,
            referenced_candidate_ids=referenced_candidate_ids,
            referenced_residual_ids=referenced_residual_ids,
            referenced_gate_ids=referenced_gate_ids,
            referenced_rank_values=referenced_rank_values,
            output_type=OutputType.EXPLANATION,
            requires_algorithm_rerun=False,
            validation_status=validation_status,
            residuals_about_dataset_generation=tuple(residuals),
        )

    @staticmethod
    def generate_from_repair_suggestion_candidate(
        trace: AlgorithmTracePayload,
        repair: RepairSuggestionCandidate,
    ) -> DatasetRow:
        """
        Generate dataset row from validated RepairSuggestionCandidate.

        Constitutional Requirements:
            1. repair.source_trace_id MUST match trace.trace_id
            2. repair.requires_algorithm_rerun MUST be True
            3. All references in repair MUST exist in trace
            4. repair MUST pass GovernedTraceT5Contract validation
            5. Generated row preserves all trace bindings

        Args:
            trace: Source algorithm trace (immutable)
            repair: Validated repair suggestion candidate (immutable)

        Returns:
            DatasetRow with validation_status indicating success/rejection

        Raises:
            ValueError: If trace_id mismatch or requires_algorithm_rerun is False
        """
        # Validate trace_id binding (CONSTITUTIONAL REQUIREMENT)
        if repair.source_trace_id != trace.trace_id:
            raise ValueError(
                f"Constitutional violation: repair.source_trace_id "
                f"'{repair.source_trace_id}' does not match "
                f"trace.trace_id '{trace.trace_id}'. "
                f"Repair suggestions MUST bind to specific trace instances."
            )

        # Validate requires_algorithm_rerun (CONSTITUTIONAL REQUIREMENT)
        if not repair.requires_algorithm_rerun:
            raise ValueError(
                "Constitutional violation: RepairSuggestionCandidate.requires_algorithm_rerun "
                "MUST be True. T5 suggests repairs; T5 does NOT execute repairs."
            )

        # Validate repair against contract
        residuals = []
        validation_status = ValidationStatus.VALID

        try:
            GovernedTraceT5Validator.validate_repair_suggestion(repair)
            # RepairSuggestionCandidate has different fields than ExplanationCandidate
            # It doesn't have referenced_* fields, so we validate its own fields
        except (ValueError, TypeError) as e:
            validation_status = ValidationStatus.REJECTED_VALIDATION_FAILURE
            residuals.append(
                DatasetGenerationResidual(
                    issue_type="validation_failure",
                    message=str(e),
                )
            )

        # Extract references from repair suggestion
        # RepairSuggestionCandidate doesn't have the same reference structure
        # It has blocked_by_residual_ids and suggested_gate
        referenced_candidate_ids = ()  # Not present in RepairSuggestionCandidate
        referenced_residual_ids = repair.blocked_by_residual_ids
        referenced_gate_ids = (repair.suggested_gate,) if repair.suggested_gate else ()
        referenced_rank_values = ()  # Repair suggestions don't reference ranks

        # Validate that residuals exist in trace
        if validation_status == ValidationStatus.VALID:
            valid_residual_ids = set()
            for cand in trace.candidates:
                residual_set = cand.residual_payload.residuals
                for residual in residual_set.residuals:
                    valid_residual_ids.add(str(residual))

            for ref_id in referenced_residual_ids:
                if ref_id not in valid_residual_ids:
                    validation_status = ValidationStatus.REJECTED_VALIDATION_FAILURE
                    residuals.append(
                        DatasetGenerationResidual(
                            issue_type="validation_failure",
                            message=f"Repair references residual_id '{ref_id}' not found in trace",
                        )
                    )
                    break

        # Validate that suggested_gate exists in trace provenance (CONSTITUTIONAL REQUIREMENT)
        if validation_status == ValidationStatus.VALID and repair.suggested_gate:
            gate_found = False

            # Check in candidate residual_sources
            for cand in trace.candidates:
                if hasattr(cand, 'residual_payload') and hasattr(cand.residual_payload, 'residual_sources'):
                    if repair.suggested_gate in cand.residual_payload.residual_sources:
                        gate_found = True
                        break

            # Check in candidate trace/operation provenance
            if not gate_found:
                for cand in trace.candidates:
                    if hasattr(cand, 'trace') and repair.suggested_gate in cand.trace:
                        gate_found = True
                        break

            # Check in residual locations
            if not gate_found:
                for cand in trace.candidates:
                    if hasattr(cand, 'residual_payload'):
                        residual_set = cand.residual_payload.residuals
                        for residual in residual_set.residuals:
                            if hasattr(residual, 'location') and residual.location == repair.suggested_gate:
                                gate_found = True
                                break
                        if gate_found:
                            break

            if not gate_found:
                validation_status = ValidationStatus.REJECTED_INVENTED_REFERENCES
                residuals.append(
                    DatasetGenerationResidual(
                        issue_type="invented_gate_reference",
                        message=f"Repair suggests gate '{repair.suggested_gate}' not found in trace provenance",
                        rejected_references=(repair.suggested_gate,),
                    )
                )

        # Create input trace summary (NO raw surface - trace metadata only)
        input_trace_summary = (
            f"Trace ID: {trace.trace_id}, "
            f"Algorithm: {trace.source_algorithm}, "
            f"Layer: {trace.source_layer}, "
            f"Candidates: {len(trace.candidates)}, "
            f"Residuals: {sum(len(c.residual_payload.residuals.residuals) for c in trace.candidates)}, "
            f"Blocking Residuals: {len(repair.blocked_by_residual_ids)}"
        )

        # Generate dataset row
        return DatasetRow(
            dataset_row_id=f"dataset_row_{uuid4().hex[:16]}",
            source_trace_id=trace.trace_id,
            source_algorithm=trace.source_algorithm,
            operation=TraceConsumerOperation.SUGGEST_REPAIR,  # Hardcoded for repair suggestions
            input_trace_summary=input_trace_summary,
            target_output_text=repair.explanation,  # Field is 'explanation' not 'suggestion_text'
            referenced_candidate_ids=referenced_candidate_ids,
            referenced_residual_ids=referenced_residual_ids,
            referenced_gate_ids=referenced_gate_ids,
            referenced_rank_values=referenced_rank_values,
            output_type=OutputType.REPAIR_SUGGESTION,
            requires_algorithm_rerun=True,
            validation_status=validation_status,
            residuals_about_dataset_generation=tuple(residuals),
        )

    @staticmethod
    def reject_raw_arabic(raw_text: str) -> DatasetRow:
        """
        Reject raw Arabic text as dataset input (CONSTITUTIONAL GUARD).

        This method exists to explicitly demonstrate that raw Arabic
        text CANNOT become a dataset row.

        Args:
            raw_text: Raw Arabic text (REJECTED)

        Returns:
            DatasetRow with validation_status=REJECTED_RAW_ARABIC

        Constitutional Law:
            Dataset rows are derived from traces, NOT from raw Arabic analysis.
        """
        return DatasetRow(
            dataset_row_id=f"dataset_row_rejected_{uuid4().hex[:16]}",
            source_trace_id="<no_trace>",
            source_algorithm="<no_algorithm>",
            operation=TraceConsumerOperation.EXPLAIN_TRACE,
            input_trace_summary="<raw_arabic_rejected>",
            target_output_text="",
            referenced_candidate_ids=(),
            referenced_residual_ids=(),
            referenced_gate_ids=(),
            referenced_rank_values=(),
            output_type=OutputType.EXPLANATION,
            requires_algorithm_rerun=False,
            validation_status=ValidationStatus.REJECTED_RAW_ARABIC,
            residuals_about_dataset_generation=(
                DatasetGenerationResidual(
                    issue_type="raw_arabic_input",
                    message=(
                        f"Raw Arabic text '{raw_text}' cannot become dataset row. "
                        f"Dataset rows MUST be derived from AlgorithmTracePayload only."
                    ),
                ),
            ),
        )
