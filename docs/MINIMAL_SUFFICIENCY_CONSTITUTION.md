# دستور الحد الأدنى الكافي | Minimal Sufficiency Constitution

**Status**: Constitutional Framework
**Version**: 1.0
**Date**: 2026-05-24
**Authority**: Supreme Law of the General Algebra

---

## القانون الأعلى | The Supreme Law

**الجبر العام لا يتوسع بالتراكم، بل يتدرج بالحد الأدنى الكافي.**

**The General Algebra does not expand by accumulation, but progresses by minimal sufficiency.**

This means:

1. **No new concept** until proven it is not merely a branch of an existing concept
2. **No new rule** until proven it is not a special case of a general rule
3. **No new layer** until proven the transition cannot be governed without it
4. **No new gate** until proven there exists a forbidden leap that no existing gate prevents

---

## 1. مبدأ منع التضخم | Anti-Inflation Principle

### The Problem

Every new concept, observation, or relation cannot become:
- A new **layer**
- A new **rule**
- A new **gate**

Otherwise, the algebra **explodes** (inflates uncontrollably).

### The Law

**لا أصل لما يكفيه فرع.**
**No foundation for what a branch suffices.**

- No **layer** for what a **rule** suffices
- No **general rule** for what a **specific rule** suffices
- No **specific rule** for what a **case** suffices
- No **case** without **trace**

---

## 2. البنية المنهجية لكل مجال | Methodological Structure of Every Domain

Every domain in the General Algebra must be built following this exact progression:

```text
الفكرة الكلية    (Core Idea)
    ↓
الطريقة         (Method)
    ↓
القواعد العامة   (General Rules)
    ↓
القواعد الخاصة   (Specific Rules)
    ↓
الحالات         (Cases)
    ↓
البقايا         (Residuals)
    ↓
المراجعة        (Revision)
```

### Definition of Each Level

1. **CoreIdea** (الفكرة الكلية): The intellectual foundation that defines the domain's subject
2. **Method** (الطريقة): How to operate within this domain
3. **GeneralRules** (القواعد العامة): Rules governing the most frequent transitions
4. **SpecificRules** (القواعد الخاصة): Rules addressing constrained cases
5. **Cases** (الحالات): Concrete applications
6. **Residuals** (البقايا): What the rules did not cover
7. **Revision** (المراجعة): Rule modification when residuals appear

### Anti-Pattern

**INCORRECT progression** (leads to inflation):

```text
مفهوم جديد     (New concept)
    ↓
طبقة جديدة     (New layer)
    ↓
Gate جديدة     (New gate)
    ↓
PR جديد        (New PR)
    ↓
تضخم           (Inflation)
```

---

## 3. الصياغة الرياضية | Mathematical Formulation

Every domain can be represented as:

```
DomainAlgebra D = ⟨ CoreIdea, Method, GeneralRules, SpecificRules, Cases, Residuals, Revision ⟩
```

Where:
- **CoreIdea**: The supreme intellectual rule
- **Method**: Domain methodology
- **GeneralRules**: General governing rules
- **SpecificRules**: Specific governing rules
- **Cases**: Applications
- **Residuals**: Ungoverned remainders
- **Revision**: Rule modification process

### Progression Ladder

```
CoreIdea
    → Method
        → GeneralRule
            → SpecificRule
                → Case
                    → Residual
                        → Revision
```

This prevents explosion because any new addition must answer:

- Is it a **CoreIdea**?
- Or a **Method**?
- Or a **GeneralRule**?
- Or a **SpecificRule**?
- Or a **Case**?
- Or a **Residual**?
- Or a **Revision**?

If it falls in none of these positions, it is **ad-hoc** and **rejected**.

---

## 4. قاعدة الحد الأدنى الكافي | Minimal Sufficiency Rule

### English Formulation

**Minimal Sufficiency Rule:**

> A new construct is admissible **only if** no existing construct can represent the required distinction without losing:
> - **Trace**
> - **Rank**
> - **Residuals**
> - **NoLeap protection**

### Arabic Formulation

**قاعدة الحد الأدنى الكافي:**

> لا يقبل بناء جديد إذا كان البناء الموجود يكفي لتمثيل الفرق
> مع حفظ الأثر والرتبة والبقايا ومنع القفز.

### Implication

An addition is **not accepted** because it is "useful", but because it is **necessary**.

---

## 5. اختبار منع التضخم | Anti-Inflation Test

Before any new PR, the following must be answered:

### MinimalSufficiencyCheck Template

```yaml
MinimalSufficiencyCheck:
  new_construct: "<name of proposed construct>"

  why_needed:
    question: "What distinction can the current system NOT represent?"
    answer: "<specific answer>"

  existing_constructs_checked:
    - construct: "<existing construct name>"
      why_insufficient: "<specific reason>"
    - construct: "<another existing construct>"
      why_insufficient: "<specific reason>"

  smallest_possible_form:
    type:
      - case                # Simplest: just a case
      - specific_rule       # More general: specific rule
      - general_rule        # Even more general
      - method_extension    # Extends method
      - new_layer           # Most extreme: new layer
      - new_domain          # Most extreme: entire new domain

  does_it_prevent_forbidden_leap: true/false

  does_it_preserve_trace: true/false
  does_it_affect_rank_policy: true/false
  does_it_create_new_residual_type: true/false

  explosion_risk:
    level: low | medium | high
    justification: "<why this risk level>"

  decision:
    outcome: admit | reduce_to_case | reduce_to_specific_rule | merge_with_existing | reject
    rationale: "<final rationale>"
```

---

## 6. أمثلة تطبيقية | Application Examples

### Example 1: Arabic Language Domain

**الفكرة الكلية (CoreIdea):**
> العربية نظام دال ومدلول ونسبة وإفادة.
> Arabic is a system of signifier, signified, predication, and statement.

**الطريقة (Method):**
> لا ننتقل من اللفظ إلى الحكم إلا عبر: الدال، المدلول اللفظي، الوضع، الدلالة، النسبة، الإفادة.
> We do not transition from utterance to judgment except through: signifier, linguistic signified, conventional assignment, signification, predication, statement.

**قاعدة عامة (GeneralRule):**
> لا دلالة بلا وضع.
> No signification without conventional assignment.

**قاعدة خاصة (SpecificRule):**
> لا مجاز بلا علاقة وقرينة.
> No metaphor without relation and contextual indicator.

**حالة (Case):**
> "رأيت أسدًا يخطب" - Does not carry the external animal meaning, but opens a possible metaphorical usage.

**بقايا (Residuals):**
> - Is the contextual indicator sufficient?
> - Does the context prove bravery?
> - Is the intended meaning certain or probable?

---

### Example 2: Prior Information Domain

**الفكرة الكلية (CoreIdea):**
> العقل لا يعمل بلا معلومات سابقة.
> The mind does not operate without prior information.

**الطريقة (Method):**
> لا تدخل معلومة سابقة إلا بمجال ومصدر ودليل ورتبة وبقايا.
> Prior information enters only with domain, source, evidence, rank, and residuals.

**قاعدة عامة (GeneralRule):**
> الرأي السابق لا يكون دليلًا.
> Prior opinion cannot be evidence.

**قاعدة خاصة (SpecificRule):**
> الانطباع الشخصي عن مراد النص لا يصلح PriorInformation.
> Personal impression about textual intent is not valid PriorInformation.

**حالة (Case):**
> "أظن أن المجتمع يعني كذا" - Does not enter as evidence.

**بقايا (Residuals):**
> - Is there a sociological definition?
> - Is the domain political, jurisprudential, or linguistic?

---

## 7. العلاقة بالطريقة العقلية | Relation to Rational Method

The **Rational Method** itself operates by this pattern:

```
أثر (Trace)
    → تمييز (Distinction)
        → ربط (Binding)
            → تصور (Conception)
                → نسبة (Predication)
                    → إفادة (Statement)
                        → حكم (Judgment)
```

**And it does NOT jump.**

The **General Algebra** must mirror this with the same discipline:

```
فكرة كلية (Core Idea)
    → طريقة (Method)
        → قاعدة عامة (General Rule)
            → قاعدة خاصة (Specific Rule)
                → حالة (Case)
                    → بقايا (Residuals)
                        → مراجعة (Revision)
```

---

## 8. البنية الكسيرية | Fractal Structure

This means:

**العقل فكرة وطريقة.**
**The mind is idea and method.**

**الجبر العام فكرة وطريقة.**
**The General Algebra is idea and method.**

**كل مجال داخل الجبر يجب أن يكون فكرة وطريقة.**
**Every domain within the Algebra must be idea and method.**

This creates a **methodological fractal** (not decorative):

At every level:
- **Idea** governs the subject
- **Method** governs the transition
- **Rules** govern repetition
- **Residuals** govern failure
- **Revision** prevents inflation

---

## 9. الاختبارات المطلوبة | Required Tests

Every PR proposing a new construct must pass:

### Test 1: Unnecessary Layer
**Scenario**: PR proposes new layer without proof of necessity
**Expected**: FAIL

### Test 2: Reducible to Case
**Scenario**: PR can be represented as a case but requests a layer
**Expected**: FAIL

### Test 3: General Rule When Specific Suffices
**Scenario**: PR adds general rule when specific rule suffices
**Expected**: FAIL

### Test 4: Minimal Complete Unit
**Scenario**: PR contains minimal complete unit with minimal sufficiency justification
**Expected**: PASS

---

## 10. القانون المختصر | The Concise Law

**لا أصل لما يكفيه فرع.**
**No foundation for what a branch suffices.**

**لا طبقة لما تكفيه قاعدة.**
**No layer for what a rule suffices.**

**لا قاعدة عامة لما تكفيه قاعدة خاصة.**
**No general rule for what a specific rule suffices.**

**لا قاعدة خاصة لما تكفيه حالة.**
**No specific rule for what a case suffices.**

**ولا حالة بلا أثر.**
**And no case without trace.**

---

## 11. السلطة الدستورية | Constitutional Authority

This constitution is **binding** on:

1. All new PRs
2. All architectural decisions
3. All domain extensions
4. All gate additions
5. All layer proposals

**Violation** of minimal sufficiency results in **PR rejection**.

---

## 12. الخلاصة النهائية | Final Summary

**الجبر العام ليس نظام تكاثر مفاهيم، بل نظام توليد مضبوط.**

**The General Algebra is not a concept proliferation system, but a disciplined generation system.**

Every domain begins with:
1. **Core Idea**
2. **Method**
3. **General Rules**
4. **Specific Rules**
5. **Cases**
6. **Residuals**
7. **Revision**

And at every level, only **minimal sufficiency** is accepted that:
- **Preserves trace**
- **Prevents leaps**
- **Determines rank**
- **Calculates residuals**
- **Does not inflate structure**

This is what saves the project from **explosion**.

---

**End of Constitution**

**تم بحمد الله**
