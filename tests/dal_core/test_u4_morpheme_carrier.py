"""
Tests for U₄ Morpheme Carrier Layer

PR: U4-LAYER
Created: 2026-05-25
"""

import pytest
from dal_core.u4_morpheme_carrier import (
    MorphemeSpan,
    MorphemeCandidate,
    MorphemeIdentity,
    MorphemeSort,
    MorphemeRank,
    ClosedClassType,
    AffixType,
    RootCandidateType,
    AttachmentMode,
    FeaturePotential,
    CompleteOne₄,
)
from dal_core.u4_operations import (
    classify_morpheme,
    merge_morphemes,
    attach_affix,
    promote_morpheme,
    block_morpheme,
    preserve_competitors,
    MorphemeOperationStatus,
)
from dal_core.u3_functional_roles import RoleSpan, FunctionalRole, RoleRank, RoleSort, ClosedClassRole
from dal_core.syllables import Syllable
from dal_core.residuals import make_blocker, ResidualType


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_role_span():
    """Create a sample U₃ role span for testing."""
    return RoleSpan(
        span_id="role_test_001",
        syllable_ids=["syl_001"],
        surface="بِ",
        candidate_roles=None,  # Will be filled by test
        attachment_potential=None,
        trace_to_u2=["syl_001"],
        residuals=[],
        evidence=[],
        rank=RoleRank.ROLE_CANDIDATE.value
    )


# ============================================================================
# Test 1: Basic Morpheme Classification
# ============================================================================

def test_classify_closed_class_morpheme(sample_role_span):
    """
    Test classification of closed-class morpheme.

    Law: Closed-class morphemes require lexicon match.
    """
    result = classify_morpheme(
        role_span=sample_role_span,
        morpheme_sort=MorphemeSort.CLOSED_CLASS,
        morpheme_type=ClosedClassType.HARF_JARR,
        evidence={'lexicon_match': 'بِ = preposition'}
    )

    assert result.is_success()
    assert result.output is not None
    assert len(result.output.candidates) == 1

    candidate = result.output.candidates[0]
    assert candidate.identity.sort == MorphemeSort.CLOSED_CLASS
    assert candidate.identity.morpheme_type == ClosedClassType.HARF_JARR
    assert candidate.rank == MorphemeRank.CANDIDATE


def test_classify_affix_morpheme(sample_role_span):
    """
    Test classification of affix morpheme.

    Law: Affixes require host attachment.
    """
    role_span = RoleSpan(
        span_id="role_test_002",
        syllable_ids=["syl_002"],
        surface="الـ",
        candidate_roles=None,
        attachment_potential=None,
        trace_to_u2=["syl_002"],
        residuals=[],
        evidence=[],
        rank=RoleRank.ROLE_CANDIDATE.value
    )

    result = classify_morpheme(
        role_span=role_span,
        morpheme_sort=MorphemeSort.AFFIX,
        morpheme_type=AffixType.DEFINITE_ARTICLE,
        evidence={'affix_type': 'definite_article'}
    )

    assert result.is_success()
    assert result.output.attachment.requires_host is True
    assert result.output.attachment.host_position == "prefix"


def test_classify_root_candidate(sample_role_span):
    """
    Test classification of root candidate.

    Law: Root candidates are NOT certified at U₄.
    They require pattern confirmation at U₅.
    """
    role_span = RoleSpan(
        span_id="role_test_003",
        syllable_ids=["syl_003"],
        surface="ك",
        candidate_roles=None,
        attachment_potential=None,
        trace_to_u2=["syl_003"],
        residuals=[],
        evidence=[],
        rank=RoleRank.ROLE_CANDIDATE.value
    )

    result = classify_morpheme(
        role_span=role_span,
        morpheme_sort=MorphemeSort.ROOT_CANDIDATE,
        morpheme_type=RootCandidateType.FA_CANDIDATE,
        evidence={'position_hint': 'first_radical'}
    )

    assert result.is_success()
    candidate = result.output.candidates[0]
    assert candidate.rank != MorphemeRank.CERTIFICATE  # Not certified yet!


# ============================================================================
# Test 2: Morpheme Operations
# ============================================================================

def test_merge_morphemes():
    """
    Test merging two morpheme spans.

    Example: إِنَّ = إِ + نَّ
    """
    # Create two morpheme spans
    span1 = MorphemeSpan(
        span_id="mspan_001",
        role_span_ids=["role_001"],
        candidates=[],
        attachment=AttachmentMode(),
        features=FeaturePotential(),
        trace_to_u3=["role_001"],
        residuals=[],
        rank=MorphemeRank.CANDIDATE.value
    )

    span2 = MorphemeSpan(
        span_id="mspan_002",
        role_span_ids=["role_002"],
        candidates=[],
        attachment=AttachmentMode(),
        features=FeaturePotential(),
        trace_to_u3=["role_002"],
        residuals=[],
        rank=MorphemeRank.CANDIDATE.value
    )

    result = merge_morphemes(span1, span2, evidence={'compound': 'إنّ'})

    assert result.is_success()
    assert len(result.output.role_span_ids) == 2
    assert len(result.output.trace_to_u3) == 2


def test_attach_affix_to_host():
    """
    Test attaching affix to host.

    Example: الـ + كتاب
    """
    # Create affix span (الـ)
    affix = MorphemeSpan(
        span_id="mspan_affix",
        role_span_ids=["role_affix"],
        candidates=[],
        attachment=AttachmentMode(requires_host=True, host_position="prefix"),
        features=FeaturePotential(),
        trace_to_u3=["role_affix"],
        residuals=[],
        rank=MorphemeRank.CANDIDATE.value
    )

    # Create host span (كتاب)
    host = MorphemeSpan(
        span_id="mspan_host",
        role_span_ids=["role_host"],
        candidates=[],
        attachment=AttachmentMode(),
        features=FeaturePotential(),
        trace_to_u3=["role_host"],
        residuals=[],
        rank=MorphemeRank.HYPOTHESIS.value
    )

    result = attach_affix(affix, host, position="prefix")

    assert result.is_success()
    assert result.evidence['attached_to'] == host.span_id
    assert result.evidence['position'] == "prefix"


def test_promote_morpheme_rank():
    """
    Test promoting morpheme rank.

    Progression: CANDIDATE → HYPOTHESIS → STRONG_HYPOTHESIS → CERTIFICATE
    """
    # Create morpheme span with candidate
    identity = MorphemeIdentity(
        morpheme_id="morph_001",
        sort=MorphemeSort.CLOSED_CLASS,
        morpheme_type=ClosedClassType.HARF_JARR,
        surface_form="بِ",
        trace_to_u3="role_001"
    )

    candidate = MorphemeCandidate(
        identity=identity,
        rank=MorphemeRank.CANDIDATE,
        evidence=[],
        competitors=frozenset(),
        residuals=[]
    )

    span = MorphemeSpan(
        span_id="mspan_001",
        role_span_ids=["role_001"],
        candidates=[candidate],
        attachment=AttachmentMode(),
        features=FeaturePotential(),
        trace_to_u3=["role_001"],
        residuals=[],
        rank=MorphemeRank.CANDIDATE.value
    )

    # Promote to HYPOTHESIS
    result = promote_morpheme(span, 0, {'lexicon_match': True})

    assert result.is_success()
    assert result.output.candidates[0].rank == MorphemeRank.HYPOTHESIS


# ============================================================================
# Test 3: Completeness Predicate
# ============================================================================

def test_complete_one_u4_valid():
    """
    Test CompleteOne₄ predicate with valid span.
    """
    identity = MorphemeIdentity(
        morpheme_id="morph_001",
        sort=MorphemeSort.CLOSED_CLASS,
        morpheme_type=ClosedClassType.HARF_JARR,
        surface_form="بِ",
        trace_to_u3="role_001"
    )

    candidate = MorphemeCandidate(
        identity=identity,
        rank=MorphemeRank.HYPOTHESIS,
        evidence=[],
        competitors=frozenset(),
        residuals=[]
    )

    span = MorphemeSpan(
        span_id="mspan_001",
        role_span_ids=["role_001"],
        candidates=[candidate],
        attachment=AttachmentMode(),
        features=FeaturePotential(),
        trace_to_u3=["role_001"],
        residuals=[],
        rank=MorphemeRank.HYPOTHESIS.value
    )

    assert CompleteOne₄(span) is True


def test_complete_one_u4_no_trace():
    """
    Test CompleteOne₄ fails without trace.

    Law: Trace preservation is mandatory.
    """
    identity = MorphemeIdentity(
        morpheme_id="morph_001",
        sort=MorphemeSort.CLOSED_CLASS,
        morpheme_type=ClosedClassType.HARF_JARR,
        surface_form="بِ",
        trace_to_u3="role_001"
    )

    candidate = MorphemeCandidate(
        identity=identity,
        rank=MorphemeRank.HYPOTHESIS,
        evidence=[],
        competitors=frozenset(),
        residuals=[]
    )

    span = MorphemeSpan(
        span_id="mspan_001",
        role_span_ids=["role_001"],
        candidates=[candidate],
        attachment=AttachmentMode(),
        features=FeaturePotential(),
        trace_to_u3=[],  # NO TRACE - should fail
        residuals=[],
        rank=MorphemeRank.HYPOTHESIS.value
    )

    assert CompleteOne₄(span) is False


# ============================================================================
# Test 4: Critical Laws
# ============================================================================

def test_law_morpheme_neq_word():
    """
    Law: Morpheme ≠ Word

    Morphemes do not claim to be complete words at U₄.
    """
    # This law is enforced by not having word-level fields
    # like POS, syntactic_role, etc.
    identity = MorphemeIdentity(
        morpheme_id="morph_001",
        sort=MorphemeSort.ROOT_CANDIDATE,
        morpheme_type=RootCandidateType.FA_CANDIDATE,
        surface_form="ك",
        trace_to_u3="role_001"
    )

    # Check identity has no word-level fields
    assert not hasattr(identity, 'pos')
    assert not hasattr(identity, 'syntactic_role')
    assert not hasattr(identity, 'case')


def test_law_root_not_certified_at_u4():
    """
    Law: Root candidates NOT certified at U₄.

    Certification requires pattern matching at U₅.
    """
    identity = MorphemeIdentity(
        morpheme_id="morph_001",
        sort=MorphemeSort.ROOT_CANDIDATE,
        morpheme_type=RootCandidateType.FA_CANDIDATE,
        surface_form="ك",
        trace_to_u3="role_001"
    )

    candidate = MorphemeCandidate(
        identity=identity,
        rank=MorphemeRank.HYPOTHESIS,  # Can be hypothesis
        evidence=[],
        competitors=frozenset(),
        residuals=[]
    )

    # But NOT certificate
    assert candidate.rank != MorphemeRank.CERTIFICATE


def test_preserve_competitors():
    """
    Test preserving competing morpheme interpretations.

    Example: بِ could be:
    - حرف جر (preposition)
    - فاء الجذر (root radical)
    """
    identity1 = MorphemeIdentity(
        morpheme_id="morph_001",
        sort=MorphemeSort.CLOSED_CLASS,
        morpheme_type=ClosedClassType.HARF_JARR,
        surface_form="بِ",
        trace_to_u3="role_001"
    )

    identity2 = MorphemeIdentity(
        morpheme_id="morph_002",
        sort=MorphemeSort.ROOT_CANDIDATE,
        morpheme_type=RootCandidateType.FA_CANDIDATE,
        surface_form="بِ",
        trace_to_u3="role_001"
    )

    candidate1 = MorphemeCandidate(identity=identity1, rank=MorphemeRank.HYPOTHESIS)
    candidate2 = MorphemeCandidate(identity=identity2, rank=MorphemeRank.CANDIDATE)

    span = MorphemeSpan(
        span_id="mspan_001",
        role_span_ids=["role_001"],
        candidates=[candidate1, candidate2],
        attachment=AttachmentMode(),
        features=FeaturePotential(),
        trace_to_u3=["role_001"],
        residuals=[],
        rank=MorphemeRank.CANDIDATE.value
    )

    result = preserve_competitors(span)

    assert result.is_success()
    assert len(result.output.candidates) == 2
    # Both candidates should have each other as competitors
    for candidate in result.output.candidates:
        assert len(candidate.competitors) == 2
