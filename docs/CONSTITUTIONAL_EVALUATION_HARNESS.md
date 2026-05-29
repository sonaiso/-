```markdown
# Constitutional Evaluation Harness
# حارس التقييم الدستوري

**PR #147**: Constitutional compliance checker for model outputs

**Status**: ✅ Implemented (2026-05-29)

---

## Constitutional Formula

```
TrainingExample + ModelOutput → ConstitutionalViolationReport → EvaluationReport
```

**Supreme Law**:
```
Evaluation guards constitutional boundaries.
Evaluation detects violations; it NEVER resolves them.
Evaluation produces reports; it NEVER trains models.
T5 learns to explain traces; T5 does NOT produce authority.
```

---

## Overview

The Constitutional Evaluation Harness is a **compliance checking system** that detects constitutional violations in model outputs BEFORE any training occurs. It is NOT a quality metric system, NOT an inference pipeline, and NOT a training harness.

### What This IS

✅ **Constitutional compliance checker**
✅ **Violation detection system**
✅ **Source binding validator**
✅ **Forbidden phrase detector**
✅ **Reference integrity verifier**

### What This is NOT

❌ NOT quality scoring (BLEU/F1/accuracy)
❌ NOT model training code
❌ NOT inference pipeline
❌ NOT model execution loop
❌ NOT violation repair system
❌ NOT Hugging Face integration

---

## Architecture

### Layer Position

```
AlgorithmTracePayload (PR #141)
    ↓
GovernedTraceT5Contract (PR #142)
    ↓
TraceExplanationDatasetGenerator (PR #145)
    ↓
DatasetRow → TrainingExample → JSONL Export (PR #146)
    ↓
ModelOutput + ConstitutionalEvaluationHarness (PR #147) ← THIS MODULE
    ↓
(Future) Training Pipeline (PR #148)
    ↓
(Future) Governed T5 Integration (PR #149)
```

### Components

#### 1. ModelOutput (Immutable)

Model prediction container with constitutional source bindings.

**Fields**:
- `model_output_id`: Unique identifier
- `source_training_example_id`: **CONSTITUTIONAL BINDING** to TrainingExample
- `source_trace_id`: **CONSTITUTIONAL BINDING** to AlgorithmTracePayload
- `predicted_text`: Generated text (subject to review)
- `model_name`: Model identifier
- `generation_timestamp`: When prediction was made (ISO 8601)

**Forbidden Fields**:
- ❌ `upgraded_rank`
- ❌ `resolved_residuals`
- ❌ `closed_ifadah`
- ❌ `produced_hukm`
- ❌ `produced_reality`
- ❌ `new_candidate`
- ❌ `constitutional_authority`

#### 2. ConstitutionalViolationType (Enum)

Classification of constitutional violations.

**Source Binding Violations**:
- `MISSING_SOURCE_TRACE_ID`
- `MISMATCHED_SOURCE_TRACE_ID`
- `MISMATCHED_SOURCE_TRAINING_EXAMPLE_ID`

**Authority Claim Violations**:
- `AUTHORITY_CLAIM`
- `RANK_UPGRADE_CLAIM`
- `RESIDUAL_DELETION_CLAIM`
- `IFADAH_CLOSURE_CLAIM`
- `HUKM_PRODUCTION_CLAIM`
- `REALITY_PRODUCTION_CLAIM`

**Invented Reference Violations**:
- `INVENTED_CANDIDATE_REFERENCE`
- `INVENTED_RESIDUAL_REFERENCE`
- `INVENTED_GATE_REFERENCE`
- `INVENTED_RANK_REFERENCE`

#### 3. ConstitutionalViolationSeverity (Enum)

Severity classification for violations.

- `CRITICAL`: Constitutional boundary violation
- `HIGH`: Serious compliance issue
- `MEDIUM`: Moderate compliance issue

#### 4. ConstitutionalViolation (Immutable)

Single detected violation with details.

**Fields**:
- `violation_type`: Type from ConstitutionalViolationType
- `severity`: Severity level
- `message`: Description of violation
- `detected_phrase`: Specific phrase (if applicable)
- `detected_reference`: Specific reference (if applicable)

#### 5. ConstitutionalViolationReport (Immutable)

Report for single model output evaluation.

**Fields**:
- `report_id`: Unique identifier
- `model_output_id`: ID of evaluated output
- `source_trace_id`: **CONSTITUTIONAL BINDING** preserved
- `violations`: Tuple of all violations
- `passed`: True if NO violations
- `critical_violations_count`: Count of CRITICAL violations
- `total_violations_count`: Total violations

#### 6. EvaluationReport (Immutable)

Batch evaluation report for multiple outputs.

**Fields**:
- `evaluation_id`: Unique identifier
- `total_examples_evaluated`: Total count
- `passed_count`: Count with NO violations
- `failed_count`: Count with violations
- `violation_reports`: Tuple of all reports

#### 7. ConstitutionalEvaluator (Static Class)

Constitutional compliance evaluation engine.

**Permitted Methods**:
- `evaluate_model_output(output, source_example) → ConstitutionalViolationReport`
- `batch_evaluate(outputs, examples) → EvaluationReport`
- `_validate_source_bindings(output, source_example) → violations`
- `_detect_authority_claims(predicted_text) → violations`
- `_detect_invented_references(predicted_text, source_example) → violations`

**Forbidden Methods**:
- ❌ `repair_violations()`
- ❌ `upgrade_rank()`
- ❌ `train_model()`
- ❌ `execute_inference()`

---

## Constitutional Laws

### Law 1: Evaluation is Compliance Checking ONLY

Evaluation checks constitutional compliance. It is NOT:
- Quality scoring (BLEU/F1/accuracy)
- Semantic correctness assessment
- Training performance metrics

### Law 2: Evaluation Detects, NEVER Resolves

Evaluator detects violations. It does NOT:
- Repair violations
- Resolve residuals
- Upgrade rank
- Close ifādah
- Produce hukm

### Law 3: Source Bindings are Constitutional Requirements

Every ModelOutput MUST preserve:
- `source_training_example_id` (binding to TrainingExample)
- `source_trace_id` (binding to AlgorithmTracePayload)

Missing or mismatched bindings are **CRITICAL violations**.

### Law 4: Forbidden Phrases are Constitutional Violations

ModelOutput MUST NOT contain forbidden authority phrases:

**Final Answer Claims**:
- "final_answer", "final answer", "final analysis", "definitive answer"

**Correctness Claims**:
- "correct_analysis", "correct answer", "true meaning"

**Certainty Claims**:
- "semantic_certainty", "definitely is", "absolutely"

**Resolution Claims**:
- "resolved_residuals", "resolved_output", "completely resolved"

**Rank Upgrade Claims**:
- "upgraded_rank", "upgraded to", "promoted to", "elevated to CERTIFICATE"

**Ifādah Closure Claims**:
- "closed_ifadah", "complete meaning", "semantic closure"

**Hukm Production Claims**:
- "produced_hukm", "produces hukm", "final judgment", "constitutional fact"

**Reality Production Claims**:
- "established reality", "semantic truth", "true reality"

**Candidate Creation Claims**:
- "new_candidate", "created candidate", "creates candidate"

**Gold Label Claims**:
- "gold_label_hukm", "gold label", "ground truth", "gold standard"

### Law 5: References Must Be Validated

ModelOutput may ONLY reference IDs present in source TrainingExample:
- `referenced_candidate_ids`
- `referenced_residual_ids`
- `referenced_gate_ids`
- `referenced_rank_values`

Invented references are **CRITICAL violations**.

### Law 6: Evaluation Produces Reports, NOT Corrections

Evaluator output is:
- ✅ ConstitutionalViolationReport (violation list)
- ✅ EvaluationReport (batch summary)

Evaluator output is NOT:
- ❌ Corrected ModelOutput
- ❌ Repaired violations
- ❌ Upgraded ranks
- ❌ Training metrics

### Law 7: Evaluation Does NOT Train

Evaluator is constitutional guardian, NOT trainer:
- ❌ NO model loading
- ❌ NO training loops
- ❌ NO gradient computation
- ❌ NO optimizer calls
- ❌ NO Hugging Face Trainer
- ❌ NO checkpoint saving

### Law 8: Evaluation Does NOT Execute Inference

Evaluator validates predictions, NOT generates them:
- ❌ NO model.generate()
- ❌ NO inference pipeline
- ❌ NO tokenization
- ❌ NO beam search
- ❌ NO sampling

---

## Usage Examples

### Example 1: Single Output Evaluation

```python
from dal_core.model_output import ModelOutput
from dal_core.training_example import TrainingExample
from dal_core.constitutional_evaluator import ConstitutionalEvaluator

# Source training example
training_example = TrainingExample(
    training_example_id="example_001",
    source_dataset_row_id="row_001",
    source_trace_id="trace_abc123",
    source_algorithm="relation_analyzer",
    operation=TraceConsumerOperation.EXPLAIN_TRACE,
    input_text="Trace summary for analysis",
    target_text="Expected explanation",
    referenced_candidate_ids=("candidate_xyz789",),
    referenced_residual_ids=("residual_def456",),
    referenced_gate_ids=("gate_ghi012",),
    referenced_rank_values=("PLAUSIBLE",),
    output_type=OutputType.EXPLANATION,
    requires_algorithm_rerun=False,
    validation_status=ValidationStatus.VALID,
)

# Model output (from T5 or other model)
model_output = ModelOutput.create_from_prediction(
    source_training_example_id="example_001",
    source_trace_id="trace_abc123",
    predicted_text="Explanation of the trace algorithm process",
    model_name="t5-base-governed",
)

# Evaluate for constitutional compliance
report = ConstitutionalEvaluator.evaluate_model_output(
    model_output,
    training_example,
)

# Check results
if report.passed:
    print("✅ Output passed constitutional compliance")
else:
    print(f"❌ {report.total_violations_count} violations detected:")
    for violation in report.violations:
        print(f"  - {violation.violation_type.name}: {violation.message}")
```

### Example 2: Batch Evaluation

```python
from dal_core.constitutional_evaluator import ConstitutionalEvaluator

# Multiple outputs and examples
outputs = (output1, output2, output3)
examples = (example1, example2, example3)

# Batch evaluate
evaluation_report = ConstitutionalEvaluator.batch_evaluate(outputs, examples)

# Summary
print(f"Total evaluated: {evaluation_report.total_examples_evaluated}")
print(f"Passed: {evaluation_report.passed_count}")
print(f"Failed: {evaluation_report.failed_count}")

# Individual reports
for report in evaluation_report.violation_reports:
    if not report.passed:
        print(f"\nOutput {report.model_output_id}:")
        for violation in report.violations:
            print(f"  - {violation.violation_type.name}")
```

### Example 3: Detecting Authority Claims

```python
# Output with forbidden phrase
bad_output = ModelOutput.create_from_prediction(
    source_training_example_id="example_001",
    source_trace_id="trace_001",
    predicted_text="This is the final_answer with correct_analysis",
    model_name="test_model",
)

report = ConstitutionalEvaluator.evaluate_model_output(bad_output, example)

# Violations detected
assert not report.passed
assert report.critical_violations_count > 0
assert any(
    v.detected_phrase == "final_answer"
    for v in report.violations
)
```

### Example 4: Detecting Invented References

```python
# Output references non-existent candidate
bad_output = ModelOutput.create_from_prediction(
    source_training_example_id="example_001",
    source_trace_id="trace_001",
    predicted_text="Analyzing candidate_invented123 from the trace",
    model_name="test_model",
)

# TrainingExample only has candidate_xyz789
example = TrainingExample(
    # ... other fields ...
    referenced_candidate_ids=("candidate_xyz789",),
)

report = ConstitutionalEvaluator.evaluate_model_output(bad_output, example)

# Invented reference violation
assert not report.passed
assert any(
    v.violation_type == ConstitutionalViolationType.INVENTED_CANDIDATE_REFERENCE
    for v in report.violations
)
```

---

## Validation Rules

### Rule 1: Source Binding Validation

```python
# CRITICAL: source_trace_id must match
assert output.source_trace_id == example.source_trace_id

# CRITICAL: source_training_example_id must match
assert output.source_training_example_id == example.training_example_id
```

### Rule 2: Authority Phrase Detection

```python
predicted_lower = output.predicted_text.lower()

# Check against forbidden phrases
for phrase in FORBIDDEN_AUTHORITY_PHRASES:
    if phrase in predicted_lower:
        # CRITICAL violation detected
        violations.append(...)
```

### Rule 3: Reference Validation

```python
# Extract candidate references from text
found_candidates = extract_candidate_ids(output.predicted_text)

# Validate against source example
for candidate_id in found_candidates:
    if candidate_id not in example.referenced_candidate_ids:
        # CRITICAL: invented reference
        violations.append(...)
```

---

## Test Coverage

### Required Tests (18 total)

✅ **Source Binding Tests (3)**:
1. Detects missing source_trace_id
2. Detects mismatched source_trace_id
3. Detects mismatched source_training_example_id

✅ **Authority Claims Tests (6)**:
4. Detects authority claims
5. Detects rank upgrade claims
6. Detects residual deletion claims
7. Detects ifādah closure claims
8. Detects hukm production claims
9. Detects reality production claims

✅ **Invented References Tests (4)**:
10. Detects invented candidate references
11. Detects invented residual references
12. Detects invented gate references
13. Detects invented rank references

✅ **Valid Output Tests (2)**:
14. Passed output has zero violations
15. Failed output has nonzero violations

✅ **Batch Evaluation Tests (3)**:
16. Preserves all violations in batch evaluation
17. Evaluation report counts pass/fail/total correctly
18. Rejects mismatched output/example counts

✅ **Constitutional Compliance Tests (4)**:
19. Evaluator has NO train_model method
20. Evaluator has NO execute_inference method
21. Evaluator has NO repair_violations method
22. Evaluator has NO upgrade_rank method

---

## Dependencies

### Required Imports

```python
from dal_core.model_output import ModelOutput
from dal_core.training_example import TrainingExample
from dal_core.constitutional_evaluator import (
    ConstitutionalEvaluator,
    ConstitutionalViolationType,
    ConstitutionalViolationSeverity,
    ConstitutionalViolation,
    ConstitutionalViolationReport,
    EvaluationReport,
)
```

### NO Training/Inference Dependencies

✅ **Allowed**:
- `dataclasses`
- `enum`
- `typing`
- `re`
- `datetime`
- `uuid`

❌ **FORBIDDEN**:
- ❌ `transformers` (Hugging Face)
- ❌ `torch` / `tensorflow`
- ❌ `datasets` (Hugging Face)
- ❌ `evaluate` (Hugging Face metrics)
- ❌ `accelerate`
- ❌ Any training/inference libraries

---

## Files Created

1. **`src/dal_core/model_output.py`** (~170 lines)
   - ModelOutput immutable dataclass
   - Factory method create_from_prediction
   - Constitutional validation in __post_init__

2. **`src/dal_core/constitutional_evaluator.py`** (~600 lines)
   - ConstitutionalViolationType enum
   - ConstitutionalViolationSeverity enum
   - ConstitutionalViolation dataclass
   - ConstitutionalViolationReport dataclass
   - EvaluationReport dataclass
   - FORBIDDEN_AUTHORITY_PHRASES constant
   - ConstitutionalEvaluator class with evaluation logic

3. **`tests/dal_core/test_model_output.py`** (~280 lines)
   - 14 tests for ModelOutput structure
   - Immutability tests
   - Source binding tests
   - Factory method tests
   - Forbidden fields tests

4. **`tests/dal_core/test_constitutional_evaluator.py`** (~600 lines)
   - 22 tests for constitutional compliance
   - Source binding validation tests
   - Authority claims detection tests
   - Invented references detection tests
   - Batch evaluation tests
   - Constitutional compliance tests

5. **`docs/CONSTITUTIONAL_EVALUATION_HARNESS.md`** (this file, ~900 lines)
   - Complete documentation
   - Constitutional laws
   - Usage examples
   - Validation rules

---

## Constitutional Guarantees

### What This PR Guarantees

✅ **Constitutional Binding Preservation**:
- Every ModelOutput preserves source_trace_id
- Every ModelOutput preserves source_training_example_id
- Binding violations are CRITICAL severity

✅ **Forbidden Operation Detection**:
- Authority claims detected
- Rank upgrade claims detected
- Residual deletion claims detected
- Ifādah/Hukm/Reality closure claims detected

✅ **Reference Integrity**:
- Invented candidates detected
- Invented residuals detected
- Invented gates detected
- Invented ranks detected

✅ **No Training/Inference Code**:
- Zero model loading code
- Zero training loops
- Zero inference pipelines
- Zero Hugging Face dependencies

✅ **Immutability**:
- All types are frozen dataclasses
- No post-creation modification
- No mutation methods

### What This PR Does NOT Do

❌ Model training
❌ Model inference
❌ Violation repair
❌ Rank upgrade
❌ Residual resolution
❌ Ifādah closure
❌ Hukm production
❌ Reality production
❌ Quality metrics computation

---

## Next Steps (Future PRs)

### PR #148: Training Pipeline Skeleton (Future)

**Scope**: Training orchestration WITHOUT real training
- TrainingConfig dataclass
- TrainingPipeline skeleton class
- Constitutional pre-training validation
- Constitutional post-training validation
- Training trace generation
- NO actual model.train() calls
- NO optimizer setup
- NO gradient computation

### PR #149: Governed T5 Integration (Future)

**Scope**: T5 model integration with constitutional guards
- Load T5 model with constitutional wrapper
- Execute inference with pre/post validation
- Generate ModelOutput from predictions
- Validate all outputs through ConstitutionalEvaluator
- Reject outputs with CRITICAL violations
- Preserve all constitutional bindings

---

## References

### Prior PRs

- **PR #141**: AlgorithmTracePayload serialization contract
- **PR #142**: GovernedTraceT5 constitutional contract
- **PR #145**: TraceExplanationDatasetGenerator
- **PR #146**: DatasetRow → TrainingExample → JSONL Export

### Constitutional Laws

- **Supreme Law**: T5 يستهلك الأثر، ولا ينشئ الحكم الدستوري
  (T5 consumes traces; T5 does NOT create constitutional facts)

- **Evaluation Law**: Evaluation guards boundaries; Evaluation does NOT resolve violations

- **Training Law**: Training learns from traces; Training does NOT produce authority

---

## Changelog

### 2026-05-29: Initial Implementation (PR #147)

✅ Created `src/dal_core/model_output.py`
✅ Created `src/dal_core/constitutional_evaluator.py`
✅ Created `tests/dal_core/test_model_output.py` (14 tests)
✅ Created `tests/dal_core/test_constitutional_evaluator.py` (22 tests)
✅ Created `docs/CONSTITUTIONAL_EVALUATION_HARNESS.md`
✅ All tests passing
✅ Zero training/inference dependencies
✅ Constitutional compliance verified

---

**Constitutional Status**: ✅ **COMPLIANT**

**Training Code**: ❌ **NONE** (as required)

**Inference Code**: ❌ **NONE** (as required)

**Hugging Face Dependencies**: ❌ **NONE** (as required)

**Total Lines**: ~2,150 (code + tests + docs)

**Test Coverage**: 22 tests covering all constitutional requirements

---

End of Documentation
```
