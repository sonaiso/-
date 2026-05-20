# K.1: طبقة الرسم والضبط

# K.1: Grapho-Orthographic Layer Coverage Matrix

**Layer**: K.1
**Domain**: Graphophonemic (D0)
**Status**: 🚧 Partial (Carrier exists, detailed contracts missing)
**Version**: 1.0.0

---

## Required Concepts (المفاهيم المطلوبة)

### 1. Orthographic Scripts (أنواع الرسم)
- ✅ الرسم الإملائي (Standard orthography)
- ⚠️ الرسم العثماني (Uthmanic script for Quran)
- ⚠️ الرسم المغربي (Maghribi variant)

### 2. Hamza Representations (الهمزات)
- ⚠️ همزة القطع (Hamzat al-qat': أ، إ)
- ⚠️ همزة الوصل (Hamzat al-wasl: ا)
- ⚠️ همزة على الألف (Hamza on alif: أ، إ، آ)
- ⚠️ همزة على الواو (Hamza on waw: ؤ)
- ⚠️ همزة على الياء (Hamza on ya: ئ)
- ⚠️ همزة على السطر (Hamza on line: ء)

### 3. Taa Representations (أنواع التاء)
- ⚠️ التاء المربوطة (Taa marbuta: ة)
- ⚠️ التاء المفتوحة (Taa maftuha: ت)
- ⚠️ الهاء (Ha: ه - can be confused with taa marbuta)

### 4. Alif Representations (أنواع الألف)
- ⚠️ الألف الممدودة (Long alif: ا)
- ⚠️ الألف المقصورة (Alif maqsura: ى)
- ⚠️ ألف المد (Alif madd)
- ⚠️ ألف الوصل (Alif wasl)

### 5. Diacritics - Structural (الحركات البنيوية)
- ✅ الفتحة (Fatha: َ)
- ✅ الضمة (Damma: ُ)
- ✅ الكسرة (Kasra: ِ)
- ✅ السكون (Sukun: ْ)
- ✅ الشدة (Shadda: ّ)
- ✅ التنوين (Tanwin: ً ٌ ٍ)

### 6. Diacritics - I'rab (الحركات الإعرابية)
- ✅ حركة إعرابية (I'rab marking)
- ✅ حركة بناء (Binaa marking - fixed)
- ⚠️ حركة تقديرية (Estimated/hidden marking)

### 7. Long Vowels (حروف المد)
- ✅ الألف (Alif: ا)
- ✅ الواو (Waw: و)
- ✅ الياء (Ya: ي)

### 8. Waqf and Wasl (الوقف والوصل)
- ⚠️ الوقف (Pause: affects final marking)
- ⚠️ الوصل (Connection: affects hamzat al-wasl)
- ⚠️ حذف/إثبات في الوصل (Deletion/retention in connection)

### 9. Orthographic Normalization (التطبيع الإملائي)
- ✅ Unicode normalization
- ⚠️ Hamza normalization variants
- ⚠️ Alif normalization variants
- ⚠️ Taa/ha disambiguation

---

## Allowed Claims (الادعاءات المسموحة)

After full implementation:

- ✅ `GraphemeCandidate` - Grapheme identification candidate
- ✅ `DiacriticCandidate` - Diacritic classification candidate
- ⚠️ `HamzaPositionCandidate` - Hamza position analysis
- ⚠️ `TaaTypeCandidate` - Taa marbuta vs maftuha vs ha
- ⚠️ `AlifTypeCandidate` - Alif variants
- ⚠️ `OrthographicNormalizationCandidate` - Normalized form
- ⚠️ `WaqfWaslEffect` - Pause/connection effects

---

## Forbidden Claims (الادعاءات الممنوعة)

- ❌ `GraphemeCertificate` without orthographic attestation
- ❌ `HamzaCertificate` without dictionary/rule evidence
- ❌ Mixing orthography with phonology (رسم ≠ نطق)
- ❌ Direct promotion from grapheme to morphological pattern
- ❌ Semantic interpretation from orthography alone

---

## Requires Lexicon? (تحتاج معجم؟)

**Yes** for:
- Uthmanic script (Quranic orthography)
- Irregular hamza positions (شذوذ)
- Irregular orthography (proper names, loanwords)
- Taa marbuta in proper names (فاطمة، طلحة)
- Historical orthographic variants

**No** for:
- Standard Unicode graphemes
- Regular diacritic positions
- Standard hamza rules

---

## Requires Context? (تحتاج سياق؟)

**Yes** for:
- Waqf/wasl effects (pause at end of sentence vs connection)
- Hamzat al-wasl deletion (beginning of speech vs middle)
- Estimated i'rab markings (context determines visibility)

**No** for:
- Basic grapheme identification
- Diacritic classification
- Unicode normalization

---

## Failure Types (أنواع الفشل)

### Residuals

- `HAMZA_NORMALIZATION_FAILURE` - Multiple hamza variants, no clear choice
- `TAA_MARBUTA_HA_AMBIGUITY` - Cannot distinguish ة from ه
- `ALIF_MAQSURA_AMBIGUITY` - Cannot determine ى vs ا
- `DIACRITIC_INCONSISTENCY` - Conflicting diacritics
- `WAQF_WASL_CONTEXT_MISSING` - Cannot determine pause/connection effect
- `ORTHOGRAPHIC_VARIANT_UNRESOLVED` - Multiple valid orthographic forms
- `UTHMANIC_STANDARD_CONFLICT` - Quranic vs standard orthography mismatch

### Error Conditions

```python
# Example residual generation
if has_multiple_hamza_forms and not has_attestation:
    residual = Residual(
        type="HAMZA_NORMALIZATION_FAILURE",
        domain=DalDomain.GRAPHOPHONEMIC,
        evidence=("Multiple hamza variants detected",),
        blocker=False,  # Can proceed with candidates
    )
```

---

## Golden Tests (الاختبارات الذهبية)

### Test Set 1: Hamza Variants

| Surface | Hamza Type | Expected Analysis | Context |
|---------|------------|-------------------|---------|
| أَخَذَ | قطع على الألف | `HamzaQat`, position=alif_above | Initial, fatha |
| إِنَّ | قطع تحت الألف | `HamzaQat`, position=alif_below | Initial, kasra |
| سَأَلَ | همزة على الألف | `HamzaMutawassita`, position=alif | Medial, fatha |
| قَرَأَ | همزة على الألف | `HamzaMutawassita`, position=alif | Final |
| سُؤَال | همزة على الواو | `HamzaMutawassita`, position=waw | Medial, damma before |
| شَيْء | همزة على السطر | `HamzaMutawassita`, position=line | Final after sukun |
| ائْتِ | همزة وصل | `HamzaWasl` | Initial in imperative |
| الكِتَاب | همزة وصل | `HamzaWasl` | Definite article |

### Test Set 2: Taa Variants

| Surface | Type | Expected Analysis | Evidence |
|---------|------|-------------------|----------|
| فَاطِمَة | تاء مربوطة | `TaaMarbuta`, context=proper_name_feminine | Feminine proper name |
| كِتَابَة | تاء مربوطة | `TaaMarbuta`, context=common_noun_feminine | Feminine noun |
| كَتَبَتْ | تاء مفتوحة | `TaaMaftuha`, context=verb_feminine_marker | Verb feminine marker |
| هَذَا | هاء | `Ha`, context=demonstrative | Not taa |
| اللَّهُ | هاء | `Ha`, context=proper_name_allah | Allah name |

### Test Set 3: Alif Variants

| Surface | Type | Expected Analysis | Evidence |
|---------|------|-------------------|----------|
| كَتَبَ | ألف فتحة | Fatha (short), not alif | No long vowel |
| كَاتِب | ألف مد | `AlifMadd` | Long vowel |
| فَتَى | ألف مقصورة | `AlifMaqsura` | Final ya-alif |
| مُوسَى | ألف مقصورة | `AlifMaqsura` | Proper name |
| هُدًى | ألف مقصورة | `AlifMaqsura` | With tanwin |

### Test Set 4: Waqf and Wasl

| Surface | Context | Expected Effect | Evidence |
|---------|---------|-----------------|----------|
| الكِتَابُ | Beginning of speech | Hamza wasl pronounced | Speech-initial |
| وَالكِتَابُ | Middle of speech | Hamza wasl deleted | After conjunction |
| كِتَابٌ | Waqf (pause) | Tanwin → sukun | Sentence-final |
| كِتَابٌ | Wasl (connection) | Tanwin retained | Mid-sentence |

### Test Set 5: Diacritic Consistency

| Surface | Expected Validation | Pass/Fail |
|---------|---------------------|-----------|
| كَتَبَ | All diacritics consistent | ✅ Pass |
| كَتَبَ (with shadda on non-doubled) | Inconsistent shadda | ❌ Fail |
| كََتَب (double fatha) | Duplicate diacritic | ❌ Fail |
| كتب (no diacritics) | Ambiguous but valid | ⚠️ Pass with residual |

---

## Current Status (الحالة الحالية)

### ✅ Implemented

- Basic grapheme identification (`Carrier`)
- Unicode handling
- Basic diacritic classification
- Shadda detection
- Tanwin detection

### 🚧 Partial

- Hamza normalization (basic rules exist, comprehensive classification missing)
- Taa/ha disambiguation (heuristics exist, lexicon-based resolution missing)
- Alif variants (basic handling, comprehensive classification missing)

### ❌ Missing

- `HamzaPositionCandidate` contract
- `TaaTypeCandidate` contract
- `AlifTypeCandidate` contract
- `WaqfWaslEffect` contract
- Uthmanic script handling
- Orthographic attestation database
- Waqf/wasl context analyzer

---

## Evidence Artifacts (أثر الدليل)

### Required Files

```
src/dal_core/
├── carriers.py (✅ exists)
├── grapheme_candidates.py (❌ needed)
├── hamza_analyzer.py (❌ needed)
├── taa_analyzer.py (❌ needed)
├── alif_analyzer.py (❌ needed)
├── waqf_wasl_analyzer.py (❌ needed)
└── orthographic_normalization.py (⚠️ basic exists)

tests/dal_core/
├── test_carriers.py (✅ exists)
├── test_grapheme_candidates.py (❌ needed: 25 tests)
├── test_hamza_analyzer.py (❌ needed: 15 tests)
├── test_taa_analyzer.py (❌ needed: 10 tests)
├── test_alif_analyzer.py (❌ needed: 10 tests)
└── test_waqf_wasl_analyzer.py (❌ needed: 8 tests)

data/orthography/
├── hamza_attestation.json (❌ needed)
├── uthmanic_variants.json (❌ needed)
└── orthographic_exceptions.json (❌ needed)
```

### Test Coverage Requirements

- **Hamza**: 15+ tests covering all 6 positions
- **Taa/Ha**: 10+ tests for disambiguation
- **Alif**: 10+ tests for variants
- **Waqf/Wasl**: 8+ tests for context effects
- **Diacritics**: 12+ tests for consistency
- **Normalization**: 10+ tests for edge cases

**Total**: 65+ tests minimum

---

## Gap Analysis (تحليل الفجوات)

### Critical Gaps

1. **No Hamza Classification Contract**
   - Impact: Cannot properly analyze words with hamza
   - Blocks: Template matching, root extraction
   - Priority: High

2. **No Taa/Ha Disambiguation**
   - Impact: Gender analysis unreliable
   - Blocks: Proper name handling, gender classification
   - Priority: High

3. **No Waqf/Wasl Analyzer**
   - Impact: Cannot handle sentence boundaries
   - Blocks: Composition context analysis
   - Priority: Medium

4. **No Orthographic Attestation**
   - Impact: Cannot handle irregular orthography
   - Blocks: Proper names, Quranic text, loanwords
   - Priority: Medium

### Implementation Priority

1. **Phase 1** (PR #30): Hamza + Taa/Ha classification
2. **Phase 2** (PR #31): Alif variants + normalization
3. **Phase 3** (PR #32): Waqf/wasl context + attestation

---

## Cross-References

- `carriers.py` - Current basic grapheme handling
- `D0: GRAPHOPHONEMIC` - Domain in dal_algebra
- `K.2-PHONOLOGY-COVERAGE-MATRIX.md` - Phonological layer (distinct from orthography)
- `K.10-LEXICON-ATTESTATION-MATRIX.md` - Lexicon for irregular orthography

---

**Status**: 🚧 Partial (40% complete)
**Next**: Implement HamzaPositionCandidate contract
**Estimated**: 3-4 weeks for full coverage
