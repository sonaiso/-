"""
K9 Storage Governance Contract (عقد حوكمة التخزين K9)

Constitutional Law K9: "Do not store derivable items as primitives"

This module implements the strengthened K9 constitutional law with five critical dimensions:
1. StorageKind: Type of storage (primitive, artifact, cache, etc.)
2. DerivationRank: Rank of derivation capability
3. ProofSource: Source of derivability proof
4. ResidualState: State of residuals blocking derivation
5. RegenerationPolicy: Policy for regenerating derived artifacts

Constitutional Formula:
    K9Violation(x) ⇔
        storage_type(x) = PRIMITIVE_STORAGE
        ∧ derivable(x) = True
        ∧ derivation_rank(x) ≥ required_replacement_rank(x)
        ∧ proof_source(x) is valid
        ∧ residual_state(x) ∈ {NO_RESIDUALS, NON_BLOCKING_RESIDUALS}

Purpose:
    Prevent T5 training artifacts and model outputs from becoming "primitive knowledge".
    Ensure all derived/cached items maintain:
    - source_trace_id
    - derivation_rule_id
    - regeneration_policy

Supreme Law:
    Derived items must NOT be stored as primitives.
    Primitives must NOT be deleted unless derivation is sufficient rank with no blocking residuals.
    Artifacts/cache must maintain constitutional bindings and regeneration policies.

Reference:
    User requirement: K9 Storage Governance Specification (2026-05-30)
    Builds on: PR #147 (Constitutional Evaluator), PR #163 (Identity/Trace separation)

Created: 2026-05-30
"""

from dataclasses import dataclass
from enum import Enum


# ============================================================================
# Storage Kind Taxonomy
# ============================================================================

class StorageKind(Enum):
    """
    نوع التخزين (Storage Type Classification)

    Distinguishes between different purposes of storage to prevent
    derived items from being stored as epistemological primitives.
    """
    PRIMITIVE = "primitive"  # بدائية معرفية - epistemological primitive
    DERIVED_ARTIFACT = "derived_artifact"  # أثر مشتق محفوظ للتشغيل - derived artifact for execution
    CACHE = "cache"  # تخزين مؤقت قابل للإبطال - invalidatable temporary storage
    INDEX = "index"  # فهرس لتسريع البحث - search acceleration index
    TRACE_LOG = "trace_log"  # أثر إثباتي - proof trace log
    EXCEPTION_OVERRIDE = "exception_override"  # استثناء/سماعي - exception/auditory override


# ============================================================================
# Derivation Rank Classification
# ============================================================================

class DerivationRank(Enum):
    """
    رتبة الاشتقاق (Derivation Rank)

    Not all derivation is equal. Derivation rank determines whether
    derived knowledge can replace primitive storage.

    Constitutional Law:
        Primitive storage forbidden ONLY if:
        derivation_rank ≥ required_replacement_rank

    Example:
        وزن فاعل → candidate role potential (FORM derivation)
        This is insufficient to replace lexical entry proving "طاهر" is adjective.
    """
    NOT_DERIVABLE = 0  # غير قابل للاشتقاق
    FORM = 1  # اشتقاق شكلي - formal/structural derivation
    QIYAS = 2  # اشتقاق قياسي - analogical derivation
    SAMA = 3  # اشتقاق سماعي - auditory/lexical derivation
    CERTIFIED = 4  # اشتقاق مصدّق - certified derivation


# ============================================================================
# Proof Source Classification
# ============================================================================

class ProofSource(Enum):
    """
    مصدر البرهان (Proof Source)

    K9 cannot work without proof source. We must know WHY something is derivable.

    Constitutional Law:
        Derivable(x) accepted ONLY if:
        proof_source ∈ {RULE, TRACE, TEST, TABLE, LEXICAL, GOVERNANCE}

    FORBIDDEN:
        proof_source == MODEL_OUTPUT

    Rationale:
        T5 is NOT a proof source. Model output may explain a trace,
        but does NOT prove derivability.
    """
    RULE = "rule"  # قاعدة اشتقاق - derivation rule
    TRACE = "trace"  # أثر خوارزمي سابق - algorithmic trace
    TEST = "test"  # اختبار يثبت التوليد - test proving generation
    TABLE = "table"  # جدول أصل - origin table
    LEXICAL = "lexical"  # معجم/سماع - lexicon/auditory
    GOVERNANCE = "governance"  # gate/transition proof
    MODEL_OUTPUT = "model_output"  # مرفوض كبرهان مستقل - REJECTED as independent proof


# ============================================================================
# Residual State Classification
# ============================================================================

class ResidualState(Enum):
    """
    حالة البقايا (Residual State)

    Item may be derivable BUT with residuals. K9 cannot be applied
    to delete primitive storage directly when residuals exist.

    Constitutional Law:
        If derivable=True BUT residual_state ∈ {DEFER, BLOCKING, UNKNOWN}
        Then primitive storage MUST NOT be deleted.
        Instead, record: derivable_with_residuals

    Example:
        Augmented verb derivation (تعدية) is often derivable,
        but if auditory exception (سماع) contradicts qiyas,
        residuals prevent deleting lexical entry.
    """
    NONE = "none"  # لا بقايا
    NON_BLOCKING = "non_blocking"  # بقايا غير مانعة
    DEFER = "defer"  # بقايا مؤجلة
    BLOCKING = "blocking"  # بقايا مانعة
    UNKNOWN = "unknown"  # حالة بقايا مجهولة


# ============================================================================
# Regeneration Policy Classification
# ============================================================================

class RegenerationPolicy(Enum):
    """
    سياسة التجديد (Regeneration Policy)

    Every derived item stored as artifact MUST know when to regenerate.
    Without regeneration policy, derived artifact becomes false primitive over time.

    Example for T5 TrainingExample:
        Must regenerate when:
        - AlgorithmTracePayload changes
        - TraceExplanationDatasetGenerator changes
        - TrainingExample schema changes
        - Adapter contract changes

    Cannot be left old as if it were truth.
    """
    NEVER = "never"  # بدائية ثابتة - fixed primitive
    ON_SOURCE_CHANGE = "on_source_change"  # إذا تغير الأصل
    ON_RULE_CHANGE = "on_rule_change"  # إذا تغيرت قاعدة الاشتقاق
    ON_TRACE_CHANGE = "on_trace_change"  # إذا تغير الأثر
    ON_SCHEMA_CHANGE = "on_schema_change"  # إذا تغير العقد
    ON_MODEL_VERSION = "on_model_version"  # إذا تغير adapter/model
    TTL_CACHE = "ttl_cache"  # مؤقت بزمن
    MANUAL_REVIEW = "manual_review"  # يحتاج مراجعة بشرية


# ============================================================================
# K9 Item Contract
# ============================================================================

@dataclass(frozen=True)
class K9Item:
    """
    K9 Storage Governance Item

    Represents an item subject to K9 constitutional law with all
    five critical dimensions for operationalizing K9.

    Fields:
        item_id: Unique identifier for the item
        storage_kind: Type of storage (primitive, artifact, cache, etc.)
        derivable: Whether item can be derived
        derivation_rank: Rank of derivation capability
        required_replacement_rank: Minimum rank needed to replace primitive
        proof_source: Source proving derivability
        residual_state: State of residuals
        regeneration_policy: Policy for artifact regeneration (required for non-primitives)
        source_trace_id: Constitutional binding to source trace (required for artifacts)
        derivation_rule_id: Rule/algorithm that derives this item (required for artifacts)

    Constitutional Requirements:
        1. If storage_kind is PRIMITIVE and derivable=True with sufficient rank,
           this is a K9 violation
        2. If storage_kind is artifact/cache/index, must have:
           - source_trace_id
           - derivation_rule_id
           - regeneration_policy
        3. proof_source must NOT be MODEL_OUTPUT for derivability claims
    """
    item_id: str
    storage_kind: StorageKind
    derivable: bool
    derivation_rank: DerivationRank
    required_replacement_rank: DerivationRank
    proof_source: ProofSource
    residual_state: ResidualState
    regeneration_policy: RegenerationPolicy | None
    source_trace_id: str | None = None
    derivation_rule_id: str | None = None


# ============================================================================
# K9 Validation Function
# ============================================================================

def verify_k9(item: K9Item) -> tuple[bool, str]:
    """
    Verify K9 Constitutional Law Compliance

    K9 Strengthened Formula:
        K9Violation(x) ⇔
            storage_type(x) = PRIMITIVE_STORAGE
            ∧ derivable(x) = True
            ∧ derivation_rank(x) ≥ required_replacement_rank(x)
            ∧ proof_source(x) is valid
            ∧ residual_state(x) ∈ {NO_RESIDUALS, NON_BLOCKING_RESIDUALS}

    For Derived Artifacts:
        StoredArtifact(x) allowed IF:
            source_trace_id exists
            derivation_rule_id exists
            regeneration_policy exists
            not_claimed_as_primitive

    Args:
        item: K9Item to validate

    Returns:
        (is_valid, reason_code)
        - is_valid: True if K9 compliant, False if violation
        - reason_code: Human-readable reason code

    Reason Codes:
        - "model_output_cannot_prove_derivability": MODEL_OUTPUT not valid proof
        - "primitive_storage_of_derivable_item": K9 violation - storing derivable as primitive
        - "derived_storage_missing_source_trace": Artifact missing source_trace_id
        - "derived_storage_missing_rule": Artifact missing derivation_rule_id
        - "derived_storage_missing_regeneration_policy": Artifact missing policy
        - "k9_ok": No violation, compliant
    """
    # Validation 1: MODEL_OUTPUT cannot prove derivability
    # T5 is NOT a constitutional proof source
    if item.proof_source == ProofSource.MODEL_OUTPUT:
        return False, "model_output_cannot_prove_derivability"

    # Validation 2: PRIMITIVE storage of derivable item
    # Core K9 violation
    if item.storage_kind == StorageKind.PRIMITIVE and item.derivable:
        # Check if derivation rank is sufficient to replace primitive
        if item.derivation_rank.value >= item.required_replacement_rank.value:
            # Check if residuals block replacement
            if item.residual_state in {ResidualState.NONE, ResidualState.NON_BLOCKING}:
                return False, "primitive_storage_of_derivable_item"

    # Validation 3: DERIVED artifacts must have constitutional bindings
    # Artifacts without bindings become false primitives
    if item.storage_kind in {
        StorageKind.DERIVED_ARTIFACT,
        StorageKind.CACHE,
        StorageKind.INDEX,
    }:
        if not item.source_trace_id:
            return False, "derived_storage_missing_source_trace"
        if not item.derivation_rule_id:
            return False, "derived_storage_missing_rule"
        if item.regeneration_policy is None:
            return False, "derived_storage_missing_regeneration_policy"

    # All validations passed
    return True, "k9_ok"


# ============================================================================
# K9 Constitutional Laws (Summary)
# ============================================================================

"""
K9 Constitutional Laws Summary:

Law 1: No Primitive Storage of Derivable Items
    ¬(storage_kind=PRIMITIVE ∧ derivable ∧ sufficient_rank ∧ no_blocking_residuals)

Law 2: No Derivability Claim from Model Output
    proof_source ≠ MODEL_OUTPUT for derivability claims

Law 3: Artifacts Require Constitutional Bindings
    (storage_kind ∈ {DERIVED_ARTIFACT, CACHE, INDEX})
    ⇒ (source_trace_id ∧ derivation_rule_id ∧ regeneration_policy)

Law 4: Derivation Rank Must Exceed Replacement Threshold
    Delete_Primitive(x) ⇒ derivation_rank(x) ≥ required_replacement_rank(x)

Law 5: Blocking Residuals Prevent Primitive Deletion
    residual_state ∈ {BLOCKING, DEFER, UNKNOWN} ⇒ ¬Delete_Primitive(x)

Architecture Impact:
    This formulation is directly usable before resuming T5, as it prevents
    training files and model outputs from becoming "original knowledge"
    inside the system.
"""
