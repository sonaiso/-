# Sentence Frame Proof Documentation

**برهان إطار الجملة - SentenceFrameProof**

## Overview

The Sentence Frame Proof layer (`SentenceFrameProof`) is the critical architectural step between morphological closure (`MufradProof` → `PreSyntaxMufradVector`) and operator application (`NahwOperatorRegistry`).

**Critical Principle**: This layer transforms `list[PreSyntaxMufradVector]` → `SentenceFrameCandidate`, enabling **structural pattern identification** without operator application or semantic judgment.

## Scientific Foundation

### The Architecture Gap That Required This Layer

After PR #11 closed the PreSyntax gate, the architecture was:

```
MufradProof
  ↓
PreSyntaxMufradVector (governed interface)
  ↓
[??? GAP ???]
  ↓
NahwOperatorRegistry (100 operators)
```

Without `SentenceFrameProof`, there was dangerous temptation to jump directly from vectors to operators:

```python
# ❌ FORBIDDEN: Direct vectors → operators
def parse_vectors(vectors: list[PreSyntaxMufradVector]) -> MurakkabProof:
    if vectors[0].type_id == ParticleTypeID.HARF_NASIKH_INNA:
        return apply_inna_operator(vectors)  # Hallucination!
```

This creates **ungoverned composition** because:
1. No frame structural hypothesis
2. No competition among frame types
3. No systematic pattern matching
4. No governed candidate generation

### The Correct Architecture (After This PR)

```
MufradProof
  ↓
PreSyntaxMufradVector (typed mufrad interface)
  ↓
SentenceFrameCandidate (structural pattern candidate)  ← THIS PR
  ↓
[Future: NahwOperatorRegistry]
  ↓
[Future: OperatorCandidate + RelationCandidate]
  ↓
[Future: MurakkabProof]
```

## Mathematical Formulation

### Frame Identification Contract

Frame builder works on **PreSyntaxMufradVector sequences**, not tokens:

```
FrameBuilder : list[PreSyntaxMufradVector] → list[SentenceFrameCandidate]
```

**NOT**:

```
Parser : list[Token] → SyntaxTree  (FORBIDDEN!)
```

### Frame Type Hypothesis

Each frame candidate represents a **structural hypothesis**:

```
Frame = (type, constituents, rank, residuals, trace)
```

Where:
- `type` ∈ {NOMINAL, VERBAL, PARTICLE_LED, FRAGMENT, UNRESOLVED}
- `constituents` = ordered tuple of PreSyntaxMufradVector
- `rank` = min(constituent ranks) (Theorem 5: Rank Ceiling)
- `residuals` = inherited ∪ frame-specific (Theorem 6: Residual Inheritance)
- `trace` = link to constituent proofs

## Five Frame Types

### 1. NominalFrameCandidate (جملة اسمية مرشحة)

**Pattern**: ISM + ... (potential mubtada + khabar)

**Example**: "الكتابُ جديدٌ"
- Constituents: [الكتابُ (ISM, DAMMA), جديدٌ (ISM, TANWIN)]
- Lead noun index: 0
- **NOT** assigned: mubtada role, khabar role

**Critical**: This identifies a CANDIDATE nominal structure. Operators will later determine:
- Is constituents[0] actually mubtada? (needs absence of governing operator)
- Is constituents[1] actually khabar? (needs agreement/matching)

### 2. VerbalFrameCandidate (جملة فعلية مرشحة)

**Pattern**: FIIL + ... (potential verb + faail + mafool...)

**Example**: "كَتَبَ الطالبُ الدرسَ"
- Constituents: [كَتَبَ (FIIL_MADI), الطالبُ (ISM, DAMMA), الدرسَ (ISM, FATHA)]
- Verb index: 0
- **NOT** assigned: faail role, mafool role

**Critical**: This identifies a CANDIDATE verbal structure. Operators will later determine:
- Is constituents[1] actually faail? (needs verb-subject agreement)
- Is constituents[2] actually mafool? (needs verb valency)

### 3. ParticleLedFrameCandidate (جملة بحرف مرشح)

**Pattern**: HARF + ... (particle + governed elements)

**Example**: "إنَّ الكتابَ جديدٌ"
- Constituents: [إنَّ (HARF_NASIKH_INNA), الكتابَ (ISM, FATHA), جديدٌ (ISM, TANWIN)]
- Particle index: 0
- Operator potential: "NASIKH_INNA"
- **NOT** assigned: ism-inna role, khabar-inna role

**Critical**: This identifies a CANDIDATE particle-led structure. Operators will later determine:
- Does إنَّ govern constituents[1]?
- Does إنَّ cause nasb on constituents[1]?
- Is constituents[2] khabar-inna?

### 4. FragmentFrameCandidate (شبه جملة مرشحة)

**Patterns**:
- Single constituent: "الكتابُ" (noun without predicate)
- Prepositional phrase: "في البيتِ" (HARF_JARR + ISM)
- Incomplete verbal: "كَتَبَ" (verb without required arguments)

**Example**: "في البيتِ"
- Constituents: [في (HARF_JARR), البيتِ (ISM, KASRA)]
- Fragment reason: "prepositional_phrase"

**Critical**: Fragments may be:
- Part of larger sentence (modifier)
- Require additional context
- Have unresolved dependencies

### 5. UnresolvedFrameCandidate (إطار غير محسوم)

**When**: Frame type cannot be confidently determined

**Reasons**:
- Ambiguous constituent types
- Multiple competing interpretations
- Insufficient morphological resolution
- Blocking residuals

**Example**: Ambiguous structure
- Constituents: [??? (type unclear), ...]
- Competing types: [NOMINAL, FRAGMENT]
- Unresolved reason: "ambiguous_constituent_types"

**Critical**: This is **NOT** an error - it's honest admission of uncertainty. Operators may:
- Attempt resolution via governance rules
- Reject based on confidence thresholds

## Theorems Enforced

### Theorem 5: Rank Ceiling

**Statement**: Frame rank cannot exceed minimum constituent rank.

**Formula**:
```
rank(Frame) ≤ min(rank(constituent_i))  for all i
```

**Enforcement**:
- Validated in `SentenceFrameCandidate.__post_init__()`
- Raises `ValueError` if violated
- Tested in `TestRankCeilingTheorem` (3 tests)

**Example**:
```python
noun1 = make_noun_vector(rank=LughaRank.SAMA)      # rank = 3
noun2 = make_noun_vector(rank=LughaRank.QIYAS)     # rank = 2

frame = NominalFrameCandidate(
    constituents=(noun1, noun2),
    frame_rank=LughaRank.QIYAS,  # Must be ≤ 2 ✓
    ...
)

# This would raise ValueError:
# frame_rank=LughaRank.SAMA  # 3 > 2 ✗
```

### Theorem 6: Residual Inheritance

**Statement**: All constituent residuals MUST be inherited by frame.

**Formula**:
```
Residuals(Frame) ⊇ ⋃_i Residuals(constituent_i)
```

**Enforcement**:
- `collect_inherited_residuals()` gathers all constituent residuals
- Frame stores `inherited_residuals` separately from `frame_specific_residuals`
- Tested in `TestResidualInheritance` (2 tests)

**Example**:
```python
residual1 = Residual(type=ROOT_UNRESOLVED, ...)
residual2 = Residual(type=NOT_ATTESTED, ...)

noun1 = make_noun_vector(residuals=(residual1,))
noun2 = make_noun_vector(residuals=(residual2,))

frame = NominalFrameCandidate(
    constituents=(noun1, noun2),
    inherited_residuals=(residual1, residual2),  # Both inherited ✓
    ...
)
```

## Forbidden Fields (Validated at Construction)

All frame types validate that they contain NO:

1. **Semantic fields**:
   - `meaning`, `semantic`, `murad`, `madlul`
   - `haqiqa`, `majaz`, `literal`, `metaphor`

2. **Syntax role fields**:
   - `faail`, `mafool`, `mubtada`, `khabar`
   - `ism_inna`, `khabar_inna`, `ism_kana`, `khabar_kana`

3. **Case effect fields**:
   - `case_effect`, `marfoo_by`, `mansub_by`, `majroor_by`, `majzum_by`

4. **Operator governance fields**:
   - `governed_by_operator`, `operator_id`, `relation_type`

**Validation**: Raises `ValueError` at construction if any forbidden field present.

**Tests**: `TestFrameForbiddenFields` (4 tests)

## Frame Builder Logic

### Construction Strategy

```python
builder = FrameBuilder()
frames = builder.build_frames(constituents)
```

**Steps**:
1. Check if all constituents allow consumption
2. Try verbal frame (FIIL present?)
3. Try particle-led frame (HARF at start?)
4. Try nominal frame (ISM at start, no FIIL?)
5. Try fragment frame (incomplete pattern?)
6. Return all candidates (may compete)

### Multiple Candidates

Frame builder may return **multiple competing candidates**:

```python
# "إنَّ الكتابَ جديدٌ" may generate:
frames = [
    ParticleLedFrameCandidate(particle_index=0),  # إنَّ structure
    NominalFrameCandidate(lead_noun_index=1),     # Underlying nominal
]
```

**Resolution**: Operators will resolve competition based on governance rules.

### Blocked Constituents

If any constituent fails `allows_operator_consumption()`:

```python
frames = [
    UnresolvedFrameCandidate(
        unresolved_reason="constituents_blocked",
        frame_specific_residuals=(COMPOSITION_BLOCKER,),
        ...
    )
]
```

## Usage Examples

### Example 1: Nominal Frame

```python
from dal_core import build_sentence_frames, PreSyntaxMufradVector

# Two nouns: "الكتابُ جديدٌ"
noun1 = PreSyntaxMufradVector(...)  # الكتابُ (ISM, DAMMA)
noun2 = PreSyntaxMufradVector(...)  # جديدٌ (ISM, TANWIN)

frames = build_sentence_frames((noun1, noun2))

# Returns: [NominalFrameCandidate(lead_noun_index=0)]
assert frames[0].frame_type == FrameType.NOMINAL
assert frames[0].constituents == (noun1, noun2)
assert not hasattr(frames[0], 'mubtada')  # NO syntax roles yet
```

### Example 2: Verbal Frame

```python
# Verb + noun: "كَتَبَ الطالبُ"
verb = PreSyntaxMufradVector(...)   # كَتَبَ (FIIL_MADI)
noun = PreSyntaxMufradVector(...)   # الطالبُ (ISM, DAMMA)

frames = build_sentence_frames((verb, noun))

# Returns: [VerbalFrameCandidate(verb_index=0)]
assert frames[0].frame_type == FrameType.VERBAL
assert frames[0].verb_index == 0
assert not hasattr(frames[0], 'faail')  # NO syntax roles yet
```

### Example 3: Particle-Led Frame

```python
# Particle + nouns: "إنَّ الكتابَ جديدٌ"
particle = PreSyntaxMufradVector(...)  # إنَّ (HARF_NASIKH_INNA)
noun1 = PreSyntaxMufradVector(...)     # الكتابَ (ISM, FATHA)
noun2 = PreSyntaxMufradVector(...)     # جديدٌ (ISM, TANWIN)

frames = build_sentence_frames((particle, noun1, noun2))

# May return multiple candidates:
# [ParticleLedFrameCandidate, NominalFrameCandidate (underlying)]
particle_frame = next(f for f in frames if f.frame_type == FrameType.PARTICLE_LED)
assert particle_frame.particle_index == 0
assert not hasattr(particle_frame, 'ism_inna')  # NO syntax roles yet
```

## Test Coverage

**24 tests, all passing**:

1. **Forbidden Fields** (4 tests):
   - No meaning/semantic fields
   - No syntax role fields
   - No case effect fields
   - No operator governance fields

2. **Rank Ceiling Theorem** (3 tests):
   - Frame rank equals min constituent rank
   - Frame rank violation raises error
   - `calculate_frame_rank()` returns minimum

3. **Residual Inheritance** (2 tests):
   - Frame inherits all constituent residuals
   - Frame preserves inherited residuals

4. **Nominal Frame** (2 tests):
   - Requires ISM lead constituent
   - Rejects non-ISM lead

5. **Verbal Frame** (2 tests):
   - Requires FIIL constituent
   - Rejects non-FIIL at verb index

6. **Particle-Led Frame** (2 tests):
   - Requires HARF constituent
   - Rejects non-HARF at particle index

7. **Fragment Frame** (1 test):
   - Single constituent creates fragment

8. **Unresolved Frame** (2 tests):
   - Has competing frame types
   - Requires at least one competing type

9. **Frame Builder** (6 tests):
   - Identifies verbal frame from FIIL + ISM
   - Identifies nominal frame from ISM + ISM
   - Identifies particle-led frame from HARF + ISM
   - Identifies fragment from single constituent
   - Blocks on not-ready constituents
   - Convenience function works

## Architectural Position

### Before This PR

```
PreSyntaxMufradVector (governed mufrad interface)
  ↓
[DANGEROUS GAP]
  ↓
NahwOperatorRegistry (ungoverned jump)
```

### After This PR

```
PreSyntaxMufradVector (governed mufrad interface)
  ↓
SentenceFrameCandidate (structural pattern hypothesis)  ← THIS PR
  ↓
[Next PR: NahwOperatorRegistry]
```

## Next Steps (Future PRs)

### PR #12 (Next): CaseSignMatrix
- Map original signs ↔ substitute signs
- Compatible case effect candidates
- Unresolved sign competition resolution

### PR #13: NahwOperatorRegistry
- 100 operators as registry entries
- Input signatures, blocking conditions
- Source, school (Nabhani-default), rank
- **NO** implementation yet (just registry)

### PR #14: OperatorCandidate + RelationCandidate
- OperatorCandidate (not applied operator)
- RelationCandidate (ISN, TADMN, TAQYID)
- Operator consumes **SentenceFrameCandidate**

### PR #15: CaseEffectCandidate
- CaseEffectCandidate from Operator + Relation + CaseSignMatrix
- **NOT** in MufradProof or Frame (in composition only)

### PR #16: ParseCompetition
- Competitor resolution (frames, operators, relations)
- Tarjih by rank/residuals/evidence
- Unresolved competitors block certificate

### PR #17: MurakkabProof
- Composition closure
- Rank ceiling enforcement
- Residual inheritance
- **NO** semantic/murad/haqiqa_majaz

## Key Distinctions Summary

| Layer | What It Does | What It Does NOT Do |
|-------|--------------|---------------------|
| **MufradProof** | Morphological closure | Composition, operators, case effects |
| **PreSyntaxVector** | Governed mufrad interface | Operators, syntax roles, meanings |
| **SentenceFrame** | Structural pattern candidate | Operator application, role assignment, case effects |
| **[Future] Operators** | Governance rules, role candidates | Definitive parse, semantic meaning |
| **[Future] MurakkabProof** | Composition closure | Semantic meaning, murad, haqiqa/majaz |

## References

- **PR #10**: PreSyntax interface (PreSyntaxMufradVector)
- **PR #11**: Operator consumption gate hardening (4 gates)
- **Problem Statement**: Arabic description of architectural requirements
- **Mathematical Foundation**: x → y₀ → G(x) → arg min E paradigm

---

**Status**: ✅ PR Implementation Complete
**Tests**: 24/24 passing
**Existing Tests**: 30/30 still passing (no regressions)
**Next**: Documentation + PR creation
