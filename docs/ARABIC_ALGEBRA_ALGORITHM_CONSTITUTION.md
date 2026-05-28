# دستور خوارزميات الجبر العربي
# Arabic Algebra Algorithm Constitution

**Version**: 1.0.0
**Status**: Constitutional Framework
**Created**: 2026-05-28
**Authority**: Algebraic Foundation for Arabic Linguistic Analysis

---

## المبدأ الأعلى (Supreme Principle)

> **الجبر هو الدستور، والخوارزميات هي آليات التنفيذ.**
>
> Algebra is the constitution; algorithms are the execution mechanisms.

كما أن عروض الخليل حوّل الشعر إلى تقطيع مرخّص،
فجبر العربية يجب أن يحوّل اللفظ والتركيب إلى تحليل مرخّص،
لا يقفز من صوت إلى معنى،
ولا من وزن إلى وظيفة،
ولا من عامل إلى حكم،
ولا من إفادة إلى واقع.

Just as Al-Khalil's prosody transformed poetry into licensed analysis,
Arabic algebra must transform utterance and composition into licensed analysis,
that does NOT jump from sound to meaning,
nor from pattern to function,
nor from operator to judgment,
nor from ifadah to reality.

---

## القانون الأعلى للخوارزميات
## Supreme Law of Algorithms

**كل خوارزمية عربية يجب أن تنتج مرشحًا محدود المجال، لا نتيجة من طبقة أعلى.**

Every Arabic algorithm MUST produce a domain-bounded candidate, NOT a result from a higher layer.

### التطبيق (Application):

| Algorithm | Output | FORBIDDEN |
|-----------|--------|-----------|
| analyze_surface_dal | LafzCandidate | meaning, syntactic_role |
| analyze_wordform | WordformCandidate | final_meaning, hukm |
| analyze_weight | WeightCandidate | grammatical_role |
| detect_operator | RelationLicense | final_meaning, ifadah |
| compose_relations | RelationCandidate | meaning, hukm |
| close_dal_ifadah | Ifadah_Dal | hukm, reality |
| match_madlul | DalMadlulContract | hukm |
| infer_hukm | HukmCandidate | reality, tanzil |
| apply_tanzil | TanzilResult | (end of chain) |

### الحظر الصارم (Strict Prohibitions):

```
❌ WeightCandidate → meaning
❌ LafzCandidate → hukm
❌ RelationCandidate → reality
❌ Ifadah_Dal → tanzil
❌ Any layer → jump over intermediate layers
```

---

## القالب العام للخوارزمية
## General Algorithm Template

```python
ArabicAlgebraAlgorithm = {
    Input,           # المدخل المرخّص
    Carrier,         # الحاملات
    Prior,           # المعلومات السابقة المصنّفة
    Gate,            # بوابة الترخيص
    Operation,       # العمليات
    Identity,        # حفظ الهوية
    Candidate,       # المرشحات
    Trace,           # الأثر التتبعي
    Residuals,       # البقايا
    Rank,            # الرتبة
    Output,          # المخرج المحدود
    Forbidden        # الممنوعات
}
```

### شرح المكونات (Component Explanation):

#### 1. Input (المدخل)
- MUST be licensed from previous layer
- MUST NOT skip intermediate layers
- MUST preserve trace from source

#### 2. Carrier (الحامل)
- Basic structural units for this layer
- Examples: letter, syllable, root, pattern, operator, relation_edge

#### 3. Prior (المعلومات السابقة)
- Pre-classified knowledge required for analysis
- Examples: lexicon, pattern_registry, operator_registry, syntax_rules
- NOT inference - these are KNOWN resources

#### 4. Gate (البوابة)
- Licensing mechanism
- Determines what is admissible
- Examples: arabic_analyzability_gate, composition_license_gate

#### 5. Operation (العملية)
- Transformations and analyses
- MUST preserve identity
- MUST produce trace

#### 6. Identity (الهوية)
- What identity MUST be preserved
- Examples: preserve_lafz_trace, preserve_wordform_identity

#### 7. Candidate (المرشح)
- Output candidate type
- MUST be bounded to this layer's domain

#### 8. Trace (الأثر)
- Reversible audit trail
- Enables downward reconstruction

#### 9. Residuals (البقايا)
- What prevents certificate-level confidence
- Examples: ambiguity, missing_haraka, competing_analyses

#### 10. Rank (الرتبة)
- Confidence level: candidate < hypothesis < strong_hypothesis < certificate
- NEVER certificate without elimination of residuals

#### 11. Output (المخرج)
- Concrete output type
- MUST be domain-bounded

#### 12. Forbidden (الممنوع)
- Explicit prohibitions
- Prevents layer jumping

---

## خوارزمية اللفظ المفرد
## Single Lafz Algorithm

```python
Algorithm: analyze_surface_dal

Input:
    raw_lafz

Carrier:
    letter
    haraka
    sukun
    madd
    syllable
    root_candidate
    pattern_candidate
    prefix
    suffix
    clitic
    orthographic_trace

Prior:
    alphabet_system
    phonotactic_rules
    syllable_license
    root_registry
    pattern_registry
    morphology_doors
    lexical_memory
    usage_memory
    foreignness_policy
    residual_policy

Gate:
    arabic_analyzability_gate

Operation:
    normalize_surface
    segment_letters
    attach_harakat
    build_syllables
    detect_prefix_suffix
    propose_root
    propose_pattern
    check_wordform_license
    preserve_trace
    produce_candidates

Identity:
    preserve_lafz_trace

Candidates:
    LafzCandidate
    WordformCandidate

Residuals:
    missing_haraka
    ambiguity
    foreignness
    tashif
    spelling_variation
    weak_root_uncertainty
    shared_pattern
    unknown_lexeme

Rank:
    candidate | hypothesis | strong_hypothesis | certificate

Output:
    WordformCandidateSet

Forbidden:
    final_meaning
    syntactic_role
    hukm
    reality
```

### القانون الحاسم (Critical Law):

```
الوزن لا يعطي معنى.
الجذر لا يعطي حكمًا.
المعجم لا يعطي سياقًا.
اللفظ لا يعطي علاقة تركيبية وحده.
```

```
Pattern does NOT give meaning.
Root does NOT give judgment.
Lexicon does NOT give context.
Lafz does NOT give compositional relation alone.
```

---

## خوارزمية التركيب
## Composition Algorithm

```python
Algorithm: compose_arabic_relations

Input:
    WordformCandidateSet

Carrier:
    wordform_candidate
    operator_candidate
    governor_candidate
    governed_candidate
    relation_edge
    reference_anchor
    case_trace
    order_trace
    deletion_estimate
    residual_set

Prior:
    syntax_governor_registry
    particle_registry
    nasikh_registry
    idafa_rules
    tawabi_rules
    predication_rules
    reference_rules
    ellipsis_policy
    rank_policy

Gate:
    composition_license_gate

Operations:
    detect_operators
    detect_governors
    detect_possible_governed
    build_relation_edges
    test_case_effects
    test_order_distance
    test_reference_links
    license_ellipsis_if_needed
    close_relation_network

Identity:
    preserve_wordform_trace
    preserve_operator_trace
    preserve_relation_trace

Candidates:
    RelationCandidate
    ReferenceCandidate
    CompositionCandidate

Residuals:
    missing_governor
    possible_hidden_governor
    weak_case_evidence
    ambiguous_attachment
    possible_fronting
    possible_deletion
    reference_ambiguity
    competing_relation

Rank:
    candidate | hypothesis | strong_hypothesis | certificate

Output:
    ClosedDalNetworkCandidate
    OR Ifadah_Dal (if predication/reference/relation network closes)

Forbidden:
    final_contextual_meaning
    hukm
    reality
```

---

## القوانين الخمسة عشر المصححة للتركيب
## Fifteen Corrected Laws of Composition

### 1. لا تركيب بلا ترخيص
**No composition without license**

```
لا تركيب مرخّص بلا عامل أو رابط أو مطابقة أو إحالة أو تقدير عامل مرخّص.
```

No licensed composition without operator OR link OR agreement OR reference OR licensed operator estimation.

**Rationale**: Not all relations are strictly "operator-based" in the narrow sense. Dependencies, references, and agreement are also compositional relations.

---

### 2. العامل ينتج ترخيص علاقة، لا معنى
**Operator produces relation license, not meaning**

```
العامل لا ينتج معنى نهائيًا، بل ينتج ترخيص علاقة.
```

Operator does NOT produce final meaning; it produces RelationLicense.

**Output**: `RelationLicense`
**NOT**: `FinalMeaning`

---

### 3. المعمول يثبت بأثر مرخّص
**Ma'mul established by licensed effect**

```
المعمول لا يثبت معمولًا إلا بأثر عامل أو رابط أو تبعية أو مطابقة مرخّصة.
```

Ma'mul is NOT established as ma'mul except through effect of operator OR link OR dependency OR licensed agreement.

**Rationale**: Adjectives (na't) follow their modified nouns through dependency, not operator action.

---

### 4. الإعراب أثر قوي، لا أصل مستقل
**I'rab is strong trace, not independent source**

```
الإعراب أثر علاقة قوي، لا دليل مستقل على العلاقة.
```

I'rab is a strong relation trace, NOT independent evidence of relation.

**Principle**: I'rab is powerful evidence but insufficient alone when blockers or ambiguity exist.

---

### 5. الوزن لا ينتج دورًا نحويًا بلا عامل
**Pattern does not produce syntactic role without operator**

```
اسم الفاعل على وزن "فاعل" لا يعني أنه فاعل نحوي بلا تركيب.
```

Active participle on pattern "fā'il" does NOT mean it is a syntactic agent without composition.

**Example**:
```
كاتبٌ الدرسَ
```
"kātib" is morphologically active participle, but NOT necessarily syntactic fā'il until compositional analysis.

---

### 6. الرتبة ترجّح، لا تنشئ
**Rank boosts, does not create**

```
الرتبة لا تنتج علاقة بلا عامل؛ الرتبة ترجّح علاقة، لا تنشئها.
```

Rank does NOT produce relation without operator; rank boosts relation, does not create it.

**Principle**: Word order is evidence, not source.

---

### 7. التقديم والتأخير يغيران المسافة ويرفعان الحاجة للقرينة
**Fronting/backing changes distance and raises need for evidence**

```
التقديم والتأخير لا يلغيان العامل، بل يغيران مسافة العمل ويزيدان البقايا.
```

Fronting and backing do NOT cancel operator, but change operation distance and increase residuals.

---

### 8. الحذف والتقدير بوابة صارمة
**Ellipsis and estimation are strict gates**

```
الحذف والتقدير لا يقبلان إلا عند الحاجة وبأثر وبقايا.
```

Ellipsis and estimation are NOT accepted except when needed, with trace, and with residuals.

**Gate**: `EllipsisGate`

---

### 9. النواسخ محوّلات للإسناد
**Nawāsikh are predication transformers**

```
النواسخ عوامل تحويل في بنية الإسناد، لا مغيرات إعراب فقط.
```

Nawāsikh are operators that transform predication structure, NOT merely i'rab changers.

**Classification**:
- كان وأخواتها: Temporal transformation
- إنّ وأخواتها: Emphasis/assertion transformation
- ظننت وأخواتها: Epistemic transformation

**Example**:
```
زيد قائم        → Direct predication
كان زيد قائمًا    → Temporal predication transformation
إن زيدًا قائم    → Assertion predication transformation
ظننت زيدًا قائمًا  → Epistemic predication transformation
```

---

### 10. الحروف مشغّلات علاقات مصنّفة
**Particles are classified relation operators**

```
الحروف العاملة مشغلات علاقات، وتصنّف حسب نوع العلاقة.
```

Operator particles are relation operators, classified by relation type.

**Taxonomy**:
- CaseOperator (حروف الجر)
- RelationOperator (أحرف العطف)
- ConditionOperator (أدوات الشرط)
- NegationOperator (أدوات النفي)
- RestrictionOperator (أدوات الحصر)
- ReferenceOperator (أسماء الإشارة، الموصول)
- CausalityOperator (لام التعليل، لام كي)
- PurposeOperator (حتى، كي)

---

### 11. الإضافة عامل ربط اسمي
**Idafa is nominal binding operator**

```
الإضافة عامل ربط اسمي داخل عقدة ملكية/تخصيص/بيان/ظرفية/مادة.
```

Idafa is NominalBindingOperator within node of possession/specification/clarification/adverbial/material.

**NOT**: Simple operator
**IS**: Binding operator creating compositional nominal unit

---

### 12. التوابع حافة تبعية مرخّصة
**Tawābi' are licensed dependency edges**

```
التوابع تعمل داخل حافة تبعية مرخّصة تحمل: تابع، متبوع، نوع التبعية، مطابقة، أثر إعرابي، بقايا.
```

Tawābi' operate within licensed dependency edge carrying: tābi', matbū', dependency_type, agreement, i'rab_trace, residuals.

**Structure**:
```python
DependencyEdge = {
    tabi': WordformCandidate,
    matbu': WordformCandidate,
    dependency_type: Na't | Atf | Tawkid | Badal,
    agreement: AgreementSpec,
    i3rab_trace: Trace,
    residuals: ResidualSet
}
```

---

### 13. كل عامل له: مجال، شروط، موانع، أثر، أثر تتبعي، رتبة، بقايا
**Every operator has: scope, conditions, blockers, effect, trace, rank, residuals**

```
عامل = مجال + شروط + موانع + أثر + أثر تتبعي + رتبة + بقايا
```

```python
Operator = {
    scope: Scope,
    conditions: ConditionSet,
    blockers: BlockerSet,
    effect: Effect,
    trace: Trace,
    rank: Rank,
    residuals: ResidualSet
}
```

---

### 14. لا إفادة دالية إلا بإغلاق الشبكة
**No dal ifadah without network closure**

```
لا إفادة دالية إلا بعد إغلاق شبكة العامل والمعمول والإحالة والنسبة.
```

No dal ifadah except after closure of operator-ma'mul-reference-relation network.

**Closure Requirements**:
- [ ] Operator-ma'mul relations closed or residuals classified
- [ ] References resolved or residuals classified
- [ ] Predication established or residuals classified
- [ ] No blocking residuals

---

### 15. العامل لا ينتج حكمًا ولا واقعًا
**Operator does not produce judgment or reality**

```
العامل ينتج علاقة.
العلاقة تنتج إفادة دالية.
الإفادة تحتاج مدلولًا سياقيًا.
المطابقة تحتاج عقدًا.
الحكم يحتاج دليلًا.
الواقع يحتاج تنزيلًا.
```

```
Operator → Relation
Relation → Dal Ifadah
Ifadah needs → Contextual Madlul
Matching needs → Contract
Judgment needs → Evidence
Reality needs → Tanzil
```

---

## مثال العامل: خوارزمية الحاكم
## Governor Algorithm Example

```python
GovernorAlgorithm = {
    Input: WordformCandidateSet,

    Carrier:
        governor_candidate,
        governed_candidate,
        operator_candidate,
        case_trace,
        relation_edge,

    Prior:
        governor_registry,
        operator_registry,
        syntax_rules,
        ellipsis_policy,

    Gate:
        governor_license_gate,

    Operation:
        detect_governor,
        test_scope,
        test_conditions,
        test_blockers,
        apply_effect,
        preserve_trace,

    Identity:
        preserve_wordform_identity,

    Candidate:
        RelationLicense,

    Residuals:
        missing_case,
        ambiguous_governed,
        hidden_governor_possible,
        order_distance,

    Rank:
        candidate | hypothesis | strong_hypothesis | certificate,

    Output:
        RelationCandidate,

    Forbidden:
        final_meaning,
        hukm,
        reality
}
```

---

## مسار الطبقات الإجباري
## Mandatory Layer Pipeline

### المسار الكامل (Complete Pipeline):

```
RawInput
    ↓ [analyze_surface_dal]
LafzCandidate
    ↓ [analyze_wordform]
WordformCandidate
    ↓ [prepare_for_composition]
PreSyntaxCandidate
    ↓ [compose_relations]
RelationCandidate
    ↓ [close_dal_ifadah]
Ifadah_Dal
    ↓ [match_dal_madlul]
DalMadlulContract
    ↓ [infer_contextual_meaning]
MadlulCandidate
    ↓ [infer_murad]
MuradCandidate
    ↓ [infer_hukm]
HukmCandidate
    ↓ [apply_tanzil]
TanzilResult
```

### القفزات الممنوعة (Forbidden Jumps):

```
❌ LafzCandidate → Ifadah_Dal
❌ WordformCandidate → Meaning
❌ WeightCandidate → Syntactic Role
❌ RelationCandidate → Hukm
❌ Ifadah_Dal → Reality
❌ ANY → skip intermediate layers
```

---

## التشبيه بعروض الخليل
## Analogy with Al-Khalil's Prosody

### عروض الخليل (Al-Khalil's Prosody):

```
Poetry Verse (بيت شعري)
    ↓ [orthographic_transcription]
Prosodic Writing (كتابة عروضية)
    ↓ [segmentation]
Movements and Pauses (حركات وسكنات)
    ↓ [grouping]
Sabab and Watid (أسباب وأوتاد)
    ↓ [pattern_matching]
Taf'ila (تفعيلة)
    ↓ [variation_detection]
Zihaf and 'Illah (زحاف وعلة)
    ↓ [meter_classification]
Bahr (بحر) OR Kasr (كسر - broken)
```

### جبر العربية (Arabic Algebra):

```
Arabic Utterance (لفظ عربي)
    ↓ [dal_analysis]
Dal Candidate (مرشح دالي)
    ↓ [compositional_analysis]
Relation Network (شبكة علاقات)
    ↓ [closure]
Dal Ifadah (إفادة دالية)
    ↓ [semantic_matching]
Madlul Candidate (مرشح مدلولي)
    ↓ [contextual_inference]
Murad (مراد)
    ↓ [judgment_inference]
Hukm Candidate (مرشح حكم)
    ↓ [reality_application]
Tanzil (تنزيل)
```

### الفرق الأساسي (Key Difference):

**عروض الخليل**:
- Domain: Poetic meter (الوزن الشعري)
- Scope: Specific to poetry
- Special case of pattern analysis

**جبر العربية**:
- Domain: All Arabic linguistic analysis
- Scope: Lafz → Wordform → Composition → Ifadah → Meaning → Judgment → Reality
- General Arabic Algebraic Parser

> عروض الخليل حالة خاصة من: ArabicFormalPatternAlgorithm
> Al-Khalil's prosody is special case of: ArabicFormalPatternAlgorithm

> مشروعك يريد: General Arabic Algebraic Parser
> Your project aims for: General Arabic Algebraic Parser

---

## الخلاصة الجامعة
## Comprehensive Summary

### القوانين الست الجامعة (Six Universal Laws):

1. **الجبر = الدستور**
   Algebra = Constitution

2. **الخوارزمية = التنفيذ**
   Algorithm = Execution

3. **البوابة = الترخيص**
   Gate = Licensing

4. **الأثر = Trace**
   Effect = Trace

5. **البقايا = مانع الادعاء**
   Residuals = Claim Blockers

6. **الرتبة = قوة النتيجة**
   Rank = Result Strength

### الممنوع = منع القفز (Forbidden = Jump Prevention):

```
كما أن عروض الخليل حوّل الشعر إلى تقطيع مرخّص،
فجبر العربية يجب أن يحوّل اللفظ والتركيب إلى تحليل مرخّص،
لا يقفز من صوت إلى معنى،
ولا من وزن إلى وظيفة،
ولا من عامل إلى حكم،
ولا من إفادة إلى واقع.
```

```
Just as Al-Khalil's prosody transformed poetry into licensed analysis,
Arabic algebra must transform utterance and composition into licensed analysis,
that does NOT jump from sound to meaning,
nor from pattern to function,
nor from operator to judgment,
nor from ifadah to reality.
```

---

## الاستخدام في المشروع
## Project Usage

### Implementation Requirements:

1. **Every algorithm file MUST:**
   - Declare its Input type
   - Declare its Carrier types
   - Reference Prior knowledge sources
   - Implement Gate(s)
   - Define Operations
   - Specify Identity preservation
   - Produce bounded Candidates
   - Generate Trace
   - Track Residuals
   - Assign Rank
   - Declare bounded Output
   - List Forbidden outputs

2. **Every algorithm MUST:**
   - NOT skip layers
   - NOT jump domains
   - NOT produce forbidden outputs
   - PRESERVE trace from input
   - PRODUCE reversible audit trail

3. **Testing Requirements:**
   - Test layer boundaries
   - Test forbidden output prevention
   - Test trace preservation
   - Test residual tracking
   - Test rank assignment accuracy

---

**Constitutional Authority**: This document establishes binding law for all algorithmic implementation in the Arabic Algebra project.

**Enforcement**: All PRs implementing algorithms MUST demonstrate compliance with this constitution.

**Version Control**: Changes to this constitution require explicit justification and project-wide review.

---

**والله أعلم**
**And Allah knows best**
