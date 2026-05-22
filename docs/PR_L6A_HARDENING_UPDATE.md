# PR #67 Hardening Update

**Date**: 2026-05-22
**Status**: ✅ HARDENED AND READY FOR MERGE

---

## Hardening Completed

Added **10 additional guard tests** to strengthen PR-L6A against semantic drift.

**Total Tests**: 29/29 passing ✅ (19 original + 10 hardening)

---

## Hardening Tests Added

1. ✅ `test_mutabaqah_requires_wadh_gate_admission_not_raw_wadh_claim`
2. ✅ `test_raw_wadh_claim_without_gate_trace_cannot_admit_mutabaqah`
3. ✅ `test_mutabaqah_whole_must_come_from_mawdu_lah_structure`
4. ✅ `test_string_gloss_alone_is_not_mawdu_lah_whole` ⭐ **Most Critical**
5. ✅ `test_wadh_residuals_propagate_into_mutabaqah`
6. ✅ `test_unknown_scope_residual_blocks_or_downgrades_mutabaqah`
7. ✅ `test_mutabaqah_success_is_not_full_dalalah`
8. ✅ `test_mutabaqah_success_is_not_haqiqah`
9. ✅ `test_mutabaqah_success_is_not_external_truth`
10. ✅ `test_partial_usage_cannot_be_mutabaqah_success`

---

## Most Critical Guard

**Test**: `test_string_gloss_alone_is_not_mawdu_lah_whole`

**Critical Law**: Raw lexicon text CANNOT be used as MawduLah whole.

**What it prevents**:
- Most dangerous hallucination: treating raw lexicon glosses as "whole"
- Bypass of governance chain
- Loss of evidence/trace/structure requirements

**Verification**:
```python
# Verifies MawduLahStructure is structured object, not raw string
assert hasattr(mawdu_lah, 'structure_form')  # Has structure
assert mawdu_lah.wadh_evidence is not None  # Has evidence
assert mawdu_lah.binding_trace_id  # Has trace

# Whole comes from this structure, not raw text
assert mutabaqah_result.candidate.mawdu_lah_whole
assert mutabaqah_result.candidate.wadh_trace_id  # Proves governance
```

---

## Test Baseline Documented

**File**: `docs/PR_L6A_TEST_BASELINE.md`

**Key Findings**:
- ✅ PR-L6A introduces NO new failures
- ✅ All 29 MutabaqahGate tests passing
- ⚠️ 19 pre-existing failures in `test_dal_madlul_binding_candidate.py` (binding module)
- ✅ Pre-existing failures are ISOLATED (binding module NOT touched by PR-L6A)

**Root Cause of Pre-existing Failures**:
```python
AttributeError: 'StyleSpec' object has no attribute 'domain'
```

This is in `src/gfa/methods/lafzi_binding/dal_madlul_binding_gate.py:166` (NOT modified by PR-L6A).

---

## Governance Chain Verified

**WadhGate → MutabaqahGate chain intact**:

1. ✅ Cannot bypass WadhGate by constructing raw WadhClaim
2. ✅ Non-admitted WadhGateResult → MutabaqahGate blocks
3. ✅ WadhClaim trace (claim_id) must exist
4. ✅ Binding trace must be preserved
5. ✅ Traces propagate to MutabaqahCandidate
6. ✅ Residuals propagate (not lost)

---

## Semantic Inflation Guards (10 Total)

**Original (7)**:
1. ✅ NO external meaning
2. ✅ NO HUKM
3. ✅ NO Tadammun
4. ✅ NO Iltizam
5. ✅ NO Haqiqah/Majaz/Naql
6. ✅ NO Ifadah
7. ✅ NO rank inflation

**Hardening (3)**:
8. ✅ NO full Dalālah
9. ✅ NO Haqiqah classification
10. ✅ NO external truth

---

## Merge Readiness Criteria

### ✅ All Criteria Met

1. ✅ All MutabaqahGate tests passing (29/29)
2. ✅ No new failures introduced
3. ✅ Pre-existing failures documented and isolated
4. ✅ Semantic inflation guards verified (10 tests)
5. ✅ Governance chain verified (WadhGate → MutabaqahGate)
6. ✅ Residual propagation verified
7. ✅ Most dangerous hallucination (string gloss) guarded
8. ✅ Trace preservation verified
9. ✅ Test baseline documented
10. ✅ Hardening tests added and passing

### ❌ Not Claimed

- ❌ Does NOT claim "CERTIFIED for full suite"
- ❌ Does NOT claim pre-existing failures fixed
- ❌ Does NOT claim binding module issues resolved

---

## Test Execution Summary

```bash
# MutabaqahGate tests (PR-L6A scope)
$ python3 -m pytest tests/gfa/methods/test_mutabaqah_gate.py -v
======================== 29 passed in 0.17s ========================

# Full GFA suite (includes pre-existing failures)
$ python3 -m pytest tests/gfa/methods/ -v
==================== 197 passed, 19 failed in 0.81s ====================
```

---

## Recommendation

✅ **MERGE PR-L6A**

**Rationale**:
- All MutabaqahGate functionality verified (29/29 tests)
- No regression introduced
- Semantic boundaries enforced
- Governance chain intact
- Pre-existing failures isolated to separate module

⚠️ **Pre-existing failures** in binding module require separate PR (StyleSpec.domain field).

---

**Status**: ✅ PR-L6A hardened and ready for merge

**Documentation**:
- [PR_L6A_MUTABAQAH_GATE_SUMMARY.md](docs/PR_L6A_MUTABAQAH_GATE_SUMMARY.md)
- [PR_L6A_TEST_BASELINE.md](docs/PR_L6A_TEST_BASELINE.md)
