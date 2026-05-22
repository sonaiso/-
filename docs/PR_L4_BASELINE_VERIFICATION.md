# PR-L4 Baseline Verification

## الحكم النهائي (Final Verdict)

```text
المعمار: صحيح ✓
النطاق: صحيح ✓
القوانين: جيدة ✓
الحراسة: كاملة ✓
Test Helper Signatures: مصححة ✓ (PR-L4.1)
الحالة التنفيذية: CERTIFIED للانتقال للمرحلة التالية
```

---

## PR-L4 Scope (Baseline)

### What PR-L4 Does (Implemented)

**DalMadlulBindingCandidate** - First governed relation between Dāl and Madlūl-lafẓī:

1. **Creates governed binding candidate**
   - Between `DālCandidate` and `MadlulLafziCandidate`
   - Preserves trace_id from both sides
   - Preserves residuals from both sides
   - Records `binding_basis` (evidence for binding)

2. **Operates within governance layers**
   - Requires `RationalMethod`
   - Requires `NeutralBinding` (neutral element)
   - Requires `StyleSpec(LAFZI_DALALI)`
   - Requires `LafziMadlul` registration
   - Requires `PriorInformation`

3. **Enforces binding requirements** (7 hard gates)
   - No binding without DālCandidate
   - No binding without MadlulLafziCandidate
   - No binding without LafziMadlul registration
   - No binding without LAFZI_DALALI StyleSpec
   - No binding without NeutralBinding
   - No binding without PriorInformation
   - Returns governed failures, not bare exceptions

4. **Preserves trace lineage** (2 laws)
   - Preserves `dal_trace_id`
   - Preserves `madlul_trace_id`
   - Trace mismatch creates warning residual (not blocker)

5. **Guards against semantic drift** (9 negative laws)
   - Does NOT create external meaning
   - Does NOT create full Dalālah
   - Does NOT implement Wadh
   - Does NOT classify Mutabaqah/Tadammun/Iltizam
   - Does NOT classify Haqiqah/Majaz
   - Does NOT issue HUKM
   - Does NOT raise PredicateRank
   - Does NOT perform learning
   - Does NOT implement upward/downward transitions

---

### What PR-L4 Does NOT Do (Out of Scope)

**Explicitly NOT Implemented**:

1. **Wadh (الوضع)** - Convention establishment
   - `CONVENTIONAL_HINT` is hint only, NOT Wadh
   - Wadh requires explicit convention gate → PR-L5

2. **UsageGate (الاستعمال)** - Usage validation
   - `USAGE_HINT` is hint only, NOT usage gate
   - Usage validation → PR-L5

3. **Full Dalālah (الدلالة الكاملة)** - Complete signification
   - Binding is condition for possible Dalālah
   - Binding ≠ full signification
   - Full Dalālah → PR-L6+

4. **Semantic Classification** (التصنيف الدلالي)
   - No Mutabaqah (المطابقة) - conformity
   - No Tadammun (التضمن) - implication
   - No Iltizam (الالتزام) - entailment
   - Semantic classification → PR-L6+

5. **Literal/Metaphorical Classification** (الحقيقة والمجاز)
   - No Haqiqah (حقيقة) - literal meaning
   - No Majaz (مجاز) - metaphorical meaning
   - No Naql (نقل) - semantic transfer
   - Haqiqah/Majaz → PR-L7+

6. **Judgment Issuance** (إصدار الحكم)
   - No HUKM issuance
   - No rank elevation from binding
   - HUKM → Future (beyond PR-L7)

7. **Learning** (التعلم)
   - No learning from experience
   - No rank elevation through repetition
   - Learning → Future

---

## PR-L4 Hardening Summary (From PR #63)

### Six Hardening Guards Implemented

All 6 hardening guards from PR #63 implemented and passing:

#### H1: `test_binding_success_is_not_dalalah_success`
**Guards against**: Confusing binding success with semantic signification

**Verification**:
- ✓ Success = binding candidate ADMITTED
- ✓ Success ≠ Dalālah achieved
- ✓ Success ≠ semantic certification
- ✓ No semantic fields: `dalalah`, `wadh`, `meaning`, `hukm`, `haqiqah`, `majaz`, `mutabaqah`, `tadammun`, `iltizam`

#### H2: `test_prior_information_permits_binding_but_does_not_certify_dalalah`
**Guards against**: PriorInformation becoming semantic certification

**Verification**:
- ✓ PriorInformation permits binding attempt
- ✓ PriorInformation does NOT certify Dalālah
- ✓ No rank elevation from prior presence
- ✓ No semantic certification fields

#### H3: `test_conventional_hint_does_not_implement_wadh`
**Guards against**: `CONVENTIONAL_HINT` becoming full Wadh

**Verification**:
- ✓ `CONVENTIONAL_HINT` remains hint only
- ✓ No `wadh`, `convention`, `wadh_type` fields
- ✓ Wadh implementation reserved for PR-L5

#### H4: `test_usage_hint_does_not_implement_usage_gate`
**Guards against**: `USAGE_HINT` becoming usage validation gate

**Verification**:
- ✓ `USAGE_HINT` remains hint only
- ✓ No `usage_validated`, `usage_proof`, `usage_certification` fields
- ✓ UsageGate implementation reserved for PR-L5

#### H5: `test_lexical_hint_does_not_certify_binding`
**Guards against**: `LEXICAL_HINT` becoming lexical certification

**Verification**:
- ✓ `LEXICAL_HINT` remains hint only
- ✓ No `lexically_certified`, `lexical_proof`, `semantic_proof` fields
- ✓ Hint status preserved

#### H6: `test_binding_preserves_distinct_trace_lineages`
**Guards against**: Trace_id mismatch becoming blocker

**Verification**:
- ✓ Different trace_ids allowed (warning, not blocker)
- ✓ Both lineages preserved independently
- ✓ `TRACE_ID_MISMATCH` residual is warning severity

---

## PR-L4.1 Fixed Residuals

### Issue: Test Helper Signatures

**Problem Statement** (from PR #63):
```text
Test helper signatures (PriorInformation, StyleSpec) still need fixing (pre-existing issues)
```

### Root Cause Analysis

**PriorInformation Constructor Mismatch**:
- **Helper used**: `PriorInformation(content, source, strength)`
- **Actual constructor**: `PriorInformation(content, domain, rank, evidence_trace)`
- **Impact**: Tests would fail at runtime with `TypeError`

**FilteredPrior Initialization Error**:
- **Helper used**: `FilteredPrior(information=(prior_info,))`  # tuple
- **Actual constructor**: `FilteredPrior(information=frozenset([...]))`  # frozenset
- **Impact**: Type mismatch could cause downstream errors

### Fixes Applied (PR-L4.1)

#### Fix 1: Corrected `make_valid_neutral_binding_result()`

**Before** (incorrect):
```python
def make_valid_neutral_binding_result():
    prior_info = PriorInformation(
        content="test_prior",
        source="test",           # Wrong parameter name
        strength="strong",       # Wrong parameter name
    )
    filtered_prior = FilteredPrior(information=(prior_info,))  # Tuple instead of frozenset
    # ...
```

**After** (correct):
```python
def make_valid_neutral_binding_result():
    prior_info = PriorInformation(
        content="test_prior",
        domain="test_domain",           # Correct parameter
        rank="LICENSED",                # Correct parameter
        evidence_trace="test_evidence_trace",  # Required parameter
    )
    filtered_prior = FilteredPrior(
        information=frozenset([prior_info]),    # Frozenset
        excluded_opinions=frozenset()           # Required parameter
    )
    # ...
```

#### Fix 2: Verified `make_valid_style_spec()`

**Status**: ✓ Already correct
- Uses factory function: `make_lafzi_dalali_style()`
- Creates complete `StyleSpec` with all 5 required policies
- No changes needed

---

## PR-L4.1 New Guard Tests (5 Tests)

### Purpose

Prevent test helper signatures from drifting out of sync with implementation.

### Tests Added

#### S1: `test_prior_information_helper_matches_current_constructor`
**Guards against**: Stale PriorInformation helper parameters

**Verification**:
- ✓ Helper uses correct constructor parameters
- ✓ Creates valid `PriorInformation` with `domain`, `rank`, `evidence_trace`
- ✓ No legacy parameters (`source`, `strength`)

#### S2: `test_style_spec_helper_matches_current_constructor`
**Guards against**: Incomplete StyleSpec creation

**Verification**:
- ✓ All 5 required policies present
- ✓ Domain consistency across policies
- ✓ Domain is `LAFZI_DALALI`

#### S3: `test_lafzi_binding_helpers_do_not_bypass_governance`
**Guards against**: Helpers creating ungoverned objects

**Verification**:
- ✓ `make_valid_neutral_binding_result()` creates `NeutralBindingResult`
- ✓ `make_valid_style_spec()` creates `StyleSpec` with policies
- ✓ `make_valid_dal_candidate()` creates governed `DalCandidate`
- ✓ `make_valid_madlul_lafzi_candidate()` creates governed `MadlulLafziCandidate`

#### S4: `test_all_lafzi_binding_fixtures_create_governed_objects`
**Guards against**: Fixture bypassing governance chain

**Verification**:
- ✓ Full `DalMadlulBindingInput` created from helpers
- ✓ All components are governed
- ✓ Binding can proceed

#### S5: `test_binding_candidate_baseline_has_no_semantic_execution`
**Guards against**: Baseline implementing semantic capability

**Verification**:
- ✓ No semantic fields on candidate
- ✓ Gate guards confirm no semantic capability
- ✓ Baseline remains pre-semantic

---

## Test Coverage Summary

**Total**: 31 tests (100% pass rate required)

1. **Core Tests**: 20 tests
   - Binding requirements (7 tests)
   - Trace preservation (2 tests)
   - Residual preservation (1 test)
   - Negative laws (9 tests)
   - Governed failures (1 test)

2. **Hardening Guards** (PR #63): 6 tests
   - Semantic drift prevention (6 tests)

3. **Helper Signature Guards** (PR-L4.1): 5 tests
   - Constructor compliance (2 tests)
   - Governance compliance (3 tests)

---

## Verification Checklist

### ✓ Architecture Verification

- [x] `DalMadlulBindingCandidate` is first relation candidate
- [x] Operates inside `LAFZI_DALALI` domain
- [x] Requires all 4 governance layers
- [x] Preserves trace lineage from both sides
- [x] Returns governed failures, not exceptions

### ✓ Scope Verification

- [x] Binding ≠ Full Dalālah
- [x] Binding = Condition for possible Dalālah
- [x] No Wadh implementation
- [x] No UsageGate implementation
- [x] No semantic classification
- [x] No HUKM issuance
- [x] No learning implementation

### ✓ Hardening Verification (PR #63)

- [x] H1: Binding success ≠ Dalālah success
- [x] H2: PriorInformation permits, doesn't certify
- [x] H3: CONVENTIONAL_HINT ≠ Wadh
- [x] H4: USAGE_HINT ≠ UsageGate
- [x] H5: LEXICAL_HINT ≠ Certification
- [x] H6: Trace lineages preserved

### ✓ Helper Signature Verification (PR-L4.1)

- [x] S1: PriorInformation constructor correct
- [x] S2: StyleSpec factory correct
- [x] S3: Helpers create governed objects
- [x] S4: Fixtures create governed objects
- [x] S5: Baseline has no semantic execution

### ✓ Test Infrastructure

- [x] 31 tests implemented
- [x] All helpers match current constructors
- [x] No stale parameter names
- [x] No ungoverned object creation
- [x] Test count documented in docstring

---

## القانون الحاكم (Governing Law)

```text
الربط لا يساوي الدلالة.
والإشارة إلى الوضع لا تساوي الوضع.
ووجود prior لا يساوي شهادة دلالية.
ونجاح binding لا يساوي نجاح signification.
```

**English**:
```text
Binding ≠ Dalālah
Hint ≠ Wadh
Prior ≠ Certification
Binding success ≠ Signification success
```

---

## Transition Readiness

### PR-L4 is CERTIFIED for transition

**Reason**: All residuals closed

1. ✓ Architecture correct
2. ✓ Scope correct
3. ✓ Hardening complete (PR #63)
4. ✓ Helper signatures fixed (PR-L4.1)
5. ✓ Test coverage complete (31 tests)
6. ✓ All semantic guards in place

**Transition Rule**:
```text
لا وضع قبل ربط مستقر.
ولا دلالة قبل وضع أو استعمال.
ولا مرحلة جديدة فوق بقايا معلنة في المرحلة السابقة.

No Wadh before stable binding.
No Dalālah before Wadh or Usage.
No new phase over declared residuals.
```

**Next Phase**: PR-L5 - Wadh / Usage Gate

---

## PR-L5 Scope (Preview)

### What PR-L5 Will Add

**Limited scope** - Wadh and Usage evidence only:

1. **WadhEvidenceCandidate** (مرشح شاهد الوضع)
   - Evidence for conventional establishment
   - NOT full convention algebra
   - NOT Mutabaqah/Tadammun/Iltizam

2. **UsageEvidenceCandidate** (مرشح شاهد الاستعمال)
   - Evidence for usage patterns
   - NOT full usage certification
   - NOT learning or frequency analysis

3. **WadhUsageGate** (بوابة الوضع والاستعمال)
   - Validates Wadh/Usage evidence
   - Guards against premature semantic classification
   - Does NOT issue semantic judgments

### What PR-L5 Will NOT Add

**Explicitly forbidden**:

- ❌ Mutabaqah classification
- ❌ Tadammun classification
- ❌ Iltizam classification
- ❌ Haqiqah/Majaz classification
- ❌ HUKM issuance
- ❌ Learning implementation
- ❌ Rank elevation from usage frequency

**Law for PR-L5**:
```text
لا دلالة مرخصة بلا وضع أو استعمال محفوظ.
No licensed signification without preserved Wadh or Usage.
```

---

## Document History

- **2026-05-22**: Created (PR-L4.1)
- **Version**: 1.0
- **Status**: CERTIFIED
- **Next Review**: Before PR-L5

---

## Conclusion

**PR-L4 Baseline: CERTIFIED**

All residuals from PR #63 are now closed:
- ✓ Test helper signatures corrected
- ✓ 5 new guard tests added
- ✓ 31 total tests (20 core + 6 hardening + 5 signature)
- ✓ Architecture verified
- ✓ Scope verified
- ✓ Semantic guards in place

**Ready for PR-L5**: Wadh / Usage Gate
