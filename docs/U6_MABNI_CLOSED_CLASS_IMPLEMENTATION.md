# U₆ Mabni Closed Class Carrier - Implementation Summary

## Status: ✅ COMPLETE AND TESTED

**Date**: 2026-05-26
**Branch**: `claude/update-functional-role-carrier`
**Layer**: U₆ MabniClosedClassCarrier
**Transition**: U₅ (FunctionalRole) → U₆ (MabniClosedClass) → U₇ (PreWeightContract)

---

## Executive Summary

U₆ MabniClosedClassCarrier successfully implemented following PR #102 closure. This layer separates closed-class mabni units (particles, pronouns) from open-class cores (requiring root/weight extraction) without assigning meaning, reference, or grammatical judgments.

---

## Constitutional Laws Enforced

```
U₆ لا يستخرج الجذر.                    (No root extraction)
U₆ لا يحدد الوزن.                       (No weight determination)
U₆ لا يعيّن المعنى.                     (No meaning assignment)
U₆ لا يحل الإحالة.                      (No reference resolution)
U₆ لا يحكم بإعراب ولا بناء.             (No case/mood judgments)
U₆ يفصل المغلق عن المفتوح فقط.          (Separates closed from open class only)
```

**Enforcement Mechanism**:
- Field guards in `__post_init__` (MabniClosedClassCandidate, Unit, Layer)
- CPB₆ proof with explicit forbidden gates
- Path blocking for closed-class units (no root/weight)
- All classifications carry CANDIDATE rank (not CERTIFICATE)

---

## Architecture

### Type System

```python
MabniClosedClassType:
    - CLOSED_CLASS_MABNI_CANDIDATE      # مبني أداة مغلقة
    - ATTACHED_PRONOUN_CLOSED_CLASS     # ضمير متصل مبني
    - DETACHED_PRONOUN_CLOSED_CLASS     # ضمير منفصل مبني
    - OPEN_CLASS_CORE_CANDIDATE         # نواة مفتوحة (للجذر/الوزن)
    - LEXICON_AMBIGUOUS                 # مبهم معجمي
    - BLOCKED                            # محظور

ClosedClassSubtype:
    - HARF_JARR, HARF_ATF, HARF_NASB, ... (particles)
    - PRONOUN_ATTACHED, PRONOUN_DETACHED
    - DEMONSTRATIVE, RELATIVE, INTERROGATIVE_NOUN, ...
```

### Data Structures

```python
@dataclass(frozen=True)
class MabniClosedClassCandidate:
    uid: str
    mabni_type: MabniClosedClassType
    subtype: Optional[ClosedClassSubtype]
    lexicon_support: float  # [0.0, 1.0] NOT semantic certainty
    evidence: Tuple[str, ...]
    source_u5_unit_id: str
    mabni_entry: Optional[MabniEntry]  # From MabniRegistry
    residuals: FrozenSet[Residual]
    rank: Rank

    # FORBIDDEN: root, weight, meaning, hukm, resolved_reference

@dataclass(frozen=True)
class MabniClosedClassUnit:
    uid: str
    surface: str
    source_functional_role_unit_id: str
    trace_5: Tuple[str, ...]
    mabni_classification: MabniClosedClassCandidate
    blocked_paths: Tuple[str, ...]  # e.g., ["root_extraction", "weight_determination"]
    evidence: Tuple[str, ...]
    residuals: FrozenSet[Residual]
    rank: Rank
```

### Integration with MabniRegistry

U₆ leverages existing `MabniRegistry` (immutable, closed lexicon):

1. **Lookup**: `registry.lookup(surface)` → returns `Tuple[MabniEntry, ...]`
2. **Categories**: Pronouns, demonstratives, relatives, interrogatives, conditionals, adverbs, names-of-verb, compound numbers
3. **Evidence**: Lexicon match provides strong evidence (0.9 for unique, 0.7 for ambiguous)
4. **Fallback**: `KNOWN_SIMPLE_PARTICLES` dict for common particles (وَ، فَ، بِ، لِ، سَ)

---

## Classification Logic

### Decision Tree

```
1. Check MabniRegistry for exact match
   - Found → CLOSED_CLASS_MABNI_CANDIDATE (with subtype from category)

2. Check KNOWN_SIMPLE_PARTICLES
   - Found → CLOSED_CLASS_MABNI_CANDIDATE (with subtype)

3. Check U₅ role candidates
   - Pronoun role → ATTACHED/DETACHED_PRONOUN_CLOSED_CLASS
   - Closed-class role → CLOSED_CLASS_MABNI_CANDIDATE

4. Default
   - No closed-class evidence → OPEN_CLASS_CORE_CANDIDATE (for U₇+ root/weight)
```

### Path Blocking

**Closed-class units**:
```python
blocked_paths = ["root_extraction", "weight_determination"]
```

**Open-class units**:
```python
blocked_paths = []  # Empty - REQUIRES root/weight path
evidence += ["requires_root_weight_path"]
```

---

## Golden Cases

### Case 1: وَبِكِتَابِهِمْ

**Input** (from U₅):
```
وَ  → HARF_ATF_CANDIDATE
بِ  → HARF_JARR_CANDIDATE
كِتَابِ → DEFINITE_NOUN_CANDIDATE
ـهِمْ → ATTACHED_PRONOUN_CANDIDATE
```

**Output** (U₆ classification):
```
وَ  → CLOSED_CLASS_MABNI_CANDIDATE (HARF_ATF)
     blocked_paths: [root_extraction, weight_determination]

بِ  → CLOSED_CLASS_MABNI_CANDIDATE (HARF_JARR)
     blocked_paths: [root_extraction, weight_determination]

كِتَابِ → OPEN_CLASS_CORE_CANDIDATE
         blocked_paths: []
         evidence: [requires_root_weight_path]

ـهِمْ → ATTACHED_PRONOUN_CLOSED_CLASS (PRONOUN_ATTACHED)
       blocked_paths: [root_extraction, weight_determination]
```

**Architectural significance**:
- Closed-class (وَ، بِ، ـهِمْ) → do NOT proceed to U₈ root extraction
- Open-class (كِتَابِ) → MUST proceed to U₈ root extraction
- This separation is CRITICAL for preventing root extraction on particles/pronouns

---

## Test Coverage (20/20 Passing)

### 1. Constitutional Prohibition Tests (6/6)
✅ No 'root' field
✅ No 'weight' field
✅ No 'meaning' field
✅ No 'hukm' field
✅ No 'resolved_reference' field
✅ CPB₆ completeness validation

### 2. Closed-Class Identification (3/3)
✅ Conjunction وَ → CLOSED_CLASS (HARF_ATF)
✅ Preposition بِ → CLOSED_CLASS (HARF_JARR)
✅ Attached pronoun ـهِمْ → ATTACHED_PRONOUN_CLOSED_CLASS

### 3. Open-Class Identification (1/1)
✅ Noun كِتَابٍ → OPEN_CLASS_CORE_CANDIDATE

### 4. Path Blocking (2/2)
✅ Closed-class blocks root extraction path
✅ Open-class requires root extraction path

### 5. Golden Cases (2/2)
✅ Full composition وَبِكِتَابِهِمْ → 4 units correctly classified
✅ Path blocking verified (closed blocks, open requires)

### 6. Trace and Evidence (2/2)
✅ Trace preservation to U₅
✅ Evidence propagation from U₅ and lexicon

### 7. Execution (2/2)
✅ Execution without errors
✅ Empty input handling

### 8. CPB₆ Proof (2/2)
✅ Proof structure valid
✅ Proof limitations declared

---

## Files Created

### Implementation
- **`src/dal_core/u6_mabni_closed_class_carrier.py`** (858 lines)
  - MabniClosedClassType, ClosedClassSubtype enums
  - Core data structures (Candidate, Unit, Layer)
  - CPB₆ completeness predicate
  - Classification logic with MabniRegistry integration
  - `mabni_closed_class_6()` operation

### Tests
- **`tests/dal_core/test_u6_mabni_closed_class_carrier.py`** (738 lines)
  - 20 comprehensive test cases
  - All tests passing
  - Coverage: prohibitions, identification, path blocking, golden cases

### Documentation
- **`docs/U6_MABNI_CLOSED_CLASS_IMPLEMENTATION.md`** (this file)

---

## Architecture Status After U₆

```
U₀ Unicode               ✅ COMPLETE
U₁ Grapheme              ✅ COMPLETE
U₂p PhoneticProjection   ✅ COMPLETE
U₂s ArabicSyllable       ✅ COMPLETE
U₃ BoundaryAndAttachment ✅ COMPLETE
U₄ TrueSingularLafẓ      ✅ COMPLETE
U₅ FunctionalRole        ✅ COMPLETE
U₆ MabniClosedClass      ✅ COMPLETE + TESTED ✅
U₇ PreWeightContract     ⏸ (next layer)
U₈ RootStem              ⏸ (future)
U₉ Weight                ⏸ (future)
```

---

## Next Steps

### Immediate
- [x] U₆ implementation complete
- [x] U₆ tests complete (20/20 passing)
- [x] Documentation complete
- [ ] Create PR for review

### U₇ PreWeightContract (Next Layer)
**Purpose**: Apply pre-weight contracts (transitional logic before root/weight)

**Responsibilities**:
- Open-class units proceed to root extraction
- Closed-class units bypass root/weight
- Contract enforcement (no forbidden transitions)
- Evidence accumulation

**Does NOT**:
- Extract roots (U₈)
- Determine weights (U₉)
- Assign meanings (U₁₅)
- Make grammatical judgments (U₇+)

---

## Integration Points

### Consumes
- **U₅ FunctionalRoleLayerObject**
  - role_candidates: Tuple[FunctionalRoleCandidate, ...]
  - Uses RoleSort (CLOSED_CLASS, PRONOUN, NOUN_CANDIDATE, VERB_CANDIDATE)

### Produces
- **U₆ MabniClosedClassLayerObject**
  - units: Tuple[MabniClosedClassUnit, ...]
  - Each unit has mabni_classification and blocked_paths

### Uses
- **MabniRegistry** (dal_core.mabni_registry)
  - Immutable, closed lexicon of mabni nouns
  - 9 categories × multiple entries
  - O(1) lookup via form index

### Feeds
- **U₇ PreWeightContract** (future)
  - Open-class units → proceed to root/weight
  - Closed-class units → bypass root/weight

---

## Approval Checklist

- [x] All constitutional laws enforced
- [x] All 20 tests passing
- [x] No forbidden fields (root, weight, meaning, hukm)
- [x] Path blocking correctly implemented
- [x] MabniRegistry integration working
- [x] Trace preservation verified
- [x] Evidence propagation verified
- [x] CPB₆ proof structure valid
- [x] Documentation complete
- [x] Golden cases verified

---

**Prepared by**: Claude (Anthropic)
**Date**: 2026-05-26
**Layer**: U₆ MabniClosedClassCarrier
**Status**: ✅ READY FOR REVIEW
