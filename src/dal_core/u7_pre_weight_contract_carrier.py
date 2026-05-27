"""
U₇ Pre-Weight Contract Carrier (حامل عقد ما قبل الوزن)

Domain: U₇ = PreWeightContractCarrier
Purpose: Contract/permission gate before morphological analysis (root/weight extraction)
Transition: U₆ (MabniClosedClass) → U₇ (PreWeightContract) → U₈ (RootStem)

Critical Laws (Axioms):
    - Axiom 7.1: لا جذر قبل عقد ما قبل الوزن (No root before pre-weight contract)
    - Axiom 7.2: لا وزن قبل عقد ما قبل الوزن (No weight before pre-weight contract)
    - Axiom 7.3: المفتوح ≠ الإذن التلقائي (Open-class ≠ automatic permission)
    - Axiom 7.4: العقد ≠ الشهادة (Contract ≠ certificate)
    - Axiom 7.5: العقد ≠ الاستخراج (Contract ≠ extraction)
    - Axiom 7.6: المغلق المبني يحجب المسار (Closed-class mabni blocks path)

Type System:
    PreWeightContract ≠ Root
    PreWeightContract ≠ RootCertificate
    PreWeightContract ≠ Stem
    PreWeightContract ≠ StemCertificate
    PreWeightContract ≠ Weight
    PreWeightContract ≠ WeightCertificate
    PreWeightContract ≠ Pattern
    PreWeightContract ≠ PatternCertificate
    PreWeightContract ≠ Meaning
    PreWeightContract ≠ Hukm
    PreWeightContract ≠ ResolvedReference

Architecture:
    U₆ (MabniClosedClassLayerObject) → CPB₇ → U₇ (PreWeightContractLayerObject) → CPB₈ → RootStem

Key Principle:
    U₇ reads U₆ closed/open classification and determines path permissions.
    U₇ does NOT extract root, does NOT determine weight, does NOT certify meaning/hukm.
    U₇ answers: "هل يجوز أصلاً أن أفتح مسار الجذر/الوزن؟" (Is the path even permitted?)

Example Analysis:
    From U₆ units [وَ, بِ, كِتَاب, ـهِمْ]:
        - وَ → closed_class_blocked (root blocked, weight blocked)
        - بِ → closed_class_blocked (root blocked, weight blocked)
        - كِتَاب → open_core_contract_candidate (root possible, weight possible, no extraction yet)
        - ـهِمْ → closed_class_blocked (root blocked, weight blocked, pronoun path preserved)

U₇ Output:
    Gives U₈:
        - Contract approvals (open-class units permitted for root/stem analysis)
        - Contract blocks (closed-class units NOT permitted)
        - Contract deferrals (proper names, loanwords, need evidence)
        - Path permissions (possible, blocked, deferred, unresolved)
        - Residuals (ambiguities, insufficient evidence)
        - Rank (zero → candidate → hypothesis → certificate)

U₇ Does NOT Give:
    - Root extraction (U₈)
    - Stem extraction (U₈)
    - Weight/pattern determination (U₉)
    - Meaning/semantic interpretation (U₁₅)
    - Reference resolution (U₁₅)
    - Grammatical hukm (U₇+)

PR: U7-PRE-WEIGHT-CONTRACT
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
from dal_core.u6_mabni_closed_class_carrier import (
    MabniClosedClassLayerObject,
    MabniClosedClassUnit,
    MabniClosedClassType,
    ClosedClassSubtype
)


# ============================================================================
# Type System - Pre-Weight Contract Classification
# ============================================================================

class ContractStatus(Enum):
    """
    Contract status for pre-weight morphological path.

    This is PATH PERMISSION classification, not morphological analysis.
    U₇ determines if path is permitted, NOT what the root/weight is.
    """
    CLOSED_CLASS_BLOCKED = "closed_class_blocked"                  # مغلق محجوب
    OPEN_CORE_CONTRACT_CANDIDATE = "open_core_contract_candidate"  # مرشح عقد نواة مفتوحة
    OPEN_CORE_CONTRACT_APPROVED = "open_core_contract_approved"    # عقد نواة مفتوحة موافق
    OPEN_CORE_CONTRACT_DEFERRED = "open_core_contract_deferred"    # عقد نواة مفتوحة مؤجل
    OPEN_CORE_CONTRACT_BLOCKED = "open_core_contract_blocked"      # عقد نواة مفتوحة محجوب
    PROPER_NAME_DEFERRED = "proper_name_deferred"                  # علم مؤجل
    LOANWORD_DEFERRED = "loanword_deferred"                        # دخيل مؤجل
    JAMID_DEFERRED = "jamid_deferred"                              # جامد مؤجل
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"                # دليل غير كافٍ


class PathPermission(Enum):
    """
    Path permission values (NOT certificates).

    These are permissions/hints, not final judgments.
    """
    POSSIBLE = "possible"              # ممكن
    BLOCKED = "blocked"                # محجوب
    DEFERRED = "deferred"              # مؤجل
    UNRESOLVED = "unresolved"          # غير محسوم
    REQUIRES_EVIDENCE = "requires_evidence"  # يحتاج دليلاً


# ============================================================================
# Failure Types
# ============================================================================

class PreWeightContractFailureType(Enum):
    """Failure types for pre-weight contract determination."""
    NO_MABNI_UNITS = "no_mabni_units"
    INVALID_INPUT_LAYER = "invalid_input_layer"
    TRACE_LOSS = "trace_loss"


# ============================================================================
# U₇-B: Inflectional Surface Contract (عقد السطح الصرفي)
# ============================================================================

@dataclass(frozen=True)
class InflectionalSurfaceProfile:
    """
    U₇-B Inflectional Surface Profile - Surface marker classification BEFORE root/weight.

    Critical Law (No Root before Inflectional Filter):
        علامات الإعراب والعدد والجنس والتعريف ليست جذورًا
        Iʿrāb, number, gender, and definiteness markers are NOT root letters.

    Purpose:
        Filter inflectional surface markers BEFORE U₈ root extraction.
        Prevent كتابان → treating ان as root letters.
        Prevent مسلمون → treating ون as root letters.
        Prevent الكتاب → treating ال as root letters.

    Constitutional Principle:
        ALL fields are HINTS (possible/unlikely/unresolved), NOT certificates.
        Surface existence → boolean
        Surface interpretation → hint only

    FORBIDDEN FIELDS:
        - i3rab_certificate (that's U₇+)
        - number_certificate (that's U₇+)
        - gender_certificate (that's U₇+)
        - definiteness_certificate (that's U₇+)
        - root (that's U₈)
        - weight (that's U₉)

    Examples:
        كتابان → dual_surface_hint=possible, stripped_core_candidate=كتاب
        مسلمون → sound_masculine_plural_surface_hint=possible, stripped_core_candidate=مسلم
        مسلمات → sound_feminine_plural_surface_hint=possible, stripped_core_candidate=مسلم
        الكتاب → al_definiteness_surface_hint=possible, stripped_core_candidate=كتاب
        كتابٍ → tanwin_surface_hint=possible (genitive tanwīn)
    """

    # ========== Iʿrāb Surface Markers (Original) ==========
    # علامات الإعراب الأصلية
    nominative_surface_hint: PathPermission      # ضمة/واو رفع محتمل
    accusative_surface_hint: PathPermission      # فتحة/ألف/ياء نصب محتمل
    genitive_surface_hint: PathPermission        # كسرة/ياء جر محتمل
    jussive_surface_hint: PathPermission         # سكون/حذف جزم محتمل

    # ========== Iʿrāb Surface Markers (Secondary) ==========
    # علامات الإعراب الفرعية
    secondary_i3rab_marker_hint: PathPermission  # علامة فرعية محتملة (واو/ألف/ياء)

    # ========== Number Surface Markers ==========
    # علامات العدد
    dual_surface_hint: PathPermission                     # مثنى محتمل (ان/ين)
    sound_masculine_plural_surface_hint: PathPermission   # جمع مذكر سالم محتمل (ون/ين)
    sound_feminine_plural_surface_hint: PathPermission    # جمع مؤنث سالم محتمل (ات)
    broken_plural_surface_hint: PathPermission            # جمع تكسير محتمل
    singular_surface_hint: PathPermission                 # مفرد محتمل

    # ========== Gender Surface Markers ==========
    # علامات الجنس
    masculine_surface_hint: PathPermission        # مذكر محتمل
    feminine_surface_hint: PathPermission         # مؤنث محتمل (ة/ـة/ات)

    # ========== Rationality Surface Markers ==========
    # علامات العقل
    rational_surface_hint: PathPermission         # عاقل محتمل
    non_rational_surface_hint: PathPermission     # غير عاقل محتمل

    # ========== Definiteness Surface Markers ==========
    # علامات التعريف
    al_definiteness_surface_hint: PathPermission  # الـ موجود محتمل
    tanwin_surface_hint: PathPermission           # تنوين موجود محتمل

    # ========== Diptote Surface Marker ==========
    # الممنوع من الصرف
    diptote_surface_hint: PathPermission          # ممنوع من الصرف محتمل

    # ========== Feminine Semantic vs Literal ==========
    # التأنيث اللفظي/المعنوي
    literal_feminine_hint: PathPermission         # تأنيث لفظي (تاء/ة)
    semantic_feminine_hint: PathPermission        # تأنيث معنوي (بلا علامة)

    # ========== Core Extraction ==========
    # استخلاص النواة
    stripped_core_candidate: str                  # النواة المجردة المرشحة (كتاب من كتابان)
    preserved_suffixes: Tuple[str, ...]           # اللواحق المحفوظة (ان، ون، ات، ...)
    blocked_root_segments: Tuple[str, ...]        # المقاطع المحظورة من الجذر

    # ========== Evidence and Trace ==========
    residuals: Tuple[str, ...]                    # تحفظات
    trace_source: str                             # أصل السطح قبل التجريد

    def __post_init__(self):
        """Validate no forbidden fields."""
        forbidden_fields = [
            'i3rab_certificate', 'case_marking',
            'number_certificate', 'quantity',
            'gender_certificate', 'gender',
            'definiteness_certificate', 'is_definite',
            'root', 'root_certificate',
            'weight', 'weight_certificate',
            'pattern', 'pattern_certificate',
            'meaning', 'hukm', 'resolved_reference'
        ]

        for field in forbidden_fields:
            if hasattr(self, field):
                raise ValueError(
                    f"InflectionalSurfaceProfile MUST NOT contain '{field}' field "
                    f"(U₇-B constitutional violation)"
                )


# ============================================================================
# Core Structures
# ============================================================================

@dataclass(frozen=True)
class PreWeightContractUnit:
    """
    U₇ pre-weight contract unit for a mabni closed-class unit.

    This represents PATH PERMISSION, NOT morphological analysis.
    Contract determines if unit MAY proceed to root/weight, NOT what root/weight is.

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
        - resolved_reference (that's U₁₅)
    """
    uid: str
    surface: str  # Orthographic surface from U₆
    source_u6_unit_id: str  # Trace to U₆ mabni closed-class unit
    source_u6_trace: Tuple[str, ...]  # Ordered trace to U₆

    # Contract classification
    open_closed_status: str  # "closed_class" or "open_class"
    contract_status: ContractStatus  # Primary contract status

    # Path permissions (NOT certificates)
    lexical_path_potential: PathPermission  # Overall lexical analysis potential
    root_path_permission: PathPermission  # Permission to enter root extraction
    stem_path_permission: PathPermission  # Permission to enter stem analysis
    weight_path_permission: PathPermission  # Permission to enter weight determination

    # Surface potentials (hints, NOT judgments)
    jamid_surface_potential: PathPermission  # Frozen/non-derivational hint
    proper_name_surface_potential: PathPermission  # Proper name hint
    loanword_surface_potential: PathPermission  # Loanword hint
    frozen_primitive_potential: PathPermission  # Frozen primitive hint

    # Derivational readiness (hint, NOT certificate)
    derivational_readiness: PathPermission  # Ready for derivational analysis?

    # U₇-B: Inflectional Surface Profile (NEW)
    inflectional_surface_profile: Optional[InflectionalSurfaceProfile]  # U₇-B surface marker analysis

    # Evidence and blocking
    required_evidence: Tuple[str, ...]  # What evidence is needed for approval
    blocked_paths: Tuple[str, ...]  # Paths blocked by this contract
    residuals: FrozenSet[Residual]
    rank: Rank
    trace: Tuple[str, ...]  # Full ordered trace from U₀

    def __post_init__(self):
        """Validate pre-weight contract unit - CRITICAL constitutional checks."""
        # FORBIDDEN FIELDS - These MUST NOT exist
        forbidden_fields = [
            'root', 'root_certificate',
            'stem', 'stem_certificate',
            'weight', 'weight_certificate',
            'pattern', 'pattern_certificate',
            'meaning', 'dalalah', 'ifadah',
            'hukm', 'final_irab',
            'resolved_reference'
        ]

        for field in forbidden_fields:
            if hasattr(self, field):
                raise ValueError(
                    f"PreWeightContractUnit MUST NOT contain '{field}' field "
                    f"(Axiom 7.1-7.5 violation)"
                )


@dataclass(frozen=True)
class PreWeightContractLayerObject:
    """
    U₇ layer object containing pre-weight contract classifications.

    Provides path permissions for morphological analysis.
    Blocked units do NOT proceed to root/weight extraction.
    Approved units MAY proceed (subject to further gates).
    """
    uid: str
    units: Tuple[PreWeightContractUnit, ...]  # Contract units
    source_mabni_layer_id: str  # Trace to U₆ layer
    trace_6: Tuple[str, ...]  # Ordered trace to U₆
    residuals: FrozenSet[Residual]
    rank: Rank
    proof: Optional[ProofObject] = None

    def __post_init__(self):
        """Validate pre-weight contract layer object."""
        # FORBIDDEN FIELDS
        forbidden_fields = [
            'root', 'root_certificate',
            'stem', 'stem_certificate',
            'weight', 'weight_certificate',
            'pattern', 'pattern_certificate',
            'meaning', 'dalalah', 'ifadah',
            'hukm', 'final_irab',
            'resolved_reference'
        ]

        for field in forbidden_fields:
            if hasattr(self, field):
                raise ValueError(
                    f"PreWeightContractLayerObject MUST NOT contain '{field}' field"
                )


@dataclass(frozen=True)
class PreWeightContractResult:
    """Result of pre-weight contract determination."""
    success: bool
    layer_object: Optional[PreWeightContractLayerObject]
    failure_type: Optional[PreWeightContractFailureType]
    message: str
    residuals: FrozenSet[Residual]


# ============================================================================
# CPB₇ - Completeness Predicate and Proof Builder
# ============================================================================

@dataclass(frozen=True)
class CPB7:
    """
    CPB₇: Completeness Predicate and Proof Builder for PreWeightContract layer.

    Guards:
        - Contract statuses determined
        - Path permissions assigned
        - Mabni closed-class trace preserved
        - No forbidden fields (root, weight, meaning, hukm, etc.)
        - Allowed next gate: U₈ RootStem (for approved contracts only)
    """

    @staticmethod
    def is_complete(layer_obj: PreWeightContractLayerObject) -> bool:
        """Check if pre-weight contract layer object is complete."""
        if not layer_obj.units:
            return False

        if not layer_obj.source_mabni_layer_id:
            return False

        # Check no forbidden fields
        for unit in layer_obj.units:
            forbidden = ['root', 'stem', 'weight', 'pattern', 'meaning', 'hukm', 'resolved_reference']
            if any(hasattr(unit, field) for field in forbidden):
                return False

        return True

    @staticmethod
    def build_proof(layer_obj: PreWeightContractLayerObject) -> ProofObject:
        """Build proof object for pre-weight contract layer."""
        # Count contract statuses
        blocked_count = sum(
            1 for u in layer_obj.units
            if u.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED
        )
        approved_count = sum(
            1 for u in layer_obj.units
            if u.contract_status == ContractStatus.OPEN_CORE_CONTRACT_APPROVED
        )
        candidate_count = sum(
            1 for u in layer_obj.units
            if u.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE
        )
        deferred_count = sum(
            1 for u in layer_obj.units
            if u.contract_status in [
                ContractStatus.OPEN_CORE_CONTRACT_DEFERRED,
                ContractStatus.PROPER_NAME_DEFERRED,
                ContractStatus.LOANWORD_DEFERRED,
                ContractStatus.JAMID_DEFERRED
            ]
        )

        return make_proof_object(
            claim="U₇ pre-weight contract paths determined",
            scope="U7_PRE_WEIGHT_CONTRACT",
            evidence=frozenset([
                f"units_count={len(layer_obj.units)}",
                f"blocked_count={blocked_count}",
                f"approved_count={approved_count}",
                f"candidate_count={candidate_count}",
                f"deferred_count={deferred_count}",
                f"trace_preserved={bool(layer_obj.source_mabni_layer_id)}",
                f"rank={layer_obj.rank.value}",
            ]),
            counter_evidence=frozenset(),
            trace_graph={},
            competitors=frozenset(),
            residuals=layer_obj.residuals,
            rank_vector={},
            allowed_next_gates=frozenset({"root_stem_gate"}),
            forbidden_next_gates=frozenset({
                "root_certificate",
                "stem_certificate",
                "weight_certificate",
                "pattern_certificate",
                "meaning_certificate",
                "hukm_certificate",
            }),
            limitations=frozenset([
                "no_root_extraction",
                "no_stem_extraction",
                "no_weight_determination",
                "no_pattern_determination",
                "no_meaning_assignment",
                "no_hukm_judgment",
                "contract_is_permission_not_certificate",
                "blocked_units_must_not_proceed_to_root",
                "approved_units_may_proceed_to_root_with_evidence",
            ]),
        )


# ============================================================================
# Pre-Weight Contract Logic
# ============================================================================

def _classify_contract_status(
    mabni_unit: MabniClosedClassUnit
) -> ContractStatus:
    """
    Classify contract status based on U₆ mabni classification.

    Decision tree:
    1. If closed-class mabni → CLOSED_CLASS_BLOCKED
    2. If open-class core → OPEN_CORE_CONTRACT_CANDIDATE
    3. Otherwise → INSUFFICIENT_EVIDENCE

    Args:
        mabni_unit: U₆ mabni closed-class unit

    Returns:
        ContractStatus
    """
    mabni_type = mabni_unit.mabni_classification.mabni_type

    if mabni_type in [
        MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
        MabniClosedClassType.ATTACHED_PRONOUN_CLOSED_CLASS,
        MabniClosedClassType.DETACHED_PRONOUN_CLOSED_CLASS
    ]:
        return ContractStatus.CLOSED_CLASS_BLOCKED

    elif mabni_type == MabniClosedClassType.OPEN_CLASS_CORE_CANDIDATE:
        return ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE

    else:
        return ContractStatus.INSUFFICIENT_EVIDENCE


def _determine_path_permissions(
    contract_status: ContractStatus,
    surface: str
) -> Tuple[PathPermission, PathPermission, PathPermission, PathPermission]:
    """
    Determine path permissions based on contract status.

    Returns:
        (lexical_path, root_path, stem_path, weight_path)
    """
    if contract_status == ContractStatus.CLOSED_CLASS_BLOCKED:
        # Closed-class: ALL morphological paths blocked
        return (
            PathPermission.BLOCKED,  # lexical_path
            PathPermission.BLOCKED,  # root_path
            PathPermission.BLOCKED,  # stem_path
            PathPermission.BLOCKED   # weight_path
        )

    elif contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE:
        # Open-class candidate: paths POSSIBLE but not yet approved
        return (
            PathPermission.POSSIBLE,     # lexical_path
            PathPermission.POSSIBLE,     # root_path
            PathPermission.POSSIBLE,     # stem_path
            PathPermission.POSSIBLE      # weight_path
        )

    elif contract_status == ContractStatus.OPEN_CORE_CONTRACT_APPROVED:
        # Approved: paths POSSIBLE (actual extraction in U₈/U₉)
        return (
            PathPermission.POSSIBLE,     # lexical_path
            PathPermission.POSSIBLE,     # root_path
            PathPermission.POSSIBLE,     # stem_path
            PathPermission.POSSIBLE      # weight_path
        )

    elif contract_status in [
        ContractStatus.PROPER_NAME_DEFERRED,
        ContractStatus.LOANWORD_DEFERRED,
        ContractStatus.JAMID_DEFERRED
    ]:
        # Deferred: paths need evidence
        return (
            PathPermission.DEFERRED,     # lexical_path
            PathPermission.DEFERRED,     # root_path
            PathPermission.DEFERRED,     # stem_path
            PathPermission.DEFERRED      # weight_path
        )

    else:
        # Insufficient evidence: unresolved
        return (
            PathPermission.UNRESOLVED,   # lexical_path
            PathPermission.UNRESOLVED,   # root_path
            PathPermission.UNRESOLVED,   # stem_path
            PathPermission.UNRESOLVED    # weight_path
        )


# ============================================================================
# U₇-B: Inflectional Surface Detection Functions
# ============================================================================

def _analyze_inflectional_surface(surface: str, open_closed_status: str) -> Optional[InflectionalSurfaceProfile]:
    """
    U₇-B: Analyze inflectional surface markers before root/weight extraction.

    Critical Purpose:
        Prevent ان/ون/ات/ال from being treated as root letters in U₈.

    Args:
        surface: Orthographic surface from U₆
        open_closed_status: "closed_class" or "open_class"

    Returns:
        InflectionalSurfaceProfile if open-class, None if closed-class

    Examples:
        كتابان → dual_surface_hint=possible, stripped_core=كتاب, suffixes=(ان,)
        مسلمون → sound_masc_plural=possible, stripped_core=مسلم, suffixes=(ون,)
        الكتاب → al_definiteness=possible, stripped_core=كتاب, suffixes=()
        كتابٍ → tanwin=possible, genitive=possible, stripped_core=كتاب
    """
    # Closed-class units don't need inflectional analysis (already blocked)
    if open_closed_status == "closed_class":
        return None

    # Initialize all hints as UNRESOLVED
    residuals_list = []

    # ========== Detect Number Surface Markers ==========
    dual_hint, sound_masc_plural_hint, sound_fem_plural_hint, stripped_core, suffixes, blocked_segments = \
        _detect_number_surface_markers(surface)

    # ========== Detect Definiteness Surface Markers ==========
    al_hint, tanwin_hint, core_after_al = _detect_definiteness_surface_markers(stripped_core)
    if al_hint == PathPermission.POSSIBLE:
        # Al-definiteness detected, update stripped_core
        stripped_core = core_after_al

    # ========== Detect Iʿrāb Surface Markers ==========
    nom_hint, acc_hint, gen_hint, juss_hint, secondary_hint = _detect_irab_surface_markers(surface)

    # ========== Detect Gender Surface Markers ==========
    masc_hint, fem_hint, literal_fem_hint, semantic_fem_hint = _detect_gender_surface_markers(surface, suffixes)

    # ========== Detect Other Markers ==========
    broken_plural_hint = PathPermission.UNRESOLVED  # Needs lexicon
    singular_hint = PathPermission.UNRESOLVED if (dual_hint == PathPermission.POSSIBLE or
                                                    sound_masc_plural_hint == PathPermission.POSSIBLE or
                                                    sound_fem_plural_hint == PathPermission.POSSIBLE) else PathPermission.POSSIBLE
    rational_hint = PathPermission.UNRESOLVED
    non_rational_hint = PathPermission.UNRESOLVED
    diptote_hint = PathPermission.UNRESOLVED

    return InflectionalSurfaceProfile(
        # Iʿrāb markers
        nominative_surface_hint=nom_hint,
        accusative_surface_hint=acc_hint,
        genitive_surface_hint=gen_hint,
        jussive_surface_hint=juss_hint,
        secondary_i3rab_marker_hint=secondary_hint,

        # Number markers
        dual_surface_hint=dual_hint,
        sound_masculine_plural_surface_hint=sound_masc_plural_hint,
        sound_feminine_plural_surface_hint=sound_fem_plural_hint,
        broken_plural_surface_hint=broken_plural_hint,
        singular_surface_hint=singular_hint,

        # Gender markers
        masculine_surface_hint=masc_hint,
        feminine_surface_hint=fem_hint,

        # Rationality
        rational_surface_hint=rational_hint,
        non_rational_surface_hint=non_rational_hint,

        # Definiteness
        al_definiteness_surface_hint=al_hint,
        tanwin_surface_hint=tanwin_hint,

        # Diptote
        diptote_surface_hint=diptote_hint,

        # Feminine types
        literal_feminine_hint=literal_fem_hint,
        semantic_feminine_hint=semantic_fem_hint,

        # Core extraction
        stripped_core_candidate=stripped_core,
        preserved_suffixes=suffixes,
        blocked_root_segments=blocked_segments,

        # Evidence
        residuals=tuple(residuals_list),
        trace_source=surface
    )


def _detect_number_surface_markers(surface: str) -> tuple[PathPermission, PathPermission, PathPermission, str, Tuple[str, ...], Tuple[str, ...]]:
    """
    Detect dual and sound plural surface markers.

    Returns:
        (dual_hint, sound_masc_plural_hint, sound_fem_plural_hint, stripped_core, suffixes, blocked_segments)

    Examples:
        كتابان → (possible, unresolved, unresolved, كتاب, (ان,), (ان,))
        مسلمون → (unresolved, possible, unresolved, مسلم, (ون,), (ون,))
        مسلمات → (unresolved, unresolved, possible, مسلم, (ات,), (ات,))
    """
    dual_hint = PathPermission.UNRESOLVED
    sound_masc_plural_hint = PathPermission.UNRESOLVED
    sound_fem_plural_hint = PathPermission.UNRESOLVED
    stripped_core = surface
    suffixes = ()
    blocked_segments = ()

    # Check for dual markers (ان/ين) - must be at least 3 letters before marker
    if len(surface) >= 4:
        if surface.endswith("انِ") or surface.endswith("انَ") or surface.endswith("ان"):
            dual_hint = PathPermission.POSSIBLE
            stripped_core = surface[:-2]  # Remove ان
            suffixes = ("ان",)
            blocked_segments = ("ان",)
        elif surface.endswith("ينِ") or surface.endswith("ينَ") or surface.endswith("ين"):
            dual_hint = PathPermission.POSSIBLE
            stripped_core = surface[:-2]  # Remove ين
            suffixes = ("ين",)
            blocked_segments = ("ين",)

        # Check for sound masculine plural (ون/ين)
        elif surface.endswith("ونَ") or surface.endswith("ون"):
            sound_masc_plural_hint = PathPermission.POSSIBLE
            stripped_core = surface[:-2]  # Remove ون
            suffixes = ("ون",)
            blocked_segments = ("ون",)

        # Check for sound feminine plural (ات)
        elif surface.endswith("اتٌ") or surface.endswith("اتٍ") or surface.endswith("اتُ") or surface.endswith("اتِ") or surface.endswith("اتَ") or surface.endswith("ات"):
            sound_fem_plural_hint = PathPermission.POSSIBLE
            stripped_core = surface[:-2]  # Remove ات
            suffixes = ("ات",)
            blocked_segments = ("ات",)

    return (dual_hint, sound_masc_plural_hint, sound_fem_plural_hint, stripped_core, suffixes, blocked_segments)


def _detect_definiteness_surface_markers(surface: str) -> tuple[PathPermission, PathPermission, str]:
    """
    Detect definiteness surface markers (ال and tanwīn).

    Returns:
        (al_hint, tanwin_hint, core_after_al)

    Examples:
        الكتاب → (possible, unresolved, كتاب)
        كتابٌ → (unresolved, possible, كتابٌ)
        كتاب → (unresolved, unresolved, كتاب)
    """
    al_hint = PathPermission.UNRESOLVED
    tanwin_hint = PathPermission.UNRESOLVED
    core_after_al = surface

    # Check for ال prefix
    if len(surface) >= 3:
        if surface.startswith("ال"):
            al_hint = PathPermission.POSSIBLE
            core_after_al = surface[2:]  # Remove ال

    # Check for tanwīn (ٌ, ٍ, ً)
    if "ٌ" in surface or "ٍ" in surface or "ً" in surface:
        tanwin_hint = PathPermission.POSSIBLE

    return (al_hint, tanwin_hint, core_after_al)


def _detect_irab_surface_markers(surface: str) -> tuple[PathPermission, PathPermission, PathPermission, PathPermission, PathPermission]:
    """
    Detect iʿrāb surface markers (hints only, NOT certificates).

    Returns:
        (nominative_hint, accusative_hint, genitive_hint, jussive_hint, secondary_marker_hint)

    Examples:
        كتابٌ → (possible, unresolved, unresolved, unresolved, unresolved)
        كتابًا → (unresolved, possible, unresolved, unresolved, unresolved)
        كتابٍ → (unresolved, unresolved, possible, unresolved, unresolved)
    """
    nom_hint = PathPermission.UNRESOLVED
    acc_hint = PathPermission.UNRESOLVED
    gen_hint = PathPermission.UNRESOLVED
    juss_hint = PathPermission.UNRESOLVED
    secondary_hint = PathPermission.UNRESOLVED

    # Check for damma/tanwīn damma (nominative)
    if "ُ" in surface or "ٌ" in surface or surface.endswith("ون"):
        nom_hint = PathPermission.POSSIBLE

    # Check for fatha/tanwīn fatha (accusative)
    if "َ" in surface or "ً" in surface or "ا" in surface[-2:]:
        acc_hint = PathPermission.POSSIBLE

    # Check for kasra/tanwīn kasra (genitive)
    if "ِ" in surface or "ٍ" in surface or surface.endswith("ين"):
        gen_hint = PathPermission.POSSIBLE

    # Check for sukūn (jussive)
    if "ْ" in surface:
        juss_hint = PathPermission.POSSIBLE

    # Check for secondary markers (واو/ألف/ياء in terminal position)
    if len(surface) >= 2:
        if surface[-1] in ["و", "ا", "ي"] or surface[-2:] in ["ون", "ين", "ان"]:
            secondary_hint = PathPermission.POSSIBLE

    return (nom_hint, acc_hint, gen_hint, juss_hint, secondary_hint)


def _detect_gender_surface_markers(surface: str, suffixes: Tuple[str, ...]) -> tuple[PathPermission, PathPermission, PathPermission, PathPermission]:
    """
    Detect gender surface markers (hints only).

    Returns:
        (masculine_hint, feminine_hint, literal_feminine_hint, semantic_feminine_hint)

    Examples:
        كاتبة → (unresolved, possible, possible, unresolved)
        كاتبات → (unresolved, possible, possible, unresolved)
        كاتب → (possible, unresolved, unresolved, possible)
    """
    masc_hint = PathPermission.UNRESOLVED
    fem_hint = PathPermission.UNRESOLVED
    literal_fem_hint = PathPermission.UNRESOLVED
    semantic_fem_hint = PathPermission.UNRESOLVED

    # Check for tāʾ marbūṭa (ة)
    if "ة" in surface or "ـة" in surface:
        fem_hint = PathPermission.POSSIBLE
        literal_fem_hint = PathPermission.POSSIBLE

    # Check for ات suffix (sound feminine plural)
    if "ات" in suffixes or surface.endswith("ات"):
        fem_hint = PathPermission.POSSIBLE
        literal_fem_hint = PathPermission.POSSIBLE

    # If no literal feminine marker, could be masculine or semantic feminine
    if literal_fem_hint == PathPermission.UNRESOLVED:
        masc_hint = PathPermission.POSSIBLE
        semantic_fem_hint = PathPermission.POSSIBLE

    return (masc_hint, fem_hint, literal_fem_hint, semantic_fem_hint)


def _check_jamid_potential(surface: str) -> PathPermission:
    """
    Check if surface suggests frozen/non-derivational (جامد) potential.

    This is a HINT, not a certificate.
    """
    # Placeholder: actual implementation would check lexicon
    return PathPermission.UNRESOLVED


def _check_proper_name_potential(surface: str) -> PathPermission:
    """
    Check if surface suggests proper name (علم) potential.

    This is a HINT, not a certificate.
    """
    # Placeholder: actual implementation would check patterns
    # Example: زيد, إبراهيم, محمد
    return PathPermission.UNRESOLVED


def _check_loanword_potential(surface: str) -> PathPermission:
    """
    Check if surface suggests loanword (دخيل) potential.

    This is a HINT, not a certificate.
    """
    # Placeholder: actual implementation would check patterns
    # Example: إبراهيم (Hebrew loanword)
    return PathPermission.UNRESOLVED


# ============================================================================
# Pre-Weight Contract Operations
# ============================================================================

def pre_weight_contract_7(
    mabni_layer: MabniClosedClassLayerObject
) -> PreWeightContractResult:
    """
    Determine pre-weight contract permissions from U₆ mabni closed-class layer.

    Critical Examples:
        وَ → closed_class_blocked (root blocked, weight blocked)
        بِ → closed_class_blocked (root blocked, weight blocked)
        ـهِمْ → closed_class_blocked (pronoun path preserved)
        كِتَابِ → open_core_contract_candidate (root possible, weight possible, NO extraction)
        كَتَبَ → open_core_contract_candidate (verb surface, NO root emitted)
        كَاتِب → open_core_contract_candidate (noun surface, NO weight emitted)

    Args:
        mabni_layer: U₆ layer object with mabni closed-class classifications

    Returns:
        PreWeightContractResult with path permissions

    Forbidden:
        - Root extraction (U₈)
        - Stem extraction (U₈)
        - Weight determination (U₉)
        - Pattern certification (U₉+)
        - Meaning assignment (U₁₅)
        - Hukm judgment (U₇+)
    """
    # Validate input
    if not mabni_layer.units:
        return PreWeightContractResult(
            success=False,
            layer_object=None,
            failure_type=PreWeightContractFailureType.NO_MABNI_UNITS,
            message="No mabni units in input",
            residuals=frozenset([make_blocker("no_units", "Cannot determine contract without mabni units")])
        )

    # Process each mabni unit
    contract_units = []
    all_residuals = []

    for mabni_unit in mabni_layer.units:
        # Classify contract status
        contract_status = _classify_contract_status(mabni_unit)

        # Determine path permissions
        (lexical_path, root_path, stem_path, weight_path) = _determine_path_permissions(
            contract_status,
            mabni_unit.surface
        )

        # Check surface potentials (hints only)
        jamid_potential = _check_jamid_potential(mabni_unit.surface)
        proper_name_potential = _check_proper_name_potential(mabni_unit.surface)
        loanword_potential = _check_loanword_potential(mabni_unit.surface)
        frozen_primitive_potential = PathPermission.UNRESOLVED

        # Derivational readiness (hint only)
        derivational_readiness = PathPermission.UNRESOLVED

        # Determine open/closed status FIRST (needed for U₇-B)
        if contract_status == ContractStatus.CLOSED_CLASS_BLOCKED:
            open_closed_status = "closed_class"
        else:
            open_closed_status = "open_class"

        # U₇-B: Inflectional Surface Analysis (NEW - before root/weight)
        inflectional_surface_profile = _analyze_inflectional_surface(
            mabni_unit.surface,
            open_closed_status
        )

        # Determine blocked paths
        blocked_paths = []
        required_evidence = []

        if contract_status == ContractStatus.CLOSED_CLASS_BLOCKED:
            blocked_paths = ["root_extraction", "weight_determination", "stem_extraction"]
            required_evidence = ["closed_class_mabni_blocks_morphology"]
        elif contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE:
            required_evidence = ["lexical_attestation", "surface_family_evidence"]

        # Build trace
        trace = mabni_unit.trace_5

        # Build PreWeightContractUnit
        contract_unit = PreWeightContractUnit(
            uid=str(uuid4()),
            surface=mabni_unit.surface,
            source_u6_unit_id=mabni_unit.uid,
            source_u6_trace=mabni_unit.trace_5,
            open_closed_status=open_closed_status,
            contract_status=contract_status,
            lexical_path_potential=lexical_path,
            root_path_permission=root_path,
            stem_path_permission=stem_path,
            weight_path_permission=weight_path,
            jamid_surface_potential=jamid_potential,
            proper_name_surface_potential=proper_name_potential,
            loanword_surface_potential=loanword_potential,
            frozen_primitive_potential=frozen_primitive_potential,
            derivational_readiness=derivational_readiness,
            inflectional_surface_profile=inflectional_surface_profile,  # U₇-B
            required_evidence=tuple(required_evidence),
            blocked_paths=tuple(blocked_paths),
            residuals=mabni_unit.residuals,  # Preserve residuals from U₆
            rank=mabni_unit.rank,
            trace=trace
        )

        contract_units.append(contract_unit)
        all_residuals.extend(list(mabni_unit.residuals))

    # Build layer object
    layer_obj = PreWeightContractLayerObject(
        uid=str(uuid4()),
        units=tuple(contract_units),
        source_mabni_layer_id=mabni_layer.uid,
        trace_6=(mabni_layer.uid,),
        residuals=frozenset(all_residuals),
        rank=mabni_layer.rank,  # Inherit rank from U₆
        proof=None
    )

    # Build proof
    proof = CPB7.build_proof(layer_obj)
    layer_obj = PreWeightContractLayerObject(
        uid=layer_obj.uid,
        units=layer_obj.units,
        source_mabni_layer_id=layer_obj.source_mabni_layer_id,
        trace_6=layer_obj.trace_6,
        residuals=layer_obj.residuals,
        rank=layer_obj.rank,
        proof=proof
    )

    return PreWeightContractResult(
        success=True,
        layer_object=layer_obj,
        failure_type=None,
        message=f"Pre-weight contract permissions determined: {len(contract_units)} units processed",
        residuals=layer_obj.residuals
    )


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Core types
    'ContractStatus',
    'PathPermission',

    # U₇-B: Inflectional Surface Contract
    'InflectionalSurfaceProfile',

    # Structures
    'PreWeightContractUnit',
    'PreWeightContractLayerObject',
    'PreWeightContractResult',

    # Failures
    'PreWeightContractFailureType',

    # CPB
    'CPB7',

    # Operations
    'pre_weight_contract_7',
]
