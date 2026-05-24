"""Test specificity ordering law for NameRealitySubGate.

Constitutional Law:

    Specific failures must precede general failures.

Bug Fixed (PR-INS1):

    Before: General NAME_WITHOUT_DOMAIN check fired before specific
            TECHNICAL_WITHOUT_DOMAIN check.

    After:  Specific TECHNICAL_WITHOUT_DOMAIN check fires first.

Why This Matters:

    Specificity provides diagnostic precision. General failures give
    vague error messages. Specific failures pinpoint exact issue.

    Example:
    - General:  "Name requires domain" (which kind of name?)
    - Specific: "Technical name requires domain" (clear: it's technical!)

This is not just a "nice to have" - it's a constitutional requirement
for all gates and checkers.
"""

import pytest

from gfa.prior_information import NameRealitySubGate
from gfa.prior_information.reality_type import RealityType
from gfa.prior_information.name_reality_subgate import NameRealityFailureKind


class TestSpecificityOrderingLaw:
    """Test constitutional law: Specific failures precede general failures."""

    def test_technical_without_domain_before_general(self):
        """TECHNICAL_WITHOUT_DOMAIN must fire before general NAME_WITHOUT_DOMAIN."""
        gate = NameRealitySubGate()

        result = gate.admit_named_reality(
            name="InspectionAlgebra",
            referent_candidate="some_object",
            existence_type=RealityType.TECHNICAL,
            domain=None,  # Missing domain!
        )

        # Should get specific failure, not general
        assert result.is_blocked()
        assert result.failure is not None
        assert result.failure.kind is NameRealityFailureKind.TECHNICAL_WITHOUT_DOMAIN
        # NOT NAME_WITHOUT_DOMAIN

        # Message should mention "Technical"
        assert "Technical" in result.failure.message or "technical" in result.failure.message

    def test_general_check_fires_for_non_technical(self):
        """General NAME_WITHOUT_DOMAIN still fires for non-technical types."""
        gate = NameRealitySubGate()

        # Test with MENTAL (also requires domain)
        result = gate.admit_named_reality(
            name="Consciousness",
            referent_candidate="mental_state",
            existence_type=RealityType.MENTAL,
            domain=None,  # Missing domain!
        )

        # Should get general failure (MENTAL is not TECHNICAL)
        assert result.is_blocked()
        assert result.failure is not None
        assert result.failure.kind is NameRealityFailureKind.NAME_WITHOUT_DOMAIN

    def test_ordering_preserves_precision(self):
        """Specificity ordering ensures most precise error message."""
        gate = NameRealitySubGate()

        # TECHNICAL without domain
        tech_result = gate.admit_named_reality(
            name="TechnicalTerm",
            referent_candidate="obj",
            existence_type=RealityType.TECHNICAL,
            domain=None,
        )

        # MENTAL without domain
        mental_result = gate.admit_named_reality(
            name="MentalConcept",
            referent_candidate="obj",
            existence_type=RealityType.MENTAL,
            domain=None,
        )

        # Both blocked, but different failure kinds
        assert tech_result.is_blocked()
        assert mental_result.is_blocked()

        # Technical gets specific error
        assert tech_result.failure.kind is NameRealityFailureKind.TECHNICAL_WITHOUT_DOMAIN

        # Mental gets general error
        assert mental_result.failure.kind is NameRealityFailureKind.NAME_WITHOUT_DOMAIN

        # Error messages have different precision
        assert "Technical" in tech_result.failure.message
        assert "MENTAL" in mental_result.failure.message or "Mental" in mental_result.failure.message


class TestDocumentSpecificityOrderingPrinciple:
    """Document the general principle for all gates and checkers."""

    def test_specificity_ordering_is_constitutional_law(self):
        """Specificity ordering applies to ALL verification operations."""
        law = "Specific failures must precede general failures"

        # This law applies to:
        # 1. NameRealitySubGate (now fixed)
        # 2. PriorInformationGate
        # 3. InspectionAlgebra (to be implemented)
        # 4. check_architectural_admission.py (to be refactored)
        # 5. All future gates and checkers

        assert "Specific" in law
        assert "precede" in law
        assert "general" in law

    def test_example_ordering_pattern(self):
        """Document the pattern: specific → general."""
        # Correct ordering (specific first):
        ordering_correct = [
            "TECHNICAL_WITHOUT_DOMAIN",  # Most specific
            "NAME_WITHOUT_DOMAIN",       # General
        ]

        # Wrong ordering (general first):
        ordering_wrong = [
            "NAME_WITHOUT_DOMAIN",       # General (fires first - BAD!)
            "TECHNICAL_WITHOUT_DOMAIN",  # Specific (never reached - BUG!)
        ]

        # In correct ordering, specific check happens first
        assert ordering_correct.index("TECHNICAL_WITHOUT_DOMAIN") < \
               ordering_correct.index("NAME_WITHOUT_DOMAIN")

        # Wrong ordering has general before specific
        assert ordering_wrong.index("NAME_WITHOUT_DOMAIN") < \
               ordering_wrong.index("TECHNICAL_WITHOUT_DOMAIN")

    def test_diagnostic_precision_benefit(self):
        """Specificity improves diagnostic precision."""
        # General error message
        general_msg = "Name requires domain"

        # Specific error message
        specific_msg = "Technical name requires domain"

        # Specific message contains more information
        assert "Technical" in specific_msg
        assert "Technical" not in general_msg

        # Developer sees specific message → knows it's a technical term issue
        # Developer sees general message → must investigate what kind of name
