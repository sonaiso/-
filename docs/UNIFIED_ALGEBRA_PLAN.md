# خطة توحيد الجبر الكاملة
# Unified Algebra Plan - Corrective Edition

**Purpose**: Unify existing algebraic achievements into coherent system
**Status**: Phase 1 - Inventory and Mapping
**Created**: 2026-05-27
**Constitutional Authority**: Evidence-indexed Typed Partial Algebra

---

## المبدأ المصحح (Corrective Principle)

**الخطأ السابق**: اقترحتُ خطة كأن المستودع فارغ، محاولًا بناء kernel جديد.

**التصحيح**:
```
لا تبدأ مستودعًا أو خطة جديدة بمحو الموجود.
ابدأ بتوحيد المنجز.
ثم أدخل SlotGeometry كأصل.
ثم اربط U₈/U₉/U₁₀ بما قبله.
ثم أصلح RelationAlgebraCore.
ثم فقط ابنِ RelationClosure وIfadah.
```

**English Translation**:
> Don't start a new repository or plan by erasing what exists.
> Start by unifying achievements.
> Then introduce SlotGeometry as foundation.
> Then connect U₈/U₉/U₁₀ to what came before.
> Then fix RelationAlgebraCore.
> Then only build RelationClosure and Ifadah.

---

## المنجزات الحقيقية (Real Achievements Inventory)

### 1. dal_algebra.py - النواة الموجودة (Existing Kernel)

**File**: `src/dal_core/dal_algebra.py` (400+ lines)

**Core Components**:
```python
# Lines 34-47: DalTransitionDomain (8 layers)
class DalTransitionDomain(Enum):
    D0_GRAPHOPHONEMIC = auto()
    D1_SYLLABIC = auto()
    D2_PRE_MORPH = auto()
    D3_ORIGIN = auto()
    D4_TEMPLATE = auto()
    D5_IDENTITY_AXIS = auto()
    D6_DIRECTIONAL_ANALYSIS = auto()
    D7_JUDGMENT = auto()

# Lines 50-68: DalClaimScope
class DalClaimScope(Enum):
    ATOM_TRANSITION = auto()
    SYLLABLE_FORMATION = auto()
    BOUNDARY_DETECTION = auto()
    MORPHOLOGICAL_ANALYSIS = auto()
    TYPE_INFERENCE = auto()
    FRAME_CONSTRUCTION = auto()
    OPERATOR_APPLICATION = auto()

# Lines 102-122: DalEvidence (span requirement)
@dataclass(frozen=True)
class DalEvidence:
    domain: DalTransitionDomain
    scope: DalClaimScope
    span: tuple[int, int]  # Required
    description: str
    rank: Rank
    trace_ref: Optional[DalTraceRef] = None

# Lines 143-150: DalTraceRef (reversibility)
@dataclass(frozen=True)
class DalTraceRef:
    operation: str
    inputs: tuple
    parameters: dict
    reversible: bool = True
```

**Achievement Status**: ✅ Implemented, exported, used in SyllableCandidate

**Gap**: Not yet promoted as unification kernel for all transitions

---

### 2. D_mufrad Pipeline - مسار الدال المفرد

**Files**:
- `src/dal_core/pipeline.py` (Entry point)
- `src/dal_core/d_form.py` (FormCandidate)
- `src/dal_core/d_lugha.py` (LughaAttestation)
- `src/dal_core/d_type.py` (TypedDal)
- `src/dal_core/d_closed.py` (DClosed)

**Pipeline Flow**:
```
atoms_from_text(text)
    → build_d_form(atoms)         # DForm
    → prove_lugha(form)           # DLugha
    → infer_type(lugha)           # DType
    → close_mufrad(typed)         # DMufrad
```

**Achievement Status**: ✅ Core pipeline functional, exported

**Gap**: Not yet mapped to ExecutionLayer (U₀-U₁₅) or DalTransitionDomain (D0-D7)

---

### 3. MufradProof → PreSyntax Stack

**Files**:
- `src/dal_core/mufrad_proof.py` (MufradProof contract)
- `src/dal_core/presyntax_vector.py` (PreSyntaxMufradVector)
- `src/dal_core/sentence_frame.py` (SentenceFrameCandidate)
- `src/dal_core/case_sign_matrix.py` (CaseSignMatrix)
- `src/dal_core/operator_trigger.py` (OperatorTriggerPotential)
- `src/dal_core/operator_candidate.py` (OperatorCandidate)

**Critical Principle** (from mufrad_proof.py:6-16):
```python
"""
CRITICAL PRINCIPLE:
Before moving to تركيب/syntax, the Arabic singular signifier must be closed
as a جامع مانع مفردي proof object.

Syntax layer works ONLY on MufradProof, not on:
- Raw tokens
- DForm
- DType
- DClosed (basic)

Because: D_mufrad هو أساس أرقام التركيب
"""
```

**Achievement Status**: ✅ Complete stack from MufradProof to OperatorCandidate

**Gap**: Transition governance between these layers not formalized in dal_algebra.py

---

### 4. Syllable Layer - الطبقة المقطعية

**Files**:
- `src/dal_core/syllable_candidate.py` (SyllableCandidate, follows DalCandidateProtocol)
- `src/dal_core/d1_correctness.py` (Corr_D1 validator)
- `src/dal_core/d1_failures.py` (D1FailureSet)
- `src/dal_core/d1_rank_policy.py` (SyllableRankVector)
- `src/dal_core/d1_proof.py` (ProofObject_D1)

**Critical Achievement** (from syllable_candidate.py:1-20):
```python
"""
Syllable Candidate Layer (D1) - PR #30 + PR #32

Domain: SYLLABIC (D1)
Transition: Atom sequence → Syllable candidates
Purpose: Generate syllable structure candidates with boundaries

PR #30: Base syllable candidate generation
PR #32: Integrated D1 certification (Corr_D1 + Failure_D1 + RankPolicy_D1 + ProofObject_D1)

Implements:
- SyllableCandidate class following DalCandidateProtocol
- Syllable candidate generator (atom → syllable transitions)
- Syllable boundary detection
- Evidence-based syllable validation
- Integrated Corr_D1 validation in generation path
- D1FailureSet replacing generic residuals
- SyllableRankVector replacing simple confidence
- ProofObject_D1 for certification
"""
```

**Achievement Status**: ✅ D1 domain fully certified with Corr_D1, Failure_D1, Rank_D1, Proof_D1

**Gap**: SlotGeometry formalization missing (should build ON this, not replace it)

---

### 5. AlgebraicDecisionCore + U₈/U₉/U₁₀

**Files**:
- `src/dal_core/algebraic_decision_core.py` (AlgebraicDecisionCore, 667 lines)
- `src/dal_core/approved_transition_context.py` (ApprovedTransitionContext)
- `src/dal_core/u9_weight_candidate_carrier.py` (U₉ implementation)
- `src/dal_core/u10_word_form_candidate_carrier.py` (U₁₀ implementation)

**8-Dimension Governance** (from algebraic_decision_core.py):
```python
class AlgebraicDecisionCore:
    """
    8-dimension transition governor:
    1. Identity preservation (IdentityRegistry)
    2. Domain boundary (DomainRegistry)
    3. Execution layer order (ExecutionLayerRegistry)
    4. Evidence requirement (EvidenceRequirement)
    5. Claim scope (DalClaimScope)
    6. Shortcut policy (ShortcutPolicy)
    7. Candidate budget (CandidateBudgetPolicy)
    8. Transition contract (DalTransitionContract)
    """
```

**Achievement Status**: ✅ Core governance operational, U₉ fully implemented

**Gap**: U₉→U₁₀ transition has paradox (verify_no_forbidden_leap rejects by default but U₁₀ requires ApprovedTransitionContext from same core)

---

### 6. RelationAlgebraCore (نواة جبر العلاقات)

**File**: `src/dal_core/relation_algebra_core.py` (690 lines)

**Critical Law** (from relation_algebra_core.py:10-11):
```python
"""
Critical Law:
    لا U₁₁ قبل RelationAlgebraCore.
    No U₁₁ before RelationAlgebraCore.
"""
```

**Five Relation Types** (lines 55-67):
```python
class RelationType(Enum):
    ISNAD = auto()      # الإسناد - Predication
    TADMIN = auto()     # التضمين - Embedding/Containment
    TAQYID = auto()     # التقييد - Restriction/Modification
    WASF = auto()       # الوصف - Description/Attribution
    IDAFAH = auto()     # الإضافة - Attachment/Possession
```

**Achievement Status**: ✅ Foundation defined with carrier types (Entity, Transformation, Function)

**Gaps Identified**:
1. EntityAnchor/TransformationAnchor/FunctionAnchor lack `anchor_id` field
2. RelationResult has `preserved_identities` (types) but no `preserved_anchor_ids`
3. Operations raise ValueError instead of returning OperationFailure
4. `added_loads` is `FrozenSet[str]` not typed RelationLoad objects

---

### 7. Execution Layer Registry (سجل الطبقات التنفيذية)

**File**: `src/dal_core/execution_layer_registry.py` (410 lines)

**Canonical Order** (lines 8-28):
```
Execution Core (U₀-U₉): Closed, implemented, operational layers
    U₀ Unicode          → U₁ Grapheme
    U₁ Grapheme         → U₂p PhoneticProjection
    U₂p PhoneticProjection → U₂s ArabicSyllable
    U₂s ArabicSyllable  → U₃ BoundaryAndAttachment
    U₃ BoundaryAndAttachment → U₄ TrueSingularLafẓ
    U₄ TrueSingularLafẓ → U₅ FunctionalRole
    U₅ FunctionalRole   → U₆ MabniClosedClass
    U₆ MabniClosedClass → U₇-A PreWeightContract
    U₇-A PreWeightContract → U₇-B WordSurfaceGuard
    U₇-B WordSurfaceGuard → U₇-C ClauseSurfaceAgreementContract
    U₇-C ClauseSurfaceAgreementContract → U₈ RootStem
    U₈ RootStem         → U₉ Weight

Design Layers (U₁₀-U₁₅): Future design, not closed execution layers
    U₁₀ WordForm
    U₁₁ RelationComposition
    U₁₂ Ifadah
    U₁₃ Hukm
    U₁₄ SentenceStructure
    U₁₅ Dalālah
```

**Achievement Status**: ✅ U₀-U₉ defined, U₇ split into 3 phases (U₇-A, U₇-B, U₇-C)

**Gap**: U₇ defined but not yet extended to PrePathContract as required

---

### 8. Domain Registry (سجل النطاقات)

**File**: `src/dal_core/domain_registry.py` (725 lines)

**20+ Domains Defined**:
```python
class DomainType(Enum):
    # Phonological
    PHONEME_DOMAIN = auto()
    SYLLABLE_DOMAIN = auto()

    # Morphological
    ROOT_DOMAIN = auto()
    PATTERN_DOMAIN = auto()
    STEM_DOMAIN = auto()
    WEIGHT_DOMAIN = auto()  # ✅ Exists

    # Surface
    SOURCE_FORM_DOMAIN = auto()
    ATTRIBUTE_FORM_DOMAIN = auto()
    FUNCTIONAL_FORM_DOMAIN = auto()

    # Syntactic
    RELATION_DOMAIN = auto()
    OPERATOR_DOMAIN = auto()

    # ... (more domains)
```

**Gap Identified**: WORDFORM_DOMAIN referenced in U₁₀ but doesn't exist in enum

---

### 9. Identity Registry (سجل الهويات)

**File**: `src/dal_core/identity_registry.py` (676 lines)

**30+ Identity Types Defined**

**Critical Bug** (lines 346-357):
```python
IdentityType.WEIGHT_IDENTITY: IdentitySpec(
    layer=IdentityLayer.MORPHOLOGICAL_WEIGHT,
    requires=frozenset({
        IdentityType.ROOT_MATERIAL_IDENTITY,  # ❌ Both required
        IdentityType.STEM_IDENTITY            # ❌ AND logic
    }),
    # ...
)
```

**Bug**: Uses AND logic requiring both ROOT_MATERIAL_IDENTITY and STEM_IDENTITY simultaneously
**Expected**: Should be ONE-OF (OR logic) since weight can be determined from either root OR stem

---

## خريطة التوحيد (Unification Map)

### Map 1: DalTransitionDomain ↔ DomainType ↔ ExecutionLayer

| DalTransitionDomain | DomainType | ExecutionLayer | Implementation Status |
|---------------------|------------|----------------|----------------------|
| D0_GRAPHOPHONEMIC | PHONEME_DOMAIN | U₀ Unicode → U₁ Grapheme | ✅ Implemented |
| D1_SYLLABIC | SYLLABLE_DOMAIN | U₂s ArabicSyllable | ✅ Implemented (SyllableCandidate) |
| D2_PRE_MORPH | ? | U₃ BoundaryAndAttachment | ⚠️ Mapping unclear |
| D3_ORIGIN | ROOT_DOMAIN | U₈ RootStem | ✅ Implemented |
| D4_TEMPLATE | PATTERN_DOMAIN, WEIGHT_DOMAIN | U₉ Weight | ✅ Implemented |
| D5_IDENTITY_AXIS | ? | ? | ❌ Not mapped |
| D6_DIRECTIONAL_ANALYSIS | ? | ? | ❌ Not mapped |
| D7_JUDGMENT | ? | ? | ❌ Not mapped |

**Critical Gap**: D2-D7 domains not clearly mapped to ExecutionLayer or DomainType

---

### Map 2: D_mufrad Pipeline ↔ Execution Layers

| Pipeline Stage | Output Type | Corresponding ExecutionLayer | Gap |
|----------------|-------------|------------------------------|-----|
| atoms_from_text | List[ArabicAtom] | U₀ Unicode | ✅ Clear |
| build_d_form | DForm (FormCandidate) | U₁ Grapheme? | ⚠️ Mapping unclear |
| prove_lugha | DLugha (LughaAttestation) | ? | ❌ Not mapped |
| infer_type | DType (TypedDal) | U₅ FunctionalRole? | ⚠️ Tentative |
| close_mufrad | DMufrad | ? | ❌ Not mapped |

**Critical Gap**: D_mufrad pipeline stages don't align clearly with ExecutionLayer sequence

---

### Map 3: MufradProof → PreSyntax Stack

| Component | Purpose | ExecutionLayer | Dal Domain | Status |
|-----------|---------|----------------|------------|--------|
| MufradProof | Closed singular proof | ? | ? | ✅ Implemented |
| PreSyntaxMufradVector | Operator interface | ? | ? | ✅ Implemented |
| SentenceFrameCandidate | Frame hypothesis | ? | ? | ✅ Implemented |
| CaseSignMatrix | Case potential matrix | ? | ? | ✅ Implemented |
| OperatorTriggerPotential | Operator activation | ? | ? | ✅ Implemented |
| OperatorCandidate | Operator application | ? | OPERATOR_DOMAIN | ✅ Implemented |

**Critical Gap**: Entire PreSyntax stack not mapped to ExecutionLayer or DalTransitionDomain

---

## الأخطاء البنيوية المحددة (Identified Structural Bugs)

### Bug 1: U₉→U₁₀ Transition Paradox

**Location**: `src/dal_core/algebraic_decision_core.py:389`

**Problem**:
```python
def verify_no_forbidden_leap(self, ...):
    # Line 389: Calls is_transition_allowed WITHOUT include_design=True
    allowed = self.execution_layer_registry.is_transition_allowed(
        from_layer=from_layer,
        to_layer=to_layer
        # Missing: include_design=True
    )
```

**Impact**: U₉→U₁₀ transition rejected by default because U₁₀ is DESIGN_LAYER, but U₁₀ requires ApprovedTransitionContext from this same core.

**Fix Required**: Add `include_design` parameter to AlgebraicDecisionCore.verify_no_forbidden_leap()

---

### Bug 2: WEIGHT_IDENTITY AND Logic

**Location**: `src/dal_core/identity_registry.py:346-357`

**Problem**:
```python
IdentityType.WEIGHT_IDENTITY: IdentitySpec(
    requires=frozenset({
        IdentityType.ROOT_MATERIAL_IDENTITY,  # Both required (AND)
        IdentityType.STEM_IDENTITY
    })
)
```

**Impact**: Weight identity requires BOTH root AND stem simultaneously, when it should be ONE-OF (weight can be determined from either)

**Fix Required**: Change to ONE-OF logic or add `requires_any_of` field

---

### Bug 3: WORDFORM_DOMAIN Missing

**Location**: `src/dal_core/u10_word_form_candidate_carrier.py` references WORDFORM_DOMAIN
**Location**: `src/dal_core/domain_registry.py` (missing from enum)

**Problem**: U₁₀ assumes WORDFORM_DOMAIN exists but it's not in DomainType enum

**Fix Required**: Add WORDFORM_DOMAIN to DomainType enum

---

### Bug 4: No anchor_id in Relation Anchors

**Location**: `src/dal_core/relation_algebra_core.py:113-198`

**Problem**:
```python
@dataclass(frozen=True)
class EntityAnchor:
    identity_type: IdentityType
    ontic_type: OnticType
    # ❌ Missing: anchor_id field
```

**Impact**: Instance collapse - cannot distinguish between two entity instances with same type

**Fix Required**: Add `anchor_id: str` field to EntityAnchor, TransformationAnchor, FunctionAnchor

---

### Bug 5: String Loads

**Location**: `src/dal_core/relation_algebra_core.py:285`

**Problem**:
```python
@dataclass(frozen=True)
class RelationResult:
    added_loads: FrozenSet[str]  # ❌ Strings, not typed objects
```

**Impact**: No type safety, cannot validate load compatibility

**Fix Required**: Define RelationLoad dataclass, change to `FrozenSet[RelationLoad]`

---

### Bug 6: Exception vs Failure

**Location**: `src/dal_core/relation_algebra_core.py:404-419`

**Problem**:
```python
def validate_isnad_requirements(...):
    if not self._has_required_identities(...):
        raise ValueError("Missing required identities")  # ❌ Exception
```

**Impact**: Violates algebraic closure - operations should return OperationFailure, not raise exceptions

**Fix Required**: Return `OperationFailure` object instead of raising ValueError

---

## النقص في المكونات (Missing Components)

### Missing 1: SlotGeometry Formalization

**Location**: Should be in `src/dal_core/slot_geometry.py` (doesn't exist)

**Purpose**: Formalize slot algebra OVER existing syllable layer

**Required Components**:
```python
@dataclass(frozen=True)
class SlotAtom:
    """Atomic slot unit (C or V)"""
    kind: SlotKind  # CONSONANT or VOWEL
    position: int

@dataclass(frozen=True)
class EmptySlot:
    """Unfilled slot requiring filler"""
    atom: SlotAtom
    constraints: FrozenSet[SlotConstraint]

@dataclass(frozen=True)
class FillCandidate:
    """Candidate to fill empty slot"""
    slot: EmptySlot
    filler: ArabicAtom
    evidence: List[DalEvidence]

@dataclass(frozen=True)
class FilledSlot:
    """Filled slot with evidence"""
    slot: EmptySlot
    filler: ArabicAtom
    fill_evidence: DalEvidence
```

**Constitutional Principle**:
```
SlotGeometry = foundation UNDER D_form, NOT replacement
D_form = SlotGeometry + surface realization
```

---

### Missing 2: U₇ Extension to PrePathContract

**Location**: `src/dal_core/u7_pre_weight_contract_carrier.py` exists but incomplete

**Required Addition**: PrePathContract

**Purpose**: Ensure pathability evidence exists before U₈ (root extraction)

**Required Components**:
```python
@dataclass(frozen=True)
class PathabilityEvidence:
    """Evidence that root path is discoverable"""
    stem_form: str
    pattern_hypothesis: str
    boundary_evidence: List[DalEvidence]

@dataclass(frozen=True)
class PrePathContract:
    """Contract guaranteeing pathability before U₈"""
    surface_contract: PreWeightContract
    pathability: PathabilityEvidence
    rank: Rank
    failures: FailureSet
```

---

### Missing 3: Unified AlgebraicFailure Object

**Location**: Should be in `src/dal_core/dal_algebra.py`

**Purpose**: Replace exception-based errors with algebraic failure objects

**Required**:
```python
@dataclass(frozen=True)
class AlgebraicFailure:
    """Unified failure object for all algebraic operations"""
    operation: str
    domain: DalTransitionDomain
    reason: str
    evidence: List[DalCounterEvidence]
    recoverable: bool
    recovery_suggestion: Optional[str] = None
```

---

### Missing 4: AnchorId and IdentityPair

**Location**: Should be in `src/dal_core/dal_algebra.py`

**Purpose**: Enable instance-level identity preservation

**Required**:
```python
@dataclass(frozen=True)
class AnchorId:
    """Unique identifier for anchor instance"""
    id: str
    domain: DalTransitionDomain
    created_at: str  # ISO timestamp

@dataclass(frozen=True)
class IdentityPair:
    """Pair of identity type and instance anchor"""
    identity_type: IdentityType
    anchor_id: AnchorId
```

---

### Missing 5: MinimalSufficiencyCheck

**Location**: Should be in `src/dal_core/dal_algebra.py`

**Purpose**: Validate Minimal Sufficient License (MSL) for transitions

**Required**:
```python
@dataclass(frozen=True)
class MinimalSufficiencyCheck:
    """Check if transition has minimal sufficient evidence"""
    transition: DalTransitionContract
    required_evidence: FrozenSet[DalClaimScope]
    provided_evidence: FrozenSet[DalEvidence]
    is_sufficient: bool
    missing_evidence: FrozenSet[DalClaimScope]
```

---

### Missing 6: RelationClosure

**Location**: Should be in `src/dal_core/relation_closure.py` (doesn't exist)

**Purpose**: Compose relations with identity preservation proof

**Required**:
```python
@dataclass(frozen=True)
class RelationClosure:
    """Closed composition of relations with identity proof"""
    relations: Tuple[RelationCandidate, ...]
    preserved_identities: FrozenSet[IdentityPair]  # NOT just types
    added_loads: FrozenSet[RelationLoad]
    rank: Rank
    proof: CompositionProof

def compose_relations(
    r1: RelationCandidate,
    r2: RelationCandidate
) -> RelationClosure | AlgebraicFailure:
    """Compose two relations with identity preservation"""
    # Returns closure OR failure, never raises exception
```

---

### Missing 7: IfadahCandidate

**Location**: Should be in `src/dal_core/ifadah_candidate.py` (doesn't exist)

**Purpose**: U₁₂ Ifadah layer - compositional benefit without semantic meaning

**Required**:
```python
@dataclass(frozen=True)
class IfadahCandidate:
    """Compositional benefit (إفادة) without meaning (معنى)"""
    relation_closure: RelationClosure
    benefit_type: BenefitType  # INFORMATIVE, DIRECTIVE, EXPRESSIVE
    completeness: CompletenessType  # COMPLETE, INCOMPLETE
    rank: Rank
    failures: FailureSet
```

**Critical Distinction**:
```
Ifadah (إفادة) = compositional benefit (what composition achieves)
Meaning (معنى) = semantic content (forbidden in dal_core)
```

---

## خطة الإصلاح (11-PR Repair Plan)

### PR-1: Inventory + Mapping Document ✅ THIS DOCUMENT

**Purpose**: Complete inventory and mapping of existing achievements

**Deliverables**:
1. ✅ Inventory of 9 existing achievement categories
2. ✅ 3 unification maps (Domain/Layer/Pipeline)
3. ✅ 6 identified structural bugs
4. ✅ 7 missing components
5. ✅ Corrective principle established

**Status**: COMPLETE (this document)

---

### PR-2: Promote dal_algebra.py as Unified Kernel

**Purpose**: Extend dal_algebra.py to become unification kernel for all transitions

**Changes to**: `src/dal_core/dal_algebra.py`

**Add**:
1. AlgebraicFailure object (replacing exceptions)
2. AnchorId and IdentityPair (instance-level identity)
3. MinimalSufficiencyCheck (MSL validation)
4. TypedTransitionResult = CandidateSet | AlgebraicFailure

**Update**:
1. DalCandidateProtocol to require failures: FailureSet (not residuals)
2. DalCandidateSetProtocol to require rank_vector (not confidence)
3. DalTransitionProtocol to return TypedTransitionResult

**Tests**:
1. test_algebraic_failure_construction.py
2. test_anchor_id_uniqueness.py
3. test_identity_pair_preservation.py
4. test_minimal_sufficiency_check.py

**Constitutional Authority**: Evidence-indexed Typed Partial Algebra Article 1

---

### PR-3: Formalize SlotGeometry Over Syllable Layer

**Purpose**: Build SlotGeometry as foundation UNDER D_form, not replacing syllable layer

**New File**: `src/dal_core/slot_geometry.py`

**Components**:
1. SlotAtom (atomic C/V unit)
2. EmptySlot (unfilled slot)
3. FillCandidate (candidate to fill slot)
4. FilledSlot (filled slot with evidence)
5. SlotComposition (composition of filled slots)

**Integration**:
1. Update `d_form.py` to use SlotGeometry
2. Update `syllable_candidate.py` to expose slot structure
3. Update `d1_correctness.py` to validate slot filling

**Tests**:
1. test_slot_atom_construction.py
2. test_empty_slot_constraints.py
3. test_fill_candidate_validation.py
4. test_filled_slot_evidence.py
5. test_slot_composition_closure.py

**Critical Principle**:
```
D_form = SlotGeometry + SurfaceRealization
SyllableCandidate builds ON SlotGeometry
NOT: SlotGeometry replaces SyllableCandidate
```

---

### PR-4: Extend U₇ to PrePathContract

**Purpose**: Ensure pathability evidence exists before U₈ (root extraction)

**Changes to**: `src/dal_core/u7_pre_weight_contract_carrier.py`

**Add**:
1. PathabilityEvidence dataclass
2. PrePathContract dataclass
3. validate_pathability() function
4. extend_to_prepath_contract() function

**Update**:
1. PreWeightContract to include pathability check
2. U₇→U₈ transition to require PrePathContract

**Tests**:
1. test_pathability_evidence.py
2. test_prepath_contract_validation.py
3. test_u7_to_u8_requires_pathability.py

---

### PR-5: U₈ RootStem Pathability Dependency

**Purpose**: Make U₈ depend on pathability evidence from U₇

**Changes to**: `src/dal_core/u8_root_stem_carrier.py`

**Update**:
1. RootStemCarrier to require PrePathContract input
2. Root extraction to validate pathability before proceeding
3. Return AlgebraicFailure if pathability insufficient

**Tests**:
1. test_u8_requires_prepath_contract.py
2. test_u8_validates_pathability.py
3. test_u8_fails_without_pathability.py

---

### PR-6: U₉ Weight Pathability Dependency

**Purpose**: Make U₉ depend on pathability evidence from U₇ and U₈

**Changes to**: `src/dal_core/u9_weight_candidate_carrier.py`

**Update**:
1. WeightCandidateCarrier to validate pathability chain
2. Pattern matching to require stem evidence from U₈
3. Return AlgebraicFailure if evidence chain broken

**Tests**:
1. test_u9_validates_pathability_chain.py
2. test_u9_requires_u8_stem_evidence.py
3. test_u9_fails_without_evidence_chain.py

---

### PR-7: U₁₀ WordForm Pathability Dependency + Fix Paradox

**Purpose**: Make U₁₀ depend on pathability and fix U₉→U₁₀ transition paradox

**Changes to**:
1. `src/dal_core/u10_word_form_candidate_carrier.py`
2. `src/dal_core/algebraic_decision_core.py`
3. `src/dal_core/domain_registry.py`

**Fixes**:
1. Add WORDFORM_DOMAIN to DomainType enum
2. Add `include_design` parameter to verify_no_forbidden_leap()
3. WordFormCandidate to validate full pathability chain

**Tests**:
1. test_wordform_domain_exists.py
2. test_u9_to_u10_transition_allowed.py
3. test_u10_validates_full_pathability_chain.py

---

### PR-8: PreSyntax Transition Governance

**Purpose**: Formalize transitions in PreSyntax stack under dal_algebra.py

**Changes to**:
1. `src/dal_core/mufrad_proof.py`
2. `src/dal_core/presyntax_vector.py`
3. `src/dal_core/sentence_frame.py`
4. `src/dal_core/case_sign_matrix.py`
5. `src/dal_core/operator_trigger.py`
6. `src/dal_core/operator_candidate.py`

**Add to each**:
1. DalTransitionContract specification
2. Evidence requirements
3. Failure handling (not exceptions)
4. Rank validation

**Map**:
1. MufradProof → PreSyntaxVector: Which DalTransitionDomain?
2. PreSyntax → SentenceFrame: Which domain?
3. Frame → CaseSignMatrix: Which domain?
4. Matrix → OperatorTrigger: Which domain?
5. Trigger → OperatorCandidate: OPERATOR_DOMAIN ✅

---

### PR-9: Fix RelationAlgebraCore Instance Identity

**Purpose**: Fix 4 bugs in RelationAlgebraCore

**Changes to**: `src/dal_core/relation_algebra_core.py`

**Fixes**:
1. Add `anchor_id: AnchorId` to EntityAnchor, TransformationAnchor, FunctionAnchor
2. Add `preserved_anchor_ids: FrozenSet[AnchorId]` to RelationResult
3. Define RelationLoad dataclass, change `added_loads: FrozenSet[RelationLoad]`
4. Replace ValueError raises with return AlgebraicFailure

**Tests**:
1. test_anchor_has_anchor_id.py
2. test_relation_preserves_anchor_ids.py
3. test_relation_loads_typed.py
4. test_relation_returns_failure_not_exception.py

---

### PR-10: Add RelationClosure

**Purpose**: Add relation composition with identity preservation proof

**New File**: `src/dal_core/relation_closure.py`

**Components**:
1. CompositionProof dataclass
2. RelationClosure dataclass
3. compose_relations() function
4. validate_composition_identity_preservation()

**Critical Law**:
```python
def compose_relations(
    r1: RelationCandidate,
    r2: RelationCandidate
) -> RelationClosure | AlgebraicFailure:
    """
    Compose two relations with identity preservation.

    Returns:
        RelationClosure if identity preserved
        AlgebraicFailure if composition violates identity

    NEVER raises exception.
    """
```

**Tests**:
1. test_relation_composition_preserves_identity.py
2. test_relation_composition_accumulates_loads.py
3. test_relation_composition_fails_on_identity_violation.py
4. test_compose_returns_failure_not_exception.py

---

### PR-11: Add IfadahCandidate (U₁₂)

**Purpose**: Add compositional benefit layer (إفادة) without semantic meaning

**New File**: `src/dal_core/ifadah_candidate.py`

**Components**:
1. BenefitType enum (INFORMATIVE, DIRECTIVE, EXPRESSIVE)
2. CompletenessType enum (COMPLETE, INCOMPLETE)
3. IfadahCandidate dataclass
4. compute_ifadah() function

**Critical Distinction**:
```python
"""
Ifadah (إفادة) vs Meaning (معنى)

Ifadah = Compositional benefit
- What composition achieves structurally
- Observable from form and relations
- PERMITTED in dal_core

Meaning (معنى) = Semantic content
- What speaker intends
- Not observable from form alone
- FORBIDDEN in dal_core

Example:
    "كتب الطالب" (The student wrote)

    Ifadah: INFORMATIVE + COMPLETE
    - Predication relation (ISNAD) is complete
    - Composition provides informative benefit
    - Observable from grammar

    Meaning: ???
    - What was written? (Unknown)
    - Why? (Unknown)
    - When? (Unknown)
    - Requires context/world knowledge
    - FORBIDDEN here
"""
```

**Tests**:
1. test_ifadah_from_relation_closure.py
2. test_ifadah_benefit_type_classification.py
3. test_ifadah_completeness_detection.py
4. test_ifadah_no_semantic_meaning.py

---

## المبادئ الدستورية (Constitutional Principles)

### Principle 1: Evidence-Indexed Identity Preservation

```
For all operations f: A → B in the algebra:
    Idₑ(f(a)) = Idₑ(a)

Where:
    Idₑ = Evidence-indexed identity function
    e = Evidence set supporting identity claim
```

**Implementation**: Every transition must preserve `anchor_id` and provide evidence

---

### Principle 2: Algebraic Closure (No Exceptions)

```
All operations return values in the algebra:
    f: A → B  (where B = CandidateSet | AlgebraicFailure)

NEVER:
    f: A → B  (where f can raise Exception)
```

**Implementation**: Replace all ValueError/RuntimeError with AlgebraicFailure returns

---

### Principle 3: Evidence Requirement

```
No transition without evidence:
    transition: (X, Evidence) → Y | Failure

NOT:
    transition: X → Y
```

**Implementation**: DalTransitionContract requires evidence set

---

### Principle 4: Layer Order (No Jumps)

```
Forbidden transitions:
    U₂s → U₅  (skips U₃, U₄)
    U₂s → U₈  (skips 6 layers)
    U₈ → U₁₂ (skips U₉, U₁₀, U₁₁)
```

**Implementation**: ExecutionLayerRegistry.validate_transition_order()

---

### Principle 5: Domain Separation

```
Each layer has exactly one domain:
    U₂s ↔ SYLLABLE_DOMAIN
    U₈ ↔ ROOT_DOMAIN
    U₉ ↔ WEIGHT_DOMAIN
    U₁₀ ↔ WORDFORM_DOMAIN
```

**Implementation**: DomainRegistry.verify_domain_boundary()

---

### Principle 6: Minimal Sufficient License (MSL)

```
For transition X → Y to be licensed:
    Evidence(X → Y) ≥ MSL(X → Y)

Where MSL is minimal evidence set sufficient for transition.
```

**Implementation**: MinimalSufficiencyCheck validation

---

### Principle 7: Rank Monotonicity

```
Composition never raises rank:
    rank(compose(a, b)) ≤ min(rank(a), rank(b))
```

**Implementation**: Rank algebra in dal_algebra.py

---

### Principle 8: Failure Semantics

```
Failures are values, not control flow:
    Result = Success(value) | Failure(reason, evidence)

NOT:
    try { value } catch { error }
```

**Implementation**: AlgebraicFailure as first-class value

---

## ترتيب التنفيذ (Execution Order)

### Phase 1: Foundation (PR-1, PR-2, PR-3)

**Week 1**:
- ✅ PR-1: This inventory document (COMPLETE)
- PR-2: Promote dal_algebra.py as kernel
- PR-3: Formalize SlotGeometry

**Goal**: Establish unified algebraic foundation

---

### Phase 2: Pathability Chain (PR-4, PR-5, PR-6, PR-7)

**Week 2-3**:
- PR-4: Extend U₇ to PrePathContract
- PR-5: U₈ pathability dependency
- PR-6: U₉ pathability dependency
- PR-7: U₁₀ pathability + fix paradox

**Goal**: Connect U₇ → U₈ → U₉ → U₁₀ with evidence chain

---

### Phase 3: Syntax Governance (PR-8, PR-9)

**Week 4**:
- PR-8: PreSyntax transition governance
- PR-9: Fix RelationAlgebraCore bugs

**Goal**: Formalize PreSyntax stack and fix relation algebra

---

### Phase 4: Composition Closure (PR-10, PR-11)

**Week 5**:
- PR-10: Add RelationClosure
- PR-11: Add IfadahCandidate

**Goal**: Complete compositional layers with closure proof

---

## معايير النجاح (Success Criteria)

### Criterion 1: All 6 Bugs Fixed

- [ ] U₉→U₁₀ transition paradox resolved
- [ ] WEIGHT_IDENTITY uses ONE-OF logic
- [ ] WORDFORM_DOMAIN exists in enum
- [ ] Relation anchors have anchor_id
- [ ] Relation loads are typed objects
- [ ] No exceptions, only AlgebraicFailure

---

### Criterion 2: All 7 Missing Components Added

- [ ] SlotGeometry formalized
- [ ] U₇ extended to PrePathContract
- [ ] AlgebraicFailure object exists
- [ ] AnchorId and IdentityPair exist
- [ ] MinimalSufficiencyCheck exists
- [ ] RelationClosure exists
- [ ] IfadahCandidate exists

---

### Criterion 3: Complete Mapping

- [ ] DalTransitionDomain ↔ DomainType ↔ ExecutionLayer mapped
- [ ] D_mufrad pipeline mapped to ExecutionLayer
- [ ] PreSyntax stack mapped to DalTransitionDomain

---

### Criterion 4: All Tests Pass

- [ ] 100% test coverage for dal_algebra.py
- [ ] All pathability chain tests pass
- [ ] All PreSyntax governance tests pass
- [ ] All relation algebra tests pass

---

### Criterion 5: Documentation Complete

- [ ] UNIFIED_ALGEBRA_PLAN.md (this document) ✅
- [ ] SLOT_GEOMETRY_CONSTITUTION.md
- [ ] PATHABILITY_EVIDENCE_SPEC.md
- [ ] RELATION_CLOSURE_PROOF.md
- [ ] IFADAH_VS_MEANING_DISTINCTION.md

---

## الخلاصة (Summary)

### What We Have ✅

1. **dal_algebra.py**: Existing transition signature foundation (400+ lines)
2. **D_mufrad Pipeline**: Functional pipeline (atoms → DMufrad)
3. **MufradProof → PreSyntax Stack**: Complete 6-layer stack
4. **Syllable Layer**: Fully certified D1 with Corr_D1, Failure_D1, Rank_D1, Proof_D1
5. **AlgebraicDecisionCore**: 8-dimension governance operational
6. **U₉ Implementation**: Fully functional weight candidate carrier
7. **RelationAlgebraCore**: Foundation with 5 relation types
8. **ExecutionLayer Registry**: U₀-U₁₅ canonical order
9. **Domain + Identity Registries**: 20+ domains, 30+ identities

### What We Need ❌

1. **SlotGeometry**: Formalization OVER syllable layer
2. **U₇ Extension**: PrePathContract for pathability
3. **Pathability Chain**: U₇ → U₈ → U₉ → U₁₀ evidence dependency
4. **PreSyntax Governance**: Transition contracts for MufradProof → OperatorCandidate
5. **RelationAlgebraCore Fixes**: anchor_id, typed loads, no exceptions
6. **RelationClosure**: Composition with identity proof
7. **IfadahCandidate**: U₁₂ compositional benefit layer

### How We Fix It 🔧

**11-PR Corrective Plan**:
1. PR-1: Inventory + Mapping ✅ (this document)
2. PR-2: Promote dal_algebra.py as kernel
3. PR-3: Formalize SlotGeometry
4. PR-4 to PR-7: Build pathability chain
5. PR-8: Govern PreSyntax transitions
6. PR-9: Fix RelationAlgebraCore
7. PR-10: Add RelationClosure
8. PR-11: Add IfadahCandidate

### Constitutional Authority 📜

All work governed by:
- Evidence-indexed Typed Partial Algebra
- Identity preservation (Idₑ(a) = a)
- Algebraic closure (no exceptions)
- Evidence requirement (no transition without evidence)
- Layer order (no jumps)
- Minimal Sufficient License (MSL)

---

**Document Status**: Phase 1 Complete
**Next Step**: PR-2 (Promote dal_algebra.py as unified kernel)
**Created**: 2026-05-27
**Author**: Algebraic Decision Core Team

