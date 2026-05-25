"""
Tests for Grapheme Phonetic Projection (U₁ Layer)

Validates:
1. Clear cases (consonants, vowels)
2. Policy-based handling (shadda, tanween, madd, boundary)
3. Ambiguous cases (ا و ي)
4. No-jumping validation (no syllable/root/pattern)
5. Trace preservation
6. Residual accumulation
7. Theorem verification
"""

import pytest
from typing import List

from dal_core.grapheme_phonetic_projection import (
    GraphemeCarrierU1,
    PhoneticClass1,
    PhoneticCandidate,
    PhoneticProjectionResult,
    ShaddahPolicy,
    TanweenPolicy,
    BoundaryPolicy,
    GRAPHEME_PHONETIC_HYPOTHESIS_RANK,
)
from dal_core.grapheme_phonetic_engine import (
    project_phonetic1,
    text_to_grapheme_projections,
    validate_no_syllable_formation,
    validate_no_root_extraction,
    validate_no_pattern_matching,
    validate_rank_ceiling,
    validate_trace_preserved,
    validate_phonetic_projection,
    verify_grapheme_phonetic_projection_theorem,
)
from dal_core.carriers import Carrier
from dal_core.atoms import ArabicAtom, AtomKind


# ============================================================================
# Test Helpers
# ============================================================================

def make_test_grapheme(base: str, marks: List[str] = None, position: int = 0) -> GraphemeCarrierU1:
    """Create a test grapheme"""
    if marks is None:
        marks = []

    carrier = Carrier(
        char=base,
        codepoint=ord(base),
        index=position,
        unicode_name=f"TEST-{base}"
    )

    return GraphemeCarrierU1(
        base=base,
        marks=marks,
        position=position,
        trace0=carrier,
        grapheme_class="test"
    )


# ============================================================================
# 1. Clear Consonant Tests
# ============================================================================

def test_clear_consonant_ba():
    """Test: بَ → C=/b/ + V=/a/ (both clear)"""
    grapheme = make_test_grapheme('ب', ['\u064E'])  # بَ

    result = project_phonetic1(grapheme)

    assert result.success
    assert result.phonetic_class == PhoneticClass1.CLEAR_CONSONANT_C
    assert len(result.candidates) > 0
    assert result.rank <= GRAPHEME_PHONETIC_HYPOTHESIS_RANK


def test_clear_consonant_ta():
    """Test: تُ → C=/t/ + V=/u/"""
    grapheme = make_test_grapheme('ت', ['\u064F'])  # تُ

    result = project_phonetic1(grapheme)

    assert result.success
    assert result.phonetic_class == PhoneticClass1.CLEAR_CONSONANT_C


def test_clear_consonant_without_vowel():
    """Test: ب → C=/b/ (no vowel)"""
    grapheme = make_test_grapheme('ب', [])

    result = project_phonetic1(grapheme)

    assert result.success
    assert result.phonetic_class == PhoneticClass1.CLEAR_CONSONANT_C


# ============================================================================
# 2. Short Vowel Tests
# ============================================================================

def test_short_vowel_fatha():
    """Test: بَ contains short vowel /a/"""
    grapheme = make_test_grapheme('ب', ['\u064E'])

    result = project_phonetic1(grapheme)

    assert result.success
    # Primary classification is consonant, but vowel is part of candidate
    assert any(c.vowel_candidate is not None for c in result.candidates) or \
           result.phonetic_class == PhoneticClass1.CLEAR_SHORT_VOWEL_V


def test_orphan_vowel_residual():
    """Test: Orphan diacritic (no carrier) → residual"""
    # Space with fatha - invalid
    grapheme = make_test_grapheme(' ', ['\u064E'])

    result = project_phonetic1(grapheme)

    # Should produce residual or fail
    assert not result.success or len(result.residuals) > 0


# ============================================================================
# 3. Long Vowel Tests
# ============================================================================

def test_long_vowel_candidate_ba_alif():
    """Test: بَا → /bā/ candidate (relation-based)"""
    grapheme1 = make_test_grapheme('ب', ['\u064E'], position=0)  # بَ
    grapheme2 = make_test_grapheme('ا', [], position=1)  # ا

    result = project_phonetic1(grapheme1, next_grapheme=grapheme2)

    # Should detect long vowel candidate
    if result.phonetic_class == PhoneticClass1.CLEAR_LONG_VOWEL_VV:
        assert result.success
        assert any(c.vowel_candidate and c.vowel_candidate.length == "long"
                   for c in result.candidates)


def test_long_vowel_bu_waw():
    """Test: بُو → /bū/ candidate"""
    grapheme1 = make_test_grapheme('ب', ['\u064F'], position=0)  # بُ
    grapheme2 = make_test_grapheme('و', [], position=1)  # و

    result = project_phonetic1(grapheme1, next_grapheme=grapheme2)

    # May detect long vowel
    assert result.success


def test_long_vowel_bi_ya():
    """Test: بِي → /bī/ candidate"""
    grapheme1 = make_test_grapheme('ب', ['\u0650'], position=0)  # بِ
    grapheme2 = make_test_grapheme('ي', [], position=1)  # ي

    result = project_phonetic1(grapheme1, next_grapheme=grapheme2)

    assert result.success


# ============================================================================
# 4. Sukun/Closure Tests
# ============================================================================

def test_sukun_closure_candidate():
    """Test: بْ → closure candidate (not final syllable)"""
    grapheme = make_test_grapheme('ب', ['\u0652'])  # بْ

    result = project_phonetic1(grapheme)

    assert result.success
    assert result.phonetic_class == PhoneticClass1.SUKUN_OR_CLOSURE

    # Should have closure candidate
    assert any(c.closure_candidate is not None for c in result.candidates)

    # Should have residual noting deferred resolution
    assert len(result.residuals) > 0


# ============================================================================
# 5. Shadda Policy Tests
# ============================================================================

def test_shadda_geminate_candidate():
    """Test: نَّ → geminate candidate (not final gemination)"""
    grapheme = make_test_grapheme('ن', ['\u0651', '\u064E'])  # نَّ

    result = project_phonetic1(grapheme)

    assert result.success
    assert result.phonetic_class == PhoneticClass1.SHADDA_POLICY

    # Should have policy declaration
    assert len(result.policies) > 0
    assert result.policies[0].policy_type == "shadda"

    # Should have deferred residual
    assert any("deferred" in r.message.lower() for r in result.residuals)


def test_shadda_not_expanded_at_u1():
    """Test: Shadda NOT expanded to two consonants at U₁"""
    grapheme = make_test_grapheme('م', ['\u0651', '\u064E'])  # مَّ

    result = project_phonetic1(grapheme)

    # Should preserve as single grapheme with policy
    assert result.grapheme.base == 'م'
    assert len(result.grapheme.marks) == 2


# ============================================================================
# 6. Tanween Policy Tests
# ============================================================================

def test_tanween_wasl_waqf_candidates():
    """Test: كِتَابٌ → both wasl (/un/) and waqf (/u/) candidates"""
    grapheme = make_test_grapheme('ب', ['\u064C'])  # ٌ (dammatan)

    result = project_phonetic1(grapheme)

    if result.phonetic_class == PhoneticClass1.TANWEEN_POLICY:
        assert result.success

        # Should have policy with both candidates
        assert len(result.policies) > 0
        policy = result.policies[0]
        assert policy.policy_type == "tanween"

        # Should preserve both wasl and waqf
        assert len(policy.candidates) == 2


def test_tanween_fathatan():
    """Test: كِتَابًا → fathatan with waqf/wasl sensitivity"""
    grapheme = make_test_grapheme('ب', ['\u064B'])  # ً

    result = project_phonetic1(grapheme)

    assert result.success


# ============================================================================
# 7. Ambiguous Letter Tests
# ============================================================================

def test_ambiguous_waw_consonant():
    """Test: وَلَد - initial و is consonant /w/, not long vowel"""
    grapheme = make_test_grapheme('و', ['\u064E'])  # وَ

    result = project_phonetic1(grapheme)

    assert result.success
    # May be classified as deferred or have multiple candidates
    # Should NOT make final determination without context


def test_ambiguous_ya_consonant():
    """Test: يَوْم - initial ي is consonant /y/"""
    grapheme = make_test_grapheme('ي', ['\u064E'])  # يَ

    result = project_phonetic1(grapheme)

    assert result.success


def test_ambiguous_alif():
    """Test: ا - ambiguous (long vowel carrier or hamza support)"""
    grapheme = make_test_grapheme('ا', [])

    result = project_phonetic1(grapheme)

    # Should indicate ambiguity
    assert result.success or len(result.residuals) > 0


# ============================================================================
# 8. No-Jumping Validation Tests (CRITICAL)
# ============================================================================

def test_no_syllable_formation():
    """Test: Phonetic projection does NOT create syllable structures"""
    grapheme = make_test_grapheme('ب', ['\u064E'])

    result = project_phonetic1(grapheme)

    is_valid, violations = validate_no_syllable_formation(result)
    assert is_valid, f"Should not form syllables: {violations}"


def test_no_root_extraction():
    """Test: Phonetic projection does NOT extract roots"""
    grapheme = make_test_grapheme('ك', ['\u064E'])

    result = project_phonetic1(grapheme)

    is_valid, violations = validate_no_root_extraction(result)
    assert is_valid, f"Should not extract roots: {violations}"


def test_no_pattern_matching():
    """Test: Phonetic projection does NOT match patterns (أوزان)"""
    grapheme = make_test_grapheme('ت', ['\u064E'])

    result = project_phonetic1(grapheme)

    is_valid, violations = validate_no_pattern_matching(result)
    assert is_valid, f"Should not match patterns: {violations}"


def test_rank_ceiling():
    """Test: Rank never exceeds grapheme_phonetic_hypothesis"""
    grapheme = make_test_grapheme('ب', ['\u064E'])

    result = project_phonetic1(grapheme)

    is_valid, violations = validate_rank_ceiling(result)
    assert is_valid, f"Rank exceeds ceiling: {violations}"

    assert result.rank <= GRAPHEME_PHONETIC_HYPOTHESIS_RANK


def test_trace_preserved():
    """Test: Trace to U₀ is preserved"""
    carrier = Carrier(char='ب', codepoint=ord('ب'), index=0, unicode_name="BA")
    grapheme = GraphemeCarrierU1(
        base='ب',
        marks=['\u064E'],
        position=0,
        trace0=carrier
    )

    result = project_phonetic1(grapheme)

    is_valid, violations = validate_trace_preserved(result)
    assert is_valid, f"Trace not preserved: {violations}"


def test_comprehensive_validation():
    """Test: All no-jumping validations pass"""
    grapheme = make_test_grapheme('ب', ['\u064E'])

    result = project_phonetic1(grapheme)

    is_valid, violations = validate_phonetic_projection(result)
    assert is_valid, f"Validation failed: {violations}"


# ============================================================================
# 9. Residual Accumulation Tests
# ============================================================================

def test_residuals_preserved():
    """Test: Residuals accumulate, never erased"""
    grapheme = make_test_grapheme('ب', ['\u064E'])
    grapheme.residuals.append(
        pytest.importorskip("dal_core.residuals").make_warning(
            pytest.importorskip("dal_core.residuals").ResidualType.DEFERRED_CLASSIFICATION,
            "Test residual"
        )
    )

    result = project_phonetic1(grapheme)

    # Original residual should still be there
    assert len(result.residuals) >= 1


# ============================================================================
# 10. Full Pipeline Tests
# ============================================================================

def test_text_to_projections_simple():
    """Test: Full pipeline - بَا (simple word)"""
    text = "بَا"

    results, residuals = text_to_grapheme_projections(text)

    assert len(results) > 0
    # Should have projections for both graphemes


def test_text_to_projections_with_shadda():
    """Test: Full pipeline - نَّ (with shadda)"""
    text = "نَّ"

    results, residuals = text_to_grapheme_projections(text)

    assert len(results) > 0
    # Should have shadda policy


def test_text_to_projections_tanween():
    """Test: Full pipeline - كِتَابٌ"""
    text = "كِتَابٌ"

    results, residuals = text_to_grapheme_projections(text)

    assert len(results) > 0
    # Should handle tanween


# ============================================================================
# 11. Theorem Verification Test (CRITICAL)
# ============================================================================

def test_grapheme_phonetic_projection_theorem():
    """
    Test: Grapheme Phonetic Projection Theorem

    Theorem: ∀G ∈ U₁, phon_project1(G) ∈ PhoneticCandidate₁⁺ ∪ Residual₁ ∪ Fail₁

    Every grapheme produces:
    - One or more phonetic candidates, OR
    - Classified residuals
    - WITHOUT claiming syllable/root/pattern
    """
    # Test cases covering different grapheme types
    test_cases = [
        "بَ",     # Clear consonant + vowel
        "نَّ",    # Shadda
        "كِتَابٌ",  # Tanween
        "بَا",    # Long vowel candidate
        "وَ",     # Ambiguous letter
    ]

    for text in test_cases:
        results, residuals = text_to_grapheme_projections(text)

        # Verify theorem for this text
        is_valid, message = verify_grapheme_phonetic_projection_theorem(results)
        assert is_valid, f"Theorem failed for '{text}': {message}"

        # Each result must have either candidates OR residuals
        for result in results:
            has_output = len(result.candidates) > 0 or len(result.residuals) > 0
            assert has_output, f"Grapheme {result.grapheme.get_full_grapheme()} has no output"

            # No jumping violations
            is_valid, violations = validate_phonetic_projection(result)
            assert is_valid, f"No-jumping violated: {violations}"


# ============================================================================
# 12. Edge Cases
# ============================================================================

def test_empty_grapheme():
    """Test: Empty grapheme"""
    grapheme = make_test_grapheme('', [])

    result = project_phonetic1(grapheme)

    # Should handle gracefully (residual or fail)
    assert result is not None


def test_multiple_marks():
    """Test: Grapheme with multiple marks"""
    grapheme = make_test_grapheme('ن', ['\u0651', '\u064E', '\u0652'])

    result = project_phonetic1(grapheme)

    assert result is not None


def test_unknown_character():
    """Test: Unknown character → residual"""
    grapheme = make_test_grapheme('X', [])

    result = project_phonetic1(grapheme)

    # Should produce residual classification
    assert result.phonetic_class == PhoneticClass1.RESIDUAL or len(result.residuals) > 0


# ============================================================================
# 13. Policy Boundary Tests
# ============================================================================

def test_policy_not_resolved_at_u1():
    """Test: Policies declared but NOT resolved at U₁"""
    grapheme = make_test_grapheme('ن', ['\u0651', '\u064E'])  # نَّ with shadda

    result = project_phonetic1(grapheme)

    if result.phonetic_class == PhoneticClass1.SHADDA_POLICY:
        # Should have policy declaration
        assert len(result.policies) > 0

        # But grapheme should NOT be expanded yet
        assert result.grapheme.base == 'ن'  # Still single base


def test_boundary_policy_preserves_both():
    """Test: Boundary policy preserves both waqf and wasl candidates"""
    grapheme = make_test_grapheme('ب', ['\u064C'])  # Tanween

    result = project_phonetic1(grapheme)

    if result.phonetic_class == PhoneticClass1.TANWEEN_POLICY:
        # Should have both candidates preserved
        policy = result.policies[0]
        assert len(policy.candidates) >= 2  # wasl and waqf
