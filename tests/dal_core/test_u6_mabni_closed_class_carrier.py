"""
Tests for U₆ Mabni Closed Class Carrier

Test Categories:
1. Constitutional prohibition tests (no root, weight, meaning, hukm)
2. Closed-class identification tests
3. Open-class identification tests
4. Path blocking tests
5. Golden case tests (وَبِكِتَابِهِمْ)
6. Trace and evidence tests
"""

import pytest
from uuid import uuid4

from dal_core.foundation import Rank
from dal_core.residuals import make_warning
from dal_core.u4_true_singular_lafz_carrier import (
    TrueLafzUnit,
    TrueLafzUnitType,
    TrueLafzLayerObject,
)
from dal_core.u5_functional_role_carrier import (
    FunctionalRoleUnit,
    FunctionalRoleLayerObject,
    FunctionalRoleCandidate,
    RoleSort,
    ClosedClassRoleCandidate,
    PronounRoleCandidate,
    NounRoleCandidate,
)
from dal_core.u6_mabni_closed_class_carrier import (
    MabniClosedClassType,
    ClosedClassSubtype,
    MabniClosedClassCandidate,
    MabniClosedClassUnit,
    MabniClosedClassLayerObject,
    MabniClosedClassResult,
    MabniClosedClassFailureType,
    CPB6,
    mabni_closed_class_6,
)
from dal_core.mabni_registry import get_default_mabni_registry


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_u5_layer_with_closed_class():
    """U₅ layer with closed-class candidates (وَ, بِ)."""
    # وَ - conjunction
    wa_candidate = FunctionalRoleCandidate(
        uid=str(uuid4()),
        role=ClosedClassRoleCandidate.HARF_ATF_CANDIDATE,
        sort=RoleSort.CLOSED_CLASS,
        surface_support=0.9,
        evidence=("surface_match_conjunction", "surface=وَ"),
        source_u4_unit_id="u4_wa",
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    wa_unit = FunctionalRoleUnit(
        uid="u5_wa",
        surface="وَ",
        source_lafz_unit_id="u4_wa",
        trace_4=("u4_layer",),
        role_candidates=(wa_candidate,),
        evidence=("u4_unit_type=BOUND_PROCLITIC",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    # بِ - preposition
    bi_candidate = FunctionalRoleCandidate(
        uid=str(uuid4()),
        role=ClosedClassRoleCandidate.HARF_JARR_CANDIDATE,
        sort=RoleSort.CLOSED_CLASS,
        surface_support=0.8,
        evidence=("surface_match_preposition", "surface=بِ"),
        source_u4_unit_id="u4_bi",
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    bi_unit = FunctionalRoleUnit(
        uid="u5_bi",
        surface="بِ",
        source_lafz_unit_id="u4_bi",
        trace_4=("u4_layer",),
        role_candidates=(bi_candidate,),
        evidence=("u4_unit_type=BOUND_PROCLITIC",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    layer = FunctionalRoleLayerObject(
        uid="u5_layer",
        units=(wa_unit, bi_unit),
        source_lafz_layer_id="u4_layer",
        trace_4=("u4_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    return layer


@pytest.fixture
def sample_u5_layer_with_open_class():
    """U₅ layer with open-class candidate (كِتَابٍ)."""
    # كِتَابٍ - noun candidate
    noun_candidate = FunctionalRoleCandidate(
        uid=str(uuid4()),
        role=NounRoleCandidate.INDEFINITE_NOUN_CANDIDATE,
        sort=RoleSort.NOUN_CANDIDATE,
        surface_support=0.7,
        evidence=("u4_indefinite_surface_hint_possible",),
        source_u4_unit_id="u4_kitaab",
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    kitaab_unit = FunctionalRoleUnit(
        uid="u5_kitaab",
        surface="كِتَابٍ",
        source_lafz_unit_id="u4_kitaab",
        trace_4=("u4_layer",),
        role_candidates=(noun_candidate,),
        evidence=("u4_unit_type=TRUE_SINGULAR_CORE_CANDIDATE",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    layer = FunctionalRoleLayerObject(
        uid="u5_layer",
        units=(kitaab_unit,),
        source_lafz_layer_id="u4_layer",
        trace_4=("u4_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    return layer


@pytest.fixture
def sample_u5_layer_with_pronoun():
    """U₅ layer with pronoun candidate (ـهِمْ)."""
    # ـهِمْ - attached pronoun
    pronoun_candidate = FunctionalRoleCandidate(
        uid=str(uuid4()),
        role=PronounRoleCandidate.ATTACHED_PRONOUN_CANDIDATE,
        sort=RoleSort.PRONOUN,
        surface_support=0.9,
        evidence=("u4_attached_pronoun_type",),
        source_u4_unit_id="u4_hum",
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    hum_unit = FunctionalRoleUnit(
        uid="u5_hum",
        surface="ـهِمْ",
        source_lafz_unit_id="u4_hum",
        trace_4=("u4_layer",),
        role_candidates=(pronoun_candidate,),
        evidence=("u4_unit_type=ATTACHED_PRONOUN_CANDIDATE",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    layer = FunctionalRoleLayerObject(
        uid="u5_layer",
        units=(hum_unit,),
        source_lafz_layer_id="u4_layer",
        trace_4=("u4_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    return layer


@pytest.fixture
def sample_u5_layer_full_composition():
    """U₅ layer with full composition (وَبِكِتَابِهِمْ)."""
    # وَ - conjunction
    wa_candidate = FunctionalRoleCandidate(
        uid=str(uuid4()),
        role=ClosedClassRoleCandidate.HARF_ATF_CANDIDATE,
        sort=RoleSort.CLOSED_CLASS,
        surface_support=0.9,
        evidence=("surface_match_conjunction",),
        source_u4_unit_id="u4_wa",
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    wa_unit = FunctionalRoleUnit(
        uid="u5_wa",
        surface="وَ",
        source_lafz_unit_id="u4_wa",
        trace_4=("u4_layer",),
        role_candidates=(wa_candidate,),
        evidence=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    # بِ - preposition
    bi_candidate = FunctionalRoleCandidate(
        uid=str(uuid4()),
        role=ClosedClassRoleCandidate.HARF_JARR_CANDIDATE,
        sort=RoleSort.CLOSED_CLASS,
        surface_support=0.8,
        evidence=("surface_match_preposition",),
        source_u4_unit_id="u4_bi",
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    bi_unit = FunctionalRoleUnit(
        uid="u5_bi",
        surface="بِ",
        source_lafz_unit_id="u4_bi",
        trace_4=("u4_layer",),
        role_candidates=(bi_candidate,),
        evidence=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    # كِتَابِ - noun
    noun_candidate = FunctionalRoleCandidate(
        uid=str(uuid4()),
        role=NounRoleCandidate.DEFINITE_NOUN_CANDIDATE,
        sort=RoleSort.NOUN_CANDIDATE,
        surface_support=0.7,
        evidence=("u4_definite_surface_hint_possible",),
        source_u4_unit_id="u4_kitaab",
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    kitaab_unit = FunctionalRoleUnit(
        uid="u5_kitaab",
        surface="كِتَابِ",
        source_lafz_unit_id="u4_kitaab",
        trace_4=("u4_layer",),
        role_candidates=(noun_candidate,),
        evidence=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    # ـهِمْ - pronoun
    pronoun_candidate = FunctionalRoleCandidate(
        uid=str(uuid4()),
        role=PronounRoleCandidate.ATTACHED_PRONOUN_CANDIDATE,
        sort=RoleSort.PRONOUN,
        surface_support=0.9,
        evidence=("u4_attached_pronoun_type",),
        source_u4_unit_id="u4_hum",
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    hum_unit = FunctionalRoleUnit(
        uid="u5_hum",
        surface="ـهِمْ",
        source_lafz_unit_id="u4_hum",
        trace_4=("u4_layer",),
        role_candidates=(pronoun_candidate,),
        evidence=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    layer = FunctionalRoleLayerObject(
        uid="u5_layer",
        units=(wa_unit, bi_unit, kitaab_unit, hum_unit),
        source_lafz_layer_id="u4_layer",
        trace_4=("u4_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    return layer


# ============================================================================
# Test 1: Constitutional Prohibition Tests
# ============================================================================

def test_mabni_candidate_no_root_field():
    """MabniClosedClassCandidate MUST NOT contain 'root' field."""
    # Test that guard catches attempt to create candidate with root via hasattr check
    candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
        subtype=ClosedClassSubtype.HARF_JARR,
        lexicon_support=0.9,
        evidence=("test",),
        source_u5_unit_id="u5_test",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    # Verify no root field exists
    assert not hasattr(candidate, 'root')


def test_mabni_candidate_no_weight_field():
    """MabniClosedClassCandidate MUST NOT contain 'weight' field."""
    candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
        subtype=ClosedClassSubtype.HARF_JARR,
        lexicon_support=0.9,
        evidence=("test",),
        source_u5_unit_id="u5_test",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    # Verify no weight field exists
    assert not hasattr(candidate, 'weight')


def test_mabni_candidate_no_meaning_field():
    """MabniClosedClassCandidate MUST NOT contain 'meaning' field."""
    candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
        subtype=ClosedClassSubtype.HARF_JARR,
        lexicon_support=0.9,
        evidence=("test",),
        source_u5_unit_id="u5_test",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    # Verify no meaning field exists
    assert not hasattr(candidate, 'meaning')


def test_mabni_candidate_no_hukm_field():
    """MabniClosedClassCandidate MUST NOT contain 'hukm' field."""
    candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
        subtype=ClosedClassSubtype.HARF_JARR,
        lexicon_support=0.9,
        evidence=("test",),
        source_u5_unit_id="u5_test",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    # Verify no hukm field exists
    assert not hasattr(candidate, 'hukm')


def test_mabni_candidate_no_resolved_reference_field():
    """MabniClosedClassCandidate MUST NOT contain 'resolved_reference' field."""
    candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE,
        subtype=ClosedClassSubtype.PRONOUN_ATTACHED,
        lexicon_support=0.9,
        evidence=("test",),
        source_u5_unit_id="u5_test",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    # Verify no resolved_reference field exists
    assert not hasattr(candidate, 'resolved_reference')


def test_cpb6_completeness():
    """CPB₆ completeness predicate validation."""
    # Create minimal valid layer
    candidate = MabniClosedClassCandidate(
        uid=str(uuid4()),
        mabni_type=MabniClosedClassType.OPEN_CLASS_CORE_CANDIDATE,
        subtype=None,
        lexicon_support=0.8,
        evidence=("test",),
        source_u5_unit_id="u5_test",
        mabni_entry=None,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    unit = MabniClosedClassUnit(
        uid=str(uuid4()),
        surface="test",
        source_functional_role_unit_id="u5_test",
        trace_5=("u5_layer",),
        mabni_classification=candidate,
        blocked_paths=(),
        evidence=("test",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
    layer = MabniClosedClassLayerObject(
        uid=str(uuid4()),
        units=(unit,),
        source_functional_role_layer_id="u5_layer",
        trace_5=("u5_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    assert CPB6.is_complete(layer)


# ============================================================================
# Test 2: Closed-Class Identification Tests
# ============================================================================

def test_identify_conjunction_wa(sample_u5_layer_with_closed_class):
    """وَ should be identified as CLOSED_CLASS_MABNI_CANDIDATE (HARF_ATF)."""
    result = mabni_closed_class_6(sample_u5_layer_with_closed_class)

    assert result.success
    assert result.layer_object is not None

    # Find وَ unit
    wa_unit = next(u for u in result.layer_object.units if u.surface == "وَ")

    assert wa_unit.mabni_classification.mabni_type == MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE
    assert wa_unit.mabni_classification.subtype == ClosedClassSubtype.HARF_ATF
    assert "root_extraction" in wa_unit.blocked_paths
    assert "weight_determination" in wa_unit.blocked_paths


def test_identify_preposition_bi(sample_u5_layer_with_closed_class):
    """بِ should be identified as CLOSED_CLASS_MABNI_CANDIDATE (HARF_JARR)."""
    result = mabni_closed_class_6(sample_u5_layer_with_closed_class)

    assert result.success
    assert result.layer_object is not None

    # Find بِ unit
    bi_unit = next(u for u in result.layer_object.units if u.surface == "بِ")

    assert bi_unit.mabni_classification.mabni_type == MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE
    assert bi_unit.mabni_classification.subtype == ClosedClassSubtype.HARF_JARR
    assert "root_extraction" in bi_unit.blocked_paths
    assert "weight_determination" in bi_unit.blocked_paths


def test_identify_attached_pronoun(sample_u5_layer_with_pronoun):
    """ـهِمْ should be identified as ATTACHED_PRONOUN_CLOSED_CLASS."""
    result = mabni_closed_class_6(sample_u5_layer_with_pronoun)

    assert result.success
    assert result.layer_object is not None

    hum_unit = result.layer_object.units[0]

    assert hum_unit.surface == "ـهِمْ"
    assert hum_unit.mabni_classification.mabni_type == MabniClosedClassType.ATTACHED_PRONOUN_CLOSED_CLASS
    assert hum_unit.mabni_classification.subtype == ClosedClassSubtype.PRONOUN_ATTACHED
    assert "root_extraction" in hum_unit.blocked_paths


# ============================================================================
# Test 3: Open-Class Identification Tests
# ============================================================================

def test_identify_open_class_noun(sample_u5_layer_with_open_class):
    """كِتَابٍ should be identified as OPEN_CLASS_CORE_CANDIDATE."""
    result = mabni_closed_class_6(sample_u5_layer_with_open_class)

    assert result.success
    assert result.layer_object is not None

    kitaab_unit = result.layer_object.units[0]

    assert kitaab_unit.surface == "كِتَابٍ"
    assert kitaab_unit.mabni_classification.mabni_type == MabniClosedClassType.OPEN_CLASS_CORE_CANDIDATE
    assert kitaab_unit.mabni_classification.subtype is None
    assert "root_extraction" not in kitaab_unit.blocked_paths  # Open class REQUIRES root path
    assert "requires_root_weight_path" in kitaab_unit.evidence


# ============================================================================
# Test 4: Path Blocking Tests
# ============================================================================

def test_closed_class_blocks_root_path(sample_u5_layer_with_closed_class):
    """Closed-class units should block root extraction path."""
    result = mabni_closed_class_6(sample_u5_layer_with_closed_class)

    assert result.success

    for unit in result.layer_object.units:
        # All units in this fixture are closed-class
        assert "root_extraction" in unit.blocked_paths
        assert "weight_determination" in unit.blocked_paths


def test_open_class_requires_root_path(sample_u5_layer_with_open_class):
    """Open-class units should NOT block root extraction path."""
    result = mabni_closed_class_6(sample_u5_layer_with_open_class)

    assert result.success

    kitaab_unit = result.layer_object.units[0]
    assert "root_extraction" not in kitaab_unit.blocked_paths
    assert "requires_root_weight_path" in kitaab_unit.evidence


# ============================================================================
# Test 5: Golden Cases
# ============================================================================

def test_golden_case_full_composition(sample_u5_layer_full_composition):
    """
    Golden case: وَبِكِتَابِهِمْ

    Expected classification:
        وَ → CLOSED_CLASS_MABNI_CANDIDATE (HARF_ATF)
        بِ → CLOSED_CLASS_MABNI_CANDIDATE (HARF_JARR)
        كِتَابِ → OPEN_CLASS_CORE_CANDIDATE
        ـهِمْ → ATTACHED_PRONOUN_CLOSED_CLASS
    """
    result = mabni_closed_class_6(sample_u5_layer_full_composition)

    assert result.success
    assert len(result.layer_object.units) == 4

    # وَ - conjunction
    wa_unit = next(u for u in result.layer_object.units if u.surface == "وَ")
    assert wa_unit.mabni_classification.mabni_type == MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE
    assert wa_unit.mabni_classification.subtype == ClosedClassSubtype.HARF_ATF

    # بِ - preposition
    bi_unit = next(u for u in result.layer_object.units if u.surface == "بِ")
    assert bi_unit.mabni_classification.mabni_type == MabniClosedClassType.CLOSED_CLASS_MABNI_CANDIDATE
    assert bi_unit.mabni_classification.subtype == ClosedClassSubtype.HARF_JARR

    # كِتَابِ - open class noun
    kitaab_unit = next(u for u in result.layer_object.units if u.surface == "كِتَابِ")
    assert kitaab_unit.mabni_classification.mabni_type == MabniClosedClassType.OPEN_CLASS_CORE_CANDIDATE

    # ـهِمْ - attached pronoun
    hum_unit = next(u for u in result.layer_object.units if u.surface == "ـهِمْ")
    assert hum_unit.mabni_classification.mabni_type == MabniClosedClassType.ATTACHED_PRONOUN_CLOSED_CLASS


def test_golden_case_path_blocking(sample_u5_layer_full_composition):
    """
    Verify path blocking in golden case.

    Closed-class (وَ، بِ، ـهِمْ) → block root/weight paths
    Open-class (كِتَابِ) → require root/weight paths
    """
    result = mabni_closed_class_6(sample_u5_layer_full_composition)

    wa_unit = next(u for u in result.layer_object.units if u.surface == "وَ")
    bi_unit = next(u for u in result.layer_object.units if u.surface == "بِ")
    kitaab_unit = next(u for u in result.layer_object.units if u.surface == "كِتَابِ")
    hum_unit = next(u for u in result.layer_object.units if u.surface == "ـهِمْ")

    # Closed-class blocks root paths
    assert "root_extraction" in wa_unit.blocked_paths
    assert "root_extraction" in bi_unit.blocked_paths
    assert "root_extraction" in hum_unit.blocked_paths

    # Open-class requires root paths
    assert "root_extraction" not in kitaab_unit.blocked_paths
    assert "requires_root_weight_path" in kitaab_unit.evidence


# ============================================================================
# Test 6: Trace and Evidence Tests
# ============================================================================

def test_trace_preservation(sample_u5_layer_with_closed_class):
    """U₆ must preserve trace to U₅."""
    result = mabni_closed_class_6(sample_u5_layer_with_closed_class)

    assert result.success
    assert result.layer_object.source_functional_role_layer_id == "u5_layer"
    assert "u5_layer" in result.layer_object.trace_5

    for unit in result.layer_object.units:
        assert unit.source_functional_role_unit_id in ["u5_wa", "u5_bi"]


def test_evidence_propagation(sample_u5_layer_with_closed_class):
    """U₆ must build evidence from U₅ and lexicon."""
    result = mabni_closed_class_6(sample_u5_layer_with_closed_class)

    wa_unit = next(u for u in result.layer_object.units if u.surface == "وَ")

    # Should have evidence from classification
    assert len(wa_unit.evidence) > 0
    evidence_str = " ".join(wa_unit.evidence)
    assert "known_particle" in evidence_str or "u5_closed_class_role" in evidence_str


# ============================================================================
# Test 7: Execution Tests
# ============================================================================

def test_execution_without_errors(sample_u5_layer_full_composition):
    """U₆ should execute without errors on valid input."""
    result = mabni_closed_class_6(sample_u5_layer_full_composition)

    assert result.success
    assert result.failure_type is None
    assert result.layer_object is not None


def test_empty_input_handling():
    """U₆ should handle empty input gracefully."""
    empty_layer = FunctionalRoleLayerObject(
        uid="empty",
        units=(),
        source_lafz_layer_id="u4_layer",
        trace_4=("u4_layer",),
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )

    result = mabni_closed_class_6(empty_layer)

    assert not result.success
    assert result.failure_type == MabniClosedClassFailureType.NO_FUNCTIONAL_ROLE_UNITS


# ============================================================================
# Test 8: CPB₆ Proof Tests
# ============================================================================

def test_cpb6_proof_structure(sample_u5_layer_full_composition):
    """CPB₆ should build valid proof structure."""
    result = mabni_closed_class_6(sample_u5_layer_full_composition)

    proof = result.layer_object.proof
    assert proof is not None
    assert proof.claim == "U₆ mabni closed-class paths identified"
    assert proof.scope == "U6_MABNI_CLOSED_CLASS"
    assert "pre_weight_contract_gate" in proof.allowed_next_gates
    assert "root_certificate" in proof.forbidden_next_gates


def test_cpb6_proof_limitations(sample_u5_layer_full_composition):
    """CPB₆ proof should declare limitations."""
    result = mabni_closed_class_6(sample_u5_layer_full_composition)

    proof = result.layer_object.proof
    limitations = proof.limitations

    assert "no_root_extraction" in limitations
    assert "no_weight_determination" in limitations
    assert "no_meaning_assignment" in limitations
    assert "closed_class_blocks_root_path" in limitations
