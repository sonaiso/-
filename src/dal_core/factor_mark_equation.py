"""
Factor Mark Equation (معادلة العامل والعلامة)

Builds candidate equation for factor/affected/mark WITHOUT producing case_effect.

Constitutional Purpose:
    Begin factor-mark algebra as CANDIDATE equations,
    NOT as final case effects.

Critical Principles:
    1. Factor provides trace (from operator/relation)
    2. Affected is PreSyntaxMufradVector
    3. Mark is CaseSignPotential (observation, NOT effect)
    4. Equation is CANDIDATE (not final judgment)
    5. NO case_effect production
    6. NO meaning/ifadah/hukm

Forbidden Outputs:
    ❌ case_effect, marfoo_by, mansub_by, majroor_by
    ❌ meaning, semantic, madlul, murad
    ❌ ifadah, pragmatic_completion
    ❌ hukm, judgment

Architecture Position:
    PreSyntaxMufradVector + CaseSignPotential
        → build_factor_mark_equation (this module)
            → FactorMarkEquation (CANDIDATE)
                → [Future: FactorMarkJudgment with case_effect]

Reference:
    PR: Bridge Arabic Composition Chain
    Builds on: PreSyntaxVector, CaseSignPotential

PR #159: Strengthened factor source (no bare string)

Created: 2026-05-29
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.case_signs import CaseSignPotential
from dal_core.ranks import LughaRank
from dal_core.transition_proof_kernel import (
    EffectiveDescription,
    IdentityNeutralCheck,
    MinimalCompletenessCheck,
    QiyasProof,
    TransitionProof,
)
from fvafk.algebra.core import Rank


# ============================================================================
# Rank Conversion (PR #163 Integration)
# ============================================================================

def _lugha_rank_to_fvafk_rank(lugha_rank: LughaRank) -> Rank:
    """
    Convert LughaRank to fvafk.algebra.Rank.

    Conservative mapping to prevent rank inflation:
    - ZERO/FORM → CANDIDATE (not yet licensed)
    - QIYAS → CANDIDATE (conservative, pending evidence validation)
    - SAMA/AHAD/TAWATUR → CANDIDATE (conservative ceiling per PR #163)

    Constitutional Law:
        Per PR #163, TransitionProof.to_result() applies rank ceiling.
        Until Evidence objects are fully validated (not just strings),
        all transitions stay at CANDIDATE max.

    Args:
        lugha_rank: LughaRank enum value

    Returns:
        Corresponding fvafk.algebra.Rank value (conservative mapping)
    """
    # Conservative mapping: all ranks → CANDIDATE until evidence validated
    # This prevents rank inflation identified in PR #163 review
    if lugha_rank == LughaRank.ZERO:
        return Rank.UNRESOLVED
    else:
        # FORM, QIYAS, SAMA, AHAD, TAWATUR all map to CANDIDATE
        # Rank ceiling in TransitionProof.to_result() enforces this anyway
        return Rank.CANDIDATE


# ============================================================================
# Factor Source (PR #159)
# ============================================================================

class FactorSourceKind(Enum):
    """
    نوع مصدر العامل (Factor Source Kind)

    Classification of where the factor candidate originates.
    """
    RELATION_CANDIDATE = "relation_candidate"
    """Factor from RelationCandidate (ISNAD/TADMIN/TAQYID)"""

    OPERATOR_CANDIDATE = "operator_candidate"
    """Factor from NahwOperatorCandidate"""

    ANCHOR = "anchor"
    """Factor from algebraic Anchor"""

    PREPOSITION = "preposition"
    """Factor from preposition/particle"""


@dataclass(frozen=True)
class FactorSourceCandidate:
    """
    مرشح مصدر العامل (Factor Source Candidate)

    PR #159: Structured factor source (NOT bare string).

    Constitutional Law:
        Factor must be preserved as structured candidate with:
        - source_id (unique identifier)
        - source_kind (classification)
        - identity_ids (linguistic identities)
        - trace_ids (provenance)
        - rank (authority level)

    Fields:
        source_id: Unique identifier of factor source
        source_kind: Kind of factor source
        identity_ids: Linguistic identity IDs
        trace_ids: Provenance trace IDs
        rank: Rank of factor candidate
    """
    source_id: str
    source_kind: FactorSourceKind
    identity_ids: tuple[str, ...]
    trace_ids: tuple[str, ...]
    rank: LughaRank


# ============================================================================
# Factor Mark Equation Type
# ============================================================================

class FactorMarkEquationType(Enum):
    """
    نوع معادلة العامل والعلامة

    Equation type classifications based on expected case.

    Note: These are CANDIDATE types, NOT final case effects.
    """
    RAFʿ_CANDIDATE = "raf_candidate"
    """Raf' (nominative) candidate equation"""

    NASB_CANDIDATE = "nasb_candidate"
    """Nasb (accusative) candidate equation"""

    JARR_CANDIDATE = "jarr_candidate"
    """Jarr (genitive) candidate equation"""

    JAZM_CANDIDATE = "jazm_candidate"
    """Jazm (jussive) candidate equation"""

    DEFERRED = "deferred"
    """Deferred (mark potential missing or unclear)"""


# ============================================================================
# Factor Mark Equation
# ============================================================================

@dataclass(frozen=True)
class FactorMarkEquation:
    """
    معادلة العامل والعلامة (Factor Mark Equation)

    Candidate equation linking factor → affected → mark.

    Constitutional Law:
        This equation is ALWAYS a candidate.
        It does NOT produce case_effect.
        It only establishes the potential relationship.

    PR #159: Factor is structured FactorSourceCandidate, not bare string.

    Fields:
        equation_id: Unique identifier
        factor_source: Structured factor source candidate (PR #159)
        affected_trace_id: Trace ID of affected mufrad
        affected_vector: Preserved PreSyntaxMufradVector
        mark_potential: Observed case sign potential (or None if deferred)
        equation_type: Type of candidate equation
        transition_proof: Complete transition proof
        produces_case_effect: Whether produces case_effect (ALWAYS False)
        produces_meaning: Whether produces meaning (ALWAYS False)
        produces_ifadah: Whether produces ifadah (ALWAYS False)
        produces_hukm: Whether produces hukm (ALWAYS False)
    """
    equation_id: str
    factor_source: FactorSourceCandidate  # PR #159: structured, not string
    affected_trace_id: str

    affected_vector: PreSyntaxMufradVector
    mark_potential: Optional[CaseSignPotential]

    equation_type: FactorMarkEquationType

    transition_proof: TransitionProof

    produces_case_effect: bool = False
    produces_meaning: bool = False
    produces_ifadah: bool = False
    produces_hukm: bool = False


# ============================================================================
# Main Builder Function
# ============================================================================

def build_factor_mark_equation(
    *,
    factor_source: FactorSourceCandidate,  # PR #159: structured, not string
    affected_vector: PreSyntaxMufradVector,
    mark_potential: Optional[CaseSignPotential],
    equation_type: FactorMarkEquationType,
) -> FactorMarkEquation:
    """
    Build factor-mark candidate equation.

    PR #159: Factor is structured FactorSourceCandidate, not bare string.

    Constitutional Requirements:
        1. Verify affected_vector allows operator consumption
        2. Build qiyas proof linking factor → affected
        3. Preserve identities (factor + affected)
        4. Check minimal completeness
        5. Build transition proof
        6. NO case_effect production

    Args:
        factor_source: Structured factor source candidate (NOT string)
        affected_vector: PreSyntaxMufradVector being affected
        mark_potential: Observed case sign potential (or None)
        equation_type: Type of candidate equation

    Returns:
        FactorMarkEquation with complete proof

    Raises:
        ValueError: If affected_vector not ready for consumption

    Example:
        >>> factor = FactorSourceCandidate(
        ...     source_id="rel:123",
        ...     source_kind=FactorSourceKind.RELATION_CANDIDATE,
        ...     identity_ids=("form:xyz",),
        ...     trace_ids=("trace:123",),
        ...     rank=LughaRank.CANDIDATE
        ... )
        >>> equation = build_factor_mark_equation(
        ...     factor_source=factor,
        ...     affected_vector=presyntax_vector,
        ...     mark_potential=case_sign_potential,
        ...     equation_type=FactorMarkEquationType.RAFʿ_CANDIDATE
        ... )
        >>> assert not equation.produces_case_effect
    """
    # Gate: Verify readiness
    if not affected_vector.allows_operator_consumption():
        raise ValueError("Affected vector is not ready for factor/mark equation")

    affected_trace_id = affected_vector.trace_id

    # Build transition proof components
    effective = EffectiveDescription(
        description_id=f"effective:factor_mark:{affected_trace_id}",
        description_type="factor_mark_candidate_equation",
        evidence=("FactorSourceCandidate", "PreSyntaxMufradVector", "CaseSignPotential"),
    )

    qiyas = QiyasProof(
        proof_id=f"qiyas:factor_mark:{affected_trace_id}",
        origin_id=f"origin:factor_mark:{equation_type.value}",
        branch_id=affected_trace_id,
        effective_description=effective,
        shared_cause="factor source candidate licenses potential mark relation without producing case effect",
        invalidating_differences=(),
    )

    # PR #159: Use factor identity_ids + affected identity_ids
    # PR #166: Empty identity_ids cannot be considered "identity preserved"
    factor_identity_ids = factor_source.identity_ids
    affected_identity_ids = affected_vector.identity_ids or ()

    combined_identity_ids = factor_identity_ids + affected_identity_ids
    has_missing_identity = not combined_identity_ids
    # Empty → empty IS preserved (trivially), but flagged as missing
    preserved_flag = True  # Empty set ⊆ empty set = true

    # If identity is missing, add residual
    residual_ids_list = list(str(r) for r in affected_vector.residuals)
    if has_missing_identity:
        missing_identity_residual_id = f"residual:missing_identity:factor_mark:{affected_trace_id}"
        residual_ids_list.append(missing_identity_residual_id)

    neutral = IdentityNeutralCheck(
        check_id=f"id_neutral:factor_mark:{affected_trace_id}",
        input_identity_ids=combined_identity_ids,
        output_identity_ids=combined_identity_ids,
        preserved=preserved_flag,
        has_missing_identity=has_missing_identity,
    )

    # Check for missing conditions
    missing = ()
    if mark_potential is None:
        missing = ("mark_potential_missing",)

    minimum = MinimalCompletenessCheck(
        check_id=f"minimum:factor_mark:{affected_trace_id}",
        target_layer="FACTOR_MARK_EQUATION",
        required_conditions=(
            "factor_source_structured",  # PR #159
            "affected_trace_present",
            "affected_ready",
            "mark_potential_present_or_deferred",
            "no_case_effect",
            "no_meaning",
            "no_ifadah",
            "no_hukm",
        ),
        satisfied_conditions=(
            "factor_source_structured",  # PR #159
            "affected_trace_present",
            "affected_ready",
            "no_case_effect",
            "no_meaning",
            "no_ifadah",
            "no_hukm",
        ) + (() if missing else ("mark_potential_present_or_deferred",)),
        missing_conditions=missing,
        passed=not missing,
    )

    # PR #159: Combine factor trace_ids + affected trace_ids
    # PR #166: Use residual_ids_list (includes missing_identity if needed)
    factor_trace_ids = factor_source.trace_ids
    affected_trace_ids = (affected_trace_id,)

    transition = TransitionProof(
        proof_id=f"transition:factor_mark:{affected_trace_id}",
        source_layer="PRESYNTAX_MUFRAD_VECTOR",
        target_layer="FACTOR_MARK_EQUATION",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=factor_trace_ids + affected_trace_ids,
        residual_ids=tuple(residual_ids_list),
        rank=_lugha_rank_to_fvafk_rank(affected_vector.final_rank),
    )

    # Build and return equation
    return FactorMarkEquation(
        equation_id=f"factor_mark:{factor_source.source_id}:{affected_trace_id}",
        factor_source=factor_source,  # PR #159: structured object
        affected_trace_id=affected_trace_id,
        affected_vector=affected_vector,
        mark_potential=mark_potential,
        equation_type=equation_type if mark_potential is not None else FactorMarkEquationType.DEFERRED,
        transition_proof=transition,
    )
