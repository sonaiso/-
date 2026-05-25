# U₄ Morpheme Carrier - Implementation Summary

## Overview

**U₄ = MorphemeCarrier** - Morpheme/Affix/ClosedClass classification layer

## Problem Statement

Previous architecture jumped from:
- **U₃ (FunctionalRole)** → **D2 (PreMorph)** or directly to **Root/Pattern**

This created a **premature root commitment problem**: functional roles were forced into root interpretations without proper morpheme classification.

## Solution: U₄ Intermediate Layer

U₄ provides a **morpheme classification layer** where functional roles are classified into morpheme types with competing interpretations.

### Architecture Position

```
U₃ (FunctionalRole)  [src/dal_core/u3_functional_roles.py]
  ↓
U₄ (Morpheme)        [THIS LAYER: src/dal_core/u4_morpheme_carrier.py]
  ↓
U₅ (StemRoot)        [NEXT: root/stem distinction]
```

## Core Principle

**MORPHEME ≠ WORD ≠ ROOT**

Same surface form may have multiple morpheme interpretations:

```
بِ may be:
  - حرف جر (preposition)          [ClosedClass]
  - فاء الجذر (root radical)      [RootCandidate]

الـ may be:
  - أداة تعريف (definite article)  [Affix]
  - جزء من الجذر (part of root)   [RootCandidate]

ـهُ may be:
  - ضمير متصل (attached pronoun)  [ClosedClass]
  - علامة (marker)                [Inflectional]
```

## Implementation Components

### 1. Core Structures (`u4_morpheme_carrier.py`)

**Implemented:**
- **6 Morpheme Sorts** (multi-sorted algebra):
  1. `CLOSED_CLASS` - Particles, pronouns (15 types)
  2. `AFFIX` - Prefixes, suffixes, infixes (15 types)
  3. `ROOT_CANDIDATE` - Potential root radicals (8 types)
  4. `STEM` - Stem structures
  5. `INFLECTIONAL` - Gender/number/case markers
  6. `DERIVATIONAL` - Pattern augments

- **MorphemeIdentity**: Unique morpheme identification
- **MorphemeCandidate**: Single morpheme interpretation with rank
- **MorphemeSpan**: Functional unit carrying competing morpheme candidates
- **AttachmentMode**: Affix attachment requirements
- **FeaturePotential**: Feature hints for U₉ (MorphosyntacticFeatures)

**Total:** 38+ distinct morpheme types across 6 sorts

### 2. Morpheme Operations (`u4_operations.py`)

**Implemented Ω₄ operations:**
1. `classify_morpheme`: U₃ RoleSpan → U₄ MorphemeCandidate
2. `merge_morphemes`: M₁ + M₂ → MCompound (e.g., إِنَّ = إِ + نَّ)
3. `attach_affix`: Affix + Host → AttachedMorpheme
4. `promote_morpheme`: Advance rank (candidate → hypothesis → certificate)
5. `demote_morpheme`: Reduce rank
6. `block_morpheme`: Remove candidate from competition
7. `discharge_residual`: Remove resolved residual
8. `preserve_competitors`: Explicitly maintain competing interpretations

**Operation semantics:**
- All operations preserve **Trace₃** (back to U₃)
- All operations respect **blocking residuals**
- All operations document **evidence**
- All operations return **governed results** (no exceptions)

### 3. Rank System

**MorphemeRank** progression:
```
ZERO (0)              - No classification
  ↓
CANDIDATE (1)         - Possible morpheme (from U₃ role)
  ↓
HYPOTHESIS (2)        - Supported by evidence
  ↓
STRONG_HYPOTHESIS (3) - Multiple evidence sources
  ↓
CERTIFICATE (4)       - Lexicon-attested or pattern-confirmed
```

### 4. Completeness Predicate

**CompleteOne₄(morpheme_span)** requires:
1. At least one candidate
2. No blocking residuals
3. Trace to U₃ preserved
4. If affix, has attachment mode defined

## Critical Laws

### Law 1: Morpheme ≠ Word
```python
# Morphemes do not claim POS or syntactic role
assert not hasattr(MorphemeIdentity, 'pos')
assert not hasattr(MorphemeIdentity, 'syntactic_role')
```

### Law 2: Root NOT certified at U₄
```python
# Root candidates require pattern confirmation at U₅
if morpheme.identity.sort == MorphemeSort.ROOT_CANDIDATE:
    assert morpheme.rank != MorphemeRank.CERTIFICATE
```

### Law 3: No semantics at U₄
```python
# No meaning fields in evidence
for ev in morpheme.evidence:
    assert 'meaning' not in ev
    assert 'murad' not in ev
    assert 'dalālah' not in ev
```

### Law 4: Affix attachment
```python
# Affixes must declare attachment requirements
if morpheme.sort == MorphemeSort.AFFIX:
    assert morpheme_span.attachment.requires_host is True
    assert morpheme_span.attachment.host_position is not None
```

### Law 5: Trace preservation
```python
# All morphemes preserve trace to U₃
assert morpheme_span.trace_to_u3 is not None
assert len(morpheme_span.trace_to_u3) > 0
```

## Test Coverage

**18 tests** covering:
1. Basic morpheme classification (closed-class, affix, root candidate)
2. Morpheme operations (merge, attach, promote, block)
3. Completeness predicate
4. Critical law enforcement
5. Competitor preservation

## Next Steps

### U₅ (StemRoot Carrier) will implement:
- Root/Stem distinction
- Weak/Hamzated/Doubled root classification
- Primitive vs Derived stem distinction
- جامد (frozen) vs مشتق (derived) classification
- Pattern hints for U₆

### Integration with existing layers:
- U₃ → U₄ transition gate
- U₄ → U₅ transition evidence requirements
- Lexicon interface preparation for U₈

## Files Created

1. `src/dal_core/u4_morpheme_carrier.py` - Core structures (450 lines)
2. `src/dal_core/u4_operations.py` - Operations (350 lines)
3. `tests/dal_core/test_u4_morpheme_carrier.py` - Test suite (350 lines)
4. `docs/U4_IMPLEMENTATION_SUMMARY.md` - This document

## Compliance

✅ Multi-sorted algebra (6 sorts, no mixing)
✅ Evidence-based rank progression
✅ Trace preservation to U₃
✅ Residual algebra (warnings/blockers)
✅ Governed failures (no exceptions)
✅ Competitor preservation
✅ No premature commitment
✅ No semantic fields
✅ CPB-ready (identity guardian patterns)

---

**PR**: U4-LAYER
**Created**: 2026-05-25
**Status**: Core implementation complete, ready for U₅
