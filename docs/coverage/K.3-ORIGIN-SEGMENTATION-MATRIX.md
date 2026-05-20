# K.3: طبقة الأصل والزيادة واللواصق

# K.3: Origin-Augmentation-Clitics Layer Coverage Matrix

**Layer**: K.3
**Domain**: Origin (D3) + Pre-Morph (D2)
**Status**: 🚧 Partial (RootCandidate + SegmentationProof exist, augmentation rules missing)
**Version**: 1.0.0

---

## القوانين الحاكمة (Governing Laws)

```
لا زيادة بلا موضع محدد.
(No augmentation without specified position)

لا لاصق بلا حد خارجي واضح.
(No clitic without clear external boundary)

لا أصل بلا دليل (قياس أو سماع).
(No root without evidence - qiyas or sama')
```

---

## Required Concepts (المفاهيم المطلوبة)

### 1. Root Types (أنواع الجذور)

#### By Length
- ✅ ثلاثي (Trilateral: ك ت ب)
- ⚠️ رباعي (Quadrilateral: د ح ر ج)
- ⚠️ خماسي (Quinqueliteral: rare)

#### By Health (will be covered in K.5)
- صحيح سالم (Sound/healthy)
- مهموز (With hamza)
- معتل (Weak - contains weak letters)
- مضعف (Doubled)

### 2. Augmentation Letters (حروف الزيادة)

**Mnemonic**: سألتمونيها (sa'altumuniha)

- ⚠️ س (sin) - استفعل (Form X)
- ⚠️ أ (hamza) - أفعل (Form IV)
- ⚠️ ل (lam) - انفعل (rare)
- ⚠️ ت (ta') - افتعل, تفعّل, تفاعل
- ⚠️ م (mim) - مفعول, مفاعل
- ⚠️ و (waw) - استفعل, patterns with waw
- ⚠️ ن (nun) - انفعل, فعلان
- ⚠️ ي (ya') - فعيل, أفعال
- ⚠️ ه (ha') - rare augmentation
- ⚠️ ا (alif) - فاعل, مفاعل

### 3. Internal Augmentation (الزيادة الداخلية)

By position:
- ⚠️ زيادة أول (Initial: أفعل)
- ⚠️ زيادة وسط (Medial: فاعل)
- ⚠️ زيادة آخر (Final: فعلان)
- ⚠️ زيادة متعددة (Multiple: استفعل)

### 4. External Clitics (اللواصق الخارجية)

#### Prefixes (السوابق)
- ✅ ال (definite article)
- ✅ و، ف، ب، ك، ل (conjunction, prepositions)
- ⚠️ ها (vocative - rare prefix)

#### Suffixes (اللواحق)
- ✅ Pronouns: ه، ها، هم، هن، ك، كم، كن، ي، نا
- ✅ Dual: ان، ين
- ✅ Plural masculine: ون، ين
- ✅ Plural feminine: ات
- ⚠️ Nisba: ي + ة (النسبة)

### 5. Functional Particles (حروف المعنى)

- ✅ حروف الجر (Prepositions): من، إلى، على، في، عن، ب، ل، ك
- ✅ حروف العطف (Conjunctions): و، ف، ثم، أو، أم، لكن، بل
- ⚠️ حروف النفي (Negation): ما، لا، لم، لن، لات
- ⚠️ حروف الاستفهام (Interrogative): هل، أ
- ⚠️ حروف النداء (Vocative): يا، أيا، هيا، أي

### 6. Segmentation (التقسيم)

- ✅ Stem extraction (استخراج الجذع)
- ✅ Prefix identification (تحديد السوابق)
- ✅ Suffix identification (تحديد اللواحق)
- ⚠️ Boundary disambiguation (حل الالتباس في الحدود)
- ⚠️ Nested clitics (لواصق متداخلة: والكتاب)

---

## Allowed Claims (الادعاءات المسموحة)

After full implementation:

- ✅ `RootCandidate` - Root extraction candidate (exists in MufradProof)
- ✅ `SegmentationProof` - Stem + clitics (exists in MufradProof)
- ✅ `CliticProof` - Individual clitic (exists in MufradProof)
- ⚠️ `AugmentationCandidate` - Internal augmentation letter
- ⚠️ `AugmentationPositionCandidate` - Position of augmentation
- ⚠️ `StemBoundaryCandidate` - Stem boundaries
- ⚠️ `RootTypeCandidate` - Trilateral/quadrilateral classification
- ⚠️ `FunctionalParticleCandidate` - Particle classification

---

## Forbidden Claims (الادعاءات الممنوعة)

- ❌ `RootCertificate` without lexicon or attestation
- ❌ Augmentation without position evidence
- ❌ Clitic without boundary evidence
- ❌ Root without trace to surface form
- ❌ Direct promotion: ORIGIN → TEMPLATE (requires transition)
- ❌ Stem extraction without segmentation evidence

---

## Requires Lexicon? (تحتاج معجم؟)

**Yes** for:
- Irregular roots (شواذ)
- Frozen forms (جوامد) without extractable root
- Proper names (أعلام)
- Loanwords (دخيل)
- Rare quadrilateral/quinqueliteral roots
- Particle meanings and usage

**No** for:
- Standard trilateral roots
- Regular verb forms
- Regular derived forms (اسم فاعل، مفعول)
- Common clitics (ال، و، ف، ب، ل)

---

## Requires Context? (تحتاج سياق؟)

**No** for single word analysis (مفرد):
- Root extraction
- Clitic segmentation
- Augmentation identification

**Yes** for composition (if extended):
- Clitic disambiguation across words
- Particle scope determination

---

## Failure Types (أنواع الفشل)

### Residuals

- `ROOT_EXTRACTION_AMBIGUITY` - Multiple possible roots
- `AUGMENTATION_POSITION_UNRESOLVED` - Cannot determine augmentation position
- `CLITIC_BOUNDARY_AMBIGUITY` - Unclear clitic boundaries
- `STEM_EXTRACTION_FAILURE` - Cannot isolate stem
- `ROOT_TYPE_UNRESOLVED` - Unclear if trilateral/quadrilateral
- `FROZEN_FORM_NO_ROOT` - Frozen word without extractable root
- `PARTICLE_CLASSIFICATION_AMBIGUITY` - Unclear particle type
- `SEGMENTATION_COMPETING_ANALYSES` - Multiple valid segmentations

### Error Conditions

```python
# Example: Multiple root candidates
if len(root_candidates) > 1 and not has_lexicon_attestation:
    residual = Residual(
        type="ROOT_EXTRACTION_AMBIGUITY",
        domain=DalDomain.ORIGIN,
        evidence=(f"{len(root_candidates)} root candidates without attestation",),
        blocker=False,  # Can proceed with candidates
    )
```

---

## Golden Tests (الاختبارات الذهبية)

### Test Set 1: Trilateral Roots

| Surface | Root | Augmentation | Evidence |
|---------|------|--------------|----------|
| كَتَبَ | ك ت ب | None | Base form |
| كَاتِب | ك ت ب | ا (alif) | فاعل pattern |
| مَكْتُوب | ك ت ب | م، و (mim, waw) | مفعول pattern |
| كِتَاب | ك ت ب | ا (alif) | فِعَال pattern |
| كُتُب | ك ت ب | None | Plural pattern |
| تَكَاتُب | ك ت ب | ت، ا (ta', alif) | تفاعل pattern |

### Test Set 2: Augmentation Position

| Surface | Root | Augmentation Letters | Positions | Pattern |
|---------|------|---------------------|-----------|---------|
| أَخْرَجَ | خ ر ج | أ | Initial | أفعل (Form IV) |
| اِسْتَخْرَجَ | خ ر ج | ا، س، ت | Initial × 3 | استفعل (Form X) |
| تَكَلَّمَ | ك ل م | ت، شدة | Initial, medial | تفعّل (Form V) |
| اِنْكَسَرَ | ك س ر | ا، ن | Initial × 2 | انفعل (Form VII) |

### Test Set 3: Clitics - Prefixes

| Surface | Stem | Prefixes | Analysis |
|---------|------|----------|----------|
| الكِتَاب | كِتَاب | ال | Definite article |
| وَالكِتَاب | كِتَاب | و، ال | Conjunction + article |
| بِالكِتَاب | كِتَاب | ب، ال | Preposition + article |
| فَلِلْكِتَاب | كِتَاب | ف، ل، ال | Conj + prep + article |
| كَالكِتَاب | كِتَاب | ك، ال | Comparison + article |

### Test Set 4: Clitics - Suffixes

| Surface | Stem | Suffixes | Analysis |
|---------|------|----------|----------|
| كِتَابُهُ | كِتَاب | ه | Possessive pronoun (his) |
| كِتَابُهُمْ | كِتَاب | هم | Possessive pronoun (their) |
| كِتَابَانِ | كِتَاب | ان | Dual nominative |
| كِتَابَيْنِ | كِتَاب | ين | Dual genitive/accusative |
| كِتَابُونَ | كِتَاب | ون | Plural masculine nominative |
| كِتَابَاتٌ | كِتَاب | ات | Plural feminine |

### Test Set 5: Complex Segmentation

| Surface | Segmentation | Analysis |
|---------|--------------|----------|
| وَالكِتَابُ | و + ال + كِتَاب + ُ | Conj + article + stem + damma |
| فَبِكِتَابِهِمْ | ف + ب + كِتَاب + هم | Conj + prep + stem + pronoun |
| أَسْتَخْرِجُهَا | ا + س + ت + خ ر ج + ها | Prefix + root + augmentation + pronoun |

### Test Set 6: Functional Particles

| Surface | Type | Function | Evidence |
|---------|------|----------|----------|
| مِنْ | حرف جر | Preposition | From |
| إِلَى | حرف جر | Preposition | To |
| فِي | حرف جر | Preposition | In |
| وَ | حرف عطف | Conjunction | And |
| فَ | حرف عطف | Conjunction | Then/so |
| هَلْ | حرف استفهام | Interrogative | Question marker |
| مَا | حرف نفي | Negation | Not |

### Test Set 7: Frozen Forms (No Root)

| Surface | Classification | Root Extractable? | Evidence |
|---------|----------------|-------------------|----------|
| هَذَا | جامد وظيفي | ❌ No | Demonstrative |
| الذِي | جامد وظيفي | ❌ No | Relative pronoun |
| أَنَا | جامد وظيفي | ❌ No | Personal pronoun |
| الآنَ | ظرف مبني | ❌ No | Time adverb |
| حَيْثُ | ظرف مبني | ❌ No | Place adverb |

---

## Current Status (الحالة الحالية)

### ✅ Implemented

- `RootCandidate` in MufradProof
- `SegmentationProof` in MufradProof
- `CliticProof` in MufradProof
- Basic root extraction (simple cases)
- Basic clitic segmentation (ال، pronouns)

### 🚧 Partial

- Augmentation letter identification (heuristics exist)
- Prefix/suffix boundary detection (common cases)

### ❌ Missing

- `AugmentationCandidate` contract
- `AugmentationPositionCandidate` contract
- Comprehensive augmentation rules (all forms I-X+)
- Nested clitic handling
- Particle classification contract
- Boundary disambiguation for ambiguous cases
- Frozen form detection
- Quadrilateral/quinqueliteral root handling

---

## Evidence Artifacts (أثر الدليل)

### Required Files

```
src/dal_core/
├── morph_features.py (✅ exists - has RootCandidate)
├── mufrad_proof.py (✅ exists - has SegmentationProof, CliticProof)
├── augmentation_analyzer.py (❌ needed)
├── augmentation_rules.py (❌ needed)
├── clitic_boundary.py (⚠️ basic exists)
├── particle_classifier.py (❌ needed)
├── frozen_form_detector.py (❌ needed)
└── root_extractor.py (⚠️ basic exists)

tests/dal_core/
├── test_mufrad_proof.py (✅ exists)
├── test_augmentation_analyzer.py (❌ needed: 25 tests)
├── test_clitic_segmentation.py (❌ needed: 20 tests)
├── test_particle_classifier.py (❌ needed: 15 tests)
├── test_frozen_forms.py (❌ needed: 10 tests)
└── test_complex_segmentation.py (❌ needed: 18 tests)

data/morphology/
├── augmentation_patterns.json (❌ needed)
├── verb_forms_I_to_X.json (❌ needed)
├── particle_catalog.json (❌ needed)
└── frozen_forms_catalog.json (❌ needed)
```

### Test Coverage Requirements

- **Root Extraction**: 20+ tests (trilateral, quadrilateral)
- **Augmentation**: 25+ tests (all forms I-X)
- **Clitics**: 20+ tests (prefixes, suffixes, nested)
- **Particles**: 15+ tests (جر، عطف، نفي، استفهام)
- **Frozen Forms**: 10+ tests
- **Complex Segmentation**: 18+ tests
- **Boundary Disambiguation**: 10+ tests

**Total**: 118+ tests minimum

---

## Gap Analysis (تحليل الفجوات)

### Critical Gaps

1. **No Augmentation Position Analyzer**
   - Impact: Cannot trace derived forms to roots
   - Blocks: Template analysis (K.4), derivation classification (K.6)
   - Priority: Critical

2. **No Comprehensive Verb Forms Catalog**
   - Impact: Cannot classify Forms I-X properly
   - Blocks: Verb pattern matching
   - Priority: High

3. **No Particle Classification Contract**
   - Impact: Cannot distinguish particle types
   - Blocks: Syntax analysis, operator detection
   - Priority: High

4. **No Frozen Form Detector**
   - Impact: Attempts root extraction on frozen words
   - Blocks: Proper handling of pronouns, demonstratives
   - Priority: Medium

### Blocker for Other Layers

This layer **blocks**:
- **K.4**: Template matching (needs augmentation trace)
- **K.6**: Word type classification (needs derivation analysis)
- **K.7**: Jamid/mushtaq judgment (needs derivation status)

### Implementation Priority

1. **Phase 1** (PR #30): Augmentation analyzer + Forms I-X
2. **Phase 2** (PR #31): Particle classifier + frozen forms
3. **Phase 3** (PR #32): Complex segmentation + boundary disambiguation

---

## Cross-References

- `morph_features.py` - RootCandidate definition
- `mufrad_proof.py` - SegmentationProof, CliticProof
- `D3: ORIGIN` - Domain in dal_algebra
- `D2: PRE_MORPH` - Segmentation domain
- `K.4-TEMPLATE-TRANSFORMATION-MATRIX.md` - Needs augmentation trace
- `K.6-WORD-TYPE-TAXONOMY-MATRIX.md` - Needs derivation classification
- `K.7-SURFACE-FORCES-VERIFICATION.md` - Jamid/mushtaq depends on root

---

**Status**: 🚧 Partial (50% complete)
**Next**: Implement AugmentationCandidate + Forms I-X catalog
**Estimated**: 4-5 weeks for full coverage
