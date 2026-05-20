# DAL Core - الدال وحده

**Signifier-Only Analysis System** following Nabahani linguistic methodology.

## المبدأ (Principle)

```
نبني برهانًا للدال وحده داخل عقود معلنة،
لا برهانًا للمعنى ولا للمراد.
```

**We build a proof for the signifier alone within declared contracts,
not a proof for meaning nor for intent.**

## Architecture

Pipeline: **U → A → O → S → F → L → T → D**

1. **U** (Unicode) → **Carrier** - Unicode is not a letter, it's a carrier
2. **A** (ArabicAtom) → Classification into letters, vowels, marks
3. **O** (OperativeUnit) → حرف + حركة combinations
4. **Context** → Entry/judgment gates, wasl/waqf
5. **S** (Syllable) → CV, CVC, CVV, CVVC, CVCC patterns
6. **F** (FormCandidate) → Morphological forms
7. **L** (LughaAttestation) → Linguistic attestation (رواية، سماع، قياس)
8. **T** (TypedDal) → Classification (اسم، فعل، حرف)
9. **D** (DClosed) → Closed signifier unit

## Six Theorems (المبرهنات الست)

1. **لا Unicode بلا عقد** - Unicode ≠ Letter without contracts
2. **لا دال من حرف مفرد** - Single character ≠ Closed signifier
3. **لا عربية من الوزن وحده** - Pattern alone ≠ Arabic attestation
4. **لا مفرد بلا نوع** - No mufrad without type
5. **لا معنى داخل الدال** - No meaning in signifier (CRITICAL)
6. **التعلم لا يرفع الرتبة** - ML ranks but doesn't create

## Usage

```python
from dal_core import analyze_dal_mufrad

# Analyze vocalized Arabic word
result = analyze_dal_mufrad("كِتَابٌ")

# Enforce Theorem 5: No meaning in output
assert not hasattr(result, 'meaning')
assert not hasattr(result, 'murad')
assert not hasattr(result, 'haqiqa_majaz')

# Access signifier-only analysis
print(result.typed_dal.dal_type)  # ISM
print(result.final_rank)  # TAWATUR (if attested)
print(result.all_residuals)  # Empty if clean
```

## Installation

```bash
# From repository root
pip install -e .
# Or directly
python3 -c "import sys; sys.path.insert(0, 'src'); import dal_core"
```

## Testing

```bash
# All dal_core tests
pytest tests/dal_core/ -v

# Specific test suites
pytest tests/dal_core/test_theorems.py -v       # 21 theorem tests
pytest tests/dal_core/test_syllables.py -v      # 16 syllable tests
pytest tests/dal_core/test_witness_store.py -v  # 27 witness tests
pytest tests/dal_core/test_golden_dataset.py -v # 26 dataset tests
```

## Core Modules

### Phase 1 (Complete)
- `carriers.py` - Contract 1: Unicode → Carrier
- `atoms.py` - Contract 2: Carrier → ArabicAtom
- `units.py` - Contract 3: Atoms → OperativeUnit
- `context.py` - Contract 4: Context enrichment (stub)
- `d_form.py` - Contract 6: Syllables → FormCandidate (stub)
- `d_lugha.py` - Contract 7: Form → LughaAttestation (stub)
- `d_type.py` - Contract 8: Attestation → TypedDal (stub)
- `d_mufrad.py` - Contract 9: TypedDal → DClosed
- `pipeline.py` - Full pipeline orchestrator
- `ranks.py` - Linguistic attestation ranks
- `residuals.py` - Residual types and utilities
- `evidence.py` - Evidence tracking

### Phase 2 (Complete)
- `syllables.py` - Contract 5: Units → Syllables (expanded)
  - CV/CVC/CVV/CVVC/CVCC patterns
  - Shadda, tanwin, madd, sukun handling
- `witness_store.py` - Linguistic attestation database (new)
  - 16 seed attestations
  - TAWATUR/AHAD/SAMA/QIYAS/FORM/ZERO ranks
  - Source provenance

### Mufrad Axes (PR-A → PR-G)

Four orthogonal axes that close the singular form *before* it enters
composition. See [`docs/MUFRAD_AXES.md`](../../docs/MUFRAD_AXES.md) for the
full plan.

- `mufrad_axes.py` — Typed enums for all four axes:
  `BinaaJudgment`, `BinaaSubtype`, `IshtiqaqJudgment`, `MushtaqSubtype`,
  `JamidSubtype`, `SarfFlexibility`.
- `mabni_registry.py` — Immutable closed registry of mabni nouns
  (pronouns, demonstratives, relative nouns, interrogatives/conditionals,
  built adverbs, action-nouns, compound numerals). Backed by
  `MappingProxyType`; safe to share at module scope.
- `binaa_judge.py` — `judge_binaa(BinaaJudgeInput) → BinaaJudgmentResult`.
  Rules in priority order: harf ⇒ MABNI; past/imperative ⇒ MABNI;
  imperfect + nun-nuswa/tawkid ⇒ MABNI; imperfect otherwise ⇒ MUERAB;
  noun in `MabniRegistry` ⇒ MABNI + subtype; otherwise ⇒ MUERAB.
  **Does NOT accept syllable count or syllable shapes as input.**
- `ishtiqaq_judge.py` — `judge_ishtiqaq(IshtiqaqJudgeInput) → IshtiqaqJudgmentResult`.
  Handles harf/fiil (NOT_APPLICABLE), functional/proper/concrete jamid,
  and the nine mushtaq subtypes via wazn matching.

Integration points:
- `mufrad_proof.py` — Five new optional fields on `MufradProof`:
  `binaa_judgment`, `binaa_subtype`, `ishtiqaq_judgment`,
  `ishtiqaq_subtype`, `sarf_flexibility`. `__post_init__` enforces typed
  subtypes (no free-form strings).
- `morph_features.NounInflectionClass` — Added optional `binaa_judgment`
  and `sarf_flexibility` fields; legacy `inflection_type` string preserved.
- `case_sign_matrix._is_mabni_by_value` — Prefers the classified
  `binaa_judgment`, falls back to the legacy string.
- `presyntax_vector.PreSyntaxMufradVector` — Exposes both judgments; the
  `allows_operator_consumption` gate has a 5th rule blocking on
  `UNRESOLVED` binaa (any type) or `UNRESOLVED` ishtiqaq (nouns only).
- `dal_algebra.FORBIDDEN_AXIS_PROMOTIONS` + `assert_axis_promotion_allowed()` —
  Categorical ban on `SYLLABIC → BINAA_JUDGMENT` and
  `SYLLABIC → ISHTIQAQ_JUDGMENT`, with no escape hatch.

## Success Criteria

The system succeeds if:

### Phase 1 Criteria ✅
- ✅ Unicode ≠ Letter enforced
- ✅ D_form ⊄ D_lugha enforced
- ✅ Pattern alone insufficient for attestation
- ✅ Type required before mufrad
- ✅ **No meaning/murad/haqiqa_majaz in output** (ENFORCED)
- ✅ Every decision has evidence + rank + residuals
- ✅ Full trace graph available
- ✅ ML ranks but doesn't create

### Phase 2 Criteria ✅
- ✅ Syllable patterns tested (CV/CVC/CVV/CVVC/CVCC)
- ✅ Shadda/tanwin/madd/sukun traces operational
- ✅ Witness store with explicit ranks
- ✅ Theorem 3 verified: Pattern ≠ attestation
- ✅ Golden dataset validates end-to-end behavior
- ✅ 122 tests passing (100% pass rate)

## Documentation

- [SPEC_DAL_CORE.md](../../docs/SPEC_DAL_CORE.md) - Complete specification
- [DAL_CORE_COMPLIANCE.md](../../docs/DAL_CORE_COMPLIANCE.md) - Phase 1 compliance report
- [DAL_CORE_PHASE2_COMPLETION_PLAN.md](../../docs/DAL_CORE_PHASE2_COMPLETION_PLAN.md) - Phase 2 implementation plan
- [DAL_CORE_PHASE2_STATUS.md](../../docs/DAL_CORE_PHASE2_STATUS.md) - Phase 2 status report

## Version

**2.0** - Phase 2 Complete (Syllable + Witness Expansion)
- 122 tests passing
- Syllable patterns operational
- Witness store with 16 attestations
- Golden dataset for validation

**1.0** - Phase 1 Complete (Proof Spine)
- 51 tests passing
- Governed contracts
- Semantic leak prevention

## Status

**Phase 2 Complete**: Core syllable and witness expansion implemented.

**Allowed Claims**:
```text
dal_core implements governed proof spine for الدال وحده (signifier-only).
dal_core supports syllable analysis (CV/CVC/CVV/CVVC/CVCC) with trace.
dal_core provides linguistic attestation via witness store with explicit ranks.
dal_core enforces Theorem 3: Pattern ≠ attestation (D_form ⊄ D_lugha).
dal_core enforces Theorem 5: No semantic fields (لا معنى داخل الدال).
```

**Forbidden Claims**:
```text
dal_core fully analyzes all Arabic texts.        ❌ (limited witness coverage)
dal_core performs complete morphology.           ❌ (MorphFeatures pending)
dal_core handles sentence composition.           ❌ (syntax is future work)
dal_core infers semantic meaning.                ❌ (violates Theorem 5)
```

**Next**: Documentation updates, optional contract hardening (D_type, MorphFeatures).
