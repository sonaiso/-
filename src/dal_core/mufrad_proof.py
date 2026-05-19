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
from typing import Optional

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

    # Composition readiness
    composition_readiness: CompositionReadiness = CompositionReadiness.NOT_READY

    # Proof metadata
    rank: LughaRank = LughaRank.ZERO
    residuals: tuple[Residual, ...] = field(default_factory=tuple)
    trace: dict = field(default_factory=dict)

    # Competing analyses
    competitors: tuple["MufradProof", ...] = field(default_factory=tuple)

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
