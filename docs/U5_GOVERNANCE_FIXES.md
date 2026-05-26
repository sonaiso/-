# U₅ Governance Fixes Summary

## PR #102 Review Response

**Status**: Governance fixes applied ✅

Date: 2026-05-25
Reviewer Feedback: REQUEST CHANGES (light governance fixes)

## Changes Applied

### 1. ✅ Renamed `confidence` to `surface_support`

**Why**: `confidence` could be misread as epistemic certificate rather than surface evidence strength.

**Before**:
```python
confidence: float  # [0.0, 1.0]
```

**After**:
```python
surface_support: float  # [0.0, 1.0] - Surface evidence strength, NOT epistemic certificate
```

**Impact**: All builder functions updated, tests updated, documentation updated.

### 2. ✅ Changed CPB5 proof claim from "determined" to "opened"

**Why**: "determined" implies assignment/commitment; "opened" correctly reflects path opening.

**Before**:
```python
claim="U₅ functional role candidates determined"
```

**After**:
```python
claim="U₅ functional role candidate paths opened"
```

**Rationale**: U₅ opens paths, does not determine/assign roles.

### 3. ✅ Added forbidden-field guards to FunctionalRoleUnit

**Why**: Constitutional protection must exist at ALL levels (candidate, unit, layer).

**Added**:
```python
@dataclass(frozen=True)
class FunctionalRoleUnit:
    # ... fields ...

    def __post_init__(self):
        """Validate functional role unit."""
        # No root field allowed
        if hasattr(self, 'root'):
            raise ValueError("FunctionalRoleUnit MUST NOT contain 'root' field")

        # No weight field allowed
        if hasattr(self, 'weight'):
            raise ValueError("FunctionalRoleUnit MUST NOT contain 'weight' field")

        # No meaning field allowed
        if hasattr(self, 'meaning'):
            raise ValueError("FunctionalRoleUnit MUST NOT contain 'meaning' field")

        # No hukm field allowed
        if hasattr(self, 'hukm'):
            raise ValueError("FunctionalRoleUnit MUST NOT contain 'hukm' field")
```

### 4. ✅ Added forbidden-field guards to FunctionalRoleLayerObject

**Why**: Layer-level constitutional protection.

**Added**:
```python
@dataclass(frozen=True)
class FunctionalRoleLayerObject:
    # ... fields ...

    def __post_init__(self):
        """Validate functional role layer object."""
        # No root field allowed
        if hasattr(self, 'root'):
            raise ValueError("FunctionalRoleLayerObject MUST NOT contain 'root' field")

        # No weight field allowed
        if hasattr(self, 'weight'):
            raise ValueError("FunctionalRoleLayerObject MUST NOT contain 'weight' field")

        # No meaning field allowed
        if hasattr(self, 'meaning'):
            raise ValueError("FunctionalRoleLayerObject MUST NOT contain 'meaning' field")

        # No hukm field allowed
        if hasattr(self, 'hukm'):
            raise ValueError("FunctionalRoleLayerObject MUST NOT contain 'hukm' field")
```

### 5. ✅ Added residual when zero role candidates produced

**Why**: "No silent deletion" law - empty candidates must be flagged, not pass silently.

**Added**:
```python
# Check for zero candidates and add residual
unit_residuals = list(lafz_unit.residuals)
if len(all_candidates) == 0:
    # Add warning when no functional role candidates opened
    unit_residuals.append(
        make_warning(
            "no_functional_role_candidates_opened",
            f"No functional role candidates opened for unit: {lafz_unit.surface}"
        )
    )
```

**Effect**: Units with zero candidates now carry explicit warning residual.

## Verification

### Tests: All Passing ✅

```
======================================================================
U₅ FUNCTIONAL ROLE CARRIER TESTS
======================================================================

1. PROHIBITION TESTS
----------------------------------------------------------------------
✓ Test passed: U₅ role candidates are NOT certificates
✓ Test passed: U₅ has no 'root' field
✓ Test passed: U₅ has no 'weight' field
✓ Test passed: U₅ has no 'meaning' field
✓ Test passed: U₅ has no 'hukm' field
✓ Test passed: CPB₅ completeness validation works

2. ROLE CANDIDATE TESTS
----------------------------------------------------------------------
✓ Test passed: U₅ assigns verb candidates from U₄ potentials
✓ Test passed: U₅ assigns noun candidates from U₄ potentials
✓ Test passed: U₅ assigns closed-class candidates
✓ Test passed: U₅ assigns pronoun candidates

3. GOLDEN CASES
----------------------------------------------------------------------
✓ Golden Case 1: كَتَبَ → 3 candidates
✓ Golden Case 2: بِكِتَابٍ
✓ Golden Case 3: وَبِكِتَابِهِمْ → 4 units processed

4. TRACE AND EVIDENCE TESTS
----------------------------------------------------------------------
✓ Test passed: U₅ preserves trace to U₄
✓ Test passed: Role candidates have evidence from U₄

5. EXECUTION TESTS
----------------------------------------------------------------------
✓ Test passed: U₅ runs without errors on 4 cases

======================================================================
ALL U₅ TESTS PASSED ✅
======================================================================
```

### Example Output After Changes

**Input**: كَتَبَ

**Output**:
```
✓ Golden Case 1: كَتَبَ → 3 candidates
  - مرشح فعلي سطحي (surface_support=0.60)
  - فعل ماض سطحي محتمل (surface_support=0.70)
  - مفرد سطحي محتمل (surface_support=0.60)
```

Note: `surface_support` instead of `confidence`.

## Files Modified

1. `src/dal_core/u5_functional_role_carrier.py`
   - Renamed field: `confidence` → `surface_support`
   - Added `__post_init__` to `FunctionalRoleUnit`
   - Added `__post_init__` to `FunctionalRoleLayerObject`
   - Changed CPB5 proof claim
   - Added zero-candidate residual logic
   - Updated all 13 candidate creation sites

2. `tests/dal_core/test_u5_functional_role_carrier.py`
   - Updated test output: `confidence` → `surface_support`

3. `docs/U5_FUNCTIONAL_ROLE_CARRIER.md`
   - Updated all examples with `surface_support`
   - Updated CPB5 documentation
   - Updated usage examples

## Constitutional Compliance

### Before Fixes
- ⚠️ `confidence` could be misread as epistemic certainty
- ⚠️ CPB5 claim said "determined" (assignment language)
- ⚠️ Guards only on `FunctionalRoleCandidate`
- ⚠️ Zero candidates passed silently

### After Fixes
- ✅ `surface_support` clearly indicates surface evidence only
- ✅ CPB5 claim says "paths opened" (correct semantics)
- ✅ Guards on all three levels (Candidate, Unit, Layer)
- ✅ Zero candidates flagged with residual warning

## Reviewer's Specific Concerns Addressed

### Concern 1: `confidence` → `surface_support`
**Status**: ✅ RESOLVED
- Field renamed across entire codebase
- Comment added: "Surface evidence strength, NOT epistemic certificate"
- All usages updated (13 sites)

### Concern 2: CPB5 proof claim
**Status**: ✅ RESOLVED
- Changed from "determined" to "opened"
- Matches U₅ semantics: opening paths, not assigning roles

### Concern 3: Guards on Unit/Layer
**Status**: ✅ RESOLVED
- `FunctionalRoleUnit.__post_init__` added
- `FunctionalRoleLayerObject.__post_init__` added
- Guards against: root, weight, meaning, hukm

### Concern 4: Zero candidates residual
**Status**: ✅ RESOLVED
- Warning residual added when `len(all_candidates) == 0`
- Code: "no_functional_role_candidates_opened"
- Message: "No functional role candidates opened for unit: {surface}"

### Concern 5: GENITIVE_PRONOUN_CANDIDATE
**Status**: ✅ ALREADY ADDRESSED
- Already has residual: `make_warning("genitive_vs_possessive", "Needs context to disambiguate")`
- Surface support: 0.7 (lower than ATTACHED_PRONOUN_CANDIDATE at 0.9)
- Evidence clearly states context-dependency

## Next Steps

1. ✅ All governance fixes applied
2. ✅ All tests passing
3. ✅ Documentation updated
4. Ready for PR approval and merge

## Architectural Status After Fixes

```
U₀ Unicode ✅
U₁ Grapheme ✅
U₂p PhoneticProjection ✅
U₂s ArabicSyllable ✅
U₃ BoundaryAndAttachment ✅
U₄ TrueSingularLafẓ ✅
U₅ FunctionalRole ✅ GOVERNANCE CLOSURE COMPLETE
U₆ MabniClosedClass ⏸ (next)
```

**U₅ Status**: ✅ Implementation complete + ✅ Governance closure complete

---

**Date**: 2026-05-25
**PR**: #102
**Commits**:
- `a554322` - Initial U₅ implementation
- `a29dae3` - Tests and documentation
- `609d8b0` - Governance fixes

**Ready for**: Final review and merge
