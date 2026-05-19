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


@dataclass(frozen=True)
class DClosed:
    """
    دال مغلق (Closed Signifier)

    Final closed signifier unit ready for eventual وضع (conventional sign).

    CRITICAL CONSTRAINT (المبرهنة 5):
    This class does NOT contain fields: meaning, murad, haqiqa_majaz.
    This system deals with الدال وحده (signifier alone).

    The absence of these fields enforces that no semantic information
    can ever be stored in a DClosed instance.
    """
    typed_dal: TypedDal
    is_mufrad: bool = True              # عدم تركيب إسنادي داخلي
    is_placeable: bool = True           # صلاحية للوضع
    final_rank: LughaRank = LughaRank.ZERO
    all_residuals: tuple[Residual, ...] = field(default_factory=tuple)
    full_trace: dict = field(default_factory=dict)

    def is_closed(self) -> bool:
        """
        Check if signifier is fully closed.

        Closure conditions:
        - Attested in Arabic
        - Has determinate type
        - Is mufrad (single unit)
        - No blocking residuals
        """
        return (
            self.typed_dal.attestation.is_arabic and
            self.typed_dal.dal_type != DalType.AMBIGUOUS and
            self.is_mufrad and
            not has_blocking_residuals(list(self.all_residuals))
        )

    def __str__(self) -> str:
        status = "closed" if self.is_closed() else "open"
        return f"DClosed({self.typed_dal.attestation.form.vocalization}, {status})"
