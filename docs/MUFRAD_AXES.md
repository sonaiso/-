# المحاور المتعامدة الأربعة للفظ المفرد قبل التركيب

# Four Orthogonal Axes of the Singular Form (Pre-Composition)

> هذه الوثيقة تشرح ما يخص "إغلاق شكل اللفظ المفرد قبل التركيب" في
> `dal_core`. تطبيق هذه الخطة سدّ ثغرة جذرية حصلت سابقًا: ربط
> البناء/الإعراب بعدد المقاطع (هلوسة).

---

## ١. ما تم تصحيحه (شفافية)

### الخطأ السابق (هلوسة)

ربط البناء/الإعراب بعدد المقاطع على شكل قاعدة:
> «الكلمة ذات ١..٥ مقاطع ⇒ مبنية، وإلا فمعربة».

### الصواب

- عدد المقاطع **محور وصفي رقمي** (D1 `SYLLABIC`)؛ ليس حُكمًا.
- البناء/الإعراب **محور حُكمي ثنائي** يعتمد على نوع الكلمة (D5
  `IDENTITY_AXIS`) وخصائصها الصرفية (D3/D4) — لا على عدد المقاطع.
- الجامد/المشتق **محور حُكمي ثنائي مستقل** يعتمد على الجذر (D3)
  والوزن (D4) والهوية (D5) — لا على البناء/الإعراب ولا على المقاطع.

النتيجة: **ثلاثة محاور متعامدة** فوق محور أساسي رابع (الهوية).
لا أحدها يُستنبط من الآخر.

---

## ٢. المحاور الأربعة

| المحور | الموقع في `dal_core` | النوع | القيم |
|---|---|---|---|
| ١. الهوية | `d_type.DalType` (موجود) | تصنيفي | `ISM` / `FIIL` / `HARF` / `AMBIGUOUS` |
| ٢. المقاطع | `syllables.Syllable` (موجود) | وصفي رقمي | `1..5`, `OVERFLOW` |
| ٣. البناء/الإعراب | `mufrad_axes.BinaaJudgment` (جديد، PR-A) | حُكمي ثنائي | `MABNI` / `MUERAB` / `UNRESOLVED` / `NOT_APPLICABLE` |
| ٤. الجامد/المشتق | `mufrad_axes.IshtiqaqJudgment` (جديد، PR-A) | حُكمي ثنائي | `JAMID` / `MUSHTAQ` / `UNRESOLVED` / `NOT_APPLICABLE` |

### الأنواع الفرعية للمحور الثالث (البناء)

`mufrad_axes.BinaaSubtype`:

- `BINAA_SUKUN` (مبني على السكون)
- `BINAA_FATH` (مبني على الفتح)
- `BINAA_DAMM` (مبني على الضم)
- `BINAA_KASR` (مبني على الكسر)
- `INVARIANT_PROPER` (مبني/ثابت لكونه عَلَم أعجمي مثلًا)

### الأنواع الفرعية للمحور الرابع

`mufrad_axes.MushtaqSubtype`:

- `ISM_FAIL` (اسم فاعل: فاعل)
- `ISM_MAFUL` (اسم مفعول: مفعول)
- `SIFA_MUSHABBAHA` (صفة مشبّهة)
- `ISM_TAFDIL` (اسم تفضيل: أفعل)
- `ISM_ZAMAN` (اسم زمان: مَفْعَل)
- `ISM_MAKAN` (اسم مكان: مَفْعَل/مَفْعِل)
- `ISM_ALA` (اسم آلة: مِفْعَل/مِفْعَال/مِفْعَلَة)
- `MASDAR_MIMI` (مصدر ميمي)
- `MASDAR_SINAII` (مصدر صناعي)

`mufrad_axes.JamidSubtype`:

- `JAMID_DHAT` (جامد ذاتي: رجل، حجر)
- `JAMID_MASDAR_ASLI` (مصدر أصلي: ضَرْب، عِلْم)
- `JAMID_PROPER_NAME` (عَلَم: محمد، مكة)
- `JAMID_FUNCTIONAL` (وظيفي: ضمائر، إشارات، موصولات…)

### المحور الإضافي: مرونة الصرف

`mufrad_axes.SarfFlexibility` يفكّ الخلط الذي كان موجودًا في النصّ الحرّ
`NounInflectionClass.inflection_type`:

- `MUNSARIF` (مصروف)
- `MAMNU_MIN_SARF` (ممنوع من الصرف)
- `NOT_APPLICABLE` (للأفعال والحروف والأسماء المبنيّة)

---

## ٣. مصفوفة المحاور (٢×٢ للأسماء)

| | جامد | مشتق |
|---|---|---|
| **مبني** | هذا، الذين، أنت (`JAMID_FUNCTIONAL`) | لا يوجد |
| **معرب** | رجل، حجر (`JAMID_DHAT`)؛ محمد (`JAMID_PROPER_NAME`)؛ ضَرْب (`JAMID_MASDAR_ASLI`) | كاتب (`ISM_FAIL`)، مكتوب (`ISM_MAFUL`)، أفضل (`ISM_TAFDIL`)… |

ملاحظة: خانة (مبني، مشتق) فارغة لأن الأسماء المشتقّة كلها معربة (لا يوجد
اسم فاعل أو مفعول مبني). لكن هذا **نتيجة عبور القاعدتين المستقلتين**،
وليس قاعدة مُدخلة في النظام.

للأفعال والحروف:

| | المحور الثالث | المحور الرابع |
|---|---|---|
| **حرف** (مِن، إنّ، هل…) | `MABNI` دائمًا | `NOT_APPLICABLE` |
| **فعل ماضٍ** (ضرب) | `MABNI` | `NOT_APPLICABLE` |
| **فعل أمر** (اضرب) | `MABNI` | `NOT_APPLICABLE` |
| **فعل مضارع + نون نسوة/توكيد** (يضربن، ليضربنّ) | `MABNI` | `NOT_APPLICABLE` |
| **فعل مضارع** (يضرب) | `MUERAB` | `NOT_APPLICABLE` |

---

## ٤. القاضيان

### `dal_core.binaa_judge.judge_binaa`

```python
from dal_core.binaa_judge import BinaaJudgeInput, judge_binaa
from dal_core.d_type import DalType
from dal_core.type_ids import VerbTypeID

result = judge_binaa(BinaaJudgeInput(
    dal_type=DalType.FIIL,
    surface_form="يَضْرِبْنَ",
    verb_type_id=VerbTypeID.FIIL_MUDARI,
))
# result.judgment == BinaaJudgment.MABNI
# result.subtype  == BinaaSubtype.BINAA_SUKUN
# result.evidence.source == "binaa_judge.R3"  (مضارع + نون النسوة)
```

ترتيب القواعد (لا يقبل عدد المقاطع كمدخل):

1. R0 — `AMBIGUOUS` ⇒ `UNRESOLVED`.
2. R1 — حرف ⇒ `MABNI`.
3. R2a — فعل ماضٍ ⇒ `MABNI`.
4. R2b — فعل أمر ⇒ `MABNI`.
5. R3 — فعل مضارع + نون النسوة/التوكيد ⇒ `MABNI`.
6. R4 — فعل مضارع غير ذلك ⇒ `MUERAB`.
7. R5 — اسم في `MabniRegistry` ⇒ `MABNI` + النوع الفرعي من السجل.
8. R6 — اسم غير ذلك ⇒ `MUERAB` افتراضًا.

أي شك ⇒ `UNRESOLVED` + بقيّة `MUFRAD_MABNI_MURAB_UNRESOLVED`.

### `dal_core.ishtiqaq_judge.judge_ishtiqaq`

```python
from dal_core.ishtiqaq_judge import IshtiqaqJudgeInput, judge_ishtiqaq
from dal_core.morph_features import WaznCandidate

result = judge_ishtiqaq(IshtiqaqJudgeInput(
    dal_type=DalType.ISM,
    surface_form="كَاتِبٌ",
    wazn_candidates=(katib_wazn,),
))
# result.judgment == IshtiqaqJudgment.MUSHTAQ
# result.subtype  == MushtaqSubtype.ISM_FAIL
```

ترتيب القواعد:

1. R0 — `AMBIGUOUS` ⇒ `UNRESOLVED`.
2. R1 — حرف ⇒ `NOT_APPLICABLE`.
3. R2 — فعل ⇒ `NOT_APPLICABLE` (المحور لا ينطبق على الأفعال بهذه الدلالة).
4. R3 — اسم في `MabniRegistry` ⇒ `JAMID` + `JAMID_FUNCTIONAL`.
5. R4 — اسم علم ⇒ `JAMID` + `JAMID_PROPER_NAME`.
6. R5 — تطابق وزن مشتق (فاعل، مفعول، تفضيل…) ⇒ `MUSHTAQ` + النوع.
7. R6 — وجود جذر بلا وزن مشتق ⇒ `JAMID` + `JAMID_MASDAR_ASLI`.
8. R7 — اسم بلا جذر ولا وزن ⇒ `JAMID` + `JAMID_DHAT`.
9. R8 — تنافس أكثر من نوع اشتقاقي ⇒ `UNRESOLVED` + بقيّة
   `MUFRAD_JAMID_MUSHTAQ_UNRESOLVED`.

---

## ٥. سجلّ الأسماء المبنية المغلق

`dal_core.mabni_registry.MabniRegistry` (PR-B) يحوي الفئات الست:

- **ضمائر منفصلة:** أنا، أنت، هو، هي، نحن…
- **ضمائر متصلة:** الكاف، الهاء، الياء، التاء، النا…
- **أسماء إشارة:** هذا، هذه، هؤلاء، ذلك، تلك… (المثنّى معرب)
- **أسماء موصولة:** الذي، التي، الذين، اللاتي… (اللذان واللتان معرب مثنى)
- **أسماء استفهام/شرط:** مَن، ما، متى، أين، كيف، كم…
- **ظروف مبنية:** حيث، إذ، إذا، أمسِ، الآن، قطّ، عوض…
- **أسماء أفعال:** هيهات، صَهْ، آمين…
- **أعداد مركّبة:** أحد عشر، اثنا عشر، ثلاثة عشر…

السجلّ مغلَق بـ`MappingProxyType` (نمط `NahwOperatorRegistry`):
لا إضافة ولا حذف ولا تعديل بعد البناء.

---

## ٦. الدمج في `MufradProof`

```python
from dal_core.mufrad_proof import MufradProof
from dal_core.mufrad_axes import (
    BinaaJudgment, BinaaSubtype,
    IshtiqaqJudgment, MushtaqSubtype,
    SarfFlexibility,
)

proof = MufradProof(
    ...,  # الحقول القديمة كما هي
    binaa_judgment=BinaaJudgment.MUERAB,
    binaa_subtype=None,                    # المعرب ليس له نوع فرعي
    ishtiqaq_judgment=IshtiqaqJudgment.MUSHTAQ,
    ishtiqaq_subtype=MushtaqSubtype.ISM_FAIL,
    sarf_flexibility=SarfFlexibility.MUNSARIF,
)
```

التحقق التلقائي (`__post_init__`):

- `MABNI` ⇒ `binaa_subtype` لا بدّ أن يكون `BinaaSubtype` (لا نصًّا).
- `MUERAB`/`NOT_APPLICABLE` ⇒ `binaa_subtype` لا بدّ أن يكون `None`.
- `MUSHTAQ` ⇒ `ishtiqaq_subtype` لا بدّ أن يكون `MushtaqSubtype`.
- `JAMID` ⇒ `ishtiqaq_subtype` لا بدّ أن يكون `JamidSubtype`.
- `NOT_APPLICABLE` ⇒ `ishtiqaq_subtype` لا بدّ أن يكون `None`.

التوافق الخلفي: الحقلان القديمان `mabni_murab_status` و
`jamid_mushtaq_status` (من نوع `CandidateStatus`) لم يُحذفا. كذلك الحقل
`NounInflectionClass.inflection_type` (نصّ حرّ) لم يُحذف؛ صار حقلًا قديمًا
يُقرأ احتياطًا. القراءة في `case_sign_matrix._is_mabni_by_value` تُفضّل
المحور المُصنَّف أولًا ثم ترجع للنصّ القديم.

---

## ٧. البوّابة الخامسة في `PreSyntaxMufradVector`

`presyntax_vector.allows_operator_consumption()` صار يحوي بوّابة خامسة:

```python
# Gate 5 (PR-F): block on unresolved mufrad axes.
if self.binaa_judgment == BinaaJudgment.UNRESOLVED:
    return False
is_noun = (self.type_value or "").upper() == "ISM" or ...
if is_noun and self.ishtiqaq_judgment == IshtiqaqJudgment.UNRESOLVED:
    return False
```

لا عامل (`operator`) يستهلك متّجهًا مفرديًا قبل حسم البناء؛ ولا عامل يستهلك
متّجهًا اسميًا قبل حسم الجامد/المشتق. هذا يمنع تسرّب القرار غير المحسوم إلى
طبقة التركيب.

---

## ٨. منع الهلوسة المستقبليّ

### قاعدة جبرية صريحة

`dal_core.dal_algebra.FORBIDDEN_AXIS_PROMOTIONS` تحوي:

```python
frozenset({
    ("SYLLABIC", "BINAA_JUDGMENT"),
    ("SYLLABIC", "ISHTIQAQ_JUDGMENT"),
})
```

ودالّة `assert_axis_promotion_allowed(source_domain, target_axis_name)`
ترفع `ValueError` فورًا لأي محاولة ترقية من المقاطع إلى المحور الحُكمي.
هذا حظر فئوي لا يقبل أي مبرّر (`trace`/`shortcut`/`attestation` لا تكسر
الحظر).

### اختبار حارس

`tests/dal_core/test_mufrad_axes_coverage.py::TestEqualSyllableCountWordsDifferentJudgment`
يثبت أن كلمتين قصيرتين بصورة مقطعيّة متشابهة (`هَذَا` و`رَجُلٌ`) تقعان في
خانتين مختلفتين على محور البناء. إذا انهار هذا الاختبار ⇒ شخصٌ ما أدخل
المقاطع كمدخل في القاضي.

### تعليق توثيقي صريح

أعلى `binaa_judge.py` و`ishtiqaq_judge.py`:

> «هذا القاضي لا يستخدم عدد المقاطع كمدخل ولا `syllable_shapes`.
> إذا احتجت ذلك فأنت تُقحم محورًا في آخر.»

---

## ٩. ما هو خارج النطاق (صراحة)

- لا حكم نحوي (مرفوع/منصوب/مجرور) داخل `MufradProof`. هذا قرار العامل،
  ليس قرار اللفظ المفرد.
- لا دور تركيبي (مبتدأ/خبر/فاعل/مفعول). نفس السبب.
- لا دلالة (حقيقة/مجاز/مرادف). محور خارج `dal_core` كاملًا.
- محور المقاطع (D1 `SYLLABIC`) يبقى وصفيًا فقط؛ استخدامه الوحيد المرتبط
  بالمفرد هو مطابقة قوالب الوزن في D4، لا أكثر.

---

## ١٠. الملفات الجديدة (PR-A → PR-G)

| الملف | الدور | PR |
|---|---|---|
| `src/dal_core/mufrad_axes.py` | تعدادات المحاور (Enums) | PR-A |
| `src/dal_core/mabni_registry.py` | السجلّ المغلق للأسماء المبنية | PR-B |
| `src/dal_core/binaa_judge.py` | قاضي البناء/الإعراب | PR-C |
| `src/dal_core/ishtiqaq_judge.py` | قاضي الجامد/المشتق | PR-D |
| `tests/dal_core/test_mufrad_axes.py` | اختبارات التعدادات | PR-A |
| `tests/dal_core/test_mabni_registry.py` | اختبارات السجل | PR-B |
| `tests/dal_core/test_binaa_judge.py` | اختبارات قاضي البناء (٢٨ اختبار) | PR-C |
| `tests/dal_core/test_ishtiqaq_judge.py` | اختبارات قاضي الاشتقاق (٢١ اختبار) | PR-D |
| `tests/dal_core/test_mufrad_axes_integration.py` | تكامل `MufradProof` (١٣ اختبار) | PR-E |
| `tests/dal_core/test_presyntax_axes_gate.py` | البوّابة الخامسة (١١ اختبار) | PR-F |
| `tests/dal_core/test_mufrad_axes_coverage.py` | تغطية المصفوفة + كناري المقاطع (٣٢ اختبار) | PR-G |
| `tests/dal_core/test_axis_promotion_ban.py` | حظر `SYLLABIC→BINAA` (٨ اختبارات) | PR-G |

---

## ١١. مراجع متقاطعة

- `docs/DAL_ALGEBRA_SIGNATURE.md` — توقيع الجبر العام ومنع الترقية
  المباشرة (D1→D7).
- `docs/DAL_CORE_MUFRAD_PROOF.md` — عقد `MufradProof` وحدوده.
- `src/dal_core/README.md` — قائمة الملفات الكاملة.
