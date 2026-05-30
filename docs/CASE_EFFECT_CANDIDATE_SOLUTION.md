# حل الفجوة: طبقة مرشح الأثر الإعرابي

## الحل Solution (المستودع الآن مكتمل بعد هذا التنفيذ)

تاريخ: 2026-05-30

## الملخص التنفيذي

المستودع كان قد عالج المراحل التمهيدية للعامل والإعراب لكنه لم يصل إلى معادلة الإعراب التنفيذية النهائية. **هذا الحل يغلق تلك الفجوة.**

---

## 1. ما كان موجودًا؟

السلسلة الموجودة قبل هذا الحل:

```
PreSyntaxMufradVector
→ SentenceFrameCandidate
→ CaseSignMatrix
→ OperatorTriggerPotential
→ NahwOperatorRegistry
→ OperatorCandidate
→ FactorMarkEquation
```

**المشكلة**: السلسلة توقفت عند `FactorMarkEquation` دون إنتاج `CaseEffectCandidate`.

---

## 2. ما كانت الفجوة؟

### الطبقة المفقودة

لم يكن هناك طبقة تربط:

```
OperatorCandidate
+
RelationCandidate (مستقبلي)
+
FactorMarkEquation
+
CaseSignMatrixRow
→
CaseEffectCandidate
```

أي لم نصل بعد إلى:

> **هذا العامل أثّر في هذا المعمول بهذا الأثر الإعرابي المرشح**

بل كنا عند:

> **هذا العامل محتمل، وهذه العلامة متوافقة، وهذه معادلة عامل/علامة مرشحة**

---

## 3. الحل المُنفذ

### ملف جديد: `src/dal_core/case_effect_candidate.py`

الحل يضيف الطبقة المفقودة التي:

1. **تربط العامل المرشح** (`OperatorCandidate`) **بالأثر الإعرابي المرشح**
2. **تستهلك**:
   - `OperatorCandidate` (من PR #17)
   - `FactorMarkEquation` (من PR #158/#159)
   - `CaseSignMatrixRow` (من PR #13)
3. **تنتج**: `CaseEffectCandidate` (مرشح الأثر الإعرابي)

### المعمارية الكاملة بعد الحل

```
PreSyntaxMufradVector
↓
SentenceFrameCandidate
↓
CaseSignMatrix                    (PR #13)
↓
OperatorTriggerPotential          (PR #14)
↓
NahwOperatorRegistry              (PR #15)
↓
OperatorCandidate                 (PR #17)
↓
FactorMarkEquation                (PR #158/#159)
↓
CaseEffectCandidate               ✅ NEW (هذا الحل)
↓
[future] AmilMamulEquation
↓
[future] RoleEquation
```

---

## 4. ما يضيفه الحل؟

### 4.1 الكائنات الجديدة

#### (أ) `CaseEffectCandidateType` (نوع مرشح الأثر الإعرابي)

```python
class CaseEffectCandidateType(Enum):
    RAFʿ_EFFECT_CANDIDATE = "raf_effect_candidate"
    NASB_EFFECT_CANDIDATE = "nasb_effect_candidate"
    JARR_EFFECT_CANDIDATE = "jarr_effect_candidate"
    JAZM_EFFECT_CANDIDATE = "jazm_effect_candidate"
    BUILDING_EFFECT_CANDIDATE = "building_effect_candidate"
    ESTIMATED_EFFECT_CANDIDATE = "estimated_effect_candidate"
    DEFERRED_EFFECT_CANDIDATE = "deferred_effect_candidate"
    BLOCKED_EFFECT_CANDIDATE = "blocked_effect_candidate"
```

**مهم**: هذه **مرشحات** لا أحكام نهائية.

#### (ب) `CaseEffectCandidate` (مرشح الأثر الإعرابي)

```python
@dataclass(frozen=True)
class CaseEffectCandidate:
    case_effect_id: str
    operator_candidate_id: str
    factor_equation_id: str
    effect_type: CaseEffectCandidateType
    operator_candidate: OperatorCandidate
    factor_source: FactorSourceCandidate
    affected_vector: PreSyntaxMufradVector
    matrix_row: CaseSignMatrixRow
    factor_equation: FactorMarkEquation
    compatibility_evidence: tuple[CaseCompatibilityFamily, ...]
    policy_family: CaseEffectPolicyFamily
    rank: LughaRank
    inherited_residuals: tuple[Residual, ...]
    case_effect_residuals: tuple[Residual, ...]
    trace: CaseEffectCandidateTrace

    # Constitutional guards (ALWAYS False)
    produces_final_case_effect: bool = False
    produces_final_syntax_role: bool = False
    produces_meaning: bool = False
    produces_ifadah: bool = False
    produces_hukm: bool = False
```

#### (ج) `build_case_effect_candidate` (الدالة البانية)

```python
def build_case_effect_candidate(
    operator_candidate: OperatorCandidate,
    factor_equation: FactorMarkEquation,
    matrix_row: CaseSignMatrixRow,
) -> CaseEffectCandidate:
    """
    Build one case effect candidate from operator candidate, factor equation,
    and matrix row.

    GOVERNING RULES:
    1. Accepts only OperatorCandidate, FactorMarkEquation, CaseSignMatrixRow
    2. Reads policy family from operator_candidate.registry_entry
    3. Reads compatibility from matrix_row.compatibility_families
    4. Determines effect type via policy + compatibility + equation type
    5. Produces CANDIDATE only, never final case effect
    6. Preserves all identities (operator, factor, affected)
    7. Candidate rank: rank ≤ min(operator.rank, equation.rank, row.rank)
    8. Residual inheritance: case_effect.inherited_residuals ⊇
       operator.get_all_residuals()
    9. Constitutional law: NO final case_effect, NO meaning, NO ifadah, NO hukm
    """
```

### 4.2 القوانين الدستورية المُطبقة

الكائن `CaseEffectCandidate` يطبق جميع القوانين الدستورية:

1. **لا حكم إعرابي نهائي**:
   - `produces_final_case_effect: bool = False` (ثابت)
   - لا يوجد حقول `marfoo`, `mansub`, `majroor`, `majzum` بدون لاحقة `_candidate`

2. **لا دور نحوي نهائي**:
   - `produces_final_syntax_role: bool = False` (ثابت)
   - لا يوجد حقول `faail`, `mafool`, `mubtada`, `khabar` بدون لاحقة `_candidate`

3. **لا معنى**:
   - `produces_meaning: bool = False` (ثابت)
   - لا يوجد حقول `meaning`, `semantic`, `madlul`, `murad`, `haqiqa`, `majaz`

4. **لا إفادة**:
   - `produces_ifadah: bool = False` (ثابت)
   - لا يوجد حقول `ifadah`, `ifadah_complete`, `pragmatic_completion`

5. **لا حُكم**:
   - `produces_hukm: bool = False` (ثابت)
   - لا يوجد حقول `hukm`, `hukm_final`, `judgment`, `judgment_complete`

6. **حفظ الهوية**:
   - هوية العامل محفوظة (عبر `operator_candidate`)
   - هوية العامل المصدري محفوظة (عبر `factor_source.identity_ids`)
   - هوية المعمول محفوظة (عبر `affected_vector.identity_ids`)

7. **سقف الرتبة**:
   - `rank ≤ min(operator.rank, equation.rank, matrix_row.rank)`

8. **وراثة المخلفات**:
   - `inherited_residuals ⊇ operator.get_all_residuals()`

### 4.3 خوارزمية تحديد نوع الأثر

الدالة `_determine_effect_type` تطبق المنطق التالي:

```
Input:
  - policy_family (from NahwOperatorEntry)
  - compatibility_families (from CaseSignMatrixRow)
  - equation_type (from FactorMarkEquation)

Logic:
  1. If BUILDING_COMPATIBLE in compatibility → BUILDING_EFFECT_CANDIDATE
  2. If equation_type == DEFERRED → DEFERRED_EFFECT_CANDIDATE
  3. If policy == RAFI_POLICY:
       If RAFA_COMPATIBLE in compatibility → RAFʿ_EFFECT_CANDIDATE
       Else → BLOCKED_EFFECT_CANDIDATE
  4. If policy == NASB_POLICY:
       If NASB_COMPATIBLE in compatibility → NASB_EFFECT_CANDIDATE
       Else → BLOCKED_EFFECT_CANDIDATE
  5. If policy == JARR_POLICY:
       If JARR_COMPATIBLE in compatibility → JARR_EFFECT_CANDIDATE
       Else → BLOCKED_EFFECT_CANDIDATE
  6. If policy == JAZM_POLICY:
       If JAZM_COMPATIBLE in compatibility → JAZM_EFFECT_CANDIDATE
       Else → BLOCKED_EFFECT_CANDIDATE
  7. If policy == MIXED_RAFI_NASB_POLICY:
       If RAFA_COMPATIBLE in compatibility → RAFʿ_EFFECT_CANDIDATE
       Elif NASB_COMPATIBLE in compatibility → NASB_EFFECT_CANDIDATE
       Else → BLOCKED_EFFECT_CANDIDATE
  8. If policy == NO_CASE_EFFECT_POLICY → DEFERRED_EFFECT_CANDIDATE

Output: (effect_type, residuals)
```

---

## 5. الاختبارات المُضافة

### ملف جديد: `tests/dal_core/test_case_effect_candidate.py`

الاختبارات تغطي:

1. **الحراس الدستورية**: `test_case_effect_candidate_constitutional_guards`
2. **الحقول المحظورة**: `test_case_effect_candidate_forbidden_fields`
3. **حفظ الهوية**: `test_case_effect_candidate_identity_preservation`
4. **سقف الرتبة**: `test_case_effect_candidate_rank_ceiling`
5. **وراثة المخلفات**: `test_case_effect_candidate_residual_inheritance`
6. **بناء مرشح رفع**: `test_build_case_effect_candidate_rafa`
7. **تعارض التوافق**: `test_build_case_effect_candidate_compatibility_conflict`
8. **مرشح مؤجل**: `test_build_case_effect_candidate_deferred_missing_mark`
9. **مرشح بناء**: `test_build_case_effect_candidate_building_compatible`
10. **تناسق الأثر**: `test_case_effect_candidate_trace_consistency`

---

## 6. ما يبقى للمستقبل؟

بعد هذا الحل، الطبقات المتبقية هي:

### أ) طبقات الجسور المتبقية

1. **EstimatedMarkEquation** (معادلة العلامة المقدرة)
   - للعلامات المقدرة/المحذوفة (تعذر، ثقل، بناء)

2. **ReferenceCandidate** (مرشح الإحالة)
   - للضمائر المستترة، أسماء الإشارة، أسماء الموصول

3. **EllipsisCandidate** (مرشح الحذف)
   - للأفعال المحذوفة، الفواعل المحذوفة، الأخبار المحذوفة

### ب) طبقات الحالات الخاصة

4. **VerbStateAlgebra** (جبر حالة الفعل)
   - المبني للمجهول (تحويل الحركات + كبت فتحة الفاعل)
   - الأمر (مشتق من المضارع)
   - المجزوم (سكون/حذف/حذف النون)
   - الأفعال الخمسة (نون الإعراب + حذف مشروط)

5. **NominalMarkConstraintAlgebra** (جبر قيد علامة الاسم)
   - الممنوع من الصرف (منع التنوين + جر بالفتحة)

6. **FrameOperatorAlgebra** (جبر معامل الإطار)
   - الأفعال الناسخة (كان وأخواتها)
   - الحروف الناسخة (إنّ وأخواتها)
   - أفعال المقاربة والشروع (كاد، عسى، أخذ...)
   - أفعال القلوب (ظنّ، حسب، علم...)

### ج) طبقات التركيب النهائية

7. **AmilMamulEquation** (معادلة العامل والمعمول)
   - ربط العامل بالمعمول المحدد
   - تحديد العلاقة (إسناد، تضمين، تقييد)

8. **NisbahEquation** (معادلة النسبة)
   - تحديد نوع النسبة (إضافة، وصف، بيان، عطف...)

9. **RoleEquation** (معادلة الدور النحوي)
   - فاعل_مرشح، مفعول_مرشح، مبتدأ_مرشح، خبر_مرشح...
   - **فقط بعد إغلاق كل الطبقات السابقة**

---

## 7. الترتيب الصحيح للتنفيذ المستقبلي

```
✅ CaseEffectCandidate             (تم - هذا الحل)
↓
⏩ EstimatedMarkEquation           (التالي المباشر)
↓
⏩ VerbStateAlgebra                (حالات الأفعال)
   - PassiveVoiceCandidate
   - ImperativeCandidate
   - JussiveCandidate
   - FiveVerbsCandidate
↓
⏩ NominalMarkConstraintAlgebra    (قيود الأسماء)
   - DiptoteCandidate
↓
⏩ FrameOperatorAlgebra             (معاملات الإطار)
   - NasikhVerbCandidate (كان وأخواتها)
   - NasikhHarfCandidate (إنّ وأخواتها)
↓
⏩ ReferenceCandidate               (الإحالة)
↓
⏩ EllipsisCandidate                (الحذف)
↓
⏩ AmilMamulEquation                (العامل والمعمول)
↓
⏩ NisbahEquation                   (النسبة)
↓
⏩ RoleEquation                     (الدور النحوي)
```

---

## 8. الحكم النهائي

### ما قبل هذا الحل

❌ **السلسلة لم تكن مكتملة**:
```
OperatorCandidate
→ FactorMarkEquation
→ ??? (فجوة)
```

### ما بعد هذا الحل

✅ **السلسلة الآن مكتملة**:
```
OperatorCandidate
→ FactorMarkEquation
→ CaseEffectCandidate ✅
→ [future layers]
```

### القول الدقيق النهائي

> **المستودع الآن عالج رصد العلامة، توافق العلامة، محفز العامل، سجل العامل، مرشح العامل، معادلة العامل/العلامة، وأنتج طبقة مرشح الأثر الإعرابي.**
>
> **لم يبقَ إلا طبقات الجسور (علامة مقدرة، إحالة، حذف)، الحالات الخاصة (حالة الفعل، قيود الاسم، معاملات الإطار)، ثم التركيب النهائي (عامل/معمول، نسبة، دور نحوي).**

---

## 9. الأمثلة التطبيقية

### مثال 1: جملة اسمية بسيطة

**Input**: "الكتابُ جديدٌ"

**السلسلة**:

1. **PreSyntaxMufradVector** × 2:
   - `الكتابُ`: ISM_COMMON, damma
   - `جديدٌ`: ISM_COMMON, damma + tanwin

2. **SentenceFrameCandidate**: NominalFrameCandidate
   - lead_noun_index = 0

3. **CaseSignMatrix**: rows × 2
   - row[0]: RAFA_COMPATIBLE
   - row[1]: RAFA_COMPATIBLE

4. **OperatorTriggerPotential**:
   - triggered_families = (POSSIBLE_IBTIDAA_FAMILY,)

5. **OperatorCandidate**:
   - registry_entry: "الابتداء"
   - policy_family: MIXED_RAFI_NASB_POLICY_FAMILY

6. **FactorMarkEquation** × 2:
   - equation[0]: factor=ibtidaa, affected=الكتابُ, type=RAFʿ_CANDIDATE
   - equation[1]: factor=ibtidaa, affected=جديدٌ, type=RAFʿ_CANDIDATE

7. **CaseEffectCandidate** × 2 ✅ (NEW):
   - candidate[0]: effect_type=RAFʿ_EFFECT_CANDIDATE (الكتابُ مبتدأ_مرشح)
   - candidate[1]: effect_type=RAFʿ_EFFECT_CANDIDATE (جديدٌ خبر_مرشح)

**Output**: مرشحات أثر إعرابي جاهزة للطبقة التالية (AmilMamulEquation).

### مثال 2: جملة فعلية

**Input**: "كتبَ الطالبُ"

**السلسلة**:

1. **PreSyntaxMufradVector** × 2:
   - `كتبَ`: FIIL_MADI, fatha
   - `الطالبُ`: ISM_COMMON, damma

2. **SentenceFrameCandidate**: VerbalFrameCandidate
   - verb_index = 0

3. **OperatorTriggerPotential**:
   - triggered_families = (POSSIBLE_VERBAL_GOVERNANCE_FAMILY,)

4. **OperatorCandidate**:
   - registry_entry: "الفعل المتعدي"
   - policy_family: RAFI_POLICY_FAMILY (للفاعل)

5. **FactorMarkEquation**:
   - factor=verb, affected=الطالبُ, type=RAFʿ_CANDIDATE

6. **CaseEffectCandidate** ✅ (NEW):
   - effect_type=RAFʿ_EFFECT_CANDIDATE (الطالبُ فاعل_مرشح)

---

## 10. الحواجز المتبقية

### 10.1 العلامات المقدرة

```python
# مثال: "المُستشفى جميلٌ"
# العلامة المقدرة على "المُستشفى" (للتعذر)

equation = EstimatedMarkEquation(
    reason=EstimationReason.TAʿADHDHUR,  # تعذر
    base_mark=CaseSignValue.ESTIMATED_DAMMA,
    ...
)
```

### 10.2 الحالات الخاصة للأفعال

```python
# مثال: "يكتبان" (فعل من الأفعال الخمسة)
# نون الإعراب + حذف مشروط

verb_state = FiveVerbsCandidate(
    base_form="يكتب",
    attached_pronoun=ALIF_ITHNAYN,
    nun_status=NunStatus.RETAINED,  # ثبوت النون (رفع)
    conditional_deletion=lambda op: op in {لم, لن, ...}
)
```

### 10.3 الأفعال الناسخة

```python
# مثال: "كان الكتابُ جديدًا"
# كان تفتح إطار اسمي وتحوّله

nasikh_frame = NasikhFrameOperator(
    verb="كان",
    ism_kana_candidate=الكتابُ,  # رفع
    khabar_kana_candidate=جديدًا,  # نصب
)
```

---

## 11. الخلاصة الحاسمة

### ✅ ما حققه هذا الحل

1. **سدّ الفجوة** بين `FactorMarkEquation` و `CaseEffectCandidate`
2. **إنتاج مرشحات أثر إعرابي** (لا أحكام نهائية)
3. **تطبيق جميع القوانين الدستورية** (لا معنى، لا إفادة، لا حكم)
4. **حفظ الهويات** (عامل + عامل مصدري + معمول)
5. **تطبيق سقف الرتبة** و **وراثة المخلفات**
6. **تنفيذ خوارزمية تحديد نوع الأثر** (policy + compatibility + equation)

### ⏩ ما يبقى للمستقبل

1. **EstimatedMarkEquation** (علامة مقدرة)
2. **VerbStateAlgebra** (حالة الفعل)
3. **NominalMarkConstraintAlgebra** (قيود الاسم)
4. **FrameOperatorAlgebra** (معاملات الإطار)
5. **ReferenceCandidate** (إحالة)
6. **EllipsisCandidate** (حذف)
7. **AmilMamulEquation** (عامل ومعمول)
8. **NisbahEquation** (نسبة)
9. **RoleEquation** (دور نحوي)

### القول الختامي

> **الخوارزمية الآن تملك سلسلة مكتملة من رصد العلامة السطحية إلى إنتاج مرشح الأثر الإعرابي.**
>
> **الطبقة التالية (`AmilMamulEquation`) تستطيع الآن الاستناد إلى `CaseEffectCandidate` لبناء معادلات العامل والمعمول الكاملة.**
>
> **الفجوة مُغلقة. الطريق واضح.**

---

**تاريخ التنفيذ**: 2026-05-30
**المُنفذ**: Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
**الملفات المُضافة**:
- `src/dal_core/case_effect_candidate.py` (831 lines)
- `tests/dal_core/test_case_effect_candidate.py` (627 lines)
- `docs/CASE_EFFECT_CANDIDATE_SOLUTION.md` (هذا الملف)
