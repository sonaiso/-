"""Claim ↔ Evidence Alignment Tests (PR-POST80)

These tests enforce a single, narrow invariant:

    If a PR body claims a file, module, or class as part of its delivery,
    that artifact MUST appear in the PR's changed-files set.

    Otherwise the claim is unsupported and the PR must be flagged with a
    CLAIM_INFLATION residual (see InspectionResidualKind.CLAIM_INFLATION).

This test file is intentionally fixture-based (no GitHub API calls). It
proves the *checker logic* is correct so that a later step (A3 in
``docs/GOVERNANCE_ROADMAP.md``) can wire it to real PR metadata.

Authority:
- docs/POST_MERGE_TRUTH_AUDIT_PR80.md
- docs/GOVERNANCE_ROADMAP.md
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence, Tuple

import pytest

# Make the inspection algebra importable. The checker uses the same path
# manipulation; we mirror it here so this test is self-contained.
_REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO_ROOT / "src"))

from fvafk.algebra import (  # noqa: E402
    InspectionFinding,
    InspectionResidual,
    InspectionResidualKind,
    InspectionResult,
    Rank,
)


# ---------------------------------------------------------------------------
# Checker under test
# ---------------------------------------------------------------------------

# Patterns that indicate the PR body is naming a concrete deliverable.
# These are deliberately conservative: they look for a token that is
# unambiguously a file or class reference, not a free-form English mention.
_FILE_REF = re.compile(
    r"`?([A-Za-z_][A-Za-z0-9_\-/]*\.py)`?",
)
_CLASS_REF = re.compile(
    r"\b(?:class\s+|implements\s+|introduces\s+|adds\s+)"
    r"`?([A-Z][A-Za-z0-9_]+)`?",
)
# Backticked CamelCase identifiers without a file extension are treated as
# class/type claims (e.g. ``WorkUnit``, ``AgentPermission``). This catches
# list continuations like "introduces `Foo`, `Bar`, and `Baz`".
_BACKTICKED_CAMEL = re.compile(
    r"`([A-Z][A-Za-z0-9_]*[a-z][A-Za-z0-9_]*)`"
)


@dataclass(frozen=True)
class ClaimedArtifact:
    """An artifact named in a PR body."""

    kind: str  # "file" or "class"
    name: str


def extract_claimed_artifacts(pr_body: str) -> List[ClaimedArtifact]:
    """Extract concrete file/class claims from a PR body.

    The extractor is deliberately narrow: it matches tokens that look like
    Python file paths (``foo.py``) or capitalised identifiers introduced
    by an action verb (``adds Foo``, ``implements Bar``, ``class Baz``).
    """
    claimed: List[ClaimedArtifact] = []

    for match in _FILE_REF.finditer(pr_body):
        claimed.append(ClaimedArtifact(kind="file", name=match.group(1)))

    for match in _CLASS_REF.finditer(pr_body):
        claimed.append(ClaimedArtifact(kind="class", name=match.group(1)))

    for match in _BACKTICKED_CAMEL.finditer(pr_body):
        name = match.group(1)
        # Skip if it looks like a file (has a dot) — already covered above.
        if "." in name:
            continue
        claimed.append(ClaimedArtifact(kind="class", name=name))

    # Deduplicate while preserving order.
    seen = set()
    unique: List[ClaimedArtifact] = []
    for art in claimed:
        key = (art.kind, art.name)
        if key in seen:
            continue
        seen.add(key)
        unique.append(art)
    return unique


def check_claim_evidence_alignment(
    pr_body: str,
    changed_files: Sequence[str],
    file_contents: Sequence[Tuple[str, str]] = (),
) -> InspectionResult:
    """Return an InspectionResult flagging any claim with no diff evidence.

    Args:
        pr_body: The full PR description text.
        changed_files: List of paths changed in the PR.
        file_contents: Optional ``(path, content)`` pairs so the checker
            can verify class-level claims against the actual diff text.

    Returns:
        InspectionResult with:
            - status PASS if every claim is backed by changed_files / contents.
            - status FAIL with a REFUTED finding (CLAIM_INFLATION residual)
              otherwise.
    """
    claims = extract_claimed_artifacts(pr_body)
    findings: List[InspectionFinding] = []
    residuals: List[InspectionResidual] = []
    replay = ["extract_claimed_artifacts(pr_body)", "scan(changed_files)"]

    changed_basenames = {Path(p).name for p in changed_files}
    changed_paths = set(changed_files)

    # Flatten file contents for class lookups.
    all_content = "\n".join(content for _, content in file_contents)

    for claim in claims:
        if claim.kind == "file":
            # A file claim is satisfied if some changed path ends with the
            # claimed basename, or equals the claimed path.
            satisfied = (
                claim.name in changed_paths
                or Path(claim.name).name in changed_basenames
                or any(p.endswith("/" + claim.name) for p in changed_paths)
            )
            if not satisfied:
                residual = InspectionResidual(
                    kind=InspectionResidualKind.CLAIM_INFLATION,
                    description=(
                        f"PR body claims file '{claim.name}' but it is not "
                        f"present in changed_files"
                    ),
                )
                findings.append(
                    InspectionFinding(
                        claim=f"File '{claim.name}' is part of this PR",
                        evidence=(),
                        rank=Rank.REFUTED,
                        residuals=(residual,),
                        trace=("check_claim_evidence_alignment(file)",),
                    )
                )
                residuals.append(residual)

        elif claim.kind == "class":
            # A class claim is satisfied if a class with that name appears
            # in any provided file content.
            pattern = re.compile(
                rf"^\s*class\s+{re.escape(claim.name)}\b", re.MULTILINE
            )
            satisfied = bool(pattern.search(all_content))
            if not satisfied:
                residual = InspectionResidual(
                    kind=InspectionResidualKind.CLAIM_INFLATION,
                    description=(
                        f"PR body claims class '{claim.name}' but no "
                        f"matching `class {claim.name}` definition is "
                        f"present in changed files"
                    ),
                )
                findings.append(
                    InspectionFinding(
                        claim=f"Class '{claim.name}' is defined by this PR",
                        evidence=(),
                        rank=Rank.REFUTED,
                        residuals=(residual,),
                        trace=("check_claim_evidence_alignment(class)",),
                    )
                )
                residuals.append(residual)

    if findings:
        return InspectionResult(
            status="FAIL",
            findings=tuple(findings),
            rank=Rank.REFUTED,
            residuals=tuple(residuals),
            replay=tuple(replay),
        )

    # Nothing claimed (or everything backed): PASS with a single CERTIFIED
    # finding so the result is governed (no bare success).
    return InspectionResult(
        status="PASS",
        findings=(
            InspectionFinding(
                claim="All concrete claims in PR body are backed by changed files",
                evidence=(f"{len(claims)} claim(s) checked",),
                rank=Rank.CERTIFIED,
                trace=("check_claim_evidence_alignment(aligned)",),
            ),
        ),
        rank=Rank.CERTIFIED,
        residuals=(),
        replay=tuple(replay),
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestClaimInflation:
    """A claim in the PR body that has no diff evidence must be flagged."""

    def test_claimed_file_missing_from_changed_files_is_inflation(self):
        pr_body = (
            "This PR implements GOV1.\n"
            "It adds `work_unit.py` and `check_work_unit.py`.\n"
        )
        changed_files = [
            "tools/project_audit/check_architectural_admission.py",
            "docs/POST_MERGE_TRUTH_AUDIT_PR80.md",
        ]

        result = check_claim_evidence_alignment(pr_body, changed_files)

        assert result.status == "FAIL"
        assert result.rank is Rank.REFUTED

        descriptions = [r.description for r in result.residuals]
        assert any("work_unit.py" in d for d in descriptions)
        assert any("check_work_unit.py" in d for d in descriptions)
        assert all(
            r.kind is InspectionResidualKind.CLAIM_INFLATION
            for r in result.residuals
        )

    def test_claimed_class_missing_from_diff_is_inflation(self):
        pr_body = "This PR introduces `WorkUnit` and `AgentPermission` classes."
        changed_files = ["docs/POST_MERGE_TRUTH_AUDIT_PR80.md"]
        # No file contents define those classes.

        result = check_claim_evidence_alignment(
            pr_body, changed_files, file_contents=[]
        )

        assert result.status == "FAIL"
        assert any(
            r.kind is InspectionResidualKind.CLAIM_INFLATION
            for r in result.residuals
        )
        descriptions = [r.description for r in result.residuals]
        assert any("WorkUnit" in d for d in descriptions)
        assert any("AgentPermission" in d for d in descriptions)


class TestAlignedClaims:
    """When every claim is backed, the inspection passes."""

    def test_claimed_file_present_in_changed_files_passes(self):
        pr_body = "Adds `check_architectural_admission.py` with new logic."
        changed_files = [
            "tools/project_audit/check_architectural_admission.py",
        ]

        result = check_claim_evidence_alignment(pr_body, changed_files)

        assert result.status == "PASS"
        assert result.rank is Rank.CERTIFIED
        assert not result.residuals

    def test_claimed_class_present_in_diff_passes(self):
        pr_body = "This PR adds `WorkUnit` to govern delivery."
        changed_files = ["src/governance/work_unit.py"]
        contents = [
            (
                "src/governance/work_unit.py",
                "class WorkUnit:\n    pass\n",
            ),
        ]

        result = check_claim_evidence_alignment(
            pr_body, changed_files, file_contents=contents
        )

        assert result.status == "PASS"
        assert result.rank is Rank.CERTIFIED
        assert not result.residuals

    def test_no_concrete_claims_passes_trivially(self):
        pr_body = "This PR refactors internal naming."
        changed_files = ["src/foo.py"]

        result = check_claim_evidence_alignment(pr_body, changed_files)

        assert result.status == "PASS"
        assert result.rank is Rank.CERTIFIED


class TestPR80Regression:
    """Concrete reproduction of the PR #80 mismatch.

    PR #80 was titled/described as delivering GOV1 (WorkUnit, AgentPermission,
    DashboardGovernance, check_work_unit.py, verify_pr_admission.py) but its
    diff contained none of those artifacts. This test pins that exact case so
    the same mistake cannot recur unnoticed.
    """

    def test_pr80_style_body_against_actual_diff_fails(self):
        pr_body = (
            "# GOV1: Project Operating System\n\n"
            "This PR implements GOV1. It introduces `WorkUnit`, "
            "`AgentPermission`, and `DashboardGovernance`, and ships "
            "`check_work_unit.py` and `verify_pr_admission.py` as admission "
            "helpers.\n"
        )
        # The *actual* PR #80 diff (per POST_MERGE_TRUTH_AUDIT_PR80.md):
        actual_changed_files = [
            ".github/workflows/ci.yml",
            "src/fvafk/algebra/code_learning_loop.py",
            "src/fvafk/algebra/governance/inspection.py",
            "src/fvafk/algebra/rank.py",
            "tests/fvafk/algebra/test_inspection_algebra.py",
            "tests/tools/test_architectural_admission.py",
        ]

        result = check_claim_evidence_alignment(pr_body, actual_changed_files)

        assert result.status == "FAIL"
        assert result.rank is Rank.REFUTED

        # Every named GOV1 artifact must be flagged as CLAIM_INFLATION.
        descriptions = " ".join(r.description for r in result.residuals)
        for missing in (
            "check_work_unit.py",
            "verify_pr_admission.py",
            "WorkUnit",
            "AgentPermission",
            "DashboardGovernance",
        ):
            assert missing in descriptions, (
                f"Expected CLAIM_INFLATION for '{missing}'"
            )


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
