# Broken Plural Surface Guard Architecture

## Executive Summary

**Architectural Principle**: Broken plurals (جمع التكسير) must be elevated from a "morphological pattern" to a **comprehensive protection node** before U₈, because they combine multiple linguistic dimensions that cannot be safely reduced to simple root extraction.

**Core Problem**: Unlike sound plurals (جمع سالم) which preserve a clear core through suffixation, broken plurals involve **internal vowel transformation** that can obscure the relationship between singular and root.

---

## The Governing Law: BrokenPluralSurfaceGuard Law

```
لا يُسمح لجمع التكسير أن يدخل U₈ كمدخل جذر خام
إلا إذا رُخّص مساره عبر عقد حماية تكشف:

Broken plurals SHALL NOT enter U₈ as raw root_input
unless their path is licensed through protection nodes that reveal:

- Is it a broken plural or ambiguous surface?
- What is the probable singular?
- Is the singular jāmid (frozen) or mushtaq (derived)?
- Is it a concrete noun (اسم ذات) or quality/adjective (صفة)?
- Does it carry biological, grammatical, or semantic gender?
- Is it rational (عاقل) or non-rational (غير عاقل)?
- Does it require lexical attestation?
- Does the underlying verb path affect derivation (transitive/intransitive)?
- Is the root sound or weak (معتل الفاء/العين/اللام)?
```

---

## Why Broken Plurals Are More Dangerous Than Sound Plurals

### Sound Plurals: Clear Core Preservation

Sound plurals generally maintain an obvious core:

```
مسلمون → مسلم + ون
مسلمين → مسلم + ين
مسلمات → مسلم + ات
```

Protection is relatively straightforward:
```python
surface = "مسلمون"
protected_suffix = "ون"
root_input = "مسلم"
```

### Broken Plurals: Internal Transformation

Broken plurals involve internal structural breaking:

```
رجل → رجال
كتاب → كتب
مدرسة → مدارس
قلم → أقلام
نفس → نفوس
```

**There is no simple suffix removal**. Internal breaking occurs:

```
رجل ≠ رجال (by mere suffix removal)
مدرسة ≠ مدارس (by mere suffix removal)
كتاب ≠ كتب (by mere suffix removal)
```

**Therefore**:
```
broken_plural_surface ≠ safe_root_input
```

---

## The Proposed Algebraic Representation

### BrokenPluralGuard Structure

```python
BrokenPluralGuard = (
    Surface
    + PatternHint
    + SingularCandidate
    + OnticTypePotential          # Entity vs. Quality
    + GenderContractPotential
    + RationalityPotential
    + DerivationalStatusPotential  # Jāmid vs. Mushtaq
    + RootWeaknessPotential
    + TransitivityPotential
    + LexicalEvidenceRequirement
    + Residuals
)
```

### Licensing Logic

```python
if broken_plural_surface_hint in {POSSIBLE, AMBIGUOUS}:
    root_input_permission = DEFERRED
    root_input = ""
    residual += "broken_plural_requires_singular_resolution"
```

---

## Linking Broken Plurals to Jāmid vs. Mushtaq

**We must NOT directly ask**: "What is the root of this broken plural?"

**Instead, we ask**: "Is the probable singular jāmid or mushtaq?"

### 1. Jāmid (Frozen) Singular

Examples:
```
رجل → رجال (man → men)
جبل → جبال (mountain → mountains)
نهر → أنهار (river → rivers)
بيت → بيوت (house → houses)
```

The singular denotes an entity/being, not an obvious derived event.

```python
singular_candidate = "رجل"
derivational_status = "jamid_possible"
entity_type = "ذات"  # concrete entity
root_path_permission = "deferred_or_possible_with_lexicon"
weight_path_permission = "deferred"
```

### 2. Mushtaq (Derived) Singular

Examples:
```
كاتب → كتّاب (writer → writers)
عامل → عمّال (worker → workers)
قائم → قوّام (standing/upright → those standing)
```

The plural may relate to an adjective, active participle (اسم فاعل), or intensive form (صيغة مبالغة).

```python
singular_candidate = "كاتب"
derivational_status = "mushtaq_possible"
adjective_or_agentive_surface = "possible"
root_path_permission = "possible_after_singular_resolution"
weight_path_permission = "possible_after_U8"
```

### 3. Adjective/Quality Singular

Examples:
```
كريم → كرام (generous → generous ones)
طويل → طوال (tall → tall ones)
أحمر → حمر (red → red ones)
أعمى → عميان (blind → blind ones)
```

Broken plural from adjective carries gender, number, and special grammatical agreement.

```python
surface = "كرام"
singular_candidate = "كريم"
quality_source = "صفة مشبهة / وصف"  # descriptive adjective
adjective_type = "وصف ذاتي محتمل"  # intrinsic quality possible
gender_contract = "unresolved"
rationality = "context_required"
```

### 4. Concrete Noun (اسم ذات) Singular

Examples:
```
كتاب → كتب (book → books)
قلم → أقلام (pen → pens)
مدرسة → مدارس (school → schools)
```

The plural is not a quality, but a collection of entities.

```python
entity_type = "اسم ذات"
quality_source = "none"
root_path = "deferred_until_singular"
```

---

## Linking to Gender and Its Types

Broken plurals don't have a single consistent agreement pattern. Sometimes treated as feminine singular non-rational, sometimes by rational agreement, sometimes context-dependent.

**We must separate**:

```python
biological_gender      # Biological sex
grammatical_gender     # Surface grammatical markers
semantic_gender        # Meaning-based gender
agreement_gender       # Agreement in context
rationality           # Rational vs. non-rational
species_type          # Human, animal, object
type_branch           # Subcategories
```

### Examples

**رجال (men)**:
```python
singular_candidate = "رجل"
rationality = "human_possible"
gender_semantic = "masculine_possible"
agreement_contract = "plural_human_possible"
root_input = "deferred until singular confirmed"
```

**كتب (books)**:
```python
singular_candidate = "كتاب"
rationality = "non_rational_possible"
agreement_contract = "feminine_singular_agreement_possible"
gender_semantic = "unresolved"
```

**مدارس (schools)**:
```python
singular_candidate = "مدرسة"
gender_surface = "feminine_singular_origin_possible"
plural_type = "broken_plural_possible"
agreement_contract = "non_rational_plural_as_feminine_singular_possible"
```

### Clause-Level Verification

Agreement is not resolved within the word alone, but in the clause:

```
الكتبُ مفيدةٌ
(The books [are] useful)
```

Non-rational broken plural takes feminine singular agreement:
```python
كتب → non_rational_broken_plural
مفيدة → feminine_singular_agreement
```

**This confirms the need for U₇-C ClauseSurfacePatternContract later.**

---

## Quality Source and Quality Type

If a broken plural comes from an adjective, it must open paths without resolving them:

```
Adjective types to consider:
- صفة مشبهة (descriptive adjective)
- اسم فاعل (active participle)
- اسم مفعول (passive participle)
- صيغة مبالغة (intensive form)
- صفة لون/عيب (color/defect adjective)
- نسبة (relative adjective)
```

### Examples

```
كريم → كرام (generous)
كاتب → كتّاب (writer/writing)
قتيل → قتلى (killed/slain)
أحمر → حمر (red)
أعمى → عميان (blind)
```

**In U₇-B, we do NOT say**: "This is definitely a descriptive adjective."

**Instead**:
```python
quality_surface_hint = "possible"
quality_source_hint = "adjective_like_surface"
adjective_type_hint = "unresolved"
requires_lexical_evidence = True
```

---

## Linking to Transitivity and Verb Origin

**Important but must NOT be resolved in U₇-B.** Should be opened as residual path.

**Why?** Because broken plurals may come from:
- Active participle from intransitive verb
- Active participle from transitive verb
- Passive participle
- Descriptive adjective
- Frozen concrete noun

### Examples

**قائم → قوّام (standing/upright)**

May relate to intransitive verb:
```python
قام → intransitive
```

**كاتب → كتّاب (writer)**

Relates to transitive verb generally:
```python
كتب الشيءَ → transitive
```

**قتيل → قتلى (slain/killed)**

Relates to passive:
```python
قُتِلَ → passive / patient
```

**In U₇-B**:
```python
transitivity_surface_hint = "unresolved"
verb_origin_path_hint = "possible"
agentive_path_hint = "possible"
patient_path_hint = "possible"
requires_U8_U9_U5_later_evidence = True
```

**We do NOT say**:
- This is intransitive
- This is transitive
- This is passive

**Instead, we preserve the possibility**:
```python
transitivity_residual = "needs_root_and_derivational_source"
```

---

## Linking to Root Weakness

Broken plurals may hide root weakness:

```
قول → أقوال (sayings)
بيع → بيوع (sales)
باب → أبواب (doors)
سيد → سادة (masters)
قاضٍ → قضاة (judges)
```

Before U₈, we must NOT give raw `root_input` if the plural might hide a weak letter.

**Add**:
```python
weak_radical_surface_hint:
    fa_weak_possible        # First radical weak
    ayn_weak_possible       # Middle radical weak
    lam_weak_possible       # Final radical weak
    doubled_possible        # Doubled consonant
    hamzated_possible       # Contains hamza
    unresolved
```

### Examples

**أبواب (doors)**:
```python
singular_candidate = "باب"
ayn_or_lam_weak_possible = "unresolved"
root_input = "deferred"
```

**قضاة (judges)**:
```python
singular_candidate = "قاضٍ"
lam_weak_possible = "true_hint"
root_input = "deferred"
```

**بيوع (sales)**:
```python
singular_candidate = "بيع"
ayn_weak_possible = "possible"
root_input = "deferred"
```

### The Law

```
If broken plural may hide فاء/عين/لام weakness,
then no raw root_input before singular_candidate + weak_radical_hint.
```

---

## Representation via Spaces, Nodes, Vectors, and Edges

The broken plural model must be a **graph**, not a single rule.

### Nodes

```
SurfaceNode
BrokenPluralPatternNode
SingularCandidateNode
GenderContractNode
RationalityNode
EntityOrQualityNode
JamidMushtaqNode
TransitivityPotentialNode
WeakRadicalHintNode
LexicalEvidenceNode
RootInputGateNode
ResidualNode
```

### Edges

```
surface_has_pattern
pattern_suggests_singular
singular_has_derivational_status
singular_has_gender_contract
singular_has_rationality
singular_has_entity_or_quality_type
quality_requires_source
source_may_have_transitivity
surface_may_hide_weak_radical
all_require_lexical_evidence
evidence_permits_root_input
missing_evidence_defers_root_input
```

### Vector Representation

```python
BrokenPluralVector = [
    pattern_family,
    singular_confidence,
    jamid_mushtaq_axis,
    entity_quality_axis,
    gender_axis,
    rationality_axis,
    agreement_axis,
    transitivity_axis,
    weak_radical_axis,
    lexical_evidence_axis,
    residual_axis,
    root_permission_axis
]
```

### Decision Logic

```python
if lexical_evidence_axis insufficient:
    root_permission_axis = DEFERRED

if pattern_family ambiguous:
    residual += "broken_plural_pattern_ambiguous"

if singular_candidate missing:
    residual += "missing_singular_candidate"

if weak_radical_axis unresolved:
    residual += "weak_radical_unresolved"

if entity_quality_axis unresolved:
    residual += "entity_or_quality_unresolved"
```

---

## Proposed Structure Within U₇-B

```python
@dataclass(frozen=True)
class BrokenPluralSurfaceGuard:
    """
    Comprehensive protection node for broken plurals.

    Broken plurals are NOT simple markers - they are internal transformations
    that combine multiple linguistic dimensions requiring special handling.
    """

    # Surface and pattern
    surface: str
    broken_plural_surface_hint: MarkerHint
    broken_plural_pattern_hint: str
    singular_candidate_surface: str | None

    # Derivational status
    singular_derivational_status_hint: str
    # Values: "jamid_possible" | "mushtaq_possible" | "unresolved"

    # Entity vs. quality
    entity_or_quality_hint: str
    # Values: "entity_possible" | "quality_possible" | "ambiguous" | "unresolved"

    # Quality source (if quality)
    quality_source_hint: str
    # Values: "sifat_mushabbaha_possible" | "ism_faail_possible" |
    #         "ism_mafool_possible" | "none" | "unresolved"

    # Gender contract
    gender_contract_hint: str
    # Values: "masculine_possible" | "feminine_possible" |
    #         "feminine_singular_agreement_possible" | "unresolved"

    # Rationality
    rationality_hint: str
    # Values: "rational_possible" | "non_rational_possible" | "unresolved"

    # Transitivity origin (if derived from verb)
    transitivity_origin_hint: str
    # Values: "lazim_possible" | "mutaaddi_one_possible" |
    #         "mutaaddi_two_possible" | "patient_path_possible" | "unresolved"

    # Root weakness
    weak_radical_hint: str
    # Values: "fa_weak_possible" | "ayn_weak_possible" |
    #         "lam_weak_possible" | "sound_possible" | "unresolved"

    # Evidence and permission
    lexical_evidence_required: bool
    root_input_permission: RootInputPermission
    root_input: str
    residuals: Tuple[str, ...]
```

---

## Golden Examples

### Example 1: رجال (men)

```python
surface = "رجال"
broken_plural_pattern_hint = "فِعال"
singular_candidate = "رجل"
singular_derivational_status_hint = "jamid_possible"
entity_or_quality_hint = "entity_possible"
gender_contract_hint = "masculine_human_possible"
rationality_hint = "rational_possible"
root_input_permission = DEFERRED
root_input = ""
residuals = ["broken_plural_requires_singular_resolution"]
```

### Example 2: كتب (books or "he wrote")

```python
surface = "كتب"
broken_plural_pattern_hint = "فُعُل / فعل محتمل"
singular_candidate = "كتاب possible"
also_verb_surface_possible = True
entity_or_quality_hint = "ambiguous"
root_input_permission = DEFERRED
residuals = [
    "broken_plural_or_verb_ambiguous",
    "singular_candidate_unconfirmed"
]
```

### Example 3: مدارس (schools)

```python
surface = "مدارس"
broken_plural_pattern_hint = "مفاعل"
singular_candidate = "مدرسة / مدرس possible"
gender_contract_hint = "feminine_origin_possible"
entity_or_quality_hint = "entity_possible"
rationality_hint = "non_rational_possible"
root_input_permission = DEFERRED
residuals = [
    "broken_plural_requires_singular_resolution",
    "feminine_marker_hidden_in_singular_candidate"
]
```

### Example 4: كرام (generous ones)

```python
surface = "كرام"
broken_plural_pattern_hint = "فِعال"
singular_candidate = "كريم"
entity_or_quality_hint = "quality_possible"
quality_source_hint = "adjective_like_possible"
gender_contract_hint = "plural_agreement_context_required"
root_input_permission = DEFERRED
residuals = [
    "adjective_source_unresolved",
    "transitivity_not_applicable_or_unresolved"
]
```

### Example 5: قتلى (slain/killed ones)

```python
surface = "قتلى"
singular_candidate = "قتيل / قتيلة possible"
entity_or_quality_hint = "quality_or_patient_possible"
quality_source_hint = "ism_mafool_or_patient_adjective_possible"
transitivity_origin_hint = "patient_path_possible"
weak_radical_hint = "lam_weak_or_alif_terminal_possible"
root_input_permission = DEFERRED
residuals = [
    "patient_quality_possible",
    "singular_candidate_required"
]
```

---

## How U₈ Should Handle This

**U₈ must NOT see**:
```
رجال
مدارس
كتب
كرام
قتلى
```

**as `root_input` unless U₇-B says**:
```python
root_input_permission = ALLOWED
root_input = "..."
```

**Otherwise**:
```python
root_status = DEFERRED
root_candidates = ()
residuals += "blocked_by_broken_plural_guard"
```

**This prevents consuming markers and internal transformations.**

---

## Broken Plural Guard Checklist

Proposed addition to U₇-B checklist:

```
BrokenPluralGuard Checklist:

[ ] detect_broken_plural_surface_hint
[ ] detect_pattern_family_hint
[ ] require_singular_candidate
[ ] mark_jamid_or_mushtaq_potential
[ ] mark_entity_or_quality_potential
[ ] mark_quality_source_potential
[ ] mark_gender_contract_potential
[ ] mark_rationality_potential
[ ] mark_transitivity_origin_potential
[ ] mark_weak_radical_potential
[ ] require_lexical_evidence
[ ] block_raw_root_input
[ ] defer_when_ambiguous
[ ] preserve_all_residuals
```

---

## Final Formulation of Laws

### SurfaceGuard Law

```
Every surface carrying:
- a marker
- a plural
- a verbal noun (مصدر)
- a quality (صفة)
- a proper name (علم)
- a loanword (دخيل)
- or possible jāmid status

MUST pass through protection nodes before U₈.

Protection does not analyze.
Protection does not certify.
Protection does not extract root.
Protection prevents incorrect consumption of markers and transformations.
Protection preserves residuals.
And root extraction begins only from licensed root_input.
```

### BrokenPluralGuard Law

```
Broken plural is internal transformation, not just surface marker.
Therefore it SHALL NOT enter U₈ as raw root_input
until proven or likely or deferred:

- Its singular
- Its singular's type
- Its gender
- Its rationality
- Its quality or entity nature
- Its quality source
- Its transitivity possibility
- Its root weakness possibility

Broken plural must be a high-risk protection node within U₇-B,
not merely a pattern hint.

Because it is not just "plural" - it is a gateway where intersect:
type, gender, quality, jāmid, mushtaq, rational, non-rational,
verb, root weakness, and lexicon.
```

---

## Implementation Phases

### Phase 1 (Current - PR #107)

✅ Basic broken plural detection
✅ Pattern hints (فِعال، مَفاعِل، فُعُل)
✅ Deferral of root_input
✅ Basic residuals

### Phase 2 (Proposed - PR #108+)

**Add comprehensive BrokenPluralSurfaceGuard**:

1. **Singular candidate detection**
   - Pattern reversal heuristics
   - Multiple candidate support

2. **Jāmid vs. Mushtaq hints**
   - Entity vs. derived classification
   - Requires lexical evidence

3. **Entity vs. Quality hints**
   - Concrete noun detection
   - Adjectival surface hints

4. **Quality source hints** (if quality)
   - صفة مشبهة، اسم فاعل، اسم مفعول patterns
   - Intensive forms (صيغة مبالغة)

5. **Gender contract hints**
   - Biological/grammatical/semantic separation
   - Agreement pattern hints

6. **Rationality hints**
   - Human/non-human classification
   - Agreement implications

7. **Transitivity origin hints**
   - Verb origin path possibilities
   - Patient vs. agent hints

8. **Root weakness hints**
   - فاء/عين/لام weakness detection
   - Hamza/doubling patterns

### Phase 3 (Future - U₇-C)

**Clause-level verification**:
- Agreement resolution
- Context-dependent gender
- Multi-word broken plural constructs

---

## Architectural Position

**Current Position**: Broken plurals are detected in U₇-B but with minimal metadata.

**Target Position**: Broken plurals become **comprehensive protection nodes** with:
- Multi-dimensional hint system
- Singular candidate tracking
- Derivational status hints
- Quality/entity classification
- Gender/rationality/transitivity hints
- Root weakness detection
- Lexical evidence requirements
- Rich residual tracking

**Integration Point**: Within `InflectionalSurfaceContractUnit` or as separate `BrokenPluralSurfaceGuard` sub-structure.

---

## Summary

**Broken plurals are not simple inflectional markers** - they are **internal structural transformations** that combine:

1. Pattern transformation (vowel changes)
2. Singular-plural relationship
3. Derivational status (jāmid/mushtaq)
4. Entity vs. quality nature
5. Gender contracts
6. Rationality classification
7. Agreement patterns
8. Quality source types
9. Transitivity origins
10. Root weakness possibilities

**Therefore**, they require a **comprehensive protection guard** before U₈, not just a pattern hint.

This elevation from "morphological pattern" to "comprehensive protection node" is essential for preventing premature root extraction from surfaces that cannot be safely analyzed without multi-dimensional linguistic context.

---

**Document Version**: 1.0
**Date**: 2026-05-26
**Status**: Architectural Proposal
**Related**: U₇-B Phase 2 Enhancement
**Dependencies**: Current Phase 1 (PR #107)
