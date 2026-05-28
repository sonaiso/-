## Relation Slot Readiness Constitution
# دستور جاهزية خانات النسبة

**Created**: 2026-05-28
**Status**: CONSTITUTIONAL FOUNDATION
**Authority**: Immutable architectural constraint before U₁₁

---

## Constitutional Declaration

```
RelationSlotReadiness is a bridge layer between PreSyntaxMufradVector
and RelationAlgebraCore.

It PRESERVES all PreSyntaxMufradVector identities.
It PREPARES relation slots but does NOT create final relations.
It does NOT produce meaning, ifadah, or hukm.

جاهزية خانات النسبة هي طبقة جسرية بين شعاع المفرد وجبر العلاقات.
تحفظ كل هويات شعاع المفرد.
تُهيِّئ خانات النسبة ولا تنتج علاقات نهائية.
ولا تنتج معنى ولا إفادة ولا حكم.
```

---

## Article 1: Fundamental Purpose

### 1.1 Architectural Position

```
PreSyntaxMufradVector (شعاع المفرد قبل التركيب)
    ↓
RelationSlotReadiness (جاهزية خانات النسبة) ← THIS MODULE
    ↓
RelationAlgebraCore (نواة جبر العلاقات)
    ↓
RelationCandidate (مرشح العلاقة)
    ↓
STOP before Ifadah/Hukm
```

### 1.2 What This Layer Does

**Permitted:**
- ✅ Consume composition-ready PreSyntaxMufradVector
- ✅ Prepare slot geometries for three frame types:
  - Nominal sentence (الجملة الاسمية)
  - Verbal sentence (الجملة الفعلية)
  - Semi-sentence (شبه الجملة)
- ✅ Preserve all input trace_ids
- ✅ Identify relation type potential (ISNAD/TADMIN/TAQYID/WASF/IDAFAH)
- ✅ Pass readiness to RelationAlgebraCore

**Forbidden:**
- ❌ Create final relations (only RelationAlgebraCore does this)
- ❌ Produce meaning, semantic, madlul, murad
- ❌ Produce ifadah, pragmatic completion
- ❌ Produce hukm, judgment
- ❌ Consume raw strings or tokens
- ❌ Delete or modify input PreSyntaxMufradVector

### 1.3 Why This Layer Exists

**Problem Solved:**
Without this layer, we risk:
- Jumping from PreSyntaxMufradVector → RelationCandidate (too fast)
- Jumping from PreSyntaxMufradVector → Meaning (forbidden)
- Losing trace_id preservation
- Mixing frame types without preparation

**Solution:**
This layer enforces:
- Explicit frame type classification (nominal/verbal/semi)
- Slot geometry preparation
- Trace preservation
- Readiness verification before RelationAlgebraCore

---

## Article 2: The Ten Constitutional Laws

### Law 1: No RelationSlotVector without PreSyntaxMufradVector

```
لا RelationSlotVector بلا PreSyntaxMufradVector
```

**Enforcement:**
```python
if not isinstance(input_vector, PreSyntaxMufradVector):
    raise ValueError("Must be PreSyntaxMufradVector")
```

**Test:** `test_relation_slot_readiness_rejects_raw_string`

---

### Law 2: No consumption without composition_readiness

```
لا استهلاك لمن لا يسمح composition_readiness باستهلاكه
```

**Enforcement:**
```python
if not vector.allows_operator_consumption():
    raise ValueError("Vector not ready for composition")
```

**Test:** `test_relation_slot_readiness_rejects_unready_presyntax_vector`

---

### Law 3: No deletion of mufrad vector traces

```
لا حذف لشعاع المفرد؛ يجب حفظ trace_id لكل مدخل
```

**Enforcement:**
```python
if self.preserved_trace_ids != tuple(v.trace_id for v in self.input_vectors):
    raise ValueError("Trace IDs must be preserved")
```

**Test:** `test_relation_slot_readiness_preserves_all_mufrad_trace_ids`

---

### Law 4: No predication without compositional frame

```
لا نسبة إسنادية بلا إطار تركيبي
```

**Enforcement:**
NominalFrameSlotGeometry and VerbalFrameSlotGeometry enforce frame structure.

**Test:** `test_nominal_frame_requires_two_ready_vectors`

---

### Law 5: No embedding without licensed container/contained

```
لا نسبة تضمينية بلا حاوية/محمول مرخص
```

**Enforcement:**
TADMIN relation requires both container and contained vectors ready.

**Test:** `test_tadmin_slot_does_not_create_semantics`

---

### Law 6: No restriction without qualified/qualifier

```
لا نسبة تقييدية بلا مقيد ومقيد به مرشحين
```

**Enforcement:**
SemiSentenceFrameSlotGeometry requires both operator and governed.

**Test:** `test_semisentence_frame_requires_operator_or_preposition_potential`

---

### Law 7: No final RelationCandidate from this layer

```
لا RelationCandidate نهائي من هذه الطبقة
```

**Principle:**
Only RelationAlgebraCore produces RelationCandidate.
This layer only prepares RelationSlotVector.

**Test:** `test_relation_slot_vector_can_only_target_relation_algebra_core`

---

### Law 8: No Ifadah

```
لا إفادة
```

**Enforcement:**
```python
forbidden_fields = ['ifadah', 'pragmatic_completion', 'ifadah_closure']
```

**Test:** `test_isnad_slot_does_not_create_ifadah`

---

### Law 9: No Hukm

```
لا حكم
```

**Enforcement:**
```python
forbidden_fields = ['hukm', 'judgment', 'truth_value']
```

**Test:** `test_taqyid_slot_does_not_create_hukm`

---

### Law 10: No meaning

```
لا معنى
```

**Enforcement:**
```python
forbidden_fields = ['meaning', 'semantic', 'madlul', 'murad']
```

**Test:** `test_tadmin_slot_does_not_create_semantics`

---

## Article 3: Three Frame Types

### 3.1 Nominal Sentence Frame (الجملة الاسمية)

**Structure:**
```python
@dataclass(frozen=True)
class NominalFrameSlotGeometry:
    mubtada_vector: PreSyntaxMufradVector
    khabar_vector: PreSyntaxMufradVector
    isnad_potential: bool
    agreement_potential: bool
    terminal_i3rab_potential: bool
    # Preserved traces
    mubtada_trace_id: str
    khabar_trace_id: str
    # Governance
    residuals: Tuple[Residual, ...]
    rank: LughaRank
    frame_id: str
```

**Example:**
```
زيدٌ قائمٌ
- mubtada_vector: PreSyntaxMufradVector("زيد")
- khabar_vector: PreSyntaxMufradVector("قائم")
- isnad_potential: True
```

**NOT:**
```
❌ mubtada_final = "زيد"
❌ khabar_final = "قائم"
❌ meaning = "زيد صفته القيام"
```

---

### 3.2 Verbal Sentence Frame (الجملة الفعلية)

**Structure:**
```python
@dataclass(frozen=True)
class VerbalFrameSlotGeometry:
    verb_vector: PreSyntaxMufradVector
    actor_vector: PreSyntaxMufradVector
    object_vector: Optional[PreSyntaxMufradVector]
    verb_actor_isnad_potential: bool
    verb_object_tadmin_potential: bool
    valency_satisfied: bool
    tense_event_potential: bool
    # Preserved traces
    verb_trace_id: str
    actor_trace_id: str
    object_trace_id: Optional[str]
    # Governance
    residuals: Tuple[Residual, ...]
    rank: LughaRank
    frame_id: str
```

**Example:**
```
كَتَبَ زيدٌ رسالةً
- verb_vector: PreSyntaxMufradVector("كتب")
- actor_vector: PreSyntaxMufradVector("زيد")
- object_vector: PreSyntaxMufradVector("رسالة")
```

**NOT:**
```
❌ faail_final = "زيد"
❌ mafool_final = "رسالة"
❌ meaning = "زيد فعل الكتابة على رسالة"
```

---

### 3.3 Semi-Sentence Frame (شبه الجملة)

**Structure:**
```python
@dataclass(frozen=True)
class SemiSentenceFrameSlotGeometry:
    operator_or_preposition_vector: PreSyntaxMufradVector
    governed_nominal_vector: PreSyntaxMufradVector
    taqyid_potential: bool
    tadmin_potential: bool
    attachment_target_expected: bool
    # Preserved traces
    operator_trace_id: str
    governed_trace_id: str
    # Governance
    residuals: Tuple[Residual, ...]
    rank: LughaRank
    frame_id: str
```

**Example:**
```
في البيتِ
- operator_or_preposition_vector: PreSyntaxMufradVector("في")
- governed_nominal_vector: PreSyntaxMufradVector("البيت")
- taqyid_potential: True
```

**NOT:**
```
❌ mutaalliq_final = "في البيت"
❌ khabar_final = "في البيت"
❌ meaning = "ظرف مكان"
```

---

## Article 4: Relation Type Preparation

### 4.1 Five Core Relation Types

This layer prepares slots for the five relation types:

1. **ISNAD (الإسناد)** - Predication
   - Used in: Nominal sentences, Verbal sentences
   - Example: زيدٌ قائمٌ (ISNAD between زيد and قائم)

2. **TADMIN (التضمين)** - Embedding/Containment
   - Used in: Verbal sentences (verb-object)
   - Example: كَتَبَ رسالةً (TADMIN: verb contains object)

3. **TAQYID (التقييد)** - Restriction/Modification
   - Used in: Semi-sentences
   - Example: في البيتِ (TAQYID: restricts location)

4. **WASF (الوصف)** - Description/Attribution
   - Used in: Attributive constructions
   - Example: الرجل الطويل (WASF: attribute describes entity)

5. **IDAFAH (الإضافة)** - Attachment/Possession
   - Used in: Possessive/genitive constructions
   - Example: كتاب زيدٍ (IDAFAH: possession relation)

### 4.2 Relation Slot Vector

**Unified Container:**
```python
@dataclass(frozen=True)
class RelationSlotVector:
    frame_type: CompositionFrameType
    frame_geometry: NominalFrameSlotGeometry | VerbalFrameSlotGeometry | SemiSentenceFrameSlotGeometry
    relation_slot_type: RelationType
    input_vectors: Tuple[PreSyntaxMufradVector, ...]
    preserved_trace_ids: Tuple[str, ...]
    before_vector_indices: Tuple[int, ...]
    after_candidate_index: Optional[int]
    before_after_relation_type: Optional[RelationType]
    residuals: Tuple[Residual, ...]
    rank: LughaRank
    vector_id: str
```

---

## Article 5: Before-After Relation Tracking

### 5.1 Purpose

Many Arabic constructions require tracking:
- What came before (ما قبل)
- What comes after (ما بعد)
- The relation between them

### 5.2 Implementation

```python
RelationSlotVector(
    before_vector_indices=(0,),  # Index in input_vectors
    after_candidate_index=1,     # Index in input_vectors
    before_after_relation_type=RelationType.ISNAD,
    ...
)
```

**Example:**
```
زيدٌ قائمٌ
- before: زيد (index 0)
- after: قائم (index 1)
- relation: ISNAD
```

---

## Article 6: Integration with OperationAlgebra

### 6.1 Trace Preservation

Uses `OperationAlgebra` trace system:
- Every operation must preserve trace_id
- Trace chain: slot_id → mufrad_id → raw_span

### 6.2 Residual Inheritance

Uses `Residual` taxonomy:
- Slot geometry inherits residuals from input vectors
- Adds new residuals for unresolved frame aspects
- Residuals propagate to RelationAlgebraCore

### 6.3 Rank Propagation

Uses `LughaRank`:
- Slot rank = weakest input rank
- Certificate level requires all inputs at certificate level
- Rank propagates to relation output

---

## Article 7: Integration with RelationAlgebraCore

### 7.1 Input Contract

**RelationAlgebraCore accepts ONLY:**
```python
RelationSlotVector  # From this module
```

**RelationAlgebraCore REJECTS:**
```python
❌ PreSyntaxMufradVector  # Too early
❌ raw_token              # Forbidden
❌ string                 # Forbidden
```

### 7.2 Operation Signature

```python
def relation_algebra_apply(
    slot_vector: RelationSlotVector,
    context: Optional[CompositionContext] = None
) -> RelationCandidate | AlgebraicFailure:
    """Apply relation operation on prepared slots"""
    ...
```

---

## Article 8: Forbidden Jump Prevention

### 8.1 The Forbidden Sequence

```
❌ PreSyntaxMufradVector → Meaning (NO!)
❌ PreSyntaxMufradVector → Ifadah (NO!)
❌ PreSyntaxMufradVector → Hukm (NO!)
❌ RelationSlotVector → Meaning (NO!)
❌ RelationSlotVector → Ifadah (NO!)
```

### 8.2 The Correct Sequence

```
✅ PreSyntaxMufradVector
    → RelationSlotVector
        → RelationAlgebraCore
            → RelationCandidate
                → STOP before Ifadah/Hukm
```

---

## Article 9: Constitutional Tests

### 9.1 Required Tests (10 Total)

All tests in `tests/dal_core/test_relation_slot_readiness.py`:

1. `test_relation_slot_readiness_rejects_raw_string`
2. `test_relation_slot_readiness_rejects_unready_presyntax_vector`
3. `test_relation_slot_readiness_preserves_all_mufrad_trace_ids`
4. `test_isnad_slot_does_not_create_ifadah`
5. `test_tadmin_slot_does_not_create_semantics`
6. `test_taqyid_slot_does_not_create_hukm`
7. `test_nominal_frame_requires_two_ready_vectors`
8. `test_verbal_frame_requires_verb_anchor`
9. `test_semisentence_frame_requires_operator_or_preposition_potential`
10. `test_relation_slot_vector_can_only_target_relation_algebra_core`

### 9.2 Test Execution

```bash
pytest tests/dal_core/test_relation_slot_readiness.py -v
```

All tests must pass before any code using RelationSlotReadiness is merged.

---

## Article 10: Summary Table

| Concept | Existing Name | New Name | Status |
|---------|---------------|----------|--------|
| شعاع اللفظ المفرد | PreSyntaxMufradVector | (unchanged) | ✅ EXISTS |
| جاهزية التركيب | CompositionReadiness | (unchanged) | ✅ EXISTS |
| النسب الإسنادية/التضمينية/التقييدية | RelationType (ISNAD/TADMIN/TAQYID) | (unchanged) | ✅ EXISTS |
| حفظ الأثر والبقايا والرتبة | OperationAlgebra + Residual + Rank | (unchanged) | ✅ EXISTS |
| topology قبل المعنى | arabic_layers.py | (unchanged) | ✅ EXISTS |
| **جاهزية خانات النسبة** | (missing) | **RelationSlotReadiness** | **✅ NEW** |

---

## Version History

- **2026-05-28**: Initial constitution created
  - Defined three frame types (nominal/verbal/semi)
  - Established 10 constitutional laws
  - Created bridge between PreSyntaxMufradVector and RelationAlgebraCore
  - Prohibited meaning/ifadah/hukm production
  - Required trace preservation
  - Implemented before-after relation tracking

---

**Last Updated**: 2026-05-28
**Status**: CONSTITUTIONAL FOUNDATION - Immutable
**Authority**: Must be enforced before U₁₁ implementation begins
