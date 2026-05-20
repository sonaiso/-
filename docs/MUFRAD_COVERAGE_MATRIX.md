# مصفوفة التغطية الشاملة للفظ المفرد

# Mufrad Comprehensive Coverage Matrix

**Status**: 🚧 Framework Defined (Coverage Certification Pending)
**Version**: 1.0.0
**Created**: 2026-05-20
**Last Updated**: 2026-05-20

---

## Executive Summary

هذه الوثيقة تحدد **التغطية الكاملة الجامعة المانعة** للفظ المفرد (Arabic singular word) عبر **10 طبقات** من التحليل الشكلي (pre-semantic form analysis).

This document defines **comprehensive and exclusive coverage** of the Arabic singular word across **10 layers** of pre-semantic form analysis.

---

## الوضع الحالي (Current Status)

### ✅ ما تم إنجازه (Already Achieved)

| Component | Status | Evidence |
|-----------|--------|----------|
| Framework Defined | ✅ Complete | `PROJECT_ALGEBRA_ROADMAP.md` |
| 8-Layer Domain Architecture (D0-D7) | ✅ Complete | `DAL_ALGEBRA_SIGNATURE.md` |
| MufradProof Contract | ✅ Complete | `DAL_CORE_MUFRAD_PROOF.md` |
| Four Orthogonal Axes | ✅ Complete | `MUFRAD_AXES.md` |
| Roadmap Governance | ✅ Complete | `ROADMAP_GOVERNANCE.md` (PR #27) |

### ❌ ما لم يتم بعد (Not Yet Achieved)

| Gap | Required For Certification |
|-----|----------------------------|
| Coverage Matrix Documentation | 10 layer-specific matrices |
| Golden Dataset | 100-200 annotated words |
| Deep Template Contract | `DeepTemplateCandidate` |
| Verb Health Classification | `VerbHealthCandidate` |
| Word Type Taxonomy Extension | Subtype candidates |
| Gender-Number-Definiteness Contracts | Full taxonomy |
| Event-Aspect-Transitivity | `TransitivityCandidate` |
| Lexicon Integration | 500+ entries + attestation |
| Coverage Audit Tests | 400+ tests |
| **Coverage Certification** | Final audit + evidence |

---

## المبدأ الأساسي (Core Principle)

```
لا شهادة بلا دليل
(No Certificate Without Evidence)
```

### القواعد الحاكمة (Governing Rules)

1. **الجامع المانع (Comprehensive and Exclusive)**
   - الجامع: تغطية جميع المفاهيم المطلوبة
   - المانع: منع الادعاءات الكاذبة

2. **الدليل أولًا (Evidence First)**
   ```
   Certificate ⇒ Evidence + Tests + Coverage
   Coverage Claim ⇒ Matrix + Golden Dataset
   ```

3. **القياس ≠ السماع (Qiyas ≠ Sama')**
   ```
   إذا كان سماعيًا ولا معجم:
     ⇒ Candidate, NOT Certificate
   ```

4. **الشكل ≠ المعنى (Form ≠ Meaning)**
   ```
   كل طبقات المفرد = شكلية
   لا دلالة، لا مراد، لا حقيقة/مجاز
   ```

5. **لا ترقية بلا عقد (No Promotion Without Contract)**
   ```
   المقطع الصوتي ≠ الوزن الصرفي
   الوزن الظاهر ≠ الوزن العميق
   الجذر ≠ الوزن (يتطلب عقد انتقال)
   ```

---

## الطبقات العشر (10 Layers)

| # | الطبقة | Layer | Matrix Document | Status |
|---|--------|-------|-----------------|--------|
| K.1 | الرسم والضبط | Grapho-Orthographic | [K.1-ORTHOGRAPHY-COVERAGE-MATRIX.md](coverage/K.1-ORTHOGRAPHY-COVERAGE-MATRIX.md) | 🚧 Defined |
| K.2 | الصوت والمقطع | Phonological-Syllabic | [K.2-PHONOLOGY-COVERAGE-MATRIX.md](coverage/K.2-PHONOLOGY-COVERAGE-MATRIX.md) | 🚧 Defined |
| K.3 | الأصل والزيادة واللواصق | Origin-Augmentation-Clitics | [K.3-ORIGIN-SEGMENTATION-MATRIX.md](coverage/K.3-ORIGIN-SEGMENTATION-MATRIX.md) | 🚧 Defined |
| K.4 | الوزن الظاهر والعميق | Surface vs Deep Template | [K.4-TEMPLATE-TRANSFORMATION-MATRIX.md](coverage/K.4-TEMPLATE-TRANSFORMATION-MATRIX.md) | ❌ Not Implemented |
| K.5 | الصحة والاعتلال والهمز | Verb Health Classification | [K.5-VERB-HEALTH-MATRIX.md](coverage/K.5-VERB-HEALTH-MATRIX.md) | ❌ Not Implemented |
| K.6 | نوع الكلمة | Word Type Taxonomy | [K.6-WORD-TYPE-TAXONOMY-MATRIX.md](coverage/K.6-WORD-TYPE-TAXONOMY-MATRIX.md) | 🚧 Partial |
| K.7 | القوى الأربع السطحية | Four Surface Forces | [K.7-SURFACE-FORCES-VERIFICATION.md](coverage/K.7-SURFACE-FORCES-VERIFICATION.md) | ✅ Implemented |
| K.8 | الجنس والعدد والتعريف | Gender-Number-Definiteness | [K.8-GENDER-NUMBER-DEFINITENESS-MATRIX.md](coverage/K.8-GENDER-NUMBER-DEFINITENESS-MATRIX.md) | 🚧 Partial |
| K.9 | الحدث وأحواله | Event and Aspect | [K.9-EVENT-ASPECT-TRANSITIVITY-MATRIX.md](coverage/K.9-EVENT-ASPECT-TRANSITIVITY-MATRIX.md) | 🚧 Partial |
| K.10 | المعجم والسماع | Lexicon and Attestation | [K.10-LEXICON-ATTESTATION-MATRIX.md](coverage/K.10-LEXICON-ATTESTATION-MATRIX.md) | ❌ Not Implemented |

**Legend**:
- ✅ Implemented: Contract + Tests + Documentation
- 🚧 Partial: Some components exist, incomplete coverage
- 🚧 Defined: Framework exists, needs implementation
- ❌ Not Implemented: Missing completely

---

## نموذج المصفوفة (Matrix Template)

كل طبقة تحتوي على:

Each layer contains:

### 1. Required Concepts (المفاهيم المطلوبة)

القائمة الكاملة للمفاهيم التي يجب تغطيتها.

Complete list of concepts that must be covered.

### 2. Allowed Claims (الادعاءات المسموحة)

الادعاءات العلمية المسموح بها بعد التنفيذ.

Scientific claims allowed after implementation.

### 3. Forbidden Claims (الادعاءات الممنوعة)

الادعاءات الكاذبة أو السابقة لأوانها.

False or premature claims.

### 4. Requires Lexicon? (تحتاج معجم؟)

هل تتطلب هذه الطبقة رجوعًا للمعجم/السماع؟

Does this layer require lexicon/attestation lookup?

### 5. Requires Context? (تحتاج سياق؟)

هل تتطلب هذه الطبقة سياقًا تركيبيًا؟

Does this layer require compositional context?

### 6. Failure Types (أنواع الفشل)

أنواع الفشل المحتملة وبقايا (residuals) المرتبطة.

Potential failure types and associated residuals.

### 7. Golden Tests (الاختبارات الذهبية)

20-30 حالة اختبار لكل طبقة.

20-30 test cases per layer.

### 8. Status (الحالة)

الحالة الحالية للتنفيذ.

Current implementation status.

### 9. Evidence Artifact (أثر الدليل)

الملفات والاختبارات المطلوبة للإثبات.

Required files and tests for proof.

---

## خطة التنفيذ (Implementation Roadmap)

### Phase 1: Documentation (PR #28) - **Current Phase**

**Timeline**: 2-3 weeks
**Status**: 🚧 In Progress

**Deliverables**:
- ✅ `MUFRAD_COVERAGE_MATRIX.md` (this document)
- 🚧 10 layer-specific coverage matrices
- 🚧 Gap analysis for each layer

### Phase 2: Golden Dataset (PR #29)

**Timeline**: 3-4 weeks
**Status**: 📋 Planned

**Deliverables**:
- 100-200 annotated singular words
- Coverage across all 10 layers
- JSON structure + tests
- Coverage report

### Phase 3: Missing Contracts (PR #30-35)

**Timeline**: 4-6 months
**Status**: 📋 Planned

**Contracts to Implement**:
1. **PR #30**: Deep Template Contract
2. **PR #31**: Verb Health Classification
3. **PR #32**: Word Type Taxonomy Extension
4. **PR #33**: Gender-Number-Definiteness Contracts
5. **PR #34**: Event-Aspect-Transitivity
6. **PR #35**: Lexicon Integration

### Phase 4: Coverage Audit (PR #36)

**Timeline**: 2-3 weeks
**Status**: 📋 Planned

**Deliverables**:
- 400+ coverage tests
- Audit report per layer
- Gap closure verification

### Phase 5: Coverage Certification (PR #37)

**Timeline**: 1 week
**Status**: 📋 Planned

**Deliverables**:
- Final certification document
- Allowed/forbidden claims
- Evidence artifacts index

---

## نقاط التحقق (Verification Checkpoints)

### After Phase 1 (Documentation)
- ✅ All 10 matrices documented
- ✅ Gap analysis complete
- ✅ Roadmap integrated with PROJECT_ALGEBRA_ROADMAP.md

### After Phase 2 (Golden Dataset)
- ✅ 100+ words annotated across 10 layers
- ✅ Coverage report generated
- ✅ 50+ golden tests passing

### After Phase 3 (Contracts)
- ✅ All 10 layers have contracts
- ✅ 200+ layer-specific tests passing
- ✅ No forbidden direct promotions

### After Phase 4 (Audit)
- ✅ 400+ coverage tests passing
- ✅ All gaps documented or closed
- ✅ Residuals properly classified

### After Phase 5 (Certification)
- ✅ Coverage Matrix Certified
- ✅ Mufrad Algebra Complete
- ✅ Total-Coverage Closed

---

## معايير النجاح (Success Criteria)

### التغطية مكتملة إذا (Coverage is complete if):

1. ✅ جميع الطبقات العشر لها عقود (All 10 layers have contracts)
2. ✅ جميع المفاهيم المطلوبة مغطاة (All required concepts covered)
3. ✅ 100+ كلمة ذهبية مشروحة (100+ golden words annotated)
4. ✅ 400+ اختبار تغطية تنجح (400+ coverage tests pass)
5. ✅ المعجم مدمج للسماعيات (Lexicon integrated for sama')
6. ✅ لا ترقيات محظورة (No forbidden promotions)
7. ✅ لا تسرب دلالي (No semantic leak)
8. ✅ كل claim له دليل (Every claim has evidence)

---

## الادعاء المسموح بعد الإكمال

## Allowed Claim After Completion

```
✅ `dal_core` now provides **certified comprehensive coverage**
   of the Arabic singular word (اللفظ المفرد) across 10 layers:

   1. Orthography (الرسم والضبط)
   2. Phonology (الصوت والمقطع)
   3. Origin-Segmentation (الأصل والزيادة واللواصق)
   4. Template Transformation (الوزن الظاهر والعميق)
   5. Verb Health (الصحة والاعتلال)
   6. Word Type Taxonomy (نوع الكلمة)
   7. Surface Forces (القوى السطحية الأربع)
   8. Gender-Number-Definiteness (الجنس والعدد والتعريف)
   9. Event-Aspect (الحدث وأحواله)
   10. Lexicon-Attestation (المعجم والسماع)

   With 200+ golden words, 400+ coverage tests, and
   evidence-based governance.
```

---

## الادعاء الممنوع

## Forbidden Claim

```
❌ "اللفظ المفرد مكتمل" بدون:
   - المصفوفة الكاملة
   - Dataset الذهبي
   - الاختبارات
   - الأدلة

❌ "التغطية شاملة" بدون:
   - الطبقات العشر
   - المعجم المدمج
   - قواعد السماع

❌ "النظام يفهم المعنى"
   (dal_core is pre-semantic)

❌ "النظام يفسر الدلالة"
   (dal_core ends at form)
```

---

## مراجع متقاطعة (Cross-References)

- `PROJECT_ALGEBRA_ROADMAP.md` - Overall algebra architecture roadmap
- `DAL_CORE_MUFRAD_PROOF.md` - MufradProof contract specification
- `MUFRAD_AXES.md` - Four orthogonal axes (already implemented)
- `DAL_ALGEBRA_SIGNATURE.md` - 8-layer domain architecture
- `ROADMAP_GOVERNANCE.md` - Governance rules (PR #27)

---

**Version**: 1.0.0
**Phase**: 1 of 5 (Documentation)
**Next Milestone**: Complete all 10 layer-specific matrices
**Target Completion**: PR #37 (6-8 months)
