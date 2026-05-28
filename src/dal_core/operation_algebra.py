"""
Operation Algebra Core (نواة جبر العمليات)

PR #133: Operation Algebra, CauseGeometry, and Trace Inverse Constitution

Constitutional Foundation:
    This module establishes the algebraic foundation for operations AFTER Slot Geometry (PR #132).
    It is NOT an execution layer but a specification that operation layers MUST obey.

Critical Laws:
    1. No slot algebra without operation algebra.
    2. No operation without declared before/after relation.
    3. No operation without CauseGeometry.
    4. No CauseGeometry without Bāb and Domain.
    5. No certain backward recovery without Trace.
    6. SurfaceInverse is hypothetical (never certain).
    7. TraceInverse is certain only when: injective OR trace carries preimage.
    8. If trace incomplete: candidates + residuals + lowered rank.
    9. No final meaning from operations.
    10. All outputs STOP before meaning.

Master Equation:
    Before + PriorInfo + Bāb + Domain + CauseGeometry + LicensedOperation
    = After + Invariant + Trace + Residual + Rank + STOP before meaning

Purpose:
    Complete the missing half of PR #132:
    - Slot Geometry defined WHAT transforms
    - Operation Algebra defines HOW transforms happen with cause/trace/audit

Reference:
    docs/OPERATION_ALGEBRA_CONSTITUTION.md

PR: #133
Created: 2026-05-28
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import (
    Any, Callable, FrozenSet, Mapping, Optional, Protocol, Tuple, Type
)
from types import MappingProxyType

from dal_core.foundation import Rank, ResidualSet
from dal_core.residuals import Residual


# ============================================================================
# Supporting Type Definitions
# ============================================================================


class TraceRequirement(Enum):
    """How complete must trace be for recovery."""
    NONE = auto()           # No trace needed (purely structural)
    MINIMAL = auto()        # Basic operation record
    COMPLETE = auto()       # Full preimage recovery info
    INJECTIVE = auto()      # Operation injective, minimal trace sufficient


class LicenseType(Enum):
    """What licenses this operation."""
    MORPHOLOGICAL_BAB = auto()      # باب صرفي
    PHONOLOGICAL_RULE = auto()      # قاعدة صوتية
    ORTHOGRAPHIC_RULE = auto()      # قاعدة كتابية
    STRUCTURAL_CONSTRAINT = auto()  # قيد بنيوي


class AuditStatus(Enum):
    """Result of backward audit."""
    VERIFIED_CERTAIN = auto()       # Certain recovery verified
    VERIFIED_CANDIDATE = auto()     # Candidate recovery verified
    FAILED_DOMAIN = auto()          # Not in domain
    FAILED_INVARIANT = auto()       # Invariant not preserved
    FAILED_TRACE = auto()           # Trace incomplete/invalid
    FAILED_MEANING_LEAK = auto()    # Meaning detected (constitutional violation)


# ============================================================================
# A. BeforeAfterRelation
# ============================================================================


@dataclass(frozen=True)
class BeforeAfterRelation:
    """
    Explicit declaration of before/after relation for operation.

    Constitutional Law:
        No implicit transformations.
        Every operation MUST declare what changes and what persists.

    Required for all operations.
    """
    operation_name: str
    before_type: Type
    after_type: Type
    identity_preservation: str  # How identity is preserved
    change_description: str  # What changes
    reversibility: bool  # Is operation reversible?
    trace_requirement: TraceRequirement  # What trace must capture

    def __post_init__(self):
        """Validate required fields."""
        if not self.operation_name:
            raise ValueError("BeforeAfterRelation requires operation_name")
        if not self.identity_preservation:
            raise ValueError("BeforeAfterRelation requires identity_preservation")
        if not self.change_description:
            raise ValueError("BeforeAfterRelation requires change_description")


# ============================================================================
# B. CauseGeometry
# ============================================================================


@dataclass(frozen=True)
class LicenseSpec:
    """License specification for operation."""
    license_type: LicenseType
    licensing_condition: str
    required_prior_info: FrozenSet[str]

    def __post_init__(self):
        """Validate required fields."""
        if not self.licensing_condition:
            raise ValueError("LicenseSpec requires licensing_condition")


@dataclass(frozen=True)
class CauseGeometry:
    """
    Complete geometric representation of operation causation.

    Constitutional Law:
        Every operation MUST have complete cause geometry.
        All four causes MUST be declared.
        Final cause MUST stop before meaning.

    Four Causes (الأسباب الأربعة):
        1. Material Cause: What undergoes transformation
        2. Formal Cause: Pattern/structure imposed
        3. Efficient Cause: Licensing condition
        4. Final Cause: Purpose (BEFORE meaning)
    """
    prior_info: FrozenSet[str]
    bāb: str  # باب - morphological door/gate
    domain: str
    material_cause: str  # العلة المادية
    formal_cause: str  # العلة الصورية
    efficient_cause: str  # العلة الفاعلية
    final_cause_before_meaning: str  # العلة الغائية (قبل المعنى)
    license: LicenseSpec
    invariant: str  # What must not change
    trace_requirement: TraceRequirement
    residual_handling: str
    rank_assignment: Rank
    stop_before_meaning: bool = True  # Always True

    def __post_init__(self):
        """
        Validate constitutional requirements.

        Raises:
            ValueError: If any required field missing or invalid.
        """
        # Law 4: No CauseGeometry without Bāb and Domain
        if not self.bāb:
            raise ValueError(
                "CauseGeometry requires bāb (morphological door). "
                "Violation of Operation Algebra Constitution Law #4."
            )
        if not self.domain:
            raise ValueError(
                "CauseGeometry requires domain declaration. "
                "Violation of Operation Algebra Constitution Law #4."
            )

        # Law 3: Complete cause geometry
        if not self.material_cause:
            raise ValueError("CauseGeometry requires material_cause (what transforms)")
        if not self.formal_cause:
            raise ValueError("CauseGeometry requires formal_cause (pattern imposed)")
        if not self.efficient_cause:
            raise ValueError("CauseGeometry requires efficient_cause (licensing)")
        if not self.final_cause_before_meaning:
            raise ValueError("CauseGeometry requires final_cause_before_meaning")

        # Law 8: Stop before meaning
        if not self.stop_before_meaning:
            raise ValueError(
                "CauseGeometry.stop_before_meaning MUST be True. "
                "Violation of Operation Algebra Constitution Law #8."
            )

        if not self.invariant:
            raise ValueError("CauseGeometry requires invariant declaration")


# ============================================================================
# C. OperationTrace
# ============================================================================


@dataclass(frozen=True)
class OperationTrace:
    """
    Trace of operation execution.

    Constitutional Law:
        Trace completeness determines recovery certainty.
        Complete trace enables certain recovery (if injective or carries preimage).
        Incomplete trace → candidates + residuals + lowered rank.

    Attributes:
        is_complete: Full preimage info available
        is_injective_operation: Operation preserves info naturally
        carries_preimage: Trace explicitly stores lost preimage (for non-injective ops)
    """
    operation_name: str
    before_identity: str
    after_identity: str
    preserved_invariant: str
    changed_components: Tuple[str, ...]
    trace_data: Mapping[str, Any]  # MappingProxyType for immutability
    is_complete: bool
    is_injective_operation: bool
    carries_preimage: bool  # For non-injective operations like deletion/assimilation
    residuals_at_operation: FrozenSet[Residual]
    rank_at_operation: Rank

    def __post_init__(self):
        """Ensure trace_data is immutable."""
        if not isinstance(self.trace_data, MappingProxyType):
            # Coerce to immutable
            object.__setattr__(
                self, 'trace_data',
                MappingProxyType(dict(self.trace_data))
            )

        if not self.operation_name:
            raise ValueError("OperationTrace requires operation_name")
        if not self.before_identity:
            raise ValueError("OperationTrace requires before_identity")
        if not self.after_identity:
            raise ValueError("OperationTrace requires after_identity")

    def can_recover_certainly(self) -> bool:
        """
        Check if trace enables certain recovery.

        Constitutional Law (Law #6):
            TraceInverse is certain within domain when EITHER:
            1. Operation is injective on that domain, OR
            2. Trace carries sufficient preserved preimage information.
        """
        return self.is_complete and (
            self.is_injective_operation or self.carries_preimage
        )


# ============================================================================
# D. Inversion Types
# ============================================================================


@dataclass(frozen=True)
class SurfaceInverse:
    """
    Surface-level inversion (hypothetical, probabilistic).

    Constitutional Law (Law #5):
        SurfaceInverse NEVER returns certainty.
        Always returns candidates with residuals.
        Maximum rank: STRONG_HYPOTHESIS.

    Use Case:
        Hypothetical reconstruction without trace.
        Example: "What could have produced this surface form?"
    """
    surface_after: Any
    recovered_candidates: Tuple[Any, ...]  # Multiple possibilities
    residuals: FrozenSet[Residual]
    rank: Rank  # Always ≤ STRONG_HYPOTHESIS
    certainty: bool = False  # Always False (constitutional invariant)

    def __post_init__(self):
        """
        Enforce constitutional constraints.

        Raises:
            ValueError: If certainty=True or rank > STRONG_HYPOTHESIS.
        """
        # Law 5: SurfaceInverse never certain
        if self.certainty:
            raise ValueError(
                "SurfaceInverse.certainty MUST be False. "
                "Surface inversion is always hypothetical (ظني). "
                "Violation of Operation Algebra Constitution Law #5."
            )

        # Law 5: Rank limit
        rank_order = [Rank.ZERO, Rank.CANDIDATE, Rank.HYPOTHESIS,
                      Rank.STRONG_HYPOTHESIS, Rank.CERTIFICATE]
        if self.rank in rank_order:
            rank_idx = rank_order.index(self.rank)
            strong_hyp_idx = rank_order.index(Rank.STRONG_HYPOTHESIS)
            if rank_idx > strong_hyp_idx:
                raise ValueError(
                    f"SurfaceInverse rank cannot exceed STRONG_HYPOTHESIS. "
                    f"Got: {self.rank}. "
                    f"Violation of Operation Algebra Constitution Law #5."
                )


@dataclass(frozen=True)
class TraceInverse:
    """
    Trace-based inversion (certain under conditions).

    Constitutional Law (Law #6, #7):
        TraceInverse is certain within declared domain when EITHER:
        1. Operation is injective on that domain, OR
        2. Trace carries sufficient preserved preimage information.

        If trace incomplete:
        → Return candidates with residuals and lowered rank (≤ HYPOTHESIS)

    Use Case:
        Verified backward audit with trace.
        Example: "Given trace, what was the before-state?"
    """
    after_state: Any
    trace: OperationTrace
    domain: str
    recovered_before: Optional[Any]  # Certain recovery (when is_certain=True)
    alternative_candidates: Tuple[Any, ...]  # Uncertain recovery
    residuals: FrozenSet[Residual]
    rank: Rank
    is_certain: bool  # True only when conditions met
    certainty_basis: Optional[str]  # "injective" or "trace_carries_preimage" or None

    def __post_init__(self):
        """
        Enforce constitutional constraints.

        Raises:
            ValueError: If certainty claimed without proper basis.
        """
        # Law 6: Certainty requires conditions
        if self.is_certain:
            if not self.trace.can_recover_certainly():
                raise ValueError(
                    "TraceInverse cannot claim certainty without complete trace. "
                    "Trace must be complete AND (injective OR carries_preimage). "
                    "Violation of Operation Algebra Constitution Law #6."
                )
            if not self.certainty_basis:
                raise ValueError(
                    "TraceInverse.is_certain=True requires certainty_basis. "
                    "Must be 'injective' or 'trace_carries_preimage'."
                )
            if not self.recovered_before:
                raise ValueError(
                    "TraceInverse.is_certain=True requires recovered_before value."
                )

        # Law 7: Incomplete trace → lowered rank
        if not self.trace.is_complete:
            rank_order = [Rank.ZERO, Rank.CANDIDATE, Rank.HYPOTHESIS,
                          Rank.STRONG_HYPOTHESIS, Rank.CERTIFICATE]
            if self.rank in rank_order:
                rank_idx = rank_order.index(self.rank)
                hypothesis_idx = rank_order.index(Rank.HYPOTHESIS)
                if rank_idx > hypothesis_idx:
                    raise ValueError(
                        f"Incomplete trace requires rank ≤ HYPOTHESIS. "
                        f"Got: {self.rank}. "
                        f"Violation of Operation Algebra Constitution Law #7."
                    )
            if len(self.residuals) == 0:
                raise ValueError(
                    "Incomplete trace MUST have residuals. "
                    "Violation of Operation Algebra Constitution Law #7."
                )


# ============================================================================
# E. Backward Audit
# ============================================================================


@dataclass(frozen=True)
class AuditResult:
    """Result of backward audit."""
    status: AuditStatus
    verified_invariant: bool
    verified_domain: bool
    verified_trace_complete: bool
    verified_no_meaning: bool
    violation_details: Tuple[str, ...]


@dataclass(frozen=True)
class BackwardAudit:
    """
    Validates backward recovery from after-state + trace.

    Constitutional Law (Law #9):
        BackwardAudit MUST verify:
        1. Trace completeness
        2. Invariant preservation
        3. Domain membership
        4. No meaning production (Law #8)

    Returns:
        AuditResult with verification status.
    """
    after_state: Any
    trace: OperationTrace
    attempted_recovery: Any
    audit_result: AuditResult
    residuals: FrozenSet[Residual]
    rank: Rank

    def __post_init__(self):
        """Validate audit result consistency."""
        if not self.audit_result:
            raise ValueError("BackwardAudit requires audit_result")

        # If status is VERIFIED_CERTAIN, all checks must pass
        if self.audit_result.status == AuditStatus.VERIFIED_CERTAIN:
            if not all([
                self.audit_result.verified_invariant,
                self.audit_result.verified_domain,
                self.audit_result.verified_trace_complete,
                self.audit_result.verified_no_meaning
            ]):
                raise ValueError(
                    "AuditStatus.VERIFIED_CERTAIN requires all verifications to pass."
                )


# ============================================================================
# F. Policies
# ============================================================================


@dataclass(frozen=True)
class InvariantPolicy:
    """
    What MUST NOT change during operation.

    Constitutional requirement for all operations.
    """
    preserved_identity: str
    preserved_features: FrozenSet[str]
    forbidden_changes: FrozenSet[str]
    violation_handling: str  # "block" or "residual"

    def __post_init__(self):
        """Validate policy."""
        if not self.preserved_identity:
            raise ValueError("InvariantPolicy requires preserved_identity")
        if self.violation_handling not in ("block", "residual"):
            raise ValueError(
                "InvariantPolicy.violation_handling must be 'block' or 'residual'"
            )


@dataclass(frozen=True)
class ResidualPolicy:
    """
    What remains unresolved after operation.

    Algebraic law:
        Res(output) ⊇ Res(input) - DischargedByProof(output)
    """
    inherited_residuals: FrozenSet[Residual]
    operation_residuals: FrozenSet[Residual]
    discharge_conditions: Mapping[str, str]  # MappingProxyType
    blocking_residuals: FrozenSet[Residual]

    def __post_init__(self):
        """Ensure discharge_conditions is immutable."""
        if not isinstance(self.discharge_conditions, MappingProxyType):
            object.__setattr__(
                self, 'discharge_conditions',
                MappingProxyType(dict(self.discharge_conditions))
            )


@dataclass(frozen=True)
class RankPolicy:
    """
    Epistemic rank assignment for operation output.

    Constitutional Law:
        Operations NEVER produce CERTIFICATE rank.
        Only certification layers can certify.
    """
    input_rank_requirement: Rank
    output_rank: Rank
    rank_lowering_conditions: Mapping[str, Rank]  # MappingProxyType
    certification_prohibited: bool = True  # Always True

    def __post_init__(self):
        """
        Enforce constitutional constraints.

        Raises:
            ValueError: If operation attempts certification.
        """
        if not self.certification_prohibited:
            raise ValueError(
                "RankPolicy.certification_prohibited MUST be True. "
                "Operations cannot certify."
            )

        if self.output_rank == Rank.CERTIFICATE:
            raise ValueError(
                "Operations MUST NOT produce CERTIFICATE rank. "
                "Only certification layers can certify."
            )

        # Ensure immutability
        if not isinstance(self.rank_lowering_conditions, MappingProxyType):
            object.__setattr__(
                self, 'rank_lowering_conditions',
                MappingProxyType(dict(self.rank_lowering_conditions))
            )


@dataclass(frozen=True)
class TracePolicy:
    """How trace is generated and used."""
    required_completeness: bool
    preserved_preimage_fields: FrozenSet[str]
    injective_operation: bool
    inverse_certainty_conditions: Tuple[str, ...]


# ============================================================================
# G. MeaningStopGate
# ============================================================================


@dataclass(frozen=True)
class MeaningStopGate:
    """
    Constitutional gate preventing meaning production.

    Constitutional Law (Law #8):
        Operations MUST NOT produce:
        - meaning, murad, haqiqa_majaz
        - semantic_identity, ifadah_identity, hukm_identity
        - final_meaning

    Usage:
        Applied to all operation outputs.
        Raises ValueError if meaning detected.
    """
    forbidden_fields: FrozenSet[str] = frozenset([
        "meaning", "murad", "haqiqa_majaz",
        "semantic_identity", "ifadah_identity",
        "hukm_identity", "final_meaning",
        "lexical_meaning", "contextual_meaning"
    ])

    def validate(self, output: Any) -> None:
        """
        Validate output does not contain forbidden meaning fields.

        Raises:
            ValueError: If output contains forbidden fields.
        """
        for field in self.forbidden_fields:
            if hasattr(output, field):
                raise ValueError(
                    f"Operation output MUST NOT contain '{field}'. "
                    f"Operations stop before meaning. "
                    f"Violation of Operation Algebra Constitution Law #8."
                )


# ============================================================================
# H. OperationSpec (Complete Specification)
# ============================================================================


@dataclass(frozen=True)
class OperationSpec:
    """
    Complete specification of a licensed operation.

    Constitutional Law (Law #1, #2, #3):
        Every operation MUST declare:
        1. Before/after relation (Law #2)
        2. Complete cause geometry (Law #3)
        3. Trace policy
        4. Invariant preservation
        5. Residual handling
        6. Rank assignment
        7. Meaning prohibition (Law #8)
        8. Next allowed operations

    This is the MASTER STRUCTURE for all operations.
    """
    name: str
    domain_before: str
    domain_after: str
    input_type: Type
    output_type: Type
    required_prior_info: FrozenSet[str]
    bāb: str  # باب - morphological door
    cause_geometry: CauseGeometry
    licensed_operation: Callable  # Actual transformation function
    declared_before_after_relation: BeforeAfterRelation
    preserved_invariant: str
    changed_component: str
    trace_policy: TracePolicy
    residual_policy: ResidualPolicy
    rank_policy: RankPolicy
    surface_inverse_policy: Optional[str]
    trace_inverse_policy: Optional[str]
    forbidden_outputs: FrozenSet[str]
    next_allowed_operations: FrozenSet[str]
    stop_before_meaning: bool = True  # Always True

    def __post_init__(self):
        """
        Enforce constitutional requirements.

        Raises:
            ValueError: If any constitutional law violated.
        """
        # Law 1: Complete specification
        if not self.name:
            raise ValueError("OperationSpec requires name")

        # Law 2: Before/after relation
        if not self.declared_before_after_relation:
            raise ValueError(
                "OperationSpec requires declared_before_after_relation. "
                "Violation of Operation Algebra Constitution Law #2."
            )

        # Law 3: Complete cause geometry
        if not self.cause_geometry:
            raise ValueError(
                "OperationSpec requires complete cause_geometry. "
                "Violation of Operation Algebra Constitution Law #3."
            )

        # Ensure bāb consistency
        if self.bāb != self.cause_geometry.bāb:
            raise ValueError(
                "OperationSpec.bāb must match CauseGeometry.bāb"
            )

        # Law 8: Meaning prohibition
        if not self.stop_before_meaning:
            raise ValueError(
                "OperationSpec.stop_before_meaning MUST be True. "
                "Violation of Operation Algebra Constitution Law #8."
            )

        # Forbidden outputs must include meaning-related fields
        required_forbidden = {
            "meaning", "ifadah", "hukm", "semantic_identity"
        }
        if not required_forbidden.issubset(self.forbidden_outputs):
            missing = required_forbidden - self.forbidden_outputs
            raise ValueError(
                f"OperationSpec.forbidden_outputs must include: {missing}. "
                f"Violation of Operation Algebra Constitution Law #8."
            )

        if not self.licensed_operation:
            raise ValueError("OperationSpec requires licensed_operation callable")


# ============================================================================
# I. Protocol for Operation Execution
# ============================================================================


class OperationProtocol(Protocol):
    """
    Protocol for operation execution.

    All operations must implement this protocol.
    """

    def apply(
        self,
        before_state: Any,
        prior_info: Mapping[str, Any]
    ) -> Tuple[Any, OperationTrace, ResidualSet, Rank]:
        """
        Apply operation to before-state.

        Returns:
            (after_state, trace, residuals, rank)

        Raises:
            ValueError: If meaning produced (Law #8)
        """
        ...

    def surface_inverse(
        self,
        after_state: Any
    ) -> SurfaceInverse:
        """
        Hypothetical surface inversion (never certain).

        Returns:
            SurfaceInverse with candidates
        """
        ...

    def trace_inverse(
        self,
        after_state: Any,
        trace: OperationTrace
    ) -> TraceInverse:
        """
        Trace-based inversion (certain under conditions).

        Returns:
            TraceInverse with recovery result
        """
        ...

    def backward_audit(
        self,
        after_state: Any,
        trace: OperationTrace,
        attempted_recovery: Any
    ) -> BackwardAudit:
        """
        Audit backward recovery.

        Returns:
            BackwardAudit with verification result
        """
        ...


# ============================================================================
# Export
# ============================================================================


__all__ = [
    # Enums
    "TraceRequirement",
    "LicenseType",
    "AuditStatus",
    # Core Structures
    "BeforeAfterRelation",
    "LicenseSpec",
    "CauseGeometry",
    "OperationTrace",
    "SurfaceInverse",
    "TraceInverse",
    "AuditResult",
    "BackwardAudit",
    # Policies
    "InvariantPolicy",
    "ResidualPolicy",
    "RankPolicy",
    "TracePolicy",
    # Gates
    "MeaningStopGate",
    # Master Structure
    "OperationSpec",
    # Protocol
    "OperationProtocol",
]
