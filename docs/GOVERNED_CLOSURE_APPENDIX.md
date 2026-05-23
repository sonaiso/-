# ملحق إغلاق النموذج الكاشف: من بصيرة الجامد والمشتق إلى جبر منع الانتحال المعرفي

## Governed Closure Appendix: From Jamid/Mushtaq Insight to Epistemological Usurpation Prevention Algebra

**Status**: Theoretical Framework
**Version**: 1.0
**Date**: 2026-05-23
**Branch**: `claude/add-overflowing-form-closure`

---

## تمهيد محكّم (Governed Preface)

### البصيرة الأولى (The Foundational Insight)

The foundational insight of the **Revealing Model** (النموذج الكاشف) is that disciplined, vocalized Arabic (العربية المشكولة المنضبطة) reveals two primary axes:

```text
الوجود        (Existence)
معرفة الوجود  (Knowledge of Existence)
```

This manifests initially in the distinction:

```text
الجامد (Jamid/Solid)  ← يحضر الوجود (presents existence)
المشتق (Mushtaq/Derived) ← يكشف معرفة الوجود (reveals knowledge of existence)
                           from the perspective of event, attribute, trace, or relation
```

- **الجامد (Jamid)** presents the thing as an entity, stable name, or preserved form
- **المشتق (Mushtaq)** reveals an aspect of knowledge about that thing: its action, attribute, trace, relation, potentiality, or transformation

### الفجوة (The Gap)

However powerful this insight, **it is not yet a complete general algebra**.

A complete general algebra does not merely observe the axis of existence and knowledge—it must **govern every transition point** between them:

```text
من الأثر إلى الواقع      (from trace to reality)
من الاسم إلى المسمى      (from name to referent)
من الدال إلى المدلول     (from signifier to signified)
من الصيغة إلى المعنى     (from form to meaning)
من التركيب إلى الإفادة   (from structure to statement)
من الإفادة إلى الحكم     (from statement to judgment)
من الحكم العام إلى التنزيل (from general judgment to instantiation)
```

If these transition points are not closed by **gates**, **epistemological usurpation** (الانتحال المعرفي) occurs:

- **اسم ينتحل الواقع** - A name usurps reality
- **أثر ينتحل اليقين** - A trace usurps certainty
- **صيغة تنتحل المعنى** - A form usurps meaning
- **تركيب ينتحل الحكم** - A structure usurps judgment

---

## 1. مبدأ الإغلاق الأعلى (Supreme Closure Principle)

### القانون الأعلى (Supreme Law)

Nothing transitions from one layer to another unless it establishes:

```text
نوعه     (type)
مجاله    (domain)
دليله    (evidence)
رتبته    (rank)
بقاياه   (residuals)
أثره المحفوظ (preserved trace)
```

### الصياغة المانعة (Preventive Formulation)

```text
لا اسم بلا مسمى مرشح        (No name without candidate referent)
لا مسمى بلا مجال            (No referent without domain)
لا أثر بلا مصدر             (No trace without source)
لا واقع بلا نوع وجود        (No reality without existence type)
لا دال بلا ترخيص            (No signifier without license)
لا معنى بلا وضع             (No meaning without conventional assignment)
لا إفادة بلا نسبة           (No statement without predication)
لا حكم بلا دليل             (No judgment without evidence)
لا تنزيل بلا مناط           (No instantiation without criterion)
لا يقين مع بقايا مانعة      (No certainty with blocking residuals)
```

This is the **center of the entire appendix**.

---

## 2. البنية المعمارية: ست حزم إغلاق (Architectural Structure: Six Closure Bundles)

Rather than maintaining 20 layers as a long list, we organize them into **six primary bundles**:

### البنية الكاملة (Complete Structure)

```text
A. إغلاق الواقع والأثر      (Reality & Trace Closure)
B. إغلاق الدال واللفظ       (Signifier & Utterance Closure)
C. إغلاق الصيغة والبنية     (Form & Structure Closure)
D. إغلاق الدلالة والاستعمال (Signification & Usage Closure)
E. إغلاق الإفادة والحكم     (Statement & Judgment Closure)
F. إغلاق الحوكمة والتجريب   (Governance & Testing Closure)
```

---

## A. إغلاق الواقع والأثر (Reality & Trace Closure)

### A.1 طبقة الوجود (Existence Layer)

#### المشكلة (The Problem)

The word "existence" (الوجود) cannot remain absolute; if left so, it becomes a source of leaping.

#### التصنيف التشغيلي (Operational Classification)

```python
ExistenceType:
    EXTERNAL      # خارجي - has realization outside mind & utterance
    EFFECTUAL     # أثري - present through trace
    MENTAL        # ذهني - present in conception
    VERBAL        # لفظي - present in utterance
    TECHNICAL     # اصطلاحي - present within specific domain
    METAPHORICAL  # مجازي - transferred signification
    NORMATIVE     # حكمي - judgment-based
```

#### القانون (Law)

```text
لا يعامل الاسم بوصفه واقعًا حتى يحدد نوع وجوده
A name shall not be treated as reality until its existence type is determined.
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class RealityCandidate:
    existence_type: ExistenceType
    domain: str
    evidence: List[Evidence]
    trace: Trace
    rank: PredicateRank
    residuals: List[Residual]
```

---

### A.2 طبقة منع الاسم من انتحال الواقع (Name-Reality Usurpation Prevention Layer)

#### المشكلة (The Problem)

**This is a central layer.** Much corrupt thinking begins here: we possess a name and think we possess a reality.

#### أمثلة (Examples)

```text
العقل     (the mind)
المجتمع   (society)
الدولة    (the state)
الحرية    (freedom)
اللغة     (language)
الأمة     (the nation)
الوعي     (consciousness)
```

These words must not be treated as ready-made realities before determining their referents, domains, and traces.

#### القفزة الممنوعة (Forbidden Leap)

```text
Name → Reality
```

#### المسار الصحيح (Correct Path)

```text
Name
→ ReferentCandidate
→ Domain
→ Evidence
→ Rank
→ Residuals
```

#### البوابة (Gate)

```python
class NameRealityGate:
    """
    Prevents names from usurping reality status.

    Critical Questions:
    - Do we have reality or just a name?
    - Has the referent been established?
    - Has the domain been established?
    - Has its trace been established?
    - Is the name technical/metaphorical/transferred?
    - Is the name shared/ambiguous?
    """

    def admit_reality_claim(
        self,
        name: str,
        referent_candidate: Any,
        evidence: List[Evidence]
    ) -> NameRealityGateResult:
        pass
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class NamedRealityCandidate:
    name: str
    referent_candidate: Any
    domain: str
    referent_evidence: List[Evidence]
    ambiguity_score: float
    rank: PredicateRank
    residuals: List[Residual]
```

---

### A.3 هندسة الأثر (Trace Geometry)

#### المبدأ (Principle)

The mind does not always deal with reality directly, but with its **trace** (أثر).

This is the key that makes this project more general than language alone.

#### أنواع الأثر (Trace Types)

```python
TraceEffectType:
    SENSORY      # حسي - perceived through senses
    TEXTUAL      # نصي - preserved in text
    TESTIMONIAL  # خبري - conveyed through report
    HISTORICAL   # تاريخي - established through history
    STATISTICAL  # إحصائي - established through statistics
    BEHAVIORAL   # سلوكي - manifest in behavior
    LINGUISTIC   # لغوي - manifest in language
    MATERIAL     # مادي/أثري - material remains
```

#### القانون (Law)

```text
الأثر لا يساوي الواقع
A trace does not equal reality.

الأثر يرشح واقعًا برتبة وبقايا
A trace nominates reality with rank and residuals.
```

#### القفزة الممنوعة (Forbidden Leap)

```text
TraceEffect → Certainty
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class TraceEffectCandidate:
    effect_type: TraceEffectType
    source: str
    transmission_chain: List[TransmissionLink]
    preservation_level: float  # [0.0, 1.0]
    distortion_risk: float     # [0.0, 1.0]
    reality_candidate: RealityCandidate
    rank: PredicateRank
    residuals: List[Residual]
```

---

## B. إغلاق الدال واللفظ (Signifier & Utterance Closure)

### B.1 هندسة الدال وحده (Pure Signifier Geometry)

#### البوابة الأولى في العربية (First Gate in Arabic)

This gate's function is to **prevent leaping from script or sound to meaning**.

#### المسار (Path)

```text
RawArabicTrace
→ LicensedSignifierObject
```

#### محتوى الدال المرخّص (Licensed Signifier Contents)

A licensed signifier MUST carry:

```text
✓ حروف    (letters)
✓ حركات   (diacritics)
✓ مقاطع   (syllables)
✓ حدود    (boundaries)
✓ لواصق   (affixes)
✓ صيغة مرشحة (candidate form)
✓ مسار    (path)
✓ حالة نهائية (terminal state)
✓ رتبة    (rank)
✓ بقايا   (residuals)
✓ أثر محفوظ (preserved trace)
```

And MUST NOT carry:

```text
✗ meaning
✗ wadh
✗ dalalah
✗ hukm
✗ mutabaqah
✗ tadammun
✗ iltizam
```

#### القانون (Law)

```text
لا معنى قبل دال مرخّص
No meaning before licensed signifier.
```

**Reference**: This aligns with PR-L3 (Pure Dal Geometry).

---

### B.2 فصل طبقات المدلول (Signified Layer Separation)

#### المشكلة (The Problem)

The word "signified" (مدلول) is not a single layer.

#### الطبقات (Layers)

```python
SignifiedType:
    VERBAL_SIGNIFIED    # مدلول لفظي - what the form opens
    LEXICAL_MEANING     # مدلول معجمي - what lexicon/attestation establishes
    CONTEXTUAL_MEANING  # مدلول سياقي - what context selects
    INTENDED_MEANING    # مراد - what speaker/text intends
    JUDGMENT            # حكم - what is affirmed/negated/applied
```

#### القفزات الممنوعة (Forbidden Leaps)

```text
مدلول لفظي → مراد          (Verbal signified → Intended)
مدلول معجمي → حكم         (Lexical meaning → Judgment)
مدلول سياقي → صدق         (Contextual meaning → Truth)
```

#### المسار الصحيح (Correct Path)

```text
VerbalSignified
→ LexicalMeaningCandidate
→ ContextualMeaningCandidate
→ IntendedMeaningCandidate
→ HukmCandidate
```

**Each transition requires a gate.**

---

## C. إغلاق الصيغة والبنية (Form & Structure Closure)

### C.1 الجامد والمشتق كمتصل جبري (Jamid/Mushtaq as Algebraic Continuum)

#### البصيرة المعمارية (Architectural Insight)

This is one of the **strongest parts of the appendix**. It must be established as an architectural principle:

```python
root_status ≠ derivational_status
```

**The existence of a possible root does not mean productive derivation.**

#### أمثلة (Examples)

```text
الأرض  (earth)
السماء (sky)
الماء  (water)
النار  (fire)
الناس  (people)
```

These may carry origins, roots, or linguistic history, but they are not treated automatically as productive derivations.

#### المتصل المقترح (Proposed Continuum)

```python
DerivationalStatus:
    JAMID_ORIGINAL        # جامد أصلي - original solid
    JAMID_RADICAL         # جامد جذري - solid with root
    JAMID_PRESERVED       # جامد محفوظ سماعًا - preserved by attestation
    DERIVED_PRODUCTIVE    # مشتق منتج - productively derived
    DERIVED_FROZEN        # مشتق متجمد - frozen derivation
    TRANSFERRED_TECHNICAL # منقول اصطلاحي - technical transfer
    PROPER_NAME           # علم - proper name
    BORROWED              # دخيل - borrowed
    MABNI                 # مبني - indeclinable
    PATH_AMBIGUOUS        # ملتبس المسار - ambiguous path
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class DerivationalContinuumCandidate:
    root_status: RootStatus  # rooted | rootless | candidate_root | defective_root | disputed
    derivational_status: DerivationalStatus
    frozen_level: float     # [0.0, 1.0]
    productivity: float     # [0.0, 1.0]
    lexical_attestation: List[AttestationEvidence]
    rank: PredicateRank
    residuals: List[Residual]
```

---

### C.2 هندسة المبنيات (Indeclinable/Mabni Structure)

#### المبدأ (Principle)

**Indeclinables (المبنيات) must not forcibly enter root-pattern geometry.**

#### أمثلة (Examples)

```text
هذا     (this)
الذي    (which/who)
من      (who/from)
في      (in)
هو      (he)
أنت     (you)
لم      (did not)
لن      (will not)
إن      (indeed/if)
هل      (interrogative particle)
```

These are not ordinary derivational material—they are **operators, linkers, reference tools, or constraints**.

#### القفزة الممنوعة (Forbidden Leap)

```text
Mabni → ForcedRootPattern
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class MabniCandidate:
    mabni_type: MabniType  # pronoun | demonstrative | relative | particle | ...
    operator_function: List[OperatorFunction]
    reference_potential: Optional[ReferenceCandidate]
    required_complement: List[ComplementRequirement]
    rank: PredicateRank
    residuals: List[Residual]
```

---

### C.3 هندسة المعرب والعامل (I'rab & 'Amil Geometry)

#### المبدأ (Principle)

**I'rab (الإعراب) is not a terminal vowel.**
It is **positional susceptibility to receive operator effect**.

```text
زيدٌ   (nominative)
زيدًا  (accusative)
زيدٍ   (genitive)
```

The ḍamma, fatḥa, and kasra are not mere sounds—they are **traces of relations**.

#### القوانين (Laws)

```text
لا إعراب بلا عامل
No i'rab without operator.

ولا علامة بلا علاقة
No marking without relation.

ولا علاقة بلا بوابة
No relation without gate.
```

#### مخرج المعرب (I'rab Output)

```python
@dataclass(frozen=True)
class MurabCandidate:
    terminal_form: str
    case_potential: CasePotential  # nominative | accusative | genitive | jussive | unknown
    visible_or_estimated: CaseVisibility  # visible | estimated | blocked
    amil_required: bool
    inflection_constraints: List[InflectionConstraint]
    rank: PredicateRank
    residuals: List[Residual]
```

#### مخرج العامل ('Amil Output)

```python
@dataclass(frozen=True)
class AmilCandidate:
    amil_type: AmilType  # verbal | nominal | particle | semantic | explicit | implicit | deleted | nasikh | jazim | nasib | jarr
    target: str
    effect: str
    conditions: List[ActivationCondition]
    blocking_factors: List[BlockingFactor]
    rank: PredicateRank
    residuals: List[Residual]
```

**Reference**: Aligns with NahwOperatorRegistry (PR #16) and OperatorTriggerPotential (PR #14).

---

### C.4 هندسة الزمن والنسخ (Tense & Nasikh Geometry)

#### المبدأ (Principle)

**Word-level tense ≠ compositional tense.**

#### أمثلة (Examples)

```text
كتب         (wrote - simple past)
قد كتب      (has written - perfective)
كان يكتب    (was writing - past continuous)
لم يكتب     (did not write - negated)
لن يكتب     (will not write - future negative)
سيكتب       (will write - future)
سوف يكتب    (will write - emphatic future)
ما زال يكتب (still writing - continuous)
```

#### القانون (Law)

```text
زمن المفرد لا يساوي زمن التركيب
Word-level tense does not equal compositional tense.
```

#### النسخ (Nasikh/Copular Verbs)

```text
كان في المفرد ≠ ناسخ عامل دائمًا
kāna as isolated word ≠ always active nasikh.
```

Rather:

```text
كان → NasikhCandidate
      → activation only in composition when conditions met
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class TenseNasikhCandidate:
    word_level_tense: WordTense  # past | present | imperative | nominal | unknown
    compositional_tense: CompositionalTense  # past | present | future | habitual | continuous | negated | conditional | unknown
    nasikh_candidate: bool
    activation_conditions: List[ActivationCondition]
    fulfilled_slots: List[SyntacticSlot]
    rank: PredicateRank
    residuals: List[Residual]
```

---

### C.5 هندسة الإحالة (Reference Geometry)

#### المبدأ (Principle)

**Reference is not pronoun resolution alone.**
It is **opening a search domain for referent**.

#### أمثلة (Examples)

```text
هو              (he/it)
هذا             (this)
الذي            (which/who)
إياك            (you-accusative)
كاف الخطاب      (address-kaf)
الضمير المستتر  (hidden pronoun)
```

#### القانون (Law)

```text
العلامة الإحالية لا تثبت المرجع
إنما تفتح مجال بحث مرجعي

The referential marker does not establish the referent.
Rather, it opens a referential search domain.
```

#### القفزة الممنوعة (Forbidden Leap)

```text
Pronoun → FinalReferent
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class ReferenceCandidate:
    reference_type: ReferenceType  # pronominal | demonstrative | relative | deictic | anaphoric | cataphoric | discourse | event | judgment | elliptic
    search_domain: SearchDomain    # text | context | discourse | situation | prior_sentence | following_sentence
    agreement_constraints: List[AgreementConstraint]
    syntactic_fit: List[SyntacticFitConstraint]
    candidate_referents: List[ReferentCandidate]
    rank: PredicateRank
    residuals: List[Residual]
```

---

## D. إغلاق الدلالة والاستعمال (Signification & Usage Closure)

### D.1 هندسة الوضع (Wadh/Conventional Assignment Geometry)

**Wadh** (الوضع) is what licenses the transition from utterance to meaning.
Not form alone, not root alone, not assumed usage.

#### مصادر الوضع (Wadh Sources)

```python
WadhSource:
    SAMA        # السماع - direct attestation
    URF         # العرف - customary usage
    NAQL        # النقل - transmission
    SHAR        # الشرع - legal/religious stipulation
    ISTILAH     # الاصطلاح - technical terminology
    QARINA      # القرينة - contextual indicator
    LEXICON     # المعجم - lexicon witness
    WITNESS     # الشاهد - textual witness
```

#### القانون (Law)

```text
لا دلالة بلا وضع
No signification without wadh.

ولا وضع بلا مصدر
No wadh without source.

ولا مصدر بلا مجال ورتبة
No source without domain and rank.
```

**Reference**: PR-L5A (WadhGeometry), PR-L5B (WadhGate).

---

### D.2 هندسة الاستعمال (Usage Geometry)

#### المبدأ (Principle)

**Wadh establishes the origin, but usage determines movement within context.**

#### أنواع الاستعمال (Usage Types)

```python
UsageType:
    LITERAL        # حقيقة - literal
    METAPHORICAL   # مجاز - metaphorical
    TRANSFERRED    # نقل - transferred
    CUSTOMARY      # عرف - customary
    LEGAL          # شرع - legal
    TECHNICAL      # اصطلاح - technical
    SPECIFIED      # تخصيص - specified
    GENERALIZED    # تعميم - generalized
    ABSOLUTE       # إطلاق - absolute
    RESTRICTED     # تقييد - restricted
```

#### القانون (Law)

```text
الوضع الأصلي لا يكفي لإثبات الاستعمال السياقي
Original wadh is insufficient to establish contextual usage.
```

#### مثال (Example)

```text
رأيت أسدًا يخطب
I saw a lion giving a speech.

أسد موضوع للحيوان (lion is placed-for the animal)
لكن الاستعمال هنا مجازي (but the usage here is metaphorical)
يحتاج قرينة (requires contextual indicator)
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class UsageCandidate:
    usage_type: UsageType
    context_evidence: List[ContextEvidence]
    transfer_path: List[TransferStep]
    literal_or_figural_status: str
    rank: PredicateRank
    residuals: List[Residual]
```

---

### D.3 القوة الخطابية (Speech Force)

#### المبدأ (Principle)

This layer **must not be confused with judgment** (الحكم).

#### أنواع القوة الخطابية (Speech Force Types)

```python
SpeechForceType:
    DECLARATIVE    # خبر - declarative
    IMPERATIVE     # أمر - imperative
    PROHIBITIVE    # نهي - prohibitive
    INTERROGATIVE  # استفهام - interrogative
    VOCATIVE       # نداء - vocative
    OPTATIVE       # تمنٍّ - optative (wish)
    EXCLAMATIVE    # تعجب - exclamative
    CONDITIONAL    # شرط - conditional
    OATH           # قسم - oath
    OFFER          # عرض - offer
    INCITEMENT     # تحضيض - incitement
```

#### القوانين (Laws)

```text
الخبر لا يساوي الصدق
Declarative ≠ Truth.

الأمر لا يساوي الوجوب
Imperative ≠ Obligation.

النهي لا يساوي التحريم
Prohibitive ≠ Prohibition (legal).

الاستفهام لا يساوي الجهل
Interrogative ≠ Ignorance.
```

**Reference**: Aligns with Maqam Theory gates (InterrogativeGate, VocativeGate, ImperativeGate, etc.).

---

## E. إغلاق الإفادة والحكم (Statement & Judgment Closure)

### E.1 صحة التركيب وصحة الحكم (Structural Validity vs. Judgment Validity)

#### المشكلة (The Problem)

**This is one of the most dangerous gaps.**

```text
الجبل طار
The mountain flew.
```

This may be a structurally valid sentence, linguistically informative, but it does not establish reality.

#### القانون (Law)

```text
صحة التركيب لا تساوي صحة الحكم
Structural validity ≠ Judgment validity.
```

#### المسار الصحيح (Correct Path)

```text
صحة تركيب (Structural validity)
→ إفادة لغوية (Linguistic statement)
→ دعوى (Claim)
→ مجال (Domain)
→ دليل (Evidence)
→ حكم (Judgment)
```

---

### E.2 الحكم والتنزيل وتحقيق المناط (Judgment, Instantiation, Criterion Realization)

#### المبدأ (Principle)

**Judgment does not come from mere statement.**

It requires:

```text
موضوعًا  (subject matter)
مجالًا   (domain)
مناطًا   (criterion)
دليلًا   (evidence)
شروطًا   (conditions)
موانع    (blockers)
رتبة     (rank)
بقايا    (residuals)
```

#### القانون (Law)

```text
لا تنزيل بلا تحقيق مناط
No instantiation without criterion realization.
```

#### مثال (Example)

```text
الماء طاهر
Water is pure.
```

The sentence structure is insufficient. We must examine:

```text
أي ماء؟              (Which water?)
هل تغير؟            (Has it changed?)
هل خالطه شيء؟        (Has something mixed with it?)
ما المجال؟ فقهي؟ علمي؟ لغوي؟ (What domain? Juristic? Scientific? Linguistic?)
```

#### القفزة الممنوعة (Forbidden Leap)

```text
إفادة عامة → حكم منزّل
General statement → Instantiated judgment
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class HukmCandidate:
    claim: str
    domain: str
    manat: Any  # criterion
    conditions: List[Condition]
    blockers: List[Blocker]
    evidence: List[Evidence]
    rank: PredicateRank
    residuals: List[Residual]
```

---

### E.3 نظام المجال (Domain System)

#### المبدأ (Principle)

**Rules do not transfer from one domain to another without license.**

#### المجالات (Domains)

```text
نحو        (grammar)
صرف        (morphology)
بلاغة      (rhetoric)
فقه        (jurisprudence)
منطق       (logic)
رياضيات    (mathematics)
فيزياء     (physics)
تاريخ      (history)
اجتماع     (sociology)
برمجة      (programming)
```

#### القفزة الممنوعة (Forbidden Leap)

```text
DomainRule_A → Domain_B (without license)
```

#### أمثلة (Examples)

```text
قاعدة نحوية لا تثبت حكمًا واقعيًا
A grammatical rule does not establish a real-world judgment.

قاعدة إحصائية لا تثبت يقينًا
A statistical rule does not establish certainty.

قاعدة معجمية لا تثبت مراد المتكلم
A lexical rule does not establish speaker's intent.
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class DomainCandidate:
    domain: str
    primitives: List[Primitive]
    rules: List[Rule]
    allowed_transfers: List[DomainTransfer]
    forbidden_transfers: List[DomainTransfer]
    rank: PredicateRank
    residuals: List[Residual]
```

---

## F. إغلاق الحوكمة والتجريب (Governance & Testing Closure)

### F.1 نظام المعلومات السابقة (Prior Information System)

#### المبدأ الحاكم (Governing Principle)

```python
PriorInformation ≠ PriorOpinion
```

#### PriorInformation

```text
قواعد       (rules)
تعريفات     (definitions)
شواهد       (witnesses/examples)
تصنيفات     (classifications)
مصادر       (sources)
استثناءات   (exceptions)
رتب         (ranks)
بقايا       (residuals)
```

#### PriorOpinion

```text
انطباع              (impression)
تحيز                (bias)
ذوق                 (taste)
عادة                (habit)
تفسير غير موثق      (undocumented interpretation)
حكم سابق            (prior judgment)
```

#### القانون (Law)

```text
لا رأي سابق يدخل بوصفه معلومة سابقة
No prior opinion enters as prior information.
```

**Reference**: Aligns with PR-N1 (NeutralBinding) which preserves PriorInformation while excluding PriorOpinion.

---

### F.2 الانتباه والذاكرة والخطأ والتصحيح (Attention, Memory, Error & Correction)

#### المبدأ (Principle)

This addition is important because it opens the project from **"linguistic system"** to **"cognitive simulation"**.

But it must be governed:

```text
الذاكرة ليست دليلًا
Memory is not evidence.

الانتباه ليس حكمًا
Attention is not judgment.

الاستحضار ليس تحققًا
Recall is not realization.

الفشل ليس نهاية، بل أثر تعلم
Failure is not an end, but a learning trace.
```

#### القفزة الممنوعة (Forbidden Leap)

```text
MemoryTrace → Evidence
```

#### المخرج (Output)

```python
@dataclass(frozen=True)
class CognitiveStateCandidate:
    attention_focus: Any
    memory_trace: List[MemoryTrace]
    prior_activation: List[Activation]
    error_risk: float  # [0.0, 1.0]
    correction_path: List[CorrectionStep]
    rank: PredicateRank
    residuals: List[Residual]
```

**Reference**: Aligns with PR-G1 (Memory Geometry Kernel).

---

### F.3 Golden Dataset

#### المبدأ (Principle)

**The model does not become science without golden examples.**

#### التغطية المطلوبة (Required Coverage)

```text
أمثلة صحيحة           (correct examples)
أمثلة خاطئة           (incorrect examples)
أمثلة ملتبسة          (ambiguous examples)
أمثلة ناقصة           (incomplete examples)
أمثلة تمنع الحكم      (judgment-blocking examples)
أمثلة تخفض الرتبة     (rank-lowering examples)
أمثلة تكشف القفز      (leap-revealing examples)
```

#### أمثلة ممتازة من النص (Excellent Examples from Text)

```text
كتب
→ ناقص تشكيل، رتبة منخفضة
Incomplete diacritization, low rank

كَتَبَ
→ دال مرخّص، لا معنى نهائي
Licensed signifier, no final meaning

هذا
→ إحالة مفتوحة، مرجع غير مثبت
Open reference, referent not established

الذي
→ صلة مطلوبة
Relative clause required

كتاب زيد
→ إضافة، لا إفادة تامة وحدها
Construct state, not complete statement alone

زيد قائم
→ إفادة مرشحة
Candidate statement

اكتب
→ أمر، لا وجوب بلا بوابة حكم
Imperative, no obligation without judgment gate

أسد في الحرب
→ مجاز محتمل يحتاج قرينة
Possible metaphor requiring indicator
```

---

### F.4 Dashboard النضج المحكوم (Governed Maturity Dashboard)

#### المبدأ (Principle)

This layer is **indispensable** to prevent the project from becoming beautiful documents without realization.

#### القانون (Law)

```text
لا يُحسب الإنجاز بعدد الملفات،
بل باكتمال:
النوع،        (type)
التنفيذ،      (implementation)
الدليل،       (evidence)
الرتبة،       (rank)
البقايا،      (residuals)
الاختبار،     (testing)
الأثر.        (trace)

Achievement is not counted by number of files,
but by completeness of type, implementation, evidence, rank, residuals, testing, and trace.
```

#### المؤشرات (Metrics)

```text
Typed Contract Coverage       (نسبة تغطية العقود المكتوبة)
NoLeap Coverage               (نسبة تغطية منع القفز)
Rank Inflation Risk           (خطر تضخيم الرتبة)
Residual Debt                 (دَين البقايا)
Trace Coverage                (تغطية الأثر)
Golden Dataset Coverage       (تغطية الأمثلة الذهبية)
Claim Inflation Risk          (خطر تضخيم الادعاءات)
Layer Completion              (اكتمال الطبقات)
```

---

## مصفوفة الإغلاق النهائية (Final Closure Matrix)

| الحزمة (Bundle) | الخطر (Danger) | القفزة الممنوعة (Forbidden Leap) | البوابة المطلوبة (Required Gate) |
|---|---|---|---|
| الواقع (Reality) | الاسم ينتحل الواقع | اسم → واقع | NameRealityGate |
| الأثر (Trace) | الأثر ينتحل اليقين | أثر → يقين | AtharGeometry |
| الدال (Signifier) | الرسم ينتحل المعنى | لفظ → معنى | PureDalGate |
| الجامد/المشتق (Jamid/Mushtaq) | الجذر ينتحل الاشتقاق | جذر → مشتق | DerivationalContinuumGate |
| المبني (Mabni) | الأداة تُجبر على وزن | مبني → جذر | MabniGate |
| المعرب (Mu'rab) | الحركة تنتحل العلاقة | علامة → إعراب | MurabAmilGate |
| الزمن (Tense) | الصيغة تنتحل زمن التركيب | فعل → زمن نهائي | TenseCompositionGate |
| الإحالة (Reference) | الضمير ينتحل المرجع | ضمير → مرجع | ReferenceGate |
| الوضع (Wadh) | الصيغة تنتحل المعنى | صيغة → معنى | WadhGate ✓ |
| الاستعمال (Usage) | الوضع ينتحل السياق | وضع → استعمال | UsageGate |
| القوة (Speech Force) | الأمر ينتحل الوجوب | أمر → وجوب | SpeechForceGate ✓ |
| الإفادة (Statement) | التركيب ينتحل الصدق | إفادة → حكم | HukmEvidenceGate |
| المجال (Domain) | القاعدة تنتقل بلا ترخيص | مجال → مجال | DomainTransferGate |
| المعلومات السابقة (Prior Info) | الرأي ينتحل المعلومة | رأي → معلومة | PriorFilterGate ✓ |
| الذاكرة (Memory) | الاستحضار ينتحل الدليل | ذاكرة → دليل | CognitiveAuditGate ✓ |
| التجريب (Testing) | الوثيقة تنتحل الإنجاز | claim → completion | MaturityDashboard |

**Legend**:
- ✓ = Already implemented (fully or partially)
- (blank) = Needs implementation

---

## الخلاصة المحكّمة (Governed Conclusion)

### البصيرة والجبر (Insight and Algebra)

The **Revealing Model** (النموذج الكاشف) does not complete by merely discovering that:

```text
الجامد يحضر الوجود
Jamid presents existence

المشتق يكشف معرفة الوجود
Mushtaq reveals knowledge of existence
```

This is a **foundational insight**, but it is not yet a **general algebra**.

### الجبر العام (General Algebra)

The general algebra begins when we **close the positions of usurpation**:

```text
انتحال الاسم للواقع          (name usurping reality)
انتحال الأثر لليقين          (trace usurping certainty)
انتحال الصيغة للمعنى          (form usurping meaning)
انتحال التركيب للحكم          (structure usurping judgment)
انتحال الأمر للوجوب          (imperative usurping obligation)
انتحال الرأي للمعلومة        (opinion usurping information)
انتحال الذاكرة للدليل        (memory usurping evidence)
انتحال النجاح البرمجي للصدق المعرفي (programming success usurping epistemological truth)
```

### النظام الطبقي المحكوم (Governed Layered System)

Therefore, Arabic must transform from a **revealing insight** to a **governed layered system**:

Each layer must have:

```text
مدخل          (input)
مخرج          (output)
نوع           (type)
بوابة         (gate)
دليل          (evidence)
رتبة          (rank)
بقايا         (residuals)
أثر محفوظ     (preserved trace)
اختبار منع قفز (leap-prevention test)
```

### أقصر صياغة حاكمة (Shortest Governing Formulation)

```text
النموذج الكاشف يبدأ بالجامد والمشتق،
لكنه لا يكتمل إلا بإغلاق:

الواقع، الأثر، الاسم، الدال، المبني، المعرب، العامل، الزمن، الإحالة،
الوضع، الاستعمال، الإفادة، الحكم، المجال، المعلومات السابقة، الذاكرة، الفشل، والتصحيح.

وبذلك لا تكون العربية مجرد لغة محللة،
بل مختبرًا لجبر المعرفة:

كيف ينتقل الإنسان من أثر الوجود إلى تصور،
ومن التصور إلى نسبة،
ومن النسبة إلى إفادة،
ومن الإفادة إلى حكم،
بلا قفز ولا هلوسة.
```

**English Translation**:

```text
The Revealing Model begins with Jamid and Mushtaq,
but it completes only by closing:

Reality, Trace, Name, Signifier, Mabni, Mu'rab, 'Amil, Tense, Reference,
Wadh, Usage, Statement, Judgment, Domain, Prior Information, Memory, Failure, and Correction.

Thus Arabic becomes not merely an analyzed language,
but a laboratory for the algebra of knowledge:

How does a human transition from trace of existence to conception,
from conception to predication,
from predication to statement,
from statement to judgment,
without leaping and without hallucination.
```

---

## Next Steps

See **CLOSURE_GATE_MATRIX.md** for the executable implementation matrix.

---

**Document Status**: Theoretical Framework Complete
**Next Phase**: Implementation Matrix (CLOSURE_GATE_MATRIX.md)
**Architecture Alignment**: Verified with existing gates (WadhGate, MutabaqahGate, NeutralBinding, Memory Geometry)
