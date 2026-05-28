# Relation Anchor Extraction Constitution

**دستور استخراج مرساة النسبة**

## Constitutional Position (الموقع الدستوري)

This module closes the critical gap in RelationAlgebraCore:

**The Gap:**
```
RelationResult.preserved_identities: FrozenSet[IdentityType]  ❌ TYPE-LEVEL ONLY
```

**The Problem:**
```
زيد قائم
- Entity: زيد (FORM_IDENTITY)
- Transformation: قائم (FORM_IDENTITY)

Result = {FORM_IDENTITY}  ❌ Cannot distinguish which is entity, which is transformation
```

**The Solution:**
```
AnchoredMufradInput preserves INSTANCE identity:
- anchor_instance_id = "rel_123_anchor_0"
- source_vector_id = "mufrad_زيد_456"
- anchor = EntityAnchor(FORM_IDENTITY, ...)

RelationResultWithInstanceTrace enables downward_audit():
→ anchor_instances: ["anchor_0", "anchor_1"]
→ source_vectors: ["mufrad_زيد", "mufrad_قائم"]
✅ Full distinction preserved
```

---

## Purpose (الغرض)

Close the algebraic gap by adding instance-level identity preservation:

```
PreSyntaxMufradVector
  → AnchoredMufradInput (instance-preserving wrapper)
    → RelationOperation.apply()
      → RelationResultWithInstanceTrace (instance-preserving wrapper)
        → downward_audit() ✅
```

---

## Critical Design Decisions (القرارات المعمارية)

### Decision 1: Wrapper Pattern (Not Direct Modification)

**Decision:**
Use `AnchoredMufradInput` as WRAPPER around `Anchor`, not modify `Anchor` directly.

**Rationale:**
- ✅ Safe: Does not break existing `RelationAlgebraCore` tests
- ✅ Reversible: Can be removed if needed
- ✅ Clear separation: Instance tracking vs type definition

**Rejected Alternative:**
Adding `anchor_id`, `source_vector_id` fields directly to `EntityAnchor`/`TransformationAnchor`.

**Risk:**
Would require modifying all Anchor constructors, breaking existing code.

---

### Decision 2: External Adapter (Not Internal apply())

**Decision:**
Use external function `extract_anchored_inputs_from_slot_vector()`, NOT add `apply_via_relation_algebra()` method to `RelationSlotVector`.

**Rationale:**
- ✅ Preserves separation: RelationSlotVector = readiness, not execution
- ✅ Constitutional compliance: No execution logic in slot layer
- ✅ Clear boundary: Adapter function is explicit bridge point

**Rejected Alternative:**
```python
class RelationSlotVector:
    def apply_via_relation_algebra(self):  # ❌ REJECTED
        # Would mix readiness with execution
```

**Risk:**
Would transform RelationSlotVector from preparation layer to execution layer.

---

### Decision 3: Stub _extract_anchor (Not Full Implementation)

**Decision:**
Create `_extract_anchor_from_presyntax()` as documented stub raising `NotImplementedError`.

**Rationale:**
- ✅ Documents interface contract
- ✅ Allows testing of surrounding infrastructure
- ✅ Prevents premature implementation without full requirements
- ✅ Clear TODO for future work

**Full Implementation Requires:**
1. Mapping `ishtiqaq_judgment` → Anchor type
2. Mapping `binaa_judgment` → Anchor type
3. Mapping `type_id` → Anchor type
4. Full decision tree for all PreSyntaxMufradVector combinations

**Current State:**
Stub exists. Full implementation is NEXT STEP after design validation.

---

### Decision 4: Reference Links Placeholder

**Decision:**
Add `reference_links: Tuple[str, ...] = ()` field with empty default.

**Rationale:**
- ✅ Reserves architectural space
- ✅ Documents future requirement
- ✅ Does not implement prematurely
- ✅ Fails safely (empty tuple)

**NOT IMPLEMENTED:**
- `ReferenceLink` dataclass
- Pronoun reference tracking
- Demonstrative reference tracking
- Relative reference tracking
- Forward/backward reference tracking

**Future Work:**
When reference algebra is needed, the field exists and is ready.

---

## Constitutional Laws (القوانين الدستورية)

### Law 1: لا تعديل مباشر على Anchor
**No direct modification to existing Anchor classes**

Anchor classes (`EntityAnchor`, `TransformationAnchor`, `FunctionAnchor`) MUST NOT be modified.

Instance tracking achieved via wrapper pattern.

---

### Law 2: لا execution داخل RelationSlotVector
**No execution logic inside RelationSlotVector**

`RelationSlotVector` is readiness/preparation layer ONLY.

Execution via external adapter function.

---

### Law 3: حفظ هوية النسخة لا النوع فقط
**Preserve instance identity not just type identity**

Every `AnchoredMufradInput` MUST have:
- `anchor_instance_id`: Unique instance identifier
- `source_vector_id`: Source PreSyntaxMufradVector ID
- `source_trace_id`: Full trace ID

---

### Law 4: كل علاقة يجب أن تُدقَّق رجوعياً
**Every relation must support downward audit**

`RelationResultWithInstanceTrace.downward_audit()` MUST return complete trail:
- Which anchor instances entered
- Which source vectors produced them
- Which operation was applied
- What was preserved/added

---

### Law 5: لا meaning/ifadah/hukm
**No meaning/ifadah/hukm production**

Both `AnchoredMufradInput` and `RelationResultWithInstanceTrace` MUST NOT contain:
- `meaning`
- `ifadah`
- `hukm`
- `murad`
- `semantic`

Validation in `__post_init__` enforces this.

---

## What This Closes (ما يُغلَق)

### ✅ Type-Level vs Instance-Level Gap

**Before:**
```python
RelationResult.preserved_identities = {FORM_IDENTITY}
# ❌ If both inputs are FORM_IDENTITY, cannot distinguish which is which
```

**After:**
```python
result.downward_audit() = {
    'anchor_instances': ['anchor_entity_001', 'anchor_transformation_002'],
    'source_vectors': ['mufrad_زيد_123', 'mufrad_قائم_456'],
    ...
}
# ✅ Full distinction: which input was entity, which was transformation
```

---

### ✅ Downward Audit Gap

**Before:**
No mechanism to trace from relation result back to source mufrad vectors.

**After:**
```python
result = RelationResultWithInstanceTrace(...)
audit = result.downward_audit()
# ✅ Complete trail: operation → anchors → vectors
```

---

### ✅ Instance Preservation Gap

**Before:**
`OperatorCandidate` has `trigger_source_vector_id`, but Anchors don't.

**After:**
`AnchoredMufradInput.source_vector_id` brings same rigor to relations.

---

## What This Does NOT Close (ما لا يُغلَق بعد)

### ❌ Full Anchor Extraction

`_extract_anchor_from_presyntax()` is STUB.

Requires full implementation mapping PreSyntaxMufradVector → Anchor.

---

### ❌ Reference Tracking

`reference_links` field exists but is always empty tuple.

Requires:
- `ReferenceLink` dataclass
- Pronoun resolution
- Demonstrative resolution
- Relative clause tracking
- Forward/backward reference

---

### ❌ Operation Licensing

No `OperationLicense` or `RelationOperationProof` yet.

Currently, any RelationSlotVector can convert to anchored inputs.

Future: May need licensing layer proving WHY relation is permitted.

---

### ❌ Upward Potential

`downward_audit()` works.

`upward_potential()` (what can be built above) not yet implemented.

---

## Testing Requirements (متطلبات الاختبار)

### Constitutional Tests (must pass):

1. ✅ `test_anchored_mufrad_input_preserves_source_identity()`
2. ✅ `test_relation_result_downward_audit()`
3. ✅ `test_relation_result_prevents_instance_loss()`
4. ✅ `test_no_direct_anchor_modification()`
5. ✅ `test_wrapper_count_matches_input_count()`

### Integration Tests (will fail until _extract_anchor implemented):

1. ❌ `test_extract_anchored_inputs_requires_implementation()` (expected to fail)

---

## Usage Example (مثال الاستخدام)

```python
from dal_core.relation_slot_readiness import RelationSlotVector
from dal_core.relation_anchor_extraction import (
    extract_anchored_inputs_from_slot_vector,
    RelationResultWithInstanceTrace,
)
from dal_core.relation_algebra_core import IsnadOperation

# 1. Prepare slot vector (from RelationSlotReadiness)
slot_vector = RelationSlotVector(...)  # Prepared from PreSyntaxMufradVector

# 2. Extract anchored inputs (THIS MODULE)
anchored_inputs = extract_anchored_inputs_from_slot_vector(slot_vector)

# 3. Apply relation operation
operation = IsnadOperation()
anchors = tuple(ai.anchor for ai in anchored_inputs)
base_result = operation.apply(anchors)

# 4. Wrap with instance trace
result_with_trace = RelationResultWithInstanceTrace(
    base_result=base_result,
    input_anchor_instance_ids=tuple(ai.anchor_instance_id for ai in anchored_inputs),
    input_source_vector_ids=tuple(ai.source_vector_id for ai in anchored_inputs),
    input_source_trace_ids=tuple(ai.source_trace_id for ai in anchored_inputs),
    operation_trace_id="operation_unique_id",
    relation_type=RelationType.ISNAD,
)

# 5. Perform downward audit
audit = result_with_trace.downward_audit()
print(audit['anchor_instances'])  # → ["anchor_0", "anchor_1"]
print(audit['source_vectors'])    # → ["mufrad_زيد", "mufrad_قائم"]
```

---

## Next Steps (الخطوات التالية)

### Immediate (مباشر):

1. ✅ Run constitutional tests: `pytest tests/dal_core/test_relation_anchor_extraction.py -v`
2. ✅ Verify all tests pass except integration test (expected)
3. ✅ Store memory of this implementation

### Short-term (قريب):

1. Implement `_extract_anchor_from_presyntax()` full logic
2. Map PreSyntaxMufradVector features → Anchor types
3. Update integration test to verify full flow

### Medium-term (متوسط):

1. Add `ReferenceLink` dataclass
2. Implement reference tracking
3. Populate `reference_links` field

### Long-term (بعيد):

1. Add operation licensing layer
2. Implement upward potential mapping
3. Full RelationAlgebraCore integration with U₁₁

---

## Evidence This Closes The Gap (الدليل على سد الفجوة)

### Gap Identified (from problem statement):

> الفجوة الجبرية الحقيقية:
>
> حفظ FORM_IDENTITY لا يكفي إذا دخل طرفان كلاهما FORM_IDENTITY.
>
> زيد قائم → {FORM_IDENTITY} → لا يكفي للرجوع إلى: زيد كطرف كيان، قائم كطرف صفة

### Solution Implemented:

```python
result = RelationResultWithInstanceTrace(
    input_anchor_instance_ids=("anchor_entity_001", "anchor_transformation_002"),
    input_source_vector_ids=("mufrad_زيد_123", "mufrad_قائم_456"),
    ...
)

audit = result.downward_audit()
# ✅ audit['anchor_instances'][0] = "anchor_entity_001" (زيد)
# ✅ audit['anchor_instances'][1] = "anchor_transformation_002" (قائم)
# ✅ Full distinction even with same type identity
```

### Test Proving Gap Closed:

`test_relation_result_prevents_instance_loss()`:
```python
# Both have FORM_IDENTITY type
assert IdentityType.FORM_IDENTITY in result.base_result.preserved_identities

# But instance-level distinction preserved
audit = result.downward_audit()
assert len(set(audit['anchor_instances'])) == 2  # ✅ Distinct instances
assert len(set(audit['source_vectors'])) == 2  # ✅ Distinct sources
```

---

## Constitutional Compliance Checklist

- [x] لا تعديل مباشر على Anchor classes (wrapper pattern used)
- [x] لا execution داخل RelationSlotVector (external adapter used)
- [x] حفظ هوية النسخة (anchor_instance_id + source_vector_id)
- [x] تدقيق رجوعي (downward_audit() implemented)
- [x] منع meaning/ifadah/hukm (validation in __post_init__)
- [x] Immutability (frozen=True dataclasses)
- [x] Constitutional tests written and passing
- [ ] Full _extract_anchor implementation (documented stub - next step)
- [ ] Reference tracking (placeholder exists - future work)

---

**Status:** ✅ Constitutional foundation complete. Implementation stub documented. Ready for next phase.

**Date:** 2026-05-28

**Verified by:** Evidence-based implementation following strict constitutional requirements.
