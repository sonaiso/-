"""
Tests for D_lugha Witness Store

Tests linguistic attestation with explicit ranks.

Critical Theorems:
- Theorem 3: D_form ⊄ D_lugha (pattern ≠ attestation)
- Qiyas ≠ Sama (analogy ≠ hearing)
"""

import pytest
from dal_core.witness_store import (
    WitnessRecord,
    LexicalType,
    WITNESS_STORE,
    lookup_witness,
    is_attested,
    get_attestation_rank,
    get_witness_type
)
from dal_core.ranks import LughaRank


class TestWitnessStore:
    """Test witness store structure"""

    def test_witness_store_exists(self):
        """Witness store is populated"""
        assert len(WITNESS_STORE) > 0

    def test_witness_store_has_kataba(self):
        """كَتَبَ is attested"""
        assert "كَتَبَ" in WITNESS_STORE

    def test_witness_store_has_kitaab(self):
        """كِتَابٌ is attested"""
        assert "كِتَابٌ" in WITNESS_STORE

    def test_witness_record_has_rank(self):
        """All witness records have explicit rank"""
        for form, record in WITNESS_STORE.items():
            assert isinstance(record.rank, LughaRank)
            assert record.rank != LughaRank.ZERO  # All attested forms have rank > ZERO


class TestWeightNotAttestation:
    """Theorem 3: Pattern/weight alone is not attestation"""

    def test_weight_not_attestation(self):
        """Valid pattern without witness is not attested"""
        # This form matches pattern فَعَلَ but is not in witness store
        fake_form = "سَطَرَبَ"

        assert not is_attested(fake_form)
        assert lookup_witness(fake_form) is None
        assert get_attestation_rank(fake_form) == LughaRank.ZERO

    def test_form_only_does_not_close_lugha(self):
        """FORM rank is insufficient for lugha closure"""
        # Unattested form gets ZERO rank (not even FORM)
        fake_form = "غَرِيبٌ"

        rank = get_attestation_rank(fake_form)

        # Not attested → ZERO rank
        assert rank == LughaRank.ZERO

        # ZERO < SAMA, AHAD, TAWATUR
        assert rank < LughaRank.SAMA
        assert rank < LughaRank.AHAD
        assert rank < LughaRank.TAWATUR


class TestRankDistinction:
    """Test rank hierarchy and distinction"""

    def test_qiyas_rank_is_not_sama(self):
        """Qiyas rank < Sama rank"""
        assert LughaRank.QIYAS < LughaRank.SAMA
        assert LughaRank.QIYAS.value < LughaRank.SAMA.value

    def test_ahad_attestation_closes_with_ahad_rank(self):
        """Form with AHAD witness gets AHAD rank"""
        # مَكْتَبٌ is attested as AHAD
        record = lookup_witness("مَكْتَبٌ")

        assert record is not None
        assert record.rank == LughaRank.AHAD

    def test_tawatur_attestation_closes_with_tawatur_rank(self):
        """Form with TAWATUR witness gets TAWATUR rank"""
        # كَتَبَ is attested as TAWATUR
        record = lookup_witness("كَتَبَ")

        assert record is not None
        assert record.rank == LughaRank.TAWATUR

    def test_tawatur_higher_than_ahad(self):
        """TAWATUR rank > AHAD rank"""
        assert LughaRank.TAWATUR > LughaRank.AHAD
        assert LughaRank.TAWATUR.value > LughaRank.AHAD.value


class TestWitnessLookup:
    """Test witness lookup functions"""

    def test_unknown_witness_blocks_certificate(self):
        """Unknown form returns ZERO rank"""
        unknown_form = "ذَهَبِيَّةٌ"

        rank = get_attestation_rank(unknown_form)

        # ZERO rank should block certificate
        assert rank == LughaRank.ZERO

    def test_lookup_witness_returns_record(self):
        """lookup_witness returns WitnessRecord for attested forms"""
        record = lookup_witness("كِتَابٌ")

        assert record is not None
        assert isinstance(record, WitnessRecord)
        assert record.form == "كِتَابٌ"

    def test_lookup_witness_returns_none_for_unattested(self):
        """lookup_witness returns None for unattested forms"""
        record = lookup_witness("غَرِيبٌ")

        assert record is None

    def test_is_attested_true_for_witnessed(self):
        """is_attested returns True for witnessed forms"""
        assert is_attested("كَتَبَ") is True
        assert is_attested("كِتَابٌ") is True

    def test_is_attested_false_for_unattested(self):
        """is_attested returns False for unattested forms"""
        assert is_attested("غَرِيبٌ") is False
        assert is_attested("سَطَرَبَ") is False


class TestWitnessType:
    """Test type classification from witnesses"""

    def test_get_witness_type_for_verb(self):
        """Verb witnesses return FIIL type"""
        verb_type = get_witness_type("كَتَبَ")

        assert verb_type == LexicalType.FIIL

    def test_get_witness_type_for_noun(self):
        """Noun witnesses return ISM type"""
        noun_type = get_witness_type("كِتَابٌ")

        assert noun_type == LexicalType.ISM

    def test_get_witness_type_for_particle(self):
        """Particle witnesses return HARF type"""
        particle_type = get_witness_type("مِنْ")

        assert particle_type == LexicalType.HARF

    def test_get_witness_type_none_for_unattested(self):
        """Unattested forms return None type"""
        unknown_type = get_witness_type("غَرِيبٌ")

        assert unknown_type is None


class TestWitnessProvenance:
    """Test witness source and provenance"""

    def test_witness_has_source(self):
        """All witnesses have explicit source"""
        for form, record in WITNESS_STORE.items():
            assert record.source
            assert len(record.source) > 0

    def test_witness_has_form_and_normalized(self):
        """All witnesses have both vocalized and normalized forms"""
        for form, record in WITNESS_STORE.items():
            assert record.form
            assert record.normalized_form
            assert len(record.form) > 0
            assert len(record.normalized_form) > 0


class TestResidualPreservation:
    """Test that witness store preserves residuals pattern"""

    def test_residuals_preserved_from_d_form_to_d_lugha(self):
        """
        When looking up witness, previous residuals must be preserved.
        This test verifies the pattern (actual preservation happens in pipeline).
        """
        # This is a pattern test - the actual preservation is in pipeline.py
        # Here we just verify witness lookup doesn't interfere with residuals

        record = lookup_witness("كَتَبَ")

        # Witness record itself doesn't have residuals
        # Residuals are managed by pipeline
        assert record is not None
        assert not hasattr(record, 'residuals')  # Witness doesn't carry residuals


class TestSeedCoverage:
    """Test seed witness store coverage"""

    def test_has_verb_witnesses(self):
        """Store contains verb witnesses"""
        verb_count = sum(1 for r in WITNESS_STORE.values() if r.type == LexicalType.FIIL)
        assert verb_count >= 3  # At least 3 verb forms

    def test_has_noun_witnesses(self):
        """Store contains noun witnesses"""
        noun_count = sum(1 for r in WITNESS_STORE.values() if r.type == LexicalType.ISM)
        assert noun_count >= 5  # At least 5 noun forms

    def test_has_particle_witnesses(self):
        """Store contains particle witnesses"""
        particle_count = sum(1 for r in WITNESS_STORE.values() if r.type == LexicalType.HARF)
        assert particle_count >= 2  # At least 2 particles

    def test_has_tawatur_witnesses(self):
        """Store contains TAWATUR witnesses"""
        tawatur_count = sum(1 for r in WITNESS_STORE.values() if r.rank == LughaRank.TAWATUR)
        assert tawatur_count >= 10  # At least 10 mass-transmitted forms

    def test_has_ahad_witnesses(self):
        """Store contains AHAD witnesses"""
        ahad_count = sum(1 for r in WITNESS_STORE.values() if r.rank == LughaRank.AHAD)
        assert ahad_count >= 1  # At least 1 singular transmission
