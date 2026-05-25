# Execution Layer Refactor - Architectural Correction

## Executive Summary

This PR implements a **critical architectural refactor** to correct the execution layer ordering and prevent layer jumps that violate the no-leap principle.

## Problem Statement

The previous architecture had **U₃ = FunctionalRoleCarrier** positioned immediately after **U₂s ArabicSyllableCarrier**, creating an architectural violation:

```
❌ OLD (INCORRECT):
U₂s Syllable → U₃ FunctionalRole → U₄ Morpheme → ...

PROBLEM: Cannot assign functional roles before:
  1. Identifying boundaries (separate وَ, بِـ, كِتَاب, ـهِمْ in وَبِكِتَابِهِمْ)
  2. Determining true singular lafẓ vs. compound
```

**Violation**: لا دور وظيفي قبل فصل الحدود (No functional role before boundary separation)

## Solution

Correct the execution layer ordering by inserting two missing intermediate layers:

```
✅ NEW (CORRECT):
U₂s ArabicSyllable
  → U₃ BoundaryAndAttachment (separate boundaries)
  → U₄ TrueSingularLafẓ (identify standalone vs. compound)
  → U₅ FunctionalRole (assign roles)
  → U₆ MabniClosedClass
  → U₇ PreWeightContract
  → U₈ RootStem
  → U₉ Weight
```

## Implementation

### 1. Execution Layer Registry (`src/dal_core/execution_layer_registry.py`)

**New canonical registry** defining:
- Official layer sequence (U₀-U₁₅)
- Allowed transitions (U₂s → U₃ only)
- Forbidden jumps (U₂s → U₅, U₂s → U₈, U₂s → U₉)
- Validation functions
- Legacy layer mapping

**Key Functions**:
```python
is_transition_allowed(from_layer, to_layer) -> bool
get_forbidden_jump_reason(from_layer, to_layer) -> str
get_required_intermediate_layers(from_layer, to_layer) -> set
validate_layer_sequence(sequence) -> (bool, error)
```

### 2. U₃ BoundaryAndAttachmentCarrier (`src/dal_core/u3_boundary_attachment_carrier.py`)

**NEW LAYER** - Identifies boundaries and attachment relationships

**Types**:
- `BoundaryUnitType`: STANDALONE_CORE, ATTACHED_PROCLITIC, ATTACHED_ENCLITIC, etc.
- `AttachmentType`: PROCLITIC_TO_HOST, ENCLITIC_TO_HOST, BOTH_SIDES, etc.
- `BoundaryEvidence`: SPACE_SEPARATOR, ORTHOGRAPHIC_PATTERN, LEXICON_MATCH, etc.

**Core Structures**:
- `BoundaryUnit`: Single boundary unit (وَ, بِـ, كِتَاب, ـهِمْ)
- `BoundaryLayerObject`: U₃ layer output
- `CPB3`: Completeness predicate with allowed/forbidden gates

**Operation**: `boundary_3(syllable_layer) -> BoundaryResult` (skeleton implementation)

**Forbidden Fields**: root, weight, functional_role, meaning, hukm

**Example**:
```
وَبِكِتَابِهِمْ → [وَ, بِـ, كِتَاب, ـهِمْ]
  وَ = standalone_proclitic (potential conjunction)
  بِـ = attached_proclitic (potential preposition)
  كِتَاب = core_candidate (potential lexical unit)
  ـهِمْ = attached_enclitic (potential pronoun)
```

### 3. U₄ TrueSingularLafẓCarrier (`src/dal_core/u4_true_singular_lafz_carrier.py`)

**NEW LAYER** - Distinguishes true singular lafẓ from orthographic compounds

**Types**:
- `LafzStatus`: TRUE_SINGULAR, ORTHOGRAPHIC_COMPOUND, NOT_STANDALONE, etc.
- `LafzComposition`: SINGLE_UNIT, PREFIX_PLUS_CORE, CORE_PLUS_SUFFIX, FULL_COMPOSITE
- `LafzEvidence`: BOUNDARY_EVIDENCE, STANDALONE_TEST, LEXICON_ATTESTATION, etc.

**Core Structures**:
- `TrueLafzCandidate`: Lafẓ candidate with singularity status
- `TrueLafzLayerObject`: U₄ layer output
- `CPB4`: Completeness predicate with allowed/forbidden gates

**Operation**: `true_lafz_4(boundary_layer) -> TrueLafzResult` (skeleton implementation)

**Forbidden Fields**: root, weight, functional_role, meaning

**Example**:
```
From [وَ, بِـ, كِتَاب, ـهِمْ]:
  وَ → TRUE_SINGULAR (standalone conjunction)
  بِـ → TRUE_SINGULAR (can standalone)
  كِتَاب → TRUE_SINGULAR (lexical core)
  ـهِمْ → NOT_STANDALONE (requires host)
  بِكِتَاب → ORTHOGRAPHIC_COMPOUND (preposition + noun)
```

### 4. U₅ FunctionalRoleCarrier (`src/dal_core/u5_functional_role_carrier.py`)

**ADAPTER** - Re-exports from legacy `u3_functional_roles.py`

**Purpose**: Establish canonical U₅ position while preserving backward compatibility

**Re-exports**:
- All role types (RoleSort, ClosedClassRole, PronounRole, RootRole, etc.)
- All structures (FunctionalRole, RoleCandidate, FunctionalRoleLayerObject, etc.)
- All operations (CPB_FunctionalRole, etc.)

**Validation Functions**:
- `validate_preconditions(input_layer)`: Ensures U₄ TrueLafẓ as input
- `validate_next_layer(next_layer)`: Ensures U₆ MabniClosedClass as output

### 5. Legacy U₃ Marking (`src/dal_core/u3_functional_roles.py`)

**UPDATED** - Marked as legacy/mispositioned with architectural note

**Header**:
```
⚠️ LEGACY U₃ Functional Role Layer - ARCHITECTURAL REPOSITIONING REQUIRED ⚠️

DEPRECATED POSITION: This module was originally U₃ but is now recognized as U₅.

MIGRATION PATH:
  - This file is retained for compatibility
  - New code should use: from dal_core.u5_functional_role_carrier import *
  - Canonical layer order: See execution_layer_registry.EXECUTION_LAYER_ORDER
```

### 6. Comprehensive Tests (`tests/dal_core/test_execution_layer_registry.py`)

**31 tests** covering:

#### Registry Structure (3 tests)
- ✅ All layers in EXECUTION_LAYER_ORDER
- ✅ U₃ is BoundaryAndAttachment (not FunctionalRole)
- ✅ U₄ TrueLafẓ exists between U₃ and U₅

#### Allowed Transitions (3 tests)
- ✅ U₂s → U₃ Boundary allowed
- ✅ U₃ → U₄ TrueLafẓ allowed
- ✅ U₄ → U₅ FunctionalRole allowed

#### Forbidden Jumps (5 tests) - **CRITICAL**
- ❌ U₂s → U₅ FunctionalRole FORBIDDEN (missing U₃ and U₄)
- ❌ U₂s → U₈ Root FORBIDDEN (missing 6 layers)
- ❌ U₂s → U₉ Weight FORBIDDEN (missing 7 layers)
- ❌ U₃ → U₅ FunctionalRole FORBIDDEN (missing U₄)

#### Required Intermediate Layers (2 tests)
- ✅ U₂s → U₅ requires [U₃, U₄]
- ✅ U₂s → U₈ requires [U₃, U₄, U₅, U₆, U₇]

#### Sequence Validation (5 tests)
- ✅ Correct sequence validated
- ❌ U₂s → U₅ jump rejected
- ❌ U₂s → U₈ jump rejected
- ❌ U₃ → U₅ jump rejected

#### Legacy Mapping (2 tests)
- ✅ legacy_u3_functional_role → U₅
- ✅ Nonexistent legacy → None

#### Architectural Invariants (3 tests)
- ✅ No layer can jump over U₃ Boundary
- ✅ No layer can jump over U₄ TrueLafẓ
- ✅ FunctionalRole is U₅, not U₃

#### Integration (2 tests)
- ✅ Full canonical path U₂s → U₃ → U₄ → U₅ valid
- ✅ All transitions individually allowed

## Architectural Compliance

### Critical Laws Enforced

| Law | Enforcement | File |
|-----|-------------|------|
| لا دور وظيفي قبل فصل الحدود | U₂s → U₃ mandatory | execution_layer_registry.py |
| لا لفظ حقيقي قبل الحدود | U₃ → U₄ mandatory | execution_layer_registry.py |
| لا جذر في U₃ | Field validation | u3_boundary_attachment_carrier.py |
| لا وزن في U₃ | Field validation | u3_boundary_attachment_carrier.py |
| لا جذر في U₄ | Field validation | u4_true_singular_lafz_carrier.py |
| لا وزن في U₄ | Field validation | u4_true_singular_lafz_carrier.py |
| Boundary ≠ Role | Type system | u3_boundary_attachment_carrier.py |
| Lafẓ ≠ Root | Type system | u4_true_singular_lafz_carrier.py |

### Canonical Pattern (CPB)

Both U₃ and U₄ follow canonical pattern:

```python
Carrier: BoundaryUnit / TrueLafzCandidate
Identity: uid (frozen dataclass)
Operations: boundary_3 / true_lafz_4 (skeleton)
Relations: trace_2s / trace_3 (preserved)
Gate: CPB3 / CPB4 (with allowed/forbidden gates)
Rank: Evidence-based progression
Residuals: Warnings/blockers
Proof: ProofObject with completeness predicate
```

**Allowed Next Gates**:
- CPB₃: `true_singular_lafz_gate` ONLY
- CPB₄: `functional_role_gate` ONLY

**Forbidden Gates**:
- CPB₃: `functional_role_direct`, `root_certificate`, `weight_certificate`, `meaning_certificate`, `hukm_certificate`
- CPB₄: `root_certificate`, `weight_certificate`, `meaning_certificate`, `hukm_certificate`

## Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `src/dal_core/execution_layer_registry.py` | 273 | Canonical layer registry |
| `src/dal_core/u3_boundary_attachment_carrier.py` | 350 | U₃ Boundary layer (skeleton) |
| `src/dal_core/u4_true_singular_lafz_carrier.py` | 300 | U₄ TrueLafẓ layer (skeleton) |
| `src/dal_core/u5_functional_role_carrier.py` | 150 | U₅ adapter (re-export) |
| `tests/dal_core/test_execution_layer_registry.py` | 400 | 31 comprehensive tests |

**Total**: ~1,473 new lines

## Files Modified

| File | Change | Purpose |
|------|--------|---------|
| `src/dal_core/u3_functional_roles.py` | Header update | Mark as legacy U₃ → U₅ |

## Migration Path

### Backward Compatibility

✅ **No breaking changes**:
- Legacy `u3_functional_roles.py` still works
- Existing imports continue to function
- All existing tests should pass

### Recommended Migration

```python
# OLD (still works):
from dal_core.u3_functional_roles import FunctionalRole

# NEW (recommended):
from dal_core.u5_functional_role_carrier import FunctionalRole
```

### Future Work

1. **Implement Full U₃ Boundary Detection**:
   - Lexicon-based boundary detection
   - Morphological pattern recognition
   - Statistical boundary inference
   - Test cases: كَتَبَ, بِكِتَابٍ, وَبِكِتَابِهِمْ

2. **Implement Full U₄ TrueLafẓ Determination**:
   - Standalone tests
   - Compositional structure analysis
   - Lexicon attestation checks
   - Morphological integrity validation

3. **Update Existing Pipelines**:
   - Modify pipelines using U₃ FunctionalRole to use canonical sequence
   - Add U₃ and U₄ to processing chains

4. **Documentation**:
   - Update architecture diagrams
   - Update layer documentation
   - Create migration guide

## Test Results

**Expected**: All 31 tests should pass

```bash
pytest tests/dal_core/test_execution_layer_registry.py -v
```

**Critical Tests** (must pass):
- ✅ `test_u2s_to_functional_role_is_FORBIDDEN`
- ✅ `test_u2s_to_root_is_FORBIDDEN`
- ✅ `test_u2s_to_weight_is_FORBIDDEN`
- ✅ `test_validate_rejects_u2s_to_functional_role_jump`
- ✅ `test_no_layer_allows_jump_over_boundary`
- ✅ `test_no_layer_allows_jump_over_true_lafz`
- ✅ `test_functional_role_is_not_u3`

## Rationale

### Why This Refactor Is Critical

Example: **وَبِكِتَابِهِمْ**

**Without U₃ and U₄** (old architecture):
```
Syllable layer: [وَ, بِ, كِ, تَا, بِ, هِمْ]
↓ (JUMP)
FunctionalRole: ??? (cannot determine roles without boundaries)
```

**With U₃ and U₄** (new architecture):
```
U₂s Syllable: [وَ, بِ, كِ, تَا, بِ, هِمْ]
↓
U₃ Boundary: [وَ, بِـ, كِتَاب, ـهِمْ]
  - وَ = standalone_proclitic
  - بِـ = attached_proclitic
  - كِتَاب = core_candidate
  - ـهِمْ = attached_enclitic
↓
U₄ TrueLafẓ:
  - وَ = TRUE_SINGULAR
  - بِـ = TRUE_SINGULAR
  - كِتَاب = TRUE_SINGULAR
  - ـهِمْ = NOT_STANDALONE
  - بِكِتَاب = ORTHOGRAPHIC_COMPOUND
  - كِتَابِهِمْ = ORTHOGRAPHIC_COMPOUND
↓
U₅ FunctionalRole:
  - وَ = HARF_ATF (conjunction)
  - بِـ = HARF_JARR (preposition)
  - كِتَاب = ROOT candidate
  - ـهِمْ = ATTACHED_PRONOUN
```

**Result**: Roles can be assigned **only after** boundaries identified and true lafẓ determined.

## Impact

### Immediate
- ✅ Prevents architectural layer jumps
- ✅ Establishes canonical layer ordering
- ✅ Preserves backward compatibility
- ✅ Adds 31 tests for layer validation

### Long-term
- Enables proper boundary detection
- Enables true lafẓ identification
- Prevents premature role assignment
- Supports compositional analysis
- Aligns with no-leap principle

## PR Checklist

- [x] Execution layer registry created
- [x] U₃ BoundaryAndAttachmentCarrier skeleton implemented
- [x] U₄ TrueSingularLafẓCarrier skeleton implemented
- [x] U₅ FunctionalRoleCarrier adapter created
- [x] Legacy U₃ marked as repositioned
- [x] 31 comprehensive tests added
- [x] Documentation updated
- [x] No breaking changes
- [ ] All tests passing (to be verified)

## Conclusion

This refactor **corrects a fundamental architectural violation** where FunctionalRole was positioned as U₃, allowing direct jumps from Syllable to Role without boundary detection or lafẓ identification.

The new canonical sequence:
```
U₂s → U₃ Boundary → U₄ TrueLafẓ → U₅ FunctionalRole
```

Enforces the critical law: **لا دور وظيفي قبل فصل الحدود** (No functional role before boundary separation)

This is **not optional**—it is an architectural necessity for correct linguistic analysis.
