"""
ProtoPrior Validator

Validates FirstPriorUnit against constitutional laws.

This enforces the hard laws that prevent:
- FirstPriorUnit without mandatory fields
- Hypothetical existence being CERTIFIED
- Textual/symbolic/acoustic implying physical without bridge
- FirstPriorUnit producing rules/meanings/judgments/certificates
"""

from typing import List, Optional
from .first_prior_unit import FirstPriorUnit, Rank
from .existence_type import ExistenceType


class ValidationError(Exception):
    """Validation error for FirstPriorUnit."""
    pass


class ProtoPriorValidator:
    """
    Validator for FirstPriorUnit constitutional laws.

    Enforces:
    1. All 14 mandatory fields present and valid
    2. Rank constraints based on existence type
    3. Existence type implication rules
    4. Prohibition of rule/meaning/judgment/certificate production
    """

    @staticmethod
    def validate_first_prior_unit(unit: FirstPriorUnit) -> None:
        """
        Validate FirstPriorUnit against all constitutional laws.

        Raises ValidationError if any law is violated.
        """
        errors: List[str] = []

        # Law 1: All mandatory fields must be present
        try:
            if not unit.is_valid:
                errors.append("FirstPriorUnit has invalid mandatory fields")
        except Exception as e:
            errors.append(f"Validation failed: {str(e)}")

        # Law 2: Hypothetical existence cannot be CERTIFIED
        if unit.existence_type == ExistenceType.HYPOTHETICAL:
            if unit.rank == Rank.CERTIFIED:
                errors.append(
                    "FORBIDDEN: Hypothetical existence cannot be CERTIFIED. "
                    "Hypothetical units remain CANDIDATE or OBSERVED at most."
                )

        # Law 3: Potential existence cannot be CERTIFIED
        if unit.existence_type == ExistenceType.POTENTIAL:
            if unit.rank == Rank.CERTIFIED:
                errors.append(
                    "FORBIDDEN: Potential existence cannot be CERTIFIED. "
                    "Potential units remain CANDIDATE until actualized."
                )

        # Law 4: Linguistic existence claiming physical content cannot be CERTIFIED without bridge
        if unit.existence_type == ExistenceType.LINGUISTIC:
            entity_str = str(unit.entity_or_effect).lower()
            if unit.rank == Rank.CERTIFIED and any(
                keyword in entity_str for keyword in ["physical", "exists physically", "material"]
            ):
                errors.append(
                    "FORBIDDEN: Linguistic/textual existence cannot certify physical existence "
                    "without explicit ExistenceBridge."
                )

        # Law 5: FirstPriorUnit cannot produce rules
        if unit.can_produce_rule():
            errors.append(
                "FORBIDDEN: FirstPriorUnit cannot produce rules. "
                "Rules emerge from PriorGeometry and learning."
            )

        # Law 6: FirstPriorUnit cannot produce meaning
        if unit.can_produce_meaning():
            errors.append(
                "FORBIDDEN: FirstPriorUnit cannot produce meaning. "
                "Meaning emerges from binding and learning."
            )

        # Law 7: FirstPriorUnit cannot issue judgment
        if unit.can_issue_judgment():
            errors.append(
                "FORBIDDEN: FirstPriorUnit cannot issue judgment. "
                "Judgment requires learned binding conditions."
            )

        # Law 8: FirstPriorUnit cannot certify
        if unit.can_certify():
            errors.append(
                "FORBIDDEN: FirstPriorUnit cannot certify results. "
                "Certification requires full audit and evidence."
            )

        # If any errors, raise ValidationError
        if errors:
            error_msg = "\n".join(f"  - {e}" for e in errors)
            raise ValidationError(
                f"FirstPriorUnit validation failed:\n{error_msg}"
            )

    @staticmethod
    def validate_existence_type_promotion(
        source_type: ExistenceType,
        target_type: ExistenceType,
        has_bridge: bool = False
    ) -> None:
        """
        Validate that existence type promotion is allowed.

        Critical law: Linguistic/Hypothetical/Conceptual cannot imply Physical
        without explicit bridge.
        """
        if not has_bridge:
            # Check if promotion is allowed without bridge
            if not source_type.can_imply(target_type):
                raise ValidationError(
                    f"FORBIDDEN: {source_type.name} existence cannot imply "
                    f"{target_type.name} existence without explicit ExistenceBridge."
                )

    @staticmethod
    def validate_rank_promotion(
        current_rank: Rank,
        target_rank: Rank,
        has_evidence: bool = False,
        has_audit: bool = False
    ) -> None:
        """
        Validate that rank promotion is allowed.

        Critical laws:
        - Promotion requires evidence
        - CERTIFIED requires audit
        - Absence of counterexample ≠ CERTIFIED
        """
        if not current_rank.can_promote_to(target_rank):
            raise ValidationError(
                f"Invalid rank promotion: {current_rank.name} cannot promote to {target_rank.name}"
            )

        if target_rank in {Rank.LICENSED, Rank.CERTIFIED}:
            if not has_evidence:
                raise ValidationError(
                    f"Rank promotion to {target_rank.name} requires positive evidence"
                )

        if target_rank == Rank.CERTIFIED:
            if not has_audit:
                raise ValidationError(
                    "Rank promotion to CERTIFIED requires full audit. "
                    "Absence of counterexample is NOT sufficient."
                )

    @staticmethod
    def check_minimal_sufficiency(unit: FirstPriorUnit) -> bool:
        """
        Check if FirstPriorUnit meets minimal sufficiency criteria.

        Minimal sufficient means:
        - Sufficient for entering PriorGeometry
        - Insufficient for producing rules/meanings/judgments

        Returns True if minimally sufficient.
        """
        # Check all mandatory components present
        if not unit.is_valid:
            return False

        # Check capabilities are present
        if not unit.retention_state.is_retainable:
            return False
        if not unit.comparability_state.is_comparable:
            return False
        if not unit.primitive_bindability.is_bindable:
            return False

        # Check prohibitions are enforced
        if unit.can_produce_rule():
            return False
        if unit.can_produce_meaning():
            return False
        if unit.can_issue_judgment():
            return False
        if unit.can_certify():
            return False

        return True
