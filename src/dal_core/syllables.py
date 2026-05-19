"""
Syllable Contract (عقد المقطع)

Contract 5: OperativeUnits → Syllables
Folds units into prosodic syllables (CV, CVC, CVV, CVVC, CVCC).
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from dal_core.atoms import ArabicAtom, AtomKind
from dal_core.units import OperativeUnit
from dal_core.residuals import Residual, make_blocker, make_warning, ResidualType


class SyllableType(Enum):
    """أنواع المقاطع (Syllable Types)"""
    CV = "قصير مفتوح"      # Short open: consonant + short vowel
    CVC = "قصير مغلق"      # Short closed: consonant + short vowel + consonant
    CVV = "طويل مفتوح"     # Long open: consonant + long vowel
    CVVC = "طويل مغلق"     # Long closed: consonant + long vowel + consonant
    CVCC = "فائق الطول"    # Super heavy: consonant + vowel + consonant + consonant


@dataclass
class Syllable:
    """
    مقطع (Syllable)

    Prosodic syllable unit.

    Structure:
    - onset: Consonant(s)
    - nucleus: Vowel(s)
    - coda: Optional consonant(s)
    """
    type: SyllableType
    onset: list[ArabicAtom] = field(default_factory=list)
    nucleus: list[ArabicAtom] = field(default_factory=list)
    coda: list[ArabicAtom] = field(default_factory=list)
    units: list[OperativeUnit] = field(default_factory=list)
    residuals: list[Residual] = field(default_factory=list)
    trace: dict = field(default_factory=dict)

    def __str__(self) -> str:
        return f"Syllable({self.type.value})"

    def to_text(self) -> str:
        """Reconstruct syllable text from atoms"""
        all_atoms = self.onset + self.nucleus + self.coda
        return ''.join(a.carrier.char for a in all_atoms)


def handle_shadda(atom: ArabicAtom, base_letter: ArabicAtom) -> tuple[list[ArabicAtom], dict]:
    """
    Handle shadda (gemination).

    Theorem: Shadda = doubled consonant effect

    Returns: (expanded_atoms, trace)
    """
    if atom.kind != AtomKind.SHADDA:
        return [atom], {}

    # Shadda represents gemination (doubling)
    # Trace the expansion
    trace = {
        'shadda_position': atom.carrier.index,
        'base_letter': base_letter.carrier.char,
        'effect': 'gemination',
        'expansion': f"{base_letter.carrier.char} + {base_letter.carrier.char}"
    }

    # Return shadda marker (keep for trace, don't duplicate letter yet)
    return [atom], trace


def handle_tanwin(atom: ArabicAtom) -> tuple[ArabicAtom, dict]:
    """
    Handle tanwin (nunation).

    Theorem: Tanwin = operational marker (not semantic)

    Returns: (atom, trace)
    """
    if atom.kind != AtomKind.TANWIN:
        return atom, {}

    trace = {
        'tanwin_type': atom.features.get('name', 'UNKNOWN'),
        'position': atom.carrier.index,
        'effect': 'nunation marker',
        'operational': True,  # Operational, not semantic
    }

    return atom, trace


def handle_sukun(atom: ArabicAtom, position: str) -> list[Residual]:
    """
    Handle sukun (absence of vowel).

    Theorem: Sukun closes syllable.

    Returns: residuals (if any)
    """
    residuals = []

    if atom.kind != AtomKind.SUKUN:
        return residuals

    # Sukun is valid in:
    # 1. Coda position (closes syllable)
    # 2. End of word (waqf)
    # Invalid in:
    # 1. Word-initial position (onset cannot be sukun)

    if position == 'onset':
        residuals.append(make_blocker(
            ResidualType.INVALID_SYLLABLE_PATTERN,
            "Sukun cannot appear in syllable onset",
            location=f"position {atom.carrier.index}"
        ))

    return residuals


def is_long_vowel_sequence(atoms: list[ArabicAtom], start_idx: int) -> bool:
    """
    Check if atoms form a long vowel (madd) sequence.

    Long vowels:
    - ا (alif) after fatha
    - و (waw) after damma
    - ي (ya) after kasra
    """
    if start_idx >= len(atoms) - 1:
        return False

    vowel = atoms[start_idx]
    letter = atoms[start_idx + 1]

    if vowel.kind != AtomKind.VOWEL or letter.kind != AtomKind.LETTER:
        return False

    vowel_name = vowel.features.get('name', '')
    letter_char = letter.carrier.char

    # Check valid long vowel combinations
    if vowel_name == 'FATHA' and letter_char in ('ا', 'ى'):  # alif/alif maqsurah
        return True
    if vowel_name == 'DAMMA' and letter_char == 'و':  # waw
        return True
    if vowel_name == 'KASRA' and letter_char == 'ي':  # ya
        return True

    return False


def handle_madd(atoms: list[ArabicAtom], start_idx: int) -> tuple[list[ArabicAtom], dict]:
    """
    Handle madd (long vowel).

    Theorem: Madd lengthens syllable nucleus.

    Returns: (nucleus_atoms, trace)
    """
    if not is_long_vowel_sequence(atoms, start_idx):
        return [atoms[start_idx]], {}

    vowel = atoms[start_idx]
    letter = atoms[start_idx + 1]

    trace = {
        'madd_type': f"{vowel.features.get('name')} + {letter.carrier.char}",
        'effect': 'syllable lengthening',
        'nucleus_atoms': [vowel.carrier.char, letter.carrier.char]
    }

    return [vowel, letter], trace


def parse_syllables(units: list[OperativeUnit]) -> tuple[list[Syllable], list[Residual]]:
    """
    Parse operative units into syllables.

    Returns: (syllables, residuals)
    """
    syllables = []
    all_residuals = []

    # TODO: Full syllabification algorithm
    # For now, simple placeholder that preserves structure

    if not units:
        return syllables, all_residuals

    # Preserve units as trace
    trace = {
        'input_units': len(units),
        'method': 'placeholder_syllabification'
    }

    # Create a simple syllable wrapper (to be expanded)
    syllable = Syllable(
        type=SyllableType.CV,  # Default
        units=units,
        trace=trace
    )

    syllables.append(syllable)

    return syllables, all_residuals


def validate_syllable_pattern(syllable: Syllable) -> list[Residual]:
    """
    Validate syllable pattern.

    Returns: residuals (if invalid)
    """
    residuals = []

    # Basic validation
    if not syllable.onset and not syllable.nucleus:
        residuals.append(make_blocker(
            ResidualType.INVALID_SYLLABLE,
            "Syllable must have at least onset or nucleus",
            location="syllable structure"
        ))

    # Validate type matches structure
    # TODO: Full validation logic

    return residuals
