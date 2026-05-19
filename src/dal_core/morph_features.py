"""
Morphological Features for MufradProof (ملامح صرفية لبرهان المفرد)

Typed proof structures for morphological analysis within composition-ready signifiers.
These structures belong to D_mufrad proof layer, not semantic meaning.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from dal_core.ranks import LughaRank
from dal_core.residuals import Residual
from dal_core.evidence import Evidence


class CandidateStatus(Enum):
    """Status of morphological feature candidates"""
    UNRESOLVED = "غير محسوم"              # Unresolved competition
    RESOLVED_CERTAIN = "محسوم يقيني"      # Resolved with certainty
    RESOLVED_PROBABLE = "محسوم محتمل"     # Resolved with probability
    BLOCKED = "ممنوع"                     # Blocked by constraints
    NOT_APPLICABLE = "غير منطبق"          # Not applicable to this word


@dataclass(frozen=True)
class SegmentationProof:
    """
    برهان التقطيع (Segmentation Proof)

    Proves word segmentation into stem + clitics.
    """
    segments: tuple[str, ...]
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)


@dataclass(frozen=True)
class StemProof:
    """
    برهان الجذع (Stem Proof)

    The core inflectable part after removing clitics.
    """
    stem: str
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)


@dataclass(frozen=True)
class CliticProof:
    """
    برهان الملحق (Clitic Proof)

    Proof of attached particle (prefix/suffix).
    Examples: ال، ب، ك، ل، و، ف، ها، هم، كم
    """
    clitic: str
    position: str  # "prefix" | "suffix"
    clitic_type: str  # "definite_article" | "preposition" | "pronoun" | "conjunction"
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)


@dataclass(frozen=True)
class RootCandidate:
    """
    مرشح جذر (Root Candidate)

    Root extraction candidate with evidence.
    Competition between roots is tracked via multiple candidates.
    """
    root: tuple[str, ...]  # e.g., ("ك", "ت", "ب")
    root_type: str  # "trilateral" | "quadrilateral" | "defective" | "hollow" | "doubled"
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    confidence: float  # 0.0 to 1.0
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)


@dataclass(frozen=True)
class WaznCandidate:
    """
    مرشح وزن (Pattern/Template Candidate)

    Morphological pattern candidate.
    Examples: فَعَلَ، فاعِل، مَفعول، فَعّال
    """
    wazn: str
    pattern_class: str  # "verb_form_I" | "active_participle" | "passive_participle" | etc
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    confidence: float
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)


@dataclass(frozen=True)
class VerbFeatureProof:
    """
    برهان الملامح الفعلية (Verb Feature Proof)

    Verb-specific morphological features.
    Required when DType == FIIL.
    """
    tense: CandidateStatus  # madi, mudari, amr
    voice: CandidateStatus  # malum, majhul
    transitivity: CandidateStatus  # lazim, mutaaddi
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    person: Optional[CandidateStatus] = None  # first, second, third
    gender: Optional[CandidateStatus] = None  # masculine, feminine
    number: Optional[CandidateStatus] = None  # singular, dual, plural
    mood: Optional[CandidateStatus] = None  # marfu, mansoob, majzoom (for mudari)
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)


@dataclass(frozen=True)
class NounInflectionClass:
    """
    صنف التصريف الاسمي (Noun Inflection Class)

    Noun-specific inflection patterns.
    Required when DType == ISM.
    """
    inflection_type: str  # "munassarif" | "mamnu_min_sarf" | "mabni"
    declension_pattern: str  # "triptote" | "diptote" | "indeclinable"

    evidence: tuple[Evidence, ...]
    rank: LughaRank
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)


@dataclass(frozen=True)
class ParticleOperatorPotential:
    """
    احتمال عملية الحرف (Particle Operator Potential)

    Whether particle can act as operator (عامل) in composition.
    Required when DType == HARF.

    Examples:
    - إنّ وأخواتها (nasb operators)
    - كان وأخواتها (raf/nasb operators)
    - حروف الجر (jarr operators)
    """
    can_govern: bool
    evidence: tuple[Evidence, ...]
    rank: LughaRank
    operator_class: Optional[str] = None  # "inna_sisters" | "kana_sisters" | "jarr" | etc
    governance_type: Optional[str] = None  # "nasb" | "raf_nasb" | "jarr"
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)
