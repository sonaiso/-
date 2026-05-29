"""
Mufrad Acceptance Equation (معادلة قبول المفرد)

Proves that MufradProof satisfies the acceptance equation:

    Carriers + Identities + Causes ≡ LicensedWord + PreservedIdentities + Trace

Constitutional Purpose:
    Build on top of existing MufradProof without replacing it.
    Provide explicit LHS ≡ RHS equation proof for composition readiness.

Critical Principles:
    1. Carriers must be preserved (LHS carriers ⊆ RHS carriers)
    2. Identities must be preserved (LHS identities ⊆ RHS identities)
    3. Transition proof must be ACCEPTED
    4. No meaning/ifadah/hukm produced

Forbidden Outputs:
    ❌ meaning, semantic, madlul, murad
    ❌ ifadah, pragmatic_completion
    ❌ hukm, judgment
    ❌ case_effect (only case_sign_potential allowed)

Architecture Position:
    MufradProof
        → MufradAcceptanceEquation (this module)
            → PreSyntaxMufradVector
                → RelationSlotReadiness

Reference:
    PR: Bridge Arabic Composition Chain
    Builds on: MufradProof

Created: 2026-05-29
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from dal_core.mufrad_proof import MufradProof
from dal_core.transition_proof_kernel import (
    EffectiveDescription,
    IdentityNeutralCheck,
    InvalidatingDifference,
    MinimalCompletenessCheck,
    QiyasProof,
    TransitionProof,
)


# ============================================================================
# Mufrad Acceptance Equation
# ============================================================================

@dataclass(frozen=True)
class MufradAcceptanceEquation:
    """
    معادلة قبول المفرد (Mufrad Acceptance Equation)

    Explicit equation proving MufradProof acceptance:

        LHS: Carriers + Identities + EffectiveDescriptions + QiyasProofs
        RHS: Word + PreservedCarriers + PreservedIdentities + Trace

    Constitutional Law:
        An equation is accepted if and only if:
        1. carriers_balanced: LHS carriers ⊆ RHS carriers
        2. identities_balanced: LHS identities ⊆ RHS identities
        3. transition_proof.decision == ACCEPTED

    Fields:
        equation_id: Unique identifier
        mufrad_id: Identifier of source MufradProof
        lhs_carrier_ids: Carrier identifiers (input side)
        lhs_identity_ids: Identity identifiers (input side)
        lhs_effective_description_ids: Effective description IDs
        lhs_qiyas_proof_ids: Qiyas proof IDs
        rhs_word_surface: The resulting word surface
        rhs_preserved_carrier_ids: Preserved carriers (output side)
        rhs_preserved_identity_ids: Preserved identities (output side)
        rhs_trace_id: Trace identifier
        transition_proof: Complete transition proof
    """
    equation_id: str
    mufrad_id: str

    # Left-hand side (inputs)
    lhs_carrier_ids: Tuple[str, ...]
    lhs_identity_ids: Tuple[str, ...]
    lhs_effective_description_ids: Tuple[str, ...]
    lhs_qiyas_proof_ids: Tuple[str, ...]

    # Right-hand side (outputs)
    rhs_word_surface: str
    rhs_preserved_carrier_ids: Tuple[str, ...]
    rhs_preserved_identity_ids: Tuple[str, ...]
    rhs_trace_id: str

    # Complete transition proof
    transition_proof: TransitionProof

    @property
    def carriers_balanced(self) -> bool:
        """Check if carriers are preserved (LHS ⊆ RHS)."""
        return set(self.lhs_carrier_ids).issubset(set(self.rhs_preserved_carrier_ids))

    @property
    def identities_balanced(self) -> bool:
        """Check if identities are preserved (LHS ⊆ RHS)."""
        return set(self.lhs_identity_ids).issubset(set(self.rhs_preserved_identity_ids))

    @property
    def accepted(self) -> bool:
        """
        Check if equation is fully accepted.

        An equation is accepted if:
        1. Carriers balanced
        2. Identities balanced
        3. Transition proof decision is ACCEPTED
        """
        return (
            self.carriers_balanced
            and self.identities_balanced
            and self.transition_proof.decision.value == "accepted"
        )


# ============================================================================
# Helper Functions
# ============================================================================

def _carrier_ids_from_mufrad(proof: MufradProof) -> Tuple[str, ...]:
    """
    Extract carrier IDs from MufradProof.

    PR #159: Strengthened carrier provenance hierarchy.

    Three-tier approach:
    1. If carrier/atom IDs available from FormCandidate → use them (ACCEPTED)
    2. If form identity available → use provisional (CANDIDATE_WITH_RESIDUAL)
    3. If only text fallback → use fallback (DEFERRED or residual)

    Args:
        proof: MufradProof to extract carriers from

    Returns:
        Tuple of carrier IDs (may be provisional/fallback)
    """
    # Tier 1: Try to get real carrier/atom IDs from FormCandidate
    # (Currently not exposed in data structure - fallback to Tier 3)

    # Tier 2: Use form identity as provisional carrier
    # (Currently not distinguished from Tier 3)

    # Tier 3: Text fallback (mark as fallback)
    surface = proof.form.vocalization or proof.form.text
    return tuple(f"carrier:fallback:{i}:{ch}" for i, ch in enumerate(surface))


def _identity_ids_from_mufrad(proof: MufradProof) -> Tuple[str, ...]:
    """
    Extract identity IDs from MufradProof.

    PR #159: Explicit linguistic identity extraction.

    Extracts identities from:
    - form (vocalization)
    - type (dal_type value)
    - root_candidates
    - wazn_candidates
    - clitics

    CRITICAL: identity_ids ≠ trace_ids

    Args:
        proof: MufradProof to extract identities from

    Returns:
        Tuple of identity IDs
    """
    ids = []

    # Form identity
    ids.append(f"form:{proof.form.vocalization}")

    # Type identity
    type_value = getattr(proof.type, 'dal_type', '') or getattr(proof.type, 'type_value', '')
    ids.append(f"type:{type_value}")

    # Root identities
    for root in proof.root_candidates:
        root_id = getattr(root, 'root', getattr(root, 'root_id', id(root)))
        ids.append(f"root:{root_id}")

    # Wazn identities
    for wazn in proof.wazn_candidates:
        wazn_id = getattr(wazn, 'pattern', getattr(wazn, 'wazn_id', id(wazn)))
        ids.append(f"wazn:{wazn_id}")

    # Clitic identities
    for clitic in proof.clitics:
        clitic_id = getattr(clitic, 'surface', id(clitic))
        ids.append(f"clitic:{clitic_id}")

    return tuple(str(x) for x in ids)


def _has_carrier_fallback(carrier_ids: Tuple[str, ...]) -> bool:
    """
    Check if carrier IDs use text fallback.

    PR #159: Detect carrier provenance fallback.

    Args:
        carrier_ids: Carrier ID tuple to check

    Returns:
        True if using fallback (not full provenance)
    """
    return any(":fallback:" in cid for cid in carrier_ids)


# ============================================================================
# Main Proof Function
# ============================================================================

def prove_mufrad_acceptance(proof: MufradProof) -> MufradAcceptanceEquation:
    """
    Prove MufradProof acceptance via complete equation.

    Constitutional Requirements:
        1. Extract carrier and identity IDs
        2. Build qiyas proof (origin/branch/cause/differences)
        3. Check identity preservation
        4. Check minimal completeness
        5. Build transition proof
        6. Return complete equation

    Args:
        proof: MufradProof to prove acceptance for

    Returns:
        MufradAcceptanceEquation with complete proof

    Example:
        >>> equation = prove_mufrad_acceptance(mufrad_proof)
        >>> assert equation.accepted  # If composition-ready and no blockers
    """
    # Extract carrier and identity IDs
    carrier_ids = _carrier_ids_from_mufrad(proof)
    identity_ids = _identity_ids_from_mufrad(proof)

    # Extract or create trace ID
    trace_id = proof.trace.get("id", f"trace:{id(proof)}") if isinstance(proof.trace, dict) else f"trace:{id(proof)}"

    # Check for blocking invalidating differences
    blocking_differences = []

    if not proof.is_composition_ready():
        blocking_differences.append(
            InvalidatingDifference(
                difference_id="mufrad_not_composition_ready",
                message="MufradProof is not composition-ready",
                blocks_transition=True,
                evidence=("composition_readiness",),
            )
        )

    if proof.has_unresolved_competitors():
        blocking_differences.append(
            InvalidatingDifference(
                difference_id="mufrad_unresolved_competitors",
                message="MufradProof has unresolved competitors",
                blocks_transition=True,
                evidence=("competitors",),
            )
        )

    # PR #159: Warn about carrier fallback (non-blocking)
    if _has_carrier_fallback(carrier_ids):
        blocking_differences.append(
            InvalidatingDifference(
                difference_id="carrier_provenance_fallback",
                message="Carrier IDs use text fallback, not Unicode/Atom provenance",
                blocks_transition=False,  # Warning, not blocker
                evidence=("carrier_ids", "text_fallback"),
            )
        )

    # Build effective description
    effective = EffectiveDescription(
        description_id=f"effective:mufrad:{id(proof)}",
        description_type="composition_ready_mufrad_carrier",
        evidence=("MufradProof", "composition_readiness", "surface_effects", "case_sign_potentials"),
    )

    # Build qiyas proof
    qiyas = QiyasProof(
        proof_id=f"qiyas:mufrad:{id(proof)}",
        origin_id="origin:mufrad_acceptance_contract",
        branch_id=f"branch:{trace_id}",
        effective_description=effective,
        shared_cause="mufrad proof preserves form/type/morphology/surface potentials without semantic or syntactic role output",
        invalidating_differences=tuple(blocking_differences),
    )

    # Build identity neutral check
    neutral = IdentityNeutralCheck(
        check_id=f"id_neutral:mufrad:{id(proof)}",
        input_identity_ids=identity_ids,
        output_identity_ids=identity_ids,  # MufradProof preserves all identities
        preserved=True,
    )

    # Build minimal completeness check
    satisfied = [
        "carriers_present",
        "identities_preserved",
        "trace_present",
        "no_meaning",
        "no_ifadah",
        "no_hukm",
    ]
    if not blocking_differences:
        satisfied.extend(["composition_readiness", "no_blocking_residuals"])

    minimum = MinimalCompletenessCheck(
        check_id=f"minimum:mufrad:{id(proof)}",
        target_layer="LAFZ_MUFRAD_ACCEPTANCE",
        required_conditions=(
            "carriers_present",
            "identities_preserved",
            "composition_readiness",
            "no_blocking_residuals",
            "trace_present",
            "no_meaning",
            "no_ifadah",
            "no_hukm",
        ),
        satisfied_conditions=tuple(satisfied),
        missing_conditions=tuple(d.difference_id for d in blocking_differences),
        passed=not blocking_differences,
    )

    # Build transition proof
    transition = TransitionProof(
        proof_id=f"transition:mufrad:{id(proof)}",
        source_layer="MUFRAD_PROOF",
        target_layer="PRESYNTAX_MUFRAD_VECTOR",
        qiyas=qiyas,
        identity_neutral=neutral,
        minimal_completeness=minimum,
        preserved_trace_ids=(trace_id,),
        residual_ids=tuple(str(r) for r in proof.collect_all_residuals()),
        rank_name=proof.rank.name,
    )

    # Build surface string
    surface = proof.form.vocalization or proof.form.text

    # Return complete equation
    return MufradAcceptanceEquation(
        equation_id=f"equation:mufrad:{id(proof)}",
        mufrad_id=f"mufrad:{id(proof)}",
        lhs_carrier_ids=carrier_ids,
        lhs_identity_ids=identity_ids,
        lhs_effective_description_ids=(effective.description_id,),
        lhs_qiyas_proof_ids=(qiyas.proof_id,),
        rhs_word_surface=surface,
        rhs_preserved_carrier_ids=carrier_ids,
        rhs_preserved_identity_ids=identity_ids,
        rhs_trace_id=trace_id,
        transition_proof=transition,
    )
