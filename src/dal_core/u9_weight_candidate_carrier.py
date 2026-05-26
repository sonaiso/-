"""
U₉ WeightCandidateCarrier (حامل مرشح الوزن)

Domain: U₉ = WeightCandidateCarrier
Transition: U₈ (RootStemCandidate) → U₉ (WeightCandidate)
Purpose: Weight pattern determination under constitutional governance

Constitutional Governance:
    This layer operates under STRICT AlgebraicDecisionCore governance.

    CRITICAL LAW:
        Layer does not own Governor.
        Governor owns Transition Permission.

    Execution Pattern:
        Pipeline/Orchestrator owns AlgebraicDecisionCore
          → asks: approve U₈→U₉ transition?
          → receives DecisionAudit
          → if approved: creates ApprovedTransitionContext
          → passes context to U₉
          → U₉ verifies context and executes

    Constitutional Requirements (12 Laws):
        1. ✓ No U₉ execution without ApprovedTransitionContext
        2. ✓ No U₉ instantiation of AlgebraicDecisionCore
        3. ✓ No execution with wrong transition context (must be U₈→U₉)
        4. ✓ No execution in non-WEIGHT_DOMAIN
        5. ✓ No execution without ROOT_MATERIAL_IDENTITY or STEM_IDENTITY
        6. ✓ No SEMANTIC_IDENTITY output
        7. ✓ No HUKM_IDENTITY output
        8. ✓ No FUNCTIONAL_RELATION_IDENTITY output
        9. ✓ U₇-C agreement edges preserved as external trace
       10. ✓ Residual audit preserved
       11. ✓ Candidate rank preserved (not certificate)
       12. ✓ Golden path execution

Domain Boundaries:
    Forbidden in WEIGHT_DOMAIN:
        ✗ Meaning determination (معنى)
        ✗ Syntactic role (فاعل نحوي)
        ✗ I'rab judgment (إعراب)
        ✗ Hukm (حكم)
        ✗ Semantic derivation (اشتقاق معنوي)
        ✗ Functional assignment (وظيفة)

    Permitted in WEIGHT_DOMAIN:
        ✓ Weight pattern (وزن)
        ✓ Morphological template (قالب صرفي)
        ✓ F-'-L mapping (فاء-عين-لام)

Key Principle:
    U₉ is WeightCandidateCarrier ONLY.
    Not WeightCertifier.
    Not MeaningDeterminer.
    Not SyntacticRoleAssigner.

Architecture:
    U₀ → U₁ → U₂p → U₂s → U₃ → U₄ → U₅ → U₆ →
    U₇(A/B/C) → U₈ → U₉ (this layer)

PR: U9-WEIGHT-CANDIDATE-CARRIER
Created: 2026-05-26
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, FrozenSet, Any
from uuid import uuid4

from dal_core.approved_transition_context import ApprovedTransitionContext
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.identity_registry import IdentityType
from dal_core.domain_registry import DomainType
from dal_core.foundation import Rank
from dal_core.residuals import Residual, ResidualType, ResidualSeverity


# ============================================================================
# Constitutional Validation
# ============================================================================

def validate_approved_context_for_u9(
    context: Optional[ApprovedTransitionContext],
    u8_input: Dict[str, Any]
) -> None:
    """
    Validate ApprovedTransitionContext for U₉ execution.

    Constitutional Laws Enforced:
        1. Context must be present (not None)
        2. Context must be for U₈→U₉ transition
        3. Context domain must be WEIGHT_DOMAIN
        4. Context input_identity must be ROOT_MATERIAL_IDENTITY or STEM_IDENTITY
        5. Context output_identity must be WEIGHT_IDENTITY
        6. Context output_identity must NOT be semantic/hukm/syntactic

    Args:
        context: ApprovedTransitionContext (or None)
        u8_input: Input from U₈

    Raises:
        ValueError: If any constitutional law is violated
    """
    # Law 1: Context required
    if context is None:
        raise ValueError(
            "Constitutional Violation: U₉ execution requires ApprovedTransitionContext. "
            "No U₉ execution without governance approval. "
            "Pipeline/Orchestrator must call AlgebraicDecisionCore.decide_transition() first."
        )

    # Law 2: Must be U₈→U₉ transition
    if context.from_layer != ExecutionLayer.U8_ROOT_STEM:
        raise ValueError(
            f"Constitutional Violation: ApprovedTransitionContext.from_layer must be U8_ROOT_STEM, "
            f"got {context.from_layer}. "
            f"Each context is transition-specific and cannot be reused."
        )

    if context.to_layer != ExecutionLayer.U9_WEIGHT:
        raise ValueError(
            f"Constitutional Violation: ApprovedTransitionContext.to_layer must be U9_WEIGHT, "
            f"got {context.to_layer}. "
            f"This context is not for U₉."
        )

    # Law 3: Domain must be WEIGHT_DOMAIN
    if context.domain != DomainType.WEIGHT_DOMAIN:
        raise ValueError(
            f"Constitutional Violation: U₉ operates ONLY in WEIGHT_DOMAIN, "
            f"got {context.domain}. "
            f"Domain boundaries are constitutional. "
            f"No cross-domain execution allowed."
        )

    # Law 4: Input identity must be ROOT_MATERIAL_IDENTITY or STEM_IDENTITY
    valid_input_identities = {
        IdentityType.ROOT_MATERIAL_IDENTITY,
        IdentityType.STEM_IDENTITY,
    }
    if context.input_identity not in valid_input_identities:
        raise ValueError(
            f"Constitutional Violation: U₉ input_identity must be ROOT_MATERIAL_IDENTITY or STEM_IDENTITY, "
            f"got {context.input_identity}. "
            f"U₉ operates on root/stem material, not other identities."
        )

    # Law 5: Output identity must be WEIGHT_IDENTITY
    if context.output_identity != IdentityType.WEIGHT_IDENTITY:
        raise ValueError(
            f"Constitutional Violation: U₉ output_identity must be WEIGHT_IDENTITY, "
            f"got {context.output_identity}. "
            f"U₉ produces weight candidates, not other identities."
        )

    # Law 6: Output identity must NOT be semantic/hukm/syntactic
    forbidden_outputs = {
        IdentityType.SEMANTIC_IDENTITY,
        IdentityType.HUKM_IDENTITY,
        IdentityType.FUNCTIONAL_RELATION_IDENTITY,
        IdentityType.AMIL_IDENTITY,
        IdentityType.MAAMUL_IDENTITY,
    }
    if context.output_identity in forbidden_outputs:
        raise ValueError(
            f"Constitutional Violation: U₉ MUST NOT produce {context.output_identity}. "
            f"Forbidden outputs: {forbidden_outputs}. "
            f"U₉ produces WEIGHT_IDENTITY only (morphological pattern, not meaning/hukm/syntax)."
        )


# ============================================================================
# U₉ Weight Candidate Result
# ============================================================================

@dataclass(frozen=True)
class WeightCandidateResult:
    """
    Result from U₉ WeightCandidateCarrier.

    Constitutional contract:
        - Contains ONLY weight pattern information
        - Does NOT contain meaning/hukm/syntactic role
        - Preserves agreement edges as external trace
        - Preserves residuals
        - Preserves rank (candidate, not certificate unless evidenced)
    """
    uid: str
    weight_pattern: Optional[str]  # e.g., "فَاعِل", "مَفْعُول"
    morphological_template: Optional[str]  # e.g., "CaCiC", "mafCuuC"
    faa_ayn_lam_mapping: Optional[Dict[str, str]]  # e.g., {"ك": "ف", "ت": "ع", "ب": "ل"}

    # Constitutional preservation
    output_identity: IdentityType
    domain: DomainType
    rank: Rank
    residuals: Tuple[Residual, ...]
    trace: Tuple[str, ...]

    # External trace (NOT consumed by U₉)
    external_agreement_trace: Tuple[str, ...]  # From U₇-C, preserved for U₁₃+

    # Source traceability
    source_u8_root_candidates: Tuple[Tuple[str, ...], ...]
    source_u8_pattern_candidate: Optional[str]

    # Governance audit
    approved_by_decision_id: str
    transition_id: str

    def __post_init__(self):
        """Verify constitutional constraints."""
        # Verify output_identity is WEIGHT_IDENTITY
        if self.output_identity != IdentityType.WEIGHT_IDENTITY:
            raise ValueError(
                f"WeightCandidateResult.output_identity must be WEIGHT_IDENTITY, "
                f"got {self.output_identity}"
            )

        # Verify domain is WEIGHT_DOMAIN
        if self.domain != DomainType.WEIGHT_DOMAIN:
            raise ValueError(
                f"WeightCandidateResult.domain must be WEIGHT_DOMAIN, "
                f"got {self.domain}"
            )

        # Verify no forbidden attributes
        forbidden_attrs = [
            "meaning", "murad", "hukm", "haqiqa_majaz",
            "syntactic_role", "functional_relation", "i3rab_status",
            "semantic_identity", "semantic_derivation"
        ]
        for attr in forbidden_attrs:
            if hasattr(self, attr):
                raise ValueError(
                    f"Constitutional Violation: WeightCandidateResult MUST NOT contain '{attr}' field. "
                    f"Weight ⊬ Meaning, Weight ⊬ Hukm, Weight ⊬ Syntax."
                )


# ============================================================================
# U₉ Weight Candidate Carrier (Main Function)
# ============================================================================

def weight_candidate_carrier_9(
    u8_input: Dict[str, Any],
    approved_context: Optional[ApprovedTransitionContext]
) -> Dict[str, Any]:
    """
    U₉ Weight Candidate Carrier (حامل مرشح الوزن)

    Constitutional Execution Pattern:
        1. Validate ApprovedTransitionContext (constitutional requirement)
        2. Extract weight pattern candidates from root/stem
        3. Preserve agreement edges as external trace (not consumed)
        4. Preserve residuals (not deleted)
        5. Return weight candidate (not certificate unless evidenced)

    Args:
        u8_input: Input from U₈ RootStemCandidateCarrier
            Required keys:
                - root_candidates: List[Tuple[str, ...]]
                - trace: Tuple[str, ...]
            Optional keys:
                - stem_candidates: List[str]
                - pattern_candidate: str
                - agreement_edge_ids: List[str]
                - residuals: List[Residual]
                - rank: Rank

        approved_context: ApprovedTransitionContext from AlgebraicDecisionCore
            REQUIRED. Cannot be None.
            Must be for U₈→U₉ transition in WEIGHT_DOMAIN.

    Returns:
        Dict with weight candidate information

    Raises:
        ValueError: If constitutional laws are violated

    Constitutional Laws Enforced:
        ✓ No execution without ApprovedTransitionContext
        ✓ No execution with wrong context
        ✓ No execution in wrong domain
        ✓ No forbidden identity outputs
        ✓ Agreement edges preserved
        ✓ Residuals preserved
        ✓ Rank appropriate
    """
    # ========================================================================
    # Step 1: Constitutional Validation
    # ========================================================================

    validate_approved_context_for_u9(approved_context, u8_input)

    # ========================================================================
    # Step 2: Extract Input
    # ========================================================================

    root_candidates = u8_input.get("root_candidates", [])
    stem_candidates = u8_input.get("stem_candidates", [])
    pattern_candidate = u8_input.get("pattern_candidate")
    agreement_edge_ids = u8_input.get("agreement_edge_ids", [])
    input_residuals = u8_input.get("residuals", [])
    input_rank = u8_input.get("rank", Rank.CANDIDATE)
    input_trace = u8_input.get("trace", ())

    # ========================================================================
    # Step 3: Weight Pattern Determination (Allowed Competency)
    # ========================================================================

    # Determine weight pattern from pattern_candidate
    # This is MORPHOLOGICAL determination, NOT semantic
    weight_pattern = None
    morphological_template = None
    faa_ayn_lam_mapping = None

    if pattern_candidate:
        weight_pattern = pattern_candidate  # e.g., "فَاعِل"

        # Extract morphological template (structural pattern)
        # This is surface-to-slot mapping, NOT meaning
        if root_candidates and len(root_candidates) > 0:
            root = root_candidates[0]
            if len(root) == 3:  # Triliteral
                faa_ayn_lam_mapping = {
                    root[0]: "ف",
                    root[1]: "ع",
                    root[2]: "ل",
                }
                # Derive template from pattern
                morphological_template = derive_template(pattern_candidate)

    # ========================================================================
    # Step 4: Preserve Agreement Edges as External Trace
    # ========================================================================

    # Agreement edges from U₇-C are NOT consumed by U₉
    # They are preserved for higher layers (U₁₃+)
    # This implements Law #9: حفظ حواف الاتفاق من U₇-C كأثر خارجي
    external_agreement_trace = tuple(agreement_edge_ids)

    # ========================================================================
    # Step 5: Preserve Residuals
    # ========================================================================

    # Residuals are NOT deleted, they are preserved
    # This implements Law #10: حفظ تدقيق البقايا
    preserved_residuals = list(input_residuals)

    # Add any new residuals from U₉ analysis
    if not weight_pattern:
        preserved_residuals.append(Residual(
            type=ResidualType.WAZN_UNRESOLVED,
            severity=ResidualSeverity.WARNING,
            message="No weight pattern candidate identified",
            location="U₉"
        ))

    # ========================================================================
    # Step 6: Rank Preservation (Constitutional Law #11)
    # ========================================================================

    # Rank does NOT inflate to CERTIFICATE without evidence
    # U₉ outputs are CANDIDATES, not CERTIFICATES
    output_rank = input_rank

    # Only elevate to HYPOTHESIS if we have pattern candidate
    if weight_pattern and output_rank == Rank.CANDIDATE:
        output_rank = Rank.HYPOTHESIS

    # Do NOT elevate to CERTIFICATE (requires strong evidence from higher layers)

    # ========================================================================
    # Step 7: Build Trace
    # ========================================================================

    output_trace = input_trace + ("u9",)

    # ========================================================================
    # Step 8: Build Result
    # ========================================================================

    result = WeightCandidateResult(
        uid=str(uuid4()),
        weight_pattern=weight_pattern,
        morphological_template=morphological_template,
        faa_ayn_lam_mapping=faa_ayn_lam_mapping,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        domain=DomainType.WEIGHT_DOMAIN,
        rank=output_rank,
        residuals=tuple(preserved_residuals),
        trace=output_trace,
        external_agreement_trace=external_agreement_trace,
        source_u8_root_candidates=tuple(tuple(r) for r in root_candidates),
        source_u8_pattern_candidate=pattern_candidate,
        approved_by_decision_id=approved_context.get_decision_id(),
        transition_id=approved_context.get_transition_id(),
    )

    # ========================================================================
    # Step 9: Return as Dict for Compatibility
    # ========================================================================

    return {
        "uid": result.uid,
        "weight_pattern": result.weight_pattern,
        "morphological_template": result.morphological_template,
        "faa_ayn_lam_mapping": result.faa_ayn_lam_mapping,
        "output_identity": result.output_identity,
        "domain": result.domain,
        "rank": result.rank,
        "residuals": result.residuals,
        "trace": result.trace,
        "external_agreement_trace": result.external_agreement_trace,
        "source_u8_root_candidates": result.source_u8_root_candidates,
        "approved_by_decision_id": result.approved_by_decision_id,
        "transition_id": result.transition_id,
    }


# ============================================================================
# Helper Functions
# ============================================================================

def derive_template(pattern: str) -> str:
    """
    Derive morphological template from Arabic pattern.

    This is STRUCTURAL analysis, NOT semantic.

    Examples:
        فَاعِل → CaaCiC
        مَفْعُول → mafCuuC

    Args:
        pattern: Arabic pattern (e.g., "فَاعِل")

    Returns:
        Structural template (e.g., "CaaCiC")
    """
    # Simple template derivation (can be expanded)
    # This is morphological structure, NOT meaning

    template_map = {
        "فَاعِل": "CaaCiC",
        "مَفْعُول": "mafCuuC",
        "فَعَلَ": "CaCaC",
        "فِعْل": "CiCC",
        "فَعْل": "CaCC",
    }

    return template_map.get(pattern, "unknown_template")


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    "WeightCandidateResult",
    "weight_candidate_carrier_9",
    "validate_approved_context_for_u9",
]
