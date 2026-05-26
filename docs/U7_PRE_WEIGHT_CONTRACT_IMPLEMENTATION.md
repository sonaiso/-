# U₇ Pre-Weight Contract Implementation

**Status**: ✅ COMPLETE
**Date**: 2026-05-26
**Layer**: U₇ PreWeightContractCarrier
**Transition**: U₆ (MabniClosedClass) → U₇ (PreWeightContract) → U₈ (RootStem)

---

## Executive Summary

U₇ PreWeightContractCarrier is now **fully implemented** as the contract/permission gate before morphological analysis. This layer determines which units are **permitted** to enter root/stem/weight extraction (U₈/U₉), without performing the extraction itself.

### Critical Achievement

**Path Blocking Law Enforced**:
```
لا جذر قبل عقد ما قبل الوزن
لا وزن قبل عقد ما قبل الوزن
```

**Translation**: No root before pre-weight contract. No weight before pre-weight contract.

---

## Architectural Position

### Layer Sequence (U₀-U₉ Execution Core)

```
U₀ Unicode              ✅ COMPLETE
U₁ Grapheme             ✅ COMPLETE
U₂p PhoneticProjection  ✅ COMPLETE
U₂s ArabicSyllable      ✅ COMPLETE
U₃ BoundaryAttachment   ✅ COMPLETE
U₄ TrueSingularLafẓ     ✅ COMPLETE
U₅ FunctionalRole       ✅ COMPLETE
U₆ MabniClosedClass     ✅ COMPLETE (PR #103 merged)
U₇ PreWeightContract    ✅ COMPLETE (this implementation)
U₈ RootStem             ⏳ Next layer
U₉ Weight               ⏳ Future
```

### What U₇ Is and Is Not

**U₇ IS**:
- Contract gate before morphological analysis
- Path permission determination (possible/blocked/deferred)
- Evidence requirement specification
- Blocker for closed-class mabni units

**U₇ IS NOT**:
- Root extraction (that's U₈)
- Stem extraction (that's U₈)
- Weight determination (that's U₉)
- Pattern certification (that's U₉+)
- Meaning assignment (that's U₁₅)
- Grammatical judgment (that's U₇+)

---

## Core Laws (Axioms)

### Axiom 7.1: لا جذر قبل عقد ما قبل الوزن
**No root before pre-weight contract**

All units must pass through U₇ contract gate before U₈ root extraction.

### Axiom 7.2: لا وزن قبل عقد ما قبل الوزن
**No weight before pre-weight contract**

All units must pass through U₇ contract gate before U₉ weight determination.

### Axiom 7.3: المفتوح ≠ الإذن التلقائي
**Open-class ≠ automatic permission**

Open-class classification (from U₆) does NOT automatically grant morphological permission. U₇ must evaluate and grant contract.

### Axiom 7.4: العقد ≠ الشهادة
**Contract ≠ certificate**

U₇ contract is PERMISSION, not CERTIFICATION. Approval means "may proceed" not "is certified root/weight".

### Axiom 7.5: العقد ≠ الاستخراج
**Contract ≠ extraction**

U₇ contract gate does NOT extract morphological features. It only permits/blocks downstream extraction.

### Axiom 7.6: المغلق المبني يحجب المسار
**Closed-class mabni blocks path**

Closed-class mabni units (particles, pronouns) MUST block root/weight paths.

---

## Type System

### Core Enumerations

#### ContractStatus
```python
CLOSED_CLASS_BLOCKED           # مغلق محجوب
OPEN_CORE_CONTRACT_CANDIDATE   # مرشح عقد نواة مفتوحة
OPEN_CORE_CONTRACT_APPROVED    # عقد نواة مفتوحة موافق
OPEN_CORE_CONTRACT_DEFERRED    # عقد نواة مفتوحة مؤجل
OPEN_CORE_CONTRACT_BLOCKED     # عقد نواة مفتوحة محجوب
PROPER_NAME_DEFERRED           # علم مؤجل
LOANWORD_DEFERRED              # دخيل مؤجل
JAMID_DEFERRED                 # جامد مؤجل
INSUFFICIENT_EVIDENCE          # دليل غير كافٍ
```

#### PathPermission
```python
POSSIBLE           # ممكن - path may be opened with evidence
BLOCKED            # محجوب - path is blocked
DEFERRED           # مؤجل - path needs evidence
UNRESOLVED         # غير محسوم - path status unknown
REQUIRES_EVIDENCE  # يحتاج دليلاً - explicit evidence required
```

### Core Structures

#### PreWeightContractUnit
```python
@dataclass(frozen=True)
class PreWeightContractUnit:
    uid: str
    surface: str
    source_u6_unit_id: str
    source_u6_trace: Tuple[str, ...]

    # Contract classification
    open_closed_status: str
    contract_status: ContractStatus

    # Path permissions (NOT certificates)
    lexical_path_potential: PathPermission
    root_path_permission: PathPermission
    stem_path_permission: PathPermission
    weight_path_permission: PathPermission

    # Surface potentials (hints only)
    jamid_surface_potential: PathPermission
    proper_name_surface_potential: PathPermission
    loanword_surface_potential: PathPermission
    frozen_primitive_potential: PathPermission

    # Derivational readiness
    derivational_readiness: PathPermission

    # Evidence and blocking
    required_evidence: Tuple[str, ...]
    blocked_paths: Tuple[str, ...]
    residuals: FrozenSet[Residual]
    rank: Rank
    trace: Tuple[str, ...]
```

**CRITICAL**: PreWeightContractUnit has comprehensive `__post_init__` validation that **raises ValueError** if any forbidden field exists:
- `root`, `root_certificate`
- `stem`, `stem_certificate`
- `weight`, `weight_certificate`
- `pattern`, `pattern_certificate`
- `meaning`, `dalalah`, `ifadah`
- `hukm`, `final_irab`
- `resolved_reference`

---

## Decision Logic

### Contract Status Classification

```python
def _classify_contract_status(mabni_unit: MabniClosedClassUnit) -> ContractStatus:
    """
    Decision tree:
    1. If closed-class mabni → CLOSED_CLASS_BLOCKED
    2. If open-class core → OPEN_CORE_CONTRACT_CANDIDATE
    3. Otherwise → INSUFFICIENT_EVIDENCE
    """
```

### Path Permission Determination

```python
def _determine_path_permissions(
    contract_status: ContractStatus,
    surface: str
) -> (lexical_path, root_path, stem_path, weight_path):
    """
    CLOSED_CLASS_BLOCKED → all paths BLOCKED
    OPEN_CORE_CONTRACT_CANDIDATE → all paths POSSIBLE
    OPEN_CORE_CONTRACT_APPROVED → all paths POSSIBLE
    *_DEFERRED → all paths DEFERRED
    INSUFFICIENT_EVIDENCE → all paths UNRESOLVED
    """
```

---

## Golden Test Cases (All Passing ✓)

### 1. وَ (Conjunction) → Blocked

**Input**: U₆ closed-class وَ (HARF_ATF)

**Output**:
```python
contract_status = CLOSED_CLASS_BLOCKED
root_path_permission = BLOCKED
weight_path_permission = BLOCKED
stem_path_permission = BLOCKED
blocked_paths = ["root_extraction", "weight_determination", "stem_extraction"]
```

**Test**: `test_golden_case_wa_blocks_root_weight` ✓

---

### 2. بِ (Preposition) → Blocked

**Input**: U₆ closed-class بِ (HARF_JARR)

**Output**:
```python
contract_status = CLOSED_CLASS_BLOCKED
root_path_permission = BLOCKED
weight_path_permission = BLOCKED
blocked_paths = ["root_extraction", "weight_determination"]
```

**Test**: `test_golden_case_bi_blocks_root_weight` ✓

---

### 3. ـهِمْ (Attached Pronoun) → Blocked

**Input**: U₆ closed-class ـهِمْ (PRONOUN_ATTACHED)

**Output**:
```python
contract_status = CLOSED_CLASS_BLOCKED
root_path_permission = BLOCKED
weight_path_permission = BLOCKED
blocked_paths = ["root_extraction", "weight_determination"]
```

**Test**: `test_golden_case_attached_pronoun_blocks_root` ✓

---

### 4. كِتَابِ (Open-class noun) → Contract Candidate

**Input**: U₆ open-class كِتَابِ

**Output**:
```python
contract_status = OPEN_CORE_CONTRACT_CANDIDATE
root_path_permission = POSSIBLE
weight_path_permission = POSSIBLE
stem_path_permission = POSSIBLE
required_evidence = ["lexical_attestation", "surface_family_evidence"]
```

**CRITICAL**: NO `root` field, NO `weight` field, NO `pattern` field

**Test**: `test_golden_case_kitaab_opens_contract` ✓

---

### 5. وَبِكِتَابِهِمْ (Full Composition) → Mixed

**Input**: U₆ layer with 4 units

**Output**:
- وَ → CLOSED_CLASS_BLOCKED
- بِ → CLOSED_CLASS_BLOCKED
- كِتَابِ → OPEN_CORE_CONTRACT_CANDIDATE
- ـهِمْ → CLOSED_CLASS_BLOCKED

**Test**: `test_golden_case_full_composition` ✓

---

## Constitutional Prohibition Tests (All Passing ✓)

### Forbidden Field Enforcement

U₇ **MUST NOT** contain these fields:

```python
forbidden_fields = [
    'root', 'root_certificate',
    'stem', 'stem_certificate',
    'weight', 'weight_certificate',
    'pattern', 'pattern_certificate',
    'meaning', 'dalalah', 'ifadah',
    'hukm', 'final_irab',
    'resolved_reference'
]
```

**Tests**:
- `test_contract_unit_no_root_field` ✓
- `test_contract_unit_no_weight_field` ✓
- `test_contract_unit_no_meaning_field` ✓
- `test_contract_unit_no_hukm_field` ✓

Each test verifies that attempting to add forbidden field raises `ValueError`.

---

## CPB₇ (Completeness Predicate and Proof Builder)

### Completeness Checks

```python
def is_complete(layer_obj: PreWeightContractLayerObject) -> bool:
    """
    Checks:
    1. Units exist
    2. Source mabni layer ID preserved
    3. No forbidden fields in any unit
    """
```

### Proof Structure

```python
proof = CPB7.build_proof(layer_obj)
```

**Evidence**:
- `units_count=N`
- `blocked_count=M` (closed-class units)
- `approved_count=K` (approved contracts)
- `candidate_count=L` (contract candidates)
- `deferred_count=D` (deferred contracts)
- `trace_preserved=True`
- `rank=CANDIDATE`

**Allowed Next Gates**:
- `root_stem_gate` (U₈)

**Forbidden Next Gates**:
- `root_certificate`
- `stem_certificate`
- `weight_certificate`
- `pattern_certificate`
- `meaning_certificate`
- `hukm_certificate`

**Limitations**:
- `no_root_extraction`
- `no_stem_extraction`
- `no_weight_determination`
- `no_pattern_determination`
- `no_meaning_assignment`
- `no_hukm_judgment`
- `contract_is_permission_not_certificate`
- `blocked_units_must_not_proceed_to_root`
- `approved_units_may_proceed_to_root_with_evidence`

**Tests**:
- `test_cpb7_completeness` ✓
- `test_cpb7_proof_structure` ✓
- `test_cpb7_proof_limitations` ✓

---

## Test Results

### All U₇ Tests (21/21 Passing ✓)

```
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.3, pluggy-1.6.0
rootdir: /home/runner/work/-/-
configfile: pytest.ini
collected 21 items

tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_contract_unit_no_root_field PASSED [  4%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_contract_unit_no_weight_field PASSED [  9%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_contract_unit_no_meaning_field PASSED [ 14%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_contract_unit_no_hukm_field PASSED [ 19%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_golden_case_wa_blocks_root_weight PASSED [ 23%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_golden_case_bi_blocks_root_weight PASSED [ 28%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_golden_case_attached_pronoun_blocks_root PASSED [ 33%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_golden_case_kitaab_opens_contract PASSED [ 38%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_golden_case_full_composition PASSED [ 42%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_open_class_no_root_emission PASSED [ 47%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_open_class_no_weight_emission PASSED [ 52%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_trace_preservation PASSED [ 57%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_evidence_propagation PASSED [ 61%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_cpb7_completeness PASSED [ 66%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_cpb7_proof_structure PASSED [ 71%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_cpb7_proof_limitations PASSED [ 76%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_empty_input_handling PASSED [ 80%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_execution_without_errors PASSED [ 85%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_closed_class_all_paths_blocked PASSED [ 90%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_open_class_all_paths_possible PASSED [ 95%]
tests/dal_core/test_u7_pre_weight_contract_carrier.py::test_contract_candidate_requires_evidence PASSED [100%]

============================== 21 passed in 0.31s
```

### No Regressions in U₆ (20/20 Passing ✓)

```
============================== 20 passed in 0.21s
```

---

## Files Created

### Implementation
- `/home/runner/work/-/-/src/dal_core/u7_pre_weight_contract_carrier.py` (733 lines)

### Tests
- `/home/runner/work/-/-/tests/dal_core/test_u7_pre_weight_contract_carrier.py` (627 lines)

### Documentation
- `/home/runner/work/-/-/docs/U7_PRE_WEIGHT_CONTRACT_IMPLEMENTATION.md` (this file)

---

## Next Steps

### Immediate: U₈ RootStem Implementation

U₇ now provides the contract gate. The next layer must implement:

**U₈ RootStem Carrier**:
- Consumes U₇ PreWeightContractLayerObject
- Processes ONLY units with `root_path_permission = POSSIBLE`
- Blocks units with `root_path_permission = BLOCKED`
- Defers units with `root_path_permission = DEFERRED`
- Extracts root candidates (NOT certificates)
- Outputs root/stem potential paths for U₉

**Critical Law for U₈**:
```
U₇.BLOCKED → U₈ must skip (no root extraction)
U₇.POSSIBLE → U₈ may extract (root candidates)
U₇.DEFERRED → U₈ may defer or extract with evidence
```

### Future: U₉ Weight Implementation

After U₈, implement:

**U₉ Weight Carrier**:
- Consumes U₈ RootStemLayerObject
- Processes ONLY units with `weight_path_permission = POSSIBLE`
- Determines pattern/weight candidates (NOT certificates)
- Outputs weight potential paths for higher layers

---

## Architectural Significance

### Pre-Morphological Governance Core Complete

With U₇ implementation, the project has completed the **Pre-Morphological Governance Core** (U₀-U₇):

```
U₀ Unicode              → Character encoding
U₁ Grapheme             → Visual units
U₂p PhoneticProjection  → Sound representation
U₂s ArabicSyllable      → Syllable structure
U₃ BoundaryAttachment   → Word boundaries
U₄ TrueSingularLafẓ     → True singular units
U₅ FunctionalRole       → Functional classification
U₆ MabniClosedClass     → Closed/open separation
U₇ PreWeightContract    → Morphological permission gate
```

### Path Blocking Enforced

The system now **enforces architectural path blocking**:

```
لا قفز إلى الجذر بلا عقد
لا قفز إلى الوزن بلا عقد
```

**Translation**: No jump to root without contract. No jump to weight without contract.

---

## Conclusion

**U₇ PreWeightContract is COMPLETE and TESTED**.

The layer successfully implements:
1. ✅ Contract/permission gate before morphological analysis
2. ✅ Path blocking for closed-class mabni units
3. ✅ Path opening for open-class core units (without extraction)
4. ✅ Constitutional prohibition enforcement (no root/weight/meaning/hukm)
5. ✅ Trace preservation from U₆
6. ✅ Evidence requirement specification
7. ✅ CPB₇ proof generation
8. ✅ 21/21 golden tests passing
9. ✅ 20/20 U₆ regression tests passing

**The project is now ready for U₈ RootStem implementation.**

---

**Document Version**: 1.0
**Implementation Date**: 2026-05-26
**Commit**: bb4ff13
