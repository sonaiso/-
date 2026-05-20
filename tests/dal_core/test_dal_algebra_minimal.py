"""Tests for minimal dal transition signature (PR #22).

Verifies compliance with PR #21 governance:
- Ordered bounded sequences
- Position-scoped claims
- Reverse trace
- Direction specification
- Boundary preservation
- Claim-scoped evidence
"""

import sys
sys.path.insert(0, 'src')

import pytest
from dal_core import (
    DalTransitionDomain,
    DalClaimScope,
    DalEvidence,
    DalCounterEvidence,
    ShortcutPolicy,
    EvidenceRequirement,
    CandidateBudgetPolicy,
    DalTrace,
    DalCandidateProtocol,
    DalCandidateSetProtocol,
    DalTransitionContract,
    validate_transition_contract,
    validate_candidate_set_shape,
    validate_no_direct_promotion,
)
from dataclasses import dataclass
from typing import List, Tuple


# =============================================================================
# TEST EVIDENCE VALIDATION
# =============================================================================

def test_evidence_requires_span():
    """PR #21 Invariant 1: No claim without position."""
    evidence = DalEvidence(
        claim_scope=DalClaimScope.SPAN,
        span=(0, 3),
        observation="Three letters",
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
    )
    assert evidence.span == (0, 3)


def test_evidence_rejects_invalid_span():
    """Span must be valid ordered sequence."""
    with pytest.raises(ValueError, match="Invalid span"):
        DalEvidence(
            claim_scope=DalClaimScope.SINGLE_POSITION,
            span=(5, 2),  # End before start
            observation="Invalid",
            source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        )


def test_evidence_rejects_negative_span():
    """Span cannot have negative indices."""
    with pytest.raises(ValueError, match="Invalid span"):
        DalEvidence(
            claim_scope=DalClaimScope.SPAN,
            span=(-1, 3),
            observation="Negative start",
            source_domain=DalTransitionDomain.SYLLABIC,
        )


def test_counter_evidence_has_span():
    """Counter-evidence also requires position (PR #21)."""
    counter = DalCounterEvidence(
        claim_scope=DalClaimScope.ADJACENCY,
        span=(1, 2),
        blocking_observation="Phonotactic constraint violated",
        source_domain=DalTransitionDomain.SYLLABIC,
    )
    assert counter.span == (1, 2)


# =============================================================================
# TEST TRACE REVERSIBILITY
# =============================================================================

def test_trace_preserves_fold_reversibility():
    """PR #21 Invariant 2: No fold without reverse trace."""
    trace = DalTrace(
        source_domain=DalTransitionDomain.SYLLABIC,
        target_domain=DalTransitionDomain.PRE_MORPH,
        operation="fold_syllables",
        input_spans=[(0, 2), (2, 4)],  # Two syllables
        output_span=(0, 4),              # Combined pre-morph unit
    )
    assert trace.is_reversible()
    assert len(trace.input_spans) == 2


def test_trace_without_input_is_not_reversible():
    """Trace without input spans cannot be reversed."""
    trace = DalTrace(
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.SYLLABIC,
        operation="invalid",
        input_spans=[],
        output_span=(0, 1),
    )
    assert not trace.is_reversible()


# =============================================================================
# TEST PROTOCOLS (STRUCTURAL TYPING)
# =============================================================================

@dataclass
class MockCandidate:
    """Mock candidate for testing protocol compliance."""
    span: Tuple[int, int]
    claim_scope: DalClaimScope


@dataclass
class MockCandidateSet:
    """Mock candidate set for testing."""
    candidates: List[MockCandidate]
    domain: DalTransitionDomain

    def is_empty(self) -> bool:
        return len(self.candidates) == 0


def test_candidate_protocol_requires_span():
    """PR #21 Invariant 4: No candidate without boundaries."""
    cand = MockCandidate(
        span=(2, 5),
        claim_scope=DalClaimScope.SPAN,
    )
    # Duck typing: should satisfy protocol
    assert hasattr(cand, 'span')
    assert hasattr(cand, 'claim_scope')


def test_candidate_set_protocol_preserves_order():
    """Candidate sets preserve sequence ordering."""
    cand1 = MockCandidate(span=(0, 2), claim_scope=DalClaimScope.SPAN)
    cand2 = MockCandidate(span=(2, 4), claim_scope=DalClaimScope.SPAN)

    cand_set = MockCandidateSet(
        candidates=[cand1, cand2],
        domain=DalTransitionDomain.ORIGIN,
    )

    assert len(cand_set.candidates) == 2
    assert cand_set.candidates[0].span == (0, 2)
    assert cand_set.candidates[1].span == (2, 4)


def test_empty_candidate_set_allowed():
    """Empty candidate set is explicitly allowed."""
    cand_set = MockCandidateSet(
        candidates=[],
        domain=DalTransitionDomain.TEMPLATE,
    )
    assert cand_set.is_empty()


# =============================================================================
# TEST VALIDATION FUNCTIONS
# =============================================================================

class MinimalContract:
    """Minimal contract for testing."""
    source_domain = DalTransitionDomain.GRAPHOPHONEMIC
    target_domain = DalTransitionDomain.SYLLABIC
    shortcut_policy = ShortcutPolicy.FORBIDDEN
    evidence_requirement = EvidenceRequirement.WEAK

    def apply(self, input_unit, evidence):
        return MockCandidateSet([], DalTransitionDomain.SYLLABIC)


def test_validate_minimal_contract_passes():
    """Minimal valid contract passes validation."""
    contract = MinimalContract()
    errors = validate_transition_contract(contract)
    assert len(errors) == 0


def test_validate_contract_detects_missing_domain():
    """Validation detects missing domain."""
    class BadContract:
        shortcut_policy = ShortcutPolicy.FORBIDDEN
        evidence_requirement = EvidenceRequirement.NONE
        def apply(self, x, e): pass

    errors = validate_transition_contract(BadContract())
    assert "source_domain" in errors[0]
    assert "target_domain" in errors[1]


def test_validate_contract_detects_missing_apply():
    """Validation detects missing apply method."""
    class BadContract:
        source_domain = DalTransitionDomain.ORIGIN
        target_domain = DalTransitionDomain.TEMPLATE
        shortcut_policy = ShortcutPolicy.FORBIDDEN
        evidence_requirement = EvidenceRequirement.STRONG

    errors = validate_transition_contract(BadContract())
    assert any("apply" in err for err in errors)


def test_validate_candidate_set_requires_boundaries():
    """PR #21 Invariant 4: Candidates must have boundaries."""
    @dataclass
    class BadCandidate:
        claim: str  # Missing span!

    bad_set = MockCandidateSet(
        candidates=[BadCandidate(claim="test")],
        domain=DalTransitionDomain.IDENTITY_AXIS,
    )

    errors = validate_candidate_set_shape(bad_set)
    assert any("missing span" in err.lower() for err in errors)


def test_validate_candidate_set_allows_empty_explicitly():
    """Empty sets allowed when explicitly permitted."""
    empty_set = MockCandidateSet(
        candidates=[],
        domain=DalTransitionDomain.JUDGMENT,
    )
    errors = validate_candidate_set_shape(empty_set, allow_empty=True)
    assert len(errors) == 0


def test_validate_candidate_set_rejects_empty_when_disallowed():
    """Empty sets rejected when not allowed."""
    empty_set = MockCandidateSet(
        candidates=[],
        domain=DalTransitionDomain.SYLLABIC,
    )
    errors = validate_candidate_set_shape(empty_set, allow_empty=False)
    assert any("empty" in err.lower() for err in errors)


# =============================================================================
# TEST NO DIRECT PROMOTION POLICY
# =============================================================================

def test_adjacent_layers_allowed():
    """Adjacent layer transitions (distance 1) are allowed."""
    violations = validate_no_direct_promotion(
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.SYLLABIC,
        shortcut_policy=ShortcutPolicy.FORBIDDEN,
    )
    assert len(violations) == 0


def test_forbidden_cross_layer_promotion():
    """Repository memory: Prohibited cross-layer promotions.

    رسم/صوت → وزن (grapheme/phoneme to pattern) is FORBIDDEN.
    """
    violations = validate_no_direct_promotion(
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,  # D0
        target_domain=DalTransitionDomain.TEMPLATE,         # D4
        shortcut_policy=ShortcutPolicy.FORBIDDEN,
    )
    assert len(violations) > 0
    assert "forbidden" in violations[0].lower()


def test_lexicon_attested_shortcut_requires_attestation():
    """LEXICON_ATTESTED policy requires attestation flag."""
    violations = validate_no_direct_promotion(
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.IDENTITY_AXIS,
        shortcut_policy=ShortcutPolicy.LEXICON_ATTESTED,
        lexicon_attested=False,  # Not attested
    )
    assert len(violations) > 0
    assert "lexicon" in violations[0].lower()


def test_lexicon_attested_shortcut_passes_with_attestation():
    """LEXICON_ATTESTED policy passes when attested."""
    violations = validate_no_direct_promotion(
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.IDENTITY_AXIS,
        shortcut_policy=ShortcutPolicy.LEXICON_ATTESTED,
        lexicon_attested=True,  # Attested
    )
    assert len(violations) == 0


def test_trace_shortcut_requires_trace():
    """WITH_TRACE policy requires trace_provided flag."""
    violations = validate_no_direct_promotion(
        source_domain=DalTransitionDomain.SYLLABIC,
        target_domain=DalTransitionDomain.ORIGIN,
        shortcut_policy=ShortcutPolicy.WITH_TRACE,
        trace_provided=False,
    )
    assert len(violations) > 0
    assert "trace" in violations[0].lower()


def test_trace_shortcut_passes_with_trace():
    """WITH_TRACE policy passes when trace provided."""
    violations = validate_no_direct_promotion(
        source_domain=DalTransitionDomain.SYLLABIC,
        target_domain=DalTransitionDomain.ORIGIN,
        shortcut_policy=ShortcutPolicy.WITH_TRACE,
        trace_provided=True,
    )
    assert len(violations) == 0


# =============================================================================
# TEST DOMAIN ENUM COMPLETENESS
# =============================================================================

def test_eight_layer_architecture():
    """Repository memory: 8-layer Dal Algebra architecture (D0-D7)."""
    domains = list(DalTransitionDomain)
    assert len(domains) == 8
    assert DalTransitionDomain.GRAPHOPHONEMIC in domains
    assert DalTransitionDomain.JUDGMENT in domains


def test_claim_scope_types():
    """Claim scopes cover main categories from PR #21."""
    scopes = list(DalClaimScope)
    assert DalClaimScope.SINGLE_POSITION in scopes
    assert DalClaimScope.SPAN in scopes
    assert DalClaimScope.ADJACENCY in scopes
    assert DalClaimScope.FOLD in scopes
    assert DalClaimScope.BOUNDARY in scopes


# =============================================================================
# TEST OUT-OF-SCOPE VERIFICATION
# =============================================================================

def test_no_relation_candidate_import():
    """PR #22 out of scope: No RelationCandidate."""
    import dal_core
    assert not hasattr(dal_core, 'RelationCandidate')


def test_no_case_effect_candidate_import():
    """PR #22 out of scope: No CaseEffectCandidate."""
    import dal_core
    assert not hasattr(dal_core, 'CaseEffectCandidate')


def test_no_rank_algebra_implementation():
    """PR #22 out of scope: No Rank Algebra implementation."""
    import dal_core.dal_algebra as da
    # Should not have RankAlgebra class
    module_classes = [name for name in dir(da) if name[0].isupper()]
    assert not any('RankAlgebra' in cls for cls in module_classes)


def test_no_residual_algebra_implementation():
    """PR #22 out of scope: No Residual Algebra implementation."""
    import dal_core.dal_algebra as da
    module_classes = [name for name in dir(da) if name[0].isupper()]
    assert not any('ResidualAlgebra' in cls for cls in module_classes)


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
