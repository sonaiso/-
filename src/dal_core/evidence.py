"""
Evidence System (نظام الدليل)

Tracks the evidence and justification for every decision in the pipeline.
"""

from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class Evidence:
    """
    دليل (Evidence)

    Records the justification for a decision or classification.
    """
    source: str                          # Source of evidence
    reason: str                          # Why this decision was made
    confidence: float = 1.0              # Confidence level [0, 1]
    metadata: dict = field(default_factory=dict)

    def __str__(self) -> str:
        conf = f" (ثقة: {self.confidence:.2f})" if self.confidence < 1.0 else ""
        return f"{self.source}: {self.reason}{conf}"


@dataclass
class FeatureEvidence:
    """
    دليل خاصية

    Evidence for a specific feature value.
    """
    feature_name: str
    feature_value: Any
    evidence: Evidence

    def __str__(self) -> str:
        return f"{self.feature_name}={self.feature_value} ← {self.evidence}"


def make_evidence(
    source: str,
    reason: str,
    confidence: float = 1.0,
    **metadata: Any
) -> Evidence:
    """Helper to create evidence"""
    return Evidence(
        source=source,
        reason=reason,
        confidence=confidence,
        metadata=metadata
    )


def make_feature_evidence(
    feature_name: str,
    feature_value: Any,
    source: str,
    reason: str,
    confidence: float = 1.0
) -> FeatureEvidence:
    """Helper to create feature evidence"""
    return FeatureEvidence(
        feature_name=feature_name,
        feature_value=feature_value,
        evidence=make_evidence(source, reason, confidence)
    )
