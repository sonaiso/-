# U₁₀ WordFormCandidateCarrier Constitutional Specification

**Date:** 2026-05-26
**Status:** 🔧 DESIGN SPECIFICATION (Not Yet Implemented)
**Prerequisite:** U₉ WeightCandidateCarrier (✅ Closed)
**Branch:** `claude/update-u9-constitution-status`

---

## Executive Summary

**U₁₀ WordFormCandidateCarrier** is the governed word form layer that carries the linguistic structure produced after preserved WEIGHT_IDENTITY from U₉.

### Core Principle

```
لا معنى بعد الوزن حتى تثبت صورة الكلمة.
No semantic transition before governed WordFormCandidate.
```

U₁₀ is the necessary intermediate layer between morphological weight (U₉) and semantic/syntactic interpretation (U₁₁+). It **prevents direct jumps from weight to meaning**.

---

## Naming Rationale

### Why "WordFormCandidateCarrier" (Not "FormCandidateCarrier")

**Rejected:** `FormCandidateCarrier`
- "Form" is ambiguous
- Could imply semantic form (صورة دلالية)
- Could imply general structure without specificity

**Accepted:** `WordFormCandidateCarrier`
- "WordForm" is specific to linguistic/morphological structure
- Clear distinction from semantic form
- Maintains focus on lexical level (not phrasal/sentential)
- Aligns with morphological domain (not semantic domain)

---

## Constitutional Position

### Layer Definition

**U₁₀:** WordFormCandidateCarrier (حامل مرشح صورة الكلمة)

**Transition:**
```
U₉ (WeightCandidate) → U₁₀ (WordFormCandidate)
```

**Domain:** WORDFORM_DOMAIN (new domain between WEIGHT and SEMANTIC)

**Identity:**
- **Input:** WEIGHT_IDENTITY (from U₉)
- **Output:** WORDFORM_IDENTITY (new identity type)

---

## Purpose and Non-Purpose

### U₁₀ Purpose (What It DOES)

- ✓ **Carries word form structure** after weight determination
- ✓ **Preserves WEIGHT_IDENTITY** from U₉ in trace
- ✓ **Maintains governed transition** under ApprovedTransitionContext
- ✓ **Prevents weight→meaning bypass** by existing as mandatory intermediate
- ✓ **Produces ranked candidates** (not certificates)
- ✓ **Preserves residual audit** from upstream layers

### U₁₀ Non-Purpose (What It DOES NOT Do)

- ✗ **Does NOT determine meaning** (معنى)
- ✗ **Does NOT assign syntactic role** (دور نحوي)
- ✗ **Does NOT produce ṣifah** (صفة)
- ✗ **Does NOT produce hukm** (حكم)
- ✗ **Does NOT perform i'rab** (إعراب)
- ✗ **Does NOT determine semantic derivation** (اشتقاق معنوي)

---

## Constitutional Laws (القوانين الدستورية)

### Arabic Formulation

```
لا U₁₀ بلا WEIGHT_IDENTITY محفوظة.
ولا U₁₀ بلا ApprovedTransitionContext.
ولا صورة كلمة بلا وزن محفوظ.
ولا انتقال من الوزن إلى المعنى مباشرة.
ولا معنى بلا WordForm محفوظة.
```

### English Translation

1. **No U₁₀ without preserved WEIGHT_IDENTITY**
   Input must contain valid WEIGHT_IDENTITY from U₉.

2. **No U₁₀ without ApprovedTransitionContext**
   U₁₀ operates under AlgebraicDecisionCore governance.

3. **No word form without preserved weight**
   Word form candidates must trace to weight candidates.

4. **No transition from weight to meaning directly**
   U₁₀ exists as mandatory layer preventing bypass.

5. **No meaning without preserved WordForm**
   Downstream semantic layers must consume WordForm, not Weight.

---

## Domain Definition

### New Domain: WORDFORM_DOMAIN

**Position:** Between WEIGHT_DOMAIN and SEMANTIC_DOMAIN

**Scope:**
- Word-level morphological structure
- Lexical form after weight application
- Surface realization of weight pattern
- NOT semantic interpretation
- NOT syntactic function
- NOT grammatical judgment

**Forbidden Outputs:**
- SEMANTIC_IDENTITY
- HUKM_IDENTITY
- FUNCTIONAL_RELATION_IDENTITY
- IRAB_IDENTITY
- MEANING_IDENTITY

**Required Trace:**
- WEIGHT_IDENTITY (input from U₉)
- U₇-C agreement edges (external trace)
- Residual audit from upstream

---

## Data Structures

### WordFormCandidateUnit

```python
@dataclass(frozen=True)
class WordFormCandidateUnit:
    """
    Single word form candidate unit.

    Represents one possible word form realization after weight application.
    Does NOT contain semantic interpretation.
    """
    unit_id: str
    source_weight_unit_id: str  # Trace to U₉

    # Word form structure (morphological, not semantic)
    surface_form: str  # Resulting surface word
    internal_structure: Tuple[str, ...]  # Morpheme boundaries

    # Preserved trace from U₉
    weight_identity: IdentityType  # Must be WEIGHT_IDENTITY
    weight_pattern: str  # E.g., "فَعَلَ", "فَاعِل"

    # Preserved trace from U₇-C (external)
    agreement_edge_ids: FrozenSet[str]

    # Candidate metadata (not certificate)
    rank: Rank
    residuals: Tuple[Residual, ...]

    # Constitutional guards
    def __post_init__(self):
        """Validate constitutional constraints."""
        if self.weight_identity not in {
            IdentityType.WEIGHT_IDENTITY
        }:
            raise ValueError(
                f"WordFormCandidate must have WEIGHT_IDENTITY, "
                f"got {self.weight_identity}"
            )
```

### WordFormCandidateResult

```python
@dataclass(frozen=True)
class WordFormCandidateResult:
    """
    Result of U₁₀ execution.

    Contains ranked word form candidates with preserved weight trace.
    """
    result_id: str
    source_layer: ExecutionLayer  # Must be U9_WEIGHT
    target_layer: ExecutionLayer  # Must be U10_WORD_FORM

    # Candidates (ranked, not certified)
    candidates: Tuple[WordFormCandidateUnit, ...]

    # Governance context
    approved_context: ApprovedTransitionContext

    # Audit trail
    residual_audit: Tuple[Residual, ...]
    execution_trace: Tuple[str, ...]  # Layer IDs traversed
```

---

## Constitutional Test Specification

### 11 Required Tests

All tests must pass before U₁₀ can be considered constitutionally implemented.

#### 1. Governance Tests (2 tests)

**Test 1:** `test_u10_rejects_without_approved_transition_context`
- **Law:** لا U₁₀ بلا ApprovedTransitionContext
- **Verify:** U₁₀ raises `ValueError` when called without context
- **Expected:** Exception with message about missing governance

**Test 2:** `test_u10_rejects_context_not_for_u9_to_u10`
- **Law:** Context must be for U₉→U₁₀ transition
- **Verify:** U₁₀ rejects context for U₈→U₉ or other transitions
- **Expected:** Exception with message about wrong transition

---

#### 2. Input Validation Tests (1 test)

**Test 3:** `test_u10_rejects_missing_weight_identity`
- **Law:** لا صورة كلمة بلا وزن محفوظ
- **Verify:** U₁₀ rejects input without WEIGHT_IDENTITY
- **Expected:** Exception when input has PHONETIC_IDENTITY or other non-weight

---

#### 3. Forbidden Output Tests (3 tests)

**Test 4:** `test_u10_rejects_semantic_identity_output`
- **Law:** No SEMANTIC_IDENTITY output
- **Verify:** Context claiming SEMANTIC_IDENTITY output is rejected
- **Expected:** Exception - word form ≠ semantic meaning

**Test 5:** `test_u10_rejects_hukm_identity_output`
- **Law:** No HUKM_IDENTITY output
- **Verify:** Context claiming HUKM_IDENTITY output is rejected
- **Expected:** Exception - word form ≠ grammatical judgment

**Test 6:** `test_u10_rejects_syntactic_role_output`
- **Law:** No FUNCTIONAL_RELATION_IDENTITY output
- **Verify:** Context claiming syntactic role output is rejected
- **Expected:** Exception - word form ≠ syntactic function

---

#### 4. Trace Preservation Tests (3 tests)

**Test 7:** `test_u10_preserves_weight_trace`
- **Law:** Preserve WEIGHT_IDENTITY in trace
- **Verify:** Output contains source_weight_unit_id and weight_identity
- **Expected:** Complete trace to U₉ weight candidate

**Test 8:** `test_u10_preserves_u7c_agreement_edges_as_external_trace`
- **Law:** U₇-C agreement edges preserved externally
- **Verify:** agreement_edge_ids present in output (not consumed)
- **Expected:** Agreement edges available for downstream layers

**Test 9:** `test_u10_preserves_residual_audit`
- **Law:** Residuals from upstream preserved
- **Verify:** residual_audit contains upstream residuals
- **Expected:** Complete residual chain maintained

---

#### 5. Rank Tests (1 test)

**Test 10:** `test_u10_preserves_candidate_rank`
- **Law:** Output is candidate (ranked), not certificate
- **Verify:** Result contains Rank, not Certainty
- **Expected:** rank field present, no certificate claim

---

#### 6. Golden Path Test (1 test)

**Test 11:** `test_u10_golden_path_word_form_candidate`
- **Law:** Full execution with valid governance
- **Setup:**
  1. Create valid U₉ WeightCandidateResult
  2. Request U₉→U₁₀ transition from AlgebraicDecisionCore
  3. Receive approved DecisionAudit
  4. Create ApprovedTransitionContext
  5. Execute word_form_candidate_carrier_10()
- **Verify:**
  - Execution succeeds
  - Output contains WordFormCandidateResult
  - WEIGHT_IDENTITY preserved
  - No semantic/syntactic/hukm identities
  - Rank preserved
  - Residuals preserved
- **Expected:** Complete governed execution produces valid word form candidates

---

## Execution Pattern

### Canonical Flow

```python
# Step 1: Pipeline owns AlgebraicDecisionCore
governor = AlgebraicDecisionCore(...)

# Step 2: Request transition approval
audit = governor.decide_transition(
    from_layer=ExecutionLayer.U9_WEIGHT,
    to_layer=ExecutionLayer.U10_WORD_FORM,
    input_identity=IdentityType.WEIGHT_IDENTITY,
    output_identity=IdentityType.WORDFORM_IDENTITY,
    domain=DomainType.WORDFORM_DOMAIN,
    evidence=...,
    residuals=...,
)

# Step 3: Check approval
if audit.status != CPBStatus.APPROVED:
    raise ValueError("U₉→U₁₀ transition not approved")

# Step 4: Create approved context
context = create_approved_context(audit)

# Step 5: Execute U₁₀
result = word_form_candidate_carrier_10(
    u9_input=weight_candidate_result,
    approved_context=context,
)

# Step 6: Use result (NOT for direct semantic interpretation)
# Must pass through U₁₁+ for semantic analysis
```

---

## Architectural Significance

### Why U₁₀ Matters

**Prevents Direct Weight→Meaning Jump:**
```
❌ FORBIDDEN:
U₉ WeightCandidate → U₁₁ SemanticInterpretation

✅ REQUIRED:
U₉ WeightCandidate → U₁₀ WordFormCandidate → U₁₁ SemanticInterpretation
```

**Establishes Layer Discipline:**
- Each layer adds ONE dimension
- No layer can be skipped
- Governance applies at every transition
- Trace preservation is mandatory

**Architectural Integrity:**
- U₉ produces weight patterns (morphological templates)
- U₁₀ realizes word forms (lexical structures)
- U₁₁+ interprets meaning (semantic/syntactic)

Each domain is distinct and cannot be conflated.

---

## Implementation Checklist

### Phase 1: Foundation
- [ ] Add `U10_WORD_FORM` to `ExecutionLayer` enum
- [ ] Add `WORDFORM_DOMAIN` to `DomainType` enum
- [ ] Add `WORDFORM_IDENTITY` to `IdentityType` enum
- [ ] Update `DESIGN_LAYERS` in execution_layer_registry.py
- [ ] Update allowed transitions: `U9_WEIGHT → U10_WORD_FORM`

### Phase 2: Data Structures
- [ ] Create `u10_word_form_candidate_carrier.py`
- [ ] Implement `WordFormCandidateUnit` dataclass
- [ ] Implement `WordFormCandidateResult` dataclass
- [ ] Implement `validate_approved_context_for_u10()` function

### Phase 3: Core Logic
- [ ] Implement `word_form_candidate_carrier_10()` function
- [ ] Add constitutional validation (11 laws)
- [ ] Implement weight trace preservation
- [ ] Implement agreement edge preservation
- [ ] Implement residual audit chain

### Phase 4: Testing
- [ ] Create `test_u10_word_form_candidate_constitutional.py`
- [ ] Implement all 11 constitutional tests
- [ ] Verify 11/11 tests passing
- [ ] Add golden path integration test

### Phase 5: Integration
- [ ] Export from `dal_core/__init__.py`
- [ ] Update documentation
- [ ] Store architectural memory
- [ ] Create closure document when complete

---

## Domain Hierarchy

```
U₀  Unicode
U₁  Grapheme
U₂p PhoneticProjection
U₂s ArabicSyllable
U₃  BoundaryAndAttachment
U₄  TrueSingularLafẓ
U₅  FunctionalRole
U₆  MabniClosedClass
U₇  PreWeightContract (A/B/C sublayers)
U₈  RootStem
U₉  Weight              ← CLOSED CONSTITUTIONALLY
U₁₀ WordForm            ← THIS LAYER (design specification)
U₁₁ LexicalEntry        ← Future semantic layer
U₁₂ MorphosyntacticFeature
U₁₃ PhraseRelation
U₁₄ SentenceStructure
U₁₅ Dalālah
```

---

## Key Distinctions

| Aspect | U₉ Weight | U₁₀ WordForm | U₁₁+ Semantic |
|--------|-----------|--------------|---------------|
| **Domain** | WEIGHT_DOMAIN | WORDFORM_DOMAIN | SEMANTIC_DOMAIN |
| **Identity** | WEIGHT_IDENTITY | WORDFORM_IDENTITY | SEMANTIC_IDENTITY |
| **Output** | Weight pattern (فَاعِل) | Word form (كَاتِب) | Meaning (doer/agent) |
| **Level** | Morphological template | Lexical realization | Semantic interpretation |
| **Example** | "فَاعِل pattern" | "كَاتِب surface form" | "active participle meaning" |

---

## References

- **U₉ Closure:** `docs/U9_CONSTITUTIONAL_CLOSURE.md`
- **Execution Registry:** `src/dal_core/execution_layer_registry.py`
- **Governance:** `src/dal_core/algebraic_decision_core.py`
- **Approved Context:** `src/dal_core/approved_transition_context.py`
- **Identity Registry:** `src/dal_core/identity_registry.py`
- **Domain Registry:** `src/dal_core/domain_registry.py`

---

## Status

**Current:** Design Specification Only
**Next Step:** Implement Phase 1 (Foundation updates)
**Goal:** Constitutional implementation with 11/11 tests passing

---

**Conclusion:**

U₁₀ WordFormCandidateCarrier is the constitutional layer that prevents direct weight→meaning jumps. It carries the governed word form structure after preserved WEIGHT_IDENTITY, maintaining strict domain boundaries and governance requirements.

No semantic transition before governed WordFormCandidate.
