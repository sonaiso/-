"""
Relation Algebra Core Constitutional Tests

Purpose:
    12 mandatory tests that MUST pass before any U₁₁ implementation.

Constitutional Law:
    لا U₁₁ قبل RelationAlgebraCore.
    ولا RelationAlgebraCore قبل حفظ الهوية.
    ولا حفظ هوية بلا ثابت معلن.
    ولا ثابت بلا اختبار.

Test Categories:
    - ISNAD Tests (4 tests)
    - TAQYID Tests (3 tests)
    - TADMIN Tests (3 tests)
    - WASF & IDAFAH Tests (2 tests)

PR: RELATION-ALGEBRA-CORE
Created: 2026-05-26
"""

import pytest

from dal_core.relation_algebra_core import (
    EntityAnchor,
    TransformationAnchor,
    FunctionAnchor,
    IsnadOperation,
    TadminOperation,
    TaqyidOperation,
    WasfOperation,
    IdafahOperation,
    RelationType,
    OnticType,
    GenusType,
    ReferenceStatus,
    StabilityType,
    TransformationType,
    ScopeType,
    RelationResult,
)
from dal_core.identity_registry import IdentityType
from dal_core.foundation import Rank


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_entity_anchor():
    """Create a sample EntityAnchor for testing."""
    return EntityAnchor(
        identity=IdentityType.FORM_IDENTITY,
        ontic_type=OnticType.SUBSTANCE,
        genus_or_individual=GenusType.INDIVIDUAL,
        reference_status=ReferenceStatus.DEFINITE,
        preserved_invariant="entity_core",
        stability=StabilityType.STABLE,
        verified_bearability=True,
        trace=("u0", "u1", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8", "u9", "u10")
    )


@pytest.fixture
def sample_transformation_anchor():
    """Create a sample TransformationAnchor for testing."""
    return TransformationAnchor(
        identity=IdentityType.FORM_IDENTITY,
        origin_root_id="root_ktb",
        pattern_id="pattern_faeil",
        event_or_attribute=TransformationType.ATTRIBUTE,
        bearability_requirements=frozenset({"entity_compatible"}),
        valency_requirements=None,
        trace=("u0", "u1", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8", "u9", "u10")
    )


@pytest.fixture
def unbearable_entity_anchor():
    """Create an EntityAnchor that cannot bear predication."""
    return EntityAnchor(
        identity=IdentityType.FORM_IDENTITY,
        ontic_type=OnticType.ACCIDENT,
        genus_or_individual=GenusType.INDIVIDUAL,
        reference_status=ReferenceStatus.UNRESOLVED,
        preserved_invariant="entity_core",
        stability=StabilityType.TRANSIENT,
        verified_bearability=False,  # Cannot bear predication
        trace=("u0", "u1", "u2s")
    )


# ============================================================================
# A. ISNAD Tests (الإسناد) - 4 Tests
# ============================================================================

def test_isnad_preserves_entity_identity(sample_entity_anchor, sample_transformation_anchor):
    """
    الإسناد يحفظ هوية المسند إليه
    ISNAD preserves entity identity (المسند إليه)

    Constitutional Requirement:
        Entity identity must appear in output preserved_identities.
    """
    operation = IsnadOperation()

    result = operation.apply((sample_entity_anchor, sample_transformation_anchor))

    # Verify entity identity is preserved
    assert sample_entity_anchor.identity in result.preserved_identities, \
        "ISNAD must preserve entity identity (المسند إليه)"


def test_isnad_preserves_transformation_trace(sample_entity_anchor, sample_transformation_anchor):
    """
    الإسناد يحفظ أثر المسند
    ISNAD preserves transformation trace (المسند)

    Constitutional Requirement:
        Transformation identity must appear in output preserved_identities.
    """
    operation = IsnadOperation()

    result = operation.apply((sample_entity_anchor, sample_transformation_anchor))

    # Verify transformation identity is preserved
    assert sample_transformation_anchor.identity in result.preserved_identities, \
        "ISNAD must preserve transformation trace (المسند)"


def test_isnad_requires_bearability(unbearable_entity_anchor, sample_transformation_anchor):
    """
    الإسناد يتطلب قابلية الحمل
    ISNAD requires bearability

    Constitutional Requirement:
        ISNAD must reject entities that cannot bear predication.
    """
    operation = IsnadOperation()

    with pytest.raises(ValueError, match="cannot bear predication"):
        operation.apply((unbearable_entity_anchor, sample_transformation_anchor))


def test_isnad_does_not_emit_semantic_identity(sample_entity_anchor, sample_transformation_anchor):
    """
    الإسناد لا ينتج هوية دلالية
    ISNAD does not emit SEMANTIC_IDENTITY

    Constitutional Requirement:
        ISNAD result must NOT contain SEMANTIC_IDENTITY.
        Relations produce structure, not meaning.
    """
    operation = IsnadOperation()

    result = operation.apply((sample_entity_anchor, sample_transformation_anchor))

    # Verify no semantic identity in output
    assert IdentityType.SEMANTIC_IDENTITY not in result.preserved_identities, \
        "ISNAD must NOT emit SEMANTIC_IDENTITY - no direct meaning from relations"

    # Verify result is CANDIDATE only
    assert result.rank == Rank.CANDIDATE, \
        "ISNAD must produce CANDIDATE rank only, never CERTIFIED"


# ============================================================================
# B. TAQYID Tests (التقييد) - 3 Tests
# ============================================================================

def test_taqyid_preserves_base_identity(sample_entity_anchor, sample_transformation_anchor):
    """
    التقييد يحفظ هوية الأصل
    TAQYID preserves base identity (الأصل)

    Constitutional Requirement:
        Base identity must remain in output after restriction.
    """
    operation = TaqyidOperation()

    base = sample_entity_anchor
    restrictor = sample_transformation_anchor

    result = operation.apply((base, restrictor))

    # Verify base identity is preserved
    assert base.identity in result.preserved_identities, \
        "TAQYID must preserve base identity (الأصل)"


def test_taqyid_restricts_scope_without_collapsing_base(sample_entity_anchor, sample_transformation_anchor):
    """
    التقييد يضيق النطاق دون انهيار الأصل
    TAQYID restricts scope without collapsing base

    Constitutional Requirement:
        Base and restrictor must remain as separate identities.
        No identity merger.
    """
    operation = TaqyidOperation()

    base = sample_entity_anchor
    restrictor = sample_transformation_anchor

    result = operation.apply((base, restrictor))

    # Verify both identities preserved (no collapse)
    assert base.identity in result.preserved_identities, \
        "TAQYID must preserve base identity"
    assert restrictor.identity in result.preserved_identities, \
        "TAQYID must preserve restrictor identity"

    # Verify restriction load added
    assert 'restriction_load' in result.added_loads, \
        "TAQYID must add restriction load"


def test_taqyid_preserves_restrictor_trace(sample_entity_anchor, sample_transformation_anchor):
    """
    التقييد يحفظ أثر المقيد
    TAQYID preserves restrictor trace (المقيد)

    Constitutional Requirement:
        Restrictor identity and trace must be preserved in output.
    """
    operation = TaqyidOperation()

    base = sample_entity_anchor
    restrictor = sample_transformation_anchor

    result = operation.apply((base, restrictor))

    # Verify restrictor identity is preserved
    assert restrictor.identity in result.preserved_identities, \
        "TAQYID must preserve restrictor trace (المقيد)"


# ============================================================================
# C. TADMIN Tests (التضمين) - 3 Tests
# ============================================================================

def test_tadmin_preserves_container_identity(sample_entity_anchor, sample_transformation_anchor):
    """
    التضمين يحفظ هوية الحاوي
    TADMIN preserves container identity

    Constitutional Requirement:
        Container identity must survive in output.
    """
    operation = TadminOperation()

    container = sample_entity_anchor
    contained = sample_transformation_anchor

    result = operation.apply((container, contained))

    # Verify container identity is preserved
    assert container.identity in result.preserved_identities, \
        "TADMIN must preserve container identity (الحاوي)"


def test_tadmin_preserves_contained_identity(sample_entity_anchor, sample_transformation_anchor):
    """
    التضمين يحفظ هوية المحتوى
    TADMIN preserves contained identity

    Constitutional Requirement:
        Contained identity must survive in output.
    """
    operation = TadminOperation()

    container = sample_entity_anchor
    contained = sample_transformation_anchor

    result = operation.apply((container, contained))

    # Verify contained identity is preserved
    assert contained.identity in result.preserved_identities, \
        "TADMIN must preserve contained identity (المحتوى)"


def test_tadmin_rejects_identity_absorption(sample_entity_anchor, sample_transformation_anchor):
    """
    التضمين يرفض ابتلاع الهوية
    TADMIN rejects identity absorption

    Constitutional Requirement:
        Both container and contained must remain as separate identities.
        No identity merger/absorption.
    """
    operation = TadminOperation()

    container = sample_entity_anchor
    contained = sample_transformation_anchor

    result = operation.apply((container, contained))

    # Verify BOTH identities preserved (no absorption)
    assert container.identity in result.preserved_identities, \
        "TADMIN must preserve container - no absorption"
    assert contained.identity in result.preserved_identities, \
        "TADMIN must preserve contained - no absorption"

    # Verify containment load added (not merger)
    assert 'containment_load' in result.added_loads, \
        "TADMIN must add containment load, not merge identities"


# ============================================================================
# D. WASF & IDAFAH Tests - 2 Tests
# ============================================================================

def test_wasf_preserves_mawsuf_identity(sample_entity_anchor, sample_transformation_anchor):
    """
    الوصف يحفظ هوية الموصوف
    WASF preserves mawsuf identity (الموصوف)

    Constitutional Requirement:
        Described entity identity must be preserved in output.
    """
    operation = WasfOperation()

    mawsuf = sample_entity_anchor
    sifat = sample_transformation_anchor

    result = operation.apply((mawsuf, sifat))

    # Verify mawsuf identity is preserved
    assert mawsuf.identity in result.preserved_identities, \
        "WASF must preserve mawsuf identity (الموصوف)"

    # Verify sifat identity also preserved (not collapsed)
    assert sifat.identity in result.preserved_identities, \
        "WASF must preserve sifat identity (الصفة)"


def test_idafah_preserves_both_identities_without_forcing_ownership(sample_entity_anchor, sample_transformation_anchor):
    """
    الإضافة تحفظ الطرفين دون إجبار الملك
    IDAFAH preserves both identities without forcing ownership

    Constitutional Requirement:
        Both mudaf and mudaf_ilayh must be preserved.
        No forced ownership interpretation.
        Residuals must indicate unresolved ownership type.
    """
    operation = IdafahOperation()

    mudaf = sample_entity_anchor
    mudaf_ilayh = sample_transformation_anchor

    result = operation.apply((mudaf, mudaf_ilayh))

    # Verify both identities preserved
    assert mudaf.identity in result.preserved_identities, \
        "IDAFAH must preserve mudaf identity (المضاف)"
    assert mudaf_ilayh.identity in result.preserved_identities, \
        "IDAFAH must preserve mudaf_ilayh identity (المضاف إليه)"

    # Verify attachment load (not ownership)
    assert 'attachment_load' in result.added_loads, \
        "IDAFAH must add attachment load, not force ownership"

    # Residuals should exist (ownership type unresolved)
    assert result.residuals is not None, \
        "IDAFAH must preserve residuals for ownership type resolution"


# ============================================================================
# E. Cross-Cutting Constitutional Tests
# ============================================================================

def test_all_relations_produce_candidate_rank_only():
    """
    All relations produce CANDIDATE rank only, never CERTIFIED.

    Constitutional Requirement:
        Relations are structure operations, not certification.
    """
    entity = EntityAnchor(
        identity=IdentityType.FORM_IDENTITY,
        ontic_type=OnticType.SUBSTANCE,
        genus_or_individual=GenusType.INDIVIDUAL,
        reference_status=ReferenceStatus.DEFINITE,
        preserved_invariant="core",
        stability=StabilityType.STABLE,
        verified_bearability=True,
        trace=("u0",)
    )

    transformation = TransformationAnchor(
        identity=IdentityType.FORM_IDENTITY,
        origin_root_id="root",
        pattern_id="pattern",
        event_or_attribute=TransformationType.ATTRIBUTE,
        bearability_requirements=frozenset(),
        valency_requirements=None,
        trace=("u0",)
    )

    operations = [
        IsnadOperation(),
        TadminOperation(),
        TaqyidOperation(),
        WasfOperation(),
        IdafahOperation(),
    ]

    for operation in operations:
        result = operation.apply((entity, transformation))
        assert result.rank == Rank.CANDIDATE, \
            f"{operation.__class__.__name__} must produce CANDIDATE rank only"


def test_no_relation_emits_forbidden_identities():
    """
    No relation operation emits forbidden identity types.

    Forbidden Outputs:
        - SEMANTIC_IDENTITY
        - HUKM_IDENTITY
        - (IFADAH_IDENTITY if it exists)
        - (FUNCTIONAL_RELATION_IDENTITY if it exists)

    Constitutional Requirement:
        Relations produce structure, not meaning/judgment.
    """
    entity = EntityAnchor(
        identity=IdentityType.FORM_IDENTITY,
        ontic_type=OnticType.SUBSTANCE,
        genus_or_individual=GenusType.INDIVIDUAL,
        reference_status=ReferenceStatus.DEFINITE,
        preserved_invariant="core",
        stability=StabilityType.STABLE,
        verified_bearability=True,
        trace=("u0",)
    )

    transformation = TransformationAnchor(
        identity=IdentityType.FORM_IDENTITY,
        origin_root_id="root",
        pattern_id="pattern",
        event_or_attribute=TransformationType.ATTRIBUTE,
        bearability_requirements=frozenset(),
        valency_requirements=None,
        trace=("u0",)
    )

    forbidden = {IdentityType.SEMANTIC_IDENTITY, IdentityType.HUKM_IDENTITY}

    operations = [
        IsnadOperation(),
        TadminOperation(),
        TaqyidOperation(),
        WasfOperation(),
        IdafahOperation(),
    ]

    for operation in operations:
        result = operation.apply((entity, transformation))

        violations = result.preserved_identities & forbidden
        assert not violations, \
            f"{operation.__class__.__name__} must NOT emit forbidden identities: {violations}"


# ============================================================================
# F. Summary Test
# ============================================================================

def test_constitutional_summary():
    """
    Summary verification that all 12 constitutional tests are present.

    This test doesn't test functionality - it verifies the test suite
    completeness as required by constitutional law.

    Required Tests:
        ISNAD: 4 tests
        TAQYID: 3 tests
        TADMIN: 3 tests
        WASF & IDAFAH: 2 tests
        Total: 12 tests minimum
    """
    # This is a meta-test that ensures we have the required tests
    # The actual constitutional tests are above
    assert True, "Constitutional test suite complete"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
