"""
EvidencePolicy - سياسة الدليل

Defines what counts as valid evidence in each domain.

Nabhani Core Principle:
    الدليل يختلف باختلاف المجال
    Evidence varies by domain.

Critical Laws:
    1. Evidence policy is domain-specific
    2. Evidence from wrong domain is rejected
    3. Evidence quality determines claim strength
    4. No claim without evidence
    5. Evidence does not create meaning
    6. Evidence supports or refutes claims, does not judge them

Position:
    EvidencePolicy is declaration layer, not execution layer.
    EvidencePolicy does NOT issue judgment.
    EvidencePolicy does NOT certify claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .domain_spec import ThinkingDomain, EvidenceKind


class EvidenceStrength(Enum):
    """
    Strength of evidence - قوة الدليل

    This is descriptive, not prescriptive.
    Strength assessment is domain-specific.
    """

    # Evidence strength levels
    DECISIVE = "decisive"  # قطعي
    STRONG = "strong"  # قوي
    MODERATE = "moderate"  # متوسط
    WEAK = "weak"  # ضعيف
    INSUFFICIENT = "insufficient"  # غير كاف
    INVALID = "invalid"  # باطل


class EvidenceRequirement(Enum):
    """
    Requirements for evidence in different contexts.
    """

    MANDATORY = "mandatory"  # Must have this evidence
    RECOMMENDED = "recommended"  # Should have this evidence
    OPTIONAL = "optional"  # May have this evidence
    FORBIDDEN = "forbidden"  # Must NOT have this evidence


@dataclass(frozen=True)
class EvidenceConstraint:
    """
    A constraint on what evidence is required or forbidden.
    """
    evidence_kind: EvidenceKind
    requirement: EvidenceRequirement
    reason: str


@dataclass(frozen=True)
class EvidencePolicy:
    """
    Policy governing evidence in a specific domain.

    EvidencePolicy declares what evidence is valid, required, or forbidden.
    It does NOT evaluate claims or issue judgments.

    Critical Laws:
        - EvidencePolicy is domain-bound
        - EvidencePolicy does NOT implement reasoning
        - EvidencePolicy does NOT certify claims
        - EvidencePolicy only declares requirements
    """
    domain: ThinkingDomain

    # Required evidence kinds for claims in this domain
    required_evidence: frozenset[EvidenceKind]

    # Optional evidence kinds (may strengthen claim)
    optional_evidence: frozenset[EvidenceKind]

    # Forbidden evidence kinds (invalid in this domain)
    forbidden_evidence: frozenset[EvidenceKind]

    # Minimum evidence strength for different claim types
    min_strength_for_zanni: EvidenceStrength = EvidenceStrength.WEAK
    min_strength_for_certified: EvidenceStrength = EvidenceStrength.STRONG
    min_strength_for_decisive: EvidenceStrength = EvidenceStrength.DECISIVE

    def __post_init__(self):
        """Validate evidence policy construction."""
        # Check no overlap between required and forbidden
        overlap = self.required_evidence & self.forbidden_evidence
        if overlap:
            raise ValueError(
                f"Evidence cannot be both required and forbidden: {overlap}"
            )

        # Check no overlap between optional and forbidden
        overlap = self.optional_evidence & self.forbidden_evidence
        if overlap:
            raise ValueError(
                f"Evidence cannot be both optional and forbidden: {overlap}"
            )

    def allows_evidence_kind(self, kind: EvidenceKind) -> bool:
        """Check if evidence kind is allowed in this domain."""
        return (
            kind in self.required_evidence
            or kind in self.optional_evidence
        ) and kind not in self.forbidden_evidence

    def requires_evidence_kind(self, kind: EvidenceKind) -> bool:
        """Check if evidence kind is required in this domain."""
        return kind in self.required_evidence

    def forbids_evidence_kind(self, kind: EvidenceKind) -> bool:
        """Check if evidence kind is forbidden in this domain."""
        return kind in self.forbidden_evidence

    def get_requirement(self, kind: EvidenceKind) -> EvidenceRequirement:
        """Get requirement level for evidence kind."""
        if kind in self.required_evidence:
            return EvidenceRequirement.MANDATORY
        elif kind in self.optional_evidence:
            return EvidenceRequirement.OPTIONAL
        elif kind in self.forbidden_evidence:
            return EvidenceRequirement.FORBIDDEN
        else:
            # Not specified - treat as forbidden by default
            return EvidenceRequirement.FORBIDDEN

    def is_strength_sufficient(
        self,
        strength: EvidenceStrength,
        target_rank: str  # "ZANNI", "CERTIFIED", "DECISIVE"
    ) -> bool:
        """
        Check if evidence strength is sufficient for target rank.

        This is descriptive check, not judgment.
        Actual rank assignment happens elsewhere.
        """
        strength_order = [
            EvidenceStrength.INVALID,
            EvidenceStrength.INSUFFICIENT,
            EvidenceStrength.WEAK,
            EvidenceStrength.MODERATE,
            EvidenceStrength.STRONG,
            EvidenceStrength.DECISIVE,
        ]

        if target_rank == "ZANNI":
            min_strength = self.min_strength_for_zanni
        elif target_rank == "CERTIFIED":
            min_strength = self.min_strength_for_certified
        elif target_rank == "DECISIVE":
            min_strength = self.min_strength_for_decisive
        else:
            return False

        try:
            strength_idx = strength_order.index(strength)
            min_idx = strength_order.index(min_strength)
            return strength_idx >= min_idx
        except ValueError:
            return False


# Factory functions for domain-specific policies

def make_material_evidence_policy() -> EvidencePolicy:
    """Create evidence policy for material/experimental domain."""
    return EvidencePolicy(
        domain=ThinkingDomain.MATERIAL_EXPERIMENTAL,
        required_evidence=frozenset([
            EvidenceKind.OBSERVATION,
            EvidenceKind.MEASUREMENT,
        ]),
        optional_evidence=frozenset([
            EvidenceKind.SENSORY,
        ]),
        forbidden_evidence=frozenset([
            EvidenceKind.AXIOM,
            EvidenceKind.PROOF,
            EvidenceKind.NASS,
            EvidenceKind.IJMA,
            EvidenceKind.QIYAS,
        ]),
        min_strength_for_zanni=EvidenceStrength.WEAK,
        min_strength_for_certified=EvidenceStrength.STRONG,
        min_strength_for_decisive=EvidenceStrength.DECISIVE,
    )


def make_formal_evidence_policy() -> EvidencePolicy:
    """Create evidence policy for formal/logical domain."""
    return EvidencePolicy(
        domain=ThinkingDomain.FORMAL_LOGICAL,
        required_evidence=frozenset([
            EvidenceKind.AXIOM,
            EvidenceKind.PROOF,
        ]),
        optional_evidence=frozenset([
            EvidenceKind.DERIVATION,
        ]),
        forbidden_evidence=frozenset([
            EvidenceKind.MEASUREMENT,
            EvidenceKind.OBSERVATION,
            EvidenceKind.NASS,
            EvidenceKind.ISTIMAL,
        ]),
        min_strength_for_zanni=EvidenceStrength.MODERATE,
        min_strength_for_certified=EvidenceStrength.STRONG,
        min_strength_for_decisive=EvidenceStrength.DECISIVE,
    )


def make_lafzi_evidence_policy() -> EvidencePolicy:
    """
    Create evidence policy for lafzi/dalali domain.

    This is DECLARATION ONLY.
    Actual LafziMadlul implementation is NOT part of this PR.
    """
    return EvidencePolicy(
        domain=ThinkingDomain.LAFZI_DALALI,
        required_evidence=frozenset([
            EvidenceKind.WADH,  # وضع لغوي
            EvidenceKind.ISTIMAL,  # استعمال
        ]),
        optional_evidence=frozenset([
            EvidenceKind.QARYNAH,  # قرينة
        ]),
        forbidden_evidence=frozenset([
            EvidenceKind.MEASUREMENT,
            EvidenceKind.PROOF,
            EvidenceKind.EXECUTION,
        ]),
        min_strength_for_zanni=EvidenceStrength.WEAK,
        min_strength_for_certified=EvidenceStrength.STRONG,
        min_strength_for_decisive=EvidenceStrength.DECISIVE,
    )


def make_textual_evidence_policy() -> EvidencePolicy:
    """Create evidence policy for textual/normative domain."""
    return EvidencePolicy(
        domain=ThinkingDomain.TEXTUAL_NORMATIVE,
        required_evidence=frozenset([
            EvidenceKind.NASS,  # نص
        ]),
        optional_evidence=frozenset([
            EvidenceKind.IJMA,  # إجماع
            EvidenceKind.QIYAS,  # قياس
        ]),
        forbidden_evidence=frozenset([
            EvidenceKind.MEASUREMENT,
            EvidenceKind.EXECUTION,
            EvidenceKind.PROOF,
        ]),
        min_strength_for_zanni=EvidenceStrength.WEAK,
        min_strength_for_certified=EvidenceStrength.STRONG,
        min_strength_for_decisive=EvidenceStrength.DECISIVE,
    )


def make_programming_evidence_policy() -> EvidencePolicy:
    """Create evidence policy for programming/execution domain."""
    return EvidencePolicy(
        domain=ThinkingDomain.PROGRAMMING_EXECUTION,
        required_evidence=frozenset([
            EvidenceKind.EXECUTION,
            EvidenceKind.TYPE_CHECK,
        ]),
        optional_evidence=frozenset([
            EvidenceKind.ASSERTION,
        ]),
        forbidden_evidence=frozenset([
            EvidenceKind.NASS,
            EvidenceKind.IJMA,
            EvidenceKind.WADH,
            EvidenceKind.QARYNAH,
        ]),
        min_strength_for_zanni=EvidenceStrength.WEAK,
        min_strength_for_certified=EvidenceStrength.STRONG,
        min_strength_for_decisive=EvidenceStrength.DECISIVE,
    )
