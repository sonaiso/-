"""
Tests for Architectural Admission Checker

Validates enforcement of Minimal Sufficiency Constitution.

Critical Test Cases:
1. PR with new layer without proof → FAIL
2. PR reducible to case but requests layer → FAIL
3. PR with general rule when specific suffices → FAIL
4. PR with minimal complete unit and sufficiency check → PASS
"""

import pytest
from pathlib import Path
import sys
import tempfile

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "tools" / "project_audit"))

from check_architectural_admission import (
    ArchitecturalAdmissionChecker,
    ValidationResult,
    check_file,
)


class TestAntiPatternDetection:
    """Test detection of anti-patterns."""

    def test_useful_vs_necessary_antipattern(self):
        """Detect 'useful but not necessary' anti-pattern."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] **New Architectural Construct**

        ```yaml
        MinimalSufficiencyCheck:
          new_construct: "NewLayer"
          construct_type: new_layer
          why_needed:
            answer: "It would be useful to have this feature"
          existing_constructs_checked:
            - construct: "Existing1"
              why_insufficient: "Doesn't work"
            - construct: "Existing2"
              why_insufficient: "Not good"
          smallest_possible_form:
            proposed_type: "new_layer"
          explosion_risk:
            level: low
          decision:
            rationale: "Seems good"
        ```
        """

        result = checker.check_pr_description(pr_body)

        assert not result.passed
        assert any('useful' in w.lower() and 'necessary' in w.lower() for w in result.warnings)

    def test_vague_insufficient_reasons(self):
        """Detect vague 'why_insufficient' reasons."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] **New Architectural Construct**

        ```yaml
        MinimalSufficiencyCheck:
          new_construct: "NewGate"
          construct_type: new_gate
          why_needed:
            answer: "Prevents X→Y leap"
          existing_constructs_checked:
            - construct: "ExistingGate"
              why_insufficient: "Doesn't handle this case"
            - construct: "AnotherGate"
              why_insufficient: "Doesn't work"
          smallest_possible_form:
            proposed_type: "new_gate"
          does_it_prevent_forbidden_leap:
            answer: true
          explosion_risk:
            level: low
            justification: "Low risk"
          decision:
            rationale: "Necessary"
        ```
        """

        result = checker.check_pr_description(pr_body)

        assert any('vague' in w.lower() for w in result.warnings)


class TestRequiredFieldValidation:
    """Test validation of required fields."""

    def test_missing_new_construct_name(self):
        """Fail if new_construct name missing."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] **New Architectural Construct**

        ```yaml
        MinimalSufficiencyCheck:
          construct_type: new_layer
        ```
        """

        result = checker.check_pr_description(pr_body)

        assert not result.passed
        assert any('new_construct' in e.lower() or 'construct name' in e.lower() for e in result.errors)

    def test_missing_why_needed(self):
        """Fail if why_needed missing."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] **New Architectural Construct**

        ```yaml
        MinimalSufficiencyCheck:
          new_construct: "TestConstruct"
          construct_type: new_gate
        ```
        """

        result = checker.check_pr_description(pr_body)

        assert not result.passed
        assert any('why_needed' in e.lower() or 'why needed' in e.lower() for e in result.errors)

    def test_insufficient_existing_constructs_checked(self):
        """Fail if less than 2 existing constructs checked."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] **New Architectural Construct**

        ```yaml
        MinimalSufficiencyCheck:
          new_construct: "NewLayer"
          construct_type: new_layer
          why_needed:
            answer: "Necessary for X"
          existing_constructs_checked:
            - construct: "OnlyOne"
              why_insufficient: "Not enough"
          smallest_possible_form:
            proposed_type: "new_layer"
          explosion_risk:
            level: low
          decision:
            rationale: "Admit"
        ```
        """

        result = checker.check_pr_description(pr_body)

        assert not result.passed
        assert any('at least 2' in e.lower() for e in result.errors)


class TestReductionAttempts:
    """Test reduction attempt validation."""

    def test_new_layer_requires_reduction_attempts(self):
        """New layer must document reduction attempts."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] **New Architectural Construct**

        ```yaml
        MinimalSufficiencyCheck:
          new_construct: "NewLayer"
          construct_type: new_layer
          why_needed:
            answer: "Prevents forbidden leap X→Y"
          existing_constructs_checked:
            - construct: "Gate1"
              why_insufficient: "Loses trace"
            - construct: "Gate2"
              why_insufficient: "Loses rank"
          smallest_possible_form:
            proposed_type: "new_layer"
            justification: "Only layer works"
          does_it_prevent_forbidden_leap:
            answer: true
          explosion_risk:
            level: low
            justification: "Isolated case"
          decision:
            outcome: admit
            rationale: "Necessary"
        ```
        """

        result = checker.check_pr_description(pr_body)

        assert not result.passed
        assert any('reduction' in e.lower() for e in result.errors)

    def test_case_does_not_require_reduction_attempts(self):
        """Case construct does not require reduction attempts."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] **New Architectural Construct**

        ```yaml
        MinimalSufficiencyCheck:
          new_construct: "MetaphorCase"
          construct_type: case
          why_needed:
            answer: "Specific metaphor pattern"
          existing_constructs_checked:
            - construct: "GeneralMetaphorRule"
              why_insufficient: "Too general"
            - construct: "OtherCase"
              why_insufficient: "Different pattern"
          smallest_possible_form:
            proposed_type: "case"
            justification: "Simplest form"
          does_it_prevent_forbidden_leap:
            answer: false
          does_it_preserve_trace:
            answer: true
          explosion_risk:
            level: low
            justification: "Single case"
          decision:
            outcome: admit
            rationale: "Minimal sufficient case"
        ```
        """

        result = checker.check_pr_description(pr_body)

        # Should pass - cases don't need reduction attempts
        assert result.passed or 'reduction' not in ' '.join(result.errors).lower()


class TestRiskAssessment:
    """Test explosion risk assessment."""

    def test_high_risk_requires_mitigation(self):
        """High explosion risk requires mitigation strategy."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] **New Architectural Construct**

        ```yaml
        MinimalSufficiencyCheck:
          new_construct: "RiskyConstruct"
          construct_type: new_gate
          why_needed:
            answer: "Necessary"
          existing_constructs_checked:
            - construct: "Gate1"
              why_insufficient: "Insufficient"
            - construct: "Gate2"
              why_insufficient: "Insufficient"
          smallest_possible_form:
            proposed_type: "new_gate"
          does_it_prevent_forbidden_leap:
            answer: true
          explosion_risk:
            level: high
            justification: "Could proliferate"
          decision:
            rationale: "Accept anyway"
        ```
        """

        result = checker.check_pr_description(pr_body)

        assert not result.passed
        assert any('mitigation' in e.lower() for e in result.errors)


class TestExemptionCriteria:
    """Test exemption from MinimalSufficiencyCheck."""

    def test_bug_fix_exempt(self):
        """Bug fix PRs are exempt."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] Bug fix

        ## Description
        Fixes issue #123 in the parser.
        """

        result = checker.check_pr_description(pr_body)

        assert result.passed
        assert any('exemption' in i.lower() for i in result.info)

    def test_documentation_only_exempt(self):
        """Documentation-only PRs are exempt."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] Documentation update

        ## Description
        Updates README with new examples.
        """

        result = checker.check_pr_description(pr_body)

        assert result.passed

    def test_refactoring_without_new_construct_exempt(self):
        """Refactoring without new constructs is exempt."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] Refactoring

        ## Description
        Refactors existing code for clarity.
        No new layers or gates added.
        """

        result = checker.check_pr_description(pr_body)

        assert result.passed


class TestCompleteValidation:
    """Test complete validation scenarios."""

    def test_complete_valid_new_gate(self):
        """Complete, valid MinimalSufficiencyCheck passes."""
        checker = ArchitecturalAdmissionChecker()

        pr_body = """
        ## Type of Change
        - [x] **New Architectural Construct**

        ```yaml
        MinimalSufficiencyCheck:
          new_construct: "NameRealitySubGate"
          construct_type: new_gate

          why_needed:
            question: "What distinction can the current system NOT represent?"
            answer: "Prevents name→reality usurpation which existing gates don't block"

          existing_constructs_checked:
            - construct: "RealityTypeGate"
              why_insufficient: "Works on reality candidates, not name→reality transition"
              attempted_representation: "Tried pre-filtering names"
              what_failed: "Trace lost - cannot track which names were rejected vs admitted"

            - construct: "DomainGate"
              why_insufficient: "Operates on domain level, not name-referent binding"
              attempted_representation: "Tried domain-scoped name filtering"
              what_failed: "NoLeap violation - jumps from name to domain without referent candidate"

          smallest_possible_form:
            proposed_type: "new_gate"
            justification: "Cannot reduce to case/rule - requires gate-level trace preservation"
            reduction_attempts:
              - attempted_form: "specific_rule"
                why_failed: "Rule cannot maintain trace across Prior Information→Name→Reality path"

          does_it_prevent_forbidden_leap:
            answer: true
            which_leap: "name→reality without referent candidate + domain + evidence"
            existing_gate_insufficient: "No existing gate governs name-to-reality transition"

          does_it_preserve_trace:
            answer: true
            how: "Maintains trace through name-referent-domain-evidence chain"

          does_it_affect_rank_policy:
            answer: true
            impact: "Adds rank degradation when domain/evidence missing"

          does_it_create_new_residual_type:
            answer: true
            which_residual: "R-NAME-MISSING-REFERENT, R-NAME-MISSING-DOMAIN"
            why_needed: "Existing residuals don't cover name-specific failures"

          explosion_risk:
            level: low
            justification: "Only one Name-Reality transition point. Cannot proliferate to other usurpations"

            proliferation_potential:
              similar_constructs_possible: 0
              mitigation: "Each usurpation type (trace→certainty, form→meaning) has separate gate"

            complexity_increase:
              cognitive_load: low
              integration_cost: low

          decision:
            outcome: admit
            rationale: "Necessary gate preventing documented usurpation. Minimal form. Low explosion risk."

            if_admitted:
              integration_plan: "Integrates as sub-gate within PriorInformationGeometry"
              documentation_updates: ["MINIMAL_SUFFICIENCY_CONSTITUTION.md", "CLOSURE_GATE_MATRIX.md"]
              test_coverage: "140+ test cases covering all blocking conditions"
        ```
        """

        result = checker.check_pr_description(pr_body)

        assert result.passed, f"Expected pass but got errors: {result.errors}"
        assert len(result.errors) == 0


class TestFileBasedValidation:
    """Test validation from files."""

    def test_check_file_not_found(self):
        """Handle file not found gracefully."""
        result = check_file(Path("/nonexistent/file.md"))

        assert not result.passed
        assert any('not found' in e.lower() for e in result.errors)

    def test_check_file_valid_content(self, tmp_path):
        """Check file with valid content."""
        test_file = tmp_path / "pr_description.md"
        test_file.write_text("""
        ## Type of Change
        - [x] Bug fix

        ## Description
        Fixes parser bug.
        """)

        result = check_file(test_file)

        assert result.passed


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
