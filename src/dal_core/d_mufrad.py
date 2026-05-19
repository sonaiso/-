"""
D_mufrad Contract (عقد المفرد الدالي)

Contract 9: TypedDal → DClosed
Closes the signifier unit WITHOUT semantic meaning.

CRITICAL UPDATE (Phase 2.5):
D_mufrad now includes MorphProof for composition readiness.
Without morphological proof, the unit is lexically closed but not composition-ready.
"""

from dataclasses import dataclass, field
from typing import Optional

from dal_core.d_type import TypedDal, DalType
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, has_blocking_residuals
from dal_core.morph_proof import MorphProof


@dataclass(frozen=True)
class DClosed:
    """
    دال مغلق (Closed Signifier)

    Final closed signifier unit with two levels of closure:

    1. LEXICAL CLOSURE (D_form + D_lugha + D_type)
       - Ready for lexical/dictionary use
       - Ready for وضع (conventional sign pairing)

    2. COMPOSITION CLOSURE (+ MorphProof + SurfaceProof)
       - Ready for compositional syntax
       - Required for D_murakkab (compositional analysis)

    CRITICAL CONSTRAINT (المبرهنة 5):
    This class does NOT contain fields: meaning, murad, haqiqa_majaz.
    This system deals with الدال وحده (signifier alone).

    MorphProof contains morphological SIGNIFIER features, NOT semantic meanings.
    The absence of semantic fields enforces that no semantic information
    can ever be stored in a DClosed instance.
    """
    typed_dal: TypedDal
    morph_proof: Optional[MorphProof] = None  # NEW: Morphological proof for composition
    is_mufrad: bool = True              # عدم تركيب إسنادي داخلي
    is_placeable: bool = True           # صلاحية للوضع
    final_rank: LughaRank = LughaRank.ZERO
    all_residuals: tuple[Residual, ...] = field(default_factory=tuple)
    full_trace: dict = field(default_factory=dict)

    def is_closed(self) -> bool:
        """
        Check if signifier is fully closed for LEXICAL use.

        Lexical closure conditions:
        - Attested in Arabic
        - Has determinate type
        - Is mufrad (single unit)
        - No blocking residuals

        NOTE: This does NOT check composition readiness.
        Use is_composition_ready() for that.
        """
        return (
            self.typed_dal.attestation.is_arabic and
            self.typed_dal.dal_type != DalType.AMBIGUOUS and
            self.is_mufrad and
            not has_blocking_residuals(list(self.all_residuals))
        )

    def is_composition_ready(self) -> bool:
        """
        Check if signifier is ready for compositional analysis.

        Composition readiness requires:
        - Lexical closure (is_closed() == True)
        - MorphProof present and composition-ready
        - No blocker residuals in morph_proof

        THEOREM: No compositional certificate over morphologically incomplete mufrad.
        Cert(D_murakkab) ⟹ MorphClosed(D_mufrad_i) for all i
        """
        # Must be lexically closed first
        if not self.is_closed():
            return False

        # Must have morphological proof
        if self.morph_proof is None:
            return False

        # MorphProof must be composition-ready
        return self.morph_proof.is_composition_ready()

    def __str__(self) -> str:
        status = "closed" if self.is_closed() else "open"
        return f"DClosed({self.typed_dal.attestation.form.vocalization}, {status})"
