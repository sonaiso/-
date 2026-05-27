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
- ❌ `raw_slot` - bare phonological/graphemic slot
- ❌ `raw_syllable` - bare syllable without license
- ❌ `root_candidate` - morphological primitive only
- ❌ `weight_candidate` - pattern without word contract
- ❌ `LicensedSingularLafz` - licensed utterance before word contract (see Article 1A)
- ❌ `meaning` - semantic entity
- ❌ `hukm` - judgment entity

**Rationale**: Only licensed, identity-preserving **word contracts** and **relation candidates** provide stable anchors for syntactic operator effects.

---

## Article 1A: LicensedSingularLafz vs WordContract (Critical Distinction)

### 1A.1 The Two Algebraic Paths

**Constitutional Principle**:
```
No syntactic operator before WordContract.
No WordContract before LicensedSingularLafz.
```

There are **two distinct algebraic paths**:

#### Path 1: Licensed Singular Utterance (Lafz Path)

```
SlotGeometry
  → LetterSlot / VowelSlot
  → SyllableLicense
  → SlotComposition
  → MinimalLicensedLafz
  → LicensedSingularLafz
```

**What this establishes**:
- ✅ A single, licensed phonological/graphemic utterance exists
- ✅ Slot composition is valid
- ✅ Syllable structure is licensed
- ✅ Minimal lafz requirements met

**What this does NOT establish**:
- ❌ Whether it's a noun, verb, or particle ready for composition
- ❌ Whether it carries syntactic function
- ❌ Whether it's eligible for operator effects

#### Path 2: Word Contract (Word Path)

```
LicensedSingularLafz
  → Pathability
  → MabniGate / ToolGate / PronounGate / Rootability / Stemability / Weightability
  → WordIdentityCandidate
  → WordContract
```

**What this establishes**:
- ✅ The lafz has become a contracted word node
- ✅ Identity classification complete (or residualized)
- ✅ Syntactic readiness achieved
- ✅ Operator eligibility confirmed

### 1A.2 Formal Definitions

#### LicensedSingularLafz

```python
@dataclass(frozen=True)
class LicensedSingularLafz:
    """
    A phonologically/graphemically licensed singular utterance.

    This is NOT yet a word contract. It is a licensed lafz that:
    - May be a root candidate
    - May be a stem candidate
    - May be mabni (invariable)
    - May be a tool/particle
    - May be a pronoun
    - May be part of a longer composition
    - May carry unresolved residuals

    Syntactic operators MUST NOT consume this directly.
    Only WordContract or RelationCandidate are valid operator targets.
    """
    lafz_anchor_id: str
    slot_trace: tuple[int, ...]
    syllable_trace: tuple[str, ...]
    minimal_license: bool
    path_candidates: tuple[str, ...]  # Possible paths (mabni, root, stem, tool, etc.)
    residuals: tuple[Residual, ...]
    rank: Rank
    evidence: DalEvidence
```

#### WordContract

```python
@dataclass(frozen=True)
class WordContract:
    """
    A singular word with established contract for syntactic composition.

    This is derived from LicensedSingularLafz after:
    - Path resolution (or residualized path with rank bounds)
    - Word identity establishment
    - Syntactic readiness confirmation
    - Operator eligibility verification

    This is the MINIMAL input for syntactic operators.
    """
    lafz_anchor_id: str  # Preserved from LicensedSingularLafz
    word_anchor_id: str  # New word-level identity
    slot_trace: tuple[int, ...]  # Preserved
    path_trace: tuple[str, ...]  # Path resolution history
    word_identity: WordIdentity  # Classified or residualized
    syntactic_readiness: bool
    operator_eligibility: bool
    preserved_residuals: tuple[Residual, ...]
    rank: Rank
    evidence: DalEvidence
```

### 1A.3 Example: ما (mā)

Consider the particle ما:

**Stage 1: LicensedSingularLafz**
```python
LicensedSingularLafz(
    lafz_anchor_id="lafz_ma_001",
    slot_trace=(0, 1),
    syllable_trace=("mā",),
    minimal_license=True,
    path_candidates=("negation", "interrogative", "relative", "masdariyya", "zaidah"),
    residuals=(
        Residual(type="path_ambiguity", candidates=5),
    ),
    rank=Rank.CANDIDATE,
    evidence=DalEvidence(...)
)
```

At this stage:
- ❌ Syntactic operators **CANNOT** operate on it
- ❌ We don't know which ما it is yet
- ⚠️ Operator would be premature - path unresolved

**Stage 2: WordContract** (after path resolution or residualization)
```python
WordContract(
    lafz_anchor_id="lafz_ma_001",  # PRESERVED
    word_anchor_id="word_ma_negation_001",
    slot_trace=(0, 1),  # PRESERVED
    path_trace=("tool_gate", "negation_particle"),
    word_identity=WordIdentity.NEGATION_PARTICLE,
    syntactic_readiness=True,
    operator_eligibility=True,
    preserved_residuals=(),  # Path resolved
    rank=Rank.VALIDATED,
    evidence=DalEvidence(...)
)
```

Now:
- ✅ Syntactic operators **CAN** operate on it
- ✅ Identity established: negation particle
- ✅ Operator can add negation scope effect

### 1A.4 Constitutional Laws

```
No ʿĀmil before LicensedSingularLafz.
No syntactic ʿĀmil before WordContract.
No WordContract before LicensedSingularLafz.
No WordContract before pathability or residualized path.
No OperatorEffect without WordContract or RelationCandidate.
```

**In Arabic**:
```
لا عامل قبل لفظ مفرد مرخص.
ولا عامل نحوي قبل عقد كلمة.
ولا عقد كلمة قبل لفظ مفرد مرخص.
ولا عقد كلمة قبل قابلية مسار أو بقايا مسار مصنفة.
ولا أثر عاملي بلا WordContract أو RelationCandidate.
```

### 1A.5 Why This Distinction is Critical

**Without this distinction**, an operator could act on ما before knowing:
- Is it negation? (لا أثر نفي)
- Is it interrogative? (استفهام)
- Is it relative? (موصولة)
- Is it masdariyya? (مصدرية)
- Is it redundant? (زائدة)

**With this distinction**:
1. ما first becomes `LicensedSingularLafz` (licensed, but path ambiguous)
2. Path resolution (or residualization) produces `WordContract`
3. **Only then** can syntactic operators apply effects
4. Operators work on **resolved or bounded-residual identities**, not raw lafz

### 1A.6 PreWord Operators (Exception)

**Rare exception**: Some operators/particles may participate in **forming** the WordContract itself, not in operating on it syntactically.

These are classified as:
```python
class PreWordOperator:
    """
    Operators that assist in WordContract formation.
    NOT syntactic operators.
    """
```

Examples:
- Definiteness markers (ال) - part of word formation
- Certain affixes - part of morphological composition

These are **NOT covered by this constitutional law** - they belong to the lafz formation layer, not the syntactic operator layer.

### 1A.7 Revised Operator Signature

```
ʿĀmilOpₑ : O × (W ∪ R) × Scope → E ∪ AlgebraicFailure

where:
  O = OperatorCandidate
  W = WordContract (NOT LicensedSingularLafz)
  R = RelationCandidate
  E = OperatorEffectCandidate
```

**NOT**:
```
❌ ʿĀmilOpₑ : O × L × Scope → E
   where L = LicensedSingularLafz
```

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

def test_operator_cannot_accept_raw_slot():
    """Operator rejects bare phonological/graphemic slot."""

def test_operator_cannot_accept_raw_syllable():
    """Operator rejects bare syllable without license."""

def test_operator_cannot_accept_root_candidate():
    """Operator rejects bare root without WordContract."""

def test_operator_cannot_accept_weight_candidate():
    """Operator rejects bare weight without WordContract."""

def test_operator_cannot_accept_licensed_singular_lafz():
    """
    CRITICAL: Operator rejects LicensedSingularLafz.

    Syntactic operators MUST NOT operate on licensed lafz before
    it becomes a WordContract. This prevents premature operator
    application before path resolution.
    """
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
SlotGeometry (U₀-U₄)
  ↓
LicensedSingularLafz (Licensed utterance path)
  ↓
WordContract (U₁₀ WORDFORM_DOMAIN) ← OPERATOR INPUT STARTS HERE
  ↓
RelationCandidate (U₁₁ RelationAlgebraCore: ISNAD/TADMIN/TAQYID/WASF/IDAFAH)
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

### 9.2 Identity Preservation Across Paths

**Lafz Path**:
```python
LicensedSingularLafz preserves:
  lafz_anchor_id
  slot_trace
  syllable_trace
  residuals
```

**Word Path**:
```python
WordContract preserves:
  lafz_anchor_id  # FROM LicensedSingularLafz
  word_anchor_id  # NEW word-level identity
  slot_trace      # FROM LicensedSingularLafz
  path_trace      # NEW path resolution history
  residuals       # Inherited and new
```

**Operator Path**:
```python
OperatorEffect preserves:
  target_anchor_id     # FROM WordContract.word_anchor_id
  word_anchor_id       # FROM WordContract
  lafz_anchor_id       # Transitively preserved
  slot_trace           # FROM WordContract
  relation_anchor_id   # If target is RelationCandidate
```

**Principle**: Identity never dissolves:
- Lafz does not dissolve into Word
- Word does not dissolve into Operator
- Operator does not dissolve into Hukm

### 9.3 Forbidden Jump

```
❌ Operator → Hukm (FORBIDDEN)
❌ LicensedSingularLafz → Operator (FORBIDDEN - Article 1A)
```

The first jump **breaks the entire algebra** because:
- It bypasses WordContract validation
- It bypasses RelationCandidate validation
- It bypasses RelationClosure
- It bypasses Ifadah completion
- It produces judgment without evidence closure

The second jump **breaks operator input contract** because:
- It operates on unresolved path ambiguity
- It operates before syntactic readiness
- It operates before operator eligibility verification
- It produces premature effects on ambiguous lafz

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

### 12.1 Operator Input Law (English)

```
A syntactic operator may not consume raw slots, raw syllables,
root candidates, weight candidates, or merely licensed lafẓ.

It may consume only:
1. WordContract derived from LicensedSingularLafz, OR
2. RelationCandidate derived from WordContracts.

The operator produces only OperatorEffectCandidate or AlgebraicFailure,
while preserving anchor_id, slot_trace, residuals, and rank bounds.

Every operator must:
- Consume WordContract or RelationCandidate (NOT LicensedSingularLafz)
- Pass its own Minimal Sufficient License
- Operate inside an explicit scope
- Preserve anchor_id and slot_trace
- Inherit residuals
- Remain rank-bounded (never CERTIFICATE)
- Output only OperatorEffectCandidate or AlgebraicFailure
- Never produce Meaning, Ifadah, or Hukm
```

### 12.2 قانون مدخل العامل (Arabic)

```
لا يدخل العامل النحوي على الخانة الخام،
ولا على المقطع الخام،
ولا على الجذر المرشح،
ولا على الوزن المرشح،
ولا على اللفظ المفرد بما هو لفظ فقط.

بل لا يدخل إلا على:
WordContract ناتج عن LicensedSingularLafz،
أو RelationCandidate ناتجة عن عقود كلمات.

ولا ينتج إلا OperatorEffectCandidate أو AlgebraicFailure،
مع حفظ anchor_id و slot_trace وتوريث البقايا وضبط الرتبة.

جبر العوامل العربية جبر آثار مرخّصة، لا جبر أحكام.
لا يعمل العامل إلا على WordContract أو RelationCandidate،
ولا يعمل إلا بعد حد أدنى كافٍ،
ولا يضيف إلا OperatorEffectCandidate محدود النطاق،
مع حفظ anchor_id و slot_trace،
وتوريث البقايا، وضبط الرتبة،
ومنع أي قفز إلى Meaning أو Ifadah أو Hukm.
```

### 12.3 The Critical Path Separation

```
LicensedSingularLafz (لفظ مفرد مرخص)
  = Phonologically/graphemically licensed utterance
  = Licensed, but NOT yet a word contract
  ❌ NOT valid operator input

WordContract (عقد كلمة)
  = Singular word with syntactic contract
  = Derived from LicensedSingularLafz after path resolution
  ✅ VALID operator input

This separation prevents operators from acting on:
- Ambiguous particles (ما: negation? interrogative? relative?)
- Unresolved roots/stems
- Unlicensed morphological forms
- Syntactically unprepared utterances
```

---

## Version History

- **2026-05-27 (Amendment 1)**: Added Article 1A - LicensedSingularLafz vs WordContract
  - Defined two distinct algebraic paths (lafz path vs word path)
  - Established constitutional principle: No syntactic operator before WordContract
  - Added formal definitions for LicensedSingularLafz and WordContract
  - Provided example: ما (mā) ambiguity resolution
  - Updated prohibited targets to include LicensedSingularLafz
  - Added critical test: test_operator_cannot_accept_licensed_singular_lafz
  - Updated identity preservation across three paths (lafz, word, operator)
  - Clarified forbidden jumps: LicensedSingularLafz → Operator
  - Revised operator signature: W = WordContract (NOT LicensedSingularLafz)

- **2026-05-27**: Initial constitutional law document created
  - Defined 11 constitutional prohibitions
  - Established OperatorEffectCandidate structure
  - Specified forbidden outputs
  - Required 15 constitutional tests
  - Blocked meaning/ifadah/hukm production
  - Enforced identity preservation
  - Established correct pipeline sequence

---

**Last Updated**: 2026-05-27 (Amendment 1)
**Status**: CONSTITUTIONAL FOUNDATION - Immutable
**Authority**: Must be enforced before any Operator Algebra implementation begins
