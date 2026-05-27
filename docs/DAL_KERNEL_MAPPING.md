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
| `WORDFORM` | U₁₀ | Word form candidate (صورة الكلمة) |
| `JUDGMENT` | U₇-C | Morphological judgment (حكم صرفي) |

**Key Principles**:
1. **One-to-Many**: One DalTransitionDomain may map to multiple ExecutionLayers
2. **Non-Overlapping**: Each ExecutionLayer belongs to exactly one DalTransitionDomain
3. **Sequential Preservation**: ExecutionLayer order (U₀→U₁₅) preserved within each domain

**Critical Correction (PR-126)**:
- ✅ **U₁₀ separated from JUDGMENT**: U10_WORD_FORM now maps to WORDFORM domain, NOT JUDGMENT
- ✅ **Constitutional law enforced**: WordForm is not Judgment (لا صورة الكلمة حكمًا)

### Map 2: DalTransitionDomain → DomainType

✅ **STATUS**: COMPLETE MAPPING (Updated 2026-05-27, PR-126)

| DalTransitionDomain | DomainType(s) | Description | Status |
|---------------------|---------------|-------------|--------|
| `GRAPHOPHONEMIC` | `SCRIPT_DOMAIN`, `SOUND_DOMAIN` | Script and sound (U₀-U₁) | ✅ Verified |
| `SYLLABIC` | `SYLLABLE_DOMAIN` | Syllabic structure (U₂) | ✅ Verified |
| `PRE_MORPH` | `BOUNDARY_DOMAIN`, `LAFZ_DOMAIN` | Boundary and lexical unit (U₃-U₄) | ⚠️ Tentative |
| `ORIGIN` | `ROOT_STEM_DOMAIN` | Root and stem material (U₈) | ✅ Verified |
| `TEMPLATE` | `WEIGHT_DOMAIN` | Weight determination (U₉) | ✅ Verified |
| `IDENTITY_AXIS` | `IDENTITY_DOMAIN` | Identity axis classification (Ism/Fi'l/Harf) - **Path-aware** (PR-127) | ✅ ADDED (PR-125), ✅ PATH-AWARE (PR-127) |
| `DIRECTIONAL_ANALYSIS` | `MARKER_PROTECTION_DOMAIN`, `CLAUSE_AGREEMENT_DOMAIN` | Surface protection (U₇-A, U₇-B, U₇-C) | ⚠️ Tentative |
| `WORDFORM` | `WORDFORM_DOMAIN` | Word form candidate (U₁₀) | ✅ ADDED (PR-126) |
| `JUDGMENT` | `JUDGMENT_DOMAIN` | Final judgment (U₇-C ONLY) | ✅ CORRECTED (PR-126) |

**Critical Notes**:
1. ✅ **IDENTITY_AXIS → IDENTITY_DOMAIN**: Added in PR-125. Maps to محور الهوية (Ism/Fi'l/Harf classification).
2. ✅ **Path-aware IDENTITY_DOMAIN** (PR-127): IDENTITY_DOMAIN does NOT unconditionally require WEIGHT_DOMAIN. Arabic identity can arise through multiple paths:
   - **Weight path**: WEIGHT_DOMAIN → IDENTITY_DOMAIN (derived forms: فاعل، مفعول...)
   - **Mabni/closed-class path**: LAFZ_DOMAIN → IDENTITY_DOMAIN (closed-class: ما، هل، إن...)
   - **Tool/particle path**: LAFZ_DOMAIN → IDENTITY_DOMAIN (particles: في، على، من...)
   - **Pronoun path**: LAFZ_DOMAIN → IDENTITY_DOMAIN (pronouns: هو، أنت...)
   - **Jāmid/frozen path**: LAFZ_DOMAIN → IDENTITY_DOMAIN (frozen nouns, non-weighted)
   - **Constitutional law enforced**: لا هوية من الوزن وحده (No Identity from weight alone for all paths)
3. ✅ **WORDFORM → WORDFORM_DOMAIN**: Added in PR-126. Maps to صورة الكلمة المرشحة (Word form candidate).
4. ✅ **JUDGMENT ≠ U₁₀ WordForm**: Confirmed and enforced (PR-126). U₁₀ WordFormCandidate is NOT final judgment. It's a word contract/form holder.
5. **Derivational forms**: `SOURCE_FORM_DOMAIN`, `ATTRIBUTE_FORM_DOMAIN`, `FUNCTIONAL_FORM_DOMAIN` exist for future architecture.
6. **Syntax/Semantics domains**: `AMIL_RELATION_DOMAIN`, `I3RAB_SURFACE_DOMAIN`, `SYNTAX_DOMAIN`, `SEMANTICS_DOMAIN`, `PRAGMATICS_DOMAIN` exist for future U₁₁-U₁₅ layers.

**Previously Non-Existent DomainTypes** (Now added):
- ✅ `IDENTITY_DOMAIN` - ADDED (PR-125) - محور الهوية
- ✅ `WORDFORM_DOMAIN` - ADDED (PR-125) - صورة الكلمة المرشحة

**Previously Non-Existent DalTransitionDomain** (Now added):
- ✅ `WORDFORM` - ADDED (PR-126) - صورة الكلمة (U₁₀)

**Still Non-Existent DomainTypes** (Previously hallucinated):
- ❌ `PHONEME_DOMAIN` - does NOT exist (use `SOUND_DOMAIN`)
- ❌ `PRE_MORPHOLOGICAL_DOMAIN` - does NOT exist (use `BOUNDARY_DOMAIN` or `LAFZ_DOMAIN`)
- ❌ `ROOT_DOMAIN` - does NOT exist (use `ROOT_STEM_DOMAIN`)
- ❌ `PATTERN_DOMAIN` - does NOT exist

### Map 3: D_mufrad Pipeline → Dal Architecture

✅ **STATUS**: RESOLVED (Updated 2026-05-27, PR-126)

**Decision**: Option B - Map to existing DalTransitionDomain (APPROVED with corrections)

| D_mufrad Stage | File | DalTransitionDomain | ExecutionLayer | DomainType | Status |
|----------------|------|---------------------|----------------|------------|--------|
| atoms → DForm | `d_form.py` | `PRE_MORPH` | U₃, U₄ | `BOUNDARY_DOMAIN`, `LAFZ_DOMAIN` | ⚠️ Tentative |
| DForm → DLugha | `d_lugha.py` | `ORIGIN` | U₈ | `ROOT_STEM_DOMAIN` | ✅ Likely correct |
| DLugha → DType | `d_type.py` | `IDENTITY_AXIS` | U₅, U₆ | `IDENTITY_DOMAIN` | ✅ RESOLVED (PR-125) |
| DType → DMufrad | `d_mufrad.py` | `WORDFORM` | U₁₀ | `WORDFORM_DOMAIN` | ✅ RESOLVED (PR-126) |

**Resolved Issues**:
1. ✅ **IDENTITY_DOMAIN added** (PR-125): DType (Ism/Fi'l/Harf classification) now has corresponding DomainType.
2. ✅ **WORDFORM_DOMAIN added** (PR-125): U₁₀ WordFormCandidate now has its own domain.
3. ✅ **WORDFORM DalTransitionDomain added** (PR-126): U₁₀ now has its own transition domain.
4. ✅ **DMufrad ≠ JUDGMENT**: Clarified and enforced. DMufrad is NOT final judgment (no Ifādah, no Hukm). It's a closed lexical form/word contract.
5. ✅ **U₁₀ mapping corrected**: U10_WORD_FORM removed from JUDGMENT, now properly mapped to WORDFORM.

**Previously Identified Gaps** (Now RESOLVED):
- ~~Missing IDENTITY_DOMAIN~~: ✅ ADDED (PR-125)
- ~~Missing WORDFORM_DOMAIN~~: ✅ ADDED (PR-125)
- ~~U₁₀ incorrectly mapped to JUDGMENT_DOMAIN~~: ✅ CORRECTED (PR-126)
- ~~Missing WORDFORM DalTransitionDomain~~: ✅ ADDED (PR-126)

**Rejected Options**:
- **Option A** (Extend DalTransitionDomain): Would create parallel D_mufrad-specific domains
- **Option C** (Keep separate): Would break kernel integration

**Current Reality**: D_mufrad pipeline exists and works, and dal_algebra mapping is now COMPLETE for existing DomainType requirements.

## PR-1B Status: Complete - Metadata Added

✅ **COMPLETE**: PR-1B added dal_* fields with metadata integration.

### What PR-1B Added

1. **DecisionAudit** extended with 3 optional fields:
   ```python
   dal_contract: Optional[DalTransitionContract] = None
   dal_domain: Optional[DalTransitionDomain] = None
   dal_claim_scope: Optional[DalClaimScope] = None
   ```

2. **ApprovedTransitionContext** extended with same 3 fields

3. **DAL_KERNEL_MAPPING.md** created (this document)

### Current Status: Transitional Metadata (Validation Added in PR-122)

The dal_* fields were initially **transitional metadata**. PR-122 added full validation.

## PR-122 Status: Complete - Validators Implemented

✅ **COMPLETE**: PR-122 added dal_kernel mapping validators and enforcement.

### What PR-122 Added

1. ✅ **dal_kernel_validators.py module** with validation functions
2. ✅ **Canonical mapping tables** (immutable):
   - `DAL_DOMAIN_TO_EXECUTION_LAYER_MAP`
   - `DAL_DOMAIN_TO_DOMAIN_TYPE_MAP`
   - `DAL_DOMAIN_TO_CLAIM_SCOPE_MAP`
3. ✅ **validate_dal_kernel_mapping()** function
4. ✅ **AlgebraicDecisionCore integration** - validates dal_* fields in audit_decision()
5. ✅ **ApprovedTransitionContext enforcement** - blocks creation with invalid dal_* metadata
6. ✅ **CPBStatus.DAL_KERNEL_INCONSISTENCY** - new status for kernel violations
7. ✅ **Comprehensive tests** - 22 tests covering all validation rules

### Validation Enforcement

The dal_* fields are now **validated governance metadata**.

Enforcement points:
1. **AlgebraicDecisionCore.audit_decision()** validates dal_* consistency
2. **ApprovedTransitionContext.__post_init__()** validates dal_* before creation
3. Invalid dal_* combinations are **BLOCKED** with clear violation messages

### Validation Rules (Enforced)

1. ✅ dal_domain ↔ from_layer/to_layer consistency
2. ✅ dal_domain ↔ domain consistency
3. ✅ dal_claim_scope ↔ dal_domain consistency
4. ✅ dal_contract ↔ dal_domain/dal_claim_scope consistency
5. ✅ Legacy mode (dal_domain=None) allowed for backward compatibility

### Implementation Details (PR-122)

**Location**: `src/dal_core/dal_kernel_validators.py`

**Main Function**:
```python
def validate_dal_kernel_mapping(
    dal_domain: DalTransitionDomain | None,
    dal_claim_scope: DalClaimScope | None,
    dal_contract: DalTransitionContract | None,
    from_layer: ExecutionLayer,
    to_layer: ExecutionLayer,
    domain: DomainType
) -> Tuple[str, ...]:
    """
    Validate consistency between dal_* fields and ExecutionLayer/DomainType.

    Returns tuple of validation error messages (empty if valid).

    Validation Rules:
        1. If dal_domain is None: allow legacy mode (no validation)
        2. If dal_domain present: must match from_layer/to_layer
        3. If dal_claim_scope present: must be allowed for dal_domain
        4. If dal_contract present: must match dal_domain/dal_claim_scope
        5. Domain mapping must be consistent (or documented GAP)
    """
```

**Status**: ✅ IMPLEMENTED (PR-122)

**Tests**: ✅ IMPLEMENTED - 22 comprehensive tests in `tests/dal_core/test_dal_kernel_validators.py`

### Validation Rules (Enforced in PR-122)

### Rule 1: Domain Consistency
If `DecisionAudit.dal_domain` is set, it MUST be consistent with `from_layer` and `to_layer`.

**Example**:
- `dal_domain=SYLLABIC` → `from_layer` and `to_layer` must be within U₂s range

✅ **Status**: ENFORCED in `algebraic_decision_core.py:audit_decision()`

### Rule 2: Claim Scope Consistency
If `DecisionAudit.dal_claim_scope` is set, it MUST be consistent with `dal_domain`.

**Example**:
- `dal_domain=SYLLABIC` → `dal_claim_scope` can only be `SYLLABLE_STRUCTURE_VALID`

✅ **Status**: ENFORCED in `algebraic_decision_core.py:audit_decision()`

### Rule 3: Contract Consistency
If `DecisionAudit.dal_contract` is set:
- `dal_contract.source_domain` must match source `dal_domain`
- `dal_contract.target_domain` must match target `dal_domain`
- `dal_contract.claim_scope` must match `dal_claim_scope`

✅ **Status**: ENFORCED in `algebraic_decision_core.py:audit_decision()` and `approved_transition_context.py:__post_init__()`

## Integration Example

✅ **WORKING EXAMPLE** (validators implemented in PR-122):

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

- **2026-05-27 (PR-125)**: Domain gaps resolved - **COMPLETE**
  - Added IDENTITY_DOMAIN to DomainType enum and DomainRegistry
  - Added WORDFORM_DOMAIN to DomainType enum and DomainRegistry
  - Updated Map 2: IDENTITY_AXIS → IDENTITY_DOMAIN (removed GAP)
  - Updated Map 3: DMufrad → WORDFORM_DOMAIN (resolved)
  - Removed GAP handling in validate_dal_kernel_mapping()
  - Added 5 new tests for IDENTITY_DOMAIN and WORDFORM_DOMAIN
  - **Status**: Map 2 and Map 3 now COMPLETE ✅

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
2. ✅ **PR-1B**: Complete - Metadata integration
   - [x] Fix DAL_KERNEL_MAPPING.md (hallucinated DomainType names) ✅ DONE
   - [x] Add dal_* fields to DecisionAudit/ApprovedTransitionContext ✅ DONE
3. ✅ **PR-122**: Complete - Validators implemented
   - [x] Add validate_dal_kernel_mapping() function ✅ DONE
   - [x] Add tests for dal_* field validation (22 tests) ✅ DONE
   - [x] Integrate validation into AlgebraicDecisionCore ✅ DONE
   - [x] Add CPBStatus.DAL_KERNEL_INCONSISTENCY ✅ DONE
   - [x] Consider adding IDENTITY_DOMAIN and WORDFORM_DOMAIN to DomainType ✅ DONE (PR-125)
4. ✅ **PR-1C**: Complete - Hybrid failure semantics
   - [x] Implement Option C (hybrid failure semantics) ✅ DONE
   - [x] Update dal_algebra.py docstring ✅ DONE
   - [x] Update DalTransitionProtocol.apply() signature ✅ DONE
   - [x] Add AlgebraicFailure dataclass ✅ DONE
   - [x] Add comprehensive tests (18 AlgebraicFailure tests) ✅ DONE
   - [x] Create BACKLOG.md with identified gaps ✅ DONE
5. ✅ **PR-125**: Complete - Domain gaps resolved
   - [x] Add IDENTITY_DOMAIN to DomainType and DomainRegistry ✅ DONE
   - [x] Add WORDFORM_DOMAIN to DomainType and DomainRegistry ✅ DONE
   - [x] Update DAL_DOMAIN_TO_DOMAIN_TYPE_MAP: IDENTITY_AXIS → IDENTITY_DOMAIN ✅ DONE
   - [x] Remove GAP handling in validate_dal_kernel_mapping() ✅ DONE
   - [x] Add 5 tests for IDENTITY_DOMAIN and WORDFORM_DOMAIN ✅ DONE
   - [x] Update BACKLOG.md (items #1, #2 resolved) ✅ DONE
   - [x] Update DAL_KERNEL_MAPPING.md (maps 2 and 3 complete) ✅ DONE
6. ✅ **PR-126**: Complete - U10/JUDGMENT/WORDFORM mapping corrected
   - [x] Add WORDFORM to DalTransitionDomain (dal_algebra.py) ✅ DONE
   - [x] Add WORDFORM_DETERMINED to DalClaimScope (dal_algebra.py) ✅ DONE
   - [x] Remove U10_WORD_FORM from JUDGMENT execution mapping ✅ DONE
   - [x] Add WORDFORM → U10_WORD_FORM execution mapping ✅ DONE
   - [x] Add WORDFORM → WORDFORM_DOMAIN domain mapping ✅ DONE
   - [x] Add WORDFORM → WORDFORM_DETERMINED claim scope mapping ✅ DONE
   - [x] Add 6 tests for WORDFORM domain mapping ✅ DONE
   - [x] Update DAL_KERNEL_MAPPING.md (all maps corrected) ✅ DONE
   - [x] Update BACKLOG.md (item #4 resolved) ✅ PENDING
7. ✅ **PR-127**: Complete - Path-aware IDENTITY_DOMAIN prerequisites
   - [x] Fix WEIGHT_IDENTITY logic bug (AND → ONE-OF for root/stem) ✅ DONE
   - [x] Remove unconditional WEIGHT_DOMAIN requirement from IDENTITY_DOMAIN ✅ DONE
   - [x] Remove unconditional WEIGHT_IDENTITY requirement from WORDFORM_IDENTITY ✅ DONE
   - [x] Add 17 tests proving path-aware identity (weighted vs non-weighted paths) ✅ DONE
   - [x] Update DAL_KERNEL_MAPPING.md with path-aware notes ✅ DONE
   - [x] Update BACKLOG.md (new item documenting PR-127) ✅ PENDING
8. 🔵 **PR-2**: READY to proceed (all foundational gaps closed)

---

**Last Updated**: 2026-05-27 (PR-127: Path-aware IDENTITY_DOMAIN prerequisites)
**Status**: PR-1B complete, PR-122 complete, PR-1C complete, PR-125 complete, PR-126 complete, PR-127 complete
**Achievement**: Dal kernel mapping fully validated and enforced, hybrid failure semantics implemented, all critical domain gaps closed, U₁₀ architectural violation corrected, path-aware identity prerequisites implemented
