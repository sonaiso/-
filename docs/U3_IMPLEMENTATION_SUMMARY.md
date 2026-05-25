# U₃ Functional Role Layer - Implementation Summary

## Overview

This PR implements **U₃ = SyllabicFunctionalRoleCarrier**, a critical intermediate layer in the Arabic computational linguistics architecture.

## Problem Statement

The previous architecture jumped directly from:
- **U₂ (Syllables)** → **D2 (Pre-Morph/Morphology)**

This created a **premature commitment problem**: syllables were immediately forced into morphological interpretations without considering their functional ambiguity.

## Solution: U₃ Intermediate Layer

U₃ provides a **role candidacy layer** where syllables receive **competing functional role candidates** that are resolved through evidence, not assumption.

### Architecture Position

```
U₀ (Unicode)
  ↓
U₁ (Grapheme)
  ↓
U₂ (Syllable)     [Already implemented: src/dal_core/syllables.py]
  ↓
U₃ (FunctionalRole)  [THIS PR: src/dal_core/u3_*.py]
  ↓
D2 (PreMorph)     [Future: morphological analysis]
  ↓
D3+ (Higher layers)
```

## Core Principle

**NO PREMATURE COMMITMENT**

Same syllable may have multiple roles depending on context:

```
بِ may be:
  - حرف جر (preposition)       [ClosedClassRole]
  - فاء/عين/لام جذر (radical)  [RootRole]
  - سابقة (prefix)             [DerivationalRole]

كَ may be:
  - كاف التشبيه (comparison)    [ClosedClassRole]
  - ضمير متصل (attached pronoun) [PronounRole]
  - حرف جذري (radical)         [RootRole]
```

## Implementation Components

### 1. Core Structures (`u3_functional_roles.py`)

**Implemented:**
- **9 Role Categories** (multi-sorted algebra):
  1. `ClosedClassRole` - Particles (12 types)
  2. `PronounRole` - Pronouns (7 types)
  3. `RootRole` - Root radicals (9 types)
  4. `DerivationalRole` - Augments/affixes (13 types)
  5. `GenderNumberRole` - Gender/number markers (9 types)
  6. `DefinitenessRole` - Definiteness markers (6 types)
  7. `VerbFeatureRole` - Verb features (9 types)
  8. `RelationPossessionRole` - Relations (7 types)
  9. `BuildInflectRole` - Mabni/Murab (6 types)

- **RoleSpan**: Functional unit over one or more syllables
- **RoleSet**: Competing role candidates
- **FunctionalRole**: Individual role with evidence
- **CompleteOne₃ predicate**: Minimal completeness check

**Total:** 78 distinct role types across 9 categories

### 2. Role Operations (`u3_operations.py`)

**Implemented Ω₃ operations:**
1. `assign_candidate_role`: Add role to candidate set
2. `merge_span`: Merge adjacent spans (e.g., إنّ = إِ + نَّ)
3. `split_span`: Split span at syllable boundary
4. `attach_to_host`: Attach to host element
5. `promote_role`: Advance rank (candidate → hypothesis → certificate)
6. `demote_role`: Reduce rank due to conflicting evidence
7. `block_role`: Remove role from candidates
8. `discharge_residual`: Remove resolved residual
9. `preserve_competitors`: Explicitly maintain competing roles

**Operation semantics:**
- All operations preserve **Trace₂** (back to U₂)
- All operations respect **blocking residuals**
- All operations document **evidence**
- All operations return **governed results** (no exceptions)

### 3. CPB₃ Guardian (`u3_cpb.py` - TO BE IMPLEMENTED)

**Will implement:**
- Trace preservation validation
- Residual composition logic
- Rank non-inflation guards
- Competitor preservation mechanism
- No-layer-jump validation
- Evidence-based promotion/demotion

### 4. U₂→U₃ Transition (`u3_projection.py` - TO BE IMPLEMENTED)

**Will implement:**
- `role_project₂₃`: Main transition function
- Syllable-to-role-span mapping
- Multi-syllable role detection (إنّ، استفعل، etc.)
- Closed-class lexicon matching
- Position-based role inference
- Host-relation analysis

### 5. Theorems (`u3_theorems.py` - TO BE IMPLEMENTED)

**Will prove:**
1. **Syllable Functional Role Theorem**:
   ```
   ∀S ∈ U₂, CompleteOne₂(S)
   ⇒
   ∃R ∈ U₃: R.span = S ∧ R.RoleSet ≠ ∅ ∧ Trace₂(R) = S
   ```

2. **Competitor Preservation Theorem**:
   ```
   CertificateRole(R, r)
   ⇒
   r ∈ RoleSet(R)
   ∧ Evidence₃(r) sufficient
   ∧ CompetitorsClosed(R, r)
   ∧ Res₃ non_blocking
   ∧ TracePreserved(R)
   ```

3. **No Premature Commitment Theorem**:
   ```
   Role assigned
   ⇒
   (Evidence sufficient ∧ Competitors blocked)
   ∨
   Rank < certificate
   ```

## Residual System

### U₃ Residual Codes (15 types)

1. `ROLE_AMBIGUITY` - Multiple competing roles
2. `CLOSED_CLASS_VS_ROOT_CONFLICT` - Particle vs radical
3. `PREFIX_VS_RADICAL_CONFLICT` - Prefix vs radical
4. `PRONOUN_VS_SUFFIX_CONFLICT` - Pronoun vs suffix
5. `DEFINITE_ARTICLE_AMBIGUITY` - ال ambiguity
6. `TANWEEN_ROLE_DEFERRED` - Tanween role unclear
7. `CASE_MARKER_DEFERRED` - Case marker unclear
8. `GENDER_MARKER_DEFERRED` - Gender marker unclear
9. `NUMBER_MARKER_DEFERRED` - Number marker unclear
10. `VERB_PREFIX_AMBIGUITY` - Verb prefix ambiguous
11. `WEAK_LETTER_ROLE_AMBIGUITY` - Weak letter role unclear
12. `HOST_NOT_IDENTIFIED` - Host relation unknown
13. `SPAN_BOUNDARY_UNCLEAR` - Span boundary unclear
14. `LEXICON_MISSING` - Closed-class lexicon unavailable
15. `PATTERN_NOT_YET_AVAILABLE` - Pattern evidence unavailable

### Residual Inheritance

```
Res₃ = Res₂ ⊕ RoleResiduals
```

U₃ inherits all U₂ residuals and adds role-specific residuals.

## Rank System

### U₃ Rank Levels

```
role_zero → role_candidate → role_hypothesis → role_strong_hypothesis → role_certificate
                                                                          ↓
                                                                    role_blocked
```

**Rank progression rules:**
- Promotion requires evidence
- Demotion on conflicting evidence
- Certificate requires all competitors blocked
- Blocked roles cannot be promoted

## Critical Laws

### Law 1: No Role Without Competitors
```
RoleSet(R) = {r₁, r₂, ..., rₙ}

Certificate(r₁) ⇒ ∀rᵢ ≠ r₁, BlockedOrDemotedByEvidence(rᵢ)
```

### Law 2: Context-Dependent Roles
```
Same syllable → Different roles in different contexts

Example:
  كَ in كَالرَّجُلِ → HarfTashbih (certificate)
  كَ in كتابُكَ  → AttachedPronoun (certificate)
  كَ in كَتَبَ   → FaRadical (certificate)
```

### Law 3: Trace Preservation
```
∀ operation ∈ Ω₃,
operation(R) = R'
⇒
Trace₂(R') ⊇ Trace₂(R)
```

### Law 4: No Layer Jumping
```
U₃ does NOT access:
  - Meaning (Madlul)
  - Syntax (I'rab)
  - Semantics (Dalalah)
  - Intent (Murad)
```

### Law 5: Evidence-Based Progression
```
Promote(R, r) requires:
  - Evidence(r) sufficient
  - No blocker residuals
  - Rank < certificate
```

## Example Scenarios

### Example 1: بِ in بِالْقَلَمِ

**U₂ (Syllable):**
```
S = بِ = CV (consonant + kasra)
```

**U₃ (Functional Role):**
```
RoleSpan(بِ) = {
  syllables: [بِ],
  candidate_roles: {
    HarfJarr (confidence: 0.8),
    PrefixCandidate (confidence: 0.3),
    FaRadicalCandidate (confidence: 0.2)
  },
  position: initial,
  evidence: [
    {source: "closed_class_lexicon", match: "بِ → HARF_JARR"},
    {source: "context", next_token: "اسم مجرور"}
  ],
  rank: role_strong_hypothesis
}
```

**After evidence from context (اسم مجرور follows):**
```
HarfJarr promoted to: role_certificate
PrefixCandidate blocked
FaRadicalCandidate blocked
```

### Example 2: إنّ (Multi-syllable)

**U₂ (Syllables):**
```
S₁ = إِ = CV
S₂ = نَّ = CّV (with shadda)
```

**U₃ (Merged span):**
```
merge_span(S₁, S₂) →
RoleSpan(إنّ) = {
  syllables: [إِ, نَّ],
  candidate_roles: {
    HarfNasb (confidence: 0.9)
  },
  position: initial,
  evidence: [
    {source: "closed_class_lexicon", match: "إنّ → HARF_NASB"},
    {source: "pattern", type: "multi_syllable_particle"}
  ],
  rank: role_certificate
}
```

### Example 3: كَ (Ambiguous)

**Context 1: كَالرَّجُلِ**
```
HarfTashbih → certificate (followed by noun)
```

**Context 2: كتابُكَ**
```
AttachedPronoun → certificate (attached to noun, position: final)
```

**Context 3: كَتَبَ**
```
FaRadical → certificate (part of root pattern)
```

**Same syllable, different certified roles in different contexts!**

## Integration with Existing Architecture

### Backward Compatibility

- **D1 (Syllables)** continues to work independently
- U₃ is **optional layer** - can be bypassed if not needed
- Existing D2 (PreMorph) can be updated to consume U₃ outputs

### Forward Compatibility

- U₃ outputs feed into **D2 (PreMorph)** for morphological analysis
- D2 will use role information to guide pattern matching
- Root roles → stem extraction
- Closed-class roles → particle recognition
- Derivational roles → augment identification

## Testing Strategy

### Unit Tests (`tests/dal_core/test_u3_*.py`)

1. **test_u3_role_structures.py**
   - Test all 78 role types
   - Test RoleSpan creation
   - Test CompleteOne₃ predicate

2. **test_u3_operations.py**
   - Test all 9 operations
   - Test operation composition
   - Test blocking behavior
   - Test evidence requirements

3. **test_u3_role_assignment.py**
   - Test بِ assignment (particle vs radical)
   - Test كَ assignment (tashbih vs pronoun vs radical)
   - Test تَ assignment (prefix vs marker vs radical)
   - Test multi-syllable roles (إنّ، استفعل)

4. **test_u3_cpb.py**
   - Test trace preservation
   - Test rank progression
   - Test competitor management
   - Test residual propagation

5. **test_u3_theorems.py**
   - Prove Syllable Functional Role Theorem
   - Prove Competitor Preservation Theorem
   - Prove No Premature Commitment Theorem

### Integration Tests

- Test D1→U₃ transition
- Test U₃→D2 boundary (when D2 updated)
- Test full pipeline: Unicode → U₃

## Performance Considerations

### Complexity Analysis

- **Role assignment**: O(1) per role
- **Span merge**: O(n) where n = syllable count
- **Competitor management**: O(m) where m = role count (typically < 10)
- **Evidence evaluation**: O(k) where k = evidence count

### Memory Usage

- Each RoleSpan: ~500 bytes (syllables + roles + traces + residuals)
- Typical word (3 syllables): ~1.5 KB
- Acceptable for real-time processing

### Optimization Opportunities

- Lazy role evaluation (only compute when needed)
- Role caching for common patterns
- Closed-class lexicon as frozen dict for fast lookup

## Documentation

### Created Files

1. `src/dal_core/u3_functional_roles.py` (✓)
2. `src/dal_core/u3_operations.py` (✓)
3. `docs/U3_FUNCTIONAL_ROLE_ALGEBRA.md` (pending)

### To Be Created

4. `src/dal_core/u3_cpb.py`
5. `src/dal_core/u3_projection.py`
6. `src/dal_core/u3_theorems.py`
7. `tests/dal_core/test_u3_*.py`

## Conclusion

U₃ layer solves the **premature commitment problem** by introducing a **role candidacy mechanism** that:

1. Preserves ambiguity until evidence resolves it
2. Allows same syllable to have different roles in different contexts
3. Uses multi-sorted algebra to prevent category mixing
4. Maintains trace back to U₂ for reversibility
5. Enforces evidence-based rank progression
6. Prevents layer jumping to semantics/syntax

This creates a **more rigorous, algebraically sound** transition from syllables to morphological analysis.

---

**PR Status:** Core structures and operations implemented. CPB₃, projection, theorems, and tests pending.

**Next Steps:**
1. Implement CPB₃ guardian
2. Implement U₂→U₃ projection
3. Implement theorems and proofs
4. Create comprehensive test suite
5. Write full documentation
6. Integrate with D1 and D2

**Architecture Version:** U₃-LAYER-v1.0
**Created:** 2026-05-25
**Author:** Claude Code Agent
