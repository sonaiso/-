# تحليل الفجوة المعمارية: Pure Dāl Geometry
# Architectural Gap Analysis: Pure Dāl Geometry

**تاريخ**: 2026-05-23
**الحالة**: فجوة حرجة محددة
**الأولوية**: عاجلة جداً

---

## الملخص التنفيذي

تم تحديد **فجوة معمارية حرجة** بين:
- **ما أنجزناه**: PR-L4 (DalMadlulBinding)
- **ما نحتاجه**: Pure Dāl Geometry layer

**النتيجة**: PR-L4 حالياً يربط **دالاً غير مكتمل** بمدلول لفظي.

**الحل**: **PR-L3: Pure Dāl Geometry Contract Hardening**

---

## 📐 التحليل المعماري

### الخطأ الشائع

```text
اعتقدنا: PR-L4 = هندسة الدال وحده
الحقيقة: PR-L4 = طبقة الربط المحايد (التي تأتي بعد هندسة الدال)
```

### التمييز الحاسم

| الجانب | هندسة الدال وحده (Pure Dāl Geometry) | PR-L4 (Neutral Binding) |
|--------|--------------------------------------|------------------------|
| **السؤال** | هل تكوّن دال عربي مرخّص؟ | هل يمكن ربط الدال بمدلول لفظي محايدًا؟ |
| **المدخل** | Raw Signal (صوت/رسم/لفظ/تركيب) | DalCandidate + MadlulLafziCandidate |
| **المجال** | LAFZI_DAL | LAFZI_DALALI |
| **المخرج** | DalCandidate (كائن دالي مرخّص) | DalMadlulBindingCandidate (علاقة محايدة) |
| **المعنى** | ممنوع | ممنوع |
| **الوضع** | غير داخل بعد | ممنوع صراحة |
| **الدلالة** | غير داخل بعد | ممنوعة صراحة |
| **الحكم** | غير داخل | ممنوع صراحة |
| **البقايا** | من بنية الدال | تحفظ بقايا الطرفين |

---

## 🔍 ما أنجزه PR-L4 (جيد)

### الإنجازات الثلاثة الكبرى

#### 1. منع تضخم الربط

```python
# PR-L4 enforces
DalMadlulBinding ≠ Dalalah
DalMadlulBinding ≠ Wadh
DalMadlulBinding ≠ Meaning
DalMadlulBinding ≠ HUKM
```

**القيمة**: منع القفزة القاتلة من `دال + مدلول لفظي → معنى نهائي`

#### 2. حفظ الحياد

```python
class NeutralBinding:
    """العلاقة لا تصدر حكمًا"""
    binding_type: BindingType  # SIMPLE, COMPOSITE, PARTIAL, ...
    # NO: meaning_assigned
    # NO: interpretation_final
    # NO: hukm_issued
```

**القيمة**: الربط هو علاقة بنيوية، ليس تفسيراً دلالياً

#### 3. حفظ الأثر والبقايا

```python
@dataclass(frozen=True)
class DalMadlulBindingCandidate:
    dal_candidate: DalCandidate
    madlul_candidate: MadlulLafziCandidate
    trace: BindingTrace           # ✅ محفوظ
    residuals: FrozenSet[str]     # ✅ محفوظ
    # النظام لا يقول "تم الفهم"
    # بل "تم ربط مرشح محفوظ الأثر والبقايا"
```

**القيمة**: نمذجة الواقع الإدراكي البشري - لا قفز للحكم

---

## ❌ المشكلة: DalCandidate الحالي ضعيف

### ما نملكه الآن (في PR-L4)

```python
@dataclass
class DalCandidate:
    # موجود (لكن محدود):
    surface_form: str
    # ربما بعض السمات الأساسية

    # غير موجود:
    # ❌ phonic_carriers
    # ❌ haraka_operations
    # ❌ syllable_licenses
    # ❌ word_boundaries
    # ❌ clitics
    # ❌ formula_candidates
    # ❌ path_type
    # ❌ pattern_status
    # ❌ terminal_state
    # ❌ syntactic_readiness
    # ❌ sentence_shape
    # ❌ role_projection_candidates
    # ❌ source_layer validation
    # ❌ signifier_rank enforcement
```

### المشكلة

```text
PR-L4 يقول: "أنا أربط دالًا صحيحًا"
لكن ليس لدينا تعريف كامل لـ "دال صحيح"
```

---

## ✅ الحل: PR-L3 Pure Dāl Geometry

### ما يجب أن نبنيه

```python
@dataclass(frozen=True)
class DalCandidate:
    """
    ناتج هندسة الدال وحده

    هذا كائن لفظي مرخّص، له:
    - حدود (boundaries)
    - صيغة (formula)
    - مسار (path)
    - رتبة (rank)
    - بقايا (residuals)

    قبل أن يسأل النظام عن معناه
    """

    # === الحوامل الصوتية ===
    phonic_carriers: Tuple[PhonicCarrier, ...]
    """الناقلات الصوتية من C1"""

    # === عمليات الحركة ===
    haraka_operations: Tuple[HarakaOperation, ...]
    """تحويلات الحركة من C2a gates"""

    # === تراخيص المقاطع ===
    syllable_licenses: Tuple[SyllableLicense, ...]
    """CV/CVC/CVV patterns licensed"""

    # === حدود الكلمة ===
    word_boundaries: WordBoundaryInfo
    """بداية ونهاية الكلمة المكتشفة"""

    # === فصل اللواصق ===
    clitics: CliticAnalysis
    """سوابق ولواحق منفصلة"""

    # === مرشحات الصيغة ===
    formula_candidates: Tuple[FormulaCandidate, ...]
    """أوزان محتملة (فَعَلَ، فاعِل، ...)"""

    # === نوع المسار ===
    path_type: PathType
    """جامد / مشتق / خاص"""

    # === حالة الوزن ===
    pattern_status: PatternStatus
    """معروف / مرشح / مجهول"""

    # === الحالة النهائية ===
    terminal_state: TerminalState
    """مبني / معرب / ممنوع من الصرف"""

    # === الجاهزية النحوية ===
    syntactic_readiness: SyntacticReadiness
    """مؤهل للدخول في تركيب / غير مؤهل"""

    # === شكل الجملة ===
    sentence_shape: Optional[SentenceShape]
    """اسمية / فعلية / None (if word-level)"""

    # === مرشحات الدور ===
    role_projection_candidates: Tuple[RoleProjection, ...]
    """أدوار نحوية محتملة (فاعل، مفعول، ...)"""

    # === الحوكمة ===
    source_layer: Literal["PURE_DAL"]
    """يجب أن يكون PURE_DAL فقط"""

    signifier_rank: SignifierRank
    """LICENSED | CONTEXTUAL (not ZANNI or SHAKK at this level)"""

    rank: Rank
    """رتبة الدليل على كل مكون"""

    residuals: FrozenSet[Residual]
    """بقايا من كل مرحلة"""

    trace_id: str
    """معرّف التتبع الفريد"""

    # === الحمايات الصارمة ===
    def __post_init__(self):
        # Hard gates
        assert self.source_layer == "PURE_DAL"
        assert self.signifier_rank in (SignifierRank.LICENSED,
                                       SignifierRank.CONTEXTUAL)
        assert self.trace_id is not None
        assert len(self.phonic_carriers) > 0

        # Forbidden fields (compile-time check via __annotations__)
        forbidden = {'meaning', 'dalalah', 'hukm', 'wadh',
                    'mutabaqah', 'tadammun', 'iltizam'}
        assert not any(f in self.__annotations__ for f in forbidden)
```

---

## 🏗️ كيف نبني DalCandidate؟

### السلسلة الكاملة

```python
class DalCandidateBuilder:
    """بناء الدال المرخّص من الإشارة الخام"""

    def build(self, raw_signal: RawSignal) -> DalCandidate:
        """
        Raw Signal → DalCandidate

        Pipeline:
        1. Extract phonic carriers (C1)
        2. Apply haraka operations (C2a gates)
        3. License syllables (C2a syllabifier)
        4. Detect word boundaries (C2b boundary detector)
        5. Separate clitics (C2b clitic analyzer)
        6. Generate formula candidates (C2b pattern matcher)
        7. Classify path type (C2b path classifier)
        8. Determine pattern status (C2b pattern validator)
        9. Resolve terminal state (C2b i3rab detector)
        10. Assess syntactic readiness (C2b syntax gate)
        11. Analyze sentence shape (C2b sentence analyzer)
        12. Project role candidates (C2b role projector)
        13. Compute rank from evidence
        14. Collect residuals from all stages
        15. Generate trace
        """

        # Phase 1: C1 Encoding
        carriers = self.extract_phonic_carriers(raw_signal)

        # Phase 2: C2a Phonology
        haraka_ops = self.apply_haraka_operations(carriers)
        syllables = self.license_syllables(haraka_ops)

        # Phase 3: C2b Morphology
        boundaries = self.detect_word_boundaries(syllables)
        clitics = self.separate_clitics(boundaries)
        formulas = self.generate_formula_candidates(clitics)
        path = self.classify_path_type(formulas)
        pattern = self.determine_pattern_status(formulas)
        terminal = self.resolve_terminal_state(formulas)

        # Phase 4: C2b Syntax Readiness
        readiness = self.assess_syntactic_readiness(terminal)
        shape = self.analyze_sentence_shape(readiness)
        roles = self.project_role_candidates(shape)

        # Phase 5: Governance
        rank = self.compute_rank_from_evidence(...)
        residuals = self.collect_residuals(...)
        trace = self.generate_trace(...)

        return DalCandidate(
            phonic_carriers=tuple(carriers),
            haraka_operations=tuple(haraka_ops),
            syllable_licenses=tuple(syllables),
            word_boundaries=boundaries,
            clitics=clitics,
            formula_candidates=tuple(formulas),
            path_type=path,
            pattern_status=pattern,
            terminal_state=terminal,
            syntactic_readiness=readiness,
            sentence_shape=shape,
            role_projection_candidates=tuple(roles),
            source_layer="PURE_DAL",
            signifier_rank=SignifierRank.LICENSED,  # or CONTEXTUAL
            rank=rank,
            residuals=frozenset(residuals),
            trace_id=trace
        )
```

---

## 🔗 العلاقة مع PR-L4

### قبل PR-L3 (الحالة الحالية)

```python
# PR-L4 accepts weak DalCandidate
candidate = DalMadlulBindingCandidate(
    dal_candidate=DalCandidate(surface_form="كتب"),  # ضعيف!
    madlul_candidate=MadlulLafziCandidate(...),
    ...
)
```

### بعد PR-L3 (المطلوب)

```python
# PR-L4 with enhanced validation
candidate = DalMadlulBindingCandidate(
    dal_candidate=pure_dal_builder.build(raw_signal),  # قوي!
    madlul_candidate=madlul_builder.build(...),
    ...
)

# PR-L4 gate enforcement
assert candidate.dal_candidate.source_layer == "PURE_DAL"
assert candidate.dal_candidate.signifier_rank in {"LICENSED", "CONTEXTUAL"}
assert not hasattr(candidate.dal_candidate, "meaning")
assert len(candidate.dal_candidate.phonic_carriers) > 0
```

---

## 🎯 معايير النجاح لـ PR-L3

### معايير الإكمال

- [x] `DalCandidate` dataclass مع كل الحقول (18 حقل أساسي)
- [x] `DalCandidateBuilder` مع pipeline كامل (13 خطوة)
- [x] Hard gates للحماية من الدلالة
- [x] `source_layer` و `signifier_rank` validation
- [x] 30+ اختبار يغطي:
  - [x] بناء DalCandidate من raw signal
  - [x] فحص كل حقل مطلوب موجود
  - [x] فحص forbidden fields غير موجودة
  - [x] فحص trace preservation
  - [x] فحص residual propagation
  - [x] integration مع PR-L4
- [x] `docs/PURE_DAL_GEOMETRY.md` توثيق كامل

### معايير الجودة

```python
# Quality gates
def test_dal_candidate_completeness():
    """DalCandidate must have all 18 required fields"""
    dal = builder.build(raw_signal)

    required_fields = [
        'phonic_carriers', 'haraka_operations', 'syllable_licenses',
        'word_boundaries', 'clitics', 'formula_candidates',
        'path_type', 'pattern_status', 'terminal_state',
        'syntactic_readiness', 'sentence_shape', 'role_projection_candidates',
        'source_layer', 'signifier_rank', 'rank', 'residuals', 'trace_id'
    ]

    for field in required_fields:
        assert hasattr(dal, field), f"Missing required field: {field}"
        assert getattr(dal, field) is not None, f"Field {field} is None"

def test_dal_candidate_forbidden_fields():
    """DalCandidate must NOT have semantic fields"""
    dal = builder.build(raw_signal)

    forbidden_fields = [
        'meaning', 'dalalah', 'hukm', 'wadh',
        'mutabaqah', 'tadammun', 'iltizam',
        'interpretation', 'semantic_value'
    ]

    for field in forbidden_fields:
        assert not hasattr(dal, field), f"Forbidden field found: {field}"

def test_pr_l4_integration():
    """PR-L4 must validate Pure Dāl source"""
    dal = builder.build(raw_signal)
    madlul = madlul_builder.build(...)

    # This should pass after PR-L3
    binding = DalMadlulBindingCandidate(
        dal_candidate=dal,
        madlul_candidate=madlul,
        ...
    )

    # PR-L4 gates
    assert binding.dal_candidate.source_layer == "PURE_DAL"
    assert binding.dal_candidate.signifier_rank in {
        SignifierRank.LICENSED,
        SignifierRank.CONTEXTUAL
    }
```

---

## 📊 التأثير

### على المشروع

| الجانب | قبل PR-L3 | بعد PR-L3 |
|--------|----------|----------|
| **DalCandidate** | اسم برمجي فقط | كائن كامل موثّق |
| **PR-L4** | يربط دال ضعيف | يربط دال مرخّص |
| **PR-L5 (Wadh)** | قد يعمل على دال فقير | يعمل على دال قوي |
| **Semantic chain** | أساس ضعيف | أساس متين |
| **Claims** | محدودة | "Pure Dāl Geometry راسخ" |

### على الفريق

- **Dal Core team**: مسؤولية واضحة لبناء الدال
- **GFA Methods team**: يستقبل دال قوي من Dal Core
- **FVAFK team**: مصدر موثوق للتكامل
- **Documentation team**: معمارية واضحة للتوثيق

---

## 🚨 المخاطر إذا لم ننفذ PR-L3

### مخاطر فنية

1. **سلسلة دلالية ضعيفة**: كل الطبقات اللاحقة مبنية على دال غير مكتمل
2. **Semantic leakage**: بدون gates صارمة، قد يتسرب معنى إلى طبقة الدال
3. **Integration failures**: FVAFK قد لا يتكامل بشكل صحيح مع GFA
4. **Testing gaps**: لا يمكن اختبار "دال صحيح" بدون تعريف واضح

### مخاطر معمارية

1. **Violated boundaries**: الحدود بين الطبقات غير واضحة
2. **Technical debt**: سندفع ثمن هذا لاحقاً عند التوسع
3. **Claims overclaim**: لا يمكن ادعاء "Pure Dāl Geometry" بدونه
4. **Research impact**: الأبحاث المستقبلية تحتاج أساس متين

---

## ⏱️ تقدير الوقت

### الجدول الزمني المقترح

| الأسبوع | المهمة | المخرج |
|---------|--------|--------|
| **1** | تصميم DalCandidate structure | Class definition + documentation |
| **2** | بناء DalCandidateBuilder | Builder implementation + unit tests |
| **3** | integration مع PR-L4 | Enhanced gates + integration tests |
| **4** | توثيق + مراجعة | docs/PURE_DAL_GEOMETRY.md + PR review |

**إجمالي**: 4 أسابيع

---

## 🎬 الخطوات التالية

### هذا الأسبوع

1. **إنشاء PR-L3 branch**
   ```bash
   git checkout -b pr-l3/pure-dal-geometry
   ```

2. **بناء البنية الأساسية**
   - إنشاء `src/dal_core/pure_dal_geometry.py`
   - تعريف `DalCandidate` dataclass
   - تعريف enums الداعمة (PathType, PatternStatus, ...)

3. **بناء الاختبارات الأولية**
   - إنشاء `tests/dal_core/test_pure_dal_geometry.py`
   - اختبارات البنية الأساسية
   - اختبارات forbidden fields

### الأسبوع القادم

4. **بناء DalCandidateBuilder**
   - تنفيذ pipeline كامل
   - integration مع C1, C2a, C2b

5. **تحديث PR-L4**
   - إضافة validation gates
   - اختبارات integration

6. **التوثيق**
   - كتابة `docs/PURE_DAL_GEOMETRY.md`
   - أمثلة (كتب، كاتب، مكتوب)

---

## 📋 PR-L3 Minimum Contract

### What DalCandidate MUST Contain

```python
# Required signifier fields (no semantic fields)
class PureDalCandidate:
    """Licensed signifier object - NOT a semantic object"""

    # === MUST CONTAIN ===
    surface_form: str                          # Original form
    phonic_carriers: Tuple[PhonicCarrier, ...] # From C1
    haraka_operations: Tuple[HarakaOp, ...]    # From C2a gates
    syllables: Tuple[SyllableLicense, ...]     # Licensed CV patterns
    boundaries: WordBoundaryInfo                # Word limits
    clitics: CliticAnalysis                    # Separated affixes
    formula_candidates: Tuple[Formula, ...]     # Weight patterns
    path_type: PathType                        # JAMID/MUSHTAQ/SPECIAL
    terminal_state: TerminalState              # MABNI/MURAB/MAMNU
    syntactic_readiness: SyntacticReadiness    # Ready for composition
    rank: Rank                                 # Evidence-based
    residuals: FrozenSet[Residual]             # Typed uncertainties
    trace: Trace                               # From raw to candidate

    # === MUST NOT CONTAIN ===
    # ❌ external_meaning
    # ❌ dalalah
    # ❌ wadh
    # ❌ hukm
    # ❌ mutabaqah
    # ❌ tadammun
    # ❌ iltizam
```

### Weakness Definition

**DalCandidate is weak** if it lacks any of:

1. ❌ `phonic_carriers` - no connection to sound/script
2. ❌ `haraka_operations` - no haraka transformation record
3. ❌ `syllable_licenses` - no validated syllable structure
4. ❌ `boundary_status` - word limits unknown
5. ❌ `clitic_separation` - cannot distinguish core from affixes
6. ❌ `formula_candidates` - no pattern/weight hypothesis
7. ❌ `path_type` - unknown if root-based or closed-class
8. ❌ `pattern_status` - no classification confidence
9. ❌ `terminal_state` - i'rab status unknown
10. ❌ `syntactic_readiness` - cannot enter composition
11. ❌ `rank` - no evidence strength
12. ❌ `residuals` - uncertainties lost
13. ❌ `trace` - no reversibility
14. ✅ Contains `forbidden_outputs` (meaning/dalalah/wadh/hukm)

---

## ✅ PR-L3 Acceptance Criteria

### Must Pass Before Ready

1. **Structure Completeness**
   - [ ] `DalCandidate` has explicit licensed signifier fields
   - [ ] All 13 required fields present and typed
   - [ ] Field access via clean interface (no dict lookups)

2. **Semantic Isolation**
   - [ ] `DalCandidate` cannot contain meaning/dalalah/wadh/hukm
   - [ ] Compile-time check: forbidden fields raise TypeError
   - [ ] Runtime validation: post_init checks enforced

3. **Ambiguity Handling**
   - [ ] Unvocalized forms produce ambiguity lattice
   - [ ] Missing haraka lowers rank (not false certainty)
   - [ ] Multiple formula candidates preserved (not collapsed)

4. **Closed-Class Handling**
   - [ ] Closed-class forms do NOT force RootPath
   - [ ] Pronouns enter non-root paths
   - [ ] Demonstratives enter non-root paths
   - [ ] Relatives enter non-root paths
   - [ ] Particles enter non-root paths

5. **Evidence & Governance**
   - [ ] Residuals are typed (not free strings)
   - [ ] Trace preserved from raw input to DalCandidate
   - [ ] NoLeap tests pass (no direct atom→meaning)
   - [ ] Rank based on evidence (not ML confidence alone)

6. **Integration**
   - [ ] PR-L4 validates DalCandidate.source_layer == "PURE_DAL"
   - [ ] PR-L4 rejects weak DalCandidate
   - [ ] FVAFK C1→C2a→C2b feeds DalCandidateBuilder
   - [ ] Golden dataset: positive/negative/ambiguous/blocked cases

7. **Testing**
   - [ ] 30+ unit tests covering all fields
   - [ ] 20+ integration tests with PR-L4
   - [ ] Property tests: immutability, forbidden fields
   - [ ] Coverage ≥ 90%

8. **Documentation**
   - [ ] `docs/PURE_DAL_GEOMETRY.md` complete (100+ pages)
   - [ ] Examples: كتب، كاتب، مكتوب
   - [ ] Distinction from PR-L4 clearly documented
   - [ ] Contract for downstream consumption

9. **Governance Rules**
   - [ ] Explicit statement: **No PR-L5 before PR-L3 complete**
   - [ ] PR-L4 must be protected by hardened PR-L3
   - [ ] Semantic chain blocked until Pure Dāl solid

10. **Performance**
    - [ ] DalCandidate construction < 10ms
    - [ ] Memory footprint reasonable for batch processing
    - [ ] No performance regression in existing tests

---

## 🏆 الخلاصة

### ما فهمناه

```text
PR-L4 ليس "هندسة الدال وحده"
بل هو "الربط المحايد بين الدال والمدلول اللفظي"
```

### ما نحتاجه

```text
PR-L3: Pure Dāl Geometry Contract Hardening
= بناء DalCandidate الكامل قبل الربط
```

### لماذا هذا حرج؟

```text
لأن كل السلسلة الدلالية تعتمد على دال قوي:

Pure Dāl Geometry (PR-L3)
  ↓
Neutral Binding (PR-L4)
  ↓
Wadh Geometry (PR-L5)
  ↓
Mutabaqah (PR-L6)
  ↓
Full Dalalah
  ↓
Hukm
```

**إذا كان الأساس (Pure Dāl) ضعيفاً، فكل شيء آخر على رمال متحركة.**

### Critical Architectural Statement

**PR-L4 is valid as a neutral binding layer, but it must be protected by a hardened PR-L3 Pure Dāl contract; otherwise the semantic chain begins from an under-licensed signifier.**

**Governance Rule**: No Wadh before Pure Dāl. No Dalalah before Wadh. No Hukm before Ifadah. No rank inflation across layers.

---

**الحالة**: فجوة محددة بوضوح
**الأولوية**: عاجلة جداً
**التقدير**: 4 أسابيع
**المالك**: Dal Core team
**المراجع**: [MASTER_PROJECT_PLAN_2026.md](./MASTER_PROJECT_PLAN_2026.md)

**⚠️ هام**: هذه الوثيقة تحلل وتوثق الفجوة. PR #74 نفسه لا يصلح الفجوة - بل يحددها رسمياً.

---

*هذه الوثيقة تحدد الفجوة الأكثر أهمية في المشروع حالياً.*
*This document identifies the most critical gap in the project currently.*
