# PR #10 Review - Action Required

## Context

PR #10 introduces the PreSyntax Interface (`PreSyntaxMufradVector`, `CaseSignPotential`, `type_ids.py`) as the bridge between `MufradProof` (lexical layer) and future syntax operators.

**Current Status**: Draft, not ready for merge

**Scientific Assessment**: PR is directionally correct (65% complete) but requires hardening before moving from Draft to Ready for Review.

---

## Required Actions

### For Repository Owner/Maintainer

1. **Post the review comment to PR #10**
   - Review comment is in: `PR_10_REVIEW_COMMENT.md`
   - Post this as a comment on GitHub PR #10

2. **Keep PR #10 in Draft status** until all 4 hardening points are addressed

3. **Review the detailed analysis**
   - See `PR_10_HARDENING_ANALYSIS.md` for current implementation status
   - 13 tests need to be added
   - 2 validation logic enhancements needed

---

## Four Critical Hardening Points

### 1. Conditional `allows_operator_consumption()`
**Status**: ⚠️ Partial implementation
**Gap**: Currently only checks `composition_readiness`, missing checks for:
- Blocking residuals
- Trace to raw input
- Rank ceiling
- Unresolved competitors (for certificate)

**Required**: 4 new tests + logic enhancement

### 2. `CaseSignPotential` ≠ `CaseEffect`
**Status**: ✅ Well implemented
**Gap**: Minor - add 3 explicit tests for documentation

**Required**: 3 new tests (enforcement logic already exists)

### 3. Type IDs = Operational Codes, Not Meanings
**Status**: ✅ Well documented
**Gap**: Tests exist but with different names

**Required**: 3 renamed/additional tests for clarity

### 4. Rank Preservation (No Rank Inflation)
**Status**: ⚠️ Structure exists but no validation
**Gap**: No validation that `rank(PreSyntaxVector) <= rank(MufradProof)`

**Required**: 3 new tests + validation logic

---

## Scientific Boundary Enforcement

After hardening, PR #10 will enforce:

### ✅ Allowed Claims
```
dal_core can export a governed PreSyntaxMufradVector from MufradProof for future syntax operators.
```

### ❌ Forbidden Claims
```
dal_core performs syntax.
CaseSignPotential is CaseEffect.
Operators may consume raw tokens or incomplete MufradProof.
```

---

## Files Generated

1. **PR_10_REVIEW_COMMENT.md** - Ready-to-post review comment for GitHub PR #10
2. **PR_10_HARDENING_ANALYSIS.md** - Detailed implementation status analysis
3. **This file** - Action summary and instructions

---

## Next Steps

### Immediate (before merge)
1. Post review comment to PR #10 on GitHub
2. Implement 13 missing tests
3. Enhance `allows_operator_consumption()` logic
4. Add rank preservation validation
5. Re-run full test suite
6. Move PR from Draft to Ready for Review only after all tests pass

### After Merge (future PRs)
Once PR #10 is hardened and merged, it becomes foundation for:
- **PR #11**: SentenceFrameProof
- **PR #12**: CaseSignMatrix
- **PR #13**: NahwOperatorRegistry

---

## Why This Matters

The PreSyntax interface is the **critical gate** preventing:
- ❌ Operators working on raw tokens (hallucination risk)
- ❌ Syntax logic leaking into lexical layer
- ❌ Case effects appearing before operator governance
- ❌ Incomplete proofs entering composition

**Weak gate = broken architecture**
**Strong gate = provably safe syntax composition**

---

## القرار العلمي

```text
PR #10 = خطوة صحيحة جدًا.
لكن لا يُدمج حتى نضمن أن PreSyntaxMufradVector ليس مجرد data export،
بل بوابة حاكمة تمنع العامل من العمل على مفرد ناقص.
```

**Current Hardening Level**: 65%
**Required for Merge**: 100%
**Missing Components**: 13 tests + 2 validation enhancements
