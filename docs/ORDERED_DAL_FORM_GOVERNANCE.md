# Ordered Dal Form Governance

**PR #21**: Foundation governance for ordered dal representation
**Status**: Governance documentation (no implementation)
**Created**: 2026-05-20

---

## Executive Summary

This document establishes the **foundational governance principle** for all dal_core representation:

> **A mufrad signifier is an ordered bounded composition, not a bag of features.**

Every claim about a linguistic unit must carry positional and directional context. No isolated claims. No bag-of-features representation.

---

## Core Principle

### The Ordered Unit Axiom

```text
الدال المفرد = ordered bounded sequence
لا bag of features
```

**English**: A dal (signifier) unit is an ordered sequence with clear boundaries, not an unordered collection of features.

**Implications**:
1. Every unit has a position within a larger sequence
2. Every unit has defined left and right boundaries
3. Every unit has prev/next relations to adjacent units
4. Every claim about a unit must reference its position

---

## Required Invariants

### Invariant 1: No Claim Without Position

```text
لا claim بلا موضع
```

**Rule**: Every claim about a unit (letter, syllable, morpheme, word) must specify:
- `span`: (start_index, end_index)
- `index`: position within parent sequence
- `previous_unit`: reference to preceding unit (or None if first)
- `next_unit`: reference to following unit (or None if last)
- `left_boundary`: boundary type (WORD_START, SYLLABLE_START, etc.)
- `right_boundary`: boundary type (WORD_END, SYLLABLE_END, etc.)

**Forbidden**: Claims like "م is ziyadah" without specifying WHERE in the ordered sequence.

**Allowed**: "م at index 0 of 'مَكْتَب' (span 0-1) with left_boundary=WORD_START is prefix candidate"

---

### Invariant 2: No Fold Without Reverse Trace

```text
لا fold بلا reverse trace
```

**Rule**: When folding/aggregating units into higher-level structures, the transformation must preserve:
- `source_trace`: which lower-level units were folded
- `fold_operation`: what operation combined them
- `reverse_trace`: how to unfold back to source units

**Example**: If syllables [CV, CVC] fold into pre-morph candidate, the candidate must trace back to exact syllables.

---

### Invariant 3: No Adjacency Without Direction

```text
لا adjacency بلا direction
```

**Rule**: Relationships between adjacent units must specify direction:
- `previous → current` (backward relation)
- `current → next` (forward relation)
- `bidirectional` (mutual relation)

**Forbidden**: "Letter ك relates to letter ت" without specifying direction.

**Allowed**: "Letter ك at index 0 → letter ت at index 1 (forward adjacency)"

---

### Invariant 4: No Candidate Without Boundaries

```text
لا candidate بلا boundaries
```

**Rule**: Every candidate (morpheme, root, pattern) must specify:
- Start boundary within source sequence
- End boundary within source sequence
- Boundary types (MORPHEME_BOUNDARY, WORD_BOUNDARY, etc.)

**Example**: Root extraction candidate for 'كَتَبَ':
```python
RootCandidate(
    root_letters=("ك", "ت", "ب"),
    source_span=(0, 5),  # Full word span
    letter_indices=(0, 2, 4),  # Letter positions
    left_boundary=WORD_START,
    right_boundary=WORD_END
)
```

---

### Invariant 5: No Certificate Without Claim-Scoped Evidence

```text
لا certificate بلا claim-scoped evidence
```

**Rule**: High-rank judgments (TAWATUR, QIYAS) must provide evidence scoped to the claim:
- Evidence must reference exact span
- Evidence must reference exact boundary context
- Evidence must be traceable to source units

**Forbidden**: "This is فَاعِل pattern" without evidence linking to specific letter positions.

---

## Prohibited Representations

### 1. Bag of Features

❌ **FORBIDDEN**:
```python
# Unordered feature bag
word_features = {
    "has_alif": True,
    "has_shadda": True,
    "root": ("ك", "ت", "ب"),
    "pattern": "فَعَلَ"
}
```

✅ **REQUIRED**:
```python
# Ordered sequence with positions
ordered_atoms = [
    Atom(char="ك", haraka="FATHA", index=0, span=(0,1)),
    Atom(char="ت", haraka="FATHA", index=1, span=(1,2)),
    Atom(char="ب", haraka="FATHA", index=2, span=(2,3)),
]
```

### 2. Isolated Unit Claims

❌ **FORBIDDEN**:
```python
# Isolated claim without position
claim = "م is مكان indicator"
```

✅ **REQUIRED**:
```python
# Positioned claim
claim = MorphemeCandidate(
    letter="م",
    index=0,
    span=(0, 1),
    semantic_hypothesis="MAKAN_PREFIX",
    left_boundary=WORD_START,
    source_word="مَكْتَب",
    evidence=[...]
)
```

### 3. Direct Promotions Without Intermediate Levels

❌ **FORBIDDEN** (from problem statement):
1. Surface mark → case effect (علامة سطحية → إعراب)
2. Syllable → wazn (مقطع → وزن)
3. Ziyadah letter → semantic effect (زيادة → معنى)
4. Short form → root (قصير → جذر)

✅ **REQUIRED**: Each promotion goes through intermediate bounded units:
1. Surface mark → positioned atom → syllable → morpheme → case sign potential → ... → case effect
2. Syllable → pre-morph → origin → template → ... → wazn
3. Ziyadah → positioned augment → morpheme candidate → ... → semantic hypothesis
4. Short form → lexicon check → attestation → origin classification

---

## Internal Composition Before Syntax

### Layered Composition (Inside-Out)

```text
Layer 0: Letters/Marks → Positioned Atoms
Layer 1: Atoms → Syllables (with boundaries)
Layer 2: Syllables → Pre-Morph Candidates
Layer 3: Pre-Morph → Origin/Template Candidates
Layer 4: Origin/Template → Form Candidates
```

**Rule**: Each layer must complete with full positional context before proceeding to next layer.

**Example**: Cannot claim "This is فَاعِل pattern" before:
1. Atoms are positioned
2. Syllables are bounded
3. Pre-morph classification is done
4. Origin/template candidates are scoped

---

## Bidirectional Form Analysis

### Forward vs Backward Scan

**Forward Scan** (left-to-right):
- Identifies prefixes, root starts, initial patterns
- Direction: `previous → current → next`
- Use case: Finding بادئة، أصل، زيادة أمامية

**Backward Scan** (right-to-left):
- Identifies suffixes, case marks, final patterns
- Direction: `next → current → previous`
- Use case: Finding لاحقة، إعراب، ضمير، عدد/جنس

**Bidirectional Analysis**:
- Combines both scans
- Produces **form evidence**, NOT syntax
- Example: "Letter م at position 0 is prefix candidate (forward scan) AND root-initial candidate (pattern match)"

### Critical Distinction

```text
Directional analysis produces FORM EVIDENCE, not SYNTAX.
```

- ✅ Form evidence: "م at index 0 with pattern مَفْعَل suggests place noun"
- ❌ Syntax claim: "م is mubtada" (requires operator application)

---

## Explicitly Out of Scope for PR #21

This PR establishes **governance only**. The following are **explicitly forbidden** in PR #21:

❌ Do NOT implement:
- `dal_algebra.py`
- `TransitionContract`
- `RankAlgebra`
- `ResidualAlgebra`
- `CandidateSet Contract`
- `RelationCandidate`
- `CaseEffectCandidate`
- New analyzers
- MufradProof refactor

---

## Success Criteria for PR #21

After merging PR #21, the project can claim:

✅ **Allowed claim**:
> "The project has documented that dal forms must be treated as ordered, bounded, bidirectionally analyzable sequences, not bags of features."

❌ **Forbidden claim**:
> "The project has implemented Dal Algebra."
> "The project has implemented transition contracts."
> "The project has implemented ordered form analysis."

---

## Future Integration (Post-PR #21)

**PR #22**: Minimal Dal Transition Signature
- Implement `dal_algebra.py` with typed transition contracts
- Implement 8-layer transition domain architecture
- Reference this governance doc as foundation

**Roadmap PR #23-25**: Rank/Residual/CandidateSet algebras (planned, not yet created)
- Build on ordered form foundation
- Enforce positional invariants in algebra operations
- Note: PR numbers are roadmap identifiers; see `PR_STATUS_INDEX.md` for GitHub PR mapping

---

## Verification

To verify compliance with this governance:

```python
# Every unit representation must answer these questions:
def verify_ordered_unit(unit):
    assert hasattr(unit, 'span'), "No claim without position"
    assert hasattr(unit, 'index'), "No unit without index"
    assert hasattr(unit, 'left_boundary'), "No candidate without boundaries"
    assert hasattr(unit, 'right_boundary'), "No candidate without boundaries"

    # If unit is derived from fold:
    if hasattr(unit, 'fold_operation'):
        assert hasattr(unit, 'source_trace'), "No fold without reverse trace"
        assert hasattr(unit, 'reverse_trace'), "No fold without reverse trace"

    # If unit has adjacency claims:
    if hasattr(unit, 'adjacent_to'):
        assert hasattr(unit, 'direction'), "No adjacency without direction"
```

---

## Conclusion

This governance establishes the **non-negotiable foundation** for dal_core:

> **Every linguistic unit is an ordered, bounded sequence element.**
> **No isolated claims. No bag-of-features. No promotion without intermediate bounded levels.**

All future PRs must respect these invariants.

---

**Governance Status**: ✅ Documented (no implementation required)
**Next PR**: #22 (Minimal Dal Transition Signature - implements dal_algebra.py on this foundation)
