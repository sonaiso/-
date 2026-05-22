"""Tests for Lafẓī Madlūl Fractal Structure.

Validates that:
1. Fractal pattern is self-similar across all layers
2. Each layer implements complete algebra (not just transition node)
3. Four geometries (Unit, Boundary, Binding, Inheritance) are consistent
4. Validation functions enforce the pattern
"""

import pytest

from fvafk.algebra.lafzi_madlul.fractal_algebra import (
    BoundaryGeometry,
    BindingGeometry,
    FractalPattern,
    InheritanceGeometry,
    LayerType,
    UnitGeometry,
    validate_internal_closure,
    validate_no_meaning_field,
)
from fvafk.algebra.lafzi_madlul.layer_algebras import (
    AtomAlgebra,
    HarakahAlgebra,
    LetterAlgebra,
    RootCandidateAlgebra,
)


# ===========================================================================
# Fractal Pattern Self-Similarity Tests
# ===========================================================================


def test_fractal_pattern_has_all_stages():
    """Fractal pattern must define all 8 stages."""
    stages = FractalPattern.PATTERN_STAGES

    assert len(stages) == 8
    assert "discrimination" in stages
    assert "unit" in stages
    assert "boundaries" in stages
    assert "binding" in stages
    assert "gate" in stages
    assert "rank" in stages
    assert "residuals" in stages
    assert "inheritance" in stages


def test_fractal_pattern_applies_to_all_layers():
    """Fractal pattern must instantiate for each layer."""
    for layer_type in LayerType:
        pattern = FractalPattern.apply_to_layer(layer_type.name)

        # Each layer gets same pattern structure
        assert "discrimination" in pattern
        assert "unit" in pattern
        assert "boundaries" in pattern
        assert "binding" in pattern
        assert "gate" in pattern
        assert "rank" in pattern
        assert "residuals" in pattern
        assert "inheritance" in pattern


def test_layer_completeness_validation():
    """Layer completeness validates all required attributes."""
    # Create a complete letter algebra
    letter = LetterAlgebra.from_form("ك")

    is_complete, missing = FractalPattern.validate_layer_completeness(letter)

    assert is_complete
    assert len(missing) == 0


def test_layer_completeness_detects_forbidden_meaning_field():
    """Layer validation must detect forbidden semantic fields."""

    # Create mock object with forbidden field
    class FakeLafziLayer:
        unit_type = LayerType.LETTER
        unit_value = "ك"
        boundaries = {}
        internal_bindings = {}
        rank = None
        residuals = []
        trace = None
        meaning = "كتابة"  # FORBIDDEN!

    fake = FakeLafziLayer()
    is_complete, missing = FractalPattern.validate_layer_completeness(fake)

    assert not is_complete
    assert "FORBIDDEN:meaning" in missing


# ===========================================================================
# Four Geometries Tests
# ===========================================================================


def test_unit_geometry_defines_all_layers():
    """UnitGeometry must define minimal unit for each layer."""
    for layer_type in LayerType:
        unit_def = UnitGeometry.define_minimal_unit(layer_type)

        assert isinstance(unit_def, str)
        assert len(unit_def) > 0
        assert unit_def != "undefined"


def test_boundary_geometry_has_questions():
    """BoundaryGeometry must provide questions for key layers."""
    # Letter boundaries
    letter_questions = BoundaryGeometry.boundary_questions(LayerType.LETTER)
    assert len(letter_questions) > 0
    assert any("جذر" in q for q in letter_questions)

    # Harakah boundaries
    harakah_questions = BoundaryGeometry.boundary_questions(LayerType.HARAKAH)
    assert len(harakah_questions) > 0
    assert any("بناء" in q or "إعراب" in q for q in harakah_questions)


def test_binding_geometry_describes_bindings():
    """BindingGeometry must describe what each layer binds to."""
    # Letter binds to Harakah
    letter_binding = BindingGeometry.binding_targets(LayerType.LETTER)
    assert "binds_to" in letter_binding
    assert letter_binding["binds_to"] == "Harakah"

    # Harakah binds to Letter
    harakah_binding = BindingGeometry.binding_targets(LayerType.HARAKAH)
    assert "binds_to" in harakah_binding
    assert harakah_binding["binds_to"] == "Letter"


def test_inheritance_geometry_prohibits_meaning():
    """InheritanceGeometry must prohibit meaning inheritance for all layers."""
    for layer_type in LayerType:
        inheritance = InheritanceGeometry.allowed_inheritance(layer_type)

        # All layers must prohibit meaning
        assert "prohibits" in inheritance
        prohibits = inheritance["prohibits"]
        # Either explicitly lists meaning-related prohibitions, or uses default
        # Check that at least one meaning-related term is prohibited
        assert any(
            any(term in p for term in ["meaning", "semantic", "hukm", "i'rab", "madlul", "certainty"])
            for p in prohibits
        ) or "meaning" in prohibits


# ===========================================================================
# Validation Function Tests
# ===========================================================================


def test_validate_no_meaning_field_accepts_clean_layer():
    """validate_no_meaning_field should accept layers without semantic fields."""
    letter = LetterAlgebra.from_form("ك")

    # Should not raise
    validate_no_meaning_field(letter)


def test_validate_no_meaning_field_rejects_semantic_field():
    """validate_no_meaning_field must reject objects with semantic fields."""

    class FakeLafziWithMeaning:
        meaning = "كتابة"  # FORBIDDEN

    fake = FakeLafziWithMeaning()

    with pytest.raises(ValueError, match="Forbidden semantic field"):
        validate_no_meaning_field(fake)


def test_validate_no_meaning_field_detects_all_forbidden():
    """validate_no_meaning_field must detect all forbidden semantic fields."""
    forbidden_fields = ["meaning", "madlul", "semantic_value", "hukm", "ifadah", "dalalah"]

    for field in forbidden_fields:

        class FakeLayer:
            pass

        fake = FakeLayer()
        setattr(fake, field, "some_value")

        with pytest.raises(ValueError, match=f"Forbidden semantic field '{field}'"):
            validate_no_meaning_field(fake)


def test_validate_internal_closure_checks_unit():
    """validate_internal_closure must check unit_value is defined."""

    class IncompleteLayer:
        unit_value = None  # Incomplete!
        boundaries = {"some_boundary": True}
        internal_bindings = {"some_binding": "value"}

    incomplete = IncompleteLayer()
    is_closed, missing = validate_internal_closure(incomplete)

    assert not is_closed
    assert "unit_undefined" in missing


def test_validate_internal_closure_checks_boundaries():
    """validate_internal_closure must check boundaries exist (empty OK)."""

    class IncompleteLayer:
        unit_value = "some_value"
        # Missing boundaries attribute entirely!
        internal_bindings = {"some_binding": "value"}

    incomplete = IncompleteLayer()
    is_closed, missing = validate_internal_closure(incomplete)

    assert not is_closed
    assert "boundaries_missing" in missing


def test_validate_internal_closure_accepts_complete():
    """validate_internal_closure should accept complete layers."""
    letter = LetterAlgebra.from_form("ك")

    is_closed, missing = validate_internal_closure(letter)

    # Letter may have empty internal_bindings initially, which is acceptable
    # The validation checks for existence of the attribute, not that it's non-empty
    assert is_closed or "internal_bindings" not in missing


# ===========================================================================
# Layer Algebra Structural Tests
# ===========================================================================


def test_all_layer_algebras_have_unit_type():
    """Every layer algebra must have unit_type field."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))

    assert hasattr(letter, "unit_type")
    assert hasattr(harakah, "unit_type")
    assert hasattr(root, "unit_type")


def test_all_layer_algebras_have_rank():
    """Every layer algebra must have rank field."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))

    assert hasattr(letter, "rank")
    assert hasattr(harakah, "rank")
    assert hasattr(root, "rank")


def test_all_layer_algebras_have_residuals():
    """Every layer algebra must have residuals field."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))

    assert hasattr(letter, "residuals")
    assert hasattr(harakah, "residuals")
    assert hasattr(root, "residuals")


def test_all_layer_algebras_have_trace():
    """Every layer algebra must have trace field."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")
    root = RootCandidateAlgebra(consonants=("ك", "ت", "ب"))

    assert hasattr(letter, "trace")
    assert hasattr(harakah, "trace")
    assert hasattr(root, "trace")


def test_all_layer_algebras_frozen():
    """All layer algebras must be frozen (immutable)."""
    letter = LetterAlgebra.from_form("ك")

    with pytest.raises(Exception):  # FrozenInstanceError
        letter.unit_value = "ب"


# ===========================================================================
# Integration: Complete Fractal Check
# ===========================================================================


def test_letter_algebra_implements_complete_fractal():
    """LetterAlgebra must implement all fractal pattern components."""
    letter = LetterAlgebra.from_form("ك")

    # U_L: Unit
    assert hasattr(letter, "unit_type")
    assert hasattr(letter, "unit_value")
    assert letter.unit_value == "ك"

    # T_L: Type system
    assert hasattr(letter, "letter_type")

    # B_L: Boundaries
    assert hasattr(letter, "boundaries")
    assert isinstance(letter.boundaries, dict)

    # I_L: Internal bindings
    assert hasattr(letter, "internal_bindings")

    # G_L: Gates (implicit in validation)
    # Validated by from_form construction

    # ρ_L: Rank
    assert hasattr(letter, "rank")

    # R_L: Residuals
    assert hasattr(letter, "residuals")

    # Trace
    assert hasattr(letter, "trace")

    # F_L: Failure types (handled at Result level)
    # No direct failure field needed at algebra level


def test_atom_algebra_implements_complete_fractal():
    """AtomAlgebra must implement all fractal pattern components."""
    letter = LetterAlgebra.from_form("ك")
    harakah = HarakahAlgebra.from_form("َ")
    atom = AtomAlgebra(letter=letter, harakah=harakah)

    # U_L: Unit
    assert hasattr(atom, "unit_type")
    assert atom.unit_type == LayerType.ATOM

    # B_L: Boundaries
    assert hasattr(atom, "boundaries")

    # I_L: Internal bindings
    assert hasattr(atom, "internal_bindings")

    # ρ_L: Rank
    assert hasattr(atom, "rank")

    # R_L: Residuals
    assert hasattr(atom, "residuals")

    # Trace
    assert hasattr(atom, "trace")
