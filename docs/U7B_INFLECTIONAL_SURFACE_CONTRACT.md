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
