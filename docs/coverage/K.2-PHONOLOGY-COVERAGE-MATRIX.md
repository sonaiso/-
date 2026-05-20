# K.2: طبقة الصوت والمقطع

# K.2: Phonological-Syllabic Layer Coverage Matrix

**Layer**: K.2
**Domain**: Syllabic (D1)
**Status**: 🚧 Partial (Syllable exists, phonological rules missing)
**Version**: 1.0.0

---

## Critical Principle (المبدأ الحرج)

```
المقطع الصوتي ≠ الوزن الصرفي
(Syllable ≠ Morphological Pattern)
```

**المقطع** (syllable) is **descriptive** (D1: SYLLABIC).
**الوزن** (wazn/pattern) is **judgmental** (D4: TEMPLATE).

**No direct promotion from D1 → D4.**

---

## Required Concepts (المفاهيم المطلوبة)

### 1. Phoneme Inventory (الفونيمات)

#### Consonants (الصوامت)
- ✅ 28 Arabic consonants
- ✅ Emphatic vs non-emphatic (مفخم vs مرقق)
- ⚠️ Sun letters vs moon letters (حروف شمسية vs قمرية)

#### Vowels (الصوائت)
- ✅ Short vowels: a (fatha), u (damma), i (kasra)
- ✅ Long vowels: aa (alif), uu (waw), ii (ya)
- ✅ Sukun (zero vowel)

### 2. Syllable Types (أنواع المقاطع)

- ✅ CV (صَ)
- ✅ CVV (صَا، صُو، صِي)
- ✅ CVC (صَبْ)
- ✅ CVVC (صَابْ)
- ⚠️ CVCC (صَبْت - rare, mostly in pause)
- ⚠️ VV, VC (in particles like إِلَى)

### 3. Syllable Boundaries (حدود المقاطع)

- ✅ Syllable segmentation
- ⚠️ Resyllabification (إعادة تقطيع)
- ⚠️ Epenthesis at boundaries (كسر التقاء الساكنين)

### 4. Phonological Rules (القواعد الصوتية)

#### Idgham (الإدغام)
- ⚠️ إدغام بغنة (with nasalization: ن، م)
- ⚠️ إدغام بلا غنة (without nasalization: ل، ر)
- ⚠️ إدغام المتقاربين (similar consonants)
- ⚠️ إدغام المتجانسين (identical consonants)
- ⚠️ إدغام المتماثلين (same consonants)

#### I'lal (الإعلال)
- ⚠️ قلب (transformation: و/ي → ا)
- ⚠️ حذف (deletion: weak letter deletion)
- ⚠️ نقل (transfer: haraka shift)
- ⚠️ تسكين (vowel deletion)

#### Deletion (الحذف)
- ⚠️ حذف حرف العلة (weak letter deletion)
- ⚠️ حذف همزة الوصل (hamzat wasl deletion)
- ⚠️ حذف الألف في الوصل (alif deletion in connection)

#### Transformation (القلب)
- ⚠️ انقلاب الواو ألفًا (waw → alif)
- ⚠️ انقلاب الياء ألفًا (ya → alif)
- ⚠️ انقلاب التاء طاءً (ta → ta' - in افتعل)

#### Sakin Meeting (التقاء الساكنين)
- ⚠️ كسر الأول (vowel insertion on first)
- ⚠️ حذف الأول (deletion of first)
- ⚠️ همزة الوصل (epenthetic hamza)

#### Economy (الاقتصاد الصوتي)
- ⚠️ Syllable economy constraints
- ⚠️ Preferred syllable structures
- ⚠️ Avoidance of heavy clusters

---

## Allowed Claims (الادعاءات المسموحة)

After full implementation:

- ✅ `PhonemeCandidate` - Phoneme identification
- ✅ `SyllableCandidate` - Syllable structure (already exists)
- ✅ `SyllableBoundaryCandidate` - Syllable boundaries
- ⚠️ `IdghamRuleCandidate` - Assimilation rule application
- ⚠️ `IlalRuleCandidate` - Vowel change rule
- ⚠️ `DeletionRuleCandidate` - Deletion rule
- ⚠️ `TransformationRuleCandidate` - Sound transformation
- ⚠️ `SakinMeetingResolutionCandidate` - Sakin clash resolution
- ⚠️ `PhonologicalEconomyScore` - Syllable economy measure

---

## Forbidden Claims (الادعاءات الممنوعة)

- ❌ `SyllableCertificate` without phonological rule evidence
- ❌ Direct promotion: SYLLABIC → TEMPLATE (محظور جبريًا)
- ❌ Direct promotion: SYLLABIC → ORIGIN (محظور جبريًا)
- ❌ Using syllable count to determine binaa/i'rab (هلوسة)
- ❌ Syllable-based morphological judgment
- ❌ Phoneme inventory as linguistic axiom (must emerge from F-constraints)

---

## Requires Lexicon? (تحتاج معجم؟)

**Yes** for:
- Irregular phonological patterns (شواذ)
- Loanword phonology
- Dialectal variants
- Historical phonological changes

**No** for:
- Standard syllable identification
- Regular phonological rules
- Phoneme classification

---

## Requires Context? (تحتاج سياق؟)

**Yes** for:
- Idgham in composition (across word boundaries)
- Sakin meeting at word juncture
- Resyllabification in connected speech
- Sun/moon letter assimilation (with ال)

**No** for:
- Single word syllabification
- Phoneme inventory
- Basic syllable types

---

## Failure Types (أنواع الفشل)

### Residuals

- `INVALID_SYLLABLE_STRUCTURE` - Syllable doesn't match Arabic patterns
- `SAKIN_MEETING_FAILURE` - Two sukuns meet, no resolution
- `IDGHAM_CONTEXT_MISSING` - Assimilation requires context
- `ILAL_RULE_UNRESOLVED` - Multiple possible i'lal rules
- `TRANSFORMATION_RULE_UNRESOLVED` - Unclear transformation
- `SYLLABLE_ECONOMY_VIOLATION` - Violates economy constraints
- `RESYLLABIFICATION_AMBIGUITY` - Multiple syllabification candidates
- `PHONOLOGICAL_RULE_CONFLICT` - Competing phonological rules

### Error Conditions

```python
# Example: Sakin meeting without resolution
if has_adjacent_sukuns and not has_context:
    residual = Residual(
        type="SAKIN_MEETING_FAILURE",
        domain=DalDomain.SYLLABIC,
        evidence=("Two sukuns detected without resolution context",),
        blocker=True,  # Cannot proceed
    )
```

---

## Golden Tests (الاختبارات الذهبية)

### Test Set 1: Basic Syllable Types

| Surface | Syllabification | Syllable Types | Evidence |
|---------|-----------------|----------------|----------|
| كَتَبَ | ka-ta-ba | CV-CV-CV | All open syllables |
| كِتَاب | ki-taab | CV-CVVC | One long, one closed |
| كُتُب | ku-tub | CV-CVC | One open, one closed |
| مَكْتَب | mak-tab | CVC-CVC | Two closed |
| مَكْتَبَة | mak-ta-ba | CVC-CV-CV | Mixed |
| اِسْتِخْرَاج | is-tikh-raaj | VC-CVC-CVVC | Initial vowel |

### Test Set 2: I'lal (Vowel Changes)

| Surface | Deep Form | I'lal Rule | Evidence |
|---------|-----------|------------|----------|
| قَالَ | قَوَلَ | قلب: و → ا | Waw → alif transformation |
| يَقُولُ | يَقْوُلُ | No i'lal | Waw retained (not in context) |
| قُلْ | قُوْلْ | حذف: deletion of waw | Imperative deletion |
| بَاعَ | بَيَعَ | قلب: ي → ا | Ya → alif transformation |
| يَبِيعُ | يَبْيِعُ | No i'lal | Ya retained |

### Test Set 3: Idgham (Assimilation)

| Surface | Context | Idgham Type | Result |
|---------|---------|-------------|--------|
| مِنْ مَا | Composition | Idgham mutamathibin | مِمَّا |
| مِنْ لَ | Composition | Idgham mutaqaribin | No idgham (optional) |
| الشَّمْس | With ال | Sun letter assimilation | اَشْ-شَمْس |
| الْقَمَر | With ال | Moon letter (no assimilation) | اَلْ-قَمَر |

### Test Set 4: Sakin Meeting

| Surface | Problem | Resolution | Result |
|---------|---------|------------|--------|
| مِنْ ٱلْبَيْت | ن sukun + ل sukun | Kasra insertion | مِنَ ٱلْبَيْت |
| قُلْ ٱرْجِعْ | ل sukun + ا vowel | Hamzat wasl | قُلِ ٱرْجِعْ |
| يَكْتُبْ + نَ | ب sukun + ن | Vowel on ب | يَكْتُبُنَ (or delete ن) |

### Test Set 5: Syllable Economy

| Surface | Syllable Count | Economy Score | Assessment |
|---------|----------------|---------------|------------|
| هَذَا | 2 | Optimal | Short functional |
| كَاتِبٌ | 3 | Optimal | Standard noun |
| اِسْتِخْرَاج | 3 | Heavy but valid | Derived form |
| يَسْتَخْرِجُونَ | 5 | Complex but valid | Verb with suffix |

### Test Set 6: Phoneme Classification

| Phoneme | Type | Features | Evidence |
|---------|------|----------|----------|
| /k/ ك | Consonant | Voiceless, velar | Standard |
| /q/ ق | Consonant | Voiceless, uvular | Emphatic |
| /t/ ت | Consonant | Voiceless, dental | Standard |
| /ṭ/ ط | Consonant | Voiceless, emphatic | Emphatic |
| /a/ َ | Vowel | Short, low | Fatha |
| /aa/ ا | Vowel | Long, low | Alif |

---

## Current Status (الحالة الحالية)

### ✅ Implemented

- Basic syllable identification (`Syllable`)
- Syllable types (CV, CVC, CVV, CVVC)
- Syllable count
- Basic phoneme inventory

### 🚧 Partial

- Syllable boundary detection (basic heuristics exist)
- Sun/moon letter handling (for ال prefix)

### ❌ Missing

- `PhonologicalRuleCandidate` contract
- `IdghamRuleCandidate` contract
- `IlalRuleCandidate` contract
- `DeletionRuleCandidate` contract
- `TransformationRuleCandidate` contract
- `SakinMeetingResolutionCandidate` contract
- Comprehensive phonological rule engine
- Resyllabification analyzer
- Phonological economy scorer
- Context-sensitive idgham
- I'lal trace tracking

---

## Evidence Artifacts (أثر الدليل)

### Required Files

```
src/dal_core/
├── syllables.py (✅ exists - basic)
├── phoneme_inventory.py (❌ needed)
├── phonological_rules.py (❌ needed)
├── idgham_analyzer.py (❌ needed)
├── ilal_analyzer.py (❌ needed)
├── sakin_meeting_resolver.py (❌ needed)
├── syllable_economy.py (❌ needed)
└── resyllabification.py (❌ needed)

tests/dal_core/
├── test_syllables.py (✅ exists - basic)
├── test_phoneme_inventory.py (❌ needed: 15 tests)
├── test_idgham_analyzer.py (❌ needed: 20 tests)
├── test_ilal_analyzer.py (❌ needed: 25 tests)
├── test_sakin_meeting.py (❌ needed: 15 tests)
├── test_syllable_economy.py (❌ needed: 10 tests)
└── test_axis_promotion_ban.py (✅ exists - prohibits SYLLABIC→BINAA)

data/phonology/
├── idgham_rules.json (❌ needed)
├── ilal_rules.json (❌ needed)
└── phonological_exceptions.json (❌ needed)
```

### Test Coverage Requirements

- **Syllable Types**: 15+ tests
- **Idgham**: 20+ tests (all types)
- **I'lal**: 25+ tests (قلب، حذف، نقل)
- **Sakin Meeting**: 15+ tests
- **Syllable Economy**: 10+ tests
- **Resyllabification**: 10+ tests
- **Axis Promotion Ban**: 8+ tests (already exists)

**Total**: 113+ tests minimum

---

## Gap Analysis (تحليل الفجوات)

### Critical Gaps

1. **No Phonological Rule Engine**
   - Impact: Cannot trace i'lal transformations
   - Blocks: Deep template analysis (K.4), verb health (K.5)
   - Priority: Critical

2. **No I'lal Analyzer**
   - Impact: Cannot connect deep forms to surface forms
   - Blocks: Root extraction, pattern matching
   - Priority: Critical

3. **No Idgham Rules**
   - Impact: Cannot analyze assimilation
   - Blocks: Composition analysis
   - Priority: High

4. **No Sakin Meeting Resolver**
   - Impact: Cannot handle word boundaries
   - Blocks: Composition, sentence analysis
   - Priority: High

### Blocker for Other Layers

This layer **blocks**:
- **K.4**: Template transformation (needs i'lal trace)
- **K.5**: Verb health (needs weak letter identification)
- **K.3**: Root extraction (needs phonological normalization)

### Implementation Priority

1. **Phase 1** (PR #30): I'lal analyzer + transformation trace
2. **Phase 2** (PR #31): Idgham rules + sakin meeting
3. **Phase 3** (PR #32): Economy + resyllabification

---

## Cross-References

- `syllables.py` - Current basic syllable handling
- `D1: SYLLABIC` - Domain in dal_algebra
- `K.1-ORTHOGRAPHY-COVERAGE-MATRIX.md` - Orthographic layer (رسم ≠ نطق)
- `K.4-TEMPLATE-TRANSFORMATION-MATRIX.md` - Needs i'lal trace
- `K.5-VERB-HEALTH-MATRIX.md` - Needs weak letter classification
- `MUFRAD_AXES.md` - Prohibits SYLLABIC → BINAA hallucination
- `dal_algebra.py:FORBIDDEN_AXIS_PROMOTIONS` - Enforces ban

---

**Status**: 🚧 Partial (30% complete)
**Next**: Implement IlalRuleCandidate + transformation trace
**Estimated**: 4-6 weeks for full coverage
