# Project Algebra Roadmap

**PR #22**: Sequential roadmap from current state to complete architecture
**Created**: 2026-05-20
**Status**: Planning document (not commitment)

---

## Purpose

This document defines the **sequential roadmap** for implementing the complete project algebra architecture, from current state (Dal-Mufrad Phase 0/1 + partial Dal-Murakkab) through semantic linking to inference.

**Critical Principle**: This is a **roadmap**, not a commitment. Priorities may shift based on research needs, technical discoveries, or resource constraints.

---

## Current State (Before PR #22)

### ✅ Implemented

**PR #21**: Ordered Dal Form Governance
- Established 5 invariants for ordered bounded sequences
- Governance documentation only

**Dal-Mufrad** (A3 - Phase 0/1):
- Carrier / Ordered Form (A1)
- MufradProof closure
- Contracts 1-3 (Carrier, Atom, Unit)
- Basic morphological analysis

**Dal-Murakkab** (A4 - Partial):
- PreSyntaxMufradVector (PR #10)
- SentenceFrameCandidate (PR #12)
- CaseSignMatrix (PR #13)
- OperatorTriggerPotential (PR #14)
- NahwOperatorRegistry (PR #15/16)
- OperatorCandidate (PR #17)

---

## The Roadmap

### Phase 1: Architectural Foundation (PR #22-#27)

#### PR #22: Project Algebra Architecture Map ✅ (This PR)

**Status**: Documentation only

**Deliverables**:
- `docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md`
- `docs/GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md`
- `docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md`
- `docs/PROJECT_ALGEBRA_ROADMAP.md` (this file)
- `tests/dal_core/test_project_algebra_architecture_docs.py`

**Goal**: Establish complete architectural map (A0-A10) positioning Dal Algebra within larger framework

**Out of Scope**:
- ❌ No General Algebra implementation
- ❌ No Dal Algebra runtime
- ❌ No semantic linking
- ❌ No meaning understanding

---

#### PR #23: Minimal Dal Transition Signature

**Status**: Next after PR #22

**Deliverables**:
- `src/dal_core/dal_algebra.py` (minimal contracts only)
- DalTransitionDomain enum (8 layers: D0-D7)
- DalClaimScope enum
- DalEvidence / DalCounterEvidence
- ShortcutPolicy / EvidenceRequirement / CandidateBudgetPolicy
- DalTrace (reversibility tracking)
- DalCandidateProtocol / DalCandidateSetProtocol / DalTransitionContract
- Validation functions (3)
- Comprehensive tests

**Goal**: Minimal transition signature for licensed dal transitions

**Out of Scope**:
- ❌ No analyzers
- ❌ No RelationCandidate/CaseEffectCandidate
- ❌ No Rank/Residual Algebra implementation
- ❌ No refactoring existing code

---

#### PR #24: Rank Algebra

**Deliverables**:
- Rank composition rules
- Evidence-based ranking logic
- Rank inheritance rules
- Competitor tracking
- Rank algebra tests

**Goal**: Formalize preference ordering over candidates

**Dependencies**: PR #23 (transition contracts)

---

#### PR #25: Residual Algebra

**Deliverables**:
- Residual propagation rules
- Residual composition logic
- Residual source tracking (via DalTrace)
- Residual inheritance
- Explicit unresolved tracking
- Residual algebra tests

**Goal**: Formalize uncertainty/unresolved question tracking

**Dependencies**: PR #23 (transition contracts), PR #24 (rank)

---

#### PR #26: CandidateSet Contract

**Deliverables**:
- Candidate set operations
- Set-level ranking
- Competitor preservation
- Budget policies
- Empty set handling
- CandidateSet tests

**Goal**: Formalize candidate set behavior

**Dependencies**: PR #23-#25

---

#### PR #27: Stage-Aware NoMeaning Invariant

**Deliverables**:
- Stage-specific meaning prohibition tests
- Mufrad stage: no meaning/murad/haqiqa_majaz
- Murakkab stage: no sentence_meaning/semantic_roles/murad
- Pre-Wadh' stage: no signified fields
- Enforcement at layer boundaries
- Governance tests

**Goal**: Enforce form/meaning boundary at every stage

**Dependencies**: PR #23-#26

---

### Phase 2: Dal-Mufrad Completion (PR #28-#36)

#### PR #28: OrderedUnit / FormSequence Primitives

**Deliverables**:
- OrderedUnit base protocol
- FormSequence operations
- Span/boundary primitives
- Direction primitives
- Position tracking
- Tests

**Goal**: Foundation for 8-layer candidate implementations

**Dependencies**: PR #23-#27

---

#### PR #29: Graphophonemic Candidate Layer (D0)

**Deliverables**:
- Grapheme candidates
- Phoneme candidates
- Grapheme-phoneme correspondence
- Encoding validation
- D0 tests

**Goal**: First layer of 8-layer architecture

**Dependencies**: PR #28

---

#### PR #30: Syllable Candidate Layer (D1)

**Deliverables**:
- Syllable structure candidates (CV, CVC, etc.)
- Syllable boundary detection
- Phonotactic constraints
- Syllabification algorithms
- D1 tests

**Goal**: Second layer of 8-layer architecture

**Dependencies**: PR #29

---

#### PR #31: PreMorph Candidate Layer (D2)

**Deliverables**:
- Segmentation candidates
- Clitic detection candidates
- Stem extraction candidates
- Boundary hypotheses
- D2 tests

**Goal**: Third layer of 8-layer architecture

**Dependencies**: PR #30

---

#### PR #32: Origin Candidate Layer (D3)

**Deliverables**:
- Root extraction candidates (derived words)
- Frozen word candidates (particles, pronouns)
- Origin distinction logic
- Lexicon lookup for frozen forms
- D3 tests

**Goal**: Fourth layer - root vs frozen distinction

**Dependencies**: PR #31

---

#### PR #33: Template Candidate Layer (D4)

**Deliverables**:
- Wazn (pattern) candidates
- Pattern derivation logic
- Pattern-root compatibility
- Morphological pattern catalog
- D4 tests

**Goal**: Fifth layer - pattern application

**Dependencies**: PR #32

---

#### PR #34: Identity Axis Candidate Layer (D5)

**Deliverables**:
- Lexical identity candidates
- Lexicon lookup logic
- Identity axes (lexical vs functional vs frozen)
- Lexicon integration
- D5 tests

**Goal**: Sixth layer - lexical identity establishment

**Dependencies**: PR #33

---

#### PR #35: Directional Analysis Candidate Layer (D6)

**Deliverables**:
- Bidirectional scan logic
- Left-to-right candidates
- Right-to-left candidates
- Direction-sensitive patterns
- D6 tests

**Goal**: Seventh layer - directional analysis

**Dependencies**: PR #34

---

#### PR #36: Judgment Candidate Layer (D7)

**Deliverables**:
- Final mufrad categorization candidates
- Type resolution logic
- Noun/verb/particle judgment
- MufradProof finalization
- D7 tests

**Goal**: Eighth layer - mufrad closure

**Dependencies**: PR #35

---

### Phase 3: Dal-Murakkab Completion (PR #37-#40)

#### PR #37: RelationCandidate

**Deliverables**:
- RelationCandidate type (إسناد/تضمين/تقييد)
- ISN (إسناد) candidate logic
- TADMN (تضمين) candidate logic
- TAQYID (تقييد) candidate logic
- Relation detection from frame/operator
- Relation candidate tests

**Goal**: Grammatical relation candidates

**Dependencies**: Phase 2 complete, OperatorCandidate (PR #17)

---

#### PR #38: CaseEffectCandidate

**Deliverables**:
- CaseEffectCandidate type
- Raf' (رفع) candidates
- Nasb (نصب) candidates
- Jarr (جر) candidates
- Jazm (جزم) candidates
- Case compatibility with operators
- Case candidate tests

**Goal**: Case marking candidates (not final resolution)

**Dependencies**: PR #37

---

#### PR #39: Multi-Operator Interaction

**Deliverables**:
- Operator precedence logic
- Operator competition handling
- Operator blocking conditions
- Multi-operator trace
- Interaction tests

**Goal**: Handle complex sentences with multiple operators

**Dependencies**: PR #37-#38

---

#### PR #40: MurakkabProof Closure

**Deliverables**:
- MurakkabProof type
- Compositional closure logic
- Relation/case candidate integration
- Residual inheritance validation
- Competitor preservation validation
- Murakkab tests

**Goal**: Close compositional signifier analysis

**Dependencies**: PR #37-#39

---

### Phase 4: Semantic Boundary (PR #41-#42)

**Critical Checkpoint**: Do NOT proceed to Phase 4 until:
- ✅ Dal-Mufrad complete and stable (PR #28-#36)
- ✅ Dal-Murakkab complete and stable (PR #37-#40)
- ✅ All governance tests passing
- ✅ Architectural review complete

---

#### PR #41: Wadh' Boundary Specification

**Status**: 🔮 Future (after Dal-only loop stable)

**Deliverables**:
- Wadh' boundary documentation
- Dal → Madlul linking specification
- Lexicon-based mapping protocol
- Polysemy/homonymy handling
- Governance tests for semantic boundary

**Goal**: Specify (not implement) signifier-signified linking

**Out of Scope**: No implementation, documentation only

---

#### PR #42: Madlul Space Specification

**Status**: 🔮 Future

**Deliverables**:
- Madlul (signified) space documentation
- Concept definition framework
- Semantic feature framework
- Conceptual relation types
- Governance tests

**Goal**: Specify (not implement) signified meaning space

**Out of Scope**: No implementation, documentation only

---

### Phase 5: Semantic Implementation (PR #43+)

**Status**: 🔮 Far future

**Only after**:
- Dal-Mufrad complete
- Dal-Murakkab complete
- Wadh' boundary specified
- Madlul space specified
- Research on semantic linking completed

**Potential PRs**:
- PR #43: Wadh' Linking Implementation
- PR #44: Madlul Algebra Implementation
- PR #45: Dalalah (المطابقة/التضمن/الالتزام) Implementation
- PR #46: Usage Algebra (حقيقة/مجاز) Implementation
- PR #47: Murad Inference Implementation
- PR #48: Hukm Algebra Implementation

**Note**: Sequence and scope TBD based on research

---

## Sequencing Rules

### Rule 1: Complete Phases Sequentially

**Do NOT skip phases**:
- ❌ Don't jump to semantic (Phase 5) before completing dal-only (Phases 2-3)
- ❌ Don't implement Murakkab completion (Phase 3) before Mufrad completion (Phase 2)
- ❌ Don't implement 8-layer candidates (Phase 2) before contracts (Phase 1)

**Complete each phase** before moving to next

---

### Rule 2: Respect Dependencies

**Dependency graph**:
```
PR #22 (architecture map)
  ↓
PR #23 (transition contracts)
  ↓
PR #24 (rank) + PR #25 (residual) + PR #26 (candidate set)
  ↓
PR #27 (no-meaning invariant)
  ↓
PR #28 (ordered unit primitives)
  ↓
PR #29-#36 (8-layer candidates, sequential)
  ↓
PR #37-#40 (murakkab completion, sequential)
  ↓
Checkpoint: Dal-only loop complete
  ↓
PR #41-#42 (semantic boundary specs)
  ↓
PR #43+ (semantic implementation)
```

**Never implement** a PR before its dependencies

---

### Rule 3: Governance Tests First

**Before implementing runtime**:
- Write governance tests
- Define prohibited claims
- Define allowed claims
- Document boundaries

**Pattern**:
1. Governance documentation
2. Governance tests
3. Runtime implementation
4. Validation

---

### Rule 4: No Semantic Linking Before Dal Closure

**Critical boundary**: Do NOT start PR #41 (Wadh' boundary spec) until:
- ✅ All Phase 2 complete (PR #28-#36)
- ✅ All Phase 3 complete (PR #37-#40)
- ✅ Dal-only governance tests passing
- ✅ No meaning leaks detected

**Rationale**: Semantic linking on unstable dal foundation will propagate form errors into meaning errors

---

## Milestone Markers

### Milestone M1: Architectural Foundation Complete

**Definition**: PR #22-#27 merged

**Deliverables**:
- Complete architecture map (A0-A10)
- Transition contracts
- Rank/residual/candidate algebras
- No-meaning invariant enforced

**Validation**: All Phase 1 governance tests passing

---

### Milestone M2: Dal-Mufrad Complete

**Definition**: PR #28-#36 merged

**Deliverables**:
- 8-layer candidate implementations (D0-D7)
- Complete mufrad closure
- All morphological candidates working
- Judgment layer operational

**Validation**:
- All 8 layers tested
- MufradProof closure validated
- No semantic leaks

---

### Milestone M3: Dal-Murakkab Complete

**Definition**: PR #37-#40 merged

**Deliverables**:
- RelationCandidate working
- CaseEffectCandidate working
- Multi-operator handling
- MurakkabProof closure

**Validation**:
- Compositional tests passing
- Residual inheritance validated
- Competitor preservation validated
- No meaning leaks

---

### Milestone M4: Dal-Only Loop Closed

**Definition**: M2 + M3 + governance validation

**Criteria**:
- ✅ Dal-Mufrad complete
- ✅ Dal-Murakkab complete
- ✅ No-meaning invariant enforced at all stages
- ✅ All governance tests passing
- ✅ Architectural review complete
- ✅ Form/meaning boundary validated

**Allowed after M4**:
- Proceed to semantic boundary specification (PR #41-#42)
- Begin research on semantic linking

**Forbidden before M4**:
- Any semantic implementation
- Any meaning understanding claims
- Any murad inference

---

### Milestone M5: Semantic Boundary Specified

**Definition**: PR #41-#42 merged

**Deliverables**:
- Wadh' boundary specification
- Madlul space specification
- Dal→Madlul linking protocol
- Semantic governance tests

**Validation**:
- Boundary clearly defined
- Crossing rules specified
- Governance tests written

**Note**: Still no implementation, specification only

---

### Milestone M6: Semantic Implementation Begins

**Definition**: PR #43+ starts

**Prerequisites**:
- M4 complete (dal-only loop closed)
- M5 complete (semantic boundary specified)
- Research complete
- Design reviewed

**Status**: 🔮 Far future

---

## Flexibility and Adaptation

### This Roadmap May Change

**Reasons for change**:
- Research discoveries
- Technical constraints
- Resource limitations
- Priority shifts
- User needs

**Change process**:
- Document proposed change
- Explain rationale
- Update roadmap
- Communicate to stakeholders

---

### What is Fixed vs Flexible

**Fixed** (architectural principles):
- ✅ Dal-only before semantic
- ✅ Mufrad before Murakkab
- ✅ Contracts before implementations
- ✅ Governance tests before runtime
- ✅ No-meaning boundary enforcement

**Flexible** (implementation details):
- Exact PR boundaries
- Sequencing within phase
- Feature prioritization
- Performance optimizations
- Refactoring decisions

---

## Anti-Patterns to Avoid

### ❌ Don't: Jump to Semantic Implementation

**Problem**: Implementing Wadh'/Madlul before Dal-Murakkab complete

**Why bad**: Form errors will propagate into meaning errors

**Solution**: Complete M4 (dal-only loop closed) before starting M5

---

### ❌ Don't: Skip Governance Tests

**Problem**: Implementing runtime before governance tests

**Why bad**: No verification of boundary enforcement

**Solution**: Always write governance tests first

---

### ❌ Don't: Violate Dependencies

**Problem**: Implementing PR #30 (syllable) before PR #29 (graphophonemic)

**Why bad**: Breaks architectural layering

**Solution**: Respect dependency graph

---

### ❌ Don't: Over-Claim Progress

**Problem**: Claiming "semantic understanding" when only dal-only implemented

**Why bad**: Creates false expectations, architectural confusion

**Solution**: Use precise language from allowed/prohibited claims

---

## Progress Tracking

### Current Status (After PR #22)

```
Phase 1: Architectural Foundation
  [█░░░░░░] PR #22 done, PR #23-#27 remaining

Phase 2: Dal-Mufrad Completion
  [░░░░░░░░░] Not started

Phase 3: Dal-Murakkab Completion
  [░░░░] Not started

Phase 4: Semantic Boundary
  [░░] Not started

Phase 5: Semantic Implementation
  [░░░░░░] Far future
```

### Milestones

- [ ] M1: Architectural Foundation Complete (PR #22-#27)
- [ ] M2: Dal-Mufrad Complete (PR #28-#36)
- [ ] M3: Dal-Murakkab Complete (PR #37-#40)
- [ ] M4: Dal-Only Loop Closed (M2 + M3 + validation)
- [ ] M5: Semantic Boundary Specified (PR #41-#42)
- [ ] M6: Semantic Implementation Begins (PR #43+)

---

## Conclusion

This roadmap provides a **sequential path** from current state (Dal-Mufrad Phase 0/1 + partial Dal-Murakkab) to complete architecture (dal-only loop + semantic linking + inference).

**Key Principles**:
1. **Sequential phases**: Complete each phase before next
2. **Respect dependencies**: Follow dependency graph
3. **Dal before semantic**: Close dal-only loop before crossing to meaning
4. **Governance first**: Tests before runtime
5. **Flexible adaptation**: Roadmap may change based on research/needs

**Next Step**: PR #23 (Minimal Dal Transition Signature)

---

**Document Version**: 1.0
**Created**: 2026-05-20
**Author**: Claude Sonnet 4.5
**PR**: #22 (Documentation only)
**Status**: Planning roadmap - not commitment
