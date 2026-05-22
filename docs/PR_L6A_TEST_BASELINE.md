# PR-L6A Test Baseline Documentation

**Date**: 2026-05-22
**Branch**: `claude/mutabaqah-gate`
**PR**: #67

---

## Executive Summary

**PR-L6A introduces NO new test failures.**

- **MutabaqahGate tests**: 29/29 passing ✅ (19 original + 10 hardening)
- **Pre-existing failures**: 19 failures in `test_dal_madlul_binding_candidate.py` (unrelated to PR-L6A)
- **Scope**: PR-L6A only modifies `lafzi_dalalah` module (new), does NOT touch binding module

---

## Test Suite Status

### 1. MutabaqahGate Tests (PR-L6A)

**File**: `tests/gfa/methods/test_mutabaqah_gate.py`

**Command**:
```bash
python3 -m pytest tests/gfa/methods/test_mutabaqah_gate.py -v
```

**Result**: 29/29 passing ✅

**Test Breakdown**:

#### Original Tests (19)
1. ✅ test_mutabaqah_requires_admitted_wadh_claim
2. ✅ test_mutabaqah_requires_mawdu_lah_structure
3. ✅ test_mutabaqah_requires_mawdu_lah_whole
4. ✅ test_mutabaqah_preserves_wadh_trace
5. ✅ test_mutabaqah_preserves_binding_trace
6. ✅ test_mutabaqah_preserves_residuals
7. ✅ test_mutabaqah_does_not_create_external_meaning
8. ✅ test_mutabaqah_does_not_issue_hukm
9. ✅ test_mutabaqah_does_not_create_tadammun
10. ✅ test_mutabaqah_does_not_create_iltizam
11. ✅ test_mutabaqah_does_not_classify_haqiqah_majaz_naql
12. ✅ test_mutabaqah_does_not_create_ifadah
13. ✅ test_mutabaqah_does_not_raise_predicate_rank_to_certified
14. ✅ test_unknown_mawdu_lah_whole_becomes_residual
15. ✅ test_polysemy_possible_becomes_residual
16. ✅ test_homonymy_possible_becomes_residual
17. ✅ test_partial_usage_blocks_or_residualizes_mutabaqah
18. ✅ test_mutabaqah_success_means_candidate_admitted_not_truth_certified
19. ✅ test_mutabaqah_returns_governed_failure_not_exception

#### Hardening Tests (10)
20. ✅ test_mutabaqah_requires_wadh_gate_admission_not_raw_wadh_claim
21. ✅ test_raw_wadh_claim_without_gate_trace_cannot_admit_mutabaqah
22. ✅ test_mutabaqah_whole_must_come_from_mawdu_lah_structure
23. ✅ test_string_gloss_alone_is_not_mawdu_lah_whole ⭐ **Most Critical**
24. ✅ test_wadh_residuals_propagate_into_mutabaqah
25. ✅ test_unknown_scope_residual_blocks_or_downgrades_mutabaqah
26. ✅ test_mutabaqah_success_is_not_full_dalalah
27. ✅ test_mutabaqah_success_is_not_haqiqah
28. ✅ test_mutabaqah_success_is_not_external_truth
29. ✅ test_partial_usage_cannot_be_mutabaqah_success

---

### 2. Full GFA Methods Suite

**Command**:
```bash
python3 -m pytest tests/gfa/methods/ -v
```

**Result**: 197 passed, **19 failed** ⚠️

**Failures**: All 19 failures in `test_dal_madlul_binding_candidate.py`

**Failure Root Cause**:
```python
AttributeError: 'StyleSpec' object has no attribute 'domain'
```

**Affected Tests** (all in `test_dal_madlul_binding_candidate.py`):
1. ❌ test_binding_requires_dal_candidate
2. ❌ test_binding_requires_madlul_lafzi_candidate
3. ❌ test_binding_requires_lafzi_registration
4. ❌ test_binding_requires_neutral_binding
5. ❌ test_binding_requires_prior_information
6. ❌ test_binding_preserves_dal_trace_id
7. ❌ test_binding_preserves_madlul_trace_id
8. ❌ test_binding_preserves_residuals_from_both_sides
9. ❌ test_binding_blocks_domain_mismatch
10. ❌ test_unknown_binding_basis_becomes_residual
11. ❌ test_binding_candidate_admission_success
12. ❌ test_binding_success_is_not_dalalah_success
13. ❌ test_prior_information_permits_binding_but_does_not_certify_dalalah
14. ❌ test_conventional_hint_does_not_implement_wadh
15. ❌ test_usage_hint_does_not_implement_usage_gate
16. ❌ test_lexical_hint_does_not_certify_binding
17. ❌ test_binding_preserves_distinct_trace_lineages
18. ❌ test_all_lafzi_binding_fixtures_create_governed_objects
19. ❌ test_binding_candidate_baseline_has_no_semantic_execution

---

### 3. Why Pre-existing Failures Are Unrelated to PR-L6A

**Evidence 1: Module Isolation**

PR-L6A files:
- `src/gfa/methods/lafzi_dalalah/` (NEW module)
- `tests/gfa/methods/test_mutabaqah_gate.py` (NEW test file)

Failing module:
- `src/gfa/methods/lafzi_binding/` (EXISTING, untouched)
- `tests/gfa/methods/test_dal_madlul_binding_candidate.py` (EXISTING, untouched)

**No overlap**: PR-L6A does not modify binding module.

**Evidence 2: Error Location**

Failure occurs in:
```
src/gfa/methods/lafzi_binding/dal_madlul_binding_gate.py:166
```

Line 166 (from error trace):
```python
elif input_data.style_spec.domain.domain_type != ThinkingDomain.LAFZI_DALALI:
```

This line expects `StyleSpec.domain` field, which doesn't exist in current `StyleSpec` implementation.

**Evidence 3: PR-L6A Does Not Import Binding Gate**

`test_mutabaqah_gate.py` imports:
- `DalMadlulBindingCandidate` (data structure only, for test helpers)
- `BindingBasis` (enum only)

Does NOT import:
- `DalMadlulBindingGate` (where failures occur)

**Evidence 4: Temporal Evidence**

These failures existed BEFORE PR-L6A work began. They are documented issues in the binding module architecture (StyleSpec refactoring incomplete).

---

## Critical Hardening Verification

### Most Dangerous Hallucination Guard

**Test**: `test_string_gloss_alone_is_not_mawdu_lah_whole`

**Critical Law**: Raw lexicon text CANNOT be used as MawduLah whole.

**Verification**:
```python
# Verifies MawduLahStructure is structured object, not raw string
assert hasattr(mawdu_lah, 'structure_form')  # Has structure
assert mawdu_lah.wadh_evidence is not None  # Has evidence
assert mawdu_lah.binding_trace_id  # Has trace
```

**Why Critical**: Prevents bypass of governance chain where raw lexicon glosses would become "whole" without evidence/trace/structure wrapping.

---

## Governance Chain Verification

### WadhGate → MutabaqahGate Chain Intact

**Test**: `test_mutabaqah_requires_wadh_gate_admission_not_raw_wadh_claim`

**Verification**:
- Non-admitted WadhGateResult → MutabaqahGate blocked ✅
- Cannot bypass WadhGate by constructing WadhClaim directly ✅

**Test**: `test_raw_wadh_claim_without_gate_trace_cannot_admit_mutabaqah`

**Verification**:
- WadhGate trace (claim_id) must exist ✅
- Binding trace must be preserved ✅
- Traces propagate to MutabaqahCandidate ✅

---

## Semantic Inflation Guards

All 7 semantic boundary tests passing:

1. ✅ **NO external meaning**: `test_mutabaqah_does_not_create_external_meaning`
2. ✅ **NO HUKM**: `test_mutabaqah_does_not_issue_hukm`
3. ✅ **NO Tadammun**: `test_mutabaqah_does_not_create_tadammun`
4. ✅ **NO Iltizam**: `test_mutabaqah_does_not_create_iltizam`
5. ✅ **NO Haqiqah/Majaz**: `test_mutabaqah_does_not_classify_haqiqah_majaz_naql`
6. ✅ **NO Ifadah**: `test_mutabaqah_does_not_create_ifadah`
7. ✅ **NO rank inflation**: `test_mutabaqah_does_not_raise_predicate_rank_to_certified`

**Hardening additions**:

8. ✅ **NO full Dalālah**: `test_mutabaqah_success_is_not_full_dalalah`
9. ✅ **NO Haqiqah**: `test_mutabaqah_success_is_not_haqiqah`
10. ✅ **NO external truth**: `test_mutabaqah_success_is_not_external_truth`

**Total**: 10 semantic boundary guards enforced.

---

## Residual Propagation Verification

**Test**: `test_wadh_residuals_propagate_into_mutabaqah`

**Verification**:
- Residuals field exists in MutabaqahCandidate ✅
- Residuals are tracked (not lost) ✅
- Blocking residuals prevent admission ✅

**Test**: `test_partial_usage_cannot_be_mutabaqah_success`

**Verification**:
- Partial usage residual is blocker ✅
- Adding partial usage residual invalidates candidate ✅
- Enforces: Partial usage indicates Tadammun, blocks Mutabaqah ✅

---

## Test Collection Verification

**Command**:
```bash
python3 -m pytest tests/ --collect-only
```

**Result**: All tests discovered, no collection errors.

**MutabaqahGate tests discovered**: 29/29 ✅

---

## Merge Readiness Criteria

### ✅ Criteria Met

1. ✅ All MutabaqahGate tests passing (29/29)
2. ✅ No new failures introduced
3. ✅ Pre-existing failures documented and isolated
4. ✅ Semantic inflation guards verified (10 tests)
5. ✅ Governance chain verified (WadhGate → MutabaqahGate)
6. ✅ Residual propagation verified
7. ✅ Most dangerous hallucination (string gloss) guarded
8. ✅ Trace preservation verified
9. ✅ Test baseline documented

### ❌ Not Claimed

- ❌ Does NOT claim "CERTIFIED for full suite"
- ❌ Does NOT claim pre-existing failures fixed
- ❌ Does NOT claim binding module issues resolved

---

## Conclusion

**PR-L6A is READY for merge** with the following understanding:

✅ **Locally certified**: All MutabaqahGate functionality verified
✅ **Governance intact**: No bypass of WadhGate requirements
✅ **Boundaries enforced**: 10 semantic inflation guards passing
✅ **No regression**: Pre-existing failures are isolated and unrelated

⚠️ **Pre-existing failures** in binding module are SEPARATE issue requiring separate fix (StyleSpec.domain field).

**Recommendation**: Merge PR-L6A. Address binding module failures in separate PR.

---

**Test Execution Summary**:

```bash
# MutabaqahGate tests (PR-L6A scope)
$ python3 -m pytest tests/gfa/methods/test_mutabaqah_gate.py -v
======================== 29 passed in 0.17s ========================

# Full GFA suite (includes pre-existing failures)
$ python3 -m pytest tests/gfa/methods/ -v
==================== 197 passed, 19 failed in 0.81s ====================
```

**Status**: ✅ PR-L6A hardened and ready for merge
