# Layer Maturity Model
# نموذج نضج الطبقات

**Version**: 1.0.0
**Part of**: PR-D0 Dashboard Specification
**Date**: 2026-05-23

---

## 1. Maturity Levels

The Layer Maturity Model defines six distinct maturity levels, each with specific requirements and constraints.

### Level 0: GAP (0-9%)
**Status**: Missing or fundamentally conflicted

**Characteristics**:
- No implementation, or
- Critical claim conflicts, or
- Implementation contradicts documentation

**Requirements to Exit**:
- Create specification document
- Define typed contracts
- Resolve claim conflicts

**Example**: Layer A9 (General Cognitive Layers) - planned but not claimed as implemented

---

### Level 1: PLANNED (10-29%)
**Status**: Documented specification only

**Characteristics**:
- Specification exists
- No runtime code
- Design documented
- Claims clearly state "planned"

**Requirements to Exit**:
- Implement typed contracts (@dataclass with frozen=True)
- Create at least stub implementations
- Write first tests

**Example**: Original state of PR-L5 (Wadh) before implementation

---

### Level 2: DEMONSTRATOR (30-49%)
**Status**: Proof of concept with strings/booleans

**Characteristics**:
- Some runtime code exists
- Uses strings/booleans instead of typed candidates
- Basic tests exist
- Demonstrates concept but not production-ready

**Ceiling Triggers**:
- No typed contract → max 30%
- Strings/booleans instead of types → max 45%

**Requirements to Exit**:
- Replace strings with typed dataclasses
- Implement evidence tracking
- Add residual taxonomy
- Increase test coverage

**Example**: Current state of A7 (Ifādah) - boolean dict closure

---

### Level 3: PARTIAL (50-69%)
**Status**: Typed implementation, incomplete coverage

**Characteristics**:
- Typed contracts exist
- Runtime implementation works
- Tests exist but incomplete
- Some NoLeap guards missing
- Golden dataset absent or incomplete

**Ceiling Triggers**:
- No tests → max 50%
- No NoLeap tests → max 55%
- No golden dataset → max 70%

**Requirements to Exit**:
- Complete NoLeap test coverage (≥90%)
- Add trace/replay to all operations
- Create golden dataset (all case types)
- Resolve any remaining claim conflicts

**Example**: Current state of A2 (Pure Dāl) - typed but needs golden dataset

---

### Level 4: IMPLEMENTED (70-89%)
**Status**: Complete typed implementation with tests

**Characteristics**:
- Fully typed contracts
- Complete runtime implementation
- Comprehensive tests (≥90% coverage)
- NoLeap guards tested
- Trace/replay working
- Evidence policy defined
- Rank policy defined
- Residual taxonomy clear

**Ceiling Triggers**:
- Broken trace/replay → max 60%
- Claim conflicts → max 70%

**Requirements to Exit**:
- Add complete golden dataset
- Pass external audit
- Verify no claim inflation
- Ensure documentation accuracy

**Example**: Current state of A4 (Neutral Binding) - implemented, needs golden certification

---

### Level 5: CERTIFIED (90-100%)
**Status**: Production-ready with golden dataset

**Characteristics**:
- All IMPLEMENTED requirements met
- Complete golden dataset with all case types:
  - ≥5 positive cases
  - ≥3 negative cases
  - ≥2 ambiguous cases
  - ≥1 blocked (NoLeap) case
  - ≥1 rank-lowering case
- External audit passed
- Documentation verified accurate
- No claim conflicts
- Trace/replay validated
- Evidence requirements enforced

**Maintenance Requirements**:
- Regular golden dataset updates
- Continuous claim auditing
- Trace coverage monitoring

**Example**: Target state for A0 (Kernel) and A1 (Typed Layers)

---

## 2. Maturity Assessment Criteria

### 2.1 Typed Contract (15 points)

**CERTIFIED (13-15 points)**:
```python
# All of:
# 1. Frozen dataclasses
@dataclass(frozen=True)
class DalCandidate:
    surface_form: str
    phonic_carriers: Tuple[PhonicCarrier, ...]
    # ...

# 2. Protocols for interfaces
class DalCandidateProtocol(Protocol):
    def get_surface(self) -> str: ...

# 3. Enums for closed sets
class PathType(Enum):
    VERB = "verb"
    JAMID = "jamid"
    # ...

# 4. Type hints everywhere
def build_dal(raw: str) -> Result[DalCandidate]:
    ...
```

**IMPLEMENTED (10-12 points)**:
- Mostly typed, some `Any` types
- Some mutable classes
- Type hints ≥80%

**PARTIAL (5-9 points)**:
- Some typed contracts
- Mix of typed and untyped
- Type hints 50-79%

**DEMONSTRATOR (1-4 points)**:
- Minimal typing
- Mostly strings/dicts
- Type hints <50%

**GAP (0 points)**:
- No typed contracts

---

### 2.2 Runtime Implementation (20 points)

**CERTIFIED (18-20 points)**:
- Complete logic, no TODOs
- All paths implemented
- Error handling comprehensive
- No placeholder returns

**IMPLEMENTED (14-17 points)**:
- Core logic complete
- Minor TODOs acceptable
- Error handling present
- Edge cases handled

**PARTIAL (8-13 points)**:
- Core paths work
- Some TODOs remain
- Basic error handling
- Some edge cases missing

**DEMONSTRATOR (1-7 points)**:
- Basic proof of concept
- Many TODOs/stubs
- Minimal error handling
- Happy path only

**GAP (0 points)**:
- No implementation

---

### 2.3 Evidence Policy (10 points)

**CERTIFIED (9-10 points)**:
```python
# Layer-specific required evidence
required_evidence = {
    "CERTIFIED": [
        "transmission_evidence",
        "source_evidence",
        "scope_evidence",
        "structure_evidence"
    ],
    "LICENSED": [
        "transmission_evidence",
        "source_evidence"
    ],
    "CANDIDATE": [
        "source_evidence"
    ]
}

# Evidence types defined
@dataclass(frozen=True)
class WadhEvidence:
    evidence_type: WadhEvidenceType
    source: WadhSource
    strength: float
    trace: Trace
```

**IMPLEMENTED (7-8 points)**:
- Evidence types defined
- Generic requirements (not layer-specific)

**PARTIAL (4-6 points)**:
- Evidence mentioned
- No formal requirements

**DEMONSTRATOR (1-3 points)**:
- Evidence field exists
- No types or requirements

**GAP (0 points)**:
- No evidence policy

---

### 2.4 Rank Policy (10 points)

**CERTIFIED (9-10 points)**:
```python
# Layer-specific rank ceiling
def determine_rank(evidence: List[Evidence]) -> Rank:
    # Required evidence check
    if not has_required_evidence(evidence, "CERTIFIED"):
        max_rank = Rank.LICENSED

    # Quality check
    if any(e.strength < 0.8 for e in evidence):
        max_rank = Rank.CANDIDATE

    # Residual check
    if residuals:
        max_rank = Rank.PARTIAL

    return min(calculated_rank, max_rank)
```

**IMPLEMENTED (7-8 points)**:
- Rank ceiling exists
- Generic rules (not layer-specific)

**PARTIAL (4-6 points)**:
- Rank mentioned
- No ceiling enforcement

**DEMONSTRATOR (1-3 points)**:
- Rank field exists
- Always same value

**GAP (0 points)**:
- No rank policy

---

### 2.5 Residual Taxonomy (10 points)

**CERTIFIED (9-10 points)**:
```python
# Clear separation
class LinguisticResidual(Enum):
    MISSING_HARAKA = "missing_haraka"
    AMBIGUOUS_ROOT = "ambiguous_root"
    # ...

class ImplementationFailure(Enum):
    PARSING_ERROR = "parsing_error"
    INVALID_INPUT = "invalid_input"
    # ...

# Proper usage
Result(
    value=candidate,
    rank=Rank.CANDIDATE,
    residuals=frozenset([LinguisticResidual.MISSING_HARAKA]),
    failures=frozenset([]),  # No implementation failures
)
```

**IMPLEMENTED (7-8 points)**:
- Taxonomy defined
- Mostly used correctly
- Occasional misclassification

**PARTIAL (4-6 points)**:
- Some classification
- Mix of types in residuals

**DEMONSTRATOR (1-3 points)**:
- String residuals
- No taxonomy

**GAP (0 points)**:
- No residual tracking

---

### 2.6 NoLeap Tests (10 points)

**CERTIFIED (9-10 points)**:
- All forbidden transitions tested (100%)
- Tests verify guards work
- Tests check error messages

**IMPLEMENTED (7-8 points)**:
- Most transitions tested (≥90%)

**PARTIAL (4-6 points)**:
- Some transitions tested (50-89%)

**DEMONSTRATOR (1-3 points)**:
- Few transitions tested (<50%)

**GAP (0 points)**:
- No NoLeap tests

**Example**:

```python
def test_noleap_dal_cannot_create_meaning():
    """A2→A5 leap forbidden: Dāl CANNOT create meaning directly."""
    dal = build_dal_candidate("كتب")

    # Guard 1: No meaning field
    assert not hasattr(dal, "meaning")

    # Guard 2: Attempting access raises error
    with pytest.raises(AttributeError, match="meaning"):
        _ = dal.meaning

    # Guard 3: No wadh field
    assert not hasattr(dal, "wadh")
```

---

### 2.7 Trace/Replay (10 points)

**CERTIFIED (9-10 points)**:
```python
# Complete trace
result = operation.apply(input)
assert result.trace is not None
assert result.trace.source == "input_text"
assert result.trace.operation == "build_dal"
assert result.trace.is_reversible()

# Replay works
replayed = result.trace.replay()
assert replayed == result.value
```

**IMPLEMENTED (7-8 points)**:
- Trace exists
- Replay works for most cases

**PARTIAL (4-6 points)**:
- Trace field present
- Replay not implemented

**DEMONSTRATOR (1-3 points)**:
- Trace is string
- No replay

**GAP (0 points)**:
- No trace

---

### 2.8 Golden Dataset (10 points)

**CERTIFIED (9-10 points)**:
- All case types covered:
  - ≥5 positive cases (should succeed)
  - ≥3 negative cases (should fail gracefully)
  - ≥2 ambiguous cases (multiple interpretations)
  - ≥1 blocked case (NoLeap guard triggers)
  - ≥1 rank-lowering case (insufficient evidence)
- Tests use golden dataset
- Dataset documented

**IMPLEMENTED (7-8 points)**:
- Most case types (≥4/5)
- Good coverage

**PARTIAL (4-6 points)**:
- Some case types (2-3/5)
- Basic coverage

**DEMONSTRATOR (1-3 points)**:
- Only positive cases
- Minimal coverage

**GAP (0 points)**:
- No golden dataset

**Example**:

```python
# tests/gfa/methods/golden/test_dal_golden_dataset.py
GOLDEN_POSITIVE = [
    "كتب",    # Simple trilateral
    "الكتاب",  # With AL prefix
    "كاتب",    # Active participle
    "مكتوب",   # Passive participle
    "كتابة",   # Masdar
]

GOLDEN_NEGATIVE = [
    "",        # Empty input
    "123",     # Non-Arabic
    "ك",       # Too short
]

GOLDEN_AMBIGUOUS = [
    "قال",     # Multiple roots possible
    "بار",     # Rare/foreign
]

GOLDEN_BLOCKED = [
    # These should NOT produce meaning (NoLeap)
    ("كتب", "meaning"),  # Dāl → meaning forbidden
]

GOLDEN_RANK_LOWERING = [
    ("كتب", "no_haraka"),  # Missing diacritics → CANDIDATE
]
```

---

### 2.9 Documentation Honesty (5 points)

**CERTIFIED (5 points)**:
- Docs match code exactly
- Claims verified
- Status clearly stated
- No inflation

**IMPLEMENTED (4 points)**:
- Minor wording issues
- Generally accurate

**PARTIAL (2-3 points)**:
- Some discrepancies
- Ambiguous claims

**DEMONSTRATOR (1 point)**:
- Misleading wording
- Overstated claims

**GAP (0 points)**:
- False claims
- Major conflicts

---

## 3. Layer Transition Rules

### 3.1 Entry Requirements

| From | To | Requirements |
|------|-----|-------------|
| GAP | PLANNED | Specification document, claim conflicts resolved |
| PLANNED | DEMONSTRATOR | Typed contract stub, 1+ test |
| DEMONSTRATOR | PARTIAL | Replace strings with types, evidence tracking |
| PARTIAL | IMPLEMENTED | NoLeap tests ≥90%, trace/replay working |
| IMPLEMENTED | CERTIFIED | Golden dataset complete, external audit |

### 3.2 Exit Requirements

Layers CANNOT advance if:
- Previous layer is GAP or PLANNED
- Claim conflicts unresolved
- Tests failing
- NoLeap guards untested
- Trace/replay broken

**Example**:

```
Layer A5 (Wadh) wants to advance to IMPLEMENTED:
  - Check: A4 (Binding) status → IMPLEMENTED ✓
  - Check: Typed contracts → ✓
  - Check: Tests passing → ✓
  - Check: NoLeap coverage → 50% ✗ BLOCKED
  - Result: A5 remains PARTIAL until NoLeap coverage ≥90%
```

---

## 4. Ceiling Enforcement

### 4.1 Automatic Caps

```python
def apply_maturity_ceiling(layer: Layer, raw_score: int) -> int:
    """
    Apply maturity-based ceiling.

    Ceilings cascade: multiple violations = lowest cap.
    """
    caps = []

    # Critical caps (0-30%)
    if not layer.has_typed_contract:
        caps.append(30)

    if layer.has_critical_claim_conflict:
        caps.append(0)

    # Major caps (30-50%)
    if layer.uses_strings_not_types:
        caps.append(45)

    if not layer.has_tests:
        caps.append(50)

    # Moderate caps (50-60%)
    if not layer.has_noleap_tests:
        caps.append(55)

    if layer.trace_broken:
        caps.append(60)

    # Minor caps (60-70%)
    if layer.has_claim_conflict:
        caps.append(70)

    if not layer.has_golden_dataset:
        caps.append(70)

    # Apply lowest cap
    if caps:
        return min(raw_score, min(caps))

    return raw_score
```

### 4.2 Manual Overrides

**Allowed overrides** (with justification):
- Experimental features (explicitly labeled)
- Research prototypes (separate from production)

**Forbidden overrides**:
- Production code
- Claimed features
- Core layers (A0-A8)

---

## 5. Example Layer Assessments

### Example 1: A0 (Algebra Kernel)

```yaml
layer_id: A0
name: Algebra Kernel
principle: Result/Rank/Evidence/Residual/Trace foundation

assessment:
  typed_contract: 15/15        # Complete typed contracts
  runtime: 20/20               # Full implementation
  evidence_policy: 10/10       # Evidence types defined
  rank_policy: 9/10            # Generic policy (needs layer-specific)
  residual_taxonomy: 10/10     # Clear separation
  noleap_tests: 10/10          # All tested
  trace_replay: 9/10           # Works, needs usage audit
  golden_dataset: 0/10         # Missing
  doc_honesty: 5/5             # Accurate

raw_score: 88
ceiling: 70  # No golden dataset
capped_score: 70

maturity: IMPLEMENTED
next_step: Add golden dataset → CERTIFIED
```

### Example 2: A5 (Wadh Geometry)

```yaml
layer_id: A5
name: Wadh Geometry
principle: يرخّص المعنى (licenses meaning)

assessment:
  typed_contract: 12/15        # Mostly typed, some strings
  runtime: 15/20               # Core works, some stubs
  evidence_policy: 8/10        # Evidence defined
  rank_policy: 7/10            # Basic policy
  residual_taxonomy: 8/10      # Mostly clear
  noleap_tests: 5/10           # 50% coverage
  trace_replay: 8/10           # Works
  golden_dataset: 0/10         # Missing
  doc_honesty: 4/5             # Minor issues

raw_score: 67
ceiling: 45  # Uses strings (mawdu_lah as string gloss)
capped_score: 45

maturity: DEMONSTRATOR
next_step: Replace strings with typed MawduLahStructure
```

### Example 3: A7 (Ifādah)

```yaml
layer_id: A7
name: Nisbah/Ifādah
principle: تكمل النسبة (completes predication)

assessment:
  typed_contract: 3/15         # Minimal typing
  runtime: 8/20                # Boolean dict closure
  evidence_policy: 3/10        # Mentioned only
  rank_policy: 2/10            # Not enforced
  residual_taxonomy: 5/10      # Some separation
  noleap_tests: 2/10           # 20% coverage
  trace_replay: 5/10           # Partial
  golden_dataset: 0/10         # Missing
  doc_honesty: 2/5             # Claims "implemented"

raw_score: 30
ceiling: 45  # Boolean dict (not typed closure)
capped_score: 30

maturity: DEMONSTRATOR
next_step: Create typed IfadahClosure contract
```

---

## 6. Maturity Progression Paths

### Path 1: New Layer (from scratch)

```
GAP (0%) → Specification
  ↓
PLANNED (15%) → Typed contracts
  ↓
DEMONSTRATOR (35%) → Replace strings with types
  ↓
PARTIAL (58%) → Add NoLeap tests + golden dataset
  ↓
IMPLEMENTED (78%) → External audit
  ↓
CERTIFIED (92%)
```

### Path 2: Existing Demonstrator (upgrade)

```
DEMONSTRATOR (45%) → Replace strings
  ↓
PARTIAL (62%) → Add tests
  ↓
PARTIAL (68%) → Add NoLeap tests
  ↓
IMPLEMENTED (76%) → Add golden dataset
  ↓
CERTIFIED (94%)
```

### Path 3: Implemented (certification)

```
IMPLEMENTED (78%) → Create golden dataset
  ↓
IMPLEMENTED (82%) → Fix claim conflicts
  ↓
IMPLEMENTED (87%) → External audit
  ↓
CERTIFIED (93%)
```

---

## 7. Governance Rules

### 7.1 Layer Dependencies

**Rule**: A layer CANNOT reach maturity level N if any prerequisite layer is below level N-1.

```
A5 (Wadh) wants CERTIFIED:
  Prerequisites: A2 (Dāl), A3 (Madlūl), A4 (Binding)
  Check: All must be ≥ IMPLEMENTED
  If A3 is DEMONSTRATOR → A5 blocked from CERTIFIED
```

### 7.2 Claim Consistency

**Rule**: Documentation maturity claims MUST NOT exceed code maturity.

```
# FORBIDDEN
README.md: "Ifādah fully implemented and certified"
Code maturity: DEMONSTRATOR (30%)

# ALLOWED
README.md: "Ifādah demonstrator implemented (30% maturity)"
Code maturity: DEMONSTRATOR (30%)
```

### 7.3 Test Requirements

**Rule**: Maturity level ≥ PARTIAL requires tests.

```
# FORBIDDEN
Maturity: PARTIAL (55%)
Tests: 0

# ALLOWED
Maturity: DEMONSTRATOR (35%)
Tests: 0 (acceptable at this level)
```

---

## 8. Audit Checklist

For each layer, verify:

- [ ] Typed contract exists and complete
- [ ] Runtime implementation matches spec
- [ ] Evidence policy defined and enforced
- [ ] Rank policy defined with ceiling
- [ ] Residual taxonomy clear (linguistic vs implementation)
- [ ] NoLeap tests cover ≥90% of forbidden transitions
- [ ] Trace/replay working and tested
- [ ] Golden dataset complete (all case types)
- [ ] Documentation accurate (no claim inflation)
- [ ] Prerequisites at adequate maturity
- [ ] No claim conflicts
- [ ] CI passing

---

**Document Status**: SPECIFICATION (PR-D0)
**Last Updated**: 2026-05-23
**Next Review**: After PR-D1 implementation
