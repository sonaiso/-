"""
Tests for U₀ UnicodeCarrier strict type system.

Positive tests: Valid Unicode processing
Negative tests: Violations of type system laws
"""

import pytest
from dal_core.u0_unicode_carrier import (
    UnicodeUnit,
    UnicodeClass,
    classify_unicode_scalar,
    cpb0_validate,
    text_to_unicode_layer,
    make_u0_proof
)
from dal_core.foundation import Rank


# ============================================================================
# Positive Tests
# ============================================================================

def test_positive_1_arabic_letter():
    """
    Positive Test 1: ك (Arabic letter)

    Expected:
        - unicode_class = ARABIC_LETTER
        - rank = CERTIFICATE
        - residuals = ∅
        - success = True
    """
    result = classify_unicode_scalar("ك", 0)

    assert result.success
    assert result.unit is not None
    assert result.unit.unicode_class == UnicodeClass.ARABIC_LETTER
    assert result.unit.rank == Rank.CERTIFICATE
    assert len(result.residuals) == 0
    assert result.unit.codepoint == 0x0643
    assert "pos:0" in result.unit.trace


def test_positive_2_arabic_diacritic():
    """
    Positive Test 2: َ (Arabic diacritic - fatha)

    Expected:
        - unicode_class = ARABIC_DIACRITIC
        - rank = CERTIFICATE
        - residuals = ∅
        - success = True
    """
    result = classify_unicode_scalar("\u064E", 0)  # Fatha

    assert result.success
    assert result.unit is not None
    assert result.unit.unicode_class == UnicodeClass.ARABIC_DIACRITIC
    assert result.unit.rank == Rank.CERTIFICATE
    assert len(result.residuals) == 0


def test_positive_3_full_word_kataba():
    """
    Positive Test 3: كَتَبَ (full word with diacritics)

    Expected:
        - All units classified
        - Letters CERTIFICATE
        - Diacritics CERTIFICATE
        - CPB₀ valid
    """
    text = "كَتَبَ"
    cpb_result = text_to_unicode_layer(text)

    assert cpb_result.valid
    assert cpb_result.layer_object is not None
    assert len(cpb_result.violations) == 0

    units = list(cpb_result.layer_object.units)
    assert len(units) == 6  # 3 letters + 3 diacritics

    # All should be certified
    certified_count = sum(1 for u in units if u.rank == Rank.CERTIFICATE)
    assert certified_count == 6


def test_positive_4_mixed_text_with_space():
    """
    Positive Test 4: "كتاب جديد" (text with space)

    Expected:
        - Letters classified as ARABIC_LETTER
        - Space classified as SEPARATOR
        - CPB₀ valid
    """
    text = "كتاب جديد"
    cpb_result = text_to_unicode_layer(text)

    assert cpb_result.valid
    assert cpb_result.layer_object is not None

    units = list(cpb_result.layer_object.units)
    assert len(units) == 9  # 8 letters + 1 space

    # Check space classification
    space_units = [u for u in units if u.unicode_class == UnicodeClass.SEPARATOR]
    assert len(space_units) == 1
    assert space_units[0].position == 4


def test_positive_5_trace_preservation():
    """
    Positive Test 5: Trace preservation

    Expected:
        - Every unit has trace
        - Trace references input position
        - CPB₀ TracePreserved passes
    """
    text = "كتب"
    cpb_result = text_to_unicode_layer(text)

    assert cpb_result.valid
    units = sorted(cpb_result.layer_object.units, key=lambda u: u.position)

    for unit in units:
        assert len(unit.trace) > 0
        # Check that trace contains position marker for THIS unit's position
        assert f"pos:{unit.position}" in unit.trace


def test_positive_6_proof_object():
    """
    Positive Test 6: ProofObject creation

    Expected:
        - Proof contains claim
        - Forbidden gates documented
        - Rank vector shows only unicode_rank certified
        - Limitations documented
    """
    text = "كَ"
    cpb_result = text_to_unicode_layer(text)

    assert cpb_result.valid
    proof = make_u0_proof(text, cpb_result)

    assert proof.claim == "Unicode scalars classified and preserved"
    assert proof.scope == "U₀ / UnicodeCarrier"

    # Check forbidden gates
    assert "root_certificate" in proof.forbidden_next_gates
    assert "weight_certificate" in proof.forbidden_next_gates
    assert "meaning_certificate" in proof.forbidden_next_gates
    assert "hukm_certificate" in proof.forbidden_next_gates

    # Check rank vector (dict form)
    assert proof.rank_vector["unicode_rank"] == Rank.CERTIFICATE
    assert proof.rank_vector["pattern_weight_rank"] == Rank.ZERO
    assert proof.rank_vector["semantic_rank"] == Rank.ZERO
    assert proof.rank_vector["hukm_rank"] == Rank.ZERO

    # Check limitations
    assert "No morphological analysis" in proof.limitations
    assert "No semantic interpretation" in proof.limitations


# ============================================================================
# Negative Tests
# ============================================================================

def test_negative_1_floating_diacritic():
    """
    Negative Test 1: َكتب (initial fatha without base)

    Expected at U₀:
        - Diacritic CLASSIFIED (U₀ classifies all scalars)
        - No BLOCKER at U₀ (will fail at U₁ grapheme clustering)
        - CPB₀ valid (classification succeeds)

    Note: This is allowed at U₀ (Unicode layer only classifies).
          Will be blocked at U₁ (grapheme layer).
    """
    text = "\u064Eكتب"  # Fatha before ك
    cpb_result = text_to_unicode_layer(text)

    # At U₀, this is valid (just Unicode classification)
    assert cpb_result.valid

    units = list(cpb_result.layer_object.units)
    assert len(units) == 4

    # First unit is diacritic
    first_unit = sorted(units, key=lambda u: u.position)[0]
    assert first_unit.unicode_class == UnicodeClass.ARABIC_DIACRITIC
    # At U₀, it's classified (will be blocked at U₁)


def test_negative_2_unknown_codepoint():
    """
    Negative Test 2: Unknown Unicode scalar

    Expected:
        - unicode_class = UNKNOWN
        - rank = BLOCKED
        - blocker residual
        - success = False
    """
    # Use a rare/invalid codepoint
    char = "\uFFFF"  # Invalid character
    result = classify_unicode_scalar(char, 0)

    assert not result.success
    # Unit may still be created but with BLOCKED rank
    if result.unit:
        assert result.unit.unicode_class == UnicodeClass.UNKNOWN
        assert result.unit.rank == Rank.BLOCKED
    assert len(result.residuals) > 0


def test_negative_3_control_character_forbidden():
    """
    Negative Test 3: Control character without policy

    Expected:
        - unicode_class = CONTROL
        - rank = BLOCKED
        - FORBIDDEN_CONTROL residual
        - success = False
    """
    # NULL character
    result = classify_unicode_scalar("\x00", 0, policy={"allow_control": False})

    assert not result.success
    if result.unit:
        assert result.unit.rank == Rank.BLOCKED
    assert len(result.residuals) > 0


def test_negative_4_multiple_character_input():
    """
    Negative Test 4: Multiple characters passed as single scalar

    Expected:
        - Validation error
        - MALFORMED_ATOM residual
        - success = False
    """
    result = classify_unicode_scalar("كت", 0)

    assert not result.success
    assert result.unit is None
    assert len(result.residuals) > 0


def test_negative_5_cpb0_rank_inflation():
    """
    Negative Test 5: Attempt to create CERTIFICATE for non-Arabic

    This tests CPB₀ rank validation.

    Expected:
        - Foreign letter gets HYPOTHESIS rank
        - Not CERTIFICATE
    """
    result = classify_unicode_scalar("A", 0)

    assert result.success
    assert result.unit is not None
    assert result.unit.unicode_class == UnicodeClass.FOREIGN_LETTER
    # Foreign letters get HYPOTHESIS, not CERTIFICATE
    assert result.unit.rank == Rank.HYPOTHESIS
    assert len(result.residuals) > 0  # Should have warning


def test_negative_6_no_layer_jump():
    """
    Negative Test 6: Verify no layer jump to root/weight/meaning

    ProofObject should forbid:
        - root_certificate
        - weight_certificate
        - meaning_certificate
        - hukm_certificate
    """
    text = "كتب"
    cpb_result = text_to_unicode_layer(text)
    proof = make_u0_proof(text, cpb_result)

    # These gates must be forbidden
    assert "root_certificate" in proof.forbidden_next_gates
    assert "weight_certificate" in proof.forbidden_next_gates
    assert "meaning_certificate" in proof.forbidden_next_gates

    # Rank vector should show ZERO for higher layers
    assert proof.rank_vector["pattern_weight_rank"] == Rank.ZERO
    assert proof.rank_vector["semantic_rank"] == Rank.ZERO


def test_negative_7_axiom_0_1_no_conversion_before_preservation():
    """
    Negative Test 7: Axiom 0.1 - لا تحويل قبل حفظ

    Verify that Unicode layer does NOT convert to:
        - Grapheme
        - Syllable
        - Root
        - Weight
        - Meaning

    Check ProofObject limitations.
    """
    text = "ك"
    cpb_result = text_to_unicode_layer(text)
    proof = make_u0_proof(text, cpb_result)

    # Check limitations
    assert "No grapheme clustering" in proof.limitations
    assert "No syllabification" in proof.limitations
    assert "No morphological analysis" in proof.limitations
    assert "No semantic interpretation" in proof.limitations

    # Check allowed gates (only cluster₀₁)
    assert "cluster₀₁" in proof.allowed_next_gates
    assert len(proof.allowed_next_gates) == 1


def test_negative_8_axiom_0_6_no_syllable_before_unicode():
    """
    Negative Test 8: Axiom 0.6 - لا مقطع قبل حفظ Unicode

    Verify that syllable_certificate is forbidden at U₀.
    """
    text = "كَ"  # Potential CV syllable
    cpb_result = text_to_unicode_layer(text)
    proof = make_u0_proof(text, cpb_result)

    # Syllable certificate must be forbidden
    assert "syllable_certificate" in proof.forbidden_next_gates

    # Syllable rank must be ZERO
    assert proof.rank_vector["syllable_rank"] == Rank.ZERO


# ============================================================================
# CPB₀ Validation Tests
# ============================================================================

def test_cpb0_trace_preserved():
    """
    Test CPB₀: TracePreserved

    Every unit must have trace to input position.
    """
    text = "كتب"
    units = []

    for i, char in enumerate(text):
        result = classify_unicode_scalar(char, i)
        if result.success and result.unit:
            units.append(result.unit)

    cpb_result = cpb0_validate(text, units)

    assert cpb_result.valid
    assert "TraceViolation" not in str(cpb_result.violations)


def test_cpb0_no_silent_deletion():
    """
    Test CPB₀: NoSilentDeletion

    If a character is not in output, there must be a residual explaining why.
    """
    text = "كتب"
    units = []

    # Classify all characters
    for i, char in enumerate(text):
        result = classify_unicode_scalar(char, i)
        if result.success and result.unit:
            units.append(result.unit)

    cpb_result = cpb0_validate(text, units)

    assert cpb_result.valid
    # All characters should be in output (no deletion)
    assert len(units) == len(text)


def test_cpb0_residuals_explicit():
    """
    Test CPB₀: ResidualsExplicit

    All warnings/blockers must be explicit in output.
    """
    text = "كA"  # Mixed Arabic + foreign
    cpb_result = text_to_unicode_layer(text)

    assert cpb_result.valid
    # Foreign letter should have warning residual
    assert len(cpb_result.layer_object.total_residuals) > 0


# ============================================================================
# Type System Tests
# ============================================================================

def test_type_system_unicode_not_grapheme():
    """
    Test: UnicodeScalar ≠ GraphemeCluster

    Verify that UnicodeUnit does not contain grapheme-level fields.
    """
    result = classify_unicode_scalar("ك", 0)

    assert result.success
    unit = result.unit

    # UnicodeUnit should NOT have these grapheme-level attributes
    assert not hasattr(unit, "base")
    assert not hasattr(unit, "marks")
    assert not hasattr(unit, "grapheme_class")


def test_type_system_unicode_not_syllable():
    """
    Test: UnicodeScalar ≠ ArabicSyllable

    Verify that UnicodeUnit does not contain syllable-level fields.
    """
    result = classify_unicode_scalar("ك", 0)

    assert result.success
    unit = result.unit

    # UnicodeUnit should NOT have these syllable-level attributes
    assert not hasattr(unit, "onset")
    assert not hasattr(unit, "nucleus")
    assert not hasattr(unit, "coda")
    assert not hasattr(unit, "syllable_pattern")


def test_type_system_unicode_not_root():
    """
    Test: UnicodeScalar ≠ Root

    Verify that UnicodeUnit does not contain root-level fields.
    """
    result = classify_unicode_scalar("ك", 0)

    assert result.success
    unit = result.unit

    # UnicodeUnit should NOT have these root-level attributes
    assert not hasattr(unit, "radicals")
    assert not hasattr(unit, "root_type")
    assert not hasattr(unit, "root_class")


def test_type_system_unicode_not_meaning():
    """
    Test: UnicodeScalar ≠ Meaning

    Verify that UnicodeUnit does not contain meaning-level fields.
    """
    result = classify_unicode_scalar("ك", 0)

    assert result.success
    unit = result.unit

    # UnicodeUnit should NOT have these meaning-level attributes
    assert not hasattr(unit, "meaning")
    assert not hasattr(unit, "semantic_class")
    assert not hasattr(unit, "madlul")


# ============================================================================
# Immutability Tests
# ============================================================================

def test_immutability_unicode_unit():
    """
    Test: UnicodeUnit is immutable (frozen dataclass)

    Attempting to modify should raise error.
    """
    result = classify_unicode_scalar("ك", 0)
    unit = result.unit

    with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
        unit.rank = Rank.ZERO  # type: ignore


def test_immutability_layer_object():
    """
    Test: UnicodeLayerObject is immutable

    Attempting to modify should raise error.
    """
    cpb_result = text_to_unicode_layer("ك")
    layer_obj = cpb_result.layer_object

    # UnicodeLayerObject is frozen, cannot modify
    with pytest.raises(Exception):
        layer_obj.units = frozenset()  # type: ignore
