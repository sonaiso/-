# PreMeaning Dataset Schema for GARA-T5

**PR #135** | Created: 2026-05-28 | Status: Schema Complete

---

## Constitutional Purpose

Define dataset contracts for training GARA-T5 on **ALGEBRAIC PRE-MEANING TRACES**, NOT on final meanings, relations, ifādah, or hukm.

### Critical Distinction

```
Dataset Target = algebraic_trace_output
Dataset Target ≠ semantic_output
```

---

## T5 Learning Target

```
classified input
→ licensed operation
→ cause geometry
→ trace
→ residual
→ rank
→ stop gate
```

**NOT**:
```
→ meaning
→ relation
→ ifādah
→ hukm
```

---

## Constitutional Laws (10 Laws)

1. **Dataset target = algebraic_trace_output** (NOT semantic_output)
2. **NO** meaning, translation, syntax_role, relation_candidate, ifādah, hukm
3. **SurfaceInverse** examples MUST forbid certainty
4. **TraceInverse** certainty REQUIRES: injective OR carries_preimage
5. **All examples** MUST have residuals and rank
6. **All examples** MUST have `stop_before_meaning = True`
7. **Dataset** uses existing `Rank` and `Residual` types
8. **CauseGeometry** MUST include all 4 Aristotelian causes
9. **Trace** MUST NOT contain semantic keys (meaning, ifadah, hukm)
10. **forbidden_outputs** MUST be explicitly declared

---

## Six Schema Types

### 1. PreMeaningTrainingExample (Base)

**Purpose**: Base schema for all training examples

**Required Fields**:
- `example_id`: Unique identifier
- `example_type`: Schema type
- `input_surface`: Surface form
- `input_classification`: Input type
- `operation_name`: Operation identifier
- `operation_spec_reference`: Reference to OperationSpec
- `cause_geometry`: Complete CauseGeometryDataset
- `before_state`, `after_state`, `invariant`
- `trace`: Immutable mapping (no semantic keys)
- `residuals`: FrozenSet of (type, severity, message) tuples
- `rank`: Rank enum name
- `stop_before_meaning`: MUST be True
- `forbidden_outputs`: FrozenSet of forbidden field names

**Example**:
```python
PreMeaningTrainingExample(
    example_id="example_001",
    example_type="base",
    input_surface="كَتَبَ",
    input_classification="vocalized_surface",
    operation_name="morphological_analysis",
    operation_spec_reference="morph_spec",
    cause_geometry=CauseGeometryDataset(...),
    before_state="surface",
    after_state="analyzed",
    invariant="consonants",
    trace=MappingProxyType({"operation": "analysis"}),
    residuals=frozenset([("ROOT_UNRESOLVED", "WARNING", "Multiple candidates")]),
    rank="HYPOTHESIS",
    stop_before_meaning=True,
    forbidden_outputs=frozenset(["meaning", "translation", "ifadah", "hukm"])
)
```

---

### 2. OperationTraceTrainingExample

**Purpose**: Training with complete operation trace

**Additional Fields**:
- `is_injective_operation`: Boolean
- `carries_preimage`: Boolean (for non-injective operations)
- `changed_components`: FrozenSet of component names

**Target Learning**:
```
Given: input + operation_spec + cause_geometry
Predict: after_state + trace + residuals + rank
```

**Constitutional Law**:
- Trace MUST be complete
- Either `is_injective_operation` OR `carries_preimage` declared
- Changed components explicitly listed

---

### 3. SurfaceInverseTrainingExample

**Purpose**: Surface-only inversion (HYPOTHETICAL)

**Additional Fields**:
- `recovered_candidates`: Tuple[str, ...] (multiple possibilities)
- `certainty`: Boolean (MUST be False)

**Target Learning**:
```
Given: surface_after
Predict: multiple_candidates + residuals + rank
Certainty: ALWAYS False
```

**Constitutional Laws**:
- `certainty` MUST be False
- `rank` ≤ STRONG_HYPOTHESIS (never CERTIFICATE)
- MUST have ≥2 candidates (ambiguity)
- MUST have residuals

**Example**:
```python
SurfaceInverseTrainingExample(
    # ... base fields ...
    recovered_candidates=("ك ت ب", "ك ت ب + فَعَلَ", "ك ت ب + كِتَاب"),
    certainty=False  # ✅ Required
)
```

---

### 4. TraceInverseTrainingExample

**Purpose**: Trace-based inversion (CONDITIONALLY CERTAIN)

**Additional Fields**:
- `recovered_before`: Optional[str] (certain recovery)
- `alternative_candidates`: Tuple[str, ...] (uncertain recovery)
- `is_certain`: Boolean
- `certainty_basis`: Optional[str] ("injective" or "trace_carries_preimage")
- `trace_is_complete`: Boolean
- `domain_declared`: Boolean
- `invariant_preserved`: Boolean
- `has_blocking_residuals`: Boolean
- `is_injective_operation`: Boolean
- `carries_preimage`: Boolean

**Target Learning**:
```
Given: after_state + trace + domain
Predict: recovered_before OR alternative_candidates
Certainty: True ONLY when conditions met
```

**Constitutional Laws (Law 6)**:

TraceInverse certain **ONLY when ALL**:
1. Trace complete
2. Domain declared
3. Invariant preserved
4. No blocking residuals
5. Either `is_injective_operation` OR `carries_preimage`

Otherwise: hypothetical candidates + lowered rank

**Example (Certain Recovery - إدغام with preimage)**:
```python
TraceInverseTrainingExample(
    # ... base fields ...
    before_state="ن + ل",
    after_state="لّ",
    trace=MappingProxyType({
        "deleted_consonant": "ن",
        "geminated_consonant": "ل",
        "operation": "assimilation"
    }),
    recovered_before="ن + ل",
    alternative_candidates=(),
    is_certain=True,  # ✅ All conditions met
    certainty_basis="trace_carries_preimage",
    trace_is_complete=True,
    domain_declared=True,
    invariant_preserved=True,
    has_blocking_residuals=False,
    is_injective_operation=False,  # Non-injective but...
    carries_preimage=True  # ...preimage preserved!
)
```

---

### 5. StopGateTrainingExample

**Purpose**: Demonstrate STOP before meaning

**Additional Fields**:
- `has_pattern_signified`: Boolean
- `has_root_stem_signified`: Boolean
- `has_operator_potential`: Boolean
- `has_reference_potential`: Boolean
- `has_relation_readiness`: Boolean
- `has_trace_only`: Boolean
- `has_compositional_relation`: Boolean (MUST be False)
- `has_pragmatic_closure`: Boolean (MUST be False)
- `has_evidence_for_truth`: Boolean (MUST be False)
- `expected_output`: str ("STOP_BEFORE_MEANING")

**Target Learning**:
```
Given: input with ONLY:
    - pattern signified
    - root/stem signified
    - operator potential
    - reference potential
    - relation readiness
    - trace only
Predict: STOP_BEFORE_MEANING (not final meaning)
```

**Constitutional Law**:
When input lacks semantic closure conditions (compositional relation, pragmatic closure, evidence for truth), output MUST be STOP signal, NOT meaning/ifadah/hukm.

---

### 6. ResidualRankTrainingExample

**Purpose**: Residual tracking and rank assignment

**Additional Fields**:
- `trace_completeness`: str ("complete", "incomplete", "missing")
- `has_blocking_residuals`: Boolean
- `has_warning_residuals`: Boolean
- `residual_count`: int
- `rank_justification`: str

**Target Learning**:
```
Given: operation + trace completeness + blocking conditions
Predict: residuals + appropriate rank
```

**Constitutional Law (Law 7)**:
```
Incomplete trace → candidates + residuals + lowered rank
```

**Rank Policy**:
- Operations cannot produce CERTIFICATE (only certification layers)
- Incomplete trace forces rank ≤ HYPOTHESIS
- Blocking residuals force rank = ZERO (or minimal)

---

## CauseGeometry Dataset Schema

**Complete 4 Aristotelian Causes + Domain Governance**

```python
@dataclass(frozen=True)
class CauseGeometryDataset:
    # Domain & Prior
    prior_info: FrozenSet[str]
    bāb: str  # Morphological door
    domain: str

    # Four Causes
    material_cause: str  # What transforms
    formal_cause: str  # Pattern imposed
    efficient_cause: str  # Licensing condition
    final_cause_before_meaning: str  # Purpose (PRE-SEMANTIC)

    # Governance
    license_type: str  # From LicenseType enum
    license_condition: str
    invariant: str
    trace_requirement: str  # From TraceRequirement enum
```

**Validation**:
- All 4 causes MUST be non-empty
- `bāb` and `domain` MUST be non-empty
- `final_cause_before_meaning` MUST NOT contain: "meaning", "semantic", "ifadah", "hukm", "truth"

---

## Forbidden Outputs

**Enum Definition**:
```python
class ForbiddenOutput(Enum):
    MEANING = "meaning"
    SEMANTIC_PAYLOAD = "semantic_payload"
    TRANSLATION = "translation"
    SYNTAX_ROLE = "syntax_role"
    RELATION_CANDIDATE = "relation_candidate"
    IFADAH = "ifadah"
    HUKM = "hukm"
    TRUTH_JUDGMENT = "truth_judgment"
```

**Validation**:
```python
def validate_no_forbidden_outputs(**kwargs) -> None:
    """Raises ValueError if any forbidden output present"""
```

**Usage**:
```python
# ❌ This will raise ValueError
validate_no_forbidden_outputs(meaning="some meaning")

# ❌ This will raise ValueError
validate_no_forbidden_outputs(ifadah="some ifadah")

# ✅ This is allowed
validate_no_forbidden_outputs(trace="operation_trace")
```

---

## Sample Examples

### Sample 1: SurfaceInverse (كَتَبَ → multiple roots)

```python
from dal_core.premeaning_dataset_schema import make_sample_surface_inverse_example

example = make_sample_surface_inverse_example()
# example_id: "surf_inv_001"
# input_surface: "كَتَبَ"
# recovered_candidates: ("ك ت ب", "ك ت ب + فَعَلَ", "ك ت ب + كِتَاب")
# certainty: False
# rank: "HYPOTHESIS"
```

### Sample 2: TraceInverse (إدغام: ن + ل → لّ)

```python
from dal_core.premeaning_dataset_schema import make_sample_trace_inverse_example

example = make_sample_trace_inverse_example()
# example_id: "trace_inv_001"
# before_state: "ن + ل"
# after_state: "لّ"
# is_certain: True
# certainty_basis: "trace_carries_preimage"
# trace: {"deleted_consonant": "ن", "geminated_consonant": "ل"}
```

---

## Testing Coverage (30 Tests)

### Law 1: No final meaning (5 tests)
- ✅ `test_base_example_forbids_meaning_in_trace`
- ✅ `test_forbidden_output_validator_blocks_meaning`
- ✅ `test_forbidden_output_validator_blocks_translation`
- ✅ `test_forbidden_output_validator_blocks_ifadah`
- ✅ `test_forbidden_output_validator_blocks_hukm`

### Law 2-4: No syntax/relation/ifadah/hukm (3 tests)
- ✅ `test_forbidden_output_validator_blocks_syntax_role`
- ✅ `test_forbidden_output_validator_blocks_relation_candidate`
- ✅ `test_forbidden_output_enum_complete`

### Law 5: SurfaceInverse never certain (4 tests)
- ✅ `test_surface_inverse_forbids_certainty`
- ✅ `test_surface_inverse_rank_ceiling`
- ✅ `test_surface_inverse_requires_multiple_candidates`
- ✅ `test_surface_inverse_sample_valid`

### Law 6-7: TraceInverse certainty conditions (7 tests)
- ✅ `test_trace_inverse_certainty_requires_complete_trace`
- ✅ `test_trace_inverse_certainty_requires_domain`
- ✅ `test_trace_inverse_certainty_forbids_blocking_residuals`
- ✅ `test_trace_inverse_certainty_requires_injective_or_preimage`
- ✅ `test_trace_inverse_certainty_requires_basis`
- ✅ `test_trace_inverse_certain_with_injective`
- ✅ `test_trace_inverse_sample_valid`

### Law 8: Residuals and rank required (2 tests)
- ✅ `test_example_requires_residuals`
- ✅ `test_example_requires_rank`

### Law 9: stop_before_meaning = True (2 tests)
- ✅ `test_example_requires_stop_before_meaning`
- ✅ `test_stop_gate_example_enforces_no_compositional_relation`

### Law 10: CauseGeometry complete (4 tests)
- ✅ `test_cause_geometry_requires_material_cause`
- ✅ `test_cause_geometry_requires_all_four_causes`
- ✅ `test_cause_geometry_requires_bab_and_domain`
- ✅ `test_cause_geometry_final_cause_forbids_semantic_terms`

### Residual/Rank Integration (2 tests)
- ✅ `test_residual_rank_example_validates_trace_completeness`
- ✅ `test_residual_rank_example_blocking_residuals_lower_rank`

### Integration (1 test)
- ✅ `test_sample_examples_all_valid`

**Total: 30/30 tests PASSING** ✅

---

## What This PR Does NOT Include

❌ **T5 model implementation**
❌ **Tokenizer training**
❌ **Generated dataset corpus**
❌ **Dataset generation code**
❌ **Semantic labels**
❌ **Relation/ifadah/hukm outputs**
❌ **Training scripts**
❌ **Model evaluation**

---

## What This PR DOES Include

✅ **Dataset schema contracts** (6 types)
✅ **CauseGeometry dataset schema**
✅ **Forbidden output validation**
✅ **Constitutional tests** (30 tests, all passing)
✅ **Sample examples** (2 working examples)
✅ **Documentation** (this file)

---

## Integration with Operation Algebra (PR #133)

This schema builds directly on PR #133:

```
PR #133: Operation Algebra Constitution
    ↓
    Defines: CauseGeometry, OperationTrace, SurfaceInverse, TraceInverse
    ↓
PR #135: PreMeaning Dataset Schema
    ↓
    Provides: Training example contracts for GARA-T5
    ↓
Future: Dataset Generation (PR #136?)
    ↓
    Generates: Corpus of PreMeaning training examples
    ↓
Future: GARA-T5 Training (PR #137?)
    ↓
    Trains: T5 on algebraic traces, NOT final meanings
```

---

## Next Steps (Out of Scope for This PR)

### PR #136: Dataset Generation
- Implement corpus generator
- Generate training/validation/test splits
- Export to HuggingFace format

### PR #137: GARA-T5 Model
- Initialize T5 architecture
- Custom tokenizer for Arabic
- Training loop
- Evaluation metrics

### PR #138: GARA-T5 Inference
- Inference pipeline
- Algebraic trace decoding
- Integration with dal_core

---

## Files Added

1. `src/dal_core/premeaning_dataset_schema.py` (696 lines)
   - 6 schema classes
   - CauseGeometry dataset
   - Forbidden output validation
   - Sample example generators

2. `tests/dal_core/test_premeaning_dataset_schema.py` (869 lines)
   - 30 constitutional tests
   - Complete law coverage
   - Integration tests

3. `docs/PREMEANING_DATASET_SCHEMA.md` (this file)
   - Complete documentation
   - Examples and usage
   - Test coverage summary

---

## Verification

```bash
# Run all schema tests
python -m pytest tests/dal_core/test_premeaning_dataset_schema.py -v

# Result: 30/30 PASSING ✅
```

---

## Conclusion

This PR establishes the **schema foundation** for GARA-T5 PreMeaning dataset.

**Key Achievement**:
> GARA-T5 will learn algebraic effects (trace-based transformations), NOT direct meanings.

This ensures:
```
GARA-T5 = T5 that follows algebra
GARA-T5 ≠ T5 that replaces algebra
```

**Constitutional Compliance**: All 10 laws enforced, all 30 tests passing.

**Ready for**: Dataset generation (next PR).
