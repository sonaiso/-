# K.7: القوى الأربع للشكل السطحي

# K.7: Four Surface Forces Layer Coverage Matrix

**Layer**: K.7
**Domain**: Multiple (D3-D6)
**Status**: ✅ Implemented (MUFRAD_AXES.md)
**Version**: 1.0.0

---

## القوى الأربعة (Four Forces)

```
قوة الحمل (Jamid Force)      ← الجامد
قوة التحول (Mushtaq Force)    ← المشتق / المصدر / الفعل
قوة الإغلاق (Mabni Force)     ← المبني
قوة العلامة (Murab Force)     ← المعرب
```

---

## القيد الحاكم

```
هذه قوى سطحية، لا معانٍ نهائية.
(These are surface forces, not final meanings)
```

---

## Implementation Status

### ✅ Fully Implemented

- `IshtiqaqJudgment` (JAMID/MUSHTAQ)
- `BinaaJudgment` (MABNI/MUERAB)
- `IshtiqaqSubtype` (ISM_FAIL, ISM_MAFUL, etc.)
- `JamidSubtype` (JAMID_DHAT, JAMID_MASDAR_ASLI, etc.)
- `BinaaSubtype` (BINAA_SUKUN, BINAA_FATH, etc.)
- `SarfFlexibility` (MUNSARIF/MAMNU_MIN_SARF)
- `binaa_judge.py` - Judge with 6 rules
- `ishtiqaq_judge.py` - Judge with 8 rules
- `MabniRegistry` - Closed registry of built nouns
- 105+ tests passing

### Documentation

- ✅ `MUFRAD_AXES.md` - Complete specification
- ✅ `test_mufrad_axes.py`
- ✅ `test_binaa_judge.py` (28 tests)
- ✅ `test_ishtiqaq_judge.py` (21 tests)
- ✅ `test_mufrad_axes_integration.py` (13 tests)
- ✅ `test_mufrad_axes_coverage.py` (32 tests)
- ✅ `test_axis_promotion_ban.py` (8 tests)

---

## Status

**✅ CERTIFIED COMPLETE**

This layer is the **only fully certified layer** in the Mufrad coverage matrix.

---

**Cross-References**: MUFRAD_AXES.md (primary documentation)
