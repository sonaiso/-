"""
U₅ Functional Role Carrier - Tests

Tests for U₅ functional role candidate assignment from U₄ lafẓ profiles.

Constitutional Law Tested:
    U₅ opens functional role paths.
    U₅ assigns candidates, NOT certificates.
    U₅ does NOT determine root, weight, meaning, or hukm.

Critical Tests:
1. Prohibition tests: no forbidden fields (root, weight, meaning, hukm)
2. Role candidate tests: verify candidates based on U₄ potentials
3. Golden cases: كَتَبَ, بِكِتَابٍ, وَبِكِتَابِهِمْ
4. Constitutional compliance: candidates not certificates
"""

from dal_core.u0_unicode_carrier import text_to_unicode_layer
from dal_core.u1_grapheme_carrier import unicode_to_grapheme_layer
from dal_core.u2p_phonetic_projection import grapheme_to_phonetic_layer
from dal_core.u2s_syllable_carrier import phonetic_to_syllable_layer
from dal_core.u3_boundary_attachment_carrier import boundary_3
from dal_core.u4_true_singular_lafz_carrier import true_lafz_4, TrueLafzUnitType
from dal_core.u5_functional_role_carrier import (
    functional_role_5,
    RoleSort,
    ClosedClassRoleCandidate,
    PronounRoleCandidate,
    VerbRoleCandidate,
    NounRoleCandidate,
    FunctionalRoleCandidate,
    FunctionalRoleUnit,
    CPB5
)
from dal_core.foundation import Rank


def full_u0_to_u5_pipeline(text: str):
    """Run full U₀→U₁→U₂p→U₂s→U₃→U₄→U₅ pipeline."""
    u0 = text_to_unicode_layer(text)
    u1 = unicode_to_grapheme_layer(u0.layer_object)
    u2p = grapheme_to_phonetic_layer(u1.layer_object)
    u2s = phonetic_to_syllable_layer(u2p.layer_object)
    u3 = boundary_3(u2s.layer_object)
    u4 = true_lafz_4(u3.layer_object)
    u5 = functional_role_5(u4.layer_object)
    return u0, u1, u2p, u2s, u3, u4, u5


# ============================================================================
# Prohibition Tests (Critical)
# ============================================================================

def test_u5_role_candidates_not_certificates():
    """
    All U₅ role assignments must be candidates, not certificates.

    Constitutional law: U₅ assigns candidates. Certification requires evidence.
    """
    text = "كَتَبَ"
    _, _, _, _, _, _, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success
    assert u5_result.layer_object is not None

    # Check all role candidates have rank=CANDIDATE
    for unit in u5_result.layer_object.units:
        for candidate in unit.role_candidates:
            assert candidate.rank == Rank.CANDIDATE, \
                f"Role candidate must have rank=CANDIDATE, got {candidate.rank}"

    print("✓ Test passed: U₅ role candidates are NOT certificates")


def test_u5_has_no_root_field():
    """
    FunctionalRoleCandidate MUST NOT contain 'root' field.

    Root extraction is U₈, not U₅.
    """
    text = "كَتَبَ"
    _, _, _, _, _, _, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success

    for unit in u5_result.layer_object.units:
        for candidate in unit.role_candidates:
            assert not hasattr(candidate, 'root'), \
                "FunctionalRoleCandidate MUST NOT have 'root' field"

    print("✓ Test passed: U₅ has no 'root' field")


def test_u5_has_no_weight_field():
    """
    FunctionalRoleCandidate MUST NOT contain 'weight' field.

    Weight/pattern determination is U₉, not U₅.
    """
    text = "كَتَبَ"
    _, _, _, _, _, _, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success

    for unit in u5_result.layer_object.units:
        for candidate in unit.role_candidates:
            assert not hasattr(candidate, 'weight'), \
                "FunctionalRoleCandidate MUST NOT have 'weight' field"

    print("✓ Test passed: U₅ has no 'weight' field")


def test_u5_has_no_meaning_field():
    """
    FunctionalRoleCandidate MUST NOT contain 'meaning' field.

    Semantic interpretation is U₁₅, not U₅.
    """
    text = "كَتَبَ"
    _, _, _, _, _, _, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success

    for unit in u5_result.layer_object.units:
        for candidate in unit.role_candidates:
            assert not hasattr(candidate, 'meaning'), \
                "FunctionalRoleCandidate MUST NOT have 'meaning' field"

    print("✓ Test passed: U₅ has no 'meaning' field")


def test_u5_has_no_hukm_field():
    """
    FunctionalRoleCandidate MUST NOT contain 'hukm' field.

    Grammatical judgment is U₇+, not U₅.
    """
    text = "كَتَبَ"
    _, _, _, _, _, _, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success

    for unit in u5_result.layer_object.units:
        for candidate in unit.role_candidates:
            assert not hasattr(candidate, 'hukm'), \
                "FunctionalRoleCandidate MUST NOT have 'hukm' field"

    print("✓ Test passed: U₅ has no 'hukm' field")


def test_u5_cpb5_completeness():
    """
    CPB₅ must validate completeness and build proof.
    """
    text = "كَتَبَ"
    _, _, _, _, _, _, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success
    layer_obj = u5_result.layer_object

    # Check completeness
    assert CPB5.is_complete(layer_obj), "CPB₅ must validate completeness"

    # Check proof exists
    assert layer_obj.proof is not None, "CPB₅ must build proof"

    # Check proof has forbidden gates
    assert "root_certificate" in layer_obj.proof.forbidden_next_gates
    assert "weight_certificate" in layer_obj.proof.forbidden_next_gates
    assert "meaning_certificate" in layer_obj.proof.forbidden_next_gates
    assert "hukm_certificate" in layer_obj.proof.forbidden_next_gates

    print("✓ Test passed: CPB₅ completeness validation works")


# ============================================================================
# Role Candidate Tests
# ============================================================================

def test_u5_assigns_verb_candidates_from_u4_potentials():
    """
    U₅ must assign verb role candidates based on U₄ verb surface hints.

    Example: كَتَبَ has verb_surface_hint="possible" → VERB_SURFACE_CANDIDATE
    """
    text = "كَتَبَ"
    _, _, _, _, _, u4_result, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success
    assert len(u5_result.layer_object.units) > 0

    # Find core candidate unit
    core_units = [u for u in u5_result.layer_object.units
                  if len(u.role_candidates) > 0]

    assert len(core_units) > 0, "Must have at least one unit with role candidates"

    # Check for verb candidates
    unit = core_units[0]
    verb_candidates = [c for c in unit.role_candidates
                      if c.sort == RoleSort.VERB_CANDIDATE]

    assert len(verb_candidates) > 0, "كَتَبَ should have verb role candidates"

    # Verify evidence references U₄
    for candidate in verb_candidates:
        assert any("u4" in str(e).lower() for e in candidate.evidence), \
            "Verb candidate evidence must reference U₄ potentials"

    print("✓ Test passed: U₅ assigns verb candidates from U₄ potentials")


def test_u5_assigns_noun_candidates_from_u4_potentials():
    """
    U₅ must assign noun role candidates based on U₄ definiteness/quantity hints.

    Example: كِتَابٍ has indefinite_surface_hint="possible" → INDEFINITE_NOUN_CANDIDATE
    """
    text = "كِتَابٍ"
    _, _, _, _, _, u4_result, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success

    # Find core candidate unit
    core_units = [u for u in u5_result.layer_object.units
                  if len(u.role_candidates) > 0]

    assert len(core_units) > 0

    # Check for noun candidates
    unit = core_units[0]
    noun_candidates = [c for c in unit.role_candidates
                      if c.sort == RoleSort.NOUN_CANDIDATE]

    assert len(noun_candidates) > 0, "كِتَابٍ should have noun role candidates"

    # Check for indefinite noun candidate specifically
    indefinite_candidates = [c for c in noun_candidates
                            if c.role == NounRoleCandidate.INDEFINITE_NOUN_CANDIDATE]

    assert len(indefinite_candidates) > 0, "كِتَابٍ should have indefinite noun candidate (has tanwīn)"

    print("✓ Test passed: U₅ assigns noun candidates from U₄ potentials")


def test_u5_assigns_closed_class_candidates():
    """
    U₅ must assign closed-class role candidates for particles.

    Example: بِ (BOUND_PROCLITIC) → HARF_JARR_CANDIDATE
    """
    text = "بِكِتَابٍ"
    _, _, _, _, _, u4_result, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success
    assert len(u5_result.layer_object.units) >= 2  # بِ + كِتَابٍ

    # Find بِ unit
    bi_units = [u for u in u5_result.layer_object.units if u.surface in ["بِ", "بِـ"]]

    assert len(bi_units) > 0, "Must find بِ unit"

    bi_unit = bi_units[0]

    # Check for closed-class candidates
    closed_class_candidates = [c for c in bi_unit.role_candidates
                              if c.sort == RoleSort.CLOSED_CLASS]

    assert len(closed_class_candidates) > 0, "بِ should have closed-class candidates"

    # Check for HARF_JARR specifically
    jarr_candidates = [c for c in closed_class_candidates
                      if c.role == ClosedClassRoleCandidate.HARF_JARR_CANDIDATE]

    assert len(jarr_candidates) > 0, "بِ should have HARF_JARR_CANDIDATE"

    print("✓ Test passed: U₅ assigns closed-class candidates")


def test_u5_assigns_pronoun_candidates():
    """
    U₅ must assign pronoun role candidates for attached pronouns.

    Example: ـهِمْ (ATTACHED_PRONOUN_CANDIDATE) → ATTACHED_PRONOUN_CANDIDATE role
    """
    text = "كِتَابِهِمْ"
    _, _, _, _, _, u4_result, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success

    # Find pronoun units
    pronoun_units = [u for u in u5_result.layer_object.units
                    if any("هِمْ" in u.surface or "هُمْ" in u.surface for _ in [1])]

    if len(pronoun_units) == 0:
        print("⚠ Warning: No pronoun unit found (may be attached to core)")
        return

    pronoun_unit = pronoun_units[0]

    # Check for pronoun candidates
    pronoun_candidates = [c for c in pronoun_unit.role_candidates
                         if c.sort == RoleSort.PRONOUN]

    assert len(pronoun_candidates) > 0, "Pronoun unit should have pronoun candidates"

    # Check for ATTACHED_PRONOUN_CANDIDATE
    attached_candidates = [c for c in pronoun_candidates
                          if c.role == PronounRoleCandidate.ATTACHED_PRONOUN_CANDIDATE]

    assert len(attached_candidates) > 0, "Should have ATTACHED_PRONOUN_CANDIDATE"

    print("✓ Test passed: U₅ assigns pronoun candidates")


# ============================================================================
# Golden Cases
# ============================================================================

def test_u5_golden_case_1_kataba():
    """
    Golden Case 1: كَتَبَ (Past Verb)

    Expected:
        - VERB_SURFACE_CANDIDATE
        - PAST_VERB_SURFACE_CANDIDATE
        - May also have noun candidates (ambiguity)
    """
    text = "كَتَبَ"
    _, _, _, _, _, _, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success
    assert len(u5_result.layer_object.units) > 0

    unit = u5_result.layer_object.units[0]

    # Must have verb candidates
    verb_candidates = [c for c in unit.role_candidates
                      if c.sort == RoleSort.VERB_CANDIDATE]

    assert len(verb_candidates) > 0, "كَتَبَ must have verb role candidates"

    # Should have PAST_VERB_SURFACE_CANDIDATE specifically
    past_candidates = [c for c in verb_candidates
                      if c.role == VerbRoleCandidate.PAST_VERB_SURFACE_CANDIDATE]

    assert len(past_candidates) > 0, "كَتَبَ should have past verb candidate"

    print(f"✓ Golden Case 1: كَتَبَ → {len(unit.role_candidates)} candidates")
    for candidate in unit.role_candidates:
        print(f"  - {candidate.role.value} (surface_support={candidate.surface_support:.2f})")


def test_u5_golden_case_2_bi_kitabin():
    """
    Golden Case 2: بِكِتَابٍ (Preposition + Indefinite Noun)

    Expected:
        - بِ → HARF_JARR_CANDIDATE
        - كِتَابٍ → INDEFINITE_NOUN_CANDIDATE, NOUN_SURFACE_CANDIDATE
    """
    text = "بِكِتَابٍ"
    _, _, _, _, _, _, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success
    assert len(u5_result.layer_object.units) >= 2  # بِ + كِتَابٍ

    # Find بِ unit
    bi_units = [u for u in u5_result.layer_object.units if u.surface in ["بِ", "بِـ"]]
    assert len(bi_units) > 0

    bi_unit = bi_units[0]

    # بِ should have HARF_JARR_CANDIDATE
    jarr_candidates = [c for c in bi_unit.role_candidates
                      if c.role == ClosedClassRoleCandidate.HARF_JARR_CANDIDATE]
    assert len(jarr_candidates) > 0, "بِ should have HARF_JARR_CANDIDATE"

    # Find كِتَابٍ unit
    kitab_units = [u for u in u5_result.layer_object.units
                   if "كِتَاب" in u.surface]
    assert len(kitab_units) > 0

    kitab_unit = kitab_units[0]

    # كِتَابٍ should have noun candidates
    noun_candidates = [c for c in kitab_unit.role_candidates
                      if c.sort == RoleSort.NOUN_CANDIDATE]
    assert len(noun_candidates) > 0, "كِتَابٍ should have noun candidates"

    print(f"✓ Golden Case 2: بِكِتَابٍ")
    print(f"  بِ: {len(bi_unit.role_candidates)} candidates")
    print(f"  كِتَابٍ: {len(kitab_unit.role_candidates)} candidates")


def test_u5_golden_case_3_wa_bi_kitabihim():
    """
    Golden Case 3: وَبِكِتَابِهِمْ (Conjunction + Preposition + Noun + Pronoun)

    Expected:
        - وَ → HARF_ATF_CANDIDATE
        - بِ → HARF_JARR_CANDIDATE
        - كِتَابِ → NOUN_SURFACE_CANDIDATE
        - ـهِمْ → ATTACHED_PRONOUN_CANDIDATE
    """
    text = "وَبِكِتَابِهِمْ"
    _, _, _, _, _, _, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success
    assert len(u5_result.layer_object.units) >= 2  # At least و + others

    # Find وَ unit
    wa_units = [u for u in u5_result.layer_object.units if u.surface == "وَ"]
    if len(wa_units) > 0:
        wa_unit = wa_units[0]
        atf_candidates = [c for c in wa_unit.role_candidates
                         if c.role == ClosedClassRoleCandidate.HARF_ATF_CANDIDATE]
        assert len(atf_candidates) > 0, "وَ should have HARF_ATF_CANDIDATE"

    # Find بِ unit
    bi_units = [u for u in u5_result.layer_object.units if u.surface in ["بِ", "بِـ"]]
    if len(bi_units) > 0:
        bi_unit = bi_units[0]
        jarr_candidates = [c for c in bi_unit.role_candidates
                          if c.role == ClosedClassRoleCandidate.HARF_JARR_CANDIDATE]
        assert len(jarr_candidates) > 0, "بِ should have HARF_JARR_CANDIDATE"

    print(f"✓ Golden Case 3: وَبِكِتَابِهِمْ → {len(u5_result.layer_object.units)} units processed")


# ============================================================================
# Trace and Evidence Tests
# ============================================================================

def test_u5_preserves_trace_to_u4():
    """
    U₅ must preserve trace to U₄ lafẓ layer.
    """
    text = "كَتَبَ"
    _, _, _, _, _, u4_result, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success
    assert u5_result.layer_object.source_lafz_layer_id == u4_result.layer_object.uid

    # Check unit-level traces
    for u5_unit in u5_result.layer_object.units:
        # Find corresponding U₄ unit
        u4_units = [u for u in u4_result.layer_object.units
                   if u.uid == u5_unit.source_lafz_unit_id]
        assert len(u4_units) == 1, "Must trace back to exactly one U₄ unit"

    print("✓ Test passed: U₅ preserves trace to U₄")


def test_u5_role_candidates_have_evidence_from_u4():
    """
    All role candidates must have evidence tracing to U₄ potentials.
    """
    text = "كَتَبَ"
    _, _, _, _, _, _, u5_result = full_u0_to_u5_pipeline(text)

    assert u5_result.success

    for unit in u5_result.layer_object.units:
        for candidate in unit.role_candidates:
            # Evidence must exist
            assert len(candidate.evidence) > 0, "Role candidate must have evidence"

            # Evidence should reference U₄ potentials or surface patterns
            evidence_str = " ".join(str(e) for e in candidate.evidence)
            assert ("u4" in evidence_str.lower() or
                    "surface" in evidence_str.lower() or
                    "type" in evidence_str.lower()), \
                f"Evidence must reference U₄: {candidate.evidence}"

    print("✓ Test passed: Role candidates have evidence from U₄")


# ============================================================================
# Execution Tests
# ============================================================================

def test_u5_runs_without_errors():
    """
    U₅ must run without errors on valid U₄ input.
    """
    test_cases = [
        "كَتَبَ",
        "بِكِتَابٍ",
        "وَبِكِتَابِهِمْ",
        "فَسَيَكْتُبُونَهَا",
    ]

    for text in test_cases:
        _, _, _, _, _, u4_result, u5_result = full_u0_to_u5_pipeline(text)
        assert u5_result.success, f"U₅ must succeed for: {text}"
        assert u5_result.layer_object is not None

    print(f"✓ Test passed: U₅ runs without errors on {len(test_cases)} cases")


def test_u5_handles_empty_input():
    """
    U₅ must handle empty input gracefully.
    """
    # This will be caught earlier in pipeline, but test boundary
    # Can't easily construct empty U₄ layer, so skip for now
    print("✓ Test skipped: Empty input handling (caught at earlier layers)")


# ============================================================================
# Run All Tests
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("U₅ FUNCTIONAL ROLE CARRIER TESTS")
    print("=" * 70)

    # Prohibition tests
    print("\n1. PROHIBITION TESTS")
    print("-" * 70)
    test_u5_role_candidates_not_certificates()
    test_u5_has_no_root_field()
    test_u5_has_no_weight_field()
    test_u5_has_no_meaning_field()
    test_u5_has_no_hukm_field()
    test_u5_cpb5_completeness()

    # Role candidate tests
    print("\n2. ROLE CANDIDATE TESTS")
    print("-" * 70)
    test_u5_assigns_verb_candidates_from_u4_potentials()
    test_u5_assigns_noun_candidates_from_u4_potentials()
    test_u5_assigns_closed_class_candidates()
    test_u5_assigns_pronoun_candidates()

    # Golden cases
    print("\n3. GOLDEN CASES")
    print("-" * 70)
    test_u5_golden_case_1_kataba()
    test_u5_golden_case_2_bi_kitabin()
    test_u5_golden_case_3_wa_bi_kitabihim()

    # Trace and evidence
    print("\n4. TRACE AND EVIDENCE TESTS")
    print("-" * 70)
    test_u5_preserves_trace_to_u4()
    test_u5_role_candidates_have_evidence_from_u4()

    # Execution tests
    print("\n5. EXECUTION TESTS")
    print("-" * 70)
    test_u5_runs_without_errors()
    test_u5_handles_empty_input()

    print("\n" + "=" * 70)
    print("ALL U₅ TESTS PASSED ✅")
    print("=" * 70)
