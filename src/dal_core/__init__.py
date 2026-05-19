"""
DAL Core - الدال وحده
Signifier-Only Analysis System following Nabahani methodology

This module implements برهان الدال وحده (proof of signifier alone)
without mixing meaning (المعنى) or intent (المراد).

Pipeline: U → A → O → S → F → L → T → D

Core principle: No semantic meaning fields in any output.
"""

__version__ = "0.1.0"

from dal_core.carriers import Carrier
from dal_core.atoms import ArabicAtom, AtomKind
from dal_core.units import OperativeUnit
from dal_core.context import UnitContext
from dal_core.syllables import Syllable, SyllableType
from dal_core.d_form import FormCandidate
from dal_core.d_lugha import LughaAttestation, LughaRank
from dal_core.d_type import TypedDal, DalType
from dal_core.d_mufrad import DClosed
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, ResidualSeverity, ResidualType
from dal_core.pipeline import DalPipeline

__all__ = [
    "Carrier",
    "ArabicAtom",
    "AtomKind",
    "OperativeUnit",
    "UnitContext",
    "Syllable",
    "SyllableType",
    "FormCandidate",
    "LughaAttestation",
    "LughaRank",
    "TypedDal",
    "DalType",
    "DClosed",
    "Residual",
    "ResidualSeverity",
    "ResidualType",
    "DalPipeline",
]
