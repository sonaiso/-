# D1 Syllable Algebra Certification Checklist

**Domain**: D1 (SYLLABIC)
**Transition**: D0 (GRAPHOPHONEMIC) → D1 (SYLLABIC)
**Status**: 🔶 In Progress (Implementation Started, Not Certified)
**Date**: 2026-05-21

---

## Executive Summary

PR #30 successfully **started** D1 implementation with candidate generation infrastructure. However, full algebraic certification requires additional components to ensure mathematical rigor and prevent cross-layer leakage.

**Current Status**:
```
D1 implementation started ✅
Syllable candidate generation exists ✅
Protocol compliance (DalCandidateProtocol) ✅
D1 algebra certified ❌
D1 total coverage closed ❌
Ready to build D2 from it ⚠️ (with caution)
```

---

## Certification Matrix

| Component | Status | Priority | Evidence |
|-----------|--------|----------|----------|
| **U_D1** (Domain Definition) | ✅ Complete | P0 | `SyllableCandidate` class defined |
| **Corr_D1** (Correctness Predicate) | ❌ Missing | P0 | Formal validator needed |
| **CPB_D1** (Conservation/Preservation/Boundary) | ⚠️ Partial | P0 | Some checks exist, not exhaustive |
| **Failure_D1** (Typed Failure Algebra) | ❌ Missing | P0 | Only generic residuals exist |
| **RankPolicy_D1** (Multi-dimensional Ranking) | ❌ Missing | P1 | Only simple confidence score |
| **ProofObject_D1** (Structured Proof) | ❌ Missing | P2 | Evidence exists but not structured as proof |
| **TestSuite_D1** (Anti-promotion Tests) | ⚠️ Partial | P0 | Architectural guards exist, local tests missing |
| **Coverage** (All Arabic Syllable Patterns) | ⚠️ Partial | P1 | Basic patterns covered, edge cases missing |

**Priority Legend**: P0 = Critical (blocks certification), P1 = High (required for production), P2 = Medium (enhances rigor)

---

## 1. U_D1: Domain Definition ✅

**Status**: Complete
**Evidence**: `src/dal_core/syllable_candidate.py:40-82`

### Definition

```python
U_D1 = {SyllableCandidate |
    candidate ∈ DalCandidateProtocol ∧
    domain = SYLLABIC ∧
    syllable ∈ {CV, CVC, CVV, CVVC, CVCC} ∧
    span = (start, end) where 0 ≤ start ≤ end ∧
    source_atoms preserved ∧
    trace reversible
}
```

### Current Implementation

```python
@dataclass
class SyllableCandidate:
    candidate_id: str
    domain: DalTransitionDomain.SYLLABIC
    syllable: Syllable
    source_atoms: List[ArabicAtom]
    span: tuple[int, int]
    evidence: List[DalEvidence]
    trace: Optional[DalTraceRef]
    confidence: float
```

### Gaps

- ❌ No explicit `boundary_before/boundary_after` markers
- ❌ No shadda expansion tracking
- ❌ No explicit long vowel type markers

### Action Items

- [ ] Add boundary markers for word-boundary sensitivity
- [ ] Add shadda expansion metadata
- [ ] Document edge cases in docstrings

---

## 2. Corr_D1: Correctness Predicate ❌

**Status**: **MISSING - Critical Gap**
**Priority**: P0 (Blocks Certification)

### Required Definition

```python
Corr_D1(candidate) =
    source_atoms_preserved(candidate) ∧
    span_correct(candidate) ∧
    syllable_pattern_legal(candidate) ∧
    nucleus_valid(candidate) ∧
    boundary_rule_satisfied(candidate) ∧
    trace_reversible(candidate) ∧
    no_illegal_atom_loss(candidate) ∧
    atom_order_preserved(candidate)
```

### Current Situation

- ⚠️ `validate_syllable_pattern()` exists but checks pattern only
- ❌ No check for atom preservation
- ❌ No check for ordering preservation
- ❌ `trace.reversible = True` is **claimed**, not **proven**

### Action Items

- [ ] **Create `src/dal_core/d1_correctness.py`** with formal `Corr_D1` validator
- [ ] Implement `verify_source_atoms_preserved()`
- [ ] Implement `verify_atom_order_preserved()`
- [ ] Implement `verify_no_atom_loss()`
- [ ] Implement `verify_trace_actually_reversible()` (run reverse operation)
- [ ] Add tests for each correctness component

---

## 3. CPB_D1: Conservation, Preservation, Boundary ⚠️

**Status**: Partial
**Priority**: P0

### Required Properties

| Property | Current Status | Evidence |
|----------|----------------|----------|
| **Type preservation** | ✅ | `domain = SYLLABIC` enforced |
| **Order preservation** | ❌ Not tested | No test verifies atom order maintained |
| **Span preservation** | ✅ | `span: tuple[int, int]` stored |
| **Boundary preservation** | ⚠️ | Detected but not validated against competitors |
| **Trace preservation** | ⚠️ | Reference stored, reversibility not proven |
| **No meaning injection** | ✅ | No meaning fields exist |
| **No premature promotion** | ⚠️ | Architectural guards exist, local tests missing |

### Critical Gap: Premature Promotion Guards

**Missing Tests**:
```python
def test_syllable_does_not_claim_root():
    """D1 must NOT claim root (D3 domain)"""

def test_syllable_does_not_claim_wazn():
    """D1 must NOT claim pattern (D4 domain)"""

def test_syllable_does_not_claim_meaning():
    """D1 must NOT claim semantic meaning"""

def test_syllable_does_not_promote_to_premorph():
    """D1 must NOT skip to D2 directly"""
```

### Action Items

- [ ] Add `test_d1_anti_promotion.py` with 6+ tests
- [ ] Test that `SyllableCandidate` has no `root` field
- [ ] Test that `SyllableCandidate` has no `wazn` field
- [ ] Test that `SyllableCandidate` has no `meaning` field
- [ ] Test that `SyllableCandidate` has no `ism/fil/harf` classification
- [ ] Verify atom order preservation in tests

---

## 4. Failure_D1: Typed Failure Algebra ❌

**Status**: **MISSING - Critical Gap**
**Priority**: P0

### Required Failure Types

```python
class D1Failure(Enum):
    INVALID_ATOM_SEQUENCE = auto()     # Atoms don't form valid syllable
    MISSING_NUCLEUS = auto()           # No vowel found
    ILLEGAL_SYLLABLE_PATTERN = auto()  # Pattern not in {CV, CVC, CVV, CVVC, CVCC}
    BOUNDARY_AMBIGUITY = auto()        # Multiple valid boundary interpretations
    LONG_VOWEL_AMBIGUITY = auto()      # Unclear if sequence is long vowel
    SHADDA_EXPANSION_FAILURE = auto()  # Can't expand shadda properly
    SUKUN_CONFLICT = auto()            # Sukun in invalid position
    TRACE_LOSS = auto()                # Cannot trace back to atoms
    SPAN_MISMATCH = auto()             # Span doesn't match atom count
    CANDIDATE_OVERFLOW = auto()        # Too many candidates generated
```

### Current Situation

```python
# Generic warning (NOT typed)
global_residuals.append(make_warning(
    ResidualType.INVALID_SYLLABLE,  # Too generic!
    "No syllable boundaries detected",
    location="syllabification"
))
```

### Action Items

- [ ] **Create `src/dal_core/d1_failures.py`** with typed failure enum
- [ ] Replace generic residuals with typed failures
- [ ] Each failure type should have:
  - Error code
  - Span information
  - Recovery suggestions
  - Severity level
- [ ] Add tests for each failure type

---

## 5. RankPolicy_D1: Multi-Dimensional Ranking ❌

**Status**: **MISSING**
**Priority**: P1 (High)

### Required Rank Vector

```python
@dataclass
class SyllableRankVector:
    """Multi-dimensional rank for syllable candidates."""
    pattern_legality: float      # Is pattern legal? [0.0, 1.0]
    boundary_confidence: float   # How confident in boundaries? [0.0, 1.0]
    trace_completeness: float    # Is trace complete/reversible? [0.0, 1.0]
    atom_coverage: float         # % of atoms included [0.0, 1.0]
    ambiguity_penalty: float     # Penalty for ambiguity [0.0, 1.0]
    long_vowel_confidence: float # Confidence in long vowel detection [0.0, 1.0]
    shadda_sukun_handling: float # Quality of shadda/sukun handling [0.0, 1.0]

    def total_rank(self, weights: Optional[dict] = None) -> float:
        """Weighted sum of rank components."""
        if weights is None:
            weights = {
                'pattern_legality': 0.25,
                'boundary_confidence': 0.20,
                'trace_completeness': 0.15,
                'atom_coverage': 0.15,
                'ambiguity_penalty': 0.10,
                'long_vowel_confidence': 0.10,
                'shadda_sukun_handling': 0.05
            }
        return sum(
            getattr(self, k) * v
            for k, v in weights.items()
        )
```

### Current Situation

```python
# Simple binary confidence (NOT a rank policy)
confidence = 0.9 if not validation_residuals else 0.5
```

**Problem**: This is a score, not a policy. It doesn't encode:
- Why this confidence?
- What dimensions were evaluated?
- How to compare two candidates with same confidence?

### Action Items

- [ ] **Create `src/dal_core/d1_rank_policy.py`**
- [ ] Implement `SyllableRankVector` class
- [ ] Replace simple `confidence` with rank vector
- [ ] Add `compute_rank()` method to `SyllableCandidate`
- [ ] Add tests for rank comparison

### Critical Law

```
confidence_score ≠ Certificate
RankPolicy ≠ Correctness
```

A high-ranked candidate can still be incorrect if Corr_D1 fails.

---

## 6. ProofObject_D1: Structured Proof ❌

**Status**: **MISSING**
**Priority**: P2 (Medium - enhances rigor)

### Required Structure

```python
@dataclass
class SyllableCandidateProof:
    """Proof that atoms form valid syllable."""

    # Claim
    claim: str  # "Atoms [0:3] form valid CV syllable"
    layer: DalTransitionDomain  # SYLLABIC

    # Input/Output
    source_domain: DalTransitionDomain  # GRAPHOPHONEMIC
    input_atoms: List[ArabicAtom]
    output_candidate: SyllableCandidate

    # Structure
    span: tuple[int, int]
    syllable_pattern: SyllableType
    onset: List[ArabicAtom]
    nucleus: List[ArabicAtom]
    coda: List[ArabicAtom]

    # Evidence
    boundary_rule: str  # Which rule determined boundaries
    evidence: List[DalEvidence]
    trace: DalTrace  # Full trace, not just ref

    # Quality
    residuals: List[Residual]
    rank_vector: SyllableRankVector

    # Context
    competitors: List[SyllableCandidate]  # Alternative interpretations
    failure_tests_passed: List[str]  # Which failure tests passed
    correctness_checks_passed: List[str]  # Which Corr_D1 checks passed
```

### Current Situation

- Evidence exists (`DalEvidence`)
- Trace reference exists (`DalTraceRef`)
- But no unified `ProofObject`

### Action Items

- [ ] Create `src/dal_core/d1_proof.py`
- [ ] Implement `SyllableCandidateProof` class
- [ ] Add `to_proof()` method on `SyllableCandidate`
- [ ] Store proof objects for certification

---

## 7. TestSuite_D1: Comprehensive Testing ⚠️

**Status**: Partial (25 tests exist, gaps remain)
**Priority**: P0

### Current Coverage (25 tests) ✅

| Category | Tests | Status |
|----------|-------|--------|
| SyllableCandidate class | 5 | ✅ |
| Boundary detection | 4 | ✅ |
| Candidate generation | 6 | ✅ |
| Candidate sets | 5 | ✅ |
| Protocol compliance | 3 | ✅ |
| Integration | 2 | ✅ |

### Missing Critical Tests ❌

#### Anti-Promotion Tests (P0)
```python
# File: tests/dal_core/test_d1_anti_promotion.py
def test_syllable_does_not_claim_root()
def test_syllable_does_not_claim_wazn()
def test_syllable_does_not_claim_meaning()
def test_syllable_does_not_claim_identity_axis()
def test_syllable_does_not_promote_to_premorph()
def test_syllable_does_not_skip_layers()
```

#### Preservation Tests (P0)
```python
# File: tests/dal_core/test_d1_preservation.py
def test_atom_order_preserved()
def test_no_atom_loss()
def test_no_atom_duplication()
def test_span_matches_atom_count()
```

#### Reversibility Tests (P0)
```python
# File: tests/dal_core/test_d1_reversibility.py
def test_trace_is_actually_reversible()  # Run reverse operation!
def test_reverse_trace_recovers_atoms()
def test_reverse_trace_preserves_order()
```

#### Failure Tests (P0)
```python
# File: tests/dal_core/test_d1_failures.py
def test_empty_sequence_returns_typed_failure()
def test_no_vowel_returns_missing_nucleus_failure()
def test_invalid_pattern_returns_typed_failure()
def test_boundary_ambiguity_produces_multiple_candidates()
```

#### Edge Case Tests (P1)
```python
# File: tests/dal_core/test_d1_edge_cases.py
def test_shadda_expansion()
def test_sukun_handling()
def test_tanwin_handling()
def test_long_vowel_ambiguity()
def test_word_boundary_syllables()
def test_geminate_consonants()
```

### Action Items

- [ ] Create `test_d1_anti_promotion.py` (6 tests)
- [ ] Create `test_d1_preservation.py` (4 tests)
- [ ] Create `test_d1_reversibility.py` (3 tests)
- [ ] Create `test_d1_failures.py` (4 tests)
- [ ] Create `test_d1_edge_cases.py` (6 tests)
- [ ] **Total new tests needed**: ~23 tests

---

## 8. Coverage: Arabic Syllable Patterns ⚠️

**Status**: Partial
**Priority**: P1

### Currently Covered ✅

- CV (كَ)
- CVC (كَتْ)
- CVV (كَا)
- CVVC (كَاتْ)
- CVCC (partial)

### Missing Patterns ❌

- **Word-initial patterns**
  - Hamza handling
  - Wasla handling

- **Word-final patterns**
  - Tanwin syllables
  - Sukun endings
  - Waqf patterns

- **Special patterns**
  - Shadda-expanded syllables
  - Geminate clusters
  - Triple consonant sequences (if permitted)

- **Cross-word syllabification**
  - Pause boundaries
  - Connected speech

### Action Items

- [ ] Add hamza pattern tests
- [ ] Add wasla pattern tests
- [ ] Add tanwin syllable tests
- [ ] Add waqf pattern tests
- [ ] Document coverage matrix

---

## Acceptance Criteria

D1 is **certified** only when ALL of the following are true:

### Critical (P0) - Must Pass

- [ ] **Corr_D1** formal validator implemented and tested
- [ ] **Failure_D1** typed failure algebra implemented
- [ ] **Anti-promotion tests** passing (no D1 → D3/D4 jumps)
- [ ] **Preservation tests** passing (order, atoms, span)
- [ ] **Reversibility tests** passing (actual reverse operation, not just claim)
- [ ] All invalid inputs return **typed** failure or residual

### High Priority (P1) - Should Pass

- [ ] **RankPolicy_D1** implemented (multi-dimensional ranking)
- [ ] **Edge case tests** passing (shadda, sukun, tanwin, long vowels)
- [ ] **Coverage audit** complete for Arabic syllable patterns
- [ ] No boundary finalization without documenting competitors

### Medium Priority (P2) - Nice to Have

- [ ] **ProofObject_D1** structured and tested
- [ ] Performance benchmarks established
- [ ] Cross-word syllabification handled

---

## Laws (Non-Negotiable)

1. ❌ **No D1 certificate without proven reversible trace**
   Current: `reversible=True` is claimed. Required: actual reverse operation tested.

2. ❌ **No syllable without nucleus validation**
   Current: Basic validation exists. Required: Exhaustive nucleus rules.

3. ❌ **No boundary finalization without competitors**
   Current: Single boundary chosen. Required: Document why others rejected.

4. ❌ **No confidence score equals certificate**
   Current: `confidence` used as quality. Required: Separate RankPolicy from Corr_D1.

5. ✅ **No D1 produces root/wazn/meaning**
   Current: Architectural guards exist (verified in `test_axis_promotion_ban.py`).

6. ❌ **All invalid inputs return typed failure**
   Current: Generic residuals. Required: Typed failure enum.

---

## Implementation Roadmap

### Phase 1: Critical Gaps (P0) - Week 1

1. **Corr_D1 Validator**
   - File: `src/dal_core/d1_correctness.py`
   - Tests: `tests/dal_core/test_d1_correctness.py`
   - Lines: ~200 code, ~150 tests

2. **Failure_D1 Algebra**
   - File: `src/dal_core/d1_failures.py`
   - Update: `syllable_candidate.py` to use typed failures
   - Tests: `tests/dal_core/test_d1_failures.py`
   - Lines: ~150 code, ~100 tests

3. **Anti-Promotion Tests**
   - File: `tests/dal_core/test_d1_anti_promotion.py`
   - Lines: ~150 tests

4. **Preservation Tests**
   - File: `tests/dal_core/test_d1_preservation.py`
   - Lines: ~100 tests

5. **Reversibility Tests**
   - File: `tests/dal_core/test_d1_reversibility.py`
   - Implement: `reverse_syllable_candidate()` function
   - Lines: ~100 code, ~75 tests

### Phase 2: High Priority (P1) - Week 2

6. **RankPolicy_D1**
   - File: `src/dal_core/d1_rank_policy.py`
   - Update: `SyllableCandidate` to use rank vector
   - Tests: `tests/dal_core/test_d1_rank_policy.py`
   - Lines: ~200 code, ~100 tests

7. **Edge Case Coverage**
   - File: `tests/dal_core/test_d1_edge_cases.py`
   - Update: `syllable_candidate.py` edge case handling
   - Lines: ~150 tests

### Phase 3: Medium Priority (P2) - Week 3

8. **ProofObject_D1**
   - File: `src/dal_core/d1_proof.py`
   - Tests: `tests/dal_core/test_d1_proof.py`
   - Lines: ~150 code, ~75 tests

---

## Verification Commands

```bash
# Run existing tests
pytest tests/dal_core/test_syllable_candidate.py -v

# Run new correctness tests (after implementation)
pytest tests/dal_core/test_d1_correctness.py -v

# Run new failure tests
pytest tests/dal_core/test_d1_failures.py -v

# Run anti-promotion tests
pytest tests/dal_core/test_d1_anti_promotion.py -v

# Run preservation tests
pytest tests/dal_core/test_d1_preservation.py -v

# Run reversibility tests
pytest tests/dal_core/test_d1_reversibility.py -v

# Run full D1 test suite
pytest tests/dal_core/test_d1_*.py tests/dal_core/test_syllable_candidate.py -v

# Expected: ~70+ tests passing
```

---

## Current Status Summary

### What Works ✅

```
✅ D1 domain defined (U_D1)
✅ Candidate generation (D0 → D1 transition)
✅ Protocol compliance (DalCandidateProtocol)
✅ Evidence-based claims
✅ Span tracking
✅ 25 initial tests passing
✅ Integration with dal_algebra architecture
✅ Anti-promotion guards (architectural level)
```

### What's Missing ❌

```
❌ Corr_D1 formal validator
❌ Failure_D1 typed algebra
❌ RankPolicy_D1 multi-dimensional ranking
❌ ProofObject_D1 structured proofs
❌ Anti-promotion tests (local D1 level)
❌ Trace reversibility proof (not just claim)
❌ Preservation tests (order, atoms, span)
❌ Edge case coverage (shadda, sukun, long vowels)
❌ Exhaustive Arabic syllable pattern coverage
```

### Status Declaration

```
Status: D1 implementation STARTED, not CERTIFIED.

Merged ≠ Certified
Tests passing ≠ Total coverage
Candidate generation ≠ Algebra closure
Implementation started ≠ Domain closed
```

---

## Next PR Recommendation

**PR Title**: "D1 Algebraic Certification: Corr_D1, Failure_D1, and Anti-Promotion Tests"

**Scope**:
- Implement Corr_D1 validator
- Implement Failure_D1 typed failures
- Add anti-promotion tests
- Add preservation tests
- Add reversibility tests

**Files**:
- `src/dal_core/d1_correctness.py` (new)
- `src/dal_core/d1_failures.py` (new)
- `src/dal_core/syllable_candidate.py` (update)
- `tests/dal_core/test_d1_correctness.py` (new)
- `tests/dal_core/test_d1_failures.py` (new)
- `tests/dal_core/test_d1_anti_promotion.py` (new)
- `tests/dal_core/test_d1_preservation.py` (new)
- `tests/dal_core/test_d1_reversibility.py` (new)

**Success Criteria**: All P0 acceptance criteria met.

---

**Document Status**: ✅ Complete
**Last Updated**: 2026-05-21
**Maintainer**: Dal Algebra Team
