# Next Phase Plan: Foundation Hardening

**Phase Name**: Foundation Hardening
**Status**: Required before new layer implementation
**Priority**: CRITICAL
**Blocking**: All cognitive layer expansion (Tasawwur/Nisbah/Ifadah/Hukm)

---

## Rationale

The constitutional foundation (Result contract, CPB, Rank policy) is **solid and enforced**. However, **7 critical governance gaps** prevent safe expansion:

1. No separation of linguistic residuals from implementation failures
2. No automatic rank ceiling enforcement
3. No formal LayerSpec contract
4. No golden dataset validation
5. No PriorInformationSystem formal contract
6. No general governed_binding function
7. Missing cognitive layers (Tasawwur through Hukm)

**Building new layers without fixing these gaps risks**:
- Runtime exceptions becoming "acceptable residuals"
- Rank inflation (CANDIDATE → CERTIFIED without validation)
- Layer leaps (bypassing intermediate layers)
- Claim inflation (overclaiming capabilities)

**Solution**: Three foundation hardening PRs **before** any new layer work.

---

## The Three Critical PRs

### PR-F1: Residual Taxonomy Formalization ⚠️ CRITICAL

**Priority**: HIGHEST (blocks all other work)

**Problem**:
PR #75 shows `success=True` with `residuals={'c2a_phonology_error:AttributeError'}`. Implementation exceptions are being treated as linguistic residuals.

**Goal**: Separate linguistic residuals from implementation failures at the type level.

**Deliverables**:

1. **Create `src/gfa/governance/residual_taxonomy.py`**:
```python
from dataclasses import dataclass
from enum import Enum, auto
from typing import FrozenSet

class ResidualType(Enum):
    LINGUISTIC = auto()          # missing_haraka, ambiguous_formula
    IMPLEMENTATION = auto()      # AttributeError, Exception, gate_crash

@dataclass(frozen=True)
class ResidualTaxonomy:
    """Classifies residuals into linguistic (acceptable) vs implementation (blocking)"""

    linguistic_patterns: FrozenSet[str]
    implementation_patterns: FrozenSet[str]

    def classify(self, residual: str) -> ResidualType:
        """Classify a residual string"""
        # Check implementation patterns first (more specific)
        if any(pattern in residual for pattern in self.implementation_patterns):
            return ResidualType.IMPLEMENTATION

        # Default to linguistic
        return ResidualType.LINGUISTIC

    def validate_success_residuals(self, residuals: FrozenSet[str], success: bool) -> bool:
        """Validate that successful results don't contain implementation failures"""
        if not success:
            return True  # Failed results can have any residuals

        for residual in residuals:
            if self.classify(residual) == ResidualType.IMPLEMENTATION:
                return False  # SUCCESS with implementation failure is invalid

        return True

# Standard taxonomy
STANDARD_TAXONOMY = ResidualTaxonomy(
    linguistic_patterns=frozenset([
        "missing_haraka",
        "ambiguous_formula",
        "context_absent",
        "lexical_ambiguity",
        "proper_name_possible",
        "transfer_possible",
        "weak_letter_present",
        "affix_aggressive_strip",
        "root_ambiguous",
        "pattern_collision",
        "broken_plural_possible",
    ]),
    implementation_patterns=frozenset([
        "Error",      # AttributeError, ValueError, TypeError, etc.
        "Exception",  # All exception types
        "gate_crash",
        "internal_failure",
        "validation_failure",
    ])
)
```

2. **Update `src/fvafk/algebra/core.py` Result validation**:
```python
from gfa.governance.residual_taxonomy import STANDARD_TAXONOMY

@dataclass(frozen=True)
class Result(Generic[T]):
    # ... existing fields ...

    def __post_init__(self):
        # ... existing validation ...

        # NEW: Validate residuals are appropriate for success status
        if hasattr(self, 'success'):
            if not STANDARD_TAXONOMY.validate_success_residuals(self.residuals, self.success):
                raise ValueError(
                    f"Result cannot be success=True with implementation failure residuals. "
                    f"Found: {[r for r in self.residuals if 'Error' in r or 'Exception' in r]}"
                )
```

3. **Fix PR #75 DalCandidateBuilder**:
```python
# BEFORE (incorrect):
result = BuilderResult(
    success=True,
    residuals={'c2a_phonology_error:AttributeError'}
)

# AFTER (correct):
result = BuilderResult(
    success=False,  # Implementation failure blocks success
    status=Status.BLOCKED,
    residuals={'c2a_phonology_error:AttributeError'},
    failure_kind=FailureKind.INTERNAL_FAILURE
)
```

4. **Create `tests/gfa/governance/test_residual_taxonomy.py`** (20 tests):
- Test linguistic residual classification
- Test implementation failure classification
- Test success validation (must reject implementation failures)
- Test blocked validation (can contain implementation failures)
- Test edge cases (empty string, mixed residuals)

**Exit Criterion**:
- ✅ All 20 taxonomy tests pass
- ✅ Result.__post_init__ blocks success with implementation failures
- ✅ PR #75 fixed to use correct failure handling
- ✅ All existing tests remain green

**Estimated Scope**: 1 new file, 2 modified files, 20 new tests

---

### PR-F2: Rank Policy Hardening ⚠️ CRITICAL

**Priority**: HIGH (blocks cognitive layers)

**Problem**:
No automatic enforcement of rank ceilings. Later layer success can manually promote earlier layer rank. No automatic downgrade when ambiguity increases.

**Goal**: Enforce rank ceilings and automatic downgrades at the operation level.

**Deliverables**:

1. **Create `src/gfa/governance/rank_policy.py`**:
```python
from dataclasses import dataclass
from typing import Dict, Optional
from fvafk.algebra.core import Rank

@dataclass(frozen=True)
class RankCeiling:
    """Defines maximum rank an operation can produce given input rank"""

    operation_type: str
    input_rank: Rank
    max_output_rank: Rank
    reason: str

class RankPolicy:
    """Enforces rank ceilings and downgrades"""

    ceilings: Dict[tuple[str, Rank], Rank]

    def __init__(self):
        # Rule: نجاح طبقة لا يرفع رتبة الطبقة التالية
        # (Success of later layer does not raise rank of earlier layer)
        self.ceilings = {
            # Binding operations
            ("neutral_binding", Rank.CANDIDATE): Rank.LICENSED,  # ceiling
            ("neutral_binding", Rank.LICENSED): Rank.LICENSED,   # preserve
            ("dal_madlul_binding", Rank.CANDIDATE): Rank.LICENSED,
            ("dal_madlul_binding", Rank.LICENSED): Rank.LICENSED,

            # Wadh operations
            ("wadh_gate", Rank.UNRESOLVED): Rank.BLOCKED,  # too weak
            ("wadh_gate", Rank.CANDIDATE): Rank.BLOCKED,    # too weak
            ("wadh_gate", Rank.LICENSED): Rank.LICENSED,    # minimum required
            ("wadh_gate", Rank.CERTIFIED): Rank.LICENSED,   # cannot auto-certify

            # Morphology
            ("root_extraction", Rank.CANDIDATE): Rank.LICENSED,
            ("pattern_match", Rank.CANDIDATE): Rank.LICENSED,
        }

    def enforce_ceiling(self, operation_type: str, input_rank: Rank) -> Rank:
        """Get maximum allowed output rank for operation given input rank"""
        key = (operation_type, input_rank)
        return self.ceilings.get(key, input_rank)  # default: preserve input

    def should_downgrade(self, residuals: FrozenSet[str], current_rank: Rank) -> Optional[Rank]:
        """Determine if rank should be downgraded based on residuals"""
        # High-severity residuals force downgrade
        high_severity = {
            "path_type_unknown",
            "ambiguous_formula",
            "root_ambiguous",
            "context_absent",
        }

        if any(r in residuals for r in high_severity):
            if current_rank == Rank.CERTIFIED:
                return Rank.LICENSED  # cannot certify with high-severity residuals
            elif current_rank == Rank.LICENSED:
                return Rank.CANDIDATE  # downgrade to candidate

        return None  # no downgrade needed

GLOBAL_RANK_POLICY = RankPolicy()
```

2. **Update operation implementations** to use ceiling enforcement:
```python
# Example: src/gfa/methods/lafzi_dalalah/dal_madlul_binding_gate.py
from gfa.governance.rank_policy import GLOBAL_RANK_POLICY

def process_binding(dal: DalCandidate, madlul: MadlulCandidate) -> BindingResult:
    # ... existing logic ...

    # Enforce rank ceiling
    max_rank = GLOBAL_RANK_POLICY.enforce_ceiling("dal_madlul_binding", dal.rank)
    result_rank = min(computed_rank, max_rank)

    # Check for auto-downgrade
    downgrade = GLOBAL_RANK_POLICY.should_downgrade(result_residuals, result_rank)
    if downgrade:
        result_rank = downgrade

    return BindingResult(rank=result_rank, ...)
```

3. **Add rank guard to WadhGate**:
```python
# src/gfa/methods/lafzi_wadh/wadh_gate.py
def admit_wadh_claim(dal: DalCandidate, ...) -> WadhResult:
    # NEW: Verify Dal rank is strong enough
    if dal.rank not in {Rank.LICENSED, Rank.CONTEXTUAL, Rank.CERTIFIED}:
        return blocked("dal_rank_too_low_for_wadh")

    # ... existing logic ...
```

4. **Create `tests/gfa/governance/test_rank_policy.py`** (25 tests):
- Test ceiling enforcement for each operation type
- Test automatic downgrades
- Test Wadh gate rank guard
- Test prevention of CANDIDATE → CERTIFIED inflation
- Test rank preservation when appropriate

**Exit Criterion**:
- ✅ All 25 rank policy tests pass
- ✅ WadhGate blocks weak Dal
- ✅ Binding operations respect ceilings
- ✅ Automatic downgrade on high-severity residuals
- ✅ All existing tests remain green

**Estimated Scope**: 1 new file, 3 modified files, 25 new tests

---

### PR-F3: LayerSpec Contract ⚠️ CRITICAL

**Priority**: HIGH (enables systematic layer expansion)

**Problem**:
Layers have implicit contracts. No machine-enforceable specification of layer boundaries, forbidden outputs, or required evidence.

**Goal**: Create explicit typed layer specifications with runtime validation.

**Deliverables**:

1. **Create `src/gfa/governance/layer_spec.py`**:
```python
from dataclasses import dataclass
from typing import FrozenSet, Type, Callable, Any
from fvafk.algebra.core import Rank, Evidence, Residual

@dataclass(frozen=True)
class LayerSpec:
    """Formal specification of a cognitive/linguistic layer"""

    name: str                                    # "PURE_DAL", "WADH", "TASAWWUR"
    domain: str                                  # "LAFZI_DALALI", "COGNITIVE"
    input_type: Type                             # Expected input type
    output_type: Type                            # Expected output type
    allowed_operations: FrozenSet[str]           # {"build", "bind", "filter"}
    forbidden_outputs: FrozenSet[str]            # {"meaning", "dalalah", "hukm"}
    required_evidence_kinds: FrozenSet[str]      # {"c2b_analysis", "lexicon_report"}
    residual_policy: str                         # "PRESERVE", "ACCUMULATE", "BLOCK"
    rank_policy: str                             # "CEILING_LICENSED", "ALLOW_CERTIFIED"
    min_input_rank: Rank                         # Minimum rank to process
    max_output_rank: Rank                        # Maximum rank to emit

    def validate_input(self, obj: Any) -> bool:
        """Validate input matches expected type"""
        return isinstance(obj, self.input_type)

    def validate_output(self, obj: Any) -> bool:
        """Validate output matches expected type and contains no forbidden fields"""
        if not isinstance(obj, self.output_type):
            return False

        # Check forbidden outputs
        for forbidden in self.forbidden_outputs:
            if hasattr(obj, forbidden):
                return False

        return True

    def validate_rank(self, output_rank: Rank) -> bool:
        """Validate output rank respects layer ceiling"""
        return output_rank <= self.max_output_rank

# Define standard layer specs
LAYER_SPECS = {
    "PURE_DAL": LayerSpec(
        name="PURE_DAL",
        domain="LAFZI_DALALI",
        input_type=str,  # raw Arabic text
        output_type=DalCandidate,
        allowed_operations=frozenset({"build", "normalize"}),
        forbidden_outputs=frozenset({"meaning", "dalalah", "wadh", "hukm"}),
        required_evidence_kinds=frozenset({"c1_encoding", "c2a_phonology", "c2b_morphology"}),
        residual_policy="ACCUMULATE",
        rank_policy="CEILING_LICENSED",
        min_input_rank=Rank.UNRESOLVED,
        max_output_rank=Rank.LICENSED,
    ),

    "WADH": LayerSpec(
        name="WADH",
        domain="LAFZI_DALALI",
        input_type=DalCandidate,
        output_type=WadhClaim,
        allowed_operations=frozenset({"admit", "block"}),
        forbidden_outputs=frozenset({"meaning", "dalalah", "hukm", "murad"}),
        required_evidence_kinds=frozenset({"lexicon_report", "transmission"}),
        residual_policy="PRESERVE",
        rank_policy="CEILING_LICENSED",
        min_input_rank=Rank.LICENSED,  # Wadh requires strong Dal
        max_output_rank=Rank.LICENSED,
    ),

    "TASAWWUR": LayerSpec(
        name="TASAWWUR",
        domain="COGNITIVE",
        input_type=BindingCandidate,
        output_type=TasawwurCandidate,  # to be created
        allowed_operations=frozenset({"conceptualize"}),
        forbidden_outputs=frozenset({"hukm", "murad"}),
        required_evidence_kinds=frozenset({"binding_trace", "prior_information"}),
        residual_policy="ACCUMULATE",
        rank_policy="CEILING_LICENSED",
        min_input_rank=Rank.LICENSED,
        max_output_rank=Rank.LICENSED,
    ),
}
```

2. **Update layer implementations** to use LayerSpec:
```python
# Example: src/gfa/methods/lafzi_dal/dal_candidate_builder.py
from gfa.governance.layer_spec import LAYER_SPECS

class DalCandidateBuilder:
    def __init__(self):
        self.layer_spec = LAYER_SPECS["PURE_DAL"]

    def build(self, text: str) -> BuilderResult:
        # Validate input
        if not self.layer_spec.validate_input(text):
            return blocked("invalid_input_type")

        # ... build logic ...

        # Validate output
        if not self.layer_spec.validate_output(candidate):
            return internal_failure("layer_spec_violation")

        # Validate rank
        if not self.layer_spec.validate_rank(candidate.rank):
            return internal_failure(f"rank_exceeds_layer_ceiling: {candidate.rank} > {self.layer_spec.max_output_rank}")

        return success(candidate)
```

3. **Create `tests/gfa/governance/test_layer_spec.py`** (30 tests):
- Test LayerSpec validation for each defined layer
- Test forbidden output detection
- Test rank ceiling enforcement
- Test input/output type checking
- Test required evidence validation

**Exit Criterion**:
- ✅ All 30 LayerSpec tests pass
- ✅ At least 3 layers use LayerSpec (PURE_DAL, WADH, one more)
- ✅ Forbidden outputs blocked at runtime
- ✅ Rank ceilings enforced
- ✅ All existing tests remain green

**Estimated Scope**: 1 new file, 2 modified files, 30 new tests

---

## After Foundation Hardening

Once PR-F1/F2/F3 are complete, safe expansion becomes possible:

### Phase C: Cognitive Layers

**PR-C1: PriorInformationSystem Formal Contract**
- Formalize full PriorInformationSystem (beyond FirstPriorUnit)
- Integrate with prior_filter Opinion blocking
- Add PriorOpinion contamination detection

**PR-C2: General governed_binding Function**
- Extract unified binding contract from NeutralBinding + DalMadlulBinding
- Create generic governed_binding(left, right, prior_info, evidence, layer, scope)
- Unify trace preservation and residual handling

**PR-C3: TasawwurLayer**
- Create TasawwurCandidate dataclass
- Implement binding → tasawwur gate
- Forbid direct jump to hukm
- Add NoLeap tests

**PR-C4: NisbahLayer**
- Create NisbahCandidate (distinct from syntax nisbah)
- Implement relational binding
- Prevent ifadah claims

**PR-C5: IfadahLayer**
- Create IfadahCandidate dataclass
- Implement semantic completion closure
- Enforce all 8 ifadah requirements
- Prevent hukm jump

**PR-C6: HukmLayer**
- Create HukmCandidate dataclass
- Implement judgment boundary
- Require external authority validation
- Add aspirational status disclaimer

### Phase G: Validation

**PR-G1: Golden Dataset**
- Create `tests/golden_dataset/`
- Implement 100 YAML examples
- Add dataset test runner
- Validate all governance claims

**PR-A1: Audit Trace**
- Implement reverse trace (Hukm → Reality)
- Verify no layers skipped
- Ensure residuals preserved
- Add audit validation

---

## Timeline

**Foundation Hardening (Required First)**:
- PR-F1: 3-5 days (residual taxonomy)
- PR-F2: 3-5 days (rank policy)
- PR-F3: 4-6 days (LayerSpec contract)
- **Total**: 10-16 days

**Cognitive Expansion (After Hardening)**:
- PR-C1: 3 days
- PR-C2: 3 days
- PR-C3-C6: 4 days each = 16 days
- **Total**: 22 days

**Validation (Parallel with Expansion)**:
- PR-G1: 5 days
- PR-A1: 4 days
- **Total**: 9 days

**Overall**: 6-8 weeks for complete foundation + cognitive layers + validation

---

## Success Criteria

Foundation hardening is complete when:

1. ✅ PR-F1: Implementation exceptions cannot appear in successful residuals
2. ✅ PR-F2: Rank ceilings enforced automatically, WadhGate blocks weak Dal
3. ✅ PR-F3: LayerSpec validated at runtime for at least 3 layers
4. ✅ All new tests pass (75+ new tests)
5. ✅ All existing tests remain green (497+)
6. ✅ Documentation updated to reflect new governance
7. ✅ No claim inflation in updated docs

---

## Risk Mitigation

**Risk**: Foundation hardening breaks existing code

**Mitigation**:
- PR-F1 only adds validation, doesn't change Result interface
- PR-F2 adds ceilings but preserves current behavior where correct
- PR-F3 validates but doesn't require immediate refactoring
- All PRs maintain backward compatibility

**Risk**: Timeline slips

**Mitigation**:
- Each PR is independently valuable
- Can pause between PRs if needed
- Foundation hardening is **mandatory**, cognitive expansion is **optional**

**Risk**: Over-engineering

**Mitigation**:
- Focus on critical gaps only (taxonomy, ceilings, specs)
- No speculative features
- Test-driven development ensures minimal viable implementation

---

**Next Step**: Begin PR-F1 (Residual Taxonomy) immediately after PR-F0 merges.
