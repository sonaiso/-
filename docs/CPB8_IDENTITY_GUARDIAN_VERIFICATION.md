# CPB₈ Identity Guardian Verification Report

**Date**: 2026-05-26
**PR**: U₈ Identity Preservation Hardening
**Status**: ✅ **VERIFIED**

---

## Executive Summary

U₈ RootStemCandidateCarrier has been **architecturally verified** to preserve U₇-C ClauseSurfaceAgreement identity without silent loss. All 8 critical identity preservation tests **PASS**.

---

## CPB₈ Identity Guardian Law

```
Every layer must either:
1. Preserve the identity received from the previous layer, OR
2. Explicitly emit residuals explaining what could not be preserved

NO SILENT IDENTITY LOSS
```

**Arabic Formulation**:
```
CPB₈ = حارس هوية مادة الجذر المرخّصة

لا يسمح بأكل العلامة داخل الجذر
لا يسمح بأكل الحافة داخل الجذر
لا يسمح بأكل الوظيفة داخل الوزن
لا يسمح بضياع البقايا
```

---

## Verification Results

### ✅ Test 1: Agreement Edge Preservation

**Case**: الكتب كثيرة (broken plural + feminine agreement)

**U₇-C Output**:
- `agreement_edges = ("edge_123",)`
- `rationality_surface_hint = NON_RATIONAL_POSSIBLE`
- `root_input_permission = DEFERRED`

**U₈ Behavior**:
```python
u8_unit.agreement_edge_ids == ("edge_123",)  # ✅ PRESERVED
u8_unit.root_status == DEFERRED              # ✅ NO EXTRACTION
u8_unit.root_candidate_paths == ()           # ✅ EMPTY (deferred)
```

**Verdict**: ✅ PASS - U₈ preserves agreement edge without interpreting rationality

---

### ✅ Test 2: Broken Plural Guard Preservation

**Case**: الرجال (broken plural with multi-dimensional guard)

**U₇-C Output**:
- `broken_plural_guard = BrokenPluralGuardNode(uid="bpg_456", ...)`
- `singular_candidate_path = "رجل"`
- `rationality_surface_hint = RATIONAL_POSSIBLE`
- `root_input_permission = DEFERRED`

**U₈ Behavior**:
```python
u8_unit.broken_plural_guard_id == "bpg_456"  # ✅ PRESERVED
u8_unit.root_status == DEFERRED              # ✅ NO EXTRACTION
```

**Verdict**: ✅ PASS - U₈ preserves broken plural guard as trace

---

### ✅ Test 3: Permission Elevation Preservation

**Case**: Permission elevated by U₇-C based on agreement evidence

**U₇-C Output**:
- `permission_elevated_by_agreement = True`
- `permission_elevation_evidence = "agreement_with_definite_noun"`

**U₈ Behavior**:
```python
u8_unit.permission_elevated_by_agreement == True  # ✅ PRESERVED
```

**Verdict**: ✅ PASS - U₈ preserves permission elevation fact

---

### ✅ Test 4: Root Input Extraction (Not Surface)

**Case**: كَتَبَ

**U₇-C Output**:
- `surface = "كَتَبَ"` (with diacritics)
- `protected_core = "كتب"`
- `root_input = "كتب"` (licensed for extraction)
- `root_input_permission = ALLOWED`

**U₈ Behavior**:
```python
# Extraction happens from root_input="كتب" ONLY
u8_unit.root_candidate_paths[0].radicals == ("ك", "ت", "ب")  # ✅ FROM root_input
u8_unit.surface == "كَتَبَ"                                  # ✅ PRESERVED (not used)
```

**Verdict**: ✅ PASS - U₈ extracts from root_input only

---

### ✅ Test 5: DEFERRED Enforcement

**Case**: كتاب with DEFERRED permission

**U₇-C Output**:
- `root_input = "كتاب"`
- `root_input_permission = DEFERRED`

**U₈ Behavior**:
```python
u8_unit.root_status == DEFERRED           # ✅ BLOCKED
u8_unit.root_candidate_paths == ()        # ✅ NO EXTRACTION
```

**Verdict**: ✅ PASS - DEFERRED prevents extraction even if root_input present

---

### ✅ Test 6: BLOCKED Enforcement

**Case**: وَ (closed-class particle)

**U₇-C Output**:
- `root_input = ""`
- `root_input_permission = BLOCKED`

**U₈ Behavior**:
```python
u8_unit.root_status == BLOCKED           # ✅ BLOCKED
u8_unit.root_candidate_paths == ()       # ✅ NO EXTRACTION
```

**Verdict**: ✅ PASS - BLOCKED prevents extraction

---

### ✅ Test 7: U₇-C Trace Preservation

**Case**: Trace chain validation

**U₇-C Output**:
- `source_u7b_unit_id = "u7b_trace"`
- `source_u7b_trace = ("u6_t", "u5_t", ..., "u0_t")`

**U₈ Behavior**:
```python
u8_unit.source_u7c_unit_id == "u7c_trace_test"               # ✅ PRESERVED
u8_unit.source_u7c_trace contains "u7b_trace"                # ✅ PRESERVED
layer.source_clause_surface_layer_id == "u7c_layer_trace"   # ✅ PRESERVED
```

**Verdict**: ✅ PASS - Complete trace chain preserved

---

### ✅ Test 8: No Silent Identity Loss

**Case**: DEFERRED case must emit residual

**U₇-C Output**:
- `root_input_permission = DEFERRED`
- `agreement_edges = ("edge_res",)`

**U₈ Behavior**:
```python
len(result.residuals) > 0                    # ✅ HAS RESIDUALS
any("deferred" in r.message.lower() ...)     # ✅ EXPLAINS WHY
```

**Verdict**: ✅ PASS - Identity loss explicitly documented in residuals

---

## Forbidden Field Verification

### ❌ Fields That MUST NOT Exist in U₈

**Tested via structure inspection**:
```python
field_names = {f.name for f in fields(RootStemCandidateUnit)}

# FORBIDDEN (grammar/semantics)
assert 'weight' not in field_names          # ✅ ABSENT
assert 'pattern' not in field_names         # ✅ ABSENT
assert 'meaning' not in field_names         # ✅ ABSENT
assert 'hukm' not in field_names            # ✅ ABSENT

# FORBIDDEN (syntactic functions)
assert 'fa3il' not in field_names           # ✅ ABSENT
assert 'maf3ul' not in field_names          # ✅ ABSENT
assert 'mubtada' not in field_names         # ✅ ABSENT
assert 'khabar' not in field_names          # ✅ ABSENT

# FORBIDDEN (certificates)
assert 'root_certificate' not in field_names    # ✅ ABSENT
assert 'stem_certificate' not in field_names    # ✅ ABSENT
```

**Verdict**: ✅ PASS - All forbidden fields absent

---

## Required Field Verification

### ✅ Fields That MUST Exist in U₈

**U₇-C Identity Preservation Fields**:
```python
# U₇-C trace fields
assert 'source_u7c_unit_id' in field_names      # ✅ PRESENT
assert 'source_u7c_trace' in field_names        # ✅ PRESENT

# Agreement preservation fields
assert 'agreement_edge_ids' in field_names      # ✅ PRESENT
assert 'broken_plural_guard_id' in field_names  # ✅ PRESENT
assert 'permission_elevated_by_agreement' in field_names  # ✅ PRESENT

# Extraction source fields
assert 'root_input' in field_names              # ✅ PRESENT
assert 'protected_core' in field_names          # ✅ PRESENT
assert 'surface' in field_names                 # ✅ PRESENT
```

**Verdict**: ✅ PASS - All required fields present

---

## Architectural Compliance Summary

| Law | Status | Evidence |
|-----|--------|----------|
| U₈ consumes U₇-C ONLY (not U₇-B) | ✅ VERIFIED | Function signature accepts ClauseSurfaceAgreementLayerObject |
| U₈ preserves agreement_edge_ids | ✅ VERIFIED | Test 1 passes |
| U₈ preserves broken_plural_guard_id | ✅ VERIFIED | Test 2 passes |
| U₈ preserves permission_elevated_by_agreement | ✅ VERIFIED | Test 3 passes |
| U₈ extracts from root_input ONLY | ✅ VERIFIED | Test 4 passes |
| DEFERRED prevents extraction | ✅ VERIFIED | Test 5 passes |
| BLOCKED prevents extraction | ✅ VERIFIED | Test 6 passes |
| U₈ preserves U₇-C trace | ✅ VERIFIED | Test 7 passes |
| No silent identity loss | ✅ VERIFIED | Test 8 passes |
| No forbidden fields | ✅ VERIFIED | Structure inspection passes |

---

## Conclusion

**U₈ is IDENTITY-CLOSED over U₇-C ClauseSurfaceAgreement ✅**

The transition U₇-B → U₇-C → U₈ is architecturally sound:

```
U₇-B: Protects word-level markers
  ↓
U₇-C: Protects clause-level agreement contracts
  ↓
U₈:   Preserves all U₇-C identity without interpretation
      Opens root/stem candidate paths ONLY from licensed root_input
      DEFERRED/BLOCKED enforcement prevents unauthorized extraction
      Agreement edges preserved as trace (not consumed)
      Broken plural guards preserved as trace (not interpreted)
```

**No weight before the root preserves the agreement edge.**

---

## Next Steps

U₈ is now proven closed over U₇-C identity guards. The architecture is ready for:

1. ✅ U₉ WeightCandidateCarrier can begin (U₈ foundation verified)
2. Integration tests for full U₀→U₇-C→U₈ pipeline
3. Golden case tests (الكتب كثيرة, الرجال صالحون, إِيَّاكَ نَعْبُدُ)
4. Performance benchmarking

**Signed**: CPB₈ Identity Guardian
**Date**: 2026-05-26
**Verification**: COMPLETE ✅
