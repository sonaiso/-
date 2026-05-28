# Operation Algebra Constitution
## دستور جبر العمليات

**Document Type**: Constitutional Foundation
**Status**: Theoretical Specification (PR #133)
**Version**: 1.0.0
**Date**: 2026-05-28
**Depends On**: PR #132 (Slot Geometry Algebra)

---

## Executive Summary | الملخص التنفيذي

**الأصل الجبري الثاني:**

> لا جبر خانات بلا جبر عمليات.
> ولا عملية بلا علة.
> ولا رجوع يقيني بلا أثر.

**The Second Algebraic Principle:**

> No slot algebra without operation algebra.
> No operation without cause.
> No certain reversal without trace.

---

## 1. Foundational Definitions | التعريفات الأساسية

### 1.1 The Operation (العملية)

```
Operation = تحول مرخّص من حالة قبل إلى حالة بعد مع علة وأثر
```

**Definition**: Licensed transformation from before-state to after-state with cause and trace.

**Properties**:
- **Declared before/after relation** (not implicit)
- **Cause geometry** (why the operation is licensed)
- **Trace generation** (how to recover preimage)
- **Invariant preservation** (what must not change)
- **Residual tracking** (what remains unresolved)
- **Rank assignment** (epistemic certainty level)

---

### 1.2 The Cause Geometry (هندسة العلة)

```
CauseGeometry = PriorInfo + Bāb + Domain + MaterialCause + FormalCause + EfficientCause + FinalCauseBeforeMeaning
```

**Definition**: Geometric representation of why an operation is licensed.

**Four Causes** (الأسباب الأربعة):
1. **Material Cause** (العلة المادية): What undergoes transformation
2. **Formal Cause** (العلة الصورية): The pattern/structure being imposed
3. **Efficient Cause** (العلة الفاعلية): The licensing condition
4. **Final Cause** (العلة الغائية): The purpose (BEFORE meaning)

**Critical Law**:
```
No operation without complete cause geometry.
Incomplete cause → residual + lowered rank.
```

---

### 1.3 The Trace (الأثر)

```
Trace = سجل محفوظ للانتقال من قبل إلى بعد
```

**Definition**: Preserved record of the transition from before to after.

**Properties**:
- **Complete**: All information needed for reversal
- **Incomplete**: Partial information, reversal uncertain
- **Injective operations**: Trace may be minimal (operation itself preserves info)
- **Non-injective operations**: Trace must carry lost preimage information

---

### 1.4 The Backward Audit (التدقيق العكسي)

```
BackwardAudit(after, trace) → before | RecoveredCandidate + Residual
```

**Definition**: Validation that after-state + trace can recover before-state within domain.

**Two Modes**:
1. **Certain recovery**: When trace is complete and operation injective (or trace carries preimage)
2. **Candidate recovery**: When trace incomplete → candidates + residuals + lowered rank

---

## 2. The Constitutional Pipeline | المسار الدستوري

### 2.1 The Complete Operation Path

```
Before
  + PriorInfo
  + Bāb
  + Domain
  + CauseGeometry
  + LicensedOperation
  →
After
  + Invariant
  + Trace
  + Residual
  + Rank
  + STOP before meaning
```

### 2.2 The Forbidden Paths

```
Operation → Meaning                    ❌ FORBIDDEN
Operation → Ifadah                     ❌ FORBIDDEN
Operation → Hukm                       ❌ FORBIDDEN
Operation → RelationCandidate          ❌ FORBIDDEN (too early)
Operation without CauseGeometry        ❌ FORBIDDEN
Operation without BeforeAfterRelation  ❌ FORBIDDEN
TraceInverse → Certainty without conditions ❌ FORBIDDEN
```

---

## 3. Core Constructs | البنى الأساسية

### 3.1 OperationSpec

```python
@dataclass(frozen=True)
class OperationSpec:
    """
    Complete specification of a licensed operation.

    Constitutional Law:
        Every operation MUST declare:
        1. Before/after relation
        2. Complete cause geometry
        3. Trace policy
        4. Invariant preservation
        5. Residual handling
        6. Rank assignment
        7. Meaning prohibition
    """
    name: str
    domain_before: str
    domain_after: str
    input_type: type
    output_type: type
    required_prior_info: FrozenSet[str]
    bāb: str  # Morphological gate/door
    cause_geometry: 'CauseGeometry'
    licensed_operation: Callable
    declared_before_after_relation: 'BeforeAfterRelation'
    preserved_invariant: str
    changed_component: str
    trace_policy: 'TracePolicy'
    residual_policy: 'ResidualPolicy'
    rank_policy: 'RankPolicy'
    surface_inverse_policy: 'SurfaceInversePolicy'
    trace_inverse_policy: 'TraceInversePolicy'
    forbidden_outputs: FrozenSet[str]  # Must include: meaning, ifadah, hukm
    next_allowed_operations: FrozenSet[str]
    stop_before_meaning: bool = True  # Always True
```

### 3.2 CauseGeometry

```python
@dataclass(frozen=True)
class CauseGeometry:
    """
    Complete geometric representation of operation causation.

    Constitutional Law:
        Cause geometry MUST include all four causes.
        Final cause MUST stop before meaning.
    """
    prior_info: FrozenSet[str]
    bāb: str  # ‫باب - morphological door
    domain: str
    material_cause: str  # What undergoes transformation
    formal_cause: str  # Pattern/structure imposed
    efficient_cause: str  # Licensing condition
    final_cause_before_meaning: str  # Purpose (pre-semantic)
    license: 'LicenseSpec'
    invariant: str
    trace_requirement: 'TraceRequirement'
    residual_handling: str
    rank_assignment: 'Rank'
    stop_before_meaning: bool = True
```

### 3.3 OperationTrace

```python
@dataclass(frozen=True)
class OperationTrace:
    """
    Trace of operation execution.

    Constitutional Law:
        Trace completeness determines recovery certainty.
    """
    operation_name: str
    before_identity: str
    after_identity: str
    preserved_invariant: str
    changed_components: Tuple[str, ...]
    trace_data: Mapping[str, Any]  # Preserved preimage info
    is_complete: bool
    is_injective_operation: bool
    carries_preimage: bool  # For non-injective operations
    residuals_at_operation: FrozenSet['Residual']
    rank_at_operation: 'Rank'
```

### 3.4 SurfaceInverse

```python
@dataclass(frozen=True)
class SurfaceInverse:
    """
    Surface-level inversion (hypothetical, probabilistic).

    Constitutional Law:
        SurfaceInverse NEVER returns certainty.
        Always returns candidates with residuals.
    """
    surface_after: Any
    recovered_candidates: Tuple[Any, ...]  # Multiple possibilities
    residuals: FrozenSet['Residual']
    rank: 'Rank'  # Always ≤ STRONG_HYPOTHESIS
    certainty: bool = False  # Always False
```

### 3.5 TraceInverse

```python
@dataclass(frozen=True)
class TraceInverse:
    """
    Trace-based inversion (certain under conditions).

    Constitutional Law:
        TraceInverse is certain within declared domain when EITHER:
        1. Operation is injective on that domain, OR
        2. Trace carries sufficient preserved preimage information.

        Otherwise returns candidates with residuals and lowered rank.
    """
    after_state: Any
    trace: 'OperationTrace'
    domain: str
    recovered_before: Optional[Any]  # Certain recovery
    alternative_candidates: Tuple[Any, ...]  # Uncertain recovery
    residuals: FrozenSet['Residual']
    rank: 'Rank'
    is_certain: bool  # True only when conditions met
    certainty_basis: str  # "injective" or "trace_carries_preimage"
```

### 3.6 BackwardAudit

```python
@dataclass(frozen=True)
class BackwardAudit:
    """
    Validates backward recovery from after-state + trace.

    Constitutional Law:
        BackwardAudit MUST verify:
        1. Trace completeness
        2. Invariant preservation
        3. Domain membership
        4. No meaning production
    """
    after_state: Any
    trace: 'OperationTrace'
    attempted_recovery: Any
    audit_result: 'AuditResult'
    verified_invariant: bool
    verified_domain: bool
    verified_trace_complete: bool
    verified_no_meaning: bool
    residuals: FrozenSet['Residual']
    rank: 'Rank'
```

---

## 4. Policies | السياسات

### 4.1 InvariantPolicy

```python
@dataclass(frozen=True)
class InvariantPolicy:
    """What MUST NOT change during operation."""
    preserved_identity: str
    preserved_features: FrozenSet[str]
    forbidden_changes: FrozenSet[str]
    violation_handling: str  # "block" or "residual"
```

### 4.2 ResidualPolicy

```python
@dataclass(frozen=True)
class ResidualPolicy:
    """What remains unresolved after operation."""
    inherited_residuals: FrozenSet['Residual']
    operation_residuals: FrozenSet['Residual']
    discharge_conditions: Mapping[str, str]
    blocking_residuals: FrozenSet['Residual']
```

### 4.3 RankPolicy

```python
@dataclass(frozen=True)
class RankPolicy:
    """Epistemic rank assignment for operation output."""
    input_rank_requirement: 'Rank'
    output_rank: 'Rank'
    rank_lowering_conditions: Mapping[str, 'Rank']
    certification_prohibited: bool = True  # Operations never produce CERTIFICATE
```

### 4.4 TracePolicy

```python
@dataclass(frozen=True)
class TracePolicy:
    """How trace is generated and used."""
    required_completeness: bool
    preserved_preimage_fields: FrozenSet[str]
    injective_operation: bool
    inverse_certainty_conditions: Tuple[str, ...]
```

---

## 5. Constitutional Laws | القوانين الدستورية

### Law 1: Operation Requires Complete Specification

```
∀ operation:
  operation exists
  ⇒ ∃ OperationSpec with all required fields
```

**Enforcement**: `ValueError` if any required field missing.

---

### Law 2: Operation Requires Before/After Relation

```
∀ operation:
  operation exists
  ⇒ ∃ BeforeAfterRelation declared explicitly
```

**Reason**: No implicit transformations.

---

### Law 3: Operation Requires Complete CauseGeometry

```
∀ operation:
  operation exists
  ⇒ ∃ CauseGeometry with all four causes
```

**Enforcement**: `ValueError` if any cause missing.

---

### Law 4: No CauseGeometry Without Bāb and Domain

```
∀ cause_geometry:
  cause_geometry exists
  ⇒ bāb ≠ "" ∧ domain ≠ ""
```

---

### Law 5: SurfaceInverse Never Returns Certainty

```
∀ surface_inverse:
  surface_inverse.certainty = False
  ∧ surface_inverse.rank ≤ STRONG_HYPOTHESIS
```

---

### Law 6: TraceInverse Certainty Requires Conditions

```
∀ trace_inverse:
  trace_inverse.is_certain = True
  ⇒ (trace.is_complete = True
     ∧ (trace.is_injective_operation = True
        ∨ trace.carries_preimage = True))
```

---

### Law 7: Incomplete Trace → Lowered Rank

```
∀ trace_inverse:
  trace.is_complete = False
  ⇒ (trace_inverse.rank ≤ HYPOTHESIS
     ∧ trace_inverse.residuals ≠ ∅)
```

---

### Law 8: Operations Stop Before Meaning

```
∀ operation_output:
  operation_output MUST NOT contain:
    - meaning field
    - ifadah field
    - hukm field
    - semantic_identity
```

**Enforcement**: `ValueError` on meaning production.

---

### Law 9: BackwardAudit Validates Domain

```
∀ backward_audit:
  backward_audit.verified_domain = True
  ⇔ (attempted_recovery ∈ domain_before)
```

---

### Law 10: Trace Does Not Imply Meaning

```
∀ trace:
  trace.trace_data MUST NOT contain semantic information
```

**Enforcement**: Constitutional test.

---

## 6. Critical Distinctions | الفروق الحرجة

### 6.1 SurfaceInverse vs TraceInverse

| Aspect | SurfaceInverse | TraceInverse |
|--------|----------------|--------------|
| **Certainty** | Never certain (ظني) | Certain under conditions (يقيني في المجال) |
| **Input** | After-state only | After-state + Trace |
| **Output** | Multiple candidates | Single recovery or candidates |
| **Rank** | ≤ STRONG_HYPOTHESIS | Can be STRONG_HYPOTHESIS if certain |
| **Residuals** | Always present | May be empty if certain |
| **Use case** | Hypothetical reconstruction | Verified backward audit |

### 6.2 Complete vs Incomplete Trace

| Property | Complete Trace | Incomplete Trace |
|----------|----------------|------------------|
| **Recovery** | Certain (if injective or carries preimage) | Candidates only |
| **Rank** | STRONG_HYPOTHESIS | ≤ HYPOTHESIS |
| **Residuals** | May be empty | Always present |
| **Audit** | Passes verification | Fails certainty verification |

### 6.3 Injective vs Non-Injective Operations

| Type | Trace Requirement | Recovery |
|------|-------------------|----------|
| **Injective** | Minimal (operation preserves info) | Certain within domain |
| **Non-injective** | Must carry preimage | Certain only if trace carries preimage |

**Examples**:
- **Injective**: Adding diacritics (reversible by removal)
- **Non-injective**: حذف (deletion), إدغام (assimilation), إعلال (vowel change), إبدال (substitution)

---

## 7. Integration with PR #132 | الاندماج مع PR #132

### PR #132 Established

```
Carrier → SlotGeometry → VerbalSignifiedCandidate → STOP before meaning
```

**15 Verbal Signified Families** (slot geometry effects, not meanings)

### PR #133 Completes

```
SlotGeometry + OperationAlgebra = Complete Pre-Meaning Foundation
```

**Every slot transformation now carries**:
- **Cause**: Why licensed (CauseGeometry)
- **Trace**: How to reverse (OperationTrace)
- **Residual**: What remains unresolved (ResidualPolicy)
- **Rank**: Epistemic certainty (RankPolicy)
- **Audit**: Backward verification (BackwardAudit)

---

## 8. What This PR Does NOT Include | ما لا يشمله هذا PR

**Out of Scope** (comes later):
- ❌ RelationAlgebraCore expansion
- ❌ Ifadah logic
- ❌ Hukm logic
- ❌ Meaning interpretation
- ❌ T5 model code
- ❌ Dataset generation

**Reason**: Operation Algebra is foundational. Relations, meanings, and models build ON TOP of it.

---

## 9. Success Criteria | معايير النجاح

### Constitutional Tests Required

1. ✅ Operation cannot exist without OperationSpec
2. ✅ Operation cannot exist without BeforeAfterRelation
3. ✅ Operation cannot exist without CauseGeometry
4. ✅ CauseGeometry cannot exist without Bāb and Domain
5. ✅ SurfaceInverse never returns certainty
6. ✅ TraceInverse cannot return certainty without complete trace
7. ✅ TraceInverse returns certainty when conditions met (injective or carries preimage)
8. ✅ TraceInverse lowers rank when trace incomplete
9. ✅ Trace does not contain meaning
10. ✅ Operation does not produce RelationCandidate, Ifadah, Hukm, Meaning
11. ✅ BackwardAudit verifies domain membership
12. ✅ PR #132 SlotGeometry boundaries remain intact

---

## 10. The Master Equation | المعادلة الرئيسية

```
Before
  + PriorInfo       (ما سبق معرفته)
  + Bāb             (الباب الصرفي)
  + Domain          (المجال)
  + CauseGeometry   (هندسة العلة)
  + LicensedOperation (العملية المرخصة)
  =
After
  + Invariant       (الثابت المحفوظ)
  + Trace           (الأثر)
  + Residual        (البقايا)
  + Rank            (الرتبة)
  + STOP before meaning (توقف قبل المعنى)
```

---

## Appendix A: BeforeAfterRelation

```python
@dataclass(frozen=True)
class BeforeAfterRelation:
    """
    Explicit declaration of before/after relation.

    Constitutional Law:
        No implicit transformations.
        Every operation MUST declare what changes and what persists.
    """
    operation_name: str
    before_type: type
    after_type: type
    identity_preservation: str  # How identity is preserved
    change_description: str  # What changes
    reversibility: bool  # Is operation reversible?
    trace_requirement: str  # What trace must capture
```

---

## Appendix B: MeaningStopGate

```python
@dataclass(frozen=True)
class MeaningStopGate:
    """
    Constitutional gate preventing meaning production.

    Usage:
        Applied to all operation outputs.
        Raises ValueError if meaning detected.
    """
    forbidden_fields: FrozenSet[str] = frozenset([
        "meaning", "murad", "haqiqa_majaz",
        "semantic_identity", "ifadah_identity",
        "hukm_identity", "final_meaning"
    ])

    def validate(self, output: Any) -> None:
        """Raise ValueError if output contains forbidden fields."""
        for field in self.forbidden_fields:
            if hasattr(output, field):
                raise ValueError(
                    f"Operation output MUST NOT contain '{field}'. "
                    f"Operations stop before meaning. "
                    f"Violation of Operation Algebra Constitution Law #8."
                )
```

---

**End of Constitution** | نهاية الدستور

This constitution establishes the complete algebraic foundation for operations, enabling:
1. Rigorous cause-effect reasoning
2. Certified backward audit
3. Explicit trace-based recovery
4. Principled residual handling
5. Epistemic rank tracking
6. Constitutional meaning prohibition

**After PR #133**: Every transformation carries mathematical accountability, not just linguistic labels.
