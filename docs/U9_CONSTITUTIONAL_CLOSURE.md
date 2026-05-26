# U₉ WeightCandidateCarrier Constitutional Closure

**Date:** 2026-05-26
**Status:** ✅ CLOSED CONSTITUTIONALLY
**Final PR:** #116 (Legacy path blocked)
**Branch:** `claude/update-u9-constitution-status`

---

## Executive Summary

**U₉ WeightCandidateCarrier is now constitutionally closed.** After PR #116, there is no longer a legacy execution path. U₉ has one canonical governed implementation under AlgebraicDecisionCore control.

### What Changed After #116

**Before #116:**
- U₉ constitutional implementation existed
- Legacy path (`u9_arabic_weight.py`) still executable
- Status: "U₉ constitutional but with legacy path"

**After #116:**
- U₉ has **single canonical governed implementation**
- Legacy path **constitutionally blocked** (raises `RuntimeError`)
- Status: "U₉ canonical single governed implementation"

---

## Constitutional Chain (السلسلة الدستورية)

The complete constitutional foundation for U₉:

```
#111: U₈ preserves agreement edges (doesn't consume them)
      └─→ Law: Agreement surface preserved as external trace

#112: AlgebraicDecisionCore governs transitions
      └─→ Law: No transition without governance decision

#113: ApprovedTransitionContext cannot be forged
      └─→ Law: Context only from approved DecisionAudit

#114: AlgebraicDecisionCore constitutionally green
      └─→ Law: Governor fully operational and tested

#115: Constitutional U₉ introduced
      └─→ Law: U₉ operates under ApprovedTransitionContext

#116: U₉ becomes canonical single implementation
      └─→ Law: Legacy path blocked, one official path only
```

---

## Final Constitutional Laws (القوانين الدستورية النهائية)

### Arabic Formulation

```
لا وزن بلا ApprovedTransitionContext.
ولا ApprovedTransitionContext بلا DecisionAudit مُجاز.
ولا DecisionAudit بلا AlgebraicDecisionCore.
ولا U₉ legacy path.
ولا وزن خارج التنفيذ الرسمي المحكوم.
```

### English Translation

1. **No weight without ApprovedTransitionContext**
   U₉ execution requires approved governance context.

2. **No ApprovedTransitionContext without approved DecisionAudit**
   Context can only be created from APPROVED audit status.

3. **No DecisionAudit without AlgebraicDecisionCore**
   Only the governor can create valid decision audits.

4. **No U₉ legacy path**
   Legacy `u9_arabic_weight.py` raises `RuntimeError` constitutionally.

5. **No weight outside official governed execution**
   All weight determination flows through canonical governed path.

---

## Official U₉ Implementation

### Single Canonical Path

**File:** `src/dal_core/u9_weight_candidate_carrier.py`

**Exports:**
```python
from dal_core import (
    WeightCandidateResult,
    weight_candidate_carrier_9,
    validate_approved_context_for_u9,
)
```

**Execution Pattern:**
```
Pipeline/Orchestrator
  └─→ AlgebraicDecisionCore.decide_transition(U₈→U₉)
      └─→ DecisionAudit (status = APPROVED)
          └─→ create_approved_context(audit)
              └─→ ApprovedTransitionContext
                  └─→ weight_candidate_carrier_9(u8_input, context)
                      └─→ WeightCandidateResult
```

### Constitutional Requirements (12 Laws)

All 12 constitutional tests passing (see `test_u9_weight_candidate_constitutional.py`):

1. ✅ No execution without ApprovedTransitionContext
2. ✅ No direct AlgebraicDecisionCore instantiation
3. ✅ Context must be for U₈→U₉ transition
4. ✅ Context domain must be WEIGHT_DOMAIN
5. ✅ Input identity must be ROOT_MATERIAL_IDENTITY or STEM_IDENTITY
6. ✅ No SEMANTIC_IDENTITY output
7. ✅ No HUKM_IDENTITY output
8. ✅ No FUNCTIONAL_RELATION_IDENTITY output
9. ✅ U₇-C agreement edges preserved as external trace
10. ✅ Residual audit preserved
11. ✅ Candidate rank preserved (not certificate)
12. ✅ Golden path execution

---

## Domain Boundaries

### Forbidden in WEIGHT_DOMAIN

- ✗ Meaning determination (معنى)
- ✗ Syntactic role assignment (فاعل نحوي)
- ✗ I'rab judgment (إعراب)
- ✗ Hukm production (حكم)
- ✗ Semantic derivation (اشتقاق معنوي)
- ✗ Functional assignment (وظيفة)

### Permitted in WEIGHT_DOMAIN

- ✓ Weight pattern determination (وزن)
- ✓ Morphological template mapping (قالب صرفي)
- ✓ F-'-L consonantal mapping (فاء-عين-لام)
- ✓ Candidate rank (not certificate)
- ✓ Residual audit preservation

---

## Legacy Path Status

### File: `u9_arabic_weight.py`

**Status:** DEPRECATED and BLOCKED

**Purpose:** Backward compatibility warnings only

**Execution:** Raises `RuntimeError` with migration guidance

**Warning Banner:**
```
⚠️ DEPRECATION WARNING ⚠️
This module is DEPRECATED and maintained only for backward compatibility.

Official U₉ Implementation:
    src/dal_core/u9_weight_candidate_carrier.py

DO NOT use dispatch_weight() directly.
DO NOT use gate_89_validate() directly.

Use ONLY the new official API from dal_core.
```

---

## Verification Commands

### Test U₉ Constitutional Laws
```bash
pytest tests/dal_core/test_u9_weight_candidate_constitutional.py -v
# Expected: 12/12 tests passing
```

### Test U₉ Canonicalization
```bash
pytest tests/dal_core/test_u9_canonicalization.py -v
# Expected: Verifies single canonical implementation
```

### Verify Exports
```python
from dal_core import (
    WeightCandidateResult,
    weight_candidate_carrier_9,
    validate_approved_context_for_u9,
)
# Should import successfully from official implementation
```

---

## What U₉ Is (and Is Not)

### U₉ IS

- **WeightCandidateCarrier** - Carries weight pattern candidates
- **Governed** - Operates under AlgebraicDecisionCore
- **Morphological** - Operates in WEIGHT_DOMAIN only
- **Candidate Producer** - Produces ranked candidates, not certificates
- **Trace Preserver** - Maintains complete execution trace

### U₉ IS NOT

- **WeightCertifier** - Does not certify weight (requires downstream evidence)
- **Meaning Determiner** - Does not determine semantic meaning
- **Syntactic Role Assigner** - Does not assign grammatical functions
- **Hukm Producer** - Does not produce grammatical judgments
- **Direct Executor** - Cannot execute without ApprovedTransitionContext

---

## Next Layer: U₁₀ WordFormCandidateCarrier

With U₉ constitutionally closed, the foundation is ready for U₁₀.

### Constitutional Principle

```
لا معنى بعد الوزن حتى تثبت صورة الكلمة.
No semantic transition before governed WordFormCandidate.
```

### Architecture

```
U₉ WeightCandidateCarrier
   ↓ (governed transition)
U₁₀ WordFormCandidateCarrier
   ↓ (NOT direct to meaning)
U₁₁+ Semantic/Syntactic layers
```

### U₁₀ Purpose

**NOT:**
- Meaning determination
- Syntactic role assignment
- Hukm production

**YES:**
- Word form/structure carrier
- Preserves WEIGHT_IDENTITY
- Prevents direct weight→meaning jumps
- Operates under ApprovedTransitionContext

---

## Architectural Milestone

U₉ represents a critical milestone in the constitutional architecture:

1. **First layer implemented AFTER governance infrastructure**
2. **Demonstrates end-to-end constitutional enforcement**
3. **Proves AlgebraicDecisionCore operational**
4. **Establishes pattern for all future layers**

### Key Achievement

> U₉ is not just "working code" - it is **constitutionally governed code** that cannot execute outside the official approval pathway.

This is the foundation for building the entire execution core (U₀-U₁₅) with constitutional integrity.

---

## Status Summary

| Aspect | Status |
|--------|--------|
| Implementation | ✅ Complete |
| Constitutional Tests | ✅ 12/12 Passing |
| Governance Integration | ✅ AlgebraicDecisionCore |
| Legacy Path | ✅ Blocked |
| Domain Boundaries | ✅ Enforced |
| Export API | ✅ Official |
| Documentation | ✅ Complete |
| **Overall Status** | **✅ CLOSED CONSTITUTIONALLY** |

---

## References

- **Implementation:** `src/dal_core/u9_weight_candidate_carrier.py`
- **Tests:** `tests/dal_core/test_u9_weight_candidate_constitutional.py`
- **Documentation:** `docs/U9_CONSTITUTIONAL_IMPLEMENTATION_SUMMARY.md`
- **PR Chain:** #111, #112, #113, #114, #115, #116
- **Governance:** `src/dal_core/algebraic_decision_core.py`
- **Context:** `src/dal_core/approved_transition_context.py`

---

**Conclusion:**
U₉ WeightCandidateCarrier is constitutionally closed. One canonical governed implementation. No legacy path. Foundation ready for U₁₀ WordFormCandidateCarrier.
