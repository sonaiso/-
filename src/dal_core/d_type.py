"""
D_type Contract (عقد النوع)

Contract 8: LughaAttestation → TypedDal
Classifies into اسم، فعل، حرف (noun, verb, particle).
"""

from dataclasses import dataclass, field
from enum import Enum

from dal_core.d_lugha import LughaAttestation
from dal_core.residuals import Residual


class DalType(Enum):
    """أنواع الدوال (Signifier Types)"""
    ISM = "اسم"        # Noun
    FIIL = "فعل"       # Verb
    HARF = "حرف"       # Particle
    AMBIGUOUS = "ملتبس"  # Ambiguous


@dataclass
class TypedDal:
    """
    دال منوّع (Typed Signifier)

    Classified signifier without semantic meaning.
    """
    attestation: LughaAttestation
    dal_type: DalType = DalType.AMBIGUOUS
    type_evidence: list[str] = field(default_factory=list)
    residuals: list[Residual] = field(default_factory=list)
    trace: dict = field(default_factory=dict)

    def __str__(self) -> str:
        return f"TypedDal({self.attestation.form.vocalization}, type={self.dal_type.value})"
