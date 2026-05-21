# Phase 4: Algebraic Syntax — Implementation Summary

## النحو الجبري لا يحكم بالمعنى النهائي، بل يرخص علاقة تركيبية محفوظة الأثر والرتبة والبقايا

**Status**: ✅ Complete
**PR**: This PR
**Tests**: 43/43 passing
**Regression**: All Phase 0-3 tests passing

---

## Core Principles Implemented

### 1. النحو يرخص علاقة (Syntax licenses relations)
Syntax operations license relational structure only, never final meaning or HUKM.

**Proof**: `test_syntax_licenses_structure_not_meaning`

```python
operator_result = governed_mabni_operator("لم", evidence=(...))
assert operator_result.rank == Rank.LICENSED  # Not CERTIFIED
assert len(operator_result.residuals) > 0     # Residuals present
```

### 2. No SYNTAX → HUKM jump
Syntax operations never emit `hukm.*` evidence kinds.

**Proof**: `test_syntax_operations_never_claim_hukm`

```python
for result in all_syntax_results:
    for ev in result.evidence:
        assert not ev.kind.startswith("hukm.")
```

### 3. No SYNTAX → SEMANTICS certification with residuals
Syntax operations with residuals stay LICENSED, never CERTIFIED.

**Proof**: `test_nisbah_binding_may_license_but_not_certify_with_residuals`

```python
result = governed_nisbah_binding("ISN", evidence=(...))
assert result.rank == Rank.LICENSED  # Not CERTIFIED
assert len(result.residuals) > 0     # Residuals remain
```

### 4. SyntaxAdapter as witness only
Adapters provide evidence, not judgment — operations make governed decisions.

**Proof**: `test_evidence_from_syntax_adapter_supports_syntax_claims`

```python
evidence = (Evidence(kind="syntax.relation_candidate", source="adapter:SyntaxAdapter:1"),)
result = governed_nisbah_binding("ISN", evidence=evidence)
assert result.rank == Rank.LICENSED  # Evidence supports, but residuals remain
```

---

## Architecture

### Module Structure

```
src/fvafk/algebra/syntax/
├── __init__.py              # Public API
├── residual_taxonomy.py     # 10 residual kinds + constructors
└── operations.py            # 5 governed operations + wrappers
```

### Residual Taxonomy (10 kinds)

1. **syntax.context_absent** — Surrounding tokens needed for disambiguation
2. **syntax.operator_scope_unresolved** — Operator scope not determined (e.g., إن, لم)
3. **syntax.case_missing** — Case marking (إعراب) not visible on surface
4. **syntax.case_estimated** — Case marking estimated/inferred (تقدير)
5. **syntax.case_ambiguous** — Multiple case readings possible
6. **syntax.governor_ambiguous** — Multiple possible عامل candidates
7. **syntax.ellipsis_possible** — Possible ellipsis (حذف) in structure
8. **syntax.attachment_ambiguous** — Unclear which phrase attaches where
9. **syntax.relation_candidate** — Relation type (ISN/TADMN/TAQYID) not finalized
10. **syntax.word_order_ambiguous** — Multiple word order interpretations

**Proof**: `test_syntax_residual_kinds_canonical_set`

### Governed Operations (5 operations)

#### 1. MabniClosedOperatorOperation (مبني)

Identifies closed operators (particles) such as:
- لم، لن، لا (negation/mood particles)
- إن، أن، كأن، لكن، ليت، لعل (inna sisters)
- من، ما، متى، أين، كيف (interrogative/relative particles)

**Bridge**: SYNTAX → SYNTAX (identity)
**Input**: Operator candidate (e.g., "لم")
**Output**: Result with CANDIDATE/LICENSED rank
**Residuals**: context.absent, operator_scope_unresolved

```python
op = MabniClosedOperatorOperation()
carrier = Carrier(domain=Domain.SYNTAX, value="لم")
result = op.run(carrier)
# Result(value="لم", rank=CANDIDATE, residuals=(...))
```

**Proof**: `test_mabni_operator_returns_result_with_provenance`

#### 2. MurabOpenCarrierOperation (معرب)

Treats معرب (inflectable) words as open relational carriers:
- Require a governor (عامل) to determine case
- May have visible, estimated, or ambiguous case marks
- Carry relational potential (subject/object/complement)

**Bridge**: SYNTAX → SYNTAX (identity)
**Input**: Word form (e.g., "كاتبٌ")
**Output**: Result with residuals for governor/case
**Residuals**: context.absent, governor_ambiguous, case_missing

```python
op = MurabOpenCarrierOperation()
carrier = Carrier(domain=Domain.SYNTAX, value="كاتبٌ")
result = op.run(carrier)
# Requires governor → governor_ambiguous residual
```

**Proof**: `test_murab_carrier_requires_governor`

#### 3. AmilFunctionOperation (عامل)

Represents العامل (governor) as an operating function over a dependent:
- Verb governing subject/object
- Particle governing noun (إن governing ism)
- Preposition governing majrur

**Bridge**: SYNTAX → SYNTAX (identity)
**Input**: Amil candidate (e.g., "كان", "إن")
**Output**: Result with scope/attachment residuals
**Residuals**: context.absent, operator_scope_unresolved, attachment_ambiguous

**Proof**: `test_amil_function_needs_governed_element`

#### 4. IrabRelationEffectOperation (إعراب)

Represents الإعراب as an effect of syntactic relation, not a bare vowel:
- رفع as effect of subject relation (fael/mubtada)
- نصب as effect of object relation (maf'ul) or inna operation
- جر as effect of preposition or idafa
- جزم as effect of jazm operators

Distinguishes:
- Visible case (ظاهر)
- Estimated case (تقدير)
- Local case (محلي)
- Missing case
- Ambiguous case

**Bridge**: SYNTAX → SYNTAX (identity)
**Input**: Word with case marking
**Output**: Result with case-related residuals
**Residuals**: context.absent, case_missing/estimated/ambiguous

```python
op = IrabRelationEffectOperation()
carrier = Carrier(domain=Domain.SYNTAX, value="الكتابُ")  # Has damma
result = op.run(carrier)
# Creates case_ambiguous residual (even with visible case)
```

**Proof**: `test_irab_effect_detects_visible_case`

#### 5. NisbahBindingOperation (نسبة)

Binds syntactic relation candidates:
- ISN (إسنادي) — Predicative relation (mubtada-khabar, fael-fi'l)
- TADMN (تضميني) — Complement relation (maf'ul, khabar kaana)
- TAQYD (تقييدي) — Modifier relation (sifa, haal, zarf)
- IDAFA (إضافي) — Possessive/genitive relation
- HALI (حالي) — Circumstantial relation
- ZARFI (ظرفي) — Adverbial relation

**Bridge**: SYNTAX → SYNTAX (identity)
**Input**: Relation candidate (e.g., "ISN")
**Output**: Result with relation residuals
**Residuals**: context.absent, relation_candidate, word_order_ambiguous, ellipsis_possible

**Proof**: `test_nisbah_binding_creates_relation_candidate_residual`

### Convenience Wrappers

```python
# Mabni operator
result = governed_mabni_operator("لم", evidence=(...))

# Mu'rab carrier
result = governed_murab_carrier("كاتبٌ", evidence=(...))

# Amil function
result = governed_amil_function("كان", evidence=(...))

# I'rab effect
result = governed_irab_effect("الكتابُ", evidence=(...))

# Nisbah binding
result = governed_nisbah_binding("ISN", evidence=(...))
```

---

## Evidence Integration

Phase 4 operations consume Evidence from Phase 2 SyntaxAdapter:

```python
from fvafk.algebra.adapters import SyntaxAdapter
from fvafk.algebra.syntax import governed_nisbah_binding

adapter = SyntaxAdapter()
# Hypothetical: adapter.adapt(link) → Evidence

result = governed_nisbah_binding("ISN", evidence=evidence_from_adapter)
# Promotes to LICENSED when Evidence present
assert result.rank == Rank.LICENSED
```

**Proof**: `test_evidence_from_syntax_adapter_supports_syntax_claims`

---

## Domain Boundary Enforcement

### No SYNTAX → SEMANTICS jump

```python
result = governed_mabni_operator("لم", evidence=(...))
for ev in result.evidence:
    assert not ev.kind.startswith("semantic.")
```

**Proof**: `test_syntax_operations_never_claim_semantics`

### No SYNTAX → HUKM jump

```python
result = governed_nisbah_binding("ISN", evidence=(...))
for ev in result.evidence:
    assert not ev.kind.startswith("hukm.")
```

**Proof**: `test_syntax_operations_never_claim_hukm`

---

## Rank Invariants

### 1. LICENSED requires Evidence

```python
# This fails:
Result(value="test", rank=Rank.LICENSED, evidence=())
# ValueError: LICENSED requires at least one Evidence
```

**Proof**: `test_licensed_rank_requires_evidence`

### 2. CERTIFIED forbids residuals

```python
# This fails:
Result(
    value="test",
    rank=Rank.CERTIFIED,
    evidence=(Evidence(...),),
    residuals=(Residual(...),)
)
# ValueError: CERTIFIED cannot have residuals
```

**Proof**: `test_certified_rank_forbids_residuals`

### 3. Fatal Failure forces REFUTED

```python
# This fails:
Result(
    value="test",
    rank=Rank.CANDIDATE,  # Not REFUTED
    failures=(Failure(kind="error", fatal=True),)
)
# ValueError: fatal Failure requires REFUTED rank
```

**Proof**: `test_fatal_failure_forces_refuted`

---

## Test Coverage (43 tests)

### Residual Taxonomy (11 tests)
- ✅ Canonical set (10 residuals)
- ✅ `make_context_absent()`
- ✅ `make_operator_scope_unresolved()` with operator
- ✅ `make_case_missing()`
- ✅ `make_case_estimated()`
- ✅ `make_case_ambiguous()` with cases
- ✅ `make_governor_ambiguous()`
- ✅ `make_ellipsis_possible()`
- ✅ `make_attachment_ambiguous()`
- ✅ `make_relation_candidate()` with relation types
- ✅ `make_word_order_ambiguous()`

### MabniClosedOperatorOperation (6 tests)
- ✅ Returns Result with provenance
- ✅ Stays CANDIDATE without Evidence
- ✅ Never CERTIFIED with residuals
- ✅ Refutes on domain mismatch
- ✅ Convenience wrapper
- ✅ Promotes to LICENSED with Evidence

### MurabOpenCarrierOperation (4 tests)
- ✅ Returns Result
- ✅ Requires governor
- ✅ Detects missing case
- ✅ Promotes with Evidence

### AmilFunctionOperation (3 tests)
- ✅ Returns Result
- ✅ Needs governed element
- ✅ Never claims semantics

### IrabRelationEffectOperation (4 tests)
- ✅ Returns Result
- ✅ Detects visible case
- ✅ Detects missing case
- ✅ Is relational, not bare vowel

### NisbahBindingOperation (4 tests)
- ✅ Returns Result
- ✅ Creates relation_candidate residual
- ✅ May license but not certify with residuals
- ✅ Cannot jump to HUKM

### Evidence Integration (1 test)
- ✅ Evidence from SyntaxAdapter supports syntax claims

### Domain Boundary Enforcement (2 tests)
- ✅ No SEMANTICS claims
- ✅ No HUKM claims

### Rank Invariants (3 tests)
- ✅ LICENSED requires Evidence
- ✅ CERTIFIED forbids residuals
- ✅ Fatal Failure forces REFUTED

### Regression Tests (4 tests)
- ✅ Phase 0 Rank set unchanged
- ✅ Phase 0 bridge matrix unchanged
- ✅ Phase 2 adapters still available
- ✅ Phase 3 morphology operations still available

### النحو الجبري (1 test)
- ✅ Syntax licenses structure, not meaning

---

## Files Changed

### New Files (4)
1. `src/fvafk/algebra/syntax/__init__.py` (105 lines)
2. `src/fvafk/algebra/syntax/residual_taxonomy.py` (235 lines)
3. `src/fvafk/algebra/syntax/operations.py` (610 lines)
4. `tests/test_algebra_syntax_phase4.py` (550+ lines)

### Modified Files (1)
1. `docs/ARABIC_ALGEBRA_ROADMAP.md` — Phase 4 marked complete

### Unchanged Files (Critical)
- ✅ `src/fvafk/c1/` — No changes
- ✅ `src/fvafk/c2a/` — No changes
- ✅ `src/fvafk/c2b/` — No changes
- ✅ `src/fvafk/syntax/` — No changes
- ✅ `src/dal_core/` — No changes
- ✅ `src/fvafk/algebra/core.py` — No changes
- ✅ `src/fvafk/algebra/cpb.py` — No changes
- ✅ `src/fvafk/algebra/policies.py` — No changes
- ✅ `src/fvafk/algebra/arabic_layers.py` — No changes
- ✅ `src/fvafk/algebra/morphology/` — No changes

---

## Exit Criteria ✅

- [x] All 43 Phase 4 tests pass
- [x] Mabni operator with Evidence promotes to LICENSED
- [x] Mabni operator never CERTIFIED with residuals
- [x] Mu'rab carrier creates governor_ambiguous residual
- [x] I'rab effect distinguishes visible/missing/estimated case
- [x] Nisbah binding creates relation_candidate residual
- [x] Fatal contradiction forces REFUTED
- [x] All Phase 0, 0.5, 1, 2, 3 tests remain green
- [x] No SYNTAX → SEMANTICS jump without Evidence
- [x] No SYNTAX → HUKM jump
- [x] Syntax operations never emit `semantic.*` evidence
- [x] Syntax operations never emit `hukm.*` evidence
- [x] FVAFK pipeline unchanged
- [x] Bridge matrix unchanged
- [x] Rank set unchanged

---

## What's Next: Phase 5 — Dalalah/Ifadah/Judgment Boundary

After Phase 4, the algebraic chain is:

```
Phase 0: Constitution (لا مخرج عارٍ)
Phase 1: Decision tree governance
Phase 2: Evidence adapters (C1, C2a, C2b, Syntax)
Phase 3: Algebraic morphology (Pattern, Root, Affix)
Phase 4: Algebraic syntax (Mabni, Mu'rab, Amil, I'rab, Nisbah) ← YOU ARE HERE
Phase 5: Dalalah/Ifadah/Judgment boundary
```

Phase 5 will establish the governed boundary between:
- **Syntax** (relational structure) → **Semantics** (lexical meaning)
- **Semantics** → **Murad** (intended meaning)
- **Murad** → **Hukm** (inference/judgment)

Each boundary will have:
- Clear transition contract
- Evidence requirements
- Rank promotion rules
- Residual propagation

The core principle for Phase 5:

```
الدلالة ليست الحكم
المعنى المعجمي ليس المعنى المراد
المعنى المراد ليس الحكم النهائي
```

(Lexical meaning is not intended meaning; intended meaning is not final inference)

---

**Phase 4 Complete** ✅
**Date**: 2026-05-21
**Tests**: 43/43 passing (100%)
**Regression**: All prior phases passing (100%)
