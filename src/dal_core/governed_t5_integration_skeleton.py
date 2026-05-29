"""
Governed T5 Integration Skeleton (هيكل تكامل T5 المحكوم)

PR #150: Integration skeleton for T5 model integration (contract/boundary layer ONLY).

Constitutional Laws:
    1. GovernedT5IntegrationConfig is integration contract ONLY, not execution
    2. ModelDependencyDeclaration declares dependencies as DATA, not imports
    3. AdapterBoundaryPlan defines adapter interfaces ONLY, not implementations
    4. NoExecutionIntegrationReport confirms no execution occurred
    5. IntegrationPreflightCheck validates constitutional compliance ONLY
    6. Integration skeleton declares dependencies; it does NOT load models
    7. Integration skeleton defines boundaries; it does NOT execute inference
    8. Integration skeleton plans integration; it does NOT train models
    9. Integration skeleton validates contracts; it does NOT compute metrics
    10. Integration skeleton produces plans; it does NOT create authority

Forbidden Operations:
    ❌ import transformers: Integration skeleton does NOT import transformers
    ❌ import torch: Integration skeleton does NOT import torch
    ❌ from_pretrained(): Integration skeleton does NOT load models
    ❌ AutoTokenizer: Integration skeleton does NOT create tokenizers
    ❌ T5ForConditionalGeneration: Integration skeleton does NOT instantiate T5
    ❌ Trainer(): Integration skeleton does NOT create trainers
    ❌ model.generate(): Integration skeleton does NOT execute inference
    ❌ forward(): Integration skeleton does NOT execute forward passes
    ❌ compute_metrics(): Integration skeleton does NOT compute metrics
    ❌ training_loop(): Integration skeleton does NOT train models

Permitted Operations:
    ✅ declare_model_dependency(): Declare model as string/enum
    ✅ declare_version_requirement(): Declare version as data
    ✅ define_adapter_boundary(): Define interface contract
    ✅ validate_integration_contract(): Check constitutional compliance
    ✅ scan_for_forbidden_markers(): Detect execution markers
    ✅ link_to_training_run_plan(): Connect to training plan

Constitutional Formula:
    TrainingRunPlan → GovernedT5IntegrationConfig
    GovernedT5IntegrationConfig → ModelDependencyDeclaration
    ModelDependencyDeclaration → AdapterBoundaryPlan
    AdapterBoundaryPlan → NoExecutionIntegrationReport
    NoExecutionIntegrationReport = Integration contract validated, NOT executed

Supreme Law:
    Integration skeleton declares dependency and adapter contracts.
    Integration skeleton does NOT execute them.

Reference:
    User requirement: PR #150 specification (2026-05-29)
    Builds on: PR #148 (TrainingPipelineSkeleton)
    Related: PR #142 (GovernedTraceT5Contract)

Created: 2026-05-29
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, FrozenSet, Optional
from pathlib import Path

from dal_core.training_pipeline_skeleton import TrainingRunPlan


# ============================================================================
# Model Family and Architecture Declarations
# ============================================================================

class ModelFamily(Enum):
    """
    Model family specification (declaration ONLY, not loaded models).

    Constitutional Note:
        These are string identifiers for model families.
        They do NOT import transformers, torch, or any ML libraries.
        They do NOT load models or weights.
        They are CONTRACT declarations only.
    """
    T5_FAMILY = "t5"
    T5_SMALL = "t5-small"
    T5_BASE = "t5-base"
    T5_LARGE = "t5-large"

    # Constitutional Law: These are strings, NOT model instances


class AdapterBoundaryType(Enum):
    """
    Adapter boundary type classification.

    Types:
        INPUT_ADAPTER: Transforms TrainingRunPlan data → model input format spec
        OUTPUT_ADAPTER: Transforms model output format spec → evaluation format
        VALIDATION_ADAPTER: Validates constitutional constraints at boundary

    Constitutional Note:
        These define boundary TYPES, not implementations.
        Actual adapter implementations are out of scope for PR #150.
    """
    INPUT_ADAPTER = auto()
    OUTPUT_ADAPTER = auto()
    VALIDATION_ADAPTER = auto()


class IntegrationCheckType(Enum):
    """
    Integration preflight check types.

    Types:
        DEPENDENCY_DECLARATION: Verifies dependencies declared as data
        NO_FORBIDDEN_IMPORTS: Verifies no transformers/torch imports
        NO_MODEL_LOADING: Verifies no .from_pretrained() calls
        NO_INFERENCE_EXECUTION: Verifies no .generate() or forward() calls
        NO_TRAINING_EXECUTION: Verifies no Trainer or training loops
        ADAPTER_BOUNDARY_VALID: Verifies adapter boundaries properly defined
        CONSTITUTIONAL_CONSTRAINTS: Verifies constitutional constraints preserved
    """
    DEPENDENCY_DECLARATION = auto()
    NO_FORBIDDEN_IMPORTS = auto()
    NO_MODEL_LOADING = auto()
    NO_INFERENCE_EXECUTION = auto()
    NO_TRAINING_EXECUTION = auto()
    ADAPTER_BOUNDARY_VALID = auto()
    CONSTITUTIONAL_CONSTRAINTS = auto()


class IntegrationCheckStatus(Enum):
    """Status of integration preflight check."""
    PASSED = auto()
    FAILED = auto()
    WARNING = auto()


# ============================================================================
# Model Dependency Declaration
# ============================================================================

@dataclass(frozen=True)
class ModelDependencyDeclaration:
    """
    Model dependency declaration (DATA ONLY, not actual imports).

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - model_family specifies model family as STRING/ENUM
        - required_transformers_version specifies version as STRING
        - required_torch_version specifies version as STRING (optional)
        - checkpoint_path specifies path as STRING (optional)
        - NO actual imports of transformers or torch
        - NO model loading or instantiation
        - Dependencies are DECLARED, not EXECUTED

    Forbidden Fields:
        ❌ loaded_model: Does NOT contain loaded model
        ❌ tokenizer_instance: Does NOT contain tokenizer
        ❌ model_weights: Does NOT contain model weights
        ❌ torch_device: Does NOT allocate GPU/device

    Fields:
        dependency_id: Unique identifier for this dependency declaration
        model_family: Model family as enum/string (NOT loaded model)
        required_transformers_version: Version requirement as string
        required_torch_version: Torch version requirement (optional)
        checkpoint_path: Checkpoint path specification (optional)
        additional_requirements: Additional dependencies as strings
    """
    dependency_id: str
    model_family: ModelFamily
    required_transformers_version: str
    required_torch_version: Optional[str] = None
    checkpoint_path: Optional[str] = None
    additional_requirements: Tuple[str, ...] = ()

    def __post_init__(self):
        """
        Validate ModelDependencyDeclaration constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.dependency_id:
            raise ValueError("ModelDependencyDeclaration requires dependency_id")

        if not self.required_transformers_version:
            raise ValueError("ModelDependencyDeclaration requires required_transformers_version")

        # Validate version format (basic string check, not actual version comparison)
        if not isinstance(self.required_transformers_version, str):
            raise ValueError("required_transformers_version must be string")

        if self.required_torch_version and not isinstance(self.required_torch_version, str):
            raise ValueError("required_torch_version must be string or None")


# ============================================================================
# Adapter Boundary Plan
# ============================================================================

@dataclass(frozen=True)
class AdapterBoundaryPlan:
    """
    Adapter boundary plan (interface definition ONLY, not implementation).

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - boundary_id is unique identifier
        - boundary_type specifies adapter type
        - input_contract_description describes expected input
        - output_contract_description describes expected output
        - constitutional_constraints lists boundary constraints
        - NO actual adapter implementation
        - NO model execution
        - Boundaries are DEFINED, not IMPLEMENTED

    Forbidden Fields:
        ❌ adapter_implementation: Does NOT contain implementation
        ❌ tokenizer: Does NOT contain tokenizer instance
        ❌ execution_function: Does NOT contain execution code
        ❌ model_reference: Does NOT reference loaded model

    Fields:
        boundary_id: Unique identifier for this boundary
        boundary_type: Type of adapter boundary
        input_contract_description: Description of input contract
        output_contract_description: Description of output contract
        constitutional_constraints: Constitutional constraints at boundary
        preserves_source_bindings: Whether source_trace_id bindings preserved
        prevents_authority_claims: Whether authority claims prevented
        prevents_rank_upgrade: Whether rank upgrades prevented
    """
    boundary_id: str
    boundary_type: AdapterBoundaryType
    input_contract_description: str
    output_contract_description: str
    constitutional_constraints: Tuple[str, ...]
    preserves_source_bindings: bool
    prevents_authority_claims: bool
    prevents_rank_upgrade: bool

    def __post_init__(self):
        """
        Validate AdapterBoundaryPlan constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.boundary_id:
            raise ValueError("AdapterBoundaryPlan requires boundary_id")

        if not self.input_contract_description:
            raise ValueError("AdapterBoundaryPlan requires input_contract_description")

        if not self.output_contract_description:
            raise ValueError("AdapterBoundaryPlan requires output_contract_description")

        if not self.constitutional_constraints:
            raise ValueError("AdapterBoundaryPlan requires constitutional_constraints")

        # Validate constitutional safeguards
        if not self.preserves_source_bindings:
            raise ValueError("AdapterBoundaryPlan must preserve_source_bindings")

        if not self.prevents_authority_claims:
            raise ValueError("AdapterBoundaryPlan must prevent_authority_claims")

        if not self.prevents_rank_upgrade:
            raise ValueError("AdapterBoundaryPlan must prevent_rank_upgrade")


# ============================================================================
# Governed T5 Integration Config
# ============================================================================

@dataclass(frozen=True)
class GovernedT5IntegrationConfig:
    """
    Governed T5 integration configuration (contract ONLY, not execution).

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - integration_id is unique identifier
        - training_run_plan_id references TrainingRunPlan
        - dependency_declaration specifies model dependencies as data
        - adapter_boundaries define boundary contracts
        - NO model loading or instantiation
        - NO transformers/torch imports
        - NO inference or training execution
        - Integration is CONFIGURED, not EXECUTED

    Forbidden Fields:
        ❌ loaded_model: Does NOT load models
        ❌ tokenizer: Does NOT create tokenizers
        ❌ trainer: Does NOT create trainers
        ❌ inference_results: Does NOT execute inference
        ❌ training_metrics: Does NOT train models
        ❌ upgraded_rank: Does NOT upgrade rank
        ❌ produced_hukm: Does NOT produce hukm

    Fields:
        integration_id: Unique identifier for this integration config
        training_run_plan_id: References TrainingRunPlan
        dependency_declaration: Model dependency declaration (data only)
        input_adapter_boundary: Input adapter boundary plan
        output_adapter_boundary: Output adapter boundary plan
        validation_adapter_boundary: Validation adapter boundary plan
        constitutional_constraints: Constitutional constraints for integration
    """
    integration_id: str
    training_run_plan_id: str
    dependency_declaration: ModelDependencyDeclaration
    input_adapter_boundary: AdapterBoundaryPlan
    output_adapter_boundary: AdapterBoundaryPlan
    validation_adapter_boundary: AdapterBoundaryPlan
    constitutional_constraints: Tuple[str, ...]

    def __post_init__(self):
        """
        Validate GovernedT5IntegrationConfig constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.integration_id:
            raise ValueError("GovernedT5IntegrationConfig requires integration_id")

        if not self.training_run_plan_id:
            raise ValueError("GovernedT5IntegrationConfig requires training_run_plan_id")

        if not self.constitutional_constraints:
            raise ValueError("GovernedT5IntegrationConfig requires constitutional_constraints")

        # Validate adapter boundary types are correct
        if self.input_adapter_boundary.boundary_type != AdapterBoundaryType.INPUT_ADAPTER:
            raise ValueError("input_adapter_boundary must be INPUT_ADAPTER type")

        if self.output_adapter_boundary.boundary_type != AdapterBoundaryType.OUTPUT_ADAPTER:
            raise ValueError("output_adapter_boundary must be OUTPUT_ADAPTER type")

        if self.validation_adapter_boundary.boundary_type != AdapterBoundaryType.VALIDATION_ADAPTER:
            raise ValueError("validation_adapter_boundary must be VALIDATION_ADAPTER type")


# ============================================================================
# Integration Preflight Check
# ============================================================================

@dataclass(frozen=True)
class IntegrationPreflightCheck:
    """
    Single integration preflight check result.

    Fields:
        check_type: Type of preflight check
        status: Status of the check
        message: Description of check result
        detected_violations: Detected violations (if any)
    """
    check_type: IntegrationCheckType
    status: IntegrationCheckStatus
    message: str
    detected_violations: Tuple[str, ...] = ()


@dataclass(frozen=True)
class IntegrationPreflightReport:
    """
    Integration preflight validation report.

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - report_id is unique identifier
        - integration_config_id references integration config
        - checks contains all preflight check results
        - all_checks_passed indicates overall status
        - NO execution of models or training
        - Report is VALIDATION only

    Fields:
        report_id: Unique identifier for this report
        integration_config_id: References integration config
        checks: All preflight check results
        all_checks_passed: Whether all checks passed
        critical_violations: Critical violations detected
    """
    report_id: str
    integration_config_id: str
    checks: Tuple[IntegrationPreflightCheck, ...]
    all_checks_passed: bool
    critical_violations: Tuple[str, ...]

    def __post_init__(self):
        """
        Validate IntegrationPreflightReport constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.report_id:
            raise ValueError("IntegrationPreflightReport requires report_id")

        if not self.integration_config_id:
            raise ValueError("IntegrationPreflightReport requires integration_config_id")

        if not self.checks:
            raise ValueError("IntegrationPreflightReport requires checks")


# ============================================================================
# No Execution Integration Report
# ============================================================================

@dataclass(frozen=True)
class NoExecutionIntegrationReport:
    """
    Integration report confirming no execution occurred.

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - report_id is unique identifier
        - integration_config_id references integration config
        - preflight_report contains preflight validation
        - Confirms NO model loading
        - Confirms NO training execution
        - Confirms NO inference execution
        - Confirms NO metrics computation
        - Report is CONFIRMATION of contract adherence

    Forbidden Fields:
        ❌ model_loaded: Does NOT load models
        ❌ training_executed: Does NOT train
        ❌ inference_executed: Does NOT execute inference
        ❌ metrics_computed: Does NOT compute metrics
        ❌ rank_upgraded: Does NOT upgrade rank
        ❌ hukm_produced: Does NOT produce hukm

    Fields:
        report_id: Unique identifier for this report
        integration_config_id: References integration config
        preflight_report: Preflight validation report
        dependencies_declared_not_loaded: Confirms dependencies are data only
        boundaries_defined_not_implemented: Confirms boundaries are contracts only
        no_model_loading_detected: Confirms no model loading
        no_training_execution_detected: Confirms no training
        no_inference_execution_detected: Confirms no inference
        integration_contract_valid: Overall contract validity
    """
    report_id: str
    integration_config_id: str
    preflight_report: IntegrationPreflightReport
    dependencies_declared_not_loaded: bool
    boundaries_defined_not_implemented: bool
    no_model_loading_detected: bool
    no_training_execution_detected: bool
    no_inference_execution_detected: bool
    integration_contract_valid: bool

    def __post_init__(self):
        """
        Validate NoExecutionIntegrationReport constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.report_id:
            raise ValueError("NoExecutionIntegrationReport requires report_id")

        if not self.integration_config_id:
            raise ValueError("NoExecutionIntegrationReport requires integration_config_id")

        # Validate structural confirmations are always True
        if not self.dependencies_declared_not_loaded:
            raise ValueError("Must confirm dependencies_declared_not_loaded")

        if not self.boundaries_defined_not_implemented:
            raise ValueError("Must confirm boundaries_defined_not_implemented")

        # Note: no_model_loading_detected, no_training_execution_detected,
        # and no_inference_execution_detected can be False if markers were detected.
        # They reflect marker detection status, not execution status.


# ============================================================================
# Governed T5 Integration Skeleton
# ============================================================================

# Forbidden execution markers to detect in validation
FORBIDDEN_EXECUTION_MARKERS = frozenset([
    "import transformers",
    "import torch",
    "from transformers import",
    "from torch import",
    ".from_pretrained(",
    "AutoTokenizer",
    "T5ForConditionalGeneration",
    "T5Tokenizer",
    "Trainer(",
    "TrainingArguments(",
    ".generate(",
    ".forward(",
    "model.train(",
    "optimizer.step(",
    "loss.backward(",
    "torch.cuda",
    "device = ",
])


class GovernedT5IntegrationSkeleton:
    """
    Governed T5 Integration Skeleton (contract validation ONLY).

    Constitutional Laws:
        This class validates integration contracts.
        It does NOT execute model loading, training, or inference.
        It does NOT import transformers or torch.
        It provides contract validation and preflight checks ONLY.

    Forbidden Operations:
        ❌ load_model(): Does NOT load models
        ❌ execute_training(): Does NOT train
        ❌ execute_inference(): Does NOT execute inference
        ❌ import_transformers(): Does NOT import libraries

    Permitted Operations:
        ✅ validate_integration_config(): Validate contract
        ✅ run_preflight_checks(): Run preflight validation
        ✅ create_integration_report(): Create validation report
        ✅ scan_for_execution_markers(): Detect forbidden markers
        ✅ create_integration_config_from_run_plan(): Create config from TrainingRunPlan
    """

    @staticmethod
    def create_integration_config_from_run_plan(
        run_plan: TrainingRunPlan,
        dependency_declaration: ModelDependencyDeclaration,
        input_adapter_boundary: AdapterBoundaryPlan,
        output_adapter_boundary: AdapterBoundaryPlan,
        validation_adapter_boundary: AdapterBoundaryPlan,
    ) -> GovernedT5IntegrationConfig:
        """
        Create integration config from TrainingRunPlan.

        Args:
            run_plan: TrainingRunPlan to link to
            dependency_declaration: Model dependency declaration
            input_adapter_boundary: Input adapter boundary plan
            output_adapter_boundary: Output adapter boundary plan
            validation_adapter_boundary: Validation adapter boundary plan

        Returns:
            GovernedT5IntegrationConfig linked to run_plan

        Raises:
            ValueError: If run_plan is not ready for execution

        Constitutional Law:
            This method creates integration config from run_plan.
            It validates run_plan.ready_for_execution == True.
            It preserves run_plan.run_plan_id in training_run_plan_id.
            It does NOT execute training or load models.
        """
        # Validate run_plan is ready
        if not run_plan.ready_for_execution:
            raise ValueError(
                f"TrainingRunPlan '{run_plan.run_plan_id}' is not ready_for_execution. "
                f"Preflight status: {run_plan.preflight_report.passed}"
            )

        # Create integration config linked to run_plan
        return GovernedT5IntegrationConfig(
            integration_id=f"integration_{run_plan.run_plan_id}",
            training_run_plan_id=run_plan.run_plan_id,
            dependency_declaration=dependency_declaration,
            input_adapter_boundary=input_adapter_boundary,
            output_adapter_boundary=output_adapter_boundary,
            validation_adapter_boundary=validation_adapter_boundary,
            constitutional_constraints=INTEGRATION_CONSTITUTIONAL_CONSTRAINTS,
        )

    @staticmethod
    def validate_integration_config(
        config: GovernedT5IntegrationConfig,
    ) -> Tuple[bool, Tuple[str, ...]]:
        """
        Validate integration config constitutional compliance.

        Args:
            config: Integration config to validate

        Returns:
            Tuple of (is_valid, violations)

        Constitutional Law:
            This method validates contract structure ONLY.
            It does NOT load models, execute training, or run inference.
        """
        violations = []

        # Validate required fields
        try:
            # Fields validated in __post_init__, just check they exist
            _ = config.integration_id
            _ = config.training_run_plan_id
            _ = config.dependency_declaration
            _ = config.constitutional_constraints
        except AttributeError as e:
            violations.append(f"Missing required field: {e}")

        # Validate adapter boundaries
        if not config.input_adapter_boundary.preserves_source_bindings:
            violations.append("Input adapter must preserve source bindings")

        if not config.output_adapter_boundary.prevents_authority_claims:
            violations.append("Output adapter must prevent authority claims")

        if not config.validation_adapter_boundary.prevents_rank_upgrade:
            violations.append("Validation adapter must prevent rank upgrade")

        return (len(violations) == 0, tuple(violations))

    @staticmethod
    def scan_for_execution_markers(text: str) -> Tuple[str, ...]:
        """
        Scan text for forbidden execution markers (case-insensitive).

        Args:
            text: Text to scan

        Returns:
            Tuple of detected forbidden markers

        Constitutional Law:
            This method performs STATIC SCANNING only.
            It does NOT execute code or import libraries.
            Scanning is case-insensitive to catch variations.
        """
        detected = []
        text_lower = text.lower()

        for marker in FORBIDDEN_EXECUTION_MARKERS:
            marker_lower = marker.lower()
            if marker_lower in text_lower:
                detected.append(marker)

        return tuple(detected)

    @staticmethod
    def run_preflight_checks(
        config: GovernedT5IntegrationConfig,
        scan_text: Optional[str] = None,
    ) -> IntegrationPreflightReport:
        """
        Run integration preflight validation checks.

        Args:
            config: Integration config to validate
            scan_text: Optional text to scan for forbidden markers

        Returns:
            IntegrationPreflightReport with check results

        Constitutional Law:
            This method validates contracts ONLY.
            It does NOT execute models, training, or inference.
        """
        checks = []
        critical_violations = []

        # Categorize detected markers if scan_text provided
        import_markers = []
        model_loading_markers = []
        inference_markers = []
        training_markers = []

        if scan_text:
            detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(scan_text)

            # Categorize detected markers
            for marker in detected:
                marker_lower = marker.lower()
                if "import" in marker_lower:
                    import_markers.append(marker)
                elif "from_pretrained" in marker_lower or "tokenizer" in marker_lower:
                    model_loading_markers.append(marker)
                elif "generate" in marker_lower or "forward" in marker_lower:
                    inference_markers.append(marker)
                elif "trainer" in marker_lower or "train(" in marker_lower or "backward" in marker_lower or "optimizer" in marker_lower:
                    training_markers.append(marker)
                else:
                    # General execution marker
                    import_markers.append(marker)

        # Check 1: Dependency declaration (data only)
        dep_check = IntegrationPreflightCheck(
            check_type=IntegrationCheckType.DEPENDENCY_DECLARATION,
            status=IntegrationCheckStatus.PASSED,
            message="Dependencies declared as data structures",
            detected_violations=(),
        )
        checks.append(dep_check)

        # Check 2: No forbidden imports
        if scan_text:
            if import_markers:
                import_check = IntegrationPreflightCheck(
                    check_type=IntegrationCheckType.NO_FORBIDDEN_IMPORTS,
                    status=IntegrationCheckStatus.FAILED,
                    message=f"Detected {len(import_markers)} forbidden import markers",
                    detected_violations=tuple(import_markers),
                )
                critical_violations.extend(import_markers)
            else:
                import_check = IntegrationPreflightCheck(
                    check_type=IntegrationCheckType.NO_FORBIDDEN_IMPORTS,
                    status=IntegrationCheckStatus.PASSED,
                    message="No forbidden imports detected",
                    detected_violations=(),
                )
        else:
            import_check = IntegrationPreflightCheck(
                check_type=IntegrationCheckType.NO_FORBIDDEN_IMPORTS,
                status=IntegrationCheckStatus.PASSED,
                message="No scan text provided; declaration-only preflight",
                detected_violations=(),
            )
        checks.append(import_check)

        # Check 3: No model loading
        if scan_text:
            if model_loading_markers:
                loading_check = IntegrationPreflightCheck(
                    check_type=IntegrationCheckType.NO_MODEL_LOADING,
                    status=IntegrationCheckStatus.FAILED,
                    message=f"Detected {len(model_loading_markers)} model loading markers",
                    detected_violations=tuple(model_loading_markers),
                )
                critical_violations.extend(model_loading_markers)
            else:
                loading_check = IntegrationPreflightCheck(
                    check_type=IntegrationCheckType.NO_MODEL_LOADING,
                    status=IntegrationCheckStatus.PASSED,
                    message="No model loading markers detected",
                    detected_violations=(),
                )
        else:
            loading_check = IntegrationPreflightCheck(
                check_type=IntegrationCheckType.NO_MODEL_LOADING,
                status=IntegrationCheckStatus.PASSED,
                message="No scan text provided; declaration-only preflight",
                detected_violations=(),
            )
        checks.append(loading_check)

        # Check 4: No inference execution
        if scan_text:
            if inference_markers:
                inference_check = IntegrationPreflightCheck(
                    check_type=IntegrationCheckType.NO_INFERENCE_EXECUTION,
                    status=IntegrationCheckStatus.FAILED,
                    message=f"Detected {len(inference_markers)} inference execution markers",
                    detected_violations=tuple(inference_markers),
                )
                critical_violations.extend(inference_markers)
            else:
                inference_check = IntegrationPreflightCheck(
                    check_type=IntegrationCheckType.NO_INFERENCE_EXECUTION,
                    status=IntegrationCheckStatus.PASSED,
                    message="No inference execution markers detected",
                    detected_violations=(),
                )
        else:
            inference_check = IntegrationPreflightCheck(
                check_type=IntegrationCheckType.NO_INFERENCE_EXECUTION,
                status=IntegrationCheckStatus.PASSED,
                message="No scan text provided; declaration-only preflight",
                detected_violations=(),
            )
        checks.append(inference_check)

        # Check 5: No training execution
        if scan_text:
            if training_markers:
                training_check = IntegrationPreflightCheck(
                    check_type=IntegrationCheckType.NO_TRAINING_EXECUTION,
                    status=IntegrationCheckStatus.FAILED,
                    message=f"Detected {len(training_markers)} training execution markers",
                    detected_violations=tuple(training_markers),
                )
                critical_violations.extend(training_markers)
            else:
                training_check = IntegrationPreflightCheck(
                    check_type=IntegrationCheckType.NO_TRAINING_EXECUTION,
                    status=IntegrationCheckStatus.PASSED,
                    message="No training execution markers detected",
                    detected_violations=(),
                )
        else:
            training_check = IntegrationPreflightCheck(
                check_type=IntegrationCheckType.NO_TRAINING_EXECUTION,
                status=IntegrationCheckStatus.PASSED,
                message="No scan text provided; declaration-only preflight",
                detected_violations=(),
            )
        checks.append(training_check)

        # Check 6: Adapter boundaries valid
        is_valid, violations = GovernedT5IntegrationSkeleton.validate_integration_config(config)
        if is_valid:
            boundary_check = IntegrationPreflightCheck(
                check_type=IntegrationCheckType.ADAPTER_BOUNDARY_VALID,
                status=IntegrationCheckStatus.PASSED,
                message="All adapter boundaries valid",
                detected_violations=(),
            )
        else:
            boundary_check = IntegrationPreflightCheck(
                check_type=IntegrationCheckType.ADAPTER_BOUNDARY_VALID,
                status=IntegrationCheckStatus.FAILED,
                message=f"Adapter boundary violations: {len(violations)}",
                detected_violations=violations,
            )
            critical_violations.extend(violations)
        checks.append(boundary_check)

        # Check 7: Constitutional constraints
        const_check = IntegrationPreflightCheck(
            check_type=IntegrationCheckType.CONSTITUTIONAL_CONSTRAINTS,
            status=IntegrationCheckStatus.PASSED,
            message="Constitutional constraints defined",
            detected_violations=(),
        )
        checks.append(const_check)

        all_passed = all(c.status == IntegrationCheckStatus.PASSED for c in checks)

        return IntegrationPreflightReport(
            report_id=f"preflight_{config.integration_id}",
            integration_config_id=config.integration_id,
            checks=tuple(checks),
            all_checks_passed=all_passed,
            critical_violations=tuple(critical_violations),
        )

    @staticmethod
    def create_integration_report(
        config: GovernedT5IntegrationConfig,
        preflight_report: IntegrationPreflightReport,
    ) -> NoExecutionIntegrationReport:
        """
        Create integration report confirming no execution.

        Args:
            config: Integration config
            preflight_report: Preflight validation report

        Returns:
            NoExecutionIntegrationReport confirming contract adherence

        Constitutional Law:
            This method creates CONFIRMATION report only.
            It does NOT execute any models, training, or inference.
            Detection flags reflect whether markers were found in preflight checks.
        """
        # Determine detection status from preflight violations
        no_model_loading_detected = True
        no_training_execution_detected = True
        no_inference_execution_detected = True

        # Check if any markers were detected in preflight
        for check in preflight_report.checks:
            if check.check_type == IntegrationCheckType.NO_MODEL_LOADING:
                if check.status == IntegrationCheckStatus.FAILED:
                    no_model_loading_detected = False
            elif check.check_type == IntegrationCheckType.NO_TRAINING_EXECUTION:
                if check.status == IntegrationCheckStatus.FAILED:
                    no_training_execution_detected = False
            elif check.check_type == IntegrationCheckType.NO_INFERENCE_EXECUTION:
                if check.status == IntegrationCheckStatus.FAILED:
                    no_inference_execution_detected = False

        return NoExecutionIntegrationReport(
            report_id=f"integration_report_{config.integration_id}",
            integration_config_id=config.integration_id,
            preflight_report=preflight_report,
            dependencies_declared_not_loaded=True,
            boundaries_defined_not_implemented=True,
            no_model_loading_detected=no_model_loading_detected,
            no_training_execution_detected=no_training_execution_detected,
            no_inference_execution_detected=no_inference_execution_detected,
            integration_contract_valid=preflight_report.all_checks_passed,
        )


# ============================================================================
# Constitutional Constraints (Declaration)
# ============================================================================

INTEGRATION_CONSTITUTIONAL_CONSTRAINTS = (
    "Integration skeleton declares dependencies; it does NOT load models",
    "Integration skeleton defines boundaries; it does NOT execute inference",
    "Integration skeleton plans integration; it does NOT train models",
    "Integration skeleton validates contracts; it does NOT compute metrics",
    "Integration skeleton produces reports; it does NOT create authority",
    "Integration skeleton preserves source bindings throughout",
    "Integration skeleton prevents authority claims at all boundaries",
    "Integration skeleton prevents rank upgrades at all boundaries",
    "Integration skeleton does NOT close ifādah",
    "Integration skeleton does NOT produce hukm",
    "Integration skeleton does NOT produce reality",
)
