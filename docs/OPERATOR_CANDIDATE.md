# OperatorCandidate (PR #17)

## Architecture Position

```
MufradProof
→ PreSyntaxMufradVector
→ SentenceFrameCandidate
→ CaseSignMatrix
→ OperatorTriggerPotential
→ NahwOperatorRegistry
→ OperatorCandidateSet                    ← THIS MODULE
    ↓
[future] RelationCandidate
      → CaseEffectCandidate
      → ParseCompetition
      → MurakkabProof
```

## Purpose

`OperatorCandidate` creates typed links between:
- `TriggerSource` (from `OperatorTriggerPotential`)
- `NahwOperatorEntry` (from `NahwOperatorRegistry`)

**This is NOT operator application. This is NOT relation creation. This is NOT case effect production.**

It is a candidate-linking layer that preserves all competing (source, entry) pairs without resolution.

## What OperatorCandidate IS

✅ **Allowed:**
- Creates typed `(TriggerSource, NahwOperatorEntry)` pairs
- Preserves ALL competing trigger families
- Preserves ALL competing registry entries
- Inherits residuals from trigger → matrix → frame chain
- Enforces rank ceiling: `candidate.rank ≤ min(trigger.rank, lookup.rank, entry.rank)`
- Records trace linking back to trigger source and registry entry

## What OperatorCandidate IS NOT

❌ **Forbidden:**
- Does NOT apply operators
- Does NOT produce relations (ISN/TADMN/TAQYID)
- Does NOT produce case effects (raf'/nasb/jarr/jazm)
- Does NOT assign syntax roles (فاعل/مفعول/مبتدأ/خبر/مضاف/مضاف إليه)
- Does NOT infer semantic meaning (معنى/مراد/مدلول/حقيقة/مجاز)
- Does NOT contain methods: `apply()`, `bind()`, `resolve()`, `governs()`, `produces_relation()`, `produces_case()`

## Core Types

### OperatorCandidateTrace

Links candidate back to its sources:
- `trigger_id`: from `OperatorTriggerPotential`
- `trigger_source_vector_id`: from specific `TriggerSource`
- `registry_entry_id`: from `NahwOperatorEntry`
- `frame_id`, `matrix_id`: chain provenance

### OperatorCandidate

Single `(TriggerSource, NahwOperatorEntry)` pair:
- `trigger_source`: Specific trigger source this candidate is tied to
- `registry_entry`: Registry entry this candidate links to
- `rank`: `≤ min(trigger.rank, lookup.rank, entry.rank)`
- `inherited_residuals`: From trigger (includes matrix, frame, etc.)
- `candidate_residuals`: Candidate-specific (e.g., rank ceiling violations)
- `trace`: Links back to sources

**Key invariant:** `trigger_source.family == registry_entry.family`

### OperatorCandidateSet

Complete set of all candidates for a trigger:
- `candidates`: All `(TriggerSource, RegistryEntry)` pairs
- `competitors_preserved`: `True` when multiple candidates exist
- `rank`: `≤ min(candidate.rank)` if candidates exist, else `≤ trigger.rank`
- `inherited_residuals`: From trigger
- `candidate_set_residuals`: Set-specific (e.g., no entries, competition)

## Builder Function

```python
def build_operator_candidates(
    trigger: OperatorTriggerPotential,
    registry: NahwOperatorRegistry,
) -> OperatorCandidateSet
```

**Rules:**
1. Accepts only `OperatorTriggerPotential` and `NahwOperatorRegistry`
2. Uses `registry.entries_for_trigger(trigger)` for lookup
3. Creates one `OperatorCandidate` per `(TriggerSource, RegistryEntry)` pair where `source.family == entry.family`
4. Preserves all competing entries (no resolution)
5. Preserves all competing trigger families (no suppression)
6. If trigger family has no entries: `candidates=()` + residual
7. Rank ceiling enforced at candidate and set levels
8. Residual inheritance preserved
9. No candidate may erase registry lookup residuals

## Usage Example

```python
from dal_core import (
    build_sentence_frames,
    build_case_sign_matrix,
    build_operator_trigger_potential,
    build_default_nahw_operator_registry,
    build_operator_candidates,
)

# From prior layers
frame = build_sentence_frames(vectors)[0]
matrix = build_case_sign_matrix(frame)
trigger = build_operator_trigger_potential(frame, matrix)

# Create registry
registry = build_default_nahw_operator_registry()

# Build candidates
candidate_set = build_operator_candidates(trigger, registry)

# Inspect candidates
print(f"Candidates: {len(candidate_set.candidates)}")
print(f"Competition preserved: {candidate_set.competitors_preserved}")

for candidate in candidate_set.candidates:
    print(f"  {candidate.trigger_source.family.value} → {candidate.registry_entry.operator_id}")
    print(f"    Rank: {candidate.rank.name}")
```

## Competition Preservation

Key behavior:
- If family has 2 trigger sources and 3 registry entries → 6 candidates
- All preserved, no "best" choice
- `candidates[i].competitors_preserved = True`
- Resolution deferred to future `ParseCompetition` layer

## Empty Candidate Sets

When trigger family has no registry entries:
- `candidates = ()`
- `OPERATOR_CANDIDATE_NO_REGISTRY_ENTRIES` residual emitted
- `rank ≤ trigger.rank` (not `min([])`)
- Trace still points to trigger

## Rank Ceiling

Candidate rank never exceeds:
```
min(trigger.rank, lookup_result.rank, registry_entry.rank)
```

Candidate set rank never exceeds:
```
min(candidate.rank for candidate in candidates) if candidates else trigger.rank
```

## Residual Inheritance

Candidate inherits all residuals from:
- Trigger (includes matrix, frame, mufrad chain)
- Lookup result (registry-specific info/warnings)

Candidate set inherits trigger residuals.

## Residual Types

New residuals (PR #17):
- `OPERATOR_CANDIDATE_REQUIRES_TRIGGER_AND_REGISTRY`
- `OPERATOR_CANDIDATE_RANK_CEILING_VIOLATION`
- `OPERATOR_CANDIDATE_RESIDUAL_INHERITANCE_VIOLATION`
- `OPERATOR_CANDIDATE_NO_REGISTRY_ENTRIES`
- `OPERATOR_CANDIDATE_COMPETITION_PRESERVED`
- `OPERATOR_CANDIDATE_TRACE_MISSING`

## Allowed Claims

✅ **You MAY say:**
> "dal_core can create typed OperatorCandidate links from trigger sources and registry entries while preserving all competing candidates."

## Forbidden Claims

❌ **You MUST NOT say:**
> "dal_core applies nahw operators."
> "dal_core produces relations."
> "dal_core produces case effects."
> "dal_core performs i'rab (إعراب)."
> "dal_core assigns syntax roles."
> "dal_core infers semantic meaning."

## Out of Scope (NOT in this PR)

Future PRs will add:
- `RelationCandidate` (relation type candidates)
- `CaseEffectCandidate` (case effect candidates)
- `ParseCompetition` (candidate resolution)
- `MurakkabProof` (composite proof)
- Operator application logic
- I'rab (إعراب) judgments
- Semantic meaning inference

## Testing

Tests verify:
- Input typing (requires trigger + registry)
- All trigger families preserved
- All registry entries preserved
- (Source, entry) pairing with family matching
- Empty registry handling
- Rank ceiling enforcement
- Residual inheritance
- Trace completeness
- No forbidden fields
- No forbidden methods
- Immutability
- Competition flags

## Summary

`OperatorCandidate` is the typed candidate-linking layer between `OperatorTriggerPotential` and (future) `RelationCandidate`. It creates `(TriggerSource, RegistryEntry)` pairs, preserves all competition, enforces rank ceilings, and maintains residual inheritance—all without applying operators, producing relations, or making grammatical judgments.
