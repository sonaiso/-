# U₂s Terminal Closure Policy Implementation

**Date**: 2026-05-25
**Branch**: claude/fix-u2s-syllabification-issues
**Status**: ✅ OPERATIONAL

---

## Problem Statement

After fixing the ordered execution trace (removing `sorted()` and using `Tuple`), U₂s still had a critical gap: **word-final consonants without explicit vowels** were being left as dangling residuals.

### Examples of the Problem

**Before Terminal Closure Policy**:

| Word | U₂s Output | Issue |
|------|-----------|-------|
| كَاتِب | CVV + CV (/k//ā/ + /t//i/) | Final /b/ ignored |
| مَكْتَب | CVC + CV (/m//a//k/ + /t//a/) | Final /b/ ignored |
| بِكِتَابٍ | CV + CV + CVV | Final /b/ ignored |

**Root Cause**: Final consonants (projection with C but no V, no closure) were not consumed by any syllabification rule. They fell through to residuals as "unhandled projections."

---

## Constitutional Law: No Dangling Final Consonant

### Arabic Phonological Reality

In Arabic, word-final consonants exist in two modes:

1. **Waqf (Pause) Mode وقف**: Word pronounced in isolation or at pause
   - Final consonant becomes syllable coda
   - كَاتِب → /kaa.tib/ (CVV.CVC)
   - مَكْتَب → /mak.tab/ (CVC.CVC)

2. **Wasl (Connection) Mode وصل**: Word connected to following word
   - Final consonant may receive case vowel
   - كَاتِبٌ → /kaa.ti.bun/ (CVV.CV.CVC)
   - Requires grammatical context

### Law: No Dangling Final Consonant Without Policy

```
IF projection = final AND C ∧ ¬V ∧ ¬closure
THEN one of:
  1. Attach as coda (waqf policy)
  2. Preserve as TerminalConsonantResidual (wasl/unresolved mode)
  3. NEVER: Silent deletion
```

---

## Solution: Terminal Closure Policy

### Architecture

```
Main Syllabification Loop
  ↓
  [All projections processed]
  ↓
Terminal Closure Policy (Post-Processing)
  ↓
  Check: Is final projection unprocessed C (no V, no closure)?
  ↓
  YES → Apply policy mode:
    - waqf: Attach to previous syllable as coda
    - wasl: Preserve as residual (awaiting context)
    - unresolved: Preserve as residual
  ↓
  NO → Continue
  ↓
Validation & Result
```

### Policy Modes

1. **Waqf (Default)**: `terminal_closure="waqf"`
   - Attach final C as coda to previous syllable
   - Transform patterns: CV→CVC, CVV→CVVC
   - Mark syllable with `BoundaryPolicy.PAUSAL`

2. **Wasl**: `terminal_closure="wasl"` (future)
   - Preserve final C as residual
   - Awaiting grammatical context

3. **Unresolved**: `terminal_closure="unresolved"`
   - Preserve final C as residual
   - No policy decision made

---

## Implementation

### Core Function: `_attach_terminal_coda()`

**Location**: `src/dal_core/u2s_syllable_carrier.py:660-750`

```python
def _attach_terminal_coda(
    base_syllable: ArabicSyllable,
    terminal_proj: PhoneticProjection,
    residuals_list: List[Residual]
) -> Optional[ArabicSyllable]:
    """
    Attach terminal consonant as coda to existing syllable (waqf policy).

    Terminal Closure Policy:
        - Word-final consonant without vowel → attach as coda
        - CV + terminal C → CVC
        - CVV + terminal C → CVVC
        - Preserve trace to terminal projection

    Returns:
        Updated syllable with terminal coda, or None if cannot attach
    """
```

**Pattern Transformations**:

| Base Pattern | + Terminal C | Result | Weight |
|--------------|--------------|--------|---------|
| CV | C | CVC | Heavy |
| CVV | C | CVVC | Super-Heavy |
| CVC | C | ❌ Cannot attach | (would create CCC) |
| CVVC | C | ❌ Cannot attach | (illegal cluster) |

**Arabic Phonotactic Law Enforced**: No triple consonant clusters (no CCC onset/coda)

### Integration Point

**Location**: `src/dal_core/u2s_syllable_carrier.py:366-432`

After main syllabification loop completes:

```python
# ========================================================================
# Terminal Closure Policy (Waqf Mode)
# ========================================================================

terminal_closure_mode = policy.get("terminal_closure", "waqf")

if terminal_closure_mode == "waqf" and len(projections) > 0:
    last_proj = projections[-1]

    # Check if final projection is unprocessed consonant
    if (last_proj.consonant_candidate and
        not last_proj.short_vowel_candidate and
        not last_proj.closure_candidate):

        # Check if already consumed by previous syllable
        consumed_proj_ids = set()
        for syll in syllables:
            consumed_proj_ids.update(syll.trace_2p)

        if last_proj.id not in consumed_proj_ids:
            # Apply waqf policy: attach to previous syllable
            if len(syllables) > 0:
                last_syll = syllables[-1]
                if not last_syll.ordered_coda:
                    updated_syll = _attach_terminal_coda(
                        last_syll, last_proj, residuals_list
                    )
                    if updated_syll:
                        syllables[-1] = updated_syll
```

---

## Test Results

### Critical Cases (All Passing ✓)

| Word | Expected | Actual | Status |
|------|----------|--------|--------|
| كَتَبَ | CV.CV.CV | CV.CV.CV | ✓ PASS |
| كَاتِب | CVV.CVC | CVV.CVC | ✓ PASS (FIXED!) |
| مَكْتَب | CVC.CVC | CVC.CVC | ✓ PASS (FIXED!) |
| بِكِتَابٍ | CV.CV.CVVC | CV.CV.CVVC | ✓ PASS |
| وَبِكِتَابِهِمْ | 6 syllables | CV.CV.CV.CVV.CV.CVC | ✓ PASS |

### Detailed Verification

**كَاتِب** (writer):
```
Before: CVV(/k//ā/) + CV(/t//i/) + dangling /b/
After:  CVV(/k//ā/) + CVC(/t//i//b/ [pausal])
✓ Final /b/ attached as coda
✓ Marked with BoundaryPolicy.PAUSAL
```

**مَكْتَب** (office):
```
Before: CVC(/m//a//k/) + CV(/t//a/) + dangling /b/
After:  CVC(/m//a//k/) + CVC(/t//a//b/ [pausal])
✓ Final /b/ attached as coda
✓ Marked with BoundaryPolicy.PAUSAL
```

**بِكِتَابٍ** (with a book - tanween):
```
Projections: /b/, /k/, /t/, /ā/, /b/ (final)
Result: CV(/b//i/) + CV(/k//i/) + CVVC(/t//ā//b/ [pausal])
✓ Tanween creates long vowel + final coda → CVVC pattern
✓ Final /b/ from tanween attached as coda
```

**وَبِكِتَابِهِمْ** (and with their book):
```
Result: 6 syllables
  CV(/w//a/)
  CV(/b//i/)
  CV(/k//i/)
  CVV(/t//ā/)
  CV(/b//i/)
  CVC(/h//i//m/ [pausal])
✓ Final /m/ (from sukun) attached as coda
```

### Verification Checklist

- [x] All syllables use `tuple` (ordered)
- [x] Terminal consonants attached as coda
- [x] No CC onset violations (all onset_size ≤ 1)
- [x] `ordered_surface` preserves full phonetic string
- [x] Pausal syllables marked with `BoundaryPolicy.PAUSAL`
- [x] No silent deletion of projections
- [x] Trace preservation to terminal projection
- [x] Full U₀→U₃ pipeline operational

---

## Laws Enforced

### 1. No Dangling Final Consonant Without Policy

**Principle**: Every final consonant must be accounted for.

**Implementation**:
```python
if last_proj.consonant_candidate and not consumed:
    # MUST apply policy or preserve residual
    # CANNOT silently ignore
```

### 2. Waqf Policy: Attach as Coda

**Principle**: In word-final/pausal mode, attach final C as coda.

**Transformation**:
- CV + C → CVC (light → heavy)
- CVV + C → CVVC (heavy → super-heavy)

**Constraint**: Only if previous syllable has no coda (Arabic: no CCC)

### 3. Trace Preservation

**Principle**: Terminal syllable must trace to both original and terminal projections.

**Implementation**:
```python
trace_2p=base_syllable.trace_2p.union(frozenset([terminal_proj.id]))
```

### 4. Pausal Marking

**Principle**: Syllables modified by waqf policy must be marked.

**Implementation**:
```python
boundary_policy=BoundaryPolicy.PAUSAL
metadata += (("waqf_policy", "applied"),)
```

---

## Edge Cases

### 1. Final Consonant Already Consumed

**Example**: مَكْ (where final /k/ has sukun - already consumed as CVC coda)

**Handling**:
```python
consumed_proj_ids = set()
for syll in syllables:
    consumed_proj_ids.update(syll.trace_2p)

if last_proj.id not in consumed_proj_ids:
    # Only apply policy if not already consumed
```

### 2. Previous Syllable Has Coda

**Example**: Hypothetical word ending in CVCC pattern

**Handling**:
```python
if not last_syll.ordered_coda:
    # Only attach if no existing coda
else:
    # Preserve as residual (cannot create CCC)
```

### 3. No Previous Syllable

**Example**: Single consonant input (rare edge case)

**Handling**:
```python
if len(syllables) > 0:
    # Attach to previous
else:
    # Preserve as residual
```

---

## Residuals

### Terminal Closure Info Residual

**Type**: `ResidualType.AMBIGUOUS_SYMBOL`
**Severity**: `ResidualSeverity.INFO`
**Message**: `"TerminalClosureWaqf: Attached {consonant} as final coda"`

**Rationale**: This is a **policy decision**, not an error. The residual documents which policy was applied and which consonant was attached.

### Unattached Terminal Consonant

**Type**: `ResidualType.AMBIGUOUS_SYMBOL`
**Severity**: `ResidualSeverity.WARNING`
**Message**: Various (cannot attach, previous has coda, no previous syllable)

**Rationale**: Terminal consonant exists but could not be attached. Preserved for downstream processing.

---

## Bug Fix: `has_blocker()` Method

### Original Bug

**Location**: `src/dal_core/u2s_syllable_carrier.py:179`

**Before**:
```python
def has_blocker(self) -> bool:
    return any(r.type == ResidualType.BLOCKER for r in self.residuals)
```

**Issue**: `ResidualType.BLOCKER` doesn't exist. `BLOCKER` is a **severity level**, not a type.

**After**:
```python
def has_blocker(self) -> bool:
    return any(r.severity == ResidualSeverity.BLOCKER for r in self.residuals)
```

**Impact**: This bug would have caused `AttributeError` in CPB₂s validation. Fixed as part of terminal closure implementation.

---

## Architecture Impact

### Before Terminal Closure Policy

```
U₀ ✅ ordered trace
  ↓
U₁ ✅ ordered trace
  ↓
U₂p ✅ ordered trace
  ↓
U₂s ⚠️ ordered + CVC, but final consonants dangling
  ↓
U₃ ❌ blocked by incomplete U₂s
```

### After Terminal Closure Policy

```
U₀ ✅ ordered trace
  ↓
U₁ ✅ ordered trace
  ↓
U₂p ✅ ordered trace
  ↓
U₂s ✅ ordered + CVC + terminal coda (waqf policy)
  ↓
U₃ ✅ operational (receives complete syllables)
```

---

## Files Changed

### src/dal_core/u2s_syllable_carrier.py

**Changes**:
1. **Line 42**: Added `ResidualSeverity` to imports
2. **Line 179**: Fixed `has_blocker()` method (type → severity)
3. **Lines 366-432**: Added terminal closure policy post-processing
4. **Lines 660-750**: Added `_attach_terminal_coda()` helper function

**Total**: ~190 lines added (policy logic + helper function)

---

## Acceptance Criteria

### Minimal Criteria ✓

- [x] Detect final consonant without vowel/closure
- [x] Attach as coda to previous syllable (waqf mode)
- [x] Mark with BoundaryPolicy.PAUSAL
- [x] Preserve trace to terminal projection
- [x] No silent deletion

### Full Closure Criteria ✓

- [x] كَاتِب → CVV.CVC
- [x] مَكْتَب → CVC.CVC
- [x] بِكِتَابٍ → CV.CV.CVVC (or CVV.CVC)
- [x] وَبِكِتَابِهِمْ → 6 syllables with final CVC
- [x] All onset sizes ≤ 1
- [x] All syllables have ordered_surface
- [x] Full U₀→U₃ integration tests pass

---

## Next Steps

### Immediate

- [x] Terminal closure policy implemented
- [x] All critical tests passing
- [x] Documentation complete
- [ ] Final commit and PR update

### Future Enhancements

1. **Wasl Mode**: Implement `terminal_closure="wasl"` for connected speech
   - Preserve final C as residual awaiting case vowel
   - Requires grammatical context from downstream layers

2. **Case Vowel Integration**: When U₅ (grammatical roles) is operational
   - Terminal C + case vowel → final CV syllable
   - Example: كَاتِبٌ → /kaa.ti.bun/ (CVV.CV.CVC)

3. **Tanween Policy Refinement**:
   - Current: tanween creates CVVC pattern
   - Alternative: Split into CVV + CVC (both valid)
   - Policy decision based on phonological analysis preferences

---

## Conclusion

**Status**: ✅ U₂s TERMINAL CLOSURE POLICY COMPLETE

**Impact**:
- ✅ No dangling final consonants
- ✅ Waqf policy operational (default mode)
- ✅ All critical test cases pass
- ✅ Arabic phonotactic laws enforced (no CCC)
- ✅ Full trace preservation
- ✅ Pausal boundary marking

**Architecture State**:
```
U₀ ✅ operational + ordered trace
U₁ ✅ operational + ordered trace
U₂p ✅ operational + ordered trace
U₂s ✅ operational + ordered trace + CVC + terminal coda ← COMPLETE
U₃ ✅ operational (ready for stable U₂s input)
U₄ ⏸ blocked until U₃ fully verified
```

**Commits**:
- Ordered trace fix: c680ef0
- Terminal closure policy: 7716ea6

**Date**: 2026-05-25
**Branch**: claude/fix-u2s-syllabification-issues
