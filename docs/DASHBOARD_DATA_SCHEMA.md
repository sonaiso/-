# Dashboard Data Schema
# مخطط بيانات لوحة القياس

**Version**: 1.0.0
**Part of**: PR-D0 Dashboard Specification
**Date**: 2026-05-23

---

## 1. Overview

This document defines the JSON schema for the Governed Project Maturity Dashboard data output.

**File**: `reports/project_governance_status.json`

**Generation**: PR-D1 will implement `tools/project_audit/generate_dashboard_report.py`

---

## 2. Root Schema

```typescript
interface ProjectGovernanceStatus {
  // Metadata
  project: string;
  generated_at: string;  // ISO 8601 timestamp
  version: string;       // Schema version
  generator_version: string;  // Tool version

  // Top-level metrics
  overall_real_completion: number;  // 0-100
  claim_inflation_risk: RiskLevel;

  // Detailed metrics
  metrics: DashboardMetrics;

  // Layer details
  layers: Layer[];

  // Issues
  claim_conflicts: ClaimConflict[];
  noleap_violations: NoLeapViolation[];
  residual_issues: ResidualIssue[];

  // CI/Test status
  ci_status: CIStatus;
  test_summary: TestSummary;
}

type RiskLevel = "NONE" | "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
```

---

## 3. Dashboard Metrics

```typescript
interface DashboardMetrics {
  // Primary metrics
  noleap_coverage: number;        // 0-100 percentage
  trace_coverage: number;         // 0-100 percentage
  golden_coverage: number;        // 0-100 percentage
  rank_inflation_risk: RiskLevel;
  residual_debt: number;          // Count of issues

  // Detailed breakdowns
  layers_by_maturity: {
    CERTIFIED: number;
    IMPLEMENTED: number;
    PARTIAL: number;
    DEMONSTRATOR: number;
    PLANNED: number;
    GAP: number;
  };

  // Test statistics
  total_tests: number;
  passing_tests: number;
  noleap_tests: number;
  golden_tests: number;

  // Code statistics
  typed_contracts: number;
  dataclass_count: number;
  protocol_count: number;
  enum_count: number;
}
```

---

## 4. Layer Schema

```typescript
interface Layer {
  // Identity
  id: string;                    // e.g., "A2"
  name: string;                  // e.g., "Pure Dāl Geometry"
  principle_ar: string;          // Arabic principle
  principle_en: string;          // English principle

  // Maturity
  status: LayerStatus;
  maturity_level: MaturityLevel;

  // Scoring
  score_raw: number;             // 0-100
  score_capped: number;          // 0-100 after ceilings
  cap_reason: string | null;     // Why score was capped

  // Score components
  components: LayerScoreComponents;

  // Governance
  governance: LayerGovernance;

  // Files
  files: LayerFiles;

  // Boundaries
  forbidden_outputs: string[];   // e.g., ["meaning", "hukm"]
  allowed_outputs: string[];     // e.g., ["dal_candidate"]

  // Issues
  gaps: string[];
  warnings: string[];

  // Next steps
  next_action: NextAction | null;
}

type LayerStatus =
  | "IMPLEMENTED"
  | "PARTIAL"
  | "DEMONSTRATOR"
  | "PLANNED"
  | "GAP";

type MaturityLevel =
  | "CERTIFIED"     // 90-100%
  | "IMPLEMENTED"   // 70-89%
  | "PARTIAL"       // 50-69%
  | "DEMONSTRATOR"  // 30-49%
  | "PLANNED"       // 10-29%
  | "GAP";          // 0-9%
```

---

## 5. Layer Score Components

```typescript
interface LayerScoreComponents {
  typed_contract: number;          // 0-15
  runtime_implementation: number;  // 0-20
  evidence_policy: number;         // 0-10
  rank_policy: number;             // 0-10
  residual_taxonomy: number;       // 0-10
  noleap_tests: number;            // 0-10
  trace_replay: number;            // 0-10
  golden_dataset: number;          // 0-10
  doc_honesty: number;             // 0-5

  // Total (should equal score_raw)
  total: number;  // 0-100
}
```

---

## 6. Layer Governance

```typescript
interface LayerGovernance {
  // Evidence
  has_evidence_policy: boolean;
  evidence_count: number;
  evidence_types: string[];

  // Rank
  has_rank_policy: boolean;
  rank_ceiling: string | null;  // e.g., "LICENSED", "PARTIAL"
  rank_inflation_risk: RiskLevel;

  // Residuals
  has_residual_taxonomy: boolean;
  residual_count: number;
  linguistic_residuals: number;
  implementation_failures: number;

  // Tests
  noleap_coverage: number;      // 0.0-1.0
  noleap_tested: number;
  noleap_total: number;

  // Trace
  has_trace_replay: boolean;
  trace_coverage: number;       // 0.0-1.0

  // Golden dataset
  has_golden_dataset: boolean;
  golden_coverage: number;      // 0.0-1.0
  golden_case_types: string[];  // e.g., ["positive", "negative"]
}
```

---

## 7. Layer Files

```typescript
interface LayerFiles {
  // Source files
  contracts: string[];         // Typed contract files
  implementations: string[];   // Implementation files
  tests: string[];             // Test files
  docs: string[];              // Documentation files

  // Statistics
  total_lines: number;
  code_lines: number;
  test_lines: number;
  doc_lines: number;
}
```

---

## 8. Next Action

```typescript
interface NextAction {
  pr: string;                  // e.g., "PR-F3 LayerSpec"
  priority: Priority;
  blocking: string[];          // Layer IDs blocked by this gap
  description: string;
  estimated_effort: string | null;  // e.g., "2 weeks"
}

type Priority = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
```

---

## 9. Claim Conflict

```typescript
interface ClaimConflict {
  claim: string;               // The claim made
  doc_location: string;        // File:line
  code_reality: string;        // What code actually does
  test_reality: string;        // What tests show
  severity: ConflictSeverity;
  risk: RiskLevel;
  recommended_fix: string;
  related_layer: string | null;  // Layer ID if applicable
}

type ConflictSeverity =
  | "CRITICAL"   // Claim completely false
  | "HIGH"       // Major feature claimed but not typed
  | "MEDIUM"     // Partial implementation, misleading docs
  | "LOW";       // Minor wording issue
```

---

## 10. NoLeap Violation

```typescript
interface NoLeapViolation {
  source_layer: string;        // e.g., "DĀL"
  target_layer: string;        // e.g., "MEANING"
  forbidden_transition: string;  // e.g., "DĀL→MEANING"

  guard_exists: boolean;       // Code guard present
  test_exists: boolean;        // Test for guard exists
  test_location: string | null;

  risk: RiskLevel;
  status: ViolationStatus;
}

type ViolationStatus =
  | "GUARDED"      // Guard + test exist
  | "UNGUARDED"    // Guard exists, no test
  | "MISSING"      // No guard or test
  | "BYPASSED";    // Guard exists but can be bypassed
```

---

## 11. Residual Issue

```typescript
interface ResidualIssue {
  location: string;            // File:line
  residual_value: string;      // The residual itself
  issue_type: IssueType;
  severity: RiskLevel;
  layer: string | null;        // Related layer
  recommended_fix: string;
}

type IssueType =
  | "MISLABELED"     // Implementation error labeled as linguistic
  | "UNCLASSIFIED"   // Not in known taxonomy
  | "MIXED"          // Linguistic + implementation mixed
  | "MISSING_TAXONOMY";  // No taxonomy defined
```

---

## 12. CI Status

```typescript
interface CIStatus {
  status: "PASSING" | "FAILING" | "DEGRADED" | "UNKNOWN";
  latest_run: string;          // ISO 8601 timestamp
  workflow_name: string;
  run_url: string | null;

  // Details if failing
  failing_jobs: string[];
  error_summary: string | null;
}
```

---

## 13. Test Summary

```typescript
interface TestSummary {
  total: number;
  passing: number;
  failing: number;
  skipped: number;

  // By category
  unit_tests: number;
  integration_tests: number;
  noleap_tests: number;
  golden_tests: number;

  // Coverage
  coverage_percent: number | null;
  lines_covered: number | null;
  lines_total: number | null;
}
```

---

## 14. Complete Example

```json
{
  "project": "General Cognitive Arabic Algebra",
  "generated_at": "2026-05-23T20:00:00Z",
  "version": "1.0.0",
  "generator_version": "0.1.0",

  "overall_real_completion": 42,
  "claim_inflation_risk": "HIGH",

  "metrics": {
    "noleap_coverage": 73,
    "trace_coverage": 58,
    "golden_coverage": 40,
    "rank_inflation_risk": "MEDIUM",
    "residual_debt": 12,

    "layers_by_maturity": {
      "CERTIFIED": 0,
      "IMPLEMENTED": 3,
      "PARTIAL": 4,
      "DEMONSTRATOR": 2,
      "PLANNED": 1,
      "GAP": 1
    },

    "total_tests": 497,
    "passing_tests": 497,
    "noleap_tests": 22,
    "golden_tests": 45,

    "typed_contracts": 67,
    "dataclass_count": 52,
    "protocol_count": 8,
    "enum_count": 15
  },

  "layers": [
    {
      "id": "A0",
      "name": "Algebra Kernel",
      "principle_ar": "النتيجة = القيمة + الرتبة + الدليل + البقايا + الأثر",
      "principle_en": "Result = value + rank + evidence + residuals + trace",

      "status": "IMPLEMENTED",
      "maturity_level": "IMPLEMENTED",

      "score_raw": 88,
      "score_capped": 70,
      "cap_reason": "No golden dataset",

      "components": {
        "typed_contract": 15,
        "runtime_implementation": 20,
        "evidence_policy": 10,
        "rank_policy": 9,
        "residual_taxonomy": 10,
        "noleap_tests": 10,
        "trace_replay": 9,
        "golden_dataset": 0,
        "doc_honesty": 5,
        "total": 88
      },

      "governance": {
        "has_evidence_policy": true,
        "evidence_count": 47,
        "evidence_types": ["trace", "operation", "source"],

        "has_rank_policy": true,
        "rank_ceiling": null,
        "rank_inflation_risk": "MEDIUM",

        "has_residual_taxonomy": true,
        "residual_count": 23,
        "linguistic_residuals": 18,
        "implementation_failures": 5,

        "noleap_coverage": 1.0,
        "noleap_tested": 12,
        "noleap_total": 12,

        "has_trace_replay": true,
        "trace_coverage": 0.85,

        "has_golden_dataset": false,
        "golden_coverage": 0.0,
        "golden_case_types": []
      },

      "files": {
        "contracts": [
          "src/fvafk/algebra/core.py"
        ],
        "implementations": [
          "src/fvafk/algebra/core.py",
          "src/fvafk/algebra/policies.py"
        ],
        "tests": [
          "tests/fvafk/algebra/test_core.py",
          "tests/fvafk/algebra/test_policies.py"
        ],
        "docs": [
          "docs/ALGEBRA_KERNEL.md"
        ],
        "total_lines": 1250,
        "code_lines": 850,
        "test_lines": 320,
        "doc_lines": 80
      },

      "forbidden_outputs": [],
      "allowed_outputs": ["Result", "Rank", "Evidence", "Residual", "Trace"],

      "gaps": [
        "No golden dataset for Result/Rank/Evidence",
        "Rank policy needs layer-specific requirements"
      ],
      "warnings": [
        "Trace usage audit needed"
      ],

      "next_action": {
        "pr": "PR-G1 Golden Dataset for Kernel",
        "priority": "HIGH",
        "blocking": ["A2", "A3", "A4"],
        "description": "Create golden dataset with positive/negative/ambiguous cases",
        "estimated_effort": "1 week"
      }
    },

    {
      "id": "A2",
      "name": "Pure Dāl Geometry",
      "principle_ar": "الدال يصنع الصورة",
      "principle_en": "Dāl makes the form",

      "status": "PARTIAL",
      "maturity_level": "PARTIAL",

      "score_raw": 68,
      "score_capped": 55,
      "cap_reason": "No NoLeap tests at 90%+ and no golden dataset",

      "components": {
        "typed_contract": 15,
        "runtime_implementation": 18,
        "evidence_policy": 8,
        "rank_policy": 9,
        "residual_taxonomy": 10,
        "noleap_tests": 7,
        "trace_replay": 9,
        "golden_dataset": 0,
        "doc_honesty": 4,
        "total": 80
      },

      "governance": {
        "has_evidence_policy": true,
        "evidence_count": 23,
        "evidence_types": ["phonic_carrier", "haraka_operation", "syllable"],

        "has_rank_policy": true,
        "rank_ceiling": "PARTIAL",
        "rank_inflation_risk": "LOW",

        "has_residual_taxonomy": true,
        "residual_count": 15,
        "linguistic_residuals": 13,
        "implementation_failures": 2,

        "noleap_coverage": 0.71,
        "noleap_tested": 5,
        "noleap_total": 7,

        "has_trace_replay": true,
        "trace_coverage": 0.82,

        "has_golden_dataset": false,
        "golden_coverage": 0.0,
        "golden_case_types": []
      },

      "files": {
        "contracts": [
          "src/gfa/methods/lafzi_dal/dal_candidate.py",
          "src/gfa/methods/lafzi_dal/dal_structures.py"
        ],
        "implementations": [
          "src/gfa/methods/lafzi_dal/dal_candidate_builder.py"
        ],
        "tests": [
          "tests/gfa/methods/test_pr_l3_pure_dal_geometry.py",
          "tests/gfa/methods/test_pr_l3_phase2_builder_integration.py"
        ],
        "docs": [
          "docs/PR_L3_PURE_DAL_GEOMETRY_SUMMARY.md",
          "docs/PR_L3_PHASE2_BUILDER_GUIDE.md"
        ],
        "total_lines": 2150,
        "code_lines": 1420,
        "test_lines": 650,
        "doc_lines": 80
      },

      "forbidden_outputs": ["meaning", "dalalah", "ifadah", "hukm"],
      "allowed_outputs": ["dal_candidate"],

      "gaps": [
        "NoLeap coverage at 71% (need 90%+)",
        "No golden dataset",
        "C2a gate orchestration needs debugging"
      ],
      "warnings": [],

      "next_action": {
        "pr": "PR-L3 Phase 4: Golden Dataset + NoLeap Tests",
        "priority": "CRITICAL",
        "blocking": ["A3", "A4", "A5"],
        "description": "Add 2 missing NoLeap tests and create complete golden dataset",
        "estimated_effort": "1 week"
      }
    }
  ],

  "claim_conflicts": [
    {
      "claim": "Ifādah fully implemented",
      "doc_location": "README.md:45",
      "code_reality": "boolean dict closure, no typed IfadahClosure",
      "test_reality": "No typed Ifadah tests",
      "severity": "HIGH",
      "risk": "HIGH",
      "recommended_fix": "PR-F7: Typed Ifādah Contract",
      "related_layer": "A7"
    },
    {
      "claim": "General Cognitive Algebra complete",
      "doc_location": "docs/ARCHITECTURE.md:12",
      "code_reality": "5/13 cognitive layers implemented",
      "test_reality": "Partial test coverage",
      "severity": "CRITICAL",
      "risk": "CRITICAL",
      "recommended_fix": "Update docs: 'foundation implemented, cognitive expansion planned'",
      "related_layer": "A9"
    }
  ],

  "noleap_violations": [
    {
      "source_layer": "DĀL",
      "target_layer": "MEANING",
      "forbidden_transition": "DĀL→MEANING",
      "guard_exists": true,
      "test_exists": true,
      "test_location": "tests/gfa/methods/test_noleap_dal_to_meaning.py",
      "risk": "LOW",
      "status": "GUARDED"
    },
    {
      "source_layer": "WADH",
      "target_layer": "HUKM",
      "forbidden_transition": "WADH→HUKM",
      "guard_exists": true,
      "test_exists": false,
      "test_location": null,
      "risk": "HIGH",
      "status": "UNGUARDED"
    },
    {
      "source_layer": "MADLUL",
      "target_layer": "IFADAH",
      "forbidden_transition": "MADLUL→IFADAH",
      "guard_exists": false,
      "test_exists": false,
      "test_location": null,
      "risk": "HIGH",
      "status": "MISSING"
    }
  ],

  "residual_issues": [
    {
      "location": "src/gfa/methods/lafzi_wadh/wadh_gate.py:145",
      "residual_value": "AttributeError: 'NoneType' object has no attribute 'source'",
      "issue_type": "MISLABELED",
      "severity": "HIGH",
      "layer": "A5",
      "recommended_fix": "Move to failures field, not residuals"
    },
    {
      "location": "src/gfa/methods/lafzi_dal/dal_candidate_builder.py:387",
      "residual_value": "unknown_classification_path",
      "issue_type": "UNCLASSIFIED",
      "severity": "MEDIUM",
      "layer": "A2",
      "recommended_fix": "Add to PathType enum or LinguisticResidual"
    }
  ],

  "ci_status": {
    "status": "PASSING",
    "latest_run": "2026-05-23T19:45:00Z",
    "workflow_name": "Python CI",
    "run_url": "https://github.com/sonaiso/-/actions/runs/12345",
    "failing_jobs": [],
    "error_summary": null
  },

  "test_summary": {
    "total": 497,
    "passing": 497,
    "failing": 0,
    "skipped": 0,

    "unit_tests": 389,
    "integration_tests": 86,
    "noleap_tests": 22,
    "golden_tests": 0,

    "coverage_percent": 87.5,
    "lines_covered": 6234,
    "lines_total": 7125
  }
}
```

---

## 15. Schema Validation

The JSON output MUST be validated against this schema using JSON Schema Draft 7.

**Validation Rules**:

1. All required fields present
2. Numbers in valid ranges (0-100 for percentages, etc.)
3. Enums match allowed values
4. Arrays non-empty where required
5. Foreign key references valid (e.g., layer IDs in blocking lists)

**Invalid Example** (will be rejected):

```json
{
  "overall_real_completion": 150,  // ❌ Must be 0-100
  "claim_inflation_risk": "SUPER_HIGH",  // ❌ Not in RiskLevel enum
  "layers": []  // ❌ Must have at least 1 layer
}
```

---

## 16. Schema Evolution

**Versioning**: Semantic versioning (MAJOR.MINOR.PATCH)

**Breaking changes** (increment MAJOR):
- Remove required field
- Change field type
- Remove enum value

**Non-breaking changes** (increment MINOR):
- Add optional field
- Add enum value
- Add new object type

**Patches** (increment PATCH):
- Documentation fixes
- Example updates

---

**Document Status**: SPECIFICATION (PR-D0)
**Last Updated**: 2026-05-23
**Next Review**: After PR-D1 implementation

---

## Appendix: TypeScript Types

Complete TypeScript definitions available at:
`tools/project_audit/types/dashboard-schema.d.ts` (to be created in PR-D1)
