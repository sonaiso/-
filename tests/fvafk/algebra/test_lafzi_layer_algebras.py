"""Tests for Layer Algebra Implementations.

Validates that:
1. Each layer algebra correctly implements its specific structure
2. Validation functions prevent meaning leakage
3. Factory methods work correctly
4. Residuals accumulate properly
"""

import pytest

from fvafk.algebra.core import Rank, Trace
from fvafk.algebra.lafzi_madlul.fractal_algebra import LayerType, validate_no_meaning_field
from fvafk.algebra.lafzi_madlul.layer_algebras import (
    AtomAlgebra,
    BuiltFormAlgebra,
    HarakahAlgebra,
    HarakahRole,
    HarakahType,
    LetterAlgebra,
    LetterRole,
    LetterType,
    PatternTemplateAlgebra,
    RootCandidateAlgebra,
    RootType,
    SyllableAlgebra,
    SyllableType,
    TraceAlgebra,
    WordCandidateAlgebra,
)


# ===========================================================================
# Layer 0: Trace Algebra
# ===========================================================================


def test_trace_algebra_construction():
    """TraceAlgebra should construct with minimal info."""
    trace_alg = TraceAlgebra(
        unit_value="ك",
        trace_type="رسم",
        is_readable=True,
    )

    assert trace_alg.unit_type == LayerType.TRACE
    assert trace_alg.unit_value == "ك"
    assert trace_alg.trace_type == "رسم"
    assert trace_alg.is_readable


def test_trace_algebra_no_meaning():
    """TraceAlgebra must not have semantic meaning field."""
    trace_alg = TraceAlgebra(unit_value="ك")

    # Should not raise
    validate_no_meaning_field(trace_alg)


# ===========================================================================
# Layer 1: Letter Algebra
# ===========================================================================


def test_letter_from_form_simple():
    """LetterAlgebra.from_form should construct from simple letter."""
    letter = LetterAlgebra.from_form("ك")

    assert letter.unit_value == "ك"
    assert letter.letter_type == LetterType.CONSONANT
    assert letter.role == LetterRole.UNRESOLVED


def test_letter_from_form_vowel():
    """LetterAlgebra.from_form should classify vowels correctly."""
    alif = LetterAlgebra.from_form("ا")

    assert alif.unit_value == "ا"
    # Alif can be either consonant or vowel, depends on context
    assert alif.letter_type in (LetterType.CONSONANT, LetterType.LONG_VOWEL)


def test_letter_from_form_hamza():
    """LetterAlgebra.from_form should handle hamza."""
    hamza = LetterAlgebra.from_form("ء")

    assert hamza.unit_value == "ء"
    assert hamza.letter_type == LetterType.CONSONANT


def test_letter_algebra_no_meaning():
    """LetterAlgebra must NEVER have semantic meaning.

    **Critical test**: Letter is NOT meaning.
    """
    letter = LetterAlgebra.from_form("ك")

    # Must not have meaning field
    assert not hasattr(letter, "meaning")
    assert not hasattr(letter, "madlul")
    assert not hasattr(letter, "semantic_value")

    # Validation should pass
    validate_no_meaning_field(letter)


def test_letter_algebra_has_boundaries():
    """LetterAlgebra must define boundaries."""
    letter = LetterAlgebra.from_form("ك")

    assert "is_from_root" in letter.boundaries
    assert "is_from_affix" in letter.boundaries
    assert "is_semantic_particle" in letter.boundaries


def test_letter_algebra_has_residuals():
    """LetterAlgebra should start with residuals."""
    letter = LetterAlgebra.from_form("ك")

    # Initial construction has unresolved aspects
    assert isinstance(letter.residuals, list)


# ===========================================================================
# Layer 2: Harakah Algebra
# ===========================================================================


def test_harakah_from_form_fatha():
    """HarakahAlgebra.from_form should recognize fatha."""
    harakah = HarakahAlgebra.from_form("َ")

    assert harakah.unit_value == "َ"
    assert harakah.harakah_type == HarakahType.FATHA


def test_harakah_from_form_kasra():
    """HarakahAlgebra.from_form should recognize kasra."""
    harakah = HarakahAlgebra.from_form("ِ")

    assert harakah.unit_value == "ِ"
    assert harakah.harakah_type == HarakahType.KASRA


def test_harakah_from_form_damma():
    """HarakahAlgebra.from_form should recognize damma."""
    harakah = HarakahAlgebra.from_form("ُ")

    assert harakah.unit_value == "ُ"
    assert harakah.harakah_type == HarakahType.DAMMA


def test_harakah_from_form_sukun():
    """HarakahAlgebra.from_form should recognize sukun."""
    harakah = HarakahAlgebra.from_form("ْ")

    assert harakah.unit_value == "ْ"
    assert harakah.harakah_type == HarakahType.SUKUN


def test_harakah_role_unresolved_initially():
    """HarakahAlgebra role must be UNRESOLVED initially.

    **Critical**: Harakah FORM ≠ Harakah ROLE.
    Role is context-dependent (binaa/iraab/pattern).
    """
    harakah = HarakahAlgebra.from_form("َ")

    # Role starts UNRESOLVED
    assert harakah.role == HarakahRole.UNRESOLVED

    # Form is known
    assert harakah.harakah_type == HarakahType.FATHA


def test_harakah_algebra_no_meaning():
    """HarakahAlgebra must NEVER have semantic meaning.

    **Critical test**: Harakah is NOT meaning.
    Harakah is NOT i'rāb judgment.
    """
    harakah = HarakahAlgebra.from_form("َ")

    # Must not have meaning field
    assert not hasattr(harakah, "meaning")
    assert not hasattr(harakah, "hukm")
    assert not hasattr(harakah, "iraab_judgment")

    # Validation should pass
    validate_no_meaning_field(harakah)


def test_harakah_algebra_has_boundaries():
    """HarakahAlgebra must define boundaries."""
    harakah = HarakahAlgebra.from_form("َ")

    assert "is_binaa" in harakah.boundaries
    assert "is_iraab" in harakah.boundaries
    assert "is_pattern_vowel" in harakah.boundaries


# ===========================================================================
# Layer 3: Atom Algebra
# ===========================================================================


def test_atom_algebra_construction():
    """AtomAlgebra should bind letter + harakah."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")

    atom = AtomAlgebra(letter=letter, harakah=harakah)

    assert atom.letter == letter
    assert atom.harakah == harakah
    assert atom.unit_type == LayerType.ATOM


def test_atom_algebra_unit_value():
    """AtomAlgebra unit_value should combine letter + harakah."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")

    atom = AtomAlgebra(letter=letter, harakah=harakah)

    assert atom.unit_value == "كَ"


def test_atom_algebra_no_meaning():
    """AtomAlgebra must NEVER have semantic meaning.

    **Critical test**: Atom is binding, NOT meaning generation.
    """
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")
    atom = AtomAlgebra(letter=letter, harakah=harakah)

    # Must not have meaning field
    assert not hasattr(atom, "meaning")
    assert not hasattr(atom, "madlul")

    # Validation should pass
    validate_no_meaning_field(atom)


def test_atom_algebra_preserves_rank():
    """AtomAlgebra rank should be min of letter and harakah."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")

    atom = AtomAlgebra(letter=letter, harakah=harakah)

    # Rank should be conservative
    assert atom.rank == min(letter.rank, harakah.rank)


# ===========================================================================
# Layer 4: Syllable Algebra
# ===========================================================================


def test_syllable_algebra_construction():
    """SyllableAlgebra should construct from atom sequence."""
    letter_k = LetterAlgebra.from_form("ك")
    harakah_a = HarakahAlgebra.from_form("َ")
    atom_ka = AtomAlgebra(letter=letter_k, harakah=harakah_a)

    syllable = SyllableAlgebra(atoms=[atom_ka])

    assert len(syllable.atoms) == 1
    assert syllable.atoms[0] == atom_ka
    assert syllable.syllable_type == SyllableType.CV


def test_syllable_algebra_unit_value():
    """SyllableAlgebra unit_value should concatenate atoms."""
    letter_k = LetterAlgebra.from_form("ك")
    harakah_a = HarakahAlgebra.from_form("َ")
    atom_ka = AtomAlgebra(letter=letter_k, harakah=harakah_a)

    letter_t = LetterAlgebra.from_form("ت")
    harakah_a2 = HarakahAlgebra.from_form("َ")
    atom_ta = AtomAlgebra(letter=letter_t, harakah=harakah_a2)

    syllable = SyllableAlgebra(atoms=[atom_ka, atom_ta])

    assert syllable.unit_value == "كَتَ"


def test_syllable_algebra_no_meaning():
    """SyllableAlgebra must NEVER have semantic meaning."""
    letter_k = LetterAlgebra.from_form("ك")
    harakah_a = HarakahAlgebra.from_form("َ")
    atom_ka = AtomAlgebra(letter=letter_k, harakah=harakah_a)

    syllable = SyllableAlgebra(atoms=[atom_ka])

    validate_no_meaning_field(syllable)


# ===========================================================================
# Layer 6: Root Candidate Algebra
# ===========================================================================


def test_root_candidate_construction():
    """RootCandidateAlgebra should construct from root letters."""
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))

    assert root.consonants == ("ك", "ت", "ب")
    assert root.root_type == RootType.TRILATERAL


def test_root_candidate_unit_value():
    """RootCandidateAlgebra unit_value should be root letters joined."""
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))

    # unit_value is space-separated
    assert root.unit_value == "ك ت ب"


def test_root_candidate_no_meaning():
    """RootCandidateAlgebra must NEVER have semantic meaning.

    **Critical test**: Root is NOT meaning.
    Root does NOT directly produce maṣdar.
    """
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))

    # Must not have meaning field
    assert not hasattr(root, "meaning")
    assert not hasattr(root, "masdar")
    assert not hasattr(root, "direct_meaning")

    # Validation should pass
    validate_no_meaning_field(root)


def test_root_candidate_starts_unverified():
    """RootCandidateAlgebra should start as candidate (not certified)."""
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))

    # Starts as CANDIDATE rank
    assert root.rank == Rank.CANDIDATE


def test_root_candidate_quadrilateral():
    """RootCandidateAlgebra should detect quadrilateral roots."""
    root = RootCandidateAlgebra(consonants=("د", "ح", "ر", "ج"))

    assert root.root_type == RootType.QUADRILATERAL


# ===========================================================================
# Layer 8: Pattern Template Algebra
# ===========================================================================


def test_pattern_template_construction():
    """PatternTemplateAlgebra should construct from pattern form."""
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    assert pattern.pattern_form == "فَعَلَ"
    assert pattern.slot_count == 3


def test_pattern_template_no_meaning():
    """PatternTemplateAlgebra must NEVER have semantic meaning.

    **Critical test**: Pattern is NOT meaning.
    Pattern does NOT guarantee fā'iliyyah or maf'ūliyyah.
    """
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    # Must not have meaning field
    assert not hasattr(pattern, "meaning")
    assert not hasattr(pattern, "faaliyyah")
    assert not hasattr(pattern, "mafuuliyyah")
    assert not hasattr(pattern, "certainty")

    # Validation should pass
    validate_no_meaning_field(pattern)


# ===========================================================================
# Layer 9: Built Form Algebra
# ===========================================================================


def test_built_form_construction():
    """BuiltFormAlgebra should bind root ⊗ pattern."""
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")

    form = BuiltFormAlgebra(
        root=root,
        pattern=pattern,
        surface_form="كَتَبَ",
    )

    assert form.root == root
    assert form.pattern == pattern
    assert form.surface_form == "كَتَبَ"


def test_built_form_no_meaning():
    """BuiltFormAlgebra must NEVER have semantic meaning.

    **Critical test**: BuiltForm is formal structure, NOT meaning.
    """
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")
    form = BuiltFormAlgebra(root=root, pattern=pattern, surface_form="كَتَبَ")

    # Must not have meaning field
    assert not hasattr(form, "meaning")
    assert not hasattr(form, "madlul")

    # Validation should pass
    validate_no_meaning_field(form)


# ===========================================================================
# Layer 10: Word Candidate Algebra
# ===========================================================================


def test_word_candidate_construction():
    """WordCandidateAlgebra should construct with usage status."""
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")
    form = BuiltFormAlgebra(root=root, pattern=pattern, surface_form="كَتَبَ")

    word = WordCandidateAlgebra(
        form=form,
        is_attested=True,
        usage_status="مُستعمَل",
    )

    assert word.form == form
    assert word.is_attested
    assert word.usage_status == "مُستعمَل"


def test_word_candidate_no_meaning():
    """WordCandidateAlgebra must NEVER have semantic meaning.

    **Critical test**: Even at word level, lafẓī layer does NOT produce meaning.
    Meaning comes from external semantic layer.
    """
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))
    pattern = PatternTemplateAlgebra(pattern_form="فَعَلَ")
    form = BuiltFormAlgebra(root=root, pattern=pattern, surface_form="كَتَبَ")
    word = WordCandidateAlgebra(form=form, is_attested=True)

    # Must not have meaning field
    assert not hasattr(word, "meaning")
    assert not hasattr(word, "madlul")
    assert not hasattr(word, "semantic_value")

    # Validation should pass
    validate_no_meaning_field(word)


# ===========================================================================
# Critical Negative Tests (MUST FAIL)
# ===========================================================================


def test_cannot_add_meaning_to_letter():
    """Adding meaning field to letter must be rejected by validation."""

    # Try to create a fake letter with meaning
    class FakeLetterWithMeaning:
        unit_value = "ك"
        meaning = "كتابة"  # FORBIDDEN!

    fake = FakeLetterWithMeaning()

    with pytest.raises(ValueError, match="Forbidden semantic field"):
        validate_no_meaning_field(fake)


def test_cannot_add_iraab_judgment_to_harakah():
    """Adding i'rāb judgment to harakah must be rejected."""

    class FakeHarakahWithIraab:
        unit_value = "َ"
        hukm = "فاعل مرفوع"  # FORBIDDEN!

    fake = FakeHarakahWithIraab()

    with pytest.raises(ValueError, match="Forbidden semantic field"):
        validate_no_meaning_field(fake)


def test_cannot_add_masdar_to_root():
    """Adding maṣdar directly to root must be rejected."""

    class FakeRootWithMasdar:
        root_letters = ("ك", "ت", "ب")
        madlul = "الكتابة"  # FORBIDDEN!

    fake = FakeRootWithMasdar()

    with pytest.raises(ValueError, match="Forbidden semantic field"):
        validate_no_meaning_field(fake)


def test_cannot_add_faaliyyah_certainty_to_pattern():
    """Adding fā'iliyyah certainty to pattern must be rejected."""

    class FakePatternWithCertainty:
        pattern_form = "فَاعِل"
        ifadah = "فاعلية مؤكدة"  # FORBIDDEN!

    fake = FakePatternWithCertainty()

    with pytest.raises(ValueError, match="Forbidden semantic field"):
        validate_no_meaning_field(fake)
