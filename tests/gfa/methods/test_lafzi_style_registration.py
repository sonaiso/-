"""
Tests for LafziMadlul Registration as Governed Style

Critical Law:
    Registration is NOT execution.
    Registration is governance verification ONLY.

Test Coverage (14 Required Tests):
    1. test_lafzi_registration_requires_style_spec
    2. test_lafzi_registration_requires_lafzi_dalali_domain
    3. test_lafzi_registration_rejects_material_experimental_domain
    4. test_lafzi_registration_rejects_formal_logical_domain
    5. test_lafzi_registration_requires_neutral_binding
    6. test_lafzi_registration_requires_prior_information
    7. test_lafzi_registration_excludes_prior_opinion
    8. test_lafzi_registration_does_not_create_meaning
    9. test_lafzi_registration_does_not_issue_hukm
    10. test_lafzi_registration_does_not_raise_predicate_rank
    11. test_lafzi_registration_does_not_implement_dal
    12. test_lafzi_registration_does_not_implement_madlul
    13. test_lafzi_registration_does_not_implement_dalalah
    14. test_lafzi_registration_returns_governed_failure_not_exception
"""

import pytest
from uuid import uuid4

from gfa.methods.rational import (
    NeutralBindingInput,
    PriorInformation,
    PriorOpinion,
    AqlOperationInput,
    FilteredPrior,
)
from gfa.methods.styles import (
    make_lafzi_dalali_style,
    make_material_experimental_style,
    make_formal_logical_style,
    ThinkingDomain,
)
from gfa.methods.lafzi_registration import (
    LafziStyleRegistration,
    LafziRegistrationResult,
    LafziRegistrationFailure,
    LafziGovernanceContract,
    LafziRegistrationFailureKind,
)


# Test fixtures

@pytest.fixture
def valid_prior_information():
    """Create valid PriorInformation."""
    return PriorInformation(
        content="لغة عربية",
        domain="lafzi_dalali",
        rank="LICENSED",
        evidence_trace="معجم لغوي",
        trace_id=uuid4().hex,
    )


@pytest.fixture
def invalid_prior_opinion():
    """Create PriorOpinion (invalid for LafziMadlul)."""
    return PriorOpinion(
        content="رأي شخصي",
        opinion_type="bias",
        contamination_risk="predetermined_conclusion",
        trace_id=uuid4().hex,
    )


@pytest.fixture
def valid_aql_input(valid_prior_information):
    """Create valid AqlOperationInput with PriorInformation."""
    # Use placeholder strings like in existing tests
    return AqlOperationInput(
        reality="test_reality",
        sensory_transfer="test_sensory",
        cognitive_carrier="test_carrier",
        filtered_prior=FilteredPrior(
            information=frozenset([valid_prior_information]),
            excluded_opinions=frozenset(),
        ),
    )


@pytest.fixture
def aql_input_with_opinion(invalid_prior_opinion):
    """Create AqlOperationInput with PriorOpinion (invalid)."""
    return AqlOperationInput(
        reality="test_reality",
        sensory_transfer="test_sensory",
        cognitive_carrier="test_carrier",
        filtered_prior=FilteredPrior(
            information=frozenset(),
            excluded_opinions=frozenset([invalid_prior_opinion]),
        ),
    )


@pytest.fixture
def valid_neutral_binding_input(valid_aql_input):
    """Create valid NeutralBindingInput."""
    return NeutralBindingInput(
        aql_input=valid_aql_input,
        trace_id=uuid4().hex,
        residuals=(),
    )


@pytest.fixture
def neutral_binding_with_opinion(aql_input_with_opinion):
    """Create NeutralBindingInput with PriorOpinion."""
    return NeutralBindingInput(
        aql_input=aql_input_with_opinion,
        trace_id=uuid4().hex,
        residuals=(),
    )


@pytest.fixture
def lafzi_style_spec():
    """Create LAFZI_DALALI StyleSpec."""
    return make_lafzi_dalali_style()


@pytest.fixture
def material_style_spec():
    """Create MATERIAL_EXPERIMENTAL StyleSpec."""
    return make_material_experimental_style()


@pytest.fixture
def formal_style_spec():
    """Create FORMAL_LOGICAL StyleSpec."""
    return make_formal_logical_style()


# Test 1: Requires StyleSpec

def test_lafzi_registration_requires_style_spec(valid_neutral_binding_input):
    """
    Test Law 1: No LafziMadlul without StyleSpec.

    Registration must fail if StyleSpec is None.
    """
    result = LafziStyleRegistration.register(
        style_spec=None,
        neutral_binding_input=valid_neutral_binding_input,
    )

    assert result.is_failure()
    assert not result.is_success()
    assert result.failure is not None
    assert "Missing StyleSpec" in result.get_violations()

    # Verify residual
    assert len(result.failure.residuals) > 0
    assert any(
        r.kind == LafziRegistrationFailureKind.MISSING_STYLE_SPEC
        for r in result.failure.residuals
    )


# Test 2: Requires LAFZI_DALALI domain

def test_lafzi_registration_requires_lafzi_dalali_domain(
    lafzi_style_spec,
    valid_neutral_binding_input,
):
    """
    Test Law 2: No LafziMadlul unless domain = LAFZI_DALALI.

    Registration must succeed with LAFZI_DALALI domain.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    assert result.is_success()
    assert not result.is_failure()
    assert result.governance_contract is not None
    assert result.governance_contract.requires_lafzi_dalali_domain()
    assert result.governance_contract.get_domain() == ThinkingDomain.LAFZI_DALALI


# Test 3: Rejects MATERIAL_EXPERIMENTAL domain

def test_lafzi_registration_rejects_material_experimental_domain(
    material_style_spec,
    valid_neutral_binding_input,
):
    """
    Test Law 3: No LafziMadlul with MATERIAL_EXPERIMENTAL domain.

    Registration must fail with MATERIAL_EXPERIMENTAL domain.
    """
    result = LafziStyleRegistration.register(
        style_spec=material_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    assert result.is_failure()
    assert not result.is_success()
    assert result.failure is not None
    assert any(
        "MATERIAL_EXPERIMENTAL" in v
        for v in result.get_violations()
    )

    # Verify residual
    assert any(
        r.kind == LafziRegistrationFailureKind.MATERIAL_DOMAIN_REJECTED
        for r in result.failure.residuals
    )


# Test 4: Rejects FORMAL_LOGICAL domain

def test_lafzi_registration_rejects_formal_logical_domain(
    formal_style_spec,
    valid_neutral_binding_input,
):
    """
    Test Law 4: No LafziMadlul with FORMAL_LOGICAL domain.

    Registration must fail with FORMAL_LOGICAL domain.
    """
    result = LafziStyleRegistration.register(
        style_spec=formal_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    assert result.is_failure()
    assert not result.is_success()
    assert result.failure is not None
    assert any(
        "FORMAL_LOGICAL" in v
        for v in result.get_violations()
    )

    # Verify residual
    assert any(
        r.kind == LafziRegistrationFailureKind.FORMAL_DOMAIN_REJECTED
        for r in result.failure.residuals
    )


# Test 5: Requires NeutralBinding

def test_lafzi_registration_requires_neutral_binding(lafzi_style_spec):
    """
    Test Law 5: No LafziMadlul without NeutralBinding.

    Registration must fail if NeutralBindingInput is None.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=None,
    )

    assert result.is_failure()
    assert not result.is_success()
    assert result.failure is not None
    assert "Missing NeutralBindingInput" in result.get_violations()

    # Verify residual
    assert any(
        r.kind == LafziRegistrationFailureKind.MISSING_NEUTRAL_BINDING
        for r in result.failure.residuals
    )


# Test 6: Requires PriorInformation

def test_lafzi_registration_requires_prior_information(
    lafzi_style_spec,
    valid_neutral_binding_input,
):
    """
    Test Law 6: No LafziMadlul without PriorInformation.

    This test verifies registration succeeds with valid PriorInformation.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    assert result.is_success()
    assert result.governance_contract is not None
    assert result.governance_contract.requires_prior_information()


# Test 7: Excludes PriorOpinion

def test_lafzi_registration_excludes_prior_opinion(
    lafzi_style_spec,
    neutral_binding_with_opinion,
):
    """
    Test Law 7: No LafziMadlul with PriorOpinion.

    Registration must fail if PriorOpinion is present.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=neutral_binding_with_opinion,
    )

    assert result.is_failure()
    assert result.failure is not None
    assert any(
        "PriorOpinion" in v
        for v in result.get_violations()
    )

    # Verify residual
    assert any(
        r.kind == LafziRegistrationFailureKind.PRIOR_OPINION_PRESENT
        for r in result.failure.residuals
    )


# Test 8: Does NOT create meaning

def test_lafzi_registration_does_not_create_meaning(
    lafzi_style_spec,
    valid_neutral_binding_input,
):
    """
    Test: Registration does NOT create meaning.

    Registration is governance gate, not semantic execution.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    # Registration result does not create meaning
    assert result.does_not_create_meaning()

    # If success, governance contract also does not create meaning
    if result.is_success():
        assert result.governance_contract.does_not_create_meaning()

    # Static method also confirms
    assert LafziStyleRegistration.does_not_implement_dal()


# Test 9: Does NOT issue HUKM

def test_lafzi_registration_does_not_issue_hukm(
    lafzi_style_spec,
    valid_neutral_binding_input,
):
    """
    Test: Registration does NOT issue HUKM.

    Registration is governance gate, not judgment.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    # Registration result does not issue HUKM
    assert result.does_not_issue_hukm()

    # If success, governance contract also does not issue HUKM
    if result.is_success():
        assert result.governance_contract.does_not_issue_hukm()


# Test 10: Does NOT raise PredicateRank

def test_lafzi_registration_does_not_raise_predicate_rank(
    lafzi_style_spec,
    valid_neutral_binding_input,
):
    """
    Test: Registration does NOT raise PredicateRank.

    Registration preserves rank, does not certify claims.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    # Registration result does not raise rank
    assert result.does_not_raise_predicate_rank()

    # If success, governance contract also does not raise rank
    if result.is_success():
        assert result.governance_contract.does_not_raise_predicate_rank()
        assert result.governance_contract.preserves_rank()


# Test 11: Does NOT implement Dal

def test_lafzi_registration_does_not_implement_dal(
    lafzi_style_spec,
    valid_neutral_binding_input,
):
    """
    Test: Registration does NOT implement Dal (الدال).

    Dal implementation is future work (PR-L2).
    This PR only registers governance.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    # Registration result does not implement Dal
    assert result.does_not_implement_dal()

    # If success, governance contract also does not implement Dal
    if result.is_success():
        assert result.governance_contract.does_not_implement_dal()

    # Static method confirms
    assert LafziStyleRegistration.does_not_implement_dal()


# Test 12: Does NOT implement Madlul

def test_lafzi_registration_does_not_implement_madlul(
    lafzi_style_spec,
    valid_neutral_binding_input,
):
    """
    Test: Registration does NOT implement Madlul (المدلول).

    Madlul implementation is future work (PR-L3).
    This PR only registers governance.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    # Registration result does not implement Madlul
    assert result.does_not_implement_madlul()

    # If success, governance contract also does not implement Madlul
    if result.is_success():
        assert result.governance_contract.does_not_implement_madlul()

    # Static method confirms
    assert LafziStyleRegistration.does_not_implement_madlul()


# Test 13: Does NOT implement Dalalah

def test_lafzi_registration_does_not_implement_dalalah(
    lafzi_style_spec,
    valid_neutral_binding_input,
):
    """
    Test: Registration does NOT implement Dalalah (الدلالة).

    Dalalah implementation is future work (PR-L4).
    This PR only registers governance.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    # Registration result does not implement Dalalah
    assert result.does_not_implement_dalalah()

    # If success, governance contract also does not implement Dalalah
    if result.is_success():
        assert result.governance_contract.does_not_implement_dalalah()

    # Static method confirms
    assert LafziStyleRegistration.does_not_implement_dalalah()


# Test 14: Returns governed failure, not exception

def test_lafzi_registration_returns_governed_failure_not_exception(
    lafzi_style_spec,
):
    """
    Test: Registration returns governed failures, not bare exceptions.

    All failures must be typed LafziRegistrationFailure objects.
    No bare exceptions should be raised.
    """
    # Test with None input (should return governed failure, not raise exception)
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=None,
    )

    # Should return result, not raise exception
    assert isinstance(result, LafziRegistrationResult)
    assert result.is_failure()
    assert isinstance(result.failure, LafziRegistrationFailure)

    # Failure has typed residuals
    assert len(result.failure.residuals) > 0
    for residual in result.failure.residuals:
        assert hasattr(residual, 'kind')
        assert hasattr(residual, 'reason')
        assert hasattr(residual, 'violated_law')

    # Failure has trace
    assert result.failure.trace_id is not None

    # Failure has violations
    assert len(result.failure.violations) > 0


# Additional integration test: Full success path

def test_lafzi_registration_full_success_path(
    lafzi_style_spec,
    valid_neutral_binding_input,
):
    """
    Integration test: Full successful registration.

    Verifies all governance requirements satisfied.
    """
    result = LafziStyleRegistration.register(
        style_spec=lafzi_style_spec,
        neutral_binding_input=valid_neutral_binding_input,
    )

    # Success
    assert result.is_success()
    assert not result.is_failure()
    assert result.failure is None

    # Governance contract created and valid
    assert result.governance_contract is not None
    contract = result.governance_contract

    # All 10 laws satisfied
    assert contract.requires_style_spec()
    assert contract.requires_lafzi_dalali_domain()
    assert contract.rejects_material_experimental_domain()
    assert contract.rejects_formal_logical_domain()
    assert contract.requires_neutral_binding()
    assert contract.requires_prior_information()
    assert contract.excludes_prior_opinion()
    assert contract.preserves_trace()
    assert contract.preserves_residuals()
    assert contract.preserves_rank()

    # Overall validity
    assert contract.is_valid()
    assert len(contract.get_violations()) == 0

    # Does not implement execution
    assert contract.does_not_create_meaning()
    assert contract.does_not_issue_hukm()
    assert contract.does_not_raise_predicate_rank()
    assert contract.does_not_implement_dal()
    assert contract.does_not_implement_madlul()
    assert contract.does_not_implement_dalalah()

    # Result also confirms no execution
    assert result.does_not_create_meaning()
    assert result.does_not_issue_hukm()
    assert result.does_not_raise_predicate_rank()
    assert result.does_not_implement_dal()
    assert result.does_not_implement_madlul()
    assert result.does_not_implement_dalalah()
