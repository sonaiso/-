"""Anti-Promotion Tests for D2 (PRE_MORPH Domain).

These tests enforce the critical law:
    D2 must NOT claim information belonging to higher layers

Forbidden claims for D2:
- Root/radicals (D3: ORIGIN)
- Wazn/pattern (D4: TEMPLATE)
- Ism/Fi'l/Harf classification (D5: IDENTITY_AXIS)
- Case/mood/i'rab (D6: DIRECTIONAL_ANALYSIS)
- Meaning/murad/semantics (post-D7)

Each test proves ONE forbidden field is blocked.
"""

import pytest
from dal_core.premorph_candidate import PreMorphUnitCandidate, PreMorphUnitCandidateSet
from dal_core.premorph_types import PreMorphSegmentation
from dal_core.d2_failures import D2FailureType
from dal_core.dal_algebra import DalTransitionDomain


# ============================================================================
# Test Data Helpers
# ============================================================================


def make_test_syllables():
    """Create mock certified syllables for testing."""
    from dal_core.syllable_candidate import SyllableCandidate
    from dal_core.syllables import Syllable, SyllableType
    from dal_core.d1_proof import ProofObject_D1
    from dal_core.d1_correctness import Corr_D1_Result
    from dal_core.d1_failures import D1FailureSet
    from dal_core.d1_rank_policy import SyllableRankVector

    # Create certified syllable
    syllable = SyllableCandidate(
        candidate_id="test-syl-001",
        syllable=Syllable(type=SyllableType.CV),
        source_atoms=[],
        span=(0, 2)
    )

    # Add certification proof
    syllable.proof = ProofObject_D1(
        candidate_id="test-syl-001",
        is_certified=True,
        corr_result=Corr_D1_Result(is_correct=True, checks=[]),
        failure_set=D1FailureSet(),
        rank_vector=SyllableRankVector()
    )

    return [syllable]


def make_test_candidate(extra_fields: dict = None) -> PreMorphUnitCandidate:
    """Create test candidate with optional extra fields.

    Args:
        extra_fields: Dictionary of extra field names/values to inject

    Returns:
        PreMorphUnitCandidate with extra fields (for testing anti-promotion)
    """
    syllables = make_test_syllables()

    candidate = PreMorphUnitCandidate(
        candidate_id="test-pm-001",
        domain=DalTransitionDomain.PRE_MORPH,
        segmentation=PreMorphSegmentation(core_syllables=syllables),
        source_syllables=syllables,
        span=(0, 1)
    )

    # Inject extra fields (simulating cross-layer leakage)
    if extra_fields:
        for field, value in extra_fields.items():
            setattr(candidate, field, value)

    return candidate


# ============================================================================
# D3 (ORIGIN) Anti-Promotion Tests - Root Extraction
# ============================================================================


def test_d2_no_root_field():
    """D2 must NOT contain 'root' field."""
    candidate = make_test_candidate()

    # Verify field doesn't exist
    assert not hasattr(candidate, 'root'), \
        "D2 candidate should not have 'root' field (D3 ORIGIN domain)"


def test_d2_no_radicals_field():
    """D2 must NOT contain 'radicals' field."""
    candidate = make_test_candidate()

    # Verify field doesn't exist
    assert not hasattr(candidate, 'radicals'), \
        "D2 candidate should not have 'radicals' field (D3 ORIGIN domain)"


def test_d2_root_claim_detected_in_validation():
    """D2 validation must detect premature root claim."""
    # Create candidate with forbidden root field
    candidate = make_test_candidate(extra_fields={'root': 'كتب'})

    # Run validation
    syllables = make_test_syllables()
    proof = candidate.validate(syllables)

    # Verify anti-promotion failure detected
    assert not proof.is_certified, \
        "Candidate with 'root' field should not be certified"

    # Check for specific failure type
    root_failures = candidate.failures.by_type(D2FailureType.PREMATURE_ROOT_CLAIM)
    assert len(root_failures) > 0, \
        "Should have PREMATURE_ROOT_CLAIM failure"


def test_d2_radicals_claim_detected_in_validation():
    """D2 validation must detect premature radicals claim."""
    candidate = make_test_candidate(extra_fields={'radicals': ['ك', 'ت', 'ب']})

    syllables = make_test_syllables()
    proof = candidate.validate(syllables)

    assert not proof.is_certified
    root_failures = candidate.failures.by_type(D2FailureType.PREMATURE_ROOT_CLAIM)
    assert len(root_failures) > 0


# ============================================================================
# D4 (TEMPLATE) Anti-Promotion Tests - Pattern/Wazn
# ============================================================================


def test_d2_no_wazn_field():
    """D2 must NOT contain 'wazn' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'wazn'), \
        "D2 candidate should not have 'wazn' field (D4 TEMPLATE domain)"


def test_d2_no_pattern_field():
    """D2 must NOT contain 'pattern' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'pattern'), \
        "D2 candidate should not have 'pattern' field (D4 TEMPLATE domain)"


def test_d2_no_template_field():
    """D2 must NOT contain 'template' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'template'), \
        "D2 candidate should not have 'template' field (D4 TEMPLATE domain)"


def test_d2_wazn_claim_detected_in_validation():
    """D2 validation must detect premature wazn claim."""
    candidate = make_test_candidate(extra_fields={'wazn': 'فَعَلَ'})

    syllables = make_test_syllables()
    proof = candidate.validate(syllables)

    assert not proof.is_certified
    pattern_failures = candidate.failures.by_type(D2FailureType.PREMATURE_PATTERN_CLAIM)
    assert len(pattern_failures) > 0, \
        "Should have PREMATURE_PATTERN_CLAIM failure"


def test_d2_pattern_claim_detected_in_validation():
    """D2 validation must detect premature pattern claim."""
    candidate = make_test_candidate(extra_fields={'pattern': 'CaCaCa'})

    syllables = make_test_syllables()
    proof = candidate.validate(syllables)

    assert not proof.is_certified
    pattern_failures = candidate.failures.by_type(D2FailureType.PREMATURE_PATTERN_CLAIM)
    assert len(pattern_failures) > 0


# ============================================================================
# D5 (IDENTITY_AXIS) Anti-Promotion Tests - Word Class
# ============================================================================


def test_d2_no_ism_field():
    """D2 must NOT contain 'ism' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'ism'), \
        "D2 candidate should not have 'ism' field (D5 IDENTITY_AXIS domain)"


def test_d2_no_fil_field():
    """D2 must NOT contain 'fil' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'fil'), \
        "D2 candidate should not have 'fil' field (D5 IDENTITY_AXIS domain)"


def test_d2_no_harf_field():
    """D2 must NOT contain 'harf' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'harf'), \
        "D2 candidate should not have 'harf' field (D5 IDENTITY_AXIS domain)"


def test_d2_no_word_class_field():
    """D2 must NOT contain 'word_class' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'word_class'), \
        "D2 candidate should not have 'word_class' field (D5 IDENTITY_AXIS domain)"


def test_d2_no_pos_field():
    """D2 must NOT contain 'pos' (part-of-speech) field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'pos'), \
        "D2 candidate should not have 'pos' field (D5 IDENTITY_AXIS domain)"


def test_d2_word_class_claim_detected_in_validation():
    """D2 validation must detect premature word class claim."""
    candidate = make_test_candidate(extra_fields={'word_class': 'NOUN'})

    syllables = make_test_syllables()
    proof = candidate.validate(syllables)

    assert not proof.is_certified
    identity_failures = candidate.failures.by_type(D2FailureType.PREMATURE_IDENTITY_CLAIM)
    assert len(identity_failures) > 0, \
        "Should have PREMATURE_IDENTITY_CLAIM failure"


# ============================================================================
# D6 (DIRECTIONAL_ANALYSIS) Anti-Promotion Tests - Case/Mood
# ============================================================================


def test_d2_no_case_field():
    """D2 must NOT contain 'case' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'case'), \
        "D2 candidate should not have 'case' field (D6 DIRECTIONAL_ANALYSIS domain)"


def test_d2_no_mood_field():
    """D2 must NOT contain 'mood' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'mood'), \
        "D2 candidate should not have 'mood' field (D6 DIRECTIONAL_ANALYSIS domain)"


def test_d2_no_irab_field():
    """D2 must NOT contain 'irab' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'irab'), \
        "D2 candidate should not have 'irab' field (D6 DIRECTIONAL_ANALYSIS domain)"


def test_d2_no_case_marking_field():
    """D2 must NOT contain 'case_marking' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'case_marking'), \
        "D2 candidate should not have 'case_marking' field (D6 DIRECTIONAL_ANALYSIS domain)"


def test_d2_case_claim_detected_in_validation():
    """D2 validation must detect premature case claim."""
    candidate = make_test_candidate(extra_fields={'case': 'NOMINATIVE'})

    syllables = make_test_syllables()
    proof = candidate.validate(syllables)

    assert not proof.is_certified
    case_failures = candidate.failures.by_type(D2FailureType.PREMATURE_CASE_CLAIM)
    assert len(case_failures) > 0, \
        "Should have PREMATURE_CASE_CLAIM failure"


# ============================================================================
# Semantic Anti-Promotion Tests - Meaning
# ============================================================================


def test_d2_no_meaning_field():
    """D2 must NOT contain 'meaning' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'meaning'), \
        "D2 candidate should not have 'meaning' field (semantic domain)"


def test_d2_no_murad_field():
    """D2 must NOT contain 'murad' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'murad'), \
        "D2 candidate should not have 'murad' field (semantic domain)"


def test_d2_no_haqiqa_majaz_field():
    """D2 must NOT contain 'haqiqa_majaz' field."""
    candidate = make_test_candidate()

    assert not hasattr(candidate, 'haqiqa_majaz'), \
        "D2 candidate should not have 'haqiqa_majaz' field (semantic domain)"


def test_d2_meaning_claim_detected_in_validation():
    """D2 validation must detect premature meaning claim."""
    candidate = make_test_candidate(extra_fields={'meaning': 'to write'})

    syllables = make_test_syllables()
    proof = candidate.validate(syllables)

    assert not proof.is_certified
    meaning_failures = candidate.failures.by_type(D2FailureType.PREMATURE_MEANING_CLAIM)
    assert len(meaning_failures) > 0, \
        "Should have PREMATURE_MEANING_CLAIM failure"


# ============================================================================
# Integration Anti-Promotion Tests
# ============================================================================


def test_d2_multiple_violations_detected():
    """D2 validation must detect multiple anti-promotion violations."""
    # Create candidate with multiple forbidden fields
    candidate = make_test_candidate(extra_fields={
        'root': 'كتب',
        'wazn': 'فَعَلَ',
        'word_class': 'VERB',
        'case': 'NOMINATIVE',
        'meaning': 'to write'
    })

    syllables = make_test_syllables()
    proof = candidate.validate(syllables)

    # Should not be certified
    assert not proof.is_certified

    # Should have multiple failure types
    failures = candidate.failures
    assert len(failures.failures) >= 5, \
        "Should detect all anti-promotion violations"


def test_d2_clean_candidate_passes_anti_promotion():
    """D2 candidate without forbidden fields should pass anti-promotion checks."""
    # Create clean candidate (no forbidden fields)
    candidate = make_test_candidate()

    syllables = make_test_syllables()
    proof = candidate.validate(syllables)

    # Should pass anti-promotion checks (other checks may fail)
    anti_promotion_failures = [
        f for f in candidate.failures.failures
        if f.failure_type in {
            D2FailureType.PREMATURE_ROOT_CLAIM,
            D2FailureType.PREMATURE_PATTERN_CLAIM,
            D2FailureType.PREMATURE_IDENTITY_CLAIM,
            D2FailureType.PREMATURE_CASE_CLAIM,
            D2FailureType.PREMATURE_MEANING_CLAIM
        }
    ]

    assert len(anti_promotion_failures) == 0, \
        "Clean candidate should have no anti-promotion failures"


# ============================================================================
# Summary Test
# ============================================================================


def test_d2_anti_promotion_complete_coverage():
    """Verify all forbidden fields are tested."""
    forbidden_fields = [
        'root', 'radicals',  # D3
        'wazn', 'pattern', 'template',  # D4
        'ism', 'fil', 'harf', 'word_class', 'pos',  # D5
        'case', 'mood', 'irab', 'case_marking',  # D6
        'meaning', 'murad', 'haqiqa_majaz'  # Semantic
    ]

    candidate = make_test_candidate()

    # Verify none of the forbidden fields exist
    for field in forbidden_fields:
        assert not hasattr(candidate, field), \
            f"D2 candidate should not have '{field}' field"

    print(f"✅ D2 Anti-Promotion: {len(forbidden_fields)} forbidden fields verified absent")
