# Phase 3: Algebraic Morphology — Implementation Summary

## الصرف الجبري لا يحكم بالمعنى، بل يرخص بنية صرفية محفوظة الأثر والرتبة والبقايا

**Status**: ✅ Complete
**PR**: This PR
**Tests**: 33/33 passing
**Regression**: All Phase 0-2 tests passing (63 total)

---

## Core Principles Implemented

### 1. الجذر ليس معنى (ROOT is not meaning)
Root extraction supports ROOT domain claims only, never SEMANTICS or HUKM.

**Proof**: `test_root_extraction_never_emits_semantic_or_hukm_evidence`

```python
result = governed_root_extract("كاتب")
# No semantic.* or hukm.* evidence kinds
for ev in result.evidence:
    assert not ev.kind.startswith("semantic.")
    assert not ev.kind.startswith("hukm.")
```

### 2. الوزن ليس حكماً (Pattern is not judgment)
Pattern matching licenses structure (LICENSED) without claiming semantic meaning.

**Proof**: `test_pattern_match_never_promotes_to_certified_with_residuals`

```python
result = governed_pattern_match("فاعل")
# Stays LICENSED, never CERTIFIED when residuals remain
assert result.rank != Rank.CERTIFIED
assert len(result.residuals) > 0
```

### 3. الاشتقاق ليس دلالة نهائية (Derivation is not final semantics)
Morphological operations emit MORPH_DEEP evidence without claiming meaning.

### 4. الصرف يرخص بنية (Morphology licenses structure)
All operations stay LICENSED when residuals remain; CERTIFIED requires full resolution.

**Proof**: `test_morphology_licenses_structure_not_meaning`

```python
pattern_result = governed_pattern_match(
    "فاعل",
    evidence=(Evidence(kind="pattern.match", source="test:Test:1"),),
)
assert pattern_result.rank == Rank.LICENSED  # Not CERTIFIED
assert len(pattern_result.residuals) > 0     # Residuals present
```

---

## Architecture

### Module Structure

```
src/fvafk/algebra/morphology/
├── __init__.py              # Public API
├── residual_taxonomy.py     # 9 residual kinds + constructors
└── operations.py            # 3 governed operations + wrappers
```

### Residual Taxonomy (9 kinds)

1. **context.absent** — Surrounding tokens needed
2. **lexical.ambiguity** — Multiple valid interpretations
3. **proper_name.possible** — Could be proper noun (علم)
4. **transfer.possible** — Could be loanword (دخيل/معرب)
5. **weak_letter.present** — Weak radicals (و، ي، alif)
6. **affix.aggressive_strip** — Over-zealous affix removal
7. **root.ambiguous** — Multiple root candidates
8. **pattern.collision** — Multiple patterns match
9. **broken_plural.possible** — Could be broken plural (جمع تكسير)

**Proof**: `test_morphology_residual_kinds_canonical_set`

### Governed Operations (3 operations)

#### 1. PatternMatchOperation
- **Bridge**: MORPH_SURFACE → MORPH_SURFACE (identity)
- **Input**: Pattern candidate (e.g., "فاعل")
- **Output**: Result with CANDIDATE/LICENSED rank
- **Residuals**: context.absent, lexical.ambiguity

```python
op = PatternMatchOperation()
carrier = Carrier(domain=Domain.MORPH_SURFACE, value="فاعل")
result = op.run(carrier)
# Result(value="فاعل", rank=CANDIDATE, residuals=(...))
```

#### 2. RootExtractionOperation
- **Bridge**: MORPH_SURFACE → ROOT
- **Input**: Surface form (e.g., "كاتب")
- **Output**: Result with ROOT value
- **Residuals**: context.absent, root.ambiguous, weak_letter.present

```python
op = RootExtractionOperation()
carrier = Carrier(domain=Domain.MORPH_SURFACE, value="كاتب")
result = op.run(carrier)
# Result(value="???", rank=CANDIDATE, residuals=(...))
```

**Proof**: `test_root_extraction_detects_weak_letters`

#### 3. AffixDetectionOperation
- **Bridge**: MORPH_SURFACE → MORPH_SURFACE (identity)
- **Input**: Surface form with affixes
- **Output**: Result with detected affixes
- **Residuals**: affix.aggressive_strip, context.absent

```python
op = AffixDetectionOperation()
carrier = Carrier(domain=Domain.MORPH_SURFACE, value="الكاتب")
result = op.run(carrier)
# Detects "ال" prefix → affix.aggressive_strip residual
```

**Proof**: `test_affix_detection_creates_aggressive_strip_residual`

### Convenience Wrappers

```python
# Pattern matching
result = governed_pattern_match("فاعل", evidence=(...))

# Root extraction
result = governed_root_extract("كاتب", evidence=(...))

# Affix detection
result = governed_affix_detect("الكاتب", evidence=(...))
```

---

## Evidence Integration

Phase 3 operations consume Evidence from Phase 2 adapters:

```python
from fvafk.algebra.adapters import C2bAdapter
from fvafk.algebra.morphology import governed_root_extract

adapter = C2bAdapter()
# Hypothetical: adapter.adapt(root_extraction_result) → Evidence

result = governed_root_extract("كاتب", evidence=evidence_from_adapter)
# Promotes to LICENSED when Evidence present
assert result.rank == Rank.LICENSED
```

**Proof**: `test_evidence_from_adapters_supports_root_claims`

---

## Domain Boundary Enforcement

### No MORPH_SURFACE → SEMANTICS jump

```python
result = governed_pattern_match("فاعل")
for ev in result.evidence:
    assert not ev.kind.startswith("semantic.")
```

**Proof**: `test_morphology_operations_never_claim_semantics`

### No MORPH_DEEP → HUKM jump

```python
result = governed_root_extract("كاتب")
for ev in result.evidence:
    assert not ev.kind.startswith("hukm.")
```

**Proof**: `test_morphology_operations_never_claim_hukm`

---

## Rank Invariants

### 1. LICENSED requires Evidence

```python
# This fails:
Result(value="test", rank=Rank.LICENSED, evidence=())
# ValueError: LICENSED requires at least one Evidence
```

**Proof**: `test_licensed_rank_requires_evidence`

### 2. CERTIFIED forbids residuals

```python
# This fails:
Result(
    value="test",
    rank=Rank.CERTIFIED,
    evidence=(Evidence(...),),
    residuals=(Residual(...),)
)
# ValueError: CERTIFIED cannot have residuals
```

**Proof**: `test_certified_rank_forbids_residuals`

### 3. Fatal Failure forces REFUTED

```python
# This fails:
Result(
    value="test",
    rank=Rank.CANDIDATE,  # Not REFUTED
    failures=(Failure(kind="error", fatal=True),)
)
# ValueError: fatal Failure requires REFUTED rank
```

**Proof**: `test_fatal_failure_forces_refuted`

---

## Test Coverage (33 tests)

### Residual Taxonomy (7 tests)
- ✅ Canonical set (9 residuals)
- ✅ `make_context_absent()`
- ✅ `make_lexical_ambiguity()`
- ✅ `make_weak_letter_present()` with letters
- ✅ `make_affix_aggressive_strip()` with details
- ✅ `make_root_ambiguous()` with candidates
- ✅ `make_pattern_collision()` with patterns

### PatternMatchOperation (6 tests)
- ✅ Returns Result with provenance
- ✅ Stays CANDIDATE without Evidence
- ✅ Never CERTIFIED with residuals
- ✅ Refutes on domain mismatch
- ✅ Convenience wrapper
- ✅ Promotes to LICENSED with Evidence

### RootExtractionOperation (5 tests)
- ✅ Returns Result
- ✅ Never emits semantic/hukm evidence
- ✅ Detects weak letters
- ✅ Promotes to LICENSED with Evidence
- ✅ Bridges MORPH_SURFACE → ROOT

### AffixDetectionOperation (4 tests)
- ✅ Returns Result
- ✅ Creates aggressive_strip residual
- ✅ Detects prefix and suffix
- ✅ Always has context residual

### Evidence Integration (1 test)
- ✅ Evidence from adapters supports ROOT claims

### Domain Boundary Enforcement (2 tests)
- ✅ No SEMANTICS claims
- ✅ No HUKM claims

### Rank Invariants (3 tests)
- ✅ LICENSED requires Evidence
- ✅ CERTIFIED forbids residuals
- ✅ Fatal Failure forces REFUTED

### Regression Tests (4 tests)
- ✅ Phase 0 Rank set unchanged
- ✅ Phase 0 bridge matrix unchanged
- ✅ Phase 2 adapters still available
- ✅ Integration with decision tree

### الصرف الجبري (1 test)
- ✅ Morphology licenses structure, not meaning

---

## Files Changed

### New Files (3)
1. `src/fvafk/algebra/morphology/__init__.py` (85 lines)
2. `src/fvafk/algebra/morphology/residual_taxonomy.py` (220 lines)
3. `src/fvafk/algebra/morphology/operations.py` (360 lines)
4. `tests/test_algebra_morphology_phase3.py` (500+ lines)

### Modified Files (1)
1. `docs/ARABIC_ALGEBRA_ROADMAP.md` — Phase 3 marked complete

### Unchanged Files (Critical)
- ✅ `src/fvafk/c1/` — No changes
- ✅ `src/fvafk/c2a/` — No changes
- ✅ `src/fvafk/c2b/` — No changes
- ✅ `src/fvafk/syntax/` — No changes
- ✅ `src/dal_core/` — No changes
- ✅ `src/fvafk/algebra/core.py` — No changes
- ✅ `src/fvafk/algebra/cpb.py` — No changes
- ✅ `src/fvafk/algebra/policies.py` — No changes
- ✅ `src/fvafk/algebra/arabic_layers.py` — No changes

---

## Exit Criteria ✅

- [x] All 33 Phase 3 tests pass
- [x] Root extraction with Evidence promotes to LICENSED
- [x] Root extraction never CERTIFIED with residuals
- [x] Weak letters create `weak_letter.present` residual
- [x] Aggressive affix stripping creates `affix.aggressive_strip` residual
- [x] Fatal contradiction forces REFUTED
- [x] All Phase 0, 0.5, 1, 2 tests remain green (63 total)
- [x] No MORPH_SURFACE → SEMANTICS jump
- [x] No MORPH_DEEP → HUKM jump
- [x] Morphology operations never emit `semantic.*` evidence
- [x] Morphology operations never emit `hukm.*` evidence
- [x] FVAFK pipeline unchanged
- [x] Bridge matrix unchanged
- [x] Rank set unchanged

---

## What's Next: Phase 4 — Algebraic Syntax

Transform syntax operations from functions to governed operations:
- `ISNADIOperation` (إسنادي) — SYNTAX → SYNTAX
- `TADMINIOperation` (تضميني) — SYNTAX → SYNTAX
- `TAQYIDIOperation` (تقييدي) — SYNTAX → SYNTAX

Each operation:
- Consumes Evidence from `SyntaxAdapter`
- Emits residuals for case/agreement violations
- Never promotes to SEMANTICS or HUKM
- Stays LICENSED when grammatical ambiguity remains

---

**Phase 3 Complete** ✅
**Date**: 2026-05-21
**Tests**: 33/33 passing (100%)
**Regression**: 63/63 passing (100%)
