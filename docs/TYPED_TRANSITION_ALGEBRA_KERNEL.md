# Typed Transition Algebra Kernel

**PR #22**: Mathematical kernel for typed transition systems
**Status**: Architecture definition (no runtime implementation)
**Created**: 2026-05-20

---

## Executive Summary

This document defines the **Typed Transition Algebra Kernel** — the mathematical foundation governing all transition systems in this project.

This is **not a complete algebraic structure** (group, ring, monoid). It is a **governed transition system** over typed successful objects with:

- Typed carrier (successful objects only)
- Typed transitions (domain-scoped)
- Candidate sets (not unbounded possibilities)
- Failure outside carrier
- Claim-scoped rank
- Claim-scoped proof
- Domain-scoped equivalence
- Local neutral elements
- Conditional composition

---

## 1. Carrier: Successful Typed Objects

### Definition

```text
𝔾 = successful typed objects
Failure ∉ 𝔾
```

**Critical Distinction**:
- The carrier contains **only successful typed objects**
- Failure is **not an element** of the carrier
- Failure is a **transition result**

### Carrier Elements

Every element in 𝔾 must be a typed successful object such as:

```text
SourceOfEffect        (origin of surface effects)
EffectTrace           (surface effect history)
PriorStructure        (prior analysis results)
TasawwurCandidate     (conceptual form candidate)
MadlulCandidate       (signified candidate)
DalForm               (signifier form)
WadhContract          (signifier-signified link)
DalalahRelation       (semantic relation type)
UsageInstance         (usage context instance)
MuradCandidate        (intended meaning candidate)
```

### Non-Negotiable Properties

Every element `e ∈ 𝔾` must have:

```python
TypedElement:
    id: str                          # unique identifier
    domain: Domain                   # typed domain
    claim_scope: ClaimScope          # scope of validity
    evidence: List[Evidence]         # supporting evidence
    rank: Rank                       # claim-scoped rank
    residuals: List[Residual]        # unresolved issues
    trace: Trace                     # transformation history
```

**Rules**:
- No element may be untyped
- No type may lack a domain
- No domain may lack allowed and forbidden operations

---

## 2. Transition Form

### Definition

Transitions are **not functions** `f : 𝔾ᵢ → 𝔾ⱼ`.

Transitions are **candidate-generating operations**:

```text
Ωᵢⱼ : 𝔾ᵢ × Aux → CandidateSet[𝔾ⱼ] ∪ Failure
```

Where:

```text
Aux = Evidence | Context | Lexicon | Attestation | Policy | Qarina
```

### Graph-Based Architecture

The transition system is a **directed graph**, not a single pipeline:

```text
Different inputs follow different paths.
Not all domains connect to all other domains.
Some transitions are bidirectional.
Some transitions require intermediate domains.
```

### Transition Properties

Every transition `Ωᵢⱼ` must specify:

1. **Source domain** (𝔾ᵢ)
2. **Target domain** (𝔾ⱼ)
3. **Required auxiliary data** (Aux subset)
4. **Activation conditions** (when this transition is licensed)
5. **Success conditions** (what makes a valid candidate)
6. **Failure conditions** (when to return Failure)

---

## 3. CandidateSet

### Definition

```text
CandidateSet[𝔾ᵢ] = {
    claim_scope: ClaimScope,
    candidates: List[TypedElement],
    evidence: List[Evidence],
    counter_evidence: List[CounterEvidence],
    rank: Rank,
    residuals: List[Residual],
    trace: Trace,
    competitors: List[Competitor]
}
```

### Critical Properties

**CandidateSet is NOT**:
- An open possibility list
- An unbounded search space
- A lazy evaluation

**CandidateSet IS**:
- A **bounded** collection of competing candidates
- **Evidence-bearing** (both supporting and contradicting)
- **Rank-ordered** within claim scope
- **Residual-bearing** (tracks unresolved issues)
- **Trace-preserving** (maintains transformation history)
- **Competitor-preserving** (maintains alternative interpretations)

### Boundedness Requirement

Every CandidateSet must satisfy:

```text
|candidates| < ∞
∀ c ∈ candidates: c ∈ 𝔾ⱼ
```

No transition may produce unbounded candidates.

---

## 4. ProofObject

### Definition

Proof is **claim-scoped**, not global:

```python
ProofObject:
    claim: str                              # the claim being proven
    claim_scope: ClaimScope                 # domain and boundaries
    transition_contract: TransitionContract # which transition licensed this
    evidence: List[Evidence]                # supporting evidence
    counter_evidence: List[CounterEvidence] # contradicting evidence
    rank: Rank                              # claim-scoped rank
    residuals: List[Residual]               # unresolved issues
    trace: Trace                            # transformation history
    competitors: List[Competitor]           # alternative proofs
    failure_tests: List[FailureTest]        # negative evidence
```

### No Global Certificate

There is **no global certificate** that works across all domains.

Only **scoped certificates**:

```text
graphophonemic certificate    (carrier → atoms valid)
syllabic certificate          (atoms → syllables valid)
origin certificate            (form has attested origin)
template certificate          (form matches known template)
identity-axis certificate     (morphological features valid)
dalform certificate           (signifier form closed)
wadh certificate              (signifier-signified link valid)
dalalah certificate           (semantic relation valid)
usage certificate             (usage context valid)
murad certificate             (intended meaning valid)
```

### Rank is Claim-Scoped

```text
High rank in DalForm does NOT imply high rank in Madlul.
```

Example:

```text
"كَتَبَ" has TAWATUR rank as dalform (widely attested signifier)
"كَتَبَ" has SAMA rank as madlul (semantic meaning requires context)
```

---

## 5. Failure

### Definition

```python
Failure:
    failure_type: FailureType           # category of failure
    failed_transition: str              # which transition failed
    missing_requirement: List[str]      # what was missing
    blocking_residuals: List[Residual]  # what blocked success
    trace: Trace                        # history up to failure
```

### Critical Property

**Failure is NOT an element of 𝔾**.

Failure is **returned by transition**:

```text
Ωᵢⱼ(x, aux) = Failure
```

Failure is **never inserted into carrier**:

```text
Failure ∉ 𝔾ᵢ
Failure ∉ 𝔾ⱼ
```

### Failure Types

```text
MISSING_EVIDENCE        (required evidence not provided)
BLOCKING_RESIDUAL       (unresolved blocker)
INVALID_DOMAIN          (source not in expected domain)
UNSATISFIED_CONDITION   (activation condition not met)
EMPTY_CANDIDATESET      (no valid candidates generated)
UNBOUNDED_GENERATION    (candidate explosion)
```

---

## 6. Closure

### Definition

Typed closure is **not ordinary algebraic closure**:

```text
Ω(𝔾) ⊆ CandidateSet[𝔾] ∪ Failure
```

This does NOT mean `a + b ∈ 𝔾` (ordinary closure).

This means:

```text
Every licensed transition over successful typed objects returns either:
  - CandidateSet of successful typed objects, or
  - Failure
```

### Closure Properties

1. **Type preservation**: If `x ∈ 𝔾ᵢ`, then `Ωᵢⱼ(x, aux) ∈ CandidateSet[𝔾ⱼ] ∪ Failure`
2. **No type leakage**: Transition cannot produce candidates in wrong domain
3. **Bounded generation**: Every CandidateSet has finite candidates
4. **Evidence preservation**: Every candidate carries evidence from source

---

## 7. Domain-Scoped Equivalence

### Definition

Equivalence relations are **per domain**, not global:

```text
≡effect      (effect trace equivalence)
≡prior       (prior structure equivalence)
≡tasawwur    (conceptual equivalence)
≡madlul      (signified equivalence)
≡dalform     (signifier equivalence)
≡wadh        (link equivalence)
≡dalalah     (relation equivalence)
≡usage       (usage equivalence)
≡murad       (intended meaning equivalence)
```

### No Cross-Domain Equivalence Transfer

**Critical Rule**:

```text
No equivalence relation transfers across domains without a licensed transition.
```

Example:

```text
DalForm₁ ≡dalform DalForm₂  does NOT imply  Madlul₁ ≡madlul Madlul₂
```

A **WadhContract** (signifier-signified link) is required to relate dal equivalence to madlul equivalence.

### Equivalence Properties

Each equivalence relation must specify:

1. **Reflexivity** (within domain)
2. **Symmetry** (within domain)
3. **Transitivity** (within domain)
4. **Domain boundaries** (where equivalence does not transfer)

---

## 8. Composition

### Definition

Composition is **licensed fold**, not free combination:

```text
compose(source_objects, rule) → composed_object
```

### Required Preservation

Every composition must preserve:

```text
source_ids              (which objects were composed)
order                   (sequence of composition)
boundary                (where composition starts/ends)
rule                    (which composition rule applied)
direction               (forward/backward/bidirectional)
trace                   (full transformation history)
residuals               (inherited unresolved issues)
reversible_explanation  (how to unfold)
```

### Conditional Associativity

Composition is **not globally associative**.

Associativity is **allowed only when**:

```text
trace and boundaries are preserved
```

Example:

```text
(a ∘ b) ∘ c = a ∘ (b ∘ c)   IF AND ONLY IF trace((a ∘ b) ∘ c) = trace(a ∘ (b ∘ c))
```

If traces differ, associativity is **forbidden**.

---

## 9. Neutral Elements

### No Global Neutral

There is **no global neutral element** `e` such that:

```text
e ∘ x = x ∘ e = x  for all x
```

### Local Neutral Elements

Only **local neutral elements** per context:

```text
NoResidual              (no unresolved issues)
ZeroRank                (no evidence)
EmptyTrace              (no transformation history)
IdentityTransition      (no change)
EmptyEvidenceSet        (no supporting evidence)
NoCounterEvidence       (no contradicting evidence)
```

### Critical Distinction

```text
NoEvidence ≠ evidence of absence
ZeroRank ≠ certificate
EmptyTrace ≠ claim
```

Examples:

```text
NoEvidence means "no evidence was collected" (not "evidence shows it's false")
ZeroRank means "no attestation" (not "certified false")
EmptyTrace means "no transformations applied" (not "proven irreducible")
```

---

## 10. Rank

### Claim-Scoped Rank

**Rank is always scoped to claim domain**.

### Governance Ranks

Ordinal rank for governance:

```text
ZERO            (no evidence, hypothesis only)
HYPOTHESIS      (proposed but unverified)
LICENSED        (meets activation conditions)
CERTIFICATE     (meets full proof policy)
BLOCKED         (has blocking residuals)
```

### Internal Multi-Axis Rank

Within a domain, rank may have multiple axes:

```text
evidence_strength       (quality of supporting evidence)
trace_completeness      (how complete the transformation history is)
residual_risk           (severity of unresolved issues)
context_dependence      (how much context is required)
lexicon_dependence      (how much lexical data is required)
counter_evidence        (strength of contradicting evidence)
competitor_strength     (how strong competing candidates are)
```

### Cross-Domain Rank Independence

**Critical Rule**:

```text
High rank in domain Dᵢ does NOT imply high rank in domain Dⱼ.
```

Example:

```text
TAWATUR rank in DalForm (widely attested signifier)
  does NOT imply
TAWATUR rank in Madlul (widely attested meaning)
```

Each domain requires its own evidence and rank assessment.

---

## 11. Metrics

### Metrics Assist But Do Not Govern

Numerical metrics may **assist ranking** but **cannot grant certificate**:

```text
confidence_score        (0.0 - 1.0)
coverage_ratio          (how much of input is explained)
trace_completeness      (how complete transformation is)
similarity_score        (how similar to known patterns)
evidence_weight         (cumulative evidence strength)
residual_count          (number of unresolved issues)
competitor_distance     (separation from competitors)
```

### Critical Rule

```text
0.97 confidence does NOT imply certificate.
```

Certificate requires:

```text
rank_policy             (what rank is required)
evidence_policy         (what evidence is required)
residual_policy         (what residuals are allowed)
proof_policy            (what constitutes proof)
```

### Example

```text
ML model outputs: confidence=0.97, similarity=0.95
Rank: HYPOTHESIS (not CERTIFICATE)

Why?
- No lexical attestation
- No morphological trace
- No compositional evidence
- Metric alone insufficient
```

---

## 12. Typed Elements Contract

### Minimal Abstract Shape

Every typed element must implement:

```python
@dataclass
class TypedElement:
    """Abstract base for all typed elements"""

    # Identity
    id: str

    # Typing
    domain: Domain
    element_type: str

    # Claim scope
    claim_scope: ClaimScope

    # Evidence
    evidence: List[Evidence]
    counter_evidence: List[CounterEvidence] = field(default_factory=list)

    # Rank
    rank: Rank

    # Residuals
    residuals: List[Residual] = field(default_factory=list)

    # Trace
    trace: Trace

    # Competitors
    competitors: List['TypedElement'] = field(default_factory=list)
```

### Domain Contract

Every domain must specify:

```python
@dataclass
class Domain:
    """Domain specification"""

    name: str
    allowed_types: Set[str]
    forbidden_operations: Set[str]
    equivalence_relation: EquivalenceRelation
    neutral_elements: Dict[str, Any]
    rank_policy: RankPolicy
    proof_policy: ProofPolicy
```

---

## 13. Key Theorems

### Theorem 1: Type Safety

```text
∀ x ∈ 𝔾ᵢ, ∀ Ωᵢⱼ:
  Ωᵢⱼ(x, aux) = CandidateSet[𝔾ⱼ] ∨ Ωᵢⱼ(x, aux) = Failure

Never: Ωᵢⱼ(x, aux) ∈ 𝔾ₖ where k ≠ j
```

### Theorem 2: Failure Exclusion

```text
Failure ∉ 𝔾
∀ domain D: Failure ∉ D
```

### Theorem 3: Bounded Generation

```text
∀ Ωᵢⱼ, ∀ x ∈ 𝔾ᵢ:
  Ωᵢⱼ(x, aux) = CandidateSet[𝔾ⱼ] ⇒ |CandidateSet[𝔾ⱼ].candidates| < ∞
```

### Theorem 4: Rank Independence

```text
∀ x ∈ 𝔾ᵢ, ∀ Ωᵢⱼ(x, aux) = CS:
  ∀ c ∈ CS.candidates:
    rank(x) in 𝔾ᵢ ≠ rank(c) in 𝔾ⱼ
```

### Theorem 5: Evidence Preservation

```text
∀ x ∈ 𝔾ᵢ, ∀ Ωᵢⱼ(x, aux) = CS:
  ∀ c ∈ CS.candidates:
    x.trace ⊆ c.trace
```

---

## 14. Out of Scope

This kernel definition does **NOT include**:

- ❌ Runtime implementation
- ❌ Specific domain implementations
- ❌ Semantic linking
- ❌ Meaning understanding
- ❌ Operator application
- ❌ Case effect inference
- ❌ Syntax analysis
- ❌ I'rab determination

This kernel **ONLY defines**:

- ✅ Mathematical structure
- ✅ Type contracts
- ✅ Transition form
- ✅ Proof requirements
- ✅ Rank policies
- ✅ Evidence policies
- ✅ Failure semantics

---

## 15. Allowed Claim After This Definition

```text
The project has defined a Typed Transition Algebra Kernel governing transition systems over successful typed objects.
```

## Forbidden Claim After This Definition

```text
The project has implemented a complete algebra.
The project has implemented transition runtime.
The project has implemented semantic linking.
The project understands meaning.
```

---

**Version**: 1.0.0
**Status**: Kernel definition complete
**Next**: Apply kernel to specific domains (Dal Algebra, Madlul Algebra, etc.)
