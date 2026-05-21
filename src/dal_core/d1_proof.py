"""D1 Proof Object (ProofObject_D1).

Certification proof for syllable candidates.

A candidate is certified iff:
    ProofObject_D1.is_certified = True

Certification requires:
- All Corr_D1 checks pass
- No critical failures exist
- Trace is reversible (verified, not just claimed)
- Anti-promotion validated
- Rank vector computed

This enforces the law:
    High rank ≠ correctness
    Certification = formal proof, not statistical confidence
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

from dal_core.d1_correctness import Corr_D1_Result
from dal_core.d1_failures import D1FailureSet
from dal_core.d1_rank_policy import SyllableRankVector


@dataclass
class ProofObject_D1:
    """
    Certification proof for D1 candidate.

    Proves candidate passed all D1 correctness checks.

    This is NOT a rank or confidence score.
    This is a formal proof object.
    """
    candidate_id: str
    is_certified: bool
    corr_result: Corr_D1_Result
    failure_set: D1FailureSet
    rank_vector: SyllableRankVector
    certification_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate proof invariants."""
        # Critical invariant: is_certified must match corr_result
        if self.is_certified and not self.corr_result.is_correct:
            raise ValueError(
                "Proof claims certification but Corr_D1 failed. "
                "is_certified must be False when corr_result.is_correct is False."
            )

        # Critical invariant: is_certified must check for critical failures
        if self.is_certified and self.failure_set.has_critical_failure():
            raise ValueError(
                "Proof claims certification but critical failures exist. "
                "is_certified must be False when critical failures present."
            )

    def failed_checks(self) -> list:
        """Get list of failed Corr_D1 checks."""
        return self.corr_result.failed_checks()

    def critical_failures(self) -> list:
        """Get list of critical D1 failures."""
        return self.failure_set.critical_failures()

    def is_valid_for_promotion(self) -> bool:
        """Check if candidate can be promoted to D2.

        Promotion requires:
        - is_certified = True
        - No critical failures
        - Corr_D1 passed

        Returns:
            True if candidate may be promoted to D2
        """
        return (
            self.is_certified and
            not self.failure_set.has_critical_failure() and
            self.corr_result.is_correct
        )

    def summary(self) -> str:
        """Summary of proof status."""
        if self.is_certified:
            status = "✅ CERTIFIED"
        else:
            status = "❌ NOT CERTIFIED"

        corr_summary = self.corr_result.summary()
        failure_summary = self.failure_set.summary()

        return (
            f"{status}\n"
            f"  Corr_D1: {corr_summary}\n"
            f"  Failures: {failure_summary}\n"
            f"  Rank: {self.rank_vector.total_rank():.2f}\n"
            f"  Timestamp: {self.certification_timestamp}"
        )

    def __str__(self) -> str:
        """Human-readable proof representation."""
        cert_mark = "✅" if self.is_certified else "❌"
        return f"{cert_mark} ProofObject_D1({self.candidate_id}, certified={self.is_certified})"


# ============================================================================
# Proof Construction Functions
# ============================================================================


def create_proof(
    candidate_id: str,
    corr_result: Corr_D1_Result,
    failure_set: D1FailureSet,
    rank_vector: SyllableRankVector,
    metadata: Optional[Dict[str, Any]] = None
) -> ProofObject_D1:
    """Create proof object from validation results.

    Args:
        candidate_id: Candidate identifier
        corr_result: Corr_D1 validation result
        failure_set: D1 failures
        rank_vector: Rank vector
        metadata: Optional metadata

    Returns:
        ProofObject_D1

    The proof is certified iff:
    - corr_result.is_correct = True
    - No critical failures exist
    """
    is_certified = (
        corr_result.is_correct and
        not failure_set.has_critical_failure()
    )

    return ProofObject_D1(
        candidate_id=candidate_id,
        is_certified=is_certified,
        corr_result=corr_result,
        failure_set=failure_set,
        rank_vector=rank_vector,
        metadata=metadata or {}
    )


def create_uncertified_proof(
    candidate_id: str,
    reason: str,
    corr_result: Optional[Corr_D1_Result] = None,
    failure_set: Optional[D1FailureSet] = None,
    rank_vector: Optional[SyllableRankVector] = None
) -> ProofObject_D1:
    """Create uncertified proof with reason.

    Args:
        candidate_id: Candidate identifier
        reason: Reason for non-certification
        corr_result: Optional Corr_D1 result
        failure_set: Optional failure set
        rank_vector: Optional rank vector

    Returns:
        ProofObject_D1 with is_certified=False
    """
    from dal_core.d1_correctness import Corr_D1_Result
    from dal_core.d1_failures import D1FailureSet, make_trace_loss_failure
    from dal_core.d1_rank_policy import SyllableRankVector

    if corr_result is None:
        corr_result = Corr_D1_Result(is_correct=False, checks=[])

    if failure_set is None:
        failure_set = D1FailureSet()
        # Add generic failure with reason
        failure_set.add(make_trace_loss_failure(span=(0, 0)))

    if rank_vector is None:
        rank_vector = SyllableRankVector(
            pattern_legality=0.0,
            boundary_confidence=0.0,
            trace_completeness=0.0
        )

    return ProofObject_D1(
        candidate_id=candidate_id,
        is_certified=False,
        corr_result=corr_result,
        failure_set=failure_set,
        rank_vector=rank_vector,
        metadata={'uncertified_reason': reason}
    )


def verify_proof_consistency(proof: ProofObject_D1) -> tuple[bool, str]:
    """Verify proof is internally consistent.

    Args:
        proof: Proof to verify

    Returns:
        (is_consistent, reason) tuple
    """
    # Check: certified ⟹ corr_result.is_correct
    if proof.is_certified and not proof.corr_result.is_correct:
        return False, "Certified but Corr_D1 failed"

    # Check: certified ⟹ no critical failures
    if proof.is_certified and proof.failure_set.has_critical_failure():
        return False, "Certified but critical failures exist"

    # Check: not certified ⟹ reason exists
    if not proof.is_certified:
        if proof.corr_result.is_correct and not proof.failure_set.has_critical_failure():
            return False, "Not certified but no failures found"

    return True, "Proof is consistent"


# ============================================================================
# D1 Closure Law (Formal Definition)
# ============================================================================


def is_d1_closed(proof: ProofObject_D1) -> bool:
    """Check if D1 candidate satisfies closure law.

    D1 is closed iff:
        U_D1 defined ∧
        Corr_D1.is_correct ∧
        trace.reversible ∧ reverse_verified ∧
        ¬∃ critical_failure ∧
        rank_vector ≠ ∅ ∧
        anti_promotion_passed ∧
        proof ≠ None ∧
        proof.is_certified

    Args:
        proof: Proof object to check

    Returns:
        True if D1 candidate satisfies closure law
    """
    if proof is None:
        return False

    # Check all closure requirements
    closure_checks = [
        proof.is_certified,                           # Certified
        proof.corr_result.is_correct,                # Corr_D1 passed
        not proof.failure_set.has_critical_failure(), # No critical failures
        proof.rank_vector is not None,               # Rank computed
        len(proof.corr_result.checks) == 8,          # All 8 checks present
    ]

    return all(closure_checks)


def explain_closure_violation(proof: ProofObject_D1) -> str:
    """Explain why D1 is not closed.

    Args:
        proof: Proof to analyze

    Returns:
        Human-readable explanation of closure violations
    """
    if proof is None:
        return "No proof object exists"

    violations = []

    if not proof.is_certified:
        violations.append("Not certified")

    if not proof.corr_result.is_correct:
        violations.append(f"Corr_D1 failed: {proof.corr_result.summary()}")

    if proof.failure_set.has_critical_failure():
        critical = proof.failure_set.critical_failures()
        violations.append(f"{len(critical)} critical failures: {[str(f) for f in critical[:3]]}")

    if proof.rank_vector is None:
        violations.append("No rank vector")

    if len(proof.corr_result.checks) != 8:
        violations.append(f"Incomplete checks: {len(proof.corr_result.checks)}/8")

    if not violations:
        return "D1 is closed ✅"

    return "D1 closure violations:\n" + "\n".join(f"  - {v}" for v in violations)
