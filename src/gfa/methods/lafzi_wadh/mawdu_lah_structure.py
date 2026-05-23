"""
MawduLahStructure - بنية الموضوع له

Critical Law:
    الموضوع له بنية لغوية، لا حقيقة خارجية
    Mawdu-lah is linguistic structure, NOT external truth.

MawduLahStructure represents the structured placed-for candidate,
NOT external meaning or truth.

What MawduLahStructure Does:
    - Records structured placed-for candidate
    - Preserves binding trace
    - Preserves Wadh evidence
    - Guards against external meaning injection

What MawduLahStructure Does NOT Do:
    - Does NOT create external meaning
    - Does NOT certify truth
    - Does NOT implement full Dalālah
    - Does NOT classify Mutabaqah/Tadammun/Iltizam
    - Does NOT classify Haqiqah/Majaz/Naql
    - Does NOT issue HUKM

Position in Architecture:
    DalMadlulBindingCandidate (PR-L4, certified)
    └── WadhGeometry (PR-L5A)
        ├── WadhEvidence
        ├── WadhClaim
        └── MawduLahStructure ← THIS MODULE
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
from uuid import uuid4

from .wadh_evidence import WadhEvidence
from .residual_taxonomy import WadhResidual


@dataclass(frozen=True)
class MawduLahStructure:
    """
    Structured placed-for candidate - الموضوع له

    This represents what a term is conventionally placed-for,
    as a linguistic structure, NOT as external truth or meaning.

    Critical Properties:
        - structure_form: The linguistic structure
        - wadh_evidence: Evidence for this placement
        - binding_trace_id: Preserved from binding candidate
        - structure_id: Unique identifier
        - residuals: Unresolved issues

    Critical Laws:
        - MawduLahStructure is linguistic structure, NOT external truth
        - MawduLahStructure is NOT external meaning
        - MawduLahStructure does NOT certify semantics
        - MawduLahStructure preserves binding trace
        - MawduLahStructure does NOT create Dalālah
        - MawduLahStructure does NOT classify Mutabaqah/Tadammun/Iltizam
        - MawduLahStructure does NOT classify Haqiqah/Majaz/Naql
    """

    structure_form: str
    wadh_evidence: WadhEvidence
    binding_trace_id: str = ""
    structure_id: str = ""
    residuals: Tuple[WadhResidual, ...] = ()

    def __post_init__(self):
        """Validate MawduLahStructure construction."""
        if not self.structure_form:
            raise ValueError("structure_form is required")
        if not isinstance(self.wadh_evidence, WadhEvidence):
            raise TypeError("wadh_evidence must be WadhEvidence")

        # Generate structure_id if not provided
        if not self.structure_id:
            object.__setattr__(self, "structure_id", uuid4().hex)

        # Preserve binding_trace_id from evidence if not provided
        if not self.binding_trace_id and self.wadh_evidence.binding_trace_id:
            object.__setattr__(self, "binding_trace_id", self.wadh_evidence.binding_trace_id)

    @property
    def has_binding_trace(self) -> bool:
        """Check if binding trace is preserved."""
        return bool(self.binding_trace_id)

    @property
    def has_valid_evidence(self) -> bool:
        """Check if Wadh evidence is valid."""
        return self.wadh_evidence.is_valid

    @property
    def has_residuals(self) -> bool:
        """Check if structure has residuals."""
        return len(self.residuals) > 0

    @property
    def has_blocking_residuals(self) -> bool:
        """Check if structure has blocking residuals."""
        return any(r.is_blocker for r in self.residuals)

    @property
    def is_transmitted(self) -> bool:
        """Check if underlying evidence is transmitted."""
        return self.wadh_evidence.is_transmitted

    @property
    def is_valid(self) -> bool:
        """
        Check if structure is valid.

        Valid means:
            - structure_form exists
            - wadh_evidence is valid
            - binding trace preserved
            - no blocking residuals
        """
        return (
            bool(self.structure_form)
            and self.has_valid_evidence
            and self.has_binding_trace
            and not self.has_blocking_residuals
        )

    def with_residual(self, residual: WadhResidual) -> MawduLahStructure:
        """Return new MawduLahStructure with additional residual."""
        return MawduLahStructure(
            structure_form=self.structure_form,
            wadh_evidence=self.wadh_evidence,
            binding_trace_id=self.binding_trace_id,
            structure_id=self.structure_id,
            residuals=self.residuals + (residual,),
        )

    def __str__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        return (
            f"MawduLahStructure[{status}]: '{self.structure_form}' "
            f"(evidence={self.wadh_evidence.source.kind.value}, "
            f"residuals={len(self.residuals)})"
        )

    def __repr__(self) -> str:
        return (
            f"MawduLahStructure(structure_id='{self.structure_id}', "
            f"form='{self.structure_form}', "
            f"residuals={len(self.residuals)})"
        )
