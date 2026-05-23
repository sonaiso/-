# خطة المشروع الرئيسية الموحدة 2026
# Master Unified Project Plan 2026

**تاريخ الإنشاء**: 2026-05-23
**الحالة**: خطة موحدة نشطة تدمج جميع المسارات
**المالك**: فريق المشروع

---

## الملخص التنفيذي

هذه الوثيقة هي **المرجع الوحيد** للخطة الرئيسية للمشروع، تدمج:

1. **Dal Algebra Roadmap** (PR #22-#48+)
2. **FVAFK Pipeline** (6-Month Enhanced Roadmap)
3. **Pure Dāl Geometry Architecture** (المسار الجديد الحرج)
4. **AGT Framework Extensions** (Coq Formal Theory)
5. **GFA Methods** (PR-L4, PR-L5, PR-L6 series)

---

## 🎯 المبادئ الجوهرية

### 1. الفصل المعماري الصارم

```
الطبقة 0: Pure Signal (الإشارة الخام)
  ↓
الطبقة 1: Pure Dāl Geometry (هندسة الدال وحده)
  DalCandidate = {
    phonic_carriers, haraka_operations, syllable_licenses,
    word_boundaries, clitics, formula_candidates,
    path_type, pattern_status, terminal_state,
    syntactic_readiness, sentence_shape,
    role_projection_candidates, rank, residuals, trace_id
  }
  ↓
الطبقة 2: Madlūl Lafẓī Geometry (هندسة المدلول اللفظي)
  MadlulLafziCandidate = Lafẓī Madlūl Fractal Algebra (11 layers)
  ↓
الطبقة 3: Neutral Dal-Madlul Binding (الربط المحايد)
  DalMadlulBindingCandidate ≠ Dalalah ≠ Wadh ≠ Meaning
  [PR-L4 implementation]
  ↓
الطبقة 4: Wadh Geometry (هندسة الوضع)
  WadhClaim + MawduLahStructure
  [PR-L5A + PR-L5B implementation]
  ↓
الطبقة 5: Mutabaqah (المطابقة)
  [PR-L6A implementation]
  ↓
الطبقة 6: Tadammun / Iltizam (التضمن / الالتزام)
  [Planned]
  ↓
الطبقة 7: Full Dalalah (الدلالة الكاملة)
  [Planned]
  ↓
الطبقة 8: Hukm (الحكم)
  [Research-level]
```

### 2. قانون "لا قفز" (No Jumping Law)

```text
❌ ممنوع: صوت → معنى مباشرة
❌ ممنوع: دال → حكم بدون وضع
❌ ممنوع: مدلول لفظي → دلالة كاملة بدون مطابقة

✅ مطلوب: كل طبقة تنتج مخرجًا كاملاً
✅ مطلوب: كل انتقال له عقد (contract) واضح
✅ مطلوب: كل مرشح له rank + residuals + trace
```

### 3. مبدأ الدليل أولاً (Evidence-First)

```text
كل ادعاء يحتاج دليلاً
كل رتبة تحتاج سياسة
كل انتقال يحتاج عقداً
كل بوابة لها شرط تفعيل وشرط إشباع
```

---

## 📊 الحالة الحالية (Status as of 2026-05-23)

### ✅ مكتمل (Completed)

#### Dal Core Layer (A0-A4)
- ✅ **PR #7**: MufradProof Contract
- ✅ **PR #9**: SentenceFrameCandidate
- ✅ **PR #10**: PreSyntaxMufradVector
- ✅ **PR #12**: CaseSignMatrix
- ✅ **PR #14**: OperatorTriggerPotential
- ✅ **PR #16**: NahwOperatorRegistry (immutable)
- ✅ **PR #18**: OperatorCandidate
- ✅ **PR #21**: Ordered Dal Form Governance
- ✅ **PR #22**: Project Algebra Architecture Map

#### FVAFK Pipeline
- ✅ **Sprint 1**: Foundation + ISNADI in CLI (373 tests passing)
- ✅ **Sprint 2**: Phonology gates unification + Coq skeletons
- ✅ **Sprint 3**: Semantic gates + C2B fixes (829 tests)
- ✅ **Sprint 4**: I3rab Parser integration (68 new tests)
- ✅ **C1 → C2a → C2b** pipeline operational
- ✅ **Phonology V2** with lattice + witnesses
- ✅ **WordForm + ISNADI** in CLI output

#### GFA Methods Layer
- ✅ **PR-N1** (PR #56): NeutralBinding implementation
- ✅ **PR-G1**: Memory Geometry Kernel (30/30 tests)
- ✅ **PR-L4** (commit ac1e35b): DalMadlulBindingCandidate (18 tests)
- ✅ **PR-L4.1** (PR #64): Test helper signature fixes (31 tests)
- ✅ **PR-L5A** (PR #65): WadhGeometry definitions (15 tests)
- ✅ **PR-L5B** (commit 6b3120f): WadhGate (22 tests)
- ✅ **PR-L6A** (PR #67): MutabaqahGate hardening (29 tests)
- ✅ **CognitiveCarrier** Layer 0.5 (20 tests)

#### Lafẓī Madlūl Fractal Algebra
- ✅ **11-layer fractal structure** (85/85 tests passing)
- ✅ Complete closure validation across layers
- ✅ Unicode-aware factory methods
- ✅ Auto-detection of root types (quadrilateral/quinqueliteral)

### 🚧 قيد التنفيذ (In Progress)

#### FVAFK Evolution
- 🚧 **L10B**: Clause-span / locality-collapse diagnosis
- 🚧 **L14**: Jamid vs Mushtaq (Pass 1 implemented)
- 🚧 **L17**: Rule-Based Iʿrāb Reasoner (v3 Quranic-aligned)
- 🚧 **Stage 15**: Dependency Syntax Builder (Batch 28.30)
- 🚧 **Stage 16**: Clause Engine (conditional decomposition)

### ❌ غير مبدوء (Not Started - Critical Gap)

#### **PR-L3: Pure Dāl Geometry Contract Hardening** ⚠️

**الأهمية الحرجة**: هذا هو الطبقة المفقودة التي تم تحديدها في التحليل المعماري.

**الهدف**:
```text
بناء كائن الدال المرخّص (DalCandidate) الكامل قبل الربط المحايد
```

**المخرجات المطلوبة**:
1. `src/dal_core/pure_dal_geometry.py`
   - DalCandidate dataclass with full structure
   - Source layer validation (must be PURE_DAL)
   - Signifier rank enforcement (LICENSED | CONTEXTUAL)
   - Hard gates: no meaning, no dalalah, no hukm, no wadh
   - Mandatory trace_id and residuals

2. `src/dal_core/dal_candidate_builder.py`
   - Raw Signal → DalCandidate pipeline
   - Phonic carrier extraction
   - Haraka operation sequencing
   - Syllable license validation
   - Word boundary detection
   - Clitic separation
   - Formula candidate generation
   - Path type classification
   - Pattern status determination
   - Terminal state resolution
   - Syntactic readiness assessment
   - Sentence shape analysis
   - Role projection candidate generation

3. `tests/dal_core/test_pure_dal_geometry.py`
   - Test that DalCandidate contains all required fields
   - Test that no meaning field exists
   - Test that no dalalah field exists
   - Test that no hukm field exists
   - Test that trace is preserved
   - Test that residuals are preserved
   - Test that rank is evidence-based

4. `docs/PURE_DAL_GEOMETRY.md`
   - Complete specification
   - Examples (كتب، كاتب، مكتوب)
   - Distinction from PR-L4 (binding layer)
   - Contract for downstream consumption

**التبعيات**:
- يسبق: PR-L4 (حالياً يقبل DalCandidate ضعيف)
- يعتمد على: A0-A4 Dal layers (موجودة)
- يحجب: PR-L5 (Wadh يجب أن يعمل على دال قوي)

**معيار النجاح**:
```python
# PR-L4 gate enhancement
assert candidate.dal_candidate.source_layer == "PURE_DAL"
assert candidate.dal_candidate.signifier_rank in {"LICENSED", "CONTEXTUAL"}
assert not hasattr(candidate.dal_candidate, "meaning")
assert not hasattr(candidate.dal_candidate, "dalalah")
assert not hasattr(candidate.dal_candidate, "hukm")
assert candidate.dal_candidate.trace_id is not None
assert candidate.dal_candidate.residuals is not None
assert len(candidate.dal_candidate.phonic_carriers) > 0
assert candidate.dal_candidate.syllable_licenses is not None
```

---

## 🗺️ خريطة الطريق الكاملة (Complete Roadmap)

### المسار A: Dal Core Algebra (PR #23-#48+)

**الأولوية**: عالية جداً
**التقدير الزمني**: 12-24 شهر

#### Phase 1: Foundation Algebras (PR #23-#27)

| PR | العنوان | الحالة | المدة المقدرة |
|----|---------|--------|---------------|
| **PR #23** | Minimal Dal Transition Signature | 📋 Planned | 2-3 weeks |
| **PR #24** | Rank Algebra | 📋 Planned | 2 weeks |
| **PR #25** | Residual Algebra | 📋 Planned | 2 weeks |
| **PR #26** | CandidateSet Contract | 📋 Planned | 2 weeks |
| **PR #27** | Stage-Aware NoMeaning Invariant | 📋 Planned | 1 week |

**المخرجات الرئيسية**:
- `dal_algebra.py`: DalDomain (D0-D7), transition contracts
- `rank_algebra.py`: Cross-domain independence
- `residual_algebra.py`: Blocker propagation
- `candidate_set.py`: Bounded generation
- Tests: 50+ new tests

#### Phase 2: Dal Candidate Layers (PR #28-#36)

| PR | Layer | المدة المقدرة |
|----|-------|---------------|
| **PR #28** | OrderedUnit / FormSequence | 1 week |
| **PR #29** | D0: Graphophonemic | 2 weeks |
| **PR #30** | D1: Syllable | 2 weeks |
| **PR #31** | D2: PreMorph | 2 weeks |
| **PR #32** | D3: Origin | 3 weeks |
| **PR #33** | D4: Template | 3 weeks |
| **PR #34** | D5: Identity Axis | 2 weeks |
| **PR #35** | D6: Directional Analysis | 2 weeks |
| **PR #36** | D7: Judgment | 3 weeks |

**التقدير الإجمالي**: 4-6 أشهر

#### Phase 3: Dal-Murakkab Completion (PR #37-#39)

| PR | العنوان | المدة المقدرة |
|----|---------|---------------|
| **PR #37** | RelationCandidate (ISN/TADMN/TAQYID) | 3 weeks |
| **PR #38** | CaseEffectCandidate | 3 weeks |
| **PR #39** | MurakkabProof Closure | 2 weeks |

**التقدير الإجمالي**: 2 شهر

#### Phase 4: Dal-Madlul Boundary (PR #40-#42)

| PR | العنوان | الحالة | المدة المقدرة |
|----|---------|--------|---------------|
| **PR #40** | Wadh' Contract Definition | 📋 Planned | 2 weeks |
| **PR #41** | Lexicon with Wadh' Attestations | 📋 Planned | 3 weeks |
| **PR #42** | Wadh' Transition Implementation | 📋 Planned | 3 weeks |

**التقدير الإجمالي**: 2 شهر

#### Phase 5: Semantic Algebras (PR #43-#47)

| PR | العنوان | المدة المقدرة |
|----|---------|---------------|
| **PR #43** | Madlul Algebra | 3 weeks |
| **PR #44** | Dalalah Algebra (المطابقة/التضمن/الالتزام) | 4 weeks |
| **PR #45** | Usage Algebra (حقيقة/مجاز/نقل) | 3 weeks |
| **PR #46** | Murad Inference Engine | 4 weeks |
| **PR #47** | General Algebra Definition | 2 weeks |

**التقدير الإجمالي**: 4 شهر

#### Phase 6: Verification (PR #48+)

| PR | العنوان | المدة المقدرة |
|----|---------|---------------|
| **PR #48** | Dal-General Inclusion Proof | 3 weeks |
| **PR #49+** | Hukm Algebra (research-level) | TBD |

**التقدير الإجمالي**: 1-2 شهر +

---

### المسار B: FVAFK Pipeline Completion

**الأولوية**: عالية
**التقدير الزمني**: 6-8 أشهر

#### Remaining Sprints (3-6)

| Sprint | الأسابيع | التركيز | الحالة |
|--------|----------|---------|--------|
| **Sprint 3** | 5-6 | Morphology + corpus F1 | 🎯 Next |
| **Sprint 4** | 7-8 | TADMINI/TAQYIDI + parser | Pending |
| **Sprint 5** | 9-10 | Constraints + validator | Pending |
| **Sprint 6** | 11-14 | Integration + eval + ops | Pending |

**المخرجات الرئيسية**:
- WordBoundaryDetector Plan B
- PatternCatalog integration
- TADMINI + TAQYIDI linkers
- SyntacticParser
- 5-6 constraint modules
- ConstraintValidator
- Corpus evaluation (F1, UAS, LAS)
- C2c semantic gate design

---

### المسار C: GFA Methods Evolution

**الأولوية**: حرجة لإكمال السلسلة الدلالية
**التقدير الزمني**: 6-9 أشهر

#### Immediate Priority: PR-L3

**⚠️ يجب أن يسبق كل ما يلي**

| PR | العنوان | الحالة | المدة المقدرة |
|----|---------|--------|---------------|
| **PR-L3** | Pure Dāl Geometry Contract Hardening | ❌ Critical Gap | 3-4 weeks |

#### Continuing Sequence

| PR | العنوان | الحالة | المدة المقدرة |
|----|---------|--------|---------------|
| **PR-L7** | Tadammun Gate | 📋 Planned | 3 weeks |
| **PR-L8** | Iltizam Gate | 📋 Planned | 3 weeks |
| **PR-L9** | Usage Gate (حقيقة/مجاز) | 📋 Planned | 4 weeks |
| **PR-L10** | Full Dalalah Integration | 📋 Planned | 4 weeks |
| **PR-L11** | Hukm Geometry (research) | 📋 Planned | TBD |

---

### المسار D: AGT Formal Framework

**الأولوية**: متوسطة (بحثية)
**التقدير الزمني**: 11-15 أسبوع

#### Extensions (من ROADMAP.md)

| Extension | التركيز | المدة المقدرة |
|-----------|---------|---------------|
| **Extension 1** | Master Theorem Proofs (no axioms) | 2-3 weeks |
| **Extension 2** | Discourse-Compositional Integration | 2-3 weeks |
| **Extension 3** | Complete Sarf Pattern Coverage (50+ patterns) | 3-4 weeks |
| **Extension 4** | Corpus Interface & Empirical Validation | 4-5 weeks |

**المخرجات الرئيسية**:
- Zero axioms for core theorems
- 50+ verb patterns proven
- 30+ noun patterns proven
- ≥90% coverage on Quranic corpus
- ≥85% coverage on MSA corpus

---

## 🔬 معايير النجاح (Success Criteria)

### المعايير التقنية

| المعيار | الهدف | الحالة الحالية | الفجوة |
|---------|-------|----------------|--------|
| **Tests** | ≥ 500 | 829 passing | ✅ تم تجاوزه |
| **Phonology gates** | 10 gates, 100+ tests | 11 gates, many tests | ✅ Complete |
| **Morphology F1** | ≥ 0.85 | Not measured | ❌ Need corpus |
| **Syntax UAS** | ≥ 0.80 | Not measured | ❌ Need implementation |
| **Constraint violations** | 0 on correct text | N/A | ❌ Not started |
| **Coq theorems** | 50+ proven | 3 skeletons | ❌ Need proofs |
| **Performance** | 1000 words/s | Not measured | ❌ Need benchmarks |
| **Documentation** | 50,000+ words | Partial | 🟡 In progress |

### المعايير المعمارية

```text
✅ Pure Dāl Geometry: DalCandidate with all required fields
✅ Neutral Binding: DalMadlulBinding ≠ Dalalah
✅ Wadh Geometry: WadhClaim ≠ external meaning
✅ Mutabaqah Gate: whole of placed-for only
❌ Tadammun/Iltizam: Not yet implemented
❌ Full Dalalah: Not yet implemented
❌ Hukm Algebra: Research-level
```

### معايير الحوكمة

```text
✅ No meaning in Dal-only layers (D0-D7)
✅ No semantic leakage in MufradProof
✅ Trace preservation across all transitions
✅ Residual propagation verified
✅ Evidence-based rank across layers
❌ Cross-domain rank independence (needs PR #24)
❌ Blocker detection systematic (needs PR #25)
```

---

## 📅 الجدول الزمني المقترح (Proposed Timeline)

### الربع الثاني 2026 (Q2 2026) - أبريل-يونيو [الحالي]

**التركيز**: Pure Dāl Geometry + Dal Transition Signature

**ملاحظة**: هذا الجدول يعكس الخطة الحالية اعتباراً من مايو 2026.

- **أسبوع 1-4 (مايو)**: PR-L3 (Pure Dāl Geometry Contract Hardening) ⚠️ **أولوية قصوى**
- **أسبوع 5-7**: PR #23 (Minimal Dal Transition Signature)
- **أسبوع 8-10**: PR #24 (Rank Algebra) + PR #25 (Residual Algebra)
- **أسبوع 11-12**: PR #26 (CandidateSet Contract)

**المخرجات**: DalCandidate كامل + Dal Algebra runtime

### الربع الثالث 2026 (Q3 2026) - يوليو-سبتمبر

**التركيز**: Dal Candidate Layers + FVAFK Syntax

- **أسبوع 1-8**: PR #28-#32 (OrderedUnit → Origin layer)
- **أسبوع 9-12**: FVAFK Sprint 4 (TADMINI/TAQYIDI + parser)

**المخرجات**: D0-D3 layers + Syntax في CLI

### الربع الرابع 2026 (Q4 2026) - أكتوبر-ديسمبر

**التركيز**: Dal Completion + Constraints

- **أسبوع 1-7**: PR #33-#36 (Template → Judgment layers)
- **أسبوع 8-11**: PR #37-#39 (RelationCandidate + MurakkabProof)
- **أسبوع 12**: FVAFK Sprint 5 (Constraints)

**المخرجات**: Dal-Murakkab complete + Constraint validation

### Q1 2027 (يناير-مارس)

**التركيز**: Dal-Madlul Boundary + Integration

**⚠️ مشروط بإكمال PR-L3**: لا يجوز البدء في PR-L5 (Wadh) قبل تقوية DalCandidate

- **أسبوع 1-8**: PR #40-#42 (Wadh' Contract + Implementation) - بعد PR-L3 فقط
- **أسبوع 9-12**: PR-L7, PR-L8 (Tadammun + Iltizam Gates)
- **أسبوع 13-16**: FVAFK Sprint 6 (Integration + corpus eval)

**المخرجات**: Wadh' transition + Full pipeline integration

### 2027 (Year 2) - التوسع

**التركيز**: Semantic Algebras + AGT Extensions + Research

- **Q1**: PR #43-#45 (Madlul + Dalalah + Usage Algebras)
- **Q2**: PR #46-#47 (Murad + General Algebra)
- **Q3**: AGT Extensions 1-3 (Master Theorems + Discourse + Sarf)
- **Q4**: AGT Extension 4 (Corpus Validation) + Hukm Research

---

## 🚨 المخاطر والتخفيف (Risks & Mitigation)

### مخاطر عالية (High Risk)

| المخاطرة | التأثير | الاحتمالية | التخفيف |
|----------|---------|-----------|----------|
| **Pure Dāl Geometry غير مكتمل** | PR-L4 يربط دال ضعيف | عالية | **PR-L3 أولوية قصوى** |
| **Axiom leakage** في GFA | False meaning creation | متوسطة | Hard gates في كل طبقة |
| **Performance bottleneck** | لا يصل 1000 كلمة/ثانية | متوسطة | Profiling + Cython للعمليات الحرجة |
| **Corpus unavailability** | لا يمكن قياس F1/UAS | منخفضة | استخدام Quran + test corpus |

### مخاطر متوسطة (Medium Risk)

| المخاطرة | التأثير | الاحتمالية | التخفيف |
|----------|---------|-----------|----------|
| **Coq proofs عمل مكثف** | تأخير AGT extensions | متوسطة | Admit intermediate lemmas |
| **Integration conflicts** | Breaking changes | متوسطة | Small PRs + CI enforcement |
| **Documentation lag** | Onboarding صعب | متوسطة | Update docs في كل PR |

---

## 🎓 الادعاءات المسموحة والممنوعة (Allowed & Forbidden Claims)

### ✅ ادعاءات مسموحة (بعد الإكمال الكامل)

```text
✅ The project implements a complete typed transition algebra system
   for Arabic linguistic analysis, spanning from graphophonemic
   analysis (D0) through intended meaning inference (A9), with
   documented boundaries and evidence-based governance at every layer.

✅ DalCandidate is the output of Pure Dāl Geometry, carrying full
   signifier structure before semantic interpretation.

✅ DalMadlulBinding creates neutral relation, not Dalalah.

✅ Wadh' requires transmission evidence, not reason alone.

✅ Mutabaqah is whole of placed-for only, not Tadammun/Iltizam.

✅ All transitions preserve trace and residuals.

✅ Rank is evidence-based and domain-scoped.
```

### ❌ ادعاءات ممنوعة (إلى الأبد)

```text
❌ The system understands Arabic.
❌ The system produces perfect semantic interpretation.
❌ The system replaces human judgment.
❌ The system is complete (linguistic analysis is unbounded).
❌ Dal + Madlul = automatic meaning.
❌ High ML confidence = certificate.
❌ Composition raises Mufrad rank automatically.
```

---

## 📚 الوثائق المرجعية (Reference Documents)

### الوثائق الأساسية

1. **docs/PROJECT_ALGEBRA_ROADMAP.md** - Dal Algebra خريطة الطريق
2. **docs/ENHANCED_ROADMAP.md** - FVAFK 6-month plan
3. **docs/architecture/SCIENTIFIC_NEXT_PHASES.md** - FVAFK evolution
4. **ROADMAP.md** - AGT extensions
5. **docs/PR_STATUS_INDEX.md** - PR number mapping
6. **docs/ROADMAP_GOVERNANCE.md** - Governance rules

### الوثائق الفنية

1. **docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md** - A0-A10 architecture
2. **docs/TYPED_TRANSITION_ALGEBRA_KERNEL.md** - Core algebra
3. **docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md** - A3-A4 position
4. **docs/GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md** - A1-A2 boundary
5. **docs/PURE_DAL_GEOMETRY.md** - **يجب إنشاؤه في PR-L3**

### الوثائق التنفيذية

1. **docs/PR_L4_DAL_MADLUL_BINDING_SUMMARY.md** - L4 implementation
2. **docs/PR_L5A_WADH_GEOMETRY_SUMMARY.md** - L5A definitions
3. **docs/PR_L5B_WADH_GATE_SUMMARY.md** - L5B gate
4. **docs/PR_L6A_MUTABAQAH_GATE_SUMMARY.md** - L6A mutabaqah

---

## 🔄 التحديثات والحوكمة (Updates & Governance)

### متى يجب تحديث هذه الخطة؟

1. **عند إكمال PR رئيسي** → تحديث الحالة + نقل من Planned إلى ✅
2. **عند اكتشاف فجوة معمارية** → إضافة PR جديد مع أولوية
3. **عند تغيير التقديرات الزمنية** → تحديث الجداول
4. **كل ربع سنة** → مراجعة شاملة للتقدم

### من يملك هذه الوثيقة؟

- **المالك**: فريق المشروع
- **المراجعين**: Architecture team + Domain experts
- **الموافقون**: Project leads

### عملية التحديث

1. إنشاء PR مع التحديثات المقترحة
2. مراجعة من فريق Architecture
3. موافقة من lead
4. دمج + إشعار الفريق

---

## 🎯 الخطوات التالية الفورية (Immediate Next Actions)

### الأولوية القصوى (This Week)

1. **إنشاء PR-L3: Pure Dāl Geometry Contract Hardening**
   - إنشاء `src/dal_core/pure_dal_geometry.py`
   - تعريف DalCandidate كامل
   - إنشاء اختبارات الحماية (meaning/dalalah/hukm forbidden)
   - كتابة `docs/PURE_DAL_GEOMETRY.md`

2. **تحديث PR-L4 مع Pure Dāl gates**
   - إضافة assertions على DalCandidate
   - فحص source_layer = PURE_DAL
   - فحص signifier_rank ∈ {LICENSED, CONTEXTUAL}

### الأسبوع القادم

3. **بدء PR #23: Minimal Dal Transition Signature**
   - تعريف DalDomain enum
   - تعريف DalTransitionContract protocol
   - تعريف DalEvidence + DalTrace models

4. **إنهاء FVAFK Sprint 3**
   - WordBoundaryDetector Plan B
   - PatternCatalog integration
   - Corpus evaluation script

### الشهر القادم

5. **PR #24 + PR #25** (Rank + Residual Algebras)
6. **FVAFK Sprint 4** (TADMINI/TAQYIDI)
7. **AGT Extension 1** (Master Theorem Proofs)

---

## 📊 لوحة المتابعة (Dashboard)

### التقدم الإجمالي

```
Dal Core (PR #7-#48):        [████████░░░░░░░░░░] 40% (9/23 PRs)
FVAFK Pipeline (Sprint 1-6): [████████████████░░] 67% (4/6 Sprints)
GFA Methods (PR-N1 to L11):  [████████████░░░░░░] 64% (7/11 PRs)
AGT Framework (Ext 1-4):     [███░░░░░░░░░░░░░░░] 20% (Foundation only)
```

### الإحصائيات الرئيسية

- **Total Tests**: 829 passing + 16 skipped
- **Coq Modules**: 11 modules (~9,540 lines)
- **Theorems Proven**: 193+ (AGT) + 3 skeletons (FVAFK)
- **Documentation**: ~100,000+ words across all docs
- **Active PRs**: TBD
- **Merged PRs**: 73+

---

## 🌟 الرؤية طويلة المدى (Long-Term Vision)

### 2026: الأساس
- Dal-only layers (A2-A4) كاملة
- Pure Dāl Geometry راسخة
- FVAFK pipeline متكامل
- GFA Methods chain (L4-L6) مكتملة

### 2027: الدلالة
- Semantic algebras (A6-A9) مُنفذة
- Tadammun/Iltizam/Usage gates عاملة
- Murad inference operational
- Corpus validation على 90%+ coverage

### 2028+: البحث والتطبيقات
- Hukm Algebra (research-level)
- Cross-linguistic extensions
- Educational applications
- Production deployment
- Community contributions

---

**النسخة**: 1.0.0
**تاريخ آخر تحديث**: 2026-05-23
**الحالة**: نشطة وموحدة
**المراجعة القادمة**: 2026-08-23 (Q3 review)

---

*هذه الوثيقة هي المرجع الوحيد لخطة المشروع. كل الوثائق الأخرى يجب أن تشير إليها.*
*This document is the single source of truth for the project plan. All other documents should reference it.*
