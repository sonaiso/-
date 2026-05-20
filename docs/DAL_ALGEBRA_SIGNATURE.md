# Dal Algebra Signature (F1)

**Status**: Foundation PR #21
**Created**: 2026-05-20
**Purpose**: Establish foundational typed transition contract for all dal_core stages

---

## Executive Summary

The project is moving from **local pipeline stages** to a **Typed Guarded Residual Candidate Algebra**.

This document defines **F1: Dal Algebra Signature**, the lightweight protocol layer that establishes:
- Type signatures for inputs and outputs
- Evidence trail requirements
- Rank constraint propagation
- Residual preservation
- Trace provenance
- Candidate set operations
- Forbidden output detection

**Key Principle**: Every dal_core stage transition must be a well-typed, auditable, residual-preserving transformation.

---

## Context: Why F1 Now?

PR #20 corrected the architectural scope of D_mufrad:
- Layers 6–10 are **not outside D_mufrad** absolutely
- They are out of scope as **generation** and **semantic interpretation**
- They are **in scope** as **analytic form-feature recognition**

This scope correction means we need more than just new layers—we need a **general law governing all layers**.

F1 provides that law: a **minimal, non-invasive protocol** that all future transitions should follow.

---

## Mathematical Idea

Every dal_core transformation is a typed transition:

```text
μᵢ : InputType × Optional[Guard/Registry] → CandidateSet[OutputType]
```

Each transition `μᵢ` must expose:

| Field | Type | Purpose |
|-------|------|---------|
| `input_type` | Type specification | What this stage consumes |
| `output_type` | Type specification | What this stage produces |
| `evidence` | Evidence trail | Why this transformation was performed |
| `rank` | LughaRank constraint | Attestation level ceiling |
| `residuals` | Residual set | Issues/warnings/blockers propagated |
| `trace` | Transformation provenance | Full derivation history |
| `competitors` | Alternative candidates | Competing hypotheses preserved |
| `forbidden_outputs` | Stage-specific prohibitions | What must NOT appear at this stage |

---

## Core Components

### 1. Typed Input/Output Contracts

```python
@dataclass(frozen=True)
class DalTypedInput:
    input_type_name: str  # e.g., "MufradProof"
    source_stage: str     # e.g., "mufrad_proof"

    def get_type_signature(self) -> str:
        return f"{self.source_stage}::{self.input_type_name}"

@dataclass(frozen=True)
class DalTypedOutput:
    output_type_name: str  # e.g., "OperatorCandidate"
    target_stage: str      # e.g., "operator_candidate"

    def get_type_signature(self) -> str:
        return f"{self.target_stage}::{self.output_type_name}"
```

**Purpose**: Every stage declares what it consumes and what it produces.

---

### 2. Evidence Trail

```python
@dataclass(frozen=True)
class DalEvidence:
    transformation_type: str         # e.g., "syllabification"
    evidence_chain: tuple[Evidence, ...]  # Supporting evidence from lower layers
```

**Purpose**: Track why each transformation was performed, with chain of supporting evidence.

---

### 3. Transformation Trace

```python
@dataclass(frozen=True)
class DalTrace:
    stage_name: str              # Which stage performed this
    input_signature: str         # Type signature of input
    output_signature: str        # Type signature of output
    transformation_id: str       # Unique ID for this transformation
    parent_trace_id: Optional[str]  # Parent trace for chaining

    def get_trace_path(self) -> str:
        if self.parent_trace_id:
            return f"{self.parent_trace_id} → {self.transformation_id}"
        return self.transformation_id
```

**Purpose**: Full provenance trail allowing reverse trace from output to input.

---

### 4. Transition Guards

```python
@dataclass(frozen=True)
class DalTransitionGuard:
    guard_type: str      # e.g., "input_validation", "rank_ceiling"
    condition: str       # Human-readable condition
    required: bool = True  # Mandatory vs advisory
```

**Purpose**: Precondition/postcondition checks for transitions.

---

### 5. Forbidden Outputs

```python
@dataclass(frozen=True)
class DalForbiddenOutput:
    forbidden_field_names: frozenset[str]  # e.g., {"meaning", "semantic"}
    stage_name: str                        # Which stage these apply to
    reason: str                            # Why forbidden

    def contains_forbidden_field(self, field_name: str) -> bool: ...
    def get_violation_message(self, field_name: str) -> str: ...
```

**Purpose**: Stage-specific prohibition of semantic/syntactic fields.

**Example**:
```python
mufrad_forbidden = DalForbiddenOutput(
    forbidden_field_names=frozenset({
        "meaning", "semantic", "murad", "madlul",
        "case_effect", "relation", "syntax_role"
    }),
    stage_name="mufrad_proof",
    reason="D_mufrad is pre-syntax, pre-semantics"
)
```

---

### 6. Transition Contract

```python
@dataclass(frozen=True)
class DalTransitionContract:
    input_type: DalTypedInput
    output_type: DalTypedOutput
    stage_name: str
    rank_constraint: Optional[LughaRank] = None
    forbidden_outputs: tuple[DalForbiddenOutput, ...] = ()
    guards: tuple[DalTransitionGuard, ...] = ()
    evidence_required: bool = True
    trace_required: bool = True
    competitors_allowed: bool = True

    def validate_contract(self) -> tuple[bool, list[str]]: ...
    def get_contract_signature(self) -> str: ...
```

**Purpose**: Complete specification of what a stage must provide.

---

### 7. Candidate Set Protocol

```python
class DalCandidateSetProtocol(Protocol[OutputT]):
    def get_candidates(self) -> tuple[OutputT, ...]: ...
    def get_rank(self) -> LughaRank: ...
    def get_residuals(self) -> tuple[Residual, ...]: ...
    def get_trace(self) -> DalTrace: ...
    def get_competitors(self) -> tuple[OutputT, ...]: ...
    def is_empty(self) -> bool: ...
    def has_residuals(self) -> bool: ...
```

**Purpose**: Standard interface for all candidate sets, regardless of layer.

---

### 8. Transition Protocol

```python
class DalTransitionProtocol(Protocol[InputT, OutputT]):
    def get_contract(self) -> DalTransitionContract: ...
    def apply(self, input_obj: InputT, **kwargs) -> DalCandidateSetProtocol[OutputT]: ...
```

**Purpose**: Standard interface for stage transformations.

---

## Validation Helpers

### 1. validate_transition_contract

```python
def validate_transition_contract(contract: DalTransitionContract) -> None:
    """Validate contract is well-formed. Raises ValueError if invalid."""
```

### 2. validate_candidate_set_shape

```python
def validate_candidate_set_shape(
    candidate_set: DalCandidateSetProtocol[Any],
    allow_empty: bool = True
) -> None:
    """
    Validate candidate set shape:
    - Empty sets allowed (if allow_empty=True)
    - No None candidates
    - All required methods present
    """
```

### 3. ensure_no_forbidden_outputs

```python
def ensure_no_forbidden_outputs(
    obj: Any,
    forbidden_outputs: tuple[DalForbiddenOutput, ...],
    stage_name: str
) -> None:
    """Ensure object does not contain forbidden field names. Raises ValueError if violated."""
```

---

## Invariants

F1 establishes these **non-negotiable invariants**:

1. ✅ **Every transition has typed input and typed output**
2. ✅ **Every candidate set preserves competitors**
3. ✅ **No candidate set has fake `None` candidates**
4. ✅ **Empty candidate sets are allowed but must be explicit**
5. ✅ **Rank is present but rank algebra is not implemented here** (F2)
6. ✅ **Residuals are present but residual algebra is not implemented here** (F3)
7. ✅ **Trace is present but detailed trace algebra is not implemented here**
8. ✅ **Forbidden outputs are declared per stage**
9. ✅ **No semantic meaning is introduced**
10. ✅ **No syntax relation or case effect is introduced**

---

## What F1 Does NOT Do

F1 is a **minimal protocol layer**. It does NOT:

❌ Implement full rank algebra (see F2)
❌ Implement full residual algebra (see F3)
❌ Force CandidateSet base inheritance migration (see F4)
❌ Implement NoMeaning scanner (see F5)
❌ Implement RelationCandidate
❌ Implement CaseEffectCandidate
❌ Refactor existing MufradProof, OperatorCandidate, or other classes

**Key Design Decision**: F1 uses **protocols** and **validation helpers**, not base classes.

Existing classes do NOT need to inherit from F1 types. They can continue as-is, and gradually adopt the protocol through duck typing.

---

## Usage Examples

### Example 1: Defining a Transition Contract

```python
from dal_core.dal_algebra import (
    DalTypedInput,
    DalTypedOutput,
    DalTransitionContract,
    DalForbiddenOutput,
    validate_transition_contract,
)
from dal_core.ranks import LughaRank

# Define contract for syllabifier
syllabifier_contract = DalTransitionContract(
    input_type=DalTypedInput(
        input_type_name="AtomSequence",
        source_stage="atom_builder"
    ),
    output_type=DalTypedOutput(
        output_type_name="SyllableCandidate",
        target_stage="syllabifier"
    ),
    stage_name="syllabifier",
    rank_constraint=LughaRank.FORM,
    forbidden_outputs=(
        DalForbiddenOutput(
            forbidden_field_names=frozenset({"meaning", "semantic"}),
            stage_name="syllabifier",
            reason="Syllabification is pre-semantic"
        ),
    ),
    evidence_required=True,
    trace_required=True,
)

# Validate contract
validate_transition_contract(syllabifier_contract)
print(syllabifier_contract.get_contract_signature())
# Output: "syllabifier: atom_builder::AtomSequence → syllabifier::SyllableCandidate"
```

### Example 2: Creating a Candidate Set

```python
from dataclasses import dataclass
from dal_core.dal_algebra import DalTrace, validate_candidate_set_shape
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual

@dataclass(frozen=True)
class SyllableCandidate:
    syllable_type: str
    cv_pattern: str

@dataclass(frozen=True)
class SyllableCandidateSet:
    candidates: tuple[SyllableCandidate, ...]
    rank: LughaRank
    residuals: tuple[Residual, ...]
    trace: DalTrace

    def get_candidates(self) -> tuple[SyllableCandidate, ...]:
        return self.candidates

    def get_rank(self) -> LughaRank:
        return self.rank

    def get_residuals(self) -> tuple[Residual, ...]:
        return self.residuals

    def get_trace(self) -> DalTrace:
        return self.trace

    def get_competitors(self) -> tuple[SyllableCandidate, ...]:
        return self.candidates

# Create instance
candidate_set = SyllableCandidateSet(
    candidates=(
        SyllableCandidate(syllable_type="CV", cv_pattern="كَ"),
        SyllableCandidate(syllable_type="CVC", cv_pattern="كَتْ"),
    ),
    rank=LughaRank.FORM,
    residuals=(),
    trace=DalTrace(
        stage_name="syllabifier",
        input_signature="atom_builder::AtomSequence",
        output_signature="syllabifier::SyllableCandidate",
        transformation_id="syll_001"
    )
)

# Validate shape
validate_candidate_set_shape(candidate_set)
```

### Example 3: Forbidden Output Detection

```python
from dal_core.dal_algebra import DalForbiddenOutput, ensure_no_forbidden_outputs

# Define forbidden outputs for MufradProof stage
mufrad_forbidden = DalForbiddenOutput(
    forbidden_field_names=frozenset({
        "meaning", "semantic", "murad", "madlul",
        "case_effect", "relation", "syntax_role",
        "faail", "mafool", "mubtada", "khabar"
    }),
    stage_name="mufrad_proof",
    reason="D_mufrad is pre-syntax, pre-semantics"
)

# Valid object
@dataclass
class ValidMufradOutput:
    root_candidates: tuple = ()
    wazn_candidates: tuple = ()

valid_obj = ValidMufradOutput()
ensure_no_forbidden_outputs(valid_obj, (mufrad_forbidden,), "mufrad_proof")  # ✅ Passes

# Invalid object
@dataclass
class InvalidMufradOutput:
    root_candidates: tuple = ()
    meaning: str = "forbidden!"  # ❌ Forbidden field

invalid_obj = InvalidMufradOutput()
# ensure_no_forbidden_outputs(invalid_obj, (mufrad_forbidden,), "mufrad_proof")
# Raises ValueError: Forbidden outputs detected
```

---

## Integration Path

### Phase 1: Foundation (Current PR)

✅ **F1: Dal Algebra Signature** (this PR)
- Define protocols and types
- Add validation helpers
- Document usage patterns
- **Do NOT refactor existing classes**

### Phase 2: Algebra Extensions (Future PRs)

⏳ **F2: Rank Algebra**
- Formalize rank operations (ceiling, floor, propagation)
- Define rank constraint satisfaction
- Implement rank violation detection

⏳ **F3: Residual Algebra**
- Define residual classification taxonomy
- Establish residual propagation rules
- Implement residual set operations

⏳ **F4: CandidateSet Contract**
- Unified base contract for all candidate sets
- Standard trace structure
- Standard set operations interface

⏳ **F5: Stage-aware NoMeaning Invariant**
- Formalize prohibition on meaning fields at each stage
- Compile-time and runtime enforcement mechanisms

### Phase 3: Early-Layer Analytic Contracts (Future PRs)

After F1-F5, implement analytic contracts for:
- E1: Carrier/Normalization → `CarrierCandidateSet`
- E2: AtomCandidate → `AtomCandidateSet`
- E3: SyllableCandidate → `SyllableCandidateSet`
- ...and more (see LAYER_COVERAGE_ANALYSIS.md)

---

## Compliance Check

Any code using F1 must satisfy:

### Prohibition Check
- [ ] Does not force existing classes to inherit from new base classes?
- [ ] Does not import relation/case_effect concepts?
- [ ] Does not introduce semantic meaning fields?

### Requirement Check
- [ ] Provides typed input/output specifications?
- [ ] Includes evidence trail and trace?
- [ ] Declares forbidden outputs for stage?
- [ ] Validates candidate set shape?

---

## Allowed Claims After This PR

After F1 is merged, we can claim:

✅ **dal_core has a formal lightweight algebra signature for future typed transitions**

### Forbidden Claims

We **cannot** claim after this PR:

❌ dal_core has a full rank algebra (that's F2)
❌ dal_core has a full residual algebra (that's F3)
❌ dal_core can build RelationCandidate (that's Phase 3)
❌ dal_core performs syntax or i'rab (that's post-MufradProof)

---

## Testing

All tests are in `tests/dal_core/test_dal_algebra_signature.py`.

Required test coverage:

1. ✅ `test_transition_contract_requires_input_and_output_types`
2. ✅ `test_transition_contract_requires_rank_residual_trace_fields`
3. ✅ `test_candidate_set_shape_allows_empty_set`
4. ✅ `test_candidate_set_shape_rejects_none_candidates`
5. ✅ `test_forbidden_outputs_detect_forbidden_field_names`
6. ✅ `test_forbidden_outputs_allow_stage_specific_allowed_names`
7. ✅ `test_protocol_does_not_force_existing_classes_to_inherit`
8. ✅ `test_dal_algebra_signature_does_not_import_relation_or_case_effect`

Run tests:
```bash
pytest tests/dal_core/test_dal_algebra_signature.py -v
```

---

## References

### Related Documentation
- `docs/LAYER_COVERAGE_ANALYSIS.md` - PR #20 scope correction
- `docs/DAL_CORE_MUFRAD_PROOF.md` - MufradProof structure
- `docs/OPERATOR_CANDIDATE.md` - OperatorCandidate (PR #17)
- `src/dal_core/dal_algebra.py` - Implementation

### Related PRs
- PR #20: Correct layer coverage analysis (generative vs analytic scope)
- PR #21: **This PR** - F1 Dal Algebra Signature

---

## Conclusion

**F1 establishes the minimal typed transition contract** that all dal_core stages should follow.

It is:
- ✅ **Lightweight** (protocols, not base classes)
- ✅ **Non-invasive** (no refactoring of existing classes required)
- ✅ **Auditable** (evidence, trace, residual preservation)
- ✅ **Type-safe** (typed input/output signatures)
- ✅ **Stage-aware** (forbidden outputs per stage)

After F1, we can build:
- F2-F5: Extended algebras (rank, residual, candidate set, no-meaning)
- E1-E12: Early-layer analytic contracts
- Phase 3: Composition layer (RelationCandidate, CaseEffectCandidate)

**The foundation is now in place for a rigorous, typed, auditable dal_core architecture.**

---

**Document Changelog**:
- 2026-05-20: Initial creation (PR #21) - F1 Dal Algebra Signature
