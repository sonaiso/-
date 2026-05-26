"""
Tests for U₇ Pre-Weight Contract Carrier

Test Categories:
1. Constitutional prohibition tests (no root, weight, meaning, hukm, etc.)
2. Closed-class blocking tests
3. Open-class contract tests
4. Path permission tests
5. Golden case tests (وَ, بِ, كِتَابِ, ـهِمْ, etc.)
6. Trace and evidence tests
"""

import pytest
from uuid import uuid4

from dal_core.foundation import Rank
from dal_core.residuals import make_warning
from dal_core.u6_mabni_closed_class_carrier import (
    MabniClosedClassUnit,
    MabniClosedClassLayerObject,
    MabniClosedClassCandidate,
    MabniClosedClassType,
    ClosedClassSubtype,
)
from dal_core.u7_pre_weight_contract_carrier import (
    ContractStatus,
    PathPermission,
    PreWeightContractUnit,
    PreWeightContractLayerObject,
    PreWeightContractResult,
    PreWeightContractFailureType,
    CPB7,
    pre_weight_contract_7,
)


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_u6_layer_closed_class_wa():
    """U₆ layer with closed-class وَ (conjunction)."""
    mabni_candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
        subtype=ClosedClassSubtype.HARF_ATF,
        lexicon_support=0.9,
        evidence=("known_particle=وَ", "subtype=حرف عطف"),
        source_u5_unit_id="u5_wa",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    mabni_unit = MabniClosedClassUnit(
        uid="u6_wa",
        surface="وَ",
        source_functional_role_unit_id="u5_wa",
        trace_5=("u5_layer",),
        mabni_classification=mabni_candidate,
        blocked_paths=("root_extraction", "weight_determination"),
        evidence=("known_particle=وَ", "blocks_root_weight_path"),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    layer = MabniClosedClassLayerObject(
        uid="u6_layer",
        units=(mabni_unit,),
        source_functional_role_layer_id="u5_layer",
        trace_5=("u5_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    return layer


@pytest.fixture
def sample_u6_layer_closed_class_bi():
    """U₆ layer with closed-class بِ (preposition)."""
    mabni_candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
        subtype=ClosedClassSubtype.HARF_JARR,
        lexicon_support=0.9,
        evidence=("known_particle=بِ", "subtype=حرف جر"),
        source_u5_unit_id="u5_bi",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    mabni_unit = MabniClosedClassUnit(
        uid="u6_bi",
        surface="بِ",
        source_functional_role_unit_id="u5_bi",
        trace_5=("u5_layer",),
        mabni_classification=mabni_candidate,
        blocked_paths=("root_extraction", "weight_determination"),
        evidence=("known_particle=بِ", "blocks_root_weight_path"),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    layer = MabniClosedClassLayerObject(
        uid="u6_layer",
        units=(mabni_unit,),
        source_functional_role_layer_id="u5_layer",
        trace_5=("u5_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    return layer


@pytest.fixture
def sample_u6_layer_attached_pronoun():
    """U₆ layer with attached pronoun ـهِمْ."""
    mabni_candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.ATTACHED_PRONOUN_CLOSED_CLASS,
        subtype=ClosedClassSubtype.PRONOUN_ATTACHED,
        lexicon_support=0.9,
        evidence=("u5_pronoun_role=attached", "subtype=ضمير متصل"),
        source_u5_unit_id="u5_hum",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    mabni_unit = MabniClosedClassUnit(
        uid="u6_hum",
        surface="ـهِمْ",
        source_functional_role_unit_id="u5_hum",
        trace_5=("u5_layer",),
        mabni_classification=mabni_candidate,
        blocked_paths=("root_extraction", "weight_determination"),
        evidence=("u5_pronoun_role=attached", "blocks_root_weight_path"),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    layer = MabniClosedClassLayerObject(
        uid="u6_layer",
        units=(mabni_unit,),
        source_functional_role_layer_id="u5_layer",
        trace_5=("u5_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    return layer


@pytest.fixture
def sample_u6_layer_open_class():
    """U₆ layer with open-class كِتَابِ."""
    mabni_candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.OPEN_CLASS_CORE_CANDIDATE,
        subtype=None,
        lexicon_support=0.8,
        evidence=("no_closed_class_evidence", "default_to_open_class"),
        source_u5_unit_id="u5_kitaab",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    mabni_unit = MabniClosedClassUnit(
        uid="u6_kitaab",
        surface="كِتَابِ",
        source_functional_role_unit_id="u5_kitaab",
        trace_5=("u5_layer",),
        mabni_classification=mabni_candidate,
        blocked_paths=(),
        evidence=("no_closed_class_evidence", "requires_root_weight_path"),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    layer = MabniClosedClassLayerObject(
        uid="u6_layer",
        units=(mabni_unit,),
        source_functional_role_layer_id="u5_layer",
        trace_5=("u5_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    return layer


@pytest.fixture
def sample_u6_layer_full_composition():
    """U₆ layer with full composition (وَبِكِتَابِهِمْ)."""
    # وَ - conjunction
    wa_candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
        subtype=ClosedClassSubtype.HARF_ATF,
        lexicon_support=0.9,
        evidence=("known_particle=وَ",),
        source_u5_unit_id="u5_wa",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    wa_unit = MabniClosedClassUnit(
        uid="u6_wa",
        surface="وَ",
        source_functional_role_unit_id="u5_wa",
        trace_5=("u5_layer",),
        mabni_classification=wa_candidate,
        blocked_paths=("root_extraction", "weight_determination"),
        evidence=("known_particle=وَ",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    # بِ - preposition
    bi_candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
        subtype=ClosedClassSubtype.HARF_JARR,
        lexicon_support=0.9,
        evidence=("known_particle=بِ",),
        source_u5_unit_id="u5_bi",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    bi_unit = MabniClosedClassUnit(
        uid="u6_bi",
        surface="بِ",
        source_functional_role_unit_id="u5_bi",
        trace_5=("u5_layer",),
        mabni_classification=bi_candidate,
        blocked_paths=("root_extraction", "weight_determination"),
        evidence=("known_particle=بِ",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    # كِتَابِ - open class
    kitaab_candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.OPEN_CLASS_CORE_CANDIDATE,
        subtype=None,
        lexicon_support=0.8,
        evidence=("no_closed_class_evidence",),
        source_u5_unit_id="u5_kitaab",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    kitaab_unit = MabniClosedClassUnit(
        uid="u6_kitaab",
        surface="كِتَابِ",
        source_functional_role_unit_id="u5_kitaab",
        trace_5=("u5_layer",),
        mabni_classification=kitaab_candidate,
        blocked_paths=(),
        evidence=("requires_root_weight_path",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    # ـهِمْ - attached pronoun
    hum_candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.ATTACHED_PRONOUN_CLOSED_CLASS,
        subtype=ClosedClassSubtype.PRONOUN_ATTACHED,
        lexicon_support=0.9,
        evidence=("u5_pronoun_role=attached",),
        source_u5_unit_id="u5_hum",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    hum_unit = MabniClosedClassUnit(
        uid="u6_hum",
        surface="ـهِمْ",
        source_functional_role_unit_id="u5_hum",
        trace_5=("u5_layer",),
        mabni_classification=hum_candidate,
        blocked_paths=("root_extraction", "weight_determination"),
        evidence=("blocks_root_weight_path",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    layer = MabniClosedClassLayerObject(
        uid="u6_layer",
        units=(wa_unit, bi_unit, kitaab_unit, hum_unit),
        source_functional_role_layer_id="u5_layer",
        trace_5=("u5_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    return layer


# ============================================================================
# Constitutional Prohibition Tests
# ============================================================================

def test_contract_unit_no_root_field():
    """U₇ PreWeightContractUnit MUST NOT contain 'root' field."""
    # This should raise ValueError
    with pytest.raises(ValueError, match="MUST NOT contain 'root' field"):
        # We can't actually add the field in frozen dataclass, but we can test the validation
        # Create valid unit first
        unit = PreWeightContractUnit(
            uid=str(uuid4()),
            surface="test",
            source_u6_unit_id="u6_test",
            source_u6_trace=("u6_layer",),
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
            required_evidence=(),
            blocked_paths=(),
            residuals=frozenset(),
            rank=Rank.CANDIDATE,
            trace=("u6_layer",)
        )
        # Manually add forbidden field to trigger validation
        object.__setattr__(unit, 'root', 'ktb')
        unit.__post_init__()


def test_contract_unit_no_weight_field():
    """U₇ PreWeightContractUnit MUST NOT contain 'weight' field."""
    with pytest.raises(ValueError, match="MUST NOT contain 'weight' field"):
        unit = PreWeightContractUnit(
            uid=str(uuid4()),
            surface="test",
            source_u6_unit_id="u6_test",
            source_u6_trace=("u6_layer",),
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
            required_evidence=(),
            blocked_paths=(),
            residuals=frozenset(),
            rank=Rank.CANDIDATE,
            trace=("u6_layer",)
        )
        object.__setattr__(unit, 'weight', 'فعل')
        unit.__post_init__()


def test_contract_unit_no_meaning_field():
    """U₇ PreWeightContractUnit MUST NOT contain 'meaning' field."""
    with pytest.raises(ValueError, match="MUST NOT contain 'meaning' field"):
        unit = PreWeightContractUnit(
            uid=str(uuid4()),
            surface="test",
            source_u6_unit_id="u6_test",
            source_u6_trace=("u6_layer",),
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
            required_evidence=(),
            blocked_paths=(),
            residuals=frozenset(),
            rank=Rank.CANDIDATE,
            trace=("u6_layer",)
        )
        object.__setattr__(unit, 'meaning', 'some_meaning')
        unit.__post_init__()


def test_contract_unit_no_hukm_field():
    """U₇ PreWeightContractUnit MUST NOT contain 'hukm' field."""
    with pytest.raises(ValueError, match="MUST NOT contain 'hukm' field"):
        unit = PreWeightContractUnit(
            uid=str(uuid4()),
            surface="test",
            source_u6_unit_id="u6_test",
            source_u6_trace=("u6_layer",),
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
            required_evidence=(),
            blocked_paths=(),
            residuals=frozenset(),
            rank=Rank.CANDIDATE,
            trace=("u6_layer",)
        )
        object.__setattr__(unit, 'hukm', 'some_hukm')
        unit.__post_init__()


# ============================================================================
# Golden Case Tests
# ============================================================================

def test_golden_case_wa_blocks_root_weight(sample_u6_layer_closed_class_wa):
    """وَ → closed_class_blocked, root blocked, weight blocked."""
    result = pre_weight_contract_7(sample_u6_layer_closed_class_wa)

    assert result.success
    assert result.layer_object is not None
    assert len(result.layer_object.units) == 1

    unit = result.layer_object.units[0]
    assert unit.surface == "وَ"
    assert unit.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED
    assert unit.root_path_permission == PathPermission.BLOCKED
    assert unit.weight_path_permission == PathPermission.BLOCKED
    assert unit.stem_path_permission == PathPermission.BLOCKED
    assert "root_extraction" in unit.blocked_paths
    assert "weight_determination" in unit.blocked_paths


def test_golden_case_bi_blocks_root_weight(sample_u6_layer_closed_class_bi):
    """بِ → closed_class_blocked, root blocked, weight blocked."""
    result = pre_weight_contract_7(sample_u6_layer_closed_class_bi)

    assert result.success
    assert result.layer_object is not None
    assert len(result.layer_object.units) == 1

    unit = result.layer_object.units[0]
    assert unit.surface == "بِ"
    assert unit.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED
    assert unit.root_path_permission == PathPermission.BLOCKED
    assert unit.weight_path_permission == PathPermission.BLOCKED
    assert "root_extraction" in unit.blocked_paths
    assert "weight_determination" in unit.blocked_paths


def test_golden_case_attached_pronoun_blocks_root(sample_u6_layer_attached_pronoun):
    """ـهِمْ → closed_class_blocked, root blocked, weight blocked, pronoun path preserved."""
    result = pre_weight_contract_7(sample_u6_layer_attached_pronoun)

    assert result.success
    assert result.layer_object is not None
    assert len(result.layer_object.units) == 1

    unit = result.layer_object.units[0]
    assert unit.surface == "ـهِمْ"
    assert unit.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED
    assert unit.root_path_permission == PathPermission.BLOCKED
    assert unit.weight_path_permission == PathPermission.BLOCKED
    assert "root_extraction" in unit.blocked_paths


def test_golden_case_kitaab_opens_contract(sample_u6_layer_open_class):
    """كِتَابِ → open_core_contract_candidate, root possible, weight possible, NO extraction."""
    result = pre_weight_contract_7(sample_u6_layer_open_class)

    assert result.success
    assert result.layer_object is not None
    assert len(result.layer_object.units) == 1

    unit = result.layer_object.units[0]
    assert unit.surface == "كِتَابِ"
    assert unit.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE
    assert unit.root_path_permission == PathPermission.POSSIBLE
    assert unit.weight_path_permission == PathPermission.POSSIBLE
    assert unit.stem_path_permission == PathPermission.POSSIBLE

    # CRITICAL: U₇ does NOT extract root or weight
    assert not hasattr(unit, 'root')
    assert not hasattr(unit, 'weight')
    assert not hasattr(unit, 'pattern')


def test_golden_case_full_composition(sample_u6_layer_full_composition):
    """وَبِكِتَابِهِمْ → 3 blocked (وَ,بِ,ـهِمْ) + 1 contract candidate (كِتَابِ)."""
    result = pre_weight_contract_7(sample_u6_layer_full_composition)

    assert result.success
    assert result.layer_object is not None
    assert len(result.layer_object.units) == 4

    # وَ - blocked
    wa = result.layer_object.units[0]
    assert wa.surface == "وَ"
    assert wa.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED
    assert wa.root_path_permission == PathPermission.BLOCKED

    # بِ - blocked
    bi = result.layer_object.units[1]
    assert bi.surface == "بِ"
    assert bi.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED
    assert bi.root_path_permission == PathPermission.BLOCKED

    # كِتَابِ - contract candidate
    kitaab = result.layer_object.units[2]
    assert kitaab.surface == "كِتَابِ"
    assert kitaab.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE
    assert kitaab.root_path_permission == PathPermission.POSSIBLE
    assert kitaab.weight_path_permission == PathPermission.POSSIBLE

    # ـهِمْ - blocked
    hum = result.layer_object.units[3]
    assert hum.surface == "ـهِمْ"
    assert hum.contract_status == ContractStatus.CLOSED_CLASS_BLOCKED
    assert hum.root_path_permission == PathPermission.BLOCKED


def test_open_class_no_root_emission(sample_u6_layer_open_class):
    """Open-class unit opens contract but does NOT emit root."""
    result = pre_weight_contract_7(sample_u6_layer_open_class)

    assert result.success
    unit = result.layer_object.units[0]

    # Root path is POSSIBLE
    assert unit.root_path_permission == PathPermission.POSSIBLE

    # But NO root field exists
    assert not hasattr(unit, 'root')
    assert not hasattr(unit, 'root_certificate')


def test_open_class_no_weight_emission(sample_u6_layer_open_class):
    """Open-class unit opens contract but does NOT emit weight."""
    result = pre_weight_contract_7(sample_u6_layer_open_class)

    assert result.success
    unit = result.layer_object.units[0]

    # Weight path is POSSIBLE
    assert unit.weight_path_permission == PathPermission.POSSIBLE

    # But NO weight field exists
    assert not hasattr(unit, 'weight')
    assert not hasattr(unit, 'weight_certificate')
    assert not hasattr(unit, 'pattern')


# ============================================================================
# Trace and Evidence Tests
# ============================================================================

def test_trace_preservation(sample_u6_layer_closed_class_wa):
    """U₇ preserves trace from U₆."""
    result = pre_weight_contract_7(sample_u6_layer_closed_class_wa)

    assert result.success
    assert result.layer_object.source_mabni_layer_id == "u6_layer"
    assert result.layer_object.trace_6 == ("u6_layer",)

    unit = result.layer_object.units[0]
    assert unit.source_u6_unit_id == "u6_wa"
    assert unit.source_u6_trace == ("u5_layer",)


def test_evidence_propagation(sample_u6_layer_closed_class_wa):
    """U₇ propagates evidence about blocking."""
    result = pre_weight_contract_7(sample_u6_layer_closed_class_wa)

    assert result.success
    unit = result.layer_object.units[0]

    # Required evidence should be present
    assert len(unit.required_evidence) > 0
    assert "closed_class_mabni_blocks_morphology" in unit.required_evidence


def test_cpb7_completeness(sample_u6_layer_full_composition):
    """CPB₇ validates completeness."""
    result = pre_weight_contract_7(sample_u6_layer_full_composition)

    assert result.success
    assert CPB7.is_complete(result.layer_object)


def test_cpb7_proof_structure(sample_u6_layer_full_composition):
    """CPB₇ builds valid proof structure."""
    result = pre_weight_contract_7(sample_u6_layer_full_composition)

    assert result.success
    assert result.layer_object.proof is not None
    assert result.layer_object.proof.claim == "U₇ pre-weight contract paths determined"
    assert "U7_PRE_WEIGHT_CONTRACT" in result.layer_object.proof.scope
    assert "root_stem_gate" in result.layer_object.proof.allowed_next_gates


def test_cpb7_proof_limitations(sample_u6_layer_full_composition):
    """CPB₇ proof declares limitations."""
    result = pre_weight_contract_7(sample_u6_layer_full_composition)

    assert result.success
    proof = result.layer_object.proof

    # Check forbidden next gates
    assert "root_certificate" in proof.forbidden_next_gates
    assert "weight_certificate" in proof.forbidden_next_gates
    assert "meaning_certificate" in proof.forbidden_next_gates
    assert "hukm_certificate" in proof.forbidden_next_gates

    # Check limitations
    assert "no_root_extraction" in proof.limitations
    assert "no_weight_determination" in proof.limitations
    assert "contract_is_permission_not_certificate" in proof.limitations


def test_empty_input_handling():
    """U₇ handles empty input gracefully."""
    empty_layer = MabniClosedClassLayerObject(
        uid="empty_layer",
        units=(),
        source_functional_role_layer_id="u5_layer",
        trace_5=("u5_layer",),
        residuals=frozenset(),
        rank=Rank.ZERO
    )

    result = pre_weight_contract_7(empty_layer)

    assert not result.success
    assert result.failure_type == PreWeightContractFailureType.NO_MABNI_UNITS


def test_execution_without_errors(sample_u6_layer_full_composition):
    """U₇ executes without runtime errors on full composition."""
    result = pre_weight_contract_7(sample_u6_layer_full_composition)

    assert result.success
    assert result.layer_object is not None
    assert len(result.layer_object.units) == 4


# ============================================================================
# Path Permission Tests
# ============================================================================

def test_closed_class_all_paths_blocked(sample_u6_layer_closed_class_wa):
    """Closed-class unit blocks ALL morphological paths."""
    result = pre_weight_contract_7(sample_u6_layer_closed_class_wa)

    assert result.success
    unit = result.layer_object.units[0]

    assert unit.lexical_path_potential == PathPermission.BLOCKED
    assert unit.root_path_permission == PathPermission.BLOCKED
    assert unit.stem_path_permission == PathPermission.BLOCKED
    assert unit.weight_path_permission == PathPermission.BLOCKED


def test_open_class_all_paths_possible(sample_u6_layer_open_class):
    """Open-class unit marks ALL morphological paths as POSSIBLE."""
    result = pre_weight_contract_7(sample_u6_layer_open_class)

    assert result.success
    unit = result.layer_object.units[0]

    assert unit.lexical_path_potential == PathPermission.POSSIBLE
    assert unit.root_path_permission == PathPermission.POSSIBLE
    assert unit.stem_path_permission == PathPermission.POSSIBLE
    assert unit.weight_path_permission == PathPermission.POSSIBLE


def test_contract_candidate_requires_evidence(sample_u6_layer_open_class):
    """Contract candidate requires evidence for approval."""
    result = pre_weight_contract_7(sample_u6_layer_open_class)

    assert result.success
    unit = result.layer_object.units[0]

    assert unit.contract_status == ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE
    assert len(unit.required_evidence) > 0
    assert "lexical_attestation" in unit.required_evidence or "surface_family_evidence" in unit.required_evidence
