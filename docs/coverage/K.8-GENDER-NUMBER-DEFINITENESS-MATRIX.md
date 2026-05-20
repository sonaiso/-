# K.8: طبقة الجنس والعدد والتعريف

# K.8: Gender-Number-Definiteness Layer Coverage Matrix

**Layer**: K.8
**Domain**: Judgment (D7)
**Status**: 🚧 Partial
**Version**: 1.0.0

---

## Required Concepts

### الجنس (Gender)
- ⚠️ مذكر حقيقي (real masculine): رجل، أسد
- ⚠️ مذكر مجازي (metaphorical masculine): كتاب، باب
- ⚠️ مؤنث حقيقي (real feminine): امرأة، بقرة
- ⚠️ مؤنث مجازي (metaphorical feminine): شمس، أرض
- ⚠️ مؤنث لفظي (lexical feminine): طلحة، حمزة
- ⚠️ مؤنث معنوي (semantic feminine): زينب، سعاد
- ⚠️ مؤنث سماعي (attested feminine): دار، نار، أرض

### العدد (Number)
- ✅ مفرد (singular)
- ✅ مثنى (dual): ان/ين
- ✅ جمع مذكر سالم (sound masculine plural): ون/ين
- ✅ جمع مؤنث سالم (sound feminine plural): ات
- ⚠️ جمع تكسير (broken plural): رجال، كتب، أقلام
- ⚠️ اسم جمع (collective noun): قوم، رهط
- ⚠️ اسم جنس جمعي (collective generic): تمر/تمرة، عرب/عربي

### التعريف (Definiteness)
- ✅ نكرة (indefinite)
- ✅ معرفة بالألف واللام (definite by article)
- ⚠️ أل العهدية (anaphoric al)
- ⚠️ أل الجنسية (generic al)
- ⚠️ أل الاستغراقية (universal al)
- ⚠️ أل الزائدة (extra al)
- ⚠️ أل الغلبة (al of predominance)
- ⚠️ معرفة بالعلمية (definite by proper name)
- ⚠️ معرفة بالإضافة (definite by idafa)
- ⚠️ معرفة بالضمير (definite by pronoun)
- ⚠️ معرفة بالإشارة (definite by demonstrative)
- ⚠️ معرفة بالموصول (definite by relative)

---

## القانون الحاكم

```
إذا كان الحكم يحتاج سماعًا ولا يوجد معجم/شاهد:
لا Certificate.
```

---

## Current Status

### ✅ Exists
- `gender_status` in MufradProof
- `number_status` in MufradProof
- `definiteness_status` in MufradProof

### ❌ Missing
- Gender subtype classification
- Plural pattern classification (broken plurals)
- Definiteness subtype (types of al)
- Lexicon for metaphorical gender

---

## Gap Analysis

Need lexicon integration for:
- Metaphorical gender (شمس: feminine)
- Broken plural patterns (كتاب → كتب)
- Collective nouns

**Estimated**: 3-4 weeks

---

**Requires Lexicon**: Yes (critical for metaphorical gender, broken plurals)
