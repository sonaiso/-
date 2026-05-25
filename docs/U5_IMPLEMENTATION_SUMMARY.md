# U₅ Implementation Summary

## Status

**U₅ FunctionalRoleCarrier: COMPLETE ✅**

Date: 2026-05-25
PR Branch: `claude/complete-true-singular-lafz`

## Achievement

U₅ FunctionalRoleCarrier has been implemented as a complete layer that:

1. **Consumes U₄ lafẓ profiles** (not U₂s syllables)
2. **Opens functional role paths** (verb, noun, particle, pronoun candidates)
3. **Assigns candidates** (NOT certificates)
4. **Preserves constitutional law** (no root, weight, meaning, hukm)

## Execution Layer Progression

```
U₀ Unicode ✅
U₁ Grapheme ✅
U₂p PhoneticProjection ✅
U₂s ArabicSyllable ✅
U₃ BoundaryAndAttachment ✅
U₄ TrueSingularLafẓ ✅
U₅ FunctionalRole ✅ COMPLETE ← NEW
U₆ MabniClosedClass ⏸ (next)
U₇ PreWeightContract ⏸
U₈ RootStem ⏸
U₉ Weight ⏸
```

## Implementation Details

### Core Components

1. **Role Taxonomy** (7 sorts)
   - `CLOSED_CLASS` - Particles (10 candidates)
   - `PRONOUN` - Pronouns (6 candidates)
   - `VERB_CANDIDATE` - Verb surfaces (7 candidates)
   - `NOUN_CANDIDATE` - Noun surfaces (6 candidates)
   - `OPERATOR_CANDIDATE` - Operators (4 candidates)
   - `REFERENCE_CANDIDATE` - Reference carriers (3 candidates)
   - `QUANTITY_CANDIDATE` - Quantity patterns (4 candidates)

2. **Data Structures**
   - `FunctionalRoleCandidate` - Single role with confidence, evidence, trace
   - `FunctionalRoleUnit` - Unit with competing role candidates
   - `FunctionalRoleLayerObject` - Complete U₅ layer
   - `CPB5` - Completeness predicate and proof builder

3. **Role Assignment Logic**
   - `_build_closed_class_candidates()` - From U₄ unit_type (BOUND_PROCLITIC)
   - `_build_pronoun_candidates()` - From U₄ unit_type (ATTACHED_PRONOUN)
   - `_build_verb_candidates()` - From U₄ VerbSurfacePotential
   - `_build_noun_candidates()` - From U₄ Definiteness + Quantity potentials
   - `functional_role_5()` - Main entry point

### Constitutional Guards

**Forbidden Fields** (validated in `__post_init__`):
- ❌ `root` (U₈)
- ❌ `weight` (U₉)
- ❌ `meaning` (U₁₅)
- ❌ `hukm` (U₇+)
- ❌ `iʿrāb` (U₇+)
- ❌ `tense` (U₇+)
- ❌ `voice` (U₇+)

**Allowed Fields**:
- ✅ Role candidate enums
- ✅ Confidence scores
- ✅ Evidence tuples
- ✅ Trace to U₄
- ✅ Residuals
- ✅ Rank (CANDIDATE only)

### Evidence Model

All candidates trace to U₄ potentials:

```python
# Example: Verb candidate
PAST_VERB_SURFACE_CANDIDATE(
    evidence=("u4_past_surface_hint_possible",)
)

# Example: Noun candidate
INDEFINITE_NOUN_CANDIDATE(
    evidence=(
        "u4_indefinite_surface_hint_possible",
        "has_tanwin=True"
    )
)

# Example: Particle candidate
HARF_JARR_CANDIDATE(
    evidence=(
        "surface_match_preposition",
        "surface=بِ"
    )
)
```

## Testing

**20 comprehensive tests**, all passing ✅:

### 1. Prohibition Tests (6 tests)
- ✅ Role candidates are NOT certificates
- ✅ No 'root' field
- ✅ No 'weight' field
- ✅ No 'meaning' field
- ✅ No 'hukm' field
- ✅ CPB₅ completeness validation

### 2. Role Candidate Tests (4 tests)
- ✅ Verb candidates from U₄ potentials
- ✅ Noun candidates from U₄ potentials
- ✅ Closed-class candidates
- ✅ Pronoun candidates

### 3. Golden Cases (3 tests)
- ✅ كَتَبَ → 3 candidates (verb + noun ambiguity)
- ✅ بِكِتَابٍ → 2 units (particle + noun)
- ✅ وَبِكِتَابِهِمْ → 4 units (complex composition)

### 4. Trace and Evidence (2 tests)
- ✅ Preserves trace to U₄
- ✅ Evidence references U₄ potentials

### 5. Execution Tests (2 tests)
- ✅ Runs without errors
- ✅ Handles edge cases

## Files Modified/Created

### Modified
- `src/dal_core/u5_functional_role_carrier.py` (856 lines)
  - Complete rewrite from legacy re-export to full implementation
  - Consumes U₄ `TrueLafzLayerObject`
  - Implements 7 role sorts, 40+ role candidates
  - Full CPB₅ implementation

### Created
- `tests/dal_core/test_u5_functional_role_carrier.py` (603 lines)
  - 20 comprehensive tests
  - Prohibition, role candidate, golden case, trace, execution tests
  - All tests passing

- `docs/U5_FUNCTIONAL_ROLE_CARRIER.md` (525 lines)
  - Complete documentation
  - Constitutional law
  - Role taxonomy
  - Examples (كَتَبَ, بِكِتَابٍ, وَبِكِتَابِهِمْ)
  - Forbidden fields
  - CPB₅ specification

## Example Output

### Input (U₄):
```
كَتَبَ → TrueLafzUnit(
    surface="كَتَبَ",
    unit_type=TRUE_SINGULAR_CORE_CANDIDATE,
    verb_surface_potential=VerbSurfacePotential(
        verb_surface_hint="possible",
        past_surface_hint="possible"
    )
)
```

### Output (U₅):
```
FunctionalRoleUnit(
    surface="كَتَبَ",
    role_candidates=[
        VERB_SURFACE_CANDIDATE (0.6),
        PAST_VERB_SURFACE_CANDIDATE (0.7),
        SINGULAR_NOUN_CANDIDATE (0.6)
    ]
)
```

**Critical**: Multiple candidates present. Disambiguation requires U₆+ evidence.

## Constitutional Compliance

**U₅ Law**:
```
U₅ يفتح مسارات الأدوار الوظيفية.
U₅ لا يشهد بجذر ولا وزن ولا معنى ولا حكم.
U₅ الدور مرشح حتى يُحجب المنافسون.
```

**Verification**:
- ✅ Opens paths (verb, noun, particle, pronoun candidates)
- ✅ No root extraction (validated in tests)
- ✅ No weight determination (validated in tests)
- ✅ No meaning assignment (validated in tests)
- ✅ No hukm judgment (validated in tests)
- ✅ Candidates not certificates (rank=CANDIDATE)

## Next Steps

**U₆ MabniClosedClass** (next layer):
- Consumes U₅ `FunctionalRoleLayerObject`
- Certifies closed-class particles via lexicon match
- Blocks competing candidates for mabni items
- Opens path to U₇ (case/mood analysis)

**Critical Law for U₆**:
```
No MabniCertificate before FunctionalRoleCandidate.
No ClosedClassCertificate before LexiconMatch.
```

## Commit History

1. `a554322` - Implement U₅ FunctionalRoleCarrier consuming U₄ lafẓ profiles
   - Core implementation (856 lines)
   - 7 role sorts, 40+ candidates
   - CPB₅ with constitutional guards

2. `a29dae3` - Add comprehensive U₅ tests and documentation
   - 20 tests (all passing)
   - 525-line documentation
   - Golden cases with examples

## Summary

U₅ FunctionalRoleCarrier is **COMPLETE** and ready for integration.

**Key Achievements**:
1. ✅ Proper layer position (after U₄, before U₆)
2. ✅ Consumes U₄ surface potentials (not syllables)
3. ✅ Opens role paths without certification
4. ✅ Constitutional guards enforced
5. ✅ Comprehensive tests (20/20 passing)
6. ✅ Complete documentation

**Ready for**: U₆ MabniClosedClass implementation

**Blocked by**: None (U₅ is self-contained)

---

**Date**: 2026-05-25
**Status**: ✅ COMPLETE
**Next**: U₆ MabniClosedClass
