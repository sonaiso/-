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
5. **S** (Syllable) → CV, CVC, CVV, CVVC patterns
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
from dal_core import DalPipeline

pipeline = DalPipeline()
dclosed, residuals = pipeline.process("كِتَابٌ")

# Enforce Theorem 5: No meaning in output
assert dclosed.meaning is None
assert dclosed.murad is None
assert dclosed.haqiqa_majaz is None
```

## Installation

```bash
# From repository root
python3 -c "import sys; sys.path.insert(0, 'src'); import dal_core"
```

## Testing

```bash
python3 tests/dal_core/test_runner.py
```

## Core Modules

- `carriers.py` - Contract 1: Unicode → Carrier
- `atoms.py` - Contract 2: Carrier → ArabicAtom
- `units.py` - Contract 3: Atoms → OperativeUnit
- `context.py` - Contract 4: Context enrichment
- `syllables.py` - Contract 5: Units → Syllables
- `d_form.py` - Contract 6: Syllables → FormCandidate
- `d_lugha.py` - Contract 7: Form → LughaAttestation
- `d_type.py` - Contract 8: Attestation → TypedDal
- `d_mufrad.py` - Contract 9: TypedDal → DClosed
- `pipeline.py` - Full pipeline orchestrator

## Success Criteria

The system succeeds if:

- ✅ Unicode ≠ Letter enforced
- ✅ D_form ⊄ D_lugha enforced
- ✅ Pattern alone insufficient for attestation
- ✅ Type required before mufrad
- ✅ **No meaning/murad/haqiqa_majaz in output** (ENFORCED)
- ✅ Every decision has evidence + rank + residuals
- ✅ Full trace graph available
- ✅ ML ranks but doesn't create

## Documentation

- [SPEC_DAL_CORE.md](../../docs/SPEC_DAL_CORE.md) - Complete specification

## Version

0.1.0 - Initial implementation (Phase 0 & 1 complete)

## Status

**Phase 1 Complete**: Core foundation implemented and tested.

Next: Implement full pipeline stages (Units → Syllables → Form → Lugha → Type → Mufrad)
