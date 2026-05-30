# K9 Storage Governance Constitutional Law
**عقد حوكمة التخزين K9**

**Status**: Constitutional Framework
**Version**: 1.0
**Date**: 2026-05-30
**Authority**: Supreme Law of the General Algebra

---

## القانون الأعلى | The Supreme Law

**لا تُخزّن المشتقات كبدائيات.**
**Do not store derivable items as primitives.**

This constitutional law prevents:
- T5 training artifacts from becoming "primitive knowledge"
- Model outputs from being stored as epistemological foundations
- Cached/derived data from masquerading as original sources
- Loss of regeneration capability and constitutional bindings

---

## 1. The Problem: Binary "Stored/Derivable" is Insufficient

### Original K9 Formulation (Too Simple)
```
¬(stored ∧ derivable)
```

This binary formulation is **insufficient** for operational systems because:

1. **No storage type distinction**: "stored" doesn't distinguish between primitive, artifact, cache
2. **No derivation rank**: Not all derivation is equal (FORM vs QIYAS vs SAMA vs CERTIFIED)
3. **No proof source**: We don't know WHY something is derivable
4. **No residual handling**: Derivable items may have blocking residuals
5. **No regeneration policy**: Derived artifacts become stale primitives over time

### Real-World Failure Scenarios

**Scenario 1**: TrainingExample derived from trace
- **Problem**: Can we store it?
- **Binary K9 says**: No (derivable ∧ stored = violation)
- **Reality**: Must store as JSONL artifact for T5, but NOT as primitive knowledge

**Scenario 2**: Augmented verb تعدية
- **Problem**: Pattern derivable via قياس, but سماع contradicts
- **Binary K9 says**: Delete primitive lexical entry (derivable)
- **Reality**: Blocking residuals prevent deletion; lexical entry required

**Scenario 3**: Model output explanation
- **Problem**: T5 generates explanation from trace
- **Binary K9 says**: Unclear (is MODEL_OUTPUT valid proof?)
- **Reality**: Model output is NOT constitutional proof; cannot prove derivability

---

## 2. Strengthened K9: Five Critical Dimensions

### Dimension 1: Storage Kind (نوع التخزين)

Not all storage is "primitive". We must distinguish:

```python
class StorageKind(Enum):
    PRIMITIVE = "primitive"              # بدائية معرفية
    DERIVED_ARTIFACT = "derived_artifact"  # أثر مشتق محفوظ للتشغيل
    CACHE = "cache"                      # تخزين مؤقت قابل للإبطال
    INDEX = "index"                      # فهرس لتسريع البحث
    TRACE_LOG = "trace_log"              # أثر إثباتي
    EXCEPTION_OVERRIDE = "exception_override"  # استثناء/سماعي
```

**Constitutional Distinction**:
- **PRIMITIVE**: Epistemological foundation; claims to be original knowledge
- **DERIVED_ARTIFACT**: Execution artifact; knows it's derived, maintains bindings
- **CACHE**: Temporary optimization; invalidatable
- **INDEX**: Search acceleration; regenerable
- **TRACE_LOG**: Proof record; immutable history
- **EXCEPTION_OVERRIDE**: Auditory exception; overrides qiyas

**K9 Violation**: Only **PRIMITIVE** storage of derivable items violates K9.
Storing as **DERIVED_ARTIFACT** with proper bindings is **compliant**.

---

### Dimension 2: Derivation Rank (رتبة الاشتقاق)

Not all derivation is sufficient to replace primitives.

```python
class DerivationRank(Enum):
    NOT_DERIVABLE = 0  # غير قابل للاشتقاق
    FORM = 1           # اشتقاق شكلي - structural only
    QIYAS = 2          # اشتقاق قياسي - analogical
    SAMA = 3           # اشتقاق سماعي - auditory/lexical
    CERTIFIED = 4      # اشتقاق مصدّق - certified
```

**Constitutional Law**:
```
Primitive storage forbidden ONLY if:
derivation_rank ≥ required_replacement_rank
```

**Example**:
- **Pattern وزن فاعل → candidate role potential** (FORM derivation, rank=1)
- **Required rank for lexical replacement** (SAMA, rank=3)
- **Result**: Primitive lexical entry for "طاهر" (adjective) cannot be deleted
- **Reason**: FORM derivation insufficient; lexical entry needed to distinguish adjective from active participle

---

### Dimension 3: Proof Source (مصدر البرهان)

K9 cannot work without knowing **why** something is derivable.

```python
class ProofSource(Enum):
    RULE = "rule"              # قاعدة اشتقاق
    TRACE = "trace"            # أثر خوارزمي سابق
    TEST = "test"              # اختبار يثبت التوليد
    TABLE = "table"            # جدول أصل
    LEXICAL = "lexical"        # معجم/سماع
    GOVERNANCE = "governance"  # gate/transition proof
    MODEL_OUTPUT = "model_output"  # مرفوض كبرهان مستقل
```

**Constitutional Law**:
```
Derivable(x) accepted ONLY if:
proof_source ∈ {RULE, TRACE, TEST, TABLE, LEXICAL, GOVERNANCE}

FORBIDDEN:
proof_source == MODEL_OUTPUT
```

**Rationale**: T5 is NOT a constitutional proof source.
- Model output may **explain** a trace
- Model output does NOT **prove** derivability
- Model output is **description**, not **constitutional fact**

---

### Dimension 4: Residual State (حالة البقايا)

Item may be derivable BUT with blocking residuals.

```python
class ResidualState(Enum):
    NONE = "none"                # لا بقايا
    NON_BLOCKING = "non_blocking"  # بقايا غير مانعة
    DEFER = "defer"              # بقايا مؤجلة
    BLOCKING = "blocking"        # بقايا مانعة
    UNKNOWN = "unknown"          # حالة بقايا مجهولة
```

**Constitutional Law**:
```
If derivable=True BUT residual_state ∈ {DEFER, BLOCKING, UNKNOWN}
Then primitive storage MUST NOT be deleted
Instead record: derivable_with_residuals
```

**Example**:
- **Augmented verb**: Can derive تعدية via قياس generally
- **But**: سماع contradicts قياس for specific verb
- **Result**: BLOCKING residuals prevent deleting lexical entry
- **Storage**: Primitive lexical entry + residual annotation

---

### Dimension 5: Regeneration Policy (سياسة التجديد)

Every derived artifact must know **when to regenerate**.

```python
class RegenerationPolicy(Enum):
    NEVER = "never"                      # بدائية ثابتة
    ON_SOURCE_CHANGE = "on_source_change"  # إذا تغير الأصل
    ON_RULE_CHANGE = "on_rule_change"    # إذا تغيرت قاعدة الاشتقاق
    ON_TRACE_CHANGE = "on_trace_change"  # إذا تغير الأثر
    ON_SCHEMA_CHANGE = "on_schema_change"  # إذا تغير العقد
    ON_MODEL_VERSION = "on_model_version"  # إذا تغير adapter/model
    TTL_CACHE = "ttl_cache"              # مؤقت بزمن
    MANUAL_REVIEW = "manual_review"      # يحتاج مراجعة بشرية
```

**Constitutional Law**:
```
Without regeneration_policy:
derived_artifact → stale_artifact → false_primitive (over time)
```

**Example for T5 TrainingExample**:
Must regenerate when:
1. **AlgorithmTracePayload changes** (source changed)
2. **TraceExplanationDatasetGenerator changes** (rule changed)
3. **TrainingExample schema changes** (schema changed)
4. **Adapter contract changes** (model version changed)

Cannot be left old as if it were truth.

---

## 3. Strengthened K9 Formula

### Core K9 Violation Definition

```python
K9Violation(x) ⇔
    storage_type(x) = PRIMITIVE_STORAGE
    ∧ derivable(x) = True
    ∧ derivation_rank(x) ≥ required_replacement_rank(x)
    ∧ proof_source(x) is valid  # NOT MODEL_OUTPUT
    ∧ residual_state(x) ∈ {NO_RESIDUALS, NON_BLOCKING_RESIDUALS}
```

### Derived Artifact Requirements

```python
StoredArtifact(x) allowed IF:
    source_trace_id exists            # Constitutional binding
    derivation_rule_id exists         # Derivation provenance
    regeneration_policy exists        # Regeneration contract
    not_claimed_as_primitive          # Epistemological honesty
```

---

## 4. Constitutional Laws (Complete Set)

### Law 1: No Primitive Storage of Derivable Items
```
¬(storage_kind=PRIMITIVE ∧ derivable ∧ sufficient_rank ∧ no_blocking_residuals)
```

**Violation**: Storing derivable item with sufficient rank and no blocking residuals as PRIMITIVE.
**Remedy**: Store as DERIVED_ARTIFACT with bindings, or maintain PRIMITIVE with residual annotation.

---

### Law 2: No Derivability Claim from Model Output
```
proof_source ≠ MODEL_OUTPUT for derivability claims
```

**Violation**: Using T5/model output as proof that something is derivable.
**Remedy**: Use TRACE, RULE, GOVERNANCE, LEXICAL, TEST, or TABLE as proof source.

---

### Law 3: Artifacts Require Constitutional Bindings
```
(storage_kind ∈ {DERIVED_ARTIFACT, CACHE, INDEX})
⇒ (source_trace_id ∧ derivation_rule_id ∧ regeneration_policy)
```

**Violation**: Derived artifact missing source_trace_id, derivation_rule_id, or regeneration_policy.
**Remedy**: Add all three required bindings to artifact.

---

### Law 4: Derivation Rank Must Exceed Replacement Threshold
```
Delete_Primitive(x) ⇒ derivation_rank(x) ≥ required_replacement_rank(x)
```

**Violation**: Deleting primitive when derivation rank insufficient.
**Example**: Cannot delete lexical entry "طاهر" (adjective) with only FORM-level pattern derivation.
**Remedy**: Maintain primitive until SAMA or CERTIFIED derivation available.

---

### Law 5: Blocking Residuals Prevent Primitive Deletion
```
residual_state ∈ {BLOCKING, DEFER, UNKNOWN} ⇒ ¬Delete_Primitive(x)
```

**Violation**: Deleting primitive when residuals block derivation.
**Example**: Cannot delete augmented verb entry when سماع contradicts قياس.
**Remedy**: Maintain primitive with residual annotation; mark derivable_with_residuals.

---

## 5. Implementation Contract

### K9Item Dataclass

```python
@dataclass(frozen=True)
class K9Item:
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
```

### Validation Function

```python
def verify_k9(item: K9Item) -> tuple[bool, str]:
    """
    Returns: (is_valid, reason_code)

    Reason codes:
        - "model_output_cannot_prove_derivability"
        - "primitive_storage_of_derivable_item"
        - "derived_storage_missing_source_trace"
        - "derived_storage_missing_rule"
        - "derived_storage_missing_regeneration_policy"
        - "k9_ok"
    """
```

---

## 6. Real-World Application Examples

### Example 1: TrainingExample (Compliant)

```python
training_example = K9Item(
    item_id="training_example_001",
    storage_kind=StorageKind.DERIVED_ARTIFACT,  # NOT primitive
    derivable=True,
    derivation_rank=DerivationRank.QIYAS,
    required_replacement_rank=DerivationRank.FORM,
    proof_source=ProofSource.TRACE,  # Derived from algorithmic trace
    residual_state=ResidualState.NON_BLOCKING,
    regeneration_policy=RegenerationPolicy.ON_TRACE_CHANGE,
    source_trace_id="algorithm_trace_payload_789",
    derivation_rule_id="TraceExplanationDatasetGenerator",
)

is_valid, reason = verify_k9(training_example)
# Result: True, "k9_ok"
```

**Compliant because**:
- Stored as DERIVED_ARTIFACT (not primitive)
- Has source_trace_id (constitutional binding)
- Has derivation_rule_id (provenance)
- Has regeneration_policy (regeneration contract)

---

### Example 2: TrainingExample as Primitive (Violation)

```python
training_example_bad = K9Item(
    item_id="training_example_002",
    storage_kind=StorageKind.PRIMITIVE,  # VIOLATION
    derivable=True,
    derivation_rank=DerivationRank.QIYAS,
    required_replacement_rank=DerivationRank.FORM,
    proof_source=ProofSource.TRACE,
    residual_state=ResidualState.NONE,
    regeneration_policy=None,
)

is_valid, reason = verify_k9(training_example_bad)
# Result: False, "primitive_storage_of_derivable_item"
```

**Violation because**:
- Stored as PRIMITIVE (epistemological claim)
- Derivable with sufficient rank
- No blocking residuals
- K9 violation: primitive storage of derivable item

---

### Example 3: Lexical Entry (Compliant)

```python
lexical_entry = K9Item(
    item_id="lexical_entry_طاهر",
    storage_kind=StorageKind.PRIMITIVE,
    derivable=False,  # Lexical, not derivable from pattern alone
    derivation_rank=DerivationRank.NOT_DERIVABLE,
    required_replacement_rank=DerivationRank.NOT_DERIVABLE,
    proof_source=ProofSource.LEXICAL,
    residual_state=ResidualState.NONE,
    regeneration_policy=None,
)

is_valid, reason = verify_k9(lexical_entry)
# Result: True, "k9_ok"
```

**Compliant because**:
- Not derivable (lexical knowledge)
- Primitive storage allowed for non-derivable items

---

### Example 4: Augmented Verb with Blocking Residuals (Compliant)

```python
verb_with_residuals = K9Item(
    item_id="verb_augmented_سمع",
    storage_kind=StorageKind.PRIMITIVE,
    derivable=True,  # Can derive تعدية via قياس
    derivation_rank=DerivationRank.QIYAS,
    required_replacement_rank=DerivationRank.QIYAS,
    proof_source=ProofSource.RULE,
    residual_state=ResidualState.BLOCKING,  # سماع contradicts قياس
    regeneration_policy=None,
)

is_valid, reason = verify_k9(verb_with_residuals)
# Result: True, "k9_ok"
```

**Compliant because**:
- Blocking residuals prevent primitive deletion
- Epistemologically honest: lexical entry required despite derivability

---

### Example 5: Model Output as Proof (Violation)

```python
model_derived = K9Item(
    item_id="model_output_001",
    storage_kind=StorageKind.DERIVED_ARTIFACT,
    derivable=True,
    derivation_rank=DerivationRank.FORM,
    required_replacement_rank=DerivationRank.FORM,
    proof_source=ProofSource.MODEL_OUTPUT,  # FORBIDDEN
    residual_state=ResidualState.NONE,
    regeneration_policy=RegenerationPolicy.ON_MODEL_VERSION,
    source_trace_id="trace_123",
    derivation_rule_id="rule_456",
)

is_valid, reason = verify_k9(model_derived)
# Result: False, "model_output_cannot_prove_derivability"
```

**Violation because**:
- MODEL_OUTPUT is not valid constitutional proof
- T5 cannot prove derivability; it only describes

---

## 7. Architecture Impact

### Before T5 Integration

This strengthened K9 formulation is **directly usable before resuming T5** because:

1. **Prevents training files from becoming primitives**
   - TrainingExample must be DERIVED_ARTIFACT
   - Must maintain source_trace_id
   - Must have regeneration_policy

2. **Prevents model outputs from becoming knowledge**
   - MODEL_OUTPUT cannot be proof_source
   - Model explanations are descriptions, not constitutional facts

3. **Enforces regeneration contracts**
   - Artifacts know when to regenerate
   - Schema changes, trace changes, model version changes trigger regeneration
   - Prevents stale artifacts from masquerading as truth

4. **Maintains epistemological honesty**
   - Primitives are primitives
   - Artifacts are artifacts
   - Constitutional bindings preserved
   - Derivation provenance tracked

---

## 8. Integration with Existing Constitutional Framework

### Relationship to PR #163 (Identity/Trace Separation)

K9 **complements** identity/trace separation:
- **PR #163**: identity_ids ≠ trace_ids
- **K9**: primitives ≠ artifacts; artifacts require trace bindings

**Combined formula**:
```python
DERIVED_ARTIFACT(x) ⇒
    source_trace_id(x)  # K9 requirement
    ∧ identity_ids(x) ≠ trace_ids(x)  # PR #163 requirement
```

---

### Relationship to PR #147 (Constitutional Evaluator)

K9 **extends** constitutional evaluation:
- **PR #147**: Detects authority claims, rank upgrades, residual deletion
- **K9**: Detects primitive storage of derivable items

**Combined detection**:
```python
class ConstitutionalViolationType(Enum):
    # ... existing violations from PR #147 ...
    K9_PRIMITIVE_STORAGE_OF_DERIVABLE = auto()  # New
    K9_MODEL_OUTPUT_PROOF_SOURCE = auto()  # New
    K9_ARTIFACT_MISSING_BINDINGS = auto()  # New
```

---

### Relationship to TrainingExample (PR #146)

K9 **governs** TrainingExample storage:
- **PR #146**: TrainingExample structure and export
- **K9**: Storage governance for TrainingExample

**Required K9 fields for TrainingExample**:
```python
@dataclass(frozen=True)
class TrainingExample:
    # ... existing fields from PR #146 ...

    # K9 governance fields
    k9_storage_kind: StorageKind = StorageKind.DERIVED_ARTIFACT
    k9_derivation_rank: DerivationRank = DerivationRank.QIYAS
    k9_proof_source: ProofSource = ProofSource.TRACE
    k9_regeneration_policy: RegenerationPolicy = RegenerationPolicy.ON_TRACE_CHANGE
```

---

## 9. Testing Requirements

### Constitutional Tests (25 tests minimum)

1. **K9 Core Violation** (6 tests)
   - Primitive storage of derivable item (violation)
   - Insufficient derivation rank (allowed)
   - Blocking residuals (allowed)
   - Defer residuals (allowed)
   - Unknown residuals (allowed)
   - Not derivable (allowed)

2. **MODEL_OUTPUT Proof Source** (3 tests)
   - MODEL_OUTPUT rejected for derivability
   - MODEL_OUTPUT rejected for primitives
   - Valid proof sources accepted

3. **Artifact Bindings** (6 tests)
   - Missing source_trace_id (violation)
   - Missing derivation_rule_id (violation)
   - Missing regeneration_policy (violation)
   - CACHE missing bindings (violation)
   - INDEX missing bindings (violation)
   - Valid artifact with all bindings (compliant)

4. **Derivation Rank** (3 tests)
   - Equal rank triggers violation
   - Greater rank triggers violation
   - Lesser rank allows primitive

5. **Real-World Scenarios** (5 tests)
   - TrainingExample as DERIVED_ARTIFACT (compliant)
   - TrainingExample as PRIMITIVE (violation)
   - Lexical entry as PRIMITIVE (compliant)
   - Augmented verb with residuals (compliant)
   - Model output JSONL as artifact (compliant)

6. **Enum Completeness** (2 tests)
   - All enum values present
   - Derivation rank ordering correct

---

## 10. Summary

### What K9 Now Says

**Before (binary)**:
> Do not store what can be derived.

**After (five-dimensional)**:
> 1. Do not store derived items as primitives.
> 2. Do not delete primitives unless derivation is sufficient rank with no blocking residuals.
> 3. Derived artifacts must maintain trace, rule, and regeneration policy.
> 4. Model output cannot prove derivability.
> 5. Without regeneration policy, artifacts become false primitives over time.

### Why This Matters for T5

This strengthened K9 prevents:
- ✅ Training files from becoming "primitive knowledge"
- ✅ Model outputs from being stored as epistemological foundations
- ✅ Cached/derived data from losing constitutional bindings
- ✅ Stale artifacts from masquerading as truth
- ✅ T5 explanations from becoming constitutional facts

This formulation is **directly applicable before T5 integration** and ensures constitutional governance throughout the training pipeline.

---

**File**: `/home/runner/work/-/-/src/dal_core/k9_storage_governance.py`
**Tests**: `/home/runner/work/-/-/tests/dal_core/test_k9_storage_governance.py`
**Documentation**: `/home/runner/work/-/-/docs/K9_STORAGE_GOVERNANCE_CONSTITUTION.md`

**Created**: 2026-05-30
**Status**: Ready for Constitutional Review
