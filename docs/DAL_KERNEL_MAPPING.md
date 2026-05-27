# Dal Algebra Kernel Mapping

**Created**: 2026-05-27 (PR-1B)
**Status**: CANONICAL MAPPING (Approved)

## Overview

This document defines the **canonical mapping** between three foundational registries:
- `DalTransitionDomain` (dal_algebra.py) - 8-layer transition architecture
- `ExecutionLayer` (execution_layer_registry.py) - U₀-U₁₅ runtime order
- `DomainType` (domain_registry.py) - Competency boundaries

## Kernel Role Division

| Component | Role | Authority |
|-----------|------|-----------|
| **dal_algebra.py** | Contract Algebra | Constitution (الدستور) |
| **AlgebraicDecisionCore** | Decision/Audit Executor | Governance (الحكم) |
| **ApprovedTransitionContext** | Permission Token | Evidence (الدليل) |
| **ExecutionLayer** | Runtime Order | Implementation (التنفيذ) |
| **DomainType** | Competency Boundary | Reference (المرجع) |
| **IdentityType** | Identity Vocabulary | Reference (المرجع) |

## Canonical Mapping

### Map 1: DalTransitionDomain → ExecutionLayer

| DalTransitionDomain | ExecutionLayer(s) | Description |
|---------------------|-------------------|-------------|
| `GRAPHOPHONEMIC` | U₀, U₁ | Carrier → Atom (رسم/صوت) |
| `SYLLABIC` | U₂s | Syllable structure (مقطع) |
| `PRE_MORPH` | U₃, U₄ | Pre-morphological classification |
| `ORIGIN` | U₈ | Root/frozen/functional (أصل) |
| `TEMPLATE` | U₉ | Pattern/weight matching (وزن) |
| `IDENTITY_AXIS` | U₅, U₆ | Ism/Fi'l/Harf classification (محور الهوية) |
| `DIRECTIONAL_ANALYSIS` | U₇-A, U₇-B | Bidirectional form analysis (تحليل اتجاهي) |
| `JUDGMENT` | U₇-C, U₁₀ | Morphological judgment (حكم صرفي) |

**Key Principles**:
1. **One-to-Many**: One DalTransitionDomain may map to multiple ExecutionLayers
2. **Non-Overlapping**: Each ExecutionLayer belongs to exactly one DalTransitionDomain
3. **Sequential Preservation**: ExecutionLayer order (U₀→U₁₅) preserved within each domain

### Map 2: DalTransitionDomain → DomainType

⚠️ **STATUS**: PARTIAL MAPPING (Code-accurate as of 2026-05-27)

| DalTransitionDomain | DomainType(s) | Description | Status |
|---------------------|---------------|-------------|--------|
| `GRAPHOPHONEMIC` | `SCRIPT_DOMAIN`, `SOUND_DOMAIN` | Script and sound (U₀-U₁) | ✅ Verified |
| `SYLLABIC` | `SYLLABLE_DOMAIN` | Syllabic structure (U₂) | ✅ Verified |
| `PRE_MORPH` | `BOUNDARY_DOMAIN`, `LAFZ_DOMAIN` | Boundary and lexical unit (U₃-U₄) | ⚠️ Tentative |
| `ORIGIN` | `ROOT_STEM_DOMAIN` | Root and stem material (U₈) | ✅ Verified |
| `TEMPLATE` | `WEIGHT_DOMAIN` | Weight determination (U₉) | ✅ Verified |
| `IDENTITY_AXIS` | **UNMAPPED** | Identity axis classification | ❌ Missing |
| `DIRECTIONAL_ANALYSIS` | `MARKER_PROTECTION_DOMAIN`, `CLAUSE_AGREEMENT_DOMAIN` | Surface protection (U₇-A, U₇-B, U₇-C) | ⚠️ Tentative |
| `JUDGMENT` | `JUDGMENT_DOMAIN` | Final judgment (NOT U₁₀ WordForm) | ⚠️ See note below |

**Critical Notes**:
1. **IDENTITY_AXIS → No matching DomainType**: `IDENTITY_DOMAIN` does NOT exist in domain_registry.py. This is a GAP.
2. **JUDGMENT ≠ U₁₀ WordForm**: U₁₀ WordFormCandidate is NOT final judgment. It's a word contract/form holder.
3. **Derivational forms**: `SOURCE_FORM_DOMAIN`, `ATTRIBUTE_FORM_DOMAIN`, `FUNCTIONAL_FORM_DOMAIN` exist but have no DalTransitionDomain mapping yet.
4. **Syntax/Semantics domains**: `AMIL_RELATION_DOMAIN`, `I3RAB_SURFACE_DOMAIN`, `SYNTAX_DOMAIN`, `SEMANTICS_DOMAIN`, `PRAGMATICS_DOMAIN` exist for future U₁₁-U₁₅ layers.

**Non-Existent DomainTypes** (Previously hallucinated in this document):
- ❌ `PHONEME_DOMAIN` - does NOT exist (use `SOUND_DOMAIN`)
- ❌ `PRE_MORPHOLOGICAL_DOMAIN` - does NOT exist (use `BOUNDARY_DOMAIN` or `LAFZ_DOMAIN`)
- ❌ `ROOT_DOMAIN` - does NOT exist (use `ROOT_STEM_DOMAIN`)
- ❌ `PATTERN_DOMAIN` - does NOT exist
- ❌ `IDENTITY_DOMAIN` - does NOT exist (GAP - needs to be added)
- ❌ `FORM_DOMAIN` - does NOT exist
- ❌ `WORDFORM_DOMAIN` - does NOT exist (GAP - needs to be added)

### Map 3: D_mufrad Pipeline → Dal Architecture

⚠️ **STATUS**: TENTATIVE MAPPING (Requires validation)

**Decision**: Option B - Map to existing DalTransitionDomain (APPROVED with caveats)

| D_mufrad Stage | File | DalTransitionDomain | ExecutionLayer | DomainType | Status |
|----------------|------|---------------------|----------------|------------|--------|
| atoms → DForm | `d_form.py` | `PRE_MORPH` | U₃, U₄ | `BOUNDARY_DOMAIN`, `LAFZ_DOMAIN` | ⚠️ Tentative |
| DForm → DLugha | `d_lugha.py` | `ORIGIN` | U₈ | `ROOT_STEM_DOMAIN` | ✅ Likely correct |
| DLugha → DType | `d_type.py` | `IDENTITY_AXIS` | U₅, U₆ | **UNMAPPED** (missing IDENTITY_DOMAIN) | ❌ GAP |
| DType → DMufrad | `d_mufrad.py` | **UNMAPPED** | U₁₀ | **UNMAPPED** (missing WORDFORM_DOMAIN) | ❌ GAP |

**Critical Issues**:
1. **DMufrad ≠ JUDGMENT**: DMufrad is NOT final judgment (no Ifādah, no Hukm). It's a closed lexical form/word contract.
2. **Missing WORDFORM_DOMAIN**: U₁₀ WordFormCandidate needs its own domain, which doesn't exist yet.
3. **Missing IDENTITY_DOMAIN**: DType (Ism/Fi'l/Harf classification) has no corresponding DomainType.

**Proposed Corrections** (Requires separate PR):
- Add `IDENTITY_DOMAIN` to DomainType enum for DType (U₅, U₆)
- Add `WORDFORM_DOMAIN` to DomainType enum for DMufrad/U₁₀
- Map DMufrad to new domain: `WORDFORM_DOMAIN` or `LEXICAL_FORM_DOMAIN`
- **NOT** to `JUDGMENT_DOMAIN` (that's for U₁₅ Hukm after Ifādah)

**Rejected Options**:
- **Option A** (Extend DalTransitionDomain): Would create parallel D_mufrad-specific domains
- **Option C** (Keep separate): Would break kernel integration

**Current Reality**: D_mufrad pipeline exists and works, but dal_algebra mapping is incomplete due to missing DomainType entries.

## PR-1B Status: Incomplete - Metadata Only

⚠️ **CRITICAL**: PR-1B added dal_* fields but **WITHOUT validators**.

### What PR-1B Added

1. **DecisionAudit** extended with 3 optional fields:
   ```python
   dal_contract: Optional[DalTransitionContract] = None
   dal_domain: Optional[DalTransitionDomain] = None
   dal_claim_scope: Optional[DalClaimScope] = None
   ```

2. **ApprovedTransitionContext** extended with same 3 fields

3. **DAL_KERNEL_MAPPING.md** created (this document)

### What PR-1B Did NOT Add (GAPS)

1. ❌ **No validators** for dal_* fields consistency
2. ❌ **No tests** for kernel integration
3. ❌ **No enforcement** that dal_domain matches ExecutionLayer
4. ❌ **No enforcement** that dal_domain matches DomainType
5. ❌ **No enforcement** that dal_claim_scope matches dal_domain
6. ❌ **No enforcement** that dal_contract is preserved correctly

### Current Status: Transitional Metadata

The dal_* fields are currently **transitional metadata**, NOT enforced governance.

They can be:
- Set to any value without validation
- Inconsistent with from_layer/to_layer
- Inconsistent with domain
- Passed through without checks

This means PR-1B is **NOT "kernel integration complete"** - it's a **foundation for future integration**.

### Required Next Steps (Before PR-1C)

**TODO: Add validate_dal_kernel_mapping()**

```python
def validate_dal_kernel_mapping(audit: DecisionAudit) -> List[str]:
    """
    Validate that dal_* fields are consistent with ExecutionLayer and DomainType.

    Returns list of validation errors (empty if valid).

    Checks:
    1. dal_domain ↔ from_layer/to_layer consistency
    2. dal_domain ↔ domain consistency
    3. dal_claim_scope ↔ dal_domain consistency
    4. dal_contract (if present) ↔ dal_domain/dal_claim_scope consistency
    """
    errors = []

    if audit.dal_domain is None:
        return errors  # Optional field, no validation if absent

    # Check 1: dal_domain ↔ ExecutionLayer mapping
    expected_layers = DAL_DOMAIN_TO_EXECUTION_LAYER_MAP.get(audit.dal_domain, set())
    if audit.from_layer not in expected_layers and audit.to_layer not in expected_layers:
        errors.append(
            f"dal_domain {audit.dal_domain} inconsistent with "
            f"{audit.from_layer}→{audit.to_layer}"
        )

    # Check 2: dal_domain ↔ DomainType mapping
    expected_domains = DAL_DOMAIN_TO_DOMAIN_TYPE_MAP.get(audit.dal_domain, set())
    if audit.domain not in expected_domains:
        errors.append(
            f"dal_domain {audit.dal_domain} inconsistent with "
            f"DomainType {audit.domain}"
        )

    # Check 3: dal_claim_scope ↔ dal_domain consistency
    if audit.dal_claim_scope is not None:
        expected_scopes = DAL_DOMAIN_TO_CLAIM_SCOPE_MAP.get(audit.dal_domain, set())
        if audit.dal_claim_scope not in expected_scopes:
            errors.append(
                f"dal_claim_scope {audit.dal_claim_scope} inconsistent with "
                f"dal_domain {audit.dal_domain}"
            )

    # Check 4: dal_contract consistency
    if audit.dal_contract is not None:
        if audit.dal_contract.source_domain != audit.dal_domain:
            errors.append(
                f"dal_contract.source_domain {audit.dal_contract.source_domain} "
                f"!= dal_domain {audit.dal_domain}"
            )
        if audit.dal_contract.claim_scope != audit.dal_claim_scope:
            errors.append(
                f"dal_contract.claim_scope {audit.dal_contract.claim_scope} "
                f"!= dal_claim_scope {audit.dal_claim_scope}"
            )

    return errors
```

**Status**: ❌ NOT IMPLEMENTED (must be added before PR-1C)

**Tests Required**: ❌ NOT IMPLEMENTED

### Validation Rules

### Rule 1: Domain Consistency
If `DecisionAudit.dal_domain` is set, it MUST be consistent with `from_layer` and `to_layer`.

**Example**:
- `dal_domain=SYLLABIC` → `from_layer` and `to_layer` must be within U₂s range

⚠️ **Current Status**: Rule documented but NOT enforced in code

### Rule 2: Claim Scope Consistency
If `DecisionAudit.dal_claim_scope` is set, it MUST be consistent with `dal_domain`.

**Example**:
- `dal_domain=SYLLABIC` → `dal_claim_scope` can only be `SYLLABLE_STRUCTURE_VALID`

⚠️ **Current Status**: Rule documented but NOT enforced in code

### Rule 3: Contract Consistency
If `DecisionAudit.dal_contract` is set:
- `dal_contract.source_domain` must match source `dal_domain`
- `dal_contract.target_domain` must match target `dal_domain`
- `dal_contract.claim_scope` must match `dal_claim_scope`

⚠️ **Current Status**: Rule documented but NOT enforced in code

## Integration Example

⚠️ **WARNING**: This example shows intended usage, but validators don't exist yet.

```python
from dal_core.dal_algebra import DalTransitionDomain, DalTransitionContract
from dal_core.algebraic_decision_core import AlgebraicDecisionCore, DecisionAudit
from dal_core.approved_transition_context import create_approved_context

# Example: U₈→U₉ transition with dal_algebra contract
core = AlgebraicDecisionCore()

# Create audit with dal_algebra integration
audit = DecisionAudit(
    decision_id="decision-001",
    transition_id="u8_to_u9",
    from_layer=ExecutionLayer.ROOT_STEM_CANDIDATE,
    to_layer=ExecutionLayer.WEIGHT_CANDIDATE,
    input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
    output_identity=IdentityType.WEIGHT_IDENTITY,
    domain=DomainType.WEIGHT_DOMAIN,
    function="weight_determination",
    gate="weight_gate",
    evidence=("root_evidence", "pattern_evidence"),
    rank=Rank.CANDIDATE,
    residuals=(),
    trace=("u8", "u9"),
    cpb_status=CPBStatus.APPROVED,
    allowed=True,
    # PR-1B: Kernel integration fields
    dal_domain=DalTransitionDomain.TEMPLATE,
    dal_claim_scope=DalClaimScope.TEMPLATE_MATCHED,
)

# Create approved context (includes dal_contract)
if audit.is_approved():
    context = create_approved_context(audit, existing_identities=frozenset())
    # context.dal_domain == DalTransitionDomain.TEMPLATE
    # context.dal_claim_scope == DalClaimScope.TEMPLATE_MATCHED
```

## Validation Rules

### Rule 1: Domain Consistency
If `DecisionAudit.dal_domain` is set, it MUST be consistent with `from_layer` and `to_layer`.

**Example**:
- `dal_domain=SYLLABIC` → `from_layer` and `to_layer` must be within U₂s range

### Rule 2: Claim Scope Consistency
If `DecisionAudit.dal_claim_scope` is set, it MUST be consistent with `dal_domain`.

**Example**:
- `dal_domain=SYLLABIC` → `dal_claim_scope` can only be `SYLLABLE_STRUCTURE_VALID`

### Rule 3: Contract Consistency
If `DecisionAudit.dal_contract` is set:
- `dal_contract.source_domain` must match source `dal_domain`
- `dal_contract.target_domain` must match target `dal_domain`
- `dal_contract.claim_scope` must match `dal_claim_scope`

## Forbidden Transitions

### Direct Jumps (Constitutional Violation)
- ❌ U₀ → U₈ (GRAPHOPHONEMIC → ORIGIN) - Skips syllabic and pre-morph layers
- ❌ U₉ → U₁₁ (TEMPLATE → COMPOSITION) - Skips U₁₀ WordForm layer
- ❌ Any transition that skips a DalTransitionDomain

### Backward Jumps (Reversibility Violation)
- ❌ U₉ → U₇ (TEMPLATE → DIRECTIONAL_ANALYSIS) - Backward jump forbidden
- ⚠️ Exception: Repair/correction mechanisms (requires explicit evidence)

## Compositional Extensions

### Future Layers (U₁₁-U₁₅)

| DalTransitionDomain | ExecutionLayer | Purpose |
|---------------------|----------------|---------|
| **PRE_COMPOSITION** (proposed) | U₁₁ | Pre-lexical word classification |
| **COMPOSITION** (proposed) | U₁₂ | Relation establishment |
| **SEMANTICS** (proposed) | U₁₃ | Lexical meaning |
| **IFADAH** (proposed) | U₁₄ | Compositional benefit |
| **HUKM** (proposed) | U₁₅ | Epistemic judgment |

**Status**: PROPOSED (not yet implemented)

## References

1. **dal_algebra.py**: Lines 34-47 (DalTransitionDomain enum)
2. **dal_algebra.py**: Lines 50-67 (DalClaimScope enum)
3. **execution_layer_registry.py**: Lines 17-42 (ExecutionLayer enum)
4. **domain_registry.py**: Lines 9-33 (DomainType enum)
5. **UNIFIED_ALGEBRA_PLAN.md**: Lines 609-660 (Temporary kernel role division)

## Version History

- **2026-05-27 (Initial)**: Created canonical mapping (PR-1B) - **INCOMPLETE**
  - Map 1: DalTransitionDomain → ExecutionLayer ✅
  - Map 2: DalTransitionDomain → DomainType ⚠️ (hallucinated names corrected)
  - Map 3: D_mufrad Pipeline → Dal Architecture ⚠️ (gaps identified)
  - Added dal_* fields to DecisionAudit/ApprovedTransitionContext ✅
  - **Missing**: validators, tests, enforcement

- **2026-05-27 (Correction)**: Fixed hallucinated DomainType names
  - Removed: PHONEME_DOMAIN, PRE_MORPHOLOGICAL_DOMAIN, ROOT_DOMAIN, PATTERN_DOMAIN, IDENTITY_DOMAIN, FORM_DOMAIN, WORDFORM_DOMAIN
  - Replaced with actual DomainType values from domain_registry.py
  - Identified 2 critical gaps: IDENTITY_DOMAIN, WORDFORM_DOMAIN need to be added
  - Clarified: U₁₀ WordForm ≠ JUDGMENT (no Ifādah, no Hukm)
  - Added: "PR-1B Status: Incomplete - Metadata Only" section
  - Added: validate_dal_kernel_mapping() TODO

---

## PR-1C Decision: Hybrid Failure Semantics (Option C)

⚠️ **BLOCKING PR-1C**: Cannot proceed until PR-1B mapping corrected.

### The Contradiction (dal_algebra.py)

- **Module docstring (line 19)**: "Transitions return CandidateSet[𝔾] or Failure"
- **Protocol (line 310-315)**: "Returns CandidateSet or raises exception for Failure"

### Resolution: Option C - Hybrid Failure Semantics

**Mathematically Correct Approach**:

```
Construction invariant violation → Exception (ValueError, TypeError)
Algebraic operation failure → AlgebraicFailure value
```

### Rule 1: Exceptions for Invalid Construction

**When to raise exceptions**:
- Object built with impossible invariants
- Required field missing
- Invalid enum value
- Attempt to forge ApprovedTransitionContext (sentinel token violation)
- Invalid dataclass field type

**Examples**:
```python
@dataclass(frozen=True)
class DalTransitionContract:
    def __post_init__(self):
        if self.source_domain == self.target_domain:
            raise ValueError("Source and target domain must differ")
        # ✅ Correct: construction invariant violation
```

### Rule 2: AlgebraicFailure for Operation Non-Satisfaction

**When to return AlgebraicFailure**:
- Gate not satisfied
- Evidence insufficient
- Rank inadequate
- Blocking residuals present
- Rootability check failed
- Weightability check failed
- Slot composition failed
- Isnad relation failed (no bearability)

**Examples**:
```python
def apply_isnad_operation(entity, transformation) -> Success[IsnadRelation] | AlgebraicFailure:
    if not entity.can_bear(transformation):
        return AlgebraicFailure(
            reason="Entity cannot bear transformation",
            gate="bearability_gate",
            evidence_gap="ontic_type_mismatch"
        )
    # ✅ Correct: algebraic operation non-satisfaction
```

### Mathematical Formulation

```
Opₑ : A → Success[B] ∪ AlgebraicFailure
```

Where:
- `A` is valid input (construction already validated)
- `Success[B]` is successful operation result
- `AlgebraicFailure` is failed operation with traceable reason

### Constructor vs Operation

| Context | Invalid State | Response |
|---------|---------------|----------|
| **Construction** (`__init__`, `__post_init__`) | Invariant violation | `raise ValueError/TypeError` |
| **Algebraic Operation** (`apply`, `transform`, `compose`) | Non-satisfaction | `return AlgebraicFailure` |

### Impact on dal_algebra.py (PR-1C)

1. **DalTransitionProtocol.apply()**: Return `CandidateSet[𝔾] | AlgebraicFailure`
2. **Contract constructors**: Raise exceptions for invalid contracts
3. **Evidence validation**: Return AlgebraicFailure for insufficient evidence
4. **Module docstring**: Update to reflect hybrid semantics

### Why Not Option A or B Alone?

- **Option A (Value-based only)**: Cannot handle invalid construction (e.g., negative probability, self-loop transition)
- **Option B (Exception-based only)**: Breaks algebraic closure, makes composition difficult
- **Option C (Hybrid)**: Preserves both construction safety AND algebraic composability

---

## Next Required Steps (Ordered)

1. ✅ **PR-1A**: Complete (100%)
2. ⚠️ **PR-1B**: Incomplete - Fix mapping, add validators
   - [ ] Fix DAL_KERNEL_MAPPING.md (hallucinated DomainType names) ✅ DONE
   - [ ] Add validate_dal_kernel_mapping() function
   - [ ] Add tests for dal_* field validation
   - [ ] Consider adding IDENTITY_DOMAIN and WORDFORM_DOMAIN to DomainType (separate PR)
3. 🚫 **PR-1C**: BLOCKED until PR-1B complete
   - Implement Option C (hybrid failure semantics)
   - Update dal_algebra.py docstring
   - Update DalTransitionProtocol.apply() signature
   - Add AlgebraicFailure dataclass
4. 🚫 **PR-2**: BLOCKED until PR-1B + PR-1C complete

---

**Last Updated**: 2026-05-27 (Corrected after user feedback)
**Status**: PR-1B incomplete, PR-1C blocked
**Critical Issue**: Hallucinated DomainType names corrected, but validators still missing
