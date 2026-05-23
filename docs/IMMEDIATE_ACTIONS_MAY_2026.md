# إجراءات فورية - مايو 2026
# Immediate Actions - May 2026

**تاريخ**: 2026-05-23
**الحالة**: خطة عمل فورية
**المدة**: الأسابيع 4 القادمة

---

## 🎯 الهدف الوحيد لهذا الشهر

**إنشاء PR-L3: Pure Dāl Geometry Contract Hardening**

### لماذا؟

```text
فجوة معمارية حرجة:
PR-L4 (Neutral Binding) يربط دالًا غير مكتمل

الحل:
بناء DalCandidate كامل قبل الربط
```

### الأثر

```text
✅ يقوي: PR-L4, PR-L5, PR-L6, والسلسلة الدلالية كاملة
✅ يمكّن: Dal Core roadmap (PR #23-#48)
✅ يوضّح: الحدود المعمارية بين الطبقات
```

---

## 📅 الجدول الزمني (4 أسابيع)

### الأسبوع 1 (23-29 مايو): البنية الأساسية

#### اليوم 1-2: التصميم

```bash
# إنشاء branch
git checkout -b pr-l3/pure-dal-geometry
```

**المهام**:
- [ ] تصميم `DalCandidate` dataclass (18 حقل)
- [ ] تصميم enums الداعمة:
  - [ ] `PathType` (JAMID, MUSHTAQ, SPECIAL)
  - [ ] `PatternStatus` (KNOWN, CANDIDATE, UNKNOWN)
  - [ ] `TerminalState` (MABNI, MURAB, MAMNU_MIN_SARF)
  - [ ] `SignifierRank` (LICENSED, CONTEXTUAL)
  - [ ] `SyntacticReadiness` (READY, NOT_READY)
- [ ] رسم UML diagram

**المخرج**: Design document في `docs/PR_L3_DESIGN.md`

#### اليوم 3-5: التنفيذ الأولي

```python
# ملف: src/dal_core/pure_dal_geometry.py

from dataclasses import dataclass
from typing import Tuple, FrozenSet, Optional, Literal
from enum import Enum

@dataclass(frozen=True)
class DalCandidate:
    """ناتج هندسة الدال وحده"""

    # Phase 1: Phonic foundation
    phonic_carriers: Tuple[PhonicCarrier, ...]
    haraka_operations: Tuple[HarakaOperation, ...]
    syllable_licenses: Tuple[SyllableLicense, ...]

    # Phase 2: Morphological structure
    word_boundaries: WordBoundaryInfo
    clitics: CliticAnalysis
    formula_candidates: Tuple[FormulaCandidate, ...]

    # Phase 3: Classification
    path_type: PathType
    pattern_status: PatternStatus
    terminal_state: TerminalState

    # Phase 4: Syntactic projection
    syntactic_readiness: SyntacticReadiness
    sentence_shape: Optional[SentenceShape]
    role_projection_candidates: Tuple[RoleProjection, ...]

    # Phase 5: Governance
    source_layer: Literal["PURE_DAL"]
    signifier_rank: SignifierRank
    rank: Rank
    residuals: FrozenSet[Residual]
    trace_id: str

    def __post_init__(self):
        # Hard gates
        assert self.source_layer == "PURE_DAL"
        assert self.signifier_rank in (
            SignifierRank.LICENSED,
            SignifierRank.CONTEXTUAL
        )
        assert self.trace_id is not None

        # Forbidden fields check
        forbidden = {'meaning', 'dalalah', 'hukm', 'wadh'}
        for field in forbidden:
            assert not hasattr(self, field)
```

**المخرج**: ملف `pure_dal_geometry.py` مع structure كامل

#### اليوم 6-7: الاختبارات الأساسية

```python
# ملف: tests/dal_core/test_pure_dal_geometry.py

def test_dal_candidate_structure():
    """DalCandidate has all required fields"""
    dal = make_test_dal_candidate()

    # Required fields
    assert hasattr(dal, 'phonic_carriers')
    assert hasattr(dal, 'haraka_operations')
    assert hasattr(dal, 'syllable_licenses')
    # ... test all 18 fields

def test_dal_candidate_forbidden_fields():
    """DalCandidate must NOT have semantic fields"""
    dal = make_test_dal_candidate()

    forbidden = ['meaning', 'dalalah', 'hukm', 'wadh']
    for field in forbidden:
        assert not hasattr(dal, field)

def test_dal_candidate_source_layer():
    """source_layer must be PURE_DAL"""
    dal = make_test_dal_candidate()
    assert dal.source_layer == "PURE_DAL"

def test_dal_candidate_signifier_rank():
    """signifier_rank must be LICENSED or CONTEXTUAL"""
    dal = make_test_dal_candidate()
    assert dal.signifier_rank in (
        SignifierRank.LICENSED,
        SignifierRank.CONTEXTUAL
    )

def test_dal_candidate_immutability():
    """DalCandidate must be frozen"""
    dal = make_test_dal_candidate()
    with pytest.raises(FrozenInstanceError):
        dal.phonic_carriers = ()
```

**المخرج**: 10 اختبارات أساسية تمر

---

### الأسبوع 2 (30 مايو - 5 يونيو): Builder Implementation

#### اليوم 1-3: DalCandidateBuilder

```python
# ملف: src/dal_core/dal_candidate_builder.py

class DalCandidateBuilder:
    """بناء DalCandidate من Raw Signal"""

    def __init__(
        self,
        c1_encoder: C1Encoder,
        c2a_orchestrator: GateOrchestrator,
        c2b_analyzer: MorphologicalAnalyzer
    ):
        self.c1 = c1_encoder
        self.c2a = c2a_orchestrator
        self.c2b = c2b_analyzer

    def build(self, raw_signal: RawSignal) -> DalCandidate:
        """
        Pipeline:
        Raw Signal → C1 → C2a → C2b → DalCandidate
        """
        # Phase 1: C1 Encoding
        carriers = self._extract_phonic_carriers(raw_signal)

        # Phase 2: C2a Phonology
        c2a_result = self.c2a.run(carriers)
        haraka_ops = c2a_result.operations
        syllables = c2a_result.syllables

        # Phase 3: C2b Morphology
        c2b_result = self.c2b.analyze(syllables)

        # Phase 4: Build DalCandidate
        return DalCandidate(
            phonic_carriers=tuple(carriers),
            haraka_operations=tuple(haraka_ops),
            syllable_licenses=tuple(syllables),
            word_boundaries=c2b_result.boundaries,
            clitics=c2b_result.clitics,
            formula_candidates=tuple(c2b_result.formulas),
            path_type=c2b_result.path_type,
            pattern_status=c2b_result.pattern_status,
            terminal_state=c2b_result.terminal_state,
            syntactic_readiness=c2b_result.syntactic_readiness,
            sentence_shape=c2b_result.sentence_shape,
            role_projection_candidates=tuple(c2b_result.roles),
            source_layer="PURE_DAL",
            signifier_rank=self._compute_rank(c2b_result),
            rank=c2b_result.rank,
            residuals=frozenset(c2b_result.residuals),
            trace_id=self._generate_trace()
        )

    def _extract_phonic_carriers(self, signal):
        """C1: Raw → Carriers"""
        return self.c1.encode(signal.text)

    def _compute_rank(self, c2b_result):
        """Determine signifier rank from evidence"""
        if c2b_result.evidence_strength > 0.8:
            return SignifierRank.LICENSED
        return SignifierRank.CONTEXTUAL

    def _generate_trace(self):
        """Generate unique trace ID"""
        import uuid
        return f"DAL_{uuid.uuid4().hex[:8]}"
```

**المخرج**: Builder class كامل

#### اليوم 4-5: Builder Tests

```python
def test_builder_pipeline():
    """Builder creates valid DalCandidate"""
    builder = DalCandidateBuilder(c1, c2a, c2b)
    raw = RawSignal("كَتَبَ")

    dal = builder.build(raw)

    assert isinstance(dal, DalCandidate)
    assert dal.source_layer == "PURE_DAL"
    assert len(dal.phonic_carriers) > 0

def test_builder_trace_generation():
    """Each build generates unique trace"""
    builder = DalCandidateBuilder(c1, c2a, c2b)

    dal1 = builder.build(RawSignal("كتب"))
    dal2 = builder.build(RawSignal("كتب"))

    assert dal1.trace_id != dal2.trace_id

def test_builder_rank_computation():
    """Rank based on evidence"""
    # High evidence → LICENSED
    dal_strong = builder.build(RawSignal("كَتَبَ"))
    assert dal_strong.signifier_rank == SignifierRank.LICENSED

    # Low evidence → CONTEXTUAL
    dal_weak = builder.build(RawSignal("كتب"))
    assert dal_weak.signifier_rank == SignifierRank.CONTEXTUAL
```

**المخرج**: 15 اختبار builder تمر

#### اليوم 6-7: Integration مع Existing Code

```python
# تحديث: src/fvafk/c2b/morphological_analyzer.py

class MorphologicalAnalyzer:
    """تحديث لإنتاج DalCandidate"""

    def analyze_for_dal(self, segments) -> DalCandidate:
        """New method: returns DalCandidate"""
        # Reuse existing logic
        result = self.analyze(segments)

        # Convert to DalCandidate
        return DalCandidate(
            phonic_carriers=result.phonic_carriers,
            # ... map all fields
        )
```

**المخرج**: Integration working

---

### الأسبوع 3 (6-12 يونيو): PR-L4 Integration

#### اليوم 1-3: PR-L4 Enhancement

```python
# تحديث: src/gfa/methods/lafzi_dalalah/dal_madlul_binding_gate.py

class DalMadlulBindingGate:
    """Enhanced with Pure Dāl validation"""

    def validate_dal_candidate(
        self,
        dal: DalCandidate
    ) -> ValidationResult:
        """
        Validate that DalCandidate is from Pure Dāl Geometry

        Hard Gates:
        1. source_layer must be PURE_DAL
        2. signifier_rank must be LICENSED or CONTEXTUAL
        3. No forbidden semantic fields
        4. All required fields present
        5. Trace ID exists
        6. Residuals preserved
        """

        # Gate 1: Source layer
        if dal.source_layer != "PURE_DAL":
            return ValidationResult.fail(
                "DalCandidate must have source_layer=PURE_DAL"
            )

        # Gate 2: Signifier rank
        if dal.signifier_rank not in (
            SignifierRank.LICENSED,
            SignifierRank.CONTEXTUAL
        ):
            return ValidationResult.fail(
                "Invalid signifier_rank"
            )

        # Gate 3: Forbidden fields
        forbidden = ['meaning', 'dalalah', 'hukm', 'wadh']
        for field in forbidden:
            if hasattr(dal, field):
                return ValidationResult.fail(
                    f"Forbidden field found: {field}"
                )

        # Gate 4: Required fields
        required = [
            'phonic_carriers', 'haraka_operations',
            'syllable_licenses', 'word_boundaries',
            # ... all 18 fields
        ]
        for field in required:
            if not hasattr(dal, field):
                return ValidationResult.fail(
                    f"Missing required field: {field}"
                )

        # Gate 5: Trace
        if not dal.trace_id:
            return ValidationResult.fail("Missing trace_id")

        # Gate 6: Residuals
        if dal.residuals is None:
            return ValidationResult.fail("Missing residuals")

        return ValidationResult.pass_()

    def build_binding(
        self,
        dal: DalCandidate,
        madlul: MadlulLafziCandidate
    ) -> DalMadlulBindingResult:
        """Enhanced binding with Pure Dāl validation"""

        # Validate Dal first
        dal_validation = self.validate_dal_candidate(dal)
        if not dal_validation.is_pass():
            return DalMadlulBindingResult.fail(
                dal_validation.reason
            )

        # Continue with existing binding logic
        # ...
```

**المخرج**: PR-L4 gates enhanced

#### اليوم 4-5: Integration Tests

```python
# ملف: tests/gfa/methods/test_pr_l3_l4_integration.py

def test_pr_l4_accepts_pure_dal():
    """PR-L4 accepts DalCandidate from PR-L3"""
    # Build from PR-L3
    dal = dal_builder.build(RawSignal("كتب"))

    # Build Madlul
    madlul = madlul_builder.build("كتب")

    # PR-L4 binding should succeed
    binding = binding_gate.build_binding(dal, madlul)

    assert binding.is_success()

def test_pr_l4_rejects_weak_dal():
    """PR-L4 rejects DalCandidate without PURE_DAL"""
    # Weak Dal (simulated)
    weak_dal = DalCandidate(
        phonic_carriers=(),  # incomplete!
        source_layer="UNKNOWN",  # wrong!
        # ... minimal fields
    )

    madlul = madlul_builder.build("كتب")

    # PR-L4 should reject
    binding = binding_gate.build_binding(weak_dal, madlul)

    assert binding.is_failure()
    assert "source_layer" in binding.failure_reason

def test_pr_l4_rejects_semantic_leakage():
    """PR-L4 rejects Dal with semantic fields"""
    # Dal with forbidden field
    class BadDal(DalCandidate):
        meaning: str = "to write"  # forbidden!

    bad_dal = BadDal(...)
    madlul = madlul_builder.build("كتب")

    # PR-L4 should reject
    binding = binding_gate.build_binding(bad_dal, madlul)

    assert binding.is_failure()
    assert "Forbidden field" in binding.failure_reason
```

**المخرج**: 20 integration tests تمر

#### اليوم 6-7: Documentation Update

```markdown
# docs/PR_L4_DAL_MADLUL_BINDING_SUMMARY.md

## Update: PR-L3 Integration (2026-05-23)

PR-L4 now validates that DalCandidate comes from Pure Dāl Geometry:

### New Validation Gates

1. **Source Layer Gate**: `source_layer == "PURE_DAL"`
2. **Signifier Rank Gate**: `rank ∈ {LICENSED, CONTEXTUAL}`
3. **Forbidden Fields Gate**: No `meaning`/`dalalah`/`hukm`/`wadh`
4. **Completeness Gate**: All 18 required fields present
5. **Trace Gate**: `trace_id` exists
6. **Residual Gate**: `residuals` preserved

### Example

```python
# Build Pure Dāl
dal = DalCandidateBuilder(c1, c2a, c2b).build(
    RawSignal("كَتَبَ")
)

# Build Madlul
madlul = MadlulBuilder().build("كتب")

# Bind (now with validation)
binding = DalMadlulBindingGate().build_binding(dal, madlul)

assert binding.is_success()
assert binding.dal_candidate.source_layer == "PURE_DAL"
```
```

**المخرج**: Updated docs

---

### الأسبوع 4 (13-19 يونيو): Documentation & PR

#### اليوم 1-3: docs/PURE_DAL_GEOMETRY.md

```markdown
# Pure Dāl Geometry (هندسة الدال وحده)

## الملخص

Pure Dāl Geometry هي الطبقة المسؤولة عن:

```
Raw Signal → DalCandidate (licensed signifier)
```

**لا تسأل عن المعنى. تبني الدال فقط.**

## البنية

### DalCandidate

```python
@dataclass(frozen=True)
class DalCandidate:
    # 18 required fields
    # ...
```

### DalCandidateBuilder

```python
class DalCandidateBuilder:
    def build(self, raw: RawSignal) -> DalCandidate:
        # 13-step pipeline
        # ...
```

## Examples

### Example 1: كَتَبَ (فعل)

```python
dal = builder.build(RawSignal("كَتَبَ"))

assert dal.phonic_carriers == (
    PhonicCarrier('ك', ...),
    PhonicCarrier('ت', ...),
    PhonicCarrier('ب', ...)
)
assert dal.path_type == PathType.MUSHTAQ
assert dal.formula_candidates == (
    FormulaCandidate("فَعَلَ", ...),
)
```

### Example 2: كاتِب (اسم فاعل)

```python
dal = builder.build(RawSignal("كاتِب"))

assert dal.path_type == PathType.MUSHTAQ
assert dal.pattern_status == PatternStatus.KNOWN
assert dal.formula_candidates == (
    FormulaCandidate("فاعِل", ...),
)
```

## التكامل

### مع PR-L4

PR-L4 يستقبل DalCandidate من PR-L3 ويربطه بـ MadlulLafziCandidate.

### مع FVAFK

FVAFK C1→C2a→C2b تغذي DalCandidateBuilder.

## اختبارات

30+ اختبار تغطي:
- Structure completeness
- Forbidden fields
- Builder pipeline
- Integration
```

**المخرج**: Documentation complete (100 pages)

#### اليوم 4-5: PR Review Prep

```bash
# Run all tests
pytest tests/dal_core/test_pure_dal_geometry.py -v
pytest tests/gfa/methods/test_pr_l3_l4_integration.py -v

# Run type checks
mypy src/dal_core/pure_dal_geometry.py

# Run coverage
pytest --cov=src/dal_core/pure_dal_geometry --cov-report=html
```

**Checklist**:
- [ ] All tests passing (30+)
- [ ] Type checks passing
- [ ] Coverage ≥ 90%
- [ ] Documentation complete
- [ ] Examples working
- [ ] Integration verified

#### اليوم 6-7: PR Submission

```bash
# Commit
git add src/dal_core/pure_dal_geometry.py
git add src/dal_core/dal_candidate_builder.py
git add src/gfa/methods/lafzi_dalalah/dal_madlul_binding_gate.py
git add tests/dal_core/test_pure_dal_geometry.py
git add tests/gfa/methods/test_pr_l3_l4_integration.py
git add docs/PURE_DAL_GEOMETRY.md
git commit -m "PR-L3: Pure Dāl Geometry Contract Hardening

- Add DalCandidate dataclass (18 required fields)
- Add DalCandidateBuilder (13-step pipeline)
- Add validation gates (source_layer, signifier_rank, forbidden fields)
- Enhance PR-L4 with Pure Dāl validation
- Add 30+ tests
- Add complete documentation

Closes: #XXX (create issue first)
Ref: docs/PURE_DAL_GEOMETRY_GAP_ANALYSIS.md
"

# Push
git push origin pr-l3/pure-dal-geometry

# Create PR
gh pr create \
  --title "PR-L3: Pure Dāl Geometry Contract Hardening" \
  --body "$(cat docs/PURE_DAL_GEOMETRY.md)" \
  --label "priority:critical,layer:dal-core,type:architecture"
```

**المخرج**: PR opened

---

## ✅ معايير القبول

### للأسبوع 1
- [x] `DalCandidate` dataclass كامل
- [x] Enums داعمة معرّفة
- [x] 10 اختبارات أساسية تمر
- [x] Design document

### للأسبوع 2
- [x] `DalCandidateBuilder` مُنفذ
- [x] Pipeline كامل (13 خطوة)
- [x] 15 builder tests تمر
- [x] Integration مع FVAFK

### للأسبوع 3
- [x] PR-L4 gates enhanced
- [x] 20 integration tests تمر
- [x] PR-L4 docs updated

### للأسبوع 4
- [x] `docs/PURE_DAL_GEOMETRY.md` كامل
- [x] All tests passing (30+)
- [x] Coverage ≥ 90%
- [x] PR opened

---

## 📊 التتبع اليومي

### Template للتقرير اليومي

```markdown
## تقرير يومي: [التاريخ]

### ما تم إنجازه
- [ ] المهمة 1
- [ ] المهمة 2

### العوائق
- لا يوجد / [وصف العائق]

### الخطة لليوم التالي
- [ ] المهمة القادمة 1
- [ ] المهمة القادمة 2

### الوقت المستغرق
- [X] ساعات
```

---

## 🚨 نقاط التوقف (Blockers)

### إذا ظهرت هذه المشاكل، توقف واطلب المساعدة

1. **C1/C2a/C2b لا تنتج بيانات كافية**
   - Solution: Extend C2b outputs first

2. **Performance issues** في Builder
   - Solution: Profile first, optimize later

3. **Integration conflicts** مع PR-L4 الموجود
   - Solution: Coordinate with GFA team

4. **Test coverage < 90%**
   - Solution: Add edge case tests

---

## 🎯 التسليمات النهائية

### الملفات المطلوبة (9 files)

1. `src/dal_core/pure_dal_geometry.py` (DalCandidate)
2. `src/dal_core/dal_candidate_builder.py` (Builder)
3. `src/dal_core/enums.py` (PathType, etc.)
4. `src/gfa/methods/lafzi_dalalah/dal_madlul_binding_gate.py` (Enhanced)
5. `tests/dal_core/test_pure_dal_geometry.py` (30 tests)
6. `tests/gfa/methods/test_pr_l3_l4_integration.py` (20 tests)
7. `docs/PURE_DAL_GEOMETRY.md` (100 pages)
8. `docs/PR_L3_DESIGN.md` (Design doc)
9. `docs/PR_L4_DAL_MADLUL_BINDING_SUMMARY.md` (Updated)

### الإحصائيات المستهدفة

- **Lines of code**: ~1,500
- **Tests**: 30+
- **Documentation**: 100+ pages
- **Coverage**: ≥ 90%
- **Performance**: < 10ms per DalCandidate

---

## 📞 جهات الاتصال

### للمساعدة الفنية

- **Dal Core team**: [contact]
- **GFA team**: [contact]
- **FVAFK team**: [contact]

### للمراجعة

- **Architecture review**: [reviewer 1]
- **Code review**: [reviewer 2]
- **Documentation review**: [reviewer 3]

---

**الحالة**: جاهز للتنفيذ
**البدء**: 2026-05-23 (اليوم)
**الانتهاء المتوقع**: 2026-06-19 (4 أسابيع)
**المخرج النهائي**: PR-L3 merged

---

*هذا الملف يحدد كل ما يجب عمله في الأسابيع 4 القادمة.*
*This file specifies everything to be done in the next 4 weeks.*
