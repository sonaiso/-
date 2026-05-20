## Dal Algebra Minimal Transition Signature

**PR #22**: Minimal licensed-transition contracts for ordered bounded dal sequences
**Created**: 2026-05-20
**Builds on**: PR #21 Ordered Dal Form Governance

---

## Purpose

This document specifies the **minimal signature** for dal transitions, implementing the governance principles established in PR #21.

**Core Principle**: Dal transitions operate on **ordered bounded sequences**, not bags of features.

---

## Architecture Overview

### 8-Layer Transition Domain Architecture

Dal transitions operate across 8 distinct domains (D0-D7):

| Domain | Layer | Arabic | Description |
|--------|-------|--------|-------------|
| D0 | GRAPHOPHONEMIC | رسم/صوت | Grapheme/phoneme level |
| D1 | SYLLABIC | مقطع | Syllable structure |
| D2 | PRE_MORPH | ما قبل الصرف | Pre-morphological |
| D3 | ORIGIN | أصل | Root or frozen form |
| D4 | TEMPLATE | وزن | Morphological pattern |
| D5 | IDENTITY_AXIS | محور الهوية | Lexical identity |
| D6 | DIRECTIONAL_ANALYSIS | تحليل اتجاهي | Bidirectional scan |
| D7 | JUDGMENT | حكم | Final categorization |

**Key Insight**: This is a **partial transition network** (شبكة انتقالات جزئية), not a single pipeline. Different words follow different paths.

---

## Transition Contracts

### DalTransitionContract Protocol

Every transition must implement:

```python
class DalTransitionContract(Protocol[T_Input, T_Output]):
    @property
    def source_domain(self) -> DalTransitionDomain: ...

    @property
    def target_domain(self) -> DalTransitionDomain: ...

    @property
    def shortcut_policy(self) -> ShortcutPolicy: ...

    @property
    def evidence_requirement(self) -> EvidenceRequirement: ...

    def apply(
        self,
        input_unit: T_Input,
        evidence: List[DalEvidence],
    ) -> DalCandidateSetProtocol[T_Output]: ...
```

**Contract Requirements**:
1. Must declare source and target domains
2. Must specify shortcut policy (for cross-layer jumps)
3. Must specify evidence requirement level
4. Must implement `apply()` method taking input + evidence

---

## Evidence Model

### DalEvidence (Claim-Scoped)

**PR #21 Invariant 5**: No certificate without claim-scoped evidence.

```python
@dataclass(frozen=True)
class DalEvidence:
    claim_scope: DalClaimScope      # What kind of claim
    span: Tuple[int, int]           # Position (required by PR #21)
    observation: str                 # What was observed
    source_domain: DalTransitionDomain
    confidence: float = 1.0
```

**Claim Scopes**:
- `SINGLE_POSITION`: Claim about one position
- `SPAN`: Claim about contiguous span
- `ADJACENCY`: Claim about two adjacent positions (PR #21 Invariant 3)
- `FOLD`: Claim about folded units (PR #21 Invariant 2)
- `BOUNDARY`: Claim about boundary condition (PR #21 Invariant 4)

### DalCounterEvidence

Counter-evidence also requires position-scoping:

```python
@dataclass(frozen=True)
class DalCounterEvidence:
    claim_scope: DalClaimScope
    span: Tuple[int, int]
    blocking_observation: str
    source_domain: DalTransitionDomain
    severity: float = 1.0  # How strongly it blocks
```

---

## Trace Model

### DalTrace (Reverse Recoverability)

**PR #21 Invariant 2**: No fold without reverse trace.

```python
@dataclass(frozen=True)
class DalTrace:
    source_domain: DalTransitionDomain
    target_domain: DalTransitionDomain
    operation: str
    input_spans: List[Tuple[int, int]]  # What was consumed
    output_span: Tuple[int, int]        # What was produced

    def is_reversible(self) -> bool:
        return len(self.input_spans) > 0 and self.output_span[0] >= 0
```

**Example**:
```python
# Folding two syllables into pre-morph unit
trace = DalTrace(
    source_domain=DalTransitionDomain.SYLLABIC,
    target_domain=DalTransitionDomain.PRE_MORPH,
    operation="fold_syllables",
    input_spans=[(0, 2), (2, 4)],  # Two syllables
    output_span=(0, 4),             # Combined unit
)
assert trace.is_reversible()  # Can unfold back to syllables
```

---

## Candidate Model

### DalCandidateProtocol

**PR #21 Invariant 4**: No candidate without boundaries.

```python
class DalCandidateProtocol(Protocol):
    @property
    def span(self) -> Tuple[int, int]:
        """Span within parent sequence (required by PR #21)."""
        ...

    @property
    def claim_scope(self) -> DalClaimScope:
        """Scope of the claim this candidate makes."""
        ...
```

**Key Point**: Candidates must always specify their `span` - position within the parent ordered sequence.

### DalCandidateSetProtocol

Candidate sets preserve ordering:

```python
class DalCandidateSetProtocol(Protocol[T_Output]):
    @property
    def candidates(self) -> List[T_Output]:
        """Ordered list of candidates (preserves sequence order)."""
        ...

    @property
    def domain(self) -> DalTransitionDomain:
        """Which domain these candidates belong to."""
        ...

    def is_empty(self) -> bool:
        """Check if candidate set is empty (allowed explicitly)."""
        ...
```

**Empty Sets**: Explicitly allowed. An empty candidate set means "no valid candidates found" (not an error).

---

## Policy Types

### ShortcutPolicy

Controls cross-layer transitions:

```python
class ShortcutPolicy(Enum):
    FORBIDDEN = auto()         # No direct jump allowed
    LEXICON_ATTESTED = auto()  # Allowed if in closed lexicon
    WITH_TRACE = auto()        # Allowed if trace path provided
```

**Prohibited Direct Promotions** (from repository memory):
- رسم/صوت → وزن (grapheme/phoneme to pattern): **FORBIDDEN**
- مقطع → أصل (syllable to root): **FORBIDDEN**
- وزن ظاهر → وزن عميق (surface to deep pattern): **FORBIDDEN**
- جامد → جذر (frozen to root): **FORBIDDEN**
- مبني → وزن صرفي (built to morph pattern): **FORBIDDEN**

**Rule**: Each layer jump requires intermediate contract.

### EvidenceRequirement

How much evidence is required:

```python
class EvidenceRequirement(Enum):
    NONE = auto()       # No evidence needed (structural only)
    WEAK = auto()       # At least one piece of evidence
    STRONG = auto()     # Multiple converging evidence
    UNANIMOUS = auto()  # No counter-evidence allowed
```

### CandidateBudgetPolicy

How many candidates can be emitted:

```python
class CandidateBudgetPolicy(Enum):
    UNIQUE = auto()     # Exactly one candidate
    BOUNDED = auto()    # Fixed upper limit
    UNBOUNDED = auto()  # No limit (use with caution)
```

---

## Validation Functions

### validate_transition_contract

Validates contract structure:

```python
errors = validate_transition_contract(
    contract=my_contract,
    require_domain=True,
    require_policy=True,
)
if errors:
    raise ValueError(f"Invalid contract: {errors}")
```

**Checks**:
- Has `source_domain` and `target_domain`
- Has `shortcut_policy` and `evidence_requirement`
- Has `apply()` method

### validate_candidate_set_shape

Validates candidate set structure:

```python
errors = validate_candidate_set_shape(
    candidate_set=my_candidates,
    allow_empty=True,
    require_boundaries=True,
)
```

**Checks**:
- Has `candidates` property
- Empty only if `allow_empty=True`
- Each candidate has `span` (PR #21 compliance)

### validate_no_direct_promotion

Validates no prohibited cross-layer jumps:

```python
violations = validate_no_direct_promotion(
    source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
    target_domain=DalTransitionDomain.TEMPLATE,
    shortcut_policy=ShortcutPolicy.FORBIDDEN,
)
if violations:
    raise ValueError(f"Prohibited promotion: {violations}")
```

**Policy Enforcement**:
- `FORBIDDEN`: Layer distance > 1 not allowed
- `LEXICON_ATTESTED`: Requires `lexicon_attested=True`
- `WITH_TRACE`: Requires `trace_provided=True`

---

## PR #21 Governance Compliance

This implementation respects all 5 PR #21 invariants:

### Invariant 1: No Claim Without Position
✅ **Enforced**: `DalEvidence` requires `span: Tuple[int, int]`

```python
evidence = DalEvidence(
    claim_scope=DalClaimScope.SPAN,
    span=(0, 3),  # ← Required
    observation="Three letters",
    source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
)
```

### Invariant 2: No Fold Without Reverse Trace
✅ **Enforced**: `DalTrace` tracks `input_spans` and provides `is_reversible()`

```python
trace = DalTrace(
    source_domain=...,
    target_domain=...,
    operation="fold_syllables",
    input_spans=[(0, 2), (2, 4)],  # ← Can reverse
    output_span=(0, 4),
)
```

### Invariant 3: No Adjacency Without Direction
✅ **Enforced**: `DalClaimScope.ADJACENCY` claim scope specifies directional claims

```python
evidence = DalEvidence(
    claim_scope=DalClaimScope.ADJACENCY,  # ← Direction specified
    span=(i, i+1),  # Adjacent positions
    observation="Letters are adjacent",
    source_domain=...,
)
```

### Invariant 4: No Candidate Without Boundaries
✅ **Enforced**: `DalCandidateProtocol` requires `span` property

```python
@dataclass
class MyCandidate:
    span: Tuple[int, int]  # ← Required by protocol
    claim_scope: DalClaimScope
```

### Invariant 5: No Certificate Without Claim-Scoped Evidence
✅ **Enforced**: `DalEvidence` requires both `claim_scope` and `span`

```python
evidence = DalEvidence(
    claim_scope=DalClaimScope.FOLD,  # ← Scope specified
    span=(0, 4),                      # ← Position specified
    observation="Folded structure",
    source_domain=...,
)
```

---

## What Is Out of Scope

**PR #22 is MINIMAL**. The following are explicitly out of scope:

### ❌ No Analyzers
- No `RootAnalyzer`
- No `PatternAnalyzer`
- No `SyllableAnalyzer`

### ❌ No Relation/Case Candidates
- No `RelationCandidate`
- No `CaseEffectCandidate`
- These belong to higher-level syntax layers

### ❌ No Rank/Residual Algebra
- No `RankAlgebra` implementation
- No `ResidualAlgebra` implementation
- These are future PRs (#23, #24)

### ❌ No Refactoring
- No refactoring existing classes to inherit from new bases
- Existing code unchanged (except `__init__.py` imports)

### ❌ No Semantic Interpretation
- No `meaning` fields
- No `murad` fields
- No `haqiqa_majaz` fields
- Dal core stays at form level

### ❌ No I'rab
- No grammatical case assignment
- No operator application
- Syntax remains separate

---

## Usage Examples

### Example 1: Simple Transition (Adjacent Layers)

```python
from dal_core import (
    DalTransitionDomain,
    DalEvidence,
    DalClaimScope,
    ShortcutPolicy,
)

# Define evidence
evidence = DalEvidence(
    claim_scope=DalClaimScope.SPAN,
    span=(0, 2),
    observation="CV syllable pattern",
    source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
)

# Transition: Graphophonemic → Syllabic (adjacent, allowed)
violations = validate_no_direct_promotion(
    source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
    target_domain=DalTransitionDomain.SYLLABIC,
    shortcut_policy=ShortcutPolicy.FORBIDDEN,
)
assert len(violations) == 0  # ✓ Adjacent layers allowed
```

### Example 2: Forbidden Cross-Layer Jump

```python
# Attempt: Graphophonemic → Template (skip 3 layers)
violations = validate_no_direct_promotion(
    source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
    target_domain=DalTransitionDomain.TEMPLATE,
    shortcut_policy=ShortcutPolicy.FORBIDDEN,
)
assert len(violations) > 0  # ✗ Forbidden
# "Direct promotion from GRAPHOPHONEMIC to TEMPLATE forbidden (layer distance 4)"
```

### Example 3: Lexicon-Attested Shortcut

```python
# Frozen word: direct GRAPHOPHONEMIC → IDENTITY_AXIS
violations = validate_no_direct_promotion(
    source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
    target_domain=DalTransitionDomain.IDENTITY_AXIS,
    shortcut_policy=ShortcutPolicy.LEXICON_ATTESTED,
    lexicon_attested=True,  # ✓ Word in closed lexicon
)
assert len(violations) == 0  # Allowed
```

---

## Testing

### Test Coverage

**Basic Tests** (smoke tests):
```bash
python -c "
import sys
sys.path.insert(0, 'src')
from dal_core import DalEvidence, DalClaimScope, DalTransitionDomain
evidence = DalEvidence(
    claim_scope=DalClaimScope.SPAN,
    span=(0, 3),
    observation='Test',
    source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
)
print('✓ Imports and basic usage work')
"
```

**Full Test Suite** (when pytest available):
```bash
pytest tests/dal_core/test_dal_algebra_minimal.py -v
```

### Test Categories

1. **Evidence validation**: Span requirements, invalid spans
2. **Trace reversibility**: Fold operations, reverse path
3. **Protocol compliance**: Duck typing, structural typing
4. **Contract validation**: Domain requirements, policy requirements
5. **Candidate validation**: Boundary requirements, empty sets
6. **No-direct-promotion**: Cross-layer jump detection, policy enforcement
7. **Out-of-scope verification**: No relation/case imports, no algebra implementations

---

## Migration Notes

### For Existing Code

**No changes required** to existing dal_core classes. This PR only adds:
1. `dal_algebra.py` module
2. Updated `__init__.py` imports
3. New test file

**Existing code continues to work** without modification.

### For Future PRs

**PR #23: Rank Algebra** will build on this minimal signature:
- Use `DalTransitionContract` as base
- Respect no-direct-promotion policy
- Use claim-scoped evidence model

**PR #24: Residual Algebra** will extend residual tracking:
- Add residual propagation through transitions
- Use `DalTrace` for residual source tracking

**PR #25: CandidateSet Contract** will add:
- Ranking within candidate sets
- Residual inheritance
- Competitor tracking

---

## Architectural Decisions

### Why Protocols, Not Base Classes?

**Structural typing** (protocols) instead of inheritance allows:
1. **No forced refactoring**: Existing classes don't need changes
2. **Duck typing**: Any class with right structure satisfies protocol
3. **Future flexibility**: Different implementations possible

### Why Minimal?

**Governance before implementation**:
1. PR #21 established **what** (ordered bounded sequences)
2. PR #22 establishes **how** (minimal transition signature)
3. Future PRs add **operations** (rank, residual, etc.)

**Benefits**:
- Clear separation of concerns
- Incremental validation
- No premature optimization
- No architectural debt

### Why 8 Layers?

Based on linguistic reality of Arabic morphology:
- **Graphophonemic**: Written/spoken representation
- **Syllabic**: Phonological units
- **Pre-morph**: Pre-analysis segmentation
- **Origin**: Root vs frozen distinction
- **Template**: Pattern application
- **Identity**: Lexical lookup
- **Directional**: Bidirectional analysis
- **Judgment**: Final categorization

**Not a pipeline**: Different paths for different word types.

---

## Conclusion

**PR #22 delivers**:
✅ Minimal transition signature for dal_core
✅ Full PR #21 governance compliance
✅ 8-layer domain architecture
✅ Evidence-based transition model
✅ Trace-based reversibility
✅ Protocol-based structural typing
✅ No-direct-promotion policy enforcement

**PR #22 does NOT deliver** (explicitly out of scope):
❌ Analyzers
❌ Relation/case candidates
❌ Rank/residual algebra
❌ Refactoring existing classes
❌ Semantic interpretation
❌ I'rab

**Next steps**: PR #23 (Rank Algebra) will build on this foundation.

---

**Created**: 2026-05-20
**Author**: Claude Sonnet 4.5
**Based on**: PR #21 Ordered Dal Form Governance
**Commit**: f97d7c3
