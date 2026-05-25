"""
Tests for Execution Layer Registry and Layer Jump Prevention

Purpose: Verify that architectural layer jumps are prevented and canonical
         layer ordering is enforced.

Critical Laws Tested:
    - U₂s CANNOT jump to FunctionalRole (U₅) directly
    - U₂s MUST go through U₃ Boundary and U₄ TrueLafẓ first
    - Canonical layer order is enforced
    - Legacy U₃ FunctionalRole is marked as mispositioned
    - New U₅ FunctionalRole is the canonical position

PR: EXEC-LAYER-REFACTOR
Created: 2026-05-25
"""

import pytest
from dal_core.execution_layer_registry import (
    ExecutionLayer,
    EXECUTION_LAYER_ORDER,
    ALLOWED_TRANSITIONS,
    FORBIDDEN_JUMPS,
    is_transition_allowed,
    get_forbidden_jump_reason,
    get_required_intermediate_layers,
    validate_layer_sequence,
    get_canonical_layer,
)


# ============================================================================
# Test Layer Registry Structure
# ============================================================================

def test_execution_layer_order_contains_all_layers():
    """Verify execution layer order contains all expected layers."""
    expected_layers = {
        ExecutionLayer.U0_UNICODE,
        ExecutionLayer.U1_GRAPHEME,
        ExecutionLayer.U2P_PHONETIC_PROJECTION,
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        ExecutionLayer.U4_TRUE_SINGULAR_LAFZ,
        ExecutionLayer.U5_FUNCTIONAL_ROLE,
        ExecutionLayer.U6_MABNI_CLOSED_CLASS,
        ExecutionLayer.U7_PRE_WEIGHT_CONTRACT,
        ExecutionLayer.U8_ROOT_STEM,
        ExecutionLayer.U9_WEIGHT,
    }

    for layer in expected_layers:
        assert layer in EXECUTION_LAYER_ORDER, f"{layer} missing from EXECUTION_LAYER_ORDER"


def test_u3_is_boundary_not_functional_role():
    """CRITICAL: Verify U₃ is BoundaryAndAttachment, not FunctionalRole."""
    # U₃ position in canonical order
    u3_index = EXECUTION_LAYER_ORDER.index(ExecutionLayer.U3_BOUNDARY_ATTACHMENT)
    assert u3_index == 4, "U₃ should be at position 4 (after U₀, U₁, U₂p, U₂s)"

    # U₅ is FunctionalRole
    u5_index = EXECUTION_LAYER_ORDER.index(ExecutionLayer.U5_FUNCTIONAL_ROLE)
    assert u5_index == 6, "U₅ should be at position 6"

    # U₃ comes before U₅
    assert u3_index < u5_index, "U₃ (Boundary) must come before U₅ (FunctionalRole)"


def test_u4_true_lafz_exists_between_boundary_and_role():
    """Verify U₄ TrueSingularLafẓ exists between Boundary and FunctionalRole."""
    u3_index = EXECUTION_LAYER_ORDER.index(ExecutionLayer.U3_BOUNDARY_ATTACHMENT)
    u4_index = EXECUTION_LAYER_ORDER.index(ExecutionLayer.U4_TRUE_SINGULAR_LAFZ)
    u5_index = EXECUTION_LAYER_ORDER.index(ExecutionLayer.U5_FUNCTIONAL_ROLE)

    assert u3_index < u4_index < u5_index, (
        "Layer order must be: U₃ Boundary → U₄ TrueLafẓ → U₅ FunctionalRole"
    )


# ============================================================================
# Test Allowed Transitions
# ============================================================================

def test_u2s_to_u3_boundary_is_allowed():
    """Verify U₂s → U₃ BoundaryAndAttachment is allowed."""
    assert is_transition_allowed(
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT
    ), "U₂s → U₃ Boundary MUST be allowed"


def test_u3_boundary_to_u4_true_lafz_is_allowed():
    """Verify U₃ → U₄ TrueSingularLafẓ is allowed."""
    assert is_transition_allowed(
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        ExecutionLayer.U4_TRUE_SINGULAR_LAFZ
    ), "U₃ Boundary → U₄ TrueLafẓ MUST be allowed"


def test_u4_true_lafz_to_u5_functional_role_is_allowed():
    """Verify U₄ → U₅ FunctionalRole is allowed."""
    assert is_transition_allowed(
        ExecutionLayer.U4_TRUE_SINGULAR_LAFZ,
        ExecutionLayer.U5_FUNCTIONAL_ROLE
    ), "U₄ TrueLafẓ → U₅ FunctionalRole MUST be allowed"


# ============================================================================
# Test Forbidden Jumps (CRITICAL)
# ============================================================================

def test_u2s_to_functional_role_is_FORBIDDEN():
    """CRITICAL: U₂s → U₅ FunctionalRole is FORBIDDEN."""
    assert not is_transition_allowed(
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U5_FUNCTIONAL_ROLE
    ), "U₂s → FunctionalRole MUST be FORBIDDEN (missing U₃ and U₄)"

    reason = get_forbidden_jump_reason(
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U5_FUNCTIONAL_ROLE
    )
    assert reason is not None, "Forbidden jump must have a reason"
    assert "U₃" in reason or "Boundary" in reason, "Reason must mention missing U₃"
    assert "U₄" in reason or "TrueLafẓ" in reason or "TrueSingular" in reason, "Reason must mention missing U₄"


def test_u2s_to_root_is_FORBIDDEN():
    """CRITICAL: U₂s → U₈ Root is FORBIDDEN."""
    assert not is_transition_allowed(
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U8_ROOT_STEM
    ), "U₂s → Root MUST be FORBIDDEN (missing 6 layers)"

    reason = get_forbidden_jump_reason(
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U8_ROOT_STEM
    )
    assert reason is not None, "Forbidden jump must have a reason"


def test_u2s_to_weight_is_FORBIDDEN():
    """CRITICAL: U₂s → U₉ Weight is FORBIDDEN."""
    assert not is_transition_allowed(
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U9_WEIGHT
    ), "U₂s → Weight MUST be FORBIDDEN (missing 7 layers)"

    reason = get_forbidden_jump_reason(
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U9_WEIGHT
    )
    assert reason is not None, "Forbidden jump must have a reason"


def test_u3_boundary_to_u5_functional_role_is_FORBIDDEN():
    """U₃ → U₅ is forbidden (missing U₄)."""
    assert not is_transition_allowed(
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        ExecutionLayer.U5_FUNCTIONAL_ROLE
    ), "U₃ Boundary → U₅ FunctionalRole MUST be FORBIDDEN (missing U₄ TrueLafẓ)"

    reason = get_forbidden_jump_reason(
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        ExecutionLayer.U5_FUNCTIONAL_ROLE
    )
    assert reason is not None, "Forbidden jump must have a reason"
    assert "U₄" in reason or "TrueLafẓ" in reason or "TrueSingular" in reason, "Reason must mention missing U₄"


# ============================================================================
# Test Required Intermediate Layers
# ============================================================================

def test_get_required_intermediate_layers_u2s_to_u5():
    """Verify required intermediate layers from U₂s to U₅."""
    intermediate = get_required_intermediate_layers(
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U5_FUNCTIONAL_ROLE
    )

    # Must include U₃ and U₄
    assert ExecutionLayer.U3_BOUNDARY_ATTACHMENT in intermediate, "Must include U₃ Boundary"
    assert ExecutionLayer.U4_TRUE_SINGULAR_LAFZ in intermediate, "Must include U₄ TrueLafẓ"
    assert len(intermediate) == 2, "Should be exactly 2 intermediate layers"


def test_get_required_intermediate_layers_u2s_to_u8():
    """Verify required intermediate layers from U₂s to U₈ Root."""
    intermediate = get_required_intermediate_layers(
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U8_ROOT_STEM
    )

    # Must include all 6 intermediate layers
    expected = {
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        ExecutionLayer.U4_TRUE_SINGULAR_LAFZ,
        ExecutionLayer.U5_FUNCTIONAL_ROLE,
        ExecutionLayer.U6_MABNI_CLOSED_CLASS,
        ExecutionLayer.U7_PRE_WEIGHT_CONTRACT,
    }

    for layer in expected:
        assert layer in intermediate, f"Must include {layer}"

    assert len(intermediate) == 5, "Should be exactly 5 intermediate layers"


# ============================================================================
# Test Sequence Validation
# ============================================================================

def test_validate_correct_sequence():
    """Verify validation passes for correct layer sequence."""
    correct_sequence = [
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        ExecutionLayer.U4_TRUE_SINGULAR_LAFZ,
        ExecutionLayer.U5_FUNCTIONAL_ROLE,
    ]

    is_valid, error = validate_layer_sequence(correct_sequence)
    assert is_valid, f"Correct sequence should be valid. Error: {error}"


def test_validate_rejects_u2s_to_functional_role_jump():
    """CRITICAL: Verify validation rejects U₂s → U₅ jump."""
    invalid_sequence = [
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U5_FUNCTIONAL_ROLE,  # JUMP! Missing U₃ and U₄
    ]

    is_valid, error = validate_layer_sequence(invalid_sequence)
    assert not is_valid, "Should reject U₂s → U₅ jump"
    assert error is not None, "Should have error message"
    error_lower = error.lower()
    assert "u2s" in error_lower or "syllable" in error_lower, "Error should mention source"
    assert "u5" in error_lower or "functional" in error_lower, "Error should mention target"


def test_validate_rejects_u2s_to_root_jump():
    """CRITICAL: Verify validation rejects U₂s → U₈ Root jump."""
    invalid_sequence = [
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U8_ROOT_STEM,  # JUMP! Missing 6 layers
    ]

    is_valid, error = validate_layer_sequence(invalid_sequence)
    assert not is_valid, "Should reject U₂s → U₈ jump"
    assert error is not None, "Should have error message"


def test_validate_rejects_u3_to_u5_jump():
    """Verify validation rejects U₃ → U₅ jump (missing U₄)."""
    invalid_sequence = [
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        ExecutionLayer.U5_FUNCTIONAL_ROLE,  # JUMP! Missing U₄
    ]

    is_valid, error = validate_layer_sequence(invalid_sequence)
    assert not is_valid, "Should reject U₃ → U₅ jump"
    assert error is not None, "Should have error message"


# ============================================================================
# Test Legacy Mapping
# ============================================================================

def test_legacy_u3_functional_role_maps_to_u5():
    """Verify legacy U₃ FunctionalRole maps to canonical U₅."""
    canonical = get_canonical_layer("legacy_u3_functional_role")
    assert canonical == ExecutionLayer.U5_FUNCTIONAL_ROLE, (
        "Legacy U₃ FunctionalRole should map to canonical U₅"
    )


def test_nonexistent_legacy_returns_none():
    """Verify nonexistent legacy names return None."""
    canonical = get_canonical_layer("nonexistent_layer")
    assert canonical is None, "Nonexistent legacy layer should return None"


# ============================================================================
# Test Critical Architectural Invariants
# ============================================================================

def test_no_layer_allows_jump_over_boundary():
    """CRITICAL: No layer can jump over U₃ Boundary to reach higher layers."""
    # U₂s cannot reach any layer beyond U₃ without going through U₃
    for layer in EXECUTION_LAYER_ORDER:
        if layer in {
            ExecutionLayer.U0_UNICODE,
            ExecutionLayer.U1_GRAPHEME,
            ExecutionLayer.U2P_PHONETIC_PROJECTION,
            ExecutionLayer.U2S_ARABIC_SYLLABLE,
            ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        }:
            continue

        # U₂s → layer should not be directly allowed
        if layer != ExecutionLayer.U3_BOUNDARY_ATTACHMENT:
            assert not is_transition_allowed(
                ExecutionLayer.U2S_ARABIC_SYLLABLE,
                layer
            ), f"U₂s → {layer} should not be directly allowed (must go through U₃)"


def test_no_layer_allows_jump_over_true_lafz():
    """CRITICAL: After U₃, must go through U₄ before reaching U₅+."""
    # U₃ cannot reach any layer beyond U₄ without going through U₄
    for layer in EXECUTION_LAYER_ORDER:
        if layer in {
            ExecutionLayer.U0_UNICODE,
            ExecutionLayer.U1_GRAPHEME,
            ExecutionLayer.U2P_PHONETIC_PROJECTION,
            ExecutionLayer.U2S_ARABIC_SYLLABLE,
            ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
            ExecutionLayer.U4_TRUE_SINGULAR_LAFZ,
        }:
            continue

        # U₃ → layer should not be directly allowed
        if layer != ExecutionLayer.U4_TRUE_SINGULAR_LAFZ:
            assert not is_transition_allowed(
                ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
                layer
            ), f"U₃ → {layer} should not be directly allowed (must go through U₄)"


def test_functional_role_is_not_u3():
    """CRITICAL META-TEST: Verify FunctionalRole is U₅, not U₃."""
    # This test documents the architectural correction
    assert ExecutionLayer.U5_FUNCTIONAL_ROLE.value == "u5_functional_role", (
        "FunctionalRole must be U₅"
    )

    assert ExecutionLayer.U3_BOUNDARY_ATTACHMENT.value == "u3_boundary_attachment", (
        "U₃ must be BoundaryAndAttachment"
    )

    # Verify they are in correct order
    u3_idx = EXECUTION_LAYER_ORDER.index(ExecutionLayer.U3_BOUNDARY_ATTACHMENT)
    u5_idx = EXECUTION_LAYER_ORDER.index(ExecutionLayer.U5_FUNCTIONAL_ROLE)
    assert u3_idx < u5_idx, "U₃ must come before U₅"


# ============================================================================
# Integration Test
# ============================================================================

def test_full_canonical_path_u2s_to_u5():
    """Integration test: Verify full canonical path from U₂s to U₅."""
    path = [
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        ExecutionLayer.U4_TRUE_SINGULAR_LAFZ,
        ExecutionLayer.U5_FUNCTIONAL_ROLE,
    ]

    is_valid, error = validate_layer_sequence(path)
    assert is_valid, f"Canonical path should be valid. Error: {error}"


def test_integration_all_transitions_in_path_allowed():
    """Verify every transition in canonical path is individually allowed."""
    path = [
        ExecutionLayer.U2S_ARABIC_SYLLABLE,
        ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
        ExecutionLayer.U4_TRUE_SINGULAR_LAFZ,
        ExecutionLayer.U5_FUNCTIONAL_ROLE,
    ]

    for i in range(len(path) - 1):
        from_layer = path[i]
        to_layer = path[i + 1]
        assert is_transition_allowed(from_layer, to_layer), (
            f"Transition {from_layer.value} → {to_layer.value} should be allowed"
        )
