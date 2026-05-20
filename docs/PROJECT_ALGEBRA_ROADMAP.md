# Project Algebra Roadmap

**PR #22**: Complete algebra implementation roadmap
**Status**: Architecture roadmap (no implementation)
**Created**: 2026-05-20
**Last Updated**: 2026-05-20

---

## ⚠️ Important: PR Numbering

**PR numbers in this document** (e.g., "PR #23", "PR #24") are **planning identifiers**, not necessarily GitHub PR numbers.

- **Roadmap PR numbers** = Logical sequence of planned work
- **GitHub PR numbers** = Actual pull request numbers (assigned by GitHub)

**These two systems may diverge.** See `PR_STATUS_INDEX.md` for the canonical mapping between roadmap PRs and actual GitHub PRs.

**When claiming completion**: Always cite actual GitHub PR numbers, e.g.:
```
✅ "GitHub PR #22 (Roadmap PR #22: Architecture Map) is merged"
❌ "PR #23 is complete" ← Ambiguous!
```

See `ROADMAP_GOVERNANCE.md` for full governance rules.

---

## Executive Summary

This document provides the **complete roadmap** for implementing the 11-layer algebra architecture (A0-A10).

**Current Position**: PR #22 (Architecture Map)

**Roadmap Scope**: PR #22 through PR #48+ and beyond

**Numbering Note**: PR numbers below are planning identifiers. Check `PR_STATUS_INDEX.md` for actual GitHub PR mappings.

---

## Completed PRs (Before #22)

### ✅ PR #7: MufradProof Contract
- **Status**: Merged
- **Deliverable**: MufradProof data structure
- **Layer**: A3 (Dal-Mufrad)

### ✅ PR #9: SentenceFrameCandidate
- **Status**: Merged
- **Deliverable**: Frame structure analysis
- **Layer**: A4 (Dal-Murakkab)

### ✅ PR #10: PreSyntaxMufradVector
- **Status**: Merged
- **Deliverable**: Governed interface for operator consumption
- **Layer**: A4 (Dal-Murakkab)

### ✅ PR #12: CaseSignMatrix
- **Status**: Merged
- **Deliverable**: Surface case sign observations
- **Layer**: A4 (Dal-Murakkab)

### ✅ PR #14: OperatorTriggerPotential
- **Status**: Merged
- **Deliverable**: Operator activation candidates
- **Layer**: A4 (Dal-Murakkab)

### ✅ PR #16: NahwOperatorRegistry
- **Status**: Merged
- **Deliverable**: Immutable operator catalog
- **Layer**: A4 (Dal-Murakkab)

### ✅ PR #18: OperatorCandidate
- **Status**: Merged
- **Deliverable**: Operator application candidates
- **Layer**: A4 (Dal-Murakkab)

### ✅ PR #21: Ordered Dal Form Governance
- **Status**: Merged
- **Deliverable**: Governance documentation for ordered units
- **Layer**: A0 (Kernel governance)

---

## Current PR

### PR #22: Project Algebra Architecture Map (This PR)

**Scope**: Documentation and governance tests **only**

**Deliverables**:
- ✅ `TYPED_TRANSITION_ALGEBRA_KERNEL.md` (A0)
- ✅ `PROJECT_ALGEBRA_ARCHITECTURE_MAP.md` (A0-A10)
- ✅ `GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md` (A1-A2 boundary)
- ✅ `DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md` (A3-A4)
- ✅ `PROJECT_ALGEBRA_ROADMAP.md` (this document)
- ✅ `test_project_algebra_architecture_docs.py` (governance tests)

**Layer**: A0 (Kernel), A1 (General placeholder), A2-A4 (Dal positioning)

**Out of Scope**:
- ❌ Runtime implementation
- ❌ `dal_algebra.py`
- ❌ Semantic linking
- ❌ RelationCandidate
- ❌ CaseEffectCandidate

---

## Phase 1: Foundation Algebras (PR #23-#27)

**Status Note**: As of 2026-05-20, PR #23-#27 are **planning identifiers** and not yet implemented. See `PR_STATUS_INDEX.md` for GitHub PR mapping when created.

### PR #23: Minimal Dal Transition Signature

**Status**: 📋 Planned (not yet created as GitHub PR)

**Purpose**: Implement `dal_algebra.py` runtime

**Scope**: Minimal typed transition signature

**Deliverables**:
- `src/dal_core/dal_algebra.py`
  - DalDomain enum (D0-D7)
  - DalTransitionContract protocol
  - DalCandidateProtocol
  - DalEvidence model
  - DalTrace model
- `tests/dal_core/test_dal_transition_signature.py`
- `docs/DAL_TRANSITION_SIGNATURE.md`

**Out of Scope**:
- ❌ Full analyzers
- ❌ RelationCandidate
- ❌ CaseEffectCandidate
- ❌ Semantic linking

**Layer**: A2 (Pre-Semantic Dal Algebra)

---

### PR #24: Rank Algebra

**Status**: 📋 Planned (not yet created as GitHub PR)

**Purpose**: Implement claim-scoped rank system

**Scope**: Rank composition, ordering, independence

**Deliverables**:
- `src/dal_core/rank_algebra.py`
  - RankDomain enum
  - RankComposition operations
  - RankOrdering rules
  - CrossDomainRankIndependence verification
- `tests/dal_core/test_rank_algebra.py`
  - Test rank independence across domains
  - Test rank does not transfer without transition
  - Test metrics do not grant certificate
- `docs/RANK_ALGEBRA.md`

**Key Rules**:
```text
High rank in DalForm ≠ high rank in Madlul
Composition does not raise Mufrad rank
ML confidence ≠ certificate
```

**Layer**: A0 (Kernel algebra)

---

### PR #25: Residual Algebra

**Status**: 📋 Planned (not yet created as GitHub PR)

**Purpose**: Implement residual propagation and composition

**Scope**: Residual inheritance, blocker detection, composition

**Deliverables**:
- `src/dal_core/residual_algebra.py`
  - ResidualComposition operations
  - ResidualInheritance rules
  - BlockerDetection logic
  - ResidualPropagation through transitions
- `tests/dal_core/test_residual_algebra.py`
  - Test Murakkab inherits Mufrad residuals
  - Test blocker propagation
  - Test residual composition
- `docs/RESIDUAL_ALGEBRA.md`

**Key Rules**:
```text
Murakkab inherits Mufrad residuals
Composition adds residuals, never removes
Blocker in source → blocker in target
```

**Layer**: A0 (Kernel algebra)

---

### PR #26: CandidateSet Contract

**Purpose**: Implement bounded candidate set algebra

**Scope**: Candidate generation, boundedness, competitor preservation

**Deliverables**:
- `src/dal_core/candidate_set.py`
  - CandidateSet data structure
  - Boundedness enforcement
  - Competitor preservation
  - Evidence/counter-evidence tracking
- `tests/dal_core/test_candidate_set.py`
  - Test bounded generation
  - Test competitor preservation
  - Test evidence composition
- `docs/CANDIDATE_SET_CONTRACT.md`

**Key Rules**:
```text
|candidates| < ∞
Competitors preserved
Evidence + counter-evidence tracked
```

**Layer**: A0 (Kernel algebra)

---

### PR #27: Stage-Aware NoMeaning Invariant

**Purpose**: Strengthen no-meaning enforcement across all stages

**Scope**: Verify meaning fields forbidden in dal-only layers

**Deliverables**:
- Enhanced tests in `test_semantic_leak_detection.py`
- Stage-specific meaning prohibition verification
- Documentation update in `SPEC_DAL_CORE.md`

**Key Rules**:
```text
∀ stage ∈ {D0, D1, D2, D3, D4, D5, D6, D7}: meaning = FORBIDDEN
∀ MufradProof: meaning = FORBIDDEN
∀ MurakkabProof: meaning = FORBIDDEN
```

**Layer**: A2-A4 (Dal governance)

---

## Phase 2: Dal Candidate Layers (PR #28-#36)

### PR #28: OrderedUnit / FormSequence Primitives

**Purpose**: Implement ordered sequence primitives

**Scope**: Position, boundary, adjacency contracts

**Deliverables**:
- `src/dal_core/ordered_unit.py`
  - OrderedUnit protocol
  - PositionContract
  - BoundaryContract
  - AdjacencyContract
- Tests verifying ordered unit invariants

**Layer**: A2 (Pre-Semantic Dal)

---

### PR #29: Graphophonemic Candidate Layer (D0)

**Purpose**: Implement carrier → atom transitions

**Scope**: Unicode → ArabicAtom with evidence

**Deliverables**:
- Graphophonemic candidate generator
- Carrier validation
- Atom typing with evidence
- Tests for D0 layer

**Layer**: A2 (Domain D0)

---

### PR #30: Syllable Candidate Layer (D1)

**Purpose**: Implement atom → syllable transitions

**Scope**: CV, CVC, CVV, CVVC with boundaries

**Deliverables**:
- Syllable candidate generator
- Syllable boundary detection
- Syllable validation
- Tests for D1 layer

**Layer**: A2 (Domain D1)

---

### PR #31: PreMorph Candidate Layer (D2)

**Purpose**: Implement syllable → pre-morph transitions

**Scope**: Pre-morphological classification

**Deliverables**:
- PreMorph candidate generator
- Classification logic
- Boundary preservation
- Tests for D2 layer

**Layer**: A2 (Domain D2)

---

### PR #32: Origin Candidate Layer (D3)

**Purpose**: Implement origin classification

**Scope**: Root, frozen, functional classification

**Deliverables**:
- Origin candidate generator
- Root extraction candidates
- Frozen form detection
- Functional particle classification
- Tests for D3 layer

**Layer**: A2 (Domain D3)

---

### PR #33: Template Candidate Layer (D4)

**Purpose**: Implement template matching

**Scope**: Pattern (وزن) candidates

**Deliverables**:
- Template candidate generator
- Pattern matching logic
- Pattern evidence tracking
- Tests for D4 layer

**Layer**: A2 (Domain D4)

---

### PR #34: Identity Axis Candidate Layer (D5)

**Purpose**: Implement identity axis classification

**Scope**: Ism, Fi'l, Harf classification

**Deliverables**:
- Identity axis candidate generator
- Ism/Fi'l/Harf classification
- Evidence-based typing
- Tests for D5 layer

**Layer**: A2 (Domain D5)

---

### PR #35: Directional Analysis Candidate Layer (D6)

**Purpose**: Implement bidirectional form analysis

**Scope**: Forward/backward scan candidates

**Deliverables**:
- Directional analysis generator
- Forward scan logic
- Backward scan logic
- Form evidence generation
- Tests for D6 layer

**Layer**: A2 (Domain D6)

---

### PR #36: Judgment Candidate Layer (D7)

**Purpose**: Implement morphological judgment

**Scope**: Final form judgment candidates

**Deliverables**:
- Judgment candidate generator
- Morphological judgment logic
- Rank assessment
- Tests for D7 layer

**Layer**: A2 (Domain D7)

---

## Phase 3: Dal-Murakkab Completion (PR #37-#39)

### PR #37: RelationCandidate

**Purpose**: Implement ISN/TADMN/TAQYID relation candidates

**Scope**: Compositional relation structure

**Deliverables**:
- `src/dal_core/relation_candidate.py`
  - RelationType enum (ISN, TADMN, TAQYID)
  - RelationCandidate data structure
  - Relation evidence tracking
  - Competitor preservation
- `tests/dal_core/test_relation_candidate.py`
- `docs/RELATION_CANDIDATE.md`

**Layer**: A4 (Dal-Murakkab)

---

### PR #38: CaseEffectCandidate

**Purpose**: Implement case effect as structural candidates

**Scope**: Raf', nasb, jarr, jazm as compositional structure

**Deliverables**:
- `src/dal_core/case_effect_candidate.py`
  - CaseEffectType enum
  - CaseEffectCandidate data structure
  - Operator-based case assignment
  - Evidence tracking
- `tests/dal_core/test_case_effect_candidate.py`
- `docs/CASE_EFFECT_CANDIDATE.md`

**Key Distinction**:
```text
CaseEffectCandidate = structural analysis
NOT semantic interpretation
```

**Layer**: A4 (Dal-Murakkab)

---

### PR #39: MurakkabProof Closure

**Purpose**: Implement composition closure

**Scope**: Final dal-murakkab proof

**Deliverables**:
- `src/dal_core/murakkab_proof.py`
  - MurakkabProof data structure
  - Composition closure logic
  - Evidence/rank/residual composition
  - Competitor preservation
- `tests/dal_core/test_murakkab_proof.py`
- `docs/MURAKKAB_PROOF.md`

**Layer**: A4 (Dal-Murakkab)

---

## Phase 4: Dal-Madlul Boundary (PR #40-#42)

### PR #40: Wadh' Contract Definition

**Purpose**: Define signifier-signified linking contract

**Scope**: Governance for dal-madlul transition

**Deliverables**:
- `docs/WADH_CONTRACT.md`
  - Wadh' contract specification
  - Lexical attestation requirements
  - Context evidence requirements
  - Conventional usage requirements
- Governance tests (no implementation)

**Layer**: A5 (Wadh' Algebra - governance only)

---

### PR #41: Lexicon with Wadh' Attestations

**Purpose**: Implement lexicon with signifier-signified links

**Scope**: Lexical data with attestation evidence

**Deliverables**:
- `src/lexicon/wadh_lexicon.py`
  - Lexicon data structure
  - Wadh' attestation tracking
  - Evidence model
- Seed lexicon (100+ entries)
- Tests for lexicon access

**Layer**: A5 (Wadh' Algebra - data)

---

### PR #42: Wadh' Transition Implementation

**Purpose**: Implement dal → madlul transition

**Scope**: DalForm × Context → MadlulCandidate

**Deliverables**:
- `src/dal_core/wadh_transition.py`
  - WadhTransition contract
  - Lexicon lookup logic
  - Context evidence integration
  - Candidate generation
- `tests/dal_core/test_wadh_transition.py`
- `docs/WADH_TRANSITION.md`

**Layer**: A5 (Wadh' Algebra - runtime)

---

## Phase 5: Semantic Algebras (PR #43-#47)

### PR #43: Madlul Algebra

**Purpose**: Implement signified analysis

**Scope**: Lexical meaning candidates

**Deliverables**:
- `src/semantic/madlul_algebra.py`
  - MadlulCandidate structure
  - Polysemy handling
  - Homonymy detection
  - Semantic features
- `docs/MADLUL_ALGEBRA.md`

**Layer**: A6 (Madlul Algebra)

---

### PR #44: Dalalah Algebra

**Purpose**: Implement semantic relation analysis

**Scope**: المطابقة / التضمن / الالتزام

**Deliverables**:
- `src/semantic/dalalah_algebra.py`
  - DalalahType enum
  - Relation analysis logic
  - Evidence tracking
- `docs/DALALAH_ALGEBRA.md`

**Layer**: A7 (Dalalah Algebra)

---

### PR #45: Usage Algebra

**Purpose**: Implement usage type analysis

**Scope**: حقيقة / مجاز / نقل / عرف / شرع

**Deliverables**:
- `src/semantic/usage_algebra.py`
  - UsageType enum
  - Usage classification logic
  - Context evidence integration
- `docs/USAGE_ALGEBRA.md`

**Layer**: A8 (Usage Algebra)

---

### PR #46: Murad Inference Engine

**Purpose**: Implement intended meaning inference

**Scope**: Context-based intent resolution

**Deliverables**:
- `src/semantic/murad_inference.py`
  - Murad inference logic
  - Context integration
  - Ambiguity resolution
  - Speaker-intent markers
- `docs/MURAD_INFERENCE.md`

**Layer**: A9 (Murad Algebra)

---

### PR #47: General Algebra Definition

**Purpose**: Define abstract framework

**Scope**: Abstract typed transition system

**Deliverables**:
- `docs/GENERAL_ALGEBRA.md`
  - Abstract domain contracts
  - Generic transition contracts
  - Universal evidence model
  - Cross-domain boundaries
  - Composition laws

**Layer**: A1 (General Algebra)

---

## Phase 6: Verification and Hardening (PR #48+)

### PR #48: Dal-General Inclusion Proof

**Purpose**: Verify Dal Algebra satisfies General Algebra contracts

**Scope**: Formal verification

**Deliverables**:
- `docs/DAL_GENERAL_INCLUSION_PROOF.md`
  - Domain contract satisfaction
  - Transition contract satisfaction
  - Proof contract satisfaction
  - Rank policy compliance
  - Evidence policy compliance
- Verification tests

**Layer**: A1-A2 boundary verification

---

### PR #49+: Additional Algebras

Future work includes:

- **Hukm Algebra** (A10): Inference application (research-level, not automated)
- **Rhetoric Algebras**: Figurative language analysis
- **Discourse Algebras**: Multi-sentence analysis
- **Quranic Algebras**: Quranic-specific analysis

---

## Timeline Summary

### Already Completed (PR #7-#21)
- 8 PRs implementing partial dal-murakkab chain
- PR #21: Ordered dal governance

### Current (PR #22)
- Architecture map documentation

### Near-Term (PR #23-#27)
- Foundation algebras (5 PRs)
- Estimated: 2-3 months

### Medium-Term (PR #28-#39)
- Dal candidate layers (9 PRs)
- Dal-murakkab completion (3 PRs)
- Estimated: 4-6 months

### Long-Term (PR #40-#48+)
- Dal-madlul boundary (3 PRs)
- Semantic algebras (5 PRs)
- General algebra definition (1 PR)
- Verification (1+ PRs)
- Estimated: 6-12 months

**Total**: 48+ PRs over 12-24 months

---

## Critical Principles Across All PRs

### Principle 1: No Premature Abstraction

```text
Define concrete before abstract.
Dal Algebra before General Algebra.
```

### Principle 2: Evidence-First

```text
Every claim requires evidence.
Every rank requires policy.
Every transition requires contract.
```

### Principle 3: Boundary Respect

```text
No algebra claims later outputs.
Dal does not claim meaning.
Madlul does not claim murad.
```

### Principle 4: Governance Before Implementation

```text
Document contracts before runtime.
Define policies before enforcement.
Specify tests before code.
```

### Principle 5: No Overclaim

```text
Claim what is proven.
Document what is defined.
Test what is claimed.
```

---

## Verification Checkpoints

### After Phase 1 (PR #27)
- ✅ Foundation algebras defined and tested
- ✅ Dal transition signature implemented
- ✅ Rank/residual/candidateset contracts enforced

### After Phase 2 (PR #36)
- ✅ All 8 dal domains have candidate generators
- ✅ D0-D7 transitions implemented
- ✅ Mufrad closure complete

### After Phase 3 (PR #39)
- ✅ Dal-murakkab complete
- ✅ Relation and case effect candidates implemented
- ✅ Murakkab closure complete

### After Phase 4 (PR #42)
- ✅ Dal-madlul boundary crossed
- ✅ Wadh' transition implemented
- ✅ Lexicon operational

### After Phase 5 (PR #47)
- ✅ Semantic algebras defined
- ✅ Murad inference operational
- ✅ General algebra framework defined

### After Phase 6 (PR #48+)
- ✅ Dal-General inclusion verified
- ✅ All contracts proven satisfied
- ✅ System hardened

---

## Success Criteria

### Project is successful if:

1. ✅ All 11 layers (A0-A10) architecturally defined
2. ✅ Dal-only layers (A2-A4) fully implemented and tested
3. ✅ No semantic leakage in dal-only layers
4. ✅ Wadh' boundary clearly enforced
5. ✅ Evidence-based rank across all layers
6. ✅ Residual propagation verified
7. ✅ Competitor preservation verified
8. ✅ General Algebra framework defined
9. ✅ Dal inclusion in General verified
10. ✅ Complete documentation with no overclaim

---

## Allowed Claim After Full Roadmap

```text
The project has implemented a complete typed transition algebra system for Arabic linguistic analysis, spanning from graphophonemic analysis (D0) through intended meaning inference (A9), with documented boundaries and evidence-based governance at every layer.
```

## Forbidden Claim After Full Roadmap

```text
The system understands Arabic.
The system produces perfect semantic interpretation.
The system replaces human judgment.
The system is complete (linguistic analysis is unbounded).
```

---

**Version**: 1.0.0
**Status**: Roadmap complete
**Scope**: 48+ PRs across 11 algebra layers
**Timeline**: 12-24 months estimated
