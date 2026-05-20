"""PR-F tests: PreSyntaxMufradVector exposes the classified axes and
its ``allows_operator_consumption`` gate blocks on UNRESOLVED axes.

These extend the PR #11 30-test suite to 35+ scenarios covering the new
5th gate.
"""

import pytest

from dal_core.composition_readiness import CompositionReadiness
from dal_core.morph_features import CandidateStatus
from dal_core.mufrad_axes import (
    BinaaJudgment,
    IshtiqaqJudgment,
)
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.ranks import LughaRank


def _vec(
    *,
    type_value: str = "ISM",
    binaa: BinaaJudgment = BinaaJudgment.MUERAB,
    ishtiqaq: IshtiqaqJudgment = IshtiqaqJudgment.JAMID,
    readiness: CompositionReadiness = CompositionReadiness.READY_FOR_COMPOSITION,
    type_id=None,
) -> PreSyntaxMufradVector:
    return PreSyntaxMufradVector(
        mufrad_id="m",
        raw_span=(0, 1),
        type_value=type_value,
        type_id=type_id,
        type_rank=LughaRank.TAWATUR,
        mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
        noun_inflection_class=None,
        verb_features=None,
        particle_operator_potential=None,
        surface_effects=(),
        case_sign_potentials=(),
        morph_rank=LughaRank.TAWATUR,
        final_rank=LughaRank.TAWATUR,
        residuals=(),
        trace_id="t",
        competitors_count=0,
        composition_readiness=readiness,
        binaa_judgment=binaa,
        ishtiqaq_judgment=ishtiqaq,
    )


# ---------------------------------------------------------------------------
# Axis fields are present and exposed
# ---------------------------------------------------------------------------


class TestAxisExposure:
    def test_vector_exposes_binaa_judgment(self):
        v = _vec(binaa=BinaaJudgment.MABNI)
        assert v.binaa_judgment == BinaaJudgment.MABNI

    def test_vector_exposes_ishtiqaq_judgment(self):
        v = _vec(ishtiqaq=IshtiqaqJudgment.MUSHTAQ)
        assert v.ishtiqaq_judgment == IshtiqaqJudgment.MUSHTAQ

    def test_axes_default_to_unresolved(self):
        # Construct with required args only — defaults must be UNRESOLVED.
        v = PreSyntaxMufradVector(
            mufrad_id="m",
            raw_span=(0, 1),
            type_value="ISM",
            type_id=None,
            type_rank=LughaRank.TAWATUR,
            mabni_murab_status=CandidateStatus.RESOLVED_CERTAIN,
            noun_inflection_class=None,
            verb_features=None,
            particle_operator_potential=None,
            surface_effects=(),
            case_sign_potentials=(),
            morph_rank=LughaRank.TAWATUR,
            final_rank=LughaRank.TAWATUR,
            residuals=(),
            trace_id="t",
            competitors_count=0,
            composition_readiness=CompositionReadiness.READY_FOR_COMPOSITION,
        )
        assert v.binaa_judgment == BinaaJudgment.UNRESOLVED
        assert v.ishtiqaq_judgment == IshtiqaqJudgment.UNRESOLVED


# ---------------------------------------------------------------------------
# Gate 5 — blocks operator consumption on UNRESOLVED axes
# ---------------------------------------------------------------------------


class TestGate5UnresolvedAxes:
    def test_unresolved_binaa_blocks_consumption(self):
        v = _vec(binaa=BinaaJudgment.UNRESOLVED)
        assert v.allows_operator_consumption() is False

    def test_unresolved_ishtiqaq_blocks_noun_consumption(self):
        v = _vec(type_value="ISM", ishtiqaq=IshtiqaqJudgment.UNRESOLVED)
        assert v.allows_operator_consumption() is False

    def test_resolved_axes_allow_consumption(self):
        v = _vec(
            type_value="ISM",
            binaa=BinaaJudgment.MUERAB,
            ishtiqaq=IshtiqaqJudgment.MUSHTAQ,
        )
        assert v.allows_operator_consumption() is True

    def test_verb_with_not_applicable_ishtiqaq_passes(self):
        # Verbs are NOT_APPLICABLE on ishtiqaq axis — this must not block.
        v = _vec(
            type_value="FIIL",
            binaa=BinaaJudgment.MABNI,
            ishtiqaq=IshtiqaqJudgment.NOT_APPLICABLE,
        )
        assert v.allows_operator_consumption() is True

    def test_particle_with_not_applicable_ishtiqaq_passes(self):
        v = _vec(
            type_value="HARF",
            binaa=BinaaJudgment.MABNI,
            ishtiqaq=IshtiqaqJudgment.NOT_APPLICABLE,
        )
        assert v.allows_operator_consumption() is True

    def test_verb_with_unresolved_ishtiqaq_is_NOT_blocked(self):
        # Edge case: for non-nouns, ishtiqaq UNRESOLVED should NOT block,
        # because the axis doesn't apply to them. (Defensive — should not
        # happen in practice; the judge would have returned NOT_APPLICABLE.)
        v = _vec(
            type_value="FIIL",
            binaa=BinaaJudgment.MABNI,
            ishtiqaq=IshtiqaqJudgment.UNRESOLVED,
        )
        assert v.allows_operator_consumption() is True


# ---------------------------------------------------------------------------
# Gate ordering preserved
# ---------------------------------------------------------------------------


class TestGateOrderingPreserved:
    def test_readiness_gate_still_active(self):
        # NOT_READY readiness must still block, even with resolved axes.
        v = _vec(
            readiness=CompositionReadiness.NOT_READY,
            binaa=BinaaJudgment.MUERAB,
            ishtiqaq=IshtiqaqJudgment.JAMID,
        )
        assert v.allows_operator_consumption() is False


# ---------------------------------------------------------------------------
# Type-id based noun detection works as well as type_value string
# ---------------------------------------------------------------------------


class TestNounDetection:
    def test_type_id_based_noun_blocks_on_unresolved_ishtiqaq(self):
        from dal_core.type_ids import NounTypeID

        v = _vec(
            type_value="",  # empty string; only type_id is informative
            type_id=NounTypeID.ISM_COMMON,
            binaa=BinaaJudgment.MUERAB,
            ishtiqaq=IshtiqaqJudgment.UNRESOLVED,
        )
        assert v.allows_operator_consumption() is False
