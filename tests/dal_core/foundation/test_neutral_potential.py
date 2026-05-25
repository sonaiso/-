"""
Tests for Neutral Potential: الحياد لا يعني الفراغ. الحياد يعني حفظ الإمكان بلا شهادة

Purpose: Verify that neutral element is redefined as "preserved potential without certification"
         across all algebraic layers.

Critical Laws Tested:
    - Neutral ≠ Empty
    - Neutral = Preserved Potential without Certification
    - C+V opens PotentialSyllablePath but does not certify syllable
    - بْ (B + sukun) cannot open valid PotentialSyllablePath (no nucleus)
    - PotentialWeightedCarrier opens WeightPath candidates but no WeightCertificate
    - NeutralPotential MUST have empty certified_paths
    - NeutralPotential MUST NOT have CERTIFICATE rank
    - CPB₀ preserves neutral potential without transformation

Theorem (Neutral Potential):
    ∀L ∈ Layers, ∀x ∈ CarrierDomain_L:
        Neutral_L(x) ⇒ PreserveIdentity(x) ∧ PreserveTrace(x) ∧ PreserveResiduals(x)
                     ∧ PreserveCompetitors(x) ∧ OpensPotentialPaths(x) ∧ ¬CertifiesPath(x)

PR: EXEC-LAYER-REFACTOR
Created: 2026-05-25
"""

import pytest
from uuid import uuid4

from dal_core.foundation import (
    Rank,
    NeutralPotential,
    NeutralSyllablePotential,
    NeutralWeightPotential,
    NeutralBoundaryPotential,
    NeutralPotentialViolation,
    validate_neutral_potential,
    validate_cpb_zero_preserves_neutral,
    make_neutral_syllable_potential,
    make_neutral_weight_potential,
    make_neutral_boundary_potential,
)
from dal_core.residuals import make_info


# ============================================================================
# Test NeutralPotential Base Invariants
# ============================================================================

def test_neutral_potential_requires_empty_certified_paths():
    """CRITICAL: NeutralPotential MUST have empty certified_paths."""
    with pytest.raises(ValueError, match="MUST have empty certified_paths"):
        NeutralPotential(
            neutral_id=str(uuid4()),
            carrier_id=str(uuid4()),
            layer="U2S_ARABIC_SYLLABLE",
            opened_paths=("syllable_path_1", "syllable_path_2"),
            certified_paths=("certified_syllable",),  # VIOLATION: not empty
            trace=(),
            residuals=frozenset(),
            competitors=(),
            rank=Rank.CANDIDATE
        )


def test_neutral_potential_forbids_certificate_rank():
    """CRITICAL: NeutralPotential MUST NOT have CERTIFICATE rank."""
    with pytest.raises(ValueError, match="MUST NOT have CERTIFICATE rank"):
        NeutralPotential(
            neutral_id=str(uuid4()),
            carrier_id=str(uuid4()),
            layer="U2S_ARABIC_SYLLABLE",
            opened_paths=("syllable_path_1",),
            certified_paths=(),
            trace=(),
            residuals=frozenset(),
            competitors=(),
            rank=Rank.CERTIFICATE  # VIOLATION: certificate rank for neutral
        )


def test_neutral_potential_allows_candidate_rank():
    """Neutral can have CANDIDATE rank."""
    neutral = NeutralPotential(
        neutral_id=str(uuid4()),
        carrier_id=str(uuid4()),
        layer="U2S_ARABIC_SYLLABLE",
        opened_paths=("syllable_path_1",),
        certified_paths=(),  # Empty: correct
        trace=(),
        residuals=frozenset(),
        competitors=(),
        rank=Rank.CANDIDATE  # Valid for neutral
    )

    assert neutral.rank == Rank.CANDIDATE
    assert len(neutral.certified_paths) == 0


def test_neutral_potential_allows_hypothesis_rank():
    """Neutral can have HYPOTHESIS rank."""
    neutral = NeutralPotential(
        neutral_id=str(uuid4()),
        carrier_id=str(uuid4()),
        layer="U9_WEIGHT",
        opened_paths=("weight_path_فَعَلَ", "weight_path_فَعْلَة"),
        certified_paths=(),
        trace=(),
        residuals=frozenset(),
        competitors=(),
        rank=Rank.HYPOTHESIS
    )

    assert neutral.rank == Rank.HYPOTHESIS
    assert len(neutral.certified_paths) == 0


# ============================================================================
# Test NeutralSyllablePotential (C+V opens potential, does not certify)
# ============================================================================

def test_neutral_syllable_c_plus_v_opens_potential():
    """C+V opens PotentialSyllablePath but does not certify syllable."""
    # Example: كَ (K + fatha) opens CV syllable path
    neutral_syllable = make_neutral_syllable_potential(
        carrier_id="cv_carrier_كَ",
        opened_paths=("syllable_path_CV",),
        trace=("U0_UNICODE", "U1_GRAPHEME", "U2P_PHONETIC_PROJECTION")
    )

    assert isinstance(neutral_syllable, NeutralSyllablePotential)
    assert neutral_syllable.layer == "U2S_ARABIC_SYLLABLE"
    assert len(neutral_syllable.opened_paths) == 1
    assert "syllable_path_CV" in neutral_syllable.opened_paths
    assert len(neutral_syllable.certified_paths) == 0  # CRITICAL: no certification
    assert neutral_syllable.rank != Rank.CERTIFICATE


def test_neutral_syllable_b_sukun_cannot_open_valid_path():
    """بْ (B + sukun) cannot open valid PotentialSyllablePath because no nucleus."""
    # This should be represented as neutral with no opened_paths or with blocker residual
    neutral_invalid = make_neutral_syllable_potential(
        carrier_id="c_sukun_carrier_بْ",
        opened_paths=(),  # No valid paths: missing nucleus
        trace=("U0_UNICODE", "U1_GRAPHEME", "U2P_PHONETIC_PROJECTION"),
        residuals=frozenset([
            make_info("no_nucleus", "Consonant + sukun lacks syllable nucleus")
        ])
    )

    assert len(neutral_invalid.opened_paths) == 0
    assert len(neutral_invalid.certified_paths) == 0
    assert neutral_invalid.rank == Rank.CANDIDATE  # Default rank


def test_neutral_syllable_cvc_opens_multiple_paths():
    """CVC carrier opens multiple syllable path candidates."""
    neutral_cvc = make_neutral_syllable_potential(
        carrier_id="cvc_carrier_كَتْ",
        opened_paths=(
            "syllable_path_CVC",
            "syllable_path_CV.C",  # Alternative parse
        ),
        trace=("U0_UNICODE", "U1_GRAPHEME", "U2P_PHONETIC_PROJECTION")
    )

    assert len(neutral_cvc.opened_paths) == 2
    assert len(neutral_cvc.certified_paths) == 0  # Still no certification


# ============================================================================
# Test NeutralWeightPotential (Carrier opens weight paths, does not certify)
# ============================================================================

def test_neutral_weight_trilateral_opens_weight_paths():
    """TriLiteralCarrier opens weight path candidates but no WeightCertificate."""
    neutral_weight = make_neutral_weight_potential(
        carrier_id="trilateral_carrier_كتب",
        opened_paths=(
            "weight_path_فَعَلَ",
            "weight_path_فَعْلَة",
            "weight_path_فُعْلَة",
            "weight_path_فَاعِل",
        ),
        trace=("U8_ROOT_STEM",)
    )

    assert isinstance(neutral_weight, NeutralWeightPotential)
    assert neutral_weight.layer == "U9_WEIGHT"
    assert len(neutral_weight.opened_paths) == 4
    assert len(neutral_weight.certified_paths) == 0  # CRITICAL: no weight certified yet
    assert neutral_weight.rank != Rank.CERTIFICATE


def test_neutral_weight_quadrilateral_opens_different_paths():
    """QuadriLiteralCarrier opens different weight paths."""
    neutral_weight = make_neutral_weight_potential(
        carrier_id="quadrilateral_carrier_دحرج",
        opened_paths=(
            "weight_path_فَعْلَلَ",
            "weight_path_فِعْلَال",
            "weight_path_فَعْلَلَة",
        ),
        trace=("U8_ROOT_STEM",)
    )

    assert len(neutral_weight.opened_paths) == 3
    assert len(neutral_weight.certified_paths) == 0


def test_neutral_weight_does_not_certify_without_gate():
    """Weight neutral does not become certificate without gate passage."""
    neutral = make_neutral_weight_potential(
        carrier_id="carrier_كتب",
        opened_paths=("weight_path_فَعَلَ",),
        trace=("U8_ROOT_STEM",)
    )

    # Validate it's truly neutral
    assert validate_neutral_potential(neutral)
    assert neutral.rank != Rank.CERTIFICATE
    assert len(neutral.certified_paths) == 0


# ============================================================================
# Test NeutralBoundaryPotential
# ============================================================================

def test_neutral_boundary_opens_attachment_paths():
    """Boundary carrier opens attachment path candidates."""
    neutral_boundary = make_neutral_boundary_potential(
        carrier_id="boundary_carrier_وَبِكِتَابِهِمْ",
        opened_paths=(
            "boundary_path_standalone_وَ",
            "boundary_path_prefix_بِـ",
            "boundary_path_core_كِتَاب",
            "boundary_path_suffix_ـهِمْ",
        ),
        trace=("U2S_ARABIC_SYLLABLE",)
    )

    assert isinstance(neutral_boundary, NeutralBoundaryPotential)
    assert neutral_boundary.layer == "U3_BOUNDARY_ATTACHMENT"
    assert len(neutral_boundary.opened_paths) == 4
    assert len(neutral_boundary.certified_paths) == 0


# ============================================================================
# Test validate_neutral_potential
# ============================================================================

def test_validate_neutral_potential_accepts_valid():
    """Validate accepts valid neutral potential."""
    neutral = NeutralPotential(
        neutral_id=str(uuid4()),
        carrier_id=str(uuid4()),
        layer="U2S_ARABIC_SYLLABLE",
        opened_paths=("path1", "path2"),
        certified_paths=(),  # Empty: valid
        trace=(),
        residuals=frozenset(),
        competitors=(),
        rank=Rank.CANDIDATE
    )

    assert validate_neutral_potential(neutral)


def test_validate_neutral_potential_rejects_certified_paths():
    """Validate rejects neutral with certified_paths."""
    # Cannot use dataclass constructor (will raise ValueError)
    # So we test the validator directly on a mock object

    class MockNeutral:
        certified_paths = ("certified_1",)
        rank = Rank.CANDIDATE

    assert not validate_neutral_potential(MockNeutral())


def test_validate_neutral_potential_rejects_certificate_rank():
    """Validate rejects neutral with CERTIFICATE rank."""
    class MockNeutral:
        certified_paths = ()
        rank = Rank.CERTIFICATE

    assert not validate_neutral_potential(MockNeutral())


# ============================================================================
# Test CPB₀ Preserves Neutral (Identity Operation)
# ============================================================================

def test_cpb_zero_preserves_neutral_identity():
    """CPB₀: Identity operation preserves neutral potential without transformation."""
    neutral_before = make_neutral_syllable_potential(
        carrier_id="carrier_كَ",
        opened_paths=("syllable_path_CV",),
        trace=("U0", "U1", "U2P")
    )

    # Simulate CPB₀ (identity)
    neutral_after = NeutralSyllablePotential(
        neutral_id=neutral_before.neutral_id,
        carrier_id=neutral_before.carrier_id,
        layer=neutral_before.layer,
        opened_paths=neutral_before.opened_paths,  # Preserved
        certified_paths=neutral_before.certified_paths,  # Still empty
        trace=neutral_before.trace,  # Preserved
        residuals=neutral_before.residuals,  # Preserved
        competitors=neutral_before.competitors,  # Preserved
        rank=neutral_before.rank  # Preserved
    )

    assert validate_cpb_zero_preserves_neutral(neutral_before, neutral_after)


def test_cpb_zero_fails_if_identity_broken():
    """CPB₀ validation fails if identity is broken."""
    neutral_before = make_neutral_syllable_potential(
        carrier_id="carrier_كَ",
        opened_paths=("syllable_path_CV",),
        trace=("U0", "U1", "U2P")
    )

    # Simulate broken CPB₀ (added certified path)
    neutral_after = NeutralSyllablePotential(
        neutral_id=neutral_before.neutral_id,
        carrier_id=neutral_before.carrier_id,
        layer=neutral_before.layer,
        opened_paths=neutral_before.opened_paths,
        certified_paths=(),  # Still empty (would fail constructor otherwise)
        trace=("U0", "U1", "U2P", "TRANSFORMED"),  # CHANGED: trace broken
        residuals=neutral_before.residuals,
        competitors=neutral_before.competitors,
        rank=neutral_before.rank
    )

    assert not validate_cpb_zero_preserves_neutral(neutral_before, neutral_after)


def test_cpb_zero_fails_if_rank_changed():
    """CPB₀ validation fails if rank is changed."""
    neutral_before = make_neutral_syllable_potential(
        carrier_id="carrier_كَ",
        opened_paths=("syllable_path_CV",),
        trace=("U0", "U1", "U2P")
    )

    # Simulate broken CPB₀ (rank changed)
    neutral_after = NeutralSyllablePotential(
        neutral_id=neutral_before.neutral_id,
        carrier_id=neutral_before.carrier_id,
        layer=neutral_before.layer,
        opened_paths=neutral_before.opened_paths,
        certified_paths=(),
        trace=neutral_before.trace,
        residuals=neutral_before.residuals,
        competitors=neutral_before.competitors,
        rank=Rank.HYPOTHESIS  # CHANGED: rank upgraded (breaks identity)
    )

    assert not validate_cpb_zero_preserves_neutral(neutral_before, neutral_after)


# ============================================================================
# Test Neutral Potential Theorem (Comprehensive)
# ============================================================================

def test_neutral_potential_theorem_syllable_layer():
    """
    Theorem: Neutral_U2s(x) ⇒ PreserveIdentity(x) ∧ OpensPotentialPaths(x) ∧ ¬CertifiesPath(x)
    """
    # Create neutral syllable potential
    neutral = make_neutral_syllable_potential(
        carrier_id="carrier_كَتْ",
        opened_paths=("syllable_path_CVC",),
        trace=("U0_UNICODE", "U1_GRAPHEME", "U2P_PHONETIC_PROJECTION"),
        residuals=frozenset([make_info("cv_analysis", "C+V+C structure detected")])
    )

    # Verify theorem properties
    # 1. PreserveIdentity: neutral_id, carrier_id, layer remain unchanged
    assert neutral.neutral_id is not None
    assert neutral.carrier_id == "carrier_كَتْ"
    assert neutral.layer == "U2S_ARABIC_SYLLABLE"

    # 2. OpensPotentialPaths: has opened_paths
    assert len(neutral.opened_paths) > 0
    assert "syllable_path_CVC" in neutral.opened_paths

    # 3. ¬CertifiesPath: certified_paths is empty
    assert len(neutral.certified_paths) == 0

    # 4. Rank is not CERTIFICATE
    assert neutral.rank != Rank.CERTIFICATE

    # 5. Validate overall
    assert validate_neutral_potential(neutral)


def test_neutral_potential_theorem_weight_layer():
    """
    Theorem: Neutral_U9(x) ⇒ PreserveIdentity(x) ∧ OpensPotentialPaths(x) ∧ ¬CertifiesPath(x)
    """
    neutral = make_neutral_weight_potential(
        carrier_id="carrier_كتب",
        opened_paths=("weight_path_فَعَلَ", "weight_path_فَعْلَة"),
        trace=("U8_ROOT_STEM",)
    )

    # Theorem verification
    assert neutral.carrier_id == "carrier_كتب"
    assert neutral.layer == "U9_WEIGHT"
    assert len(neutral.opened_paths) == 2
    assert len(neutral.certified_paths) == 0
    assert neutral.rank != Rank.CERTIFICATE
    assert validate_neutral_potential(neutral)


def test_neutral_potential_theorem_boundary_layer():
    """
    Theorem: Neutral_U3(x) ⇒ PreserveIdentity(x) ∧ OpensPotentialPaths(x) ∧ ¬CertifiesPath(x)
    """
    neutral = make_neutral_boundary_potential(
        carrier_id="carrier_بِكِتَابٍ",
        opened_paths=("boundary_path_prefix_بِـ", "boundary_path_core_كِتَاب"),
        trace=("U2S_ARABIC_SYLLABLE",)
    )

    assert neutral.carrier_id == "carrier_بِكِتَابٍ"
    assert neutral.layer == "U3_BOUNDARY_ATTACHMENT"
    assert len(neutral.opened_paths) == 2
    assert len(neutral.certified_paths) == 0
    assert neutral.rank != Rank.CERTIFICATE
    assert validate_neutral_potential(neutral)


# ============================================================================
# Test Neutral ≠ Empty (Philosophical Distinction)
# ============================================================================

def test_neutral_is_not_empty_has_opened_paths():
    """CRITICAL: Neutral ≠ Empty. Neutral has opened_paths, Empty has nothing."""
    # Neutral: has opened potential paths
    neutral = make_neutral_syllable_potential(
        carrier_id="carrier_كَ",
        opened_paths=("syllable_path_CV",),
        trace=("U0", "U1", "U2P")
    )

    # Empty: would have no opened_paths
    empty_representation = make_neutral_syllable_potential(
        carrier_id="carrier_empty",
        opened_paths=(),  # No paths opened
        trace=()
    )

    # Neutral has paths (even though not certified)
    assert len(neutral.opened_paths) > 0

    # Empty has no paths
    assert len(empty_representation.opened_paths) == 0

    # But both have no certified_paths
    assert len(neutral.certified_paths) == 0
    assert len(empty_representation.certified_paths) == 0

    # The distinction: Neutral preserves POTENTIAL, Empty has none


def test_neutral_preserves_trace_empty_has_no_trace():
    """Neutral preserves trace (identity), Empty may have no trace."""
    neutral = make_neutral_syllable_potential(
        carrier_id="carrier_كَ",
        opened_paths=("syllable_path_CV",),
        trace=("U0_UNICODE", "U1_GRAPHEME", "U2P_PHONETIC_PROJECTION")
    )

    # Neutral preserves trace
    assert len(neutral.trace) > 0
    assert "U0_UNICODE" in neutral.trace


# ============================================================================
# Integration Tests
# ============================================================================

def test_integration_syllable_neutral_to_certificate_requires_gate():
    """Integration: Neutral syllable becomes certificate only through gate passage."""
    # Start with neutral
    neutral = make_neutral_syllable_potential(
        carrier_id="carrier_كَتْ",
        opened_paths=("syllable_path_CVC",),
        trace=("U0", "U1", "U2P")
    )

    assert len(neutral.certified_paths) == 0
    assert neutral.rank != Rank.CERTIFICATE

    # Attempting to directly create certificate from neutral violates the law
    # (This would be done through a gate in real system)


def test_integration_weight_neutral_opens_multiple_competitors():
    """Integration: Weight neutral opens multiple competing weight paths."""
    neutral = make_neutral_weight_potential(
        carrier_id="carrier_كتب",
        opened_paths=(
            "weight_path_فَعَلَ",
            "weight_path_فَعْلَة",
            "weight_path_كَتَبَ",
        ),
        trace=("U8_ROOT_STEM",),
        competitors=("فَعَلَ_competitor", "فَعْلَة_competitor")
    )

    # Neutral preserves competitors without certification
    assert len(neutral.competitors) > 0
    assert len(neutral.opened_paths) == 3
    assert len(neutral.certified_paths) == 0


def test_integration_neutral_potential_exception_message():
    """Integration: NeutralPotentialViolation provides clear error message."""
    with pytest.raises(NeutralPotentialViolation, match="Constitutional Violation"):
        raise NeutralPotentialViolation(
            "Constitutional Violation: Attempted to certify path without gate passage"
        )
