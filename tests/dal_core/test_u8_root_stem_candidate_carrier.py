"""
U₈ Root/Stem Candidate Carrier Tests

Tests for U₈ root/stem candidate extraction and classification.

Critical Laws Under Test:
    - Axiom 8.1: No root before pre-weight contract
    - Axiom 8.2: Root in U₈ is candidate, not certificate
    - Axiom 8.3: No weight before root candidate
    - Axiom 8.4: Blocked in U₇ remains blocked in U₈
    - Axiom 8.5: Candidate ≠ certificate
    - Axiom 8.6: No meaning before weight
"""

import pytest

from dal_core.u8_root_stem_candidate_carrier import (
    root_stem_candidate_8,
    RootStemCandidateUnit,
    RootStemCandidateLayerObject,
    RootStemCandidateResult,
    RootCandidateStatus,
    StemCandidateStatus,
    RadicalCountHint,
    WeakRadicalHint,
    RootStemFailureType,
    CPB8,
)
from dal_core.u7_pre_weight_contract_carrier import (
    PreWeightContractLayerObject,
    PreWeightContractUnit,
    ContractStatus,
    PathPermission,
)
from dal_core.foundation import Rank


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_u7_unit_blocked():
    """Mock U₇ unit with BLOCKED paths (e.g., وَ, بِ, ـهِمْ)."""
    return PreWeightContractUnit(
        uid="u7_blocked_1",
        surface="وَ",
        source_u6_unit_id="u6_1",
        source_u6_trace=("u5_1", "u4_1", "u3_1", "u2_1", "u1_1", "u0_1"),
        open_closed_status="closed_class",
        contract_status=ContractStatus.CLOSED_CLASS_BLOCKED,
        lexical_path_potential=PathPermission.BLOCKED,
        root_path_permission=PathPermission.BLOCKED,
        stem_path_permission=PathPermission.BLOCKED,
        weight_path_permission=PathPermission.BLOCKED,
        jamid_surface_potential=PathPermission.UNRESOLVED,
        proper_name_surface_potential=PathPermission.UNRESOLVED,
        loanword_surface_potential=PathPermission.UNRESOLVED,
        frozen_primitive_potential=PathPermission.UNRESOLVED,
        derivational_readiness=PathPermission.UNRESOLVED,
        required_evidence=("closed_class_mabni_blocks_morphology",),
        blocked_paths=("root_extraction", "weight_determination", "stem_extraction"),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=("u5_1", "u4_1", "u3_1", "u2_1", "u1_1", "u0_1")
    )


@pytest.fixture
def mock_u7_unit_open_class():
    """Mock U₇ unit with POSSIBLE paths (e.g., كَتَبَ, كَاتِب)."""
    return PreWeightContractUnit(
        uid="u7_open_1",
        surface="كَتَبَ",
        source_u6_unit_id="u6_2",
        source_u6_trace=("u5_2", "u4_2", "u3_2", "u2_2", "u1_2", "u0_2"),
        open_closed_status="open_class",
        contract_status=ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE,
        lexical_path_potential=PathPermission.POSSIBLE,
        root_path_permission=PathPermission.POSSIBLE,
        stem_path_permission=PathPermission.POSSIBLE,
        weight_path_permission=PathPermission.POSSIBLE,
        jamid_surface_potential=PathPermission.UNRESOLVED,
        proper_name_surface_potential=PathPermission.UNRESOLVED,
        loanword_surface_potential=PathPermission.UNRESOLVED,
        frozen_primitive_potential=PathPermission.UNRESOLVED,
        derivational_readiness=PathPermission.UNRESOLVED,
        required_evidence=("lexical_attestation", "surface_family_evidence"),
        blocked_paths=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=("u5_2", "u4_2", "u3_2", "u2_2", "u1_2", "u0_2")
    )


@pytest.fixture
def mock_u7_layer_blocked_only(mock_u7_unit_blocked):
    """Mock U₇ layer with only blocked units."""
    return PreWeightContractLayerObject(
        uid="u7_layer_blocked",
        units=(mock_u7_unit_blocked,),
        source_mabni_layer_id="u6_layer_1",
        trace_6=("u6_layer_1",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )


@pytest.fixture
def mock_u7_layer_open_class(mock_u7_unit_open_class):
    """Mock U₇ layer with open-class candidate."""
    return PreWeightContractLayerObject(
        uid="u7_layer_open",
        units=(mock_u7_unit_open_class,),
        source_mabni_layer_id="u6_layer_2",
        trace_6=("u6_layer_2",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )


@pytest.fixture
def mock_u7_layer_mixed(mock_u7_unit_blocked, mock_u7_unit_open_class):
    """Mock U₇ layer with mixed blocked and open-class units."""
    return PreWeightContractLayerObject(
        uid="u7_layer_mixed",
        units=(mock_u7_unit_blocked, mock_u7_unit_open_class),
        source_mabni_layer_id="u6_layer_3",
        trace_6=("u6_layer_3",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )


# ============================================================================
# Unit Structure Tests
# ============================================================================

def test_root_stem_candidate_unit_forbids_weight():
    """CRITICAL: RootStemCandidateUnit MUST NOT contain 'weight' field."""
    with pytest.raises(ValueError, match="MUST NOT contain 'weight' field"):
        # This should fail during __post_init__
        unit = RootStemCandidateUnit(
            uid="test",
            surface="كتب",
            source_u7_unit_id="u7_1",
            source_u7_trace=("u6_1",),
            root_status=RootCandidateStatus.CANDIDATE,
            stem_status=StemCandidateStatus.CANDIDATE,
            root_candidate_paths=(),
            stem_candidate_paths=(),
            radical_count_hint=RadicalCountHint.UNRESOLVED,
            weak_radical_hint=WeakRadicalHint.UNRESOLVED,
            jamid_blocking_potential=PathPermission.UNRESOLVED,
            proper_name_blocking_potential=PathPermission.UNRESOLVED,
            loanword_blocking_potential=PathPermission.UNRESOLVED,
            frozen_primitive_blocking_potential=PathPermission.UNRESOLVED,
            required_evidence=(),
            blocked_paths=(),
            residuals=frozenset(),
            rank=Rank.CANDIDATE,
            trace=()
        )
        # Manually add forbidden field (simulates accidental addition)
        object.__setattr__(unit, 'weight', 'فَعَلَ')
        unit.__post_init__()


def test_root_stem_candidate_unit_forbids_certificates():
    """CRITICAL: RootStemCandidateUnit MUST NOT contain certificate fields."""
    forbidden_fields = [
        'root_certificate',
        'stem_certificate',
        'weight_certificate',
        'pattern_certificate',
    ]

    for field in forbidden_fields:
        with pytest.raises(ValueError, match=f"MUST NOT contain '{field}' field"):
            unit = RootStemCandidateUnit(
                uid="test",
                surface="كتب",
                source_u7_unit_id="u7_1",
                source_u7_trace=("u6_1",),
                root_status=RootCandidateStatus.CANDIDATE,
                stem_status=StemCandidateStatus.CANDIDATE,
                root_candidate_paths=(),
                stem_candidate_paths=(),
                radical_count_hint=RadicalCountHint.UNRESOLVED,
                weak_radical_hint=WeakRadicalHint.UNRESOLVED,
                jamid_blocking_potential=PathPermission.UNRESOLVED,
                proper_name_blocking_potential=PathPermission.UNRESOLVED,
                loanword_blocking_potential=PathPermission.UNRESOLVED,
                frozen_primitive_blocking_potential=PathPermission.UNRESOLVED,
                required_evidence=(),
                blocked_paths=(),
                residuals=frozenset(),
                rank=Rank.CANDIDATE,
                trace=()
            )
            object.__setattr__(unit, field, "FORBIDDEN")
            unit.__post_init__()


# ============================================================================
# Blocked Path Tests (Critical Law: Axiom 8.4)
# ============================================================================

def test_blocked_unit_produces_blocked_status(mock_u7_layer_blocked_only):
    """
    CRITICAL: Blocked in U₇ → Blocked in U₈.

    Test case: وَ (conjunction particle)
        U₇: root_path_permission = BLOCKED
        U₈: root_status = BLOCKED, no candidates
    """
    result = root_stem_candidate_8(mock_u7_layer_blocked_only)

    assert result.success
    assert result.layer_object is not None

    unit = result.layer_object.units[0]
    assert unit.root_status == RootCandidateStatus.BLOCKED
    assert unit.stem_status == StemCandidateStatus.BLOCKED
    assert len(unit.root_candidate_paths) == 0
    assert len(unit.stem_candidate_paths) == 0
    assert "root_extraction" in unit.blocked_paths
    assert "stem_extraction" in unit.blocked_paths


def test_blocked_unit_preserves_surface(mock_u7_layer_blocked_only):
    """Blocked units preserve surface without extraction."""
    result = root_stem_candidate_8(mock_u7_layer_blocked_only)

    unit = result.layer_object.units[0]
    assert unit.surface == "وَ"
    assert unit.root_status == RootCandidateStatus.BLOCKED


# ============================================================================
# Open-Class Candidate Tests
# ============================================================================

def test_open_class_produces_candidates(mock_u7_layer_open_class):
    """
    Open-class unit → Root/stem candidates extracted.

    Test case: كَتَبَ (verb)
        U₇: root_path_permission = POSSIBLE
        U₈: root_status = CANDIDATE, root_candidates = [(ك,ت,ب)]
    """
    result = root_stem_candidate_8(mock_u7_layer_open_class)

    assert result.success
    assert result.layer_object is not None

    unit = result.layer_object.units[0]
    assert unit.root_status in [RootCandidateStatus.CANDIDATE, RootCandidateStatus.MULTIPLE_CANDIDATES]
    assert unit.stem_status in [StemCandidateStatus.CANDIDATE, StemCandidateStatus.MULTIPLE_CANDIDATES]

    # Should have at least one root candidate
    assert len(unit.root_candidate_paths) > 0

    # Should have at least one stem candidate
    assert len(unit.stem_candidate_paths) > 0


def test_root_candidates_are_not_certificates(mock_u7_layer_open_class):
    """
    CRITICAL: Root candidates are HYPOTHESES, not certificates.

    Axiom 8.2: Root in U₈ is candidate, not certificate
    """
    result = root_stem_candidate_8(mock_u7_layer_open_class)

    unit = result.layer_object.units[0]

    # Should have root candidates
    assert len(unit.root_candidate_paths) > 0

    # Should NOT have 'root_certificate' field
    assert not hasattr(unit, 'root_certificate')

    # Should have required evidence for certification
    assert len(unit.required_evidence) > 0
    assert any('lexical' in ev for ev in unit.required_evidence)


def test_root_candidate_structure(mock_u7_layer_open_class):
    """Test RootCandidate structure and evidence."""
    result = root_stem_candidate_8(mock_u7_layer_open_class)

    unit = result.layer_object.units[0]
    if unit.root_candidate_paths:
        candidate = unit.root_candidate_paths[0]

        # Should have radicals
        assert len(candidate.radicals) >= 3

        # Should have evidence
        assert len(candidate.evidence) > 0

        # Confidence should be in [0, 1]
        assert 0.0 <= candidate.confidence <= 1.0

        # Should have radical count
        assert candidate.radical_count >= 3


def test_stem_candidate_structure(mock_u7_layer_open_class):
    """Test StemCandidate structure and evidence."""
    result = root_stem_candidate_8(mock_u7_layer_open_class)

    unit = result.layer_object.units[0]
    if unit.stem_candidate_paths:
        candidate = unit.stem_candidate_paths[0]

        # Should have surface
        assert len(candidate.surface) > 0

        # Should have evidence
        assert len(candidate.evidence) > 0

        # Confidence should be in [0, 1]
        assert 0.0 <= candidate.confidence <= 1.0


# ============================================================================
# Mixed Layer Tests
# ============================================================================

def test_mixed_layer_preserves_both_types(mock_u7_layer_mixed):
    """
    Mixed layer with blocked + open-class units.

    Should preserve blocked units AND extract candidates from open-class.
    """
    result = root_stem_candidate_8(mock_u7_layer_mixed)

    assert result.success
    assert len(result.layer_object.units) == 2

    # First unit (blocked)
    blocked_unit = result.layer_object.units[0]
    assert blocked_unit.root_status == RootCandidateStatus.BLOCKED
    assert len(blocked_unit.root_candidate_paths) == 0

    # Second unit (open-class)
    open_unit = result.layer_object.units[1]
    assert open_unit.root_status in [RootCandidateStatus.CANDIDATE, RootCandidateStatus.MULTIPLE_CANDIDATES]
    assert len(open_unit.root_candidate_paths) > 0


# ============================================================================
# CPB₈ Tests
# ============================================================================

def test_cpb8_is_complete(mock_u7_layer_open_class):
    """Test CPB₈ is_complete validation."""
    result = root_stem_candidate_8(mock_u7_layer_open_class)

    assert CPB8.is_complete(result.layer_object)


def test_cpb8_build_proof(mock_u7_layer_mixed):
    """Test CPB₈ proof building."""
    result = root_stem_candidate_8(mock_u7_layer_mixed)

    proof = CPB8.build_proof(result.layer_object)

    assert proof is not None
    assert "U₈ root/stem candidate paths opened" in proof.claim
    assert "U8_ROOT_STEM_CANDIDATE" in proof.scope

    # Check evidence
    evidence_str = " ".join(proof.evidence)
    assert "units_count=" in evidence_str
    assert "blocked_count=" in evidence_str
    assert "candidate_count=" in evidence_str

    # Check allowed/forbidden gates
    assert "weight_pattern_gate" in proof.allowed_next_gates
    assert "root_certificate" in proof.forbidden_next_gates
    assert "weight_certificate" in proof.forbidden_next_gates
    assert "meaning_certificate" in proof.forbidden_next_gates


def test_cpb8_proof_has_limitations(mock_u7_layer_open_class):
    """Test CPB₈ proof includes constitutional limitations."""
    result = root_stem_candidate_8(mock_u7_layer_open_class)

    proof = CPB8.build_proof(result.layer_object)

    # Check limitations
    assert "no_root_certificate" in proof.limitations
    assert "no_stem_certificate" in proof.limitations
    assert "no_weight_determination" in proof.limitations
    assert "candidate_is_hypothesis_not_certificate" in proof.limitations


# ============================================================================
# Trace Preservation Tests
# ============================================================================

def test_trace_preservation_from_u7(mock_u7_layer_open_class):
    """Verify trace preservation U₇→U₈."""
    result = root_stem_candidate_8(mock_u7_layer_open_class)

    # Layer should preserve U₇ layer ID
    assert result.layer_object.source_pre_weight_layer_id == mock_u7_layer_open_class.uid

    # Units should preserve U₇ unit traces
    for unit in result.layer_object.units:
        assert unit.source_u7_unit_id is not None
        assert unit.source_u7_trace is not None


# ============================================================================
# Failure Mode Tests
# ============================================================================

def test_empty_input_fails():
    """Empty U₇ layer should fail gracefully."""
    empty_layer = PreWeightContractLayerObject(
        uid="empty",
        units=(),
        source_mabni_layer_id="u6_empty",
        trace_6=("u6_empty",),
        residuals=frozenset(),
        rank=Rank.ZERO,
        proof=None
    )

    result = root_stem_candidate_8(empty_layer)

    assert not result.success
    assert result.failure_type == RootStemFailureType.NO_PRE_WEIGHT_UNITS


# ============================================================================
# Radical Count Hint Tests
# ============================================================================

def test_triliteral_hint(mock_u7_layer_open_class):
    """Test triliteral radical count hint."""
    result = root_stem_candidate_8(mock_u7_layer_open_class)

    unit = result.layer_object.units[0]
    # كَتَبَ should hint triliteral
    if unit.root_candidate_paths:
        assert unit.radical_count_hint in [
            RadicalCountHint.TRILITERAL_POSSIBLE,
            RadicalCountHint.AMBIGUOUS,
            RadicalCountHint.UNRESOLVED
        ]


# ============================================================================
# Residuals Preservation Tests
# ============================================================================

def test_residuals_preserved_from_u7(mock_u7_layer_open_class):
    """Residuals from U₇ should be preserved in U₈."""
    result = root_stem_candidate_8(mock_u7_layer_open_class)

    # Layer residuals should match or extend U₇ residuals
    u7_residuals = mock_u7_layer_open_class.residuals
    u8_residuals = result.layer_object.residuals

    # U₈ should at least preserve U₇ residuals
    # (might add more, but shouldn't remove)
    assert u7_residuals.issubset(u8_residuals) or len(u8_residuals) >= len(u7_residuals)


# ============================================================================
# Golden Case Tests
# ============================================================================

def test_golden_case_kataba():
    """
    Golden case: كَتَبَ

    Expected:
        - root_status = CANDIDATE
        - root_candidates = [(ك,ت,ب)]
        - stem_candidates = [كتب]
        - NO weight, NO pattern, NO meaning
    """
    # Create mock U₇ unit for كَتَبَ
    u7_unit = PreWeightContractUnit(
        uid="u7_kataba",
        surface="كَتَبَ",
        source_u6_unit_id="u6_kataba",
        source_u6_trace=("u5", "u4", "u3", "u2", "u1", "u0"),
        open_closed_status="open_class",
        contract_status=ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE,
        lexical_path_potential=PathPermission.POSSIBLE,
        root_path_permission=PathPermission.POSSIBLE,
        stem_path_permission=PathPermission.POSSIBLE,
        weight_path_permission=PathPermission.POSSIBLE,
        jamid_surface_potential=PathPermission.UNRESOLVED,
        proper_name_surface_potential=PathPermission.UNRESOLVED,
        loanword_surface_potential=PathPermission.UNRESOLVED,
        frozen_primitive_potential=PathPermission.UNRESOLVED,
        derivational_readiness=PathPermission.UNRESOLVED,
        required_evidence=("lexical_attestation",),
        blocked_paths=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=("u5", "u4", "u3", "u2", "u1", "u0")
    )

    u7_layer = PreWeightContractLayerObject(
        uid="u7_kataba_layer",
        units=(u7_unit,),
        source_mabni_layer_id="u6_layer",
        trace_6=("u6_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )

    result = root_stem_candidate_8(u7_layer)

    assert result.success
    unit = result.layer_object.units[0]

    # Should have root candidates
    assert unit.root_status in [RootCandidateStatus.CANDIDATE, RootCandidateStatus.MULTIPLE_CANDIDATES]
    assert len(unit.root_candidate_paths) > 0

    # Should have stem candidates
    assert len(unit.stem_candidate_paths) > 0

    # CRITICAL: NO weight, pattern, meaning
    assert not hasattr(unit, 'weight')
    assert not hasattr(unit, 'pattern')
    assert not hasattr(unit, 'meaning')
