# U₇-B InflectionalSurfaceContract Implementation

**Status**: ✅ IMPLEMENTED
**Date**: 2026-05-26
**Layer**: U₇ PreWeightContract (U₇-B sub-layer)

---

## Summary

U₇-B InflectionalSurfaceContract is the **inflectional surface marker filter** that sits between U₇-A (closed/open permission) and U₈ (root extraction).

**Critical Law**:
```
علامات الإعراب والعدد والجنس والتعريف ليست جذورًا
Iʿrāb, number, gender, and definiteness markers are NOT root letters.
```

**Architectural Position**:
```
U₇ PreWeightContract = U₇-A (Closed/Open Permission) + U₇-B (InflectionalSurfaceContract)

U₆ (MabniClosedClass)
  → U₇-A (Permission Gate) ✅ Blocks closed-class from morphology
    → U₇-B (Inflectional Filter) ✅ NEW - Detects/strips surface markers
      → U₈ (RootStem) - Root extraction on stripped_core only
```

---

## Problem Statement

**Before U₇-B** (missing layer):
- كتابان → U₈ might treat "ان" as root letters → WRONG
- مسلمون → U₈ might treat "ون" as root letters → WRONG
- الكتاب → U₈ might treat "ال" as root letters → WRONG
- مسلمات → U₈ might treat "ات" as root letters → WRONG

**After U₇-B** (complete):
- كتابان → U₇-B: dual_hint=possible, stripped_core=كتاب, blocked_segments=(ان,) → U₈: root from كتاب only ✅
- مسلمون → U₇-B: sound_masc_plural=possible, stripped_core=مسلم, blocked_segments=(ون,) → U₈: root from مسلم only ✅
- الكتاب → U₇-B: al_definiteness=possible, stripped_core=كتاب → U₈: root from كتاب only ✅
- مسلمات → U₇-B: sound_fem_plural=possible, stripped_core=مسلم, blocked_segments=(ات,) → U₈: root from مسلم only ✅

---

## Architecture

### U₇ Complete Structure

```
U₇ PreWeightContract:
  ├── U₇-A: Closed/Open Permission (EXISTING)
  │   ├── Closed-class → BLOCKED (no root/weight path)
  │   └── Open-class → POSSIBLE (may proceed, pending U₇-B)
  │
  └── U₇-B: InflectionalSurfaceContract (NEW)
      ├── Dual markers (ان/ين) detection
      ├── Sound masculine plural (ون/ين) detection
      ├── Sound feminine plural (ات) detection
      ├── Al-definiteness (ال) detection
      ├── Tanwīn (ٌ/ٍ/ً) detection
      ├── Iʿrāb surface hints (nom/acc/gen/juss)
      ├── Gender surface hints (masc/fem/literal/semantic)
      ├── Rationality hints (rational/non-rational)
      ├── Diptote hints (ممنوع من الصرف)
      │
      ├── Core Extraction:
      │   ├── stripped_core_candidate (النواة المجردة)
      │   ├── preserved_suffixes (اللواحق المحفوظة)
      │   └── blocked_root_segments (المقاطع المحظورة من الجذر)
      │
      └── Constitutional Principle:
          ALL fields are HINTS (possible/unlikely/unresolved)
          NOT certificates or final judgments
```

---

## Data Structure

### InflectionalSurfaceProfile

```python
@dataclass(frozen=True)
class InflectionalSurfaceProfile:
    """
    U₇-B Inflectional Surface Profile

    Purpose: Filter surface markers BEFORE root/weight extraction

    Constitutional Law:
        Surface existence → boolean
        Surface interpretation → hint (possible/unlikely/unresolved)

    FORBIDDEN FIELDS:
        - i3rab_certificate (that's U₇+)
        - number_certificate (that's U₇+)
        - root (that's U₈)
        - weight (that's U₉)
    """

    # Iʿrāb markers (original + secondary)
    nominative_surface_hint: PathPermission
    accusative_surface_hint: PathPermission
    genitive_surface_hint: PathPermission
    jussive_surface_hint: PathPermission
    secondary_i3rab_marker_hint: PathPermission

    # Number markers
    dual_surface_hint: PathPermission
    sound_masculine_plural_surface_hint: PathPermission
    sound_feminine_plural_surface_hint: PathPermission
    broken_plural_surface_hint: PathPermission
    singular_surface_hint: PathPermission

    # Gender markers
    masculine_surface_hint: PathPermission
    feminine_surface_hint: PathPermission

    # Rationality
    rational_surface_hint: PathPermission
    non_rational_surface_hint: PathPermission

    # Definiteness
    al_definiteness_surface_hint: PathPermission
    tanwin_surface_hint: PathPermission

    # Diptote
    diptote_surface_hint: PathPermission

    # Feminine types
    literal_feminine_hint: PathPermission
    semantic_feminine_hint: PathPermission

    # Core extraction (CRITICAL for U₈)
    stripped_core_candidate: str
    preserved_suffixes: Tuple[str, ...]
    blocked_root_segments: Tuple[str, ...]

    # Evidence
    residuals: Tuple[str, ...]
    trace_source: str
```

---

## Detection Logic

### 1. Number Surface Markers

```python
def _detect_number_surface_markers(surface: str):
    """
    Detects: ان/ين (dual), ون/ين (sound masc plural), ات (sound fem plural)

    Examples:
        كتابان → dual=possible, stripped=كتاب, blocked=(ان,)
        مسلمون → sound_masc_plural=possible, stripped=مسلم, blocked=(ون,)
        مسلمات → sound_fem_plural=possible, stripped=مسلم, blocked=(ات,)
    """
```

**Rules**:
- Dual: surface ends with ان or ين (length ≥ 4)
- Sound masculine plural: surface ends with ون (length ≥ 4)
- Sound feminine plural: surface ends with ات (length ≥ 4)
- stripped_core = surface minus detected suffix
- blocked_segments = detected suffix

### 2. Definiteness Surface Markers

```python
def _detect_definiteness_surface_markers(surface: str):
    """
    Detects: ال (definiteness), ٌ/ٍ/ً (tanwīn)

    Examples:
        الكتاب → al_definiteness=possible, stripped=كتاب
        كتابٌ → tanwin=possible
    """
```

**Rules**:
- Al-definiteness: surface starts with ال (length ≥ 3)
- Tanwīn: surface contains ٌ or ٍ or ً
- stripped_core = surface minus ال if detected

### 3. Iʿrāb Surface Markers

```python
def _detect_irab_surface_markers(surface: str):
    """
    Detects: ُ/ٌ (nominative), َ/ً (accusative), ِ/ٍ (genitive), ْ (jussive)

    All as HINTS, not certificates.
    """
```

**Rules** (hints only):
- Nominative: ُ or ٌ or ends with ون
- Accusative: َ or ً or ends with ا
- Genitive: ِ or ٍ or ends with ين
- Jussive: ْ present
- Secondary: ends with و/ا/ي or ون/ين/ان

### 4. Gender Surface Markers

```python
def _detect_gender_surface_markers(surface: str, suffixes: Tuple[str, ...]):
    """
    Detects: ة (tāʾ marbūṭa - literal feminine), ات (sound fem plural)

    Examples:
        كاتبة → feminine=possible, literal_feminine=possible
        كاتب → masculine=possible, semantic_feminine=possible
    """
```

**Rules**:
- Literal feminine: ة or ـة present OR ات in suffixes
- Masculine/semantic feminine: possible if no literal feminine marker

---

## Integration into U₇ Pipeline

### Updated pre_weight_contract_7() Flow

```python
def pre_weight_contract_7(mabni_layer: MabniClosedClassLayerObject):
    """
    U₇ = U₇-A (permission) + U₇-B (inflectional filter)
    """
    for mabni_unit in mabni_layer.units:
        # U₇-A: Classify contract status
        contract_status = _classify_contract_status(mabni_unit)

        # Determine open/closed status
        open_closed_status = "closed_class" if contract_status == CLOSED_CLASS_BLOCKED else "open_class"

        # U₇-B: Inflectional surface analysis (NEW)
        inflectional_surface_profile = _analyze_inflectional_surface(
            mabni_unit.surface,
            open_closed_status
        )

        # Build PreWeightContractUnit with U₇-B profile
        contract_unit = PreWeightContractUnit(
            ...
            inflectional_surface_profile=inflectional_surface_profile,  # U₇-B
            ...
        )
```

**Key Change**:
- Closed-class units: `inflectional_surface_profile = None` (already blocked at U₇-A)
- Open-class units: `inflectional_surface_profile = InflectionalSurfaceProfile(...)` with full analysis

---

## Usage Example

### Input: كتابان

```python
# U₅ → U₆ → U₇
u5_layer = make_u5_layer("كتابان")
u6_result = mabni_closed_class_6(u5_layer)
u7_result = pre_weight_contract_7(u6_result.layer_object)

# Access U₇-B profile
unit = u7_result.layer_object.units[0]
profile = unit.inflectional_surface_profile

# CRITICAL OUTPUTS
assert profile.dual_surface_hint == PathPermission.POSSIBLE
assert profile.stripped_core_candidate == "كتاب"
assert "ان" in profile.preserved_suffixes
assert "ان" in profile.blocked_root_segments

# U₈ RootStem (future) will use:
#   - stripped_core_candidate = "كتاب" (NOT "كتابان")
#   - blocked_root_segments = ("ان",) (must not extract root from this)
```

---

## Golden Test Cases

### 1. Dual (كتابان)
- **Input**: كتابان
- **U₇-B Output**:
  - dual_surface_hint = POSSIBLE
  - stripped_core_candidate = كتاب
  - preserved_suffixes = (ان,)
  - blocked_root_segments = (ان,)

### 2. Sound Masculine Plural (مسلمون)
- **Input**: مسلمون
- **U₇-B Output**:
  - sound_masculine_plural_surface_hint = POSSIBLE
  - stripped_core_candidate = مسلم
  - preserved_suffixes = (ون,)
  - blocked_root_segments = (ون,)

### 3. Sound Feminine Plural (مسلمات)
- **Input**: مسلمات
- **U₇-B Output**:
  - sound_feminine_plural_surface_hint = POSSIBLE
  - feminine_surface_hint = POSSIBLE
  - literal_feminine_hint = POSSIBLE
  - stripped_core_candidate = مسلم
  - preserved_suffixes = (ات,)
  - blocked_root_segments = (ات,)

### 4. Al-Definiteness (الكتاب)
- **Input**: الكتاب
- **U₇-B Output**:
  - al_definiteness_surface_hint = POSSIBLE
  - stripped_core_candidate = كتاب
  - tanwin_surface_hint = UNRESOLVED

### 5. Tanwīn (كتابٌ)
- **Input**: كتابٌ
- **U₇-B Output**:
  - tanwin_surface_hint = POSSIBLE
  - nominative_surface_hint = POSSIBLE
  - stripped_core_candidate = كتابٌ (no stripping, just hint)

---

## Constitutional Laws

### 1. No Root Before Inflectional Filter
```
U₇-B MUST execute before U₈ root extraction.
U₈ MUST use stripped_core_candidate, NOT original surface.
U₈ MUST NOT extract root from blocked_root_segments.
```

### 2. Hints, Not Certificates
```
All U₇-B fields are PathPermission (possible/unlikely/unresolved).
U₇-B DOES NOT certify:
  - i3rab status (that's U₇+)
  - number status (that's U₇+)
  - gender status (that's U₇+)
  - definiteness status (that's U₇+)
```

### 3. Closed-Class Skip
```
Closed-class units (وَ, بِ, فَ, ـهِمْ) already blocked at U₇-A.
U₇-B does NOT analyze closed-class units.
inflectional_surface_profile = None for closed-class.
```

### 4. Trace Preservation
```
trace_source MUST preserve original surface.
stripped_core_candidate is transformation, NOT replacement.
U₈ can reconstruct original form via trace if needed.
```

---

## Test Coverage

**Test File**: `tests/dal_core/test_u7b_inflectional_surface.py`

**Test Count**: 18 tests

**Coverage**:
- [x] Dual surface markers (كتابان/كتابين)
- [x] Sound masculine plural (مسلمون)
- [x] Sound feminine plural (مسلمات)
- [x] Al-definiteness (الكتاب)
- [x] Tanwīn detection (كتابٌ/كتابٍ/كتابًا)
- [x] Iʿrāb surface hints (nominative/accusative/genitive/jussive)
- [x] Gender surface hints (masculine/feminine/literal/semantic)
- [x] Blocked root segments preservation
- [x] Closed-class units (no inflectional analysis)
- [x] Forbidden fields enforcement
- [x] Complete U₅→U₆→U₇ pipeline

---

## Impact on U₈ RootStem (Future)

**U₈ RootStem Requirements** (when implemented):

1. **MUST use `stripped_core_candidate`** for root extraction, NOT original `surface`
   ```python
   # WRONG
   root = extract_root(unit.surface)  # "كتابان" → wrong!

   # CORRECT
   profile = unit.inflectional_surface_profile
   if profile:
       root = extract_root(profile.stripped_core_candidate)  # "كتاب" → correct!
   ```

2. **MUST NOT extract root from `blocked_root_segments`**
   ```python
   # WRONG
   root_letters = analyze_all_letters(surface)  # includes ان/ون/ات → wrong!

   # CORRECT
   for segment in profile.blocked_root_segments:
       assert segment not in root_letters  # enforce block
   ```

3. **MAY use surface hints for pattern selection**
   ```python
   if profile.sound_masculine_plural_surface_hint == PathPermission.POSSIBLE:
       # Consider plural patterns for root search
       pattern_family = PLURAL_PATTERNS
   ```

---

## Files

### Implementation
- `src/dal_core/u7_pre_weight_contract_carrier.py` (1039 lines, +250 lines U₇-B)

### Tests
- `tests/dal_core/test_u7b_inflectional_surface.py` (535 lines, 18 tests)

### Documentation
- `docs/U7B_INFLECTIONAL_SURFACE_CONTRACT.md` (this file)

---

## Architectural Significance

### Pre-Morphological Governance Complete

With U₇-B, the **Pre-Morphological Governance Core** is truly complete:

```
U₀-U₇: Pre-Morphological Governance ✅ COMPLETE
    - Character encoding (U₀)
    - Visual segmentation (U₁)
    - Sound representation (U₂p, U₂s)
    - Boundary detection (U₃)
    - True singular identification (U₄)
    - Functional classification (U₅)
    - Closed/open separation (U₆)
    - Morphological permission gate (U₇-A)
    - Inflectional surface filter (U₇-B) ← NEW

U₈-U₉: Morphological Analysis Core ⏳ READY TO IMPLEMENT
    - Root/stem extraction (U₈) - now safe to implement
    - Weight/pattern determination (U₉)
```

### Path Blocking Law Enforced

```
لا جذر قبل تجريد علامات الإعراب والعدد ✅
No root before stripping iʿrāb and number markers.

This architectural law is now **enforced in code**.
```

---

## Conclusion

**U₇-B InflectionalSurfaceContract is COMPLETE and INTEGRATED.**

The implementation:
- ✅ Detects all major inflectional surface markers
- ✅ Provides stripped_core_candidate for U₈
- ✅ Blocks marker segments from root extraction
- ✅ Maintains hints-not-certificates principle
- ✅ Skips closed-class units (already blocked)
- ✅ Preserves full trace to original surface
- ✅ Passes 18 comprehensive tests
- ✅ Ready for U₈ RootStem implementation

**The project can now safely proceed to U₈ RootStem.**

---

**Status**: ✅ IMPLEMENTATION COMPLETE
**Author**: Claude Sonnet 4.5
**Date**: 2026-05-26
**Branch**: claude/update-inflectional-filter-layer
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
