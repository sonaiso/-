"""Tests for ``dal_core.binaa_judge`` (PR-C).

Covers every rule R0..R8 plus the anti-hallucination guard: no syllable
information is permitted as input.
"""

import pytest

from dal_core.binaa_judge import (
    BinaaJudgeInput,
    BinaaJudgmentResult,
    judge_binaa,
)
from dal_core.d_type import DalType
from dal_core.mufrad_axes import BinaaJudgment, BinaaSubtype
from dal_core.residuals import ResidualSeverity, ResidualType
from dal_core.type_ids import VerbTypeID


def _judge(form, dal_type, verb_type_id=None):
    return judge_binaa(
        BinaaJudgeInput(
            dal_type=dal_type, surface_form=form, verb_type_id=verb_type_id
        )
    )


# ---------------------------------------------------------------------------
# R0 — unresolved guards
# ---------------------------------------------------------------------------


class TestR0Unresolved:
    def test_ambiguous_dal_type_unresolved(self):
        r = _judge("x", DalType.AMBIGUOUS)
        assert r.judgment == BinaaJudgment.UNRESOLVED
        assert r.subtype is None
        assert any(
            res.type == ResidualType.MUFRAD_MABNI_MURAB_UNRESOLVED
            and res.severity == ResidualSeverity.BLOCKER
            for res in r.residuals
        )

    def test_verb_without_tense_unresolved(self):
        r = _judge("xxx", DalType.FIIL, verb_type_id=None)
        assert r.judgment == BinaaJudgment.UNRESOLVED
        assert r.residuals


# ---------------------------------------------------------------------------
# R1 — harf is always MABNI
# ---------------------------------------------------------------------------


class TestR1Harf:
    @pytest.mark.parametrize("form", ["مِنْ", "فِي", "إِنَّ", "هَلْ"])
    def test_all_particles_mabni(self, form):
        r = _judge(form, DalType.HARF)
        assert r.judgment == BinaaJudgment.MABNI
        assert r.subtype == BinaaSubtype.INVARIANT_PROPER
        assert r.residuals == ()


# ---------------------------------------------------------------------------
# R2..R6 — verbs
# ---------------------------------------------------------------------------


class TestVerbs:
    def test_madi_is_mabni_fath(self):
        r = _judge("ضَرَبَ", DalType.FIIL, verb_type_id=VerbTypeID.FIIL_MADI)
        assert r.judgment == BinaaJudgment.MABNI
        assert r.subtype == BinaaSubtype.BINAA_FATH

    def test_amr_is_mabni_sukun(self):
        r = _judge("اضْرِبْ", DalType.FIIL, verb_type_id=VerbTypeID.FIIL_AMR)
        assert r.judgment == BinaaJudgment.MABNI
        assert r.subtype == BinaaSubtype.BINAA_SUKUN

    def test_mudari_default_is_muerab(self):
        r = _judge("يَضْرِبُ", DalType.FIIL, verb_type_id=VerbTypeID.FIIL_MUDARI)
        assert r.judgment == BinaaJudgment.MUERAB
        assert r.subtype is None

    def test_mudari_with_nun_niswa_is_mabni_sukun(self):
        # يَضْرِبْنَ — مضارع متصل بنون النسوة.
        r = _judge("يَضْرِبْنَ", DalType.FIIL, verb_type_id=VerbTypeID.FIIL_MUDARI)
        assert r.judgment == BinaaJudgment.MABNI
        assert r.subtype == BinaaSubtype.BINAA_SUKUN

    def test_mudari_with_heavy_tawkid_is_mabni_fath(self):
        # لَيَضْرِبَنَّ — نون التوكيد الثقيلة.
        r = _judge(
            "لَيَضْرِبَنَّ", DalType.FIIL, verb_type_id=VerbTypeID.FIIL_MUDARI
        )
        assert r.judgment == BinaaJudgment.MABNI
        assert r.subtype == BinaaSubtype.BINAA_FATH

    def test_mudari_with_light_tawkid_is_mabni_fath(self):
        # ليضربَنْ — نون التوكيد الخفيفة.
        r = _judge("لَيَضْرِبَنْ", DalType.FIIL, verb_type_id=VerbTypeID.FIIL_MUDARI)
        assert r.judgment == BinaaJudgment.MABNI

    def test_mudari_five_verbs_not_misclassified_as_niswa(self):
        # يَضْرِبُونَ ends in نَ but is the RAF' nun of the five verbs.
        r = _judge("يَضْرِبُونَ", DalType.FIIL, verb_type_id=VerbTypeID.FIIL_MUDARI)
        assert r.judgment == BinaaJudgment.MUERAB

        r2 = _judge("يَضْرِبَانِ", DalType.FIIL, verb_type_id=VerbTypeID.FIIL_MUDARI)
        # ends with ان not نَ, so default MUERAB
        assert r2.judgment == BinaaJudgment.MUERAB


# ---------------------------------------------------------------------------
# R7..R8 — nouns
# ---------------------------------------------------------------------------


class TestNouns:
    def test_demonstrative_mabni(self):
        r = _judge("هَذَا", DalType.ISM)
        assert r.judgment == BinaaJudgment.MABNI
        assert r.subtype == BinaaSubtype.INVARIANT_PROPER

    def test_relative_plural_mabni(self):
        r = _judge("الَّذِينَ", DalType.ISM)
        assert r.judgment == BinaaJudgment.MABNI
        assert r.subtype == BinaaSubtype.BINAA_FATH

    def test_interrogative_mabni(self):
        r = _judge("كَيْفَ", DalType.ISM)
        assert r.judgment == BinaaJudgment.MABNI
        assert r.subtype == BinaaSubtype.BINAA_FATH

    def test_compound_number_mabni(self):
        r = _judge("خَمْسَةَ عَشَرَ", DalType.ISM)
        assert r.judgment == BinaaJudgment.MABNI

    def test_common_noun_default_muerab(self):
        r = _judge("كَاتِبٌ", DalType.ISM)
        assert r.judgment == BinaaJudgment.MUERAB
        assert r.subtype is None

    def test_concrete_noun_default_muerab(self):
        r = _judge("رَجُلٌ", DalType.ISM)
        assert r.judgment == BinaaJudgment.MUERAB


# ---------------------------------------------------------------------------
# Anti-hallucination guard
# ---------------------------------------------------------------------------


class TestAntiHallucinationGuard:
    def test_judge_input_has_no_syllable_fields(self):
        # Defensive: ensure no syllable_* field is present on the input.
        fields = set(BinaaJudgeInput.__dataclass_fields__.keys())
        forbidden = {
            "syllable_count",
            "syllable_shapes",
            "syllables",
            "cv_shape",
        }
        assert forbidden.isdisjoint(fields), (
            f"BinaaJudgeInput must not expose syllable fields, got {fields & forbidden}"
        )

    def test_equal_syllable_count_words_get_different_judgments(self):
        # هَذَا and رَجُلٌ have the same syllable count (≈3 short syllables);
        # the judge must produce different judgments based on identity +
        # registry, not on syllables. This is the anti-hallucination
        # canary test: if anyone ever wires syllable_count into the judge,
        # this test will fail.
        r_hadha = _judge("هَذَا", DalType.ISM)
        r_rajul = _judge("رَجُلٌ", DalType.ISM)
        assert r_hadha.judgment == BinaaJudgment.MABNI
        assert r_rajul.judgment == BinaaJudgment.MUERAB
        assert r_hadha.judgment != r_rajul.judgment


# ---------------------------------------------------------------------------
# Result invariants
# ---------------------------------------------------------------------------


class TestResultInvariants:
    @pytest.mark.parametrize(
        "form,dt,vid",
        [
            ("ضَرَبَ", DalType.FIIL, VerbTypeID.FIIL_MADI),
            ("اضْرِبْ", DalType.FIIL, VerbTypeID.FIIL_AMR),
            ("يَضْرِبُ", DalType.FIIL, VerbTypeID.FIIL_MUDARI),
            ("كَاتِبٌ", DalType.ISM, None),
            ("هَذَا", DalType.ISM, None),
            ("مِنْ", DalType.HARF, None),
        ],
    )
    def test_resolved_results_have_no_blocker_residuals(self, form, dt, vid):
        r = _judge(form, dt, verb_type_id=vid)
        assert r.judgment in (BinaaJudgment.MABNI, BinaaJudgment.MUERAB)
        assert not any(
            res.severity == ResidualSeverity.BLOCKER for res in r.residuals
        )

    def test_evidence_source_tagged_with_rule_id(self):
        r = _judge("ضَرَبَ", DalType.FIIL, verb_type_id=VerbTypeID.FIIL_MADI)
        assert r.evidence.source.startswith("binaa_judge.R")
