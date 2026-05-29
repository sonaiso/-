# Training Pipeline Skeleton Contract

**PR #148: Training Pipeline Skeleton (Contract Only, NOT Execution)**

## Constitutional Summary

```
Training pipeline skeleton plans training; it does NOT train.
Training pipeline skeleton checks conditions; it does NOT execute models.
Training pipeline skeleton produces plans; it does NOT create authority.
```

## Architecture Overview

```
TrainingExample + JSONL
    ↓
TrainingPipelineConfig (immutable configuration)
    ↓
TrainingPlanCandidate (resource estimation)
    ↓
ConstitutionalPreflightCheck (validation)
    ↓
TrainingRunPlan (governed plan)
```

### Constitutional Formula

```
TrainingExample + Config → TrainingPlanCandidate
TrainingPlanCandidate + Preflight → TrainingRunPlan
TrainingRunPlan = Plan for training, NOT training execution
```

## Core Components

### 1. TrainingPipelineConfig

**Purpose**: Immutable configuration contract (NOT execution)

**Fields**:
- `config_id`: Unique identifier
- `training_examples_path`: Path to JSONL file
- `model_architecture`: Target architecture (contract only, NOT loaded model)
- `training_mode`: EXPLANATION_GENERATION | REPAIR_SUGGESTION | MIXED
- `max_input_length`: Input tokenization limit
- `max_target_length`: Target tokenization limit
- `batch_size`: Training batch size
- `num_epochs`: Training duration
- `learning_rate`: Optimizer parameter
- `output_dir`: Where plan suggests saving
- `allowed_operations`: Permitted TraceConsumerOperations

**Constitutional Requirements**:
- ✅ Configuration is immutable (frozen=True)
- ✅ All fields validated at construction
- ✅ Model architecture is contract specification only
- ❌ Does NOT load models
- ❌ Does NOT execute training
- ❌ Does NOT create authority

### 2. TrainingPlanCandidate

**Purpose**: Plan representation (NOT execution)

**Fields**:
- `plan_id`: Unique identifier
- `config_id`: References TrainingPipelineConfig
- `config`: The training configuration
- `total_examples`: Count of training examples
- `estimated_steps`: Estimated training steps
- `estimated_duration_minutes`: Estimated duration
- `requires_preflight_check`: Whether validation needed

**Constitutional Requirements**:
- ✅ Plan is immutable representation
- ✅ Estimates resources, does NOT allocate them
- ✅ Counts examples, does NOT train on them
- ❌ Does NOT execute training
- ❌ Does NOT load models
- ❌ Does NOT create authority

### 3. ConstitutionalPreflightReport

**Purpose**: Validation results (NOT execution)

**Fields**:
- `report_id`: Unique identifier
- `plan_id`: References TrainingPlanCandidate
- `checks`: Tuple of PreflightCheckResult
- `passed`: True if ALL checks PASSED
- `failed_checks_count`: Count of FAILED checks
- `warning_checks_count`: Count of WARNING checks

**Preflight Check Types**:
1. `CONFIG_VALIDATION`: Config fields valid
2. `TRAINING_EXAMPLES_EXIST`: Training file exists
3. `TRAINING_EXAMPLES_VALID`: Examples well-formed
4. `OUTPUT_DIR_WRITABLE`: Output directory accessible
5. `OPERATION_PERMITTED`: Operations constitutionally allowed
6. `NO_FORBIDDEN_PHRASES`: No authority claims in examples
7. `SOURCE_BINDINGS_PRESERVED`: All examples have source bindings

**Constitutional Requirements**:
- ✅ Checks validate conditions ONLY
- ✅ Checks detect violations, NOT resolve them
- ✅ Checks produce report, NOT corrections
- ❌ Does NOT execute training
- ❌ Does NOT modify examples
- ❌ Does NOT create authority

### 4. TrainingRunPlan

**Purpose**: Governed training plan (NOT execution, NOT authority)

**Fields**:
- `run_plan_id`: Unique identifier
- `plan_id`: References TrainingPlanCandidate
- `plan_candidate`: The training plan
- `preflight_report`: Preflight check report
- `ready_for_execution`: Whether plan passed preflight
- `constitutional_constraints`: Forbidden operations

**Constitutional Requirements**:
- ✅ RunPlan is plan ONLY
- ✅ Preserves constitutional constraints
- ✅ `ready_for_execution` based on preflight (NOT execution itself)
- ❌ Does NOT execute training
- ❌ Does NOT load models
- ❌ Does NOT create authority

## Constitutional Constraints

The `CONSTITUTIONAL_CONSTRAINTS` frozen set declares all forbidden operations:

```python
CONSTITUTIONAL_CONSTRAINTS = frozenset([
    "NO_TRAINING_EXECUTION",
    "NO_MODEL_LOADING",
    "NO_INFERENCE_EXECUTION",
    "NO_METRIC_COMPUTATION",
    "NO_RANK_UPGRADE",
    "NO_RESIDUAL_RESOLUTION",
    "NO_IFADAH_CLOSURE",
    "NO_HUKM_PRODUCTION",
    "NO_REALITY_PRODUCTION",
    "NO_CANDIDATE_CREATION",
    "NO_HUGGING_FACE_IMPORTS",
    "NO_T5_MODEL_INSTANTIATION",
    "EVALUATION_BOUNDARY_ONLY",
    "PLAN_ONLY_NOT_AUTHORITY",
])
```

## Usage Example

```python
from dal_core.training_pipeline_skeleton import (
    TrainingPipelineConfig,
    TrainingPipelineSkeleton,
    TrainingMode,
    ModelArchitecture,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation

# 1. Create immutable configuration
config = TrainingPipelineConfig(
    config_id="config_001",
    training_examples_path="/data/examples.jsonl",
    model_architecture=ModelArchitecture.T5_BASE,
    training_mode=TrainingMode.EXPLANATION_GENERATION,
    max_input_length=512,
    max_target_length=256,
    batch_size=8,
    num_epochs=3,
    learning_rate=5e-5,
    output_dir="/output",
    allowed_operations=frozenset([
        TraceConsumerOperation.EXPLAIN_TRACE,
        TraceConsumerOperation.SUMMARIZE_CANDIDATES,
    ]),
)

# 2. Create training plan (counts examples, estimates resources)
plan = TrainingPipelineSkeleton.create_training_plan(config, examples)

# 3. Run preflight checks (validates conditions)
preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)

# 4. Create training run plan (governed plan)
run_plan = TrainingPipelineSkeleton.create_training_run_plan(plan, preflight)

# 5. Check if plan is ready
if run_plan.ready_for_execution:
    print(f"Plan ready: {run_plan.run_plan_id}")
    print(f"Estimated steps: {plan.estimated_steps}")
    print(f"Estimated duration: {plan.estimated_duration_minutes} minutes")
    print(f"Constitutional constraints: {len(run_plan.constitutional_constraints)}")
else:
    print(f"Plan failed preflight")
    print(f"Failed checks: {preflight.failed_checks_count}")
    for check in preflight.checks:
        if check.status == PreflightCheckStatus.FAILED:
            print(f"  - {check.check_type.name}: {check.message}")
```

## Forbidden Operations

### ❌ NEVER Allowed

1. **`train_model()`**: Training pipeline does NOT train
2. **`load_t5_model()`**: Training pipeline does NOT load models
3. **`execute_inference()`**: Training pipeline does NOT execute inference
4. **`compute_metrics()`**: Training pipeline does NOT compute metrics
5. **`upgrade_rank()`**: Training pipeline does NOT upgrade rank
6. **`resolve_residuals()`**: Training pipeline does NOT resolve residuals
7. **`close_ifadah()`**: Training pipeline does NOT close ifādah
8. **`produce_hukm()`**: Training pipeline does NOT produce hukm
9. **`create_candidate()`**: Training pipeline does NOT create candidates

### ✅ Always Allowed

1. **`create_training_config()`**: Define immutable configuration
2. **`create_training_plan()`**: Create plan candidate
3. **`validate_preflight_conditions()`**: Check constitutional compliance
4. **`create_training_run_plan()`**: Produce governed plan

## Testing Coverage

Total: **30 tests** covering:

### TrainingPipelineConfig (6 tests)
- ✅ Valid config creation
- ✅ Config immutability
- ✅ Required fields validation
- ✅ Positive value constraints
- ✅ Allowed operations required

### TrainingPlanCandidate (5 tests)
- ✅ Plan creation from config
- ✅ Step estimation correctness
- ✅ Plan immutability
- ✅ Non-empty examples requirement
- ✅ Config ID match validation

### ConstitutionalPreflightCheck (6 tests)
- ✅ All checks pass scenario
- ✅ Missing training file detection
- ✅ Empty examples detection
- ✅ Disallowed operations detection
- ✅ Missing source bindings detection
- ✅ Forbidden phrases warning

### TrainingRunPlan (5 tests)
- ✅ Run plan creation
- ✅ Run plan immutability
- ✅ Plan ID match validation
- ✅ Ready/failed preflight consistency
- ✅ Constitutional constraints required

### Constitutional Constraints (8 tests)
- ✅ Constraints non-empty
- ✅ Training execution forbidden
- ✅ Model loading forbidden
- ✅ Inference execution forbidden
- ✅ Rank upgrade forbidden
- ✅ Hukm production forbidden
- ✅ Plan-only enforcement
- ✅ All constraints preserved in run plan

## Constitutional Laws

### Supreme Law
```
Training pipeline skeleton is planning boundary, NOT execution.
Training pipeline skeleton is validation boundary, NOT training.
Training pipeline skeleton is estimation boundary, NOT authority.
```

### Constitutional Requirements

1. **Configuration Contract**
   - TrainingPipelineConfig is configuration ONLY
   - Model architecture is contract specification, NOT loaded model
   - All fields are immutable

2. **Plan Representation**
   - TrainingPlanCandidate is plan ONLY, NOT execution
   - Estimates resources, does NOT allocate them
   - Counts examples, does NOT train on them

3. **Validation Only**
   - ConstitutionalPreflightCheck validates conditions ONLY
   - Detects violations, does NOT resolve them
   - Produces reports, does NOT make corrections

4. **Governed Plan**
   - TrainingRunPlan is plan ONLY, NOT authority
   - Preserves constitutional constraints
   - `ready_for_execution` indicates preflight status, NOT execution itself

### Constitutional Prohibitions

1. **NO Training Execution**
   - Pipeline skeleton does NOT train models
   - Pipeline skeleton does NOT load models
   - Pipeline skeleton does NOT execute inference

2. **NO Metrics Computation**
   - Pipeline skeleton does NOT compute metrics
   - Pipeline skeleton does NOT evaluate quality
   - Pipeline skeleton does NOT produce scores

3. **NO Authority Creation**
   - Pipeline skeleton does NOT upgrade rank
   - Pipeline skeleton does NOT resolve residuals
   - Pipeline skeleton does NOT close ifādah
   - Pipeline skeleton does NOT produce hukm
   - Pipeline skeleton does NOT produce reality
   - Pipeline skeleton does NOT create candidates

## Integration with Existing Components

### Builds On
- **PR #146**: TrainingExample, DatasetExporter
- **PR #147**: ModelOutput, ConstitutionalEvaluator
- **PR #142**: GovernedTraceT5 (contract only)
- **PR #141**: AlgorithmTracePayload, TraceConsumerOperation

### Prepares For
- **Future PR**: Actual training execution (OUTSIDE this skeleton)
- **Future PR**: Model inference (OUTSIDE this skeleton)
- **Future PR**: Metrics computation (OUTSIDE this skeleton)

### Constitutional Boundaries

```
┌─────────────────────────────────────────┐
│   TrainingPipelineSkeleton (PR #148)    │
│   ────────────────────────────────────  │
│   • Plans training (NOT executes)       │
│   • Validates conditions (NOT trains)   │
│   • Estimates resources (NOT allocates) │
│   • Produces governed plans             │
└─────────────────────────────────────────┘
           ↓ (uses)
┌─────────────────────────────────────────┐
│   TrainingExample (PR #146)             │
│   ConstitutionalEvaluator (PR #147)     │
│   ────────────────────────────────────  │
│   • Immutable serialization boundary    │
│   • Constitutional evaluation harness   │
└─────────────────────────────────────────┘
           ↓ (uses)
┌─────────────────────────────────────────┐
│   AlgorithmTracePayload (PR #141)       │
│   GovernedTraceT5 (PR #142)             │
│   ────────────────────────────────────  │
│   • Non-authoritative trace evidence    │
│   • T5 constitutional contract          │
└─────────────────────────────────────────┘
```

## File Locations

- **Contract**: `src/dal_core/training_pipeline_skeleton.py`
- **Tests**: `tests/dal_core/test_training_pipeline_skeleton.py`
- **Documentation**: `docs/TRAINING_PIPELINE_SKELETON.md` (this file)

## Verification Commands

```bash
# Run all training pipeline skeleton tests
pytest tests/dal_core/test_training_pipeline_skeleton.py -v

# Run specific test class
pytest tests/dal_core/test_training_pipeline_skeleton.py::TestTrainingPipelineConfig -v

# Run constitutional constraints tests
pytest tests/dal_core/test_training_pipeline_skeleton.py::TestConstitutionalConstraints -v

# Verify constitutional guards
grep -n "NO_TRAINING_EXECUTION\|NO_MODEL_LOADING\|NO_INFERENCE_EXECUTION" \
  src/dal_core/training_pipeline_skeleton.py

# Verify no forbidden imports
! grep -n "from transformers\|import torch\|from huggingface" \
  src/dal_core/training_pipeline_skeleton.py
```

## Constitutional Compliance

### ✅ Compliant

- [x] Immutable data structures (frozen dataclasses)
- [x] Source bindings preserved (TrainingExample → Config → Plan)
- [x] Constitutional constraints declared explicitly
- [x] Preflight checks detect violations
- [x] No training execution
- [x] No model loading
- [x] No inference execution
- [x] No metrics computation
- [x] No authority creation
- [x] Plan representation only
- [x] Validation boundary only
- [x] 30 tests passing
- [x] All forbidden operations documented

### ❌ Non-Compliant (Would Violate Constitution)

- [ ] Importing `transformers` or `torch`
- [ ] Loading T5 models
- [ ] Executing training loops
- [ ] Computing metrics
- [ ] Upgrading rank
- [ ] Resolving residuals
- [ ] Closing ifādah
- [ ] Producing hukm
- [ ] Creating candidates
- [ ] Claiming constitutional authority

## Supreme Constitutional Principle

```arabic
خط التدريب يخطط، لا يدرّب.
يفحص الشروط، لا ينفذ النموذج.
ينتج خطة محكومة، لا سلطة دستورية.

Training pipeline plans; it does NOT train.
Checks conditions; does NOT execute models.
Produces governed plan; NOT constitutional authority.
```

---

**Created**: 2026-05-29
**PR**: #148
**Status**: Constitutional Contract (Skeleton Only)
**Next**: Actual training execution (FUTURE PR, OUTSIDE this skeleton)
