"""
Path-Aware Identity Validator (PR-128)

Validates that identity transitions only occur through licensed paths.

Constitutional Law:
    لا هوية بلا مسار مرخّص
    No identity without licensed path.

PR-127 correctly removed unconditional WEIGHT_DOMAIN requirement from IDENTITY_DOMAIN.
PR-128 adds path-aware validation at transition time to prevent permissive holes.

Licensed Identity Paths:
1. Weight path: ROOT/STEM → WEIGHT → IDENTITY
2. Mabni/closed-class path: LAFZ → MABNI → IDENTITY
3. Tool/particle path: LAFZ → TOOL → IDENTITY
4. Pronoun path: LAFZ → PRONOUN → IDENTITY
5. Jāmid/frozen path: LAFZ → JĀMID → IDENTITY
6. Residualized identity path: existing identity with residuals

Algebraic Properties:
- Returns AlgebraicFailure (not Exception) for operation failures
- Preserves lafz_anchor_id and slot_trace where available
- Does NOT produce meaning, syntactic_role, iʿrab, ifādah, or hukm
- Validates at transition time, not structure time

Created: 2026-05-27 (PR-128)
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple, Any, Dict, FrozenSet
from types import MappingProxyType

from dal_core.dal_algebra import AlgebraicFailure
from dal_core.domain_registry import DomainType, DomainRegistry
from dal_core.identity_registry import IdentityType, IdentityRegistry


# ============================================================================
# Licensed Path Enumeration
# ============================================================================

class IdentityPathType(Enum):
    """Licensed paths to identity determination."""
    WEIGHT_PATH = auto()          # Root/Stem → Weight → Identity
    MABNI_PATH = auto()           # Lafz → Mabni → Identity (closed-class)
    TOOL_PATH = auto()            # Lafz → Tool → Identity (particles)
    PRONOUN_PATH = auto()         # Lafz → Pronoun → Identity
    JAMID_PATH = auto()           # Lafz → Jāmid → Identity (frozen nouns)
    RESIDUALIZED_PATH = auto()    # Existing identity with residuals


@dataclass(frozen=True)
class PathEvidence:
    """Evidence for a licensed identity path.

    Attributes:
        path_type: Which licensed path is being used
        source_domain: Where the path originates (e.g., LAFZ_DOMAIN, WEIGHT_DOMAIN)
        evidence_present: Whether required evidence exists
        lafz_anchor_id: Optional lafz anchor ID (preserved)
        slot_trace: Optional slot trace (preserved)
        details: Additional path-specific evidence
    """
    path_type: IdentityPathType
    source_domain: DomainType
    evidence_present: bool
    lafz_anchor_id: Optional[str] = None
    slot_trace: Optional[Tuple[int, ...]] = None
    details: MappingProxyType = MappingProxyType({})

    def __post_init__(self):
        """Validate path evidence invariants."""
        if not isinstance(self.details, MappingProxyType):
            # Coerce to immutable
            object.__setattr__(self, "details", MappingProxyType(dict(self.details)))


@dataclass(frozen=True)
class IdentityCandidate:
    """Identity candidate with path evidence.

    This is the validated output of path-aware identity validation.

    Attributes:
        identity_type: The identity being claimed (e.g., WORDFORM_IDENTITY)
        path_evidence: Evidence for the licensed path used
        rank: Candidate rank (NOT CERTIFICATE)
        residuals: Unresolved residuals from transition
        lafz_anchor_id: Preserved lafz anchor ID
        slot_trace: Preserved slot trace
    """
    identity_type: IdentityType
    path_evidence: PathEvidence
    rank: float  # Candidate rank, not certificate
    residuals: Tuple[str, ...] = ()
    lafz_anchor_id: Optional[str] = None
    slot_trace: Optional[Tuple[int, ...]] = None

    def __post_init__(self):
        """Validate identity candidate invariants."""
        if self.rank < 0.0:
            raise ValueError(f"Rank must be non-negative, got {self.rank}")
        if self.rank >= 1.0:
            raise ValueError(
                f"Rank must be < 1.0 (CERTIFICATE forbidden), got {self.rank}"
            )
        if not isinstance(self.residuals, tuple):
            object.__setattr__(self, "residuals", tuple(self.residuals))
        if not isinstance(self.slot_trace, tuple) and self.slot_trace is not None:
            object.__setattr__(self, "slot_trace", tuple(self.slot_trace))


# ============================================================================
# Path-Aware Identity Validator
# ============================================================================

class PathAwareIdentityValidator:
    """
    Validates identity transitions through licensed paths only.

    Constitutional Law:
        لا هوية بلا مسار مرخّص
        No identity without licensed path.

    Prohibitions (enforced):
        - No meaning output
        - No syntactic_role output
        - No iʿrab output
        - No ifādah output
        - No hukm output
        - No CERTIFICATE rank (rank < 1.0 always)

    Usage:
        validator = PathAwareIdentityValidator()
        result = validator.validate_identity_transition(
            source_domain=DomainType.WEIGHT_DOMAIN,
            target_identity=IdentityType.WORDFORM_IDENTITY,
            path_type=IdentityPathType.WEIGHT_PATH,
            evidence={...}
        )

        if isinstance(result, AlgebraicFailure):
            # Handle failure
            print(result.reason)
        else:
            # Use identity candidate
            identity_candidate = result
    """

    def __init__(self):
        """Initialize validator with registries."""
        self.domain_registry = DomainRegistry()
        self.identity_registry = IdentityRegistry()

        # Build licensed path mapping (immutable)
        self._licensed_paths = self._build_licensed_paths()

    def _build_licensed_paths(self) -> MappingProxyType:
        """Build mapping of licensed identity paths.

        Returns:
            Immutable mapping: IdentityPathType → (allowed_source_domains, required_evidence_keys)
        """
        paths = {
            IdentityPathType.WEIGHT_PATH: (
                frozenset({DomainType.WEIGHT_DOMAIN}),
                frozenset({"weight_pattern", "root_or_stem"})
            ),
            IdentityPathType.MABNI_PATH: (
                frozenset({DomainType.LAFZ_DOMAIN, DomainType.IDENTITY_DOMAIN}),
                frozenset({"closed_class_marker"})
            ),
            IdentityPathType.TOOL_PATH: (
                frozenset({DomainType.LAFZ_DOMAIN, DomainType.IDENTITY_DOMAIN}),
                frozenset({"particle_type"})
            ),
            IdentityPathType.PRONOUN_PATH: (
                frozenset({DomainType.LAFZ_DOMAIN, DomainType.IDENTITY_DOMAIN}),
                frozenset({"pronoun_class"})
            ),
            IdentityPathType.JAMID_PATH: (
                frozenset({DomainType.LAFZ_DOMAIN, DomainType.IDENTITY_DOMAIN}),
                frozenset({"jamid_marker"})
            ),
            IdentityPathType.RESIDUALIZED_PATH: (
                frozenset({DomainType.IDENTITY_DOMAIN}),
                frozenset({"existing_identity", "residuals"})
            ),
        }
        return MappingProxyType(paths)

    def validate_identity_transition(
        self,
        source_domain: DomainType,
        target_identity: IdentityType,
        path_type: IdentityPathType,
        evidence: Dict[str, Any],
        lafz_anchor_id: Optional[str] = None,
        slot_trace: Optional[Tuple[int, ...]] = None,
        residuals: Tuple[str, ...] = ()
    ) -> IdentityCandidate | AlgebraicFailure:
        """
        Validate identity transition through licensed path.

        Args:
            source_domain: Domain where transition originates
            target_identity: Identity type being claimed
            path_type: Which licensed path is being used
            evidence: Path-specific evidence (dict with required keys)
            lafz_anchor_id: Optional lafz anchor ID (preserved)
            slot_trace: Optional slot trace (preserved)
            residuals: Unresolved residuals from transition

        Returns:
            IdentityCandidate if valid, AlgebraicFailure if invalid

        Validation Steps:
            1. Check path_type is licensed
            2. Check source_domain matches path requirements
            3. Check required evidence is present
            4. Check target_identity is allowed from source_domain
            5. Check no prohibited outputs (meaning, syntax, iʿrab, ifādah, hukm)
            6. Compute rank (always < 1.0, never CERTIFICATE)
            7. Build IdentityCandidate
        """
        # Step 1: Check path_type is licensed
        if path_type not in self._licensed_paths:
            return AlgebraicFailure(
                reason=f"Path type {path_type} not licensed",
                forbidden_path=str(path_type),
                gate="licensed_path_gate"
            )

        allowed_sources, required_evidence_keys = self._licensed_paths[path_type]

        # Step 2: Check source_domain matches path requirements
        if source_domain not in allowed_sources:
            return AlgebraicFailure(
                reason=(
                    f"Source domain {source_domain} not allowed for path {path_type}. "
                    f"Allowed: {allowed_sources}"
                ),
                domain_violation=f"{source_domain} → {target_identity} via {path_type}",
                gate="source_domain_gate"
            )

        # Step 3: Check required evidence is present
        missing_evidence = required_evidence_keys - evidence.keys()
        if missing_evidence:
            return AlgebraicFailure(
                reason=(
                    f"Missing required evidence for path {path_type}: "
                    f"{', '.join(missing_evidence)}"
                ),
                evidence_gap=f"Required: {required_evidence_keys}, Got: {evidence.keys()}",
                gate="evidence_gate"
            )

        # Step 4: Check target_identity is allowed from source_domain
        # (This is a basic check; full validation would check IdentityRegistry)
        # For now, just ensure target_identity is in the registry
        try:
            identity_spec = self.identity_registry.get_spec(target_identity)
        except KeyError:
            return AlgebraicFailure(
                reason=f"Target identity {target_identity} not found in registry",
                gate="identity_registry_gate"
            )

        # Step 5: Check no prohibited outputs
        # (This is enforced by NOT including those fields in IdentityCandidate)
        # Validator itself does NOT produce meaning/syntax/iʿrab/ifādah/hukm

        # Step 6: Compute rank (always < 1.0)
        # Simple rank calculation based on evidence quality
        # (In production, this would be more sophisticated)
        rank = 0.8  # Default candidate rank (< 1.0, not certificate)
        if "confidence" in evidence:
            rank = min(0.99, float(evidence["confidence"]))

        # Step 7: Build path evidence
        path_evidence = PathEvidence(
            path_type=path_type,
            source_domain=source_domain,
            evidence_present=True,
            lafz_anchor_id=lafz_anchor_id,
            slot_trace=slot_trace,
            details=MappingProxyType(evidence)
        )

        # Step 8: Build IdentityCandidate
        return IdentityCandidate(
            identity_type=target_identity,
            path_evidence=path_evidence,
            rank=rank,
            residuals=residuals,
            lafz_anchor_id=lafz_anchor_id,
            slot_trace=slot_trace
        )

    def validate_no_path_rejection(
        self,
        source_domain: DomainType,
        target_identity: IdentityType,
        evidence: Dict[str, Any]
    ) -> AlgebraicFailure:
        """
        Validate that identity transition is REJECTED when no path evidence exists.

        This is a negative test helper: verifies that missing path evidence
        causes rejection, not acceptance.

        Args:
            source_domain: Domain where transition originates
            target_identity: Identity type being claimed
            evidence: Evidence dict (should be empty or incomplete)

        Returns:
            AlgebraicFailure explaining why transition was rejected
        """
        # Try all licensed paths, all should fail
        failures = []

        for path_type in IdentityPathType:
            result = self.validate_identity_transition(
                source_domain=source_domain,
                target_identity=target_identity,
                path_type=path_type,
                evidence=evidence
            )

            if isinstance(result, AlgebraicFailure):
                failures.append((path_type, result))
            else:
                # This should NOT happen - identity accepted without valid path
                return AlgebraicFailure(
                    reason=(
                        f"VALIDATION ERROR: Identity {target_identity} accepted "
                        f"via {path_type} without proper path evidence"
                    ),
                    gate="no_path_rejection_gate",
                    forbidden_path="permissive_hole"
                )

        # All paths failed (correct behavior)
        return AlgebraicFailure(
            reason=(
                f"Identity {target_identity} rejected: no licensed path from "
                f"{source_domain}. Tried {len(failures)} paths, all failed."
            ),
            gate="licensed_path_gate",
            evidence_gap="No valid path evidence for any licensed path"
        )


__all__ = [
    "IdentityPathType",
    "PathEvidence",
    "IdentityCandidate",
    "PathAwareIdentityValidator",
]
