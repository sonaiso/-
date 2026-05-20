# Dal-Mufrad and Dal-Murakkab Position

**PR #22**: Position specification for the two dal-only analysis loops
**Created**: 2026-05-20
**Status**: Documentation only (no implementation)

---

## Purpose

This document clarifies the **two specialized dal-only algebras** within the larger architecture:

1. **Dal-Mufrad Algebra** (A3): Individual signifier closure
2. **Dal-Murakkab Algebra** (A4): Compositional signifier structure

Both are **pre-semantic** - they operate on form (الدال) only, never on meaning (المدلول).

---

## The Two-Loop Dal Architecture

```
A1: Carrier / Ordered Form
          ↓
A3: Dal-Mufrad (Individual Signifier Closure)
          ↓ MufradProof
A4: Dal-Murakkab (Compositional Structure)
          ↓ (future) MurakkabProof
          ║
          ║ ← Boundary: Form ends, meaning begins
          ↓
A5: Wadh' (Signifier-Signified Linking)
```

**Critical Principle**: A3 and A4 are **form-only loops**. They close without crossing into semantic domain.

---

## A3: Dal-Mufrad Algebra (Individual Signifier Closure)

### Purpose

**Close the individual signifier** as an ordered, bounded, internally composed **form candidate**.

**Input**: Single Arabic word (raw text or carriers)

**Output**: `MufradProof` - certified form analysis with candidates, rank, residuals

**Domain**: الدال المفرد (individual signifier) only

---

### Implementation Chain

```
Carrier (encoded text with marks)
  ↓
Atom (letters with diacritics)
  ↓
Syllable (phonological units)
  ↓
Pre-morph (segmentation candidates)
  ↓
Origin (root vs frozen distinction)
  ↓
Template (pattern/wazn candidates)
  ↓
Identity Axis (lexical lookup)
  ↓
Directional Analysis (bidirectional scan)
  ↓
Judgment (final mufrad categorization)
  ↓
MufradProof (closure)
```

**8-Layer Transition Domains** (D0-D7):
- D0: GRAPHOPHONEMIC (رسم/صوت)
- D1: SYLLABIC (مقطع)
- D2: PRE_MORPH (ما قبل الصرف)
- D3: ORIGIN (أصل - root or frozen)
- D4: TEMPLATE (وزن)
- D5: IDENTITY_AXIS (محور الهوية)
- D6: DIRECTIONAL_ANALYSIS (تحليل اتجاهي)
- D7: JUDGMENT (حكم - categorization)

**Note**: This is a **partial transition network** (شبكة انتقالات جزئية), not a single pipeline. Different words follow different paths.

---

### What Dal-Mufrad Includes

✅ **Form Analysis**:
- Carrier representation
- Mark attachment (diacritics, hamza, shadda)
- Atomic units
- Syllable structure
- Morphological segmentation
- Root extraction candidates (if applicable)
- Pattern (wazn) candidates (if applicable)
- Stem analysis
- Clitic analysis
- Surface effects

✅ **Form Candidates**:
- `RootCandidate` (if derived word)
- `WaznCandidate` (if patterned word)
- `StemProof`
- `CliticProof`
- `SegmentationProof`
- `VerbFeatureProof` (if verb)
- `NounInflectionClass` (if noun)
- `ParticleOperatorPotential` (if particle)

✅ **Form Evidence**:
- Surface marks (الحركات)
- Phonological patterns
- Morphological patterns
- Lexicon attestation
- Pattern frequency
- Root productivity

✅ **Form Metadata**:
- Rank (preference ordering among candidates)
- Residuals (unresolved morphological questions)
- Trace (transition history)
- Competitors (alternative analyses)
- Surface effects

---

### What Dal-Mufrad Does NOT Include

❌ **Semantic Outputs**:
- Meaning (المعنى)
- Signified (المدلول)
- Murad (المراد / intended meaning)
- Haqiqa/Majaz interpretation
- Usage context (عرف/شرع)
- Real-world reference

❌ **Syntax Outputs**:
- Syntax role (subject, object, etc.) - that's A4's job
- Case effect (رفع/نصب/جر) - that's A4's job
- Grammatical relation (إسناد/تضمين/تقييد) - that's A4's job
- Operator application - that's A4's job

❌ **Judgment Outputs**:
- Legal judgment (الحكم الشرعي) - that's A10
- Logical inference - that's A10
- Final interpretation - that's A9/A10

---

### Current Implementation Status

**Phase 0/1**: ✅ **Implemented**

**Files**:
- `src/dal_core/pipeline.py` - `analyze_dal_mufrad()`
- `src/dal_core/mufrad_proof.py` - `MufradProof`
- `src/dal_core/morph_features.py` - Morphological candidates
- `src/dal_core/carriers.py` - Carrier implementation
- `src/dal_core/atoms.py` - Atomic units

**Tests**:
- `tests/dal_core/test_runner.py`
- `tests/test_dal_pipeline.py`
- `tests/dal_core/test_carriers.py`
- `tests/dal_core/test_mufrad_proof.py`

**Contracts Implemented**:
- Contract 1: Carrier
- Contract 2: Atom
- Contract 3: Unit

**Contracts Data-Only** (no logic yet):
- Contracts 4-9 exist as data structures

---

### Dal-Mufrad Output: MufradProof

**Structure**:
```python
@dataclass
class MufradProof:
    d_form: DForm                    # Carrier form
    d_lugha: DLugha                  # Language/encoding
    d_type: DType                    # Lexical type
    d_mufrad: DMufrad                # Closed mufrad

    # Morphological candidates
    root_candidates: List[RootCandidate]
    wazn_candidates: List[WaznCandidate]
    stem_proof: Optional[StemProof]
    clitic_proof: Optional[CliticProof]
    segmentation_proof: Optional[SegmentationProof]

    # Surface analysis
    surface_effects: List[SurfaceEffect]

    # Metadata
    rank: Rank
    residuals: List[Residual]
    evidence: List[Evidence]

    # Forbidden fields (enforced by tests)
    # ❌ meaning: ...
    # ❌ murad: ...
    # ❌ haqiqa_majaz: ...
```

**Key Laws**:
1. **No meaning fields** - `meaning`, `murad`, `haqiqa_majaz` are FORBIDDEN
2. **Form-only certification** - MufradProof certifies form, not meaning
3. **Unresolved allowed** - Residuals track unresolved morphological questions
4. **Competitors preserved** - Alternative root/wazn candidates maintained

---

## A4: Dal-Murakkab Algebra (Compositional Structure)

### Purpose

**Compose already-closed `MufradProof` objects** into governed structure candidates.

**Input**: List of `MufradProof` objects (each already closed)

**Output**: (future) `MurakkabProof` - certified compositional structure with relation/case candidates

**Domain**: الدال المركب (compositional signifier) - still form-only

---

### Implementation Chain

```
MufradProof (A3 output)
  ↓
PreSyntaxMufradVector (governed interface)
  ↓
SentenceFrameCandidate (nominal/verbal/particle-led/fragment)
  ↓
CaseSignMatrix (surface sign observations)
  ↓
OperatorTriggerPotential (operator trigger candidates)
  ↓
NahwOperatorRegistry (operator lookup)
  ↓
OperatorCandidate (operator application candidates)
  ↓
(future) RelationCandidate (إسناد/تضمين/تقييد candidates)
  ↓
(future) CaseEffectCandidate (رفع/نصب/جر/جزم candidates)
  ↓
(future) MurakkabProof (closure)
```

---

### Current Implementation Status

**Partially Implemented**: 🚧

**Implemented Components**:
- ✅ `PreSyntaxMufradVector` (PR #10)
- ✅ `SentenceFrameCandidate` (PR #12)
- ✅ `CaseSignMatrix` (PR #13)
- ✅ `OperatorTriggerPotential` (PR #14)
- ✅ `NahwOperatorRegistry` (PR #15/16)
- ✅ `OperatorCandidate` (PR #17)

**Future Components**:
- 🔮 `RelationCandidate` (إسناد/تضمين/تقييد)
- 🔮 `CaseEffectCandidate` (case marking)
- 🔮 `MurakkabProof` (compositional closure)

---

### What Dal-Murakkab Includes

✅ **Compositional Analysis**:
- Frame type detection (nominal/verbal/particle-led/fragment)
- Surface sign observation (marks on composition)
- Operator trigger detection
- Operator application candidates
- Relation candidates (future)
- Case effect candidates (future)

✅ **Compositional Evidence**:
- Surface signs on composed units
- Frame structure patterns
- Operator compatibility
- Sign matrix observations

✅ **Compositional Metadata**:
- Frame rank
- Inherited residuals (from MufradProof)
- Compositional trace
- Operator competitors

---

### What Dal-Murakkab Does NOT Include

❌ **Semantic Composition**:
- Meaning composition
- Semantic role assignment
- Murad inference
- Contextual interpretation

❌ **Final Judgment**:
- Resolved case (final رفع/نصب/جر decision) - only candidates
- Resolved relation (final إسناد decision) - only candidates
- Legal/logical judgment
- Inference

❌ **Mufrad Modification**:
- Cannot raise Mufrad rank
- Cannot resolve Mufrad residuals
- Cannot modify Mufrad candidates
- Only inherits, never improves

---

### Critical Dal-Murakkab Laws

#### Law 1: Murakkab Does Not Raise Mufrad Rank

**Principle**: Composition cannot improve individual form quality

```python
# ❌ FORBIDDEN
murakkab_proof.modify_mufrad_rank(mufrad_id, new_rank=higher)

# ✅ CORRECT
murakkab_proof.mufrad_proofs = original_mufrad_proofs  # unchanged
murakkab_proof.frame_rank = calculate_frame_rank(...)  # separate
```

**Rationale**: Form quality is intrinsic to individual signifier, not determined by composition context.

#### Law 2: Murakkab Inherits Mufrad Residuals

**Principle**: Unresolved morphological questions propagate upward

```python
# ✅ CORRECT
murakkab_residuals = []
for mufrad in mufrad_proofs:
    murakkab_residuals.extend(mufrad.residuals)  # inherited
murakkab_residuals.extend(composition_residuals)  # added
```

**Rationale**: Cannot resolve at composition level what was unresolved at individual level.

#### Law 3: Murakkab Preserves Mufrad Competitors

**Principle**: Alternative analyses at individual level remain visible at compositional level

```python
# ✅ CORRECT
for mufrad in mufrad_proofs:
    # All root/wazn candidates preserved
    murakkab_proof.store_mufrad_competitors(mufrad)
```

**Rationale**: Composition explores combinations, doesn't eliminate individual alternatives.

#### Law 4: Murakkab Does Not Create Meaning

**Principle**: Dal-Murakkab is still dal-only (form)

```python
# ❌ FORBIDDEN
murakkab_proof.sentence_meaning = "The writer wrote"
murakkab_proof.semantic_roles = {"agent": "الكاتب", "theme": "الكتاب"}

# ✅ CORRECT
murakkab_proof.relation_candidates = [
    RelationCandidate(type=ISN, mubtada_index=0, khabar_index=1)
]
```

**Rationale**: Form composition ≠ meaning composition. Meaning requires A5+ (Wadh', Madlul, Murad).

#### Law 5: Murakkab Does Not Infer Murad

**Principle**: Intended meaning requires context, speaker intent, usage - not available at form level

```python
# ❌ FORBIDDEN
murakkab_proof.intended_meaning = "..."
murakkab_proof.speaker_intent = "..."

# ✅ CORRECT
murakkab_proof.case_effect_candidates = [
    CaseEffectCandidate(effect=INNA_NASB, target_index=1)
]
```

**Rationale**: Murad is A9 - requires all previous layers including semantic linking.

---

### Dal-Murakkab Output: MurakkabProof (Future)

**Structure** (proposed):
```python
@dataclass
class MurakkabProof:
    mufrad_proofs: List[MufradProof]  # Input (unchanged)

    # Compositional analysis
    frame: SentenceFrameCandidate
    case_sign_matrix: CaseSignMatrix
    operator_trigger_potential: OperatorTriggerPotential
    operator_candidates: OperatorCandidateSet

    # Future: Relation/case candidates
    relation_candidates: List[RelationCandidate]  # إسناد/تضمين/تقييد
    case_effect_candidates: List[CaseEffectCandidate]  # رفع/نصب/جر/جزم

    # Metadata
    frame_rank: Rank
    inherited_residuals: List[Residual]  # From mufrad
    composition_residuals: List[Residual]  # New
    compositional_trace: List[str]

    # Forbidden fields (enforced by tests)
    # ❌ sentence_meaning: ...
    # ❌ semantic_roles: ...
    # ❌ murad: ...
```

**Key Laws**:
1. **No meaning fields** - Same prohibition as MufradProof
2. **Mufrad proofs unchanged** - Input preserved without modification
3. **Residuals inherited** - Morphological residuals propagate
4. **Candidates only** - No final resolved case/relation (only candidates)

---

## The Mufrad → Murakkab Boundary

### What Crosses the Boundary

**From Mufrad to Murakkab**:
- `MufradProof` objects (closed individual analyses)
- Rank (form quality)
- Residuals (unresolved morphological questions)
- Surface effects
- Morphological candidates
- Trace

### What Does NOT Cross

**Prohibited**:
- ❌ Meaning (doesn't exist in Mufrad)
- ❌ Semantic roles (not in Mufrad)
- ❌ Murad (not in Mufrad)
- ❌ Final judgments (not in Mufrad)

### Interface: PreSyntaxMufradVector

**Purpose**: Governed interface preventing operators from working on raw tokens

**Contract**: `O_j : PreSyntaxMufradVector^k → CandidateSet`

**NOT**: `O_j : Token^k → CaseEffect` (forbidden)

**Enforcement**:
- Operators cannot access raw text
- Operators cannot access meaning (doesn't exist)
- Operators work on certified form (MufradProof wrapped in PreSyntaxMufradVector)

---

## Relation to Larger Architecture

### Position in 10-Layer Map

```
A0: General Algebra (future concept)
A1: Carrier / Ordered Form ✅
A2: Dal Algebra (contains A3 + A4)
  ├─ A3: Dal-Mufrad ✅ (Phase 0/1)
  └─ A4: Dal-Murakkab 🚧 (Partial)
        ║
        ║ ← Boundary: Form ends, meaning begins
        ↓
A5: Wadh' (future)
A6: Madlul (future)
A7: Dalalah (future)
A8: Usage (future)
A9: Murad (future)
A10: Hukm (future)
```

### Dal-Only Loop Closure

**A3 + A4 = Pre-Semantic Dal Loop**

This loop **closes without semantic input**:
- Input: Raw Arabic text
- Process: Form analysis (individual + compositional)
- Output: Form candidates with rank, residuals, trace
- No semantic linking required
- No meaning understanding required

**After closure**: Results available for A5 (Wadh') to begin licensed semantic linking

---

## Testing Dal-Mufrad and Dal-Murakkab

### Governance Tests (This PR)

**Required tests**:
- `test_dal_mufrad_no_meaning_fields()`
- `test_dal_murakkab_no_meaning_fields()`
- `test_murakkab_does_not_raise_mufrad_rank()`
- `test_murakkab_inherits_mufrad_residuals()`
- `test_murakkab_preserves_mufrad_competitors()`
- `test_presyntax_vector_prevents_raw_token_access()`

### Boundary Violation Detection

**Test Mufrad boundary**:
```python
# ❌ VIOLATION
mufrad_proof.meaning = "writer"
mufrad_proof.murad = "the specific writer mentioned"

# ✅ CORRECT
mufrad_proof.root_candidates = [RootCandidate(letters=("ك","ت","ب"))]
```

**Test Murakkab boundary**:
```python
# ❌ VIOLATION
murakkab_proof.sentence_meaning = "The writer wrote the book"
murakkab_proof.semantic_composition = ...

# ✅ CORRECT
murakkab_proof.relation_candidates = [RelationCandidate(type=ISN)]
```

---

## Future Work

### Completing Dal-Mufrad (A3)

**Remaining**:
- 8-layer candidate implementations
- Graphophonemic candidates
- Syllable candidates
- Pre-morph candidates
- Origin candidates
- Template candidates
- Identity axis candidates
- Directional analysis candidates
- Judgment candidates

### Completing Dal-Murakkab (A4)

**Remaining**:
- `RelationCandidate` (إسناد/تضمين/تقييد candidates)
- `CaseEffectCandidate` (case marking candidates)
- `MurakkabProof` (compositional closure)
- Multi-operator interaction
- Operator precedence/competition
- Case sign resolution logic

### After Dal Closure

**Only after A3 + A4 are stable**:
- A5: Wadh' (signifier-signified linking)
- A6-A10: Semantic/judgment algebras

**Rule**: Do not start semantic linking before Dal-Mufrad and Dal-Murakkab are governed.

---

## Summary

### Dal-Mufrad (A3)

- ✅ **Implemented** (Phase 0/1)
- Individual signifier closure
- Form-only (no meaning)
- Outputs: MufradProof with candidates, rank, residuals

### Dal-Murakkab (A4)

- 🚧 **Partially implemented**
- Compositional structure candidates
- Form-only (no meaning)
- Laws: No rank raising, inherits residuals, preserves competitors
- Outputs: (future) MurakkabProof with relation/case candidates

### Boundary

- **Both are pre-semantic** (dal-only)
- **Both output candidates**, not final decisions
- **Both forbidden from meaning** (enforced by governance tests)
- **Together form closed loop** before semantic linking

---

## Prohibited Claims

After this PR, we **may NOT claim**:

- ❌ "Dal-Mufrad understands meaning"
- ❌ "Dal-Murakkab infers murad"
- ❌ "Dal-Murakkab resolves case effects" (only candidates)
- ❌ "Dal-Murakkab improves mufrad quality"

---

## Allowed Claims

After this PR, we **may claim**:

- ✅ "Dal-Mufrad closes individual signifier form analysis"
- ✅ "Dal-Murakkab composes certified mufrad proofs into structure candidates"
- ✅ "Both are pre-semantic (form-only)"
- ✅ "Together they form a closed dal-only loop"

---

**Document Version**: 1.0
**Created**: 2026-05-20
**Author**: Claude Sonnet 4.5
**PR**: #22 (Documentation only)
**Status**: Position specification - not new implementation
