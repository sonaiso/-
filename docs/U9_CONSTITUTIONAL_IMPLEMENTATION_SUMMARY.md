# U₉ WeightCandidateCarrier Constitutional Implementation

**Date:** 2026-05-26
**Branch:** `claude/implement-u9-weight-candidate-carrier`
**Status:** ✅ Complete (12/12 tests passing)
**PR:** Building on #114 (AlgebraicDecisionCore governance)

---

## Executive Summary

U₉ WeightCandidateCarrier is now fully implemented with complete constitutional governance under AlgebraicDecisionCore. All 12 constitutional tests pass, enforcing the strict architectural laws that prevent layer bypass, domain violations, and identity leaps.

### Key Achievement

**U₉ is the first layer to be implemented AFTER the governance infrastructure**, demonstrating that the constitutional framework works end-to-end:

```
Pipeline/Orchestrator
  └─→ AlgebraicDecisionCore.decide_transition(U₈→U₉)
      └─→ DecisionAudit (approved)
          └─→ create_approved_context(audit)
              └─→ ApprovedTransitionContext
                  └─→ weight_candidate_carrier_9(u8_input, context)
                      └─→ WeightCandidateResult
```

---

## Constitutional Laws Enforced

### Arabic Formulation (الصياغة العربية)

```
لا وزن بلا ApprovedTransitionContext.
ولا ApprovedTransitionContext بلا DecisionAudit مُجاز.
ولا DecisionAudit بلا AlgebraicDecisionCore.
ولا AlgebraicDecisionCore بلا منع قفز، وحفظ رتبة، وحفظ أثر، وحفظ مجال.
```

### English Translation

1. **No weight without ApprovedTransitionContext**
   U₉ MUST reject execution if ApprovedTransitionContext is not provided.

2. **No ApprovedTransitionContext without approved DecisionAudit**
   Context can only be created from approved audit (CPBStatus.APPROVED).

3. **No DecisionAudit without AlgebraicDecisionCore**
   Only AlgebraicDecisionCore can create valid audit through `decide_transition()`.

4. **No AlgebraicDecisionCore without:**
   - **Leap prevention** (لا قفز): Sequential layer progression verified
   - **Rank preservation** (حفظ رتبة): No elevation without evidence
   - **Trace preservation** (حفظ أثر): Complete execution trace maintained
   - **Domain preservation** (حفظ مجال): Domain boundaries enforced

---

## 12 Constitutional Tests (All Passing ✓)

### 1. Governance Requirement Tests

**Test 1:** `test_u9_rejects_without_approved_transition_context`
**Law:** لا وزن بلا ApprovedTransitionContext
**Status:** ✅ PASS
**Verification:** U₉ raises `ValueError` when called without context.

**Test 2:** `test_u9_rejects_direct_algebraic_decision_core_instantiation`
**Law:** U₉ must NOT instantiate AlgebraicDecisionCore internally
**Status:** ✅ PASS
**Verification:** Source code scan confirms no `AlgebraicDecisionCore()` instantiation.

---

### 2. Context Validation Tests

**Test 3:** `test_u9_rejects_context_not_for_u8_to_u9`
**Law:** Context must be for U₈→U₉ transition only
**Status:** ✅ PASS
**Verification:** U₉ rejects context for U₇→U₈ transition.

**Test 4:** `test_u9_rejects_non_weight_domain`
**Law:** Context domain must be WEIGHT_DOMAIN
**Status:** ✅ PASS
**Verification:** U₉ rejects context with SYNTAX_DOMAIN.

**Test 5:** `test_u9_rejects_missing_root_or_stem_identity`
**Law:** Input identity must be ROOT_MATERIAL_IDENTITY or STEM_IDENTITY
**Status:** ✅ PASS
**Verification:** U₉ rejects context with PHONETIC_IDENTITY input.

---

### 3. Forbidden Output Tests

**Test 6:** `test_u9_rejects_semantic_identity_output`
**Law:** No SEMANTIC_IDENTITY output (صيغة فاعل ≠ معنى الفاعلية)
**Status:** ✅ PASS
**Verification:** U₉ rejects context claiming semantic output.

**Test 7:** `test_u9_rejects_hukm_identity_output`
**Law:** No HUKM_IDENTITY output
**Status:** ✅ PASS
**Verification:** U₉ rejects context claiming hukm output.

**Test 8:** `test_u9_rejects_syntactic_role_output`
**Law:** No FUNCTIONAL_RELATION_IDENTITY output (صيغة فاعل ≠ الفاعل النحوي)
**Status:** ✅ PASS
**Verification:** U₉ rejects context claiming syntactic role output.

---

### 4. Preservation Tests

**Test 9:** `test_u9_preserves_u7c_agreement_edges_as_external_trace`
**Law:** Agreement edges from U₇-C preserved as external trace (not consumed)
**Status:** ✅ PASS
**Verification:** Agreement edges appear in `external_agreement_trace` field.

**Test 10:** `test_u9_preserves_residual_audit`
**Law:** Residuals preserved (not deleted without trace)
**Status:** ✅ PASS
**Verification:** Upstream residuals carried forward in output.

**Test 11:** `test_u9_preserves_candidate_rank_not_certificate`
**Law:** Rank does not inflate to CERTIFICATE without evidence
**Status:** ✅ PASS
**Verification:** Output rank is CANDIDATE or HYPOTHESIS, not CERTIFICATE.

---

### 5. Golden Path Test

**Test 12:** `test_u9_golden_path_weight_candidate`
**Law:** Valid weight candidate with full constitutional compliance
**Status:** ✅ PASS
**Verification:** Complete execution with all governance satisfied.

**Example:** `ك ت ب` + `فَاعِل` → `كَاتِب` weight candidate

---

## Implementation Details

### File Structure

```
src/dal_core/u9_weight_candidate_carrier.py     (463 lines)
tests/dal_core/test_u9_weight_candidate_constitutional.py  (802 lines)
```

### Key Components

#### 1. Constitutional Validation Function

```python
def validate_approved_context_for_u9(
    context: Optional[ApprovedTransitionContext],
    u8_input: Dict[str, Any]
) -> None:
    """
    Validate ApprovedTransitionContext for U₉ execution.

    Enforces 6 constitutional laws:
    1. Context must be present (not None)
    2. Context must be for U₈→U₉ transition
    3. Context domain must be WEIGHT_DOMAIN
    4. Context input_identity must be ROOT_MATERIAL_IDENTITY or STEM_IDENTITY
    5. Context output_identity must be WEIGHT_IDENTITY
    6. Context output_identity must NOT be semantic/hukm/syntactic
    """
```

#### 2. Weight Candidate Result

```python
@dataclass(frozen=True)
class WeightCandidateResult:
    """
    Result from U₉ WeightCandidateCarrier.

    Allowed competencies:
    ✓ weight_pattern (وزن)
    ✓ morphological_template (قالب صرفي)
    ✓ faa_ayn_lam_mapping (فاء-عين-لام)

    Forbidden competencies:
    ✗ meaning (معنى)
    ✗ syntactic_role (دور نحوي)
    ✗ hukm (حكم)
    ✗ semantic_derivation (اشتقاق معنوي)
    """
    weight_pattern: Optional[str]
    morphological_template: Optional[str]
    faa_ayn_lam_mapping: Optional[Dict[str, str]]

    # Constitutional fields
    output_identity: IdentityType  # WEIGHT_IDENTITY only
    domain: DomainType  # WEIGHT_DOMAIN only
    rank: Rank  # CANDIDATE or HYPOTHESIS
    residuals: Tuple[Residual, ...]
    trace: Tuple[str, ...]
    external_agreement_trace: Tuple[str, ...]
```

#### 3. Main Execution Function

```python
def weight_candidate_carrier_9(
    u8_input: Dict[str, Any],
    approved_context: Optional[ApprovedTransitionContext]
) -> Dict[str, Any]:
    """
    U₉ Weight Candidate Carrier.

    Execution Pattern:
    1. Validate ApprovedTransitionContext
    2. Extract weight pattern candidates
    3. Preserve agreement edges (external trace)
    4. Preserve residuals
    5. Return weight candidate (not certificate)
    """
```

---

## Domain Boundaries

### Permitted in WEIGHT_DOMAIN

✅ **weight_pattern** (وزن)
Example: `"فَاعِل"`, `"مَفْعُول"`

✅ **morphological_template** (قالب صرفي)
Example: `"CaaCiC"`, `"mafCuuC"`

✅ **faa_ayn_lam_mapping** (فاء-عين-لام)
Example: `{"ك": "ف", "ت": "ع", "ب": "ل"}`

### Forbidden in WEIGHT_DOMAIN

❌ **meaning** (معنى)
Belongs to: SEMANTICS_DOMAIN (U₁₄-U₁₅)

❌ **syntactic_role** (دور نحوي)
Belongs to: SYNTAX_DOMAIN (U₁₃+)

❌ **i3rab** (إعراب)
Belongs to: I3RAB_SURFACE_DOMAIN (U₁₃+)

❌ **hukm** (حكم)
Belongs to: JUDGMENT_DOMAIN (U₁₃+)

❌ **semantic_derivation** (اشتقاق معنوي)
Belongs to: SEMANTICS_DOMAIN (U₁₄-U₁₅)

❌ **functional_relation** (علاقة وظيفية)
Belongs to: AMIL_RELATION_DOMAIN (U₁₃+)

---

## Critical Distinctions

### صيغة فاعل vs الفاعل النحوي vs معنى الفاعلية

**Three different domains, three different layers:**

1. **صيغة فاعل** (Weight Domain - U₉)
   Morphological form: `فَاعِل` pattern
   Output: WEIGHT_IDENTITY
   Competency: Pattern structure only

2. **الفاعل النحوي** (Syntax Domain - U₁₃+)
   Syntactic agent: Functional relation to verb
   Output: FUNCTIONAL_RELATION_IDENTITY
   Competency: Grammatical role assignment

3. **معنى الفاعلية** (Semantics Domain - U₁₄-U₁₅)
   Semantic meaning: Who performs the action
   Output: SEMANTIC_IDENTITY
   Competency: Meaning determination

**U₉ operates ONLY in domain #1.** Domains #2 and #3 are constitutionally forbidden.

---

## Execution Trace Preservation

### U₇-C Agreement Edge Preservation

Agreement edges from U₇-C (Clause Surface Agreement) are preserved as **external trace**, not consumed:

```python
# Agreement edges from U₇-C
agreement_edge_ids = ["edge_123", "edge_456"]

# U₉ preserves as external trace
external_agreement_trace = tuple(agreement_edge_ids)

# NOT consumed/interpreted by U₉
# Preserved for higher layers (U₁₃+)
```

This implements PR #111 law:
**"U₈ يحفظ أثر U₇-C ولا يبتلع حافة الاتفاق"**

---

## Rank Progression

### Constitutional Rank Policy

**Input:** `Rank.CANDIDATE` (from U₈)
**Output:** `Rank.CANDIDATE` or `Rank.HYPOTHESIS`
**Forbidden:** `Rank.CERTIFICATE` (without strong evidence)

```python
# Rank does NOT inflate to CERTIFICATE without evidence
output_rank = input_rank

# Only elevate to HYPOTHESIS if we have pattern candidate
if weight_pattern and output_rank == Rank.CANDIDATE:
    output_rank = Rank.HYPOTHESIS

# Do NOT elevate to CERTIFICATE (requires strong evidence from higher layers)
```

---

## Test Execution

### Running Tests

```bash
# Run U₉ constitutional tests only
pytest tests/dal_core/test_u9_weight_candidate_constitutional.py -v

# Run full governance test suite
pytest tests/dal_core/test_u9_weight_candidate_constitutional.py \
       tests/dal_core/test_approved_transition_context.py \
       tests/dal_core/test_algebraic_decision_core.py -v

# Quick verification
pytest tests/dal_core/test_u9_weight_candidate_constitutional.py --tb=no -q
```

### Expected Output

```
============================= test session starts ==============================
collected 12 items

tests/dal_core/test_u9_weight_candidate_constitutional.py ............   [100%]

============================== 12 passed in 0.15s ==============================
```

---

## Integration with AlgebraicDecisionCore

### Complete Governance Flow

```
┌─────────────────────────────────────────────────────────────┐
│ Pipeline/Orchestrator                                        │
│   owns: AlgebraicDecisionCore                                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ AlgebraicDecisionCore.decide_transition()                    │
│   Input: U₈ output, transition request (U₈→U₉)               │
│   Output: DecisionAudit                                      │
│   Validates: 8 dimensions                                    │
│     1. Identity   2. Domain     3. Gate      4. Evidence     │
│     5. Rank       6. Residuals  7. Trace     8. No Leap      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ if audit.is_approved():                                      │
│   create_approved_context(audit, existing_identities)        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ ApprovedTransitionContext (unforgeable)                      │
│   - Transition-specific (U₈→U₉ only)                         │
│   - Domain-specific (WEIGHT_DOMAIN only)                     │
│   - Identity-validated                                       │
│   - Cannot be forged (private sentinel token)                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ weight_candidate_carrier_9(u8_input, approved_context)       │
│   1. Validate context (6 constitutional laws)                │
│   2. Extract weight pattern                                  │
│   3. Preserve agreement edges (external trace)               │
│   4. Preserve residuals                                      │
│   5. Return WeightCandidateResult                            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ WeightCandidateResult                                        │
│   ✓ WEIGHT_IDENTITY                                          │
│   ✓ WEIGHT_DOMAIN                                            │
│   ✓ Rank: CANDIDATE/HYPOTHESIS                               │
│   ✓ Agreement edges preserved                                │
│   ✓ Residuals preserved                                      │
│   ✗ No meaning/hukm/syntax                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Security & Anti-Forgery

### ApprovedTransitionContext Cannot Be Forged

**Private Sentinel Token Pattern:**

```python
# In approved_transition_context.py
_APPROVED_CONTEXT_TOKEN = object()  # Private sentinel

@dataclass(frozen=True)
class ApprovedTransitionContext:
    _token: object = field(repr=False, compare=False, default=None)

    def __post_init__(self):
        # Verify construction through factory function
        if self._token is not _APPROVED_CONTEXT_TOKEN:
            raise ValueError(
                "ApprovedTransitionContext cannot be constructed directly. "
                "Use create_approved_context() factory function."
            )
```

**Only authorized path:**

```python
def create_approved_context(
    audit: DecisionAudit,
    existing_identities: FrozenSet[IdentityType]
) -> ApprovedTransitionContext:
    """ONLY authorized way to create context."""
    if not audit.is_approved():
        raise ValueError("Cannot create context from unapproved audit")

    return ApprovedTransitionContext(
        ...,
        _token=_APPROVED_CONTEXT_TOKEN  # Pass sentinel
    )
```

---

## Next Steps (Future Work)

### Out of Scope for This PR

1. **Pipeline/Orchestrator Implementation**
   - Owns AlgebraicDecisionCore
   - Manages full U₀→U₉ pipeline
   - Creates and passes ApprovedTransitionContext

2. **U₉ Integration Tests**
   - Full pipeline U₀→U₁→...→U₈→U₉
   - Real Arabic examples
   - Performance benchmarks

3. **Higher Layers (U₁₀+)**
   - U₁₀ WordForm
   - U₁₁ LexicalEntry
   - U₁₂ MorphosyntacticFeature
   - U₁₃ PhraseRelation (syntax)
   - U₁₄ SentenceStructure
   - U₁₅ Dalālah (semantics)

---

## Architectural Significance

### Why This Matters

**U₉ is the proof that AlgebraicDecisionCore governance works.**

Before this PR:
- Governance infrastructure existed (PR #112, #113, #114)
- But no layer was fully governed

After this PR:
- U₉ demonstrates complete governance
- Shows that constitutional architecture is operational
- Proves that layers CAN be prevented from:
  - Self-approving transitions
  - Bypassing domain boundaries
  - Leaping identity types
  - Deleting residuals
  - Inflating ranks
  - Claiming forbidden competencies

**This is the foundation for all future layers.**

Every layer from U₁₀ onward will follow this pattern:
1. No execution without ApprovedTransitionContext
2. No self-instantiation of AlgebraicDecisionCore
3. Domain boundaries enforced
4. Identity progression verified
5. Rank evidence-based
6. Trace preserved
7. Residuals preserved

---

## Conclusion

**U₉ WeightCandidateCarrier is constitutionally complete.**

12/12 tests passing.
All governance laws enforced.
No architectural violations.
Ready for integration with full pipeline.

**القانون الحاكم لـ U₉ مُطبَّق.**

---

**Document Version:** 1.0
**Last Updated:** 2026-05-26
**Maintainer:** Claude Code Agent
**Related PRs:** #111, #112, #113, #114
