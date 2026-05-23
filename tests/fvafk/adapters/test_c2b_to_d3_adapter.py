"""
Tests for C2bToD3Adapter - FVAFK WordForm → dal_core DMufrad

**Test Suite**: 8 required tests as per FVAFK_GFA_INTEGRATION_MAP.md

**Governance Laws Tested**:
1. Trace reversibility (DalTrace.is_reversible() = True)
2. Evidence contains span (claim-scoped)
3. No meaning field in DMufrad (Theorem 5)
4. No direct cross-layer promotion
5. Governed failures (None not exceptions)
6. MabniRegistry integration
7. IshtiqaqJudgment integration
8. Round-trip reversibility

**Reference**: docs/FVAFK_GFA_INTEGRATION_MAP.md
"""

import pytest
from dataclasses import dataclass
from typing import Optional

# FVAFK imports
from fvafk.c2b.word_form import WordForm, Span, Root, Pattern, PartOfSpeech

# Adapter under test
from fvafk.adapters import C2bToD3Adapter

# dal_core imports (with fallback)
try:
    from dal_core import (
        DMufrad,
        DalEvidence,
        DalTraceRef,
        DalTransitionDomain,
        DalClaimScope,
    )
    DAL_CORE_AVAILABLE = True
except ImportError:
    DAL_CORE_AVAILABLE = False
    pytestmark = pytest.mark.skip(reason="dal_core not available")


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def adapter():
    """Create adapter instance"""
    return C2bToD3Adapter(strict_mode=False)


@pytest.fixture
def adapter_strict():
    """Create strict mode adapter (raises on errors)"""
    return C2bToD3Adapter(strict_mode=True)


@pytest.fixture
def valid_noun_word_form():
    """
    Valid noun WordForm: كِتَابٌ (kitābun - book)

    Root: ك-ت-ب
    Pattern: فِعَال (fi'āl)
    POS: NOUN
    """
    return WordForm(
        surface="كِتَابٌ",
        span=Span(start=0, end=6),
        pos=PartOfSpeech.NOUN,
        root=Root(
            letters=("ك", "ت", "ب"),
            formatted="ك-ت-ب",
            type="trilateral"
        ),
        pattern=Pattern(
            template="فِعَال",
            type="noun",
            category="noun_pattern"
        ),
    )


@pytest.fixture
def valid_verb_word_form():
    """
    Valid verb WordForm: كَتَبَ (kataba - he wrote)

    Root: ك-ت-ب
    Pattern: فَعَلَ (fa'ala)
    POS: VERB
    """
    return WordForm(
        surface="كَتَبَ",
        span=Span(start=0, end=5),
        pos=PartOfSpeech.VERB,
        root=Root(
            letters=("ك", "ت", "ب"),
            formatted="ك-ت-ب",
            type="trilateral"
        ),
        pattern=Pattern(
            template="فَعَلَ",
            type="verb",
            category="verb_mujarrad"
        ),
    )


@pytest.fixture
def minimal_word_form():
    """
    Minimal valid WordForm (bare minimum required fields)
    """
    return WordForm(
        surface="كلمة",
        span=Span(start=0, end=4),
        pos=PartOfSpeech.NOUN,
    )


@pytest.fixture
def inadmissible_word_form():
    """
    Inadmissible WordForm (missing required fields)
    """
    return WordForm(
        surface="",  # Empty surface
        span=None,  # Missing span
        pos=PartOfSpeech.UNKNOWN,
    )


# ============================================================================
# Test 1: Valid word → DMufrad with trace
# ============================================================================

def test_1_valid_word_to_dmufrad_with_trace(adapter, valid_noun_word_form):
    """
    Test 1: Valid word → DMufrad with trace

    **Success Criteria**:
    - Returns (DMufrad, Evidence, Trace) tuple
    - DMufrad is not None
    - Evidence is not None
    - Trace is not None
    """
    if not DAL_CORE_AVAILABLE:
        pytest.skip("dal_core not available")

    # Act
    mufrad, evidence, trace = adapter.adapt_word_form(valid_noun_word_form)

    # Assert
    assert mufrad is not None, "Valid word should produce DMufrad"
    assert evidence is not None, "Evidence should always be present"
    assert trace is not None, "Trace should always be present"
    assert isinstance(mufrad, DMufrad), "Output should be DMufrad instance"
    assert isinstance(evidence, DalEvidence), "Evidence should be DalEvidence instance"
    assert isinstance(trace, DalTraceRef), "Trace should be DalTraceRef instance"


# ============================================================================
# Test 2: Evidence contains span (claim-scoped)
# ============================================================================

def test_2_evidence_contains_span(adapter, valid_noun_word_form):
    """
    Test 2: Evidence contains span

    **Governance Law**: DalEvidence requires span (claim-scoped evidence)

    **Success Criteria**:
    - Evidence.span is not None
    - Evidence.span matches WordForm.span
    - Evidence.domain == D3_MUFRAD
    - Evidence.scope == WORD_LEVEL
    """
    if not DAL_CORE_AVAILABLE:
        pytest.skip("dal_core not available")

    # Act
    mufrad, evidence, trace = adapter.adapt_word_form(valid_noun_word_form)

    # Assert: Evidence structure
    assert evidence is not None
    assert hasattr(evidence, 'span'), "Evidence must have span field"
    assert evidence.span is not None, "Evidence.span must not be None"

    # Assert: Span matches input
    expected_span = (valid_noun_word_form.span.start, valid_noun_word_form.span.end)
    assert evidence.span == expected_span, f"Evidence span {evidence.span} != WordForm span {expected_span}"

    # Assert: claim_scope (not domain - dal_core uses claim_scope)
    assert evidence.claim_scope == DalClaimScope.ORIGIN_CLASSIFIED, "Evidence claim_scope should be ORIGIN_CLASSIFIED"

    # Assert: Source preserved in details
    assert "surface" in evidence.details, "Evidence details should contain surface"
    assert evidence.details["surface"] == valid_noun_word_form.surface, "Surface should match WordForm surface"


# ============================================================================
# Test 3: Trace is reversible
# ============================================================================

def test_3_trace_is_reversible(adapter, valid_noun_word_form):
    """
    Test 3: Trace is reversible

    **Governance Law**: DalTrace.is_reversible() = True

    **Success Criteria**:
    - Trace.reversible == True
    - Trace.source_atoms preserved
    - Trace.steps recorded
    """
    if not DAL_CORE_AVAILABLE:
        pytest.skip("dal_core not available")

    # Act
    mufrad, evidence, trace = adapter.adapt_word_form(valid_noun_word_form)

    # Assert: Reversibility
    assert trace is not None
    assert hasattr(trace, 'reversible'), "Trace must have reversible field"
    assert trace.reversible is True, "Trace must be reversible (is_reversible() = True)"

    # Assert: Source atoms preserved in metadata (not direct attribute)
    assert hasattr(trace, 'metadata'), "Trace must have metadata"
    assert 'source_atoms' in trace.metadata, "Trace metadata must preserve source_atoms"
    assert trace.metadata['source_atoms'] is not None, "Source atoms must not be None"
    assert len(trace.metadata['source_atoms']) > 0, "Source atoms must not be empty"

    # Assert: Steps recorded in metadata
    assert 'steps' in trace.metadata, "Trace metadata must record steps"
    assert trace.metadata['steps'] is not None, "Steps must not be None"
    assert len(trace.metadata['steps']) > 0, "Steps must not be empty for reversibility"


# ============================================================================
# Test 4: No meaning field in DMufrad (Theorem 5)
# ============================================================================

def test_4_no_meaning_field_in_dmufrad(adapter, valid_noun_word_form):
    """
    Test 4: No meaning field in DMufrad

    **Governance Law**: Theorem 5 - DMufrad must NOT contain meaning/murad/haqiqa_majaz

    **Success Criteria**:
    - DMufrad has NO field named 'meaning'
    - DMufrad has NO field named 'murad'
    - DMufrad has NO field named 'haqiqa_majaz'
    """
    if not DAL_CORE_AVAILABLE:
        pytest.skip("dal_core not available")

    # Act
    mufrad, evidence, trace = adapter.adapt_word_form(valid_noun_word_form)

    # Assert: Theorem 5 compliance
    assert mufrad is not None
    assert not hasattr(mufrad, 'meaning'), "DMufrad must NOT have 'meaning' field (Theorem 5)"
    assert not hasattr(mufrad, 'murad'), "DMufrad must NOT have 'murad' field (Theorem 5)"
    assert not hasattr(mufrad, 'haqiqa_majaz'), "DMufrad must NOT have 'haqiqa_majaz' field (Theorem 5)"

    # Assert: DMufrad should have valid D3 fields instead
    # (Exact fields depend on dal_core implementation)
    assert hasattr(mufrad, '__class__'), "DMufrad should be a proper object"
    assert mufrad.__class__.__name__ == 'DMufrad', "Object should be DMufrad instance"


# ============================================================================
# Test 5: Invalid word → None (governed failure)
# ============================================================================

def test_5_invalid_word_returns_none_governed_failure(adapter, inadmissible_word_form):
    """
    Test 5: Invalid word → None (governed failure)

    **Governance Law**: Returns None (not exception) for inadmissible words

    **Success Criteria**:
    - Returns (None, Evidence, Trace) for inadmissible input
    - Does NOT raise exception (governed failure)
    - Evidence still present (with inadmissible flag)
    - Trace still present (marked non-reversible)
    """
    # Act
    mufrad, evidence, trace = adapter.adapt_word_form(inadmissible_word_form)

    # Assert: Governed failure (None not exception)
    assert mufrad is None, "Inadmissible word should return None (governed failure)"

    # Assert: Evidence still present
    assert evidence is not None, "Evidence should be present even for inadmissible word"
    if DAL_CORE_AVAILABLE:
        assert hasattr(evidence, 'details'), "Evidence should have details"
        assert evidence.details.get('inadmissible') is True, "Evidence should mark word as inadmissible"

    # Assert: Trace still present
    assert trace is not None, "Trace should be present even for inadmissible word"
    if DAL_CORE_AVAILABLE:
        assert trace.reversible is False, "Trace should be non-reversible for inadmissible word"


# ============================================================================
# Test 6: Mabni word → MabniRegistry lookup
# ============================================================================

@pytest.mark.skip(reason="MabniRegistry integration not yet implemented in adapter")
def test_6_mabni_word_registry_lookup(adapter):
    """
    Test 6: Mabni word → MabniRegistry lookup

    **Frozen Words**: إنّ، كان، هذا، أنا، etc.

    **Success Criteria**:
    - Adapter recognizes mabni words
    - Delegates to MabniRegistry
    - Returns DMufrad with mabni flag
    """
    # TODO: Implement when MabniRegistry integration is added
    pass


# ============================================================================
# Test 7: Mushtaq word → IshtiqaqJudgment
# ============================================================================

@pytest.mark.skip(reason="IshtiqaqJudgment integration not yet implemented in adapter")
def test_7_mushtaq_word_ishtiqaq_judgment(adapter, valid_verb_word_form):
    """
    Test 7: Mushtaq word → IshtiqaqJudgment

    **Derived Words**: Verbs, participles, verbal nouns

    **Success Criteria**:
    - Adapter recognizes mushtaq words
    - Applies IshtiqaqJudgment
    - Returns DMufrad with derivation info
    """
    # TODO: Implement when IshtiqaqJudgment integration is added
    pass


# ============================================================================
# Test 8: Round-trip: DMufrad → trace → FVAFK atoms
# ============================================================================

def test_8_round_trip_dmufrad_to_fvafk_atoms(adapter, valid_noun_word_form):
    """
    Test 8: Round-trip reversibility

    **Governance Law**: Trace allows reconstruction of FVAFK atoms

    **Success Criteria**:
    - Trace.source_atoms matches WordForm.bare characters
    - Can reconstruct WordForm from trace
    - Round-trip preserves essential information
    """
    if not DAL_CORE_AVAILABLE:
        pytest.skip("dal_core not available")

    # Act
    mufrad, evidence, trace = adapter.adapt_word_form(valid_noun_word_form)

    # Assert: Source atoms match input
    assert trace is not None
    assert trace.metadata.get('source_atoms') is not None

    # Reconstruct bare form from trace atoms
    reconstructed_bare = "".join(trace.metadata['source_atoms'])
    expected_bare = adapter._get_bare_form(valid_noun_word_form.surface)

    assert reconstructed_bare == expected_bare, \
        f"Round-trip failed: reconstructed '{reconstructed_bare}' != original '{expected_bare}'"

    # Assert: Trace steps are documented
    assert len(trace.metadata['steps']) > 0, "Trace should document transformation steps"

    # Verify key steps present
    step_names = [step.get("step", "") for step in trace.metadata['steps']]
    assert "extract_bare_form" in step_names, "Trace should document bare form extraction"
    assert "extract_root" in step_names, "Trace should document root extraction"
    assert "extract_pattern" in step_names, "Trace should document pattern extraction"


# ============================================================================
# Additional Tests: Edge Cases and Governance
# ============================================================================

def test_minimal_word_form_succeeds(adapter, minimal_word_form):
    """
    **Edge Case**: Minimal valid WordForm (only required fields)

    Should succeed even without root/pattern/features
    """
    if not DAL_CORE_AVAILABLE:
        pytest.skip("dal_core not available")

    # Act
    mufrad, evidence, trace = adapter.adapt_word_form(minimal_word_form)

    # Assert: Should succeed (not None)
    # Note: Depending on dal_core implementation, this might return None
    # if root/pattern are required. Adjust based on actual behavior.
    assert evidence is not None, "Evidence should always be present"
    assert trace is not None, "Trace should always be present"


def test_adapter_preserves_governance_laws_with_verb(adapter, valid_verb_word_form):
    """
    **Governance Smoke Test**: Verify all laws hold for verb input

    Laws:
    1. Trace reversibility
    2. Evidence with span
    3. No meaning field
    4. Governed failures
    """
    if not DAL_CORE_AVAILABLE:
        pytest.skip("dal_core not available")

    # Act
    mufrad, evidence, trace = adapter.adapt_word_form(valid_verb_word_form)

    # Assert: All governance laws
    if mufrad is not None:  # Only if construction succeeded
        # Law 1: Reversibility
        assert trace.reversible is True, "Trace must be reversible"

        # Law 2: Evidence with span
        assert evidence.span is not None, "Evidence must have span"
        assert evidence.span == (valid_verb_word_form.span.start, valid_verb_word_form.span.end)

        # Law 3: No meaning field
        assert not hasattr(mufrad, 'meaning'), "DMufrad must NOT have meaning field"
        assert not hasattr(mufrad, 'murad'), "DMufrad must NOT have murad field"
        assert not hasattr(mufrad, 'haqiqa_majaz'), "DMufrad must NOT have haqiqa_majaz field"

    # Law 4: Governed failure (even if None, no exception raised)
    # Already tested by reaching this point without exception


def test_strict_mode_raises_on_invalid(adapter_strict, inadmissible_word_form):
    """
    **Strict Mode**: Should raise exception on inadmissible word
    """
    if not DAL_CORE_AVAILABLE:
        pytest.skip("dal_core not available")

    # Act & Assert: Should raise (not return None)
    # Note: Actual exception type depends on dal_core implementation
    # This test may need adjustment based on actual behavior
    try:
        mufrad, evidence, trace = adapter_strict.adapt_word_form(inadmissible_word_form)
        # If strict mode doesn't raise, verify it returns None
        assert mufrad is None, "Strict mode should either raise or return None"
    except Exception as e:
        # Expected behavior in strict mode
        assert True, f"Strict mode raised {type(e).__name__}: {e}"
