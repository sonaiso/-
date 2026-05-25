"""
Tests for U₁ GraphemeCarrier strict grapheme clustering.

Positive tests: Valid grapheme formation
Negative tests: Violations of clustering laws
No-layer-jump tests: Verify forbidden operations
"""

import pytest
from dal_core.u1_grapheme_carrier import (
    GraphemeCluster,
    GraphemeClass,
    GraphemeLayerObject,
    cluster_unicode_units,
    cpb1_validate,
    unicode_to_grapheme_layer,
    SHADDA,
    SUKUN,
    SHORT_VOWELS
)
from dal_core.u0_unicode_carrier import (
    UnicodeUnit,
    UnicodeClass,
    UnicodeLayerObject,
    text_to_unicode_layer
)
from dal_core.foundation import Rank
from dal_core.residuals import ResidualType, ResidualSeverity


# ============================================================================
# Test Helpers
# ============================================================================

def make_test_unicode_unit(char: str, position: int, unicode_class: UnicodeClass) -> UnicodeUnit:
    """Create test Unicode unit."""
    from uuid import uuid4
    return UnicodeUnit(
        id=str(uuid4()),
        scalar=char,
        codepoint=ord(char),
        char=char,
        unicode_class=unicode_class,
        unicode_name=f"TEST-{char}",
        position=position,
        trace=frozenset([f"pos:{position}"]),
        residuals=frozenset(),
        rank=Rank.CERTIFICATE if unicode_class in (
            UnicodeClass.ARABIC_LETTER,
            UnicodeClass.ARABIC_DIACRITIC
        ) else Rank.HYPOTHESIS
    )


# ============================================================================
# Positive Tests
# ============================================================================

def test_positive_1_ka_with_fatha():
    """
    Positive Test 1: كَ (ك + َ)

    Expected:
        - grapheme_class = CONSONANT_WITH_VOWEL
        - rank = CERTIFICATE
        - residuals = ∅ or inherited only
        - success = True
        - trace_0 preserved
    """
    # Create Unicode units
    base = make_test_unicode_unit('ك', 0, UnicodeClass.ARABIC_LETTER)
    fatha = make_test_unicode_unit('\u064E', 1, UnicodeClass.ARABIC_DIACRITIC)

    result = cluster_unicode_units([base, fatha])

    assert result.success
    assert result.cluster is not None
    assert result.cluster.base == 'ك'
    assert '\u064E' in result.cluster.marks
    assert result.cluster.grapheme_class == GraphemeClass.CONSONANT_WITH_VOWEL
    assert result.cluster.rank == Rank.CERTIFICATE
    assert len(result.cluster.trace_0) == 2  # base + mark
    assert base.id in result.cluster.trace_0
    assert fatha.id in result.cluster.trace_0


def test_positive_2_nun_with_shadda_fatha():
    """
    Positive Test 2: نَّ (ن + ّ + َ)

    Expected:
        - grapheme_class = CONSONANT_WITH_SHADDA
        - rank = CERTIFICATE
        - shadda and fatha in marks
        - trace_0 preserved
    """
    base = make_test_unicode_unit('ن', 0, UnicodeClass.ARABIC_LETTER)
    shadda = make_test_unicode_unit('\u0651', 1, UnicodeClass.ARABIC_DIACRITIC)
    fatha = make_test_unicode_unit('\u064E', 2, UnicodeClass.ARABIC_DIACRITIC)

    result = cluster_unicode_units([base, shadda, fatha])

    assert result.success
    assert result.cluster is not None
    assert result.cluster.base == 'ن'
    assert '\u0651' in result.cluster.marks  # Shadda
    assert '\u064E' in result.cluster.marks  # Fatha
    assert result.cluster.grapheme_class == GraphemeClass.CONSONANT_WITH_SHADDA
    assert result.cluster.rank == Rank.CERTIFICATE
    assert len(result.cluster.trace_0) == 3


def test_positive_3_ba_with_sukun():
    """
    Positive Test 3: بْ (ب + ْ)

    Expected:
        - grapheme_class = CONSONANT_WITH_SUKUN
        - rank = CERTIFICATE
        - sukun in marks
        - trace_0 preserved
    """
    base = make_test_unicode_unit('ب', 0, UnicodeClass.ARABIC_LETTER)
    sukun = make_test_unicode_unit('\u0652', 1, UnicodeClass.ARABIC_DIACRITIC)

    result = cluster_unicode_units([base, sukun])

    assert result.success
    assert result.cluster is not None
    assert result.cluster.base == 'ب'
    assert '\u0652' in result.cluster.marks
    assert result.cluster.grapheme_class == GraphemeClass.CONSONANT_WITH_SUKUN
    assert result.cluster.rank == Rank.CERTIFICATE
    assert len(result.cluster.trace_0) == 2


def test_positive_4_bare_consonant():
    """
    Positive Test 4: ك (bare consonant, no marks)

    Expected:
        - grapheme_class = CONSONANT_BARE
        - rank = CERTIFICATE
        - marks = ∅
    """
    base = make_test_unicode_unit('ك', 0, UnicodeClass.ARABIC_LETTER)

    result = cluster_unicode_units([base])

    assert result.success
    assert result.cluster is not None
    assert result.cluster.base == 'ك'
    assert len(result.cluster.marks) == 0
    assert result.cluster.grapheme_class == GraphemeClass.CONSONANT_BARE
    assert result.cluster.rank == Rank.CERTIFICATE


def test_positive_5_full_word_kataba():
    """
    Positive Test 5: كَتَبَ (full word)

    Expected:
        - 3 grapheme clusters
        - All certified
        - All with CONSONANT_WITH_VOWEL
    """
    text = "كَتَبَ"
    u0_result = text_to_unicode_layer(text)
    assert u0_result.valid

    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)

    assert u1_result.valid
    assert u1_result.layer_object is not None

    clusters = list(u1_result.layer_object.clusters)
    assert len(clusters) == 3  # كَ، تَ، بَ

    for cluster in clusters:
        assert cluster.grapheme_class == GraphemeClass.CONSONANT_WITH_VOWEL
        assert cluster.rank == Rank.CERTIFICATE
        assert len(cluster.marks) == 1


def test_positive_6_proof_object():
    """
    Positive Test 6: ProofObject creation

    Expected:
        - Proof contains claim
        - Forbidden gates documented
        - Rank vector shows grapheme_rank certified
        - Limitations documented
    """
    text = "كَ"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)

    assert u1_result.valid
    assert u1_result.layer_object is not None
    assert u1_result.layer_object.proof is not None

    proof = u1_result.layer_object.proof

    assert proof.claim == "Grapheme clusters formed and preserved"
    assert proof.scope == "U₁ / GraphemeCarrier"

    # Check forbidden gates
    assert "syllable_certificate" in proof.forbidden_next_gates
    assert "root_certificate" in proof.forbidden_next_gates
    assert "weight_certificate" in proof.forbidden_next_gates
    assert "meaning_certificate" in proof.forbidden_next_gates
    assert "hukm_certificate" in proof.forbidden_next_gates

    # Check allowed gates (only project_12p)
    assert "project_12p" in proof.allowed_next_gates
    assert len(proof.allowed_next_gates) == 1

    # Check rank vector
    assert proof.rank_vector["unicode_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["grapheme_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["phonetic_rank"] == Rank.ZERO
    assert proof.rank_vector["syllable_rank"] == Rank.ZERO
    assert proof.rank_vector["pattern_weight_rank"] == Rank.ZERO
    assert proof.rank_vector["semantic_rank"] == Rank.ZERO

    # Check limitations
    assert "No phonetic projection" in proof.limitations
    assert "No syllabification" in proof.limitations
    assert "No morphological analysis" in proof.limitations


# ============================================================================
# Negative Tests
# ============================================================================

def test_negative_1_floating_fatha():
    """
    Negative Test 1: َكتب (initial fatha without base)

    Expected at U₁:
        - UnattachedMark blocker
        - rank = BLOCKED
        - success = False
    """
    # Create fatha without base
    fatha = make_test_unicode_unit('\u064E', 0, UnicodeClass.ARABIC_DIACRITIC)

    result = cluster_unicode_units([fatha])

    assert not result.success
    assert result.cluster is None
    # Should have UnattachedMark residual
    residual_types = {r.type for r in result.residuals}
    assert ResidualSeverity.BLOCKER in {r.severity for r in result.residuals} or ResidualType.MALFORMED_ATOM in residual_types


def test_negative_2_duplicate_short_vowels():
    """
    Negative Test 2: بَُ (ب + َ + ُ) - duplicate short vowels

    Expected:
        - MultipleShortVowels blocker
        - rank = BLOCKED
        - success = False
    """
    base = make_test_unicode_unit('ب', 0, UnicodeClass.ARABIC_LETTER)
    fatha = make_test_unicode_unit('\u064E', 1, UnicodeClass.ARABIC_DIACRITIC)
    damma = make_test_unicode_unit('\u064F', 2, UnicodeClass.ARABIC_DIACRITIC)

    result = cluster_unicode_units([base, fatha, damma])

    assert not result.success
    assert result.cluster is None
    # Should have MultipleShortVowels residual
    residual_messages = {r.message for r in result.residuals}
    assert any("MultipleShortVowels" in msg for msg in residual_messages)


def test_negative_3_unattached_shadda():
    """
    Negative Test 3: ّب (shadda before base)

    Expected:
        - UnattachedShaddah blocker
        - success = False
    """
    shadda = make_test_unicode_unit('\u0651', 0, UnicodeClass.ARABIC_DIACRITIC)

    result = cluster_unicode_units([shadda])

    assert not result.success
    assert result.cluster is None
    # Should have UnattachedMark or similar blocker
    assert len(result.residuals) > 0


def test_negative_4_duplicate_sukun():
    """
    Negative Test 4: بْْ (ب + ْ + ْ) - duplicate sukun

    Expected:
        - DuplicateSukūn blocker
        - success = False
    """
    base = make_test_unicode_unit('ب', 0, UnicodeClass.ARABIC_LETTER)
    sukun1 = make_test_unicode_unit('\u0652', 1, UnicodeClass.ARABIC_DIACRITIC)
    sukun2 = make_test_unicode_unit('\u0652', 2, UnicodeClass.ARABIC_DIACRITIC)

    result = cluster_unicode_units([base, sukun1, sukun2])

    assert not result.success
    assert result.cluster is None
    # Should have DuplicateSukūn residual
    residual_messages = {r.message for r in result.residuals}
    assert any("DuplicateSukūn" in msg or "Duplicate" in msg for msg in residual_messages)


def test_negative_5_shadda_on_non_letter():
    """
    Negative Test 5: Shadda on separator (invalid)

    Expected:
        - UnattachedShaddah blocker
        - success = False
    """
    space = make_test_unicode_unit(' ', 0, UnicodeClass.SEPARATOR)
    shadda = make_test_unicode_unit('\u0651', 1, UnicodeClass.ARABIC_DIACRITIC)

    result = cluster_unicode_units([space, shadda])

    assert not result.success
    # Should have UnattachedShaddah residual
    residual_messages = {r.message for r in result.residuals}
    assert any("Shadda" in msg for msg in residual_messages)


def test_negative_6_empty_input():
    """
    Negative Test 6: Empty input

    Expected:
        - Blocker residual
        - success = False
    """
    result = cluster_unicode_units([])

    assert not result.success
    assert result.cluster is None
    assert len(result.residuals) > 0


# ============================================================================
# No-Layer-Jump Tests
# ============================================================================

def test_no_layer_jump_1_no_phonetic_projection():
    """
    No-Layer-Jump Test 1: Verify GraphemeCluster has no phonetic fields

    GraphemeCluster should NOT contain:
        - phonetic_class
        - phonetic_projection
        - makhraj_candidate
        - vowel_candidate
    """
    base = make_test_unicode_unit('ك', 0, UnicodeClass.ARABIC_LETTER)
    fatha = make_test_unicode_unit('\u064E', 1, UnicodeClass.ARABIC_DIACRITIC)

    result = cluster_unicode_units([base, fatha])
    cluster = result.cluster

    # Should NOT have phonetic projection fields
    assert not hasattr(cluster, 'phonetic_class')
    assert not hasattr(cluster, 'phonetic_projection')
    assert not hasattr(cluster, 'makhraj_candidate')
    assert not hasattr(cluster, 'vowel_candidate')


def test_no_layer_jump_2_no_syllable_structure():
    """
    No-Layer-Jump Test 2: Verify GraphemeCluster has no syllable fields

    GraphemeCluster should NOT contain:
        - onset
        - nucleus
        - coda
        - syllable_pattern
    """
    base = make_test_unicode_unit('ك', 0, UnicodeClass.ARABIC_LETTER)
    fatha = make_test_unicode_unit('\u064E', 1, UnicodeClass.ARABIC_DIACRITIC)

    result = cluster_unicode_units([base, fatha])
    cluster = result.cluster

    # Should NOT have syllable structure fields
    assert not hasattr(cluster, 'onset')
    assert not hasattr(cluster, 'nucleus')
    assert not hasattr(cluster, 'coda')
    assert not hasattr(cluster, 'syllable_pattern')


def test_no_layer_jump_3_no_morphological_fields():
    """
    No-Layer-Jump Test 3: Verify GraphemeCluster has no root/weight fields

    GraphemeCluster should NOT contain:
        - root
        - radicals
        - pattern
        - weight
    """
    base = make_test_unicode_unit('ك', 0, UnicodeClass.ARABIC_LETTER)

    result = cluster_unicode_units([base])
    cluster = result.cluster

    # Should NOT have morphological fields
    assert not hasattr(cluster, 'root')
    assert not hasattr(cluster, 'radicals')
    assert not hasattr(cluster, 'pattern')
    assert not hasattr(cluster, 'weight')


def test_no_layer_jump_4_no_semantic_fields():
    """
    No-Layer-Jump Test 4: Verify GraphemeCluster has no meaning fields

    GraphemeCluster should NOT contain:
        - meaning
        - semantic_class
        - madlul
    """
    base = make_test_unicode_unit('ك', 0, UnicodeClass.ARABIC_LETTER)

    result = cluster_unicode_units([base])
    cluster = result.cluster

    # Should NOT have semantic fields
    assert not hasattr(cluster, 'meaning')
    assert not hasattr(cluster, 'semantic_class')
    assert not hasattr(cluster, 'madlul')


def test_no_layer_jump_5_forbidden_gates():
    """
    No-Layer-Jump Test 5: Verify forbidden gates in ProofObject

    ProofObject must forbid:
        - syllable_certificate
        - root_certificate
        - weight_certificate
        - meaning_certificate
        - hukm_certificate
    """
    text = "كتب"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)

    assert u1_result.valid
    proof = u1_result.layer_object.proof

    # These gates must be forbidden
    assert "syllable_certificate" in proof.forbidden_next_gates
    assert "root_certificate" in proof.forbidden_next_gates
    assert "weight_certificate" in proof.forbidden_next_gates
    assert "meaning_certificate" in proof.forbidden_next_gates
    assert "hukm_certificate" in proof.forbidden_next_gates

    # These gates must NOT be allowed
    assert "syllable_certificate" not in proof.allowed_next_gates
    assert "root_certificate" not in proof.allowed_next_gates


def test_no_layer_jump_6_rank_vector_zeros():
    """
    No-Layer-Jump Test 6: Verify rank vector shows ZERO for higher layers

    Rank vector should show:
        - unicode_rank = CERTIFICATE
        - grapheme_rank = CERTIFICATE
        - All higher layers = ZERO
    """
    text = "كَ"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)

    assert u1_result.valid
    proof = u1_result.layer_object.proof

    # Check rank vector
    assert proof.rank_vector["unicode_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["grapheme_rank"] == Rank.CERTIFICATE

    # Higher layers must be ZERO
    assert proof.rank_vector["phonetic_rank"] == Rank.ZERO
    assert proof.rank_vector["syllable_rank"] == Rank.ZERO
    assert proof.rank_vector["functional_role_rank"] == Rank.ZERO
    assert proof.rank_vector["morpheme_rank"] == Rank.ZERO
    assert proof.rank_vector["stem_root_rank"] == Rank.ZERO
    assert proof.rank_vector["pattern_weight_rank"] == Rank.ZERO
    assert proof.rank_vector["semantic_rank"] == Rank.ZERO
    assert proof.rank_vector["hukm_rank"] == Rank.ZERO


# ============================================================================
# CPB₁ Validation Tests
# ============================================================================

def test_cpb1_trace_preserved():
    """
    Test CPB₁: TracePreserved

    Every cluster must have trace to U₀ units.
    """
    text = "كتب"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)

    assert u1_result.valid

    # All clusters should have trace_0
    for cluster in u1_result.layer_object.clusters:
        assert len(cluster.trace_0) > 0
        # Trace should reference U₀ unit IDs
        assert all(isinstance(tid, str) for tid in cluster.trace_0)


def test_cpb1_residuals_inherited():
    """
    Test CPB₁: ResidualsInherited

    All U₀ residuals must be preserved in U₁.
    """
    # Create text with foreign character (produces U₀ residual)
    text = "كA"
    u0_result = text_to_unicode_layer(text)
    assert u0_result.valid
    assert len(u0_result.layer_object.total_residuals) > 0

    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    assert u1_result.valid

    # U₀ residuals should be in U₁
    u0_residuals = u0_result.layer_object.total_residuals
    u1_residuals = u1_result.layer_object.total_residuals

    # Check that U₀ residuals are preserved
    assert u0_residuals.issubset(u1_residuals)


def test_cpb1_rank_non_inflation():
    """
    Test CPB₁: RankNonInflation

    Clusters should not have inflated ranks without evidence.
    """
    text = "ك"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)

    assert u1_result.valid

    for cluster in u1_result.layer_object.clusters:
        if cluster.rank == Rank.CERTIFICATE:
            # Certificate requires Arabic letter base
            assert cluster.grapheme_class in (
                GraphemeClass.CONSONANT_WITH_VOWEL,
                GraphemeClass.CONSONANT_WITH_SUKUN,
                GraphemeClass.CONSONANT_WITH_SHADDA,
                GraphemeClass.CONSONANT_BARE
            )


# ============================================================================
# Immutability Tests
# ============================================================================

def test_immutability_grapheme_cluster():
    """
    Test: GraphemeCluster is immutable (frozen dataclass)

    Attempting to modify should raise error.
    """
    base = make_test_unicode_unit('ك', 0, UnicodeClass.ARABIC_LETTER)
    result = cluster_unicode_units([base])
    cluster = result.cluster

    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        cluster.rank = Rank.ZERO  # type: ignore


def test_immutability_layer_object():
    """
    Test: GraphemeLayerObject is immutable

    Attempting to modify should raise error.
    """
    text = "ك"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)

    layer_obj = u1_result.layer_object

    with pytest.raises(Exception):
        layer_obj.clusters = frozenset()  # type: ignore


# ============================================================================
# Integration Tests
# ============================================================================

def test_integration_u0_to_u1_pipeline():
    """
    Integration Test: Complete U₀ → U₁ pipeline

    Text: "كَتَبَ"

    Expected:
        - U₀ produces 6 units (3 letters + 3 diacritics)
        - U₁ produces 3 clusters
        - All clusters certified
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

    # All clusters should be certified
    certified_count = u1_result.layer_object.count_certified()
    assert certified_count == 3

    # Trace should be preserved
    for cluster in u1_result.layer_object.clusters:
        assert len(cluster.trace_0) > 0


def test_integration_mixed_content():
    """
    Integration Test: Mixed Arabic and foreign content

    Text: "كتابA"

    Expected:
        - Arabic clusters certified
        - Foreign cluster with warning
        - All clusters have trace
    """
    text = "كتابA"

    u0_result = text_to_unicode_layer(text)
    assert u0_result.valid

    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    assert u1_result.valid

    clusters = list(u1_result.layer_object.clusters)
    assert len(clusters) == 5  # ك، ت، ا، ب، A

    # Check foreign cluster
    foreign_clusters = [c for c in clusters if c.grapheme_class == GraphemeClass.FOREIGN_CLUSTER]
    assert len(foreign_clusters) == 1
