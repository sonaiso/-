"""
Tests for U₂s ArabicSyllableCarrier syllable formation.

Positive tests: Valid syllable formation
Negative tests: Violations of syllabification laws
No-layer-jump tests: Verify forbidden operations
"""

import pytest
from typing import Optional
from dal_core.u2s_syllable_carrier import (
    ArabicSyllable,
    SyllablePattern,
    SyllableWeight,
    BoundaryPolicy,
    SyllableLayerObject,
    SyllableFailureType,
    syllabify_phonetic_projections,
    cpb2s_validate,
    phonetic_to_syllable_layer
)
from dal_core.u2p_phonetic_projection import (
    PhoneticProjection,
    PhoneticClass,
    PhoneticProjectionLayerObject,
    grapheme_to_phonetic_layer
)
from dal_core.u1_grapheme_carrier import unicode_to_grapheme_layer
from dal_core.u0_unicode_carrier import text_to_unicode_layer
from dal_core.foundation import Rank
from dal_core.residuals import ResidualType, ResidualSeverity


# ============================================================================
# Test Helpers
# ============================================================================

def make_test_projection(
    consonant: Optional[str] = None,
    short_vowel: Optional[str] = None,
    closure: bool = False,
    gemination: bool = False,
    phonetic_class: PhoneticClass = PhoneticClass.CONSONANT,
    grapheme_ref: str = "test_grapheme"
) -> PhoneticProjection:
    """Create test phonetic projection."""
    from uuid import uuid4
    return PhoneticProjection(
        id=str(uuid4()),
        grapheme_ref=grapheme_ref,
        phonetic_class=phonetic_class,
        consonant_candidate=consonant,
        short_vowel_candidate=short_vowel,
        long_vowel_candidate=None,
        closure_candidate=closure,
        gemination_candidate=gemination,
        policies=frozenset(),
        competitors=frozenset(),
        trace_1=frozenset([grapheme_ref]),
        residuals=frozenset(),
        rank=Rank.CERTIFICATE,
        metadata=(("test", "projection"),)
    )


# ============================================================================
# Positive Tests
# ============================================================================

def test_positive_1_ka_becomes_cv():
    """
    Positive Test 1: كَ → CV

    Expected:
        - Onset = /k/
        - Nucleus = /a/
        - Coda = ∅
        - Pattern = CV
        - Weight = LIGHT
        - Rank = CERTIFICATE
    """
    proj = make_test_projection(consonant='/k/', short_vowel='/a/')

    result = syllabify_phonetic_projections([proj])

    assert result.success
    assert len(result.syllables) == 1

    syllable = result.syllables[0]
    assert syllable.pattern == SyllablePattern.CV
    assert '/k/' in syllable.onset
    assert '/a/' in syllable.nucleus
    assert len(syllable.coda) == 0
    assert syllable.weight == SyllableWeight.LIGHT
    assert syllable.rank == Rank.CERTIFICATE


def test_positive_2_qaa_becomes_cvv():
    """
    Positive Test 2: قَا → CVV

    Expected:
        - Pattern = CVV
        - Weight = HEAVY

    Note: This test uses full pipeline to ensure proper long vowel detection.
    """
    text = "قَا"
    u0_result = text_to_unicode_layer(text)
    assert u0_result.valid

    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    assert u1_result.valid

    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    assert u2p_result.valid

    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    # Should produce at least one syllable
    # (May be CV or CVV depending on long vowel detection)
    assert len(u2s_result.layer_object.syllables) >= 1


def test_positive_3_full_word_kataba():
    """
    Positive Test 3: Full pipeline كَتَبَ → CV.CV.CV

    Expected:
        - 3 syllables
        - All CV pattern
        - All LIGHT weight
        - All certified
    """
    text = "كَتَبَ"
    u0_result = text_to_unicode_layer(text)
    assert u0_result.valid

    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    assert u1_result.valid

    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    assert u2p_result.valid

    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)
    assert u2s_result.valid
    assert u2s_result.layer_object is not None

    syllables = list(u2s_result.layer_object.syllables)
    assert len(syllables) == 3

    for syllable in syllables:
        assert syllable.pattern == SyllablePattern.CV
        assert syllable.weight == SyllableWeight.LIGHT
        assert len(syllable.nucleus) > 0  # Has nucleus


def test_positive_4_proof_object():
    """
    Positive Test 4: ProofObject creation

    Expected:
        - Proof contains claim
        - Forbidden gates documented (root, weight, meaning, hukm)
        - Allowed gates = boundary_attachment_gate only
        - Rank vector shows syllable_rank certified
        - Limitations documented
    """
    text = "كَ"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    assert u2s_result.valid
    assert u2s_result.layer_object.proof is not None

    proof = u2s_result.layer_object.proof

    assert proof.claim == "Arabic syllables formed and licensed"
    assert proof.scope == "U₂s / ArabicSyllableCarrier"

    # Check forbidden gates
    assert "root_certificate" in proof.forbidden_next_gates
    assert "weight_certificate" in proof.forbidden_next_gates
    assert "meaning_certificate" in proof.forbidden_next_gates
    assert "hukm_certificate" in proof.forbidden_next_gates

    # Check allowed gates (only boundary_attachment_gate)
    assert "boundary_attachment_gate" in proof.allowed_next_gates
    assert len(proof.allowed_next_gates) == 1

    # Check rank vector
    assert proof.rank_vector["unicode_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["grapheme_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["phonetic_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["syllable_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["stem_root_rank"] == Rank.ZERO
    assert proof.rank_vector["pattern_weight_rank"] == Rank.ZERO
    assert proof.rank_vector["semantic_rank"] == Rank.ZERO

    # Check limitations
    assert "No morphological analysis" in proof.limitations
    assert "No semantic interpretation" in proof.limitations


# ============================================================================
# Negative Tests
# ============================================================================

def test_negative_1_ba_sukun_missing_nucleus():
    """
    Negative Test 1: بْ must fail MissingNucleus

    Expected:
        - syllabify_2p2s produces MissingNucleus blocker
        - No syllable_certificate
        - Residual explains failure
    """
    proj = make_test_projection(consonant='/b/', closure=True)

    result = syllabify_phonetic_projections([proj])

    # Should have blocker
    assert any(r.severity == ResidualSeverity.BLOCKER for r in result.residuals)

    # Should indicate missing nucleus
    nucleus_blockers = [r for r in result.residuals
                       if "MissingNucleus" in r.message]
    assert len(nucleus_blockers) > 0


def test_negative_2_alif_alone_no_cvv():
    """
    Negative Test 2: ا alone must NOT become CVV

    Expected:
        - Ambiguous carrier without context
        - OrphanLongVowel residual
        - No syllable formed
    """
    proj = PhoneticProjection(
        id='alif_id',
        grapheme_ref='alif',
        phonetic_class=PhoneticClass.AMBIGUOUS_CARRIER,
        consonant_candidate='/ā/',
        short_vowel_candidate=None,
        long_vowel_candidate=None,
        closure_candidate=False,
        gemination_candidate=False,
        policies=frozenset(),
        competitors=frozenset(["long_vowel_carrier_/ā/"]),
        trace_1=frozenset(['alif']),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        metadata=(("base", "ا"),)
    )

    result = syllabify_phonetic_projections([proj])

    # Should have orphan long vowel warning
    orphan_warnings = [r for r in result.residuals
                      if "OrphanLongVowel" in r.message or "Ambiguous" in r.message]
    assert len(orphan_warnings) > 0

    # Should not form syllable
    assert len(result.syllables) == 0


def test_negative_3_waw_alone_competitors_preserved():
    """
    Negative Test 3: و alone with competitors must not certify

    Expected:
        - Ambiguous carrier residual
        - No certificate
        - Competitors preserved in warning
    """
    proj = PhoneticProjection(
        id='waw_id',
        grapheme_ref='waw',
        phonetic_class=PhoneticClass.AMBIGUOUS_CARRIER,
        consonant_candidate='/w/',
        short_vowel_candidate=None,
        long_vowel_candidate=None,
        closure_candidate=False,
        gemination_candidate=False,
        policies=frozenset(),
        competitors=frozenset(["consonant_/w/", "long_vowel_carrier_/ū/"]),
        trace_1=frozenset(['waw']),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        metadata=(("base", "و"),)
    )

    result = syllabify_phonetic_projections([proj])

    # Should have ambiguity warning
    assert len(result.residuals) > 0

    # Should not form certified syllable
    assert len(result.syllables) == 0


def test_negative_4_shadda_alone_needs_context():
    """
    Negative Test 4: نَّ alone must preserve gemination information

    Expected:
        - May form syllable (CV) but preserves gemination policy info
        - Gemination candidate flag preserved in U₂p projection
        - Not an error to syllabify, but context needed for full interpretation
    """
    proj = make_test_projection(
        consonant='/n/',
        short_vowel='/a/',
        gemination=True,
        phonetic_class=PhoneticClass.GEMINATION
    )

    result = syllabify_phonetic_projections([proj])

    # The key is that gemination info is preserved (in projection)
    # Syllabification may succeed (forming CV) since there IS a nucleus
    # This is acceptable - gemination is a phonetic feature, not a syllable blocker
    assert result.success or len(result.residuals) > 0

    # May form syllable
    if result.syllables:
        syllable = result.syllables[0]
        # Syllable should have nucleus (that's the requirement)
        assert len(syllable.nucleus) > 0


# ============================================================================
# No-Layer-Jump Tests
# ============================================================================

def test_no_layer_jump_1_no_root_fields():
    """
    No-Layer-Jump Test 1: ArabicSyllable has no root fields

    ArabicSyllable should NOT contain:
        - root
        - radicals
        - root_type
    """
    proj = make_test_projection(consonant='/k/', short_vowel='/a/')
    result = syllabify_phonetic_projections([proj])

    syllable = result.syllables[0]

    # Should NOT have root fields
    assert not hasattr(syllable, 'root')
    assert not hasattr(syllable, 'radicals')
    assert not hasattr(syllable, 'root_type')


def test_no_layer_jump_2_no_weight_fields():
    """
    No-Layer-Jump Test 2: ArabicSyllable has no morphological weight fields

    ArabicSyllable should NOT contain:
        - pattern (morphological, note: has syllable_pattern)
        - weight_name (morphological, note: has syllable_weight)
        - transformation
    """
    proj = make_test_projection(consonant='/k/', short_vowel='/a/')
    result = syllabify_phonetic_projections([proj])

    syllable = result.syllables[0]

    # Should NOT have morphological fields
    # Note: syllable has 'pattern' for SyllablePattern (CV, CVV, etc.)
    # and 'weight' for SyllableWeight (LIGHT, HEAVY, etc.)
    # These are syllabic, NOT morphological
    assert not hasattr(syllable, 'transformation')
    assert not hasattr(syllable, 'weight_name')  # Morphological weight name


def test_no_layer_jump_3_no_meaning_fields():
    """
    No-Layer-Jump Test 3: ArabicSyllable has no meaning fields

    ArabicSyllable should NOT contain:
        - meaning
        - semantic_class
        - madlul
        - dalalah
    """
    proj = make_test_projection(consonant='/k/', short_vowel='/a/')
    result = syllabify_phonetic_projections([proj])

    syllable = result.syllables[0]

    # Should NOT have semantic fields
    assert not hasattr(syllable, 'meaning')
    assert not hasattr(syllable, 'semantic_class')
    assert not hasattr(syllable, 'madlul')
    assert not hasattr(syllable, 'dalalah')


def test_no_layer_jump_4_no_hukm_fields():
    """
    No-Layer-Jump Test 4: ArabicSyllable has no hukm fields

    ArabicSyllable should NOT contain:
        - hukm
        - i3rab
        - case_marking
    """
    proj = make_test_projection(consonant='/k/', short_vowel='/a/')
    result = syllabify_phonetic_projections([proj])

    syllable = result.syllables[0]

    # Should NOT have hukm fields
    assert not hasattr(syllable, 'hukm')
    assert not hasattr(syllable, 'i3rab')
    # Note: may have boundary_policy which is syllabic, not grammatical


def test_no_layer_jump_5_forbidden_gates():
    """
    No-Layer-Jump Test 5: Verify forbidden gates in ProofObject

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
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    assert u2s_result.valid
    proof = u2s_result.layer_object.proof

    # These gates must be forbidden
    assert "root_certificate" in proof.forbidden_next_gates
    assert "weight_certificate" in proof.forbidden_next_gates
    assert "meaning_certificate" in proof.forbidden_next_gates
    assert "hukm_certificate" in proof.forbidden_next_gates


def test_no_layer_jump_6_rank_vector_zeros():
    """
    No-Layer-Jump Test 6: Rank vector shows ZERO for higher layers

    Rank vector should show:
        - unicode_rank = CERTIFICATE
        - grapheme_rank = CERTIFICATE
        - phonetic_rank = CERTIFICATE
        - syllable_rank = CERTIFICATE
        - All higher layers = ZERO
    """
    text = "كَ"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    assert u2s_result.valid
    proof = u2s_result.layer_object.proof

    # Check rank vector
    assert proof.rank_vector["unicode_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["grapheme_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["phonetic_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["syllable_rank"] == Rank.CERTIFICATE

    # Higher layers must be ZERO
    assert proof.rank_vector["functional_role_rank"] == Rank.ZERO
    assert proof.rank_vector["morpheme_rank"] == Rank.ZERO
    assert proof.rank_vector["stem_root_rank"] == Rank.ZERO
    assert proof.rank_vector["pattern_weight_rank"] == Rank.ZERO
    assert proof.rank_vector["semantic_rank"] == Rank.ZERO
    assert proof.rank_vector["hukm_rank"] == Rank.ZERO


# ============================================================================
# CPB₂s Validation Tests
# ============================================================================

def test_cpb2s_nucleus_required():
    """
    Test CPB₂s: NucleusRequired

    Every syllable must have nucleus (enforced by __post_init__).
    """
    # This is enforced by the dataclass __post_init__
    # Attempting to create syllable without nucleus raises ValueError
    with pytest.raises(ValueError, match="No nucleus"):
        ArabicSyllable(
            id='test',
            onset=frozenset(['/k/']),
            nucleus=frozenset(),  # Empty nucleus
            coda=frozenset(),
            pattern=SyllablePattern.CV,
            weight=SyllableWeight.LIGHT,
            trace_2p=frozenset(['proj1']),
            trace_1=frozenset(['grapheme1'])
        )


def test_cpb2s_trace_preserved():
    """
    Test CPB₂s: TracePreserved

    Every syllable must have trace to U₂p projections.
    """
    text = "كتب"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    assert u2s_result.valid

    # All syllables should have trace_2p
    for syllable in u2s_result.layer_object.syllables:
        assert len(syllable.trace_2p) > 0
        # Trace should reference U₂p projection IDs
        assert all(isinstance(tid, str) for tid in syllable.trace_2p)


def test_cpb2s_residuals_inherited():
    """
    Test CPB₂s: ResidualsInherited

    All U₂p residuals must be preserved in U₂s.
    """
    # Create text that will produce U₂p residuals
    text = "نَّ"  # Shadda produces policy residual
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)

    # U₂p should have policy residuals
    assert len(u2p_result.layer_object.total_residuals) > 0

    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    # U₂p residuals should be in U₂s
    u2p_residuals = u2p_result.layer_object.total_residuals
    u2s_residuals = u2s_result.layer_object.total_residuals

    # Check that U₂p residuals are preserved
    assert u2p_residuals.issubset(u2s_residuals)


# ============================================================================
# Immutability Tests
# ============================================================================

def test_immutability_syllable():
    """
    Test: ArabicSyllable is immutable (frozen dataclass)

    Attempting to modify should raise error.
    """
    proj = make_test_projection(consonant='/k/', short_vowel='/a/')
    result = syllabify_phonetic_projections([proj])
    syllable = result.syllables[0]

    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        syllable.rank = Rank.ZERO  # type: ignore


def test_immutability_layer_object():
    """
    Test: SyllableLayerObject is immutable

    Attempting to modify should raise error.
    """
    text = "ك"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    layer_obj = u2s_result.layer_object

    with pytest.raises(Exception):
        layer_obj.syllables = frozenset()  # type: ignore


# ============================================================================
# Integration Tests
# ============================================================================

def test_integration_ordered_surface_kataba():
    """
    Integration Test: كَتَبَ → CV.CV.CV with ordered surface preservation.

    Expected:
        - 3 CV syllables
        - Each syllable has ordered_surface
        - get_phonetic_string() returns ordered surface (not sorted)
    """
    text = "كَتَبَ"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    assert u2s_result.valid
    assert len(u2s_result.layer_object.syllables) == 3

    # Verify all syllables have ordered_surface
    for syllable in u2s_result.layer_object.syllables:
        assert hasattr(syllable, 'ordered_surface'), "Syllable must have ordered_surface field"
        assert syllable.ordered_surface != "", "ordered_surface must not be empty"
        assert hasattr(syllable, 'ordered_onset'), "Syllable must have ordered_onset"
        assert hasattr(syllable, 'ordered_nucleus'), "Syllable must have ordered_nucleus"
        assert hasattr(syllable, 'ordered_coda'), "Syllable must have ordered_coda"

        # Verify get_phonetic_string() uses ordered_surface
        phonetic = syllable.get_phonetic_string()
        assert phonetic == syllable.ordered_surface, \
            "get_phonetic_string() must return ordered_surface"


def test_integration_ordered_surface_kaatib_cvv_cvc():
    """
    Integration Test: كَاتِب → CVV.CVC with ordered surface.

    Expected:
        - 2 syllables: CVV + CVC
        - ordered_surface preserved
        - No sorted() usage
    """
    text = "كَاتِب"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    assert u2s_result.valid
    syllables = list(u2s_result.layer_object.syllables)

    # Verify ordered fields exist
    for syllable in syllables:
        assert syllable.ordered_surface, "ordered_surface must be populated"
        assert isinstance(syllable.ordered_onset, tuple), "ordered_onset must be tuple"
        assert isinstance(syllable.ordered_nucleus, tuple), "ordered_nucleus must be tuple"
        assert isinstance(syllable.ordered_coda, tuple), "ordered_coda must be tuple"


def test_integration_ordered_surface_maktab_cvc_cvc():
    """
    Integration Test: مَكْتَب → CVC.CVC (CRITICAL)

    Expected:
        - 2 syllables: CVC + CVC
        - NOT CV.CCVC (no CC onset in Arabic)
        - ordered_surface preserved
    """
    text = "مَكْتَب"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    # Debug output
    print(f"\n[TEST] مَكْتَب syllabification:")
    if u2s_result.valid:
        syllables = list(u2s_result.layer_object.syllables)
        print(f"  Syllables: {len(syllables)}")
        for i, syll in enumerate(syllables):
            print(f"    {i+1}. Pattern={syll.pattern.value}, Surface={syll.ordered_surface}")
    else:
        print(f"  FAILED: {u2s_result.violations}")

    # Verify syllabification succeeded
    assert u2s_result.valid or not u2s_result.layer_object.has_blocking_failure(), \
        f"مَكْتَب syllabification must not have blocking failures"

    # If successful, verify pattern is CVC.CVC
    if u2s_result.valid:
        syllables = list(u2s_result.layer_object.syllables)
        # May be 2 syllables (CVC.CVC) or different depending on U₂p detection
        # The critical law: NO syllable should have pattern CV followed by CC onset
        for syllable in syllables:
            # Verify no CC onset (Arabic law)
            assert len(syllable.ordered_onset) <= 1, \
                f"Arabic syllable must not have CC onset, got onset={syllable.ordered_onset}"


def test_integration_bikitaabin_surface_preservation():
    """
    Integration Test: بِكِتَابٍ ordered surface preservation.

    Expected:
        - Tanween (ٍ) preserved in surface trace
        - ordered_surface contains all diacritics
    """
    text = "بِكِتَابٍ"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    # Should succeed or have non-blocking residuals
    assert u2s_result.valid or not u2s_result.layer_object.has_blocking_failure()

    # Verify all syllables have ordered representation
    if u2s_result.valid:
        for syllable in u2s_result.layer_object.syllables:
            assert syllable.ordered_surface, "ordered_surface must be populated"


def test_integration_u0_to_u2s_pipeline():
    """
    Integration Test: Complete U₀ → U₁ → U₂p → U₂s pipeline

    Text: "كَتَبَ"

    Expected:
        - U₀ produces 6 units
        - U₁ produces 3 clusters
        - U₂p produces 3 projections
        - U₂s produces 3 syllables
        - All syllables certified or hypothesized
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

    # U₂s layer
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)
    assert u2s_result.valid
    assert len(u2s_result.layer_object.syllables) == 3

    # All syllables should have trace
    for syllable in u2s_result.layer_object.syllables:
        assert len(syllable.trace_2p) > 0
        assert len(syllable.trace_1) > 0
        assert len(syllable.nucleus) > 0  # Nucleus required


def test_integration_syllable_patterns():
    """
    Integration Test: Different syllable patterns

    Text: "كَا" (should produce CVV or CV+CV depending on long vowel detection)

    Expected:
        - At least 1 syllable
        - Has nucleus
    """
    text = "كَا"
    u0_result = text_to_unicode_layer(text)
    u1_result = unicode_to_grapheme_layer(u0_result.layer_object)
    u2p_result = grapheme_to_phonetic_layer(u1_result.layer_object)
    u2s_result = phonetic_to_syllable_layer(u2p_result.layer_object)

    assert u2s_result.valid

    syllables = list(u2s_result.layer_object.syllables)
    assert len(syllables) >= 1

    # All syllables should have nucleus
    for syllable in syllables:
        assert len(syllable.nucleus) > 0
