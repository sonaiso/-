# U₄ TrueSingularLafẓ Closure Status

**Date**: 2026-05-25
**Status**: ✅ CLOSED
**Commit**: def2e0e

## Summary

U₄ TrueSingularLafẓCarrier is now **CLOSED** over real U₃ BoundaryAndAttachment output.

The layer successfully:
1. Consumes U₃ boundary units
2. Classifies units into lafẓ eligibility types
3. Preserves orthographic surface from U₃
4. Maintains ordered trace preservation
5. Enforces constitutional prohibitions (no root/weight/meaning/hukm/functional_role/iʿrab)
6. Passes all 8 acceptance tests on real Arabic examples

---

## Architecture Position

```
U₀ Unicode ✅
  ↓
U₁ Grapheme ✅
  ↓
U₂p PhoneticProjection ✅
  ↓
U₂s ArabicSyllable ✅
  ↓
U₃ BoundaryAndAttachment ✅
  ↓
U₄ TrueSingularLafẓ ✅  ← NOW CLOSED
  ↓
U₅ FunctionalRole (next)
```

---

## Constitutional Laws Enforced

### Axiom 4.1: True lafẓ ≠ Orthographic compound
U₄ distinguishes between:
- TRUE_SINGULAR_CORE_CANDIDATE (eligible as true lafẓ)
- ORTHOGRAPHIC_COMPOSITE (written together but structurally multiple)

### Axiom 4.2: True lafẓ after boundary separation
U₄ **requires** U₃ boundary detection to be complete first.
Cannot jump directly from U₂s to U₄.

### Axiom 4.3: Lafẓ ≠ Functional role
U₄ does NOT assign functional roles (that's U₅).
Only determines eligibility to be a true singular lafẓ.

### Axiom 4.4: No root in U₄
U₄ MUST NOT contain `root` field (enforced via `__post_init__` validation).

### Axiom 4.5: No weight in U₄
U₄ MUST NOT contain `weight` field (enforced via `__post_init__` validation).

### Axiom 4.6: No meaning in U₄
U₄ MUST NOT contain `meaning` field (enforced via `__post_init__` validation).

### Additional Prohibitions
- No `hukm` (grammatical judgment)
- No `functional_role` (role assignment)
- No `iʿrab` (case/mood marking)

---

## Classification Types

U₄ classifies boundary units into 6 types:

| Type | Arabic Example | Description |
|------|---------------|-------------|
| `TRUE_SINGULAR_CORE_CANDIDATE` | كَتَبَ, كِتَابٌ | Eligible as true singular lafẓ |
| `BOUND_PROCLITIC` | وَ, فَ, بِـ, لِـ, سَـ | Particles attached before core |
| `ATTACHED_ENCLITIC` | Generic enclitic | Generic suffix attachment |
| `ATTACHED_PRONOUN_CANDIDATE` | ـهُ, ـهَا, ـهِمْ | Pronoun enclitics |
| `ORTHOGRAPHIC_COMPOSITE` | Multi-unit compound | Written together, structurally multiple |
| `BLOCKED` | Unresolved | Cannot be determined |

---

## Acceptance Tests (All Passing ✅)

### Test 1: كَتَبَ (Simple Verb)
```
Input: كَتَبَ
Output: 1 unit
  - كَتَبَ → TRUE_SINGULAR_CORE_CANDIDATE
Status: ✅ PASS
```

### Test 2: كَاتِب (Active Participle - No False Split)
```
Input: كَاتِب
Output: 1 unit
  - كَاتِب → TRUE_SINGULAR_CORE_CANDIDATE
Status: ✅ PASS
Critical: كَ NOT split as proclitic
```

### Test 3: مَكْتَب (Noun of Place - No False Prefix)
```
Input: مَكْتَب
Output: 1 unit
  - مَكْتَب → TRUE_SINGULAR_CORE_CANDIDATE
Status: ✅ PASS
Critical: مَ NOT split as prefix
```

### Test 4: بِكِتَابٍ (Preposition + Noun)
```
Input: بِكِتَابٍ
Output: 2 units
  - بِ → BOUND_PROCLITIC
  - كِتَابٍ → TRUE_SINGULAR_CORE_CANDIDATE
Status: ✅ PASS
```

### Test 5: وَبِكِتَابِهِمْ (Conjunction + Preposition + Noun + Pronoun)
```
Input: وَبِكِتَابِهِمْ
Output: 4 units
  - وَ → BOUND_PROCLITIC
  - بِـ → BOUND_PROCLITIC
  - كِتَابِ → TRUE_SINGULAR_CORE_CANDIDATE
  - ـهِمْ → ATTACHED_PRONOUN_CANDIDATE
Status: ✅ PASS
```

### Test 6: فَسَيَكْتُبُونَهَا (Conjunction + Future + Verb + Pronoun)
```
Input: فَسَيَكْتُبُونَهَا
Output: 4 units
  - فَ → BOUND_PROCLITIC
  - سَـ → BOUND_PROCLITIC
  - يَكْتُبُونَ → TRUE_SINGULAR_CORE_CANDIDATE
  - ـهَا → ATTACHED_PRONOUN_CANDIDATE
Status: ✅ PASS
```

### Test 7: No Forbidden Fields
```
Verified: U₄ layer and all units have NO:
  - root
  - weight
  - meaning
  - hukm
  - functional_role
  - iʿrab / i3rab
Status: ✅ PASS
```

### Test 8: ProofObject Forbidden Gates
```
Verified: U₄ ProofObject forbids:
  - root_certificate
  - weight_certificate
  - meaning_certificate
  - hukm_certificate
  - i3rab_certificate
Allowed: functional_role_gate (U₅)
Status: ✅ PASS
```

---

## Implementation Details

### File: `src/dal_core/u4_true_singular_lafz_carrier.py`

**Core Structures:**
- `TrueLafzUnitType` (Enum): 6 classification types
- `TrueLafzUnit` (dataclass): Individual unit classification
- `TrueLafzLayerObject` (dataclass): Layer output
- `TrueLafzResult` (dataclass): Operation result

**Key Function:**
```python
def true_lafz_4(boundary_layer: BoundaryLayerObject) -> TrueLafzResult
```

**Classification Logic:**
- `_classify_boundary_unit()`: Decision tree for unit type classification
- Known proclitics: وَ, فَ, بِ, لِ, كَ, سَ
- Known pronoun enclitics: ـهُ, ـهَا, ـهُمْ, ـهِمْ, ـكَ, ـكِ, ـنَا

**CPB₄ (Completeness Predicate and Proof Builder):**
- Validates completeness
- Builds ProofObject with forbidden gates
- Enforces limitations

### File: `tests/dal_core/test_u4_acceptance.py`

**Test Pipeline:**
```python
U₀ → U₁ → U₂p → U₂s → U₃ → U₄
```

**8 Comprehensive Tests:**
1. `test_kataba_single_core_candidate()`
2. `test_kaatib_no_false_split()`
3. `test_maktab_no_false_prefix()`
4. `test_bikitabin_proclitic_plus_core()`
5. `test_wabikitabihim_full_composite()`
6. `test_fasayaktubunaha_future_verb_composite()`
7. `test_u4_layer_no_forbidden_fields()`
8. `test_u4_proof_forbidden_gates()`

---

## Critical Architectural Laws Proven

### Law 1: Potentiality-Certification Separation
U₄ does NOT directly certify final lafẓ status.
It opens **potential paths** for U₅ FunctionalRole layer.

### Law 2: Orthographic Surface Preservation
U₄ uses `orthographic_surface` from U₃, NOT phonetic reconstruction.
Critical for boundary detection: وَ (orthographic) ≠ /w//a/ (phonetic).

### Law 3: Ordered Trace Preservation
U₄ maintains ordered `trace_3` as Tuple, never frozenset.
Preserves execution order from U₃.

### Law 4: No Premature Commitment
U₄ does NOT commit to:
- Root extraction (U₈)
- Weight/pattern (U₉)
- Meaning (U₁₅)
- Functional role (U₅)

### Law 5: Governed Failures Only
All failures are typed (`LafzFailureType`), traced, and recoverable.
No exceptions thrown for normal flow.

---

## Integration Points

### Input: U₃ BoundaryLayerObject
```python
@dataclass(frozen=True)
class BoundaryLayerObject:
    uid: str
    units: Tuple[BoundaryUnit, ...]
    trace_2s: str
    residuals: FrozenSet[Residual]
    rank: Rank
    proof: Optional[ProofObject]
```

### Output: U₄ TrueLafzLayerObject
```python
@dataclass(frozen=True)
class TrueLafzLayerObject:
    uid: str
    units: Tuple[TrueLafzUnit, ...]
    source_boundary_layer_id: str
    trace_3: Tuple[str, ...]
    residuals: FrozenSet[Residual]
    rank: Rank
    proof: Optional[ProofObject]
```

### Next Layer: U₅ FunctionalRole (Future)
U₄ opens path to U₅ via:
- `allowed_next_gates = {"functional_role_gate"}`
- Preserves eligibility classification for role assignment

---

## What U₄ Does

✅ **U₄ DOES:**
1. Classify boundary units into eligibility types
2. Distinguish bound proclitics (وَ, بِـ) from core candidates
3. Identify attached pronoun candidates (ـهُ, ـهِمْ)
4. Preserve orthographic surface from U₃
5. Maintain ordered trace to U₃
6. Open potential path to U₅ FunctionalRole

❌ **U₄ DOES NOT:**
1. Extract roots (that's U₈)
2. Determine patterns/weights (that's U₉)
3. Assign meanings (that's U₁₅)
4. Make grammatical judgments (hukm)
5. Assign functional roles (that's U₅)
6. Determine iʿrab (case/mood)

---

## Next Steps

With U₄ closed, the execution core now has:

```
✅ U₀ Unicode
✅ U₁ Grapheme
✅ U₂p PhoneticProjection
✅ U₂s ArabicSyllable
✅ U₃ BoundaryAndAttachment
✅ U₄ TrueSingularLafẓ
⏳ U₅ FunctionalRole (next to implement)
⏳ U₆ MabniClosedClass
⏳ U₇ PreWeightContract
⏳ U₈ RootStem
⏳ U₉ Weight
```

**Next Implementation**: U₅ FunctionalRole
- Consumes U₄ true lafẓ eligibility classifications
- Assigns functional role candidates (no final commitment)
- Opens path to U₆ (mabni/muʿrab distinction)

---

## Verification Commands

```bash
# Run all U₄ acceptance tests
PYTHONPATH=/home/runner/work/-/-/src python tests/dal_core/test_u4_acceptance.py

# Expected output:
# ======================================================================
# U₄ True Singular Lafẓ - Acceptance Tests
# ======================================================================
#
# ✓ Test passed: كَتَبَ → 1 TRUE_SINGULAR_CORE_CANDIDATE
# ✓ Test passed: كَاتِب → 1 TRUE_SINGULAR_CORE_CANDIDATE (no false split)
# ✓ Test passed: مَكْتَب → 1 TRUE_SINGULAR_CORE_CANDIDATE (no false prefix)
# ✓ Test passed: بِكِتَابٍ → بِـ (BOUND_PROCLITIC) + كِتَابٍ (TRUE_SINGULAR_CORE_CANDIDATE)
# ✓ Test passed: وَبِكِتَابِهِمْ → وَ + بِـ (BOUND_PROCLITIC) + كِتَابِ (CORE) + ـهِمْ (PRONOUN)
# ✓ Test passed: فَسَيَكْتُبُونَهَا → فَ + سَـ (BOUND_PROCLITIC) + يَكْتُبُونَ (CORE) + ـهَا (PRONOUN)
# ✓ Test passed: U₄ has no forbidden fields (root, weight, meaning, hukm, functional_role, iʿrab)
# ✓ Test passed: U₄ ProofObject correctly forbids direct jumps to U₈/U₉/U₁₅
#
# ======================================================================
# ALL U₄ ACCEPTANCE TESTS PASSED ✓
# ======================================================================
```

---

## Conclusion

**U₄ TrueSingularLafẓCarrier is CLOSED ✅**

All acceptance criteria met:
- ✅ Consumes real U₃ output
- ✅ Classifies all 6 test cases correctly
- ✅ Preserves orthographic surface
- ✅ Maintains ordered trace
- ✅ Enforces constitutional prohibitions
- ✅ No forbidden fields (root/weight/meaning/hukm/functional_role/iʿrab)
- ✅ ProofObject forbids direct jumps to U₈/U₉/U₁₅
- ✅ Opens path to U₅ FunctionalRole only

The execution pipeline U₀→U₁→U₂p→U₂s→U₃→U₄ is now **fully operational** and tested on real Arabic text.

**Ready to proceed to U₅ FunctionalRole implementation.**
