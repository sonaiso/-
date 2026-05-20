# Dal Algebra Signature

**PR #23**: Minimal Dal Transition Signature
**Status**: Lightweight runtime foundation
**Created**: 2026-05-20

---

## Executive Summary

This PR implements a **minimal licensed-transition signature** for future dal candidate layers.

**It does NOT implement full Dal Algebra.**

This is the first lightweight runtime foundation after:
- PR #21: Ordered Dal Form Governance
- PR #22: Project Algebra Architecture Map

---

## What This PR Implements

### Core Types

1. **DalTransitionDomain** (enum)
   - 8-layer domain architecture (D0-D7)
   - GRAPHOPHONEMIC, SYLLABIC, PRE_MORPH, ORIGIN, TEMPLATE, IDENTITY_AXIS, DIRECTIONAL_ANALYSIS, JUDGMENT

2. **DalClaimScope** (enum)
   - Claim-scoped certificates (no global certificate)
   - CARRIER_VALID, ATOM_SEQUENCE_VALID, SYLLABLE_STRUCTURE_VALID, etc.

3. **Policy Enums**
   - EvidenceRequirement
   - ShortcutPolicy
   - CandidateBudgetPolicy

4. **Evidence Model**
   - `DalEvidence` (dataclass)
   - `DalCounterEvidence` (dataclass)
   - `DalTraceRef` (dataclass)

5. **Contracts and Protocols**
   - `DalTransitionContract` (dataclass)
   - `DalCandidateProtocol` (protocol)
   - `DalCandidateSetProtocol` (protocol)
   - `DalTransitionProtocol` (protocol)

6. **Validation Helpers**
   - `validate_transition_contract()`
   - `validate_candidate_set_shape()`
   - `ensure_no_forbidden_outputs()`
   - `validate_no_direct_promotion()`

---

## Obeys PR #21: Ordered Dal Form Governance

This implementation enforces all PR #21 principles:

```text
✅ A dal form is an ordered bounded sequence, not a bag of features
✅ No claim without position (evidence requires span)
✅ No fold without reverse trace (DalTraceRef.reversible)
✅ No adjacency without direction (ordered domains D0-D7)
✅ No candidate without boundaries (CandidateSet validation)
✅ No certificate without claim-scoped evidence (DalClaimScope)
```

---

## Obeys PR #22: Project Algebra Architecture Map

This implementation enforces all PR #22 principles:

```text
✅ 𝔾 = successful typed objects
✅ Failure ∉ 𝔾
✅ Transitions return CandidateSet[𝔾] or Failure
✅ No algebra may claim outputs of later algebra
```

### Pre-Semantic Boundary

All `DalTransitionDomain` values are **pre-semantic** (form analysis only):

```text
D0-D7: Form analysis only
A5+: Semantic analysis (not in this PR)
```

No semantic claim scopes exist in `DalClaimScope`:

```text
❌ MEANING_DETERMINED
❌ MURAD_INFERRED
❌ HUKM_ISSUED
❌ SEMANTIC_RELATION_IDENTIFIED
```

---

## 8-Layer Transition Domain Architecture

### D0: GRAPHOPHONEMIC (رسم/صوت)

**Purpose**: Carrier → Atom transition

**Input**: Unicode sequence
**Output**: ArabicAtom sequence
**Claim**: CARRIER_VALID, ATOM_SEQUENCE_VALID

---

### D1: SYLLABIC (مقطع)

**Purpose**: Atom → Syllable transition

**Input**: ArabicAtom sequence
**Output**: Syllable structure
**Claim**: SYLLABLE_STRUCTURE_VALID

---

### D2: PRE_MORPH (ما قبل الصرف)

**Purpose**: Pre-morphological classification

**Input**: Syllable structure
**Output**: Pre-morph classification
**Claim**: (Pre-morphological boundaries)

---

### D3: ORIGIN (أصل)

**Purpose**: Origin classification

**Input**: Pre-morph structure
**Output**: Root/frozen/functional classification
**Claim**: ORIGIN_CLASSIFIED

**Types**:
- Root-derived (مشتق)
- Frozen (جامد)
- Functional/particle (وظيفي)

---

### D4: TEMPLATE (وزن)

**Purpose**: Pattern matching

**Input**: Origin classification
**Output**: Template/pattern candidates
**Claim**: TEMPLATE_MATCHED

---

### D5: IDENTITY_AXIS (محور الهوية)

**Purpose**: Ism/Fi'l/Harf classification

**Input**: Template candidates
**Output**: Identity axis classification
**Claim**: IDENTITY_DETERMINED

---

### D6: DIRECTIONAL_ANALYSIS (تحليل اتجاهي)

**Purpose**: Bidirectional form analysis

**Input**: Identity classification
**Output**: Forward/backward analysis
**Claim**: FORM_ANALYZED

---

### D7: JUDGMENT (حكم صرفي)

**Purpose**: Morphological judgment

**Input**: Directional analysis
**Output**: Final form judgment
**Claim**: JUDGMENT_ISSUED

---

## Partial Transition Network

**Critical**: This is a **partial transition network** (شبكة انتقالات جزئية), **not a single pipeline**.

Different words follow different paths:

```text
Root-derived word:
  D0 → D1 → D2 → D3 → D4 → D5 → D6 → D7

Functional particle:
  D0 → D1 → D3 → D5 (shortcut via closed-class lexicon)

Frozen word:
  D0 → D1 → D2 → D3 → D5 → D7 (no template matching)

Unresolved:
  D0 → D1 → D2 → (unresolved candidate set)
```

---

## No-Direct-Promotion Rules

### Prohibited Cross-Layer Promotions

Without intermediate contract, trace, or explicit shortcut:

```text
❌ GRAPHOPHONEMIC → TEMPLATE (رسم/صوت → وزن)
❌ GRAPHOPHONEMIC → ORIGIN (رسم/صوت → أصل)
❌ GRAPHOPHONEMIC → IDENTITY_AXIS (رسم/صوت → محور)
❌ SYLLABIC → TEMPLATE (مقطع → وزن)
❌ SYLLABIC → ORIGIN (مقطع → أصل)
❌ PRE_MORPH → IDENTITY_AXIS (ما قبل الصرف → محور)
```

### Allowed Promotions

1. **Adjacent transitions** (D0→D1, D1→D2, etc.)
2. **With intermediate trace**
3. **With closed-class lexicon shortcut**
4. **With explicit attestation**

### Categorical Bans — Mufrad Judicial Axes (PR-A → PR-G)

In addition to the trace-conditional rules above, two promotions are
**categorically forbidden** regardless of trace, shortcut, or
attestation. These cover the historical hallucination of inferring the
binaa/i'rab judgment from descriptive syllable counts:

```text
🚫 SYLLABIC → BINAA_JUDGMENT     (عدد المقاطع → بناء/إعراب) — ممنوع بلا استثناء
🚫 SYLLABIC → ISHTIQAQ_JUDGMENT  (عدد المقاطع → جامد/مشتق) — ممنوع بلا استثناء
```

Enforced at runtime by `FORBIDDEN_AXIS_PROMOTIONS` and
`assert_axis_promotion_allowed()` in `dal_core.dal_algebra`. The binaa
and ishtiqaq judgments emerge from `D5 IDENTITY_AXIS` + D3/D4
(origin/template) only — never from D1. See [`MUFRAD_AXES.md`](MUFRAD_AXES.md)
§8 for the full rationale.

---

## Shortcut Policies

### ShortcutPolicy.FORBIDDEN

No shortcuts allowed. All transitions must go through intermediate layers.

### ShortcutPolicy.CLOSED_CLASS_ONLY

Shortcuts allowed only for closed-class items (particles, pronouns, etc.) with lexicon attestation.

**Example**:
```python
contract = DalTransitionContract(
    contract_id="particle-shortcut",
    source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
    target_domain=DalTransitionDomain.IDENTITY_AXIS,
    shortcut_policy=ShortcutPolicy.CLOSED_CLASS_ONLY,
    lexicon_requirement=True
)
```

### ShortcutPolicy.WITH_ATTESTATION

Shortcuts allowed with explicit attestation evidence.

### ShortcutPolicy.ALLOWED

Shortcuts generally allowed (use with caution).

---

## Evidence Model

### DalEvidence

**Required fields**:
- `source`: Evidence source (lexicon, rule, observation)
- `claim_scope`: Scope of this evidence
- `span`: Position span `(start, end)` in ordered sequence
- `confidence`: [0.0, 1.0]

**Critical**: Evidence **must** include `span` (position in ordered sequence).

**Example**:
```python
evidence = DalEvidence(
    source="lexicon:seed",
    claim_scope=DalClaimScope.TEMPLATE_MATCHED,
    span=(0, 3),
    confidence=0.95,
    details={"pattern": "فَعَلَ", "root": "ك-ت-ب"}
)
```

### DalCounterEvidence

Counter-evidence against a claim, with severity [0.0, 1.0].

### DalTraceRef

Transformation trace reference with reversibility flag.

**Example**:
```python
trace = DalTraceRef(
    transition_id="origin-to-template",
    source_domain=DalTransitionDomain.ORIGIN,
    target_domain=DalTransitionDomain.TEMPLATE,
    timestamp="2026-05-20T00:00:00Z",
    reversible=True
)
```

---

## Claim-Scoped Certificates

### No Global Certificate

There is **no global certificate** that works across all domains.

All certificates are **claim-scoped**:

```python
✅ CARRIER_VALID           # Unicode carrier is valid
✅ ATOM_SEQUENCE_VALID     # Atom sequence is well-formed
✅ SYLLABLE_STRUCTURE_VALID # Syllable structure is valid
✅ ORIGIN_CLASSIFIED       # Origin is classified
✅ TEMPLATE_MATCHED        # Template matched
✅ IDENTITY_DETERMINED     # Identity axis determined
✅ FORM_ANALYZED           # Form analysis complete
✅ JUDGMENT_ISSUED         # Morphological judgment issued

# Composition claims (dal-murakkab)
✅ FRAME_STRUCTURE_VALID   # Sentence frame valid
✅ CASE_SIGNS_OBSERVED     # Surface case signs observed
✅ OPERATOR_TRIGGERED      # Operator trigger identified

# FORBIDDEN
❌ MEANING_DETERMINED
❌ MURAD_INFERRED
❌ HUKM_ISSUED
```

---

## Transition Contract

### DalTransitionContract Fields

**Required**:
- `contract_id`: Unique identifier
- `source_domain`: Source DalTransitionDomain
- `target_domain`: Target DalTransitionDomain
- `input_type`: Expected input type
- `output_type`: Expected output type
- `claim_scope`: Scope of certificate

**Requirements**:
- `evidence_requirement`: EvidenceRequirement enum
- `lexicon_requirement`: bool
- `context_requirement`: bool

**Policies**:
- `shortcut_policy`: ShortcutPolicy enum
- `candidate_budget_policy`: CandidateBudgetPolicy enum
- `candidate_budget_limit`: Optional[int]

**Forbidden outputs**:
- `forbidden_output_types`: Set[type] (prevent semantic leakage)

**Flags**:
- `allows_unresolved`: bool
- `hypothesis_only`: bool

### Example

```python
contract = DalTransitionContract(
    contract_id="syllable-to-promorph",
    source_domain=DalTransitionDomain.SYLLABIC,
    target_domain=DalTransitionDomain.PRE_MORPH,
    input_type=list,
    output_type=dict,
    claim_scope=DalClaimScope.ORIGIN_CLASSIFIED,
    evidence_requirement=EvidenceRequirement.TRACE,
    shortcut_policy=ShortcutPolicy.FORBIDDEN,
    candidate_budget_policy=CandidateBudgetPolicy.MEDIUM,
    forbidden_output_types={MeaningType, MuradType},
    allows_unresolved=True
)
```

---

## Protocols (Duck-Typed Interfaces)

### DalCandidateProtocol

Structural typing for dal candidates:

```python
@property
def candidate_id(self) -> str: ...

@property
def domain(self) -> DalTransitionDomain: ...

@property
def evidence(self) -> List[DalEvidence]: ...

@property
def counter_evidence(self) -> List[DalCounterEvidence]: ...
```

### DalCandidateSetProtocol

Structural typing for candidate sets:

```python
@property
def claim_scope(self) -> DalClaimScope: ...

@property
def candidates(self) -> List[T]: ...

@property
def evidence(self) -> List[DalEvidence]: ...

@property
def counter_evidence(self) -> List[DalCounterEvidence]: ...

@property
def trace(self) -> List[DalTraceRef]: ...
```

### DalTransitionProtocol

Structural typing for transitions:

```python
@property
def contract(self) -> DalTransitionContract: ...

def apply(self, input_obj: Any, **aux) -> DalCandidateSetProtocol[T]: ...
```

**Critical**: Protocols do **not force existing classes to inherit**. They provide duck-typed interfaces.

---

## Validation Helpers

### validate_transition_contract()

Validates transition contract invariants:
- Source ≠ target
- Custom budget policy has limit
- No forbidden direct promotions

### validate_candidate_set_shape()

Validates candidate set shape:
- No `None` candidates
- Finite candidate set

### ensure_no_forbidden_outputs()

Prevents semantic leakage:
- Checks object type against forbidden set
- Checks object fields against forbidden set

### validate_no_direct_promotion()

Validates direct promotion justification:
- Adjacent transitions allowed
- Non-adjacent requires trace/shortcut/attestation

---

## Out of Scope

This PR **does NOT implement**:

```text
❌ Rank Algebra (PR #24)
❌ Residual Algebra (PR #25)
❌ CandidateSet base migration (PR #26)
❌ NoMeaning scanner (PR #27)
❌ RelationCandidate (PR #37)
❌ CaseEffectCandidate (PR #38)
❌ MurakkabProof (PR #39)
❌ Wadh' Contract runtime (PR #40-42)
❌ Dalalah runtime (PR #44)
❌ Meaning/Murad/Hukm (A6-A10)
❌ Full analyzers or generators
❌ Semantic linking
```

---

## Allowed Claim After This PR

```text
dal_core has a minimal licensed-transition signature for future dal candidate layers.
```

## Forbidden Claim After This PR

```text
dal_core has complete Dal Algebra.
dal_core has full rank algebra.
dal_core has full residual algebra.
dal_core performs relation analysis.
dal_core performs i'rab.
dal_core understands meaning.
```

---

## Next Steps

After PR #23:

- **PR #24**: Rank Algebra
- **PR #25**: Residual Algebra
- **PR #26**: CandidateSet Contract
- **PR #27**: Stage-Aware NoMeaning Invariant
- **PR #28-36**: Dal candidate layers (D0-D7)
- **PR #37**: RelationCandidate
- **PR #38**: CaseEffectCandidate
- **PR #39**: MurakkabProof closure

---

**Version**: 1.0.0
**Status**: Minimal signature complete
**Scope**: Runtime foundation only (no full algebra)
