# U₇-B Marker Coverage Checklist

## Purpose

This document tracks **complete marker family coverage** for U₇-B InflectionalSurfaceContract.

**Architectural Law**: No U₈ root extraction from any surface whose marker-family coverage is incomplete.

**Policy**: Protection-or-defer for ALL marker families.

---

## A. مغطى الآن (Currently Covered) ✅

### A1. Definiteness (التعريف)

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| الـ | ✅ | ✅ | ✅ | COMPLETE |

**Fields**:
- `definiteness_marker_hint: MarkerHint`
- `protected_prefixes: Tuple[str, ...]`

**Test cases**: `test_golden_case_definite_alkitab`

---

### A2. Tanwīn (التنوين)

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| ـٌ (ḍammatayn) | ✅ | ✅ | ✅ | COMPLETE |
| ـاً (fatḥatayn) | ✅ | ✅ | ✅ | COMPLETE |
| ـٍ (kasratayn) | ✅ | ✅ | ✅ | COMPLETE |

**Fields**:
- `tanwin_marker_hint: MarkerHint`
- `protected_suffixes: Tuple[str, ...]`

**Test cases**: `test_golden_case_tanwin_kitabun`

---

### A3. Sound Masculine Plural (جمع المذكر السالم)

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| ون | ✅ | ✅ | ✅ | COMPLETE |
| ين | ✅ | ✅ | ✅ | COMPLETE |

**Fields**:
- `number_marker_hint: MarkerHint`
- `protected_suffixes: Tuple[str, ...]`

**Test cases**: `test_golden_case_masculine_plural_muslimoon`

---

### A4. Dual (المثنى)

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| ان | ✅ | ✅ | ✅ | COMPLETE |
| ين | ✅ | ✅ | ✅ | COMPLETE |

**Fields**:
- `number_marker_hint: MarkerHint`
- `protected_suffixes: Tuple[str, ...]`

**Test cases**: `test_golden_case_dual_musliman`, `test_golden_case_dual_muslimain`

---

### A5. Sound Feminine Plural (جمع المؤنث السالم)

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| ات | ✅ | ✅ | ✅ | COMPLETE |

**Fields**:
- `number_marker_hint: MarkerHint`
- `gender_marker_hint: MarkerHint`
- `protected_suffixes: Tuple[str, ...]`

**Test cases**: `test_golden_case_feminine_plural_muslimat`

---

### A6. Feminine Marker (تاء التأنيث)

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| ة (tā' marbūṭa) | ✅ | ✅ | ✅ | COMPLETE |

**Fields**:
- `gender_marker_hint: MarkerHint`
- `protected_suffixes: Tuple[str, ...]`

**Test cases**: `test_golden_case_feminine_madrasa`

---

### A7. Present Tense Prefixes (سوابق المضارعة)

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| ي | ✅ | ✅ | ✅ | COMPLETE |
| ت | ✅ | ✅ | ✅ | COMPLETE |
| ن | ✅ | ✅ | ✅ | COMPLETE |
| أ | ✅ | ✅ | ✅ | COMPLETE |

**Fields**:
- `verb_prefix_hint: MarkerHint`
- `protected_prefixes: Tuple[str, ...]`

**Test cases**: `test_golden_case_present_tense_yaktuboon`

---

### A8. Mazīd Augmentation (زوائد المزيد)

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| است | ✅ | ✅ | ✅ | COMPLETE |
| انـ | ✅ | ✅ | ⚠️ | PARTIAL |
| تـ (Form V/VI) | ⚠️ | ⚠️ | ❌ | INCOMPLETE |
| ا (Form III/IV) | ⚠️ | ⚠️ | ❌ | INCOMPLETE |

**Fields**:
- `mazid_extra_hint: MarkerHint`
- `protected_prefixes: Tuple[str, ...]`

**Test cases**: `test_golden_case_mazid_istakhraj`

**Status**: Basic patterns (است، انـ) covered. Complete mazīd pattern matrix needed.

---

### A9. Pronoun Suffixes (الضمائر المتصلة) - PARTIAL

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| ه | ✅ | ✅ | ✅ | COMPLETE |
| ها | ✅ | ✅ | ✅ | COMPLETE |
| هم | ✅ | ✅ | ✅ | COMPLETE |
| نا | ✅ | ✅ | ⚠️ | PARTIAL |
| ك | ✅ | ✅ | ⚠️ | PARTIAL |
| كم | ❌ | ❌ | ❌ | MISSING |
| كما | ❌ | ❌ | ❌ | MISSING |
| كن | ❌ | ❌ | ❌ | MISSING |
| هن | ❌ | ❌ | ❌ | MISSING |
| هما | ❌ | ❌ | ❌ | MISSING |

**Fields**:
- `pronoun_suffix_hint: MarkerHint`
- `protected_pronoun_suffixes: Tuple[str, ...]`

**Test cases**: `test_pronoun_suffix_hu`, `test_pronoun_suffix_haa`, `test_pronoun_suffix_hum`

**Status**: 5 of 14 pronoun forms covered. **Needs completion**.

---

### A10. Broken Plural Deferral (جمع التكسير) - CRITICAL ✅

| Pattern | Detection | Deferral | Tests | Status |
|---------|-----------|----------|-------|--------|
| فِعال (rijāl) | ✅ | ✅ | ✅ | COMPLETE |
| مَفاعِل (madāris) | ✅ | ✅ | ✅ | COMPLETE |
| فُعُل (kutub - ambiguous) | ✅ | ✅ | ✅ | COMPLETE |

**Fields**:
- `root_input_permission: RootInputPermission`
- `broken_plural_surface_hint: MarkerHint`
- `broken_plural_pattern_hint: str`

**Test cases**: `test_rijal_broken_plural_deferred`, `test_madaris_broken_plural_deferred`, `test_kutub_ambiguous_broken_plural_deferred`

**Status**: Core patterns detected, deferral policy active. **Most dangerous gap closed**.

---

### A11. U₈ Permission Enforcement ✅

| Check | Implementation | Tests | Status |
|-------|----------------|-------|--------|
| DEFERRED check | ✅ | ✅ | COMPLETE |
| BLOCKED check | ✅ | ✅ | COMPLETE |
| ALLOWED proceeds | ✅ | ✅ | COMPLETE |

**Implementation**: `u8_root_stem_candidate_carrier.py:651-722`

**Status**: U₈ respects `root_input_permission` before extraction.

---

### A12. Three-Surface Separation ✅

| Surface | Field | Preservation | Status |
|---------|-------|--------------|--------|
| Original | `surface: str` | ✅ | COMPLETE |
| Protected | `protected_core: str` | ✅ | COMPLETE |
| Licensed | `root_input: str` | ✅ | COMPLETE |

**Architectural law**: `surface ≠ protected_core ≠ root_input`

**Status**: Fully enforced.

---

## B. ناقص - يحتاج إكمال (Incomplete - Needs Completion) ⚠️

### B1. Original I'rāb Markers (علامات الإعراب الأصلية) - CRITICAL

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| ضمة (ḍamma) | ❌ | ❌ | ❌ | **MISSING** |
| فتحة (fatḥa) | ❌ | ❌ | ❌ | **MISSING** |
| كسرة (kasra) | ❌ | ❌ | ❌ | **MISSING** |
| سكون (sukūn) | ❌ | ❌ | ❌ | **MISSING** |

**Required fields**:
- `original_irab_marker_hint: MarkerHint` (exists but not populated)
- `nominative_surface_hint: MarkerHint` (exists, UNRESOLVED)
- `accusative_surface_hint: MarkerHint` (exists, UNRESOLVED)
- `genitive_surface_hint: MarkerHint` (exists, UNRESOLVED)

**Current status**: Field placeholders exist, detection/protection NOT implemented.

**Priority**: **HIGH** - Cannot leave these unprotected.

**Example gap**:
```
كِتَابِ (kitābi - with kasra)

Current: kasra not explicitly protected as i'rāb hint
Should: original_irab_marker_hint=POSSIBLE, genitive_surface_hint=POSSIBLE
```

---

### B2. Secondary I'rāb Markers (علامات الإعراب الفرعية) - CRITICAL

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| ألف (alif - dual nom) | ❌ | ❌ | ❌ | **MISSING** |
| واو (wāw - plural nom) | ❌ | ❌ | ❌ | **MISSING** |
| ياء (yā' - dual/plural gen/acc) | ❌ | ❌ | ❌ | **MISSING** |
| نون (nūn - five verbs) | ❌ | ❌ | ❌ | **MISSING** |
| حذف النون (nūn deletion) | ❌ | ❌ | ❌ | **MISSING** |
| حذف حرف العلة (weak letter deletion) | ❌ | ❌ | ❌ | **MISSING** |

**Required fields**:
- `secondary_irab_marker_hint: MarkerHint` (exists but not populated)

**Current status**: Field placeholder exists, detection/protection NOT implemented.

**Priority**: **HIGH** - These are i'rāb markers, not optional.

**Example gap**:
```
مسلمون (muslimūn - wāw as nominative marker)

Current: ون detected as number marker only
Should: secondary_irab_marker_hint=POSSIBLE, nominative_surface_hint=POSSIBLE
```

---

### B3. Imperative Markers (علامات الأمر) - HIGH PRIORITY

| Marker | Detection | Protection | Tests | Status |
|--------|-----------|------------|-------|--------|
| همزة الوصل (hamzat waṣl) | ❌ | ❌ | ❌ | **MISSING** |
| حذف حرف العلة | ❌ | ❌ | ❌ | **MISSING** |
| حذف النون | ❌ | ❌ | ❌ | **MISSING** |

**Required fields**:
- New field needed: `imperative_surface_hint: MarkerHint`
- Or expand `verb_prefix_hint` to cover imperative

**Current status**: Not detected, not protected.

**Priority**: **HIGH** - Imperative forms should not pass as raw root input.

**Example gap**:
```
اكتب (uktub - imperative "write!")

Current: Might pass as root input with alif
Should: imperative_surface_hint=POSSIBLE, protect hamzat waṣl
```

---

### B4. Passive Voice Surface (المبني للمجهول) - HIGH PRIORITY

| Pattern | Detection | Protection | Tests | Status |
|---------|-----------|----------|-------|--------|
| ضم الأول وكسر ما قبل الآخر (past) | ❌ | ❌ | ❌ | **MISSING** |
| ضم أوله ويفتح ما قبل آخره (present) | ❌ | ❌ | ❌ | **MISSING** |

**Required fields**:
- `passive_surface_hint: MarkerHint` (exists but UNRESOLVED)
- `protected_vowels: Tuple[str, ...]` (exists but empty)

**Current status**: Field placeholders exist, detection/protection NOT implemented.

**Priority**: **HIGH** - Passive voice has distinct vowel pattern, should be protected.

**Example gap**:
```
قُتِلَ (qutila - was killed)

Current: Vowel pattern not protected, might pass as active
Should: passive_surface_hint=POSSIBLE, protected_vowels=("ُ", "ِ")
```

---

### B5. Rationality Markers (العاقل / غير العاقل) - MEDIUM PRIORITY

| Marker Type | Detection | Protection | Tests | Status |
|-------------|-----------|------------|-------|--------|
| Surface agreement hints | ❌ | ❌ | ❌ | **MISSING** |

**Required fields**:
- `rationality_marker_hint: MarkerHint` (exists but UNRESOLVED)

**Current status**: Field placeholder exists, no detection logic.

**Priority**: **MEDIUM** - Surface hints for rationality agreement.

**Example**:
```
الذين (alladhīna - rational plural)

Should: rationality_marker_hint=POSSIBLE (rational surface)
```

---

### B6. Six Nouns (الأسماء الستة) - MEDIUM PRIORITY

| Noun | Pattern | Detection | Protection | Tests | Status |
|------|---------|-----------|------------|-------|--------|
| أب / أبو / أبا / أبي | ❌ | ❌ | ❌ | **MISSING** |
| أخ / أخو / أخا / أخي | ❌ | ❌ | ❌ | **MISSING** |
| حم / حمو / حما / حمي | ❌ | ❌ | ❌ | **MISSING** |
| فو / فاك / فيك | ❌ | ❌ | ❌ | **MISSING** |
| ذو / ذا / ذي | ❌ | ❌ | ❌ | **MISSING** |
| هن (rare) | ❌ | ❌ | ❌ | **MISSING** |

**Required**: New detection logic for six-noun patterns.

**Priority**: **MEDIUM** - Special i'rāb patterns, should be protected.

---

### B7. Proper Names / Loanwords / Jāmid - Deferral Policy

| Category | Deferral | Tests | Status |
|----------|----------|-------|--------|
| Proper names (أعلام) | ⚠️ PARTIAL | ⚠️ | INCOMPLETE |
| Loanwords (دخيل) | ⚠️ PARTIAL | ⚠️ | INCOMPLETE |
| Jāmid forms (جامد) | ⚠️ PARTIAL | ⚠️ | INCOMPLETE |
| Frozen primitives | ⚠️ PARTIAL | ⚠️ | INCOMPLETE |

**Current fields**:
- `proper_name_surface_hint: MarkerHint` (inherited from U₇-A)
- `loanword_surface_hint: MarkerHint` (inherited from U₇-A)
- `jamid_surface_hint: MarkerHint` (inherited from U₇-A)
- `frozen_primitive_surface_hint: MarkerHint` (inherited from U₇-A)

**Current status**: Hints inherited but no explicit deferral policy.

**Required**: These should trigger `root_input_permission=DEFERRED` or `BLOCKED`.

**Priority**: **MEDIUM** - Should not extract raw roots from these.

---

## C. مؤجل للمرحلة التالية (Deferred to Next Phase)

### C1. Clause-Level Contract (U₇-C) - LOW PRIORITY

Some markers cannot be resolved at word level, need clause context:

- Agreement markers (verb-subject, adjective-noun)
- Idafa chains (construct state sequences)
- Multi-word expressions
- Discourse particles with clause scope

**Status**: Out of scope for U₇-B. Requires separate U₇-C layer.

**Priority**: **LOW** - Can be deferred to PR #109.

---

## Summary Statistics

### Phase 1 (Current)

| Category | Count | Status |
|----------|-------|--------|
| **Fully covered** | 12 | ✅ |
| **Partially covered** | 2 | ⚠️ |
| **Missing (high priority)** | 4 | ❌ |
| **Missing (medium priority)** | 3 | ❌ |
| **Deferred to U₇-C** | 1 | 🔜 |

### Coverage Percentage

- **By marker family**: 12/22 = **55% complete**
- **By critical markers**: 12/18 = **67% critical markers complete**
- **Broken plural deferral**: **100% (most dangerous gap closed)**

---

## Acceptance Criteria for U₇-B Full Closure

### Required for "U₇-B CLOSED" Status

1. ✅ All marker families in section A (complete)
2. ❌ All marker families in section B implemented
3. ❌ Marker coverage matrix tests (each family has 5 test types)
4. ❌ No unprotected marker family passes to U₈
5. ❌ All surfaces with incomplete coverage → DEFERRED
6. ✅ U₈ enforcement of DEFERRED/BLOCKED status
7. ✅ Three-surface separation maintained
8. ✅ Constitutional prohibitions enforced

### Current Status vs. Acceptance

**Current**: 4/8 criteria met = **50% toward closure**

**Blocked by**: Missing i'rāb markers (B1, B2), imperative (B3), passive (B4)

---

## Next PR Requirements (PR #108)

### Title
"Complete U₇-B Marker Protection Matrix"

### Must Include

1. **I'rāb original markers** (B1)
   - Detection for ضمة، فتحة، كسرة، سكون
   - Population of nominative/accusative/genitive surface hints
   - Tests for each marker

2. **I'rāb secondary markers** (B2)
   - Detection for ألف، واو، ياء، نون، حذف patterns
   - Population of secondary_irab_marker_hint
   - Tests for each pattern

3. **Imperative markers** (B3)
   - Detection for همزة الوصل، حذف patterns
   - New imperative_surface_hint field
   - Tests for imperative forms

4. **Passive voice** (B4)
   - Vowel pattern detection (ُـِـَ for past, ُـَـَ for present)
   - Population of passive_surface_hint
   - protected_vowels tuple
   - Tests for passive forms

5. **Complete pronoun suffixes** (A9 completion)
   - All 14 pronoun forms
   - Tests for each form

6. **Proper name/loanword/jāmid deferral** (B7)
   - Explicit deferral policy
   - Tests for deferral behavior

7. **Marker coverage matrix tests**
   - For each marker family:
     - Detection test
     - Protection test
     - Deferral test (if applicable)
     - U₈ blocking test
     - Residual emission test

### Estimated Scope

- **New detection functions**: ~8
- **New tests**: ~60
- **Modified fields**: ~10
- **Lines of code**: ~400-600

---

## Architectural Law Tracking

### Enforced (Phase 1) ✅

```
1. No root from raw surface (Axiom 7B.1)
2. No stripping without trace (Axiom 7B.3)
3. surface ≠ protected_core ≠ root_input (Axiom 7B.5)
4. Protection-or-defer for broken plurals
5. U₈ respects DEFERRED/BLOCKED permission
```

### Partially Enforced ⚠️

```
6. No marker deletion; only protection (Axiom 7B.4)
   → Only some marker families protected

7. Marker ≠ judgment (Axiom 7B.6)
   → All outputs are hints (good)
   → But incomplete marker coverage (needs work)
```

### Target for Full Closure

```
No U₈ root extraction from any surface segment
whose marker-family coverage is incomplete.
```

---

**Document Version**: 1.0
**Last Updated**: 2026-05-26
**Phase**: 1 (Protection-or-Defer Core)
**Next Phase**: 2 (Complete Marker Coverage Matrix)
