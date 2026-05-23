"""
Type definitions for Dashboard Data Schema
تعريفات الأنواع لمخطط بيانات لوحة القياس

Based on DASHBOARD_DATA_SCHEMA.md (PR-D0)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class RiskLevel(Enum):
    """Risk level enumeration"""
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class LayerStatus(Enum):
    """Layer implementation status"""
    IMPLEMENTED = "IMPLEMENTED"
    PARTIAL = "PARTIAL"
    DEMONSTRATOR = "DEMONSTRATOR"
    PLANNED = "PLANNED"
    GAP = "GAP"


class MaturityLevel(Enum):
    """Layer maturity level with score ranges"""
    CERTIFIED = "CERTIFIED"  # 90-100%
    IMPLEMENTED = "IMPLEMENTED"  # 70-89%
    PARTIAL = "PARTIAL"  # 50-69%
    DEMONSTRATOR = "DEMONSTRATOR"  # 30-49%
    PLANNED = "PLANNED"  # 10-29%
    GAP = "GAP"  # 0-9%


class ConflictSeverity(Enum):
    """Claim conflict severity levels"""
    CRITICAL = "CRITICAL"  # Claim completely false
    HIGH = "HIGH"  # Major feature claimed but not typed
    MEDIUM = "MEDIUM"  # Partial implementation, misleading docs
    LOW = "LOW"  # Minor wording issue


class ViolationStatus(Enum):
    """NoLeap guard violation status"""
    GUARDED = "GUARDED"  # Guard + test exist
    UNGUARDED = "UNGUARDED"  # Guard exists, no test
    MISSING = "MISSING"  # No guard or test
    BYPASSED = "BYPASSED"  # Guard exists but can be bypassed


class IssueType(Enum):
    """Residual issue classification"""
    MISLABELED = "MISLABELED"  # Implementation error labeled as linguistic
    UNCLASSIFIED = "UNCLASSIFIED"  # Not in known taxonomy
    MIXED = "MIXED"  # Linguistic + implementation mixed
    MISSING_TAXONOMY = "MISSING_TAXONOMY"  # No taxonomy defined


class Priority(Enum):
    """Action priority levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


@dataclass
class LayerScoreComponents:
    """Score components for layer evaluation (0-100 total)"""
    typed_contract: int  # 0-15
    runtime_implementation: int  # 0-20
    evidence_policy: int  # 0-10
    rank_policy: int  # 0-10
    residual_taxonomy: int  # 0-10
    noleap_tests: int  # 0-10
    trace_replay: int  # 0-10
    golden_dataset: int  # 0-10
    doc_honesty: int  # 0-5

    @property
    def total(self) -> int:
        """Calculate total score"""
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


@dataclass
class LayerGovernance:
    """Governance metrics for a layer"""
    has_evidence_policy: bool
    evidence_count: int
    evidence_types: List[str]

    has_rank_policy: bool
    rank_ceiling: Optional[str]
    rank_inflation_risk: RiskLevel

    has_residual_taxonomy: bool
    residual_count: int
    linguistic_residuals: int
    implementation_failures: int

    noleap_coverage: float  # 0.0-1.0
    noleap_tested: int
    noleap_total: int

    has_trace_replay: bool
    trace_coverage: float  # 0.0-1.0

    has_golden_dataset: bool
    golden_coverage: float  # 0.0-1.0
    golden_case_types: List[str]


@dataclass
class LayerFiles:
    """File references for a layer"""
    contracts: List[str] = field(default_factory=list)
    implementations: List[str] = field(default_factory=list)
    tests: List[str] = field(default_factory=list)
    docs: List[str] = field(default_factory=list)

    total_lines: int = 0
    code_lines: int = 0
    test_lines: int = 0
    doc_lines: int = 0


@dataclass
class NextAction:
    """Next required action for layer advancement"""
    pr: str
    priority: Priority
    blocking: List[str]
    description: str
    estimated_effort: Optional[str] = None


@dataclass
class Layer:
    """Complete layer assessment"""
    # Identity
    id: str
    name: str
    principle_ar: str
    principle_en: str

    # Maturity
    status: LayerStatus
    maturity_level: MaturityLevel

    # Scoring
    score_raw: int
    score_capped: int
    cap_reason: Optional[str]

    # Components
    components: LayerScoreComponents
    governance: LayerGovernance
    files: LayerFiles

    # Boundaries
    forbidden_outputs: List[str]
    allowed_outputs: List[str]

    # Issues
    gaps: List[str]
    warnings: List[str]

    # Next steps
    next_action: Optional[NextAction]


@dataclass
class ClaimConflict:
    """Documentation claim vs code reality conflict"""
    claim: str
    doc_location: str
    code_reality: str
    test_reality: str
    severity: ConflictSeverity
    risk: RiskLevel
    recommended_fix: str
    related_layer: Optional[str] = None


@dataclass
class NoLeapViolation:
    """Forbidden layer transition violation"""
    source_layer: str
    target_layer: str
    forbidden_transition: str

    guard_exists: bool
    test_exists: bool
    test_location: Optional[str]

    risk: RiskLevel
    status: ViolationStatus


@dataclass
class ResidualIssue:
    """Residual taxonomy violation"""
    location: str
    residual_value: str
    issue_type: IssueType
    severity: RiskLevel
    layer: Optional[str]
    recommended_fix: str


@dataclass
class CIStatus:
    """CI/CD status"""
    status: str  # PASSING, FAILING, DEGRADED, UNKNOWN
    latest_run: str
    workflow_name: str
    run_url: Optional[str]
    failing_jobs: List[str] = field(default_factory=list)
    error_summary: Optional[str] = None


@dataclass
class TestSummary:
    """Test execution summary"""
    total: int
    passing: int
    failing: int
    skipped: int

    unit_tests: int
    integration_tests: int
    noleap_tests: int
    golden_tests: int

    coverage_percent: Optional[float] = None
    lines_covered: Optional[int] = None
    lines_total: Optional[int] = None


@dataclass
class DashboardMetrics:
    """Top-level dashboard metrics"""
    # Primary metrics
    noleap_coverage: float  # 0-100
    trace_coverage: float  # 0-100
    golden_coverage: float  # 0-100
    rank_inflation_risk: RiskLevel
    residual_debt: int

    # Maturity breakdown
    layers_by_maturity: Dict[str, int]

    # Test statistics
    total_tests: int
    passing_tests: int
    noleap_tests: int
    golden_tests: int

    # Code statistics
    typed_contracts: int
    dataclass_count: int
    protocol_count: int
    enum_count: int


@dataclass
class ProjectGovernanceStatus:
    """Complete project governance status report"""
    # Metadata
    project: str
    generated_at: str
    version: str
    generator_version: str

    # Top-level metrics
    overall_real_completion: float
    claim_inflation_risk: RiskLevel

    # Detailed metrics
    metrics: DashboardMetrics

    # Layer details
    layers: List[Layer]

    # Issues
    claim_conflicts: List[ClaimConflict]
    noleap_violations: List[NoLeapViolation]
    residual_issues: List[ResidualIssue]

    # CI/Test status
    ci_status: CIStatus
    test_summary: TestSummary
