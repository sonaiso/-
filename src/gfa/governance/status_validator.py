"""Status Validator: Prevents False Completion Claims.

Implements runtime validation to ensure no component claims
completion without proof.

Core Law:
    لا ادعاء بالإنجاز بلا برهان.
    "No claim without proof."
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Set, Tuple

from .algebra_status import (
    AlgebraStatus,
    ComponentStatus,
    ProjectStatus,
    get_project_status,
)


class GovernanceViolation(Exception):
    """Raised when governance rules are violated."""

    pass


# Forbidden claims that require proof
FORBIDDEN_CLAIMS_WITHOUT_PROOF = [
    "General Algebra implemented",
    "CPB computationally proven",
    "Self-learning is general",
    "LayerGenerator exists",
    "GFA is generated from General Algebra",
    "Dalalah closure is complete",
    "Hukm is reachable",
    "General Algebra complete",
    "CPB extraction complete",
    "Generality proven",
    "Architecture 100%",
    "Architecture complete",
]


@dataclass(frozen=True)
class ValidationResult:
    """Result of status validation.

    Attributes:
        passed: Whether validation passed
        violations: List of violations found
        warnings: List of warnings
        status: Current project status
    """

    passed: bool
    violations: List[str]
    warnings: List[str]
    status: ProjectStatus


class StatusValidator:
    """Validates project status against false claims.

    Methods:
        validate_project_status: Check entire project
        validate_no_false_claims: Search for forbidden claims
        check_required_components: Verify required components exist
    """

    def __init__(self):
        self.base_path = Path("/home/runner/work/-/-")

    def validate_project_status(self) -> ValidationResult:
        """Validate entire project status.

        Returns:
            ValidationResult with all violations and warnings
        """
        violations = []
        warnings = []

        # Get current status
        status = get_project_status()

        # Check for false claims in docs and code
        claim_violations = self._check_false_claims()
        violations.extend(claim_violations)

        # Check component consistency
        component_warnings = self._check_component_consistency(status)
        warnings.extend(component_warnings)

        # Check if GFA claims generality
        gfa_violations = self._check_gfa_generality_claims()
        violations.extend(gfa_violations)

        passed = len(violations) == 0

        return ValidationResult(
            passed=passed,
            violations=violations,
            warnings=warnings,
            status=status,
        )

    def _check_false_claims(self) -> List[str]:
        """Search for forbidden completion claims.

        Returns:
            List of violations found
        """
        violations = []

        # Search in docs
        docs_path = self.base_path / "docs"
        if docs_path.exists():
            for forbidden_claim in FORBIDDEN_CLAIMS_WITHOUT_PROOF:
                matches = self._search_in_directory(docs_path, forbidden_claim, "*.md")
                if matches:
                    violations.append(
                        f"Found forbidden claim '{forbidden_claim}' in docs: {matches}"
                    )

        # Search in source code comments/docstrings
        src_path = self.base_path / "src"
        if src_path.exists():
            for forbidden_claim in FORBIDDEN_CLAIMS_WITHOUT_PROOF:
                matches = self._search_in_directory(src_path, forbidden_claim, "*.py")
                if matches:
                    violations.append(
                        f"Found forbidden claim '{forbidden_claim}' in source: {matches}"
                    )

        return violations

    def _search_in_directory(
        self, directory: Path, text: str, pattern: str
    ) -> List[str]:
        """Search for text in files matching pattern.

        Args:
            directory: Directory to search
            text: Text to search for
            pattern: File pattern (e.g. "*.md")

        Returns:
            List of files containing the text
        """
        matches = []

        try:
            for file_path in directory.rglob(pattern):
                if file_path.is_file():
                    try:
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        if text.lower() in content.lower():
                            matches.append(str(file_path.relative_to(self.base_path)))
                    except Exception:
                        # Skip files that can't be read
                        pass
        except Exception:
            # Skip if directory issues
            pass

        return matches

    def _check_component_consistency(self, status: ProjectStatus) -> List[str]:
        """Check component implementation consistency.

        Args:
            status: Current project status

        Returns:
            List of warnings
        """
        warnings = []

        # Check if claiming general without required components
        required_for_general = {
            ComponentStatus.COGNITIVE_CARRIER,
            ComponentStatus.MEMORY_GEOMETRY,
            ComponentStatus.COMPARISON_GEOMETRY,
            ComponentStatus.BINDING_CORE,
            ComponentStatus.CPB_EXTRACTION,
        }

        missing_for_general = required_for_general - status.implemented_components

        if missing_for_general:
            warnings.append(
                f"Missing components for General Algebra Runtime: "
                f"{[c.value for c in missing_for_general]}"
            )

        # Check if CPB proven without required components
        if status.cpb_proven:
            if ComponentStatus.CPB_EXTRACTION not in status.implemented_components:
                warnings.append(
                    "CPB marked as proven but CPB_EXTRACTION component not found"
                )

        return warnings

    def _check_gfa_generality_claims(self) -> List[str]:
        """Check if GFA falsely claims to be general.

        Returns:
            List of violations
        """
        violations = []

        # Check if any GFA result claims general status
        gfa_methods_path = self.base_path / "src" / "gfa" / "methods"

        if gfa_methods_path.exists():
            # Search for GENERAL_ALGEBRA_RUNTIME or PROVEN_GENERAL claims
            general_claims = self._search_in_directory(
                gfa_methods_path,
                "GENERAL_ALGEBRA_RUNTIME",
                "*.py"
            )

            if general_claims:
                violations.append(
                    f"GFA methods claim GENERAL_ALGEBRA_RUNTIME status: {general_claims}"
                )

            proven_claims = self._search_in_directory(
                gfa_methods_path,
                "PROVEN_GENERAL",
                "*.py"
            )

            if proven_claims:
                violations.append(
                    f"GFA methods claim PROVEN_GENERAL status: {proven_claims}"
                )

        return violations


def validate_project_status() -> ValidationResult:
    """Validate project status (convenience function).

    Returns:
        ValidationResult

    Raises:
        GovernanceViolation: If critical violations found
    """
    validator = StatusValidator()
    result = validator.validate_project_status()

    if not result.passed:
        raise GovernanceViolation(
            f"Project status validation failed:\n" + "\n".join(result.violations)
        )

    return result


def validate_no_false_claims() -> None:
    """Validate no false completion claims exist.

    Raises:
        GovernanceViolation: If false claims found
    """
    validator = StatusValidator()
    result = validator.validate_project_status()

    if result.violations:
        raise GovernanceViolation(
            "Found false completion claims:\n" + "\n".join(result.violations)
        )


__all__ = [
    "StatusValidator",
    "ValidationResult",
    "GovernanceViolation",
    "validate_project_status",
    "validate_no_false_claims",
    "FORBIDDEN_CLAIMS_WITHOUT_PROOF",
]
