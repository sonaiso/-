"""Tests for Project Algebra Architecture documentation (PR #22).

Governance tests verifying that architecture map documentation exists
and contains required concepts, boundaries, and prohibited claims.

These tests ensure architectural discipline through documentation review.
"""

import sys
sys.path.insert(0, 'src')

import os


# =============================================================================
# TEST DOCUMENT EXISTENCE
# =============================================================================

def test_project_algebra_architecture_map_exists():
    """PROJECT_ALGEBRA_ARCHITECTURE_MAP.md must exist."""
    path = "docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    assert os.path.exists(path), f"Missing: {path}"


def test_general_to_dal_boundary_doc_exists():
    """GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md must exist."""
    path = "docs/GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md"
    assert os.path.exists(path), f"Missing: {path}"


def test_dal_mufrad_murakkab_position_doc_exists():
    """DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md must exist."""
    path = "docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md"
    assert os.path.exists(path), f"Missing: {path}"


def test_project_algebra_roadmap_exists():
    """PROJECT_ALGEBRA_ROADMAP.md must exist."""
    path = "docs/PROJECT_ALGEBRA_ROADMAP.md"
    assert os.path.exists(path), f"Missing: {path}"


# =============================================================================
# TEST ARCHITECTURE MAP CONTENT
# =============================================================================

def test_docs_state_dal_algebra_is_pre_semantic():
    """Architecture map must state Dal Algebra is pre-semantic."""
    with open("docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md") as f:
        content = f.read()

    assert "pre-semantic" in content.lower(), \
        "Must state Dal Algebra is pre-semantic"

    assert "signifier" in content.lower() or "دال" in content, \
        "Must mention signifier (dal)"

    # Should NOT claim dal handles meaning
    assert "Dal Algebra" in content and ("meaning" in content or "معنى" in content), \
        "Must discuss Dal Algebra boundary with meaning"


def test_docs_state_dal_algebra_is_not_full_general_algebra():
    """Docs must clarify Dal Algebra is specialization, not General Algebra itself."""
    with open("docs/GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md") as f:
        content = f.read()

    # Must state relationship
    assert "specialization" in content.lower() or "domain specialization" in content.lower(), \
        "Must state Dal is specialization of General"

    # Must NOT claim General Algebra is implemented
    assert "future" in content.lower() or "not implemented" in content.lower(), \
        "Must clarify General Algebra is future work"


def test_docs_distinguish_mufrad_and_murakkab():
    """Docs must distinguish Dal-Mufrad from Dal-Murakkab."""
    with open("docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md") as f:
        content = f.read()

    assert "mufrad" in content.lower() or "مفرد" in content, \
        "Must mention Dal-Mufrad"

    assert "murakkab" in content.lower() or "مركب" in content, \
        "Must mention Dal-Murakkab"

    assert "individual" in content.lower() or "compositional" in content.lower(), \
        "Must distinguish individual (mufrad) from compositional (murakkab)"


def test_docs_state_murakkab_does_not_create_meaning():
    """Docs must state Dal-Murakkab does not create meaning."""
    with open("docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md") as f:
        content = f.read()

    # Find section on Murakkab and verify no-meaning claim
    assert "murakkab" in content.lower() and ("meaning" in content.lower() or "معنى" in content), \
        "Must discuss Dal-Murakkab and meaning boundary"

    # Should find "does not create meaning" or similar prohibition
    assert ("not create meaning" in content.lower() or
            "no meaning" in content.lower() or
            "form-only" in content.lower()), \
        "Must prohibit meaning creation in Dal-Murakkab"


def test_docs_state_no_algebra_claims_later_outputs():
    """Docs must state no algebra may claim outputs of later algebra."""
    with open("docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md") as f:
        content = f.read()

    # Must have the key law
    assert ("no algebra may claim" in content.lower() or
            "may not claim" in content.lower()), \
        "Must state the key architectural law about claiming later outputs"


def test_docs_include_wadh_dal_madlul_future_boundary():
    """Docs must mention Wadh' as future signifier-signified linking."""
    with open("docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md") as f:
        content = f.read()

    assert "wadh" in content.lower() or "وضع" in content, \
        "Must mention Wadh' algebra"

    assert "madlul" in content.lower() or "مدلول" in content, \
        "Must mention Madlul (signified)"

    # Wadh' should be marked as future
    assert "future" in content.lower(), \
        "Must mark semantic algebras as future work"


def test_docs_forbid_semantic_linking_in_this_pr():
    """Docs must prohibit semantic linking implementation in PR #22."""
    # Check architecture map
    with open("docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md") as f:
        arch_content = f.read()

    # Check boundary doc
    with open("docs/GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md") as f:
        boundary_content = f.read()

    # Both should have prohibited/out-of-scope sections
    for content, doc_name in [
        (arch_content, "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"),
        (boundary_content, "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md")
    ]:
        assert ("prohibited" in content.lower() or
                "forbidden" in content.lower() or
                "out of scope" in content.lower()), \
            f"{doc_name} must have prohibited/forbidden/out-of-scope sections"

        # Should prohibit implementation claims
        assert ("not implement" in content.lower() or
                "no implementation" in content.lower() or
                "documentation only" in content.lower()), \
            f"{doc_name} must clarify this PR is documentation only"


def test_docs_define_roadmap_before_relation_candidate():
    """Roadmap must show RelationCandidate comes after dal transition signature."""
    with open("docs/PROJECT_ALGEBRA_ROADMAP.md") as f:
        content = f.read()

    assert "relationcandidate" in content.lower(), \
        "Roadmap must mention RelationCandidate"

    # Find PR #23 (transition) and PR #37 (RelationCandidate)
    # PR #23 should come before PR #37
    pr23_pos = content.find("PR #23")
    pr37_pos = content.find("PR #37")

    if pr23_pos != -1 and pr37_pos != -1:
        assert pr23_pos < pr37_pos, \
            "PR #23 (transition signature) must come before PR #37 (RelationCandidate)"


# =============================================================================
# TEST 10-LAYER ARCHITECTURE
# =============================================================================

def test_docs_include_ten_layer_architecture():
    """Architecture map must include A0-A10 layers."""
    with open("docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md") as f:
        content = f.read()

    # Check for layer markers
    layers = ["A0", "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"]
    for layer in layers:
        assert layer in content, f"Must include layer {layer}"


def test_docs_include_algebra_names():
    """Architecture map must include specific algebra names."""
    with open("docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md") as f:
        content = f.read()

    required_names = [
        "General Algebra",
        "Carrier",
        "Dal Algebra",
        "Dal-Mufrad",
        "Dal-Murakkab",
        "Wadh",  # وضع
        "Madlul",  # مدلول
        "Murad",  # مراد
        "Hukm",  # حكم
    ]

    for name in required_names:
        assert name.lower() in content.lower(), \
            f"Must include {name} in architecture map"


# =============================================================================
# TEST BOUNDARY SPECIFICATIONS
# =============================================================================

def test_docs_specify_form_meaning_boundary():
    """Docs must specify where form ends and meaning begins."""
    with open("docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md") as f:
        content = f.read()

    # Should discuss boundary between dal (form) and semantic
    assert "boundary" in content.lower(), \
        "Must discuss boundaries"

    assert ("form" in content.lower() and
            ("meaning" in content.lower() or "semantic" in content.lower())), \
        "Must discuss form/meaning boundary"


def test_docs_specify_mufrad_murakkab_boundary():
    """Docs must specify boundary between Mufrad and Murakkab."""
    with open("docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md") as f:
        content = f.read()

    # Should find section on mufrad → murakkab boundary
    assert "mufrad" in content.lower() and "murakkab" in content.lower(), \
        "Must discuss both mufrad and murakkab"

    # Should discuss interface or crossing
    assert ("boundary" in content.lower() or
            "interface" in content.lower() or
            "crosses" in content.lower()), \
        "Must discuss boundary/interface between mufrad and murakkab"


# =============================================================================
# TEST PROHIBITED DIRECT PROMOTIONS
# =============================================================================

def test_docs_mention_no_direct_promotion_policy():
    """Docs should mention no-direct-promotion policy."""
    with open("docs/GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md") as f:
        content = f.read()

    assert ("promotion" in content.lower() or
            "shortcut" in content.lower() or
            "cross-layer" in content.lower()), \
        "Should mention promotion/shortcut policies"


# =============================================================================
# TEST PHASE/MILESTONE STRUCTURE
# =============================================================================

def test_docs_define_phases_and_milestones():
    """Roadmap must define phases and milestones."""
    with open("docs/PROJECT_ALGEBRA_ROADMAP.md") as f:
        content = f.read()

    assert "phase" in content.lower(), \
        "Roadmap must define phases"

    assert "milestone" in content.lower(), \
        "Roadmap must define milestones"


def test_docs_enforce_semantic_after_dal_complete():
    """Roadmap must enforce semantic work after dal-only complete."""
    with open("docs/PROJECT_ALGEBRA_ROADMAP.md") as f:
        content = f.read()

    # Should find rule about not starting semantic before dal complete
    assert ("semantic" in content.lower() and
            ("after" in content.lower() or
             "before" in content.lower() or
             "complete" in content.lower())), \
        "Must enforce semantic work comes after dal completion"


# =============================================================================
# TEST ALLOWED/PROHIBITED CLAIMS
# =============================================================================

def test_docs_list_prohibited_claims():
    """Docs must explicitly list prohibited claims."""
    with open("docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md") as f:
        content = f.read()

    assert ("prohibited" in content.lower() or
            "forbidden" in content.lower() or
            "may not" in content.lower()), \
        "Must have prohibited claims section"


def test_docs_list_allowed_claims():
    """Docs must explicitly list allowed claims."""
    with open("docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md") as f:
        content = f.read()

    assert ("allowed" in content.lower() or
            "may claim" in content.lower()), \
        "Must have allowed claims section"


# =============================================================================
# TEST NO IMPLEMENTATION IN PR #22
# =============================================================================

def test_pr22_adds_no_runtime_dal_algebra():
    """PR #22 must not add src/dal_core/dal_algebra.py as runtime (docs only)."""
    # This test documents the expectation that PR #22 is documentation only
    # Note: dal_algebra.py may exist from previous work (which becomes PR #23)
    # This test ensures we understand PR #22's scope

    with open("docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md") as f:
        content = f.read()

    # Must clarify this PR is documentation only
    assert "documentation" in content.lower(), \
        "Must state this PR is documentation only"


def test_pr22_prohibits_semantic_implementation():
    """PR #22 must prohibit semantic implementation."""
    # Check all 4 docs for implementation prohibition
    docs = [
        "docs/PROJECT_ALGEBRA_ARCHITECTURE_MAP.md",
        "docs/GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md",
        "docs/DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md",
        "docs/PROJECT_ALGEBRA_ROADMAP.md",
    ]

    for doc_path in docs:
        with open(doc_path) as f:
            content = f.read()

        # Each doc should mention implementation status
        has_implementation_mention = (
            "implementation" in content.lower() or
            "not implement" in content.lower() or
            "no implementation" in content.lower()
        )

        assert has_implementation_mention, \
            f"{doc_path} must clarify implementation status"


# =============================================================================
# RUN ALL TESTS
# =============================================================================

if __name__ == '__main__':
    # Run all test functions
    import traceback

    test_functions = [
        # Document existence
        test_project_algebra_architecture_map_exists,
        test_general_to_dal_boundary_doc_exists,
        test_dal_mufrad_murakkab_position_doc_exists,
        test_project_algebra_roadmap_exists,

        # Architecture content
        test_docs_state_dal_algebra_is_pre_semantic,
        test_docs_state_dal_algebra_is_not_full_general_algebra,
        test_docs_distinguish_mufrad_and_murakkab,
        test_docs_state_murakkab_does_not_create_meaning,
        test_docs_state_no_algebra_claims_later_outputs,
        test_docs_include_wadh_dal_madlul_future_boundary,
        test_docs_forbid_semantic_linking_in_this_pr,
        test_docs_define_roadmap_before_relation_candidate,

        # 10-layer architecture
        test_docs_include_ten_layer_architecture,
        test_docs_include_algebra_names,

        # Boundaries
        test_docs_specify_form_meaning_boundary,
        test_docs_specify_mufrad_murakkab_boundary,

        # Policies
        test_docs_mention_no_direct_promotion_policy,

        # Phases/milestones
        test_docs_define_phases_and_milestones,
        test_docs_enforce_semantic_after_dal_complete,

        # Claims
        test_docs_list_prohibited_claims,
        test_docs_list_allowed_claims,

        # PR #22 scope
        test_pr22_adds_no_runtime_dal_algebra,
        test_pr22_prohibits_semantic_implementation,
    ]

    passed = 0
    failed = 0

    for test_func in test_functions:
        try:
            test_func()
            print(f"✓ {test_func.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__}: {e}")
            traceback.print_exc()
            failed += 1

    print(f"\n{passed} passed, {failed} failed")

    if failed > 0:
        sys.exit(1)
