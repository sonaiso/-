"""
Architectural Admission Checker

Validates that PRs adding new architectural constructs include
proper MinimalSufficiencyCheck and comply with the constitution.

Authority: MINIMAL_SUFFICIENCY_CONSTITUTION.md
Schema: ARCHITECTURAL_ADMISSION_SCHEMA.md

CONSTITUTIONAL GOVERNANCE (PR-INS1):

    This checker uses governed inspection algebra internally.

    Old way (bare boolean):
        regex → pass/fail  # ❌ Violates "لا مخرج عارٍ"

    New way (governed):
        artifact → evidence → counter_evidence → finding → rank → residuals → trace

    The public API remains backward-compatible (ValidationResult),
    but internally all decisions flow through InspectionResult.
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
from enum import Enum

# Import inspection algebra (PR-INS1)
# Use try/except for environments where fvafk.algebra may not be in path
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
    from fvafk.algebra import (
        InspectionArtifact,
        InspectionFinding,
        InspectionResidual,
        InspectionResult,
        InspectionResidualKind,
        Rank,
    )
    INSPECTION_ALGEBRA_AVAILABLE = True
except ImportError:
    INSPECTION_ALGEBRA_AVAILABLE = False


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

        This is the public API method that returns ValidationResult for
        backward compatibility. Internally uses governed inspection algebra.

        Args:
            pr_body: Full PR description/body text

        Returns:
            ValidationResult with pass/fail and details
        """
        if INSPECTION_ALGEBRA_AVAILABLE:
            # Use governed inspection algebra
            inspection_result = self._check_pr_governed(pr_body)
            return self._inspection_to_validation(inspection_result)
        else:
            # Fallback to legacy implementation
            return self._check_pr_legacy(pr_body)

    def _check_pr_governed(self, pr_body: str) -> 'InspectionResult':
        """
        Governed inspection using InspectionAlgebra.

        Follows constitutional law:
            artifact → evidence → counter_evidence → finding → rank → residuals → trace

        Args:
            pr_body: PR description text

        Returns:
            InspectionResult (NO bare boolean)
        """
        # Build artifact
        artifact = InspectionArtifact(
            kind="pr_body",
            content_ref="PR description",
            trace="read_pr_description()",
        )

        findings = []
        residuals = []
        replay = ["inspect_pr()", "build_artifact(pr_body)"]

        # Finding 1: Check for new construct claim
        new_construct_finding = self._extract_new_construct_finding(pr_body)
        findings.append(new_construct_finding)
        replay.append("extract_new_construct_claim()")

        if new_construct_finding.is_blocked() or new_construct_finding.rank is Rank.UNRESOLVED:
            # No new construct → exemption criteria met
            return InspectionResult(
                status="PASS",
                findings=tuple(findings),
                rank=Rank.CERTIFIED,
                residuals=tuple(residuals),
                replay=tuple(replay),
            )

        # New construct detected - check for MinimalSufficiencyCheck
        replay.append("new_construct_detected")

        sufficiency_check_finding = self._extract_sufficiency_check_finding(pr_body)
        findings.append(sufficiency_check_finding)
        replay.append("extract_sufficiency_check()")

        if sufficiency_check_finding.rank is Rank.REFUTED:
            # Missing sufficiency check
            return InspectionResult(
                status="FAIL",
                findings=tuple(findings),
                rank=Rank.REFUTED,
                residuals=tuple(residuals),
                replay=tuple(replay),
            )

        # Validate sufficiency check content
        content_findings, content_residuals = self._validate_check_content_governed(pr_body)
        findings.extend(content_findings)
        residuals.extend(content_residuals)
        replay.append("validate_check_content()")

        # Determine status from findings
        has_refuted = any(f.rank is Rank.REFUTED for f in findings)
        has_blocked = any(f.is_blocked() for f in findings)

        if has_refuted or has_blocked:
            status = "FAIL"
            rank = Rank.REFUTED if has_refuted else Rank.CANDIDATE
        elif residuals:
            status = "NEEDS_REVIEW"
            rank = Rank.LICENSED
        else:
            status = "PASS"
            rank = Rank.CERTIFIED

        return InspectionResult(
            status=status,
            findings=tuple(findings),
            rank=rank,
            residuals=tuple(residuals),
            replay=tuple(replay),
        )

    def _extract_new_construct_finding(self, text: str) -> 'InspectionFinding':
        """
        Extract finding about new construct claim.

        Uses counter-evidence to detect negation:
        - "No new layers or gates" → counter-evidence blocks claim
        - Explicit checkbox → strong evidence

        Returns:
            InspectionFinding with evidence and counter-evidence
        """
        claim = "New architectural construct added"
        evidence = []
        counter_evidence = []

        # Strong evidence: Explicit checkbox
        if re.search(r'\[x\]\s+\*\*New Architectural Construct\*\*', text, re.IGNORECASE):
            evidence.append("Explicit checkbox: [x] **New Architectural Construct** checked")

        # Weak evidence: YAML field
        if re.search(r'new_construct:\s*["\']?\w+', text):
            evidence.append("YAML field: new_construct present")

        # Weak evidence: construct_type field
        if re.search(r'construct_type:', text):
            evidence.append("YAML field: construct_type present")

        # Weak evidence: Regex patterns (BUT check for negation first!)
        pattern_matches = []
        if re.search(r'new.*(?:layer|gate|rule|domain)', text, re.IGNORECASE):
            pattern_matches.append(re.search(r'new.*(?:layer|gate|rule|domain)', text, re.IGNORECASE).group())

        # CRITICAL: Check for negation markers (counter-evidence)
        negation_context = self._extract_negation_context(text, pattern_matches)
        if negation_context:
            counter_evidence.extend(negation_context)
        elif pattern_matches:
            # No negation → weak evidence
            evidence.append(f"Regex pattern match: '{pattern_matches[0]}'")

        # Determine rank
        if counter_evidence:
            # Blocked by negation
            rank = Rank.CANDIDATE
        elif not evidence:
            # No evidence
            rank = Rank.UNRESOLVED
        elif any("Explicit checkbox" in e for e in evidence):
            # Strong evidence
            rank = Rank.LICENSED
        else:
            # Weak evidence only
            rank = Rank.CANDIDATE

        return InspectionFinding(
            claim=claim,
            evidence=tuple(evidence),
            counter_evidence=tuple(counter_evidence),
            rank=rank,
            trace=("_detect_new_construct(text)",),
        )

    def _extract_negation_context(self, text: str, pattern_matches: List[str]) -> List[str]:
        """
        Extract negation markers that create counter-evidence.

        Negation patterns:
        - "No new layers"
        - "not adding new gates"
        - "without new domain"

        Args:
            text: Full text
            pattern_matches: Matches from regex patterns

        Returns:
            List of counter-evidence strings
        """
        counter_evidence = []

        # Check for negation markers near pattern matches
        negation_patterns = [
            r'\bno\b\s+new\s+(?:layers?|gates?|rules?|domains?)',
            r'\bnot\b.*new\s+(?:layers?|gates?|rules?|domains?)',
            r'\bwithout\b.*new\s+(?:layers?|gates?|rules?|domains?)',
            r'no\s+new\s+(?:layers?|gates?|rules?|domains?)\s+(?:or|and)',
        ]

        for pattern in negation_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                counter_evidence.append(f"Negation marker: '{match.group()}'")

        return counter_evidence

    def _extract_sufficiency_check_finding(self, text: str) -> 'InspectionFinding':
        """Extract finding about MinimalSufficiencyCheck presence."""
        claim = "MinimalSufficiencyCheck section present"
        evidence = []

        patterns = [
            (r'MinimalSufficiencyCheck:', "Header 'MinimalSufficiencyCheck:'"),
            (r'```yaml\s*MinimalSufficiencyCheck:', "YAML code block with MinimalSufficiencyCheck"),
        ]

        for pattern, desc in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                evidence.append(desc)

        if evidence:
            rank = Rank.LICENSED
        else:
            rank = Rank.REFUTED

        return InspectionFinding(
            claim=claim,
            evidence=tuple(evidence),
            rank=rank,
            trace=("_has_minimal_sufficiency_check(text)",),
        )

    def _validate_check_content_governed(self, text: str) -> Tuple[List['InspectionFinding'], List['InspectionResidual']]:
        """
        Validate MinimalSufficiencyCheck content using governed inspection.

        Returns:
            Tuple of (findings, residuals)
        """
        findings = []
        residuals = []

        # Extract YAML block
        yaml_match = re.search(
            r'```yaml\s*MinimalSufficiencyCheck:(.*?)```',
            text,
            re.DOTALL | re.IGNORECASE
        )

        if not yaml_match:
            findings.append(
                InspectionFinding(
                    claim="MinimalSufficiencyCheck in proper YAML format",
                    evidence=(),
                    rank=Rank.REFUTED,
                    trace=("_validate_check_content()",),
                )
            )
            return findings, residuals

        check_content = yaml_match.group(1)

        # Check required fields
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
            if field in check_content:
                findings.append(
                    InspectionFinding(
                        claim=f"Required field '{description}' present",
                        evidence=(f"Field '{field}' found in YAML",),
                        rank=Rank.LICENSED,
                        trace=("check_required_field()",),
                    )
                )
            else:
                findings.append(
                    InspectionFinding(
                        claim=f"Required field '{description}' present",
                        evidence=(),
                        rank=Rank.REFUTED,
                        residuals=(
                            InspectionResidual(
                                kind=InspectionResidualKind.CLAIM_WITHOUT_EVIDENCE,
                                description=f"Missing required field: {description} ({field})",
                            ),
                        ),
                        trace=("check_required_field()",),
                    )
                )

        # Check existing constructs count (CRITICAL: Must be at least 2)
        existing_count = check_content.count('construct:')
        if existing_count < 2:
            findings.append(
                InspectionFinding(
                    claim="At least 2 existing constructs checked",
                    evidence=(f"Found {existing_count} construct(s)",),
                    rank=Rank.REFUTED,
                    residuals=(
                        InspectionResidual(
                            kind=InspectionResidualKind.INSUFFICIENT_SPECIFICITY,
                            description=f"At least 2 existing constructs must be checked, found: {existing_count}",
                        ),
                    ),
                    trace=("check_existing_constructs_count()",),
                )
            )

        # Check anti-patterns
        anti_pattern_findings, anti_pattern_residuals = self._check_anti_patterns_governed(check_content)
        findings.extend(anti_pattern_findings)
        residuals.extend(anti_pattern_residuals)

        return findings, residuals

    def _check_anti_patterns_governed(self, content: str) -> Tuple[List['InspectionFinding'], List['InspectionResidual']]:
        """Check for anti-patterns using governed inspection."""
        findings = []
        residuals = []
        content_lower = content.lower()

        # Anti-pattern 1: "Useful but not necessary"
        if 'useful' in content_lower and 'necessary' not in content_lower:
            residuals.append(
                InspectionResidual(
                    kind=InspectionResidualKind.WEAK_EVIDENCE,
                    description=(
                        "Answer focuses on 'useful' rather than 'necessary' - "
                        "constitutional requirement is necessity, not utility"
                    ),
                )
            )

        # Anti-pattern 2: Vague insufficient reasons
        if 'doesn\'t work' in content_lower or 'doesn\'t handle' in content_lower:
            if 'trace' not in content_lower and 'rank' not in content_lower and 'residual' not in content_lower:
                residuals.append(
                    InspectionResidual(
                        kind=InspectionResidualKind.WEAK_EVIDENCE,
                        description=(
                            "Insufficient reasons are vague - must specify what is lost "
                            "(trace/rank/residuals/noleap)"
                        ),
                    )
                )

        # Anti-pattern 3: High risk without mitigation
        if re.search(r'level:\s*high', content_lower):
            if 'mitigation' not in content_lower:
                findings.append(
                    InspectionFinding(
                        claim="High explosion risk requires mitigation",
                        evidence=("Risk level: high found",),
                        counter_evidence=("No mitigation strategy found",),
                        rank=Rank.REFUTED,
                        trace=("check_high_risk_mitigation()",),
                    )
                )

        return findings, residuals

    def _inspection_to_validation(self, inspection: 'InspectionResult') -> ValidationResult:
        """
        Convert InspectionResult to ValidationResult for backward compatibility.

        This bridge allows gradual migration while preserving public API.

        Args:
            inspection: InspectionResult from governed inspection

        Returns:
            ValidationResult (legacy format)
        """
        legacy = inspection.to_legacy_validation_result()
        return ValidationResult(
            passed=legacy["passed"],
            errors=legacy["errors"],
            warnings=legacy["warnings"],
            info=legacy["info"],
        )

    def _check_pr_legacy(self, pr_body: str) -> ValidationResult:
        """
        Legacy implementation (fallback when inspection algebra unavailable).

        This is the old bare-boolean implementation.

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
