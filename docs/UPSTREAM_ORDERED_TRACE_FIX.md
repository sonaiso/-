# Upstream Ordered Trace Fix - Implementation Summary

**PR**: Fix ordered trace preservation from U₀ through U₂p
**Date**: 2026-05-25
**Status**: ✅ OPERATIONAL (Ordering Fixed)

---

## Problem Discovered

During U₂s testing, مَكْتَب arrived at U₂p with **reversed character ordering**:
```
Expected: م َ ك ْ ت َ ب
Actual:   َ َ ب ك ْ ت م (REVERSED!)
```

This was a **foundational architectural defect** blocking all downstream layers.

## Root Cause

All carrier layers used `FrozenSet` for storage, which **loses ordering**:

```python
# WRONG (old implementation)
@dataclass(frozen=True)
class UnicodeLayerObject:
    units: FrozenSet[UnicodeUnit]  # ❌ Unordered!

@dataclass(frozen=True)
class GraphemeLayerObject:
    clusters: FrozenSet[GraphemeCluster]  # ❌ Unordered!

@dataclass(frozen=True)
class PhoneticProjectionLayerObject:
    projections: FrozenSet[PhoneticProjection]  # ❌ Unordered!
```

**Python frozenset iteration order is arbitrary** - not insertion order.

---

## Solution: Tuple for Ordered Execution Trace

Changed all carrier layers to use `Tuple` for **ordered execution trace**:

### U₀ Unicode Carrier (src/dal_core/u0_unicode_carrier.py)

**Line 145**:
```python
# CORRECT (new implementation)
@dataclass(frozen=True)
class UnicodeLayerObject:
    units: Tuple[UnicodeUnit, ...]  # ✓ Preserves insertion order
    total_residuals: FrozenSet[Residual]
    metadata: Dict[str, Any] = field(default_factory=dict)
```

**Line 465**:
```python
# CRITICAL: Preserve order with tuple (not frozenset)
layer_object = UnicodeLayerObject(
    units=tuple(units),  # ✓ Was frozenset(units) - WRONG
    total_residuals=frozenset(total_residuals),
    ...
)
```

### U₁ Grapheme Carrier (src/dal_core/u1_grapheme_carrier.py)

**Line 139**:
```python
clusters: Tuple[GraphemeCluster, ...]  # ✓ Ordered (was FrozenSet)
```

**Line 543**:
```python
clusters=tuple(clusters),  # ✓ Was frozenset - WRONG
```

### U₂p Phonetic Projection Carrier (src/dal_core/u2p_phonetic_projection.py)

**Line 182**:
```python
projections: Tuple[PhoneticProjection, ...]  # ✓ Ordered (was FrozenSet)
```

**Line 557**:
```python
projections=tuple(projections),  # ✓ Was frozenset - WRONG
```

---

## Test Results

### مَكْتَب Ordering Test

```python
text = "مَكْتَب"

U₀: 7 units (type=tuple) ✓
  0: م (pos=0)
  1: َ (pos=1)
  2: ك (pos=2)
  3: ْ (pos=3)
  4: ت (pos=4)
  5: َ (pos=5)
  6: ب (pos=6)

U₁: 4 clusters (type=tuple) ✓
  0: base=م marks={'َ'}  → مَ
  1: base=ك marks={'ْ'}  → كْ
  2: base=ت marks={'َ'}  → تَ
  3: base=ب marks={}     → ب

U₂p: 4 projections (type=tuple) ✓
  0: C=/m/, V=/a/, closure=False
  1: C=/k/, V=None, closure=True
  2: C=/t/, V=/a/, closure=False
  3: C=/b/, V=None, closure=False
```

**CRITICAL SUCCESS**: Characters appear in correct order!
- U₀: `type=tuple` ✓
- U₁: `type=tuple` ✓
- U₂p: `type=tuple` ✓

---

## Critical Law Enforced

### No FrozenSet for Execution Trace

```python
# LAW: Execution trace must preserve order
units/clusters/projections: Tuple[...]  # AUTHORITATIVE ordered trace
residuals: FrozenSet[...]                # Comparison view (order doesn't matter)
```

**Frozenset is ONLY for comparison views** where order is irrelevant:
- Residuals
- Trace IDs (set membership, not sequence)
- Marks (unordered set of diacritics)

**Tuple is MANDATORY for execution sequences** where order matters:
- Unicode units (character sequence)
- Grapheme clusters (grapheme sequence)
- Phonetic projections (phonetic sequence)
- Syllables (syllable sequence)
- Any carrier layer output

---

## Architecture Impact

### Before Fix

```
Text: مَكْتَب
→ U₀: FrozenSet{...} → arbitrary iteration order
→ U₁: FrozenSet{...} → arbitrary iteration order
→ U₂p: FrozenSet{...} → arbitrary iteration order
→ U₂s: FAILS (broken input)
```

### After Fix

```
Text: مَكْتَب
→ U₀: Tuple(م, َ, ك, ْ, ت, َ, ب) ✓
→ U₁: Tuple(مَ, كْ, تَ, ب) ✓
→ U₂p: Tuple(/m//a/, /k/⁰, /t//a/, /b/) ✓
→ U₂s: Processes ordered input ✓
```

---

## Acceptance Criteria

### ✅ Completed

- [x] U₀ uses Tuple for units (ordered)
- [x] U₁ uses Tuple for clusters (ordered)
- [x] U₂p uses Tuple for projections (ordered)
- [x] Test confirms ordering preserved for مَكْتَب
- [x] No frozenset for execution trace
- [x] Tuple is authoritative for all carrier outputs

### ⏸ Remaining Work

- [ ] U₂s CVC syllabification refinement (partial implementation)
- [ ] Full U₀→U₃ integration tests passing
- [ ] وَبِكِتَابِهِمْ → 4 U₃ boundary units verified

---

## Status Summary

### What This PR Fixed

**✅ CRITICAL BLOCKER RESOLVED**: Upstream ordered trace preservation

The foundational defect (frozenset losing ordering) is **completely fixed**. All layers now use Tuple for ordered execution trace.

### Current State

```
U₀ ✅ operational + ordered trace preserved
U₁ ✅ operational + ordered trace preserved
U₂p ✅ operational + ordered trace preserved
U₂s ✅ improved (ordered_surface added)
U₂s ⚠️ partial (CVC needs refinement based on ordered U₂p input)
U₃ ✅ operational (ready for stable U₂s)
U₄ ⏸ blocked until U₂s→U₃ fully verified
```

### Accurate Status Claim

**DO NOT claim**: "U₂s complete"
**DO claim**: "Upstream ordered trace fixed; U₂s improved with ordered_surface"

---

## Key Learnings

### Python FrozenSet Pitfall

```python
# DANGER: Frozenset loses order
units_list = [unit1, unit2, unit3]
units_frozen = frozenset(units_list)
# Iteration order is ARBITRARY, not insertion order!

# CORRECT: Tuple preserves order
units_tuple = tuple(units_list)
# Iteration order is GUARANTEED insertion order
```

### Architectural Principle

> **Execution trace MUST be ordered.**
> **Frozenset is only for comparison views.**

This is now a **constitutional law** across all carrier layers.

---

## Next Steps

1. Refine U₂s CVC syllabification to work with current U₂p output structure
2. Run full U₀→U₃ integration tests
3. Verify وَبِكِتَابِهِمْ → 4 U₃ units
4. Only then proceed to U₄ TrueSingularLafẓ

---

**Commit**: 122883f
**PR**: claude/fix-u2s-syllabification-issues
**Date**: 2026-05-25
