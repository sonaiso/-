# Atomic Algebra Boundary (𝔄₀)

**Created**: 2026-05-23
**Status**: ✅ **Architectural Specification**
**Authority**: Core principle governing all dal layers

---

## Executive Summary

**Critical Principle**:

```text
𝔄₀ does NOT extract entities or events directly.
It ONLY certifies that phonetic/diacritic/positional material
is valid for entry into higher analysis.
```

This document defines the **atomic algebra boundary** and the **no-jumping law** (قانون منع القفز).

---

## 1. The Governing Distinction

### Level Zero (𝔄₀)

```text
A₀ = C × V × P
```

Where:
```text
C = Phonetic/Graphemic Carrier
V = Diacritic Activation
P = Position
```

The algebra:
```text
𝔄₀ = (A₀, Ω₀, Rel₀, Ax₀)
```

**Output**:
```text
AtomicChain₀ = {
  status: licensed | rejected | incomplete,
  atoms: [(c, v, p)],
  trace,
  residuals,
  rank
}
```

**NOT OUTPUT**:
```text
❌ Root (جذر)
❌ Pattern (وزن)
❌ Meaning (معنى)
❌ Entity (كيان)
❌ Event (حدث)
```

### The Intended Level

```text
ArabicWordInquiry
```

This is NOT a single layer, but a **complete fulfillment wrapper** over multiple layers.

```text
ArabicWordInquiry(word, context) = {
  layer0_atomic_chain,
  layer1_syllables,
  layer2_path,
  layer3_pattern,
  layer4_transformations,
  layer5_terminal_state,
  layer6_syntax,
  layer7_reference,
  layer8_dalalah,
  layer9_ifadah,
  layer10_judgment,
  minimal_entity_event,
  residuals
}
```

---

## 2. The No-Jumping Law (قانون منع القفز)

The central axiom in Ax₀:

```text
No transition from A₀ to root
nor to pattern
nor to meaning
nor to judgment
except through a licensed intermediate layer.
```

### Forbidden Jumps

```text
❌ letter + vowel ⟶ meaning
❌ letter + vowel ⟶ root
❌ phonetic sequence ⟶ judgment
```

### Licensed Path

```text
A₀
⟶ licensed syllable
⟶ candidate lexical unit
⟶ PathType
⟶ Pattern
⟶ candidate meaning
⟶ candidate entity/event
⟶ rank + residuals
```

---

## 3. Proposed Ascent Layers

### Layer 0: Atomic Algebra

**Input**: Raw letters + vowels + positions

**Operation**: Form A₀ units

**Output**: `atomic_chain`

**Failure modes**:
- Missing vowel
- Unlicensed initial sukun
- Uninterpretable position
- Letter without activation

**Example atom structure**:
```python
Atom₀ = {
  carrier: "ك",
  haraka: "َ",
  position: "initial",
  role: unknown,  # NOT determined at this layer
  residuals: []
}
```

---

### Layer 1: Syllable Algebra

Takes atomic chain and produces syllables:

```text
CV, CVC, CVV, CVVC, ...
```

Example:
```text
كَتَبَ
= كَ / تَ / بَ
= CV / CV / CV
```

**Important**: Still NO judgment about root or verb. Only:
```text
syllable_chain = licensed
```

---

### Layer 2: PathType Algebra

Critical layer preventing major errors:

```text
Path classification:
- RootPath?
- StemPath?
- OperatorPath?
- PronounPath?
- DemonstrativePath?
- RelativePath?
- ProperNamePath?
- LoanPath?
- MabniPath?
- ResidualPath?
```

**Critical principle**:
```text
Not every Arabic word = root
```

Examples of non-root words:
```text
هذا، الذي، من، إلى، أنا، أنت، مكة، إبراهيم
```

These MUST NOT be pushed to RootPath without evidence.

---

### Layer 3: Pattern / Weight Algebra

If path allows pattern, transition to:

```text
pattern
```

But pattern is threefold:

```text
1. StemWeight (وزن الجامد)
2. DerivationWeight (وزن الاشتقاق)
3. TransformationWeight (وزن التحول)
```

Different geometries for:
- Frozen nouns (جامد)
- Derived forms (مشتق)
- Verbal transformations (تحويل فعلي)

---

### Layer 4: Entity / Event Extraction

**Only at this layer** do we reach:

```text
Entity and Event with minimal sufficiency
```

---

## 4. Minimal Entity Definition

```text
MinimalEntity =
A licensed linguistic unit that can be treated as
thing/self/subject/reference sufficient for entering
syntactic or referential relations.
```

**Examples**:
```text
رجل       ⟶ nominal entity
زيد       ⟶ proper name entity
هذا       ⟶ demonstrative/referential entity
أنا       ⟶ pronominal entity
الذي      ⟶ relative entity (requires antecedent)
كتاب      ⟶ frozen entity
كاتب      ⟶ derived entity carrying event of writing
```

**Proposed structure**:
```python
MinimalEntity = {
  exists: bool,
  entity_type: EntityType,  # lexical | proper_name | pronoun |
                            # demonstrative | relative |
                            # operator_bound | inferred
  carrier: str,
  reference_status: ReferenceStatus,  # direct | contextual |
                                      # unresolved | elliptic
  evidence: Evidence,
  residuals: list[Residual],
  rank: float
}
```

---

## 5. Minimal Event Definition

```text
MinimalEvent =
A licensed linguistic unit carrying transformation,
occurrence, or predication capacity.
```

**Examples**:
```text
كَتَبَ     ⟶ explicit event
يكتب      ⟶ temporal/present event
اكتب      ⟶ imperative event
كتابة     ⟶ abstract event / masdar
كاتب      ⟶ derived entity embedding event
مكتوب     ⟶ patient entity embedding event
```

**Proposed structure**:
```python
MinimalEvent = {
  exists: bool,
  event_type: EventType,  # explicit_verb | abstract_masdar |
                         # derived_event | implied_event |
                         # no_word_level_event
  tense_aspect: TenseAspect,  # past | present | command |
                              # abstract | none
  voice: Voice,  # active | passive | none | unknown
  valency: Valency,  # transitive | intransitive | unknown
  role_projection: RoleProjection,  # agent | patient |
                                    # cause | result | none
  evidence: Evidence,
  residuals: list[Residual],
  rank: float
}
```

---

## 6. Frozen vs. Derived Relationship

**Licensed rule** (not absolute):

```text
Frozen → Entity (usually)
Verb → Event (usually)
Masdar → AbstractEvent (usually)
Derived → Entity + EmbeddedEvent (usually)
```

**Example**:
```text
كاتب =
  Entity: person/subject described
  Event: embedded writing event
  Role: agent (فاعل)
```

**Example**:
```text
كتاب =
  Entity: thing/written/knowledge container
  Event: not explicit (may be inferred historically/contextually)
```

---

## 7. Concise Operational Version

```text
ArabicWordInquiry(word, context):

1. Build A₀ atoms
2. License atomic chain through 𝔄₀
3. Build syllable chain
4. Classify PathType
5. Test Pattern / Weight if allowed
6. Detect transformations
7. Extract terminal state
8. Extract candidate entity
9. Extract candidate event
10. Attach evidence, rank, residuals
11. Stop before ifādah unless context provides relation
```

**Rationale**: A single word rarely provides complete ifādah.

```text
كتب ⟶ candidate event
```

But:
```text
زيد كتب ⟶ preliminary ifādah (attribution complete)
```

---

## 8. Final Rigorous Formulation

**English**:
```text
ArabicWordInquiry is NOT a direct semantic parser.

It is a licensed ascent system:

A₀ ⟶ Syllable ⟶ PathType ⟶ Pattern ⟶ Transformation
⟶ TerminalState ⟶ Entity/Event Candidate
⟶ Dalalah ⟶ Ifadah ⟶ Judgment

with every transition guarded by:
License, Evidence, Rank, Trace, Residuals.
```

**Arabic**:
```text
تحقيق الكلمة العربية هو صعود مرخّص من الحامل الذري
إلى المقطع، ثم المسار، ثم النمط، ثم التحول،
حتى استخراج الكيان والحدث بالحد الأدنى الكافي،
من غير قفز إلى الجذر أو الوزن أو الدلالة أو الحكم
إلا بدليل وبقايا ورتبة.
```

---

## 9. Operational Laws

```text
لا كيان بلا مسار.        No entity without path.
لا حدث بلا تحول.         No event without transformation.
لا دلالة بلا وضع.        No meaning without wadh.
لا إفادة بلا نسبة.       No ifadah without attribution.
لا حكم بلا دليل.         No judgment without evidence.
لا يقين بلا بقايا محسوبة. No certainty without computed residuals.
```

---

## 10. Immediate Objective

Not analyzing all of Arabic at once, but:

**Extract**:
```text
MinimalEntity + MinimalEvent
```

From a word or small construction, with:
```text
trace + residuals + rank
```

---

## Implementation Status

### ✅ Implemented (dal_core)

- `Carrier` (Contract 1): Unicode → Carrier
- `ArabicAtom` (Contract 2): Carrier → Atom
- Residual system
- Evidence system
- Rank system

**Files**:
- `src/dal_core/carriers.py`
- `src/dal_core/atoms.py`
- `src/dal_core/residuals.py`
- `src/dal_core/evidence.py`

### ⏳ Partially Implemented

- Syllable algebra (basic structure exists)
- PathType classification (needs expansion)

### 📋 Planned

- Pattern algebra (full threefold structure)
- Transformation detection
- MinimalEntity extraction
- MinimalEvent extraction
- Complete ArabicWordInquiry wrapper

---

## Forbidden Patterns (Anti-patterns)

### ❌ Direct Semantic Jump
```python
# WRONG
def analyze_word(word: str) -> Meaning:
    atoms = parse_atoms(word)
    return extract_meaning(atoms)  # FORBIDDEN JUMP
```

### ✅ Licensed Ascent
```python
# CORRECT
def analyze_word(word: str) -> ArabicWordInquiry:
    atoms = build_atoms(word)              # Layer 0
    syllables = build_syllables(atoms)     # Layer 1
    path = classify_path(syllables)        # Layer 2
    pattern = test_pattern(path)           # Layer 3
    transformations = detect_trans(pattern) # Layer 4
    entity = extract_entity(transformations)
    event = extract_event(transformations)
    return ArabicWordInquiry(
        atoms=atoms,
        syllables=syllables,
        path=path,
        pattern=pattern,
        entity=entity,
        event=event,
        residuals=collect_residuals()
    )
```

---

## References

- **PR #21**: Ordered Dal Form Governance
- **PR #22**: Project Algebra Architecture Map
- `docs/DAL_ALGEBRA_SIGNATURE.md`
- `docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md`
- `src/dal_core/carriers.py`
- `src/dal_core/atoms.py`

---

## Governance

**This document is normative** for all dal layers and Arabic word analysis.

**Violation of the no-jumping law is a blocker residual.**

**Updates require**: Architectural review and PR approval

---

**Document Version**: 1.0
**Author**: Architectural Specification Agent
**Status**: ✅ **Approved** (pending user review)
