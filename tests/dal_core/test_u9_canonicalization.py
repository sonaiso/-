"""
U₉ Canonicalization Tests (اختبارات توحيد U₉)

Tests enforcing U₉ canonical implementation requirements:
    1. Official U₉ API is importable from dal_core
    2. Legacy u9_arabic_weight path is deprecated
    3. No U₉ execution occurs without ApprovedTransitionContext
    4. Canonical implementation passes constitutional tests

Constitutional Laws Under Test:
    ✓ U₉ has one canonical governed implementation
    ✓ Legacy U₉ must not bypass ApprovedTransitionContext
    ✓ No weight candidate outside u9_weight_candidate_carrier.py

PR: #116 - Canonicalize U₉ WeightCandidateCarrier
Created: 2026-05-26
"""

import pytest
import warnings
from uuid import uuid4

# ============================================================================
# Test 1: Official U₉ API is importable from dal_core
# ============================================================================

def test_official_u9_api_importable_from_dal_core():
    """
    Constitutional Law: Official U₉ API must be importable from dal_core.

    This ensures the canonical implementation is the primary API surface.
    """
    # Import official API from dal_core
    from dal_core import (
        WeightCandidateResult,
        weight_candidate_carrier_9,
        validate_approved_context_for_u9,
    )

    # Verify imports are not None
    assert WeightCandidateResult is not None
    assert weight_candidate_carrier_9 is not None
    assert validate_approved_context_for_u9 is not None

    # Verify they are the correct types
    assert callable(weight_candidate_carrier_9)
    assert callable(validate_approved_context_for_u9)


def test_official_u9_api_is_from_canonical_module():
    """
    Verify official API comes from u9_weight_candidate_carrier module.
    """
    from dal_core import weight_candidate_carrier_9

    # Verify module source
    assert weight_candidate_carrier_9.__module__ == "dal_core.u9_weight_candidate_carrier"


# ============================================================================
# Test 2: Legacy module shows deprecation warning
# ============================================================================

def test_legacy_dispatch_weight_shows_deprecation_warning():
    """
    Constitutional Law: Legacy dispatch_weight() must be BLOCKED, not just warned.

    This enforces constitutional prohibition of ungoverned U₉ execution.
    """
    from dal_core.u9_arabic_weight import dispatch_weight, PreWeightContract, RootStemInput
    from dal_core.evidence import Evidence

    # Create minimal mock inputs
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="UnknownLexical",
        path_type="Muʿrab",
        derivation_access="blocked",
        inflection_access=False,
        evidence=(),
        trace={},
        competitors=frozenset(),
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootCandidate",
        evidence=(),
        trace={},
        pattern_candidate=None,
    )

    # Should raise RuntimeError, not just warn
    with pytest.raises(RuntimeError) as exc_info:
        dispatch_weight(contract, root_stem)

    # Verify error message explains constitutional block
    error_msg = str(exc_info.value)
    assert "Constitutional Violation" in error_msg or "BLOCKED" in error_msg
    assert "ApprovedTransitionContext" in error_msg
    assert "weight_candidate_carrier_9" in error_msg


# ============================================================================
# Test 3: Official API requires ApprovedTransitionContext
# ============================================================================

def test_official_u9_rejects_without_approved_context():
    """
    Constitutional Law: Official U₉ must reject execution without ApprovedTransitionContext.

    This is the primary constitutional defense.
    """
    from dal_core import weight_candidate_carrier_9

    # Mock U₈ input (valid structure)
    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "stem_candidates": ["كتب"],
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    # Attempt to call without ApprovedTransitionContext (context=None)
    with pytest.raises(ValueError) as exc_info:
        weight_candidate_carrier_9(u8_input, approved_context=None)

    # Verify error message
    assert "ApprovedTransitionContext" in str(exc_info.value)
    assert "required" in str(exc_info.value).lower() or "must" in str(exc_info.value).lower()


def test_official_u9_rejects_wrong_transition_context():
    """
    Constitutional Law: Official U₉ must reject wrong transition context.

    Context must be for U₈→U₉ transition specifically.

    Note: This test is simplified to verify the validation logic exists.
    Full integration tests are in test_u9_weight_candidate_constitutional.py
    """
    from dal_core import validate_approved_context_for_u9

    # Mock U₈ input
    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "stem_candidates": ["كتب"],
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    # Test that None context is rejected
    with pytest.raises(ValueError) as exc_info:
        validate_approved_context_for_u9(None, u8_input)

    # Verify error mentions ApprovedTransitionContext
    error_msg = str(exc_info.value)
    assert "ApprovedTransitionContext" in error_msg


# ============================================================================
# Test 4: Verify no AlgebraicDecisionCore instantiation in U9 files
# ============================================================================

def test_no_algebraic_decision_core_instantiation_in_u9_files():
    """
    Constitutional Law: U₉ files must NOT instantiate AlgebraicDecisionCore.

    Layer does not own Governor. Governor owns Transition Permission.
    """
    import ast
    from pathlib import Path

    # Read u9_weight_candidate_carrier.py
    u9_canonical = Path(__file__).parent.parent.parent / "src" / "dal_core" / "u9_weight_candidate_carrier.py"
    u9_legacy = Path(__file__).parent.parent.parent / "src" / "dal_core" / "u9_arabic_weight.py"

    violations = []

    for filepath in [u9_canonical, u9_legacy]:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            tree = ast.parse(content)

        # Check for AlgebraicDecisionCore() instantiation
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id == "AlgebraicDecisionCore":
                        violations.append(f"{filepath.name}: AlgebraicDecisionCore() instantiation found")

    # Assert no violations
    assert len(violations) == 0, f"Constitutional violations found:\n" + "\n".join(violations)


# ============================================================================
# Test 5: Legacy tests still pass (backward compatibility)
# ============================================================================

def test_legacy_module_still_importable():
    """
    Verify legacy module is still importable for backward compatibility.

    This ensures we don't break existing code that imports from u9_arabic_weight.
    """
    # Should not raise ImportError
    from dal_core.u9_arabic_weight import (
        WeightType,
        WeightRank,
        ArabicWeightObject,
        dispatch_weight,
    )

    # Verify types exist
    assert WeightType is not None
    assert WeightRank is not None
    assert ArabicWeightObject is not None
    assert callable(dispatch_weight)


# ============================================================================
# Test 6: Documentation points to official implementation
# ============================================================================

def test_legacy_module_documentation_shows_deprecation():
    """
    Verify legacy module documentation clearly indicates deprecation.
    """
    import dal_core.u9_arabic_weight as legacy_module

    docstring = legacy_module.__doc__
    assert docstring is not None

    # Check for deprecation markers
    assert "DEPRECATED" in docstring or "deprecated" in docstring
    assert "u9_weight_candidate_carrier" in docstring
    assert "ApprovedTransitionContext" in docstring


# ============================================================================
# Test 7: No dual execution paths
# ============================================================================

def test_no_dual_u9_execution_paths():
    """
    Constitutional Law: There must be ONE canonical governed implementation.

    This test ensures:
    1. Official API enforces ApprovedTransitionContext
    2. Legacy API is BLOCKED (raises RuntimeError)
    3. No code can bypass governance
    """
    from dal_core import weight_candidate_carrier_9
    from dal_core.u9_arabic_weight import dispatch_weight

    # Official API requires context
    u8_input = {"root_candidates": [], "stem_candidates": [], "trace": ()}

    with pytest.raises(ValueError):
        weight_candidate_carrier_9(u8_input, approved_context=None)

    # Legacy API is BLOCKED (raises RuntimeError)
    from dal_core.u9_arabic_weight import PreWeightContract, RootStemInput

    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="UnknownLexical",
        path_type="Muʿrab",
        derivation_access="blocked",
        inflection_access=False,
        evidence=(),
        trace={},
        competitors=frozenset(),
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootCandidate",
        evidence=(),
        trace={},
        pattern_candidate=None,
    )

    # Must raise RuntimeError, not just warn
    with pytest.raises(RuntimeError) as exc_info:
        dispatch_weight(contract, root_stem)

    assert "Constitutional" in str(exc_info.value) or "BLOCKED" in str(exc_info.value)


# ============================================================================
# Test 8: Explicit constitutional block test
# ============================================================================

def test_legacy_dispatch_weight_cannot_produce_weight_without_approved_context():
    """
    Constitutional Law Enforcement Test:

    Legacy dispatch_weight() CANNOT produce a weight object without ApprovedTransitionContext.
    This is not a deprecation - it's a constitutional block.

    The function MUST raise RuntimeError, preventing any weight candidate production
    outside the governed canonical implementation.

    Critical: This test proves NO legacy execution path exists.
    """
    from dal_core.u9_arabic_weight import dispatch_weight, PreWeightContract, RootStemInput

    # Attempt to create weight via legacy path
    contract = PreWeightContract(
        build_status="MuʿrabCandidate",
        lexical_status="UnknownLexical",
        path_type="Muʿrab",
        derivation_access="blocked",
        inflection_access=False,
        evidence=(),
        trace={},
        competitors=frozenset(),
    )

    root_stem = RootStemInput(
        root_or_stem=("ك", "ت", "ب"),
        input_type="root",
        root_status="RootCandidate",
        evidence=(),
        trace={},
        pattern_candidate=None,
    )

    # CRITICAL: Must raise RuntimeError, not return any weight object
    with pytest.raises(RuntimeError) as exc_info:
        weight_obj = dispatch_weight(contract, root_stem)
        # If we reach here, the constitutional block failed
        pytest.fail("Constitutional violation: dispatch_weight() produced a weight object without ApprovedTransitionContext")

    # Verify the error is a constitutional block, not a runtime accident
    error_msg = str(exc_info.value)
    assert "Constitutional" in error_msg, "Error must explicitly state constitutional violation"
    assert "BLOCKED" in error_msg or "prohibited" in error_msg, "Error must indicate execution is blocked"
    assert "ApprovedTransitionContext" in error_msg, "Error must reference governance requirement"
    assert "weight_candidate_carrier_9" in error_msg, "Error must guide to official implementation"
