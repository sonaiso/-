"""
ResidualPolicy - سياسة البواقي

Defines how residuals are handled in each domain.

Nabhani Core Principle:
    البواقي تحفظ ولا تهمل
    Residuals are preserved, not discarded.

Critical Laws:
    1. All residuals must be tracked
    2. Blocker residuals prevent operation
    3. Domain determines residual severity
    4. Residuals accumulate, not override
    5. Residual policy does NOT remove residuals
    6. Residual policy only classifies them

Position:
    ResidualPolicy is declaration layer, not execution layer.
    ResidualPolicy does NOT resolve residuals.
    ResidualPolicy only declares handling rules.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .domain_spec import ThinkingDomain
from ..rational import RationalResidual, RationalResidualKind


class ResidualSeverity(Enum):
    """
    Severity levels for residuals.

    Severity determines whether operation can proceed.
    """

    BLOCKER = "blocker"  # Blocks operation completely
    HIGH = "high"  # Serious concern, may block
    MEDIUM = "medium"  # Notable concern, tracked
    LOW = "low"  # Minor concern, tracked
    INFO = "info"  # Informational only


class ResidualHandling(Enum):
    """
    How residuals should be handled.
    """

    REJECT = "reject"  # Reject operation
    WARN = "warn"  # Warn but allow
    TRACK = "track"  # Track silently
    IGNORE = "ignore"  # Informational only (still preserved!)


@dataclass(frozen=True)
class ResidualRule:
    """
    Rule for handling a specific residual kind in a domain.
    """
    residual_kind: RationalResidualKind
    severity: ResidualSeverity
    handling: ResidualHandling
    reason: str


@dataclass(frozen=True)
class ResidualPolicy:
    """
    Policy governing residual handling in a domain.

    ResidualPolicy declares how residuals are classified and handled.
    It does NOT remove or resolve residuals.
    All residuals are preserved regardless of handling.

    Critical Laws:
        - ResidualPolicy is domain-bound
        - ResidualPolicy does NOT remove residuals
        - ResidualPolicy does NOT resolve uncertainties
        - ResidualPolicy only declares severity and handling
        - All residuals are preserved in trace
    """
    domain: ThinkingDomain

    # Rules for specific residual kinds
    rules: frozenset[ResidualRule]

    # Default handling for unspecified residuals
    default_severity: ResidualSeverity = ResidualSeverity.MEDIUM
    default_handling: ResidualHandling = ResidualHandling.WARN

    def get_severity(self, residual_kind: RationalResidualKind) -> ResidualSeverity:
        """Get severity for a residual kind in this domain."""
        for rule in self.rules:
            if rule.residual_kind == residual_kind:
                return rule.severity
        return self.default_severity

    def get_handling(self, residual_kind: RationalResidualKind) -> ResidualHandling:
        """Get handling for a residual kind in this domain."""
        for rule in self.rules:
            if rule.residual_kind == residual_kind:
                return rule.handling
        return self.default_handling

    def is_blocker(self, residual: RationalResidual) -> bool:
        """
        Check if residual blocks operation in this domain.

        Blockers prevent operation from succeeding.
        """
        severity = self.get_severity(residual.kind)
        handling = self.get_handling(residual.kind)

        return (
            severity == ResidualSeverity.BLOCKER
            or handling == ResidualHandling.REJECT
        )

    def requires_attention(self, residual: RationalResidual) -> bool:
        """Check if residual requires explicit attention."""
        severity = self.get_severity(residual.kind)
        return severity in [
            ResidualSeverity.BLOCKER,
            ResidualSeverity.HIGH,
            ResidualSeverity.MEDIUM,
        ]

    def blocks_operation(self, residuals: frozenset[RationalResidual]) -> bool:
        """
        Check if any residual blocks operation.

        Returns True if ANY residual is a blocker.
        """
        return any(self.is_blocker(r) for r in residuals)

    def get_blockers(
        self,
        residuals: frozenset[RationalResidual]
    ) -> frozenset[RationalResidual]:
        """Get all blocker residuals from a set."""
        return frozenset(r for r in residuals if self.is_blocker(r))


# Factory functions for domain-specific policies

def make_material_residual_policy() -> ResidualPolicy:
    """
    Create residual policy for material/experimental domain.

    Material domain is strict about missing sensory evidence.
    """
    rules = frozenset([
        ResidualRule(
            residual_kind=RationalResidualKind.MISSING_REALITY,
            severity=ResidualSeverity.BLOCKER,
            handling=ResidualHandling.REJECT,
            reason="Material domain requires physical reality"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.MISSING_SENSORY_TRANSFER,
            severity=ResidualSeverity.BLOCKER,
            handling=ResidualHandling.REJECT,
            reason="Material domain requires sensory evidence"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.PRIOR_OPINION_DETECTED,
            severity=ResidualSeverity.HIGH,
            handling=ResidualHandling.WARN,
            reason="Opinion contamination in experimental domain"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.INSUFFICIENT_EVIDENCE,
            severity=ResidualSeverity.BLOCKER,
            handling=ResidualHandling.REJECT,
            reason="Material claims need sufficient evidence"
        ),
    ])

    return ResidualPolicy(
        domain=ThinkingDomain.MATERIAL_EXPERIMENTAL,
        rules=rules,
        default_severity=ResidualSeverity.MEDIUM,
        default_handling=ResidualHandling.WARN,
    )


def make_formal_residual_policy() -> ResidualPolicy:
    """
    Create residual policy for formal/logical domain.

    Formal domain does not require physical reality or sensory transfer.
    """
    rules = frozenset([
        ResidualRule(
            residual_kind=RationalResidualKind.MISSING_REALITY,
            severity=ResidualSeverity.INFO,
            handling=ResidualHandling.TRACK,
            reason="Formal domain doesn't require physical reality"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.MISSING_SENSORY_TRANSFER,
            severity=ResidualSeverity.INFO,
            handling=ResidualHandling.TRACK,
            reason="Formal domain doesn't require senses"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.PRIOR_OPINION_DETECTED,
            severity=ResidualSeverity.BLOCKER,
            handling=ResidualHandling.REJECT,
            reason="Logic must be free of opinion"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.INSUFFICIENT_EVIDENCE,
            severity=ResidualSeverity.BLOCKER,
            handling=ResidualHandling.REJECT,
            reason="Proofs must be complete"
        ),
    ])

    return ResidualPolicy(
        domain=ThinkingDomain.FORMAL_LOGICAL,
        rules=rules,
        default_severity=ResidualSeverity.HIGH,
        default_handling=ResidualHandling.REJECT,
    )


def make_lafzi_residual_policy() -> ResidualPolicy:
    """
    Create residual policy for lafzi/dalali domain.

    This is DECLARATION ONLY.
    Actual LafziMadlul implementation is NOT part of this PR.
    """
    rules = frozenset([
        ResidualRule(
            residual_kind=RationalResidualKind.MISSING_PRIOR_INFORMATION,
            severity=ResidualSeverity.BLOCKER,
            handling=ResidualHandling.REJECT,
            reason="Linguistic meaning requires prior وضع"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.PRIOR_OPINION_DETECTED,
            severity=ResidualSeverity.HIGH,
            handling=ResidualHandling.WARN,
            reason="Opinion should not affect linguistic analysis"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.INSUFFICIENT_EVIDENCE,
            severity=ResidualSeverity.HIGH,
            handling=ResidualHandling.WARN,
            reason="Meaning claims need استعمال evidence"
        ),
    ])

    return ResidualPolicy(
        domain=ThinkingDomain.LAFZI_DALALI,
        rules=rules,
        default_severity=ResidualSeverity.MEDIUM,
        default_handling=ResidualHandling.WARN,
    )


def make_textual_residual_policy() -> ResidualPolicy:
    """
    Create residual policy for textual/normative domain.

    Textual domain requires prior نصوص knowledge.
    """
    rules = frozenset([
        ResidualRule(
            residual_kind=RationalResidualKind.MISSING_PRIOR_INFORMATION,
            severity=ResidualSeverity.BLOCKER,
            handling=ResidualHandling.REJECT,
            reason="Textual analysis requires prior نصوص"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.PRIOR_OPINION_DETECTED,
            severity=ResidualSeverity.BLOCKER,
            handling=ResidualHandling.REJECT,
            reason="Rulings must be free of opinion"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.INSUFFICIENT_EVIDENCE,
            severity=ResidualSeverity.BLOCKER,
            handling=ResidualHandling.REJECT,
            reason="Rulings require textual evidence"
        ),
    ])

    return ResidualPolicy(
        domain=ThinkingDomain.TEXTUAL_NORMATIVE,
        rules=rules,
        default_severity=ResidualSeverity.HIGH,
        default_handling=ResidualHandling.REJECT,
    )


def make_programming_residual_policy() -> ResidualPolicy:
    """
    Create residual policy for programming/execution domain.

    Programming domain requires execution evidence.
    """
    rules = frozenset([
        ResidualRule(
            residual_kind=RationalResidualKind.MISSING_REALITY,
            severity=ResidualSeverity.BLOCKER,
            handling=ResidualHandling.REJECT,
            reason="Code must execute in real system"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.PRIOR_OPINION_DETECTED,
            severity=ResidualSeverity.MEDIUM,
            handling=ResidualHandling.WARN,
            reason="Code execution is objective"
        ),
        ResidualRule(
            residual_kind=RationalResidualKind.INSUFFICIENT_EVIDENCE,
            severity=ResidualSeverity.HIGH,
            handling=ResidualHandling.WARN,
            reason="Need execution or type check evidence"
        ),
    ])

    return ResidualPolicy(
        domain=ThinkingDomain.PROGRAMMING_EXECUTION,
        rules=rules,
        default_severity=ResidualSeverity.MEDIUM,
        default_handling=ResidualHandling.WARN,
    )
