"""Integration Tests for D2 (PRE_MORPH Domain).

Tests D1→D2 pipeline integration:
- Syllable certification verification
- Pre-morphological segmentation generation
- Corr_D2 validation
- ProofObject_D2 certification
- Failure detection and handling
- Rank vector computation
"""

import pytest
from dal_core.premorph_candidate import (
    PreMorphUnitCandidate,
    PreMorphUnitCandidateSet,
    generate_premorph_candidates
)
from dal_core.premorph_types import PreMorphPolicy, PreMorphSegmentation
from dal_core.syllable_candidate import SyllableCandidate
from dal_core.syllables import Syllable, SyllableType
from dal_core.d1_proof import ProofObject_D1
from dal_core.d1_correctness import Corr_D1_Result
from dal_core.d1_failures import D1FailureSet
from dal_core.d1_rank_policy import SyllableRankVector
from dal_core.d2_failures import D2FailureType
from dal_core.dal_algebra import DalTransitionDomain


# ============================================================================
# Test Data Helpers
# ============================================================================


def make_certified_syllable(syllable_id: str, span: tuple[int, int]) -> SyllableCandidate:
    """Create a certified syllable candidate."""
    syllable = SyllableCandidate(
        candidate_id=syllable_id,
        domain=DalTransitionDomain.SYLLABIC,
        syllable=Syllable(type=SyllableType.CV),
        source_atoms=[],
        span=span
    )

    # Add certification proof
    syllable.proof = ProofObject_D1(
        candidate_id=syllable_id,
        is_certified=True,
        corr_result=Corr_D1_Result(is_correct=True, checks=[]),
        failure_set=D1FailureSet(),
        rank_vector=SyllableRankVector()
    )

    return syllable


def make_uncertified_syllable(syllable_id: str) -> SyllableCandidate:
    """Create an uncertified syllable candidate."""
    syllable = SyllableCandidate(
        candidate_id=syllable_id,
        syllable=Syllable(type=SyllableType.CV),
        source_atoms=[],
        span=(0, 2)
    )

    # No proof = uncertified
    return syllable


# ============================================================================
# Basic D1→D2 Transition Tests
# ============================================================================


def test_d2_accepts_certified_syllables():
    """D2 should accept certified D1 syllables."""
    syllables = [
        make_certified_syllable("syl-001", (0, 2)),
        make_certified_syllable("syl-002", (2, 4))
    ]

    candidate_set = generate_premorph_candidates(syllables)

    # Should generate candidates
    assert len(candidate_set) > 0, "Should generate candidates from certified syllables"
    assert len(candidate_set.candidates) > 0


def test_d2_rejects_uncertified_syllables():
    """D2 should reject uncertified D1 syllables."""
    syllables = [
        make_uncertified_syllable("syl-001"),
        make_uncertified_syllable("syl-002")
    ]

    candidate_set = generate_premorph_candidates(syllables)

    # Should not generate candidates
    assert len(candidate_set.candidates) == 0, \
        "Should not generate candidates from uncertified syllables"
    assert len(candidate_set.global_residuals) > 0, \
        "Should have blocker residual for uncertified input"


def test_d2_mixed_certification_rejected():
    """D2 should reject mixed certified/uncertified syllables."""
    syllables = [
        make_certified_syllable("syl-001", (0, 2)),
        make_uncertified_syllable("syl-002")  # One uncertified
    ]

    candidate_set = generate_premorph_candidates(syllables)

    # Should reject entire sequence
    assert len(candidate_set.candidates) == 0, \
        "Should reject mixed certified/uncertified syllables"


# ============================================================================
# Segmentation Generation Tests
# ============================================================================


def test_d2_generates_simple_segmentation():
    """D2 should generate simple segmentation (whole sequence as core)."""
    syllables = [
        make_certified_syllable("syl-001", (0, 2)),
        make_certified_syllable("syl-002", (2, 4))
    ]

    candidate_set = generate_premorph_candidates(syllables)

    # Should have at least simple segmentation
    assert len(candidate_set.candidates) >= 1
    simple_candidates = [
        c for c in candidate_set.candidates
        if len(c.segmentation.proclitics) == 0 and
           len(c.segmentation.enclitics) == 0
    ]
    assert len(simple_candidates) > 0, "Should have simple segmentation candidate"


def test_d2_segmentation_preserves_syllables():
    """D2 segmentation must preserve all syllables."""
    syllables = [
        make_certified_syllable("syl-001", (0, 2)),
        make_certified_syllable("syl-002", (2, 4)),
        make_certified_syllable("syl-003", (4, 6))
    ]

    candidate_set = generate_premorph_candidates(syllables)

    for candidate in candidate_set.candidates:
        # Count syllables in segmentation
        total_syllables = (
            len(candidate.segmentation.proclitics) +
            len(candidate.segmentation.core_syllables) +
            len(candidate.segmentation.enclitics)
        )

        assert total_syllables == len(syllables), \
            f"Segmentation must preserve all {len(syllables)} syllables"


# ============================================================================
# Certification Tests
# ============================================================================


def test_d2_candidate_has_proof():
    """D2 candidate should have ProofObject_D2 after generation."""
    syllables = [make_certified_syllable("syl-001", (0, 2))]

    candidate_set = generate_premorph_candidates(syllables)

    for candidate in candidate_set.candidates:
        assert candidate.proof is not None, \
            "D2 candidate should have proof object"
        assert hasattr(candidate.proof, 'd1_syllable_certification_verified'), \
            "D2 proof should track D1 certification verification"


def test_d2_proof_verifies_d1_certification():
    """D2 proof should verify D1 certification."""
    syllables = [make_certified_syllable("syl-001", (0, 2))]

    candidate_set = generate_premorph_candidates(syllables)

    for candidate in candidate_set.valid_candidates():
        assert candidate.proof.d1_syllable_certification_verified, \
            "D2 proof should verify D1 certification"


def test_d2_certification_independent_from_d1():
    """D2 certification is independent from D1 (not inherited)."""
    syllables = [make_certified_syllable("syl-001", (0, 2))]

    candidate_set = generate_premorph_candidates(syllables)

    # D2 has its own proof object type
    for candidate in candidate_set.candidates:
        assert type(candidate.proof).__name__ == 'ProofObject_D2', \
            "D2 should use ProofObject_D2, not ProofObject_D1"

        # D2 has its own rank vector type
        if candidate.rank_vector:
            assert type(candidate.rank_vector).__name__ == 'PreMorphRankVector', \
                "D2 should use PreMorphRankVector, not SyllableRankVector"


# ============================================================================
# Failure Detection Tests
# ============================================================================


def test_d2_detects_uncertified_input_failure():
    """D2 should detect and report uncertified D1 input."""
    syllables = [make_uncertified_syllable("syl-001")]

    # Try to create candidate manually (bypass generation blocker)
    candidate = PreMorphUnitCandidate(
        candidate_id="test-pm-001",
        domain=DalTransitionDomain.PRE_MORPH,
        segmentation=PreMorphSegmentation(core_syllables=syllables),
        source_syllables=syllables,
        span=(0, 1)
    )

    # Run validation
    proof = candidate.validate(syllables)

    # Should not be certified
    assert not proof.is_certified

    # Should have uncertified input failure
    uncert_failures = candidate.failures.by_type(
        D2FailureType.UNCERTIFIED_SYLLABLE_INPUT
    )
    assert len(uncert_failures) > 0, \
        "Should detect uncertified syllable input"


def test_d2_detects_syllable_loss():
    """D2 should detect syllable loss in segmentation."""
    syllables = [
        make_certified_syllable("syl-001", (0, 2)),
        make_certified_syllable("syl-002", (2, 4))
    ]

    # Create candidate with incomplete segmentation (syllable loss)
    candidate = PreMorphUnitCandidate(
        candidate_id="test-pm-001",
        domain=DalTransitionDomain.PRE_MORPH,
        segmentation=PreMorphSegmentation(
            core_syllables=[syllables[0]]  # Missing syllables[1]!
        ),
        source_syllables=syllables,
        span=(0, 2)
    )

    proof = candidate.validate(syllables)

    # Should not be certified
    assert not proof.is_certified

    # Should have syllable loss failure
    loss_failures = candidate.failures.by_type(D2FailureType.SYLLABLE_LOSS)
    assert len(loss_failures) > 0, "Should detect syllable loss"


# ============================================================================
# Rank Vector Tests
# ============================================================================


def test_d2_computes_rank_vector():
    """D2 should compute rank vector for candidates."""
    syllables = [make_certified_syllable("syl-001", (0, 2))]

    candidate_set = generate_premorph_candidates(syllables)

    for candidate in candidate_set.candidates:
        assert candidate.rank_vector is not None, \
            "D2 candidate should have rank vector"

        # Verify rank vector type
        assert hasattr(candidate.rank_vector, 'segmentation_simplicity'), \
            "D2 rank vector should have D2-specific dimensions"
        assert hasattr(candidate.rank_vector, 'syllable_preservation')


def test_d2_rank_vector_independent():
    """D2 rank vector is independent from D1."""
    syllables = [make_certified_syllable("syl-001", (0, 2))]

    candidate_set = generate_premorph_candidates(syllables)

    for candidate in candidate_set.candidates:
        # D1 has: pattern_legality, boundary_confidence, etc.
        # D2 has: segmentation_simplicity, clitic_confidence, etc.

        assert not hasattr(candidate.rank_vector, 'pattern_legality'), \
            "D2 rank vector should not have D1 dimensions"
        assert not hasattr(candidate.rank_vector, 'boundary_confidence'), \
            "D2 rank vector should not have D1 dimensions"


# ============================================================================
# Policy Tests
# ============================================================================


def test_d2_respects_max_candidates_policy():
    """D2 should respect max_candidates policy limit."""
    syllables = [
        make_certified_syllable("syl-001", (0, 2)),
        make_certified_syllable("syl-002", (2, 4))
    ]

    policy = PreMorphPolicy(max_candidates=1)

    candidate_set = generate_premorph_candidates(syllables, policy)

    assert len(candidate_set.candidates) <= policy.max_candidates, \
        "Should respect max_candidates limit"


# ============================================================================
# Reversibility Tests
# ============================================================================


def test_d2_trace_reversible():
    """D2 candidates should have reversible trace."""
    syllables = [make_certified_syllable("syl-001", (0, 2))]

    candidate_set = generate_premorph_candidates(syllables)

    for candidate in candidate_set.valid_candidates():
        assert candidate.trace is not None, "Should have trace"
        assert candidate.trace.reversible, "Trace should claim reversibility"


# ============================================================================
# Summary Test
# ============================================================================


def test_d2_integration_complete():
    """Complete D1→D2 integration test."""
    # Create certified syllable sequence
    syllables = [
        make_certified_syllable("syl-001", (0, 2)),
        make_certified_syllable("syl-002", (2, 4)),
        make_certified_syllable("syl-003", (4, 6))
    ]

    # Generate D2 candidates
    candidate_set = generate_premorph_candidates(syllables)

    # Verify generation
    assert len(candidate_set.candidates) > 0, "Should generate candidates"

    # Verify all candidates have required components
    for candidate in candidate_set.candidates:
        # Has D2-specific components
        assert candidate.domain == DalTransitionDomain.PRE_MORPH
        assert candidate.segmentation is not None
        assert candidate.source_syllables == syllables

        # Has CPB_D2 components
        assert candidate.failures is not None
        assert candidate.rank_vector is not None
        assert candidate.proof is not None

        # Independent from D1
        assert type(candidate.proof).__name__ == 'ProofObject_D2'
        assert type(candidate.rank_vector).__name__ == 'PreMorphRankVector'

        # D1 certification verified
        if candidate.proof.is_certified:
            assert candidate.proof.d1_syllable_certification_verified

    print(f"✅ D2 Integration: {len(candidate_set.candidates)} candidates generated")
    print(f"✅ D2 Integration: {len(candidate_set.valid_candidates())} valid candidates")
