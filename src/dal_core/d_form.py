"""
D_form Contract (عقد الصورة)

Contract 6: Syllables → FormCandidate
Produces form candidates without linguistic attestation.
"""

from dataclasses import dataclass, field

from dal_core.syllables import Syllable
from dal_core.ranks import FormRank
from dal_core.residuals import Residual


@dataclass
class FormCandidate:
    """
    مرشح صوري (Form Candidate)

    A morphological form candidate.
    D_form ⊄ D_lugha (pattern alone doesn't prove Arabic attestation)
    """
    text: str
    vocalization: str
    syllables: list[Syllable] = field(default_factory=list)
    morph_shape: str = ""
    rank: FormRank = FormRank.FORM
    residuals: list[Residual] = field(default_factory=list)
    trace: dict = field(default_factory=dict)

    def __str__(self) -> str:
        return f"Form({self.vocalization})"
