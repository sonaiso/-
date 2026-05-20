"""
Test PR #22: Project Algebra Architecture Map Documentation

Governance tests verifying architecture documentation exists and contains
required principles.

These tests verify DOCUMENTATION ONLY (no runtime implementation).
"""

import os
import pytest


# Path to docs directory
DOCS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "docs")


def read_doc(filename: str) -> str:
    """Read documentation file content"""
    filepath = os.path.join(DOCS_DIR, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


# ============================================================================
# File Existence Tests
# ============================================================================


def test_project_algebra_architecture_map_exists():
    """Verify PROJECT_ALGEBRA_ARCHITECTURE_MAP.md exists"""
    filepath = os.path.join(DOCS_DIR, "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")
    assert os.path.exists(filepath), "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md must exist"


def test_typed_transition_algebra_kernel_doc_exists():
    """Verify TYPED_TRANSITION_ALGEBRA_KERNEL.md exists"""
    filepath = os.path.join(DOCS_DIR, "TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    assert os.path.exists(filepath), "TYPED_TRANSITION_ALGEBRA_KERNEL.md must exist"


def test_general_to_dal_boundary_doc_exists():
    """Verify GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md exists"""
    filepath = os.path.join(DOCS_DIR, "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md")
    assert os.path.exists(filepath), "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md must exist"


def test_dal_mufrad_murakkab_position_doc_exists():
    """Verify DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md exists"""
    filepath = os.path.join(DOCS_DIR, "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md")
    assert os.path.exists(filepath), "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md must exist"


def test_project_algebra_roadmap_exists():
    """Verify PROJECT_ALGEBRA_ROADMAP.md exists"""
    filepath = os.path.join(DOCS_DIR, "PROJECT_ALGEBRA_ROADMAP.md")
    assert os.path.exists(filepath), "PROJECT_ALGEBRA_ROADMAP.md must exist"


# ============================================================================
# Kernel Documentation Tests
# ============================================================================


def test_docs_define_successful_typed_objects_carrier():
    """Verify docs define carrier as successful typed objects"""
    content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    assert "𝔾 = successful typed objects" in content
    assert "Carrier" in content or "carrier" in content


def test_docs_state_failure_not_in_carrier():
    """Verify docs state Failure ∉ 𝔾"""
    content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    assert "Failure ∉ 𝔾" in content or "Failure is not an element" in content


def test_docs_define_transition_as_candidate_set_or_failure():
    """Verify docs define transitions returning CandidateSet or Failure"""
    content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    assert "CandidateSet" in content
    assert "Failure" in content
    assert "Ω" in content or "transition" in content.lower()


def test_docs_state_no_global_certificate():
    """Verify docs state no global certificate"""
    content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    assert "no global certificate" in content.lower() or "No Global Certificate" in content


def test_docs_define_claim_scoped_proof_object():
    """Verify docs define claim-scoped ProofObject"""
    content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    assert "ProofObject" in content
    assert "claim_scope" in content or "claim-scoped" in content


def test_docs_state_equivalence_is_domain_scoped():
    """Verify docs state equivalence is domain-scoped"""
    content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    assert "domain-scoped" in content.lower() or "Domain-Scoped Equivalence" in content
    assert "equivalence" in content.lower()


def test_docs_state_no_global_neutral_element():
    """Verify docs state no global neutral element"""
    content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    assert "no global neutral" in content.lower() or "No Global Neutral" in content


def test_docs_state_associativity_is_conditional():
    """Verify docs state composition associativity is conditional"""
    content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    assert "conditional" in content.lower() and "associativity" in content.lower()


def test_docs_state_metrics_do_not_grant_certificate():
    """Verify docs state metrics do not grant certificate"""
    content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    assert "metrics" in content.lower()
    assert ("0.97" in content and "certificate" in content.lower()) or \
           "metrics assist but do not govern" in content.lower() or \
           "Metrics Assist But Do Not Govern" in content


# ============================================================================
# Architecture Map Tests
# ============================================================================


def test_docs_define_11_layer_architecture():
    """Verify docs define 11-layer architecture (A0-A10)"""
    content = read_doc("PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")
    # Check for layer references
    assert "A0" in content
    assert "A1" in content
    assert "A10" in content or "Hukm" in content


def test_docs_state_dal_algebra_is_pre_semantic():
    """Verify docs state Dal Algebra is pre-semantic"""
    content = read_doc("PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")
    assert "pre-semantic" in content.lower() or "Pre-Semantic" in content


def test_docs_position_dal_mufrad_as_a3():
    """Verify docs position Dal-Mufrad as A3"""
    content = read_doc("PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")
    assert "A3" in content
    assert "Dal-Mufrad" in content or "Mufrad" in content


def test_docs_position_dal_murakkab_as_a4():
    """Verify docs position Dal-Murakkab as A4"""
    content = read_doc("PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")
    assert "A4" in content
    assert "Dal-Murakkab" in content or "Murakkab" in content


def test_docs_position_wadh_as_a5():
    """Verify docs position Wadh' as A5"""
    content = read_doc("PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")
    assert "A5" in content
    assert "Wadh" in content or "وضع" in content


def test_docs_state_no_algebra_claims_later_outputs():
    """Verify docs state no algebra claims later outputs"""
    content = read_doc("PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")
    assert "no algebra may claim" in content.lower() or \
           "No algebra may claim the outputs of a later algebra" in content


# ============================================================================
# Dal-Mufrad and Dal-Murakkab Tests
# ============================================================================


def test_docs_distinguish_mufrad_and_murakkab():
    """Verify docs distinguish Dal-Mufrad and Dal-Murakkab"""
    content = read_doc("DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md")
    assert "Dal-Mufrad" in content or "Mufrad" in content
    assert "Dal-Murakkab" in content or "Murakkab" in content


def test_docs_state_mufrad_closes_individual_signifier():
    """Verify docs state Mufrad closes individual signifier"""
    content = read_doc("DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md")
    assert "individual" in content.lower() or "single" in content.lower()
    assert "signifier" in content.lower() or "dal" in content.lower()


def test_docs_state_murakkab_composes_closed_signifiers():
    """Verify docs state Murakkab composes closed signifiers"""
    content = read_doc("DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md")
    assert "compose" in content.lower() or "composition" in content.lower()


def test_docs_state_murakkab_does_not_create_meaning():
    """Verify docs state Murakkab does not create meaning"""
    content = read_doc("DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md")
    assert "does not create meaning" in content.lower() or \
           "does NOT create meaning" in content or \
           "NOT create meaning" in content


def test_docs_state_murakkab_inherits_mufrad_residuals():
    """Verify docs state Murakkab inherits Mufrad residuals"""
    content = read_doc("DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md")
    assert "inherit" in content.lower() and "residual" in content.lower()


def test_docs_state_murakkab_preserves_mufrad_competitors():
    """Verify docs state Murakkab preserves Mufrad competitors"""
    content = read_doc("DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md")
    assert "preserve" in content.lower() and "competitor" in content.lower()


def test_docs_state_murakkab_does_not_raise_mufrad_rank():
    """Verify docs state Murakkab does not raise Mufrad rank"""
    content = read_doc("DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md")
    assert ("does not raise" in content.lower() or "does NOT raise" in content) and \
           "rank" in content.lower()


# ============================================================================
# Boundary Documentation Tests
# ============================================================================


def test_docs_state_general_algebra_is_future():
    """Verify docs state General Algebra is future"""
    content = read_doc("GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md")
    assert "future" in content.lower() or "Future" in content
    assert "General Algebra" in content


def test_docs_state_dal_is_architectural_inclusion():
    """Verify docs state Dal is architectural inclusion (not proven subalgebra)"""
    content = read_doc("GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md")
    assert "architectural inclusion" in content.lower() or \
           "Architectural Inclusion" in content


def test_docs_forbid_overclaim_complete_algebra():
    """Verify docs forbid overclaim of 'complete algebra'"""
    content = read_doc("GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md")
    assert "FORBIDDEN" in content or "forbidden" in content.lower()
    assert "complete" in content.lower()


def test_docs_include_wadh_dal_madlul_future_boundary():
    """Verify docs include Wadh' as dal-madlul boundary"""
    content = read_doc("PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")
    assert "Wadh" in content or "وضع" in content
    assert "boundary" in content.lower() or "Boundary" in content


def test_docs_forbid_semantic_linking_in_this_pr():
    """Verify docs forbid semantic linking in this PR"""
    kernel_content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    boundary_content = read_doc("GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md")

    # Check either doc mentions semantic linking is out of scope
    assert "semantic" in kernel_content.lower() or "semantic" in boundary_content.lower()
    assert ("out of scope" in kernel_content.lower() or "Out of Scope" in kernel_content) or \
           ("out of scope" in boundary_content.lower() or "Out of Scope" in boundary_content)


# ============================================================================
# Roadmap Tests
# ============================================================================


def test_roadmap_defines_pr_sequence():
    """Verify roadmap defines PR sequence"""
    content = read_doc("PROJECT_ALGEBRA_ROADMAP.md")
    assert "PR #22" in content
    assert "PR #23" in content


def test_roadmap_includes_foundation_algebras():
    """Verify roadmap includes foundation algebras"""
    content = read_doc("PROJECT_ALGEBRA_ROADMAP.md")
    assert "Rank Algebra" in content or "rank" in content.lower()
    assert "Residual Algebra" in content or "residual" in content.lower()


def test_roadmap_includes_dal_candidate_layers():
    """Verify roadmap includes dal candidate layers"""
    content = read_doc("PROJECT_ALGEBRA_ROADMAP.md")
    # Check for some domain references
    assert "Graphophonemic" in content or "D0" in content
    assert "Syllable" in content or "Syllabic" in content or "D1" in content


def test_roadmap_includes_wadh_boundary_work():
    """Verify roadmap includes Wadh' boundary work"""
    content = read_doc("PROJECT_ALGEBRA_ROADMAP.md")
    assert "Wadh" in content or "وضع" in content
    assert "boundary" in content.lower() or "Boundary" in content


def test_roadmap_states_current_pr_is_22():
    """Verify roadmap states current PR is #22"""
    content = read_doc("PROJECT_ALGEBRA_ROADMAP.md")
    assert "PR #22" in content
    assert "Current" in content or "current" in content


# ============================================================================
# Out of Scope Verification
# ============================================================================


def test_docs_state_no_runtime_implementation_in_pr22():
    """Verify docs state no runtime implementation in PR #22"""
    kernel_content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    roadmap_content = read_doc("PROJECT_ALGEBRA_ROADMAP.md")

    # Check kernel doc states out of scope
    assert "Out of Scope" in kernel_content or "out of scope" in kernel_content.lower()

    # Check roadmap states PR #22 is docs only
    assert ("documentation" in roadmap_content.lower() or "Documentation" in roadmap_content) and \
           "PR #22" in roadmap_content


def test_docs_state_no_semantic_understanding_claimed():
    """Verify docs do not claim semantic understanding"""
    # Check all major docs
    for filename in [
        "TYPED_TRANSITION_ALGEBRA_KERNEL.md",
        "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md",
        "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md",
        "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md"
    ]:
        content = read_doc(filename)

        # Should have forbidden claims section
        if "Forbidden" in content or "forbidden" in content.lower():
            # If forbidden section exists, should mention semantic understanding
            if "forbidden" in content.lower() and "claim" in content.lower():
                # Good - has forbidden claims documented
                assert "semantic" in content.lower() or "meaning" in content.lower()


# ============================================================================
# Allowed vs Forbidden Claims Tests
# ============================================================================


def test_docs_have_allowed_claim_section():
    """Verify docs have 'Allowed Claim' sections"""
    kernel_content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    map_content = read_doc("PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")

    assert "Allowed Claim" in kernel_content or "allowed claim" in kernel_content.lower()
    assert "Allowed Claim" in map_content or "allowed claim" in map_content.lower()


def test_docs_have_forbidden_claim_section():
    """Verify docs have 'Forbidden Claim' sections"""
    kernel_content = read_doc("TYPED_TRANSITION_ALGEBRA_KERNEL.md")
    map_content = read_doc("PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")

    assert "Forbidden Claim" in kernel_content or "forbidden claim" in kernel_content.lower()
    assert "Forbidden Claim" in map_content or "forbidden claim" in map_content.lower()


def test_forbidden_claims_include_semantic_understanding():
    """Verify forbidden claims include semantic understanding"""
    content = read_doc("PROJECT_ALGEBRA_ARCHITECTURE_MAP.md")
    # Find forbidden section
    if "Forbidden Claim" in content:
        forbidden_section_start = content.index("Forbidden Claim")
        forbidden_section = content[forbidden_section_start:forbidden_section_start + 500]
        assert "semantic" in forbidden_section.lower() or "meaning" in forbidden_section.lower()


def test_forbidden_claims_include_complete_algebra():
    """Verify forbidden claims include 'complete algebra'"""
    boundary_content = read_doc("GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md")
    if "Forbidden" in boundary_content or "forbidden" in boundary_content.lower():
        assert "complete" in boundary_content.lower()


# ============================================================================
# Cross-Document Consistency Tests
# ============================================================================


def test_all_docs_mention_typed_transition():
    """Verify all docs mention typed transitions"""
    for filename in [
        "TYPED_TRANSITION_ALGEBRA_KERNEL.md",
        "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md",
    ]:
        content = read_doc(filename)
        assert "typed" in content.lower() or "Typed" in content


def test_all_docs_reference_pr22():
    """Verify all docs reference PR #22"""
    for filename in [
        "TYPED_TRANSITION_ALGEBRA_KERNEL.md",
        "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md",
        "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md",
        "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md",
        "PROJECT_ALGEBRA_ROADMAP.md"
    ]:
        content = read_doc(filename)
        assert "PR #22" in content or "PR #22" in content


def test_all_docs_have_version_and_status():
    """Verify all docs have version and status"""
    for filename in [
        "TYPED_TRANSITION_ALGEBRA_KERNEL.md",
        "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md",
        "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md",
        "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md",
        "PROJECT_ALGEBRA_ROADMAP.md"
    ]:
        content = read_doc(filename)
        # Check for version and status indicators
        has_version = "Version" in content or "version" in content.lower()
        has_status = "Status" in content or "status" in content.lower()
        assert has_version or has_status, f"{filename} should have version/status"


# ============================================================================
# Summary Test
# ============================================================================


def test_all_required_concepts_documented():
    """Verify all required concepts are documented somewhere"""
    # Read all docs
    all_content = ""
    for filename in [
        "TYPED_TRANSITION_ALGEBRA_KERNEL.md",
        "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md",
        "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md",
        "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md",
        "PROJECT_ALGEBRA_ROADMAP.md"
    ]:
        all_content += read_doc(filename).lower()

    # Required concepts
    required_concepts = [
        "carrier",
        "transition",
        "candidateset",
        "failure",
        "proof",
        "rank",
        "residual",
        "trace",
        "evidence",
        "domain",
        "equivalence",
        "composition",
        "dal-mufrad",
        "dal-murakkab",
        "wadh",
    ]

    for concept in required_concepts:
        assert concept.lower() in all_content, f"Concept '{concept}' must be documented"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
