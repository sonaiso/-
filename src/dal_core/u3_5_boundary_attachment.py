"""
U₃.₅ Boundary and Attachment Layer (طبقة الحدود والاتصال)

Domain: U₃.₅ = BoundaryAttachmentCarrier
Transition: Functional Role (U₃) → Boundary Segmentation (U₃.₅) → Morpheme (U₄)
Purpose: Distinguish WrittenCompositeToken from TrueSingularLafẓ before morphological analysis

Key Principle:
    Orthographic boundary ≠ True lafẓ boundary
    Written whitespace ≠ Functional unit boundary

    WrittenCompositeToken (اللفظ الكتابي المركب):
        Orthographically connected unit that may contain multiple functional units.
        Example: وَبِكِتَابِهِمْ is ONE written token but FOUR true units:
            وَ (conjunction) + بِ (preposition) + كِتَاب (core stem) + ـهِمْ (pronoun)

    TrueSingularLafẓ (اللفظ المفرد الحقيقي):
        Minimal licensed functional unit with independent contract.
        Example: كِتَاب is a true singular lafẓ (open lexical core)

Critical Laws:
    1. Only CoreStem/VerbalCore enters weight/pattern analysis (U₆)
    2. External attachment ≠ Internal pattern augment
       - بِ in بِكِتَابٍ = proclitic (external) → separable
       - مـ in مَكْتَب = pattern prefix (internal) → non-separable until U₆
    3. Proclitic/Enclitic are detachable functional units
    4. Prefix/Suffix are morphological elements (handled in U₄-U₆)
    5. Trace preserved from U₃
    6. Residuals propagate through segmentation

Architecture:
    U₃ (FunctionalRole) → U₃.₅ (BoundaryAttachment) → U₄ (Morpheme) → U₅ (StemRoot) → U₆ (Pattern)

Positioning Logic:
    - After U₃ because we need syllabic functional role candidates
    - Before U₄ because morpheme classification requires knowing what's a clitic vs morpheme
    - Before U₆ because only true lexical cores enter pattern/weight analysis

PR: U3.5-BOUNDARY-LAYER
Created: 2026-05-25
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Set, FrozenSet, Dict, Any, Tuple
from uuid import uuid4, UUID

from dal_core.u3_functional_roles import RoleSpan
from dal_core.residuals import Residual


# ============================================================================
# Attachment Type Taxonomy
# ============================================================================

class AttachmentType(Enum):
    """
    Types of attachment for boundary segmentation.

    Critical distinction:
        External attachments (Proclitic/Enclitic) = detachable functional units
        Internal elements (Prefix/Suffix/Infix) = morphological structure

    Examples:
        Proclitic: وَ، فَ، بِ، لِ، كَ (external, separable before weight)
        Enclitic: ـهُ، ـكَ، ـها، ـهُمْ (external, separable before weight)
        Prefix: يَـ in يَكْتُبُ (internal, part of verb conjugation)
        Suffix: ـونَ in يَكْتُبُونَ (internal, part of verb conjugation)
        Infix: ا in كَاتِب (internal, part of pattern فَاعِل)
        StemCore: كِتَاب (true lexical core, enters weight analysis)
    """
    # External attachments (separable before weight/pattern)
    PROCLITIC = "سابقة لاصقة"              # و، ف، ب، ل، ك
    ENCLITIC = "لاحقة لاصقة"              # ـه، ـك، ـها، ـهم

    # Internal morphological elements (handled in U₄-U₆)
    PREFIX = "سابقة صرفية"                # يَـ، تَـ، نَـ، أَـ in verbs
    SUFFIX = "لاحقة صرفية"                # ـون، ـين، ـات
    INFIX = "زيادة داخلية"                # ا in كَاتِب, ت in تَفَعَّل

    # Core elements
    STEM_CORE = "جذع"                      # Core stem (enters U₅/U₆)
    VERBAL_CORE = "نواة فعلية"             # Verbal core

    # Special cases
    ORTHOGRAPHIC_JOIN = "اتصال كتابي فقط"  # Written connection only
    NON_DETACHABLE = "جزء غير قابل للفصل"  # Non-separable part
    UNKNOWN = "غير محدد"                   # Unknown attachment


class BoundarySegmentationType(Enum):
    """
    Segmentation strategy types.

    Examples:
        PROCLITIC_CORE_ENCLITIC: وَبِكِتَابِهِمْ → [وَ, بِ] + كِتَاب + [ـهِمْ]
        CORE_ONLY: كِتَابٌ → كِتَابٌ (no external attachments)
        MULTIPLE_PROCLITICS: وَلَكَ → [وَ, لَـ] + كَ (or [وَ] + لَكَ)
    """
    PROCLITIC_CORE_ENCLITIC = "سابقة_جذع_لاحقة"
    CORE_ONLY = "جذع_فقط"
    MULTIPLE_PROCLITICS = "سوابق_متعددة"
    MULTIPLE_ENCLITICS = "لواحق_متعددة"
    COMPLEX_SEGMENTATION = "تقطيع_معقد"
    UNSEGMENTED = "غير_مقطّع"
    AMBIGUOUS = "ملتبس"


class TrueSingularLafzType(Enum):
    """
    Types of true singular lafẓ units.

    Each represents a minimal licensed functional/lexical unit.

    Examples:
        CLOSED_CLASS: و، ف، ب، ل، إنّ، لكنّ (particles)
        PRONOUN: هو، هي، ـه، ـك (pronouns)
        OPEN_LEXICAL_CORE: كِتَاب، قَلَم (noun stems)
        VERBAL_CORE: كَتَبَ، يَكْتُبُ (verb cores)
    """
    CLOSED_CLASS = "أداة"                  # Particles, prepositions
    PRONOUN = "ضمير"                       # Pronouns (attached/detached)
    OPEN_LEXICAL_CORE = "جذع_معجمي_مفتوح"  # Open class noun/adjective stem
    VERBAL_CORE = "نواة_فعلية"             # Verbal core
    INFLECTIONAL_CLITIC = "لاحقة_تصريفية"  # Inflectional clitic (واو الجماعة, etc.)
    DERIVATIONAL_MARKER = "علامة_اشتقاقية" # Derivational marker
    FUNCTIONAL_MARKER = "علامة_وظيفية"     # Functional marker
    UNKNOWN = "غير_محدد"                   # Unknown type


# ============================================================================
# Boundary Rank System
# ============================================================================

class BoundaryRank(Enum):
    """
    Epistemic rank for boundary segmentation hypotheses.

    Evidence-based progression:
        ZERO → CANDIDATE → HYPOTHESIS → STRONG_HYPOTHESIS → CERTIFICATE
    """
    BOUNDARY_ZERO = 0              # No hypothesis
    BOUNDARY_CANDIDATE = 1         # Possible segmentation
    BOUNDARY_HYPOTHESIS = 2        # Hypothesis with some evidence
    BOUNDARY_STRONG_HYPOTHESIS = 3 # Strong evidence
    BOUNDARY_CERTIFICATE = 4       # Lexicon-attested or rule-certified
    BOUNDARY_BLOCKED = -1          # Blocked by evidence


# ============================================================================
# Boundary Residuals
# ============================================================================

class BoundaryResidual(Enum):
    """
    Residual types for boundary segmentation.

    Warnings and blockers that propagate through operations.
    """
    # Ambiguity residuals
    PROCLITIC_VS_STEM_AMBIGUITY = "التباس_سابقة_جذع"
    ENCLITIC_VS_STEM_AMBIGUITY = "التباس_لاحقة_جذع"
    PREFIX_VS_PATTERN_AUGMENT_AMBIGUITY = "التباس_سابقة_زيادة"
    SUFFIX_VS_PATTERN_ENDING_AMBIGUITY = "التباس_لاحقة_نهاية"

    # Pronoun ambiguity
    DETACHED_VS_ATTACHED_PRONOUN_AMBIGUITY = "التباس_ضمير_منفصل_متصل"

    # Definiteness issues
    DEFINITE_ARTICLE_BOUNDARY_AMBIGUITY = "التباس_حد_أل"
    HAMZAT_WASL_BOUNDARY_ISSUE = "قضية_همزة_وصل"
    SOLAR_ASSIMILATION_BOUNDARY_ISSUE = "قضية_إدغام_شمسي"

    # Segmentation risks
    ORTHOGRAPHIC_FUSION = "دمج_كتابي"
    MISSING_WHITESPACE = "بياض_مفقود"
    OVER_SEGMENTATION_RISK = "خطر_تقطيع_زائد"
    UNDER_SEGMENTATION_RISK = "خطر_تقطيع_ناقص"

    # Pattern vs clitic
    PATTERN_ELEMENT_MISIDENTIFIED_AS_CLITIC = "عنصر_وزني_حُدّد_كلاصق"
    CLITIC_MISIDENTIFIED_AS_PATTERN = "لاصق_حُدّد_كعنصر_وزني"

    # Evidence issues
    INSUFFICIENT_EVIDENCE = "دليل_غير_كاف"
    CONFLICTING_EVIDENCE = "دليل_متعارض"
    LEXICON_MISMATCH = "عدم_تطابق_معجمي"


# ============================================================================
# Core Data Structures
# ============================================================================

@dataclass(frozen=True)
class WrittenCompositeToken:
    """
    Written composite token (اللفظ الكتابي المركب).

    Orthographic unit written without internal whitespace,
    but may contain multiple functional units.

    Example:
        وَبِكِتَابِهِمْ is one WrittenCompositeToken

    Fields:
        surface: Surface string as written
        role_spans: Input from U₃ (functional role candidates)
        id: Unique identifier
    """
    surface: str
    role_spans: Tuple[RoleSpan, ...]  # From U₃
    id: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return f"WrittenComposite({self.surface})"


@dataclass(frozen=True)
class TrueSingularLafz:
    """
    True singular lafẓ (اللفظ المفرد الحقيقي).

    Minimal licensed lexical/functional unit with independent contract.

    Example:
        كِتَاب is TrueSingularLafz (OPEN_LEXICAL_CORE)
        بِ is TrueSingularLafz (CLOSED_CLASS)
        ـهِمْ is TrueSingularLafz (PRONOUN)

    Fields:
        surface: Surface form
        lafz_type: Type of true singular lafz
        attachment_type: How it attaches (if applicable)
        role_spans: Underlying role spans from U₃
        weight_access: Can this unit enter weight/pattern analysis?
        detachable: Is this unit separable?
        id: Unique identifier
    """
    surface: str
    lafz_type: TrueSingularLafzType
    attachment_type: AttachmentType
    role_spans: Tuple[RoleSpan, ...]
    weight_access: bool  # True only for STEM_CORE/VERBAL_CORE
    detachable: bool     # True for PROCLITIC/ENCLITIC
    id: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return f"TrueSingular({self.surface}:{self.lafz_type.value})"


@dataclass(frozen=True)
class BoundarySegmentation:
    """
    Boundary segmentation result.

    Represents ONE hypothesis about segmenting a WrittenCompositeToken
    into TrueSingularLafẓ units.

    Example:
        وَبِكِتَابِهِمْ → [
            TrueSingular(وَ:CLOSED_CLASS),
            TrueSingular(بِ:CLOSED_CLASS),
            TrueSingular(كِتَاب:OPEN_LEXICAL_CORE),
            TrueSingular(ـهِمْ:PRONOUN)
        ]

    Fields:
        written_token: Original written token
        units: List of true singular lafẓ units
        segmentation_type: Type of segmentation
        trace: Trace to U₃ role spans
        residuals: Warnings/blockers
        rank: Epistemic rank
        evidence: Supporting evidence
    """
    written_token: WrittenCompositeToken
    units: Tuple[TrueSingularLafz, ...]
    segmentation_type: BoundarySegmentationType
    trace: Tuple[RoleSpan, ...]  # Complete trace to U₃
    residuals: FrozenSet[BoundaryResidual]
    rank: BoundaryRank
    evidence: Dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)

    def is_composite(self) -> bool:
        """Check if this is truly a composite (multiple units)."""
        return len(self.units) > 1

    def core_units(self) -> List[TrueSingularLafz]:
        """Get core stem/verbal units (those that enter weight analysis)."""
        return [u for u in self.units if u.weight_access]

    def external_clitics(self) -> List[TrueSingularLafz]:
        """Get external clitics (proclitics + enclitics)."""
        return [u for u in self.units if u.detachable]

    def __str__(self) -> str:
        unit_str = " + ".join(str(u) for u in self.units)
        return f"Segmentation({unit_str})"


@dataclass(frozen=True)
class BoundaryCandidate:
    """
    Carrier element for U₃.₅ layer.

    Represents a boundary segmentation candidate with full algebraic structure.

    Fields:
        segmentation: The boundary segmentation
        rank: Epistemic rank
        residuals: Warnings/blockers
        trace: Complete trace to U₃
        competitors: Alternative segmentations
        evidence: Supporting evidence
        id: Unique identifier
    """
    segmentation: BoundarySegmentation
    rank: BoundaryRank
    residuals: FrozenSet[BoundaryResidual]
    trace: Tuple[RoleSpan, ...]
    competitors: FrozenSet['BoundaryCandidate'] = field(default_factory=frozenset)
    evidence: Dict[str, Any] = field(default_factory=dict)
    id: UUID = field(default_factory=uuid4)

    def is_blocked(self) -> bool:
        """Check if this candidate is blocked."""
        return self.rank == BoundaryRank.BOUNDARY_BLOCKED

    def has_warnings(self) -> bool:
        """Check if this candidate has warning residuals."""
        warning_residuals = {
            BoundaryResidual.PROCLITIC_VS_STEM_AMBIGUITY,
            BoundaryResidual.ENCLITIC_VS_STEM_AMBIGUITY,
            BoundaryResidual.INSUFFICIENT_EVIDENCE,
        }
        return bool(self.residuals & warning_residuals)

    def has_blockers(self) -> bool:
        """Check if this candidate has blocker residuals."""
        blocker_residuals = {
            BoundaryResidual.CONFLICTING_EVIDENCE,
            BoundaryResidual.LEXICON_MISMATCH,
            BoundaryResidual.PATTERN_ELEMENT_MISIDENTIFIED_AS_CLITIC,
            BoundaryResidual.CLITIC_MISIDENTIFIED_AS_PATTERN,
        }
        return bool(self.residuals & blocker_residuals)

    def __str__(self) -> str:
        return f"BoundaryCandidate({self.segmentation}, rank={self.rank.name})"


# ============================================================================
# Completeness Predicate
# ============================================================================

def CompleteOne_3_5(candidate: BoundaryCandidate) -> bool:
    """
    Completeness predicate for U₃.₅ layer (CompleteOne₃.₅).

    A boundary candidate is complete if:
        1. Segmentation is non-empty
        2. All units have valid types
        3. Trace preserved from U₃
        4. No blocker residuals (warnings acceptable)
        5. Rank ≥ CANDIDATE
        6. Evidence documented
        7. Core units have weight_access = True
        8. External clitics have detachable = True

    Args:
        candidate: Boundary candidate to check

    Returns:
        True if complete, False otherwise
    """
    seg = candidate.segmentation

    # Check 1: Non-empty segmentation
    if not seg.units:
        return False

    # Check 2: All units have valid types
    for unit in seg.units:
        if unit.lafz_type == TrueSingularLafzType.UNKNOWN:
            return False
        if unit.attachment_type == AttachmentType.UNKNOWN:
            return False

    # Check 3: Trace preserved
    if not seg.trace:
        return False

    # Check 4: No blocker residuals
    if candidate.has_blockers():
        return False

    # Check 5: Rank ≥ CANDIDATE
    if candidate.rank == BoundaryRank.BOUNDARY_ZERO or \
       candidate.rank == BoundaryRank.BOUNDARY_BLOCKED:
        return False

    # Check 6: Evidence documented
    if not seg.evidence and candidate.rank.value >= BoundaryRank.BOUNDARY_HYPOTHESIS.value:
        return False

    # Check 7: Core units consistency
    for unit in seg.units:
        if unit.attachment_type in {AttachmentType.STEM_CORE, AttachmentType.VERBAL_CORE}:
            if not unit.weight_access:
                return False

    # Check 8: Clitic detachability
    for unit in seg.units:
        if unit.attachment_type in {AttachmentType.PROCLITIC, AttachmentType.ENCLITIC}:
            if not unit.detachable:
                return False

    return True


# ============================================================================
# Critical Laws
# ============================================================================

def law_weight_access_for_core_only(candidate: BoundaryCandidate) -> bool:
    """
    Critical Law: Only core stems/verbal cores enter weight analysis.

    weight_access = True ⟺ attachment_type ∈ {STEM_CORE, VERBAL_CORE}

    Args:
        candidate: Boundary candidate to check

    Returns:
        True if law satisfied, False if violated
    """
    for unit in candidate.segmentation.units:
        core_types = {AttachmentType.STEM_CORE, AttachmentType.VERBAL_CORE}
        is_core = unit.attachment_type in core_types
        has_access = unit.weight_access

        if is_core != has_access:
            return False

    return True


def law_external_attachment_detachable(candidate: BoundaryCandidate) -> bool:
    """
    Critical Law: External attachments are detachable.

    attachment_type ∈ {PROCLITIC, ENCLITIC} ⟹ detachable = True

    Args:
        candidate: Boundary candidate to check

    Returns:
        True if law satisfied, False if violated
    """
    for unit in candidate.segmentation.units:
        external_types = {AttachmentType.PROCLITIC, AttachmentType.ENCLITIC}
        is_external = unit.attachment_type in external_types
        is_detachable = unit.detachable

        if is_external and not is_detachable:
            return False

    return True


def law_internal_morpheme_not_detachable(candidate: BoundaryCandidate) -> bool:
    """
    Critical Law: Internal morphological elements are NOT detachable at this layer.

    attachment_type ∈ {PREFIX, SUFFIX, INFIX} ⟹ detachable = False

    These are handled in U₄-U₆, not separated here.

    Args:
        candidate: Boundary candidate to check

    Returns:
        True if law satisfied, False if violated
    """
    for unit in candidate.segmentation.units:
        internal_types = {AttachmentType.PREFIX, AttachmentType.SUFFIX, AttachmentType.INFIX}
        is_internal = unit.attachment_type in internal_types
        is_detachable = unit.detachable

        if is_internal and is_detachable:
            return False

    return True
