# Trace Explanation Dataset Generator

**PR #145**: Constitutional dataset generator for T5 teaching from algorithm traces.

## Purpose

This module generates **teaching datasets** from validated algorithm traces. It enforces constitutional boundaries ensuring that T5 training data:

1. **Derives ONLY from AlgorithmTracePayload** - No raw Arabic input
2. **Contains ONLY validated references** - No invented candidates, residuals, gates, or ranks
3. **Preserves algorithm authority boundaries** - No forbidden fields that create constitutional facts
4. **Maintains trace_id binding** - Explanations bound to specific execution instances
5. **Preserves repair semantics** - Repairs require algorithm rerun, never resolve residuals directly

## Architecture

```
AlgorithmTracePayload (PR #141)
         ↓
GovernedTraceT5Contract (PR #142)
         ↓
ExplanationCandidate OR RepairSuggestionCandidate
         ↓
GovernedTraceT5Validator.validate_explanation()
GovernedTraceT5Validator.validate_explanation_references()
         ↓
DatasetRow (Teaching Artifact)
```

## Core Types

### DatasetRow

**Teaching artifact** derived from validated trace explanations.

```python
@dataclass(frozen=True)
class DatasetRow:
    dataset_row_id: str                    # Unique row identifier
    source_trace_id: str                   # Binds to specific execution
    source_algorithm: str                  # Algorithm class name
    operation: TraceConsumerOperation      # EXPLAIN or SUGGEST_REPAIR
    input_trace_summary: str               # Trace summary for teaching
    target_output_text: str                # Validated explanation text
    referenced_candidate_ids: Tuple[str, ...]   # Candidate IDs from trace
    referenced_residual_ids: Tuple[str, ...]    # Residual IDs from trace
    referenced_gate_ids: Tuple[str, ...]        # Gate IDs from trace
    referenced_rank_values: Tuple[str, ...]     # Rank values from trace
    output_type: OutputType                     # EXPLANATION or REPAIR_SUGGESTION
    requires_algorithm_rerun: bool              # True for repair suggestions
    validation_status: ValidationStatus         # VALID or rejection reason
    residuals_about_dataset_generation: Tuple[DatasetGenerationResidual, ...]
```

### Forbidden Fields (NOT in DatasetRow)

These fields are **constitutionally forbidden** because they would make T5 produce authority:

- ❌ `new_candidate` - T5 does NOT create candidates
- ❌ `upgraded_rank` - T5 does NOT upgrade rank
- ❌ `resolved_residuals` - T5 does NOT resolve residuals
- ❌ `closed_ifadah` - T5 does NOT close ifādah
- ❌ `hukm` - T5 does NOT produce ḥukm
- ❌ `reality` - T5 does NOT produce reality
- ❌ `semantic_certainty` - T5 does NOT certify semantics
- ❌ `final_answer` - T5 does NOT produce final answers
- ❌ `correct_analysis` - T5 does NOT judge correctness
- ❌ `gold_label_hukm` - T5 does NOT label constitutional facts
- ❌ `resolved_output` - T5 does NOT resolve algorithm outputs

**Constitutional Principle**: DatasetRow is a teaching artifact, NOT an authority-producing structure.

## Usage

### Generate from Valid Explanation

```python
from dal_core.trace_explanation_dataset_generator import TraceExplanationDatasetGenerator
from dal_core.governed_trace_t5_contract import ExplanationCandidate, TraceConsumerOperation
from tests.fixtures.golden_trace_explanation_fixtures import create_valid_explanation_fixture

# Load golden fixture
fixture = create_valid_explanation_fixture()

# Generate dataset row
row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
    trace=fixture.trace,
    explanation=fixture.explanation_candidate
)

assert row.validation_status == ValidationStatus.VALID
assert row.output_type == OutputType.EXPLANATION
assert row.source_trace_id == fixture.trace.trace_id
assert row.requires_algorithm_rerun == False
```

### Generate from Valid Repair Suggestion

```python
from tests.fixtures.golden_trace_explanation_fixtures import create_valid_repair_suggestion_fixture

# Load repair fixture
fixture = create_valid_repair_suggestion_fixture()

# Generate dataset row
row = TraceExplanationDatasetGenerator.generate_from_repair_suggestion_candidate(
    trace=fixture.trace,
    repair=fixture.repair_suggestion_candidate
)

assert row.validation_status == ValidationStatus.VALID
assert row.output_type == OutputType.REPAIR_SUGGESTION
assert row.requires_algorithm_rerun == True  # ALWAYS True for repairs
```

### Handle Invalid References

```python
from tests.fixtures.golden_trace_explanation_fixtures import create_invalid_invented_candidate_fixture

# Load invalid fixture (invented candidate_id)
fixture = create_invalid_invented_candidate_fixture()

# Generate dataset row
row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
    trace=fixture.trace,
    explanation=fixture.explanation_candidate
)

assert row.validation_status == ValidationStatus.REJECTED_INVENTED_REFERENCES
assert len(row.residuals_about_dataset_generation) > 0
assert row.residuals_about_dataset_generation[0].issue_type == "invented_candidate_reference"
```

### Reject Raw Arabic Input

```python
raw_arabic = "الكاتب المجتهد"

# Constitutional guard rejects raw Arabic
row = TraceExplanationDatasetGenerator.reject_raw_arabic(raw_arabic)

assert row.validation_status == ValidationStatus.REJECTED_RAW_ARABIC
assert len(row.residuals_about_dataset_generation) > 0
assert "Raw Arabic input forbidden" in row.residuals_about_dataset_generation[0].message
```

## Validation Pipeline

### Step 1: Trace ID Binding Validation

```python
if explanation.source_trace_id != trace.trace_id:
    return DatasetRow(
        validation_status=ValidationStatus.REJECTED_VALIDATION_FAILURE,
        residuals_about_dataset_generation=(
            DatasetGenerationResidual(
                issue_type="trace_id_mismatch",
                message=f"source_trace_id mismatch: explanation={explanation.source_trace_id}, trace={trace.trace_id}"
            ),
        ),
        # ... other fields
    )
```

### Step 2: GovernedTraceT5Contract Validation

```python
validator = GovernedTraceT5Validator(trace)
validation_result = validator.validate_explanation(explanation)

if not validation_result.is_valid:
    return DatasetRow(
        validation_status=ValidationStatus.REJECTED_VALIDATION_FAILURE,
        residuals_about_dataset_generation=tuple(
            DatasetGenerationResidual(
                issue_type="contract_validation_failure",
                message=res.message
            ) for res in validation_result.residuals
        ),
        # ... other fields
    )
```

### Step 3: Reference Validation

```python
reference_result = validator.validate_explanation_references(explanation)

if not reference_result.is_valid:
    return DatasetRow(
        validation_status=ValidationStatus.REJECTED_INVENTED_REFERENCES,
        residuals_about_dataset_generation=tuple(
            DatasetGenerationResidual(
                issue_type="invented_candidate_reference",
                message=res.message,
                rejected_references=tuple(res.message.split(": ")[1].split(", "))
            ) for res in reference_result.residuals
        ),
        # ... other fields
    )
```

### Step 4: Repair Semantics Validation

For `RepairSuggestionCandidate`:

```python
if not repair.requires_algorithm_rerun:
    return DatasetRow(
        validation_status=ValidationStatus.REJECTED_FORBIDDEN_OPERATION,
        residuals_about_dataset_generation=(
            DatasetGenerationResidual(
                issue_type="forbidden_direct_repair",
                message="RepairSuggestionCandidate MUST have requires_algorithm_rerun=True"
            ),
        ),
        # ... other fields
    )
```

## Integration with Golden Fixtures

This module consumes golden fixtures from PR #144:

```python
from tests.fixtures.golden_trace_explanation_fixtures import create_all_golden_fixtures

all_fixtures = create_all_golden_fixtures()

# Valid fixtures generate VALID dataset rows
valid_explanation = all_fixtures["valid_explanation"]
row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
    trace=valid_explanation.trace,
    explanation=valid_explanation.explanation_candidate
)
assert row.validation_status == ValidationStatus.VALID

# Invalid fixtures generate REJECTED dataset rows
invalid_candidate = all_fixtures["invalid_invented_candidate"]
row = TraceExplanationDatasetGenerator.generate_from_explanation_candidate(
    trace=invalid_candidate.trace,
    explanation=invalid_candidate.explanation_candidate
)
assert row.validation_status == ValidationStatus.REJECTED_INVENTED_REFERENCES
```

## Constitutional Laws Enforced

### Law 1: T5 Dataset Derived ONLY from AlgorithmTracePayload

**Evidence**:
- `generate_from_explanation_candidate()` requires `AlgorithmTracePayload` parameter
- `generate_from_repair_suggestion_candidate()` requires `AlgorithmTracePayload` parameter
- `reject_raw_arabic()` explicitly rejects raw string input

**Tests**: `test_dataset_row_from_valid_explanation`, `test_reject_raw_arabic`

---

### Law 2: T5 Dataset Contains ONLY Validated References

**Evidence**:
- All references validated through `GovernedTraceT5Validator.validate_explanation_references()`
- Invented references produce `REJECTED_INVENTED_REFERENCES` status
- Residuals track rejected references

**Tests**: `test_invalid_explanation_rejected`, `test_invented_candidate_rejected`, `test_invented_residual_rejected`, `test_invented_gate_rejected`

---

### Law 3: T5 Dataset Has NO Forbidden Authority Fields

**Evidence**:
- `DatasetRow` has exactly 14 fields
- None of the 11 forbidden fields appear in DatasetRow definition
- Structural absence prevents T5 from producing authority

**Tests**: `test_dataset_row_no_dangerous_authority_fields`

---

### Law 4: Trace ID Binding Preserved

**Evidence**:
- `source_trace_id` field required in DatasetRow
- Trace ID mismatch produces validation failure
- Binds to specific execution instance, not algorithm class

**Tests**: `test_preserves_source_trace_id`, `test_source_trace_id_mismatch_handling`

---

### Law 5: Repair Rows Require Algorithm Rerun

**Evidence**:
- `requires_algorithm_rerun` hardcoded to `True` for repair rows
- Validation rejects repairs with `requires_algorithm_rerun=False`
- No `resolved_residuals` field in DatasetRow

**Tests**: `test_repair_row_requires_algorithm_rerun`, `test_repair_row_does_not_resolve_residuals`

---

### Law 6: Immutability Preserved

**Evidence**:
- All types are frozen dataclasses
- Cannot mutate DatasetRow after creation
- Cannot mutate source trace or candidates

**Tests**: `test_immutability`

---

## Test Coverage

**File**: `tests/dal_core/test_trace_explanation_dataset_generator.py`

**Total Tests**: 16

1. ✅ `test_dataset_row_from_valid_explanation` - Valid explanation → VALID row
2. ✅ `test_dataset_row_from_valid_repair_suggestion` - Valid repair → VALID row
3. ✅ `test_invalid_explanation_rejected` - Invalid explanation → REJECTED row
4. ✅ `test_reject_raw_arabic` - Raw Arabic → REJECTED_RAW_ARABIC
5. ✅ `test_invented_candidate_rejected` - Invented candidate_id → REJECTED
6. ✅ `test_invented_residual_rejected` - Invented residual_id → REJECTED
7. ✅ `test_invented_gate_rejected` - Invented gate_id → REJECTED
8. ✅ `test_invented_rank_rejected` - Invented rank → REJECTED
9. ✅ `test_source_trace_id_mismatch_handling` - Wrong trace_id → REJECTED
10. ✅ `test_preserves_source_trace_id` - Preserves trace_id binding
11. ✅ `test_dataset_row_no_dangerous_authority_fields` - No forbidden fields
12. ✅ `test_repair_row_requires_algorithm_rerun` - Repairs require rerun
13. ✅ `test_repair_row_does_not_resolve_residuals` - No resolved_residuals field
14. ✅ `test_validation_through_governed_trace_t5_contract` - Uses contract validator
15. ✅ `test_dataset_row_does_not_close_ifadah_hukm_reality` - No ifādah/ḥukm/reality
16. ✅ `test_immutability` - All types frozen

**Run**: `python -m pytest tests/dal_core/test_trace_explanation_dataset_generator.py -v`

---

## Forbidden Operations

The following operations are **constitutionally forbidden** in this module:

1. ❌ **Accept raw Arabic input** - Only `AlgorithmTracePayload` allowed
2. ❌ **Load T5 model** - This is dataset generation, NOT inference
3. ❌ **Create training pipeline** - This is row generation, NOT training
4. ❌ **Invent references** - Only existing trace elements allowed
5. ❌ **Resolve residuals** - Repairs require algorithm rerun
6. ❌ **Upgrade rank** - T5 does NOT change epistemic rank
7. ❌ **Create candidates** - T5 does NOT generate new candidates
8. ❌ **Close ifādah** - T5 does NOT produce ifādah closure
9. ❌ **Produce ḥukm** - T5 does NOT produce constitutional facts
10. ❌ **Produce reality** - T5 does NOT produce reality claims
11. ❌ **Add forbidden fields** - DatasetRow structure is final

---

## Future Dataset Export (NOT in this PR)

When exporting dataset rows to JSON/CSV for T5 training (FUTURE PR):

```python
# FUTURE: Export to training format
def export_dataset_rows_to_jsonl(rows: List[DatasetRow], output_path: str):
    """Export validated dataset rows to JSONL for T5 training."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for row in rows:
            if row.validation_status == ValidationStatus.VALID:
                training_example = {
                    "input": row.input_trace_summary,
                    "target": row.target_output_text,
                    "metadata": {
                        "source_trace_id": row.source_trace_id,
                        "source_algorithm": row.source_algorithm,
                        "output_type": row.output_type.name,
                        "requires_algorithm_rerun": row.requires_algorithm_rerun,
                    }
                }
                f.write(json.dumps(training_example, ensure_ascii=False) + '\n')
```

**Note**: Export logic is NOT in this PR. This PR only generates validated DatasetRow objects.

---

## References

- **PR #141**: `AlgorithmTracePayload` serialization contract
- **PR #142**: `GovernedTraceT5Contract` boundary enforcement
- **PR #143**: Trace ID and provenance validation hardening
- **PR #144**: Golden trace explanation fixtures
- **PR #145**: This PR - Trace explanation dataset generator

---

## Constitutional Formula

```
DatasetRow = تحويل الأثر المصادق إلى مثال تعليمي
(DatasetRow = Conversion of Validated Trace to Teaching Example)

Input:  AlgorithmTracePayload + ExplanationCandidate/RepairSuggestionCandidate
Validation: GovernedTraceT5Contract
Output: DatasetRow (Teaching Artifact)

NOT:
DatasetRow ≠ حكم دستوري    (DatasetRow ≠ Constitutional Fact)
DatasetRow ≠ إنتاج واقع     (DatasetRow ≠ Reality Production)
DatasetRow ≠ إغلاق إفادة    (DatasetRow ≠ Ifādah Closure)
DatasetRow ≠ ترقية الرتبة   (DatasetRow ≠ Rank Upgrade)
DatasetRow ≠ حل البقايا      (DatasetRow ≠ Residual Resolution)
```

---

**Created**: 2026-05-28
**Status**: Implementation complete, tests passing ✅
**Constitutional Compliance**: Verified ✅
**Branch**: `claude/trace-explanation-dataset-generator`
