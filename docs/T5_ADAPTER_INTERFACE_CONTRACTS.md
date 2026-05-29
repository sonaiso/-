# T5 Adapter Interface Contracts

**PR #152: Adapter Interface Contracts (Interfaces Only, No Execution)**

## Overview

This document specifies the adapter interface contracts between the governed T5 integration skeleton (PR #150) and any future T5 implementation. These contracts define the boundaries and transformation specifications WITHOUT implementing actual execution.

## Constitutional Position

### Supreme Law
**Adapter contracts declare transformation boundaries.**
**Adapter contracts do NOT execute transformations.**

### Constitutional Formula
```
TrainingExample → AdapterInput → AdapterRawOutput → ModelOutput → ConstitutionalEvaluator
```

The adapter layer sits between:
- **Input**: GovernedT5IntegrationConfig + TrainingRunPlan (already stable)
- **Output**: Future T5 implementation (NOT in this PR)

## Architecture

### Layer Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│ TrainingExample (PR #146)                                       │
│ - Immutable training data                                       │
│ - Source bindings: source_trace_id, source_training_example_id │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ InputAdapterContract (PR #152) ◄── THIS PR                     │
│ - Protocol: prepare_input()                                     │
│ - Protocol: validate_input()                                    │
│ - Produces: AdapterInput (abstract text, NOT tokenized)        │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ [Future T5 Implementation]                                      │
│ - NOT in this PR                                                │
│ - Will consume AdapterInput, produce AdapterRawOutput          │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ OutputAdapterContract (PR #152) ◄── THIS PR                    │
│ - Protocol: parse_output()                                      │
│ - Protocol: validate_output()                                   │
│ - Consumes: AdapterRawOutput (abstract text)                   │
│ - Produces: ModelOutput                                         │
└────────────────┬────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────────┐
│ ConstitutionalEvaluator (PR #147)                              │
│ - Evaluates ModelOutput for constitutional violations          │
└─────────────────────────────────────────────────────────────────┘
```

### Validation Layer

```
┌─────────────────────────────────────────────────────────────────┐
│ ValidationAdapterContract (PR #152) ◄── THIS PR                │
│ - ABC: validate_adapter_boundaries()                            │
│ - ABC: check_constitutional_compliance()                        │
│ - Validates: GovernedT5IntegrationConfig                        │
│ - Validates: AdapterBoundaryPlan                                │
│ - Produces: AdapterValidationResult                             │
└─────────────────────────────────────────────────────────────────┘
```

## Core Contracts

### 1. InputAdapterContract (Protocol)

**Purpose**: Transform TrainingExample to AdapterInput

**Required Methods**:
```python
def prepare_input(training_example: TrainingExample) -> AdapterInput:
    """
    Prepare AdapterInput from TrainingExample.

    MUST preserve source_trace_id and source_training_example_id.
    MUST NOT tokenize.
    MUST NOT create tensors.
    """
    ...

def validate_input(adapter_input: AdapterInput) -> AdapterValidationResult:
    """
    Validate AdapterInput structure and bindings.

    MUST check source bindings present.
    MUST NOT modify input.
    """
    ...
```

**Constitutional Requirements**:
1. Preserve `source_trace_id` from TrainingExample
2. Preserve `source_training_example_id` from TrainingExample
3. Prepare abstract input text (NOT tokenize)
4. Do NOT load models
5. Do NOT create tensors
6. Do NOT execute inference

### 2. OutputAdapterContract (Protocol)

**Purpose**: Transform AdapterRawOutput to ModelOutput

**Required Methods**:
```python
def parse_output(
    adapter_raw_output: AdapterRawOutput,
    source_training_example_id: str,
    source_trace_id: str,
) -> ModelOutput:
    """
    Parse AdapterRawOutput into ModelOutput.

    MUST preserve source_trace_id and source_training_example_id.
    MUST NOT generate text (receives abstract text).
    MUST NOT decode tensors.
    """
    ...

def validate_output(model_output: ModelOutput) -> AdapterValidationResult:
    """
    Validate ModelOutput structure and bindings.

    MUST check source bindings present.
    MUST NOT modify output.
    """
    ...
```

**Constitutional Requirements**:
1. Map abstract raw text to ModelOutput
2. Preserve source bindings through transformation chain
3. Do NOT generate text (receives already-generated abstract text)
4. Do NOT decode tensors (receives abstract text)
5. Do NOT execute inference
6. Do NOT create authority
7. Produce ModelOutput for ConstitutionalEvaluator review

### 3. ValidationAdapterContract (ABC)

**Purpose**: Validate adapter boundaries and constitutional compliance

**Required Methods**:
```python
@abstractmethod
def validate_adapter_boundaries(
    config: GovernedT5IntegrationConfig,
) -> AdapterValidationResult:
    """
    Validate adapter boundaries against integration config.

    MUST check all adapter boundaries defined.
    MUST check no forbidden imports present.
    MUST NOT execute models.
    """
    pass

@abstractmethod
def check_constitutional_compliance(
    adapter_input: AdapterInput,
) -> AdapterValidationResult:
    """
    Check adapter input for constitutional compliance.

    MUST check source bindings present.
    MUST check no forbidden fields present.
    MUST NOT modify input.
    """
    pass
```

**Constitutional Requirements**:
1. Check GovernedT5IntegrationConfig compliance
2. Check AdapterBoundaryPlan constraints
3. Detect forbidden imports/execution markers
4. Do NOT execute models
5. Do NOT train models
6. Do NOT resolve violations (only detect)
7. Produce reports, NOT corrections

## Data Structures

### AdapterInput

**Immutable input to adapter (abstract text ONLY, not tokenized)**

```python
@dataclass(frozen=True)
class AdapterInput:
    adapter_input_id: str
    source_training_example_id: str  # CONSTITUTIONAL BINDING
    source_trace_id: str             # CONSTITUTIONAL BINDING
    input_text: str                  # Abstract text (NOT tokenized)
    metadata: Tuple[Tuple[str, str], ...]
```

**Forbidden Fields**:
- ❌ `tokenizer`: Does NOT contain tokenizer
- ❌ `input_ids`: Does NOT contain token IDs
- ❌ `attention_mask`: Does NOT contain tensors
- ❌ `tensor`: Does NOT contain torch tensors
- ❌ `model`: Does NOT reference model
- ❌ `device`: Does NOT specify GPU/device

### AdapterRawOutput

**Immutable raw output from adapter (abstract text ONLY, not decoded tensors)**

```python
@dataclass(frozen=True)
class AdapterRawOutput:
    adapter_output_id: str
    source_adapter_input_id: str     # BINDING to AdapterInput
    raw_output_text: str             # Abstract text (NOT decoded)
    adapter_metadata: Tuple[Tuple[str, str], ...]
```

**Forbidden Fields**:
- ❌ `output_ids`: Does NOT contain token IDs
- ❌ `logits`: Does NOT contain logits
- ❌ `scores`: Does NOT contain scores
- ❌ `tensor`: Does NOT contain torch tensors
- ❌ `model`: Does NOT reference model
- ❌ `trainer`: Does NOT reference Trainer

### AdapterValidationResult

**Immutable result of adapter boundary validation**

```python
@dataclass(frozen=True)
class AdapterValidationResult:
    validation_id: str
    is_valid: bool
    violations: Tuple[AdapterViolationType, ...]
    warnings: Tuple[str, ...]
    checked_constraints: Tuple[str, ...]
```

**Forbidden Fields**:
- ❌ `repair_suggestions`: Does NOT repair
- ❌ `resolved_violations`: Does NOT resolve
- ❌ `upgraded_rank`: Does NOT upgrade rank
- ❌ `closed_ifadah`: Does NOT close ifādah

### AdapterResult

**Immutable result of adapter operation (carries data, does NOT resolve)**

```python
@dataclass(frozen=True)
class AdapterResult:
    adapter_result_id: str
    status: AdapterStatus
    model_output: Optional[ModelOutput]  # Present only if VALID
    violations: Tuple[AdapterViolationType, ...]
    residuals: Tuple[str, ...]           # Preserved, NOT resolved
```

**Forbidden Fields**:
- ❌ `resolved_residuals`: Does NOT resolve residuals
- ❌ `upgraded_rank`: Does NOT upgrade rank
- ❌ `closed_ifadah`: Does NOT close ifādah
- ❌ `produced_hukm`: Does NOT produce hukm
- ❌ `produced_reality`: Does NOT produce reality
- ❌ `repair_function`: Does NOT contain repair logic
- ❌ `optimizer`: Does NOT contain optimizer
- ❌ `trainer`: Does NOT contain trainer

## Enums

### AdapterStatus

```python
class AdapterStatus(Enum):
    VALID = auto()                      # Operation successful
    BOUNDARY_VIOLATION = auto()         # Integration boundary violated
    CONSTITUTIONAL_VIOLATION = auto()   # Constitutional constraint violated
    STRUCTURAL_ERROR = auto()           # Structural data error
```

### AdapterViolationType

```python
class AdapterViolationType(Enum):
    # Source binding violations
    MISSING_SOURCE_TRACE_ID = auto()
    MISSING_SOURCE_TRAINING_EXAMPLE_ID = auto()

    # Execution violations
    TOKENIZATION_ATTEMPTED = auto()
    TENSOR_CONVERSION_ATTEMPTED = auto()
    MODEL_LOADING_ATTEMPTED = auto()
    INFERENCE_EXECUTION_ATTEMPTED = auto()
    TRAINING_EXECUTION_ATTEMPTED = auto()

    # Constitutional violations
    RANK_UPGRADE_ATTEMPTED = auto()
    RESIDUAL_RESOLUTION_ATTEMPTED = auto()
    IFADAH_CLOSURE_ATTEMPTED = auto()
    HUKM_PRODUCTION_ATTEMPTED = auto()
    REALITY_PRODUCTION_ATTEMPTED = auto()
    AUTHORITY_CLAIM_ATTEMPTED = auto()

    # Structural violations
    FORBIDDEN_FIELD_PRESENT = auto()
```

## Constitutional Laws

### 10 Fundamental Laws

1. **Adapter contracts define boundaries; they do NOT implement execution**
2. **InputAdapterContract prepares abstract input text; it does NOT tokenize**
3. **OutputAdapterContract maps abstract raw text to ModelOutput; it does NOT generate**
4. **ValidationAdapterContract checks contracts; it does NOT execute models**
5. **Adapter results do NOT upgrade rank**
6. **Adapter results do NOT resolve residuals**
7. **Adapter results do NOT close ifādah**
8. **Adapter results do NOT produce hukm**
9. **Adapter results do NOT produce reality**
10. **Adapter results do NOT create constitutional authority**

### Forbidden Operations

The following operations are **categorically forbidden** in adapter contracts:

#### Import Violations
- ❌ `import transformers`
- ❌ `import torch`
- ❌ `from transformers import ...`
- ❌ `from torch import ...`

#### Execution Violations
- ❌ Tokenization (text → token IDs)
- ❌ Tensor conversion (data → torch.Tensor)
- ❌ Model loading (`.from_pretrained()`)
- ❌ Checkpoint loading
- ❌ Text generation (`.generate()`)
- ❌ Trainer creation (`Trainer()`)
- ❌ Training loops
- ❌ Inference execution
- ❌ Metrics computation
- ❌ Optimizer creation
- ❌ Forward pass execution
- ❌ GPU/device allocation

#### Constitutional Violations
- ❌ Rank upgrade
- ❌ Residual resolution
- ❌ Ifādah closure
- ❌ Hukm production
- ❌ Reality production
- ❌ Authority claims

### Permitted Operations

The following operations are **permitted** in adapter contracts:

#### Interface Definitions
- ✅ `typing.Protocol` definitions
- ✅ `abc.ABC` abstract base classes
- ✅ Abstract method signatures
- ✅ `@abstractmethod` decorators

#### Data Structures
- ✅ `@dataclass(frozen=True)` immutable types
- ✅ `Enum` definitions
- ✅ Immutable tuples
- ✅ Type hints

#### Validation Logic
- ✅ Data structure completeness checks
- ✅ Source binding verification
- ✅ Field presence validation
- ✅ Consistency checks
- ✅ Violation detection

#### References
- ✅ References to existing dal_core boundary types
- ✅ TrainingExample consumption
- ✅ ModelOutput production
- ✅ GovernedT5IntegrationConfig validation
- ✅ AdapterBoundaryPlan validation

## Integration Points

### With Existing Contracts

#### TrainingExample (PR #146)
- `InputAdapterContract` **consumes** `TrainingExample`
- Source bindings **MUST** be preserved:
  - `source_trace_id`
  - `source_training_example_id`

#### ModelOutput (PR #147)
- `OutputAdapterContract` **produces** `ModelOutput`
- Source bindings **MUST** be preserved through chain:
  - `TrainingExample.source_trace_id` → `AdapterInput.source_trace_id` → `ModelOutput.source_trace_id`
  - `TrainingExample.training_example_id` → `AdapterInput.source_training_example_id` → `ModelOutput.source_training_example_id`

#### ConstitutionalEvaluator (PR #147)
- `ModelOutput` from `OutputAdapterContract` is evaluated by `ConstitutionalEvaluator`
- Adapter violations are distinct from model output violations:
  - `AdapterViolationType`: Boundary violations at adapter layer
  - `ConstitutionalViolationType`: Content violations in model output

#### GovernedT5IntegrationConfig (PR #150)
- `ValidationAdapterContract` **validates** `GovernedT5IntegrationConfig`
- Checks adapter boundaries properly defined
- Detects forbidden imports/execution markers

#### AdapterBoundaryPlan (PR #150)
- `ValidationAdapterContract` **validates** `AdapterBoundaryPlan`
- Checks constitutional constraints at boundaries
- Verifies source binding preservation
- Verifies authority claim prevention
- Verifies rank upgrade prevention

### Binding Preservation Chain

```
TrainingExample.source_trace_id
    ↓
AdapterInput.source_trace_id
    ↓
[Future T5 execution - NOT in this PR]
    ↓
AdapterRawOutput (linked via source_adapter_input_id)
    ↓
ModelOutput.source_trace_id
    ↓
ConstitutionalEvaluator (validates binding)
```

**Constitutional Requirement**: Every transformation MUST preserve source bindings.

## Testing Requirements

### Comprehensive Test Coverage

All tests are in `tests/dal_core/test_t5_adapter_interface_contracts.py`.

#### Immutability Tests
- ✅ All dataclasses are `frozen=True`
- ✅ Mutation attempts raise `FrozenInstanceError`

#### Required Fields Tests
- ✅ All required fields validated
- ✅ Empty fields raise `ValueError`

#### Protocol/ABC Tests
- ✅ Protocols expose required method names
- ✅ ABCs declare abstract methods
- ✅ Method signatures have correct type hints

#### Source Binding Tests
- ✅ `AdapterInput` preserves `source_trace_id`
- ✅ `AdapterInput` preserves `source_training_example_id`
- ✅ Bindings preserved from `TrainingExample` to `AdapterInput`

#### Text-Only Tests
- ✅ `AdapterRawOutput` is raw text only (no tensors)
- ✅ No tensor fields present

#### Violation Carrying Tests
- ✅ `AdapterResult` can carry violations without resolving
- ✅ `AdapterResult` can carry residuals without resolving
- ✅ No resolution methods exist

#### Forbidden Fields Tests
- ✅ No forbidden fields in `AdapterInput` (tokenizer, tensor, model, device, etc.)
- ✅ No forbidden fields in `AdapterRawOutput` (logits, tensor, model, etc.)
- ✅ No forbidden fields in `AdapterResult` (resolved_residuals, upgraded_rank, etc.)
- ✅ `FORBIDDEN_ADAPTER_FIELDS` constant is comprehensive

#### Integration Chain Tests
- ✅ Source bindings preserved through full chain
- ✅ `AdapterRawOutput` convertible to `ModelOutput` shape
- ✅ Full constitutional chain shape is valid

#### Negative Tests
- ✅ No concrete T5 adapter implementation exists
- ✅ No forbidden imports in contracts module (transformers, torch)
- ✅ No execution markers present (AutoTokenizer, T5ForConditionalGeneration, .from_pretrained, Trainer, .generate)

### Test Count: 25+ Tests

All tests verify **interface contracts only**, with **zero execution**.

## Out of Scope

The following are **explicitly out of scope** for PR #152:

### NOT Implemented
- ❌ Tokenizer adapter implementation
- ❌ T5 model loading
- ❌ Hugging Face integration
- ❌ Inference execution
- ❌ Training execution
- ❌ Metrics computation
- ❌ Actual text generation
- ❌ Actual tokenization
- ❌ Tensor operations
- ❌ GPU/device management

### Deferred to Future PRs
After PR #152 is stable, the progression would be:
1. **PR #153**: Adapter contract hardening (additional validation)
2. **PR #154**: Dummy/no-op adapter (smoke tests without Hugging Face)
3. **PR #155+**: Actual T5 tokenizer/model integration (if constitutional review passes)

## File Structure

### Core Module
```
src/dal_core/t5_adapter_interface_contracts.py
```

**Contents**:
- `AdapterStatus` enum
- `AdapterViolationType` enum
- `AdapterInput` dataclass
- `AdapterRawOutput` dataclass
- `AdapterValidationResult` dataclass
- `AdapterResult` dataclass
- `InputAdapterContract` Protocol
- `OutputAdapterContract` Protocol
- `ValidationAdapterContract` ABC
- `FORBIDDEN_ADAPTER_FIELDS` constant

### Tests
```
tests/dal_core/test_t5_adapter_interface_contracts.py
```

**Contents**:
- 25+ comprehensive tests
- Immutability tests
- Source binding tests
- Protocol/ABC signature tests
- Forbidden fields tests
- Integration chain tests
- Negative tests (no implementation, no forbidden imports)

### Documentation
```
docs/T5_ADAPTER_INTERFACE_CONTRACTS.md
```

**Contents**:
- Architecture overview
- Contract specifications
- Data structure specifications
- Constitutional laws
- Integration points
- Testing requirements
- Out of scope items

## Summary

PR #152 establishes the **adapter interface contract layer** between:
- **Governed constitutional skeleton** (PRs #146-#150, already stable)
- **Future T5 implementation** (not in this PR)

**Key Principles**:
1. **Interfaces only**, no execution
2. **Abstract text**, no tokenization
3. **Source bindings preserved**, no authority claims
4. **Violations detected**, not resolved
5. **Boundaries declared**, not implemented

This PR is **3 files total**:
1. `src/dal_core/t5_adapter_interface_contracts.py` (contract definitions)
2. `tests/dal_core/test_t5_adapter_interface_contracts.py` (comprehensive tests)
3. `docs/T5_ADAPTER_INTERFACE_CONTRACTS.md` (this document)

**Constitutional Status**: ✅ **Compliant**
**Execution Status**: ⛔ **None** (interfaces only)
**Integration Status**: ✅ **Ready** (links to existing contracts)

---

**Created**: 2026-05-29
**PR**: #152
**Builds on**: PR #150 (GovernedT5IntegrationSkeleton), PR #147 (ConstitutionalEvaluator), PR #146 (TrainingExample)
