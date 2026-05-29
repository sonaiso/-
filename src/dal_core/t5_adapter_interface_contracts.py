"""
T5 Adapter Interface Contracts (عقود واجهة محوّل T5)

PR #152: Adapter interface contracts between governed T5 integration skeleton
         and future T5 implementation (INTERFACES ONLY, NO EXECUTION).

Constitutional Laws:
    1. Adapter contracts define boundaries; they do NOT implement execution
    2. InputAdapterContract prepares abstract input text; it does NOT tokenize
    3. OutputAdapterContract maps abstract raw text to ModelOutput; it does NOT generate
    4. ValidationAdapterContract checks contracts; it does NOT execute models
    5. Adapter results do NOT upgrade rank
    6. Adapter results do NOT resolve residuals
    7. Adapter results do NOT close ifādah
    8. Adapter results do NOT produce hukm
    9. Adapter results do NOT produce reality
    10. Adapter results do NOT create constitutional authority

Forbidden Operations:
    ❌ import transformers: Adapter contracts do NOT import transformers
    ❌ import torch: Adapter contracts do NOT import torch
    ❌ tokenization: Adapter contracts do NOT tokenize
    ❌ tensor conversion: Adapter contracts do NOT convert to tensors
    ❌ model loading: Adapter contracts do NOT load models
    ❌ .from_pretrained(): Adapter contracts do NOT load checkpoints
    ❌ .generate(): Adapter contracts do NOT generate text
    ❌ Trainer: Adapter contracts do NOT create trainers
    ❌ training loop: Adapter contracts do NOT train models
    ❌ inference execution: Adapter contracts do NOT execute inference
    ❌ metrics computation: Adapter contracts do NOT compute metrics

Permitted Operations:
    ✅ Protocol/ABC definitions: Define abstract method signatures
    ✅ frozen dataclasses: Define immutable boundary data structures
    ✅ validation logic: Check data structure completeness
    ✅ source binding preservation: Maintain constitutional bindings
    ✅ abstract text preparation: Define input text format specification
    ✅ abstract output mapping: Define output to ModelOutput mapping spec

Constitutional Formula:
    TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput → ConstitutionalEvaluator

    Adapter contracts are INTERFACES between:
        - Governed constitutional skeleton (already stable)
        - Future T5 implementation (not in this PR)

Supreme Law:
    Adapter contracts declare transformation boundaries.
    Adapter contracts do NOT execute transformations.

Reference:
    User requirement: PR #152 specification (2026-05-29)
    Builds on: PR #150 (GovernedT5IntegrationSkeleton)
    Consumes: PR #146 (TrainingExample), PR #147 (ModelOutput)
    Validates with: PR #147 (ConstitutionalEvaluator)

Created: 2026-05-29
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol, Tuple, Optional, List
from abc import ABC, abstractmethod

from dal_core.training_example import TrainingExample
from dal_core.model_output import ModelOutput
from dal_core.governed_t5_integration_skeleton import (
    GovernedT5IntegrationConfig,
    AdapterBoundaryPlan,
)


# ============================================================================
# Adapter Status and Violation Types
# ============================================================================

class AdapterStatus(Enum):
    """
    Status of adapter operation result.

    States:
        VALID: Adapter operation completed successfully, output is valid
        BOUNDARY_VIOLATION: Adapter violated integration boundary constraints
        CONSTITUTIONAL_VIOLATION: Adapter violated constitutional constraints
        STRUCTURAL_ERROR: Adapter encountered structural data error

    Constitutional Note:
        These statuses classify adapter results, NOT model predictions.
        Model prediction quality is evaluated by ConstitutionalEvaluator.
    """
    VALID = auto()
    BOUNDARY_VIOLATION = auto()
    CONSTITUTIONAL_VIOLATION = auto()
    STRUCTURAL_ERROR = auto()


class AdapterViolationType(Enum):
    """
    Types of adapter boundary violations.

    Violations:
        MISSING_SOURCE_TRACE_ID: Adapter lost source_trace_id binding
        MISSING_SOURCE_TRAINING_EXAMPLE_ID: Adapter lost source_training_example_id binding
        TOKENIZATION_ATTEMPTED: Adapter attempted forbidden tokenization
        TENSOR_CONVERSION_ATTEMPTED: Adapter attempted forbidden tensor conversion
        MODEL_LOADING_ATTEMPTED: Adapter attempted forbidden model loading
        INFERENCE_EXECUTION_ATTEMPTED: Adapter attempted forbidden inference
        TRAINING_EXECUTION_ATTEMPTED: Adapter attempted forbidden training
        RANK_UPGRADE_ATTEMPTED: Adapter attempted forbidden rank upgrade
        RESIDUAL_RESOLUTION_ATTEMPTED: Adapter attempted forbidden residual resolution
        IFADAH_CLOSURE_ATTEMPTED: Adapter attempted forbidden ifādah closure
        HUKM_PRODUCTION_ATTEMPTED: Adapter attempted forbidden hukm production
        REALITY_PRODUCTION_ATTEMPTED: Adapter attempted forbidden reality production
        AUTHORITY_CLAIM_ATTEMPTED: Adapter attempted forbidden authority claim
        FORBIDDEN_FIELD_PRESENT: Adapter contains forbidden field

    Constitutional Note:
        These violations represent boundary breaches at adapter layer.
        They are distinct from ConstitutionalViolationType which evaluates
        model output content.
    """
    # Source binding violations
    MISSING_SOURCE_TRACE_ID = auto()
    MISSING_SOURCE_TRAINING_EXAMPLE_ID = auto()

    # Execution violations
    TOKENIZATION_ATTEMPTED = auto()
    TENSOR_CONVERSION_ATTEMPTED = auto()
    MODEL_LOADING_ATTEMPTED = auto()
    INFERENCE_EXECUTION_ATTEMPTED = auto()
    TRAINING_EXECUTION_ATTEMPTED = auto()

    # Constitutional violations
    RANK_UPGRADE_ATTEMPTED = auto()
    RESIDUAL_RESOLUTION_ATTEMPTED = auto()
    IFADAH_CLOSURE_ATTEMPTED = auto()
    HUKM_PRODUCTION_ATTEMPTED = auto()
    REALITY_PRODUCTION_ATTEMPTED = auto()
    AUTHORITY_CLAIM_ATTEMPTED = auto()

    # Structural violations
    FORBIDDEN_FIELD_PRESENT = auto()


# ============================================================================
# Adapter Input
# ============================================================================

@dataclass(frozen=True)
class AdapterInput:
    """
    Immutable input to adapter (abstract text ONLY, not tokenized).

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - adapter_input_id is unique identifier
        - source_training_example_id MUST reference valid TrainingExample
        - source_trace_id MUST reference valid AlgorithmTracePayload
        - input_text is prepared abstract text (NOT tokenized)
        - metadata preserves additional context as strings
        - NO tokenizer field
        - NO tensor field
        - NO model reference field
        - Source bindings MUST be preserved from TrainingExample

    Forbidden Fields:
        ❌ tokenizer: AdapterInput does NOT contain tokenizer
        ❌ input_ids: AdapterInput does NOT contain token IDs
        ❌ attention_mask: AdapterInput does NOT contain tensors
        ❌ tensor: AdapterInput does NOT contain torch tensors
        ❌ model: AdapterInput does NOT reference model
        ❌ device: AdapterInput does NOT specify GPU/device
        ❌ logits: AdapterInput does NOT contain model outputs
        ❌ loss: AdapterInput does NOT contain training loss

    Fields:
        adapter_input_id: Unique identifier for this adapter input
        source_training_example_id: training_example_id from TrainingExample (BINDING)
        source_trace_id: trace_id from AlgorithmTracePayload (BINDING)
        input_text: Prepared input text (abstract, NOT tokenized)
        metadata: Additional context as string key-value pairs
    """
    adapter_input_id: str
    source_training_example_id: str
    source_trace_id: str
    input_text: str
    metadata: Tuple[Tuple[str, str], ...]  # ((key, value), ...)

    def __post_init__(self):
        """
        Validate AdapterInput constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.adapter_input_id:
            raise ValueError("AdapterInput requires adapter_input_id")

        if not self.source_training_example_id:
            raise ValueError("AdapterInput requires source_training_example_id")

        if not self.source_trace_id:
            raise ValueError("AdapterInput requires source_trace_id")

        if not self.input_text:
            raise ValueError("AdapterInput requires input_text")


# ============================================================================
# Adapter Raw Output
# ============================================================================

@dataclass(frozen=True)
class AdapterRawOutput:
    """
    Immutable raw output from adapter (abstract text ONLY, not decoded tensors).

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - adapter_output_id is unique identifier
        - source_adapter_input_id MUST reference valid AdapterInput
        - raw_output_text is abstract text (NOT decoded from tensors)
        - adapter_metadata preserves adapter-specific context
        - NO tensor field
        - NO logits field
        - NO model reference field
        - Source bindings MUST be traceable to TrainingExample

    Forbidden Fields:
        ❌ output_ids: AdapterRawOutput does NOT contain token IDs
        ❌ logits: AdapterRawOutput does NOT contain logits
        ❌ scores: AdapterRawOutput does NOT contain scores
        ❌ tensor: AdapterRawOutput does NOT contain torch tensors
        ❌ model: AdapterRawOutput does NOT reference model
        ❌ device: AdapterRawOutput does NOT specify GPU/device
        ❌ loss: AdapterRawOutput does NOT contain training loss
        ❌ trainer: AdapterRawOutput does NOT reference Trainer

    Fields:
        adapter_output_id: Unique identifier for this adapter output
        source_adapter_input_id: adapter_input_id from AdapterInput (BINDING)
        raw_output_text: Raw output text (abstract, NOT decoded tensors)
        adapter_metadata: Adapter-specific metadata as string pairs
    """
    adapter_output_id: str
    source_adapter_input_id: str
    raw_output_text: str
    adapter_metadata: Tuple[Tuple[str, str], ...]  # ((key, value), ...)

    def __post_init__(self):
        """
        Validate AdapterRawOutput constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.adapter_output_id:
            raise ValueError("AdapterRawOutput requires adapter_output_id")

        if not self.source_adapter_input_id:
            raise ValueError("AdapterRawOutput requires source_adapter_input_id")

        if not self.raw_output_text:
            raise ValueError("AdapterRawOutput requires raw_output_text")


# ============================================================================
# Adapter Validation Result
# ============================================================================

@dataclass(frozen=True)
class AdapterValidationResult:
    """
    Immutable result of adapter boundary validation.

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - is_valid is boolean validation result
        - violations list adapter boundary violations
        - warnings list non-critical issues
        - checked_constraints list constraints that were validated
        - NO repair method
        - NO resolution method
        - Validation DETECTS violations, does NOT resolve them

    Forbidden Fields:
        ❌ repair_suggestions: AdapterValidationResult does NOT repair
        ❌ resolved_violations: AdapterValidationResult does NOT resolve
        ❌ upgraded_rank: AdapterValidationResult does NOT upgrade rank
        ❌ closed_ifadah: AdapterValidationResult does NOT close ifādah

    Fields:
        validation_id: Unique identifier for this validation
        is_valid: Whether validation passed (no violations)
        violations: List of adapter boundary violations detected
        warnings: List of non-critical warnings
        checked_constraints: List of constraints that were checked
    """
    validation_id: str
    is_valid: bool
    violations: Tuple[AdapterViolationType, ...]
    warnings: Tuple[str, ...]
    checked_constraints: Tuple[str, ...]

    def __post_init__(self):
        """
        Validate AdapterValidationResult constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.validation_id:
            raise ValueError("AdapterValidationResult requires validation_id")

        # Validate consistency: if violations present, is_valid must be False
        if self.violations and self.is_valid:
            raise ValueError(
                "AdapterValidationResult cannot be valid with violations present"
            )


# ============================================================================
# Adapter Result
# ============================================================================

@dataclass(frozen=True)
class AdapterResult:
    """
    Immutable result of adapter operation (carries data, does NOT resolve).

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - adapter_result_id is unique identifier
        - status indicates result classification
        - model_output present only if status == VALID
        - violations list any boundary violations detected
        - residuals list unresolved issues (preserved, NOT resolved)
        - NO resolution method
        - NO repair method
        - NO rank upgrade
        - Adapter result CARRIES violations/residuals, does NOT resolve them

    Forbidden Fields:
        ❌ resolved_residuals: AdapterResult does NOT resolve residuals
        ❌ upgraded_rank: AdapterResult does NOT upgrade rank
        ❌ closed_ifadah: AdapterResult does NOT close ifādah
        ❌ produced_hukm: AdapterResult does NOT produce hukm
        ❌ produced_reality: AdapterResult does NOT produce reality
        ❌ repair_function: AdapterResult does NOT contain repair logic
        ❌ resolution_function: AdapterResult does NOT contain resolution logic
        ❌ optimizer: AdapterResult does NOT contain optimizer
        ❌ trainer: AdapterResult does NOT contain trainer

    Fields:
        adapter_result_id: Unique identifier for this result
        status: AdapterStatus classification
        model_output: ModelOutput if successful (None if failed)
        violations: Adapter boundary violations detected
        residuals: Unresolved issues (preserved, NOT resolved)
    """
    adapter_result_id: str
    status: AdapterStatus
    model_output: Optional[ModelOutput]
    violations: Tuple[AdapterViolationType, ...]
    residuals: Tuple[str, ...]

    def __post_init__(self):
        """
        Validate AdapterResult constitutional requirements.

        Raises:
            ValueError: If constitutional requirements violated
        """
        if not self.adapter_result_id:
            raise ValueError("AdapterResult requires adapter_result_id")

        # Validate consistency: VALID status requires model_output
        if self.status == AdapterStatus.VALID and self.model_output is None:
            raise ValueError(
                "AdapterResult with VALID status requires model_output"
            )

        # Validate consistency: non-VALID status requires violations or residuals
        if self.status != AdapterStatus.VALID:
            if not self.violations and not self.residuals:
                raise ValueError(
                    f"AdapterResult with {self.status} status requires violations or residuals"
                )


# ============================================================================
# Input Adapter Contract (Protocol)
# ============================================================================

class InputAdapterContract(Protocol):
    """
    Protocol for input adapter (TrainingExample → AdapterInput).

    Constitutional Requirements:
        1. Adapter MUST preserve source_trace_id from TrainingExample
        2. Adapter MUST preserve source_training_example_id from TrainingExample
        3. Adapter prepares abstract input text, does NOT tokenize
        4. Adapter does NOT load models
        5. Adapter does NOT create tensors
        6. Adapter does NOT execute inference
        7. Adapter does NOT train models

    Forbidden Operations:
        ❌ tokenize(): Does NOT tokenize
        ❌ to_tensor(): Does NOT create tensors
        ❌ load_model(): Does NOT load models

    Required Methods:
        prepare_input(): Transform TrainingExample to AdapterInput
        validate_input(): Validate AdapterInput structure

    Constitutional Formula:
        TrainingExample → AdapterInput
        (source bindings preserved, no execution)
    """

    def prepare_input(self, training_example: TrainingExample) -> AdapterInput:
        """
        Prepare AdapterInput from TrainingExample.

        Constitutional Requirements:
            - MUST preserve source_trace_id
            - MUST preserve source_training_example_id
            - MUST NOT tokenize
            - MUST NOT create tensors
            - MUST NOT load models

        Args:
            training_example: TrainingExample to transform

        Returns:
            AdapterInput with preserved bindings

        Raises:
            ValueError: If constitutional requirements violated
        """
        ...

    def validate_input(self, adapter_input: AdapterInput) -> AdapterValidationResult:
        """
        Validate AdapterInput structure and bindings.

        Constitutional Requirements:
            - MUST check source_trace_id present
            - MUST check source_training_example_id present
            - MUST check input_text present
            - MUST NOT execute models
            - MUST NOT modify input

        Args:
            adapter_input: AdapterInput to validate

        Returns:
            AdapterValidationResult with violations detected
        """
        ...


# ============================================================================
# Output Adapter Contract (Protocol)
# ============================================================================

class OutputAdapterContract(Protocol):
    """
    Protocol for output adapter (AdapterRawOutput → ModelOutput).

    Constitutional Requirements:
        1. Adapter MUST map abstract raw text to ModelOutput
        2. Adapter MUST preserve source bindings through transformation chain
        3. Adapter does NOT generate text (receives already-generated abstract text)
        4. Adapter does NOT decode tensors (receives abstract text)
        5. Adapter does NOT execute inference
        6. Adapter does NOT create authority
        7. Adapter produces ModelOutput for ConstitutionalEvaluator review

    Forbidden Operations:
        ❌ model.generate(): Does NOT generate text
        ❌ decode_tensor(): Does NOT decode tensors
        ❌ load_model(): Does NOT load models
        ❌ upgrade_rank(): Does NOT upgrade rank

    Required Methods:
        parse_output(): Transform AdapterRawOutput to ModelOutput
        validate_output(): Validate ModelOutput structure

    Constitutional Formula:
        AdapterRawOutput → ModelOutput → ConstitutionalEvaluator
        (source bindings preserved, no authority claims)
    """

    def parse_output(
        self,
        adapter_raw_output: AdapterRawOutput,
        source_training_example_id: str,
        source_trace_id: str,
    ) -> ModelOutput:
        """
        Parse AdapterRawOutput into ModelOutput.

        Constitutional Requirements:
            - MUST preserve source_trace_id
            - MUST preserve source_training_example_id
            - MUST NOT generate text (receives abstract text)
            - MUST NOT decode tensors
            - MUST NOT claim authority

        Args:
            adapter_raw_output: Raw output from adapter
            source_training_example_id: TrainingExample binding
            source_trace_id: Trace binding

        Returns:
            ModelOutput with preserved bindings

        Raises:
            ValueError: If constitutional requirements violated
        """
        ...

    def validate_output(self, model_output: ModelOutput) -> AdapterValidationResult:
        """
        Validate ModelOutput structure and bindings.

        Constitutional Requirements:
            - MUST check source_trace_id present
            - MUST check source_training_example_id present
            - MUST check predicted_text present
            - MUST NOT execute models
            - MUST NOT modify output

        Args:
            model_output: ModelOutput to validate

        Returns:
            AdapterValidationResult with violations detected
        """
        ...


# ============================================================================
# Validation Adapter Contract (ABC)
# ============================================================================

class ValidationAdapterContract(ABC):
    """
    Abstract base class for validation adapter.

    Constitutional Requirements:
        1. Validator MUST check GovernedT5IntegrationConfig compliance
        2. Validator MUST check AdapterBoundaryPlan constraints
        3. Validator MUST detect forbidden imports/execution markers
        4. Validator does NOT execute models
        5. Validator does NOT train models
        6. Validator does NOT resolve violations (only detects)
        7. Validator produces reports, NOT corrections

    Forbidden Operations:
        ❌ repair_violations(): Does NOT repair
        ❌ resolve_residuals(): Does NOT resolve
        ❌ load_model(): Does NOT load models
        ❌ execute_inference(): Does NOT execute inference

    Required Methods:
        validate_adapter_boundaries(): Check adapter boundary compliance
        check_constitutional_compliance(): Check constitutional constraints

    Constitutional Formula:
        GovernedT5IntegrationConfig + AdapterBoundaryPlan → ValidationReport
        (detection only, no execution, no resolution)
    """

    @abstractmethod
    def validate_adapter_boundaries(
        self,
        config: GovernedT5IntegrationConfig,
    ) -> AdapterValidationResult:
        """
        Validate adapter boundaries against integration config.

        Constitutional Requirements:
            - MUST check all adapter boundaries defined
            - MUST check no forbidden imports present
            - MUST check no execution markers present
            - MUST NOT execute models
            - MUST NOT load dependencies

        Args:
            config: GovernedT5IntegrationConfig to validate

        Returns:
            AdapterValidationResult with violations detected
        """
        pass

    @abstractmethod
    def check_constitutional_compliance(
        self,
        adapter_input: AdapterInput,
    ) -> AdapterValidationResult:
        """
        Check adapter input for constitutional compliance.

        Constitutional Requirements:
            - MUST check source bindings present
            - MUST check no forbidden fields present
            - MUST check no authority claims present
            - MUST NOT execute models
            - MUST NOT modify input

        Args:
            adapter_input: AdapterInput to check

        Returns:
            AdapterValidationResult with violations detected
        """
        pass


# ============================================================================
# Forbidden Field Detection Constants
# ============================================================================

# These constants list forbidden field names for validation purposes.
# They are intentionally declared here to enable validation logic.
# They do NOT represent actual fields in any adapter contract.

FORBIDDEN_ADAPTER_FIELDS: Tuple[str, ...] = (
    # Tokenization fields (FORBIDDEN)
    "tokenizer",
    "input_ids",
    "attention_mask",
    "token_type_ids",

    # Tensor fields (FORBIDDEN)
    "tensor",
    "logits",
    "hidden_states",
    "scores",

    # Model fields (FORBIDDEN)
    "model",
    "model_instance",
    "loaded_model",
    "checkpoint",

    # Device fields (FORBIDDEN)
    "device",
    "cuda",
    "gpu",

    # Training fields (FORBIDDEN)
    "trainer",
    "optimizer",
    "loss",
    "gradients",

    # Authority fields (FORBIDDEN)
    "upgraded_rank",
    "resolved_residuals",
    "closed_ifadah",
    "produced_hukm",
    "produced_reality",
    "constitutional_authority",
    "final_answer",
    "correct_analysis",

    # Execution fields (FORBIDDEN)
    "forward_pass",
    "inference_result",
    "training_result",
    "metrics_result",
)
