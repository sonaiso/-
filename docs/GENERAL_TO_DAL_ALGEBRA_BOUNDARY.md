# General Algebra to Dal Algebra Boundary

**PR #22**: Positioning Dal Algebra as Pre-Semantic Specialization
**Status**: Governance documentation (no implementation)
**Created**: 2026-05-20

---

## Executive Summary

This document clarifies the **relationship between General Algebra and Dal Algebra**.

**Core positioning**:
> **Dal Algebra is a pre-semantic specialization concerned with ordered signifier form.**
> **It depends on the broader General Algebra but does not replace prior-information, candidate-madlul, or Wadhʿ layers.**

---

## What is Dal Algebra?

### Definition

**Dal Algebra** = A6 + A7 + A8 within the General Algebra hierarchy

```text
A6: Ordered Dal Form Algebra (structure governance)
A7: Dal-Mufrad Algebra (individual signifier analysis)
A8: Dal-Murakkab Algebra (composed signifier)
```

### Scope: Form, Not Meaning

**Dal Algebra is concerned with SIGNIFIER FORM**:
- ✅ Ordering (sequence, indices, direction)
- ✅ Boundaries (left, right, internal)
- ✅ Units (atoms, syllables, morphemes)
- ✅ Composition (fold, split, concatenate)
- ✅ Direction (forward, backward, bidirectional)
- ✅ Trace (derivation, reversibility)
- ✅ Morphological structure (root, pattern, affixes)
- ✅ Lexical identity (word closure)

**Dal Algebra explicitly excludes**:
- ❌ Meaning (that's A5: CandidateMadlul)
- ❌ Wadhʿ contracts (that's A9: Wadhʿ Algebra)
- ❌ Dalalah direction (that's A10: Dalalah Algebra)
- ❌ Usage classification (that's A11: Istiʿmal Algebra)
- ❌ Intended meaning (that's A12: Murad Algebra)
- ❌ Judgment/inference (that's A13: Hukm Algebra)

---

## Dal Algebra ⊂ General Algebra

### The Subset Relationship

**Claim**:
> **Dal Algebra ⊂ General Algebra**

**Important caveat**:
> **This is an architectural inclusion at this stage,**
> **not yet a formally proven mathematical subalgebra.**

### What "⊂" Means Here

#### ✅ Architectural Sense (Current Status)

**Dal Algebra uses General Algebra patterns**:
1. **Candidate generation**: Dal operations produce candidate sets, not unique answers
2. **Rank/Residual**: Dal candidates carry rank (confidence) and residuals (unexplained aspects)
3. **Trace preservation**: Dal operations preserve derivation traces for reversibility
4. **Evidence-scoped claims**: Dal claims reference span, boundaries, position
5. **Layer dependencies**: Dal respects General Algebra layer ordering

**Dal Algebra respects General Algebra laws**:
- Law 1: Layer dependency (no claiming later outputs)
- Law 2: No layer skipping
- Law 3: Evidence preservation
- Law 6: No Wadhʿ without structure

**Dal Algebra is positioned within General Algebra hierarchy**:
```text
General Algebra (A0)
├─ ... [A1-A5: Pre-Dal layers]
├─ Ordered Dal Form Algebra (A6) ← Dal Algebra starts here
├─ Dal-Mufrad Algebra (A7)
├─ Dal-Murakkab Algebra (A8)      ← Dal Algebra ends here
├─ ... [A9-A13: Post-Dal layers]
```

#### ❌ Mathematical Sense (Future Work)

**Not yet proven**:
- Formal subalgebra axioms
- Closure under operations
- Homomorphism properties
- Ideal/quotient structures
- Algebraic laws (associativity, commutativity where applicable)

**Future work**: Formal verification that Dal Algebra satisfies mathematical subalgebra axioms with respect to General Algebra.

---

## Dependency: Dal Algebra Requires Pre-Dal Layers

### Dal Algebra Does Not Start From Zero

**Critical principle**:
> **Dal Algebra assumes pre-existing foundations.**
> **It does not replace A1-A5.**

### Required Pre-Dal Layers

#### A1: Source-of-Effect Algebra
**Why required**:
- Dal forms originate from effects (sound, script, text...)
- Effects must be sourced (sensory, textual, reported...)
- Dal cannot be analyzed without knowing its source reality

**Example**: Analyzing written "كتاب" requires knowing it's **script** (A2) from **textual source** (A1).

#### A2: Effect Reception Algebra
**Why required**:
- Dal operates on **received effects**, not abstract symbols
- Different effects (sound vs script) require different analysis
- Effect normalization precedes Dal structuring

**Example**: Phonological Dal requires **sound effect**; graphemic Dal requires **script effect**.

#### A3: Prior-Information Algebra
**Why required**:
- Dal analysis uses **lexicon** (prior word forms)
- Dal pattern matching uses **rules** (morphological constraints)
- Dal candidate ranking uses **attestation** (corpus frequency)
- Dal classification uses **examples** (paradigmatic instances)

**Example**: Identifying "كَتَبَ" as فَعَلَ pattern requires **prior knowledge** of this template.

#### A4: Effect-Prior Binding Algebra
**Why required**:
- Dal units are **bound** to prior exemplars, not discovered in vacuum
- Morphological patterns are **matched** against prior templates
- Root extraction is **validated** against prior root inventory

**Example**: Extracting root ك-ت-ب from "كَتَبَ" requires **binding** surface form to prior root patterns.

#### A5: Candidate-Madlul Algebra
**Why required** (for semantic-adjacent tasks):
- While Dal Algebra avoids **claiming** Madlul, it may **reference** CandidateMadlul for disambiguation
- Example: Distinguishing homographs may require **candidate meanings** as context

**Important constraint**:
> **Dal Algebra may USE CandidateMadlul as input when provided**
> **but MUST NOT GENERATE or CLAIM CandidateMadlul as output.**

---

## Dal Algebra Position: Between Binding and Wadhʿ

### Before Dal: Effect-Prior Binding (A4)

```text
Effect (A2) × Prior (A3) → Binding (A4) → CandidateMadlul (A5)
                                              ↓
                                        OrderedDal (A6)
```

**Dal receives**:
- Effects that have been sourced (A1 → A2)
- Prior information that is available (A3)
- Optional: Binding candidates (A4)
- Optional: Madlul candidates (A5) for disambiguation

**Dal does not create**:
- Sources (A1 responsibility)
- Effects (A2 responsibility)
- Prior information (A3 responsibility)
- Bindings (A4 responsibility)
- Madlul candidates (A5 responsibility)

### After Dal: Wadhʿ Contract (A9)

```text
OrderedDal (A6/A7/A8) + CandidateMadlul (A5) → Wadhʿ Contract (A9)
```

**Dal provides** (to Wadhʿ layer):
- Structured signifier forms (OrderedDal)
- Morphological analysis
- Lexical identity (closed words)
- Composition structure

**Dal does not provide** (Wadhʿ layer responsibility):
- Dal-Madlul linking
- Wadhʿ evidence
- Wadhʿ type classification (lexical, technical, shar'i...)

---

## What Dal Algebra Provides to General Algebra

### Contributions

**Dal Algebra specializes General Algebra for linguistic signifier analysis**:

1. **Ordered representation** (A6):
   - Signifiers as ordered sequences, not bags of features
   - Boundary specification
   - Positional indexing
   - Directional analysis (forward/backward)

2. **Individual signifier closure** (A7):
   - Morphological analysis (root, pattern, affixes)
   - Syllabic structure
   - Lexical identity
   - Pre-syntax interface

3. **Composed signifier governance** (A8):
   - Multi-word composition
   - Boundary preservation across composition
   - Trace preservation for reversibility

### What Dal Algebra Does NOT Provide

**Dal Algebra does NOT handle**:
- Source identification (A1)
- Effect reception (A2)
- Prior information management (A3)
- Effect-prior binding (A4)
- Meaning formation (A5)
- Wadhʿ contracts (A9)
- Dalalah direction (A10)
- Usage classification (A11)
- Intended meaning inference (A12)
- Judgment/inference (A13)

---

## Forbidden Claims for Dal Algebra

### What Dal Algebra Must Not Claim

#### Claim 1: "Dal Algebra is the first algebra"
```text
❌ FORBIDDEN: Dal is the starting point
✅ CORRECT: Dal depends on A1-A5 (source, effect, prior, binding, madlul)
```

#### Claim 2: "Dal Algebra handles meaning"
```text
❌ FORBIDDEN: Dal creates or infers Madlul
✅ CORRECT: Dal may reference CandidateMadlul (A5) but does not generate it
```

#### Claim 3: "Dal Algebra establishes Wadhʿ"
```text
❌ FORBIDDEN: Dal determines Dal-Madlul correspondence
✅ CORRECT: Dal provides OrderedDal structure; Wadhʿ (A9) links it to Madlul
```

#### Claim 4: "Dal Algebra infers Murad"
```text
❌ FORBIDDEN: Dal determines intended meaning
✅ CORRECT: Dal provides structured forms; Murad (A12) infers intent from usage + context
```

#### Claim 5: "Dal Algebra is independent of prior information"
```text
❌ FORBIDDEN: Dal operates in vacuum
✅ CORRECT: Dal requires lexicon, rules, attestation (A3) and binding (A4)
```

---

## Allowed Claims for Dal Algebra

### What Dal Algebra Can Claim

#### Claim 1: "Dal Algebra analyzes signifier form"
```text
✅ ALLOWED: Dal structures, orders, bounds, and analyzes linguistic forms
```

#### Claim 2: "Dal Algebra performs morphological analysis"
```text
✅ ALLOWED: Dal extracts roots, patterns, affixes within structured forms
```

#### Claim 3: "Dal Algebra produces lexical identity"
```text
✅ ALLOWED: Dal closes individual signifiers (A7: MufradProof)
```

#### Claim 4: "Dal Algebra generates syntax candidates"
```text
✅ ALLOWED: Dal produces OperatorTrigger candidates (not syntax application)
```

#### Claim 5: "Dal Algebra uses prior information"
```text
✅ ALLOWED: Dal references lexicon, rules, attestation for analysis
```

#### Claim 6: "Dal Algebra preserves trace for reversibility"
```text
✅ ALLOWED: Dal fold operations maintain source trace for unfolding
```

---

## Examples: Dal Algebra Boundaries in Practice

### Example 1: Root Extraction

**Input**: "كَتَبَ" (surface form)

#### ✅ Dal Algebra Responsibility
```text
1. Structure as OrderedDal:
   - Sequence: [ك, َ, ت, َ, ب, َ]
   - Boundaries: (WORD_START, WORD_END)
   - Indices: [0, 1, 2, 3, 4, 5]

2. Extract root candidate:
   - Root: (ك, ت, ب)
   - Root type: TRILATERAL
   - Indices: [0, 2, 4]
   - Pattern: فَعَلَ
   - Evidence: "matches فَعَلَ template"
   - Rank: HIGH (exact template match)
   - Residuals: [] (no unexplained elements)

3. Close as MufradProof:
   - Morphology: root=(ك,ت,ب), pattern=فَعَلَ
   - Lexical identity: "كَتَبَ"
   - Boundaries: (0, 6)
```

#### ❌ Dal Algebra Must NOT Claim
```text
❌ Meaning: "he wrote" ← A5 (CandidateMadlul) + A9 (Wadhʿ)
❌ Dalalah: مطابقة (conformity) ← A10 (Dalalah)
❌ Usage: حقيقة (literal) ← A11 (Istiʿmal)
❌ Murad: "author's intent is..." ← A12 (Murad)
```

### Example 2: Homograph Disambiguation

**Input**: "عَلِمَ" (surface form)

#### ✅ Dal Algebra Responsibility
```text
1. Structure as OrderedDal:
   - Sequence: [ع, َ, ل, ِ, م, َ]
   - Boundaries: (WORD_START, WORD_END)

2. Extract root candidate:
   - Root: (ع, ل, م)
   - Pattern: فَعِلَ

3. Generate alternative candidates:
   Candidate 1:
     - Root: (ع, ل, م)
     - Pattern: فَعِلَ
     - Evidence: "matches فَعِلَ template"
     - Rank: 0.5

   Candidate 2:
     - Root: (ع, ل, م)
     - Pattern: فَعَلَ (with kasra)
     - Evidence: "rare فَعَلَ with kasra"
     - Rank: 0.3

   [Both candidates are FORM candidates, not MEANING candidates]

4. Close as MufradProof with competing candidates:
   - Morphology: root=(ع,ل,م), pattern={فَعِلَ|فَعَلَ}
   - Lexical identity: "عَلِمَ"
   - Residuals: "pattern ambiguity unresolved"
```

#### ❌ Dal Algebra Must NOT Claim
```text
❌ Meaning: "he knew" vs "flag/banner" ← A5 + A9
❌ Disambiguation: "context suggests knowledge sense" ← A11 + A12
❌ Murad: "speaker intends knowledge, not object" ← A12
```

#### ✅ Dal Algebra MAY Use (If Provided)
```text
✅ IF CandidateMadlul provided from A5 as input:
   - Use meaning candidates to rank form candidates
   - Example: "If context provides KNOWLEDGE madlul candidate,
              rank فَعِلَ pattern higher than فَعَلَ"

✅ BUT: Dal does not GENERATE these meaning candidates
```

### Example 3: Composed Signifier

**Input**: "كِتَابُ اللَّهِ" (phrase)

#### ✅ Dal Algebra Responsibility
```text
A7 (Dal-Mufrad):
  1. Close "كِتَابُ" as MufradProof:
     - Root: (ك, ت, ب)
     - Pattern: فِعَال
     - Boundaries: (0, 7)

  2. Close "اللَّهِ" as MufradProof:
     - Frozen form: الله
     - Type: PROPER_NOUN
     - Boundaries: (8, 14)

A8 (Dal-Murakkab):
  3. Compose into MurakkabCandidate:
     - Sequence: [MufradProof1, MufradProof2]
     - Indices: [0, 1]
     - Boundaries: (0, 14)
     - Composition type: IDAFA (structural, not syntactic)
     - Trace: [mufrad1=(0,7), mufrad2=(8,14)]

  4. Generate operator trigger candidates:
     - IDAFA_CONSTRUCTION trigger
     - First=mudaf, Second=mudaf_ilayh (positional, not case)
```

#### ❌ Dal Algebra Must NOT Claim
```text
❌ Meaning: "Book of Allah" ← A9 (Wadhʿ)
❌ Dalalah: مطابقة (both words signify full concepts) ← A10
❌ Usage: حقيقة or مجاز ← A11
❌ Murad: "Qur'an is intended" ← A12
❌ Syntax: "كِتَابُ is mudaf, اللَّهِ is mudaf_ilayh with jarr" ← Syntax layer (nahw operators)
```

#### ✅ Dal Algebra MAY Claim
```text
✅ Structure: "Two-unit composition with boundaries preserved"
✅ Trigger: "IDAFA_CONSTRUCTION trigger candidate"
✅ Position: "First unit at index 0, second at index 1"
✅ Trace: "Reversible to individual mufrad units"
```

---

## Integration Pattern: Dal Algebra Within General Algebra

### Information Flow

```text
[A1] Source-of-Effect
  ↓ (source type)
[A2] Effect Reception
  ↓ (effect pattern)
[A3] Prior Information ←──────┐ (lookup)
  ↓                           │
[A4] Effect-Prior Binding     │
  ↓ (binding candidates)      │
[A5] Candidate-Madlul         │
  ↓ (optional input)          │
┌─────────────────────────────┴──┐
│ [A6] Ordered Dal Form Algebra  │
│   ↓ (structured signifier)      │
│ [A7] Dal-Mufrad Algebra         │ ← Dal Algebra
│   ↓ (closed signifier)          │   specialization
│ [A8] Dal-Murakkab Algebra       │
└─────────────────────────────────┘
  ↓ (OrderedDal output)
[A9] Wadhʿ Contract (OrderedDal + CandidateMadlul + Evidence)
  ↓ (wadhʿ contract)
[A10] Dalalah
  ↓ (dalalah direction)
[A11] Istiʿmal
  ↓ (usage type + qarina)
[A12] Murad
  ↓ (intended meaning + context)
[A13] Hukm
  ↓ (judgment)
```

### Key Principles

1. **Dal receives** from A1-A5 (source, effect, prior, binding, optional madlul)
2. **Dal processes** form (order, boundaries, composition)
3. **Dal outputs** to A9 (OrderedDal for Wadhʿ linking)
4. **Dal does NOT bypass** A9-A13 to claim meaning/usage/murad/hukm

---

## Verification: Is Dal Algebra Respecting Boundaries?

### Checklist

To verify Dal Algebra compliance with General Algebra:

#### ✅ Required Properties

- [ ] Dal operations produce **candidate sets**, not unique answers
- [ ] Dal candidates carry **rank** (confidence) and **residuals**
- [ ] Dal operations preserve **trace** (derivation path)
- [ ] Dal claims are **evidence-scoped** (reference span, boundaries)
- [ ] Dal respects **layer dependencies** (uses A1-A5, outputs to A9)
- [ ] Dal does NOT skip layers (no A7 → A12 jumps)

#### ❌ Forbidden Properties

- [ ] Dal must NOT contain `meaning` field
- [ ] Dal must NOT contain `wadhʿ` field
- [ ] Dal must NOT contain `murad` field
- [ ] Dal must NOT contain `hukm` field
- [ ] Dal must NOT generate `CandidateMadlul` outputs
- [ ] Dal must NOT claim `Dalalah` direction
- [ ] Dal must NOT claim `Istiʿmal` usage type
- [ ] Dal must NOT infer `Murad` intent

### Example Verification: MufradProof

```python
# From src/dal_core/d_mufrad.py
@dataclass
class DClosed:
    """Closed lexical sign (Dal-Mufrad output)."""

    lemma: str
    morphology: DMorph
    boundaries: Tuple[int, int]

    # REQUIRED: Morphological fields
    ✅ root: Optional[Tuple[str, ...]]
    ✅ pattern: Optional[str]
    ✅ affixes: Optional[List[str]]

    # FORBIDDEN: Semantic fields
    ❌ meaning: ... # Must not exist
    ❌ wadhʿ: ...   # Must not exist
    ❌ murad: ...   # Must not exist
    ❌ haqiqa_majaz: ... # Must not exist
```

**Verification result**: ✅ `DClosed` respects Dal Algebra boundaries (no semantic fields)

---

## Conclusion

**Dal Algebra is correctly positioned** as:

1. **A pre-semantic specialization** (A6-A8) within General Algebra (A0)
2. **Dependent on pre-Dal layers** (A1-A5: source, effect, prior, binding, madlul)
3. **Providing to post-Dal layers** (A9: Wadhʿ receives OrderedDal)
4. **Concerned with FORM**, not MEANING
5. **Architecturally included** in General Algebra (formal proof pending)

**Dal Algebra does NOT replace**:
- Prior-information layer (A3)
- Effect-prior binding layer (A4)
- Candidate-madlul layer (A5)
- Wadhʿ contract layer (A9)
- Higher semantic/pragmatic layers (A10-A13)

**Dal Algebra correctly claims**:
- Ordered signifier structure
- Morphological analysis
- Lexical identity
- Syntax candidacy (not syntax application)

**Dal Algebra correctly avoids claiming**:
- Meaning generation
- Wadhʿ contracts
- Dalalah direction
- Usage classification
- Intended meaning
- Judgment/inference

---

**Status**: ✅ Documented (boundary specification)
**Related**:
- `docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md` (complete A0-A13 hierarchy)
- `docs/REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md` (A1-A6 pre-Wadhʿ layers)
- `docs/ORDERED_DAL_FORM_GOVERNANCE.md` (A6 governance, PR #21)
- `docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md` (A7-A8 scope clarification, this PR)
- `docs/SPEC_DAL_CORE.md` (A7 implementation specification)

