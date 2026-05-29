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

Created: 2026-05-29
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.case_signs import CaseSignPotential
from dal_core.transition_proof_kernel import (
    EffectiveDescription,
    IdentityNeutralCheck,
    MinimalCompletenessCheck,
    QiyasProof,
    TransitionProof,
)


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

    Fields:
        equation_id: Unique identifier
        factor_trace_id: Trace ID of factor (operator/relation)
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
    factor_trace_id: str
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
    factor_trace_id: str,
    affected_vector: PreSyntaxMufradVector,
    mark_potential: Optional[CaseSignPotential],
    equation_type: FactorMarkEquationType,
) -> FactorMarkEquation:
    """
    Build factor-mark candidate equation.

    Constitutional Requirements:
        1. Verify affected_vector allows operator consumption
        2. Build qiyas proof linking factor → affected
        3. Preserve identities (factor + affected traces)
        4. Check minimal completeness
        5. Build transition proof
        6. NO case_effect production

    Args:
        factor_trace_id: Trace ID of factor (operator/relation)
        affected_vector: PreSyntaxMufradVector being affected
        mark_potential: Observed case sign potential (or None)
        equation_type: Type of candidate equation

    Returns:
        FactorMarkEquation with complete proof

    Raises:
        ValueError: If affected_vector not ready for consumption

    Example:
        >>> equation = build_factor_mark_equation(
        ...     factor_trace_id="trace:operator_123",
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
        evidence=("PreSyntaxMufradVector", "CaseSignPotential"),
    )

    qiyas = QiyasProof(
        proof_id=f"qiyas:factor_mark:{affected_trace_id}",
        origin_id=f"origin:factor_mark:{equation_type.value}",
        branch_id=affected_trace_id,
        effective_description=effective,
        shared_cause="operator/factor trace licenses candidate mark relation without producing case effect",
        invalidating_differences=(),
    )

    neutral = IdentityNeutralCheck(
        check_id=f"id_neutral:factor_mark:{affected_trace_id}",
        input_identity_ids=(factor_trace_id, affected_trace_id),
        output_identity_ids=(factor_trace_id, affected_trace_id),
        preserved=True,
    )

    # Check for missing conditions
    missing = ()
    if mark_potential is None:
        missing = ("mark_potential_missing",)

    minimum = MinimalCompletenessCheck(
        check_id=f"minimum:factor_mark:{affected_trace_id}",
        target_layer="FACTOR_MARK_EQUATION",
        required_conditions=(
            "factor_trace_present",
            "affected_trace_present",
            "affected_ready",
            "mark_potential_present_or_deferred",
            "no_case_effect",
            "no_meaning",
            "no_ifadah",
            "no_hukm",
        ),
        satisfied_conditions=(
            "factor_trace_present",
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

    transition = TransitionProof(
        proof_id=f"transition:factor_mark:{affected_trace_id}",
        source_layer="PRESYNTAX_MUFRAD_VECTOR",
        target_layer="FACTOR_MARK_EQUATION",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=(factor_trace_id, affected_trace_id),
        residual_ids=tuple(str(r) for r in affected_vector.residuals),
        rank_name=affected_vector.final_rank.name if hasattr(affected_vector.final_rank, 'name') else str(affected_vector.final_rank),
    )

    # Build and return equation
    return FactorMarkEquation(
        equation_id=f"factor_mark:{factor_trace_id}:{affected_trace_id}",
        factor_trace_id=factor_trace_id,
        affected_trace_id=affected_trace_id,
        affected_vector=affected_vector,
        mark_potential=mark_potential,
        equation_type=equation_type if mark_potential is not None else FactorMarkEquationType.DEFERRED,
        transition_proof=transition,
    )
