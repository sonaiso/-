# Project Audit Tools
# أدوات مراجعة المشروع

Static audit generator for Governed Project Maturity Dashboard.

## Overview

This tool implements PR-D1: Static Audit Generator, which converts the governance specifications from PR-D0 into working code that produces objective, evidence-based maturity metrics.

## Installation

No additional dependencies required beyond standard library.

## Usage

### Generate Dashboard Report

```bash
python tools/project_audit/generate_dashboard_report.py \
  --output governance_dashboard.json
```

### Custom Project Root

```bash
python tools/project_audit/generate_dashboard_report.py \
  --project-root /path/to/project \
  --output report.json
```

## Output

Generates JSON report matching `DASHBOARD_DATA_SCHEMA.md`:

- Overall real completion percentage
- Layer-by-layer scores with ceiling caps
- NoLeap coverage analysis
- Golden dataset coverage
- Claim conflict detection
- Blocking gaps identification

## Tests

```bash
pytest tests/project_audit/test_generate_dashboard_report.py -v
```

## Components

- `types.py` - Type definitions from DASHBOARD_DATA_SCHEMA.md
- `code_analyzer.py` - Static code analysis (AST parsing)
- `test_analyzer.py` - Test coverage analysis
- `scorer.py` - Layer scoring with ceiling enforcement
- `generate_dashboard_report.py` - Main report generator

## Scoring Logic

Per GOVERNANCE_METRICS.md:

- Typed contract: 15 points
- Runtime implementation: 20 points
- Evidence policy: 10 points
- Rank policy: 10 points
- Residual taxonomy: 10 points
- NoLeap tests: 10 points
- Trace/replay: 10 points
- Golden dataset: 10 points
- Documentation honesty: 5 points

**Total**: 100 points

## Ceiling Caps

Strictly enforced per LAYER_MATURITY_MODEL.md:

| Condition | Max Score |
|-----------|-----------|
| No typed contract | 30% |
| Strings instead of types | 45% |
| No tests | 50% |
| No NoLeap tests | 55% |
| Broken trace/replay | 60% |
| Claim conflicts | 70% |
| No golden dataset | 70% |

## Layer Definitions

11 layers from A0 (Algebra Kernel) to A10 (Golden Dataset + Audit):

- A0: Result/Rank/Evidence/Residual/Trace foundation
- A1: Typed layer definitions
- A2: Pure Dāl Geometry (الدال يصنع الصورة)
- A3: Madlūl-Lafẓī (يفتح التصور اللفظي)
- A4: Neutral Binding (ربط محايد)
- A5: Wadh Geometry (يرخّص المعنى)
- A6: Dalālah Gates (تحدد العلاقة)
- A7: Nisbah/Ifādah (تكمل النسبة)
- A8: Hukm Boundary (منع القفز للحكم)
- A9: General Cognitive Layers
- A10: Golden Dataset + Audit

## Example Output

```json
{
  "project": "General Cognitive Arabic Algebra",
  "overall_real_completion": 38.7,
  "claim_inflation_risk": "NONE",
  "metrics": {
    "noleap_coverage": 10.0,
    "golden_coverage": 0.0,
    "layers_by_maturity": {
      "PARTIAL": 5,
      "DEMONSTRATOR": 5,
      "PLANNED": 1
    }
  }
}
```

## Constitutional Principles

Enforces:
- **لا مخرج عارٍ** (No bare output) - All scores require evidence
- **No claim inflation** - Ceiling caps prevent artificial scores
- **Transparent gaps** - Blocking issues clearly identified
- **Data-driven decisions** - Metrics guide next steps

## Version

0.1.0 (PR-D1)

## See Also

- [DASHBOARD_SPEC.md](../../docs/DASHBOARD_SPEC.md)
- [GOVERNANCE_METRICS.md](../../docs/GOVERNANCE_METRICS.md)
- [LAYER_MATURITY_MODEL.md](../../docs/LAYER_MATURITY_MODEL.md)
- [DASHBOARD_DATA_SCHEMA.md](../../docs/DASHBOARD_DATA_SCHEMA.md)
- [PR_D1_IMPLEMENTATION_SUMMARY.md](../../PR_D1_IMPLEMENTATION_SUMMARY.md)
