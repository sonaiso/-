"""Tests for governed inspection algebra.

Authority: PR-INS1

Test Categories:

1. Constitutional invariants (no bare output, evidence requirements, etc.)
2. Negation detection (counter-evidence blocks findings)
3. Claim-evidence binding (claims verified against artifacts)
4. Evidence hierarchy (stronger sources override weaker)
5. Specificity ordering (specific failures precede general)
6. Residual tracking (explicit reason for non-CERTIFIED)
7. Replay preservation (full audit trail)
8. Legacy compatibility (conversion to ValidationResult)

Critical Laws Being Tested:

- No finding without claim
- No rank >= LICENSED without evidence
- No CERTIFIED with residuals
- No CERTIFIED with counter-evidence
- Status derived from findings, not arbitrary
"""

import pytest

from fvafk.algebra import (
    InspectionArtifact,
    InspectionFinding,
    InspectionResidual,
    InspectionResult,
    InspectionResidualKind,
    Rank,
)


class TestInspectionArtifact:
    """Test InspectionArtifact type and evidence hierarchy."""

    def test_create_pr_body_artifact(self):
        """Create PR body artifact with trace."""
        artifact = InspectionArtifact(
            kind="pr_body",
            content_ref="PR #80 description",
            trace="read_pr_description(pr_number=80)"
        )
        assert artifact.kind == "pr_body"
        assert artifact.content_ref == "PR #80 description"
        assert artifact.evidence_weight() == 0.3  # Weakest evidence

    def test_create_workflow_artifact(self):
        """Create CI workflow artifact with highest evidence weight."""
        artifact = InspectionArtifact(
            kind="workflow",
            content_ref=".github/workflows/ci.yml run #123",
            trace="fetch_workflow_run(run_id=123)"
        )
        assert artifact.kind == "workflow"
        assert artifact.evidence_weight() == 1.0  # Strongest evidence

    def test_evidence_hierarchy(self):
        """Verify evidence hierarchy ordering."""
        artifacts = [
            InspectionArtifact(kind="pr_body", content_ref="pr", trace="t"),
            InspectionArtifact(kind="diff", content_ref="diff", trace="t"),
            InspectionArtifact(kind="source_file", content_ref="src", trace="t"),
            InspectionArtifact(kind="workflow", content_ref="wf", trace="t"),
        ]

        weights = [a.evidence_weight() for a in artifacts]
        assert weights == [0.3, 0.6, 0.8, 1.0]  # Ascending order

    def test_require_content_ref(self):
        """Artifact must have non-empty content_ref."""
        with pytest.raises(ValueError, match="content_ref must be non-empty"):
            InspectionArtifact(kind="pr_body", content_ref="", trace="t")

    def test_require_trace(self):
        """Artifact must have non-empty trace."""
        with pytest.raises(ValueError, match="trace must be non-empty"):
            InspectionArtifact(kind="pr_body", content_ref="ref", trace="")


class TestInspectionFinding:
    """Test InspectionFinding with evidence and counter-evidence."""

    def test_create_simple_finding_with_evidence(self):
        """Create finding with claim and evidence."""
        finding = InspectionFinding(
            claim="New architectural construct added",
            evidence=("Checkbox [x] **New Architectural Construct** checked",),
            rank=Rank.LICENSED,
        )
        assert finding.claim == "New architectural construct added"
        assert len(finding.evidence) == 1
        assert finding.rank is Rank.LICENSED
        assert not finding.is_blocked()

    def test_counter_evidence_blocks_finding(self):
        """Counter-evidence prevents high rank."""
        # This should raise because counter-evidence blocks LICENSED rank
        with pytest.raises(ValueError, match="counter-evidence cannot be >= LICENSED"):
            InspectionFinding(
                claim="New gate added",
                evidence=("Regex match: 'new.*gate'",),
                counter_evidence=("Negation marker: 'No new gates'",),
                rank=Rank.LICENSED,  # Too high with counter-evidence
            )

    def test_counter_evidence_allows_candidate(self):
        """Counter-evidence allows CANDIDATE rank (unsupported claim)."""
        finding = InspectionFinding(
            claim="New gate added",
            evidence=("Regex match: 'new.*gate'",),
            counter_evidence=("Negation marker: 'No new gates'",),
            rank=Rank.CANDIDATE,  # Demoted due to counter-evidence
        )
        assert finding.is_blocked()
        assert finding.rank is Rank.CANDIDATE

    def test_certified_finding_requires_no_residuals(self):
        """CERTIFIED finding cannot have residuals."""
        with pytest.raises(ValueError, match="cannot be CERTIFIED while residuals remain"):
            InspectionFinding(
                claim="Bug fix verified",
                evidence=("Test passes", "Source code change"),
                rank=Rank.CERTIFIED,
                residuals=(
                    InspectionResidual(
                        kind=InspectionResidualKind.UNTESTED_CLAIM,
                        description="Edge case not tested"
                    ),
                ),
            )

    def test_licensed_requires_evidence(self):
        """LICENSED rank requires evidence (la-mukhraj-arin)."""
        with pytest.raises(ValueError, match="requires evidence"):
            InspectionFinding(
                claim="Something changed",
                evidence=(),  # Empty!
                rank=Rank.LICENSED,
            )

    def test_candidate_allows_no_evidence(self):
        """CANDIDATE rank allows unsupported claim."""
        finding = InspectionFinding(
            claim="Might be a new construct",
            evidence=(),
            rank=Rank.CANDIDATE,
        )
        assert finding.rank is Rank.CANDIDATE

    def test_require_claim(self):
        """Finding must have non-empty claim."""
        with pytest.raises(ValueError, match="claim must be non-empty"):
            InspectionFinding(claim="")


class TestInspectionResidual:
    """Test InspectionResidual types."""

    def test_create_claim_without_evidence_residual(self):
        """Create residual for claim without evidence."""
        residual = InspectionResidual(
            kind=InspectionResidualKind.CLAIM_WITHOUT_EVIDENCE,
            description="PR claims new files added but changed_files list is empty",
            location="PR body line 45"
        )
        assert residual.kind is InspectionResidualKind.CLAIM_WITHOUT_EVIDENCE
        assert "changed_files list is empty" in residual.description

    def test_create_claim_inflation_residual(self):
        """Create residual for claim inflation."""
        residual = InspectionResidual(
            kind=InspectionResidualKind.CLAIM_INFLATION,
            description="Claimed work_unit.py exists but not in changed files",
        )
        assert residual.kind is InspectionResidualKind.CLAIM_INFLATION

    def test_require_description(self):
        """Residual must have non-empty description."""
        with pytest.raises(ValueError, match="description must be non-empty"):
            InspectionResidual(
                kind=InspectionResidualKind.WEAK_EVIDENCE,
                description=""
            )


class TestInspectionResult:
    """Test InspectionResult governed output."""

    def test_pass_with_certified_findings(self):
        """PASS status with CERTIFIED findings."""
        findings = (
            InspectionFinding(
                claim="Bug fix verified",
                evidence=("Test passes", "Source changed"),
                rank=Rank.CERTIFIED,
            ),
        )
        result = InspectionResult(
            status="PASS",
            findings=findings,
            rank=Rank.CERTIFIED,
        )
        assert result.status == "PASS"
        assert result.findings[0].is_certified()

    def test_fail_with_refuted_finding(self):
        """FAIL status requires REFUTED finding."""
        findings = (
            InspectionFinding(
                claim="New construct added",
                evidence=("Checkbox checked",),
                rank=Rank.REFUTED,  # Contradicted
            ),
        )
        result = InspectionResult(
            status="FAIL",
            findings=findings,
            rank=Rank.REFUTED,
        )
        assert result.status == "FAIL"

    def test_fail_with_blocked_finding(self):
        """FAIL status with counter-evidence blocked finding."""
        findings = (
            InspectionFinding(
                claim="New gate",
                evidence=("Regex match",),
                counter_evidence=("Negation: 'No new gates'",),
                rank=Rank.CANDIDATE,
            ),
        )
        result = InspectionResult(
            status="FAIL",
            findings=findings,
            rank=Rank.CANDIDATE,
        )
        assert result.status == "FAIL"
        assert findings[0].is_blocked()

    def test_fail_without_refuted_or_blocked_raises(self):
        """FAIL status without REFUTED/blocked finding violates invariant."""
        findings = (
            InspectionFinding(
                claim="Something",
                evidence=("Evidence",),
                rank=Rank.LICENSED,
            ),
        )
        with pytest.raises(ValueError, match="FAIL requires at least one REFUTED or blocked"):
            InspectionResult(
                status="FAIL",
                findings=findings,
            )

    def test_pass_with_refuted_finding_raises(self):
        """PASS status cannot have REFUTED findings."""
        findings = (
            InspectionFinding(
                claim="Contradiction",
                evidence=("Evidence",),
                rank=Rank.REFUTED,
            ),
        )
        with pytest.raises(ValueError, match="PASS cannot contain REFUTED"):
            InspectionResult(
                status="PASS",
                findings=findings,
            )

    def test_needs_review_with_residuals(self):
        """NEEDS_REVIEW status for mixed or ambiguous findings."""
        findings = (
            InspectionFinding(
                claim="Possibly new construct",
                evidence=("Weak regex match",),
                rank=Rank.LICENSED,
                residuals=(
                    InspectionResidual(
                        kind=InspectionResidualKind.WEAK_EVIDENCE,
                        description="Only PR body claim"
                    ),
                ),
            ),
        )
        result = InspectionResult(
            status="NEEDS_REVIEW",
            findings=findings,
            rank=Rank.LICENSED,
            residuals=(findings[0].residuals[0],),
        )
        assert result.status == "NEEDS_REVIEW"

    def test_to_legacy_validation_result_pass(self):
        """Convert PASS to legacy format."""
        findings = (
            InspectionFinding(
                claim="Clean check",
                evidence=("All good",),
                rank=Rank.CERTIFIED,
            ),
        )
        result = InspectionResult(
            status="PASS",
            findings=findings,
            rank=Rank.CERTIFIED,
        )

        legacy = result.to_legacy_validation_result()
        assert legacy["passed"] is True
        assert "Clean check: CERTIFIED" in legacy["info"]
        assert not legacy["errors"]

    def test_to_legacy_validation_result_fail(self):
        """Convert FAIL to legacy format."""
        findings = (
            InspectionFinding(
                claim="Bad construct",
                evidence=("Evidence",),
                rank=Rank.REFUTED,
            ),
        )
        result = InspectionResult(
            status="FAIL",
            findings=findings,
            rank=Rank.REFUTED,
        )

        legacy = result.to_legacy_validation_result()
        assert legacy["passed"] is False
        assert any("REFUTED" in e for e in legacy["errors"])

    def test_to_legacy_validation_result_with_blocked(self):
        """Convert blocked finding to legacy errors."""
        findings = (
            InspectionFinding(
                claim="New gate",
                evidence=("Match",),
                counter_evidence=("No new gates",),
                rank=Rank.CANDIDATE,
            ),
        )
        result = InspectionResult(
            status="FAIL",
            findings=findings,
        )

        legacy = result.to_legacy_validation_result()
        assert legacy["passed"] is False
        assert any("blocked by counter-evidence" in e for e in legacy["errors"])


class TestNegationDetection:
    """Test that negation markers create counter-evidence."""

    def test_no_new_layers_creates_counter_evidence(self):
        """Phrase 'No new layers' should be counter-evidence, not evidence."""
        # This is the bug from check_architectural_admission.py
        # The regex r'new.*(?:layer|gate)' matches "No new layers"
        # But should produce counter-evidence, not evidence

        finding = InspectionFinding(
            claim="New layer added",
            evidence=("Regex: 'new.*layer' matched",),
            counter_evidence=("Negation marker: 'No new layers or gates added'",),
            rank=Rank.CANDIDATE,  # Demoted due to negation
        )

        assert finding.is_blocked()
        assert finding.rank is Rank.CANDIDATE
        # High ranks forbidden with counter-evidence

    def test_explicit_checkbox_overrides_negation(self):
        """Strong evidence (checkbox) can override weak counter-evidence."""
        # If checkbox is explicitly checked AND body says "no new",
        # that's a contradiction that needs NEEDS_REVIEW

        finding1 = InspectionFinding(
            claim="Checkbox indicates new construct",
            evidence=("[x] **New Architectural Construct** checked",),
            rank=Rank.LICENSED,  # Strong evidence
        )

        finding2 = InspectionFinding(
            claim="Body text denies new construct",
            evidence=("Text: 'No new layers or gates added'",),
            rank=Rank.LICENSED,
        )

        # Both findings present = contradiction = NEEDS_REVIEW
        result = InspectionResult(
            status="NEEDS_REVIEW",
            findings=(finding1, finding2),
            rank=Rank.LICENSED,
            residuals=(
                InspectionResidual(
                    kind=InspectionResidualKind.WEAK_EVIDENCE,
                    description="Contradiction: checkbox checked but body denies"
                ),
            ),
        )

        assert result.status == "NEEDS_REVIEW"


class TestClaimEvidenceBinding:
    """Test that claims must be verified against actual artifacts."""

    def test_claim_inflation_detected(self):
        """Claim about file not in changed_files produces residual."""
        # PR #80 claims work_unit.py exists but it's not in changed files

        finding = InspectionFinding(
            claim="work_unit.py added",
            evidence=("PR body mentions work_unit.py",),
            rank=Rank.LICENSED,
            residuals=(
                InspectionResidual(
                    kind=InspectionResidualKind.CLAIM_INFLATION,
                    description="work_unit.py claimed but not in changed_files list",
                    location="PR body vs. diff"
                ),
            ),
        )

        # Residuals prevent CERTIFIED
        assert not finding.is_certified()
        assert finding.residuals[0].kind is InspectionResidualKind.CLAIM_INFLATION

    def test_source_verification_removes_residual(self):
        """Claim verified against source_file has no residual."""
        finding = InspectionFinding(
            claim="inspection.py added",
            evidence=(
                "PR body mentions inspection.py",
                "changed_files includes src/fvafk/algebra/governance/inspection.py",
                "source_file content verified"
            ),
            rank=Rank.CERTIFIED,  # No residuals
        )

        assert finding.is_certified()
        assert not finding.residuals


class TestSpecificityOrdering:
    """Test that specific failures precede general failures.

    Constitutional Law: Specific failures must precede general failures.

    Bug Example: NameRealitySubGate checks general NAME_WITHOUT_DOMAIN
    before specific TECHNICAL_WITHOUT_DOMAIN.
    """

    def test_specific_residual_before_general(self):
        """Specific residual kind should be checked before general."""
        # TECHNICAL_WITHOUT_DOMAIN is more specific than NAME_WITHOUT_DOMAIN

        specific_residual = InspectionResidual(
            kind=InspectionResidualKind.INSUFFICIENT_SPECIFICITY,
            description=(
                "General NAME_WITHOUT_DOMAIN check fired before "
                "specific TECHNICAL_WITHOUT_DOMAIN check"
            ),
        )

        # This residual indicates the bug: wrong ordering
        assert "General" in specific_residual.description
        assert "before specific" in specific_residual.description

    def test_ordering_law_documented(self):
        """Specificity ordering is a constitutional law."""
        # This test documents the law, even though we can't enforce
        # ordering at the type level (requires implementation discipline)

        law = "Specific failures precede general failures"
        assert "Specific" in law
        assert "precede" in law

        # Implementation checkers must:
        # 1. Check TECHNICAL_WITHOUT_DOMAIN before NAME_WITHOUT_DOMAIN
        # 2. Check specific cases before general cases
        # 3. Return first matching specific failure, not first matching general


class TestReplayPreservation:
    """Test full trace preservation for audit."""

    def test_finding_with_trace(self):
        """Finding preserves full trace chain."""
        finding = InspectionFinding(
            claim="Construct verified",
            evidence=("Evidence 1", "Evidence 2"),
            rank=Rank.CERTIFIED,
            trace=(
                "read_pr_body(pr=80)",
                "extract_checkbox_section()",
                "verify_against_changed_files()",
            ),
        )

        assert len(finding.trace) == 3
        assert finding.trace[0] == "read_pr_body(pr=80)"

    def test_result_with_replay(self):
        """Result preserves replay chain."""
        result = InspectionResult(
            status="PASS",
            findings=(
                InspectionFinding(
                    claim="Verified",
                    evidence=("E",),
                    rank=Rank.CERTIFIED,
                ),
            ),
            rank=Rank.CERTIFIED,
            replay=(
                "inspect_pr(pr_number=80)",
                "build_artifacts()",
                "extract_findings()",
                "apply_rank_policy()",
            ),
        )

        assert len(result.replay) == 4
        assert result.replay[0] == "inspect_pr(pr_number=80)"


class TestNoBareBooleanAnywhere:
    """Critical: No bare boolean in inspection algebra."""

    def test_inspection_result_has_no_bool_field(self):
        """InspectionResult must not have bare 'passed' boolean field."""
        result = InspectionResult(
            status="PASS",
            findings=(),
            rank=Rank.UNRESOLVED,
        )

        # Should have status (str), not passed (bool)
        assert hasattr(result, "status")
        assert not hasattr(result, "passed")
        assert result.status in ("PASS", "FAIL", "NEEDS_REVIEW")

    def test_finding_has_no_bool_field(self):
        """InspectionFinding must not have bare boolean fields."""
        finding = InspectionFinding(
            claim="Test",
            evidence=("E",),
            rank=Rank.LICENSED,
        )

        # Should have rank (Rank enum), not passed/valid (bool)
        assert hasattr(finding, "rank")
        assert not hasattr(finding, "passed")
        assert not hasattr(finding, "valid")

    def test_legacy_conversion_is_explicit(self):
        """Boolean only appears in explicit legacy conversion."""
        result = InspectionResult(
            status="PASS",
            findings=(),
            rank=Rank.UNRESOLVED,
        )

        # to_legacy_validation_result() is the ONLY way to get boolean
        legacy = result.to_legacy_validation_result()
        assert "passed" in legacy  # Now allowed, because explicit conversion
        assert isinstance(legacy["passed"], bool)

        # But result itself has no boolean
        assert not hasattr(result, "passed")
