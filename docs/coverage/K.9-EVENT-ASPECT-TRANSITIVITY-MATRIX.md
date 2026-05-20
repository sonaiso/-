# K.9: طبقة الحدث وأحواله

# K.9: Event and Aspect Layer Coverage Matrix

**Layer**: K.9
**Domain**: Judgment (D7) + Verb Features
**Status**: 🚧 Partial (VerbFeatureProof exists, transitivity missing)
**Version**: 1.0.0

---

## Required Concepts

### حالة الفعل (Verb Form)
- ✅ ماض (past)
- ✅ مضارع (present)
- ✅ أمر (imperative)

### البناء للمعلوم/المجهول
- ⚠️ معلوم (active voice): ضَرَبَ
- ⚠️ مجهول (passive voice): ضُرِبَ

### التعدي واللزوم (Transitivity)
- ❌ متعدٍّ لمفعول واحد (transitive to one object)
- ❌ متعدٍّ لمفعولين (transitive to two objects)
- ❌ متعدٍّ لثلاثة مفاعيل (transitive to three objects)
- ❌ لازم (intransitive)
- ❌ تعدي سماعي (attested transitivity): رَغِبَ في

### الأبنية الخاصة (Special Forms)
- ⚠️ مطاوعة (reciprocal): انكسر، انفتح
- ⚠️ مشاركة (mutual): قاتل، ضارب
- ⚠️ سببية (causative): أخرج، أدخل
- ⚠️ مسببية (requestative): استخرج، استفهم

### الزمن والجهة (Time and Aspect)
- ⚠️ ماض (past time)
- ⚠️ حاضر (present time)
- ⚠️ مستقبل (future time)
- ⚠️ تمام (perfective)
- ⚠️ استمرار (progressive)

---

## القانون الحاكم

```
التعدي واللزوم: قياس ≠ سماع
Transitivity: qiyas ≠ sama'

ضَرَبَ: متعدٍّ (قياس)
ذَهَبَ: لازم (قياس)
رَغِبَ: متعدٍّ بـ(في) (سماع)
```

---

## Current Status

### ✅ Exists
- `VerbFeatureProof` in MufradProof
- Basic verb type (madi/mudari/amr)

### ❌ Missing
- `TransitivityCandidate` contract
- `VoiceCandidate` (malum/majhul)
- `EventAspectCandidate`
- Transitivity lexicon (لازم/متعدي)

---

## Requires Lexicon

**Yes - Critical** for:
- Transitivity (some verbs have attested transitivity)
- Irregular verb behavior
- Prepositional complements (رَغِبَ في)

---

## Gap Analysis

**Estimated**: 3-4 weeks

---

**Cross-References**: K.4 (verb forms), K.5 (verb health), K.10 (lexicon)
