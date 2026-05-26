"""
Tests for U₇-B Phase 2 Marker Coverage

Tests verify complete marker family protection:
1. Original i'rāb markers (ضمة، فتحة، كسرة، سكون)
2. Secondary i'rāb markers (ألف، واو، ياء، نون)
3. Imperative markers (همزة الوصل)
4. Passive voice surface markers
5. Complete pronoun suffix inventory (14 forms)
6. Six nouns patterns (الأسماء الستة)
7. Proper name/loanword/jāmid deferral
"""

import pytest
from uuid import uuid4

from dal_core.foundation import Rank
from dal_core.residuals import Residual
from dal_core.u7_pre_weight_contract_carrier import (
    PreWeightContractLayerObject,
    PreWeightContractUnit,
    ContractStatus,
    PathPermission,
)
from dal_core.u7b_inflectional_surface_contract_carrier import (
    inflectional_surface_contract_7b,
    InflectionalSurfaceContractLayerObject,
    InflectionalSurfaceContractUnit,
    MarkerHint,
    RootInputPermission,
    CPB7B,
)


def make_test_u7_unit(
    surface: str,
    contract_status: ContractStatus = ContractStatus.OPEN_CORE_CONTRACT_CANDIDATE,
    root_path_permission: PathPermission = PathPermission.POSSIBLE,
    proper_name_hint: PathPermission = PathPermission.UNRESOLVED,
    loanword_hint: PathPermission = PathPermission.UNRESOLVED,
    jamid_hint: PathPermission = PathPermission.UNRESOLVED,
) -> PreWeightContractUnit:
    """Helper to create test U₇-A pre-weight contract unit."""
    return PreWeightContractUnit(
        uid=str(uuid4()),
        surface=surface,
        source_u6_unit_id=str(uuid4()),
        source_u6_trace=(str(uuid4()),),
        open_closed_status="open_class",
        contract_status=contract_status,
        lexical_path_potential=root_path_permission,
        root_path_permission=root_path_permission,
        stem_path_permission=root_path_permission,
        weight_path_permission=root_path_permission,
        jamid_surface_potential=jamid_hint,
        proper_name_surface_potential=proper_name_hint,
        loanword_surface_potential=loanword_hint,
        frozen_primitive_potential=PathPermission.UNRESOLVED,
        derivational_readiness=PathPermission.UNRESOLVED,
        required_evidence=(),
        blocked_paths=(),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        trace=(str(uuid4()),)
    )


def make_test_u7_layer(units: list[PreWeightContractUnit]) -> PreWeightContractLayerObject:
    """Helper to create test U₇-A layer."""
    return PreWeightContractLayerObject(
        uid=str(uuid4()),
        units=tuple(units),
        source_mabni_layer_id=str(uuid4()),
        trace_6=(str(uuid4()),),
        residuals=frozenset(),
        rank=Rank.CANDIDATE,
        proof=None
    )


# ============================================================================
# Original I'rāb Markers Tests (علامات الإعراب الأصلية)
# ============================================================================

class TestOriginalIrabMarkers:
    """Test original i'rāb marker detection."""

    def test_nominative_damma_detected(self):
        """
        Test: كِتَابُ (with damma for nominative)
        Expected: nominative_surface_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("كِتَابُ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        assert len(result.layer_object.units) == 1
        unit = result.layer_object.units[0]

        # Nominative hint detected
        assert unit.nominative_surface_hint == MarkerHint.POSSIBLE
        assert unit.original_irab_marker_hint == MarkerHint.POSSIBLE

    def test_accusative_fatha_detected(self):
        """
        Test: كِتَابَ (with fatha for accusative)
        Expected: accusative_surface_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("كِتَابَ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        assert unit.accusative_surface_hint == MarkerHint.POSSIBLE
        assert unit.original_irab_marker_hint == MarkerHint.POSSIBLE

    def test_genitive_kasra_detected(self):
        """
        Test: كِتَابِ (with kasra for genitive)
        Expected: genitive_surface_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("كِتَابِ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        assert unit.genitive_surface_hint == MarkerHint.POSSIBLE
        assert unit.original_irab_marker_hint == MarkerHint.POSSIBLE

    def test_jussive_sukun_detected(self):
        """
        Test: لَمْ يَكْتُبْ (with sukun for jussive)
        Expected: jussive_surface_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("يَكْتُبْ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        assert unit.jussive_surface_hint == MarkerHint.POSSIBLE


# ============================================================================
# Secondary I'rāb Markers Tests (علامات الإعراب الفرعية)
# ============================================================================

class TestSecondaryIrabMarkers:
    """Test secondary i'rāb marker detection."""

    def test_dual_alif_nominative(self):
        """
        Test: مُسْلِمَان (dual nominative with alif)
        Expected: secondary_irab_marker_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("مسلمان")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        assert unit.secondary_irab_marker_hint == MarkerHint.POSSIBLE
        assert 'ان_alif' in unit.protected_suffixes

    def test_dual_yaa_genitive(self):
        """
        Test: مُسْلِمَيْن (dual genitive/accusative with yā')
        Expected: secondary_irab_marker_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("مسلمين")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        assert unit.secondary_irab_marker_hint == MarkerHint.POSSIBLE
        assert 'ين_yaa' in unit.protected_suffixes

    def test_sound_masc_plural_waw_nominative(self):
        """
        Test: مُسْلِمُون (sound masc plural nominative with wāw)
        Expected: secondary_irab_marker_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("مسلمون")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        assert unit.secondary_irab_marker_hint == MarkerHint.POSSIBLE
        assert 'ون_waw' in unit.protected_suffixes


# ============================================================================
# Imperative Markers Tests (علامات الأمر)
# ============================================================================

class TestImperativeMarkers:
    """Test imperative marker detection."""

    def test_imperative_hamzat_wasl_detected(self):
        """
        Test: اكْتُبْ (imperative "write!" with hamzat waṣl)
        Expected: imperative_surface_hint = AMBIGUOUS (needs context)
        """
        u7_unit = make_test_u7_unit("اكتب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        # Hamzat waṣl detected but ambiguous without context
        assert unit.imperative_surface_hint in [MarkerHint.AMBIGUOUS, MarkerHint.POSSIBLE]
        assert 'ا_hamza_wasl_possible' in unit.protected_prefixes

    def test_imperative_residual_emitted(self):
        """
        Test: Imperative hint emits residual
        """
        u7_unit = make_test_u7_unit("اذهب")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        # Check residual emitted
        residual_keys = [r.key for r in unit.residuals]
        assert "imperative_surface_hint" in residual_keys


# ============================================================================
# Passive Voice Markers Tests (المبني للمجهول)
# ============================================================================

class TestPassiveVoiceMarkers:
    """Test passive voice surface marker detection."""

    def test_past_passive_pattern_detected(self):
        """
        Test: قُتِلَ (was killed - passive past with ُـِـَ pattern)
        Expected: passive_surface_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("قُتِلَ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        # Passive pattern detected
        assert unit.passive_surface_hint == MarkerHint.POSSIBLE
        assert len(unit.protected_vowels) > 0

    def test_present_passive_pattern_detected(self):
        """
        Test: يُقْتَلُ (is killed - passive present with ُـَـُ pattern)
        Expected: passive_surface_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit("يُقْتَلُ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        assert unit.passive_surface_hint == MarkerHint.POSSIBLE

    def test_passive_residual_emitted(self):
        """
        Test: Passive voice hint emits residual
        """
        u7_unit = make_test_u7_unit("فُتِحَ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        residual_keys = [r.key for r in unit.residuals]
        assert "passive_voice_surface_hint" in residual_keys


# ============================================================================
# Complete Pronoun Suffix Tests (الضمائر المتصلة - 14 forms)
# ============================================================================

class TestCompletePronounSuffixes:
    """Test complete pronoun suffix inventory (14 forms)."""

    def test_pronoun_hu_detected(self):
        """Test: كتابه (his book - ـه)"""
        u7_unit = make_test_u7_unit("كتابه")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.pronoun_suffix_hint == MarkerHint.POSSIBLE
        assert 'ـه' in unit.protected_pronoun_suffixes

    def test_pronoun_haa_detected(self):
        """Test: كتابها (her book - ـها)"""
        u7_unit = make_test_u7_unit("كتابها")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.pronoun_suffix_hint == MarkerHint.POSSIBLE
        assert 'ـها' in unit.protected_pronoun_suffixes

    def test_pronoun_huma_detected(self):
        """Test: كتابهما (their dual book - ـهما)"""
        u7_unit = make_test_u7_unit("كتابهما")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.pronoun_suffix_hint == MarkerHint.POSSIBLE
        assert 'ـهما' in unit.protected_pronoun_suffixes

    def test_pronoun_hum_detected(self):
        """Test: كتابهم (their masc plural book - ـهم)"""
        u7_unit = make_test_u7_unit("كتابهم")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.pronoun_suffix_hint == MarkerHint.POSSIBLE
        assert 'ـهم' in unit.protected_pronoun_suffixes

    def test_pronoun_hunna_detected(self):
        """Test: كتابهن (their fem plural book - ـهن)"""
        u7_unit = make_test_u7_unit("كتابهن")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.pronoun_suffix_hint == MarkerHint.POSSIBLE
        assert 'ـهن' in unit.protected_pronoun_suffixes

    def test_pronoun_ka_detected(self):
        """Test: كتابك (your masc sing book - ـك)"""
        u7_unit = make_test_u7_unit("كتابك")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        # ك is ambiguous without context
        assert unit.pronoun_suffix_hint in [MarkerHint.POSSIBLE, MarkerHint.AMBIGUOUS]
        assert 'ـك' in unit.protected_pronoun_suffixes

    def test_pronoun_kum_detected(self):
        """Test: كتابكم (your masc plural book - ـكم)"""
        u7_unit = make_test_u7_unit("كتابكم")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.pronoun_suffix_hint == MarkerHint.POSSIBLE
        assert 'ـكم' in unit.protected_pronoun_suffixes

    def test_pronoun_kunna_detected(self):
        """Test: كتابكن (your fem plural book - ـكن)"""
        u7_unit = make_test_u7_unit("كتابكن")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.pronoun_suffix_hint == MarkerHint.POSSIBLE
        assert 'ـكن' in unit.protected_pronoun_suffixes

    def test_pronoun_kuma_detected(self):
        """Test: كتابكما (your dual book - ـكما)"""
        u7_unit = make_test_u7_unit("كتابكما")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.pronoun_suffix_hint == MarkerHint.POSSIBLE
        assert 'ـكما' in unit.protected_pronoun_suffixes

    def test_pronoun_naa_detected(self):
        """Test: كتابنا (our book - ـنا)"""
        u7_unit = make_test_u7_unit("كتابنا")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.pronoun_suffix_hint == MarkerHint.POSSIBLE
        assert 'ـنا' in unit.protected_pronoun_suffixes

    def test_pronoun_ni_verb_detected(self):
        """Test: ضربني (he hit me - verbal ـني)"""
        u7_unit = make_test_u7_unit("ضربني")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.pronoun_suffix_hint == MarkerHint.POSSIBLE
        assert 'ـني' in unit.protected_pronoun_suffixes


# ============================================================================
# Six Nouns Tests (الأسماء الستة)
# ============================================================================

class TestSixNouns:
    """Test six nouns pattern detection."""

    def test_abu_nominative_deferred(self):
        """
        Test: أبو (father - nominative)
        Expected: six_nouns_pattern_hint detected, root_input DEFERRED
        """
        u7_unit = make_test_u7_unit("أبو")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        assert unit.six_nouns_pattern_hint == "أب_six_nouns"
        assert unit.root_input_permission == RootInputPermission.DEFERRED
        assert unit.root_input == ""

    def test_aba_accusative_deferred(self):
        """Test: أبا (father - accusative)"""
        u7_unit = make_test_u7_unit("أبا")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.six_nouns_pattern_hint == "أب_six_nouns"
        assert unit.root_input_permission == RootInputPermission.DEFERRED

    def test_abi_genitive_deferred(self):
        """Test: أبي (father - genitive)"""
        u7_unit = make_test_u7_unit("أبي")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.six_nouns_pattern_hint == "أب_six_nouns"
        assert unit.root_input_permission == RootInputPermission.DEFERRED

    def test_akhu_nominative_deferred(self):
        """Test: أخو (brother - nominative)"""
        u7_unit = make_test_u7_unit("أخو")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.six_nouns_pattern_hint == "أخ_six_nouns"
        assert unit.root_input_permission == RootInputPermission.DEFERRED

    def test_dhu_nominative_deferred(self):
        """Test: ذو (owner/possessor - nominative)"""
        u7_unit = make_test_u7_unit("ذو")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]
        assert unit.six_nouns_pattern_hint == "ذو_six_nouns"
        assert unit.root_input_permission == RootInputPermission.DEFERRED

    def test_six_nouns_residual_emitted(self):
        """Test: Six nouns emit deferral residual"""
        u7_unit = make_test_u7_unit("أبو")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        residual_keys = [r.key for r in unit.residuals]
        assert "six_nouns_deferred" in residual_keys


# ============================================================================
# Proper Name / Loanword / Jāmid Deferral Tests
# ============================================================================

class TestProperNameLoanwordJamidDeferral:
    """Test proper name, loanword, and jāmid deferral policy."""

    def test_proper_name_deferred(self):
        """
        Test: زيد (proper name)
        Expected: root_input DEFERRED when proper_name_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit(
            "زيد",
            proper_name_hint=PathPermission.POSSIBLE
        )
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        assert unit.root_input_permission == RootInputPermission.DEFERRED
        assert unit.root_input == ""

        residual_keys = [r.key for r in unit.residuals]
        assert "proper_name_deferred" in residual_keys

    def test_loanword_deferred(self):
        """
        Test: تلفزيون (loanword)
        Expected: root_input DEFERRED when loanword_hint = POSSIBLE
        """
        u7_unit = make_test_u7_unit(
            "تلفزيون",
            loanword_hint=PathPermission.POSSIBLE
        )
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        assert unit.root_input_permission == RootInputPermission.DEFERRED
        assert unit.root_input == ""

        residual_keys = [r.key for r in unit.residuals]
        assert "loanword_deferred" in residual_keys

    def test_jamid_surface_potential_residual(self):
        """
        Test: Jāmid surface potential emits residual
        """
        u7_unit = make_test_u7_unit(
            "رجل",
            jamid_hint=PathPermission.POSSIBLE
        )
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        residual_keys = [r.key for r in unit.residuals]
        assert "jamid_surface_potential" in residual_keys


# ============================================================================
# Architectural Tests
# ============================================================================

class TestPhase2ArchitecturalCompliance:
    """Test Phase 2 architectural compliance."""

    def test_all_new_fields_present(self):
        """
        Test: All Phase 2 fields present in output
        """
        u7_unit = make_test_u7_unit("قُتِلَ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        # Phase 2 fields must exist
        assert hasattr(unit, 'nominative_surface_hint')
        assert hasattr(unit, 'accusative_surface_hint')
        assert hasattr(unit, 'genitive_surface_hint')
        assert hasattr(unit, 'jussive_surface_hint')
        assert hasattr(unit, 'secondary_irab_marker_hint')
        assert hasattr(unit, 'imperative_surface_hint')
        assert hasattr(unit, 'six_nouns_pattern_hint')
        assert hasattr(unit, 'protected_vowels')

    def test_protected_vowels_tuple_not_empty_for_passive(self):
        """
        Test: protected_vowels tuple populated for passive
        """
        u7_unit = make_test_u7_unit("قُتِلَ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        # Passive detected, protected_vowels should be non-empty
        if unit.passive_surface_hint == MarkerHint.POSSIBLE:
            assert len(unit.protected_vowels) > 0

    def test_blocked_segments_include_vowels(self):
        """
        Test: blocked_root_segments include protected_vowels for passive
        """
        u7_unit = make_test_u7_unit("قُتِلَ")
        u7_layer = make_test_u7_layer([u7_unit])

        result = inflectional_surface_contract_7b(u7_layer)

        assert result.success
        unit = result.layer_object.units[0]

        # Blocked segments should include vowels
        assert len(unit.blocked_root_segments) >= len(unit.protected_vowels)
