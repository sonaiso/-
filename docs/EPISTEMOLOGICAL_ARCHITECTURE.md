# البنية المعرفية: الأصول والجسور والفروع
# Epistemological Architecture: Origins, Bridges, and Branches

**Created**: 2026-05-30
**Status**: Constitutional Framework
**Integration**: Post PR #165 (K9 Storage Governance)

---

## الصيغة الجامعة | The Unifying Formula

```
الأصل = ما لا ينتجه النظام من داخله في تلك المرحلة، بل يعتمد عليه كبداية مرخِّصة
الجسر = آلية الانتقال من أصل إلى فرع
الفرع = نتيجة مشتقة لا تُقبل إلا ببرهان انتقال
```

**English**:
- **Origin** = What the system does not produce internally at that stage, but depends on as a licensing foundation
- **Bridge** = The mechanism of transition from origin to branch
- **Branch** = A derived result that is only accepted with proof of transition

---

## 1. الأصول المعرفية | Epistemological Origins

### المبدأ الأساسي | Fundamental Principle

Origins are NOT all of the same rank. Some are fixed origins, some are auditory (سماعي), some are trace-based (أثري), some are universal (كلي).

### أ. الجداول | Tables

Tables are closed or semi-closed operational origins.

**Examples**:
- Unicode Arabic table
- Letters table (الحروف)
- Diacritics table (الحركات)
- Pause and connection marks (الوقف والوصل)
- Original weights/patterns (الأوزان الأصلية)
- Addition letters (أحرف الزيادة)
- Pronouns table (الضمائر)
- Meaning particles (حروف المعاني)
- Operators table (العوامل)
- Original and derived case markers (العلامات الإعرابية الأصلية والفرعية)
- Diptotes (الممنوع من الصرف)
- Five verbs (الأفعال الخمسة)
- Abrogating verbs (الأفعال الناسخة)

**K9 Storage Rule**:
```python
# Store the tabular origin, NOT all results
StorePrimitive(table_rule)  # ✅
StorePrimitive(every_instance_of_rule)  # ❌

# Example:
# ✅ Store: "Wāw is a rafʿ marker in sound masculine plural"
# ❌ Do NOT store: Every rafʿ instance of every sound masculine plural
```

---

### ب. الجذور | Roots

The root is a material origin, but it is NOT a final meaning.

**Examples**:
- ك ت ب (k-t-b)
- ض ر ب (ḍ-r-b)
- خ ر ج (kh-r-j)
- د خ ل (d-kh-l)
- ق و م (q-w-m)

**Constitutional Law**:
```
الجذر = حامل مادة قابل للتركيب مع وزن وصيغة وسياق
Root = Material carrier capable of composition with pattern, form, and context

الجذر ≠ المعنى
Root ≠ Meaning
```

**Classification**:
```python
# Origin (stored)
root = "ك ت ب"  # k-t-b

# Branches (derived, NOT stored as primitives)
derived_1 = root + pattern("فَعَلَ") + licensing  # كَتَبَ
derived_2 = root + pattern("فاعل") + licensing  # كاتب
derived_3 = root + pattern("مفعول") + licensing  # مكتوب
derived_4 = root + pattern("فِعَالَة") + licensing  # كتابة
```

---

### ج. القواعد | Rules

Rules are operational origins, NOT results.

**Examples**:
- Syllable licensing rule (قاعدة ترخيص المقطع)
- Pattern application rule (قاعدة انطباق الوزن)
- Augmentation rule (قاعدة المزيد)
- Transitivity rule (قاعدة اللزوم والتعدي)
- Passive voice rule (قاعدة المبني للمجهول)
- Imperative from jussive rule (قاعدة الأمر من المضارع المجزوم)
- Jussive by weak letter deletion (قاعدة الجزم بحذف حرف العلة)
- Jussive by nūn deletion (قاعدة الجزم بحذف النون)
- Diptote rule (قاعدة الممنوع من الصرف)
- Operator-operand rule (قاعدة العامل والمعمول)
- Attribution rule (قاعدة الإسناد)
- Specification rule (قاعدة التقييد)
- Annexation rule (قاعدة الإضافة)
- Description rule (قاعدة الوصف)
- Reference rule (قاعدة الإحالة)
- Informativeness rule (قاعدة الإفادة)
- Judgment rule (قاعدة الحكم)

**Critical Principle**:
```
قاعدة + أصل + فرع مرشح + علة + فرق قادح + حفظ هوية + أثر
= انتقال مقبول

Rule alone does NOT produce branch.
Bridge required: Rule + Origin + Candidate + Cause + Difference + Identity + Trace
```

---

### د. العلاقات الأولية | Primary Relations

These are general relational origins BEFORE sentences.

**Examples**:
- Carrier ← Carried (حامل ← محمول)
- Operator ← Operand (عامل ← معمول)
- Cause ← Effect (سبب ← مسبب)
- Quality ← Qualified (صفة ← موصوف)
- Possessor ← Possessed (مضاف ← مضاف إليه)
- Referrer ← Referent (مشير ← مرجع)
- Restrictor ← Restricted (مقيِّد ← مقيَّد)
- Part ← Whole (جزء ← كل)
- Species ← Genus (نوع ← جنس)
- Event ← Potential agent (حدث ← فاعل محتمل)
- Event ← Potential patient (حدث ← مفعول محتمل)
- Time ← Event (زمن ← حدث)
- Place ← Event (مكان ← حدث)

**Constitutional Warning**:
```
Primary relations do NOT give final meaning.
They give the FORM of a possible relation.

Example:
Event + Potential Agent
≠ Agent actually performed the event
= There is a formal agent slot available for licensing
```

---

### هـ. الكليات | Universals

Universals are higher conceptual origins.

**Examples**:
- Human ⊂ Animal (إنسان ⊂ حيوان)
- Horse ⊂ Animal (فرس ⊂ حيوان)
- Book ⊂ Manufactured/Written (كتاب ⊂ مصنوع / مكتوب)
- Writing ⊂ Event (كتابة ⊂ حدث)
- Standing ⊂ State/Quality/Positional Event (قيام ⊂ هيئة / صفة / حدث وضعي)
- Color ⊂ Quality (لون ⊂ صفة)
- Place ⊂ Circumstantial (مكان ⊂ ظرف)
- Time ⊂ Circumstantial (زمان ⊂ ظرف)
- Tool ⊂ Operator (أداة ⊂ مشغّل)

**Critical Layer Placement**:
```
Universals enter AFTER signifier and composition layers,
during informativeness construction, NOT before.
```

**FORBIDDEN Pattern**:
```python
# ❌ WRONG: Direct projection to universal
if word == "كاتب":
    return Universal("human who writes")

# ✅ CORRECT: Layered derivation
word = "كاتب"
→ derived_pattern_licensed
→ compositional_relation
→ context
→ potential_concept
→ informativeness
→ judgment (if evidence exists)
```

---

### و. الآثار | Traces

**The trace is a very special origin in this project.**

The trace is NOT a rule, but a RECORD of what happened.

**Examples**:
```python
TransitionProof
AlgorithmTracePayload
candidate_ids
residual_ids
gate_ids
rank_values
source_trace_id
evaluation_report
```

**Trace as Origin for T5**:
```
T5 does NOT explain from vacuum.
T5 explains a preserved trace.

Trace = What happened in the algorithm
Trace ≠ What is true in reality
```

---

### ز. السماع | Auditory Authority (Samāʿ)

Auditory authority is an origin when analogy (qiyās) is insufficient.

**Examples**:
- Auditory form (صيغة سماعية)
- Auditory verbal noun (مصدر سماعي)
- Intransitive by hearing (فعل لازم سماعًا)
- Transitive by hearing (فعل متعدٍ سماعًا)
- Auditory plural (جمع سماعي)
- Auditory diptote or proper noun (ممنوع من الصرف سماعي أو علمي)
- Special particle usage (استعمال خاص لحرف)
- Conventional transferred meaning (معنى اصطلاحي منقول)

**Storage Rule**:
```python
# Auditory cannot be derived from general rule
# Therefore stored as origin or lexical_proof
# But MUST have source or rank, not admitted without trace

ProofSource.LEXICAL  # Auditory evidence
ProofSource.TABLE    # Recorded in authoritative table
```

---

### ح. الاستثناءات | Exceptions

An exception is NOT a general rule, but a BLOCKER to generalizing the rule.

**Examples**:
- Verb does not follow expected transitivity pattern
- Verbal noun does not follow expected pattern
- Word is diptote despite expected inflection
- Fixed construction does not accept case marking
- Conventional usage not analogized to

**Constitutional Law**:
```
الاستثناء محفوظ في موضعه
Exception is preserved in its place

الاستثناء لا يتحول إلى قاعدة إلا ببرهان تعميم مستقل
Exception does NOT become rule except with independent generalization proof
```

---

## 2. الجسور المعرفية | Epistemological Bridges

**The bridge is what allows transition from origin to branch.**

```
الأصل وحده لا ينتج
الفرع وحده لا يقبل
لا بد من جسر

Origin alone does not produce
Branch alone is not accepted
Bridge is necessary
```

---

### أ. القياس | Analogy (Qiyās)

Analogy says: This branch attaches to this origin due to a unifying cause.

**Formula**:
```
أصل مرخّص
+ فرع مرشح
+ وصف مؤثر
+ علة جامعة
+ لا فرق قادح
= انتقال مقبول

Licensed origin
+ Candidate branch
+ Effective description
+ Unifying cause
+ No invalidating difference
= Accepted transition
```

**Example**:
```python
origin_pattern = "فَعَلَ"
candidate_branch = "كَتَبَ"
unifying_cause = "trilateral root compatibility with vowel/slot distribution"
invalidating_difference = None
result = "Pattern applies, candidate licensed"
```

---

### ب. برهان الانتقال | Transition Proof

Transition proof is broader than analogy; it records EVERYTHING:

```python
@dataclass
class TransitionProof:
    origin: Origin
    branch: Branch
    effective_description: Description
    unifying_cause: Cause
    invalidating_differences: list[Difference]
    identity_preservation: IdentityPreservation
    minimal_completion: MinimalCompletion
    trace: Trace
    rank: Rank
    residuals: list[Residual]
```

**Constitutional Law**:
```
لا انتقال بلا برهان
No transition without proof
```

---

### ج. المناط | Applicability Condition (Manāṭ)

The manāṭ determines WHEN the rule works and when it does NOT.

**Example**:
```
وزن فاعل لا ينتج فاعلية دائمًا
Pattern fāʿil does NOT always produce agency

المناط يقول:
إذا كان الأصل حدثيًا
والسياق يفتح علاقة فعلية
ولا يوجد تجمد أو وصفية محضة
جاز ترشيح الفاعلية

Manāṭ says:
IF origin is eventive
AND context opens verbal relation
AND no fossilization or pure descriptiveness
THEN agency candidacy permitted
```

**Application**:
```python
# كاتب - may open agency (eventive, active pattern)
word = "كاتب"
if eventive and verbal_context and not_fossilized:
    agency_candidate = True

# طاهر، حامض، بارد - do NOT treat as agents
# despite fāʿil pattern (descriptive, not agentive)
words = ["طاهر", "حامض", "بارد"]
for word in words:
    agency_candidate = False  # Pure descriptive, manāṭ not met
```

---

### د. حفظ الهوية | Identity Preservation

Identity preservation is the NEUTRAL ELEMENT in this project.

**Constitutional Requirement**:
```
أي انتقال يجب أن يثبت:
هوية الحامل قبل الانتقال محفوظة بعد الانتقال

Any transition must prove:
Carrier identity before transition is preserved after transition
```

**Example**:
```python
root_identity = "ك ت ب"  # k-t-b

# Derive multiple branches
derived_branches = [
    "كاتب",   # kātib
    "مكتوب",  # maktūb
    "كتابة",  # kitāba
]

# Material identity MUST be preserved
for branch in derived_branches:
    assert preserves_material_identity(root_identity, branch)
    # Record what changed:
    changes = {
        "pattern": ...,
        "vowels": ...,
        "augmentation": ...,
        "form": ...,
        "time": ...,
        "voice": ...,
    }
```

**FORBIDDEN**:
```python
# ❌ Trace becomes identity
output_identity = anchor.trace  # VIOLATION

# ❌ Identity lost in bridge
transition_output = process(input_identity)
if transition_output.identity != input_identity:
    raise IdentityLossViolation
```

---

### هـ. فحص الفرق القادح | Invalidating Difference Check

The invalidating difference is what PREVENTS analogizing the branch to the origin.

**Examples**:
- Word resembles pattern but is foreign (أعجمية)
- Form resembles verb but is proper noun (اسم علم)
- Marker resembles rafʿ but in indeclinable (مبني)
- Particle resembles operator but is not operative in this context
- Intransitive verb does not accept object without augmentation or auditory authority
- Augmented verb did not fulfill causation cause

**Effect**:
```python
if invalidating_difference_detected:
    decision = BLOCK or DEFER
```

---

## 3. الفروع المعرفية | Epistemological Branches

**Branches are derived results. They are NOT stored as origins per K9.**

---

### أ. وزن منطبق | Applied Pattern

```python
root + pattern + vowels + minimal_completion
→ WeightCandidate

# NOT meaning

pattern("فَعَلَ") + root("ك ت ب")
→ "كَتَبَ" as pattern_candidate
```

---

### ب. كلمة مرخصة | Licensed Word

```python
licensed_signifier
+ root/stem
+ pattern or construction
+ prefixes/suffixes
+ identity_preservation
+ residuals
→ Word/Lafẓ Mufrad Candidate

# NO meaning, NO informativeness, NO judgment
```

---

### ج. عامل | Operator

```python
# Operator is NOT accepted merely because stored in table

operator_primitive
+ context
+ scope
+ candidate_operand
+ no_blocker
→ OperatorCandidate
```

**Example**:
```python
particle = "لم"  # lam (negation + jussive)

# Stored as origin
# But being operator in specific sentence is DERIVED BRANCH

operator_candidate = OperatorCandidate(
    primitive="لم",
    context=sentence_context,
    scope=verb_scope,
    operand_candidate=verb,
    blockers=[],
)
```

---

### د. أثر إعرابي | Case Effect

```python
# Case effect does NOT come from marker alone

operator
+ operand
+ position
+ marker
+ policy
+ matrix_row
→ CaseEffectCandidate
```

**Example**:
```python
word = "زيدُ"  # Zaydun (rafʿ marker)

# Does NOT mean automatically it is subject
# May give:
surface_candidate = RafʿSurfaceCandidate

# Then needs operator or position
```

---

### هـ. علاقة | Relation

```python
# Relation is derived branch from preserved endpoints

first_endpoint
+ second_endpoint
+ relation_type
+ licensing
+ no_invalidating_difference
→ RelationCandidate
```

**Relation Types**:
- Attribution (إسناد - ISNAD)
- Specification (تقييد - TAQYID)
- Inclusion (تضمين - TADMIN)
- Annexation (إضافة - IDAFAH)
- Description (وصف - WASF)
- Reference (إحالة)
- Causation (سببية)
- Effect (مسببية)

**But does NOT give informativeness yet.**

---

### و. إفادة | Informativeness (Ifādah)

Informativeness is a higher branch.

```python
# Does NOT come from mere relation existence
# But from formal and conceptual completion

relation_candidate
+ prior_concepts
+ predication_capability
+ description_capability
+ domain
+ maqām (context)
+ no_blocking_residuals
→ IfadahCandidate
```

**Informativeness is NOT judgment.**

```
Informativeness says:
We now have an informative statement within a controlled domain

Does NOT say:
This is true in reality
```

---

### ز. حكم | Judgment (Ḥukm)

**Judgment is the highest and most dangerous branch.**

```python
# Only comes after:

informativeness
+ evidence
+ valid_domain
+ preserved_correspondence
+ sufficient_rank
+ absence_of_conflicting_blocker
→ HukmCandidate
```

**Formula**:
```python
ifadah_candidate
+ Evidence
+ Reality/Domain_Matching
+ Rank
+ Residual_audit
→ HukmCandidate
```

**CONSTITUTIONAL LAW**:
```
T5 MUST NOT produce Hukm
```

---

## 4. الخريطة الكاملة | Complete Map

```
الأصول (Origins)
│
├─ جداول (Tables)
├─ جذور (Roots)
├─ قواعد (Rules)
├─ علاقات أولية (Primary Relations)
├─ كليات (Universals)
├─ آثار (Traces)
├─ سماع (Auditory Authority)
└─ استثناءات (Exceptions)

        عبر الجسور (via Bridges)

├─ قياس (Analogy)
├─ برهان انتقال (Transition Proof)
├─ مناط (Applicability Condition)
├─ حفظ هوية (Identity Preservation)
└─ فحص فرق قادح (Invalidating Difference Check)

        تنتج الفروع (produce Branches)

├─ وزن منطبق (Applied Pattern)
├─ كلمة مرخصة (Licensed Word)
├─ عامل مرشح (Operator Candidate)
├─ أثر إعرابي (Case Effect)
├─ علاقة (Relation)
├─ إفادة (Informativeness)
└─ حكم (Judgment)
```

---

## 5. الفرق بين الأصل والفرع في K9 | Origin vs Branch in K9

**K9 Storage Governance Rules**:

```python
# Origin is stored
StorageKind.PRIMITIVE if is_origin and not_derivable

# Branch is NOT stored as primitive
if is_branch and derivable:
    storage_kind = StorageKind.DERIVED_ARTIFACT
    # Branch re-derived when needed

# But branch CAN be stored as artifact with conditions:
@dataclass
class StoredBranch:
    storage_kind: StorageKind.DERIVED_ARTIFACT  # NOT PRIMITIVE
    source_trace_id: str  # Required
    derivation_rule_id: str  # Required
    regeneration_policy: RegenerationPolicy  # Required
```

**Example**:
```python
# TrainingExample is branch derived from trace
# Stored as artifact, NOT origin

training_example = TrainingExample(...)
k9_item = K9Item(
    storage_kind=StorageKind.DERIVED_ARTIFACT,  # NOT PRIMITIVE
    derivable=True,
    proof_source=ProofSource.TRACE,  # NOT MODEL_OUTPUT
    source_trace_id=trace_id,
    derivation_rule_id="TraceExplanationDatasetGenerator",
    regeneration_policy=RegenerationPolicy.ON_TRACE_CHANGE,
)
```

---

## 6. القاعدة الذهبية | The Golden Rule

```
إذا كان الشيء يُنتج من جدول + قاعدة + قياس + أثر،
فهو فرع لا أصل

If something is produced from table + rule + analogy + trace,
it is a branch, NOT an origin

وإذا لم يمكن إنتاجه إلا بالسماع أو الجذر أو الجدول أو الكلي الأولي،
فهو أصل

If it can only be produced by auditory authority, root, table, or primary universal,
it is an origin

وإذا كان مشتقًا لكنه خالف القياس،
فنخزن الاستثناء لا النتيجة كلها

If it is derived but violated analogy,
we store the exception, NOT the entire result
```

---

## 7. الصيغة الرياضية | Mathematical Formula

**Notation**:
```
O = Origin
B = Bridge
F = Branch
```

**Derivation**:
```
F = B(O)
```

**Acceptance Conditions**:
```
Accept(F) ⇔
    Licensed(B)
    ∧ IdentityPreserved(O,F)
    ∧ NoInvalidatingDifference(O,F)
    ∧ ManatApplies(B,O,F)
    ∧ TraceComplete
    ∧ RankAssigned
```

**Storage Rule**:
```
StorePrimitive(x) ⇔ Origin(x) ∧ ¬Derivable(x)

Branch(x) ∧ Derivable(x) ⇒ ¬StorePrimitive(x)
```

---

## 8. التكامل مع K9 Storage Governance | Integration with K9

This epistemological architecture directly informs K9 storage decisions:

```python
def classify_epistemological_type(item):
    """Classify item as Origin, Bridge, or Branch"""

    # Origins (may be stored as PRIMITIVE)
    if is_table_rule(item):
        return EpistemologicalType.ORIGIN, StorageKind.PRIMITIVE

    if is_root(item):
        return EpistemologicalType.ORIGIN, StorageKind.PRIMITIVE

    if is_auditory_authority(item):
        return EpistemologicalType.ORIGIN, StorageKind.PRIMITIVE

    if is_exception(item):
        return EpistemologicalType.ORIGIN, StorageKind.EXCEPTION_OVERRIDE

    if is_trace(item):
        return EpistemologicalType.ORIGIN, StorageKind.TRACE_LOG

    # Bridges (procedures, not stored as data)
    if is_analogy_procedure(item):
        return EpistemologicalType.BRIDGE, None

    if is_transition_proof(item):
        return EpistemologicalType.BRIDGE, StorageKind.TRACE_LOG

    # Branches (derived, stored as artifacts if needed)
    if is_derived_result(item):
        return EpistemologicalType.BRANCH, StorageKind.DERIVED_ARTIFACT
```

---

## 9. الخلاصة النهائية | Final Summary

```
الأصول:
ما لا يشتقه النظام في تلك الطبقة:
جداول، جذور، قواعد، علاقات أولية، كليات، آثار، سماع، استثناءات

Origins:
What the system does not derive at that layer:
Tables, Roots, Rules, Primary Relations, Universals, Traces, Auditory Authority, Exceptions

الجسور:
ما يبرر الانتقال:
قياس، برهان انتقال، مناط، حفظ هوية، فحص فرق قادح

Bridges:
What justifies the transition:
Analogy, Transition Proof, Applicability Condition, Identity Preservation, Invalidating Difference Check

الفروع:
ما ينتجه النظام:
وزن منطبق، كلمة مرخصة، عامل مرشح، أثر إعرابي، علاقة، إفادة، حكم

Branches:
What the system produces:
Applied Pattern, Licensed Word, Operator Candidate, Case Effect, Relation, Informativeness, Judgment
```

---

## القانون الحاكم | The Governing Law

```
الأصل يُخزّن
Origin is stored

الجسر يُطبّق
Bridge is applied

الفرع يُشتق
Branch is derived

الأثر يُحفظ
Trace is preserved

الاستثناء يُقيّد
Exception is restricted

الحكم لا ينتج إلا بدليل
Judgment is only produced with evidence
```

---

**File**: `/home/runner/work/-/-/docs/EPISTEMOLOGICAL_ARCHITECTURE.md`
**Integration**: Post PR #165 (K9 Storage Governance)
**Related**: `K9_STORAGE_GOVERNANCE_CONSTITUTION.md`, `IDENTITY_VS_TRACE_SEMANTICS.md`
**Status**: Constitutional Framework

