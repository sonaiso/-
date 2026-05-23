"""
Tests for FvafkToSyntaxInputAdapter - FVAFK tokens → syntax_theory SyntacticInput

**Test Suite**: 6 required tests as per FVAFK_GFA_INTEGRATION_MAP.md

**Tests**:
1. Nominal sentence → SyntacticInput
2. Verbal sentence → SyntacticInput with verb valency
3. Interrogative intent → IntentConstraint
4. Imperative intent → IntentConstraint
5. Mixed sentence → correct atom classification
6. Empty sentence → governed failure

**Reference**: docs/FVAFK_GFA_INTEGRATION_MAP.md
"""

import pytest
from typing import List

# FVAFK imports
from fvafk.c2b.word_form import WordForm, Span, Root, Pattern, PartOfSpeech

# Adapter under test
from fvafk.adapters import FvafkToSyntaxInputAdapter

# syntax_theory imports (with fallback)
try:
    from syntax_theory.structures import SyntacticInput, LexicalAtom, IntentConstraint
    SYNTAX_THEORY_AVAILABLE = True
except ImportError:
    SYNTAX_THEORY_AVAILABLE = False
    pytestmark = pytest.mark.skip(reason="syntax_theory not available (Phase 2)")


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def adapter():
    """Create adapter instance"""
    return FvafkToSyntaxInputAdapter()


@pytest.fixture
def nominal_sentence_tokens():
    """
    Nominal sentence: الكِتَابُ جَدِيدٌ (the book is new)

    Tokens:
    1. الكِتَابُ (al-kitābu - the book) - NOUN, mubtada
    2. جَدِيدٌ (jadīdun - new) - NOUN, khabar
    """
    return [
        WordForm(
            surface="الكِتَابُ",
            bare="الكتاب",
            kind="noun",
            pos=PartOfSpeech.NOUN,
            span=Span(start=0, end=8),
            root=Root(
                letters=("ك", "ت", "ب"),
                formatted="ك-ت-ب",
                type="trilateral",
            ),
            pattern=Pattern(
                template="فِعَال",
                type="noun",
                category="noun_pattern",
                stem="كتاب"
            ),
            features={
                "case": "nominative",
                "definiteness": True,
                "number": "singular",
                "gender": "masculine"
            }
        ),
        WordForm(
            surface="جَدِيدٌ",
            bare="جديد",
            kind="noun",
            pos=PartOfSpeech.NOUN,
            span=Span(start=9, end=15),
            root=Root(
                letters=("ج", "د", "د"),
                formatted="ج-د-د",
                type="trilateral",
            ),
            pattern=Pattern(
                template="فَعِيل",
                type="adjective",
                category="adjective_pattern",
                stem="جديد"
            ),
            features={
                "case": "nominative",
                "definiteness": False,
                "number": "singular",
                "gender": "masculine"
            }
        ),
    ]


@pytest.fixture
def verbal_sentence_tokens():
    """
    Verbal sentence: كَتَبَ الطَّالِبُ الدَّرْسَ (the student wrote the lesson)

    Tokens:
    1. كَتَبَ (kataba - wrote) - VERB
    2. الطَّالِبُ (al-ṭālibu - the student) - NOUN, subject
    3. الدَّرْسَ (al-darsa - the lesson) - NOUN, object
    """
    return [
        WordForm(
            surface="كَتَبَ",
            bare="كتب",
            kind="verb",
            pos=PartOfSpeech.VERB,
            span=Span(start=0, end=5),
            root=Root(
                letters=("ك", "ت", "ب"),
                formatted="ك-ت-ب",
                type="trilateral",
            ),
            pattern=Pattern(
                template="فَعَلَ",
                type="verb",
                category="verb_mujarrad",
                stem="كتب"
            ),
            features={
                "tense": "past",
                "person": "3rd",
                "number": "singular",
                "gender": "masculine",
                "valency": 2  # Transitive: subject + object
            }
        ),
        WordForm(
            surface="الطَّالِبُ",
            bare="الطالب",
            kind="noun",
            pos=PartOfSpeech.NOUN,
            span=Span(start=6, end=15),
            root=Root(
                letters=("ط", "ل", "ب"),
                formatted="ط-ل-ب",
                type="trilateral",
            ),
            features={"case": "nominative", "definiteness": True}
        ),
        WordForm(
            surface="الدَّرْسَ",
            bare="الدرس",
            kind="noun",
            pos=PartOfSpeech.NOUN,
            span=Span(start=16, end=23),
            root=Root(
                letters=("د", "ر", "س"),
                formatted="د-ر-س",
                type="trilateral",
            ),
            features={"case": "accusative", "definiteness": True}
        ),
    ]


@pytest.fixture
def interrogative_tokens():
    """
    Interrogative sentence: هَلْ قَرَأْتَ الكِتَابَ؟ (Did you read the book?)

    Tokens:
    1. هَلْ (hal - interrogative particle)
    2. قَرَأْتَ (qara'ta - you read)
    3. الكِتَابَ (al-kitāba - the book)
    """
    return [
        WordForm(
            surface="هَلْ",
            bare="هل",
            kind="particle",
            pos=PartOfSpeech.PARTICLE,
            span=Span(start=0, end=3),
            features={"function": "interrogative_polar"}
        ),
        WordForm(
            surface="قَرَأْتَ",
            bare="قرأت",
            kind="verb",
            pos=PartOfSpeech.VERB,
            span=Span(start=4, end=10),
            features={"tense": "past", "person": "2nd"}
        ),
        WordForm(
            surface="الكِتَابَ",
            bare="الكتاب",
            kind="noun",
            pos=PartOfSpeech.NOUN,
            span=Span(start=11, end=19),
            features={"case": "accusative", "definiteness": True}
        ),
    ]


@pytest.fixture
def imperative_tokens():
    """
    Imperative sentence: اقْرَأِ الكِتَابَ (Read the book!)

    Tokens:
    1. اقْرَأْ (iqra' - read! - imperative verb)
    2. الكِتَابَ (al-kitāba - the book)
    """
    return [
        WordForm(
            surface="اقْرَأْ",
            bare="اقرأ",
            kind="verb",
            pos=PartOfSpeech.VERB,
            span=Span(start=0, end=6),
            features={"mood": "imperative", "person": "2nd"}
        ),
        WordForm(
            surface="الكِتَابَ",
            bare="الكتاب",
            kind="noun",
            pos=PartOfSpeech.NOUN,
            span=Span(start=7, end=15),
            features={"case": "accusative", "definiteness": True}
        ),
    ]


@pytest.fixture
def mixed_sentence_tokens():
    """
    Mixed sentence: إنَّ الطَّالِبَ يَكْتُبُ الدَّرْسَ (Indeed, the student writes the lesson)

    Tokens:
    1. إنَّ (inna - operator/particle)
    2. الطَّالِبَ (al-ṭāliba - the student - accusative after inna)
    3. يَكْتُبُ (yaktubu - writes - present verb)
    4. الدَّرْسَ (al-darsa - the lesson)
    """
    return [
        WordForm(
            surface="إنَّ",
            bare="إن",
            kind="operator",
            pos=PartOfSpeech.OPERATOR,
            span=Span(start=0, end=3),
            features={"family": "inna_sisters", "effect": "nasb"}
        ),
        WordForm(
            surface="الطَّالِبَ",
            bare="الطالب",
            kind="noun",
            pos=PartOfSpeech.NOUN,
            span=Span(start=4, end=13),
            features={"case": "accusative", "definiteness": True}
        ),
        WordForm(
            surface="يَكْتُبُ",
            bare="يكتب",
            kind="verb",
            pos=PartOfSpeech.VERB,
            span=Span(start=14, end=21),
            features={"tense": "present", "person": "3rd"}
        ),
        WordForm(
            surface="الدَّرْسَ",
            bare="الدرس",
            kind="noun",
            pos=PartOfSpeech.NOUN,
            span=Span(start=22, end=29),
            features={"case": "accusative", "definiteness": True}
        ),
    ]


# ============================================================================
# Test 1: Nominal sentence → SyntacticInput
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_1_nominal_sentence_to_syntactic_input(adapter, nominal_sentence_tokens):
    """
    Test 1: Nominal sentence → SyntacticInput

    **Success Criteria**:
    - Returns SyntacticInput instance
    - Contains 2 LexicalAtoms (mubtada + khabar)
    - Intent constraints for declarative
    - Preserves token order
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.adapt_tokens(nominal_sentence_tokens, intent="declarative")

    # Assert
    assert isinstance(result, SyntacticInput), "Should return SyntacticInput"
    assert hasattr(result, 'atoms'), "SyntacticInput should have atoms"
    assert len(result.atoms) == 2, "Should have 2 atoms (mubtada + khabar)"
    assert hasattr(result, 'constraints'), "SyntacticInput should have constraints"


# ============================================================================
# Test 2: Verbal sentence → SyntacticInput with verb valency
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_2_verbal_sentence_with_valency(adapter, verbal_sentence_tokens):
    """
    Test 2: Verbal sentence → SyntacticInput with verb valency

    **Success Criteria**:
    - Returns SyntacticInput with 3 atoms (verb + subject + object)
    - Verb atom has valency information (transitive)
    - Atom types correctly classified (VERB, NOUN, NOUN)
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.adapt_tokens(verbal_sentence_tokens, intent="declarative")

    # Assert
    assert isinstance(result, SyntacticInput)
    assert len(result.atoms) == 3, "Should have 3 atoms (verb + subject + object)"

    # Check verb atom has valency
    verb_atom = result.atoms[0]
    assert hasattr(verb_atom, 'valency') or hasattr(verb_atom, 'verb_valency'), \
        "Verb atom should have valency information"


# ============================================================================
# Test 3: Interrogative intent → IntentConstraint
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_3_interrogative_intent_constraint(adapter, interrogative_tokens):
    """
    Test 3: Interrogative intent → IntentConstraint

    **Success Criteria**:
    - Returns SyntacticInput with interrogative constraints
    - Detects interrogative particle (هل)
    - Intent type is "interrogative_polar"
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.adapt_tokens(interrogative_tokens, intent="interrogative")

    # Assert
    assert isinstance(result, SyntacticInput)
    assert hasattr(result, 'constraints')
    assert len(result.constraints) > 0, "Should have intent constraints"

    # Check for interrogative constraint
    constraint_types = [c.type if hasattr(c, 'type') else c for c in result.constraints]
    assert any("interrogative" in str(c).lower() for c in constraint_types), \
        "Should have interrogative constraint"


# ============================================================================
# Test 4: Imperative intent → IntentConstraint
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_4_imperative_intent_constraint(adapter, imperative_tokens):
    """
    Test 4: Imperative intent → IntentConstraint

    **Success Criteria**:
    - Returns SyntacticInput with imperative constraints
    - Detects imperative mood in verb
    - Intent type is "imperative"
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.adapt_tokens(imperative_tokens, intent="imperative")

    # Assert
    assert isinstance(result, SyntacticInput)
    assert hasattr(result, 'constraints')

    # Check for imperative constraint
    constraint_types = [c.type if hasattr(c, 'type') else c for c in result.constraints]
    assert any("imperative" in str(c).lower() for c in constraint_types), \
        "Should have imperative constraint"


# ============================================================================
# Test 5: Mixed sentence → correct atom classification
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_5_mixed_sentence_atom_classification(adapter, mixed_sentence_tokens):
    """
    Test 5: Mixed sentence → correct atom classification

    **Success Criteria**:
    - Correctly classifies OPERATOR (إنَّ)
    - Correctly classifies NOUNs
    - Correctly classifies VERB
    - Preserves operator effect information
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.adapt_tokens(mixed_sentence_tokens, intent="declarative")

    # Assert
    assert isinstance(result, SyntacticInput)
    assert len(result.atoms) == 4, "Should have 4 atoms"

    # Check atom types
    # Note: Exact attribute names depend on syntax_theory implementation
    atom_types = [getattr(atom, 'lexical_type', None) for atom in result.atoms]
    assert "OPERATOR" in str(atom_types) or "PARTICLE" in str(atom_types), \
        "Should classify operator/particle"
    assert "NOUN" in str(atom_types), "Should classify nouns"
    assert "VERB" in str(atom_types), "Should classify verb"


# ============================================================================
# Test 6: Empty sentence → governed failure
# ============================================================================

def test_6_empty_sentence_governed_failure(adapter):
    """
    Test 6: Empty sentence → governed failure

    **Governance Law**: Returns gracefully (not crash) for empty input

    **Success Criteria**:
    - Does NOT raise exception
    - Returns either:
      * Empty SyntacticInput, or
      * Raises NotImplementedError (adapter stub), or
      * Returns None
    """
    # Act & Assert: Should not crash
    empty_tokens = []

    if not SYNTAX_THEORY_AVAILABLE:
        # Adapter should raise NotImplementedError (stub)
        with pytest.raises(NotImplementedError):
            adapter.adapt_tokens(empty_tokens)
    else:
        # Should handle gracefully
        try:
            result = adapter.adapt_tokens(empty_tokens)
            # Accept any graceful handling:
            # - None, or
            # - Empty SyntacticInput, or
            # - SyntacticInput with empty atoms
            if result is not None:
                assert isinstance(result, SyntacticInput)
        except (ValueError, AssertionError) as e:
            # Graceful error acceptable
            assert "empty" in str(e).lower() or "no tokens" in str(e).lower(), \
                f"Error should mention empty input: {e}"
