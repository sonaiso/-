# PreSyntax Mufrad Interface Documentation

**الواجهة الرقمية قبل التركيب النحوي**

## Overview

The PreSyntax layer provides the **governed numerical interface** between morphological closure (MufradProof) and future syntactic composition (MurakkabProof). This is **PR #10** in the 17-PR roadmap toward full nahw operator implementation.

## Scientific Foundation

### The Fundamental Problem

Without PreSyntax, there's a dangerous temptation to jump directly from tokens to syntax:

```python
# ❌ FORBIDDEN: Direct token → syntax
def parse_sentence(text: str) -> SyntaxTree:
    if text.startswith("إنَّ"):
        return apply_inna_operator(text)  # Hallucination!
```

This creates **ungoverned hallucination** because:
1. No morphological proof
2. No surface effect analysis
3. No rank tracking
4. No residual inheritance

### The Correct Architecture

```
Unicode
  ↓
Carrier → ArabicAtom → OperativeUnit → Syllable
  ↓
DForm → DLugha → DType → DClosed
  ↓
MufradProof (morphological + surface closure)
  ↓
PreSyntaxMufradVector (typed interface)
  ↓
[Future: SentenceFrameProof]
  ↓
[Future: NahwOperatorRegistry]
  ↓
[Future: MurakkabProof]
```

## Mathematical Formulation

### Operator Contract

Operators work on **PreSyntaxMufradVector**, not tokens:

```
O_j : PreSyntaxMufradVector^k → CandidateSet
```

**NOT**:

```
O_j : Token^k → CaseEffect  (FORBIDDEN!)
```

### Type Safety

```python
# ✅ CORRECT: Governed operator
def apply_operator(
    vectors: tuple[PreSyntaxMufradVector, ...],
    operator: NahwOperatorRegistryEntry
) -> OperatorCandidate:
    # Operator sees only:
    # - type_id (operational code)
    # - morph_features (candidates)
    # - surface_effects (observations)
    # - case_sign_potentials (not effects!)
    # - rank, residuals, trace
    pass
```

## Core Components

### 1. PreSyntaxMufradVector

**Purpose**: Typed, non-semantic interface for operator consumption.

**Fields**:
- `mufrad_id`: Unique identifier
- `raw_span`: Position in source text
- `type_value`: Type string (ISM, FIIL, HARF)
- `type_id`: Operational type code (NounTypeID | VerbTypeID | ParticleTypeID)
- `type_rank`: Rank of type determination
- Morphological status (candidates only)
- `surface_effects`: Surface observations
- `case_sign_potentials`: **Potential** signs (NOT case effects!)
- `morph_rank`, `final_rank`: Rank tracking
- `residuals`: Unresolved issues
- `trace_id`: Evidence chain
- `competitors_count`: Unresolved competitions
- `composition_readiness`: Readiness level

**FORBIDDEN Fields** (validated at construction):
- `meaning`, `semantic`, `murad`, `madlul`
- `haqiqa`, `majaz`
- `faail`, `mafool`, `mubtada`, `khabar` (syntax roles)
- `case_effect`, `marfoo_by`, `mansub_by`, `majroor_by`
- `governed_by_operator`

### 2. CaseSignPotential

**Purpose**: Surface case sign observations (NOT grammatical judgments).

**Critical Distinction**:
```python
# ✅ ALLOWED in MufradProof
case_sign_potential = CaseSignPotential(
    observed_surface=FINAL_DAMMA,
    sign_family=ORIGINAL,
    sign_value=DAMMA,
    compatible_case_effects=("rafa_candidate", "building_on_damma_candidate"),
    ...
)

# ❌ FORBIDDEN in MufradProof
case_effect = CaseEffect(
    effect_type=RAFA,
    governed_by=inna_operator,  # NO! Too early!
    ...
)
```

**Sign Families**:
- `ORIGINAL`: damma, fatha, kasra, sukun
- `SUBSTITUTE`: alif, waw, ya, nun deletion, weak letter modifications
- `BUILDING`: Invariant marking (mabni)
- `ESTIMATED`: Hidden/estimated marks
- `UNRESOLVED`: Competing interpretations

**Sign Values** (41 total):
- Original: DAMMA, FATHA, KASRA, SUKUN
- Substitute: ALIF, WAW, YA, NUN_RETAINED, NUN_DELETED, WEAK_LETTER_DELETED, etc.
- Tanwin: TANWIN_DAMM, TANWIN_FATH, TANWIN_KASR
- Estimated: ESTIMATED_DAMMA, ESTIMATED_FATHA, ESTIMATED_KASRA
- Unresolved: UNRESOLVED_SIGN

### 3. Type ID Registry

**Purpose**: Operational codes for operator matching (NOT semantic meanings).

**Principle**:
```
type_id ≠ meaning
type_id = operational key for operator entry
```

**Examples**:
```python
# Noun types (26 types)
NounTypeID.ISM_COMMON           # اسم_جنس
NounTypeID.ISM_PROPER           # اسم_علم
NounTypeID.ISM_DERIVED_ACTIVE_PARTICIPLE  # اسم_فاعل

# Verb types (16 types)
VerbTypeID.FIIL_MADI           # فعل_ماضٍ
VerbTypeID.FIIL_MUDARI         # فعل_مضارع
VerbTypeID.FIIL_MUTADI_TWO     # فعل_متعدٍّ_لمفعولين

# Particle types (22 types)
ParticleTypeID.HARF_JARR       # حرف_جر
ParticleTypeID.HARF_NASB       # حرف_نصب
ParticleTypeID.HARF_NASIKH_INNA  # حرف_ناسخ_إن_وأخواتها
```

Operators check:
```python
if vector.type_id == ParticleTypeID.HARF_NASIKH_INNA:
    # Apply inna operator logic
```

NOT:
```python
if meaning == "inna particle":  # ❌ FORBIDDEN
```

## Usage Example

### From MufradProof to PreSyntaxVector

```python
# 1. Build MufradProof (morphological + surface closure)
mufrad_proof = MufradProof(
    form=...,
    lugha=...,
    type=...,
    segmentation=...,
    stem=...,
    clitics=...,
    surface_effects=(...,),
    case_sign_potentials=(...,),  # NEW in PR #10
    composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
    ...
)

# 2. Export to PreSyntaxVector
vector = mufrad_proof.to_presyntax_vector()

# 3. Vector ready for operator consumption
assert vector.allows_operator_consumption()
assert not hasattr(vector, 'meaning')  # ✓ No semantic leak
assert not hasattr(vector, 'faail')    # ✓ No syntax role leak
assert not hasattr(vector, 'marfoo_by')  # ✓ No case effect leak

# 4. Operator sees only governed interface
operator = NahwOperatorRegistryEntry(...)
candidate = operator.apply(vector)  # Future PR #13+
```

## Theorems Enforced

### Theorem 1: No Operator Before Interface
**Statement**: Operators cannot work on raw tokens, strings, or unproven structures.

**Enforcement**: Type system + runtime validation in OperatorContract.

### Theorem 2: No CaseEffect Before CaseSignPotential
**Statement**: Case effects (marfoo, mansub, majrur) can only appear in composition, never in MufradProof.

**Enforcement**:
- MufradProof allows `case_sign_potentials`
- MufradProof forbids `case_effect` (validated in `__post_init__`)
- CaseEffectCandidate created only in future composition layer (PR #15)

### Theorem 3: Type IDs Are Not Meanings
**Statement**: type_id is an operational code for operator matching, not a semantic classification.

**Enforcement**: Enums in type_ids.py with Arabic operational labels.

### Theorem 4: Readiness Gates Operator Access
**Statement**: Only composition-ready MufradProof may be consumed by operators.

**Enforcement**:
```python
if not vector.allows_operator_consumption():
    raise OperatorOnNotReadyMufradError()
```

### Theorem 5: Rank Ceiling
**Statement**: Composition cannot raise the rank of its constituent MufradProofs.

**Enforcement** (future PR #17):
```python
rank(Murakkab) ≤ min(rank(Mufrad_i))
```

### Theorem 6: Residual Inheritance
**Statement**: All MufradProof residuals must be inherited by composition.

**Enforcement** (future PR #17):
```python
Residuals(Murakkab) ⊇ ⋃_i Residuals(Mufrad_i)
```

## Test Coverage

**17 tests, all passing**:

1. **CaseSignPotential vs CaseEffect** (4 tests)
   - Potentials are observations, not judgments
   - Original signs (damma, fatha, kasra, sukun)
   - Substitute signs (alif, waw, ya, nun)
   - Rejection of judgment names

2. **PreSyntaxVector Leak Prevention** (3 tests)
   - No semantic fields
   - No syntax role fields
   - No case effect fields

3. **Type IDs Are Operational** (3 tests)
   - Noun type IDs are codes
   - Verb type IDs are codes
   - Particle type IDs are codes

4. **Operator Token Rejection** (4 tests)
   - Operators reject raw strings
   - Operators require PreSyntaxVector
   - NOT_READY blocks consumption
   - READY_FOR_COMPOSITION allows consumption

5. **MufradProof Export** (2 tests)
   - to_presyntax_vector() method exists
   - case_sign_potentials field exists

6. **Residual Types** (1 test)
   - Case sign residual types defined

## Roadmap: Next 7 PRs

This is PR #10 of 17. Remaining PreSyntax → MurakkabProof PRs:

### PR #11: SentenceFrameProof ✅ IMPLEMENTED
- ✅ NominalFrameCandidate (جملة اسمية مرشحة)
- ✅ VerbalFrameCandidate (جملة فعلية مرشحة)
- ✅ ParticleLedFrameCandidate (جملة بحرف مرشحة)
- ✅ FragmentFrameCandidate (شبه جملة مرشحة)
- ✅ UnresolvedFrameCandidate (إطار غير محسوم)
- ✅ FrameBuilder: list[PreSyntaxMufradVector] → list[SentenceFrameCandidate]
- ✅ Rank ceiling enforced (Theorem 5)
- ✅ Residual inheritance enforced (Theorem 6)
- ✅ 24/24 tests passing
- See [SENTENCE_FRAME_PROOF.md](SENTENCE_FRAME_PROOF.md) for complete documentation

### PR #12: CaseSignMatrix
- Original/Substitute sign mapping
- Compatible case effect matrix
- Unresolved sign competition

### PR #13: NahwOperatorRegistry
- 100 operators as registry entries
- source, school (Nabhani-default), rank
- input_signature, blocking_conditions
- NO implementation yet (just registry)

### PR #14: OperatorCandidate + RelationCandidate
- OperatorCandidate (not applied operator)
- RelationCandidate (ISN, TADMN, TAQYID)
- Operator consumes SentenceFrameCandidate (not PreSyntaxVector directly)

### PR #15: CaseEffectCandidate
- CaseEffectCandidate from Operator + Relation + CaseSignMatrix
- NOT in MufradProof or Frame (in composition only)

### PR #16: ParseCompetition
- Competitor resolution
- Tarjih by rank/residuals/evidence
- Unresolved competitors block certificate

### PR #17: MurakkabProof
- Composition closure
- Rank ceiling enforcement
- Residual inheritance
- NO semantic/murad/haqiqa_majaz

## Key Distinctions Summary

| Concept | ALLOWED in MufradProof | FORBIDDEN in MufradProof |
|---------|------------------------|--------------------------|
| Surface marks | ✅ SurfaceEffect | ❌ CaseEffect |
| Case signs | ✅ CaseSignPotential | ❌ CaseEffect |
| Type info | ✅ type_id (operational) | ❌ meaning (semantic) |
| Morph features | ✅ candidates | ❌ definitive meanings |
| Syntax | ❌ (future composition) | ❌ faail, mafool, etc. |
| Operators | ❌ (future composition) | ❌ governed_by, marfoo_by |

## References

- Problem Statement: See main task description (Arabic)
- PR #8: MufradProof implementation
- PR #9: Hardening requirements documentation
- Mathematical Foundation: x → y₀ → G(x) → arg min E paradigm

---

**Status**: ✅ PR #10 Complete
**Next**: PR #11 (SentenceFrameProof)
**Tests**: 17/17 passing
**Existing Tests**: 148/148 passing
