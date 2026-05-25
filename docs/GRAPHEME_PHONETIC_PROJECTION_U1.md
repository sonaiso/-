# Grapheme Phonetic Projection Theory (U₁ Layer)

## Overview

This document specifies the **Initial Phonetic Projection** layer (U₁) in the Arabic linguistic analysis pipeline. U₁ adds phonetic classification capabilities to grapheme clusters WITHOUT prematurely jumping to syllable, morphological, or semantic analysis.

## Core Principle

**U₁ produces phonetic CANDIDATES (hypotheses), not CERTIFICATES (proven structures).**

The maximum epistemic rank at this layer is `grapheme_phonetic_hypothesis` (0.5), which is strictly less than a phonological certificate (≥ 0.7).

## Mathematical Formulation

### Grapheme Phonetic Projection Theorem

**Statement:**

For every licensed grapheme G ∈ U₁, the system produces one or more initial phonetic projections or classified residuals, without claiming syllable/root/pattern/meaning.

**Formal:**

```
∀G ∈ U₁, phon_project1(G) ∈ PhoneticCandidate1⁺ ∪ Residual1 ∪ Fail1
```

Where:
- `PhoneticCandidate1⁺`: One or more phonetic candidates
- `Residual1`: Classified residuals (ambiguous, deferred, or unclassifiable)
- `Fail1`: Explicit failure with evidence

### Grapheme Structure

A grapheme in U₁ is defined as:

```
G = (
  base,                    # Base character
  marks,                   # Diacritics list
  position,                # Position in sequence
  trace0,                  # Trace to U₀ Carrier
  grapheme_class,          # Graphemic classification
  phonetic_projection1,    # NEW: Initial phonetic projection
  policies,                # NEW: Policy declarations
  residuals                # Accumulated residuals
)
```

## Phonetic Classification Categories (10 Types)

### 1. ClearConsonant_C (صامت واضح)

**Definition:** Unambiguous Arabic consonants

**Examples:** ب، ت، ج، د، ر، س، ص، ض، ط، ظ، ع، غ، ف، ق، ك، ل، م، ن، ه

**Evidence:** Membership in `CLEAR_CONSONANTS` set

**Rank:** `RANK_CLEAR_CLASSIFICATION` (0.45)

**Output:** `MakhrajCandidate` with approximate articulation region

**Not Produced:** Root extraction, syllable position, morphological role

### 2. ClearShortVowel_V (صائت قصير واضح)

**Definition:** Short vowel marks attached to a carrier

**Marks:**
- `\u064E` (َ) → fatha → /a/
- `\u064F` (ُ) → damma → /u/
- `\u0650` (ِ) → kasra → /i/

**Critical Constraint:** Vowel MUST have carrier (base character)

**Orphan Vowel:** Diacritic without carrier → `RESIDUAL` with blocker

**Output:** `VowelCandidate` with quality and length

**Example:**
```
بَ → C=/b/ (clear) + V=/a/ (short, clear)
```

### 3. ClearLongVowel_VV (صائت طويل واضح)

**Definition:** Long vowel candidate based on TWO-grapheme relation

**Formation:**
```
Gi (with short vowel v) + Gi+1 (compatible letter) → VV candidate
```

**Compatibility Table:**
```
fatha (َ) + ا → /ā/ candidate
damma (ُ) + و → /ū/ candidate
kasra (ِ) + ي → /ī/ candidate
```

**Examples:**
```
بَا → /bā/ candidate (ba + alif)
بُو → /bū/ candidate (bu + waw)
بِي → /bī/ candidate (bi + ya)
```

**Critical:** This is RELATION-BASED, not single-character classification

**Not Guaranteed:** Second letter (ا، و، ي) may also be consonant in other contexts

### 4. SukunOrClosure (سكون أو إغلاق)

**Definition:** Sukun mark (ْ) indicating potential syllable closure

**Mark:** `\u0652` (ْ)

**Output:** `ClosureCandidate` with:
- `is_coda: True` (potential coda)
- `is_sukun: True` (written sukun present)

**Critical Residual:** "Sukun closure needs syllable context (U₂)"

**Example:**
```
بْ → closure candidate (NOT final syllable structure)
```

**Deferred:**
- Solar/lunar assimilation (الشمسية/القمرية)
- Waqf/Wasl boundary effects

### 5. ShaddahPolicy (سياسة الشدة)

**Definition:** Shadda mark (ّ) with gemination policy

**Mark:** `\u0651` (ّ)

**Policy Options:**
1. `PreserveAsMark` - Keep as written (default at U₁)
2. `ExpandToGeminateCandidate` - Note expansion possibility
3. `ExpandOnlyInPhonologyLayer` - Defer to U₂
4. `ResidualizeIfAmbiguous` - Mark as residual

**Example:**
```
نَّ → geminate candidate
  Policy: EXPAND_TO_GEMINATE_CANDIDATE
  Expansion hypothesis: nْ + nَ
  Critical: Expansion NOT performed at U₁
```

**Trace Preservation:** If expanded later, both C₁ and C₂ trace back to same original grapheme

### 6. TanweenPolicy (سياسة التنوين)

**Definition:** Tanween marks with waqf/wasl sensitivity

**Marks:**
```
\u064B (ً) → fathatan → /an/ (wasl) or /ā/ (waqf)
\u064C (ٌ) → dammatan → /un/ (wasl) or /u/ (waqf)
\u064D (ٍ) → kasratan → /in/ (wasl) or /i/ (waqf)
```

**Policy:** `WAQF_SENSITIVE` - Preserve BOTH candidates

**Example:**
```
كِتَابٌ
  Wasl candidate: /kitābun/
  Waqf candidate: /kitāb/ or /kitābu/
  Both preserved at U₁
```

**Not Produced:** Final determination of definiteness (نكرة/معرفة)

### 7. MaddPolicy (سياسة المد)

**Definition:** Madd marks and extended vowels

**Cases:**
1. Written madd: آ (alif with maddah)
2. Quranic madd marks
3. Prolonged vowels

**Policy Options:**
- `PreserveWrittenMadd`
- `SplitHamzaAlifCandidate` (آ → أ + ا)
- `ProjectLongVowelCandidate`
- `QuranicMaddDeferred`

**Example:**
```
آ → Madd candidates:
  1. Hamza + alif split
  2. Long vowel with hamza
  Policy deferred to context
```

### 8. WaqfWaslPolicy (سياسة الوقف والوصل)

**Definition:** Boundary sensitivity (pausal vs connected speech)

**Modes:**
- `WaslMode` - Connected speech
- `WaqfMode` - Pausal form
- `UnknownBoundary` - Context needed
- `PreserveBothCandidates` - Default at U₁

**Example:**
```
الْأَعْمَالُ (final U)
  Wasl: /ul/ realized before next word
  Waqf: /u/ or sukun at pause
  U₁: Preserves both
```

### 9. Deferred (مؤجل)

**Definition:** Ambiguous graphemes requiring context

**Cases:**
- ا: Long vowel carrier OR hamza support
- و: Consonant /w/ OR long vowel nucleus
- ي: Consonant /y/ OR long vowel nucleus

**Output:** Multiple `PhoneticCandidate` entries, all preserved

**Example:**
```
وَلَد (initial و)
  Candidate 1: Consonant /w/ (likely)
  Candidate 2: Long vowel carrier (unlikely but preserved)
  No final determination at U₁
```

### 10. Residual (بقايا)

**Definition:** Unclassifiable or malformed graphemes

**Examples:**
- Orphan diacritics (no carrier)
- Unknown characters
- Foreign symbols in Arabic text

**Output:** `RESIDUAL` classification with blocker

## Critical Laws (No-Jumping Validation)

### Law 1: NO Syllable Formation

**Forbidden:**
- CV, CVC, CVV syllable patterns
- Syllable boundary marking
- Prosodic structure assignment

**Validation:**
```python
def validate_no_syllable_formation(result):
    # Check candidates don't have syllable_type field
    # Check length_candidate not in {'CV', 'CVC', 'CVV', 'CVCC'}
```

### Law 2: NO Root Extraction

**Forbidden:**
- Root consonants identification (جذر)
- Root type classification (trilateral/quadrilateral)
- Root-pattern binding

**Validation:**
```python
def validate_no_root_extraction(result):
    # Check candidates don't have root_consonants field
    # Check no root_type field
```

### Law 3: NO Pattern Matching

**Forbidden:**
- Morphological pattern (وزن) identification
- Pattern-form binding (فَعَل، فاعل، etc.)

**Validation:**
```python
def validate_no_pattern_matching(result):
    # Check candidates don't have pattern/wazn field
    # Check no morph_class field
```

### Law 4: Rank Ceiling

**Maximum Rank:** `GRAPHEME_PHONETIC_HYPOTHESIS_RANK = 0.5`

**Enforcement:**
```python
assert result.rank <= 0.5
assert all(c.rank <= 0.5 for c in result.candidates)
```

### Law 5: Trace Preservation

**Requirement:** Every U₁ projection must trace back to U₀

**Validation:**
```python
assert result.grapheme.trace0 is not None or \
       result.grapheme.source_atom is not None
```

### Law 6: Residual Accumulation

**Law:** Residuals accumulate, never get erased

**Formula:**
```
Res(output) = Res(input) ⊕ NewResiduals - DischargedByProof
```

At U₁: No discharging occurs, only accumulation

## Data Flow

### U₀ → U₁ Pipeline

```
Text → U₀ Carriers → Atoms → U₁ Graphemes → Phonetic Projections
```

**Step 1:** Text to Carriers
```python
carriers, residuals = text_to_carriers("بَا")
```

**Step 2:** Carriers to Atoms
```python
atoms, atom_residuals = carriers_to_atoms(carriers)
```

**Step 3:** Atoms to Graphemes
```python
# Collect base + following marks
grapheme = GraphemeCarrierU1(
    base=atom.carrier.char,
    marks=[...],
    trace0=atom.carrier,
    source_atom=atom
)
```

**Step 4:** Phonetic Projection
```python
result = project_phonetic1(grapheme, prev_g, next_g)
```

**Step 5:** Validation
```python
is_valid, violations = validate_phonetic_projection(result)
```

## Implementation Architecture

### Core Modules

1. **grapheme_phonetic_projection.py** (356 lines)
   - Enums: `PhoneticClass1`, policies
   - Data classes: `PhoneticCandidate`, `GraphemeCarrierU1`
   - Constants: consonant/vowel tables

2. **grapheme_phonetic_classifiers.py** (540 lines)
   - 7 classification functions
   - Policy handlers
   - Candidate generation

3. **grapheme_phonetic_engine.py** (453 lines)
   - Main projection function
   - Batch processing
   - No-jumping validation
   - Theorem verification

### API Entry Points

```python
# High-level API
results, residuals = text_to_grapheme_projections("بَا")

# Low-level API
grapheme = make_grapheme(...)
result = project_phonetic1(grapheme, prev_g, next_g)

# Validation
is_valid, violations = validate_phonetic_projection(result)

# Theorem verification
is_proven, message = verify_grapheme_phonetic_projection_theorem(results)
```

## Examples

### Example 1: Clear Consonant + Vowel

```python
text = "بَ"  # ba with fatha
results, residuals = text_to_grapheme_projections(text)

assert len(results) == 1
assert results[0].phonetic_class == PhoneticClass1.CLEAR_CONSONANT_C
assert results[0].success == True
assert results[0].rank <= 0.5
```

### Example 2: Long Vowel Candidate

```python
text = "بَا"  # ba + alif
results, residuals = text_to_grapheme_projections(text)

# First grapheme: consonant
assert results[0].phonetic_class == PhoneticClass1.CLEAR_CONSONANT_C

# May detect long vowel relation
# (depends on classifier seeing both graphemes)
```

### Example 3: Shadda Policy

```python
text = "نَّ"  # noon with shadda + fatha
results, residuals = text_to_grapheme_projections(text)

result = results[0]
assert result.phonetic_class == PhoneticClass1.SHADDA_POLICY
assert len(result.policies) > 0
assert result.policies[0].policy_type == "shadda"

# Gemination candidate present but NOT expanded
assert result.grapheme.base == 'ن'  # Still single grapheme
```

### Example 4: Tanween with Waqf/Wasl

```python
text = "كِتَابٌ"  # kitab with dammatan
results, residuals = text_to_grapheme_projections(text)

# Last grapheme has tanween
tanween_result = [r for r in results
                  if r.phonetic_class == PhoneticClass1.TANWEEN_POLICY][0]

# Both candidates preserved
policy = tanween_result.policies[0]
assert len(policy.candidates) == 2  # wasl and waqf
```

### Example 5: Ambiguous Letter

```python
text = "وَلَد"  # walad (initial waw)
results, residuals = text_to_grapheme_projections(text)

# First grapheme: و with fatha
# May be DEFERRED with multiple candidates
assert results[0].phonetic_class in {
    PhoneticClass1.CLEAR_CONSONANT_C,  # If treated as /w/
    PhoneticClass1.DEFERRED  # If ambiguous
}
```

## Theorem Proof Sketch

### Theorem Statement

∀G ∈ U₁, phon_project1(G) ∈ PhoneticCandidate1⁺ ∪ Residual1 ∪ Fail1

### Proof by Cases

**Case 1:** G.base ∈ CLEAR_CONSONANTS
- Classifier: `classify_clear_consonant(G)`
- Output: PhoneticCandidate1 with MakhrajCandidate
- ✓ Theorem satisfied

**Case 2:** G has short vowel mark (َ ُ ِ)
- Classifier: `classify_short_vowel(G)`
- If carrier exists: PhoneticCandidate1 with VowelCandidate
- If no carrier: Residual1 (orphan vowel)
- ✓ Theorem satisfied

**Case 3:** G + G_{i+1} form long vowel relation
- Classifier: `detect_long_vowel_candidate(G, G_{i+1})`
- Output: PhoneticCandidate1 with VowelCandidate (long)
- ✓ Theorem satisfied

**Case 4:** G has sukun mark
- Classifier: `classify_sukun_closure(G)`
- Output: PhoneticCandidate1 with ClosureCandidate + Residual1 (deferred)
- ✓ Theorem satisfied

**Case 5:** G has shadda mark
- Classifier: `apply_shadda_policy(G)`
- Output: PhoneticCandidate1 + PolicyDeclaration + Residual1 (deferred)
- ✓ Theorem satisfied

**Case 6:** G has tanween mark
- Classifier: `apply_tanween_policy(G)`
- Output: Multiple PhoneticCandidate1 (wasl + waqf) + PolicyDeclaration
- ✓ Theorem satisfied

**Case 7:** G.base ∈ AMBIGUOUS_LETTERS
- Classifier: `classify_ambiguous_letter(G, prev_G)`
- Output: Multiple PhoneticCandidate1 + Residual1 (ambiguous)
- ✓ Theorem satisfied

**Case 8:** G unclassifiable
- Default handler in `project_phonetic1`
- Output: Fail1 with RESIDUAL classification + blocker
- ✓ Theorem satisfied

### Verification

For all test cases:
```python
is_proven, message = verify_grapheme_phonetic_projection_theorem(results)
assert is_proven
```

## Limitations and Future Work

### Current Limitations

1. **Context Window:** Only sees prev/next grapheme, not full word/sentence
2. **No Tajweed Rules:** Advanced Quranic phonology deferred
3. **No Dialect Variation:** Classical Arabic only
4. **No Stress/Intonation:** Prosodic features deferred to U₂

### Future U₂ Layer (Phonological Carrier)

U₂ will provide:
- **Syllable Formation:** CV, CVC, CVV structures
- **Phonological Processes:** Assimilation, deletion, epenthesis
- **Prosodic Structure:** Stress patterns, foot structure
- **Final Certificates:** rank ≥ 0.7 (phonological certificate)

### Deferred to Morphology Layer

- Root extraction (جذر)
- Pattern matching (وزن)
- Derivational analysis (اشتقاق)
- Inflectional features (صرف)

### Deferred to Syntax Layer

- Case assignment (إعراب)
- Syntactic roles (فاعل، مفعول، etc.)
- Operator effects (عوامل)

## Conclusion

The U₁ Grapheme Phonetic Projection layer successfully implements initial phonetic classification while rigorously enforcing the no-jumping laws. All graphemes produce either phonetic candidates or classified residuals, with full trace preservation and residual accumulation, at a maximum rank of 0.5 (hypothesis, not certificate).

This architecture enables a clean separation of concerns:
- U₀: Character-level carriers
- U₁: Grapheme-level phonetic hypotheses ← **This layer**
- U₂: Syllable-level phonological certificates
- Higher layers: Morphology, syntax, semantics

The theorem is proven by exhaustive case analysis, and validation is enforced programmatically through the no-jumping validation functions.
