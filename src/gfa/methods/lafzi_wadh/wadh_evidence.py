"""
WadhEvidence - شاهد الوضع

Critical Law:
    الشاهد ليس وضعاً
    Evidence is NOT Wadh itself.

WadhEvidence represents evidence for a Wadh claim, NOT the Wadh convention itself.

What WadhEvidence Does:
    - Records Wadh evidence
    - Preserves source, transmission mode, and scope
    - Guards against evidence = certification confusion
    - Creates residuals for insufficient evidence

What WadhEvidence Does NOT Do:
    - Does NOT certify Wadh
    - Does NOT create meaning
    - Does NOT implement full Dalālah
    - Does NOT bypass transmission requirements
    - Does NOT issue HUKM

Position in Architecture:
    DalMadlulBindingCandidate (PR-L4, certified)
    └── WadhGeometry (PR-L5A)
        ├── WadhSource
        ├── WadhTransmissionMode
        ├── WadhScope
        ├── WadhEvidence ← THIS MODULE
        ├── WadhClaim
        └── MawduLahStructure
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
from uuid import uuid4

from .wadh_source import WadhSource
from .wadh_transmission_mode import WadhTransmissionMode
from .wadh_scope import WadhScope
from .residual_taxonomy import WadhResidual


@dataclass(frozen=True)
class WadhEvidence:
    """
    Evidence for a Wadh claim.

    This represents evidence that a Wadh (convention) may exist,
    NOT the Wadh itself.

    Critical Properties:
        - source: Where evidence came from
        - transmission_mode: How evidence was transmitted
        - scope: Domain of claimed Wadh
        - evidence_content: What the evidence says
        - binding_trace_id: Preserved from DalMadlulBindingCandidate
        - residuals: Unresolved issues

    Critical Laws:
        - Evidence ≠ Wadh certification
        - Lexicon report is evidence, NOT meaning injection
        - Usage attestation is evidence, NOT UsageGate
        - Reason alone CANNOT certify Arabic Wadh
        - Unknown source/transmission/scope becomes residual
        - Binding trace must be preserved
    """

    source: WadhSource
    transmission_mode: WadhTransmissionMode
    scope: WadhScope
    evidence_content: str
    binding_trace_id: str = ""
    evidence_id: str = ""
    residuals: Tuple[WadhResidual, ...] = ()

    def __post_init__(self):
        """Validate WadhEvidence construction."""
        if not isinstance(self.source, WadhSource):
            raise TypeError("source must be WadhSource")
        if not isinstance(self.transmission_mode, WadhTransmissionMode):
            raise TypeError("transmission_mode must be WadhTransmissionMode")
        if not isinstance(self.scope, WadhScope):
            raise TypeError("scope must be WadhScope")
        if not self.evidence_content:
            raise ValueError("evidence_content is required")

        # Generate evidence_id if not provided
        if not self.evidence_id:
            object.__setattr__(self, "evidence_id", uuid4().hex)

    @property
    def is_source_known(self) -> bool:
        """Check if source is known."""
        return self.source.is_known

    @property
    def is_transmission_known(self) -> bool:
        """Check if transmission mode is known."""
        return self.transmission_mode.is_known

    @property
    def is_scope_known(self) -> bool:
        """Check if scope is known."""
        return self.scope.is_known

    @property
    def has_binding_trace(self) -> bool:
        """Check if binding trace is preserved."""
        return bool(self.binding_trace_id)

    @property
    def has_residuals(self) -> bool:
        """Check if evidence has residuals."""
        return len(self.residuals) > 0

    @property
    def has_blocking_residuals(self) -> bool:
        """Check if evidence has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    @property
    def is_transmitted(self) -> bool:
        """
        Check if evidence is transmitted (not reason alone).

        Critical Law: Arabic Wadh requires transmission.
        """
        return (
            self.source.is_transmitted
            and self.transmission_mode.is_direct
        )

    @property
    def sufficient_for_arabic_wadh(self) -> bool:
        """
        Check if evidence is sufficient for Arabic Wadh claim.

        Critical Law: Requires transmitted source + direct transmission + known scope.
        """
        return (
            self.source.sufficient_for_arabic_wadh
            and self.transmission_mode.sufficient_for_arabic_wadh
            and self.scope.is_known
            and not self.has_blocking_residuals
        )

    @property
    def is_valid(self) -> bool:
        """
        Check if evidence is valid.

        Valid means:
            - source is known
            - transmission mode is known
            - scope is known
            - binding trace preserved
            - no blocking residuals
        """
        return (
            self.is_source_known
            and self.is_transmission_known
            and self.is_scope_known
            and self.has_binding_trace
            and not self.has_blocking_residuals
        )

    def with_residual(self, residual: WadhResidual) -> WadhEvidence:
        """Return new WadhEvidence with additional residual."""
        return WadhEvidence(
            source=self.source,
            transmission_mode=self.transmission_mode,
            scope=self.scope,
            evidence_content=self.evidence_content,
            binding_trace_id=self.binding_trace_id,
            evidence_id=self.evidence_id,
            residuals=self.residuals + (residual,),
        )

    def __str__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        transmitted = "TRANSMITTED" if self.is_transmitted else "NOT_TRANSMITTED"
        return (
            f"WadhEvidence[{status}, {transmitted}]: "
            f"source={self.source.kind.value}, "
            f"mode={self.transmission_mode.kind.value}, "
            f"scope={self.scope.kind.value}"
        )

    def __repr__(self) -> str:
        return (
            f"WadhEvidence(evidence_id='{self.evidence_id}', "
            f"source={self.source.kind.value}, "
            f"residuals={len(self.residuals)})"
        )
