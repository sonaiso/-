# Adapter Boundary Review Matrix

**PR #157**: Central audit matrix documenting constitutional requirements at each adapter-chain boundary BEFORE T5 integration.

**Status**: ✅ Implemented (Audit Matrix Only)
**Version**: 1.0.0
**Created**: 2026-05-29

---

## Purpose

The Adapter Boundary Review Matrix is the **constitutional guardrails** for the adapter chain pipeline. It declares:

1. **What MUST be preserved** at each boundary (source bindings, references)
2. **What MUST be forbidden** at each boundary (authority claims, rank upgrades, execution markers)
3. **How to verify compliance** (verification criteria for each requirement)

The matrix is **NOT** a full validation engine (that's PR #158 Adapter Preflight Harness). It is a **central audit documentation tool** that establishes the constitutional law for ALL future adapter implementations.

---

## Constitutional Laws

### The Matrix Declares, Does NOT Execute

```
Matrix = Constitutional Audit Documentation
Verification = Compliance Checking (NOT Execution)
Result = Report (NOT Correction)
```

The matrix:
- ✅ Declares what must be preserved and forbidden
- ✅ Documents verification criteria
- ✅ Provides minimal shape verification
- ✅ Integrates with golden fixtures for validation

The matrix does NOT:
- ❌ Execute adapters
- ❌ Correct violations
- ❌ Run T5
- ❌ Replace ConstitutionalEvaluator
- ❌ Import transformers/torch
- ❌ Tokenize, load models, or execute inference

---

## Adapter Chain Formula

```
TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput → ConstitutionalEvaluator
```

Each `→` transition has documented constitutional requirements:

1. **TrainingExample → AdapterInput**: Source binding preservation, no execution
2. **AdapterInput → AdapterRawOutput**: Chain traceability, no model generation
3. **AdapterRawOutput → ModelOutput**: Source binding preservation, no authority claims
4. **ModelOutput → ConstitutionalEvaluator**: Required fields, violation detection

---

## Matrix Structure

### Four Boundary Transitions

| Transition | Source | Target | Key Requirements |
|-----------|---------|--------|------------------|
| 1 | TrainingExample | AdapterInput | Preserve source bindings, forbid execution |
| 2 | AdapterInput | AdapterRawOutput | Maintain chain traceability, forbid generation |
| 3 | AdapterRawOutput | ModelOutput | Preserve bindings, forbid authority |
| 4 | ModelOutput | ConstitutionalEvaluator | Require fields, detect violations |

### Nine Requirement Types

| Requirement Type | Category | Examples |
|-----------------|----------|----------|
| SOURCE_BINDING_PRESERVATION | Preservation | source_trace_id, source_training_example_id |
| REFERENCE_PRESERVATION | Preservation | candidate/residual/gate/rank IDs |
| AUTHORITY_PROHIBITION | Prohibition | No authority claims, no final_answer |
| RANK_UPGRADE_PROHIBITION | Prohibition | No rank upgrades |
| RESIDUAL_RESOLUTION_PROHIBITION | Prohibition | No residual deletion |
| IFADAH_CLOSURE_PROHIBITION | Prohibition | No ifādah closure |
| HUKM_PRODUCTION_PROHIBITION | Prohibition | No hukm production |
| REALITY_PRODUCTION_PROHIBITION | Prohibition | No reality production |
| EXECUTION_MARKER_PROHIBITION | Prohibition | No tokenizer, tensors, models |

---

## Transition Details

### Transition 1: TrainingExample → AdapterInput

**Purpose**: Transform training example into adapter input while preserving ALL constitutional bindings.

**Required Preservations**:
- `source_trace_id` (CRITICAL)
- `source_training_example_id` (CRITICAL)
- Referenced candidate/residual/gate/rank IDs (HIGH)

**Required Prohibitions**:
- No tokenization (tokenizer, input_ids, attention_mask)
- No tensor creation
- No model loading
- No authority claims
- No rank upgrade
- No residual resolution

**Verification Criteria**:
```python
# Check source bindings
assert adapter_input.source_trace_id == training_example.source_trace_id
assert adapter_input.source_training_example_id == training_example.training_example_id

# Check no execution markers
assert not hasattr(adapter_input, 'tokenizer')
assert not hasattr(adapter_input, 'input_ids')
assert not hasattr(adapter_input, 'tensor')
```

---

### Transition 2: AdapterInput → AdapterRawOutput

**Purpose**: Produce abstract raw output while maintaining chain traceability.

**Required Preservations**:
- `source_adapter_input_id` (CRITICAL)
- Chain traceability to original TrainingExample (CRITICAL)

**Required Prohibitions**:
- No model generation (model.generate())
- No tensor decoding
- No inference execution

**Verification Criteria**:
```python
# Check adapter input linkage
assert adapter_raw_output.source_adapter_input_id == adapter_input.adapter_input_id

# Check chain traceability (via registry)
chain_registry = get_chain_registry()
assert chain_registry.can_trace(adapter_raw_output, training_example)
```

---

### Transition 3: AdapterRawOutput → ModelOutput

**Purpose**: Map abstract raw output to ModelOutput while preserving ALL constitutional bindings.

**Required Preservations**:
- `source_trace_id` (CRITICAL)
- `source_training_example_id` (CRITICAL)
- Referenced IDs through predicted_text/metadata (HIGH)

**Required Prohibitions**:
- No authority claims
- No final_answer / correct_analysis / gold_label claims
- No rank upgrade
- No hukm production
- No reality production

**Verification Criteria**:
```python
# Check source bindings preserved through chain
assert model_output.source_trace_id == training_example.source_trace_id
assert model_output.source_training_example_id == training_example.training_example_id

# Check no authority phrases
forbidden_phrases = ["final_answer", "correct_analysis", "gold_label"]
assert not any(phrase in model_output.predicted_text.lower() for phrase in forbidden_phrases)
```

---

### Transition 4: ModelOutput → ConstitutionalEvaluator

**Purpose**: Ensure ModelOutput has ALL required fields for constitutional evaluation.

**Required Preservations** (Fields that MUST be present):
- `source_trace_id` (CRITICAL)
- `source_training_example_id` (CRITICAL)
- `predicted_text` (CRITICAL)
- `model_name` (CRITICAL)
- `generation_timestamp` (CRITICAL)

**Required Prohibitions** (Evaluator MUST detect):
- Missing bindings (MISSING_SOURCE_TRACE_ID, MISMATCHED_SOURCE_TRACE_ID)
- Authority claims (AUTHORITY_CLAIM)
- Invented references (INVENTED_CANDIDATE_REFERENCE, etc.)
- Rank upgrade claims (RANK_UPGRADE_CLAIM)
- Residual deletion claims (RESIDUAL_DELETION_CLAIM)
- Ifādah/Hukm/Reality closure claims (IFADAH_CLOSURE_CLAIM, etc.)

**Verification Criteria**:
```python
# Check required fields present
assert model_output.source_trace_id
assert model_output.source_training_example_id
assert model_output.predicted_text
assert model_output.model_name
assert model_output.generation_timestamp

# Evaluator detects violations
report = constitutional_evaluator.evaluate_model_output(model_output, training_example)
# Report will contain violations if any constitutional laws violated
```

---

## Usage

### 1. Build Canonical Matrix

```python
from dal_core.adapter_boundary_review_matrix import (
    build_canonical_adapter_boundary_matrix,
)

# Build the canonical adapter boundary matrix
matrix = build_canonical_adapter_boundary_matrix()

print(f"Matrix version: {matrix.matrix_version}")
print(f"Total requirements: {matrix.total_requirements_count}")
print(f"Critical requirements: {matrix.critical_requirements_count}")
print(f"Transitions: {len(matrix.transitions)}")
```

**Output**:
```
Matrix version: 1.0.0
Total requirements: 32
Critical requirements: 28
Transitions: 4
```

---

### 2. Verify Transition Shape

```python
from dal_core.adapter_boundary_review_matrix import (
    make_training_example_to_adapter_input_transition,
    verify_transition_shape,
)

# Get a transition
transition = make_training_example_to_adapter_input_transition()

# Verify shape
result = verify_transition_shape(transition)

print(f"Passed: {result.passed}")
print(f"Violations: {result.violations}")
print(f"Preserved bindings: {result.preserved_bindings}")
print(f"Detected prohibitions: {result.detected_prohibitions}")
```

---

### 3. Verify Matrix Shape

```python
from dal_core.adapter_boundary_review_matrix import (
    build_canonical_adapter_boundary_matrix,
    verify_matrix_shape,
)

# Build matrix
matrix = build_canonical_adapter_boundary_matrix()

# Verify shape
result = verify_matrix_shape(matrix)

print(f"Passed: {result.passed}")
print(f"Violations: {result.violations}")
```

---

### 4. Verify Golden Fixture Against Matrix

```python
from dal_core.adapter_boundary_review_matrix import (
    build_canonical_adapter_boundary_matrix,
    verify_golden_fixture_against_matrix,
)
from tests.fixtures.dal_core.golden_noop_adapter_chains import (
    make_valid_explanation_chain_fixture,
)

# Build matrix
matrix = build_canonical_adapter_boundary_matrix()

# Get golden fixture
fixture = make_valid_explanation_chain_fixture()

# Verify fixture against matrix
results = verify_golden_fixture_against_matrix(fixture, matrix)

print(f"Verification results: {len(results)}")
for i, result in enumerate(results, 1):
    print(f"Transition {i}: {'✓' if result.passed else '✗'}")
    if not result.passed:
        print(f"  Violations: {result.violations}")
```

---

## Integration with Golden Fixtures

The matrix integrates with the 6 golden no-op adapter chain fixtures (PR #155):

1. **valid_explanation_chain**: Passes all boundary verifications ✓
2. **authority_violation_chain**: Demonstrates authority prohibition requirement
3. **binding_loss_blocked_chain**: Demonstrates source binding preservation requirement
4. **wrong_output_link_blocked_chain**: Demonstrates adapter input preservation requirement
5. **reference_preservation_chain**: Demonstrates reference preservation requirement
6. **evaluator_ready_chain**: Demonstrates evaluator transition requirements

**Verification Pattern**:
```python
from dal_core.adapter_boundary_review_matrix import (
    build_canonical_adapter_boundary_matrix,
    verify_golden_fixture_against_matrix,
)
from tests.fixtures.dal_core.golden_noop_adapter_chains import (
    all_golden_noop_chain_fixtures,
)

matrix = build_canonical_adapter_boundary_matrix()

for fixture in all_golden_noop_chain_fixtures():
    results = verify_golden_fixture_against_matrix(fixture, matrix)
    print(f"{fixture.fixture_id}: {all(r.passed for r in results)}")
```

---

## Requirement Severity Levels

| Severity | Meaning | Examples |
|----------|---------|----------|
| CRITICAL | Constitutional boundary violation | Missing source_trace_id, tokenization attempted |
| HIGH | Serious compliance issue | Reference preservation failure |
| MEDIUM | Moderate compliance issue | (Reserved for future use) |

**All source binding requirements are CRITICAL.**
**All execution prohibition requirements are CRITICAL.**

---

## Matrix Immutability

The matrix is **fully immutable**:

```python
matrix = build_canonical_adapter_boundary_matrix()

# This will raise FrozenInstanceError
matrix.matrix_version = "2.0.0"  # ❌ Error

# Transitions are also frozen
transition = matrix.transitions[0]
transition.transition_id = "new_id"  # ❌ Error

# Requirements are also frozen
requirement = transition.requirements[0]
requirement.description = "new description"  # ❌ Error
```

**Why immutable?**
The matrix is constitutional law. Constitutional law does NOT change at runtime.

---

## Forbidden Operations

The matrix module explicitly FORBIDS:

```python
# ❌ FORBIDDEN: import transformers
# ❌ FORBIDDEN: import torch
# ❌ FORBIDDEN: tokenization
# ❌ FORBIDDEN: tensor creation
# ❌ FORBIDDEN: model loading
# ❌ FORBIDDEN: .from_pretrained()
# ❌ FORBIDDEN: model.generate()
# ❌ FORBIDDEN: Trainer
# ❌ FORBIDDEN: inference execution
# ❌ FORBIDDEN: training loop
# ❌ FORBIDDEN: metrics computation
# ❌ FORBIDDEN: repair violations
# ❌ FORBIDDEN: resolve residuals
```

**Verification**:
```bash
# Check module does NOT import transformers/torch
grep -r "import transformers\|import torch" src/dal_core/adapter_boundary_review_matrix.py
# Output: (nothing - no matches)
```

---

## Next Steps

After PR #157 (this PR), the roadmap is:

1. **PR #158: Adapter Preflight Harness**
   - Uses this matrix to build full validation engine
   - Implements deep content validation
   - Checks every requirement against actual adapter chains
   - Produces comprehensive preflight reports

2. **PR #159: Dependency Availability Check**
   - Checks if transformers/torch are available (NOT loading)
   - Validates version compatibility
   - Produces dependency readiness reports

3. **PR #160: Tokenizer Adapter Skeleton**
   - Defines tokenizer adapter interface (NOT implementation)
   - Documents tokenizer boundary requirements

4. **PR #161: Controlled Tokenizer Adapter Implementation**
   - First REAL T5 integration (tokenizer only)
   - MUST pass all matrix requirements
   - MUST pass adapter preflight harness

---

## Testing

**Test Coverage**: 36 tests across 4 categories

### Test Categories

1. **Matrix Construction Tests** (6 tests)
   - Canonical matrix structure
   - All transitions present
   - All requirement types covered
   - Matrix immutability
   - Requirement counts correct
   - Critical requirements identified

2. **Transition Requirement Tests** (12 tests - 3 per transition)
   - Preservations for each transition
   - Prohibitions for each transition
   - Verification criteria for each transition

3. **Verification Tests with Golden Fixtures** (12 tests)
   - Shape verification passes for canonical transitions
   - Shape verification passes for canonical matrix
   - Valid explanation fixture passes
   - Authority violation fixture maps to prohibition
   - Binding loss fixture maps to preservation
   - Wrong output link fixture maps to preservation
   - Reference preservation fixture passes
   - Evaluator-ready fixture passes
   - Every transition has preservation requirement
   - Every transition has prohibition requirement
   - Transition IDs unique
   - Requirement IDs unique

4. **Integration Tests** (6 tests)
   - No transformers imports
   - No torch imports
   - No execution markers
   - No production imports from fixtures
   - Matrix documentation exists
   - Canonical matrix is complete

**Run Tests**:
```bash
pytest tests/dal_core/test_adapter_boundary_review_matrix.py -v
```

---

## Files

| File | Purpose | Lines |
|------|---------|-------|
| `src/dal_core/adapter_boundary_review_matrix.py` | Matrix implementation | ~950 |
| `tests/dal_core/test_adapter_boundary_review_matrix.py` | Comprehensive tests | ~500 |
| `docs/ADAPTER_BOUNDARY_REVIEW_MATRIX.md` | This documentation | ~650 |

---

## Summary

The Adapter Boundary Review Matrix is the **constitutional audit tool** that documents ALL requirements for the adapter chain pipeline BEFORE any T5 integration.

**What it is**:
- Central audit matrix
- Constitutional documentation
- Minimal shape verification
- Integration with golden fixtures

**What it is NOT**:
- Full validation engine (that's PR #158)
- T5 implementation
- Execution tool
- Correction tool

**The matrix enforces**:
```
TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput → ConstitutionalEvaluator

No shortcuts. No bypasses. Full constitutional chain.
```

**Supreme Law**: The matrix declares what must be preserved and what must be forbidden. The matrix does NOT execute adapters.

---

**Version**: 1.0.0
**Status**: ✅ Complete
**Next**: PR #158 Adapter Preflight Harness
