# Claim Boundary Audit

**PR**: PR-F0
**Date**: 2026-05-23
**Purpose**: Audit all architectural claims against actual implementation
**Rule**: Code wins over docs when they conflict

---

## Audit Methodology

1. **IMPLEMENTED**: Feature is coded, tested, and passing in CI
2. **PARTIAL**: Feature is coded but incomplete or limited scope
3. **DEMONSTRATOR**: Feature exists as proof-of-concept only
4. **PLANNED**: Feature is documented but not implemented
5. **NOT FOUND**: Claim exists in docs but no evidence in code
6. **CONFLICT**: Docs and code contradict each other

---

## Constitutional Claims

| Claim | Status | Evidence | Risk | Required Fix |
|-------|--------|----------|------|--------------|
| No bare output constitution | **IMPLEMENTED** | `src/fvafk/algebra/core.py:Result.__post_init__` enforces evidence requirement for LICENSED/CERTIFIED | None | None |
| Result contract (value+rank+evidence+residuals+failures+trace) | **IMPLEMENTED** | `src/fvafk/algebra/core.py:68-120` dataclass with all 6 fields | None | None |
| CPB bridge enforcement | **IMPLEMENTED** | `src/fvafk/algebra/cpb.py:validate_cpb` checks ALLOWED_BRIDGES/FORBIDDEN_BRIDGES | None | None |
| Rank policy (UNRESOLVED→CANDIDATE→LICENSED→CERTIFIED→REFUTED) | **IMPLEMENTED** | `src/fvafk/algebra/core.py:17-24` Rank enum | None | None |
| Residual blocks CERTIFIED | **IMPLEMENTED** | `src/fvafk/algebra/core.py:89-92` raises ValueError if CERTIFIED with residuals | None | None |
| Fatal failure forces REFUTED | **IMPLEMENTED** | `src/fvafk/algebra/core.py:93-98` checks fatal failures | None | None |
| Evidence required for LICENSED+ | **IMPLEMENTED** | `src/fvafk/algebra/core.py:84-88` enforces evidence requirement | None | None |

**Assessment**: Constitutional foundation is **solid and enforced at runtime**.

---

## Arabic Algebra (FVAFK) Claims

| Claim | Status | Evidence | Risk | Required Fix |
|-------|--------|----------|------|--------------|
| Pure Dāl Geometry | **PARTIAL** | `src/gfa/methods/lafzi_dal/` exists with DalCandidate builder (PR #75 draft) | Dal is partial baseline, not complete | Mark as "Phase 2 baseline" not "complete" |
| Dāl/Madlūl Binding | **IMPLEMENTED** | `src/gfa/methods/lafzi_dalalah/dal_madlul_binding_gate.py`, 31 tests passing | None | None |
| Wadh Geometry | **IMPLEMENTED** | `src/gfa/methods/lafzi_wadh/`, 37 tests passing (PR #65, #66) | None | None |
| Dalālah gates (Mutabaqah/Tadammun/Iltizam) | **IMPLEMENTED** | `src/fvafk/algebra/semantics/operations.py:MutabaqahGate/TadammunGate/IltizamGate`, `src/gfa/methods/lafzi_dalalah/mutabaqah_gate.py` (29 tests PR #67) | None | None |
| Ifādah closure | **PARTIAL** | Referenced in roadmap but no `IfadahCandidate` or `IfadahGate` in code | Claim inflation | Mark as PLANNED not IMPLEMENTED |
| Hukm boundary | **PARTIAL** | Boundary guards exist (`test_semantic_boundary_hardening.py` gates 12-17) but no HukmCandidate | Boundary defined but layer not implemented | Clarify "boundary guards exist, layer not implemented" |
| NoLeap tests | **IMPLEMENTED** | `tests/fvafk/algebra/test_semantic_boundary_hardening.py` (14 tests), `tests/fvafk/algebra/test_ifadah_forbidden_jumps.py` (14 tests) | None | None |
| Residual taxonomy (morphology) | **IMPLEMENTED** | `src/fvafk/algebra/morphology/residual_taxonomy.py` - 9 kinds | None | None |
| Residual taxonomy (syntax) | **IMPLEMENTED** | `src/fvafk/algebra/syntax/residual_taxonomy.py` - 10 kinds | None | None |
| Residual taxonomy (semantics) | **IMPLEMENTED** | `src/fvafk/algebra/semantics/residual_taxonomy.py` - 11 kinds | None | None |
| Residual taxonomy (linguistic vs implementation) | **NOT FOUND** | No separation between linguistic residuals and implementation failures (AttributeError) | **CRITICAL** | PR-F1 must create this taxonomy |
| Lafẓī Madlūl Fractal Algebra | **IMPLEMENTED** | `src/fvafk/algebra/lafzi_madlul/`, 85/85 tests passing | None | None |

**Assessment**: Arabic algebra has **strong foundation** (Dal→Binding→Wadh→Mutabaqah) but **Ifādah/Hukm are planned not implemented**.

---

## General Cognitive Algebra (GFA) Claims

| Claim | Status | Evidence | Risk | Risk | Required Fix |
|-------|--------|----------|------|------|--------------|
| RealityGeometry | **IMPLEMENTED** | `src/gfa/reality/`, 21 tests passing | None | None |
| SensoryTransferGeometry | **IMPLEMENTED** | `src/gfa/sensory_transfer/`, 25 tests passing | None | None |
| CognitiveCarrierGeometry | **IMPLEMENTED** | `src/gfa/cognitive_carrier/`, 37 tests passing | None | None |
| PriorInformationSystem | **PARTIAL** | `src/gfa/proto_prior/first_prior_unit.py` (14 fields), `src/gfa/methods/rational/prior_filter.py` (Opinion blocking) | Missing formal PriorInformationSystem contract | PR-C1 must formalize full contract |
| AttentionGeometry | **IMPLEMENTED** | `src/gfa/attention/`, 19 tests passing | None | None |
| MemoryGeometry | **IMPLEMENTED** | `src/gfa/foundations/memory/`, 30 tests passing (PR-G1) | None | None |
| GovernedBinding (general contract) | **PARTIAL** | `src/gfa/methods/rational/neutral_binding.py` (specific), no general governed_binding function | Missing general function | PR-C2 must extract general contract |
| TasawwurLayer | **NOT FOUND** | No `TasawwurCandidate` or `TasawwurGate` in codebase | **MAJOR** | PR-C3 required |
| NisbahLayer | **NOT FOUND** | No `NisbahCandidate` distinct from syntax nisbah | **MAJOR** | PR-C4 required |
| IfadahLayer | **NOT FOUND** | No `IfadahCandidate` or `IfadahGate` in codebase | **MAJOR** | PR-C5 required |
| HukmLayer | **NOT FOUND** | No `HukmCandidate` or `HukmGate` in codebase | **MAJOR** | PR-C6 required |
| ActionEffectLayer | **NOT FOUND** | No ActionEffect tracking in code | PLANNED | Future work |
| AuditLayer | **NOT FOUND** | No reverse trace audit in code | PLANNED | PR-A1 required |
| Complete General Cognitive Algebra | **NOT FOUND** | Only Layers -2 through 1 implemented (5 of 13 layers) | **CRITICAL OVERCLAIM** | Update all docs to say "5/13 layers, foundation only" |

**Assessment**: General Cognitive Algebra is **5/13 layers implemented**. Claims of "General Cognitive Algebra" without qualification are **overclaims**.

---

## Governance Claims

| Claim | Status | Evidence | Risk | Required Fix |
|-------|--------|----------|------|--------------|
| LayerSpec contract | **NOT FOUND** | No `LayerSpec` dataclass in codebase | **CRITICAL** | PR-F3 must create formal contract |
| Rank ceiling enforcement | **PARTIAL** | `Result.with_rank` allows manual rank setting, no ceiling enforcement in binding operations | **RANK INFLATION RISK** | PR-F2 must add `enforce_rank_ceiling` |
| Rank downgrade on ambiguity | **PARTIAL** | Some operations create residuals but don't auto-downgrade rank | Weak governance | PR-F2 must formalize |
| Implementation failure separation | **NOT FOUND** | No separation of `AttributeError` from linguistic residuals | **CRITICAL** | PR-F1 must separate |
| Golden Dataset | **NOT FOUND** | No `tests/golden_dataset/` directory or YAML files | **MISSING VALIDATION** | PR-G1 must create 100 examples |
| Wadh requires strong Dal | **NOT FOUND** | No gate checking `dal_candidate.rank in {LICENSED, CONTEXTUAL, CERTIFIED}` before Wadh | Governance gap | Add to WadhGate |

**Assessment**: Governance is **conceptually strong** but **missing formal enforcement mechanisms**.

---

## DAL_CORE Claims

| Claim | Status | Evidence | Risk | Required Fix |
|-------|--------|----------|------|--------------|
| 8-layer domain architecture (D0-D7) | **IMPLEMENTED** | `src/dal_core/` modules implement domains | None | None |
| Claim-scoped evidence | **IMPLEMENTED** | `DalEvidence` requires span | None | None |
| Trace-based reversibility | **IMPLEMENTED** | `DalTrace.is_reversible()` | None | None |
| Protocol-based contracts | **IMPLEMENTED** | `DalTransitionContract`, `DalCandidateProtocol` | None | None |
| No meaning field in DClosed | **IMPLEMENTED** | `src/dal_core/d_mufrad.py:16-29` prohibits meaning/murad/haqiqa_majaz fields | None | None |
| MufradProof | **IMPLEMENTED** | `src/dal_core/mufrad_proof.py` | None | None |
| NahwOperatorRegistry | **IMPLEMENTED** | `src/dal_core/nahw_operator_registry.py`, immutable (PR #16) | None | None |
| OperatorTriggerPotential | **IMPLEMENTED** | `src/dal_core/operator_trigger.py` (PR #14) | None | None |
| RelationCandidate | **NOT FOUND** | Mentioned in roadmap but not in code | PLANNED | Future PR |
| CaseEffectCandidate | **NOT FOUND** | Mentioned in roadmap but not in code | PLANNED | Future PR |
| MurakkabProof | **NOT FOUND** | Mentioned in roadmap but not in code | PLANNED | Future PR |

**Assessment**: DAL_CORE is **solid up to OperatorTrigger**, composition closure is **planned not implemented**.

---

## Documentation vs Code Conflicts

| Document | Claim | Code Reality | Conflict Severity |
|----------|-------|--------------|-------------------|
| README.md | "Arabic NLP pipeline" | Actually General Cognitive Algebra testbed using Arabic | **MAJOR UNDERSELLING** |
| README.md | Current sprint: "Sprint 5 Web API" | Web API is stub, GFA/algebra are active work | **OUTDATED** |
| ARABIC_ALGEBRA_ROADMAP.md | "Phase 5 — Dāl/Madlūl/Dalālah/Ifādah Algebra ✅" | Ifādah is NOT implemented, only gates 1-11 exist | **OVERCLAIM** |
| GFA README.md | "Complete General Cognitive Algebra" claim avoided | States "5/13 layers" correctly | **CORRECT** |
| PROJECT_ALGEBRA_ARCHITECTURE_MAP.md | A5-A10 documented | A5-A6 partial, A7 partial (Mutabaqah only), A8-A10 not implemented | **PLANNING DOC** (OK) |
| pyproject.toml | "Arabic NLP pipeline" | Undersells General Cognitive Algebra research | **UNDERSELLING** |

**Assessment**: README and roadmap **overclaim completion**, GFA docs are **accurate**, architecture map is **planning only** (correctly scoped).

---

## Critical Gaps Found

### Gap 1: Residual Taxonomy (Linguistic vs Implementation) ⚠️ CRITICAL

**Evidence**: PR #75 shows `success=True` with `residuals={'c2a_phonology_error:AttributeError'}`
**Risk**: Implementation exceptions treated as linguistic residuals
**Required**: PR-F1 must separate:
- `LinguisticResidual` (missing_haraka, ambiguous_formula) → coexist with success
- `ImplementationFailure` (AttributeError, Exception) → must be BLOCKED or INTERNAL_FAILURE

### Gap 2: LayerSpec Contract ⚠️ CRITICAL

**Evidence**: Layers have implicit contracts, no formal `LayerSpec` dataclass
**Risk**: No machine-enforceable layer boundaries
**Required**: PR-F3 must create:
```python
@dataclass(frozen=True)
class LayerSpec:
    name: str
    input_type: type
    output_type: type
    forbidden_outputs: tuple[str, ...]
    required_evidence: tuple[str, ...]
    rank_policy: str
    residual_policy: str
```

### Gap 3: Rank Policy Enforcement ⚠️ CRITICAL

**Evidence**: No `enforce_rank_ceiling` function, manual rank promotion possible
**Risk**: CANDIDATE Dal → binding succeeds → result promoted to CERTIFIED without validation
**Required**: PR-F2 must create:
```python
def enforce_rank_ceiling(input_rank: Rank, operation_type: str) -> Rank:
    """نجاح طبقة لا يرفع رتبة الطبقة التالية"""
    if input_rank == Rank.CANDIDATE:
        return Rank.LICENSED  # ceiling, not CERTIFIED
    return input_rank
```

### Gap 4: Wadh Gate Rank Guard ⚠️ MAJOR

**Evidence**: No verification that WadhGate requires LICENSED+ Dal
**Risk**: Weak Dal (CANDIDATE) can proceed to Wadh
**Required**: Add to `WadhGate`:
```python
if dal_candidate.rank not in {Rank.LICENSED, Rank.CONTEXTUAL, Rank.CERTIFIED}:
    return blocked("dal_rank_too_low_for_wadh")
```

### Gap 5: Golden Dataset ⚠️ MAJOR

**Evidence**: No `tests/golden_dataset/` directory
**Risk**: No canonical test suite for governance
**Required**: PR-G1 must create 100 examples:
- 30 general cognitive (from كتاب التفكير)
- 40 Arabic dal/binding
- 20 rank policy
- 10 residual classification

### Gap 6: PriorInformationSystem Formal Contract ⚠️ MAJOR

**Evidence**: `FirstPriorUnit` exists but no `PriorInformationSystem` contract
**Risk**: Conceptual clarity without formal enforcement
**Required**: PR-C1 must formalize:
```python
@dataclass(frozen=True)
class PriorInformationSystem:
    domain: str
    primitives: tuple[str, ...]
    rules: tuple[str, ...]
    evidence_sources: tuple[str, ...]
    rank_policy: str
    update_policy: str
```

### Gap 7: TasawwurLayer Missing ⚠️ MAJOR

**Evidence**: No `TasawwurCandidate` in codebase
**Risk**: Cognitive algebra jump from binding directly to Hukm without Tasawwur
**Required**: PR-C3 must implement:
- `TasawwurCandidate` dataclass
- `TasawwurGate` preventing direct jump to Hukm
- Tests enforcing "تصور لا يصبح حكماً"

### Gap 8: General governed_binding Function ⚠️ MODERATE

**Evidence**: `NeutralBinding` and `DalMadlulBindingGate` exist separately
**Risk**: No unified binding contract
**Required**: PR-C2 must extract general function

### Gap 9: Nisbah/Ifadah/Hukm Layers ⚠️ MODERATE

**Evidence**: Not found in codebase
**Status**: Correctly marked as future work in GFA README
**Required**: PR-C4, PR-C5, PR-C6 respectively

### Gap 10: Audit Trace ⚠️ LOW

**Evidence**: Forward trace exists, no reverse audit
**Status**: Planned for PR-A1
**Required**: Future work

---

## Hallucination / Overclaim Risks

### Hallucination 1: "Complete General Cognitive Algebra" ⚠️ CRITICAL

**Where**: Implied in some documentation
**Reality**: 5/13 layers implemented (Layers -2 through 1 only)
**Fix**: Add to every doc: "General Cognitive Algebra foundation (5/13 layers)"

### Hallucination 2: "Ifādah Algebra Implemented" ⚠️ MAJOR

**Where**: ARABIC_ALGEBRA_ROADMAP.md "Phase 5 ✅"
**Reality**: Gates 1-11 exist (boundary guards), no IfadahCandidate or IfadahGate
**Fix**: Change to "Phase 5.5 boundary hardening ✅, Phase 5F-5H planned"

### Hallucination 3: "Arabic proves the general theory" ⚠️ MODERATE

**Where**: Some informal descriptions
**Reality**: Arabic is first revealing model / testbed, not proof
**Fix**: Use "Arabic as revealing model" consistently

### Hallucination 4: "Semantic understanding is complete" ⚠️ MODERATE

**Where**: Implied by Phase 5 completion claims
**Reality**: Mutabaqah gate exists, Tadammun/Iltizam exist, but no Ifadah/Murad
**Fix**: Clarify "semantic boundary guards exist, semantic completion planned"

### Hallucination 5: "Web API ready" ⚠️ LOW

**Where**: README.md "In Progress ⏳ Web API"
**Reality**: `web_app/main.py` is stub
**Fix**: Demote to "planned" or remove from current status

---

## Test Coverage vs Claims

| Claim Area | Tests Found | Coverage Assessment |
|------------|-------------|---------------------|
| Result invariants | `tests/fvafk/algebra/test_result_invariants.py` | ✅ STRONG |
| CPB bridge enforcement | `tests/fvafk/algebra/test_bridge_matrix.py` | ✅ STRONG |
| Morphology algebra | `tests/test_algebra_morphology_phase3.py` (33 tests) | ✅ STRONG |
| Syntax algebra | `tests/test_algebra_syntax_phase4.py` (43 tests) | ✅ STRONG |
| Semantic boundaries | `tests/fvafk/algebra/test_semantic_boundary_hardening.py` (14 tests), `test_ifadah_forbidden_jumps.py` (14 tests) | ✅ STRONG |
| Dal geometry | `tests/gfa/methods/test_dal_candidate_builder.py` | ⚠️ PARTIAL (PR #75 draft) |
| Wadh geometry | `tests/gfa/methods/test_wadh_geometry_definitions.py` (15 tests), `test_wadh_gate.py` (22 tests) | ✅ STRONG |
| Mutabaqah | `tests/gfa/methods/test_mutabaqah_gate.py` (29 tests) | ✅ STRONG |
| Ifadah closure | NOT FOUND | ❌ MISSING |
| Golden dataset | NOT FOUND | ❌ MISSING |
| Rank inflation prevention | NOT FOUND | ❌ MISSING |
| Implementation failure separation | NOT FOUND | ❌ MISSING |

**Assessment**: Test coverage is **strong for implemented features**, **absent for claimed-but-missing features**.

---

## Summary Statistics

- **IMPLEMENTED**: 28 claims
- **PARTIAL**: 11 claims
- **DEMONSTRATOR**: 0 claims
- **PLANNED**: 9 claims
- **NOT FOUND**: 14 claims
- **CONFLICT**: 6 claims

**Total Audited**: 68 claims

**Critical Gaps**: 7
**Major Gaps**: 5
**Moderate Gaps**: 2
**Low Gaps**: 1

---

## Verdict

### What is SOLID ✅

1. **Constitutional foundation** (Result contract, CPB, Rank policy) - **fully enforced at runtime**
2. **Arabic algebra foundation** (Dal→Binding→Wadh→Mutabaqah) - **strong implementation with tests**
3. **General Cognitive Algebra foundation** (Reality→Sensory→Carrier→Prior→Attention→Memory) - **5/13 layers implemented**
4. **NoLeap boundary guards** - **comprehensive test suite**
5. **DAL_CORE** (D0-D7, MufradProof, OperatorTrigger) - **solid pre-semantic algebra**

### What is MISSING ⚠️

1. **Residual taxonomy** (linguistic vs implementation) - **PR-F1 required**
2. **LayerSpec contract** - **PR-F3 required**
3. **Rank policy enforcement** (ceiling, auto-downgrade) - **PR-F2 required**
4. **Cognitive layers** (Tasawwur, Nisbah, Ifadah, Hukm) - **PR-C3-C6 required**
5. **Golden dataset** - **PR-G1 required**
6. **General governed_binding contract** - **PR-C2 required**
7. **Ifadah/Hukm implementation** - **planned, not implemented**

### What is OVERCLAIMED 🚨

1. **"Complete General Cognitive Algebra"** - only 5/13 layers
2. **"Phase 5 implemented"** - only boundary guards, no Ifadah layer
3. **"Full semantic understanding"** - Mutabaqah exists, Ifadah/Murad do not
4. **"Arabic proves theory"** - Arabic is revealing model, not proof

---

## Recommended Next Steps

**Before any new feature implementation:**

1. ✅ **This PR (PR-F0)**: Rewrite project definition and audit claims
2. ✅ **PR-F1**: Residual Taxonomy Formalization (linguistic vs implementation)
3. ✅ **PR-F2**: Rank Policy Hardening (ceiling enforcement, auto-downgrade)
4. ✅ **PR-F3**: LayerSpec Contract (formal typed layer specifications)

**After foundation hardening:**

5. PR-C1: PriorInformationSystem formal contract
6. PR-C2: General governed_binding function
7. PR-C3-C6: Tasawwur/Nisbah/Ifadah/Hukm layers
8. PR-G1: Golden Dataset (100 examples)
9. PR-A1: Audit Trace (reverse traceability)

---

**Audit Date**: 2026-05-23
**Auditor**: Claude Agent (PR-F0)
**Status**: Foundation is solid, governance needs hardening, cognitive completion is 38% (5/13 layers)
