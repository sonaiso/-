"""
Training Pipeline Skeleton Contract (عقد هيكل خط التدريب)

PR #148: Training pipeline skeleton for planning training runs.

Constitutional Laws:
    1. TrainingPipelineConfig is configuration ONLY, not execution
    2. TrainingPlanCandidate is plan representation ONLY, not execution
    3. ConstitutionalPreflightCheck validates conditions ONLY, not training
    4. TrainingRunPlan is governed plan ONLY, not authority
    5. Pipeline skeleton plans training; it does NOT train
    6. Pipeline skeleton checks conditions; it does NOT execute models
    7. Pipeline skeleton produces plans; it does NOT produce constitutional facts
    8. Pipeline skeleton does NOT load T5 models
    9. Pipeline skeleton does NOT execute inference
    10. Pipeline skeleton does NOT upgrade rank
    11. Pipeline skeleton does NOT resolve residuals
    12. Pipeline skeleton does NOT close ifādah
    13. Pipeline skeleton does NOT produce hukm
    14. Pipeline skeleton does NOT produce reality

Forbidden Operations:
    ❌ train_model(): Training pipeline does NOT train
    ❌ load_t5_model(): Training pipeline does NOT load models
    ❌ execute_inference(): Training pipeline does NOT execute inference
    ❌ compute_metrics(): Training pipeline does NOT compute metrics
    ❌ upgrade_rank(): Training pipeline does NOT upgrade rank
    ❌ resolve_residuals(): Training pipeline does NOT resolve residuals
    ❌ close_ifadah(): Training pipeline does NOT close ifādah
    ❌ produce_hukm(): Training pipeline does NOT produce hukm
    ❌ create_candidate(): Training pipeline does NOT create candidates

Permitted Operations:
    ✅ create_training_config(): Define immutable configuration
    ✅ create_training_plan(): Create plan candidate
    ✅ validate_preflight_conditions(): Check constitutional compliance
    ✅ create_training_run_plan(): Produce governed plan

Constitutional Formula:
    TrainingExample + Config → TrainingPlanCandidate
    TrainingPlanCandidate + Preflight → TrainingRunPlan
    TrainingRunPlan = Plan for training, NOT training execution

Supreme Law:
    Training pipeline skeleton plans training.
    Training pipeline skeleton does NOT train models.
    Training pipeline skeleton does NOT execute inference.
    Training pipeline skeleton does NOT create constitutional facts.

Reference:
    User requirement: PR #148 specification (2026-05-29)
    Builds on: PR #141, PR #142, PR #145, PR #146, PR #147

Created: 2026-05-29
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, FrozenSet
from pathlib import Path

from dal_core.training_example import TrainingExample
from dal_core.algorithm_trace_payload import TraceConsumerOperation


# ============================================================================
# Training Configuration
# ============================================================================

class TrainingMode(Enum):
    """Training mode specification."""
    EXPLANATION_GENERATION = auto()  # Train to explain traces
    REPAIR_SUGGESTION = auto()        # Train to suggest repairs
    MIXED = auto()                   # Both explanation and repair


class ModelArchitecture(Enum):
    """Model architecture specification (contract only, NOT implementation)."""
    T5_SMALL = "t5-small"
    T5_BASE = "t5-base"
    T5_LARGE = "t5-large"

    # Constitutional Note:
    # These are CONTRACT specifications, NOT loaded models.
    # This enum declares WHAT model architecture the plan targets.
    # It does NOT load models, initialize weights, or execute inference.


@dataclass(frozen=True)
class TrainingPipelineConfig:
    """
    Immutable training pipeline configuration (contract ONLY).

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - config_id is unique identifier
        - training_examples_path references JSONL file
        - model_architecture specifies target architecture (NOT loaded model)
        - training_mode specifies what operation to learn
        - max_input_length constrains input tokenization
        - max_target_length constrains target tokenization
        - batch_size specifies training batch size
        - num_epochs specifies training duration
        - learning_rate specifies optimizer parameter
        - output_dir specifies where plan will suggest saving (NOT execution)

    Forbidden Fields:
        ❌ loaded_model: Config does NOT load models
        ❌ trained_weights: Config does NOT train models
        ❌ inference_function: Config does NOT execute inference
        ❌ metric_results: Config does NOT compute metrics
        ❌ upgraded_rank: Config does NOT upgrade rank
        ❌ resolved_residuals: Config does NOT resolve residuals
        ❌ produced_hukm: Config does NOT produce hukm

    Fields:
        config_id: Unique identifier for this configuration
        training_examples_path: Path to JSONL training examples file
        model_architecture: Target model architecture (contract only)
        training_mode: What type of training to plan
        max_input_length: Maximum input sequence length
        max_target_length: Maximum target sequence length
        batch_size: Training batch size
        num_epochs: Number of training epochs
        learning_rate: Learning rate for optimizer
        output_dir: Directory where plan suggests saving outputs
        allowed_operations: Permitted TraceConsumerOperations for this config
    """
    config_id: str
    training_examples_path: str
    model_architecture: ModelArchitecture
    training_mode: TrainingMode
    max_input_length: int
    max_target_length: int
    batch_size: int
    num_epochs: int
    learning_rate: float
    output_dir: str
    allowed_operations: FrozenSet[TraceConsumerOperation]

    def __post_init__(self):
        """
        Validate TrainingPipelineConfig constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.config_id:
            raise ValueError("TrainingPipelineConfig requires config_id")

        if not self.training_examples_path:
            raise ValueError("TrainingPipelineConfig requires training_examples_path")

        if self.max_input_length <= 0:
            raise ValueError("max_input_length must be positive")

        if self.max_target_length <= 0:
            raise ValueError("max_target_length must be positive")

        if self.batch_size <= 0:
            raise ValueError("batch_size must be positive")

        if self.num_epochs <= 0:
            raise ValueError("num_epochs must be positive")

        if self.learning_rate <= 0:
            raise ValueError("learning_rate must be positive")

        if not self.output_dir:
            raise ValueError("TrainingPipelineConfig requires output_dir")

        if not self.allowed_operations:
            raise ValueError("TrainingPipelineConfig requires allowed_operations")


# ============================================================================
# Training Plan Candidate
# ============================================================================

@dataclass(frozen=True)
class TrainingPlanCandidate:
    """
    Candidate training plan (representation ONLY, not execution).

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - plan_id is unique identifier
        - config references TrainingPipelineConfig
        - total_examples counts examples in training set
        - estimated_steps estimates training steps (NOT execution)
        - estimated_duration_minutes estimates duration (NOT execution)
        - requires_preflight_check indicates validation needed

    Forbidden Fields:
        ❌ training_execution: Plan does NOT execute training
        ❌ loaded_model: Plan does NOT load models
        ❌ inference_results: Plan does NOT execute inference
        ❌ metric_scores: Plan does NOT compute metrics
        ❌ upgraded_rank: Plan does NOT upgrade rank
        ❌ constitutional_authority: Plan does NOT create authority

    Fields:
        plan_id: Unique identifier for this plan
        config_id: References TrainingPipelineConfig
        config: The training configuration
        total_examples: Count of training examples
        estimated_steps: Estimated training steps (NOT execution)
        estimated_duration_minutes: Estimated duration (NOT execution)
        requires_preflight_check: Whether preflight validation needed
    """
    plan_id: str
    config_id: str
    config: TrainingPipelineConfig
    total_examples: int
    estimated_steps: int
    estimated_duration_minutes: int
    requires_preflight_check: bool

    def __post_init__(self):
        """
        Validate TrainingPlanCandidate constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.plan_id:
            raise ValueError("TrainingPlanCandidate requires plan_id")

        if not self.config_id:
            raise ValueError("TrainingPlanCandidate requires config_id")

        if self.config.config_id != self.config_id:
            raise ValueError(
                f"config_id mismatch: plan has '{self.config_id}', "
                f"config has '{self.config.config_id}'"
            )

        if self.total_examples < 0:
            raise ValueError("total_examples must be non-negative")

        if self.estimated_steps < 0:
            raise ValueError("estimated_steps must be non-negative")

        if self.estimated_duration_minutes < 0:
            raise ValueError("estimated_duration_minutes must be non-negative")


# ============================================================================
# Preflight Check Result
# ============================================================================

class PreflightCheckType(Enum):
    """Types of preflight checks."""
    CONFIG_VALIDATION = auto()           # Config fields valid
    TRAINING_EXAMPLES_EXIST = auto()     # Training file exists
    TRAINING_EXAMPLES_VALID = auto()     # Examples are well-formed
    OUTPUT_DIR_WRITABLE = auto()         # Output directory accessible
    OPERATION_PERMITTED = auto()         # Operations constitutionally allowed
    NO_FORBIDDEN_PHRASES = auto()        # No authority claims in examples
    SOURCE_BINDINGS_PRESERVED = auto()   # All examples have source bindings


class PreflightCheckStatus(Enum):
    """Preflight check status."""
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"


@dataclass(frozen=True)
class PreflightCheckResult:
    """
    Result of a single preflight check.

    Fields:
        check_type: Type of preflight check
        status: PASSED, FAILED, or WARNING
        message: Description of check result
        details: Additional details (if any)
    """
    check_type: PreflightCheckType
    status: PreflightCheckStatus
    message: str
    details: str = ""


@dataclass(frozen=True)
class ConstitutionalPreflightReport:
    """
    Report of constitutional preflight checks.

    Constitutional Requirements:
        - report_id is unique identifier
        - plan_id references TrainingPlanCandidate
        - checks is immutable tuple of all check results
        - passed is True only if ALL checks PASSED
        - failed_checks_count counts FAILED status only
        - warning_checks_count counts WARNING status only

    Fields:
        report_id: Unique identifier for this report
        plan_id: ID of TrainingPlanCandidate checked
        checks: Tuple of all preflight check results
        passed: True if ALL checks PASSED
        failed_checks_count: Count of FAILED checks
        warning_checks_count: Count of WARNING checks
    """
    report_id: str
    plan_id: str
    checks: Tuple[PreflightCheckResult, ...]
    passed: bool
    failed_checks_count: int
    warning_checks_count: int


# ============================================================================
# Training Run Plan
# ============================================================================

@dataclass(frozen=True)
class TrainingRunPlan:
    """
    Governed training run plan (plan ONLY, not authority).

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - run_plan_id is unique identifier
        - plan_candidate references TrainingPlanCandidate
        - preflight_report references ConstitutionalPreflightReport
        - ready_for_execution indicates if plan passed preflight
        - constitutional_constraints preserves forbidden operations

    Forbidden Fields:
        ❌ training_execution: RunPlan does NOT execute training
        ❌ model_weights: RunPlan does NOT produce weights
        ❌ inference_capability: RunPlan does NOT enable inference
        ❌ metric_results: RunPlan does NOT compute metrics
        ❌ upgraded_rank: RunPlan does NOT upgrade rank
        ❌ constitutional_authority: RunPlan does NOT create authority

    Forbidden Methods:
        ❌ execute_training(): RunPlan does NOT train
        ❌ load_model(): RunPlan does NOT load models
        ❌ run_inference(): RunPlan does NOT execute inference

    Fields:
        run_plan_id: Unique identifier for this run plan
        plan_id: References TrainingPlanCandidate
        plan_candidate: The training plan candidate
        preflight_report: Constitutional preflight check report
        ready_for_execution: Whether plan passed preflight (NOT execution itself)
        constitutional_constraints: Immutable set of forbidden operations
    """
    run_plan_id: str
    plan_id: str
    plan_candidate: TrainingPlanCandidate
    preflight_report: ConstitutionalPreflightReport
    ready_for_execution: bool
    constitutional_constraints: FrozenSet[str]

    def __post_init__(self):
        """
        Validate TrainingRunPlan constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.run_plan_id:
            raise ValueError("TrainingRunPlan requires run_plan_id")

        if not self.plan_id:
            raise ValueError("TrainingRunPlan requires plan_id")

        if self.plan_candidate.plan_id != self.plan_id:
            raise ValueError(
                f"plan_id mismatch: run_plan has '{self.plan_id}', "
                f"candidate has '{self.plan_candidate.plan_id}'"
            )

        if self.preflight_report.plan_id != self.plan_id:
            raise ValueError(
                f"plan_id mismatch: run_plan has '{self.plan_id}', "
                f"preflight has '{self.preflight_report.plan_id}'"
            )

        # Validate ready_for_execution matches preflight status
        if self.ready_for_execution and not self.preflight_report.passed:
            raise ValueError(
                "Constitutional violation: ready_for_execution=True but "
                "preflight_report.passed=False"
            )

        # Validate constitutional constraints present
        if not self.constitutional_constraints:
            raise ValueError(
                "Constitutional violation: TrainingRunPlan must declare "
                "constitutional_constraints"
            )


# ============================================================================
# Constitutional Constraints
# ============================================================================

CONSTITUTIONAL_CONSTRAINTS: FrozenSet[str] = frozenset([
    "NO_TRAINING_EXECUTION",
    "NO_MODEL_LOADING",
    "NO_INFERENCE_EXECUTION",
    "NO_METRIC_COMPUTATION",
    "NO_RANK_UPGRADE",
    "NO_RESIDUAL_RESOLUTION",
    "NO_IFADAH_CLOSURE",
    "NO_HUKM_PRODUCTION",
    "NO_REALITY_PRODUCTION",
    "NO_CANDIDATE_CREATION",
    "NO_HUGGING_FACE_IMPORTS",
    "NO_T5_MODEL_INSTANTIATION",
    "EVALUATION_BOUNDARY_ONLY",
    "PLAN_ONLY_NOT_AUTHORITY",
])


# ============================================================================
# Training Pipeline Skeleton
# ============================================================================

class TrainingPipelineSkeleton:
    """
    Training pipeline skeleton for planning training runs (NOT executing training).

    Constitutional Laws:
        1. Skeleton plans training; it does NOT train
        2. Skeleton checks conditions; it does NOT execute models
        3. Skeleton produces plans; it does NOT produce authority
        4. Skeleton validates config; it does NOT load models
        5. Skeleton estimates resources; it does NOT compute metrics

    Forbidden Methods:
        ❌ train_model()
        ❌ load_t5_model()
        ❌ execute_inference()
        ❌ compute_metrics()
        ❌ upgrade_rank()

    Permitted Methods:
        ✅ create_training_plan()
        ✅ run_preflight_checks()
        ✅ create_training_run_plan()
    """

    @staticmethod
    def create_training_plan(
        config: TrainingPipelineConfig,
        examples: Tuple[TrainingExample, ...],
    ) -> TrainingPlanCandidate:
        """
        Create training plan candidate from configuration and examples.

        Constitutional Requirements:
            1. Plan is representation ONLY, not execution
            2. Plan estimates resources, does NOT allocate them
            3. Plan counts examples, does NOT train on them

        Args:
            config: TrainingPipelineConfig specifying training parameters
            examples: Tuple of TrainingExample instances

        Returns:
            TrainingPlanCandidate with resource estimates
        """
        from uuid import uuid4

        # Validate examples are not empty
        if not examples:
            raise ValueError("Cannot create training plan with zero examples")

        # Count total examples
        total_examples = len(examples)

        # Estimate training steps
        steps_per_epoch = (total_examples + config.batch_size - 1) // config.batch_size
        estimated_steps = steps_per_epoch * config.num_epochs

        # Estimate duration (rough estimate: 1 second per step)
        estimated_duration_minutes = (estimated_steps + 59) // 60

        # Generate plan ID
        plan_id = f"training_plan_{uuid4().hex[:16]}"

        # Create plan candidate
        return TrainingPlanCandidate(
            plan_id=plan_id,
            config_id=config.config_id,
            config=config,
            total_examples=total_examples,
            estimated_steps=estimated_steps,
            estimated_duration_minutes=estimated_duration_minutes,
            requires_preflight_check=True,
        )

    @staticmethod
    def run_preflight_checks(
        plan: TrainingPlanCandidate,
        examples: Tuple[TrainingExample, ...],
    ) -> ConstitutionalPreflightReport:
        """
        Run constitutional preflight checks on training plan.

        Constitutional Requirements:
            1. Checks validate conditions ONLY, do NOT execute training
            2. Checks detect violations ONLY, do NOT resolve them
            3. Checks produce report ONLY, do NOT create authority

        Args:
            plan: TrainingPlanCandidate to validate
            examples: Tuple of TrainingExample instances

        Returns:
            ConstitutionalPreflightReport with all check results
        """
        from uuid import uuid4

        checks = []

        # Check 1: Config validation
        try:
            # Config already validated in __post_init__
            checks.append(
                PreflightCheckResult(
                    check_type=PreflightCheckType.CONFIG_VALIDATION,
                    status=PreflightCheckStatus.PASSED,
                    message="TrainingPipelineConfig valid",
                )
            )
        except ValueError as e:
            checks.append(
                PreflightCheckResult(
                    check_type=PreflightCheckType.CONFIG_VALIDATION,
                    status=PreflightCheckStatus.FAILED,
                    message=f"Config validation failed: {str(e)}",
                )
            )

        # Check 2: Training examples exist
        training_path = Path(plan.config.training_examples_path)
        if training_path.exists():
            checks.append(
                PreflightCheckResult(
                    check_type=PreflightCheckType.TRAINING_EXAMPLES_EXIST,
                    status=PreflightCheckStatus.PASSED,
                    message=f"Training examples file exists: {training_path}",
                )
            )
        else:
            checks.append(
                PreflightCheckResult(
                    check_type=PreflightCheckType.TRAINING_EXAMPLES_EXIST,
                    status=PreflightCheckStatus.FAILED,
                    message=f"Training examples file not found: {training_path}",
                )
            )

        # Check 3: Training examples valid
        if examples:
            checks.append(
                PreflightCheckResult(
                    check_type=PreflightCheckType.TRAINING_EXAMPLES_VALID,
                    status=PreflightCheckStatus.PASSED,
                    message=f"Training examples valid (count: {len(examples)})",
                )
            )
        else:
            checks.append(
                PreflightCheckResult(
                    check_type=PreflightCheckType.TRAINING_EXAMPLES_VALID,
                    status=PreflightCheckStatus.FAILED,
                    message="No training examples provided",
                )
            )

        # Check 4: Output directory writable
        output_dir = Path(plan.config.output_dir)
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            checks.append(
                PreflightCheckResult(
                    check_type=PreflightCheckType.OUTPUT_DIR_WRITABLE,
                    status=PreflightCheckStatus.PASSED,
                    message=f"Output directory accessible: {output_dir}",
                )
            )
        except (OSError, PermissionError) as e:
            checks.append(
                PreflightCheckResult(
                    check_type=PreflightCheckType.OUTPUT_DIR_WRITABLE,
                    status=PreflightCheckStatus.FAILED,
                    message=f"Output directory not writable: {str(e)}",
                )
            )

        # Check 5: Operations permitted
        if examples:
            example_operations = set(ex.operation for ex in examples)
            disallowed_operations = example_operations - plan.config.allowed_operations

            if not disallowed_operations:
                checks.append(
                    PreflightCheckResult(
                        check_type=PreflightCheckType.OPERATION_PERMITTED,
                        status=PreflightCheckStatus.PASSED,
                        message="All example operations permitted by config",
                    )
                )
            else:
                checks.append(
                    PreflightCheckResult(
                        check_type=PreflightCheckType.OPERATION_PERMITTED,
                        status=PreflightCheckStatus.FAILED,
                        message=f"Disallowed operations: {disallowed_operations}",
                        details=str(disallowed_operations),
                    )
                )

        # Check 6: No forbidden phrases (sample check on first 10 examples)
        sample_examples = examples[:10] if len(examples) > 10 else examples
        forbidden_found = []
        from dal_core.constitutional_evaluator import FORBIDDEN_AUTHORITY_PHRASES

        for example in sample_examples:
            input_lower = example.input_text.lower()
            target_lower = example.target_text.lower()

            for phrase in FORBIDDEN_AUTHORITY_PHRASES:
                if phrase in input_lower or phrase in target_lower:
                    forbidden_found.append((example.training_example_id, phrase))

        if not forbidden_found:
            checks.append(
                PreflightCheckResult(
                    check_type=PreflightCheckType.NO_FORBIDDEN_PHRASES,
                    status=PreflightCheckStatus.PASSED,
                    message="No forbidden authority phrases in sample examples",
                )
            )
        else:
            checks.append(
                PreflightCheckResult(
                    check_type=PreflightCheckType.NO_FORBIDDEN_PHRASES,
                    status=PreflightCheckStatus.WARNING,
                    message=f"Found {len(forbidden_found)} forbidden phrases in sample",
                    details=str(forbidden_found[:3]),  # Show first 3
                )
            )

        # Check 7: Source bindings preserved
        if examples:
            missing_bindings = [
                ex.training_example_id
                for ex in examples
                if not ex.source_trace_id or not ex.source_dataset_row_id
            ]

            if not missing_bindings:
                checks.append(
                    PreflightCheckResult(
                        check_type=PreflightCheckType.SOURCE_BINDINGS_PRESERVED,
                        status=PreflightCheckStatus.PASSED,
                        message="All examples preserve source bindings",
                    )
                )
            else:
                checks.append(
                    PreflightCheckResult(
                        check_type=PreflightCheckType.SOURCE_BINDINGS_PRESERVED,
                        status=PreflightCheckStatus.FAILED,
                        message=f"{len(missing_bindings)} examples missing source bindings",
                        details=str(missing_bindings[:3]),  # Show first 3
                    )
                )

        # Determine overall status
        failed_count = sum(1 for c in checks if c.status == PreflightCheckStatus.FAILED)
        warning_count = sum(1 for c in checks if c.status == PreflightCheckStatus.WARNING)
        passed = (failed_count == 0)

        # Generate report ID
        report_id = f"preflight_report_{uuid4().hex[:16]}"

        return ConstitutionalPreflightReport(
            report_id=report_id,
            plan_id=plan.plan_id,
            checks=tuple(checks),
            passed=passed,
            failed_checks_count=failed_count,
            warning_checks_count=warning_count,
        )

    @staticmethod
    def create_training_run_plan(
        plan: TrainingPlanCandidate,
        preflight: ConstitutionalPreflightReport,
    ) -> TrainingRunPlan:
        """
        Create training run plan from validated candidate and preflight report.

        Constitutional Requirements:
            1. RunPlan is plan ONLY, not execution
            2. RunPlan preserves constitutional constraints
            3. RunPlan ready_for_execution based on preflight status

        Args:
            plan: TrainingPlanCandidate (validated)
            preflight: ConstitutionalPreflightReport (completed)

        Returns:
            TrainingRunPlan with constitutional constraints

        Raises:
            ValueError: If plan_id mismatch between plan and preflight
        """
        from uuid import uuid4

        # Validate plan_id match
        if plan.plan_id != preflight.plan_id:
            raise ValueError(
                f"plan_id mismatch: plan has '{plan.plan_id}', "
                f"preflight has '{preflight.plan_id}'"
            )

        # Generate run plan ID
        run_plan_id = f"run_plan_{uuid4().hex[:16]}"

        # Determine ready status
        ready_for_execution = preflight.passed

        # Create training run plan
        return TrainingRunPlan(
            run_plan_id=run_plan_id,
            plan_id=plan.plan_id,
            plan_candidate=plan,
            preflight_report=preflight,
            ready_for_execution=ready_for_execution,
            constitutional_constraints=CONSTITUTIONAL_CONSTRAINTS,
        )
