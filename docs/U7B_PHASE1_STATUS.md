# U₇-B Phase 1 Status: Protection-or-Defer Core Established

## Executive Summary

**PR #107 Status**: ✅ Phase 1 Complete - **NOT** Full U₇-B Closure

**Critical Achievement**: Established protection-or-defer policy and prevented the most dangerous gap (broken plurals entering U₈ as raw singular forms).

**Architectural Law Established**:
```
If marker family is not protected → root_input must be deferred.
```

---

## What PR #107 Actually Accomplished

### Core Innovation: Protection-or-Defer Policy

PR #107 established the foundational architectural pattern that will govern all of U₇-B:

```python
# CRITICAL POLICY: Protection-or-defer for root_input
if marker_family_is_not_protected(surface):
    root_input_permission = DEFERRED
    root_input = ""  # Empty - deferred pending evidence
    emit_residual("marker_family_deferred")
else:
    root_input_permission = ALLOWED
    root_input = protected_core
```

### Why This Matters: The Broken Plural Problem

**Before U₇-B Phase 1**:
```
رجال → U₈ might extract root as ر-ج-ل (WRONG - treats plural as singular)
مدارس → U₈ might extract م-د-ر-س (WRONG - treats plural as singular)
كتب → Ambiguous: books or "he wrote"? U₈ can't tell
```

**After U₇-B Phase 1**:
```
رجال → broken_plural_possible → root_input="" → DEFERRED → await lexical evidence
مدارس → broken_plural_possible → root_input="" → DEFERRED → await lexical evidence
كتب → ambiguous (plural/verb) → root_input="" → DEFERRED/AMBIGUOUS residual
```

This is **critically important** because in Arabic morphology:

> Every trilateral or quadrilateral surface ≠ directly extractable root

Especially with broken plurals (جمع التكسير), where the surface itself is the result of internal vowel transformations, not just affixation.

**Example**:
```
مدارس (schools)

If passed to U₈ raw, system might try to extract:
    م-د-ر-س (quadrilateral root - WRONG)

Or mistake it for a simple surface, when the correct path requires:
    مدارس ← broken plural candidate ← مدرسة/مدرس? ← needs lexicon/pattern/context
```

**PR #107 placed the correct barrier.**

---

## What Is Actually Covered Now

### ✅ Protected Marker Families (Phase 1)

1. **Definiteness**: الـ
2. **Tanwīn**: ـٌ، ـاً، ـٍ
3. **Sound Masculine Plural**: ون / ين
4. **Dual**: ان / ين
5. **Sound Feminine Plural**: ات
6. **Feminine marker**: ة / tā' marbūṭa
7. **Present tense prefixes**: ي، ت، ن، أ
8. **Some mazīd augmentation**: است، انـ
9. **Some attached pronouns**: ه، ها، هم، نا، ك
10. **Broken plural deferral** (via protection-or-defer pattern)
11. **U₈ blocked from reading root_input when DEFERRED/BLOCKED**
12. **Three-surface separation**: surface / protected_core / root_input

---

## What Is Still Missing (Cannot Leave Unprotected)

### ⚠️ Incomplete Marker Coverage (Phase 2+ Required)

| Marker Family | Status | Priority |
|---------------|--------|----------|
| **Original i'rāb markers** (ضمة، فتحة، كسرة، سكون) | ⚠️ Missing | HIGH |
| **Secondary i'rāb markers** (ألف، واو، ياء، نون، حذف النون، حذف حرف العلة) | ⚠️ Missing | HIGH |
| **Imperative markers** (همزة الوصل، حذف حرف العلة، حذف النون) | ⚠️ Missing | HIGH |
| **Passive voice surface** (ضم الأول وكسر ما قبل الآخر) | ⚠️ Missing | HIGH |
| **All attached pronouns** (not just some) | ⚠️ Partial | MEDIUM |
| **Rationality markers** (عاقل / غير عاقل surface agreement) | ⚠️ Missing | MEDIUM |
| **Six nouns** (الأسماء الستة) and annexed forms | ⚠️ Missing | MEDIUM |
| **Proper names, loanwords, jāmid** as defer/block paths (not raw root) | ⚠️ Partial | MEDIUM |
| **Clause-level contract** (U₇-C) - some markers need clause context | ⚠️ Not started | LOW |

---

## Architectural Truth: Why Phase 1 ≠ Closure

### The Remaining Law to Enforce

PR #107 established the **protection-or-defer principle**, but full U₇-B closure requires:

```
No U₈ root extraction from any surface segment
whose marker-family coverage is incomplete.
```

### Current State

**What's blocked**: ✅ Broken plurals (most dangerous gap closed)

**What's not yet blocked**: ⚠️ Surfaces with unprotected i'rāb, imperative, passive, pronoun markers

**Example of remaining gap**:
```
قُتِلَ (was killed - passive)

Current U₇-B Phase 1:
    - Might pass to U₈ as root_input="قتل"
    - Vowel pattern (ُـِـَ) not yet protected as passive surface hint

Full U₇-B (Phase 2+):
    - Should detect: passive_surface_hint=POSSIBLE
    - Should protect: vowel pattern markers
    - Should emit residual: passive_voice_surface_detected
```

---

## Correct Terminology

### ❌ Do NOT Say:
- "U₇-B complete"
- "U₇-B closed"
- "U₇-B fully implemented"

### ✅ DO Say:
- "U₇-B Phase 1 complete: Protection-or-defer core established"
- "U₇-B broken plural deferral active"
- "U₇-B core policy implemented, full marker coverage pending"

---

## Roadmap: What Comes Next

### Logical Next Steps

**PR #108: Complete U₇-B Marker Protection Matrix**

**NOT** U₈ refinement. **NOT** U₉ weight. First complete U₇-B.

**Contents**:
1. I'rāb original marker protection (ضمة، فتحة، كسرة، سكون)
2. I'rāb secondary marker protection (ألف، واو، ياء، نون، حذف)
3. Full attached-pronoun suffix inventory (all 14 forms)
4. Imperative surface protection (همزة الوصل، حذف حرف العلة، حذف النون)
5. Passive surface protection (vowel pattern detection)
6. Six nouns / annexed forms protection
7. Proper-name / loanword / jāmid deferral policy completion
8. **Explicit marker coverage matrix tests**

Then:

**PR #109: Introduce U₇-C ClauseSurfacePatternContract**

Because some markers cannot be resolved within a single word - they require clause-level context.

---

## Test Coverage Status

### Current Tests (53 total)

**Golden cases**: 13
- 9 marker protection cases (الكتاب, كتابٌ, مسلمان, مسلمين, مسلمون, مسلمات, مدرسة, يكتبون, استخرج)
- 3 broken plural deferral cases (رجال, مدارس, كتب) - **CRITICAL**
- 1 pronoun suffix case (كتابه, كتابها, كتابهم)

**Architectural tests**: 40
- Three-surface separation verification
- Constitutional prohibitions (no root, weight, hukm fields)
- Marker hint validation
- CPB₇B completeness
- U₈ DEFERRED/BLOCKED enforcement

### Required for Phase 2

**Marker coverage matrix tests**:
- Each marker family must have:
  - ✅ Detection test
  - ✅ Protection test
  - ✅ Deferral test (if unprotected)
  - ✅ U₈ blocking test
  - ✅ Residual emission test

---

## Critical Laws Enforced (Phase 1)

### ✅ Implemented

1. **No root from raw surface** (Axiom 7B.1)
   - U₈ consumes `root_input`, never `surface`

2. **No stripping without trace** (Axiom 7B.3)
   - All protected markers preserved in ordered trace

3. **surface ≠ protected_core ≠ root_input** (Axiom 7B.5)
   - Three distinct surfaces maintained

4. **Protection-or-defer policy**
   - Broken plurals → DEFERRED
   - Unprotected markers → DEFERRED (principle established)

5. **U₈ enforcement**
   - Checks `root_input_permission` before extraction
   - DEFERRED → no extraction, emit DEFERRED status
   - BLOCKED → no extraction, emit BLOCKED status

### ⚠️ Partially Implemented

6. **No marker deletion; only protection** (Axiom 7B.4)
   - Currently: definiteness, tanwīn, number, gender, some pronouns
   - Missing: i'rāb, imperative, passive, rationality, six nouns

7. **Marker ≠ judgment** (Axiom 7B.6)
   - All outputs are hints (POSSIBLE/UNLIKELY/UNRESOLVED/AMBIGUOUS)
   - No final grammatical judgments

---

## Merge Decision Criteria

### PR #107 IS Mergeable If:

✅ All tests pass (53/53)
✅ No breaking changes to existing U₇-A or U₈
✅ Protection-or-defer pattern demonstrably working
✅ Broken plural deferral verified
✅ Documentation clearly states "Phase 1" not "Closure"

### PR Description MUST Include:

```markdown
## Status: U₇-B Phase 1 - Protection-or-Defer Core

This PR establishes U₇-B protection-or-defer Phase 1.
**It does NOT fully close U₇-B marker coverage.**

### What This PR Accomplishes
- Establishes protection-or-defer architectural pattern
- Implements broken plural deferral (رجال، مدارس، كتب)
- Prevents most dangerous gap (plurals as raw singulars)
- Adds pronoun suffix protection (partial)
- Enforces U₈ respect for DEFERRED/BLOCKED status

### What Remains for Full U₇-B Closure
- I'rāb marker protection (original + secondary)
- Imperative marker protection
- Passive voice surface protection
- Complete pronoun suffix inventory
- Six nouns protection
- Marker coverage matrix tests

### Architectural Status
✅ U₇-B core policy active
⚠️ Full marker coverage pending (Phase 2+)
```

---

## Files Changed (Phase 1)

1. **New**:
   - `src/dal_core/u7b_inflectional_surface_contract_carrier.py` (856 lines)
   - `tests/dal_core/test_u7b_inflectional_surface_contract.py` (710 lines)
   - `docs/U7B_INFLECTIONAL_SURFACE_CONTRACT.md` (555 lines)

2. **Modified**:
   - `src/dal_core/execution_layer_registry.py` (split U₇ → U₇-A + U₇-B)
   - `src/dal_core/u8_root_stem_candidate_carrier.py` (added permission checking)

3. **New (this document)**:
   - `docs/U7B_PHASE1_STATUS.md` (status clarification)

---

## Summary

**PR #107 is correct and critically important**, especially for broken plurals.

But it is a **central protection phase**, not the end of protection.

### Final Formulation

✅ **U₇-B now has the protection-or-defer law**
✅ **Broken plurals no longer enter U₈ as raw root input**
⚠️ **But full U₇-B closure requires complete marker coverage matrix**

### Strongest Law to Enforce Now

```
No U₈ root extraction from any surface segment
whose marker-family coverage is incomplete.
```

**Phase 1 Status**: Core policy established, most dangerous gap closed.

**Phase 2 Required**: Complete marker protection matrix before any layer beyond U₈.

---

**Document Version**: 1.0
**Date**: 2026-05-26
**Corresponds to**: Commit 1523f31 (PR #107)
**Next Required**: PR #108 (Complete Marker Coverage Matrix)
