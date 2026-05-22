# General Algebra Formal Specification v0.1

**Constitutional Document**: CPB Generation Theorem Foundation

**Date**: 2026-05-22
**Status**: Foundational Specification
**Supersedes**: All prior assumptions of CPB as axiom

---

## Constitutional Principle

```text
CPB is not an origin (أصل).
CPB is a learned stable result from history of trace, primitive binding, failure, and correction.
```

The transformation:

```text
ExistentialTrace
→ PrimitiveBinding
→ Repetition / Contrast
→ Classification
→ PriorGeometry
→ Learning
→ BindingConditions
→ CPB (as theorem)
→ LayerAlgebraGenerator
```

---

## I. Breaking the Circular Dependency

### The Circle (Invalid)

```text
❌ Need CPB to bind
❌ Need binding to learn
❌ Need learning to prove CPB
```

### The Solution (Valid)

**Distinguish two binding levels**:

1. **PrimitiveBinding** (الربط البدائي): Weak experimental connection
2. **NeutralBinding / CPB** (الربط المحايد): Learned stable policy

**Relationship**:
```text
PrimitiveBinding → learns from failures → extracts conditions → NeutralBinding
```

---

## II. Formal Definitions

### Definition 1: ExistentialTrace

**Primary matter of algebra**.

```python
ExistentialTrace := ⟨
    entity_or_effect: Any,
    existence_type: ExistenceType,
    domain: Domain,
    time: TimePoint,        # MANDATORY
    place: PlacePoint,      # MANDATORY
    reference: Reference,   # MANDATORY
    channel: Channel,
    distinction: Distinction,
    trace_id: TraceID,
    residuals: Set[Residual],
    rank: Rank
⟩
```

**Laws**:
```text
L1.1: No trace without time
L1.2: No trace without place
L1.3: No trace without reference
L1.4: No prior without trace
L1.5: No learning without preserved trace
```

**Forbidden**:
```text
F1.1: Textual existence → Physical existence (without explicit bridge)
F1.2: Trace without spacetime anchor
F1.3: Reference-free trace
```

**Proof Obligations**:
```text
P1.1: Every prior must trace back to ExistentialTrace
P1.2: Time/place/reference preservation through all operations
```

**Tests Required**:
```python
test_no_trace_without_time()
test_no_trace_without_place()
test_no_trace_without_reference()
test_no_textual_to_physical_without_bridge()
test_trace_preservation_through_binding()
```

---

### Definition 2: PrimitiveBinding

**Experimental binding attempt - may fail**.

```python
PrimitiveBinding := ⟨
    trace_1: ExistentialTrace,
    trace_2: ExistentialTrace,
    relation_candidate: RelationType,
    temporal_relation: Optional[TemporalRelation],
    spatial_relation: Optional[SpatialRelation],
    reference_relation: Optional[ReferenceRelation],
    outcome: BindingOutcome,  # SUCCESS | FAILURE | UNCERTAIN
    rank: Rank,               # ceiling at CANDIDATE
    residuals: Set[Residual]
⟩
```

**Laws**:
```text
L2.1: PrimitiveBinding cannot promote rank above CANDIDATE
L2.2: PrimitiveBinding cannot produce meaning
L2.3: PrimitiveBinding cannot issue judgment
L2.4: PrimitiveBinding must preserve failure
L2.5: PrimitiveBinding preserves time/place/reference
```

**Forbidden**:
```text
F2.1: Rank promotion to LICENSED or CERTIFIED
F2.2: Meaning production from primitive binding alone
F2.3: Hiding failures
F2.4: Erasing residuals
F2.5: Cross-existence-mode binding without validation
```

**Proof Obligations**:
```text
P2.1: All failures preserved in BindingHistory
P2.2: Rank ceiling enforced
P2.3: No semantic meaning produced
```

**Tests Required**:
```python
test_primitive_binding_cannot_promote_rank()
test_primitive_binding_preserves_failures()
test_primitive_binding_no_meaning_production()
test_primitive_binding_preserves_residuals()
test_primitive_binding_rank_ceiling()
```

---

### Definition 3: BindingHistory

**Record of all primitive binding attempts**.

```python
BindingHistory := {
    attempts: List[PrimitiveBinding],
    successes: List[PrimitiveBinding],
    failures: List[PrimitiveBinding],
    uncertain: List[PrimitiveBinding],
    timestamp_ordered: bool = True
}
```

**Laws**:
```text
L3.1: History is append-only (no deletion)
L3.2: History preserves temporal order
L3.3: History categorizes outcomes
```

---

### Definition 4: PriorSeed

**NOT a hand-written rule - emerged pattern from traces**.

```python
PriorSeed := ⟨
    claim: str,
    origin_traces: Set[ExistentialTrace],
    positive_support: Set[PrimitiveBinding],
    negative_boundaries: Set[PrimitiveBinding],
    counterexamples: Set[Any],
    residuals: Set[Residual],
    rank: Rank,
    trace_history: BindingHistory
⟩
```

**Laws**:
```text
L4.1: Every PriorSeed traces to ExistentialTrace
L4.2: PriorSeed preserves binding history
L4.3: PriorSeed preserves counterexamples
L4.4: PriorSeed preserves residuals
```

**Forbidden**:
```text
F4.1: Hand-written rule without trace history
F4.2: Prior without binding history
F4.3: Hiding counterexamples
F4.4: Erasing residuals to inflate rank
```

---

### Definition 5: PriorGeometry

**Stabilized trace memory - not rule database**.

```python
PriorGeometry := {
    seeds: Dict[SeedID, PriorSeed],
    stabilization_criteria: StabilizationPolicy,
    trace_lineage: TraceGraph
}
```

**Laws**:
```text
L5.1: PriorGeometry is emergent, not pre-loaded
L5.2: All seeds trace to existential events
L5.3: Stabilization requires repeated confirmation
```

**Tests Required**:
```python
test_no_prior_without_existential_trace()
test_no_prior_without_history()
test_prior_preserves_residuals()
test_prior_preserves_counterexamples()
```

---

### Definition 6: BindingCondition

**Learned constraint on correct binding**.

```python
BindingCondition := ⟨
    condition_type: ConditionType,
    constraint: Constraint,
    origin: BindingFailure,
    scope: Scope,
    residuals: Set[Residual]
⟩
```

**Extraction Rules**:
```text
E6.1: Failure → Blocking condition
E6.2: Counterexample → Scope narrowing
E6.3: Success in limited domain → Conditional permission
```

---

### Definition 7: CPBPolicy (Central Theorem)

**Stable learned binding policy - NOT axiom**.

```python
CPBPolicy := ⟨
    conditions: Set[BindingCondition],
    scope: Scope,
    rank_policy: RankPolicy,
    residual_policy: ResidualPolicy,
    failure_modes: Set[FailureMode],
    stability_proof: StabilityProof
⟩
```

**Mathematical Formulation**:

Define policy space:
```text
Π = BindingPolicySpace
```

Define learning function:
```text
Φ: Π × BindingHistory → Π

where Φ(p, h):
  - Adds condition on failure
  - Narrows scope on counterexample
  - Preserves residuals
  - Prevents promotion without evidence
  - Expands policy only on safe repetition
```

**CPB as Fixed Point**:
```text
CPB = μΦ  (smallest stable safe policy)

Formally:
CPB = min{p ∈ Π | Φ(p, h) = p ∧ Safe(p) ∧ Stable(p)}
```

**Laws**:
```text
L7.1: CPB requires learned binding conditions
L7.2: CPB preserves trace
L7.3: CPB preserves residuals
L7.4: CPB cannot raise rank alone
L7.5: CPB is stable under Φ
```

**Forbidden**:
```text
F7.1: CPB as axiom
F7.2: CPB without learning history
F7.3: CPB that erases residuals
F7.4: CPB that promotes rank without audit
```

**Proof Obligations**:
```text
P7.1: Existence of fixed point
P7.2: Uniqueness of minimal safe stable policy
P7.3: Safety preservation under Φ
P7.4: Trace preservation through CPB operations
```

**Tests Required**:
```python
test_no_cpb_without_learned_conditions()
test_cpb_preserves_trace()
test_cpb_preserves_residuals()
test_cpb_cannot_raise_rank_alone()
test_cpb_stability_under_learning()
```

---

### Definition 8: MinimalSufficientUnit (MSU)

**Universal law - not layer-specific**.

```python
MSU[Layer] := {
    unit_requirements: Set[Requirement],
    transition_gate: Gate,
    evidence_required: Evidence,
    residuals_declared: Set[Residual]
}
```

**Universal MSU Hierarchy**:

```text
MSU_ExistentialTrace = {
    existence_type, domain, time, place, reference,
    channel, distinction, trace, residuals
}

MSU_PrimitiveBinding = {
    two_or_more_traces, relation_attempt,
    temporal_relation, spatial_relation,
    outcome_observation, residuals
}

MSU_Learning = {
    origin, repeated_cases, failed_cases,
    contrast_cases, candidate_invariant,
    candidate_scope, residuals, trace
}

MSU_CPB = {
    learned_binding_conditions, failure_handling,
    scope, rank_policy, residual_policy, replayability
}
```

**Law**:
```text
L8.1: No layer transition without MSU
```

---

### Definition 9: Rank & Residual Policies

**Rank Promotion Audit**:

```text
RankPromotion(result, target_rank) requires:
  - Evidence sufficient for target rank
  - Residuals audited and declared
  - Counterexample search performed
  - Trace preserved
  - Audit trail recorded
```

**Critical Law**:
```text
L9.1: Absence of counterexample ≠ CERTIFIED
L9.2: Counterexample absence → provisionally unblocked only
L9.3: CERTIFIED requires positive evidence + active search + scope + residual audit
```

**Tests Required**:
```python
test_absence_of_counterexample_not_certificate()
test_rank_promotion_requires_audit()
test_residual_preservation_through_promotion()
```

---

### Definition 10: LayerAlgebraGenerator

**Generates algebra from specification - not hand-coded**.

```python
LayerSpec := ⟨
    name: str,
    units: Set[UnitType],
    existence_modes: Set[ExistenceType],
    allowed_primitive_bindings: Set[BindingType],
    observable_outcomes: Set[OutcomeType],
    failure_types: Set[FailureType],
    rank_policy: RankPolicy,
    residual_policy: ResidualPolicy,
    transition_targets: Set[LayerID],
    msu_contract: MSUContract
⟩

LayerAlgebra := Generate(CPB, PriorGeometry, LayerSpec)
```

**Law**:
```text
L10.1: Every LayerAlgebra must be generated, not hand-coded
L10.2: Same generator works on multiple domains
```

**Proof of Generality**:
```text
P10.1: Generator produces physical micro layer
P10.2: Generator produces conceptual micro layer
P10.3: Generator produces linguistic micro layer
P10.4: All three preserve trace/residuals/rank
```

---

## III. Five Core Theorems

### Theorem 1: Trace Theorem

```text
∀ prior ∈ PriorGeometry:
  ∃ traces ∈ Set[ExistentialTrace]:
    prior.origin_traces = traces ∧
    ∀ t ∈ traces: Valid(t.time) ∧ Valid(t.place) ∧ Valid(t.reference)
```

**Statement**: Every legitimate prior traces back to preserved ExistentialTrace.

---

### Theorem 2: Primitive Binding Theorem

```text
∀ learning ∈ Learning:
  ∃ history ∈ BindingHistory:
    learning.source = history ∧
    (∃ success ∈ history.successes ∨
     ∃ failure ∈ history.failures ∨
     ∃ residual ∈ history.residuals)
```

**Statement**: Every legitimate learning traces back to PrimitiveBindingHistory containing successes, failures, or residuals.

---

### Theorem 3: CPB Generation Theorem ⭐

```text
CPB = μΦ

where:
  Φ: BindingPolicy × BindingHistory → BindingPolicy
  CPB is the minimal stable safe policy

Properties:
  1. Existence: μΦ exists
  2. Stability: Φ(CPB, h) = CPB for stabilized h
  3. Safety: CPB preserves trace, residuals, rank constraints
  4. Minimality: CPB is the smallest policy satisfying stability
```

**Statement**: CPB is a learned stable binding policy (fixed point of Φ), not an assumed axiom.

---

### Theorem 4: Layer Generation Theorem

```text
∀ layer ∈ LayerAlgebra:
  ∃ spec ∈ LayerSpec:
    layer = Generate(CPB, PriorGeometry, spec)
```

**Statement**: Every legitimate LayerAlgebra is generated from spec + CPB + PriorGeometry.

---

### Theorem 5: Generality Theorem

```text
Let G = LayerAlgebraGenerator
Let L₁, L₂, L₃ be three structurally different layer algebras

If:
  G.generate(spec₁) = L₁ ∧
  G.generate(spec₂) = L₂ ∧
  G.generate(spec₃) = L₃ ∧
  PreservesTrace(L₁, L₂, L₃) ∧
  PreservesResiduals(L₁, L₂, L₃) ∧
  PreservesRank(L₁, L₂, L₃)

Then:
  G qualifies as "general algebra generator"
```

**Statement**: Generality is proven when the same generator produces 3+ different layer algebras while preserving trace/residuals/rank.

---

## IV. Forbidden Operations (Red Lines)

```text
❌ F1: CPB as axiom
❌ F2: Prior without trace
❌ F3: Rule without binding_history
❌ F4: Counterexample as comment only (must be data)
❌ F5: Rank promotion without audit
❌ F6: Absence of counterexample → CERTIFIED
❌ F7: Textual existence → Physical existence without bridge
❌ F8: Hand-coded layer algebra claiming to be "generated"
❌ F9: lafzi_madlul before proving trace→binding→prior→learning→CPB
❌ F10: Deletion of failures from history
```

---

## V. Completion Criteria

Cannot declare "General Algebra Complete" unless all 10 requirements met:

```text
✅ 1. Every prior traces to ExistentialTrace
✅ 2. Every CPB traces to learned binding conditions
✅ 3. Every learned condition traces to primitive binding history
✅ 4. Every primitive binding history contains success/failure/residual
✅ 5. Every transition passes through MSU
✅ 6. Every rank promotion passes through audit
✅ 7. Every layer algebra is generated, not hand-coded
✅ 8. Generator works on 3+ different layers
✅ 9. Absence of counterexamples ≠ CERTIFIED
✅ 10. Every result is replayable
```

---

## VI. Implementation Phases

### Phase 0: This Specification ✓

### Phase 1: Existential Trace Kernel
- ExistenceEvent
- TimeGeometry
- PlaceGeometry
- ReferenceGeometry
- ExistenceBridge

### Phase 2: Primitive Binding Kernel
- PrimitiveBindingAttempt
- BindingHistory
- BindingOutcome
- BindingFailure

### Phase 3: PriorGeometry Kernel
- PriorSeed
- PriorGeometry
- PriorStabilizer

### Phase 4: Binding Condition Learner
- BindingCondition
- ConditionExtractor
- PolicyRefiner (Φ function)
- CounterexampleHandler

### Phase 5: CPB Extractor
- CPBPolicy
- CPBExtractor (μΦ solver)
- StabilityChecker

### Phase 6: Layer Generator
- LayerSpec
- LayerAlgebraGenerator
- Proof of generality on 3 micro layers

---

## VII. Test Requirements Summary

All implementations must include:

1. **Unit tests** for each definition
2. **Property tests** for laws
3. **Negative tests** for forbidden operations
4. **Integration tests** for theorems
5. **Proof-of-work tests** for completion criteria

Minimum test coverage: **95%**

---

## VIII. References

This specification supersedes:
- Prior assumptions of CPB as primitive
- Hand-coded layer algebras claiming generality
- Rule databases masquerading as PriorGeometry

This specification establishes:
- CPB as theorem (μΦ)
- Trace-first architecture
- Learning-based binding policy extraction
- Generated (not coded) layer algebras

---

**Status**: CONSTITUTIONAL
**Revision**: 0.1
**Date**: 2026-05-22

---

## IX. Summary Formula

```text
General Algebra does not begin from rule,
nor from element,
nor from CPB,
nor from language.

It begins from distinguished existential trace,
preserved in time, place, and reference,
then from primitive binding that may fail,
then from repetition and classification,
then from PriorGeometry,
then from learning correct binding conditions,
then from extracting CPB as stable binding policy,
then from generating layer algebras.

Everything before this is not general algebra,
but specialized layer algebras or organized code.
```

**The Solution**:
**CPB Generation Theorem before Layer Algebra.**

