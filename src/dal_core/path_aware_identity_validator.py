"""
Path-Aware Identity Validator (PR-128)

Validates that identity transitions only occur through licensed paths.

Constitutional Law:
    لا هوية بلا مسار مرخّص
    No identity without licensed path.

PR-127 correctly removed unconditional WEIGHT_DOMAIN requirement from IDENTITY_DOMAIN.
PR-128 adds path-aware validation at transition time to prevent permissive holes.

**Implementation Status: FOUNDATION-ONLY (2026-05-27)**

This module provides the foundation for path-aware identity validation.
Integration with AlgebraicDecisionCore and ApprovedTransitionContext is pending.

Current status:
- ✅ PathAwareIdentityValidator class implemented
- ✅ 6 licensed paths defined and validated
- ✅ Target identity whitelist/blacklist enforced
- ✅ Rank enum + confidence float separation
- ✅ AlgebraicFailure returns for operation failures
- ✅ 30+ tests covering all paths + forbidden targets
- ⚠️  Integration with core pipeline pending (future work)

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
Updated: 2026-05-27 (PR-128 fixes: whitelist, rank enum, tests)
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Tuple, Any, Dict, FrozenSet
from types import MappingProxyType

from dal_core.dal_algebra import AlgebraicFailure
from dal_core.domain_registry import DomainType, DomainRegistry
from dal_core.identity_registry import IdentityType, IdentityRegistry
from dal_core.pipeline import Rank


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
        rank: Epistemic rank (from Rank enum, NOT Rank.CERT)
        confidence: Confidence score [0.0, 1.0) for this candidate
        residuals: Unresolved residuals from transition
        lafz_anchor_id: Preserved lafz anchor ID
        slot_trace: Preserved slot trace
    """
    identity_type: IdentityType
    path_evidence: PathEvidence
    rank: Rank  # Epistemic rank enum (FORM, QIYAS, AHAD, TAWATUR - NOT CERT)
    confidence: float  # Confidence score [0.0, 1.0)
    residuals: Tuple[str, ...] = ()
    lafz_anchor_id: Optional[str] = None
    slot_trace: Optional[Tuple[int, ...]] = None

    def __post_init__(self):
        """Validate identity candidate invariants."""
        # Rank must NOT be CERT (certificate)
        if self.rank == Rank.CERT:
            raise ValueError(
                f"Rank.CERT (CERTIFICATE) forbidden in IdentityCandidate, got {self.rank}"
            )

        # Confidence must be in [0.0, 1.0)
        if self.confidence < 0.0:
            raise ValueError(f"Confidence must be non-negative, got {self.confidence}")
        if self.confidence >= 1.0:
            raise ValueError(
                f"Confidence must be < 1.0 (certainty forbidden), got {self.confidence}"
            )

        # Coerce to immutable types
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

        # Build allowed target identities whitelist (immutable)
        self._allowed_target_identities = self._build_allowed_target_identities()

        # Build forbidden target identities blacklist (immutable)
        self._forbidden_target_identities = self._build_forbidden_target_identities()

    def _build_allowed_target_identities(self) -> FrozenSet[IdentityType]:
        """Build whitelist of allowed target identities.

        Constitutional Law:
            Identity path validation targets IDENTITY_AXIS candidates and
            WORDFORM_IDENTITY, NOT semantic/judgment/functional layers.

        Returns:
            Immutable set of allowed target identity types
        """
        allowed = {
            # Layer 4: Lafz identities
            IdentityType.LAFZ_IDENTITY,

            # Layer 8: Root/Stem candidates (NOT certificates)
            IdentityType.ROOT_MATERIAL_IDENTITY,
            IdentityType.STEM_IDENTITY,

            # Layer 9: Weight identities
            IdentityType.WEIGHT_IDENTITY,

            # Layer 10: Word form identities
            IdentityType.WORDFORM_IDENTITY,
            IdentityType.FORM_IDENTITY,

            # Closed class identities
            IdentityType.CLOSED_CLASS_IDENTITY,

            # Derivational identities (if licensed)
            IdentityType.SOURCE_IDENTITY,
            IdentityType.ATTRIBUTE_IDENTITY,
        }
        return frozenset(allowed)

    def _build_forbidden_target_identities(self) -> FrozenSet[IdentityType]:
        """Build blacklist of forbidden target identities.

        Constitutional Law:
            Identity path validation MUST NOT target:
            - Semantic identities (meaning layer)
            - Judgment identities (hukm layer)
            - Ifādah identities (pragmatic closure)
            - Functional relation identities (syntax layer)
            - Operator identities (ʿāmil/maʿmūl)

        These identities arise AFTER identity determination, not during it.

        Returns:
            Immutable set of forbidden target identity types
        """
        forbidden = {
            # Semantic layer (FORBIDDEN)
            IdentityType.SEMANTIC_IDENTITY,

            # Ifādah layer (FORBIDDEN)
            IdentityType.IFADAH_IDENTITY,

            # Judgment layer (FORBIDDEN)
            IdentityType.HUKM_IDENTITY,

            # Functional relation layer (FORBIDDEN)
            IdentityType.FUNCTIONAL_RELATION_IDENTITY,

            # Operator identities (FORBIDDEN)
            IdentityType.AMIL_IDENTITY,
            IdentityType.MAAMUL_IDENTITY,

            # Relation composition (FORBIDDEN at identity stage)
            IdentityType.RELATION_COMPOSITION_IDENTITY,
        }
        return frozenset(forbidden)

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

        # Step 4: Check target_identity is whitelisted (NOT forbidden)
        # CRITICAL: Prevent semantic/judgment/functional identities
        if target_identity in self._forbidden_target_identities:
            return AlgebraicFailure(
                reason=(
                    f"Target identity {target_identity} is FORBIDDEN. "
                    f"Identity path validation cannot target semantic/judgment/functional layers. "
                    f"Forbidden identities: {self._forbidden_target_identities}"
                ),
                forbidden_path=f"path → {target_identity}",
                gate="forbidden_target_identity_gate"
            )

        # Check target_identity is in allowed whitelist
        if target_identity not in self._allowed_target_identities:
            return AlgebraicFailure(
                reason=(
                    f"Target identity {target_identity} not in allowed whitelist. "
                    f"Allowed identities: {self._allowed_target_identities}"
                ),
                gate="allowed_target_identity_gate"
            )

        # Verify target_identity exists in registry
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

        # Step 6: Compute rank and confidence
        # Use Rank enum (FORM/QIYAS/AHAD/TAWATUR), NOT Rank.CERT
        # Confidence is separate float [0.0, 1.0)
        rank = Rank.FORM  # Default: candidate rank (form-based)
        confidence = 0.8  # Default confidence

        if "confidence" in evidence:
            confidence = min(0.99, float(evidence["confidence"]))

        if "rank" in evidence:
            # Allow evidence to suggest rank (but validate it)
            suggested_rank = evidence["rank"]
            if isinstance(suggested_rank, Rank) and suggested_rank != Rank.CERT:
                rank = suggested_rank
            elif isinstance(suggested_rank, str):
                # Map string to Rank (e.g., "QIYAS" → Rank.QIYAS)
                try:
                    rank_candidate = Rank[suggested_rank.upper()]
                    if rank_candidate != Rank.CERT:
                        rank = rank_candidate
                except (KeyError, AttributeError):
                    pass  # Keep default FORM rank

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
            confidence=confidence,
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
