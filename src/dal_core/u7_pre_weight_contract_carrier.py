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

        # Determine blocked paths
        blocked_paths = []
        required_evidence = []

        if contract_status == ContractStatus.CLOSED_CLASS_BLOCKED:
            blocked_paths = ["root_extraction", "weight_determination", "stem_extraction"]
            required_evidence = ["closed_class_mabni_blocks_morphology"]
        elif contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE:
            required_evidence = ["lexical_attestation", "surface_family_evidence"]

        # Determine open/closed status
        if contract_status == ContractStatus.CLOSED_CLASS_BLOCKED:
            open_closed_status = "closed_class"
        else:
            open_closed_status = "open_class"

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
