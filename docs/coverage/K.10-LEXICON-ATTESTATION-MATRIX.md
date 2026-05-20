# K.10: طبقة المعجم والسماع

# K.10: Lexicon and Attestation Layer Coverage Matrix

**Layer**: K.10
**Domain**: All layers (cross-cutting)
**Status**: ❌ Not Implemented (no integrated lexicon)
**Version**: 1.0.0

---

## المبدأ الأساسي

```
إذا كان الحكم يحتاج سماعًا ولا يوجد معجم/شاهد:
لا Certificate.

If judgment requires attestation and no lexicon/witness:
No Certificate.
```

---

## Required Concepts

### Sama' Types
- ❌ سماع آحاد (singular attestation)
- ❌ سماع تواتر (multiple attestations)
- ❌ سماع إجماع (consensus)

### Lexicon Requirements

#### For Frozen Words (جوامد)
- ❌ Concrete nouns: رجل، حجر، امرأة
- ❌ Proper names: محمد، مكة، زيد
- ❌ Broken plurals: رِجَال (from رجل)
- ❌ Functional particles: هذا، الذي، أنا

#### For Orthography (K.1)
- ❌ Uthmanic variants
- ❌ Irregular hamza positions
- ❌ Proper name orthography

#### For Gender (K.8)
- ❌ Metaphorical gender: شمس (feminine), قمر (masculine)
- ❌ Lexical feminine: طلحة، حمزة

#### For Transitivity (K.9)
- ❌ Attested transitivity: رَغِبَ في، طَمِعَ في

#### For Weak Letter Identity (K.5)
- ❌ Original و vs ي: قال (واوي), باع (يائي)

#### For Irregular Forms
- ❌ Irregular verbs: رأى، أكل
- ❌ Irregular masdars
- ❌ Loanwords: تلفون، كمبيوتر

---

## Allowed Claims

- ❌ `LexiconEntryCandidate`
- ❌ `AttestationEvidence`
- ❌ `SamaaRank` (AHAD/TAWATUR/IJMAA)

---

## Current Status

### ❌ Completely Missing

No integrated lexicon exists.

Some heuristics exist for:
- Common particles (من، إلى، على)
- Demonstratives (هذا، ذلك)
- Pronouns (أنا، هو)

But no formal lexicon structure.

---

## Required Files

```
data/lexicon/
├── core_lexicon.json (500+ entries)
├── frozen_nouns.json
├── proper_names.json
├── broken_plurals.json
├── weak_verb_identity.json (و vs ي)
├── metaphorical_gender.json
├── transitivity.json
├── irregular_forms.json
└── loanwords.json

src/dal_core/
├── lexicon_lookup.py
├── attestation_manager.py
└── sama_rank.py

tests/dal_core/
├── test_lexicon_lookup.py (50+ tests)
└── test_attestation.py (30+ tests)
```

---

## Gap Analysis

**This is the FOUNDATION for certification.**

Without lexicon:
- Cannot certify gender for metaphorical cases
- Cannot certify weak letter identity
- Cannot certify transitivity
- Cannot certify broken plurals
- Cannot certify proper names

**Priority**: **Critical**
**Estimated**: 6-8 weeks

---

## Implementation Priority

1. **Phase 1**: Core lexicon structure (500 entries)
2. **Phase 2**: Weak verb identity database
3. **Phase 3**: Metaphorical gender + broken plurals
4. **Phase 4**: Transitivity + irregular forms

---

**This layer is required for CERTIFICATION of all other layers.**

---

**Cross-References**: All layers K.1-K.9 require lexicon support
