"""
U₉ WeightCandidateCarrier Constitutional Tests (الاختبارات الدستورية لحامل مرشح الوزن)

Constitutional Laws Under Test:
    1. No U₉ execution without ApprovedTransitionContext
    2. No U₉ instantiation of AlgebraicDecisionCore
    3. No execution with wrong transition context (not U₈→U₉)
    4. No execution in non-WEIGHT_DOMAIN
    5. No execution without ROOT_MATERIAL_IDENTITY or STEM_IDENTITY
    6. No SEMANTIC_IDENTITY output
    7. No HUKM_IDENTITY output
    8. No FUNCTIONAL_RELATION_IDENTITY output
    9. U₇-C agreement edges preserved as external trace
    10. Residual audit preserved
    11. Candidate rank preserved (not elevated to certificate without evidence)
    12. Golden path: valid weight candidate with all governance

Forbidden Competencies:
    ✗ Meaning determination (معنى)
    ✗ Syntactic role (فاعل نحوي)
    ✗ I'rab judgment (إعراب)
    ✗ Hukm (حكم)
    ✗ Semantic derivation (اشتقاق معنوي)
    ✗ Functional assignment (وظيفة)

Allowed Competencies:
    ✓ Weight pattern (وزن)
    ✓ Morphological template (قالب صرفي)
    ✓ F-'-L mapping (فاء-عين-لام)

PR: U9-WEIGHT-CANDIDATE-CARRIER
Created: 2026-05-26
"""

import pytest
from uuid import uuid4

from dal_core.approved_transition_context import (
    ApprovedTransitionContext,
    create_approved_context,
)
from dal_core.algebraic_decision_core import (
    AlgebraicDecisionCore,
    DecisionAudit,
    CPBStatus,
)
from dal_core.execution_layer_registry import ExecutionLayer
from dal_core.identity_registry import IdentityType
from dal_core.domain_registry import DomainType
from dal_core.foundation import Rank
from dal_core.residuals import Residual, ResidualType, ResidualSeverity
from dal_core.evidence import Evidence, make_evidence
from dal_core.ranks import LughaRank


# ============================================================================
# Constitutional Test 1: Reject Without ApprovedTransitionContext
# ============================================================================

def test_u9_rejects_without_approved_transition_context():
    """
    Constitutional Law 1: لا وزن بلا ApprovedTransitionContext

    U₉ MUST reject execution if ApprovedTransitionContext is not provided.

    This is the first line of constitutional defense:
    No layer may execute without governance approval.
    """
    # Import the function we'll create
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Attempt to call U₉ without ApprovedTransitionContext
    # Should raise ValueError or return rejection

    # Mock U₈ input (valid structure)
    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "stem_candidates": ["كتب"],
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    with pytest.raises(ValueError) as exc_info:
        weight_candidate_carrier_9(
            u8_input=u8_input,
            approved_context=None  # KEY: No context provided
        )

    assert "ApprovedTransitionContext" in str(exc_info.value)
    assert "requires" in str(exc_info.value).lower()


# ============================================================================
# Constitutional Test 2: Reject Direct AlgebraicDecisionCore Instantiation
# ============================================================================

def test_u9_rejects_direct_algebraic_decision_core_instantiation():
    """
    Constitutional Law 2: لا AlgebraicDecisionCore داخل U₉

    U₉ MUST NOT instantiate AlgebraicDecisionCore internally.

    This would be constitutional violation:
    "The guard inside the guarded breaks constitutional meaning."

    Pipeline/Orchestrator owns AlgebraicDecisionCore.
    Layer receives ApprovedTransitionContext as proof.
    """
    # This test verifies that u9_weight_candidate_carrier.py does NOT contain:
    # - AlgebraicDecisionCore() instantiation
    # - core = AlgebraicDecisionCore()
    # - Any creation of decision core

    import inspect
    from dal_core import u9_weight_candidate_carrier

    # Get source code of the module
    source = inspect.getsource(u9_weight_candidate_carrier)

    # Check that AlgebraicDecisionCore() is NOT instantiated
    assert "AlgebraicDecisionCore()" not in source, \
        "U₉ MUST NOT instantiate AlgebraicDecisionCore - constitutional violation"

    # Also check for common patterns
    assert "core = AlgebraicDecisionCore" not in source
    assert "decision_core = AlgebraicDecisionCore" not in source

    # Importing AlgebraicDecisionCore for type hints is OK
    # But instantiation is forbidden


# ============================================================================
# Constitutional Test 3: Reject Context Not For U₈→U₉
# ============================================================================

def test_u9_rejects_context_not_for_u8_to_u9():
    """
    Constitutional Law 3: السياق يجب أن يكون للانتقال U₈→U₉ فقط

    U₉ MUST reject ApprovedTransitionContext that is NOT for U₈→U₉ transition.

    Each context is transition-specific and cannot be reused for different transitions.
    """
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Create wrong transition context (e.g., U₇→U₈)
    wrong_audit = DecisionAudit(
        decision_id=str(uuid4()),
        transition_id="U7_to_U8",  # WRONG: Not U₈→U₉
        from_layer=ExecutionLayer.U7C_CLAUSE_SURFACE_AGREEMENT,
        to_layer=ExecutionLayer.U8_ROOT_STEM,  # WRONG
        input_identity=IdentityType.LICENSED_ROOT_INPUT_IDENTITY,
        output_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        domain=DomainType.ROOT_STEM_DOMAIN,
        function="root_stem_extraction",
        gate="Gate₇₈",
        evidence=(),
        rank=Rank.CANDIDATE,
        residuals=(),
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=(),
        timestamp="2026-05-26T19:00:00Z"
    )

    wrong_context = create_approved_context(
        audit=wrong_audit,
        existing_identities=frozenset([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.LICENSED_ROOT_INPUT_IDENTITY,
        ])
    )

    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    with pytest.raises(ValueError) as exc_info:
        weight_candidate_carrier_9(
            u8_input=u8_input,
            approved_context=wrong_context
        )

    assert "U8" in str(exc_info.value) or "U9" in str(exc_info.value)
    assert "transition" in str(exc_info.value).lower()


# ============================================================================
# Constitutional Test 4: Reject Non-WEIGHT_DOMAIN
# ============================================================================

def test_u9_rejects_non_weight_domain():
    """
    Constitutional Law 4: لا تنفيذ خارج مجال الوزن

    U₉ MUST reject execution if domain is NOT WEIGHT_DOMAIN.

    Domain boundaries are constitutional:
    - WEIGHT_DOMAIN: allowed
    - SYNTAX_DOMAIN: forbidden
    - SEMANTICS_DOMAIN: forbidden
    - ROOT_STEM_DOMAIN: wrong layer
    """
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Create context with wrong domain (e.g., SYNTAX_DOMAIN)
    wrong_audit = DecisionAudit(
        decision_id=str(uuid4()),
        transition_id="U8_to_U9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        domain=DomainType.SYNTAX_DOMAIN,  # WRONG: Should be WEIGHT_DOMAIN
        function="weight_determination",
        gate="Gate₈₉",
        evidence=(),
        rank=Rank.CANDIDATE,
        residuals=(),
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=(),
        timestamp="2026-05-26T19:00:00Z"
    )

    wrong_context = create_approved_context(
        audit=wrong_audit,
        existing_identities=frozenset([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,
        ])
    )

    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    with pytest.raises(ValueError) as exc_info:
        weight_candidate_carrier_9(
            u8_input=u8_input,
            approved_context=wrong_context
        )

    assert "WEIGHT_DOMAIN" in str(exc_info.value) or "domain" in str(exc_info.value).lower()


# ============================================================================
# Constitutional Test 5: Reject Missing Root or Stem Identity
# ============================================================================

def test_u9_rejects_missing_root_or_stem_identity():
    """
    Constitutional Law 5: لا وزن بلا هوية جذر أو جذع

    U₉ MUST reject if input_identity is NOT:
    - ROOT_MATERIAL_IDENTITY, or
    - STEM_IDENTITY

    These are the ONLY valid identities for U₉ input.
    """
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Create context with wrong input identity (e.g., PHONETIC_IDENTITY)
    wrong_audit = DecisionAudit(
        decision_id=str(uuid4()),
        transition_id="U8_to_U9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.PHONETIC_IDENTITY,  # WRONG: Not root/stem
        output_identity=IdentityType.WEIGHT_IDENTITY,
        domain=DomainType.WEIGHT_DOMAIN,
        function="weight_determination",
        gate="Gate₈₉",
        evidence=(),
        rank=Rank.CANDIDATE,
        residuals=(),
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=(),
        timestamp="2026-05-26T19:00:00Z"
    )

    wrong_context = create_approved_context(
        audit=wrong_audit,
        existing_identities=frozenset([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.PHONETIC_IDENTITY,
        ])
    )

    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    with pytest.raises(ValueError) as exc_info:
        weight_candidate_carrier_9(
            u8_input=u8_input,
            approved_context=wrong_context
        )

    assert "identity" in str(exc_info.value).lower()


# ============================================================================
# Constitutional Test 6: Reject Semantic Identity Output
# ============================================================================

def test_u9_rejects_semantic_identity_output():
    """
    Constitutional Law 6: لا هوية دلالية في الخرج

    U₉ MUST NOT produce SEMANTIC_IDENTITY output.

    Forbidden: صيغة فاعل → معنى الفاعلية (semantic meaning)
    Allowed: صيغة فاعل → وزن فَاعِل (morphological pattern)

    Semantic identity belongs to U₁₄-U₁₅, NOT U₉.
    """
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Create context claiming semantic output (constitutional violation)
    wrong_audit = DecisionAudit(
        decision_id=str(uuid4()),
        transition_id="U8_to_U9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.SEMANTIC_IDENTITY,  # WRONG: Semantic output
        domain=DomainType.WEIGHT_DOMAIN,
        function="weight_determination",
        gate="Gate₈₉",
        evidence=(),
        rank=Rank.CANDIDATE,
        residuals=(),
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=(),
        timestamp="2026-05-26T19:00:00Z"
    )

    wrong_context = create_approved_context(
        audit=wrong_audit,
        existing_identities=frozenset([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,
        ])
    )

    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    with pytest.raises(ValueError) as exc_info:
        weight_candidate_carrier_9(
            u8_input=u8_input,
            approved_context=wrong_context
        )

    assert "SEMANTIC" in str(exc_info.value) or "semantic" in str(exc_info.value).lower()


# ============================================================================
# Constitutional Test 7: Reject Hukm Identity Output
# ============================================================================

def test_u9_rejects_hukm_identity_output():
    """
    Constitutional Law 7: لا هوية حكم في الخرج

    U₉ MUST NOT produce HUKM_IDENTITY output.

    Hukm (grammatical judgment) belongs to U₁₃+, NOT U₉.
    Weight is form, NOT judgment.
    """
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Create context claiming hukm output (constitutional violation)
    wrong_audit = DecisionAudit(
        decision_id=str(uuid4()),
        transition_id="U8_to_U9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.HUKM_IDENTITY,  # WRONG: Hukm output
        domain=DomainType.WEIGHT_DOMAIN,
        function="weight_determination",
        gate="Gate₈₉",
        evidence=(),
        rank=Rank.CANDIDATE,
        residuals=(),
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=(),
        timestamp="2026-05-26T19:00:00Z"
    )

    wrong_context = create_approved_context(
        audit=wrong_audit,
        existing_identities=frozenset([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,
        ])
    )

    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    with pytest.raises(ValueError) as exc_info:
        weight_candidate_carrier_9(
            u8_input=u8_input,
            approved_context=wrong_context
        )

    assert "HUKM" in str(exc_info.value) or "hukm" in str(exc_info.value).lower()


# ============================================================================
# Constitutional Test 8: Reject Syntactic Role Output
# ============================================================================

def test_u9_rejects_syntactic_role_output():
    """
    Constitutional Law 8: لا دور نحوي في الخرج

    U₉ MUST NOT produce FUNCTIONAL_RELATION_IDENTITY output.

    Forbidden: صيغة فاعل → الفاعل النحوي (syntactic agent)
    Allowed: صيغة فاعل → وزن فَاعِل (morphological pattern)

    Syntactic role belongs to U₁₃, NOT U₉.
    """
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Create context claiming functional relation output (constitutional violation)
    wrong_audit = DecisionAudit(
        decision_id=str(uuid4()),
        transition_id="U8_to_U9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.FUNCTIONAL_RELATION_IDENTITY,  # WRONG
        domain=DomainType.WEIGHT_DOMAIN,
        function="weight_determination",
        gate="Gate₈₉",
        evidence=(),
        rank=Rank.CANDIDATE,
        residuals=(),
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=(),
        timestamp="2026-05-26T19:00:00Z"
    )

    wrong_context = create_approved_context(
        audit=wrong_audit,
        existing_identities=frozenset([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,
        ])
    )

    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    with pytest.raises(ValueError) as exc_info:
        weight_candidate_carrier_9(
            u8_input=u8_input,
            approved_context=wrong_context
        )

    assert "FUNCTIONAL_RELATION" in str(exc_info.value) or "syntactic" in str(exc_info.value).lower()


# ============================================================================
# Constitutional Test 9: Preserve U₇-C Agreement Edges as External Trace
# ============================================================================

def test_u9_preserves_u7c_agreement_edges_as_external_trace():
    """
    Constitutional Law 9: حفظ حواف الاتفاق من U₇-C كأثر خارجي

    U₉ MUST preserve agreement_edge_ids from U₇-C as external trace.

    Agreement edges are NOT consumed/interpreted by U₉.
    They are preserved for higher layers (U₁₃+).

    This implements the law from #111:
    "U₈ يحفظ أثر U₇-C ولا يبتلع حافة الاتفاق"
    """
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Create valid approved context
    audit = DecisionAudit(
        decision_id=str(uuid4()),
        transition_id="U8_to_U9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        domain=DomainType.WEIGHT_DOMAIN,
        function="weight_pattern_determination",
        gate="Gate₈₉",
        evidence=(),
        rank=Rank.CANDIDATE,
        residuals=(),
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=(),
        timestamp="2026-05-26T19:00:00Z"
    )

    context = create_approved_context(
        audit=audit,
        existing_identities=frozenset([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,
        ])
    )

    # U₈ input with agreement edges from U₇-C
    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "stem_candidates": ["كتب"],
        "agreement_edge_ids": ["edge_123", "edge_456"],  # From U₇-C
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    # Execute U₉
    result = weight_candidate_carrier_9(
        u8_input=u8_input,
        approved_context=context
    )

    # Verify agreement edges preserved as external trace
    assert "agreement_edge_ids" in result or "external_agreement_trace" in result

    # Verify NOT consumed/interpreted
    assert "agreement_interpretation" not in result
    assert "agreement_resolution" not in result


# ============================================================================
# Constitutional Test 10: Preserve Residual Audit
# ============================================================================

def test_u9_preserves_residual_audit():
    """
    Constitutional Law 10: حفظ تدقيق البقايا

    U₉ MUST preserve all residuals from upstream layers.

    Residuals are NOT deleted, they are:
    - Preserved (carried forward)
    - Augmented (new residuals added)
    - Discharged (marked as resolved if evidence allows)

    But NEVER deleted without trace.
    """
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Create valid approved context
    audit = DecisionAudit(
        decision_id=str(uuid4()),
        transition_id="U8_to_U9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        domain=DomainType.WEIGHT_DOMAIN,
        function="weight_pattern_determination",
        gate="Gate₈₉",
        evidence=(),
        rank=Rank.CANDIDATE,
        residuals=(),  # No blocking residuals in audit
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=(),
        timestamp="2026-05-26T19:00:00Z"
    )

    context = create_approved_context(
        audit=audit,
        existing_identities=frozenset([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,
        ])
    )

    # U₈ input with residuals
    upstream_residual = Residual(
        type=ResidualType.ROOT_UNRESOLVED,
        severity=ResidualSeverity.WARNING,
        message="Root candidate ambiguity: ك-ت-ب vs ك-ت-ب",
        location="U8"
    )

    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "residuals": [upstream_residual],
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    # Execute U₉
    result = weight_candidate_carrier_9(
        u8_input=u8_input,
        approved_context=context
    )

    # Verify residuals preserved
    assert "residuals" in result
    assert len(result["residuals"]) > 0

    # Verify upstream residual still present (not deleted)
    residual_types = [r.type for r in result["residuals"]]
    assert ResidualType.ROOT_UNRESOLVED in residual_types


# ============================================================================
# Constitutional Test 11: Preserve Candidate Rank (Not Certificate)
# ============================================================================

def test_u9_preserves_candidate_rank_not_certificate():
    """
    Constitutional Law 11: حفظ رتبة المرشح (ليس الشهادة)

    U₉ MUST NOT elevate rank to CERTIFICATE without sufficient evidence.

    Rank progression law:
    - ZERO → CANDIDATE: allowed (opening path)
    - CANDIDATE → HYPOTHESIS: allowed (with weak evidence)
    - HYPOTHESIS → CERTIFICATE: requires strong evidence

    U₉ outputs are CANDIDATES, not CERTIFICATES (unless strong evidence present).
    """
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Create valid approved context with CANDIDATE rank
    audit = DecisionAudit(
        decision_id=str(uuid4()),
        transition_id="U8_to_U9",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        domain=DomainType.WEIGHT_DOMAIN,
        function="weight_pattern_determination",
        gate="Gate₈₉",
        evidence=(),  # No strong evidence
        rank=Rank.CANDIDATE,  # Input is CANDIDATE
        residuals=(),
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=(),
        timestamp="2026-05-26T19:00:00Z"
    )

    context = create_approved_context(
        audit=audit,
        existing_identities=frozenset([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,
        ])
    )

    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "rank": Rank.CANDIDATE,
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    # Execute U₉
    result = weight_candidate_carrier_9(
        u8_input=u8_input,
        approved_context=context
    )

    # Verify rank did NOT inflate to CERTIFICATE
    assert result["rank"] != Rank.CERTIFICATE
    assert result["rank"] in [Rank.ZERO, Rank.CANDIDATE, Rank.HYPOTHESIS]


# ============================================================================
# Constitutional Test 12: Golden Path - Valid Weight Candidate
# ============================================================================

def test_u9_golden_path_weight_candidate():
    """
    Constitutional Test 12: المسار الذهبي - مرشح وزن صحيح

    Golden path test: Valid weight candidate with full constitutional compliance.

    Example: ك ت ب → فَاعِل pattern → كَاتِب weight candidate

    All governance satisfied:
    ✓ ApprovedTransitionContext present
    ✓ U₈→U₉ transition
    ✓ WEIGHT_DOMAIN
    ✓ ROOT_MATERIAL_IDENTITY → WEIGHT_IDENTITY
    ✓ No semantic/hukm/syntactic leaks
    ✓ Agreement edges preserved
    ✓ Residuals preserved
    ✓ Rank appropriate (CANDIDATE)
    """
    from dal_core.u9_weight_candidate_carrier import weight_candidate_carrier_9

    # Create fully valid approved context
    audit = DecisionAudit(
        decision_id=str(uuid4()),
        transition_id="U8_to_U9_weight_candidate",
        from_layer=ExecutionLayer.U8_ROOT_STEM,
        to_layer=ExecutionLayer.U9_WEIGHT,
        input_identity=IdentityType.ROOT_MATERIAL_IDENTITY,
        output_identity=IdentityType.WEIGHT_IDENTITY,
        domain=DomainType.WEIGHT_DOMAIN,
        function="weight_pattern_determination",
        gate="Gate₈₉",
        evidence=(make_evidence("Root k-t-b attested", LughaRank.TAWATUR),),
        rank=Rank.CANDIDATE,
        residuals=(),
        trace=("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
        cpb_status=CPBStatus.APPROVED,
        allowed=True,
        violations=(),
        timestamp="2026-05-26T19:00:00Z"
    )

    context = create_approved_context(
        audit=audit,
        existing_identities=frozenset([
            IdentityType.RAW_SURFACE_IDENTITY,
            IdentityType.ORTHOGRAPHIC_IDENTITY,
            IdentityType.PHONETIC_IDENTITY,
            IdentityType.SYLLABIC_IDENTITY,
            IdentityType.BOUNDARY_IDENTITY,
            IdentityType.LAFZ_IDENTITY,
            IdentityType.PROTECTED_SURFACE_IDENTITY,
            IdentityType.LICENSED_ROOT_INPUT_IDENTITY,
            IdentityType.ROOT_MATERIAL_IDENTITY,
        ])
    )

    # Valid U₈ input
    u8_input = {
        "root_candidates": [("ك", "ت", "ب")],
        "stem_candidates": ["كتب"],
        "pattern_candidate": "فَاعِل",
        "agreement_edge_ids": [],
        "residuals": [],
        "rank": Rank.CANDIDATE,
        "trace": ("u0", "u1", "u2p", "u2s", "u3", "u4", "u5", "u6", "u7a", "u7b", "u7c", "u8"),
    }

    # Execute U₉ - should succeed
    result = weight_candidate_carrier_9(
        u8_input=u8_input,
        approved_context=context
    )

    # Verify valid output structure
    assert result is not None
    assert "weight_candidates" in result or "weight_pattern" in result

    # Verify identity
    assert result["output_identity"] == IdentityType.WEIGHT_IDENTITY

    # Verify domain
    assert result["domain"] == DomainType.WEIGHT_DOMAIN

    # Verify rank appropriate
    assert result["rank"] in [Rank.CANDIDATE, Rank.HYPOTHESIS]

    # Verify trace preserved
    assert "trace" in result
    assert len(result["trace"]) > 0

    # Verify no forbidden fields
    assert "meaning" not in result
    assert "semantic_identity" not in result
    assert "hukm" not in result
    assert "syntactic_role" not in result
    assert "functional_relation" not in result

    # Verify allowed competencies present
    assert "weight_pattern" in result or "morphological_template" in result

    # Success: Constitutional golden path complete
