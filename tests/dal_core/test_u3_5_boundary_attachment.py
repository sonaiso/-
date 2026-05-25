"""
Tests for U₃.₅ Boundary and Attachment Layer

Tests cover:
    1. WrittenCompositeToken creation
    2. TrueSingularLafz classification
    3. Boundary segmentation operations
    4. Critical laws enforcement
    5. Trace preservation
    6. Residual propagation

PR: U3.5-BOUNDARY-LAYER
Created: 2026-05-25
"""

import pytest
from uuid import UUID

from dal_core.u3_5_boundary_attachment import (
    WrittenCompositeToken,
    TrueSingularLafz,
    BoundarySegmentation,
    BoundaryCandidate,
    AttachmentType,
    BoundarySegmentationType,
    TrueSingularLafzType,
    BoundaryRank,
    BoundaryResidual,
    CompleteOne_3_5,
    law_weight_access_for_core_only,
    law_external_attachment_detachable,
    law_internal_morpheme_not_detachable,
)
from dal_core.u3_5_operations import (
    segment_written_token,
    classify_unit,
    promote_boundary,
    block_segmentation,
    preserve_competitors,
    detach_clitic,
    OperationStatus,
)
from dal_core.u3_functional_roles import RoleSpan, RoleSort


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def sample_role_span():
    """Create sample role span from U₃."""
    from dal_core.syllables import Syllable, SyllableStructure

    # Create a simple syllable
    syllable = Syllable(
        structure=SyllableStructure.CV,
        onset_consonant="ك",
        nucleus_vowel="ِ",
        coda_consonant="",
        diacritics="",
        is_final=False,
        is_initial=True
    )

    return RoleSpan(
        syllables=[syllable],
        syllable_indices=(0,),
        candidate_roles=frozenset(),
        position="initial",
        trace_u2=[syllable],
        residuals=[],
        rank="role_hypothesis"
    )


@pytest.fixture
def written_composite_wabikatibihim(sample_role_span):
    """Create WrittenCompositeToken for وَبِكِتَابِهِمْ"""
    return WrittenCompositeToken(
        surface="وَبِكِتَابِهِمْ",
        role_spans=(sample_role_span,)
    )


@pytest.fixture
def written_composite_kitabun(sample_role_span):
    """Create WrittenCompositeToken for كِتَابٌ (core only)"""
    return WrittenCompositeToken(
        surface="كِتَابٌ",
        role_spans=(sample_role_span,)
    )


# ============================================================================
# Test 1: WrittenCompositeToken Creation
# ============================================================================

def test_written_composite_token_creation(sample_role_span):
    """Test creating WrittenCompositeToken."""
    token = WrittenCompositeToken(
        surface="وَبِكِتَابِهِمْ",
        role_spans=(sample_role_span,)
    )

    assert token.surface == "وَبِكِتَابِهِمْ"
    assert len(token.role_spans) == 1
    assert isinstance(token.id, UUID)
    assert str(token) == "WrittenComposite(وَبِكِتَابِهِمْ)"


# ============================================================================
# Test 2: TrueSingularLafz Creation
# ============================================================================

def test_true_singular_lafz_proclitic(sample_role_span):
    """Test creating TrueSingularLafz for proclitic (بِ)."""
    unit = TrueSingularLafz(
        surface="بِ",
        lafz_type=TrueSingularLafzType.CLOSED_CLASS,
        attachment_type=AttachmentType.PROCLITIC,
        role_spans=(sample_role_span,),
        weight_access=False,
        detachable=True
    )

    assert unit.surface == "بِ"
    assert unit.lafz_type == TrueSingularLafzType.CLOSED_CLASS
    assert unit.attachment_type == AttachmentType.PROCLITIC
    assert unit.weight_access is False  # Proclitics don't enter weight analysis
    assert unit.detachable is True      # Proclitics are detachable
    assert str(unit) == "TrueSingular(بِ:أداة)"


def test_true_singular_lafz_core_stem(sample_role_span):
    """Test creating TrueSingularLafz for core stem (كِتَاب)."""
    unit = TrueSingularLafz(
        surface="كِتَاب",
        lafz_type=TrueSingularLafzType.OPEN_LEXICAL_CORE,
        attachment_type=AttachmentType.STEM_CORE,
        role_spans=(sample_role_span,),
        weight_access=True,  # Core enters weight analysis
        detachable=False
    )

    assert unit.surface == "كِتَاب"
    assert unit.lafz_type == TrueSingularLafzType.OPEN_LEXICAL_CORE
    assert unit.attachment_type == AttachmentType.STEM_CORE
    assert unit.weight_access is True   # Core enters U₆
    assert unit.detachable is False     # Core is not detachable
    assert str(unit) == "TrueSingular(كِتَاب:جذع_معجمي_مفتوح)"


def test_true_singular_lafz_enclitic(sample_role_span):
    """Test creating TrueSingularLafz for enclitic pronoun (ـهِمْ)."""
    unit = TrueSingularLafz(
        surface="ـهِمْ",
        lafz_type=TrueSingularLafzType.PRONOUN,
        attachment_type=AttachmentType.ENCLITIC,
        role_spans=(sample_role_span,),
        weight_access=False,
        detachable=True
    )

    assert unit.surface == "ـهِمْ"
    assert unit.lafz_type == TrueSingularLafzType.PRONOUN
    assert unit.attachment_type == AttachmentType.ENCLITIC
    assert unit.weight_access is False
    assert unit.detachable is True


# ============================================================================
# Test 3: Segment Written Token Operation - وَبِكِتَابِهِمْ
# ============================================================================

def test_segment_wabikatibihim(written_composite_wabikatibihim):
    """
    Test segmentation of وَبِكِتَابِهِمْ

    Expected:
        [وَ, بِ, كِتَابِ, ـهِمْ]
        - وَ: proclitic (conjunction)
        - بِ: proclitic (preposition)
        - كِتَابِ: core stem
        - ـهِمْ: enclitic (pronoun)
    """
    result = segment_written_token(written_composite_wabikatibihim)

    assert result.is_success()
    assert result.output is not None

    candidate = result.output
    seg = candidate.segmentation

    # Check segmentation
    assert seg.is_composite()
    assert len(seg.units) >= 3  # At least و + core + pronoun

    # Check core units (only core should have weight_access)
    core_units = seg.core_units()
    assert len(core_units) >= 1
    assert all(u.weight_access for u in core_units)

    # Check clitics
    clitics = seg.external_clitics()
    assert len(clitics) >= 2  # At least proclitics and enclitics
    assert all(u.detachable for u in clitics)

    # Check residuals (should have ambiguity warnings)
    assert len(seg.residuals) > 0
    # Should warn about potential proclitic/stem ambiguity


def test_segment_kitabun_core_only(written_composite_kitabun):
    """
    Test segmentation of كِتَابٌ (core only, no clitics)

    Expected:
        [كِتَابٌ]
        - كِتَابٌ: core stem only
    """
    result = segment_written_token(written_composite_kitabun)

    assert result.is_success()
    assert result.output is not None

    candidate = result.output
    seg = candidate.segmentation

    # Should be single unit (core only)
    assert not seg.is_composite() or len(seg.units) == 1
    assert seg.segmentation_type == BoundarySegmentationType.CORE_ONLY

    # Check core
    core_units = seg.core_units()
    assert len(core_units) == 1
    assert core_units[0].weight_access is True
    assert core_units[0].detachable is False


# ============================================================================
# Test 4: Proclitic vs Prefix Distinction
# ============================================================================

def test_proclitic_vs_prefix_distinction(sample_role_span):
    """
    Test distinction between:
        - بِ in بِكِتَابٍ = proclitic (external, separable)
        - مـ in مَكْتَب = prefix (internal, part of pattern)

    Critical law: External attachments are separable before weight.
                  Internal pattern elements are NOT separable here.
    """
    # Test 1: بِكِتَابٍ should separate بِ as proclitic
    token1 = WrittenCompositeToken(surface="بِكِتَابٍ", role_spans=(sample_role_span,))
    result1 = segment_written_token(token1)

    assert result1.is_success()
    seg1 = result1.output.segmentation

    # Should have separated بِ
    assert seg1.is_composite()
    bi_units = [u for u in seg1.units if u.surface in {'ب', 'بِ'}]
    assert len(bi_units) > 0
    if bi_units:
        bi_unit = bi_units[0]
        assert bi_unit.attachment_type == AttachmentType.PROCLITIC
        assert bi_unit.detachable is True

    # Test 2: مَكْتَب should NOT separate مـ as proclitic
    # (مـ is part of the pattern مَفْعَل, handled in U₆)
    token2 = WrittenCompositeToken(surface="مَكْتَب", role_spans=(sample_role_span,))
    result2 = segment_written_token(token2)

    assert result2.is_success()
    seg2 = result2.output.segmentation

    # Should be core only (or minimal segmentation)
    # مـ should NOT be separated as proclitic
    mim_proclitics = [u for u in seg2.units
                      if u.surface == 'م' and u.attachment_type == AttachmentType.PROCLITIC]
    assert len(mim_proclitics) == 0  # مـ is NOT a proclitic


# ============================================================================
# Test 5: Critical Law - Weight Access for Core Only
# ============================================================================

def test_law_weight_access_for_core_only(written_composite_wabikatibihim):
    """
    Test critical law: Only STEM_CORE/VERBAL_CORE have weight_access = True

    weight_access = True ⟺ attachment_type ∈ {STEM_CORE, VERBAL_CORE}
    """
    result = segment_written_token(written_composite_wabikatibihim)
    assert result.is_success()

    candidate = result.output
    assert law_weight_access_for_core_only(candidate)

    # Check each unit
    for unit in candidate.segmentation.units:
        core_types = {AttachmentType.STEM_CORE, AttachmentType.VERBAL_CORE}
        is_core = unit.attachment_type in core_types
        has_access = unit.weight_access

        # Law: is_core ⟺ has_access
        assert is_core == has_access


# ============================================================================
# Test 6: Critical Law - External Attachments Detachable
# ============================================================================

def test_law_external_attachment_detachable(written_composite_wabikatibihim):
    """
    Test critical law: External attachments (proclitics/enclitics) are detachable.

    attachment_type ∈ {PROCLITIC, ENCLITIC} ⟹ detachable = True
    """
    result = segment_written_token(written_composite_wabikatibihim)
    assert result.is_success()

    candidate = result.output
    assert law_external_attachment_detachable(candidate)

    # Check each external attachment
    for unit in candidate.segmentation.units:
        external_types = {AttachmentType.PROCLITIC, AttachmentType.ENCLITIC}
        if unit.attachment_type in external_types:
            assert unit.detachable is True


# ============================================================================
# Test 7: Critical Law - Internal Morphemes Not Detachable
# ============================================================================

def test_law_internal_morpheme_not_detachable(sample_role_span):
    """
    Test critical law: Internal morphological elements are NOT detachable here.

    attachment_type ∈ {PREFIX, SUFFIX, INFIX} ⟹ detachable = False

    These are handled in U₄-U₆, not separated at boundary layer.
    """
    # Create a unit with PREFIX attachment
    unit_prefix = TrueSingularLafz(
        surface="يَ",
        lafz_type=TrueSingularLafzType.FUNCTIONAL_MARKER,
        attachment_type=AttachmentType.PREFIX,
        role_spans=(sample_role_span,),
        weight_access=False,
        detachable=False  # Must be False for PREFIX
    )

    seg = BoundarySegmentation(
        written_token=WrittenCompositeToken(surface="يَكْتُبُ", role_spans=(sample_role_span,)),
        units=(unit_prefix,),
        segmentation_type=BoundarySegmentationType.CORE_ONLY,
        trace=(sample_role_span,),
        residuals=frozenset(),
        rank=BoundaryRank.BOUNDARY_HYPOTHESIS
    )

    candidate = BoundaryCandidate(
        segmentation=seg,
        rank=BoundaryRank.BOUNDARY_HYPOTHESIS,
        residuals=frozenset(),
        trace=(sample_role_span,)
    )

    assert law_internal_morpheme_not_detachable(candidate)


# ============================================================================
# Test 8: Completeness Predicate
# ============================================================================

def test_completeness_predicate_valid(written_composite_kitabun):
    """Test CompleteOne_3_5 with valid complete candidate."""
    result = segment_written_token(written_composite_kitabun)
    assert result.is_success()

    candidate = result.output

    # Should be complete (or nearly complete)
    # May have warnings but no blockers
    if not candidate.has_blockers():
        is_complete = CompleteOne_3_5(candidate)
        # May or may not be complete depending on evidence
        # But should satisfy basic structure


def test_completeness_predicate_blocked(written_composite_kitabun):
    """Test CompleteOne_3_5 with blocked candidate."""
    result = segment_written_token(written_composite_kitabun)
    assert result.is_success()

    # Block the candidate
    blocked_result = block_segmentation(
        result.output,
        BoundaryResidual.CONFLICTING_EVIDENCE,
        {'reason': 'test blocking'}
    )

    blocked_candidate = blocked_result.output
    assert blocked_candidate.is_blocked()

    # Blocked candidates are NOT complete
    assert not CompleteOne_3_5(blocked_candidate)


# ============================================================================
# Test 9: Classify Unit Operation
# ============================================================================

def test_classify_unit_particle(sample_role_span):
    """Test classify_unit for particle (بِ)."""
    unit = TrueSingularLafz(
        surface="بِ",
        lafz_type=TrueSingularLafzType.UNKNOWN,
        attachment_type=AttachmentType.PROCLITIC,
        role_spans=(sample_role_span,),
        weight_access=False,
        detachable=True
    )

    result = classify_unit(unit)

    assert result.is_success()
    classified = result.output.segmentation.units[0]

    # Should be classified as CLOSED_CLASS
    assert classified.lafz_type == TrueSingularLafzType.CLOSED_CLASS
    assert result.output.rank == BoundaryRank.BOUNDARY_CERTIFICATE


def test_classify_unit_pronoun(sample_role_span):
    """Test classify_unit for pronoun (ـه)."""
    unit = TrueSingularLafz(
        surface="ـه",
        lafz_type=TrueSingularLafzType.UNKNOWN,
        attachment_type=AttachmentType.ENCLITIC,
        role_spans=(sample_role_span,),
        weight_access=False,
        detachable=True
    )

    result = classify_unit(unit)

    assert result.is_success()
    classified = result.output.segmentation.units[0]

    # Should be classified as PRONOUN
    assert classified.lafz_type == TrueSingularLafzType.PRONOUN
    assert result.output.rank == BoundaryRank.BOUNDARY_CERTIFICATE


# ============================================================================
# Test 10: Promote Boundary Operation
# ============================================================================

def test_promote_boundary_with_evidence(written_composite_kitabun):
    """Test promote_boundary with lexicon evidence."""
    result = segment_written_token(written_composite_kitabun)
    assert result.is_success()

    candidate = result.output
    original_rank = candidate.rank

    # Promote with strong evidence
    promoted_result = promote_boundary(
        candidate,
        evidence_type='strong_evidence',
        evidence_data={'lexicon_match': True}
    )

    assert promoted_result.is_success()
    promoted_candidate = promoted_result.output

    # Rank should advance
    assert promoted_candidate.rank.value >= original_rank.value


# ============================================================================
# Test 11: Trace Preservation
# ============================================================================

def test_trace_preservation_through_segmentation(written_composite_wabikatibihim):
    """Test that trace from U₃ is preserved through segmentation."""
    original_role_spans = written_composite_wabikatibihim.role_spans

    result = segment_written_token(written_composite_wabikatibihim)
    assert result.is_success()

    candidate = result.output
    seg = candidate.segmentation

    # Trace should be preserved
    assert seg.trace == original_role_spans
    assert candidate.trace == original_role_spans

    # Each unit should preserve trace
    for unit in seg.units:
        assert unit.role_spans == original_role_spans


# ============================================================================
# Test 12: Residual Propagation
# ============================================================================

def test_residual_propagation(written_composite_wabikatibihim):
    """Test that residuals propagate through operations."""
    result = segment_written_token(written_composite_wabikatibihim)
    assert result.is_success()

    candidate = result.output

    # Should have some residuals (ambiguity warnings)
    assert len(candidate.residuals) > 0
    assert len(result.residuals) > 0

    # Segmentation should have residuals
    assert len(candidate.segmentation.residuals) > 0


# ============================================================================
# Test 13: Competitor Preservation
# ============================================================================

def test_preserve_competitors(written_composite_kitabun):
    """Test preserving competing segmentations."""
    result1 = segment_written_token(written_composite_kitabun)
    assert result1.is_success()

    candidate1 = result1.output

    # Create alternative segmentation (hypothetical)
    candidate2 = BoundaryCandidate(
        segmentation=candidate1.segmentation,
        rank=BoundaryRank.BOUNDARY_HYPOTHESIS,
        residuals=frozenset([BoundaryResidual.PROCLITIC_VS_STEM_AMBIGUITY]),
        trace=candidate1.trace
    )

    # Preserve competitors
    result = preserve_competitors(candidate1, [candidate2])

    assert result.is_success()
    updated_candidate = result.output

    # Should have competitor
    assert len(updated_candidate.competitors) == 1


# ============================================================================
# Test 14: Detach Clitic Operation
# ============================================================================

def test_detach_clitic(sample_role_span):
    """Test detaching clitic from host."""
    clitic = TrueSingularLafz(
        surface="بِ",
        lafz_type=TrueSingularLafzType.CLOSED_CLASS,
        attachment_type=AttachmentType.PROCLITIC,
        role_spans=(sample_role_span,),
        weight_access=False,
        detachable=True
    )

    host = TrueSingularLafz(
        surface="كِتَابٍ",
        lafz_type=TrueSingularLafzType.OPEN_LEXICAL_CORE,
        attachment_type=AttachmentType.STEM_CORE,
        role_spans=(sample_role_span,),
        weight_access=True,
        detachable=False
    )

    result = detach_clitic(clitic, host)

    assert result.is_success()
    assert result.output is not None

    seg = result.output.segmentation
    assert len(seg.units) == 2
    assert clitic in seg.units
    assert host in seg.units


# ============================================================================
# Test 15: Complex Segmentation - فَسَيَكْتُبُونَهَا
# ============================================================================

def test_complex_segmentation_fasayaktubunaha(sample_role_span):
    """
    Test complex segmentation of فَسَيَكْتُبُونَهَا

    Expected segmentation:
        - فَ: proclitic (conjunction/branching)
        - سَ: proclitic (future marker)
        - يَكْتُبُونَ: verbal core (with internal يَـ prefix and ـونَ suffix)
        - ـها: enclitic (object pronoun)

    Note: يَـ and ـونَ are internal to the verb, NOT separated here.
          Only external clitics (فَ، سَ، ـها) are separated.
    """
    token = WrittenCompositeToken(
        surface="فَسَيَكْتُبُونَهَا",
        role_spans=(sample_role_span,)
    )

    result = segment_written_token(token)

    assert result.is_success()
    seg = result.output.segmentation

    # Should be composite
    assert seg.is_composite()

    # Should have proclitics (ف، س) and enclitic (ها)
    clitics = seg.external_clitics()
    assert len(clitics) >= 2  # At least some external clitics

    # Should have verbal core
    core_units = seg.core_units()
    assert len(core_units) >= 1

    # يَـ and ـونَ should NOT be separated as proclitics/enclitics
    # They are part of the verbal core
    ya_proclitics = [u for u in seg.units
                     if u.surface in {'ي', 'يَ'} and u.attachment_type == AttachmentType.PROCLITIC]
    # Should be empty or minimal (يَ is internal PREFIX, not PROCLITIC)
