# DAL Core Backlog

**Created**: 2026-05-27 (Post PR-1C)
**Purpose**: Track identified gaps and future improvements

This document tracks known issues and improvements that were identified during implementation but deferred to maintain focused PR scope.

---

## Critical Gaps (Must Address Before U₁₁+)

### 1. Missing IDENTITY_DOMAIN in DomainType

**Status**: ✅ RESOLVED (PR-125)
**Impact**: HIGH
**Identified In**: PR-1B, PR-122
**Resolved In**: PR-125 (2026-05-27)

**Issue**:
- `DalTransitionDomain.IDENTITY_AXIS` has no corresponding `DomainType`
- Current mapping: `IDENTITY_AXIS → U5_FUNCTIONAL_ROLE, U6_MABNI_CLOSED_CLASS`
- Missing domain for Ism/Fi'l/Harf classification (DType)

**Resolution**:
```python
# In domain_registry.py, added:
IDENTITY_DOMAIN = auto()  # مجال محور الهوية (Ism/Fi'l/Harf)
```

**DomainSpec Added**:
- Arabic name: "مجال محور الهوية"
- Layer: DERIVATION_LAYER
- Competencies: ism_fil_harf_classification, functional_role_determination, mabni_closed_class_determination
- Prohibitions: syntactic_role, meaning, i3rab, case_assignment, semantic_interpretation
- Requires: WEIGHT_DOMAIN
- Allows transition to: WORDFORM_DOMAIN

**Mapping Updated**:
- `DAL_DOMAIN_TO_DOMAIN_TYPE_MAP[IDENTITY_AXIS]` now maps to `{IDENTITY_DOMAIN}`
- Removed GAP handling in `validate_dal_kernel_mapping()`

**Tests Added** (3 tests):
- `test_identity_axis_with_identity_domain_passes`
- `test_identity_axis_with_wrong_domain_fails`
- `test_identity_domain_exists_in_mapping`
- `test_identity_domain_exists_in_domain_registry`

---

### 2. Missing WORDFORM_DOMAIN for U₁₀

**Status**: ✅ RESOLVED (PR-125)
**Impact**: HIGH
**Identified In**: PR-1B, PR-122
**Resolved In**: PR-125 (2026-05-27)

**Issue**:
- U₁₀ WordFormCandidateCarrier has no specific `DomainType`
- Previously incorrectly mapped to `JUDGMENT_DOMAIN`
- U₁₀ is NOT judgment (no Ifādah, no Hukm)

**Resolution**:
```python
# In domain_registry.py, added:
WORDFORM_DOMAIN = auto()  # مجال صورة الكلمة المرشحة
```

**DomainSpec Added**:
- Arabic name: "مجال صورة الكلمة المرشحة"
- Layer: DERIVATION_LAYER
- Competencies: word_form_candidate, lexical_form_closed, word_contract_holder, jamid_mushtaq_classification, mabni_murab_classification
- Prohibitions: syntactic_role, meaning, i3rab_judgment, compositional_relation, ifadah, hukm
- Requires: IDENTITY_DOMAIN
- Allows transition to: SYNTAX_DOMAIN (U₁₀ → U₁₁ composition)

**Constitutional Clarification**:
- U₁₀ is a word CONTRACT/FORM holder, not a judgment
- No isolated word→meaning jump allowed (constitutional law)
- No Ifādah (no تمام الإفادة) at U₁₀
- Mapping to JUDGMENT_DOMAIN was architectural violation (now corrected)

**Tests Added** (1 test):
- `test_wordform_domain_exists_in_domain_registry`

**Priority**: ✅ COMPLETE

---

### 3. dal_contract without dal_domain Validation Gap

**Status**: ✅ RESOLVED (PR-124)
**Impact**: MEDIUM
**Identified In**: PR-122 review
**Resolved In**: PR-124 (2026-05-27)

**Issue**:
Current validator allows:
```python
dal_contract = Some_Contract  # Present
dal_domain = None             # Absent
dal_claim_scope = None        # Absent
```

This passes validation because:
```python
if dal_domain is None:
    return tuple(violations)  # Early return, no dal_contract check
```

**Resolution**:
```python
# In dal_kernel_validators.py, validate_dal_kernel_mapping():
# Before early return for dal_domain=None:
if dal_contract is not None and dal_domain is None:
    violations.append("dal_contract requires dal_domain")

if dal_contract is not None and dal_claim_scope is None:
    violations.append("dal_contract requires dal_claim_scope")
```

**Tests Added** (5 tests):
- `test_dal_contract_without_dal_domain_is_violation`
- `test_dal_contract_without_dal_claim_scope_is_violation`
- `test_dal_contract_without_both_domain_and_scope_has_two_violations`
- `test_approved_context_rejects_dal_contract_without_domain`
- `test_approved_context_rejects_dal_contract_without_claim_scope`

**Constitutional Law Enforced**:
- No contract without domain.
- No contract without claim scope.

---

### 4. U₁₀/JUDGMENT Ambiguity

**Status**: ✅ RESOLVED (PR-126)
**Impact**: MEDIUM
**Identified In**: PR-122 architectural review
**Resolved In**: PR-126 (2026-05-27)

**Issue**:
```python
# Old mapping in dal_kernel_validators.py (INCORRECT):
DalTransitionDomain.JUDGMENT: frozenset({
    ExecutionLayer.U7C_CLAUSE_SURFACE_AGREEMENT,
    ExecutionLayer.U10_WORD_FORM,  # ❌ U₁₀ is NOT judgment
})
```

But:
```python
# Mapping in domain_registry.py showed:
DalTransitionDomain.JUDGMENT → DomainType.JUDGMENT_DOMAIN
```

This created a contradiction:
- Execution map allowed JUDGMENT to reach U10_WORD_FORM
- Domain map said JUDGMENT = JUDGMENT_DOMAIN
- But U₁₀ should be WORDFORM_DOMAIN, not JUDGMENT_DOMAIN

**Constitutional Violation**:
- U₁₀ WordForm is NOT judgment (no Ifādah, no Hukm)
- Mixing U₁₀ with JUDGMENT violates: "WordForm is not Judgment" (لا صورة الكلمة حكمًا)

**Resolution (PR-126)**:
```python
# Added new DalTransitionDomain:
DalTransitionDomain.WORDFORM = auto()  # D7: صورة الكلمة - Word form candidate (U₁₀)

# Added new DalClaimScope:
DalClaimScope.WORDFORM_DETERMINED = auto()  # Word form candidate determined (U₁₀)

# Corrected execution mapping:
DalTransitionDomain.WORDFORM: frozenset({
    ExecutionLayer.U10_WORD_FORM,  # ✅ Correctly maps to U₁₀
})

DalTransitionDomain.JUDGMENT: frozenset({
    ExecutionLayer.U7C_CLAUSE_SURFACE_AGREEMENT,  # ✅ U₁₀ removed
})

# Added domain mapping:
DalTransitionDomain.WORDFORM: frozenset({
    DomainType.WORDFORM_DOMAIN,
})

# Added claim scope mapping:
DalTransitionDomain.WORDFORM: frozenset({
    DalClaimScope.WORDFORM_DETERMINED,
})
```

**Tests Added** (6 tests in PR-126):
- `test_wordform_domain_with_u10_passes`
- `test_u10_with_judgment_domain_fails`
- `test_judgment_domain_does_not_include_u10`
- `test_wordform_domain_maps_to_u10`
- `test_wordform_domain_maps_to_wordform_domain_type`
- `test_wordform_claim_scope_exists`

**Priority**: ✅ COMPLETE

---

## Future Architectural Improvements

### 5. ApprovedTransitionContext dal_contract Enforcement

**Status**: ✅ RESOLVED (PR-124)
**Impact**: LOW-MEDIUM
**Identified In**: PR-122 implementation
**Resolved In**: PR-124 (2026-05-27)

**Previous State**:
```python
# ApprovedTransitionContext.__post_init__() only checks if dal_domain OR dal_claim_scope present:
if self.audit.dal_domain is not None or self.audit.dal_claim_scope is not None:
    # validate
```

**Resolution**:
```python
# Now also triggers validation if dal_contract present alone:
if (self.audit.dal_domain is not None
    or self.audit.dal_claim_scope is not None
    or self.audit.dal_contract is not None):  # ✅ Added
    # validate
```

**Impact**:
- Previously: Unforgeable tokens could theoretically be created with dal_contract but no domain
- Now: Full validation enforced whenever dal_contract is present
- Combined with issue #3 fix, ensures complete dal_contract validation chain

**Tests**: Covered by PR-124 tests (see issue #3 above)

---

### 6. SlotGeometry Blocked Until AlgebraicFailure Proven

**Status**: BLOCKED
**Impact**: N/A (future feature)
**Identified In**: PR-1C planning

**Decision**:
- PR-1C implements hybrid failure semantics ONLY
- SlotGeometry deferred until:
  1. AlgebraicFailure proven in real usage
  2. Clear use cases identified
  3. Algebraic composition patterns established

**Reasoning**:
- Cannot design slot geometry without knowing failure patterns
- Must see how operations actually fail before designing failure geometry
- Premature architecture = technical debt

**Next Steps**:
1. Use AlgebraicFailure in actual operations (U₈→U₉, U₉→U₁₀, etc.)
2. Collect failure patterns
3. Design SlotGeometry based on evidence
4. Implement in separate PR

**Priority**: Not urgent - design phase required first

---

### 7. RelationClosure Blocked Until RelationAlgebraCore Strengthened

**Status**: BLOCKED
**Impact**: N/A (future feature)
**Identified In**: PR-120, U₁₁ planning

**Dependencies**:
- RelationAlgebraCore needs instance identity preservation (not just type)
- WEIGHT_IDENTITY algebra bug must be fixed (AND → ONE-OF logic)
- Typed loads instead of string loads
- U₁₁ canonical layer map resolution

**Blocking Issues** (from PR-120 analysis):
1. `anchor_id` missing (only `anchor_type` exists)
2. String loads instead of typed objects
3. WEIGHT_IDENTITY requires BOTH root AND stem (should be ONE-OF)
4. U₁₁ ExecutionLayer canonical map undefined

**Next Steps**:
1. Implement PR-120 (Post-Relation Algebra Reconciliation)
2. Fix WEIGHT_IDENTITY logic
3. Add instance identity preservation
4. THEN design RelationClosure

**Priority**: High for U₁₁, but PR-120 must come first

---

### 8. Ifādah Layer Blocked Until RelationClosure

**Status**: BLOCKED
**Impact**: N/A (future feature)
**Identified In**: Composition architecture planning

**Constitutional Law**:
```
لا حكم بلا إفادة ودليل
No Hukm without Ifādah and evidence
```

**Dependencies**:
1. RelationClosure must exist (U₁₂)
2. Relation → Ifādah boundary must be clear
3. Ifādah completion point (تمام الإفادة) must be formal
4. Backward scanning from completion point must be implemented

**Architecture Order**:
```
U₁₁ (RelationComposition)
  → U₁₂ (RelationClosure/Ifādah)
  → U₁₃ (Hukm)
```

**Priority**: Low - distant future, clear blocking chain

---

## Testing Improvements

### 9. AlgebraicFailure Integration Tests

**Status**: PENDING
**Impact**: MEDIUM
**Identified In**: PR-1C implementation

**Current**:
- 18 unit tests for AlgebraicFailure construction and properties
- NO integration tests with actual operations

**Required**:
1. Test real operation returning AlgebraicFailure
2. Test composition with AlgebraicFailure propagation
3. Test AlgebraicFailure → Exception boundary (when to convert)
4. Test AlgebraicFailure in AlgebraicDecisionCore

**Example Test Cases Needed**:
```python
def test_operation_returns_algebraic_failure_not_exception():
    """Operation failure returns AlgebraicFailure, not exception."""
    # Test that gate non-satisfaction returns AlgebraicFailure
    result = some_operation(input_that_fails_gate)
    assert isinstance(result, AlgebraicFailure)
    assert result.gate == "expected_gate"

def test_construction_failure_raises_exception():
    """Construction invariant violation raises exception."""
    with pytest.raises(ValueError):
        InvalidObject(impossible_invariant=True)
```

**Priority**: High - should be added in next PR that uses AlgebraicFailure

---

### 10. dal_kernel Validator Edge Case Tests

**Status**: GOOD COVERAGE, MINOR GAPS
**Impact**: LOW
**Identified In**: PR-122 test suite

**Current Coverage**: 22/22 tests passing

**Missing Edge Cases**:
1. dal_contract with dal_domain=None (gap #3)
2. dal_contract with dal_claim_scope=None (gap #3)
3. Multiple simultaneous violations (priority testing)
4. ApprovedTransitionContext with dal_contract only (gap #5)

**Priority**: Low - add when fixing gaps #3, #5

---

## Documentation Gaps

### 11. Hybrid Failure Semantics Usage Guide

**Status**: MISSING
**Impact**: MEDIUM
**Identified In**: PR-1C

**Required**:
- Practical guide: "When to use AlgebraicFailure vs Exception"
- Examples from real operations
- Pattern catalog for common failures
- Integration with CPBStatus

**Content Needed**:
1. Decision tree: Exception or AlgebraicFailure?
2. Code examples from actual layers
3. Anti-patterns to avoid
4. Composition patterns

**Priority**: Medium - should be added after first real usage

---

### 12. dal_algebra Mathematical Specification

**Status**: INFORMAL
**Impact**: MEDIUM
**Identified In**: General architecture

**Current**:
- Module docstring mentions math: `Opₑ : A → Success[B] ∪ AlgebraicFailure`
- No formal specification document

**Required**:
```markdown
# DAL_ALGEBRA_FORMAL_SPEC.md

## Type System
- 𝔾 = successful typed objects
- Failure ∉ 𝔾
- Operations: Opₑ : 𝔾ᵢ × Aux → CandidateSet[𝔾ⱼ] ∪ AlgebraicFailure

## Laws
1. Construction Safety: ∀ obj ∈ 𝔾, invariants(obj) = True
2. Algebraic Closure: ∀ op, input ∈ 𝔾 → (output ∈ 𝔾 ∨ output ∈ AlgebraicFailure)
3. No Silent None: output ≠ None
4. Exception Boundary: Exceptions ONLY for construction, not operations

## Composition
- Sequential: op₂(op₁(x)) with failure propagation
- Parallel: [op₁(x), op₂(x)] with failure collection
- Conditional: if success(op₁(x)) then op₂(x) else handle_failure
```

**Priority**: Medium - important for maintainability

---

## Version History

- **2026-05-27 (PR-125)**: Items #1 and #2 resolved
  - Added IDENTITY_DOMAIN to DomainType and DomainRegistry
  - Added WORDFORM_DOMAIN to DomainType and DomainRegistry
  - Updated DAL_DOMAIN_TO_DOMAIN_TYPE_MAP: IDENTITY_AXIS → IDENTITY_DOMAIN
  - Removed GAP handling for IDENTITY_AXIS in dal_kernel_validators
  - Added 5 new tests for IDENTITY_DOMAIN and WORDFORM_DOMAIN
  - Clarified U₁₀ as word contract/form holder, NOT judgment
  - Constitutional law enforced: "No isolated word→meaning jump without compositional relation"

- **2026-05-27 (PR-124)**: Items #3 and #5 resolved
  - Tightened dal_contract validation
  - Added 5 new tests for dal_contract without dal_domain/dal_claim_scope
  - ApprovedTransitionContext now triggers validation for dal_contract
  - Constitutional law enforced: "No contract without domain. No contract without claim scope."

- **2026-05-27**: Initial BACKLOG created (Post PR-1C)
  - 12 items identified
  - 4 critical gaps (must fix before U₁₁)
  - 4 architectural improvements (future features)
  - 2 testing improvements
  - 2 documentation gaps

---

## Usage Notes

**How to use this backlog**:
1. Critical gaps (#1-4): Must be fixed in specific order before advancing
2. Architectural improvements (#5-8): Design when dependencies clear
3. Testing improvements (#9-10): Add as features are used
4. Documentation gaps (#11-12): Fill after real usage patterns emerge

**PR Planning**:
- Small validator fix PR: Items #3, #5, #10
- Domain extension PR: Items #1, #2, #4
- Testing PR: Items #9, #10
- Documentation PR: Items #11, #12
- Architecture PRs: Items #6, #7, #8 (in order, much later)

**Constitutional Compliance**:
All items respect:
- لا metadata غير محكومة (No ungoverned metadata)
- لا حكم بلا إفادة ودليل (No judgment without Ifādah and evidence)
- Construction safety ≠ Operation safety (Hybrid failure semantics)

---

**Last Updated**: 2026-05-27
**Status**: Living document - update as gaps identified/resolved
