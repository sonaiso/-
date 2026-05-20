# K.5: طبقة الصحة والاعتلال والهمز والتضعيف

# K.5: Verb Health Classification Layer Coverage Matrix

**Layer**: K.5
**Domain**: Template (D4) + Origin (D3)
**Status**: ❌ Not Implemented
**Version**: 1.0.0
**Depends On**: K.4 (Template Transformation) - **CRITICAL DEPENDENCY**

---

## المبدأ الأساسي (Core Principle)

```
بدون طبقة الصحة:
- الأوزان العميقة تفشل
- المصادر تفشل
- المشتقات تفشل

(Without verb health layer:
- Deep templates fail
- Masdars fail
- Derivations fail)
```

---

## Required Concepts (المفاهيم المطلوبة)

### 1. صحيح (Sound/Healthy Verbs)

#### صحيح سالم (Sound, No Weak Letters, No Hamza, No Doubling)
- Examples: ك ت ب، د ر س، ف ت ح
- All three root letters are strong consonants
- No special phonological behavior

#### صحيح مهموز (Contains Hamza)
- **مهموز الفاء**: أ خ ذ، أ م ر (hamza as first radical)
- **مهموز العين**: س أ ل، ر أ س (hamza as second radical)
- **مهموز اللام**: ق ر أ، ب د أ (hamza as third radical)

#### صحيح مضعف (Doubled Middle Radical)
- **مضعف ثلاثي**: ش د د، م د د، ر د د (C₁C₂C₂)
- **مضعف رباعي**: ز ل ز ل، و س و س (C₁C₂C₁C₂)

### 2. معتل (Weak Verbs - Containing Weak Letters و/ي)

#### مثال (First Radical is Weak)
- **مثال واوي**: و ع د، و ج د، و ص ل (و as first)
- **مثال يائي**: ي س ر، ي م ن (ي as first - rare)
- Special behavior: و often deletes in forms

#### أجوف (Middle Radical is Weak - Hollow)
- **أجوف واوي**: ق و ل، ص و م، ع و د (و as middle)
- **أجوف يائي**: ب ي ع، س ي ر، ط ي ر (ي as middle)
- Special behavior: weak letter → alif in past, kept or transformed in present

#### ناقص (Final Radical is Weak - Defective)
- **ناقص واوي**: د ع و، غ ز و (و as final)
- **ناقص يائي**: ر م ي، ب ك ي، ق ض ي (ي as final)
- Special behavior: final weak letter → alif maqsura or deleted

#### لفيف (Two Weak Letters)
- **لفيف مفروق**: و ق ي، و ف ي (weak at positions 1 and 3)
- **لفيف مقرون**: ط و ي، ر و ي، ح ي ي (weak at positions 2 and 3)
- Combines behaviors of both weak positions

---

## Allowed Claims (الادعاءات المسموحة)

After full implementation:

- ❌ `VerbHealthCandidate` - Health classification
- ❌ `WeakLetterPositionCandidate` - Position of weak letter(s)
- ❌ `WeakLetterIdentityCandidate` - Original و or ي?
- ❌ `HamzaPositionCandidate` - Position of hamza
- ❌ `DoublingPatternCandidate` - Doubled radical pattern
- ❌ `VerbHealthBehaviorPredictor` - Predicts conjugation behavior

---

## Forbidden Claims (الادعاءات الممنوعة)

- ❌ `VerbHealthCertificate` without lexicon (for و/ي ambiguity)
- ❌ Health classification without template analysis (depends on K.4)
- ❌ Weak letter identity without lexicon attestation
- ❌ Behavior prediction without health classification

---

## Requires Lexicon? (تحتاج معجم؟)

**Yes - Critical** for:
- **Determining و vs ي** in weak verbs (قال: واوي، باع: يائي)
- Irregular weak verb behavior
- Historical weak letter changes
- Anomalous health patterns

**No** for:
- Hamza detection (visible in surface)
- Doubled radical detection (shadda visible)
- Weak letter position (after template analysis)

---

## Requires Context? (تحتاج سياق؟)

**No** for single word:
- Health classification
- Weak letter position
- Hamza position

---

## Failure Types (أنواع الفشل)

### Residuals

- `WEAK_LETTER_IDENTITY_AMBIGUITY` - Cannot determine original و vs ي
- `VERB_HEALTH_UNRESOLVED` - Unclear health classification
- `HAMZA_POSITION_UNCLEAR` - Hamza position ambiguous
- `DOUBLING_PATTERN_UNRESOLVED` - Unclear if doubled
- `WEAK_LETTER_POSITION_CONFLICT` - Conflicting position evidence
- `HEALTH_TEMPLATE_MISMATCH` - Health doesn't match template
- `LEXICON_REQUIRED_FOR_HEALTH` - Must consult lexicon

---

## Golden Tests (الاختبارات الذهبية)

### Test Set 1: صحيح سالم (Sound)

| Root | Surface (Past) | Health | Evidence |
|------|----------------|--------|----------|
| ك ت ب | كَتَبَ | صحيح سالم | No hamza, no weak, no doubling |
| د ر س | دَرَسَ | صحيح سالم | All strong consonants |
| ف ت ح | فَتَحَ | صحيح سالم | All strong consonants |

### Test Set 2: مهموز (Hamza)

| Root | Surface | Hamza Position | Health |
|------|---------|----------------|--------|
| أ خ ذ | أَخَذَ | Faa (first) | مهموز الفاء |
| س أ ل | سَأَلَ | Ayn (middle) | مهموز العين |
| ق ر أ | قَرَأَ | Lam (final) | مهموز اللام |

### Test Set 3: مضعف (Doubled)

| Root | Surface | Doubling | Health |
|------|---------|----------|--------|
| ش د د | شَدَّ | C₂ = C₃ | مضعف ثلاثي |
| م د د | مَدَّ | C₂ = C₃ | مضعف ثلاثي |
| ز ل ز ل | زَلْزَلَ | C₁C₂C₁C₂ | مضعف رباعي |

### Test Set 4: مثال (First Weak)

| Root | Surface (Past) | Surface (Present) | Weak Letter | Health |
|------|----------------|-------------------|-------------|--------|
| و ع د | وَعَدَ | يَعِدُ (و deleted) | و | مثال واوي |
| و ج د | وَجَدَ | يَجِدُ (و deleted) | و | مثال واوي |
| ي س ر | يَسَرَ | يَيْسِرُ (ي retained) | ي | مثال يائي |

### Test Set 5: أجوف (Middle Weak) - **CRITICAL**

| Root | Deep | Surface (Past) | Surface (Present) | Original | Health |
|------|------|----------------|-------------------|----------|--------|
| ق و ل | قَوَلَ | قَالَ | يَقُولُ | و | أجوف واوي |
| ب ي ع | بَيَعَ | بَاعَ | يَبِيعُ | ي | أجوف يائي |
| ن و م | نَوَمَ | نَامَ | يَنَامُ | و | أجوف واوي |
| س ي ر | سَيَرَ | سَارَ | يَسِيرُ | ي | أجوف يائي |

**Critical Note**: Determining و vs ي requires lexicon or paradigm analysis.

### Test Set 6: ناقص (Final Weak)

| Root | Deep | Surface (Past) | Surface (Present) | Original | Health |
|------|------|----------------|-------------------|----------|--------|
| د ع و | دَعَوَ | دَعَا | يَدْعُو | و | ناقص واوي |
| ر م ي | رَمَيَ | رَمَى | يَرْمِي | ي | ناقص يائي |
| ق ض ي | قَضَيَ | قَضَى | يَقْضِي | ي | ناقص يائي |

### Test Set 7: لفيف (Two Weak Letters)

| Root | Type | Positions | Health |
|------|------|-----------|--------|
| و ق ي | مفروق | 1 + 3 | لفيف مفروق |
| و ف ي | مفروق | 1 + 3 | لفيف مفروق |
| ط و ي | مقرون | 2 + 3 | لفيف مقرون |
| ح ي ي | مقرون | 2 + 3 | لفيف مقرون |

---

## Current Status

### ✅ Implemented
- None

### ❌ Missing (Everything)
- VerbHealthCandidate contract
- Weak letter detection
- Hamza position classification
- Doubling pattern detection
- Weak letter identity resolver (و vs ي)
- Health-based behavior prediction
- Lexicon integration for weak letter identity

---

## Evidence Artifacts

### Required Files

```
src/dal_core/
├── verb_health.py (❌ needed - main contract)
├── weak_letter_detector.py (❌ needed)
├── weak_letter_identity.py (❌ needed - critical)
├── hamza_classifier.py (❌ needed)
├── doubling_detector.py (❌ needed)
└── health_behavior_predictor.py (❌ needed)

tests/dal_core/
├── test_verb_health.py (❌ needed: 30 tests)
├── test_weak_letter_identity.py (❌ needed: 25 tests - critical)
├── test_hamza_position.py (❌ needed: 15 tests)
├── test_doubling_pattern.py (❌ needed: 10 tests)
└── test_health_behavior.py (❌ needed: 20 tests)

data/verb_health/
├── weak_verb_lexicon.json (❌ needed - و vs ي)
├── irregular_weak_verbs.json (❌ needed)
└── hamza_verb_patterns.json (❌ needed)
```

**Total**: 100+ tests minimum

---

## Gap Analysis

### Critical Dependency

**K.5 CANNOT BE IMPLEMENTED WITHOUT K.4**

Reason:
- Need deep/surface template distinction
- Need i'lal trace to identify weak letters
- Need transformation rules to determine original form

### Critical Gaps

1. **No Weak Letter Identity Resolver (و vs ي)**
   - Impact: Cannot distinguish قال (واوي) from باع (يائي) without lexicon
   - Priority: **Critical**

2. **No Health Classifier**
   - Impact: Cannot classify verb types
   - Priority: **Critical**

3. **No Lexicon Integration**
   - Impact: Cannot resolve و/ي ambiguity
   - Priority: **Critical**

### Implementation Order

**Must implement K.4 first**, then:
1. **Phase 1** (PR #31): VerbHealthCandidate + weak letter detector
2. **Phase 2** (PR #32): Weak letter identity + lexicon integration
3. **Phase 3** (PR #33): Health-based behavior prediction

**Estimated**: 4-5 weeks (after K.4 is complete)

---

## Cross-References

- **K.4-TEMPLATE-TRANSFORMATION-MATRIX.md** - **Required prerequisite**
- `K.2-PHONOLOGY-COVERAGE-MATRIX.md` - I'lal rules
- `K.3-ORIGIN-SEGMENTATION-MATRIX.md` - Root extraction
- `K.10-LEXICON-ATTESTATION-MATRIX.md` - Weak letter identity resolution

---

**Status**: ❌ Not Implemented (0%)
**Blocker**: K.4 must be implemented first
**Next**: Wait for K.4, then implement VerbHealthCandidate
**Estimated**: 4-5 weeks after K.4
