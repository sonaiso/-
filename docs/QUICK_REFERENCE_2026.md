# مرجع سريع للمشروع 2026
# Project Quick Reference 2026

**آخر تحديث**: 2026-05-23

---

## 🎯 الوثيقة الرئيسية

**المرجع الوحيد لكل شيء**:
👉 **[docs/MASTER_PROJECT_PLAN_2026.md](./MASTER_PROJECT_PLAN_2026.md)** 👈

---

## 🚀 أين أبدأ؟

### للمطورين الجدد

1. اقرأ [README.md](../README.md) للنظرة العامة
2. اقرأ **[MASTER_PROJECT_PLAN_2026.md](./MASTER_PROJECT_PLAN_2026.md)** للخطة الكاملة
3. اقرأ [PROJECT_STATUS.md](./PROJECT_STATUS.md) للحالة الحالية
4. اختر مسارًا للمساهمة

### للمراجعين

1. راجع [PR_STATUS_INDEX.md](./PR_STATUS_INDEX.md) لرسم خريطة أرقام PR
2. اتبع [ROADMAP_GOVERNANCE.md](./ROADMAP_GOVERNANCE.md) للقواعد

### للباحثين

1. اطلع على [ROADMAP.md](../ROADMAP.md) لـ AGT extensions
2. راجع `coq/` directory للنظريات الرسمية

---

## 📊 الأولويات الحالية (مايو 2026)

### ⚠️ أولوية قصوى (هذا الأسبوع)

**PR-L3: Pure Dāl Geometry Contract Hardening**

```text
WHY: فجوة معمارية حرجة - PR-L4 يربط دال غير مكتمل
WHAT: بناء DalCandidate كامل مع كل الحقول المطلوبة
WHERE: src/dal_core/pure_dal_geometry.py
WHEN: هذا الأسبوع
WHO: Dal Core team
```

**الملفات المطلوبة**:
- [ ] `src/dal_core/pure_dal_geometry.py`
- [ ] `src/dal_core/dal_candidate_builder.py`
- [ ] `tests/dal_core/test_pure_dal_geometry.py`
- [ ] `docs/PURE_DAL_GEOMETRY.md`

### أولويات الأسبوع القادم

1. **تحديث PR-L4** مع Pure Dāl gates
2. **بدء PR #23**: Minimal Dal Transition Signature
3. **إنهاء FVAFK Sprint 3**: Morphology + corpus

---

## 🗺️ المسارات الأربعة

### المسار A: Dal Core Algebra
- **الحالة**: PR #7-#22 مكتمل، PR #23-#48+ مخطط
- **الأولوية**: عالية جداً
- **الوثيقة**: [PROJECT_ALGEBRA_ROADMAP.md](./PROJECT_ALGEBRA_ROADMAP.md)

### المسار B: FVAFK Pipeline
- **الحالة**: Sprint 1-4 مكتمل، Sprint 5-6 قيد الانتظار
- **الأولوية**: عالية
- **الوثيقة**: [ENHANCED_ROADMAP.md](./ENHANCED_ROADMAP.md)

### المسار C: GFA Methods
- **الحالة**: PR-N1 إلى PR-L6A مكتمل، PR-L3 فجوة حرجة
- **الأولوية**: حرجة (PR-L3)
- **الوثيقة**: [MASTER_PROJECT_PLAN_2026.md](./MASTER_PROJECT_PLAN_2026.md) - المسار C

### المسار D: AGT Framework
- **الحالة**: Foundation مكتمل، Extensions 1-4 مخطط
- **الأولوية**: متوسطة (بحثية)
- **الوثيقة**: [ROADMAP.md](../ROADMAP.md)

---

## 📈 الإحصائيات السريعة

```
Tests:          829 passing + 16 skipped
Coq Lines:      ~9,540 (11 modules)
Theorems:       193+ proven
PRs Merged:     73+
PRs Planned:    48+ (Dal Core alone)
Documentation:  100,000+ words
```

---

## 🏗️ الطبقات المعمارية

```
L0: Raw Signal (الإشارة الخام)
  ↓
L1: Pure Dāl Geometry (هندسة الدال وحده) ← PR-L3 مفقود ⚠️
  ↓
L2: Madlūl Lafẓī (المدلول اللفظي) ← 85/85 tests ✅
  ↓
L3: Neutral Binding (الربط المحايد) ← PR-L4 ✅
  ↓
L4: Wadh Geometry (هندسة الوضع) ← PR-L5A + PR-L5B ✅
  ↓
L5: Mutabaqah (المطابقة) ← PR-L6A ✅
  ↓
L6: Tadammun/Iltizam ← Planned
  ↓
L7: Full Dalalah ← Planned
  ↓
L8: Hukm ← Research
```

---

## 🎓 القوانين الذهبية

### ممنوع (FORBIDDEN)

```text
❌ Dal + Madlul = automatic meaning
❌ Jumping layers (صوت → معنى مباشرة)
❌ Meaning fields in Dal-only layers
❌ High ML confidence = certificate
❌ Composition raises Mufrad rank
```

### مطلوب (REQUIRED)

```text
✅ Every claim needs evidence
✅ Every rank needs policy
✅ Every transition needs contract
✅ Every candidate has trace + residuals
✅ DalCandidate must be PURE_DAL output
```

---

## 📚 الوثائق الأساسية

### خرائط الطريق

| وثيقة | الوصف |
|------|-------|
| **[MASTER_PROJECT_PLAN_2026.md](./MASTER_PROJECT_PLAN_2026.md)** | 🔥 **المرجع الوحيد** - الخطة الموحدة |
| [PROJECT_ALGEBRA_ROADMAP.md](./PROJECT_ALGEBRA_ROADMAP.md) | Dal Core (PR #22-#48+) |
| [ENHANCED_ROADMAP.md](./ENHANCED_ROADMAP.md) | FVAFK 6-month plan |
| [ROADMAP.md](../ROADMAP.md) | AGT extensions |

### الحالة

| وثيقة | الوصف |
|------|-------|
| [PROJECT_STATUS.md](./PROJECT_STATUS.md) | Current progress (829 tests) |
| [PR_STATUS_INDEX.md](./PR_STATUS_INDEX.md) | PR number mapping |
| [WHERE_WE_ARE_VS_PLAN.md](./WHERE_WE_ARE_VS_PLAN.md) | Gap analysis |

### المعمارية

| وثيقة | الوصف |
|------|-------|
| [PROJECT_ALGEBRA_ARCHITECTURE_MAP.md](./PROJECT_ALGEBRA_ARCHITECTURE_MAP.md) | A0-A10 layers |
| [TYPED_TRANSITION_ALGEBRA_KERNEL.md](./TYPED_TRANSITION_ALGEBRA_KERNEL.md) | Core algebra |
| [DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md](./DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md) | A3-A4 |
| **[PURE_DAL_GEOMETRY.md](./PURE_DAL_GEOMETRY.md)** | ⚠️ يجب إنشاؤه في PR-L3 |

### التنفيذ

| وثيقة | الوصف |
|------|-------|
| [PR_L4_DAL_MADLUL_BINDING_SUMMARY.md](./PR_L4_DAL_MADLUL_BINDING_SUMMARY.md) | Neutral binding |
| [PR_L5A_WADH_GEOMETRY_SUMMARY.md](./PR_L5A_WADH_GEOMETRY_SUMMARY.md) | Wadh definitions |
| [PR_L5B_WADH_GATE_SUMMARY.md](./PR_L5B_WADH_GATE_SUMMARY.md) | Wadh gate |
| [PR_L6A_MUTABAQAH_GATE_SUMMARY.md](./PR_L6A_MUTABAQAH_GATE_SUMMARY.md) | Mutabaqah |

---

## 🔧 أوامر سريعة

### Testing

```bash
# Run all tests
pytest -v

# Run specific layer
pytest tests/dal_core/ -v
pytest tests/gfa/methods/ -v
pytest tests/fvafk/algebra/ -v

# Run with coverage
pytest --cov=src --cov-report=html
```

### FVAFK CLI

```bash
# Basic analysis
python -m fvafk.cli "كَتَبَ" --morphology

# With phonology
python -m fvafk.cli "كَتَبَ" --phonology-v2

# JSON output
python -m fvafk.cli "كَتَبَ" --morphology --json
```

### Coq

```bash
# Compile theories
make -C coq

# Check specific file
coqc coq/AGT_Core.v
```

---

## 🆘 أين أحصل على المساعدة؟

### للأسئلة الفنية

1. اطلع على [docs/](./README.md) للوثائق الكاملة
2. راجع [tests/](../tests/) للأمثلة
3. افتح issue في GitHub

### للمساهمات

1. اقرأ **[MASTER_PROJECT_PLAN_2026.md](./MASTER_PROJECT_PLAN_2026.md)**
2. اختر PR من القائمة
3. راجع [ROADMAP_GOVERNANCE.md](./ROADMAP_GOVERNANCE.md)
4. أنشئ branch وافتح PR

### للبحث

1. اطلع على [ROADMAP.md](../ROADMAP.md) - AGT Extensions
2. راجع `coq/` للنظريات الحالية
3. تواصل مع البحث team

---

## 🎯 الأهداف قصيرة المدى (Q2 2026)

```
✅ PR-L3: Pure Dāl Geometry (أسبوع 1-4)
✅ PR #23: Dal Transition Signature (أسبوع 5-7)
✅ PR #24-25: Rank + Residual (أسبوع 8-10)
✅ PR #26: CandidateSet (أسبوع 11-12)
```

---

## 📅 الجدول الزمني

### Q1 2026 (الآن)
- Pure Dāl Geometry + Dal Transition Signature

### Q2 2026
- Dal Candidate Layers + FVAFK Syntax

### Q3 2026
- Dal Completion + Constraints

### Q4 2026
- Dal-Madlul Boundary + Integration

### 2027
- Semantic Algebras + AGT Extensions + Research

---

**نسخة**: 1.0.0
**آخر تحديث**: 2026-05-23

---

*للحصول على التفاصيل الكاملة، راجع دائمًا [MASTER_PROJECT_PLAN_2026.md](./MASTER_PROJECT_PLAN_2026.md)*
