"""Integration tests for PR-E: axes wired into MufradProof and
NounInflectionClass with backward compatibility preserved.
"""

import pytest

from dal_core.composition_readiness import CompositionReadiness
from dal_core.d_form import FormCandidate
from dal_core.d_lugha import LughaAttestation
from dal_core.d_type import DalType, TypedDal
from dal_core.evidence import Evidence
from dal_core.morph_features import (
    CandidateStatus,
    NounInflectionClass,
    SegmentationProof,
    StemProof,
)
from dal_core.mufrad_axes import (
    BinaaJudgment,
    BinaaSubtype,
    IshtiqaqJudgment,
    JamidSubtype,
    MushtaqSubtype,
    SarfFlexibility,
)
from dal_core.mufrad_proof import MufradProof
from dal_core.ranks import FormRank, LughaRank


# Build a minimal MufradProof matching the real ctor signature.


def _minimal_kwargs(dt: DalType = DalType.ISM) -> dict:
    form = FormCandidate(text="x", vocalization="x", rank=FormRank.FORM)
    lugha = LughaAttestation(form=form, rank=LughaRank.TAWATUR, is_arabic=True)
    typed_dal = TypedDal(attestation=lugha, dal_type=dt)
    seg = SegmentationProof(
        segments=("x",),
        evidence=(Evidence("manual", "test", LughaRank.TAWATUR),),
        rank=LughaRank.TAWATUR,
    )
    stem = StemProof(
        stem="x",
        evidence=(Evidence("manual", "test", LughaRank.TAWATUR),),
        rank=LughaRank.TAWATUR,
    )
    return dict(
        form=form,
        lugha=lugha,
        type=typed_dal,
        segmentation=seg,
        stem=stem,
        clitics=tuple(),
        root_candidates=tuple(),
        wazn_candidates=tuple(),
        derivation_status=CandidateStatus.NOT_APPLICABLE,
        jamid_mushtaq_status=CandidateStatus.NOT_APPLICABLE,
        mabni_murab_status=CandidateStatus.NOT_APPLICABLE,
        definiteness_status=CandidateStatus.NOT_APPLICABLE,
        gender_status=CandidateStatus.NOT_APPLICABLE,
        number_status=CandidateStatus.NOT_APPLICABLE,
        composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
    )


def _build(
    *,
    dt: DalType = DalType.ISM,
    binaa: BinaaJudgment = BinaaJudgment.UNRESOLVED,
    binaa_sub: BinaaSubtype | None = None,
    ishtiqaq: IshtiqaqJudgment = IshtiqaqJudgment.UNRESOLVED,
    ishtiqaq_sub=None,
    sarf: SarfFlexibility = SarfFlexibility.NOT_APPLICABLE,
    nic: NounInflectionClass | None = None,
) -> MufradProof:
    kw = _minimal_kwargs(dt)
    kw["noun_inflection_class"] = nic
    return MufradProof(
        **kw,
        binaa_judgment=binaa,
        binaa_subtype=binaa_sub,
        ishtiqaq_judgment=ishtiqaq,
        ishtiqaq_subtype=ishtiqaq_sub,
        sarf_flexibility=sarf,
    )


# ---------------------------------------------------------------------------
# Backward compatibility
# ---------------------------------------------------------------------------


class TestBackwardCompat:
    def test_default_constructor_omitting_new_fields_works(self):
        m = MufradProof(**_minimal_kwargs(DalType.ISM))
        assert m.binaa_judgment == BinaaJudgment.UNRESOLVED
        assert m.ishtiqaq_judgment == IshtiqaqJudgment.UNRESOLVED
        assert m.sarf_flexibility == SarfFlexibility.NOT_APPLICABLE

    def test_legacy_inflection_type_string_still_accepted(self):
        nic = NounInflectionClass(
            inflection_type="mabni",
            declension_pattern="indeclinable",
            evidence=(),
            rank=LughaRank.QIYAS,
        )
        assert nic.inflection_type == "mabni"
        assert nic.binaa_judgment is None
        assert nic.sarf_flexibility is None

    def test_new_axes_can_be_populated_on_nic(self):
        nic = NounInflectionClass(
            inflection_type="munassarif",
            declension_pattern="triptote",
            evidence=(),
            rank=LughaRank.QIYAS,
            binaa_judgment=BinaaJudgment.MUERAB,
            sarf_flexibility=SarfFlexibility.MUNSARIF,
        )
        assert nic.binaa_judgment == BinaaJudgment.MUERAB
        assert nic.sarf_flexibility == SarfFlexibility.MUNSARIF


# ---------------------------------------------------------------------------
# Axis consistency validation
# ---------------------------------------------------------------------------


class TestAxisConsistency:
    def test_mabni_with_typed_subtype_ok(self):
        m = _build(
            dt=DalType.ISM,
            binaa=BinaaJudgment.MABNI,
            binaa_sub=BinaaSubtype.BINAA_SUKUN,
        )
        assert m.binaa_subtype == BinaaSubtype.BINAA_SUKUN

    def test_muerab_with_subtype_rejected(self):
        with pytest.raises(ValueError, match="binaa_subtype"):
            _build(
                dt=DalType.ISM,
                binaa=BinaaJudgment.MUERAB,
                binaa_sub=BinaaSubtype.BINAA_FATH,
            )

    def test_mushtaq_with_jamid_subtype_rejected(self):
        with pytest.raises(ValueError, match="ishtiqaq_subtype"):
            _build(
                dt=DalType.ISM,
                ishtiqaq=IshtiqaqJudgment.MUSHTAQ,
                ishtiqaq_sub=JamidSubtype.JAMID_DHAT,
            )

    def test_jamid_with_mushtaq_subtype_rejected(self):
        with pytest.raises(ValueError, match="ishtiqaq_subtype"):
            _build(
                dt=DalType.ISM,
                ishtiqaq=IshtiqaqJudgment.JAMID,
                ishtiqaq_sub=MushtaqSubtype.ISM_FAIL,
            )

    def test_not_applicable_must_have_no_subtype(self):
        with pytest.raises(ValueError, match="ishtiqaq_subtype"):
            _build(
                dt=DalType.HARF,
                ishtiqaq=IshtiqaqJudgment.NOT_APPLICABLE,
                ishtiqaq_sub=JamidSubtype.JAMID_DHAT,
            )

    def test_typed_mushtaq_pair_accepted(self):
        m = _build(
            dt=DalType.ISM,
            ishtiqaq=IshtiqaqJudgment.MUSHTAQ,
            ishtiqaq_sub=MushtaqSubtype.ISM_FAIL,
        )
        assert m.ishtiqaq_subtype == MushtaqSubtype.ISM_FAIL


# ---------------------------------------------------------------------------
# Case-sign matrix backward-compat: classified field is preferred
# ---------------------------------------------------------------------------


class TestCaseSignMatrixReadsClassifiedField:
    def _vec(self, nic):
        from dal_core.composition_readiness import CompositionReadiness as CR
        from dal_core.presyntax_vector import PreSyntaxMufradVector

        return PreSyntaxMufradVector(
            mufrad_id="m1",
            raw_span=(0, 1),
            type_value="ISM",
            type_id=None,
            type_rank=LughaRank.TAWATUR,
            mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
            noun_inflection_class=nic,
            verb_features=None,
            particle_operator_potential=None,
            surface_effects=(),
            case_sign_potentials=(),
            morph_rank=LughaRank.TAWATUR,
            final_rank=LughaRank.TAWATUR,
            residuals=(),
            trace_id="t1",
            competitors_count=0,
            composition_readiness=CR.READY_FOR_COMPOSITION,
        )

    def test_classified_mabni_detected(self):
        from dal_core.case_sign_matrix import _is_mabni_by_value

        nic = NounInflectionClass(
            inflection_type="",  # legacy string empty
            declension_pattern="indeclinable",
            evidence=(),
            rank=LughaRank.QIYAS,
            binaa_judgment=BinaaJudgment.MABNI,
        )
        assert _is_mabni_by_value(self._vec(nic)) is True

    def test_legacy_string_still_detected(self):
        from dal_core.case_sign_matrix import _is_mabni_by_value

        nic = NounInflectionClass(
            inflection_type="mabni",  # legacy
            declension_pattern="indeclinable",
            evidence=(),
            rank=LughaRank.QIYAS,
        )
        assert _is_mabni_by_value(self._vec(nic)) is True

    def test_muerab_classified_not_treated_as_mabni(self):
        from dal_core.case_sign_matrix import _is_mabni_by_value

        nic = NounInflectionClass(
            inflection_type="munassarif",
            declension_pattern="triptote",
            evidence=(),
            rank=LughaRank.QIYAS,
            binaa_judgment=BinaaJudgment.MUERAB,
        )
        assert _is_mabni_by_value(self._vec(nic)) is False


# ---------------------------------------------------------------------------
# Public API surface
# ---------------------------------------------------------------------------


class TestPublicAPI:
    def test_axes_exported_from_dal_core(self):
        import dal_core

        for name in (
            "BinaaJudgment",
            "BinaaSubtype",
            "IshtiqaqJudgment",
            "MushtaqSubtype",
            "JamidSubtype",
            "SarfFlexibility",
            "judge_binaa",
            "judge_ishtiqaq",
            "get_default_mabni_registry",
        ):
            assert hasattr(dal_core, name), f"dal_core.{name} not exported"
