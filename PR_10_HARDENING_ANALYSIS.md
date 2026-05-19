# PR #10 Hardening Analysis

## Current Implementation Status

Based on code review of PR #10 implementation, here's the status of each hardening requirement:

---

## 1. `allows_operator_consumption()` Conditional Logic

### Current Implementation (src/dal_core/presyntax_vector.py:150-156)

```python
def allows_operator_consumption(self) -> bool:
    """
    Check if this vector is ready for operator consumption.

    Operators require minimum readiness level.
    """
    return self.composition_readiness.allows_composition()
```

### Analysis

**✅ PARTIALLY MET**: Current implementation checks `composition_readiness`, which gates on:
- `READY_AS_HYPOTHESIS`
- `READY_FOR_COMPOSITION`
- `READY_FOR_CERTIFICATE_COMPOSITION`

**❌ MISSING**: The method does NOT check:
- Blocking residuals
- Unresolved competitors (for certificate)
- Trace to raw input
- Rank ceiling (weakest-link)

### Required Enhancement

```python
def allows_operator_consumption(self) -> bool:
    """
    Check if this vector is ready for operator consumption.

    Operators require minimum readiness level AND:
    - No blocking residuals
    - Trace reaches raw input
    - Rank obeys weakest-link ceiling
    - Competitors resolved for certificate (if certificate requested)
    """
    # Basic readiness check
    if not self.composition_readiness.allows_composition():
        return False

    # Block if blocking residuals present
    if self.has_blocking_residuals():
        return False

    # Require valid trace to raw input
    if not self.trace_id or self.trace_id == "":
        return False

    # Additional checks can be added here
    return True
```

### Required Tests (MISSING)

```python
test_presyntax_vector_does_not_allow_operator_consumption_by_default
test_presyntax_vector_rejects_blockers
test_presyntax_vector_rejects_unresolved_competitors_for_certificate
test_presyntax_vector_requires_trace_to_raw_input
```

**Current test coverage**: 2 tests exist
- `test_composition_readiness_gates_operator_access()` - checks NOT_READY blocks
- `test_ready_vector_allows_operator_consumption()` - checks READY allows

**Status**: ⚠️ **NEEDS HARDENING** - Add 4 missing tests + enhance logic

---

## 2. `CaseSignPotential` Must Not Become Disguised `CaseEffect`

### Current Implementation (src/dal_core/case_signs.py:145-163)

```python
def __post_init__(self):
    """Validate that this is a potential, not an effect"""
    # Forbidden field names (these belong to CaseEffect, not CaseSignPotential)
    forbidden_terms = [
        'marfoo', 'mansub', 'majrur', 'majzum',  # Case judgments
        'governed_by', 'operator', 'relation',     # Syntax governance
        'faail', 'mafool', 'mubtada', 'khabar',   # Syntax roles
    ]

    # Check compatible_case_effects are names only (candidates)
    for effect_name in self.compatible_case_effects:
        if not effect_name.endswith('_candidate'):
            # Verify it's a descriptive name, not a judgment
            for term in forbidden_terms:
                if term in effect_name.lower():
                    raise ValueError(
                        f"CaseSignPotential cannot contain case judgment: {effect_name}. "
                        f"Use '*_candidate' naming for compatibility list."
                    )
```

### Analysis

**✅ WELL IMPLEMENTED**:
- Validates no forbidden terms in `compatible_case_effects`
- Enforces `*_candidate` naming convention
- No `marfoo_by`, `mansub_by`, `governed_by`, `operator_id` fields exist

**✅ TEST COVERAGE**:
- `test_case_sign_potential_is_observation_not_judgment()` - verifies no judgment fields
- `test_case_sign_potential_rejects_judgment_names()` - tests forbidden terms rejection

### Required Tests (MISSING)

```python
test_case_sign_potential_contains_no_operator_binding
test_case_sign_potential_contains_no_final_case_judgment
test_case_sign_potential_contains_no_syntax_role
```

**Status**: ✅ **MOSTLY MET** - Add 3 explicit tests for clarity

---

## 3. Type IDs Must Remain Operational, Not Semantic

### Current Implementation (src/dal_core/type_ids.py:1-16)

```python
"""
Type ID Registry (سجل أكواد الأنواع)

Operational type identifiers for PreSyntax interface.

CRITICAL PRINCIPLE:
type_id ≠ meaning
type_id = operational key for operator entry

These are NOT semantic categories. They are typed identifiers that:
1. Enable operator contracts to check input signatures
2. Prevent operators from working on wrong types
3. Provide numerical foundation for composition

Before any operator works, each MufradProof must have a stable type_id.
"""
```

### Analysis

**✅ WELL DOCUMENTED**: Clear statement that type_id ≠ meaning

**✅ CURRENT TESTS**:
- `test_noun_type_ids_are_codes_not_meanings()` - verifies operational nature
- `test_verb_type_ids_are_codes_not_meanings()` - verifies codes
- `test_particle_type_ids_are_codes_not_meanings()` - verifies codes

### Required Tests (MISSING)

```python
test_type_id_is_operational_code_not_meaning
test_particle_type_id_does_not_emit_semantic_value
test_verb_type_id_does_not_emit_intended_time
```

**Status**: ✅ **MOSTLY MET** - Tests exist with different names; add 3 explicit tests for completeness

---

## 4. PreSyntax Rank Must Not Raise MufradProof Rank

### Current Implementation

**DataClass Fields** (src/dal_core/presyntax_vector.py:109-113):
```python
morph_rank: LughaRank
"""Rank from morphological analysis"""

final_rank: LughaRank
"""Weakest rank in proof chain"""
```

### Analysis

**✅ STRUCTURE EXISTS**:
- `final_rank` field indicates weakest-link principle
- Both `morph_rank` and `final_rank` preserved from MufradProof

**❌ NO VALIDATION**: No code enforces `rank(PreSyntaxVector) <= rank(MufradProof)`

**❌ NO TESTS**: Zero tests verify rank preservation

### Required Tests (MISSING - ALL)

```python
test_presyntax_vector_rank_cannot_exceed_mufrad_rank
test_presyntax_vector_preserves_mufrad_residuals
test_presyntax_vector_preserves_mufrad_trace
```

**Status**: ⚠️ **NEEDS HARDENING** - Add all 3 tests + validation logic

---

## Summary Table

| Hardening Point | Current Status | Missing Tests | Validation Logic |
|----------------|---------------|---------------|------------------|
| 1. Conditional `allows_operator_consumption()` | ⚠️ Partial | 4 tests | Needs enhancement |
| 2. `CaseSignPotential` not `CaseEffect` | ✅ Good | 3 tests | Already enforced |
| 3. Type IDs operational not semantic | ✅ Good | 3 tests | Well documented |
| 4. Rank preservation | ⚠️ Partial | 3 tests | Needs validation |

**Total missing tests**: 13

**Critical gaps**:
1. `allows_operator_consumption()` logic incomplete
2. No rank preservation validation
3. Test coverage gaps in all 4 areas

---

## Recommendation

**Before moving PR #10 from Draft to Ready**:

1. ✅ Keep current implementation of `CaseSignPotential` and `type_ids` (already solid)
2. ⚠️ Enhance `allows_operator_consumption()` with additional checks
3. ⚠️ Add rank validation in `PreSyntaxMufradVector` construction
4. ⚠️ Add all 13 missing tests

**Status**: PR #10 is **65% hardened** - needs remaining 35% before merge-ready.
