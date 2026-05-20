# Dal-Mufrad and Dal-Murakkab Position

**PR #22**: Clarifying A7-A8 Scope and Limitations
**Status**: Governance documentation (no implementation)
**Created**: 2026-05-20

---

## Executive Summary

This document clarifies the **scope and limitations** of Dal-Mufrad (A7) and Dal-Murakkab (A8) algebras.

**Core principle**:
> **Dal-Mufrad closes the ordered individual signifier.**
> **Dal-Murakkab composes already-closed signifiers.**
> **Neither creates CandidateMadlul.**
> **Neither creates Wadhʿ.**
> **Neither creates Dalalah.**
> **Neither infers Murad.**

---

## A7: Dal-Mufrad Algebra

### Definition

**Dal-Mufrad Algebra** governs the analysis and closure of **individual lexical signifiers** (words).

**Mufrad** (مفرد) = individual, singular, standalone linguistic unit

### Scope

**Dal-Mufrad is responsible for**:

1. **Internal morphological structure**:
   - Root extraction (جذر)
   - Pattern identification (وزن)
   - Affix segmentation (بادئة، لاحقة)
   - Template matching

2. **Syllabic structure**:
   - CV pattern analysis
   - Syllable boundaries
   - Phonotactic constraints

3. **Lexical identity**:
   - Word closure (DClosed)
   - Lemma determination
   - Frozen vs. derived classification

4. **Pre-syntactic interface**:
   - PreSyntaxMufradVector (syntax-ready representation)
   - Operator trigger candidacy (not operator application)
   - Case sign potential (not case effect)

5. **Ordered dal form** (from A6):
   - Sequence: [atom₀, atom₁, ..., atomₙ]
   - Boundaries: (left_boundary, right_boundary)
   - Indices: position of each atom
   - Direction: forward/backward analysis
   - Trace: derivation path

### Dal-Mufrad Contracts (dal_core Implementation)

**Contract 1: Carrier** (Unicode/UTF-8 representation)
```text
Unicode → UTF-8 bytes
Reversible encoding
```

**Contract 2: Atom** (Letters + diacritics)
```text
Raw input → ArabicAtom (letter + haraka)
Boundary: Individual letter representation
```

**Contract 3: Unit** (Syllables)
```text
[Atom] → [Syllable]
CV pattern: C, V, CV, CVC, CVCC, etc.
```

**Contract 4: MorphProof** (Morphological evidence)
```text
[Syllable] → MorphProof
Root candidates, pattern candidates, affix candidates
Rank, residuals, trace
```

**Contract 5: MufradProof** (Lexical closure)
```text
MorphProof → DClosed (closed lexical sign)
Lemma, morphology, boundaries
NO meaning field (Theorem 5 compliance)
```

**Contract 6: PreSyntaxVector** (Syntax interface)
```text
DClosed → PreSyntaxMufradVector
composition_readiness, form_potential, case_sign_potential
NOT case_effect (that's syntax application)
```

**Contract 7: OperatorTrigger** (Operator candidacy)
```text
PreSyntaxMufradVector → OperatorTriggerPotential
Trigger families: NASIKH_INNA, NASIKH_KANA, IBTIDAA, ...
NOT operator application (that's nahw layer)
```

**Contract 8: OperatorRegistry** (Operator inventory)
```text
Catalog of available nahw operators
NOT operator application logic
```

**Contract 9: SentenceFrame** (Composition container)
```text
[MufradProof] → SentenceFrame
Container for multiple mufrad units
Bridge to A8 (Dal-Murakkab)
```

### What Dal-Mufrad Does NOT Do

**Explicitly forbidden**:

#### ❌ Does NOT Create CandidateMadlul (A5)
```text
Dal-Mufrad analyzes FORM, not MEANING.

Example:
✅ كَتَبَ → root=(ك,ت,ب), pattern=فَعَلَ
❌ كَتَبَ → meaning="he wrote"
```

#### ❌ Does NOT Create Wadhʿ (A9)
```text
Dal-Mufrad does not link Dal to Madlul.

Example:
✅ كِتَاب → root=(ك,ت,ب), pattern=فِعَال
❌ كِتَاب ↔ "book" (wadhʿ contract)
```

#### ❌ Does NOT Create Dalalah (A10)
```text
Dal-Mufrad does not specify signification direction.

Example:
✅ إنسان → root=(أ,ن,س), pattern=إفعال
❌ إنسان signifies rational-animal by مطابقة
```

#### ❌ Does NOT Infer Murad (A12)
```text
Dal-Mufrad does not determine intended meaning.

Example:
✅ أسد → root=(أ,س,د), frozen form
❌ أسد means "brave man" in this context (murad inference)
```

#### ❌ Does NOT Apply Syntax Operators
```text
Dal-Mufrad generates operator CANDIDACY, not operator APPLICATION.

Example:
✅ "إنّ" triggers NASIKH_INNA candidate
❌ "إنّ" causes following noun to be mansub (operator application)
```

#### ❌ Does NOT Determine Case Effect
```text
Dal-Mufrad identifies case SIGN POTENTIAL, not case EFFECT.

Example:
✅ "ُ" (damma) is compatible with case effect RAF'
❌ "ُ" means this word IS marfu' (case effect determination)
```

### Implementation Status: A7

**✅ Implemented** in `src/dal_core/`

Key files:
- `carriers.py` (Contract 1: Unicode/UTF-8)
- `atoms.py` (Contract 2: Letters + diacritics)
- `syllables.py` (Contract 3: CV patterns)
- `morph_proof.py` (Contract 4: Morphological evidence)
- `d_mufrad.py` (Contract 5: Lexical closure)
- `presyntax_vector.py` (Contract 6: Syntax interface)
- `operator_trigger.py` (Contract 7: Operator candidacy)
- `nahw_operator_registry.py` (Contract 8: Operator inventory)
- `sentence_frame.py` (Contract 9: Composition container)

**Compliance**: See `docs/DAL_CORE_COMPLIANCE.md`

---

## A8: Dal-Murakkab Algebra

### Definition

**Dal-Murakkab Algebra** governs the **composition** of already-closed individual signifiers.

**Murakkab** (مركب) = composed, compound, multi-unit structure

**Critical principle**:
> **Dal-Murakkab composes CLOSED SIGNIFIERS, not raw forms.**

### Scope

**Dal-Murakkab is responsible for**:

1. **Composition of closed units**:
   - Input: [MufradProof₁, MufradProof₂, ..., MufradProofₙ]
   - Output: MurakkabCandidate
   - Preserve mufrad boundaries within murakkab
   - Maintain order and trace

2. **Structural composition types**:
   - Sequential composition (juxtaposition)
   - Idafa construction (structural, not syntactic)
   - Particle-noun combination
   - Verb-argument sequence
   - **Note**: These are STRUCTURAL patterns, not syntactic relations

3. **Boundary preservation**:
   - Track individual mufrad boundaries
   - Maintain internal boundaries
   - Preserve compositional trace for reversibility

4. **Operator trigger composition**:
   - Combine operator triggers from multiple mufrad units
   - Generate compositional trigger candidates
   - **NOT operator application**

### What Dal-Murakkab Does

#### ✅ Composes Already-Closed Signifiers
```text
Input: [DClosed("كِتَابُ"), DClosed("اللَّهِ")]
Process: Compose with boundary preservation
Output: MurakkabCandidate(
    units=[mufrad1, mufrad2],
    boundaries=[(0,7), (8,14)],
    composition_type=IDAFA_STRUCTURAL,
    trace=[mufrad1, mufrad2]
)
```

#### ✅ Preserves Mufrad Boundaries
```text
MurakkabCandidate maintains:
- Individual mufrad spans
- Boundary positions
- Trace back to individual units
- Reversibility (unfold to mufrad components)
```

#### ✅ Generates Structural Patterns
```text
Identifies composition patterns:
- SEQUENTIAL (juxtaposition)
- IDAFA_STRUCTURAL (positional, not case-based)
- PARTICLE_NOUN (ل + noun, ب + noun...)
- VERB_ARGUMENT (positional sequence)
```

#### ✅ Provides Compositional Operator Triggers
```text
Example: "إنّ الكِتَابَ"
- Mufrad1: "إنّ" → NASIKH_INNA trigger
- Mufrad2: "الكِتَابَ" → DEFINITE_NOUN
- Murakkab: NASIKH_INNA + DEFINITE_NOUN → compositional trigger
```

### What Dal-Murakkab Does NOT Do

#### ❌ Does NOT Create CandidateMadlul (A5)
```text
Dal-Murakkab composes FORMS, not MEANINGS.

Example:
✅ "كِتَابُ اللَّهِ" → [DClosed("كِتَابُ"), DClosed("اللَّهِ")]
❌ "كِتَابُ اللَّهِ" → meaning="Book of Allah"
```

#### ❌ Does NOT Create Wadhʿ (A9)
```text
Dal-Murakkab does not link composed forms to meanings.

Example:
✅ "بيت الله" → structural composition [بيت, الله]
❌ "بيت الله" ↔ "Ka'bah" (wadhʿ for compound)
```

#### ❌ Does NOT Create Dalalah (A10)
```text
Dal-Murakkab does not specify how composition signifies.

Example:
✅ "صلاة الفجر" → compositional structure
❌ "صلاة" signifies ritual prayer by مطابقة, "الفجر" by تضمن
```

#### ❌ Does NOT Infer Murad (A12)
```text
Dal-Murakkab does not determine intended meaning of composition.

Example:
✅ "رأس المال" → [رأس, المال] composition
❌ "رأس المال" means "capital" not "head of wealth" (murad inference)
```

#### ❌ Does NOT Apply Syntax
```text
Dal-Murakkab generates compositional structure, NOT syntactic relations.

Example:
✅ "كِتَابُ اللَّهِ" → IDAFA_STRUCTURAL pattern
❌ "كِتَابُ" is mudaf marfu', "اللَّهِ" is mudaf_ilayh majrur (syntax application)
```

#### ❌ Does NOT Compose Meanings
```text
Dal-Murakkab composes signifier forms, NOT semantic composition.

Example:
✅ "بيت" + "كبير" → sequential composition
❌ HOUSE(big) → semantic composition of house + big
```

### Critical Distinction: Structural vs. Syntactic

**Dal-Murakkab handles STRUCTURAL composition**:
```text
STRUCTURAL: Positional, boundary-based, form-oriented
Examples:
- First unit + Second unit (sequence)
- Unit with particle prefix (ب + noun)
- Idafa pattern: mudaf position + mudaf_ilayh position
```

**NOT syntactic composition**:
```text
SYNTACTIC: Case-based, operator-governed, relation-based
Examples:
- Subject-predicate relation (مبتدأ-خبر)
- Verb-object relation with nasb (فعل-مفعول)
- Operator-operand with case effect (عامل-معمول)
```

**Example: Idafa**

**Dal-Murakkab view** (A8):
```text
"كِتَابُ اللَّهِ"
- Structure: [unit1, unit2]
- Pattern: IDAFA_STRUCTURAL
- Positions: first=potential_mudaf, second=potential_mudaf_ilayh
- Boundaries: preserved
- Trigger: IDAFA_CONSTRUCTION candidate
```

**Syntax view** (out of scope for Dal):
```text
"كِتَابُ اللَّهِ"
- Syntactic relation: IDAFA
- كِتَابُ: mudaf, marfu' by being mubtada (operator application)
- اللَّهِ: mudaf_ilayh, majrur by idafa operator
```

**Dal-Murakkab provides**: Structural pattern trigger
**Syntax layer applies**: Operator, determines case effects

### Implementation Status: A8

**✅ Partially implemented** in `src/dal_core/`

Current implementation:
- `SentenceFrame`: Container for multiple mufrad units
- `OperatorTrigger`: Compositional trigger candidacy

**Not yet implemented**:
- Full MurakkabCandidate contract
- Boundary preservation algebra
- Trace-preserving composition operations
- Structural pattern catalog

**Future work**: Complete A8 implementation in later PRs

---

## Relationship: A7 ↔ A8

### Information Flow

```text
A7 (Dal-Mufrad):
  Input: Raw word form
  Process: Morphological analysis, syllabic structure, lexical closure
  Output: DClosed (MufradProof)

A8 (Dal-Murakkab):
  Input: [DClosed₁, DClosed₂, ..., DClosedₙ]
  Process: Composition, boundary preservation, structural pattern
  Output: MurakkabCandidate

No feedback loop: A8 does not modify A7 outputs
```

### Dependency

**A8 depends on A7**:
```text
A8 requires A7 to complete first.
Cannot compose unclosed signifiers.

❌ FORBIDDEN: Compose raw forms directly
✅ REQUIRED: A7 closes individual forms → A8 composes closed forms
```

### Boundary Preservation

**Critical invariant**:
```text
A8 must preserve A7 boundaries.

Example:
A7 output: DClosed("كِتَابُ", boundaries=(0,7))
A8 composition: Must maintain (0,7) as internal boundary in murakkab
```

---

## Comparison Table: A7 vs A8

| Aspect | A7 (Dal-Mufrad) | A8 (Dal-Murakkab) |
|--------|-----------------|-------------------|
| **Input** | Raw word form | [DClosed₁, ..., DClosedₙ] |
| **Scope** | Individual signifier | Composition of signifiers |
| **Analysis** | Morphology, syllables | Structure, composition |
| **Output** | DClosed (MufradProof) | MurakkabCandidate |
| **Boundaries** | Word boundaries | Preserves mufrad boundaries |
| **Closure** | Lexical closure | Compositional structure |
| **Triggers** | Operator trigger (single) | Compositional trigger |
| **Trace** | Morphological derivation | Composition trace |
| **Implementation** | ✅ Fully implemented | ✅ Partially implemented |

---

## What BOTH A7 and A8 Do NOT Do

### Shared Forbidden Operations

Both Dal-Mufrad and Dal-Murakkab **must not**:

#### 1. Generate CandidateMadlul (A5)
```text
❌ A7: "كَتَبَ" → meaning candidate
❌ A8: "كِتَابُ اللَّهِ" → compositional meaning

Neither creates meaning candidates.
```

#### 2. Establish Wadhʿ (A9)
```text
❌ A7: Link word to meaning via wadhʿ
❌ A8: Link phrase to meaning via wadhʿ

Neither establishes Dal-Madlul correspondence.
```

#### 3. Determine Dalalah (A10)
```text
❌ A7: Specify signification direction (مطابقة/تضمن/التزام)
❌ A8: Specify compositional signification

Neither handles dalalah.
```

#### 4. Apply Syntax Operators
```text
❌ A7: Determine case effect (marfu'/mansub/majrur)
❌ A8: Apply syntactic relations (mubtada-khabar, fa'il-maf'ul)

Both generate operator CANDIDACY, not APPLICATION.
```

#### 5. Classify Usage (A11)
```text
❌ A7: Determine حقيقة vs مجاز
❌ A8: Classify compositional usage

Neither handles istiʿmal classification.
```

#### 6. Infer Murad (A12)
```text
❌ A7: Infer speaker intent
❌ A8: Infer compositional intent

Neither infers intended meaning.
```

#### 7. Produce Hukm (A13)
```text
❌ A7: Generate legal ruling
❌ A8: Infer compositional judgment

Neither handles inference or judgment.
```

---

## Governance: Forbidden Fields in A7 and A8

### DClosed (A7 Output) Must NOT Contain

```python
@dataclass
class DClosed:
    """Dal-Mufrad lexical closure."""

    # ✅ ALLOWED
    lemma: str
    morphology: DMorph
    boundaries: Tuple[int, int]
    root: Optional[Tuple[str, ...]]
    pattern: Optional[str]

    # ❌ FORBIDDEN (Theorem 5 compliance)
    meaning: ...        # Must not exist
    wadhʿ: ...          # Must not exist
    madlul: ...         # Must not exist
    murad: ...          # Must not exist
    haqiqa_majaz: ...   # Must not exist
    dalalah: ...        # Must not exist
    hukm: ...           # Must not exist
```

### MurakkabCandidate (A8 Output) Must NOT Contain

```python
@dataclass
class MurakkabCandidate:
    """Dal-Murakkab compositional structure."""

    # ✅ ALLOWED
    units: List[DClosed]
    boundaries: List[Tuple[int, int]]
    composition_type: CompositionType
    trace: List[DClosed]
    structural_pattern: StructuralPattern

    # ❌ FORBIDDEN
    compositional_meaning: ...  # Must not exist
    wadhʿ: ...                  # Must not exist
    semantic_composition: ...   # Must not exist
    murad: ...                  # Must not exist
    syntactic_relation: ...     # Must not exist
    case_effects: ...           # Must not exist (operator application)
```

---

## Examples: A7 and A8 in Practice

### Example 1: Simple Word (A7 Only)

**Input**: "كَتَبَ"

**A7 Processing**:
```text
1. Carriers (Contract 1):
   Unicode: [U+0643, U+064E, U+062A, U+064E, U+0628, U+064E]

2. Atoms (Contract 2):
   [Atom(ك, FATHA), Atom(ت, FATHA), Atom(ب, FATHA)]

3. Syllables (Contract 3):
   [Syllable(ka, CV), Syllable(ta, CV), Syllable(ba, CV)]

4. MorphProof (Contract 4):
   RootCandidate(root=(ك,ت,ب), rank=HIGH, residuals=[])
   PatternCandidate(pattern=فَعَلَ, rank=HIGH)

5. MufradProof (Contract 5):
   DClosed(
       lemma="كَتَبَ",
       morphology=DMorph(root=(ك,ت,ب), pattern=فَعَلَ),
       boundaries=(0, 6)
   )
```

**A7 Output**: `DClosed("كَتَبَ")`

**A8**: Not applicable (single word, no composition)

### Example 2: Phrase (A7 → A8)

**Input**: "كِتَابُ اللَّهِ"

**A7 Processing** (for each word):
```text
Word 1: "كِتَابُ"
  → DClosed(
      lemma="كِتَاب",
      morphology=DMorph(root=(ك,ت,ب), pattern=فِعَال),
      boundaries=(0, 7)
  )

Word 2: "اللَّهِ"
  → DClosed(
      lemma="الله",
      morphology=DMorph(frozen=True, type=PROPER_NOUN),
      boundaries=(8, 14)
  )
```

**A8 Processing**:
```text
Input: [DClosed1, DClosed2]

Composition:
  MurakkabCandidate(
      units=[DClosed1, DClosed2],
      boundaries=[(0,7), (8,14)],
      composition_type=SEQUENTIAL,
      structural_pattern=IDAFA_STRUCTURAL,
      trace=[DClosed1, DClosed2],
      operator_triggers=[IDAFA_CONSTRUCTION]
  )
```

**A8 Output**: `MurakkabCandidate` with preserved mufrad boundaries

**What A8 does NOT output**:
```text
❌ Meaning: "Book of Allah"
❌ Wadhʿ: compound ↔ Qur'an
❌ Syntactic relation: mudaf-mudaf_ilayh with case
❌ Murad: "Qur'an is intended"
```

### Example 3: Operator Particle (A7 → A8)

**Input**: "إنّ الكِتَابَ"

**A7 Processing**:
```text
Word 1: "إنّ"
  → DClosed(
      lemma="إنّ",
      morphology=DMorph(type=PARTICLE_NASIKH),
      boundaries=(0, 3),
      operator_trigger=NASIKH_INNA
  )

Word 2: "الكِتَابَ"
  → DClosed(
      lemma="كِتَاب",
      morphology=DMorph(root=(ك,ت,ب), pattern=فِعَال),
      boundaries=(4, 13),
      definiteness=DEFINITE,
      case_sign_potential=[NASB_COMPATIBLE]
  )
```

**A8 Processing**:
```text
Input: [DClosed1, DClosed2]

Composition:
  MurakkabCandidate(
      units=[DClosed1, DClosed2],
      boundaries=[(0,3), (4,13)],
      composition_type=PARTICLE_NOUN,
      structural_pattern=OPERATOR_OPERAND_STRUCTURAL,
      trace=[DClosed1, DClosed2],
      operator_triggers=[NASIKH_INNA],
      operand_candidates=[DClosed2]
  )
```

**What A8 provides**:
```text
✅ Structural pattern: PARTICLE + NOUN
✅ Trigger: NASIKH_INNA candidate
✅ Operand candidate: DClosed2 with NASB_COMPATIBLE sign
```

**What A8 does NOT provide**:
```text
❌ Case effect: "الكِتَابَ is mansub by إنّ"
❌ Syntactic relation: "ism of إنّ"
❌ Operator application result
```

**Operator application** is responsibility of **syntax layer** (outside Dal), which:
- Receives operator trigger from A8
- Applies operator to operand
- Determines case effect
- Validates syntactic constraints

---

## Verification: A7 and A8 Compliance

### Checklist for A7 (Dal-Mufrad)

#### ✅ Required
- [ ] DClosed contains morphology fields (root, pattern, affixes)
- [ ] DClosed contains boundaries
- [ ] DClosed contains lemma
- [ ] MufradProof preserves trace
- [ ] PreSyntaxVector generates operator trigger candidates
- [ ] Case sign potential (not case effect)

#### ❌ Forbidden
- [ ] DClosed must NOT contain `meaning` field
- [ ] DClosed must NOT contain `wadhʿ` field
- [ ] DClosed must NOT contain `murad` field
- [ ] DClosed must NOT contain `dalalah` field
- [ ] Must NOT generate CandidateMadlul
- [ ] Must NOT apply syntax operators
- [ ] Must NOT determine case effects

### Checklist for A8 (Dal-Murakkab)

#### ✅ Required
- [ ] MurakkabCandidate contains list of DClosed units
- [ ] Preserves individual mufrad boundaries
- [ ] Contains composition trace
- [ ] Contains structural pattern classification
- [ ] Generates compositional operator triggers
- [ ] Maintains reversibility (unfold to mufrad)

#### ❌ Forbidden
- [ ] Must NOT contain compositional meaning
- [ ] Must NOT contain compositional wadhʿ
- [ ] Must NOT contain semantic composition
- [ ] Must NOT contain syntactic relations
- [ ] Must NOT apply operators
- [ ] Must NOT determine case effects
- [ ] Must NOT infer murad

---

## Conclusion

**Dal-Mufrad (A7)** and **Dal-Murakkab (A8)** are correctly scoped as:

1. **Pre-semantic specializations** (form analysis, not meaning)
2. **Pre-Wadhʿ layers** (structure, not Dal-Madlul linking)
3. **Pre-syntax layers** (candidacy, not operator application)
4. **Form-oriented** (morphology, composition, structure)

**They do NOT handle**:
- Meaning formation (A5: CandidateMadlul)
- Wadhʿ contracts (A9)
- Dalalah direction (A10)
- Usage classification (A11)
- Intended meaning (A12)
- Judgment/inference (A13)
- Syntax operator application (syntax layer, outside Dal)

**They correctly provide**:
- Morphological analysis (A7)
- Lexical closure (A7)
- Compositional structure (A8)
- Operator trigger candidacy (A7, A8)
- Boundary preservation (A7, A8)
- Trace preservation (A7, A8)

**Implementation status**:
- A7: ✅ Fully implemented (`dal_core`)
- A8: ✅ Partially implemented (`SentenceFrame`, `OperatorTrigger`)

**Compliance**: Verified via `docs/DAL_CORE_COMPLIANCE.md` and Theorem 5 (no meaning fields in DClosed)

---

**Status**: ✅ Documented (scope clarification)
**Related**:
- `docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md` (complete A0-A13 hierarchy)
- `docs/GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md` (Dal positioning in General Algebra)
- `docs/ORDERED_DAL_FORM_GOVERNANCE.md` (A6 governance, PR #21)
- `docs/REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md` (pre-Wadhʿ layers A1-A6)
- `docs/SPEC_DAL_CORE.md` (A7 implementation specification)
- `docs/DAL_CORE_COMPLIANCE.md` (A7 compliance verification)

