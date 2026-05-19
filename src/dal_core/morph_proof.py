"""
MorphProof Contract (عقد البرهان الصرفي)

Morphological proof structure required for composition readiness.

CRITICAL PRINCIPLE:
- These are NOT semantic meanings
- These are morphological/surface signifier features
- All values are CANDIDATES with evidence/rank/residuals
- Maintains Theorem 5: لا معنى داخل الدال

The composition layer requires these features to operate correctly.
Without them, compositional analysis would be incomplete or incorrect.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from dal_core.evidence import Evidence
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual


class CandidateStatus(Enum):
    """
    حالة المرشح (Candidate Status)

    Status of a morphological feature candidate.
    """
    RESOLVED = "محسوم"           # Definitively determined
    CANDIDATE = "مرشح"           # Candidate with evidence
    COMPETING = "متنافس"         # Multiple competing candidates
    UNRESOLVED = "غير محسوم"     # Cannot determine
    NOT_APPLICABLE = "غير منطبق"  # Not applicable to this word type


@dataclass
class RootCandidate:
    """
    مرشح الجذر (Root Candidate)

    Candidate for the morphological root.
    NOT definitive without witness confirmation.
    """
    letters: tuple[str, ...]  # Root letters (typically 3-4)
    evidence: list[Evidence] = field(default_factory=list)
    rank: LughaRank = LughaRank.FORM  # Pattern-based is FORM, not attestation
    residuals: list[Residual] = field(default_factory=list)
    confidence: float = 0.0

    def __str__(self) -> str:
        return f"Root({''.join(self.letters)}, rank={self.rank.name})"


@dataclass
class WaznCandidate:
    """
    مرشح الوزن (Pattern Candidate)

    Candidate for the morphological pattern.

    CRITICAL: Wazn detection does NOT prove D_lugha.
    Pattern alone is insufficient for linguistic attestation (Theorem 3).
    """
    pattern: str  # e.g., "فَعَلَ", "فَاعِل", "مَفْعُول"
    form_number: Optional[int] = None  # Verb form I-X (if applicable)
    evidence: list[Evidence] = field(default_factory=list)
    rank: LughaRank = LughaRank.FORM  # Pattern detection is FORM rank
    residuals: list[Residual] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Wazn({self.pattern}, rank={self.rank.name})"


@dataclass
class VerbFeatureProof:
    """
    برهان خصائص الفعل (Verb Feature Proof)

    Morphological features specific to verbs.
    These are FORM features, not semantic time/intention.
    """
    # Tense FORM (not semantic time)
    tense_form: Optional[str] = None  # "ماضٍ", "مضارع", "أمر" (morphological form)

    # Voice FORM (not semantic agent/patient)
    voice_form: Optional[str] = None  # "معلوم", "مجهول" (morphological form)

    # Mood potential (for مضارع only)
    mood_potential: Optional[str] = None  # "مرفوع", "منصوب", "مجزوم" (potential state)

    # Form pattern (I-X)
    form_pattern: Optional[int] = None

    # Evidence and rank
    evidence: list[Evidence] = field(default_factory=list)
    rank: LughaRank = LughaRank.FORM
    residuals: list[Residual] = field(default_factory=list)


@dataclass
class SurfaceEffect:
    """
    أثر سطحي (Surface Effect)

    Surface-level ending effects.

    CRITICAL: These are signifier states, NOT i'rab interpretations.
    The syntactic/i'rab interpretation comes later in composition.
    """
    effect_type: str  # "vowel", "letter", "deletion", "nunation"
    effect_value: str  # "ضمة", "فتحة", "كسرة", "ألف", "واو", "ياء", etc.
    position: str  # "final", "penultimate"
    is_original: bool  # True if original to root, False if added
    evidence: list[Evidence] = field(default_factory=list)
    trace: dict = field(default_factory=dict)


@dataclass(frozen=True)
class MorphProof:
    """
    برهان صرفي (Morphological Proof)

    Complete morphological analysis required for composition readiness.

    PRINCIPLES:
    1. All features are CANDIDATES (not absolute truths)
    2. Each candidate has evidence/rank/residuals
    3. Unknown features produce residuals
    4. Competing candidates block composition certificate
    5. NO SEMANTIC FIELDS (maintains Theorem 5)

    These features are signifier-level properties needed for
    compositional syntax, NOT meanings or semantic interpretations.
    """

    # Root and pattern
    root_candidates: tuple[RootCandidate, ...] = field(default_factory=tuple)
    wazn_candidates: tuple[WaznCandidate, ...] = field(default_factory=tuple)

    # Morphological classifications
    jamid_mushtaq_status: CandidateStatus = CandidateStatus.UNRESOLVED
    jamid_mushtaq_evidence: tuple[Evidence, ...] = field(default_factory=tuple)

    mabni_murab_status: CandidateStatus = CandidateStatus.UNRESOLVED
    mabni_murab_evidence: tuple[Evidence, ...] = field(default_factory=tuple)

    # Signifier features (NOT semantic)
    definiteness_status: CandidateStatus = CandidateStatus.UNRESOLVED
    definiteness_markers: tuple[str, ...] = field(default_factory=tuple)  # "أل", "علم", "ضمير", etc.
    definiteness_evidence: tuple[Evidence, ...] = field(default_factory=tuple)

    gender_status: CandidateStatus = CandidateStatus.UNRESOLVED
    gender_value: Optional[str] = None  # "مذكر", "مؤنث"
    gender_type: Optional[str] = None  # "صوري", "سماعي", "معنوي"
    gender_evidence: tuple[Evidence, ...] = field(default_factory=tuple)

    number_status: CandidateStatus = CandidateStatus.UNRESOLVED
    number_value: Optional[str] = None  # "مفرد", "مثنى", "جمع"
    number_evidence: tuple[Evidence, ...] = field(default_factory=tuple)

    # Verb-specific features (if applicable)
    verb_features: Optional[VerbFeatureProof] = None

    # Surface effects
    surface_effects: tuple[SurfaceEffect, ...] = field(default_factory=tuple)

    # Overall proof status
    rank: LughaRank = LughaRank.FORM  # Morphological analysis starts at FORM
    all_residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)

    def is_composition_ready(self) -> bool:
        """
        Check if morphological proof is sufficient for composition.

        Composition requires:
        - No competing candidates for critical features
        - Mabni/murab status determined (critical for syntax)
        - No blocker residuals

        NOT required for composition readiness:
        - Absolute certainty (candidates with evidence are acceptable)
        - Complete feature coverage (some features can be unresolved)
        """
        from dal_core.residuals import has_blocking_residuals

        # Check for blockers
        if has_blocking_residuals(list(self.all_residuals)):
            return False

        # Check for critical competing candidates
        if self.mabni_murab_status == CandidateStatus.COMPETING:
            return False  # Must know if word is built or declined

        # If mabni/murab is unresolved, that's a blocker for composition
        if self.mabni_murab_status == CandidateStatus.UNRESOLVED:
            # Exception: particles are typically mabni
            # But we need explicit determination, not assumption
            return False

        return True

    def __str__(self) -> str:
        status = "composition-ready" if self.is_composition_ready() else "not-ready"
        return f"MorphProof({status}, rank={self.rank.name})"


def make_stub_morph_proof() -> MorphProof:
    """
    Create a stub MorphProof for testing/placeholder use.

    This indicates morphological analysis has not been performed.
    """
    from dal_core.residuals import ResidualType, ResidualSeverity

    return MorphProof(
        rank=LughaRank.ZERO,
        all_residuals=(
            Residual(
                type=ResidualType.MORPH_ANALYSIS_INCOMPLETE,
                severity=ResidualSeverity.WARNING,
                message="Morphological analysis not yet implemented"
            ),
        )
    )
