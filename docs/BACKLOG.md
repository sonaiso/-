# DAL Core Backlog

**Created**: 2026-05-27 (Post PR-1C)
**Purpose**: Track identified gaps and future improvements

This document tracks known issues and improvements that were identified during implementation but deferred to maintain focused PR scope.

---

## Critical Gaps (Must Address Before U₁₁+)

### 1. Missing IDENTITY_DOMAIN in DomainType

**Status**: GAP
**Impact**: HIGH
**Identified In**: PR-1B, PR-122

**Issue**:
- `DalTransitionDomain.IDENTITY_AXIS` has no corresponding `DomainType`
- Current mapping: `IDENTITY_AXIS → U5_FUNCTIONAL_ROLE, U6_MABNI_CLOSED_CLASS`
- Missing domain for Ism/Fi'l/Harf classification (DType)

**Required Action**:
```python
# In domain_registry.py, add:
IDENTITY_DOMAIN = "identity_domain"  # محور الهوية (Ism/Fi'l/Harf)
```

**Blocking**:
- Full dal_kernel validation for U₅-U₆ transitions
- DType → DMufrad architectural clarity

**Priority**: Must fix before U₁₁ implementation

---

### 2. Missing WORDFORM_DOMAIN for U₁₀

**Status**: GAP
**Impact**: HIGH
**Identified In**: PR-1B, PR-122

**Issue**:
- U₁₀ WordFormCandidateCarrier has no specific `DomainType`
- Currently incorrectly mapped to `JUDGMENT_DOMAIN`
- U₁₀ is NOT judgment (no Ifādah, no Hukm)

**Required Action**:
```python
# In domain_registry.py, add:
WORDFORM_DOMAIN = "wordform_domain"  # صورة الكلمة المرشحة
# OR
LEXICAL_FORM_DOMAIN = "lexical_form_domain"  # الصيغة المعجمية المغلقة
```

**Constitutional Issue**:
- U₁₀ is a word CONTRACT/FORM holder, not a judgment
- Mapping to JUDGMENT_DOMAIN violates architectural separation
- Must be corrected before claiming U₁₀ constitutional completion

**Priority**: Must fix in next architecture cleanup PR

---

### 3. dal_contract without dal_domain Validation Gap

**Status**: MINOR GAP
**Impact**: MEDIUM
**Identified In**: PR-122 review

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

**Required Action**:
```python
# In dal_kernel_validators.py, validate_dal_kernel_mapping():
# Before early return for dal_domain=None:
if dal_contract is not None and dal_domain is None:
    violations.append("dal_contract requires dal_domain")

if dal_contract is not None and dal_claim_scope is None:
    violations.append("dal_contract requires dal_claim_scope")
```

**Impact**:
- Currently low (dal_contract rarely used without dal_domain)
- Could cause inconsistency if contract used standalone

**Priority**: Add in next validator tightening PR

---

### 4. U₁₀/JUDGMENT Ambiguity

**Status**: DESIGN INCONSISTENCY
**Impact**: MEDIUM
**Identified In**: PR-122 architectural review

**Issue**:
```python
# Current mapping in dal_kernel_validators.py:
DalTransitionDomain.JUDGMENT: frozenset({
    ExecutionLayer.U7C_CLAUSE_SURFACE_AGREEMENT,
    ExecutionLayer.U10_WORD_FORM,  # ❌ U₁₀ is NOT judgment
})
```

But:
```python
# DomainType mapping:
DalTransitionDomain.JUDGMENT: frozenset({
    DomainType.JUDGMENT_DOMAIN,  # Correct for U₇-C
})
```

**Contradiction**:
- ExecutionLayer mapping includes U₁₀
- DomainType mapping excludes U₁₀ (correctly)
- U₁₀ documented as "NOT final judgment"

**Resolution** (once WORDFORM_DOMAIN exists):
```python
# Remove U10_WORD_FORM from JUDGMENT domain:
DalTransitionDomain.JUDGMENT: frozenset({
    ExecutionLayer.U7C_CLAUSE_SURFACE_AGREEMENT,
    # U10_WORD_FORM removed - moved to WORDFORM domain
})

# Add new domain for U₁₀:
DalTransitionDomain.WORDFORM: frozenset({
    ExecutionLayer.U10_WORD_FORM,
})
```

**Priority**: Fix when adding WORDFORM_DOMAIN

---

## Future Architectural Improvements

### 5. ApprovedTransitionContext dal_contract Enforcement

**Status**: PARTIAL ENFORCEMENT
**Impact**: LOW-MEDIUM
**Identified In**: PR-122 implementation

**Current**:
```python
# ApprovedTransitionContext.__post_init__() only checks if dal_domain OR dal_claim_scope present:
if self.audit.dal_domain is not None or self.audit.dal_claim_scope is not None:
    # validate
```

**Missing**:
```python
# Should also trigger validation if dal_contract present alone:
if (self.audit.dal_domain is not None
    or self.audit.dal_claim_scope is not None
    or self.audit.dal_contract is not None):  # ← Add this
    # validate
```

**Impact**:
- Unforgeable tokens could theoretically be created with dal_contract but no domain
- Low risk if dal_contract validation (issue #3 above) is fixed first

**Priority**: Address after fixing issue #3

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
