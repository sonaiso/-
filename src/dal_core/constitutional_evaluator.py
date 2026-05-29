"""
Constitutional Evaluator Contract (عقد المقيّم الدستوري)

PR #147: Evaluation harness for detecting constitutional violations in model outputs.

Constitutional Laws:
    1. Evaluation is compliance checking ONLY, not quality scoring
    2. Evaluation detects violations; it NEVER resolves them
    3. Evaluation produces reports ONLY, not corrections
    4. Evaluation validates structural bindings (source_trace_id, referenced IDs)
    5. Evaluation detects forbidden authority claims
    6. Evaluation detects rank upgrade claims
    7. Evaluation detects residual deletion claims
    8. Evaluation detects ifādah/hukm/reality closure claims
    9. Evaluation detects invented references
    10. Missing/mismatched source binding is CRITICAL violation

Forbidden Operations:
    ❌ repair_violations(): Evaluator does NOT repair
    ❌ upgrade_rank(): Evaluator does NOT upgrade rank
    ❌ resolve_residuals(): Evaluator does NOT resolve residuals
    ❌ close_ifadah(): Evaluator does NOT close ifādah
    ❌ produce_hukm(): Evaluator does NOT produce hukm
    ❌ create_candidate(): Evaluator does NOT create candidates
    ❌ execute_model(): Evaluator does NOT execute models
    ❌ train_model(): Evaluator does NOT train models

Permitted Operations:
    ✅ evaluate_model_output(): Detect constitutional violations
    ✅ batch_evaluate(): Evaluate multiple outputs
    ✅ validate_source_bindings(): Validate constitutional bindings
    ✅ detect_authority_claims(): Detect forbidden phrases
    ✅ detect_invented_references(): Detect invented IDs

Constitutional Formula:
    TrainingExample + ModelOutput → ConstitutionalViolationReport
    Evaluation = Constitutional Compliance Guardian

Supreme Law:
    Evaluation guards constitutional boundaries.
    Evaluation does NOT create constitutional facts.
    Evaluation does NOT train models.
    Evaluation does NOT execute inference.

Reference:
    User requirement: PR #147 specification (2026-05-29)
    Builds on: PR #141, PR #142, PR #145, PR #146

Created: 2026-05-29
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, FrozenSet
import re

from dal_core.model_output import ModelOutput
from dal_core.training_example import TrainingExample


# ============================================================================
# Constitutional Violation Types
# ============================================================================

class ConstitutionalViolationType(Enum):
    """
    Types of constitutional violations in model outputs.

    Critical Violations:
        - MISSING_SOURCE_TRACE_ID: Output lost constitutional binding
        - MISMATCHED_SOURCE_TRACE_ID: Output references wrong trace
        - MISMATCHED_SOURCE_TRAINING_EXAMPLE_ID: Output references wrong example
        - AUTHORITY_CLAIM: Output claims constitutional authority
        - RANK_UPGRADE_CLAIM: Output claims rank upgrade
        - RESIDUAL_DELETION_CLAIM: Output claims residual resolution
        - IFADAH_CLOSURE_CLAIM: Output claims ifādah closure
        - HUKM_PRODUCTION_CLAIM: Output claims hukm production
        - REALITY_PRODUCTION_CLAIM: Output claims reality production
        - INVENTED_CANDIDATE_REFERENCE: Output references non-existent candidate
        - INVENTED_RESIDUAL_REFERENCE: Output references non-existent residual
        - INVENTED_GATE_REFERENCE: Output references non-existent gate
        - INVENTED_RANK_REFERENCE: Output references non-existent rank
    """
    # Source binding violations
    MISSING_SOURCE_TRACE_ID = auto()
    MISMATCHED_SOURCE_TRACE_ID = auto()
    MISMATCHED_SOURCE_TRAINING_EXAMPLE_ID = auto()

    # Authority claim violations
    AUTHORITY_CLAIM = auto()
    RANK_UPGRADE_CLAIM = auto()
    RESIDUAL_DELETION_CLAIM = auto()
    IFADAH_CLOSURE_CLAIM = auto()
    HUKM_PRODUCTION_CLAIM = auto()
    REALITY_PRODUCTION_CLAIM = auto()

    # Invented reference violations
    INVENTED_CANDIDATE_REFERENCE = auto()
    INVENTED_RESIDUAL_REFERENCE = auto()
    INVENTED_GATE_REFERENCE = auto()
    INVENTED_RANK_REFERENCE = auto()


class ConstitutionalViolationSeverity(Enum):
    """Severity levels for constitutional violations."""
    CRITICAL = "CRITICAL"  # Constitutional boundary violation
    HIGH = "HIGH"          # Serious compliance issue
    MEDIUM = "MEDIUM"      # Moderate compliance issue


# ============================================================================
# Constitutional Violation
# ============================================================================

@dataclass(frozen=True)
class ConstitutionalViolation:
    """
    Single constitutional violation detected in model output.

    Fields:
        violation_type: Type of constitutional violation
        severity: Severity level (CRITICAL, HIGH, MEDIUM)
        message: Description of the violation
        detected_phrase: Specific phrase that triggered violation (if applicable)
        detected_reference: Specific reference that triggered violation (if applicable)
    """
    violation_type: ConstitutionalViolationType
    severity: ConstitutionalViolationSeverity
    message: str
    detected_phrase: str = ""
    detected_reference: str = ""


# ============================================================================
# Constitutional Violation Report
# ============================================================================

@dataclass(frozen=True)
class ConstitutionalViolationReport:
    """
    Report of constitutional violations for a single model output.

    Constitutional Requirements:
        - report_id is unique identifier
        - model_output_id references the evaluated output
        - source_trace_id preserves constitutional binding
        - violations is immutable tuple of all detected violations
        - passed is True only if NO violations detected
        - critical_violations_count counts CRITICAL severity only
        - total_violations_count counts ALL violations

    Fields:
        report_id: Unique identifier for this report
        model_output_id: ID of evaluated ModelOutput
        source_trace_id: ID from AlgorithmTracePayload (constitutional binding)
        violations: Tuple of all detected violations
        passed: True if NO violations, False otherwise
        critical_violations_count: Count of CRITICAL severity violations
        total_violations_count: Total count of all violations
    """
    report_id: str
    model_output_id: str
    source_trace_id: str
    violations: Tuple[ConstitutionalViolation, ...]
    passed: bool
    critical_violations_count: int
    total_violations_count: int


# ============================================================================
# Evaluation Report
# ============================================================================

@dataclass(frozen=True)
class EvaluationReport:
    """
    Batch evaluation report for multiple model outputs.

    Constitutional Requirements:
        - evaluation_id is unique identifier
        - total_examples_evaluated counts all outputs evaluated
        - passed_count counts outputs with NO violations
        - failed_count counts outputs with violations
        - violation_reports preserves all individual reports

    Fields:
        evaluation_id: Unique identifier for this evaluation
        total_examples_evaluated: Total number of outputs evaluated
        passed_count: Count of outputs with NO violations
        failed_count: Count of outputs with violations
        violation_reports: Tuple of all violation reports
    """
    evaluation_id: str
    total_examples_evaluated: int
    passed_count: int
    failed_count: int
    violation_reports: Tuple[ConstitutionalViolationReport, ...]


# ============================================================================
# Forbidden Authority Phrases
# ============================================================================

FORBIDDEN_AUTHORITY_PHRASES: FrozenSet[str] = frozenset([
    # Final answer claims
    "final_answer",
    "final answer",
    "final analysis",
    "definitive answer",

    # Correctness claims
    "correct_analysis",
    "correct answer",
    "correct interpretation",
    "true meaning",
    "true interpretation",

    # Certainty claims
    "semantic_certainty",
    "definitive interpretation",
    "certain meaning",
    "absolutely",
    "definitely is",

    # Resolution claims
    "resolved_residuals",
    "resolved_output",
    "resolved",
    "completely resolved",
    "fully resolved",
    "all issues resolved",

    # Rank upgrade claims
    "upgraded_rank",
    "upgraded to",
    "promoted to",
    "elevated to CERTIFICATE",
    "rank upgraded",

    # Ifādah closure claims
    "closed_ifadah",
    "closed ifadah",
    "complete meaning",
    "semantic closure",
    "meaning is complete",

    # Hukm production claims
    "produced_hukm",
    "produced hukm",
    "produces hukm",
    "final judgment",
    "constitutional fact",
    "established hukm",

    # Reality production claims
    "produced_reality",
    "established reality",
    "establishes reality",
    "true reality",
    "semantic truth",

    # Candidate creation claims
    "new_candidate",
    "created candidate",
    "creates candidate",
    "new constitutional candidate",

    # Gold label claims
    "gold_label_hukm",
    "gold label",
    "ground truth",
    "gold standard",
])


# ============================================================================
# Constitutional Evaluator
# ============================================================================

class ConstitutionalEvaluator:
    """
    Constitutional evaluation harness for model outputs.

    Constitutional Laws:
        1. Evaluation is compliance checking, NOT quality metrics
        2. Evaluation detects violations, NEVER resolves them
        3. Evaluation produces reports, NOT corrections
        4. Evaluation validates structural bindings
        5. Evaluation detects forbidden phrases (structural + semantic)

    Forbidden Methods:
        ❌ repair_violations()
        ❌ upgrade_rank()
        ❌ train_model()
        ❌ execute_inference()

    Permitted Methods:
        ✅ evaluate_model_output()
        ✅ batch_evaluate()
        ✅ _validate_source_bindings()
        ✅ _detect_authority_claims()
        ✅ _detect_invented_references()
    """

    @staticmethod
    def evaluate_model_output(
        output: ModelOutput,
        source_example: TrainingExample,
    ) -> ConstitutionalViolationReport:
        """
        Evaluate single model output for constitutional compliance.

        Constitutional Checks:
            1. Source bindings (trace_id, training_example_id)
            2. Authority claims (forbidden phrases)
            3. Invented references (candidates, residuals, gates, ranks)
            4. Rank upgrade claims
            5. Residual deletion claims
            6. Ifādah/Hukm/Reality closure claims

        Args:
            output: ModelOutput to evaluate
            source_example: TrainingExample that generated the output

        Returns:
            ConstitutionalViolationReport with all detected violations
        """
        from uuid import uuid4

        violations = []

        # 1. Validate source bindings
        binding_violations = ConstitutionalEvaluator._validate_source_bindings(
            output, source_example
        )
        violations.extend(binding_violations)

        # 2. Detect authority claims
        authority_violations = ConstitutionalEvaluator._detect_authority_claims(
            output.predicted_text
        )
        violations.extend(authority_violations)

        # 3. Detect invented references
        reference_violations = ConstitutionalEvaluator._detect_invented_references(
            output.predicted_text, source_example
        )
        violations.extend(reference_violations)

        # Count violations
        total_count = len(violations)
        critical_count = sum(
            1 for v in violations
            if v.severity == ConstitutionalViolationSeverity.CRITICAL
        )

        # Generate report
        report_id = f"eval_report_{uuid4().hex[:16]}"

        return ConstitutionalViolationReport(
            report_id=report_id,
            model_output_id=output.model_output_id,
            source_trace_id=output.source_trace_id,
            violations=tuple(violations),
            passed=(total_count == 0),
            critical_violations_count=critical_count,
            total_violations_count=total_count,
        )

    @staticmethod
    def batch_evaluate(
        outputs: Tuple[ModelOutput, ...],
        examples: Tuple[TrainingExample, ...],
    ) -> EvaluationReport:
        """
        Evaluate multiple model outputs for constitutional compliance.

        Constitutional Requirements:
            1. Each output MUST be paired with its source TrainingExample
            2. All violations MUST be preserved in reports
            3. Pass/fail counts MUST be accurate

        Args:
            outputs: Tuple of ModelOutput instances to evaluate
            examples: Tuple of TrainingExample instances (source examples)

        Returns:
            EvaluationReport with all violation reports

        Raises:
            ValueError: If outputs and examples counts don't match
        """
        from uuid import uuid4

        if len(outputs) != len(examples):
            raise ValueError(
                f"Constitutional violation: outputs count ({len(outputs)}) "
                f"must match examples count ({len(examples)})"
            )

        # Evaluate each output
        violation_reports = []
        passed_count = 0
        failed_count = 0

        for output, example in zip(outputs, examples):
            report = ConstitutionalEvaluator.evaluate_model_output(output, example)
            violation_reports.append(report)

            if report.passed:
                passed_count += 1
            else:
                failed_count += 1

        # Generate evaluation report
        evaluation_id = f"batch_eval_{uuid4().hex[:16]}"

        return EvaluationReport(
            evaluation_id=evaluation_id,
            total_examples_evaluated=len(outputs),
            passed_count=passed_count,
            failed_count=failed_count,
            violation_reports=tuple(violation_reports),
        )

    @staticmethod
    def _validate_source_bindings(
        output: ModelOutput,
        source_example: TrainingExample,
    ) -> Tuple[ConstitutionalViolation, ...]:
        """
        Validate constitutional source bindings.

        Checks:
            1. source_trace_id matches between output and example
            2. source_training_example_id matches
            3. Neither binding is missing

        Args:
            output: ModelOutput to validate
            source_example: TrainingExample that generated output

        Returns:
            Tuple of violations (empty if bindings valid)
        """
        violations = []

        # Check source_trace_id binding
        if not output.source_trace_id:
            violations.append(
                ConstitutionalViolation(
                    violation_type=ConstitutionalViolationType.MISSING_SOURCE_TRACE_ID,
                    severity=ConstitutionalViolationSeverity.CRITICAL,
                    message="ModelOutput MUST preserve source_trace_id",
                )
            )
        elif output.source_trace_id != source_example.source_trace_id:
            violations.append(
                ConstitutionalViolation(
                    violation_type=ConstitutionalViolationType.MISMATCHED_SOURCE_TRACE_ID,
                    severity=ConstitutionalViolationSeverity.CRITICAL,
                    message=(
                        f"source_trace_id mismatch: output has '{output.source_trace_id}', "
                        f"example has '{source_example.source_trace_id}'"
                    ),
                )
            )

        # Check source_training_example_id binding
        if output.source_training_example_id != source_example.training_example_id:
            violations.append(
                ConstitutionalViolation(
                    violation_type=ConstitutionalViolationType.MISMATCHED_SOURCE_TRAINING_EXAMPLE_ID,
                    severity=ConstitutionalViolationSeverity.CRITICAL,
                    message=(
                        f"source_training_example_id mismatch: output has "
                        f"'{output.source_training_example_id}', example has "
                        f"'{source_example.training_example_id}'"
                    ),
                )
            )

        return tuple(violations)

    @staticmethod
    def _detect_authority_claims(predicted_text: str) -> Tuple[ConstitutionalViolation, ...]:
        """
        Detect forbidden authority claims in predicted text.

        Checks for:
            - Final answer/analysis claims
            - Correctness/certainty claims
            - Resolution claims
            - Rank upgrade claims
            - Ifādah/Hukm/Reality closure claims

        Args:
            predicted_text: Text to check for forbidden phrases

        Returns:
            Tuple of violations (empty if no forbidden phrases)
        """
        violations = []
        predicted_lower = predicted_text.lower()

        # Check for forbidden authority phrases
        for phrase in FORBIDDEN_AUTHORITY_PHRASES:
            if phrase in predicted_lower:
                # Determine violation type based on phrase
                if "rank" in phrase or "upgrade" in phrase or "promoted" in phrase:
                    violation_type = ConstitutionalViolationType.RANK_UPGRADE_CLAIM
                elif "resolved" in phrase or "resolution" in phrase:
                    violation_type = ConstitutionalViolationType.RESIDUAL_DELETION_CLAIM
                elif "ifadah" in phrase or "complete meaning" in phrase or "semantic closure" in phrase:
                    violation_type = ConstitutionalViolationType.IFADAH_CLOSURE_CLAIM
                elif "hukm" in phrase or "judgment" in phrase:
                    violation_type = ConstitutionalViolationType.HUKM_PRODUCTION_CLAIM
                elif "reality" in phrase or "truth" in phrase:
                    violation_type = ConstitutionalViolationType.REALITY_PRODUCTION_CLAIM
                else:
                    violation_type = ConstitutionalViolationType.AUTHORITY_CLAIM

                violations.append(
                    ConstitutionalViolation(
                        violation_type=violation_type,
                        severity=ConstitutionalViolationSeverity.CRITICAL,
                        message=f"Forbidden authority phrase detected: '{phrase}'",
                        detected_phrase=phrase,
                    )
                )

        return tuple(violations)

    @staticmethod
    def _detect_invented_references(
        predicted_text: str,
        source_example: TrainingExample,
    ) -> Tuple[ConstitutionalViolation, ...]:
        """
        Detect invented references to candidates/residuals/gates/ranks.

        Constitutional Law:
            Model output may ONLY reference IDs present in source TrainingExample.
            Any reference to non-existent ID is constitutional violation.

        Args:
            predicted_text: Text to check for references
            source_example: TrainingExample with valid reference IDs

        Returns:
            Tuple of violations (empty if all references valid)
        """
        violations = []

        # Extract candidate references from predicted text
        candidate_pattern = r'candidate[_\s]([a-z0-9]{6,16})'
        found_candidates = set(re.findall(candidate_pattern, predicted_text.lower()))
        valid_candidates = set(source_example.referenced_candidate_ids)

        for candidate_id in found_candidates:
            if candidate_id not in valid_candidates:
                violations.append(
                    ConstitutionalViolation(
                        violation_type=ConstitutionalViolationType.INVENTED_CANDIDATE_REFERENCE,
                        severity=ConstitutionalViolationSeverity.CRITICAL,
                        message=f"Reference to non-existent candidate: '{candidate_id}'",
                        detected_reference=candidate_id,
                    )
                )

        # Extract residual references
        residual_pattern = r'residual[_\s]([a-z0-9]{6,16})'
        found_residuals = set(re.findall(residual_pattern, predicted_text.lower()))
        valid_residuals = set(source_example.referenced_residual_ids)

        for residual_id in found_residuals:
            if residual_id not in valid_residuals:
                violations.append(
                    ConstitutionalViolation(
                        violation_type=ConstitutionalViolationType.INVENTED_RESIDUAL_REFERENCE,
                        severity=ConstitutionalViolationSeverity.CRITICAL,
                        message=f"Reference to non-existent residual: '{residual_id}'",
                        detected_reference=residual_id,
                    )
                )

        # Extract gate references
        gate_pattern = r'gate[_\s]([a-z0-9]{6,16})'
        found_gates = set(re.findall(gate_pattern, predicted_text.lower()))
        valid_gates = set(source_example.referenced_gate_ids)

        for gate_id in found_gates:
            if gate_id not in valid_gates:
                violations.append(
                    ConstitutionalViolation(
                        violation_type=ConstitutionalViolationType.INVENTED_GATE_REFERENCE,
                        severity=ConstitutionalViolationSeverity.CRITICAL,
                        message=f"Reference to non-existent gate: '{gate_id}'",
                        detected_reference=gate_id,
                    )
                )

        # Check for rank value references
        rank_pattern = r'rank[_\s]([A-Z_]+)'
        found_ranks = set(re.findall(rank_pattern, predicted_text.upper()))
        valid_ranks = set(source_example.referenced_rank_values)

        for rank_value in found_ranks:
            if rank_value not in valid_ranks and rank_value in {
                "CERTIFICATE", "PLAUSIBLE", "CANDIDATE", "RESIDUAL"
            }:
                violations.append(
                    ConstitutionalViolation(
                        violation_type=ConstitutionalViolationType.INVENTED_RANK_REFERENCE,
                        severity=ConstitutionalViolationSeverity.CRITICAL,
                        message=f"Reference to non-existent rank: '{rank_value}'",
                        detected_reference=rank_value,
                    )
                )

        return tuple(violations)
