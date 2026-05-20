# K.4: طبقة الوزن الظاهر والعميق

# K.4: Surface vs Deep Template Layer Coverage Matrix

**Layer**: K.4
**Domain**: Template (D4)
**Status**: ❌ Not Implemented (WaznCandidate exists but no deep/surface distinction)
**Version**: 1.0.0

---

## المبدأ الأساسي (Core Principle)

```
الوزن الظاهر ≠ الوزن العميق
(Surface Template ≠ Deep Template)
```

**Critical Law**:
```
قال ≠ (ق و ل) مباشرة → يجب تتبع الإعلال
(qala ≠ q-w-l directly → must trace i'lal)

شدّ ≠ (ش د) فقط → يجب تتبع التضعيف
(shadda ≠ sh-d only → must trace doubling)

رمى ≠ (ر م ى) → يجب تتبع الأصل (و/ي)
(rama ≠ r-m-y → must trace original waw/ya)
```

---

## Required Concepts (المفاهيم المطلوبة)

### 1. Surface Template (الوزن الظاهر)

What you see on the surface after all phonological transformations.

Examples:
- قال → فَعَلَ (surface)
- قُلْ → فُعْ (surface - shortened)
- يَقُول → يَفْعُل (surface)
- قَائِل → فَاعِل (surface)

### 2. Deep Template (الوزن العميق)

The underlying form before phonological rules (i'lal, idgham, deletion).

Examples:
- قال ← قَوَلَ (deep: q-w-l before waw→alif)
- قُلْ ← قُوْلْ (deep: before waw deletion)
- يَقُول ← يَقْوُل (deep: before vowel shift)
- قَائِل ← قَاوِل (deep: waw→hamza transformation)

### 3. Transformation Trace (أثر التحول)

The sequence of phonological rules applied from deep to surface.

```
Deep Form → [Rule 1] → [Rule 2] → ... → Surface Form
```

Example:
```
قَوَلَ (deep)
  → [I'lal: waw in open syllable with fatha]
  → [Transformation: waw → alif]
  → قَالَ (surface)
```

### 4. Template Types (أنواع الأوزان)

#### Verb Templates
- ⚠️ فَعَلَ، فَعِلَ، فَعُلَ (Form I - 6 babs)
- ⚠️ فَعَّلَ (Form II - intensive)
- ⚠️ فَاعَلَ (Form III - participation)
- ⚠️ أَفْعَلَ (Form IV - causative)
- ⚠️ تَفَعَّلَ (Form V)
- ⚠️ تَفَاعَلَ (Form VI)
- ⚠️ انْفَعَلَ (Form VII)
- ⚠️ افْتَعَلَ (Form VIII)
- ⚠️ افْعَلَّ (Form IX - colors/defects)
- ⚠️ اسْتَفْعَلَ (Form X)

#### Noun Templates (اسم)
- ⚠️ فَاعِل (active participle)
- ⚠️ مَفْعُول (passive participle)
- ⚠️ فَعِيل (intensive adjective)
- ⚠️ فَعَّال (intensive agent)
- ⚠️ مِفْعَال، مِفْعَل (instrument noun)
- ⚠️ فِعَال (abstract noun)

#### Masdar Templates (مصدر)
- ⚠️ فَعْل، فَعَل، فُعُول، فِعَال (various forms)
- ⚠️ تَفْعِيل (Form II masdar)
- ⚠️ مُفَاعَلَة (Form III masdar)
- ⚠️ إِفْعَال (Form IV masdar)

### 5. Transformation Rules (قواعد التحول)

Covered in K.2 (Phonology), but traced here:

- ⚠️ I'lal rules (قلب، حذف، نقل)
- ⚠️ Idgham rules (assimilation)
- ⚠️ Deletion rules (حذف)
- ⚠️ Epenthesis rules (زيادة)
- ⚠️ Metathesis rules (قلب مكاني)

---

## Allowed Claims (الادعاءات المسموحة)

After full implementation:

- ⚠️ `WaznCandidate` (✅ exists but needs enhancement)
- ❌ `DeepTemplateCandidate` - Underlying template
- ❌ `SurfaceTemplateCandidate` - Surface template
- ❌ `TransformationTrace` - Step-by-step derivation
- ❌ `IlalApplicationTrace` - I'lal rule sequence
- ❌ `TemplateMatchCandidate` - Pattern matching result
- ❌ `VerbFormCandidate` - Form I-X classification
- ❌ `VerbBabCandidate` - Bab classification (Form I)

---

## Forbidden Claims (الادعاءات الممنوعة)

- ❌ `TemplateCertificate` without transformation trace
- ❌ Surface template without deep template derivation
- ❌ Pattern matching without i'lal awareness
- ❌ Direct surface→root mapping (must trace transformations)
- ❌ Claiming pattern without checking weak letter effects

---

## Requires Lexicon? (تحتاج معجم؟)

**Yes** for:
- Irregular verb forms (أفعال شاذة)
- Irregular masdars (مصادر سماعية)
- Anomalous patterns (أوزان شاذة)
- Frozen patterns (جامد without derivational template)

**No** for:
- Standard verb forms I-X
- Regular derived nouns (فاعل، مفعول)
- Predictable transformations

---

## Requires Context? (تحتاج سياق؟)

**No** for single word (مفرد):
- Template identification
- Deep/surface mapping
- Transformation trace

**Yes** (if extended to composition):
- Contextual i'lal (across word boundaries)

---

## Failure Types (أنواع الفشل)

### Residuals

- `DEEP_TEMPLATE_UNRESOLVED` - Cannot determine underlying form
- `TRANSFORMATION_RULE_MISSING` - Cannot trace surface←deep
- `ILAL_TRACE_INCOMPLETE` - I'lal steps unclear
- `TEMPLATE_MATCH_AMBIGUITY` - Multiple template candidates
- `VERB_FORM_UNRESOLVED` - Cannot determine Form I-X
- `VERB_BAB_UNRESOLVED` - Cannot determine bab (Form I only)
- `WEAK_LETTER_ORIGINAL_UNKNOWN` - Cannot determine original و/ي
- `TEMPLATE_PATTERN_CONFLICT` - Surface contradicts expected pattern

### Error Conditions

```python
# Example: Cannot trace i'lal
if has_weak_letters and not has_ilal_trace:
    residual = Residual(
        type="ILAL_TRACE_INCOMPLETE",
        domain=DalDomain.TEMPLATE,
        evidence=("Weak letters present but no i'lal trace",),
        blocker=True,  # Cannot certify pattern
    )
```

---

## Golden Tests (الاختبارات الذهبية)

### Test Set 1: I'lal Transformations (قال، باع، رمى)

| Surface | Deep | Root | I'lal Rule | Trace |
|---------|------|------|------------|-------|
| قَالَ | قَوَلَ | ق و ل | قلب: و→ا (open syllable + fatha) | Deep: q-w-l → Surface: q-a-l |
| بَاعَ | بَيَعَ | ب ي ع | قلب: ي→ا (open syllable + fatha) | Deep: b-y-' → Surface: b-a-' |
| رَمَى | رَمَيَ | ر م ي | قلب: ي→ى (final position) | Deep: r-m-y → Surface: r-m-a |
| قَالَ | قَوَلَ | ق و ل | Same as above | فَعَلَ deep → فَالَ surface |

### Test Set 2: Deletion (قُلْ، بِعْ، ارْمِ)

| Surface | Deep | Root | Deletion Rule | Trace |
|---------|------|------|---------------|-------|
| قُلْ | قُوْلْ | ق و ل | حذف: و in jussive/imperative | Deep: q-u-w-l → Surface: q-u-l |
| بِعْ | بِيْعْ | ب ي ع | حذف: ي in imperative | Deep: b-i-y-' → Surface: b-i-' |
| ارْمِ | ارْمِيْ | ر م ي | حذف: ي final in imperative | Deep: r-m-y → Surface: r-m |

### Test Set 3: Preservation (يَقُولُ، يَبِيعُ، يَرْمِي)

| Surface | Deep | Root | Preservation | Trace |
|---------|------|------|--------------|-------|
| يَقُولُ | يَقْوُلُ | ق و ل | و preserved (not in i'lal context) | Deep: y-q-w-u-l → Surface: y-q-u-u-l |
| يَبِيعُ | يَبْيِعُ | ب ي ع | ي preserved | Deep: y-b-y-i-' → Surface: y-b-i-i-' |
| يَرْمِي | يَرْمِيُ | ر م ي | ي preserved (final long) | Deep: y-r-m-y → Surface: y-r-m-i |

### Test Set 4: Verb Forms (Forms I-X)

| Surface | Form | Deep Template | Surface Template | Augmentation |
|---------|------|---------------|------------------|--------------|
| ضَرَبَ | I | فَعَلَ | فَعَلَ | None |
| كَسَّرَ | II | فَعَّلَ | فَعَّلَ | Shadda |
| قَاتَلَ | III | فَاعَلَ | فَاعَلَ | ا (alif) |
| أَخْرَجَ | IV | أَفْعَلَ | أَفْعَلَ | أ (hamza) |
| تَكَلَّمَ | V | تَفَعَّلَ | تَفَعَّلَ | ت + shadda |
| تَقَاتَلَ | VI | تَفَاعَلَ | تَفَاعَلَ | ت + ا |
| انْكَسَرَ | VII | انْفَعَلَ | انْفَعَلَ | ا + ن |
| اجْتَمَعَ | VIII | افْتَعَلَ | افْتَعَلَ | ا + ت |
| احْمَرَّ | IX | افْعَلَّ | افْعَلَّ | ا + shadda final |
| اسْتَخْرَجَ | X | اسْتَفْعَلَ | اسْتَفْعَلَ | ا + س + ت |

### Test Set 5: Derived Nouns

| Surface | Root | Deep Template | Surface Template | Type |
|---------|------|---------------|------------------|------|
| كَاتِب | ك ت ب | فَاعِل | فَاعِل | اسم فاعل |
| مَكْتُوب | ك ت ب | مَفْعُول | مَفْعُول | اسم مفعول |
| قَائِل | ق و ل | قَاوِل | قَائِل (و→ء) | اسم فاعل + i'lal |
| مَقُول | ق و ل | مَقْوُول | مَقُول (deletion) | اسم مفعول + i'lal |

### Test Set 6: Masdars

| Surface | Root | Form | Deep Template | Surface Template | I'lal |
|---------|------|------|---------------|------------------|-------|
| ضَرْب | ض ر ب | I | فَعْل | فَعْل | None |
| قَوْل | ق و ل | I | قَوْل | قَوْل | None (masdar preserves waw) |
| بَيْع | ب ي ع | I | بَيْع | بَيْع | Preserved |
| تَكْسِير | ك س ر | II | تَفْعِيل | تَفْعِيل | None |
| قِتَال | ق ت ل | III | فِعَال | فِعَال | None |

---

## Current Status (الحالة الحالية)

### ✅ Implemented

- `WaznCandidate` in MufradProof (basic pattern storage)

### ⚠️ Partial

- Pattern matching (simple heuristics)
- Basic template names (فاعل، مفعول...)

### ❌ Missing

- `DeepTemplateCandidate` contract
- `SurfaceTemplateCandidate` contract
- `TransformationTrace` contract
- `IlalApplicationTrace` contract
- Deep→surface derivation engine
- Comprehensive verb forms I-X catalog
- Verb bab classification (Form I: 6 babs)
- I'lal-aware pattern matching
- Weak letter original form detection
- Template transformation rules

---

## Evidence Artifacts (أثر الدليل)

### Required Files

```
src/dal_core/
├── morph_features.py (✅ has WaznCandidate - needs extension)
├── deep_template.py (❌ needed)
├── surface_template.py (❌ needed)
├── transformation_trace.py (❌ needed)
├── ilal_trace.py (❌ needed)
├── verb_forms.py (❌ needed - Forms I-X)
├── verb_babs.py (❌ needed - 6 babs for Form I)
├── template_matcher.py (❌ needed - i'lal-aware)
└── weak_letter_resolver.py (❌ needed)

tests/dal_core/
├── test_deep_template.py (❌ needed: 20 tests)
├── test_transformation_trace.py (❌ needed: 25 tests)
├── test_ilal_trace.py (❌ needed: 30 tests)
├── test_verb_forms.py (❌ needed: 20 tests - Forms I-X)
├── test_verb_babs.py (❌ needed: 12 tests - 6 babs)
├── test_template_matcher.py (❌ needed: 25 tests)
└── test_weak_letter_resolver.py (❌ needed: 18 tests)

data/templates/
├── verb_forms_I_to_X.json (❌ needed)
├── verb_babs_form_I.json (❌ needed)
├── noun_templates.json (❌ needed)
├── masdar_templates.json (❌ needed)
└── ilal_transformation_rules.json (❌ needed)
```

### Test Coverage Requirements

- **Deep Template**: 20+ tests
- **Transformation Trace**: 25+ tests
- **I'lal Trace**: 30+ tests (critical)
- **Verb Forms I-X**: 20+ tests
- **Verb Babs**: 12+ tests
- **Template Matching**: 25+ tests
- **Weak Letter Resolver**: 18+ tests

**Total**: 150+ tests minimum

---

## Gap Analysis (تحليل الفجوات)

### Critical Gaps

1. **No Deep/Surface Distinction**
   - Impact: Cannot properly analyze weak verbs
   - Blocks: Root extraction accuracy, verb health classification (K.5)
   - Priority: **Critical** (foundation for all template analysis)

2. **No I'lal Trace**
   - Impact: Cannot connect surface forms to roots
   - Blocks: Pattern matching, derivation analysis
   - Priority: **Critical**

3. **No Verb Forms Catalog**
   - Impact: Cannot classify Forms I-X
   - Blocks: Verb analysis, masdar prediction
   - Priority: High

4. **No Verb Bab Classification**
   - Impact: Cannot distinguish 6 babs of Form I
   - Blocks: Complete verb analysis
   - Priority: High

### This Layer is a **Critical Blocker**

Without K.4:
- ❌ Cannot properly analyze weak verbs (قال، باع، رمى)
- ❌ Cannot connect roots to surface forms
- ❌ Cannot distinguish verb forms I-X
- ❌ K.5 (Verb Health) cannot function
- ❌ K.6 (Word Type) derivation analysis incomplete

### Implementation Priority

1. **Phase 1** (PR #30 - High Priority): Deep/Surface + I'lal trace
2. **Phase 2** (PR #31): Verb Forms I-X catalog
3. **Phase 3** (PR #32): Verb babs + template matcher

**Estimated**: 6-8 weeks (this is the hardest layer)

---

## Cross-References

- `morph_features.py:WaznCandidate` - Current basic template
- `D4: TEMPLATE` - Domain in dal_algebra
- `K.2-PHONOLOGY-COVERAGE-MATRIX.md` - I'lal rules defined there
- `K.3-ORIGIN-SEGMENTATION-MATRIX.md` - Root extraction needs this
- `K.5-VERB-HEALTH-MATRIX.md` - **Depends entirely on K.4**
- `K.6-WORD-TYPE-TAXONOMY-MATRIX.md` - Derivation classification needs this

---

**Status**: ❌ Not Implemented (0% - only basic WaznCandidate exists)
**Next**: Implement DeepTemplateCandidate + TransformationTrace
**Priority**: **Critical** - Blocks K.5 and K.6
**Estimated**: 6-8 weeks for full coverage
