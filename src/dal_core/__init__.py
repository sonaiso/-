"""
DAL Core - الدال وحده
Signifier-Only Analysis System following Nabahani methodology

This module implements برهان الدال وحده (proof of signifier alone)
without mixing meaning (المعنى) or intent (المراد).

Phase 0/1 Implementation Status:
- ✅ Contract 1: Unicode Carrier (complete)
- ✅ Contract 2: ArabicAtom (complete)
- ✅ Contract 3: OperativeUnit (complete)
- ⚠️ Contract 4-9: Data structures defined, logic incomplete

Core principle: No semantic meaning fields in any output.
"""

__version__ = "0.1.0"

# Phase 0/1: Fully implemented contracts
from dal_core.carriers import Carrier, make_carrier, text_to_carriers
from dal_core.atoms import ArabicAtom, AtomKind, classify_carrier, carriers_to_atoms
from dal_core.units import OperativeUnit, make_unit
from dal_core.residuals import Residual, ResidualSeverity, ResidualType
from dal_core.ranks import LughaRank, FormRank
from dal_core.evidence import Evidence, make_evidence

# Future phases: Data structures only (not fully implemented)
from dal_core.context import UnitContext
from dal_core.syllables import Syllable, SyllableType
from dal_core.d_form import FormCandidate
from dal_core.d_lugha import LughaAttestation
from dal_core.d_type import TypedDal, DalType
from dal_core.d_mufrad import DClosed
from dal_core.pipeline import DalPipeline

__all__ = [
    # Phase 0/1: Complete implementations
    "Carrier",
    "make_carrier",
    "text_to_carriers",
    "ArabicAtom",
    "AtomKind",
    "classify_carrier",
    "carriers_to_atoms",
    "OperativeUnit",
    "make_unit",
    "Residual",
    "ResidualSeverity",
    "ResidualType",
    "Evidence",
    "make_evidence",
    "LughaRank",
    "FormRank",

    # Future phases: Data structures
    "UnitContext",
    "Syllable",
    "SyllableType",
    "FormCandidate",
    "LughaAttestation",
    "TypedDal",
    "DalType",
    "DClosed",
    "DalPipeline",
]
