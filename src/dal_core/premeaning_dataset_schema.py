"""
PreMeaning Dataset Schema for GARA-T5 (مخطط بيانات ما قبل المعنى)

PR #135: Add PreMeaning Dataset Schema for GARA-T5

Constitutional Purpose:
    Define dataset contracts for training GARA-T5 on ALGEBRAIC PRE-MEANING TRACES,
    NOT on final meanings, relations, ifādah, or hukm.

Critical Laws:
    1. Dataset target = algebraic_trace_output (NOT semantic_output)
    2. NO meaning, translation, syntax_role, relation_candidate, ifādah, hukm
    3. SurfaceInverse examples MUST forbid certainty
    4. TraceInverse certainty REQUIRES: injective OR carries_preimage
    5. All examples MUST have residuals and rank
    6. All examples MUST have stop_before_meaning = True
    7. Dataset uses existing Rank and Residual types

T5 Learning Target:
    classified input
    → licensed operation
    → cause geometry
    → trace
    → residual
    → rank
    → stop gate

    NOT:
    → meaning
    → relation
    → ifādah
    → hukm

Reference:
    - PR #133: Operation Algebra Constitution
    - docs/OPERATION_ALGEBRA_CONSTITUTION.md

PR: #135
Created: 2026-05-28
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import FrozenSet, Mapping, Optional, Tuple
from types import MappingProxyType

from dal_core.foundation import Rank
from dal_core.residuals import Residual, ResidualType, ResidualSeverity
from dal_core.operation_algebra import (
    CauseGeometry,
    OperationTrace,
    TraceRequirement,
    LicenseType,
    LicenseSpec,
)


# ============================================================================
# Constitutional Gates (Forbidden Outputs)
# ============================================================================


class ForbiddenOutput(Enum):
    """Outputs that are constitutionally FORBIDDEN in PreMeaning datasets."""
    MEANING = "meaning"
    SEMANTIC_PAYLOAD = "semantic_payload"
    TRANSLATION = "translation"
    SYNTAX_ROLE = "syntax_role"
    RELATION_CANDIDATE = "relation_candidate"
    IFADAH = "ifadah"
    HUKM = "hukm"
    TRUTH_JUDGMENT = "truth_judgment"


def validate_no_forbidden_outputs(**kwargs) -> None:
    """
    Constitutional validation: No forbidden semantic outputs.

    Raises:
        ValueError: If any forbidden output is present
    """
    for key in kwargs:
        try:
            ForbiddenOutput(key)
            raise ValueError(
                f"Constitutional Violation: {key} is FORBIDDEN in PreMeaning dataset. "
                f"Dataset target is algebraic_trace_output, NOT semantic_output."
            )
        except ValueError as e:
            if "Constitutional Violation" in str(e):
                raise
            # Not a forbidden field, continue


# ============================================================================
# A. CauseGeometry Dataset Schema
# ============================================================================


@dataclass(frozen=True)
class CauseGeometryDataset:
    """
    CauseGeometry in dataset format.

    Includes all 4 Aristotelian causes + domain governance.
    """
    # Domain & Prior
    prior_info: FrozenSet[str]
    bāb: str  # Morphological door
    domain: str

    # Four Causes
    material_cause: str  # What transforms
    formal_cause: str  # Pattern imposed
    efficient_cause: str  # Licensing condition
    final_cause_before_meaning: str  # Purpose (PRE-SEMANTIC)

    # Governance
    license_type: str  # From LicenseType enum
    license_condition: str
    invariant: str
    trace_requirement: str  # From TraceRequirement enum

    def __post_init__(self):
        """Validate all 4 causes present."""
        if not self.material_cause:
            raise ValueError("CauseGeometry requires material_cause")
        if not self.formal_cause:
            raise ValueError("CauseGeometry requires formal_cause")
        if not self.efficient_cause:
            raise ValueError("CauseGeometry requires efficient_cause")
        if not self.final_cause_before_meaning:
            raise ValueError("CauseGeometry requires final_cause_before_meaning")
        if not self.bāb:
            raise ValueError("CauseGeometry requires bāb")
        if not self.domain:
            raise ValueError("CauseGeometry requires domain")

        # Verify final cause is PRE-semantic
        forbidden_terms = ["meaning", "semantic", "ifadah", "hukm", "truth"]
        if any(term in self.final_cause_before_meaning.lower() for term in forbidden_terms):
            raise ValueError(
                f"final_cause_before_meaning contains forbidden semantic term: "
                f"{self.final_cause_before_meaning}"
            )


# ============================================================================
# B. PreMeaningTrainingExample (Base Schema)
# ============================================================================


@dataclass(frozen=True)
class PreMeaningTrainingExample:
    """
    Base training example for GARA-T5 PreMeaning dataset.

    Constitutional Law:
        Every example MUST:
        - Have unique ID
        - Declare input surface + classification
        - Include complete CauseGeometry
        - Track before/after states
        - Record invariant, trace, residuals, rank
        - Set stop_before_meaning = True
        - List forbidden_outputs explicitly

        Every example MUST NOT:
        - Contain meaning, translation, syntax_role
        - Contain relation_candidate, ifadah, hukm
        - Claim certainty without trace
        - Skip residuals or rank
    """
    # Identification
    example_id: str
    example_type: str  # "operation_trace", "surface_inverse", etc.

    # Input
    input_surface: str
    input_classification: str  # "root", "stem", "pattern", "mabni", etc.

    # Operation Specification
    operation_name: str
    operation_spec_reference: str  # Reference to OperationSpec

    # Cause Geometry (complete)
    cause_geometry: CauseGeometryDataset

    # States
    before_state: str
    after_state: str
    invariant: str

    # Trace (may be minimal or complete based on operation)
    trace: Mapping[str, str]

    # Governance
    residuals: FrozenSet[Tuple[str, str, str]]  # (type, severity, message) tuples
    rank: str  # Rank enum name

    # Constitutional Gates
    stop_before_meaning: bool  # MUST be True
    forbidden_outputs: FrozenSet[str]  # Explicit forbidden list

    def __post_init__(self):
        """Constitutional validation."""
        # Validate stop gate
        if not self.stop_before_meaning:
            raise ValueError(
                "Constitutional Violation: stop_before_meaning MUST be True. "
                "PreMeaning dataset cannot contain final meanings."
            )

        # Validate forbidden outputs list not empty
        if not self.forbidden_outputs:
            raise ValueError(
                "forbidden_outputs MUST list at least one forbidden output type"
            )

        # Validate no forbidden fields in trace
        forbidden_keys = {
            "meaning", "semantic", "translation", "syntax_role",
            "relation", "ifadah", "hukm", "truth"
        }
        for key in self.trace.keys():
            if any(forbidden in key.lower() for forbidden in forbidden_keys):
                raise ValueError(
                    f"Trace contains forbidden semantic key: {key}"
                )

        # Validate trace is mapping (immutable)
        if not isinstance(self.trace, (Mapping, MappingProxyType)):
            raise ValueError("trace must be Mapping (immutable)")


# ============================================================================
# C. OperationTraceTrainingExample
# ============================================================================


@dataclass(frozen=True)
class OperationTraceTrainingExample(PreMeaningTrainingExample):
    """
    Training example for operation with complete trace.

    Target Learning:
        Given: input + operation_spec + cause_geometry
        Predict: after_state + trace + residuals + rank

    Constitutional Law:
        - Trace MUST be complete for this example type
        - is_injective_operation OR carries_preimage declared
        - Changed components explicitly listed
    """
    # Additional trace metadata
    is_injective_operation: bool
    carries_preimage: bool  # For non-injective (إدغام, حذف, إعلال, إبدال)
    changed_components: FrozenSet[str]

    def __post_init__(self):
        """Validate operation trace requirements."""
        super().__post_init__()

        # Non-injective operations SHOULD carry preimage for certain recovery
        if not self.is_injective_operation and not self.carries_preimage:
            # This is allowed but signals hypothetical recovery only
            if "hypothetical" not in self.rank.lower():
                raise ValueError(
                    "Non-injective operation without preimage trace "
                    "MUST have hypothetical rank"
                )


# ============================================================================
# D. SurfaceInverseTrainingExample
# ============================================================================


@dataclass(frozen=True)
class SurfaceInverseTrainingExample(PreMeaningTrainingExample):
    """
    Training example for surface-only inversion (HYPOTHETICAL).

    Target Learning:
        Given: surface_after
        Predict: multiple_candidates + residuals + rank
        Certainty: ALWAYS False

    Constitutional Law:
        - SurfaceInverse NEVER returns certainty
        - rank ≤ STRONG_HYPOTHESIS (never CERTIFICATE)
        - MUST have multiple candidates (ambiguity)
        - MUST have residuals
    """
    # Surface inversion output
    recovered_candidates: Tuple[str, ...]  # Multiple possibilities
    certainty: bool  # MUST be False

    def __post_init__(self):
        """Validate surface inverse constraints."""
        super().__post_init__()

        # Law 5: SurfaceInverse forbids certainty
        if self.certainty:
            raise ValueError(
                "Constitutional Violation: SurfaceInverse CANNOT be certain. "
                "Use TraceInverse for certain recovery."
            )

        # Rank ceiling
        forbidden_ranks = {"CERTIFICATE", "CERT"}
        if any(fr in self.rank.upper() for fr in forbidden_ranks):
            raise ValueError(
                f"Constitutional Violation: SurfaceInverse rank={self.rank} "
                f"exceeds ceiling (max=STRONG_HYPOTHESIS)"
            )

        # Must have multiple candidates (ambiguity)
        if len(self.recovered_candidates) < 2:
            raise ValueError(
                "SurfaceInverse MUST have multiple candidates (ambiguity). "
                f"Got {len(self.recovered_candidates)} candidate(s)."
            )

        # Must have residuals
        if not self.residuals:
            raise ValueError(
                "SurfaceInverse MUST have residuals documenting ambiguity"
            )


# ============================================================================
# E. TraceInverseTrainingExample
# ============================================================================


@dataclass(frozen=True)
class TraceInverseTrainingExample(PreMeaningTrainingExample):
    """
    Training example for trace-based inversion (CONDITIONALLY CERTAIN).

    Target Learning:
        Given: after_state + trace + domain
        Predict: recovered_before OR alternative_candidates
        Certainty: True ONLY when conditions met

    Constitutional Law (Law 6):
        TraceInverse certain ONLY when:
        1. Trace complete
        2. Domain declared
        3. Invariant preserved
        4. No blocking residuals
        5. Either is_injective_operation OR carries_preimage

    Otherwise: hypothetical candidates + lowered rank
    """
    # Trace inversion output
    recovered_before: Optional[str]  # Certain recovery
    alternative_candidates: Tuple[str, ...]  # Uncertain recovery
    is_certain: bool
    certainty_basis: Optional[str]  # "injective" or "trace_carries_preimage"

    # Trace completeness metadata
    trace_is_complete: bool
    domain_declared: bool
    invariant_preserved: bool
    has_blocking_residuals: bool
    is_injective_operation: bool
    carries_preimage: bool

    def __post_init__(self):
        """Validate trace inverse certainty conditions."""
        super().__post_init__()

        # Law 6: Certainty requires ALL conditions
        if self.is_certain:
            if not self.trace_is_complete:
                raise ValueError(
                    "TraceInverse cannot claim certainty without complete trace"
                )
            if not self.domain_declared:
                raise ValueError(
                    "TraceInverse cannot claim certainty without declared domain"
                )
            if not self.invariant_preserved:
                raise ValueError(
                    "TraceInverse cannot claim certainty without preserved invariant"
                )
            if self.has_blocking_residuals:
                raise ValueError(
                    "TraceInverse cannot claim certainty with blocking residuals"
                )
            if not (self.is_injective_operation or self.carries_preimage):
                raise ValueError(
                    "TraceInverse cannot claim certainty without: "
                    "is_injective_operation OR carries_preimage"
                )
            if not self.certainty_basis:
                raise ValueError(
                    "TraceInverse certainty MUST declare basis: "
                    "'injective' or 'trace_carries_preimage'"
                )
            if self.certainty_basis not in {"injective", "trace_carries_preimage"}:
                raise ValueError(
                    f"Invalid certainty_basis: {self.certainty_basis}. "
                    f"Must be 'injective' or 'trace_carries_preimage'"
                )

        # If certain, recovered_before MUST be set
        if self.is_certain and not self.recovered_before:
            raise ValueError(
                "TraceInverse with is_certain=True MUST have recovered_before"
            )

        # If uncertain, alternative_candidates MUST be set
        if not self.is_certain and not self.alternative_candidates:
            raise ValueError(
                "TraceInverse with is_certain=False MUST have alternative_candidates"
            )


# ============================================================================
# F. StopGateTrainingExample
# ============================================================================


@dataclass(frozen=True)
class StopGateTrainingExample(PreMeaningTrainingExample):
    """
    Training example demonstrating STOP before meaning.

    Target Learning:
        Given: input containing ONLY:
            - pattern signified
            - root/stem signified
            - operator potential
            - reference potential
            - relation readiness
            - trace only
        Predict: STOP_BEFORE_MEANING (not final meaning)

    Constitutional Law:
        When input lacks semantic closure conditions,
        output MUST be STOP signal, NOT meaning/ifadah/hukm.
    """
    # Input components (pre-semantic)
    has_pattern_signified: bool
    has_root_stem_signified: bool
    has_operator_potential: bool
    has_reference_potential: bool
    has_relation_readiness: bool
    has_trace_only: bool

    # Semantic closure conditions (all False for stop gate)
    has_compositional_relation: bool  # MUST be False
    has_pragmatic_closure: bool  # MUST be False
    has_evidence_for_truth: bool  # MUST be False

    # Expected output
    expected_output: str  # "STOP_BEFORE_MEANING"

    def __post_init__(self):
        """Validate stop gate conditions."""
        super().__post_init__()

        # Law 8: MeaningStopGate enforcement
        if self.has_compositional_relation:
            raise ValueError(
                "StopGateExample MUST NOT have compositional_relation. "
                "This example demonstrates pre-compositional stage."
            )
        if self.has_pragmatic_closure:
            raise ValueError(
                "StopGateExample MUST NOT have pragmatic_closure (ifadah)"
            )
        if self.has_evidence_for_truth:
            raise ValueError(
                "StopGateExample MUST NOT have evidence_for_truth (hukm)"
            )

        # Expected output MUST be stop signal
        if self.expected_output != "STOP_BEFORE_MEANING":
            raise ValueError(
                f"StopGateExample expected_output MUST be 'STOP_BEFORE_MEANING'. "
                f"Got: {self.expected_output}"
            )


# ============================================================================
# G. ResidualRankTrainingExample
# ============================================================================


@dataclass(frozen=True)
class ResidualRankTrainingExample(PreMeaningTrainingExample):
    """
    Training example for residual tracking and rank assignment.

    Target Learning:
        Given: operation + trace completeness + blocking conditions
        Predict: residuals + appropriate rank

    Constitutional Law (Law 7):
        Incomplete trace → candidates + residuals + lowered rank

    Rank Policy:
        - Operations cannot produce CERTIFICATE (only certification layers)
        - Incomplete trace forces rank ≤ HYPOTHESIS
        - Blocking residuals force rank = ZERO (or minimal)
    """
    # Trace completeness
    trace_completeness: str  # "complete", "incomplete", "missing"

    # Residual metadata
    has_blocking_residuals: bool
    has_warning_residuals: bool
    residual_count: int

    # Rank assignment
    rank_justification: str  # Why this rank was assigned

    def __post_init__(self):
        """Validate residual/rank policy."""
        super().__post_init__()

        # Must have residuals
        if self.residual_count != len(self.residuals):
            raise ValueError(
                f"residual_count={self.residual_count} but "
                f"len(residuals)={len(self.residuals)}"
            )

        # Blocking residuals MUST lower rank
        if self.has_blocking_residuals:
            forbidden_ranks = {"CERTIFICATE", "CERT", "STRONG"}
            if any(fr in self.rank.upper() for fr in forbidden_ranks):
                raise ValueError(
                    f"Blocking residuals present but rank={self.rank} is too high"
                )

        # Incomplete trace MUST have residuals and lowered rank
        if self.trace_completeness == "incomplete":
            if not self.residuals:
                raise ValueError(
                    "Incomplete trace MUST generate residuals"
                )
            if "CERTIFICATE" in self.rank.upper():
                raise ValueError(
                    "Incomplete trace cannot have CERTIFICATE rank"
                )


# ============================================================================
# H. Dataset Validation Utilities
# ============================================================================


def validate_premeaning_example(example: PreMeaningTrainingExample) -> None:
    """
    Validate any PreMeaning training example against constitutional laws.

    Checks:
        1. stop_before_meaning = True
        2. forbidden_outputs declared
        3. No forbidden semantic fields
        4. Has residuals and rank
        5. CauseGeometry complete
    """
    if not example.stop_before_meaning:
        raise ValueError(
            f"Example {example.example_id}: stop_before_meaning MUST be True"
        )

    if not example.forbidden_outputs:
        raise ValueError(
            f"Example {example.example_id}: forbidden_outputs cannot be empty"
        )

    if not example.residuals:
        raise ValueError(
            f"Example {example.example_id}: residuals cannot be empty"
        )

    if not example.rank:
        raise ValueError(
            f"Example {example.example_id}: rank cannot be empty"
        )

    # CauseGeometry completeness already validated in __post_init__
    # Additional checks can be added here


def make_sample_surface_inverse_example() -> SurfaceInverseTrainingExample:
    """
    Create a sample SurfaceInverse example for testing.

    Example: كَتَبَ surface → multiple root candidates
    """
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["arabic_text", "vocalized"]),
        bāb="تحليل_سطحي",
        domain="morphology",
        material_cause="surface form كَتَبَ",
        formal_cause="trilateral root pattern",
        efficient_cause="harakat pattern matches فَعَلَ",
        final_cause_before_meaning="identify root candidates",
        license_type="MORPHOLOGICAL_BAB",
        license_condition="surface pattern compatible",
        invariant="consonantal skeleton",
        trace_requirement="MINIMAL"
    )

    return SurfaceInverseTrainingExample(
        example_id="surf_inv_001",
        example_type="surface_inverse",
        input_surface="كَتَبَ",
        input_classification="vocalized_surface",
        operation_name="surface_root_extraction",
        operation_spec_reference="surface_inverse_spec",
        cause_geometry=cause_geo,
        before_state="",
        after_state="كَتَبَ",
        invariant="consonants: ك ت ب",
        trace=MappingProxyType({"operation": "surface_only"}),
        residuals=frozenset([
            ("ROOT_UNRESOLVED", "WARNING", "Multiple root candidates"),
            ("WAZN_UNRESOLVED", "WARNING", "Pattern ambiguous")
        ]),
        rank="HYPOTHESIS",
        stop_before_meaning=True,
        forbidden_outputs=frozenset([
            "meaning", "translation", "syntax_role",
            "relation_candidate", "ifadah", "hukm"
        ]),
        recovered_candidates=("ك ت ب", "ك ت ب + فَعَلَ", "ك ت ب + كِتَاب"),
        certainty=False
    )


def make_sample_trace_inverse_example() -> TraceInverseTrainingExample:
    """
    Create a sample TraceInverse example (certain recovery).

    Example: إدغام assimilation (ن + ل → لّ) with preimage trace
    """
    cause_geo = CauseGeometryDataset(
        prior_info=frozenset(["phonology", "assimilation_context"]),
        bāb="إدغام",
        domain="phonology",
        material_cause="nun + lam sequence",
        formal_cause="gemination of lam",
        efficient_cause="identical articulation points",
        final_cause_before_meaning="phonological simplification",
        license_type="PHONOLOGICAL_RULE",
        license_condition="sun_letter_context",
        invariant="total mora count",
        trace_requirement="COMPLETE"
    )

    return TraceInverseTrainingExample(
        example_id="trace_inv_001",
        example_type="trace_inverse",
        input_surface="ال + لَيْل",
        input_classification="assimilated_form",
        operation_name="idgham_assimilation",
        operation_spec_reference="idgham_spec",
        cause_geometry=cause_geo,
        before_state="ن + ل",
        after_state="لّ",
        invariant="mora_count=2",
        trace=MappingProxyType({
            "deleted_consonant": "ن",
            "geminated_consonant": "ل",
            "operation": "assimilation"
        }),
        residuals=frozenset([
            ("TRACE_COMPLETE", "INFO", "Complete trace with preimage")
        ]),
        rank="STRONG_HYPOTHESIS",
        stop_before_meaning=True,
        forbidden_outputs=frozenset([
            "meaning", "translation", "syntax_role",
            "relation_candidate", "ifadah", "hukm"
        ]),
        recovered_before="ن + ل",
        alternative_candidates=(),
        is_certain=True,
        certainty_basis="trace_carries_preimage",
        trace_is_complete=True,
        domain_declared=True,
        invariant_preserved=True,
        has_blocking_residuals=False,
        is_injective_operation=False,
        carries_preimage=True
    )
