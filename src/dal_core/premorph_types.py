"""Pre-Morphological Types for D2 Domain.

Supporting types for pre-morphological unit candidates.

These types describe segmentation structures BEFORE:
- Root extraction (D3: ORIGIN)
- Pattern matching (D4: TEMPLATE)
- Identity classification (D5: IDENTITY_AXIS)
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum, auto


class CliticType(Enum):
    """Types of clitics."""
    PROCLITIC = auto()   # Prefix clitics (و، ف، ل، ب...)
    ENCLITIC = auto()    # Suffix clitics (ني، ك، ه، ها...)


class CliticForm(Enum):
    """Specific clitic forms (examples)."""
    # Proclitics
    WAW = "و"           # Conjunction
    FA = "ف"            # Then/so
    LAM = "ل"           # To/for
    BA = "ب"            # In/with
    KAF = "ك"           # Like (as proclitic)

    # Enclitics
    NI = "ني"          # Me
    KA = "ك"           # You
    HU = "ه"           # Him
    HA = "ها"          # Her/it
    HUM = "هم"         # Them (masculine)
    HUNNA = "هن"       # Them (feminine)


class AugmentationType(Enum):
    """Types of augmentation markers."""
    PREFIX = auto()      # Prefixes (أ، ت، ي، ن...)
    INFIX = auto()       # Infixes (ا، ت...)
    SUFFIX = auto()      # Suffixes (not clitics, but morphological)


@dataclass
class CliticMarker:
    """Marker for detected clitic."""
    clitic_type: CliticType
    form: Optional[str] = None          # Surface form
    syllable_count: int = 1             # Number of syllables in clitic
    attested: bool = False              # Whether attested in lexicon
    confidence: float = 1.0             # Detection confidence [0.0, 1.0]


@dataclass
class AugmentationMarker:
    """Marker for detected augmentation."""
    augmentation_type: AugmentationType
    position: int = 0                   # Position in syllable sequence
    form: Optional[str] = None          # Surface form
    confidence: float = 1.0             # Detection confidence [0.0, 1.0]


@dataclass
class PreMorphSegmentation:
    """
    Pre-morphological segmentation structure.

    Represents ONE hypothesis about how to segment syllables into:
    - Proclitics (if any)
    - Core unit
    - Enclitics (if any)
    - Augmentation markers (if detected)

    Does NOT contain:
    - Root (D3)
    - Pattern/Wazn (D4)
    - Ism/Fi'l/Harf (D5)
    - Case/Mood (D6)
    - Meaning (semantic)
    """
    # Syllable segmentation
    proclitics: List = field(default_factory=list)      # Proclitic syllables (from D1)
    core_syllables: List = field(default_factory=list)  # Core unit syllables (from D1)
    enclitics: List = field(default_factory=list)       # Enclitic syllables (from D1)

    # Detection markers
    clitic_markers: List[CliticMarker] = field(default_factory=list)
    augmentation_markers: List[AugmentationMarker] = field(default_factory=list)

    # Classification flags (mutually exclusive in most cases)
    is_frozen_word: bool = False            # Is this a frozen/lexicalized word?
    frozen_word_attested: bool = False      # Is frozen word in lexicon?

    is_functional_particle: bool = False    # Is this a functional particle?
    particle_attested: bool = False         # Is particle in lexicon?

    # Metadata
    segmentation_confidence: float = 1.0    # Overall segmentation confidence
    alternative_count: int = 1              # Number of alternative segmentations

    def total_syllable_count(self) -> int:
        """Total number of syllables in segmentation."""
        return (
            len(self.proclitics) +
            len(self.core_syllables) +
            len(self.enclitics)
        )

    def has_clitics(self) -> bool:
        """Check if segmentation contains clitics."""
        return bool(self.proclitics or self.enclitics)

    def has_augmentation(self) -> bool:
        """Check if segmentation contains augmentation markers."""
        return bool(self.augmentation_markers)

    def segment_structure(self) -> str:
        """String representation of segment structure."""
        parts = []
        if self.proclitics:
            parts.append(f"PRO({len(self.proclitics)})")
        if self.core_syllables:
            parts.append(f"CORE({len(self.core_syllables)})")
        if self.enclitics:
            parts.append(f"ENC({len(self.enclitics)})")
        return "+".join(parts) if parts else "EMPTY"

    def __str__(self) -> str:
        """Human-readable segmentation."""
        structure = self.segment_structure()
        flags = []
        if self.is_frozen_word:
            flags.append("FROZEN")
        if self.is_functional_particle:
            flags.append("PARTICLE")
        if self.has_augmentation():
            flags.append(f"AUG({len(self.augmentation_markers)})")

        flag_str = f" [{', '.join(flags)}]" if flags else ""
        return f"{structure}{flag_str}"


@dataclass
class PreMorphPolicy:
    """Policy for pre-morphological unit generation."""
    # Generation strategy
    exhaustive: bool = True                 # Generate all possible segmentations
    max_candidates: int = 100               # Maximum candidates to generate

    # Clitic detection
    enable_proclitic_detection: bool = True
    enable_enclitic_detection: bool = True
    max_proclitics: int = 3                 # Max consecutive proclitics
    max_enclitics: int = 2                  # Max consecutive enclitics

    # Frozen word detection
    enable_frozen_word_detection: bool = True
    require_frozen_word_attestation: bool = False  # Require lexicon attestation

    # Particle detection
    enable_particle_detection: bool = True
    require_particle_attestation: bool = False  # Require lexicon attestation

    # Augmentation detection
    enable_augmentation_detection: bool = True

    # Ranking
    prefer_simpler_segmentation: bool = True    # Prefer fewer segments
    prefer_attested_forms: bool = True          # Prefer lexicon-attested forms


# ============================================================================
# Convenience Functions
# ============================================================================


def make_simple_segmentation(core_syllables: List) -> PreMorphSegmentation:
    """Create simple segmentation with only core unit.

    Args:
        core_syllables: Syllables for core unit

    Returns:
        PreMorphSegmentation with no clitics or augmentation
    """
    return PreMorphSegmentation(
        core_syllables=core_syllables,
        segmentation_confidence=1.0,
        alternative_count=1
    )


def make_clitic_segmentation(
    proclitics: List,
    core_syllables: List,
    enclitics: List,
    clitic_markers: Optional[List[CliticMarker]] = None
) -> PreMorphSegmentation:
    """Create segmentation with clitics.

    Args:
        proclitics: Proclitic syllables
        core_syllables: Core syllables
        enclitics: Enclitic syllables
        clitic_markers: Optional clitic markers

    Returns:
        PreMorphSegmentation with clitics
    """
    return PreMorphSegmentation(
        proclitics=proclitics,
        core_syllables=core_syllables,
        enclitics=enclitics,
        clitic_markers=clitic_markers or [],
        segmentation_confidence=0.8,  # Lower confidence with clitics
        alternative_count=1
    )


def make_frozen_word_segmentation(
    syllables: List,
    attested: bool = False
) -> PreMorphSegmentation:
    """Create frozen word segmentation.

    Args:
        syllables: All syllables (treated as frozen unit)
        attested: Whether attested in frozen word lexicon

    Returns:
        PreMorphSegmentation marked as frozen word
    """
    return PreMorphSegmentation(
        core_syllables=syllables,
        is_frozen_word=True,
        frozen_word_attested=attested,
        segmentation_confidence=0.9 if attested else 0.5,
        alternative_count=1
    )


def make_particle_segmentation(
    syllables: List,
    attested: bool = False
) -> PreMorphSegmentation:
    """Create functional particle segmentation.

    Args:
        syllables: All syllables (treated as particle)
        attested: Whether attested in particle lexicon

    Returns:
        PreMorphSegmentation marked as functional particle
    """
    return PreMorphSegmentation(
        core_syllables=syllables,
        is_functional_particle=True,
        particle_attested=attested,
        segmentation_confidence=0.9 if attested else 0.5,
        alternative_count=1
    )
