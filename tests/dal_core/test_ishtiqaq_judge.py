"""Tests for ``dal_core.ishtiqaq_judge`` (PR-D)."""

import pytest

from dal_core.d_type import DalType
from dal_core.evidence import Evidence as _E
from dal_core.ishtiqaq_judge import (
    IshtiqaqJudgeInput,
    judge_ishtiqaq,
)
from dal_core.morph_features import RootCandidate, WaznCandidate
from dal_core.mufrad_axes import (
    IshtiqaqJudgment,
    JamidSubtype,
    MushtaqSubtype,
)
from dal_core.ranks import LughaRank
from dal_core.residuals import ResidualSeverity, ResidualType


# Convenience builders -----------------------------------------------------


def _wazn(pattern_class: str, wazn: str = "فاعل") -> WaznCandidate:
    return WaznCandidate(
        wazn=wazn,
        pattern_class=pattern_class,
        evidence=(),
        rank=LughaRank.QIYAS,
        confidence=1.0,
    )


def _root(letters=("ك", "ت", "ب")) -> RootCandidate:
    return RootCandidate(
        root=letters,
        root_type="trilateral",
        evidence=(),
        rank=LughaRank.QIYAS,
        confidence=1.0,
    )


def _judge(form, dt, *, wazns=(), roots=(), proper=False):
    return judge_ishtiqaq(
        IshtiqaqJudgeInput(
            dal_type=dt,
            surface_form=form,
            root_candidates=tuple(roots),
            wazn_candidates=tuple(wazns),
            is_proper_name=proper,
        )
    )


# ---------------------------------------------------------------------------
# R0 — unresolved
# ---------------------------------------------------------------------------


class TestR0:
    def test_ambiguous_type_unresolved(self):
        r = _judge("x", DalType.AMBIGUOUS)
        assert r.judgment == IshtiqaqJudgment.UNRESOLVED
        assert any(
            res.type == ResidualType.MUFRAD_JAMID_MUSHTAQ_UNRESOLVED
            for res in r.residuals
        )


# ---------------------------------------------------------------------------
# R1, R2 — non-applicable for harf / fiil
# ---------------------------------------------------------------------------


class TestNonApplicable:
    def test_harf_not_applicable(self):
        r = _judge("مِنْ", DalType.HARF)
        assert r.judgment == IshtiqaqJudgment.NOT_APPLICABLE
        assert r.subtype is None
        assert r.residuals == ()

    def test_fiil_not_applicable(self):
        r = _judge("ضَرَبَ", DalType.FIIL)
        assert r.judgment == IshtiqaqJudgment.NOT_APPLICABLE
        assert r.residuals == ()


# ---------------------------------------------------------------------------
# Mushtaq cases (R5)
# ---------------------------------------------------------------------------


class TestMushtaq:
    def test_active_participle(self):
        r = _judge("كَاتِبٌ", DalType.ISM, wazns=[_wazn("active_participle")])
        assert r.judgment == IshtiqaqJudgment.MUSHTAQ
        assert r.subtype == MushtaqSubtype.ISM_FAIL

    def test_passive_participle(self):
        r = _judge("مَكْتُوبٌ", DalType.ISM, wazns=[_wazn("passive_participle")])
        assert r.judgment == IshtiqaqJudgment.MUSHTAQ
        assert r.subtype == MushtaqSubtype.ISM_MAFUL

    def test_tafdil(self):
        r = _judge("أَفْضَلُ", DalType.ISM, wazns=[_wazn("ism_tafdil")])
        assert r.judgment == IshtiqaqJudgment.MUSHTAQ
        assert r.subtype == MushtaqSubtype.ISM_TAFDIL

    def test_ism_makan(self):
        r = _judge("مَكْتَبٌ", DalType.ISM, wazns=[_wazn("ism_makan")])
        assert r.judgment == IshtiqaqJudgment.MUSHTAQ
        assert r.subtype == MushtaqSubtype.ISM_MAKAN

    def test_ism_ala(self):
        r = _judge("مِفْتَاحٌ", DalType.ISM, wazns=[_wazn("ism_ala")])
        assert r.judgment == IshtiqaqJudgment.MUSHTAQ
        assert r.subtype == MushtaqSubtype.ISM_ALA

    def test_unknown_pattern_class_does_not_count_as_mushtaq(self):
        # If pattern_class is something we cannot map, treat as no-match.
        r = _judge("شيء", DalType.ISM, wazns=[_wazn("totally_unknown_class")])
        # No mapped mushtaq + no root + not in registry → JAMID_DHAT.
        assert r.judgment == IshtiqaqJudgment.JAMID
        assert r.subtype == JamidSubtype.JAMID_DHAT


# ---------------------------------------------------------------------------
# Jamid cases
# ---------------------------------------------------------------------------


class TestJamid:
    def test_functional_jamid_via_registry(self):
        r = _judge("هَذَا", DalType.ISM)
        assert r.judgment == IshtiqaqJudgment.JAMID
        assert r.subtype == JamidSubtype.JAMID_FUNCTIONAL

    def test_proper_name_jamid(self):
        r = _judge("محمد", DalType.ISM, proper=True)
        assert r.judgment == IshtiqaqJudgment.JAMID
        assert r.subtype == JamidSubtype.JAMID_PROPER_NAME

    def test_masdar_asli_from_root_no_wazn(self):
        # كِتاب has root k-t-b but no mushtaq wazn match.
        r = _judge("كِتَابٌ", DalType.ISM, roots=[_root()])
        assert r.judgment == IshtiqaqJudgment.JAMID
        assert r.subtype == JamidSubtype.JAMID_MASDAR_ASLI

    def test_jamid_dhat_no_root_no_wazn(self):
        r = _judge("رَجُلٌ", DalType.ISM)
        assert r.judgment == IshtiqaqJudgment.JAMID
        assert r.subtype == JamidSubtype.JAMID_DHAT


# ---------------------------------------------------------------------------
# R8 — competing wazn candidates trigger UNRESOLVED
# ---------------------------------------------------------------------------


class TestCompetition:
    def test_competing_mushtaq_subtypes_unresolved(self):
        r = _judge(
            "x",
            DalType.ISM,
            wazns=[_wazn("active_participle"), _wazn("ism_tafdil")],
        )
        assert r.judgment == IshtiqaqJudgment.UNRESOLVED
        assert any(
            res.type == ResidualType.MUFRAD_JAMID_MUSHTAQ_UNRESOLVED
            for res in r.residuals
        )

    def test_duplicate_same_subtype_resolves(self):
        # Two candidates pointing to the same MushtaqSubtype must NOT
        # be treated as competition.
        r = _judge(
            "كَاتِبٌ",
            DalType.ISM,
            wazns=[_wazn("active_participle"), _wazn("ism_fail")],
        )
        assert r.judgment == IshtiqaqJudgment.MUSHTAQ


# ---------------------------------------------------------------------------
# Orthogonality with binaa axis — the 2x2 matrix
# ---------------------------------------------------------------------------


class TestAxisOrthogonality:
    def test_mabni_jamid_demonstrative(self):
        r = _judge("هَذَا", DalType.ISM)
        # MABNI + JAMID (this test only checks the ishtiqaq axis).
        assert r.judgment == IshtiqaqJudgment.JAMID

    def test_mabni_not_applicable_particle(self):
        # MABNI on binaa axis, NOT_APPLICABLE on ishtiqaq axis.
        r = _judge("مِنْ", DalType.HARF)
        assert r.judgment == IshtiqaqJudgment.NOT_APPLICABLE

    def test_muerab_jamid_common_noun(self):
        r = _judge("رَجُلٌ", DalType.ISM)
        assert r.judgment == IshtiqaqJudgment.JAMID

    def test_muerab_mushtaq_active_participle(self):
        r = _judge("كَاتِبٌ", DalType.ISM, wazns=[_wazn("active_participle")])
        assert r.judgment == IshtiqaqJudgment.MUSHTAQ


# ---------------------------------------------------------------------------
# Anti-hallucination guard
# ---------------------------------------------------------------------------


class TestAntiHallucinationGuard:
    def test_input_has_no_syllable_fields(self):
        fields = set(IshtiqaqJudgeInput.__dataclass_fields__.keys())
        forbidden = {
            "syllable_count",
            "syllable_shapes",
            "syllables",
            "cv_shape",
        }
        assert forbidden.isdisjoint(fields)


# ---------------------------------------------------------------------------
# Evidence
# ---------------------------------------------------------------------------


class TestEvidence:
    def test_each_rule_emits_tagged_evidence(self):
        r = _judge("هَذَا", DalType.ISM)
        assert isinstance(r.evidence, _E)
        assert r.evidence.source.startswith("ishtiqaq_judge.R")
