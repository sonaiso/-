"""
ProofObject - Layer-agnostic proof structure.

ProofObject is NOT a test report. It is a layer validity condition that
documents what a layer certifies, what it forbids, and what limitations
it has.

Every layer (U₀, U₁, U₂, ...) produces a ProofObject documenting:
    - claim: What this layer certifies
    - scope: Boundaries of certification (which layer)
    - evidence: What was checked
    - counter_evidence: What failed
    - trace_graph: Trace to lower layers
    - competitors: Competing interpretations preserved
    - residuals: Warnings/blockers
    - rank_vector: Epistemic status across all layers
    - allowed_next_gates: Permitted transitions
    - forbidden_next_gates: Blocked transitions
    - limitations: Known boundaries

Laws:
    - ProofObject is immutable (frozen)
    - forbidden_next_gates prevents layer jumping
    - rank_vector shows only current layer can have high rank
    - limitations explicitly document boundaries

Architecture:
    ProofObject is general, not U₀-specific.
    Each layer fills it with layer-appropriate values.

PR: U0-STRICT-TYPE-SYSTEM (Foundation extraction)
Created: 2026-05-25
"""

from dataclasses import dataclass
from typing import FrozenSet, Dict, Any, Optional

from dal_core.residuals import Residual
from dal_core.foundation.rank import Rank


@dataclass(frozen=True)
class ProofObject:
    """
    Layer-agnostic proof structure.

    Documents what a layer certifies and what it forbids.

    Fields:
        claim: Human-readable claim (e.g., "Unicode scalars classified")
        scope: Layer identifier (e.g., "U₀ / UnicodeCarrier")
        evidence: Set of verification statements
        counter_evidence: Set of violations/failures
        trace_graph: Trace structure to lower layers
        competitors: Competing interpretations (preserved, not resolved)
        residuals: All residuals from this layer
        rank_vector: Rank status across all layers (dict form)
        allowed_next_gates: Operations permitted from this layer
        forbidden_next_gates: Operations forbidden from this layer
        limitations: Explicit boundaries of this layer's capabilities
        metadata: Optional additional information

    Usage:
        proof = make_proof_object(
            claim="Unicode scalars classified",
            scope="U₀",
            ...
        )

    Laws:
        - ProofObject is immutable
        - forbidden_next_gates must include higher-layer certificates
        - rank_vector must show ZERO for uncertified layers
        - limitations must be explicit
    """
    claim: str
    scope: str
    evidence: FrozenSet[str]
    counter_evidence: FrozenSet[str]
    trace_graph: Dict[str, Any]
    competitors: FrozenSet[str]
    residuals: FrozenSet[Residual]
    rank_vector: Dict[str, Rank]  # Serialized form of RankVector
    allowed_next_gates: FrozenSet[str]
    forbidden_next_gates: FrozenSet[str]
    limitations: FrozenSet[str]
    metadata: Optional[Dict[str, Any]] = None

    def has_blocking_failures(self) -> bool:
        """Check if proof has blocking residuals."""
        return any(r.is_blocker() for r in self.residuals)

    def is_gate_allowed(self, gate: str) -> bool:
        """Check if a gate/operation is allowed."""
        return gate in self.allowed_next_gates

    def is_gate_forbidden(self, gate: str) -> bool:
        """Check if a gate/operation is forbidden."""
        return gate in self.forbidden_next_gates

    def get_rank_for_layer(self, layer: str) -> Optional[Rank]:
        """Get rank for specific layer."""
        return self.rank_vector.get(layer)


def make_proof_object(
    claim: str,
    scope: str,
    evidence: FrozenSet[str],
    counter_evidence: FrozenSet[str],
    trace_graph: Dict[str, Any],
    competitors: FrozenSet[str],
    residuals: FrozenSet[Residual],
    rank_vector: Dict[str, Rank],
    allowed_next_gates: FrozenSet[str],
    forbidden_next_gates: FrozenSet[str],
    limitations: FrozenSet[str],
    metadata: Optional[Dict[str, Any]] = None
) -> ProofObject:
    """
    Factory function for creating ProofObject.

    Validates consistency before creation.

    Args:
        claim: Human-readable claim
        scope: Layer identifier
        evidence: Set of verification statements
        counter_evidence: Set of violations
        trace_graph: Trace to lower layers
        competitors: Competing interpretations
        residuals: All residuals
        rank_vector: Rank status (dict form)
        allowed_next_gates: Permitted operations
        forbidden_next_gates: Blocked operations
        limitations: Explicit boundaries
        metadata: Optional additional info

    Returns:
        ProofObject instance

    Raises:
        ValueError: If validation fails
    """
    # Validation: allowed and forbidden should be disjoint
    if allowed_next_gates & forbidden_next_gates:
        overlap = allowed_next_gates & forbidden_next_gates
        raise ValueError(f"Gates cannot be both allowed and forbidden: {overlap}")

    # Validation: rank_vector should contain recognized ranks
    valid_rank_keys = {
        "unicode_rank", "grapheme_rank", "phonetic_rank", "syllable_rank",
        "functional_role_rank", "morpheme_rank", "stem_root_rank",
        "pattern_weight_rank", "semantic_rank", "hukm_rank"
    }

    for key in rank_vector.keys():
        if key not in valid_rank_keys:
            raise ValueError(f"Unknown rank key: {key}")

    return ProofObject(
        claim=claim,
        scope=scope,
        evidence=evidence,
        counter_evidence=counter_evidence,
        trace_graph=trace_graph,
        competitors=competitors,
        residuals=residuals,
        rank_vector=rank_vector,
        allowed_next_gates=allowed_next_gates,
        forbidden_next_gates=forbidden_next_gates,
        limitations=limitations,
        metadata=metadata
    )
