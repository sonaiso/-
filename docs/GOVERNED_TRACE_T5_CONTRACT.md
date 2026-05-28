# Governed Trace T5 Contract (عقد T5 المحكوم بالأثر)

**PR #142: Constitutional Contract for T5 Trace Consumption**

Created: 2026-05-28
Status: Contract Only (No Implementation)

---

## Constitutional Foundation

### Core Principle

```
T5 لا ينتج طبقة جديدة؛ T5 يشرح أثر طبقة أنتجتها الخوارزمية
(T5 does not produce new layers; T5 explains traces of layers produced by algorithms)
```

### Constitutional Formula

```
الجبر = الدستور
(Algebra = Constitution)

الخوارزمية = تنفيذ الدستور
(Algorithm = Constitutional Execution)

AlgorithmTracePayload = أثر التنفيذ
(Trace = Execution Evidence)

GovernedTraceT5Contract = عقد استهلاك الأثر
(Contract = Trace Consumption Contract)

T5 = مستهلك الأثر
(T5 = Bounded Trace Explainer)
```

---

## T5 Boundaries (What T5 Is NOT)

### Forbidden Identities

T5 is **NOT**:
1. An Arabic analyzer
2. A candidate generator
3. A rank upgrader
4. A residual resolver
5. An ifādah closer
6. A hukm/reality producer

### Forbidden Operations

T5 **MUST NOT**:
- `CREATE_CANDIDATE` - Only algorithms create candidates
- `UPGRADE_RANK` - Only proof procedures modify rank
- `DELETE_RESIDUALS` - Only gates resolve residuals
- `CLOSE_IFADAH` - Only ifadah closure gates
- `PRODUCE_HUKM` - Only judgment layer
- `PRODUCE_REALITY` - Only reality establishment
- `ANALYZE_RAW_ARABIC` - Only algorithms analyze Arabic text
- `MODIFY_TRACE` - Traces are immutable audit evidence
- `EXECUTE_REPAIR` - Only algorithms execute repairs
- `RESOLVE_RESIDUALS` - Only discharge procedures resolve residuals
- `PRODUCE_SEMANTIC_CERTAINTY` - Only semantic gates produce certainty

---

## T5 Role (What T5 IS)

T5 is a **bounded trace explainer** that may ONLY:

1. **Consume existing immutable `AlgorithmTracePayload`**
   - Never raw Arabic text
   - Never partial/incomplete traces
   - Never modified traces

2. **Produce bounded explanations**
   - Reference existing trace elements only
   - Explain what algorithms already produced
   - Provide natural language summaries

3. **Suggest repairs (NOT execute repairs)**
   - Identify blocking residuals
   - Suggest which gates might help
   - Require algorithm rerun for actual repair

---

## Permitted vs Forbidden Pipelines

### ❌ Forbidden Pipelines

```
Raw Arabic → T5 → Candidate         FORBIDDEN
Raw Arabic → T5 → Rank              FORBIDDEN
Raw Arabic → T5 → Meaning           FORBIDDEN
T5 → Residual Resolution            FORBIDDEN
T5 → Ifādah Closure                 FORBIDDEN
T5 → Hukm                           FORBIDDEN
T5 → Reality                        FORBIDDEN
T5 → New Constitutional Fact        FORBIDDEN
```

### ✅ Permitted Pipelines

```
AlgorithmTracePayload → GovernedTraceT5Input → ExplanationCandidate
AlgorithmTracePayload → GovernedTraceT5Input → RepairSuggestionCandidate
```

**Complete Permitted Flow:**
```
Raw Arabic
  → Arabic Algebra Algorithms
  → Candidate Objects (RelationCandidate, WordformCandidate, etc.)
  → AlgorithmTracePayload
  → GovernedTraceT5Input
  → [T5 Processing - FUTURE PR]
  → ExplanationCandidate / RepairSuggestionCandidate
```

---

## Contract Types

### 1. Input Contract: `GovernedTraceT5Input`

**Purpose:** Define what T5 may consume

**Fields:**
- `trace: AlgorithmTracePayload` (required) - The algorithm trace to consume
- `operation: TraceConsumerOperation` (required) - One of 5 permitted operations
- `context: Optional[TraceConsumerContext]` - Optional bounded context

**Validation Rules:**
- Input MUST be `AlgorithmTracePayload` (never raw Arabic string)
- Operation MUST be from permitted set
- Context MUST NOT contain forbidden instructions

**Example:**
```python
t5_input = GovernedTraceT5Input(
    trace=algorithm_trace_payload,
    operation=TraceConsumerOperation.EXPLAIN_TRACE,
    context=TraceConsumerContext(
        user_query="Explain this relation",
        explanation_scope="relations only",
        max_referenced_elements=10
    )
)
```

---

### 2. Output Type A: `ExplanationCandidate`

**Purpose:** T5-generated explanation of existing trace elements

**Constitutional Laws:**
1. ONLY explains what algorithms produced
2. CANNOT create new candidates
3. CANNOT modify ranks
4. CANNOT close ifadah
5. CANNOT produce hukm
6. MUST reference only existing trace elements

**Fields:**
- `source_trace_id: str` - References `AlgorithmTracePayload.source_algorithm`
- `operation: TraceConsumerOperation` - Which operation was performed
- `explanation_text: str` - Natural language explanation
- `referenced_candidate_ids: Tuple[str, ...]` - Read-only candidate references
- `referenced_rank_values: Tuple[str, ...]` - Read-only rank references
- `referenced_residual_ids: Tuple[str, ...]` - Read-only residual references
- `referenced_gate_ids: Tuple[str, ...]` - Read-only gate references
- `confidence: float` - Explanation confidence [0.0, 1.0]

**Forbidden Fields (enforced by absence):**
- NO `new_candidate`
- NO `upgraded_rank`
- NO `resolved_residuals`
- NO `closed_ifadah`
- NO `produced_hukm`
- NO `produced_reality`
- NO `modified_trace`

**Example:**
```python
explanation = ExplanationCandidate(
    source_trace_id="RelationAlgebraCore",
    operation=TraceConsumerOperation.EXPLAIN_TRACE,
    explanation_text="This trace shows a predicative relation between زيد and قائم",
    referenced_candidate_ids=("cand_predicative_zayd_qaim",),
    referenced_rank_values=("HYPOTHESIS",),
    referenced_residual_ids=(),
    referenced_gate_ids=("PredicationGate",),
    confidence=0.85
)
```

---

### 3. Output Type B: `RepairSuggestionCandidate`

**Purpose:** T5-suggested repair that REQUIRES algorithm rerun

**Constitutional Laws:**
1. ONLY suggests repairs (NOT executes)
2. CANNOT resolve residuals
3. MUST require algorithm rerun
4. Actual repair belongs to algorithms/gates only

**Fields:**
- `source_trace_id: str` - References `AlgorithmTracePayload.source_algorithm`
- `blocked_by_residual_ids: Tuple[str, ...]` - Residual IDs blocking progress
- `suggested_gate: Optional[str]` - Which gate might resolve blockage
- `suggested_rerun: bool` - Whether algorithm rerun is suggested
- `explanation: str` - Why this repair might work
- `requires_algorithm_rerun: bool` - MUST always be `True`

**Forbidden Fields (enforced by absence):**
- NO `executed_repair`
- NO `new_candidate`
- NO `resolved_residuals`
- NO `upgraded_rank`
- NO `closed_ifadah`

**Example:**
```python
suggestion = RepairSuggestionCandidate(
    source_trace_id="RelationAlgebraCore",
    blocked_by_residual_ids=("residual_agreement_mismatch",),
    suggested_gate="AgreementGate",
    suggested_rerun=True,
    explanation="Rerun AgreementGate with explicit agreement evidence",
    requires_algorithm_rerun=True  # MUST be True
)
```

---

### 4. Context: `TraceConsumerContext`

**Purpose:** Optional bounded context for trace consumption

**Fields:**
- `user_query: Optional[str]` - User question about trace
- `explanation_scope: Optional[str]` - Scope limitation
- `max_referenced_elements: Optional[int]` - Limit on elements to reference

**Forbidden Context Content:**
- "create new candidate"
- "upgrade rank"
- "resolve residuals"
- "close ifadah"
- "produce hukm"

**Example:**
```python
context = TraceConsumerContext(
    user_query="Explain why this relation was constructed",
    explanation_scope="relations only",
    max_referenced_elements=10
)
```

---

## Validation: `GovernedTraceT5Validator`

**Purpose:** Enforce constitutional boundaries on T5 trace consumption

**Methods:**

1. **`validate_input(input: GovernedTraceT5Input)`**
   - Input must be `AlgorithmTracePayload` (not raw Arabic)
   - Operation must be permitted
   - Context must not contain forbidden instructions

2. **`validate_output(output: GovernedTraceT5Output)`**
   - Output must be `ExplanationCandidate` or `RepairSuggestionCandidate`
   - Output must not claim to create/modify constitutional facts

3. **`validate_explanation(explanation: ExplanationCandidate)`**
   - Explanation must reference only existing trace elements
   - Confidence must be in [0.0, 1.0]
   - No forbidden fields (new_candidate, upgraded_rank, etc.)

4. **`validate_repair_suggestion(suggestion: RepairSuggestionCandidate)`**
   - Suggestion must require algorithm rerun
   - No executed repair fields
   - No resolved residuals fields

5. **`validate_explanation_references(explanation, trace)`**
   - Explanation references must belong to source trace
   - No references to non-existent elements

---

## Permitted Operations

From `TraceConsumerOperation` enum (PR #141):

### ✅ Permitted (5 Operations)

1. **`EXPLAIN_TRACE`** - Explain algorithmic trace to user
2. **`SUMMARIZE_CANDIDATES`** - Summarize candidate set
3. **`EXPLAIN_EXISTING_RANK`** - Explain rank (NOT assign rank)
4. **`SUGGEST_REPAIR`** - Suggest repair (NOT execute repair)
5. **`GENERATE_BOUNDED_EXPLANATION`** - Generate natural language explanation

### ❌ Forbidden (6 Operations)

1. **`PRODUCE_HUKM`** - Create hukm from trace alone
2. **`CLOSE_IFADAH`** - Close ifadah from trace alone
3. **`CREATE_REALITY`** - Create reality claim from trace
4. **`UPGRADE_RANK`** - Upgrade epistemic rank without algorithm
5. **`DELETE_RESIDUALS`** - Delete residuals without discharge proof
6. **`CREATE_CANDIDATE`** - Create new candidate without algorithm

---

## Constitutional Enforcement Mechanisms

### 1. Structural Prevention (No Forbidden Fields)

`ExplanationCandidate` and `RepairSuggestionCandidate` are designed **without** fields for forbidden operations:

- NO `new_candidate` field
- NO `upgraded_rank` field
- NO `resolved_residuals` field
- NO `closed_ifadah` field
- NO `produced_hukm` field
- NO `produced_reality` field

**Enforcement:** Structure itself prevents forbidden operations.

### 2. Validation Guards

`__post_init__` methods enforce:
- Required fields present
- Types correct
- Bounds validated (e.g., confidence in [0.0, 1.0])
- Constitutional requirements (e.g., `requires_algorithm_rerun=True`)

### 3. Validator Layer

`GovernedTraceT5Validator` provides additional enforcement:
- Input must be `AlgorithmTracePayload`
- Operation must be permitted
- References must belong to source trace
- No forbidden attributes exist

### 4. Test Suite

Comprehensive tests prove:
- Raw Arabic input is rejected
- Explanation cannot create candidate
- Explanation cannot modify rank
- Explanation cannot close ifadah
- Explanation cannot produce hukm/reality
- Repair suggestion cannot execute repair
- Repair suggestion cannot resolve residuals
- Repair suggestion must require rerun
- All contract dataclasses are frozen/immutable

---

## Integration with Architecture

### Layer Position

```
Layer 0: Raw Arabic Input
  ↓
Layer 1-N: Arabic Algebra Algorithms
  ↓
  → Candidate Objects (RelationCandidate, WordformCandidate, etc.)
  ↓
  → AlgorithmTracePayload (PR #141 - Serialization Layer)
  ↓
  → GovernedTraceT5Contract (PR #142 - THIS CONTRACT)
  ↓
  → [T5 Implementation - FUTURE PR #143+]
  ↓
  → ExplanationCandidate / RepairSuggestionCandidate
```

### Builds On

- **PR #141:** `AlgorithmTracePayload` - Immutable trace serialization contract
  - Provides input type for T5
  - Declares permitted/forbidden operations
  - Enforces non-authoritative audit evidence

### Enables (Future PRs)

- **PR #143:** Golden trace explanation fixtures
- **PR #144:** Dataset generator from traces
- **PR #145+:** T5 model integration (implementing THIS contract)

---

## What PR #142 Does NOT Include

This PR is **contract-only**. It does NOT include:

- ❌ T5 model loading or initialization
- ❌ Training pipeline or dataset generation
- ❌ Inference implementation
- ❌ Model weights or checkpoints
- ❌ FastAPI endpoints or web integration
- ❌ Complete pipeline from raw Arabic to explanation
- ❌ Any implementation that actually calls T5

**Scope:** Define types, validation, and constitutional boundaries only.

---

## Usage Examples

### Example 1: Explain Trace

```python
from dal_core.algorithm_trace_payload import AlgorithmTracePayload, TraceConsumerOperation
from dal_core.governed_trace_t5_contract import (
    GovernedTraceT5Input,
    ExplanationCandidate,
    TraceConsumerContext,
    GovernedTraceT5Validator,
)

# Step 1: Get algorithm trace (from algorithm execution)
trace: AlgorithmTracePayload = run_relation_algorithm("زيد قائم")

# Step 2: Create T5 input
t5_input = GovernedTraceT5Input(
    trace=trace,
    operation=TraceConsumerOperation.EXPLAIN_TRACE,
    context=TraceConsumerContext(
        user_query="Explain this relation",
        explanation_scope=None,
        max_referenced_elements=None
    )
)

# Step 3: Validate input
GovernedTraceT5Validator.validate_input(t5_input)

# Step 4: [FUTURE] Call T5 to produce explanation
# explanation = governed_t5.explain(t5_input)  # NOT IN PR #142

# Step 5: Validate output
# GovernedTraceT5Validator.validate_output(explanation)
```

### Example 2: Suggest Repair

```python
from dal_core.algorithm_trace_payload import AlgorithmTracePayload, TraceConsumerOperation
from dal_core.governed_trace_t5_contract import (
    GovernedTraceT5Input,
    RepairSuggestionCandidate,
    GovernedTraceT5Validator,
)

# Step 1: Get blocked algorithm trace
trace: AlgorithmTracePayload = run_blocked_algorithm("test input")

# Step 2: Create T5 input for repair suggestion
t5_input = GovernedTraceT5Input(
    trace=trace,
    operation=TraceConsumerOperation.SUGGEST_REPAIR,
    context=None
)

# Step 3: Validate input
GovernedTraceT5Validator.validate_input(t5_input)

# Step 4: [FUTURE] Call T5 to suggest repair
# suggestion = governed_t5.suggest_repair(t5_input)  # NOT IN PR #142

# Step 5: Validate output
# GovernedTraceT5Validator.validate_output(suggestion)
# assert suggestion.requires_algorithm_rerun is True
```

---

## Testing Strategy

### Test Categories (33 Tests)

1. **Input Validation (6 tests)**
   - Input requires `AlgorithmTracePayload`
   - Input rejects raw Arabic string
   - Input requires permitted operation
   - Input rejects forbidden operation
   - Context rejects forbidden instructions
   - Context allows valid queries

2. **ExplanationCandidate (10 tests)**
   - Basic construction
   - Requires source_trace_id
   - Requires permitted operation
   - Validates confidence bounds
   - Has no `create_candidate` field
   - Has no `upgrade_rank` field
   - Has no `close_ifadah` field
   - Has no `produce_hukm` field
   - Has no `produce_reality` field
   - Is immutable (frozen)

3. **RepairSuggestionCandidate (5 tests)**
   - Basic construction
   - Requires algorithm rerun (MUST be True)
   - Has no `executed_repair` field
   - Has no `resolved_residuals` field
   - Has no `new_candidate` field

4. **Validator Enforcement (6 tests)**
   - Validates input
   - Rejects raw Arabic input
   - Validates explanation
   - Validates repair suggestion
   - Validates output union
   - Validates explanation references

5. **Immutability (4 tests)**
   - `GovernedTraceT5Input` is immutable
   - `ExplanationCandidate` is immutable
   - `RepairSuggestionCandidate` is immutable
   - `TraceConsumerContext` is immutable

6. **Complete Flow (2 tests)**
   - Complete T5 contract flow: Input → Explanation
   - Complete T5 contract flow: Input → Repair Suggestion

---

## Constitutional Laws Summary

### Supreme Law

```
T5 يستهلك الأثر، ولا ينشئ الحكم الدستوري
(T5 consumes traces; T5 does not create constitutional facts)
```

### 11 Constitutional Laws

1. T5 input MUST be `AlgorithmTracePayload` (never raw Arabic)
2. T5 operation MUST be from permitted set
3. `ExplanationCandidate` CANNOT create candidates
4. `ExplanationCandidate` CANNOT modify rank
5. `ExplanationCandidate` CANNOT close ifadah
6. `ExplanationCandidate` CANNOT produce hukm
7. `ExplanationCandidate` CANNOT produce reality
8. `ExplanationCandidate` MUST reference only existing trace elements
9. `RepairSuggestionCandidate` CANNOT execute repairs
10. `RepairSuggestionCandidate` CANNOT resolve residuals
11. `RepairSuggestionCandidate` MUST require algorithm rerun

---

## Verification Checklist

PR #142 is complete when:

- [x] Contract types defined in `src/dal_core/governed_trace_t5_contract.py`
- [x] All contract types are frozen/immutable (`frozen=True`)
- [x] Forbidden operations documented in `ForbiddenT5Operation` enum
- [x] Validators enforce constitutional boundaries
- [x] Tests prove constitutional laws (33 tests)
- [x] Tests prove raw Arabic input is rejected
- [x] Tests prove explanation cannot create candidates
- [x] Tests prove explanation cannot modify rank
- [x] Tests prove explanation cannot close ifadah
- [x] Tests prove explanation cannot produce hukm/reality
- [x] Tests prove repair suggestion cannot execute repairs
- [x] Tests prove repair suggestion must require rerun
- [x] Tests prove all dataclasses are immutable
- [x] Documentation explains constitutional boundaries

---

## Future Work (NOT in PR #142)

### PR #143: Golden Trace Explanation Fixtures
- Create example traces with expected explanations
- Test data for T5 training/evaluation

### PR #144: Dataset Generator from Traces
- Generate training data from algorithm traces
- Format for T5 fine-tuning

### PR #145+: T5 Model Integration
- Load pre-trained T5 model
- Implement `GovernedTraceT5` class
- Fine-tune on golden fixtures
- Implement inference respecting contract
- Add FastAPI endpoints (if needed)

---

## References

- **PR #141:** AlgorithmTracePayload (builds on)
- **User Requirement:** PR #142 specification (2026-05-28)
- **Constitutional Formula:** T5 يشرح أثر طبقة أنتجتها الخوارزمية

---

**Document Version:** 1.0
**Last Updated:** 2026-05-28
**Status:** Contract Specification Complete
