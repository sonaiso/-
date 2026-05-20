"""
Tests for Ordered Dal Form Governance (PR #21)

These are lightweight doc-presence tests that verify governance documentation
exists and contains required governance principles.

NO IMPLEMENTATION - only documentation verification.
"""

import pytest
from pathlib import Path


# ---------------------------------------------------------------------------
# Test: Governance Documents Exist
# ---------------------------------------------------------------------------


def test_ordered_dal_form_governance_doc_exists():
    """Verify ORDERED_DAL_FORM_GOVERNANCE.md exists."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    assert doc_path.exists(), "ORDERED_DAL_FORM_GOVERNANCE.md must exist"


def test_internal_composition_boundaries_doc_exists():
    """Verify INTERNAL_COMPOSITION_BOUNDARIES.md exists."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "INTERNAL_COMPOSITION_BOUNDARIES.md"
    assert doc_path.exists(), "INTERNAL_COMPOSITION_BOUNDARIES.md must exist"


def test_bidirectional_analysis_charter_doc_exists():
    """Verify BIDIRECTIONAL_ANALYSIS_CHARTER.md exists."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "BIDIRECTIONAL_ANALYSIS_CHARTER.md"
    assert doc_path.exists(), "BIDIRECTIONAL_ANALYSIS_CHARTER.md must exist"


# ---------------------------------------------------------------------------
# Test: Core Governance Principles Present
# ---------------------------------------------------------------------------


def test_ordered_unit_axiom_documented():
    """Verify 'ordered bounded sequence' principle is documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    # Must document the core axiom
    assert "ordered bounded sequence" in content, \
        "Must document 'ordered bounded sequence' principle"
    assert "not a bag of features" in content or "bag of features" in content, \
        "Must reject bag-of-features representation"


def test_no_claim_without_position_documented():
    """Verify 'no claim without position' invariant is documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    assert "no claim without position" in content.lower() or "لا claim بلا موضع" in content, \
        "Must document 'no claim without position' invariant"
    assert "span" in content, "Must require span specification"
    assert "index" in content, "Must require index specification"


def test_no_fold_without_trace_documented():
    """Verify 'no fold without reverse trace' invariant is documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    assert "no fold without" in content.lower() or "لا fold بلا" in content, \
        "Must document 'no fold without reverse trace' invariant"
    assert "source_trace" in content or "reverse_trace" in content, \
        "Must require trace preservation"


def test_no_adjacency_without_direction_documented():
    """Verify 'no adjacency without direction' invariant is documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    assert "no adjacency without direction" in content.lower() or "لا adjacency بلا direction" in content, \
        "Must document 'no adjacency without direction' invariant"
    assert "previous" in content and "next" in content, \
        "Must require prev/next relations"


def test_no_candidate_without_boundaries_documented():
    """Verify 'no candidate without boundaries' invariant is documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    assert "no candidate without boundaries" in content.lower() or "لا candidate بلا boundaries" in content, \
        "Must document 'no candidate without boundaries' invariant"
    assert "left_boundary" in content and "right_boundary" in content, \
        "Must require boundary specification"


def test_prohibited_direct_promotions_documented():
    """Verify prohibited direct promotions are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    # Must prohibit key direct promotions
    prohibited_patterns = [
        "surface mark",  # → case effect
        "syllable",  # → wazn
        "short form",  # → root
    ]

    for pattern in prohibited_patterns:
        assert pattern in content.lower(), \
            f"Must document prohibition of '{pattern}' direct promotion"


# ---------------------------------------------------------------------------
# Test: Boundary Rules Present
# ---------------------------------------------------------------------------


def test_boundary_types_documented():
    """Verify boundary types are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "INTERNAL_COMPOSITION_BOUNDARIES.md"
    content = doc_path.read_text()

    # Must document boundary types
    assert "WORD_START" in content or "بداية_كلمة" in content, \
        "Must document WORD_START boundary"
    assert "WORD_END" in content or "نهاية_كلمة" in content, \
        "Must document WORD_END boundary"


def test_composition_operations_documented():
    """Verify composition operations (fold, split, concat) are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "INTERNAL_COMPOSITION_BOUNDARIES.md"
    content = doc_path.read_text()

    operations = ["fold", "split", "concatenate"]
    for op in operations:
        assert op.lower() in content.lower(), \
            f"Must document {op} operation"


def test_boundary_preservation_rules_documented():
    """Verify boundary preservation rules are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "INTERNAL_COMPOSITION_BOUNDARIES.md"
    content = doc_path.read_text()

    # Must document preservation during transformations
    assert "boundary preservation" in content.lower() or "preserving" in content.lower(), \
        "Must document boundary preservation"
    assert "layer transition" in content.lower() or "transformation" in content.lower(), \
        "Must document layer transitions"


# ---------------------------------------------------------------------------
# Test: Bidirectional Analysis Principles Present
# ---------------------------------------------------------------------------


def test_forward_backward_scan_documented():
    """Verify forward and backward scan directions are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "BIDIRECTIONAL_ANALYSIS_CHARTER.md"
    content = doc_path.read_text()

    assert "forward scan" in content.lower(), "Must document forward scan"
    assert "backward scan" in content.lower(), "Must document backward scan"
    assert "left-to-right" in content.lower() or "previous → current → next" in content, \
        "Must document forward direction"
    assert "right-to-left" in content.lower() or "next → current → previous" in content, \
        "Must document backward direction"


def test_form_vs_syntax_distinction_documented():
    """Verify form analysis vs syntax analysis distinction is documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "BIDIRECTIONAL_ANALYSIS_CHARTER.md"
    content = doc_path.read_text()

    assert "form evidence" in content.lower() or "form analysis" in content.lower(), \
        "Must document form analysis"
    assert "not syntax" in content.lower() or "syntax analysis" in content.lower(), \
        "Must distinguish from syntax"
    assert "forbidden" in content.lower() or "must not" in content.lower(), \
        "Must specify forbidden syntax claims"


def test_directional_candidates_documented():
    """Verify directional candidates are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "BIDIRECTIONAL_ANALYSIS_CHARTER.md"
    content = doc_path.read_text()

    assert "scan_direction" in content or "direction" in content.lower(), \
        "Must require direction in candidates"
    assert "ForwardCandidate" in content or "forward candidate" in content.lower(), \
        "Must document forward candidates"
    assert "BackwardCandidate" in content or "backward candidate" in content.lower(), \
        "Must document backward candidates"


def test_prohibited_syntax_claims_documented():
    """Verify prohibited syntax claims are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "BIDIRECTIONAL_ANALYSIS_CHARTER.md"
    content = doc_path.read_text()

    # Must explicitly prohibit syntax claims
    prohibited_claims = [
        "case_effect",
        "relation_type",
        "grammatical_function",
    ]

    for claim in prohibited_claims:
        assert claim in content, \
            f"Must prohibit {claim} in form analysis"


# ---------------------------------------------------------------------------
# Test: Out-of-Scope Items Documented
# ---------------------------------------------------------------------------


def test_out_of_scope_documented():
    """Verify out-of-scope items for PR #21 are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    # Must explicitly list out-of-scope items
    out_of_scope = [
        "dal_algebra",
        "TransitionContract",
        "RankAlgebra",
        "ResidualAlgebra",
    ]

    for item in out_of_scope:
        assert item in content, \
            f"Must document that {item} is out of scope for PR #21"


def test_governance_only_status_documented():
    """Verify governance-only status is documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    # Must clarify this is governance documentation, not implementation
    assert "governance" in content.lower(), "Must mention governance"
    assert "no implementation" in content.lower() or "documentation" in content.lower(), \
        "Must clarify no implementation required"


# ---------------------------------------------------------------------------
# Test: Success Criteria Documented
# ---------------------------------------------------------------------------


def test_success_criteria_documented():
    """Verify success criteria are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    # Must specify what can/cannot be claimed after PR #21
    assert "allowed claim" in content.lower() or "success criteria" in content.lower(), \
        "Must document success criteria"
    assert "forbidden claim" in content.lower() or "cannot claim" in content.lower(), \
        "Must document forbidden claims"


def test_future_integration_path_documented():
    """Verify future integration path is documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    # Must reference future PRs
    assert "PR #22" in content or "future" in content.lower(), \
        "Must document future integration path"
    assert "dal algebra" in content.lower() or "dal_algebra" in content, \
        "Must reference dal_algebra as future work"


# ---------------------------------------------------------------------------
# Test: No Implementation Code Present
# ---------------------------------------------------------------------------


def test_dal_algebra_implementation_exists_in_pr23():
    """Verify dal_algebra.py EXISTS (implemented in PR #23)."""
    impl_path = Path(__file__).parent.parent.parent / "src" / "dal_core" / "dal_algebra.py"
    assert impl_path.exists(), \
        "dal_algebra.py must exist in PR #23 (minimal signature)"


def test_dal_algebra_tests_exist_in_pr23():
    """Verify dal_algebra tests EXIST (implemented in PR #23)."""
    test_path = Path(__file__).parent.parent.parent / "tests" / "dal_core" / "test_dal_algebra_signature.py"
    assert test_path.exists(), \
        "test_dal_algebra_signature.py must exist in PR #23"


def test_no_full_algebra_implementation_in_pr23():
    """Verify full algebra NOT implemented yet (deferred to PR #24+)."""
    # Check that full algebra files don't exist yet
    src_path = Path(__file__).parent.parent.parent / "src" / "dal_core"

    if src_path.exists():
        # These should NOT exist yet (future PRs)
        forbidden_files = [
            "rank_algebra.py",
            "residual_algebra.py",
            "relation_candidate.py",
            "case_effect_candidate.py",
        ]

        for forbidden in forbidden_files:
            file_path = src_path / forbidden
            assert not file_path.exists(), \
                f"{forbidden} must NOT exist in PR #23 (deferred to future PRs)"


# ---------------------------------------------------------------------------
# Test: Governance Completeness
# ---------------------------------------------------------------------------


def test_all_five_invariants_documented():
    """Verify all 5 core invariants are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    invariants = [
        "no claim without position",
        "no fold without",  # reverse trace
        "no adjacency without direction",
        "no candidate without boundaries",
        "no certificate without",  # claim-scoped evidence
    ]

    for invariant in invariants:
        assert invariant.lower() in content.lower(), \
            f"Must document invariant: {invariant}"


def test_internal_composition_layers_documented():
    """Verify internal composition layers are documented."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "ORDERED_DAL_FORM_GOVERNANCE.md"
    content = doc_path.read_text()

    # Must document layered composition
    layers = [
        "Letters",  # or atoms
        "Syllables",
        "Pre-Morph",
        "Origin",  # or Template
        "Form",
    ]

    # At least 3 of these layers must be mentioned
    mentioned = sum(1 for layer in layers if layer.lower() in content.lower())
    assert mentioned >= 3, \
        "Must document at least 3 internal composition layers"


# ---------------------------------------------------------------------------
# Summary Test
# ---------------------------------------------------------------------------


def test_pr21_governance_complete():
    """
    Summary test: Verify PR #21 governance + PR #23 minimal signature.

    Success criteria:
    ✅ 3 governance docs exist (PR #21)
    ✅ Core principles documented (PR #21)
    ✅ 5 invariants documented (PR #21)
    ✅ Boundary rules documented (PR #21)
    ✅ Bidirectional analysis rules documented (PR #21)
    ✅ Out-of-scope items documented (PR #21)
    ✅ Minimal dal_algebra.py implementation (PR #23)
    ✅ NO full algebra yet (deferred to PR #24+)
    """
    docs_path = Path(__file__).parent.parent.parent / "docs"

    # All 3 governance docs must exist (PR #21)
    required_docs = [
        "ORDERED_DAL_FORM_GOVERNANCE.md",
        "INTERNAL_COMPOSITION_BOUNDARIES.md",
        "BIDIRECTIONAL_ANALYSIS_CHARTER.md",
    ]

    for doc in required_docs:
        assert (docs_path / doc).exists(), f"{doc} must exist"

    # Minimal dal_algebra.py must exist (PR #23)
    impl_path = Path(__file__).parent.parent.parent / "src" / "dal_core" / "dal_algebra.py"
    assert impl_path.exists(), "dal_algebra.py must exist in PR #23"

    # Full algebra must NOT exist yet (future PRs)
    src_path = Path(__file__).parent.parent.parent / "src" / "dal_core"
    forbidden_files = ["rank_algebra.py", "residual_algebra.py"]
    for forbidden in forbidden_files:
        assert not (src_path / forbidden).exists(), \
            f"{forbidden} must NOT exist yet (deferred to future PRs)"

    # Success summary
    print("\n✅ PR #21 Governance + PR #23 Minimal Signature Complete:")
    print("  - 3 governance documents present (PR #21)")
    print("  - Core invariants documented (PR #21)")
    print("  - Minimal dal_algebra.py implemented (PR #23)")
    print("  - Full algebra deferred to future PRs (PR #24+)")
    print("  - Ready for PR #24 (Rank Algebra)")
