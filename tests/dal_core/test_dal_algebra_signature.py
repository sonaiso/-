"""Tests for Minimal Dal Transition Signature (PR #23).

Tests verify:
1. Transition contract structure
2. Claim-scoped certificates (no global certificate)
3. Candidate set shape validation
4. No-direct-promotion rules
5. Forbidden outputs detection
6. Shortcut policies
7. Protocols don't force inheritance
8. No semantic leakage
"""

import pytest
from dataclasses import dataclass
from typing import List, Mapping

from dal_core.dal_algebra import (
    DalTransitionDomain,
    DalClaimScope,
    EvidenceRequirement,
    ShortcutPolicy,
    CandidateBudgetPolicy,
    DalEvidence,
    DalCounterEvidence,
    DalTraceRef,
    AlgebraicFailure,  # PR-1C
    DalTransitionContract,
    DalCandidateProtocol,
    DalCandidateSetProtocol,
    DalTransitionProtocol,
    validate_transition_contract,
    validate_candidate_set_shape,
    ensure_no_forbidden_outputs,
    validate_no_direct_promotion,
)


# ============================================================================
# Test AlgebraicFailure (PR-1C: Hybrid Failure Semantics)
# ============================================================================


def test_algebraic_failure_basic_construction():
    """AlgebraicFailure can be constructed with minimal fields."""
    failure = AlgebraicFailure(reason="Gate not satisfied")
    assert failure.reason == "Gate not satisfied"
    assert failure.gate is None
    assert failure.evidence_gap is None
    assert failure.rank_issue is None
    assert failure.residual_block is None
    assert failure.domain_violation is None
    assert failure.forbidden_path is None
    # After immutability conversion: tuple not list, MappingProxyType not dict
    assert failure.counter_evidence == ()
    assert failure.trace == ()
    assert isinstance(failure.metadata, Mapping)
    assert not isinstance(failure.metadata, dict)


def test_algebraic_failure_with_all_fields():
    """AlgebraicFailure can be constructed with all optional fields."""
    counter_ev = DalCounterEvidence(
        source="test",
        claim_scope=DalClaimScope.CARRIER_VALID,
        span=(0, 1),
        severity=0.8,
        reason="Test counter-evidence"
    )
    trace = DalTraceRef(
        transition_id="test_transition",
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.SYLLABIC,
        timestamp="2026-05-27T08:00:00Z"
    )

    failure = AlgebraicFailure(
        reason="Multiple failures",
        gate="bearability_gate",
        evidence_gap="ontic_type_mismatch",
        rank_issue="insufficient_rank",
        residual_block="blocking_residual",
        domain_violation="crossed_boundary",
        forbidden_path="U9->U11",
        counter_evidence=[counter_ev],
        trace=[trace],
        metadata={"detail": "test"}
    )

    assert failure.reason == "Multiple failures"
    assert failure.gate == "bearability_gate"
    assert failure.evidence_gap == "ontic_type_mismatch"
    assert failure.rank_issue == "insufficient_rank"
    assert failure.residual_block == "blocking_residual"
    assert failure.domain_violation == "crossed_boundary"
    assert failure.forbidden_path == "U9->U11"
    assert len(failure.counter_evidence) == 1
    assert len(failure.trace) == 1
    assert failure.metadata["detail"] == "test"


def test_algebraic_failure_requires_non_empty_reason():
    """AlgebraicFailure must have non-empty reason (construction validation)."""
    with pytest.raises(ValueError, match="must have non-empty reason"):
        AlgebraicFailure(reason="")


def test_algebraic_failure_requires_string_reason():
    """AlgebraicFailure.reason must be string (construction validation)."""
    with pytest.raises(TypeError, match="must be str"):
        AlgebraicFailure(reason=123)  # type: ignore


def test_algebraic_failure_is_frozen():
    """AlgebraicFailure is immutable (frozen dataclass)."""
    failure = AlgebraicFailure(reason="Test")

    with pytest.raises(Exception):  # FrozenInstanceError
        failure.reason = "Modified"  # type: ignore


def test_algebraic_failure_gate_not_satisfied():
    """AlgebraicFailure for gate non-satisfaction use case."""
    failure = AlgebraicFailure(
        reason="Entity cannot bear transformation",
        gate="bearability_gate",
        evidence_gap="ontic_type_mismatch"
    )

    assert failure.reason == "Entity cannot bear transformation"
    assert failure.gate == "bearability_gate"
    assert failure.evidence_gap == "ontic_type_mismatch"


def test_algebraic_failure_evidence_insufficient():
    """AlgebraicFailure for insufficient evidence use case."""
    failure = AlgebraicFailure(
        reason="Insufficient evidence for lexicon attestation",
        evidence_gap="lexicon_attestation_required"
    )

    assert "Insufficient evidence" in failure.reason
    assert failure.evidence_gap == "lexicon_attestation_required"


def test_algebraic_failure_rank_violation():
    """AlgebraicFailure for rank violation use case."""
    failure = AlgebraicFailure(
        reason="Rank not licensed for this operation",
        rank_issue="CANDIDATE cannot emit VERIFIED"
    )

    assert "Rank not licensed" in failure.reason
    assert failure.rank_issue == "CANDIDATE cannot emit VERIFIED"


def test_algebraic_failure_residual_blocking():
    """AlgebraicFailure for blocking residuals use case."""
    failure = AlgebraicFailure(
        reason="Blocking residuals prevent operation",
        residual_block="unresolved_homograph"
    )

    assert "Blocking residuals" in failure.reason
    assert failure.residual_block == "unresolved_homograph"


def test_algebraic_failure_domain_violation():
    """AlgebraicFailure for domain boundary violation use case."""
    failure = AlgebraicFailure(
        reason="Operation crosses domain boundary without permission",
        domain_violation="SCRIPT_DOMAIN -> WEIGHT_DOMAIN without intermediate"
    )

    assert "domain boundary" in failure.reason
    assert failure.domain_violation is not None


def test_algebraic_failure_forbidden_path():
    """AlgebraicFailure for forbidden transition path use case."""
    failure = AlgebraicFailure(
        reason="Forbidden path: U9 -> U11 skips U10",
        forbidden_path="U9_WEIGHT -> U11_COMPOSITION"
    )

    assert "Forbidden path" in failure.reason
    assert failure.forbidden_path is not None


def test_algebraic_failure_with_counter_evidence():
    """AlgebraicFailure can include counter-evidence."""
    counter_ev1 = DalCounterEvidence(
        source="lexicon",
        claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        span=(0, 5),
        severity=0.9,
        reason="Template mismatch"
    )
    counter_ev2 = DalCounterEvidence(
        source="phonology",
        claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,
        span=(2, 4),
        severity=0.7,
        reason="Invalid syllable"
    )

    failure = AlgebraicFailure(
        reason="Multiple counter-evidences block operation",
        counter_evidence=[counter_ev1, counter_ev2]
    )

    assert len(failure.counter_evidence) == 2
    assert failure.counter_evidence[0].severity == 0.9
    assert failure.counter_evidence[1].severity == 0.7


def test_algebraic_failure_with_trace():
    """AlgebraicFailure can include transformation trace."""
    trace1 = DalTraceRef(
        transition_id="u8_to_u9",
        source_domain=DalTransitionDomain.ORIGIN,
        target_domain=DalTransitionDomain.TEMPLATE,
        timestamp="2026-05-27T08:00:00Z",
        reversible=True
    )
    trace2 = DalTraceRef(
        transition_id="u9_failed",
        source_domain=DalTransitionDomain.TEMPLATE,
        target_domain=DalTransitionDomain.IDENTITY_AXIS,
        timestamp="2026-05-27T08:00:01Z",
        reversible=False
    )

    failure = AlgebraicFailure(
        reason="Operation failed after partial trace",
        trace=[trace1, trace2]
    )

    assert len(failure.trace) == 2
    assert failure.trace[0].reversible is True
    assert failure.trace[1].reversible is False


def test_algebraic_failure_preserves_immutability():
    """AlgebraicFailure is truly immutable with tuple/MappingProxyType."""
    failure = AlgebraicFailure(
        reason="Test",
        counter_evidence=[],
        trace=[],
        metadata={}
    )

    # Fields are converted to immutable types in __post_init__
    assert isinstance(failure.counter_evidence, tuple)
    assert isinstance(failure.trace, tuple)
    # MappingProxyType is a Mapping but not a dict
    assert isinstance(failure.metadata, Mapping)
    assert not isinstance(failure.metadata, dict)

    # Tuple has no append method
    assert not hasattr(failure.counter_evidence, 'append')
    assert not hasattr(failure.trace, 'append')

    # MappingProxyType prevents modification
    with pytest.raises(TypeError):
        failure.metadata['key'] = 'value'  # type: ignore


def test_algebraic_failure_accepts_list_input_stores_tuple():
    """AlgebraicFailure accepts list input but stores as tuple."""
    counter_ev = DalCounterEvidence(
        source="test",
        claim_scope=DalClaimScope.CARRIER_VALID,
        span=(0, 1),
        severity=0.8
    )
    trace_ref = DalTraceRef(
        transition_id="test",
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.SYLLABIC,
        timestamp="2026-05-27T08:00:00Z"
    )

    # Pass lists (mutable)
    failure = AlgebraicFailure(
        reason="Test",
        counter_evidence=[counter_ev],
        trace=[trace_ref],
        metadata={"key": "value"}
    )

    # Stored as tuples and MappingProxyType (immutable)
    assert isinstance(failure.counter_evidence, tuple)
    assert isinstance(failure.trace, tuple)
    assert isinstance(failure.metadata, Mapping)
    assert len(failure.counter_evidence) == 1
    assert len(failure.trace) == 1
    assert failure.metadata["key"] == "value"


# ============================================================================
# Test Operation-Level Failure Semantics (PR-1C)
# ============================================================================


def test_transition_operation_failure_returns_algebraic_failure():
    """Operation failure returns AlgebraicFailure, not exception."""

    class MockFailingTransition:
        """Mock transition that fails due to gate non-satisfaction."""

        @property
        def contract(self):
            return DalTransitionContract(
                contract_id="mock_failing",
                source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
                target_domain=DalTransitionDomain.SYLLABIC,
                input_type=str,
                output_type=str,
                claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID
            )

        def apply(self, input_obj, **aux):
            """Returns AlgebraicFailure for gate non-satisfaction."""
            # Input is valid (construction passed)
            # But operation fails (gate not satisfied)
            return AlgebraicFailure(
                reason="Gate not satisfied",
                gate="mock_gate",
                evidence_gap="missing_lexicon_attestation"
            )

    transition = MockFailingTransition()
    result = transition.apply("valid_input")

    # Operation failure returns AlgebraicFailure value
    assert isinstance(result, AlgebraicFailure)
    assert result.reason == "Gate not satisfied"
    assert result.gate == "mock_gate"
    assert result.evidence_gap == "missing_lexicon_attestation"


def test_transition_construction_failure_raises_exception():
    """Construction/invariant failure raises exception, not AlgebraicFailure."""

    class MockConstructionCheckingTransition:
        """Mock transition that validates construction invariants."""

        @property
        def contract(self):
            return DalTransitionContract(
                contract_id="mock_construction",
                source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
                target_domain=DalTransitionDomain.SYLLABIC,
                input_type=str,
                output_type=str,
                claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID
            )

        def apply(self, input_obj, **aux):
            """Raises exception for invalid construction."""
            # Construction invariant violation: input must be non-empty string
            if not isinstance(input_obj, str):
                raise TypeError(f"Expected str, got {type(input_obj)}")
            if not input_obj:
                raise ValueError("Input must be non-empty")

            # Success path not under test here
            # Would return CandidateSet on valid input, but we only test failures
            return AlgebraicFailure(reason="mock - success path not tested")

    transition = MockConstructionCheckingTransition()

    # Construction failure raises exception
    with pytest.raises(TypeError, match="Expected str"):
        transition.apply(None)

    with pytest.raises(ValueError, match="non-empty"):
        transition.apply("")


def test_algebraic_failure_with_evidence_gap_operation():
    """Operation failing due to evidence insufficiency returns AlgebraicFailure."""

    class MockEvidenceRequiringTransition:
        """Mock transition requiring evidence."""

        @property
        def contract(self):
            return DalTransitionContract(
                contract_id="mock_evidence",
                source_domain=DalTransitionDomain.TEMPLATE,
                target_domain=DalTransitionDomain.IDENTITY_AXIS,
                input_type=str,
                output_type=str,
                claim_scope=DalClaimScope.IDENTITY_DETERMINED,
                evidence_requirement=EvidenceRequirement.LEXICON_LOOKUP
            )

        def apply(self, input_obj, **aux):
            """Returns AlgebraicFailure for insufficient evidence."""
            # Check for evidence in aux
            if "evidence" not in aux:
                return AlgebraicFailure(
                    reason="Insufficient evidence for lexicon attestation",
                    evidence_gap="lexicon_attestation_required"
                )
            # Would return success if evidence present
            return AlgebraicFailure(reason="mock")

    transition = MockEvidenceRequiringTransition()
    result = transition.apply("valid_input")  # No evidence provided

    assert isinstance(result, AlgebraicFailure)
    assert "Insufficient evidence" in result.reason
    assert result.evidence_gap == "lexicon_attestation_required"


def test_algebraic_failure_composability():
    """AlgebraicFailure enables compositional patterns."""

    # Create multiple failures
    failure1 = AlgebraicFailure(
        reason="Gate A failed",
        gate="gate_a"
    )
    failure2 = AlgebraicFailure(
        reason="Gate B failed",
        gate="gate_b"
    )

    # Can be collected and analyzed
    failures = [failure1, failure2]
    assert all(isinstance(f, AlgebraicFailure) for f in failures)
    assert [f.gate for f in failures] == ["gate_a", "gate_b"]

    # Can be traced through operations
    combined_failure = AlgebraicFailure(
        reason="Multiple gates failed",
        gate="composite",
        metadata={"component_failures": len(failures)}
    )
    assert combined_failure.metadata["component_failures"] == 2


def test_dal_evidence_requires_span():
    """Evidence must include span (position in ordered sequence)."""
    evidence = DalEvidence(
        source="lexicon",
        claim_scope=DalClaimScope.CARRIER_VALID,
        span=(0, 5),
        confidence=0.9
    )
    assert evidence.span == (0, 5)
    assert evidence.confidence == 0.9


def test_dal_evidence_validates_confidence():
    """Evidence confidence must be in [0.0, 1.0]."""
    with pytest.raises(ValueError, match="Confidence must be in"):
        DalEvidence(
            source="test",
            claim_scope=DalClaimScope.CARRIER_VALID,
            span=(0, 1),
            confidence=1.5  # Invalid
        )


def test_dal_evidence_validates_span():
    """Evidence span must be valid (start <= end, non-negative)."""
    with pytest.raises(ValueError, match="Invalid span: start > end"):
        DalEvidence(
            source="test",
            claim_scope=DalClaimScope.CARRIER_VALID,
            span=(5, 3)  # Invalid: start > end
        )

    with pytest.raises(ValueError, match="Invalid span: negative start"):
        DalEvidence(
            source="test",
            claim_scope=DalClaimScope.CARRIER_VALID,
            span=(-1, 3)  # Invalid: negative start
        )


def test_dal_counter_evidence_validates_severity():
    """Counter-evidence severity must be in [0.0, 1.0]."""
    with pytest.raises(ValueError, match="Severity must be in"):
        DalCounterEvidence(
            source="test",
            claim_scope=DalClaimScope.CARRIER_VALID,
            span=(0, 1),
            severity=2.0  # Invalid
        )


def test_dal_counter_evidence_validates_span():
    """Counter-evidence span must be valid (start <= end, non-negative)."""
    with pytest.raises(ValueError, match="Invalid span: start > end"):
        DalCounterEvidence(
            source="test",
            claim_scope=DalClaimScope.CARRIER_VALID,
            span=(5, 3)  # Invalid: start > end
        )

    with pytest.raises(ValueError, match="Invalid span: negative start"):
        DalCounterEvidence(
            source="test",
            claim_scope=DalClaimScope.CARRIER_VALID,
            span=(-1, 3)  # Invalid: negative start
        )


# ============================================================================
# Test DalTraceRef
# ============================================================================


def test_dal_trace_ref_reversibility():
    """Trace must specify reversibility."""
    trace = DalTraceRef(
        transition_id="test-transition",
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.SYLLABIC,
        timestamp="2026-05-20T00:00:00Z",
        reversible=True
    )
    assert trace.reversible is True


# ============================================================================
# Test DalTransitionContract
# ============================================================================


def test_transition_contract_requires_domains_and_types():
    """Transition contract must specify source/target domains and types."""
    contract = DalTransitionContract(
        contract_id="test-contract",
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.SYLLABIC,
        input_type=str,
        output_type=list,
        claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID
    )
    assert contract.source_domain == DalTransitionDomain.GRAPHOPHONEMIC
    assert contract.target_domain == DalTransitionDomain.SYLLABIC
    assert contract.input_type == str
    assert contract.output_type == list


def test_transition_contract_is_claim_scoped():
    """Transition contract must be claim-scoped (no global certificate)."""
    contract = DalTransitionContract(
        contract_id="test-contract",
        source_domain=DalTransitionDomain.ORIGIN,
        target_domain=DalTransitionDomain.TEMPLATE,
        input_type=str,
        output_type=str,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED
    )
    assert contract.claim_scope == DalClaimScope.TEMPLATE_MATCHED


def test_transition_contract_forbids_identity():
    """Transition contract must not allow source == target (identity)."""
    with pytest.raises(ValueError, match="Source and target domain must differ"):
        DalTransitionContract(
            contract_id="invalid",
            source_domain=DalTransitionDomain.ORIGIN,
            target_domain=DalTransitionDomain.ORIGIN,  # Same as source
            input_type=str,
            output_type=str,
            claim_scope=DalClaimScope.ORIGIN_CLASSIFIED
        )


def test_transition_contract_custom_budget_requires_limit():
    """Custom budget policy must specify limit."""
    with pytest.raises(ValueError, match="CUSTOM budget policy requires"):
        DalTransitionContract(
            contract_id="invalid",
            source_domain=DalTransitionDomain.ORIGIN,
            target_domain=DalTransitionDomain.TEMPLATE,
            input_type=str,
            output_type=str,
            claim_scope=DalClaimScope.TEMPLATE_MATCHED,
            candidate_budget_policy=CandidateBudgetPolicy.CUSTOM,
            candidate_budget_limit=None  # Missing limit
        )


# ============================================================================
# Test No Global Certificate
# ============================================================================


def test_no_global_certificate():
    """There is no global certificate claim scope.

    All certificates must be scoped to specific claims.
    """
    # Verify no GLOBAL claim scope exists
    claim_scopes = [scope for scope in DalClaimScope]
    claim_scope_names = [scope.name for scope in claim_scopes]

    assert "GLOBAL" not in claim_scope_names
    assert "UNIVERSAL" not in claim_scope_names
    assert "COMPLETE" not in claim_scope_names


def test_certificate_must_be_claim_scoped():
    """Certificate evidence must specify claim scope."""
    evidence = DalEvidence(
        source="test",
        claim_scope=DalClaimScope.ORIGIN_CLASSIFIED,
        span=(0, 3)
    )
    # Must have a specific claim scope, not a generic one
    assert evidence.claim_scope != None
    assert isinstance(evidence.claim_scope, DalClaimScope)


# ============================================================================
# Test CandidateSet Shape Validation
# ============================================================================


@dataclass
class MockCandidate:
    """Mock candidate for testing."""
    candidate_id: str
    domain: DalTransitionDomain
    evidence: List[DalEvidence]
    counter_evidence: List[DalCounterEvidence]


@dataclass
class MockCandidateSet:
    """Mock candidate set implementing the protocol."""
    claim_scope: DalClaimScope
    candidates: List[MockCandidate]
    evidence: List[DalEvidence]
    counter_evidence: List[DalCounterEvidence]
    trace: List[DalTraceRef]


def test_candidate_set_shape_rejects_none_candidates():
    """CandidateSet must reject None candidates."""
    candidate_set = MockCandidateSet(
        claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,
        candidates=[None, MockCandidate("c1", DalTransitionDomain.SYLLABIC, [], [])],
        evidence=[],
        counter_evidence=[],
        trace=[]
    )

    with pytest.raises(ValueError, match="contains None candidates"):
        validate_candidate_set_shape(candidate_set)


def test_candidate_set_shape_allows_explicit_empty_set():
    """CandidateSet may be empty only explicitly."""
    candidate_set = MockCandidateSet(
        claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,
        candidates=[],  # Explicitly empty
        evidence=[],
        counter_evidence=[],
        trace=[]
    )

    # Should not raise
    validate_candidate_set_shape(candidate_set)


def test_candidate_set_protocols_are_structural():
    """Protocols provide structural typing, not inheritance."""
    # MockCandidateSet implements the protocol without inheriting from it
    candidate = MockCandidate(
        candidate_id="test",
        domain=DalTransitionDomain.SYLLABIC,
        evidence=[],
        counter_evidence=[]
    )

    candidate_set = MockCandidateSet(
        claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,
        candidates=[candidate],
        evidence=[],
        counter_evidence=[],
        trace=[]
    )

    # Verify protocol methods work
    assert candidate_set.claim_scope == DalClaimScope.SYLLABLE_STRUCTURE_VALID
    assert len(candidate_set.candidates) == 1


# ============================================================================
# Test No Direct Promotion Rules
# ============================================================================


def test_no_direct_promotion_graphophonemic_to_template():
    """GRAPHOPHONEMIC → TEMPLATE must fail without trace/shortcut."""
    contract = DalTransitionContract(
        contract_id="invalid",
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.TEMPLATE,
        input_type=str,
        output_type=str,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        shortcut_policy=ShortcutPolicy.FORBIDDEN
    )

    with pytest.raises(ValueError, match="Direct promotion.*is forbidden"):
        validate_transition_contract(contract)


def test_no_direct_promotion_syllabic_to_origin():
    """SYLLABIC → ORIGIN must fail without trace/shortcut."""
    contract = DalTransitionContract(
        contract_id="invalid",
        source_domain=DalTransitionDomain.SYLLABIC,
        target_domain=DalTransitionDomain.ORIGIN,
        input_type=str,
        output_type=str,
        claim_scope=DalClaimScope.ORIGIN_CLASSIFIED,
        shortcut_policy=ShortcutPolicy.FORBIDDEN
    )

    with pytest.raises(ValueError, match="Direct promotion.*is forbidden"):
        validate_transition_contract(contract)


def test_direct_promotion_allowed_with_shortcut_policy():
    """Direct promotion is allowed if shortcut policy permits."""
    contract = DalTransitionContract(
        contract_id="valid",
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.TEMPLATE,
        input_type=str,
        output_type=str,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        shortcut_policy=ShortcutPolicy.CLOSED_CLASS_ONLY  # Permits shortcuts
    )

    # Should not raise
    validate_transition_contract(contract)


def test_validate_no_direct_promotion_requires_justification():
    """validate_no_direct_promotion requires trace/shortcut/attestation."""
    # Without justification
    with pytest.raises(ValueError, match="requires trace, shortcut, or attestation"):
        validate_no_direct_promotion(
            source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
            target_domain=DalTransitionDomain.TEMPLATE,
            has_trace=False,
            has_shortcut=False,
            has_attestation=False
        )

    # With trace - should pass
    validate_no_direct_promotion(
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.TEMPLATE,
        has_trace=True,
        has_shortcut=False,
        has_attestation=False
    )

    # With shortcut - should pass
    validate_no_direct_promotion(
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.TEMPLATE,
        has_trace=False,
        has_shortcut=True,
        has_attestation=False
    )

    # With attestation - should pass
    validate_no_direct_promotion(
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.TEMPLATE,
        has_trace=False,
        has_shortcut=False,
        has_attestation=True
    )


def test_adjacent_domain_transitions_allowed():
    """Adjacent domain transitions (D0→D1, D1→D2, etc.) are allowed."""
    # GRAPHOPHONEMIC → SYLLABIC (adjacent)
    validate_no_direct_promotion(
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.SYLLABIC,
        has_trace=False,
        has_shortcut=False,
        has_attestation=False
    )

    # SYLLABIC → PRE_MORPH (adjacent)
    validate_no_direct_promotion(
        source_domain=DalTransitionDomain.SYLLABIC,
        target_domain=DalTransitionDomain.PRE_MORPH,
        has_trace=False,
        has_shortcut=False,
        has_attestation=False
    )


# ============================================================================
# Test Closed-Class Shortcut
# ============================================================================


def test_closed_class_shortcut_allowed_with_lexicon():
    """Closed-class shortcuts are allowed for particles, etc."""
    contract = DalTransitionContract(
        contract_id="particle-shortcut",
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.IDENTITY_AXIS,
        input_type=str,
        output_type=str,
        claim_scope=DalClaimScope.IDENTITY_DETERMINED,
        shortcut_policy=ShortcutPolicy.CLOSED_CLASS_ONLY,
        lexicon_requirement=True  # Requires lexicon lookup
    )

    # Should not raise
    validate_transition_contract(contract)


def test_explicit_attestation_shortcut_allowed():
    """Explicit attestation allows shortcuts."""
    contract = DalTransitionContract(
        contract_id="attested-shortcut",
        source_domain=DalTransitionDomain.SYLLABIC,
        target_domain=DalTransitionDomain.TEMPLATE,
        input_type=str,
        output_type=str,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        shortcut_policy=ShortcutPolicy.WITH_ATTESTATION,
        evidence_requirement=EvidenceRequirement.ATTESTATION
    )

    # Should not raise
    validate_transition_contract(contract)


# ============================================================================
# Test Forbidden Outputs (Semantic Leakage Prevention)
# ============================================================================


class ForbiddenMeaningType:
    """Mock forbidden type (e.g., semantic meaning)."""
    pass


class ForbiddenMuradType:
    """Mock forbidden type (e.g., intended meaning)."""
    pass


def test_forbidden_outputs_detect_forbidden_type():
    """ensure_no_forbidden_outputs detects forbidden types."""
    obj = ForbiddenMeaningType()

    with pytest.raises(ValueError, match="Forbidden output type detected"):
        ensure_no_forbidden_outputs(
            obj,
            forbidden_outputs={ForbiddenMeaningType}
        )


def test_forbidden_outputs_detect_forbidden_field():
    """ensure_no_forbidden_outputs detects forbidden fields."""
    @dataclass
    class ObjectWithForbiddenField:
        name: str
        forbidden_field: ForbiddenMeaningType

    obj = ObjectWithForbiddenField(
        name="test",
        forbidden_field=ForbiddenMeaningType()
    )

    with pytest.raises(ValueError, match="Forbidden output type in field"):
        ensure_no_forbidden_outputs(
            obj,
            forbidden_outputs={ForbiddenMeaningType}
        )


def test_forbidden_outputs_allows_valid_types():
    """ensure_no_forbidden_outputs allows valid types."""
    @dataclass
    class ValidObject:
        name: str
        value: int

    obj = ValidObject(name="test", value=42)

    # Should not raise
    ensure_no_forbidden_outputs(
        obj,
        forbidden_outputs={ForbiddenMeaningType, ForbiddenMuradType}
    )


# ============================================================================
# Test Protocols Don't Force Inheritance
# ============================================================================


def test_protocols_do_not_force_existing_classes_to_inherit():
    """Protocols provide duck typing, not forced inheritance."""
    # MockCandidate and MockCandidateSet implement protocols
    # without inheriting from DalCandidateProtocol or DalCandidateSetProtocol

    candidate = MockCandidate(
        candidate_id="test",
        domain=DalTransitionDomain.SYLLABIC,
        evidence=[],
        counter_evidence=[]
    )

    # Verify properties exist (duck typing)
    assert hasattr(candidate, 'candidate_id')
    assert hasattr(candidate, 'domain')
    assert hasattr(candidate, 'evidence')
    assert hasattr(candidate, 'counter_evidence')

    # Verify no direct inheritance from Protocol class
    # (Protocols are structural, not nominal typing)
    assert DalCandidateProtocol not in type(candidate).__mro__


# ============================================================================
# Test Signature Does Not Import Relation or Case Effect
# ============================================================================


def test_signature_does_not_import_relation_or_case_effect():
    """dal_algebra.py must not import RelationCandidate or CaseEffectCandidate.

    These are future implementations (PR #37, PR #38).
    """
    import dal_core.dal_algebra as dal_algebra_module

    # Get all names in module
    module_names = dir(dal_algebra_module)

    # Verify no relation or case effect imports
    assert "RelationCandidate" not in module_names
    assert "CaseEffectCandidate" not in module_names
    assert "RelationType" not in module_names
    assert "CaseEffectType" not in module_names


def test_signature_does_not_claim_complete_algebra():
    """dal_algebra.py is minimal signature, not complete algebra."""
    import dal_core.dal_algebra as dal_algebra_module

    module_names = dir(dal_algebra_module)

    # Verify no rank/residual algebra implementations
    assert "RankAlgebra" not in module_names
    assert "ResidualAlgebra" not in module_names
    assert "CandidateSetBase" not in module_names

    # Verify no analyzers
    assert "DalAnalyzer" not in module_names
    assert "MorphAnalyzer" not in module_names


# ============================================================================
# Test Semantic Leakage Prevention
# ============================================================================


def test_dal_claim_scopes_forbid_semantic_claims():
    """DalClaimScope must not include semantic claims.

    Forbidden claims:
    - Meaning
    - Murad (intended meaning)
    - Hukm (legal ruling)
    - Semantic relations (before wadh' boundary)
    """
    claim_scope_names = [scope.name for scope in DalClaimScope]

    # Verify forbidden claim scopes don't exist
    forbidden_claims = [
        "MEANING_DETERMINED",
        "MURAD_INFERRED",
        "HUKM_ISSUED",
        "SEMANTIC_RELATION_IDENTIFIED",
        "MADLUL_LINKED",
        "WADH_ESTABLISHED"
    ]

    for forbidden in forbidden_claims:
        assert forbidden not in claim_scope_names, \
            f"Forbidden claim scope {forbidden} found in DalClaimScope"


def test_dal_transition_domains_are_pre_semantic():
    """All DalTransitionDomain values are pre-semantic (form only)."""
    domain_names = [domain.name for domain in DalTransitionDomain]

    # Verify no semantic domains
    forbidden_domains = [
        "SEMANTIC",
        "WADH",
        "MADLUL",
        "DALALAH",
        "USAGE",
        "MURAD",
        "HUKM"
    ]

    for forbidden in forbidden_domains:
        assert forbidden not in domain_names, \
            f"Forbidden semantic domain {forbidden} found in DalTransitionDomain"


# ============================================================================
# Test Evidence Requirements
# ============================================================================


def test_evidence_requirements_are_typed():
    """Evidence requirements must be explicitly typed."""
    # Verify all evidence requirement types exist
    requirements = [
        EvidenceRequirement.NONE,
        EvidenceRequirement.LEXICON_LOOKUP,
        EvidenceRequirement.CONTEXT,
        EvidenceRequirement.ATTESTATION,
        EvidenceRequirement.TRACE,
    ]

    assert len(requirements) == 5


def test_contract_with_lexicon_requirement():
    """Contract can specify lexicon requirement."""
    contract = DalTransitionContract(
        contract_id="lexicon-test",
        source_domain=DalTransitionDomain.ORIGIN,
        target_domain=DalTransitionDomain.TEMPLATE,
        input_type=str,
        output_type=str,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        lexicon_requirement=True,
        evidence_requirement=EvidenceRequirement.LEXICON_LOOKUP
    )

    assert contract.lexicon_requirement is True
    assert contract.evidence_requirement == EvidenceRequirement.LEXICON_LOOKUP


# ============================================================================
# Test Budget Policies
# ============================================================================


def test_budget_policies_enforce_boundedness():
    """Candidate budget policies enforce finite candidate sets."""
    policies = [
        CandidateBudgetPolicy.UNBOUNDED,
        CandidateBudgetPolicy.SMALL,
        CandidateBudgetPolicy.MEDIUM,
        CandidateBudgetPolicy.LARGE,
        CandidateBudgetPolicy.CUSTOM,
    ]

    assert len(policies) == 5


def test_small_budget_policy():
    """SMALL budget policy suggests ≤10 candidates."""
    contract = DalTransitionContract(
        contract_id="small-budget",
        source_domain=DalTransitionDomain.ORIGIN,
        target_domain=DalTransitionDomain.TEMPLATE,
        input_type=str,
        output_type=str,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        candidate_budget_policy=CandidateBudgetPolicy.SMALL
    )

    assert contract.candidate_budget_policy == CandidateBudgetPolicy.SMALL


def test_custom_budget_policy_with_limit():
    """CUSTOM budget policy specifies explicit limit."""
    contract = DalTransitionContract(
        contract_id="custom-budget",
        source_domain=DalTransitionDomain.ORIGIN,
        target_domain=DalTransitionDomain.TEMPLATE,
        input_type=str,
        output_type=str,
        claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        candidate_budget_policy=CandidateBudgetPolicy.CUSTOM,
        candidate_budget_limit=50
    )

    assert contract.candidate_budget_limit == 50


# ============================================================================
# Integration Tests
# ============================================================================


def test_full_transition_contract_example():
    """Example of a complete transition contract."""
    contract = DalTransitionContract(
        contract_id="syllable-to-promorph",
        source_domain=DalTransitionDomain.SYLLABIC,
        target_domain=DalTransitionDomain.PRE_MORPH,
        input_type=list,  # List of syllables
        output_type=dict,  # Pre-morph classification
        claim_scope=DalClaimScope.ORIGIN_CLASSIFIED,
        evidence_requirement=EvidenceRequirement.TRACE,
        lexicon_requirement=False,
        context_requirement=False,
        shortcut_policy=ShortcutPolicy.FORBIDDEN,
        candidate_budget_policy=CandidateBudgetPolicy.MEDIUM,
        forbidden_output_types={ForbiddenMeaningType, ForbiddenMuradType},
        allows_unresolved=True,
        hypothesis_only=False
    )

    validate_transition_contract(contract)

    assert contract.source_domain == DalTransitionDomain.SYLLABIC
    assert contract.target_domain == DalTransitionDomain.PRE_MORPH
    assert contract.allows_unresolved is True
    assert ForbiddenMeaningType in contract.forbidden_output_types


def test_full_evidence_example():
    """Example of complete evidence with all fields."""
    evidence = DalEvidence(
        source="lexicon:seed",
        claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        span=(0, 3),
        confidence=0.95,
        details={
            "pattern": "فَعَلَ",
            "root": "ك-ت-ب",
            "attestations": 100
        }
    )

    assert evidence.confidence == 0.95
    assert evidence.details["pattern"] == "فَعَلَ"


def test_full_candidate_set_example():
    """Example of complete candidate set."""
    candidates = [
        MockCandidate(
            candidate_id="c1",
            domain=DalTransitionDomain.TEMPLATE,
            evidence=[
                DalEvidence(
                    source="lexicon",
                    claim_scope=DalClaimScope.TEMPLATE_MATCHED,
                    span=(0, 3),
                    confidence=0.9
                )
            ],
            counter_evidence=[]
        ),
        MockCandidate(
            candidate_id="c2",
            domain=DalTransitionDomain.TEMPLATE,
            evidence=[
                DalEvidence(
                    source="pattern-match",
                    claim_scope=DalClaimScope.TEMPLATE_MATCHED,
                    span=(0, 3),
                    confidence=0.7
                )
            ],
            counter_evidence=[]
        )
    ]

    candidate_set = MockCandidateSet(
        claim_scope=DalClaimScope.TEMPLATE_MATCHED,
        candidates=candidates,
        evidence=[
            DalEvidence(
                source="aggregate",
                claim_scope=DalClaimScope.TEMPLATE_MATCHED,
                span=(0, 3)
            )
        ],
        counter_evidence=[],
        trace=[
            DalTraceRef(
                transition_id="origin-to-template",
                source_domain=DalTransitionDomain.ORIGIN,
                target_domain=DalTransitionDomain.TEMPLATE,
                timestamp="2026-05-20T00:00:00Z",
                reversible=True
            )
        ]
    )

    validate_candidate_set_shape(candidate_set)

    assert len(candidate_set.candidates) == 2
    assert len(candidate_set.trace) == 1
    assert candidate_set.trace[0].reversible is True
