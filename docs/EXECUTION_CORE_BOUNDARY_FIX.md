# Execution Core Boundary Fix

## Problem Statement

**Arabic (Original)**:
```
U₀–U₉ = execution core.
U₁₀–U₁₅ = future design layers, not closed execution layers.
الوثائق تقول U₀–U₉.
الكود يسمح بقراءة U₀–U₁₅ كسلسلة تنفيذية.
```

**English Translation**:
- U₀–U₉ = execution core
- U₁₀–U₁₅ = future design layers, not closed execution layers
- The documentation says U₀–U₉
- The code allows reading U₀–U₁₅ as an execution chain

## Root Cause

The `execution_layer_registry.py` module had architectural ambiguity:

1. **Documentation** (module docstring): Stated "Canonical U₀-U₉ Order" indicating execution core is U₀–U₉
2. **Code implementation**: Included all layers U₀–U₁₅ in `EXECUTION_LAYER_ORDER` and `ALLOWED_TRANSITIONS` as a continuous execution chain

This created confusion about which layers are operational (closed execution core) vs. which are architectural placeholders (future design).

## Solution

### 1. Code Changes (`src/dal_core/execution_layer_registry.py`)

**Added explicit separation**:

```python
# Execution Core Layers (U₀-U₉): Closed, implemented, operational
EXECUTION_CORE_LAYERS = [
    ExecutionLayer.U0_UNICODE,
    ExecutionLayer.U1_GRAPHEME,
    ExecutionLayer.U2P_PHONETIC_PROJECTION,
    ExecutionLayer.U2S_ARABIC_SYLLABLE,
    ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
    ExecutionLayer.U4_TRUE_SINGULAR_LAFZ,
    ExecutionLayer.U5_FUNCTIONAL_ROLE,
    ExecutionLayer.U6_MABNI_CLOSED_CLASS,
    ExecutionLayer.U7_PRE_WEIGHT_CONTRACT,
    ExecutionLayer.U8_ROOT_STEM,
    ExecutionLayer.U9_WEIGHT,
]

# Design Layers (U₁₀-U₁₅): Future design, not closed execution layers
DESIGN_LAYERS = [
    ExecutionLayer.U10_WORD_FORM,
    ExecutionLayer.U11_LEXICAL_ENTRY,
    ExecutionLayer.U12_MORPHOSYNTACTIC_FEATURE,
    ExecutionLayer.U13_PHRASE_RELATION,
    ExecutionLayer.U14_SENTENCE_STRUCTURE,
    ExecutionLayer.U15_DALALAH,
]

# Complete layer order (for reference and tooling)
EXECUTION_LAYER_ORDER = EXECUTION_CORE_LAYERS + DESIGN_LAYERS
```

**Split transitions**:

```python
# Core execution layer transitions (U₀-U₉) - Operational
CORE_ALLOWED_TRANSITIONS = { ... }

# Design layer transitions (U₁₀-U₁₅) - Future design, not closed execution
DESIGN_ALLOWED_TRANSITIONS = { ... }

# Combined transitions (for compatibility and tooling)
ALLOWED_TRANSITIONS = {**CORE_ALLOWED_TRANSITIONS, **DESIGN_ALLOWED_TRANSITIONS}
```

**Added helper functions**:

```python
def is_core_layer(layer: ExecutionLayer) -> bool:
    """Check if a layer is part of the execution core (U₀-U₉)."""
    return layer in EXECUTION_CORE_LAYERS

def is_design_layer(layer: ExecutionLayer) -> bool:
    """Check if a layer is part of the design layers (U₁₀-U₁₅)."""
    return layer in DESIGN_LAYERS
```

**Updated module docstring**:

```python
"""
Execution Layer Registry - Canonical U₀-U₉ Order (سجل الطبقات التنفيذية)

...

Execution Core (U₀-U₉): Closed, implemented, operational layers
    U₀ Unicode          → U₁ Grapheme
    ...
    U₈ RootStem         → U₉ Weight

Design Layers (U₁₀-U₁₅): Future design, not closed execution layers
    U₁₀ WordForm
    U₁₁ LexicalEntry
    ...
    U₁₅ Dalālah
"""
```

### 2. Documentation Updates

**`docs/EXEC_LAYER_REFACTOR_SUMMARY.md`**:
- Added "Architectural Distinction: Core vs Design Layers" section
- Clarified that U₀-U₉ are "Closed, implemented, operational"
- Clarified that U₁₀-U₁₅ are "Future design, not closed execution"
- Added critical note: "Production code should only rely on U₀-U₉"

**`docs/U0_U15_IMPLEMENTATION_SUMMARY.md`**:
- Changed title from "Implementation Complete" to "Implementation Status"
- Split table into "Execution Core (U₀-U₉)" and "Design Layers (U₁₀-U₁₅)"
- Added warning: "These layers are architectural placeholders, NOT operational execution layers"
- Marked all U₁₀-U₁₅ as "(planned)" status

### 3. Test Updates

**`tests/dal_core/test_execution_layer_registry.py`**:
- Fixed case sensitivity issue in test assertions
- All 23 tests passing

## Impact

### Immediate Benefits

1. **Clear architectural boundaries**: Code now explicitly distinguishes execution core from design layers
2. **Better documentation**: Developers can clearly see which layers are operational vs. planned
3. **API clarity**: New helper functions (`is_core_layer`, `is_design_layer`) enable programmatic distinction
4. **Backward compatible**: `ALLOWED_TRANSITIONS` still includes all layers for tooling support

### Long-term Implications

1. **Production code guidance**: Clear signal that U₀-U₉ are production-ready, U₁₀-U₁₅ are not
2. **Future implementation**: When U₁₀-U₁₅ are implemented, they can be moved from `DESIGN_LAYERS` to `EXECUTION_CORE_LAYERS`
3. **Architectural clarity**: Prevents confusion about which layers are "closed" (finalized) vs. "open" (subject to change)

## Verification

All tests passing:
```bash
$ python -m pytest tests/dal_core/test_execution_layer_registry.py -v
============================== 23 passed in 0.15s ==============================
```

Key tests validated:
- ✅ Layer ordering preserved
- ✅ Transition validation works correctly
- ✅ Forbidden jumps still blocked
- ✅ Legacy mapping intact

## Architectural Compliance

This fix aligns with the constitutional law:

> **Potentiality-Certification Separation Law**: Carrierᵢ ⊬ Certificateᵢ₊₁

Design layers (U₁₀-U₁₅) are explicitly marked as "potential" (future design) not "certified" (operational execution core).

## Files Changed

| File | Change | Lines |
|------|--------|-------|
| `src/dal_core/execution_layer_registry.py` | Separate core/design, add helpers | +55 |
| `docs/EXEC_LAYER_REFACTOR_SUMMARY.md` | Add architectural distinction | +43 |
| `docs/U0_U15_IMPLEMENTATION_SUMMARY.md` | Clarify implementation status | +18 |
| `tests/dal_core/test_execution_layer_registry.py` | Fix case sensitivity | +3 |
| `docs/EXECUTION_CORE_BOUNDARY_FIX.md` | This document | +200 |

**Total**: ~319 lines changed/added

## Conclusion

The fix resolves the discrepancy between documentation and code by:

1. **Explicitly separating** execution core (U₀-U₉) from design layers (U₁₀-U₁₅) in code
2. **Clarifying documentation** to indicate operational vs. planned status
3. **Providing helper functions** for programmatic distinction
4. **Maintaining backward compatibility** for tooling

**Status**: ✅ Complete, all tests passing

**PR**: claude/update-execution-core-documentation

**Date**: 2026-05-25
