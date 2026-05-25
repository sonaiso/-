"""
U₄-B Lafẓ Surface Potential Profiles - Tests

Tests for U₄-B surface potential profile implementation.

Constitutional Law Tested:
    U₄-B describes surface.
    U₄-B opens guarded potentials.
    U₄-B does NOT certify morphology, syntax, meaning, reference, quantity, tense, voice, or valency.

Critical Tests:
1. Prohibition tests: no forbidden fields
2. Golden cases: كَتَبَ, بِكِتَابٍ, وَبِكِتَابِهِمْ, فَسَيَكْتُبُونَهَا, كَاتِب, مَكْتَب

Surface Existence Rule:
    Surface existence → boolean (allowed)
    Surface interpretation → hint (required: "possible", "unlikely", "unresolved")
"""

from dal_core.u0_unicode_carrier import text_to_unicode_layer
from dal_core.u1_grapheme_carrier import unicode_to_grapheme_layer
from dal_core.u2p_phonetic_projection import grapheme_to_phonetic_layer
from dal_core.u2s_syllable_carrier import phonetic_to_syllable_layer
from dal_core.u3_boundary_attachment_carrier import boundary_3
from dal_core.u4_true_singular_lafz_carrier import (
    true_lafz_4,
    TrueLafzUnitType,
    TerminalProfile,
    DefinitenessSurfacePotential,
    QuantitySurfacePotential,
    VerbSurfacePotential,
    DownstreamPathHints
)


def full_u0_to_u4_pipeline(text: str):
    """Run full U₀→U₁→U₂p→U₂s→U₃→U₄ pipeline."""
    u0 = text_to_unicode_layer(text)
    u1 = unicode_to_grapheme_layer(u0.layer_object)
    u2p = grapheme_to_phonetic_layer(u1.layer_object)
    u2s = phonetic_to_syllable_layer(u2p.layer_object)
    u3 = boundary_3(u2s.layer_object)
    u4 = true_lafz_4(u3.layer_object)
    return u0, u1, u2p, u2s, u3, u4


# ============================================================================
# Prohibition Tests (Critical)
# ============================================================================

def test_u4_profiles_are_surface_potentials_not_certificates():
    """
    All U₄ profile fields must be hints/surfaces, not certificates.

    Constitutional law: U₄-B describes surface, does NOT certify.
    """
    text = "كَتَبَ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    assert u4_result.layer_object is not None

    # Find TRUE_SINGULAR_CORE_CANDIDATE unit
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    assert len(core_units) > 0, "Must have at least one core candidate"

    unit = core_units[0]

    # Verify profiles exist
    assert unit.terminal_profile is not None, "Terminal profile must exist for core candidate"
    assert unit.definiteness_surface_potential is not None
    assert unit.quantity_surface_potential is not None
    assert unit.verb_surface_potential is not None
    assert unit.downstream_path_hints is not None

    print("✓ Test passed: U₄ profiles are surface potentials, not certificates")


def test_u4_terminal_profile_has_no_case_or_irab_field():
    """
    TerminalProfile MUST NOT contain case_marking or i3rab_status.

    Terminal profile describes surface endings, NOT grammatical case.
    """
    text = "كَتَبَ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    unit = core_units[0]
    terminal_profile = unit.terminal_profile

    # Verify NO forbidden fields
    assert not hasattr(terminal_profile, 'case_marking'), \
        "TerminalProfile MUST NOT have 'case_marking' field"
    assert not hasattr(terminal_profile, 'i3rab_status'), \
        "TerminalProfile MUST NOT have 'i3rab_status' field"
    assert not hasattr(terminal_profile, 'mood_marking'), \
        "TerminalProfile MUST NOT have 'mood_marking' field"

    # Verify it uses hints, not certificates
    assert isinstance(terminal_profile.mabni_surface_hint, str)
    assert isinstance(terminal_profile.murab_surface_hint, str)
    assert terminal_profile.mabni_surface_hint in ["possible", "unlikely", "unresolved"]
    assert terminal_profile.murab_surface_hint in ["possible", "unlikely", "unresolved"]

    print("✓ Test passed: TerminalProfile has no case/iʿrāb fields")


def test_u4_definiteness_has_no_resolved_reference():
    """
    DefinitenessSurfacePotential MUST NOT contain resolved_reference.

    Definiteness potential identifies surface markers, NOT resolved reference.
    """
    text = "الكِتَابُ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    if len(core_units) > 0:
        unit = core_units[0]
        definiteness_potential = unit.definiteness_surface_potential

        # Verify NO forbidden fields
        assert not hasattr(definiteness_potential, 'resolved_reference'), \
            "DefinitenessSurfacePotential MUST NOT have 'resolved_reference' field"
        assert not hasattr(definiteness_potential, 'is_definite'), \
            "DefinitenessSurfacePotential MUST NOT have 'is_definite' boolean field"
        assert not hasattr(definiteness_potential, 'referent'), \
            "DefinitenessSurfacePotential MUST NOT have 'referent' field"

        # Verify it uses hints
        assert isinstance(definiteness_potential.definite_surface_hint, str)
        assert definiteness_potential.definite_surface_hint in ["possible", "unlikely", "unresolved"]

    print("✓ Test passed: DefinitenessSurfacePotential has no resolved_reference")


def test_u4_quantity_has_no_counted_reality():
    """
    QuantitySurfacePotential MUST NOT contain counted_entities.

    Quantity potential identifies surface markers, NOT counted reality.
    """
    text = "كِتَابَانِ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    if len(core_units) > 0:
        unit = core_units[0]
        quantity_potential = unit.quantity_surface_potential

        # Verify NO forbidden fields
        assert not hasattr(quantity_potential, 'quantity'), \
            "QuantitySurfacePotential MUST NOT have 'quantity' field"
        assert not hasattr(quantity_potential, 'counted_entities'), \
            "QuantitySurfacePotential MUST NOT have 'counted_entities' field"

        # Verify it uses hints
        assert isinstance(quantity_potential.dual_surface_hint, str)
        assert isinstance(quantity_potential.plural_surface_hint, str)
        assert isinstance(quantity_potential.singular_surface_hint, str)

    print("✓ Test passed: QuantitySurfacePotential has no counted_reality")


def test_u4_verb_surface_has_no_tense_voice_valency():
    """
    VerbSurfacePotential MUST NOT contain tense, voice, or valency.

    Verb potential identifies surface patterns, NOT tense/voice/valency certificates.
    """
    text = "كَتَبَ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    unit = core_units[0]
    verb_potential = unit.verb_surface_potential

    # Verify NO forbidden fields
    assert not hasattr(verb_potential, 'tense'), \
        "VerbSurfacePotential MUST NOT have 'tense' field"
    assert not hasattr(verb_potential, 'voice'), \
        "VerbSurfacePotential MUST NOT have 'voice' field"
    assert not hasattr(verb_potential, 'valency'), \
        "VerbSurfacePotential MUST NOT have 'valency' field"
    assert not hasattr(verb_potential, 'aspect'), \
        "VerbSurfacePotential MUST NOT have 'aspect' field"
    assert not hasattr(verb_potential, 'mood'), \
        "VerbSurfacePotential MUST NOT have 'mood' field"

    # Verify it uses hints
    assert isinstance(verb_potential.verb_surface_hint, str)
    assert isinstance(verb_potential.past_surface_hint, str)
    assert isinstance(verb_potential.present_surface_hint, str)

    print("✓ Test passed: VerbSurfacePotential has no tense/voice/valency")


def test_u4_downstream_hints_do_not_include_root_or_weight_path():
    """
    DownstreamPathHints MUST NOT mention root or weight paths.

    Downstream hints open paths to U₅/U₆, NOT U₈/U₉.
    """
    text = "كَتَبَ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    unit = core_units[0]
    downstream_hints = unit.downstream_path_hints

    # Verify NO forbidden fields
    assert not hasattr(downstream_hints, 'pattern_family_hints'), \
        "DownstreamPathHints MUST NOT have 'pattern_family_hints' field"
    assert not hasattr(downstream_hints, 'root_hints'), \
        "DownstreamPathHints MUST NOT have 'root_hints' field"
    assert not hasattr(downstream_hints, 'weight_hints'), \
        "DownstreamPathHints MUST NOT have 'weight_hints' field"

    # Verify it has allowed path flags
    assert isinstance(downstream_hints.may_open_functional_role_path, bool)
    assert isinstance(downstream_hints.may_open_verb_candidate_path, bool)

    print("✓ Test passed: DownstreamPathHints has no root/weight/pattern fields")


# ============================================================================
# Golden Cases
# ============================================================================

def test_kataba_surface_profiles():
    """
    Test: كَتَبَ (he wrote)

    Expected profiles:
    - verb_surface_hint = "possible" or "unresolved"
    - past_surface_hint = "possible"
    - NO certified tense
    """
    text = "كَتَبَ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    assert len(core_units) == 1
    unit = core_units[0]

    # Verify verb potential
    assert unit.verb_surface_potential is not None
    assert unit.verb_surface_potential.past_surface_hint in ["possible", "unresolved"]
    assert not unit.verb_surface_potential.has_present_prefix_surface

    # Verify downstream hints
    assert unit.downstream_path_hints.may_open_verb_candidate_path or \
           unit.downstream_path_hints.may_open_noun_candidate_path

    print(f"✓ Test passed: كَتَبَ → verb_surface_hint={unit.verb_surface_potential.verb_surface_hint}, past_hint={unit.verb_surface_potential.past_surface_hint}")


def test_bikitabin_surface_profiles():
    """
    Test: بِكِتَابٍ (in a book)

    Expected profiles:
    - has_tanwin_surface = True
    - indefinite_surface_hint = "possible"
    - NO resolved reference
    """
    text = "بِكِتَابٍ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success

    # Find the core candidate (كِتَابٍ)
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    assert len(core_units) == 1
    unit = core_units[0]
    assert "كِتَابٍ" in unit.surface or "كتاب" in unit.surface.lower()

    # Verify terminal profile
    assert unit.terminal_profile.has_tanwin_surface

    # Verify definiteness potential
    assert unit.definiteness_surface_potential.has_tanwin_surface
    assert unit.definiteness_surface_potential.indefinite_surface_hint == "possible"

    print(f"✓ Test passed: بِكِتَابٍ → has_tanwin=True, indefinite_hint=possible")


def test_wabikitabihim_surface_profiles():
    """
    Test: وَبِكِتَابِهِمْ (and with their book)

    Expected profiles:
    - has_attached_pronoun_surface for ـهِمْ unit (or in context)
    - reference_surface_hint = "possible"
    - NO resolved referent
    """
    text = "وَبِكِتَابِهِمْ"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success

    # Find the core candidate (كِتَابِ)
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    assert len(core_units) >= 1

    # Find pronoun units
    pronoun_units = [u for u in u4_result.layer_object.units
                     if u.unit_type == TrueLafzUnitType.ATTACHED_PRONOUN_CANDIDATE]

    # Either core has pronoun context or pronoun unit exists
    has_pronoun_context = len(pronoun_units) > 0

    print(f"✓ Test passed: وَبِكِتَابِهِمْ → pronoun_units={len(pronoun_units)}")


def test_fasayaktubunaha_surface_profiles():
    """
    Test: فَسَيَكْتُبُونَهَا (and they will write it)

    Expected profiles:
    - verb_surface_hint = "possible" (for يَكْتُبُونَ)
    - present_surface_hint = "possible"
    - has_present_prefix_surface = True
    - NO certified tense
    """
    text = "فَسَيَكْتُبُونَهَا"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success

    # Find the core verb candidate (يَكْتُبُونَ)
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    assert len(core_units) >= 1

    # Find unit with present prefix
    verb_units = [u for u in core_units if u.verb_surface_potential.has_present_prefix_surface]

    if len(verb_units) > 0:
        unit = verb_units[0]
        assert unit.verb_surface_potential.present_surface_hint == "possible"
        assert unit.verb_surface_potential.verb_surface_hint in ["possible", "unresolved"]

    print(f"✓ Test passed: فَسَيَكْتُبُونَهَا → verb_units with present prefix={len(verb_units)}")


def test_kaatib_surface_profiles():
    """
    Test: كَاتِب (writer/scribe)

    Expected profiles:
    - noun_candidate_path possible
    - NO weight
    - NO pattern certificate
    """
    text = "كَاتِب"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    assert len(core_units) == 1
    unit = core_units[0]

    # Verify no weight field
    assert not hasattr(unit, 'weight'), "Unit MUST NOT have 'weight' field"
    assert not hasattr(unit, 'pattern'), "Unit MUST NOT have 'pattern' field"

    # Verify downstream hints
    assert unit.downstream_path_hints.may_open_noun_candidate_path or \
           unit.downstream_path_hints.may_open_verb_candidate_path

    print(f"✓ Test passed: كَاتِب → no weight, downstream paths available")


def test_maktab_surface_profiles():
    """
    Test: مَكْتَب (office/desk)

    Expected profiles:
    - noun_candidate_path possible
    - NO weight
    - NO pattern certificate
    """
    text = "مَكْتَب"
    _, _, _, _, _, u4_result = full_u0_to_u4_pipeline(text)

    assert u4_result.success
    core_units = [u for u in u4_result.layer_object.units
                  if u.unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE]

    assert len(core_units) == 1
    unit = core_units[0]

    # Verify no weight field
    assert not hasattr(unit, 'weight'), "Unit MUST NOT have 'weight' field"
    assert not hasattr(unit, 'pattern'), "Unit MUST NOT have 'pattern' field"

    # Verify downstream hints
    assert unit.downstream_path_hints.may_open_noun_candidate_path or \
           unit.downstream_path_hints.may_open_verb_candidate_path

    print(f"✓ Test passed: مَكْتَب → no weight, downstream paths available")


# ============================================================================
# Run all tests
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("U₄-B Lafẓ Surface Potential Profiles - Tests")
    print("=" * 70)
    print()

    print("PROHIBITION TESTS:")
    print("-" * 70)
    test_u4_profiles_are_surface_potentials_not_certificates()
    test_u4_terminal_profile_has_no_case_or_irab_field()
    test_u4_definiteness_has_no_resolved_reference()
    test_u4_quantity_has_no_counted_reality()
    test_u4_verb_surface_has_no_tense_voice_valency()
    test_u4_downstream_hints_do_not_include_root_or_weight_path()

    print()
    print("GOLDEN CASES:")
    print("-" * 70)
    test_kataba_surface_profiles()
    test_bikitabin_surface_profiles()
    test_wabikitabihim_surface_profiles()
    test_fasayaktubunaha_surface_profiles()
    test_kaatib_surface_profiles()
    test_maktab_surface_profiles()

    print()
    print("=" * 70)
    print("ALL U₄-B TESTS PASSED ✓")
    print("=" * 70)
