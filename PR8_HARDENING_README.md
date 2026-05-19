# PR #8 Hardening Requirements - Documentation Suite

This branch contains comprehensive documentation for hardening the MufradProof implementation from PR #8 before proceeding to full syntax composition.

## Files Created

### 1. **PR8_COMMENT.md** (Recommended for posting)
Concise, ready-to-post comment text for PR #8. Contains:
- Summary of 10 required additions
- Key distinction: CaseSignPotential vs CaseEffect
- 20+ test requirements
- Acceptance criteria
- Allowed/forbidden claims
- Arabic summary

**Usage**: Copy content directly to PR #8 as a comment.

### 2. **PR8_HARDENING_REQUIREMENTS.md** (Detailed specification)
Full technical specification with:
- Detailed code examples for each requirement
- Complete type signatures
- Comprehensive test descriptions
- Implementation guidelines
- Architectural justification

**Usage**: Reference document for implementation work.

### 3. **GITHUB_ISSUE_PR8_HARDENING.md** (Issue template)
Complete GitHub issue template with:
- Implementation checklist (6 major sections)
- Acceptance criteria (10 requirements)
- Related work references
- Priority and labels
- Bilingual summary

**Usage**: Create a tracking issue in GitHub using this template.

## Context

**PR #8 Status**: Merged (2026-05-19)
- Successfully implemented MufradProof base
- Enforced 10 core theorems
- 21/21 tests passing

**Next Required Phase**: Pre-Syntax Interface Layer
- Add PreSyntaxMufradVector (typed interface)
- Add CaseSignPotential (surface observations, not case judgments)
- Add OperatorReadiness (composition contracts)
- Model original/substitute signs explicitly
- Stub registry for future grammar operators
- Strengthen competitor handling
- Add composition rank ceiling rules

## Critical Distinction

```text
✅ ALLOWED in MufradProof:
   - SurfaceEffect (observable diacritics)
   - CaseSignPotential (sign observations + compatible interpretations)
   - MorphFeatures (as candidates with evidence/rank)

❌ FORBIDDEN in MufradProof:
   - CaseEffect (grammatical case judgments)
   - SyntaxRole (faail, mafool, mubtada, khabar)
   - Semantic fields (meaning, murad, haqiqa, majaz)
```

## Why This Matters

The hundred grammatical operators (العوامل النحوية المئة) will be implemented as ranked `OperatorContract`s that consume composition-ready `MufradProof`. This hardening layer ensures:

1. **D_mufrad** = numerical morphological basis (no syntax, no meaning)
2. **D_murakkab** = composition layer (syntax operators + case effects)
3. Clean architectural boundary with no leakage

## Implementation Path

1. ✅ Create tracking issue (use GITHUB_ISSUE_PR8_HARDENING.md)
2. ✅ Post comment to PR #8 (use PR8_COMMENT.md)
3. ⏳ Implement hardening layer in new PR
4. ⏳ Verify all 20+ tests pass
5. ⏳ Ensure no semantic/syntax/case-effect leaks
6. ⏳ Mark new PR ready when all acceptance criteria met

## Posting Instructions

### To add comment to PR #8:
1. Navigate to: https://github.com/sonaiso/-/pull/8
2. Scroll to bottom (comment section)
3. Copy entire content of `PR8_COMMENT.md`
4. Paste and submit comment

### To create tracking issue:
1. Navigate to: https://github.com/sonaiso/-/issues
2. Click "New issue"
3. Copy content of `GITHUB_ISSUE_PR8_HARDENING.md`
4. Set title: "Harden MufradProof with Pre-Syntax Interface Layer"
5. Add labels: `enhancement`, `dal_core`, `phase-2`
6. Submit issue

## Acceptance Before Merge

The follow-up implementation PR must satisfy:

1. ✅ All CI checks pass
2. ✅ All existing dal_core tests pass (21 tests)
3. ✅ All new tests pass (20+ additional tests)
4. ✅ No semantic field leaks
5. ✅ No syntax role leaks
6. ✅ No CaseEffect leaks
7. ✅ PreSyntaxMufradVector exists and tested
8. ✅ CaseSignPotential exists and tested
9. ✅ OperatorReadiness exists and tested
10. ✅ Operator registry stub exists (source/school/rank-bound)

## الخلاصة بالعربية

تحتوي هذه الوثائق على المتطلبات الكاملة لتقوية `MufradProof` قبل الدخول في تركيب الجمل:

1. **PreSyntaxMufradVector**: واجهة رقمية بلا معنى دلالي
2. **CaseSignPotential**: العلامات كاحتماليات سطحية (ليست أحكام إعرابية)
3. **OperatorReadiness**: عقد الجاهزية للتركيب
4. تمييز واضح: D_mufrad (أساس رقمي) ≠ D_murakkab (تركيب نحوي)
5. منع تسريب المعنى أو الدور النحوي أو أثر الإعراب إلى المفرد

**الهدف**: جسر معماري ضروري بين المفرد والتركيب، يحفظ النقاء الرقمي للمفرد.

---

**Branch**: `claude/update-pr-8-comment`
**Reference PR**: #8 (merged)
**Date**: 2026-05-19
