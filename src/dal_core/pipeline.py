"""
DAL Pipeline (خط الدال)

Main pipeline orchestrator: U → A → O → S → F → L → T → D
"""

from dataclasses import dataclass
from typing import Optional

from dal_core.carriers import text_to_carriers
from dal_core.atoms import carriers_to_atoms
from dal_core.d_mufrad import DClosed
from dal_core.residuals import Residual


@dataclass
class DalPipeline:
    """
    خط الدال (DAL Pipeline)

    Orchestrates the full pipeline from text to closed signifier.
    """

    def process(self, text: str) -> tuple[Optional[DClosed], list[Residual]]:
        """
        Process text through the full pipeline.

        Returns (dclosed, all_residuals) tuple.
        """
        all_residuals = []

        # Stage 1: Text → Carriers
        carriers, residuals = text_to_carriers(text)
        all_residuals.extend(residuals)

        # Stage 2: Carriers → Atoms
        atoms, residuals = carriers_to_atoms(carriers)
        all_residuals.extend(residuals)

        # TODO: Implement remaining stages
        # Stage 3: Atoms → Units
        # Stage 4: Units → Context
        # Stage 5: Units → Syllables
        # Stage 6: Syllables → FormCandidate
        # Stage 7: FormCandidate → LughaAttestation
        # Stage 8: LughaAttestation → TypedDal
        # Stage 9: TypedDal → DClosed

        return None, all_residuals
