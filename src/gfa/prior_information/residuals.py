"""
Prior Information Residual Taxonomy

Residuals for prior information system failures.

Critical distinction:
- These are NOT exceptions
- These are governed failures with taxonomic classification
- They carry trace and can be analyzed
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class PriorInformationResidualKind(Enum):
    """
    Residual taxonomy for prior information system.

    Prior Information Residuals:
    - R_PRIOR_MISSING_DOMAIN: Prior information without domain
    - R_PRIOR_MISSING_SOURCE: Prior information without source trace
    - R_PRIOR_MISSING_EVIDENCE: Prior information without evidence or testability
    - R_PRIOR_UNTESTABLE: Prior information that cannot be tested
    - R_PRIOR_OPINION_CONTAMINATION: Prior opinion detected in information

    Name Reality Residuals:
    - R_NAME_ONLY: Name without referent candidate
    - R_NAME_MISSING_REFERENT: Name without referent evidence
    - R_NAME_MISSING_DOMAIN: Name requiring domain but none provided
    - R_NAME_METAPHOR_AS_EXTERNAL: Metaphorical name claiming external existence
    - R_NAME_TECHNICAL_WITHOUT_DOMAIN: Technical term without domain specification
    """

    # Prior Information Residuals
    R_PRIOR_MISSING_DOMAIN = auto()
    R_PRIOR_MISSING_SOURCE = auto()
    R_PRIOR_MISSING_EVIDENCE = auto()
    R_PRIOR_UNTESTABLE = auto()
    R_PRIOR_OPINION_CONTAMINATION = auto()

    # Name Reality Residuals
    R_NAME_ONLY = auto()
    R_NAME_MISSING_REFERENT = auto()
    R_NAME_MISSING_DOMAIN = auto()
    R_NAME_METAPHOR_AS_EXTERNAL = auto()
    R_NAME_TECHNICAL_WITHOUT_DOMAIN = auto()


@dataclass(frozen=True)
class PriorInformationResidual:
    """
    A single residual from prior information system.

    Properties:
    - kind: ResidualKind classification
    - message: Human-readable explanation
    - severity: LOW | MEDIUM | HIGH | BLOCKER
    - trace: Source trace
    """

    kind: PriorInformationResidualKind
    message: str
    severity: str = "MEDIUM"  # LOW | MEDIUM | HIGH | BLOCKER
    trace: Optional[str] = None

    def is_blocker(self) -> bool:
        """Check if this residual blocks admission."""
        return self.severity == "BLOCKER"

    def __str__(self) -> str:
        return f"{self.kind.name}[{self.severity}]: {self.message}"


# Factory functions for residuals

def make_prior_missing_domain_residual(content: str) -> PriorInformationResidual:
    """Create residual for missing domain."""
    return PriorInformationResidual(
        kind=PriorInformationResidualKind.R_PRIOR_MISSING_DOMAIN,
        message=f"Prior information missing domain: {content[:50]}",
        severity="BLOCKER",
    )


def make_prior_missing_source_residual(content: str) -> PriorInformationResidual:
    """Create residual for missing source."""
    return PriorInformationResidual(
        kind=PriorInformationResidualKind.R_PRIOR_MISSING_SOURCE,
        message=f"Prior information missing source trace: {content[:50]}",
        severity="BLOCKER",
    )


def make_prior_missing_evidence_residual(content: str) -> PriorInformationResidual:
    """Create residual for missing evidence."""
    return PriorInformationResidual(
        kind=PriorInformationResidualKind.R_PRIOR_MISSING_EVIDENCE,
        message=f"Prior information missing evidence or testability: {content[:50]}",
        severity="HIGH",
    )


def make_prior_untestable_residual(content: str) -> PriorInformationResidual:
    """Create residual for untestable prior."""
    return PriorInformationResidual(
        kind=PriorInformationResidualKind.R_PRIOR_UNTESTABLE,
        message=f"Prior information is untestable: {content[:50]}",
        severity="HIGH",
    )


def make_prior_opinion_contamination_residual(
    opinion_type: str, contamination_risk: float
) -> PriorInformationResidual:
    """Create residual for opinion contamination."""
    return PriorInformationResidual(
        kind=PriorInformationResidualKind.R_PRIOR_OPINION_CONTAMINATION,
        message=f"Prior opinion contamination: {opinion_type}, risk={contamination_risk:.2f}",
        severity="BLOCKER",
    )


def make_name_only_residual(name: str) -> PriorInformationResidual:
    """Create residual for name without referent."""
    return PriorInformationResidual(
        kind=PriorInformationResidualKind.R_NAME_ONLY,
        message=f"Name without referent candidate: {name}",
        severity="BLOCKER",
    )


def make_name_missing_referent_residual(name: str) -> PriorInformationResidual:
    """Create residual for name missing referent evidence."""
    return PriorInformationResidual(
        kind=PriorInformationResidualKind.R_NAME_MISSING_REFERENT,
        message=f"Name missing referent evidence: {name}",
        severity="HIGH",
    )


def make_name_missing_domain_residual(name: str, existence_type: str) -> PriorInformationResidual:
    """Create residual for name missing required domain."""
    return PriorInformationResidual(
        kind=PriorInformationResidualKind.R_NAME_MISSING_DOMAIN,
        message=f"Name '{name}' with existence type '{existence_type}' requires domain",
        severity="BLOCKER",
    )


def make_name_metaphor_as_external_residual(name: str) -> PriorInformationResidual:
    """Create residual for metaphor claiming external existence."""
    return PriorInformationResidual(
        kind=PriorInformationResidualKind.R_NAME_METAPHOR_AS_EXTERNAL,
        message=f"Metaphorical name '{name}' cannot claim external existence",
        severity="BLOCKER",
    )


def make_name_technical_without_domain_residual(name: str) -> PriorInformationResidual:
    """Create residual for technical term without domain."""
    return PriorInformationResidual(
        kind=PriorInformationResidualKind.R_NAME_TECHNICAL_WITHOUT_DOMAIN,
        message=f"Technical name '{name}' requires domain specification",
        severity="BLOCKER",
    )
