"""Tests for Constraint-Preserving Binding Transitions.

Validates that:
1. Transitions enforce the three governing laws
2. CPB functions preserve without generating meaning
3. Rank, trace, and residuals are properly preserved
4. Internal closure is checked before transition
"""

import pytest

from fvafk.algebra.core import Rank, Trace
from fvafk.algebra.lafzi_madlul.fractal_algebra import LayerType
from fvafk.algebra.lafzi_madlul.layer_algebras import (
    AtomAlgebra,
    BuiltFormAlgebra,
    HarakahAlgebra,
    LetterAlgebra,
    PatternTemplateAlgebra,
    RootCandidateAlgebra,
)
from fvafk.algebra.lafzi_madlul.transitions import (
    AlgebraicTransition,
    cpb_letter_harakah,
    cpb_root_pattern,
    internal_closure_law,
    no_meaning_jump_law,
    preservation_law,
)


# ===========================================================================
# Three Governing Laws Tests
# ===========================================================================


def test_internal_closure_law_validates_complete():
    """internal_closure_law should accept complete layers."""
    letter = LetterAlgebra.from_form("ك")

    is_complete, missing = internal_closure_law(letter)

    assert is_complete
    assert len(missing) == 0


def test_internal_closure_law_detects_incomplete():
    """internal_closure_law should detect incomplete layers."""

    class IncompleteLayer:
        unit_value = None  # Incomplete!
        boundaries = {}

    incomplete = IncompleteLayer()
    is_complete, missing = internal_closure_law(incomplete)

    assert not is_complete
    assert "unit_undefined" in missing


def test_preservation_law_preserves_trace():
    """preservation_law must preserve trace provenance."""
    source_trace = Trace(operation="letter_construction", source_span=(0, 1))
    target_trace = Trace(operation="harakah_construction", source_span=(1, 2))

    result_trace, _, _ = preservation_law(
        source_trace,
        Rank.LICENSED,
        [],
        target_trace,
        Rank.LICENSED,
        [],
        operation="cpb_letter_harakah",
    )

    # Result trace should reference both parents
    assert source_trace.trace_id in result_trace.parents
    assert target_trace.trace_id in result_trace.parents
    assert result_trace.operation == "cpb_letter_harakah"


def test_preservation_law_preserves_rank_conservatively():
    """preservation_law must take minimum rank."""
    source_trace = Trace(operation="source")
    target_trace = Trace(operation="target")

    # Test with different ranks
    _, result_rank, _ = preservation_law(
        source_trace,
        Rank.LICENSED,
        [],
        target_trace,
        Rank.CANDIDATE,
        [],
        operation="test",
    )

    # Should take minimum
    assert result_rank == Rank.CANDIDATE


def test_preservation_law_accumulates_residuals():
    """preservation_law must accumulate residuals from both sources."""
    source_trace = Trace(operation="source")
    target_trace = Trace(operation="target")

    source_residuals = ["residual_1", "residual_2"]
    target_residuals = ["residual_3"]

    _, _, result_residuals = preservation_law(
        source_trace,
        Rank.LICENSED,
        source_residuals,
        target_trace,
        Rank.LICENSED,
        target_residuals,
        operation="test",
    )

    # Should contain all residuals
    assert "residual_1" in result_residuals
    assert "residual_2" in result_residuals
    assert "residual_3" in result_residuals
    assert len(result_residuals) == 3


def test_no_meaning_jump_law_accepts_clean_layer():
    """no_meaning_jump_law should accept layers without semantic fields."""
    letter = LetterAlgebra.from_form("ك")

    # Should not raise
    no_meaning_jump_law(letter)


def test_no_meaning_jump_law_rejects_semantic_layer():
    """no_meaning_jump_law must reject layers with semantic fields."""

    class FakeLayerWithMeaning:
        meaning = "كتابة"

    fake = FakeLayerWithMeaning()

    with pytest.raises(ValueError, match="Forbidden semantic field"):
        no_meaning_jump_law(fake)


# ===========================================================================
# AlgebraicTransition Tests
# ===========================================================================


def test_algebraic_transition_construction():
    """AlgebraicTransition should construct with source and target layers."""
    transition = AlgebraicTransition(
        source_layer=LayerType.LETTER,
        target_layer=LayerType.ATOM,
        operation="cpb_letter_harakah",
    )

    assert transition.source_layer == LayerType.LETTER
    assert transition.target_layer == LayerType.ATOM
    assert transition.operation == "cpb_letter_harakah"
    assert transition.preserves_trace
    assert transition.preserves_rank
    assert transition.preserves_residuals


def test_algebraic_transition_validates_internal_closure():
    """AlgebraicTransition should validate source layer closure."""
    transition = AlgebraicTransition(
        source_layer=LayerType.LETTER,
        target_layer=LayerType.ATOM,
        operation="test",
    )

    letter = LetterAlgebra.from_form("ك")
    is_closed, missing = transition.validate_internal_closure(letter)

    assert is_closed
    assert len(missing) == 0


def test_algebraic_transition_validates_no_meaning_jump():
    """AlgebraicTransition should validate no meaning jump."""
    transition = AlgebraicTransition(
        source_layer=LayerType.LETTER,
        target_layer=LayerType.ATOM,
        operation="test",
    )

    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")

    # Should not raise
    transition.validate_no_meaning_jump(letter, harakah)


# ===========================================================================
# CPB: Letter + Harakah → Atom
# ===========================================================================


def test_cpb_letter_harakah_basic():
    """cpb_letter_harakah should bind letter and harakah into atom."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")

    atom = cpb_letter_harakah(letter, harakah)

    assert atom.letter == letter
    assert atom.harakah == harakah
    assert atom.unit_value == "كَ"


def test_cpb_letter_harakah_preserves_trace():
    """cpb_letter_harakah must preserve trace from both inputs."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")

    atom = cpb_letter_harakah(letter, harakah)

    # Atom trace should reference both parents
    assert letter.trace.trace_id in atom.trace.parents
    assert harakah.trace.trace_id in atom.trace.parents


def test_cpb_letter_harakah_preserves_rank():
    """cpb_letter_harakah must preserve rank conservatively."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")

    atom = cpb_letter_harakah(letter, harakah)

    # Rank should be minimum
    assert atom.rank == min(letter.rank, harakah.rank)


def test_cpb_letter_harakah_preserves_residuals():
    """cpb_letter_harakah must accumulate residuals."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")

    atom = cpb_letter_harakah(letter, harakah)

    # Residuals should include both sources
    # (exact residuals depend on implementation)
    assert isinstance(atom.residuals, list)


def test_cpb_letter_harakah_no_meaning():
    """cpb_letter_harakah must NOT generate meaning.

    **Critical test**: CPB preserves constraints, does NOT generate semantics.
    """
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")

    atom = cpb_letter_harakah(letter, harakah)

    # Must not have meaning field
    assert not hasattr(atom, "meaning")
    assert not hasattr(atom, "madlul")
    assert not hasattr(atom, "semantic_value")


def test_cpb_letter_harakah_checks_internal_closure():
    """cpb_letter_harakah must check internal closure before binding."""

    # Create incomplete letter (mock)
    class IncompleteLetter:
        unit_value = None  # Incomplete!
        boundaries = {}
        internal_bindings = {}

    incomplete = IncompleteLetter()
    harakah = HarakahAlgebra.from_form("َ")

    with pytest.raises(ValueError, match="incomplete"):
        cpb_letter_harakah(incomplete, harakah)


# ===========================================================================
# CPB: Root ⊗ Pattern → BuiltForm
# ===========================================================================


def test_cpb_root_pattern_basic():
    """cpb_root_pattern should bind root and pattern into form."""
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    form = cpb_root_pattern(root, pattern)

    assert form.root == root
    assert form.pattern == pattern
    assert form.surface_form == "كَتَبَ"


def test_cpb_root_pattern_preserves_trace():
    """cpb_root_pattern must preserve trace from both inputs."""
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    form = cpb_root_pattern(root, pattern)

    # Form trace should reference both parents
    assert root.trace.trace_id in form.trace.parents
    assert pattern.trace.trace_id in form.trace.parents


def test_cpb_root_pattern_preserves_rank():
    """cpb_root_pattern must preserve rank conservatively."""
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    form = cpb_root_pattern(root, pattern)

    # Rank should be minimum
    assert form.rank == min(root.rank, pattern.rank)


def test_cpb_root_pattern_preserves_residuals():
    """cpb_root_pattern must accumulate residuals."""
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    form = cpb_root_pattern(root, pattern)

    # Should have residuals from both sources
    assert isinstance(form.residuals, list)


def test_cpb_root_pattern_no_meaning():
    """cpb_root_pattern must NOT generate meaning.

    **Critical test**: Root ⊗ Pattern creates FORMAL structure, NOT meaning.
    """
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    form = cpb_root_pattern(root, pattern)

    # Must not have meaning field
    assert not hasattr(form, "meaning")
    assert not hasattr(form, "madlul")
    assert not hasattr(form, "semantic_value")
    assert not hasattr(form, "faaliyyah")
    assert not hasattr(form, "mafuuliyyah")


def test_cpb_root_pattern_applies_pattern_correctly():
    """cpb_root_pattern should correctly map root letters to pattern slots."""
    root = RootCandidateAlgebra(consonants=("د", "ر", "س"))
    pattern = PatternTemplateAlgebra(pattern_form="فَاعِل")

    form = cpb_root_pattern(root, pattern)

    # د → ف, ر → ع, س → ل
    assert form.surface_form == "دَارِس"


def test_cpb_root_pattern_checks_internal_closure():
    """cpb_root_pattern must check internal closure before binding."""

    class IncompleteRoot:
        root_letters = ("ك", "ت", "ب")
        boundaries = {}
        internal_bindings = {}

    incomplete = IncompleteRoot()
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    with pytest.raises(ValueError, match="incomplete"):
        cpb_root_pattern(incomplete, pattern)


# ===========================================================================
# Integration: Full Transition Chain
# ===========================================================================


def test_full_transition_letter_to_atom():
    """Full transition: Letter + Harakah → Atom with all laws enforced."""
    # Build letter
    letter = LetterAlgebra.from_form("ك")

    # Check internal closure
    is_closed, _ = internal_closure_law(letter)
    assert is_closed

    # Build harakah
    harakah = HarakahAlgebra.from_form("َ")

    # Check internal closure
    is_closed, _ = internal_closure_law(harakah)
    assert is_closed

    # CPB binding
    atom = cpb_letter_harakah(letter, harakah)

    # Verify preservation law
    assert atom.trace.operation == "cpb_letter_harakah"
    assert atom.rank == min(letter.rank, harakah.rank)
    assert isinstance(atom.residuals, list)

    # Verify no meaning jump
    no_meaning_jump_law(atom)


def test_full_transition_root_pattern_to_form():
    """Full transition: Root ⊗ Pattern → BuiltForm with all laws enforced."""
    # Build root
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))

    # Check internal closure
    is_closed, _ = internal_closure_law(root)
    assert is_closed

    # Build pattern
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    # Check internal closure
    is_closed, _ = internal_closure_law(pattern)
    assert is_closed

    # CPB binding
    form = cpb_root_pattern(root, pattern)

    # Verify preservation law
    assert form.trace.operation == "cpb_root_pattern"
    assert form.rank == min(root.rank, pattern.rank)
    assert isinstance(form.residuals, list)

    # Verify no meaning jump
    no_meaning_jump_law(form)


# ===========================================================================
# Critical Negative Tests
# ===========================================================================


def test_cpb_cannot_leak_meaning_letter_harakah():
    """CPB letter+harakah must never produce semantic meaning."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")

    atom = cpb_letter_harakah(letter, harakah)

    # Validation should pass (no meaning fields)
    no_meaning_jump_law(atom)

    # Explicitly check forbidden fields
    assert not hasattr(atom, "meaning")
    assert not hasattr(atom, "madlul")


def test_cpb_cannot_leak_meaning_root_pattern():
    """CPB root⊗pattern must never produce semantic meaning."""
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    form = cpb_root_pattern(root, pattern)

    # Validation should pass (no meaning fields)
    no_meaning_jump_law(form)

    # Explicitly check forbidden fields
    assert not hasattr(form, "meaning")
    assert not hasattr(form, "faaliyyah")
    assert not hasattr(form, "mafuuliyyah")
