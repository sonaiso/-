"""
Roadmap Consistency and Governance Tests

PR #26: Roadmap Reconciliation + Audit Claim Guard

These tests enforce governance rules to prevent:
1. Premature certification claims
2. Undocumented PR numbering divergence
3. Semantic leakage in dal_core
4. Completion claims without evidence
"""

import os
import re
from pathlib import Path
import pytest


# Path to repository root
REPO_ROOT = Path(__file__).parent.parent.parent


class TestPrematureCertificationPrevention:
    """Prevent claiming certification without required reports"""

    def test_audit_checklist_exists(self):
        """DAL_FORMAL_AUDIT_CHECKLIST.md must exist"""
        checklist_path = REPO_ROOT / "docs" / "DAL_FORMAL_AUDIT_CHECKLIST.md"
        assert checklist_path.exists(), "Audit checklist must exist"

    def test_audit_checklist_has_framework_warning(self):
        """Audit checklist must clarify framework ≠ certification"""
        checklist_path = REPO_ROOT / "docs" / "DAL_FORMAL_AUDIT_CHECKLIST.md"
        content = checklist_path.read_text()

        # Must contain warning about framework vs. certification
        assert "Checklist ≠ Certification" in content or "checklist ≠ certification" in content.lower(), \
            "Audit checklist must warn that framework ≠ certification"
        assert "Framework Defined" in content or "framework defined" in content.lower(), \
            "Must distinguish framework definition from audit passed"

    def test_no_premature_total_coverage_claim(self):
        """Cannot claim 'Total-Coverage closed' without K reports"""
        # Check if reports directory exists with required reports
        reports_dir = REPO_ROOT / "reports"

        if reports_dir.exists():
            # If reports exist, check they're empty (∅)
            hole_report = reports_dir / "hole_report.json"
            jump_report = reports_dir / "jump_report.json"
            leak_report = reports_dir / "semantic_leak_report.json"

            if hole_report.exists():
                import json
                holes = json.loads(hole_report.read_text())
                assert len(holes) == 0, "hole_report must be empty (∅) for Total-Coverage claim"

            if jump_report.exists():
                import json
                jumps = json.loads(jump_report.read_text())
                assert len(jumps) == 0, "jump_report must be empty (∅) for Total-Coverage claim"

            if leak_report.exists():
                import json
                leaks = json.loads(leak_report.read_text())
                assert len(leaks) == 0, "leak_report must be empty (∅) for Total-Coverage claim"

        # Otherwise, reports don't exist, so Total-Coverage cannot be claimed
        # This test passes by default if reports don't exist (no premature claim possible)


class TestRoadmapNumberingConsistency:
    """Enforce PR numbering governance"""

    def test_pr_status_index_exists(self):
        """PR_STATUS_INDEX.md must exist"""
        index_path = REPO_ROOT / "docs" / "PR_STATUS_INDEX.md"
        assert index_path.exists(), "PR_STATUS_INDEX.md must exist to track numbering"

    def test_roadmap_governance_exists(self):
        """ROADMAP_GOVERNANCE.md must exist"""
        governance_path = REPO_ROOT / "docs" / "ROADMAP_GOVERNANCE.md"
        assert governance_path.exists(), "ROADMAP_GOVERNANCE.md must exist"

    def test_roadmap_has_numbering_warning(self):
        """PROJECT_ALGEBRA_ROADMAP.md must warn about numbering"""
        roadmap_path = REPO_ROOT / "docs" / "PROJECT_ALGEBRA_ROADMAP.md"
        content = roadmap_path.read_text()

        # Must contain PR numbering clarification
        assert "planning identifiers" in content.lower() or "roadmap pr" in content.lower(), \
            "Roadmap must clarify PR numbers are planning identifiers"
        assert "PR_STATUS_INDEX" in content or "pr_status_index" in content.lower(), \
            "Roadmap must reference PR_STATUS_INDEX.md"


class TestSemanticLeakagePrevention:
    """Enforce no semantic fields in dal_core"""

    def test_no_meaning_field_in_dal_core(self):
        """dal_core dataclasses must not have 'meaning' field"""
        dal_core_dir = REPO_ROOT / "src" / "dal_core"

        if not dal_core_dir.exists():
            pytest.skip("src/dal_core does not exist yet")

        forbidden_fields = ["meaning", "murad", "haqiqa_majaz", "semantics", "intent"]

        # Scan all Python files in dal_core
        for py_file in dal_core_dir.rglob("*.py"):
            content = py_file.read_text()

            # Skip comments and docstrings (basic check)
            lines = content.split("\n")
            for line_num, line in enumerate(lines, 1):
                # Skip comments
                if line.strip().startswith("#"):
                    continue

                # Check for forbidden field assignments in dataclass
                for forbidden in forbidden_fields:
                    # Pattern: field_name: Type or field_name =
                    if re.search(rf"\b{forbidden}\s*[:=]", line):
                        # Allow if it's a comment about prohibition
                        if "forbidden" in line.lower() or "prohibited" in line.lower() or "not" in line.lower():
                            continue
                        pytest.fail(
                            f"Forbidden semantic field '{forbidden}' found in {py_file.name}:{line_num}\n"
                            f"Line: {line.strip()}"
                        )

    def test_no_semantic_imports_in_dal_core(self):
        """dal_core must not import semantic modules"""
        dal_core_dir = REPO_ROOT / "src" / "dal_core"

        if not dal_core_dir.exists():
            pytest.skip("src/dal_core does not exist yet")

        forbidden_imports = ["semantic", "wadh", "madlul", "dalalah", "murad", "hukm"]

        for py_file in dal_core_dir.rglob("*.py"):
            content = py_file.read_text()

            for forbidden in forbidden_imports:
                # Check for imports
                if re.search(rf"import\s+{forbidden}|from\s+{forbidden}", content):
                    pytest.fail(
                        f"Forbidden semantic import '{forbidden}' found in {py_file.name}"
                    )


class TestDocumentationEvidence:
    """Enforce evidence requirements for documentation claims"""

    def test_planned_prs_marked_as_planned(self):
        """PRs not yet created must be marked as 'Planned' or similar"""
        roadmap_path = REPO_ROOT / "docs" / "PROJECT_ALGEBRA_ROADMAP.md"
        content = roadmap_path.read_text()

        # Check that PR #23, #24, #25 are marked as planned
        # Pattern: look for "PR #23" or "### PR #23" sections
        for pr_num in [23, 24, 25]:
            # Find section for this PR
            pattern = rf"###\s*PR\s*#{pr_num}[:\s]"
            match = re.search(pattern, content)

            if match:
                # Get section content (next 10 lines)
                section_start = match.end()
                section_content = content[section_start:section_start+500]

                # Must contain "Planned" or "not yet created" or similar
                assert any(marker in section_content for marker in [
                    "Planned", "planned", "not yet created", "📋"
                ]), f"PR #{pr_num} must be marked as planned/not yet created"

    def test_dal_algebra_signature_marked_as_planned(self):
        """DAL_ALGEBRA_SIGNATURE.md must clarify it's planning documentation"""
        sig_path = REPO_ROOT / "docs" / "DAL_ALGEBRA_SIGNATURE.md"

        if not sig_path.exists():
            pytest.skip("DAL_ALGEBRA_SIGNATURE.md does not exist")

        content = sig_path.read_text()

        # Must contain warning that it's planning documentation
        assert "planning" in content.lower() or "planned" in content.lower(), \
            "DAL_ALGEBRA_SIGNATURE.md must clarify it's planning documentation"
        assert "not yet implemented" in content.lower() or "not yet created" in content.lower(), \
            "Must state that implementation doesn't exist yet"


class TestGovernanceDocumentConsistency:
    """Ensure governance documents are consistent"""

    def test_all_governance_docs_exist(self):
        """All required governance documents must exist"""
        required_docs = [
            "docs/PR_STATUS_INDEX.md",
            "docs/ROADMAP_GOVERNANCE.md",
            "docs/PROJECT_ALGEBRA_ROADMAP.md",
            "docs/DAL_FORMAL_AUDIT_CHECKLIST.md",
        ]

        for doc_path in required_docs:
            full_path = REPO_ROOT / doc_path
            assert full_path.exists(), f"Required governance document missing: {doc_path}"

    def test_governance_cross_references(self):
        """Governance documents must reference each other"""
        # PR_STATUS_INDEX should reference ROADMAP_GOVERNANCE
        index_path = REPO_ROOT / "docs" / "PR_STATUS_INDEX.md"
        index_content = index_path.read_text()
        assert "ROADMAP_GOVERNANCE" in index_content, \
            "PR_STATUS_INDEX.md must reference ROADMAP_GOVERNANCE.md"

        # ROADMAP_GOVERNANCE should reference PR_STATUS_INDEX
        governance_path = REPO_ROOT / "docs" / "ROADMAP_GOVERNANCE.md"
        governance_content = governance_path.read_text()
        assert "PR_STATUS_INDEX" in governance_content, \
            "ROADMAP_GOVERNANCE.md must reference PR_STATUS_INDEX.md"

        # PROJECT_ALGEBRA_ROADMAP should reference both
        roadmap_path = REPO_ROOT / "docs" / "PROJECT_ALGEBRA_ROADMAP.md"
        roadmap_content = roadmap_path.read_text()
        assert "PR_STATUS_INDEX" in roadmap_content or "pr_status_index" in roadmap_content.lower(), \
            "PROJECT_ALGEBRA_ROADMAP.md must reference PR_STATUS_INDEX.md"


# Marker for this test suite
pytestmark = pytest.mark.governance
