# مواصفة نظام الدال وحده (DAL Core Specification)

## 1. الهدف (Objective)

```
نبني برهانًا للدال وحده داخل عقود معلنة،
لا برهانًا للمعنى ولا للمراد.
```

**System Goal**: Transform vocalized Arabic text into closed signifier units (DClosed) without inferring semantic meaning.

```
Input:  نص عربي مشكول (vocalized Arabic text)
Output: DClosed(d) = {
    typed_dal: TypedDal,
    is_mufrad: bool,
    is_placeable: bool,
    final_rank: LughaRank,
    all_residuals: List[Residual],
    full_trace: Graph,
    meaning: None,      # MUST be None
    murad: None,        # MUST be None
    haqiqa_majaz: None  # MUST be None
}
```

## 2. الفضاءات الرياضية (Mathematical Spaces)

### Pipeline Chain

```
U → A → O → S → F → L → T → D
```

Where:
- **U** = Unicode carriers (حوامل يونيكود)
- **A** = ArabicAtoms (ذرات عربية)
- **O** = OperativeUnits (وحدات تشغيلية)
- **S** = Syllables (مقاطع)
- **F** = FormCandidates (مرشحات صورية)
- **L** = LughaAttestation (ثبوت لغوي)
- **T** = TypedDal (دال منوّع)
- **D** = DClosed (دال مغلق)

## 3. العقود التسعة (Nine Contracts)

### Contract 1: Unicode Carrier
```python
Carrier(char: str, codepoint: int, index: int, unicode_name: str)
```
**Constraint**: Unicode ≠ Letter (المبرهنة 1)

### Contract 2: ArabicAtom
```python
ArabicAtom(
    kind: AtomKind,  # LETTER|VOWEL|MARK|SUKUN|SHADDA|TANWIN|...
    carrier: Carrier,
    features: Dict[str, Any],
    evidence: List[str],
    rank: float,
    residuals: List[Residual]
)
```
**Constraint**: ك ≠ "number 22", ك = Atom with recoverable features

### Contract 3: OperativeUnit
```python
OperativeUnit(
    base_letter: ArabicAtom,
    mark_bundle: List[ArabicAtom],
    position: int,
    residuals: List[Residual]
)
```
**Constraint**: حرف + حركة only; orphan vowel → BLOCKER residual

### Contract 4: Context
```python
UnitContext(
    unit: OperativeUnit,
    prev_unit: Optional[OperativeUnit],
    next_unit: Optional[OperativeUnit],
    is_entry_gate: bool,
    is_judgment_gate: bool,
    is_wasl: bool,
    is_waqf: bool
)
```

### Contract 5: Syllable
```python
Syllable(
    type: SyllableType,  # CV|CVC|CVV|CVVC
    onset: List[ArabicAtom],
    nucleus: List[ArabicAtom],
    coda: List[ArabicAtom],
    units: List[OperativeUnit],
    residuals: List[Residual]
)
```

### Contract 6: D_form
```python
FormCandidate(
    text: str,
    vocalization: str,
    syllables: List[Syllable],
    morph_shape: str,
    rank: FormRank,
    residuals: List[Residual],
    trace: TraceNode
)
```
**Constraint**: D_form ⊄ D_lugha (المبرهنة 3)

### Contract 7: D_lugha
```python
LughaAttestation(
    form: FormCandidate,
    rank: LughaRank,  # ZERO|FORM|QIYAS|SAMA|AHAD|TAWATUR
    sources: List[str],
    is_arabic: bool,
    residuals: List[Residual],
    trace: TraceNode
)
```
**Principle**: العربية بالرواية والسماع، لا بالوزن وحده

### Contract 8: D_type
```python
TypedDal(
    attestation: LughaAttestation,
    dal_type: DalType,  # ISM|FIIL|HARF|AMBIGUOUS
    type_evidence: List[str],
    residuals: List[Residual],
    trace: TraceNode
)
```
**Constraint**: No mufrad without type (المبرهنة 4)

### Contract 9: D_mufrad
```python
DClosed(
    typed_dal: TypedDal,
    is_mufrad: bool,
    is_placeable: bool,
    final_rank: LughaRank,
    all_residuals: List[Residual],
    full_trace: Graph,
    meaning: None = None,
    murad: None = None,
    haqiqa_majaz: None = None
)
```
**Constraint**: meaning|murad|haqiqa_majaz MUST be None (المبرهنة 5)

## 4. المبرهنات الست (Six Theorems)

### Theorem 1: لا Unicode بلا عقد
```
∀ u ∈ Unicode: u ∉ ArabicAtom unless u passes Carrier → Atom contracts
```

### Theorem 2: لا دال من حرف مفرد
```
∀ a ∈ ArabicAtom: a ∉ DClosed
```

### Theorem 3: لا عربية من الوزن وحده
```
D_form(x) ⊄ D_lugha(x)
```

### Theorem 4: لا مفرد بلا نوع
```
∀ d: DClosed(d) ⇒ ∃ t: D_type(d) = t ∧ t ≠ AMBIGUOUS
```

### Theorem 5: لا معنى داخل الدال
```
∀ d ∈ DClosed: d.meaning = None ∧ d.murad = None
```

### Theorem 6: التعلم لا يرفع الرتبة
```
ML_rank(candidates) → ordering only
ML_rank(candidates) ⊄ create(SAMA | TAWATUR | W)
```

## 5. Residual Types

```python
class ResidualSeverity(Enum):
    INFO = 0      # Informational
    WARNING = 1   # Non-blocking warning
    BLOCKER = 2   # Prevents closure

class ResidualType(Enum):
    # Carrier level
    NON_ARABIC_SYMBOL = "رمز غير عربي"
    AMBIGUOUS_SYMBOL = "رمز ملتبس"

    # Atom level
    UNKNOWN_ATOM = "ذرة مجهولة"

    # Unit level
    ORPHAN_MARK = "علامة يتيمة"
    MISSING_VOCALIZATION = "تشكيل ناقص"

    # Form level
    INVALID_SYLLABLE = "مقطع غير صحيح"

    # Lugha level
    NOT_ATTESTED = "غير مثبت لغويًا"

    # Type level
    AMBIGUOUS_TYPE = "نوع ملتبس"
```

## 6. Rank System

```python
class LughaRank(Enum):
    ZERO = 0      # غير ثابت
    FORM = 1      # صورة فقط
    QIYAS = 2     # قياس مرخص
    SAMA = 3      # سماع خاص
    AHAD = 4      # آحاد لغوي
    TAWATUR = 5   # تواتر
```

## 7. Closure Conditions

```python
def is_closed(d: DClosed) -> bool:
    return (
        d.typed_dal.attestation.is_arabic and
        d.typed_dal.dal_type != DalType.AMBIGUOUS and
        d.is_mufrad and
        not has_blocking_residuals(d.all_residuals) and
        d.meaning is None and
        d.murad is None and
        d.haqiqa_majaz is None
    )
```

## 8. Test Requirements

### Critical Tests (Must Pass)

1. **test_unicode_not_letter**: Unicode ≠ ArabicAtom
2. **test_vowel_not_letter**: Vowel ≠ Letter
3. **test_orphan_vowel_blocks**: Vowel without letter → BLOCKER
4. **test_form_not_lugha**: Valid form may not be attested
5. **test_no_meaning_in_dclosed**: DClosed.meaning must be None
6. **test_ml_cannot_create**: ML cannot create atoms/sama/tawatur

## 9. MVP Scope

**Input**: Single vocalized word (كلمة واحدة مشكولة)
**Output**: DClosed or blocking residuals

**Coverage**:
- ✅ 28 letters + hamza + alif maqsurah
- ✅ 3 vowels (fatha, damma, kasra)
- ✅ Shadda, sukun, tanwin
- ✅ Syllables (CV, CVC, CVV, CVVC)
- ✅ D_form → D_lugha → D_type → D_mufrad
- ✅ Seed lexicon (100 words)

**Out of Scope (Phase 2+)**:
- ❌ Unvocalized text
- ❌ Multi-word phrases
- ❌ I'rab analysis
- ❌ Semantic fields
- ❌ Prosodic meter

## 10. Success Criteria

The system succeeds if:

1. ✅ Unicode ≠ Letter enforced
2. ✅ D_form ⊄ D_lugha enforced
3. ✅ Pattern alone insufficient for attestation
4. ✅ Type required before mufrad
5. ✅ No meaning/murad/haqiqa_majaz in output
6. ✅ Every decision has evidence + rank + residuals
7. ✅ Full trace graph available
8. ✅ ML ranks but doesn't create

---

**Version**: 1.0.0
**Date**: 2026-05-19
**Status**: Specification Complete
