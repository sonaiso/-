# Golden Trace Explanation Fixtures

**PR #144**: Constitutional fixtures proving `GovernedTraceT5Contract` works on realistic trace examples.

## Purpose

These fixtures demonstrate that the `GovernedTraceT5Contract` (PR #142) enforces constitutional boundaries:

1. **T5 explains only what traces contain** - All references must exist in the source trace
2. **T5 cannot invent references** - No phantom candidates, residuals, gates, or ranks
3. **T5 cannot analyze raw Arabic** - Only consumes `AlgorithmTracePayload`
4. **T5 cannot create/upgrade/resolve/close** - Structural absence of forbidden fields

## Fixture Families

### 1. Valid Explanation (Golden Path)

**File**: `tests/fixtures/golden_trace_explanation_fixtures.py::create_valid_explanation_fixture()`

**Scenario**: Algorithm produces trace with candidates, residuals, ranks, and gates. T5 explains the trace referencing only existing elements.

**Proves**:
- `ExplanationCandidate` can reference existing trace elements
- All references validate successfully
- Explanation text can describe trace content

**Test Coverage**: 6 tests

---

### 2. Valid Repair Suggestion

**File**: `tests/fixtures/golden_trace_explanation_fixtures.py::create_valid_repair_suggestion_fixture()`

**Scenario**: Algorithm produces trace with blocking residuals. T5 suggests repair requiring algorithm rerun.

**Proves**:
- `RepairSuggestionCandidate.requires_algorithm_rerun` MUST be `True`
- T5 does NOT execute repairs
- T5 does NOT resolve residuals
- T5 does NOT create repaired candidates

**Test Coverage**: 6 tests

---

### 3. Invalid Invented Candidate

**File**: `tests/fixtures/golden_trace_explanation_fixtures.py::create_invalid_invented_candidate_fixture()`

**Scenario**: T5 explanation references `candidate_id` that does NOT exist in trace.

**Proves**:
- `GovernedTraceT5Validator.validate_explanation_references()` MUST reject
- T5 cannot invent candidate IDs

**Test Coverage**: 3 tests

---

### 4. Invalid Invented Residual

**File**: `tests/fixtures/golden_trace_explanation_fixtures.py::create_invalid_invented_residual_fixture()`

**Scenario**: T5 explanation references `residual_id` (via `str(residual)`) that does NOT exist in trace.

**Proves**:
- Validator MUST reject invented residual references
- T5 cannot claim residuals not in trace

**Test Coverage**: 3 tests

---

### 5. Invalid Invented Gate/Operation

**File**: `tests/fixtures/golden_trace_explanation_fixtures.py::create_invalid_invented_gate_fixture()`

**Scenario**: T5 explanation references `gate_id` that does NOT exist in trace.

**Proves**:
- Validator MUST reject invented gate/operation references
- T5 cannot claim gates not in trace provenance

**Test Coverage**: 3 tests

---

### 6. Invalid Rank Claim

**File**: `tests/fixtures/golden_trace_explanation_fixtures.py::create_invalid_rank_claim_fixture()`

**Scenario**: Trace has `HYPOTHESIS` rank. T5 claims `CERTIFICATE` rank (NOT in trace).

**Proves**:
- Validator MUST reject rank values not present in trace
- T5 cannot upgrade rank

**Test Coverage**: 3 tests

---

### 7. Wrong Trace (Different `trace_id`)

**File**: `tests/fixtures/golden_trace_explanation_fixtures.py::create_wrong_trace_fixture()`

**Scenario**: Two traces from SAME algorithm but DIFFERENT `trace_id`. Explanation for trace A must NOT validate against trace B.

**Proves**:
- Explanations bind to SPECIFIC `trace_id`, NOT algorithm name
- `source_trace_id` is constitutional binding, not documentary label

**Critical Law**: `trace_id` identifies a specific execution instance. `source_algorithm` identifies the algorithm class. T5 explanations bind to execution instances, not algorithm classes.

**Test Coverage**: 5 tests

---

### 8. Raw Arabic Bypass Attempt

**File**: `tests/fixtures/golden_trace_explanation_fixtures.py::create_raw_arabic_bypass_fixture()`

**Scenario**: Attempt to create `GovernedTraceT5Input` with raw Arabic string instead of `AlgorithmTracePayload`.

**Proves**:
- `GovernedTraceT5Input` constructor MUST reject raw strings
- Type system prevents raw Arabic analysis

**Test Coverage**: 2 tests

---

### 9. Immutability Preservation

**File**: `tests/fixtures/golden_trace_explanation_fixtures.py::create_immutability_fixture()`

**Scenario**: Create trace → Create input → Create explanation → Verify trace unchanged.

**Proves**:
- `AlgorithmTracePayload` is frozen (immutable)
- `GovernedTraceT5Input` is frozen
- `ExplanationCandidate` is frozen
- Consuming trace does NOT mutate original

**Test Coverage**: 5 tests

---

## Constitutional Laws Demonstrated

### Law 1: T5 Explains ONLY What Trace Contains

**Evidence**:
- Valid explanation fixture passes validation (references exist)
- Invalid invented fixtures fail validation (references missing)

**Tests**: `test_constitutional_law_t5_explains_only_what_trace_contains`

---

### Law 2: T5 Does NOT Analyze Raw Arabic

**Evidence**:
- Raw Arabic string cannot be used as `GovernedTraceT5Input`
- Type system prevents bypass

**Tests**: `test_constitutional_law_t5_does_not_analyze_raw_arabic`

---

### Law 3: T5 Does NOT Create Candidates

**Evidence**:
- `ExplanationCandidate` has no `new_candidate` field
- `RepairSuggestionCandidate` has no `create_candidate` field

**Tests**: `test_constitutional_law_t5_does_not_create_candidates`

---

### Law 4: T5 Does NOT Upgrade Rank

**Evidence**:
- `ExplanationCandidate` has no `upgraded_rank` field
- Invalid rank claim fails validation

**Tests**: `test_constitutional_law_t5_does_not_upgrade_rank`

---

### Law 5: T5 Does NOT Resolve Residuals

**Evidence**:
- `RepairSuggestionCandidate` has no `resolved_residuals` field
- `requires_algorithm_rerun` MUST be `True`

**Tests**: `test_constitutional_law_t5_does_not_resolve_residuals`

---

### Law 6: T5 Does NOT Close Ifādah

**Evidence**:
- `ExplanationCandidate` has no `close_ifadah` field

**Tests**: `test_constitutional_law_t5_does_not_close_ifadah`

---

### Law 7: T5 Does NOT Produce Hukm or Reality

**Evidence**:
- `ExplanationCandidate` has no `produce_hukm` or `produce_reality` fields

**Tests**: `test_constitutional_law_t5_does_not_produce_hukm_or_reality`

---

### Law 8: Trace ID Binding

**Evidence**:
- Explanation validates against correct trace (trace A)
- Explanation fails against wrong trace (trace B)
- Even though both traces from same algorithm

**Tests**: `test_constitutional_law_trace_id_binding`

---

### Law 9: Immutability Preservation

**Evidence**:
- All types are frozen dataclasses
- Trace unchanged after consumption

**Tests**: `test_constitutional_law_immutability_preservation`

---

## Test Statistics

- **Total Tests**: 46
- **Total Fixtures**: 9 fixture families
- **Positive Fixtures**: 2 (valid explanation, valid repair suggestion)
- **Negative Fixtures**: 6 (invented candidate/residual/gate/rank, wrong trace, raw Arabic bypass)
- **Invariant Fixtures**: 1 (immutability preservation)

---

## Usage

### Loading All Fixtures

```python
from tests.fixtures.golden_trace_explanation_fixtures import create_all_golden_fixtures

all_fixtures = create_all_golden_fixtures()
# Returns dict with keys:
# - "valid_explanation"
# - "valid_repair_suggestion"
# - "invalid_invented_candidate"
# - "invalid_invented_residual"
# - "invalid_invented_gate"
# - "invalid_rank_claim"
# - "wrong_trace"
# - "raw_arabic_bypass"
# - "immutability"
```

### Loading Individual Fixtures

```python
from tests.fixtures.golden_trace_explanation_fixtures import (
    create_valid_explanation_fixture,
    create_valid_repair_suggestion_fixture,
    # ... etc
)

fixture = create_valid_explanation_fixture()
assert fixture.trace.trace_id == "trace_golden_001"
```

---

## Residual ID Format

**Critical Note**: Residuals are referenced via their `str()` representation, NOT a separate `residual_id` field.

**Format**: `[{SEVERITY}] {type_in_arabic} at {location}: {message}`

**Example**:
```
"[WARNING] تحليل صرفي غير مكتمل at AgreementGate: Number agreement required"
```

---

## Future T5 Implementation Checklist

When implementing actual T5 inference (FUTURE PR, NOT this PR):

- [ ] T5 input MUST be `GovernedTraceT5Input` (not raw Arabic)
- [ ] T5 output MUST be `ExplanationCandidate` or `RepairSuggestionCandidate`
- [ ] Explanation MUST pass `validate_explanation_references()`
- [ ] Repair suggestion MUST have `requires_algorithm_rerun=True`
- [ ] No T5 output may contain forbidden fields
- [ ] All tests in `test_golden_trace_explanation_fixtures.py` MUST pass

---

## Constitutional Formula

```
T5 = مستهلك الأثر المحدد
(T5 = Consumer of Specific Trace)

NOT:
T5 ≠ محلل عربي    (T5 ≠ Arabic Analyzer)
T5 ≠ منشئ مرشحات  (T5 ≠ Candidate Generator)
T5 ≠ مُرقّي الرتبة (T5 ≠ Rank Upgrader)
T5 ≠ حلّال البقايا  (T5 ≠ Residual Resolver)
T5 ≠ مُغلق الإفادة (T5 ≠ Ifādah Closer)
T5 ≠ منتج الحكم    (T5 ≠ Hukm Producer)
```

---

## References

- **PR #141**: `AlgorithmTracePayload` serialization contract
- **PR #142**: `GovernedTraceT5Contract` boundary enforcement
- **PR #143**: Trace ID and provenance validation hardening
- **PR #144**: This PR - Golden trace explanation fixtures

---

**Created**: 2026-05-28
**Status**: All 46 tests passing ✅
**Constitutional Compliance**: Verified ✅
