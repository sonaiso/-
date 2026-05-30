"""
Transition Proof Kernel (نواة برهان الانتقال)

Unified transition proof foundation for Arabic composition chain.

Constitutional Purpose:
    Unify transition proof language across all layers without replacing
    existing dal_algebra.py or fvafk/algebra/core.py.

    This is a KERNEL - a neutral common language that sits above both
    existing algebraic systems and provides unified proof structure.

Critical Principles:
    1. Origin/Branch paradigm (أصل/فرع)
    2. Effective description with shared cause (وصف فعّال/علة جامعة)
    3. Invalidating differences as blockers (فرق قادح)
    4. Identity preservation check (حفظ الهوية)
    5. Minimal completeness verification (حد أدنى مكتمل)
    6. Constitutional prohibition gates (لا معنى، لا إفادة، لا حكم)

Forbidden Outputs:
    ❌ meaning, semantic, madlul, murad
    ❌ ifadah, pragmatic_completion
    ❌ hukm, judgment
    ❌ case_effect (only case_sign_potential allowed)
    ❌ syntax_role (only role_candidate allowed)

Architecture Position:
    dal_algebra.py + fvafk/algebra/core.py
        → TransitionProofKernel (this module - unifying layer)
            → MufradAcceptanceEquation
            → RelationSlotToAnchorAdapter
            → RelationCandidateBuilder
            → FactorMarkEquation

Reference:
    PR #163: Harden TransitionProofKernel with fvafk.algebra.Result
    Builds on: dal_algebra.py, fvafk/algebra/core.py

Created: 2026-05-29
Updated: 2026-05-30 (PR #163: Connect to fvafk.algebra.Result)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Optional, TypeVar, Generic

# CRITICAL FIX (PR #163): Import fvafk.algebra types for typed Results
from fvafk.algebra.core import (
    Result,
    Rank,
    Evidence,
    Residual,
    Failure,
    Trace,
)

T = TypeVar("T")


# ============================================================================
# Transition Decision Enum
# ============================================================================

class TransitionDecision(Enum):
    """
    حكم الانتقال (Transition Decision)

    Three possible outcomes for any transition proof.
    """
    ACCEPTED = "accepted"
    """Transition fully accepted - all conditions satisfied"""

    REJECTED = "rejected"
    """Transition rejected - blocking conditions present"""

    DEFERRED = "deferred"
    """Transition deferred - missing non-blocking conditions"""


# ============================================================================
# Qiyas Proof Components
# ============================================================================

@dataclass(frozen=True)
class EffectiveDescription:
    """
    وصف فعّال (Effective Description)

    The operational description that justifies the transition.

    Constitutional Law:
        The effective description must be verifiable through evidence.
        It describes WHAT is preserved/transformed, not WHY semantically.

    Fields:
        description_id: Unique identifier
        description_type: Type classification (morphological/syntactic/compositional)
        evidence: Tuple of evidence references
    """
    description_id: str
    description_type: str
    evidence: Tuple[str, ...]


@dataclass(frozen=True)
class InvalidatingDifference:
    """
    فرق قادح (Invalidating Difference)

    A difference that blocks or warns about the transition.

    Constitutional Law:
        If blocks_transition=True, the transition MUST be REJECTED.
        If blocks_transition=False, it's a warning/residual.

    Fields:
        difference_id: Unique identifier
        message: Human-readable description of the difference
        blocks_transition: Whether this blocks the transition
        evidence: Supporting evidence for this difference
    """
    difference_id: str
    message: str
    blocks_transition: bool
    evidence: Tuple[str, ...]


@dataclass(frozen=True)
class QiyasProof:
    """
    برهان القياس (Qiyas Proof)

    Analogical proof structure: Origin → Branch via shared cause,
    checked for invalidating differences.

    Constitutional Law:
        A valid qiyas requires:
        1. Clear origin (أصل)
        2. Clear branch (فرع)
        3. Shared effective cause (علة جامعة)
        4. No blocking invalidating differences (لا فرق قادح)

    Fields:
        proof_id: Unique identifier
        origin_id: The origin/foundation being analogized from
        branch_id: The branch/derivative being established
        effective_description: The effective description linking them
        shared_cause: The shared cause justifying the analogy
        invalidating_differences: Tuple of differences (may block)
    """
    proof_id: str
    origin_id: str
    branch_id: str
    effective_description: EffectiveDescription
    shared_cause: str
    invalidating_differences: Tuple[InvalidatingDifference, ...]

    @property
    def has_blocking_difference(self) -> bool:
        """Check if any invalidating difference blocks the transition."""
        return any(d.blocks_transition for d in self.invalidating_differences)

    @property
    def accepted(self) -> bool:
        """Check if qiyas proof is accepted (all components present, no blockers)."""
        return bool(
            self.origin_id
            and self.branch_id
            and self.shared_cause
        ) and not self.has_blocking_difference


# ============================================================================
# Identity and Completeness Checks
# ============================================================================

@dataclass(frozen=True)
class IdentityNeutralCheck:
    """
    فحص حياد الهوية (Identity Neutral Check)

    Verifies that transition preserves input identities.

    Constitutional Law:
        All input identity IDs MUST appear in output identity IDs.
        Transitions may ADD identities but MUST NOT lose them.

    Fields:
        check_id: Unique identifier
        input_identity_ids: Identity IDs before transition
        output_identity_ids: Identity IDs after transition
        preserved: Whether all inputs are preserved in outputs
    """
    check_id: str
    input_identity_ids: Tuple[str, ...]
    output_identity_ids: Tuple[str, ...]
    preserved: bool

    def __post_init__(self):
        """Validate that preserved flag matches actual preservation."""
        missing = set(self.input_identity_ids) - set(self.output_identity_ids)
        if self.preserved and missing:
            raise ValueError(
                f"Identity neutral check claims preservation but lost: {missing}"
            )


@dataclass(frozen=True)
class MinimalCompletenessCheck:
    """
    فحص الحد الأدنى المكتمل (Minimal Completeness Check)

    Verifies minimum required conditions for target layer are satisfied.

    Constitutional Law:
        Each layer has minimum required conditions.
        If ALL required conditions satisfied → passed = True
        If ANY required condition missing → passed = False

    Fields:
        check_id: Unique identifier
        target_layer: Name of target layer
        required_conditions: All conditions required for target layer
        satisfied_conditions: Conditions that are currently satisfied
        missing_conditions: Conditions that are missing
        passed: Whether all required conditions are satisfied
    """
    check_id: str
    target_layer: str
    required_conditions: Tuple[str, ...]
    satisfied_conditions: Tuple[str, ...]
    missing_conditions: Tuple[str, ...]
    passed: bool

    def __post_init__(self):
        """Validate that passed flag matches actual condition satisfaction."""
        if self.passed and self.missing_conditions:
            raise ValueError(
                "Minimal completeness cannot pass with missing conditions"
            )


# ============================================================================
# Unified Transition Proof
# ============================================================================

@dataclass(frozen=True)
class TransitionProof:
    """
    برهان الانتقال (Transition Proof)

    Complete unified proof for any layer-to-layer transition.

    Constitutional Law:
        A transition is ACCEPTED if and only if:
        1. Qiyas proof accepted (no blocking differences)
        2. Identity preserved (all inputs in outputs)
        3. Minimal completeness passed (all required conditions)
        4. NO forbidden outputs (meaning/ifadah/hukm)

    Fields:
        proof_id: Unique identifier
        source_layer: Name of source layer
        target_layer: Name of target layer
        qiyas: Analogical proof structure
        identity_neutral: Identity preservation check
        minimal_completeness: Minimum conditions check
        preserved_trace_ids: Trace IDs preserved through transition
        residual_ids: Residual IDs carried forward
        rank: Epistemic rank (from fvafk.algebra.Rank, NOT upgraded by transition)
        produces_meaning: Whether transition produces meaning (FORBIDDEN)
        produces_ifadah: Whether transition produces ifadah (FORBIDDEN)
        produces_hukm: Whether transition produces hukm (FORBIDDEN)
    """
    proof_id: str
    source_layer: str
    target_layer: str

    qiyas: QiyasProof
    identity_neutral: IdentityNeutralCheck
    minimal_completeness: MinimalCompletenessCheck

    preserved_trace_ids: Tuple[str, ...]
    residual_ids: Tuple[str, ...]

    # CRITICAL FIX (PR #163): Use typed Rank, not string
    rank: Rank

    produces_meaning: bool = False
    produces_ifadah: bool = False
    produces_hukm: bool = False

    @property
    def decision(self) -> TransitionDecision:
        """
        Compute transition decision from proof components.

        Decision Logic:
            1. If produces_meaning/ifadah/hukm → REJECTED
            2. If qiyas has blocking difference → REJECTED
            3. If identity not preserved → REJECTED
            4. If minimal completeness not passed → DEFERRED
            5. If qiyas not accepted → DEFERRED
            6. Otherwise → ACCEPTED

        Returns:
            TransitionDecision enum value
        """
        # Constitutional prohibition gates (immediate rejection)
        if self.produces_meaning or self.produces_ifadah or self.produces_hukm:
            return TransitionDecision.REJECTED

        # Qiyas blocking check
        if self.qiyas.has_blocking_difference:
            return TransitionDecision.REJECTED

        # Identity preservation check
        if not self.identity_neutral.preserved:
            return TransitionDecision.REJECTED

        # Minimal completeness check (deferred if not complete)
        if not self.minimal_completeness.passed:
            return TransitionDecision.DEFERRED

        # Qiyas acceptance check (deferred if not accepted)
        if not self.qiyas.accepted:
            return TransitionDecision.DEFERRED

        # All checks passed
        return TransitionDecision.ACCEPTED

    def to_result(self, value: T, *, operation: str = "transition") -> Result[T]:
        """
        Convert TransitionProof to fvafk.algebra.Result[T].

        Constitutional Law:
            1. ACCEPTED → Result with LICENSED or CANDIDATE (depending on evidence)
            2. DEFERRED → Result with CANDIDATE or UNRESOLVED + residuals
            3. REJECTED → Result with REFUTED + failures

        Conversion Rules:
            - InvalidatingDifference(blocks_transition=True) → Failure(fatal=True)
            - InvalidatingDifference(blocks_transition=False) → Residual
            - QiyasProof.effective_description.evidence → Evidence items
            - rank preserved from TransitionProof.rank
            - If rank >= LICENSED and no Evidence → raises ValueError

        Args:
            value: The value to wrap in Result
            operation: Operation name for trace (defaults to "transition")

        Returns:
            Result[T] with proper rank, evidence, residuals, failures

        Raises:
            ValueError: If rank >= LICENSED but no evidence available

        Example:
            >>> proof = TransitionProof(..., rank=Rank.LICENSED)
            >>> result = proof.to_result(my_value, operation="mufrad_transition")
            >>> assert result.rank == Rank.LICENSED
        """
        decision = self.decision

        # Build evidence from effective description
        evidence_items = tuple(
            Evidence(
                kind="effective_description",
                source=ev_ref,
                detail=self.qiyas.effective_description.description_type,
                weight=1.0,
            )
            for ev_ref in self.qiyas.effective_description.evidence
        )

        # Build residuals from non-blocking differences and residual_ids
        residual_items = []

        # Add non-blocking invalidating differences as residuals
        for diff in self.qiyas.invalidating_differences:
            if not diff.blocks_transition:
                residual_items.append(
                    Residual(
                        kind="non_blocking_difference",
                        description=diff.message,
                    )
                )

        # Add minimal completeness missing conditions as residuals
        for missing in self.minimal_completeness.missing_conditions:
            residual_items.append(
                Residual(
                    kind="missing_condition",
                    description=f"Missing required condition: {missing}",
                )
            )

        # Add residual_ids as residuals
        for residual_id in self.residual_ids:
            residual_items.append(
                Residual(
                    kind="residual_id",
                    description=f"Residual from previous layer: {residual_id}",
                )
            )

        residuals = tuple(residual_items)

        # Build failures from blocking differences and constitutional violations
        failure_items = []

        # Add blocking invalidating differences as fatal failures
        for diff in self.qiyas.invalidating_differences:
            if diff.blocks_transition:
                failure_items.append(
                    Failure(
                        kind="blocking_difference",
                        description=diff.message,
                        fatal=True,
                    )
                )

        # Add constitutional prohibition failures
        if self.produces_meaning:
            failure_items.append(
                Failure(
                    kind="constitutional_prohibition",
                    description="Transition produces forbidden meaning (لا معنى)",
                    fatal=True,
                )
            )

        if self.produces_ifadah:
            failure_items.append(
                Failure(
                    kind="constitutional_prohibition",
                    description="Transition produces forbidden ifadah (لا إفادة)",
                    fatal=True,
                )
            )

        if self.produces_hukm:
            failure_items.append(
                Failure(
                    kind="constitutional_prohibition",
                    description="Transition produces forbidden hukm (لا حكم)",
                    fatal=True,
                )
            )

        # Add identity loss as fatal failure
        if not self.identity_neutral.preserved:
            failure_items.append(
                Failure(
                    kind="identity_loss",
                    description="Input identities not preserved in output",
                    fatal=True,
                )
            )

        failures = tuple(failure_items)

        # Build trace
        trace = Trace(
            operation=operation,
            source_span=(0, 0),  # To be filled by caller if needed
            parents=self.preserved_trace_ids,
            metadata={
                "proof_id": self.proof_id,
                "source_layer": self.source_layer,
                "target_layer": self.target_layer,
                "decision": decision.value,
            },
        )

        # Determine final rank based on decision
        if decision == TransitionDecision.REJECTED:
            # REJECTED → REFUTED (fatal failures present)
            final_rank = Rank.REFUTED
        elif decision == TransitionDecision.DEFERRED:
            # DEFERRED → CANDIDATE or UNRESOLVED
            # If we have evidence, use CANDIDATE
            # If no evidence, use UNRESOLVED
            if evidence_items:
                final_rank = Rank.CANDIDATE
            else:
                final_rank = Rank.UNRESOLVED
        else:  # ACCEPTED
            # ACCEPTED → use proof's rank, but validate
            # If rank >= LICENSED, evidence is required
            if self.rank in (Rank.LICENSED, Rank.CERTIFIED) and not evidence_items:
                raise ValueError(
                    f"TransitionProof has rank {self.rank.name} but no evidence. "
                    f"Cannot create Result with rank >= LICENSED without evidence. "
                    f"Effective description must provide evidence."
                )
            final_rank = self.rank

        # Construct Result
        result = Result(
            value=value,
            rank=final_rank,
            evidence=evidence_items,
            residuals=residuals,
            failures=failures,
            trace=trace,
        )

        return result
