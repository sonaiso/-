# Arabic Operator Algebra Constitutional Law

**Created**: 2026-05-27
**Status**: CONSTITUTIONAL FOUNDATION
**Authority**: Immutable architectural constraint

---

## Constitutional Declaration

```
Arabic Operator Algebra is an algebra of licensed syntactic effects,
NOT an algebra of meanings, ifādah, or judgments.

جبر العوامل العربية جبر آثار مرخّصة، لا جبر أحكام.
```

---

## Article 1: Fundamental Definition

### 1.1 Formal Signature

```
ArabicOperatorAlgebra =
EvidenceIndexedPartialAlgebra
(
  Input  = WordContract ∪ RelationCandidate,
  Output = OperatorEffectCandidate ∪ AlgebraicFailure
)
```

### 1.2 Operation Signature

```
ʿĀmilOpₑ :
  OperatorCandidate × Target × Scope
  ⇀ OperatorEffectCandidate ∪ AlgebraicFailure

where:
  Target ∈ {WordContract, RelationCandidate}
```

### 1.3 Prohibited Targets

The operator algebra **MUST NOT** accept:

- ❌ `raw_word` - unlicensed surface token
- ❌ `root` - morphological primitive only
- ❌ `weight` - pattern without word contract
- ❌ `meaning` - semantic entity
- ❌ `hukm` - judgment entity

**Rationale**: Only licensed, identity-preserving contracts provide stable anchors for operator effects.

---

## Article 2: The Eleven Constitutional Prohibitions

### 2.1 No Operator before MSL (Minimal Sufficient License)

```
لا عامل بلا حد أدنى كافٍ
No Operator before MSL
```

**Enforcement**: Every operator must pass MSL validation:
- ✅ Licensed operator form exists
- ✅ Target available and valid
- ✅ Scope resolvable
- ✅ Effect licensed for this operator type
- ✅ Evidence available
- ✅ No blocking residuals

**Violation**: Return `AlgebraicFailure(reason="MSL_NOT_SATISFIED", gate="msl_validation")`

---

### 2.2 No Operator without WordContract or RelationCandidate

```
لا عامل بلا عقد لفظي أو علاقة مرشحة
No Operator without WordContract or RelationCandidate
```

**Enforcement**: Reject all inputs that are not:
- `WordContract` (from U₁₀ WORDFORM_DOMAIN), OR
- `RelationCandidate` (from U₁₁ RelationAlgebraCore)

**Violation**: Return `AlgebraicFailure(reason="INVALID_TARGET_TYPE")`

---

### 2.3 No Effect without Scope

```
لا أثر بلا نطاق
No Effect without Scope
```

**Enforcement**: Every `OperatorEffectCandidate` must include:
- `scope.source_operator_id`
- `scope.target_anchor_id`
- `scope.start_slot`
- `scope.end_slot`
- `scope.attachment_type`
- `scope.termination_condition`

**Violation**: Return `AlgebraicFailure(reason="SCOPE_UNDEFINED")`

---

### 2.4 No Scope without target_anchor_id

```
لا نطاق بلا مرساة هدف
No Scope without target_anchor_id
```

**Enforcement**: Scope must anchor to preserved identity:
```python
scope.target_anchor_id == target.anchor_id
```

**Violation**: Return `AlgebraicFailure(reason="SCOPE_NOT_ANCHORED")`

---

### 2.5 No Effect without Evidence

```
لا أثر بلا دليل
No Effect without Evidence
```

**Enforcement**: Every `OperatorEffectCandidate` must carry:
```python
effect.evidence: DalEvidence  # span + source + claim
```

**Violation**: Return `AlgebraicFailure(reason="EVIDENCE_MISSING", evidence_gap=...)`

---

### 2.6 No Effect without Residual Inheritance

```
لا أثر بلا توريث بقايا
No Effect without Residual Inheritance
```

**Enforcement**: Operator must inherit and propagate:
```python
effect.inherited_residuals = target.residuals
effect.new_residuals = operator.residuals ∪ effect_induced_residuals
```

**Violation**: Return `AlgebraicFailure(reason="RESIDUAL_INHERITANCE_BROKEN")`

---

### 2.7 No Effect without Rank Bound

```
لا أثر بلا رتبة مضبوطة
No Effect without Rank Bound
```

**Enforcement**: Operator effect rank must satisfy:
```python
effect.rank ≤ operator.max_rank
effect.rank ∈ {Rank.CANDIDATE, Rank.HYPOTHESIS, Rank.VALIDATED}
effect.rank ≠ Rank.CERTIFICATE  # Reserved for Ifadah + Evidence closure
```

**Violation**: Return `AlgebraicFailure(reason="RANK_BOUND_VIOLATED", rank_issue=...)`

---

### 2.8 No Meaning from Operator

```
لا معنى من العامل
No Meaning from Operator
```

**Enforcement**: Operator **MUST NOT** produce:
- `SemanticIdentity`
- `LexicalMeaning`
- `ConceptualContent`
- Fields named: `meaning`, `murad`, `haqiqa_majaz`

**Violation**: `ValueError` raised during construction (construction invariant violation)

---

### 2.9 No Ifadah from Operator

```
لا إفادة من العامل
No Ifadah from Operator
```

**Enforcement**: Operator **MUST NOT** produce:
- `IfadahCandidate`
- `IfadahClosure`
- `PragmaticCompletion` (تمام الإفادة)

**Violation**: `ValueError` raised during construction

---

### 2.10 No Hukm from Operator

```
لا حكم من العامل
No Hukm from Operator
```

**Enforcement**: Operator **MUST NOT** produce:
- `HukmCandidate`
- `Judgment`
- `TruthValue`
- `EpistemicCertificate`

**Violation**: `ValueError` raised during construction

---

### 2.11 No identity collapse under Operator

```
لا انهيار هوية تحت العامل
No identity collapse under Operator
```

**Enforcement**: Operator **MUST** preserve:
```python
effect.preserved_anchor_id == target.anchor_id
effect.preserved_slot_trace == target.slot_trace
effect.preserved_word_contract_trace == target.word_contract_trace  # if applicable
effect.preserved_relation_trace == target.relation_trace  # if RelationCandidate
```

**Principle**: The operator adds a layer, does not replace identity:
```
target + licensed_effect  ✅
NOT: target → new_identity  ❌
```

**Violation**: Return `AlgebraicFailure(reason="IDENTITY_COLLAPSE")`

---

## Article 3: What Operators Produce

### 3.1 OperatorEffectCandidate Definition

```python
@dataclass(frozen=True)
class OperatorEffectCandidate:
    """
    Constitutional operator output.

    An operator effect is a scoped, evidence-backed, rank-bounded,
    identity-preserving syntactic transformation candidate.

    It is NOT:
    - A meaning
    - An ifadah
    - A hukm
    - A semantic judgment
    """
    operator_id: str
    operator_type: OperatorType
    target_anchor_id: str  # PRESERVED from input
    target_type: TargetType  # WordContract | RelationCandidate
    scope: EffectScope
    effect_type: EffectType  # case/mood/scope/negation/condition/etc.
    effect_value: Any  # Typed based on effect_type
    preserved_anchor_id: str  # === target_anchor_id
    preserved_slot_trace: tuple[int, ...]  # Preserved from target
    inherited_residuals: tuple[Residual, ...]
    new_residuals: tuple[Residual, ...]
    rank: Rank  # ≤ operator.max_rank, ≠ CERTIFICATE
    evidence: DalEvidence
    blocked_outputs: frozenset[str]  # MUST contain forbidden outputs

    def __post_init__(self):
        # Constitutional enforcement
        if self.preserved_anchor_id != self.target_anchor_id:
            raise ValueError("Identity collapse: preserved_anchor_id ≠ target_anchor_id")

        required_blocks = {"Meaning", "Ifadah", "Hukm", "SemanticIdentity", "FinalJudgment"}
        if not required_blocks.issubset(self.blocked_outputs):
            raise ValueError(f"Missing required blocked outputs: {required_blocks - self.blocked_outputs}")

        if self.rank == Rank.CERTIFICATE:
            raise ValueError("Operator effects cannot have rank CERTIFICATE")
```

### 3.2 Mandatory Blocked Outputs

Every `OperatorEffectCandidate.blocked_outputs` **MUST** contain:

- `"Meaning"`
- `"Ifadah"`
- `"Hukm"`
- `"SemanticIdentity"`
- `"FinalJudgment"`

---

## Article 4: Effect Types and Their Boundaries

### 4.1 Permitted Effect Types

Operators may produce **scoped effects only**:

| Effect Type | Operator Family | Scope | Example |
|-------------|----------------|-------|---------|
| `case_effect` | Jarr, Nasb | attachment to operator | مررتُ بزيدٍ |
| `mood_effect` | Jazm, Nasb | verbal complement | لم يذهبْ |
| `scope_effect` | Negation, Condition | conditional/negation scope | ما جاء زيد |
| `negation_effect` | Negation operators | negation scope | لم، لا، ما |
| `condition_effect` | Conditional operators | condition→consequence | إن ... ف |
| `temporal_effect` | Temporal operators | time shift potential | كان، لم |
| `emphasis_effect` | Emphatic operators | emphasis scope | إنَّ، قد |
| `attachment_effect` | Prepositions | attachment relation | الباء، اللام |
| `coordination_effect` | Coordination | coordination scope | و، ف، ثم |
| `exception_effect` | Exception | exception scope | إلا |

### 4.2 Forbidden Effect Types

Operators **MUST NOT** produce:

- ❌ `meaning_determination`
- ❌ `semantic_interpretation`
- ❌ `ifadah_closure`
- ❌ `pragmatic_completion`
- ❌ `hukm_assignment`
- ❌ `truth_value`
- ❌ `epistemic_certificate`

---

## Article 5: Operators Prepare Relations, Not Close Them

### 5.1 Readiness States (Permitted)

Operators may prepare relational readiness:

- ✅ `IsnadReadiness` - prepares for ISNAD relation
- ✅ `TadminReadiness` - prepares for TADMIN relation
- ✅ `TaqyidReadiness` - prepares for TAQYID relation
- ✅ `IdafahReadiness` - prepares for IDAFAH relation
- ✅ `WasfReadiness` - prepares for WASF relation
- ✅ `AttachmentReadiness` - prepares attachment
- ✅ `ConditionalReadiness` - prepares conditional structure
- ✅ `NegationScopeReadiness` - prepares negation scope

### 5.2 Closure States (Forbidden)

Operators **MUST NOT** produce:

- ❌ `ClosedIsnad`
- ❌ `ClosedTadmin`
- ❌ `ClosedTaqyid`
- ❌ `RelationClosure`
- ❌ `Ifadah`
- ❌ `Hukm`

**Principle**: Operators prepare, they do not close.

---

## Article 6: Example - إنَّ زيدًا قائمٌ

### 6.1 What the Operator إنَّ Produces

```python
OperatorEffectCandidate(
    operator_id="inna_001",
    operator_type=OperatorType.NOMINAL_ACCUSATIVE,
    target_anchor_id="anchor_zayd_123",  # PRESERVED
    target_type=TargetType.WORD_CONTRACT,
    scope=EffectScope(
        source_operator_id="inna_001",
        target_anchor_id="anchor_zayd_123",
        start_slot=0,
        end_slot=2,  # إنَّ ... خبرها
        attachment_type=AttachmentType.OPERATOR_OPERAND,
        termination_condition="until_khabar"
    ),
    effect_type=EffectType.EMPHASIS_ACCUSATIVE_NOMINAL,
    effect_value="mansub_candidate",
    preserved_anchor_id="anchor_zayd_123",  # SAME
    preserved_slot_trace=(0, 1),
    inherited_residuals=(),  # from زيد WordContract
    new_residuals=(
        Residual(type="khabar_pending", rank=Rank.HYPOTHESIS),
    ),
    rank=Rank.CANDIDATE,  # NOT CERTIFICATE
    evidence=DalEvidence(
        span=(0, 2),
        source="inna_particle",
        claim="emphasis_with_nominal_effect"
    ),
    blocked_outputs=frozenset({
        "Meaning",
        "Ifadah",
        "Hukm",
        "SemanticIdentity",
        "FinalJudgment"
    })
)
```

### 6.2 What إنَّ Does NOT Produce

❌ The operator does NOT produce:
- A judgment that "زيد is قائم"
- A closed relation
- A semantic meaning
- An ifadah completion
- A truth value

### 6.3 Correct Pipeline

```
WordContract(زيد) + WordContract(قائم)
  → RelationCandidate(ISNAD: زيد ← قائم)
  → OperatorEffect(إنَّ adds emphasis/accusative scope)
  → RelationAdjustedCandidate
  → RelationClosure
  → IfadahCandidate
  → HukmCandidate
```

---

## Article 7: Identity Preservation Law

### 7.1 The Preservation Principle

```
زيد ≠ النصب
زيد preserves identity
النصب is a licensed structural effect carried on زيد
```

**Formal statement**:
```python
assert effect.preserved_anchor_id == target.anchor_id
assert effect.preserved_slot_trace == target.slot_trace
```

### 7.2 Effect as Layer, Not Replacement

```
Correct:   target + licensed_effect
Incorrect: target → new_identity
```

**Example**:
```
جاء زيدٌ      → زيد carries nominative effect (فاعل readiness)
رأيتُ زيدًا   → زيد carries accusative effect (مفعول readiness)
مررتُ بزيدٍ   → زيد carries genitive effect (مجرور readiness)
```

In all cases: `anchor_id(زيد)` remains constant.

---

## Article 8: Constitutional Tests (Required Before Implementation)

### 8.1 Rejection Tests

Every operator implementation **MUST** pass:

```python
def test_operator_cannot_accept_raw_word():
    """Operator rejects unlicensed surface token."""

def test_operator_cannot_accept_root_candidate():
    """Operator rejects bare root without WordContract."""

def test_operator_cannot_accept_weight_candidate():
    """Operator rejects bare weight without WordContract."""
```

### 8.2 MSL Tests

```python
def test_operator_requires_msl():
    """Operator returns AlgebraicFailure if MSL not satisfied."""
```

### 8.3 Scope Tests

```python
def test_operator_requires_scope():
    """Operator returns AlgebraicFailure if scope undefined."""

def test_operator_returns_algebraic_failure_on_missing_scope():
    """Missing scope → AlgebraicFailure, not exception."""
```

### 8.4 Identity Preservation Tests

```python
def test_operator_preserves_anchor_id():
    """effect.preserved_anchor_id == target.anchor_id."""

def test_operator_preserves_slot_trace():
    """effect.preserved_slot_trace == target.slot_trace."""
```

### 8.5 Residual Tests

```python
def test_operator_inherits_residuals():
    """effect.inherited_residuals == target.residuals."""
```

### 8.6 Rank Tests

```python
def test_operator_output_rank_is_not_certificate_by_default():
    """Operator effects cannot be CERTIFICATE rank."""
```

### 8.7 Forbidden Output Tests

```python
def test_operator_cannot_output_meaning():
    """Operator raises ValueError if producing meaning field."""

def test_operator_cannot_output_ifadah():
    """Operator raises ValueError if producing Ifadah."""

def test_operator_cannot_output_hukm():
    """Operator raises ValueError if producing Hukm."""
```

### 8.8 Evidence Tests

```python
def test_operator_returns_algebraic_failure_on_missing_evidence():
    """Missing evidence → AlgebraicFailure."""
```

### 8.9 Target Type Tests

```python
def test_operator_requires_word_contract_or_relation_candidate():
    """Only WordContract or RelationCandidate accepted."""
```

**Note**: These tests are **more important** than cataloging the 100 operators themselves.

---

## Article 9: The Correct Pipeline

### 9.1 Architectural Sequence

```
U₁₀: WordFormCandidate (WORDFORM_DOMAIN)
  ↓
U₁₁: RelationCandidate (RelationAlgebraCore: ISNAD/TADMIN/TAQYID/WASF/IDAFAH)
  ↓
[Operator Algebra Layer]  ← Licensed structural effects only
  ↓
OperatorEffectCandidate
  ↓
RelationAdjustedCandidate
  ↓
U₁₂: RelationClosure
  ↓
U₁₃: IfadahCandidate
  ↓
U₁₄: HukmCandidate
```

### 9.2 Forbidden Jump

```
❌ Operator → Hukm (FORBIDDEN)
```

This jump **breaks the entire algebra** because:
- It bypasses WordContract validation
- It bypasses RelationCandidate validation
- It bypasses RelationClosure
- It bypasses Ifadah completion
- It produces judgment without evidence closure

---

## Article 10: Domain and Layer Mapping

### 10.1 Proposed Domain

Add to `DomainType`:
```python
OPERATOR_DOMAIN = auto()  # مجال العوامل التركيبية
```

**DomainSpec**:
- Arabic name: "مجال العوامل التركيبية"
- Layer: SYNTAX_LAYER
- Competencies: operator_effect, scope_bounded_transformation, readiness_preparation
- Prohibitions: meaning, ifadah, hukm, semantic_interpretation, relation_closure
- Requires: WORDFORM_DOMAIN or SYNTAX_DOMAIN (RelationCandidate)
- Allows transition to: SYNTAX_DOMAIN (RelationAdjustedCandidate)

### 10.2 Proposed ExecutionLayer

Consider adding:
```python
U11A_OPERATOR_ALGEBRA = auto()  # Between U₁₁ and U₁₂
```

Or integrate into existing U₁₂ as pre-closure phase.

---

## Article 11: Failure Semantics

### 11.1 AlgebraicFailure Returns

Per PR-1C hybrid failure semantics, operators **MUST** return `AlgebraicFailure` (not raise exceptions) for:

- MSL not satisfied
- Invalid target type
- Scope undefined
- Scope not anchored
- Evidence missing
- Residual inheritance broken
- Rank bound violated
- Identity collapse

### 11.2 Exception Raises

Operators **MUST** raise construction exceptions for:

- Attempting to produce `Meaning`
- Attempting to produce `Ifadah`
- Attempting to produce `Hukm`
- Missing required blocked outputs
- Rank == CERTIFICATE

---

## Article 12: Final Constitutional Statement

```
Every operator must consume either a WordContract or a RelationCandidate,
must pass its own Minimal Sufficient License,
must operate inside an explicit scope,
must preserve anchor_id and slot_trace,
must inherit residuals,
must remain rank-bounded,
and must output only OperatorEffectCandidate or AlgebraicFailure.
```

**In Arabic**:
```
جبر العوامل العربية جبر آثار مرخّصة، لا جبر أحكام.
لا يعمل العامل إلا على WordContract أو RelationCandidate،
ولا يعمل إلا بعد حد أدنى كافٍ،
ولا يضيف إلا OperatorEffectCandidate محدود النطاق،
مع حفظ anchor_id و slot_trace،
وتوريث البقايا، وضبط الرتبة،
ومنع أي قفز إلى Meaning أو Ifadah أو Hukm.
```

---

## Version History

- **2026-05-27**: Initial constitutional law document created
  - Defined 11 constitutional prohibitions
  - Established OperatorEffectCandidate structure
  - Specified forbidden outputs
  - Required 15 constitutional tests
  - Blocked meaning/ifadah/hukm production
  - Enforced identity preservation
  - Established correct pipeline sequence

---

**Last Updated**: 2026-05-27
**Status**: CONSTITUTIONAL FOUNDATION - Immutable
**Authority**: Must be enforced before any Operator Algebra implementation begins
