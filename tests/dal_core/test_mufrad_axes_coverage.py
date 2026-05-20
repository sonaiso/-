"""PR-G — Anti-hallucination coverage tests.

This file is the **canary** that prevents the original hallucination from
returning. It enforces three architectural invariants over the mufrad
axes:

  1. The 2×2 matrix of (binaa, ishtiqaq) is fully covered by real Arabic
     words — every cell has at least one example, and the cells are
     mutually exclusive.
  2. ``harf`` is *always* MABNI on the binaa axis. There is no exception.
  3. Two words with the same surface syllable count can land in different
     binaa cells — i.e. syllable count is NEVER a usable predictor of
     binaa judgment. This is the "equal syllable count" guard the plan
     specifically calls out (§5.4).

If anyone in the future wires syllable shape into ``judge_binaa`` or
``judge_ishtiqaq``, at least one of these tests will fail loudly.
"""

import pytest

from dal_core.binaa_judge import BinaaJudgeInput, judge_binaa
from dal_core.d_type import DalType
from dal_core.ishtiqaq_judge import IshtiqaqJudgeInput, judge_ishtiqaq
from dal_core.morph_features import WaznCandidate
from dal_core.mufrad_axes import (
    BinaaJudgment,
    IshtiqaqJudgment,
    JamidSubtype,
    MushtaqSubtype,
)
from dal_core.ranks import LughaRank
from dal_core.type_ids import VerbTypeID


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _wazn(pc: str) -> WaznCandidate:
    return WaznCandidate(
        wazn="x",
        pattern_class=pc,
        evidence=(),
        rank=LughaRank.QIYAS,
        confidence=1.0,
    )


def _full_judge(
    form: str,
    dt: DalType,
    *,
    wazns=(),
    verb_type_id=None,
    proper=False,
):
    """Run BOTH judges and return (binaa_judgment, ishtiqaq_judgment)."""
    bj = judge_binaa(
        BinaaJudgeInput(
            dal_type=dt, surface_form=form, verb_type_id=verb_type_id
        )
    )
    ij = judge_ishtiqaq(
        IshtiqaqJudgeInput(
            dal_type=dt,
            surface_form=form,
            wazn_candidates=tuple(wazns),
            is_proper_name=proper,
        )
    )
    return bj, ij


# ---------------------------------------------------------------------------
# Golden cell table: (form, type, wazns, verb_type, expected_binaa,
# expected_ishtiqaq, expected_mushtaq/jamid subtype or None)
# ---------------------------------------------------------------------------


GOLDEN_CELLS = [
    # ----- ISM × MABNI × JAMID (functional pronouns/demonstratives) -----
    (
        "هَذَا",
        DalType.ISM,
        [],
        None,
        BinaaJudgment.MABNI,
        IshtiqaqJudgment.JAMID,
        JamidSubtype.JAMID_FUNCTIONAL,
        False,
    ),
    (
        "الَّذِينَ",
        DalType.ISM,
        [],
        None,
        BinaaJudgment.MABNI,
        IshtiqaqJudgment.JAMID,
        JamidSubtype.JAMID_FUNCTIONAL,
        False,
    ),
    (
        "كَيْفَ",
        DalType.ISM,
        [],
        None,
        BinaaJudgment.MABNI,
        IshtiqaqJudgment.JAMID,
        JamidSubtype.JAMID_FUNCTIONAL,
        False,
    ),
    # ----- ISM × MUERAB × JAMID (concrete and proper jamid) -----
    (
        "رَجُلٌ",
        DalType.ISM,
        [],
        None,
        BinaaJudgment.MUERAB,
        IshtiqaqJudgment.JAMID,
        JamidSubtype.JAMID_DHAT,
        False,
    ),
    (
        "محمد",
        DalType.ISM,
        [],
        None,
        BinaaJudgment.MUERAB,
        IshtiqaqJudgment.JAMID,
        JamidSubtype.JAMID_PROPER_NAME,
        True,
    ),
    # ----- ISM × MUERAB × MUSHTAQ (derived nominals) -----
    (
        "كَاتِبٌ",
        DalType.ISM,
        [_wazn("active_participle")],
        None,
        BinaaJudgment.MUERAB,
        IshtiqaqJudgment.MUSHTAQ,
        MushtaqSubtype.ISM_FAIL,
        False,
    ),
    (
        "مَكْتُوبٌ",
        DalType.ISM,
        [_wazn("passive_participle")],
        None,
        BinaaJudgment.MUERAB,
        IshtiqaqJudgment.MUSHTAQ,
        MushtaqSubtype.ISM_MAFUL,
        False,
    ),
    (
        "أَفْضَلُ",
        DalType.ISM,
        [_wazn("ism_tafdil")],
        None,
        BinaaJudgment.MUERAB,
        IshtiqaqJudgment.MUSHTAQ,
        MushtaqSubtype.ISM_TAFDIL,
        False,
    ),
    (
        "مَكْتَبٌ",
        DalType.ISM,
        [_wazn("ism_makan")],
        None,
        BinaaJudgment.MUERAB,
        IshtiqaqJudgment.MUSHTAQ,
        MushtaqSubtype.ISM_MAKAN,
        False,
    ),
    (
        "مِفْتَاحٌ",
        DalType.ISM,
        [_wazn("ism_ala")],
        None,
        BinaaJudgment.MUERAB,
        IshtiqaqJudgment.MUSHTAQ,
        MushtaqSubtype.ISM_ALA,
        False,
    ),
    # ----- FIIL × MABNI × NOT_APPLICABLE -----
    (
        "ضَرَبَ",
        DalType.FIIL,
        [],
        VerbTypeID.FIIL_MADI,
        BinaaJudgment.MABNI,
        IshtiqaqJudgment.NOT_APPLICABLE,
        None,
        False,
    ),
    (
        "اضْرِبْ",
        DalType.FIIL,
        [],
        VerbTypeID.FIIL_AMR,
        BinaaJudgment.MABNI,
        IshtiqaqJudgment.NOT_APPLICABLE,
        None,
        False,
    ),
    (
        "يَضْرِبْنَ",  # نون النسوة
        DalType.FIIL,
        [],
        VerbTypeID.FIIL_MUDARI,
        BinaaJudgment.MABNI,
        IshtiqaqJudgment.NOT_APPLICABLE,
        None,
        False,
    ),
    # ----- FIIL × MUERAB × NOT_APPLICABLE -----
    (
        "يَضْرِبُ",
        DalType.FIIL,
        [],
        VerbTypeID.FIIL_MUDARI,
        BinaaJudgment.MUERAB,
        IshtiqaqJudgment.NOT_APPLICABLE,
        None,
        False,
    ),
    # ----- HARF × MABNI × NOT_APPLICABLE -----
    (
        "مِنْ",
        DalType.HARF,
        [],
        None,
        BinaaJudgment.MABNI,
        IshtiqaqJudgment.NOT_APPLICABLE,
        None,
        False,
    ),
    (
        "إِنَّ",
        DalType.HARF,
        [],
        None,
        BinaaJudgment.MABNI,
        IshtiqaqJudgment.NOT_APPLICABLE,
        None,
        False,
    ),
]


# ---------------------------------------------------------------------------
# Test 1: Every golden cell lands in the expected (binaa, ishtiqaq, subtype) cell
# ---------------------------------------------------------------------------


class TestGoldenCellCoverage:
    @pytest.mark.parametrize(
        "form,dt,wazns,vid,exp_binaa,exp_ishtiqaq,exp_subtype,proper",
        GOLDEN_CELLS,
    )
    def test_word_lands_in_expected_cell(
        self,
        form,
        dt,
        wazns,
        vid,
        exp_binaa,
        exp_ishtiqaq,
        exp_subtype,
        proper,
    ):
        bj, ij = _full_judge(
            form, dt, wazns=wazns, verb_type_id=vid, proper=proper
        )
        assert bj.judgment == exp_binaa, (
            f"{form}: expected binaa={exp_binaa.name}, "
            f"got {bj.judgment.name}"
        )
        assert ij.judgment == exp_ishtiqaq, (
            f"{form}: expected ishtiqaq={exp_ishtiqaq.name}, "
            f"got {ij.judgment.name}"
        )
        if exp_subtype is not None:
            assert ij.subtype == exp_subtype, (
                f"{form}: expected subtype={exp_subtype.name}, "
                f"got {ij.subtype}"
            )


# ---------------------------------------------------------------------------
# Test 2: Every (binaa, ishtiqaq) cell of the orthogonality matrix is
# populated by at least one golden word
# ---------------------------------------------------------------------------


def _classify_cells():
    cells = {}
    for (form, dt, wazns, vid, eb, ei, _es, proper) in GOLDEN_CELLS:
        cells.setdefault((eb, ei), []).append(form)
    return cells


class TestOrthogonalityMatrixCoverage:
    def test_all_required_cells_populated(self):
        cells = _classify_cells()
        # Each axis cell required by the plan §2.
        required = [
            (BinaaJudgment.MABNI, IshtiqaqJudgment.JAMID),  # هذا، الذين
            (BinaaJudgment.MUERAB, IshtiqaqJudgment.JAMID),  # رجل، محمد
            (BinaaJudgment.MUERAB, IshtiqaqJudgment.MUSHTAQ),  # كاتب
            (BinaaJudgment.MABNI, IshtiqaqJudgment.NOT_APPLICABLE),  # من، ضرب
            (BinaaJudgment.MUERAB, IshtiqaqJudgment.NOT_APPLICABLE),  # يضرب
        ]
        for cell in required:
            assert cell in cells, (
                f"Cell {cell[0].name}×{cell[1].name} not populated; "
                f"every plan-required cell needs at least one golden word."
            )


# ---------------------------------------------------------------------------
# Test 3: Negative guard — no harf can ever be MUERAB.
# ---------------------------------------------------------------------------


class TestHarfIsAlwaysMabni:
    @pytest.mark.parametrize(
        "form", ["مِنْ", "إِنَّ", "هَلْ", "فِي", "لَنْ", "كَيْ", "إِلَى"]
    )
    def test_every_particle_is_mabni(self, form):
        bj, _ = _full_judge(form, DalType.HARF)
        # Hard invariant. If this ever fails, the binaa judge has been
        # corrupted with an ad-hoc rule.
        assert bj.judgment == BinaaJudgment.MABNI, (
            f"{form}: HARF must always be MABNI; got {bj.judgment.name}"
        )


# ---------------------------------------------------------------------------
# Test 4: THE anti-hallucination canary.
#
# Two ISM words with very similar / equal surface CV shape but living in
# DIFFERENT binaa cells. If anyone ever derives binaa from syllable
# count, both will collapse to the same cell and this test will fail.
# ---------------------------------------------------------------------------


class TestEqualSyllableCountWordsDifferentJudgment:
    def test_hadha_vs_rajul_have_different_binaa(self):
        # Both هَذَا and رَجُلٌ are short ~2-3-syllable Arabic words.
        # هَذَا is MABNI (it's in the closed pronouns/demonstratives list)
        # رَجُلٌ is MUERAB (it's a regular common noun).
        bj_hadha, _ = _full_judge("هَذَا", DalType.ISM)
        bj_rajul, _ = _full_judge("رَجُلٌ", DalType.ISM)
        assert bj_hadha.judgment == BinaaJudgment.MABNI
        assert bj_rajul.judgment == BinaaJudgment.MUERAB
        assert bj_hadha.judgment != bj_rajul.judgment, (
            "Equal-syllable-count canary: هَذَا and رَجُلٌ have similar "
            "syllable shape but must land in DIFFERENT binaa cells. "
            "If you see this fail, somebody wired syllable count into "
            "judge_binaa, which is forbidden by plan §5.1."
        )

    def test_anta_vs_kaatib_have_different_axes(self):
        # أَنْتَ and كَاتِب are both ~2 syllables.
        bj_anta, ij_anta = _full_judge("أَنْتَ", DalType.ISM)
        bj_katib, ij_katib = _full_judge(
            "كَاتِبٌ",
            DalType.ISM,
            wazns=[_wazn("active_participle")],
        )
        assert bj_anta.judgment == BinaaJudgment.MABNI
        assert bj_katib.judgment == BinaaJudgment.MUERAB
        assert ij_anta.judgment == IshtiqaqJudgment.JAMID
        assert ij_katib.judgment == IshtiqaqJudgment.MUSHTAQ


# ---------------------------------------------------------------------------
# Test 5: Axis-input contract — judges accept NO syllable info.
# ---------------------------------------------------------------------------


class TestJudgeInputsHaveNoSyllableFields:
    def test_binaa_input(self):
        fields = set(BinaaJudgeInput.__dataclass_fields__.keys())
        bad = {"syllable_count", "syllable_shapes", "syllables", "cv_shape"}
        leaks = fields & bad
        assert not leaks, f"binaa_judge accepts syllable inputs: {leaks}"

    def test_ishtiqaq_input(self):
        fields = set(IshtiqaqJudgeInput.__dataclass_fields__.keys())
        bad = {"syllable_count", "syllable_shapes", "syllables", "cv_shape"}
        leaks = fields & bad
        assert not leaks, f"ishtiqaq_judge accepts syllable inputs: {leaks}"


# ---------------------------------------------------------------------------
# Test 6: Plan §2 four-quadrant matrix is explicitly populated.
# (Sanity restatement: this is also a documentation test.)
# ---------------------------------------------------------------------------


class TestPlanFourCellExamples:
    def test_mabni_jamid_demonstrative_exists(self):
        bj, ij = _full_judge("هَذَا", DalType.ISM)
        assert (bj.judgment, ij.judgment) == (
            BinaaJudgment.MABNI,
            IshtiqaqJudgment.JAMID,
        )

    def test_muerab_jamid_concrete_exists(self):
        bj, ij = _full_judge("رَجُلٌ", DalType.ISM)
        assert (bj.judgment, ij.judgment) == (
            BinaaJudgment.MUERAB,
            IshtiqaqJudgment.JAMID,
        )

    def test_muerab_mushtaq_active_participle_exists(self):
        bj, ij = _full_judge(
            "كَاتِبٌ", DalType.ISM, wazns=[_wazn("active_participle")]
        )
        assert (bj.judgment, ij.judgment) == (
            BinaaJudgment.MUERAB,
            IshtiqaqJudgment.MUSHTAQ,
        )

    def test_mabni_jamid_relative_exists(self):
        bj, ij = _full_judge("الَّذِينَ", DalType.ISM)
        assert (bj.judgment, ij.judgment) == (
            BinaaJudgment.MABNI,
            IshtiqaqJudgment.JAMID,
        )
