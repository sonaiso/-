# Governance Metrics Definition
# تعريف مقاييس الحوكمة

**Version**: 1.0.0
**Part of**: PR-D0 Dashboard Specification
**Date**: 2026-05-23

---

## 1. Overview

This document defines the precise calculation methods for all governance metrics used in the Governed Project Maturity Dashboard.

**Core Principle:**

```text
Metrics must be:
- Objective (code/test-based, not opinion)
- Verifiable (reproducible from repo state)
- Resistant to gaming (caps prevent inflation)
- Honest (reveal gaps, not hide them)
```

---

## 2. Primary Metrics

### 2.1 Real Completion

**Definition**: Weighted average of capped layer scores.

**Formula**:

```python
def calculate_real_completion(layers: List[Layer]) -> float:
    """
    Real Completion = Σ(layer.score_capped × layer.weight) / Σ(layer.weight)

    Weight factors:
    - Kernel layers (A0, A1): 1.5x
    - Foundational layers (A2-A5): 1.0x
    - Advanced layers (A6-A8): 1.0x
    - Cognitive expansion (A9): 0.8x
    - Quality assurance (A10): 1.2x
    """
    total_weighted_score = 0
    total_weight = 0

    for layer in layers:
        weight = get_layer_weight(layer.id)
        total_weighted_score += layer.score_capped * weight
        total_weight += weight

    return (total_weighted_score / total_weight) if total_weight > 0 else 0

def get_layer_weight(layer_id: str) -> float:
    weights = {
        "A0": 1.5,  # Kernel
        "A1": 1.5,  # Typed Layers
        "A2": 1.0,  # Pure Dāl
        "A3": 1.0,  # Madlūl-Lafẓī
        "A4": 1.0,  # Binding
        "A5": 1.0,  # Wadh
        "A6": 1.0,  # Dalālah
        "A7": 1.0,  # Ifādah
        "A8": 1.0,  # Hukm Boundary
        "A9": 0.8,  # Cognitive (planned)
        "A10": 1.2, # Golden/Audit (quality gate)
    }
    return weights.get(layer_id, 1.0)
```

**Interpretation**:
- 0-29%: Foundation incomplete
- 30-49%: Demonstrators exist
- 50-69%: Partial implementation
- 70-89%: Implemented, needs certification
- 90-100%: Certified

**Current Baseline**: ~42% (as of PR-L3 Phase 2)

---

### 2.2 Claim Inflation Risk

**Definition**: Severity of discrepancy between documentation claims and code reality.

**Calculation**:

```python
from enum import Enum
from dataclasses import dataclass
from typing import List

class ConflictSeverity(Enum):
    CRITICAL = "critical"    # Claim completely false
    HIGH = "high"            # Major feature claimed but not typed
    MEDIUM = "medium"        # Partial implementation, misleading docs
    LOW = "low"              # Minor wording issue

@dataclass
class ClaimConflict:
    claim: str
    doc_location: str
    code_reality: str
    test_reality: str
    severity: ConflictSeverity

def calculate_claim_inflation_risk(conflicts: List[ClaimConflict]) -> str:
    """
    Risk levels:
    - CRITICAL: Any critical conflict OR ≥5 high conflicts
    - HIGH: ≥3 high conflicts OR ≥6 medium conflicts
    - MEDIUM: 1-2 high conflicts OR 3-5 medium conflicts
    - LOW: ≤2 medium conflicts, no high
    - NONE: No conflicts
    """
    critical_count = sum(1 for c in conflicts if c.severity == ConflictSeverity.CRITICAL)
    high_count = sum(1 for c in conflicts if c.severity == ConflictSeverity.HIGH)
    medium_count = sum(1 for c in conflicts if c.severity == ConflictSeverity.MEDIUM)

    if critical_count > 0 or high_count >= 5:
        return "CRITICAL"
    elif high_count >= 3 or medium_count >= 6:
        return "HIGH"
    elif high_count >= 1 or medium_count >= 3:
        return "MEDIUM"
    elif medium_count > 0:
        return "LOW"
    else:
        return "NONE"
```

**Detection Method**:

1. Parse documentation for claims (grep for "implemented", "complete", "supports")
2. Find corresponding code implementation
3. Check if typed contract exists
4. Check if tests exist
5. Classify conflict severity

**Examples**:

```python
conflicts = [
    ClaimConflict(
        claim="Ifādah fully implemented",
        doc_location="README.md:45",
        code_reality="boolean dict closure, no typed IfahClosure",
        test_reality="No typed Ifadah tests",
        severity=ConflictSeverity.HIGH
    ),
    ClaimConflict(
        claim="General Cognitive Algebra complete",
        doc_location="docs/ARCHITECTURE.md:12",
        code_reality="5/13 layers implemented",
        test_reality="Partial test coverage",
        severity=ConflictSeverity.CRITICAL
    ),
]

risk = calculate_claim_inflation_risk(conflicts)
# Returns: "CRITICAL"
```

---

### 2.3 NoLeap Coverage

**Definition**: Percentage of forbidden layer transitions with test guards.

**Formula**:

```python
def calculate_noleap_coverage(guards: List[NoLeapGuard]) -> float:
    """
    NoLeap Coverage = tested_guards / total_guards × 100
    """
    total = len(guards)
    tested = sum(1 for g in guards if g.has_test)

    return (tested / total * 100) if total > 0 else 0

@dataclass
class NoLeapGuard:
    source_layer: str
    target_layer: str
    guard_exists: bool      # Code guard exists
    has_test: bool          # Test for guard exists
    test_location: str      # Path to test file
```

**Forbidden Transitions** (Must be guarded):

| Source | Target | Rationale |
|--------|--------|-----------|
| MORPH_SURFACE | SEMANTICS | No meaning without Wadh |
| SEMANTICS | HUKM | No judgment without Ifādah |
| IFADAH | HUKM | Ifādah ≠ Hukm |
| DĀL | MEANING | Dāl is signifier, not signified |
| BINDING | DALĀLAH | Binding ≠ relation determination |
| WADH | HUKM | Licensing ≠ judgment |
| MADLUL | IFADAH | Conception ≠ predication |
| TASAWWUR | HUKM | Conception ≠ judgment |
| ATOMS | ENTITIES | Atoms ≠ semantic units |
| PHONOLOGY | SYNTAX | Sound ≠ structure |

**Test Pattern**:

```python
# Example: tests/gfa/methods/test_noleap_dal_to_meaning.py
def test_noleap_dal_cannot_create_meaning():
    """Guard: Dāl CANNOT produce external meaning directly."""
    dal = DalCandidate(...)

    # Verify no meaning field
    assert not hasattr(dal, "meaning")
    assert not hasattr(dal, "murad")
    assert not hasattr(dal, "external_referent")

    # Verify attempting to access raises appropriate error
    with pytest.raises(AttributeError):
        _ = dal.meaning
```

**Current Baseline**: ~73% (22/30 guards tested)

---

### 2.4 Rank Inflation Risk

**Definition**: Risk of results achieving `CERTIFIED` rank without sufficient evidence.

**Calculation**:

```python
from enum import Enum

class RankInflationRisk(Enum):
    CRITICAL = "critical"  # Auto-certify without evidence requirements
    HIGH = "high"          # Ceiling undefined or permissive
    MEDIUM = "medium"      # Ceiling exists but not layer-specific
    LOW = "low"            # Layer-specific ceiling enforced
    NONE = "none"          # Per-evidence-type ceiling + required evidence

def assess_rank_inflation_risk(layer: Layer) -> RankInflationRisk:
    """
    Check if layer can produce CERTIFIED rank without proper evidence.
    """
    # Critical: No rank policy at all
    if not layer.has_rank_policy:
        return RankInflationRisk.CRITICAL

    # High: Generic ceiling, no layer-specific requirements
    if not layer.has_required_evidence_policy:
        return RankInflationRisk.HIGH

    # Medium: Has policy but not enforced in code
    if not layer.rank_ceiling_enforced_in_code:
        return RankInflationRisk.MEDIUM

    # Low: Has policy and enforcement but no per-evidence-type rules
    if not layer.has_evidence_type_rank_map:
        return RankInflationRisk.LOW

    # None: Complete rank governance
    return RankInflationRisk.NONE
```

**Required Evidence Policy** (per layer):

```python
# Example: A5 Wadh layer
required_evidence_wadh = {
    "CERTIFIED": [
        "transmission_evidence",     # Riwayah/naql required
        "source_evidence",            # Lexicon or expert source
        "scope_evidence",             # Clear boundaries
        "mawdu_lah_structure"         # Linguistic structure
    ],
    "LICENSED": [
        "transmission_evidence",
        "source_evidence"
    ],
    "CANDIDATE": [
        "source_evidence"
    ]
}
```

**Current Issue**: Generic rank policy in `fvafk/algebra/policies.py` allows CERTIFIED with any evidence that has no residuals. Need layer-specific required evidence.

---

### 2.5 Residual Debt

**Definition**: Count of residuals that are mislabeled or unclassified.

**Formula**:

```python
from typing import List, Set

@dataclass
class ResidualIssue:
    location: str           # File:line
    residual_value: str     # The residual itself
    issue_type: str         # MISLABELED | UNCLASSIFIED | MIXED
    severity: str           # HIGH | MEDIUM | LOW

def calculate_residual_debt(issues: List[ResidualIssue]) -> int:
    """
    Residual Debt = count of HIGH severity issues
    """
    return sum(1 for issue in issues if issue.severity == "HIGH")

def detect_residual_issues(results: List[Result]) -> List[ResidualIssue]:
    """
    Scan for residual taxonomy violations.
    """
    issues = []

    # Linguistic residuals (acceptable)
    linguistic_patterns = {
        "missing_haraka",
        "ambiguous_root",
        "multiple_patterns",
        "idiomatic_expression",
        "rare_usage",
    }

    # Implementation failures (NOT linguistic)
    implementation_patterns = {
        "AttributeError",
        "KeyError",
        "TypeError",
        "IndexError",
        "NoneType",
        "import_error",
    }

    for result in results:
        for residual in result.residuals:
            # Check for implementation error labeled as linguistic
            if any(pattern in residual for pattern in implementation_patterns):
                issues.append(ResidualIssue(
                    location=result.trace.source if result.trace else "unknown",
                    residual_value=residual,
                    issue_type="MISLABELED",
                    severity="HIGH"
                ))

            # Check for unclassified residual
            if not any(pattern in residual for pattern in
                      linguistic_patterns | implementation_patterns):
                issues.append(ResidualIssue(
                    location=result.trace.source if result.trace else "unknown",
                    residual_value=residual,
                    issue_type="UNCLASSIFIED",
                    severity="MEDIUM"
                ))

    return issues
```

**Example**:

```python
# BAD: Implementation error as linguistic residual
Result(
    value=dal_candidate,
    rank=Rank.CANDIDATE,
    residuals=frozenset(["AttributeError: 'NoneType' object has no attribute 'stem'"]),
    # ^ This is a BUG, not a linguistic residual!
)

# GOOD: Properly classified
Result(
    value=dal_candidate,
    rank=Rank.CANDIDATE,
    residuals=frozenset(["missing_haraka"]),  # Linguistic
    failures=frozenset(["stem_extraction_failed"]),  # Implementation
)
```

---

### 2.6 Trace Coverage

**Definition**: Percentage of `Result` objects with replay-capable `Trace`.

**Formula**:

```python
def calculate_trace_coverage(results: List[Result]) -> float:
    """
    Trace Coverage = results_with_trace / total_results × 100

    A valid trace must:
    - Be non-None
    - Have source field
    - Have operation field
    - Be replay-capable (has enough info to reproduce)
    """
    total = len(results)
    with_trace = sum(1 for r in results if has_valid_trace(r))

    return (with_trace / total * 100) if total > 0 else 0

def has_valid_trace(result: Result) -> bool:
    """Check if Result has a replay-capable trace."""
    if result.trace is None:
        return False

    trace = result.trace

    # Must have source
    if not hasattr(trace, 'source') or not trace.source:
        return False

    # Must have operation
    if not hasattr(trace, 'operation') or not trace.operation:
        return False

    # Must be replay-capable (if method exists)
    if hasattr(trace, 'is_reversible'):
        return trace.is_reversible()

    return True
```

**Current Baseline**: ~58% (estimated based on recent PRs)

---

### 2.7 Golden Dataset Coverage

**Definition**: Percentage of layers with complete golden dataset.

**Formula**:

```python
from enum import Enum

class GoldenCaseType(Enum):
    POSITIVE = "positive"         # Should succeed
    NEGATIVE = "negative"         # Should fail gracefully
    AMBIGUOUS = "ambiguous"       # Multiple valid interpretations
    BLOCKED = "blocked"           # NoLeap guard triggers
    RANK_LOWERING = "rank_lowering"  # Evidence insufficient
    RESIDUAL_RICH = "residual_rich"  # Multiple residuals

@dataclass
class GoldenDataset:
    layer_id: str
    cases: Dict[GoldenCaseType, List[str]]  # type -> example IDs

    def is_complete(self) -> bool:
        """
        Complete dataset must have:
        - ≥5 positive cases
        - ≥3 negative cases
        - ≥2 ambiguous cases
        - ≥1 blocked case
        - ≥1 rank-lowering case
        """
        return (
            len(self.cases.get(GoldenCaseType.POSITIVE, [])) >= 5 and
            len(self.cases.get(GoldenCaseType.NEGATIVE, [])) >= 3 and
            len(self.cases.get(GoldenCaseType.AMBIGUOUS, [])) >= 2 and
            len(self.cases.get(GoldenCaseType.BLOCKED, [])) >= 1 and
            len(self.cases.get(GoldenCaseType.RANK_LOWERING, [])) >= 1
        )

def calculate_golden_coverage(datasets: List[GoldenDataset]) -> float:
    """
    Golden Coverage = complete_datasets / total_layers × 100
    """
    complete = sum(1 for ds in datasets if ds.is_complete())
    total = len(datasets)

    return (complete / total * 100) if total > 0 else 0
```

**Current Baseline**: ~40% (4/10 layers have partial golden coverage)

---

### 2.8 CI Health

**Definition**: Latest CI/CD pipeline status.

**Values**:
- `PASSING`: All tests passing, no failures
- `FAILING`: One or more test failures
- `DEGRADED`: Passing but with warnings
- `UNKNOWN`: CI not run or unavailable

**Extraction**:

```python
import requests
from typing import Optional

def get_ci_status(repo: str, branch: str = "main") -> str:
    """
    Fetch CI status from GitHub Actions API.
    """
    url = f"https://api.github.com/repos/{repo}/actions/runs"
    params = {"branch": branch, "per_page": 1}

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return "UNKNOWN"

    data = response.json()
    if not data.get("workflow_runs"):
        return "UNKNOWN"

    latest_run = data["workflow_runs"][0]
    conclusion = latest_run.get("conclusion")

    if conclusion == "success":
        return "PASSING"
    elif conclusion in ("failure", "timed_out", "cancelled"):
        return "FAILING"
    elif conclusion == "skipped":
        return "DEGRADED"
    else:
        return "UNKNOWN"
```

---

## 3. Layer-Specific Metrics

### 3.1 Raw Score Calculation

```python
@dataclass
class LayerScoreComponents:
    typed_contract: int        # 0-15
    runtime_implementation: int  # 0-20
    evidence_policy: int       # 0-10
    rank_policy: int           # 0-10
    residual_taxonomy: int     # 0-10
    noleap_tests: int          # 0-10
    trace_replay: int          # 0-10
    golden_dataset: int        # 0-10
    doc_honesty: int           # 0-5

    @property
    def total(self) -> int:
        return (
            self.typed_contract +
            self.runtime_implementation +
            self.evidence_policy +
            self.rank_policy +
            self.residual_taxonomy +
            self.noleap_tests +
            self.trace_replay +
            self.golden_dataset +
            self.doc_honesty
        )

def score_layer(layer: Layer) -> LayerScoreComponents:
    """Calculate raw score for a layer."""
    return LayerScoreComponents(
        typed_contract=score_typed_contract(layer),
        runtime_implementation=score_runtime(layer),
        evidence_policy=score_evidence_policy(layer),
        rank_policy=score_rank_policy(layer),
        residual_taxonomy=score_residual_taxonomy(layer),
        noleap_tests=score_noleap_tests(layer),
        trace_replay=score_trace_replay(layer),
        golden_dataset=score_golden_dataset(layer),
        doc_honesty=score_doc_honesty(layer),
    )
```

### 3.2 Ceiling Application

```python
def apply_ceiling(layer: Layer, raw_score: int) -> tuple[int, str]:
    """
    Apply ceiling caps to raw score.

    Returns: (capped_score, cap_reason)
    """
    # Check caps in order of severity

    if not layer.has_typed_contract:
        return (min(raw_score, 30), "No typed contract")

    if layer.uses_strings_instead_of_types:
        return (min(raw_score, 45), "Strings/booleans instead of typed candidates")

    if not layer.has_tests:
        return (min(raw_score, 50), "No tests")

    if not layer.has_noleap_tests:
        return (min(raw_score, 55), "No NoLeap tests")

    if layer.trace_broken:
        return (min(raw_score, 60), "Broken trace/replay")

    if layer.has_claim_conflicts:
        return (min(raw_score, 70), "Claim/code conflict")

    if not layer.has_golden_dataset:
        return (min(raw_score, 70), "No golden dataset")

    # No cap
    return (raw_score, "")
```

---

## 4. Metric Update Schedule

| Metric | Update Frequency | Trigger |
|--------|-----------------|---------|
| Real Completion | On every PR merge | CI post-merge |
| Claim Inflation Risk | Weekly + on doc change | Cron + doc commit |
| NoLeap Coverage | On test file change | CI |
| Rank Inflation Risk | Monthly | Manual audit |
| Residual Debt | On every PR merge | CI |
| Trace Coverage | On every PR merge | CI |
| Golden Dataset Coverage | On test file change | CI |
| CI Health | On every CI run | GitHub Actions |

---

## 5. Metric Thresholds

**Alert Levels:**

| Metric | Green | Yellow | Orange | Red |
|--------|-------|--------|--------|-----|
| Real Completion | ≥70% | 50-69% | 30-49% | <30% |
| Claim Inflation | NONE/LOW | MEDIUM | HIGH | CRITICAL |
| NoLeap Coverage | ≥90% | 70-89% | 50-69% | <50% |
| Trace Coverage | ≥80% | 60-79% | 40-59% | <40% |
| Golden Coverage | ≥80% | 50-79% | 30-49% | <30% |
| Residual Debt | 0-2 | 3-5 | 6-10 | >10 |

**PR Merge Requirements** (Suggested):
- Real Completion: Must not decrease
- Claim Inflation: Must not increase to CRITICAL
- NoLeap Coverage: Must not decrease
- CI Health: Must be PASSING

---

## 6. Examples

### Example 1: Layer A2 (Pure Dāl Geometry)

```python
layer_a2 = Layer(
    id="A2",
    name="Pure Dāl Geometry",
    # Raw scoring
    has_typed_contract=True,           # 15 points
    runtime_implementation=0.9,        # 18/20 points
    has_evidence_policy=True,          # 8/10 points
    has_rank_policy=True,              # 9/10 points
    has_residual_taxonomy=True,        # 10/10 points
    noleap_coverage=0.71,              # 7/10 points (5/7 tests)
    trace_replay_working=True,         # 9/10 points
    has_golden_dataset=False,          # 0/10 points
    doc_matches_code=True,             # 4/5 points
)

raw_score = 15 + 18 + 8 + 9 + 10 + 7 + 9 + 0 + 4 = 80

# Apply ceiling
capped_score, reason = apply_ceiling(layer_a2, raw_score)
# Result: capped_score = 55, reason = "No golden dataset"
```

### Example 2: Project-Wide Real Completion

```python
layers = [
    Layer(id="A0", score_capped=85, weight=1.5),
    Layer(id="A1", score_capped=82, weight=1.5),
    Layer(id="A2", score_capped=55, weight=1.0),
    Layer(id="A3", score_capped=45, weight=1.0),
    Layer(id="A4", score_capped=78, weight=1.0),
    Layer(id="A5", score_capped=45, weight=1.0),
    Layer(id="A6", score_capped=58, weight=1.0),
    Layer(id="A7", score_capped=35, weight=1.0),
    Layer(id="A8", score_capped=72, weight=1.0),
    Layer(id="A9", score_capped=15, weight=0.8),
    Layer(id="A10", score_capped=22, weight=1.2),
]

real_completion = calculate_real_completion(layers)
# Result: ~42%
```

---

## 7. Validation

All metrics must be:

1. **Reproducible**: Same repo state → same metric values
2. **Auditable**: Calculation logic documented and open
3. **Resistant to gaming**: Caps prevent artificial inflation
4. **Actionable**: Clear path to improvement
5. **Honest**: Reveal gaps, don't hide them

---

**Document Status**: SPECIFICATION (PR-D0)
**Last Updated**: 2026-05-23
**Next Review**: After PR-D1 implementation
