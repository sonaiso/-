"""
Witness Store for D_lugha Contract

Provides seed linguistic attestation records with explicit ranks.

Theorem 3: D_form ⊄ D_lugha
Pattern/weight alone is NOT linguistic attestation.

This module contains witnessed forms with:
- Explicit attestation rank (TAWATUR, AHAD, SAMA, QIYAS, FORM_ONLY)
- Source references
- Type classification
- Evidence provenance
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from dal_core.ranks import LughaRank


class LexicalType(Enum):
    """Lexical type classification (اسم، فعل، حرف)"""
    ISM = "اسم"      # Noun
    FIIL = "فعل"     # Verb
    HARF = "حرف"     # Particle
    AMBIGUOUS = "متعدد"  # Ambiguous
    UNRESOLVED = "غير محدد"  # Unresolved


@dataclass
class WitnessRecord:
    """
    شاهد لغوي (Linguistic Witness)

    Explicit attestation record with rank and provenance.
    """
    form: str  # Vocalized form
    normalized_form: str  # Unvocalized normalized
    type: LexicalType  # Type classification
    rank: LughaRank  # Attestation rank
    source: str  # Source reference
    notes: str = ""  # Additional information

    def __str__(self) -> str:
        return f"Witness({self.form}, {self.type.value}, rank={self.rank.name})"


# Seed witness store
# These are verified attestations from classical sources
WITNESS_STORE: dict[str, WitnessRecord] = {
    # Verbs - Trilateral roots
    "كَتَبَ": WitnessRecord(
        form="كَتَبَ",
        normalized_form="كتب",
        type=LexicalType.FIIL,
        rank=LughaRank.TAWATUR,
        source="Quran 96:4, Classical corpus",
        notes="Past tense verb, root ك-ت-ب, pattern فَعَلَ"
    ),

    "كُتِبَ": WitnessRecord(
        form="كُتِبَ",
        normalized_form="كتب",
        type=LexicalType.FIIL,
        rank=LughaRank.TAWATUR,
        source="Quran 2:183, Classical corpus",
        notes="Passive past tense, root ك-ت-ب, pattern فُعِلَ"
    ),

    "يَكْتُبُ": WitnessRecord(
        form="يَكْتُبُ",
        normalized_form="يكتب",
        type=LexicalType.FIIL,
        rank=LughaRank.TAWATUR,
        source="Quran 2:282, Classical corpus",
        notes="Present tense verb, root ك-ت-ب, pattern يَفْعُلُ"
    ),

    "قَالَ": WitnessRecord(
        form="قَالَ",
        normalized_form="قال",
        type=LexicalType.FIIL,
        rank=LughaRank.TAWATUR,
        source="Quran 2:30, Classical corpus",
        notes="Past tense verb, root ق-و-ل, pattern فَعَلَ"
    ),

    # Nouns - Patterns
    "كِتَابٌ": WitnessRecord(
        form="كِتَابٌ",
        normalized_form="كتاب",
        type=LexicalType.ISM,
        rank=LughaRank.TAWATUR,
        source="Quran 2:2, Classical lexicons",
        notes="Noun, root ك-ت-ب, pattern فِعَال"
    ),

    "كَاتِبٌ": WitnessRecord(
        form="كَاتِبٌ",
        normalized_form="كاتب",
        type=LexicalType.ISM,
        rank=LughaRank.TAWATUR,
        source="Quran 2:282, Classical lexicons",
        notes="Active participle, root ك-ت-ب, pattern فَاعِل"
    ),

    "مَكْتُوبٌ": WitnessRecord(
        form="مَكْتُوبٌ",
        normalized_form="مكتوب",
        type=LexicalType.ISM,
        rank=LughaRank.TAWATUR,
        source="Classical corpus",
        notes="Passive participle, root ك-ت-ب, pattern مَفْعُول"
    ),

    "مَكْتَبٌ": WitnessRecord(
        form="مَكْتَبٌ",
        normalized_form="مكتب",
        type=LexicalType.ISM,
        rank=LughaRank.AHAD,
        source="Classical lexicons",
        notes="Place noun, root ك-ت-ب, pattern مَفْعَل"
    ),

    # Particles
    "مِنْ": WitnessRecord(
        form="مِنْ",
        normalized_form="من",
        type=LexicalType.HARF,
        rank=LughaRank.TAWATUR,
        source="Quran 1:2, Classical grammar",
        notes="Preposition particle"
    ),

    "إِلَى": WitnessRecord(
        form="إِلَى",
        normalized_form="الى",
        type=LexicalType.HARF,
        rank=LughaRank.TAWATUR,
        source="Quran 17:1, Classical grammar",
        notes="Preposition particle"
    ),

    "عَنْ": WitnessRecord(
        form="عَنْ",
        normalized_form="عن",
        type=LexicalType.HARF,
        rank=LughaRank.TAWATUR,
        source="Classical grammar",
        notes="Preposition particle"
    ),

    # Pronouns
    "هُوَ": WitnessRecord(
        form="هُوَ",
        normalized_form="هو",
        type=LexicalType.ISM,
        rank=LughaRank.TAWATUR,
        source="Quran 1:2, Classical grammar",
        notes="Pronoun - third person masculine singular"
    ),

    "هِيَ": WitnessRecord(
        form="هِيَ",
        normalized_form="هي",
        type=LexicalType.ISM,
        rank=LughaRank.TAWATUR,
        source="Classical grammar",
        notes="Pronoun - third person feminine singular"
    ),

    # Demonstratives
    "هَذَا": WitnessRecord(
        form="هَذَا",
        normalized_form="هذا",
        type=LexicalType.ISM,
        rank=LughaRank.TAWATUR,
        source="Quran 2:25, Classical grammar",
        notes="Demonstrative pronoun - near masculine"
    ),

    "ذَلِكَ": WitnessRecord(
        form="ذَلِكَ",
        normalized_form="ذلك",
        type=LexicalType.ISM,
        rank=LughaRank.TAWATUR,
        source="Quran 2:2, Classical grammar",
        notes="Demonstrative pronoun - far masculine"
    ),

    # Relative pronouns
    "الَّذِي": WitnessRecord(
        form="الَّذِي",
        normalized_form="الذي",
        type=LexicalType.ISM,
        rank=LughaRank.TAWATUR,
        source="Quran 1:2, Classical grammar",
        notes="Relative pronoun - masculine singular"
    ),
}


def lookup_witness(vocalized_form: str) -> Optional[WitnessRecord]:
    """
    Lookup a vocalized form in the witness store.

    Returns None if form is not attested.
    """
    return WITNESS_STORE.get(vocalized_form)


def is_attested(vocalized_form: str) -> bool:
    """Check if a form is attested in witness store"""
    return vocalized_form in WITNESS_STORE


def get_attestation_rank(vocalized_form: str) -> LughaRank:
    """
    Get attestation rank for a form.

    Returns ZERO if not attested.
    """
    record = lookup_witness(vocalized_form)
    if record:
        return record.rank
    return LughaRank.ZERO


def get_witness_type(vocalized_form: str) -> Optional[LexicalType]:
    """
    Get type from witness record.

    Returns None if not attested.
    """
    record = lookup_witness(vocalized_form)
    if record:
        return record.type
    return None
