"""
ArabicAtom Contract (عقد الذرة العربية)

Contract 2: Carrier → ArabicAtom
Classifies carriers into atomic units: letters, vowels, marks, etc.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from dal_core.carriers import Carrier
from dal_core.residuals import Residual, make_blocker, make_warning, ResidualType
from dal_core.evidence import Evidence, make_evidence


class AtomKind(Enum):
    """
    نوع الذرة (Atom Kind)

    Classification of Arabic atomic units.
    """
    LETTER = "حرف"           # Consonant letter
    VOWEL = "حركة"           # Short vowel (fatha, damma, kasra)
    SUKUN = "سكون"           # Sukun (no vowel)
    SHADDA = "شدة"           # Shadda (gemination)
    TANWIN = "تنوين"         # Tanwin (nunation)
    MADD = "مد"              # Long vowel (alif, waw, ya)
    MARK = "علامة"           # Other diacritic mark
    HAMZA = "همزة"           # Hamza (glottal stop)
    SPACE = "فراغ"           # Whitespace
    PUNCT = "ترقيم"          # Punctuation
    UNKNOWN = "مجهول"        # Unknown/unclassified


@dataclass
class ArabicAtom:
    """
    ذرة عربية (Arabic Atom)

    Smallest classified unit in Arabic text.
    NOT a letter until classified as such.

    Enforces principle: ك ≠ "number 22", ك = Atom with recoverable features
    """
    kind: AtomKind
    carrier: Carrier
    features: dict = field(default_factory=dict)
    evidence: list[Evidence] = field(default_factory=list)
    rank: float = 1.0  # Confidence [0, 1]
    residuals: list[Residual] = field(default_factory=list)

    def is_letter(self) -> bool:
        """Check if this atom is a letter"""
        return self.kind == AtomKind.LETTER

    def is_vowel(self) -> bool:
        """Check if this atom is a vowel"""
        return self.kind == AtomKind.VOWEL

    def is_mark(self) -> bool:
        """Check if this atom is a diacritic mark"""
        return self.kind in {AtomKind.VOWEL, AtomKind.SUKUN, AtomKind.SHADDA,
                             AtomKind.TANWIN, AtomKind.MARK}

    def __str__(self) -> str:
        return f"Atom({self.carrier.char!r}:{self.kind.value})"

    def __repr__(self) -> str:
        return self.__str__()


# Arabic letter classification
ARABIC_LETTERS = {
    # Letters (28 + hamza + alif maqsurah)
    'ا': ('ALIF', {}),
    'ب': ('BA', {}),
    'ت': ('TA', {}),
    'ث': ('THA', {}),
    'ج': ('JIM', {}),
    'ح': ('HAH', {}),
    'خ': ('KHA', {}),
    'د': ('DAL', {}),
    'ذ': ('DHAL', {}),
    'ر': ('RA', {}),
    'ز': ('ZAY', {}),
    'س': ('SIN', {}),
    'ش': ('SHIN', {}),
    'ص': ('SAD', {}),
    'ض': ('DAD', {}),
    'ط': ('TAH', {}),
    'ظ': ('ZAH', {}),
    'ع': ('AIN', {}),
    'غ': ('GHAIN', {}),
    'ف': ('FA', {}),
    'ق': ('QAF', {}),
    'ك': ('KAF', {}),
    'ل': ('LAM', {}),
    'م': ('MIM', {}),
    'ن': ('NUN', {}),
    'ه': ('HA', {}),
    'و': ('WAW', {}),
    'ي': ('YA', {}),
    'ى': ('ALIF_MAQSURAH', {}),
    'ء': ('HAMZA', {}),
    'أ': ('ALIF_HAMZA_ABOVE', {}),
    'إ': ('ALIF_HAMZA_BELOW', {}),
    'ؤ': ('WAW_HAMZA', {}),
    'ئ': ('YA_HAMZA', {}),
    'ة': ('TA_MARBUTA', {}),
}

# Vowels and diacritics
ARABIC_MARKS = {
    '\u064B': (AtomKind.TANWIN, 'FATHATAN', {}),     # ً
    '\u064C': (AtomKind.TANWIN, 'DAMMATAN', {}),     # ٌ
    '\u064D': (AtomKind.TANWIN, 'KASRATAN', {}),     # ٍ
    '\u064E': (AtomKind.VOWEL, 'FATHA', {}),         # َ
    '\u064F': (AtomKind.VOWEL, 'DAMMA', {}),         # ُ
    '\u0650': (AtomKind.VOWEL, 'KASRA', {}),         # ِ
    '\u0651': (AtomKind.SHADDA, 'SHADDA', {}),       # ّ
    '\u0652': (AtomKind.SUKUN, 'SUKUN', {}),         # ْ
    '\u0653': (AtomKind.MARK, 'MADDAH', {}),         # ٓ
    '\u0654': (AtomKind.MARK, 'HAMZA_ABOVE', {}),    # ٔ
    '\u0655': (AtomKind.MARK, 'HAMZA_BELOW', {}),    # ٕ
    '\u0656': (AtomKind.MARK, 'SUBSCRIPT_ALIF', {}), # ٖ
    '\u0670': (AtomKind.MARK, 'SUPERSCRIPT_ALIF', {}), # ٰ
}


def classify_carrier(carrier: Carrier) -> tuple[Optional[ArabicAtom], list[Residual]]:
    """
    Classify a carrier into an ArabicAtom.

    Returns (atom, residuals) tuple.
    """
    residuals = []
    char = carrier.char

    # Check for letter
    if char in ARABIC_LETTERS:
        name, features = ARABIC_LETTERS[char]
        atom = ArabicAtom(
            kind=AtomKind.LETTER,
            carrier=carrier,
            features={'name': name, **features},
            evidence=[make_evidence(
                "ARABIC_LETTERS table",
                f"Character {char!r} classified as letter {name}"
            )],
            rank=1.0
        )
        return atom, residuals

    # Check for mark/vowel/diacritic
    if char in ARABIC_MARKS:
        kind, name, features = ARABIC_MARKS[char]
        atom = ArabicAtom(
            kind=kind,
            carrier=carrier,
            features={'name': name, **features},
            evidence=[make_evidence(
                "ARABIC_MARKS table",
                f"Character {char!r} classified as {kind.value} {name}"
            )],
            rank=1.0
        )
        return atom, residuals

    # Check for whitespace
    if char.isspace():
        atom = ArabicAtom(
            kind=AtomKind.SPACE,
            carrier=carrier,
            features={'type': 'whitespace'},
            evidence=[make_evidence(
                "Unicode category",
                "Character is whitespace"
            )],
            rank=1.0
        )
        return atom, residuals

    # Unknown atom - create with blocker residual
    residuals.append(make_blocker(
        ResidualType.UNKNOWN_ATOM,
        f"Cannot classify character {char!r} (U+{carrier.codepoint:04X})",
        location=f"index {carrier.index}",
        codepoint=carrier.codepoint
    ))

    atom = ArabicAtom(
        kind=AtomKind.UNKNOWN,
        carrier=carrier,
        features={},
        evidence=[make_evidence(
            "classification failure",
            f"Character {char!r} not in known tables",
            confidence=0.0
        )],
        rank=0.0,
        residuals=residuals
    )

    return atom, residuals


def carriers_to_atoms(carriers: list[Carrier]) -> tuple[list[ArabicAtom], list[Residual]]:
    """
    Convert carriers to atoms.

    Returns (atoms, all_residuals) tuple.
    Skips carriers that produce blocking residuals.
    """
    atoms = []
    all_residuals = []

    for carrier in carriers:
        atom, residuals = classify_carrier(carrier)
        all_residuals.extend(residuals)

        if atom is not None and not any(r.is_blocker() for r in residuals):
            atoms.append(atom)

    return atoms, all_residuals
