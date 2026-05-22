"""
Residual Taxonomy for Styles - تصنيف البواقي للأساليب

Style-specific residuals that extend RationalResidual.

Nabhani Core Principle:
    كل أسلوب له بواقيه الخاصة
    Each style has its specific residuals.

Critical Laws:
    1. Style residuals extend RationalResidual
    2. Style residuals are domain-specific
    3. All residuals are preserved
    4. Residuals do not block unless marked blocker
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StyleResidualKind(Enum):
    """
    Categories of residuals specific to style specs.

    These extend RationalResidualKind with style-specific concerns.
    """

    # Domain boundary violations
    DOMAIN_MISMATCH = "domain_mismatch"
    FORBIDDEN_DOMAIN_JUMP = "forbidden_domain_jump"
    MISSING_DOMAIN_BRIDGE = "missing_domain_bridge"

    # Evidence policy violations
    FORBIDDEN_EVIDENCE_KIND = "forbidden_evidence_kind"
    MISSING_REQUIRED_EVIDENCE = "missing_required_evidence"
    EVIDENCE_STRENGTH_INSUFFICIENT = "evidence_strength_insufficient"

    # Rank policy violations
    FORBIDDEN_RANK_TRANSITION = "forbidden_rank_transition"
    RANK_INFLATION_DETECTED = "rank_inflation_detected"
    EXISTENCE_PREDICATE_CONFUSION = "existence_predicate_confusion"

    # Operation policy violations
    FORBIDDEN_OPERATION_ATTEMPTED = "forbidden_operation_attempted"
    OPERATION_WITHOUT_EVIDENCE = "operation_without_evidence"

    # Style spec violations
    STYLE_SPEC_MISSING = "style_spec_missing"
    DOMAIN_SPEC_MISSING = "domain_spec_missing"
    EVIDENCE_POLICY_MISSING = "evidence_policy_missing"
    RANK_POLICY_MISSING = "rank_policy_missing"
    RESIDUAL_POLICY_MISSING = "residual_policy_missing"
    OPERATION_POLICY_MISSING = "operation_policy_missing"

    # Meta violations (critical)
    STYLE_CLAIMS_TO_BE_RATIONAL_METHOD = "style_claims_to_be_rational_method"
    STYLE_IMPLEMENTS_SCIENTIFIC_METHOD = "style_implements_scientific_method"
    STYLE_IMPLEMENTS_LOGICAL_STYLE = "style_implements_logical_style"
    STYLE_IMPLEMENTS_LAFZI_MADLUL = "style_implements_lafzi_madlul"
    STYLE_ISSUES_JUDGMENT = "style_issues_judgment"
    STYLE_CERTIFIES_WITHOUT_AUTHORITY = "style_certifies_without_authority"


@dataclass(frozen=True)
class StyleResidual:
    """
    A residual from style spec validation.

    StyleResiduals represent violations or concerns specific to
    style specifications and domain constraints.
    """
    kind: StyleResidualKind
    description: str
    severity: str = "medium"  # "low", "medium", "high", "blocker"
    context: str = ""  # Additional context

    def is_blocker(self) -> bool:
        """Check if this residual blocks style operation."""
        return self.severity == "blocker"

    def is_meta_violation(self) -> bool:
        """
        Check if this is a meta-level violation.

        Meta violations are critical architectural errors.
        """
        return self.kind in [
            StyleResidualKind.STYLE_CLAIMS_TO_BE_RATIONAL_METHOD,
            StyleResidualKind.STYLE_IMPLEMENTS_SCIENTIFIC_METHOD,
            StyleResidualKind.STYLE_IMPLEMENTS_LOGICAL_STYLE,
            StyleResidualKind.STYLE_IMPLEMENTS_LAFZI_MADLUL,
            StyleResidualKind.STYLE_ISSUES_JUDGMENT,
            StyleResidualKind.STYLE_CERTIFIES_WITHOUT_AUTHORITY,
        ]

    def is_domain_violation(self) -> bool:
        """Check if this is a domain boundary violation."""
        return self.kind in [
            StyleResidualKind.DOMAIN_MISMATCH,
            StyleResidualKind.FORBIDDEN_DOMAIN_JUMP,
            StyleResidualKind.MISSING_DOMAIN_BRIDGE,
        ]

    def is_policy_violation(self) -> bool:
        """Check if this is a policy violation."""
        return self.kind in [
            StyleResidualKind.FORBIDDEN_EVIDENCE_KIND,
            StyleResidualKind.MISSING_REQUIRED_EVIDENCE,
            StyleResidualKind.FORBIDDEN_RANK_TRANSITION,
            StyleResidualKind.RANK_INFLATION_DETECTED,
            StyleResidualKind.FORBIDDEN_OPERATION_ATTEMPTED,
        ]

    def __str__(self) -> str:
        if self.context:
            return f"[{self.kind.value}] {self.description} ({self.context})"
        return f"[{self.kind.value}] {self.description}"


# Factory functions for common style residuals

def make_domain_mismatch_residual(
    expected_domain: str,
    actual_domain: str
) -> StyleResidual:
    """Create residual for domain mismatch."""
    return StyleResidual(
        kind=StyleResidualKind.DOMAIN_MISMATCH,
        description=f"Domain mismatch: expected {expected_domain}, got {actual_domain}",
        severity="blocker",
        context=f"expected={expected_domain}, actual={actual_domain}"
    )


def make_forbidden_domain_jump_residual(
    from_domain: str,
    to_domain: str
) -> StyleResidual:
    """Create residual for forbidden domain jump."""
    return StyleResidual(
        kind=StyleResidualKind.FORBIDDEN_DOMAIN_JUMP,
        description=f"Cannot jump from {from_domain} to {to_domain} without bridge",
        severity="blocker",
        context=f"from={from_domain}, to={to_domain}"
    )


def make_forbidden_evidence_residual(
    evidence_kind: str,
    domain: str
) -> StyleResidual:
    """Create residual for forbidden evidence kind."""
    return StyleResidual(
        kind=StyleResidualKind.FORBIDDEN_EVIDENCE_KIND,
        description=f"Evidence kind {evidence_kind} forbidden in {domain}",
        severity="blocker",
        context=f"evidence={evidence_kind}, domain={domain}"
    )


def make_missing_required_evidence_residual(
    evidence_kind: str,
    domain: str
) -> StyleResidual:
    """Create residual for missing required evidence."""
    return StyleResidual(
        kind=StyleResidualKind.MISSING_REQUIRED_EVIDENCE,
        description=f"Required evidence {evidence_kind} missing in {domain}",
        severity="blocker",
        context=f"evidence={evidence_kind}, domain={domain}"
    )


def make_rank_inflation_residual(
    from_rank: str,
    to_rank: str
) -> StyleResidual:
    """Create residual for rank inflation."""
    return StyleResidual(
        kind=StyleResidualKind.RANK_INFLATION_DETECTED,
        description=f"Rank inflation: {from_rank} → {to_rank} without evidence",
        severity="blocker",
        context=f"from={from_rank}, to={to_rank}"
    )


def make_forbidden_operation_residual(
    operation: str,
    domain: str,
    reason: str
) -> StyleResidual:
    """Create residual for forbidden operation."""
    return StyleResidual(
        kind=StyleResidualKind.FORBIDDEN_OPERATION_ATTEMPTED,
        description=f"Operation {operation} forbidden in {domain}: {reason}",
        severity="blocker",
        context=f"operation={operation}, domain={domain}"
    )


def make_style_spec_missing_residual(component: str) -> StyleResidual:
    """Create residual for missing style spec component."""
    return StyleResidual(
        kind=StyleResidualKind.STYLE_SPEC_MISSING,
        description=f"StyleSpec missing required component: {component}",
        severity="blocker",
        context=f"component={component}"
    )


def make_meta_violation_residual(violation_kind: StyleResidualKind) -> StyleResidual:
    """Create residual for meta-level violation."""
    descriptions = {
        StyleResidualKind.STYLE_CLAIMS_TO_BE_RATIONAL_METHOD: (
            "StyleSpec claims to be RationalMethod"
        ),
        StyleResidualKind.STYLE_IMPLEMENTS_SCIENTIFIC_METHOD: (
            "StyleSpec implements ScientificMethod"
        ),
        StyleResidualKind.STYLE_IMPLEMENTS_LOGICAL_STYLE: (
            "StyleSpec implements LogicalStyle"
        ),
        StyleResidualKind.STYLE_IMPLEMENTS_LAFZI_MADLUL: (
            "StyleSpec implements LafziMadlul"
        ),
        StyleResidualKind.STYLE_ISSUES_JUDGMENT: (
            "StyleSpec issues judgment"
        ),
        StyleResidualKind.STYLE_CERTIFIES_WITHOUT_AUTHORITY: (
            "StyleSpec certifies without authority"
        ),
    }

    return StyleResidual(
        kind=violation_kind,
        description=descriptions.get(violation_kind, "Meta-level violation"),
        severity="blocker",
        context="architectural_violation"
    )
