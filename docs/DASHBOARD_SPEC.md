# Governed Project Maturity Dashboard Specification
# لوحة نضج المشروع المحكومة طبقيًا

**Version**: 1.0.0
**Status**: Specification (PR-D0)
**Date**: 2026-05-23

---

## Executive Summary

The Governed Project Maturity Dashboard measures **real governed maturity**, not claim maturity. It enforces the constitutional principle:

```text
لا مخرج عارٍ
No bare output
```

Every result must carry: `value + rank + evidence + residuals + failures + trace`.

---

## 1. Core Principle

The dashboard **does NOT** measure:
- ✗ Number of PRs merged
- ✗ Lines of code written
- ✗ Documentation volume
- ✗ Features claimed

The dashboard **DOES** measure:
- ✓ Typed contracts implemented
- ✓ Runtime behavior governed
- ✓ Evidence requirements enforced
- ✓ Rank policies applied
- ✓ Residual taxonomies defined
- ✓ NoLeap guards tested
- ✓ Trace/replay coverage
- ✓ Golden dataset coverage
- ✓ Documentation honesty

**Governing Statement:**

```text
الداش بورد ليس لعرض التقدم؛
بل لمنع الوهم في التقدم.

The dashboard is not to show progress;
but to prevent the illusion of progress.
```

---

## 2. The Governed Chain

The dashboard monitors implementation maturity across the Arabic Algebra cognitive chain:

```text
الدال يصنع الصورة.
المدلول اللفظي يفتح التصور.
الوضع يرخّص المعنى.
الدلالة تحدد العلاقة.
الإفادة تكمل النسبة.
والحكم لا يأتي إلا بعد ذلك.
```

Translated to implementation layers:

```text
A0: Algebra Kernel             (Result/Rank/Evidence/Residual/Trace)
A1: Typed Layers               (Layer definitions, domains, bridges)
A2: Pure Dāl Geometry          (الدال يصنع الصورة)
A3: Madlūl-Lafẓī Geometry      (يفتح التصور اللفظي)
A4: Neutral Dāl/Madlūl Binding (ربط محايد)
A5: Wadh Geometry              (يرخّص المعنى)
A6: Dalālah Gates              (تحدد العلاقة)
A7: Nisbah/Ifādah              (تكمل النسبة)
A8: Hukm Boundary              (منع القفز للحكم)
A9: General Cognitive Layers   (العقل العام)
A10: Golden Dataset + Audit    (اختبار ومراجعة)
```

---

## 3. Dashboard Metrics

### 3.1 Primary Metrics

| Metric | Definition | Calculation |
|--------|------------|-------------|
| **Real Completion** | Weighted layer scores after caps | `Σ(layer_score_capped × layer_weight) / Σ(layer_weight)` |
| **Claim Inflation Risk** | Documentation vs code evidence gap | `HIGH` if ≥3 conflicts, `MEDIUM` if 1-2, `LOW` if 0 |
| **NoLeap Coverage** | Percentage of forbidden transitions tested | `tested_noleap_guards / total_noleap_guards × 100` |
| **Rank Inflation Risk** | Auto-certification without required evidence | `HIGH` if rank ceiling undefined, `MEDIUM` if partial, `LOW` if enforced |
| **Residual Debt** | Unclassified or mislabeled residuals | Count of `AttributeError` labeled as linguistic residual |
| **Trace Coverage** | Results with replay-capable trace | `results_with_trace / total_results × 100` |
| **Golden Dataset Coverage** | Layers with positive/negative/ambiguous/blocked cases | `layers_with_golden / total_layers × 100` |
| **CI Health** | Latest CI/CD status | `PASSING` / `FAILING` / `UNKNOWN` |

### 3.2 Layer-Specific Metrics

Each layer reports:
- **Status**: `IMPLEMENTED` / `PARTIAL` / `DEMONSTRATOR` / `PLANNED` / `GAP`
- **Raw Score**: 0-100 based on criteria
- **Capped Score**: Raw score after applying ceiling rules
- **Rank Ceiling**: Maximum achievable rank
- **Evidence Count**: Number of typed evidence instances
- **Residual Count**: Classified residuals
- **NoLeap Tests**: Count of transition guards
- **Golden Coverage**: Percentage of required test categories
- **Next Blocking Gap**: What prevents advancement

---

## 4. Layer Scoring Model

### 4.1 Raw Score Components (100 points total)

| Component | Points | Description |
|-----------|--------|-------------|
| **Typed Contract** | 15 | Dataclasses, protocols, enums defined with frozen=True |
| **Runtime Implementation** | 20 | Actual logic, not stubs or TODOs |
| **Required Evidence Policy** | 10 | Evidence types defined and enforced |
| **Rank Policy** | 10 | Rank ceilings defined per evidence quality |
| **Residual Taxonomy** | 10 | Linguistic vs implementation failures separated |
| **NoLeap Tests** | 10 | Forbidden transitions have test guards |
| **Trace/Replay** | 10 | Results include Trace objects with replay |
| **Golden Dataset Coverage** | 10 | Positive, negative, ambiguous, blocked cases |
| **Documentation Honesty** | 5 | Docs match code, no claim inflation |

### 4.2 Ceiling Rules (Score Caps)

**Hard Caps:**

| Condition | Max Score | Reason |
|-----------|-----------|--------|
| No typed contract | 30% | Cannot govern untyped code |
| No tests | 50% | Cannot verify behavior |
| Broken trace/replay | 60% | Constitutional violation |
| Strings/booleans instead of typed candidates | 45% | Type discipline failure |
| No NoLeap tests | 55% | Leap risk unguarded |
| No golden dataset | 70% | Cannot certify |
| Claim/code conflict | 70% | Trust deficit |

**Example:**

```python
layer = "A5: Wadh Geometry"
raw_score = 68  # Has some implementation

# Apply caps
if not has_typed_contract:
    capped_score = min(raw_score, 30)
elif uses_strings_not_types:
    capped_score = min(raw_score, 45)
elif not has_tests:
    capped_score = min(raw_score, 50)
else:
    capped_score = raw_score

# Result: capped_score = 45 (demonstrator level)
```

### 4.3 Maturity Levels

| Level | Score Range | Requirements |
|-------|-------------|--------------|
| **CERTIFIED** | 90-100 | All criteria + golden dataset + no conflicts |
| **IMPLEMENTED** | 70-89 | Typed contract + tests + trace + NoLeap |
| **PARTIAL** | 50-69 | Some typed parts, incomplete coverage |
| **DEMONSTRATOR** | 30-49 | Proof of concept, strings/booleans |
| **PLANNED** | 10-29 | Documentation only |
| **GAP** | 0-9 | Missing or conflicted |

---

## 5. Dashboard Views

### 5.1 Overview Cards

```text
┌─────────────────────────┐  ┌─────────────────────────┐
│ Real Completion: 42%    │  │ Claim Inflation: HIGH   │
│ ██████░░░░░░░░░░░░░░    │  │ ⚠ 5 conflicts detected  │
└─────────────────────────┘  └─────────────────────────┘

┌─────────────────────────┐  ┌─────────────────────────┐
│ NoLeap Coverage: 73%    │  │ Trace Coverage: 58%     │
│ 22/30 guards tested     │  │ 234/405 with Trace      │
└─────────────────────────┘  └─────────────────────────┘

┌─────────────────────────┐  ┌─────────────────────────┐
│ Golden Dataset: 40%     │  │ CI Status: PASSING      │
│ 4/10 layers covered     │  │ ✓ 497 tests passing     │
└─────────────────────────┘  └─────────────────────────┘
```

### 5.2 Layer Matrix

| Layer | Principle | Status | Raw | Cap | Ceiling | Evidence | NoLeap | Golden | Next Gap |
|-------|-----------|--------|-----|-----|---------|----------|--------|--------|----------|
| A0 | Kernel | IMPL | 85 | 85 | CERTIFIED | 47 | 12/12 | ✓ | Trace usage audit |
| A1 | Layers | IMPL | 82 | 82 | CERTIFIED | 31 | 8/8 | ✓ | Domain bridge tests |
| A2 | Pure Dāl | PARTIAL | 68 | 55 | PARTIAL | 23 | 5/7 | ✗ | Golden dataset |
| A3 | Madlūl | PARTIAL | 45 | 45 | DEMONSTRATOR | 8 | 3/6 | ✗ | Typed candidate |
| A4 | Binding | IMPL | 78 | 78 | IMPLEMENTED | 18 | 6/6 | ✓ | Full integration |
| A5 | Wadh | PARTIAL | 62 | 45 | DEMONSTRATOR | 15 | 4/8 | ✗ | Replace strings |
| A6 | Dalālah | PARTIAL | 58 | 58 | PARTIAL | 11 | 3/9 | ✗ | Full algebra |
| A7 | Ifādah | DEMO | 35 | 35 | DEMONSTRATOR | 4 | 1/12 | ✗ | Typed closure |
| A8 | Hukm | PARTIAL | 72 | 72 | IMPLEMENTED | 9 | 7/7 | ✓ | Hukm itself |
| A9 | Cognitive | PLANNED | 15 | 15 | PLANNED | 0 | 0/25 | ✗ | Not claimed |
| A10 | Golden | GAP | 22 | 22 | GAP | 0 | N/A | partial | Create dataset |

### 5.3 Pipeline Flow Diagram

```text
Raw Arabic Text
      ↓
 [A2: Pure Dāl]       ● GREEN (Partial: 55%)
      ↓
[A3: Madlūl-Lafẓī]    ● ORANGE (Demonstrator: 45%)
      ↓
[A4: Binding]         ● YELLOW (Implemented: 78%)
      ↓
 [A5: Wadh]           ● ORANGE (Demonstrator: 45%)
      ↓
[A6: Dalālah]         ● YELLOW (Partial: 58%)
      ↓
 [A7: Ifādah]         ● ORANGE (Demonstrator: 35%)
      ↓
[A8: Hukm Boundary]   ● YELLOW (Guard: 72%)
      ↓
   (Hukm itself)      ● GRAY (Not implemented)
```

**Color Legend:**
- 🟢 GREEN (90-100): CERTIFIED
- 🟡 YELLOW (70-89): IMPLEMENTED
- 🟠 ORANGE (30-69): PARTIAL/DEMONSTRATOR
- 🔴 RED (10-29): PLANNED
- ⚫ GRAY (0-9): GAP

### 5.4 Claim Audit Table

| Claim | Code Evidence | Test Evidence | Status | Risk | Fix |
|-------|---------------|---------------|--------|------|-----|
| "Ifādah implemented" | boolean dict closure | No typed tests | ❌ CONFLICT | HIGH | PR-F7 Typed Ifādah |
| "Hukm production" | Guard exists, no Hukm | 7 NoLeap tests | ⚠ PARTIAL | MEDIUM | Clarify: boundary not production |
| "General Cognitive Algebra" | Partial (5/13 layers) | Layer tests | ⚠ PARTIAL | MEDIUM | Update docs: "foundation" |
| "Pure Dāl Geometry" | DalCandidate + Builder | 57 tests | ✓ VALID | LOW | Add golden dataset |
| "Wadh licenses meaning" | Demonstrator strings | 22 tests | ⚠ DEMONSTRATOR | MEDIUM | PR-F5 Typed Wadh |

### 5.5 NoLeap Violations Monitor

| Forbidden Transition | Guard Exists | Test Exists | Status | Risk |
|---------------------|--------------|-------------|--------|------|
| MORPH_SURFACE → SEMANTICS | ✓ | ✓ | GUARDED | LOW |
| SEMANTICS → HUKM | ✓ | ✓ | GUARDED | LOW |
| IFADAH → HUKM | ✓ | ✓ | GUARDED | LOW |
| DĀL → MEANING | ✓ | ✓ | GUARDED | LOW |
| BINDING → DALĀLAH | ✓ | ✓ | GUARDED | LOW |
| WADH → HUKM | ✓ | ✗ | UNGUARDED | HIGH |
| MADLUL → IFADAH | ✗ | ✗ | MISSING | HIGH |
| TASAWWUR → HUKM | ✓ | ✗ | UNGUARDED | MEDIUM |

---

## 6. Data Collection Points

### 6.1 Static Analysis

**Source locations:**
- `src/fvafk/algebra/core.py` - Result/Rank/Evidence/Residual definitions
- `src/gfa/methods/*/` - Layer implementations
- `tests/gfa/methods/test_*.py` - Test coverage
- `docs/*.md` - Documentation claims
- `pyproject.toml` - Dependencies and metadata

**Extraction methods:**
- AST parsing for `@dataclass(frozen=True)` contracts
- Grep for `Result(` instantiations with trace
- Test file parsing for `test_noleap_*` patterns
- Documentation parsing for claim statements
- Git blame for implementation dates

### 6.2 Runtime Analysis

**Instrumentation points:**
- Count `Result` objects with non-None `trace`
- Count residuals by taxonomy (linguistic vs implementation)
- Count rank elevations by evidence type
- Measure trace replay success rate

### 6.3 Test Analysis

**Coverage metrics:**
- NoLeap test count per layer
- Golden dataset case types (positive/negative/ambiguous/blocked)
- Test-to-implementation ratio
- Assertion count per test

---

## 7. JSON Data Schema

See [DASHBOARD_DATA_SCHEMA.md](./DASHBOARD_DATA_SCHEMA.md) for complete schema.

**Minimal example:**

```json
{
  "project": "General Cognitive Arabic Algebra",
  "generated_at": "2026-05-23T20:00:00Z",
  "version": "1.0.0",
  "overall_real_completion": 42,
  "claim_inflation_risk": "HIGH",
  "metrics": {
    "noleap_coverage": 73,
    "trace_coverage": 58,
    "golden_coverage": 40,
    "rank_inflation_risk": "MEDIUM",
    "residual_debt": 12,
    "ci_status": "PASSING"
  },
  "layers": [
    {
      "id": "A2",
      "name": "Pure Dāl Geometry",
      "principle_ar": "الدال يصنع الصورة",
      "principle_en": "Dāl makes the form",
      "status": "PARTIAL",
      "score_raw": 68,
      "score_capped": 55,
      "cap_reason": "No complete golden dataset",
      "rank_ceiling": "PARTIAL",
      "evidence": {
        "typed_contract": true,
        "runtime_implementation": true,
        "evidence_policy": true,
        "rank_policy": true,
        "residual_taxonomy": true,
        "noleap_tests": 5,
        "noleap_total": 7,
        "trace_replay": true,
        "golden_dataset": false,
        "doc_honesty": true
      },
      "forbidden_outputs": [
        "meaning",
        "dalalah",
        "ifadah",
        "hukm"
      ],
      "gaps": [
        "No full RawArabicTrace→DalCandidate golden coverage",
        "C2a gate orchestration needs debugging"
      ],
      "next_required_pr": "PR-F3 LayerSpec + PR-G1 Golden Dataset"
    }
  ],
  "claim_conflicts": [
    {
      "claim": "Ifādah implemented",
      "doc_location": "README.md:45",
      "code_reality": "boolean dict closure",
      "test_reality": "No typed tests",
      "risk": "HIGH",
      "recommended_fix": "PR-F7 Typed Ifādah Contract"
    }
  ]
}
```

---

## 8. Implementation Roadmap

### PR-D0: Governance Metrics Specification (This Document)
**Status**: Current
**Deliverables**:
- `docs/DASHBOARD_SPEC.md`
- `docs/GOVERNANCE_METRICS.md`
- `docs/LAYER_MATURITY_MODEL.md`
- `docs/DASHBOARD_DATA_SCHEMA.md`

**Acceptance Criteria**:
- [x] Define 10+ dashboard metrics
- [x] Define layer scoring model with caps
- [x] Define maturity levels
- [x] Define JSON schema
- [x] No runtime code changes
- [x] No claim inflation

### PR-D1: Static Audit Report Generator
**Deliverables**:
- `tools/project_audit/generate_dashboard_report.py`
- `reports/project_governance_status.json`

**Functionality**:
- Parse source code for typed contracts
- Extract test counts and NoLeap coverage
- Scan documentation for claim statements
- Compare claims vs code reality
- Generate JSON report
- Apply scoring and ceiling rules

**Dependencies**: PR-D0

### PR-D2: Dashboard UI
**Deliverables**:
- `dashboard/index.html` (or within `src/fvafk/dashboard/`)
- Static site or FastAPI integration
- Real-time metrics display
- Layer matrix visualization
- Pipeline flow diagram
- Claim audit table

**Dependencies**: PR-D0, PR-D1

### PR-D3: CI Integration
**Deliverables**:
- `.github/workflows/governance-audit.yml`
- Auto-generate report on every PR
- Comment on PRs with maturity impact
- Fail if claim inflation detected

**Dependencies**: PR-D1

### PR-D4: Live GitHub PR/Issue Integration
**Deliverables**:
- Auto-link layers to PRs
- Track implementation status
- Update dashboard on merge
- Generate release notes from governance state

**Dependencies**: PR-D2, PR-D3

---

## 9. Forbidden Practices

The dashboard **MUST NOT**:

- ❌ Count PRs as completion metric
- ❌ Accept documentation as implementation proof
- ❌ Treat demonstrator code as certified
- ❌ Hide claim conflicts
- ❌ Auto-promote maturity without evidence
- ❌ Allow claim inflation to persist
- ❌ Conflate strings with typed candidates
- ❌ Ignore NoLeap violations
- ❌ Skip residual taxonomy
- ❌ Accept broken trace/replay

The dashboard **MUST**:

- ✓ Enforce typed contracts
- ✓ Verify runtime behavior
- ✓ Apply ceiling caps ruthlessly
- ✓ Highlight claim conflicts
- ✓ Separate linguistic residuals from bugs
- ✓ Count NoLeap test coverage
- ✓ Measure trace/replay capability
- ✓ Require golden datasets for certification
- ✓ Maintain documentation honesty
- ✓ Report gaps transparently

---

## 10. Success Criteria

The dashboard is successful when:

1. **No layer claims CERTIFIED without golden dataset**
2. **Claim conflicts are visible and tracked**
3. **Real completion ≠ PR count**
4. **Ceiling caps prevent score inflation**
5. **NoLeap violations are monitored**
6. **Trace coverage is measurable**
7. **Residual debt is quantified**
8. **Documentation matches code reality**
9. **Every layer's next gap is clear**
10. **The project cannot deceive itself about maturity**

---

## 11. Maintenance

**Update triggers:**
- New layer implementation → Recalculate scores
- Test addition → Update NoLeap/golden coverage
- Documentation change → Re-audit claims
- PR merge → Regenerate dashboard
- Claim conflict resolution → Update risk level

**Ownership:**
- Dashboard spec: Architecture team
- Audit generator: DevOps + QA
- UI: Frontend team
- CI integration: DevOps
- Content accuracy: All contributors

---

## Appendix A: Layer Detail Requirements

Each layer entry in the dashboard must include:

```yaml
layer:
  id: A2
  name: Pure Dāl Geometry
  principle_ar: الدال يصنع الصورة
  principle_en: Dāl makes the form
  status: PARTIAL | IMPLEMENTED | DEMONSTRATOR | PLANNED | GAP
  maturity_level: CERTIFIED | IMPLEMENTED | PARTIAL | DEMONSTRATOR | PLANNED | GAP

  scores:
    raw: 68
    capped: 55
    cap_reason: "No golden dataset"
    components:
      typed_contract: 15
      runtime: 18
      evidence_policy: 8
      rank_policy: 9
      residual_taxonomy: 10
      noleap_tests: 7
      trace_replay: 9
      golden_dataset: 0
      doc_honesty: 4

  governance:
    rank_ceiling: PARTIAL
    evidence_count: 23
    residual_count: 15
    noleap_coverage: 0.71  # 5/7
    golden_coverage: 0.0
    trace_coverage: 0.85

  files:
    contracts:
      - src/gfa/methods/lafzi_dal/dal_candidate.py
      - src/gfa/methods/lafzi_dal/dal_structures.py
    implementations:
      - src/gfa/methods/lafzi_dal/dal_candidate_builder.py
    tests:
      - tests/gfa/methods/test_pr_l3_pure_dal_geometry.py
      - tests/gfa/methods/test_pr_l3_phase2_builder_integration.py

  forbidden_outputs:
    - meaning
    - dalalah
    - ifadah
    - hukm

  gaps:
    - "No full RawArabicTrace→DalCandidate golden coverage"
    - "C2a gate orchestration needs debugging"

  next_action:
    pr: "PR-F3 LayerSpec + PR-G1 Golden Dataset"
    priority: HIGH
    blocking: ["A3", "A4", "A5"]
```

---

**Document Status**: SPECIFICATION (PR-D0)
**Last Updated**: 2026-05-23
**Next Review**: After PR-D1 implementation
