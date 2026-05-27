"""
Tests for U₇-C Clause Surface Agreement Contract Carrier

Purpose: Verify clause-level agreement protection before U₈ root extraction

Critical Laws Being Tested:
    - Axiom 7C.1: العلامة لا تُفهم إلا في تعاقد (Marker understood only in contract)
    - Axiom 7C.2: التعاقد ≠ الإعراب (Agreement ≠ i'rab judgment)
    - Axiom 7C.3: التعاقد ≠ الوظيفة (Agreement ≠ function assignment)
    - Axiom 7C.6: جمع التكسير يحتاج عقدًا متعدد الأبعاد (Broken plural needs multi-dimensional contract)
"""

import pytest
from uuid import uuid4

from dal_core.foundation import Rank, make_proof_object
from dal_core.residuals import make_warning, make_blocker
from dal_core.u7b_inflectional_surface_contract_carrier import (
    InflectionalSurfaceContractUnit,
    InflectionalSurfaceContractLayerObject,
    MarkerHint,
    RootInputPermission,
)
from dal_core.u7c_clause_surface_agreement_carrier import (
    ClauseSurfaceAgreementUnit,
    ClauseSurfaceAgreementLayerObject,
    BrokenPluralGuardNode,
    AgreementSurfaceEdge,
    AgreementSurfaceCandidate,
    AgreementHint,
    AgreementEdgeType,
    RationalityHint,
    GenderSurfaceHint,
    NumberSurfaceHint,
    TransitivitySurfacePotential,
    WeakRadicalRiskVector,
    WeakRadicalRisk,
    TransitivityHint,
    transition_u7b_to_u7c,
)


# ============================================================================
# Test 1: Basic U₇-C Unit Creation
# ============================================================================

def test_u7c_unit_basic_creation():
    """Test basic creation of U₇-C clause surface agreement unit."""
    unit = ClauseSurfaceAgreementUnit(
        uid=str(uuid4()),
        surface="كِتَابٌ",
        source_u7b_unit_id="u7b_123",
        source_u7b_trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b"),
        protected_core="كتاب",
        root_input="كتاب",
        root_input_permission=RootInputPermission.ALLOWED,
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c"),
    )

    assert unit.surface == "كِتَابٌ"
    assert unit.protected_core == "كتاب"
    assert unit.root_input == "كتاب"
    assert unit.root_input_permission == RootInputPermission.ALLOWED
    assert unit.rationality_surface_hint == RationalityHint.UNRESOLVED
    assert unit.gender_surface_hint == GenderSurfaceHint.UNRESOLVED


# ============================================================================
# Test 2: Forbidden Fields Validation
# ============================================================================

def test_u7c_unit_forbidden_fields():
    """Test that U₇-C unit rejects forbidden fields (constitutional check)."""

    # These fields MUST NOT exist in U₇-C unit
    forbidden_attempts = [
        {'root': 'كتب'},
        {'stem': 'كتاب'},
        {'weight': 'فعال'},
        {'pattern': 'فعال'},
        {'meaning': 'book'},
        {'hukm': 'mubtada'},
        {'fa3il': 'something'},
        {'maf3ul': 'something'},
        {'mubtada': 'something'},
        {'khabar': 'something'},
        {'final_irab': 'nominative'},
    ]

    for forbidden_field_dict in forbidden_attempts:
        # Python's dataclass doesn't allow adding arbitrary fields,
        # but we test the __post_init__ validation logic
        # by verifying it's not settable via normal means
        unit = ClauseSurfaceAgreementUnit(
            uid=str(uuid4()),
            surface="كِتَابٌ",
            source_u7b_unit_id="u7b_123",
            source_u7b_trace=("u7b",),
            protected_core="كتاب",
            root_input="كتاب",
            root_input_permission=RootInputPermission.ALLOWED,
        )

        # Verify forbidden fields don't exist
        for forbidden_field in forbidden_field_dict.keys():
            assert not hasattr(unit, forbidden_field), \
                f"U₇-C unit MUST NOT have '{forbidden_field}' field (Axiom 7C violation)"


# ============================================================================
# Test 3: BrokenPluralGuardNode Multi-Dimensional Structure
# ============================================================================

def test_broken_plural_guard_node_comprehensive():
    """Test BrokenPluralGuardNode contains all required dimensions."""
    guard = BrokenPluralGuardNode(
        uid=str(uuid4()),
        surface="رجال",
        broken_pattern_hint="فِعَال",
        singular_candidate_path="رجل",
        singular_requires_lexicon=True,
        singular_jamid_potential=MarkerHint.POSSIBLE,
        singular_mushtaq_potential=MarkerHint.UNLIKELY,
        entity_noun_potential=MarkerHint.POSSIBLE,
        adjective_potential=MarkerHint.UNLIKELY,
        adjective_source_hint=None,
        gender_surface_hint=GenderSurfaceHint.MASCULINE_POSSIBLE,
        real_feminine_hint=MarkerHint.UNLIKELY,
        semantic_feminine_hint=MarkerHint.UNLIKELY,
        grammatical_feminine_agreement_hint=MarkerHint.UNRESOLVED,
        rationality_surface_hint=RationalityHint.HUMAN_POSSIBLE,
        agreement_edges=(),
        transitivity_path_hint=TransitivityHint.UNRESOLVED,
        weak_radical_risk=WeakRadicalRisk.NO_RISK,
        lexical_attestation_required=True,
        root_input_permission=RootInputPermission.DEFERRED,
        residuals=frozenset([make_warning("singular_not_certified")]),
        rank=Rank.CANDIDATE,
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c"),
    )

    # Verify all 10+ dimensions present
    assert guard.surface == "رجال"
    assert guard.broken_pattern_hint == "فِعَال"
    assert guard.singular_candidate_path == "رجل"
    assert guard.singular_requires_lexicon is True
    assert guard.rationality_surface_hint == RationalityHint.HUMAN_POSSIBLE
    assert guard.gender_surface_hint == GenderSurfaceHint.MASCULINE_POSSIBLE
    assert guard.entity_noun_potential == MarkerHint.POSSIBLE
    assert guard.root_input_permission == RootInputPermission.DEFERRED
    assert guard.lexical_attestation_required is True


def test_broken_plural_guard_node_ambiguous():
    """Test BrokenPluralGuardNode for ambiguous broken plural (كتب)."""
    guard = BrokenPluralGuardNode(
        uid=str(uuid4()),
        surface="كتب",
        broken_pattern_hint="فُعُل",  # Could be كُتُب
        singular_candidate_path="كتاب",  # Possible singular
        singular_requires_lexicon=True,
        singular_jamid_potential=MarkerHint.UNLIKELY,
        singular_mushtaq_potential=MarkerHint.POSSIBLE,
        entity_noun_potential=MarkerHint.POSSIBLE,
        adjective_potential=MarkerHint.UNLIKELY,
        adjective_source_hint=None,
        gender_surface_hint=GenderSurfaceHint.MASCULINE_POSSIBLE,
        real_feminine_hint=MarkerHint.UNLIKELY,
        semantic_feminine_hint=MarkerHint.UNLIKELY,
        grammatical_feminine_agreement_hint=MarkerHint.UNRESOLVED,
        rationality_surface_hint=RationalityHint.NON_RATIONAL_POSSIBLE,
        agreement_edges=(),
        transitivity_path_hint=TransitivityHint.UNRESOLVED,
        weak_radical_risk=WeakRadicalRisk.UNRESOLVED,
        lexical_attestation_required=True,
        root_input_permission=RootInputPermission.DEFERRED,
        residuals=frozenset([
            make_warning("plural_or_verb_ambiguity"),
            make_warning("singular_not_certified")
        ]),
        rank=Rank.CANDIDATE,
        trace=("u7c",),
    )

    assert guard.surface == "كتب"
    assert guard.root_input_permission == RootInputPermission.DEFERRED
    assert len(guard.residuals) == 2


# ============================================================================
# Test 4: AgreementSurfaceEdge Structure
# ============================================================================

def test_agreement_surface_edge_noun_adjective():
    """Test noun-adjective agreement surface edge."""
    edge = AgreementSurfaceEdge(
        uid=str(uuid4()),
        edge_type=AgreementEdgeType.NOUN_ADJECTIVE,
        source_unit_id="unit_noun_123",
        target_unit_id="unit_adj_456",
        number_agreement_hint=AgreementHint.POSSIBLE,
        gender_agreement_hint=AgreementHint.POSSIBLE,
        rationality_agreement_hint=AgreementHint.UNRESOLVED,
        broken_plural_feminine_singular_hint=MarkerHint.UNLIKELY,
        non_rational_plural_feminine_agreement_hint=MarkerHint.UNLIKELY,
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
    )

    assert edge.edge_type == AgreementEdgeType.NOUN_ADJECTIVE
    assert edge.number_agreement_hint == AgreementHint.POSSIBLE
    assert edge.gender_agreement_hint == AgreementHint.POSSIBLE


def test_agreement_surface_edge_broken_plural_feminine():
    """Test broken plural with feminine singular agreement edge: الكتب كثيرة"""
    edge = AgreementSurfaceEdge(
        uid=str(uuid4()),
        edge_type=AgreementEdgeType.BROKEN_PLURAL_ADJECTIVE,
        source_unit_id="unit_kutub_123",  # الكتب
        target_unit_id="unit_kathira_456",  # كثيرة
        number_agreement_hint=AgreementHint.POSSIBLE,
        gender_agreement_hint=AgreementHint.POSSIBLE,
        rationality_agreement_hint=AgreementHint.POSSIBLE,
        broken_plural_feminine_singular_hint=MarkerHint.POSSIBLE,
        non_rational_plural_feminine_agreement_hint=MarkerHint.POSSIBLE,
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
    )

    assert edge.edge_type == AgreementEdgeType.BROKEN_PLURAL_ADJECTIVE
    assert edge.broken_plural_feminine_singular_hint == MarkerHint.POSSIBLE
    assert edge.non_rational_plural_feminine_agreement_hint == MarkerHint.POSSIBLE


# ============================================================================
# Test 5: TransitivitySurfacePotential
# ============================================================================

def test_transitivity_surface_potential_transitive():
    """Test transitivity surface potential for transitive verb: نعبد"""
    transitivity = TransitivitySurfacePotential(
        uid=str(uuid4()),
        surface_word="نعبد",
        intransitive_path_hint=MarkerHint.UNLIKELY,
        transitive_one_object_hint=MarkerHint.POSSIBLE,
        transitive_two_objects_hint=MarkerHint.UNLIKELY,
        prepositional_object_hint=MarkerHint.UNLIKELY,
        passive_blocks_agent_hint=MarkerHint.UNLIKELY,
        residuals=frozenset(),
    )

    assert transitivity.surface_word == "نعبد"
    assert transitivity.transitive_one_object_hint == MarkerHint.POSSIBLE
    assert transitivity.intransitive_path_hint == MarkerHint.UNLIKELY


def test_transitivity_surface_potential_prepositional():
    """Test transitivity surface potential for prepositional verb: نستعين"""
    transitivity = TransitivitySurfacePotential(
        uid=str(uuid4()),
        surface_word="نستعين",
        intransitive_path_hint=MarkerHint.UNLIKELY,
        transitive_one_object_hint=MarkerHint.UNLIKELY,
        transitive_two_objects_hint=MarkerHint.UNLIKELY,
        prepositional_object_hint=MarkerHint.POSSIBLE,
        passive_blocks_agent_hint=MarkerHint.UNLIKELY,
        residuals=frozenset(),
    )

    assert transitivity.prepositional_object_hint == MarkerHint.POSSIBLE


# ============================================================================
# Test 6: WeakRadicalRiskVector
# ============================================================================

def test_weak_radical_risk_medial():
    """Test weak radical risk for medial weak verb: قال"""
    risk_vector = WeakRadicalRiskVector(
        uid=str(uuid4()),
        surface_word="قال",
        initial_weak_risk=MarkerHint.UNLIKELY,
        medial_weak_risk=MarkerHint.POSSIBLE,
        final_weak_risk=MarkerHint.UNLIKELY,
        hamzated_risk=MarkerHint.UNLIKELY,
        doubled_risk=MarkerHint.UNLIKELY,
        hollow_surface_risk=MarkerHint.POSSIBLE,
        defective_surface_risk=MarkerHint.UNLIKELY,
        residuals=frozenset(),
    )

    assert risk_vector.surface_word == "قال"
    assert risk_vector.medial_weak_risk == MarkerHint.POSSIBLE
    assert risk_vector.hollow_surface_risk == MarkerHint.POSSIBLE


def test_weak_radical_risk_final():
    """Test weak radical risk for final weak verb: سعى"""
    risk_vector = WeakRadicalRiskVector(
        uid=str(uuid4()),
        surface_word="سعى",
        initial_weak_risk=MarkerHint.UNLIKELY,
        medial_weak_risk=MarkerHint.UNLIKELY,
        final_weak_risk=MarkerHint.POSSIBLE,
        hamzated_risk=MarkerHint.UNLIKELY,
        doubled_risk=MarkerHint.UNLIKELY,
        hollow_surface_risk=MarkerHint.UNLIKELY,
        defective_surface_risk=MarkerHint.POSSIBLE,
        residuals=frozenset(),
    )

    assert risk_vector.final_weak_risk == MarkerHint.POSSIBLE
    assert risk_vector.defective_surface_risk == MarkerHint.POSSIBLE


# ============================================================================
# Test 7: U₇-B to U₇-C Transition
# ============================================================================

def test_transition_u7b_to_u7c_basic():
    """Test basic transition from U₇-B to U₇-C."""
    # Create mock U₇-B unit
    u7b_unit = InflectionalSurfaceContractUnit(
        uid="u7b_unit_123",
        surface="كِتَابٌ",
        source_u7_unit_id="u7a_unit_123",
        source_u7_trace=("u7a",),
        protected_prefixes=(),
        protected_suffixes=(),
        protected_infixes=(),
        protected_vowels=(),
        protected_core="كتاب",
        root_input="كتاب",
        root_input_permission=RootInputPermission.ALLOWED,
        broken_plural_surface_hint=MarkerHint.UNLIKELY,
        broken_plural_pattern_hint="",
        pronoun_suffix_hint=MarkerHint.UNLIKELY,
        protected_pronoun_suffixes=(),
        definiteness_marker_hint=MarkerHint.UNLIKELY,
        tanwin_marker_hint=MarkerHint.POSSIBLE,
        number_marker_hint=MarkerHint.UNRESOLVED,
        gender_marker_hint=MarkerHint.UNRESOLVED,
        rationality_marker_hint=MarkerHint.UNRESOLVED,
        original_irab_marker_hint=MarkerHint.POSSIBLE,
        secondary_irab_marker_hint=MarkerHint.UNLIKELY,
        nominative_surface_hint=MarkerHint.POSSIBLE,
        accusative_surface_hint=MarkerHint.UNLIKELY,
        genitive_surface_hint=MarkerHint.UNLIKELY,
        jussive_surface_hint=MarkerHint.UNLIKELY,
        verb_prefix_hint=MarkerHint.UNLIKELY,
        verb_suffix_hint=MarkerHint.UNLIKELY,
        passive_surface_hint=MarkerHint.UNLIKELY,
        mazid_extra_hint=MarkerHint.UNLIKELY,
        imperative_surface_hint=MarkerHint.UNLIKELY,
        six_nouns_pattern_hint="",
        proper_name_surface_hint=MarkerHint.UNLIKELY,
        loanword_surface_hint=MarkerHint.UNLIKELY,
        jamid_surface_hint=MarkerHint.POSSIBLE,
        frozen_primitive_surface_hint=MarkerHint.UNLIKELY,
        blocked_root_segments=(),
        blocked_weight_segments=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b"),
    )

    # Create U₇-B layer
    u7b_layer = InflectionalSurfaceContractLayerObject(
        uid="u7b_layer_123",
        units=(u7b_unit,),
        source_pre_weight_layer_id="u7a_layer_123",
        trace_7a=("u7a",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None,
    )

    # Transition to U₇-C
    u7c_layer = transition_u7b_to_u7c(u7b_layer)

    # Verify transition
    assert len(u7c_layer.units) == 1
    u7c_unit = u7c_layer.units[0]
    assert u7c_unit.surface == "كِتَابٌ"
    assert u7c_unit.protected_core == "كتاب"
    assert u7c_unit.root_input == "كتاب"
    assert u7c_unit.root_input_permission == RootInputPermission.ALLOWED
    assert u7c_unit.source_u7b_unit_id == "u7b_unit_123"


def test_transition_u7b_to_u7c_deferred_permission():
    """Test U₇-B to U₇-C transition with DEFERRED permission (broken plural)."""
    # Create mock U₇-B unit with broken plural
    u7b_unit = InflectionalSurfaceContractUnit(
        uid="u7b_unit_rijal",
        surface="رجال",
        source_u7_unit_id="u7a_unit_rijal",
        source_u7_trace=("u7a",),
        protected_prefixes=(),
        protected_suffixes=(),
        protected_infixes=(),
        protected_vowels=(),
        protected_core="رجال",
        root_input="رجال",
        root_input_permission=RootInputPermission.DEFERRED,  # DEFERRED for broken plural
        broken_plural_surface_hint=MarkerHint.POSSIBLE,
        broken_plural_pattern_hint="فِعَال",
        pronoun_suffix_hint=MarkerHint.UNLIKELY,
        protected_pronoun_suffixes=(),
        definiteness_marker_hint=MarkerHint.UNLIKELY,
        tanwin_marker_hint=MarkerHint.UNLIKELY,
        number_marker_hint=MarkerHint.POSSIBLE,
        gender_marker_hint=MarkerHint.UNRESOLVED,
        rationality_marker_hint=MarkerHint.UNRESOLVED,
        original_irab_marker_hint=MarkerHint.UNLIKELY,
        secondary_irab_marker_hint=MarkerHint.UNLIKELY,
        nominative_surface_hint=MarkerHint.UNLIKELY,
        accusative_surface_hint=MarkerHint.UNLIKELY,
        genitive_surface_hint=MarkerHint.UNLIKELY,
        jussive_surface_hint=MarkerHint.UNLIKELY,
        verb_prefix_hint=MarkerHint.UNLIKELY,
        verb_suffix_hint=MarkerHint.UNLIKELY,
        passive_surface_hint=MarkerHint.UNLIKELY,
        mazid_extra_hint=MarkerHint.UNLIKELY,
        imperative_surface_hint=MarkerHint.UNLIKELY,
        six_nouns_pattern_hint="",
        proper_name_surface_hint=MarkerHint.UNLIKELY,
        loanword_surface_hint=MarkerHint.UNLIKELY,
        jamid_surface_hint=MarkerHint.POSSIBLE,
        frozen_primitive_surface_hint=MarkerHint.UNLIKELY,
        blocked_root_segments=(),
        blocked_weight_segments=(),
        residuals=frozenset([make_warning("broken_plural_requires_lexicon")]),
        rank=Rank.CANDIDATE,
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b"),
    )

    u7b_layer = InflectionalSurfaceContractLayerObject(
        uid="u7b_layer_rijal",
        units=(u7b_unit,),
        source_pre_weight_layer_id="u7a_layer_rijal",
        trace_7a=("u7a",),
        residuals=frozenset([make_warning("broken_plural_requires_lexicon")]),
        rank=Rank.CANDIDATE,
        proof=None,
    )

    # Transition to U₇-C
    u7c_layer = transition_u7b_to_u7c(u7b_layer)

    # Verify DEFERRED permission carried forward
    u7c_unit = u7c_layer.units[0]
    assert u7c_unit.surface == "رجال"
    assert u7c_unit.root_input_permission == RootInputPermission.DEFERRED
    assert len(u7c_unit.residuals) > 0


# ============================================================================
# Test 8: Layer Object Validation
# ============================================================================

def test_u7c_layer_object_validation():
    """Test U₇-C layer object validates agreement edge references."""
    unit1 = ClauseSurfaceAgreementUnit(
        uid="unit_1",
        surface="كِتَابٌ",
        source_u7b_unit_id="u7b_1",
        source_u7b_trace=("u7b",),
        protected_core="كتاب",
        root_input="كتاب",
        root_input_permission=RootInputPermission.ALLOWED,
    )

    unit2 = ClauseSurfaceAgreementUnit(
        uid="unit_2",
        surface="جميل",
        source_u7b_unit_id="u7b_2",
        source_u7b_trace=("u7b",),
        protected_core="جميل",
        root_input="جميل",
        root_input_permission=RootInputPermission.ALLOWED,
    )

    # Valid edge between existing units
    valid_edge = AgreementSurfaceEdge(
        uid="edge_1",
        edge_type=AgreementEdgeType.NOUN_ADJECTIVE,
        source_unit_id="unit_1",
        target_unit_id="unit_2",
        number_agreement_hint=AgreementHint.POSSIBLE,
        gender_agreement_hint=AgreementHint.POSSIBLE,
        rationality_agreement_hint=AgreementHint.UNRESOLVED,
        broken_plural_feminine_singular_hint=MarkerHint.UNLIKELY,
        non_rational_plural_feminine_agreement_hint=MarkerHint.UNLIKELY,
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
    )

    # Create layer with valid edge
    layer = ClauseSurfaceAgreementLayerObject(
        uid="layer_1",
        units=(unit1, unit2),
        agreement_edges=(valid_edge,),
        agreement_candidates=(),
        broken_plural_guards=(),
        source_u7b_layer_id="u7b_layer",
        trace_7b=("u7b",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
    )

    assert len(layer.units) == 2
    assert len(layer.agreement_edges) == 1


def test_u7c_layer_object_invalid_edge_reference():
    """Test U₇-C layer object rejects edge with non-existent unit reference."""
    unit1 = ClauseSurfaceAgreementUnit(
        uid="unit_1",
        surface="كِتَابٌ",
        source_u7b_unit_id="u7b_1",
        source_u7b_trace=("u7b",),
        protected_core="كتاب",
        root_input="كتاب",
        root_input_permission=RootInputPermission.ALLOWED,
    )

    # Edge referencing non-existent unit
    invalid_edge = AgreementSurfaceEdge(
        uid="edge_1",
        edge_type=AgreementEdgeType.NOUN_ADJECTIVE,
        source_unit_id="unit_1",
        target_unit_id="unit_999",  # Non-existent unit
        number_agreement_hint=AgreementHint.POSSIBLE,
        gender_agreement_hint=AgreementHint.POSSIBLE,
        rationality_agreement_hint=AgreementHint.UNRESOLVED,
        broken_plural_feminine_singular_hint=MarkerHint.UNLIKELY,
        non_rational_plural_feminine_agreement_hint=MarkerHint.UNLIKELY,
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
    )

    # Should raise ValueError
    with pytest.raises(ValueError, match="non-existent.*unit"):
        layer = ClauseSurfaceAgreementLayerObject(
            uid="layer_1",
            units=(unit1,),
            agreement_edges=(invalid_edge,),
            agreement_candidates=(),
            broken_plural_guards=(),
            source_u7b_layer_id="u7b_layer",
            trace_7b=("u7b",),
            residuals=frozenset(),
            rank=Rank.CANDIDATE,
        )


# ============================================================================
# Test 9: Constitutional Law Enforcement
# ============================================================================

def test_u7c_agreement_not_irab_judgment():
    """Test Axiom 7C.2: Agreement ≠ i'rab judgment."""
    # Agreement edge is observation, NOT judgment
    edge = AgreementSurfaceEdge(
        uid=str(uuid4()),
        edge_type=AgreementEdgeType.NOUN_ADJECTIVE,
        source_unit_id="noun_unit",
        target_unit_id="adj_unit",
        number_agreement_hint=AgreementHint.POSSIBLE,
        gender_agreement_hint=AgreementHint.POSSIBLE,
        rationality_agreement_hint=AgreementHint.UNRESOLVED,
        broken_plural_feminine_singular_hint=MarkerHint.UNLIKELY,
        non_rational_plural_feminine_agreement_hint=MarkerHint.UNLIKELY,
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
    )

    # Verify edge contains only hints, not judgments
    assert edge.number_agreement_hint == AgreementHint.POSSIBLE
    assert edge.gender_agreement_hint == AgreementHint.POSSIBLE
    # No i'rab fields should exist
    assert not hasattr(edge, 'irab')
    assert not hasattr(edge, 'final_irab')
    assert not hasattr(edge, 'hukm')


def test_u7c_agreement_not_function_assignment():
    """Test Axiom 7C.3: Agreement ≠ function assignment."""
    # Agreement candidate does NOT assign grammatical function
    candidate = AgreementSurfaceCandidate(
        uid=str(uuid4()),
        agreement_edge=AgreementSurfaceEdge(
            uid=str(uuid4()),
            edge_type=AgreementEdgeType.VERB_SUBJECT,
            source_unit_id="verb_unit",
            target_unit_id="subject_unit",
            number_agreement_hint=AgreementHint.POSSIBLE,
            gender_agreement_hint=AgreementHint.POSSIBLE,
            rationality_agreement_hint=AgreementHint.POSSIBLE,
            broken_plural_feminine_singular_hint=MarkerHint.UNLIKELY,
            non_rational_plural_feminine_agreement_hint=MarkerHint.UNLIKELY,
            residuals=frozenset(),
            rank=Rank.CANDIDATE,
        ),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
    )

    # Verify no function assignment fields exist
    assert not hasattr(candidate, 'fa3il')
    assert not hasattr(candidate, 'maf3ul')
    assert not hasattr(candidate, 'mubtada')
    assert not hasattr(candidate, 'khabar')
    # Only hints and evidence
    assert hasattr(candidate, 'agreement_edge')
    assert hasattr(candidate, 'elevates_permission')
    assert hasattr(candidate, 'confirms_permission')


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
