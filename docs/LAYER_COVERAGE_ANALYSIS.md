# Layer Coverage Analysis: Generative vs Analytic D_mufrad Scope

**Document Status**: Architectural Clarification
**Created**: 2026-05-20
**Purpose**: Correct the scope understanding of morphological layers 6-10 in D_mufrad

---

## Executive Summary

**Critical Distinction**: Layers 6–10 (pattern expansion, masdar, derivation, inflection, number/gender, residuals) are **NOT outside D_mufrad scope** absolutely.

They are:
- ❌ **Out of scope** as **generative production** (creating new forms)
- ❌ **Out of scope** as **semantic interpretation** (meaning assignment)
- ✅ **In scope** as **analytic form-feature recognition** (classification candidates)

### The Correct Formulation

```text
generation: out of scope
semantic interpretation: out of scope
analytic recognition/classification: in scope
```

This document establishes that D_mufrad must provide **analytic contracts** for recognizing and classifying morphological features at all layers, even though it does not generate new forms or interpret their meanings.

---

## Scope Distinction Table

| Layer | Generative Scope | Semantic Scope | Analytic Scope |
|-------|-----------------|----------------|----------------|
| 6 Pattern Expansion | ❌ Out | ❌ Out | ✅ **In** |
| 7 Masdar | ❌ Out | ❌ Out | ✅ **In** |
| 8 Derivation/Inflection | ❌ Out | ❌ Out | ✅ **In** |
| 9 Number/Gender | ❌ Out | ❌ Out | ✅ **In** |
| 10 Residuals | ❌ Out | ❌ Out | ✅ **In** |

---

## Layer-to-Contract Mapping

### Layer 1: Minimal Carrier
- **Current Status**: Partial / existing contracts in `dal_core`
- **Future Analytic Contract**: `CarrierCandidate` / `MarkCandidate` / `AtomCandidate`
- **Scope**: Normalize carriers, classify atoms, preserve diacritics as candidates

### Layer 2: Syllable
- **Current Status**: Partial implementation
- **Future Analytic Contract**: `SyllableCandidateSet`
- **Scope**: Recognize syllable boundaries, classify syllable types, preserve competing segmentations

### Layer 3: Pre-pattern
- **Current Status**: Implicit / partial
- **Future Analytic Contract**: `PreWeightUnitCandidateSet`
- **Scope**: Recognize pre-pattern units, classify weight components

### Layer 4: Complete Minimal Pattern
- **Current Status**: Partial through `root_candidates` / `wazn_candidates` in `MufradProof`
- **Future Analytic Contract**: `PatternCandidateSet`
- **Scope**: Recognize complete patterns, preserve competing root/wazn hypotheses

### Layer 5: Pattern Identity
- **Current Status**: Partial through status fields in `MufradProof`
- **Future Analytic Contract**: `FormIdentityCandidateSet`
- **Scope**: Classify pattern identity (trilateral, quadrilateral, etc.)

### Layer 6: Pattern Expansion
- **Correct Scope**: ✅ **In D_mufrad as analytic recognition**, ❌ **not generation**
- **Future Analytic Contract**: `AugmentedPatternCandidateSet`
- **Scope**:
  - ✅ Recognize augmented patterns (زيادة)
  - ✅ Classify expansion types
  - ✅ Preserve competing augmentation hypotheses
  - ❌ NOT: Generate all possible augmented forms
  - ❌ NOT: Infer semantic nuances of augmentation

### Layer 7: Masdar
- **Correct Scope**: ✅ **In D_mufrad as analytic recognition**, ❌ **not semantic meaning**
- **Future Analytic Contract**: `MasdarFormCandidateSet`
- **Scope**:
  - ✅ Recognize masdar form patterns (مصدر صريح، مصدر ميمي، مصدر صناعي)
  - ✅ Classify masdar types
  - ✅ Preserve competing masdar hypotheses
  - ❌ NOT: Interpret the meaning of the source/action
  - ❌ NOT: Generate all masdar forms from a root

**Example**:
```text
مَكْتَب = MasdarFormCandidate(type=MASDAR_MIMI, pattern=مَفْعَل)
        ≠ semantic meaning "the place/act of writing"
```

### Layer 8: Derivation / Inflection
- **Correct Scope**: ✅ **In D_mufrad as analytic form-feature recognition**, ❌ **not derivational generation**
- **Future Analytic Contract**: `DerivationFormCandidateSet` / `InflectionFormCandidateSet`
- **Scope**:
  - ✅ Recognize derived forms (اسم فاعل، اسم مفعول، صفة مشبهة، etc.)
  - ✅ Classify derivation patterns
  - ✅ Recognize inflectional features
  - ✅ Preserve competing derivation hypotheses
  - ❌ NOT: Generate all derivatives from a root
  - ❌ NOT: Interpret semantic roles ("the one who performed the action")

**Example**:
```text
كَاتِب = DerivationFormCandidate(type=ISM_FAIL, pattern=فَاعِل)
       ≠ "the one who performed writing" (semantic role)
```

### Layer 9: Number / Gender / Inflection Class
- **Correct Scope**: ✅ **In D_mufrad as form-feature recognition**
- **Future Analytic Contract**: `NumberGenderCandidateSet` / `NounInflectionClassCandidateSet`
- **Scope**:
  - ✅ Recognize number forms (مفرد، مثنى، جمع)
  - ✅ Classify gender markers
  - ✅ Classify inflection classes (صرف، ممنوع من الصرف)
  - ✅ Preserve competing number/gender hypotheses
  - ❌ NOT: Assert real-world quantity ("two entities in reality")
  - ❌ NOT: Generate all plural forms

**Example**:
```text
كَاتِبَانِ = NumberFormCandidate(type=MUTHANNA, base=كَاتِب)
          ≠ "two writers exist in reality" (semantic assertion)
```

### Layer 10: Residuals
- **Correct Scope**: ✅ **Central governance layer** for D_mufrad
- **Future Analytic Contract**: `ResidualClassificationCandidate` + `ResidualAlgebra`
- **Scope**:
  - ✅ Classify residual types (usage flags, morphological irregularities)
  - ✅ Preserve residual traces through composition
  - ✅ Provide residual algebra for propagation
  - ❌ NOT: Interpret figurative meaning (مجاز)
  - ❌ NOT: Perform semantic disambiguation

**Example**:
```text
مجازي = ResidualClassificationCandidate(type=USAGE_FLAG)
      ≠ majaz interpretation or metaphorical meaning
```

---

## What D_mufrad Must NOT Do

D_mufrad operates at the **lexical-sign closure** level. It must **not**:

1. ❌ **Generate all derivatives**: Do not produce all possible derived forms from a root
2. ❌ **Infer meaning**: Do not assign semantic interpretations to forms
3. ❌ **Assert murad**: Do not determine intended meaning (المراد)
4. ❌ **Assign semantic roles**: Do not interpret agent/patient/beneficiary roles
5. ❌ **Apply syntax operators**: Do not apply grammatical operators (إن، كان، etc.)
6. ❌ **Produce RelationCandidate**: Do not establish syntactic relations (إسناد، تضمين، تقييد)
7. ❌ **Produce CaseEffectCandidate**: Do not assign grammatical case effects (رفع، نصب، جر)
8. ❌ **Interpret figurative language**: Do not distinguish حقيقة from مجاز semantically

---

## What D_mufrad Must DO

D_mufrad provides the **foundation for composition** by preserving analytic candidates. It must:

1. ✅ **Preserve form-feature candidates**: Maintain all competing hypotheses for morphological features
2. ✅ **Preserve competitors**: Do not suppress competing analyses prematurely
3. ✅ **Preserve rank ceilings**: Track rank constraints on candidates
4. ✅ **Preserve residuals**: Maintain residual traces for propagation
5. ✅ **Preserve trace**: Record derivation history of candidates
6. ✅ **Expose analytic readiness**: Provide `PreSyntaxMufradVector` interface for composition
7. ✅ **Classify form features**: Recognize and classify morphological patterns without generating or interpreting them
8. ✅ **Maintain candidate algebra**: Provide operations for candidate set manipulation

---

## Current Implementation Status

### Already Implemented in `MufradProof`

The following fields in `MufradProof` (see `docs/DAL_CORE_MUFRAD_PROOF.md`) demonstrate that D_mufrad **already partially covers** these layers as candidates:

```python
@dataclass(frozen=True)
class MufradProof:
    # Layer 4: Pattern
    root_candidates: Tuple[RootCandidate, ...]
    wazn_candidates: Tuple[WaznCandidate, ...]

    # Layer 5: Pattern Identity
    root_status: CandidateStatus
    wazn_status: CandidateStatus

    # Layer 8: Derivation
    derivation_status: CandidateStatus

    # Layer 9: Number/Gender
    number_status: CandidateStatus
    gender_status: CandidateStatus

    # Layer 10: Residuals
    residuals: Tuple[str, ...]
```

### What's Missing: Complete Contracts

These fields exist but lack **complete typed contracts** with:
- Explicit candidate set types
- Set trace structures
- Rank algebra
- Residual algebra
- Candidate propagation rules

---

## Foundation PRs Roadmap

After `OperatorCandidate` (PR #17, #18), **do not start `RelationCandidate` yet**.

### Phase 1: Foundation (F1-F5)

1. **F1: Dal Algebra Signature**
   - Define abstract candidate set operations
   - Establish type signatures for set manipulation

2. **F2: Rank Algebra**
   - Formalize rank operations (ceiling, floor, propagation)
   - Define rank constraint satisfaction

3. **F3: Residual Algebra**
   - Define residual classification taxonomy
   - Establish residual propagation rules
   - Implement residual set operations

4. **F4: CandidateSet Contract**
   - Unified base contract for all candidate sets
   - Standard trace structure
   - Standard set operations interface

5. **F5: Stage-aware NoMeaning Invariant**
   - Formalize prohibition on meaning fields at each stage
   - Compile-time and runtime enforcement mechanisms

### Phase 2: Early-Layer Analytic Contracts (E1-E12)

1. **E1: Carrier/Normalization** → `CarrierCandidateSet`
2. **E2: AtomCandidate** → `AtomCandidateSet`
3. **E3: SyllableCandidate** → `SyllableCandidateSet`
4. **E4: PreWeightUnitCandidate** → `PreWeightUnitCandidateSet`
5. **E5: ZiyadahCandidate** → `ZiyadahCandidateSet`
6. **E6: PatternCandidate** → `PatternCandidateSet`
7. **E7: ExpandedPatternCandidate** → `AugmentedPatternCandidateSet`
8. **E8: FormIdentityCandidate** → `FormIdentityCandidateSet`
9. **E9: MasdarCandidate** → `MasdarFormCandidateSet`
10. **E10: Derivation/InflectionCandidate** → `DerivationFormCandidateSet` / `InflectionFormCandidateSet`
11. **E11: Number/Gender/InflectionClass** → `NumberGenderCandidateSet` / `NounInflectionClassCandidateSet`
12. **E12: ResidualClassificationCandidate** → `ResidualClassificationCandidateSet`

### Phase 3: Composition Layer

Only after Phases 1-2 are complete:
- `RelationCandidate`
- `CaseEffectCandidate`
- Operator application logic

---

## Key Architectural Principle

**Not everything unimplemented is out of scope.**

Some features are:
- ✅ **In scope** (part of D_mufrad's responsibility)
- ⏳ **Not yet implemented** as complete contracts
- 📋 **Planned** in the Foundation PRs roadmap

The distinction is critical:

```text
"Not yet implemented" ≠ "Out of scope"
```

### The Correct Statement

❌ **WRONG**: "Layers 6–8 are beyond D_mufrad scope"

✅ **CORRECT**: "Layers 6–8 are beyond generative and semantic scope, but inside analytic D_mufrad scope as future form-feature candidate contracts."

---

## Examples: Form Recognition vs Meaning

### Example 1: Masdar Mimi

```text
مَكْتَب

❌ WRONG (semantic interpretation):
   "the place where writing happens"

✅ CORRECT (analytic recognition):
   MasdarFormCandidate(
       type=MASDAR_MIMI,
       pattern=مَفْعَل,
       root_candidates=(ك، ت، ب),
       status=CANDIDATE_RECOGNIZED
   )
```

### Example 2: Ism Fa'il

```text
كَاتِب

❌ WRONG (semantic role):
   "the one who performed the action of writing"

✅ CORRECT (analytic recognition):
   DerivationFormCandidate(
       type=ISM_FAIL,
       pattern=فَاعِل,
       root_candidates=(ك، ت، ب),
       status=CANDIDATE_RECOGNIZED
   )
```

### Example 3: Dual Form

```text
كَاتِبَانِ

❌ WRONG (real-world assertion):
   "two writers exist in reality"

✅ CORRECT (analytic recognition):
   NumberFormCandidate(
       type=MUTHANNA,
       base_candidates=(كَاتِب,),
       number_marker=انِ,
       status=CANDIDATE_RECOGNIZED
   )
```

### Example 4: Figurative Usage Flag

```text
مجازي (as residual/flag)

❌ WRONG (semantic interpretation):
   "this is metaphorical meaning, not literal"

✅ CORRECT (analytic classification):
   ResidualClassificationCandidate(
       type=USAGE_FLAG,
       flag="مجازي",
       scope=LEXICAL_ITEM,
       status=CANDIDATE_FLAGGED
   )
```

---

## Compliance Check

Any code, documentation, or design decision must satisfy:

### Prohibition Check
- [ ] Does not generate new forms beyond analysis input?
- [ ] Does not infer semantic meaning?
- [ ] Does not assign semantic roles?
- [ ] Does not interpret figurative language?

### Requirement Check
- [ ] Preserves all competing form-feature candidates?
- [ ] Maintains rank ceilings and residuals?
- [ ] Provides typed candidate sets with trace?
- [ ] Exposes analytic readiness for composition?

---

## References

### Related Documentation
- `docs/DAL_CORE_MUFRAD_PROOF.md` - MufradProof structure with existing candidate fields
- `docs/SPEC_DAL_CORE.md` - D_mufrad specification
- `docs/OPERATOR_TRIGGER_POTENTIAL.md` - Operator trigger layer (post-MufradProof)
- `src/dal_core/operator_candidate.py` - OperatorCandidate implementation (PR #17, #18)

### Key PRs
- PR #17: Add OperatorCandidate layer
- PR #18: Update operator candidate architecture
- PR #19: **This document** - Correct layer coverage analysis

---

## Conclusion

**Layers 6–10 are central to D_mufrad's analytic mission.**

They are not:
- ❌ Generative targets (producing all forms)
- ❌ Semantic targets (interpreting meaning)

They are:
- ✅ **Analytic contracts** (recognizing and classifying form features)
- ✅ **Future implementation targets** in Foundation PRs

The D_mufrad architecture must provide **complete typed candidate contracts** for all morphological layers, preserving competing hypotheses and residual traces, while strictly prohibiting semantic interpretation and generative production.

---

**Document Changelog**:
- 2026-05-20: Initial creation (PR #19) - Correct scope understanding for Layers 6-10
