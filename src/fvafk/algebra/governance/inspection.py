"""Inspection Algebra — Constitutional verification following the rational method.

Authority: PR-INS1

Core Principle:

    Verification is a cognitive operation, not pattern matching.

    Bare regex → boolean violates constitution.
    Governed inspection:
        artifact → evidence → counter_evidence → finding → rank → residuals → trace

Critical Laws Enforced:

1. No bare output (لا مخرج عارٍ)
2. Evidence hierarchy (CI logs > tests > source > diff > PR body > docs)
3. Counter-evidence detection (negation markers, context clues)
4. Claim-evidence binding (claims must be verified against artifacts)
5. Specificity ordering (specific failures precede general failures)
6. Full trace preservation (replay chain for audit)
7. Residuals make rank explicit (no silent failures)
8. Every finding carries rank (no ungrounded claims)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal, Tuple

from ..core import Rank


class InspectionResidualKind(Enum):
    """Types of inspection residuals."""

    CLAIM_WITHOUT_EVIDENCE = "claim_without_evidence"
    CLAIM_INFLATION = "claim_inflation"  # Claimed file not in changed files
    WEAK_EVIDENCE = "weak_evidence"  # Only PR body claim, no source verification
    AMBIGUOUS_NEGATION = "ambiguous_negation"  # Negation marker but context unclear
    MISSING_COUNTER_EVIDENCE_CHECK = "missing_counter_evidence_check"
    INSUFFICIENT_SPECIFICITY = "insufficient_specificity"  # General check before specific
    UNTESTED_CLAIM = "untested_claim"  # No test coverage for claimed behavior


@dataclass(frozen=True)
class InspectionResidual:
    """What the inspection did not resolve.

    Residuals are the explicit reason an inspection finding is not CERTIFIED.
    Examples:
    - Claim in PR body but not verified against changed files
    - Weak evidence (regex match only, no source code verification)
    - Ambiguous negation context
    """

    kind: InspectionResidualKind
    description: str
    location: str = ""  # Where in artifact (line number, section, etc.)

    def __post_init__(self) -> None:
        if not self.description:
            raise ValueError("InspectionResidual.description must be non-empty")


@dataclass(frozen=True)
class InspectionArtifact:
    """What is being inspected.

    An artifact is the raw material for inspection:
    - pr_body: The PR description text
    - diff: Git diff output
    - changed_files: List of files changed in PR
    - source_file: Source code file content
    - test_log: Test execution output
    - workflow: CI workflow logs

    Evidence hierarchy (strongest to weakest):
    1. workflow (CI logs showing actual execution)
    2. test_log (test results)
    3. source_file (actual code)
    4. diff (changes made)
    5. changed_files (file list)
    6. pr_body (claims in description)
    """

    kind: Literal["pr_body", "diff", "changed_files", "source_file", "test_log", "workflow"]
    content_ref: str  # File path, section name, or identifier
    trace: str  # How this artifact was obtained

    def __post_init__(self) -> None:
        if not self.content_ref:
            raise ValueError("InspectionArtifact.content_ref must be non-empty")
        if not self.trace:
            raise ValueError("InspectionArtifact.trace must be non-empty")

    def evidence_weight(self) -> float:
        """Return evidence weight based on artifact kind.

        Returns:
            Float in range (0, 1] where higher means stronger evidence.
        """
        weights = {
            "workflow": 1.0,
            "test_log": 0.9,
            "source_file": 0.8,
            "diff": 0.6,
            "changed_files": 0.5,
            "pr_body": 0.3,
        }
        return weights.get(self.kind, 0.1)


@dataclass(frozen=True)
class InspectionFinding:
    """A single inspection finding following the rational method.

    Structure:
    - claim: What is being claimed (e.g., "New architectural construct added")
    - evidence: Supporting observations (checkbox checked, file in diff, etc.)
    - counter_evidence: Contradicting observations (negation markers, context clues)
    - rank: Epistemic status of the finding
    - residuals: What was not resolved
    - trace: Full provenance chain

    Critical Laws:
    - No finding without claim
    - No rank >= LICENSED without evidence
    - No CERTIFIED with residuals
    - Counter-evidence must be checked before concluding
    """

    claim: str
    evidence: Tuple[str, ...] = ()
    counter_evidence: Tuple[str, ...] = ()
    rank: Rank = Rank.UNRESOLVED
    residuals: Tuple[InspectionResidual, ...] = ()
    trace: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.claim:
            raise ValueError("InspectionFinding.claim must be non-empty")

        # Constitutional invariants (same as Result)
        if self.rank in (Rank.LICENSED, Rank.CERTIFIED) and not self.evidence:
            raise ValueError(
                "Finding with rank >= LICENSED requires evidence "
                "(la-mukhraj-arin invariant)"
            )

        if self.rank is Rank.CERTIFIED and self.residuals:
            raise ValueError(
                "Finding cannot be CERTIFIED while residuals remain"
            )

        # Counter-evidence blocks high ranks
        if self.counter_evidence and self.rank in (Rank.CERTIFIED, Rank.LICENSED):
            raise ValueError(
                "Finding with counter-evidence cannot be >= LICENSED; "
                "must resolve contradiction or demote to CANDIDATE"
            )

    def is_blocked(self) -> bool:
        """Return True if counter-evidence blocks this finding."""
        return bool(self.counter_evidence)

    def is_certified(self) -> bool:
        """Return True if finding is CERTIFIED (strong evidence, no residuals)."""
        return self.rank is Rank.CERTIFIED


@dataclass(frozen=True)
class InspectionReport:
    """Domain report structure for inspection operations.

    This is a DOMAIN VALUE, not a constitutional judgment container.
    It holds inspection-specific information (status, findings, replay)
    but does NOT carry constitutional judgment fields (rank, residuals, evidence).

    Constitutional judgment is carried by Result[InspectionReport] from fvafk.algebra.

    Status semantics (domain-level only):
    - PASS: All findings CERTIFIED or no blocking findings
    - FAIL: At least one finding REFUTED or BLOCKED
    - NEEDS_REVIEW: Mixed findings or residuals present

    Note: This is NOT InspectionResult. InspectionResult was a parallel kernel
    which violated ARCH0. This is the domain report carried inside Result[...].
    """

    status: Literal["PASS", "FAIL", "NEEDS_REVIEW"]
    findings: Tuple[InspectionFinding, ...] = ()
    replay: Tuple[str, ...] = ()

    def __post_init__(self) -> None:
        # Status must be consistent with findings
        if self.status == "FAIL":
            # FAIL requires at least one REFUTED finding or explicit blocking
            has_refuted = any(f.rank is Rank.REFUTED for f in self.findings)
            has_blocked = any(f.is_blocked() for f in self.findings)
            if not (has_refuted or has_blocked):
                raise ValueError(
                    "InspectionReport with status=FAIL requires at least one "
                    "REFUTED or blocked finding"
                )

        if self.status == "PASS":
            # PASS forbids REFUTED findings
            if any(f.rank is Rank.REFUTED for f in self.findings):
                raise ValueError(
                    "InspectionReport with status=PASS cannot contain REFUTED findings"
                )


def make_inspection_result(
    report: InspectionReport,
    residuals: Tuple[InspectionResidual, ...] = (),
) -> "Result[InspectionReport]":
    """Lift InspectionReport into Result[InspectionReport].

    This is the canonical way to produce a constitutional inspection output:
    1. Domain report (InspectionReport) with status/findings/replay
    2. Wrapped in Result[...] with constitutional fields (rank/evidence/residuals/trace)

    Args:
        report: The domain inspection report
        residuals: Domain-level inspection residuals to be lifted to fvafk.algebra.Residual

    Returns:
        Result[InspectionReport] with constitutional judgment

    Critical Law: This is the ONLY way inspection outputs should be produced.
    NO parallel InspectionResult class is allowed (G6 violation).
    """
    from ..core import Result, Evidence, Residual, Trace

    # Derive rank from report status and findings
    if report.status == "PASS":
        rank = Rank.CERTIFIED
    elif report.status == "FAIL":
        rank = Rank.REFUTED
    else:  # NEEDS_REVIEW
        rank = Rank.LICENSED

    # Lift domain residuals to constitutional residuals
    constitutional_residuals = tuple(
        Residual(
            kind=f"inspection.{r.kind.value}",
            description=r.description,
        )
        for r in residuals
    )

    # Collect evidence from findings
    constitutional_evidence = []
    for finding in report.findings:
        for ev in finding.evidence:
            constitutional_evidence.append(
                Evidence(
                    kind="inspection_finding",
                    source=finding.claim,
                    detail=ev,
                    weight=1.0,
                )
            )

    # Build trace from replay
    trace = Trace(
        operation="inspection",
        source_span=(0, 0),
        parents=(),
        metadata={"replay": report.replay},
    )

    # Collect failures from REFUTED findings
    failures = []
    for finding in report.findings:
        if finding.rank is Rank.REFUTED:
            from ..core import Failure
            failures.append(
                Failure(
                    kind="inspection_refuted_finding",
                    description=finding.claim,
                    fatal=True,
                )
            )

    return Result(
        value=report,
        rank=rank,
        evidence=tuple(constitutional_evidence),
        residuals=constitutional_residuals,
        failures=tuple(failures),
        trace=trace,
    )


def inspection_result_to_legacy_dict(result: "Result[InspectionReport]") -> dict:
    """Convert Result[InspectionReport] to legacy ValidationResult format.

    This allows gradual migration from bare boolean checker to governed
    inspection algebra without breaking existing tools.

    Args:
        result: Result[InspectionReport] from governed inspection

    Returns:
        Dict with keys: passed (bool), errors (list), warnings (list), info (list)
    """
    report = result.value
    passed = report.status == "PASS"

    errors = []
    warnings = []
    info = []

    # Extract from findings
    for finding in report.findings:
        if finding.rank is Rank.REFUTED:
            errors.append(f"{finding.claim}: REFUTED")
        elif finding.is_blocked():
            errors.append(
                f"{finding.claim}: blocked by counter-evidence: "
                f"{', '.join(finding.counter_evidence)}"
            )
        elif finding.residuals:
            warnings.append(
                f"{finding.claim}: has {len(finding.residuals)} residual(s)"
            )
        elif finding.rank is Rank.CERTIFIED:
            info.append(f"{finding.claim}: CERTIFIED")

    # Extract from constitutional residuals
    for residual in result.residuals:
        warnings.append(f"{residual.kind}: {residual.description}")

    # Extract from constitutional failures
    for failure in result.failures:
        if failure.fatal:
            errors.append(f"FATAL: {failure.description}")
        else:
            warnings.append(f"{failure.kind}: {failure.description}")

    return {
        "passed": passed,
        "errors": errors,
        "warnings": warnings,
        "info": info,
    }


__all__ = [
    "InspectionArtifact",
    "InspectionFinding",
    "InspectionResidual",
    "InspectionReport",  # Domain report (not InspectionResult)
    "InspectionResidualKind",
    "make_inspection_result",  # Canonical lift to Result[InspectionReport]
    "inspection_result_to_legacy_dict",  # Legacy bridge
]
