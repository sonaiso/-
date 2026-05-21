"""D2 Proof Object (ProofObject_D2).

Certification proof for pre-morphological unit candidates.

A candidate is certified iff:
    ProofObject_D2.is_certified = True

Certification requires:
- All Corr_D2 checks pass
- No critical failures exist
- Trace is reversible (verified, not just claimed)
- Anti-promotion validated (no D3/D4/D5/D6 fields)
- Rank vector computed
- Source syllables are D1-certified

Critical Law: D2 does NOT inherit D1 certification.
D2 must prove its OWN correctness independently.

This enforces the law:
    High rank ≠ correctness
    Certification = formal proof, not statistical confidence
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

from dal_core.d2_correctness import Corr_D2_Result
from dal_core.d2_failures import D2FailureSet
from dal_core.d2_rank_policy import PreMorphRankVector


@dataclass
class ProofObject_D2:
    """
    Certification proof for D2 candidate.

    Proves candidate passed all D2 correctness checks.

    This is NOT a rank or confidence score.
    This is a formal proof object.

    Independent from D1's ProofObject_D1.
    """
    candidate_id: str
    is_certified: bool
    corr_result: Corr_D2_Result
    failure_set: D2FailureSet
    rank_vector: PreMorphRankVector
    certification_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    # D2-specific: Evidence of D1 certification
    d1_syllable_certification_verified: bool = False

    def __post_init__(self):
        """Validate proof invariants."""
        # Critical invariant: is_certified must match corr_result
        if self.is_certified and not self.corr_result.is_correct:
            raise ValueError(
                "Proof claims certification but Corr_D2 failed. "
                "is_certified must be False when corr_result.is_correct is False."
            )

        # Critical invariant: is_certified must check for critical failures
        if self.is_certified and self.failure_set.has_critical_failure():
            raise ValueError(
                "Proof claims certification but critical failures exist. "
                "is_certified must be False when critical failures present."
            )

        # Critical invariant: D2 must verify D1 certification
        if self.is_certified and not self.d1_syllable_certification_verified:
            raise ValueError(
                "Proof claims certification but D1 syllable certification not verified. "
                "D2 requires certified D1 syllables as input."
            )

    def failed_checks(self) -> list:
        """Get list of failed Corr_D2 checks."""
        return self.corr_result.failed_checks()

    def critical_failures(self) -> list:
        """Get list of critical D2 failures."""
        return self.failure_set.critical_failures()

    def is_valid_for_promotion(self) -> bool:
        """Check if candidate can be promoted to D3.

        Promotion requires:
        - is_certified = True
        - No critical failures
        - Corr_D2 passed
        - D1 certification verified

        Returns:
            True if candidate may be promoted to D3
        """
        return (
            self.is_certified and
            not self.failure_set.has_critical_failure() and
            self.corr_result.is_correct and
            self.d1_syllable_certification_verified
        )

    def summary(self) -> str:
        """Summary of proof status."""
        if self.is_certified:
            status = "✅ CERTIFIED"
        else:
            status = "❌ NOT CERTIFIED"

        corr_summary = self.corr_result.summary()
        failure_summary = self.failure_set.summary()

        d1_cert = "✅" if self.d1_syllable_certification_verified else "❌"

        return (
            f"{status}\n"
            f"  Corr_D2: {corr_summary}\n"
            f"  Failures: {failure_summary}\n"
            f"  Rank: {self.rank_vector.total_rank():.2f}\n"
            f"  D1 Certification Verified: {d1_cert}\n"
            f"  Timestamp: {self.certification_timestamp}"
        )

    def __str__(self) -> str:
        """Human-readable proof representation."""
        cert_mark = "✅" if self.is_certified else "❌"
        return f"{cert_mark} ProofObject_D2({self.candidate_id}, certified={self.is_certified})"


# ============================================================================
# Proof Construction Functions
# ============================================================================


def create_d2_proof(
    candidate_id: str,
    corr_result: Corr_D2_Result,
    failure_set: D2FailureSet,
    rank_vector: PreMorphRankVector,
    d1_syllable_certification_verified: bool,
    metadata: Optional[Dict[str, Any]] = None
) -> ProofObject_D2:
    """Create D2 proof object from validation results.

    Args:
        candidate_id: Candidate identifier
        corr_result: Corr_D2 validation result
        failure_set: D2 failures
        rank_vector: Rank vector
        d1_syllable_certification_verified: Whether D1 syllables were verified certified
        metadata: Optional metadata

    Returns:
        ProofObject_D2

    The proof is certified iff:
    - corr_result.is_correct = True
    - No critical failures exist
    - D1 syllable certification verified
    """
    is_certified = (
        corr_result.is_correct and
        not failure_set.has_critical_failure() and
        d1_syllable_certification_verified
    )

    return ProofObject_D2(
        candidate_id=candidate_id,
        is_certified=is_certified,
        corr_result=corr_result,
        failure_set=failure_set,
        rank_vector=rank_vector,
        d1_syllable_certification_verified=d1_syllable_certification_verified,
        metadata=metadata or {}
    )


def create_uncertified_d2_proof(
    candidate_id: str,
    reason: str
) -> ProofObject_D2:
    """Create uncertified proof (for error cases).

    Args:
        candidate_id: Candidate identifier
        reason: Reason for failure

    Returns:
        Uncertified ProofObject_D2
    """
    from dal_core.d2_correctness import Corr_D2_Result, CorrectnessCheck

    # Create failed correctness result
    corr_result = Corr_D2_Result(
        is_correct=False,
        checks=[
            CorrectnessCheck(
                name="validation_error",
                passed=False,
                reason=reason
            )
        ]
    )

    # Create empty failure set
    failure_set = D2FailureSet()

    # Create minimal rank vector
    rank_vector = PreMorphRankVector(
        segmentation_simplicity=0.0,
        clitic_confidence=0.0,
        augmentation_consistency=0.0,
        frozen_word_attestation=0.0,
        particle_attestation=0.0,
        syllable_preservation=0.0,
        candidate_discriminability=0.0
    )

    return ProofObject_D2(
        candidate_id=candidate_id,
        is_certified=False,
        corr_result=corr_result,
        failure_set=failure_set,
        rank_vector=rank_vector,
        d1_syllable_certification_verified=False,
        metadata={'uncertified_reason': reason}
    )


def verify_d1_syllable_certification(source_syllables: list) -> bool:
    """Verify all source syllables are D1-certified.

    Args:
        source_syllables: List of SyllableCandidate objects

    Returns:
        True if all syllables are certified
    """
    if not source_syllables:
        return False

    for syll in source_syllables:
        # Check if syllable has proof and is certified
        if not hasattr(syll, 'proof') or syll.proof is None:
            return False
        if not syll.proof.is_certified:
            return False

    return True


# ============================================================================
# Proof Chain Functions
# ============================================================================


def build_certification_chain(
    d2_proof: ProofObject_D2,
    source_syllables: list
) -> Dict[str, Any]:
    """Build certification chain from D1 to D2.

    This shows the evidence chain WITHOUT inheriting certification.

    Args:
        d2_proof: D2 proof object
        source_syllables: Source syllables from D1

    Returns:
        Dictionary with certification chain evidence
    """
    d1_proofs = []
    for syll in source_syllables:
        if hasattr(syll, 'proof') and syll.proof is not None:
            d1_proofs.append({
                'candidate_id': syll.proof.candidate_id,
                'is_certified': syll.proof.is_certified,
                'timestamp': syll.proof.certification_timestamp
            })

    return {
        'd2_certification': {
            'candidate_id': d2_proof.candidate_id,
            'is_certified': d2_proof.is_certified,
            'timestamp': d2_proof.certification_timestamp
        },
        'd1_certifications': d1_proofs,
        'chain_valid': all(p['is_certified'] for p in d1_proofs) and d2_proof.is_certified,
        'note': 'D2 certification is INDEPENDENT from D1 - not inherited'
    }
