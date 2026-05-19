"""
Default seed entries for the NahwOperatorRegistry (PR #15).

Data only — kept separate from the registry logic so future PRs can
extend coverage (per-jarr-particle entries, additional Andalusian
attestations, etc.) without touching the class definition.

Coverage rule: every non-UNRESOLVED `OperatorTriggerFamily` MUST have at
least one entry. Multiple entries per family are not only allowed but
expected — the registry preserves competition (e.g. INNA / ANNA / KAANNA /
LAKINNA / LAYTA / LAALLA all attest `POSSIBLE_NASIKH_INNA_FAMILY`).

This module does NOT decide which entry "wins"; it only declares which
entries exist.
"""

from __future__ import annotations

from dal_core.nahw_operator_registry import (
    ActivationCondition,
    BlockingCondition,
    CaseEffectPolicyFamily,
    Citation,
    ExpectedRelationFamily,
    NahwOperatorEntry,
    NahwSchool,
    OperatorInputSignature,
    OperatorSource,
)
from dal_core.operator_trigger import OperatorTriggerFamily
from dal_core.ranks import LughaRank


def _entry(
    operator_id: str,
    display_name_ar: str,
    family: OperatorTriggerFamily,
    expected_relations: tuple[ExpectedRelationFamily, ...],
    case_policies: tuple[CaseEffectPolicyFamily, ...],
    *,
    arity: int = 1,
    neighbour_types: tuple[str, ...] = (),
    activation: tuple[ActivationCondition, ...] = (),
    blocking: tuple[BlockingCondition, ...] = (),
    source: OperatorSource = OperatorSource.QURAN,
    school: NahwSchool = NahwSchool.SHARED,
    rank: LughaRank = LughaRank.TAWATUR,
    reference: str = "kalaam_arab",
    note: str = "",
) -> NahwOperatorEntry:
    """Local factory keeping per-entry definitions concise and uniform."""
    return NahwOperatorEntry(
        operator_id=operator_id,
        display_name_ar=display_name_ar,
        source=source,
        school=school,
        rank=rank,
        family=family,
        input_signature=OperatorInputSignature(
            expected_arity=arity,
            expected_neighbour_types=neighbour_types,
            notes=note,
        ),
        activation_conditions=activation,
        blocking_conditions=blocking,
        expected_relation_families=expected_relations,
        case_effect_policy_families=case_policies,
        citations=(Citation(source=source, reference=reference, note=note),),
        entry_residuals=(),
        entry_trace_id=f"nahw-registry-{operator_id.lower()}",
    )


def build_seed_entries() -> tuple[NahwOperatorEntry, ...]:
    """Return the default seed entry tuple."""

    entries: list[NahwOperatorEntry] = []

    # -----------------------------------------------------------------
    # POSSIBLE_JARR_OPERATOR_FAMILY — حروف الجر
    # -----------------------------------------------------------------
    jarr_specs = [
        ("HARF_JARR_MIN", "مِنْ"),
        ("HARF_JARR_ILA", "إلى"),
        ("HARF_JARR_AN", "عَنْ"),
        ("HARF_JARR_FI", "في"),
        ("HARF_JARR_BA", "الباء"),
        ("HARF_JARR_LAM", "اللام"),
        ("HARF_JARR_KAF", "الكاف"),
        ("HARF_JARR_ALA", "على"),
    ]
    for op_id, name_ar in jarr_specs:
        entries.append(
            _entry(
                operator_id=op_id,
                display_name_ar=name_ar,
                family=OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
                expected_relations=(ExpectedRelationFamily.TAQYID_LIKE,),
                case_policies=(CaseEffectPolicyFamily.JARR_POLICY_FAMILY,),
                arity=1,
                neighbour_types=("ISM_COMMON",),
                activation=(ActivationCondition.IMMEDIATELY_PRECEDES_ISM,),
                source=OperatorSource.KALAAM_ARAB,
                reference="kalaam_arab/huruf_al_jarr",
            )
        )

    # -----------------------------------------------------------------
    # POSSIBLE_NASB_OPERATOR_FAMILY — نواصب الفعل المضارع
    # -----------------------------------------------------------------
    nasb_specs = [
        ("AN_MASDARIYYA", "أَنْ"),
        ("LAN", "لَنْ"),
        ("KAY", "كَيْ"),
        ("IDHAN", "إِذَنْ"),
    ]
    for op_id, name_ar in nasb_specs:
        entries.append(
            _entry(
                operator_id=op_id,
                display_name_ar=name_ar,
                family=OperatorTriggerFamily.POSSIBLE_NASB_OPERATOR_FAMILY,
                expected_relations=(ExpectedRelationFamily.TADMN_LIKE,),
                case_policies=(CaseEffectPolicyFamily.NASB_POLICY_FAMILY,),
                arity=1,
                neighbour_types=("FIIL_MUDARI",),
                activation=(ActivationCondition.IMMEDIATELY_PRECEDES_FIIL_MUDARI,),
                source=OperatorSource.KALAAM_ARAB,
                reference="kalaam_arab/nawasib",
            )
        )

    # -----------------------------------------------------------------
    # POSSIBLE_JAZM_OPERATOR_FAMILY — جوازم الفعل المضارع
    # -----------------------------------------------------------------
    jazm_specs = [
        ("LAM_JAAZIMA", "لَمْ"),
        ("LAMMA", "لَمَّا"),
        ("LA_NAHIYA", "لا الناهية"),
        ("LAM_AMR", "لام الأمر"),
    ]
    for op_id, name_ar in jazm_specs:
        entries.append(
            _entry(
                operator_id=op_id,
                display_name_ar=name_ar,
                family=OperatorTriggerFamily.POSSIBLE_JAZM_OPERATOR_FAMILY,
                expected_relations=(ExpectedRelationFamily.TADMN_LIKE,),
                case_policies=(CaseEffectPolicyFamily.JAZM_POLICY_FAMILY,),
                arity=1,
                neighbour_types=("FIIL_MUDARI",),
                activation=(ActivationCondition.IMMEDIATELY_PRECEDES_FIIL_MUDARI,),
                source=OperatorSource.KALAAM_ARAB,
                reference="kalaam_arab/jawazim",
            )
        )

    # -----------------------------------------------------------------
    # POSSIBLE_NASIKH_INNA_FAMILY — إنّ وأخواتها
    # -----------------------------------------------------------------
    inna_specs = [
        ("INNA", "إِنَّ"),
        ("ANNA", "أَنَّ"),
        ("KAANNA", "كَأَنَّ"),
        ("LAKINNA", "لَكِنَّ"),
        ("LAYTA", "لَيْتَ"),
        ("LAALLA", "لَعَلَّ"),
    ]
    for op_id, name_ar in inna_specs:
        entries.append(
            _entry(
                operator_id=op_id,
                display_name_ar=name_ar,
                family=OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY,
                expected_relations=(ExpectedRelationFamily.ISN_LIKE,),
                case_policies=(
                    CaseEffectPolicyFamily.MIXED_RAFI_NASB_POLICY_FAMILY,
                ),
                arity=2,
                neighbour_types=("ISM_COMMON",),
                activation=(
                    ActivationCondition.HEADS_NOMINAL_FRAME,
                    ActivationCondition.IMMEDIATELY_PRECEDES_ISM,
                ),
                source=OperatorSource.KALAAM_ARAB,
                reference="kalaam_arab/inna_wa_akhawatuha",
            )
        )

    # -----------------------------------------------------------------
    # POSSIBLE_NASIKH_LA_LILJINS_FAMILY — لا النافية للجنس
    # -----------------------------------------------------------------
    entries.append(
        _entry(
            operator_id="LA_NAFI_LILJINS",
            display_name_ar="لا النافية للجنس",
            family=OperatorTriggerFamily.POSSIBLE_NASIKH_LA_LILJINS_FAMILY,
            expected_relations=(ExpectedRelationFamily.ISN_LIKE,),
            case_policies=(
                CaseEffectPolicyFamily.MIXED_RAFI_NASB_POLICY_FAMILY,
            ),
            arity=2,
            neighbour_types=("ISM_COMMON",),
            activation=(
                ActivationCondition.HEADS_NOMINAL_FRAME,
                ActivationCondition.IMMEDIATELY_PRECEDES_ISM,
            ),
            source=OperatorSource.KALAAM_ARAB,
            reference="kalaam_arab/la_an_nafiya_liljins",
        )
    )

    # -----------------------------------------------------------------
    # POSSIBLE_NIDA_FAMILY — حروف النداء
    # -----------------------------------------------------------------
    nida_specs = [
        ("YA", "يا"),
        ("AYYUHA", "أيُّها"),
        ("AYYATUHA", "أيَّتُها"),
        ("HAYYA", "هَيَّا"),
    ]
    for op_id, name_ar in nida_specs:
        entries.append(
            _entry(
                operator_id=op_id,
                display_name_ar=name_ar,
                family=OperatorTriggerFamily.POSSIBLE_NIDA_FAMILY,
                expected_relations=(ExpectedRelationFamily.NIDA_LIKE,),
                case_policies=(CaseEffectPolicyFamily.NASB_POLICY_FAMILY,),
                arity=1,
                neighbour_types=("ISM_COMMON",),
                activation=(ActivationCondition.IMMEDIATELY_PRECEDES_ISM,),
                source=OperatorSource.KALAAM_ARAB,
                reference="kalaam_arab/huruf_an_nida",
            )
        )

    # -----------------------------------------------------------------
    # POSSIBLE_ATF_FAMILY — حروف العطف
    # -----------------------------------------------------------------
    atf_specs = [
        ("WAW_ATF", "الواو"),
        ("FA_ATF", "الفاء"),
        ("THUMMA", "ثُمَّ"),
        ("AW", "أَوْ"),
        ("AM", "أَمْ"),
    ]
    for op_id, name_ar in atf_specs:
        entries.append(
            _entry(
                operator_id=op_id,
                display_name_ar=name_ar,
                family=OperatorTriggerFamily.POSSIBLE_ATF_FAMILY,
                expected_relations=(ExpectedRelationFamily.ATF_LIKE,),
                case_policies=(
                    CaseEffectPolicyFamily.NO_CASE_EFFECT_POLICY_FAMILY,
                ),
                arity=2,
                activation=(ActivationCondition.ADJACENT_TO_ANOTHER_ISM,),
                source=OperatorSource.KALAAM_ARAB,
                reference="kalaam_arab/huruf_al_atf",
            )
        )

    # -----------------------------------------------------------------
    # POSSIBLE_NAFI_FAMILY — حروف النفي
    # -----------------------------------------------------------------
    nafi_specs = [
        ("MA_NAFIYA", "ما النافية"),
        ("LA_NAFIYA", "لا النافية"),
        ("LAYSA", "ليس"),
    ]
    for op_id, name_ar in nafi_specs:
        entries.append(
            _entry(
                operator_id=op_id,
                display_name_ar=name_ar,
                family=OperatorTriggerFamily.POSSIBLE_NAFI_FAMILY,
                expected_relations=(ExpectedRelationFamily.TADMN_LIKE,),
                case_policies=(
                    CaseEffectPolicyFamily.NO_CASE_EFFECT_POLICY_FAMILY,
                ),
                arity=1,
                source=OperatorSource.KALAAM_ARAB,
                reference="kalaam_arab/huruf_an_nafi",
            )
        )

    # -----------------------------------------------------------------
    # POSSIBLE_ISTIFHAM_FAMILY — أدوات الاستفهام
    # -----------------------------------------------------------------
    istifham_specs = [
        ("HAL", "هل"),
        ("HAMZA_ISTIFHAM", "الهمزة"),
        ("MAN", "مَنْ"),
        ("MA_ISTIFHAM", "ما"),
        ("KAYFA", "كيف"),
        ("AYNA", "أين"),
        ("MATA", "متى"),
    ]
    for op_id, name_ar in istifham_specs:
        entries.append(
            _entry(
                operator_id=op_id,
                display_name_ar=name_ar,
                family=OperatorTriggerFamily.POSSIBLE_ISTIFHAM_FAMILY,
                expected_relations=(
                    ExpectedRelationFamily.UNRESOLVED_EXPECTED_RELATION,
                ),
                case_policies=(
                    CaseEffectPolicyFamily.NO_CASE_EFFECT_POLICY_FAMILY,
                ),
                arity=1,
                activation=(ActivationCondition.LEADS_FRAME,),
                source=OperatorSource.KALAAM_ARAB,
                reference="kalaam_arab/adawat_al_istifham",
            )
        )

    # -----------------------------------------------------------------
    # POSSIBLE_VERBAL_GOVERNANCE_FAMILY — الفعل عاملٌ عامًّا
    # -----------------------------------------------------------------
    entries.append(
        _entry(
            operator_id="FIIL_GOVERNANCE_GENERIC",
            display_name_ar="الفعل (حوكمة عامة)",
            family=OperatorTriggerFamily.POSSIBLE_VERBAL_GOVERNANCE_FAMILY,
            expected_relations=(
                ExpectedRelationFamily.ISN_LIKE,
                ExpectedRelationFamily.TADMN_LIKE,
            ),
            case_policies=(
                CaseEffectPolicyFamily.MIXED_RAFI_NASB_POLICY_FAMILY,
            ),
            arity=2,
            activation=(ActivationCondition.HEADS_VERBAL_FRAME,),
            source=OperatorSource.KALAAM_ARAB,
            reference="kalaam_arab/al_fi3l_3amilun",
            note=(
                "Documented family-level entry, not a specific verb. "
                "Specific verb governance is resolved later by valency."
            ),
        )
    )

    # -----------------------------------------------------------------
    # POSSIBLE_IBTIDAA_FAMILY — عامل الابتداء (معنوي)
    # -----------------------------------------------------------------
    entries.append(
        _entry(
            operator_id="IBTIDAA_OPERATOR",
            display_name_ar="عامل الابتداء",
            family=OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY,
            expected_relations=(ExpectedRelationFamily.ISN_LIKE,),
            case_policies=(CaseEffectPolicyFamily.RAFI_POLICY_FAMILY,),
            arity=1,
            activation=(ActivationCondition.HEADS_NOMINAL_FRAME,),
            source=OperatorSource.KALAAM_ARAB,
            reference="kalaam_arab/al_ibtidaa",
            note="Abstract (ma'nawi) operator, not a lexical particle.",
        )
    )

    # -----------------------------------------------------------------
    # POSSIBLE_IDAFA_FAMILY — عامل الإضافة (إنشائي فقط)
    # NO case-effect policy — case-effect of mudaf-ilayh belongs to a
    # later layer; the IDAFA entry is construction-trigger only.
    # -----------------------------------------------------------------
    entries.append(
        _entry(
            operator_id="IDAFA_CONSTRUCTION_OPERATOR",
            display_name_ar="عامل الإضافة (إنشائي)",
            family=OperatorTriggerFamily.POSSIBLE_IDAFA_FAMILY,
            expected_relations=(ExpectedRelationFamily.IDAFA_LIKE,),
            case_policies=(
                CaseEffectPolicyFamily.NO_CASE_EFFECT_POLICY_FAMILY,
            ),
            arity=2,
            neighbour_types=("ISM_COMMON",),
            activation=(ActivationCondition.ADJACENT_TO_ANOTHER_ISM,),
            source=OperatorSource.KALAAM_ARAB,
            reference="kalaam_arab/al_idafa",
            note=(
                "Construction-trigger only. Does NOT assert jarr-judgment "
                "on the mudaf-ilayh; that belongs to a later stage."
            ),
        )
    )

    return tuple(entries)
