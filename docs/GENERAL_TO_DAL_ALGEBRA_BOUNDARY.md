# General Algebra to Dal Algebra Boundary

**PR #22**: Boundary documentation between abstract framework and concrete specialization
**Status**: Architecture documentation (no implementation)
**Created**: 2026-05-20

---

## Executive Summary

This document clarifies the **architectural relationship** between:

- **General Algebra** (A1): Future abstract framework
- **Dal Algebra** (A2-A4): Pre-semantic signifier specialization

**Critical Caution**:

```text
Dal Algebra ⊂ General Algebra

This is an ARCHITECTURAL INCLUSION, not a formally proven mathematical subalgebra.
```

This PR must **not overclaim**.

---

## What General Algebra Will Be (Future)

### Purpose

General Algebra will be the **abstract framework** governing all typed transition systems in this project.

### Scope (When Defined)

```text
1. Abstract Typed Domains
   - Generic domain contracts
   - Universal type system
   - Cross-domain boundaries

2. Generic Transition Contracts
   - Abstract transition form
   - Activation conditions
   - Success/failure semantics

3. Universal Evidence Model
   - Evidence types
   - Evidence composition
   - Counter-evidence

4. Cross-Domain Boundaries
   - Licensed transitions
   - Forbidden transitions
   - Boundary validation

5. Composition Laws
   - Conditional associativity
   - Boundary preservation
   - Trace preservation

6. Rank Algebra
   - Rank ordering
   - Rank composition
   - Rank independence

7. Residual Algebra
   - Residual inheritance
   - Residual composition
   - Blocker detection

8. Trace Algebra
   - Trace composition
   - Reversibility
   - Explanation generation
```

### Status

**General Algebra is NOT YET DEFINED.**

This PR establishes only:
- Architecture map position
- Placeholder for future work
- Boundary awareness

---

## What Dal Algebra Is (Current)

### Purpose

Dal Algebra is a **pre-semantic specialization** for Arabic signifier analysis.

### Scope

```text
Input:  Surface Arabic text (vocalized)
Output: Closed signifier forms (MufradProof, future MurakkabProof)

Constraint: NO semantic interpretation
```

### Three Sub-Algebras

#### A2: Pre-Semantic Dal Algebra

**8-layer domain architecture**:

```text
D0: Graphophonemic (رسم/صوت)
D1: Syllabic (مقطع)
D2: Pre-Morph (ما قبل الصرف)
D3: Origin (أصل)
D4: Template (وزن)
D5: Identity Axis (محور الهوية)
D6: Directional Analysis (تحليل اتجاهي)
D7: Judgment (حكم صرفي)
```

**Outputs**: Typed form candidates at each layer

#### A3: Dal-Mufrad Algebra

**Purpose**: Close individual signifier

**Output**: `MufradProof`

**Authority**: Certifies **single signifier form**, not meaning

#### A4: Dal-Murakkab Algebra

**Purpose**: Compose closed signifiers

**Output**: `MurakkabProof` (future)

**Authority**: Certifies **compositional structure**, not meaning

---

## Architectural Inclusion (Not Proven Subalgebra)

### What We Mean by "Dal ⊂ General"

```text
Dal Algebra will be positioned within General Algebra.
```

**This means**:
- Dal domains are instances of General domains
- Dal transitions follow General transition contracts
- Dal proofs satisfy General proof requirements
- Dal ranks are instances of General rank policy

**This does NOT mean**:
- Dal is a proven mathematical subalgebra (homomorphism, closure, etc.)
- General Algebra is complete enough to verify inclusion
- The relationship has been formally proven

### Why Architectural Inclusion Is Enough (For Now)

```text
Purpose: Position Dal work within planned abstract framework
Not purpose: Claim mathematical rigor before General Algebra exists
```

**Benefit**:
- Dal work follows typed transition kernel
- Dal work anticipates General framework
- Dal work won't need major refactor when General Algebra is defined

**Risk if overclaimed**:
- False sense of completeness
- Missing edge cases
- Premature abstraction

---

## Boundary Awareness

### What Dal Algebra Inherits From Kernel

Dal Algebra **must respect** Typed Transition Kernel (A0):

```text
✅ Carrier = successful typed objects (Failure ∉ 𝔾)
✅ Transitions = candidate generators (not functions)
✅ CandidateSet contract (bounded, evidence-bearing)
✅ Claim-scoped proof
✅ Domain-scoped equivalence
✅ Conditional composition
✅ Local neutral elements
✅ Metrics assist, not govern
```

### What Dal Algebra Specializes

Dal Algebra **specializes** for Arabic signifier:

```text
✅ 8-layer domain architecture (D0-D7)
✅ Graphophonemic through morphological judgment
✅ Surface effects (حركات، شدة، سكون، تنوين)
✅ Syllabic constraints (CV, CVC, CVV, CVVC)
✅ Origin classification (جذر، جامد، وظيفي)
✅ Template matching (أوزان)
✅ Identity axes (اسم، فعل، حرف)
✅ Bidirectional analysis (forward/backward scan)
```

### What Dal Algebra Forbids

Dal Algebra **must NOT**:

```text
❌ Infer meaning from form
❌ Claim semantic understanding
❌ Transfer rank across dal-madlul boundary
❌ Assume compositional semantics without wadh' contract
❌ Produce murad (intended meaning)
❌ Produce hukm (legal ruling)
```

---

## Forbidden Wording (PR #22)

### ❌ FORBIDDEN

```text
"complete General Algebra"
"proved subalgebra"
"semantic understanding"
"implemented meaning inference"
"Dal is a subalgebra of General Algebra" (without "architectural")
```

### ✅ ALLOWED

```text
"architecture map"
"typed transition kernel"
"pre-semantic specialization"
"future General Algebra"
"documented boundary"
"architectural inclusion"
"Dal Algebra positioned within planned General Algebra"
```

---

## Current Implementation Status

### What Exists

```text
✅ Typed Transition Kernel (A0) - defined
✅ Dal domains (D0-D7) - architecture defined, partially implemented
✅ MufradProof (A3) - implemented
✅ PreSyntaxMufradVector (A4) - implemented
✅ OperatorTrigger, OperatorCandidate (A4) - implemented
```

### What Does NOT Exist

```text
❌ General Algebra (A1) - not yet defined
❌ RelationCandidate, CaseEffectCandidate (A4) - not implemented
❌ MurakkabProof (A4) - not implemented
❌ Wadh' Algebra (A5) - not implemented
❌ Madlul, Dalalah, Usage algebras (A6-A8) - not implemented
```

---

## Future Work Required

### To Define General Algebra (A1)

1. **Abstract Domain Contract**
   - Generic domain specification
   - Universal type system
   - Cross-domain boundaries

2. **Generic Transition Contract**
   - Abstract activation conditions
   - Success/failure semantics
   - Candidate generation rules

3. **Universal Evidence Model**
   - Evidence types
   - Evidence composition
   - Counter-evidence handling

4. **Formal Proof**
   - Prove Dal Algebra satisfies General Algebra contracts
   - Verify homomorphism (if applicable)
   - Check closure properties

### To Complete Dal Algebra (A2-A4)

1. **Missing Implementations**
   - RelationCandidate
   - CaseEffectCandidate
   - MurakkabProof

2. **Missing Analyzers**
   - Graphophonemic candidates (D0)
   - Syllabic candidates (D1)
   - Pre-morph candidates (D2)
   - Origin candidates (D3)
   - Template candidates (D4)
   - Identity axis candidates (D5)
   - Directional analysis candidates (D6)
   - Judgment candidates (D7)

3. **Missing Algebras**
   - Rank Algebra
   - Residual Algebra
   - CandidateSet Algebra

---

## Verification Strategy

### How to Verify Inclusion (Future)

When General Algebra (A1) is defined, verify:

1. **Domain Contract Satisfaction**
   ```text
   ∀ D ∈ DalDomains: D satisfies GeneralDomain contract
   ```

2. **Transition Contract Satisfaction**
   ```text
   ∀ Ω ∈ DalTransitions: Ω satisfies GeneralTransition contract
   ```

3. **Proof Contract Satisfaction**
   ```text
   ∀ P ∈ DalProofs: P satisfies GeneralProof contract
   ```

4. **Rank Policy Compliance**
   ```text
   DalRank ⊆ GeneralRank
   ```

5. **Evidence Policy Compliance**
   ```text
   DalEvidence satisfies GeneralEvidence contract
   ```

---

## Key Distinctions

### Dal Algebra vs General Algebra

| Aspect | General Algebra (A1) | Dal Algebra (A2-A4) |
|--------|---------------------|---------------------|
| **Purpose** | Abstract framework | Signifier analysis |
| **Scope** | All transition systems | Arabic signifier forms |
| **Status** | Future (not defined) | Partially implemented |
| **Authority** | Governs all algebras | Certifies form only |
| **Meaning** | N/A (abstract) | Explicitly forbidden |
| **Output** | Generic typed objects | DalForm, MufradProof |

### Pre-Semantic vs Semantic

| Layer | Type | Meaning Allowed? |
|-------|------|-----------------|
| A0 | Kernel | N/A (abstract) |
| A1 | General | N/A (abstract) |
| A2-A4 | Dal | ❌ NO (pre-semantic) |
| A5 | Wadh' | Limited (linking only) |
| A6+ | Semantic | ✅ YES (with evidence) |

---

## Boundary Enforcement

### Tests Required (Future)

```python
def test_dal_respects_kernel():
    """Verify Dal Algebra respects Typed Transition Kernel"""
    assert all_dal_objects_are_typed()
    assert failure_not_in_dal_carrier()
    assert dal_transitions_return_candidateset_or_failure()
    assert dal_proofs_are_claim_scoped()
    assert dal_equivalence_is_domain_scoped()

def test_dal_forbids_semantic_claims():
    """Verify Dal Algebra does not claim semantic outputs"""
    assert no_dal_object_has_meaning_field()
    assert no_dal_object_has_murad_field()
    assert no_dal_proof_claims_semantic_understanding()

def test_architectural_inclusion_documented():
    """Verify architectural inclusion is documented"""
    assert general_algebra_position_documented()
    assert dal_specialization_documented()
    assert boundary_documented()
    assert no_overclaim_in_docs()
```

---

## Allowed Claim After This PR

```text
The project has documented the boundary between future General Algebra (abstract framework) and Dal Algebra (pre-semantic Arabic signifier specialization), with Dal positioned as an architectural inclusion within the planned General framework.
```

## Forbidden Claim After This PR

```text
The project has proven Dal Algebra is a subalgebra.
The project has implemented General Algebra.
Dal Algebra is mathematically complete.
The inclusion relationship has been formally verified.
```

---

## Conclusion

This document establishes **boundary awareness** without **overclaiming completeness**.

**Current reality**:
- Kernel defined (A0)
- Architecture map established (A0-A10)
- Dal positioned within architecture
- General Algebra placeholder created

**Future work**:
- Define General Algebra (A1)
- Complete Dal Algebra (A2-A4)
- Verify inclusion relationship
- Prove contracts satisfied

**Governance**:
- No overclaim
- Clear boundary documentation
- Architectural positioning
- Future verification plan

---

**Version**: 1.0.0
**Status**: Boundary documented
**Scope**: Architecture awareness (no mathematical proof)
