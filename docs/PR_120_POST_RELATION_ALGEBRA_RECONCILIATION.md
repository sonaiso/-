# PR #120: Post-RelationAlgebraCore Architecture Reconciliation

**Status**: PLANNING
**Type**: Maintenance / Architecture Strengthening
**Branch**: TBD
**Date**: 2026-05-26

---

## Context

PR #119 successfully merged **RelationAlgebraCore** foundation, converting relations from enum labels to identity-preserving operations. This was a critical step preventing "tagging" architecture.

However, **architectural review** identified that PR #119, while correct in direction, is incomplete and has gaps that **MUST** be resolved before implementing U₁₁ execution layers.

## Constitutional Law

```
لا U₁₁ قبل جبر علاقة قوي
No U₁₁ before strong relation algebra

ولا جبر علاقة قوي بلا حفظ instance identity
No strong relation algebra without instance identity preservation

ولا حفظ هوية بلا anchor_id
No identity preservation without anchor_id

ولا علاقة بلا load typed
No relation without typed load

ولا توسعة قبل إصلاح خريطة الطبقات
No expansion before fixing layer map
```

---

## PR #119 Assessment

### What It Did Right ✅

1. **Relations as Operations** (not labels)
   - `IsnadOperation`, `TadminOperation`, `TaqyidOperation`, `WasfOperation`, `IdafahOperation`
   - Each has `apply()` and `get_invariant()` methods

2. **Identity Preservation Enforcement**
   - `RelationIdentityInvariant` checks that input identities appear in output
   - Raises error on "Identity collapse"

3. **Forbidden Output Blocking**
   - Relations CANNOT emit `SEMANTIC_IDENTITY`, `IFADAH_IDENTITY`, `HUKM_IDENTITY`
   - Forces `Rank.CANDIDATE` (never CERTIFIED)

4. **Anchor Types Defined**
   - `EntityAnchor` (جامد)
   - `TransformationAnchor` (مشتق)
   - `FunctionAnchor` (مبني)

5. **15/15 Tests Passing**

### Critical Gaps Identified 🔴

#### Gap 1: Weak Identity Preservation

**Problem**:
- Tests use **same** `IdentityType.FORM_IDENTITY` for both entity and transformation
- Preserving `{FORM_IDENTITY}` doesn't prove both anchors preserved **separately**

**Example from PR #119 tests**:
```python
entity = EntityAnchor(identity=IdentityType.FORM_IDENTITY, ...)
transformation = TransformationAnchor(identity=IdentityType.FORM_IDENTITY, ...)

result = IsnadOperation().apply((entity, transformation))

# This only proves:
assert FORM_IDENTITY in result.preserved_identities  # ❌ WEAK

# Doesn't prove:
# - entity anchor preserved as distinct from transformation
# - instance-level identity maintained
```

**Required Fix**:
```python
# Add instance identity
entity = EntityAnchor(
    anchor_id="entity_123",  # NEW
    identity=IdentityType.FORM_IDENTITY,
    ...
)

transformation = TransformationAnchor(
    anchor_id="transformation_456",  # NEW
    identity=IdentityType.FORM_IDENTITY,
    ...
)

result = IsnadOperation().apply((entity, transformation))

# Must preserve BOTH:
assert FORM_IDENTITY in result.preserved_identities  # type identity
assert "entity_123" in result.preserved_anchor_ids    # instance identity ✅
assert "transformation_456" in result.preserved_anchor_ids  # instance identity ✅
```

**Law**:
```
حفظ الهوية = حفظ النوع + حفظ المثيل
Identity preservation = type preservation + instance preservation
```

#### Gap 2: String-Based Loads (Not Typed)

**Problem**:
- Relation loads are strings:
  - `"predication_load"`
  - `"restriction_load"`
  - `"containment_load"`
  - `"attachment_load"`

**This is "enhanced tagging", not full algebra.**

**Required Fix**:
```python
# Define typed load objects
@dataclass(frozen=True)
class PredicationLoad:
    """الحمل الإسنادي - Predication load"""
    bearer_anchor_id: str          # الحامل
    carried_anchor_id: str         # المحمول
    polarity: PolarityType         # affirmed | negated | near | epistemic
    scope: ScopeType               # local | clause | sentence
    residuals: FrozenSet[Residual]
    trace: Tuple[str, ...]

@dataclass(frozen=True)
class RestrictionLoad:
    """الحمل التقييدي - Restriction load"""
    base_anchor_id: str
    restrictor_anchor_id: str
    scope: ScopeType               # local | phrase | clause
    narrowing_type: NarrowingType  # temporal | locative | conditional | ...
    residuals: FrozenSet[Residual]
    trace: Tuple[str, ...]

@dataclass(frozen=True)
class ContainmentLoad:
    """الحمل التضميني - Containment load"""
    container_anchor_id: str
    contained_anchor_id: str
    containment_mode: ContainmentMode  # part_whole | conceptual | lafzi | structural
    residuals: FrozenSet[Residual]
    trace: Tuple[str, ...]

# Similarly: DescriptionLoad, AttachmentLoad
```

**Usage**:
```python
result = IsnadOperation().apply((entity, transformation))

# Instead of:
assert "predication_load" in result.added_loads  # ❌ string

# Use:
assert isinstance(result.predication_load, PredicationLoad)  # ✅ typed
assert result.predication_load.bearer_anchor_id == entity.anchor_id
assert result.predication_load.carried_anchor_id == transformation.anchor_id
```

#### Gap 3: WEIGHT_IDENTITY Bug

**Problem** (from `identity_registry.py:344-346`):
```python
WEIGHT_IDENTITY: IdentityNode = IdentityNode(
    identity_type=IdentityType.WEIGHT_IDENTITY,
    required_upstream={
        frozenset({ROOT_MATERIAL_IDENTITY, STEM_IDENTITY})  # ❌ requires BOTH
    },
    ...
)
```

**Issue**: Requires BOTH root AND stem, but weight can derive from ONE-OF:
- Root-based derivation (فَعَلَ → pattern)
- Stem-based derivation (existing stem → pattern)

**Required Fix**:
```python
WEIGHT_IDENTITY: IdentityNode = IdentityNode(
    identity_type=IdentityType.WEIGHT_IDENTITY,
    required_upstream={
        frozenset({ROOT_MATERIAL_IDENTITY}),  # OR root
        frozenset({STEM_IDENTITY})            # OR stem
    },
    ...
)
```

#### Gap 4: U₁₁ Canonical Map Unresolved

**Problem**: Multiple conflicting definitions of U₁₁:
- `execution_layer_registry.py`: U₁₁ = LexicalEntry
- Memory/docs: U₁₁ = PreLexicalWordCandidate or RelationCompositionCandidate

**Required**: Create `CANONICAL_POST_U10_LAYER_MAP.md` answering:
1. What is U₁₁? (PreLexicalWord? RelationComposition? LexicalEntry?)
2. Where does RelationAlgebraCore sit? (foundation, not execution)
3. What is U₁₂? (Composition? Ifadah?)
4. What is U₁₃? (LexicalEntry? Hukm?)
5. What legacy files map to which U layer?

#### Gap 5: PR #118 Not Reconciled

**Problem**: PR #118 modified `ExecutionLayer` registry and introduced U₁₁/U₁₂/U₁₃ definitions. PR #119 added algebraic foundation but didn't reconcile the layer map.

**Required**: Explicit reconciliation document showing:
- What PR #118 changed
- What RelationAlgebraCore requires
- How they integrate
- What conflicts remain

---

## PR #120 Requirements

### Title
```
chore: Reconcile post-RelationAlgebraCore architecture before U₁₁ execution
```

### Goal
**Do NOT implement U₁₁ yet.** Reconcile the layer map, identity model, and relation algebra strength before any composition execution layer.

### Hard Rules (MUST NOT)

1. ❌ Do not add U₁₂ or U₁₃ logic
2. ❌ Do not expand U₁₁ execution
3. ❌ Do not treat RelationAlgebraCore as closed/complete
4. ❌ Do not use identical `IdentityType.FORM_IDENTITY` as proof that two operands are preserved
5. ❌ Do not use strings as final algebraic loads
6. ❌ Do not proceed before fixing WEIGHT_IDENTITY root/stem requirement
7. ❌ Do not proceed before canonical U₁₁ map is decided

### Required Tasks

#### A. Fix WEIGHT_IDENTITY Bug

**Files**: `src/dal_core/identity_registry.py`

**Changes**:
1. Change WEIGHT_IDENTITY from AND (both required) to ONE-OF (either root or stem)
2. Add tests:
   - `test_weight_identity_accepts_root_material_path`
   - `test_weight_identity_accepts_stem_path`
   - `test_weight_identity_does_not_require_both_root_and_stem`

**Before**:
```python
required_upstream={
    frozenset({ROOT_MATERIAL_IDENTITY, STEM_IDENTITY})  # AND
}
```

**After**:
```python
required_upstream={
    frozenset({ROOT_MATERIAL_IDENTITY}),  # OR root
    frozenset({STEM_IDENTITY})            # OR stem
}
```

#### B. Strengthen RelationAlgebraCore Identity Preservation

**Files**: `src/dal_core/relation_algebra_core.py`

**Changes**:

1. **Add `anchor_id` to all anchors**:
```python
@dataclass(frozen=True)
class EntityAnchor:
    anchor_id: str  # NEW - instance identity
    identity: IdentityType
    verified_bearability: bool
    trace: Tuple[str, ...]

@dataclass(frozen=True)
class TransformationAnchor:
    anchor_id: str  # NEW - instance identity
    identity: IdentityType
    origin_root_id: str
    pattern_id: str
    trace: Tuple[str, ...]

@dataclass(frozen=True)
class FunctionAnchor:
    anchor_id: str  # NEW - instance identity
    identity: IdentityType
    trace: Tuple[str, ...]
```

2. **Add `preserved_anchor_ids` to RelationResult**:
```python
@dataclass(frozen=True)
class RelationResult:
    preserved_identities: FrozenSet[IdentityType]  # type identity
    preserved_anchor_ids: FrozenSet[str]           # NEW - instance identity
    added_loads: Tuple[str, ...]  # Will be replaced by typed loads
    residuals: FrozenSet[Residual]
    rank: Rank
    trace: Tuple[str, ...]
```

3. **Add tests**:
   - `test_isnad_preserves_distinct_entity_and_transformation_anchor_ids`
   - `test_tadmin_preserves_container_and_contained_anchor_ids`
   - `test_taqyid_preserves_base_and_restrictor_anchor_ids`
   - `test_wasf_preserves_mawsuf_and_sifah_anchor_ids`
   - `test_idafah_preserves_mudaf_and_mudaf_ilayh_anchor_ids`

#### C. Replace String Loads with Typed Load Objects

**Files**:
- `src/dal_core/relation_algebra_core.py` (add load types)
- `src/dal_core/relation_loads.py` (NEW FILE)

**Changes**:

1. **Create typed load objects**:
```python
# src/dal_core/relation_loads.py

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, FrozenSet

@dataclass(frozen=True)
class PredicationLoad:
    """إسناد - Predication (entity bears transformation)"""
    bearer_anchor_id: str
    carried_anchor_id: str
    polarity: PolarityType
    scope: ScopeType
    residuals: FrozenSet[Residual]
    trace: Tuple[str, ...]

@dataclass(frozen=True)
class RestrictionLoad:
    """تقييد - Restriction (base restricted by restrictor)"""
    base_anchor_id: str
    restrictor_anchor_id: str
    scope: ScopeType
    narrowing_type: NarrowingType
    residuals: FrozenSet[Residual]
    trace: Tuple[str, ...]

@dataclass(frozen=True)
class ContainmentLoad:
    """تضمين - Containment (container contains contained)"""
    container_anchor_id: str
    contained_anchor_id: str
    containment_mode: ContainmentMode
    residuals: FrozenSet[Residual]
    trace: Tuple[str, ...]

@dataclass(frozen=True)
class DescriptionLoad:
    """وصف - Description (mawsuf described by sifah)"""
    mawsuf_anchor_id: str
    sifah_anchor_id: str
    agreement_residuals: FrozenSet[Residual]
    trace: Tuple[str, ...]

@dataclass(frozen=True)
class AttachmentLoad:
    """إضافة - Attachment (mudaf attached to mudaf ilayh)"""
    mudaf_anchor_id: str
    mudaf_ilayh_anchor_id: str
    ownership_type: OwnershipType  # possession | part_whole | specification
    residuals: FrozenSet[Residual]
    trace: Tuple[str, ...]
```

2. **Update RelationResult**:
```python
@dataclass(frozen=True)
class RelationResult:
    preserved_identities: FrozenSet[IdentityType]
    preserved_anchor_ids: FrozenSet[str]

    # Replace added_loads: Tuple[str, ...] with:
    predication_load: Optional[PredicationLoad] = None
    restriction_load: Optional[RestrictionLoad] = None
    containment_load: Optional[ContainmentLoad] = None
    description_load: Optional[DescriptionLoad] = None
    attachment_load: Optional[AttachmentLoad] = None

    residuals: FrozenSet[Residual]
    rank: Rank
    trace: Tuple[str, ...]
```

3. **Add tests**:
   - `test_isnad_produces_typed_predication_load`
   - `test_taqyid_produces_typed_restriction_load`
   - `test_tadmin_produces_typed_containment_load`
   - `test_wasf_produces_typed_description_load`
   - `test_idafah_produces_typed_attachment_load`
   - `test_load_objects_preserve_anchor_ids`
   - `test_load_objects_preserve_residuals`

#### D. Create Canonical Layer Map

**Files**: `docs/CANONICAL_POST_U10_LAYER_MAP.md` (NEW)

**Content**:

```markdown
# Canonical Post-U₁₀ Layer Map

**Status**: CANONICAL REFERENCE
**Date**: 2026-05-26
**Authority**: Architectural Decision Record

---

## Purpose

This document provides the **single canonical mapping** of post-U₁₀ layers, reconciling:
- PR #118 (execution layer registry changes)
- PR #119 (RelationAlgebraCore foundation)
- Historical memory definitions
- Constitutional laws

---

## Canonical Layer Sequence

### U₁₀: WordFormCandidate ✅ IMPLEMENTED
- **File**: `src/dal_core/u10_word_form_candidate_carrier.py`
- **Status**: Foundation complete
- **Purpose**: Word form structure after WEIGHT_IDENTITY
- **Input**: U₉ WeightCandidate
- **Output**: WordFormCandidate
- **Forbidden**: SEMANTIC_IDENTITY, HUKM_IDENTITY, FUNCTIONAL_RELATION_IDENTITY

### RelationAlgebraCore 🔧 FOUNDATION (Not Execution Layer)
- **File**: `src/dal_core/relation_algebra_core.py`
- **Status**: Foundation complete (PR #119), **needs strengthening** (PR #120)
- **Purpose**: Algebraic operations for relations (ISNAD, TADMIN, TAQYID, WASF, IDAFAH)
- **Type**: **Algebraic specification**, NOT execution layer
- **Used by**: U₁₁, U₁₂ (future)

### U₁₁: [DECISION REQUIRED]
**Options**:
1. **PreLexicalWordCandidate** (classification: جامد/مشتق, مبني/معرب)
2. **RelationCompositionCandidate** (relation establishment)
3. **LexicalEntry** (meaning in context)

**Current conflict**:
- `execution_layer_registry.py` defines U₁₁ as LexicalEntry
- Memory defines U₁₁ as PreLexicalWordCandidate or RelationCompositionCandidate

**Recommended**: U₁₁ = PreLexicalWordCandidate
- Classifies: جامد (entity) / مشتق (transformation) / مبني (function)
- Classifies: مبني (frozen) / معرب (inflectable)
- Creates: EntityAnchor, TransformationAnchor, FunctionAnchor
- Does NOT establish relations yet

### U₁₂: [DECISION REQUIRED]
**Options**:
1. **CompositionCandidate** (relation establishment using RelationAlgebraCore)
2. **IfadahCandidate** (pragmatic closure)

**Recommended**: U₁₂ = CompositionCandidate
- Consumes: U₁₁ anchors
- Applies: RelationAlgebraCore operations (ISNAD, TADMIN, TAQYID, WASF, IDAFAH)
- Produces: RelationResult with typed loads
- Does NOT assign meaning yet

### U₁₃: [DECISION REQUIRED]
**Options**:
1. **LexicalEntry** (meaning in context)
2. **IfadahCandidate** (pragmatic closure)
3. **HukmCandidate** (epistemic truth)

**Recommended**: U₁₃ = LexicalEntry
- Assigns meaning in compositional context
- Still CANDIDATE rank (not certified truth)

### U₁₄: [FUTURE]
**Recommended**: IfadahCandidate
- Pragmatic closure (تمام الإفادة)
- Determines: assertion, question, command, exclamation

### U₁₅: [FUTURE]
**Recommended**: HukmCandidate
- Epistemic truth judgment
- Requires evidence
- May reach CERTIFIED rank

---

## Reconciliation with PR #118

PR #118 modified `execution_layer_registry.py` but created layer name conflicts.

**Action**: Update `execution_layer_registry.py` to match canonical map above.

---

## Reconciliation with PR #119

PR #119 added RelationAlgebraCore as **foundation** (not execution layer).

**Clarification**: RelationAlgebraCore is **algebraic specification** used by U₁₁/U₁₂, not a U layer itself.

---

## Constitutional Law Alignment

✅ لا انتقال من اللفظ المفرد إلى المعنى حتى تثبت علاقته في التركيب
   No isolated-word→meaning jump without compositional relation

✅ لا U₁₁ قبل RelationAlgebraCore
   No U₁₁ before RelationAlgebraCore

✅ لا تركيب بلا مفردات مرخصة
   No composition without licensed words

---

## Decision Record

**Date**: [TBD]
**Decision**: [PENDING]
**Authority**: Project maintainer approval required

---
```

#### E. Add Governance Tests

**Files**: `tests/dal_core/test_relation_algebra_governance.py` (NEW)

**Tests**:

```python
def test_relation_algebra_core_is_not_execution_layer():
    """Verify RelationAlgebraCore is foundation, not execution layer."""
    from dal_core.execution_layer_registry import EXECUTION_CORE_LAYERS

    # RelationAlgebraCore should NOT appear as execution layer
    layer_names = [layer.name for layer in EXECUTION_CORE_LAYERS]
    assert "RelationAlgebraCore" not in layer_names
    assert "RELATION_ALGEBRA" not in layer_names

def test_u11_must_not_create_algebraic_decision_core():
    """U₁₁ is not governed layer, uses RelationAlgebraCore operations."""
    # When U₁₁ is implemented, verify it doesn't instantiate AlgebraicDecisionCore
    pass  # Mark as xfail until U₁₁ implemented

def test_u11_must_use_relation_algebra_operations():
    """U₁₁ must consume RelationAlgebraCore operations, not define new labels."""
    # When U₁₁ is implemented, verify it uses IsnadOperation, etc.
    pass  # Mark as xfail until U₁₁ implemented

def test_relation_operations_preserve_anchor_instance_ids():
    """All relation operations must preserve anchor instance IDs."""
    from dal_core.relation_algebra_core import (
        EntityAnchor, TransformationAnchor,
        IsnadOperation, TadminOperation, TaqyidOperation
    )

    entity = EntityAnchor(
        anchor_id="entity_test_123",
        identity=IdentityType.FORM_IDENTITY,
        verified_bearability=True,
        trace=("u0",)
    )

    transformation = TransformationAnchor(
        anchor_id="transformation_test_456",
        identity=IdentityType.FORM_IDENTITY,
        origin_root_id="root_ktb",
        pattern_id="pattern_faeil",
        trace=("u0",)
    )

    result = IsnadOperation().apply((entity, transformation))

    # Must preserve instance IDs
    assert "entity_test_123" in result.preserved_anchor_ids
    assert "transformation_test_456" in result.preserved_anchor_ids
```

---

## Acceptance Criteria

### Must Have ✅

1. **WEIGHT_IDENTITY bug fixed** with passing tests
2. **Anchor instance IDs** added to all anchor types
3. **RelationResult preserves anchor IDs** with passing tests
4. **Typed load objects** defined (at minimum: stubs with TODO for full implementation)
5. **CANONICAL_POST_U10_LAYER_MAP.md** created with clear decisions
6. **All existing tests still pass** (no regressions)
7. **Governance tests** added (may be marked xfail for future verification)

### Must NOT Have ❌

1. No new execution layer implementation
2. No U₁₁ logic
3. No U₁₂ logic
4. No U₁₃ logic
5. No expansion of RelationAlgebraCore beyond strengthening

### Documentation Requirements 📄

All documentation must clearly distinguish:
- **Implemented** (working code with tests)
- **Stub** (placeholder with TODO)
- **Algebra foundation** (specification, not execution)
- **Execution layer** (part of pipeline)
- **Future design** (not yet implemented)

### Test Requirements 🧪

New xfail tests are acceptable ONLY if:
1. Explicitly marked as `@pytest.mark.xfail(reason="architectural debt: ...")`
2. Documented in commit message why xfail
3. Linked to future implementation plan

---

## Implementation Order

1. **Phase 1: WEIGHT_IDENTITY Fix** (immediate)
   - Fix `identity_registry.py`
   - Add 3 tests
   - Verify all existing tests pass

2. **Phase 2: Instance Identity** (immediate)
   - Add `anchor_id` to anchors
   - Add `preserved_anchor_ids` to RelationResult
   - Update all operations to preserve anchor IDs
   - Add 5 new tests

3. **Phase 3: Typed Loads** (can be stubs initially)
   - Define load dataclasses in `relation_loads.py`
   - Add load fields to RelationResult
   - Add 7 new tests (may be xfail for stub phase)

4. **Phase 4: Canonical Map** (documentation)
   - Create CANONICAL_POST_U10_LAYER_MAP.md
   - Get stakeholder approval on layer decisions
   - Update execution_layer_registry.py comments

5. **Phase 5: Governance Tests** (validation)
   - Add governance tests
   - Mark future-verification tests as xfail
   - Document architectural debt

---

## Success Criteria

**This PR succeeds if:**
1. RelationAlgebraCore is **strengthened** (not expanded)
2. Identity preservation is **rigorous** (type + instance)
3. WEIGHT_IDENTITY bug is **fixed**
4. Layer map is **canonically decided**
5. **No new execution layer** added
6. All tests pass (new xfails acceptable with justification)

**This PR fails if:**
1. U₁₁/U₁₂/U₁₃ execution logic added
2. RelationAlgebraCore treated as "closed/complete"
3. Layer map still ambiguous after PR
4. Test coverage decreases
5. Identity preservation still weak

---

## Constitutional Alignment

This PR enforces:

```
لا U₁₁ قبل جبر علاقة قوي
No U₁₁ before strong relation algebra

ولا جبر علاقة قوي بلا حفظ instance identity
No strong relation algebra without instance identity preservation

ولا حفظ هوية بلا anchor_id
No identity preservation without anchor_id

ولا علاقة بلا load typed
No relation without typed load

ولا توسعة قبل إصلاح خريطة الطبقات
No expansion before fixing layer map
```

---

**Status**: PLANNING DOCUMENT
**Next Step**: Review and approval before implementation
**Estimated Scope**: 5-7 files modified, 500-800 new lines (mostly tests/docs)
**Risk Level**: LOW (maintenance/strengthening, no new execution logic)

---
