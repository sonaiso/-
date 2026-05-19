# dal_core Phase 2: Vocalized Arabic Word Expansion

**Status**: Planning Complete
**Date**: 2026-05-19
**Version**: 2.0 Planning Document

---

## Executive Summary

### Phase 1 Achievement (Complete ✅)

```text
نجحت مرحلة تأسيس dal_core governed proof pipeline.
```

**Evidence**:
- PR #5 merged successfully
- All 51 dal_core tests passing (100%)
- 10 non-negotiable acceptance conditions implemented
- Governed proof spine with evidence/rank/residuals/trace
- Semantic leakage prevention verified
- DClosed traceable to raw Unicode input

**Current Capability**:
```text
dal_core implements a governed proof spine for الدال وحده (signifier-only).
```

### Phase 2 Goal (This Document)

```text
Move dal_core from governed proof spine to governed vocalized Arabic word analyzer for supported cases.
```

**Target Capability**:
```text
dal_core can analyze supported fully vocalized Arabic word forms under governed contracts.
```

**Forbidden Claim**:
```text
dal_core fully analyzes all Arabic texts.  [❌ NOT TRUE - needs expansion]
```

---

## Core Principle (Non-Negotiable)

### Scope: الدال وحده (Signifier-Only)

This phase remains **inside signifier analysis**. No semantic meaning inference.

**Allowed Expansions**:
```python
D_form       # Morphological forms with patterns
D_lugha      # Linguistic attestation (witness sources)
D_type       # Type classification (اسم/فعل/حرف)
D_mufrad     # Closed signifier with morph features
Syllable     # Prosodic patterns (CV/CVC/CVV/CVVC/CVCC)
MorphFeatures  # Root/wazn/jamid/mushtaq candidates
```

**Forbidden Outputs** (Theorem 5):
```python
meaning           # ❌
semantic          # ❌
madlul            # ❌
murad             # ❌
haqiqa            # ❌
majaz             # ❌
reality_ref       # ❌
grounding         # ❌
intended_meaning  # ❌
```

**Compliance Check**: All Phase 2 outputs must pass semantic leak detection tests.

---

## Scientific Assessment

### What Phase 1 Achieved

```text
1. وجود هيكل تنفيذي حاكم للدال وحده
   (Governed executive structure for signifier-only)

2. وجود بقايا ورتب وأدلة وتتبع
   (Residuals, ranks, evidence, tracing exist)

3. منع semantic leak
   (Semantic leakage prevented)

4. منع certificate مع blocker
   (Certificate blocked with blocker residuals)

5. حفظ residuals
   (Residuals preserved)

6. ضبط weakest-link rank
   (Weakest-link rank ceiling enforced)
```

### What Phase 1 Did NOT Achieve

```text
1. تحليل كل النصوص العربية المشكولة
   (Analysis of all vocalized Arabic texts)

2. تغطية كافية للشواهد اللغوية
   (Sufficient linguistic witness coverage)

3. تغطية شاملة للمقاطع العربية والعروض
   (Comprehensive syllable and prosody coverage)

4. تصنيفًا صرفيًا واسعًا للجامد والمشتق
   (Broad morphological classification)

5. تصنيفًا شاملًا للمعرفة والنكرة والتذكير والتأنيث
   (Comprehensive definiteness/gender classification)

6. قدرة عامة على الجمل والنصوص المركبة
   (General sentence and compositional text capability)
```

**Gap**: Items 1-5 above are Phase 2 scope. Item 6 is future (Phase 3+).

---

## Phase 2 Scope

### 1. Syllable Contract Expansion

**Current State**: Stub implementation with 4 syllable types

**Target**: Complete operational syllable analyzer

#### Required Patterns

```text
CV    - قصير مفتوح (كَ، تُ، بِ)
CVC   - قصير مغلق (كَتْ، تُبْ)
CVV   - طويل مفتوح (كَا، تُو، بِي)
CVVC  - طويل مغلق (كَاتْ، تُوبْ)
CVCC  - فائق الطول (كَتْبْ)
```

#### Required Features

**Shadda (الشدة)**:
- Theorem: Shadda = gemination/doubled effect
- Trace: Must show shadda expansion or doubling evidence
- Test: `test_shadda_trace`

**Tanwin (التنوين)**:
- Theorem: Tanwin = operational marker (not semantic)
- Trace: Must preserve tanwin type (fath/damm/kasr)
- Test: `test_tanwin_operational_trace`

**Sukun (السكون)**:
- Theorem: Sukun closes syllable
- Residual: Invalid sukun placement produces blocker
- Test: `test_sukun_closes_syllable`

**Madd (المد)**:
- Theorem: Madd lengthens syllable nucleus
- Pattern: Alif/waw/ya with appropriate vowel
- Test: `test_madd_lengthens_syllable`

#### Required Tests

```python
test_cv_syllable               # كَتَبَ → كَ/تَ/بَ
test_cvc_syllable              # كَتْبُ → كَتْ/بُ
test_cvv_syllable              # كَاتِبٌ → كَا/تِ/بٌ
test_cvvc_syllable             # الكَاتِبْ → الْ/كَا/تِبْ
test_cvcc_syllable             # قُلْتُ → قُلْ/تُ
test_shadda_trace              # مُدَرِّسٌ shadda expansion
test_tanwin_operational_trace  # كِتَابٌ tanwin preserved
test_sukun_closes_syllable     # سَكَنْ final sukun
test_madd_lengthens_syllable   # قَالَ madd alif
test_invalid_syllable_pattern_blocks_certificate  # Invalid patterns
```

#### Implementation Location

File: `src/dal_core/syllables.py`

Add functions:
```python
def parse_syllables(units: list[OperativeUnit]) -> tuple[list[Syllable], list[Residual]]
def validate_syllable_pattern(syllable: Syllable) -> list[Residual]
def handle_shadda(atom: ArabicAtom) -> tuple[list[ArabicAtom], dict]  # trace
def handle_tanwin(atom: ArabicAtom) -> tuple[ArabicAtom, dict]  # trace
def handle_sukun(atom: ArabicAtom, position: str) -> list[Residual]
def handle_madd(atoms: list[ArabicAtom]) -> tuple[list[ArabicAtom], dict]
```

---

### 2. D_lugha Witness Expansion

**Current State**: Stub rank enum, minimal SEED_LEXICON

**Target**: Governed witness store with explicit attestation ranks

#### Required Ranks

```python
class LughaRank(Enum):
    ZERO = 0         # No attestation
    FORM_ONLY = 1    # Pattern exists but unattested
    QIYAS = 2        # Permitted analogy
    SAMA = 3         # Specific hearing
    AHAD = 4         # Singular transmission
    TAWATUR = 5      # Mass transmission
```

#### Critical Theorems

**Theorem 3**: D_form ⊄ D_lugha
```text
Pattern/weight alone is NOT linguistic attestation.
```

**Theorem**: Qiyas ≠ Sama
```text
Analogy is not the same as hearing.
Qiyas must be ranked lower than Sama.
```

#### Seed Witness Store

File: `src/dal_core/witness_store.py` (new)

Structure:
```python
@dataclass
class WitnessRecord:
    form: str                    # Vocalized form
    normalized_form: str         # Normalized
    type: LexicalType           # ISM/FIIL/HARF
    rank: LughaRank             # Attestation rank
    source: str                 # Source identifier
    notes: str                  # Additional info

WITNESS_STORE: dict[str, WitnessRecord] = {
    "كَتَبَ": WitnessRecord(
        form="كَتَبَ",
        normalized_form="كتب",
        type=LexicalType.FIIL,
        rank=LughaRank.TAWATUR,
        source="Quran, Classical corpus",
        notes="Past tense verb, root ك-ت-ب"
    ),
    "كِتَابٌ": WitnessRecord(
        form="كِتَابٌ",
        normalized_form="كتاب",
        type=LexicalType.ISM,
        rank=LughaRank.TAWATUR,
        source="Quran 2:2, Classical lexicons",
        notes="Noun, pattern فِعَال"
    ),
    # ... minimum 10-15 clear examples
}
```

#### Required Tests

```python
test_weight_not_attestation              # Pattern ≠ proof
test_form_only_does_not_close_lugha     # FORM_ONLY is not certificate
test_qiyas_rank_is_not_sama             # Qiyas < Sama
test_ahad_attestation_closes_with_ahad_rank  # Ahad witness → Ahad rank
test_tawatur_attestation_closes_with_tawatur_rank  # Tawatur → Tawatur
test_unknown_witness_blocks_certificate  # No witness → blocker
test_residuals_preserved_from_d_form_to_d_lugha  # Non-erasing union
```

#### Integration

Update `src/dal_core/pipeline.py`:
```python
def prove_lugha(d_form: DForm, witness_store: dict) -> DLugha:
    # Lookup in witness store
    record = witness_store.get(d_form.vocalization)

    if record:
        # Attested
        rank = record.rank
        is_arabic = True
        sources = [record.source]
    else:
        # Unattested
        rank = LughaRank.FORM_ONLY
        is_arabic = False
        sources = []
        residuals.append(Residual(
            code="LUGHA_WITNESS_MISSING",
            message="Form not attested in witness store",
            severity=Severity.WARNING
        ))

    # ... build LughaAttestation
```

---

### 3. D_type Hardening

**Current State**: Basic type classification stub

**Target**: Type requires D_lugha, handles ambiguity

#### Required Rules

1. **Type depends on D_lugha**:
   - Cannot close type without attestation
   - Test: `test_d_type_requires_d_lugha`

2. **Ambiguous type emits residual**:
   - Some forms have multiple valid types
   - Test: `test_ambiguous_type_emits_residual`

3. **Type is not meaning**:
   - ISM/FIIL/HARF are signifier categories
   - Test: `test_type_does_not_emit_meaning`

#### Implementation

Update `src/dal_core/d_type.py`:
```python
@dataclass
class TypedDal:
    attestation: LughaAttestation
    dal_type: DalType  # ISM | FIIL | HARF | AMBIGUOUS | UNRESOLVED
    type_evidence: list[str] = field(default_factory=list)
    residuals: list[Residual] = field(default_factory=list)
    trace: dict = field(default_factory=dict)

    def is_closed(self) -> bool:
        return (
            self.attestation.is_arabic and
            self.attestation.rank != LughaRank.ZERO and
            self.dal_type != DalType.AMBIGUOUS and
            self.dal_type != DalType.UNRESOLVED
        )
```

Update `src/dal_core/pipeline.py`:
```python
def infer_type(d_lugha: DLugha) -> DType:
    # Rule: Cannot type without lugha
    if d_lugha.rank == LughaRank.ZERO:
        residuals.append(Residual(
            code="TYPE_REQUIRES_LUGHA",
            message="Cannot determine type without attestation",
            severity=Severity.BLOCKER
        ))
        return TypedDal(
            attestation=d_lugha,
            dal_type=DalType.UNRESOLVED,
            residuals=residuals
        )

    # Lookup witness record for type
    # Handle ambiguous cases
    # ...
```

#### Required Tests

```python
test_d_type_requires_d_lugha     # No lugha → blocker
test_attested_ism_type           # Witness says ISM → ISM
test_attested_fiil_type          # Witness says FIIL → FIIL
test_attested_harf_type          # Witness says HARF → HARF
test_ambiguous_type_emits_residual  # Multiple types → residual
test_type_does_not_emit_meaning  # No semantic fields
```

---

### 4. MorphFeatures Contract (New)

**Purpose**: Add non-semantic morphological feature candidates

**Critical**: These are **signifier features**, NOT meanings.

#### Dataclass

File: `src/dal_core/morph_features.py` (new)

```python
@dataclass
class MorphFeatures:
    """
    Morphological feature candidates (signifier-level only)

    Critical: These are CANDIDATES with evidence/rank/residuals.
    NOT absolute classifications.
    NO semantic meaning.
    """
    root_candidate: Optional[tuple[str, ...]] = None
    root_evidence: list[Evidence] = field(default_factory=list)
    root_residuals: list[Residual] = field(default_factory=list)

    wazn_candidate: Optional[str] = None  # Pattern like فَعَلَ
    wazn_evidence: list[Evidence] = field(default_factory=list)
    wazn_residuals: list[Residual] = field(default_factory=list)

    is_jamid_candidate: Optional[bool] = None  # جامد
    is_mushtaq_candidate: Optional[bool] = None  # مشتق
    derivation_evidence: list[Evidence] = field(default_factory=list)
    derivation_residuals: list[Residual] = field(default_factory=list)

    is_mabni_candidate: Optional[bool] = None  # مبني
    is_murab_candidate: Optional[bool] = None  # معرب
    inflection_evidence: list[Evidence] = field(default_factory=list)
    inflection_residuals: list[Residual] = field(default_factory=list)

    definiteness_candidate: Optional[str] = None  # معرفة/نكرة/unresolved
    definiteness_evidence: list[Evidence] = field(default_factory=list)

    gender_candidate: Optional[str] = None  # مذكر/مؤنث/unresolved
    gender_evidence: list[Evidence] = field(default_factory=list)

    number_candidate: Optional[str] = None  # مفرد/مثنى/جمع/unresolved
    number_evidence: list[Evidence] = field(default_factory=list)

    verb_form_candidate: Optional[int] = None  # Form I-X
    verb_tense_form: Optional[str] = None  # ماضي/مضارع/أمر (form, not meaning)
    verb_voice_form: Optional[str] = None  # معلوم/مجهول (form, not meaning)
    verb_evidence: list[Evidence] = field(default_factory=list)

    all_residuals: list[Residual] = field(default_factory=list)
    trace: dict = field(default_factory=dict)
```

#### Critical Theorems

**Theorem**: Root extraction is candidate-based
```text
Root cannot be absolute without witness.
Extracted root is CANDIDATE with residuals.
```

**Theorem**: Wazn does not prove lugha
```text
Pattern detection ≠ attestation.
Wazn is CANDIDATE pending witness confirmation.
```

**Theorem**: Jamid/Mushtaq may be ambiguous
```text
Pattern alone insufficient in many cases.
Evidence required for closure.
```

#### Required Tests

```python
test_root_candidate_has_residual_if_not_witnessed
test_wazn_candidate_does_not_prove_lugha
test_jamid_mushtaq_ambiguous_when_evidence_insufficient
test_mabni_candidate_for_harf
test_fiil_madi_form_detection
test_majhul_pattern_detection
test_definiteness_al_detection
test_definiteness_without_marker_unresolved
test_gender_ta_marbuta_formal_candidate
test_gender_samai_requires_witness
test_number_dual_marker_candidate
test_plural_marker_candidate
test_morph_features_no_semantic_leak
```

#### Integration with D_mufrad

Update `src/dal_core/d_mufrad.py`:
```python
@dataclass(frozen=True)
class DClosed:
    typed_dal: TypedDal
    morph_features: Optional[MorphFeatures] = None  # NEW
    is_mufrad: bool = True
    is_placeable: bool = True
    final_rank: LughaRank = LughaRank.ZERO
    all_residuals: tuple[Residual, ...] = field(default_factory=tuple)
    full_trace: dict = field(default_factory=dict)

    # ✅ Still NO semantic fields
    # ✅ morph_features contains only candidates with evidence/residuals
```

Update `src/dal_core/pipeline.py`:
```python
def extract_morph_features(d_type: DType) -> MorphFeatures:
    # Extract root candidate
    # Detect wazn pattern
    # Infer jamid/mushtaq candidates
    # Detect definiteness markers
    # All with evidence/rank/residuals
    # ...

def close_mufrad(d_type: DType) -> DMufrad:
    # Extract morph features
    morph_features = extract_morph_features(d_type)

    # Preserve all residuals (non-erasing union)
    all_residuals = list(d_type.residuals)
    all_residuals.extend(morph_features.all_residuals)

    # Weakest-link rank
    rank = min_rank(d_type.rank, rank_from_morph_features(morph_features))

    # Build DClosed with morph_features
    # ...
```

---

### 5. Golden Dataset

**Purpose**: Verified test fixtures for end-to-end validation

File: `tests/fixtures/dal_core/golden_vocalized_words.json` (new)

#### Structure

```json
{
  "clear_cases": [
    {
      "input": "كَتَبَ",
      "expected": {
        "d_form_status": "valid",
        "d_lugha_rank": "TAWATUR",
        "d_type": "FIIL",
        "morph_features": {
          "root_candidate": ["ك", "ت", "ب"],
          "wazn_candidate": "فَعَلَ",
          "verb_tense_form": "ماضي"
        },
        "forbidden_fields_absent": ["meaning", "murad", "semantic"],
        "expected_residuals": []
      }
    },
    {
      "input": "كِتَابٌ",
      "expected": {
        "d_form_status": "valid",
        "d_lugha_rank": "TAWATUR",
        "d_type": "ISM",
        "morph_features": {
          "root_candidate": ["ك", "ت", "ب"],
          "wazn_candidate": "فِعَال",
          "definiteness_candidate": "نكرة",
          "number_candidate": "مفرد"
        },
        "forbidden_fields_absent": ["meaning", "murad", "semantic"],
        "expected_residuals": []
      }
    }
  ],
  "residual_cases": [
    {
      "input": "كتب",
      "expected": {
        "d_form_status": "unvocalized",
        "d_lugha_rank": "ZERO",
        "expected_residuals": ["MISSING_VOCALIZATION"],
        "certificate_blocked": true
      }
    },
    {
      "input": "غَرِيبٌ",
      "expected": {
        "d_form_status": "valid",
        "d_lugha_rank": "FORM_ONLY",
        "expected_residuals": ["LUGHA_WITNESS_MISSING"],
        "certificate_blocked": false
      }
    }
  ]
}
```

#### Test Runner

File: `tests/dal_core/test_golden_dataset.py` (new)

```python
def test_golden_clear_cases():
    """Test clear attested cases from golden dataset"""
    with open("tests/fixtures/dal_core/golden_vocalized_words.json") as f:
        data = json.load(f)

    for case in data["clear_cases"]:
        result = analyze_dal_mufrad(case["input"])

        # Verify rank
        assert result.final_rank.name == case["expected"]["d_lugha_rank"]

        # Verify type
        assert result.typed_dal.dal_type.name == case["expected"]["d_type"]

        # Verify morph features
        if "morph_features" in case["expected"]:
            assert result.morph_features is not None
            # Check specific features

        # Verify no semantic leak
        for field in case["expected"]["forbidden_fields_absent"]:
            assert not hasattr(result, field)

def test_golden_residual_cases():
    """Test cases with expected residuals"""
    # ...
```

---

### 6. Documentation Updates

#### Update Files

1. **docs/DAL_CORE_COMPLIANCE.md**
   - Add Phase 2 completion section
   - Update test count
   - Document new contracts
   - Update residual taxonomy

2. **src/dal_core/README.md**
   - Update version to 2.0
   - Add Phase 2 completion statement
   - Document new modules
   - Update success criteria

3. **This document** (DAL_CORE_PHASE2_COMPLETION_PLAN.md)
   - Complete implementation log
   - Final acceptance report

---

## Acceptance Criteria

Phase 2 is complete ONLY if:

- [ ] All dal_core tests pass (target: 70+ tests)
- [ ] All theorem tests pass (21+ theorems)
- [ ] All semantic leak tests pass (no regressions)
- [ ] Golden dataset tests pass (10+ fixtures)
- [ ] Syllable patterns fully tested (CV/CVC/CVV/CVVC/CVCC)
- [ ] D_lugha ranks are explicit and tested
- [ ] D_type requires D_lugha (enforced)
- [ ] MorphFeatures have evidence/rank/residuals
- [ ] No semantic fields in any output
- [ ] Rank obeys weakest-link ceiling
- [ ] Residuals are preserved (non-erasing)
- [ ] Blockers prevent certificate
- [ ] Trace to raw input preserved

---

## Allowed Claims After Phase 2

### ✅ Allowed

```text
dal_core supports governed analysis of selected fully vocalized Arabic word forms
under explicit witnesses, rules, ranks, and residuals.
```

```text
dal_core implements contracts 1-9 with morphological feature candidates.
```

```text
dal_core handles CV/CVC/CVV/CVVC/CVCC syllable patterns with trace.
```

### ❌ Forbidden

```text
dal_core fully analyzes all Arabic texts.  [Needs broader witness coverage]
```

```text
dal_core handles syntax composition.  [Future: Phase 3+]
```

```text
dal_core infers meaning or intent.  [Violates Theorem 5]
```

---

## Implementation Sequence

### PR A: Syllable Expansion
- Expand syllable patterns
- Add shadda/tanwin/madd/sukun handling
- Add 10 syllable tests

### PR B: D_lugha Witness Store
- Create witness_store.py
- Add seed witnesses (10-15 entries)
- Add 7 D_lugha tests

### PR C: D_type Hardening
- Require D_lugha for type
- Handle ambiguous types
- Add 6 D_type tests

### PR D: MorphFeatures Contract
- Create morph_features.py
- Integrate with D_mufrad
- Add 13 morph feature tests

### PR E: Golden Dataset
- Create golden_vocalized_words.json
- Add test_golden_dataset.py
- Add 10+ fixture tests

### PR F: Documentation
- Update DAL_CORE_COMPLIANCE.md
- Update README.md
- Finalize this document with completion report

---

## Out of Scope (Future Phases)

### Phase 3+: Compositional Analysis
- Multi-word phrases
- ISN/TADMN/TAQYID relations
- Operator semantics
- Sentence-level composition

### Future: Semantic Layers
- W (وضع): Dāl + madlūl pairing
- Dalalah (دلالة): mutabaqah / tadammun / iltizam
- Isti'mal (استعمال): haqiqah / majaz
- Murad (مراد): intended meaning

### Future: Higher Layers
- GLCFL (grounded language)
- Reality grounding
- Conceptual models
- Pragmatic inference

---

## Signature

**Document Created**: 2026-05-19
**Status**: Planning Complete, Implementation Ready
**Next Step**: Begin PR A (Syllable Expansion)

**Compliance Statement**: This plan maintains all Phase 1 theorems and acceptance conditions while expanding governed signifier analysis capability.
