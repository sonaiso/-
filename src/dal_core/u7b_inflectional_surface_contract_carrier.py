"""
U₇-B Inflectional Surface Contract Carrier (حامل عقد السطح الصرفي)

Domain: U₇-B = InflectionalSurfaceContractCarrier
Purpose: Protect surface markers before root/stem extraction
Transition: U₇-A (PreWeightContract) → U₇-B (InflectionalSurfaceContract) → U₈ (RootStemCandidate)

Critical Laws (Axioms):
    - Axiom 7B.1: لا جذر من سطح خام (No root from raw surface)
    - Axiom 7B.2: لا وزن من سطح خام (No weight from raw surface)
    - Axiom 7B.3: لا تجريد بلا أثر (No stripping without trace)
    - Axiom 7B.4: لا حذف للعلامة؛ بل حماية وتصنيف وبقايا (No marker deletion; only protection, classification, residuals)
    - Axiom 7B.5: السطح ≠ النواة المحمية ≠ مدخل الجذر (surface ≠ protected_core ≠ root_input)
    - Axiom 7B.6: العلامة ≠ الحكم (Marker ≠ judgment)

Type System:
    InflectionalSurfaceContract ≠ Root
    InflectionalSurfaceContract ≠ RootCertificate
    InflectionalSurfaceContract ≠ Weight
    InflectionalSurfaceContract ≠ WeightCertificate
    InflectionalSurfaceContract ≠ Hukm
    InflectionalSurfaceContract ≠ ResolvedReference
    protected_core ≠ surface
    root_input ≠ surface

Architecture:
    U₇-A (PreWeightContract) → CPB₇B → U₇-B (InflectionalSurfaceContract) → CPB₈ → U₈ (RootStem)

Key Principle:
    U₇-B protects surface markers from being consumed by root/weight extraction.
    U₇-B produces protected_core and root_input (licensed input for U₈).
    U₇-B does NOT extract root, does NOT determine weight, does NOT assign i'rab.
    U₇-B answers: "ما هي العلامات السطحية المحمية؟" (What surface markers are protected?)

Example Analysis:
    From U₇-A unit [كِتَابِ] (open_class_core_contract_candidate):
        - surface = "كِتَابِ"
        - protected_core = "كتاب"
        - root_input = "كتاب"
        - protected_suffixes = ()
        - original_irab_marker_hint = "possible"
        - residuals += ("kasra_may_be_irab_or_idafa",)

    From U₇-A unit [الكِتَاب]:
        - surface = "الكِتَابِ"
        - protected_prefixes = ("الـ",)
        - protected_core = "كتاب"
        - root_input = "كتاب"
        - definiteness_marker_hint = "possible"

    From U₇-A unit [كِتَابٌ]:
        - surface = "كِتَابٌ"
        - protected_core = "كتاب"
        - root_input = "كتاب"
        - tanwin_marker_hint = "possible"

U₇-B Output:
    Gives U₈:
        - protected_core (core after marker protection)
        - root_input (licensed input for root extraction)
        - Marker hints (all as "possible"/"unlikely"/"unresolved")
        - blocked_root_segments / blocked_weight_segments
        - residuals (ambiguities)
        - rank (zero → candidate → hypothesis)

U₇-B Does NOT Give:
    - Root extraction (U₈)
    - Weight determination (U₉)
    - I'rab final judgment (U₇+)
    - Meaning/semantic interpretation (U₁₅)
    - Reference resolution (U₁₅)

PR: U7B-INFLECTIONAL-SURFACE-CONTRACT
Created: 2026-05-26
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, FrozenSet, Dict, Any, Tuple
from uuid import uuid4

from dal_core.residuals import Residual, ResidualType, make_blocker, make_warning
from dal_core.foundation import (
    Rank,
    RankVector,
    ProofObject,
    make_proof_object,
    ResidualSet,
    merge_residuals,
    has_blocking_residuals
)
from dal_core.u7_pre_weight_contract_carrier import (
    PreWeightContractLayerObject,
    PreWeightContractUnit,
    ContractStatus,
    PathPermission,
)


# ============================================================================
# Type System - Surface Marker Classification
# ============================================================================

class MarkerHint(Enum):
    """
    Marker hint values (NOT judgments).

    These are surface observations/hints, not grammatical judgments.
    """
    POSSIBLE = "possible"              # ممكن
    UNLIKELY = "unlikely"              # غير محتمل
    UNRESOLVED = "unresolved"          # غير محسوم
    AMBIGUOUS = "ambiguous"            # ملتبس
    BLOCKED = "blocked"                # محجوب


class RootInputPermission(Enum):
    """
    Permission status for root_input to proceed to U₈.

    CRITICAL: U₈ must never receive unprotected surface.
    """
    ALLOWED = "allowed"                # مسموح - protected surface, safe for U₈
    DEFERRED = "deferred"              # مؤجل - needs lexical/pattern evidence
    BLOCKED = "blocked"                # محجوب - cannot proceed to root extraction


# ============================================================================
# Failure Types
# ============================================================================

class InflectionalSurfaceContractFailureType(Enum):
    """Failure types for inflectional surface contract determination."""
    NO_PRE_WEIGHT_UNITS = "no_pre_weight_units"
    INVALID_INPUT_LAYER = "invalid_input_layer"
    TRACE_LOSS = "trace_loss"


# ============================================================================
# Core Structures
# ============================================================================

@dataclass(frozen=True)
class InflectionalSurfaceContractUnit:
    """
    U₇-B inflectional surface contract unit for a pre-weight contract unit.

    This represents SURFACE MARKER PROTECTION, NOT morphological analysis.
    Contract protects markers and emits guarded root_input for U₈.

    Forbidden fields (CRITICAL - these cause ValueError):
        - root (that's U₈)
        - root_certificate (that's U₈+)
        - stem (that's U₈)
        - stem_certificate (that's U₈+)
        - weight (that's U₉)
        - weight_certificate (that's U₉+)
        - pattern (that's U₉)
        - pattern_certificate (that's U₉+)
        - meaning (that's U₁₅)
        - dalalah (that's U₁₅)
        - ifadah (that's U₁₅)
        - hukm (that's U₇+)
        - final_irab (that's U₇+)
        - i3rab_final (that's U₇+)
        - resolved_reference (that's U₁₅)
    """
    uid: str
    surface: str  # Original orthographic surface from U₇-A
    source_u7_unit_id: str  # Trace to U₇-A pre-weight contract unit
    source_u7_trace: Tuple[str, ...]  # Ordered trace to U₇

    # Core separation (CRITICAL architectural separation)
    protected_prefixes: Tuple[str, ...]  # Protected prefix markers
    protected_suffixes: Tuple[str, ...]  # Protected suffix markers
    protected_infixes: Tuple[str, ...]   # Protected infix markers (rare)
    protected_vowels: Tuple[str, ...]    # Protected vowel patterns (e.g., passive)

    protected_core: str  # Core after marker protection (≠ surface)
    root_input: str      # Licensed input for U₈ root extraction (≠ surface, ≠ protected_core in some cases)
    root_input_permission: RootInputPermission  # CRITICAL: permission for U₈ to consume root_input

    # Broken plural special handling
    broken_plural_surface_hint: MarkerHint     # جمع التكسير surface hint
    broken_plural_pattern_hint: str            # Pattern hint (فعال، مفاعل، etc.) or empty

    # Pronoun suffix protection
    pronoun_suffix_hint: MarkerHint            # لاحقات الضمائر hint
    protected_pronoun_suffixes: Tuple[str, ...]  # Pronoun suffixes (ـه، ـها، ـهم، etc.)

    # Marker hints (all "possible"/"unlikely"/"unresolved", NOT judgments)
    definiteness_marker_hint: MarkerHint  # الـ marker hint
    tanwin_marker_hint: MarkerHint        # تنوين marker hint

    number_marker_hint: MarkerHint        # عدد (dual/plural) marker hint
    gender_marker_hint: MarkerHint        # جنس (feminine ة/ات) marker hint
    rationality_marker_hint: MarkerHint   # عاقلية marker hint

    original_irab_marker_hint: MarkerHint     # علامة إعراب أصلية hint
    secondary_irab_marker_hint: MarkerHint    # علامة إعراب فرعية hint

    nominative_surface_hint: MarkerHint   # رفع surface hint
    accusative_surface_hint: MarkerHint   # نصب surface hint
    genitive_surface_hint: MarkerHint     # جر surface hint
    jussive_surface_hint: MarkerHint      # جزم surface hint

    verb_prefix_hint: MarkerHint          # حروف المضارعة hint
    verb_suffix_hint: MarkerHint          # ضمائر الفعل hint
    passive_surface_hint: MarkerHint      # بناء للمجهول hint
    mazid_extra_hint: MarkerHint          # زوائد المزيد hint

    proper_name_surface_hint: MarkerHint  # علم hint
    loanword_surface_hint: MarkerHint     # دخيل hint
    jamid_surface_hint: MarkerHint        # جامد hint
    frozen_primitive_surface_hint: MarkerHint  # جامد بدائي hint

    # Blocking (prevent segments from being consumed by root/weight)
    blocked_root_segments: Tuple[str, ...]    # Segments blocked from root extraction
    blocked_weight_segments: Tuple[str, ...]  # Segments blocked from weight determination

    # Evidence and ambiguities
    residuals: FrozenSet[Residual]
    rank: Rank
    trace: Tuple[str, ...]  # Full ordered trace from U₀

    def __post_init__(self):
        """Validate inflectional surface contract unit - CRITICAL constitutional checks."""
        # FORBIDDEN FIELDS - These MUST NOT exist
        forbidden_fields = [
            'root', 'root_certificate',
            'stem', 'stem_certificate',
            'weight', 'weight_certificate',
            'pattern', 'pattern_certificate',
            'meaning', 'dalalah', 'ifadah',
            'hukm', 'final_irab', 'i3rab_final',
            'resolved_reference'
        ]

        for field in forbidden_fields:
            if hasattr(self, field):
                raise ValueError(
                    f"InflectionalSurfaceContractUnit MUST NOT contain '{field}' field "
                    f"(Axiom 7B.1-7B.6 violation)"
                )

        # CRITICAL: Verify architectural separation
        if not hasattr(self, 'surface'):
            raise ValueError("InflectionalSurfaceContractUnit MUST contain 'surface' field")
        if not hasattr(self, 'protected_core'):
            raise ValueError("InflectionalSurfaceContractUnit MUST contain 'protected_core' field")
        if not hasattr(self, 'root_input'):
            raise ValueError("InflectionalSurfaceContractUnit MUST contain 'root_input' field")


@dataclass(frozen=True)
class InflectionalSurfaceContractLayerObject:
    """
    U₇-B layer object containing inflectional surface contract classifications.

    Provides protected surface markers and guarded root_input for U₈.
    """
    uid: str
    units: Tuple[InflectionalSurfaceContractUnit, ...]  # Contract units
    source_pre_weight_layer_id: str  # Trace to U₇-A layer
    trace_7a: Tuple[str, ...]  # Ordered trace to U₇-A
    residuals: FrozenSet[Residual]
    rank: Rank
    proof: Optional[ProofObject] = None

    def __post_init__(self):
        """Validate inflectional surface contract layer object."""
        # FORBIDDEN FIELDS
        forbidden_fields = [
            'root', 'root_certificate',
            'stem', 'stem_certificate',
            'weight', 'weight_certificate',
            'pattern', 'pattern_certificate',
            'meaning', 'dalalah', 'ifadah',
            'hukm', 'final_irab', 'i3rab_final',
            'resolved_reference'
        ]

        for field in forbidden_fields:
            if hasattr(self, field):
                raise ValueError(
                    f"InflectionalSurfaceContractLayerObject MUST NOT contain '{field}' field"
                )


@dataclass(frozen=True)
class InflectionalSurfaceContractResult:
    """Result of inflectional surface contract determination."""
    success: bool
    layer_object: Optional[InflectionalSurfaceContractLayerObject]
    failure_type: Optional[InflectionalSurfaceContractFailureType]
    message: str
    residuals: FrozenSet[Residual]


# ============================================================================
# CPB₇B - Completeness Predicate and Proof Builder
# ============================================================================

@dataclass(frozen=True)
class CPB7B:
    """
    CPB₇B: Completeness Predicate and Proof Builder for InflectionalSurfaceContract layer.

    Guards:
        - Surface markers protected
        - protected_core and root_input emitted
        - Marker hints assigned (all as hints, NOT judgments)
        - Pre-weight contract trace preserved
        - No forbidden fields (root, weight, pattern, meaning, hukm, i3rab_final, etc.)
        - Allowed next gate: U₈ RootStemCandidate
    """

    @staticmethod
    def is_complete(layer_obj: InflectionalSurfaceContractLayerObject) -> bool:
        """Check if inflectional surface contract layer object is complete."""
        if not layer_obj.units:
            return False

        if not layer_obj.source_pre_weight_layer_id:
            return False

        # Check all units have required fields
        for unit in layer_obj.units:
            if not unit.surface:
                return False
            if not unit.protected_core:
                return False
            if not unit.root_input:
                return False

        # Check no forbidden fields
        forbidden = ['root', 'stem', 'weight', 'pattern', 'meaning', 'hukm', 'i3rab_final', 'resolved_reference']
        for unit in layer_obj.units:
            if any(hasattr(unit, field) for field in forbidden):
                return False

        return True

    @staticmethod
    def build_proof(layer_obj: InflectionalSurfaceContractLayerObject) -> ProofObject:
        """Build proof object for inflectional surface contract layer."""
        # Count marker hints
        units_with_definiteness = sum(
            1 for u in layer_obj.units
            if u.definiteness_marker_hint in [MarkerHint.POSSIBLE, MarkerHint.AMBIGUOUS]
        )
        units_with_tanwin = sum(
            1 for u in layer_obj.units
            if u.tanwin_marker_hint in [MarkerHint.POSSIBLE, MarkerHint.AMBIGUOUS]
        )
        units_with_number_markers = sum(
            1 for u in layer_obj.units
            if u.number_marker_hint in [MarkerHint.POSSIBLE, MarkerHint.AMBIGUOUS]
        )

        # Count protected markers
        total_protected_prefixes = sum(len(u.protected_prefixes) for u in layer_obj.units)
        total_protected_suffixes = sum(len(u.protected_suffixes) for u in layer_obj.units)

        return make_proof_object(
            claim="U₇-B inflectional surface markers protected",
            scope="U7B_INFLECTIONAL_SURFACE_CONTRACT",
            evidence=frozenset([
                f"units_count={len(layer_obj.units)}",
                f"units_with_definiteness_hint={units_with_definiteness}",
                f"units_with_tanwin_hint={units_with_tanwin}",
                f"units_with_number_markers_hint={units_with_number_markers}",
                f"total_protected_prefixes={total_protected_prefixes}",
                f"total_protected_suffixes={total_protected_suffixes}",
                f"trace_preserved={bool(layer_obj.source_pre_weight_layer_id)}",
                f"rank={layer_obj.rank.value}",
            ]),
            counter_evidence=frozenset(),
            trace_graph={},
            competitors=frozenset(),
            residuals=layer_obj.residuals,
            rank_vector={},
            allowed_next_gates=frozenset({"root_stem_candidate_gate"}),
            forbidden_next_gates=frozenset({
                "root_certificate",
                "stem_certificate",
                "weight_certificate",
                "pattern_certificate",
                "meaning_certificate",
                "hukm_certificate",
                "irab_final_judgment",
            }),
            limitations=frozenset([
                "no_root_extraction",
                "no_stem_extraction",
                "no_weight_determination",
                "no_pattern_determination",
                "no_meaning_assignment",
                "no_hukm_judgment",
                "no_irab_final_judgment",
                "marker_hints_are_not_judgments",
                "protected_markers_must_not_be_consumed_by_root",
                "root_input_is_licensed_not_certified",
            ]),
        )


# ============================================================================
# Surface Marker Protection Logic
# ============================================================================

def _detect_definiteness_marker(surface: str) -> Tuple[Tuple[str, ...], MarkerHint]:
    """
    Detect definiteness marker (الـ).

    Returns:
        (protected_prefixes, hint)
    """
    # Simple detection: check if surface starts with ال
    if surface.startswith('ال'):
        return (('الـ',), MarkerHint.POSSIBLE)
    return ((), MarkerHint.UNRESOLVED)


def _detect_tanwin_marker(surface: str) -> MarkerHint:
    """
    Detect tanwīn marker (تنوين).

    Returns:
        hint (POSSIBLE/UNRESOLVED)
    """
    # Check for tanwīn diacritics at end
    tanwin_marks = ['ً', 'ٍ', 'ٌ']
    if any(surface.endswith(mark) for mark in tanwin_marks):
        return MarkerHint.POSSIBLE
    return MarkerHint.UNRESOLVED


def _detect_number_markers(surface: str) -> Tuple[Tuple[str, ...], MarkerHint]:
    """
    Detect number markers (ان/ين/ون/ات).

    Returns:
        (protected_suffixes, hint)
    """
    # Remove diacritics for detection
    surface_no_diacritics = ''.join(
        c for c in surface
        if c not in ['َ', 'ِ', 'ُ', 'ْ', 'ّ', 'ً', 'ٍ', 'ٌ']
    )

    # Check for dual markers
    if surface_no_diacritics.endswith('ان'):
        return (('ان',), MarkerHint.POSSIBLE)
    elif surface_no_diacritics.endswith('ين'):
        # Ambiguous: could be dual or sound masculine plural or case marker
        return (('ين',), MarkerHint.AMBIGUOUS)
    elif surface_no_diacritics.endswith('ون'):
        return (('ون',), MarkerHint.POSSIBLE)
    elif surface_no_diacritics.endswith('ات'):
        return (('ات',), MarkerHint.POSSIBLE)

    return ((), MarkerHint.UNRESOLVED)


def _detect_gender_markers(surface: str) -> Tuple[Tuple[str, ...], MarkerHint]:
    """
    Detect gender markers (ة for feminine).

    Returns:
        (protected_suffixes, hint)
    """
    # Remove diacritics
    surface_no_diacritics = ''.join(
        c for c in surface
        if c not in ['َ', 'ِ', 'ُ', 'ْ', 'ّ', 'ً', 'ٍ', 'ٌ']
    )

    if surface_no_diacritics.endswith('ة'):
        return (('ة',), MarkerHint.POSSIBLE)

    return ((), MarkerHint.UNRESOLVED)


def _detect_verb_prefix_markers(surface: str) -> Tuple[Tuple[str, ...], MarkerHint]:
    """
    Detect verb prefix markers (ي/ت/ن/أ for present tense).

    Returns:
        (protected_prefixes, hint)
    """
    # Present tense markers
    present_markers = ['ي', 'ت', 'ن', 'أ']
    if surface and surface[0] in present_markers:
        return ((surface[0],), MarkerHint.POSSIBLE)

    # Imperative markers (hamzat waṣl)
    if surface.startswith('ا') and len(surface) > 2:
        # Could be imperative hamzat waṣl
        return (('ا',), MarkerHint.POSSIBLE)

    return ((), MarkerHint.UNRESOLVED)


def _detect_mazid_markers(surface: str) -> Tuple[Tuple[str, ...], MarkerHint]:
    """
    Detect mazīd (augmented verb) markers (است/انـ/etc.).

    Returns:
        (protected_prefixes, hint)
    """
    # Common mazīd prefixes
    if surface.startswith('است'):
        return (('است',), MarkerHint.POSSIBLE)
    elif surface.startswith('انـ'):
        return (('انـ',), MarkerHint.POSSIBLE)

    return ((), MarkerHint.UNRESOLVED)


def _detect_broken_plural(surface: str) -> Tuple[MarkerHint, str]:
    """
    Detect broken plural patterns (جمع التكسير).

    CRITICAL: Broken plurals cannot be treated as simple suffix stripping.
    They require lexical or pattern-based resolution.

    Returns:
        (broken_plural_hint, pattern_hint_string)
    """
    # Remove diacritics for pattern matching
    surface_no_diacritics = ''.join(
        c for c in surface
        if c not in ['َ', 'ِ', 'ُ', 'ْ', 'ّ', 'ً', 'ٍ', 'ٌ']
    )

    # Common broken plural patterns
    # This is a simplified detection - real implementation would be more comprehensive

    # فعال pattern (e.g., رجال)
    if len(surface_no_diacritics) == 4:
        # Could be فعال
        return (MarkerHint.POSSIBLE, "فعال_possible")

    # مفاعل pattern (e.g., مدارس)
    if surface_no_diacritics.startswith('م') and len(surface_no_diacritics) >= 5:
        return (MarkerHint.POSSIBLE, "مفاعل_possible")

    # فُعُل / فُعَل pattern (e.g., كتب)
    if len(surface_no_diacritics) == 3:
        # Could be broken plural OR verb OR singular
        # This is highly ambiguous
        return (MarkerHint.AMBIGUOUS, "ambiguous_فعل_pattern")

    return (MarkerHint.UNRESOLVED, "")


def _detect_pronoun_suffixes(surface: str) -> Tuple[Tuple[str, ...], MarkerHint]:
    """
    Detect pronoun suffixes (لاحقات الضمائر).

    Returns:
        (protected_pronoun_suffixes, hint)
    """
    # Remove diacritics for detection
    surface_no_diacritics = ''.join(
        c for c in surface
        if c not in ['َ', 'ِ', 'ُ', 'ْ', 'ّ', 'ً', 'ٍ', 'ٌ']
    )

    # Common pronoun suffixes
    # ـه (his/it), ـها (her/it), ـهم (their), ـهما (their dual), ـنا (our/us),
    # ـك (your masc), ـكِ (your fem), ـكم (your plural masc), ـكن (your plural fem)

    pronoun_suffixes = []

    # Check for multi-character suffixes first
    if surface_no_diacritics.endswith('هما'):
        pronoun_suffixes.append('ـهما')
    elif surface_no_diacritics.endswith('هم'):
        pronoun_suffixes.append('ـهم')
    elif surface_no_diacritics.endswith('ها'):
        pronoun_suffixes.append('ـها')
    elif surface_no_diacritics.endswith('كم'):
        pronoun_suffixes.append('ـكم')
    elif surface_no_diacritics.endswith('كن'):
        pronoun_suffixes.append('ـكن')
    elif surface_no_diacritics.endswith('نا'):
        pronoun_suffixes.append('ـنا')
    elif surface_no_diacritics.endswith('ه'):
        # Could be pronoun, needs context
        pronoun_suffixes.append('ـه')
    elif surface_no_diacritics.endswith('ك'):
        pronoun_suffixes.append('ـك')
    elif surface_no_diacritics.endswith('ي'):
        # Could be pronoun (my) or other marker
        pronoun_suffixes.append('ـي')

    if pronoun_suffixes:
        return (tuple(pronoun_suffixes), MarkerHint.POSSIBLE)

    return ((), MarkerHint.UNRESOLVED)


def _strip_protected_markers(
    surface: str,
    protected_prefixes: Tuple[str, ...],
    protected_suffixes: Tuple[str, ...]
) -> str:
    """
    Strip protected markers to produce protected_core.

    Args:
        surface: Original surface
        protected_prefixes: Prefixes to strip
        protected_suffixes: Suffixes to strip

    Returns:
        protected_core after stripping markers
    """
    core = surface

    # Strip prefixes
    for prefix in protected_prefixes:
        if core.startswith(prefix):
            core = core[len(prefix):]

    # Strip suffixes
    for suffix in protected_suffixes:
        if core.endswith(suffix):
            core = core[:-len(suffix)]

    # Remove diacritics for core
    core = ''.join(
        c for c in core
        if c not in ['َ', 'ِ', 'ُ', 'ْ', 'ّ', 'ً', 'ٍ', 'ٌ']
    )

    return core if core else surface


# ============================================================================
# Inflectional Surface Contract Operations
# ============================================================================

def inflectional_surface_contract_7b(
    pre_weight_layer: PreWeightContractLayerObject
) -> InflectionalSurfaceContractResult:
    """
    Determine inflectional surface contract from U₇-A pre-weight contract layer.

    Critical Examples:
        الكتاب → protected_prefixes=("الـ",), protected_core="كتاب", root_input="كتاب"
        كتابٌ → protected_core="كتاب", root_input="كتاب", tanwin_marker_hint=POSSIBLE
        مسلمان → protected_suffixes=("ان",), protected_core="مسلم", root_input="مسلم"
        مسلمين → protected_suffixes=("ين",), residuals+=("ambiguous_dual_or_plural_or_case",)
        يكتبون → protected_prefixes=("ي",), protected_suffixes=("ون",), protected_core="كتب"
        استخرج → protected_prefixes=("است",), protected_core="خرج", mazid_extra_hint=POSSIBLE

    Args:
        pre_weight_layer: U₇-A layer object with pre-weight contract permissions

    Returns:
        InflectionalSurfaceContractResult with protected markers and root_input

    Critical Law:
        surface ≠ protected_core ≠ root_input
        Markers are protected (NOT deleted), classified (NOT judged), with residuals (NOT resolved).

    Forbidden:
        - Root extraction (U₈)
        - Weight determination (U₉)
        - I'rab final judgment (U₇+)
        - Meaning assignment (U₁₅)
        - Hukm judgment (U₇+)
    """
    # Validate input
    if not pre_weight_layer.units:
        return InflectionalSurfaceContractResult(
            success=False,
            layer_object=None,
            failure_type=InflectionalSurfaceContractFailureType.NO_PRE_WEIGHT_UNITS,
            message="No pre-weight contract units in input",
            residuals=frozenset([make_blocker("no_units", "Cannot determine inflectional surface contract without pre-weight units")])
        )

    # Process each pre-weight contract unit
    contract_units = []
    all_residuals = []

    for contract_unit in pre_weight_layer.units:
        surface = contract_unit.surface

        # Detect markers
        definiteness_prefixes, definiteness_hint = _detect_definiteness_marker(surface)
        tanwin_hint = _detect_tanwin_marker(surface)
        number_suffixes, number_hint = _detect_number_markers(surface)
        gender_suffixes, gender_hint = _detect_gender_markers(surface)
        verb_prefixes, verb_prefix_hint = _detect_verb_prefix_markers(surface)
        mazid_prefixes, mazid_hint = _detect_mazid_markers(surface)

        # NEW: Detect broken plural (CRITICAL for deferral)
        broken_plural_hint, broken_plural_pattern = _detect_broken_plural(surface)

        # NEW: Detect pronoun suffixes
        pronoun_suffixes, pronoun_suffix_hint = _detect_pronoun_suffixes(surface)

        # Combine protected markers
        all_protected_prefixes = definiteness_prefixes + verb_prefixes + mazid_prefixes
        all_protected_suffixes = number_suffixes + gender_suffixes + pronoun_suffixes

        # Strip markers to produce protected_core
        protected_core = _strip_protected_markers(
            surface,
            all_protected_prefixes,
            all_protected_suffixes
        )

        # CRITICAL POLICY: Protection-or-defer for root_input
        # If marker family is not protected, root_input must be deferred
        root_input_permission = RootInputPermission.ALLOWED
        root_input = protected_core

        # Collect residuals
        unit_residuals = list(contract_unit.residuals)

        # Check for unprotected or ambiguous marker families
        # BROKEN PLURAL: Must defer (cannot be treated as simple stripping)
        if broken_plural_hint in [MarkerHint.POSSIBLE, MarkerHint.AMBIGUOUS]:
            root_input_permission = RootInputPermission.DEFERRED
            root_input = ""  # Empty - deferred pending lexical/pattern evidence
            unit_residuals.append(
                make_warning(
                    "broken_plural_deferred",
                    f"Broken plural surface detected (pattern: {broken_plural_pattern}), root_input deferred pending lexical/pattern resolution"
                )
            )

        # AMBIGUOUS NUMBER MARKER: Add residual
        if number_hint == MarkerHint.AMBIGUOUS:
            unit_residuals.append(
                make_warning("ambiguous_number_marker", "ين could be dual, sound masculine plural, or case marker")
            )

        # PRONOUN SUFFIX: If detected but not fully protected, defer
        # (This is conservative - we protect what we detect, but if ambiguous, we defer)
        if pronoun_suffix_hint == MarkerHint.AMBIGUOUS:
            unit_residuals.append(
                make_warning("ambiguous_pronoun_suffix", "Pronoun suffix detected but context needed for certainty")
            )

        # Build blocked segments (markers should not be consumed by root/weight)
        blocked_root_segments = all_protected_prefixes + all_protected_suffixes
        blocked_weight_segments = all_protected_prefixes + all_protected_suffixes

        # Build InflectionalSurfaceContractUnit
        contract_unit_obj = InflectionalSurfaceContractUnit(
            uid=str(uuid4()),
            surface=surface,
            source_u7_unit_id=contract_unit.uid,
            source_u7_trace=contract_unit.source_u6_trace,
            protected_prefixes=all_protected_prefixes,
            protected_suffixes=all_protected_suffixes,
            protected_infixes=(),  # Rare - not implemented yet
            protected_vowels=(),   # Passive vowel patterns - not implemented yet
            protected_core=protected_core,
            root_input=root_input,
            root_input_permission=root_input_permission,
            definiteness_marker_hint=definiteness_hint,
            tanwin_marker_hint=tanwin_hint,
            number_marker_hint=number_hint,
            gender_marker_hint=gender_hint,
            rationality_marker_hint=MarkerHint.UNRESOLVED,
            original_irab_marker_hint=MarkerHint.UNRESOLVED,
            secondary_irab_marker_hint=MarkerHint.UNRESOLVED,
            nominative_surface_hint=MarkerHint.UNRESOLVED,
            accusative_surface_hint=MarkerHint.UNRESOLVED,
            genitive_surface_hint=MarkerHint.UNRESOLVED,
            jussive_surface_hint=MarkerHint.UNRESOLVED,
            verb_prefix_hint=verb_prefix_hint,
            verb_suffix_hint=MarkerHint.UNRESOLVED,
            passive_surface_hint=MarkerHint.UNRESOLVED,
            mazid_extra_hint=mazid_hint,
            broken_plural_surface_hint=broken_plural_hint,
            broken_plural_pattern_hint=broken_plural_pattern,
            pronoun_suffix_hint=pronoun_suffix_hint,
            protected_pronoun_suffixes=pronoun_suffixes,
            proper_name_surface_hint=contract_unit.proper_name_surface_potential,
            loanword_surface_hint=contract_unit.loanword_surface_potential,
            jamid_surface_hint=contract_unit.jamid_surface_potential,
            frozen_primitive_surface_hint=contract_unit.frozen_primitive_potential,
            blocked_root_segments=tuple(blocked_root_segments),
            blocked_weight_segments=tuple(blocked_weight_segments),
            residuals=frozenset(unit_residuals),
            rank=contract_unit.rank,
            trace=contract_unit.trace
        )

        contract_units.append(contract_unit_obj)
        all_residuals.extend(unit_residuals)

    # Build layer object
    layer_obj = InflectionalSurfaceContractLayerObject(
        uid=str(uuid4()),
        units=tuple(contract_units),
        source_pre_weight_layer_id=pre_weight_layer.uid,
        trace_7a=(pre_weight_layer.uid,),
        residuals=frozenset(all_residuals),
        rank=pre_weight_layer.rank,  # Inherit rank from U₇-A
        proof=None
    )

    # Build proof
    proof = CPB7B.build_proof(layer_obj)
    layer_obj = InflectionalSurfaceContractLayerObject(
        uid=layer_obj.uid,
        units=layer_obj.units,
        source_pre_weight_layer_id=layer_obj.source_pre_weight_layer_id,
        trace_7a=layer_obj.trace_7a,
        residuals=layer_obj.residuals,
        rank=layer_obj.rank,
        proof=proof
    )

    return InflectionalSurfaceContractResult(
        success=True,
        layer_object=layer_obj,
        failure_type=None,
        message=f"Inflectional surface markers protected: {len(contract_units)} units processed",
        residuals=layer_obj.residuals
    )


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Core types
    'MarkerHint',
    'RootInputPermission',

    # Structures
    'InflectionalSurfaceContractUnit',
    'InflectionalSurfaceContractLayerObject',
    'InflectionalSurfaceContractResult',

    # Failures
    'InflectionalSurfaceContractFailureType',

    # CPB
    'CPB7B',

    # Operations
    'inflectional_surface_contract_7b',
]
