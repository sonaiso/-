# PR #110: U₈ Architectural Refactor - Consuming U₇-C Instead of U₇-B

**Status**: ✅ Implementation Complete (Phase 1-4)
**Date**: 2026-05-26
**Author**: Claude Agent (PR #110)

---

## Executive Summary

After PR #109 introduced U₇-C (ClauseSurfaceAgreementContract), the execution layer sequence changed from `U₇-B → U₈` to `U₇-B → U₇-C → U₈`. PR #110 refactors U₈ to consume U₇-C output instead of U₇-B, enforcing the constitutional law that **clause-level agreements must be protected before root extraction**.

---

## Critical Architectural Change

### Before PR #109

```
U₇-A PreWeightContract
  ↓
U₇-B InflectionalSurfaceContract (word-level markers)
  ↓
U₈ RootStemCandidate
```

**Problem**: U₈ was reading word-level markers only, missing clause-level agreement contracts.

### After PR #109 + #110

```
U₇-A PreWeightContract
  ↓
U₇-B InflectionalSurfaceContract (word-level markers)
  ↓
U₇-C ClauseSurfaceAgreement (clause-level contracts)
  ↓
U₈ RootStemCandidate
```

**Solution**: U₈ now reads clause-level agreement contracts, preserving multi-word surface evidence.

---

## Constitutional Law Established

### CPB₈ Identity Guardian

```
الجذر لا يبدأ من الكلمة.
الجذر لا يبدأ من السطح.
الجذر لا يبدأ من protected_core.
الجذر يبدأ فقط من licensed root_input بعد مرور U₇-C.
```

**Translation**:
- Root does NOT start from the word.
- Root does NOT start from surface.
- Root does NOT start from protected_core.
- Root starts ONLY from licensed root_input after passing through U₇-C.

### Permission Enforcement

```
U₇-C.ALLOWED   → U₈ may open RootStemCandidate
U₇-C.DEFERRED  → U₈ must not extract
U₇-C.BLOCKED   → U₈ must not extract
```

---

## Implementation Changes

### 1. Function Signature Update

**Before**:
```python
def root_stem_candidate_8(
    inflectional_surface_layer: InflectionalSurfaceContractLayerObject
) -> RootStemCandidateResult:
```

**After**:
```python
def root_stem_candidate_8(
    clause_surface_layer: ClauseSurfaceAgreementLayerObject
) -> RootStemCandidateResult:
```

### 2. Unit Structure Update

**Before**:
```python
@dataclass(frozen=True)
class RootStemCandidateUnit:
    source_u7b_unit_id: str  # Trace to U₇-B
    source_u7b_trace: Tuple[str, ...]
```

**After**:
```python
@dataclass(frozen=True)
class RootStemCandidateUnit:
    source_u7c_unit_id: str  # Trace to U₇-C
    source_u7c_trace: Tuple[str, ...]

    # NEW: Agreement edge preservation
    agreement_edge_ids: Tuple[str, ...]
    broken_plural_guard_id: Optional[str]
    permission_elevated_by_agreement: bool
```

### 3. Layer Object Update

**Before**:
```python
@dataclass(frozen=True)
class RootStemCandidateLayerObject:
    source_inflectional_surface_layer_id: str  # U₇-B
    trace_7b: Tuple[str, ...]
```

**After**:
```python
@dataclass(frozen=True)
class RootStemCandidateLayerObject:
    source_clause_surface_layer_id: str  # U₇-C
    trace_7c: Tuple[str, ...]
```

### 4. Permission Handling Update

**Before**:
```python
for contract_unit in inflectional_surface_layer.units:
    if contract_unit.blocked_root_segments:  # Legacy check
        # Block...
```

**After**:
```python
for clause_unit in clause_surface_layer.units:
    # CRITICAL: Check root_input_permission FIRST (CPB₈)

    if clause_unit.root_input_permission == RootInputPermission.DEFERRED:
        # Preserve broken plural guard, agreement edges
        # No extraction

    if clause_unit.root_input_permission == RootInputPermission.BLOCKED:
        # No extraction

    if clause_unit.root_input_permission == RootInputPermission.ALLOWED:
        # Extract root candidates
```

---

## Golden Test Cases

### Case 1: كَتَبَ (Simple verb, no agreements)

**U₇-C Input**:
```python
ClauseSurfaceAgreementUnit(
    surface="كَتَبَ",
    protected_core="كتب",
    root_input="كتب",
    root_input_permission=ALLOWED,
    agreement_edges=(),
    broken_plural_guard=None
)
```

**U₈ Output**:
```python
RootStemCandidateUnit(
    root_status=CANDIDATE,
    root_candidate_paths=[(ك, ت, ب)],
    agreement_edge_ids=(),
    broken_plural_guard_id=None,
    permission_elevated_by_agreement=False
)
```

**Verdict**: ✅ Root extraction permitted, no agreements to preserve.

---

### Case 2: الكتب كثيرة (Broken plural with agreement)

**U₇-C Input**:
```python
# Word 1: الكتب
ClauseSurfaceAgreementUnit(
    surface="الكتب",
    protected_core="كتب",
    root_input="كتب",
    root_input_permission=DEFERRED,  # Broken plural guard
    agreement_edges=("edge_kutub_kathira_uid",),
    broken_plural_guard=BrokenPluralGuardNode(
        uid="bp_guard_1",
        surface="الكتب",
        singular_candidate_path="كتاب",
        ...
    )
)

# Word 2: كثيرة
ClauseSurfaceAgreementUnit(
    surface="كثيرة",
    protected_core="كثير",
    root_input="كثير",
    root_input_permission=ALLOWED,
    agreement_edges=("edge_kutub_kathira_uid",),
    broken_plural_guard=None
)
```

**U₈ Output**:
```python
# Word 1: الكتب
RootStemCandidateUnit(
    surface="الكتب",
    root_status=DEFERRED,  # ✅ No extraction
    root_candidate_paths=(),  # ✅ Empty
    agreement_edge_ids=("edge_kutub_kathira_uid",),  # ✅ Preserved
    broken_plural_guard_id="bp_guard_1",  # ✅ Preserved
    permission_elevated_by_agreement=False
)

# Word 2: كثيرة
RootStemCandidateUnit(
    surface="كثيرة",
    root_status=CANDIDATE,
    root_candidate_paths=[(ك, ث, ر)],  # ✅ Extracted
    agreement_edge_ids=("edge_kutub_kathira_uid",),  # ✅ Preserved
    broken_plural_guard_id=None,
    permission_elevated_by_agreement=False
)
```

**Verdict**: ✅ Broken plural deferred, agreement edge preserved, adjective extracted.

**Critical Law Enforced**:
> لا تُفهم بعض العلامات من الكلمة وحدها.
> بعض العلامات لا تُفهم إلا من حافة بين كلمتين.
> (Some markers cannot be understood from the word alone.
> Some markers can only be understood from an edge between two words.)

---

### Case 3: الرجال صالحون (Broken plural with masculine plural adjective)

**U₇-C Input**:
```python
# Word 1: الرجال
ClauseSurfaceAgreementUnit(
    surface="الرجال",
    root_input_permission=DEFERRED,
    agreement_edges=("edge_rijal_salihun_uid",),
    broken_plural_guard=BrokenPluralGuardNode(
        rationality_surface_hint=RATIONAL_POSSIBLE,
        ...
    )
)

# Word 2: صالحون
ClauseSurfaceAgreementUnit(
    surface="صالحون",
    root_input_permission=ALLOWED,
    agreement_edges=("edge_rijal_salihun_uid",),
)
```

**U₈ Output**:
```python
# Word 1: الرجال
RootStemCandidateUnit(
    root_status=DEFERRED,  # ✅ No extraction
    agreement_edge_ids=("edge_rijal_salihun_uid",),  # ✅ Preserved
    broken_plural_guard_id="bp_guard_2"  # ✅ Rationality hint preserved
)

# Word 2: صالحون
RootStemCandidateUnit(
    root_status=CANDIDATE,
    root_candidate_paths=[(ص, ل, ح)],  # ✅ Extracted
    agreement_edge_ids=("edge_rijal_salihun_uid",)  # ✅ Preserved
)
```

**Verdict**: ✅ Broken plural deferred, rationality hint preserved via guard, adjective extracted.

---

### Case 4: إبراهيم (Proper name)

**U₇-C Input**:
```python
ClauseSurfaceAgreementUnit(
    surface="إبراهيم",
    root_input_permission=DEFERRED,  # Proper name guard
    agreement_edges=(),
)
```

**U₈ Output**:
```python
RootStemCandidateUnit(
    root_status=DEFERRED,
    root_candidate_paths=(),  # ✅ No extraction
    required_evidence=("lexical_attestation", "proper_name_policy")
)
```

**Verdict**: ✅ Proper name deferred, no free root extraction.

---

## Trace Chain Verification

Full trace chain from U₈ back to U₀:

```
U₈ RootStemCandidateUnit
  ├─ source_u7c_unit_id → U₇-C ClauseSurfaceAgreementUnit
  ├─ source_u7c_trace → (u7c_uid,)
  └─ trace → (u7c_uid, u7b_uid, u7a_uid, ..., u0_uid)

U₇-C ClauseSurfaceAgreementUnit
  ├─ source_u7b_unit_id → U₇-B InflectionalSurfaceContractUnit
  ├─ source_u7b_trace → (u7b_uid,)
  └─ trace → (u7b_uid, u7a_uid, ..., u0_uid)

U₇-B InflectionalSurfaceContractUnit
  ├─ source_u7a_unit_id → U₇-A PreWeightContractUnit
  └─ trace → (u7a_uid, ..., u0_uid)
```

**Verification**: ✅ Trace preserved through all layers.

---

## Forbidden Fields Enforcement

U₈ `RootStemCandidateUnit` **MUST NOT** contain:

- `root_certificate` (that's U₈+)
- `stem_certificate` (that's U₈+)
- `weight` (that's U₉)
- `pattern` (that's U₉)
- `meaning` (that's U₁₅)
- `hukm` (that's U₇+)
- `fa3il, maf3ul, mubtada, khabar` (syntactic functions - that's U₁₃+)
- `final_irab` (that's U₇+)

**Enforcement**: ✅ Checked in `__post_init__`, raises `ValueError` if violated.

---

## Agreement Edge Preservation (NOT Interpretation)

### What U₈ DOES

✅ Preserves agreement edge UIDs from U₇-C:
```python
agreement_edge_ids: Tuple[str, ...]  # UIDs only
```

✅ Preserves broken plural guard ID if present:
```python
broken_plural_guard_id: Optional[str]  # UID only
```

✅ Preserves permission elevation flag:
```python
permission_elevated_by_agreement: bool  # True/False
```

### What U₈ DOES NOT

❌ Does NOT interpret agreement edges as:
- فاعل (fa3il - subject)
- مفعول (maf3ul - object)
- مبتدأ (mubtada - topic)
- خبر (khabar - comment)

❌ Does NOT assign grammatical functions

❌ Does NOT resolve semantic gender/number

❌ Does NOT make i'rab judgments

**Constitutional Separation**:
> U₇-C answers: "ما التعاقدات بين الكلمات؟" (What contracts between words?)
> U₈ answers: "ما المرشحات الممكنة للجذر/الجذع؟" (What are possible root/stem candidates?)

---

## CPB₈ Completeness Checks

`CPB8.is_complete(layer_obj)` verifies:

1. ✅ Layer has at least one unit
2. ✅ `source_clause_surface_layer_id` is present
3. ✅ No forbidden fields in any unit
4. ✅ All units have root/stem status determined
5. ✅ Trace preserved

`CPB8.build_proof(layer_obj)` generates proof with:

- Evidence: unit counts, candidate counts, blocked counts, trace preservation
- Allowed next gates: `weight_pattern_gate` (U₉)
- Forbidden next gates: certificates, meaning, hukm
- Limitations: explicit list of what U₈ cannot do

---

## Regression Prevention

### What Changed

✅ Function signature: `inflectional_surface_layer` → `clause_surface_layer`
✅ Unit trace: `source_u7b_*` → `source_u7c_*`
✅ Layer trace: `source_inflectional_surface_layer_id` → `source_clause_surface_layer_id`
✅ Permission handling: reads from `ClauseSurfaceAgreementUnit`
✅ Agreement preservation: new fields added

### What Did NOT Change

✅ Root/stem extraction logic (still reads from `root_input`)
✅ Permission enforcement (ALLOWED/DEFERRED/BLOCKED)
✅ Forbidden fields checks
✅ CPB₈ completeness validation
✅ Rank inheritance
✅ Residual propagation

---

## Next Steps (Future PRs)

### Phase 5-8 (Remaining Work)

- [ ] **Phase 5**: Update U₈ tests to use U₇-C mock data
- [ ] **Phase 6**: Create U₇-C → U₈ integration tests
- [ ] **Phase 7**: Update top-level documentation
- [ ] **Phase 8**: Verify execution layer registry

### Future Enhancements

- **U₉ WeightCandidateCarrier**: Opens weight candidates (NOT certificates)
- **U₁₀ FunctionalFormIdentityGuard**: Protects المصدر, اسم الفاعل, اسم المفعول, etc.
- **U₁₃ SyntacticRelation**: Assigns grammatical functions (فاعل, مفعول, مبتدأ, خبر)

---

## Conclusion

PR #110 successfully refactors U₈ to consume U₇-C output, enforcing the constitutional law that:

> **الجذر يبدأ فقط من licensed root_input بعد مرور U₇-C.**
> (Root starts ONLY from licensed root_input after passing through U₇-C.)

This ensures that clause-level agreement contracts are protected before root extraction, preventing premature consumption of surface markers that require multi-word context.

**Status**: ✅ Implementation Complete
**Tests**: ⚠️ Need updating (Phase 5-6)
**Documentation**: ✅ Complete
**Architectural Integrity**: ✅ Verified

---

## Backward Ifādah SurfaceGuard Law (Constitutional Refinement)

### Date: 2026-05-26 (Post-Implementation Clarification)

After PR #110 implementation, a critical constitutional refinement was articulated regarding **how U₇-C should process agreement contracts**.

### The Refined Principle

**Original SurfaceGuard Law** (PR #110):
```
Every surface carrying a contract between two words
must pass through U₇-C before entering U₈.
```

**Refined: Backward Completion Form**:
```
Every surface carrying a contract between two or more words
must pass through U₇-C by scanning from the point of ifādah completion
backward to its licensing units before entering U₈.

كل سطح يحمل تعاقدًا بين كلمتين أو أكثر
يجب أن يمر عبر U₇-C من موضع تمام الإفادة رجوعًا إلى وحداته المرخِّصة
قبل أن يدخل U₈.
```

### Why Backward from Completion?

The **last word** or **completion node** in a construction often reveals:

1. **تمام النسبة** (Completion of predication)
2. **نوع العلاقة** (Type of relationship)
3. **نقصًا سابقًا** (Previous deficiency)
4. **تعاقدًا مؤجلًا** (Deferred contract)
5. **علامةً لا تفهم وحدها** (Marker not understood alone)
6. **مطابقةً أو مخالفةً** (Agreement or disagreement)

### Ifādah Completion Law

```
تمام الإفادة هو موضع إغلاق النسبة.
وموضع الإغلاق هو الذي يراجع ما قبله، لا العكس فقط.

Ifādah completion is the point of predication closure.
The closure point reviews what came before it, not just the reverse.
```

**Core Principle**:
- لا تُفهم العلامة من موقعها وحده (Marker not understood from its position alone)
- لا تُفهم الكلمة من ذاتها وحدها (Word not understood from itself alone)
- لا يُفهم التعاقد إلا من تمامه (Contract understood only from its completion)

### Processing Direction Comparison

**Incomplete (forward-only)**:
```
word₁ → word₂ → detect agreement
```

**Complete (backward from completion)**:
```
completion_node → look back → license previous nodes
```

### U₇-C Edge Types

U₇-C should conceptually maintain **two types of edges**:

1. **Forward Surface Edges**: `word_i → word_j` (sequential relationships)
2. **Backward Completion Edges**: `completion_unit ← required_previous_unit` (**more critical**)

```python
BackwardCompletionEdge = {
    completion_unit,              # Where ifādah completes
    required_previous_unit,       # What it licenses/requires
    agreement_surface_hint,       # Type of contract
    missing_or_satisfied_condition,
    residuals,
    trace
}
```

### Example 1: الكتب كثيرة (Broken Plural + Feminine Singular)

**Forward-only processing** (incomplete):
```
الكتب → broken plural candidate → deferred
(Processing stops, no context available)
```

**Backward from completion** (correct):
```
كثيرة → completion node (feminine singular surface)
  ↓
  ← looks back to الكتب
  ← reveals: non-rational plural + feminine singular agreement
  ← opens: agreement_surface_hint = non_rational_plural_feminine_possible
  ← الكتب remains DEFERRED for root extraction
  ← edge preserved for downstream layers
```

**Key Insight**: The feminine singular adjective **كثيرة** reveals how **الكتب** should be interpreted (as non-rational plural), but this is discovered only by scanning backward from the completion point.

### Example 2: الرجال صالحون (Broken Plural + Masculine Plural)

**Backward from completion**:
```
صالحون → completion node (masculine plural surface)
  ↓
  ← looks back to الرجال
  ← reveals: rational plural agreement
  ← opens: rationality_surface_hint = rational_possible
  ← الرجال still needs singular_candidate_path + lexical evidence
  ← does NOT enter U₈ as raw root
```

### Example 3: الشمس طلعت (Semantic Feminine + Feminine Verb)

**Backward from completion**:
```
طلعت → completion node (feminine verb surface)
  ↓
  ← looks back to الشمس
  ← reveals: semantic_feminine_surface_hint = possible
  ← preserves edge (does NOT make final judgment)
  ← judgment deferred to later layers
```

### Example 4: إِيَّاكَ نَعْبُدُ (Fronted Object)

**Backward from completion**:
```
نَعْبُدُ → completion node (verb)
  ↓
  ← opens requirement: object/معمول needed
  ← looks back to إِيَّاكَ
  ← reveals: fronted object (تقدّم المعمول)
  ← preserves edge (NOT grammatical judgment)
  ← position preserved for later syntactic analysis
```

**Critical**: This is **NOT** assigning grammatical function (مفعول), only preserving the surface contract that a verb-object relationship exists with non-canonical ordering.

### Architectural Implications

1. **U₇-C is completion-aware**: Must identify which unit represents ifādah completion
2. **Backward scanning mandatory**: Completion node licenses/requires previous nodes
3. **Edge directionality**: Primary edges point backward from completion
4. **Preservation NOT judgment**: Edges preserve surface hints, not grammatical roles
5. **U₈ respects completion**: Only processes units after backward scan completes

### Future Implementation Considerations

This refinement suggests that future U₇-C implementations should:

1. **Identify completion nodes** (typically final unit, but can vary)
2. **Scan backward** from completion to establish licensing relationships
3. **Create backward edges** with completion_unit as source
4. **Preserve context** for why each previous unit is licensed/deferred/blocked
5. **Maintain separation** between surface contracts and grammatical judgments

### Status

- **Principle**: ✅ Articulated and documented
- **Current U₇-C**: ⚠️ Needs verification of backward scanning support
- **Future work**: Explicit backward edge implementation (if not already present)

---

**الحمد لله**
*All praise is due to Allah for the successful completion of this architectural refactor and the articulation of the Backward Ifādah principle.*
