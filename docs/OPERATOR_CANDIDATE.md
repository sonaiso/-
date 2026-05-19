# OperatorCandidate (PR #17)

**Status**: Implemented
**Layer**: Post-Registry, Pre-Relation
**Purpose**: Typed candidate links between trigger sources and registry entries

---

## Architecture Position

```
SentenceFrameCandidate + CaseSignMatrix
        ↓
OperatorTriggerPotential (PR #14)
        ↓
NahwOperatorRegistry (PR #15)
        ↓
OperatorCandidate (PR #17 — THIS MODULE)
        ↓
[Future] RelationCandidate → CaseEffectCandidate
```

---

## Core Principle

**OperatorCandidate is a typed LINK, never an application.**

It creates structured connections between:
- **TriggerSource** (from OperatorTriggerPotential)
- **NahwOperatorEntry** (from NahwOperatorRegistry)

It **NEVER**:
- Applies an operator
- Produces a relation (ISN/TADMN/TAQYID)
- Produces a CaseEffect
- Assigns syntax roles (faail/mafool/mubtada/khabar)
- Asserts meaning (meaning/murad/madlul)

---

## Key Structures

### 1. OperatorCandidateTrace

Trace for a single operator candidate:

```python
@dataclass(frozen=True)
class OperatorCandidateTrace:
    candidate_id: str
    trigger_source_vector_id: str
    registry_entry_id: str
    trigger_id: str
    frame_id: str
    matrix_id: str
    family: OperatorTriggerFamily
    derivation: str = "from_trigger_source_and_registry_entry"
```

**Guarantees**:
- Complete traceability back to trigger source and registry entry
- Immutable after creation
- Validates all required ids are non-empty

---

### 2. OperatorCandidate

Single typed candidate link:

```python
@dataclass(frozen=True)
class OperatorCandidate:
    candidate_id: str
    trigger_source: TriggerSource
    registry_entry: NahwOperatorEntry
    family: OperatorTriggerFamily
    rank: LughaRank
    residuals: tuple[Residual, ...]
    trace: OperatorCandidateTrace
```

**Invariants Enforced**:
1. **Family matching**: `trigger_source.family == registry_entry.family == candidate.family`
2. **Rank ceiling**: `candidate.rank ≤ registry_entry.rank`
3. **No forbidden fields**: Validates against semantic/syntactic field leakage
4. **Trace integrity**: `trace.candidate_id == candidate.candidate_id`

---

### 3. OperatorCandidateSetTrace

**Dedicated trace for the entire set** (not reusing a single candidate trace!):

```python
@dataclass(frozen=True)
class OperatorCandidateSetTrace:
    set_id: str
    candidate_ids: tuple[str, ...]           # ALL candidate ids
    trigger_source_vector_ids: tuple[str, ...]  # ALL source vector ids
    registry_entry_ids: tuple[str, ...]      # ALL entry ids
    families: tuple[OperatorTriggerFamily, ...]  # ALL families
    trigger_id: str
    frame_id: str
    matrix_id: str
    derivation: str = "from_operator_trigger_and_registry"
```

**Critical Design Decision**:
- OperatorCandidateSetTrace is INDEPENDENT
- It preserves ALL candidate ids, trigger source vector ids, and registry entry ids
- It does NOT just point to the first candidate's trace
- All tuples must have the same length (validated in `__post_init__`)

---

### 4. OperatorCandidateSet

Container for all competing candidates:

```python
@dataclass(frozen=True)
class OperatorCandidateSet:
    set_id: str
    candidates: tuple[OperatorCandidate, ...]
    set_trace: OperatorCandidateSetTrace
    inherited_residuals: tuple[Residual, ...]
    candidate_set_residuals: tuple[Residual, ...]

    def get_all_residuals(self) -> tuple[Residual, ...]:
        """Aggregate ALL residuals across hierarchy"""
        # inherited + set-level + all candidate residuals
```

**Key Method**: `get_all_residuals()`

This method MUST aggregate:
1. `inherited_residuals` (from trigger + registry path)
2. `candidate_set_residuals` (local to set construction)
3. All residuals from EVERY OperatorCandidate in the set

**Invariants Enforced**:
1. **No fake candidates**: `None` in candidates tuple raises ValueError
2. **Trace completeness**: Set trace must reference all candidates
3. **No forbidden fields**: Validates against semantic/syntactic leakage
4. **Competition preservation**: Multiple candidates is normal and expected

---

## Rank Ceiling Semantics

### Normal Rank Lowering (CEILED)

When candidate rank is lowered to match the weaker of trigger/registry:

```python
ResidualType.OPERATOR_CANDIDATE_RANK_CEILED
```

**Example**:
- Trigger rank: SAMA (3)
- Registry entry rank: FORM (1)
- Candidate rank: FORM (1) ← lowered to ceiling
- Residual: `OPERATOR_CANDIDATE_RANK_CEILED` (INFO)

### Illegal Rank Elevation (VIOLATION)

When candidate rank is illegally set higher than registry entry rank:

```python
ResidualType.OPERATOR_CANDIDATE_RANK_CEILING_VIOLATION
```

**Example**:
- Registry entry rank: FORM (1)
- Candidate rank: SAMA (3) ← VIOLATION!
- Raises `ValueError` in `__post_init__`

**Key Distinction**:
- **CEILED** = normal behavior (rank lowering due to ceiling)
- **VIOLATION** = error condition (illegal rank elevation)

---

## Builder Pattern

### OperatorCandidateBuilder

Builds OperatorCandidateSet from OperatorTriggerPotential + NahwOperatorRegistry:

```python
builder = OperatorCandidateBuilder()
candidate_set = builder.build(trigger, registry)
```

**Algorithm**:
1. For each TriggerSource in trigger.sources:
   - Lookup matching registry entries by family
   - Create OperatorCandidate for each (source, entry) pair
2. Preserve ALL candidates (no resolution)
3. Build dedicated set trace with ALL ids
4. Inherit residuals from trigger
5. Return OperatorCandidateSet

**Guarantees**:
- All (TriggerSource × NahwOperatorEntry) pairs where families match
- No competition resolution
- No candidate invention when registry has no entries

---

## Residual Types (PR #17)

New residuals added to `ResidualType` enum:

```python
# Normal operations
OPERATOR_CANDIDATE_RANK_CEILED = "تعليق رتبة مرشح عامل"
OPERATOR_CANDIDATE_COMPETING_PRESERVED = "مرشحو عوامل متنافسون محفوظون"

# Errors
OPERATOR_CANDIDATE_RANK_CEILING_VIOLATION = "خرق سقف رتبة مرشح عامل"
OPERATOR_CANDIDATE_FAMILY_MISMATCH = "عدم تطابق عائلة المرشح"
OPERATOR_CANDIDATE_NO_REGISTRY_ENTRY = "مرشح عامل بلا مدخل سجل"
OPERATOR_CANDIDATE_REQUIRES_TRIGGER_AND_REGISTRY = "مرشح العامل يتطلب محفزًا وسجلاً"
OPERATOR_CANDIDATE_TRIGGER_REGISTRY_MISMATCH = "عدم تطابق المحفز والسجل في مرشح العامل"
```

---

## Forbidden Fields Guard

All OperatorCandidate structures are validated against forbidden semantic/syntactic fields:

**Forbidden**:
- `operator_binding`, `operator_application`, `operator_id_resolved`
- `relation`, `relation_type`, `relation_candidate`
- `case_effect`, `case_effect_candidate`
- `syntax_role`, `faail`, `mafool`, `mubtada`, `khabar`, `mudaf`, `mudaf_ilayh`
- `meaning`, `semantic`, `madlul`, `murad`, `haqiqa`, `majaz`

Any presence of these fields raises `ValueError` with clear error message.

---

## Usage Example

```python
from dal_core.operator_candidate import OperatorCandidateBuilder
from dal_core.operator_trigger import OperatorTriggerPotential
from dal_core.nahw_operator_registry import build_default_nahw_operator_registry

# Build trigger potential (from frame + matrix)
trigger = build_trigger_potential(frame, matrix)

# Get registry
registry = build_default_nahw_operator_registry()

# Build operator candidates
builder = OperatorCandidateBuilder()
candidate_set = builder.build(trigger, registry)

# Access candidates
for candidate in candidate_set.candidates:
    print(f"Candidate {candidate.candidate_id}")
    print(f"  Family: {candidate.family}")
    print(f"  Rank: {candidate.rank}")
    print(f"  Trigger source: {candidate.trigger_source.vector_id}")
    print(f"  Registry entry: {candidate.registry_entry.operator_id}")

# Check residuals (aggregated across hierarchy)
all_residuals = candidate_set.get_all_residuals()
if candidate_set.has_blocking_residuals():
    print("Set has blocking residuals")
```

---

## Testing

Comprehensive test suite in `tests/dal_core/test_operator_candidate.py`:

**Test Groups**:
- A. OperatorCandidateSetTrace preserves ALL candidate/trigger/registry ids
- B. get_all_residuals aggregates across hierarchy
- C. Rank ceiling semantics (CEILED vs VIOLATION)
- D. Family matching enforcement
- E. Competition preservation
- F. Empty set safety
- G. No fake candidates
- H. Forbidden fields guard

**Total**: 11 tests, all passing

**Run**:
```bash
PYTHONPATH=src pytest tests/dal_core/test_operator_candidate.py -v
```

---

## Hardening Features (from start)

PR #17 was implemented with hardening requirements from the beginning:

### 1. Dedicated Set Trace
- ✅ OperatorCandidateSetTrace is independent
- ✅ Preserves ALL candidate ids, trigger source vector ids, registry entry ids
- ✅ Does NOT reuse a single candidate trace
- ✅ Validates tuple lengths match

### 2. Complete Residual Aggregation
- ✅ `get_all_residuals()` includes inherited + set-level + all candidate residuals
- ✅ Deduplication while preserving order
- ✅ Validated by test

### 3. Rank Ceiling Semantics
- ✅ `OPERATOR_CANDIDATE_RANK_CEILED` for normal lowering
- ✅ `OPERATOR_CANDIDATE_RANK_CEILING_VIOLATION` only for illegal elevation
- ✅ Clear distinction in semantics and usage

---

## What Comes Next

After PR #17 merges, **do NOT start RelationCandidate immediately**.

Instead, build foundation PRs:

1. **F1**: Dal Algebra Signature
2. **F2**: Rank Algebra
3. **F3**: Residual Algebra
4. **F4**: CandidateSet Base Contract
5. **F5**: Stage-aware NoMeaning Invariant

Only after these foundations should RelationCandidate begin.

---

## Allowed Claims (Post-PR #17)

✅ **ALLOWED**:
- "dal_core can create typed OperatorCandidate links from trigger sources and registry entries"
- "dal_core preserves all competing candidates"
- "dal_core maintains rank ceiling and residual inheritance"

❌ **FORBIDDEN**:
- "dal_core applies operators"
- "dal_core creates relations"
- "dal_core creates case effects"
- "dal_core performs i'rab"
- "dal_core understands meaning"

---

**End of OperatorCandidate Documentation**
