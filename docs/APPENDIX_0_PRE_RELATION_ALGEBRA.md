# Appendix 0-Pre: Relation Algebra Before Meaning and Operators

**ملحق 0-سابق: جبر العلاقات قبل المعنى والعوامل**

## Constitutional Position (الموقع الدستوري)

This appendix defines the **algebraic foundation** for composition BEFORE:
- U₁₁ (PreLexicalWordCandidate / CompositionCandidate)
- U₁₂ (IfadahCandidate)
- U₁₃ (HukmCandidate)

**Critical Law**:
```
لا U₁₁ قبل RelationAlgebraCore.
No U₁₁ before RelationAlgebraCore.
```

## Purpose (الغرض)

RelationAlgebraCore is NOT a new execution layer.
It is the **algebraic specification** that composition layers MUST obey.

**What it defines**:
1. Identity carriers (Entity, Transformation, Function anchors)
2. Relation invariants (what each relation preserves)
3. Relation operations (NOT enums - actual algebraic operations)
4. Constitutional tests (12 mandatory tests)

**What it prevents**:
- Relations as labels only (FORBIDDEN)
- Identity collapse without license (FORBIDDEN)
- Direct semantic output from relations (FORBIDDEN)
- Direct ifadah output from relations (FORBIDDEN)
- Direct hukm output from relations (FORBIDDEN)

---

## A. Identity Carriers (المحفوظات)

### A.1 EntityAnchor (مرساة الكيان - الجامد)

```python
@dataclass(frozen=True)
class EntityAnchor:
    """
    Stable entity anchor (الجامد - jāmid)

    Constitutional Law:
        Entity identity MUST be preserved through composition.
        Relations add load but NEVER replace entity identity.

    Attributes:
        identity: IdentityType (from IdentityRegistry)
        ontic_type: OnticType (جوهر substance / عرض accident)
        genus_or_individual: GenusType
        reference_status: ReferenceStatus
        preserved_invariant: What must NOT change
        stability: StabilityType
        verified_bearability: Can bear predication?
        trace: Origin trace from U₀→U₁₀
    """
    identity: IdentityType
    ontic_type: 'OnticType'
    genus_or_individual: 'GenusType'
    reference_status: 'ReferenceStatus'
    preserved_invariant: str
    stability: 'StabilityType'
    verified_bearability: bool
    trace: Tuple[str, ...]
```

**Key Principle**: EntityAnchor represents **الجامد** (jāmid) - stable entities that can bear transformations but remain themselves.

---

### A.2 TransformationAnchor (مرساة التحول - المشتق)

```python
@dataclass(frozen=True)
class TransformationAnchor:
    """
    Transformation anchor (المشتق - mushtaq)

    Constitutional Law:
        Transformation MUST trace back to root/pattern from U₈/U₉.
        No transformations without morphological evidence.

    Attributes:
        identity: IdentityType (from IdentityRegistry)
        origin_root_id: str (from U₈ RootStemCandidate)
        pattern_id: str (from U₉ WeightCandidate)
        event_or_attribute: TransformationType
        bearability_requirements: What can bear this?
        valency_requirements: Argument structure
        trace: Origin trace from U₀→U₁₀
    """
    identity: IdentityType
    origin_root_id: str  # from U₈
    pattern_id: str  # from U₉
    event_or_attribute: 'TransformationType'
    bearability_requirements: FrozenSet[str]
    valency_requirements: Optional['ValencySpec']
    trace: Tuple[str, ...]
```

**Key Principle**: TransformationAnchor represents **المشتق** (mushtaq) - derived forms with event/attribute semantics.

---

### A.3 FunctionAnchor (مرساة الوظيفة - المبني)

```python
@dataclass(frozen=True)
class FunctionAnchor:
    """
    Function anchor (المبني - mabnī)

    Constitutional Law:
        Function words are locked (مبني).
        They require scope/anchor/join specifications.

    Attributes:
        identity: IdentityType (CLOSED_CLASS_IDENTITY)
        locked_form: str (frozen surface)
        scope_type: ScopeType (local/clause/sentence)
        attachment_requirements: What it must attach to
        trace: Origin trace from U₀→U₁₀
    """
    identity: IdentityType
    locked_form: str
    scope_type: 'ScopeType'
    attachment_requirements: FrozenSet[str]
    trace: Tuple[str, ...]
```

**Key Principle**: FunctionAnchor represents **المبني** (mabnī) - frozen function words with scope requirements.

---

## B. Relation Invariants (ثوابت العلاقة)

### B.1 RelationIdentityInvariant

```python
@dataclass(frozen=True)
class RelationIdentityInvariant:
    """
    What a relation operation MUST preserve and what it MAY change.

    Constitutional Law:
        Every relation MUST declare:
        1. Input identities (preserved)
        2. Output identities (preserved or extended)
        3. Invariants (what cannot change)
        4. Permitted shifts (what may change under license)
        5. Blocked collapses (forbidden identity mergers)
        6. Residuals (unresolved aspects)

    Attributes:
        relation_type: RelationType (ISNAD, TADMIN, TAQYID, WASF, IDAFAH)
        input_identities: Tuple of input identity types
        output_identities: Tuple of output identity types (must include inputs)
        preserved_invariants: What CANNOT change
        permitted_shifts: What MAY change under license
        blocked_collapses: Forbidden identity absorptions
        residuals: Unresolved aspects requiring evidence
        rank: Rank (CANDIDATE not CERTIFIED)
        evidence: Evidence trace
    """
    relation_type: 'RelationType'
    input_identities: Tuple[IdentityType, ...]
    output_identities: Tuple[IdentityType, ...]
    preserved_invariants: FrozenSet[str]
    permitted_shifts: FrozenSet[str]
    blocked_collapses: FrozenSet[Tuple[IdentityType, IdentityType]]
    residuals: 'ResidualSet'
    rank: 'Rank'
    evidence: Tuple[str, ...]
```

---

## C. Five Core Relation Operations (العلاقات الخمس الأساسية)

### C.1 ISNAD - الإسناد (Predication)

```python
class IsnadOperation(RelationOperation):
    """
    الإسناد - Predication Operation

    Definition:
        Attribution of transformation/state to entity while preserving entity identity.

    Preserves:
        - Entity identity (المسند إليه)
        - Transformation trace (المسند)

    Licenses:
        - Addition of predication load on entity

    Blocks:
        - Collapse of entity into transformation
        - Direct meaning production
        - Direct semantic identity output

    Example:
        الرجل كاتب
        Entity: الرجل (preserved)
        Transformation: كاتب (preserved)
        Relation: ISNAD adds predication load

        NOT:
        - الرجل = فاعل (syntactic role - FORBIDDEN)
        - الرجل = معنى الكتابة (semantic meaning - FORBIDDEN)

    Constitutional Tests:
        - test_isnad_preserves_entity_identity
        - test_isnad_preserves_transformation_trace
        - test_isnad_requires_bearability
        - test_isnad_does_not_emit_semantic_identity
    """

    def apply(self,
              entity: EntityAnchor,
              transformation: TransformationAnchor,
              context: 'CompositionContext') -> 'RelationResult':
        """Apply ISNAD operation preserving both identities."""
        # Implementation verifies:
        # 1. Entity can bear predication
        # 2. Transformation is compatible
        # 3. No semantic identity output
        # 4. Residuals preserved
        pass

    def get_invariant(self) -> RelationIdentityInvariant:
        """Get ISNAD invariant specification."""
        return RelationIdentityInvariant(
            relation_type=RelationType.ISNAD,
            input_identities=(entity.identity, transformation.identity),
            output_identities=(entity.identity, transformation.identity),  # Both preserved
            preserved_invariants=frozenset({'entity_stability', 'transformation_trace'}),
            permitted_shifts=frozenset({'predication_load_addition'}),
            blocked_collapses=frozenset({
                (IdentityType.FORM_IDENTITY, IdentityType.SEMANTIC_IDENTITY),
            }),
            residuals=...,  # Bearability, scope, etc.
            rank=Rank.CANDIDATE,
            evidence=...
        )
```

---

### C.2 TADMIN - التضمين (Embedding/Containment)

```python
class TadminOperation(RelationOperation):
    """
    التضمين - Embedding/Containment Operation

    Definition:
        Relation between container and contained preserving BOTH identities.

    Preserves:
        - Container identity
        - Contained identity
        - Both must survive independently

    Licenses:
        - Containment/specification relation candidate

    Blocks:
        - Container absorbs contained
        - Contained absorbs container
        - Identity merger without residual

    Example:
        الحق عليه
        Container: عليه (preserved)
        Contained: الحق (preserved)
        Relation: TADMIN (containment/location)

        NOT:
        - عليه swallows الحق (FORBIDDEN)
        - الحق swallows عليه (FORBIDDEN)

    Constitutional Tests:
        - test_tadmin_preserves_container_identity
        - test_tadmin_preserves_contained_identity
        - test_tadmin_rejects_identity_absorption
    """

    def apply(self,
              container: Anchor,
              contained: Anchor,
              context: 'CompositionContext') -> 'RelationResult':
        """Apply TADMIN operation preserving both identities."""
        pass
```

---

### C.3 TAQYID - التقييد (Restriction/Modification)

```python
class TaqyidOperation(RelationOperation):
    """
    التقييد - Restriction/Modification Operation

    Definition:
        Restriction of base scope/domain while preserving base identity.

    Preserves:
        - Base identity (الأصل)
        - Restrictor trace (المقيد)

    Licenses:
        - Domain narrowing
        - Scope restriction

    Blocks:
        - Base transformation
        - Forced semantic collapse
        - Judgment from restriction alone

    Example:
        دين إلى أجل مسمى
        Base: دين (preserved)
        Restrictor: إلى أجل مسمى (preserved)
        Relation: TAQYID restricts scope

        NOT:
        - دين becomes أجل (FORBIDDEN)
        - Direct hukm from restriction (FORBIDDEN)

    Residuals:
        - Is the restriction temporal? spatial? conditional?
        - Does restriction change hukm later? (unresolved until evidence)

    Constitutional Tests:
        - test_taqyid_preserves_base_identity
        - test_taqyid_restricts_scope_without_collapsing_base
        - test_taqyid_preserves_restrictor_trace
    """

    def apply(self,
              base: Anchor,
              restrictor: Anchor,
              context: 'CompositionContext') -> 'RelationResult':
        """Apply TAQYID operation preserving base identity."""
        pass
```

---

### C.4 WASF - الوصف (Description/Attribution)

```python
class WasfOperation(RelationOperation):
    """
    الوصف - Description/Attribution Operation

    Definition:
        Attribution of descriptor to described entity, preserving both.

    Preserves:
        - Described entity identity (الموصوف)
        - Descriptor trace (الصفة)

    Licenses:
        - Attribute addition
        - Description load

    Blocks:
        - Descriptor becoming independent entity
        - Judgment from description alone
        - Direct meaning from attribute

    Example:
        تجارة حاضرة
        Described: تجارة (preserved)
        Descriptor: حاضرة (preserved)
        Relation: WASF adds description

        NOT:
        - حاضرة becomes independent meaning (FORBIDDEN)
        - Hukm from "حاضرة" alone (FORBIDDEN)

    Constitutional Tests:
        - test_wasf_preserves_mawsuf_identity
    """

    def apply(self,
              mawsuf: Anchor,
              sifat: Anchor,
              context: 'CompositionContext') -> 'RelationResult':
        """Apply WASF operation preserving described entity."""
        pass
```

---

### C.5 IDAFAH - الإضافة (Attachment/Possession)

```python
class IdafahOperation(RelationOperation):
    """
    الإضافة - Attachment/Possession Operation

    Definition:
        Attachment relation preserving both mudaf and mudaf ilayh.

    Preserves:
        - Attached entity (المضاف)
        - Attachment target (المضاف إليه)

    Licenses:
        - Relation candidate (possession/part/specification)

    Blocks:
        - Forced ownership interpretation
        - Direct meaning before ifadah
        - Identity merger

    Example:
        أجلِه
        Mudaf: أجل (preserved)
        Mudaf ilayh: ـه (preserved)
        Relation: IDAFAH (attachment)

        Residuals:
        - Is this ownership? (unresolved)
        - Is this part-whole? (unresolved)
        - Is this specification? (unresolved)
        - Is this definition? (unresolved)

    Constitutional Tests:
        - test_idafah_preserves_both_identities_without_forcing_ownership
    """

    def apply(self,
              mudaf: Anchor,
              mudaf_ilayh: Anchor,
              context: 'CompositionContext') -> 'RelationResult':
        """Apply IDAFAH operation preserving both identities."""
        pass
```

---

## D. Supporting Type Definitions

```python
class RelationType(Enum):
    """Five core relation types (NOT standalone - used by operations)."""
    ISNAD = auto()      # الإسناد
    TADMIN = auto()     # التضمين
    TAQYID = auto()     # التقييد
    WASF = auto()       # الوصف
    IDAFAH = auto()     # الإضافة


class OnticType(Enum):
    """Ontic classification (what kind of being)."""
    SUBSTANCE = auto()  # جوهر (independent existence)
    ACCIDENT = auto()   # عرض (dependent existence)


class GenusType(Enum):
    """Genus vs individual."""
    GENUS = auto()      # كلي (universal)
    INDIVIDUAL = auto() # جزئي (particular)


class ReferenceStatus(Enum):
    """Reference determination status."""
    DEFINITE = auto()       # معرفة
    INDEFINITE = auto()     # نكرة
    UNRESOLVED = auto()     # غير محسوم


class StabilityType(Enum):
    """Entity stability."""
    STABLE = auto()         # ثابت
    TRANSIENT = auto()      # عارض
    UNRESOLVED = auto()     # غير محسوم


class TransformationType(Enum):
    """Transformation classification."""
    EVENT = auto()          # حدث
    ATTRIBUTE = auto()      # صفة
    STATE = auto()          # حال


class ScopeType(Enum):
    """Function word scope."""
    LOCAL = auto()          # محلي
    CLAUSE = auto()         # جملي
    SENTENCE = auto()       # نصي
```

---

## E. Constitutional Tests (12 Mandatory)

Before ANY U₁₁ implementation, these 12 tests MUST pass:

### E.1 ISNAD Tests (4 tests)

```python
def test_isnad_preserves_entity_identity():
    """الإسناد يحفظ هوية المسند إليه"""
    pass

def test_isnad_preserves_transformation_trace():
    """الإسناد يحفظ أثر المسند"""
    pass

def test_isnad_requires_bearability():
    """الإسناد يتطلب قابلية الحمل"""
    pass

def test_isnad_does_not_emit_semantic_identity():
    """الإسناد لا ينتج هوية دلالية"""
    pass
```

### E.2 TAQYID Tests (3 tests)

```python
def test_taqyid_preserves_base_identity():
    """التقييد يحفظ هوية الأصل"""
    pass

def test_taqyid_restricts_scope_without_collapsing_base():
    """التقييد يضيق النطاق دون انهيار الأصل"""
    pass

def test_taqyid_preserves_restrictor_trace():
    """التقييد يحفظ أثر المقيد"""
    pass
```

### E.3 TADMIN Tests (3 tests)

```python
def test_tadmin_preserves_container_identity():
    """التضمين يحفظ هوية الحاوي"""
    pass

def test_tadmin_preserves_contained_identity():
    """التضمين يحفظ هوية المحتوى"""
    pass

def test_tadmin_rejects_identity_absorption():
    """التضمين يرفض ابتلاع الهوية"""
    pass
```

### E.4 WASF & IDAFAH Tests (2 tests)

```python
def test_wasf_preserves_mawsuf_identity():
    """الوصف يحفظ هوية الموصوف"""
    pass

def test_idafah_preserves_both_identities_without_forcing_ownership():
    """الإضافة تحفظ الطرفين دون إجبار الملك"""
    pass
```

---

## F. Forbidden Outputs (المخرجات الممنوعة)

RelationAlgebraCore operations MUST NOT emit:

1. ❌ **SEMANTIC_IDENTITY** - No meaning determination
2. ❌ **IFADAH_IDENTITY** - No pragmatic closure
3. ❌ **HUKM_IDENTITY** - No epistemic judgment
4. ❌ **FUNCTIONAL_RELATION_IDENTITY** - No final syntactic role

**Permitted outputs**:
- ✅ **RelationCandidate** - Relation structure with preserved identities
- ✅ **Residuals** - Unresolved aspects requiring evidence
- ✅ **Rank.CANDIDATE** - Never CERTIFIED

---

## G. Integration with Execution Layers

### G.1 Relation to U₁₀ (WordFormCandidate)

U₁₀ produces **WordFormCandidates** with:
- WEIGHT_IDENTITY preserved
- FORM_IDENTITY established
- NO semantic output
- NO relation output

### G.2 Relation to Future U₁₁ (PreLexicalWordCandidate)

U₁₁ MUST use RelationAlgebraCore to:
- Classify jāmid/mushtaq/mabnī
- Create EntityAnchor/TransformationAnchor/FunctionAnchor
- Prepare for U₁₂ composition

### G.3 Relation to Future U₁₂ (CompositionCandidate)

U₁₂ MUST use RelationAlgebraCore operations:
- IsnadOperation for predication
- TadminOperation for containment
- TaqyidOperation for restriction
- WasfOperation for description
- IdafahOperation for attachment

---

## H. Summary: Algebra NOT Labels

**The Difference**:

❌ **Labels (FORBIDDEN)**:
```python
class RelationType(Enum):
    ISNAD = auto()
    TADMIN = auto()
    TAQYID = auto()

# Then just tagging:
edge.relation_type = RelationType.ISNAD
```

✅ **Algebra (REQUIRED)**:
```python
class IsnadOperation(RelationOperation):
    def apply(entity, transformation, context):
        # Verify bearability
        # Preserve identities
        # Add predication load
        # Return RelationResult with residuals
        pass

    def get_invariant():
        # Return what is preserved/licensed/blocked
        pass
```

---

## I. Constitutional Law Summary

```
لا U₁₁ قبل RelationAlgebraCore.
No U₁₁ before RelationAlgebraCore.

ولا RelationAlgebraCore قبل حفظ الهوية.
No RelationAlgebraCore before identity preservation.

ولا حفظ هوية بلا ثابت معلن.
No identity preservation without declared invariant.

ولا ثابت بلا اختبار.
No invariant without test.

ولا اختبار بلا بقايا.
No test without residuals.
```

**Final Judgment**:
This appendix defines the **algebraic foundation** that composition layers MUST obey.
It is NOT optional.
It is NOT a convenience.
It is **constitutional law**.

---

**Status**: 📐 Foundation Specification
**Created**: 2026-05-26
**PR**: chore: add RelationAlgebraCore before U₁₁ expansion
