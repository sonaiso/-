# GARA-FT-0: Boundary Specification Document
## الدال الوظيفي - حدود دستورية قبل التنفيذ

**Document Version**: 1.0.0
**Status**: Constitutional Specification (Pre-Implementation)
**Last Updated**: 2026-05-27

---

## 1. Executive Summary | الملخص التنفيذي

This document establishes **constitutional boundaries** for GARA-FT-0 (الدال الوظيفي الجبري - مستوى صفر), the foundational layer of the Algebraic Functional Tokenizer for Arabic.

**Critical Principle**: هذا المستوى يُنتج SignifierTokenResult فقط، ولا يتعامل مع:
- Neural encodings (GARA-T5 أو شبكات عصبية)
- Syntactic relations (ISN/TADMIN/TAQYID)
- Semantic meanings (معنى/مراد/إفادة)
- Case effects (رفع/نصب/جر كأحكام نحوية)

**What GARA-FT-0 IS**:
- Boundary object wrapper around MufradProof
- Preparation for pre-syntactic readiness vectors
- Constitutional prohibition enforcer

**What GARA-FT-0 IS NOT**:
- Complete tokenizer hierarchy
- Neural architecture
- Syntax analyzer
- Semantic interpreter

---

## 2. Ontological Distinctions | الفروق الوجودية التنفيذية

### 2.1 Core Type Taxonomy

```
┌─────────────────────────────────────────────────────────────┐
│ Type Hierarchy - النمط الوجودي                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Proof          ← Immutable compositional evidence         │
│    │                                                        │
│    ├─ MufradProof      (الدليل المفردي)                   │
│    └─ MurakkabProof    (الدليل التركيبي - future)         │
│                                                             │
│  Token          ← Operational unit with licensed identity  │
│    │                                                        │
│    ├─ SignifierToken   (الدال الوظيفي)                    │
│    └─ (future tokens)                                      │
│                                                             │
│  ReadinessVector ← Typed interface for operator consumption│
│    │                                                        │
│    ├─ PreSyntaxMufradVector  (الجاهزية النحوية)           │
│    └─ (future readiness)                                   │
│                                                             │
│  Potential      ← Observed surface possibility (no judgment)│
│    │                                                        │
│    ├─ CaseSignPotential     (احتمال العلامة)              │
│    └─ OperatorTriggerPotential (احتمال المحفز)            │
│                                                             │
│  Candidate      ← Typed licensed pairing (pre-activation)  │
│    │                                                        │
│    ├─ SentenceFrameCandidate (مرشح الإطار)                │
│    ├─ OperatorCandidate      (مرشح العامل)                │
│    └─ RelationCandidate      (مرشح العلاقة - FORBIDDEN)   │
│                                                             │
│  Node           ← Graph vertex with edges and governance   │
│    │                                                        │
│    └─ (future: syntax graph nodes)                         │
│                                                             │
│  State          ← Mutable computation state machine        │
│    │                                                        │
│    └─ (future: parser state)                               │
│                                                             │
│  Result         ← Operation outcome wrapper (success/fail) │
│    │                                                        │
│    ├─ SignifierTokenResult   (نتيجة الدال الوظيفي)       │
│    ├─ PreSyntaxReadinessResult (نتيجة الجاهزية)          │
│    └─ AlgebraicFailure        (الفشل الجبري)             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Operational Definitions

#### 2.2.1 Proof (الدليل)
**Definition**: Immutable compositional evidence produced by algebraic construction.

**Properties**:
- ✓ Immutable after construction
- ✓ Contains identity, form, weight, phonology
- ✓ Validates constitutional laws at construction
- ✗ NOT operational unit (cannot be consumed by operators)
- ✗ NOT token (lacks operational interface)

**Example**: `MufradProof(identity=NOUN, form="كِتَابٌ", ...)`

**Constitutional Law**:
```python
# Forbidden in MufradProof:
_FORBIDDEN_IN_PROOF = frozenset({
    "meaning", "murad", "ifadah", "hukm", "mahall",
    "syntax_role", "case_effect", "governed_by"
})
```

---

#### 2.2.2 Token (الرمز الوظيفي)
**Definition**: Operational unit with licensed identity that can participate in functional transformations.

**Properties**:
- ✓ Licensed identity from PathAwareIdentityValidator
- ✓ Operational interface (can be consumed)
- ✓ Carries proof as evidence
- ✗ NOT mutable (identity fixed at construction)
- ✗ NOT applied operator (no case effects yet)

**Example**: `SignifierToken(proof=mufrad_proof, identity=NOUN_IDENTITY)`

**Constitutional Law**:
```python
# SignifierToken MAY contain:
_ALLOWED_IN_SIGNIFIER_TOKEN = frozenset({
    "proof",           # MufradProof reference
    "identity",        # Licensed identity path
    "form_variants",   # Bidirectional forms
})

# SignifierToken MUST NOT contain:
_FORBIDDEN_IN_SIGNIFIER_TOKEN = frozenset({
    "meaning", "murad", "semantic", "madlul",
    "case_effect", "syntax_role", "relation",
    "governed_by", "governs", "operator_applied"
})
```

---

#### 2.2.3 ReadinessVector (متجه الجاهزية)
**Definition**: Typed interface preparing data for operator consumption, without applying operators.

**Properties**:
- ✓ Contains operator consumption interface
- ✓ Exposes case sign **potentials** (not effects)
- ✓ Provides frame **candidates** (not judgments)
- ✗ NOT token (different lifecycle)
- ✗ NOT applied operator (no governance yet)

**Example**: `PreSyntaxMufradVector(proof=mufrad_proof, case_signs=[...potentials...])`

**Constitutional Law**:
```python
# PreSyntaxMufradVector MAY contain:
_ALLOWED_IN_READINESS_VECTOR = frozenset({
    "proof",                    # MufradProof reference
    "case_sign_potentials",     # List[CaseSignPotential]
    "frame_candidates",         # List[SentenceFrameCandidate]
    "operator_trigger_potentials", # List[OperatorTriggerPotential]
})

# PreSyntaxMufradVector MUST NOT contain:
_FORBIDDEN_IN_READINESS_VECTOR = frozenset({
    "case_effect",      # NOT CaseEffect (only potential)
    "applied_operator", # NOT AppliedOperator
    "syntax_role",      # NOT faail/mafool
    "relation",         # NOT ISN/TADMIN
    "governed_by",      # NO governance yet
})
```

---

#### 2.2.4 Potential (الاحتمال)
**Definition**: Observed surface possibility without grammatical judgment.

**Properties**:
- ✓ Surface observation (form-based)
- ✓ Preserves competition (multiple potentials coexist)
- ✗ NOT judgment (no "this IS the case")
- ✗ NOT effect (no governance applied)

**Example**:
```python
CaseSignPotential(
    sign=CaseSignSurface.DAMMA,  # Observed: ـُ
    # NOT case_effect=RafCase     # ← FORBIDDEN
)
```

**Constitutional Law**:
```python
# CaseSignPotential distinguishes:
CaseSignPotential   ≠ CaseEffect
    ↓                    ↓
"observed damma"    "raf' judgment by operator"

# OperatorTriggerPotential distinguishes:
OperatorTriggerPotential ≠ AppliedOperator
    ↓                         ↓
"could trigger إنّ"      "إنّ actually governs X"
```

---

#### 2.2.5 Candidate (المرشح)
**Definition**: Typed licensed pairing ready for selection, not yet activated.

**Properties**:
- ✓ Typed pairing (e.g., TriggerSource + NahwOperatorEntry)
- ✓ Preserves competition (multiple candidates)
- ✓ Licensed from registry (immutable catalog)
- ✗ NOT applied (no governance yet)
- ✗ NOT relation (composition not performed)

**Example**:
```python
OperatorCandidate(
    trigger=OperatorTriggerPotential(...),
    entry=nahw_operator_registry.get("إنّ"),
    # NOT applied_operator=...   # ← FORBIDDEN
    # NOT relation=ISN           # ← FORBIDDEN
)
```

**Constitutional Law**:
```python
# OperatorCandidate is:
OperatorCandidate = (TriggerSource, NahwOperatorEntry)
    ↓
"licensed operator-entry pairing candidate"

# OperatorCandidate is NOT:
OperatorCandidate ≠ RelationCandidate
    ↓                    ↓
"pre-activation"    "requires RelationAlgebraCore"

OperatorCandidate ≠ AppliedOperator
    ↓                    ↓
"potential"         "actual governance"
```

---

#### 2.2.6 Node (العقدة)
**Definition**: Graph vertex with edges, governance, and relation participation.

**Properties**:
- ✓ Part of syntax graph
- ✓ Has edges (incoming/outgoing)
- ✓ Participates in relations
- ✗ NOT candidate (beyond candidate stage)
- ✗ NOT in GARA-FT-0 scope

**Status**: FUTURE (requires RelationAlgebraCore activation)

---

#### 2.2.7 State (الحالة)
**Definition**: Mutable computation state machine (parser state, generator state).

**Properties**:
- ✓ Mutable
- ✓ Tracks computation progress
- ✗ NOT proof (mutable vs immutable)
- ✗ NOT in GARA-FT-0 scope

**Status**: FUTURE

---

#### 2.2.8 Result (النتيجة)
**Definition**: Operation outcome wrapper containing success/failure + payload.

**Properties**:
- ✓ Wraps operational outcome
- ✓ Contains success/failure discriminator
- ✓ Carries payload (Token/ReadinessVector/Candidate)
- ✗ NOT the payload itself

**Example**:
```python
@dataclass(frozen=True)
class SignifierTokenResult:
    """نتيجة إنتاج الدال الوظيفي"""
    signifier_token: SignifierToken | None
    presyntax_readiness: PreSyntaxMufradVector | None
    failure: AlgebraicFailure | None

    # NOT: token alone
    # Result = bundle containing all relevant outputs
```

**Constitutional Law**:
```python
# Result distinguishes:
Result ≠ Payload
  ↓        ↓
wrapper   content

# SignifierTokenResult contains:
SignifierTokenResult = (
    SignifierToken,           # Operational unit
    PreSyntaxMufradVector,   # Readiness interface
    AlgebraicFailure         # Failure if any
)
```

---

## 3. GARA-FT-0 Scope & Boundaries | النطاق والحدود الدستورية

### 3.1 Input Boundary

**Allowed Inputs**:
```python
Input = MufradProof  # ONLY
```

**Forbidden Inputs**:
- Raw strings (must go through DClosed → MufradProof first)
- Neural embeddings
- Syntax graphs
- External semantic annotations

---

### 3.2 Output Boundary

**Allowed Outputs**:
```python
Output = SignifierTokenResult
    where:
        SignifierTokenResult = (
            SignifierToken | None,
            PreSyntaxMufradVector | None,
            AlgebraicFailure | None
        )
```

**Forbidden Outputs**:
- Neural vectors
- Syntax relations (ISN/TADMIN/TAQYID)
- Case effects (رفع/نصب/جر as judgments)
- Applied operators
- RelationCandidate

---

### 3.3 Process Boundary

**GARA-FT-0 Process**:
```
MufradProof
    → [validate constitutional laws]
    → [construct SignifierToken with licensed identity]
    → [construct PreSyntaxMufradVector with potentials]
    → SignifierTokenResult
```

**Forbidden Processes**:
- Operator application (deferred to composition layer)
- Relation formation (requires RelationAlgebraCore)
- Case effect determination (requires governance)
- Semantic interpretation

---

### 3.4 Constitutional Prohibitions

#### Prohibition 1: No Meaning in Signifier Layer
```python
# FORBIDDEN in SignifierToken:
_SEMANTIC_LEAK_PREVENTION = frozenset({
    "meaning", "murad", "madlul", "semantic",
    "haqiqa", "majaz", "ifadah", "hukm"
})
```

#### Prohibition 2: No Syntax Roles Before Governance
```python
# FORBIDDEN in PreSyntaxMufradVector:
_SYNTAX_ROLE_PREVENTION = frozenset({
    "faail", "mafool", "mubtada", "khabar",
    "syntax_role", "governed_by", "governs"
})
```

#### Prohibition 3: No Case Effects Before Operators
```python
# FORBIDDEN in CaseSignPotential:
_CASE_EFFECT_PREVENTION = frozenset({
    "case_effect", "raf", "nasb", "jarr",
    "marfoo_by", "mansub_by", "majroor_by"
})
```

#### Prohibition 4: No Applied Operators Before Selection
```python
# FORBIDDEN in OperatorTriggerPotential:
_APPLIED_OPERATOR_PREVENTION = frozenset({
    "applied_operator", "operator_binding",
    "governs", "governed_nodes"
})
```

#### Prohibition 5: No Relations Before Algebra
```python
# FORBIDDEN in OperatorCandidate:
_RELATION_PREVENTION = frozenset({
    "relation", "relation_type", "relation_binding",
    "isn_subject", "isn_predicate",
    "tadmin_incorporated", "taqyid_restricted"
})
```

#### Prohibition 6: No RelationCandidate Before RelationAlgebraCore
```python
# CONSTITUTIONAL BOUNDARY:
RelationCandidate production is FORBIDDEN in GARA-FT-0.

# RelationAlgebraCore serves as preventing boundary:
# - GARA-FT-0 prepares inputs (OperatorCandidate)
# - RelationAlgebraCore consumes inputs (future)
# - RelationCandidate only produced AFTER RelationAlgebraCore activation
```

---

## 4. Pre-Syntactic Chain Position | موقع السلسلة النحوية التمهيدية

### 4.1 Existing Infrastructure

GARA-FT-0 does NOT build the pre-syntactic chain from scratch.
**The chain already exists** in `dal_core`:

```
MufradProof (476 lines)
    ↓
PreSyntaxMufradVector (presyntax_vector.py)
    ↓
SentenceFrameCandidate (sentence_frame.py)
    ↓
CaseSignMatrix (case_sign_matrix.py)
    ↓
OperatorTriggerPotential (operator_trigger.py)
    ↓
OperatorCandidate (operator_candidate.py, 721 lines)
    ↓
[BOUNDARY: RelationAlgebraCore]
    ↓
RelationCandidate (FORBIDDEN - future)
```

### 4.2 GARA-FT-0 Position

**GARA-FT-0 wraps the FIRST step only**:
```
MufradProof → SignifierTokenResult
```

**NOT**:
```
MufradProof → Neural Encoding  # ← FORBIDDEN (no GARA-T5 yet)
MufradProof → SyntaxNode        # ← FORBIDDEN (no relations yet)
MufradProof → CaseEffect        # ← FORBIDDEN (no governance yet)
```

### 4.3 Future Layers (Out of Scope)

```
GARA-FT-0: MufradProof → SignifierTokenResult
    ↓
GARA-FT-1: SignifierToken → PreSyntaxReadinessResult  (FUTURE)
    ↓
GARA-FT-2: PreSyntaxVector → OperatorCandidateResult  (FUTURE)
    ↓
GARA-FT-3: OperatorCandidate → RelationCandidateResult (FUTURE)
    requires: RelationAlgebraCore activation
    ↓
GARA-T5: Neural Integration (DISTANT FUTURE)
```

---

## 5. Critical Gaps & Future Work | الفجوات الحرجة

### 5.1 VerbalSignifiedCandidate (الأكبر)

**Status**: DOES NOT EXIST

**Required Before Implementation**:
1. `WadhEvidence` - Evidence of conventional assignment (الوضع)
2. `UsageEvidence` - Evidence of actual usage (الاستعمال)
3. `DalalahPath` - Path of signification (literal/metaphorical/equivocal)
4. `DalMadlulContract` - Contract linking signifier to signified

**Constitutional Position**:
```
SignifierToken (الدال) exists ✓
    ↓
DalMadlulContract (العقد) MISSING ✗
    ↓
VerbalSignifiedCandidate (المدلول اللفظي) MISSING ✗
```

**Deferral**:
- Deferred to GARA-FT-1 or later
- Requires linguistic evidence infrastructure
- Cannot be produced without wadh/usage evidence

---

### 5.2 RelationAlgebraCore as Boundary

**Status**: EXISTS (relation_algebra_core.py)

**Position**: **Preventing Boundary**

**Function**:
- GARA-FT-0 prepares inputs (OperatorCandidate)
- RelationAlgebraCore defines minimum requirements for RelationCandidate
- No RelationCandidate production allowed BEFORE RelationAlgebraCore activation

**5 Licensed Relations** (from RelationAlgebraCore):
1. ISNAD (الإسناد) - Predication
2. TADMIN (التضمين) - Incorporation
3. TAQYID (التقييد) - Restriction
4. WASF (الوصف) - Attribution
5. IDAFAH (الإضافة) - Annexation

**Constitutional Law**:
```python
# FORBIDDEN in GARA-FT-0:
def produce_relation_candidate(...) -> RelationCandidate:
    raise ConstitutionalViolation(
        "RelationCandidate production requires RelationAlgebraCore activation"
    )
```

---

### 5.3 Dal-Mufrad vs Dal-Murakkab Position

**Reference**: `docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md`

**GARA-FT-0 Scope**:
- **Dal-Mufrad**: ✓ IN SCOPE (SignifierToken from MufradProof)
- **Dal-Murakkab**: ✗ OUT OF SCOPE (requires composition)

**Position**:
```
Dal-Mufrad (الدال المفرد)
    ↓
    MufradProof → SignifierToken  ← GARA-FT-0 handles this

Dal-Murakkab (الدال المركب)
    ↓
    Composition → MurakkabProof → CompoundToken  ← FUTURE
```

---

## 6. Proposed First PR: SignifierTokenResult Boundary | اقتراح PR الأول

### 6.1 Scope

**PR Title**: `feat(dal_core): Add SignifierTokenResult boundary object + prohibition tests`

**Files to Add**:
1. `src/dal_core/signifier_token_result.py` - Result wrapper
2. `tests/test_signifier_token_result.py` - Tests

**Files NOT to Add** (deferred):
- `src/dal_core/presyntax_token.py` - DEFERRED
- `src/dal_core/operator_trigger_token.py` - DEFERRED
- `src/dal_core/gara_ft_tokenizer.py` - DEFERRED
- Any neural components - DEFERRED

---

### 6.2 SignifierTokenResult Structure

```python
from dataclasses import dataclass
from typing import Optional
from dal_core.mufrad_proof import MufradProof
from dal_core.dal_algebra import AlgebraicFailure
from dal_core.identity import DalIdentity

# Placeholder types (to be implemented properly later)
@dataclass(frozen=True)
class SignifierToken:
    """الدال الوظيفي - Operational signifier unit"""
    proof: MufradProof
    identity: DalIdentity
    form_variants: tuple[str, ...]  # Bidirectional forms

    def __post_init__(self):
        # Constitutional validation
        _validate_no_semantic_leak(self)
        _validate_no_syntax_roles(self)
        _validate_licensed_identity(self.identity)


@dataclass(frozen=True)
class PreSyntaxMufradVector:
    """متجه الجاهزية النحوية - Pre-syntactic readiness interface"""
    proof: MufradProof
    # Potentials, NOT effects
    case_sign_potentials: tuple  # List[CaseSignPotential]
    frame_candidates: tuple      # List[SentenceFrameCandidate]

    def __post_init__(self):
        # Constitutional validation
        _validate_no_case_effects(self)
        _validate_no_applied_operators(self)


@dataclass(frozen=True)
class SignifierTokenResult:
    """
    نتيجة إنتاج الدال الوظيفي

    Result wrapper containing:
    - SignifierToken (operational unit)
    - PreSyntaxMufradVector (readiness interface)
    - AlgebraicFailure (if construction failed)

    NOT a single token, but a bundle of outputs.
    """
    signifier_token: Optional[SignifierToken]
    presyntax_readiness: Optional[PreSyntaxMufradVector]
    failure: Optional[AlgebraicFailure]

    def __post_init__(self):
        # Exactly one must be present
        success_count = sum([
            self.signifier_token is not None,
            self.failure is not None
        ])
        if success_count != 1:
            raise ValueError(
                "SignifierTokenResult must have exactly one: "
                "signifier_token OR failure"
            )

    @property
    def is_success(self) -> bool:
        return self.failure is None

    @property
    def is_failure(self) -> bool:
        return self.failure is not None
```

---

### 6.3 Constitutional Tests

**Test File**: `tests/test_signifier_token_result.py`

```python
import pytest
from dal_core.signifier_token_result import (
    SignifierToken,
    PreSyntaxMufradVector,
    SignifierTokenResult
)

class TestConstitutionalProhibitions:
    """دستور المنع - Constitutional prohibition tests"""

    def test_signifier_token_forbids_meaning(self):
        """SignifierToken MUST NOT contain semantic fields"""
        # Attempt to add forbidden field should fail
        with pytest.raises(AttributeError):
            token = SignifierToken(...)
            token.meaning = "كتاب"  # FORBIDDEN

    def test_signifier_token_forbids_syntax_role(self):
        """SignifierToken MUST NOT contain syntax roles"""
        with pytest.raises(AttributeError):
            token = SignifierToken(...)
            token.syntax_role = "faail"  # FORBIDDEN

    def test_signifier_token_forbids_case_effect(self):
        """SignifierToken MUST NOT contain case effects"""
        with pytest.raises(AttributeError):
            token = SignifierToken(...)
            token.case_effect = "raf"  # FORBIDDEN

    def test_presyntax_vector_forbids_applied_operator(self):
        """PreSyntaxMufradVector MUST NOT contain applied operators"""
        with pytest.raises(AttributeError):
            vector = PreSyntaxMufradVector(...)
            vector.applied_operator = "inna"  # FORBIDDEN

    def test_presyntax_vector_forbids_governance(self):
        """PreSyntaxMufradVector MUST NOT contain governance"""
        with pytest.raises(AttributeError):
            vector = PreSyntaxMufradVector(...)
            vector.governed_by = "verb"  # FORBIDDEN

    def test_result_forbids_relation_candidate(self):
        """SignifierTokenResult MUST NOT produce RelationCandidate"""
        # RelationCandidate should not be accessible
        with pytest.raises(ImportError):
            from dal_core.signifier_token_result import RelationCandidate


class TestResultSemantics:
    """دلالات النتيجة - Result semantics tests"""

    def test_result_is_wrapper_not_token(self):
        """Result wraps token, is not token itself"""
        result = SignifierTokenResult(...)

        assert hasattr(result, 'signifier_token')
        assert hasattr(result, 'presyntax_readiness')
        assert hasattr(result, 'failure')

        # Result ≠ Token
        assert not isinstance(result, SignifierToken)

    def test_result_contains_both_token_and_readiness(self):
        """Result contains BOTH token AND readiness vector"""
        result = SignifierTokenResult(
            signifier_token=SignifierToken(...),
            presyntax_readiness=PreSyntaxMufradVector(...),
            failure=None
        )

        assert result.signifier_token is not None
        assert result.presyntax_readiness is not None

    def test_result_mutual_exclusion(self):
        """Result has exactly one: success OR failure"""
        # Cannot have both success and failure
        with pytest.raises(ValueError):
            SignifierTokenResult(
                signifier_token=SignifierToken(...),
                failure=AlgebraicFailure(...),
                presyntax_readiness=None
            )
```

---

### 6.4 PR Checklist

**What This PR Adds**:
- [x] `SignifierTokenResult` class definition
- [x] `SignifierToken` placeholder (minimal)
- [x] `PreSyntaxMufradVector` placeholder (minimal)
- [x] Constitutional prohibition tests (6 tests minimum)
- [x] Result semantics tests (3 tests minimum)
- [x] Documentation in this spec

**What This PR Does NOT Add**:
- [ ] ~~Complete SignifierToken implementation~~
- [ ] ~~Complete PreSyntaxMufradVector implementation~~
- [ ] ~~Neural encodings~~
- [ ] ~~Tokenizer pipeline~~
- [ ] ~~Operator application logic~~
- [ ] ~~Relation formation~~
- [ ] ~~GARA-T5 components~~

**Acceptance Criteria**:
1. All constitutional prohibition tests pass
2. Result semantics tests pass
3. No semantic/syntax/relation fields in boundary objects
4. Clear documentation of what's deferred

---

## 7. MVP Phase Separation | فصل مراحل MVP

### MVP-0: SignifierTokenResult Boundary (THIS PR)
```
Input:  MufradProof
Process: Wrap in SignifierTokenResult
Output: SignifierTokenResult(
    signifier_token=SignifierToken(proof),
    presyntax_readiness=PreSyntaxMufradVector(proof),
    failure=None
)
```

**Deliverable**: Boundary object + prohibition tests ONLY

---

### MVP-1: PreSyntaxReadiness (FUTURE)
```
Input:  SignifierToken
Process: Construct full PreSyntaxMufradVector with potentials
Output: PreSyntaxReadinessResult
```

**Requires**: CaseSignPotential, FrameCandidate implementations

---

### MVP-2: CaseSignPotential (FUTURE)
```
Input:  PreSyntaxMufradVector
Process: Extract case sign potentials (NOT effects)
Output: CaseSignMatrixResult
```

**Requires**: Bidirectional form analysis

---

### MVP-3: OperatorTrigger (FUTURE)
```
Input:  CaseSignMatrix
Process: Identify operator trigger potentials
Output: OperatorTriggerResult
```

**Requires**: NahwOperatorRegistry integration

---

### MVP-4: RelationAlgebra Boundary (FUTURE)
```
Input:  OperatorCandidate
Process: STOP at RelationAlgebraCore boundary
Output: Error("RelationCandidate requires RelationAlgebraCore activation")
```

**Constitutional Boundary**: No RelationCandidate before this point

---

## 8. Testing Strategy | استراتيجية الاختبار

### 8.1 Constitutional Law Tests (Required)

Each prohibition must have executable test:

1. **No Semantic Leak**
   ```python
   def test_no_meaning_in_signifier()
   def test_no_murad_in_signifier()
   def test_no_ifadah_in_presyntax()
   ```

2. **No Syntax Roles Before Governance**
   ```python
   def test_no_faail_in_presyntax()
   def test_no_syntax_role_in_potential()
   ```

3. **No Case Effects Before Operators**
   ```python
   def test_no_case_effect_in_potential()
   def test_case_potential_not_case_effect()
   ```

4. **No Applied Operators Before Selection**
   ```python
   def test_no_applied_operator_in_trigger()
   def test_trigger_potential_not_applied()
   ```

5. **No Relations Before Algebra**
   ```python
   def test_no_relation_in_operator_candidate()
   def test_operator_candidate_not_relation()
   ```

6. **No RelationCandidate Before Core**
   ```python
   def test_no_relation_candidate_in_gara_ft_0()
   def test_relation_requires_algebra_core()
   ```

---

### 8.2 Anti-Axiom Tests (Future)

Prevent architectural violations:

```python
def test_mufrad_proof_not_neural_token():
    """MufradProof does NOT become Neural token directly"""
    proof = MufradProof(...)

    # Should not have neural encoding
    assert not hasattr(proof, 'neural_embedding')
    assert not hasattr(proof, 'encoder_hidden_state')

def test_presyntax_vector_is_readiness_not_token():
    """PreSyntaxMufradVector is ReadinessVector, not Token"""
    vector = PreSyntaxMufradVector(...)

    # Is readiness interface
    assert hasattr(vector, 'case_sign_potentials')

    # Is NOT operational token
    assert not isinstance(vector, SignifierToken)
```

---

## 9. Integration with Existing Infrastructure | التكامل مع البنية الموجودة

### 9.1 MufradProof Integration

**Existing**: `src/dal_core/mufrad_proof.py` (476 lines)

**Integration Point**:
```python
from dal_core.mufrad_proof import MufradProof

def create_signifier_token_result(
    proof: MufradProof
) -> SignifierTokenResult:
    """
    Convert MufradProof to SignifierTokenResult.

    Constitutional guarantee:
    - No semantic leak
    - No syntax roles
    - No case effects
    - No relations
    """
    # Validate proof satisfies constitutional laws
    if not _validate_constitutional_compliance(proof):
        return SignifierTokenResult(
            signifier_token=None,
            presyntax_readiness=None,
            failure=AlgebraicFailure(...)
        )

    # Construct token
    token = SignifierToken(
        proof=proof,
        identity=proof.identity,
        form_variants=proof.get_bidirectional_forms()
    )

    # Construct readiness (minimal for now)
    readiness = PreSyntaxMufradVector(
        proof=proof,
        case_sign_potentials=(),  # Empty for now
        frame_candidates=()        # Empty for now
    )

    return SignifierTokenResult(
        signifier_token=token,
        presyntax_readiness=readiness,
        failure=None
    )
```

---

### 9.2 PathAwareIdentityValidator Integration

**Existing**: `src/dal_core/path_aware_identity_validator.py`

**Integration Point**:
```python
from dal_core.path_aware_identity_validator import PathAwareIdentityValidator

def _validate_licensed_identity(identity: DalIdentity) -> None:
    """Ensure identity follows licensed paths"""
    validator = PathAwareIdentityValidator()

    if not validator.is_valid_identity_path(identity):
        raise ConstitutionalViolation(
            f"Identity {identity} not on licensed path"
        )
```

---

### 9.3 AlgebraicFailure Integration

**Existing**: `src/dal_core/dal_algebra.py`

**Integration Point**:
```python
from dal_core.dal_algebra import AlgebraicFailure

# Result wraps AlgebraicFailure
SignifierTokenResult(
    signifier_token=None,
    presyntax_readiness=None,
    failure=AlgebraicFailure(
        domain=DalTransitionDomain.CONSTRUCTION,
        reason="Constitutional violation: semantic leak detected"
    )
)
```

---

## 10. Documentation Requirements | متطلبات التوثيق

### 10.1 Code Documentation

Every class must document:
1. Constitutional position (what it IS and what it IS NOT)
2. Allowed fields (whitelist)
3. Forbidden fields (blacklist)
4. Integration points

Example:
```python
@dataclass(frozen=True)
class SignifierToken:
    """
    الدال الوظيفي - Operational Signifier Unit

    Constitutional Position:
    ----------------------
    - IS: Operational unit with licensed identity
    - IS: Wrapper around MufradProof
    - IS: Input to PreSyntaxReadiness layer

    - IS NOT: Neural encoding
    - IS NOT: Syntax node
    - IS NOT: Applied operator
    - IS NOT: Relation participant

    Allowed Fields:
    --------------
    - proof: MufradProof (evidence)
    - identity: DalIdentity (licensed)
    - form_variants: tuple[str] (bidirectional)

    Forbidden Fields:
    ----------------
    - meaning, murad, madlul (semantic)
    - syntax_role, faail, mafool (syntax)
    - case_effect, raf, nasb (governance)
    - relation, isn, tadmin (composition)
    """
```

---

### 10.2 Test Documentation

Every test must document:
1. Constitutional law being tested
2. Violation scenario
3. Expected behavior

Example:
```python
def test_signifier_token_forbids_meaning():
    """
    Constitutional Law: No Semantic Leak in Signifier Layer

    Violation: Attempting to add 'meaning' field to SignifierToken

    Expected: AttributeError or ConstitutionalViolation

    Rationale: SignifierToken represents الدال (signifier) only,
               not المدلول (signified). Meaning assignment requires
               DalMadlulContract which doesn't exist yet.
    """
```

---

## 11. Future Work Roadmap | خريطة العمل المستقبلي

### Phase 0: Boundary Establishment (THIS DOCUMENT)
- [x] Define ontological distinctions
- [x] Establish constitutional prohibitions
- [x] Propose SignifierTokenResult PR
- [ ] Get approval for boundary spec
- [ ] Implement minimal SignifierTokenResult
- [ ] Add constitutional tests

### Phase 1: VerbalSignifiedCandidate Foundation (FUTURE)
**Requires**:
- [ ] WadhEvidence infrastructure
- [ ] UsageEvidence infrastructure
- [ ] DalalahPath definition
- [ ] DalMadlulContract specification

**Deliverable**: Link between الدال and المدلول اللفظي

---

### Phase 2: PreSyntaxReadiness Full Implementation (FUTURE)
**Requires**:
- [ ] Complete CaseSignPotential implementation
- [ ] Complete SentenceFrameCandidate implementation
- [ ] Complete OperatorTriggerPotential implementation

**Deliverable**: Full PreSyntaxMufradVector with potentials

---

### Phase 3: RelationAlgebraCore Activation (FUTURE)
**Requires**:
- [ ] OperatorCandidate selection mechanism
- [ ] RelationAlgebraCore integration
- [ ] RelationCandidate production (5 types: ISN/TADMIN/TAQYID/WASF/IDAFAH)

**Deliverable**: Licensed relation formation

---

### Phase 4: Neural Integration (DISTANT FUTURE)
**Requires**:
- [ ] All algebraic layers complete
- [ ] GARA-T5 architecture specification
- [ ] AlgebraicToken → NeuralEmbedding bridge

**Deliverable**: GARA-T5 Neural-Algebraic Model

---

## 12. Conclusion | الخلاصة

### 12.1 What This Specification Establishes

1. **Clear Ontology**: 8 distinct types with operational definitions
2. **Constitutional Boundaries**: 6 prohibition laws with tests
3. **Scope Limitation**: GARA-FT-0 handles MufradProof → SignifierTokenResult ONLY
4. **Integration Points**: Clear connection to existing dal_core infrastructure
5. **Future Roadmap**: 4 phases with explicit dependencies

### 12.2 What This Specification Defers

1. **VerbalSignifiedCandidate**: Requires WadhEvidence/UsageEvidence
2. **Complete Tokenizer Hierarchy**: 11-level tokenizer deferred
3. **Neural Components**: GARA-T5 deferred to distant future
4. **Relation Formation**: Requires RelationAlgebraCore activation
5. **Full PreSyntax Chain**: Deferred to MVP-1, MVP-2, MVP-3

### 12.3 Next Immediate Step

**Action**: Propose PR for SignifierTokenResult boundary object

**Files**:
- `src/dal_core/signifier_token_result.py`
- `tests/test_signifier_token_result.py`

**Scope**: Boundary + prohibition tests ONLY

**No**: Neural code, complete tokenizer, operator application, relation formation

---

**Document Status**: READY FOR REVIEW
**Implementation Status**: BLOCKED ON APPROVAL
**Next Action**: Await user feedback on boundary specification

---

## Appendix A: Forbidden Fields Registry | سجل الحقول المحظورة

From `operator_candidate.py:67`:

```python
_FORBIDDEN_FIELDS: frozenset[str] = frozenset({
    # Applied operators (not candidates)
    "operator", "operator_id", "operator_binding", "applied_operator",

    # Relations (require RelationAlgebraCore)
    "relation", "relation_type", "relation_binding",

    # Case effects (require governance)
    "case_effect", "syntax_role",

    # Specific syntax roles
    "faail", "mafool", "mubtada", "khabar",

    # Governance markers
    "marfoo_by", "mansub_by", "majroor_by",
    "governed_by", "governs",

    # Semantic fields
    "meaning", "semantic", "madlul", "murad",

    # 67 total forbidden fields
    # See operator_candidate.py for complete list
})
```

---

## Appendix B: References | المراجع

1. `docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md` - Dal position document
2. `docs/BIDIRECTIONAL_ANALYSIS_CHARTER.md` - Bidirectional analysis
3. `docs/PRESYNTAX_INTERFACE.md` - PreSyntax interface
4. `src/dal_core/mufrad_proof.py` - MufradProof implementation (476 lines)
5. `src/dal_core/operator_candidate.py` - OperatorCandidate (721 lines)
6. `src/dal_core/path_aware_identity_validator.py` - Identity validation
7. `src/dal_core/relation_algebra_core.py` - Relation algebra foundation

---

**END OF SPECIFICATION**
