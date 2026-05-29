# Governed T5 Integration Skeleton

**PR #150** | **Status**: Integration Skeleton (Contract/Boundary Layer ONLY)

## Overview

The Governed T5 Integration Skeleton provides a constitutional contract layer for T5 model integration without executing any actual model loading, training, or inference. This skeleton establishes integration boundaries, dependency declarations, and adapter contracts while maintaining strict constitutional compliance.

## Constitutional Laws

### Supreme Law
**Integration skeleton declares dependency and adapter contracts. It does NOT execute them.**

### Core Laws

1. **GovernedT5IntegrationConfig** is integration contract ONLY, not execution
2. **ModelDependencyDeclaration** declares dependencies as DATA, not imports
3. **AdapterBoundaryPlan** defines adapter interfaces ONLY, not implementations
4. **NoExecutionIntegrationReport** confirms no execution occurred
5. Integration skeleton does NOT load models
6. Integration skeleton does NOT execute inference
7. Integration skeleton does NOT train models
8. Integration skeleton does NOT compute metrics
9. Integration skeleton does NOT create constitutional authority

## Architecture

### Integration Flow

```
TrainingRunPlan (from PR #148)
    ↓
GovernedT5IntegrationConfig
    ↓
ModelDependencyDeclaration
    ↓
AdapterBoundaryPlan (Input/Output/Validation)
    ↓
IntegrationPreflightCheck
    ↓
IntegrationPreflightReport
    ↓
NoExecutionIntegrationReport
```

### Constitutional Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│ TrainingRunPlan (PR #148)                                   │
│ - Training plan with constitutional constraints             │
│ - References training examples (JSONL)                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ GovernedT5IntegrationConfig                                 │
│ - Integration contract specification                        │
│ - Links to TrainingRunPlan via training_run_plan_id        │
│ - Defines dependency declarations (data only)               │
│ - Defines adapter boundary plans (interfaces only)          │
│ - Specifies constitutional constraints                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ ModelDependencyDeclaration                                  │
│ - Model family: enum/string (NOT loaded model)              │
│ - Transformers version: string requirement                  │
│ - Torch version: string requirement (optional)              │
│ - Checkpoint path: string specification (optional)          │
│ - NO actual imports or model loading                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ AdapterBoundaryPlan (3 types)                               │
│ - INPUT_ADAPTER: TrainingRunPlan → model input spec        │
│ - OUTPUT_ADAPTER: model output spec → evaluation format    │
│ - VALIDATION_ADAPTER: constitutional constraint validation  │
│ Each boundary MUST:                                         │
│   • Preserve source_trace_id bindings                       │
│   • Prevent authority claims                                │
│   • Prevent rank upgrades                                   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ IntegrationPreflightCheck                                   │
│ - DEPENDENCY_DECLARATION: Dependencies are data only        │
│ - NO_FORBIDDEN_IMPORTS: No transformers/torch imports       │
│ - NO_MODEL_LOADING: No .from_pretrained() calls             │
│ - NO_INFERENCE_EXECUTION: No .generate() calls              │
│ - NO_TRAINING_EXECUTION: No Trainer or training loops       │
│ - ADAPTER_BOUNDARY_VALID: Boundaries properly defined       │
│ - CONSTITUTIONAL_CONSTRAINTS: Constraints preserved         │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ↓
┌─────────────────────────────────────────────────────────────┐
│ NoExecutionIntegrationReport                                │
│ - Confirms dependencies_declared_not_loaded                 │
│ - Confirms boundaries_defined_not_implemented               │
│ - Confirms no_model_loading_detected                        │
│ - Confirms no_training_execution_detected                   │
│ - Confirms no_inference_execution_detected                  │
│ - Reports integration_contract_valid status                 │
└─────────────────────────────────────────────────────────────┘
```

## Core Types

### ModelDependencyDeclaration

Declares model dependencies as **data structures** (NOT actual imports):

```python
@dataclass(frozen=True)
class ModelDependencyDeclaration:
    dependency_id: str
    model_family: ModelFamily  # Enum: T5_SMALL, T5_BASE, T5_LARGE
    required_transformers_version: str  # e.g., ">=4.30.0"
    required_torch_version: Optional[str]  # e.g., ">=2.0.0"
    checkpoint_path: Optional[str]  # Path specification (not loaded)
    additional_requirements: Tuple[str, ...]
```

**Constitutional Note**: These are string/enum declarations, NOT imported transformers/torch modules.

### AdapterBoundaryPlan

Defines adapter boundary **interfaces** (NOT implementations):

```python
@dataclass(frozen=True)
class AdapterBoundaryPlan:
    boundary_id: str
    boundary_type: AdapterBoundaryType  # INPUT/OUTPUT/VALIDATION
    input_contract_description: str
    output_contract_description: str
    constitutional_constraints: Tuple[str, ...]
    preserves_source_bindings: bool  # MUST be True
    prevents_authority_claims: bool  # MUST be True
    prevents_rank_upgrade: bool  # MUST be True
```

**Constitutional Requirements**:
- Must preserve `source_trace_id` bindings throughout
- Must prevent authority claims at all boundaries
- Must prevent rank upgrades at all boundaries

### GovernedT5IntegrationConfig

Main integration contract specification:

```python
@dataclass(frozen=True)
class GovernedT5IntegrationConfig:
    integration_id: str
    training_run_plan_id: str  # Links to TrainingRunPlan
    dependency_declaration: ModelDependencyDeclaration
    input_adapter_boundary: AdapterBoundaryPlan
    output_adapter_boundary: AdapterBoundaryPlan
    validation_adapter_boundary: AdapterBoundaryPlan
    constitutional_constraints: Tuple[str, ...]
```

**Constitutional Note**: This is a contract specification, NOT model execution.

### NoExecutionIntegrationReport

Report confirming no execution occurred:

```python
@dataclass(frozen=True)
class NoExecutionIntegrationReport:
    report_id: str
    integration_config_id: str
    preflight_report: IntegrationPreflightReport
    dependencies_declared_not_loaded: bool  # MUST be True
    boundaries_defined_not_implemented: bool  # MUST be True
    no_model_loading_detected: bool  # MUST be True
    no_training_execution_detected: bool  # MUST be True
    no_inference_execution_detected: bool  # MUST be True
    integration_contract_valid: bool
```

## Forbidden Operations

The integration skeleton explicitly **FORBIDS**:

### Forbidden Imports
- ❌ `import transformers`
- ❌ `import torch`
- ❌ `from transformers import ...`
- ❌ `from torch import ...`

### Forbidden Model Operations
- ❌ `.from_pretrained()` - No model loading
- ❌ `AutoTokenizer` - No tokenizer creation
- ❌ `T5ForConditionalGeneration` - No T5 instantiation
- ❌ `model.generate()` - No inference execution
- ❌ `model.forward()` - No forward passes

### Forbidden Training Operations
- ❌ `Trainer()` - No trainer creation
- ❌ `TrainingArguments()` - No training args
- ❌ Training loops
- ❌ Optimizer construction
- ❌ Loss computation
- ❌ Metrics computation

### Forbidden Constitutional Operations
- ❌ Rank upgrades
- ❌ Residual resolution
- ❌ Ifādah closure
- ❌ Hukm production
- ❌ Reality production
- ❌ Authority claims

## Permitted Operations

The integration skeleton **PERMITS**:

### Declaration Operations
- ✅ Declare model dependencies as strings/enums
- ✅ Declare version requirements as data
- ✅ Specify checkpoint paths as strings
- ✅ Define adapter boundary interfaces

### Validation Operations
- ✅ Validate integration config completeness
- ✅ Run preflight constitutional checks
- ✅ Scan for forbidden execution markers
- ✅ Validate adapter boundary contracts

### Linkage Operations
- ✅ Link to `TrainingRunPlan` via ID reference
- ✅ Connect adapter boundaries to config
- ✅ Preserve constitutional constraints throughout

## Usage Example

```python
from dal_core.governed_t5_integration_skeleton import (
    GovernedT5IntegrationConfig,
    ModelDependencyDeclaration,
    AdapterBoundaryPlan,
    GovernedT5IntegrationSkeleton,
    ModelFamily,
    AdapterBoundaryType,
)

# Step 1: Declare model dependencies (data only, no imports)
dependency = ModelDependencyDeclaration(
    dependency_id="dep_001",
    model_family=ModelFamily.T5_BASE,
    required_transformers_version=">=4.30.0",
    required_torch_version=">=2.0.0",
)

# Step 2: Define adapter boundaries (interfaces only)
input_boundary = AdapterBoundaryPlan(
    boundary_id="input_boundary_001",
    boundary_type=AdapterBoundaryType.INPUT_ADAPTER,
    input_contract_description="TrainingRunPlan data",
    output_contract_description="T5 input format specification",
    constitutional_constraints=(
        "Preserve source_trace_id bindings",
        "Prevent authority claims",
    ),
    preserves_source_bindings=True,
    prevents_authority_claims=True,
    prevents_rank_upgrade=True,
)

# Similar for output_boundary and validation_boundary...

# Step 3: Create integration config (contract only)
config = GovernedT5IntegrationConfig(
    integration_id="integration_001",
    training_run_plan_id="plan_001",  # References TrainingRunPlan
    dependency_declaration=dependency,
    input_adapter_boundary=input_boundary,
    output_adapter_boundary=output_boundary,
    validation_adapter_boundary=validation_boundary,
    constitutional_constraints=INTEGRATION_CONSTITUTIONAL_CONSTRAINTS,
)

# Step 4: Run preflight validation
preflight = GovernedT5IntegrationSkeleton.run_preflight_checks(config)

if not preflight.all_checks_passed:
    print(f"Preflight failed: {preflight.critical_violations}")
else:
    # Step 5: Create integration report
    report = GovernedT5IntegrationSkeleton.create_integration_report(
        config, preflight
    )

    print(f"Integration contract valid: {report.integration_contract_valid}")
    print(f"No model loading: {report.no_model_loading_detected}")
    print(f"No training: {report.no_training_execution_detected}")
    print(f"No inference: {report.no_inference_execution_detected}")
```

## Preflight Validation

The integration skeleton includes **static scanning** for forbidden execution markers:

### Detected Markers

```python
FORBIDDEN_EXECUTION_MARKERS = frozenset([
    "import transformers",
    "import torch",
    "from transformers import",
    "from torch import",
    ".from_pretrained(",
    "AutoTokenizer",
    "T5ForConditionalGeneration",
    "Trainer(",
    ".generate(",
    ".forward(",
    # ... and more
])
```

### Preflight Checks

1. **DEPENDENCY_DECLARATION**: Verifies dependencies declared as data
2. **NO_FORBIDDEN_IMPORTS**: Scans for transformers/torch imports
3. **NO_MODEL_LOADING**: Scans for `.from_pretrained()` calls
4. **NO_INFERENCE_EXECUTION**: Scans for `.generate()` calls
5. **NO_TRAINING_EXECUTION**: Scans for `Trainer` or training loops
6. **ADAPTER_BOUNDARY_VALID**: Validates boundary contracts
7. **CONSTITUTIONAL_CONSTRAINTS**: Validates constraint preservation

## Relationship to Other Components

### PR #148: TrainingPipelineSkeleton
- `TrainingRunPlan` is the input to integration skeleton
- Integration config references `training_run_plan_id`
- Training plan constitutional constraints flow into integration

### PR #142: GovernedTraceT5Contract
- Similar constitutional approach: contract ONLY, not execution
- T5 consumes traces, does not create constitutional facts
- Integration skeleton extends this to integration planning

### PR #147: ConstitutionalEvaluationHarness
- Output adapter boundary connects to evaluation harness
- Constitutional constraints ensure evaluation compliance
- Source bindings preserved throughout integration

## Testing

All tests verify:
1. ✅ All dataclasses are immutable (`frozen=True`)
2. ✅ No forbidden imports in skeleton module
3. ✅ No forbidden execution markers in skeleton module
4. ✅ Dependencies are data only (strings/enums)
5. ✅ Boundaries are contracts only (no implementations)
6. ✅ Preflight detects forbidden markers in supplied text
7. ✅ No rank upgrade methods/fields exist
8. ✅ No residual resolution methods/fields exist
9. ✅ No ifādah closure methods/fields exist
10. ✅ No hukm/reality production methods/fields exist

**Total Tests**: 30+ comprehensive tests covering all constitutional requirements

## Future Work (Out of Scope for PR #150)

### PR #151 (Future): Actual T5 Integration
- Implement actual adapter implementations (within boundaries)
- Implement controlled dependency loading
- Implement governed inference harness
- Implement constitutional training executor

**Important**: PR #150 is **skeleton only**. Actual T5 integration implementation is explicitly out of scope.

## Constitutional Guarantee

**The integration skeleton guarantees**:
- Dependencies are **declared**, not **loaded**
- Boundaries are **defined**, not **implemented**
- Contracts are **specified**, not **executed**
- Integration is **planned**, not **run**

**This PR establishes the constitutional foundation for future T5 integration while maintaining strict boundary compliance.**

---

**See also**:
- `src/dal_core/governed_t5_integration_skeleton.py` - Implementation
- `tests/dal_core/test_governed_t5_integration_skeleton.py` - Tests
- PR #148: TrainingPipelineSkeleton
- PR #142: GovernedTraceT5Contract
- PR #147: ConstitutionalEvaluationHarness
