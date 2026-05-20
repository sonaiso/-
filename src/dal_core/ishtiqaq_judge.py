"""
Ishtiqaq / Jamid Judge (قاضي الاشتقاق/الجمود)

==============================================================================
ANTI-HALLUCINATION GUARD
==============================================================================
This judge MUST NOT use ``syllable_count`` or ``syllable_shapes``. Like the
binaa judge, this is a judicial axis built ONLY on:

  1. ``DalType`` from D5 (IDENTITY_AXIS),
  2. ``WaznCandidate``s from D4 (TEMPLATE),
  3. ``RootCandidate``s from D3 (ORIGIN),
  4. The closed mabni-noun registry (PR-B) for functional-jamid detection,
  5. An optional ``is_proper_name`` flag from upstream type classification.

==============================================================================

Rule order:

  R1  HARF                            ⇒ NOT_APPLICABLE
  R2  FIIL                            ⇒ NOT_APPLICABLE
  R3  ISM in mabni registry           ⇒ JAMID, JAMID_FUNCTIONAL
  R4  ISM is_proper_name              ⇒ JAMID, JAMID_PROPER_NAME
  R5  ISM matches a known mushtaq wazn (single, no competition)
                                      ⇒ MUSHTAQ, mapped MushtaqSubtype
  R6  ISM has root attested as verbal + no mushtaq wazn match
                                      ⇒ JAMID, JAMID_MASDAR_ASLI
  R7  ISM with no root + no wazn match ⇒ JAMID, JAMID_DHAT
  R8  Competing wazn candidates       ⇒ UNRESOLVED + residual

  R0  Missing identity                ⇒ UNRESOLVED + residual
"""

from dataclasses import dataclass
from typing import Optional, Union

from dal_core.d_type import DalType
from dal_core.evidence import Evidence, make_evidence
from dal_core.mabni_registry import (
    MabniRegistry,
    get_default_mabni_registry,
)
from dal_core.morph_features import RootCandidate, WaznCandidate
from dal_core.mufrad_axes import (
    IshtiqaqJudgment,
    JamidSubtype,
    MushtaqSubtype,
)
from dal_core.residuals import Residual, ResidualSeverity, ResidualType


# =============================================================================
# Pattern-class → MushtaqSubtype mapping
# =============================================================================


# Maps the free-form ``WaznCandidate.pattern_class`` string used elsewhere
# in the codebase (see ``morph_features.py``) to a typed MushtaqSubtype.
# Any new pattern_class added in the future must extend this map or be
# treated as "unknown derivation" by the judge.
_PATTERN_CLASS_TO_SUBTYPE: dict[str, MushtaqSubtype] = {
    "active_participle": MushtaqSubtype.ISM_FAIL,
    "ism_fail": MushtaqSubtype.ISM_FAIL,
    "passive_participle": MushtaqSubtype.ISM_MAFUL,
    "ism_maful": MushtaqSubtype.ISM_MAFUL,
    "sifa_mushabbaha": MushtaqSubtype.SIFA_MUSHABBAHA,
    "resembling_adjective": MushtaqSubtype.SIFA_MUSHABBAHA,
    "ism_tafdil": MushtaqSubtype.ISM_TAFDIL,
    "comparative": MushtaqSubtype.ISM_TAFDIL,
    "superlative": MushtaqSubtype.ISM_TAFDIL,
    "ism_zaman": MushtaqSubtype.ISM_ZAMAN,
    "ism_makan": MushtaqSubtype.ISM_MAKAN,
    "ism_zaman_makan": MushtaqSubtype.ISM_MAKAN,  # default to makan; ambiguous
    "ism_ala": MushtaqSubtype.ISM_ALA,
    "instrument_noun": MushtaqSubtype.ISM_ALA,
    "masdar_mimi": MushtaqSubtype.MASDAR_MIMI,
    "masdar_sinaii": MushtaqSubtype.MASDAR_SINAII,
}


def _map_pattern_class(pc: str) -> Optional[MushtaqSubtype]:
    if not pc:
        return None
    return _PATTERN_CLASS_TO_SUBTYPE.get(pc.strip().lower())


# =============================================================================
# Input contract
# =============================================================================


@dataclass(frozen=True)
class IshtiqaqJudgeInput:
    """The minimal typed bundle the ishtiqaq judge accepts."""

    dal_type: DalType
    """Identity from D5."""

    surface_form: str
    """Vocalized surface form. Used ONLY for registry lookup."""

    root_candidates: tuple[RootCandidate, ...] = ()
    """Candidate roots from D3."""

    wazn_candidates: tuple[WaznCandidate, ...] = ()
    """Candidate patterns from D4. Competition (>1 with different
    pattern_class) triggers UNRESOLVED."""

    is_proper_name: bool = False
    """True iff upstream classification identifies this as a proper noun.
    Cheap, explicit flag — avoids re-deriving from type_id here."""


# =============================================================================
# Result
# =============================================================================


@dataclass(frozen=True)
class IshtiqaqJudgmentResult:
    judgment: IshtiqaqJudgment
    subtype: Optional[Union[MushtaqSubtype, JamidSubtype]]
    evidence: Evidence
    residuals: tuple[Residual, ...]


# =============================================================================
# Public judge
# =============================================================================


def judge_ishtiqaq(
    input_: IshtiqaqJudgeInput,
    registry: Optional[MabniRegistry] = None,
) -> IshtiqaqJudgmentResult:
    """Apply the rule order documented at the module docstring."""
    reg = registry or get_default_mabni_registry()

    # R0 — guard against missing identity.
    if input_.dal_type is None or input_.dal_type == DalType.AMBIGUOUS:
        return IshtiqaqJudgmentResult(
            judgment=IshtiqaqJudgment.UNRESOLVED,
            subtype=None,
            evidence=make_evidence(
                source="ishtiqaq_judge.R0",
                reason="DalType missing or AMBIGUOUS; cannot judge ishtiqaq.",
                confidence=0.0,
            ),
            residuals=(
                Residual(
                    type=ResidualType.MUFRAD_JAMID_MUSHTAQ_UNRESOLVED,
                    severity=ResidualSeverity.BLOCKER,
                    message="Identity axis (D5) not resolved before ishtiqaq judge.",
                ),
            ),
        )

    # R1, R2 — non-nominal types: axis does not apply.
    if input_.dal_type == DalType.HARF:
        return IshtiqaqJudgmentResult(
            judgment=IshtiqaqJudgment.NOT_APPLICABLE,
            subtype=None,
            evidence=make_evidence(
                source="ishtiqaq_judge.R1",
                reason="الجامد/المشتق محور اسمي؛ الحرف لا يُحكم عليه به.",
                confidence=1.0,
            ),
            residuals=(),
        )

    if input_.dal_type == DalType.FIIL:
        return IshtiqaqJudgmentResult(
            judgment=IshtiqaqJudgment.NOT_APPLICABLE,
            subtype=None,
            evidence=make_evidence(
                source="ishtiqaq_judge.R2",
                reason="الفعل لا يُحكم عليه بالجمود/الاشتقاق بهذا المعنى.",
                confidence=1.0,
            ),
            residuals=(),
        )

    if input_.dal_type != DalType.ISM:
        # Defensive — unknown type.
        return IshtiqaqJudgmentResult(
            judgment=IshtiqaqJudgment.UNRESOLVED,
            subtype=None,
            evidence=make_evidence(
                source="ishtiqaq_judge.R0",
                reason=f"Unrecognized DalType {input_.dal_type!r}.",
                confidence=0.0,
            ),
            residuals=(
                Residual(
                    type=ResidualType.MUFRAD_JAMID_MUSHTAQ_UNRESOLVED,
                    severity=ResidualSeverity.BLOCKER,
                    message=f"Unrecognized DalType {input_.dal_type!r}.",
                ),
            ),
        )

    # ----------------------------- ISM -----------------------------------

    # R3 — functional-jamid via the closed mabni registry.
    if reg.is_mabni_noun(input_.surface_form):
        return IshtiqaqJudgmentResult(
            judgment=IshtiqaqJudgment.JAMID,
            subtype=JamidSubtype.JAMID_FUNCTIONAL,
            evidence=make_evidence(
                source="ishtiqaq_judge.R3",
                reason="الاسم من القائمة المغلقة المبنية ⇒ جامد وظيفي.",
                confidence=1.0,
            ),
            residuals=(),
        )

    # R4 — proper noun.
    if input_.is_proper_name:
        return IshtiqaqJudgmentResult(
            judgment=IshtiqaqJudgment.JAMID,
            subtype=JamidSubtype.JAMID_PROPER_NAME,
            evidence=make_evidence(
                source="ishtiqaq_judge.R4",
                reason="اسم علم ⇒ جامد علم.",
                confidence=1.0,
            ),
            residuals=(),
        )

    # Inspect wazn candidates for mushtaq matches.
    mushtaq_subtypes: list[MushtaqSubtype] = []
    for w in input_.wazn_candidates:
        st = _map_pattern_class(w.pattern_class)
        if st is not None:
            mushtaq_subtypes.append(st)

    distinct_mushtaq = list(dict.fromkeys(mushtaq_subtypes))

    # R8 — competing mushtaq subtypes.
    if len(distinct_mushtaq) > 1:
        return IshtiqaqJudgmentResult(
            judgment=IshtiqaqJudgment.UNRESOLVED,
            subtype=None,
            evidence=make_evidence(
                source="ishtiqaq_judge.R8",
                reason=(
                    "Multiple mushtaq pattern_class candidates compete: "
                    f"{[s.name for s in distinct_mushtaq]}"
                ),
                confidence=0.0,
            ),
            residuals=(
                Residual(
                    type=ResidualType.MUFRAD_JAMID_MUSHTAQ_UNRESOLVED,
                    severity=ResidualSeverity.BLOCKER,
                    message="Competing mushtaq pattern classes preserved.",
                ),
            ),
        )

    # R5 — single mushtaq match.
    if len(distinct_mushtaq) == 1:
        st = distinct_mushtaq[0]
        return IshtiqaqJudgmentResult(
            judgment=IshtiqaqJudgment.MUSHTAQ,
            subtype=st,
            evidence=make_evidence(
                source="ishtiqaq_judge.R5",
                reason=f"تطابق وزن اشتقاقي معروف ⇒ مشتق ({st.value}).",
                confidence=1.0,
            ),
            residuals=(),
        )

    # No mushtaq wazn match. Disambiguate jamid sub-cases.

    # R6 — has attested root ⇒ masdar asli.
    if input_.root_candidates:
        return IshtiqaqJudgmentResult(
            judgment=IshtiqaqJudgment.JAMID,
            subtype=JamidSubtype.JAMID_MASDAR_ASLI,
            evidence=make_evidence(
                source="ishtiqaq_judge.R6",
                reason="جذر مُثبت بدون وزن اشتقاقي معروف ⇒ مصدر أصلي.",
                confidence=0.9,
            ),
            residuals=(),
        )

    # R7 — concrete jamid (dhat) default.
    return IshtiqaqJudgmentResult(
        judgment=IshtiqaqJudgment.JAMID,
        subtype=JamidSubtype.JAMID_DHAT,
        evidence=make_evidence(
            source="ishtiqaq_judge.R7",
            reason="لا اشتقاق ولا جذر مثبت ⇒ جامد ذات.",
            confidence=0.8,
        ),
        residuals=(),
    )


__all__ = [
    "IshtiqaqJudgeInput",
    "IshtiqaqJudgmentResult",
    "judge_ishtiqaq",
]
