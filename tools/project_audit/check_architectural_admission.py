"""
Architectural Admission Checker

Validates that PRs adding new architectural constructs include
proper MinimalSufficiencyCheck and comply with the constitution.

Authority: MINIMAL_SUFFICIENCY_CONSTITUTION.md
Schema: ARCHITECTURAL_ADMISSION_SCHEMA.md
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
from enum import Enum


class ConstructType(Enum):
    """Types of architectural constructs."""
    CASE = "case"
    SPECIFIC_RULE = "specific_rule"
    GENERAL_RULE = "general_rule"
    METHOD_EXTENSION = "method_extension"
    NEW_GATE = "new_gate"
    NEW_LAYER = "new_layer"
    NEW_DOMAIN = "new_domain"


class RiskLevel(Enum):
    """Explosion risk levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class AdmissionDecision(Enum):
    """Admission decisions."""
    ADMIT = "admit"
    REDUCE_TO_CASE = "reduce_to_case"
    REDUCE_TO_SPECIFIC_RULE = "reduce_to_specific_rule"
    MERGE_WITH_EXISTING = "merge_with_existing"
    REJECT = "reject"


@dataclass
class ValidationResult:
    """Result of validation check."""
    passed: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]

    def __str__(self) -> str:
        result = []
        if self.passed:
            result.append("✅ VALIDATION PASSED")
        else:
            result.append("❌ VALIDATION FAILED")

        if self.errors:
            result.append("\nErrors:")
            for error in self.errors:
                result.append(f"  ❌ {error}")

        if self.warnings:
            result.append("\nWarnings:")
            for warning in self.warnings:
                result.append(f"  ⚠️  {warning}")

        if self.info:
            result.append("\nInfo:")
            for info in self.info:
                result.append(f"  ℹ️  {info}")

        return "\n".join(result)


class ArchitecturalAdmissionChecker:
    """
    Checks PRs for compliance with Minimal Sufficiency Constitution.

    Critical Laws Enforced:
    1. New constructs require MinimalSufficiencyCheck
    2. At least 2 existing constructs must be checked
    3. Reduction attempts required for non-cases
    4. Risk assessment required
    5. Decision rationale required
    """

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def check_pr_description(self, pr_body: str) -> ValidationResult:
        """
        Check PR description for MinimalSufficiencyCheck.

        Args:
            pr_body: Full PR description/body text

        Returns:
            ValidationResult with pass/fail and details
        """
        self.errors = []
        self.warnings = []
        self.info = []

        if self._is_exempt_change(pr_body):
            self.info.append(
                "Exemption criteria met: change does not introduce a new architectural construct"
            )
            return ValidationResult(
                passed=True,
                errors=self.errors,
                warnings=self.warnings,
                info=self.info
            )

        # Check if PR involves new construct
        has_new_construct = self._detect_new_construct(pr_body)

        if not has_new_construct:
            self.info.append("No new architectural construct detected - exemption criteria met")
            return ValidationResult(
                passed=True,
                errors=self.errors,
                warnings=self.warnings,
                info=self.info
            )

        # New construct detected - MinimalSufficiencyCheck required
        self.info.append("New architectural construct detected - MinimalSufficiencyCheck required")

        # Check for MinimalSufficiencyCheck presence
        has_check = self._has_minimal_sufficiency_check(pr_body)
        if not has_check:
            self.errors.append(
                "MinimalSufficiencyCheck section missing for new architectural construct. "
                "See ARCHITECTURAL_ADMISSION_SCHEMA.md for template."
            )
            return ValidationResult(
                passed=False,
                errors=self.errors,
                warnings=self.warnings,
                info=self.info
            )

        # Validate MinimalSufficiencyCheck content
        self._validate_check_content(pr_body)

        passed = len(self.errors) == 0
        return ValidationResult(
            passed=passed,
            errors=self.errors,
            warnings=self.warnings,
            info=self.info
        )

    def _is_exempt_change(self, text: str) -> bool:
        """Check for explicit exemption cases that do not add new constructs."""
        text_lower = text.lower()
        exemption_markers = [
            "bug fix",
            "documentation update",
            "docs only",
            "documentation only",
            "refactoring",
        ]
        no_new_construct_markers = [
            "no new architectural construct",
            "no new architectural constructs",
            "no new construct",
            "no new constructs",
            "without new constructs",
            "without a new construct",
            "no new layers or gates added",
            "no new layer or gate added",
            "does not add a new construct",
        ]
        return (
            any(marker in text_lower for marker in exemption_markers)
            and any(marker in text_lower for marker in no_new_construct_markers)
        ) or (
            any(marker in text_lower for marker in ("bug fix", "documentation update", "documentation only"))
            and "new architectural construct" not in text_lower
        )

    def _detect_new_construct(self, text: str) -> bool:
        """Detect if PR introduces new architectural construct."""
        text_lower = text.lower()
        explicit_no_new_patterns = [
            r"\bno new (?:architectural )?constructs?\b",
            r"\bwithout new constructs?\b",
            r"\bno new (?:layers?|gates?|rules?|domains?)\b",
            r"\bdoes not add (?:a )?new (?:construct|layer|gate|rule|domain)\b",
        ]
        if any(re.search(pattern, text_lower) for pattern in explicit_no_new_patterns):
            return False

        # Check for checkbox indicating new construct
        new_construct_patterns = [
            r'\[x\]\s+\*\*New Architectural Construct\*\*',
            r'\[X\]\s+\*\*New Architectural Construct\*\*',
            r'new_construct:\s*["\']?\w+',
            r'construct_type:',
            r'new.*(?:layer|gate|rule|domain)',
        ]

        for pattern in new_construct_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True

        # Check file changes for new construct indicators
        if any(keyword in text_lower for keyword in [
            'new layer', 'new gate', 'new domain',
            'adds gate', 'implements gate', 'creates layer'
        ]):
            return True

        return False

    def _has_minimal_sufficiency_check(self, text: str) -> bool:
        """Check if MinimalSufficiencyCheck section exists."""
        patterns = [
            r'MinimalSufficiencyCheck:',
            r'Minimal Sufficiency Check',
            r'```yaml\s*MinimalSufficiencyCheck:',
        ]

        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True

        return False

    def _validate_check_content(self, text: str):
        """Validate content of MinimalSufficiencyCheck."""
        # Extract MinimalSufficiencyCheck block
        yaml_match = re.search(
            r'```yaml\s*MinimalSufficiencyCheck:(.*?)```',
            text,
            re.DOTALL | re.IGNORECASE
        )

        if not yaml_match:
            self.errors.append("MinimalSufficiencyCheck not in proper YAML format")
            return

        check_content = yaml_match.group(1)

        # Required fields
        required_fields = [
            ('new_construct', 'New construct name'),
            ('construct_type', 'Construct type'),
            ('why_needed', 'Why needed justification'),
            ('existing_constructs_checked', 'Existing constructs checked'),
            ('smallest_possible_form', 'Smallest possible form'),
            ('does_it_prevent_forbidden_leap', 'Forbidden leap prevention'),
            ('explosion_risk', 'Explosion risk assessment'),
            ('decision', 'Decision and rationale'),
        ]

        for field, description in required_fields:
            if field not in check_content:
                self.errors.append(f"Missing required field: {description} ({field})")

        # Check existing constructs count
        existing_count = len(
            re.findall(r'^\s*-\s*construct:\s*', check_content, re.MULTILINE)
        )
        if existing_count < 2:
            self.errors.append(
                f"at least 2 existing constructs must be checked, found: {existing_count}"
            )

        # Check for reduction attempts if not a case
        if 'new_layer' in check_content or 'new_gate' in check_content or 'general_rule' in check_content:
            if 'reduction_attempts' not in check_content:
                self.errors.append(
                    "Reduction attempts required for constructs that are not cases"
                )
            elif check_content.count('attempted_form:') < 1:
                self.errors.append(
                    "At least one reduction attempt must be documented"
                )

        # Check risk assessment
        if 'explosion_risk' in check_content:
            if not re.search(r'level:\s*(low|medium|high)', check_content, re.IGNORECASE):
                self.errors.append("Risk level must be specified (low/medium/high)")
            if 'justification:' not in check_content:
                self.errors.append("Risk justification required")

        # Check decision
        if 'decision' in check_content:
            if 'rationale:' not in check_content:
                self.errors.append("Decision rationale required")

        # Check for anti-patterns
        self._check_anti_patterns(check_content)

    def _check_anti_patterns(self, content: str):
        """Check for common anti-patterns."""
        content_lower = content.lower()

        # Anti-pattern 1: "Useful but not necessary"
        if 'useful' in content_lower and 'necessary' not in content_lower:
            self.warnings.append(
                "Answer focuses on 'useful' rather than 'necessary' - "
                "constitutional requirement is necessity, not utility"
            )

        # Anti-pattern 2: Vague insufficient reasons
        if 'doesn\'t work' in content_lower or 'doesn\'t handle' in content_lower:
            if 'trace' not in content_lower and 'rank' not in content_lower and 'residual' not in content_lower:
                self.warnings.append(
                    "Insufficient reasons are vague - must specify what is lost "
                    "(trace/rank/residuals/noleap)"
                )

        # Anti-pattern 3: High risk without mitigation
        if re.search(r'level:\s*high', content_lower):
            if 'mitigation' not in content_lower:
                self.errors.append(
                    "High explosion risk requires explicit mitigation strategy"
                )

        # Anti-pattern 4: Empty answers
        empty_patterns = [
            r'answer:\s*""',
            r'justification:\s*""',
            r'rationale:\s*""',
        ]
        for pattern in empty_patterns:
            if re.search(pattern, content):
                self.errors.append(
                    f"Empty answer detected: {pattern} - all fields must be completed"
                )


def check_file(filepath: Path) -> ValidationResult:
    """Check a file (PR description) for compliance."""
    if not filepath.exists():
        return ValidationResult(
            passed=False,
            errors=[f"File not found: {filepath}"],
            warnings=[],
            info=[]
        )

    content = filepath.read_text(encoding='utf-8')
    checker = ArchitecturalAdmissionChecker()
    return checker.check_pr_description(content)


def main():
    """Main entry point for CLI usage."""
    if len(sys.argv) < 2:
        print("Usage: python check_architectural_admission.py <pr_description_file>")
        print()
        print("Example:")
        print("  python check_architectural_admission.py PR_DESCRIPTION.md")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    result = check_file(filepath)

    print(result)
    print()

    if result.passed:
        print("✅ Architectural admission check PASSED")
        sys.exit(0)
    else:
        print("❌ Architectural admission check FAILED")
        print()
        print("Please review:")
        print("  - docs/MINIMAL_SUFFICIENCY_CONSTITUTION.md")
        print("  - docs/ARCHITECTURAL_ADMISSION_SCHEMA.md")
        print("  - .github/pull_request_template.md")
        sys.exit(1)


if __name__ == "__main__":
    main()
