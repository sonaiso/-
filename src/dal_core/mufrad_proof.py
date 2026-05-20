"""
MufradProof Contract (عقد برهان المفرد)

Composition-ready closed signifier with complete morphological and surface proof.

CRITICAL PRINCIPLE:
Before moving to تركيب/syntax, the Arabic singular signifier must be closed
as a جامع مانع مفردي proof object.

Syntax layer works ONLY on MufradProof, not on:
- Raw tokens
- DForm
- DType
- DClosed (basic)

Because: D_mufrad هو أساس أرقام التركيب
"""

from dataclasses import dataclass, field
from typing import Optional, Union

from dal_core.d_form import FormCandidate
from dal_core.d_lugha import LughaAttestation
from dal_core.d_type import TypedDal, DalType
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual, ResidualType, ResidualSeverity, has_blocking_residuals
from dal_core.evidence import Evidence
from dal_core.morph_features import (
    SegmentationProof,
    StemProof,
    CliticProof,
    RootCandidate,
    WaznCandidate,
    CandidateStatus,
    VerbFeatureProof,
    NounInflectionClass,
    ParticleOperatorPotential,
)
from dal_core.surface_effects import SurfaceEffect
from dal_core.composition_readiness import CompositionReadiness
from dal_core.case_signs import CaseSignPotential
from dal_core.mufrad_axes import (
    BinaaJudgment,
    BinaaSubtype,
    IshtiqaqJudgment,
    JamidSubtype,
    MushtaqSubtype,
    SarfFlexibility,
)


@dataclass(frozen=True)
class MufradProof:
    """
    برهان المفرد (MufradProof)

    Composition-ready singular word proof with complete morphological
    and surface analysis.

    ALLOWED FIELDS:
    - Morphological features (as governed candidates)
    - Surface effects (visible/estimated marks)
    - Case potential (capacity to receive case)
    - Inflection potential (capacity to inflect)

    FORBIDDEN FIELDS:
    - meaning, semantic, madlul, murad, haqiqa_majaz
    - Syntax roles (faail, mafool, mubtada, khabar, etc)
    - Case effects (marfoo_by, mansub_by, majroor_by)
    - Operator governance (governed_by_operator)

    COMPOSITION THEOREMS:
    1. No composition before MufradProof
    2. SurfaceEffect belongs to MufradProof
    3. CaseEffect does not enter MufradProof
    4. MorphFeatures belong as candidates
    5. SyntaxRole does not enter MufradProof
    6. Operators work on MufradProof only
    7. Composition never raises MufradProof rank
    8. Composition inherits MufradProof residuals
    9. No certificate with incomplete MufradProof
    10. No certificate with unresolved competitors
    """

    # Core dal-mufrad data (required)
    form: FormCandidate
    lugha: LughaAttestation
    type: TypedDal

    # Morphological proof (required for composition)
    segmentation: SegmentationProof
    stem: StemProof
    clitics: tuple[CliticProof, ...]

    # Root and pattern candidates (may have competition)
    root_candidates: tuple[RootCandidate, ...]
    wazn_candidates: tuple[WaznCandidate, ...]

    # Morphological feature status
    derivation_status: CandidateStatus
    jamid_mushtaq_status: CandidateStatus
    mabni_murab_status: CandidateStatus
    definiteness_status: CandidateStatus
    gender_status: CandidateStatus
    number_status: CandidateStatus

    # Type-specific features
    verb_features: Optional[VerbFeatureProof] = None
    noun_inflection_class: Optional[NounInflectionClass] = None
    particle_operator_potential: Optional[ParticleOperatorPotential] = None

    # Surface effects (ALLOWED)
    surface_effects: tuple[SurfaceEffect, ...] = field(default_factory=tuple)

    # Case sign potentials (ALLOWED - these are observations, not effects)
    case_sign_potentials: tuple[CaseSignPotential, ...] = field(default_factory=tuple)

    # Composition readiness
    composition_readiness: CompositionReadiness = CompositionReadiness.NOT_READY

    # Proof metadata
    rank: LughaRank = LughaRank.ZERO
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)

    # Competing analyses
    competitors: tuple["MufradProof", ...] = field(default_factory=tuple)

    # =========================================================================
    # Classified mufrad axes (PR-E)
    # =========================================================================
    #
    # These supersede the certainty-only ``mabni_murab_status`` and
    # ``jamid_mushtaq_status`` fields above. They carry actual values
    # (MABNI vs MUERAB; JAMID vs MUSHTAQ; subtype) plus the orthogonal
    # sarf-flexibility axis. All default to UNRESOLVED / NOT_APPLICABLE so
    # existing constructors continue to work unchanged.
    #
    # Architectural invariant (enforced in ``__post_init__``):
    #   - If ``binaa_judgment`` is MABNI/MUERAB, the field must be a
    #     ``BinaaJudgment``, not a string.
    #   - If ``ishtiqaq_judgment`` is JAMID/MUSHTAQ, ``ishtiqaq_subtype``
    #     must be a typed subtype (JamidSubtype or MushtaqSubtype).
    # Cross-axis consistency:
    #   - HARF ⇒ ishtiqaq_judgment must be NOT_APPLICABLE.
    #   - FIIL ⇒ ishtiqaq_judgment must be NOT_APPLICABLE.

    binaa_judgment: BinaaJudgment = BinaaJudgment.UNRESOLVED
    """Axis 3 — classified binaa/i'rab judgment."""

    binaa_subtype: Optional[BinaaSubtype] = None
    """Axis 3 — surface subtype (sukun/fath/damm/kasr/invariant). Only
    meaningful when ``binaa_judgment == MABNI``."""

    ishtiqaq_judgment: IshtiqaqJudgment = IshtiqaqJudgment.UNRESOLVED
    """Axis 4 — classified ishtiqaq/jamid judgment."""

    ishtiqaq_subtype: Optional[Union[JamidSubtype, MushtaqSubtype]] = None
    """Axis 4 — subtype (mushtaq-class or jamid-class). Only meaningful
    when ``ishtiqaq_judgment in {JAMID, MUSHTAQ}``."""

    sarf_flexibility: SarfFlexibility = SarfFlexibility.NOT_APPLICABLE
    """Auxiliary axis — distinguishes ``munassarif`` from
    ``mamnu_min_sarf`` for MUERAB nouns. ``NOT_APPLICABLE`` for particles,
    verbs, and MABNI nouns."""

    def __post_init__(self):
        """Validate MufradProof constraints"""
        # Ensure no semantic leak
        forbidden_attrs = {"meaning", "murad", "madlul", "haqiqa_majaz", "semantic"}
        for attr in forbidden_attrs:
            if hasattr(self, attr):
                raise ValueError(f"MufradProof must not have '{attr}' field")

        # Ensure no syntax role leak
        forbidden_syntax = {
            "faail", "mafool", "mubtada", "khabar", "syntax_role",
            "subject", "object", "agent", "patient",
            "hal", "tamyiz", "badal", "naat", "mudaf_ilayh",
        }
        for attr in forbidden_syntax:
            if hasattr(self, attr):
                raise ValueError(f"MufradProof must not have syntax role '{attr}'")

        # Ensure no case effect leak
        forbidden_case = {
            "case_effect", "marfoo_by", "mansub_by", "majroor_by",
            "governed_by_operator", "governed_by",
        }
        for attr in forbidden_case:
            if hasattr(self, attr):
                raise ValueError(f"MufradProof must not have case effect '{attr}'")

        # ------------------------------------------------------------------
        # Axis consistency checks (PR-E)
        # ------------------------------------------------------------------
        # When a judgment carries a value, its subtype field must use the
        # corresponding typed enum, never a string. This blocks the kind
        # of free-form leakage that produced the original hallucination.

        if self.binaa_judgment == BinaaJudgment.MABNI:
            if self.binaa_subtype is not None and not isinstance(
                self.binaa_subtype, BinaaSubtype
            ):
                raise ValueError(
                    "binaa_subtype must be a BinaaSubtype when binaa_judgment is MABNI"
                )
        elif self.binaa_judgment in (BinaaJudgment.MUERAB, BinaaJudgment.NOT_APPLICABLE):
            if self.binaa_subtype is not None:
                raise ValueError(
                    f"binaa_subtype must be None when binaa_judgment is {self.binaa_judgment}"
                )

        if self.ishtiqaq_judgment == IshtiqaqJudgment.MUSHTAQ:
            if self.ishtiqaq_subtype is not None and not isinstance(
                self.ishtiqaq_subtype, MushtaqSubtype
            ):
                raise ValueError(
                    "ishtiqaq_subtype must be a MushtaqSubtype when ishtiqaq_judgment is MUSHTAQ"
                )
        elif self.ishtiqaq_judgment == IshtiqaqJudgment.JAMID:
            if self.ishtiqaq_subtype is not None and not isinstance(
                self.ishtiqaq_subtype, JamidSubtype
            ):
                raise ValueError(
                    "ishtiqaq_subtype must be a JamidSubtype when ishtiqaq_judgment is JAMID"
                )
        elif self.ishtiqaq_judgment == IshtiqaqJudgment.NOT_APPLICABLE:
            if self.ishtiqaq_subtype is not None:
                raise ValueError(
                    "ishtiqaq_subtype must be None when ishtiqaq_judgment is NOT_APPLICABLE"
                )

    def is_composition_ready(self) -> bool:
        """Check if ready for any level of composition"""
        return self.composition_readiness.allows_composition()

    def can_issue_certificate(self) -> bool:
        """Check if can participate in certificate-level composition"""
        return (
            self.composition_readiness.allows_certificate() and
            not has_blocking_residuals(list(self.residuals)) and
            len(self.competitors) == 0 and
            self.rank >= LughaRank.SAMA
        )

    def has_unresolved_competitors(self) -> bool:
        """Check if competing analyses remain unresolved"""
        return len(self.competitors) > 0

    def get_weakest_rank(self) -> LughaRank:
        """
        Get weakest rank across all features (weakest-link principle).

        Theorem 7: Composition rank cannot exceed MufradProof rank.
        """
        ranks = [
            self.form.rank.value if hasattr(self.form.rank, 'value') else 1,
            self.lugha.rank.value,
            self.segmentation.rank.value,
            self.stem.rank.value,
        ]

        # Include clitic ranks
        ranks.extend(c.rank.value for c in self.clitics)

        # Include root/wazn candidate ranks
        ranks.extend(r.rank.value for r in self.root_candidates)
        ranks.extend(w.rank.value for w in self.wazn_candidates)

        # Include surface effect ranks
        ranks.extend(e.rank.value for e in self.surface_effects)

        # Include type-specific feature ranks
        if self.verb_features:
            ranks.append(self.verb_features.rank.value)
        if self.noun_inflection_class:
            ranks.append(self.noun_inflection_class.rank.value)
        if self.particle_operator_potential:
            ranks.append(self.particle_operator_potential.rank.value)

        min_rank_value = min(ranks)
        return LughaRank(min_rank_value)

    def collect_all_residuals(self) -> tuple[Residual, ...]:
        """
        Collect all residuals from all components.

        Theorem 8: Composition must inherit all MufradProof residuals.
        """
        all_residuals = list(self.residuals)

        # Form/lugha/type residuals
        all_residuals.extend(self.form.residuals)
        all_residuals.extend(self.lugha.residuals)
        all_residuals.extend(self.type.residuals)

        # Morph proof residuals
        all_residuals.extend(self.segmentation.residuals)
        all_residuals.extend(self.stem.residuals)
        for clitic in self.clitics:
            all_residuals.extend(clitic.residuals)

        # Candidate residuals
        for root in self.root_candidates:
            all_residuals.extend(root.residuals)
        for wazn in self.wazn_candidates:
            all_residuals.extend(wazn.residuals)

        # Surface effect residuals
        for effect in self.surface_effects:
            all_residuals.extend(effect.residuals)

        # Type-specific residuals
        if self.verb_features:
            all_residuals.extend(self.verb_features.residuals)
        if self.noun_inflection_class:
            all_residuals.extend(self.noun_inflection_class.residuals)
        if self.particle_operator_potential:
            all_residuals.extend(self.particle_operator_potential.residuals)

        return tuple(all_residuals)

    def __str__(self) -> str:
        readiness = self.composition_readiness.value
        return f"MufradProof({self.form.vocalization}, {readiness})"

    def to_presyntax_vector(self) -> "PreSyntaxMufradVector":
        """
        Export MufradProof to PreSyntaxMufradVector.

        This is the ONLY interface that nahw operators may consume.

        The vector contains:
        - Type identification codes
        - Morphological feature summary
        - Surface effects
        - Case sign potentials (NOT case effects)
        - Rank and residuals
        - Composition readiness

        It does NOT contain:
        - meaning, semantic, murad
        - syntax roles
        - case effects
        """
        from dal_core.presyntax_vector import PreSyntaxMufradVector
        from dal_core.type_ids import NounTypeID, VerbTypeID, ParticleTypeID

        # Determine type_id from type value
        type_id: NounTypeID | VerbTypeID | ParticleTypeID | None = None

        # This is a stub - in full implementation, type_id would be
        # determined from detailed morphological analysis
        # For now, we leave it as None (unresolved)

        # Generate unique ID
        mufrad_id = f"mufrad_{id(self)}"

        # Get span from form if available
        raw_span = (0, len(self.form.vocalization))

        # Get weakest rank
        morph_rank = self.get_weakest_rank()
        final_rank = self.rank if self.rank != LughaRank.ZERO else morph_rank

        # Collect all residuals
        all_residuals = self.collect_all_residuals()

        # Generate trace ID
        trace_id = self.trace.get("id", f"trace_{id(self)}")

        # Count competitors
        competitors_count = len(self.competitors)

        return PreSyntaxMufradVector(
            mufrad_id=mufrad_id,
            raw_span=raw_span,
            type_value=self.type.dal_type.value,
            type_id=type_id,
            type_rank=self.type.rank,
            mabni_murab_status=self.mabni_murab_status,
            noun_inflection_class=self.noun_inflection_class,
            verb_features=self.verb_features,
            particle_operator_potential=self.particle_operator_potential,
            surface_effects=self.surface_effects,
            case_sign_potentials=self.case_sign_potentials,
            morph_rank=morph_rank,
            final_rank=final_rank,
            residuals=all_residuals,
            trace_id=trace_id,
            competitors_count=competitors_count,
            composition_readiness=self.composition_readiness,
        )


def verify_no_semantic_leak(proof: MufradProof) -> list[Residual]:
    """
    Verify MufradProof contains no semantic meaning fields.

    Returns list of blocker residuals if leaks detected.
    """
    residuals = []
    forbidden = {"meaning", "murad", "madlul", "haqiqa_majaz", "semantic"}

    for attr in forbidden:
        if hasattr(proof, attr):
            residuals.append(Residual(
                type=ResidualType.DAL_SEMANTIC_LEAK,
                severity=ResidualSeverity.BLOCKER,
                message=f"Semantic leak detected: '{attr}' field in MufradProof",
                location="MufradProof"
            ))

    # Check in trace/metadata
    if isinstance(proof.trace, dict):
        for key in proof.trace.keys():
            if key in forbidden:
                residuals.append(Residual(
                    type=ResidualType.DAL_SEMANTIC_LEAK,
                    severity=ResidualSeverity.BLOCKER,
                    message=f"Semantic leak in trace: '{key}'",
                    location="MufradProof.trace"
                ))

    return residuals


def verify_no_syntax_role_leak(proof: MufradProof) -> list[Residual]:
    """
    Verify MufradProof contains no syntax role fields.

    Returns list of blocker residuals if leaks detected.
    """
    residuals = []
    forbidden = {
        "faail", "mafool", "mubtada", "khabar", "syntax_role",
        "subject", "object", "agent", "patient",
        "hal", "tamyiz", "badal", "naat", "mudaf_ilayh",
    }

    for attr in forbidden:
        if hasattr(proof, attr):
            residuals.append(Residual(
                type=ResidualType.SYNTAX_ROLE_LEAK_IN_MUFRAD,
                severity=ResidualSeverity.BLOCKER,
                message=f"Syntax role leak: '{attr}' in MufradProof",
                location="MufradProof"
            ))

    return residuals


def verify_no_case_effect_leak(proof: MufradProof) -> list[Residual]:
    """
    Verify MufradProof contains no case effect fields.

    Returns list of blocker residuals if leaks detected.
    """
    residuals = []
    forbidden = {
        "case_effect", "marfoo_by", "mansub_by", "majroor_by",
        "governed_by_operator", "governed_by",
    }

    for attr in forbidden:
        if hasattr(proof, attr):
            residuals.append(Residual(
                type=ResidualType.CASE_EFFECT_LEAK_IN_MUFRAD,
                severity=ResidualSeverity.BLOCKER,
                message=f"Case effect leak: '{attr}' in MufradProof",
                location="MufradProof"
            ))

    return residuals
