# Typed Transition Algebra Kernel

**PR #22 Refinement**: Mathematical Foundation
**Status**: Governance documentation (no implementation)
**Created**: 2026-05-20

---

## Executive Summary

This document defines the **Typed Transition Algebra Kernel** - the precise mathematical foundation of the project's algebraic architecture.

**Critical clarification**:
> **We are NOT building a complete algebra.**
> **We are building a Typed Transition Algebra Kernel.**

This distinction prevents hallucination by avoiding false claims about complete algebraic structures (groups, rings, fields) while establishing rigorous typed transitions, closures, ranks, and proofs.

---

## Core Principle

**What we build**:
```text
Typed Transition Algebra Kernel
├─ Carrier: Successful typed objects only
├─ Transitions: Typed operations producing CandidateSet or Failure
├─ Closure: Typed, not arbitrary
├─ Equivalences: Scoped, not universal
├─ Composition: Licensed fold with trace
├─ Neutrals: Local, not global
├─ Associativity: Conditional, not universal
├─ Units: Domain-specific, not universal
├─ Ranks: Claim-scoped, multi-axis
└─ Measures: Supportive, not decisive alone
```

**What we do NOT claim**:
- ❌ Complete algebraic structure (group, ring, field)
- ❌ Universal composition laws
- ❌ Global neutral element
- ❌ Unrestricted associativity
- ❌ Arbitrary closure
- ❌ Cross-domain equivalence without contract

---

## 1. The Carrier (𝔾)

### Definition

The **carrier** is the set of **successful typed objects only**.

```text
𝔾 = successful typed objects
```

**Critical principle**:
> **The carrier contains only successful elements.**
> **Failure is NOT an element of the carrier.**
> **Failure is a transition outcome.**

### Carrier Elements

```text
𝔾 = SourceOfEffect
    ⊔ EffectTrace
    ⊔ PriorStructure
    ⊔ TasawwurCandidate
    ⊔ MadlulCandidate
    ⊔ DalForm
    ⊔ WadhContract
    ⊔ DalalahRelation
    ⊔ UsageInstance
    ⊔ MuradCandidate
```

Each element type represents a **successful cognitive object**, not a failure state.

### Failure Exclusion

```text
Failure ∉ 𝔾
```

**Why critical**:
Mixing "successful cognitive object" with "prevention result" creates confusion.

**Correct formulation**:
```text
Transition outcome = CandidateSet[𝔾] | Failure
```

Not:
```text
❌ Transition outcome ∈ 𝔾 (mixing success and failure)
```

---

## 2. Element Types

### Typing Requirement

**Law 1**: No element without type.

Every element must be **typed** and **claim-scoped**.

**Invalid**:
```text
❌ "مدلول" (raw string, no type)
```

**Valid**:
```text
✅ MadlulCandidate {
    id
    source_effect_id
    prior_structure_id
    tasawwur_id
    claim_scope
    evidence
    rank
    residuals
    trace
}
```

### Dal Form Type

**Invalid**:
```text
❌ DalForm = "كتاب" (raw text)
```

**Valid**:
```text
✅ DalForm {
    id
    raw_span
    normalized_span
    ordered_units
    boundaries
    composition_trace
    claim_scope
    evidence
    rank
    residuals
}
```

### Typing Laws

**Law 1**: No element without type
**Law 2**: No type without domain
**Law 3**: No domain without allowed/forbidden operations

---

## 3. Transitions (Operations)

### Transition Definition

**Transitions are NOT traditional algebraic operations** (addition, multiplication).

**Transitions are typed transformations**:
```text
μ : Input × Aux → CandidateSet[𝔾] | Failure
```

Where:
- `Input` ⊆ 𝔾 (typed input from carrier)
- `Aux` = Evidence | Context | Lexicon | Attestation | Policy | Qarina
- `CandidateSet[𝔾]` = set of candidates from carrier
- `Failure` = typed failure outcome (NOT in carrier)

### Core Transitions

```text
observe:
  SourceOfEffect → EffectTrace

bind_effect_to_prior:
  EffectTrace × PriorStructure → TasawwurCandidate

qualify_tasawwur:
  TasawwurCandidate → MadlulCandidate

order_dal:
  RawDalInput → DalForm

propose_dal:
  MadlulCandidate → DalFormCandidate

contract_wadh:
  DalForm × MadlulCandidate × WadhEvidence → WadhContract

derive_dalalah:
  WadhContract → DalalahRelation

instantiate_usage:
  DalalahRelation × Qarina → UsageInstance

infer_murad:
  UsageInstance × Context × License → MuradCandidate
```

### Transition Graph (Not Pipeline)

**Critical principle**:
> **Transitions form a GRAPH, not a linear pipeline.**

Different paths exist:

**Analysis path** (analyzing existing Dal):
```text
RawDalInput → DalForm → WadhContract lookup → MadlulCandidate
```

**Formation path** (proposing new naming):
```text
MadlulCandidate → ProposedDalForm → WadhContract
```

**Usage path**:
```text
DalalahRelation → Qarina → UsageInstance → Context → MuradCandidate
```

---

## 4. Typed Closure

### Closure Definition

**Law 4**: Any licensed transition on successful elements produces either:
- `CandidateSet` of successful elements from 𝔾, or
- `Failure`

```text
μ(𝔾, Aux) ⊆ CandidateSet[𝔾] ∪ Failure
```

### Closure Constraints

**Forbidden transitions**:
1. ❌ `derive_dalalah` directly from `DalForm` (must go through `WadhContract`)
2. ❌ `infer_murad` directly from `WadhContract` (must go through `UsageInstance`)
3. ❌ `contract_wadh` without both `DalForm` AND `MadlulCandidate`
4. ❌ `MadlulCandidate` without valid `Tasawwur`
5. ❌ `Tasawwur` without `EffectTrace` AND `PriorStructure`

**True closure**:
> **Typed closure, not arbitrary closure.**

---

## 5. Scoped Equivalence Relations

### Multiple Equivalences

**Law 5**: No universal equivalence across domains.

We need **scoped equivalences**:

```text
≡effect         (on EffectTrace)
≡prior          (on PriorStructure)
≡tasawwur       (on TasawwurCandidate)
≡madlul         (on MadlulCandidate)
≡dalform        (on DalForm)
≡wadh           (on WadhContract)
≡dalalah        (on DalalahRelation)
≡usage          (on UsageInstance)
≡murad          (on MuradCandidate)
```

### Example: DalForm Equivalence

```text
DalForm A ≡dalform DalForm B
```

If and only if they preserve:
- raw/normalized span
- order
- boundaries
- composition trace
- same form claim

### Forbidden Cross-Domain Equivalence

**Law 6**: No equivalence transfer across domains without licensed transition.

**Invalid**:
```text
❌ DalForm equivalence ⇒ Madlul equivalence
```

**Valid**:
```text
✅ DalForm A ≡dalform DalForm B
   AND WadhContract(A, M₁) exists
   AND WadhContract(B, M₂) exists
   ⇒ M₁ and M₂ may be related (requires Wadhʿ evidence)
```

---

## 6. Composition (Fold)

### Composition Definition

**Composition is licensed fold**:
```text
compose(source_objects, rule) → composed_object
```

### Composition Requirements

**Must preserve**:
1. source ids
2. order
3. boundary
4. rule
5. direction
6. trace
7. residuals
8. reversible explanation

### Dal Composition Example

```text
Letter + Diacritic → OrderedAtom
OrderedAtoms → SyllableCandidate
Syllables → DalFormCandidate
```

### Madlul Composition Example

```text
Attribute + Relation + Category → Structured MadlulCandidate
```

### Forbidden Composition Mixing

**Law 7**: No mixing composition across domains.

```text
❌ Dal composition ≠ Madlul composition
❌ Madlul composition ≠ Sentence composition
❌ Sentence composition ≠ Murad composition
```

Each domain has its own composition rules.

---

## 7. Neutral Elements

### No Global Neutral

**Law 8**: No universal neutral element for the entire algebra.

**Why critical**: A single neutral element for all operations would be a hallucination.

### Local Neutrals

We have **local neutrals** for specific operations:

```text
NoResidual         (for residual composition)
ZeroRank           (for rank initialization, not evidence)
EmptyTrace         (for trace initialization)
IdentityTransition (for no-op transitions)
EmptyEvidenceSet   (for evidence composition)
NoCounterEvidence  (for counter-evidence initialization)
```

### Neutral Limitations

**Law 9**: Local neutrals do not constitute claims.

```text
NoEvidence ≠ Evidence
ZeroRank ≠ Certificate
EmptyTrace ≠ Valid claim basis
```

**Critical**: These are initialization values, not proof objects.

---

## 8. Associativity

### No Universal Associativity

**Law 10**: Associativity is NOT universal.

**Why**: Different groupings may change:
- boundaries
- trace
- relation
- interpretation
- order
- residuals

### Conditional Associativity

**Associativity holds only when**:
```text
compose(compose(a,b),c) ≡ compose(a,compose(b,c))
```

**IF AND ONLY IF**:
- Trace preservation guaranteed
- Boundary preservation guaranteed
- Order preservation guaranteed
- Residuals unchanged

### Safe Associativity Example

**Evidence union** (may be associative):
```text
(E₁ ∪ E₂) ∪ E₃ = E₁ ∪ (E₂ ∪ E₃)
```

If source tracking preserved.

### Unsafe Associativity Example

**Dal composition** (NOT always associative):
```text
(Syllable₁ + Syllable₂) + Syllable₃
≠
Syllable₁ + (Syllable₂ + Syllable₃)
```

Because boundary placement differs.

---

## 9. Units

### No Universal Unit

**Law 11**: No single unit for all operations.

### Domain-Specific Units

**Form domain units**:
```text
FormUnit
EffectUnit
PriorUnit
```

**Meaning domain units**:
```text
MeaningFeature
RelationUnit
EvidenceUnit
TraceUnit
ResidualUnit
```

### Dal Algebra Units

```text
OrderedUnit
Atom
Syllable
PreMorphUnit
TemplateUnit
```

### Madlul Algebra Units

```text
ConceptUnit
AttributeUnit
RelationUnit
CategoryUnit
ConstraintUnit
```

### Forbidden Unit Transfer

**Law 12**: No unit transfer across domains without mapping.

```text
❌ FormUnit cannot be used in Madlul domain directly
✅ FormUnit → MappedMadlulUnit (with explicit transition)
```

---

## 10. Rank Structure

### Claim-Scoped Ranks

**Law 13**: Ranks must be claim-scoped.

**Governance ranks** (ordinal):
```text
ZERO         (no evidence)
HYPOTHESIS   (proposed, unverified)
LICENSED     (meets evidence threshold)
CERTIFICATE  (proven within scope)
BLOCKED      (violates constraint)
```

### Multi-Axis Internal Ranks

**Rank components**:
```text
evidence_strength
trace_completeness
residual_risk
context_dependence
lexicon_dependence
counter_evidence
competitor_strength
```

### Forbidden Rank Transfer

**Law 14**: No rank transfer across domains.

```text
❌ High rank in DalForm ⇏ High rank in Madlul
```

Each domain must establish its own rank.

---

## 11. Measurement Structure

### Measurements Are Supportive, Not Decisive

**Law 15**: Numerical measurement alone does NOT grant certificate.

**Numerical measures** (possible):
```text
confidence_score ∈ [0,1]
coverage_ratio ∈ [0,1]
trace_completeness ∈ [0,1]
similarity_score ∈ [0,1]
evidence_weight ∈ ℝ₊
residual_count ∈ ℕ
competitor_distance ∈ ℝ₊
```

**Ordinal measures**:
```text
weaker_than
stronger_than
blocked_by
requires_context
requires_lexicon
```

### Certificate Requires Policy Compliance

**Critical**:
```text
0.97 confidence ≠ Certificate
```

**Certificate requires**:
```text
confidence_score ≥ threshold
AND rank_policy satisfied
AND evidence_policy satisfied
AND residual_policy satisfied
AND proof_policy satisfied
```

---

## 12. Formal Mathematical Definition

### Carrier

```text
𝔾 = successful typed objects

𝔾 = SourceOfEffect
    ⊔ EffectTrace
    ⊔ PriorStructure
    ⊔ TasawwurCandidate
    ⊔ MadlulCandidate
    ⊔ DalForm
    ⊔ WadhContract
    ⊔ DalalahRelation
    ⊔ UsageInstance
    ⊔ MuradCandidate
```

### Transitions

```text
Ωᵢⱼ : 𝔾ᵢ × Aux → CandidateSet[𝔾ⱼ] ∪ Failure

Where:
  𝔾ᵢ = source domain subset
  𝔾ⱼ = target domain subset
  Aux = Evidence | Context | Lexicon | Attestation | Policy | Qarina
```

### Closure

```text
Ω(𝔾) ⊆ CandidateSet[𝔾] ∪ Failure
```

All licensed transitions on carrier elements produce either candidate sets from the carrier or failure.

### Equivalence

```text
≡ᵢ on each 𝔾ᵢ (domain-specific)
```

No universal equivalence across domains except through licensed transition.

---

## 13. The 16 Core Laws (Anti-Hallucination)

These laws **prevent hallucinations** by enforcing rigorous boundaries:

1. **No element without type**
2. **No type without domain**
3. **No transition without input/output scope**
4. **No result without trace**
5. **No candidate without source OR evidence OR declared deficiency**
6. **No rank without policy**
7. **No certificate without scoped ProofObject**
8. **No effect without declared or assumed source (with low rank)**
9. **No tasawwur without effect AND prior information**
10. **No candidate madlul without valid tasawwur binding**
11. **No dal without order AND boundaries**
12. **No wadhʿ without ordered dal AND candidate madlul AND wadhʿ evidence**
13. **No dalalah without wadhʿ contract**
14. **No istiʿmal without qarina**
15. **No murad without context AND licensing**
16. **No numerical measure alone grants judgment**

---

## 14. Minimal Programmatic Model

### TypedElement

```python
@dataclass
class TypedElement:
    id: str
    domain: Domain
    claim_scope: ClaimScope
    evidence: Evidence
    rank: Rank
    residuals: Residuals
    trace: Trace
```

### TransitionContract

```python
@dataclass
class TransitionContract:
    input_types: List[Type]
    output_type: Type
    required_evidence: EvidencePolicy
    required_context: ContextPolicy
    allowed_shortcuts: List[Shortcut]
    forbidden_outputs: List[Type]
    failure_modes: List[FailureMode]
    rank_policy: RankPolicy
    residual_policy: ResidualPolicy
    trace_policy: TracePolicy
```

### Candidate

```python
@dataclass
class Candidate:
    object: TypedElement
    claim: Claim
    evidence: Evidence
    counter_evidence: CounterEvidence
    rank: Rank
    residuals: Residuals
    trace: Trace
    competitors: List[Candidate]
```

### CandidateSet

```python
@dataclass
class CandidateSet:
    candidates: List[Candidate]
    blocked: List[BlockedCandidate]
    competitors: CompetitorAnalysis
    policy: Policy
    trace: Trace
```

### ProofObject

```python
@dataclass
class ProofObject:
    claim: Claim
    claim_scope: ClaimScope
    transition_contract: TransitionContract
    evidence: Evidence
    counter_evidence: CounterEvidence
    rank: Rank
    residuals: Residuals
    trace: Trace
    competitors: List[Candidate]
    failure_tests: List[FailureTest]
```

### Failure

```python
@dataclass
class Failure:
    failure_type: FailureType
    failed_transition: TransitionContract
    missing_requirement: Requirement
    blocking_residuals: Residuals
    trace: Trace
```

---

## 15. Formation Path vs. Analysis Path

### Formation Path (Cognitive Construction)

**Starting from concept**:
```text
SourceOfEffect
→ EffectTrace
→ PriorStructure
→ TasawwurCandidate
→ MadlulCandidate
→ ProposedDalForm
→ WadhContract
```

This is the **cognitive formation path**: how meaning + form + contract are built.

### Analysis Path (Existing Dal)

**Starting from form**:
```text
RawDalInput
→ DalForm
→ WadhContract lookup
→ MadlulCandidate
→ DalalahRelation
→ UsageInstance
→ MuradCandidate
```

This is the **analysis path**: interpreting existing linguistic forms.

### Usage Path

**Starting from established contract**:
```text
DalalahRelation
→ Qarina
→ UsageInstance
→ Context
→ MuradCandidate
```

This is the **usage path**: understanding actual usage in context.

---

## 16. Critical Distinction

### What We Build

```text
Typed Transition Algebra Kernel
```

**Characteristics**:
- Carrier: Successful typed objects only
- Outcomes: CandidateSet[𝔾] | Failure
- Ranks: Claim-scoped
- Proofs: Scoped ProofObjects
- Measures: Supportive, not decisive alone
- Structure: Transition graph, not pipeline

### What We Do NOT Build

```text
❌ Complete algebraic structure (group, ring, field)
❌ Universal composition laws
❌ Global neutral element
❌ Unrestricted associativity
❌ Arbitrary closure
❌ Single linear pipeline
```

### Most Important Prevention

**The General Algebra does NOT start from**:
- ❌ Dal
- ❌ Madlul
- ❌ Sound
- ❌ Letter

**The General Algebra starts from**:
1. ✅ Effect from declared source
2. ✅ Prior information
3. ✅ Tasawwur (from binding effect + prior)
4. ✅ Candidate Madlul
5. ✅ Ordered Dal
6. ✅ Wadhʿ contract
7. ✅ Dalalah
8. ✅ Istiʿmal
9. ✅ Murad

**But within a transition graph, not a single pipeline.**

---

## 17. Conclusion

The **Typed Transition Algebra Kernel** provides:

1. ✅ Rigorous type system (every element typed)
2. ✅ Clear carrier definition (successful objects only)
3. ✅ Explicit transition contracts (typed operations)
4. ✅ Scoped equivalences (no universal equivalence)
5. ✅ Licensed composition (with trace preservation)
6. ✅ Local neutrals (no global neutral)
7. ✅ Conditional associativity (not universal)
8. ✅ Domain-specific units (no universal unit)
9. ✅ Claim-scoped ranks (multi-axis, not single)
10. ✅ Supportive measures (not decisive alone)
11. ✅ 16 anti-hallucination laws
12. ✅ Graph structure (not pipeline)

**This formulation prevents false claims** about complete algebraic structures while establishing rigorous foundations for typed cognitive transitions.

---

**Status**: ✅ Documented (mathematical foundation)
**Integration**: Refines PR #22 architecture with precise formulation
**Next**: See `docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md` for layer hierarchy

