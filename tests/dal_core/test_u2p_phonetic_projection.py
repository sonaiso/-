"""
Tests for U₂p PhoneticProjectionCarrier phonetic candidate projection.

Positive tests: Valid phonetic projection
Negative tests: Violations of projection laws
No-layer-jump tests: Verify forbidden operations
"""

import pytest
from dal_core.u2p_phonetic_projection import (
    PhoneticProjection,
    PhoneticClass,
    PhoneticPolicy,
    PolicyType,
    PhoneticProjectionLayerObject,
    project_grapheme_to_phonetic,
    cpb2p_validate,
    grapheme_to_phonetic_layer
)
from dal_core.u1_grapheme_carrier import (
    GraphemeCluster,
    GraphemeClass,
    GraphemeLayerObject,
    unicode_to_grapheme_layer
)
from dal_core.u0_unicode_carrier import text_to_unicode_layer
from dal_core.foundation import Rank
from dal_core.residuals import ResidualType, ResidualSeverity


# ============================================================================
# Test Helpers
# ============================================================================

def make_test_grapheme(base: str, marks: list, position: int = 0) -> GraphemeCluster:
    """Create test grapheme cluster."""
    from uuid import uuid4
    return GraphemeCluster(
        id=str(uuid4()),
        base=base,
        marks=frozenset(marks),
        position=position,
        grapheme_class=GraphemeClass.CONSONANT_WITH_VOWEL if marks else GraphemeClass.CONSONANT_BARE,
        trace_0=frozenset([f"u0_{base}"]),
        residuals=frozenset(),
        rank=Rank.CERTIFICATE,
        metadata=(("test", "grapheme"),)
    )


# ============================================================================
# Positive Tests
# ============================================================================

def test_positive_1_ka_with_fatha():
    """
    Positive Test 1: كَ → C + V

    Expected:
        - phonetic_class = CONSONANT or SHORT_VOWEL
        - consonant_candidate = /k/
        - short_vowel_candidate = /a/
        - rank = CERTIFICATE
    """
    cluster = make_test_grapheme('ك', ['\u064E'])  # كَ

    result = project_grapheme_to_phonetic(cluster)

    assert result.success
    assert result.projection is not None
    assert result.projection.consonant_candidate == '/k/'
    assert result.projection.short_vowel_candidate == '/a/'
    assert result.projection.rank == Rank.CERTIFICATE
    assert len(result.projection.trace_1) == 1


def test_positive_2_ba_with_sukun():
    """
    Positive Test 2: بْ → C + closure candidate

    Expected:
        - phonetic_class = CLOSURE
        - consonant_candidate = /b/
        - closure_candidate = True
        - rank = CERTIFICATE (with residual for deferred nucleus)
    """
    cluster = make_test_grapheme('ب', ['\u0652'])  # بْ

    result = project_grapheme_to_phonetic(cluster)

    assert result.success
    assert result.projection is not None
    assert result.projection.consonant_candidate == '/b/'
    assert result.projection.closure_candidate is True
    assert result.projection.phonetic_class == PhoneticClass.CLOSURE
    # Should have warning residual about needing nucleus
    assert len(result.projection.residuals) > 0


def test_positive_3_nun_with_shadda_fatha():
    """
    Positive Test 3: نَّ → C + V + gemination candidate

    Expected:
        - consonant_candidate = /n/
        - short_vowel_candidate = /a/
        - gemination_candidate = True
        - shadda_policy declared
        - rank = HYPOTHESIS (policy unresolved)
    """
    cluster = make_test_grapheme('ن', ['\u0651', '\u064E'])  # نَّ

    result = project_grapheme_to_phonetic(cluster)

    assert result.success
    assert result.projection is not None
    assert result.projection.consonant_candidate == '/n/'
    assert result.projection.short_vowel_candidate == '/a/'
    assert result.projection.gemination_candidate is True
    assert result.projection.phonetic_class == PhoneticClass.GEMINATION

    # Should have shadda policy declared
    assert len(result.projection.policies) > 0
    has_shadda_policy = any(p.policy_type == PolicyType.SHADDA_POLICY for p in result.projection.policies)
    assert has_shadda_policy

    # Rank should be HYPOTHESIS (policy not resolved)
    assert result.projection.rank == Rank.HYPOTHESIS


def test_positive_4_qaf_alif_long_vowel():
    """
    Positive Test 4: قَ + ا → potential VV candidate

    Note: This test checks that فتحة + ا can form long vowel candidate.
    The actual VV formation happens when both are analyzed together.
    """
    cluster_qaf = make_test_grapheme('ق', ['\u064E'], position=0)  # قَ
    cluster_alif = make_test_grapheme('ا', [], position=1)  # ا

    # Project قَ
    result_qaf = project_grapheme_to_phonetic(cluster_qaf, next_cluster=cluster_alif)

    assert result_qaf.success
    assert result_qaf.projection.consonant_candidate == '/q/'
    assert result_qaf.projection.short_vowel_candidate == '/a/'

    # Project ا (should be ambiguous carrier)
    result_alif = project_grapheme_to_phonetic(cluster_alif)

    assert result_alif.success
    assert result_alif.projection.phonetic_class == PhoneticClass.AMBIGUOUS_CARRIER
    assert result_alif.projection.has_competitor()
    # Alif has competitors: long vowel carrier vs hamza carrier
    assert len(result_alif.projection.competitors) > 0


def test_positive_5_full_word_pipeline():
    """
    Positive Test 5: Full pipeline كَتَبَ

    Expected:
        - 3 phonetic projections
        - All with C + V
        - All certified
    """
    text = "كَتَبَ"
    u0_result = text_to_unicode_layer(text)
    assert u0_result.valid

    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    assert u1_result.valid

    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    assert u2p_result.valid
    assert u2p_result.layer_object is not None

    projections = list(u2p_result.layer_object.projections)
    assert len(projections) == 3  # كَ، تَ، بَ

    for proj in projections:
        assert proj.consonant_candidate is not None
        assert proj.short_vowel_candidate == '/a/'


def test_positive_6_proof_object():
    """
    Positive Test 6: ProofObject creation

    Expected:
        - Proof contains claim
        - Forbidden gates documented
        - Rank vector shows phonetic_rank certified
        - Limitations documented
    """
    text = "كَ"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    assert u2p_result.valid
    assert u2p_result.layer_object.proof is not None

    proof = u2p_result.layer_object.proof

    assert proof.claim == "Phonetic projections formed and preserved"
    assert proof.scope == "U₂p / PhoneticProjectionCarrier"

    # Check forbidden gates
    assert "root_certificate" in proof.forbidden_next_gates
    assert "weight_certificate" in proof.forbidden_next_gates
    assert "meaning_certificate" in proof.forbidden_next_gates
    assert "hukm_certificate" in proof.forbidden_next_gates

    # Check allowed gates (only syllabify_2p2s)
    assert "syllabify_2p2s" in proof.allowed_next_gates
    assert len(proof.allowed_next_gates) == 1

    # Check rank vector
    assert proof.rank_vector["unicode_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["grapheme_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["phonetic_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["syllable_rank"] == Rank.ZERO
    assert proof.rank_vector["pattern_weight_rank"] == Rank.ZERO

    # Check limitations
    assert "No syllable formation" in proof.limitations
    assert "No morphological analysis" in proof.limitations


# ============================================================================
# Negative Tests
# ============================================================================

def test_negative_1_alif_alone_no_vv_certificate():
    """
    Negative Test 1: ا alone must NOT certify VV

    Expected:
        - ا → long_vowel_carrier_candidate
        - competitors preserved
        - rank = CANDIDATE (not CERTIFICATE)
        - No VV certificate
    """
    cluster = make_test_grapheme('ا', [])  # ا alone

    result = project_grapheme_to_phonetic(cluster)

    assert result.success
    assert result.projection is not None

    # Should be ambiguous carrier
    assert result.projection.phonetic_class == PhoneticClass.AMBIGUOUS_CARRIER

    # Should have competitors
    assert result.projection.has_competitor()
    assert len(result.projection.competitors) > 0

    # Should NOT be certified
    assert result.projection.rank != Rank.CERTIFICATE
    assert result.projection.rank == Rank.CANDIDATE


def test_negative_2_waw_alone_competitors_preserved():
    """
    Negative Test 2: و alone must preserve competitors

    Expected:
        - competitors = {consonant_/w/, long_vowel_carrier_/ū/}
        - rank = CANDIDATE
        - No certificate without context
    """
    cluster = make_test_grapheme('و', [])  # و alone

    result = project_grapheme_to_phonetic(cluster)

    assert result.success
    assert result.projection is not None

    # Should be ambiguous
    assert result.projection.phonetic_class == PhoneticClass.AMBIGUOUS_CARRIER

    # Should have competitors
    assert result.projection.has_competitor()
    competitors = result.projection.competitors
    assert "consonant_/w/" in competitors or "long_vowel_carrier_/ū/" in competitors

    # Not certified
    assert result.projection.rank == Rank.CANDIDATE


def test_negative_3_sukun_no_syllable_certificate():
    """
    Negative Test 3: بْ must NOT certify syllable

    Expected:
        - C + closure candidate
        - Residual: needs nucleus for syllable
        - No syllable_certificate in proof
    """
    text = "بْ"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    assert u2p_result.valid
    proof = u2p_result.layer_object.proof

    # Should NOT have syllable certificate
    assert "syllable_certificate" not in proof.allowed_next_gates
    assert "syllable_certificate" in proof.forbidden_next_gates or \
           "syllable_certificate" not in proof.allowed_next_gates


def test_negative_4_tanween_policy_unresolved():
    """
    Negative Test 4: Tanween requires policy declaration

    Expected:
        - TanweenPolicy declared
        - candidates = {waqf, wasl}
        - rank = HYPOTHESIS (unresolved)
    """
    cluster = make_test_grapheme('ب', ['\u064C'])  # بٌ (dammatan)

    result = project_grapheme_to_phonetic(cluster)

    assert result.success
    assert result.projection is not None
    assert result.projection.phonetic_class == PhoneticClass.TANWEEN

    # Should have tanween policy
    assert len(result.projection.policies) > 0
    has_tanween = any(p.policy_type == PolicyType.TANWEEN_POLICY for p in result.projection.policies)
    assert has_tanween

    # Not certified (policy unresolved)
    assert result.projection.rank == Rank.HYPOTHESIS


# ============================================================================
# No-Layer-Jump Tests
# ============================================================================

def test_no_layer_jump_1_no_syllable_fields():
    """
    No-Layer-Jump Test 1: PhoneticProjection has no syllable fields

    PhoneticProjection should NOT contain:
        - onset
        - nucleus
        - coda
        - syllable_pattern
    """
    cluster = make_test_grapheme('ك', ['\u064E'])
    result = project_grapheme_to_phonetic(cluster)
    projection = result.projection

    # Should NOT have syllable structure fields
    assert not hasattr(projection, 'onset')
    assert not hasattr(projection, 'nucleus')
    assert not hasattr(projection, 'coda')
    assert not hasattr(projection, 'syllable_pattern')


def test_no_layer_jump_2_no_morphological_fields():
    """
    No-Layer-Jump Test 2: PhoneticProjection has no root/weight fields

    PhoneticProjection should NOT contain:
        - root
        - radicals
        - pattern
        - weight
    """
    cluster = make_test_grapheme('ك', ['\u064E'])
    result = project_grapheme_to_phonetic(cluster)
    projection = result.projection

    # Should NOT have morphological fields
    assert not hasattr(projection, 'root')
    assert not hasattr(projection, 'radicals')
    assert not hasattr(projection, 'pattern')
    assert not hasattr(projection, 'weight')


def test_no_layer_jump_3_no_semantic_fields():
    """
    No-Layer-Jump Test 3: PhoneticProjection has no meaning fields

    PhoneticProjection should NOT contain:
        - meaning
        - semantic_class
        - madlul
    """
    cluster = make_test_grapheme('ك', ['\u064E'])
    result = project_grapheme_to_phonetic(cluster)
    projection = result.projection

    # Should NOT have semantic fields
    assert not hasattr(projection, 'meaning')
    assert not hasattr(projection, 'semantic_class')
    assert not hasattr(projection, 'madlul')


def test_no_layer_jump_4_forbidden_gates():
    """
    No-Layer-Jump Test 4: Verify forbidden gates in ProofObject

    ProofObject must forbid:
        - root_certificate
        - weight_certificate
        - meaning_certificate
        - hukm_certificate
    """
    text = "كتب"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    assert u2p_result.valid
    proof = u2p_result.layer_object.proof

    # These gates must be forbidden
    assert "root_certificate" in proof.forbidden_next_gates
    assert "weight_certificate" in proof.forbidden_next_gates
    assert "meaning_certificate" in proof.forbidden_next_gates
    assert "hukm_certificate" in proof.forbidden_next_gates


def test_no_layer_jump_5_rank_vector_zeros():
    """
    No-Layer-Jump Test 5: Rank vector shows ZERO for higher layers

    Rank vector should show:
        - unicode_rank = CERTIFICATE
        - grapheme_rank = CERTIFICATE
        - phonetic_rank = CERTIFICATE
        - syllable_rank = ZERO
        - All higher layers = ZERO
    """
    text = "كَ"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    assert u2p_result.valid
    proof = u2p_result.layer_object.proof

    # Check rank vector
    assert proof.rank_vector["unicode_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["grapheme_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["phonetic_rank"] == Rank.CERTIFICATE

    # Higher layers must be ZERO
    assert proof.rank_vector["syllable_rank"] == Rank.ZERO
    assert proof.rank_vector["functional_role_rank"] == Rank.ZERO
    assert proof.rank_vector["morpheme_rank"] == Rank.ZERO
    assert proof.rank_vector["stem_root_rank"] == Rank.ZERO
    assert proof.rank_vector["pattern_weight_rank"] == Rank.ZERO
    assert proof.rank_vector["semantic_rank"] == Rank.ZERO
    assert proof.rank_vector["hukm_rank"] == Rank.ZERO


# ============================================================================
# CPB₂p Validation Tests
# ============================================================================

def test_cpb2p_trace_preserved():
    """
    Test CPB₂p: TracePreserved

    Every projection must have trace to U₁ graphemes.
    """
    text = "كتب"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    assert u2p_result.valid

    # All projections should have trace_1
    for projection in u2p_result.layer_object.projections:
        assert len(projection.trace_1) > 0
        # Trace should reference U₁ grapheme IDs
        assert all(isinstance(tid, str) for tid in projection.trace_1)


def test_cpb2p_residuals_inherited():
    """
    Test CPB₂p: ResidualsInherited

    All U₁ residuals must be preserved in U₂p.
    """
    # Create text with foreign character (produces U₁ residual)
    text = "كA"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    assert len(u1_result.layer_object.total_residuals) > 0

    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    assert u2p_result.valid

    # U₁ residuals should be in U₂p
    u1_residuals = u1_result.layer_object.total_residuals
    u2p_residuals = u2p_result.layer_object.total_residuals

    # Check that U₁ residuals are preserved
    assert u1_residuals.issubset(u2p_residuals)


def test_cpb2p_competitors_preserved():
    """
    Test CPB₂p: CompetitorsPreserved

    Ambiguous letters must preserve competitors.
    """
    # و is ambiguous
    cluster = make_test_grapheme('و', [])
    result = project_grapheme_to_phonetic(cluster)

    assert result.success
    assert result.projection.has_competitor()
    assert len(result.projection.competitors) > 0


# ============================================================================
# Immutability Tests
# ============================================================================

def test_immutability_phonetic_projection():
    """
    Test: PhoneticProjection is immutable (frozen dataclass)

    Attempting to modify should raise error.
    """
    cluster = make_test_grapheme('ك', ['\u064E'])
    result = project_grapheme_to_phonetic(cluster)
    projection = result.projection

    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        projection.rank = Rank.ZERO  # type: ignore


def test_immutability_layer_object():
    """
    Test: PhoneticProjectionLayerObject is immutable

    Attempting to modify should raise error.
    """
    text = "ك"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    layer_obj = u2p_result.layer_object

    with pytest.raises(Exception):
        layer_obj.projections = frozenset()  # type: ignore


# ============================================================================
# Integration Tests
# ============================================================================

def test_integration_u0_to_u2p_pipeline():
    """
    Integration Test: Complete U₀ → U₁ → U₂p pipeline

    Text: "كَتَبَ"

    Expected:
        - U₀ produces 6 units
        - U₁ produces 3 clusters
        - U₂p produces 3 projections
        - All projections certified or hypothesized
        - Trace preserved through layers
    """
    text = "كَتَبَ"

    # U₀ layer
    u0_result = text_to_unicode_layer(text)
    assert u0_result.valid
    assert len(u0_result.layer_object.units) == 6

    # U₁ layer
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    assert u1_result.valid
    assert len(u1_result.layer_object.clusters) == 3

    # U₂p layer
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    assert u2p_result.valid
    assert len(u2p_result.layer_object.projections) == 3

    # All projections should have trace
    for projection in u2p_result.layer_object.projections:
        assert len(projection.trace_1) > 0


def test_integration_policy_declarations():
    """
    Integration Test: Policy declarations

    Text: "نَّ" (with shadda)

    Expected:
        - Shadda policy declared
        - Gemination candidate present
        - Rank = HYPOTHESIS (unresolved)
    """
    text = "نَّ"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    assert u2p_result.valid

    projections = list(u2p_result.layer_object.projections)
    assert len(projections) == 1

    proj = projections[0]
    assert proj.gemination_candidate is True
    assert len(proj.policies) > 0
    assert any(p.policy_type == PolicyType.SHADDA_POLICY for p in proj.policies)
    assert proj.rank == Rank.HYPOTHESIS  # Policy not resolved
