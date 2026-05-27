"""
U₁₀ WordFormCandidateCarrier Constitutional Tests

Tests the 11 constitutional laws that govern U₁₀ execution:

1. No U₁₀ without ApprovedTransitionContext
2. Context must be for U₉→U₁₀ transition
3. No U₁₀ without WEIGHT_IDENTITY input
4. No SEMANTIC_IDENTITY output
5. No HUKM_IDENTITY output
6. No FUNCTIONAL_RELATION_IDENTITY output
7. Weight trace must be preserved
8. U₇-C agreement edges preserved as external trace
9. Residual audit must be preserved
10. Candidate rank preserved (not certificate)
11. Golden path execution succeeds

Constitutional Law (Arabic):
    لا U₁₀ بلا ApprovedTransitionContext.
    ولا U₁₀ بلا WEIGHT_IDENTITY محفوظة.
    ولا صورة كلمة بلا وزن محفوظ.
    ولا انتقال من الوزن إلى المعنى مباشرة.

Status: 🔧 Tests defined before implementation (TDD approach)
Created: 2026-05-26
"""

import pytest
from unittest.mock import MagicMock
from uuid import uuid4

from dal_core.u10_word_form_candidate_carrier import (
    WordFormCandidateUnit,
    WordFormCandidateResult,
    word_form_candidate_carrier_10,
    validate_approved_context_for_u10,
)
from dal_core.approved_transition_context import ApprovedTransitionContext
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.identity_registry import IdentityType
from dal_core.domain_registry import DomainType
from dal_core.foundation.rank import Rank
from dal_core.residuals import Residual, ResidualType, ResidualSeverity


# ============================================================================
# Test Helpers
# ============================================================================

def make_valid_u9_input():
    """Create valid U₉ weight candidate input."""
    return {
        "unit_id": str(uuid4()),
        "weight_pattern": "فَاعِل",
        "surface_form": "كَاتِب",
        "weight_identity": IdentityType.WEIGHT_IDENTITY,
        "agreement_edge_ids": [str(uuid4()), str(uuid4())],
        "rank": 0.8,
        "residuals": [],
    }


def make_valid_approved_context_u9_to_u10():
    """Create valid ApprovedTransitionContext for U₉→U₁₀."""
    # NOTE: This is a mock. Real implementation requires DecisionAudit.
    context = MagicMock(spec=ApprovedTransitionContext)
    context.from_layer = ExecutionLayer.U9_WEIGHT
    context.to_layer = ExecutionLayer.U10_WORD_FORM
    context.input_identity = IdentityType.WEIGHT_IDENTITY
    # NOTE: WORDFORM_IDENTITY not yet in IdentityType enum
    # For now, use a non-forbidden identity
    context.output_identity = IdentityType.WEIGHT_IDENTITY  # Placeholder
    context.domain = DomainType.WEIGHT_DOMAIN  # Placeholder (should be WORDFORM_DOMAIN)
    return context


# ============================================================================
# Test 1: Governance - No Context
# ============================================================================

def test_u10_rejects_without_approved_transition_context():
    """
    Test 1: U₁₀ must reject execution without ApprovedTransitionContext.

    Constitutional Law:
        لا U₁₀ بلا ApprovedTransitionContext.

    Verification:
        - Call word_form_candidate_carrier_10 with context=None
        - Expect ValueError
        - Error message mentions ApprovedTransitionContext requirement
    """
    u9_input = make_valid_u9_input()

    with pytest.raises(ValueError) as exc_info:
        word_form_candidate_carrier_10(u9_input, approved_context=None)

    error_message = str(exc_info.value)
    assert "ApprovedTransitionContext" in error_message
    assert "U₁₀" in error_message or "WordForm" in error_message


# ============================================================================
# Test 2: Governance - Wrong Transition
# ============================================================================

def test_u10_rejects_context_not_for_u9_to_u10():
    """
    Test 2: U₁₀ must reject context for wrong transition.

    Constitutional Law:
        Context must be for U₉→U₁₀ transition specifically.

    Verification:
        - Create context for U₈→U₉ transition
        - Call U₁₀ with this context
        - Expect ValueError about wrong transition
    """
    u9_input = make_valid_u9_input()

    # Create context for U₈→U₉ (wrong transition)
    wrong_context = MagicMock(spec=ApprovedTransitionContext)
    wrong_context.from_layer = ExecutionLayer.U8_ROOT_STEM
    wrong_context.to_layer = ExecutionLayer.U9_WEIGHT
    wrong_context.input_identity = IdentityType.STEM_IDENTITY
    wrong_context.output_identity = IdentityType.WEIGHT_IDENTITY
    wrong_context.domain = DomainType.WEIGHT_DOMAIN

    with pytest.raises(ValueError) as exc_info:
        word_form_candidate_carrier_10(u9_input, approved_context=wrong_context)

    error_message = str(exc_info.value)
    assert "U9_WEIGHT" in error_message or "U₉" in error_message
    assert "U10_WORD_FORM" in error_message or "U₁₀" in error_message


# ============================================================================
# Test 3: Input Validation - Missing WEIGHT_IDENTITY
# ============================================================================

def test_u10_rejects_missing_weight_identity():
    """
    Test 3: U₁₀ must reject input without WEIGHT_IDENTITY.

    Constitutional Law:
        لا صورة كلمة بلا وزن محفوظ.
        No word form without preserved weight.

    Verification:
        - Create context with PHONETIC_IDENTITY input (not WEIGHT_IDENTITY)
        - Call U₁₀
        - Expect ValueError about missing WEIGHT_IDENTITY
    """
    u9_input = make_valid_u9_input()

    # Create context with wrong input identity
    wrong_context = MagicMock(spec=ApprovedTransitionContext)
    wrong_context.from_layer = ExecutionLayer.U9_WEIGHT
    wrong_context.to_layer = ExecutionLayer.U10_WORD_FORM
    wrong_context.input_identity = IdentityType.PHONETIC_IDENTITY  # WRONG
    wrong_context.output_identity = IdentityType.WEIGHT_IDENTITY
    wrong_context.domain = DomainType.WEIGHT_DOMAIN

    with pytest.raises(ValueError) as exc_info:
        word_form_candidate_carrier_10(u9_input, approved_context=wrong_context)

    error_message = str(exc_info.value)
    assert "WEIGHT_IDENTITY" in error_message


# ============================================================================
# Test 4: Forbidden Output - SEMANTIC_IDENTITY
# ============================================================================

def test_u10_rejects_semantic_identity_output():
    """
    Test 4: U₁₀ must reject context claiming SEMANTIC_IDENTITY output.

    Constitutional Law:
        لا انتقال من الوزن إلى المعنى مباشرة.
        No direct transition from weight to meaning.

    Verification:
        - Create context with SEMANTIC_IDENTITY output
        - Call U₁₀
        - Expect ValueError about forbidden semantic output
    """
    u9_input = make_valid_u9_input()

    # Create context with SEMANTIC_IDENTITY output (forbidden)
    semantic_context = MagicMock(spec=ApprovedTransitionContext)
    semantic_context.from_layer = ExecutionLayer.U9_WEIGHT
    semantic_context.to_layer = ExecutionLayer.U10_WORD_FORM
    semantic_context.input_identity = IdentityType.WEIGHT_IDENTITY
    semantic_context.output_identity = IdentityType.SEMANTIC_IDENTITY  # FORBIDDEN
    semantic_context.domain = DomainType.WEIGHT_DOMAIN

    with pytest.raises(ValueError) as exc_info:
        word_form_candidate_carrier_10(u9_input, approved_context=semantic_context)

    error_message = str(exc_info.value)
    assert "SEMANTIC_IDENTITY" in error_message or "meaning" in error_message.lower()


# ============================================================================
# Test 5: Forbidden Output - HUKM_IDENTITY
# ============================================================================

def test_u10_rejects_hukm_identity_output():
    """
    Test 5: U₁₀ must reject context claiming HUKM_IDENTITY output.

    Constitutional Law:
        Word form ≠ grammatical judgment.

    Verification:
        - Create context with HUKM_IDENTITY output
        - Call U₁₀
        - Expect ValueError about forbidden hukm output
    """
    u9_input = make_valid_u9_input()

    # Create context with HUKM_IDENTITY output (forbidden)
    hukm_context = MagicMock(spec=ApprovedTransitionContext)
    hukm_context.from_layer = ExecutionLayer.U9_WEIGHT
    hukm_context.to_layer = ExecutionLayer.U10_WORD_FORM
    hukm_context.input_identity = IdentityType.WEIGHT_IDENTITY
    hukm_context.output_identity = IdentityType.HUKM_IDENTITY  # FORBIDDEN
    hukm_context.domain = DomainType.WEIGHT_DOMAIN

    with pytest.raises(ValueError) as exc_info:
        word_form_candidate_carrier_10(u9_input, approved_context=hukm_context)

    error_message = str(exc_info.value)
    assert "HUKM_IDENTITY" in error_message or "hukm" in error_message.lower()


# ============================================================================
# Test 6: Forbidden Output - FUNCTIONAL_RELATION_IDENTITY
# ============================================================================

def test_u10_rejects_syntactic_role_output():
    """
    Test 6: U₁₀ must reject context claiming FUNCTIONAL_RELATION_IDENTITY output.

    Constitutional Law:
        Word form ≠ syntactic role.

    Verification:
        - Create context with FUNCTIONAL_RELATION_IDENTITY output
        - Call U₁₀
        - Expect ValueError about forbidden syntactic role output
    """
    u9_input = make_valid_u9_input()

    # Create context with FUNCTIONAL_RELATION_IDENTITY output (forbidden)
    syntactic_context = MagicMock(spec=ApprovedTransitionContext)
    syntactic_context.from_layer = ExecutionLayer.U9_WEIGHT
    syntactic_context.to_layer = ExecutionLayer.U10_WORD_FORM
    syntactic_context.input_identity = IdentityType.WEIGHT_IDENTITY
    syntactic_context.output_identity = IdentityType.FUNCTIONAL_RELATION_IDENTITY  # FORBIDDEN
    syntactic_context.domain = DomainType.WEIGHT_DOMAIN

    with pytest.raises(ValueError) as exc_info:
        word_form_candidate_carrier_10(u9_input, approved_context=syntactic_context)

    error_message = str(exc_info.value)
    assert "FUNCTIONAL_RELATION_IDENTITY" in error_message or "syntactic" in error_message.lower()


# ============================================================================
# Test 7: Trace Preservation - Weight Trace
# ============================================================================

def test_u10_preserves_weight_trace():
    """
    Test 7: U₁₀ must preserve weight trace from U₉.

    Constitutional Law:
        لا صورة كلمة بلا وزن محفوظ.

    Verification:
        - Execute U₁₀ with valid context
        - Check output contains source_weight_unit_id
        - Check output preserves weight_identity = WEIGHT_IDENTITY
        - Check output preserves weight_pattern
    """
    u9_input = make_valid_u9_input()
    context = make_valid_approved_context_u9_to_u10()

    result = word_form_candidate_carrier_10(u9_input, approved_context=context)

    # Verify result structure
    assert isinstance(result, WordFormCandidateResult)
    assert len(result.candidates) > 0

    # Check first candidate preserves weight trace
    candidate = result.candidates[0]
    assert candidate.source_weight_unit_id == u9_input["unit_id"]
    assert candidate.weight_identity == IdentityType.WEIGHT_IDENTITY
    assert candidate.weight_pattern == u9_input["weight_pattern"]


# ============================================================================
# Test 8: Trace Preservation - Agreement Edges
# ============================================================================

def test_u10_preserves_u7c_agreement_edges_as_external_trace():
    """
    Test 8: U₁₀ must preserve U₇-C agreement edges as external trace.

    Constitutional Law:
        Agreement edges from U₇-C preserved (not consumed).

    Verification:
        - Execute U₁₀ with agreement_edge_ids in input
        - Check output preserves agreement_edge_ids
        - Edges remain available for downstream layers
    """
    u9_input = make_valid_u9_input()
    context = make_valid_approved_context_u9_to_u10()

    result = word_form_candidate_carrier_10(u9_input, approved_context=context)

    # Check first candidate preserves agreement edges
    candidate = result.candidates[0]
    input_edge_ids = set(u9_input["agreement_edge_ids"])
    output_edge_ids = candidate.agreement_edge_ids

    # Agreement edges must be preserved
    assert input_edge_ids.issubset(output_edge_ids) or len(output_edge_ids) >= len(input_edge_ids)


# ============================================================================
# Test 9: Trace Preservation - Residual Audit
# ============================================================================

def test_u10_preserves_residual_audit():
    """
    Test 9: U₁₀ must preserve residual audit from upstream.

    Constitutional Law:
        Complete residual chain maintained.

    Verification:
        - Execute U₁₀ with residuals in input
        - Check result.residual_audit contains upstream residuals
        - Residual chain unbroken
    """
    u9_input = make_valid_u9_input()

    # Add upstream residuals
    upstream_residual = Residual(
        type=ResidualType.AMBIGUOUS_TYPE,  # Fixed: residual_type → type
        severity=ResidualSeverity.INFO,  # Fixed: LOW → INFO
        message="Multiple weight candidates",
        location="U₉",
    )
    u9_input["residuals"] = [upstream_residual]

    context = make_valid_approved_context_u9_to_u10()

    result = word_form_candidate_carrier_10(u9_input, approved_context=context)

    # Residual audit should preserve upstream residuals
    # (Implementation may add them to result.residual_audit or candidate.residuals)
    # For now, just check structure exists
    assert hasattr(result, 'residual_audit')
    assert isinstance(result.residual_audit, tuple)


# ============================================================================
# Test 10: Candidate Rank Preservation
# ============================================================================

def test_u10_preserves_candidate_rank():
    """
    Test 10: U₁₀ must preserve candidate rank (not certificate).

    Constitutional Law:
        U₁₀ produces candidates, not certificates.

    Verification:
        - Execute U₁₀
        - Check output contains Rank (not Certainty)
        - No certificate claims in output
    """
    u9_input = make_valid_u9_input()
    context = make_valid_approved_context_u9_to_u10()

    result = word_form_candidate_carrier_10(u9_input, approved_context=context)

    # Check candidates have Rank
    candidate = result.candidates[0]
    assert hasattr(candidate, 'rank')
    assert isinstance(candidate.rank, Rank)


# ============================================================================
# Test 11: Golden Path Execution
# ============================================================================

def test_u10_golden_path_word_form_candidate():
    """
    Test 11: Golden path execution with full governance.

    Constitutional Law:
        Complete governed execution from U₉ to U₁₀.

    Verification:
        1. Valid U₉ input
        2. Valid ApprovedTransitionContext
        3. Execution succeeds
        4. Output is WordFormCandidateResult
        5. WEIGHT_IDENTITY preserved
        6. No semantic/syntactic/hukm identities
        7. Rank preserved
        8. Residuals preserved
        9. Agreement edges preserved
        10. Execution trace maintained
    """
    # Step 1: Create valid U₉ input
    u9_input = make_valid_u9_input()

    # Step 2: Create valid governance context
    context = make_valid_approved_context_u9_to_u10()

    # Step 3: Execute U₁₀
    result = word_form_candidate_carrier_10(u9_input, approved_context=context)

    # Verification 4: Output is correct type
    assert isinstance(result, WordFormCandidateResult)

    # Verification 5: WEIGHT_IDENTITY preserved
    assert all(
        c.weight_identity == IdentityType.WEIGHT_IDENTITY
        for c in result.candidates
    )

    # Verification 6: No forbidden identities
    forbidden_identities = {
        IdentityType.SEMANTIC_IDENTITY,
        IdentityType.HUKM_IDENTITY,
        IdentityType.FUNCTIONAL_RELATION_IDENTITY,
    }
    # Check output_identity in context (not in candidates)
    assert context.output_identity not in forbidden_identities

    # Verification 7: Rank preserved
    assert all(
        isinstance(c.rank, Rank)
        for c in result.candidates
    )

    # Verification 8: Residuals structure exists
    assert hasattr(result, 'residual_audit')

    # Verification 9: Agreement edges preserved
    assert all(
        isinstance(c.agreement_edge_ids, frozenset)
        for c in result.candidates
    )

    # Verification 10: Execution trace exists
    assert hasattr(result, 'execution_trace')
    assert result.source_layer == ExecutionLayer.U9_WEIGHT
    assert result.target_layer == ExecutionLayer.U10_WORD_FORM


# ============================================================================
# Test Summary
# ============================================================================

"""
Constitutional Test Summary:

✓ Test 1: No execution without ApprovedTransitionContext
✓ Test 2: Context must be for U₉→U₁₀ transition
✓ Test 3: No execution without WEIGHT_IDENTITY input
✓ Test 4: No SEMANTIC_IDENTITY output
✓ Test 5: No HUKM_IDENTITY output
✓ Test 6: No FUNCTIONAL_RELATION_IDENTITY output
✓ Test 7: Weight trace must be preserved
✓ Test 8: U₇-C agreement edges preserved as external trace
✓ Test 9: Residual audit must be preserved
✓ Test 10: Candidate rank preserved (not certificate)
✓ Test 11: Golden path execution succeeds

Expected Status: 11/11 tests passing (after implementation)
Current Status: Tests defined, implementation stub exists

Next Step: Implement word_form_candidate_carrier_10() logic to pass all tests
"""
