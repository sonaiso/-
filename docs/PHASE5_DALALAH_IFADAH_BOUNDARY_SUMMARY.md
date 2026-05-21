# Phase 5: Dāl/Madlūl/Dalālah/Ifādah Boundary Summary

**Status**: ✅ Complete
**Tests**: 39/39 passing (100%)
**PR**: Phase 5.0 Implementation

---

## Executive Summary

Phase 5 implements the **semantic layers** between syntax (Phase 4) and judgment (Phase 6).

**Critical Insight**: Semantics is NOT a single layer. Before ifādah (semantic completion) can be achieved, we must establish **9 intermediate sublayers** (5A-5I).

**Core Principle**:
> الإفادة لا تبدأ من النحو مباشرة ولا من المعجم مباشرة
>
> (Ifādah does not begin directly from syntax or directly from lexicon.
> It requires intermediate layers of dāl, madlūl, binding, and dalālah.)

---

## Architecture: 9 Subphases (5A-5I)

### Phase 5A — Dāl Algebra (Signifier Candidates)

**Law**: الدال وحده ليس معنى (Dāl alone is not meaning)

**Operation**: `DalCandidateOperation`
**Bridge**: SYNTAX → SEMANTICS (identity, no interpretation)
**Output**: Result with polysemy residuals
**Rank**: CANDIDATE (never CERTIFIED without binding)

**Test Coverage**: 3 tests
- ✅ Dāl candidate without evidence stays CANDIDATE
- ✅ Dāl candidate with evidence promotes to LICENSED
- ✅ Dāl alone always carries polysemy residual

---

### Phase 5B — Madlūl Algebra (Signified Candidates)

**Law**: المدلول وحده ليس دلالة (Madlūl alone is not dalālah)

**Operation**: `MadlulCandidateOperation`
**Bridge**: None (madlūl exists in semantic space)
**Output**: Result with dal_binding.absent residual
**Rank**: CANDIDATE (never CERTIFIED without dāl binding)

**Test Coverage**: 2 tests
- ✅ Madlūl candidate without binding has residual
- ✅ Madlūl alone is not dalālah

---

### Phase 5C — Dāl/Madlūl Binding (Wadh' Contract)

**Law**: لا دلالة بلا ربط (No dalālah without binding)

**Operation**: `WadhBindingOperation`
**Bridge**: SEMANTICS → SEMANTICS (binds two semantic candidates)
**Input**: Dāl + Madlūl + Evidence
**Output**: Result with binding or dalalah_gate.required residual
**Rank**: LICENSED with evidence, CANDIDATE without

**Maps to**: A5 (Wadh' Algebra) in PROJECT_ALGEBRA_ARCHITECTURE_MAP.md

**Test Coverage**: 3 tests
- ✅ Wadh' binding without evidence requires gate
- ✅ Wadh' binding with evidence becomes LICENSED
- ✅ Dāl/madlūl binding required (hard gate)

---

### Phase 5D — Individual Dalālah Gates

**Law**: المطابقة والتضمن والالتزام قبل الإفادة
(Mutābaqah, taḍammun, iltizām are **before ifādah**, not ifādah itself)

**Three Gates**:
1. **MutabaqahGate** — Direct correspondence (word → total meaning)
2. **TadammunGate** — Partial inclusion (word → part of meaning)
3. **IltizamGate** — Entailment (word → necessary consequence)

**Critical Rules**:
- Mutābaqah alone does NOT produce ifādah
- Taḍammun alone does NOT produce ifādah
- Iltizām requires explicit gate (not automatic)
- All three are **شروط غير موجبة** (necessary but not sufficient conditions)

**Maps to**: A7 (Dalalah Algebra) in PROJECT_ALGEBRA_ARCHITECTURE_MAP.md

**Test Coverage**: 3 tests
- ✅ Mutābaqah is not ifādah (hard gate)
- ✅ Taḍammun is not ifādah (hard gate)
- ✅ Iltizām requires explicit gate (hard gate)

---

### Phase 5E — Nisbah Semantic (Compositional Semantics)

**Laws**:
- النسبة الإضافية لا تصبح إفادة (Iḍāfah alone does not become ifādah)
- الشرط بلا جواب لا يصبح إفادة (Conditional without jawāb ≠ ifādah)

**Operation**: `NisbahSemanticOperation`
**Bridge**: SYNTAX → SEMANTICS
**Input**: Nisbah type from Phase 4
**Output**: Result with ifādah candidate or insufficiency residual

**Nisbah Types**:
- ISN (إسنادي) → may lead to ifādah
- IDAFA (إضافي) → does NOT become ifādah alone
- TAQYID (تقييدي) → incomplete without predication
- SHART (شرط) → requires jawāb

**Test Coverage**: 3 tests
- ✅ Iḍāfah alone is not ifādah (hard gate)
- ✅ Taqyīd alone is not ifādah (hard gate)
- ✅ Conditional without jawāb is not ifādah (hard gate)

---

### Phase 5F — Reference Resolution

**Law**: الضمير بلا مرجع لا يصبح إفادة معتمدة
(Pronoun without referent cannot produce CERTIFIED ifādah)

**Operation**: `ReferenceResolutionOperation`
**Bridge**: SEMANTICS → SEMANTICS
**Input**: Reference element + referent
**Output**: Result with resolution or pronoun.referent_missing residual
**Rank**: LICENSED if resolved, CANDIDATE if missing

**Resolution Types**:
- Pronoun resolution
- Demonstrative resolution
- Relative clause resolution
- Ellipsis handling
- Conditional jawāb requirement

**Test Coverage**: 2 tests
- ✅ Pronoun without referent cannot certify ifādah (hard gate)
- ✅ Pronoun with referent becomes candidate for licensing

---

### Phase 5G — Speech Force (Illocutionary Force)

**Laws**:
- Khabar does NOT become HUKM
- Inshā does NOT become legal judgment
- Amr does NOT become obligation at Phase 5
- Nahy does NOT become prohibition at Phase 5

**Operation**: `SpeechForceOperation`
**Bridge**: SEMANTICS → SEMANTICS (identity)
**Input**: Utterance + markers
**Output**: Result with speech force type
**Rank**: LICENSED if determined, CANDIDATE if uncertain

**Force Types**: khabar, inshā, amr, nahy, istifhām, shart, nidā, tamannī, tarjjī, taʿajjub

**Maps to**: Partial A8 (Usage Algebra) in PROJECT_ALGEBRA_ARCHITECTURE_MAP.md

**Test Coverage**: 3 tests
- ✅ Khabar is not HUKM (hard gate)
- ✅ Amr is not obligation at Phase 5 (hard gate)
- ✅ Speech force uncertainty creates residual

---

### Phase 5H — Ifādah Closure (Semantic Completion)

**Ifādah requires ALL 8 components**:
1. Licensed parties
2. Licensed dāl/madlūl binding
3. Licensed dalālah (mutābaqah/taḍammun/iltizām)
4. Licensed nisbah
5. Complete structure
6. Resolved references or residuals
7. Known speech force or residual
8. Full residual accounting

**Rank Rules**:
- Ifādah with residuals → CANDIDATE
- Ifādah without residuals + full evidence → CERTIFIED
- Incomplete ifādah → CANDIDATE

**Operation**: `IfadahClosureOperation`
**Bridge**: SEMANTICS → SEMANTICS (closure)

**Maps to**: Partial A9 (Murad Algebra) in PROJECT_ALGEBRA_ARCHITECTURE_MAP.md

**Test Coverage**: 3 tests
- ✅ Ifādah requires all 8 components
- ✅ Ifādah without evidence cannot certify
- ✅ Ifādah complete with evidence becomes CERTIFIED

---

### Phase 5I — Judgment Boundary Guard

**Hard Laws**:
- SEMANTICS cannot jump to HUKM
- IFADAH cannot issue HUKM
- HUKM is Phase 6 (future, separate algebra)

**Operation**: `BoundaryGuardOperation`
**Bridge**: None (guard operation)
**Input**: Attempted transition
**Output**: REFUTED if violation detected

**Maps to**: A9/A10 boundary in PROJECT_ALGEBRA_ARCHITECTURE_MAP.md

**Test Coverage**: 2 tests
- ✅ SEMANTICS cannot jump to HUKM (hard gate)
- ✅ IFADAH cannot issue HUKM (hard gate)

---

## Residual Taxonomy (13 Residuals)

Phase 5 introduces **13 canonical semantic residual kinds**:

### Dāl/Madlūl/Binding (5A-5C)
1. `semantics.polysemy.possible` — Dāl has multiple possible madlūl
2. `semantics.dal_binding.absent` — Madlūl not bound to dāl yet
3. `semantics.dalalah_gate.required` — Binding requires evidence

### Dalālah Gates (5D)
4. `semantics.mutabaqah.insufficient` — Mutābaqah alone ≠ ifādah
5. `semantics.tadammun.insufficient` — Taḍammun alone ≠ ifādah
6. `semantics.iltizam.gate_missing` — Iltizām requires explicit gate

### Nisbah Semantic (5E)
7. `semantics.idafah.not_ifadah` — Iḍāfah alone ≠ ifādah
8. `semantics.taqyid.incomplete` — Taqyīd incomplete without predication
9. `semantics.conditional.jawab_missing` — Conditional requires jawāb

### Reference Resolution (5F)
10. `semantics.pronoun.referent_missing` — Pronoun without referent

### Speech Force (5G)
11. `semantics.speech_force.uncertain` — Speech act type unclear

### Ifādah Closure (5H)
12. `semantics.ifadah.incomplete` — Ifādah requirements not met

### Boundary Guard (5I)
13. `semantics.hukm_boundary.violation` — Attempted SEMANTICS → HUKM jump

---

## Hard Gates Enforced (14 Gates)

All Phase 5 hard gates are tested and verified:

### Dāl/Madlūl Separation
```python
✅ dāl_alone_is_not_meaning()
✅ madlūl_alone_is_not_dalālah()
✅ dāl_madlūl_binding_required()
```

### Dalālah Gates
```python
✅ mutābaqah_is_not_ifādah()
✅ taḍammun_is_not_ifādah()
✅ iltizām_requires_gate()  # Not automatic
```

### Nisbah Gates
```python
✅ iḍāfah_alone_is_not_ifādah()
✅ taqyīd_alone_is_not_ifādah()
✅ conditional_without_jawāb_is_not_ifādah()
```

### Reference Gates
```python
✅ pronoun_without_referent_cannot_certify_ifādah()
```

### Speech Force Gates
```python
✅ khabar_is_not_hukm()
✅ amr_is_not_obligation_at_phase5()
✅ nahy_is_not_prohibition_at_phase5()
```

### Boundary Gates
```python
✅ ifādah_with_residuals_cannot_certify()
✅ semantics_cannot_jump_to_hukm()
✅ ifādah_cannot_issue_hukm()
```

---

## Test Coverage (39 tests, 100% passing)

### Residual Taxonomy (8 tests)
- ✅ Canonical set of 13 residuals
- ✅ Polysemy residual creation
- ✅ Dal binding absent residual
- ✅ Mutābaqah insufficient residual
- ✅ Iltizām gate missing residual
- ✅ Iḍāfah not ifādah residual
- ✅ Conditional jawāb missing residual
- ✅ HUKM boundary violation residual

### Phase 5A: Dāl Candidate (3 tests)
- ✅ Without evidence stays CANDIDATE
- ✅ With evidence promotes to LICENSED
- ✅ Dāl alone is not meaning (hard gate)

### Phase 5B: Madlūl Candidate (2 tests)
- ✅ Without binding has dal_binding.absent
- ✅ Madlūl alone is not dalālah (hard gate)

### Phase 5C: Wadh' Binding (3 tests)
- ✅ Without evidence requires gate
- ✅ With evidence becomes LICENSED
- ✅ Dal/madlūl binding required (hard gate)

### Phase 5D: Dalālah Gates (3 tests)
- ✅ Mutābaqah is not ifādah (hard gate)
- ✅ Taḍammun is not ifādah (hard gate)
- ✅ Iltizām requires gate (hard gate)

### Phase 5E: Nisbah Semantic (3 tests)
- ✅ Iḍāfah alone is not ifādah (hard gate)
- ✅ Taqyīd alone is not ifādah (hard gate)
- ✅ Conditional without jawāb is not ifādah (hard gate)

### Phase 5F: Reference Resolution (2 tests)
- ✅ Pronoun without referent cannot certify ifādah
- ✅ Pronoun with referent becomes candidate

### Phase 5G: Speech Force (3 tests)
- ✅ Khabar is not HUKM (hard gate)
- ✅ Amr is not obligation at Phase 5 (hard gate)
- ✅ Speech force uncertainty creates residual

### Phase 5H: Ifādah Closure (3 tests)
- ✅ Requires all 8 components
- ✅ Without evidence cannot certify
- ✅ Complete with evidence becomes CERTIFIED

### Phase 5I: Boundary Guard (2 tests)
- ✅ SEMANTICS cannot jump to HUKM
- ✅ IFADAH cannot issue HUKM

### Evidence Integration (1 test)
- ✅ Evidence supports semantic operations

### Domain Boundary (1 test)
- ✅ Semantic operations never claim HUKM

### Rank Invariants (2 tests)
- ✅ LICENSED rank requires evidence
- ✅ CERTIFIED rank forbids residuals

### Regression Tests (2 tests)
- ✅ Phase 0 Rank set unchanged
- ✅ Phase 0 Result structure unchanged

### Integration Test (1 test)
- ✅ Full semantic chain (Dāl → Madlūl → Binding → Dalālah → Nisbah → Ifādah)

---

## Files Changed

### New Files (4)
1. `src/fvafk/algebra/semantics/__init__.py` (120 lines)
2. `src/fvafk/algebra/semantics/residual_taxonomy.py` (320 lines)
3. `src/fvafk/algebra/semantics/operations.py` (685 lines)
4. `tests/test_algebra_semantics_phase5.py` (590 lines)

### Modified Files (1)
1. `docs/ARABIC_ALGEBRA_ROADMAP.md` — Phase 5 expanded to 5A-5I subphases

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
- ✅ `src/fvafk/algebra/syntax/` — No changes

---

## Exit Criteria ✅

- [x] All 39 Phase 5 tests pass
- [x] Dāl alone is not meaning (hard gate enforced)
- [x] Madlūl alone is not dalālah (hard gate enforced)
- [x] Mutābaqah/taḍammun/iltizām are not ifādah (hard gates enforced)
- [x] Iḍāfah alone is not ifādah (hard gate enforced)
- [x] Conditional without jawāb is not ifādah (hard gate enforced)
- [x] Pronoun without referent cannot certify ifādah (hard gate enforced)
- [x] Khabar is not HUKM (hard gate enforced)
- [x] SEMANTICS cannot jump to HUKM (hard gate enforced)
- [x] IFADAH cannot issue HUKM (hard gate enforced)
- [x] All Phase 0, 1, 2, 3, 4 tests remain green
- [x] FVAFK pipeline unchanged
- [x] Bridge matrix unchanged
- [x] Rank set unchanged

---

## What's Next: Phase 6 — Code Learning & CI Integration

After Phase 5, the algebraic chain is:

```
Phase 0: Constitution (لا مخرج عارٍ)
Phase 1: Decision tree governance
Phase 2: Evidence adapters (C1, C2a, C2b, Syntax)
Phase 3: Algebraic morphology (Pattern, Root, Affix)
Phase 4: Algebraic syntax (Mabni, Mu'rab, Amil, I'rab, Nisbah)
Phase 5: Semantic algebra (Dāl, Madlūl, Dalālah, Ifādah, Boundary) ← YOU ARE HERE
Phase 6: Code-learning algebra & CI integration
```

---

**Phase 5 Complete** ✅
**Date**: 2026-05-21
**Tests**: 39/39 passing (100%)
**Regression**: All prior phases passing (100%)
**Hard Gates**: 14/14 enforced (100%)
