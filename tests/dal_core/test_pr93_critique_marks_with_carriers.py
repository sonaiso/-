"""
Test to verify PR #93 critique resolution: Marks stay with their carriers.

This test explicitly verifies that U₂p does NOT create separate projections
for diacritics. Instead, marks are processed as part of the grapheme cluster
they belong to.

Critical Law (Axiom 1.3): لا حركة بلا حامل (No diacritic without carrier)

Expected behavior:
    Grapheme(base=ك, marks=[فتحة]) →
        PhoneticProjection(consonant=/k/, short_vowel=/a/, grapheme_ref=cluster_id)

NOT:
    PhoneticProjection(ك) + PhoneticProjection(َ)  ← WRONG!
"""

import pytest
from dal_core.u2p_phonetic_projection import grapheme_to_phonetic_layer
from dal_core.u1_grapheme_carrier import unicode_to_grapheme_layer
from dal_core.u0_unicode_carrier import text_to_unicode_layer


def test_pr93_critique_marks_stay_with_carriers():
    """
    PR #93 Critique Resolution: Marks stay with carriers

    Test that كَ produces ONE projection with both C and V,
    not two separate projections.

    Input U₁:
        GraphemeCluster(base=ك, marks=[فتحة])

    Expected U₂p:
        PhoneticProjection(
            consonant_candidate=/k/,
            short_vowel_candidate=/a/,
            grapheme_ref=cluster_id
        )

    NOT Expected:
        PhoneticProjection(ك) + PhoneticProjection(َ)
    """
    text = "كَ"

    # U₀ → U₁
    u0_result = text_to_unicode_layer(text)
    assert u0_result.valid

    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    assert u1_result.valid

    # Should have 1 grapheme cluster
    clusters = list(u1_result.layer_object.clusters)
    assert len(clusters) == 1

    cluster = clusters[0]
    assert cluster.base == 'ك'
    assert '\u064E' in cluster.marks  # فتحة

    # U₁ → U₂p
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    assert u2p_result.valid

    # CRITICAL CHECK: Should have exactly 1 projection (not 2)
    projections = list(u2p_result.layer_object.projections)
    assert len(projections) == 1, "Must have exactly 1 projection, not separate for mark"

    # The single projection should have both C and V
    projection = projections[0]
    assert projection.consonant_candidate == '/k/'
    assert projection.short_vowel_candidate == '/a/'

    # The projection should trace back to the cluster (not to separate mark)
    assert cluster.id in projection.trace_1


def test_pr93_critique_kataba_three_projections():
    """
    PR #93 Critique Resolution: كَتَبَ produces 3 projections (not 6)

    Each grapheme cluster (C+V) produces ONE projection.

    Input U₁:
        - GraphemeCluster(ك, [فتحة])
        - GraphemeCluster(ت, [فتحة])
        - GraphemeCluster(ب, [فتحة])

    Expected U₂p:
        - PhoneticProjection(C=/k/, V=/a/)
        - PhoneticProjection(C=/t/, V=/a/)
        - PhoneticProjection(C=/b/, V=/a/)

    Total: 3 projections (NOT 6)
    """
    text = "كَتَبَ"

    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    assert u2p_result.valid

    # Should have 3 grapheme clusters
    clusters = list(u1_result.layer_object.clusters)
    assert len(clusters) == 3

    # Should have 3 projections (NOT 6)
    projections = list(u2p_result.layer_object.projections)
    assert len(projections) == 3, "Must have 3 projections, not 6 (marks stay with carriers)"

    # Each projection should have both C and V
    for proj in projections:
        assert proj.consonant_candidate is not None
        assert proj.short_vowel_candidate == '/a/'


def test_pr93_critique_shadda_single_projection():
    """
    PR #93 Critique Resolution: نَّ produces ONE projection

    Shadda is a mark, not a separate grapheme.

    Input U₁:
        GraphemeCluster(ن, [فتحة, شدة])

    Expected U₂p:
        PhoneticProjection(
            consonant=/n/,
            short_vowel=/a/,
            gemination_candidate=True,
            grapheme_ref=cluster_id
        )

    Total: 1 projection (NOT 3)
    """
    text = "نَّ"

    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    assert u2p_result.valid

    # Should have 1 grapheme cluster
    clusters = list(u1_result.layer_object.clusters)
    assert len(clusters) == 1

    cluster = clusters[0]
    assert cluster.base == 'ن'
    assert '\u064E' in cluster.marks  # فتحة
    assert '\u0651' in cluster.marks  # شدة

    # Should have 1 projection (NOT 3)
    projections = list(u2p_result.layer_object.projections)
    assert len(projections) == 1, "Shadda is a mark, not separate projection"

    # The projection should have C + V + gemination
    projection = projections[0]
    assert projection.consonant_candidate == '/n/'
    assert projection.short_vowel_candidate == '/a/'
    assert projection.gemination_candidate is True


def test_pr93_critique_trace_preservation():
    """
    PR #93 Critique Resolution: Trace shows marks belong to carrier

    The trace should show that marks are part of the grapheme cluster,
    not separate entities.

    For كَ:
        - U₁ cluster has trace_0 = {unicode_id_ك, unicode_id_َ}
        - U₂p projection has trace_1 = {cluster_id}
        - cluster_id → cluster → trace_0 → original marks

    This proves marks stay with their carrier through the layers.
    """
    text = "كَ"

    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    # Get the cluster
    cluster = list(u1_result.layer_object.clusters)[0]

    # Get the projection
    projection = list(u2p_result.layer_object.projections)[0]

    # Trace verification
    assert cluster.id in projection.trace_1, "Projection should trace to cluster"

    # The cluster should have trace_0 to both base and mark
    assert len(cluster.trace_0) >= 2, "Cluster should trace to both base and mark units"

    # This proves the chain: projection → cluster → (base + marks)
    # NOT: projection → separate_mark_entity


def test_pr93_critique_acceptable_form():
    """
    PR #93 Critique: Acceptable form verification

    The acceptable form (from problem statement):

    PhoneticProjection(كَ):
        C = /k/
        V = /a/
        trace = Grapheme(ك + فتحة)

    This test verifies the current implementation matches this form.
    """
    text = "كَ"

    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    cluster = list(u1_result.layer_object.clusters)[0]
    projection = list(u2p_result.layer_object.projections)[0]

    # Verify acceptable form
    assert projection.consonant_candidate == '/k/', "C = /k/"
    assert projection.short_vowel_candidate == '/a/', "V = /a/"
    assert cluster.id in projection.trace_1, "trace = Grapheme(ك + فتحة)"

    # Verify cluster represents full grapheme
    full_grapheme = cluster.get_full_grapheme()
    assert 'ك' in full_grapheme
    assert '\u064E' in full_grapheme or len(cluster.marks) > 0

    # This is the CORRECT form ✓


def test_pr93_critique_rejected_form():
    """
    PR #93 Critique: Rejected form verification

    The REJECTED form (from problem statement):

    PhoneticProjection(ك) + PhoneticProjection(َ)

    This test verifies we do NOT produce this form.
    """
    text = "كَ"

    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    projections = list(u2p_result.layer_object.projections)

    # CRITICAL: Should NOT have 2 projections
    assert len(projections) != 2, "Must NOT split into separate projections"

    # Should have exactly 1 projection
    assert len(projections) == 1

    # That projection should NOT be just consonant or just vowel
    projection = projections[0]
    assert projection.consonant_candidate is not None, "Should have consonant"
    assert projection.short_vowel_candidate is not None, "Should have vowel"

    # This confirms we do NOT produce the rejected form ✓
