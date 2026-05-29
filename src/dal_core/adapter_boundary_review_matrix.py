"""
Adapter Boundary Review Matrix (مصفوفة مراجعة حدود المحوّلات)

PR #157: Central audit matrix documenting constitutional requirements
         at each adapter-chain boundary BEFORE T5 integration.

Constitutional Laws:
    1. Matrix is audit documentation ONLY (not validation engine)
    2. Matrix declares what MUST be preserved at each boundary
    3. Matrix declares what MUST be forbidden at each boundary
    4. Matrix does NOT execute adapters
    5. Matrix does NOT correct violations
    6. Matrix does NOT run T5
    7. Matrix does NOT replace ConstitutionalEvaluator
    8. Matrix prepares ground for PR #158 Adapter Preflight Harness

Forbidden Operations:
    ❌ import transformers: Matrix does NOT import transformers
    ❌ import torch: Matrix does NOT import torch
    ❌ tokenization: Matrix does NOT tokenize
    ❌ model loading: Matrix does NOT load models
    ❌ inference: Matrix does NOT execute inference
    ❌ training: Matrix does NOT train models
    ❌ repair violations: Matrix does NOT repair
    ❌ resolve residuals: Matrix does NOT resolve

Permitted Operations:
    ✅ Define boundary transition types
    ✅ Define requirement types
    ✅ Document constitutional requirements per boundary
    ✅ Minimal shape verification (structure only)
    ✅ Integration with golden fixtures (validation only)

Constitutional Formula:
    TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput → ConstitutionalEvaluator

    Each → transition has documented requirements:
        - What MUST be preserved (source bindings, references)
        - What MUST be forbidden (authority, rank upgrade, etc.)

Supreme Law:
    The matrix declares what must be preserved and what must be forbidden.
    The matrix does NOT execute adapters.
    The matrix does NOT correct violations.

Reference:
    User requirement: PR #157 specification (2026-05-29)
    Builds on: PR #152 (Adapter Contracts), PR #155 (Golden Fixtures)
    Prepares for: PR #158 (Adapter Preflight Harness)

Created: 2026-05-29
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional

from dal_core.constitutional_evaluator import ConstitutionalViolationSeverity


# ============================================================================
# Boundary Transition Types
# ============================================================================

class BoundaryTransitionType(Enum):
    """
    Types of adapter-chain boundary transitions.

    Transitions:
        TRAINING_EXAMPLE_TO_ADAPTER_INPUT: TrainingExample → AdapterInput
        ADAPTER_INPUT_TO_ADAPTER_RAW_OUTPUT: AdapterInput → AdapterRawOutput
        ADAPTER_RAW_OUTPUT_TO_MODEL_OUTPUT: AdapterRawOutput → ModelOutput
        MODEL_OUTPUT_TO_CONSTITUTIONAL_EVALUATOR: ModelOutput → ConstitutionalEvaluator

    Constitutional Note:
        These transitions represent the complete adapter chain.
        Each transition has constitutional requirements that MUST be enforced.
    """
    TRAINING_EXAMPLE_TO_ADAPTER_INPUT = auto()
    ADAPTER_INPUT_TO_ADAPTER_RAW_OUTPUT = auto()
    ADAPTER_RAW_OUTPUT_TO_MODEL_OUTPUT = auto()
    MODEL_OUTPUT_TO_CONSTITUTIONAL_EVALUATOR = auto()


# ============================================================================
# Boundary Requirement Types
# ============================================================================

class BoundaryRequirementType(Enum):
    """
    Types of constitutional requirements at adapter boundaries.

    Requirements:
        SOURCE_BINDING_PRESERVATION: Source bindings MUST be preserved
        REFERENCE_PRESERVATION: Referenced IDs MUST be preserved
        AUTHORITY_PROHIBITION: Authority claims MUST be forbidden
        RANK_UPGRADE_PROHIBITION: Rank upgrades MUST be forbidden
        RESIDUAL_RESOLUTION_PROHIBITION: Residual resolution MUST be forbidden
        IFADAH_CLOSURE_PROHIBITION: Ifādah closure MUST be forbidden
        HUKM_PRODUCTION_PROHIBITION: Hukm production MUST be forbidden
        REALITY_PRODUCTION_PROHIBITION: Reality production MUST be forbidden
        EXECUTION_MARKER_PROHIBITION: Execution markers MUST be forbidden

    Constitutional Note:
        These requirement types cover both preservation (what must be kept)
        and prohibition (what must be prevented).
    """
    SOURCE_BINDING_PRESERVATION = auto()
    REFERENCE_PRESERVATION = auto()
    AUTHORITY_PROHIBITION = auto()
    RANK_UPGRADE_PROHIBITION = auto()
    RESIDUAL_RESOLUTION_PROHIBITION = auto()
    IFADAH_CLOSURE_PROHIBITION = auto()
    HUKM_PRODUCTION_PROHIBITION = auto()
    REALITY_PRODUCTION_PROHIBITION = auto()
    EXECUTION_MARKER_PROHIBITION = auto()


# ============================================================================
# Boundary Requirement
# ============================================================================

@dataclass(frozen=True)
class BoundaryRequirement:
    """
    Single constitutional requirement at an adapter boundary.

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - requirement_id is unique identifier
        - requirement_type classifies the requirement
        - description explains the requirement in detail
        - verification_method describes how to verify compliance
        - failure_severity indicates severity if requirement violated

    Fields:
        requirement_id: Unique identifier for this requirement
        requirement_type: BoundaryRequirementType classification
        description: Detailed description of the requirement
        verification_method: How to verify this requirement
        failure_severity: Severity if requirement violated
    """
    requirement_id: str
    requirement_type: BoundaryRequirementType
    description: str
    verification_method: str
    failure_severity: ConstitutionalViolationSeverity

    def __post_init__(self):
        """Validate BoundaryRequirement fields."""
        if not self.requirement_id:
            raise ValueError("BoundaryRequirement requires requirement_id")
        if not self.description:
            raise ValueError("BoundaryRequirement requires description")
        if not self.verification_method:
            raise ValueError("BoundaryRequirement requires verification_method")


# ============================================================================
# Boundary Transition
# ============================================================================

@dataclass(frozen=True)
class BoundaryTransition:
    """
    Single boundary transition in the adapter chain.

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - transition_id is unique identifier
        - transition_type classifies the transition
        - source_type_name names the source dataclass
        - target_type_name names the target dataclass
        - required_preservations lists fields that MUST be preserved
        - required_prohibitions lists patterns that MUST be forbidden
        - requirements lists all constitutional requirements
        - verification_criteria lists how to verify the transition

    Fields:
        transition_id: Unique identifier for this transition
        transition_type: BoundaryTransitionType classification
        source_type_name: Name of source dataclass type
        target_type_name: Name of target dataclass type
        required_preservations: Field names that MUST be preserved
        required_prohibitions: Patterns that MUST be forbidden
        requirements: All constitutional requirements for this transition
        verification_criteria: How to verify this transition
    """
    transition_id: str
    transition_type: BoundaryTransitionType
    source_type_name: str
    target_type_name: str
    required_preservations: Tuple[str, ...]
    required_prohibitions: Tuple[str, ...]
    requirements: Tuple[BoundaryRequirement, ...]
    verification_criteria: Tuple[str, ...]

    def __post_init__(self):
        """Validate BoundaryTransition fields."""
        if not self.transition_id:
            raise ValueError("BoundaryTransition requires transition_id")
        if not self.source_type_name:
            raise ValueError("BoundaryTransition requires source_type_name")
        if not self.target_type_name:
            raise ValueError("BoundaryTransition requires target_type_name")
        if not self.requirements:
            raise ValueError("BoundaryTransition requires at least one requirement")


# ============================================================================
# Adapter Boundary Review Matrix
# ============================================================================

@dataclass(frozen=True)
class AdapterBoundaryReviewMatrix:
    """
    Complete adapter boundary review matrix.

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - matrix_id is unique identifier
        - matrix_version tracks matrix evolution
        - transitions lists all 4 boundary transitions
        - total_requirements_count sums all requirements
        - critical_requirements_count counts CRITICAL severity only

    Fields:
        matrix_id: Unique identifier for this matrix
        matrix_version: Version string (e.g., "1.0.0")
        transitions: All boundary transitions in the adapter chain
        total_requirements_count: Total count of all requirements
        critical_requirements_count: Count of CRITICAL severity requirements
    """
    matrix_id: str
    matrix_version: str
    transitions: Tuple[BoundaryTransition, ...]
    total_requirements_count: int
    critical_requirements_count: int

    def __post_init__(self):
        """Validate AdapterBoundaryReviewMatrix fields."""
        if not self.matrix_id:
            raise ValueError("AdapterBoundaryReviewMatrix requires matrix_id")
        if not self.matrix_version:
            raise ValueError("AdapterBoundaryReviewMatrix requires matrix_version")
        if not self.transitions:
            raise ValueError("AdapterBoundaryReviewMatrix requires transitions")

        # Validate all 4 transition types are present
        transition_types = {t.transition_type for t in self.transitions}
        expected_types = {
            BoundaryTransitionType.TRAINING_EXAMPLE_TO_ADAPTER_INPUT,
            BoundaryTransitionType.ADAPTER_INPUT_TO_ADAPTER_RAW_OUTPUT,
            BoundaryTransitionType.ADAPTER_RAW_OUTPUT_TO_MODEL_OUTPUT,
            BoundaryTransitionType.MODEL_OUTPUT_TO_CONSTITUTIONAL_EVALUATOR,
        }
        if transition_types != expected_types:
            raise ValueError(
                f"AdapterBoundaryReviewMatrix requires all 4 transition types; "
                f"got {len(transition_types)}"
            )


# ============================================================================
# Boundary Verification Result
# ============================================================================

@dataclass(frozen=True)
class BoundaryVerificationResult:
    """
    Result of minimal boundary verification (shape checking ONLY).

    Constitutional Requirements:
        - All fields are immutable (frozen=True)
        - verification_id is unique identifier
        - transition_id references the transition being verified
        - passed indicates whether shape verification passed
        - violations lists detected structural violations (NOT content violations)
        - preserved_bindings lists bindings that are present
        - detected_prohibitions lists forbidden patterns detected

    Fields:
        verification_id: Unique identifier for this verification
        transition_id: ID of transition being verified
        passed: Whether shape verification passed
        violations: Detected structural violations (shape only)
        preserved_bindings: Bindings that are present (field names)
        detected_prohibitions: Forbidden patterns detected (pattern names)
    """
    verification_id: str
    transition_id: str
    passed: bool
    violations: Tuple[str, ...]
    preserved_bindings: Tuple[str, ...]
    detected_prohibitions: Tuple[str, ...]

    def __post_init__(self):
        """Validate BoundaryVerificationResult fields."""
        if not self.verification_id:
            raise ValueError("BoundaryVerificationResult requires verification_id")
        if not self.transition_id:
            raise ValueError("BoundaryVerificationResult requires transition_id")


# ============================================================================
# Matrix Construction Functions
# ============================================================================

def make_training_example_to_adapter_input_transition() -> BoundaryTransition:
    """
    Create transition: TrainingExample → AdapterInput.

    Constitutional Requirements:
        - MUST preserve: source_trace_id
        - MUST preserve: source_training_example_id
        - MUST preserve: referenced candidate/residual/gate/rank IDs when present
        - MUST forbid: tokenization
        - MUST forbid: tensor creation
        - MUST forbid: model loading
        - MUST forbid: authority claims
        - MUST forbid: rank upgrade
        - MUST forbid: residual resolution

    Returns:
        BoundaryTransition for TrainingExample → AdapterInput
    """
    requirements = (
        BoundaryRequirement(
            requirement_id="te_to_ai_source_trace_id",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="AdapterInput MUST preserve source_trace_id from TrainingExample",
            verification_method="Check AdapterInput.source_trace_id == TrainingExample.source_trace_id",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="te_to_ai_source_training_example_id",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="AdapterInput MUST preserve source_training_example_id from TrainingExample",
            verification_method="Check AdapterInput.source_training_example_id == TrainingExample.training_example_id",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="te_to_ai_reference_preservation",
            requirement_type=BoundaryRequirementType.REFERENCE_PRESERVATION,
            description="AdapterInput MUST preserve referenced candidate/residual/gate/rank IDs when present",
            verification_method="Check all TrainingExample.referenced_*_ids are traceable in AdapterInput.metadata or input_text",
            failure_severity=ConstitutionalViolationSeverity.HIGH,
        ),
        BoundaryRequirement(
            requirement_id="te_to_ai_no_tokenization",
            requirement_type=BoundaryRequirementType.EXECUTION_MARKER_PROHIBITION,
            description="Adapter MUST NOT tokenize (no tokenizer, input_ids, attention_mask)",
            verification_method="Check AdapterInput has no forbidden fields: tokenizer, input_ids, attention_mask",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="te_to_ai_no_tensors",
            requirement_type=BoundaryRequirementType.EXECUTION_MARKER_PROHIBITION,
            description="Adapter MUST NOT create tensors",
            verification_method="Check AdapterInput has no tensor fields",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="te_to_ai_no_model_loading",
            requirement_type=BoundaryRequirementType.EXECUTION_MARKER_PROHIBITION,
            description="Adapter MUST NOT load models",
            verification_method="Check AdapterInput has no model reference fields",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="te_to_ai_no_authority",
            requirement_type=BoundaryRequirementType.AUTHORITY_PROHIBITION,
            description="Adapter MUST NOT claim authority",
            verification_method="Check AdapterInput.input_text has no authority phrases",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="te_to_ai_no_rank_upgrade",
            requirement_type=BoundaryRequirementType.RANK_UPGRADE_PROHIBITION,
            description="Adapter MUST NOT upgrade rank",
            verification_method="Check AdapterInput has no rank upgrade markers",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="te_to_ai_no_residual_resolution",
            requirement_type=BoundaryRequirementType.RESIDUAL_RESOLUTION_PROHIBITION,
            description="Adapter MUST NOT resolve residuals",
            verification_method="Check AdapterInput has no residual resolution markers",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
    )

    return BoundaryTransition(
        transition_id="transition_te_to_ai",
        transition_type=BoundaryTransitionType.TRAINING_EXAMPLE_TO_ADAPTER_INPUT,
        source_type_name="TrainingExample",
        target_type_name="AdapterInput",
        required_preservations=("source_trace_id", "source_training_example_id"),
        required_prohibitions=(
            "tokenizer", "input_ids", "attention_mask", "tensor", "model",
            "authority_claim", "rank_upgrade", "residual_resolution"
        ),
        requirements=requirements,
        verification_criteria=(
            "Source trace ID preserved",
            "Source training example ID preserved",
            "Referenced IDs traceable",
            "No tokenization markers",
            "No tensor markers",
            "No model loading markers",
            "No authority claims",
            "No rank upgrade claims",
            "No residual resolution claims",
        ),
    )


def make_adapter_input_to_raw_output_transition() -> BoundaryTransition:
    """
    Create transition: AdapterInput → AdapterRawOutput.

    Constitutional Requirements:
        - MUST preserve: source_adapter_input_id
        - MUST preserve: traceability to original training example through chain registry
        - MUST forbid: model generation
        - MUST forbid: tensor decoding
        - MUST forbid: inference execution

    Returns:
        BoundaryTransition for AdapterInput → AdapterRawOutput
    """
    requirements = (
        BoundaryRequirement(
            requirement_id="ai_to_aro_source_adapter_input_id",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="AdapterRawOutput MUST preserve source_adapter_input_id from AdapterInput",
            verification_method="Check AdapterRawOutput.source_adapter_input_id == AdapterInput.adapter_input_id",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="ai_to_aro_chain_traceability",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="AdapterRawOutput MUST preserve traceability to original TrainingExample through chain registry",
            verification_method="Check chain registry links AdapterRawOutput → AdapterInput → TrainingExample",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="ai_to_aro_no_generation",
            requirement_type=BoundaryRequirementType.EXECUTION_MARKER_PROHIBITION,
            description="Adapter MUST NOT generate text via model",
            verification_method="Check AdapterRawOutput.raw_output_text is abstract (not model-generated)",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="ai_to_aro_no_tensor_decoding",
            requirement_type=BoundaryRequirementType.EXECUTION_MARKER_PROHIBITION,
            description="Adapter MUST NOT decode tensors",
            verification_method="Check AdapterRawOutput has no tensor decoding markers",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="ai_to_aro_no_inference",
            requirement_type=BoundaryRequirementType.EXECUTION_MARKER_PROHIBITION,
            description="Adapter MUST NOT execute inference",
            verification_method="Check AdapterRawOutput has no inference execution markers",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
    )

    return BoundaryTransition(
        transition_id="transition_ai_to_aro",
        transition_type=BoundaryTransitionType.ADAPTER_INPUT_TO_ADAPTER_RAW_OUTPUT,
        source_type_name="AdapterInput",
        target_type_name="AdapterRawOutput",
        required_preservations=("source_adapter_input_id", "chain_traceability"),
        required_prohibitions=(
            "model_generation", "tensor_decoding", "inference_execution"
        ),
        requirements=requirements,
        verification_criteria=(
            "Source adapter input ID preserved",
            "Chain traceability maintained",
            "No model generation markers",
            "No tensor decoding markers",
            "No inference execution markers",
        ),
    )


def make_adapter_raw_output_to_model_output_transition() -> BoundaryTransition:
    """
    Create transition: AdapterRawOutput → ModelOutput.

    Constitutional Requirements:
        - MUST preserve: source_trace_id
        - MUST preserve: source_training_example_id
        - MUST preserve: referenced IDs through text/metadata when present
        - MUST forbid: authority claims
        - MUST forbid: final answer / gold label claims
        - MUST forbid: rank upgrade / hukm / reality production

    Returns:
        BoundaryTransition for AdapterRawOutput → ModelOutput
    """
    requirements = (
        BoundaryRequirement(
            requirement_id="aro_to_mo_source_trace_id",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="ModelOutput MUST preserve source_trace_id from original TrainingExample",
            verification_method="Check ModelOutput.source_trace_id == TrainingExample.source_trace_id (via chain)",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="aro_to_mo_source_training_example_id",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="ModelOutput MUST preserve source_training_example_id from original TrainingExample",
            verification_method="Check ModelOutput.source_training_example_id == TrainingExample.training_example_id (via chain)",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="aro_to_mo_reference_preservation",
            requirement_type=BoundaryRequirementType.REFERENCE_PRESERVATION,
            description="ModelOutput MUST preserve referenced IDs through predicted_text when present",
            verification_method="Check TrainingExample.referenced_*_ids are traceable in ModelOutput.predicted_text",
            failure_severity=ConstitutionalViolationSeverity.HIGH,
        ),
        BoundaryRequirement(
            requirement_id="aro_to_mo_no_authority",
            requirement_type=BoundaryRequirementType.AUTHORITY_PROHIBITION,
            description="Adapter MUST NOT claim authority",
            verification_method="Check ModelOutput.predicted_text has no authority phrases",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="aro_to_mo_no_final_answer",
            requirement_type=BoundaryRequirementType.AUTHORITY_PROHIBITION,
            description="Adapter MUST NOT claim final answer or gold label",
            verification_method="Check ModelOutput.predicted_text has no final_answer/correct_analysis/gold_label phrases",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="aro_to_mo_no_rank_upgrade",
            requirement_type=BoundaryRequirementType.RANK_UPGRADE_PROHIBITION,
            description="Adapter MUST NOT claim rank upgrade",
            verification_method="Check ModelOutput has no rank upgrade markers",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="aro_to_mo_no_hukm",
            requirement_type=BoundaryRequirementType.HUKM_PRODUCTION_PROHIBITION,
            description="Adapter MUST NOT produce hukm",
            verification_method="Check ModelOutput has no hukm production markers",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="aro_to_mo_no_reality",
            requirement_type=BoundaryRequirementType.REALITY_PRODUCTION_PROHIBITION,
            description="Adapter MUST NOT produce reality",
            verification_method="Check ModelOutput has no reality production markers",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
    )

    return BoundaryTransition(
        transition_id="transition_aro_to_mo",
        transition_type=BoundaryTransitionType.ADAPTER_RAW_OUTPUT_TO_MODEL_OUTPUT,
        source_type_name="AdapterRawOutput",
        target_type_name="ModelOutput",
        required_preservations=("source_trace_id", "source_training_example_id"),
        required_prohibitions=(
            "authority_claim", "final_answer", "gold_label", "rank_upgrade", "hukm_production", "reality_production"
        ),
        requirements=requirements,
        verification_criteria=(
            "Source trace ID preserved",
            "Source training example ID preserved",
            "Referenced IDs traceable",
            "No authority claims",
            "No final answer claims",
            "No rank upgrade claims",
            "No hukm production claims",
            "No reality production claims",
        ),
    )


def make_model_output_to_evaluator_transition() -> BoundaryTransition:
    """
    Create transition: ModelOutput → ConstitutionalEvaluator.

    Constitutional Requirements:
        - MUST require: source_trace_id
        - MUST require: source_training_example_id
        - MUST require: predicted_text
        - MUST require: model_name
        - MUST require: generation_timestamp
        - Evaluator MUST detect: missing bindings, authority claims, invented references,
          rank upgrade claims, residual deletion claims, ifādah/hukm/reality claims

    Returns:
        BoundaryTransition for ModelOutput → ConstitutionalEvaluator
    """
    requirements = (
        BoundaryRequirement(
            requirement_id="mo_to_eval_require_source_trace_id",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="ModelOutput MUST have source_trace_id for evaluation",
            verification_method="Check ModelOutput.source_trace_id is present and non-empty",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="mo_to_eval_require_source_training_example_id",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="ModelOutput MUST have source_training_example_id for evaluation",
            verification_method="Check ModelOutput.source_training_example_id is present and non-empty",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="mo_to_eval_require_predicted_text",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="ModelOutput MUST have predicted_text for evaluation",
            verification_method="Check ModelOutput.predicted_text is present and non-empty",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="mo_to_eval_require_model_name",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="ModelOutput MUST have model_name for evaluation",
            verification_method="Check ModelOutput.model_name is present and non-empty",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="mo_to_eval_require_generation_timestamp",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="ModelOutput MUST have generation_timestamp for evaluation",
            verification_method="Check ModelOutput.generation_timestamp is present and non-empty",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="mo_to_eval_detect_missing_bindings",
            requirement_type=BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            description="Evaluator MUST detect missing source bindings",
            verification_method="ConstitutionalEvaluator detects MISSING_SOURCE_TRACE_ID, MISMATCHED_SOURCE_TRACE_ID violations",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="mo_to_eval_detect_authority",
            requirement_type=BoundaryRequirementType.AUTHORITY_PROHIBITION,
            description="Evaluator MUST detect authority claims",
            verification_method="ConstitutionalEvaluator detects AUTHORITY_CLAIM violations",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="mo_to_eval_detect_invented_refs",
            requirement_type=BoundaryRequirementType.REFERENCE_PRESERVATION,
            description="Evaluator MUST detect invented references",
            verification_method="ConstitutionalEvaluator detects INVENTED_CANDIDATE_REFERENCE, INVENTED_RESIDUAL_REFERENCE violations",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="mo_to_eval_detect_rank_upgrade",
            requirement_type=BoundaryRequirementType.RANK_UPGRADE_PROHIBITION,
            description="Evaluator MUST detect rank upgrade claims",
            verification_method="ConstitutionalEvaluator detects RANK_UPGRADE_CLAIM violations",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="mo_to_eval_detect_residual_deletion",
            requirement_type=BoundaryRequirementType.RESIDUAL_RESOLUTION_PROHIBITION,
            description="Evaluator MUST detect residual deletion claims",
            verification_method="ConstitutionalEvaluator detects RESIDUAL_DELETION_CLAIM violations",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
        BoundaryRequirement(
            requirement_id="mo_to_eval_detect_ifadah_hukm_reality",
            requirement_type=BoundaryRequirementType.IFADAH_CLOSURE_PROHIBITION,
            description="Evaluator MUST detect ifādah/hukm/reality closure claims",
            verification_method="ConstitutionalEvaluator detects IFADAH_CLOSURE_CLAIM, HUKM_PRODUCTION_CLAIM, REALITY_PRODUCTION_CLAIM violations",
            failure_severity=ConstitutionalViolationSeverity.CRITICAL,
        ),
    )

    return BoundaryTransition(
        transition_id="transition_mo_to_eval",
        transition_type=BoundaryTransitionType.MODEL_OUTPUT_TO_CONSTITUTIONAL_EVALUATOR,
        source_type_name="ModelOutput",
        target_type_name="ConstitutionalEvaluator",
        required_preservations=(
            "source_trace_id", "source_training_example_id", "predicted_text", "model_name", "generation_timestamp"
        ),
        required_prohibitions=(
            "missing_bindings", "authority_claims", "invented_references", "rank_upgrade", "residual_deletion",
            "ifadah_closure", "hukm_production", "reality_production"
        ),
        requirements=requirements,
        verification_criteria=(
            "Source trace ID required",
            "Source training example ID required",
            "Predicted text required",
            "Model name required",
            "Generation timestamp required",
            "Evaluator detects missing bindings",
            "Evaluator detects authority claims",
            "Evaluator detects invented references",
            "Evaluator detects rank upgrade",
            "Evaluator detects residual deletion",
            "Evaluator detects ifādah/hukm/reality closure",
        ),
    )


def build_canonical_adapter_boundary_matrix() -> AdapterBoundaryReviewMatrix:
    """
    Build canonical adapter boundary review matrix.

    Constitutional Requirements:
        - Matrix includes all 4 transition types
        - All transitions have requirements
        - All requirement types are represented
        - Matrix is immutable

    Returns:
        AdapterBoundaryReviewMatrix with all 4 transitions
    """
    transitions = (
        make_training_example_to_adapter_input_transition(),
        make_adapter_input_to_raw_output_transition(),
        make_adapter_raw_output_to_model_output_transition(),
        make_model_output_to_evaluator_transition(),
    )

    # Count total requirements
    total_requirements = sum(len(t.requirements) for t in transitions)

    # Count critical requirements
    critical_requirements = sum(
        1 for t in transitions
        for r in t.requirements
        if r.failure_severity == ConstitutionalViolationSeverity.CRITICAL
    )

    return AdapterBoundaryReviewMatrix(
        matrix_id="adapter_boundary_matrix_v1",
        matrix_version="1.0.0",
        transitions=transitions,
        total_requirements_count=total_requirements,
        critical_requirements_count=critical_requirements,
    )


# ============================================================================
# Minimal Verification Functions (Shape Checking ONLY)
# ============================================================================

def verify_transition_shape(transition: BoundaryTransition) -> BoundaryVerificationResult:
    """
    Verify transition shape (structure ONLY, not content).

    Constitutional Requirements:
        - Check transition has all required fields
        - Check transition has at least one preservation requirement
        - Check transition has at least one prohibition requirement
        - Do NOT verify actual adapter implementations
        - Do NOT verify content compliance

    Args:
        transition: BoundaryTransition to verify

    Returns:
        BoundaryVerificationResult with shape verification result
    """
    from uuid import uuid4

    violations = []
    preserved_bindings = []
    detected_prohibitions = []

    # Check transition has requirements
    if not transition.requirements:
        violations.append("Transition has no requirements")

    # Check transition has preservations
    if not transition.required_preservations:
        violations.append("Transition has no required preservations")
    else:
        preserved_bindings = list(transition.required_preservations)

    # Check transition has prohibitions
    if not transition.required_prohibitions:
        violations.append("Transition has no required prohibitions")
    else:
        detected_prohibitions = list(transition.required_prohibitions)

    # Check requirements have preservation and prohibition types
    has_preservation = any(
        r.requirement_type in (
            BoundaryRequirementType.SOURCE_BINDING_PRESERVATION,
            BoundaryRequirementType.REFERENCE_PRESERVATION,
        )
        for r in transition.requirements
    )
    has_prohibition = any(
        r.requirement_type in (
            BoundaryRequirementType.AUTHORITY_PROHIBITION,
            BoundaryRequirementType.RANK_UPGRADE_PROHIBITION,
            BoundaryRequirementType.RESIDUAL_RESOLUTION_PROHIBITION,
            BoundaryRequirementType.IFADAH_CLOSURE_PROHIBITION,
            BoundaryRequirementType.HUKM_PRODUCTION_PROHIBITION,
            BoundaryRequirementType.REALITY_PRODUCTION_PROHIBITION,
            BoundaryRequirementType.EXECUTION_MARKER_PROHIBITION,
        )
        for r in transition.requirements
    )

    if not has_preservation:
        violations.append("Transition requirements missing preservation type")
    if not has_prohibition:
        violations.append("Transition requirements missing prohibition type")

    passed = len(violations) == 0

    return BoundaryVerificationResult(
        verification_id=f"verify_transition_{uuid4().hex[:8]}",
        transition_id=transition.transition_id,
        passed=passed,
        violations=tuple(violations),
        preserved_bindings=tuple(preserved_bindings),
        detected_prohibitions=tuple(detected_prohibitions),
    )


def verify_matrix_shape(matrix: AdapterBoundaryReviewMatrix) -> BoundaryVerificationResult:
    """
    Verify matrix shape (structure ONLY, not content).

    Constitutional Requirements:
        - Check matrix has all 4 transition types
        - Check all transitions are valid
        - Check requirement counts are correct
        - Do NOT verify actual adapter implementations
        - Do NOT verify content compliance

    Args:
        matrix: AdapterBoundaryReviewMatrix to verify

    Returns:
        BoundaryVerificationResult with shape verification result
    """
    from uuid import uuid4

    violations = []
    preserved_bindings = []
    detected_prohibitions = []

    # Check all 4 transition types present
    transition_types = {t.transition_type for t in matrix.transitions}
    expected_types = {
        BoundaryTransitionType.TRAINING_EXAMPLE_TO_ADAPTER_INPUT,
        BoundaryTransitionType.ADAPTER_INPUT_TO_ADAPTER_RAW_OUTPUT,
        BoundaryTransitionType.ADAPTER_RAW_OUTPUT_TO_MODEL_OUTPUT,
        BoundaryTransitionType.MODEL_OUTPUT_TO_CONSTITUTIONAL_EVALUATOR,
    }
    if transition_types != expected_types:
        violations.append(f"Matrix missing required transition types; has {len(transition_types)}, expected 4")

    # Verify each transition shape
    for transition in matrix.transitions:
        result = verify_transition_shape(transition)
        if not result.passed:
            violations.extend(result.violations)

    # Check requirement counts
    actual_total = sum(len(t.requirements) for t in matrix.transitions)
    if actual_total != matrix.total_requirements_count:
        violations.append(f"Matrix total_requirements_count mismatch: {actual_total} != {matrix.total_requirements_count}")

    actual_critical = sum(
        1 for t in matrix.transitions
        for r in t.requirements
        if r.failure_severity == ConstitutionalViolationSeverity.CRITICAL
    )
    if actual_critical != matrix.critical_requirements_count:
        violations.append(f"Matrix critical_requirements_count mismatch: {actual_critical} != {matrix.critical_requirements_count}")

    # Collect all preservations and prohibitions
    for transition in matrix.transitions:
        preserved_bindings.extend(transition.required_preservations)
        detected_prohibitions.extend(transition.required_prohibitions)

    passed = len(violations) == 0

    return BoundaryVerificationResult(
        verification_id=f"verify_matrix_{uuid4().hex[:8]}",
        transition_id=matrix.matrix_id,
        passed=passed,
        violations=tuple(violations),
        preserved_bindings=tuple(set(preserved_bindings)),  # unique
        detected_prohibitions=tuple(set(detected_prohibitions)),  # unique
    )


def verify_golden_fixture_against_matrix(
    fixture: "GoldenNoOpChainFixture",  # type: ignore
    matrix: AdapterBoundaryReviewMatrix,
) -> Tuple[BoundaryVerificationResult, ...]:
    """
    Verify golden fixture chain against matrix requirements (minimal shape checking ONLY).

    Constitutional Requirements:
        - Check fixture has all chain components
        - Check source bindings are present in fixture
        - Do NOT perform deep content validation (that's PR #158)
        - This is MINIMAL verification only

    Args:
        fixture: GoldenNoOpChainFixture to verify
        matrix: AdapterBoundaryReviewMatrix to verify against

    Returns:
        Tuple of BoundaryVerificationResult for each transition
    """
    from uuid import uuid4

    results = []

    # Transition 1: TrainingExample → AdapterInput
    te_to_ai_violations = []
    te_to_ai_preserved = []

    if fixture.adapter_input.source_trace_id == fixture.source_training_example.source_trace_id:
        te_to_ai_preserved.append("source_trace_id")
    else:
        te_to_ai_violations.append("source_trace_id not preserved")

    if fixture.adapter_input.source_training_example_id == fixture.source_training_example.training_example_id:
        te_to_ai_preserved.append("source_training_example_id")
    else:
        te_to_ai_violations.append("source_training_example_id not preserved")

    results.append(BoundaryVerificationResult(
        verification_id=f"verify_fixture_te_to_ai_{uuid4().hex[:8]}",
        transition_id="transition_te_to_ai",
        passed=len(te_to_ai_violations) == 0,
        violations=tuple(te_to_ai_violations),
        preserved_bindings=tuple(te_to_ai_preserved),
        detected_prohibitions=(),
    ))

    # Transition 2: AdapterInput → AdapterRawOutput
    ai_to_aro_violations = []
    ai_to_aro_preserved = []

    if fixture.adapter_raw_output.source_adapter_input_id == fixture.adapter_input.adapter_input_id:
        ai_to_aro_preserved.append("source_adapter_input_id")
    else:
        ai_to_aro_violations.append("source_adapter_input_id not preserved")

    results.append(BoundaryVerificationResult(
        verification_id=f"verify_fixture_ai_to_aro_{uuid4().hex[:8]}",
        transition_id="transition_ai_to_aro",
        passed=len(ai_to_aro_violations) == 0,
        violations=tuple(ai_to_aro_violations),
        preserved_bindings=tuple(ai_to_aro_preserved),
        detected_prohibitions=(),
    ))

    # Transition 3: AdapterRawOutput → ModelOutput
    aro_to_mo_violations = []
    aro_to_mo_preserved = []

    if fixture.model_output.source_trace_id == fixture.source_training_example.source_trace_id:
        aro_to_mo_preserved.append("source_trace_id")
    else:
        aro_to_mo_violations.append("source_trace_id not preserved")

    if fixture.model_output.source_training_example_id == fixture.source_training_example.training_example_id:
        aro_to_mo_preserved.append("source_training_example_id")
    else:
        aro_to_mo_violations.append("source_training_example_id not preserved")

    results.append(BoundaryVerificationResult(
        verification_id=f"verify_fixture_aro_to_mo_{uuid4().hex[:8]}",
        transition_id="transition_aro_to_mo",
        passed=len(aro_to_mo_violations) == 0,
        violations=tuple(aro_to_mo_violations),
        preserved_bindings=tuple(aro_to_mo_preserved),
        detected_prohibitions=(),
    ))

    # Transition 4: ModelOutput → ConstitutionalEvaluator
    mo_to_eval_violations = []
    mo_to_eval_preserved = []

    if fixture.model_output.source_trace_id:
        mo_to_eval_preserved.append("source_trace_id")
    else:
        mo_to_eval_violations.append("source_trace_id missing")

    if fixture.model_output.source_training_example_id:
        mo_to_eval_preserved.append("source_training_example_id")
    else:
        mo_to_eval_violations.append("source_training_example_id missing")

    if fixture.model_output.predicted_text:
        mo_to_eval_preserved.append("predicted_text")
    else:
        mo_to_eval_violations.append("predicted_text missing")

    results.append(BoundaryVerificationResult(
        verification_id=f"verify_fixture_mo_to_eval_{uuid4().hex[:8]}",
        transition_id="transition_mo_to_eval",
        passed=len(mo_to_eval_violations) == 0,
        violations=tuple(mo_to_eval_violations),
        preserved_bindings=tuple(mo_to_eval_preserved),
        detected_prohibitions=(),
    ))

    return tuple(results)
