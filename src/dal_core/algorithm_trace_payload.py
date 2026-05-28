"""
Algorithm Trace Payload Contract (عقد حمولة أثر الخوارزمية)

PR #141: Serialization contract for algorithm traces consumed by GovernedTraceT5.

Constitutional Laws:
    1. AlgorithmTracePayload is replay/audit evidence, NOT ProofObject authority
    2. Payload is non-authoritative: it cannot create constitutional candidates
    3. Payload MUST preserve candidate_id, trace, residuals, rank
    4. Payload MUST include schema_version, source_algorithm, source_layer
    5. Deserialization MUST NOT upgrade rank
    6. Deserialization MUST NOT delete residuals
    7. Deserialization MUST NOT close Ifadah_Dal
    8. Deserialization MUST NOT emit HukmCandidate
    9. Deserialization MUST NOT emit TanzilResult

Forbidden Operations:
    ❌ to_hukm() - Cannot produce hukm from trace
    ❌ to_reality() - Cannot produce reality from trace
    ❌ to_ifadah() - Cannot close ifadah from trace
    ❌ close_ifadah() - Cannot close ifadah from trace
    ❌ create_candidate() - Cannot create new candidates from trace
    ❌ upgrade_rank() - Cannot upgrade epistemic rank
    ❌ delete_residuals() - Cannot delete residuals

Permitted Operations (T5 Consumer Functions):
    ✅ explain_trace - Explain trace to user
    ✅ summarize_candidates - Summarize candidates
    ✅ explain_existing_rank - Explain rank (not assign rank)
    ✅ suggest_repair - Suggest repair (not execute repair)
    ✅ generate_bounded_explanation - Generate natural language explanation

Architecture Position:
    Raw Arabic Input
        → Arabic Algebra Algorithms
        → Candidate Objects (RelationCandidate, WordformCandidate, etc.)
        → AlgorithmTracePayload (THIS MODULE - serialization layer)
        → GovernedTraceT5 (future PR #142)
        → ExplanationCandidate / RepairSuggestionCandidate

Constitutional Formula:
    الجبر = الدستور (Algebra = Constitution)
    الخوارزمية = تنفيذ الدستور (Algorithm = Constitutional Implementation)
    T5 = مستهلك آثار التنفيذ (T5 = Consumer of Implementation Traces)

Supreme Law:
    T5 يستهلك الأثر، ولا ينشئ الحكم الدستوري
    (T5 consumes traces; T5 does not create constitutional facts)

Reference:
    User requirement: PR #141 specification (2026-05-28)

Created: 2026-05-28
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional, FrozenSet

from dal_core.foundation import Rank, ResidualSet


# ============================================================================
# Consumer Operation Classification
# ============================================================================

class TraceConsumerOperation(Enum):
    """
    Allowed operations for trace consumers (e.g., GovernedTraceT5).

    Constitutional Classification:
        PERMITTED: Operations that explain/summarize without creating facts
        FORBIDDEN: Operations that create constitutional facts

    Permitted Operations:
        - explain_trace: Explain algorithmic trace to user
        - summarize_candidates: Summarize candidate set
        - explain_existing_rank: Explain rank (NOT assign rank)
        - suggest_repair: Suggest repair (NOT execute repair)
        - generate_bounded_explanation: Generate natural language explanation

    Forbidden Operations (enforced by test suite):
        - produce_hukm: Create hukm from trace alone
        - close_ifadah: Close ifadah from trace alone
        - create_reality: Create reality claim from trace
        - upgrade_rank: Upgrade epistemic rank without algorithm
        - delete_residuals: Delete residuals without discharge proof
        - create_candidate: Create new candidate without algorithm
    """
    # Permitted operations
    EXPLAIN_TRACE = auto()
    SUMMARIZE_CANDIDATES = auto()
    EXPLAIN_EXISTING_RANK = auto()
    SUGGEST_REPAIR = auto()
    GENERATE_BOUNDED_EXPLANATION = auto()

    # Forbidden operations (declared for testing/validation)
    # These MUST NOT be implemented in any trace consumer
    PRODUCE_HUKM = auto()           # FORBIDDEN
    CLOSE_IFADAH = auto()           # FORBIDDEN
    CREATE_REALITY = auto()         # FORBIDDEN
    UPGRADE_RANK = auto()           # FORBIDDEN
    DELETE_RESIDUALS = auto()       # FORBIDDEN
    CREATE_CANDIDATE = auto()       # FORBIDDEN

    def is_permitted(self) -> bool:
        """Check if operation is constitutionally permitted."""
        permitted = {
            TraceConsumerOperation.EXPLAIN_TRACE,
            TraceConsumerOperation.SUMMARIZE_CANDIDATES,
            TraceConsumerOperation.EXPLAIN_EXISTING_RANK,
            TraceConsumerOperation.SUGGEST_REPAIR,
            TraceConsumerOperation.GENERATE_BOUNDED_EXPLANATION,
        }
        return self in permitted

    def is_forbidden(self) -> bool:
        """Check if operation is constitutionally forbidden."""
        return not self.is_permitted()


# ============================================================================
# Forbidden Jump Declarations
# ============================================================================

@dataclass(frozen=True)
class ForbiddenJumpPayload:
    """
    Declaration of forbidden domain jumps.

    Examples:
        "RelationCandidate -> Hukm"
        "RelationCandidate -> Reality"
        "WordformCandidate -> FinalMeaning"
        "LafzCandidate -> SemanticIdentity"

    Fields:
        from_layer: Source layer
        to_layer: Target layer (forbidden)
        reason: Constitutional reason for prohibition

    Constitutional Law:
        These jumps remain forbidden even in serialized form.
        No trace consumer may execute forbidden jumps.
    """
    from_layer: str
    to_layer: str
    reason: str

    def __post_init__(self):
        """Validate forbidden jump payload."""
        if not self.from_layer:
            raise ValueError("ForbiddenJumpPayload requires non-empty from_layer")
        if not self.to_layer:
            raise ValueError("ForbiddenJumpPayload requires non-empty to_layer")
        if not self.reason:
            raise ValueError("ForbiddenJumpPayload requires non-empty reason")


# ============================================================================
# Allowed Next Layer Declarations
# ============================================================================

@dataclass(frozen=True)
class AllowedNextLayerPayload:
    """
    Declaration of constitutionally allowed next layers.

    Examples:
        "RelationNetworkCandidate -> RelationClosureGate"
        "RelationClosureGate -> IfadahDalClosureGate"
        "IfadahCandidate -> HukmGate"

    Fields:
        current_layer: Current layer
        next_layer: Allowed next layer
        conditions: Optional conditions for transition

    Constitutional Law:
        Allowed transitions must be explicitly declared.
        No implicit jumps permitted.
    """
    current_layer: str
    next_layer: str
    conditions: Tuple[str, ...] = ()

    def __post_init__(self):
        """Validate allowed next layer payload."""
        if not self.current_layer:
            raise ValueError("AllowedNextLayerPayload requires non-empty current_layer")
        if not self.next_layer:
            raise ValueError("AllowedNextLayerPayload requires non-empty next_layer")
        if not isinstance(self.conditions, tuple):
            raise TypeError(f"conditions must be tuple, got {type(self.conditions)}")


# ============================================================================
# Rank Trace Payload
# ============================================================================

@dataclass(frozen=True)
class RankTracePayload:
    """
    Rank trace for audit purposes.

    Constitutional Law:
        Rank is NON-UPGRADING in serialization.
        Deserialization MUST preserve rank exactly as produced by algorithm.

    Fields:
        rank: Epistemic rank (from algorithm output)
        rank_evidence: Evidence supporting this rank
        rank_trace: Trace of rank progression

    Forbidden:
        - Upgrading rank in deserialization
        - Creating CERTIFICATE rank from trace alone
    """
    rank: Rank
    rank_evidence: Tuple[str, ...]
    rank_trace: Tuple[str, ...]

    def __post_init__(self):
        """Validate rank trace payload."""
        if not isinstance(self.rank, Rank):
            raise TypeError(f"rank must be Rank, got {type(self.rank)}")
        if not isinstance(self.rank_evidence, tuple):
            raise TypeError(f"rank_evidence must be tuple, got {type(self.rank_evidence)}")
        if not isinstance(self.rank_trace, tuple):
            raise TypeError(f"rank_trace must be tuple, got {type(self.rank_trace)}")


# ============================================================================
# Residual Trace Payload
# ============================================================================

@dataclass(frozen=True)
class ResidualTracePayload:
    """
    Residual trace for audit purposes.

    Constitutional Law:
        Residuals are NON-DELETABLE in serialization.
        Deserialization MUST preserve residuals exactly.

    Fields:
        residuals: Residual set (from algorithm output)
        residual_sources: Sources of residuals (which gates/operations)
        blocking_count: Count of blocking residuals

    Forbidden:
        - Deleting residuals in deserialization
        - Hiding blocking residuals
    """
    residuals: ResidualSet
    residual_sources: Tuple[str, ...]
    blocking_count: int

    def __post_init__(self):
        """Validate residual trace payload."""
        if not isinstance(self.residuals, ResidualSet):
            raise TypeError(f"residuals must be ResidualSet, got {type(self.residuals)}")
        if not isinstance(self.residual_sources, tuple):
            raise TypeError(f"residual_sources must be tuple, got {type(self.residual_sources)}")
        if not isinstance(self.blocking_count, int):
            raise TypeError(f"blocking_count must be int, got {type(self.blocking_count)}")
        if self.blocking_count < 0:
            raise ValueError("blocking_count cannot be negative")


# ============================================================================
# Relation Trace Payload
# ============================================================================

@dataclass(frozen=True)
class RelationTracePayload:
    """
    Relation trace for audit purposes.

    Constitutional Law:
        RelationTracePayload describes what algorithm produced.
        It does NOT authorize relation as constitutional fact.

    Fields:
        relation_id: Unique identifier for this relation
        relation_type: Type of relation (predicative/inclusion/restrictive/reference)
        anchor_id: Anchor identity (preserved)
        related_id: Related term identity
        trace: Operational trace
        rank_payload: Rank trace
        residual_payload: Residual trace

    Forbidden:
        - Creating RelationCandidate from payload without algorithm
        - Upgrading rank
        - Deleting residuals
    """
    relation_id: str
    relation_type: str
    anchor_id: str
    related_id: str
    trace: Tuple[str, ...]
    rank_payload: RankTracePayload
    residual_payload: ResidualTracePayload

    def __post_init__(self):
        """Validate relation trace payload."""
        if not self.relation_id:
            raise ValueError("RelationTracePayload requires non-empty relation_id")
        if not self.relation_type:
            raise ValueError("RelationTracePayload requires non-empty relation_type")
        if not self.anchor_id:
            raise ValueError("RelationTracePayload requires non-empty anchor_id")
        if not self.related_id:
            raise ValueError("RelationTracePayload requires non-empty related_id")
        if not isinstance(self.trace, tuple):
            raise TypeError(f"trace must be tuple, got {type(self.trace)}")
        if not self.trace:
            raise ValueError("RelationTracePayload requires non-empty trace")
        if not isinstance(self.rank_payload, RankTracePayload):
            raise TypeError(f"rank_payload must be RankTracePayload, got {type(self.rank_payload)}")
        if not isinstance(self.residual_payload, ResidualTracePayload):
            raise TypeError(
                f"residual_payload must be ResidualTracePayload, got {type(self.residual_payload)}"
            )


# ============================================================================
# Network Trace Payload
# ============================================================================

@dataclass(frozen=True)
class NetworkTracePayload:
    """
    Relation network trace for audit purposes.

    Constitutional Law:
        NetworkTracePayload describes network structure.
        It does NOT close ifadah.
        It does NOT produce hukm.

    Fields:
        network_id: Unique identifier for this network
        relations: Tuple of relation traces
        network_status: Status (open_candidate/closable_candidate/blocked)
        closure_eligible: Whether network meets basic closure preconditions
        closure_residuals: Network-level closure residuals

    Forbidden:
        - Closing ifadah from network payload
        - Producing hukm from network payload
        - Creating network candidate without algorithm
    """
    network_id: str
    relations: Tuple[RelationTracePayload, ...]
    network_status: str
    closure_eligible: bool
    closure_residuals: ResidualTracePayload

    def __post_init__(self):
        """Validate network trace payload."""
        if not self.network_id:
            raise ValueError("NetworkTracePayload requires non-empty network_id")
        if not isinstance(self.relations, tuple):
            raise TypeError(f"relations must be tuple, got {type(self.relations)}")
        if not self.relations:
            raise ValueError("NetworkTracePayload requires non-empty relations")
        for i, rel in enumerate(self.relations):
            if not isinstance(rel, RelationTracePayload):
                raise TypeError(
                    f"relations[{i}] must be RelationTracePayload, got {type(rel)}"
                )
        if not self.network_status:
            raise ValueError("NetworkTracePayload requires non-empty network_status")
        if not isinstance(self.closure_eligible, bool):
            raise TypeError(f"closure_eligible must be bool, got {type(self.closure_eligible)}")
        if not isinstance(self.closure_residuals, ResidualTracePayload):
            raise TypeError(
                f"closure_residuals must be ResidualTracePayload, "
                f"got {type(self.closure_residuals)}"
            )


# ============================================================================
# Candidate Trace Payload
# ============================================================================

@dataclass(frozen=True)
class CandidateTracePayload:
    """
    Generic candidate trace for audit purposes.

    Constitutional Law:
        CandidateTracePayload is audit trail, not authority.
        It describes what algorithm produced, not what is constitutionally true.

    Fields:
        candidate_id: Unique identifier
        candidate_type: Type of candidate (RelationCandidate/WordformCandidate/etc.)
        layer: Layer where candidate was produced
        trace: Operational trace
        rank_payload: Rank trace
        residual_payload: Residual trace
        forbidden_outputs: Forbidden operations for this candidate

    Forbidden:
        - Creating candidate object from payload without algorithm
        - Upgrading rank
        - Deleting residuals
        - Executing forbidden_outputs
    """
    candidate_id: str
    candidate_type: str
    layer: str
    trace: Tuple[str, ...]
    rank_payload: RankTracePayload
    residual_payload: ResidualTracePayload
    forbidden_outputs: Tuple[str, ...]

    def __post_init__(self):
        """Validate candidate trace payload."""
        if not self.candidate_id:
            raise ValueError("CandidateTracePayload requires non-empty candidate_id")
        if not self.candidate_type:
            raise ValueError("CandidateTracePayload requires non-empty candidate_type")
        if not self.layer:
            raise ValueError("CandidateTracePayload requires non-empty layer")
        if not isinstance(self.trace, tuple):
            raise TypeError(f"trace must be tuple, got {type(self.trace)}")
        if not self.trace:
            raise ValueError("CandidateTracePayload requires non-empty trace")
        if not isinstance(self.rank_payload, RankTracePayload):
            raise TypeError(f"rank_payload must be RankTracePayload, got {type(self.rank_payload)}")
        if not isinstance(self.residual_payload, ResidualTracePayload):
            raise TypeError(
                f"residual_payload must be ResidualTracePayload, "
                f"got {type(self.residual_payload)}"
            )
        if not isinstance(self.forbidden_outputs, tuple):
            raise TypeError(f"forbidden_outputs must be tuple, got {type(self.forbidden_outputs)}")


# ============================================================================
# Main Algorithm Trace Payload
# ============================================================================

@dataclass(frozen=True)
class AlgorithmTracePayload:
    """
    Complete algorithm trace payload (حمولة أثر الخوارزمية الكاملة).

    Constitutional Law:
        AlgorithmTracePayload is replay/audit evidence, NOT ProofObject authority.

        الأثر يصف ما أنتجته الخوارزمية.
        الأثر لا ينشئ مرشحًا جديدًا.
        الأثر لا يرفع الرتبة.
        الأثر لا يحذف البقايا.
        الأثر لا يغلق الإفادة.

        (The trace describes what algorithm produced.
         The trace does not create new candidates.
         The trace does not upgrade rank.
         The trace does not delete residuals.
         The trace does not close ifadah.)

        Constitutional Requirement:
            Payload must contain EITHER:
            - Non-empty candidates (successful algorithm execution), OR
            - Explicit blocking residuals (blocked/invalid/foreign input)

            This allows representing both:
            1. Successful analysis with candidates
            2. Blocked analysis with no candidates but blocking residuals

    Fields:
        trace_id: Unique identifier for this specific trace execution
        schema_version: Payload schema version (for evolution)
        source_algorithm: Algorithm that produced this trace
        source_layer: Layer where algorithm executed
        input_surface: Optional surface input (e.g., "زيد قائم")
        candidates: Tuple of candidate traces
        network: Optional network trace
        allowed_next_layers: Constitutionally allowed next layers
        forbidden_jumps: Forbidden domain jumps

    Forbidden Methods (MUST NOT exist):
        - to_hukm()
        - to_reality()
        - to_ifadah()
        - close_ifadah()
        - create_candidate()
        - upgrade_rank()
        - delete_residuals()

    Permitted Use:
        - Audit/replay of algorithm execution
        - Input to GovernedTraceT5 for explanation/ranking/repair suggestion
        - Serialization for storage/transmission
    """
    trace_id: str
    schema_version: str
    source_algorithm: str
    source_layer: str
    input_surface: Optional[str]
    candidates: Tuple[CandidateTracePayload, ...]
    network: Optional[NetworkTracePayload]
    allowed_next_layers: Tuple[AllowedNextLayerPayload, ...]
    forbidden_jumps: Tuple[ForbiddenJumpPayload, ...]

    def __post_init__(self):
        """
        Validate algorithm trace payload invariants.

        Constitutional guards:
            - trace_id required (unique execution identifier)
            - schema_version required
            - source_algorithm required
            - source_layer required
            - candidates required (non-empty)
            - forbidden_jumps required (may be empty tuple)
            - allowed_next_layers required (may be empty tuple)
        """
        # Validate trace_id
        if not self.trace_id:
            raise ValueError("AlgorithmTracePayload requires non-empty trace_id")
        if not isinstance(self.trace_id, str):
            raise TypeError(f"trace_id must be str, got {type(self.trace_id)}")

        # Validate schema_version
        if not self.schema_version:
            raise ValueError("AlgorithmTracePayload requires non-empty schema_version")
        if not isinstance(self.schema_version, str):
            raise TypeError(f"schema_version must be str, got {type(self.schema_version)}")

        # Validate source_algorithm
        if not self.source_algorithm:
            raise ValueError("AlgorithmTracePayload requires non-empty source_algorithm")
        if not isinstance(self.source_algorithm, str):
            raise TypeError(f"source_algorithm must be str, got {type(self.source_algorithm)}")

        # Validate source_layer
        if not self.source_layer:
            raise ValueError("AlgorithmTracePayload requires non-empty source_layer")
        if not isinstance(self.source_layer, str):
            raise TypeError(f"source_layer must be str, got {type(self.source_layer)}")

        # Validate input_surface (optional)
        if self.input_surface is not None and not isinstance(self.input_surface, str):
            raise TypeError(f"input_surface must be str or None, got {type(self.input_surface)}")

        # Validate candidates
        if not isinstance(self.candidates, tuple):
            raise TypeError(f"candidates must be tuple, got {type(self.candidates)}")

        # Constitutional requirement: Payload must represent valid algorithm execution
        # Either candidates OR blocking residuals must be present
        # (Algorithm may produce no candidates if input is blocked/invalid/foreign)
        if not self.candidates:
            # No candidates - this is allowed only if there are explicit blocking residuals
            # Check if network has blocking residuals (for blocked algorithm case)
            has_blocking_residuals = (
                self.network is not None and
                self.network.closure_residuals.blocking_count > 0
            )
            if not has_blocking_residuals:
                raise ValueError(
                    "AlgorithmTracePayload requires either non-empty candidates "
                    "OR explicit blocking residuals (for blocked/invalid input cases)"
                )

        for i, cand in enumerate(self.candidates):
            if not isinstance(cand, CandidateTracePayload):
                raise TypeError(
                    f"candidates[{i}] must be CandidateTracePayload, got {type(cand)}"
                )

        # Validate network (optional)
        if self.network is not None and not isinstance(self.network, NetworkTracePayload):
            raise TypeError(f"network must be NetworkTracePayload or None, got {type(self.network)}")

        # Validate allowed_next_layers
        if not isinstance(self.allowed_next_layers, tuple):
            raise TypeError(
                f"allowed_next_layers must be tuple, got {type(self.allowed_next_layers)}"
            )
        for i, layer in enumerate(self.allowed_next_layers):
            if not isinstance(layer, AllowedNextLayerPayload):
                raise TypeError(
                    f"allowed_next_layers[{i}] must be AllowedNextLayerPayload, got {type(layer)}"
                )

        # Validate forbidden_jumps
        if not isinstance(self.forbidden_jumps, tuple):
            raise TypeError(f"forbidden_jumps must be tuple, got {type(self.forbidden_jumps)}")
        for i, jump in enumerate(self.forbidden_jumps):
            if not isinstance(jump, ForbiddenJumpPayload):
                raise TypeError(
                    f"forbidden_jumps[{i}] must be ForbiddenJumpPayload, got {type(jump)}"
                )

    @property
    def is_non_authoritative(self) -> bool:
        """
        Confirm that payload is non-authoritative.

        Constitutional Law:
            Payload describes algorithm output but does NOT constitute proof.
            Payload is audit evidence, not constitutional authority.

        Returns:
            True (always - this is a constitutional invariant)
        """
        return True

    @property
    def forbidden_operations(self) -> Tuple[str, ...]:
        """
        List forbidden operations on this payload.

        Returns:
            Tuple of forbidden operation names
        """
        return (
            "to_hukm",
            "to_reality",
            "to_ifadah",
            "close_ifadah",
            "create_candidate",
            "upgrade_rank",
            "delete_residuals",
        )
