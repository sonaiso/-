# U₇-C Clause Surface Agreement Contract

## Executive Summary

**Domain**: U₇-C = ClauseSurfaceAgreementCarrier

**Purpose**: Protect clause-level surface agreement contracts before root extraction

**Architectural Position**:
```
U₇-A PreWeightContract
  ↓
U₇-B WordSurfaceGuard (protects markers within single words)
  ↓
U₇-C ClauseSurfaceAgreementContract (protects agreements between words)
  ↓
U₈ RootStemCandidate
```

**Status**: ✅ **Phase 2 Complete** (Core structures implemented)

---

## Critical Architectural Separation: U₇-B vs U₇-C

### The Fundamental Question Difference

**U₇-B asks**: "ما العلامات داخل هذه الكلمة؟"
- What markers exist **within this word**?
- What prefixes/suffixes/infixes are protected?
- Is this word safe for U₈ root extraction?

**U₇-C asks**: "ما التعاقدات بين الكلمات؟"
- What agreements exist **between words**?
- Do adjectives agree with nouns?
- Do verbs agree with subjects?
- Is this broken plural rational or non-rational based on context?

### Why This Separation Is Constitutional

Some linguistic phenomena **cannot be understood at the word level**:

1. **Rationality (عاقلية)**: Only clear in agreement context
   - "الرجال صالحون" → rational (masculine plural agreement)
   - "الكتب كثيرة" → non-rational (feminine singular agreement with broken plural)

2. **Semantic vs. Real Feminine (تأنيث)**: Only clear in agreement context
   - "الشمس طلعت" → semantic feminine (no marker, but verb agrees)
   - "فاطمة جاءت" → real feminine (ة marker + agreement)

3. **Broken Plural Agreement Behavior**: Only clear in clause
   - "رجال قليلون" → plural masculine agreement (rational)
   - "جبال عالية" → feminine singular agreement (non-rational)

4. **Subject-Verb Agreement**: Requires both words
   - "كتب الطالب" → verb-subject agreement
   - "كتبت الطالبة" → verb-subject-gender agreement

**Constitutional Law**:
```
علامة لا تُفهم إلا في تعاقد
A marker understood only through contract
```

---

## The Six Constitutional Axioms (القوانين الدستورية)

### Axiom 7C.1: العلامة لا تُفهم إلا في تعاقد
**Marker understood only in contract**

Single-word analysis insufficient for:
- Rationality determination
- Gender type discrimination
- Agreement behavior prediction

### Axiom 7C.2: التعاقد ≠ الإعراب
**Agreement ≠ i'rab judgment**

U₇-C observes agreement patterns.
U₇-C does NOT assign final i'rab.

```
ALLOWED: number_agreement_hint = POSSIBLE
FORBIDDEN: final_irab = NOMINATIVE
```

### Axiom 7C.3: التعاقد ≠ الوظيفة
**Agreement ≠ function assignment**

U₇-C observes surface contracts.
U₇-C does NOT assign grammatical functions.

```
ALLOWED: agreement_edge_type = VERB_SUBJECT
FORBIDDEN: this_is_fa3il = TRUE
```

### Axiom 7C.4: الحافة السطحية ≠ الحكم النحوي
**Surface edge ≠ grammatical judgment**

Agreement edges are observations, not syntactic relations.

```
AgreementSurfaceEdge ≠ SyntacticRelation
AgreementSurfaceCandidate ≠ SyntacticFunction
```

### Axiom 7C.5: لا حكم قبل العلاقات
**No judgment before relations**

Grammatical functions require full relational analysis.
U₇-C only opens potential paths.

### Axiom 7C.6: جمع التكسير يحتاج عقدًا متعدد الأبعاد
**Broken plural needs multi-dimensional contract**

Broken plurals require 10+ dimensional analysis before root extraction.

---

## Core Data Structures

### 1. ClauseSurfaceAgreementUnit

**Purpose**: Represents one word with clause-level agreement information

**Key Fields**:
```python
surface: str                          # Original surface
protected_core: str                   # From U₇-B
root_input: str                       # From U₇-B
root_input_permission: RootInputPermission  # May be elevated by U₇-C

broken_plural_guard: Optional[BrokenPluralGuardNode]
transitivity_potential: Optional[TransitivitySurfacePotential]
weak_radical_risk_vector: Optional[WeakRadicalRiskVector]

agreement_edges: Tuple[str, ...]      # UIDs of edges involving this unit
rationality_surface_hint: RationalityHint
gender_surface_hint: GenderSurfaceHint
number_surface_hint: NumberSurfaceHint

permission_elevated_by_agreement: bool
permission_elevation_evidence: Optional[str]
```

**Forbidden Fields** (Constitutional Prohibition):
- `root`, `stem`, `weight`, `pattern` (U₈/U₉)
- `meaning`, `dalalah`, `ifadah` (U₁₅)
- `hukm`, `final_irab` (U₇+)
- `fa3il`, `maf3ul`, `mubtada`, `khabar` (syntactic analysis)

### 2. BrokenPluralGuardNode (Multi-Dimensional)

**Purpose**: Comprehensive protection for broken plurals before U₈

**10+ Dimensions**:

1. **Pattern Dimension**: `broken_pattern_hint` (فِعَال, فُعُول, مَفَاعِل)
2. **Singular Recovery**: `singular_candidate_path`, `singular_requires_lexicon`
3. **Derivational Status**: `singular_jamid_potential`, `singular_mushtaq_potential`
4. **Ontic Type**: `entity_noun_potential`, `adjective_potential`
5. **Adjective Source**: `adjective_source_hint` (اسم فاعل، صفة مشبهة)
6. **Gender Contracts**:
   - `gender_surface_hint`
   - `real_feminine_hint`
   - `semantic_feminine_hint`
   - `grammatical_feminine_agreement_hint`
7. **Rationality**: `rationality_surface_hint`
8. **Agreement Behavior**: `agreement_edges`
9. **Transitivity Path**: `transitivity_path_hint`
10. **Root Weakness**: `weak_radical_risk`
11. **Lexical Evidence**: `lexical_attestation_required`
12. **Permission**: `root_input_permission` (usually DEFERRED)

**Example: رجال**
```python
BrokenPluralGuardNode(
    surface="رجال",
    broken_pattern_hint="فِعَال",
    singular_candidate_path="رجل",
    singular_requires_lexicon=True,
    rationality_surface_hint=HUMAN_POSSIBLE,
    gender_surface_hint=MASCULINE_POSSIBLE,
    entity_noun_potential=POSSIBLE,
    root_input_permission=DEFERRED,
    residuals={"singular_not_certified"}
)
```

### 3. AgreementSurfaceEdge

**Purpose**: Represents agreement observation between two words

**Types**:
- `NOUN_ADJECTIVE`: اسم - صفة
- `VERB_SUBJECT`: فعل - فاعل
- `MUBTADA_KHABAR`: مبتدأ - خبر
- `NA3T_MAN3UT`: نعت - منعوت
- `BROKEN_PLURAL_ADJECTIVE`: جمع تكسير - صفة

**Key Fields**:
```python
source_unit_id: str                   # First word
target_unit_id: str                   # Second word
number_agreement_hint: AgreementHint
gender_agreement_hint: AgreementHint
rationality_agreement_hint: AgreementHint
broken_plural_feminine_singular_hint: MarkerHint
non_rational_plural_feminine_agreement_hint: MarkerHint
```

**Example: الكتب ↔ كثيرة**
```python
AgreementSurfaceEdge(
    edge_type=BROKEN_PLURAL_ADJECTIVE,
    source_unit_id="kutub_unit",       # الكتب
    target_unit_id="kathira_unit",     # كثيرة
    number_agreement_hint=POSSIBLE,
    gender_agreement_hint=POSSIBLE,
    broken_plural_feminine_singular_hint=POSSIBLE,
    non_rational_plural_feminine_agreement_hint=POSSIBLE
)
```

### 4. AgreementSurfaceCandidate

**Purpose**: Potential agreement pattern with evidence

**Key Fields**:
```python
agreement_edge: AgreementSurfaceEdge
number_evidence: Optional[str]
gender_evidence: Optional[str]
rationality_evidence: Optional[str]
elevates_permission: bool              # Does this elevate DEFERRED?
confirms_permission: bool              # Does this confirm ALLOWED?
```

### 5. TransitivitySurfacePotential

**Purpose**: Surface hints about verb transitivity (NOT judgment)

**Fields**:
```python
intransitive_path_hint: MarkerHint
transitive_one_object_hint: MarkerHint
transitive_two_objects_hint: MarkerHint
prepositional_object_hint: MarkerHint
passive_blocks_agent_hint: MarkerHint
```

**Example: نعبد**
```python
TransitivitySurfacePotential(
    surface_word="نعبد",
    transitive_one_object_hint=POSSIBLE,
    intransitive_path_hint=UNLIKELY
)
```

### 6. WeakRadicalRiskVector

**Purpose**: Warn U₈ about potential root weakness

**Fields**:
```python
initial_weak_risk: MarkerHint          # فاء معتلة
medial_weak_risk: MarkerHint           # عين معتلة
final_weak_risk: MarkerHint            # لام معتلة
hamzated_risk: MarkerHint
doubled_risk: MarkerHint
hollow_surface_risk: MarkerHint
defective_surface_risk: MarkerHint
```

**Example: قال**
```python
WeakRadicalRiskVector(
    surface_word="قال",
    medial_weak_risk=POSSIBLE,
    hollow_surface_risk=POSSIBLE
)
```

---

## Permission Elevation Logic

### U₇-C Permission Effects

**Elevation**: DEFERRED → ALLOWED (with evidence)
```
رجال (DEFERRED in U₇-B)
  + agreement with صالحون
  → rationality_hint = HUMAN_POSSIBLE
  → May elevate permission (with lexical support)
```

**Confirmation**: ALLOWED → ALLOWED (with evidence)
```
كتاب (ALLOWED in U₇-B)
  + agreement with جميل
  → gender/number confirmed
  → Permission confirmed
```

**Demotion**: Not performed by U₇-C
- U₇-C never demotes permissions
- Only elevates or confirms with evidence

---

## The Five Types of Feminine (أنواع التأنيث الخمسة)

### 1. Real Feminine (تأنيث حقيقي)
**Marker**: ة/ات
**Example**: فاطمة، طالبات
**Detection**: Surface marker present

### 2. Semantic Feminine (تأنيث معنوي)
**Marker**: None (semantic only)
**Example**: الشمس، الأرض
**Detection**: Agreement with no surface marker

### 3. Grammatical Feminine (تأنيث نحوي)
**Marker**: Agreement-based
**Example**: Based on context and agreement
**Detection**: Agreement pattern observation

### 4. Broken Plural Feminine Agreement (جمع تكسير يعامل معاملة مفرد مؤنث)
**Pattern**: Non-rational broken plural + feminine singular adjective
**Example**: الكتب كثيرة
**Detection**: Edge between broken plural and feminine singular

### 5. Non-Rational Plural Feminine (غير عاقل جمع يعامل معاملة مفرد مؤنث)
**Pattern**: Non-rational plural treats as feminine singular
**Example**: الجبال عالية
**Detection**: Agreement behavior in clause

---

## Golden Rules (القواعد الذهبية)

### 1. No Root from Marker
```
لا نأكل العلامة داخل الجذر
We do not consume the marker within root
```

### 2. No Contract from Word
```
لا نأكل التعاقد داخل الكلمة
We do not consume the contract within word
```

### 3. No Function from Weight
```
لا نأكل الوظيفة داخل الوزن
We do not consume the function within weight
```

### 4. No Meaning from I'rab
```
لا نأكل المعنى داخل الإعراب
We do not consume the meaning within i'rab
```

### 5. No Judgment Before Preservation
```
لا حكم قبل حفظ الهوية والأثر والبقايا
No judgment before preserving identity, trace, and residuals
```

---

## Example Analysis: الكتب كثيرة

### U₇-B Analysis (Word-Level)

**Word 1: الكتب**
```
surface = "الكتب"
protected_prefix = "الـ"
protected_core = "كتب"
root_input = "كتب"
root_input_permission = DEFERRED
broken_plural_surface_hint = POSSIBLE
broken_plural_pattern_hint = "فُعُل"
```

**Word 2: كثيرة**
```
surface = "كثيرة"
protected_suffix = "ة"
protected_core = "كثير"
root_input = "كثير"
root_input_permission = ALLOWED
gender_marker_hint = POSSIBLE (feminine ة)
```

### U₇-C Analysis (Clause-Level)

**Agreement Edge Detection**:
```python
AgreementSurfaceEdge(
    edge_type=BROKEN_PLURAL_ADJECTIVE,
    source_unit_id="kutub_unit",       # الكتب
    target_unit_id="kathira_unit",     # كثيرة
    number_agreement_hint=POSSIBLE,    # Plural/singular pattern
    gender_agreement_hint=POSSIBLE,    # Feminine agreement
    broken_plural_feminine_singular_hint=POSSIBLE,
    non_rational_plural_feminine_agreement_hint=POSSIBLE
)
```

**Rationality Inference**:
```
الكتب + كثيرة (feminine singular)
→ rationality_surface_hint = NON_RATIONAL_POSSIBLE
→ Agreement strengthens non-rational hypothesis
```

**Permission Effect**:
```
الكتب: DEFERRED (no elevation yet)
  → Needs lexical evidence: كتب ← كتاب
  → Singular path candidate opened
  → Full licensing deferred to lexicon
```

**BrokenPluralGuardNode Created**:
```python
BrokenPluralGuardNode(
    surface="الكتب",
    broken_pattern_hint="فُعُل",
    singular_candidate_path="كتاب",
    singular_requires_lexicon=True,
    rationality_surface_hint=NON_RATIONAL_POSSIBLE,
    gender_surface_hint=MASCULINE_POSSIBLE,
    grammatical_feminine_agreement_hint=POSSIBLE,
    root_input_permission=DEFERRED,
    residuals={"singular_not_certified", "lexicon_required"}
)
```

---

## What U₇-C Does NOT Do

### ❌ Does NOT Extract Roots
```
FORBIDDEN: root = "كتب"
ALLOWED:   root_input = "كتب" (licensed input only)
```

### ❌ Does NOT Assign Grammatical Functions
```
FORBIDDEN: this_is_mubtada = True
ALLOWED:   agreement_edge_type = MUBTADA_KHABAR
```

### ❌ Does NOT Perform Final I'rab
```
FORBIDDEN: final_irab = NOMINATIVE
ALLOWED:   nominative_surface_hint = POSSIBLE
```

### ❌ Does NOT Resolve Semantic Ambiguity
```
FORBIDDEN: meaning = "books"
ALLOWED:   rationality_surface_hint = NON_RATIONAL_POSSIBLE
```

### ❌ Does NOT Certify References
```
FORBIDDEN: resolved_reference = entity_123
ALLOWED:   agreement_edge with evidence
```

---

## Implementation Phases

### ✅ Phase 1: Execution Layer Registry (Complete)
- Added U₇-C to ExecutionLayer enum
- Updated transition chain: U₇-B → U₇-C → U₈

### ✅ Phase 2: Core Structures (Complete)
- ClauseSurfaceAgreementUnit
- BrokenPluralGuardNode (10+ dimensions)
- AgreementSurfaceEdge
- TransitivitySurfacePotential
- WeakRadicalRiskVector
- Basic U₇-B → U₇-C transition

### ⏸ Phase 3: BrokenPluralGuard Logic (Next)
- Implement pattern detection
- Implement singular candidate path
- Implement lexical requirement checks
- Implement multi-dimensional analysis

### ⏸ Phase 4: Agreement Detection (Future)
- Noun-adjective agreement
- Verb-subject agreement
- Broken plural feminine singular
- Mubtada-khabar patterns

### ⏸ Phase 5: Surface Potential Hints (Future)
- Transitivity detection
- Weak radical risk detection
- Adjective source hints

---

## Testing Strategy

### Constitutional Law Tests
- Forbidden fields validation (Axioms 7C.1-7C.6)
- Agreement ≠ i'rab verification
- Agreement ≠ function verification

### Structure Tests
- ClauseSurfaceAgreementUnit creation
- BrokenPluralGuardNode multi-dimensional
- AgreementSurfaceEdge validation
- Layer object edge reference validation

### Transition Tests
- U₇-B → U₇-C basic transition
- Permission preservation (ALLOWED, DEFERRED)
- Trace preservation
- Residual propagation

### Agreement Detection Tests (Future)
- Noun-adjective patterns
- Verb-subject patterns
- Broken plural patterns
- Permission elevation logic

---

## Integration with Pipeline

### Input: U₇-B Layer
```python
InflectionalSurfaceContractLayerObject(
    units=(unit1, unit2, ...),
    # Word-level marker protection complete
)
```

### Transition: U₇-B → U₇-C
```python
u7c_layer = transition_u7b_to_u7c(u7b_layer)
```

### Output: U₇-C Layer
```python
ClauseSurfaceAgreementLayerObject(
    units=(u7c_unit1, u7c_unit2, ...),
    agreement_edges=(edge1, edge2, ...),
    agreement_candidates=(candidate1, ...),
    broken_plural_guards=(guard1, guard2, ...),
    # Clause-level agreement protection complete
)
```

### To U₈: Licensed Root Input Only
```
U₈ receives:
  - root_input (only if permission = ALLOWED)
  - DEFERRED items blocked
  - Agreement evidence preserved in residuals
```

---

## Architectural Guarantees

### 1. No Premature Root Extraction
```
U₈ cannot see surface directly
U₈ cannot see protected_core directly
U₈ only sees root_input if permission = ALLOWED
```

### 2. No Lost Agreement Information
```
All agreement edges preserved
All rationality hints preserved
All gender contracts preserved
```

### 3. No Function Assignment Leakage
```
No fa3il, maf3ul, mubtada, khabar fields
Only surface agreement observations
Only hint-level information
```

### 4. Full Traceability
```
Every unit traces to U₇-B
Every edge references valid units
Every permission elevation has evidence
```

---

## CPB Identity Guardian

**Role**: Constitutional Law Enforcer

**Verifies**:
1. No forbidden fields in U₇-C units
2. No premature grammatical judgments
3. Agreement edges reference valid units
4. Permission elevations have evidence
5. Trace preservation from U₇-B
6. Residual propagation

**Enforced By**: `__post_init__()` validation in all dataclasses

---

## Summary

U₇-C introduces **clause-level protection** to complement U₇-B's **word-level protection**.

**Key Principle**: Some markers can only be understood in the context of multi-word agreements.

**Constitutional Separation**: Agreement observation ≠ Grammatical judgment

**Next Step**: Implement agreement detection functions (Phase 4) to populate edges and elevate permissions based on evidence.

---

**PR**: U7C-CLAUSE-SURFACE-AGREEMENT
**Created**: 2026-05-26
**Status**: Phase 2 Complete ✅
