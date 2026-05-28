# ملحق خوارزميات النسبة
# Relation Algorithms Appendix

**النسب الإسنادية، والنسب التضمينية، والنسب التقييدية**
**Predicative, Inclusion, and Restrictive Relations**

**Version**: 1.0.0
**Status**: Constitutional Appendix
**Created**: 2026-05-28
**Depends On**: ARABIC_ALGEBRA_ALGORITHM_CONSTITUTION.md
**Position**: After wordform/operator algorithms, before ifadah/hukm algorithms

---

## الموضع المعماري (Architectural Position)

```
WordformCandidate
    ↓ [relation algorithms]
RelationCandidate (Predicative/Inclusion/Restrictive)
    ↓ [relation network closure]
Ifadah_Dal
    ↓ [semantic matching]
Hukm
```

**القانون المركزي:**
> النسبة هي الجسر بين "كلمات مرشحة" و"إفادة دالية مغلقة".
>
> Relation is the bridge between "candidate wordforms" and "closed dal ifadah".

---

## 1. الأصل الدستوري
## Constitutional Foundation

### التعريف (Definition):

**النسبة ليست:**
- معنى نهائيًا (final meaning)
- حكمًا (judgment)
- واقعًا (reality)

**النسبة هي:**

عملية ربط مرخّصة بين طرفين أو أكثر، تنتج علاقة دالية قابلة للإغلاق في الإفادة.

A licensed linking operation between two or more terms that produces a dal relation capable of closure in ifadah.

### الشروط الإجبارية (Mandatory Requirements):

```python
Relation = {
    preserved_anchor_id,      # مرساة محفوظة
    related_term,             # طرف مرتبط
    relation_type,            # نوع نسبة
    declared_invariant,       # ثابت معلن
    licensed_change,          # تغيير مرخّص
    typed_load,               # حمولة مصنفة
    trace,                    # أثر
    residual_audit,           # تدقيق البقايا
    rank,                     # رتبة
    effect                    # أثر
}
```

### القانون العام (General Law):

```
لا توجد نسبة بلا:
- مرساة محفوظة
- طرف مرتبط
- نوع علاقة
- أثر وبقايا ورتبة
```

```
No relation without:
- Preserved anchor
- Related term
- Relation type
- Trace, residuals, and rank
```

---

## 2. الأنواع الكبرى للنسبة
## Three Major Relation Types

### التصنيف الثلاثي (Tripartite Classification):

1. **PredicativeRelation** (النسبة الإسنادية)
   - Predication: حمل محمول على حامل
   - Links predicate to subject/anchor
   - Example: زيد قائم (Zayd [is] standing)

2. **InclusionRelation** (النسبة التضمينية)
   - Inclusion: إدخال طرف في مجال طرف
   - Links contained to container
   - Example: الإنسان حيوان (Human [is] animal)

3. **RestrictiveRelation** (النسبة التقييدية)
   - Restriction: تضييق مجال حامل بقيد
   - Links restrictor to restricted
   - Example: رجل كريم (generous man)

### المنع الصارم (Strict Prohibition):

```
❌ لا يجوز الخلط بينها
   Mixing these types is FORBIDDEN

❌ PredicativeRelation ≠ InclusionRelation
❌ PredicativeRelation ≠ RestrictiveRelation
❌ InclusionRelation ≠ RestrictiveRelation
```

---

## القسم الأول: خوارزمية النسبة الإسنادية
## Part I: Predicative Relation Algorithm

### 3. تعريف النسبة الإسنادية
### Predicative Relation Definition

**النسبة الإسنادية:**

ربط محمول بحامل على وجه يصلح لإنتاج إفادة دالية.

Linking a predicate to a subject/anchor in a manner suitable for producing dal ifadah.

**مثال (Example):**

```
زيد قائم

الحامل (Anchor): زيد
المحمول (Predicate): قائم
نوع النسبة (Relation Type): إسناد قيام إلى زيد
المخرج (Output): RelationCandidate قابل لإغلاق Ifadah_Dal
```

**⚠️ تنبيه حاسم (Critical Warning):**

```
النسبة الإسنادية لا تعني أن زيدًا قائم في الواقع.
هي فقط تقول إن الدال بنى علاقة إسنادية.

Predicative relation does NOT mean Zayd is actually standing.
It only says the signifier constructed a predicative relation.
```

---

### 4. خوارزمية النسبة الإسنادية
### Predicative Relation Algorithm

```python
Algorithm: build_predicative_relation

Input:
    WordformCandidateSet

Carrier:
    subject_candidate          # مبتدأ / فاعل / نائب فاعل
    predicate_candidate        # خبر / محمول
    verbal_event_candidate     # حدث فعلي
    operator_candidate         # عامل (كان، إن، ظن...)
    tense_marker              # علامة زمن
    case_trace                # أثر إعرابي
    reference_trace           # أثر إحالة
    order_trace               # أثر رتبة

Prior:
    predication_rules         # قواعد الإسناد
    nominal_sentence_rules    # قواعد الجملة الاسمية
    verbal_sentence_rules     # قواعد الجملة الفعلية
    nasikh_registry          # سجل النواسخ
    tense_operator_registry  # سجل عوامل الزمن
    agreement_rules          # قواعد المطابقة
    reference_rules          # قواعد الإحالة
    ellipsis_policy          # سياسة الحذف

Gate:
    predication_license_gate

Operation:
    detect_anchor
    detect_predicate_or_event
    test_predicative_compatibility
    test_agreement
    test_case_effect
    test_operator_intervention
    test_order_distance
    license_hidden_element_if_needed
    build_predicative_edge
    preserve_trace

Identity:
    preserve_anchor_identity

Candidate:
    PredicativeRelationCandidate

Residuals:
    missing_predicate
    hidden_subject_possible
    ambiguous_anchor
    ambiguous_predicate
    weak_case_trace
    tense_uncertainty
    operator_interference
    reference_gap

Rank:
    candidate | hypothesis | strong_hypothesis | certificate

Output:
    PredicativeRelationCandidate

Forbidden:
    contextual_final_meaning
    hukm
    reality
```

---

### 5. قوانين النسبة الإسنادية (15 Laws)
### Predicative Relation Laws

#### Law 1: لا إسناد بلا حامل ومحمول
**No predication without anchor and predicate**

```
لا إسناد بلا حامل ومحمول أو حدث وفاعل مرشح.
```

No predication without anchor and predicate OR event and agent candidate.

---

#### Law 2: الحامل يثبت بترخيص
**Anchor established by license**

```
الحامل لا يثبت حاملًا إلا بترخيص علاقة.
```

Anchor is NOT established as anchor except through relation license.

---

#### Law 3: المحمول يثبت بقبول الحمل
**Predicate established by acceptability**

```
المحمول لا يثبت محمولًا إلا بقبول الحمل على الحامل.
```

Predicate is NOT established as predicate except through acceptance of predication on anchor.

---

#### Law 4: الفعل لا ينتج فاعلًا بلا أثر
**Verb does not produce agent without trace**

```
الفعل لا ينتج فاعلًا نهائيًا بلا أثر تركيبي.
```

Verb does NOT produce final agent without compositional trace.

---

#### Law 5: اسم الفاعل ليس فاعلًا نحويًا بالوزن
**Active participle is not syntactic agent by pattern**

```
اسم الفاعل لا ينتج فاعلية نحوية من وزنه وحده.
```

Active participle does NOT produce syntactic agency from its pattern alone.

**Example:**
```
كاتبٌ الدرسَ

"كاتب" morphologically active participle
but NOT necessarily syntactic fā'il until compositional analysis
```

---

#### Law 6: المبتدأ والخبر حافة إسناد
**Mubtada and khabar are predication edge**

```
المبتدأ والخبر ليسا معنى نهائيًا، بل حافة إسناد.
```

Mubtada and khabar are NOT final meaning, but predication edge.

---

#### Law 7: النواسخ تحوّل الإسناد
**Nawāsikh transform predication**

```
النواسخ لا تلغي الإسناد، بل تحوله.
```

Nawāsikh do NOT cancel predication; they transform it.

---

#### Law 8: كان وأخواتها تحويل زمني
**Kāna and sisters: temporal transformation**

```
كان وأخواتها تحول الإسناد زمنيًا أو وجوديًا.
```

Kāna and sisters transform predication temporally or existentially.

**Example:**
```
زيد قائم      → Direct predication
كان زيد قائمًا  → Temporal predication (Zayd WAS standing)
```

---

#### Law 9: إن وأخواتها تحويل توكيدي
**Inna and sisters: assertion transformation**

```
إن وأخواتها تحول الإسناد توكيديًا أو نصبيًا.
```

Inna and sisters transform predication assertively or with nasb.

**Example:**
```
زيد قائم     → Direct predication
إن زيدًا قائم → Assertion predication (Indeed, Zayd [is] standing)
```

---

#### Law 10: ظن وأخواتها تحويل إبستيمي
**Ẓanna and sisters: epistemic transformation**

```
ظن وأخواتها تحول الإسناد إبستيميًا.
```

Ẓanna and sisters transform predication epistemically.

**Example:**
```
زيد قائم        → Direct predication
ظننت زيدًا قائمًا → Epistemic predication (I thought Zayd [was] standing)
```

---

#### Law 11: كاد وأخواتها تحويل قرب
**Kāda and sisters: near-occurrence transformation**

```
كاد وأخواتها تحول الإسناد إلى قرب وقوع.
```

Kāda and sisters transform predication to near-occurrence.

---

#### Law 12: أفعال الشروع تحويل ابتداء
**Inception verbs: beginning transformation**

```
أفعال الشروع تحول الإسناد إلى ابتداء تحقق.
```

Inception verbs transform predication to beginning of realization.

---

#### Law 13: لا إفادة إلا بإغلاق الإسناد
**No ifadah without predication closure**

```
لا إفادة دالية إلا إذا أغلقت النسبة الإسنادية أو عُلم تقديرها.
```

No dal ifadah unless predicative relation closes or its estimation is known.

---

#### Law 14: لا حكم من الإسناد وحده
**No judgment from predication alone**

```
لا حكم من الإسناد وحده.
```

No judgment from predication alone.

---

#### Law 15: لا واقع من الإسناد وحده
**No reality from predication alone**

```
لا واقع من الإسناد وحده.
```

No reality from predication alone.

---

### 6. مثال إسنادي كامل
### Complete Predicative Example

```python
# Input
input_text = "زيد قائم"
wordforms = [
    WordformCandidate(lafz="زيد", type=ISM),
    WordformCandidate(lafz="قائم", type=ISM_MUSHAQ)
]

# Operation
anchor = detect_anchor(wordforms[0])        # زيد
predicate = detect_predicate(wordforms[1])  # قائم
compatible = test_compatibility(anchor, predicate)  # entity + attribute/state
edge = build_predicative_edge(anchor, predicate)

# Output
result = PredicativeRelationCandidate(
    anchor="زيد",
    predicate="قائم",
    relation_type=RelationType.PREDICATION,
    rank=Rank.STRONG_HYPOTHESIS,
    residuals=[],
    trace=["detect_anchor", "detect_predicate", "build_edge"],
    forbidden=["final_meaning", "hukm", "reality"]
)
```

**تفسير المخرج (Output Interpretation):**

```
المخرج ليس حكمًا بأن زيدًا قائم في الواقع.
المخرج فقط: الدال أغلق علاقة إسنادية.

Output is NOT judgment that Zayd is actually standing.
Output only: The signifier closed a predicative relation.
```

---

## القسم الثاني: خوارزمية النسبة التضمينية
## Part II: Inclusion Relation Algorithm

### 7. تعريف النسبة التضمينية
### Inclusion Relation Definition

**النسبة التضمينية:**

علاقة يكون فيها طرف داخل مجال طرف آخر، أو جزءًا من مفهومه، أو تابعًا له من جهة الجنس أو النوع أو الخاصية أو اللزوم الداخلي.

A relation where one term is within the domain of another, or part of its concept, or follows it in terms of genus/species/property/internal entailment.

**أمثلة (Examples):**

#### Example 1: Genus-Species
```
الإنسان حيوان ناطق

إنسان ⊂ حيوان (Human ⊂ Animal)
ناطق = فصل/خاصية مميزة (Distinguishing differentia)
```

This is NOT mere predication; it's taxonomic inclusion.

#### Example 2: Part-Whole
```
السقف من البيت

السقف داخل بنية البيت (Ceiling within house structure)
```

---

### 8. خوارزمية النسبة التضمينية
### Inclusion Relation Algorithm

```python
Algorithm: build_inclusion_relation

Input:
    ConceptualOrDalCandidateSet

Carrier:
    container_candidate      # حاوٍ
    contained_candidate      # محتوى
    genus_candidate         # جنس
    species_candidate       # نوع
    part_candidate          # جزء
    whole_candidate         # كل
    attribute_candidate     # صفة داخلة
    implication_candidate   # لازم

Prior:
    genus_species_registry    # سجل الجنس والنوع
    part_whole_registry      # سجل الكل والجزء
    lexical_inclusion_rules  # قواعد التضمين المعجمي
    semantic_field_registry  # سجل الحقول الدلالية
    entailment_rules        # قواعد اللزوم
    idafa_rules             # قواعد الإضافة
    min_operator_registry   # سجل عوامل "من"
    residual_policy         # سياسة البقايا

Gate:
    inclusion_license_gate

Operation:
    detect_possible_container
    detect_possible_contained
    classify_inclusion_type
    test_genus_species
    test_part_whole
    test_attribute_inclusion
    test_lexical_entailment
    test_operator_marker
    preserve_anchor_identity
    build_inclusion_edge

Identity:
    preserve_container_or_genus_identity

Candidate:
    InclusionRelationCandidate

Residuals:
    uncertain_genus
    uncertain_part_whole
    metaphor_possible
    weak_inclusion_marker
    competing_classification
    lexical_gap
    domain_mismatch

Rank:
    candidate | hypothesis | strong_hypothesis | certificate

Output:
    InclusionRelationCandidate

Forbidden:
    final_contextual_meaning
    hukm
    reality
```

---

### 9. أنواع النسبة التضمينية (7 Types)
### Inclusion Relation Types

1. **Genus-Species Inclusion** (جنس / نوع)
   ```
   الإنسان حيوان
   Human ⊂ Animal
   ```

2. **Whole-Part Inclusion** (كل / جزء)
   ```
   اليد من الجسم
   Hand ⊂ Body
   ```

3. **Attribute Inclusion** (ذات / صفة داخلة)
   ```
   النطق من الإنسان
   Speech ⊂ Human nature
   ```

4. **Field Inclusion** (مجال / عنصر)
   ```
   النحو من علوم العربية
   Grammar ⊂ Arabic sciences
   ```

5. **Lexical Entailment** (تضمين معجمي)
   ```
   القتل يتضمن الموت
   Killing entails death
   ```

6. **Conceptual Entailment** (لزوم مفهومي)
   ```
   الأبوة تستلزم الولد
   Fatherhood entails child
   ```

7. **Functional Inclusion** (أداة / وظيفة)
   ```
   المفتاح من القفل
   Key ⊂ Lock system
   ```

---

### 10. قوانين النسبة التضمينية (15 Laws)
### Inclusion Relation Laws

#### Law 1-7: الشروط الأساسية (Basic Conditions)

1. لا تضمين بلا مجال حاوٍ ومندرج
2. لا جزء بلا كل مرخّص
3. لا نوع بلا جنس أو مجال تصنيف
4. لا صفة داخلة بلا حامل هوية
5. لا لزوم بلا جهة لزوم
6. لا تضمين معجمي بلا شاهد أو قاعدة
7. لا تضمين اصطلاحي بلا مجال اصطلاح

#### Law 8: بوابة النقل للمجاز (Transfer gate for metaphor)

```
لا تضمين مجازي إلا ببوابة نقل.
```

No metaphorical inclusion except through transfer gate.

#### Law 9-10: المنع (Prohibitions)

9. التضمين لا ينتج حكمًا
10. التضمين لا ينتج واقعًا

#### Law 11: التضمين يفتح الإمكان
**Inclusion opens possibility**

```
التضمين يفتح إمكان الإفادة، ولا يغلقها وحده.
```

Inclusion opens ifadah possibility; does NOT close it alone.

#### Law 12-13: الأثر والبقايا (Trace and residuals)

12. كل تضمين يجب أن يترك trace
13. كل تضمين يجب أن يحمل residual audit

#### Law 14-15: التعدد والتعارض (Multiplicity and conflict)

14. إذا تعددت مجالات التضمين انخفضت الرتبة
15. إذا تعارض التضمين مع السياق توقف الإغلاق

---

### 11. مثال تضميني كامل
### Complete Inclusion Example

```python
# Input
input_text = "الإنسان حيوان ناطق"
concepts = [
    ConceptCandidate(term="الإنسان", type=SPECIES),
    ConceptCandidate(term="حيوان", type=GENUS),
    ConceptCandidate(term="ناطق", type=DIFFERENTIA)
]

# Operation
species = detect_species(concepts[0])     # الإنسان
genus = detect_genus(concepts[1])         # حيوان
diff = detect_differentia(concepts[2])    # ناطق
edge1 = build_genus_species_edge(species, genus)
edge2 = build_attribute_inclusion_edge(species, diff)

# Output
result = InclusionRelationCandidate(
    included="الإنسان",
    container="حيوان",
    inclusion_type=InclusionType.GENUS_SPECIES,
    qualifier="ناطق",
    rank=Rank.STRONG_HYPOTHESIS,
    residuals=["definition_scope"],
    trace=["detect_species", "detect_genus", "build_edges"],
    forbidden=["final_meaning", "hukm", "reality"]
)
```

**تفسير المخرج (Output Interpretation):**

```
المخرج ليس حكمًا أن كل إنسان في الواقع كذا.
بل هو عقد تضميني دالي/مفهومي يحتاج لاحقًا إلى مطابقة ودليل إذا أريد الحكم.

Output is NOT judgment that every human in reality is thus.
Rather, it's a dal/conceptual inclusion contract needing later matching and evidence for judgment.
```

---

## القسم الثالث: خوارزمية النسبة التقييدية
## Part III: Restrictive Relation Algorithm

### 12. تعريف النسبة التقييدية
### Restrictive Relation Definition

**النسبة التقييدية:**

ربط يضيّق مجال الحامل أو الحدث أو الحكم الدالي دون أن ينشئ حكمًا نهائيًا.

A linking that narrows the domain of the anchor/event/dal judgment without creating final judgment.

**أمثلة (Examples):**

```
رجل كريم          → كريم restricts رجل (attribute restriction)
جاء زيد صباحًا     → صباحًا restricts المجيء (temporal restriction)
ضربت زيدًا تأديبًا  → تأديبًا restricts الضرب (purposive restriction)
كتاب الطالب       → الطالب restricts كتاب (possessive restriction via idafa)
```

---

### 13. خوارزمية النسبة التقييدية
### Restrictive Relation Algorithm

```python
Algorithm: build_restrictive_relation

Input:
    WordformCandidateSet
    RelationCandidateSet

Carrier:
    base_candidate          # مقيد (restricted base)
    restrictor_candidate    # قيد (restrictor)
    restriction_type        # نوع القيد
    modifier_edge          # حافة التعديل
    case_trace             # أثر إعرابي
    idafa_trace            # أثر إضافة
    adjective_trace        # أثر وصف
    adverbial_trace        # أثر ظرف
    prepositional_trace    # أثر جر

Prior:
    adjective_rules        # قواعد الصفة
    idafa_rules           # قواعد الإضافة
    hal_rules             # قواعد الحال
    tamyiz_rules          # قواعد التمييز
    zarf_rules            # قواعد الظرف
    jar_majrur_rules      # قواعد الجر
    restriction_scope_rules  # قواعد مجال القيد
    attachment_rules      # قواعد التعلق
    ellipsis_policy       # سياسة الحذف

Gate:
    restriction_license_gate

Operation:
    detect_base
    detect_restrictor
    classify_restriction_type
    test_attachment
    test_scope
    test_case_or_link_marker
    test_compatibility
    build_restriction_edge
    preserve_base_identity

Identity:
    preserve_base_identity_under_restriction

Candidate:
    RestrictiveRelationCandidate

Residuals:
    ambiguous_attachment
    wide_scope_possible
    narrow_scope_possible
    weak_marker
    hidden_base_possible
    competing_restrictor
    case_uncertainty

Rank:
    candidate | hypothesis | strong_hypothesis | certificate

Output:
    RestrictiveRelationCandidate

Forbidden:
    final_meaning
    hukm
    reality
```

---

### 14. أنواع النسبة التقييدية (14 Types)
### Restrictive Relation Types

1. **وصفية (Attributive)**: رجل كريم
2. **إضافية (Possessive)**: كتاب الطالب
3. **ظرفية (Adverbial)**: جاء صباحًا
4. **حالية (Circumstantial)**: جاء زيد راكبًا
5. **تمييزية (Specificative)**: طاب زيد نفسًا
6. **جرية/حرفية (Prepositional)**: مررت بزيد
7. **شرطية (Conditional)**: إن تدرس تنجح
8. **غائية (Purposive)**: جئت طلبًا للعلم
9. **سببية (Causal)**: مات خوفًا
10. **عددية (Numerical)**: ثلاثة رجال
11. **استثنائية (Exceptive)**: جاء القوم إلا زيدًا
12. **حصرية (Restrictive/Exclusive)**: ما جاء إلا زيد
13. **موصولية (Relative)**: جاء الذي نجح
14. **إحالية (Referential)**: هذا الرجل

---

### 15. قوانين النسبة التقييدية (15 Laws)
### Restrictive Relation Laws

#### Law 1-2: الأساس (Foundation)

1. لا قيد بلا مقيد
2. لا مقيد بلا هوية محفوظة

#### Law 3-9: طبيعة القيد (Nature of restriction)

3. القيد يضيق المجال ولا يخلق الأصل
4. الصفة لا تنشئ الموصوف
5. الإضافة لا تنشئ المضاف، بل تقيد هويته
6. الظرف لا ينشئ الحدث، بل يحدد زمانه أو مكانه
7. الحال لا تنشئ صاحب الحال، بل تقيد هيئة وقوعه
8. التمييز لا ينشئ الذات، بل يرفع إبهام النسبة أو المقدار
9. الجار والمجرور يربط بعامل أو متعلق مرخّص

#### Law 10-12: العمليات الخاصة (Special operations)

10. الشرط لا ينتج حكمًا، بل يربط تحققًا بتحقق
11. الاستثناء لا يعمل إلا داخل مجال سابق
12. الحصر يضيق المجال ولا يثبت الواقع

#### Law 13-15: الشروط النهائية (Final conditions)

13. القيد لا ينتج معنى نهائيًا بلا سياق
14. إذا تعدد مجال القيد وجب حفظ البقايا
15. إذا غاب المقيد وجب تقديره ببوابة تقدير لا بتخمين

---

### 16. مثال تقييدي كامل
### Complete Restrictive Example

```python
# Input
input_text = "رجل كريم"
wordforms = [
    WordformCandidate(lafz="رجل", type=ISM_JAMID),
    WordformCandidate(lafz="كريم", type=ISM_MUSHAQ)
]

# Operation
base = detect_base(wordforms[0])           # رجل
restrictor = detect_restrictor(wordforms[1])  # كريم
type_ = classify_restriction_type(restrictor)  # attribute
agreement = test_agreement(base, restrictor)  # True
edge = build_restrictive_edge(base, restrictor, type_)

# Output
result = RestrictiveRelationCandidate(
    base="رجل",
    restrictor="كريم",
    restriction_type=RestrictionType.ATTRIBUTE,
    rank=Rank.STRONG_HYPOTHESIS,
    residuals=[],
    trace=["detect_base", "detect_restrictor", "test_agreement", "build_edge"],
    forbidden=["final_meaning", "hukm", "reality"]
)
```

**تفسير المخرج (Output Interpretation):**

```
المخرج: رجل مقيد بصفة الكرم

NOT: هذا الرجل موجود في الواقع
NOT: حكم شرعي أو واقعي

Output: Man restricted by attribute of generosity
NOT: This man exists in reality
NOT: Legal or factual judgment
```

---

## القسم الرابع: شبكة النسب
## Part IV: Relation Network

### 17. ترتيب النسب داخل التركيب
### Relation Ordering in Composition

**النسب لا تعمل معزولة، بل داخل شبكة.**

Relations do NOT work in isolation, but within a network.

```
WordformCandidate
    ↓ [relation building]
RelationCandidate {
    PredicativeRelation,
    InclusionRelation,
    RestrictiveRelation,
    ReferenceRelation,
    OperatorRelation
}
    ↓ [network closure]
RelationNetwork
    ↓ [ifadah closure gate]
Ifadah_Dal
```

### شروط الإغلاق (Closure Conditions):

لا تغلق الإفادة إلا إذا تحققت:

1. ✅ الأطراف معروفة أو مقدرة بترخيص
2. ✅ العلاقات مصنفة
3. ✅ الحواف غير متعارضة
4. ✅ الإحالة مستقرة بالرتبة الكافية
5. ✅ البقايا غير مانعة
6. ✅ الرتبة كافية للإغلاق

---

### 18. خوارزمية إغلاق شبكة النسب
### Relation Network Closure Algorithm

```python
Algorithm: close_relation_network

Input:
    RelationCandidateSet

Carrier:
    predicative_edges      # حواف إسنادية
    inclusion_edges        # حواف تضمينية
    restrictive_edges      # حواف تقييدية
    reference_edges        # حواف إحالية
    operator_edges         # حواف عاملية
    residual_set          # مجموعة بقايا
    rank_set              # مجموعة رتب

Prior:
    ifadah_closure_rules       # قواعد إغلاق الإفادة
    contradiction_policy       # سياسة التعارض
    relation_priority_rules    # قواعد أولوية النسب
    residual_policy           # سياسة البقايا
    rank_policy               # سياسة الرتب

Gate:
    ifadah_dal_closure_gate

Operation:
    collect_edges
    test_edge_compatibility
    test_anchor_preservation
    test_relation_conflict
    test_reference_completion
    test_residual_blockers
    compute_network_rank
    close_ifadah_if_licensed

Identity:
    preserve_relation_trace

Candidate:
    IfadahDalCandidate

Residuals:
    unresolved_reference
    relation_conflict
    weak_predication
    competing_attachment
    missing_operator
    excessive_ellipsis
    semantic_leak_risk

Rank:
    candidate | hypothesis | strong_hypothesis | certificate

Output:
    Ifadah_Dal
    OR OpenRelationNetworkCandidate

Forbidden:
    contextual_final_meaning
    hukm
    reality
```

---

## القسم الخامس: قوانين المنع
## Part V: Prohibition Laws

### 19. ممنوعات النسبة
### Relation Prohibitions

#### Forbidden Jumps (القفزات الممنوعة):

```python
# Predicative Relation Prohibitions
❌ PredicativeRelation → Hukm
❌ PredicativeRelation → Reality

# Inclusion Relation Prohibitions
❌ InclusionRelation → Hukm
❌ InclusionRelation → Reality

# Restrictive Relation Prohibitions
❌ RestrictiveRelation → Hukm
❌ RestrictiveRelation → Reality

# Network Prohibitions
❌ RelationNetwork → Reality (without Madlul + Evidence)

# Ifadah Prohibitions
❌ Ifadah_Dal → Hukm (without Evidence)

# Contract Prohibitions
❌ DalMadlulContract → Reality (without Tanzil)
```

---

### 20. قوانين الحفظ (8 Laws)
### Preservation Laws

1. **كل نسبة تحفظ anchor_id**
   Every relation preserves anchor_id

2. **كل نسبة تحفظ trace**
   Every relation preserves trace

3. **كل نسبة تنتج residual audit**
   Every relation produces residual audit

4. **كل نسبة لا ترفع الرتبة بلا دليل داخلي**
   No relation raises rank without internal evidence

5. **كل نسبة لا تنتج طبقة أعلى من طبقتها**
   No relation produces higher layer than its own

6. **كل نسبة يجب أن تصرح بنوعها**
   Every relation must declare its type

7. **كل نسبة يجب أن تصرح بمجالها**
   Every relation must declare its scope

8. **كل نسبة يجب أن تصرح بأثرها**
   Every relation must declare its effect

---

## 21. الخلاصة الجامعة
## Comprehensive Summary

### الصيغة الجامعة (Universal Formulation):

```python
PredicativeRelation:
    يحمل شيئًا على شيء
    Carries something onto something
    (Predication)

InclusionRelation:
    يدخل شيئًا في شيء
    Places something within something
    (Inclusion)

RestrictiveRelation:
    يقيّد شيئًا بشيء
    Restricts something by something
    (Restriction)
```

### القانون المركزي (Central Law):

```
والإفادة الدالية لا تحصل إلا حين تغلق شبكة هذه النسب
مع العامل، والإحالة، والرتبة، والبقايا.

Dal ifadah occurs ONLY when this relation network closes
with operator, reference, rank, and residuals.
```

### الخلاصة التنفيذية (Executive Summary):

```
النسبة الإسنادية = حمل (Predication = Carrying)
النسبة التضمينية = إدخال (Inclusion = Placing within)
النسبة التقييدية = تضييق (Restriction = Narrowing)

لكن الثلاثة لا يملكون حق إنتاج الحكم.
هم فقط يبنون شبكة دالية مرخّصة
تصلح بعد ذلك لجبر المدلول السياقي والمطابقة والدليل.

But the three do NOT possess the right to produce judgment.
They only build a licensed dal network
suitable thereafter for contextual madlul algebra, matching, and evidence.
```

---

## المراجع الدستورية
## Constitutional References

This appendix operates under the authority of:
- `ARABIC_ALGEBRA_ALGORITHM_CONSTITUTION.md`
- RelationAlgebraCore (src/dal_core/relation_algebra_core.py)
- Constitutional Law: لا U₁₁ قبل RelationAlgebraCore

**Enforcement**: All relation algorithm implementations MUST comply with this appendix.

---

**والله أعلم**
**And Allah knows best**
