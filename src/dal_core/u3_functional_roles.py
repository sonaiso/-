"""
⚠️ LEGACY U₃ Functional Role Layer - ARCHITECTURAL REPOSITIONING REQUIRED ⚠️

DEPRECATED POSITION: This module was originally U₃ but is now recognized as U₅.

Domain: U₅ = FunctionalRoleCarrier (NEW CANONICAL POSITION)
Former: U₃ = SyllabicFunctionalRoleCarrier (LEGACY POSITION)

ARCHITECTURAL NOTE:
    After U₂s ArabicSyllableCarrier, the correct execution path is:
        U₂s → U₃ BoundaryAndAttachment → U₄ TrueSingularLafẓ → U₅ FunctionalRole

    This module was created before BoundaryAndAttachment and TrueSingularLafẓ layers
    were recognized as necessary intermediate steps. It is now U₅ in the canonical
    execution layer registry (see: src/dal_core/execution_layer_registry.py).

RATIONALE:
    Functional role assignment requires:
        1. Boundary detection (U₃): Separate وَ, بِـ, كِتَاب, ـهِمْ in وَبِكِتَابِهِمْ
        2. True Lafẓ identification (U₄): Determine standalone vs. compound units
        3. THEN role assignment (U₅): Assign HARF_JARR, ROOT, PRONOUN roles

    Without U₃ and U₄, role assignment jumps prematurely from syllable to role,
    violating the no-leap principle: لا دور وظيفي قبل فصل الحدود

MIGRATION PATH:
    - This file is retained for compatibility
    - New code should use: from dal_core.u5_functional_role_carrier import *
    - Canonical layer order: See execution_layer_registry.EXECUTION_LAYER_ORDER

Purpose: Assign candidate functional roles WITHOUT premature commitment

Key Principle:
    Same syllable may have multiple roles in different contexts.
    Roles are promoted/demoted based on evidence, NOT assumed.

Critical Laws:
    1. Role ≠ certified until competitors blocked by evidence
    2. Same syllable sequence may activate different roles (بِ = preposition | root radical)
    3. Closed-class roles require lexicon match
    4. Root roles require pattern evidence
    5. No meaning, syntax, or semantics at this level

Corrected Architecture:
    U₂s (Syllable) → U₃ (Boundary) → U₄ (TrueLafẓ) → U₅ (FunctionalRole) [THIS MODULE]

PR: U3-LAYER (original), EXEC-LAYER-REFACTOR (architectural correction)
Created: 2026-05-25
Updated: 2026-05-25 (architectural repositioning)
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Set, FrozenSet, Dict, Any
from uuid import uuid4

from dal_core.syllables import Syllable
from dal_core.residuals import Residual


# ============================================================================
# Role Type Taxonomy (Multi-Sorted Role Algebra)
# ============================================================================

class RoleSort(Enum):
    """
    Role sort categories for multi-sorted algebra.

    Each role belongs to exactly one sort, preventing category mixing.
    """
    CLOSED_CLASS = "closed_class"        # Particles, prepositions, etc.
    PRONOUN = "pronoun"                  # Personal, attached, detached
    ROOT = "root"                        # Root radical positions
    DERIVATIONAL = "derivational"        # Augments, affixes, patterns
    INFLECTIONAL = "inflectional"        # Gender, number, definiteness
    VERB_FEATURE = "verb_feature"        # Tense, mood, voice markers
    RELATION_POSSESSION = "relation_possession"  # Nisbah, possession
    BUILD_INFLECT = "build_inflect"      # Mabni vs Murab
    RESIDUAL = "residual"                # Unresolved, deferred


# ============================================================================
# Closed Class Roles (أدوار الأدوات والحروف)
# ============================================================================

class ClosedClassRole(Enum):
    """
    Closed-class functional roles requiring lexicon match.

    Examples:
        مِنْ، عَنْ، فِي، بِـ، لِـ، كَـ → Requires closed-class lexicon
    """
    HARF_JARR = "حرف جر"              # Preposition (بِ، لِ، مِنْ، إلى)
    HARF_ATF = "حرف عطف"              # Conjunction (وَ، فَ، ثُمَّ)
    HARF_NASB = "حرف نصب"             # Accusative particle (إنّ، أنّ، لكنّ)
    HARF_JAZM = "حرف جزم"             # Jussive particle (لَمْ، لَمّا، لام الأمر)
    HARF_TAWKID = "حرف توكيد"         # Emphasis particle (قَدْ، لَقَدْ)
    HARF_NAFY = "حرف نفي"             # Negation (لا، ما، لم، لن)
    HARF_ISTIFHAM = "حرف استفهام"    # Interrogative (هَلْ، أَ، الهمزة)
    HARF_SHART = "حرف شرط"            # Conditional (إنْ، لَوْ، لَوْلا)
    HARF_TANBIH = "حرف تنبيه"         # Alert particle (ألا، أَما)
    HARF_NIDA = "حرف نداء"            # Vocative (يا، أَيا، هَيا)
    HARF_TASHBIH = "حرف تشبيه"        # Comparison (كَ، كَأنَّ)
    HARF_MAANA_GENERIC = "حرف معنى"   # Generic meaning particle


# ============================================================================
# Pronoun Roles (أدوار الضمائر)
# ============================================================================

class PronounRole(Enum):
    """
    Pronoun functional roles.

    Examples:
        ـهُ، ـها، ـكَ → Attached pronouns
        هُوَ، هِيَ → Detached pronouns
    """
    ATTACHED_PRONOUN = "ضمير متصل"
    DETACHED_PRONOUN = "ضمير منفصل"
    SUBJECT_PRONOUN = "ضمير رفع"
    OBJECT_PRONOUN = "ضمير نصب"
    POSSESSIVE_PRONOUN = "ضمير ملكية"
    GENITIVE_ATTACHED_PRONOUN = "ضمير جر متصل"
    HIDDEN_PRONOUN_CANDIDATE = "ضمير مستتر محتمل"


# ============================================================================
# Root Roles (أدوار الجذر)
# ============================================================================

class RootRole(Enum):
    """
    Root radical position roles.

    Requires pattern evidence, NOT standalone syllable analysis.

    Examples:
        كَتَبَ → ك (fa), ت (ayn), ب (lam)
    """
    FA_RADICAL = "فاء الجذر"           # First radical
    AYN_RADICAL = "عين الجذر"          # Second radical
    LAM_RADICAL = "لام الجذر"          # Third radical
    FOURTH_RADICAL = "رابع الجذر"      # Fourth radical (quadriliteral)
    WEAK_RADICAL = "حرف علة جذري"     # Weak letter radical (و، ي، ا)
    HAMZATED_RADICAL = "مهموز"         # Hamzated radical
    DOUBLED_RADICAL = "مضعف"           # Doubled radical (shadda)
    ROOT_CANDIDATE = "مرشح جذري"       # Candidate radical (unverified)
    NON_ROOT = "غير جذري"              # Not a root radical


# ============================================================================
# Derivational Roles (أدوار الزيادة والوزن)
# ============================================================================

class DerivationalRole(Enum):
    """
    Derivational augment roles.

    Requires pattern evidence.

    Examples:
        استفعل → سين وتاء زائدة
        مُفاعَلة → ميم وألف زائدة
    """
    PREFIX_ZIYADAH = "زيادة سابقة"
    INFIX_ZIYADAH = "زيادة وسطية"
    SUFFIX_ZIYADAH = "زيادة لاحقة"
    ALIF_MUFAALA = "ألف مفاعلة"
    TA_TAFAUL = "تاء تفاعل"
    SIN_ISTIFAL = "سين استفعال"
    HAMZA_IFAL = "همزة إفعال"
    MIM_MASDAR_OR_ISM = "ميم مصدر أو اسم"
    YA_NISBAH = "ياء نسبة"
    WAW_PLURAL_OR_PATTERN = "واو جمع أو وزن"
    TA_MARBUTA = "تاء مربوطة"
    NUN_AUGMENT = "نون زائدة"
    SHADDA_PATTERN_EFFECT = "أثر شدة في الوزن"


# ============================================================================
# Gender/Number Roles (أدوار الجنس والعدد)
# ============================================================================

class GenderNumberRole(Enum):
    """
    Gender and number marker roles.

    Examples:
        ـة → Feminine marker
        ـان → Dual marker
        ـون → Masculine plural marker
    """
    FEMININE_MARKER = "علامة تأنيث"
    MASCULINE_DEFAULT_CANDIDATE = "مذكر افتراضي محتمل"
    SINGULAR_MARKER = "علامة إفراد"
    DUAL_MARKER = "علامة تثنية"
    SOUND_MASCULINE_PLURAL_MARKER = "علامة جمع مذكر سالم"
    SOUND_FEMININE_PLURAL_MARKER = "علامة جمع مؤنث سالم"
    BROKEN_PLURAL_PATTERN_CANDIDATE = "مرشح جمع تكسير"
    COLLECTIVE_MARKER = "علامة جمع"
    UNIT_NOUN_MARKER = "علامة اسم وحدة"


# ============================================================================
# Definiteness Roles (أدوار المعرفة والنكرة)
# ============================================================================

class DefinitenessRole(Enum):
    """
    Definiteness marker roles.

    Examples:
        الـ → Definite article
        ـٌ، ـً، ـٍ → Tanween (indefiniteness)
    """
    AL_DEFINITE_PREFIX = "أل التعريف"
    TANWEEN_INDEFINITENESS_CANDIDATE = "تنوين نكرة محتمل"
    PROPER_NAME_CANDIDATE = "علم محتمل"
    IDAFA_DEFINITENESS_CANDIDATE = "تعريف بالإضافة محتمل"
    PRONOUN_DEFINITENESS_CARRIER = "تعريف بالضمير"
    DEMONSTRATIVE_DEFINITENESS_CARRIER = "تعريف بالإشارة"


# ============================================================================
# Verb Feature Roles (أدوار الفعل وأحواله)
# ============================================================================

class VerbFeatureRole(Enum):
    """
    Verb feature marker roles.

    Examples:
        يَـ، تَـ، أَـ، نَـ → Present tense prefixes
        ـتْ → Feminine marker
    """
    PAST_FORM_CANDIDATE = "صيغة ماض محتملة"
    PRESENT_PREFIX_CANDIDATE = "سابقة مضارعة محتملة"
    IMPERATIVE_CANDIDATE = "أمر محتمل"
    PASSIVE_VOWEL_PATTERN_CANDIDATE = "حركات مبني للمجهول محتملة"
    ACTIVE_VOWEL_PATTERN_CANDIDATE = "حركات مبني للمعلوم محتملة"
    JUSSIVE_MARKER_CANDIDATE = "علامة جزم محتملة"
    SUBJUNCTIVE_MARKER_CANDIDATE = "علامة نصب محتملة"
    INDICATIVE_MARKER_CANDIDATE = "علامة رفع محتملة"
    NUNATION_OR_NUN_MOOD_CANDIDATE = "نون توكيد أو مزاج محتملة"


# ============================================================================
# Relation/Possession Roles (أدوار النسبة والملكية)
# ============================================================================

class RelationPossessionRole(Enum):
    """
    Relation and possession marker roles.

    Examples:
        ـيّ → Nisbah suffix
        ـي → Possessive pronoun
    """
    NISBAH_SUFFIX = "ياء نسبة"
    POSSESSIVE_SUFFIX = "ضمير ملكية"
    GENITIVE_LINK_CANDIDATE = "رابط جر محتمل"
    IDAFA_CONNECTOR_CANDIDATE = "رابط إضافة محتمل"
    LAM_OWNERSHIP = "لام الملكية"
    BI_INSTRUMENTAL_OR_CAUSAL = "باء آلة أو سببية"
    FI_LOCATIVE = "في ظرفية"


# ============================================================================
# Build/Inflect Roles (أدوار المبني والمعرب)
# ============================================================================

class BuildInflectRole(Enum):
    """
    Build vs inflect component roles.

    Examples:
        Final vowels may be i'rab or bina' markers
    """
    MABNI_COMPONENT_CANDIDATE = "جزء مبني محتمل"
    MURAB_COMPONENT_CANDIDATE = "جزء معرب محتمل"
    CASE_ENDING_CARRIER = "حامل علامة إعراب"
    FINAL_VOWEL_CARRIER = "حامل حركة أخيرة"
    IRAB_MARKER_CANDIDATE = "علامة إعراب محتملة"
    BUILDING_MARKER_CANDIDATE = "علامة بناء محتملة"


# ============================================================================
# Unified Functional Role Type
# ============================================================================

@dataclass(frozen=True)
class FunctionalRole:
    """
    A single functional role candidate.

    Attributes:
        role: The specific role enum value
        sort: The role sort category
        confidence: Role assignment confidence [0.0, 1.0]
        evidence: Evidence supporting this role
    """
    role: Enum  # One of the role enums above
    sort: RoleSort
    confidence: float = 0.5
    evidence: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be in [0.0, 1.0], got {self.confidence}")


# ============================================================================
# Role Set (Multiple Competing Roles)
# ============================================================================

@dataclass
class RoleSet:
    """
    Set of competing functional role candidates for a syllable span.

    Critical Law: Roles are NOT mutually exclusive until evidence blocks competitors.

    Example:
        بِ may simultaneously be:
            - HarfJarr (preposition)
            - RootCandidate (fa/ayn/lam radical)
            - PrefixCandidate (derivational prefix)
    """
    roles: List[FunctionalRole] = field(default_factory=list)

    def add_role(self, role: FunctionalRole):
        """Add a role candidate to the set."""
        self.roles.append(role)

    def get_by_sort(self, sort: RoleSort) -> List[FunctionalRole]:
        """Get all roles of a specific sort."""
        return [r for r in self.roles if r.sort == sort]

    def has_sort(self, sort: RoleSort) -> bool:
        """Check if set contains any role of this sort."""
        return any(r.sort == sort for r in self.roles)

    def best_role(self) -> Optional[FunctionalRole]:
        """Get highest confidence role, if any."""
        return max(self.roles, key=lambda r: r.confidence) if self.roles else None

    def __len__(self) -> int:
        return len(self.roles)


# ============================================================================
# Role Span (Functional Unit)
# ============================================================================

@dataclass
class RoleSpan:
    """
    A functional role span over one or more syllables.

    Critical: Some roles span multiple syllables (إنّ، استفعل، etc.)

    Attributes:
        span_id: Unique identifier
        syllables: Syllables participating in this role
        syllable_indices: Indices in original syllable sequence
        candidate_roles: Competing role candidates
        position: Position in word/structure (initial, medial, final)
        host_relation: Relation to adjacent elements
        evidence: Evidence supporting role assignment
        trace_u2: Trace back to U₂ syllables
        residuals: Blocking or warning residuals
        rank: Rank of role assignment (candidate → certificate)
    """
    span_id: str = field(default_factory=lambda: f"role-span-{uuid4().hex[:8]}")
    syllables: List[Syllable] = field(default_factory=list)
    syllable_indices: tuple[int, ...] = field(default_factory=tuple)
    candidate_roles: RoleSet = field(default_factory=RoleSet)
    position: str = "unknown"  # initial, medial, final, isolated
    host_relation: Dict[str, Any] = field(default_factory=dict)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    trace_u2: List[Syllable] = field(default_factory=list)
    residuals: List[Residual] = field(default_factory=list)
    rank: str = "role_zero"  # role_zero | role_candidate | role_hypothesis | role_strong_hypothesis | role_certificate | role_blocked

    def is_multi_syllable(self) -> bool:
        """Check if this span covers multiple syllables."""
        return len(self.syllables) > 1

    def has_blocker(self) -> bool:
        """Check if this span has blocking residuals."""
        return any(r.is_blocker() for r in self.residuals)

    def is_certified(self) -> bool:
        """Check if this role assignment is certified."""
        return self.rank == "role_certificate" and not self.has_blocker()

    def to_text(self) -> str:
        """Reconstruct text from syllables."""
        return ''.join(s.to_text() for s in self.syllables)


# ============================================================================
# Role Rank Levels (U₃ Rank System)
# ============================================================================

class RoleRank(Enum):
    """
    Rank levels for role assignments.

    Progression: zero → candidate → hypothesis → strong_hypothesis → certificate
    Demotion: certificate → hypothesis → candidate → blocked
    """
    ROLE_ZERO = "role_zero"                          # No role assigned
    ROLE_CANDIDATE = "role_candidate"                # Candidate role (multiple competitors)
    ROLE_HYPOTHESIS = "role_hypothesis"              # Hypothesis (some evidence)
    ROLE_STRONG_HYPOTHESIS = "role_strong_hypothesis"  # Strong hypothesis (strong evidence)
    ROLE_CERTIFICATE = "role_certificate"            # Certified (competitors blocked)
    ROLE_BLOCKED = "role_blocked"                    # Blocked by evidence


# ============================================================================
# Role Residual Codes (U₃ Residuals)
# ============================================================================

class RoleResidualCode(Enum):
    """
    Residual codes specific to U₃ functional role layer.

    These extend U₂ residuals with role-specific warnings/blockers.
    """
    ROLE_AMBIGUITY = "role_ambiguity"                      # Multiple competing roles
    CLOSED_CLASS_VS_ROOT_CONFLICT = "closed_class_vs_root_conflict"  # Particle vs radical conflict
    PREFIX_VS_RADICAL_CONFLICT = "prefix_vs_radical_conflict"  # Prefix vs radical conflict
    PRONOUN_VS_SUFFIX_CONFLICT = "pronoun_vs_suffix_conflict"  # Pronoun vs suffix conflict
    DEFINITE_ARTICLE_AMBIGUITY = "definite_article_ambiguity"  # ال ambiguity
    TANWEEN_ROLE_DEFERRED = "tanween_role_deferred"        # Tanween role deferred
    CASE_MARKER_DEFERRED = "case_marker_deferred"          # Case marker deferred
    GENDER_MARKER_DEFERRED = "gender_marker_deferred"      # Gender marker deferred
    NUMBER_MARKER_DEFERRED = "number_marker_deferred"      # Number marker deferred
    VERB_PREFIX_AMBIGUITY = "verb_prefix_ambiguity"        # Verb prefix ambiguity
    WEAK_LETTER_ROLE_AMBIGUITY = "weak_letter_role_ambiguity"  # Weak letter role ambiguity
    HOST_NOT_IDENTIFIED = "host_not_identified"            # Host relation unknown
    SPAN_BOUNDARY_UNCLEAR = "span_boundary_unclear"        # Span boundary unclear
    LEXICON_MISSING = "lexicon_missing"                    # Closed-class lexicon not available
    PATTERN_NOT_YET_AVAILABLE = "pattern_not_yet_available"  # Pattern evidence not available


# ============================================================================
# Helper Functions
# ============================================================================

def create_role_span(
    syllables: List[Syllable],
    indices: tuple[int, ...],
    position: str = "unknown"
) -> RoleSpan:
    """
    Create a role span from syllables.

    Args:
        syllables: List of syllables in this span
        indices: Indices in original syllable sequence
        position: Position in structure (initial, medial, final)

    Returns:
        RoleSpan with initialized fields
    """
    return RoleSpan(
        syllables=syllables,
        syllable_indices=indices,
        position=position,
        trace_u2=syllables.copy()
    )


def is_complete_one_u3(role_span: RoleSpan) -> bool:
    """
    Check if role span is minimally complete within U₃.

    CompleteOne₃ criteria:
        - Has at least one syllable
        - Has at least one candidate role
        - Trace to U₂ preserved
        - No blocking residuals

    Args:
        role_span: Role span to check

    Returns:
        True if minimally complete in U₃
    """
    return (
        len(role_span.syllables) > 0 and
        len(role_span.candidate_roles) > 0 and
        len(role_span.trace_u2) > 0 and
        not role_span.has_blocker()
    )
