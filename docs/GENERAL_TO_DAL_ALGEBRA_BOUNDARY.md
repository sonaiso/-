# General to Dal Algebra Boundary

**PR #22**: Boundary specification between General Algebra and Dal Algebra
**Created**: 2026-05-20
**Status**: Documentation only (no implementation)

---

## Purpose

This document defines the **architectural boundary** between:
- **General Algebra** (A0): Abstract framework (future)
- **Dal Algebra** (A2): Pre-semantic Arabic signifier specialization

**Critical Disclaimer**: This is an architecture document, not a mathematical proof. We document the boundary to guide design, not to claim formal subalgebra status.

---

## What is General Algebra? (Future Concept)

General Algebra (A0) represents the **observed common patterns** across domain-specific algebras.

### Core Abstractions (Not Yet Implemented)

1. **Typed Elements**
   - Elements have types (not duck-typed)
   - Type constraints govern composition
   - Type errors block invalid operations

2. **Ordered Compositions**
   - Elements maintain sequence order
   - Order matters for semantics
   - Not bag-of-features, not set-based

3. **Partial Transitions**
   - Transitions may succeed, fail, or remain unresolved
   - Not total functions
   - Explicit failure/residual tracking

4. **Candidate Sets**
   - Multiple competing alternatives
   - Ranked by preference
   - Carry residuals (unresolved questions)
   - Preserve competitors

5. **Rank Algebra**
   - Preference ordering over candidates
   - Evidence-based ranking
   - Rank composition rules

6. **Residual Algebra**
   - Unresolved questions propagate
   - Residual composition rules
   - Explicit uncertainty tracking

7. **Trace**
   - Reverse recoverability
   - Input → output tracking
   - Fold operations preserve unfold path

8. **Evidence Model**
   - Claim-scoped evidence
   - Position-scoped observations
   - Counter-evidence (blocking)

9. **Promotion Policy**
   - Cross-layer transitions governed
   - Direct promotion constraints
   - Shortcut licensing (lexicon, trace)

10. **Composition Algebra**
    - Combining typed units
    - Boundary preservation
    - Direction specification

11. **Blocking Algebra**
    - Constraint enforcement
    - Hard vs soft blocks
    - Block propagation

12. **Failure Handling**
    - Explicit non-coverage
    - Unresolved tracking
    - No silent failure

### Status: 🔮 **Future Work**

General Algebra is **NOT implemented** in this project yet.

It exists as:
- Architectural concept
- Pattern documentation
- Design guide for Dal Algebra
- Future abstraction target

---

## What is Dal Algebra? (Partially Implemented)

Dal Algebra (A2) is a **domain specialization** applying General Algebra patterns to pre-semantic Arabic signifier analysis.

### Domain Constraints

**Input Domain**: Arabic text (الدال / signifier)

**Output Domain**: Form candidates with rank, residuals, trace

**Forbidden Domain**: Meaning (المدلول), murad (المراد), hukm (الحكم)

### Specialized Components

1. **Typed Elements** → **Arabic Form Units**
   - Carriers (encoded text)
   - Atoms (letters with marks)
   - Syllables
   - Morphemes
   - Words (مفرد)
   - Compositions (مركب)

2. **Ordered Compositions** → **Ordered Dal Sequences**
   - PR #21 governance: dal = ordered bounded sequence
   - Position tracking (span)
   - Boundary preservation
   - Direction specification

3. **Partial Transitions** → **8-Layer Transition Network**
   - D0: GRAPHOPHONEMIC
   - D1: SYLLABIC
   - D2: PRE_MORPH
   - D3: ORIGIN
   - D4: TEMPLATE
   - D5: IDENTITY_AXIS
   - D6: DIRECTIONAL_ANALYSIS
   - D7: JUDGMENT
   - Not a pipeline; partial network (شبكة انتقالات جزئية)

4. **Candidate Sets** → **Form Candidates**
   - RootCandidate
   - WaznCandidate
   - StemProof
   - CliticProof
   - SegmentationProof
   - (future) RelationCandidate
   - (future) CaseEffectCandidate

5. **Rank** → **Form-Based Ranking**
   - Morphological rank
   - Pattern frequency
   - Lexicon attestation
   - Surface sign compatibility
   - **NOT semantic plausibility** (that's A5+)

6. **Residuals** → **Form-Based Residuals**
   - Unresolved root
   - Unresolved pattern
   - Unresolved segmentation
   - **NOT semantic ambiguity** (that's A5+)

7. **Trace** → **Form Transition Trace**
   - C1 → C2a → C2b trace
   - Segmentation trace
   - Pattern derivation trace
   - Composition trace

8. **Evidence** → **Form Evidence**
   - Surface marks (الحركات)
   - Phonological patterns
   - Morphological patterns
   - Lexicon attestation
   - **NOT contextual meaning** (that's A5+)

9. **Promotion** → **Layer Transition Policy**
   - No direct grapheme → pattern promotion
   - No direct syllable → root promotion
   - Lexicon-attested shortcuts allowed
   - Trace-provided shortcuts allowed

10. **Composition** → **Nahw Composition**
    - Mufrad → Murakkab
    - Operator application candidates
    - Relation candidates
    - **NOT semantic composition** (that's A5+)

### Status: 🚧 **Partially Implemented**

Dal Algebra is implemented at:
- ✅ Dal-Mufrad (A3): Phase 0/1
- 🚧 Dal-Murakkab (A4): Partial

---

## The Boundary Definition

### Architectural Relation

```
Dal Algebra ⊂ General Algebra
```

**Interpretation**: Dal Algebra is a **domain specialization** of General Algebra

### Caution: Not a Mathematical Claim

This relationship is **architectural**, not (yet) formally proven.

**What we mean**:
- Dal Algebra uses patterns documented in General Algebra concept
- General Algebra abstracts observed patterns from Dal (and future) algebras
- Relationship guides design consistency

**What we do NOT mean**:
- ❌ Dal Algebra is a proven mathematical subalgebra
- ❌ General Algebra is a formalized algebraic structure
- ❌ Homomorphism/isomorphism properties are established

**Future work**: If/when General Algebra is formalized, validate Dal Algebra as proper subalgebra

---

## Boundary Crossing Rules

### From General to Dal (Specialization)

When specializing General Algebra to Dal Algebra:

1. **Preserve Core Patterns**
   - Ordered compositions → ordered dal sequences
   - Candidate sets → form candidate sets
   - Rank → form-based rank
   - Residuals → form-based residuals

2. **Add Domain Constraints**
   - Input: Arabic text only
   - Output: Form candidates only
   - Forbidden: Semantic outputs

3. **Specialize Types**
   - Generic element → Carrier/Atom/Syllable/Word
   - Generic candidate → RootCandidate/WaznCandidate/etc.
   - Generic evidence → Form evidence (marks, patterns, lexicon)

### From Dal to General (Abstraction)

When abstracting Dal Algebra to General Algebra:

1. **Remove Domain Specifics**
   - Arabic text → generic typed input
   - Form candidates → generic typed candidates
   - Morphological rank → generic preference order

2. **Identify Shared Patterns**
   - What patterns repeat across domains?
   - What abstractions are useful?
   - What can be unified?

3. **Document Commonalities**
   - Ordered composition pattern
   - Candidate set pattern
   - Rank/residual pattern
   - Trace pattern

---

## What Dal Algebra Inherits from General Algebra

### Pattern: Candidate Sets

**General Pattern**:
- Multiple competing alternatives
- Preference ordering
- Unresolved tracking
- Competitor preservation

**Dal Specialization**:
- `RootCandidate`, `WaznCandidate`, etc.
- Form-based ranking
- Morphological residuals
- Alternative root/pattern preservation

### Pattern: Partial Transitions

**General Pattern**:
- Source domain → target domain
- May succeed, fail, or remain unresolved
- Evidence-based
- Trace-preserving

**Dal Specialization**:
- 8-layer domain architecture (D0-D7)
- Form transition network
- Surface evidence (marks, patterns)
- Morphological trace

### Pattern: Ordered Composition

**General Pattern**:
- Elements maintain sequence
- Position tracking
- Boundary preservation
- Direction specification

**Dal Specialization**:
- PR #21 governance: ordered bounded sequences
- Span tracking: `(start_index, end_index)`
- Left/right boundaries
- Previous/next pointers

### Pattern: No-Direct-Promotion

**General Pattern**:
- Cross-layer jumps require licensing
- Shortcut policies
- Evidence requirements

**Dal Specialization**:
- No grapheme → pattern
- No syllable → root
- Lexicon-attested shortcuts
- Trace-provided shortcuts

---

## What Dal Algebra Does NOT Inherit

### General Algebra is NOT (Yet) Implemented

Dal Algebra does NOT inherit runtime code from General Algebra because:

1. **General Algebra is conceptual** - documented patterns, not implemented framework
2. **Dal Algebra is concrete** - implements patterns directly for Arabic form analysis
3. **Abstraction comes later** - after observing multiple domain specializations

### No Forced Inheritance

Dal Algebra does NOT use base classes from General Algebra because:

1. **General Algebra doesn't exist as code** yet
2. **Structural typing (protocols)** used instead of inheritance
3. **Flexibility preserved** for future refactoring

**Future**: When General Algebra is implemented, Dal Algebra may:
- Refactor to inherit from General base classes
- Or remain protocol-based (structural typing)
- Decision deferred until General Algebra design is stable

---

## Boundary Enforcement

### What Dal Algebra Must Respect

1. **Ordered Sequence Principle**
   - All dal units are ordered bounded sequences
   - No bag-of-features violations

2. **Claim Scoping**
   - Evidence must be position-scoped
   - No global claims without span

3. **Trace Preservation**
   - Fold operations preserve unfold path
   - Reverse recoverability required

4. **Boundary Tracking**
   - Every candidate has boundaries
   - Span required: `(start_index, end_index)`

5. **Form-Only Constraint**
   - No meaning fields
   - No murad outputs
   - No hukm claims

### What Dal Algebra May Customize

1. **Domain Types**
   - Arabic-specific types (root, wazn, etc.)
   - Morphological categories
   - Syntax categories (nahw)

2. **Evidence Sources**
   - Surface marks (diacritics)
   - Phonological patterns
   - Morphological patterns
   - Lexicon attestation

3. **Layer Structure**
   - 8-layer architecture (D0-D7)
   - Partial network topology
   - Layer-specific transitions

4. **Ranking Criteria**
   - Morphological frequency
   - Pattern productivity
   - Lexicon coverage
   - Surface sign compatibility

---

## Implementation Guidance

### For Dal Algebra Developers

**Do**:
- ✅ Implement Dal-specific types
- ✅ Use protocol-based contracts
- ✅ Respect ordered sequence principle
- ✅ Track position/boundaries
- ✅ Preserve trace
- ✅ Stay form-only (no meaning)

**Don't**:
- ❌ Claim to implement General Algebra
- ❌ Force inheritance from non-existent bases
- ❌ Cross into semantic domain
- ❌ Violate ordered sequence principle
- ❌ Skip trace tracking

### For Future General Algebra Developers

**Do**:
- ✅ Observe patterns across Dal (and other) algebras
- ✅ Abstract common structures
- ✅ Document shared concepts
- ✅ Design for multiple specializations

**Don't**:
- ❌ Top-down impose abstract framework
- ❌ Force Dal Algebra refactoring prematurely
- ❌ Over-generalize from single domain
- ❌ Claim mathematical formalization prematurely

---

## Testing the Boundary

### Boundary Violation Detection

**Test**: Does Dal Algebra produce semantic outputs?

```python
# ❌ VIOLATION
mufrad_proof.meaning = "كاتب means 'writer'"
murakkab_proof.murad = "the intended meaning is..."

# ✅ CORRECT
mufrad_proof.root_candidates = [RootCandidate(letters=("ك","ت","ب"))]
murakkab_proof.relation_candidates = [RelationCandidate(type=ISN)]
```

**Test**: Does Dal Algebra skip ordered sequence principle?

```python
# ❌ VIOLATION
dal_unit.features = {"case": "nominative"}  # bag of features

# ✅ CORRECT
dal_unit.span = (0, 3)  # ordered sequence with boundaries
```

### Boundary Compliance Verification

**Governance tests** (this PR):
- `test_dal_algebra_is_pre_semantic()`
- `test_dal_algebra_is_not_full_general_algebra()`
- `test_no_meaning_fields_in_dal()`
- `test_ordered_sequence_required()`

---

## Future Work

### When General Algebra Gets Implemented

**Decision points**:
1. Base classes or protocols?
2. Refactor Dal Algebra or keep as-is?
3. Mathematical formalization level?
4. Proof of subalgebra properties?

**Current stance**: Deferred until:
- Multiple domain specializations exist
- Common patterns clearly identified
- Abstraction benefits proven

### When Semantic Algebras Get Implemented

**Boundary crossing** (A4 → A5):
- Dal-Murakkab must be stable
- Wadh' algebra must be designed
- Licensed linking required
- No silent semantic promotion

---

## Summary

### General Algebra (A0)

- 🔮 **Future concept**
- Abstract framework
- Pattern documentation
- Design guide

### Dal Algebra (A2)

- 🚧 **Partially implemented**
- Domain specialization
- Pre-semantic only
- Form analysis

### Boundary

- **Architectural relation**: Dal ⊂ General (specialization)
- **Not mathematical proof**: Design consistency, not formal subalgebra
- **Enforcement**: Governance tests + architectural review
- **Future**: May formalize when General Algebra implemented

---

## Prohibited Claims

After this PR, we **may NOT claim**:

- ❌ "General Algebra is implemented"
- ❌ "Dal Algebra inherits from General Algebra base classes"
- ❌ "Dal Algebra is a proven mathematical subalgebra"
- ❌ "The boundary is formally proven"

---

## Allowed Claims

After this PR, we **may claim**:

- ✅ "General Algebra is documented as a future abstract framework"
- ✅ "Dal Algebra is designed as a specialization of General Algebra patterns"
- ✅ "The boundary is architecturally defined for design consistency"
- ✅ "Dal Algebra respects General Algebra patterns (candidates, rank, residuals, trace)"

---

**Document Version**: 1.0
**Created**: 2026-05-20
**Author**: Claude Sonnet 4.5
**PR**: #22 (Documentation only)
**Status**: Architecture boundary - not implementation
