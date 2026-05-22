# Nabhani Methods - PR-N0: RationalMethod Kernel

## Summary

Implements **الطريقة العقلية** (RationalMethod) as the governing root of all thinking methods, following Nabhani's epistemological framework.

## Implementation Status

✅ **PR-N0: RationalMethod Kernel** (COMPLETE - 17/17 tests passing)
- ✅ Four-pillar requirement (Reality, Sensory, Carrier, PriorInformation)
- ✅ Prior opinion exclusion (PriorInformation ≠ PriorOpinion)
- ✅ Dual rank system (ExistenceRank vs PredicateRank)
- ✅ Governed failures (no bare exceptions)
- ✅ Boundary enforcement (does NOT implement future branches)

❌ **Future PRs** (NOT IMPLEMENTED):
- ❌ PR-N1: NeutralBinding
- ❌ PR-N2: DomainSpec + StyleSpec
- ❌ PR-N3: ScientificMethod (experimental branch)
- ❌ PR-N4: LogicalStyle (formal grounded style)
- ❌ PR-N5: MeansAlgebra (non-certifying tools)
- ❌ PR-N6: UniversalRules
- ❌ PR-N7: Registry integration

## Core Principles

### Nabhani Definition of Aql (العقل)

```
العقل = نقل الحس بالواقع إلى الدماغ + معلومات سابقة
Aql = Sensory transfer of reality to brain + Prior information
```

### Four Pillars (الأركان الأربعة)

No rational operation without:
1. **Reality** (الواقع)
2. **Sensory Transfer** (نقل الحس)
3. **Cognitive Carrier** (الدماغ الصالح)
4. **Prior Information** (المعلومات السابقة)

### Critical Laws

1. **Prior opinion exclusion**: `PriorInformation ≠ PriorOpinion`
2. **Dual rank system**: `ExistenceRank ≠ PredicateRank`
3. **Governed failures**: No bare exceptions, only `AqlOperationResult`
4. **Existence ≠ Predicate**: Seeing a thing ≠ Knowing its reality (رأيت شيئاً ≠ عرفت حقيقته)

## Architecture

```
src/gfa/methods/
├── __init__.py
└── rational/
    ├── __init__.py
    ├── prior_filter.py         # PriorInformation vs PriorOpinion
    ├── residual_taxonomy.py    # Rational residual categories
    ├── judgment.py             # AqlJudgment with dual ranks
    ├── aql_operation.py        # Four-pillar operation
    └── rational_method.py      # Root governing method
```

## Usage

```python
from gfa.methods.rational import RationalMethod, PriorInformation

# Create prior information (not opinion)
prior = frozenset([
    PriorInformation(
        content="validated fact",
        domain="domain_name",
        rank="LICENSED",
        evidence_trace="evidence_id"
    )
])

# Execute rational judgment
result = RationalMethod.judge(
    reality="observed_reality",
    sensory_transfer="sensory_data",
    cognitive_carrier="carrier_id",
    prior_knowledge=prior
)

# Check result
if result.is_success():
    judgment = result.judgment
    print(f"Existence: {judgment.existence_rank}")
    print(f"Predicate: {judgment.predicate_rank}")
    print(f"Residuals: {judgment.residuals}")
else:
    failure = result.failure
    print(f"Failed: {failure.reason}")
    print(f"Missing: {failure.missing_pillars}")
```

## Tests

All 17 tests passing:

```bash
python -m pytest tests/gfa/methods/test_rational_method_kernel.py -v
```

### Test Coverage

- ✅ Prior opinion exclusion (4 tests)
- ✅ Four-pillar validation (5 tests)
- ✅ Governed results (3 tests)
- ✅ Dual rank system (1 test)
- ✅ Method boundaries (4 tests)

## Key Design Decisions

### 1. No Bare Exceptions

Failures return `AqlOperationResult` with:
- `success: False`
- `failure: AqlJudgmentFailure` (with reason, missing pillars, residuals)
- `residuals: Tuple[RationalResidual, ...]`

### 2. Prior Filter

`filter_prior()` separates:
- **PriorInformation**: Valid, licensed/certified, evidence-backed
- **PriorOpinion**: Bias, assumption, predetermined conclusion (excluded)

### 3. Dual Rank System

- **ExistenceRank**: QATI (certain) or ZANNI (probable)
- **PredicateRank**: CERTIFIED → LICENSED → ZANNI → CANDIDATE → BLOCKED

**Critical Law**: `ExistenceRank.QATI ≠> PredicateRank.CERTIFIED`

### 4. Boundary Enforcement

`RationalMethod` explicitly does NOT implement:
- `ScientificMethod` (future PR-N3)
- `LogicalStyle` (future PR-N4)
- `MeansAlgebra` (future PR-N5)

Verified by tests:
```python
assert RationalMethod.does_not_implement_scientific_method()
assert RationalMethod.does_not_implement_logical_style()
assert RationalMethod.does_not_implement_means_algebra()
```

## Nabhani Method Hierarchy

```
RationalMethod (الطريقة العقلية) ← ROOT (implemented)
├─ ScientificMethod (الطريقة العلمية) ← experimental branch (NOT implemented)
├─ LogicalStyle (الطريقة المنطقية) ← formal grounded style (NOT implemented)
├─ StyleAlgebra (أساليب التفكير) ← domain specializations (NOT implemented)
└─ MeansAlgebra (وسائل التفكير) ← non-certifying tools (NOT implemented)
```

## Next Steps

After PR-N0 approval, implement in sequence:

1. **PR-N1**: NeutralBinding for AqlOperation
2. **PR-N2**: DomainSpec + StyleSpec
3. **PR-N3**: ScientificMethod as restricted style
4. **PR-N4**: LogicalStyle as grounded formal style
5. **PR-N5**: MeansAlgebra for non-certifying instruments
6. **PR-N6**: UniversalRules governance
7. **PR-N7**: Registry integration with dal_core, fvafk, syntax_theory

## Acceptance Criteria

PR-N0 meets all criteria:

- ✅ Implements only rational method (no scientific/logical/means)
- ✅ Does not import from linguistic layers
- ✅ Does not issue CERTIFIED by default
- ✅ Does not convert opinion to information
- ✅ All failures return governed objects
- ✅ All tests passing (17/17)

## License

Part of the Eqratech Arabic Diana Project.
