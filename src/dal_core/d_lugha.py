"""
D_lugha Contract (عقد الثبوت اللغوي)

Contract 7: FormCandidate → LughaAttestation
Attests forms through رواية، سماع، قياس (transmission, hearing, analogy).
"""

from dataclasses import dataclass, field

from dal_core.d_form import FormCandidate
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual


@dataclass
class LughaAttestation:
    """
    ثبوت لغوي (Linguistic Attestation)

    Proves Arabic authenticity through:
    - تواتر (mass transmission)
    - آحاد (singular transmission)
    - سماع (specific hearing)
    - قياس (permitted analogy)

    المبدأ: العربية بالرواية والسماع، لا بالوزن وحده
    """
    form: FormCandidate
    rank: LughaRank = LughaRank.ZERO
    sources: list[str] = field(default_factory=list)
    is_arabic: bool = False
    residuals: list[Residual] = field(default_factory=list)
    trace: dict = field(default_factory=dict)

    def __str__(self) -> str:
        return f"Lugha({self.form.vocalization}, rank={self.rank.name})"
