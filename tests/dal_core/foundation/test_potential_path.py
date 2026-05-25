"""
Tests for Potentiality-Certification Separation Law

Purpose: Verify that carriers CANNOT directly certify, and that certification
         requires PotentialPath + Gate passage.

Constitutional Law Tested:
    Carrierᵢ ⊬ Certificateᵢ₊₁
    Carrierᵢ ⊢ PotentialPathᵢ₊₁ only

Critical Tests:
    - Unicode cannot directly certify Grapheme
    - Grapheme cannot directly certify PhoneticProjection
    - PhoneticProjection cannot directly certify Syllable
    - Syllable cannot directly certify Boundary
    - PotentialPath requires gate passage for certification
    - PotentialWeightedCarrier is same law as all others (not special)

PR: FOUNDATION-POTENTIALITY-LAW
Created: 2026-05-25
"""

import pytest
from dal_core.foundation import (
    PotentialPath,
    PotentialPathStatus,
    Rank,
    certify_path,
    validate_no_direct_certificate,
    DirectCertificationError,
    make_potential_path,
    certify_potential_path,
    block_potential_path,
)
from dal_core.residuals import make_blocker, make_warning


# ============================================================================
# Test PotentialPathStatus Progression
# ============================================================================

def test_potential_path_status_progression():
    """Verify PotentialPathStatus follows correct progression order."""
    assert PotentialPathStatus.CANDIDATE.can_progress_to(PotentialPathStatus.HYPOTHESIS)
    assert PotentialPathStatus.CANDIDATE.can_progress_to(PotentialPathStatus.CERTIFICATE)
    assert PotentialPathStatus.HYPOTHESIS.can_progress_to(PotentialPathStatus.STRONG_HYPOTHESIS)
    assert PotentialPathStatus.STRONG_HYPOTHESIS.can_progress_to(PotentialPathStatus.CERTIFICATE)


def test_blocked_status_cannot_progress():
    """BLOCKED status terminates progression."""
    blocked = PotentialPathStatus.BLOCKED
    assert not blocked.can_progress_to(PotentialPathStatus.CANDIDATE)
    assert not blocked.can_progress_to(PotentialPathStatus.CERTIFICATE)


def test_cannot_regress_from_certificate():
    """Cannot regress from CERTIFICATE to lower status."""
    cert = PotentialPathStatus.CERTIFICATE
    assert not cert.can_progress_to(PotentialPathStatus.CANDIDATE)


# ============================================================================
# Test PotentialPath Creation
# ============================================================================

def test_make_potential_path_creates_candidate():
    """Factory creates PotentialPath in CANDIDATE status."""
    path = make_potential_path(
        source_carrier_id="unicode_123",
        source_layer="U0_UNICODE",
        target_layer="U1_GRAPHEME",
        path_name="ArabicBaseLetter_ك",
        path_family="grapheme",
        required_gates=("grapheme_base_gate",),
        evidence=("unicode_category=Lo",),
        rank=Rank.CANDIDATE,
        trace=("unicode_123",)
    )

    assert path.status == PotentialPathStatus.CANDIDATE
    assert path.source_layer == "U0_UNICODE"
    assert path.target_layer == "U1_GRAPHEME"
    assert path.required_gates == ("grapheme_base_gate",)
    assert path.passed_gates == ()
    assert path.failed_gates == ()


# ============================================================================
# Test Certification Requirements
# ============================================================================

def test_certificate_requires_evidence():
    """CERTIFICATE status requires evidence."""
    with pytest.raises(ValueError, match="CERTIFICATE status requires evidence"):
        PotentialPath(
            path_id="test",
            source_carrier_id="carrier_1",
            source_layer="U0",
            target_layer="U1",
            path_name="test",
            path_family="test",
            status=PotentialPathStatus.CERTIFICATE,  # Certified
            required_gates=("gate1",),
            passed_gates=("gate1",),
            failed_gates=(),
            evidence=(),  # NO EVIDENCE - invalid!
            residuals=frozenset(),
            competitors=(),
            rank=Rank.CERTIFICATE,
            trace=()
        )


def test_certificate_requires_all_gates_passed():
    """CERTIFICATE requires all required_gates in passed_gates."""
    with pytest.raises(ValueError, match="all required_gates in passed_gates"):
        PotentialPath(
            path_id="test",
            source_carrier_id="carrier_1",
            source_layer="U0",
            target_layer="U1",
            path_name="test",
            path_family="test",
            status=PotentialPathStatus.CERTIFICATE,
            required_gates=("gate1", "gate2"),
            passed_gates=("gate1",),  # Missing gate2!
            failed_gates=(),
            evidence=("evidence1",),
            residuals=frozenset(),
            competitors=(),
            rank=Rank.CERTIFICATE,
            trace=()
        )


def test_certificate_cannot_have_failed_gates():
    """CERTIFICATE cannot coexist with failed_gates."""
    with pytest.raises(ValueError, match="cannot coexist with failed_gates"):
        PotentialPath(
            path_id="test",
            source_carrier_id="carrier_1",
            source_layer="U0",
            target_layer="U1",
            path_name="test",
            path_family="test",
            status=PotentialPathStatus.CERTIFICATE,
            required_gates=("gate1",),
            passed_gates=("gate1",),
            failed_gates=("gate2",),  # Failed gate present!
            evidence=("evidence1",),
            residuals=frozenset(),
            competitors=(),
            rank=Rank.CERTIFICATE,
            trace=()
        )


def test_blocked_requires_reason():
    """BLOCKED status requires failed_gates or blocking residuals."""
    with pytest.raises(ValueError, match="BLOCKED status requires"):
        PotentialPath(
            path_id="test",
            source_carrier_id="carrier_1",
            source_layer="U0",
            target_layer="U1",
            path_name="test",
            path_family="test",
            status=PotentialPathStatus.BLOCKED,
            required_gates=("gate1",),
            passed_gates=(),
            failed_gates=(),  # No failed gates
            evidence=(),
            residuals=frozenset(),  # No blocking residuals
            competitors=(),
            rank=Rank.BLOCKED,
            trace=()
        )


# ============================================================================
# Test Certification Process
# ============================================================================

def test_certify_potential_path_success():
    """Successful certification through certify_potential_path()."""
    path = make_potential_path(
        source_carrier_id="carrier_1",
        source_layer="U0_UNICODE",
        target_layer="U1_GRAPHEME",
        path_name="test",
        path_family="grapheme",
        required_gates=("gate1", "gate2"),
        rank=Rank.CANDIDATE,
        trace=()
    )

    certified = certify_potential_path(
        path=path,
        passed_gates=("gate1", "gate2"),
        evidence=("evidence1", "evidence2"),
        residuals=frozenset(),
        rank=Rank.CERTIFICATE
    )

    assert certified.status == PotentialPathStatus.CERTIFICATE
    assert certified.is_certified()
    assert set(certified.passed_gates) == {"gate1", "gate2"}
    assert certified.evidence == ("evidence1", "evidence2")
    assert certified.rank == Rank.CERTIFICATE


def test_certify_potential_path_fails_if_missing_gates():
    """Cannot certify if not all required gates passed."""
    path = make_potential_path(
        source_carrier_id="carrier_1",
        source_layer="U0",
        target_layer="U1",
        path_name="test",
        path_family="test",
        required_gates=("gate1", "gate2", "gate3"),
        rank=Rank.CANDIDATE,
        trace=()
    )

    with pytest.raises(ValueError, match="Missing required gates"):
        certify_potential_path(
            path=path,
            passed_gates=("gate1", "gate2"),  # Missing gate3!
            evidence=("evidence1",),
            residuals=frozenset(),
            rank=Rank.CERTIFICATE
        )


def test_certify_potential_path_fails_if_blocking_residuals():
    """Cannot certify if path has blocking residuals."""
    path = make_potential_path(
        source_carrier_id="carrier_1",
        source_layer="U0",
        target_layer="U1",
        path_name="test",
        path_family="test",
        required_gates=("gate1",),
        rank=Rank.CANDIDATE,
        trace=()
    )

    blocking_residual = make_blocker("test_blocker", "Test blocking reason")

    with pytest.raises(ValueError, match="blocking residuals"):
        certify_potential_path(
            path=path,
            passed_gates=("gate1",),
            evidence=("evidence1",),
            residuals=frozenset([blocking_residual]),  # Blocker present!
            rank=Rank.CERTIFICATE
        )


# ============================================================================
# Test Blocking Process
# ============================================================================

def test_block_potential_path():
    """Block path due to gate failure."""
    path = make_potential_path(
        source_carrier_id="carrier_1",
        source_layer="U0",
        target_layer="U1",
        path_name="test",
        path_family="test",
        required_gates=("gate1",),
        rank=Rank.CANDIDATE,
        trace=()
    )

    blocking_residual = make_blocker("gate_failed", "Gate validation failed")

    blocked = block_potential_path(
        path=path,
        failed_gates=("gate1",),
        residuals=frozenset([blocking_residual]),
        reason="Gate validation failed"
    )

    assert blocked.status == PotentialPathStatus.BLOCKED
    assert blocked.is_blocked()
    assert "gate1" in blocked.failed_gates
    assert blocked.rank == Rank.BLOCKED


# ============================================================================
# Test Direct Certification Prevention (CRITICAL)
# ============================================================================

def test_validate_no_direct_certificate_passes_with_potential_path():
    """Validation passes when PotentialPath exists."""
    # Should NOT raise
    validate_no_direct_certificate(
        carrier_layer="U0_UNICODE",
        certificate_layer="U1_GRAPHEME",
        has_potential_path=True
    )


def test_validate_no_direct_certificate_fails_without_potential_path():
    """CRITICAL: Validation fails when carrier directly certifies."""
    with pytest.raises(DirectCertificationError, match="Constitutional Violation"):
        validate_no_direct_certificate(
            carrier_layer="U0_UNICODE",
            certificate_layer="U1_GRAPHEME",
            has_potential_path=False  # Direct certification!
        )


def test_direct_certification_error_message_explains_law():
    """Error message explains constitutional law."""
    try:
        validate_no_direct_certificate(
            carrier_layer="U0_UNICODE",
            certificate_layer="U1_GRAPHEME",
            has_potential_path=False
        )
        pytest.fail("Should have raised DirectCertificationError")
    except DirectCertificationError as e:
        error_msg = str(e)
        assert "Constitutional Violation" in error_msg
        assert "Carrier ⊬ Certificate" in error_msg
        assert "PotentialPath" in error_msg


# ============================================================================
# Test Layer-Specific Applications
# ============================================================================

def test_unicode_to_grapheme_requires_potential_path():
    """Unicode → Grapheme requires PotentialPath, not direct certificate."""
    # Simulate Unicode carrier
    unicode_carrier_id = "unicode_ك"

    # Create potential path (CORRECT)
    path = make_potential_path(
        source_carrier_id=unicode_carrier_id,
        source_layer="U0_UNICODE",
        target_layer="U1_GRAPHEME",
        path_name="ArabicBaseLetter_ك",
        path_family="grapheme",
        required_gates=("grapheme_base_gate",),
        evidence=("unicode_category=Lo", "script=Arabic"),
        rank=Rank.CANDIDATE,
        trace=(unicode_carrier_id,)
    )

    # Verify it's not certified yet
    assert not path.is_certified()
    assert path.status == PotentialPathStatus.CANDIDATE

    # Direct certification would be invalid
    with pytest.raises(DirectCertificationError):
        validate_no_direct_certificate(
            carrier_layer="U0_UNICODE",
            certificate_layer="U1_GRAPHEME",
            has_potential_path=False
        )


def test_grapheme_to_phonetic_requires_potential_path():
    """Grapheme → PhoneticProjection requires PotentialPath."""
    grapheme_carrier_id = "grapheme_كَ"

    path = make_potential_path(
        source_carrier_id=grapheme_carrier_id,
        source_layer="U1_GRAPHEME",
        target_layer="U2P_PHONETIC_PROJECTION",
        path_name="CVPhonetic_كَ",
        path_family="phonetic",
        required_gates=("phonetic_projection_gate",),
        evidence=("base=ك", "mark=َ"),
        rank=Rank.CANDIDATE,
        trace=(grapheme_carrier_id,)
    )

    assert not path.is_certified()

    # Direct certification would be invalid
    with pytest.raises(DirectCertificationError):
        validate_no_direct_certificate(
            carrier_layer="U1_GRAPHEME",
            certificate_layer="U2P_PHONETIC_PROJECTION",
            has_potential_path=False
        )


def test_phonetic_to_syllable_requires_potential_path():
    """PhoneticProjection → Syllable requires PotentialPath."""
    phonetic_carrier_id = "phonetic_C=/k/_V=/a/"

    path = make_potential_path(
        source_carrier_id=phonetic_carrier_id,
        source_layer="U2P_PHONETIC_PROJECTION",
        target_layer="U2S_SYLLABLE",
        path_name="CVSyllable",
        path_family="syllable",
        required_gates=("syllable_gate",),
        evidence=("nucleus_present=True",),
        rank=Rank.CANDIDATE,
        trace=(phonetic_carrier_id,)
    )

    assert not path.is_certified()

    # Direct certification would be invalid
    with pytest.raises(DirectCertificationError):
        validate_no_direct_certificate(
            carrier_layer="U2P_PHONETIC_PROJECTION",
            certificate_layer="U2S_SYLLABLE",
            has_potential_path=False
        )


def test_syllable_to_boundary_requires_potential_path():
    """Syllable → Boundary requires PotentialPath."""
    syllable_carrier_id = "syllable_sequence_وَبِكِتَابِهِمْ"

    path = make_potential_path(
        source_carrier_id=syllable_carrier_id,
        source_layer="U2S_SYLLABLE",
        target_layer="U3_BOUNDARY_ATTACHMENT",
        path_name="BoundaryPath_وَ_بِـ_كِتَاب_ـهِمْ",
        path_family="boundary",
        required_gates=("boundary_gate",),
        evidence=("morphology_match=True",),
        rank=Rank.CANDIDATE,
        trace=(syllable_carrier_id,)
    )

    assert not path.is_certified()

    # Direct certification would be invalid
    with pytest.raises(DirectCertificationError):
        validate_no_direct_certificate(
            carrier_layer="U2S_SYLLABLE",
            certificate_layer="U3_BOUNDARY_ATTACHMENT",
            has_potential_path=False
        )


def test_root_stem_to_weight_requires_potential_path():
    """CRITICAL: Weight is NOT special - same law applies."""
    root_stem_carrier_id = "root_stem_كتب"

    path = make_potential_path(
        source_carrier_id=root_stem_carrier_id,
        source_layer="U8_ROOT_STEM",
        target_layer="U9_WEIGHT",
        path_name="VerbWeightedPath_فعل",
        path_family="weighted",
        required_gates=("weight_gate",),
        evidence=("pattern_fit=True",),
        rank=Rank.CANDIDATE,
        trace=(root_stem_carrier_id,)
    )

    assert not path.is_certified()

    # Direct certification would be invalid - SAME LAW AS ALL OTHERS
    with pytest.raises(DirectCertificationError):
        validate_no_direct_certificate(
            carrier_layer="U8_ROOT_STEM",
            certificate_layer="U9_WEIGHT",
            has_potential_path=False
        )


# ============================================================================
# Test Competitor Management
# ============================================================================

def test_potential_path_can_have_competitors():
    """Path can list competing paths (e.g., و = consonant vs. long vowel)."""
    path1_id = "path_و_consonant"
    path2_id = "path_و_long_vowel"

    path1 = make_potential_path(
        source_carrier_id="grapheme_و",
        source_layer="U1_GRAPHEME",
        target_layer="U2P_PHONETIC_PROJECTION",
        path_name="ConsonantPath_و",
        path_family="phonetic",
        required_gates=("consonant_gate",),
        rank=Rank.CANDIDATE,
        trace=()
    )

    # Add competitor information
    path1_with_competitor = PotentialPath(
        path_id=path1.path_id,
        source_carrier_id=path1.source_carrier_id,
        source_layer=path1.source_layer,
        target_layer=path1.target_layer,
        path_name=path1.path_name,
        path_family=path1.path_family,
        status=path1.status,
        required_gates=path1.required_gates,
        passed_gates=path1.passed_gates,
        failed_gates=path1.failed_gates,
        evidence=path1.evidence,
        residuals=path1.residuals,
        competitors=(path2_id,),  # Competing path
        rank=path1.rank,
        trace=path1.trace
    )

    assert path2_id in path1_with_competitor.competitors


# ============================================================================
# Integration Tests
# ============================================================================

def test_full_certification_workflow():
    """Integration test: CANDIDATE → gate passage → CERTIFICATE."""
    # Step 1: Carrier produces PotentialPath (CANDIDATE)
    path = make_potential_path(
        source_carrier_id="carrier_test",
        source_layer="U0_UNICODE",
        target_layer="U1_GRAPHEME",
        path_name="test_path",
        path_family="test",
        required_gates=("gate1", "gate2"),
        rank=Rank.CANDIDATE,
        trace=()
    )

    assert path.status == PotentialPathStatus.CANDIDATE
    assert not path.is_certified()

    # Step 2: Gate validates and passes
    # (In real implementation, gate would validate and return evidence)
    gate_evidence = ("gate1_passed", "gate2_passed")

    # Step 3: Certify path
    certified = certify_potential_path(
        path=path,
        passed_gates=("gate1", "gate2"),
        evidence=gate_evidence,
        residuals=frozenset(),
        rank=Rank.CERTIFICATE
    )

    assert certified.status == PotentialPathStatus.CERTIFICATE
    assert certified.is_certified()
    assert certify_path(certified)  # Validator confirms


def test_full_blocking_workflow():
    """Integration test: CANDIDATE → gate failure → BLOCKED."""
    # Step 1: Carrier produces PotentialPath
    path = make_potential_path(
        source_carrier_id="carrier_test",
        source_layer="U0_UNICODE",
        target_layer="U1_GRAPHEME",
        path_name="unattached_mark",
        path_family="grapheme",
        required_gates=("attachment_gate",),
        rank=Rank.CANDIDATE,
        trace=()
    )

    # Step 2: Gate fails (e.g., mark without base)
    blocking_residual = make_blocker("unattached_mark", "Mark requires base letter")

    # Step 3: Block path
    blocked = block_potential_path(
        path=path,
        failed_gates=("attachment_gate",),
        residuals=frozenset([blocking_residual]),
        reason="Unattached mark"
    )

    assert blocked.status == PotentialPathStatus.BLOCKED
    assert blocked.is_blocked()
    assert not blocked.is_certified()


# ============================================================================
# Meta-Test: Constitutional Law Coverage
# ============================================================================

def test_all_layers_subject_to_same_law():
    """META-TEST: Verify law applies to ALL layers, not just weight."""
    layers = [
        ("U0_UNICODE", "U1_GRAPHEME"),
        ("U1_GRAPHEME", "U2P_PHONETIC_PROJECTION"),
        ("U2P_PHONETIC_PROJECTION", "U2S_SYLLABLE"),
        ("U2S_SYLLABLE", "U3_BOUNDARY_ATTACHMENT"),
        ("U3_BOUNDARY_ATTACHMENT", "U4_TRUE_LAFZ"),
        ("U4_TRUE_LAFZ", "U5_FUNCTIONAL_ROLE"),
        ("U5_FUNCTIONAL_ROLE", "U6_MABNI"),
        ("U6_MABNI", "U7_PRE_WEIGHT"),
        ("U7_PRE_WEIGHT", "U8_ROOT_STEM"),
        ("U8_ROOT_STEM", "U9_WEIGHT"),  # Weight is NOT special!
    ]

    for source_layer, target_layer in layers:
        # All must raise DirectCertificationError if no PotentialPath
        with pytest.raises(DirectCertificationError):
            validate_no_direct_certificate(
                carrier_layer=source_layer,
                certificate_layer=target_layer,
                has_potential_path=False
            )

        # All must pass if PotentialPath exists
        validate_no_direct_certificate(
            carrier_layer=source_layer,
            certificate_layer=target_layer,
            has_potential_path=True
        )
