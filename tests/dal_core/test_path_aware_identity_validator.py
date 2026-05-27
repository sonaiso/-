"""
Tests for Path-Aware Identity Validator (PR-128)

Validates that identity transitions only occur through licensed paths.

Constitutional Law:
    لا هوية بلا مسار مرخّص
    No identity without licensed path.

Test Coverage:
1. test_identity_rejects_no_path_evidence
2. test_identity_accepts_weight_path_with_weight_evidence
3. test_identity_accepts_mabni_path_without_weight
4. test_identity_accepts_tool_path_without_weight
5. test_identity_accepts_pronoun_path_without_weight
6. test_identity_accepts_jamid_path_without_weight
7. test_identity_preserves_lafz_anchor_id
8. test_identity_preserves_slot_trace
9. test_identity_inherits_residuals
10. test_identity_does_not_output_meaning
11. test_identity_does_not_output_syntax_role
12. test_identity_does_not_output_i3rab
13. test_identity_does_not_output_ifadah_or_hukm
14. test_identity_rank_is_not_certificate
15. test_identity_rejects_missing_evidence_keys
16. test_identity_rejects_wrong_source_domain
17. test_residualized_path_accepts_existing_identity

Created: 2026-05-27 (PR-128)
"""

import pytest
from dal_core.path_aware_identity_validator import (
    PathAwareIdentityValidator,
    IdentityPathType,
    PathEvidence,
    IdentityCandidate,
)
from dal_core.dal_algebra import AlgebraicFailure
from dal_core.domain_registry import DomainType
from dal_core.identity_registry import IdentityType
from dal_core.pipeline import Rank


class TestPathAwareIdentityValidator:
    """Test path-aware identity validation."""

    def test_identity_rejects_no_path_evidence(self):
        """
        Identity must be REJECTED when no path evidence exists.

        Constitutional law: لا هوية بلا مسار مرخّص
        """
        validator = PathAwareIdentityValidator()

        # Try to get identity without any valid path evidence
        result = validator.validate_no_path_rejection(
            source_domain=DomainType.LAFZ_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            evidence={}  # No evidence
        )

        # Must be AlgebraicFailure
        assert isinstance(result, AlgebraicFailure)
        assert "no licensed path" in result.reason.lower()

    def test_identity_accepts_weight_path_with_weight_evidence(self):
        """
        Identity must be ACCEPTED via weight path when weight evidence exists.

        Path: WEIGHT_DOMAIN → WORDFORM_IDENTITY
        Evidence: weight_pattern, root_or_stem
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب",
                "confidence": 0.9
            }
        )

        # Must be IdentityCandidate (success)
        assert isinstance(result, IdentityCandidate)
        assert result.identity_type == IdentityType.WORDFORM_IDENTITY
        assert result.path_evidence.path_type == IdentityPathType.WEIGHT_PATH
        assert result.path_evidence.source_domain == DomainType.WEIGHT_DOMAIN
        assert result.path_evidence.evidence_present is True

    def test_identity_accepts_mabni_path_without_weight(self):
        """
        Identity must be ACCEPTED via mabni path WITHOUT requiring weight.

        Path: LAFZ_DOMAIN → WORDFORM_IDENTITY (mabni/closed-class)
        Evidence: closed_class_marker
        Examples: ما، هل، إن، كان...
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.LAFZ_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.MABNI_PATH,
            evidence={
                "closed_class_marker": "مبني",
                "examples": ["ما", "هل", "إن"]
            }
        )

        # Must be IdentityCandidate (success)
        assert isinstance(result, IdentityCandidate)
        assert result.identity_type == IdentityType.WORDFORM_IDENTITY
        assert result.path_evidence.path_type == IdentityPathType.MABNI_PATH
        assert result.path_evidence.source_domain == DomainType.LAFZ_DOMAIN
        # Critically: NO WEIGHT_DOMAIN involved
        assert result.path_evidence.source_domain != DomainType.WEIGHT_DOMAIN

    def test_identity_accepts_tool_path_without_weight(self):
        """
        Identity must be ACCEPTED via tool/particle path WITHOUT requiring weight.

        Path: LAFZ_DOMAIN → WORDFORM_IDENTITY (particle)
        Evidence: particle_type
        Examples: في، على، من، إلى...
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.LAFZ_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.TOOL_PATH,
            evidence={
                "particle_type": "حرف جر",
                "examples": ["في", "على", "من"]
            }
        )

        # Must be IdentityCandidate (success)
        assert isinstance(result, IdentityCandidate)
        assert result.identity_type == IdentityType.WORDFORM_IDENTITY
        assert result.path_evidence.path_type == IdentityPathType.TOOL_PATH
        assert result.path_evidence.source_domain == DomainType.LAFZ_DOMAIN

    def test_identity_accepts_pronoun_path_without_weight(self):
        """
        Identity must be ACCEPTED via pronoun path WITHOUT requiring weight.

        Path: LAFZ_DOMAIN → WORDFORM_IDENTITY (pronoun)
        Evidence: pronoun_class
        Examples: هو، أنت، هم...
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.LAFZ_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.PRONOUN_PATH,
            evidence={
                "pronoun_class": "ضمير منفصل",
                "examples": ["هو", "أنت", "هم"]
            }
        )

        # Must be IdentityCandidate (success)
        assert isinstance(result, IdentityCandidate)
        assert result.identity_type == IdentityType.WORDFORM_IDENTITY
        assert result.path_evidence.path_type == IdentityPathType.PRONOUN_PATH
        assert result.path_evidence.source_domain == DomainType.LAFZ_DOMAIN

    def test_identity_accepts_jamid_path_without_weight(self):
        """
        Identity must be ACCEPTED via jāmid/frozen path WITHOUT requiring weight.

        Path: LAFZ_DOMAIN → WORDFORM_IDENTITY (jāmid)
        Evidence: jamid_marker
        Examples: Frozen nouns not derived from patterns
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.LAFZ_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.JAMID_PATH,
            evidence={
                "jamid_marker": "جامد",
                "note": "Frozen noun, not pattern-derived"
            }
        )

        # Must be IdentityCandidate (success)
        assert isinstance(result, IdentityCandidate)
        assert result.identity_type == IdentityType.WORDFORM_IDENTITY
        assert result.path_evidence.path_type == IdentityPathType.JAMID_PATH
        assert result.path_evidence.source_domain == DomainType.LAFZ_DOMAIN

    def test_identity_preserves_lafz_anchor_id(self):
        """Identity candidate must preserve lafz_anchor_id."""
        validator = PathAwareIdentityValidator()

        lafz_anchor = "lafz_12345"

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            },
            lafz_anchor_id=lafz_anchor
        )

        assert isinstance(result, IdentityCandidate)
        assert result.lafz_anchor_id == lafz_anchor
        assert result.path_evidence.lafz_anchor_id == lafz_anchor

    def test_identity_preserves_slot_trace(self):
        """Identity candidate must preserve slot_trace."""
        validator = PathAwareIdentityValidator()

        slot_trace = (0, 1, 2, 3)

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            },
            slot_trace=slot_trace
        )

        assert isinstance(result, IdentityCandidate)
        assert result.slot_trace == slot_trace
        assert result.path_evidence.slot_trace == slot_trace

    def test_identity_inherits_residuals(self):
        """Identity candidate must inherit residuals from transition."""
        validator = PathAwareIdentityValidator()

        residuals = ("unresolved_hamza", "potential_idgham")

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            },
            residuals=residuals
        )

        assert isinstance(result, IdentityCandidate)
        assert result.residuals == residuals

    def test_identity_does_not_output_meaning(self):
        """
        Identity candidate must NOT output meaning.

        Identity ≠ meaning (constitutional law).
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            }
        )

        assert isinstance(result, IdentityCandidate)
        # Check that IdentityCandidate has no meaning field
        assert not hasattr(result, "meaning")
        assert not hasattr(result, "murad")
        assert not hasattr(result, "semantic_interpretation")

    def test_identity_does_not_output_syntax_role(self):
        """
        Identity candidate must NOT output syntactic_role.

        Identity ≠ syntactic function (constitutional law).
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            }
        )

        assert isinstance(result, IdentityCandidate)
        # Check that IdentityCandidate has no syntactic_role field
        assert not hasattr(result, "syntactic_role")
        assert not hasattr(result, "faa_il")
        assert not hasattr(result, "maf_ool")

    def test_identity_does_not_output_i3rab(self):
        """
        Identity candidate must NOT output iʿrab.

        Identity ≠ iʿrab judgment (constitutional law).
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            }
        )

        assert isinstance(result, IdentityCandidate)
        # Check that IdentityCandidate has no i3rab field
        assert not hasattr(result, "i3rab")
        assert not hasattr(result, "case_marking")
        assert not hasattr(result, "raf_nasb_jarr")

    def test_identity_does_not_output_ifadah_or_hukm(self):
        """
        Identity candidate must NOT output ifādah or hukm.

        Identity ≠ ifādah ≠ hukm (constitutional law).
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            }
        )

        assert isinstance(result, IdentityCandidate)
        # Check that IdentityCandidate has no ifādah/hukm fields
        assert not hasattr(result, "ifadah")
        assert not hasattr(result, "tamam_ifadah")
        assert not hasattr(result, "hukm")
        assert not hasattr(result, "judgment")

    def test_identity_rank_is_not_certificate(self):
        """
        Identity candidate rank must be < 1.0 (NOT CERTIFICATE).

        Identity is candidate, not certificate (constitutional law).
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب",
                "confidence": 0.95
            }
        )

        assert isinstance(result, IdentityCandidate)
        assert result.rank < 1.0, f"Rank {result.rank} must be < 1.0 (not CERTIFICATE)"
        assert result.rank >= 0.0, f"Rank {result.rank} must be >= 0.0"

    def test_identity_rejects_missing_evidence_keys(self):
        """
        Identity must be REJECTED when required evidence keys are missing.

        Each path requires specific evidence keys.
        """
        validator = PathAwareIdentityValidator()

        # Weight path requires: weight_pattern, root_or_stem
        # Only provide weight_pattern (missing root_or_stem)
        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل"
                # Missing: root_or_stem
            }
        )

        # Must be AlgebraicFailure
        assert isinstance(result, AlgebraicFailure)
        assert "missing required evidence" in result.reason.lower()
        assert result.evidence_gap is not None

    def test_identity_rejects_wrong_source_domain(self):
        """
        Identity must be REJECTED when source_domain doesn't match path.

        Example: Weight path requires WEIGHT_DOMAIN, not LAFZ_DOMAIN.
        """
        validator = PathAwareIdentityValidator()

        # Weight path requires WEIGHT_DOMAIN source
        # But provide LAFZ_DOMAIN (wrong)
        result = validator.validate_identity_transition(
            source_domain=DomainType.LAFZ_DOMAIN,  # WRONG
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            }
        )

        # Must be AlgebraicFailure
        assert isinstance(result, AlgebraicFailure)
        assert "source domain" in result.reason.lower()
        assert result.domain_violation is not None

    def test_residualized_path_accepts_existing_identity(self):
        """
        Residualized path must accept existing identity with residuals.

        Path: IDENTITY_DOMAIN → IDENTITY_DOMAIN (with residuals)
        Evidence: existing_identity, residuals
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.IDENTITY_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.RESIDUALIZED_PATH,
            evidence={
                "existing_identity": "WORDFORM_IDENTITY",
                "residuals": ["unresolved_hamza"]
            },
            residuals=("unresolved_hamza",)
        )

        # Must be IdentityCandidate (success)
        assert isinstance(result, IdentityCandidate)
        assert result.identity_type == IdentityType.WORDFORM_IDENTITY
        assert result.path_evidence.path_type == IdentityPathType.RESIDUALIZED_PATH
        assert len(result.residuals) > 0


class TestPathEvidenceImmutability:
    """Test that PathEvidence is truly immutable."""

    def test_path_evidence_details_immutable(self):
        """PathEvidence.details must be MappingProxyType (immutable)."""
        from types import MappingProxyType

        evidence = PathEvidence(
            path_type=IdentityPathType.WEIGHT_PATH,
            source_domain=DomainType.WEIGHT_DOMAIN,
            evidence_present=True,
            details={"key": "value"}
        )

        assert isinstance(evidence.details, MappingProxyType)

        # Try to modify (should fail)
        with pytest.raises(TypeError):
            evidence.details["new_key"] = "new_value"


class TestIdentityCandidateImmutability:
    """Test that IdentityCandidate is truly immutable."""

    def test_identity_candidate_residuals_tuple(self):
        """IdentityCandidate.residuals must be tuple (immutable)."""
        candidate = IdentityCandidate(
            identity_type=IdentityType.WORDFORM_IDENTITY,
            path_evidence=PathEvidence(
                path_type=IdentityPathType.WEIGHT_PATH,
                source_domain=DomainType.WEIGHT_DOMAIN,
                evidence_present=True
            ),
            rank=0.8,
            residuals=["unresolved_hamza"]  # Pass list, should coerce to tuple
        )

        assert isinstance(candidate.residuals, tuple)

    def test_identity_candidate_rank_validation(self):
        """IdentityCandidate rank must be in [0.0, 1.0) (not certificate)."""
        # Valid rank
        candidate = IdentityCandidate(
            identity_type=IdentityType.WORDFORM_IDENTITY,
            path_evidence=PathEvidence(
                path_type=IdentityPathType.WEIGHT_PATH,
                source_domain=DomainType.WEIGHT_DOMAIN,
                evidence_present=True
            ),
            rank=0.9
        )
        assert candidate.rank == 0.9

        # Invalid rank (negative)
        with pytest.raises(ValueError, match="non-negative"):
            IdentityCandidate(
                identity_type=IdentityType.WORDFORM_IDENTITY,
                path_evidence=PathEvidence(
                    path_type=IdentityPathType.WEIGHT_PATH,
                    source_domain=DomainType.WEIGHT_DOMAIN,
                    evidence_present=True
                ),
                rank=-0.1
            )

        # Invalid rank (certificate)
        with pytest.raises(ValueError, match="CERTIFICATE"):
            IdentityCandidate(
                identity_type=IdentityType.WORDFORM_IDENTITY,
                path_evidence=PathEvidence(
                    path_type=IdentityPathType.WEIGHT_PATH,
                    source_domain=DomainType.WEIGHT_DOMAIN,
                    evidence_present=True
                ),
                rank=1.0  # Certificate forbidden
            )


class TestIntegration:
    """Integration tests for path-aware identity validation."""

    def test_all_six_paths_work(self):
        """
        All six licensed paths must work when evidence is present.

        Paths:
        1. Weight path
        2. Mabni path
        3. Tool path
        4. Pronoun path
        5. Jāmid path
        6. Residualized path
        """
        validator = PathAwareIdentityValidator()

        paths_to_test = [
            (IdentityPathType.WEIGHT_PATH, DomainType.WEIGHT_DOMAIN, {
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            }),
            (IdentityPathType.MABNI_PATH, DomainType.LAFZ_DOMAIN, {
                "closed_class_marker": "مبني"
            }),
            (IdentityPathType.TOOL_PATH, DomainType.LAFZ_DOMAIN, {
                "particle_type": "حرف"
            }),
            (IdentityPathType.PRONOUN_PATH, DomainType.LAFZ_DOMAIN, {
                "pronoun_class": "ضمير"
            }),
            (IdentityPathType.JAMID_PATH, DomainType.LAFZ_DOMAIN, {
                "jamid_marker": "جامد"
            }),
            (IdentityPathType.RESIDUALIZED_PATH, DomainType.IDENTITY_DOMAIN, {
                "existing_identity": "WORDFORM_IDENTITY",
                "residuals": ["unresolved"]
            }),
        ]

        for path_type, source_domain, evidence in paths_to_test:
            result = validator.validate_identity_transition(
                source_domain=source_domain,
                target_identity=IdentityType.WORDFORM_IDENTITY,
                path_type=path_type,
                evidence=evidence
            )

            assert isinstance(result, IdentityCandidate), (
                f"Path {path_type} should succeed with proper evidence"
            )
            assert result.path_evidence.path_type == path_type


class TestForbiddenTargetIdentities:
    """Test that forbidden target identities are rejected (PR-128 fix)."""

    def test_tool_path_cannot_target_semantic_identity(self):
        """
        Tool path must REJECT SEMANTIC_IDENTITY as target.

        Constitutional law: Identity path validation cannot target semantic layer.
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.LAFZ_DOMAIN,
            target_identity=IdentityType.SEMANTIC_IDENTITY,  # FORBIDDEN
            path_type=IdentityPathType.TOOL_PATH,
            evidence={
                "particle_type": "حرف جر"
            }
        )

        # Must be AlgebraicFailure
        assert isinstance(result, AlgebraicFailure)
        assert "forbidden" in result.reason.lower()
        assert result.gate == "forbidden_target_identity_gate"

    def test_weight_path_cannot_target_hukm_identity(self):
        """
        Weight path must REJECT HUKM_IDENTITY as target.

        Constitutional law: Identity path validation cannot target judgment layer.
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.HUKM_IDENTITY,  # FORBIDDEN
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            }
        )

        # Must be AlgebraicFailure
        assert isinstance(result, AlgebraicFailure)
        assert "forbidden" in result.reason.lower()
        assert result.gate == "forbidden_target_identity_gate"

    def test_mabni_path_cannot_target_ifadah_identity(self):
        """
        Mabni path must REJECT IFADAH_IDENTITY as target.

        Constitutional law: Identity path validation cannot target ifādah layer.
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.LAFZ_DOMAIN,
            target_identity=IdentityType.IFADAH_IDENTITY,  # FORBIDDEN
            path_type=IdentityPathType.MABNI_PATH,
            evidence={
                "closed_class_marker": "مبني"
            }
        )

        # Must be AlgebraicFailure
        assert isinstance(result, AlgebraicFailure)
        assert "forbidden" in result.reason.lower()
        assert result.gate == "forbidden_target_identity_gate"

    def test_pronoun_path_cannot_target_functional_relation_identity(self):
        """
        Pronoun path must REJECT FUNCTIONAL_RELATION_IDENTITY as target.

        Constitutional law: Identity path validation cannot target functional relation layer.
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.LAFZ_DOMAIN,
            target_identity=IdentityType.FUNCTIONAL_RELATION_IDENTITY,  # FORBIDDEN
            path_type=IdentityPathType.PRONOUN_PATH,
            evidence={
                "pronoun_class": "ضمير منفصل"
            }
        )

        # Must be AlgebraicFailure
        assert isinstance(result, AlgebraicFailure)
        assert "forbidden" in result.reason.lower()
        assert result.gate == "forbidden_target_identity_gate"

    def test_jamid_path_cannot_target_amil_identity(self):
        """
        Jāmid path must REJECT AMIL_IDENTITY as target.

        Constitutional law: Identity path validation cannot target operator identities.
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.LAFZ_DOMAIN,
            target_identity=IdentityType.AMIL_IDENTITY,  # FORBIDDEN
            path_type=IdentityPathType.JAMID_PATH,
            evidence={
                "jamid_marker": "جامد"
            }
        )

        # Must be AlgebraicFailure
        assert isinstance(result, AlgebraicFailure)
        assert "forbidden" in result.reason.lower()
        assert result.gate == "forbidden_target_identity_gate"

    def test_weight_path_cannot_target_maamul_identity(self):
        """
        Weight path must REJECT MAAMUL_IDENTITY as target.

        Constitutional law: Identity path validation cannot target operator identities.
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.MAAMUL_IDENTITY,  # FORBIDDEN
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "مفعول",
                "root_or_stem": "كتب"
            }
        )

        # Must be AlgebraicFailure
        assert isinstance(result, AlgebraicFailure)
        assert "forbidden" in result.reason.lower()
        assert result.gate == "forbidden_target_identity_gate"

    def test_identity_validator_rejects_forbidden_target_even_with_valid_evidence(self):
        """
        Validator must reject forbidden target identity EVEN with valid evidence.

        This is critical: evidence quality doesn't matter if target is forbidden.
        """
        validator = PathAwareIdentityValidator()

        # Perfect evidence, but forbidden target
        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.SEMANTIC_IDENTITY,  # FORBIDDEN
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب",
                "confidence": 0.99,  # High confidence
                "rank": "TAWATUR"  # Strong rank
            }
        )

        # Must STILL be AlgebraicFailure (target is forbidden)
        assert isinstance(result, AlgebraicFailure)
        assert "forbidden" in result.reason.lower()
        assert result.gate == "forbidden_target_identity_gate"


class TestRankAndConfidence:
    """Test Rank enum and confidence float usage (PR-128 fix)."""

    def test_identity_candidate_uses_rank_enum(self):
        """
        IdentityCandidate must use Rank enum (NOT float).
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب"
            }
        )

        assert isinstance(result, IdentityCandidate)
        assert isinstance(result.rank, Rank)
        assert result.rank != Rank.CERT  # Must NOT be CERT

    def test_identity_candidate_has_confidence_float(self):
        """
        IdentityCandidate must have separate confidence float [0.0, 1.0).
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب",
                "confidence": 0.85
            }
        )

        assert isinstance(result, IdentityCandidate)
        assert isinstance(result.confidence, float)
        assert 0.0 <= result.confidence < 1.0

    def test_identity_candidate_rejects_rank_cert(self):
        """
        IdentityCandidate must REJECT Rank.CERT (certificate forbidden).
        """
        from dal_core.path_aware_identity_validator import PathEvidence

        # Try to create IdentityCandidate with Rank.CERT (should fail)
        with pytest.raises(ValueError, match="CERT.*forbidden"):
            IdentityCandidate(
                identity_type=IdentityType.WORDFORM_IDENTITY,
                path_evidence=PathEvidence(
                    path_type=IdentityPathType.WEIGHT_PATH,
                    source_domain=DomainType.WEIGHT_DOMAIN,
                    evidence_present=True
                ),
                rank=Rank.CERT,  # FORBIDDEN
                confidence=0.9
            )

    def test_identity_candidate_accepts_form_rank(self):
        """
        IdentityCandidate must ACCEPT Rank.FORM (candidate rank).
        """
        from dal_core.path_aware_identity_validator import PathEvidence

        candidate = IdentityCandidate(
            identity_type=IdentityType.WORDFORM_IDENTITY,
            path_evidence=PathEvidence(
                path_type=IdentityPathType.WEIGHT_PATH,
                source_domain=DomainType.WEIGHT_DOMAIN,
                evidence_present=True
            ),
            rank=Rank.FORM,  # OK
            confidence=0.8
        )

        assert candidate.rank == Rank.FORM

    def test_validator_respects_evidence_rank(self):
        """
        Validator must respect rank suggestion from evidence (if not CERT).
        """
        validator = PathAwareIdentityValidator()

        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={
                "weight_pattern": "فاعل",
                "root_or_stem": "كتب",
                "rank": "QIYAS"  # Suggest QIYAS rank
            }
        )

        assert isinstance(result, IdentityCandidate)
        assert result.rank == Rank.QIYAS


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
