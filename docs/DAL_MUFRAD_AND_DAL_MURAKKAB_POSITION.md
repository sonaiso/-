# Dal-Mufrad and Dal-Murakkab Position

**PR #22**: Two dal-only loops within pre-semantic algebra
**Status**: Architecture positioning (no new implementation)
**Created**: 2026-05-20

---

## Executive Summary

This document defines **two distinct dal-only loops**:

1. **Dal-Mufrad** (A3): Individual signifier closure
2. **Dal-Murakkab** (A4): Compositional signifier structure

Both loops operate **before semantic interpretation** (pre-wadh').

**Critical Principle**:

```text
Dal-Mufrad closes individual forms.
Dal-Murakkab composes closed forms.
Neither creates meaning.
```

---

## Loop 1: Dal-Mufrad (A3)

### Purpose

Close the individual signifier as an **ordered, bounded, internally composed form candidate**.

### Scope

**Single-word signifier analysis** (no composition, no meaning).

### Input

```text
Surface Arabic text (vocalized word)
```

### Output

```text
MufradProof = closed individual signifier with complete morphological evidence
```

### Internal Layers

Dal-Mufrad traverses **8 internal layers** (D0-D7):

```text
D0: Graphophonemic (رسم/صوت)
    ↓
D1: Syllabic (مقطع)
    ↓
D2: Pre-Morph (ما قبل الصرف)
    ↓
D3: Origin (أصل)
    ↓
D4: Template (وزن)
    ↓
D5: Identity Axis (محور الهوية)
    ↓
D6: Directional Analysis (تحليل اتجاهي)
    ↓
D7: Judgment (حكم صرفي)
```

### What Dal-Mufrad Includes

```text
✅ Carrier (حامل) - Unicode → ArabicAtom
✅ Mark (علامة) - Diacritics, vowels, sukun, shadda
✅ Atom (ذرة) - Typed atomic units
✅ Syllable (مقطع) - CV, CVC, CVV, CVVC structures
✅ Pre-Morph (ما قبل الصرف) - Pre-morphological classification
✅ Origin (أصل) - Root, frozen form, functional particle
✅ Template (وزن) - Pattern matching (فَعَلَ، فَاعِل، etc.)
✅ Identity Axes (محاور الهوية) - Ism, Fi'l, Harf classification
✅ Surface Effects (آثار سطحية) - Harakat, tanwin, shadda effects
✅ Form Features (ميزات صورية) - Morphological feature candidates
✅ Rank (رتبة) - Evidence-based rank (ZERO, FORM, QIYAS, SAMA, TAWATUR)
✅ Residuals (بقايا) - Unresolved issues, blockers
✅ Trace (أثر) - Complete transformation history
✅ Competitors (منافسون) - Alternative interpretations
```

### What Dal-Mufrad Does NOT Include

```text
❌ Meaning (معنى) - Semantic interpretation
❌ Semantic Interpretation (تفسير دلالي)
❌ Murad (مراد) - Speaker intent
❌ Syntax Role (دور نحوي) - Mubtada, khabar, fa'il, etc.
❌ Case Effect (إعراب) - Raf', nasb, jarr, jazm
❌ Real-world Reference (مرجع واقعي)
❌ Compositional Meaning
❌ Contextual Disambiguation
```

### MufradProof Contract

```python
@dataclass(frozen=True)
class MufradProof:
    """
    برهان المفرد (MufradProof)

    Composition-ready singular word proof.
    """

    # Core dal form
    typed_dal: TypedDal

    # Morphological analysis
    segmentation: Optional[SegmentationProof]
    stem: Optional[StemProof]
    clitics: List[CliticProof]
    root_candidates: List[RootCandidate]
    wazn_candidates: List[WaznCandidate]

    # Identity axis
    is_ism: bool
    is_fiil: bool
    is_harf: bool

    # Verb features (if fi'l)
    verb_features: Optional[VerbFeatureProof]

    # Noun features (if ism)
    noun_inflection: Optional[NounInflectionClass]

    # Particle features (if harf)
    particle_operator: Optional[ParticleOperatorPotential]

    # Surface effects
    surface_effects: List[SurfaceEffect]

    # Case sign potential (observation, not effect)
    case_sign_potential: Optional[CaseSignPotential]

    # Composition readiness
    composition_readiness: CompositionReadiness

    # Evidence, rank, residuals, trace
    evidence: List[Evidence]
    rank: LughaRank
    residuals: List[Residual]
    trace: dict

    # CRITICAL: NO MEANING FIELDS
    # meaning: FORBIDDEN
    # murad: FORBIDDEN
    # haqiqa_majaz: FORBIDDEN
```

### Key Properties

1. **Ordered**: Every unit has position, boundaries, adjacency relations
2. **Bounded**: Clear start/end boundaries
3. **Traced**: Complete transformation history
4. **Ranked**: Evidence-based rank per claim
5. **Residual-bearing**: Unresolved issues tracked
6. **Competitor-preserving**: Alternative interpretations maintained
7. **Composition-ready**: Can be consumed by Dal-Murakkab

### Closure Conditions

MufradProof is **closed** when:

```python
def is_mufrad_closed(proof: MufradProof) -> bool:
    return (
        proof.typed_dal.attestation.is_arabic and
        proof.typed_dal.dal_type != DalType.AMBIGUOUS and
        not has_blocking_residuals(proof.residuals) and
        proof.composition_readiness.is_ready and
        # CRITICAL: No meaning fields
        not hasattr(proof, 'meaning') and
        not hasattr(proof, 'murad') and
        not hasattr(proof, 'haqiqa_majaz')
    )
```

### Current Implementation

**Status**: ✅ Implemented in `src/dal_core/mufrad_proof.py`

**Tests**: `tests/dal_core/test_mufrad_proof.py`

---

## Loop 2: Dal-Murakkab (A4)

### Purpose

Compose **already-closed MufradProof objects** into governed structure candidates.

### Scope

**Multi-word signifier composition** (pre-semantic).

### Input

```text
List[MufradProof]  (already-closed individual signifiers)
```

### Output

```text
MurakkabProof  (composition structure proof with relation candidates)
```

### Current Chain

Dal-Murakkab currently implements **partial chain** (PR #10-#21):

```text
MufradProof
    ↓
PreSyntaxMufradVector (PR #10)
    ↓
SentenceFrameCandidate (PR #9)
    ↓
CaseSignMatrix (PR #12)
    ↓
OperatorTriggerPotential (PR #14)
    ↓
NahwOperatorRegistry (PR #16)
    ↓
OperatorCandidate (PR #18)
    ↓
(future) RelationCandidate
    ↓
(future) CaseEffectCandidate
    ↓
(future) MurakkabProof
```

### What Dal-Murakkab Includes

```text
✅ MufradProof composition
✅ PreSyntaxMufradVector (governed interface)
✅ SentenceFrameCandidate (frame structure)
✅ CaseSignMatrix (surface case sign observations)
✅ OperatorTriggerPotential (operator activation candidates)
✅ NahwOperatorRegistry (operator catalog)
✅ OperatorCandidate (operator application candidates)
✅ (future) RelationCandidate (ISN, TADMN, TAQYID candidates)
✅ (future) CaseEffectCandidate (case effect candidates)
✅ Compositional boundaries
✅ Compositional trace
✅ Compositional residuals
✅ Competitor preservation
```

### What Dal-Murakkab Does NOT Include

```text
❌ Meaning creation
❌ Semantic interpretation
❌ Murad inference
❌ Real-world reference
❌ Pragmatic inference
❌ Contextual disambiguation (beyond case signs)
❌ Speaker intent
```

### Future MurakkabProof Contract

```python
@dataclass(frozen=True)
class MurakkabProof:
    """
    برهان المركب (MurakkabProof)

    Composition structure proof (dal-only, no meaning).
    """

    # Source mufrad proofs
    mufrad_proofs: List[MufradProof]

    # Composition structure
    sentence_frame: SentenceFrameCandidate

    # Operator application
    operator_candidates: List[OperatorCandidate]
    applied_operators: List[AppliedOperator]

    # Relation structure
    relation_candidates: List[RelationCandidate]

    # Case effects (as structural candidates, not semantic)
    case_effect_candidates: List[CaseEffectCandidate]

    # Compositional boundaries
    composition_boundaries: List[Boundary]

    # Composition trace
    composition_trace: CompositionTrace

    # Evidence, rank, residuals
    evidence: List[Evidence]
    rank: CompositionRank
    residuals: List[Residual]

    # Competitor preservation
    competitors: List['MurakkabProof']

    # CRITICAL: NO MEANING FIELDS
    # meaning: FORBIDDEN
    # murad: FORBIDDEN
    # semantic_interpretation: FORBIDDEN
```

### Critical Laws for Dal-Murakkab

#### Law 1: Murakkab Does NOT Raise Mufrad Rank

```text
rank(MufradProof) ≥ rank(MurakkabProof.mufrad_component)
```

**Principle**: Composition cannot increase attestation rank of individual signifiers.

**Example**:

```text
"كَتَبَ" has TAWATUR rank as individual signifier
"كَتَبَ الوَلَدُ" composition does NOT change "كَتَبَ" rank to higher
```

#### Law 2: Murakkab Inherits Mufrad Residuals

```text
MufradProof.residuals ⊆ MurakkabProof.residuals
```

**Principle**: Unresolved issues in individual signifiers propagate to composition.

**Example**:

```text
If "الوَلَدُ" has AMBIGUOUS_TYPE residual (could be singular or construct state),
Then "كَتَبَ الوَلَدُ" inherits this residual.
```

#### Law 3: Murakkab Preserves Mufrad Competitors

```text
∀ m ∈ MufradProofs: m.competitors preserved in MurakkabProof
```

**Principle**: Alternative interpretations of individual signifiers must be maintained in composition.

**Example**:

```text
If "قَامَ" has competitors [verb, noun],
Then all compositions must preserve both possibilities.
```

#### Law 4: Murakkab Does NOT Create Meaning

```text
MurakkabProof.meaning = FORBIDDEN
```

**Principle**: Compositional structure is **form analysis**, not semantic interpretation.

**Example**:

```text
"كَتَبَ الوَلَدُ" composition structure:
  ✅ Can certify: ISN relation candidate (إسناد)
  ✅ Can certify: Case effect candidate (raf' on الوَلَدُ)
  ❌ Cannot claim: "The boy wrote" (meaning)
  ❌ Cannot claim: "Past action by specific individual" (semantic)
```

#### Law 5: Murakkab Does NOT Infer Murad

```text
MurakkabProof.murad = FORBIDDEN
```

**Principle**: Structure analysis cannot infer speaker intent.

**Example**:

```text
"أَخْرِجُوا" structure:
  ✅ Can certify: Imperative form
  ✅ Can certify: Plural addressee
  ❌ Cannot infer: Command vs. request vs. permission
  ❌ Cannot infer: Speaker authority
```

---

## Relationship Between Mufrad and Murakkab

### Sequential Dependency

```text
Mufrad MUST close before Murakkab begins.
```

**Reason**: Murakkab operates on **closed signifiers** (MufradProof), not raw tokens.

### No Direct Token Consumption

```text
Dal-Murakkab does NOT consume raw tokens.
Dal-Murakkab consumes MufradProof objects.
```

**Governance** (from PR #10):

```text
العامل لا يعمل على token.
العامل لا يعمل على معنى.
العامل يعمل على PreSyntaxMufradVector.
```

### Evidence Inheritance

```text
MurakkabProof.evidence includes:
  - MufradProof.evidence (inherited)
  - Compositional evidence (new)
```

### Rank Independence

```text
rank(MufradProof) ≠ rank(MurakkabProof)
```

**Principle**: Individual attestation rank is independent from compositional rank.

**Example**:

```text
"كَتَبَ" individual rank: TAWATUR (widely attested)
"كَتَبَ الوَلَدُ" compositional rank: QIYAS (licensed composition)
```

### Residual Propagation

```text
MurakkabProof.residuals = MufradProof.residuals ∪ compositional_residuals
```

**Principle**: Composition adds residuals, never removes them.

---

## Current Implementation Status

### ✅ Implemented

**Dal-Mufrad (A3)**:
- ✅ MufradProof contract
- ✅ TypedDal, LughaAttestation, FormCandidate
- ✅ Morphological features (SegmentationProof, StemProof, etc.)
- ✅ Surface effects
- ✅ CaseSignPotential (observation)
- ✅ CompositionReadiness

**Dal-Murakkab (A4) - Partial**:
- ✅ PreSyntaxMufradVector
- ✅ SentenceFrameCandidate
- ✅ CaseSignMatrix
- ✅ OperatorTriggerPotential
- ✅ NahwOperatorRegistry
- ✅ OperatorCandidate

### ❌ Not Yet Implemented

**Dal-Murakkab (A4) - Remaining**:
- ❌ RelationCandidate (ISN, TADMN, TAQYID)
- ❌ CaseEffectCandidate (raf', nasb, jarr, jazm as structural)
- ❌ MurakkabProof (final composition closure)
- ❌ Composition trace algebra
- ❌ Compositional residual algebra
- ❌ Competitor preservation in composition

---

## Integration with Algebra Map

### Position in Architecture

```text
A2: Pre-Semantic Dal Algebra
  ├── A3: Dal-Mufrad ← Individual signifier closure
  └── A4: Dal-Murakkab ← Compositional structure
```

### Pre-Semantic Boundary

```text
A2-A4: Dal-only (NO meaning)
    ↓
A5: Wadh' ← Dal-Madlul boundary (semantic linking begins)
    ↓
A6+: Semantic analysis
```

### No Semantic Authority

```text
Dal-Mufrad authority:   Form closure
Dal-Murakkab authority: Structure closure
Wadh' authority:        Signifier-signified linking
Madlul authority:       Meaning analysis
```

---

## Roadmap Integration

### PR Sequence for Dal Completion

**Dal-Mufrad (Already Implemented)**:
- PR #7: MufradProof contract
- PR #10: PreSyntaxMufradVector (interface to Murakkab)

**Dal-Murakkab (Partially Implemented)**:
- PR #9: SentenceFrameCandidate
- PR #12: CaseSignMatrix
- PR #14: OperatorTriggerPotential
- PR #16: NahwOperatorRegistry
- PR #18: OperatorCandidate

**Dal-Murakkab (Future PRs)**:
- PR #30+: RelationCandidate
- PR #31+: CaseEffectCandidate
- PR #32+: MurakkabProof closure

See `PROJECT_ALGEBRA_ROADMAP.md` for full sequence.

---

## Examples

### Example 1: Single Word (Mufrad Only)

**Input**: "كَتَبَ"

**Dal-Mufrad Process**:

```text
D0: Graphophonemic
  - ك (letter) + َ (fatha)
  - ت (letter) + َ (fatha)
  - ب (letter) + َ (fatha)

D1: Syllabic
  - كَ (CV)
  - تَ (CV)
  - بَ (CV)

D2: Pre-Morph
  - Trilateral candidate

D3: Origin
  - Root candidate: ك-ت-ب

D4: Template
  - Pattern candidate: فَعَلَ

D5: Identity Axis
  - Fi'l (verb) candidate

D6: Directional Analysis
  - Past tense candidate

D7: Judgment
  - Verb, past, active voice

Output: MufradProof with rank TAWATUR
```

**Dal-Mufrad Does NOT**:
- ❌ Claim meaning "to write"
- ❌ Infer semantic action
- ❌ Require subject/object

### Example 2: Composition (Mufrad → Murakkab)

**Input**: ["كَتَبَ", "الوَلَدُ"]

**Step 1: Dal-Mufrad** (for each word)

```text
MufradProof₁: "كَتَبَ" (verb, past)
MufradProof₂: "الوَلَدُ" (noun, definite)
```

**Step 2: Dal-Murakkab**

```text
PreSyntaxMufradVector₁: verb vector
PreSyntaxMufradVector₂: noun vector

SentenceFrameCandidate: [VERB, NOUN]

CaseSignMatrix:
  - "الوَلَدُ" has damma (raf' sign potential)

OperatorTriggerPotential:
  - No explicit operator (IBTIDAA default)

OperatorCandidate:
  - IBTIDAA (sentence-initial default)

(future) RelationCandidate:
  - ISN relation between verb and noun

(future) CaseEffectCandidate:
  - Raf' on "الوَلَدُ" (fa'il candidate)

Output: MurakkabProof with ISN structure
```

**Dal-Murakkab Does NOT**:
- ❌ Claim meaning "The boy wrote"
- ❌ Infer past action by specific individual
- ❌ Assume real-world writing event

---

## Governance Tests Required

```python
def test_mufrad_closure_forbids_meaning():
    """MufradProof must not contain meaning fields"""
    proof = create_mufrad_proof("كَتَبَ")
    assert not hasattr(proof, 'meaning')
    assert not hasattr(proof, 'murad')
    assert not hasattr(proof, 'haqiqa_majaz')

def test_murakkab_inherits_mufrad_residuals():
    """MurakkabProof inherits all MufradProof residuals"""
    mufrad1 = create_mufrad_with_residual("الوَلَدُ", "AMBIGUOUS_TYPE")
    murakkab = compose_murakkab([mufrad1, ...])
    assert "AMBIGUOUS_TYPE" in murakkab.residuals

def test_murakkab_preserves_mufrad_competitors():
    """MurakkabProof preserves MufradProof competitors"""
    mufrad = create_mufrad_with_competitors("قَامَ", ["verb", "noun"])
    murakkab = compose_murakkab([mufrad, ...])
    assert all_competitors_preserved(murakkab)

def test_murakkab_does_not_raise_mufrad_rank():
    """Composition cannot increase individual rank"""
    mufrad = create_mufrad_proof("كَتَبَ", rank=LughaRank.TAWATUR)
    murakkab = compose_murakkab([mufrad, ...])
    assert murakkab.get_mufrad_rank("كَتَبَ") == LughaRank.TAWATUR

def test_murakkab_forbids_meaning():
    """MurakkabProof must not contain meaning fields"""
    murakkab = compose_murakkab([...])
    assert not hasattr(murakkab, 'meaning')
    assert not hasattr(murakkab, 'murad')
```

---

## Allowed Claim After This Document

```text
The project has defined two dal-only loops:
1. Dal-Mufrad (A3): Individual signifier closure
2. Dal-Murakkab (A4): Compositional structure

Both operate pre-semantically and do not infer meaning.
```

## Forbidden Claim After This Document

```text
Dal-Mufrad understands meaning.
Dal-Murakkab produces semantic interpretation.
Composition creates meaning.
Structure analysis infers murad.
```

---

**Version**: 1.0.0
**Status**: Architecture positioning complete
**Implementation**: Mufrad implemented, Murakkab partial
