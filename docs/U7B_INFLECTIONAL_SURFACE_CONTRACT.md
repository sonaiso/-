# U₇-B Inflectional Surface Contract - Architecture Summary

## Problem Statement

PR #106 introduced U₈ RootStemCandidateCarrier before implementing surface marker protection. This created an architectural gap where U₈ was consuming raw surface forms directly, potentially "eating" important grammatical markers:

- Definiteness markers (الـ)
- Tanwīn (تنوين)
- Number markers (ان / ين / ون / ات)
- Gender markers (ة feminine)
- I'rāb markers (original and secondary)
- Verb prefixes (ي / ت / ن / أ)
- Passive voice patterns
- Mazīd augmentation letters (است / انـ)
- Proper names and loanwords
- Frozen/jāmid forms

## Solution: U₇-B InflectionalSurfaceContract

U₇-B is an intermediate layer inserted between U₇-A (PreWeightContract) and U₈ (RootStemCandidate) to protect surface markers before root/stem extraction.

### Architectural Ordering

**Before (Problematic)**:
```
U₇ PreWeightContract → U₈ RootStemCandidate
```

**After (Corrected)**:
```
U₇-A PreWeightContract → U₇-B InflectionalSurfaceContract → U₈ RootStemCandidate
```

### Core Principles

#### Architectural Laws

```
No root from raw surface.
No weight from raw surface.
No stripping without trace.
No marker deletion; only protection, classification, and residuals.
```

#### Type System

```
surface ≠ protected_core ≠ root_input
```

- **surface**: Original orthographic form from U₇-A
- **protected_core**: Core form after marker stripping (markers preserved in separate fields)
- **root_input**: Licensed input for U₈ root extraction (currently equals protected_core)

### U₇-B Data Structure

```python
@dataclass(frozen=True)
class InflectionalSurfaceContractUnit:
    # Identity
    uid: str
    surface: str
    source_u7_unit_id: str
    source_u7_trace: Tuple[str, ...]

    # Core separation (CRITICAL)
    protected_prefixes: Tuple[str, ...]
    protected_suffixes: Tuple[str, ...]
    protected_infixes: Tuple[str, ...]
    protected_vowels: Tuple[str, ...]
    protected_core: str
    root_input: str

    # Marker hints (all MarkerHint enum: POSSIBLE/UNLIKELY/UNRESOLVED/AMBIGUOUS/BLOCKED)
    definiteness_marker_hint: MarkerHint
    tanwin_marker_hint: MarkerHint
    number_marker_hint: MarkerHint
    gender_marker_hint: MarkerHint
    rationality_marker_hint: MarkerHint
    original_irab_marker_hint: MarkerHint
    secondary_irab_marker_hint: MarkerHint
    nominative_surface_hint: MarkerHint
    accusative_surface_hint: MarkerHint
    genitive_surface_hint: MarkerHint
    jussive_surface_hint: MarkerHint
    verb_prefix_hint: MarkerHint
    verb_suffix_hint: MarkerHint
    passive_surface_hint: MarkerHint
    mazid_extra_hint: MarkerHint
    proper_name_surface_hint: MarkerHint
    loanword_surface_hint: MarkerHint
    jamid_surface_hint: MarkerHint
    frozen_primitive_surface_hint: MarkerHint

    # Blocking
    blocked_root_segments: Tuple[str, ...]
    blocked_weight_segments: Tuple[str, ...]

    # Evidence
    residuals: FrozenSet[Residual]
    rank: Rank
    trace: Tuple[str, ...]
```

### Forbidden Fields

U₇-B **MUST NOT** contain these fields (constitutional violation):

- `root` (that's U₈)
- `root_certificate` (that's U₈+)
- `weight` (that's U₉)
- `weight_certificate` (that's U₉+)
- `pattern` (that's U₉)
- `hukm` (that's U₇+)
- `final_irab` / `i3rab_final` (that's U₇+)
- `meaning` / `dalalah` (that's U₁₅)
- `resolved_reference` (that's U₁₅)

## Golden Cases (Test Examples)

### 1. Definiteness Marker

```
Input:  الكتاب
Output:
  - surface = "الكتاب"
  - protected_prefixes = ("الـ",)
  - protected_core = "كتاب"
  - root_input = "كتاب"
  - definiteness_marker_hint = POSSIBLE
  - blocked_root_segments = ("الـ",)
```

### 2. Tanwīn Marker

```
Input:  كتابٌ
Output:
  - surface = "كتابٌ"
  - protected_core = "كتاب"
  - root_input = "كتاب"
  - tanwin_marker_hint = POSSIBLE
```

### 3. Dual Marker

```
Input:  مسلمان
Output:
  - surface = "مسلمان"
  - protected_suffixes = ("ان",)
  - protected_core = "مسلم"
  - root_input = "مسلم"
  - number_marker_hint = POSSIBLE
  - blocked_root_segments = ("ان",)
```

### 4. Ambiguous Marker (ين)

```
Input:  مسلمين
Output:
  - surface = "مسلمين"
  - protected_suffixes = ("ين",)
  - protected_core = "مسلم"
  - root_input = "مسلم"
  - number_marker_hint = AMBIGUOUS
  - residuals += ("ambiguous_dual_or_plural_or_case",)
  - blocked_root_segments = ("ين",)
```

### 5. Sound Masculine Plural

```
Input:  مسلمون
Output:
  - surface = "مسلمون"
  - protected_suffixes = ("ون",)
  - protected_core = "مسلم"
  - root_input = "مسلم"
  - number_marker_hint = POSSIBLE
```

### 6. Sound Feminine Plural

```
Input:  مسلمات
Output:
  - surface = "مسلمات"
  - protected_suffixes = ("ات",)
  - protected_core = "مسلم"
  - root_input = "مسلم"
  - number_marker_hint = POSSIBLE
```

### 7. Feminine Marker

```
Input:  مدرسة
Output:
  - surface = "مدرسة"
  - protected_suffixes = ("ة",)
  - protected_core = "مدرس"
  - root_input = "مدرس"
  - gender_marker_hint = POSSIBLE
```

### 8. Verb with Prefix and Suffix

```
Input:  يكتبون
Output:
  - surface = "يكتبون"
  - protected_prefixes = ("ي",)
  - protected_suffixes = ("ون",)
  - protected_core = "كتب"
  - root_input = "كتب"
  - verb_prefix_hint = POSSIBLE
  - number_marker_hint = POSSIBLE
  - blocked_root_segments = ("ي", "ون")
```

### 9. Mazīd Augmentation

```
Input:  استخرج
Output:
  - surface = "استخرج"
  - protected_prefixes = ("است",)
  - protected_core = "خرج"
  - root_input = "خرج"
  - mazid_extra_hint = POSSIBLE
  - blocked_root_segments = ("است",)
```

### 10. Broken Plural - فِعال Pattern (CRITICAL)

```
Input:  رجال
Output:
  - surface = "رجال"
  - protected_core = "رجال"
  - root_input = "" (EMPTY - deferred)
  - root_input_permission = DEFERRED
  - broken_plural_surface_hint = POSSIBLE
  - broken_plural_pattern_hint = "فِعال"
  - residuals += ("broken_plural_deferred")
```

### 11. Broken Plural - مَفاعِل Pattern (CRITICAL)

```
Input:  مدارس
Output:
  - surface = "مدارس"
  - protected_core = "مدارس"
  - root_input = "" (EMPTY - deferred)
  - root_input_permission = DEFERRED
  - broken_plural_surface_hint = POSSIBLE
  - broken_plural_pattern_hint = "مَفاعِل"
  - residuals += ("broken_plural_deferred")
```

### 12. Broken Plural - فُعُل AMBIGUOUS (CRITICAL)

```
Input:  كتب
Output:
  - surface = "كتب"
  - protected_core = "كتب"
  - root_input = "" (EMPTY - deferred)
  - root_input_permission = DEFERRED
  - broken_plural_surface_hint = AMBIGUOUS
  - broken_plural_pattern_hint = "فُعُل"
  - residuals += ("broken_plural_deferred", "ambiguous_plural_or_verb")
```

### 13. Pronoun Suffix - ـه

```
Input:  كتابه
Output:
  - surface = "كتابه"
  - protected_pronoun_suffixes = ("ه",)
  - protected_core = "كتاب"
  - root_input = "كتاب"
  - pronoun_suffix_hint = POSSIBLE
```

## Impact on U₈ RootStemCandidate

### Before Refactoring

```python
def root_stem_candidate_8(pre_weight_layer: PreWeightContractLayerObject):
    for unit in pre_weight_layer.units:
        # ❌ Extracting from raw surface
        root_candidates = _extract_root_candidates(unit.surface, unit)
```

### After Refactoring

```python
def root_stem_candidate_8(inflectional_surface_layer: InflectionalSurfaceContractLayerObject):
    for unit in inflectional_surface_layer.units:
        # CRITICAL: Check root_input_permission FIRST
        if unit.root_input_permission == RootInputPermission.DEFERRED:
            # Cannot extract - broken plural or unresolved marker
            # Emit DEFERRED status, await lexical/pattern evidence
            continue

        if unit.root_input_permission == RootInputPermission.BLOCKED:
            # Extraction blocked
            continue

        # ✅ Extracting from protected root_input (ALLOWED)
        root_candidates = _extract_root_candidates(
            unit.root_input,        # NOT unit.surface
            unit.protected_core,
            unit
        )
```

### Key Changes in U₈

1. **Input type changed**: `PreWeightContractLayerObject` → `InflectionalSurfaceContractLayerObject`
2. **CRITICAL: Check `root_input_permission` before extraction**:
   - `DEFERRED` → Cannot extract, await evidence (broken plurals, ambiguous markers)
   - `BLOCKED` → Extraction blocked
   - `ALLOWED` → Proceed with extraction
3. **Root extraction uses `root_input`**: NOT raw `surface`
4. **Stem extraction uses `protected_core`**: Higher confidence (0.7 vs 0.6)
5. **Blocking logic changed**: Checks `blocked_root_segments` and `root_input_permission`
6. **Additional fields in RootStemCandidateUnit**:
   - `protected_core: str`
   - `root_input: str`
   - `source_u7b_unit_id` (instead of `source_u7_unit_id`)
   - `source_u7b_trace` (instead of `source_u7_trace`)

### CRITICAL: Broken Plural Handling

**Before U₇-B**:
```python
# رجال (men) would be passed to U₈ as raw surface
# U₈ might incorrectly extract root as ر-ج-ل
```

**After U₇-B**:
```python
# رجال detected as broken plural (فِعال pattern)
# root_input_permission = DEFERRED
# root_input = "" (empty)
# U₈ cannot extract - emits DEFERRED status
# Residual: "broken_plural_deferred" awaiting lexical evidence
```

**Examples**:
- `رجال` (men) - فِعال pattern → DEFERRED
- `مدارس` (schools) - مَفاعِل pattern → DEFERRED
- `كتب` (books/wrote) - فُعُل pattern AMBIGUOUS → DEFERRED
- `كتاب` (book) - NOT broken plural → ALLOWED

## Execution Layer Registry Updates

### ExecutionLayer Enum

```python
# Before
U7_PRE_WEIGHT_CONTRACT = "u7_pre_weight_contract"
U8_ROOT_STEM = "u8_root_stem"

# After
U7A_PRE_WEIGHT_CONTRACT = "u7a_pre_weight_contract"
U7B_INFLECTIONAL_SURFACE_CONTRACT = "u7b_inflectional_surface_contract"
U8_ROOT_STEM = "u8_root_stem"
```

### Allowed Transitions

```python
# Before
ExecutionLayer.U6_MABNI_CLOSED_CLASS: {ExecutionLayer.U7_PRE_WEIGHT_CONTRACT},
ExecutionLayer.U7_PRE_WEIGHT_CONTRACT: {ExecutionLayer.U8_ROOT_STEM},

# After
ExecutionLayer.U6_MABNI_CLOSED_CLASS: {ExecutionLayer.U7A_PRE_WEIGHT_CONTRACT},
ExecutionLayer.U7A_PRE_WEIGHT_CONTRACT: {ExecutionLayer.U7B_INFLECTIONAL_SURFACE_CONTRACT},
ExecutionLayer.U7B_INFLECTIONAL_SURFACE_CONTRACT: {ExecutionLayer.U8_ROOT_STEM},
```

### Legacy Compatibility

```python
LEGACY_LAYER_MAPPING = {
    "u7_pre_weight_contract": ExecutionLayer.U7A_PRE_WEIGHT_CONTRACT,
}
```

## Constitutional Guarantees

### CPB₇B Completeness Predicate

CPB₇B enforces:

1. **All units have required fields**:
   - `surface`
   - `protected_core`
   - `root_input`

2. **No forbidden fields**:
   - No `root`, `weight`, `pattern`, `meaning`, `hukm`, `i3rab_final`

3. **Marker hints are hints, NOT judgments**:
   - All hint fields use `MarkerHint` enum
   - Values: `POSSIBLE`, `UNLIKELY`, `UNRESOLVED`, `AMBIGUOUS`, `BLOCKED`

4. **Trace preservation**:
   - `source_pre_weight_layer_id` present
   - Ordered trace to U₇-A maintained

### Proof Object

CPB₇B.build_proof() generates evidence:

```python
evidence=frozenset([
    f"units_count={len(layer_obj.units)}",
    f"units_with_definiteness_hint={...}",
    f"units_with_tanwin_hint={...}",
    f"units_with_number_markers_hint={...}",
    f"total_protected_prefixes={...}",
    f"total_protected_suffixes={...}",
    f"trace_preserved={bool(layer_obj.source_pre_weight_layer_id)}",
    f"rank={layer_obj.rank.value}",
]),
allowed_next_gates=frozenset({"root_stem_candidate_gate"}),
forbidden_next_gates=frozenset({
    "root_certificate",
    "weight_certificate",
    "hukm_certificate",
    "irab_final_judgment",
}),
```

## Testing

### Test Coverage

1. **Golden cases**: All 9 examples from problem statement
2. **Architectural separation**: `surface ≠ protected_core ≠ root_input`
3. **Constitutional prohibitions**: No forbidden fields
4. **Marker hints**: All use `MarkerHint` enum
5. **Blocked segments**: Markers documented for U₈/U₉ to avoid
6. **CPB₇B**: Completeness and proof generation

### Test Files

- `tests/dal_core/test_u7b_inflectional_surface_contract.py` (529 lines, 46 tests)

## Migration Guide

### For Code Consuming U₇ Output

**Before**:
```python
from dal_core.u7_pre_weight_contract_carrier import PreWeightContractLayerObject

def process_layer(layer: PreWeightContractLayerObject):
    for unit in layer.units:
        surface = unit.surface
        # Process surface...
```

**After**:
```python
from dal_core.u7b_inflectional_surface_contract_carrier import (
    InflectionalSurfaceContractLayerObject
)

def process_layer(layer: InflectionalSurfaceContractLayerObject):
    for unit in layer.units:
        surface = unit.surface           # Original surface
        protected_core = unit.protected_core  # After marker stripping
        root_input = unit.root_input     # For root extraction
        # Process root_input, NOT surface...
```

### For U₈ Implementations

**Before**:
```python
root_candidates = extract_root(unit.surface)
```

**After**:
```python
root_candidates = extract_root(unit.root_input)  # Protected from markers
stem_candidates = extract_stem(unit.protected_core)  # Higher confidence
```

## Files Changed

1. **New files**:
   - `src/dal_core/u7b_inflectional_surface_contract_carrier.py` (710 lines)
   - `tests/dal_core/test_u7b_inflectional_surface_contract.py` (529 lines)

2. **Modified files**:
   - `src/dal_core/execution_layer_registry.py` (split U₇ → U₇-A + U₇-B)
   - `src/dal_core/u8_root_stem_candidate_carrier.py` (refactored to consume U₇-B)

## References

- Problem statement: Issue identifying PR #106 architectural gap
- Architectural law: "No root from raw surface" (Axiom 7B.1)
- Constitutional law: Potentiality-Certification Separation Law

## Summary

U₇-B InflectionalSurfaceContract is a **mandatory intermediate layer** that:

1. **Protects** surface markers from being consumed by root/weight extraction
2. **Separates** `surface` → `protected_core` → `root_input`
3. **Classifies** markers as hints (POSSIBLE/UNLIKELY/UNRESOLVED/AMBIGUOUS)
4. **Defers** broken plurals and unresolved markers via `root_input_permission` (ALLOWED/DEFERRED/BLOCKED)
5. **Blocks** segments from being included in root/weight
6. **Preserves** trace and residuals
7. **Forbids** premature judgments (no root, weight, hukm, i3rab_final)

### CRITICAL: Protection-or-Defer Policy

U₇-B implements the **protection-or-defer** architectural law:

```
If marker family is not protected → root_input must be deferred
```

**Protected marker families**:
- Definiteness (الـ)
- Tanwīn (ـٌ، ـاً، ـٍ)
- Number markers (ان، ين، ون، ات)
- Gender markers (ة)
- Verb prefixes (ي، ت، ن، أ)
- Mazīd augmentation (است، انـ، etc.)
- Pronoun suffixes (ـه، ـها، ـهم، ـنا، ـك)

**Deferred marker families** (awaiting lexical/pattern evidence):
- Broken plurals (جمع التكسير) - فِعال، مَفاعِل، فُعُل patterns
- Ambiguous forms (كتب - could be plural or verb)

**Test coverage**: 13 golden cases including:
- 9 original marker protection cases (الكتاب, كتابٌ, مسلمان, etc.)
- 3 broken plural deferral cases (رجال, مدارس, كتب) - **CRITICAL**
- Pronoun suffix protection (كتابه, كتابها, كتابهم)

This closes the architectural gap and ensures U₈ operates on **licensed, protected input** rather than raw surface forms. **No broken plural enters U₈ as raw singular/root input.**
