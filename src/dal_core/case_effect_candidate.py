"""
Case Effect Candidate (مرشح الأثر الإعرابي)

PR #160/#161: Post-operator-candidate, pre-relation applied-effect layer.

ARCHITECTURE POSITION:
    OperatorCandidate + FactorMarkEquation + CaseSignMatrixRow
            ↓
    CaseEffectCandidate                          (this module — typed case effect candidates)
            ↓
    [future] AmilMamulEquation
          → RoleEquation
          → ParseCompetition

DEFERRED COMPONENTS (PR #161):
    RelationCandidate is NOT yet consumed at this layer. The case effect candidate
    is built from OperatorCandidate + FactorMarkEquation + CaseSignMatrixRow only.
    RelationCandidate integration is deferred to AmilMamulEquation layer where
    relation types (ISN/TADMN/TAQYID) are needed to determine final case effects.

GOVERNING RULES (do NOT relax):
1. Inputs are ONLY OperatorCandidate, FactorMarkEquation, and CaseSignMatrixRow.
   RelationCandidate is deferred to AmilMamulEquation layer. All must be typed.
   Anything else raises TypeError.
2. Output is a *candidate case effect* NEVER:
     - a final case judgment (no marfoo/mansub/majroor/majzum without _candidate suffix),
     - a syntax role (no faail/mafool/mubtada/khabar without _candidate suffix),
     - a semantic meaning (no meaning/murad/madlul/haqiqa/majaz),
     - a final ifadah (no ifadah_complete/pragmatic_completion),
     - a final hukm (no hukm_final/judgment_complete).
3. Every CaseEffectCandidate must preserve:
     - operator identity (via OperatorCandidate)
     - factor identity (via FactorMarkEquation.factor_source)
     - affected identity (via FactorMarkEquation.affected_vector)
     - mark compatibility (via CaseSignMatrixRow)
4. Case effect policy families are READ from NahwOperatorEntry but NOT applied as
   final judgment. They inform the candidate type only.
5. Competing candidates are PRESERVED, never silently resolved.
6. Rank ceiling extends: case_effect.rank ≤ min(operator.rank, factor_equation.rank,
   matrix_row.rank).
7. Residual inheritance extends: case_effect.inherited_residuals ⊇
   operator.get_all_residuals() ⊇ trigger.get_all_residuals() ⊇
   matrix.get_all_residuals() ⊇ frame.get_all_residuals().
8. Every governance residual is a member of the central ResidualType taxonomy.
9. For missing mark or incompatible compatibility, produce:
   - EstimatedEffectCandidate (if mark estimated/hidden)
   - DeferredEffectCandidate (if mark missing)
   - BlockedEffectCandidate (if compatibility conflict)

Constitutional Law:
    CaseEffectCandidate يرشح الأثر ولا يحكم بالإعراب
    (CaseEffectCandidate proposes the effect, does NOT judge the i'rab)

    لا case_effect نهائي
    لا marfoo_by/mansub_by/majroor_by نهائي
    لا faail/mafool/mubtada/khabar نهائي
    لا meaning/ifadah/hukm

Created: 2026-05-30
Updated: 2026-05-30 (PR #161 hardening)
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import uuid

from dal_core.case_sign_matrix import CaseCompatibilityFamily, CaseSignMatrixRow
from dal_core.factor_mark_equation import (
    FactorMarkEquation,
    FactorMarkEquationType,
    FactorSourceCandidate,
)
from dal_core.nahw_operator_registry import (
    CaseEffectPolicyFamily,
    NahwOperatorEntry,
)
from dal_core.operator_candidate import OperatorCandidate
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.ranks import LughaRank
from dal_core.residuals import (
    Residual,
    ResidualType,
    make_blocker,
    make_info,
    make_warning,
)


# ---------------------------------------------------------------------------
# Forbidden field names (defensive governance)
# ---------------------------------------------------------------------------

_FORBIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "marfoo",  # without _candidate
        "mansub",  # without _candidate
        "majrur",  # without _candidate
        "majroor",  # without _candidate
        "majzum",  # without _candidate
        "majzoom",  # without _candidate
        "marfoo_by_final",
        "mansub_by_final",
        "majroor_by_final",
        "majzum_by_final",
        "case_effect_final",
        "case_judgment_final",
        "faail",  # without _candidate
        "mafool",  # without _candidate
        "mafool_bih",  # without _candidate
        "mubtada",  # without _candidate
        "khabar",  # without _candidate
        "syntax_role_final",
        "meaning",
        "semantic",
        "madlul",
        "murad",
        "haqiqa",
        "majaz",
        "ifadah",
        "ifadah_complete",
        "pragmatic_completion",
        "hukm",
        "hukm_final",
        "judgment",
        "judgment_complete",
        "grounding",
        "reality",
    }
)


# ---------------------------------------------------------------------------
# Case Effect Candidate Types
# ---------------------------------------------------------------------------


class CaseEffectCandidateType(Enum):
    """
    نوع مرشح الأثر الإعرابي

    Classification of case effect candidate types.

    These are CANDIDATES, not final judgments.
    """

    RAFʿ_EFFECT_CANDIDATE = "raf_effect_candidate"
    """Raf' (nominative) effect candidate"""

    NASB_EFFECT_CANDIDATE = "nasb_effect_candidate"
    """Nasb (accusative) effect candidate"""

    JARR_EFFECT_CANDIDATE = "jarr_effect_candidate"
    """Jarr (genitive) effect candidate"""

    JAZM_EFFECT_CANDIDATE = "jazm_effect_candidate"
    """Jazm (jussive) effect candidate"""

    BUILDING_EFFECT_CANDIDATE = "building_effect_candidate"
    """Building (invariant) effect candidate (mabni)"""

    ESTIMATED_EFFECT_CANDIDATE = "estimated_effect_candidate"
    """Estimated/hidden mark effect candidate"""

    DEFERRED_EFFECT_CANDIDATE = "deferred_effect_candidate"
    """Deferred (mark missing or unresolved) effect candidate"""

    BLOCKED_EFFECT_CANDIDATE = "blocked_effect_candidate"
    """Blocked (compatibility conflict) effect candidate"""


# ---------------------------------------------------------------------------
# Case Effect Candidate Trace
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CaseEffectCandidateTrace:
    """
    أثر مرشح الأثر الإعرابي

    Minimal mandatory trace linking case effect candidate back to:
    - operator_candidate_id (from OperatorCandidate)
    - factor_equation_id (from FactorMarkEquation)
    - matrix_row_id (from CaseSignMatrixRow)
    - affected_vector_id (from PreSyntaxMufradVector)
    - trigger_id, frame_id, matrix_id (chain provenance)
    """

    case_effect_id: str
    """Unique identifier for this case effect candidate."""

    operator_candidate_id: str
    """OperatorCandidate.candidate_id this effect originated from."""

    factor_equation_id: str
    """FactorMarkEquation.equation_id this effect uses."""

    matrix_row_vector_id: str
    """CaseSignMatrixRow.vector_id (affected constituent)."""

    affected_vector_id: str
    """PreSyntaxMufradVector.mufrad_id (affected constituent)."""

    trigger_id: str
    """OperatorTriggerPotential.trigger_id (chain provenance)."""

    frame_id: str
    """SentenceFrameCandidate.frame_id (chain provenance)."""

    matrix_id: str
    """CaseSignMatrix.matrix_id (chain provenance)."""

    derivation: str = "from_operator_and_factor_mark_equation"
    """Fixed derivation marker."""

    def __post_init__(self) -> None:
        if not self.case_effect_id:
            raise ValueError("CaseEffectCandidateTrace.case_effect_id is required.")
        if not self.operator_candidate_id:
            raise ValueError(
                "CaseEffectCandidateTrace.operator_candidate_id is required."
            )
        if not self.factor_equation_id:
            raise ValueError(
                "CaseEffectCandidateTrace.factor_equation_id is required."
            )
        if not self.matrix_row_vector_id:
            raise ValueError(
                "CaseEffectCandidateTrace.matrix_row_vector_id is required."
            )
        if not self.affected_vector_id:
            raise ValueError(
                "CaseEffectCandidateTrace.affected_vector_id is required."
            )
        if not self.trigger_id:
            raise ValueError("CaseEffectCandidateTrace.trigger_id is required.")
        if not self.frame_id:
            raise ValueError("CaseEffectCandidateTrace.frame_id is required.")
        if not self.matrix_id:
            raise ValueError("CaseEffectCandidateTrace.matrix_id is required.")
        if self.derivation != "from_operator_and_factor_mark_equation":
            raise ValueError(
                "CaseEffectCandidateTrace.derivation must be "
                "'from_operator_and_factor_mark_equation'."
            )


# ---------------------------------------------------------------------------
# Case Effect Candidate
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CaseEffectCandidate:
    """
    مرشح الأثر الإعرابي

    A typed candidate for case effect application.

    This is NOT a final case judgment. This is NOT a final syntax role.
    It is a candidate saying: "This operator candidate, via this factor
    equation, with this mark compatibility, produces this case effect candidate."

    FORBIDDEN: No final marfoo/mansub/majroor/majzum, no final faail/mafool,
               no meaning, no ifadah, no hukm.
    REQUIRED: All case/role references must have _candidate suffix.

    Constitutional Law:
        Every field with case/role semantics MUST end in _candidate:
        - marfoo_candidate, mansub_candidate, majroor_candidate, majzum_candidate
        - faail_candidate, mafool_candidate, mubtada_candidate, khabar_candidate
        - ism_kana_candidate, khabar_kana_candidate, etc.
    """

    case_effect_id: str
    """Unique identifier for this case effect candidate."""

    operator_candidate_id: str
    """OperatorCandidate.candidate_id this effect originated from."""

    factor_equation_id: str
    """FactorMarkEquation.equation_id this effect uses."""

    trigger_id: str
    """OperatorTriggerPotential.trigger_id (chain provenance)."""

    frame_id: str
    """SentenceFrameCandidate.frame_id (chain provenance)."""

    matrix_id: str
    """CaseSignMatrix.matrix_id (chain provenance)."""

    effect_type: CaseEffectCandidateType
    """The candidate case effect type."""

    operator_candidate: OperatorCandidate
    """The specific OperatorCandidate this effect uses."""

    factor_source: FactorSourceCandidate
    """The factor source from FactorMarkEquation."""

    affected_vector: PreSyntaxMufradVector
    """The affected PreSyntaxMufradVector."""

    matrix_row: CaseSignMatrixRow
    """The matrix row with compatibility evidence."""

    factor_equation: FactorMarkEquation
    """The complete FactorMarkEquation."""

    compatibility_evidence: tuple[CaseCompatibilityFamily, ...]
    """Compatibility families from matrix row that support this effect."""

    policy_family: CaseEffectPolicyFamily
    """The case effect policy family from operator registry entry."""

    identity_ids: tuple[str, ...]
    """
    Linguistic identity IDs preserved through this case effect candidate.
    Aggregates identities from:
    - operator_candidate.registry_entry (operator identity)
    - factor_source.identity_ids (factor linguistic identities)
    - affected_vector.identity_ids (affected constituent identities)

    PR #161: Explicit identity preservation following PR #159 pattern.
    Constitutional Law: trace_id ≠ identity_id.
    """

    trace_ids: tuple[str, ...]
    """
    Provenance trace IDs linking back to computational chain.
    Aggregates traces from:
    - operator_candidate.trace (operator candidate trace)
    - factor_source.trace_ids (factor source traces)
    - affected_vector.trace_ids (affected constituent traces)
    - matrix_row trace (row trace_id as trace only, NOT identity)

    PR #161: Explicit trace tracking following PR #159 pattern.
    Constitutional Law: trace_id ≠ identity_id.
    """

    rank: LughaRank
    """
    Case effect candidate rank ceiling:
    rank ≤ min(operator.rank, factor_equation.rank, matrix_row.rank)
    """

    inherited_residuals: tuple[Residual, ...]
    """
    Residuals inherited from operator (which inherits from trigger, matrix, frame).
    Must include operator.get_all_residuals().
    """

    case_effect_residuals: tuple[Residual, ...]
    """Residuals specific to this case effect (e.g., compatibility mismatches)."""

    trace: CaseEffectCandidateTrace
    """Trace linking back to operator, factor equation, and matrix row."""

    produces_final_case_effect: bool = False
    """Whether this produces final case effect (ALWAYS False at this stage)."""

    produces_final_syntax_role: bool = False
    """Whether this produces final syntax role (ALWAYS False at this stage)."""

    produces_meaning: bool = False
    """Whether this produces meaning (ALWAYS False)."""

    produces_ifadah: bool = False
    """Whether this produces ifadah (ALWAYS False)."""

    produces_hukm: bool = False
    """Whether this produces hukm (ALWAYS False)."""

    def __post_init__(self) -> None:
        # Field-name leak check (defensive)
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        leaks = field_names & _FORBIDDEN_FIELDS
        if leaks:
            raise ValueError(
                f"CaseEffectCandidate contains forbidden fields: {leaks}. "
                f"The case effect candidate layer may only carry typed "
                f"candidate case effects, never final judgments, syntax roles, "
                f"or meaning."
            )

        # Required boolean false checks (constitutional law enforcement)
        if self.produces_final_case_effect is not False:
            raise ValueError(
                "CaseEffectCandidate.produces_final_case_effect must be False; "
                "this layer produces candidates only, not final case judgments."
            )
        if self.produces_final_syntax_role is not False:
            raise ValueError(
                "CaseEffectCandidate.produces_final_syntax_role must be False; "
                "this layer produces candidates only, not final syntax roles."
            )
        if self.produces_meaning is not False:
            raise ValueError(
                "CaseEffectCandidate.produces_meaning must be False; "
                "this layer never produces meaning."
            )
        if self.produces_ifadah is not False:
            raise ValueError(
                "CaseEffectCandidate.produces_ifadah must be False; "
                "this layer never produces ifadah."
            )
        if self.produces_hukm is not False:
            raise ValueError(
                "CaseEffectCandidate.produces_hukm must be False; "
                "this layer never produces hukm."
            )

        # Type checks
        if not self.case_effect_id:
            raise ValueError("CaseEffectCandidate.case_effect_id is required.")
        if not self.operator_candidate_id:
            raise ValueError("CaseEffectCandidate.operator_candidate_id is required.")
        if not self.factor_equation_id:
            raise ValueError("CaseEffectCandidate.factor_equation_id is required.")
        if not self.trigger_id:
            raise ValueError("CaseEffectCandidate.trigger_id is required.")
        if not self.frame_id:
            raise ValueError("CaseEffectCandidate.frame_id is required.")
        if not self.matrix_id:
            raise ValueError("CaseEffectCandidate.matrix_id is required.")

        if not isinstance(self.effect_type, CaseEffectCandidateType):
            raise TypeError(
                "CaseEffectCandidate.effect_type must be a "
                "CaseEffectCandidateType enum member; got "
                f"{type(self.effect_type).__name__}."
            )
        if not isinstance(self.operator_candidate, OperatorCandidate):
            raise TypeError(
                "CaseEffectCandidate.operator_candidate must be an "
                f"OperatorCandidate; got {type(self.operator_candidate).__name__}."
            )
        if not isinstance(self.factor_source, FactorSourceCandidate):
            raise TypeError(
                "CaseEffectCandidate.factor_source must be a "
                f"FactorSourceCandidate; got {type(self.factor_source).__name__}."
            )
        if not isinstance(self.affected_vector, PreSyntaxMufradVector):
            raise TypeError(
                "CaseEffectCandidate.affected_vector must be a "
                f"PreSyntaxMufradVector; got {type(self.affected_vector).__name__}."
            )
        if not isinstance(self.matrix_row, CaseSignMatrixRow):
            raise TypeError(
                "CaseEffectCandidate.matrix_row must be a CaseSignMatrixRow; "
                f"got {type(self.matrix_row).__name__}."
            )
        if not isinstance(self.factor_equation, FactorMarkEquation):
            raise TypeError(
                "CaseEffectCandidate.factor_equation must be a "
                f"FactorMarkEquation; got {type(self.factor_equation).__name__}."
            )
        if not isinstance(self.compatibility_evidence, tuple):
            raise TypeError(
                "CaseEffectCandidate.compatibility_evidence must be a tuple."
            )
        for fam in self.compatibility_evidence:
            if not isinstance(fam, CaseCompatibilityFamily):
                raise TypeError(
                    "CaseEffectCandidate.compatibility_evidence must contain "
                    "only CaseCompatibilityFamily enum members; got "
                    f"{type(fam).__name__}."
                )
        if not isinstance(self.policy_family, CaseEffectPolicyFamily):
            raise TypeError(
                "CaseEffectCandidate.policy_family must be a "
                "CaseEffectPolicyFamily enum member; got "
                f"{type(self.policy_family).__name__}."
            )
        if not isinstance(self.rank, LughaRank):
            raise TypeError(
                f"CaseEffectCandidate.rank must be a LughaRank; got "
                f"{type(self.rank).__name__}."
            )
        if not isinstance(self.inherited_residuals, tuple):
            raise TypeError(
                "CaseEffectCandidate.inherited_residuals must be a tuple."
            )
        if not isinstance(self.case_effect_residuals, tuple):
            raise TypeError(
                "CaseEffectCandidate.case_effect_residuals must be a tuple."
            )
        for r in self.inherited_residuals + self.case_effect_residuals:
            if not isinstance(r, Residual):
                raise TypeError(
                    "CaseEffectCandidate residuals must be Residual instances."
                )
            if not isinstance(r.type, ResidualType):
                raise TypeError(
                    "CaseEffectCandidate residuals must use central ResidualType "
                    f"taxonomy; got {type(r.type).__name__}."
                )
        if not isinstance(self.trace, CaseEffectCandidateTrace):
            raise TypeError(
                "CaseEffectCandidate.trace must be a CaseEffectCandidateTrace; "
                f"got {type(self.trace).__name__}."
            )

        # Trace consistency
        if self.trace.case_effect_id != self.case_effect_id:
            raise ValueError(
                "CaseEffectCandidate.trace.case_effect_id must match case_effect_id."
            )
        if self.trace.operator_candidate_id != self.operator_candidate_id:
            raise ValueError(
                "CaseEffectCandidate.trace.operator_candidate_id must match "
                "operator_candidate_id."
            )
        if self.trace.factor_equation_id != self.factor_equation_id:
            raise ValueError(
                "CaseEffectCandidate.trace.factor_equation_id must match "
                "factor_equation_id."
            )
        if self.trace.matrix_row_vector_id != self.matrix_row.vector_id:
            raise ValueError(
                "CaseEffectCandidate.trace.matrix_row_vector_id must match "
                "matrix_row.vector_id."
            )
        if self.trace.affected_vector_id != self.affected_vector.mufrad_id:
            raise ValueError(
                "CaseEffectCandidate.trace.affected_vector_id must match "
                "affected_vector.mufrad_id."
            )
        if self.trace.trigger_id != self.trigger_id:
            raise ValueError(
                "CaseEffectCandidate.trace.trigger_id must match trigger_id."
            )
        if self.trace.frame_id != self.frame_id:
            raise ValueError(
                "CaseEffectCandidate.trace.frame_id must match frame_id."
            )
        if self.trace.matrix_id != self.matrix_id:
            raise ValueError(
                "CaseEffectCandidate.trace.matrix_id must match matrix_id."
            )

        # Vector-row consistency
        if self.matrix_row.vector_id != self.affected_vector.mufrad_id:
            raise ValueError(
                f"CaseEffectCandidate matrix_row.vector_id "
                f"({self.matrix_row.vector_id}) must match "
                f"affected_vector.mufrad_id ({self.affected_vector.mufrad_id})."
            )

        # Factor equation consistency
        if self.factor_equation.affected_vector.mufrad_id != self.affected_vector.mufrad_id:
            raise ValueError(
                f"CaseEffectCandidate factor_equation.affected_vector.mufrad_id "
                f"must match affected_vector.mufrad_id."
            )
        if self.factor_equation.factor_source.source_id != self.factor_source.source_id:
            raise ValueError(
                f"CaseEffectCandidate factor_equation.factor_source must match "
                f"factor_source."
            )

    def get_all_residuals(self) -> tuple[Residual, ...]:
        """Return all residuals (inherited + case-effect-specific)."""
        return self.inherited_residuals + self.case_effect_residuals


# ---------------------------------------------------------------------------
# Case Effect Candidate Set
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CaseEffectCandidateSet:
    """
    مجموعة مرشحات الأثر الإعرابي

    The complete set of all case effect candidates for a given operator candidate
    and its affected constituents.

    PRESERVES ALL COMPETING CANDIDATES. Never resolves competition.
    """

    trigger_id: str
    """OperatorTriggerPotential.trigger_id (chain provenance)."""

    frame_id: str
    """SentenceFrameCandidate.frame_id (chain provenance)."""

    matrix_id: str
    """CaseSignMatrix.matrix_id (chain provenance)."""

    candidates: tuple[CaseEffectCandidate, ...]
    """
    All case effect candidates, preserving all competing effects.
    Empty tuple if no valid case effects could be built.
    """

    rank: LughaRank
    """
    Candidate set rank ceiling:
    - If candidates non-empty: rank ≤ min(candidate.rank for candidate in candidates)
    - If candidates empty: rank ≤ operator.rank
    """

    inherited_residuals: tuple[Residual, ...]
    """Residuals inherited from operator (includes trigger, matrix, frame)."""

    candidate_set_residuals: tuple[Residual, ...]
    """Residuals specific to this candidate set (e.g., no valid effects)."""

    competitors_preserved: bool
    """
    True when multiple candidates exist. Signals unresolved competition.
    """

    def __post_init__(self) -> None:
        # Field-name leak check (defensive)
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        leaks = field_names & _FORBIDDEN_FIELDS
        if leaks:
            raise ValueError(
                f"CaseEffectCandidateSet contains forbidden fields: {leaks}."
            )

        # Type checks
        if not self.trigger_id:
            raise ValueError("CaseEffectCandidateSet.trigger_id is required.")
        if not self.frame_id:
            raise ValueError("CaseEffectCandidateSet.frame_id is required.")
        if not self.matrix_id:
            raise ValueError("CaseEffectCandidateSet.matrix_id is required.")
        if not isinstance(self.candidates, tuple):
            raise TypeError("CaseEffectCandidateSet.candidates must be a tuple.")
        for c in self.candidates:
            if not isinstance(c, CaseEffectCandidate):
                raise TypeError(
                    "CaseEffectCandidateSet.candidates entries must be "
                    f"CaseEffectCandidate; got {type(c).__name__}."
                )
        if not isinstance(self.rank, LughaRank):
            raise TypeError(
                f"CaseEffectCandidateSet.rank must be a LughaRank; got "
                f"{type(self.rank).__name__}."
            )
        if not isinstance(self.inherited_residuals, tuple):
            raise TypeError(
                "CaseEffectCandidateSet.inherited_residuals must be a tuple."
            )
        if not isinstance(self.candidate_set_residuals, tuple):
            raise TypeError(
                "CaseEffectCandidateSet.candidate_set_residuals must be a tuple."
            )
        for r in self.inherited_residuals + self.candidate_set_residuals:
            if not isinstance(r, Residual):
                raise TypeError(
                    "CaseEffectCandidateSet residuals must be Residual instances."
                )
            if not isinstance(r.type, ResidualType):
                raise TypeError(
                    "CaseEffectCandidateSet residuals must use central "
                    f"ResidualType taxonomy; got {type(r.type).__name__}."
                )
        if not isinstance(self.competitors_preserved, bool):
            raise TypeError(
                "CaseEffectCandidateSet.competitors_preserved must be a bool."
            )

    def get_all_residuals(self) -> tuple[Residual, ...]:
        """Return all residuals (inherited + set-specific)."""
        return self.inherited_residuals + self.candidate_set_residuals

    def has_unresolved_competition(self) -> bool:
        """
        Check if multiple candidates exist (unresolved competition).

        Returns True if len(candidates) >= 2, indicating that multiple
        case effect candidates exist and no resolution has been applied.
        """
        return len(self.candidates) >= 2


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def _determine_effect_type(
    policy_family: CaseEffectPolicyFamily,
    compatibility_families: tuple[CaseCompatibilityFamily, ...],
    equation_type: FactorMarkEquationType,
) -> tuple[CaseEffectCandidateType, list[Residual]]:
    """
    Determine case effect candidate type from policy family, compatibility,
    and equation type.

    Returns: (effect_type, residuals)
    """
    residuals: list[Residual] = []

    # Building compatibility always produces building effect
    if CaseCompatibilityFamily.BUILDING_COMPATIBLE in compatibility_families:
        return CaseEffectCandidateType.BUILDING_EFFECT_CANDIDATE, residuals

    # Deferred equation produces deferred effect
    if equation_type == FactorMarkEquationType.DEFERRED:
        residuals.append(
            make_warning(
                ResidualType.CASE_EFFECT_DEFERRED_MISSING_MARK,
                "Case effect deferred: mark potential missing from equation.",
                location="case_effect_builder",
            )
        )
        return CaseEffectCandidateType.DEFERRED_EFFECT_CANDIDATE, residuals

    # Map policy family + compatibility to effect type
    if policy_family == CaseEffectPolicyFamily.RAFI_POLICY_FAMILY:
        if CaseCompatibilityFamily.RAFA_COMPATIBLE in compatibility_families:
            return CaseEffectCandidateType.RAFʿ_EFFECT_CANDIDATE, residuals
        else:
            residuals.append(
                make_blocker(
                    ResidualType.CASE_EFFECT_COMPATIBILITY_CONFLICT,
                    f"Policy requires RAFA but compatibility families are "
                    f"{[f.value for f in compatibility_families]}.",
                    location="case_effect_builder",
                )
            )
            return CaseEffectCandidateType.BLOCKED_EFFECT_CANDIDATE, residuals

    if policy_family == CaseEffectPolicyFamily.NASB_POLICY_FAMILY:
        if CaseCompatibilityFamily.NASB_COMPATIBLE in compatibility_families:
            return CaseEffectCandidateType.NASB_EFFECT_CANDIDATE, residuals
        else:
            residuals.append(
                make_blocker(
                    ResidualType.CASE_EFFECT_COMPATIBILITY_CONFLICT,
                    f"Policy requires NASB but compatibility families are "
                    f"{[f.value for f in compatibility_families]}.",
                    location="case_effect_builder",
                )
            )
            return CaseEffectCandidateType.BLOCKED_EFFECT_CANDIDATE, residuals

    if policy_family == CaseEffectPolicyFamily.JARR_POLICY_FAMILY:
        if CaseCompatibilityFamily.JARR_COMPATIBLE in compatibility_families:
            return CaseEffectCandidateType.JARR_EFFECT_CANDIDATE, residuals
        else:
            residuals.append(
                make_blocker(
                    ResidualType.CASE_EFFECT_COMPATIBILITY_CONFLICT,
                    f"Policy requires JARR but compatibility families are "
                    f"{[f.value for f in compatibility_families]}.",
                    location="case_effect_builder",
                )
            )
            return CaseEffectCandidateType.BLOCKED_EFFECT_CANDIDATE, residuals

    if policy_family == CaseEffectPolicyFamily.JAZM_POLICY_FAMILY:
        if CaseCompatibilityFamily.JAZM_COMPATIBLE in compatibility_families:
            return CaseEffectCandidateType.JAZM_EFFECT_CANDIDATE, residuals
        else:
            residuals.append(
                make_blocker(
                    ResidualType.CASE_EFFECT_COMPATIBILITY_CONFLICT,
                    f"Policy requires JAZM but compatibility families are "
                    f"{[f.value for f in compatibility_families]}.",
                    location="case_effect_builder",
                )
            )
            return CaseEffectCandidateType.BLOCKED_EFFECT_CANDIDATE, residuals

    if policy_family == CaseEffectPolicyFamily.MIXED_RAFI_NASB_POLICY_FAMILY:
        # Mixed policy (e.g., kana/inna): DANGEROUS without slot/frame info
        # CRITICAL FIX (PR #161): Mixed policy should NOT choose based on
        # compatibility alone. It requires slot/frame side information to
        # determine which constituent gets which case (e.g., ism_kana vs khabar_kana).
        # Without that information, defer the decision.
        residuals.append(
            make_warning(
                ResidualType.CASE_EFFECT_MIXED_POLICY_REQUIRES_SLOT,
                "Mixed rafi/nasb policy requires frame slot/role information to "
                "determine which constituent gets which case. Producing deferred effect "
                "until slot info available.",
                location="case_effect_builder",
            )
        )
        return CaseEffectCandidateType.DEFERRED_EFFECT_CANDIDATE, residuals

    if policy_family == CaseEffectPolicyFamily.NO_CASE_EFFECT_POLICY_FAMILY:
        residuals.append(
            make_info(
                ResidualType.CASE_EFFECT_NO_POLICY,
                "Operator has NO_CASE_EFFECT_POLICY_FAMILY; producing deferred effect.",
                location="case_effect_builder",
            )
        )
        return CaseEffectCandidateType.DEFERRED_EFFECT_CANDIDATE, residuals

    # Fallback: unresolved
    residuals.append(
        make_warning(
            ResidualType.CASE_EFFECT_UNRESOLVED_POLICY,
            f"Unrecognized policy family {policy_family.value}; producing deferred effect.",
            location="case_effect_builder",
        )
    )
    return CaseEffectCandidateType.DEFERRED_EFFECT_CANDIDATE, residuals


def _get_rank_from_transition_proof(transition_proof) -> LughaRank:
    """
    Extract LughaRank from TransitionProof.rank_name.

    TransitionProof stores rank as string name (e.g., "QIYAS", "SAMA").
    Convert back to LughaRank enum.

    Args:
        transition_proof: TransitionProof with rank_name field

    Returns:
        LughaRank enum member

    Raises:
        ValueError: If rank_name is not a valid LughaRank member
    """
    rank_name = transition_proof.rank_name
    try:
        return LughaRank[rank_name]
    except KeyError:
        raise ValueError(
            f"TransitionProof.rank_name '{rank_name}' is not a valid LughaRank member. "
            f"Valid members: {[r.name for r in LughaRank]}"
        )


def build_case_effect_candidate(
    operator_candidate: OperatorCandidate,
    factor_equation: FactorMarkEquation,
    matrix_row: CaseSignMatrixRow,
) -> CaseEffectCandidate:
    """
    بناء مرشح الأثر الإعرابي

    Build one case effect candidate from operator candidate, factor equation,
    and matrix row.

    GOVERNING RULES:
    1. Accepts only OperatorCandidate, FactorMarkEquation, CaseSignMatrixRow.
    2. Reads policy family from operator_candidate.registry_entry.
    3. Reads compatibility from matrix_row.compatibility_families.
    4. Determines effect type via policy + compatibility + equation type.
    5. Produces CANDIDATE only, never final case effect.
    6. Preserves all identities (operator, factor, affected).
    7. Candidate rank: rank ≤ min(operator.rank, equation.rank, row.rank)
    8. Residual inheritance: case_effect.inherited_residuals ⊇
       operator.get_all_residuals()
    9. Constitutional law: NO final case_effect, NO meaning, NO ifadah, NO hukm.

    Args:
        operator_candidate: OperatorCandidate from prior layer
        factor_equation: FactorMarkEquation linking factor → affected → mark
        matrix_row: CaseSignMatrixRow with compatibility evidence

    Returns:
        CaseEffectCandidate with complete proof

    Raises:
        TypeError: If inputs are not the required types
        ValueError: If inputs are inconsistent
    """
    # Input validation
    if not isinstance(operator_candidate, OperatorCandidate):
        raise TypeError(
            "build_case_effect_candidate requires an OperatorCandidate; got "
            f"{type(operator_candidate).__name__}."
        )
    if not isinstance(factor_equation, FactorMarkEquation):
        raise TypeError(
            "build_case_effect_candidate requires a FactorMarkEquation; got "
            f"{type(factor_equation).__name__}."
        )
    if not isinstance(matrix_row, CaseSignMatrixRow):
        raise TypeError(
            "build_case_effect_candidate requires a CaseSignMatrixRow; got "
            f"{type(matrix_row).__name__}."
        )

    # Consistency checks
    if matrix_row.vector_id != factor_equation.affected_vector.mufrad_id:
        raise ValueError(
            f"matrix_row.vector_id ({matrix_row.vector_id}) must match "
            f"factor_equation.affected_vector.mufrad_id "
            f"({factor_equation.affected_vector.mufrad_id})."
        )

    # Extract data
    affected_vector = factor_equation.affected_vector
    factor_source = factor_equation.factor_source
    registry_entry = operator_candidate.registry_entry
    compatibility_families = matrix_row.compatibility_families
    equation_type = factor_equation.equation_type

    # Get policy families (use first one if multiple)
    policy_families = registry_entry.case_effect_policy_families
    if not policy_families:
        policy_family = CaseEffectPolicyFamily.NO_CASE_EFFECT_POLICY_FAMILY
    else:
        policy_family = policy_families[0]

    # Determine effect type
    effect_type, effect_residuals = _determine_effect_type(
        policy_family,
        compatibility_families,
        equation_type,
    )

    # Inherited residuals from operator (includes trigger, matrix, frame)
    inherited = operator_candidate.get_all_residuals()

    # Case effect residuals
    case_effect_residuals = list(effect_residuals)

    # Rank ceiling: min(operator.rank, equation.rank, row.rank)
    # CRITICAL FIX (PR #161): Extract rank from factor_equation.transition_proof
    factor_equation_rank = _get_rank_from_transition_proof(factor_equation.transition_proof)
    candidate_rank = min(
        operator_candidate.rank,
        factor_equation_rank,
        matrix_row.rank,
        key=lambda r: r.value,
    )

    # Generate IDs
    case_effect_id = f"case-effect-{uuid.uuid4().hex[:12]}"

    # Collect identity_ids (PR #161: explicit identity preservation)
    # Identity sources:
    # 1. operator registry entry ID (operator identity)
    # 2. factor_source.identity_ids (factor linguistic identities)
    # 3. affected_vector identity (if available via mufrad_id or similar)
    identity_ids_set = set()
    identity_ids_set.add(operator_candidate.registry_entry_id)
    identity_ids_set.update(factor_source.identity_ids)
    # Note: affected_vector.mufrad_id is a trace, not an identity
    # If affected_vector has explicit identity_ids, add them
    if hasattr(affected_vector, 'identity_ids'):
        identity_ids_set.update(affected_vector.identity_ids)
    identity_ids = tuple(sorted(identity_ids_set))

    # Collect trace_ids (PR #161: explicit trace tracking)
    # Trace sources:
    # 1. operator_candidate trace IDs
    # 2. factor_source.trace_ids
    # 3. affected_vector traces
    # 4. matrix_row trace (row_trace_id if available)
    trace_ids_set = set()
    trace_ids_set.update(factor_source.trace_ids)
    # Add operator candidate trace
    if hasattr(operator_candidate, 'trace') and hasattr(operator_candidate.trace, 'candidate_id'):
        trace_ids_set.add(operator_candidate.trace.candidate_id)
    # Add affected vector traces
    if hasattr(affected_vector, 'trace_ids'):
        trace_ids_set.update(affected_vector.trace_ids)
    # Add matrix row trace (trace only, NOT identity)
    if hasattr(matrix_row, 'row_trace_id'):
        trace_ids_set.add(matrix_row.row_trace_id)
    trace_ids = tuple(sorted(trace_ids_set))

    # Create trace
    trace = CaseEffectCandidateTrace(
        case_effect_id=case_effect_id,
        operator_candidate_id=operator_candidate.candidate_id,
        factor_equation_id=factor_equation.equation_id,
        matrix_row_vector_id=matrix_row.vector_id,
        affected_vector_id=affected_vector.mufrad_id,
        trigger_id=operator_candidate.trigger_id,
        frame_id=operator_candidate.frame_id,
        matrix_id=operator_candidate.matrix_id,
    )

    # Create candidate
    candidate = CaseEffectCandidate(
        case_effect_id=case_effect_id,
        operator_candidate_id=operator_candidate.candidate_id,
        factor_equation_id=factor_equation.equation_id,
        trigger_id=operator_candidate.trigger_id,
        frame_id=operator_candidate.frame_id,
        matrix_id=operator_candidate.matrix_id,
        effect_type=effect_type,
        operator_candidate=operator_candidate,
        factor_source=factor_source,
        affected_vector=affected_vector,
        matrix_row=matrix_row,
        factor_equation=factor_equation,
        compatibility_evidence=compatibility_families,
        policy_family=policy_family,
        identity_ids=identity_ids,  # PR #161
        trace_ids=trace_ids,  # PR #161
        rank=candidate_rank,
        inherited_residuals=inherited,
        case_effect_residuals=tuple(case_effect_residuals),
        trace=trace,
    )

    return candidate
