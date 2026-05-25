"""
Potential Path - Foundational Potentiality-Certification Separation

CONSTITUTIONAL LAW:
    Carrier never issues Certificate directly.
    Carrier only opens PotentialPath.
    PotentialPath becomes Certificate only through Gate + Evidence + Rank + Residuals + Trace.

Core Principle (القانون التأسيسي):
    الحامل لا يشهد - Carrier does NOT certify
    الحامل يفتح إمكانًا - Carrier only opens possibility
    الإمكان لا يصير شهادة إلا ببوابة - Possibility becomes certificate only through gate

This is NOT a late weight-only concept.
This is a FOUNDATIONAL principle applying to ALL layers from U₀ onward.

Architecture:
    U₀ UnicodeCarrier → PotentialGraphemePath → GraphemeGate → U₁ Certificate
    U₁ GraphemeCarrier → PotentialPhoneticPath → PhoneticGate → U₂p Certificate
    U₂p PhoneticProjectionCarrier → PotentialSyllablePath → SyllableGate → U₂s Certificate
    U₂s SyllableCarrier → PotentialBoundaryPath → BoundaryGate → U₃ Certificate
    ...
    U₈ RootStemCarrier → PotentialWeightedPath → WeightGate → U₉ Certificate

Formal Law:
    Carrierᵢ(x) ⊬ Certificateᵢ₊₁(x)
    Carrierᵢ(x) ⊢ PotentialPathᵢ₊₁(x)

    PotentialPathᵢ₊₁(x) + Gateᵢ₊₁ + Evidence + Rank + Residuals + Trace
    ⇒ Certificateᵢ₊₁(x)

PR: FOUNDATION-POTENTIALITY-LAW
Created: 2026-05-25
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, FrozenSet, Optional, Any
from uuid import uuid4

from dal_core.foundation.rank import Rank
from dal_core.residuals import Residual


# ============================================================================
# Potential Path Status
# ============================================================================

class PotentialPathStatus(Enum):
    """
    Status of a potential path from carrier to next layer.

    Progression mirrors Rank but emphasizes path possibility vs. certification:
        CANDIDATE: Path is possible, minimal evidence
        HYPOTHESIS: Path has weak supporting evidence
        STRONG_HYPOTHESIS: Path has strong evidence, may have competitors
        CERTIFICATE: Path is certified through gate with full evidence
        BLOCKED: Path is blocked, cannot proceed

    Critical Law:
        Status ≠ automatic progression.
        CANDIDATE → CERTIFICATE requires Gate + Evidence, not time.
    """
    CANDIDATE = auto()           # Potential path identified
    HYPOTHESIS = auto()          # Weak evidence supports path
    STRONG_HYPOTHESIS = auto()   # Strong evidence, competitors may exist
    CERTIFICATE = auto()         # Path certified through gate
    BLOCKED = auto()             # Path blocked, cannot proceed

    def can_progress_to(self, target: 'PotentialPathStatus') -> bool:
        """Check if progression to target status is permitted."""
        if self == PotentialPathStatus.BLOCKED:
            return False

        order = [
            PotentialPathStatus.CANDIDATE,
            PotentialPathStatus.HYPOTHESIS,
            PotentialPathStatus.STRONG_HYPOTHESIS,
            PotentialPathStatus.CERTIFICATE
        ]

        if target == PotentialPathStatus.BLOCKED:
            return True  # Can always fail

        try:
            current_idx = order.index(self)
            target_idx = order.index(target)
            return target_idx >= current_idx
        except ValueError:
            return False

    def is_certified(self) -> bool:
        """Check if status is CERTIFICATE."""
        return self == PotentialPathStatus.CERTIFICATE

    def is_blocked(self) -> bool:
        """Check if status is BLOCKED."""
        return self == PotentialPathStatus.BLOCKED


# ============================================================================
# Potential Path Core Structure
# ============================================================================

@dataclass(frozen=True)
class PotentialPath:
    """
    Represents a potential path from source carrier to target layer.

    This is the FUNDAMENTAL structure preventing direct carrier-to-certificate jumps.

    Every carrier in every layer produces PotentialPaths, not Certificates.

    Example Paths:
        UnicodeCarrier(ك) → PotentialArabicBaseLetterPath
        UnicodeCarrier(َ) → PotentialAttachedMarkPath (blocked if unattached)
        GraphemeCluster(كَ) → PotentialCVPhoneticPath
        PhoneticProjection(C+V) → PotentialCVSyllablePath
        Syllable(كَتَبَ) → PotentialBoundaryPath
        TrueLafẓ(كَتَبَ) → PotentialVerbWeightedPath

    Fields:
        path_id: Unique identifier for this potential path
        source_carrier_id: ID of source carrier
        source_layer: Name of source layer (U₀, U₁, U₂p, etc.)
        target_layer: Name of target layer
        path_name: Descriptive name of this path
        path_family: Family/category of paths (e.g., "phonetic", "syllabic", "weighted")
        status: Current status (CANDIDATE → CERTIFICATE or BLOCKED)
        required_gates: Tuple of gate names that must pass
        passed_gates: Tuple of gates that have passed
        failed_gates: Tuple of gates that have failed
        evidence: Tuple of evidence items supporting this path
        residuals: Tuple of residuals (warnings/blockers)
        competitors: Tuple of competing path IDs
        rank: Epistemic rank of this path
        trace: Tuple of trace IDs to previous layers
        metadata: Optional additional metadata

    Critical Laws:
        1. PotentialPath ≠ Certificate
        2. status=CERTIFICATE requires all required_gates in passed_gates
        3. status=CERTIFICATE requires no failed_gates
        4. status=CERTIFICATE requires no blocking residuals
        5. status=BLOCKED if any required gate fails
        6. Carriers produce PotentialPaths, NOT Certificates
    """
    path_id: str
    source_carrier_id: str
    source_layer: str
    target_layer: str
    path_name: str
    path_family: str
    status: PotentialPathStatus
    required_gates: Tuple[str, ...]
    passed_gates: Tuple[str, ...]
    failed_gates: Tuple[str, ...]
    evidence: Tuple[str, ...]
    residuals: FrozenSet[Residual]
    competitors: Tuple[str, ...]
    rank: Rank
    trace: Tuple[str, ...]
    metadata: Optional[Any] = None

    def __post_init__(self):
        """Validate PotentialPath invariants."""
        # If certified, must have evidence
        if self.status == PotentialPathStatus.CERTIFICATE:
            if not self.evidence:
                raise ValueError(
                    "CERTIFICATE status requires evidence. "
                    "PotentialPath cannot certify without proof."
                )

            # All required gates must have passed
            if not set(self.required_gates).issubset(set(self.passed_gates)):
                raise ValueError(
                    "CERTIFICATE status requires all required_gates in passed_gates. "
                    f"Required: {self.required_gates}, Passed: {self.passed_gates}"
                )

            # No gates should have failed
            if self.failed_gates:
                raise ValueError(
                    "CERTIFICATE status cannot coexist with failed_gates. "
                    f"Failed gates: {self.failed_gates}"
                )

        # If blocked, must have reason
        if self.status == PotentialPathStatus.BLOCKED:
            if not self.failed_gates and not any(r.is_blocker for r in self.residuals):
                raise ValueError(
                    "BLOCKED status requires either failed_gates or blocking residuals. "
                    "Blocks must have justification."
                )

    def is_certified(self) -> bool:
        """Check if path is certified."""
        return self.status == PotentialPathStatus.CERTIFICATE

    def is_blocked(self) -> bool:
        """Check if path is blocked."""
        return self.status == PotentialPathStatus.BLOCKED

    def has_blocking_residuals(self) -> bool:
        """Check if path has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    def can_certify(self) -> bool:
        """
        Check if path CAN be certified (has met all requirements).

        This is different from is_certified() - it checks requirements,
        not current status.
        """
        # All required gates must have passed
        if not set(self.required_gates).issubset(set(self.passed_gates)):
            return False

        # No gates should have failed
        if self.failed_gates:
            return False

        # No blocking residuals
        if self.has_blocking_residuals():
            return False

        # Must have evidence
        if not self.evidence:
            return False

        return True


# ============================================================================
# Path Certification Validator
# ============================================================================

def certify_path(path: PotentialPath) -> bool:
    """
    Validate that a PotentialPath meets certification requirements.

    Args:
        path: PotentialPath to validate

    Returns:
        True if path can be certified, False otherwise

    Requirements:
        1. All required_gates must be in passed_gates
        2. No failed_gates
        3. No blocking residuals
        4. Has evidence
        5. Status is CERTIFICATE

    This enforces the law: Possibility ≠ Certificate until proven.
    """
    if not path.is_certified():
        return False

    return path.can_certify()


def has_blocking_residuals(residuals: FrozenSet[Residual]) -> bool:
    """Check if residual set contains blockers."""
    return any(r.is_blocker for r in residuals)


# ============================================================================
# Direct Certification Prevention
# ============================================================================

class DirectCertificationError(Exception):
    """
    Raised when a carrier attempts to directly certify next layer.

    This enforces the constitutional law:
        Carrier ⊬ Certificate
        Carrier ⊢ PotentialPath only
    """
    pass


def validate_no_direct_certificate(
    carrier_layer: str,
    certificate_layer: str,
    has_potential_path: bool
) -> None:
    """
    Validate that certification does not bypass PotentialPath.

    Args:
        carrier_layer: Name of source carrier layer (e.g., "U0_UNICODE")
        certificate_layer: Name of target certificate layer (e.g., "U1_GRAPHEME")
        has_potential_path: Whether PotentialPath was created

    Raises:
        DirectCertificationError: If certification attempted without PotentialPath

    Example Violations:
        UnicodeCarrier(ك) → GraphemeCertificate (NO PotentialPath) ❌
        SyllableCarrier → WeightCertificate (NO PotentialPath) ❌

    Example Valid:
        UnicodeCarrier(ك) → PotentialGraphemePath → Gate → Certificate ✅
    """
    if not has_potential_path:
        raise DirectCertificationError(
            f"Constitutional Violation: {carrier_layer} attempted to directly certify {certificate_layer}. "
            f"Law: Carrier ⊬ Certificate. Carrier ⊢ PotentialPath only. "
            f"Required path: {carrier_layer} → PotentialPath → Gate → {certificate_layer}"
        )


# ============================================================================
# Factory Functions
# ============================================================================

def make_potential_path(
    source_carrier_id: str,
    source_layer: str,
    target_layer: str,
    path_name: str,
    path_family: str,
    required_gates: Tuple[str, ...],
    evidence: Tuple[str, ...] = (),
    rank: Rank = Rank.CANDIDATE,
    trace: Tuple[str, ...] = (),
) -> PotentialPath:
    """
    Factory function for creating PotentialPath in CANDIDATE status.

    This is the standard way carriers create potential paths.

    Args:
        source_carrier_id: ID of source carrier
        source_layer: Name of source layer
        target_layer: Name of target layer
        path_name: Descriptive name
        path_family: Path family/category
        required_gates: Gates that must pass for certification
        evidence: Initial evidence (optional)
        rank: Initial rank (default: CANDIDATE)
        trace: Trace to previous layers

    Returns:
        PotentialPath in CANDIDATE status
    """
    return PotentialPath(
        path_id=str(uuid4()),
        source_carrier_id=source_carrier_id,
        source_layer=source_layer,
        target_layer=target_layer,
        path_name=path_name,
        path_family=path_family,
        status=PotentialPathStatus.CANDIDATE,
        required_gates=required_gates,
        passed_gates=(),
        failed_gates=(),
        evidence=evidence,
        residuals=frozenset(),
        competitors=(),
        rank=rank,
        trace=trace,
        metadata=None
    )


def certify_potential_path(
    path: PotentialPath,
    passed_gates: Tuple[str, ...],
    evidence: Tuple[str, ...],
    residuals: FrozenSet[Residual] = frozenset(),
    rank: Rank = Rank.CERTIFICATE,
) -> PotentialPath:
    """
    Certify a PotentialPath after gates have passed.

    Args:
        path: Original PotentialPath
        passed_gates: Gates that have passed
        evidence: Evidence for certification
        residuals: Final residuals (optional)
        rank: Final rank (default: CERTIFICATE)

    Returns:
        New PotentialPath with CERTIFICATE status

    Raises:
        ValueError: If certification requirements not met
    """
    # Verify all required gates passed
    if not set(path.required_gates).issubset(set(passed_gates)):
        missing = set(path.required_gates) - set(passed_gates)
        raise ValueError(
            f"Cannot certify: Missing required gates {missing}. "
            f"Required: {path.required_gates}, Passed: {passed_gates}"
        )

    # Verify no blocking residuals
    if has_blocking_residuals(residuals):
        raise ValueError(
            "Cannot certify: Path has blocking residuals. "
            "Blockers must be resolved before certification."
        )

    return PotentialPath(
        path_id=path.path_id,
        source_carrier_id=path.source_carrier_id,
        source_layer=path.source_layer,
        target_layer=path.target_layer,
        path_name=path.path_name,
        path_family=path.path_family,
        status=PotentialPathStatus.CERTIFICATE,
        required_gates=path.required_gates,
        passed_gates=passed_gates,
        failed_gates=(),
        evidence=evidence,
        residuals=residuals,
        competitors=path.competitors,
        rank=rank,
        trace=path.trace,
        metadata=path.metadata
    )


def block_potential_path(
    path: PotentialPath,
    failed_gates: Tuple[str, ...],
    residuals: FrozenSet[Residual],
    reason: str = "",
) -> PotentialPath:
    """
    Block a PotentialPath due to gate failure or blocking residuals.

    Args:
        path: Original PotentialPath
        failed_gates: Gates that failed
        residuals: Residuals causing block
        reason: Human-readable reason for block

    Returns:
        New PotentialPath with BLOCKED status
    """
    return PotentialPath(
        path_id=path.path_id,
        source_carrier_id=path.source_carrier_id,
        source_layer=path.source_layer,
        target_layer=path.target_layer,
        path_name=path.path_name,
        path_family=path.path_family,
        status=PotentialPathStatus.BLOCKED,
        required_gates=path.required_gates,
        passed_gates=path.passed_gates,
        failed_gates=failed_gates,
        evidence=path.evidence,
        residuals=residuals,
        competitors=path.competitors,
        rank=Rank.BLOCKED,
        trace=path.trace,
        metadata={"block_reason": reason} if reason else path.metadata
    )
