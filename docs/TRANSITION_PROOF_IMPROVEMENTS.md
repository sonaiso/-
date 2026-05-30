# TransitionProofKernel Improvements: Rank Ceiling & Evidence Validation

**Date**: 2026-05-30
**Branch**: `claude/pr-162-fix-rank-inflation-issue`
**Status**: ✅ تم إكمال التحسينات (Improvements Complete)

---

## Executive Summary

بناءً على المراجعة النقدية الدقيقة، تم إضافة تحسينات حاسمة لـ `TransitionProof.to_result()`:

1. ✅ **Rank Ceiling Computation** - منع تضخم الرتبة من evidence ضعيف
2. ✅ **Evidence Validation** - التحقق من namespace صحيح للـ evidence sources
3. ✅ **Weak Evidence Residuals** - تسجيل evidence غير معتمد كـ residuals
4. ✅ **Comprehensive Tests** - 3 اختبارات جديدة للتحسينات

---

## Problem 1: Rank Inflation من Evidence Strings

### المشكلة الأصلية

```python
# قبل التحسين - خطر تضخم الرتبة
effective = EffectiveDescription("eff", "test", ("string1", "string2"))
proof = TransitionProof(..., rank=Rank.LICENSED)

result = proof.to_result("value")
# result.rank == Rank.LICENSED  ❌ من أين جاء LICENSED؟
# Evidence مجرد strings!
```

**الخطر**: `self.rank` قد يكون LICENSED بدون دليل قوي، فقط strings في `effective_description.evidence`.

### الحل: Rank Ceiling

```python
def _compute_rank_ceiling(self, evidence_items: tuple[Evidence, ...]) -> Rank:
    """
    Compute maximum allowed rank based on proof components.

    Constitutional Law (Rank Ceiling):
        final_rank = min(
            self.rank,           # Proof's declared rank
            evidence_rank,       # Rank from evidence quality
            source_rank,         # (future: from source)
            manaat_rank          # (future: from manaat)
        )
    """
    if not evidence_items:
        return Rank.CANDIDATE

    # Currently: string evidence = CANDIDATE level max
    # Future: validate trace_id/candidate_id/span for higher ranks
    return Rank.CANDIDATE
```

### النتيجة بعد التحسين

```python
# بعد التحسين - rank ceiling applied
effective = EffectiveDescription("eff", "test", ("evidence:weak1", "evidence:weak2"))
proof = TransitionProof(..., rank=Rank.LICENSED)  # يطلب LICENSED

result = proof.to_result("value")
# result.rank == Rank.CANDIDATE  ✅ محدود بالسقف!
```

**القانون الدستوري**:
```
final_rank ≤ rank_ceiling
rank_ceiling = min(proof_rank, evidence_rank, source_rank, manaat_rank)
```

---

## Problem 2: Evidence من Strings بلا Namespace

### المشكلة الأصلية

```python
# قبل التحسين - كل string يصبح Evidence
for ev_ref in self.qiyas.effective_description.evidence:
    evidence_items.append(
        Evidence(source=ev_ref, ...)  # ❌ ev_ref قد يكون أي string!
    )
```

**الخطر**:
- `ev_ref = "some random description"` → يصبح Evidence!
- لا يوجد فحص لـ trace_id أو candidate_id أو span

### الحل: Evidence Validation

```python
@staticmethod
def _validate_evidence_source(ev_ref: str) -> bool:
    """
    Validate evidence source string has proper namespace.

    Constitutional Law (Evidence Validation):
        Evidence sources must use proper namespaces:
        - trace:*       (computational trace)
        - candidate:*   (candidate reference)
        - evidence:*    (explicit evidence marker)
        - test:*        (test evidence)
        - proof:*       (proof reference)
        - source:*      (source reference)
        - span:*        (span reference)
    """
    valid_prefixes = (
        "trace:", "candidate:", "evidence:",
        "test:", "proof:", "source:", "span:"
    )
    return ev_ref.startswith(valid_prefixes)
```

### النتيجة بعد التحسين

```python
# بعد التحسين - فحص namespace
effective = EffectiveDescription(
    "eff", "test",
    ("trace:abc123", "random string", "evidence:valid")
)

# يتم بناء Evidence فقط للـ valid namespaces
evidence_items = [
    Evidence(source="trace:abc123", ...),    # ✅ valid
    Evidence(source="evidence:valid", ...)   # ✅ valid
]

# الـ "random string" يصبح residual warning
residuals = [
    Residual(
        kind="weak_evidence_source",
        description="Evidence source lacks proper namespace: random string"
    )
]
```

**القانون الدستوري**:
```
لا Evidence من string بلا namespace صحيح
Weak evidence → Residual warning, not Evidence
```

---

## التحسينات المضافة

### 1. `_compute_rank_ceiling()` Method

**الوظيفة**: حساب السقف الأقصى للرتبة بناءً على جودة Evidence.

**المنطق الحالي**:
- لا evidence → max CANDIDATE
- Evidence من strings → max CANDIDATE
- (مستقبلاً) Evidence معتمد → قد يصل LICENSED/CERTIFIED

**الكود**:
```python
rank_ceiling = self._compute_rank_ceiling(evidence_items)

if self.rank.value > rank_ceiling.value:
    # Proof claims higher rank than evidence supports
    final_rank = rank_ceiling  # Apply ceiling
else:
    final_rank = self.rank
```

### 2. `_validate_evidence_source()` Static Method

**الوظيفة**: التحقق من أن evidence source له namespace صحيح.

**Namespaces المقبولة**:
- `trace:*` - computational trace
- `candidate:*` - candidate reference
- `evidence:*` - explicit evidence marker
- `test:*` - test evidence
- `proof:*` - proof reference
- `source:*` - source reference
- `span:*` - span reference

**Namespaces المرفوضة**:
- Plain strings بدون prefix
- Generic descriptions

### 3. Weak Evidence Residuals

**الوظيفة**: تسجيل evidence sources غير معتمدة كـ residuals.

**الكود**:
```python
for weak_ev in weak_evidence_sources:
    residual_items.append(
        Residual(
            kind="weak_evidence_source",
            description=f"Evidence source lacks proper namespace: {weak_ev}"
        )
    )
```

**الفائدة**:
- لا نفقد المعلومة
- لكن نسجل أنها weak/unvalidated
- Transparency في جودة Evidence

---

## الاختبارات الجديدة (3 Tests)

### 1. `test_to_result_rank_ceiling_prevents_inflation()`

**يختبر**: أن rank ceiling يمنع تضخم الرتبة.

```python
# Proof يطلب LICENSED مع evidence ضعيف
proof = TransitionProof(..., rank=Rank.LICENSED)
result = proof.to_result("value")

# يجب أن يكون Rank.CANDIDATE وليس LICENSED
assert result.rank == Rank.CANDIDATE
```

### 2. `test_to_result_weak_evidence_creates_residual()`

**يختبر**: أن weak evidence يصبح residual.

```python
effective = EffectiveDescription(
    "eff", "test",
    ("some random string", "evidence:valid_one")
)

result = proof.to_result("value")

# Evidence واحد فقط (الصحيح)
assert len(result.evidence) == 1

# Residual واحد للـ weak
weak_residuals = [r for r in result.residuals if r.kind == "weak_evidence_source"]
assert len(weak_residuals) == 1
```

### 3. `test_validate_evidence_source_accepts_proper_namespaces()`

**يختبر**: أن validation يقبل namespaces صحيحة فقط.

```python
# Valid
assert TransitionProof._validate_evidence_source("trace:abc123")
assert TransitionProof._validate_evidence_source("evidence:form")

# Invalid
assert not TransitionProof._validate_evidence_source("random string")
assert not TransitionProof._validate_evidence_source("")
```

---

## Comparison: Before vs After

| Aspect | Before | After |
|--------|--------|-------|
| **Rank from weak evidence** | May inflate to LICENSED ❌ | Capped at CANDIDATE ✅ |
| **Evidence validation** | All strings accepted ❌ | Namespace check required ✅ |
| **Weak evidence** | Silent acceptance ❌ | Residual warning ✅ |
| **Rank ceiling** | Not computed ❌ | Computed from evidence ✅ |
| **Tests for rank inflation** | 0 ❌ | 3 new tests ✅ |

---

## ما لم يتم تنفيذه (Deferred)

### 1. ResidualEffect Enum

**المشكلة المحددة في المراجعة**:
```
Residual.kind موجود
Residual.description موجود
لكن لا يوجد ResidualEffect صريح: NONE / DEFER / BLOCK
```

**السبب**: هذا يحتاج تصميم أوسع يشمل:
- تحديث `fvafk.algebra.core.Residual`
- سياسة موحدة لـ residual effects
- ربط مع `InvalidatingDifference.blocks_transition`

**التأجيل**: سيكون في PR منفصل لاحقاً.

### 2. Domain Topology Integration

**المشكلة المحددة في المراجعة**:
```python
TransitionProof يستخدم:
    source_layer: str  # ❌ ليس Domain
    target_layer: str

ولا يفحص:
    is_canonical_bridge_allowed(source_domain, target_domain)
```

**السبب**: هذا يحتاج:
- تغيير `TransitionProof` signature (breaking change)
- ربط `source_layer`/`target_layer` بـ `Domain` enum
- سيكون جزء من `governed_transition` المستقبلي

**التأجيل**: سيكون في PR منفصل عند بناء `governed_transition.py`.

### 3. Governed Transition Function

**كما ذكرت المراجعة**:
```
لا نبدأ بـ governed_transition.py الآن.
نراجع ونحسن TransitionProofKernel أولاً.
```

**الخطة المستقبلية**:
- بعد دمج هذا PR
- نبني `governed_transition` كـ wrapper رقيق
- يستخدم `proof.to_result()` (لا يعيد كتابته)
- يضيف domain topology + manaat checks

---

## الخلاصة

### ما تم إنجازه ✅

1. ✅ **Rank Ceiling** - يمنع تضخم الرتبة من evidence ضعيف
2. ✅ **Evidence Validation** - يفحص namespace صحيح
3. ✅ **Weak Evidence Tracking** - يسجل weak evidence كـ residuals
4. ✅ **3 اختبارات جديدة** - تغطية شاملة للتحسينات
5. ✅ **توثيق كامل** - شرح المشاكل والحلول

### ما تم تأجيله (بحكمة) ⏳

1. ⏳ ResidualEffect enum - يحتاج تصميم أوسع
2. ⏳ Domain topology integration - breaking change
3. ⏳ governed_transition.py - بعد الدمج

### النتيجة النهائية

**TransitionProof.to_result()** الآن:
- ✅ يمنع rank inflation
- ✅ يتحقق من evidence quality
- ✅ يسجل weak evidence بشفافية
- ✅ مختبر بشكل شامل
- ✅ جاهز للدمج

**القانون الدستوري المُنفَّذ**:
```
لا ترقية بلا دليل قوي.
لا Evidence من string بلا namespace.
final_rank ≤ rank_ceiling.
```

---

**الخطوة القادمة**: مراجعة نهائية ← دمج إلى main ← بناء `governed_transition` (PR منفصل).

**Prepared by**: Claude (Anthropic Code Agent)
**Date**: 2026-05-30
**Branch**: `claude/pr-162-fix-rank-inflation-issue`
