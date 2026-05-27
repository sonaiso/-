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

| DalTransitionDomain | DomainType(s) | Description |
|---------------------|---------------|-------------|
| `GRAPHOPHONEMIC` | `PHONEME_DOMAIN` | Phonological space |
| `SYLLABIC` | `SYLLABLE_DOMAIN` | Syllabic structure |
| `PRE_MORPH` | `PRE_MORPHOLOGICAL_DOMAIN` | Pre-morphological classification |
| `ORIGIN` | `ROOT_DOMAIN` | Root material |
| `TEMPLATE` | `PATTERN_DOMAIN`, `WEIGHT_DOMAIN` | Template patterns and weights |
| `IDENTITY_AXIS` | `IDENTITY_DOMAIN` | Identity axis classification |
| `DIRECTIONAL_ANALYSIS` | `FORM_DOMAIN` | Directional analysis |
| `JUDGMENT` | `WORDFORM_DOMAIN` | Morphological judgment |

**Note**: Some DalTransitionDomains map to multiple DomainTypes. This is intentional - TEMPLATE domain covers both pattern matching (`PATTERN_DOMAIN`) and weight determination (`WEIGHT_DOMAIN`).

### Map 3: D_mufrad Pipeline → Dal Architecture

**Decision**: Option B - Map to existing DalTransitionDomain (APPROVED)

| D_mufrad Stage | File | DalTransitionDomain | ExecutionLayer | DomainType | Status |
|----------------|------|---------------------|----------------|------------|--------|
| atoms → DForm | `d_form.py` | `PRE_MORPH` | U₃ | `PRE_MORPHOLOGICAL_DOMAIN` | ✅ Mapped |
| DForm → DLugha | `d_lugha.py` | `ORIGIN` | U₈ | `ROOT_DOMAIN` | ✅ Mapped |
| DLugha → DType | `d_type.py` | `IDENTITY_AXIS` | U₅, U₆ | `IDENTITY_DOMAIN` | ✅ Mapped |
| DType → DMufrad | `d_mufrad.py` | `JUDGMENT` | U₁₀ | `WORDFORM_DOMAIN` | ✅ Mapped |

**Rejected Options**:
- **Option A** (Extend DalTransitionDomain): Would create parallel D_mufrad-specific domains
- **Option C** (Keep separate): Would break kernel integration

## Integration Example

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

- **2026-05-27**: Initial canonical mapping (PR-1B)
- Map 1: DalTransitionDomain → ExecutionLayer ✅
- Map 2: DalTransitionDomain → DomainType ✅
- Map 3: D_mufrad Pipeline → Dal Architecture (Option B selected) ✅

---

**Next Steps**:
- PR-1C: Resolve failure semantics (value-based vs exception-based)
- PR-2: Promote dal_algebra.py with resolved semantics and kernel integration
