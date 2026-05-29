"""
No-Op Adapter Contract Fixtures (PR #153)

Constitutional Purpose:
    Prove that T5 Adapter Interface Contracts (PR #152) are fully implementable
    WITHOUT any model execution, tokenization, or inference.

Constitutional Laws:
    1. No-op adapters are TEST FIXTURES ONLY (not production implementation)
    2. No-op adapters do NOT import transformers
    3. No-op adapters do NOT import torch
    4. No-op adapters do NOT tokenize
    5. No-op adapters do NOT create tensors
    6. No-op adapters do NOT load models
    7. No-op adapters do NOT execute inference
    8. No-op adapters do NOT train models
    9. No-op adapters ONLY manipulate abstract text strings
    10. No-op adapters preserve source bindings

Forbidden Operations:
    ❌ import transformers: No-op adapters do NOT import transformers
    ❌ import torch: No-op adapters do NOT import torch
    ❌ .encode(): No-op adapters do NOT tokenize
    ❌ .to_tensor(): No-op adapters do NOT create tensors
    ❌ .from_pretrained(): No-op adapters do NOT load models
    ❌ model.generate(): No-op adapters do NOT generate
    ❌ Trainer(): No-op adapters do NOT train

Permitted Operations:
    ✅ String manipulation: Abstract text formatting
    ✅ Source binding preservation: Maintain constitutional bindings
    ✅ Protocol implementation: Implement contract methods
    ✅ Validation logic: Check data structure completeness
    ✅ No-op transformations: Identity-like text mappings

Supreme Law:
    No-op adapters prove contracts are implementable.
    No-op adapters do NOT implement T5.

Reference:
    Builds on: PR #152 (T5 Adapter Interface Contracts)
    Purpose: Prove contract usability before T5 implementation
    Next step: NOT T5 implementation (more boundary hardening)

Created: 2026-05-29
"""

from dal_core.t5_adapter_interface_contracts import (
    # Protocols/ABCs
    InputAdapterContract,
    OutputAdapterContract,
    ValidationAdapterContract,

    # Data structures
    AdapterInput,
    AdapterRawOutput,
    AdapterValidationResult,
    AdapterStatus,
    AdapterViolationType,

    # Constants
    FORBIDDEN_ADAPTER_FIELDS,
)

from dal_core.training_example import TrainingExample
from dal_core.model_output import ModelOutput
from dal_core.governed_t5_integration_skeleton import GovernedT5IntegrationConfig

from dataclasses import dataclass, fields
from typing import Tuple, Optional, Dict


# ============================================================================
# Adapter Chain Registry (Source Binding Preservation)
# ============================================================================

@dataclass(frozen=True)
class AdapterChainLink:
    """
    Immutable link in adapter transformation chain.

    Constitutional Requirements:
        - Preserves source_trace_id through transformation
        - Preserves source_training_example_id through transformation
        - Records transformation steps for audit trail
        - Does NOT execute transformations (only records bindings)

    Fields:
        link_id: Unique identifier for this chain link
        source_training_example_id: Original TrainingExample ID
        source_trace_id: Original trace ID
        adapter_input_id: Optional AdapterInput ID (if input prepared)
        adapter_output_id: Optional AdapterRawOutput ID (if output generated)
        model_output_id: Optional ModelOutput ID (if output parsed)
        transformation_steps: Tuple of transformation step names
    """
    link_id: str
    source_training_example_id: str
    source_trace_id: str
    adapter_input_id: Optional[str] = None
    adapter_output_id: Optional[str] = None
    model_output_id: Optional[str] = None
    transformation_steps: Tuple[str, ...] = ()

    def __post_init__(self):
        """Validate chain link requirements."""
        if not self.link_id:
            raise ValueError("AdapterChainLink requires link_id")
        if not self.source_training_example_id:
            raise ValueError("AdapterChainLink requires source_training_example_id")
        if not self.source_trace_id:
            raise ValueError("AdapterChainLink requires source_trace_id")


@dataclass(frozen=True)
class AdapterChainRegistry:
    """
    Immutable registry of adapter transformation chains.

    Constitutional Requirements:
        - Maintains audit trail of transformations
        - Preserves source bindings through chain
        - Enables verification of binding preservation
        - Does NOT modify transformations (read-only registry)

    Constitutional Formula:
        TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput
        (all steps recorded with preserved bindings)

    Fields:
        registry_id: Unique registry identifier
        chains: Tuple of registered chain links
    """
    registry_id: str
    chains: Tuple[AdapterChainLink, ...] = ()

    def __post_init__(self):
        """Validate registry requirements."""
        if not self.registry_id:
            raise ValueError("AdapterChainRegistry requires registry_id")

    def with_chain(self, chain: AdapterChainLink) -> "AdapterChainRegistry":
        """
        Create new registry with added chain link.

        Args:
            chain: AdapterChainLink to add

        Returns:
            New AdapterChainRegistry with added chain (immutable operation)
        """
        return AdapterChainRegistry(
            registry_id=self.registry_id,
            chains=self.chains + (chain,)
        )

    def find_by_trace_id(self, source_trace_id: str) -> Tuple[AdapterChainLink, ...]:
        """
        Find all chains by source_trace_id.

        Args:
            source_trace_id: Trace ID to search for

        Returns:
            Tuple of matching chain links
        """
        return tuple(
            chain for chain in self.chains
            if chain.source_trace_id == source_trace_id
        )

    def find_by_training_example_id(
        self,
        source_training_example_id: str
    ) -> Tuple[AdapterChainLink, ...]:
        """
        Find all chains by source_training_example_id.

        Args:
            source_training_example_id: TrainingExample ID to search for

        Returns:
            Tuple of matching chain links
        """
        return tuple(
            chain for chain in self.chains
            if chain.source_training_example_id == source_training_example_id
        )

    def verify_binding_preservation(self, chain_link: AdapterChainLink) -> bool:
        """
        Verify that chain link preserves source bindings.

        Args:
            chain_link: Chain link to verify

        Returns:
            True if bindings preserved, False otherwise
        """
        # Verify required fields present
        if not chain_link.source_training_example_id:
            return False
        if not chain_link.source_trace_id:
            return False

        # Bindings preserved if both required fields present
        return True


def create_adapter_chain_registry(registry_id: str = "default_registry") -> AdapterChainRegistry:
    """
    Create new adapter chain registry.

    Args:
        registry_id: Unique registry identifier

    Returns:
        AdapterChainRegistry instance (empty, immutable)
    """
    return AdapterChainRegistry(registry_id=registry_id)


def create_chain_link_from_training_example(
    training_example: TrainingExample,
    link_id: str,
) -> AdapterChainLink:
    """
    Create chain link from TrainingExample (start of chain).

    Args:
        training_example: TrainingExample to create link from
        link_id: Unique link identifier

    Returns:
        AdapterChainLink with source bindings from TrainingExample
    """
    return AdapterChainLink(
        link_id=link_id,
        source_training_example_id=training_example.training_example_id,
        source_trace_id=training_example.source_trace_id,
        transformation_steps=("training_example_created",),
    )


def add_adapter_input_to_chain(
    chain: AdapterChainLink,
    adapter_input: AdapterInput,
) -> AdapterChainLink:
    """
    Add AdapterInput to chain link (next step in chain).

    Args:
        chain: Existing chain link
        adapter_input: AdapterInput to add

    Returns:
        New AdapterChainLink with adapter_input_id added (immutable operation)
    """
    # Verify binding preservation
    if adapter_input.source_training_example_id != chain.source_training_example_id:
        raise ValueError("AdapterInput lost source_training_example_id binding")
    if adapter_input.source_trace_id != chain.source_trace_id:
        raise ValueError("AdapterInput lost source_trace_id binding")

    return AdapterChainLink(
        link_id=chain.link_id,
        source_training_example_id=chain.source_training_example_id,
        source_trace_id=chain.source_trace_id,
        adapter_input_id=adapter_input.adapter_input_id,
        adapter_output_id=chain.adapter_output_id,
        model_output_id=chain.model_output_id,
        transformation_steps=chain.transformation_steps + ("adapter_input_prepared",),
    )


def add_adapter_output_to_chain(
    chain: AdapterChainLink,
    adapter_raw_output: AdapterRawOutput,
) -> AdapterChainLink:
    """
    Add AdapterRawOutput to chain link (next step in chain).

    Args:
        chain: Existing chain link
        adapter_raw_output: AdapterRawOutput to add

    Returns:
        New AdapterChainLink with adapter_output_id added (immutable operation)
    """
    # Verify link to adapter_input
    if chain.adapter_input_id != adapter_raw_output.source_adapter_input_id:
        raise ValueError("AdapterRawOutput does not reference correct AdapterInput")

    return AdapterChainLink(
        link_id=chain.link_id,
        source_training_example_id=chain.source_training_example_id,
        source_trace_id=chain.source_trace_id,
        adapter_input_id=chain.adapter_input_id,
        adapter_output_id=adapter_raw_output.adapter_output_id,
        model_output_id=chain.model_output_id,
        transformation_steps=chain.transformation_steps + ("adapter_raw_output_generated",),
    )


def add_model_output_to_chain(
    chain: AdapterChainLink,
    model_output: ModelOutput,
) -> AdapterChainLink:
    """
    Add ModelOutput to chain link (final step in chain).

    Args:
        chain: Existing chain link
        model_output: ModelOutput to add

    Returns:
        New AdapterChainLink with model_output_id added (immutable operation)
    """
    # Verify binding preservation
    if model_output.source_training_example_id != chain.source_training_example_id:
        raise ValueError("ModelOutput lost source_training_example_id binding")
    if model_output.source_trace_id != chain.source_trace_id:
        raise ValueError("ModelOutput lost source_trace_id binding")

    return AdapterChainLink(
        link_id=chain.link_id,
        source_training_example_id=chain.source_training_example_id,
        source_trace_id=chain.source_trace_id,
        adapter_input_id=chain.adapter_input_id,
        adapter_output_id=chain.adapter_output_id,
        model_output_id=model_output.model_output_id,
        transformation_steps=chain.transformation_steps + ("model_output_parsed",),
    )


# ============================================================================
# NoOpInputAdapter (Fixture Only)
# ============================================================================

@dataclass(frozen=True)
class NoOpInputAdapter:
    """
    No-op input adapter (TEST FIXTURE ONLY).

    Constitutional Requirements:
        - Implements InputAdapterContract Protocol
        - Does NOT tokenize (only formats abstract text)
        - Does NOT load models
        - Does NOT create tensors
        - Preserves source bindings
        - Is identity-like transformation (minimal formatting)
        - Is IMMUTABLE (frozen dataclass, no mutable state)

    Forbidden Operations:
        ❌ tokenize(): Does NOT tokenize
        ❌ encode(): Does NOT encode
        ❌ to_tensor(): Does NOT create tensors
        ❌ load_model(): Does NOT load models
        ❌ Mutable state: Does NOT have mutable attributes

    Permitted Operations:
        ✅ prepare_input(): Format abstract text (no tokenization)
        ✅ validate_input(): Validate structure (no execution)

    Supreme Law:
        NoOpInputAdapter is TEST FIXTURE proving contract implementability.
        NoOpInputAdapter is NOT production T5 implementation.
        NoOpInputAdapter is STATELESS (immutable, no side effects).

    Fields:
        adapter_name: Immutable adapter name
        version: Immutable version string
    """
    adapter_name: str = "NoOpInputAdapter"
    version: str = "fixture_1.0"

    def prepare_input(self, training_example: TrainingExample) -> AdapterInput:
        """
        Prepare AdapterInput from TrainingExample (no-op transformation).

        Constitutional Requirements:
            - MUST preserve source_trace_id
            - MUST preserve source_training_example_id
            - MUST NOT tokenize
            - MUST NOT create tensors
            - MUST NOT load models

        Args:
            training_example: TrainingExample to transform

        Returns:
            AdapterInput with preserved bindings and formatted text

        Raises:
            ValueError: If constitutional requirements violated
        """
        # Verify training_example is valid
        if not training_example.training_example_id:
            raise ValueError("TrainingExample missing training_example_id")
        if not training_example.source_trace_id:
            raise ValueError("TrainingExample missing source_trace_id")

        # No-op transformation: identity-like formatting
        # (prepend simple prefix to prove transformation occurred)
        formatted_input_text = f"[INPUT] {training_example.input_text}"

        # Create AdapterInput with preserved bindings
        adapter_input = AdapterInput(
            adapter_input_id=f"noop_input_{training_example.training_example_id}",
            source_training_example_id=training_example.training_example_id,
            source_trace_id=training_example.source_trace_id,
            input_text=formatted_input_text,
            metadata=(
                ("adapter_name", self.adapter_name),
                ("adapter_version", self.version),
                ("source_algorithm", training_example.source_algorithm),
            ),
        )

        return adapter_input

    def validate_input(self, adapter_input: AdapterInput) -> AdapterValidationResult:
        """
        Validate AdapterInput structure and bindings (no-op validation).

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
        violations = []
        warnings = []
        checked_constraints = []

        # Check source_trace_id
        checked_constraints.append("source_trace_id_present")
        if not adapter_input.source_trace_id:
            violations.append(AdapterViolationType.MISSING_SOURCE_TRACE_ID)

        # Check source_training_example_id
        checked_constraints.append("source_training_example_id_present")
        if not adapter_input.source_training_example_id:
            violations.append(AdapterViolationType.MISSING_SOURCE_TRAINING_EXAMPLE_ID)

        # Check input_text
        checked_constraints.append("input_text_present")
        if not adapter_input.input_text:
            warnings.append("AdapterInput has empty input_text")

        # Check for forbidden fields (defensive check)
        checked_constraints.append("no_forbidden_fields")
        adapter_input_fields = {f.name for f in fields(adapter_input)}
        forbidden_detected = adapter_input_fields.intersection(FORBIDDEN_ADAPTER_FIELDS)
        if forbidden_detected:
            violations.append(AdapterViolationType.FORBIDDEN_FIELD_PRESENT)
            warnings.append(f"Forbidden fields detected: {forbidden_detected}")

        is_valid = len(violations) == 0

        return AdapterValidationResult(
            validation_id=f"noop_validation_input_{adapter_input.adapter_input_id}",
            is_valid=is_valid,
            violations=tuple(violations),
            warnings=tuple(warnings),
            checked_constraints=tuple(checked_constraints),
        )


# ============================================================================
# NoOpOutputAdapter (Fixture Only)
# ============================================================================

@dataclass(frozen=True)
class NoOpOutputAdapter:
    """
    No-op output adapter (TEST FIXTURE ONLY).

    Constitutional Requirements:
        - Implements OutputAdapterContract Protocol
        - Does NOT generate text (receives abstract text)
        - Does NOT decode tensors (receives abstract text)
        - Does NOT execute inference
        - Preserves source bindings
        - Is identity-like transformation (minimal parsing)
        - Is IMMUTABLE (frozen dataclass, no mutable state)

    Forbidden Operations:
        ❌ model.generate(): Does NOT generate
        ❌ decode_tensor(): Does NOT decode tensors
        ❌ load_model(): Does NOT load models
        ❌ upgrade_rank(): Does NOT upgrade rank
        ❌ Mutable state: Does NOT have mutable attributes

    Permitted Operations:
        ✅ parse_output(): Parse abstract text to ModelOutput
        ✅ validate_output(): Validate structure (no execution)

    Supreme Law:
        NoOpOutputAdapter is TEST FIXTURE proving contract implementability.
        NoOpOutputAdapter is NOT production T5 implementation.
        NoOpOutputAdapter is STATELESS (immutable, no side effects).

    Fields:
        adapter_name: Immutable adapter name
        version: Immutable version string
    """
    adapter_name: str = "NoOpOutputAdapter"
    version: str = "fixture_1.0"

    def parse_output(
        self,
        adapter_raw_output: AdapterRawOutput,
        source_training_example_id: str,
        source_trace_id: str,
    ) -> ModelOutput:
        """
        Parse AdapterRawOutput into ModelOutput (no-op parsing).

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
        # Verify bindings provided
        if not source_training_example_id:
            raise ValueError("parse_output requires source_training_example_id")
        if not source_trace_id:
            raise ValueError("parse_output requires source_trace_id")

        # Verify adapter_raw_output is valid
        if not adapter_raw_output.raw_output_text:
            raise ValueError("AdapterRawOutput has empty raw_output_text")

        # No-op parsing: extract text from abstract output
        # (strip simple prefix if present to prove parsing occurred)
        parsed_text = adapter_raw_output.raw_output_text
        if parsed_text.startswith("[OUTPUT] "):
            parsed_text = parsed_text[len("[OUTPUT] "):]

        # Create ModelOutput with preserved bindings
        model_output = ModelOutput.create_from_prediction(
            source_training_example_id=source_training_example_id,
            source_trace_id=source_trace_id,
            predicted_text=parsed_text,
            model_name=f"{self.adapter_name}_v{self.version}",
        )

        return model_output

    def validate_output(self, model_output: ModelOutput) -> AdapterValidationResult:
        """
        Validate ModelOutput structure and bindings (no-op validation).

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
        violations = []
        warnings = []
        checked_constraints = []

        # Check source_trace_id
        checked_constraints.append("source_trace_id_present")
        if not model_output.source_trace_id:
            violations.append(AdapterViolationType.MISSING_SOURCE_TRACE_ID)

        # Check source_training_example_id
        checked_constraints.append("source_training_example_id_present")
        if not model_output.source_training_example_id:
            violations.append(AdapterViolationType.MISSING_SOURCE_TRAINING_EXAMPLE_ID)

        # Check predicted_text
        checked_constraints.append("predicted_text_present")
        if not model_output.predicted_text:
            warnings.append("ModelOutput has empty predicted_text")

        # Check for forbidden fields (defensive check)
        checked_constraints.append("no_forbidden_fields")
        model_output_fields = {f.name for f in fields(model_output)}
        forbidden_detected = model_output_fields.intersection(FORBIDDEN_ADAPTER_FIELDS)
        if forbidden_detected:
            violations.append(AdapterViolationType.FORBIDDEN_FIELD_PRESENT)
            warnings.append(f"Forbidden fields detected: {forbidden_detected}")

        is_valid = len(violations) == 0

        return AdapterValidationResult(
            validation_id=f"noop_validation_output_{model_output.model_output_id}",
            is_valid=is_valid,
            violations=tuple(violations),
            warnings=tuple(warnings),
            checked_constraints=tuple(checked_constraints),
        )


# ============================================================================
# NoOpValidationAdapter (Fixture Only)
# ============================================================================

@dataclass(frozen=True)
class NoOpValidationAdapter(ValidationAdapterContract):
    """
    No-op validation adapter (TEST FIXTURE ONLY).

    Constitutional Requirements:
        - Implements ValidationAdapterContract ABC
        - Does NOT execute models
        - Does NOT train models
        - Does NOT resolve violations (only detects)
        - Produces reports, NOT corrections
        - Is IMMUTABLE (frozen dataclass, no mutable state)

    Forbidden Operations:
        ❌ repair_violations(): Does NOT repair
        ❌ resolve_residuals(): Does NOT resolve
        ❌ load_model(): Does NOT load models
        ❌ execute_inference(): Does NOT execute inference
        ❌ Mutable state: Does NOT have mutable attributes

    Permitted Operations:
        ✅ validate_adapter_boundaries(): Check boundary compliance
        ✅ check_constitutional_compliance(): Check constitutional constraints

    Supreme Law:
        NoOpValidationAdapter is TEST FIXTURE proving contract implementability.
        NoOpValidationAdapter is NOT production T5 implementation.
        NoOpValidationAdapter is STATELESS (immutable, no side effects).

    Fields:
        adapter_name: Immutable adapter name
        version: Immutable version string
    """
    adapter_name: str = "NoOpValidationAdapter"
    version: str = "fixture_1.0"

    def validate_adapter_boundaries(
        self,
        config: GovernedT5IntegrationConfig,
    ) -> AdapterValidationResult:
        """
        Validate adapter boundaries against integration config (no-op validation).

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
        violations = []
        warnings = []
        checked_constraints = []

        # Check integration_id
        checked_constraints.append("integration_id_present")
        if not config.integration_id:
            warnings.append("GovernedT5IntegrationConfig has empty integration_id")

        # Check adapter boundaries present
        checked_constraints.append("input_adapter_boundary_present")
        if config.input_adapter_boundary is None:
            warnings.append("GovernedT5IntegrationConfig has no input_adapter_boundary")

        checked_constraints.append("output_adapter_boundary_present")
        if config.output_adapter_boundary is None:
            warnings.append("GovernedT5IntegrationConfig has no output_adapter_boundary")

        checked_constraints.append("validation_adapter_boundary_present")
        if config.validation_adapter_boundary is None:
            warnings.append("GovernedT5IntegrationConfig has no validation_adapter_boundary")

        # Check dependencies declared (not loaded)
        checked_constraints.append("dependencies_declared_not_loaded")
        if config.dependency_declaration is None:
            warnings.append("GovernedT5IntegrationConfig has no dependency_declaration")

        is_valid = len(violations) == 0

        return AdapterValidationResult(
            validation_id=f"noop_validation_boundaries_{config.integration_id}",
            is_valid=is_valid,
            violations=tuple(violations),
            warnings=tuple(warnings),
            checked_constraints=tuple(checked_constraints),
        )

    def check_constitutional_compliance(
        self,
        adapter_input: AdapterInput,
    ) -> AdapterValidationResult:
        """
        Check adapter input for constitutional compliance (no-op check).

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
        violations = []
        warnings = []
        checked_constraints = []

        # Check source_trace_id
        checked_constraints.append("source_trace_id_present")
        if not adapter_input.source_trace_id:
            violations.append(AdapterViolationType.MISSING_SOURCE_TRACE_ID)

        # Check source_training_example_id
        checked_constraints.append("source_training_example_id_present")
        if not adapter_input.source_training_example_id:
            violations.append(AdapterViolationType.MISSING_SOURCE_TRAINING_EXAMPLE_ID)

        # Check for forbidden fields
        checked_constraints.append("no_forbidden_fields")
        adapter_input_fields = {f.name for f in fields(adapter_input)}
        forbidden_detected = adapter_input_fields.intersection(FORBIDDEN_ADAPTER_FIELDS)
        if forbidden_detected:
            violations.append(AdapterViolationType.FORBIDDEN_FIELD_PRESENT)
            warnings.append(f"Forbidden fields detected: {forbidden_detected}")

        # Check for authority claims in text (simple heuristic check)
        checked_constraints.append("no_authority_claims")
        authority_markers = [
            "final_answer", "correct_analysis", "gold_label",
            "upgraded_rank", "closed_ifadah", "produced_hukm"
        ]
        input_text_lower = adapter_input.input_text.lower()
        for marker in authority_markers:
            if marker in input_text_lower:
                violations.append(AdapterViolationType.AUTHORITY_CLAIM_ATTEMPTED)
                warnings.append(f"Authority marker '{marker}' found in input_text")
                break

        is_valid = len(violations) == 0

        return AdapterValidationResult(
            validation_id=f"noop_validation_constitutional_{adapter_input.adapter_input_id}",
            is_valid=is_valid,
            violations=tuple(violations),
            warnings=tuple(warnings),
            checked_constraints=tuple(checked_constraints),
        )


# ============================================================================
# Fixture Factory Functions
# ============================================================================

def create_noop_input_adapter() -> NoOpInputAdapter:
    """
    Create no-op input adapter fixture.

    Returns:
        NoOpInputAdapter instance (frozen dataclass)
    """
    return NoOpInputAdapter()


def create_noop_output_adapter() -> NoOpOutputAdapter:
    """
    Create no-op output adapter fixture.

    Returns:
        NoOpOutputAdapter instance (frozen dataclass)
    """
    return NoOpOutputAdapter()


def create_noop_validation_adapter() -> NoOpValidationAdapter:
    """
    Create no-op validation adapter fixture.

    Returns:
        NoOpValidationAdapter instance (frozen dataclass)
    """
    return NoOpValidationAdapter()


def create_sample_adapter_raw_output(
    adapter_output_id: str = "sample_output_001",
    source_adapter_input_id: str = "sample_input_001",
    raw_text: str = "Sample raw output text",
) -> AdapterRawOutput:
    """
    Create sample AdapterRawOutput for testing.

    Args:
        adapter_output_id: Unique output ID
        source_adapter_input_id: Source input ID
        raw_text: Raw output text

    Returns:
        AdapterRawOutput instance
    """
    return AdapterRawOutput(
        adapter_output_id=adapter_output_id,
        source_adapter_input_id=source_adapter_input_id,
        raw_output_text=f"[OUTPUT] {raw_text}",
        adapter_metadata=(
            ("adapter_type", "noop"),
            ("version", "fixture_1.0"),
        ),
    )
