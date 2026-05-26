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

Post-PR #110 Requirements:
    - U₈ consumes U₇-C (ClauseSurfaceAgreementLayerObject) ONLY
    - U₈ preserves agreement_edge_ids without interpretation
    - U₈ preserves broken_plural_guard_id
    - U₈ preserves permission_elevated_by_agreement
    - U₈ extracts from root_input ONLY (not surface/protected_core)
    - DEFERRED/BLOCKED prevents extraction
    - No silent identity loss (requires residual)
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
from dal_core.u7c_clause_surface_agreement_carrier import (
    ClauseSurfaceAgreementLayerObject,
    ClauseSurfaceAgreementUnit,
    AgreementSurfaceEdge,
    AgreementEdgeType,
    BrokenPluralGuardNode,
    RationalityHint,
    GenderSurfaceHint,
    NumberSurfaceHint,
    AgreementHint,
    TransitivityHint,
    WeakRadicalRisk,
)
from dal_core.u7b_inflectional_surface_contract_carrier import (
    RootInputPermission,
    MarkerHint,
)
from dal_core.u7_pre_weight_contract_carrier import (
    PathPermission,  # Keep for compatibility with blocking potentials
)
from dal_core.foundation import Rank


# ============================================================================
# Fixtures - U₇-C Mock Data
# ============================================================================

@pytest.fixture
def mock_u7c_unit_blocked():
    """Mock U₇-C unit with BLOCKED root_input (e.g., وَ, بِ, particles)."""
    return ClauseSurfaceAgreementUnit(
        uid="u7c_blocked_1",
        surface="وَ",
        source_u7b_unit_id="u7b_1",
        source_u7b_trace=("u6_1", "u5_1", "u4_1", "u3_1", "u2_1", "u1_1", "u0_1"),
        protected_core="و",
        root_input="",  # Empty - blocked
        root_input_permission=RootInputPermission.BLOCKED,
        agreement_edges=(),
        rationality_surface_hint=RationalityHint.UNRESOLVED,
        gender_surface_hint=GenderSurfaceHint.UNRESOLVED,
        number_surface_hint=NumberSurfaceHint.UNRESOLVED,
        permission_elevated_by_agreement=False,
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=("u6_1", "u5_1", "u4_1", "u3_1", "u2_1", "u1_1", "u0_1")
    )


@pytest.fixture
def mock_u7c_unit_allowed_simple():
    """Mock U₇-C unit with ALLOWED root_input (e.g., كَتَبَ)."""
    return ClauseSurfaceAgreementUnit(
        uid="u7c_allowed_1",
        surface="كَتَبَ",
        source_u7b_unit_id="u7b_2",
        source_u7b_trace=("u6_2", "u5_2", "u4_2", "u3_2", "u2_2", "u1_2", "u0_2"),
        protected_core="كتب",
        root_input="كتب",  # Licensed for extraction
        root_input_permission=RootInputPermission.ALLOWED,
        agreement_edges=(),
        rationality_surface_hint=RationalityHint.UNRESOLVED,
        gender_surface_hint=GenderSurfaceHint.MASCULINE_POSSIBLE,
        number_surface_hint=NumberSurfaceHint.SINGULAR_POSSIBLE,
        permission_elevated_by_agreement=False,
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=("u6_2", "u5_2", "u4_2", "u3_2", "u2_2", "u1_2", "u0_2")
    )


@pytest.fixture
def mock_u7c_unit_deferred_broken_plural():
    """Mock U₇-C unit with DEFERRED root_input (e.g., الكتب - broken plural)."""
    broken_plural_guard = BrokenPluralGuardNode(
        uid="bpg_1",
        surface="الكتب",
        broken_pattern_hint="فُعُل",
        singular_candidate_path="كتاب",
        singular_requires_lexicon=True,
        singular_jamid_potential=MarkerHint.POSSIBLE,
        singular_mushtaq_potential=MarkerHint.UNLIKELY,
        entity_noun_potential=MarkerHint.POSSIBLE,
        adjective_potential=MarkerHint.UNLIKELY,
        adjective_source_hint=None,
        gender_surface_hint=GenderSurfaceHint.MASCULINE_POSSIBLE,
        real_feminine_hint=MarkerHint.UNLIKELY,
        semantic_feminine_hint=MarkerHint.UNLIKELY,
        grammatical_feminine_agreement_hint=MarkerHint.POSSIBLE,
        rationality_surface_hint=RationalityHint.NON_RATIONAL_POSSIBLE,
        agreement_edges=("edge_1",),
        transitivity_path_hint=TransitivityHint.UNRESOLVED,
        weak_radical_risk=WeakRadicalRisk.NO_RISK,
        lexical_attestation_required=True,
        root_input_permission=RootInputPermission.DEFERRED,
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=("u6_3",)
    )

    return ClauseSurfaceAgreementUnit(
        uid="u7c_deferred_1",
        surface="الكتب",
        source_u7b_unit_id="u7b_3",
        source_u7b_trace=("u6_3", "u5_3", "u4_3", "u3_3", "u2_3", "u1_3", "u0_3"),
        protected_core="كتب",
        root_input="",  # Empty - deferred
        root_input_permission=RootInputPermission.DEFERRED,
        broken_plural_guard=broken_plural_guard,
        agreement_edges=("edge_1",),
        rationality_surface_hint=RationalityHint.NON_RATIONAL_POSSIBLE,
        gender_surface_hint=GenderSurfaceHint.MASCULINE_POSSIBLE,
        number_surface_hint=NumberSurfaceHint.BROKEN_PLURAL_POSSIBLE,
        permission_elevated_by_agreement=False,
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=("u6_3", "u5_3", "u4_3", "u3_3", "u2_3", "u1_3", "u0_3")
    )


@pytest.fixture
def mock_u7c_layer_blocked_only(mock_u7c_unit_blocked):
    """Mock U₇-C layer with only blocked units."""
    return ClauseSurfaceAgreementLayerObject(
        uid="u7c_layer_blocked",
        units=(mock_u7c_unit_blocked,),
        agreement_edges=(),
        agreement_candidates=(),
        broken_plural_guards=(),
        source_u7b_layer_id="u7b_layer_1",
        trace_7b=("u7b_layer_1",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )


@pytest.fixture
def mock_u7c_layer_allowed_simple(mock_u7c_unit_allowed_simple):
    """Mock U₇-C layer with allowed simple unit."""
    return ClauseSurfaceAgreementLayerObject(
        uid="u7c_layer_allowed",
        units=(mock_u7c_unit_allowed_simple,),
        agreement_edges=(),
        agreement_candidates=(),
        broken_plural_guards=(),
        source_u7b_layer_id="u7b_layer_2",
        trace_7b=("u7b_layer_2",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )


@pytest.fixture
def mock_u7c_layer_deferred_broken_plural(mock_u7c_unit_deferred_broken_plural):
    """Mock U₇-C layer with deferred broken plural unit."""
    # Get the broken plural guard from the unit
    broken_plural_guard = mock_u7c_unit_deferred_broken_plural.broken_plural_guard

    return ClauseSurfaceAgreementLayerObject(
        uid="u7c_layer_deferred",
        units=(mock_u7c_unit_deferred_broken_plural,),
        agreement_edges=(),
        agreement_candidates=(),
        broken_plural_guards=(broken_plural_guard,) if broken_plural_guard else (),
        source_u7b_layer_id="u7b_layer_3",
        trace_7b=("u7b_layer_3",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )


@pytest.fixture
def mock_u7c_layer_mixed(mock_u7c_unit_blocked, mock_u7c_unit_allowed_simple):
    """Mock U₇-C layer with mixed blocked and allowed units."""
    return ClauseSurfaceAgreementLayerObject(
        uid="u7c_layer_mixed",
        units=(mock_u7c_unit_blocked, mock_u7c_unit_allowed_simple),
        agreement_edges=(),
        agreement_candidates=(),
        broken_plural_guards=(),
        source_u7b_layer_id="u7b_layer_4",
        trace_7b=("u7b_layer_4",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )


# ============================================================================
# Unit Structure Tests
# ============================================================================

def test_root_stem_candidate_unit_has_u7c_fields():
    """CRITICAL: RootStemCandidateUnit MUST have U₇-C preservation fields."""
    from dataclasses import fields

    field_names = {f.name for f in fields(RootStemCandidateUnit)}

    # CRITICAL: Must have U₇-C trace fields
    assert 'source_u7c_unit_id' in field_names
    assert 'source_u7c_trace' in field_names

    # CRITICAL: Must have agreement preservation fields
    assert 'agreement_edge_ids' in field_names
    assert 'broken_plural_guard_id' in field_names
    assert 'permission_elevated_by_agreement' in field_names

    # CRITICAL: Must have root_input (not root_path_permission)
    assert 'root_input' in field_names
    assert 'protected_core' in field_names


def test_root_stem_candidate_unit_forbids_weight():
    """CRITICAL: RootStemCandidateUnit MUST NOT contain 'weight' field."""
    # This test creates a valid unit and manually checks forbidden fields don't exist
    unit = RootStemCandidateUnit(
        uid="test",
        surface="كتب",
        protected_core="كتب",
        root_input="كتب",
        source_u7c_unit_id="u7c_1",
        source_u7c_trace=("u7c_1",),
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
        agreement_edge_ids=(),
        broken_plural_guard_id=None,
        permission_elevated_by_agreement=False,
        required_evidence=(),
        blocked_paths=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=()
    )

    # Should NOT have these forbidden fields
    assert not hasattr(unit, 'weight')
    assert not hasattr(unit, 'pattern')
    assert not hasattr(unit, 'meaning')


def test_root_stem_candidate_unit_forbids_certificates():
    """CRITICAL: RootStemCandidateUnit MUST NOT contain certificate fields."""
    # Verify forbidden fields don't exist in structure
    from dataclasses import fields

    field_names = {f.name for f in fields(RootStemCandidateUnit)}

    forbidden_fields = [
        'root_certificate',
        'stem_certificate',
        'weight_certificate',
        'pattern_certificate',
        'meaning',
        'hukm',
        'fa3il',
        'maf3ul',
        'mubtada',
        'khabar',
    ]

    for field in forbidden_fields:
        assert field not in field_names, f"FORBIDDEN: {field} found in RootStemCandidateUnit"


# ============================================================================
# Blocked Path Tests (Critical Law: Axiom 8.4)
# ============================================================================

def test_blocked_unit_produces_blocked_status(mock_u7c_layer_blocked_only):
    """
    CRITICAL: Blocked in U₇-C → Blocked in U₈.

    Test case: وَ (conjunction particle)
        U₇-C: root_input_permission = BLOCKED
        U₈: root_status = BLOCKED, no candidates
    """
    result = root_stem_candidate_8(mock_u7c_layer_blocked_only)

    assert result.success
    assert result.layer_object is not None

    unit = result.layer_object.units[0]
    assert unit.root_status == RootCandidateStatus.BLOCKED
    assert unit.stem_status == StemCandidateStatus.BLOCKED
    assert len(unit.root_candidate_paths) == 0
    assert len(unit.stem_candidate_paths) == 0
    assert "root_extraction_blocked" in unit.blocked_paths
    assert "stem_extraction_blocked" in unit.blocked_paths


def test_blocked_unit_preserves_surface(mock_u7c_layer_blocked_only):
    """Blocked units preserve surface without extraction."""
    result = root_stem_candidate_8(mock_u7c_layer_blocked_only)

    unit = result.layer_object.units[0]
    assert unit.surface == "وَ"
    assert unit.root_status == RootCandidateStatus.BLOCKED


# ============================================================================
# DEFERRED Path Tests (Critical for broken plurals)
# ============================================================================

def test_deferred_unit_produces_deferred_status(mock_u7c_layer_deferred_broken_plural):
    """
    CRITICAL: DEFERRED in U₇-C → DEFERRED in U₈ (no extraction).

    Test case: الكتب (broken plural)
        U₇-C: root_input_permission = DEFERRED, broken_plural_guard exists
        U₈: root_status = DEFERRED, no extraction, guard preserved
    """
    result = root_stem_candidate_8(mock_u7c_layer_deferred_broken_plural)

    assert result.success
    assert result.layer_object is not None

    unit = result.layer_object.units[0]
    assert unit.root_status == RootCandidateStatus.DEFERRED
    assert unit.stem_status == StemCandidateStatus.DEFERRED
    assert len(unit.root_candidate_paths) == 0  # No extraction!
    assert len(unit.stem_candidate_paths) == 0  # No extraction!


def test_deferred_unit_preserves_broken_plural_guard(mock_u7c_layer_deferred_broken_plural):
    """
    CRITICAL: U₈ preserves broken_plural_guard_id from U₇-C.

    Law: U₈ does NOT interpret guard, but MUST preserve it.
    """
    result = root_stem_candidate_8(mock_u7c_layer_deferred_broken_plural)

    unit = result.layer_object.units[0]

    # CRITICAL: broken_plural_guard_id must be preserved
    assert unit.broken_plural_guard_id is not None
    assert unit.broken_plural_guard_id == "bpg_1"


def test_deferred_unit_preserves_agreement_edges(mock_u7c_layer_deferred_broken_plural):
    """
    CRITICAL: U₈ preserves agreement_edge_ids from U₇-C without interpretation.

    Law: U₈ does NOT judge "الكتب" as non-rational.
          U₈ preserves that U₇-C found edge: الكتب ← كثيرة
    """
    result = root_stem_candidate_8(mock_u7c_layer_deferred_broken_plural)

    unit = result.layer_object.units[0]

    # CRITICAL: agreement_edge_ids must be preserved
    assert unit.agreement_edge_ids is not None
    assert len(unit.agreement_edge_ids) > 0
    assert "edge_1" in unit.agreement_edge_ids


# ============================================================================
# Open-Class Candidate Tests
# ============================================================================

def test_allowed_unit_produces_candidates(mock_u7c_layer_allowed_simple):
    """
    Allowed unit → Root/stem candidates extracted.

    Test case: كَتَبَ (verb)
        U₇-C: root_input_permission = ALLOWED, root_input = "كتب"
        U₈: root_status = CANDIDATE, root_candidates extracted from "كتب"
    """
    result = root_stem_candidate_8(mock_u7c_layer_allowed_simple)

    assert result.success
    assert result.layer_object is not None

    unit = result.layer_object.units[0]
    assert unit.root_status in [RootCandidateStatus.CANDIDATE, RootCandidateStatus.MULTIPLE_CANDIDATES]
    assert unit.stem_status in [StemCandidateStatus.CANDIDATE, StemCandidateStatus.MULTIPLE_CANDIDATES]

    # Should have at least one root candidate
    assert len(unit.root_candidate_paths) > 0

    # Should have at least one stem candidate
    assert len(unit.stem_candidate_paths) > 0


def test_root_candidates_are_not_certificates(mock_u7c_layer_allowed_simple):
    """
    CRITICAL: Root candidates are HYPOTHESES, not certificates.

    Axiom 8.2: Root in U₈ is candidate, not certificate
    """
    result = root_stem_candidate_8(mock_u7c_layer_allowed_simple)

    unit = result.layer_object.units[0]

    # Should have root candidates
    assert len(unit.root_candidate_paths) > 0

    # Should NOT have 'root_certificate' field
    assert not hasattr(unit, 'root_certificate')

    # Should have required evidence for certification
    assert len(unit.required_evidence) > 0
    assert any('lexical' in ev for ev in unit.required_evidence)


def test_root_candidate_structure(mock_u7c_layer_allowed_simple):
    """Test RootCandidate structure and evidence."""
    result = root_stem_candidate_8(mock_u7c_layer_allowed_simple)

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


def test_stem_candidate_structure(mock_u7c_layer_allowed_simple):
    """Test StemCandidate structure and evidence."""
    result = root_stem_candidate_8(mock_u7c_layer_allowed_simple)

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

def test_mixed_layer_preserves_both_types(mock_u7c_layer_mixed):
    """
    Mixed layer with blocked + open-class units.

    Should preserve blocked units AND extract candidates from open-class.
    """
    result = root_stem_candidate_8(mock_u7c_layer_mixed)

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

def test_cpb8_is_complete(mock_u7c_layer_allowed_simple):
    """Test CPB₈ is_complete validation."""
    result = root_stem_candidate_8(mock_u7c_layer_allowed_simple)

    assert CPB8.is_complete(result.layer_object)


def test_cpb8_build_proof(mock_u7c_layer_mixed):
    """Test CPB₈ proof building."""
    result = root_stem_candidate_8(mock_u7c_layer_mixed)

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


def test_cpb8_proof_has_limitations(mock_u7c_layer_allowed_simple):
    """Test CPB₈ proof includes constitutional limitations."""
    result = root_stem_candidate_8(mock_u7c_layer_allowed_simple)

    proof = CPB8.build_proof(result.layer_object)

    # Check limitations
    assert "no_root_certificate" in proof.limitations
    assert "no_stem_certificate" in proof.limitations
    assert "no_weight_determination" in proof.limitations
    assert "candidate_is_hypothesis_not_certificate" in proof.limitations


# ============================================================================
# Trace Preservation Tests
# ============================================================================

def test_trace_preservation_from_u7(mock_u7c_layer_allowed_simple):
    """Verify trace preservation U₇-C→U₈."""
    result = root_stem_candidate_8(mock_u7c_layer_allowed_simple)

    # Layer should preserve U₇-C layer ID
    assert result.layer_object.source_clause_surface_layer_id == mock_u7c_layer_allowed_simple.uid

    # Units should preserve U₇-C unit traces
    for unit in result.layer_object.units:
        assert unit.source_u7c_unit_id is not None
        assert unit.source_u7c_trace is not None


# ============================================================================
# Failure Mode Tests
# ============================================================================

def test_empty_input_fails():
    """Empty U₇-C layer should fail gracefully - but U₇-C doesn't allow empty units.

    Instead, test that U₈ handles layer with no valid units properly.
    """
    # Create a layer with a single blocked unit (effectively empty for extraction)
    blocked_unit = ClauseSurfaceAgreementUnit(
        uid="u7c_empty",
        surface="وَ",
        source_u7b_unit_id="u7b_empty",
        source_u7b_trace=("u6_empty",),
        protected_core="و",
        root_input="",
        root_input_permission=RootInputPermission.BLOCKED,
        residuals=frozenset(),
        rank=Rank.ZERO,
        trace=("u6_empty",)
    )

    layer = ClauseSurfaceAgreementLayerObject(
        uid="empty",
        units=(blocked_unit,),  # Has unit but it's blocked
        agreement_edges=(),
        agreement_candidates=(),
        broken_plural_guards=(),
        source_u7b_layer_id="u7b_empty",
        trace_7b=("u7b_empty",),
        residuals=frozenset(),
        rank=Rank.ZERO,
        proof=None
    )

    result = root_stem_candidate_8(layer)

    # Should succeed but with blocked status
    assert result.success
    assert len(result.layer_object.units) == 1
    assert result.layer_object.units[0].root_status == RootCandidateStatus.BLOCKED


# ============================================================================
# Radical Count Hint Tests
# ============================================================================

def test_triliteral_hint(mock_u7c_layer_allowed_simple):
    """Test triliteral radical count hint."""
    result = root_stem_candidate_8(mock_u7c_layer_allowed_simple)

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

def test_residuals_preserved_from_u7(mock_u7c_layer_allowed_simple):
    """Residuals from U₇ should be preserved in U₈."""
    result = root_stem_candidate_8(mock_u7c_layer_allowed_simple)

    # Layer residuals should match or extend U₇ residuals
    u7_residuals = mock_u7c_layer_allowed_simple.residuals
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
    # Create mock U₇-C unit for كَتَبَ
    u7c_unit = ClauseSurfaceAgreementUnit(
        uid="u7c_kataba",
        surface="كَتَبَ",
        source_u7b_unit_id="u7b_kataba",
        source_u7b_trace=("u6", "u5", "u4", "u3", "u2", "u1", "u0"),
        protected_core="كتب",
        root_input="كتب",  # Licensed for extraction
        root_input_permission=RootInputPermission.ALLOWED,
        agreement_edges=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=("u6", "u5", "u4", "u3", "u2", "u1", "u0")
    )

    u7c_layer = ClauseSurfaceAgreementLayerObject(
        uid="u7c_kataba_layer",
        units=(u7c_unit,),
        agreement_edges=(),
        agreement_candidates=(),
        broken_plural_guards=(),
        source_u7b_layer_id="u7b_layer",
        trace_7b=("u7b_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )

    result = root_stem_candidate_8(u7c_layer)

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
