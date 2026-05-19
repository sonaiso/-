"""
D_mufrad Contract (عقد المفرد الدالي)

Contract 9: TypedDal → DClosed
Closes the signifier unit WITHOUT semantic meaning.
"""

from dataclasses import dataclass, field
from typing import Optional

from dal_core.d_type import TypedDal, DalType
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, has_blocking_residuals


@dataclass
class DClosed:
    """
    دال مغلق (Closed Signifier)

    Final closed signifier unit ready for eventual وضع (conventional sign).

    CRITICAL CONSTRAINT (المبرهنة 5):
    meaning, murad, haqiqa_majaz MUST be None.
    This system deals with الدال وحده (signifier alone).
    """
    typed_dal: TypedDal
    is_mufrad: bool = True              # عدم تركيب إسنادي داخلي
    is_placeable: bool = True           # صلاحية للوضع
    final_rank: LughaRank = LughaRank.ZERO
    all_residuals: list[Residual] = field(default_factory=list)
    full_trace: dict = field(default_factory=dict)

    # ENFORCED CONSTRAINTS - MUST be None
    meaning: None = None                # MUST be None
    murad: None = None                  # MUST be None
    haqiqa_majaz: None = None          # MUST be None

    def __post_init__(self):
        """Enforce constraints"""
        # Theorem 5: No meaning in dal
        if self.meaning is not None:
            raise ValueError("DClosed.meaning MUST be None (Theorem 5)")
        if self.murad is not None:
            raise ValueError("DClosed.murad MUST be None (Theorem 5)")
        if self.haqiqa_majaz is not None:
            raise ValueError("DClosed.haqiqa_majaz MUST be None (Theorem 5)")

    def is_closed(self) -> bool:
        """
        Check if signifier is fully closed.

        Closure conditions:
        - Attested in Arabic
        - Has determinate type
        - Is mufrad (single unit)
        - No blocking residuals
        - No meaning/murad/haqiqa_majaz
        """
        return (
            self.typed_dal.attestation.is_arabic and
            self.typed_dal.dal_type != DalType.AMBIGUOUS and
            self.is_mufrad and
            not has_blocking_residuals(self.all_residuals) and
            self.meaning is None and
            self.murad is None and
            self.haqiqa_majaz is None
        )

    def __str__(self) -> str:
        status = "closed" if self.is_closed() else "open"
        return f"DClosed({self.typed_dal.attestation.form.vocalization}, {status})"
