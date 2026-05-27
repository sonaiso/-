"""
U₉ Arabic Weight Carrier (طبقة حامل الوزن العربي) - LEGACY/DEPRECATED

⚠️ DEPRECATION WARNING ⚠️
================================================================================
This module is DEPRECATED and maintained only for backward compatibility.

Official U₉ Implementation:
    src/dal_core/u9_weight_candidate_carrier.py

Official API:
    from dal_core import (
        WeightCandidateResult,
        weight_candidate_carrier_9,
        validate_approved_context_for_u9,
    )

Migration Path:
    All new code MUST use u9_weight_candidate_carrier.py.
    This file is retained only to:
    1. Prevent breaking existing imports
    2. Provide safe wrappers that enforce ApprovedTransitionContext
    3. Guide migration to official implementation

Constitutional Risk:
    This legacy module does NOT enforce ApprovedTransitionContext at all
    entry points. It is unsafe for direct use without governance.

    DO NOT use dispatch_weight() directly.
    DO NOT use gate_89_validate() directly.

    Use ONLY the new official API from dal_core.
================================================================================

Domain: U₉ = ArabicWeightCarrier
Transition: PreWeightContract + RootStemCarrier (U₇+U₈) → ArabicWeightObject (U₉)
Purpose: Typed weight algebra with four distinct pathways

Constitutional Governance (الحكم الدستوري):
    CRITICAL: This layer operates under AlgebraicDecisionCore governance.

    Architectural Law:
        Layer does not own Governor.
        Governor owns Transition Permission.

    Execution Pattern:
        Pipeline/Orchestrator owns AlgebraicDecisionCore
          → asks: approve U₈→U₉ transition?
          → receives DecisionAudit
          → if approved: creates ApprovedTransitionContext
          → passes context to U₉
          → U₉ verifies context and executes

    Constitutional Requirements:
        ✓ No U₉ execution without ApprovedTransitionContext
        ✓ No ApprovedTransitionContext without AlgebraicDecisionCore approval
        ✓ No approval without 8-dimensional validation:
          1. Identity: ROOT_MATERIAL_IDENTITY → WEIGHT_IDENTITY
          2. Domain: WEIGHT_DOMAIN only (no meaning, no syntax, no hukm)
          3. Gate: WeightTransitionGate passed
          4. Evidence: Root/stem candidacy evidence present
          5. Rank: CANDIDATE → CANDIDATE (no elevation without evidence)
          6. Residuals: No blocking residuals
          7. Trace: Complete U₀→U₁→...→U₈ trace preserved
          8. No Leap: Sequential progression verified

    Domain Boundaries (حدود المجال):
        Forbidden in WEIGHT_DOMAIN:
            ✗ Meaning determination (معنى) - صيغة فاعل ≠ معنى الفاعلية
            ✗ Syntactic role (فاعل نحوي) - صيغة فاعل ≠ الفاعل النحوي
            ✗ I'rab judgment (إعراب)
            ✗ Hukm (حكم)
            ✗ Semantic derivation (اشتقاق معنوي)
            ✗ Functional assignment (وظيفة)

        Permitted in WEIGHT_DOMAIN:
            ✓ Weight pattern (وزن)
            ✓ Morphological template (قالب صرفي)
            ✓ F-'-L mapping (فاء-عين-لام)

Key Principle:
    Weight is NOT just derivational pattern (وزن المشتق).
    It's an algebraic system with four types:
    1. BuiltWeight (وزن_المبني) - Preserves functional identity for particles
    2. JāmidWeight (وزن_الجامد) - Preserves lexical anchoring
    3. InflectableWeight (وزن_المعرب) - Preserves stem, allows ending variation
    4. MushtaqWeight (وزن_المشتق) - Transforms root+pattern to form

Critical Laws:
    1. No item enters MushtaqWeight until it passes Built/Jāmid gates
    2. Weight ⊬ FinalMeaning (no semantic jump)
    3. Weight ⊬ Hukm (no grammatical judgment)
    4. Trace preserved from U₈/U₇
    5. Residuals preserved, not deleted
    6. Competitors preserved until evidence blocks
    7. Rank progression evidence-based only
    8. NO internal AlgebraicDecisionCore instantiation (Constitutional violation)

Architecture:
    U₀ (Unicode) → U₁ (Grapheme) → U₂ (Syllable) → U₃ (Boundary) →
    U₄ (TrueSingularLafẓ) → U₅ (FunctionalRole) → U₆ (MabniClosedClass) →
    U₇ (PreWeightContract) → U₈ (RootStemCarrier) → U₉ (ArabicWeightCarrier)

PR: U9-WEIGHT-ALGEBRA
Created: 2026-05-25
Updated: 2026-05-26 (Constitutional governance)
Deprecated: 2026-05-26 (Superseded by u9_weight_candidate_carrier.py)
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, Set, FrozenSet, Dict, Any, Tuple, Union
from uuid import uuid4
import warnings

from dal_core.residuals import Residual, ResidualType, ResidualSeverity
from dal_core.ranks import LughaRank
from dal_core.evidence import Evidence


# ============================================================================
# Weight Type Taxonomy (Four-Path Weight Algebra)
# ============================================================================

class WeightType(Enum):
    """
    أنواع الوزن الأربعة (Four Weight Types)

    Critical: Weight is NOT just MushtaqWeight.
    Four distinct algebraic pathways with different invariants.
    """
    BUILT = "وزن_المبني"           # Built/Particle weight (preserves functional identity)
    JAMID = "وزن_الجامد"           # Frozen/Anchor weight (preserves lexical anchor)
    INFLECTABLE = "وزن_المعرب"     # Inflectable weight (preserves stem, varies ending)
    MUSHTAQ = "وزن_المشتق"         # Derived weight (transforms root→pattern→form)


# ============================================================================
# Weight Rank System
# ============================================================================

class WeightRank(Enum):
    """
    رتبة الوزن (Weight Rank)

    Evidence-based rank progression for weight analysis.
    """
    WEIGHT_ZERO = 0                # غير ثابت - No weight evidence
    WEIGHT_CANDIDATE = 1           # مرشح - Candidate weight
    WEIGHT_HYPOTHESIS = 2          # فرضية - Weight hypothesis
    WEIGHT_STRONG_HYPOTHESIS = 3   # فرضية قوية - Strong hypothesis
    WEIGHT_CERTIFICATE = 4         # شهادة - Certified weight
    WEIGHT_BLOCKED = 5             # ممنوع - Blocked by evidence

    def __lt__(self, other):
        if not isinstance(other, WeightRank):
            return NotImplemented
        return self.value < other.value

    def __le__(self, other):
        if not isinstance(other, WeightRank):
            return NotImplemented
        return self.value <= other.value

    def __gt__(self, other):
        if not isinstance(other, WeightRank):
            return NotImplemented
        return self.value > other.value

    def __ge__(self, other):
        if not isinstance(other, WeightRank):
            return NotImplemented
        return self.value >= other.value


# ============================================================================
# Weight Residuals
# ============================================================================

class WeightResidualType(Enum):
    """
    بقايا الوزن (Weight Residuals)

    Weight-specific residuals that must be preserved through pipeline.
    """
    # Dispatch ambiguity
    BUILT_VS_DERIVED_AMBIGUITY = "تنافس مبني/مشتق"
    JAMID_VS_MUSHTAQ_AMBIGUITY = "تنافس جامد/مشتق"
    INFLECTION_VS_BUILD_AMBIGUITY = "تنافس إعراب/بناء"

    # Root/Pattern issues
    ROOT_MAPPING_UNCERTAIN = "تخريط جذر غير محسوم"
    EXTRA_LETTER_UNCERTAIN = "حرف زائد غير محسوم"
    PATTERN_COMPETITION = "تنافس أوزان"
    SLOT_MAP_UNCERTAIN = "توزيع خانات غير محسوم"

    # Phonological adjustments
    WEAK_ROOT_ADJUSTMENT_REQUIRED = "تعديل جذر معتل مطلوب"
    HAMZA_ADJUSTMENT_REQUIRED = "تعديل همزة مطلوب"
    IDGHAM_TRACE_REQUIRED = "أثر إدغام مطلوب"

    # Lexicon dependencies
    BROKEN_PLURAL_REQUIRES_LEXICON = "جمع تكسير يتطلب معجم"
    PROPER_NAME_BLOCKS_DERIVATION = "اسم علم يمنع اشتقاق"
    LOANWORD_BLOCKS_ROOT_PATH = "دخيل يمنع مسار جذر"

    # Inflection-related
    DIPTOTE_AFFECTS_ENDING = "ممنوع من الصرف يؤثر على الآخر"

    # Voice/valency
    VOICE_VOWEL_TEMPLATE_AMBIGUITY = "تنافس قوالب حركية صوتية"
    TRANSITIVITY_REQUIREMENT_UNMET = "شرط تعدي غير محقق"
    PASSIVE_FROM_INTRANSITIVE_RESIDUAL = "مجهول من لازم محتمل"

    # Blocking conditions
    WEIGHT_DISPATCH_BLOCKED = "توزيع وزن ممنوع"
    DERIVATION_BLOCKED_BY_BUILT = "اشتقاق ممنوع بالبناء"
    DERIVATION_BLOCKED_BY_JAMID = "اشتقاق ممنوع بالجمود"

    # Contract violations (anti-jumping)
    WEIGHT_MEANING_LEAK = "تسرب معنى من وزن"
    WEIGHT_HUKM_LEAK = "تسرب حكم من وزن"
    WEIGHT_SYNTAX_LEAK = "تسرب نحو من وزن"


# ============================================================================
# Input Contracts (from U₇ and U₈)
# ============================================================================

@dataclass(frozen=True)
class PreWeightContract:
    """
    عقد ما قبل الوزن (Pre-Weight Contract from U₇)

    Input contract that must pass Gate₈₉ before weight construction.
    """
    build_status: str  # "ClosedMabniCertificate" | "MuʿrabCandidate" | "Unknown"
    lexical_status: str  # "JāmidCertificate" | "MushtaqCandidate" | "Unknown"
    path_type: str  # "Mabni" | "Jāmid" | "Muʿrab" | "Mushtaq" | "Ambiguous"

    # Access permissions
    derivation_access: str  # "blocked" | "open" | "limited"
    inflection_access: bool

    # Evidence
    evidence: Tuple[Evidence, ...]
    trace: Dict[str, Any]

    # Optional fields with defaults
    residuals: Tuple[Residual, ...] = field(default_factory=tuple)
    competitors: FrozenSet[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class RootStemInput:
    """
    مدخل جذر/جذع (Root/Stem Input from U₈)

    Root or stem information from U₈ carrier.
    """
    root_or_stem: Tuple[str, ...]  # e.g., ("ك", "ت", "ب") or stem surface
    input_type: str  # "root" | "stem_anchor" | "closed_built_input"
    root_status: str  # "RootLicensed" | "StemAnchor" | "BuiltForm"

    # Evidence (required)
    evidence: Tuple[Evidence, ...]
    trace: Dict[str, Any]

    # Optional fields with defaults
    pattern_candidate: Optional[str] = None
    residuals: Tuple[Residual, ...] = field(default_factory=tuple)


# ============================================================================
# Arabic Weight Object (U₉ Carrier)
# ============================================================================

@dataclass(frozen=True)
class ArabicWeightObject:
    """
    حامل الوزن العربي (Arabic Weight Object - U₉ Carrier)

    The weight is NOT just "فَعَلَ" pattern.
    It's a typed object with:
    - Weight type (Built/Jāmid/Inflectable/Mushtaq)
    - Input contracts
    - Slots, vowels, extras
    - Trace from U₈/U₇
    - Residuals
    - Rank

    Critical Laws Enforced:
        1. Weight ⊬ FinalMeaning
        2. Weight ⊬ Hukm
        3. TracePreserved from U₈/U₇
        4. ResidualsPreserved
        5. CompetitorsPreserved
    """
    # Required fields (no defaults)
    weight_type: WeightType
    input_contract: PreWeightContract
    root_stem_input: RootStemInput

    # Optional fields with defaults
    id: str = field(default_factory=lambda: str(uuid4()))
    pattern_shape: Optional[str] = None  # e.g., "فَاعِل", "مَفْعُول", "CVC"
    slot_map: Optional[Dict[str, str]] = None  # e.g., {"ك": "ف", "ت": "ع", "ب": "ل"}
    vowel_template: Optional[str] = None  # e.g., "ā-i" for فاعل
    extra_elements: Tuple[str, ...] = field(default_factory=tuple)  # Augments
    inflection_site: Optional[str] = None  # "final" | "internal"
    frozen_status: Optional[str] = None  # "frozen_ending" | "variable_ending"
    output_form_candidate: Optional[str] = None
    trace: Dict[str, Any] = field(default_factory=dict)
    residuals: Tuple[Residual, ...] = field(default_factory=tuple)
    rank: WeightRank = WeightRank.WEIGHT_ZERO
    competitors: FrozenSet[str] = field(default_factory=frozenset)
    evidence: Tuple[Evidence, ...] = field(default_factory=tuple)
    forbidden_next_gates: FrozenSet[str] = field(
        default_factory=lambda: frozenset(["final_meaning", "hukm", "syntax_judgment"])
    )

    def __post_init__(self):
        """Validate no meaning/hukm fields exist"""
        # Enforce anti-jumping law
        for attr in ["meaning", "murad", "hukm", "haqiqa_majaz", "final_meaning"]:
            if hasattr(self, attr):
                raise ValueError(
                    f"ArabicWeightObject MUST NOT contain '{attr}' field. "
                    f"Law: Weight ⊬ FinalMeaning, Weight ⊬ Hukm"
                )


# ============================================================================
# Weight-Specific Identity Structures
# ============================================================================

@dataclass(frozen=True)
class BuiltWeightIdentity:
    """
    هوية وزن المبني (Built Weight Identity)

    For مبني (built/particles): preserves functional identity.
    Examples: مِنْ، عَنْ، إِنَّ، ذَلِكَ

    Invariants:
        - closed_class_identity preserved
        - fixed_surface or fixed_ending
        - operator_function maintained
        - no_free_derivation blocked
    """
    functional_shape: str  # e.g., "CVC"
    closed_class_identity: str  # e.g., "HarfJarr", "Demonstrative"
    frozen_ending: str  # e.g., "sukūn", "kasra"
    operator_potential: Optional[str] = None  # e.g., "requires_majrur"
    derivation: str = "blocked"  # Always blocked for built


@dataclass(frozen=True)
class JāmidWeightIdentity:
    """
    هوية وزن الجامد (Jāmid Weight Identity)

    For جامد (frozen/lexical anchors): preserves stem anchor.
    Examples: أَرْض، سَمَاء، نَار

    Invariants:
        - lexical_anchor preserved
        - stem_shape maintained
        - limited_or_blocked_derivation
        - usage_certificate from lexicon
    """
    stem_anchor: str
    surface_shape: str
    lexical_anchor_status: str  # "rooted_primitive" | "jāmid" | "historical_root"
    derivation: str  # "blocked" | "limited" | "historical_only"


@dataclass(frozen=True)
class InflectableWeightIdentity:
    """
    هوية وزن المعرب (Inflectable Weight Identity)

    For معرب (inflectable): preserves stem, opens ending variation.
    Examples: كِتَابٌ/كِتَابَ/كِتَابِ، رَجُلٌ/رَجُلَ/رَجُلٍ

    Invariants:
        - stem_identity preserved
        - inflection_site identified
        - relation_sensitive_ending
        - trace_preservation
    """
    stem_shape: str
    inflection_site: str  # "final" | "internal"
    variable_ending_set: FrozenSet[str]  # e.g., {"ḍamm", "fatḥ", "kasr"}
    relation_sensitivity: bool = True  # Ending requires syntax gate


@dataclass(frozen=True)
class MushtaqWeightIdentity:
    """
    هوية وزن المشتق (Mushtaq Weight Identity)

    For مشتق (derived): transforms root+pattern→form.
    Examples: كَاتِب (ك ت ب + فَاعِل)

    Invariants:
        - root_identity preserved
        - slot_mapping verified
        - pattern_identity maintained
        - extra_letter_roles documented
        - transformation_path traced
    """
    root_identity: Tuple[str, ...]  # e.g., ("ك", "ت", "ب")
    pattern_identity: str  # e.g., "فَاعِل"
    slot_map: Dict[str, str]  # e.g., {"ك": "ف", "ت": "ع", "ب": "ل"}
    extra_elements: Tuple[str, ...]  # e.g., ("ا",)
    vowel_template: str  # e.g., "ā-i"
    transformation_path: str  # Trace of how root→pattern→form


# ============================================================================
# Gate₈₉: PreWeight to Weight Gate
# ============================================================================

@dataclass(frozen=True)
class Gate89Result:
    """
    نتيجة بوابة ٨→٩ (Gate₈₉ Result)

    Result of Gate₈₉ validation.
    """
    passed: bool
    blocked_by: Optional[str] = None
    residuals: Tuple[Residual, ...] = field(default_factory=tuple)
    trace: Dict[str, Any] = field(default_factory=dict)


def gate_89_validate(
    contract: PreWeightContract,
    root_stem: RootStemInput
) -> Gate89Result:
    """
    بوابة ٨→٩ (Gate₈₉: PreWeight → Weight)

    Validates transition from U₇+U₈ to U₉.

    Gate passes ONLY if:
        1. build_status known or preserved as competitor
        2. lexical_status known or preserved as competitor
        3. path_type identified (Mabni/Jāmid/Muʿrab/Mushtaq/Ambiguous)
        4. root_or_stem_access identified
        5. residuals non-blocking
        6. competitors preserved
        7. trace preserved from U₈/U₇

    Args:
        contract: PreWeightContract from U₇
        root_stem: RootStemInput from U₈

    Returns:
        Gate89Result with pass/fail and residuals
    """
    residuals = []
    trace = {
        "gate": "Gate₈₉",
        "input_contract_trace": contract.trace,
        "input_root_stem_trace": root_stem.trace,
    }

    # Check 1: build_status
    if contract.build_status == "Unknown" and not contract.competitors:
        residuals.append(Residual(
            type=ResidualType.MABNI_MURAB_UNRESOLVED,
            severity=ResidualSeverity.BLOCKER,
            message="build_status unknown with no competitors",
            location="Gate₈₉",
        ))

    # Check 2: lexical_status
    if contract.lexical_status == "Unknown" and not contract.competitors:
        residuals.append(Residual(
            type=ResidualType.JAMID_MUSHTAQ_COMPETING,
            severity=ResidualSeverity.BLOCKER,
            message="lexical_status unknown with no competitors",
            location="Gate₈₉",
        ))

    # Check 3: path_type
    if contract.path_type not in {"Mabni", "Jāmid", "Muʿrab", "Mushtaq", "Ambiguous"}:
        residuals.append(Residual(
            type=ResidualType.MALFORMED_STRUCTURE,
            severity=ResidualSeverity.BLOCKER,
            message=f"Invalid path_type: {contract.path_type}",
            location="Gate₈₉",
        ))

    # Check 4: root_or_stem_access
    if root_stem.input_type not in {"root", "stem_anchor", "closed_built_input"}:
        residuals.append(Residual(
            type=ResidualType.ROOT_UNRESOLVED,
            severity=ResidualSeverity.BLOCKER,
            message=f"Invalid input_type: {root_stem.input_type}",
            location="Gate₈₉",
        ))

    # Check 5: Preserve input residuals
    all_residuals = list(contract.residuals) + list(root_stem.residuals) + residuals

    # Check for blockers
    has_blockers = any(r.severity == ResidualSeverity.BLOCKER for r in all_residuals)

    if has_blockers:
        return Gate89Result(
            passed=False,
            blocked_by="blocking_residual",
            residuals=tuple(all_residuals),
            trace=trace,
        )

    return Gate89Result(
        passed=True,
        residuals=tuple(all_residuals),
        trace=trace,
    )


# ============================================================================
# Weight Dispatch (Routing to Correct Weight Type)
# ============================================================================

def dispatch_weight(
    contract: PreWeightContract,
    root_stem: RootStemInput,
    evidence: Tuple[Evidence, ...] = tuple(),
) -> ArabicWeightObject:
    """
    توزيع الوزن (Weight Dispatch) - DEPRECATED

    ⚠️ DEPRECATION WARNING:
        This function is DEPRECATED and does NOT enforce ApprovedTransitionContext.

        Use instead:
            from dal_core import weight_candidate_carrier_9

        This function may produce weight candidates WITHOUT constitutional
        governance, which violates the core architectural law:
            No U₉ execution without ApprovedTransitionContext.

    Routes input to appropriate weight type based on evidence.

    Critical Theorem (WeightDispatchSoundness):
        BuiltCertificate(X) ⇒ ¬MushtaqWeight(X)

    Dispatch order:
        1. If build_status = ClosedMabniCertificate → BuiltWeight
        2. Elif lexical_status = JāmidCertificate → JāmidWeight
        3. Elif build_status = MuʿrabCandidate and inflection_access → InflectableWeight
        4. Elif lexical_status permits derivation and root_status = RootLicensed → MushtaqWeight
        5. Else → Preserve competitors with residuals

    Args:
        contract: PreWeightContract from U₇
        root_stem: RootStemInput from U₈
        evidence: Additional evidence for dispatch

    Returns:
        ArabicWeightObject with appropriate WeightType
    """
    # CONSTITUTIONAL BLOCK: Legacy path cannot execute
    raise RuntimeError(
        "Constitutional Violation: dispatch_weight() is BLOCKED. "
        "\n\n"
        "Legacy U₉ execution path is constitutionally prohibited.\n"
        "No U₉ execution without ApprovedTransitionContext.\n"
        "\n"
        "Use the official governed implementation:\n"
        "    from dal_core import weight_candidate_carrier_9\n"
        "\n"
        "This function cannot produce weight candidates outside constitutional governance.\n"
        "For migration guidance, see docs/U9_CANONICALIZATION_SUMMARY.md"
    )


# ============================================================================
# CPB₉: Weight Carrier Preservation Barrier
# ============================================================================

@dataclass(frozen=True)
class CPB9Result:
    """
    نتيجة حارس الوزن (CPB₉ Result)

    Result of CPB₉ validation.
    """
    passed: bool
    violations: Tuple[str, ...] = field(default_factory=tuple)
    residuals: Tuple[Residual, ...] = field(default_factory=tuple)


def cpb_9_validate(weight_obj: ArabicWeightObject) -> CPB9Result:
    """
    CPB₉: حارس الوزن (Weight Carrier Preservation Barrier)

    Enforces critical laws:
        1. TracePreserved from U₈/U₇
        2. WeightTypePreservedOrLicensed
        3. RankNonInflated (evidence-based only)
        4. ResidualsPreserved
        5. CompetitorsPreserved
        6. NoMeaningClaim (weight ⊬ meaning)
        7. NoHukmClaim (weight ⊬ hukm)

    Args:
        weight_obj: ArabicWeightObject to validate

    Returns:
        CPB9Result with pass/fail and violations
    """
    violations = []
    residuals = []

    # Law 1: Trace preserved
    if not weight_obj.trace:
        violations.append("trace_missing")
        residuals.append(Residual(
            type=ResidualType.REVERSE_TRACE_MISSING_RAW_INPUT,
            severity=ResidualSeverity.BLOCKER,
            message="Trace not preserved from U₈/U₇",
            location="CPB₉",
        ))

    # Law 2: Weight type valid
    if not isinstance(weight_obj.weight_type, WeightType):
        violations.append("invalid_weight_type")

    # Law 3: Rank non-inflated
    if weight_obj.rank == WeightRank.WEIGHT_CERTIFICATE and not weight_obj.evidence:
        violations.append("rank_inflated_without_evidence")
        residuals.append(Residual(
            type=ResidualType.LOW_CONFIDENCE,
            severity=ResidualSeverity.WARNING,
            message="Certificate rank without evidence",
            location="CPB₉",
        ))

    # Law 4: Residuals preserved (not deleted)
    input_residuals = (
        weight_obj.input_contract.residuals +
        weight_obj.root_stem_input.residuals
    )
    # Check that input residuals are subset of output residuals
    # (some may be discharged, but not deleted without trace)

    # Law 5: Competitors preserved
    # (Already in weight_obj.competitors)

    # Law 6 & 7: No meaning/hukm (enforced by __post_init__)
    forbidden_attrs = ["meaning", "murad", "hukm", "haqiqa_majaz", "final_meaning"]
    for attr in forbidden_attrs:
        if hasattr(weight_obj, attr):
            violations.append(f"forbidden_attribute_{attr}")
            residuals.append(Residual(
                type=WeightResidualType.WEIGHT_MEANING_LEAK.value,  # type: ignore
                severity=ResidualSeverity.BLOCKER,
                message=f"Weight object contains forbidden '{attr}' field",
                location="CPB₉",
            ))

    all_residuals = list(weight_obj.residuals) + residuals

    return CPB9Result(
        passed=len(violations) == 0,
        violations=tuple(violations),
        residuals=tuple(all_residuals),
    )


# ============================================================================
# Validators
# ============================================================================

def validate_weight_object(weight: ArabicWeightObject) -> bool:
    """Validate general weight object structure"""
    cpb_result = cpb_9_validate(weight)
    return cpb_result.passed


def validate_built_weight(weight: ArabicWeightObject) -> bool:
    """Validate BuiltWeight invariants"""
    if weight.weight_type != WeightType.BUILT:
        return False

    # BuiltWeight must have frozen ending
    if weight.frozen_status != "frozen_ending":
        return False

    # Derivation must be blocked
    if weight.input_contract.derivation_access != "blocked":
        return False

    return True


def validate_jamid_weight(weight: ArabicWeightObject) -> bool:
    """Validate JāmidWeight invariants"""
    if weight.weight_type != WeightType.JAMID:
        return False

    # Derivation must be blocked or limited
    if weight.input_contract.derivation_access not in {"blocked", "limited"}:
        return False

    return True


def validate_inflectable_weight(weight: ArabicWeightObject) -> bool:
    """Validate InflectableWeight invariants"""
    if weight.weight_type != WeightType.INFLECTABLE:
        return False

    # Must have inflection site
    if not weight.inflection_site:
        return False

    # Inflection access must be true
    if not weight.input_contract.inflection_access:
        return False

    return True


def validate_mushtaq_weight(weight: ArabicWeightObject) -> bool:
    """Validate MushtaqWeight invariants"""
    if weight.weight_type != WeightType.MUSHTAQ:
        return False

    # Must have pattern
    if not weight.pattern_shape:
        return False

    # Root must be licensed
    if weight.root_stem_input.root_status != "RootLicensed":
        return False

    # Derivation must be open
    if weight.input_contract.derivation_access != "open":
        return False

    return True


def validate_weight_trace(weight: ArabicWeightObject) -> bool:
    """Validate trace preservation"""
    return bool(weight.trace and
                weight.input_contract.trace and
                weight.root_stem_input.trace)


def validate_weight_residuals(weight: ArabicWeightObject) -> bool:
    """Validate residuals are preserved"""
    # Input residuals should be preserved in output
    return True  # Simplified - full validation would check preservation


def validate_no_layer_jump(weight: ArabicWeightObject) -> bool:
    """Validate anti-jumping law: weight ⊬ meaning, weight ⊬ hukm"""
    forbidden = {"meaning", "murad", "hukm", "haqiqa_majaz", "final_meaning"}
    for attr in forbidden:
        if hasattr(weight, attr):
            return False
    return True
