"""
Constitutional Tests for RelationCandidate Boundary Types

PR #140: Tests proving constitutional guards are enforced.

These tests verify:
    1. Validation uses ValueError, not assert
    2. Required fields are enforced
    3. No relation exposes forbidden methods
    4. Single relations cannot close ifadah
    5. RelationNetworkCandidate is carrier only
"""

import pytest

from dal_core.relation_candidates import (
    RelationType,
    InclusionType,
    RestrictionType,
    ReferenceType,
    RelationCandidate,
    PredicativeRelationCandidate,
    InclusionRelationCandidate,
    RestrictiveRelationCandidate,
    ReferenceRelationCandidate,
    RelationNetworkCandidate,
)
from dal_core.foundation import Rank, ResidualSet


# ============================================================================
# Test Helpers
# ============================================================================

def make_valid_relation_candidate():
    """Create a valid base RelationCandidate for testing."""
    return RelationCandidate(
        anchor_id="anchor_1",
        related_id="related_1",
        relation_type=RelationType.PREDICATIVE,
        trace=("step1", "step2"),
        residuals=ResidualSet(residuals=frozenset()),
        rank=Rank.HYPOTHESIS,
    )


def make_valid_predicative_relation():
    """Create a valid PredicativeRelationCandidate for testing."""
    return PredicativeRelationCandidate(
        anchor_id="زيد",
        related_id="قائم",
        relation_type=RelationType.PREDICATIVE,
        predicate_id="قائم",
        trace=("detect_anchor", "detect_predicate", "build_edge"),
        residuals=ResidualSet(residuals=frozenset()),
        rank=Rank.STRONG_HYPOTHESIS,
    )


def make_valid_inclusion_relation():
    """Create a valid InclusionRelationCandidate for testing."""
    return InclusionRelationCandidate(
        anchor_id="الإنسان",
        related_id="حيوان",
        relation_type=RelationType.INCLUSION,
        container_id="حيوان",
        inclusion_type=InclusionType.GENUS_SPECIES,
        trace=("detect_species", "detect_genus", "build_edge"),
        residuals=ResidualSet(residuals=frozenset()),
        rank=Rank.STRONG_HYPOTHESIS,
    )


def make_valid_restrictive_relation():
    """Create a valid RestrictiveRelationCandidate for testing."""
    return RestrictiveRelationCandidate(
        anchor_id="رجل",
        related_id="كريم",
        relation_type=RelationType.RESTRICTIVE,
        base_id="رجل",
        restrictor_id="كريم",
        restriction_type=RestrictionType.ATTRIBUTIVE,
        trace=("detect_base", "detect_restrictor", "build_edge"),
        residuals=ResidualSet(residuals=frozenset()),
        rank=Rank.HYPOTHESIS,
    )


def make_valid_reference_relation():
    """Create a valid ReferenceRelationCandidate for testing."""
    return ReferenceRelationCandidate(
        anchor_id="هذا",
        related_id="رجل",
        relation_type=RelationType.REFERENCE,
        referent_id="رجل",
        reference_type=ReferenceType.DEMONSTRATIVE,
        trace=("detect_demonstrative", "detect_referent", "build_edge"),
        residuals=ResidualSet(residuals=frozenset()),
        rank=Rank.HYPOTHESIS,
    )


# ============================================================================
# Validation Tests (ValueError, not assert)
# ============================================================================

def test_relation_candidate_missing_anchor_id_fails():
    """RelationCandidate MUST require anchor_id."""
    with pytest.raises(ValueError, match="requires non-empty anchor_id"):
        RelationCandidate(
            anchor_id="",  # Empty anchor_id
            related_id="related_1",
            relation_type=RelationType.PREDICATIVE,
            trace=("step1",),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
        )


def test_relation_candidate_missing_related_id_fails():
    """RelationCandidate MUST require related_id."""
    with pytest.raises(ValueError, match="requires non-empty related_id"):
        RelationCandidate(
            anchor_id="anchor_1",
            related_id="",  # Empty related_id
            relation_type=RelationType.PREDICATIVE,
            trace=("step1",),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
        )


def test_relation_candidate_missing_trace_fails():
    """RelationCandidate MUST require trace."""
    with pytest.raises(ValueError, match="requires non-empty trace"):
        RelationCandidate(
            anchor_id="anchor_1",
            related_id="related_1",
            relation_type=RelationType.PREDICATIVE,
            trace=(),  # Empty trace
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CANDIDATE,
        )


def test_relation_candidate_requires_residual_audit():
    """RelationCandidate MUST carry residuals (even if empty)."""
    # This should succeed - empty residuals are allowed, but ResidualSet is required
    rel = RelationCandidate(
        anchor_id="anchor_1",
        related_id="related_1",
        relation_type=RelationType.PREDICATIVE,
        trace=("step1",),
        residuals=ResidualSet(residuals=frozenset()),  # Empty but present
        rank=Rank.CANDIDATE,
    )
    assert isinstance(rel.residuals, ResidualSet)


def test_relation_candidate_requires_rank():
    """RelationCandidate MUST have rank."""
    with pytest.raises(TypeError):
        RelationCandidate(
            anchor_id="anchor_1",
            related_id="related_1",
            relation_type=RelationType.PREDICATIVE,
            trace=("step1",),
            residuals=ResidualSet(residuals=frozenset()),
            rank=None,  # Invalid: None
        )


def test_relation_candidate_requires_declared_relation_type():
    """RelationCandidate MUST declare relation_type."""
    rel = make_valid_predicative_relation()
    assert rel.relation_type == RelationType.PREDICATIVE
    assert isinstance(rel.relation_type, RelationType)


def test_relation_cannot_be_certificate_rank():
    """
    Constitutional guard: RelationCandidate MUST NOT have CERTIFICATE rank.

    Relations are hypotheses, not certificates.
    """
    with pytest.raises(ValueError, match="cannot have CERTIFICATE rank"):
        RelationCandidate(
            anchor_id="anchor_1",
            related_id="related_1",
            relation_type=RelationType.PREDICATIVE,
            trace=("step1",),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.CERTIFICATE,  # FORBIDDEN
        )


# ============================================================================
# Specific Relation Type Tests
# ============================================================================

def test_predicative_relation_requires_predicative_type():
    """PredicativeRelationCandidate MUST have relation_type=PREDICATIVE."""
    with pytest.raises(ValueError, match="requires relation_type=PREDICATIVE"):
        PredicativeRelationCandidate(
            anchor_id="زيد",
            related_id="قائم",
            relation_type=RelationType.INCLUSION,  # Wrong type
            predicate_id="قائم",
            trace=("step1",),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.HYPOTHESIS,
        )


def test_predicative_relation_requires_predicate_id():
    """PredicativeRelationCandidate MUST have predicate_id."""
    with pytest.raises(ValueError, match="requires non-empty predicate_id"):
        PredicativeRelationCandidate(
            anchor_id="زيد",
            related_id="قائم",
            relation_type=RelationType.PREDICATIVE,
            predicate_id="",  # Empty
            trace=("step1",),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.HYPOTHESIS,
        )


def test_inclusion_relation_requires_inclusion_type():
    """InclusionRelationCandidate MUST have relation_type=INCLUSION."""
    with pytest.raises(ValueError, match="requires relation_type=INCLUSION"):
        InclusionRelationCandidate(
            anchor_id="الإنسان",
            related_id="حيوان",
            relation_type=RelationType.PREDICATIVE,  # Wrong type
            container_id="حيوان",
            inclusion_type=InclusionType.GENUS_SPECIES,
            trace=("step1",),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.HYPOTHESIS,
        )


def test_restrictive_relation_requires_restrictive_type():
    """RestrictiveRelationCandidate MUST have relation_type=RESTRICTIVE."""
    with pytest.raises(ValueError, match="requires relation_type=RESTRICTIVE"):
        RestrictiveRelationCandidate(
            anchor_id="رجل",
            related_id="كريم",
            relation_type=RelationType.PREDICATIVE,  # Wrong type
            base_id="رجل",
            restrictor_id="كريم",
            restriction_type=RestrictionType.ATTRIBUTIVE,
            trace=("step1",),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.HYPOTHESIS,
        )


def test_reference_relation_requires_reference_type():
    """ReferenceRelationCandidate MUST have relation_type=REFERENCE."""
    with pytest.raises(ValueError, match="requires relation_type=REFERENCE"):
        ReferenceRelationCandidate(
            anchor_id="هذا",
            related_id="رجل",
            relation_type=RelationType.PREDICATIVE,  # Wrong type
            referent_id="رجل",
            reference_type=ReferenceType.DEMONSTRATIVE,
            trace=("step1",),
            residuals=ResidualSet(residuals=frozenset()),
            rank=Rank.HYPOTHESIS,
        )


# ============================================================================
# No-Leap Constitutional Guards
# ============================================================================

def test_relation_candidate_cannot_claim_hukm():
    """RelationCandidate MUST NOT expose hukm methods."""
    rel = make_valid_predicative_relation()

    # Verify forbidden methods do NOT exist
    assert not hasattr(rel, 'to_hukm')
    assert not hasattr(rel, 'emit_hukm')
    assert not hasattr(rel, 'produce_hukm')

    # Verify forbidden_outputs metadata
    assert 'hukm' in rel.forbidden_outputs


def test_relation_candidate_cannot_claim_reality():
    """RelationCandidate MUST NOT expose reality methods."""
    rel = make_valid_predicative_relation()

    # Verify forbidden methods do NOT exist
    assert not hasattr(rel, 'to_reality')
    assert not hasattr(rel, 'emit_reality')
    assert not hasattr(rel, 'produce_reality')

    # Verify forbidden_outputs metadata
    assert 'reality' in rel.forbidden_outputs


def test_relation_candidate_cannot_claim_final_meaning():
    """RelationCandidate MUST NOT expose final meaning methods."""
    rel = make_valid_predicative_relation()

    # Verify forbidden methods do NOT exist
    assert not hasattr(rel, 'to_final_meaning')
    assert not hasattr(rel, 'to_meaning')
    assert not hasattr(rel, 'emit_meaning')

    # Verify forbidden_outputs metadata
    assert 'meaning' in rel.forbidden_outputs


def test_relation_candidate_cannot_claim_ifadah():
    """RelationCandidate MUST NOT expose ifadah methods."""
    rel = make_valid_predicative_relation()

    # Verify forbidden methods do NOT exist
    assert not hasattr(rel, 'to_ifadah')
    assert not hasattr(rel, 'close_ifadah')
    assert not hasattr(rel, 'emit_ifadah')

    # Verify forbidden_outputs metadata
    assert 'ifadah' in rel.forbidden_outputs


def test_predicative_relation_does_not_close_ifadah_alone():
    """
    CRITICAL: Single PredicativeRelationCandidate CANNOT close ifadah.

    Constitutional Law:
        PredicativeRelationCandidate alone ≠ Ifadah_Dal
    """
    rel = make_valid_predicative_relation()

    # Verify no ifadah methods exist
    assert not hasattr(rel, 'to_ifadah')
    assert not hasattr(rel, 'close_ifadah')

    # This is a BOUNDARY TYPE, not a closure engine
    assert isinstance(rel, PredicativeRelationCandidate)
    assert 'ifadah' in rel.forbidden_outputs


def test_inclusion_relation_does_not_close_ifadah_alone():
    """Single InclusionRelationCandidate CANNOT close ifadah."""
    rel = make_valid_inclusion_relation()

    assert not hasattr(rel, 'to_ifadah')
    assert not hasattr(rel, 'close_ifadah')
    assert 'ifadah' in rel.forbidden_outputs


def test_restrictive_relation_does_not_close_ifadah_alone():
    """Single RestrictiveRelationCandidate CANNOT close ifadah."""
    rel = make_valid_restrictive_relation()

    assert not hasattr(rel, 'to_ifadah')
    assert not hasattr(rel, 'close_ifadah')
    assert 'ifadah' in rel.forbidden_outputs


def test_reference_relation_does_not_close_ifadah_alone():
    """Single ReferenceRelationCandidate CANNOT close ifadah."""
    rel = make_valid_reference_relation()

    assert not hasattr(rel, 'to_ifadah')
    assert not hasattr(rel, 'close_ifadah')
    assert 'ifadah' in rel.forbidden_outputs


# ============================================================================
# RelationNetworkCandidate Tests
# ============================================================================

def test_relation_network_required_before_ifadah_dal():
    """
    CRITICAL: Single relation ≠ Ifadah_Dal.

    Must build RelationNetworkCandidate first.

    Pipeline:
        RelationCandidate → RelationNetworkCandidate → [future: Ifadah_Dal]
    """
    pred_rel = make_valid_predicative_relation()

    # Single relation cannot close ifadah
    assert not hasattr(pred_rel, 'to_ifadah')

    # Must create network
    network = RelationNetworkCandidate(
        relations=(pred_rel,),
        network_rank=Rank.HYPOTHESIS,
        closure_residuals=ResidualSet(residuals=frozenset()),
        closure_eligible=False,  # Not eligible yet
    )

    # Network is a CARRIER, not closure engine
    assert isinstance(network, RelationNetworkCandidate)
    assert len(network.relations) == 1
    assert network.relations[0] == pred_rel


def test_relation_network_is_carrier_not_closure_engine():
    """
    Constitutional Law:
        RelationNetworkCandidate is a CARRIER, NOT a closure engine.

    It holds relations but does NOT close ifadah itself.
    Future closure via RelationClosureGate.
    """
    pred_rel = make_valid_predicative_relation()
    ref_rel = make_valid_reference_relation()

    network = RelationNetworkCandidate(
        relations=(pred_rel, ref_rel),
        network_rank=Rank.HYPOTHESIS,
        closure_residuals=ResidualSet(residuals=frozenset()),
        closure_eligible=True,  # May be eligible, but doesn't close itself
    )

    # Verify it's a carrier
    assert isinstance(network, RelationNetworkCandidate)
    assert len(network.relations) == 2

    # Verify it does NOT expose closure methods (PR #140)
    assert not hasattr(network, 'close_ifadah')
    assert not hasattr(network, 'to_ifadah')
    assert not hasattr(network, 'emit_ifadah')

    # closure_eligible is metadata, not a method
    assert isinstance(network.closure_eligible, bool)


def test_relation_network_requires_non_empty_relations():
    """RelationNetworkCandidate MUST have at least one relation."""
    with pytest.raises(ValueError, match="requires non-empty relations"):
        RelationNetworkCandidate(
            relations=(),  # Empty
            network_rank=Rank.HYPOTHESIS,
            closure_residuals=ResidualSet(residuals=frozenset()),
        )


def test_relation_network_requires_relation_candidate_instances():
    """RelationNetworkCandidate MUST contain RelationCandidate instances."""
    with pytest.raises(TypeError, match="must be RelationCandidate"):
        RelationNetworkCandidate(
            relations=("not_a_relation",),  # Invalid type
            network_rank=Rank.HYPOTHESIS,
            closure_residuals=ResidualSet(residuals=frozenset()),
        )


# ============================================================================
# All Four Relation Types Instantiate Correctly
# ============================================================================

def test_predicative_relation_candidate_instantiates():
    """PredicativeRelationCandidate instantiates correctly."""
    rel = make_valid_predicative_relation()

    assert isinstance(rel, PredicativeRelationCandidate)
    assert isinstance(rel, RelationCandidate)
    assert rel.relation_type == RelationType.PREDICATIVE
    assert rel.anchor_id == "زيد"
    assert rel.predicate_id == "قائم"


def test_inclusion_relation_candidate_instantiates():
    """InclusionRelationCandidate instantiates correctly."""
    rel = make_valid_inclusion_relation()

    assert isinstance(rel, InclusionRelationCandidate)
    assert isinstance(rel, RelationCandidate)
    assert rel.relation_type == RelationType.INCLUSION
    assert rel.container_id == "حيوان"
    assert rel.inclusion_type == InclusionType.GENUS_SPECIES


def test_restrictive_relation_candidate_instantiates():
    """RestrictiveRelationCandidate instantiates correctly."""
    rel = make_valid_restrictive_relation()

    assert isinstance(rel, RestrictiveRelationCandidate)
    assert isinstance(rel, RelationCandidate)
    assert rel.relation_type == RelationType.RESTRICTIVE
    assert rel.base_id == "رجل"
    assert rel.restrictor_id == "كريم"
    assert rel.restriction_type == RestrictionType.ATTRIBUTIVE


def test_reference_relation_candidate_instantiates():
    """ReferenceRelationCandidate instantiates correctly."""
    rel = make_valid_reference_relation()

    assert isinstance(rel, ReferenceRelationCandidate)
    assert isinstance(rel, RelationCandidate)
    assert rel.relation_type == RelationType.REFERENCE
    assert rel.referent_id == "رجل"
    assert rel.reference_type == ReferenceType.DEMONSTRATIVE


# ============================================================================
# Immutability Tests
# ============================================================================

def test_relation_candidate_is_immutable():
    """RelationCandidate is frozen/immutable."""
    rel = make_valid_predicative_relation()

    with pytest.raises(Exception):  # FrozenInstanceError or similar
        rel.anchor_id = "different"


def test_relation_network_is_immutable():
    """RelationNetworkCandidate is frozen/immutable."""
    network = RelationNetworkCandidate(
        relations=(make_valid_predicative_relation(),),
        network_rank=Rank.HYPOTHESIS,
        closure_residuals=ResidualSet(residuals=frozenset()),
    )

    with pytest.raises(Exception):  # FrozenInstanceError or similar
        network.network_rank = Rank.STRONG_HYPOTHESIS
