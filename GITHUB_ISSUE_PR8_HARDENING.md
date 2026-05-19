# GitHub Issue: Harden MufradProof with Pre-Syntax Interface Layer

**Labels**: enhancement, dal_core, phase-2
**References**: PR #8
**Priority**: High

## Summary

PR #8 successfully implemented `MufradProof` as composition-ready D_mufrad with morphological and surface proof. However, before proceeding to syntax composition (العوامل النحوية المئة), we must add a hardening layer that:

1. Explicitly separates **CaseSignPotential** (allowed in MufradProof) from **CaseEffect** (forbidden in MufradProof)
2. Provides a typed **PreSyntaxMufradVector** interface for operator contracts
3. Defines **OperatorReadiness** contracts without implementing syntax operators
4. Models original/substitute case signs as surface potentials, not semantic judgments
5. Strengthens competitor resolution requirements
6. Creates a stub registry for future grammar operators (source/school/rank-bound)

## Why This Matters

The next phase will model the hundred grammatical operators as ranked `OperatorContract`s. Therefore:

```text
✓ MufradProof must preserve: morphology, surface effects, case sign potentials, rank, residuals, trace
✗ MufradProof must NOT contain: meaning, semantic, case_effect, syntax_role, murad, haqiqa/majaz
```

**Critical distinction:**
- `SurfaceEffect` in MufradProof = observable diacritics/signs (numerical)
- `CaseEffect` in Composition = grammatical judgment from operators (semantic)

## Implementation Checklist

See detailed specifications in: `PR8_HARDENING_REQUIREMENTS.md`

### 1. Core Interfaces (3 new frozen dataclasses)
- [ ] `PreSyntaxMufradVector` - typed, non-semantic export interface
- [ ] `CaseSignPotential` - original/substitute signs without case judgment
- [ ] `OperatorReadiness` - composition consumption contract

### 2. Case Sign Modeling
- [ ] Enum/constants for original signs (damma, fatha, kasra, sukun)
- [ ] Enum/constants for substitute signs (alif, waw, ya, nun variants, estimated)
- [ ] 5 new residual codes for unresolved case signs

### 3. Operator Registry Stub
- [ ] `NahwOperatorRegistryEntry` dataclass (source/school/rank/policy)
- [ ] Explicit `forbidden_in_mufrad: bool = True` flag
- [ ] No actual operator application logic

### 4. Composition Rules
- [ ] `composition_rank_ceiling()` helper (weakest-link rule)
- [ ] Explicit rejection of incomplete MufradProof
- [ ] Enhanced competitor resolution across all proof fields

### 5. Tests (20+ new tests required)
- [ ] `test_presyntax_vector_has_no_semantic_or_syntax_role_fields`
- [ ] `test_case_sign_potential_allowed_in_mufrad`
- [ ] `test_case_effect_still_forbidden_in_mufrad`
- [ ] `test_original_case_marks_are_surface_potentials_not_case_effects`
- [ ] `test_substitute_case_marks_are_surface_potentials_not_case_effects`
- [ ] `test_operator_readiness_requires_mufrad_proof`
- [ ] `test_operator_readiness_rejects_unresolved_competitors_for_certificate`
- [ ] `test_nahw_operator_registry_does_not_create_case_effect_inside_mufrad`
- [ ] `test_operator_rejects_mufrad_not_ready`
- [ ] `test_operator_rejects_mufrad_with_blockers`
- [ ] `test_unresolved_root_competition_blocks_certificate_readiness`
- [ ] `test_unresolved_case_sign_potential_blocks_certificate_readiness`
- [ ] `test_composition_rank_ceiling_uses_weakest_mufrad`
- [ ] All existing dal_core tests continue to pass

### 6. Documentation
- [ ] Add section: "Why MufradProof must close before nahw operators"
- [ ] Document distinction: D_mufrad (numerical basis) vs D_murakkab (composition)
- [ ] Update architecture diagrams if needed

## Acceptance Criteria

The follow-up PR must satisfy:

1. ✅ All CI checks pass
2. ✅ All existing dal_core tests pass
3. ✅ All new tests pass (20+ tests)
4. ✅ No semantic field leaks (`meaning`, `murad`, `haqiqa`, `majaz`)
5. ✅ No syntax role leaks (`faail`, `mafool`, `mubtada`, `khabar`)
6. ✅ No case effect leaks (`case_effect`, `marfoo_by`, `mansub_by`)
7. ✅ `PreSyntaxMufradVector` exists and is tested
8. ✅ `CaseSignPotential` exists and is tested
9. ✅ `OperatorReadiness` exists and is tested
10. ✅ Operator registry stub exists but does not apply syntax

## Final Claims (Post-Implementation)

**Allowed claim:**
```text
dal_core produces governed MufradProof ready to be consumed by future syntax
OperatorContracts, preserving morphology, surface effects, case sign potentials,
rank, residuals, trace, and competitors.
```

**Forbidden claims:**
```text
❌ dal_core performs syntax composition
❌ dal_core interprets grammatical meaning or murad
❌ MufradProof contains CaseEffect or SyntaxRole
```

## Related Work

- **Completed**: PR #8 - MufradProof base implementation
- **Next Phase**: العوامل النحوية المئة (100 grammar operators as ranked contracts)
- **Future**: Original/substitute case marks interpretation in composition layer

## الخلاصة بالعربية

PR #8 أسّس `MufradProof` كأساس رقمي. المرحلة القادمة تتطلب:

1. **PreSyntaxMufradVector**: واجهة مطبوعة بلا معنى دلالي
2. **CaseSignPotential**: العلامات الأصلية والفرعية كاحتماليات سطحية (ليست أحكام إعرابية)
3. **OperatorReadiness**: عقد الجاهزية للتركيب (بدون تطبيق عوامل نحوية)
4. تقوية معالجة المنافسين عبر كافة حقول البرهان
5. سجل مبدئي للعوامل النحوية (مصدر/مدرسة/رتبة) بدون تطبيق

**الهدف**: الجسر الضروري بين D_mufrad (المفرد) و D_murakkab (التركيب) بدون تسريب المعنى أو الدور النحوي.
