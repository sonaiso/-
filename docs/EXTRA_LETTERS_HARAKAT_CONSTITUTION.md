# Extra Letters and Harakāt Constitution
## دستور الأحرف والحركات الزائدة في جبر الخانات

**Document Type**: Constitutional Extension to Slot Geometry Algebra
**Status**: Theoretical Specification (Pre-Implementation)
**Version**: 1.0.0
**Date**: 2026-05-28
**Dependencies**: SLOT_GEOMETRY_ALGEBRA_CONSTITUTION.md

---

## Executive Summary | الملخص التنفيذي

**الأصل الجبري:**

> الحرف الزائد = إزاحة خانوية مرخّصة، لا معنى نهائي

**The Algebraic Principle:**

> Extra Letter = Licensed slot displacement, NOT final meaning

**Critical Distinction**:
```
DerivationalAugmentation (في المشتق)
≠
NonDerivationalSlotGeometry (في المبني والجامد)
```

---

## 1. Algebraic Definition of Extra Letter | تعريف الحرف الزائد جبريًا

### 1.1 The Definition

```
ExtraLetter =
  Carrier
  + NonOriginalSlot
  + License
  + StructuralEffect
  + PreservedOrigin
  + ResidualAudit
  + Rank
  + STOP before meaning
```

### 1.2 Constitutional Statement

**Extra letter does NOT mean final meaning by itself.**
**It is slot displacement (إزاحة خانوية).**

---

## 2. The Grand Laws of Extra Letters | القوانين الكبرى للأحرف الزائدة

### Law 1: No Augmentation Without Preserved Origin
### القانون 1: لا زيادة بلا أصل محفوظ

**Statement**:
```
لا حرف زائد بلا أصل محفوظ أو جذع محفوظ
No extra letter without preserved root or preserved stem
```

**Formal**:
```
ExtraLetter(x) ⇒ ∃ Origin(o) such that Preserve(o)
```

**Preserved Origin Types**:
- Root (جذر)
- Stem (جذع)
- FixedBase (قاعدة ثابتة)

**If No Preserved Origin**:

The utterance does NOT immediately enter augmentation domain, but may be:
- Jāmid (frozen noun)
- Mabni (fixed form)
- Dakhīl (loanword)
- 'Alam (proper name)
- Ḥarf ma'nā (meaning particle)
- Ḍamīr (pronoun)
- Residual (بقايا)

---

### Law 2: No Augmentation Without Non-Original Slot
### القانون 2: لا زيادة بلا خانة غير أصلية

**Statement**:
```
الحرف لا يكون زائدًا لمجرد وجوده، بل لأنه دخل خانة غير أصلية
A letter is NOT extra merely by existing, but because it occupies a non-original slot
```

**Formal**:
```
ExtraLetter(x) ⇔ Carrier(x) ∧ Occupies(x, NonOriginalSlot)
```

**Critical Consequence**:

The same letter may be:
- Original in one word
- Extra in another word

**Example**:
```
س in سأل = original
س in استغفر = extra (request/augmented pattern slot)
```

---

### Law 3: No Augmentation Without License
### القانون 3: لا زيادة بلا ترخيص

**Statement**:
```
لا يدخل الحرف خانة زائدة إلا بترخيص
A letter does NOT enter extra slot except with license
```

**License Types**:
1. **Waznī** (وزني) - Pattern-based
2. **Ṣarfī** (صرفي) - Morphological
3. **Samā'ī** (سماعي) - Auditory/usage-based
4. **Binā'ī** (بنائي) - Construction-based
5. **Taṣrīfī** (تصريفي) - Inflectional
6. **Rasmī/Imlā'ī** (رسمي/إملائي) - Orthographic
7. **Waẓīfī** (وظيفي) - Functional (for particles/mabni)

**Formal**:
```
NonOriginalSlot(x) requires License(x)
```

**If License Absent**:
```
ExtraLetterCandidate → Residual
```

---

### Law 4: Augmentation Changes Geometry, NOT Meaning
### القانون 4: الزيادة تغيّر الهندسة لا المعنى

**Statement**:
```
الزيادة تغيّر هندسة الخانات ولا تثبت المعنى النهائي
Augmentation changes slot geometry and does NOT establish final meaning
```

**Formal**:
```
Augmentation ≠ Meaning
Augmentation = SlotRedistribution
```

**Augmented Patterns**:
```
أفعل (af'ala)
فعّل (fa''ala)
استفعل (istaf'ala)
تفاعل (tafā'ala)
انفعل (infa'ala)
```

**These Are NOT final meanings, but slot redistribution methods around origin.**

---

### Law 5: Augmentation Opens Potential, NOT Judgment
### القانون 5: الزيادة تفتح احتمالًا لا حكمًا

**Statement**:
```
الحرف الزائد يفتح احتمالًا، لا يثبت حكمًا
Extra letter opens potential, does NOT establish judgment
```

**Potentials Opened**:
- Morphological potential (احتمال صرفي)
- Event potential (احتمال حدثي)
- Functional potential (احتمال وظيفي)
- Future predicational potential (احتمال إسنادي لاحق)
- Referential potential (احتمال إحالي)
- Operator potential (احتمال عاملي)

**Does NOT Establish**:
- Final meaning (معنى نهائي)
- Reality judgment (حكم واقعي)
- Syntactic function (وظيفة نحوية)
- Complete relation (علاقة مكتملة)
- Ifādah (إفادة)

**Formal**:
```
ExtraLetterEffect = Potential
ExtraLetterEffect ≠ FinalMeaning
```

---

### Law 6: Augmentation Preserves Trace and Residuals
### القانون 6: الزيادة تحفظ الأثر والبقايا

**Statement**:
```
كل زيادة يجب أن تحفظ Trace وتنتج ResidualAudit
Every augmentation must preserve Trace and produce ResidualAudit
```

**Formal**:
```
ExtraLetter(x) ⇒ Trace(x) ∧ ResidualAudit(x)
```

**Reason**:

Augmentation may be:
- Standard (قياسية)
- Auditory (سماعية)
- Potential (محتملة)
- Ambiguous (ملتبسة)
- Unlicensed (غير مرخصة)
- Constructional not derivational (بنائية لا اشتقاقية)

---

### Law 7: Augmentation Rank Does Not Exceed License Rank
### القانون 7: رتبة الزيادة لا تتجاوز دليلها

**Statement**:
```
رتبة الزيادة تساوي قوة ترخيصها
Augmentation rank equals license strength
```

**Formal**:
```
Rank(ExtraLetter) ≤ Rank(License)
```

**If License is Strong Pattern-Based**:
```
Rank = strong hypothesis / verbal certificate
```

**If License is Auditory or Ambiguous**:
```
Rank = hypothesis / candidate
```

---

## 3. Laws of Extra Harakāt | قوانين الحركات الزائدة

### 3.1 Definition

**Extra Ḥaraka is NOT a letter, but extra operation.**

```
ExtraHaraka =
  Operation
  + NonOriginalHarakaSlot
  + License (phonological/morphological/constructional/i'rāb/auditory)
  + PhonoMorphologicalEffect
  + Residuals
  + Rank
  + STOP before meaning
```

**Formal**:
```
ExtraHaraka =
  OperationalModifier
  + NonOriginalHarakaSlot
  + License
  + PhonoMorphologicalEffect
  + Residuals
  + Rank
  + STOP before meaning
```

---

### 3.2 Law of Extra Ḥaraka

**Statement**:
```
الحركة الزائدة تغيّر التشغيل لا المادة
Extra ḥaraka changes operation, NOT material
```

**Examples of Extra Ḥaraka**:
- Connection ḥaraka (حركة وصل)
- Ḥaraka to avoid double sukūn (حركة تخلص من التقاء الساكنين)
- Construction ḥaraka (حركة بناء)
- Incidental ḥaraka (حركة عارضة)
- Potential i'rāb ḥaraka (حركة إعرابية محتملة)
- Pattern ḥaraka (حركة وزن)
- Transfer ḥaraka (حركة نقل)

**Does NOT Give Final Meaning.**

---

## 4. Difference: Extra Letter vs Extra Ḥaraka | الفرق بين الحرف الزائد والحركة الزائدة

### 4.1 The Distinction

```
ExtraLetter = زيادة Carrier داخل Slot
             (Carrier addition within slot)

ExtraHaraka = زيادة Operation على Carrier
             (Operation addition on carrier)
```

**Formal**:
```
ExtraLetter modifies structure by adding a carrier
ExtraHaraka modifies operation by changing activation
```

---

### 4.2 Example: استغفر

**Extra Letters**: س، ت، ألف
- Change slot geometry

**Extra Ḥaraka**: اِستغفر (hamzat waṣl + its ḥaraka)
- Opens pronunciation
- Does NOT add final meaning

---

## 5. Critical Constraint: Augmentation Does Not Work Uniformly
## القيد المهم: الزيادة لا تعمل في كل الأبواب بالطريقة نفسها

### 5.1 The Problem

**Extra letters and extra harakāt do NOT work in:**
- Mabni forms (المبنيات)
- Mujarrad verbs (الأفعال المجردة)
- Mabni nouns (الأسماء المبنية)
- Mabni particles (الحروف المبنية)

**By the same logic as derivational augmentation.**

---

### 5.2 The Solution: Two Types of Augmentation

#### Type A: Derivational Augmentation (زيادة اشتقاقية)

Works in derived and augmented forms:
```
Root → Pattern → ExtraLetters → TransformedPattern
```

**Examples**:
```
فعل → أفعل
فعل → فعّل
فعل → استفعل
```

**Name**: `DerivationalExtraLetter`

**Opens**: Event or morphological potential

---

#### Type B: Non-Derivational / Constructional Augmentation (زيادة غير اشتقاقية / بنائية)

Works in mabni, particles, pronouns, demonstratives, particles, some frozen nouns.

**Examples**:
```
هذا، الذي، التي، من، ما، إن، أن، لكن، حيث، إذ، إذا
```

**Here we do NOT say** the letter is extra in derivational morphological sense.

**Rather**: Letter is part of `FixedSlotGeometry`

Or: `BuiltFormSlot`

**Meaning**: Inside closed mabni geometry, not inside root + pattern.

---

## 6. Law: Mabni Blocks Derivational Augmentation
## القانون 6: منع الزيادة الاشتقاقية في المبنيات

### 6.1 Statement

```
لا تُفسَّر المبنيات بمنطق الزيادة الاشتقاقية إلا بدليل خاص
Mabni forms are NOT interpreted by derivational augmentation logic except with special evidence
```

**Formal**:
```
MabniPath blocks DerivationalAugmentation
unless SpecialLicense
```

---

### 6.2 Example: هذا

**We do NOT analyze** as: root + augmentation (derivational sense).

**Rather**:
```
هذا =
  Carrier
  + FixedSlots
  + DemonstrativeClassSlots
  + ReferencePotential
  + TerminalStability
  + STOP before meaning
```

---

## 7. Law: Mujarrad Verbs
## القانون 7: الأفعال المجردة

### 7.1 Statement

```
الفعل المجرد لا يحمل أحرف زيادة اشتقاقية داخل بنيته الأصلية
Mujarrad verb does NOT carry derivational extra letters inside its original structure
```

**Examples**:
```
كتب، ضرب، علم، كرم
```

**Path**:
```
Carrier
  → RootSlots
  → MujarradPatternSlots
  → VerbFormCandidate
  → EventPotential
  → STOP before meaning
```

**We do NOT say**: `ExtraLetter`

Except when a letter appears outside its origin via:
- Inflection (تصريف)
- Attachment (إلحاق)
- Pronoun (ضمير)
- Particle (أداة)

---

### 7.2 Formal

```
MujarradVerbPath blocks InternalDerivationalExtraLetter
```

**But ALLOWS**:
- PrefixSlot
- SuffixSlot
- PronounAttachmentSlot
- TenseMarkerSlot
- PersonNumberGenderSlot

**These are NOT derivational augmentation inside origin, but inflectional/compositional slots later.**

---

## 8. Law: Mabni Nouns
## القانون 8: الأسماء المبنية

### 8.1 Statement

```
الأسماء المبنية لا تُفتح على زيادة اشتقاقية قياسية
Mabni nouns are NOT opened to standard derivational augmentation
```

**Rather, treated as**:
```
MabniNoun =
  Carrier
  + FixednessConstraint
  + ClassSpecificSlots
  + Reference/OperatorPotential
  + TerminalStability
  + Residuals
  + Rank
  + STOP before meaning
```

---

### 8.2 Examples

```
هذا، هذه، الذي، التي، من، ما، أين، متى، كيف، حيث، إذ، إذا
```

**These are NOT**:
```
Root + ExtraLetters + Pattern
```

**But**:
```
FixedSlotTemplate
```

---

## 9. Law: Mabni Particles
## القانون 9: الحروف المبنية

### 9.1 Statement

```
حروف المعاني مبنية على صورة وظيفية مغلقة، لا على زيادة اشتقاقية
Meaning particles are built on closed functional form, not derivational augmentation
```

**Examples**:
```
من، إلى، في، على، لم، لن، إن، أن، هل، قد، بل، لكن
```

---

### 9.2 We Do NOT Say

```
اللام زائدة (lām is extra)
النون زائدة (nūn is extra)
الألف زائدة (alif is extra)
```

Except with special historical or auditory evidence that does NOT enter first operational algebra.

---

### 9.3 Rather We Say

```
Particle =
  Carrier
  + OperatorFixedSlots
  + OperatorPotential
  + TerminalStability
  + STOP before applied operation
```

---

## 10. Unified Geometry After Mabni | هندسة الخانات الجامعة بعد المبنيات

### 10.1 Need

We need geometry covering what extra letters/harakāt did, but without forcing derivation on mabni.

---

### 10.2 Proposed Name

```
PostMabniSlotGeometry
```

Or more precisely:
```
NonDerivationalSlotGeometry
```

---

### 10.3 Coverage

Covers:
- Mabni (المبني)
- Particle (الأداة)
- Pronoun (الضمير)
- Demonstrative (اسم الإشارة)
- Relative (اسم الموصول)
- Conditional noun (اسم الشرط)
- Interrogative noun (اسم الاستفهام)
- Mujarrad verb (الفعل المجرد)
- Frozen noun (الاسم الجامد)
- Whatever does NOT follow Root + Augmentation

---

## 11. General Formula | الصيغة العامة

### 11.1 NonDerivationalSlotGeometry

```
NonDerivationalSlotGeometry =
  Carrier
  + FixedBaseSlot
  + ClassSpecificSlots
  + TerminalStability
  + LicensedPotential
  + AttachmentSlots
  + OperationalHarakaSlots
  + Residuals
  + Rank
  + STOP before meaning
```

---

### 11.2 Functional Mapping

What augmentation did in mushtaq → its replacement in mabni/jāmid/particle:

| Function in Mushtaq | Replacement in Mabni/Jāmid/Particle |
|---------------------|-------------------------------------|
| Pattern change | FixedTemplateSlot |
| Event opening | ClassSpecificPotential |
| Agent/patient potential | OperatorPotential or ReferencePotential |
| Structure change | FixedBaseSlot + ClassSlots |
| Inflectional effect | AttachmentSlot |
| Phonological operation | OperationalHarakaSlot |
| Functional effect | LicensedPotential |
| Rank and residuals | Residuals + Rank |

---

## 12. Post-Mabni Slots | خانات ما بعد المبنيات

### 12.1 Minimum Complete Set (25 Slots)

1. **CarrierSlot**
2. **FixedBaseSlot**
3. **TerminalStabilitySlot**
4. **ClassSpecificSlot**
5. **OperatorPotentialSlot**
6. **ReferencePotentialSlot**
7. **MissingValueSlot**
8. **ConditionSlot**
9. **ExpectedCompletionSlot**
10. **AttachmentSlot**
11. **PronounAttachmentSlot**
12. **DeicticSlot**
13. **RelativeṢilahSlot**
14. **InterrogativeSlot**
15. **ConditionalSlot**
16. **NegationSlot**
17. **EmphasisSlot**
18. **TemporalOperatorSlot**
19. **CaseBlockingSlot**
20. **OperationalHarakaSlot**
21. **PhonologicalSupportSlot**
22. **OrthographicSupportSlot**
23. **ResidualSlot**
24. **RankSlot**
25. **StopBeforeMeaningGate**

**These cover augmentation function without calling it derivational augmentation.**

---

## 13. Law of Compensation for Augmentation
## القانون 13: التعويض عن الزيادة

### 13.1 Statement

```
حيث تمنع الزيادة الاشتقاقية، تعمل خانات الصنف والثبات والوظيفة بدلها
Where derivational augmentation is blocked, class/stability/functional slots work instead
```

**Formal**:
```
If DerivationalAugmentation is blocked,
then ClassSpecificSlots provide structural potential
```

---

### 13.2 Example: من

**We do NOT say**:
```
ميم أصلية ونون زائدة
Mīm original, nūn extra
```

**Rather**:
```
من =
  Carrier
  + MabniFixedSlots
  + Interrogative/Conditional/RelativePotential
  + MissingValueSlot or ReferenceSlot
  + Residuals
  + Rank
  + STOP
```

---

## 14. Mujarrad Verb Geometry Without Extra Letters | هندسة الفعل المجرد بلا أحرف زائدة

### 14.1 Definition

```
MujarradVerbSlotGeometry =
  Carrier
  + RootSlots
  + BarePatternSlots
  + TenseFormSlot
  + VoicePotentialSlot
  + ValencyPotentialSlot
  + Person/Number/GenderPotential
  + Residuals
  + Rank
  + STOP before meaning
```

---

### 14.2 Law

```
الفعل المجرد لا يحتاج حرفًا زائدًا ليُنتج مدلولًا لفظيًا
Mujarrad verb does NOT need extra letter to produce verbal signified
```

**Because it produces from**:
```
RootSlots + BarePatternSlots
```

**NOT from**:
```
RootSlots + ExtraLetterSlots
```

---

## 15. Mazīd Verb Geometry | هندسة الفعل المزيد

### 15.1 Definition (For Comparison)

```
MazidVerbSlotGeometry =
  Carrier
  + PreservedRootSlots
  + ExtraLetterSlots
  + AugmentedPatternSlots
  + TransformationSlots
  + EventPotentialSlot
  + ValencyPotentialSlot
  + Residuals
  + Rank
  + STOP before meaning
```

---

### 15.2 Law

```
الزيادة في المزيد تحوّل بنية الحدث المحتملة،
لكن لا تثبت معنى الحدث ولا تعديته قطعًا

Augmentation in mazīd transforms potential event structure,
but does NOT establish event meaning or valency definitively
```

---

## 16. Mabni Noun Geometry | هندسة الاسم المبني

### 16.1 Definition

```
MabniNounSlotGeometry =
  Carrier
  + FixedBaseSlot
  + TerminalStability
  + NominalMabniClassSlot
  + ReferencePotentialSlot
  + MissingValueSlot (optional)
  + ExpectedCompletionSlot (optional)
  + AttachmentSlot (optional)
  + Residuals
  + Rank
  + STOP before meaning
```

---

### 16.2 Examples

```
هذا → DemonstrativeSlot + ReferencePotential
الذي → RelativeSlot + ExpectedṢilahSlot
من → Interrogative/Conditional/RelativeSlot + MissingValueSlot
أين → LocativeQuestionSlot + MissingPlaceValue
متى → TemporalQuestionSlot + MissingTimeValue
```

---

## 17. Mabni Particle Geometry | هندسة الحرف المبني

### 17.1 Definition

```
MabniParticleSlotGeometry =
  Carrier
  + FixedParticleSlot
  + OperatorClassSlot
  + OperatorPotentialSlot
  + ScopeExpectationSlot
  + TerminalStability
  + Residuals
  + Rank
  + STOP before applied operation
```

---

### 17.2 Example: لم

```
لم =
  FixedParticleSlot
  + NegationPotential
  + JussivePotential
  + TenseShiftPotential
  + ExpectedMudariSlot
  + STOP
```

**We do NOT say**: لم عملت (lam operated)

**Until after composition.**

---

## 18. Post-Mabni Ḥaraka Geometry | هندسة الحركة الزائدة بعد المبنيات

### 18.1 In Mabni and Particles

Ḥaraka may be:
- Construction ḥaraka (حركة بناء)
- Pronunciation ḥaraka (حركة نطق)
- Escape ḥaraka (حركة تخلص)
- Pause/connection ḥaraka (حركة وقف/وصل)
- Class ḥaraka (حركة صنفية)
- Fixed ḥaraka (حركة ثابتة)

**NOT**:
- Final i'rāb ḥaraka (حركة إعراب نهائي)

---

### 18.2 Definition

```
PostMabniHarakaGeometry =
  Carrier
  + FixedTerminalHaraka
  + OperationalHaraka
  + PhonologicalSupport
  + ClassMarkingPotential
  + Residuals
  + Rank
  + STOP
```

---

### 18.3 Law

```
حركة المبني تثبت الثبات أو التشغيل،
ولا تثبت عاملًا نحويًا

Mabni ḥaraka establishes stability or operation,
does NOT establish syntactic operator
```

---

## 19. Constitutional Summary | الخلاصة الدستورية

### 19.1 The Final Laws (15 Laws)

1. **No augmentation without preserved origin** (لا زيادة بلا أصل محفوظ)
2. **No augmentation without non-original slot** (لا زيادة بلا خانة غير أصلية)
3. **No augmentation without license** (لا زيادة بلا ترخيص)
4. **Extra letter changes geometry, not meaning** (الحرف الزائد يغيّر الهندسة لا المعنى)
5. **Extra ḥaraka changes operation, not material** (الحركة الزائدة تغيّر التشغيل لا المادة)
6. **Augmentation opens potential, not judgment** (الزيادة تفتح احتمالًا لا حكمًا)
7. **Every augmentation preserves Trace and records Residual** (كل زيادة تحفظ Trace وتسجل Residual)
8. **Augmentation rank does not exceed its evidence** (رتبة الزيادة لا تتجاوز دليلها)
9. **Mabni blocks standard derivational augmentation** (المبنيات تمنع الزيادة الاشتقاقية القياسية)
10. **Mujarrad verbs block internal extra letter** (الأفعال المجردة تمنع الحرف الزائد الداخلي)
11. **Mabni nouns not reduced to Root + Augmentation without evidence** (الأسماء المبنية لا تُرد إلى Root + Augmentation بلا دليل)
12. **Mabni particles are FixedOperatorSlots, not derivational augments** (الحروف المبنية FixedOperatorSlots لا مزيدات اشتقاقية)
13. **Where augmentation blocked, ClassSpecificSlots work instead of ExtraLetterSlots** (حيث تُمنع الزيادة، تعمل ClassSpecificSlots بدل ExtraLetterSlots)
14. **Mabni ḥaraka is stability/operation ḥaraka, not final i'rāb ḥaraka** (حركة المبني حركة ثبات/تشغيل لا حركة إعراب نهائي)
15. **All paths stop before meaning** (كل المسار يتوقف قبل المعنى)

---

### 19.2 The Comprehensive Statement

```
ExtraLetter works only where:
  Origin + NonOriginalSlot + License exist

Where this is blocked,
  use FixedSlotGeometry / ClassSpecificSlotGeometry,
  NOT DerivationalAugmentation
```

**Meaning**:
```
المزيد = أصل محفوظ + خانات زائدة مرخّصة
Mazīd = Preserved origin + licensed extra slots

المجرد = أصل محفوظ + خانات أصلية
Mujarrad = Preserved origin + original slots

المبني = صورة ثابتة + خانات صنفية
Mabni = Fixed form + class slots

الحرف = أداة ثابتة + خانات تشغيل
Particle = Fixed tool + operation slots

الضمير/الإشارة/الموصول = إحالة ثابتة الصورة مفتوحة المرجع
Pronoun/Demonstrative/Relative = Fixed-form reference with open referent
```

---

### 19.3 The Supreme Law Preserved

```
كل ما قبل المعنى هندسة خانات
All before meaning is slot geometry

لكن ليست كل خانة زائدة اشتقاقًا
But not every extra slot is derivation

وليست كل زيادة معنى
And not every augmentation is meaning

وليست كل مبنية قابلة للتحليل بمنطق الزوائد
And not every mabni is analyzable by augmentation logic

ثم:
Then:

STOP before meaning
```

---

## 20. Implementation Mapping | خريطة التنفيذ

### 20.1 Existing Structures

**Already Implemented** (map to slot geometry):
- MufradProof (contains morphological analysis)
- Root extraction (RootSlots)
- Pattern matching (PatternSlots)
- Mabni/Mu'rab distinction (TerminalStability)

---

### 20.2 Gaps to Fill

**Need Implementation**:
1. **DerivationalExtraLetter** slot type
2. **NonDerivationalSlotGeometry** framework
3. **ExtraLetterLicense** validation
4. **PreservedOrigin** tracking
5. **ExtraHaraka** vs ExtraLetter distinction
6. **MabniPath** gate (blocks derivational augmentation)
7. **ClassSpecificSlots** for mabni/particle/pronoun
8. **OperationalHarakaSlots** for mabni ḥarakāt

---

### 20.3 Constitutional Tests Required

Must prove:
1. Mazīd has PreservedOrigin + ExtraLetterSlots
2. Mujarrad has RootSlots + BarePatternSlots (no internal extra)
3. Mabni blocks DerivationalAugmentation
4. Particles use FixedOperatorSlots, not derivational analysis
5. All outputs stop before meaning

---

## 21. Next Steps | الخطوات التالية

### 21.1 Immediate

1. **Audit existing MufradProof** against slot geometry principles
2. **Map root/pattern analysis** to DerivationalSlotGeometry
3. **Identify mabni detection** in current code
4. **Design slot type hierarchy**:
   - DerivationalSlots
   - NonDerivationalSlots
   - FixedSlots
   - ClassSpecificSlots

---

### 21.2 Future

1. Implement **ExtraLetterCandidate** with License + Rank
2. Implement **MabniPathGate** blocking derivational analysis
3. Extend **ResidualAudit** to track augmentation residuals
4. Prove all 15 constitutional laws with tests

---

**Document Status**: CONSTITUTIONAL EXTENSION
**Implementation**: PENDING MAPPING
**Dependencies**: SLOT_GEOMETRY_ALGEBRA_CONSTITUTION.md
**Next Action**: Audit existing morphological analysis against augmentation principles

---

**END OF CONSTITUTION**
