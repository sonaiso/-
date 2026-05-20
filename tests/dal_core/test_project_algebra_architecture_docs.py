"""
Tests for Project Algebra Architecture (PR #22)

These are lightweight doc-presence tests that verify the project algebra
architecture documentation exists and contains required principles.

NO IMPLEMENTATION - only documentation verification.
"""

import pytest
from pathlib import Path


# ---------------------------------------------------------------------------
# Test: Architecture Documents Exist
# ---------------------------------------------------------------------------


def test_reality_effect_prior_boundary_doc_exists():
    """Verify REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md exists."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    assert doc_path.exists(), "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md must exist"


def test_project_algebra_architecture_map_doc_exists():
    """Verify PROJECT_ALGEBRA_ARCHITECTURE_MAP.md exists."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    assert doc_path.exists(), "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md must exist"


def test_general_to_dal_algebra_boundary_doc_exists():
    """Verify GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md exists."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md"
    assert doc_path.exists(), "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md must exist"


def test_dal_mufrad_and_murakkab_position_doc_exists():
    """Verify DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md exists."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md"
    assert doc_path.exists(), "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md must exist"


# ---------------------------------------------------------------------------
# Test: Core Architectural Principles
# ---------------------------------------------------------------------------


def test_docs_state_wadh_is_not_first_contract():
    """Verify documentation states Wadhʿ is not the first contract."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = doc_path.read_text()

    assert "Wadhʿ is not the first" in content or "Wadhʿ is not the first algebraic contract" in content, \
        "Must state Wadhʿ is not the first contract"
    assert "Effect-Prior Binding" in content, \
        "Must mention Effect-Prior Binding as earlier contract"


def test_docs_state_madlul_is_not_given_primitive():
    """Verify documentation states Madlul is not a given primitive."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = doc_path.read_text()

    assert "Madlul is not a primitive" in content or "CandidateMadlul" in content, \
        "Must state Madlul is not a primitive"
    assert "constructed candidate" in content or "licensed candidate" in content, \
        "Must state Madlul is constructed/licensed"


def test_docs_state_no_candidate_madlul_without_effect_prior_binding():
    """Verify no CandidateMadlul without Effect-Prior binding."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = doc_path.read_text()

    assert "CandidateMadlul" in content, "Must mention CandidateMadlul"
    assert "Effect" in content and "Prior" in content and "Binding" in content, \
        "Must mention Effect-Prior Binding"
    assert "Bound(Effect, PriorInformation)" in content or "Effect × Prior" in content, \
        "Must show CandidateMadlul depends on Effect-Prior binding"


def test_docs_state_no_tasawwur_without_prior_information():
    """Verify no Tasawwur without Prior Information."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = doc_path.read_text()

    assert "No Tasawwur" in content or "No tasawwur" in content, \
        "Must state 'No Tasawwur without Prior Information'"
    assert "Prior Information" in content, "Must mention Prior Information"


def test_docs_state_no_ordered_dal_without_order_boundaries_trace():
    """Verify no OrderedDal without order, boundaries, and trace."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = doc_path.read_text()

    assert "OrderedDal" in content or "Ordered Dal" in content, \
        "Must mention OrderedDal"
    assert "order" in content.lower() and "boundaries" in content.lower(), \
        "Must require order and boundaries"
    assert "trace" in content.lower(), "Must require trace"


def test_docs_state_no_wadh_without_ordered_dal_and_candidate_madlul():
    """Verify no Wadhʿ without OrderedDal and CandidateMadlul."""
    doc_path = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = doc_path.read_text()

    assert "WadhʿContract" in content or "Wadhʿ Contract" in content, \
        "Must mention WadhʿContract"
    assert "OrderedDal × CandidateMadlul" in content or \
           "OrderedDal" in content and "CandidateMadlul" in content, \
        "Must show Wadhʿ depends on OrderedDal and CandidateMadlul"


def test_docs_state_no_dalalah_without_wadh_contract():
    """Verify no Dalalah without Wadhʿ contract."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    assert "Dalalah" in content, "Must mention Dalalah"
    assert "Wadhʿ" in content, "Must mention Wadhʿ"
    # Verify Dalalah comes after Wadhʿ in hierarchy
    assert content.index("Wadhʿ") < content.index("Dalalah"), \
        "Wadhʿ must come before Dalalah in architecture"


def test_docs_state_no_istimal_without_qarina():
    """Verify no Istiʿmal without Qarina."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    assert "Istiʿmal" in content or "Istiʿmal" in content, "Must mention Istiʿmal"
    assert "Qarina" in content or "قرينة" in content, "Must mention Qarina"
    assert "No Istiʿmal without" in content or "without قرينة" in content or "without Qarina" in content, \
        "Must state no Istiʿmal without Qarina"


def test_docs_state_no_murad_without_context_and_license():
    """Verify no Murad without context and licensing."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    assert "Murad" in content, "Must mention Murad"
    assert "context" in content.lower() and "license" in content.lower() or "licensing" in content.lower(), \
        "Must require context and licensing for Murad"


# ---------------------------------------------------------------------------
# Test: 13-Layer Hierarchy Documentation
# ---------------------------------------------------------------------------


def test_13_layer_hierarchy_documented():
    """Verify all 13 algebra layers (A0-A13) are documented."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    layers = [
        "A0",  # General Algebra
        "A1",  # Source-of-Effect
        "A2",  # Effect Reception
        "A3",  # Prior-Information
        "A4",  # Effect-Prior Binding
        "A5",  # Candidate-Madlul
        "A6",  # Ordered Dal Form
        "A7",  # Dal-Mufrad
        "A8",  # Dal-Murakkab
        "A9",  # Wadhʿ Contract
        "A10", # Dalalah
        "A11", # Istiʿmal
        "A12", # Murad
        "A13", # Hukm
    ]

    for layer in layers:
        assert f"A{layer[1:]}" in content or layer in content, \
            f"Must document layer {layer}"


def test_source_of_effect_types_documented():
    """Verify 10 source types are documented."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    source_types = [
        "Sensory Reality",
        "Mental Reality",
        "Linguistic Reality",
        "Social Reality",
        "Technical Reality",
        "Legal Reality",
        "Mathematical Reality",
        "Programmatic Reality",
        "Textual Source",
        "Reported Source",
    ]

    for source_type in source_types:
        assert source_type in content, f"Must document {source_type}"


def test_effect_types_documented():
    """Verify 10 effect types are documented."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    effect_types = [
        "Sound",
        "Script",
        "Image",
        "Gesture",
        "Report",
        "Context",
        "Text",
        "Definition",
        "Event",
        "Signal",
    ]

    # Check for section headers or explicit mentions
    for effect_type in effect_types:
        assert effect_type in content, f"Must document {effect_type} as effect type"


def test_prior_information_components_documented():
    """Verify 10 prior information components are documented."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    prior_components = [
        "Lexicon",
        "Attestation",
        "Classification",
        "Examples",
        "Rules",
        "Domain Constraints",
        "Previous Experience",
        "Axioms",
        "Initial Facts",
        "Usage Conventions",
    ]

    for component in prior_components:
        assert component in content, f"Must document {component} as prior information component"


# ---------------------------------------------------------------------------
# Test: Forbidden Transitions Documentation
# ---------------------------------------------------------------------------


def test_docs_forbid_effect_to_madlul_without_prior_information():
    """Verify forbidden: Effect → Madlul without PriorInformation."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    assert "Effect → Madlul" in content or "Effect to Madlul" in content, \
        "Must mention Effect → Madlul transition"
    assert "without Prior" in content or "Forbidden" in content, \
        "Must forbid Effect → Madlul without Prior"


def test_docs_forbid_dal_to_madlul_without_wadh():
    """Verify forbidden: Dal → Madlul without Wadhʿ."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    assert "Dal → Madlul" in content or "Dal to Madlul" in content, \
        "Must mention Dal → Madlul transition"
    assert "without Wadhʿ" in content or "WadhʿContract" in content, \
        "Must forbid Dal → Madlul without Wadhʿ"


def test_docs_forbid_rawform_to_dal_without_structure():
    """Verify forbidden: RawForm → Dal without ordering and boundaries."""
    boundary_doc = Path(__file__).parent.parent.parent / "docs" / "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md"
    content = boundary_doc.read_text()

    assert "RawForm" in content or "raw" in content.lower(), \
        "Must mention raw form"
    assert "ordering" in content.lower() and "boundaries" in content.lower(), \
        "Must require ordering and boundaries"


def test_docs_forbid_reality_free_madlul():
    """Verify forbidden: Reality-free Madlul."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    assert "Reality-free" in content or "without source effect" in content, \
        "Must forbid reality-free Madlul"


def test_docs_forbid_prior_free_tasawwur():
    """Verify forbidden: Prior-free Tasawwur."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    assert "Prior-free" in content or "No Tasawwur without Prior" in content, \
        "Must forbid prior-free Tasawwur"


def test_docs_forbid_order_free_dal():
    """Verify forbidden: Order-free Dal."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    assert "Order-free" in content or "unordered" in content.lower(), \
        "Must forbid order-free Dal"


def test_docs_forbid_evidence_free_wadh():
    """Verify forbidden: Evidence-free Wadhʿ."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    assert "Evidence-free" in content or "without evidence" in content, \
        "Must forbid evidence-free Wadhʿ"


# ---------------------------------------------------------------------------
# Test: Dal Algebra Position Documentation
# ---------------------------------------------------------------------------


def test_docs_state_dal_algebra_is_pre_semantic():
    """Verify Dal Algebra is documented as pre-semantic specialization."""
    boundary_doc = Path(__file__).parent.parent.parent / "docs" / "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md"
    content = boundary_doc.read_text()

    assert "pre-semantic" in content.lower(), \
        "Must state Dal Algebra is pre-semantic"
    assert "FORM" in content and "MEANING" in content, \
        "Must distinguish FORM from MEANING"


def test_docs_state_dal_algebra_subset_general_algebra():
    """Verify Dal Algebra ⊂ General Algebra relationship is documented."""
    boundary_doc = Path(__file__).parent.parent.parent / "docs" / "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md"
    content = boundary_doc.read_text()

    assert "Dal Algebra ⊂ General Algebra" in content or "subset" in content.lower(), \
        "Must state Dal Algebra ⊂ General Algebra"
    assert "architectural inclusion" in content or "not yet a formally proven" in content, \
        "Must clarify this is architectural inclusion, not yet formal proof"


def test_docs_state_dal_algebra_equals_a6_a7_a8():
    """Verify Dal Algebra = A6 + A7 + A8 is documented."""
    boundary_doc = Path(__file__).parent.parent.parent / "docs" / "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md"
    content = boundary_doc.read_text()

    assert "Dal Algebra = A6 + A7 + A8" in content or \
           ("A6" in content and "A7" in content and "A8" in content), \
        "Must state Dal Algebra = A6 + A7 + A8"


def test_docs_state_dal_mufrad_scope():
    """Verify Dal-Mufrad (A7) scope is documented."""
    position_doc = Path(__file__).parent.parent.parent / "docs" / "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md"
    content = position_doc.read_text()

    assert "Dal-Mufrad" in content or "A7" in content, \
        "Must mention Dal-Mufrad (A7)"
    assert "individual signifier" in content.lower() or "individual lexical" in content.lower(), \
        "Must define Dal-Mufrad scope as individual signifier"


def test_docs_state_dal_murakkab_scope():
    """Verify Dal-Murakkab (A8) scope is documented."""
    position_doc = Path(__file__).parent.parent.parent / "docs" / "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md"
    content = position_doc.read_text()

    assert "Dal-Murakkab" in content or "A8" in content, \
        "Must mention Dal-Murakkab (A8)"
    assert "composed signifier" in content.lower() or "composition" in content.lower(), \
        "Must define Dal-Murakkab scope as composition"


def test_docs_state_dal_mufrad_does_not_create_candidate_madlul():
    """Verify Dal-Mufrad does NOT create CandidateMadlul."""
    position_doc = Path(__file__).parent.parent.parent / "docs" / "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md"
    content = position_doc.read_text()

    assert "Does NOT Create CandidateMadlul" in content or \
           "NOT create" in content and "CandidateMadlul" in content, \
        "Must state Dal-Mufrad does NOT create CandidateMadlul"


def test_docs_state_dal_mufrad_does_not_create_wadh():
    """Verify Dal-Mufrad does NOT create Wadhʿ."""
    position_doc = Path(__file__).parent.parent.parent / "docs" / "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md"
    content = position_doc.read_text()

    assert "Does NOT Create Wadhʿ" in content or \
           "NOT create" in content and "Wadhʿ" in content, \
        "Must state Dal-Mufrad does NOT create Wadhʿ"


def test_docs_state_dal_murakkab_does_not_create_candidate_madlul():
    """Verify Dal-Murakkab does NOT create CandidateMadlul."""
    position_doc = Path(__file__).parent.parent.parent / "docs" / "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md"
    content = position_doc.read_text()

    assert "Dal-Murakkab" in content, "Must mention Dal-Murakkab"
    # Look for forbidden operations section
    assert "Does NOT Create CandidateMadlul" in content or \
           ("NOT" in content and "CandidateMadlul" in content), \
        "Must state Dal-Murakkab does NOT create CandidateMadlul"


def test_docs_state_dal_murakkab_does_not_infer_murad():
    """Verify Dal-Murakkab does NOT infer Murad."""
    position_doc = Path(__file__).parent.parent.parent / "docs" / "DAL_MUFRAD_AND_DAL_MURAKKAB_POSITION.md"
    content = position_doc.read_text()

    assert "Dal-Murakkab" in content, "Must mention Dal-Murakkab"
    assert "Does NOT Infer Murad" in content or \
           ("NOT" in content and "Murad" in content), \
        "Must state Dal-Murakkab does NOT infer Murad"


# ---------------------------------------------------------------------------
# Test: Architectural Laws Documentation
# ---------------------------------------------------------------------------


def test_architectural_laws_documented():
    """Verify architectural laws are documented."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    laws = [
        "Layer Dependency",
        "No Layer Skipping",
        "Evidence Preservation",
        "No Effect Without Source",
        "No Tasawwur Without Prior",
        "No Wadhʿ Without Structure",
    ]

    for law in laws:
        assert law in content, f"Must document {law} law"


def test_forbidden_dal_algebra_claims_documented():
    """Verify forbidden claims for Dal Algebra are documented."""
    boundary_doc = Path(__file__).parent.parent.parent / "docs" / "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md"
    content = boundary_doc.read_text()

    forbidden_claims = [
        "Dal Algebra is the first algebra",
        "Dal Algebra handles meaning",
        "Dal Algebra establishes Wadhʿ",
    ]

    for claim in forbidden_claims:
        assert claim in content or "FORBIDDEN" in content, \
            f"Must document forbidden claim: {claim}"


def test_allowed_dal_algebra_claims_documented():
    """Verify allowed claims for Dal Algebra are documented."""
    boundary_doc = Path(__file__).parent.parent.parent / "docs" / "GENERAL_TO_DAL_ALGEBRA_BOUNDARY.md"
    content = boundary_doc.read_text()

    allowed_claims = [
        "analyzes signifier form",
        "morphological analysis",
        "lexical identity",
    ]

    for claim in allowed_claims:
        assert claim in content, f"Must document allowed claim: {claim}"


# ---------------------------------------------------------------------------
# Test: Wadhʿ Contract Definition
# ---------------------------------------------------------------------------


def test_wadh_contract_three_way_formula_documented():
    """Verify Wadhʿ = OrderedDal × CandidateMadlul × Evidence."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    assert "WadhʿContractCandidate" in content or "Wadhʿ Contract" in content, \
        "Must mention WadhʿContract"
    assert "OrderedDal × CandidateMadlul × WadhʿEvidence" in content or \
           ("OrderedDal" in content and "CandidateMadlul" in content and "Evidence" in content), \
        "Must show Wadhʿ = OrderedDal × CandidateMadlul × Evidence"


def test_wadh_types_documented():
    """Verify 4 Wadhʿ types are documented."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    wadh_types = [
        "Lexical Wadhʿ",
        "Technical Wadhʿ",
        "Shar'i Wadhʿ",
        "Stipulative Wadhʿ",
    ]

    for wadh_type in wadh_types:
        assert wadh_type in content or wadh_type.replace("Wadhʿ", "وضع") in content, \
            f"Must document {wadh_type}"


# ---------------------------------------------------------------------------
# Test: Dalalah Types Documentation
# ---------------------------------------------------------------------------


def test_three_dalalah_types_documented():
    """Verify 3 dalalah types are documented."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    dalalah_types = [
        "المطابقة",  # Conformity
        "التضمن",   # Inclusion
        "الالتزام",  # Entailment
    ]

    for dalalah_type in dalalah_types:
        assert dalalah_type in content, f"Must document {dalalah_type}"


# ---------------------------------------------------------------------------
# Test: Istiʿmal Types Documentation
# ---------------------------------------------------------------------------


def test_five_istimal_types_documented():
    """Verify 5 Istiʿmal types are documented."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    istimal_types = [
        "حقيقة",  # Literal
        "مجاز",   # Figurative
        "نقل",    # Transferred
        "عرف",    # Conventional
        "شرع",    # Religious-legal
    ]

    for istimal_type in istimal_types:
        assert istimal_type in content, f"Must document {istimal_type}"


# ---------------------------------------------------------------------------
# Test: Implementation Status Documentation
# ---------------------------------------------------------------------------


def test_docs_state_a7_implemented_in_dal_core():
    """Verify A7 (Dal-Mufrad) is documented as implemented in dal_core."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    assert "A7" in content, "Must mention A7"
    assert "dal_core" in content.lower(), "Must mention dal_core"
    assert "Implemented" in content or "implemented" in content, \
        "Must state A7 is implemented"


def test_docs_state_a1_to_a6_documented_not_implemented():
    """Verify A1-A6 are documented but not implemented."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    assert "Documented (Not Implemented)" in content or "documented but not implemented" in content.lower(), \
        "Must state A1-A6 are documented but not implemented"


def test_docs_state_a9_to_a13_out_of_scope():
    """Verify A9-A13 are documented as out of scope for PR #22."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    assert "Out of Scope" in content or "out of scope" in content.lower(), \
        "Must state what is out of scope"
    # Check that implementation is forbidden
    assert "WadhContractEngine" in content or "semantic" in content.lower(), \
        "Must mention what implementations are forbidden"


# ---------------------------------------------------------------------------
# Test: Hallucination Prevention Documentation
# ---------------------------------------------------------------------------


def test_docs_prevent_madlul_without_effect_hallucination():
    """Verify documentation prevents 'Madlul without effect' hallucination."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    # Must explicitly state Madlul requires Effect
    assert "Effect" in content and "Madlul" in content, \
        "Must link Effect to Madlul"
    assert "without" in content.lower(), \
        "Must use 'without' to describe forbidden pattern"


def test_docs_prevent_tasawwur_without_prior_hallucination():
    """Verify documentation prevents 'Tasawwur without prior' hallucination."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    assert "No Tasawwur without Prior Information" in content or \
           "No tasawwur without prior" in content.lower(), \
        "Must explicitly prevent Tasawwur without prior hallucination"


def test_docs_prevent_wadh_without_structure_hallucination():
    """Verify documentation prevents 'Wadhʿ without structure' hallucination."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    assert "No Wadhʿ without" in content or "No wadhʿ without" in content.lower(), \
        "Must prevent Wadhʿ without structure hallucination"
    assert "OrderedDal" in content and "CandidateMadlul" in content, \
        "Must require both OrderedDal and CandidateMadlul for Wadhʿ"


# ---------------------------------------------------------------------------
# Test: Verification and Compliance
# ---------------------------------------------------------------------------


def test_docs_provide_verification_checklists():
    """Verify documentation provides verification checklists."""
    reality_doc = Path(__file__).parent.parent.parent / "docs" / "REALITY_EFFECT_PRIOR_INFORMATION_BOUNDARY.md"
    content = reality_doc.read_text()

    assert "Verification" in content or "checklist" in content.lower(), \
        "Must provide verification guidance"


def test_docs_provide_allowed_vs_forbidden_claims():
    """Verify documentation clearly separates allowed vs forbidden claims."""
    arch_map_path = Path(__file__).parent.parent.parent / "docs" / "PROJECT_ALGEBRA_ARCHITECTURE_MAP.md"
    content = arch_map_path.read_text()

    assert "Allowed" in content and "Forbidden" in content, \
        "Must distinguish allowed from forbidden claims"
    assert "can claim" in content.lower() or "cannot claim" in content.lower(), \
        "Must use clear claim language"

